from celery import Celery
from flask import current_app
from datetime import datetime, timezone
from db import Message, ContactTransact, Gateway, SMSPricing, db
from gateway import send_sms_via_gateway, normalize_number, chunk_list, get_gateway_balance
from main import create_app
import redis
import uuid
import os
# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
MIN_BALANCE = 500        # Naira
MAX_RETRIES = 3          # Max retries for transient failures
BACKOFF_LIMIT = 3600     # 1 hour max delay
LOCK_TIMEOUT = 300       # 5 minutes lock to prevent duplicates

# ---------------------------------------------------------------------
# CELERY SETUP
# ---------------------------------------------------------------------
celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/1")
)

flask_app = create_app()

class ContextTask(celery.Task):
    """Ensure Flask context is available for all Celery tasks."""
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# ---------------------------------------------------------------------
# REDIS LOCK SETUP
# ---------------------------------------------------------------------
redis_client = redis.Redis(host="localhost", port=6379, db=2)

def acquire_lock(message_id: int):
    lock_name = f"lock:message:{message_id}"
    token = str(uuid.uuid4())
    lock = redis_client.lock(lock_name, timeout=LOCK_TIMEOUT, thread_local=False)
    acquired = lock.acquire(blocking=False, token=token)
    return acquired, lock, token

# ---------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------
def assign_gateways_round_robin(pending_cts, gateways):
    """Assign contacts evenly across gateways on first send."""
    assignments = {g.id: [] for g in gateways}
    gw_list = list(gateways)
    gw_count = len(gw_list)
    for idx, ct in enumerate(pending_cts):
        num = normalize_number(ct.phone_number)
        gw = gw_list[idx % gw_count]
        assignments[gw.id].append(num)
    return assignments

# ---------------------------------------------------------------------
# MAIN TASK
# ---------------------------------------------------------------------
@celery.task(bind=True, base=ContextTask, max_retries=None)
def process_messages(self, message_id: int):
    # Acquire lock to prevent duplicates
    acquired, lock, token = acquire_lock(message_id)
    if not acquired:
        current_app.logger.info(f"[Task] Message {message_id} is already being processed by another worker.")
        return {"status": "skipped", "reason": "locked"}

    try:
        msg = Message.query.get(message_id)
        if not msg:
            current_app.logger.warning(f"[Task] Message {message_id} not found.")
            return {"status": "error", "reason": "message_not_found"}

        pending_cts = ContactTransact.query.filter(
            ContactTransact.message_id == message_id,
            ContactTransact.status.in_(["pending", "retrying"])
        ).all()

        if not pending_cts:
            msg.status = "completed"
            db.session.commit()
            current_app.logger.info(f"[Task] No pending contacts for Message {message_id}.")
            return {"status": "ok", "processed": 0}

        # Load active gateways
        gateways = {g.id: g for g in Gateway.query.filter_by(active=True).order_by(Gateway.id).all()}
        if not gateways:
            msg.status = "failed"
            db.session.commit()
            current_app.logger.error("[Task] No active gateways available.")
            return {"status": "error", "reason": "no_active_gateways"}

        ct_by_number = {normalize_number(ct.phone_number): ct for ct in pending_cts}

        # Assign gateways for first-time sends
        first_send_cts = [ct for ct in pending_cts if not ct.gateway]
        if first_send_cts:
            assignments = assign_gateways_round_robin(first_send_cts, list(gateways.values()))
            for gw_id, numbers in assignments.items():
                gw_obj = gateways.get(gw_id)
                for num in numbers:
                    ct = ct_by_number.get(num)
                    if ct:
                        ct.gateway = gw_obj.name
                        db.session.add(ct)
            db.session.commit()
            current_app.logger.info(f"[Task] Assigned {len(first_send_cts)} contacts to gateways.")

        # Pricing calculation
        units_per_message = (len(msg.message) + 159) // 160
        price_row = SMSPricing.query.filter_by(sms_type="local").first()
        price_per_unit = float(price_row.price_per_sms) if price_row else 0.0

        total_processed = 0
        pending_for_balance = False
        overall_statuses = []

        # Group contacts by gateway
        gw_to_cts = {}
        for ct in pending_cts:
            if ct.status in ("sent", "delivered"):
                continue
            if ct.retry_count and ct.retry_count >= MAX_RETRIES and ct.status == "retrying":
                ct.status = "failed"
                ct.error_message = "Max retries reached"
                ct.updated_at = datetime.now(timezone.utc)
                db.session.add(ct)
                overall_statuses.append(ct.status)
                continue
            gw_to_cts.setdefault(ct.gateway, []).append(ct)

        # Process each gateway batch
        for gw_name, cts in gw_to_cts.items():
            gw = next((g for g in gateways.values() if g.name == gw_name), None)
            if not gw:
                for ct in cts:
                    ct.status = "failed"
                    ct.error_message = "Gateway unavailable"
                    if not getattr(ct, "gateway_charged", False):
                        ct.refund()
                    ct.updated_at = datetime.now(timezone.utc)
                    db.session.add(ct)
                db.session.commit()
                continue

            batch_limit = {"termii": 1000, "africastalking": 100}.get(gw.name.lower(), 100)
            all_numbers = [normalize_number(ct.phone_number) for ct in cts]

            for batch in chunk_list(all_numbers, batch_limit):
                required_cost = price_per_unit * units_per_message * len(batch)

                # Gateway balance check
                try:
                    balance = get_gateway_balance(gw)
                except Exception as e:
                    current_app.logger.warning(f"[Task] Balance check failed for {gw.name}: {e}")
                    balance = 0

                if balance < MIN_BALANCE or balance < required_cost:
                    pending_for_balance = True
                    for number in batch:
                        ct = ct_by_number.get(number)
                        if ct:
                            ct.status = "pending"
                            ct.error_message = f"Low gateway balance (need {required_cost:.2f}, have {balance:.2f})"
                            ct.updated_at = datetime.now(timezone.utc)
                            db.session.add(ct)
                            overall_statuses.append(ct.status)
                    db.session.commit()
                    continue

                # Send batch
                try:
                    response = send_sms_via_gateway(batch, msg.message, gw)
                    results = response.get("results", [])
                except Exception as e:
                    retries = getattr(self.request, "retries", 0)
                    delay = min(60 * (2 ** retries), BACKOFF_LIMIT)
                    current_app.logger.warning(f"[Task] {gw.name} send failed, retrying in {delay}s: {e}")
                    raise self.retry(countdown=delay, exc=None)

                res_map = {normalize_number(r["number"]): r for r in results} if results else {}

                sent_count = 0
                failed_count = 0

                for number in batch:
                    ct = ct_by_number.get(number)
                    if not ct:
                        continue
                    r = res_map.get(number)

                    if not r:
                        # Retry logic
                        if (ct.retry_count or 0) < MAX_RETRIES:
                            ct.status = "retrying"
                            ct.retry_count = (ct.retry_count or 0) + 1
                        else:
                            ct.status = "failed"
                            if not getattr(ct, "gateway_charged", False):
                                ct.refund()
                        ct.error_message = "No response from gateway"
                        failed_count += 1
                    else:
                        status = (r.get("status") or "").lower()
                        if status in ("sent", "success", "queued", "ok"):
                            ct.status = "sent"
                            ct.response_id = r.get("message_id")
                            ct.raw_status = r.get("raw_status")
                            ct.retry_count = 0
                            ct.gateway_charged = True
                            ct.error_message = None
                            total_processed += 1
                            sent_count += 1
                        else:
                            error_text = r.get("error") or r.get("raw_status") or "gateway_error"
                            transient = "timeout" in error_text.lower() or "gateway" in error_text.lower()
                            if transient and (ct.retry_count or 0) < MAX_RETRIES:
                                ct.status = "retrying"
                                ct.retry_count = (ct.retry_count or 0) + 1
                            else:
                                ct.status = "failed"
                                if not getattr(ct, "gateway_charged", False):
                                    ct.refund()
                            ct.error_message = error_text
                            failed_count += 1

                    ct.updated_at = datetime.now(timezone.utc)
                    db.session.add(ct)
                    overall_statuses.append(ct.status)

                db.session.commit()
                current_app.logger.info(
                    f"[Task] Gateway {gw.name} batch processed: {sent_count} sent, {failed_count} failed"
                )

        # Update message status
        if all(s == "sent" for s in overall_statuses):
            msg.status = "completed"
        elif any(s == "sent" for s in overall_statuses):
            msg.status = "partial"
        else:
            msg.status = "pending"

        msg.updated_at = datetime.now(timezone.utc)
        db.session.add(msg)
        db.session.commit()

        # Schedule retry if needed
        retries = getattr(self.request, "retries", 0)
        delay = min(60 * (2 ** retries), BACKOFF_LIMIT)

        if any(ct.status == "retrying" for ct in pending_cts) or pending_for_balance:
            current_app.logger.info(f"[Task] Retrying in {delay}s for message {message_id}")
            raise self.retry(countdown=delay, exc=None)

        current_app.logger.info(f"[Task] Message {message_id} completed with status {msg.status}")
        return {
            "status": "ok",
            "message_id": message_id,
            "processed": total_processed,
            "campaign_status": msg.status
        }

    except self.MaxRetriesExceededError:
        current_app.logger.error(f"[Task] Max retries exceeded for Message {message_id}")
        msg = Message.query.get(message_id)
        if msg:
            msg.status = "failed"
            db.session.commit()

    except Exception as exc:
        retries = getattr(self.request, "retries", 0)
        delay = min(60 * (2 ** retries), BACKOFF_LIMIT)
        current_app.logger.error(f"[Task] Unexpected error for Message {message_id}: {exc}", exc_info=True)
        raise self.retry(countdown=delay, exc=exc)

    finally:
        # Release Redis lock safely
        if 'lock' in locals() and lock.locked():
            lock.release(token=token)
