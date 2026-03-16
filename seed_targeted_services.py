from main import app
from db import db, Services, SubService, Products


TARGETED_SERVICES = [
    {
        "name": "Machine Sales & Consumables",
        "category_name": "machine-sales-consumables",
        "description": "Sales and supply support for ID card machines, printing equipment, and essential consumables.",
        "image_url": "about_us_machinery.jpeg",
        "icon_name": "#cil-layers",
        "alt_texts": "Machine sales and consumables support",
        "content": """
<h2>Machine Sales & Consumables</h2>
<p>
  Gregbuk supports institutions and businesses with practical machine sourcing, setup guidance,
  and dependable consumables continuity for daily operations.
</p>
<p>
  This category focuses on equipment readiness, replacement planning, and sustained output quality.
</p>
""",
        "subservices": [
            {
                "name": "ID Card Machines",
                "category_name": "id-card-machines",
                "description": "ID card printer selection, deployment guidance, and setup support.",
                "image_url": "business-card.jpg",
                "alt_texts": "ID card machine setup",
                "products": [
                    {
                        "name": "Desktop ID Card Printer Setup",
                        "category_name": "desktop-id-card-printer-setup",
                        "description": "Selection and setup support for compact desktop ID card printer systems.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "Desktop ID card printer setup",
                    },
                    {
                        "name": "Retransfer ID Printer Deployment",
                        "category_name": "retransfer-id-printer-deployment",
                        "description": "Deployment guidance for high-quality retransfer ID card printing environments.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "Retransfer ID printer deployment",
                    },
                ],
            },
            {
                "name": "Printing Equipment & Accessories",
                "category_name": "printing-equipment-accessories",
                "description": "Operational equipment and accessories for structured print and finishing workflows.",
                "image_url": "printing-press-about.jpg",
                "alt_texts": "Printing equipment and accessories",
                "products": [
                    {
                        "name": "Laminator Systems",
                        "category_name": "laminator-systems",
                        "description": "Durable lamination systems for secure and long-lasting card/document protection.",
                        "image_url": "printing-press-about.jpg",
                        "alt_texts": "Laminator systems",
                    },
                    {
                        "name": "Cutting & Finishing Equipment",
                        "category_name": "cutting-finishing-equipment",
                        "description": "Precision cutting and finishing equipment for clean and consistent output.",
                        "image_url": "printing-press-about.jpg",
                        "alt_texts": "Cutting and finishing equipment",
                    },
                ],
            },
            {
                "name": "Consumables Supply",
                "category_name": "consumables-supply",
                "description": "Reliable recurring supply of ribbons, PVC cards, cleaning kits, and related consumables.",
                "image_url": "marketing-essentials.jpeg",
                "alt_texts": "Consumables and accessories supply",
                "products": [
                    {
                        "name": "PVC Cards & Ribbons Supply",
                        "category_name": "pvc-cards-ribbons-supply",
                        "description": "Scheduled and one-off supply support for PVC cards and compatible print ribbons.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "PVC cards and ribbons supply",
                    },
                    {
                        "name": "Cleaning Kits & Spare Parts",
                        "category_name": "cleaning-kits-spare-parts",
                        "description": "Maintenance kits and select spare parts to keep machines running smoothly.",
                        "image_url": "about_us_machinery.jpeg",
                        "alt_texts": "Cleaning kits and spare parts",
                    },
                ],
            },
        ],
    },
    {
        "name": "Pharmaceutical Distribution",
        "category_name": "pharmaceutical-distribution",
        "description": "Inquiry-led pharmaceutical distribution support for institutions and project-based supply needs.",
        "image_url": "marketing-essentials.jpeg",
        "icon_name": "#cil-medical-cross",
        "alt_texts": "Pharmaceutical distribution support",
        "content": """
<h2>Pharmaceutical Distribution</h2>
<p>
  Gregbuk provides inquiry-based pharmaceutical distribution support for organizations that require
  dependable coordination, clear process handling, and responsible supply planning.
</p>
<p>
  Engagements are structured by scope, documentation needs, and delivery timelines.
</p>
""",
        "subservices": [
            {
                "name": "Institutional Pharma Supply",
                "category_name": "institutional-pharma-supply",
                "description": "Supply coordination for hospitals, clinics, schools, and institutional operations.",
                "image_url": "marketing-essentials.jpeg",
                "alt_texts": "Institutional pharmaceutical supply",
                "products": [
                    {
                        "name": "Bulk Supply Coordination",
                        "category_name": "bulk-supply-coordination",
                        "description": "Planning and coordinated delivery support for institution-level supply requests.",
                        "image_url": "marketing-essentials.jpeg",
                        "alt_texts": "Bulk supply coordination",
                    },
                    {
                        "name": "Scheduled Restock Program",
                        "category_name": "scheduled-restock-program",
                        "description": "Recurring restock support based on agreed inventory and service intervals.",
                        "image_url": "marketing-essentials.jpeg",
                        "alt_texts": "Scheduled restock program",
                    },
                ],
            },
            {
                "name": "Pharma Compliance & Documentation",
                "category_name": "pharma-compliance-documentation",
                "description": "Documentation and process support for compliant pharmaceutical distribution workflows.",
                "image_url": "signs&banners.jpeg",
                "alt_texts": "Pharmaceutical documentation support",
                "products": [
                    {
                        "name": "Product Documentation Review",
                        "category_name": "product-documentation-review",
                        "description": "Review support for required paperwork and procurement-aligned documentation.",
                        "image_url": "signs&banners.jpeg",
                        "alt_texts": "Product documentation review",
                    },
                    {
                        "name": "Regulatory Submission Guidance",
                        "category_name": "regulatory-submission-guidance",
                        "description": "Advisory guidance for preparing submissions and process-ready records.",
                        "image_url": "signs&banners.jpeg",
                        "alt_texts": "Regulatory submission guidance",
                    },
                ],
            },
        ],
    },
]


def get_or_create_service(payload):
    service = Services.query.filter_by(name=payload["name"]).first()
    created = False
    if not service:
        service = Services(
            name=payload["name"],
            category_name=payload["category_name"],
            description=payload["description"],
            image_url=payload["image_url"],
            icon_name=payload["icon_name"],
            alt_texts=payload["alt_texts"],
            content=payload["content"],
        )
        db.session.add(service)
        db.session.flush()
        created = True
    return service, created


def get_or_create_subservice(service, payload):
    sub = SubService.query.filter_by(name=payload["name"]).first()
    created = False
    if not sub:
        sub = SubService(
            name=payload["name"],
            category_name=payload["category_name"],
            description=payload["description"],
            image_url=payload["image_url"],
            alt_texts=payload["alt_texts"],
            services=service,
        )
        db.session.add(sub)
        db.session.flush()
        created = True
    return sub, created


def get_or_create_product(service, subservice, payload):
    product = Products.query.filter_by(name=payload["name"]).first()
    created = False
    if not product:
        product = Products(
            name=payload["name"],
            category_name=payload["category_name"],
            description=payload["description"],
            image_url=payload["image_url"],
            alt_texts=payload["alt_texts"],
            services=service if subservice is None else None,
            subservice=subservice,
        )
        db.session.add(product)
        created = True
    return created


def seed_targeted_services():
    created_counts = {"services": 0, "subservices": 0, "products": 0}
    for service_payload in TARGETED_SERVICES:
        service, service_created = get_or_create_service(service_payload)
        if service_created:
            created_counts["services"] += 1

        for sub_payload in service_payload.get("subservices", []):
            sub, sub_created = get_or_create_subservice(service, sub_payload)
            if sub_created:
                created_counts["subservices"] += 1

            for prod_payload in sub_payload.get("products", []):
                if get_or_create_product(service, sub, prod_payload):
                    created_counts["products"] += 1

    db.session.commit()
    return created_counts


if __name__ == "__main__":
    with app.app_context():
        counts = seed_targeted_services()
        print(
            f"Inserted -> services: {counts['services']}, "
            f"subservices: {counts['subservices']}, "
            f"products: {counts['products']}"
        )
