from flask import Flask, render_template, send_from_directory, Blueprint, request,url_for, jsonify, redirect, flash, session, abort
from config import Config
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, func, inspect
from db import db, Services, Products, Variable, SubService, Transaction, Wallet, Header, User, Message, Contact, ContactGroup, ContactTransact, ProductCollection
from random import randint, choice
from form import ContactForm
import os, traceback, logging
import click
from functools import wraps
from datetime import datetime, timedelta, timezone
import smtplib
from email.message import EmailMessage
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
import csv, io
from decimal import Decimal
try:
    import requests
except ModuleNotFoundError:
    requests = None
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import re
try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None
from routes import bp
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "hellodear"
    db.init_app(app)
    Migrate(app, db)
    with app.app_context():
        db.create_all()  # creates tables

    return app

app = create_app()


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
logger = logging.getLogger(__name__)

PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
UPLOAD_FOLDER = "uploads"
ALLOWED = {"csv", "xlsx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # ensure folder exists

app.register_blueprint(bp)


@app.cli.command("seed-targeted-services")
def seed_targeted_services_command():
    """Seed or refresh the newer corporate service branches."""
    from seed_targeted_services import seed_targeted_services

    results = seed_targeted_services()
    click.echo(
        "Targeted service seed complete -> "
        f"services created: {results['services_created']}, "
        f"services refreshed: {results['services_updated']}, "
        f"subservices created: {results['subservices_created']}, "
        f"subservices refreshed: {results['subservices_updated']}, "
        f"products created: {results['products_created']}, "
        f"products refreshed: {results['products_updated']}, "
        f"gallery images added: {results['gallery_images_added']}"
    )


def admin_access_allowed(user):
    if not getattr(user, "is_authenticated", False):
        return False
    allowed_emails = {
        email.strip().lower()
        for email in os.getenv("ADMIN_EMAILS", "").split(",")
        if email.strip()
    }
    if allowed_emails:
        return (user.email or "").lower() in allowed_emails
    return True


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not admin_access_allowed(current_user):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


def admin_layout_context(page_key="admin-dashboard", **extra):
    context = {
        "bulkk_sms": True,
        "the_name": page_key,
        "change": False,
        "admin_enabled": True,
    }
    context.update(extra)
    return context


def summarize_text(value, limit=120):
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", str(value))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit - 3].rstrip() + "..."

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

old_select=[]
@app.template_global()
def choose_from_list(list):
    global old_select
    count = 0
    products = choice(list)
    while True:
        new_choice = choice(products.products)

        if new_choice not in old_select:
            old_select.append(new_choice)
            return new_choice
        # elif count == 10:
        #     return new_choice
        # count+=1
@app.context_processor
def inject_template_globals():
    # Single source for current year across templates.
    leadership_team = [
        {"name": "Engr. Agada Sunday G.", "role": "MD/CEO"},
        {"name": "Mrs Bukola Agada", "role": "GM"},
        {"name": "Mrs Callista Agada", "role": "Business Development Manager / Secretary"},
        {"name": "Oluwatobi V. Onyedika Agada", "role": "Manager & Board Member"},
        {"name": "Ifeanyi Agada", "role": "IT Consultant / Board Member"},
    ]
    return {
        "current_year": datetime.now().year,
        "company_name": os.getenv("COMPANY_NAME", "Gregbuk Intl Company Ltd"),
        "company_email": os.getenv("COMPANY_EMAIL", "[TODO:COMPANY_EMAIL_HERE]"),
        "company_phone_primary": os.getenv("COMPANY_PHONE_PRIMARY", "[TODO:COMPANY_PHONE_PRIMARY]"),
        "company_phone_secondary": os.getenv("COMPANY_PHONE_SECONDARY", "[TODO:COMPANY_PHONE_SECONDARY]"),
        "company_address": os.getenv("COMPANY_ADDRESS", "[TODO:COMPANY_ADDRESS_HERE]"),
        "company_whatsapp": os.getenv("COMPANY_WHATSAPP", "[TODO:COMPANY_WHATSAPP_HERE]"),
        "company_city": os.getenv("COMPANY_CITY", "Lagos"),
        "company_country": os.getenv("COMPANY_COUNTRY", "Nigeria"),
        "company_established_year": 2004,
        "company_registration_number": "1057410",
        "company_registered_on": "10 Aug 2012",
        "company_status": "Active",
        "leadership_team": leadership_team,
        "ga4_measurement_id": os.getenv("GA4_MEASUREMENT_ID", ""),
        "service_mode": "catalog",
        "cta_copy": dynamic_cta_copy("catalog")
    }

# --- Helpers ---
PHONE_RE = re.compile(r"^\+?\d[\d\-\s()]{5,}$")  # simple permissive pattern

def normalize_var_name(name):
    """Convert column names like 'First Name' or 'Phone_Number' to 'first_name'"""
    name = str(name).strip().lower()
    name = re.sub(r"\s+", "_", name)        # spaces → underscores
    name = re.sub(r"[^\w_]", "", name)      # remove any non-word characters except underscore
    return name

def normalize_phone(raw):
    """Return digits-only phone (keeps leading + if present)."""
    if raw is None:
        return None
    raw = str(raw).strip()
    if raw.startswith("+"):
        cleaned = "+" + re.sub(r"[^\d]", "", raw)
    else:
        cleaned = re.sub(r"[^\d]", "", raw)
    return cleaned

def valid_phone(phone):
    """Basic validation: ensure digits length >= 7 and matches pattern."""
    if not phone:
        return False
    # allow + and digits
    cleaned = phone if phone.startswith("+") else phone
    return bool(PHONE_RE.match(cleaned)) and len(re.sub(r"[^\d]", "", cleaned)) >= 7


INQUIRY_SERVICE_KEYWORDS = (
    "contract",
    "pharma",
    "pharmaceutical",
    "engineering",
    "consult",
    "travel",
    "cac",
    "trademark",
    "commission",
    "crypto",
    "advisory",
)


def classify_service_mode(service_obj):
    """Classify dynamic service branches as catalog-oriented or inquiry-oriented."""
    if not service_obj:
        return "catalog"
    source = f"{getattr(service_obj, 'name', '')} {getattr(service_obj, 'category_name', '')}".lower()
    if any(keyword in source for keyword in INQUIRY_SERVICE_KEYWORDS):
        return "inquiry"
    return "catalog"


def dynamic_cta_copy(service_mode):
    """Return template-friendly CTA labels by service mode."""
    if service_mode == "inquiry":
        return {
            "primary": "Book Consultation",
            "secondary": "Submit Service Inquiry",
            "card_view": "View Service Brief",
            "related_title": "Related Service Areas",
            "list_title": "Service Engagement Areas",
            "quick_label": "Consultation Areas",
            "section_hint": "Review the service areas below and send an inquiry for tailored support."
        }
    return {
        "primary": "Request Quote",
        "secondary": "Request This Service",
        "card_view": "View Details",
        "related_title": "Related Offerings",
        "list_title": "Offerings",
        "quick_label": "Related Offerings",
        "section_hint": "Browse available items and select one to view details."
    }


INQUIRY_FORMS = {
    "digital-id-solutions": {
        "service_label": "Digital ID Solutions",
        "headline": "Request ID Solution",
        "description": "Share your identity card requirements and we will propose the right card, printer, and consumables setup.",
        "submit_label": "Submit ID Request",
        "theme": "digital",
        "icon": "bi-person-vcard",
        "hero_image": "images/placeholders/digital-id.svg",
        "highlights": ["ID Printing", "Machine Guidance", "Consumables Plan"],
        "summary_points": [
            "Tell us your card volume and use case.",
            "Select if you need printer setup and consumables.",
            "Get a tailored recommendation from our team."
        ],
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True, "placeholder": "Enter your full name"},
            {"name": "organization", "label": "Organization / Company", "type": "text", "required": True, "placeholder": "School, hospital, office, etc."},
            {"name": "phone", "label": "Phone", "type": "tel", "required": True, "placeholder": "Phone number"},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "cards_needed", "label": "Number of Cards Needed", "type": "number", "required": True, "placeholder": "e.g. 500"},
            {"name": "card_type", "label": "Card Type / Use Case", "type": "select", "required": True, "options": ["Staff ID", "Student ID", "Visitor Card", "Membership Card", "Event Access Card", "Other (Specify in Notes)"]},
            {"name": "need_printer", "label": "Need Printer?", "type": "radio", "required": True, "options": ["Yes", "No", "Not sure"]},
            {"name": "need_consumables", "label": "Consumables Needed", "type": "checkbox", "required": False, "options": ["PVC Cards", "Ribbons", "Lanyards", "Card Holders", "Cleaning Kits", "Other (Specify in Notes)"]},
            {"name": "deadline", "label": "Preferred Deadline", "type": "date", "required": False},
            {"name": "notes", "label": "Notes / Other Requirements", "type": "textarea", "required": False, "placeholder": "Tell us anything not listed above"},
        ],
        "groups": [
            {"title": "Contact Details", "hint": "Who should we follow up with?", "fields": ["full_name", "organization", "phone", "email"]},
            {"title": "ID Requirement Scope", "hint": "Help us estimate the right setup.", "fields": ["cards_needed", "card_type", "need_printer", "need_consumables", "deadline"]},
            {"title": "Additional Notes", "hint": "Add any custom request or context.", "fields": ["notes"]},
        ],
    },
    "machine-sales-consumables": {
        "service_label": "Machine Sales & Consumables",
        "headline": "Request Equipment Quote",
        "description": "Tell us the machine category, quantity, and consumables requirements for a tailored quote.",
        "submit_label": "Request Equipment Quote",
        "theme": "equipment",
        "icon": "bi-cpu",
        "hero_image": "images/placeholders/id-machine.svg",
        "highlights": ["Machine Sourcing", "Consumables", "Quote Support"],
        "summary_points": [
            "Select machine type and quantity.",
            "Add location and budget range for better quote accuracy.",
            "Include consumables and preferred model details."
        ],
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
            {"name": "company", "label": "Company", "type": "text", "required": True},
            {"name": "phone", "label": "Phone", "type": "tel", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "machine_type", "label": "Machine Type", "type": "select", "required": True, "options": ["ID Card Printer", "Laminator", "Embosser", "Industrial Machine", "Other (Specify in Notes)"]},
            {"name": "preferred_model", "label": "Preferred Brand / Model", "type": "text", "required": False},
            {"name": "quantity", "label": "Quantity", "type": "number", "required": True},
            {"name": "consumables_needed", "label": "Consumables Needed", "type": "checkbox", "required": False, "options": ["PVC Cards", "Ribbons", "Cleaning Kits", "Printer Rollers", "Other (Specify in Notes)"]},
            {"name": "location", "label": "Delivery Location", "type": "text", "required": True},
            {"name": "budget_range", "label": "Budget Range", "type": "select", "required": False, "options": ["Below NGN 500,000", "NGN 500,000 - 1,500,000", "NGN 1,500,000 - 5,000,000", "Above NGN 5,000,000", "Prefer to discuss"]},
            {"name": "notes", "label": "Notes / Other Requirements", "type": "textarea", "required": False},
        ],
        "groups": [
            {"title": "Requester Details", "hint": "Where should the quote be sent?", "fields": ["full_name", "company", "phone", "email"]},
            {"title": "Equipment Requirements", "hint": "Select the equipment and consumables scope.", "fields": ["machine_type", "preferred_model", "quantity", "consumables_needed"]},
            {"title": "Commercial Details", "hint": "These details help us send a practical quote faster.", "fields": ["location", "budget_range", "notes"]},
        ],
    },
    "printing-supplies": {
        "service_label": "Printing & Supplies",
        "headline": "Request Print Service",
        "description": "Submit your print job scope, quantity, and timeline for a business-ready response.",
        "submit_label": "Submit Print Request",
        "theme": "print",
        "icon": "bi-printer",
        "hero_image": "images/placeholders/printing-supplies.svg",
        "highlights": ["Print Production", "Branding", "Fulfillment"],
        "summary_points": [
            "Choose print item/service type.",
            "Add quantity, specs, and finishing details.",
            "Tell us deadline and design support needs."
        ],
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
            {"name": "company", "label": "Company", "type": "text", "required": True},
            {"name": "phone", "label": "Phone", "type": "tel", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "service_type", "label": "Item / Service Type", "type": "select", "required": True, "options": ["Business Cards", "Flyers", "Brochures", "Banners", "Letterheads", "Stickers / Labels", "Other (Specify in Notes)"]},
            {"name": "quantity", "label": "Quantity", "type": "number", "required": True},
            {"name": "specification", "label": "Specification", "type": "textarea", "required": True, "placeholder": "Size, color mode, paper type, dimensions, etc."},
            {"name": "finishing", "label": "Finishing / Extras", "type": "checkbox", "required": False, "options": ["Lamination", "Embossing", "Perforation", "Binding", "Cut-to-size", "Other (Specify in Notes)"]},
            {"name": "deadline", "label": "Deadline", "type": "date", "required": False},
            {"name": "design_support", "label": "Need Design Support?", "type": "radio", "required": True, "options": ["Yes", "No", "Not sure"]},
            {"name": "notes", "label": "Notes / Other Requirements", "type": "textarea", "required": False},
        ],
        "groups": [
            {"title": "Contact Details", "hint": "Who is coordinating the print request?", "fields": ["full_name", "company", "phone", "email"]},
            {"title": "Print Job Details", "hint": "Give us enough detail to estimate accurately.", "fields": ["service_type", "quantity", "specification", "finishing"]},
            {"title": "Timeline & Support", "hint": "Set urgency and any extra support needs.", "fields": ["deadline", "design_support", "notes"]},
        ],
    },
    "travel-agency": {
        "service_label": "Travel Agency Support",
        "headline": "Request Travel Assistance",
        "description": "Share your travel plans and documentation needs for coordinated support.",
        "submit_label": "Submit Travel Request",
        "theme": "travel",
        "icon": "bi-airplane",
        "hero_image": "images/placeholders/travel-agency.svg",
        "highlights": ["Trip Planning", "Documentation", "Corporate Travel"],
        "summary_points": [
            "Share destination and travel timing.",
            "Select assistance type and visa/document support.",
            "Add any special traveler considerations."
        ],
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
            {"name": "phone", "label": "Phone", "type": "tel", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "destination", "label": "Destination", "type": "text", "required": True},
            {"name": "travel_date", "label": "Travel Date", "type": "date", "required": True},
            {"name": "travelers", "label": "Number of Travelers", "type": "number", "required": True},
            {"name": "assistance_type", "label": "Assistance Type", "type": "select", "required": True, "options": ["Flight Booking", "Hotel Booking", "Tour Package", "Visa Advisory", "Documentation Support", "Other (Specify in Notes)"]},
            {"name": "visa_help", "label": "Visa / Documentation Help Needed?", "type": "radio", "required": True, "options": ["Yes", "No", "Not sure"]},
            {"name": "notes", "label": "Notes / Other Requirements", "type": "textarea", "required": False},
        ],
        "groups": [
            {"title": "Traveler Details", "hint": "Primary contact for this request.", "fields": ["full_name", "phone", "email"]},
            {"title": "Trip Information", "hint": "Core travel details for planning.", "fields": ["destination", "travel_date", "travelers", "assistance_type"]},
            {"title": "Documentation & Notes", "hint": "Tell us about visa or document expectations.", "fields": ["visa_help", "notes"]},
        ],
    },
    "cac-trademark-commission": {
        "service_label": "CAC / Trademark / Commission Services",
        "headline": "Start Business Support Request",
        "description": "Submit your registration/compliance request and our team will guide next steps.",
        "submit_label": "Start Support Request",
        "theme": "support",
        "icon": "bi-briefcase",
        "hero_image": "images/placeholders/operations.svg",
        "highlights": ["Registration", "Compliance", "Documentation"],
        "summary_points": [
            "Choose your request category.",
            "Set urgency and add context.",
            "We follow up with clear next-step guidance."
        ],
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
            {"name": "phone", "label": "Phone", "type": "tel", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "business_type", "label": "Business / Service Type", "type": "text", "required": True},
            {"name": "request_category", "label": "Request Category", "type": "select", "required": True, "options": ["CAC Registration", "Trademark Filing", "Commission Documentation", "Regulatory Guidance", "Other (Specify in Notes)"]},
            {"name": "urgency", "label": "Urgency", "type": "radio", "required": True, "options": ["Normal", "Urgent", "Immediate"]},
            {"name": "notes", "label": "Notes / Other Requirements", "type": "textarea", "required": False},
        ],
        "groups": [
            {"title": "Requester Details", "hint": "Business owner or authorized contact.", "fields": ["full_name", "phone", "email"]},
            {"title": "Support Request", "hint": "Select the area where you need support.", "fields": ["business_type", "request_category", "urgency"]},
            {"title": "Additional Notes", "hint": "Add any custom need not listed above.", "fields": ["notes"]},
        ],
    },
    "pharmaceutical-distribution": {
        "service_label": "Pharmaceutical Distribution",
        "headline": "Request Pharmaceutical Distribution Support",
        "description": "Share your product scope and delivery requirements for coordinated distribution support.",
        "submit_label": "Submit Pharma Inquiry",
        "theme": "pharma",
        "icon": "bi-capsule-pill",
        "hero_image": "images/placeholders/pharmaceutical-distribution.svg",
        "highlights": ["Distribution", "Restock Planning", "Facility Support"],
        "summary_points": [
            "Tell us organization and product scope.",
            "Add location and quantity/restock plan.",
            "We respond with distribution support options."
        ],
        "fields": [
            {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
            {"name": "organization", "label": "Organization / Facility", "type": "text", "required": True},
            {"name": "phone", "label": "Phone", "type": "tel", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "product_scope", "label": "Product Scope", "type": "text", "required": True},
            {"name": "quantity_plan", "label": "Quantity / Restock Plan", "type": "text", "required": True},
            {"name": "delivery_location", "label": "Delivery Location", "type": "text", "required": True},
            {"name": "notes", "label": "Notes / Other Requirements", "type": "textarea", "required": False},
        ],
        "groups": [
            {"title": "Organization Details", "hint": "Who is requesting this support?", "fields": ["full_name", "organization", "phone", "email"]},
            {"title": "Distribution Scope", "hint": "Share scope and logistics context.", "fields": ["product_scope", "quantity_plan", "delivery_location"]},
            {"title": "Additional Notes", "hint": "Add any requirements not captured above.", "fields": ["notes"]},
        ],
    },
}


def infer_inquiry_service_key(source_value):
    source = (source_value or "").lower()
    if "pharma" in source:
        return "pharmaceutical-distribution"
    if "machine" in source or "consumable" in source or "equipment" in source:
        return "machine-sales-consumables"
    if "travel" in source:
        return "travel-agency"
    if "cac" in source or "trademark" in source or "commission" in source:
        return "cac-trademark-commission"
    if "cards" in source or "digital id" in source or "id card" in source:
        return "digital-id-solutions"
    if "print" in source or "marketing" in source or "sticker" in source or "sign" in source:
        return "printing-supplies"
    return None


@app.template_global()
def inquiry_url_for_service(service_obj):
    if not service_obj:
        return url_for("contact")
    source = f"{getattr(service_obj, 'name', '')} {getattr(service_obj, 'category_name', '')}"
    key = infer_inquiry_service_key(source)
    if not key:
        return url_for("contact", head=getattr(service_obj, "category_name", ""))
    return url_for("service_inquiry", service_key=key)

def contact_to_dict(c):
    return {
        "id": c.id,
        "phone": c.phone,
        "variables": {v.name: v.content for v in c.variables},
        "group_id": c.group.id if c.group else None,
        "group_name": c.group.name if c.group else None
    }



# --- Routes ---

@app.route("/health")
def health():
    return jsonify({"ok": True})



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_error(e):
    return render_template("500.html"), 500

@app.route("/force500")
def force500():
    return 1 / 0

@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "")

    related_matches = db.session.query(Services).outerjoin(SubService).outerjoin(Products).filter(
        or_(
            Services.name.ilike(f'%{query}%'),
            Services.category_name.ilike(f'%{query}%'),
            SubService.name.ilike(f'%{query}%'),
            SubService.category_name.ilike(f'%{query}%'),
            Products.name.ilike(f'%{query}%'),
            Products.category_name.ilike(f'%{query}%'),
        )
    ).limit(5).all()

    header_matches = Header.query.filter(
        or_(
            Header.name.ilike(f'%{query}%'),
            Header.end_url.ilike(f'%{query}%')
        )
    ).limit(5).all()

    # Format for JSON suggestions
    suggestions = [
        {
            "title": getattr(item, 'name', getattr(item, 'category_name', '')),
            "url": get_item_url(item)
        }
        for item in related_matches + header_matches
    ]
    return jsonify(suggestions)

def get_item_url(item):
    name = item.name
    if Services.query.filter_by(name=name).first():
        category = item.category_name
        return url_for('services', name=category)
    elif SubService.query.filter_by(name=name).first():
        category = item.category_name
        service_name = item.services.category_name
        return url_for('services', name=service_name, sec=category)
    elif Products.query.filter_by(name=name).first():
        if item.services:
            category = item.category_name
            service_name = item.services.category_name
            return url_for('services', name=service_name, sec=category)
        else:
            category = item.category_name
            subservice_name = item.subservice.category_name
            service_name = item.subservice.services.category_name
            return url_for('services', name=service_name, sec=subservice_name, pro=category)
    elif Header.query.filter_by(name=name).first():
        return url_for(item.end_url)

@app.route('/search', methods=['POST'])
def search_result():
    query = request.form.get("search")
    related_matches = db.session.query(Services).outerjoin(SubService).outerjoin(Products).filter(
        or_(
            Services.name.ilike(f'%{query}%'),
            Services.category_name.ilike(f'%{query}%'),
            SubService.name.ilike(f'%{query}%'),
            SubService.category_name.ilike(f'%{query}%'),
            Products.name.ilike(f'%{query}%'),
            Products.category_name.ilike(f'%{query}%'),
        )
    ).all()

    header_matches = Header.query.filter(
        or_(
            Header.name.ilike(f'%{query}%'),
            Header.end_url.ilike(f'%{query}%')
        )
    ).all()
    suggestions = [
        {
            "title": getattr(item, 'name', getattr(item, 'category_name', '')),
            "url": get_item_url(item)
        }
        for item in related_matches + header_matches
    ]
    print(suggestions)
    return render_template("search_result.html", results=suggestions)


@app.route("/")
def home():
    header = Header.query.all()
    service = Services.query.all()
    random_service1 = Services.query.filter_by(name="Marketing Essentials").first()
    random_sub1 = choice(random_service1.sub_service)
    random_product1 = choice(random_sub1.products)
    random_service2 = Services.query.filter_by(name="Cards").first()
    random_sub2 = ""
    for n in random_service2.sub_service:
        if n.name == "ID Cards":
            random_sub2 = n
    random_product2 = random_sub2.products
    change = True
    the_name = "home"
    return render_template("main.html",the_name=the_name, change=change, random_sub1=random_sub1, random_sub2=random_sub2, random_product2=random_product2, random_product1=random_product1, header=header, services=service)

@app.route("/printing")
def printing():
    # Legacy public route: keep compatibility, but send visitors to the
    # corporate services overview instead of the old storefront-style page.
    return redirect(url_for("all"), code=301)

@app.route("/business-reg")
def business_registration():
    # Legacy public route: map business registration intent into the newer
    # service-specific support flow.
    return redirect(url_for("service_inquiry", service_key="cac-trademark-commission"), code=301)


@app.route("/services/<name>")
@app.route("/services/<name>/<sec>")
@app.route("/services/<name>/<sec>/<pro>")
def services(name=None, sec=None, pro=None):
    data = ""
    the_name=""
    if name and sec and pro:
        if Services.query.filter_by(category_name=name).first():
            if SubService.query.filter_by(category_name=sec).first():
                if Products.query.filter_by(category_name=pro).first():
                    the_name = name
                    templates = "products.html"
                    data = Products.query.filter_by(category_name=pro).first()
                else:
                    return page_not_found(NotFound("Items not found"))
            else:
                return page_not_found(NotFound("Items not found"))
        else:
            return page_not_found(NotFound("Items not found"))
    elif name and sec:
        if Services.query.filter_by(category_name=name).first():
            if SubService.query.filter_by(category_name=sec).first():
                the_name = name
                templates = "subservice.html"
                data = SubService.query.filter_by(category_name=sec).first()
            elif Products.query.filter_by(category_name=sec).first():
                the_name = name
                templates = "products.html"
                data = Products.query.filter_by(category_name=sec).first()
            else:
                return page_not_found(NotFound("Items not found"))
        else:
            return page_not_found(NotFound("Items not found"))
    elif name:
        if Services.query.filter_by(category_name=name).first():
            the_name = name
            templates = "service.html"
            data = Services.query.filter_by(category_name=the_name).first()
        else:
            return page_not_found(NotFound("Items not found"))


    the_data = data
    header = Header.query.all()
    service = Services.query.all()
    change=True
    rows = [service[n:n+2] for n in range(0, len(service), 2)]
    random_service = [choice(service), choice(service)]

    parent_service = None
    if isinstance(the_data, Services):
        parent_service = the_data
    elif isinstance(the_data, SubService):
        parent_service = the_data.services
    elif isinstance(the_data, Products):
        parent_service = the_data.subservice.services if the_data.subservice else the_data.services

    service_mode = classify_service_mode(parent_service)
    cta_copy = dynamic_cta_copy(service_mode)

    return render_template(
        f"{templates}",
        the_data=the_data,
        random_service=random_service,
        rows=rows,
        change=change,
        header=header,
        services=service,
        the_name=the_name,
        service_mode=service_mode,
        cta_copy=cta_copy
    )

@app.route("/all_services")
def all():
    the_name = "var"
    header = Header.query.all()
    service = Services.query.all()
    change=True
    rows = [service[n:n+2] for n in range(0, len(service), 2)]
    random_service = [choice(service), choice(service)]
    return render_template('all_services.html', random_service=random_service, rows=rows, change=change, header=header, services=service, the_name=the_name)


@app.route("/bulk-sms")
@login_required
def bulk_sms():
    the_name = 'var'
    show_welcome_toast = False
    the_name = 'var'
    if current_user.new:
        current_user.new = False
        show_welcome_toast = True
        db.session.commit()
    total = Message.query.filter_by(user_id=current_user.id).count()
    delivered = Message.query.filter_by(user_id=current_user.id, status="delivered").count()
    pending = Message.query.filter_by(user_id=current_user.id, status="pending").count()
    failed = Message.query.filter_by(user_id=current_user.id, status="failed").count()
    recent_messages = ContactTransact.query.order_by(ContactTransact.created_at.desc()).limit(5).all()

    delivery_rate = (delivered / total * 100) if total > 0 else 0

    return render_template("dashboard.html", recent_messages=recent_messages, the_name=the_name,
                           delivery_rate=delivery_rate, total=total, delivered=delivered, pending=pending,
                           failed=failed, bulkk_sms=True, show_welcome_toast=show_welcome_toast)

@app.route("/about-us")
def about_us():
    header = Header.query.all()
    service = Services.query.all()
    change = True
    return render_template("about_us.html", change=change, header=header, services=service)

@app.route("/leadership")
def leadership():
    header = Header.query.all()
    service = Services.query.all()
    change = True
    return render_template("leadership.html", change=change, header=header, services=service)

@app.route("/pricing")
@app.route("/princing")
def pricing():
    # Legacy compatibility route: keep old typo path, redirect to corporate services overview.
    return redirect(url_for("all"), code=301)


def send_inquiry_email(subject, body):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_mail = "ifeanyiagada9@gmail.com"
    receiver = "ifeanyiagada123@gmail.com"
    password = os.environ.get("PASSWORD_TEXT")
    message = EmailMessage()
    message["From"] = sender_mail
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_mail, password)
        server.send_message(message)


@app.route("/inquiry/<service_key>", methods=["GET", "POST"])
def service_inquiry(service_key):
    config = INQUIRY_FORMS.get(service_key)
    if not config:
        return page_not_found(NotFound("Inquiry type not found"))

    header = Header.query.all()
    service = Services.query.all()
    change = True

    if request.method == "POST":
        payload = {}
        errors = {}
        for field in config["fields"]:
            field_name = field["name"]
            field_type = field.get("type")
            if field_type == "checkbox":
                values = [val.strip() for val in request.form.getlist(field_name) if val.strip()]
                payload[field_name] = ", ".join(values)
                if field.get("required") and not values:
                    errors[field_name] = [f"{field['label']} is required."]
            else:
                value = (request.form.get(field_name) or "").strip()
                payload[field_name] = value
                if field.get("required") and not value:
                    errors[field_name] = [f"{field['label']} is required."]

        email_value = payload.get("email", "")
        if email_value and "@" not in email_value:
            errors["email"] = ["Enter a valid email address."]

        if errors:
            return jsonify({"success": False, "errors": errors})

        body_lines = [
            f"Service Inquiry: {config['service_label']}",
            "",
        ]
        for field in config["fields"]:
            label = field["label"]
            key = field["name"]
            body_lines.append(f"{label}: {payload.get(key, '') or '-'}")

        send_inquiry_email(
            subject=f"New {config['service_label']} Inquiry - Gregbuk Website",
            body="\n".join(body_lines)
        )
        return jsonify({"success": True})

    return render_template(
        "inquiry_form.html",
        inquiry_config=config,
        field_map={field["name"]: field for field in config["fields"]},
        service_key=service_key,
        change=change,
        header=header,
        services=service,
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    head = request.args.get("head")
    header = Header.query.all()
    service = Services.query.all()
    change= True
    form=ContactForm()
    choices = [("select", "Select from the dropdown")]
    choices2 = [(serve.category_name, serve.name) for serve in service]
    choices.extend(choices2)
    form.head.choices = choices
    if head:
        data = Services.query.filter_by(category_name=head).first()
        if data:
            form.head.data = data.category_name
    if request.method == "POST":
        if form.validate_on_submit():
            the_head = form.head.data
            the_name = form.name.data
            the_email = form.email.data
            the_phone = form.phone.data
            the_message = form.message.data
            email_body = (
                f"Header: {the_head}\n\n"
                f"Name: {the_name}\n\n"
                f"Email: {the_email}\n\n"
                f"Phone Number: {the_phone}\n\n"
                f"Message: {the_message}"
            )
            send_inquiry_email("Contact Message from Gregbuk Website", email_body)

            return jsonify({"success": True})
        else:
            errors = {field: errors for field, errors in form.errors.items()}
            return jsonify({"success": False, "errors": errors})

    return render_template("contact_us.html", form=form, change=change, header=header, services=service)


@app.route("/thank-you")
def thank_you():
    header = Header.query.all()
    service = Services.query.all()
    change = True
    return render_template("thank_you.html", change=change, header=header, services=service)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    register = True
    header = Header.query.all()
    change = True
    if request.method == "POST":
        data = request.form
        username = data.get("name")
        email = data.get("email")
        password = data.get("password")
        re_pass = data.get("re_password")
        if User.query.filter_by(email=email).first():
            flash("Email already registered! Login Instead", "danger")
            return redirect(url_for("login"))
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(
            username=username,
            email=email,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("dashboard"))

    return render_template("register.html", register=register, change=change, header=header)

@app.route("/login", methods=["GET", "POST"])
def login():
    login=True
    header = Header.query.all()
    change = True
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or Password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", login=login, change=change, header=header)

@app.route("/dashboard")
@login_required
def dashboard():
    show_welcome_toast = False
    the_name = 'var'
    if current_user.new:
        current_user.new = False
        show_welcome_toast = True
        db.session.commit()
    total = Message.query.filter_by(user_id=current_user.id).count()
    delivered = Message.query.filter_by(user_id=current_user.id, status="delivered").count()
    pending = Message.query.filter_by(user_id=current_user.id, status="pending").count()
    failed = Message.query.filter_by(user_id=current_user.id, status="failed").count()
    recent_messages = ContactTransact.query.order_by(ContactTransact.created_at.desc()).limit(5).all()

    delivery_rate = (delivered / total * 100) if total > 0 else 0

    return render_template("dashboard.html", recent_messages=recent_messages, the_name=the_name, delivery_rate=delivery_rate, total=total, delivered=delivered, pending=pending, failed=failed, bulkk_sms=True, show_welcome_toast=show_welcome_toast)


@app.route("/dashboard/seed-targeted-services", methods=["POST"])
@login_required
def dashboard_seed_targeted_services():
    from seed_targeted_services import seed_targeted_services

    results = seed_targeted_services()
    flash(
        "Targeted service seed complete. "
        f"Created services: {results['services_created']}, "
        f"refreshed services: {results['services_updated']}, "
        f"created subservices: {results['subservices_created']}, "
        f"refreshed subservices: {results['subservices_updated']}, "
        f"created products: {results['products_created']}, "
        f"refreshed products: {results['products_updated']}.",
        "success",
    )
    return redirect(url_for("dashboard"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    metrics = {
        "services": Services.query.count(),
        "subservices": SubService.query.count(),
        "products": Products.query.count(),
        "headers": Header.query.count(),
        "users": User.query.count(),
        "contacts": Contact.query.count(),
        "messages": Message.query.count(),
        "transactions": Transaction.query.count(),
    }
    latest_users = User.query.order_by(User.id.desc()).limit(8).all()
    latest_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(8).all()
    latest_messages = Message.query.order_by(Message.created_at.desc()).limit(8).all()
    return render_template(
        "admin_dashboard.html",
        metrics=metrics,
        latest_users=latest_users,
        latest_contacts=latest_contacts,
        latest_messages=latest_messages,
        summarize_text=summarize_text,
        **admin_layout_context("admin-dashboard")
    )


@app.route("/admin/tools/seed-targeted-services", methods=["POST"])
@admin_required
def admin_seed_targeted_services():
    from seed_targeted_services import seed_targeted_services

    results = seed_targeted_services()
    flash(
        "Corporate service seed complete. "
        f"Created services: {results['services_created']}, "
        f"refreshed services: {results['services_updated']}, "
        f"created subservices: {results['subservices_created']}, "
        f"refreshed subservices: {results['subservices_updated']}, "
        f"created products: {results['products_created']}, "
        f"refreshed products: {results['products_updated']}.",
        "success",
    )
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/services")
@admin_required
def admin_services():
    records = Services.query.order_by(Services.id.desc()).all()
    return render_template(
        "admin_list.html",
        title="Manage Services",
        subtitle="Create, update, and remove top-level public service categories.",
        records=records,
        columns=[
            ("ID", lambda item: item.id),
            ("Name", lambda item: item.name),
            ("Category", lambda item: item.category_name),
            ("Subservices", lambda item: len(item.sub_service)),
            ("Products", lambda item: len(item.products)),
        ],
        create_url=url_for("admin_service_create"),
        edit_endpoint="admin_service_edit",
        delete_endpoint="admin_service_delete",
        item_kind="service",
        page_key="admin-services",
        **admin_layout_context("admin-services")
    )


@app.route("/admin/services/new", methods=["GET", "POST"])
@admin_required
def admin_service_create():
    if request.method == "POST":
        service = Services(
            name=(request.form.get("name") or "").strip(),
            category_name=(request.form.get("category_name") or "").strip(),
            description=(request.form.get("description") or "").strip(),
            image_url=(request.form.get("image_url") or "").strip(),
            icon_name=(request.form.get("icon_name") or "").strip(),
            alt_texts=(request.form.get("alt_texts") or "").strip(),
            content=(request.form.get("content") or "").strip(),
        )
        db.session.add(service)
        db.session.commit()
        flash("Service created successfully.", "success")
        return redirect(url_for("admin_services"))

    return render_template(
        "admin_form.html",
        title="Create Service",
        subtitle="Add a new top-level service category.",
        submit_label="Create Service",
        fields=[
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category_name", "label": "Category Name", "type": "text", "required": True},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "image_url", "label": "Image URL / Path", "type": "text"},
            {"name": "icon_name", "label": "Icon Name", "type": "text"},
            {"name": "alt_texts", "label": "Alt Text", "type": "text"},
            {"name": "content", "label": "HTML Content", "type": "textarea", "rows": 10},
        ],
        values={},
        back_url=url_for("admin_services"),
        **admin_layout_context("admin-services")
    )


@app.route("/admin/services/<int:service_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_service_edit(service_id):
    service = Services.query.get_or_404(service_id)
    if request.method == "POST":
        service.name = (request.form.get("name") or "").strip()
        service.category_name = (request.form.get("category_name") or "").strip()
        service.description = (request.form.get("description") or "").strip()
        service.image_url = (request.form.get("image_url") or "").strip()
        service.icon_name = (request.form.get("icon_name") or "").strip()
        service.alt_texts = (request.form.get("alt_texts") or "").strip()
        service.content = (request.form.get("content") or "").strip()
        db.session.commit()
        flash("Service updated successfully.", "success")
        return redirect(url_for("admin_services"))

    return render_template(
        "admin_form.html",
        title=f"Edit Service: {service.name}",
        subtitle="Update the service metadata and public content.",
        submit_label="Save Service",
        fields=[
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category_name", "label": "Category Name", "type": "text", "required": True},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "image_url", "label": "Image URL / Path", "type": "text"},
            {"name": "icon_name", "label": "Icon Name", "type": "text"},
            {"name": "alt_texts", "label": "Alt Text", "type": "text"},
            {"name": "content", "label": "HTML Content", "type": "textarea", "rows": 10},
        ],
        values={
            "name": service.name,
            "category_name": service.category_name,
            "description": service.description,
            "image_url": service.image_url,
            "icon_name": service.icon_name,
            "alt_texts": service.alt_texts,
            "content": service.content,
        },
        back_url=url_for("admin_services"),
        **admin_layout_context("admin-services")
    )


@app.route("/admin/services/<int:service_id>/delete", methods=["POST"])
@admin_required
def admin_service_delete(service_id):
    service = Services.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Service deleted successfully.", "success")
    return redirect(url_for("admin_services"))


@app.route("/admin/subservices")
@admin_required
def admin_subservices():
    records = SubService.query.order_by(SubService.id.desc()).all()
    return render_template(
        "admin_list.html",
        title="Manage Subservices",
        subtitle="Maintain grouped service branches under each top-level category.",
        records=records,
        columns=[
            ("ID", lambda item: item.id),
            ("Name", lambda item: item.name),
            ("Category", lambda item: item.category_name),
            ("Parent Service", lambda item: item.services.name if item.services else "-"),
            ("Products", lambda item: len(item.products)),
        ],
        create_url=url_for("admin_subservice_create"),
        edit_endpoint="admin_subservice_edit",
        delete_endpoint="admin_subservice_delete",
        item_kind="subservice",
        page_key="admin-subservices",
        **admin_layout_context("admin-subservices")
    )


@app.route("/admin/subservices/new", methods=["GET", "POST"])
@admin_required
def admin_subservice_create():
    service_choices = Services.query.order_by(Services.name.asc()).all()
    if request.method == "POST":
        subservice = SubService(
            name=(request.form.get("name") or "").strip(),
            category_name=(request.form.get("category_name") or "").strip(),
            description=(request.form.get("description") or "").strip(),
            image_url=(request.form.get("image_url") or "").strip(),
            alt_texts=(request.form.get("alt_texts") or "").strip(),
            content=(request.form.get("content") or "").strip(),
            service_id=int(request.form.get("service_id")),
        )
        db.session.add(subservice)
        db.session.commit()
        flash("Subservice created successfully.", "success")
        return redirect(url_for("admin_subservices"))

    return render_template(
        "admin_form.html",
        title="Create Subservice",
        subtitle="Add a grouped service branch under a top-level service.",
        submit_label="Create Subservice",
        fields=[
            {"name": "service_id", "label": "Parent Service", "type": "select", "required": True, "options": [(str(item.id), item.name) for item in service_choices]},
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category_name", "label": "Category Name", "type": "text", "required": True},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "image_url", "label": "Image URL / Path", "type": "text"},
            {"name": "alt_texts", "label": "Alt Text", "type": "text"},
            {"name": "content", "label": "HTML Content", "type": "textarea", "rows": 10},
        ],
        values={},
        back_url=url_for("admin_subservices"),
        **admin_layout_context("admin-subservices")
    )


@app.route("/admin/subservices/<int:subservice_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_subservice_edit(subservice_id):
    subservice = SubService.query.get_or_404(subservice_id)
    service_choices = Services.query.order_by(Services.name.asc()).all()
    if request.method == "POST":
        subservice.service_id = int(request.form.get("service_id"))
        subservice.name = (request.form.get("name") or "").strip()
        subservice.category_name = (request.form.get("category_name") or "").strip()
        subservice.description = (request.form.get("description") or "").strip()
        subservice.image_url = (request.form.get("image_url") or "").strip()
        subservice.alt_texts = (request.form.get("alt_texts") or "").strip()
        subservice.content = (request.form.get("content") or "").strip()
        db.session.commit()
        flash("Subservice updated successfully.", "success")
        return redirect(url_for("admin_subservices"))

    return render_template(
        "admin_form.html",
        title=f"Edit Subservice: {subservice.name}",
        subtitle="Update grouped service information and relationship.",
        submit_label="Save Subservice",
        fields=[
            {"name": "service_id", "label": "Parent Service", "type": "select", "required": True, "options": [(str(item.id), item.name) for item in service_choices]},
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category_name", "label": "Category Name", "type": "text", "required": True},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "image_url", "label": "Image URL / Path", "type": "text"},
            {"name": "alt_texts", "label": "Alt Text", "type": "text"},
            {"name": "content", "label": "HTML Content", "type": "textarea", "rows": 10},
        ],
        values={
            "service_id": str(subservice.service_id),
            "name": subservice.name,
            "category_name": subservice.category_name,
            "description": subservice.description,
            "image_url": subservice.image_url,
            "alt_texts": subservice.alt_texts,
            "content": subservice.content,
        },
        back_url=url_for("admin_subservices"),
        **admin_layout_context("admin-subservices")
    )


@app.route("/admin/subservices/<int:subservice_id>/delete", methods=["POST"])
@admin_required
def admin_subservice_delete(subservice_id):
    subservice = SubService.query.get_or_404(subservice_id)
    db.session.delete(subservice)
    db.session.commit()
    flash("Subservice deleted successfully.", "success")
    return redirect(url_for("admin_subservices"))


@app.route("/admin/products")
@admin_required
def admin_products():
    records = Products.query.order_by(Products.id.desc()).all()
    return render_template(
        "admin_list.html",
        title="Manage Products / Offerings",
        subtitle="Maintain detailed offerings under either a service or a subservice.",
        records=records,
        columns=[
            ("ID", lambda item: item.id),
            ("Name", lambda item: item.name),
            ("Category", lambda item: item.category_name),
            ("Parent", lambda item: item.subservice.name if item.subservice else (item.services.name if item.services else "-")),
            ("Gallery", lambda item: len(item.image_collections)),
        ],
        create_url=url_for("admin_product_create"),
        edit_endpoint="admin_product_edit",
        delete_endpoint="admin_product_delete",
        item_kind="product",
        page_key="admin-products",
        **admin_layout_context("admin-products")
    )


@app.route("/admin/products/new", methods=["GET", "POST"])
@admin_required
def admin_product_create():
    service_choices = Services.query.order_by(Services.name.asc()).all()
    subservice_choices = SubService.query.order_by(SubService.name.asc()).all()
    if request.method == "POST":
        service_id = request.form.get("service_id") or None
        subservice_id = request.form.get("sub_service_id") or None
        product = Products(
            name=(request.form.get("name") or "").strip(),
            category_name=(request.form.get("category_name") or "").strip(),
            description=(request.form.get("description") or "").strip(),
            image_url=(request.form.get("image_url") or "").strip(),
            alt_texts=(request.form.get("alt_texts") or "").strip(),
            content=(request.form.get("content") or "").strip(),
            service_id=int(service_id) if service_id else None,
            sub_service_id=int(subservice_id) if subservice_id else None,
        )
        db.session.add(product)
        db.session.commit()
        flash("Product created successfully.", "success")
        return redirect(url_for("admin_products"))

    return render_template(
        "admin_form.html",
        title="Create Product / Offering",
        subtitle="Add a service detail under a top-level service or a subservice.",
        submit_label="Create Product",
        fields=[
            {"name": "service_id", "label": "Parent Service (optional)", "type": "select", "options": [("", "None")] + [(str(item.id), item.name) for item in service_choices]},
            {"name": "sub_service_id", "label": "Parent Subservice (optional)", "type": "select", "options": [("", "None")] + [(str(item.id), item.name) for item in subservice_choices]},
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category_name", "label": "Category Name", "type": "text", "required": True},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "image_url", "label": "Image URL / Path", "type": "text"},
            {"name": "alt_texts", "label": "Alt Text", "type": "text"},
            {"name": "content", "label": "HTML Content", "type": "textarea", "rows": 10},
        ],
        values={},
        back_url=url_for("admin_products"),
        **admin_layout_context("admin-products")
    )


@app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_product_edit(product_id):
    product = Products.query.get_or_404(product_id)
    service_choices = Services.query.order_by(Services.name.asc()).all()
    subservice_choices = SubService.query.order_by(SubService.name.asc()).all()
    if request.method == "POST":
        service_id = request.form.get("service_id") or None
        subservice_id = request.form.get("sub_service_id") or None
        product.service_id = int(service_id) if service_id else None
        product.sub_service_id = int(subservice_id) if subservice_id else None
        product.name = (request.form.get("name") or "").strip()
        product.category_name = (request.form.get("category_name") or "").strip()
        product.description = (request.form.get("description") or "").strip()
        product.image_url = (request.form.get("image_url") or "").strip()
        product.alt_texts = (request.form.get("alt_texts") or "").strip()
        product.content = (request.form.get("content") or "").strip()
        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for("admin_products"))

    return render_template(
        "admin_form.html",
        title=f"Edit Product: {product.name}",
        subtitle="Update the product/offering and parent relationship.",
        submit_label="Save Product",
        fields=[
            {"name": "service_id", "label": "Parent Service (optional)", "type": "select", "options": [("", "None")] + [(str(item.id), item.name) for item in service_choices]},
            {"name": "sub_service_id", "label": "Parent Subservice (optional)", "type": "select", "options": [("", "None")] + [(str(item.id), item.name) for item in subservice_choices]},
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category_name", "label": "Category Name", "type": "text", "required": True},
            {"name": "description", "label": "Description", "type": "textarea"},
            {"name": "image_url", "label": "Image URL / Path", "type": "text"},
            {"name": "alt_texts", "label": "Alt Text", "type": "text"},
            {"name": "content", "label": "HTML Content", "type": "textarea", "rows": 10},
        ],
        values={
            "service_id": str(product.service_id) if product.service_id else "",
            "sub_service_id": str(product.sub_service_id) if product.sub_service_id else "",
            "name": product.name,
            "category_name": product.category_name,
            "description": product.description,
            "image_url": product.image_url,
            "alt_texts": product.alt_texts,
            "content": product.content,
        },
        back_url=url_for("admin_products"),
        **admin_layout_context("admin-products")
    )


@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def admin_product_delete(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "success")
    return redirect(url_for("admin_products"))


@app.route("/admin/headers")
@admin_required
def admin_headers():
    records = Header.query.order_by(Header.id.desc()).all()
    return render_template(
        "admin_list.html",
        title="Manage Header Links",
        subtitle="Maintain legacy/shared header link records stored in the database.",
        records=records,
        columns=[
            ("ID", lambda item: item.id),
            ("Name", lambda item: item.name),
            ("End URL", lambda item: item.end_url),
        ],
        create_url=url_for("admin_header_create"),
        edit_endpoint="admin_header_edit",
        delete_endpoint="admin_header_delete",
        item_kind="header",
        page_key="admin-headers",
        **admin_layout_context("admin-headers")
    )


@app.route("/admin/headers/new", methods=["GET", "POST"])
@admin_required
def admin_header_create():
    if request.method == "POST":
        header = Header(
            name=(request.form.get("name") or "").strip(),
            end_url=(request.form.get("end_url") or "").strip(),
        )
        db.session.add(header)
        db.session.commit()
        flash("Header link created successfully.", "success")
        return redirect(url_for("admin_headers"))

    return render_template(
        "admin_form.html",
        title="Create Header Link",
        subtitle="Add a database-backed navigation record.",
        submit_label="Create Header Link",
        fields=[
            {"name": "name", "label": "Display Name", "type": "text", "required": True},
            {"name": "end_url", "label": "Endpoint / URL Key", "type": "text", "required": True},
        ],
        values={},
        back_url=url_for("admin_headers"),
        **admin_layout_context("admin-headers")
    )


@app.route("/admin/headers/<int:header_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_header_edit(header_id):
    header = Header.query.get_or_404(header_id)
    if request.method == "POST":
        header.name = (request.form.get("name") or "").strip()
        header.end_url = (request.form.get("end_url") or "").strip()
        db.session.commit()
        flash("Header link updated successfully.", "success")
        return redirect(url_for("admin_headers"))

    return render_template(
        "admin_form.html",
        title=f"Edit Header Link: {header.name}",
        subtitle="Update the database-backed navigation record.",
        submit_label="Save Header Link",
        fields=[
            {"name": "name", "label": "Display Name", "type": "text", "required": True},
            {"name": "end_url", "label": "Endpoint / URL Key", "type": "text", "required": True},
        ],
        values={"name": header.name, "end_url": header.end_url},
        back_url=url_for("admin_headers"),
        **admin_layout_context("admin-headers")
    )


@app.route("/admin/headers/<int:header_id>/delete", methods=["POST"])
@admin_required
def admin_header_delete(header_id):
    header = Header.query.get_or_404(header_id)
    db.session.delete(header)
    db.session.commit()
    flash("Header link deleted successfully.", "success")
    return redirect(url_for("admin_headers"))


@app.route("/admin/database")
@admin_required
def admin_database():
    users = User.query.order_by(User.id.desc()).limit(30).all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).limit(30).all()
    messages = Message.query.order_by(Message.created_at.desc()).limit(30).all()
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(30).all()
    return render_template(
        "admin_database.html",
        users=users,
        contacts=contacts,
        messages=messages,
        transactions=transactions,
        summarize_text=summarize_text,
        **admin_layout_context("admin-database")
    )

@app.route("/api/stats")
@login_required
def stats_api():
    total = Message.query.filter_by(user_id=current_user.id).count()
    delivered = Message.query.filter_by(user_id=current_user.id, status="delivered").count()
    pending = Message.query.filter_by(user_id=current_user.id, status="pending").count()
    failed = Message.query.filter_by(user_id=current_user.id, status="failed").count()

    delivery_rate = (delivered / total * 100) if total > 0 else 0

    # Weekly messages
    today = datetime.now(timezone.utc)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    daily_counts = (
        db.session.query(
            func.extract("dow", Message.created_at).label("day_of_week"),
            func.count(Message.id)
        )
        .filter(
            Message.user_id == current_user.id,
            Message.created_at >= start_of_week,
            Message.created_at <= end_of_week
        )
        .group_by("day_of_week")
        .all()
    )

    messages_chart_data = [0, 0, 0, 0, 0, 0, 0]  # Mon-Sun
    for day, count in daily_counts:
        index = int(day) - 1 if int(day) > 0 else 6  # Sunday -> last
        messages_chart_data[index] = int(count)  # convert to integer

    delivery_status_data = [int(delivered), int(pending), int(failed)]

    return jsonify({
        "messages_sent": total,
        "delivery_rate": round(delivery_rate, 2),
        "pending": pending,
        "failed": failed,
        "delivered": delivered,  # <- add this
        "messages_chart_data": messages_chart_data,
        "delivery_status_data": delivery_status_data
    })

@app.route("/contacts", methods=["GET", "POST"])
@login_required
def contacts():
    # Fetch user's contacts
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    groups = ContactGroup.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        name = request.form.get("name") or None
        phone = request.form.get("phone")
        group_id = request.form.get("group_id") or None

        # Basic phone validation
        if not phone.isdigit() or len(phone) < 10:
            flash("Invalid phone number.", "danger")
            return redirect(url_for("contacts"))

        new_contact = Contact(
            name=name,
            phone=phone,
            user_id=current_user.id,
            group_id=group_id
        )
        db.session.add(new_contact)
        db.session.commit()
        flash(f"Contact {name} added successfully!", "success")
        return redirect(url_for("contacts"))

    return render_template("contact.html", contacts=contacts, groups=groups, bulkk_sms=True)

@app.route("/add_contact/<int:group_id>")
def add_contact(group_id):
    group = ContactGroup.query.get_or_404(group_id)
    return render_template("add_contacts.html", group=group, bulkk_sms=True, group_id=group.id)


@app.route("/create_group", methods=["POST"])
def create_group():
    data = request.get_json()
    group_name = data.get("name", "").strip()

    if not group_name:
        return jsonify({"status": "error", "message": "Group name is required"})
    group_name = group_name.title()
    existing = ContactGroup.query.filter_by(name=group_name).first()
    if existing:
        return jsonify({"status": "error", "message": "Group already exists"})

    # create new group

    new_group = ContactGroup(name=group_name, user=current_user)
    db.session.add(new_group)
    db.session.commit()

    return jsonify({
        "status": "success",
        "redirect": url_for("add_contact", group_id=new_group.id)
    })


# Delete a group
@app.route("/groups/delete/<int:group_id>", methods=["POST"])
@login_required
def delete_group(group_id):
    group = ContactGroup.query.filter_by(id=group_id, user_id=current_user.id).first()
    if not group:
        return jsonify({"status": "error", "message": "Group not found"})

    # Optional: delete all contacts in this group
    for contact in group.contacts:
        db.session.delete(contact)

    db.session.delete(group)
    db.session.commit()
    return jsonify({"status": "success"})


# Delete a contact
@app.route("/contacts/delete/<int:contact_id>", methods=["POST"])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user.id).first()
    if not contact:
        return jsonify({"status": "error", "message": "Contact not found"})

    db.session.delete(contact)
    db.session.commit()
    return jsonify({"status": "success"})


# Edit group name
@app.route("/groups/edit/<int:group_id>", methods=["POST"])
def edit_group(group_id):
    data = request.get_json()
    new_name = data.get("name", "").strip()
    if not new_name:
        return jsonify({"status": "error", "message": "Group name cannot be empty"})

    new_name = new_name.title()
    group = ContactGroup.query.get_or_404(group_id)
    existing = ContactGroup.query.filter(ContactGroup.name == new_name, ContactGroup.id != group_id).first()
    if existing:
        return jsonify({"status": "error", "message": "Group with this name already exists"})

    group.name = new_name
    db.session.commit()
    return jsonify({"status": "success", "message": "Group name updated"})

# Edit contact phone number
@app.route("/contacts/edit/<int:id>", methods=["POST"])
def edit_contact(id):
    try:
        data = request.get_json()
        new_phone = data.get("phone", "").strip()
        group_id = data.get("group_id")

        if not new_phone:
            return jsonify({"status": "error", "message": "Phone number cannot be empty"})

        # 🔹 Ensure phone contains only digits (basic validation)
        if not new_phone.isdigit():
            return jsonify({"status": "error", "message": "Phone number must contain only digits"})

        # 🔹 (Optional) Check length for Nigerian numbers e.g. 11 digits
        if len(new_phone) < 7 or len(new_phone) > 15:
            return jsonify({"status": "error", "message": "Invalid phone number length"})

        if not group_id:
            return jsonify({"status": "error", "message": "Group ID missing"})

        group_id = int(group_id)

        existing = Contact.query.filter_by(group_id=group_id, phone=new_phone).filter(Contact.id != id).first()
        if existing:
            return jsonify({"status": "error", "message": "Phone number already exists in this group"})

        contact = Contact.query.get_or_404(id)
        contact.phone = new_phone
        contact.group_id = group_id
        db.session.commit()

        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})




# === STEP 1: Upload + Preview ===
PHONE_ALIASES = ["phone", "mobile", "number", "contact"]

@app.route("/upload_contacts", methods=["POST"])
@login_required
def upload_contacts():
    try:
        if pd is None:
            return jsonify({
                "status": "error",
                "message": "Spreadsheet import support is unavailable because pandas is not installed."
            }), 500

        file = request.files.get("file")
        group_id = request.form.get("group_id")
        print(group_id)

        if not file or not allowed_file(file.filename):
            return jsonify({"status": "error", "message": "Invalid file format. Please upload a CSV or Excel file."}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Read file
        try:
            if filename.lower().endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            logger.exception("Failed to read uploaded file")
            return jsonify({"status": "error", "message": f"Failed to read file: {str(e)}"}), 400

        # Normalize columns
        normalized_cols = [col.strip().lower() for col in df.columns]

        # Detect phone column
        phone_col = None
        for idx, col in enumerate(normalized_cols):
            for alias in PHONE_ALIASES:
                if alias in col:
                    phone_col = df.columns[idx]  # use original column name
                    break
            if phone_col:
                break

        if not phone_col:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                "status": "error",
                "message": f"Your file must include a phone column. Acceptable aliases: {', '.join(PHONE_ALIASES)}"
            }), 400

        # Save info in session
        session["upload_file"] = filepath
        session["upload_group_id"] = group_id
        session["phone_column"] = phone_col

        preview_html = df.head(5).to_html(classes="table table-bordered table-striped", index=False)
        total_rows = len(df)

        return jsonify({
            "status": "success",
            "preview": preview_html,
            "total_rows": total_rows,
            "columns": list(df.columns),
            "phone_column": phone_col
        })

    except Exception as e:
        logger.exception("Unhandled error in upload_contacts")
        return jsonify({"status": "error", "message": "Server error: " + str(e)}), 500


@app.route("/confirm_upload", methods=["POST"])
@login_required
def confirm_upload():
    try:
        if pd is None:
            return jsonify({
                "status": "error",
                "message": "Spreadsheet import support is unavailable because pandas is not installed."
            }), 500

        filepath = session.get("upload_file")
        group_id = request.json.get("group_id") or session.get("upload_group_id")
        phone_col = session.get("phone_column")


        if not filepath or not os.path.exists(filepath) or not phone_col:
            return jsonify({"status": "error", "message": "No file to confirm. Please upload again."}), 400

        # Read uploaded file
        if filepath.lower().endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        # Normalize uploaded phone numbers (strip, remove spaces, remove dashes)
        df[phone_col] = df[phone_col].astype(str).str.replace(r"\D", "", regex=True).str.strip()
        df = df.drop_duplicates(subset=[phone_col])

        # Get existing phone numbers in DB for this user & group
        existing_q = db.session.query(Contact.phone).filter_by(
            user_id=current_user.id,
            group_id=group_id
        ).all()
        existing_numbers = {str(r[0]).replace("-", "").replace(" ", "").strip() for r in existing_q}

        # Keep only new numbers
        new_rows = df[~df[phone_col].isin(existing_numbers)]
        if new_rows.empty:
            if os.path.exists(filepath):
                os.remove(filepath)
            session.pop("upload_file", None)
            session.pop("upload_group_id", None)
            session.pop("phone_column", None)
            return jsonify({"status": "error", "message": "All numbers already exist in this group."}), 400

        added = 0
        for _, row in new_rows.iterrows():
            phone = str(row[phone_col]).replace("-", "").replace(" ", "").strip()
            if not phone:
                continue
            contact = Contact(user_id=current_user.id, phone=phone, group_id=group_id if group_id else None)
            db.session.add(contact)
            db.session.flush()

            # Save other columns
            for col in new_rows.columns:
                if col != phone_col and not pd.isna(row[col]):
                    variable = Variable(contact_id=contact.id, name=col, content=str(row[col]))
                    db.session.add(variable)
            added += 1

        db.session.commit()

        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)
        session.pop("upload_file", None)
        session.pop("upload_group_id", None)
        session.pop("phone_column", None)

        return jsonify({"status": "success", "message": f"{added} new contacts uploaded successfully! (duplicates skipped)"})

    except Exception as e:
        logger.exception("Unhandled error in confirm_upload")
        return jsonify({"status": "error", "message": "Server error: " + str(e)}), 500

@app.route("/wallet")
@login_required
def wallet():
    # Ensure wallet exists for this user
    if not current_user.wallet:
        new_wallet = Wallet(user=current_user, balance=0)
        db.session.add(new_wallet)
        db.session.commit()

    return render_template("wallet.html", bulkk_sms=True, wallet=current_user.wallet, PAYSTACK_PUBLIC_KEY=PAYSTACK_PUBLIC_KEY)


@app.route("/wallet/fund", methods=["POST"])
@login_required
def fund_wallet():
    amount = float(request.form.get("amount", 0))
    print(amount)
    if amount <= 0:
        flash("Invalid amount", "danger")
        return redirect(url_for("wallet"))

    wallet = current_user.wallet
    wallet.balance += amount

    txn = Transaction(user=current_user, amount=amount, type="credit", wallet=wallet)
    db.session.add(txn)
    db.session.commit()

    flash(f"Wallet funded with ₦{amount:.2f}", "success")
    return redirect(url_for("wallet"))

@app.route("/wallet/verify/<reference>")
@login_required
def verify_payment(reference):
    if requests is None:
        flash("Payment verification is unavailable because the requests package is not installed.", "danger")
        return redirect(url_for("wallet"))

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}

    # Prevent duplicate transactions
    if Transaction.query.filter_by(reference=reference).first():
        flash("This transaction has already been processed.", "info")
        return redirect(url_for("wallet"))

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        resp = r.json()
    except requests.RequestException as e:
        app.logger.error(f"Paystack verification error: {e}")
        flash("Could not verify payment. Try again.", "danger")
        return redirect(url_for("wallet"))

    if resp.get("status") and resp["data"]:
        txn_data = resp["data"]
        txn_status = txn_data.get("status")
        amount = Decimal(txn_data.get("amount", 0)) / Decimal(100)
        wallet = current_user.wallet

        # Determine transaction type for logging
        txn_type = "credit" if txn_status == "success" else "none"

        txn = Transaction(
            user_id=current_user.id,
            wallet_id=wallet.id,
            amount=amount,
            type=txn_type,
            reference=reference,
            status=txn_status
        )
        db.session.add(txn)

        # Only credit wallet if successful
        if txn_status == "success":
            wallet.balance += amount
            flash(f"Wallet funded successfully with ₦{amount:.2f}", "success")
        elif txn_status == "failed":
            flash("Payment failed. Amount not added to wallet.", "danger")
        elif txn_status == "abandoned":
            flash("Payment abandoned. Amount not added to wallet.", "warning")
        else:
            flash(f"Transaction {txn_status}. Amount not added to wallet.", "info")

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Database commit error: {e}")
            flash("Database error occurred. Try again.", "danger")
    else:
        flash("Payment verification failed. Try again.", "danger")

    return redirect(url_for("wallet"))

@app.route("/wallet/transactions")
@login_required
def transactions():
    txns = (Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all())
    return render_template("transactions.html", bulkk_sms=True,  txns=txns)

@app.route("/existing_numbers")
@login_required
def existing_numbers():
    group_id = request.args.get("group_id")

    if not group_id:
        return jsonify({"numbers": []})

    existing_q = db.session.query(Contact.phone).filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).all()

    numbers = [str(r[0]).replace("-", "").replace(" ", "").strip() for r in existing_q]
    return jsonify({"numbers": numbers})



@app.route("/add_contacts_manual", methods=["POST"])
@login_required
def add_contacts_manual():
    try:
        group_id = request.form.get("group_id")
        if not group_id:
            return jsonify({"status": "error", "message": "Group not specified"}), 400

        # Get pasted or manual numbers
        numbers_raw = request.form.get("numbers")  # For paste
        numbers_list = request.form.getlist("phone[]")  # For manual inputs

        all_numbers = []

        # Process pasted numbers if provided
        if numbers_raw:
            # Split by common separators: comma, semicolon, space, newline, or pipe
            split_numbers = re.split(r"[,\s;\n|]+", numbers_raw)
            all_numbers.extend([n.strip() for n in split_numbers if n.strip()])

        # Process manual numbers
        all_numbers.extend([n.strip() for n in numbers_list if n.strip()])

        if not all_numbers:
            return jsonify({"status": "error", "message": "No phone numbers provided"}), 400

        # Remove duplicates in input
        all_numbers = list(set(all_numbers))

        # Validate numbers
        valid_numbers = []
        invalid_numbers = []
        for num in all_numbers:
            if re.fullmatch(r"\+?\d{6,15}", num):
                valid_numbers.append(num)
            else:
                invalid_numbers.append(num)

        if not valid_numbers:
            return jsonify({"status": "error", "message": "No valid phone numbers found"}), 400

        # Existing numbers in this group
        existing_q = db.session.query(Contact.phone).filter_by(
            user_id=current_user.id, group_id=group_id
        ).all()
        existing_numbers = {str(r[0]).strip() for r in existing_q}

        # Only keep new numbers
        new_numbers = [n for n in valid_numbers if n not in existing_numbers]

        if not new_numbers:
            msg = "All numbers already exist in this group."
            if invalid_numbers:
                msg += f" Invalid numbers skipped: {', '.join(invalid_numbers)}"
            return jsonify({"status": "error", "message": msg}), 400

        # Add new contacts
        added = 0
        for phone in new_numbers:
            contact = Contact(user_id=current_user.id, phone=phone, group_id=group_id)
            db.session.add(contact)
            added += 1

        db.session.commit()

        msg = f"{added} new contacts added successfully!"
        if invalid_numbers:
            msg += f" Invalid numbers skipped: {', '.join(invalid_numbers)}"

        return jsonify({"status": "success", "message": msg})

    except Exception as e:
        logger.exception("Error adding manual/pasted contacts")
        return jsonify({"status": "error", "message": "Server error: " + str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
