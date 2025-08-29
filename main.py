from flask import Flask, render_template, request,url_for, jsonify
from config import Config
from sqlalchemy import or_
from db import db, Services, Products, SubService, Header
from random import randint, choice



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # creates tables

    return app

app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
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
    theme = request.cookies.get("theme", "auto")
    random_service1 = Services.query.filter_by(name="Marketing Essentials").first()
    random_sub1 = choice(random_service1.sub_service)
    random_product1 = choice(random_sub1.products)
    random_service2 = Services.query.filter_by(name="Business Cards").first()
    random_product2 = choice(random_service2.products)
    change = True
    return render_template("main.html", change=change, random_sub1=random_sub1, random_product2=random_product2, random_product1=random_product1, header=header, services=service, theme=theme)

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
    if name and sec and pro:
        the_name = name
        templates = "main.html"
    elif name and sec:
        if SubService.query.filter_by(category_name=sec).first():
            the_name = name
            templates = "main.html"
        else:
            the_name = name
            templates = "main.html"
    elif name:
        the_name = name
        templates = "service.html"
        data = Services.query.filter_by(category_name=the_name).first()

    the_data = data
    print(the_data)
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
def bulk_sms():
    header = Header.query.all()
    service = Services.query.all()
    return render_template("main.html", header=header, services=service)

@app.route("/about-us")
def about_us():
    header = Header.query.all()
    service = Services.query.all()
    return render_template("main.html", header=header, services=service)

@app.route("/princing")
def pricing():
    header = Header.query.all()
    service = Services.query.all()
    return render_template("main.html", header=header, services=service)

@app.route("/contact")
def contact():
    header = Header.query.all()
    service = Services.query.all()
    change= True
    return render_template("contact_us.html", change=change, header=header, services=service)

@app.route("/logout")
def logout():
    return render_template("main.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    header = Header.query.all()
    service = Services.query.all()
    change = True
    return render_template("register.html", change=change, header=header, services=service)

@app.route("/login", methods=["GET", "POST"])
def login():
    header = Header.query.all()
    service = Services.query.all()
    change = True
    return render_template("login.html", change=change, header=header, services=service)

@app.route("/dashboard")
def dashboard():
    header = Header.query.all()
    service = Services.query.all()
    return render_template("main.html", header=header, services=service)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)