from flask import Flask, render_template, send_from_directory, Blueprint, request,url_for, jsonify, redirect, flash, session
from config import Config
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, func, inspect
from db import db, Services, Products, Variable, SubService, Transaction, Wallet, Header, User, Message, Contact, ContactGroup, ContactTransact, ProductCollection
from random import randint, choice
from form import ContactForm
import os, traceback, logging
from datetime import datetime, timedelta, timezone
import smtplib
from email.message import EmailMessage
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
import csv, io
import openpyxl
from decimal import Decimal
import requests
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import re
import pandas as pd



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "hellodear"
    db.init_app(app)
    with app.app_context():
        db.create_all()  # creates tables

    return app

app = create_app()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
logger = logging.getLogger(__name__)

PAYSTACK_PUBLIC_KEY = "pk_test_10d987b1938d5cfbdc8479fea0238bb7db38e015"
PAYSTACK_SECRET_KEY = "sk_test_adc0139baf8d91f8480325b309a6769c2c9e5c17"
UPLOAD_FOLDER = "uploads"
ALLOWED = {"csv", "xlsx"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # ensure folder exists

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
@app.template_global()
def date():
    now = datetime.now()
    year = now.year
    return year

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
    return render_template("printing.html")

@app.route("/business-reg")
def business_registration():
    header = Header.query.all()
    service = Services.query.all()
    return render_template("main.html", header=header, services=service)


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
                print("hello")
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
    change=False
    rows = [service[n:n+2] for n in range(0, len(service), 2)]
    random_service = [choice(service), choice(service)]
    return render_template(f"{templates}", the_data=the_data, random_service=random_service, rows=rows, change=change, header=header, services=service, the_name=the_name)

@app.route("/all_services")
def all():
    the_name = "var"
    header = Header.query.all()
    service = Services.query.all()
    change=False
    rows = [service[n:n+2] for n in range(0, len(service), 2)]
    random_service = [choice(service), choice(service)]
    return render_template('all_services.html', random_service=random_service, rows=rows, change=change, header=header, services=service, the_name=the_name)


@app.route("/bulk-sms")
@login_required
def bulk_sms():
    the_name = 'var'
    return render_template("dashboard.html", the_name=the_name, bulkk_sms=True)

@app.route("/about-us")
def about_us():
    header = Header.query.all()
    service = Services.query.all()
    change = True
    return render_template("about_us.html", change=change, header=header, services=service)

@app.route("/princing")
def pricing():
    header = Header.query.all()
    service = Services.query.all()
    return render_template("main.html", header=header, services=service)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    print("hello")
    head = request.args.get("head")
    header = Header.query.all()
    service = Services.query.all()
    change= True
    form=ContactForm()
    choices = [("select", "Select from the dropdown")]
    choices2 = [(serve.category_name, serve.name) for serve in service]
    manual = [("price", "Price")]
    choices.extend(choices2)
    choices.extend(manual)
    form.head.choices = choices
    if head != "":
        if Services.query.filter_by(category_name=head).first():
            data = Services.query.filter_by(category_name=head).first()
            form.head.data = data.category_name
    if request.method == "POST":
        if form.validate_on_submit():
            the_head = form.head.data
            the_name = form.name.data
            the_email = form.email.data
            the_phone = form.phone.data
            the_message = form.phone.data
            smtp_server = "smtp.gmail.com"
            port = 587
            sender_mail = "ifeanyiagada9@gmail.com"
            receiver = "ifeanyiagada123@gmail.com"
            password = os.environ.get("PASSWORD_TEXT")
            message = EmailMessage()
            message["From"] = sender_mail
            message["To"] = receiver
            message["Subject"] = "Contact Message from Blog Website"
            message.set_content(
                f"Header: {the_head}\n\n"
                f"Name: {the_name}\n\n"
                f"Email: {the_email}\n\n"
                f"Phone Number: {the_phone}\n\n"
                f"Message: {the_message}"
            )
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender_mail, password)
                server.send_message(message)

            return jsonify({"success": True})
        else:
            errors = {field: errors for field, errors in form.errors.items()}
            return jsonify({"success": False, "errors": errors})

    return render_template("contact_us.html", form=form, change=change, header=header, services=service)

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

    delivery_rate = (delivered / total * 100) if total > 0 else 0

    return render_template("dashboard.html", the_name=the_name, delivery_rate=delivery_rate, total=total, delivered=delivered, pending=pending, failed=failed, bulkk_sms=True, show_welcome_toast=show_welcome_toast)

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