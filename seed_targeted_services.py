from main import app
from db import db, Services, SubService, Products, ProductCollection
from sqlalchemy import or_


def html_block(title, intro, bullets, outro):
    bullet_markup = "".join(f"<li>{item}</li>" for item in bullets)
    return f"""
<h2>{title}</h2>
<p>{intro}</p>
<ul>
  {bullet_markup}
</ul>
<p>{outro}</p>
""".strip()


def default_subservice_content(service_name, subservice_name, description):
    return html_block(
        subservice_name,
        f"{subservice_name} sits under Gregbuk's {service_name} division and is designed for clients that need structured, practical support.",
        [
            description,
            "Inquiry-led support matched to organization needs",
            "Clearer delivery structure and next-step guidance",
        ],
        "This area can be expanded later with more specific workflow details, case examples, or service requirements.",
    )


MACHINE_GALLERY = [
    "about_us_machinery.jpeg",
    "id_cards.jpeg",
    "print_about_us.webp",
    "placeholders/id-machine.svg",
]

PHARMA_GALLERY = [
    "print_about_us.webp",
    "placeholders/pharmaceutical-distribution.svg",
    "placeholders/operations.svg",
    "marketing-essentials.jpeg",
]

ENGINEERING_GALLERY = [
    "placeholders/engineering-consultancy.svg",
    "print_about_us.webp",
    "placeholders/operations.svg",
    "printing-press-about.jpg",
]

TRAVEL_GALLERY = [
    "placeholders/travel-agency.svg",
    "placeholders/office-building.svg",
    "print_about_us.webp",
    "placeholders/operations.svg",
]

SUPPORT_GALLERY = [
    "placeholders/operations.svg",
    "placeholders/office-building.svg",
    "print_about_us.webp",
    "marketing-essentials.jpeg",
]

CONTRACT_GALLERY = [
    "print_about_us.webp",
    "placeholders/operations.svg",
    "printing-press-about.jpg",
    "placeholders/office-building.svg",
]


TARGETED_SERVICES = [
    {
        "name": "General Contracts",
        "category_name": "general-contracts",
        "description": "Structured project support, operational fulfillment, and contract execution coordination for institutions and business operations.",
        "image_url": "placeholders/operations.svg",
        "icon_name": "#cil-briefcase",
        "alt_texts": "General contracts and project execution support",
        "content": html_block(
            "General Contracts",
            "Gregbuk supports clients with practical contract execution, sourcing coordination, and delivery oversight across business and institutional projects.",
            [
                "Project support structured around timelines and operational realities",
                "Execution coordination for supplies, installations, and support services",
                "Clear communication from scope review to delivery follow-through",
            ],
            "This service branch works best for organizations that want a dependable partner to coordinate and execute multi-step deliverables.",
        ),
        "subservices": [
            {
                "name": "Project Support Services",
                "category_name": "project-support-services",
                "description": "Hands-on support for scoped assignments, project coordination, and delivery planning.",
                "image_url": "placeholders/operations.svg",
                "alt_texts": "Project support services",
                "content": html_block(
                    "Project Support Services",
                    "We help clients plan and execute operational assignments with a practical, delivery-focused structure.",
                    [
                        "Scope review and delivery planning",
                        "Assignment coordination across teams and suppliers",
                        "Follow-through support to keep work moving",
                    ],
                    "This is suitable for institutions and businesses that need reliable project execution support without unnecessary complexity.",
                ),
                "products": [
                    {
                        "name": "Procurement Coordination Support",
                        "category_name": "procurement-coordination-support",
                        "description": "Coordination support for sourcing, vendor alignment, and delivery readiness.",
                        "image_url": "placeholders/operations.svg",
                        "alt_texts": "Procurement coordination support",
                        "content": html_block(
                            "Procurement Coordination Support",
                            "Gregbuk helps organizations coordinate supply requirements and delivery planning under one support flow.",
                            [
                                "Requirement review and procurement alignment",
                                "Vendor follow-up and delivery coordination",
                                "Support for practical execution timelines",
                            ],
                            "This offering is ideal where purchasing needs to connect smoothly with operational delivery.",
                        ),
                        "image_collection": CONTRACT_GALLERY,
                    },
                    {
                        "name": "Delivery Supervision Support",
                        "category_name": "delivery-supervision-support",
                        "description": "Oversight support for coordinated project delivery and execution follow-up.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Delivery supervision support",
                        "content": html_block(
                            "Delivery Supervision Support",
                            "We help keep project deliverables organized through communication, follow-up, and execution monitoring.",
                            [
                                "Delivery milestone monitoring",
                                "Issue escalation and progress follow-up",
                                "Support for orderly execution across stakeholders",
                            ],
                            "This is useful for clients that want stronger oversight across moving project parts.",
                        ),
                        "image_collection": CONTRACT_GALLERY,
                    },
                ],
            },
            {
                "name": "Operational Fulfillment",
                "category_name": "operational-fulfillment",
                "description": "Service support for recurring business needs, supply execution, and operational continuity.",
                "image_url": "placeholders/office-building.svg",
                "alt_texts": "Operational fulfillment support",
                "products": [
                    {
                        "name": "Supply Fulfillment Planning",
                        "category_name": "supply-fulfillment-planning",
                        "description": "Support for organizing supply flows and routine fulfillment requirements.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Supply fulfillment planning",
                        "content": html_block(
                            "Supply Fulfillment Planning",
                            "We help map recurring needs into a clearer, more manageable fulfillment workflow.",
                            [
                                "Routine supply planning support",
                                "Operational requirement alignment",
                                "Practical delivery coordination",
                            ],
                            "This helps organizations reduce delays and keep operational needs better organized.",
                        ),
                        "image_collection": CONTRACT_GALLERY,
                    },
                    {
                        "name": "Institution Delivery Coordination",
                        "category_name": "institution-delivery-coordination",
                        "description": "Delivery coordination support for schools, offices, healthcare teams, and institutions.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Institution delivery coordination",
                        "content": html_block(
                            "Institution Delivery Coordination",
                            "Gregbuk provides coordination support for institutional delivery needs where structure and responsiveness matter.",
                            [
                                "Coordination across multiple delivery points",
                                "Support for documentation and follow-up",
                                "Service continuity across recurring needs",
                            ],
                            "This is designed for clients that need a steadier operational support partner.",
                        ),
                        "image_collection": CONTRACT_GALLERY,
                    },
                ],
            },
        ],
    },
    {
        "name": "Machine Sales & Consumables",
        "category_name": "machine-sales-consumables",
        "description": "Sales and supply support for ID card machines, printing equipment, and essential consumables.",
        "image_url": "about_us_machinery.jpeg",
        "icon_name": "#cil-layers",
        "alt_texts": "Machine sales and consumables support",
        "content": html_block(
            "Machine Sales & Consumables",
            "Gregbuk supports institutions and businesses with practical machine sourcing, setup guidance, and dependable consumables continuity for daily operations.",
            [
                "Machine recommendations matched to volume and use case",
                "Accessories and maintenance support for smoother operations",
                "Consumables planning for continuity and reduced downtime",
            ],
            "This category focuses on equipment readiness, replacement planning, and sustained output quality.",
        ),
        "subservices": [
            {
                "name": "ID Card Machines",
                "category_name": "id-card-machines",
                "description": "ID card printer selection, deployment guidance, and setup support.",
                "image_url": "placeholders/id-machine.svg",
                "alt_texts": "ID card machine setup",
                "products": [
                    {
                        "name": "Desktop ID Card Printer Setup",
                        "category_name": "desktop-id-card-printer-setup",
                        "description": "Selection and setup support for compact desktop ID card printer systems.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "Desktop ID card printer setup",
                        "content": html_block(
                            "Desktop ID Card Printer Setup",
                            "This option supports organizations that need a practical in-house card printing setup for routine identity production.",
                            [
                                "Guidance on suitable entry-level and mid-range printers",
                                "Workflow support for routine card issuance",
                                "Recommendations for compatible consumables and accessories",
                            ],
                            "It is a strong fit for schools, SMEs, hospitals, and offices with regular card issuance needs.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Retransfer ID Printer Deployment",
                        "category_name": "retransfer-id-printer-deployment",
                        "description": "Deployment guidance for high-quality retransfer ID card printing environments.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "Retransfer ID printer deployment",
                        "content": html_block(
                            "Retransfer ID Printer Deployment",
                            "Retransfer systems are suited to organizations that need stronger card finish quality, edge-to-edge output, and more secure card production.",
                            [
                                "Support for premium printer deployment planning",
                                "Consumables and card stock guidance",
                                "Setup support for higher-quality issuance environments",
                            ],
                            "This is especially useful for organizations prioritizing card quality, durability, and cleaner output.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Dual-Sided Printer Configuration",
                        "category_name": "dual-sided-printer-configuration",
                        "description": "Configuration support for organizations that need front-and-back card production workflows.",
                        "image_url": "about_us_machinery.jpeg",
                        "alt_texts": "Dual-sided printer configuration",
                        "content": html_block(
                            "Dual-Sided Printer Configuration",
                            "We help clients structure card systems that require both front and reverse-side printing for identity, compliance, or branding needs.",
                            [
                                "Guidance for dual-sided print workflows",
                                "Output planning for branded and information-rich cards",
                                "Practical setup recommendations for recurring production",
                            ],
                            "This option works well where cards carry access, instructional, or institutional information on both sides.",
                        ),
                        "image_collection": MACHINE_GALLERY,
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
                        "description": "Durable lamination systems for secure and long-lasting card or document protection.",
                        "image_url": "printing-press-about.jpg",
                        "alt_texts": "Laminator systems",
                        "content": html_block(
                            "Laminator Systems",
                            "Lamination equipment helps improve durability, finish quality, and longer-term handling performance for printed materials.",
                            [
                                "Support for selecting suitable lamination systems",
                                "Recommended use cases for cards and documents",
                                "Accessory planning for smoother output workflow",
                            ],
                            "This offering is useful where protection, finish, and presentation quality matter.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Cutting & Finishing Equipment",
                        "category_name": "cutting-finishing-equipment",
                        "description": "Precision cutting and finishing equipment for clean and consistent output.",
                        "image_url": "printing-press-about.jpg",
                        "alt_texts": "Cutting and finishing equipment",
                        "content": html_block(
                            "Cutting & Finishing Equipment",
                            "Gregbuk supports clients that need cleaner finishing, trimming accuracy, and more efficient post-print handling.",
                            [
                                "Cutting and finishing workflow guidance",
                                "Support for cleaner and more consistent output",
                                "Recommendations matched to production scale",
                            ],
                            "It helps improve presentation quality and reduce waste across repeat jobs.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Embossing & Personalization Tools",
                        "category_name": "embossing-personalization-tools",
                        "description": "Equipment support for personalization, embossing, and advanced card finishing needs.",
                        "image_url": "about_us_machinery.jpeg",
                        "alt_texts": "Embossing and personalization tools",
                        "content": html_block(
                            "Embossing & Personalization Tools",
                            "Where card output needs a more specialized finish, this support area helps clients identify practical personalization tools.",
                            [
                                "Guidance for advanced finishing workflows",
                                "Support for specialized output environments",
                                "Accessory matching for smoother operation",
                            ],
                            "This is suited to organizations that need more than standard output capability.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                ],
            },
            {
                "name": "Consumables Supply",
                "category_name": "consumables-supply",
                "description": "Reliable recurring supply of ribbons, PVC cards, cleaning kits, and related consumables.",
                "image_url": "id_cards.jpeg",
                "alt_texts": "Consumables and accessories supply",
                "products": [
                    {
                        "name": "PVC Cards & Ribbons Supply",
                        "category_name": "pvc-cards-ribbons-supply",
                        "description": "Scheduled and one-off supply support for PVC cards and compatible print ribbons.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "PVC cards and ribbons supply",
                        "content": html_block(
                            "PVC Cards & Ribbons Supply",
                            "We support recurring and one-time supply needs for identity card production environments.",
                            [
                                "Supply continuity for routine production",
                                "Guidance on compatible ribbon and card combinations",
                                "Support for reducing downtime caused by stock gaps",
                            ],
                            "This is ideal for organizations with an ongoing card issuance workflow.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Cleaning Kits & Spare Parts",
                        "category_name": "cleaning-kits-spare-parts",
                        "description": "Maintenance kits and select spare parts to keep machines running smoothly.",
                        "image_url": "about_us_machinery.jpeg",
                        "alt_texts": "Cleaning kits and spare parts",
                        "content": html_block(
                            "Cleaning Kits & Spare Parts",
                            "Routine maintenance support helps protect print quality and extend machine usefulness over time.",
                            [
                                "Cleaning kit guidance for ongoing maintenance",
                                "Support for select replacement components",
                                "Practical recommendations for machine care",
                            ],
                            "This helps teams avoid avoidable downtime and maintain consistent output quality.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Lanyards, Holders & Accessories",
                        "category_name": "lanyards-holders-accessories",
                        "description": "Support for badge accessories and practical identity-card usage materials.",
                        "image_url": "id_cards.jpeg",
                        "alt_texts": "Lanyards holders and accessories",
                        "content": html_block(
                            "Lanyards, Holders & Accessories",
                            "Identity systems often need more than cards alone, so this support line covers practical accessories that complete issuance workflows.",
                            [
                                "Card holder and lanyard supply support",
                                "Accessory matching for schools and institutions",
                                "Practical additions for daily identity usage",
                            ],
                            "This is useful when clients want a more complete and usable ID deployment package.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                ],
            },
            {
                "name": "Maintenance & Support",
                "category_name": "maintenance-support",
                "description": "Operational support for machine upkeep, troubleshooting guidance, and continuity planning.",
                "image_url": "placeholders/id-machine.svg",
                "alt_texts": "Machine maintenance and support",
                "products": [
                    {
                        "name": "Preventive Maintenance Planning",
                        "category_name": "preventive-maintenance-planning",
                        "description": "Maintenance planning support for keeping card and print equipment operational.",
                        "image_url": "about_us_machinery.jpeg",
                        "alt_texts": "Preventive maintenance planning",
                        "content": html_block(
                            "Preventive Maintenance Planning",
                            "We help organizations think ahead about maintenance so equipment stays reliable for ongoing operations.",
                            [
                                "Routine maintenance planning guidance",
                                "Support for continuity-minded machine care",
                                "Practical recommendations for recurring upkeep",
                            ],
                            "This is helpful where machine uptime directly affects service delivery.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                    {
                        "name": "Operator Guidance & Support",
                        "category_name": "operator-guidance-support",
                        "description": "Support for teams that need clearer handling, use-case, and workflow guidance around equipment.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Operator guidance and support",
                        "content": html_block(
                            "Operator Guidance & Support",
                            "Machine performance depends on confident day-to-day handling, so this support line focuses on practical operational guidance.",
                            [
                                "Workflow support for machine users",
                                "Use-case guidance for smoother operations",
                                "Support for more consistent handling and output",
                            ],
                            "This is especially useful for organizations onboarding new equipment into routine operations.",
                        ),
                        "image_collection": MACHINE_GALLERY,
                    },
                ],
            },
        ],
    },
    {
        "name": "Pharmaceutical Distribution",
        "category_name": "pharmaceutical-distribution",
        "description": "Inquiry-led pharmaceutical distribution support for institutions and project-based supply needs.",
        "image_url": "placeholders/pharmaceutical-distribution.svg",
        "icon_name": "#cil-medical-cross",
        "alt_texts": "Pharmaceutical distribution support",
        "content": html_block(
            "Pharmaceutical Distribution",
            "Gregbuk provides inquiry-based pharmaceutical distribution support for organizations that require dependable coordination, clear process handling, and responsible supply planning.",
            [
                "Institution-focused distribution support",
                "Delivery planning for recurring and project-based needs",
                "Documentation-aware handling for smoother workflows",
            ],
            "Engagements are structured by scope, documentation needs, and delivery timelines.",
        ),
        "subservices": [
            {
                "name": "Institutional Pharma Supply",
                "category_name": "institutional-pharma-supply",
                "description": "Supply coordination for hospitals, clinics, schools, and institutional operations.",
                "image_url": "placeholders/pharmaceutical-distribution.svg",
                "alt_texts": "Institutional pharmaceutical supply",
                "products": [
                    {
                        "name": "Bulk Supply Coordination",
                        "category_name": "bulk-supply-coordination",
                        "description": "Planning and coordinated delivery support for institution-level supply requests.",
                        "image_url": "placeholders/pharmaceutical-distribution.svg",
                        "alt_texts": "Bulk supply coordination",
                        "content": html_block(
                            "Bulk Supply Coordination",
                            "This offering is designed for facilities and organizations that need a coordinated supply approach rather than ad hoc ordering.",
                            [
                                "Scope review for larger-volume supply needs",
                                "Coordination support for scheduled deliveries",
                                "Clearer alignment between request, documentation, and fulfillment",
                            ],
                            "It is useful for operations that depend on steadier and more predictable supply handling.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                    {
                        "name": "Scheduled Restock Program",
                        "category_name": "scheduled-restock-program",
                        "description": "Recurring restock support based on agreed inventory and service intervals.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Scheduled restock program",
                        "content": html_block(
                            "Scheduled Restock Program",
                            "Where continuity matters, Gregbuk helps clients structure recurring restock planning around operational needs.",
                            [
                                "Restock planning support for recurring needs",
                                "Operational continuity through scheduled replenishment",
                                "Support for reduced supply disruption",
                            ],
                            "This works well for organizations that prefer a steadier restock rhythm.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                    {
                        "name": "Facility Supply Request Support",
                        "category_name": "facility-supply-request-support",
                        "description": "Support for compiling and coordinating supply requests for healthcare or institutional facilities.",
                        "image_url": "marketing-essentials.jpeg",
                        "alt_texts": "Facility supply request support",
                        "content": html_block(
                            "Facility Supply Request Support",
                            "We support organizations that need a clearer path for requesting, coordinating, and tracking supply requirements.",
                            [
                                "Support for organizing supply requests",
                                "Practical coordination around facility needs",
                                "Alignment between request details and delivery planning",
                            ],
                            "This is useful when supply needs involve multiple line items or operational stakeholders.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                ],
            },
            {
                "name": "Distribution Planning & Logistics",
                "category_name": "distribution-planning-logistics",
                "description": "Planning support for delivery sequencing, distribution coordination, and multi-location supply execution.",
                "image_url": "placeholders/operations.svg",
                "alt_texts": "Distribution planning and logistics",
                "products": [
                    {
                        "name": "Multi-Location Delivery Planning",
                        "category_name": "multi-location-delivery-planning",
                        "description": "Support for coordinating supply movement across multiple sites or teams.",
                        "image_url": "placeholders/operations.svg",
                        "alt_texts": "Multi location delivery planning",
                        "content": html_block(
                            "Multi-Location Delivery Planning",
                            "Some requests require more organized sequencing and follow-up, especially when multiple locations are involved.",
                            [
                                "Support for multi-point distribution planning",
                                "Coordination around delivery scheduling",
                                "Structured handling for broader supply movement",
                            ],
                            "This offering helps reduce confusion where logistics extend beyond a single destination.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                    {
                        "name": "Priority Supply Scheduling",
                        "category_name": "priority-supply-scheduling",
                        "description": "Scheduling support for urgent or time-sensitive supply coordination.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Priority supply scheduling",
                        "content": html_block(
                            "Priority Supply Scheduling",
                            "Where supply timing is important, this support area helps clients frame and coordinate more urgent distribution needs.",
                            [
                                "Support for time-sensitive request handling",
                                "Scheduling coordination for higher-priority deliveries",
                                "Clearer communication around timing expectations",
                            ],
                            "This is especially useful where operational delays carry higher risk.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                ],
            },
            {
                "name": "Pharma Compliance & Documentation",
                "category_name": "pharma-compliance-documentation",
                "description": "Documentation and process support for compliant pharmaceutical distribution workflows.",
                "image_url": "placeholders/office-building.svg",
                "alt_texts": "Pharmaceutical documentation support",
                "products": [
                    {
                        "name": "Product Documentation Review",
                        "category_name": "product-documentation-review",
                        "description": "Review support for required paperwork and procurement-aligned documentation.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Product documentation review",
                        "content": html_block(
                            "Product Documentation Review",
                            "This support area helps clients organize the paperwork and review process tied to supply requests and distribution workflows.",
                            [
                                "Documentation review support",
                                "Procurement-aligned paperwork guidance",
                                "Clearer handling of request records and supporting details",
                            ],
                            "It supports a smoother process where documentation quality affects progress.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                    {
                        "name": "Regulatory Submission Guidance",
                        "category_name": "regulatory-submission-guidance",
                        "description": "Advisory guidance for preparing submissions and process-ready records.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Regulatory submission guidance",
                        "content": html_block(
                            "Regulatory Submission Guidance",
                            "Gregbuk provides practical guidance for structuring required records and preparing the supporting information around regulated workflows.",
                            [
                                "Guidance on submission preparation",
                                "Support for process-ready records",
                                "More orderly handling of compliance-related documentation",
                            ],
                            "This helps clients approach regulated processes with better structure and clarity.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                    {
                        "name": "Procurement Documentation Support",
                        "category_name": "procurement-documentation-support",
                        "description": "Support for documentation readiness around institutional procurement and supply requests.",
                        "image_url": "marketing-essentials.jpeg",
                        "alt_texts": "Procurement documentation support",
                        "content": html_block(
                            "Procurement Documentation Support",
                            "We help clients prepare supporting records for more organized procurement and supply processing.",
                            [
                                "Support for supply request documentation",
                                "Clearer documentation flow for institutional buyers",
                                "Practical preparation for internal processing needs",
                            ],
                            "This offering is helpful when procurement documentation slows down otherwise straightforward supply requests.",
                        ),
                        "image_collection": PHARMA_GALLERY,
                    },
                ],
            },
        ],
    },
    {
        "name": "Engineering Consultancy",
        "category_name": "engineering-consultancy",
        "description": "Technical advisory, planning support, and project-facing engineering consultancy for institutions and business operations.",
        "image_url": "placeholders/engineering-consultancy.svg",
        "icon_name": "#cil-settings",
        "alt_texts": "Engineering consultancy support",
        "content": html_block(
            "Engineering Consultancy",
            "Gregbuk provides practical engineering consultancy support for clients that need project planning, technical review, and structured implementation guidance.",
            [
                "Planning support before execution begins",
                "Technical review for more informed decisions",
                "Consultative guidance aligned to operational realities",
            ],
            "This branch is best approached as an inquiry-led service for organizations that want professional support around engineering-related work.",
        ),
        "subservices": [
            {
                "name": "Project Advisory & Planning",
                "category_name": "project-advisory-planning",
                "description": "Early-stage advisory support for scoping, planning, and practical execution readiness.",
                "image_url": "placeholders/engineering-consultancy.svg",
                "alt_texts": "Project advisory and planning",
                "products": [
                    {
                        "name": "Project Scope Review",
                        "category_name": "project-scope-review",
                        "description": "Review support for project assumptions, scope framing, and technical direction.",
                        "image_url": "placeholders/engineering-consultancy.svg",
                        "alt_texts": "Project scope review",
                        "content": html_block(
                            "Project Scope Review",
                            "This offering supports organizations that want a clearer project foundation before moving into execution.",
                            [
                                "Review of project direction and scope framing",
                                "Practical feedback on feasibility and expectations",
                                "Support for better-aligned execution planning",
                            ],
                            "It is useful where early clarity can reduce later waste, confusion, or scope drift.",
                        ),
                        "image_collection": ENGINEERING_GALLERY,
                    },
                    {
                        "name": "Technical Planning Consultation",
                        "category_name": "technical-planning-consultation",
                        "description": "Planning-focused consultation to improve implementation readiness.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Technical planning consultation",
                        "content": html_block(
                            "Technical Planning Consultation",
                            "We help clients think through requirements, dependencies, and likely implementation considerations before work starts.",
                            [
                                "Consultation around planning decisions",
                                "Discussion of project requirements and constraints",
                                "Support for more realistic execution preparation",
                            ],
                            "This is valuable for teams that want a steadier transition from idea to implementation.",
                        ),
                        "image_collection": ENGINEERING_GALLERY,
                    },
                ],
            },
            {
                "name": "Site & Technical Support",
                "category_name": "site-technical-support",
                "description": "Technical support around site-facing execution, assessments, and implementation follow-up.",
                "image_url": "placeholders/operations.svg",
                "alt_texts": "Site and technical support",
                "products": [
                    {
                        "name": "Site Assessment Support",
                        "category_name": "site-assessment-support",
                        "description": "Assessment support for clients that need technical review before execution.",
                        "image_url": "placeholders/operations.svg",
                        "alt_texts": "Site assessment support",
                        "content": html_block(
                            "Site Assessment Support",
                            "Some projects need a clearer understanding of the operating environment before decisions are finalized.",
                            [
                                "Support for site-focused technical review",
                                "Assessment guidance for implementation planning",
                                "Clearer inputs for later project decisions",
                            ],
                            "This helps organizations avoid making execution plans without adequate ground-level context.",
                        ),
                        "image_collection": ENGINEERING_GALLERY,
                    },
                    {
                        "name": "Implementation Follow-Up Support",
                        "category_name": "implementation-follow-up-support",
                        "description": "Support for technical follow-up during project execution and delivery phases.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Implementation follow up support",
                        "content": html_block(
                            "Implementation Follow-Up Support",
                            "We support clients that want ongoing technical perspective while execution is in motion.",
                            [
                                "Technical follow-up through execution stages",
                                "Support for issue review and implementation decisions",
                                "Better continuity between planning and delivery",
                            ],
                            "This is useful when projects benefit from consultative oversight during implementation.",
                        ),
                        "image_collection": ENGINEERING_GALLERY,
                    },
                ],
            },
            {
                "name": "Procurement & Technical Representation",
                "category_name": "procurement-technical-representation",
                "description": "Technical input for procurement decisions, review support, and stakeholder communication.",
                "image_url": "placeholders/office-building.svg",
                "alt_texts": "Procurement and technical representation",
                "products": [
                    {
                        "name": "Technical Procurement Review",
                        "category_name": "technical-procurement-review",
                        "description": "Support for procurement reviews where technical suitability matters.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Technical procurement review",
                        "content": html_block(
                            "Technical Procurement Review",
                            "We help clients review procurement choices where technical suitability affects long-term value.",
                            [
                                "Input on technical fit and practical suitability",
                                "Support for comparing project-aligned options",
                                "Better-informed procurement decisions",
                            ],
                            "This is useful where buying decisions should be grounded in more than price alone.",
                        ),
                        "image_collection": ENGINEERING_GALLERY,
                    },
                    {
                        "name": "Vendor Evaluation Support",
                        "category_name": "vendor-evaluation-support",
                        "description": "Support for evaluating vendor responses and technical alignment.",
                        "image_url": "placeholders/engineering-consultancy.svg",
                        "alt_texts": "Vendor evaluation support",
                        "content": html_block(
                            "Vendor Evaluation Support",
                            "This support line helps organizations review vendor positioning with stronger technical context.",
                            [
                                "Support for comparing vendor submissions",
                                "Technical context for review and follow-up",
                                "Clearer evaluation support during procurement stages",
                            ],
                            "It is valuable where vendor choices have direct project or operational consequences.",
                        ),
                        "image_collection": ENGINEERING_GALLERY,
                    },
                ],
            },
        ],
    },
    {
        "name": "Travel Agency Services",
        "category_name": "travel-agency",
        "description": "Travel planning, documentation support, and coordinated movement assistance for individuals, teams, and organizations.",
        "image_url": "placeholders/travel-agency.svg",
        "icon_name": "#cil-plane",
        "alt_texts": "Travel agency services",
        "content": html_block(
            "Travel Agency Services",
            "Gregbuk supports clients with practical travel coordination, documentation guidance, and movement planning tailored to organizational or personal needs.",
            [
                "Trip planning support for individuals and teams",
                "Documentation guidance for smoother travel preparation",
                "Corporate and event travel coordination support",
            ],
            "This is an inquiry-led branch for travel requests that benefit from clearer coordination and responsive handling.",
        ),
        "subservices": [
            {
                "name": "Corporate Travel Planning",
                "category_name": "corporate-travel-planning",
                "description": "Travel coordination support for teams, executives, and business travel requirements.",
                "image_url": "placeholders/travel-agency.svg",
                "alt_texts": "Corporate travel planning",
                "products": [
                    {
                        "name": "Business Trip Coordination",
                        "category_name": "business-trip-coordination",
                        "description": "Support for planning business-related trips with timing and coordination in view.",
                        "image_url": "placeholders/travel-agency.svg",
                        "alt_texts": "Business trip coordination",
                        "content": html_block(
                            "Business Trip Coordination",
                            "We help structure business travel requests so movement, timing, and travel support are easier to manage.",
                            [
                                "Support for executive and staff trip planning",
                                "Coordination around movement schedules",
                                "Practical handling for business-focused travel needs",
                            ],
                            "This is useful where travel affects meetings, events, or operational schedules.",
                        ),
                        "image_collection": TRAVEL_GALLERY,
                    },
                    {
                        "name": "Executive Travel Support",
                        "category_name": "executive-travel-support",
                        "description": "Coordinated support for executive-level travel planning and logistics.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Executive travel support",
                        "content": html_block(
                            "Executive Travel Support",
                            "For higher-priority movement, this support line focuses on clearer coordination and responsive planning.",
                            [
                                "Travel support for executive schedules",
                                "Coordination around timing-sensitive movement",
                                "Structured assistance for professional travel needs",
                            ],
                            "This helps simplify planning where timing and coordination matter more.",
                        ),
                        "image_collection": TRAVEL_GALLERY,
                    },
                ],
            },
            {
                "name": "Documentation & Visa Support",
                "category_name": "documentation-visa-support",
                "description": "Guidance around travel documentation readiness and visa-related support needs.",
                "image_url": "placeholders/office-building.svg",
                "alt_texts": "Documentation and visa support",
                "products": [
                    {
                        "name": "Visa Advisory Request",
                        "category_name": "visa-advisory-request",
                        "description": "Initial support for understanding visa-related preparation needs and next steps.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Visa advisory request",
                        "content": html_block(
                            "Visa Advisory Request",
                            "This offering supports clients that need a clearer starting point around documentation and visa preparation.",
                            [
                                "Advisory support for visa-related requirements",
                                "Guidance on likely preparation needs",
                                "Clearer next-step orientation for applicants",
                            ],
                            "It is useful where travelers need more clarity before proceeding with documentation work.",
                        ),
                        "image_collection": TRAVEL_GALLERY,
                    },
                    {
                        "name": "Travel Documentation Preparation",
                        "category_name": "travel-documentation-preparation",
                        "description": "Support around organizing and preparing travel-related documentation.",
                        "image_url": "placeholders/travel-agency.svg",
                        "alt_texts": "Travel documentation preparation",
                        "content": html_block(
                            "Travel Documentation Preparation",
                            "We support travelers and organizations that need a more organized documentation process before travel.",
                            [
                                "Support for document-readiness planning",
                                "Guidance around required travel paperwork",
                                "A more structured preparation workflow",
                            ],
                            "This helps reduce last-minute confusion and strengthens readiness before movement dates approach.",
                        ),
                        "image_collection": TRAVEL_GALLERY,
                    },
                ],
            },
            {
                "name": "Group & Event Travel Coordination",
                "category_name": "group-event-travel-coordination",
                "description": "Support for coordinating group movement, event travel, and organization-wide travel requests.",
                "image_url": "placeholders/operations.svg",
                "alt_texts": "Group and event travel coordination",
                "products": [
                    {
                        "name": "Team Movement Coordination",
                        "category_name": "team-movement-coordination",
                        "description": "Support for coordinating movement across teams or small organizational groups.",
                        "image_url": "placeholders/operations.svg",
                        "alt_texts": "Team movement coordination",
                        "content": html_block(
                            "Team Movement Coordination",
                            "Group travel often requires more structured handling than individual requests, and this offering supports that coordination.",
                            [
                                "Support for team-focused travel planning",
                                "Coordination around scheduling and group logistics",
                                "More organized communication for movement needs",
                            ],
                            "It is suitable for business teams, event groups, and coordinated travel requests.",
                        ),
                        "image_collection": TRAVEL_GALLERY,
                    },
                    {
                        "name": "Event Travel Assistance",
                        "category_name": "event-travel-assistance",
                        "description": "Travel support for conferences, project events, and planned group engagements.",
                        "image_url": "print_about_us.webp",
                        "alt_texts": "Event travel assistance",
                        "content": html_block(
                            "Event Travel Assistance",
                            "This support area helps clients coordinate movement for event participation, project teams, and planned organizational travel.",
                            [
                                "Support for conference and event travel planning",
                                "Coordination for group or project movement",
                                "A clearer process for organizing travel details",
                            ],
                            "It helps reduce coordination pressure where multiple travelers are involved.",
                        ),
                        "image_collection": TRAVEL_GALLERY,
                    },
                ],
            },
        ],
    },
    {
        "name": "CAC / Trademark / Commission Services",
        "category_name": "cac-trademark-commission",
        "description": "Business registration, trademark, and compliance-oriented support services for organizations and founders.",
        "image_url": "placeholders/operations.svg",
        "icon_name": "#cil-description",
        "alt_texts": "Business registration and trademark support",
        "content": html_block(
            "CAC / Trademark / Commission Services",
            "Gregbuk supports business owners and organizations with structured registration, documentation, and compliance-focused support across key formalization needs.",
            [
                "Business registration and filing support",
                "Trademark process guidance and documentation support",
                "Compliance-focused help for structured business operations",
            ],
            "This branch is best handled as an inquiry-led service so requests can be matched to the right process path.",
        ),
        "subservices": [
            {
                "name": "Business Registration Services",
                "category_name": "business-registration-services",
                "description": "Support for CAC-related registration requests and business setup documentation.",
                "image_url": "placeholders/operations.svg",
                "alt_texts": "Business registration services",
                "products": [
                    {
                        "name": "New Business Registration Support",
                        "category_name": "new-business-registration-support",
                        "description": "Guidance and support for new business registration requests.",
                        "image_url": "placeholders/operations.svg",
                        "alt_texts": "New business registration support",
                        "content": html_block(
                            "New Business Registration Support",
                            "This offering helps founders and operators move from idea to a more structured registration process.",
                            [
                                "Support for CAC registration preparation",
                                "Guidance on information and documentation needs",
                                "A clearer path through early registration stages",
                            ],
                            "It is useful for new businesses that want more confidence around formal registration steps.",
                        ),
                        "image_collection": SUPPORT_GALLERY,
                    },
                    {
                        "name": "Post-Incorporation Documentation",
                        "category_name": "post-incorporation-documentation",
                        "description": "Support for selected documentation needs that arise after incorporation.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Post incorporation documentation",
                        "content": html_block(
                            "Post-Incorporation Documentation",
                            "Some needs begin after registration, and this support line helps clients handle the next layer of basic documentation work.",
                            [
                                "Guidance on post-incorporation support needs",
                                "Support for selected follow-up documentation",
                                "Structured handling of next-step paperwork",
                            ],
                            "This helps businesses stay better organized after the first registration phase.",
                        ),
                        "image_collection": SUPPORT_GALLERY,
                    },
                ],
            },
            {
                "name": "Trademark & Brand Protection",
                "category_name": "trademark-brand-protection",
                "description": "Support for brand protection requests, trademark preparation, and filing guidance.",
                "image_url": "placeholders/office-building.svg",
                "alt_texts": "Trademark and brand protection",
                "products": [
                    {
                        "name": "Trademark Filing Guidance",
                        "category_name": "trademark-filing-guidance",
                        "description": "Guidance around preparing and structuring trademark filing requests.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Trademark filing guidance",
                        "content": html_block(
                            "Trademark Filing Guidance",
                            "This offering supports businesses that want to approach trademark work with more structure and clarity.",
                            [
                                "Guidance on trademark process expectations",
                                "Support for preparing relevant filing inputs",
                                "A clearer start point for brand protection work",
                            ],
                            "It is useful for businesses that want to formalize brand protection more confidently.",
                        ),
                        "image_collection": SUPPORT_GALLERY,
                    },
                    {
                        "name": "Brand Documentation Review",
                        "category_name": "brand-documentation-review",
                        "description": "Support for reviewing brand-related documentation before filing or follow-up actions.",
                        "image_url": "marketing-essentials.jpeg",
                        "alt_texts": "Brand documentation review",
                        "content": html_block(
                            "Brand Documentation Review",
                            "We help clients organize and review the documentation that supports more orderly trademark and brand-related requests.",
                            [
                                "Review support for brand filing inputs",
                                "Support for stronger documentation readiness",
                                "Practical guidance before next-step submission",
                            ],
                            "This reduces the risk of moving forward with incomplete or poorly prepared documentation.",
                        ),
                        "image_collection": SUPPORT_GALLERY,
                    },
                ],
            },
            {
                "name": "Compliance Filings & Documentation",
                "category_name": "compliance-filings-documentation",
                "description": "Support for documentation-heavy business requests tied to commission or compliance processes.",
                "image_url": "placeholders/operations.svg",
                "alt_texts": "Compliance filings and documentation",
                "products": [
                    {
                        "name": "Commission Documentation Support",
                        "category_name": "commission-documentation-support",
                        "description": "Support for preparing and organizing commission-related documentation requests.",
                        "image_url": "placeholders/operations.svg",
                        "alt_texts": "Commission documentation support",
                        "content": html_block(
                            "Commission Documentation Support",
                            "This offering supports clients that need a more organized process around commission-related documentation work.",
                            [
                                "Documentation support for commission-focused requests",
                                "Guidance on preparing supporting records",
                                "Better structure around process handling",
                            ],
                            "It is designed for requests where documentation quality directly affects progress.",
                        ),
                        "image_collection": SUPPORT_GALLERY,
                    },
                    {
                        "name": "Business Compliance Support",
                        "category_name": "business-compliance-support",
                        "description": "Practical support for documentation and filing-related business compliance needs.",
                        "image_url": "placeholders/office-building.svg",
                        "alt_texts": "Business compliance support",
                        "content": html_block(
                            "Business Compliance Support",
                            "Gregbuk helps clients approach business compliance needs with more order, clarity, and process readiness.",
                            [
                                "Support for compliance-related documentation tasks",
                                "Guidance around filing readiness",
                                "A clearer process flow for business support requests",
                            ],
                            "This is useful for founders and operators that need guided support rather than trial-and-error handling.",
                        ),
                        "image_collection": SUPPORT_GALLERY,
                    },
                ],
            },
        ],
    },
]


for service_payload in TARGETED_SERVICES:
    for sub_payload in service_payload.get("subservices", []):
        if not sub_payload.get("content"):
            sub_payload["content"] = default_subservice_content(
                service_payload["name"],
                sub_payload["name"],
                sub_payload["description"],
            )


def sync_fields(instance, payload, fields):
    changed = False
    for field in fields:
        value = payload.get(field)
        if getattr(instance, field) != value:
            setattr(instance, field, value)
            changed = True
    return changed


def get_service(payload):
    return Services.query.filter(
        or_(
            Services.category_name == payload["category_name"],
            Services.name == payload["name"],
        )
    ).first()


def get_subservice(payload):
    return SubService.query.filter(
        or_(
            SubService.category_name == payload["category_name"],
            SubService.name == payload["name"],
        )
    ).first()


def get_product(payload):
    return Products.query.filter(
        or_(
            Products.category_name == payload["category_name"],
            Products.name == payload["name"],
        )
    ).first()


def upsert_service(payload):
    service = get_service(payload)
    created = False
    if not service:
        service = Services(category_name=payload["category_name"])
        db.session.add(service)
        created = True
    sync_fields(
        service,
        payload,
        ["name", "description", "image_url", "icon_name", "alt_texts", "content"],
    )
    db.session.flush()
    return service, created


def upsert_subservice(service, payload):
    subservice = get_subservice(payload)
    created = False
    if not subservice:
        subservice = SubService(category_name=payload["category_name"])
        db.session.add(subservice)
        created = True
    sync_fields(
        subservice,
        payload,
        ["name", "description", "image_url", "alt_texts", "content"],
    )
    if subservice.services != service:
        subservice.services = service
    db.session.flush()
    return subservice, created


def upsert_product(service, subservice, payload):
    product = get_product(payload)
    created = False
    if not product:
        product = Products(category_name=payload["category_name"])
        db.session.add(product)
        created = True
    sync_fields(
        product,
        payload,
        ["name", "description", "image_url", "alt_texts", "content"],
    )
    if subservice is not None:
        product.subservice = subservice
        product.services = None
    else:
        product.services = service
        product.subservice = None
    db.session.flush()
    return product, created


def sync_product_gallery(product, image_paths):
    existing = {item.image_collections for item in product.image_collections}
    created = 0
    for image_path in image_paths:
        if image_path not in existing:
            db.session.add(
                ProductCollection(
                    image_collections=image_path,
                    product=product,
                )
            )
            created += 1
    return created


def seed_targeted_services():
    counts = {
        "services_created": 0,
        "services_updated": 0,
        "subservices_created": 0,
        "subservices_updated": 0,
        "products_created": 0,
        "products_updated": 0,
        "gallery_images_added": 0,
    }

    for service_payload in TARGETED_SERVICES:
        service, service_created = upsert_service(service_payload)
        counts["services_created" if service_created else "services_updated"] += 1

        for sub_payload in service_payload.get("subservices", []):
            subservice, sub_created = upsert_subservice(service, sub_payload)
            counts["subservices_created" if sub_created else "subservices_updated"] += 1

            for product_payload in sub_payload.get("products", []):
                product, product_created = upsert_product(service, subservice, product_payload)
                counts["products_created" if product_created else "products_updated"] += 1
                counts["gallery_images_added"] += sync_product_gallery(
                    product,
                    product_payload.get("image_collection", []),
                )

    db.session.commit()
    return counts


if __name__ == "__main__":
    with app.app_context():
        results = seed_targeted_services()
        print(
            "Targeted service seed complete -> "
            f"services created: {results['services_created']}, "
            f"services refreshed: {results['services_updated']}, "
            f"subservices created: {results['subservices_created']}, "
            f"subservices refreshed: {results['subservices_updated']}, "
            f"products created: {results['products_created']}, "
            f"products refreshed: {results['products_updated']}, "
            f"gallery images added: {results['gallery_images_added']}"
        )
