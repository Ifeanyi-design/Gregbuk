from main import app
from db import db, Services, SubService, Products, Header, ProductCollection
from random import choice
from flask import url_for

imgg = [
    'https://picsum.photos/seed/1/400/300',
    'https://picsum.photos/seed/2/400/300',
    'https://picsum.photos/seed/3/400/300',
    'https://picsum.photos/seed/4/400/300',
    'https://picsum.photos/seed/5/400/300',
    'https://picsum.photos/seed/6/400/300',
    'https://picsum.photos/seed/7/400/300',
    'https://picsum.photos/seed/8/400/300',
    'https://picsum.photos/seed/9/400/300',
    'https://picsum.photos/seed/10/400/300',
    'https://picsum.photos/seed/11/400/300',
    'https://picsum.photos/seed/12/400/300',
    'https://picsum.photos/seed/13/400/300',
    'https://picsum.photos/seed/14/400/300',
    'https://picsum.photos/seed/15/400/300',
    'https://picsum.photos/seed/16/400/300',
    'https://picsum.photos/seed/17/400/300',
    'https://picsum.photos/seed/18/400/300',
    'https://picsum.photos/seed/19/400/300',
    'https://picsum.photos/seed/20/400/300',
    'https://picsum.photos/seed/21/400/300',
    'https://picsum.photos/seed/22/400/300',
    'https://picsum.photos/seed/23/400/300',
    'https://picsum.photos/seed/24/400/300',
    'https://picsum.photos/seed/25/400/300',
    'https://picsum.photos/seed/26/400/300',
    'https://picsum.photos/seed/27/400/300',
    'https://picsum.photos/seed/28/400/300',
    'https://picsum.photos/seed/29/400/300',
    'https://picsum.photos/seed/30/400/300',
    'https://picsum.photos/seed/31/400/300',
    'https://picsum.photos/seed/32/400/300',
    'https://picsum.photos/seed/33/400/300',
    'https://picsum.photos/seed/34/400/300',
    'https://picsum.photos/seed/35/400/300',
    'https://picsum.photos/seed/36/400/300',
    'https://picsum.photos/seed/37/400/300',
    'https://picsum.photos/seed/38/400/300',
    'https://picsum.photos/seed/39/400/300',
    'https://picsum.photos/seed/40/400/300',
    'https://picsum.photos/seed/41/400/300',
    'https://picsum.photos/seed/42/400/300',
    'https://picsum.photos/seed/43/400/300',
    'https://picsum.photos/seed/44/400/300',
    'https://picsum.photos/seed/45/400/300',
    'https://picsum.photos/seed/46/400/300',
    'https://picsum.photos/seed/47/400/300',
    'https://picsum.photos/seed/48/400/300',
    'https://picsum.photos/seed/49/400/300',
    'https://picsum.photos/seed/50/400/300',
    'https://picsum.photos/seed/51/400/300',
    'https://picsum.photos/seed/52/400/300',
    'https://picsum.photos/seed/53/400/300',
    'https://picsum.photos/seed/54/400/300',
    'https://picsum.photos/seed/55/400/300',
    'https://picsum.photos/seed/56/400/300',
    'https://picsum.photos/seed/57/400/300',
    'https://picsum.photos/seed/58/400/300',
    'https://picsum.photos/seed/59/400/300',
    'https://picsum.photos/seed/60/400/300',
    'https://picsum.photos/seed/61/400/300',
    'https://picsum.photos/seed/62/400/300',
    'https://picsum.photos/seed/63/400/300',
    'https://picsum.photos/seed/64/400/300',
    'https://picsum.photos/seed/65/400/300',
    'https://picsum.photos/seed/66/400/300',
    'https://picsum.photos/seed/67/400/300',
    'https://picsum.photos/seed/68/400/300',
    'https://picsum.photos/seed/69/400/300',
    'https://picsum.photos/seed/70/400/300',
    'https://picsum.photos/seed/71/400/300',
    'https://picsum.photos/seed/72/400/300',
    'https://picsum.photos/seed/73/400/300',
    'https://picsum.photos/seed/74/400/300',
    'https://picsum.photos/seed/75/400/300',
    'https://picsum.photos/seed/76/400/300',
    'https://picsum.photos/seed/77/400/300',
    'https://picsum.photos/seed/78/400/300',
    'https://picsum.photos/seed/79/400/300',
    'https://picsum.photos/seed/80/400/300',
    'https://picsum.photos/seed/81/400/300',
    'https://picsum.photos/seed/82/400/300',
    'https://picsum.photos/seed/83/400/300',
    'https://picsum.photos/seed/84/400/300',
    'https://picsum.photos/seed/85/400/300',
    'https://picsum.photos/seed/86/400/300',
    'https://picsum.photos/seed/87/400/300',
    'https://picsum.photos/seed/88/400/300',
    'https://picsum.photos/seed/89/400/300',
    'https://picsum.photos/seed/90/400/300',
    'https://picsum.photos/seed/91/400/300',
    'https://picsum.photos/seed/92/400/300',
    'https://picsum.photos/seed/93/400/300',
    'https://picsum.photos/seed/94/400/300',
    'https://picsum.photos/seed/95/400/300',
    'https://picsum.photos/seed/96/400/300',
    'https://picsum.photos/seed/97/400/300',
    'https://picsum.photos/seed/98/400/300',
    'https://picsum.photos/seed/99/400/300',
    'https://picsum.photos/seed/100/400/300'
]
with app.app_context():
    db.create_all()
    data = [
        {
            "name": "Business Cards",
            "description": "High-quality business cards that make a lasting first impression, available in a variety of finishes and styles.",
            "image_url": choice(imgg),
            "icon_name": "#cil-credit-card",
            "category_name": "Cards",
            "content": """
            <h1>Premium Custom Business Card Printing with Gregbuk</h1>

  <h2>Make a Lasting First Impression</h2>
  <p>
    Your business card is often the first physical touchpoint for potential clients, partners, or collaborators.
    At <strong>Gregbuk</strong>, we ensure that first impression is unforgettable. Professionally printed, high-quality <strong>business cards</strong> help you stand out, whether at networking events, conferences, or one-on-one meetings.
    Every detail matters—from design to finish—to ensure your brand looks polished and memorable.
  </p>

  <h2>Effortless Online Customization</h2>
  <p>
    With our intuitive online platform, designing and ordering your <strong>custom business cards</strong> has never been easier. Select your preferred material, finish, and design, then upload your artwork.
    Our simple interface gives you full control over layouts, fonts, colors, and logos, making it quick and effortless to create a professional look. Explore our <a href="/services/Cards">templates</a> to start your design instantly.
  </p>

  <h2>High-Quality Materials & Finishes</h2>
  <p>
    Gregbuk offers a wide range of premium paper stocks and finishes to match your brand’s personality.
    Choose from classic <strong>matte</strong> or <strong>glossy finishes</strong>, luxurious <strong>soft-touch coatings</strong>, or metallic <strong>foil-stamped accents</strong>. Every card is printed with precision to ensure sharp graphics, vibrant colors, and a long-lasting professional feel.
  </p>

  <h2>Variety of Styles & Formats</h2>
  <p>
    Our business cards are fully customizable to reflect your unique brand identity. Options include:
  </p>
  <ul>
    <li><strong>Standard Cards:</strong> Sleek, professional, and classic 3.4” x 2.2” size — <a href="/services/Cards/standard">View Standard Cards</a></li>
    <li><strong>Square Cards:</strong> Modern and creative 2.5” x 2.5” cards for a distinctive look — <a href="/services/Cards/square">View Square Cards</a></li>
    <li><strong>Rounded Corners:</strong> Smooth edges for a stylish, modern feel — <a href="/services/Cards/rounded-corner">View Rounded Cards</a></li>
    <li><strong>Ultra-Thick Cards:</strong> Extra weight for a premium tactile experience — <a href="/services/Cards/ultra-thick">View Ultra-Thick Cards</a></li>
    <li><strong>Foil & Embossed Cards:</strong> Add shine and texture for luxury appeal — <a href="/services/Cards/glossy">View Glossy Cards</a></li>
  </ul>

  <h2>Stand Out with Customization</h2>
  <p>
    Every detail counts when it comes to your business card. Add your logo, adjust typography, or experiment with color accents. With our online editor, you can test multiple designs and finishes to create the perfect card for your brand. Whether you prefer a minimalist design or a bold, eye-catching look, Gregbuk gives you full creative freedom. Start designing <a href="/contact">here</a>.
  </p>

  <h2>Specialty Cards for Unique Needs</h2>
  <p>
    Beyond standard business cards, Gregbuk offers specialty formats:
  </p>
  <ul>
    <li><strong>Loyalty Cards:</strong> Reward your customers while promoting your business — <a href="/services/Cards/loyalty">View Loyalty Cards</a></li>
    <li><strong>Appointment Cards:</strong> Perfect for salons, medical offices, and consultants to keep clients organized — <a href="/services/Cards/appointment">View Appointment Cards</a></li>
    <li><strong>Square Cards:</strong> Modern, memorable, and ideal for creative professionals — <a href="/services/Cards/square">View Square Cards</a></li>
    <li><strong>Premium Textured Cards:</strong> Linen, felt, or soft-touch finishes for a high-end feel — <a href="/services/Cards/special-pape">View Premium Textured Cards</a></li>
  </ul>

  <h2>Design Tips for Maximum Impact</h2>
  <p>
    A well-designed business card is not just a contact tool—it’s a reflection of your brand identity. Key elements to include:
  </p>
  <ul>
    <li><b>Your Name & Job Title</b></li>
    <li><b>Company Name & Logo</b></li>
    <li><b>Phone Number & Email</b></li>
    <li><b>Website & Social Media Links</b></li>
    <li><b>QR Code for Quick Access to Your Online Profile</b></li>
  </ul>

  <h2>Fast Turnaround & Flexible Quantities</h2>
  <p>
    Whether you need a small batch for personal networking or a large order for your team, Gregbuk handles it all. Our advanced digital printing ensures a fast turnaround while maintaining premium quality. Reorder anytime with ease, so you never run out of professional business cards. Learn more about our <a href="/about-us">printing services</a>.
  </p>


  <h2>Order Your Custom Business Cards Today</h2>
  <p>
    Take your networking and branding to the next level with Gregbuk <strong>custom business cards</strong>. Design online, select your preferred finish, and receive high-quality, durable cards that leave a lasting impression. <a href="/contact" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Get Quote now</strong></a>!
  </p>
            """,
            "products": [
                {"name": "Glossy Card",
                 "description": "Premium glossy finish for vibrant colors and a professional look.",
                 "image_url": choice(imgg), "category_name": "glossy", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Matte Card",
                 "description": "Smooth, non-reflective finish for a sophisticated and elegant appearance.",
                 "image_url": choice(imgg), "category_name": "matte", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Standard Business Card",
                 "description": "Classic and versatile business card perfect for any professional need.",
                 "image_url": choice(imgg), "category_name": "standard", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Square Business Card",
                 "description": "Modern square shape that stands out from traditional business cards.",
                 "image_url": choice(imgg), "category_name": "square", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Rounded Corner Business Card",
                 "description": "Elegant rounded edges for a sleek, premium finish.", "image_url": choice(imgg),
                 "category_name": "rounded-corner", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Ultra Thick Business Card",
                 "description": "Extra thick cardstock for a luxury feel and durability.", "image_url": choice(imgg),
                 "category_name": "ultra-thick", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Special Papers Business Card",
                 "description": "Unique textured or specialty paper to leave a memorable impression.",
                 "image_url": choice(imgg), "category_name": "special-paper", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Loyalty Card", "description": "Customizable loyalty cards to reward your best customers.",
                 "image_url": choice(imgg), "category_name": "loyalty", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Appointment Card",
                 "description": "Practical cards for scheduling appointments and keeping clients organized.",
                 "image_url": choice(imgg), "category_name": "appointment", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Complementary Card", "description": "Small, elegant cards to accompany gifts or services.",
                 "image_url": choice(imgg), "category_name": "complementary", "image_collection": [choice(imgg) for n in range(8)]}
            ]
        },
        {
            "name": "Marketing Essentials",
            "description": "Comprehensive marketing materials to promote your business and engage your audience.",
            "image_url": choice(imgg),
            "icon_name": "#cil-bullhorn",
            "category_name": "Marketing",
            "content": """
<h1>Marketing Essentials Printing for Your Business Success</h1>
<h2>Professional Marketing Materials & Stationery</h2>
<p>
    At <strong>Gregbuk</strong>, we specialize in <strong>custom marketing essentials</strong>
    that help your brand communicate with confidence and style. Whether you need
    <a href="/services/Cards">business cards</a>,
    <a href="/services/Marketing/flyers-and-brochures">brochures</a>,
    <a href="/services/Marketing/flyers-and-brochures">flyers</a>,
    <a href="/services/Marketing/stationery/folder">presentation folders</a>, or
    <a href="/services/Marketing/stationery/letter-head">letterheads</a>, our professional
    printing services ensure sharp colors, premium finishes, and lasting impact.
</p>

<p>
    With flexible order quantities, a wide choice of papers and finishes, and fast turnaround times,
    Gregbuk makes it easy to create <strong>marketing tools</strong> that reflect your brand’s identity
    and engage your audience.
</p>

<h2>Why Marketing Essentials Matter</h2>
<p>
    Every business needs a reliable set of printed tools to attract customers,
    build trust, and stay memorable. <strong>Marketing essentials</strong> like
    flyers, brochures, and business cards are not just paper products—they’re a
    reflection of your brand. With <strong>Gregbuk’s expertise in digital and
    offset printing</strong>, you can expect professional quality that sets you
    apart from the competition.
</p>

<h2>Explore Our Marketing Essentials</h2>
<p>
    From everyday office stationery to powerful promotional materials,
    <strong>Gregbuk</strong> provides a complete range of
    <a href="/services/Marketing">marketing essentials</a>
    tailored to your business needs:
</p>
<ul>
    <li><strong>Business Cards</strong> – Custom sizes, premium textures, and eco-friendly options.</li>
    <li><strong>Flyers & Brochures</strong> – Perfect for events, product promotions, and sales campaigns.</li>
    <li><strong>Presentation Folders</strong> – Keep proposals and documents polished and professional.</li>
    <li><strong>Letterheads & Envelopes</strong> – Elevate your brand’s communication with personalized stationery.</li>
    <li><strong>Postcards & Invitations</strong> – Great for announcements, campaigns, or personal outreach.</li>
    <li><strong>Rack Cards & Menus</strong> – Essential for restaurants, retail stores, and hospitality businesses.</li>
    <li><strong>Notebooks & Notepads</strong> – Branded office essentials that reinforce your company identity.</li>
    <li><strong>Bookmarks</strong> – Small but effective tools for giveaways and promotions.</li>
</ul>

<h2>High-Quality Business Cards</h2>
<p>
    Your <a href="/services/Cards">business card</a> is often your first impression.
    At Gregbuk, we ensure that impression is unforgettable. Choose from glossy,
    matte, textured, or foil-stamped finishes for cards that represent your brand
    with style and durability.
</p>

<h2>Flyers & Brochures That Drive Results</h2>
<p>
    Promote your services with <a href="/services/Marketing/flyers-and-brochures">flyers</a>
    and <a href="/services/Marketing/flyers-and-brochures">brochures</a> that combine
    creative design with premium print quality. Select from a wide range of sizes,
    folding styles, and paper weights to suit every campaign, from local events to
    corporate promotions.
</p>

<h2>Letterheads & Branded Stationery</h2>
<p>
    <a href="/services/Marketing/stationery/letter-head">Custom letterheads</a> and
    <a href="/services/Marketing/stationery/envelop">printed envelopes</a>
    strengthen your business identity with every piece of correspondence. Gregbuk offers modern,
    clean, and professional designs with high-quality printing that reflects your brand’s credibility and professionalism.
</p>

<h2>Postcards, Invitations & Rack Cards</h2>
<p>
    Direct mail and handouts remain powerful marketing tools—especially when they look great. With Gregbuk’s
    <strong>postcards</strong>,
    <a href="/services/Marketing/invitation-cards/invite">invitations</a>, and
    <a href="/services/Marketing/invitation-cards/holi-cards">holiday cards</a>,
    you can spread your message with style. Perfect for grand openings, special events, or seasonal promotions,
    these materials can be customized with glossy or matte finishes, premium cardstock, and unique formats.
</p>

<h2>Stationery & Office Materials</h2>
<p>
    Keep your brand consistent across all interactions with
    <a href="/services/Marketing/stationery">custom stationery</a> from Gregbuk. From branded
    <a href="/services/Marketing/stationery/notepad">notepads</a>,
    <a href="/services/Marketing/stationery/folder">folders</a>, and
    <a href="/services/Marketing/brochure/bookmark">bookmarks</a> to professional
    envelopes and letterheads, we provide everything you need to showcase a cohesive identity across your communications.
</p>

<h2>Why Choose Gregbuk for Marketing Essentials?</h2>
<ul>
    <li><strong>Premium quality printing</strong> that makes your brand shine.</li>
    <li><strong>Flexible quantities</strong> – from small batches to bulk orders.</li>
    <li><strong>Fast turnaround</strong> to meet tight deadlines.</li>
    <li><strong>Custom design support</strong> to bring your ideas to life.</li>
</ul>

<h2>Boost Your Brand with Gregbuk’s Marketing Essentials</h2>
<p>
    Whether you’re a startup building your identity or an established business
    expanding your reach, Gregbuk’s <strong>Marketing Essentials</strong> deliver the quality and reliability you need.
    Our focus on design, detail, and durability ensures your printed materials always make the right impression.
</p>

<p>
    📞 <a class="btn btn-outline-primary rounded-pill border border-2 border-primary" href="/contact"><strong>Get started today</strong></a> – contact our
    expert team to discuss your project. Let’s create marketing essentials that work for your brand.
</p>
""",
            "subservices": [
                {
                    "name": "Flyers & Brochures",
                    "description": "Eye-catching flyers and brochures to advertise your products and services effectively.",
                    "image_url": choice(imgg),
                    "category_name": "flyers-and-brochures",
                    "products": [
                        {"name": "Flyers",
                         "description": "Single-page, full-color flyers for quick promotions or events.",
                         "image_url": choice(imgg), "category_name": "flyer", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Club Flyers",
                         "description": "Vibrant, energetic flyers designed for nightlife and club promotions.",
                         "image_url": choice(imgg), "category_name": "club-flyer", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Brochures",
                         "description": "Informative brochures to showcase your business offerings in detail.",
                         "image_url": choice(imgg), "category_name": "brochures", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Tri-Fold Brochures",
                         "description": "Compact tri-fold brochures perfect for trade shows and presentations.",
                         "image_url": choice(imgg), "category_name": "tri-fold", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Z-Fold Brochure",
                         "description": "Unique Z-fold brochures that unfold to present information creatively.",
                         "image_url": choice(imgg), "category_name": "z-fold", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Booklets & Catalogs",
                    "description": "Professional booklets and catalogs to display your products and services elegantly.",
                    "image_url": choice(imgg),
                    "category_name": "brochure",
                    "products": [
                        {"name": "Booklets",
                         "description": "Compact multi-page booklets ideal for product guides and company portfolios.",
                         "image_url": choice(imgg), "category_name": "book", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Catalogs",
                         "description": "Full-scale catalogs that present your products in an organized, attractive manner.",
                         "image_url": choice(imgg), "category_name": "catalogs", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Zines",
                         "description": "Creative, small-batch publications perfect for niche audiences.",
                         "image_url": choice(imgg), "category_name": "zine", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Magazines",
                         "description": "Professional magazines to highlight your brand and stories.",
                         "image_url": choice(imgg), "category_name": "magazines", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Journals", "description": "Custom journals for personal or corporate branding.",
                         "image_url": choice(imgg), "category_name": "journals", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Bookmarks",
                         "description": "Printed bookmarks for promotional giveaways or retail use.",
                         "image_url": choice(imgg), "category_name": "bookmark", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Poster Printing",
                    "description": "Large-format posters to make a bold statement and promote your brand effectively.",
                    "image_url": choice(imgg),
                    "category_name": "poster",
                    "products": [
                        {"name": "Posters",
                         "description": "Standard posters for events, promotions, or advertisements.",
                         "image_url": choice(imgg), "category_name": "post", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Large Format Poster",
                         "description": "Extra-large posters to attract attention from a distance.",
                         "image_url": choice(imgg), "category_name": "large-poster", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Outdoor Poster",
                         "description": "Durable posters designed for outdoor use and weather resistance.",
                         "image_url": choice(imgg), "category_name": "outdoor-poster", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Mounted Poster",
                         "description": "Posters mounted on boards for a polished, professional look.",
                         "image_url": choice(imgg), "category_name": "mounted-poster", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Poster Signs",
                         "description": "Custom poster signs for retail, exhibitions, or events.",
                         "image_url": choice(imgg), "category_name": "post-s", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Stationery",
                    "description": "Custom stationery to maintain a consistent brand identity in office and client communications.",
                    "image_url": choice(imgg),
                    "category_name": "stationery",
                    "products": [
                        {"name": "Notepads", "description": "Branded notepads for office use or promotional purposes.",
                         "image_url": choice(imgg), "category_name": "notepad", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Letterheads",
                         "description": "Professional letterheads to create impactful business correspondence.",
                         "image_url": choice(imgg), "category_name": "letter-head", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Folders",
                         "description": "Durable folders for organizing documents or client materials.",
                         "image_url": choice(imgg), "category_name": "folder", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Envelopes", "description": "Custom envelopes to complement your branded stationery.",
                         "image_url": choice(imgg), "category_name": "envelop", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Invitation & Cards",
                    "description": "Elegant invitation cards and personalized cards for all occasions and events.",
                    "image_url": choice(imgg),
                    "category_name": "invitation-cards",
                    "products": [
                        {"name": "Standard Postcards",
                         "description": "Classic postcards for correspondence or promotional use.",
                         "image_url": choice(imgg), "category_name": "standard-postcd", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Foil Postcards",
                         "description": "Luxurious foil-finished postcards that shine and impress.",
                         "image_url": choice(imgg), "category_name": "foil-postcd", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Invitation Cards",
                         "description": "Stylish invitation cards for weddings, parties, and corporate events.",
                         "image_url": choice(imgg), "category_name": "invite", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Foil Invitations",
                         "description": "Premium invitations with metallic foil accents for elegance.",
                         "image_url": choice(imgg), "category_name": "foil-invite", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Holiday Cards", "description": "Festive cards for holidays and seasonal greetings.",
                         "image_url": choice(imgg), "category_name": "holi-cards", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Greeting Cards",
                         "description": "Beautifully designed cards to convey messages and well wishes.",
                         "image_url": choice(imgg), "category_name": "greet-cards", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Thank You Cards",
                         "description": "Express gratitude with custom-designed thank you cards.",
                         "image_url": choice(imgg), "category_name": "thanks-card", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Response Cards",
                         "description": "Convenient response cards to RSVP or collect feedback.",
                         "image_url": choice(imgg), "category_name": "response-card", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        },
        {
            "name": "Stickers & Labels",
            "description": "Custom stickers and labels designed for branding, packaging, and promotional purposes.",
            "image_url": choice(imgg),
            "icon_name": "#cil-tag",
            "category_name": "stickers-labels",
            "content": """
            <h1>Custom Label & Sticker Printing with Gregbuk</h1>

  <h2>High-Quality Custom Labels for Your Brand</h2>
  <p>
    Elevate your product presentation with <strong>custom labels</strong> from Gregbuk. Perfect for bottles, jars, packages, and more, our <strong>high-quality label printing</strong> services deliver vibrant colors, sharp details, and durable materials. Whether you need a few labels or bulk quantities, designing and ordering your personalized labels online is simple, fast, and reliable.
  </p>

  <h2>Why Custom Labels Are Essential</h2>
  <p>
    Labels do more than provide product information—they represent your brand. Our <strong>custom adhesive labels</strong> help you communicate key product details, highlight ingredients or instructions, and make a lasting impression on your customers. From unique shapes to custom finishes, you can create labels that perfectly fit your product and branding style. Explore our <a href="/services/stickers-labels/cr-labels">label templates</a> to get started.
  </p>

  <h2>Premium Materials & Finishes</h2>
  <p>
    Gregbuk offers a wide range of high-quality materials for your labels, including waterproof, glossy, matte, and textured finishes. Choose from different adhesives and shapes—roll labels, square, round, oval, or custom die-cut designs. Each label is printed using advanced digital printing technology to ensure vivid colors and precise details, giving your products a professional, polished look. Learn more about our <a href="/about-us">premium finishes</a>.
  </p>

  <h2>Custom Labels for Any Product</h2>
  <p>
    Whether it’s for <b>food packaging</b>, cosmetics, homemade goods, beverages, or corporate branding, our labels are versatile and easy to apply. Options include:
  </p>
  <ul>
    <li><strong>Roll Labels:</strong> Ideal for high-volume orders and industrial use, perfect for bottles, jars, and packaging. <a href="/services/stickers-labels/cr-labels">View Roll Labels</a></li>
    <li><strong>Custom Stickers:</strong> Choose die-cut, square, round, rectangular, oval, or fully custom shapes. <a href="/services/stickers-labels/custom-sticker">View Custom Stickers</a></li>
    <li><strong>Sheet Labels:</strong> Convenient for small batches or home printing. <a href="/services/stickers-labels/sheet-labels">View Sheet Labels</a></li>
  </ul>

  <h2>Industrial & Bulk Labeling Solutions</h2>
  <p>
    For businesses that require large-scale labeling, our <strong>custom roll labels</strong> are perfect. Designed for <b>wine and beer bottles</b>, <b>honey and jam jars</b>, and other <b>food packaging</b>, these labels are durable, easy to apply, and maintain consistent quality across every batch. Explore <a href="/services/stickers-labels">bulk labeling solutions</a> for efficiency and cost savings.
  </p>

  <h2>Easy Online Ordering</h2>
  <p>
    Creating <strong>custom labels online</strong> is simple with Gregbuk. Select your preferred <b>material</b>, <b>finish</b>, and label format, then upload your design or use our free templates. Our platform provides instant online pricing, so you know the cost before placing your order. <a href="/contact">Start Your Order</a>
  </p>


  <h2>Frequently Asked Questions</h2>
  <ul>
    <li><strong>Where can I print custom labels?</strong> Gregbuk provides high-quality, affordable custom label printing with fast shipping nationwide.</li>
    <li><strong>What are the benefits of roll labels?</strong> Roll labels are ideal for large-volume orders, easy to store, and simplify application.</li>
    <li><strong>Can I customize shapes and sizes?</strong> Yes! Our labels come in various shapes, sizes, and materials to match your product perfectly.</li>
  </ul>

  <h2>Boost Your Branding with Custom Labels</h2>
  <p>
    Stand out in a competitive market with professionally printed, high-quality <strong>custom labels and stickers</strong> from Gregbuk. Perfect for retail, food and beverage, cosmetics, and handmade products, our labels combine vibrant design, durability, and brand impact. <a href="/contact" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Order Your Labels Today</strong></a> and make every product unforgettable.
  </p>
            """,
            "products": [
                {"name": "Die-Cut Stickers",
                 "description": "Precision-cut stickers in custom shapes for creative branding.",
                 "image_url": choice(imgg), "category_name": "die-cut", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Round Stickers",
                 "description": "Classic circular stickers ideal for packaging and promotions.",
                 "image_url": choice(imgg), "category_name": "round-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Rectangle Stickers",
                 "description": "Versatile rectangular stickers suitable for labels and branding.",
                 "image_url": choice(imgg), "category_name": "rect-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Custom Shape Sticker",
                 "description": "Stickers cut into any shape to match your brand's unique identity.",
                 "image_url": choice(imgg), "category_name": "custom-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Oval Sticker",
                 "description": "Stylish oval stickers perfect for packaging or product labels.",
                 "image_url": choice(imgg), "category_name": "oval-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Square Sticker",
                 "description": "Square-shaped stickers for labels, promotions, and giveaways.",
                 "image_url": choice(imgg), "category_name": "square-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Custom Roll Labels",
                 "description": "High-quality roll labels for bulk packaging or industrial use.",
                 "image_url": choice(imgg), "category_name": "cr-labels", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Sheet Labels",
                 "description": "High-quality sheet labels for bulk packaging or industrial use.",
                 "image_url": choice(imgg), "category_name": "sheet-labels", "image_collection": [choice(imgg) for n in range(8)]}
            ]
        },
        {
            "name": "Signs & Banners",
            "description": "Professional signage and banners to showcase your brand, events, or promotions.",
            "image_url": choice(imgg),
            "icon_name": "#cil-notes",
            "category_name": "signs-banner",
            "content": """
            <h1>Custom Signs & Banners Printing – Gregbuk</h1>

  <h2>Professional Signs & Banners to Showcase Your Brand</h2>
  <p>
    Make your business, event, or promotion stand out with <strong>high-quality signs and banners</strong> from Gregbuk. Whether it’s for indoor displays, outdoor advertising, or trade shows, our custom solutions ensure your message is clear, vibrant, and memorable.
  </p>

  <h2>Custom Banners for Every Occasion</h2>
  <p>
    Our <strong>banners</strong> are designed for both indoor and outdoor use, fully customizable to your needs. Choose from materials such as vinyl, fabric, mesh, and more. Whether you need <a href="/services/signs-banner/banner/vinyl">vinyl banners</a> for durability, <a href="/services/signs-banner/banner/fabric">fabric banners</a> for elegance, or <a href="/services/signs-banner/banner/mesh">mesh banners</a> for wind resistance, Gregbuk has you covered.
  </p>
  <ul>
    <li><strong>Vinyl Banner:</strong> Durable and vibrant, perfect for long-term display.</li>
    <li><strong>Fabric Banner:</strong> Premium finish and soft texture for a professional look.</li>
    <li><strong>Mesh Banner:</strong> Wind-resistant banners ideal for outdoor events.</li>
    <li><strong>X Banner Stands:</strong> Portable displays perfect for trade shows.</li>
    <li><strong>Step & Repeat Banners:</strong> Ideal for photo backdrops and branding.</li>
    <li><strong>Pop Up Display:</strong> Quick and easy banners for instant setups.</li>
    <li><strong>Tablecloths & Table Runners:</strong> Branded setups for events and promotions.</li>
  </ul>

  <h2>Retractable Banners – Portable Marketing on the Go</h2>
  <p>
    Gregbuk offers a wide range of <strong>retractable banners</strong> for easy setup and professional presentation. From standard retractable banners to deluxe and double-sided options, these solutions are ideal for trade shows, exhibitions, and events. Customize your banner with premium print and finishes for maximum impact. Learn more about <a href="/services/signs-banner/retract-banner">retractable banners</a>.
  </p>

  <ul>
    <li><strong>Standard Retractable Banner:</strong> Perfect for general events and exhibitions.</li>
    <li><strong>Premium Retractable Banner:</strong> High-quality print and finish for professional use.</li>
    <li><strong>Deluxe Retractable Banner:</strong> Extra-large for maximum visibility.</li>
    <li><strong>Professional Retractable Banner:</strong> Corporate-grade for high-visibility promotions.</li>
    <li><strong>Black Retractable Banner:</strong> Sleek design for elegant displays.</li>
    <li><strong>Double-Sided Retractable Banner:</strong> Displays your message on both sides.</li>
  </ul>

  <h2>Advertising Flags – Capture Attention Outdoors</h2>
  <p>
    Promote your brand with <strong>custom advertising flags</strong>. Our feather, teardrop, blade, and fully customized flags are perfect for outdoor marketing, events, and brand visibility. Made from durable materials, these flags are designed to withstand wind and weather while keeping your brand highly visible. Explore our <a href="/services/signs-banner/ad-flag">advertising flags</a>.
  </p>
  <ul>
    <li><strong>Feather Flags:</strong> Tall and aerodynamic, ideal for outdoor advertising.</li>
    <li><strong>Teardrop Flags:</strong> Eye-catching shape for events and promotions.</li>
    <li><strong>Blade Flags:</strong> Bold graphics for maximum visibility.</li>
    <li><strong>Custom Flags:</strong> Fully customizable to match your branding.</li>
  </ul>

  <h2>Easy Online Ordering & Customization</h2>
  <p>
    Creating your <strong>custom signs and banners</strong> online is simple with Gregbuk. Select your preferred material, size, and finish, then upload your artwork or use one of our <a href="/contact">professional templates</a>. Our platform provides instant pricing so you know your cost upfront. Receive your banners promptly with fast and reliable shipping.
  </p>

  <h2>Design Tips for Effective Signs & Banners</h2>
  <ul>
    <li><strong>Bold, Readable Text:</strong> Ensure visibility from a distance.</li>
    <li><strong>High-Contrast Colors:</strong> Make your message pop.</li>
    <li><strong>Brand Consistency:</strong> Use logos, fonts, and colors consistent with your brand.</li>
    <li><strong>High-Resolution Images:</strong> Maintain sharpness and professionalism.</li>
  </ul>

  <p>
    Start designing your <strong>custom signs and banners</strong> with Gregbuk today and make your brand unforgettable!
  </p>
  <a href="/contact" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Contact Us Now</strong></a>
            """,
            "subservices": [
                {
                    "name": "Banners",
                    "description": "High-quality banners for indoor and outdoor events, customized to your needs.",
                    "image_url": choice(imgg),
                    "category_name": "banner",
                    "products": [
                        {"name": "Vinyl Banner",
                         "description": "Durable and vibrant vinyl banners suitable for long-term display.",
                         "image_url": choice(imgg), "category_name": "vinyl", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Fabric Banner",
                         "description": "Premium fabric banners with a professional finish and soft texture.",
                         "image_url": choice(imgg), "category_name": "fabric", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Mesh Banners", "description": "Wind-resistant mesh banners ideal for outdoor use.",
                         "image_url": choice(imgg), "category_name": "mesh", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "X Banner Stands",
                         "description": "Portable X-frame banners perfect for trade shows and events.",
                         "image_url": choice(imgg), "category_name": "x-banner", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Step & Repeat Banners",
                         "description": "Custom step-and-repeat banners for photo backdrops and branding.",
                         "image_url": choice(imgg), "category_name": "step-repeat", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Pop Up Display",
                         "description": "Quick and easy pop-up banners for instant presentation setups.",
                         "image_url": choice(imgg), "category_name": "pop-up", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Tablecloths",
                         "description": "Branded table covers for events, trade shows, and promotions.",
                         "image_url": choice(imgg), "category_name": "tbc", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Table Runners",
                         "description": "Custom table runners to complement your branded setup.",
                         "image_url": choice(imgg), "category_name": "T-run", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Retractable Banner",
                    "description": "Portable retractable banners for professional marketing on the go.",
                    "image_url": choice(imgg),
                    "category_name": "retract-banner",
                    "products": [
                        {"name": "Retractable Banner",
                         "description": "Standard retractable banner for events and exhibitions.",
                         "image_url": choice(imgg), "category_name": "retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Premium Retractable Banner",
                         "description": "High-quality retractable banner with premium print and finish.",
                         "image_url": choice(imgg), "category_name": "premium-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Deluxe Retractable Banner",
                         "description": "Extra-large deluxe banners for maximum visibility.", "image_url": choice(imgg),
                         "category_name": "deluxe-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Professional Retractable Banner",
                         "description": "Designed for corporate use and high-visibility promotions.",
                         "image_url": choice(imgg), "category_name": "pro-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Black Retractable Banner",
                         "description": "Sleek black retractable banner for elegant event displays.",
                         "image_url": choice(imgg), "category_name": "black-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Double Sided Retractable Banner",
                         "description": "Displays your message on both sides for maximum exposure.",
                         "image_url": choice(imgg), "category_name": "dbs-retract", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Advertising Flags",
                    "description": "Promotional flags to capture attention outdoors and boost brand visibility.",
                    "image_url": choice(imgg),
                    "category_name": "ad-flag",
                    "products": [
                        {"name": "Feather Flags",
                         "description": "Tall, aerodynamic flags ideal for outdoor advertising.",
                         "image_url": choice(imgg), "category_name": "f-flags", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Teardrop Flags",
                         "description": "Eye-catching teardrop-shaped flags for promotions and events.",
                         "image_url": choice(imgg), "category_name": "t-flag", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Blade Flags",
                         "description": "Blade-style flags with bold graphics for maximum visibility.",
                         "image_url": choice(imgg), "category_name": "b-flag", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Custom Flags",
                         "description": "Fully customizable flags tailored to your branding requirements.",
                         "image_url": choice(imgg), "category_name": "c-flag", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        },
        {
            "name": "Seals & Stamps",
            "description": "Professional seals and stamps for authentication, branding, and official documents.",
            "image_url": choice(imgg),
            "icon_name": "#cil-check",
            "category_name": "seals-stamps",
            "content": """
            <h1>Custom Seals & Stamps – Gregbuk</h1>

  <h2>Professional Seals & Stamps for Branding and Authentication</h2>
  <p>
    Ensure authenticity, professionalism, and brand recognition with <strong>custom seals and stamps</strong> from Gregbuk. Perfect for official documents, company branding, and creative purposes, our high-quality products are designed to leave a lasting impression.
  </p>

  <h2>Custom Seals for Official Documents</h2>
  <p>
    Our <strong>seals</strong> are crafted for corporate, legal, and security applications. Choose from a variety of types to suit your needs, whether it’s for company documents, notary validation, or tamper-proof security. Every seal is designed for precision and durability, reflecting your professionalism.
  </p>
  <ul>
    <li><strong>Company Seals:</strong> Official seals for corporate certifications and documents. <a href="/services/seals-stamps/seals/company-seal">Learn more</a></li>
    <li><strong>Notary Seals:</strong> Validate legal documents with professional-grade notary seals. <a href="/services/seals-stamps/seals/notary-seal">Learn more</a></li>
    <li><strong>Embossed Seals:</strong> Elegant seals that provide a sophisticated, raised impression. <a href="/services/seals-stamps/seals/embossed-seal">Learn more</a></li>
    <li><strong>Holographic Seals:</strong> Secure your documents with holographic seals for authenticity. <a href="/services/seals-stamps/seals/holo-seal">Learn more</a></li>
    <li><strong>Tamper-Evident Seals:</strong> Designed to show any unauthorized access or opening. <a href="/services/seals-stamps/seals/te-seal">Learn more</a></li>
  </ul>

  <h2>Custom Stamps for Office & Branding</h2>
  <p>
    Gregbuk offers a wide range of <strong>stamps</strong> for office use, branding, and creative purposes. From signature and rubber stamps to self-inking and pre-inked options, our stamps are designed for efficiency, consistency, and professional presentation.
  </p>
  <ul>
    <li><strong>Signature Stamp:</strong> Convenient for signing documents quickly and consistently. <a href="/services/seals-stamps/stamps/signature-stamp">Learn more</a></li>
    <li><strong>Rubber Stamp:</strong> Traditional stamp for official marking and branding. <a href="/services/seals-stamps/stamps/rubber-stamp">Learn more</a></li>
    <li><strong>Self-Inking Stamp:</strong> Easy-to-use stamps ideal for repetitive applications. <a href="/services/seals-stamps/stamps/self-ink-stamp">Learn more</a></li>
    <li><strong>Pre-Ink Stamp:</strong> Pre-inked for crisp, clean impressions every time. <a href="/services/seals-stamps/stamps/pre-ink-stamp">Learn more</a></li>
    <li><strong>Date Stamp:</strong> Track, label, and date documents with precision. <a href="/services/seals-stamps/stamps/date-stamp">Learn more</a></li>
  </ul>

  <h2>Easy Online Customization & Ordering</h2>
  <p>
    Creating your <strong>custom seals and stamps</strong> online is simple. Select your type, material, and size, then upload your artwork or use one of our templates. Gregbuk provides instant pricing so you can see your total cost before ordering. Fast shipping ensures your products arrive promptly and ready for use.
  </p>

  <h2>Tips for Effective Seals & Stamps</h2>
  <ul>
    <li><strong>Clarity:</strong> Ensure text and logos are sharp and legible.</li>
    <li><strong>Brand Consistency:</strong> Use your company colors, logos, and fonts.</li>
    <li><strong>Quality Material:</strong> Select durable stamps and premium embossing for lasting impressions.</li>
    <li><strong>Placement:</strong> Apply strategically to documents, certificates, and packaging.</li>
  </ul>

  <p>
    Start designing your <strong>custom seals and stamps</strong> with Gregbuk today and elevate your professional image!
  </p>
  <a href="/contact" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Get Quote Now<strong></a> 
            """,
            "subservices": [
                {
                    "name": "Seals",
                    "description": "High-quality seals for official documents, company use, and security.",
                    "image_url": choice(imgg),
                    "category_name": "seals",
                    "products": [
                        {"name": "Company Seals",
                         "description": "Official seals for corporate documents and certifications.",
                         "image_url": choice(imgg), "category_name": "company-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Notary Seals",
                         "description": "Professional notary seals to validate legal documents.",
                         "image_url": choice(imgg), "category_name": "notary-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Embossed Seals", "description": "Elegant embossed seals for a sophisticated finish.",
                         "image_url": choice(imgg), "category_name": "embossed-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Holographic Seals",
                         "description": "Secure holographic seals for brand protection and authenticity.",
                         "image_url": choice(imgg), "category_name": "holo-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Tamper-Evident Seals",
                         "description": "Seals designed to show any unauthorized opening.", "image_url": choice(imgg),
                         "category_name": "te-seal", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Stamps",
                    "description": "Custom stamps for office, branding, and creative purposes.",
                    "image_url": choice(imgg),
                    "category_name": "stamps",
                    "products": [
                        {"name": "Signature Stamp",
                         "description": "Convenient stamps for signing documents efficiently.",
                         "image_url": choice(imgg), "category_name": "signature-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Rubber Stamp",
                         "description": "Traditional rubber stamps for official marking and branding.",
                         "image_url": choice(imgg), "category_name": "rubber-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Self-Inking Stamp",
                         "description": "Easy-to-use self-inking stamps for repetitive use.", "image_url": choice(imgg),
                         "category_name": "self-ink-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Pre-ink Stamp", "description": "Pre-inked stamps for crisp, consistent impressions.",
                         "image_url": choice(imgg), "category_name": "pre-ink-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Date Stamp",
                         "description": "Date stamps for tracking, labeling, or official documentation.",
                         "image_url": choice(imgg), "category_name": "date-stamp", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        },
        {
            "name": "Frames and Plaques",
            "description": "Decorative and functional frames and plaques for awards, photos, and displays.",
            "image_url": choice(imgg),
            "icon_name": "#cil-image",
            "category_name": "frame-plaques",
            "content": """
            <h1>Custom Frames & Plaques – Gregbuk</h1>

  <h2>Showcase Your Memories & Achievements with Style</h2>
  <p>
    Enhance your photos, awards, and displays with <strong>custom frames and plaques</strong> from Gregbuk. Whether for personal keepsakes, corporate recognition, or artistic presentation, our high-quality products ensure your memories and achievements are displayed beautifully.
  </p>

  <h2>High-Quality Frames for Every Occasion</h2>
  <p>
    Protect and showcase your artwork, photos, and certificates with our <strong>premium frames</strong>. Choose from a variety of materials and finishes to match your decor or brand style. Every frame is crafted to combine durability with elegance.
  </p>
  <ul>
    <li><strong>Wood Frames:</strong> Classic wooden frames in multiple finishes for a timeless, elegant look. <a href="/services/frame-plaques/frame/wood-frames">Learn more</a></li>
    <li><strong>Metal Frames:</strong> Sleek, modern frames that add a contemporary touch to any display. <a href="/services/frame-plaques/frame/metal-frames">Learn more</a></li>
    <li><strong>Plastic Frames:</strong> Affordable and versatile frames available in different colors and styles. <a href="/services/frame-plaques/frame/plastic-frames">Learn more</a></li>
    <li><strong>Glass Frames:</strong> Minimalist frames that offer a clean, sophisticated look for modern interiors. <a href="/services/frame-plaques/frame/glass-frames">Learn more</a></li>
  </ul>

  <h2>Custom Plaques for Recognition & Awards</h2>
  <p>
    Celebrate achievements and milestones with <strong>custom plaques</strong>. Ideal for corporate awards, special recognitions, or personal gifts, Gregbuk provides plaques in various materials and finishes to create memorable keepsakes.
  </p>
  <ul>
    <li><strong>Wood Plaques:</strong> Elegant wooden plaques perfect for awards and recognition. <a href="/services/frame-plaques/plaques/wood-plaques">Learn more</a></li>
    <li><strong>Metal Plaques:</strong> Durable and professional plaques for achievements and commemorations. <a href="/services/frame-plaques/plaques/metal-plaques">Learn more</a></li>
    <li><strong>Acrylic Plaques:</strong> Clear, modern plaques that combine sleek design with professional presentation. <a href="/services/frame-plaques/plaques/plastic-plaques">Learn more</a></li>
    <li><strong>Glass Plaques:</strong> Premium engraved glass plaques for special recognition and awards. <a href="/services/frame-plaques/plaques/glass-plaques">Learn more</a></li>
    <li><strong>Crystal Plaques:</strong> Luxury crystal plaques designed for top-tier awards and prestigious events. <a href="/services/frame-plaques/plaques/crystal-plaques">Learn more</a></li>
  </ul>

  <h2>Easy Online Customization & Ordering</h2>
  <p>
    Creating your <strong>custom frames and plaques</strong> online is simple. Choose your preferred material, size, and finish, then upload your artwork or certificate design. Gregbuk provides instant pricing so you can see your total cost before ordering. Fast and reliable shipping ensures your products arrive on time and ready for display.
  </p>

  <h2>Tips for Displaying Frames & Plaques</h2>
  <ul>
    <li><strong>Proper Placement:</strong> Highlight important photos or awards in prominent areas.</li>
    <li><strong>Matching Style:</strong> Choose frame or plaque styles that complement your decor or brand identity.</li>
    <li><strong>High-Quality Materials:</strong> Ensure your frames and plaques are durable and long-lasting.</li>
    <li><strong>Creative Customization:</strong> Add logos, engraving, or special finishes for a unique look.</li>
  </ul>

  <p>
    Start designing your <strong>custom frames and plaques</strong> with Gregbuk today and preserve your memories and achievements in style!
  </p>
  <a href="/contact" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Contact Us Now</strong></a> 
            """,
            "subservices": [
                {
                    "name": "Frame",
                    "description": "High-quality frames to protect and showcase your photos and artwork.",
                    "image_url": choice(imgg),
                    "category_name": "frame",
                    "products": [
                        {"name": "Wood Frame",
                         "description": "Classic wooden frames available in various finishes for elegant display.",
                         "image_url": choice(imgg), "category_name": "wood-frames", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Metal Frame", "description": "Modern metal frames offering sleek and durable design.",
                         "image_url": choice(imgg), "category_name": "metal-frames", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Plastic Frame",
                         "description": "Affordable plastic frames in multiple colors and styles.",
                         "image_url": choice(imgg), "category_name": "plastic-frames", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Glass Frame",
                         "description": "Glass frames with minimalistic design, perfect for modern interiors.",
                         "image_url": choice(imgg), "category_name": "glass-frames", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Plaques",
                    "description": "Custom plaques for awards, recognition, and corporate displays.",
                    "image_url": choice(imgg),
                    "category_name": "plaques",
                    "products": [
                        {"name": "Wood Plaques", "description": "Elegant wooden plaques for awards and recognitions.",
                         "image_url": choice(imgg), "category_name": "wood-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Metal Plaques",
                         "description": "Durable metal plaques for professional achievements and commemorations.",
                         "image_url": choice(imgg), "category_name": "metal-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Acrylic Plaques",
                         "description": "Clear acrylic plaques for modern award displays with a sleek finish.",
                         "image_url": choice(imgg), "category_name": "plastic-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Glass Plaques",
                         "description": "High-quality glass plaques with premium engraving for special recognition.",
                         "image_url": choice(imgg), "category_name": "glass-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Crystal Plaques",
                         "description": "Luxury crystal plaques for top-tier awards and prestigious events.",
                         "image_url": choice(imgg), "category_name": "crystal-plaques", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        }
    ]

    # Loop and insert
    for service_data in data:
        service = Services(
            name=service_data["name"],
            image_url=service_data["image_url"],
            category_name=service_data["category_name"],
            icon_name= service_data["icon_name"],
            description= service_data["description"],
            content=service_data["content"] if "content" in service_data else None
        )
        for sub_data in service_data.get("subservices", []):
            sub = SubService(
                name=sub_data["name"],
                image_url=sub_data["image_url"],
                category_name=sub_data["category_name"],
                services=service,
                description=sub_data["description"],
                content=service_data["content"] if "content" in sub_data else None
            )
            # Products under SubService
            for prod_data in sub_data.get("products", []):
                product = Products(
                    name=prod_data["name"],
                    image_url=prod_data["image_url"],
                    category_name=prod_data["category_name"],
                    subservice=sub,
                    description=prod_data["description"],
                    content=service_data["content"] if "content" in prod_data else None
                )
                for prod_image in prod_data.get("image_collection", []):
                    collection = ProductCollection(
                        image_collections=prod_image,
                        product=product
                    )
                    db.session.add(collection)
                db.session.add(product)
            db.session.add(sub) # Products directly under Service
        for prod_data in service_data.get("products", []):
            product = Products(
                name=prod_data["name"],
                image_url=prod_data["image_url"],
                category_name=prod_data["category_name"],
                services=service,
                description=prod_data["description"],
                content=service_data["content"] if "content" in prod_data else None
            )
            for prod_image in prod_data.get("image_collection", []):
                collection = ProductCollection(
                    image_collections=prod_image,
                    product=product
                )
                db.session.add(collection)
            db.session.add(product)
        db.session.add(service)

    db.session.commit()

    head = [
        {
            "name": "Home",
            "end_url": "home",
        },
        {
            "name": "Service",
            "end_url": "home"
        },
        {
            "name": "Bulk SMS",
            "end_url": "bulk_sms"
        },
        {
            "name": "Pricing",
            "end_url": "pricing"
        },
        {
            "name": "Contact Us",
            "end_url": "contact"
        },
        {
            "name": "About Us",
            "end_url": "about_us"
        }

    ]
    for hh in head:
        da = Header(
            name= hh["name"],
            end_url= hh["end_url"]
        )
        db.session.add(da)

    db.session.commit()

