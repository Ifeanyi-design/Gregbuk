# routes.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from main import db
from db import Message, ContactTransact, Contact, ContactGroup
from tasks import send_bulk_sms_task
from sqlalchemy import func
from datetime import datetime, timezone

bp = Blueprint("main", __name__)

# Send from raw list (existing behavior)
@bp.route("/send_bulk_sms", methods=["POST"])
@login_required
def send_bulk_sms():
    data = request.get_json()
    message_text = data.get("message")
    contacts = data.get("contacts")  # list of phone numbers
    campaign_name = data.get("campaign_name")

    if not message_text or not contacts:
        return jsonify({"status":"error","message":"Missing message or contacts"}), 400

    campaign = Message(user_id=current_user.id, name=campaign_name if campaign_name else "Bulk Campaign", message=message_text)
    db.session.add(campaign)
    db.session.commit()

    # Add ContactTransact rows
    for phone in contacts:
        db.session.add(ContactTransact(message_id=campaign.id, user_id=current_user.id, phone_number=phone, status="pending"))
    db.session.commit()

    # Start Celery task
    send_bulk_sms_task.delay(campaign.id)

    return jsonify({"status":"success","message":"Bulk SMS is being sent."})

# Phonebook UI
@bp.route("/send_sms_phonebook")
@login_required
def send_sms_phonebook():
    groups = ContactGroup.query.filter_by(user_id=current_user.id).all()
    return render_template("send_sms_phonebook.html", groups=groups)

# Send for a group
@bp.route("/send_bulk_sms_group", methods=["POST"])
@login_required
def send_bulk_sms_group():
    data = request.get_json()
    group_id = data.get("group_id")
    message_text = data.get("message")
    campaign_name = data.get("campaign_name")
    if not group_id or not message_text:
        return jsonify({"status":"error","message":"Group or message missing"}), 400

    contacts = Contact.query.filter_by(user_id=current_user.id, group_id=group_id).all()
    if not contacts:
        return jsonify({"status":"error","message":"No contacts in this group"}, 400)

    phone_list = [c.phone for c in contacts]

    campaign = Message(user_id=current_user.id, name=campaign_name if campaign_name else f"Bulk-{group_id}", message=message_text)
    db.session.add(campaign)
    db.session.commit()

    for phone in phone_list:
        db.session.add(ContactTransact(message_id=campaign.id, user_id=current_user.id, phone_number=phone, status="pending"))
    db.session.commit()

    send_bulk_sms_task.delay(campaign.id)
    return jsonify({"status":"success","message":"Bulk SMS is being sent in the background."})

# DLR webhook for Termii
# Set this URL in Termii's dashboard as your delivery callback URL
@bp.route("/webhook/termii", methods=["POST"])
def dlr_termii():
    data = request.get_json(force=True, silent=True) or {}
    # Termii payload structure may vary — adapt as per their docs
    # Example: { "message_id": "xxx", "status": "delivered", "to": "2348..." }
    message_id = data.get("message_id") or (data.get("data") and data["data"].get("message_id"))
    status = (data.get("status") or (data.get("data") and data["data"].get("status")) or "").lower()
    to = data.get("to") or (data.get("data") and data["data"].get("to"))

    if not message_id and not to:
        return jsonify({"status":"ignored"}), 400

    # Try find by response_id first, else by phone number + recent sent
    ct = None
    if message_id:
        ct = ContactTransact.query.filter_by(response_id=message_id).first()
    if not ct and to:
        ct = ContactTransact.query.filter_by(phone_number=to).order_by(ContactTransact.sent_at.desc()).first()

    if ct:
        if "deliver" in status or "delivered" in status:
            ct.status = "delivered"
        elif "failed" in status or "undeliverable" in status:
            ct.status = "failed"
        else:
            ct.status = ct.status  # leave as-is if unknown
        ct.sent_at = datetime.now(timezone.utc)
        db.session.add(ct)
        db.session.commit()

    return jsonify({"status":"ok"})

# DLR webhook for Africa's Talking
# AT sends POST form-data to your callback URL; adapt parsing if they send JSON
@bp.route("/webhook/africastalking", methods=["POST"])
def dlr_africastalking():
    # Africa's Talking may POST form fields like: id, status, number ...
    data = request.form.to_dict() or request.get_json(silent=True) or {}
    message_id = data.get("id") or data.get("messageId")
    status = (data.get("status") or "").lower()
    to = data.get("number") or data.get("to")

    ct = None
    if message_id:
        ct = ContactTransact.query.filter_by(response_id=message_id).first()
    if not ct and to:
        ct = ContactTransact.query.filter_by(phone_number=to).order_by(ContactTransact.sent_at.desc()).first()

    if ct:
        if "success" in status or "delivered" in status:
            ct.status = "delivered"
        elif "failed" in status or "rejected" in status:
            ct.status = "failed"
        ct.sent_at = datetime.now(timezone.utc)
        db.session.add(ct)
        db.session.commit()

    return jsonify({"status":"ok"})

# Delivery report endpoints (uses ContactTransact)
@bp.route("/api/delivery_report_data")
@login_required
def delivery_report_data():
    user_id = current_user.id
    total_sent = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id).scalar() or 0
    delivered = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id, status="delivered").scalar() or 0
    failed = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id, status="failed").scalar() or 0
    pending = db.session.query(func.count(ContactTransact.id)).filter_by(user_id=user_id, status="pending").scalar() or 0

    weekly = (
        db.session.query(func.date(ContactTransact.sent_at), func.count(ContactTransact.id))
        .filter(ContactTransact.user_id == user_id, ContactTransact.sent_at != None)
        .group_by(func.date(ContactTransact.sent_at))
        .order_by(func.date(ContactTransact.sent_at).asc())
        .all()
    )
    # produce 7-value array Mon..Sun; we keep it simple and return available data
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
    return render_template("delivery_report.html")
