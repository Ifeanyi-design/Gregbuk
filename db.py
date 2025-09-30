from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Enum, Numeric, event
from decimal import Decimal

db = SQLAlchemy()

services = [
    {
        "name": "Marketing Materials",
        "category": "marketing-materials"
    },
{
        "name": "Business Cards",
        "category": "business-cards"
    },
{
        "name": "Stickers & Labels",
        "category": "stickers-labels"
    },
{
        "name": "Signs & Banners",
        "category": "banners"
    },
{
        "name": "Bulk Sms",
        "category": "bulk-sms"
    }
]

class Services(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image_url = db.Column(db.String(255))
    icon_name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    content = db.Column(db.Text)
    category_name = db.Column(db.String(255), nullable=False)
    alt_texts = db.Column(db.String(255))
    products = db.relationship("Products", backref="services", lazy=True, cascade="all, delete")
    sub_service = db.relationship("SubService", backref="services", lazy=True, cascade="all, delete")

class SubService(db.Model):
    __tablename__ = "subservices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image_url = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    content = db.Column(db.Text)
    category_name = db.Column(db.String(255), nullable=False)
    alt_texts = db.Column(db.String(255))
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    products = db.relationship("Products", backref="subservice", lazy=True, cascade="all, delete")

class Products(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image_url = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    content = db.Column(db.Text)
    category_name = db.Column(db.String(255), nullable=False)
    alt_texts = db.Column(db.String(255))
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=True)
    sub_service_id = db.Column(db.Integer, db.ForeignKey("subservices.id"), nullable=True)
    image_collections = db.relationship("ProductCollection", backref="product", lazy=True, cascade="all, delete")

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    new = db.Column(db.Boolean, default=True, nullable=False)
    messages = db.relationship("Message", backref="user", cascade="all, delete-orphan", lazy=True)
    contacts = db.relationship("Contact", backref="user", cascade="all, delete-orphan", lazy=True)
    groups = db.relationship("ContactGroup", backref="user", cascade="all, delete-orphan", lazy=True)
    message_transactions = db.relationship("ContactTransact", backref="user", cascade="all, delete-orphan", lazy=True)
    wallet = db.relationship("Wallet", backref="user", uselist=False, cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", backref="user", lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=True)  # for scheduling
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship
    transactions = db.relationship("ContactTransact", backref="message", cascade="all, delete-orphan", lazy=True)
    status = db.Column(db.String(20), default="pending")  # pending, delivered, failed

class ContactGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Relationship
    contacts = db.relationship("Contact", backref="group", cascade="all, delete-orphan", lazy=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('contact_group.id', ondelete="SET NULL"), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship to variables
    variables = db.relationship("Variable", backref="contact", cascade="all, delete-orphan", lazy=True)
    transactions = db.relationship("ContactTransact", backref="contact", lazy=True)

class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(50), nullable=False)  # e.g., "first_name"
    content = db.Column(db.String(255), nullable=False)  # e.g., "John"

class SMSPricing(db.Model):
    _tablename_ = "sms_pricing"
    id = db.Column(db.Integer, primary_key=True)
    sms_type = db.Column(db.String(50), unique=True, nullable=False)  # 'local' or 'international'
    price_per_sms = db.Column(db.Numeric(10, 2), nullable=False)      # Cost per SMS in ₦
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(Numeric(precision=12, scale=2), default=0.0)
    currency = db.Column(db.String(10), default="NGN")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    transactions = db.relationship("Transaction", backref="wallet", lazy=True, cascade="all, delete-orphan")

class Gateway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    max_per_sec = db.Column(db.Integer, default=1)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"), nullable=False)
    amount = db.Column(Numeric(precision=12, scale=2), nullable=False)
    currency = db.Column(db.String(10), default="NGN")
    type = db.Column(Enum("credit", "debit", name="transaction_type"), nullable=False)  # "credit" or "debit"
    reference = db.Column(db.String(100), unique=True, nullable=True, index=True)  # from Paystack/Flutterwave
    status = db.Column(Enum("pending", "success", "failed", name="transaction_status"), default="pending", index=True)  # "pending", "success", "failed"
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc), index=True)

class ContactTransact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id', ondelete="CASCADE"), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)  # optional, redundant but can be convenient
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), default="pending")  # e.g., pending, delivered, failed
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    error_message = db.Column(db.Text, nullable=True)  # store failure reason if any
    variables_applied = db.Column(db.JSON, nullable=True)  # optional: store personalized values used
    gateway = db.Column(db.String(50), nullable=True)


class ProductCollection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    image_collections = db.Column(db.String(255))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)

class Header(db.Model):
    __tablename__ = "head"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    end_url = db.Column(db.String(255), nullable=False)


@event.listens_for(User, "after_insert")
def create_user_wallet(mapper, connection, target):
    new_wallet = Wallet(
        user_id=target.id,
        balance=Decimal("0.00"), currency="NGN"
    )
    connection.execute(Wallet.__table__.insert().values(
        user_id=new_wallet.user_id,
        balance=new_wallet.balance,
        currency=new_wallet.currency
    ))