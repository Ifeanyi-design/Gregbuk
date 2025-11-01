from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from db import Message, ContactTransact, Contact, ContactGroup, Wallet, SMSPricing, db
from sqlalchemy import func
from datetime import datetime, timezone


bp = Blueprint("main", __name__)

# Utility: calculate SMS units
def sms_units(message: str) -> int:
    return (len(message) + 159) // 160  # 160 chars per unit

def normalize_number(number: str) -> str:
    """Normalize phone number to international format used by gateways."""
    if not number:
        return number
    n = number.strip()
    if n.startswith("0"):
        return "234" + n[1:]
    if n.startswith("+"):
        return n[1:]
    return n

@bp.route("/select-sms-type")
@login_required
def select_sms_type():
    return render_template("select_sms_type.html", bulkk_sms=True)


@bp.route("/send_bulk_sms_manual")
@login_required
def send_bulk_sms_manually():
    return render_template("send_bulk_sms_phone.html", bulkk_sms=True)


# Send SMS from raw list of numbers
@bp.route("/send_bulk_sms", methods=["POST"])
@login_required
def send_bulk_sms():
    data = request.get_json()
    message_text = data.get("message")
    contacts = data.get("contacts")  # list of phone numbers
    campaign_name = data.get("campaign_name")

    if not message_text or not contacts:
        return jsonify({"status": "error", "message": "Missing message or contacts"}), 400

    if isinstance(contacts, str):
        contacts = [contacts]

    # Normalize numbers and filter invalid
    valid_contacts = []
    for phone in contacts:
        try:
            normalized = normalize_number(phone)
            valid_contacts.append(normalized)
        except Exception:
            continue

    queued = len(valid_contacts)
    failed = len(contacts) - queued

    if not valid_contacts:
        return jsonify({"status": "error", "message": "No valid phone numbers provided"}), 400

    # Calculate units and cost
    units_per_message = sms_units(message_text)
    price_per_unit = SMSPricing.query.filter_by(sms_type="local").first()
    if not price_per_unit:
        return jsonify({"status": "error", "message": "Pricing not configured"}), 500

    total_cost = len(valid_contacts) * units_per_message * price_per_unit.price_per_sms

    # Check wallet balance
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet or wallet.balance < total_cost:
        return jsonify({
            "status": "error",
            "message": f"Insufficient balance. Required: {total_cost}, Available: {wallet.balance if wallet else 0}"
        }), 400

    # Deduct balance
    wallet.balance -= total_cost
    db.session.add(wallet)

    # Create campaign
    campaign = Message(
        user_id=current_user.id,
        name=campaign_name if campaign_name else "Bulk Campaign",
        message=message_text,
        units=units_per_message,
        cost=total_cost,
        status="pending"
    )
    db.session.add(campaign)
    db.session.commit()

    # Create ContactTransact records
    transacts = [
        ContactTransact(
            message_id=campaign.id,
            user_id=current_user.id,
            phone_number=phone,
            status="pending",
            retry_count=0,
            contact_id=0  # raw numbers, no linked contact
        )
        for phone in valid_contacts
    ]
    db.session.bulk_save_objects(transacts)
    db.session.commit()

    # Trigger Celery task
    from tasks import process_messages
    process_messages.delay(campaign.id)

    return jsonify({
        "status": "success",
        "message": f"Bulk SMS queued. Charged {total_cost} units.",
        "queued": queued,
        "failed": failed
    })



# Send SMS to a group
@bp.route("/send_bulk_sms_group", methods=["POST"])
@login_required
def send_bulk_sms_group():
    data = request.get_json()
    group_id = data.get("group_id")
    message_text = data.get("message")
    campaign_name = data.get("campaign_name")

    if not group_id or not message_text:
        return jsonify({"status": "error", "message": "Group or message missing"}), 400

    # Fetch contacts in the group
    contacts = Contact.query.filter_by(user_id=current_user.id, group_id=group_id).all()
    if not contacts:
        return jsonify({"status": "error", "message": "No contacts in this group"}), 400

    # Map normalized phone -> contact id for quick lookup
    phone_to_contact_id = {normalize_number(c.phone): c.id for c in contacts}

    valid_contacts = list(phone_to_contact_id.keys())
    queued = len(valid_contacts)
    failed = len(contacts) - queued

    if not valid_contacts:
        return jsonify({"status": "error", "message": "No valid phone numbers in this group"}), 400

    # Calculate units and cost
    units_per_message = sms_units(message_text)
    price_per_unit = SMSPricing.query.filter_by(sms_type="local").first()
    if not price_per_unit:
        return jsonify({"status": "error", "message": "Pricing not configured"}), 500

    total_cost = len(valid_contacts) * units_per_message * price_per_unit.price_per_sms

    # Check wallet balance
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet or wallet.balance < total_cost:
        return jsonify({
            "status": "error",
            "message": f"Insufficient balance. Required: {total_cost}, Available: {wallet.balance if wallet else 0}"
        }), 400

    # Deduct balance
    wallet.balance -= total_cost
    db.session.add(wallet)

    # Create campaign
    campaign = Message(
        user_id=current_user.id,
        name=campaign_name if campaign_name else f"Group-{group_id}",
        message=message_text,
        units=units_per_message,
        cost=total_cost,
        status="pending"
    )
    db.session.add(campaign)
    db.session.commit()

    # Create ContactTransact records
    transacts = [
        ContactTransact(
            message_id=campaign.id,
            user_id=current_user.id,
            phone_number=phone,
            status="pending",
            retry_count=0,
            contact_id=phone_to_contact_id.get(phone)
        )
        for phone in valid_contacts
    ]
    db.session.bulk_save_objects(transacts)
    db.session.commit()

    # Trigger Celery task
    from tasks import process_messages
    process_messages.delay(campaign.id)

    return jsonify({
        "status": "success",
        "message": f"Bulk SMS queued. Charged {total_cost} units.",
        "queued": queued,
        "failed": failed
    })



# Phonebook UI
@bp.route("/send_sms_phonebook")
@login_required
def send_sms_phonebook():
    groups = ContactGroup.query.filter_by(user_id=current_user.id).all()
    return render_template("send_sms_phonebook.html", groups=groups, bulkk_sms=True)


# --- DLR webhooks ---
@bp.route("/webhook/termii", methods=["POST"])
def dlr_termii():
    data = request.get_json(force=True, silent=True) or {}
    message_id = data.get("message_id") or (data.get("data") and data["data"].get("message_id"))
    status = (data.get("status") or (data.get("data") and data["data"].get("status")) or "").lower()
    to = data.get("to") or (data.get("data") and data["data"].get("to"))

    if not message_id and not to:
        return jsonify({"status": "ignored"}), 400

    ct = None
    if message_id:
        ct = ContactTransact.query.filter_by(response_id=message_id).first()
    if not ct and to:
        ct = ContactTransact.query.filter_by(phone_number=normalize_number(to)).order_by(ContactTransact.sent_at.desc()).first()

    if ct:
        if "deliver" in status:
            ct.status = "delivered"
        elif "fail" in status:
            ct.status = "failed"
        ct.sent_at = datetime.now(timezone.utc)
        db.session.add(ct)
        db.session.commit()

    return jsonify({"status": "ok"})


@bp.route("/webhook/africastalking", methods=["POST"])
def dlr_africastalking():
    data = request.form.to_dict() or request.get_json(silent=True) or {}
    message_id = data.get("id") or data.get("messageId")
    status = (data.get("status") or "").lower()
    to = data.get("number") or data.get("to")

    ct = None
    if message_id:
        ct = ContactTransact.query.filter_by(response_id=message_id).first()
    if not ct and to:
        ct = ContactTransact.query.filter_by(phone_number=normalize_number(to)).order_by(ContactTransact.sent_at.desc()).first()

    if ct:
        if "success" in status or "delivered" in status:
            ct.status = "delivered"
        elif "fail" in status or "reject" in status:
            ct.status = "failed"
        ct.sent_at = datetime.now(timezone.utc)
        db.session.add(ct)
        db.session.commit()

    return jsonify({"status": "ok"})


# Delivery report data API
@bp.route("/api/delivery_report_data")
@login_required
def delivery_report_data():
    user_id = current_user.id
    total_sent = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id).scalar() or 0
    delivered = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id, status="delivered").scalar() or 0
    failed = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id, status="failed").scalar() or 0
    pending = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id, status="pending").scalar() or 0

    weekly = (
        db.session.query(func.date(ContactTransact.updated_at), func.count(ContactTransact.id))
        .filter(ContactTransact.user_id == user_id, ContactTransact.updated_at != None)
        .group_by(func.date(ContactTransact.updated_at))
        .order_by(func.date(ContactTransact.updated_at).asc())
        .all()
    )
    weekly_data = [count for _, count in weekly]

    return jsonify({
        "messages_sent": total_sent,
        "delivered": delivered,
        "failed": failed,
        "pending": pending,
        "messages_chart_data": weekly_data,
        "delivery_status_data": [delivered, pending, failed]
    })


@bp.route("/delivery_report")
@login_required
def delivery_report():
    return render_template("delivery_report.html", bulkk_sms=True)