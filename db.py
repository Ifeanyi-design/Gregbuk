from flask_sqlalchemy import SQLAlchemy

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
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=True)
    sub_service_id = db.Column(db.Integer, db.ForeignKey("subservices.id"), nullable=True)

class Header(db.Model):
    __tablename__ = "head"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    end_url = db.Column(db.String(255), nullable=False)
