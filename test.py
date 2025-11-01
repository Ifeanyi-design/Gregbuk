# test_full_bulk_sms_multi_gateway_mock.py
from main import create_app, db
from db import Wallet, Gateway, Message, ContactTransact, SMSPricing
from tasks import send_bulk_sms_task
from datetime import datetime, timezone
import time
import random

app = create_app()
TEST_USER_ID = 999  # arbitrary test user id

# --- Mock the gateway sending function ---
from gateway import send_sms_via_gateway as real_send_sms


def mock_send_sms_via_gateway(phone_number, message, gateway):
    """Simulate sending SMS without actually calling API"""
    # Randomly simulate success or failure
    status = random.choice(["sent", "failed"])
    message_id = f"mock-{random.randint(1000, 9999)}"
    error = None if status == "sent" else "Simulated failure"
    return {"status": status, "message_id": message_id, "error": error}


# Patch the gateway function
import gateway

gateway.send_sms_via_gateway = mock_send_sms_via_gateway

with app.app_context():
    # --- 1. Create a test wallet ---
    wallet = Wallet.query.filter_by(user_id=TEST_USER_ID).first()
    if not wallet:
        wallet = Wallet(user_id=TEST_USER_ID, balance=1000.00)
        db.session.add(wallet)
    else:
        wallet.balance = 1000.00
    db.session.commit()

    # --- 2. Add multiple test gateways ---
    gateways = [
        {"name": "Termii", "api_key": "TEST_TERMI", "sender_id": "TERMI1"},
        {"name": "AfricaSTalking", "api_key": "TEST_AT", "sender_id": "AT1"}
    ]



    # if not SMSPricing.query.filter_by(sms_type="local"):
    #     new = SMSPricing(
    #         sms_type="local",
    #         price_per_sms=7
    #     )
    #     db.session.add(new)

    for g in gateways:
        gw = Gateway.query.filter_by(name=g["name"], sender_id=g["sender_id"]).first()
        if not gw:
            gw = Gateway(
                name=g["name"],
                api_key=g["api_key"],
                sender_id=g["sender_id"],
                active=True
            )
            db.session.add(gw)

    db.session.commit()

    # --- 3. Insert test contacts ---
    test_numbers = ["+2348012345678", "+2348098765432", "+2348023456789", "+2348056789012"]

    # --- 4. Create a test campaign ---
    campaign = Message(
        user_id=TEST_USER_ID,
        name="Mock Multi-Gateway Test",
        message="Hello! This is a mock test SMS.",
        status="pending",
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(campaign)
    db.session.commit()

    # --- 5. Add transactions ---
    for num in test_numbers:
        db.session.add(ContactTransact(
            message_id=campaign.id,
            contact_id=779,
            user_id=TEST_USER_ID,
            phone_number=num,
            status="pending"
        ))
    db.session.commit()

    # --- 6. Trigger Celery bulk SMS task ---
    print("Triggering bulk SMS task with mocked sending...")
    result = send_bulk_sms_task.apply(args=(campaign.id,), kwargs={"wait_for_completion": True})

    # Wait for task to finish
    while not result.ready():
        print("Waiting for Celery task to complete...")
        time.sleep(2)

    print("Task result:", result.result)

    # --- 7. Print transaction statuses ---
    transactions = ContactTransact.query.filter_by(message_id=campaign.id).all()
    for t in transactions:
        print(f"{t.phone_number} -> {t.status}, Gateway: {t.gateway}, Error: {t.error_message}")

    print("Mock multi-gateway test completed.")