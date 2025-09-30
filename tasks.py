# tasks.py
from celery import Celery
from main import create_app, db
from db import Message, ContactTransact, Wallet, SMSPricing
from gateway import send_bulk_simultaneously
from datetime import datetime, timezone
from decimal import Decimal

app = create_app()
celery = Celery(app.name, broker="redis://localhost:6379/0")


@celery.task
def send_bulk_sms_task(message_id):
    with app.app_context():
        campaign = Message.query.get(message_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found."}

        # fetch wallet
        wallet = Wallet.query.filter_by(user_id=campaign.user_id).first()
        if not wallet:
            campaign.status = "failed"
            db.session.commit()
            return {"status": "error", "message": "Wallet not found."}

        # fetch pricing (assuming one row for local SMS)
        pricing = SMSPricing.query.filter_by(sms_type="local").first()
        if not pricing:
            campaign.status = "failed"
            db.session.commit()
            return {"status": "error", "message": "SMS pricing not set."}

        # Build phone list
        rows = ContactTransact.query.filter_by(message_id=message_id).all()
        phone_list = [r.phone_number for r in rows]
        total_cost = Decimal(len(phone_list)) * pricing.price_per_sms

        # check balance
        if wallet.balance < total_cost:
            campaign.status = "failed"
            db.session.commit()
            return {"status": "error", "message": "Insufficient balance."}

        # mark as sending
        campaign.status = "sending"
        db.session.commit()

        # Send simultaneously via Termii + AT
        results = send_bulk_simultaneously(phone_list, campaign.message)

        # Split set to know which gateway handled which numbers
        mid = len(phone_list) // 2
        termii_set = set(phone_list[:mid])

        for res in results:
            phone = res["phone"]
            resp = res.get("response") or {}
            row = ContactTransact.query.filter_by(message_id=message_id, phone_number=phone).first()
            if not row:
                continue

            # Gateway
            row.gateway = "termii" if phone in termii_set else "africastalking"

            # Status detection
            api_status = None
            if isinstance(resp, dict):
                api_status = resp.get("status") or resp.get("data", {}).get("status")
            if api_status and str(api_status).lower() in ("success", "sent", "queued", "ok"):
                row.status = "sent"
                row.sent_at = datetime.now(timezone.utc)
            else:
                if "error" in str(resp).lower() or "failed" in str(resp).lower():
                    row.status = "failed"
                    row.error_message = str(resp)
                else:
                    row.status = "sent"
                    row.sent_at = datetime.now(timezone.utc)

            # capture message_id if any
            if isinstance(resp, dict):
                row.response_id = (
                    resp.get("message_id")
                    or (resp.get("data") and resp["data"].get("message_id"))
                    or row.response_id
                )

            db.session.add(row)

        # Deduct wallet *after sending*
        wallet.balance -= total_cost
        db.session.add(wallet)

        # Finish campaign
        campaign.status = "completed"
        db.session.commit()

        return {"status": "success", "sent": len(results), "deducted": str(total_cost)}