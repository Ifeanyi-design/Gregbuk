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
            "name": "Cards",
            "description": "All card types including business, ID, loyalty, and appointment cards.",
            "category_name": "Cards",
            "image_url": "cards.jpeg",
            "icon_name": "#cil-credit-card",
            "alt_texts": "Card service image",
            "content": """
<h1>Custom Card Printing Services with Gregbuk</h1>

<h2>Versatile Cards for Every Need</h2>
<p>
At <strong>Gregbuk</strong>, we provide high-quality card printing solutions tailored to your brand, business, or personal needs.
From professional <strong>business cards</strong> to secure <strong>ID cards</strong>, practical <strong>appointment cards</strong>, and customer-friendly <strong>loyalty cards</strong>, we’ve got you covered.
Each card is crafted with precision to leave a lasting impression.
</p>

<h2>Wide Range of Options</h2>
<p>
No matter your industry or style, Gregbuk offers a variety of card types and finishes to suit your requirements:
</p>
<ul>
  <li><strong>Business Cards:</strong> Make a strong first impression with premium finishes and styles — <a href="/services/Cards/Business-Cards">Explore Business Cards</a></li>
  <li><strong>ID Cards:</strong> Durable PVC and plastic ID cards with professional printing and security options — <a href="/services/Cards/id-cards">Explore ID Cards</a></li>
  <li><strong>Loyalty Cards:</strong> Build customer loyalty with personalized rewards cards — <a href="/services/Cards/loyalty">Explore Loyalty Cards</a></li>
  <li><strong>Appointment Cards:</strong> Help clients stay organized with practical appointment reminders — <a href="/services/Cards/appointment">Explore Appointment Cards</a></li>
  <li><strong>Specialty Cards:</strong> Ultra-thick, foil-stamped, or textured cards for a premium look and feel — <a href="/services/Cards/specialty">Explore Specialty Cards</a></li>
</ul>

<h2>Premium Materials & Finishes</h2>
<p>
Choose from a wide range of paper stocks and finishes, including <strong>matte</strong>, <strong>glossy</strong>, <strong>soft-touch coatings</strong>, and <strong>metallic foils</strong>. 
Each option is designed to match your brand identity and make your cards durable, stylish, and professional.
</p>

<h2>Why Choose Gregbuk?</h2>
<ul>
  <li>Fast turnaround and reliable delivery</li>
  <li>Flexible quantities, from small batches to bulk orders</li>
  <li>Easy online customization with templates</li>
  <li>High-quality printing for sharp graphics and vibrant colors</li>
</ul>

<h2>Order Your Custom Cards Today</h2>
<p>
Take your brand to the next level with Gregbuk’s <strong>custom card printing services</strong>. 
Design, customize, and order online in just a few clicks. 
From professional networking to customer engagement, our cards help you stand out. 
<a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Get a Quote Now</strong></a>
</p>
""",
            "subservices": [
            {
                "name": "Business Cards",
                "description": "High-quality business cards that make a lasting first impression, available in a variety of finishes and styles.",
                "image_url": "business_card.jpeg",
                "category_name": "Business-Cards",
                "alt_texts": "Business Card service image",
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
        Take your networking and branding to the next level with Gregbuk <strong>custom business cards</strong>. Design online, select your preferred finish, and receive high-quality, durable cards that leave a lasting impression. <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Get Quote now</strong></a>!
      </p>
                """,
                "products": [
                    {"name": "Glossy Card",
                     "description": "Premium glossy finish for vibrant colors and a professional look.",
                     "image_url": "Glossy.webp", "content": """
                     <h2>Glossy Business Cards – Vibrant Shine That Stands Out</h2>

  <p>
    Capture attention instantly with our premium <strong>glossy business cards</strong>. 
    The high-shine finish enhances colors, adds depth, and makes every detail pop, 
    ensuring your brand leaves a bold and professional impression.
  </p>

  <h2>Why Choose Glossy Business Cards?</h2>
  <ul>
    <li><strong>Vivid Colors:</strong> The glossy coating makes colors appear brighter and more striking.</li>
    <li><strong>Smooth Finish:</strong> Sleek texture that feels polished and premium.</li>
    <li><strong>Durable Quality:</strong> Protected surface resists scratches and everyday wear.</li>
    <li><strong>Affordable Luxury:</strong> Premium look at a competitive price.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Glossy cards are ideal for creatives, photographers, real estate professionals, 
    and anyone looking to make a strong first impression. Whether at trade shows, 
    meetings, or events, these cards stand out every time.
  </p>

  <h2>Order Glossy Business Cards Today</h2>
  <p>
    Upgrade your networking with <strong>custom glossy business cards</strong> from Gregbuk. 
    Easy to design, fast to print, and guaranteed to impress.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Get a Quote Now</strong>
    </a>
  </p>
                     """, "alt_texts": "Glossy Card \u2014 professional mockup for product listing.", "category_name": "glossy", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Matte Card",
                     "description": "Smooth, non-reflective finish for a sophisticated and elegant appearance.",
                     "image_url": "Matte.webp", "content": """
                     <h2>Matte Business Cards – Sleek, Modern, and Professional</h2>

  <p>
    Achieve a sophisticated look with our <strong>matte business cards</strong>. 
    The smooth, non-reflective finish gives your design an elegant appearance, 
    making text and graphics easy to read while maintaining a premium feel.
  </p>

  <h2>Why Choose Matte Business Cards?</h2>
  <ul>
    <li><strong>Elegant Finish:</strong> Soft and smooth surface without glare.</li>
    <li><strong>Readable Design:</strong> Ideal for cards with text-heavy layouts or fine details.</li>
    <li><strong>Durable Quality:</strong> Resistant to fingerprints and smudges.</li>
    <li><strong>Timeless Appeal:</strong> Minimalist style that works for any industry.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Matte cards are perfect for professionals in law, finance, consulting, and corporate industries. 
    They’re also a favorite for anyone who prefers subtle elegance over shine.
  </p>

  <h2>Order Matte Business Cards Today</h2>
  <p>
    Elevate your brand with <strong>custom matte business cards</strong> from Gregbuk.  
    Stylish, refined, and printed to perfection.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Get a Quote Now</strong>
    </a>
  </p>
                     """, "alt_texts": "Matte Card \u2014 close-up showing print detail and finish.", "category_name": "matte", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Standard Card",
                     "description": "Classic and versatile business card perfect for any professional need.",
                     "image_url": "standard_card.jpeg", "content": """
                     <h2>Standard Business Cards – Classic, Reliable, and Affordable</h2>

  <p>
    Keep it simple and effective with our <strong>standard business cards</strong>.  
    Designed to balance quality and affordability, these cards give you a professional presence without breaking the budget.
  </p>

  <h2>Why Choose Standard Business Cards?</h2>
  <ul>
    <li><strong>Cost-Effective:</strong> Perfect for startups and small businesses.</li>
    <li><strong>Professional Design:</strong> Clean and straightforward for everyday networking.</li>
    <li><strong>Quick Printing:</strong> Fast turnaround for urgent needs.</li>
    <li><strong>Customizable:</strong> Add your logo, colors, and text to reflect your brand.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Standard cards are ideal for entrepreneurs, freelancers, students, or anyone needing a simple, professional introduction tool.
  </p>

  <h2>Order Standard Business Cards Today</h2>
  <p>
    Make a lasting first impression with <strong>custom standard business cards</strong> from Gregbuk.  
    Affordable, professional, and always reliable.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Request a Quote</strong>
    </a>
  </p>
                     """, "alt_texts": "Standard Business Card \u2014 detail shot highlighting craftsmanship.", "category_name": "standard", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Square Card",
                     "description": "Modern square shape that stands out from traditional business cards.",
                     "image_url": "square_business_card.jpeg", "content": """
                     <h2>Premium Business Cards – Elevate Your First Impression</h2>

  <p>
    Showcase your professionalism with <strong>premium business cards</strong>.  
    Designed with superior materials and finishes, these cards help your brand stand out with elegance and durability.
  </p>

  <h2>Why Choose Premium Business Cards?</h2>
  <ul>
    <li><strong>High-Quality Materials:</strong> Thicker cardstock for a luxurious feel.</li>
    <li><strong>Premium Finishes:</strong> Options like matte, silk, velvet, or gloss to enhance your brand.</li>
    <li><strong>Durability:</strong> Long-lasting quality to keep your contacts impressed.</li>
    <li><strong>Custom Features:</strong> Embossing, foil stamping, and more for unique designs.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Premium cards are ideal for executives, corporate professionals, and brands that want to leave a lasting impression.
  </p>

  <h2>Order Premium Business Cards Today</h2>
  <p>
    Upgrade your networking game with <strong>custom premium business cards</strong> from Gregbuk.  
    Stylish, professional, and unforgettable.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Request a Quote</strong>
    </a>
  </p>
                     """, "alt_texts": "Square Business Card \u2014 angled view showing texture and edges.", "category_name": "square", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Rounded Corner Card",
                     "description": "Elegant rounded edges for a sleek, premium finish.", "image_url": "rounded_business_card.jpeg",
                     "category_name": "rounded-corner", "content": """
                     <h2>Glossy Business Cards – Shine with Every Handshake</h2>

  <p>
    Add brilliance to your networking with <strong>glossy business cards</strong>.  
    Featuring a polished finish that makes colors pop, these cards grab attention instantly and leave a memorable impact.
  </p>

  <h2>Why Choose Glossy Business Cards?</h2>
  <ul>
    <li><strong>Vibrant Look:</strong> High-gloss finish enhances images, logos, and designs.</li>
    <li><strong>Durable Coating:</strong> Resistant to smudges and daily wear.</li>
    <li><strong>Eye-Catching Appeal:</strong> Ideal for bold designs and creative brands.</li>
    <li><strong>Professional Finish:</strong> Adds shine without compromising readability.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Glossy cards are ideal for creatives, entrepreneurs, and businesses that want a modern, vibrant, and standout look.
  </p>

  <h2>Order Glossy Business Cards Today</h2>
  <p>
    Make your brand unforgettable with <strong>custom glossy business cards</strong> from Gregbuk.  
    Bold, colorful, and striking – the perfect way to introduce yourself.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Get a Quote Now</strong>
    </a>
  </p>
                     """, "alt_texts": "Rounded Corner Business Card \u2014 close-up showing print detail and finish.", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Ultra Thick Card",
                     "description": "Extra thick cardstock for a luxury feel and durability.", "image_url": "ultra_thick_card.png",
                     "category_name": "ultra-thick", "content": """
                     <div class="special-text" bis_skin_checked="1">
  <h2>Ultra Thick Business Cards – Bold, Sturdy, and Luxurious</h2>

  <p>
    Stand out instantly with <strong>ultra thick business cards</strong>.  
    Made with premium extra-thick cardstock, these cards deliver a bold statement of quality, strength, and luxury in every handshake.
  </p>

  <h2>Why Choose Ultra Thick Business Cards?</h2>
  <ul>
    <li><strong>Luxury Feel:</strong> Extra-thick cardstock adds prestige and weight.</li>
    <li><strong>Durability:</strong> Resistant to bending, creasing, and everyday wear.</li>
    <li><strong>Premium Branding:</strong> Instantly communicates high value and professionalism.</li>
    <li><strong>Customizable:</strong> Works beautifully with embossing, foil, and specialty finishes.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Ideal for luxury brands, real estate agents, consultants, executives, and creatives who want to make a lasting impression.
  </p>

  <h2>Order Ultra Thick Business Cards Today</h2>
  <p>
    Leave a powerful impression with <strong>custom ultra thick business cards</strong> from Gregbuk.  
    Strong, sleek, and unforgettable – your brand deserves the best.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Get a Quote Now</strong>
    </a>
  </p>
                     """, "alt_texts": "Ultra Thick Business Card \u2014 professional mockup for product listing.", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Foil Card",
                     "description": "Unique textured or specialty paper to leave a memorable impression.",
                     "image_url": "foil_business_card.webp", "content": """
                     <h2>Foil Business Cards – Shine, Elegance, and Lasting Impressions</h2>

  <p>
    Elevate your brand with <strong>foil-stamped business cards</strong>.  
    Featuring eye-catching metallic finishes, these cards shimmer under the light, giving your brand a touch of luxury and exclusivity.
  </p>

  <h2>Why Choose Foil Business Cards?</h2>
  <ul>
    <li><strong>Premium Look:</strong> Metallic foil adds elegance and sophistication.</li>
    <li><strong>Custom Finishes:</strong> Choose from gold, silver, rose gold, or custom colors.</li>
    <li><strong>Tactile Appeal:</strong> Foil stamping provides a texture that people can feel.</li>
    <li><strong>High Impact:</strong> Perfect for designs with logos, names, or accents that need to stand out.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Luxury brands, beauty professionals, fashion designers, consultants, and event planners who want to sparkle in every interaction.
  </p>

  <h2>Order Foil Business Cards Today</h2>
  <p>
    Make every introduction unforgettable with <strong>custom foil business cards</strong> from Gregbuk.  
    Stylish, professional, and built to impress.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Get a Quote Now</strong>
    </a>
  </p>
                     """, "alt_texts": "Foil Business Card \u2014 detail shot highlighting craftsmanship.", "category_name": "foil-card", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Loyalty Card", "description": "Customizable loyalty cards to reward your best customers.",
                     "image_url": "LoyaltyCard.jpeg", "content": """
                     <h2>Loyalty Cards – Reward Your Customers and Build Lasting Relationships</h2>

  <p>
    Keep customers coming back with <strong>custom loyalty cards</strong>.  
    Designed to reward frequent visits or purchases, these cards strengthen customer engagement and brand loyalty while offering a professional touch.
  </p>

  <h2>Why Choose Loyalty Cards?</h2>
  <ul>
    <li><strong>Customer Retention:</strong> Encourage repeat business with reward programs.</li>
    <li><strong>Customizable:</strong> Add your brand logo, colors, and unique reward structure.</li>
    <li><strong>Durable Printing:</strong> High-quality cardstock ensures your cards last.</li>
    <li><strong>Flexible Uses:</strong> Perfect for restaurants, salons, gyms, retail shops, and more.</li>
  </ul>

  <h2>Boost Your Brand</h2>
  <p>
    Loyalty cards not only reward customers but also promote your brand every time they’re used.  
    Whether stamped, signed, or digitally tracked, they’re a simple way to add value to every visit.
  </p>

  <h2>Order Custom Loyalty Cards Today</h2>
  <p>
    Show appreciation to your customers with <strong>personalized loyalty cards</strong> from Gregbuk.  
    Affordable, practical, and effective for business growth.  
    <a href="/contact?head=Cards" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
      <strong>Get a Quote Now</strong>
    </a>
  </p>
                     """, "alt_texts": "Loyalty Card \u2014 in-use photo demonstrating scale.", "category_name": "loyalty", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Appointment Card",
                     "description": "Practical cards for scheduling appointments and keeping clients organized.",
                     "image_url": "AppointmentCard.jpeg", "content": """
                     <h2>Custom Appointment Cards – Keep Your Clients on Schedule</h2>

  <p>Help your customers stay organized with professional <strong>custom appointment cards</strong>. Ideal for salons, clinics, offices, and service providers, these cards are a practical tool that doubles as a reminder of your brand. Durable, portable, and easy to customize, our <strong>appointment card printing</strong> ensures your business stays top of mind.</p>

  <h2>Why Choose Our Appointment Cards?</h2>
  <ul>
    <li><strong>Durable Cardstock:</strong> Printed on quality material that lasts in wallets and purses.</li>
    <li><strong>Custom Design:</strong> Add your logo, business info, and scheduling details for a professional look.</li>
    <li><strong>Versatile Use:</strong> Perfect for doctors, salons, spas, consultants, and any appointment-driven business.</li>
    <li><strong>Brand Visibility:</strong> Each appointment card doubles as a subtle business card to promote your services.</li>
  </ul>

  <h2>Simple and Effective Marketing Tool</h2>
  <p>Appointment cards do more than just remind clients of their schedule — they strengthen your professional image. Every time a customer checks their upcoming appointment, they see your brand, building trust and recognition.</p>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Order Your Custom Appointment Card
  </a>
                     """, "alt_texts": "Appointment Card \u2014 in-use photo demonstrating scale.", "category_name": "appointment", "image_collection": [choice(imgg) for n in range(8)]},
                    {"name": "Complementary Card", "description": "Small, elegant cards to accompany gifts or services.",
                     "image_url": "complementary_card.jpeg", "content": """
                     <h2>Custom Complementary Cards – Add a Touch of Elegance to Every Gift</h2>

  <p>Make your services and gifts unforgettable with beautifully designed <strong>custom complementary cards</strong>. Whether slipped into packaging, attached to a bouquet, or included with a gift, these small cards carry a big impact. They’re the perfect way to express appreciation, promote your brand, or leave a thoughtful note.</p>

  <h2>Why Choose Our Complementary Cards?</h2>
  <ul>
    <li><strong>Compact & Elegant:</strong> Small format that enhances gifts without overwhelming them.</li>
    <li><strong>Customizable Designs:</strong> Add your logo, message, or brand colors for a personal touch.</li>
    <li><strong>Premium Print Quality:</strong> Crisp text and vibrant colors for a professional finish.</li>
    <li><strong>Versatile Use:</strong> Perfect for retail stores, corporate gifts, events, and hospitality businesses.</li>
  </ul>

  <h2>A Memorable Detail That Builds Loyalty</h2>
  <p>Sometimes, it’s the smallest details that make the biggest impression. Complementary cards are a subtle yet effective way to show thoughtfulness, reinforce your brand identity, and strengthen relationships with clients or loved ones.</p>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Order Your Custom Complementary Card
  </a>
                     """, "alt_texts": "Complementary Card \u2014 in-use photo demonstrating scale.", "category_name": "complementary", "image_collection": [choice(imgg) for n in range(8)]}
                ]
            },
            {
              "name": "ID Cards",
              "description": "Plastic and PVC ID cards with photo and security features.",
              "category_name": "id-cards",
              "image_url": "id_cards.jpeg",
              "alt_texts": "ID Card service image",
              "content": """
              <h2>ID Cards Printing</h2>
  <p>
    Professional plastic and PVC ID cards designed with durability and style in mind.  
    Whether you need staff IDs, student IDs, access control, or visitor badges,  
    our high-quality prints ensure security and branding go hand-in-hand.  
  </p>

  <h3>Our ID Card Options</h3>
  <ul>
    <li><strong>PVC ID Cards:</strong> Sturdy and laminated for long-term use.</li>
    <li><strong>Lanyard ID Packs:</strong> ID cards paired with branded lanyards for a complete professional look.</li>
    <li><strong>Access Control Cards:</strong> Compatible with access control systems for security needs.</li>
    <li><strong>Visitor ID Cards:</strong> Temporary visitor badges, clear and reliable.</li>
  </ul>

  <h3>Why Choose Our ID Cards?</h3>
  <ul>
    <li>Durable PVC and plastic materials with premium finish</li>
    <li>Customizable with photos, logos, and security features</li>
    <li>Perfect for businesses, schools, and organizations</li>
    <li>Fast turnaround and professional quality</li>
  </ul>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Get a Quote
  </a>
              """,
              "products": [
                {
                  "name": "PVC ID Cards",
                  "description": "Durable PVC ID cards with lamination.",
                  "category_name": "pvc-id-cards",
                  "image_collection": [choice(imgg) for n in range(8)],
                  "image_url": "pvcCard.jpeg",
                  "content": """
                  <h2>Durable PVC ID Cards – Professional Identity Solutions</h2>

  <p>
    Our <strong>PVC ID cards</strong> are designed for long-lasting durability and a professional look.  
    Ideal for schools, businesses, events, and organizations, these cards combine functionality with brand identity.  
    Each card is printed with precision, ensuring clear photos, sharp text, and vibrant logos.
  </p>

  <h2>Features of PVC ID Cards</h2>
  <ul>
    <li><strong>Strong & Durable:</strong> Made from high-quality PVC material that resists wear and tear.</li>
    <li><strong>Customizable:</strong> Add photos, barcodes, QR codes, or magnetic stripes for security and convenience.</li>
    <li><strong>Professional Appearance:</strong> Glossy or matte finishes available to match your branding.</li>
    <li><strong>Secure Options:</strong> Incorporate holograms, signatures, or chip technology for extra protection.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Whether you’re issuing staff IDs, student IDs, membership cards, or access badges, PVC ID cards are the  
    go-to choice for reliable identity verification and a polished brand image.
  </p>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Get Your Custom PVC ID Cards
  </a>
                  """,
                  "alt_texts": choice([
                    "PVC ID Cards \u2014 product shot on white background.",
                    "PVC ID Cards \u2014 close-up showing print detail and finish.",
                    "PVC ID Cards \u2014 styled mockup with props for context.",
                    "PVC ID Cards \u2014 angled view showing texture and edges.",
                    "PVC ID Cards \u2014 stack of multiple items showing variety.",
                    "PVC ID Cards \u2014 in-use photo demonstrating scale.",
                    "PVC ID Cards \u2014 detail shot highlighting craftsmanship.",
                    "PVC ID Cards \u2014 professional mockup for product listing."
                  ])
                },
                {
                  "name": "Lanyard ID Packs",
                  "description": "ID cards paired with branded lanyards.",
                  "category_name": "lanyard-id-packs",
                  "image_url": "lanyard.jpeg",
                  "content": """
                  <h2>Lanyard ID Packs – Complete Identification Solution</h2>

  <p>
    Combine style and convenience with our <strong>Lanyard ID Packs</strong>.  
    Each pack includes a high-quality ID card paired with a branded lanyard, providing a professional and practical solution for staff, students, or event attendees.
  </p>

  <h2>Features of Lanyard ID Packs</h2>
  <ul>
    <li><strong>Ready-to-Use Packs:</strong> ID cards and matching lanyards delivered together for instant deployment.</li>
    <li><strong>Customizable:</strong> Include your organization’s logo, colors, and branding on both cards and lanyards.</li>
    <li><strong>Comfortable & Durable:</strong> Soft, strong lanyards designed for everyday wear.</li>
    <li><strong>Professional Look:</strong> Elevate your team’s appearance at work, events, or conferences.</li>
  </ul>

  <h2>Perfect For</h2>
  <p>
    Ideal for corporate offices, schools, universities, events, and membership programs. Lanyard ID packs ensure identification is visible, secure, and stylish.
  </p>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Order Your Lanyard ID Packs
  </a>
                  """,
                  "image_collection": [choice(imgg) for n in range(8)],
                  "alt_texts": choice([
                    "Lanyard ID Packs \u2014 product shot on white background.",
                    "Lanyard ID Packs \u2014 close-up showing print detail and finish.",
                    "Lanyard ID Packs \u2014 styled mockup with props for context.",
                    "Lanyard ID Packs \u2014 angled view showing texture and edges.",
                    "Lanyard ID Packs \u2014 stack of multiple items showing variety.",
                    "Lanyard ID Packs \u2014 in-use photo demonstrating scale.",
                    "Lanyard ID Packs \u2014 detail shot highlighting craftsmanship.",
                    "Lanyard ID Packs \u2014 professional mockup for product listing."
                  ])
                },
                {
                  "name": "Access Control Cards",
                  "description": "Cards compatible with access control systems.",
                  "category_name": "access-control-cards",
                  "image_url": "access_control.jpeg",
                  "content": """
                  <h2>Access Control Cards – Secure & Reliable Identification</h2>

  <p>
    Ensure safety and efficiency with our <strong>Access Control Cards</strong>.  
    Designed for seamless integration with access control systems, these cards provide secure entry while maintaining a professional look for your staff or members.
  </p>

  <h2>Features of Access Control Cards</h2>
  <ul>
    <li><strong>High Security:</strong> Compatible with most access control systems for reliable entry management.</li>
    <li><strong>Durable Material:</strong> Long-lasting PVC cards built to withstand daily use.</li>
    <li><strong>Customizable Design:</strong> Include logos, colors, and personalization for your organization.</li>
    <li><strong>Professional Appearance:</strong> Maintains a polished, corporate look for staff or members.</li>
  </ul>

  <h2>Ideal For</h2>
  <p>
    Perfect for offices, restricted areas, gyms, educational institutions, or any facility requiring controlled access.  
    Combine security and style in one simple card.
  </p>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Order Your Access Control Cards
  </a>
                  """,
                  "image_collection": [choice(imgg) for n in range(8)],
                  "alt_texts": choice([
                    "Access Control Cards \u2014 product shot on white background.",
                    "Access Control Cards \u2014 close-up showing print detail and finish.",
                    "Access Control Cards \u2014 styled mockup with props for context.",
                    "Access Control Cards \u2014 angled view showing texture and edges.",
                    "Access Control Cards \u2014 stack of multiple items showing variety.",
                    "Access Control Cards \u2014 in-use photo demonstrating scale.",
                    "Access Control Cards \u2014 detail shot highlighting craftsmanship.",
                    "Access Control Cards \u2014 professional mockup for product listing."
                  ])
                },
                {
                  "name": "Visitor ID Cards",
                  "description": "Temporary visitor ID badges.",
                  "category_name": "visitor-id-cards",
                  "image_url": "visitors_card.jpeg",
                  "content": """
                  <h2>Visitor ID Cards – Temporary Access with Professional Style</h2>

  <p>
    Keep your facility safe and organized with our <strong>Visitor ID Cards</strong>.  
    Perfect for offices, events, schools, or any environment where temporary identification is required.
  </p>

  <h2>Features of Visitor ID Cards</h2>
  <ul>
    <li><strong>Temporary & Convenient:</strong> Easy-to-issue cards for visitors without compromising security.</li>
    <li><strong>Durable Material:</strong> Sturdy PVC cards that remain intact throughout the visit.</li>
    <li><strong>Customizable Design:</strong> Include your organization’s logo, visitor name, and relevant details.</li>
    <li><strong>Professional Look:</strong> Maintain a polished appearance while identifying visitors clearly.</li>
  </ul>

  <h2>Ideal For</h2>
  <p>
    Suitable for corporate offices, schools, events, and other facilities where visitor management and security are essential.  
    Enhance your check-in process with professional, easy-to-use visitor badges.
  </p>

  <a href="/contact?head=Cards" class="btn btn-primary">
    Order Your Visitor ID Cards
  </a>
                  """,
                  "image_collection": [choice(imgg) for n in range(8)],
                  "alt_texts": choice([
                    "Visitor ID Cards \u2014 product shot on white background.",
                    "Visitor ID Cards \u2014 close-up showing print detail and finish.",
                    "Visitor ID Cards \u2014 styled mockup with props for context.",
                    "Visitor ID Cards \u2014 angled view showing texture and edges.",
                    "Visitor ID Cards \u2014 stack of multiple items showing variety.",
                    "Visitor ID Cards \u2014 in-use photo demonstrating scale.",
                    "Visitor ID Cards \u2014 detail shot highlighting craftsmanship.",
                    "Visitor ID Cards \u2014 professional mockup for product listing."
                  ])
                }
              ]
            }
            ]
        },
        {
            "name": "Marketing Essentials",
            "description": "Comprehensive marketing materials to promote your business and engage your audience.",
            "image_url": "marketing-essentials.jpeg",
            "icon_name": "#cil-bullhorn",
            "alt_texts": "Marketing Essentials Service image",
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
    📞 <a class="btn btn-outline-primary rounded-pill border border-2 border-primary" href="/contact?head=Marketing"><strong>Get started today</strong></a> – contact our
    expert team to discuss your project. Let’s create marketing essentials that work for your brand.
</p>
""",
            "subservices": [
                {
                    "name": "Flyers & Brochures",
                    "description": "Eye-catching flyers and brochures to advertise your products and services effectively.",
                    "image_url": "flyers&brochures.jpeg",
                    "category_name": "flyers-and-brochures",
                    "alt_texts": "Flyers & Brochures service images",
                    "content": """
                    <h2>Flyers & Brochures Printing</h2>
  <p>
    Make a lasting impression with professionally designed flyers and brochures.  
    Perfect for advertising, promotions, and business presentations, our high-quality prints  
    are designed to grab attention and communicate your message effectively.
  </p>

  <h3>Our Flyer & Brochure Options</h3>
  <ul>
    <li><strong>Flyers:</strong> Single-page, full-color flyers for quick promotions or events.</li>
    <li><strong>Event Flyers:</strong> Vibrant designs tailored for concerts, parties, and special events.</li>
    <li><strong>Brochures:</strong> Informative layouts to showcase your business offerings in detail.</li>
    <li><strong>Tri-Fold Brochures:</strong> Compact and professional, ideal for trade shows and presentations.</li>
    <li><strong>Z-Fold Brochures:</strong> Creative fold-out style that presents information in a unique way.</li>
  </ul>

  <h3>Why Print with Us?</h3>
  <ul>
    <li>Premium quality paper and vibrant full-color printing</li>
    <li>Custom sizes and finishes to suit your brand</li>
    <li>Fast turnaround for urgent promotions and events</li>
    <li>Affordable pricing with professional results</li>
  </ul>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get a Quote
  </a>
                    """,
                    "products": [
                        {"name": "Flyers",
                         "description": "Single-page, full-color flyers for quick promotions or events.",
                         "image_url": "flyers.jpeg", "content": """
                         <h2>Custom Flyers – Make Every Promotion Count</h2>

  <p>
    Capture attention instantly with <strong>professionally designed flyers</strong> that elevate your brand.  
    Whether promoting events, products, or services, our flyers combine vibrant colors, crisp details, and premium finishes for maximum impact.
  </p>

  <h3>Why Our Flyers Stand Out</h3>
  <ul>
    <li><strong>Vibrant, Full-Color Printing:</strong> Colors that pop and make your message unforgettable.</li>
    <li><strong>Flexible Sizes & Formats:</strong> Standard or custom dimensions to suit any marketing campaign.</li>
    <li><strong>Premium Paper & Finishes:</strong> Choose from glossy, matte, or textured stocks for a professional touch.</li>
    <li><strong>Quick Turnaround:</strong> Get high-quality flyers fast to meet your deadlines.</li>
    <li><strong>Eco-Friendly Options:</strong> Sustainable paper choices for environmentally conscious promotions.</li>
  </ul>

  <h3>Perfect For:</h3>
  <p>
    Businesses, event organizers, non-profits, and educators aiming to communicate effectively.  
    Ideal for handouts, mailers, or local distribution to reach your audience with style and clarity.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Order Your Custom Flyers Today
  </a>
                         """, "alt_texts": "Flyers \u2014 professional mockup for product listing.", "category_name": "flyer", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Event Flyers",
                         "description": "Vibrant, energetic flyers designed for incredible events promotions.",
                         "image_url": "eventflyer.jpg", "content": """
                         <h2>Event Flyers – Promote Your Event with Impact</h2>

  <p>
    Make your event impossible to ignore with <strong>vibrant, professionally printed event flyers</strong>.  
    Designed to grab attention, communicate details clearly, and generate excitement, our flyers help you fill seats and engage your audience.
  </p>

  <h3>Why Choose Our Event Flyers</h3>
  <ul>
    <li><strong>Eye-Catching Designs:</strong> Bold visuals and colors that instantly draw attention.</li>
    <li><strong>Custom Sizes & Layouts:</strong> Tailored to fit your event’s branding and marketing strategy.</li>
    <li><strong>High-Quality Materials:</strong> Glossy, matte, or textured finishes for a premium feel.</li>
    <li><strong>Quick Turnaround:</strong> Fast, reliable printing to meet tight schedules.</li>
    <li><strong>Perfect for All Events:</strong> Concerts, workshops, parties, conferences, and more.</li>
  </ul>

  <h3>Reach Your Audience Effectively</h3>
  <p>
    Whether distributed at venues, mailed to attendees, or shared locally, our event flyers make your event look professional, exciting, and can help maximize attendance.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Create Your Event Flyers Today
  </a>
                         """, "alt_texts": "Event Flyers \u2014 professional mockup for product listing.", "category_name": "event-flyer", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Brochures",
                         "description": "Informative brochures to showcase your business offerings in detail.",
                         "image_url": "Brochures.jpeg", "content": """
                         <h2>Brochures – Tell Your Brand’s Story</h2>

  <p>
    Present your products, services, and company information with <strong>high-quality printed brochures</strong> designed to impress.  
    Our brochures help you communicate clearly, professionally, and leave a lasting impact on your audience.
  </p>

  <h3>Why Choose Our Brochures</h3>
  <ul>
    <li><strong>Custom Designs:</strong> Tailored layouts to reflect your brand identity.</li>
    <li><strong>Variety of Sizes & Formats:</strong> Single-page, bi-fold, tri-fold, or Z-fold to suit your messaging needs.</li>
    <li><strong>Premium Paper & Finishes:</strong> Glossy, matte, or textured options for a polished look.</li>
    <li><strong>Attention-Grabbing Visuals:</strong> Full-color printing that highlights your products and services.</li>
    <li><strong>Ideal for Marketing & Events:</strong> Perfect for trade shows, conferences, or client presentations.</li>
  </ul>

  <h3>Make a Strong Impression</h3>
  <p>
    Whether distributed in person, mailed to prospects, or used at events, our brochures ensure your business looks professional and memorable.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get Your Brochures Printed Today
  </a>
                         """, "alt_texts": "Brochures \u2014 detail shot highlighting craftsmanship.", "category_name": "brochures", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Tri-Fold Brochures",
                         "description": "Compact tri-fold brochures perfect for trade shows and presentations.",
                         "image_url": "tri-fold.jpg", "content": """
                         <h2>Tri-Fold Brochures – Professional & Versatile</h2>

  <p>
    Make your message easy to digest with our <strong>tri-fold brochures</strong>.  
    Perfect for trade shows, presentations, and promotional campaigns, these brochures organize information neatly while maintaining a professional appearance.
  </p>

  <h3>Why Choose Tri-Fold Brochures</h3>
  <ul>
    <li><strong>Compact Layout:</strong> Three panels provide a logical flow of information.</li>
    <li><strong>Full-Color Printing:</strong> Eye-catching visuals that highlight your brand.</li>
    <li><strong>Premium Paper:</strong> Glossy, matte, or textured finishes for a professional feel.</li>
    <li><strong>Cost-Effective:</strong> Ideal for bulk printing while maintaining high quality.</li>
    <li><strong>Flexible Applications:</strong> Perfect for product catalogs, service guides, or event handouts.</li>
  </ul>

  <h3>Stand Out at Events</h3>
  <p>
    Our tri-fold brochures make it easy to showcase your services and products in a professional, visually appealing way that leaves a lasting impression.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Print Your Tri-Fold Brochures Today
  </a>
                         """, "alt_texts": "Tri-Fold Brochures \u2014 styled mockup with props for context.", "category_name": "tri-fold", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Z-Fold Brochure",
                         "description": "Unique Z-fold brochures that unfold to present information creatively.",
                         "image_url": "Z-fold-Brochure.jpeg", "content": """
                         <div class="special-text">
  <h2>Z-Fold Brochures – Stand Out with Unique Design</h2>

  <p>
    Capture attention with our <strong>Z-Fold brochures</strong>, featuring a distinctive fold that creates an engaging and interactive experience for your audience.  
    Ideal for promotional campaigns, product highlights, and events where you want to make a memorable impression.
  </p>

  <h3>Why Choose Z-Fold Brochures</h3>
  <ul>
    <li><strong>Innovative Layout:</strong> Unique fold structure provides a dynamic way to present content.</li>
    <li><strong>High-Quality Printing:</strong> Crisp, full-color images that elevate your brand.</li>
    <li><strong>Premium Paper Options:</strong> Glossy, matte, or textured finishes for a professional feel.</li>
    <li><strong>Interactive Experience:</strong> Unfolding panels guide the reader through your story naturally.</li>
    <li><strong>Perfect for Promotions:</strong> Great for events, product launches, and informational campaigns.</li>
  </ul>

  <h3>Make a Lasting Impression</h3>
  <p>
    Our Z-Fold brochures are designed to grab attention, communicate key information clearly, and leave a lasting impression on your clients and prospects.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Print Your Z-Fold Brochures Today
  </a>
                         """, "alt_texts": "Z-Fold Brochure \u2014 professional mockup for product listing.", "category_name": "z-fold", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Booklets & Catalogs",
                    "description": "Professional booklets and catalogs to display your products and services elegantly.",
                    "image_url": "booklet&catalog.jpeg",
                    "category_name": "brochure",
                    "content": """
                    <h2>Booklets & Catalogs Printing</h2>
  <p>
    Showcase your products and services in style with our professional booklets and catalogs.  
    From small creative zines to large-scale catalogs and magazines, we offer premium printing  
    solutions that help you present your brand with clarity and elegance.
  </p>

  <h3>Our Booklet & Catalog Options</h3>
  <ul>
    <li><strong>Booklets:</strong> Compact, multi-page designs ideal for product guides and company portfolios.</li>
    <li><strong>Catalogs:</strong> Full-scale catalogs that organize and highlight your products beautifully.</li>
    <li><strong>Zines:</strong> Creative, small-batch publications perfect for niche audiences.</li>
    <li><strong>Magazines:</strong> Professionally styled magazines to tell your brand’s story.</li>
    <li><strong>Journals:</strong> Custom journals designed for personal or corporate branding.</li>
    <li><strong>Bookmarks:</strong> Promotional or retail bookmarks that add a lasting touch.</li>
  </ul>

  <h3>Why Choose Our Booklets & Catalogs?</h3>
  <ul>
    <li>High-quality printing with sharp images and vibrant colors</li>
    <li>Various binding options (saddle-stitched, perfect bound, etc.)</li>
    <li>Custom sizes, finishes, and paper types</li>
    <li>Ideal for businesses, schools, publishers, and events</li>
  </ul>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get a Quote
  </a>
                    """,
                    "alt_texts": "Booklets & Catalogs service image",
                    "products": [
                        {"name": "Booklets",
                         "description": "Compact multi-page booklets ideal for product guides and company portfolios.",
                         "image_url": "Booklets.jpeg", "content": """
                         <h2>Custom Booklets – Showcase Your Brand Professionally</h2>

  <p>
    Present your products, services, or company story with <strong>professionally printed booklets</strong>.  
    Perfect for product catalogs, company portfolios, event programs, or informational guides, our booklets are tailored to reflect your brand identity.
  </p>

  <h3>Why Choose Our Booklets</h3>
  <ul>
    <li><strong>Multi-Page Layouts:</strong> Flexible options from small guides to comprehensive catalogs.</li>
    <li><strong>High-Quality Printing:</strong> Crisp, vibrant colors that bring your content to life.</li>
    <li><strong>Various Binding Options:</strong> Saddle-stitched, perfect bound, or spiral-bound for a professional finish.</li>
    <li><strong>Custom Sizes & Finishes:</strong> Choose paper types, coatings, and finishes to match your brand.</li>
    <li><strong>Versatile Use:</strong> Ideal for businesses, schools, events, and creative projects.</li>
  </ul>

  <h3>Create a Lasting Impression</h3>
  <p>
    Our custom booklets make it easy to communicate information clearly while presenting your brand professionally. Each page is designed to captivate, inform, and leave a memorable impression.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Print Your Booklets Today
  </a>
                         """, "alt_texts": "Booklets \u2014 detail shot highlighting craftsmanship.", "category_name": "book", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Catalogs",
                         "description": "Full-scale catalogs that present your products in an organized, attractive manner.",
                         "image_url": "catalogs.jpeg", "content": """
                         <h2>Custom Catalogs – Showcase Products with Style</h2>

  <p>
    Make your products shine with <strong>professionally printed catalogs</strong>.  
    From small collections to extensive product lines, our catalogs are designed to present your offerings clearly, beautifully, and in a way that engages your audience.
  </p>

  <h3>Why Choose Our Catalogs</h3>
  <ul>
    <li><strong>Structured Layouts:</strong> Organize products, descriptions, and images in an appealing format.</li>
    <li><strong>High-Resolution Printing:</strong> Crisp, vibrant colors that make your products pop.</li>
    <li><strong>Custom Sizes & Finishes:</strong> Tailor paper types, finishes, and bindings to match your brand identity.</li>
    <li><strong>Professional Appeal:</strong> Perfect for business presentations, product launches, and retail displays.</li>
    <li><strong>Durable & Long-Lasting:</strong> Catalogs that withstand handling while maintaining a polished look.</li>
  </ul>

  <h3>Make a Strong Impression</h3>
  <p>
    Our custom catalogs help your audience navigate your products with ease, while creating a professional, memorable brand presence.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Print Your Catalogs Today
  </a>
                         """, "alt_texts": "Catalogs \u2014 professional mockup for product listing.", "category_name": "catalogs", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Zines",
                         "description": "Creative, small-batch publications perfect for niche audiences.",
                         "image_url": "zines.jpg", "content": """
                         <h2>Custom Zines – Express Your Unique Voice</h2>

  <p>
    Stand out with <strong>professionally printed zines</strong>—perfect for creative projects, niche audiences, and limited editions.  
    Compact, stylish, and full of personality, our zines are ideal for sharing stories, art, and ideas in a tangible, memorable way.
  </p>

  <h3>Why Choose Our Zines</h3>
  <ul>
    <li><strong>Creative Freedom:</strong> Flexible layouts and designs to bring your vision to life.</li>
    <li><strong>High-Quality Printing:</strong> Vibrant colors and crisp details that capture attention.</li>
    <li><strong>Various Sizes & Finishes:</strong> Customize dimensions, paper types, and binding options to fit your style.</li>
    <li><strong>Perfect for Small Batches:</strong> Ideal for events, exhibitions, personal projects, or limited editions.</li>
    <li><strong>Memorable Presentation:</strong> Compact and eye-catching, your zines leave a lasting impression.</li>
  </ul>

  <h3>Showcase Your Ideas</h3>
  <p>
    Whether you’re an artist, writer, or entrepreneur, our zines provide a creative platform to share your content professionally while standing out from the crowd.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Print Your Zines Today
  </a>
                         """, "alt_texts": "Zines \u2014 close-up showing print detail and finish.", "category_name": "zine", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Magazines",
                         "description": "Professional magazines to highlight your brand and stories.",
                         "image_url": "magazines.jpg", "content": """
                         <h2>Custom Magazines – Showcase Your Brand in Style</h2>

  <p>
    Make an impact with <strong>professionally printed magazines</strong>—perfect for sharing stories, highlighting products, or presenting company news.  
    Whether for corporate, creative, or niche audiences, our magazines combine premium printing, vibrant colors, and elegant layouts for maximum effect.
  </p>

  <h3>Why Choose Our Magazines</h3>
  <ul>
    <li><strong>High-Quality Printing:</strong> Crisp images, vivid colors, and professional finishes that reflect your brand.</li>
    <li><strong>Custom Layouts:</strong> Flexible page counts, sizes, and styles to match your content needs.</li>
    <li><strong>Multiple Binding Options:</strong> Saddle-stitched, perfect-bound, or spiral-bound for a polished presentation.</li>
    <li><strong>Professional Appeal:</strong> Perfect for clients, readers, or promotional distribution.</li>
    <li><strong>Eye-Catching Design:</strong> Modern, clean, and readable layouts that engage your audience.</li>
  </ul>

  <h3>Deliver Your Message Effectively</h3>
  <p>
    From corporate reports to creative showcases, our magazines provide a tangible way to communicate, inspire, and impress.  
    Each copy is produced with attention to detail, ensuring a premium, professional finish.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Print Your Magazines Today
  </a>
                         """, "alt_texts": "Magazines \u2014 styled mockup with props for context.", "category_name": "magazines", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Journals", "description": "Custom journals for personal or corporate branding.",
                         "image_url": "journals.jpg", "content": """
                         <h2>Custom Journals – Your Brand, Your Style</h2>

  <p>
    Create a lasting impression with <strong>personalized journals</strong>—perfect for corporate gifts, conferences, or personal use.  
    Our journals are crafted with high-quality paper, durable covers, and elegant finishes to provide both function and style.
  </p>

  <h3>Why Choose Our Journals</h3>
  <ul>
    <li><strong>Premium Materials:</strong> Thick, smooth pages with durable covers for a professional feel.</li>
    <li><strong>Custom Designs:</strong> Personalize covers, layouts, and sizes to reflect your brand or purpose.</li>
    <li><strong>Practical & Stylish:</strong> Ideal for note-taking, planning, or corporate giveaways.</li>
    <li><strong>Perfect for Gifting:</strong> Make your journals memorable for clients, employees, or event attendees.</li>
    <li><strong>Attention to Detail:</strong> Expert printing and finishing ensure every journal looks and feels premium.</li>
  </ul>

  <h3>Boost Your Brand with Custom Journals</h3>
  <p>
    Whether it’s for marketing, events, or personal use, our journals combine practical utility with elegant design—helping your audience stay organized while appreciating your brand.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Customize Your Journals Today
  </a>
                         """, "alt_texts": "Journals \u2014 professional mockup for product listing.", "category_name": "journals", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Bookmarks",
                         "description": "Printed bookmarks for promotional giveaways or retail use.",
                         "image_url": "Bookmarks.jpeg", "content": """
                         <h2>Custom Bookmarks – Small Tools, Big Impact</h2>

  <p>
    Make every page memorable with <strong>personalized bookmarks</strong>. Ideal for giveaways, corporate events, or retail promotions, our bookmarks are designed to combine utility with style.
  </p>

  <h3>Why Choose Our Bookmarks</h3>
  <ul>
    <li><strong>Custom Designs:</strong> Tailor colors, shapes, and artwork to fit your brand or event theme.</li>
    <li><strong>High-Quality Materials:</strong> Printed on durable cardstock with vibrant, full-color finishes.</li>
    <li><strong>Functional & Attractive:</strong> Keep your audience engaged while promoting your brand.</li>
    <li><strong>Perfect for Giveaways:</strong> Memorable and practical items for clients, students, or attendees.</li>
    <li><strong>Eco-Friendly Options:</strong> Sustainable paper options for environmentally conscious promotions.</li>
  </ul>

  <h3>Elevate Your Brand with Custom Bookmarks</h3>
  <p>
    Bookmarks are small but powerful marketing tools. Use them to leave a lasting impression while providing a functional product your audience will appreciate.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Design Your Bookmarks Today
  </a>
                         """, "alt_texts": "Bookmarks \u2014 in-use photo demonstrating scale.", "category_name": "bookmark", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Poster Printing",
                    "description": "Large-format posters to make a bold statement and promote your brand effectively.",
                    "image_url": "poster+print.jpeg",
                    "category_name": "poster",
                    "content": """
                    <h2>Poster Printing Services</h2>
  <p>
    Make a bold statement and grab attention with our professional poster printing.  
    Whether you need posters for events, promotions, or outdoor campaigns,  
    we deliver high-quality prints that showcase your message with impact.
  </p>

  <h3>Our Poster Options</h3>
  <ul>
    <li><strong>Posters:</strong> Standard posters perfect for events, advertisements, and promotions.</li>
    <li><strong>Large Format Posters:</strong> Oversized designs that capture attention from a distance.</li>
    <li><strong>Outdoor Posters:</strong> Weather-resistant posters built for durability and visibility outdoors.</li>
    <li><strong>Mounted Posters:</strong> Posters mounted on boards for a sleek, professional presentation.</li>
  </ul>

  <h3>Why Print Posters with Us?</h3>
  <ul>
    <li>High-resolution, full-color printing for sharp and vibrant visuals</li>
    <li>Various sizes and finishes to match your branding</li>
    <li>Durable materials suitable for both indoor and outdoor use</li>
    <li>Perfect for businesses, events, schools, and campaigns</li>
  </ul>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get a Quote
  </a>
                    """,
                    "alt_texts": "Poster Printing image",
                    "products": [
                        {"name": "Posters",
                         "description": "Standard posters for events, promotions, or advertisements.",
                         "image_url": "poster_new.jpeg", "content": """
                         <h2>Custom Posters – Make Your Message Stand Out</h2>

  <p>
    Transform any space into a visual showcase with <strong>high-quality custom posters</strong>. Perfect for events, promotions, corporate branding, or personal projects, our posters are designed to grab attention and leave a lasting impression.
  </p>

  <h3>Why Our Posters Shine</h3>
  <ul>
    <li><strong>Vibrant, High-Resolution Printing:</strong> Every detail pops with sharp, full-color prints.</li>
    <li><strong>Custom Sizes & Styles:</strong> From standard A4 to large-format posters, tailored to your project’s needs.</li>
    <li><strong>Durable & Long-Lasting:</strong> Printed on premium paper or weather-resistant materials for indoor and outdoor use.</li>
    <li><strong>Creative Freedom:</strong> Choose from matte, glossy, or specialty finishes to match your design vision.</li>
    <li><strong>Perfect for Any Purpose:</strong> Events, advertisements, wall art, or informational displays—your poster, your style.</li>
  </ul>

  <h3>Boost Visibility & Engagement</h3>
  <p>
    Posters are more than just printed sheets—they're a tool to captivate audiences and communicate messages with impact. Our expert printing ensures your graphics, text, and colors always shine.  
    Whether for a promotional campaign or personal expression, posters from Gregbuk make a bold statement.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get Your Custom Poster Today
  </a>
                         """, "alt_texts": "Posters \u2014 detail shot highlighting craftsmanship.", "category_name": "post", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Large Format Poster",
                         "description": "Extra-large posters to attract attention from a distance.",
                         "image_url": "larger-format-poster.jpeg", "content": """
                         <h2>Large Format Posters – Bigger, Bolder, Unforgettable</h2>

  <p>
    Step up your branding or event visibility with <strong>large format posters</strong>. Designed to capture attention from a distance, these posters are ideal for trade shows, exhibitions, outdoor promotions, or impactful wall displays.  
    When size matters, Gregbuk delivers quality that truly stands out.
  </p>

  <h3>Why Choose Large Format Posters?</h3>
  <ul>
    <li><strong>Eye-Catching Visuals:</strong> Oversized prints that demand attention and create a lasting impression.</li>
    <li><strong>Custom Sizes:</strong> Tailored to suit walls, events, or promotional spaces, ensuring maximum impact.</li>
    <li><strong>Premium Materials:</strong> High-quality paper, weather-resistant options, and professional finishes for durability.</li>
    <li><strong>Vibrant Colors & Sharp Details:</strong> Prints maintain their brilliance, even at large scales.</li>
    <li><strong>Versatile Use:</strong> Perfect for indoor displays, storefronts, exhibitions, and outdoor promotions.</li>
  </ul>

  <h3>Stand Out with Every Impression</h3>
  <p>
    A large format poster is more than just an oversized print—it’s a statement. From marketing campaigns to event highlights, our professional printing ensures that every detail, color, and design element is crisp and impactful.  
    Make your message impossible to miss with Gregbuk’s expertise.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get Your Large Poster Today
  </a>
                         """, "alt_texts": "Large Format Poster \u2014 professional mockup for product listing.", "category_name": "large-poster", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Outdoor Poster",
                         "description": "Durable posters designed for outdoor use and weather resistance.",
                         "image_url": "outdoor_poster.jpeg", "content": """
                         <div class="special-text">
  <h2>Outdoor Posters – Bold, Weather-Resistant, Unmissable</h2>

  <p>
    Make your brand or event impossible to ignore with <strong>outdoor posters</strong>. Crafted for durability and visibility, these posters withstand the elements while keeping colors vibrant and designs sharp. Perfect for storefronts, streets, events, or any high-traffic outdoor space.
  </p>

  <h3>Why Our Outdoor Posters Stand Out</h3>
  <ul>
    <li><strong>Weather-Resistant Materials:</strong> Designed to endure rain, sun, and wind without fading or tearing.</li>
    <li><strong>High-Impact Visuals:</strong> Large, vibrant prints that grab attention from afar.</li>
    <li><strong>Custom Sizes & Finishes:</strong> Tailored to your space and campaign needs, from banners to wall posters.</li>
    <li><strong>Professional Print Quality:</strong> Crisp details, bold colors, and long-lasting durability.</li>
    <li><strong>Versatile Uses:</strong> Events, outdoor marketing, campaigns, and promotions—all with maximum visibility.</li>
  </ul>

  <h3>Turn Heads Outdoors</h3>
  <p>
    Outdoor posters are your brand’s chance to make a striking first impression. Whether promoting an event or showcasing a product, Gregbuk ensures every poster is printed with precision, color accuracy, and lasting quality.  
    Your message deserves to be seen—and remembered.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Order Your Outdoor Poster
  </a>
                         """, "alt_texts": "Outdoor Poster \u2014 product shot on white background.", "category_name": "outdoor-poster", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Mounted Poster",
                         "description": "Posters mounted on boards for a polished, professional look.",
                         "image_url": "mounted-poster.jpeg", "content": """
                         <h2>Mounted Posters – Professional Display, Instant Impact</h2>

  <p>
    Elevate your visuals with <strong>mounted posters</strong>. Perfect for exhibitions, offices, retail displays, and presentations, these posters are mounted on sturdy boards for a clean, professional appearance that instantly captures attention.
  </p>

  <h3>Why Choose Mounted Posters?</h3>
  <ul>
    <li><strong>Premium Mounting:</strong> Posters mounted on durable boards for rigidity and a polished look.</li>
    <li><strong>Vibrant & Crisp Printing:</strong> High-quality prints that showcase your message in sharp detail.</li>
    <li><strong>Ready-to-Display:</strong> Perfect for walls, displays, or promotional setups without extra framing.</li>
    <li><strong>Custom Sizes & Finishes:</strong> Tailored to your space and presentation requirements.</li>
    <li><strong>Ideal for Events & Campaigns:</strong> Make a professional statement at exhibitions, stores, or corporate presentations.</li>
  </ul>

  <h3>Professional Visuals Made Simple</h3>
  <p>
    Mounted posters combine durability with style. They’re an ideal choice when you need high-impact visuals that remain perfectly presented over time. Gregbuk ensures every mounted poster is printed, mounted, and finished to perfection.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Order Your Mounted Poster
  </a>
                         """, "alt_texts": "Mounted Poster \u2014 professional mockup for product listing.", "category_name": "mounted-poster", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Stationery",
                    "description": "Custom stationery to maintain a consistent brand identity in office and client communications.",
                    "image_url": "Stationery.jpeg",
                    "category_name": "stationery",
                    "content": """
                    <h2>Custom Stationery Printing</h2>
  <p>
    Build a consistent and professional brand identity with our custom stationery printing.  
    From notepads to letterheads, folders, and envelopes, we provide high-quality office essentials  
    that make every client interaction polished and memorable.
  </p>

  <h3>Our Stationery Options</h3>
  <ul>
    <li><strong>Notepads:</strong> Branded notepads designed for daily office use or promotional giveaways.</li>
    <li><strong>Letterheads:</strong> Professional letterheads that give your business correspondence a refined touch.</li>
    <li><strong>Folders:</strong> Durable, branded folders for presenting and organizing client documents.</li>
    <li><strong>Envelopes:</strong> Custom-printed envelopes to complement your branded stationery set.</li>
  </ul>

  <h3>Why Choose Our Stationery?</h3>
  <ul>
    <li>Premium paper and print finishes for a professional look</li>
    <li>Customizable designs to match your brand identity</li>
    <li>Durable and practical for both office and client use</li>
    <li>Perfect for businesses, schools, and organizations</li>
  </ul>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get a Quote
  </a>
                    """,
                    "alt_texts": "Stationery service image",
                    "products": [
                        {"name": "Notepads", "description": "Branded notepads for office use or promotional purposes.",
                         "image_url": "notepad.jpeg", "content": """
                         <h2>Custom Notepads – Practical, Professional, & Branded</h2>

  <p>
    Make every note a reflection of your brand with <strong>custom notepads</strong>. Perfect for office use, giveaways, or client gifts, our notepads combine practicality with professional design to keep your brand top of mind.
  </p>

  <h3>Why Choose Custom Notepads?</h3>
  <ul>
    <li><strong>High-Quality Paper:</strong> Smooth, durable sheets ideal for writing, sketching, or jotting down ideas.</li>
    <li><strong>Branding Opportunities:</strong> Add logos, taglines, and custom designs to reinforce your identity.</li>
    <li><strong>Various Sizes & Styles:</strong> From pocket-sized pads to full desk notepads, tailored to your needs.</li>
    <li><strong>Eco-Friendly Options:</strong> Recycled paper choices for sustainable branding.</li>
    <li><strong>Perfect for Promotions:</strong> Great for giveaways, events, or as corporate gifts.</li>
  </ul>

  <h3>Make an Impression with Every Page</h3>
  <p>
    Every note written on a Gregbuk custom notepad carries your brand. Choose from various layouts, cover designs, and finishes to create a professional, memorable item that enhances your business communications.
  </p>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Order Your Custom Notepad
  </a>
                         """, "alt_texts": "Notepads \u2014 detail shot highlighting craftsmanship.", "category_name": "notepad", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Letterheads",
                         "description": "Professional letterheads to create impactful business correspondence.",
                         "image_url": "letterheads.jpeg", "content": """
                         <h2>Professional Letterheads & Branded Stationery</h2>
<p>
    Elevate your business communications with <strong>custom letterheads</strong> from Gregbuk.  
    Our high-quality printing ensures every document reflects your brand's professionalism and attention to detail.  
    Choose from modern designs, premium paper, and crisp, clear printing for a lasting impression.
</p>

<h3>Why Letterheads Matter</h3>
<p>
    A well-designed letterhead does more than just convey information — it reinforces your brand identity.  
    Every letter, invoice, or proposal you send becomes a subtle ambassador of your company, showcasing credibility and professionalism.
</p>

<h3>Our Letterhead Options</h3>
<ul>
    <li><strong>Custom Sizes & Layouts:</strong> Tailored to match your business needs and branding.</li>
    <li><strong>Premium Paper:</strong> Smooth, textured, or eco-friendly paper options available.</li>
    <li><strong>Full-Color Printing:</strong> Vibrant colors that make your logo and design pop.</li>
    <li><strong>Finishing Options:</strong> Matte, glossy, or embossed finishes to add a touch of elegance.</li>
</ul>

<p>
    Ensure your correspondence always represents your business at its best.  
    <a class="btn btn-outline-primary rounded-pill border border-2 border-primary" href="/contact?head=Marketing">Get started today</a> — discuss your custom letterhead project with our expert team.
</p>
                         """, "alt_texts": "Letterheads \u2014 angled view showing texture and edges.", "category_name": "letter-head", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Folders",
                         "description": "Durable folders for organizing documents or client materials.",
                         "image_url": "folders.jpeg", "content": """
                         <h2>Custom Presentation Folders</h2>
<p>
    Make a polished impression with <strong>custom presentation folders</strong> from Gregbuk.  
    Perfect for proposals, client meetings, or corporate presentations, our folders combine functionality with professional design to showcase your brand.
</p>

<h3>Why Choose Custom Folders</h3>
<p>
    Presentation folders are more than just storage — they organize your documents while reinforcing your brand identity.  
    A well-crafted folder reflects attention to detail and professionalism, leaving a lasting impression on clients and partners.
</p>

<h3>Our Folder Options</h3>
<ul>
    <li><strong>Custom Sizes & Formats:</strong> Single-pocket, double-pocket, or tri-fold designs to suit your documents.</li>
    <li><strong>Premium Materials:</strong> Sturdy cardstock with matte, glossy, or soft-touch finishes.</li>
    <li><strong>Full-Color Printing:</strong> High-resolution printing for logos, graphics, and branding elements.</li>
    <li><strong>Special Finishes:</strong> Embossing, foil stamping, or spot UV for a luxurious touch.</li>
</ul>

<p>
    Present your business documents with confidence and style.  
    <a class="btn btn-outline-primary rounded-pill border border-2 border-primary" href="/contact?head=Marketing">Get started today</a> — connect with our team to design your custom folders.
</p>
                         """, "alt_texts": "Folders \u2014 detail shot highlighting craftsmanship.", "category_name": "folder", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Envelopes", "description": "Custom envelopes to complement your branded stationery.",
                         "image_url": "Envelopes.jpeg", "content": """
                         <h2>Custom Printed Envelopes</h2>
<p>
    Elevate your business correspondence with <strong>custom printed envelopes</strong> from Gregbuk.  
    Ideal for letters, invoices, or marketing mail, our envelopes ensure your communications stand out while maintaining a professional look.
</p>

<h3>Why Custom Envelopes Matter</h3>
<p>
    Branded envelopes help reinforce your identity with every mailing.  
    Whether for client outreach, promotions, or internal communications, a well-designed envelope reflects attention to detail and strengthens brand recognition.
</p>

<h3>Our Envelope Options</h3>
<ul>
    <li><strong>Various Sizes:</strong> Standard, business, or custom dimensions to match your letters or documents.</li>
    <li><strong>Premium Materials:</strong> High-quality paper stock for a polished and durable finish.</li>
    <li><strong>Full-Color Printing:</strong> Logos, return addresses, and brand graphics printed with vibrant detail.</li>
    <li><strong>Special Finishes:</strong> Options like foil accents, embossing, or matte coating for extra sophistication.</li>
</ul>

<p>
    Make a strong first impression with every piece of mail.  
    <a class="btn btn-outline-primary rounded-pill border border-2 border-primary" href="/contact?head=Marketing">Get started today</a> — let our team help you create envelopes that match your brand perfectly.
</p>

                         """, "alt_texts": "Envelopes \u2014 close-up showing print detail and finish.", "category_name": "envelop", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                  "name": "Merchandise & Apparel",
                  "description": "Custom apparel and promotional merchandise like t-shirts, mugs, caps and more.",
                  "category_name": "merchandise-apparel",
                  "content": """
                  <h2>Custom Merchandise & Apparel</h2>
  <p>
    Take your brand beyond paper with our wide range of custom merchandise and apparel.  
    From stylish t-shirts and hoodies to everyday items like mugs, caps, and keychains,  
    we create high-quality branded products that boost visibility and leave a lasting impression.
  </p>

  <h3>Our Merchandise & Apparel Options</h3>
  <ul>
    <li><strong>Custom T-Shirts:</strong> Screen-printed or digitally printed t-shirts tailored to your brand.</li>
    <li><strong>Branded Caps:</strong> Embroidered or printed caps for promotions, giveaways, or uniforms.</li>
    <li><strong>Printed Mugs:</strong> Perfect for gifts, events, or daily brand visibility.</li>
    <li><strong>Tote Bags:</strong> Reusable bags that make eco-friendly promotional giveaways.</li>
    <li><strong>Custom Hoodies:</strong> Comfortable branded hoodies ideal for campaigns and staff wear.</li>
    <li><strong>Water Bottles:</strong> Branded, reusable bottles that promote sustainability.</li>
    <li><strong>Phone Cases:</strong> Custom-printed phone cases for style and branding.</li>
    <li><strong>Keychains:</strong> Affordable and practical branded giveaways.</li>
  </ul>

  <h3>Why Choose Custom Merchandise?</h3>
  <ul>
    <li>High-quality printing and embroidery for lasting designs</li>
    <li>Wide variety of products to suit events, corporate branding, and promotions</li>
    <li>Durable and practical items that keep your brand top of mind</li>
    <li>Perfect for giveaways, staff uniforms, and retail merchandise</li>
  </ul>

  <a href="/contact?head=Marketing" class="btn btn-primary">
    Get a Quote
  </a>
                  """,
                  "image_url": "mercherdise&apparel.jpeg",
                  "icon_name": "#cil-check",
                  "alt_texts": "Merchandise and Apparel service image",
                  "products": [
                    {
                      "name": "Custom T-Shirts",
                      "description": "Screen-printed and digitally printed custom t-shirts.",
                      "category_name": "custom-t-shirts",
                      "image_url": "custon_tshirt.jpeg",
                      "content": """
                      <h2>Custom T-Shirts Printing</h2>
<p>
    Make your brand wearable with our high-quality <strong>custom t-shirts</strong>. Perfect for events, promotions, staff uniforms, or giveaways, these t-shirts combine comfort with professional design.
</p>

<h3>Why Choose Our Custom T-Shirts?</h3>
<ul>
    <li>Premium fabrics for comfort and durability</li>
    <li>Screen printing or digital printing for vibrant, long-lasting designs</li>
    <li>Custom sizes and colors to match your brand or campaign</li>
    <li>Ideal for corporate events, promotional campaigns, and casual wear</li>
</ul>

<h3>Design Options</h3>
<p>
    Whether you need a simple logo or a full custom artwork, we ensure your t-shirts make a statement. Choose from classic cuts, trendy fits, and eco-friendly materials for a professional yet stylish result.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Your Custom T-Shirts</strong>
</a>
                      """,
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Custom T-Shirts \u2014 product shot on white background.",
                        "Custom T-Shirts \u2014 close-up showing print detail and finish.",
                        "Custom T-Shirts \u2014 styled mockup with props for context.",
                        "Custom T-Shirts \u2014 angled view showing texture and edges.",
                        "Custom T-Shirts \u2014 stack of multiple items showing variety.",
                        "Custom T-Shirts \u2014 in-use photo demonstrating scale.",
                        "Custom T-Shirts \u2014 detail shot highlighting craftsmanship.",
                        "Custom T-Shirts \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Branded Caps",
                      "description": "Custom embroidered and printed caps.",
                      "category_name": "branded-caps",
                      "image_url": "branded_caps.jpeg",
                      "content": """
                      <h2>Custom Branded Caps</h2>
<p>
    Top off your brand with our stylish <strong>custom branded caps</strong>. Perfect for promotions, events, team uniforms, or giveaways, these caps are designed to combine fashion with your brand identity.
</p>

<h3>Why Choose Our Branded Caps?</h3>
<ul>
    <li>High-quality materials for comfort, durability, and long-lasting wear</li>
    <li>Embroidery or print options to showcase your logo or design</li>
    <li>Adjustable sizes and trendy fits for all ages and styles</li>
    <li>Perfect for corporate events, giveaways, sports teams, or casual branding</li>
</ul>

<h3>Design Options</h3>
<p>
    Choose from snapbacks, dad hats, or fitted caps. Add your logo, slogan, or artwork to make your caps truly unique and memorable. Our team ensures every detail reflects your brand’s professionalism and style.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Your Branded Caps</strong>
</a>
                      """,
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Branded Caps \u2014 product shot on white background.",
                        "Branded Caps \u2014 close-up showing print detail and finish.",
                        "Branded Caps \u2014 styled mockup with props for context.",
                        "Branded Caps \u2014 angled view showing texture and edges.",
                        "Branded Caps \u2014 stack of multiple items showing variety.",
                        "Branded Caps \u2014 in-use photo demonstrating scale.",
                        "Branded Caps \u2014 detail shot highlighting craftsmanship.",
                        "Branded Caps \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Printed Mugs",
                      "description": "Custom printed mugs for gifts and promotions.",
                      "category_name": "printed-mugs",
                      "image_url": "printed_mugs.jpeg",
                      "content": """
                      <h2>Custom Printed Mugs</h2>
<p>
    Elevate your brand’s presence with our <strong>custom printed mugs</strong>. Ideal for corporate gifts, promotional giveaways, events, or even personal use, these mugs turn every sip into a memorable brand experience.
</p>

<h3>Why Our Printed Mugs Stand Out</h3>
<ul>
    <li>Premium ceramic quality that ensures durability and long-lasting prints</li>
    <li>Vibrant full-color printing to showcase logos, artwork, or slogans</li>
    <li>Microwave and dishwasher safe for everyday convenience</li>
    <li>Perfect for branding, giveaways, office use, or special occasions</li>
</ul>

<h3>Customization Options</h3>
<p>
    Select from a variety of sizes, shapes, and finishes including glossy, matte, or color-changing mugs. Add your unique design to create a mug that not only serves a practical purpose but also makes a lasting impression on your clients and audience.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Your Custom Mugs</strong>
</a>
                      """,
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Printed Mugs \u2014 product shot on white background.",
                        "Printed Mugs \u2014 close-up showing print detail and finish.",
                        "Printed Mugs \u2014 styled mockup with props for context.",
                        "Printed Mugs \u2014 angled view showing texture and edges.",
                        "Printed Mugs \u2014 stack of multiple items showing variety.",
                        "Printed Mugs \u2014 in-use photo demonstrating scale.",
                        "Printed Mugs \u2014 detail shot highlighting craftsmanship.",
                        "Printed Mugs \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Tote Bags",
                      "description": "Printed tote bags for events and giveaways.",
                      "category_name": "tote-bags",
                      "image_url": "tote_bag.jpeg",
                      "content": """
                      <h2>Custom Tote Bags</h2>
<p>
    Make a statement while staying eco-friendly with our <strong>custom tote bags</strong>. Perfect for giveaways, events, or retail promotions, these tote bags are functional, stylish, and a walking advertisement for your brand.
</p>

<h3>Why Choose Our Tote Bags</h3>
<ul>
    <li>Durable, high-quality materials that withstand daily use</li>
    <li>Full-color printing to display your logo, artwork, or message boldly</li>
    <li>Reusable and eco-conscious for environmentally responsible branding</li>
    <li>Ideal for corporate gifts, trade shows, or customer appreciation</li>
</ul>

<h3>Customization Options</h3>
<p>
    Choose from a variety of sizes, colors, and printing styles including screen-printing or digital printing. Add your unique design to create a tote bag that is not only practical but also promotes your brand wherever it goes.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Get Your Custom Tote Bags</strong>
</a>
                      """,
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Tote Bags \u2014 product shot on white background.",
                        "Tote Bags \u2014 close-up showing print detail and finish.",
                        "Tote Bags \u2014 styled mockup with props for context.",
                        "Tote Bags \u2014 angled view showing texture and edges.",
                        "Tote Bags \u2014 stack of multiple items showing variety.",
                        "Tote Bags \u2014 in-use photo demonstrating scale.",
                        "Tote Bags \u2014 detail shot highlighting craftsmanship.",
                        "Tote Bags \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Custom Hoodies",
                      "image_url": "custom_hoodies.jpeg",
                      "description": "Branded hoodies for staff and promotional campaigns.",
                      "category_name": "custom-hoodies",
                      "content": """
                      <h2>Custom Hoodies</h2>
<p>
    Keep your team and customers cozy while showcasing your brand with our <strong>custom hoodies</strong>. Perfect for staff uniforms, giveaways, or event merchandise, these hoodies combine comfort, style, and promotional impact.
</p>

<h3>Why Choose Our Custom Hoodies</h3>
<ul>
    <li>Premium, soft fabrics for maximum comfort and durability</li>
    <li>High-quality printing or embroidery to display logos and designs vividly</li>
    <li>Available in multiple sizes and colors to suit all audiences</li>
    <li>Great for branding, promotional campaigns, or corporate gifts</li>
</ul>

<h3>Customization Options</h3>
<p>
    Select from various hoodie styles including pullover, zip-up, or lightweight options. Add your company logo, slogan, or creative design to create a hoodie that not only keeps people warm but also promotes your brand wherever it goes.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Your Custom Hoodies</strong>
</a>""",
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Custom Hoodies \u2014 product shot on white background.",
                        "Custom Hoodies \u2014 close-up showing print detail and finish.",
                        "Custom Hoodies \u2014 styled mockup with props for context.",
                        "Custom Hoodies \u2014 angled view showing texture and edges.",
                        "Custom Hoodies \u2014 stack of multiple items showing variety.",
                        "Custom Hoodies \u2014 in-use photo demonstrating scale.",
                        "Custom Hoodies \u2014 detail shot highlighting craftsmanship.",
                        "Custom Hoodies \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Water Bottles",
                      "image_url": "water_botttles.jpeg",
                      "description": "Branded reusable water bottles.",
                      "content": """
                      <h2>Branded Water Bottles</h2>
<p>
    Stay refreshed while promoting your brand with our <strong>custom water bottles</strong>. Perfect for corporate events, giveaways, gyms, or daily use, these bottles combine practicality with style, keeping your brand top of mind.
</p>

<h3>Why Choose Our Branded Water Bottles</h3>
<ul>
    <li>Durable, eco-friendly materials designed for daily use</li>
    <li>Custom printing to showcase logos, slogans, or designs</li>
    <li>Available in multiple sizes, colors, and finishes</li>
    <li>Ideal for corporate gifts, promotional campaigns, or merchandise sales</li>
</ul>

<h3>Customization Options</h3>
<p>
    Choose from sleek stainless steel, BPA-free plastic, or eco-friendly options. Add your branding to create a functional, stylish item that clients, staff, or customers will love to use every day.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Get Your Branded Water Bottles</strong>
</a>
                      """,
                      "category_name": "water-bottles",
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Water Bottles \u2014 product shot on white background.",
                        "Water Bottles \u2014 close-up showing print detail and finish.",
                        "Water Bottles \u2014 styled mockup with props for context.",
                        "Water Bottles \u2014 angled view showing texture and edges.",
                        "Water Bottles \u2014 stack of multiple items showing variety.",
                        "Water Bottles \u2014 in-use photo demonstrating scale.",
                        "Water Bottles \u2014 detail shot highlighting craftsmanship.",
                        "Water Bottles \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Phone Cases",
                      "image_url": "phone_case.jpeg",
                      "description": "Custom printed phone cases.",
                      "category_name": "phone-cases",
                      "content": """
                      <h2>Custom Phone Cases</h2>
<p>
    Protect devices while promoting your brand with our <strong>custom phone cases</strong>. Ideal for giveaways, employee gifts, or retail products, these cases combine style, functionality, and brand visibility.
</p>

<h3>Why Choose Our Custom Phone Cases</h3>
<ul>
    <li>Durable materials offering protection for everyday use</li>
    <li>Vibrant, full-color printing to showcase logos, designs, or slogans</li>
    <li>Available for a wide range of popular phone models</li>
    <li>Perfect for corporate branding, promotional campaigns, or personalized gifts</li>
</ul>

<h3>Design & Customization</h3>
<p>
    Select from slim, rugged, or flexible case types. Customize every case with your brand’s colors, logos, or artwork to create a unique promotional item that stands out.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Custom Phone Cases</strong>
</a>
                      """,
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Phone Cases \u2014 product shot on white background.",
                        "Phone Cases \u2014 close-up showing print detail and finish.",
                        "Phone Cases \u2014 styled mockup with props for context.",
                        "Phone Cases \u2014 angled view showing texture and edges.",
                        "Phone Cases \u2014 stack of multiple items showing variety.",
                        "Phone Cases \u2014 in-use photo demonstrating scale.",
                        "Phone Cases \u2014 detail shot highlighting craftsmanship.",
                        "Phone Cases \u2014 professional mockup for product listing."
                      ])
                    },
                    {
                      "name": "Keychains",
                      "image_url": "key_chains.jpeg",
                      "description": "Branded keyrings and small giveaways.",
                      "content": """
                      <h2>Branded Keychains</h2>
<p>
    Keep your brand in hand—literally—with our <strong>custom keychains</strong>. Perfect for giveaways, events, or corporate gifts, these small but impactful items help your business stay memorable.
</p>

<h3>Why Choose Our Keychains</h3>
<ul>
    <li>Durable materials designed to last and showcase your brand</li>
    <li>Custom shapes, colors, and logos to fit your brand identity</li>
    <li>Practical and stylish for everyday use, ensuring frequent visibility</li>
    <li>Ideal for promotions, giveaways, and personalized gifts</li>
</ul>

<h3>Design & Options</h3>
<p>
    Choose from a variety of materials such as metal, acrylic, or plastic. Add engravings, full-color prints, or embossed logos to make each keychain uniquely yours.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Get Custom Keychains</strong>
</a>
                      """,
                      "category_name": "keychains",
                      "image_collection": [choice(imgg) for n in range(8)],
                      "alt_texts": choice([
                        "Keychains \u2014 product shot on white background.",
                        "Keychains \u2014 close-up showing print detail and finish.",
                        "Keychains \u2014 styled mockup with props for context.",
                        "Keychains \u2014 angled view showing texture and edges.",
                        "Keychains \u2014 stack of multiple items showing variety.",
                        "Keychains \u2014 in-use photo demonstrating scale.",
                        "Keychains \u2014 detail shot highlighting craftsmanship.",
                        "Keychains \u2014 professional mockup for product listing."
                      ])
                    }
                  ]
                },
                {
                    "name": "Invitation & Cards",
                    "description": "Elegant invitation cards and personalized cards for all occasions and events.",
                    "image_url": "invitation&cards.jpeg",
                    "alt_texts": "Invitation & Cards service image",
                    "category_name": "invitation-cards",
                    "content": """
                    <h2>Invitation & Cards Printing</h2>
<p>
    Make every event and occasion truly special with our <strong>custom invitation and cards</strong>. From elegant wedding invitations to corporate event cards, each design is crafted to impress and convey your message with style.
</p>

<h3>Why Choose Our Invitation & Cards</h3>
<ul>
    <li>Premium quality cardstock with luxurious finishes for a professional look</li>
    <li>Customizable designs that reflect your unique theme or brand</li>
    <li>Perfect for weddings, parties, corporate events, and seasonal greetings</li>
    <li>Options for foil, embossed, and full-color prints to elevate every card</li>
</ul>

<h3>Design & Options</h3>
<p>
    Select from various formats including standard postcards, foil cards, RSVP cards, and holiday or greeting cards. Each piece is designed to create lasting impressions for recipients and guests alike.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Create Your Custom Invitation & Cards</strong>
</a>
                    """,
                    "products": [
                        {"name": "Standard Postcards",
                         "description": "Classic postcards for correspondence or promotional use.",
                         "image_url": "post-card.jpeg", "content": """
                         <h3>Standard Postcards</h3>
<p>
    Our <strong>Standard Postcards</strong> are the perfect balance of elegance and functionality. Whether you’re sending personal greetings, promoting an event, or launching a marketing campaign, these postcards deliver your message with clarity and style. Printed on high-quality, durable cardstock, each postcard ensures that your content makes a lasting impression.
</p>

<p>
    Available in various sizes and finishes, these postcards can be customized to reflect your brand or personal taste. From bold, vibrant designs to minimalist elegance, you can craft a postcard that truly stands out in the mailbox or on a display table. At <strong>Gregbuk</strong>, we combine professional printing expertise with creative flexibility to help your message get noticed.
</p>

<h4>Why Choose Our Standard Postcards?</h4>
<ul>
    <li><strong>Premium Cardstock:</strong> Thick, durable material ensures a high-quality feel and longevity.</li>
    <li><strong>Vivid Full-Color Printing:</strong> Every detail comes to life with bright, sharp colors that captivate attention.</li>
    <li><strong>Customizable Design:</strong> Personalize your postcard’s front and back to match your branding or event theme.</li>
    <li><strong>Versatile Use:</strong> Ideal for personal messages, invitations, holiday greetings, direct mail campaigns, and promotions.</li>
    <li><strong>Eco-Friendly Options:</strong> Available on sustainable paper choices for environmentally conscious projects.</li>
</ul>

<p>
    Whether you’re sending a heartfelt message to loved ones or promoting your business, <strong>Standard Postcards</strong> are a cost-effective, impactful tool. With fast turnaround times, flexible quantities, and professional finishes, you can rely on <strong>Gregbuk</strong> to deliver postcards that leave a positive impression every time.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Your Standard Postcards Today</strong>
</a>
                         """, "alt_texts": "Standard Postcards \u2014 professional mockup for product listing.", "category_name": "standard-postcd", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Foil Postcards",
                         "description": "Luxurious foil-finished postcards that shine and impress.",
                         "image_url": "Foilcard.jpeg", "content": """
                         <h3>Foil Postcards</h3>
<p>
    Make a dazzling impression with our <strong>Foil Postcards</strong>. Perfect for luxury invitations, premium promotions, or special announcements, these postcards feature metallic foil accents that catch the light and grab attention. Each postcard is crafted with precision on high-quality cardstock, giving your message a sophisticated, eye-catching finish.
</p>

<p>
    Whether you’re sending holiday greetings, event invites, or corporate announcements, <strong>Gregbuk’s Foil Postcards</strong> elevate your communication with elegance and style. Choose from a variety of foil colors, patterns, and layouts to create a unique design that reflects your brand or personal taste.
</p>

<h4>Why Choose Foil Postcards?</h4>
<ul>
    <li><strong>Premium Foil Finishes:</strong> Metallic accents in gold, silver, or custom colors for an upscale look.</li>
    <li><strong>High-Quality Cardstock:</strong> Thick, durable material ensures your postcard feels as luxurious as it looks.</li>
    <li><strong>Customizable Designs:</strong> Tailor the front and back with your message, logo, and imagery for a unique presentation.</li>
    <li><strong>Memorable Impact:</strong> Foil postcards stand out in mailboxes and handouts, making your message unforgettable.</li>
    <li><strong>Perfect for Special Occasions:</strong> Weddings, corporate events, holiday greetings, and VIP promotions.</li>
</ul>

<p>
    Turn every postcard into a statement piece with <strong>Gregbuk’s Foil Postcards</strong>. With attention to detail, vibrant foil finishes, and professional printing, your message will sparkle and leave a lasting impression on every recipient.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Order Your Foil Postcards Today</strong>
</a>
                         """, "alt_texts": "Foil Postcards \u2014 in-use photo demonstrating scale.", "category_name": "foil-postcd", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Invitation Cards",
                         "description": "Stylish invitation cards for weddings, parties, and corporate events.",
                         "image_url": "Invitations.jpeg", "content": """
                         <h3>Invitation Cards</h3>
<p>
    Celebrate your special moments in style with our <strong>Invitation Cards</strong>. Whether for weddings, parties, corporate events, or milestone celebrations, each card is designed to reflect elegance and sophistication. At <strong>Gregbuk</strong>, we combine high-quality materials with creative designs to make your invitations truly memorable.
</p>

<p>
    Our invitation cards come in a variety of styles, from classic and minimalist to vibrant and artistic. Personalize them with your event details, custom logos, or unique graphics, ensuring every guest receives an invitation that sets the perfect tone for your event.
</p>

<h4>Why Choose Gregbuk Invitation Cards?</h4>
<ul>
    <li><strong>Premium Paper & Printing:</strong> Thick, luxurious cardstock with crisp, vibrant printing.</li>
    <li><strong>Customizable Designs:</strong> Tailor your invitations with unique layouts, fonts, and graphics.</li>
    <li><strong>Elegant Finishes:</strong> Options include matte, glossy, embossed, or foil accents for extra flair.</li>
    <li><strong>Perfect for Every Occasion:</strong> Weddings, corporate gatherings, birthdays, and seasonal events.</li>
    <li><strong>Attention to Detail:</strong> Every card is crafted to leave a lasting impression on your recipients.</li>
</ul>

<p>
    Make your event unforgettable from the very first impression. With <strong>Gregbuk’s Invitation Cards</strong>, your guests will receive a beautifully designed, high-quality card that communicates your celebration’s elegance and importance.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Create Your Invitation Cards Today</strong>
</a>
                         """, "alt_texts": "Invitation Cards \u2014 professional mockup for product listing.", "category_name": "invite", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Foil Invitations",
                         "description": "Premium invitations with metallic foil accents for elegance.",
                         "image_url": "foilinvite.jpeg", "content": """
                         <h3>Foil Invitations</h3>
<p>
    Add a touch of luxury and sophistication to your special occasions with <strong>Foil Invitations</strong>. Our foil printing techniques create stunning metallic accents that catch the light, making each invitation truly stand out. Perfect for weddings, galas, anniversaries, and premium corporate events.
</p>

<p>
    At <strong>Gregbuk</strong>, we offer a variety of foil finishes, including gold, silver, rose gold, and custom metallic colors. Combine with elegant typography, embossed details, or high-quality cardstock to craft invitations that are both memorable and visually striking.
</p>

<h4>Why Choose Foil Invitations?</h4>
<ul>
    <li><strong>Luxurious Metallic Finishes:</strong> Gold, silver, rose gold, and custom foil options.</li>
    <li><strong>Custom Designs:</strong> Tailored layouts, fonts, and graphics to match your event theme.</li>
    <li><strong>Premium Quality:</strong> High-grade cardstock ensures durability and a professional feel.</li>
    <li><strong>Memorable First Impression:</strong> Your guests will be captivated before even opening the envelope.</li>
    <li><strong>Versatile for All Events:</strong> Perfect for weddings, invitations, corporate events, and exclusive celebrations.</li>
</ul>

<p>
    Elevate your invitations with <strong>Gregbuk’s Foil Invitations</strong> and make every occasion truly unforgettable.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Design Your Foil Invitations Today</strong>
</a>
                         """, "alt_texts": "Foil Invitations \u2014 stack of multiple items showing variety.", "category_name": "foil-invite", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Holiday Cards", "description": "Festive cards for holidays and seasonal greetings.",
                         "image_url": "holiday-card.jpeg", "content": """
                         <h3>Holiday Cards</h3>
<p>
    Celebrate the season and spread joy with <strong>Holiday Cards</strong> that leave a lasting impression. At <strong>Gregbuk</strong>, we create vibrant, high-quality holiday cards tailored for personal, family, or corporate greetings. From classic designs to modern, playful layouts, each card reflects the spirit of the season.
</p>

<p>
    Choose from a variety of finishes including glossy, matte, or textured cardstock, and add custom messages, logos, or photos for a personal touch. Our professional printing ensures sharp colors, crisp images, and premium quality that your recipients will appreciate.
</p>

<h4>Why Choose Holiday Cards?</h4>
<ul>
    <li><strong>Customizable Designs:</strong> Personalize with photos, logos, or heartfelt messages.</li>
    <li><strong>Premium Printing:</strong> Crisp colors, sharp images, and high-quality cardstock.</li>
    <li><strong>Multiple Finishes:</strong> Glossy, matte, or textured options to match your style.</li>
    <li><strong>Perfect for All Occasions:</strong> Ideal for Christmas, New Year, Thanksgiving, and other seasonal greetings.</li>
    <li><strong>Corporate or Personal:</strong> Great for sending to clients, employees, friends, or family.</li>
</ul>

<p>
    Make your holiday greetings unforgettable with <strong>Gregbuk’s Holiday Cards</strong>—where creativity meets quality.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Create Your Holiday Cards Today</strong>
</a>
                         """, "alt_texts": "Holiday Cards \u2014 detail shot highlighting craftsmanship.", "category_name": "holi-cards", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Greeting Cards",
                         "description": "Beautifully designed cards to convey messages and well wishes.",
                         "image_url": "Greeting-card.jpeg", "content": """
                         <h3>Greeting Cards</h3>
<p>
    Express your thoughts, emotions, and well wishes with <strong>custom Greeting Cards</strong> from <strong>Gregbuk</strong>. Whether it’s a birthday, anniversary, thank-you note, or just a simple hello, our cards are designed to make every message memorable and heartfelt.
</p>

<p>
    Each card can be personalized with your own text, photos, or logos. We offer a wide selection of premium finishes—glossy, matte, or textured—to give your greetings a professional and elegant touch. With high-quality printing and attention to detail, your messages are guaranteed to stand out.
</p>

<h4>Why Choose Gregbuk Greeting Cards?</h4>
<ul>
    <li><strong>Fully Customizable:</strong> Add personal messages, images, or branding.</li>
    <li><strong>Premium Paper & Printing:</strong> Crisp, vibrant colors on quality cardstock.</li>
    <li><strong>Variety of Finishes:</strong> Choose between matte, glossy, or textured styles.</li>
    <li><strong>Versatile Use:</strong> Perfect for personal, business, or event greetings.</li>
    <li><strong>Memorable Impressions:</strong> Make every recipient feel special and appreciated.</li>
</ul>

<p>
    From heartfelt personal messages to professional corporate greetings, <strong>Gregbuk Greeting Cards</strong> are your go-to solution for elegant, high-quality printed cards that make every occasion memorable.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Create Your Greeting Cards Today</strong>
</a>
                         """, "alt_texts": "Greeting Cards \u2014 angled view showing texture and edges.", "category_name": "greet-cards", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Thank You Cards",
                         "description": "Express gratitude with custom-designed thank you cards.",
                         "image_url": "thankyou-card.jpeg", "content": """
                         <h3>Thank You Cards</h3>
<p>
    Show your appreciation with <strong>custom Thank You Cards</strong> from <strong>Gregbuk</strong>. Perfect for expressing gratitude to clients, customers, friends, or family, our cards help you leave a lasting, positive impression. Each card is thoughtfully designed to convey sincerity and professionalism.
</p>

<p>
    Personalize your Thank You Cards with your own message, images, or logo. Choose from a variety of premium paper stocks and finishes—matte, glossy, or textured—to match the tone and style of your appreciation. Our high-quality printing ensures every card looks polished and elegant.
</p>

<h4>Why Choose Gregbuk Thank You Cards?</h4>
<ul>
    <li><strong>Customizable Designs:</strong> Add your personal message, logo, or branding elements.</li>
    <li><strong>High-Quality Printing:</strong> Crisp, vibrant colors on durable cardstock.</li>
    <li><strong>Variety of Finishes:</strong> Matte, glossy, or textured options to suit any occasion.</li>
    <li><strong>Versatile Applications:</strong> Ideal for personal thank-yous, corporate appreciation, or event follow-ups.</li>
    <li><strong>Professional Presentation:</strong> Make every expression of gratitude feel meaningful and memorable.</li>
</ul>

<p>
    Whether you’re thanking a valued client or sending heartfelt personal notes, <strong>Gregbuk Thank You Cards</strong> make your appreciation tangible and beautifully presented.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Design Your Thank You Cards Today</strong>
</a>
                         """, "alt_texts": "Thank You Cards \u2014 close-up showing print detail and finish.", "category_name": "thanks-card", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Response Cards",
                         "description": "Convenient response cards to RSVP or collect feedback.",
                         "image_url": "response-card.jpeg", "content": """
                         <h3>Response Cards</h3>
<p>
    Make collecting RSVPs, feedback, or important information effortless with <strong>custom Response Cards</strong> from <strong>Gregbuk</strong>. Perfect for weddings, corporate events, parties, or surveys, these cards are designed to be clear, professional, and visually appealing.
</p>

<p>
    Personalize your Response Cards with your own design, branding, or messaging. Choose from a variety of high-quality paper stocks and finishes—matte, glossy, or textured—to ensure your cards are durable and make a lasting impression. Our precise printing ensures every detail, from text to graphics, is crisp and polished.
</p>

<h4>Why Choose Gregbuk Response Cards?</h4>
<ul>
    <li><strong>Customizable Layouts:</strong> Tailor your cards with lines, checkboxes, or text fields for easy responses.</li>
    <li><strong>High-Quality Printing:</strong> Clear, vibrant colors on premium cardstock for professional results.</li>
    <li><strong>Versatile Uses:</strong> Ideal for RSVP collection, surveys, feedback, or event responses.</li>
    <li><strong>Premium Finishes:</strong> Matte, glossy, or textured options to complement your event style.</li>
    <li><strong>Easy Distribution:</strong> Compact and convenient cards for mailing or handouts.</li>
</ul>

<p>
    With <strong>Gregbuk Response Cards</strong>, you can make responding simple, stylish, and memorable for your guests or clients.
</p>

<a href="/contact?head=Marketing" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    <strong>Create Your Custom Response Cards Today</strong>
</a>
                         """, "alt_texts": "Response Cards \u2014 product shot on white background.", "category_name": "response-card", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        },
        {
            "name": "Stickers & Labels",
            "description": "Custom stickers and labels designed for branding, packaging, and promotional purposes.",
            "image_url": "stickers&labels.jpeg",
            "icon_name": "#cil-tag",
            "category_name": "stickers-labels",
            "alt_texts": "Stickers & Labels service image",
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
    Stand out in a competitive market with professionally printed, high-quality <strong>custom labels and stickers</strong> from Gregbuk. Perfect for retail, food and beverage, cosmetics, and handmade products, our labels combine vibrant design, durability, and brand impact. <a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Order Your Labels Today</strong></a> and make every product unforgettable.
  </p>
            """,
            "products": [
                {"name": "Die-Cut Stickers",
                 "description": "Precision-cut stickers in custom shapes for creative branding.",
                 "image_url": "diecut.jpeg", "content": """
                 <h2>Die-Cut Stickers – Custom Shapes for Maximum Impact</h2>

<p>
Stand out from the crowd with <strong>Gregbuk’s die-cut stickers</strong>, expertly crafted to bring your creative vision to life. Unlike standard stickers, our die-cut stickers are precision-cut into any shape you desire—perfectly reflecting your brand identity or design concept. Whether you’re promoting a business, decorating products, or creating personalized gifts, these stickers provide a professional and memorable finish.
</p>

<h3>Why Choose Die-Cut Stickers?</h3>
<ul>
    <li><strong>Custom Shapes:</strong> From logos to fun designs, our die-cut process allows your stickers to take any shape, making them unique and instantly recognizable.</li>
    <li><strong>High-Quality Materials:</strong> Printed on durable, premium sticker paper that can withstand handling, scratches, and even outdoor conditions.</li>
    <li><strong>Vibrant Colors:</strong> Full-color printing ensures that every sticker pops with vibrant, crisp details that attract attention.</li>
    <li><strong>Versatile Uses:</strong> Perfect for product packaging, promotional giveaways, branding, marketing campaigns, events, scrapbooking, and personal projects.</li>
    <li><strong>Various Finishes:</strong> Choose from glossy, matte, or transparent finishes to match your brand style and desired aesthetic.</li>
</ul>

<h3>How to Use Die-Cut Stickers Effectively</h3>
<p>
Die-cut stickers aren’t just decorative—they’re a powerful branding tool. Use them to enhance packaging, seal envelopes, decorate merchandise, or give away at events. Businesses love them for their ability to reinforce brand identity, while individuals use them for crafts, personal projects, or gifts. With Gregbuk, every sticker is produced with precision to ensure a perfect cut and polished presentation.
</p>

<h3>Our Process</h3>
<p>
We guide you from design to delivery. Simply upload your artwork, select your preferred shape, size, and finish, and let our experts handle the rest. Our high-tech die-cutting machines ensure each sticker comes out clean, detailed, and professional, making your designs pop in ways that standard stickers cannot.
</p>

<h3>Why Gregbuk?</h3>
<ul>
    <li>Expert craftsmanship to ensure precise cuts and professional finishes</li>
    <li>Flexible order quantities—from a few stickers to large promotional runs</li>
    <li>Fast turnaround and reliable shipping</li>
    <li>Dedicated customer support to help with design and material selection</li>
</ul>

<p>
Make your brand or personal project unforgettable with <strong>custom die-cut stickers</strong> from Gregbuk. Bring creativity, color, and professional quality together in every sticker.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Start Your Die-Cut Sticker Order Today
</a>
                 """, "alt_texts": "Die-Cut Stickers \u2014 professional mockup for product listing.", "category_name": "die-cut", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Round Stickers",
                 "description": "Classic circular stickers ideal for packaging and promotions.",
                 "image_url": "round.jpeg", "content": """
                 <h2>Round Stickers – Classic Design with Endless Possibilities</h2>

<p>
Add a timeless touch to your branding and projects with <strong>Gregbuk’s round stickers</strong>. Their simple, circular shape makes them incredibly versatile while offering a professional and polished look. Ideal for packaging, promotions, labeling, and personal projects, round stickers are a go-to solution for businesses and individuals alike.
</p>

<h3>Why Choose Round Stickers?</h3>
<ul>
    <li><strong>Classic Shape:</strong> Perfectly round for a clean, elegant presentation that works in any context.</li>
    <li><strong>High-Quality Printing:</strong> Crisp, full-color prints that bring your designs to life.</li>
    <li><strong>Durable Material:</strong> Made from premium sticker paper that resists scratches, fading, and moisture.</li>
    <li><strong>Multiple Uses:</strong> Ideal for product packaging, sealing envelopes, event giveaways, crafts, scrapbooking, and more.</li>
    <li><strong>Flexible Finishes:</strong> Choose from glossy, matte, or transparent finishes to suit your brand or project aesthetic.</li>
</ul>

<h3>Perfect for Branding & Marketing</h3>
<p>
Round stickers are not just decorative—they reinforce your brand identity with every application. Use them on product packaging, promotional items, or as part of a marketing campaign to make your message memorable. Their clean, circular design ensures your logo, message, or artwork is showcased effectively and professionally.
</p>

<h3>Our Production Process</h3>
<p>
At Gregbuk, we combine precision printing with high-quality materials. Simply provide your artwork, select your size and finish, and we’ll produce vibrant, perfectly cut round stickers ready for any use. Our production process ensures consistency and professionalism in every sticker.
</p>

<h3>Why Gregbuk?</h3>
<ul>
    <li>High-quality materials and full-color printing for vibrant results</li>
    <li>Flexible quantities for small or large orders</li>
    <li>Fast turnaround to meet tight deadlines</li>
    <li>Expert support for design, size selection, and finishes</li>
</ul>

<p>
Make a lasting impression with <strong>round stickers</strong> from Gregbuk—perfect for your products, events, and creative projects.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Round Stickers Today
</a>
                 """, "alt_texts": "Round Stickers \u2014 detail shot highlighting craftsmanship.", "category_name": "round-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Rectangle Stickers",
                 "description": "Versatile rectangular stickers suitable for labels and branding.",
                 "image_url": "rectangle-sticker.jpeg", "content": """
                 <h2>Rectangle Stickers – Versatile & Professional Branding</h2>

<p>
Make your brand or message stand out with <strong>Gregbuk’s rectangle stickers</strong>. Their clean, straight-edged shape is perfect for labeling, product packaging, and promotional use. Rectangle stickers are versatile and practical while giving a modern, professional look that works across industries.
</p>

<h3>Why Choose Rectangle Stickers?</h3>
<ul>
    <li><strong>Versatile Shape:</strong> Ideal for branding, packaging, shipping labels, and creative projects.</li>
    <li><strong>High-Quality Printing:</strong> Full-color, crisp prints that ensure your designs look sharp and professional.</li>
    <li><strong>Durable Material:</strong> Crafted from premium sticker paper that resists water, fading, and tearing.</li>
    <li><strong>Multiple Uses:</strong> Perfect for product labels, promotional giveaways, address labels, crafts, and more.</li>
    <li><strong>Flexible Finishes:</strong> Available in glossy, matte, and transparent options for a custom look.</li>
</ul>

<h3>Perfect for Branding & Organization</h3>
<p>
Rectangle stickers offer a clean canvas for logos, text, and artwork, making them ideal for businesses and personal projects alike. They can be applied to packaging, envelopes, folders, or any surface that needs a professional and polished touch.
</p>

<h3>Our Production Process</h3>
<p>
At Gregbuk, we use precise cutting techniques combined with high-quality printing to ensure each rectangle sticker is perfect. Choose your size, finish, and quantity, and we’ll create stickers that are vibrant, durable, and ready for use.
</p>

<h3>Why Gregbuk?</h3>
<ul>
    <li>Premium materials and full-color printing for professional results</li>
    <li>Flexible order quantities to suit small or bulk needs</li>
    <li>Fast turnaround to meet your deadlines</li>
    <li>Expert guidance on design, size, and finishes</li>
</ul>

<p>
Elevate your branding and projects with <strong>rectangle stickers</strong> from Gregbuk—versatile, professional, and designed to impress.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Rectangle Stickers Today
</a>
                 """, "alt_texts": "Rectangle Stickers \u2014 professional mockup for product listing.", "category_name": "rect-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Custom Shape Sticker",
                 "description": "Stickers cut into any shape to match your brand's unique identity.",
                 "image_url": "custom-shape.jpeg", "content": """
                 <h2>Custom Shape Stickers – Unique Designs for Your Brand</h2>

<p>
Bring your ideas to life with <strong>Gregbuk’s custom shape stickers</strong>. Unlike standard shapes, these stickers are precision-cut to match your logo, artwork, or any design you envision. Perfect for businesses, events, or personal projects, they make your branding stand out in a truly unique way.
</p>

<h3>Why Choose Custom Shape Stickers?</h3>
<ul>
    <li><strong>Tailored Designs:</strong> Any shape you can imagine—from logos to illustrations—crafted to perfection.</li>
    <li><strong>High-Quality Printing:</strong> Vibrant, full-color prints ensure your design pops on any surface.</li>
    <li><strong>Durable Material:</strong> Premium adhesive and sticker materials that resist water, fading, and peeling.</li>
    <li><strong>Versatile Uses:</strong> Ideal for branding, giveaways, product packaging, promotions, and creative projects.</li>
    <li><strong>Custom Finishes:</strong> Available in matte, glossy, or transparent finishes to suit your design aesthetic.</li>
</ul>

<h3>Stand Out with Every Detail</h3>
<p>
Custom shape stickers turn ordinary surfaces into extraordinary branding opportunities. Each sticker is carefully cut to your specifications, creating a polished, professional appearance that leaves a lasting impression on your customers and audience.
</p>

<h3>Our Production Process</h3>
<p>
At Gregbuk, we combine advanced printing techniques with precise die-cutting to deliver stickers that match your exact vision. Simply provide your artwork or let our design team assist in creating a sticker that represents your brand with creativity and style.
</p>

<h3>Why Gregbuk?</h3>
<ul>
    <li>Custom sizes and shapes to perfectly reflect your brand identity</li>
    <li>Premium materials for durability and professional finish</li>
    <li>Flexible order quantities—from a few pieces to bulk orders</li>
    <li>Fast turnaround and expert support for every project</li>
</ul>

<p>
Make your brand unforgettable with <strong>custom shape stickers</strong> from Gregbuk—where creativity meets quality.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Design Your Custom Shape Stickers Today
</a>
                 """, "alt_texts": "Custom Shape Sticker \u2014 product shot on white background.", "category_name": "custom-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Oval Sticker",
                 "description": "Stylish oval stickers perfect for packaging or product labels.",
                 "image_url": "oval-sticker.jpeg", "content": """
                 <h2>Oval Stickers – Sleek & Stylish Branding</h2>

<p>
Add elegance and versatility to your branding with <strong>Gregbuk’s oval stickers</strong>. Their smooth, rounded design makes them perfect for product labels, packaging, giveaways, and promotional materials. Oval stickers provide a professional and distinctive look that captures attention effortlessly.
</p>

<h3>Why Choose Oval Stickers?</h3>
<ul>
    <li><strong>Elegant Design:</strong> The oval shape offers a refined appearance that stands out on products and packaging.</li>
    <li><strong>Vibrant Printing:</strong> Full-color printing ensures your logo, artwork, or message looks crisp and eye-catching.</li>
    <li><strong>Durable Material:</strong> Long-lasting adhesive and high-quality sticker material resist peeling, tearing, and fading.</li>
    <li><strong>Multiple Uses:</strong> Ideal for product labels, branding, event giveaways, and promotional campaigns.</li>
    <li><strong>Customizable Finishes:</strong> Available in glossy, matte, or transparent finishes to perfectly complement your design.</li>
</ul>

<h3>Professional Branding in Every Detail</h3>
<p>
Oval stickers provide a unique opportunity to highlight your brand with sophistication. Their smooth edges and balanced shape make your message or logo easily recognizable while adding a polished, professional touch.
</p>

<h3>Gregbuk’s Production Quality</h3>
<p>
We use high-precision printing and durable materials to ensure each oval sticker meets your brand standards. Whether for small promotional batches or large-scale production, Gregbuk delivers stickers that impress every time.
</p>

<h3>Why Choose Gregbuk?</h3>
<ul>
    <li>Custom sizes to perfectly suit your brand and packaging</li>
    <li>Premium materials for a professional, long-lasting finish</li>
    <li>Flexible order quantities to match your project needs</li>
    <li>Expert guidance and fast production for every order</li>
</ul>

<p>
Make your branding stand out with <strong>oval stickers</strong> from Gregbuk—elegant, durable, and uniquely yours.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Create Your Oval Stickers Today
</a>
                 """, "alt_texts": "Oval Sticker \u2014 product shot on white background.", "category_name": "oval-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Square Sticker",
                 "description": "Square-shaped stickers for labels, promotions, and giveaways.",
                 "image_url": "square-sticker.jpeg", "content": """
                 <h2>Square Stickers – Bold & Versatile Branding</h2>

<p>
Make a strong impression with <strong>Gregbuk’s square stickers</strong>. Their clean, modern lines provide a professional look that works perfectly for product labels, packaging, promotions, and giveaways. Square stickers offer a balanced, eye-catching format that enhances your brand’s visibility.
</p>

<h3>Why Choose Square Stickers?</h3>
<ul>
    <li><strong>Modern Design:</strong> The square shape delivers a contemporary, professional appearance for any project.</li>
    <li><strong>Vibrant Printing:</strong> Full-color printing ensures your logo, artwork, or message is crisp, clear, and impactful.</li>
    <li><strong>Durable Material:</strong> High-quality adhesive and sticker materials resist peeling, tearing, and fading, even on rough surfaces.</li>
    <li><strong>Customizable Sizes:</strong> Available in multiple sizes to fit packaging, envelopes, promotional items, or creative projects.</li>
    <li><strong>Flexible Finishes:</strong> Choose glossy, matte, or transparent finishes for a personalized, polished look.</li>
</ul>

<h3>Professional Branding with Every Sticker</h3>
<p>
Square stickers provide versatility for any occasion, from retail packaging to event giveaways. Their clean edges and proportionate shape ensure your brand message is clear, memorable, and visually striking.
</p>

<h3>Gregbuk’s Quality Promise</h3>
<p>
We combine high-resolution printing with durable materials to produce square stickers that elevate your brand. Whether for small promotional batches or large-scale branding, each sticker meets our strict quality standards.
</p>

<h3>Why Choose Gregbuk?</h3>
<ul>
    <li>Custom sizes and finishes to perfectly suit your brand</li>
    <li>High-quality, durable materials for lasting impact</li>
    <li>Flexible order quantities for any project size</li>
    <li>Expert guidance and fast, reliable production</li>
</ul>

<p>
Enhance your branding with <strong>square stickers</strong> from Gregbuk—bold, versatile, and designed to impress.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Square Stickers Today
</a>
                 """, "alt_texts": "Square Sticker \u2014 detail shot highlighting craftsmanship.", "category_name": "square-sticker", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Custom Roll Labels",
                 "description": "High-quality roll labels for bulk packaging or industrial use.",
                 "image_url": "custom-roll.jpeg", "content": """
                 <h2>Custom Roll Labels – Efficient & Professional</h2>

<p>
Streamline your branding with <strong>Gregbuk’s Custom Roll Labels</strong>. Perfect for bulk packaging, product labeling, or industrial use, these labels offer a professional, consistent look while saving time and effort during application. Ideal for businesses of all sizes, roll labels provide a practical and polished solution.
</p>

<h3>Why Choose Custom Roll Labels?</h3>
<ul>
    <li><strong>High-Quality Printing:</strong> Crisp, vibrant colors and sharp details for logos, text, and artwork.</li>
    <li><strong>Durable Materials:</strong> Resistant to moisture, tearing, and fading, ensuring labels remain intact throughout handling and shipping.</li>
    <li><strong>Easy Application:</strong> Rolls are compatible with label dispensers and printing machines, making mass labeling efficient and hassle-free.</li>
    <li><strong>Custom Sizes & Shapes:</strong> Tailor each roll to suit your packaging needs—round, square, rectangular, or custom die-cut shapes.</li>
    <li><strong>Professional Finish:</strong> Glossy, matte, or semi-gloss finishes available to match your brand’s aesthetic.</li>
</ul>

<h3>Streamline Your Packaging</h3>
<p>
Whether you’re labeling food products, cosmetics, industrial parts, or promotional items, <strong>custom roll labels</strong> give you the flexibility and professional appearance your brand deserves. Each label is printed with precision and care to maintain consistent quality across every roll.
</p>

<h3>Gregbuk’s Commitment to Quality</h3>
<p>
We combine premium materials, high-resolution printing, and expert finishing techniques to create roll labels that enhance your brand identity. From small-scale production to large manufacturing runs, our labels deliver consistent quality and reliability.
</p>

<h3>Why Choose Gregbuk?</h3>
<ul>
    <li>Custom sizes, shapes, and finishes for your specific needs</li>
    <li>Durable, long-lasting materials for any application</li>
    <li>Flexible order quantities for small businesses or large industries</li>
    <li>Fast, reliable turnaround with attention to detail</li>
</ul>

<p>
Maximize efficiency and brand impact with <strong>Custom Roll Labels</strong> from Gregbuk—professional, versatile, and designed for excellence.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Custom Roll Labels Today
</a>
                 """, "alt_texts": "Custom Roll Labels \u2014 angled view showing texture and edges.", "category_name": "cr-labels", "image_collection": [choice(imgg) for n in range(8)]},
                {"name": "Sheet Labels",
                 "description": "High-quality sheet labels for bulk packaging or industrial use.",
                 "image_url": "sheetLABEL.jpeg", "content": """
                 <h2>Sheet Labels – Versatile & Professional</h2>

<p>
Create precise, high-quality labels with <strong>Gregbuk’s Sheet Labels</strong>. Ideal for small-scale packaging, office labeling, or custom projects, these labels are versatile and easy to apply. Perfect for businesses, schools, and personal use, sheet labels provide a reliable solution for all your labeling needs.
</p>

<h3>Why Choose Sheet Labels?</h3>
<ul>
    <li><strong>Professional Quality:</strong> Crisp, sharp printing ensures your designs, logos, and text look polished and clear.</li>
    <li><strong>Durable Materials:</strong> Resistant to smudging, tearing, and fading, keeping your labels looking perfect over time.</li>
    <li><strong>Easy to Use:</strong> Convenient sheets are compatible with standard printers, allowing you to print and apply labels with ease.</li>
    <li><strong>Customizable:</strong> Available in a variety of sizes, shapes, and finishes—rectangular, round, square, or custom die-cut designs.</li>
    <li><strong>Professional Finish:</strong> Choose from matte, glossy, or semi-gloss finishes to suit your brand’s style and your project needs.</li>
</ul>

<h3>Perfect for Every Application</h3>
<p>
Whether labeling products, organizing documents, creating promotional materials, or adding a personal touch to gifts, <strong>sheet labels</strong> provide a simple yet professional solution. Each sheet is designed for accurate placement and consistent quality.
</p>

<h3>Gregbuk’s Expertise</h3>
<p>
With years of experience in printing and design, Gregbuk ensures that every sheet label meets high standards for quality, durability, and appearance. From single sheets to bulk orders, we deliver professional results tailored to your requirements.
</p>

<h3>Why Choose Gregbuk?</h3>
<ul>
    <li>Custom sizes, shapes, and finishes for your specific labeling needs</li>
    <li>High-quality, long-lasting materials for any project</li>
    <li>Flexible order quantities suitable for businesses, schools, or personal use</li>
    <li>Fast, reliable service with attention to detail</li>
</ul>

<p>
Enhance your organization, packaging, or branding with <strong>Sheet Labels</strong> from Gregbuk—professional, flexible, and designed for quality.
</p>

<a href="/contact?head=stickers-labels" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Sheet Labels Today
</a>
                 """, "alt_texts": "Sheet Labels \u2014 professional mockup for product listing.", "category_name": "sheet-labels", "image_collection": [choice(imgg) for n in range(8)]}
            ]
        },
        {
            "name": "Signs & Banners",
            "description": "Professional signage and banners to showcase your brand, events, or promotions.",
            "image_url": "signs&banners.jpeg",
            "icon_name": "#cil-notes",
            "alt_texts": "Signs and Banners service image",
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
  <a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Contact Us Now</strong></a>
            """,
            "subservices": [
                {
                    "name": "Banners",
                    "description": "High-quality banners for indoor and outdoor events, customized to your needs.",
                    "image_url": "banners.jpeg",
                    "alt_texts": "Banners service image",
                    "content": """
                    <section>
  <h2>Custom Banners</h2>
  <p>
    Make your brand stand out at any event with our high-quality custom banners.  
    Whether for indoor trade shows, outdoor advertising, or special events,  
    we deliver durable and eye-catching designs tailored to your needs.
  </p>

  <h3>Our Banner Options</h3>
  <ul>
    <li><strong>Vinyl Banners:</strong> Durable and vibrant banners for long-term use and promotions.</li>
    <li><strong>Fabric Banners:</strong> Premium fabric with a soft texture and professional finish.</li>
    <li><strong>Mesh Banners:</strong> Wind-resistant material ideal for outdoor installations.</li>
    <li><strong>X Banner Stands:</strong> Portable, lightweight banners perfect for trade shows and events.</li>
    <li><strong>Step & Repeat Banners:</strong> Branded backdrops ideal for photoshoots, red carpets, and events.</li>
    <li><strong>Pop-Up Displays:</strong> Quick and easy banner stands for instant professional setups.</li>
    <li><strong>Branded Tablecloths:</strong> Full-cover table designs that reinforce your brand presence.</li>
    <li><strong>Table Runners:</strong> Custom runners to complement event or trade show tables.</li>
  </ul>

  <h3>Why Choose Our Banners?</h3>
  <ul>
    <li>High-resolution printing for bold and vivid colors</li>
    <li>Durable materials suited for both indoor and outdoor use</li>
    <li>Portable and reusable designs for convenience</li>
    <li>Perfect for advertising, exhibitions, and promotional events</li>
  </ul>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Banner Quote
  </a>
                    """,
                    "category_name": "banner",
                    "products": [
                        {"name": "Vinyl Banner",
                         "description": "Durable and vibrant vinyl banners suitable for long-term display.",
                         "image_url": "vynly-banner.jpeg", "content": """
                         <h1>Vinyl Banners – Custom Printed for Maximum Impact</h1>

<h2>Durable and Vibrant Vinyl Banners for Any Occasion</h2>
<p>
Make your brand, event, or promotion impossible to miss with our <strong>high-quality vinyl banners</strong>. Designed for both indoor and outdoor use, these banners offer vibrant colors, long-lasting durability, and a professional finish that ensures your message stands out. Whether it’s for a storefront, a grand opening, an exhibition, or an outdoor event, our vinyl banners are engineered to deliver excellent results under any condition.
</p>

<h2>Custom Sizes and Designs</h2>
<p>
At Gregbuk, we understand that every event or marketing campaign is unique. That’s why our <strong>vinyl banners</strong> are fully customizable in size, shape, and design. Choose from a variety of finishes, including matte and glossy, and upload your own artwork or use our professional design templates to create a banner that perfectly reflects your brand identity.
</p>

<h2>Why Choose Vinyl Banners?</h2>
<ul>
  <li><strong>Weather-Resistant:</strong> Made from premium vinyl, these banners withstand rain, sun, and wind, maintaining their vibrant colors and structure outdoors.</li>
  <li><strong>High-Quality Print:</strong> Our advanced printing technology ensures sharp images, bold text, and consistent colors for maximum visibility.</li>
  <li><strong>Versatile Usage:</strong> Perfect for promotional events, store openings, trade shows, exhibitions, and community events.</li>
  <li><strong>Easy Installation:</strong> Add grommets, poles, or stands for hassle-free hanging and display.</li>
  <li><strong>Long-Lasting:</strong> Durable material and professional finishing ensure your banner remains effective for months or even years.</li>
</ul>

<h2>Customizable Options</h2>
<p>
You can personalize your vinyl banner to meet your specific needs:
</p>
<ul>
  <li>Various sizes and dimensions</li>
  <li>Full-color printing and sharp imagery</li>
  <li>Matte or glossy finishes</li>
  <li>Optional reinforcement and grommets for hanging</li>
  <li>Edge-sealing for extra durability</li>
</ul>

<h2>Professional Guidance</h2>
<p>
Not sure how to create the perfect design? Our team at Gregbuk can assist with layout, graphics, and content to ensure your <strong>vinyl banner</strong> communicates your message effectively and professionally.
</p>

<h2>Order Your Vinyl Banner Today</h2>
<p>
Make a bold statement and capture your audience’s attention with a custom <strong>vinyl banner</strong> from Gregbuk. Start your project online, customize your size and design, and let us deliver a banner that helps your brand shine.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Vinyl Banners</strong>
</a>
                         """, "alt_texts": "Vinyl Banner \u2014 professional mockup for product listing.", "category_name": "vinyl", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Fabric Banner",
                         "description": "Premium fabric banners with a professional finish and soft texture.",
                         "image_url": "fabric-banner.jpeg", "content": """
                         <h1>Fabric Banners – Elegant, Premium Displays</h1>

<h2>High-Quality Fabric Banners for Sophisticated Branding</h2>
<p>
Elevate your brand presence with <strong>custom fabric banners</strong> from Gregbuk. Perfect for indoor events, trade shows, retail spaces, and corporate presentations, these banners combine elegance with professional-quality printing. Fabric banners offer a soft texture, premium finish, and an upscale appearance that makes your message stand out with style.
</p>

<h2>Custom Designs and Finishes</h2>
<p>
Our <strong>fabric banners</strong> are fully customizable to meet your unique needs. Choose your ideal size, shape, and design, and select from a variety of high-end finishes that enhance the overall look of your banner. Whether you want a sleek matte finish or a subtle satin sheen, Gregbuk ensures every banner delivers a polished and professional impression.
</p>

<h2>Why Choose Fabric Banners?</h2>
<ul>
  <li><strong>Premium Material:</strong> Made from high-quality fabrics that drape beautifully and feel luxurious to the touch.</li>
  <li><strong>Vibrant, Long-Lasting Print:</strong> Advanced printing technology preserves rich colors and sharp details.</li>
  <li><strong>Indoor Excellence:</strong> Ideal for conferences, exhibitions, events, and office displays where sophistication is key.</li>
  <li><strong>Reusable and Durable:</strong> Lightweight yet resilient, these banners can be used repeatedly without losing quality.</li>
  <li><strong>Professional Finish:</strong> Precision hemmed edges and optional pole pockets for a flawless display.</li>
</ul>

<h2>Customizable Options</h2>
<p>
Enhance your banner with a range of personalization options:
</p>
<ul>
  <li>Multiple sizes and shapes</li>
  <li>Full-color high-resolution printing</li>
  <li>Matte, satin, or textured finishes</li>
  <li>Optional grommets or pole pockets for hanging</li>
  <li>Custom stitching and edge reinforcement for added durability</li>
</ul>

<h2>Professional Design Assistance</h2>
<p>
Need help creating a visually stunning banner? Our Gregbuk design team can provide expert guidance on layouts, graphics, and branding, ensuring your fabric banner effectively communicates your message and leaves a lasting impression.
</p>

<h2>Order Your Fabric Banner Today</h2>
<p>
Showcase your brand with a touch of elegance using a custom <strong>fabric banner</strong> from Gregbuk. Customize your design online, select your finish, and let us deliver a banner that elevates your brand image.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Fabric Banners</strong>
</a>
                         """, "alt_texts": "Fabric Banner \u2014 in-use photo demonstrating scale.", "category_name": "fabric", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Mesh Banners", "description": "Wind-resistant mesh banners ideal for outdoor use.",
                         "image_url": "mesh-perforated-banner.webp", "content": """
                         <h1>Mesh Banners – Durable, Outdoor-Ready Displays</h1>

<h2>High-Impact Mesh Banners for Outdoor Branding</h2>
<p>
Make your brand impossible to miss with <strong>custom mesh banners</strong> from Gregbuk. Designed specifically for outdoor use, mesh banners are made from durable, perforated materials that withstand wind, rain, and sunlight while maintaining vibrant, eye-catching graphics. Perfect for construction sites, outdoor events, sports arenas, or street promotions, these banners deliver maximum visibility without compromising quality.
</p>

<h2>Why Choose Mesh Banners?</h2>
<ul>
  <li><strong>Weather-Resistant Material:</strong> Perforated vinyl ensures that wind passes through without tearing the banner.</li>
  <li><strong>Vibrant, Long-Lasting Print:</strong> High-resolution printing maintains sharp graphics and bold colors even under harsh outdoor conditions.</li>
  <li><strong>Durable and Reusable:</strong> Strong, reinforced edges and grommets allow multiple installations without damage.</li>
  <li><strong>Wide Applications:</strong> Perfect for construction sites, fences, sports events, concerts, festivals, or street marketing campaigns.</li>
  <li><strong>Lightweight and Portable:</strong> Easy to transport and install without heavy equipment.</li>
</ul>

<h2>Customizable Options</h2>
<p>
Gregbuk allows full customization of your mesh banner to suit your brand and environment:
</p>
<ul>
  <li>Various sizes from small promotional banners to large-scale outdoor displays</li>
  <li>Optional reinforced edges and double-stitched hems</li>
  <li>Custom grommet placement for secure installation</li>
  <li>Full-color, high-resolution print for bold and readable visuals</li>
  <li>Wind slits for extra stability in high-wind locations</li>
</ul>

<h2>Applications and Uses</h2>
<p>
Mesh banners are ideal for:
</p>
<ul>
  <li>Construction site branding</li>
  <li>Sports and concert events</li>
  <li>Outdoor trade shows and exhibitions</li>
  <li>Street-level promotions and campaigns</li>
  <li>Temporary storefront signage</li>
</ul>

<h2>Professional Design Support</h2>
<p>
Our expert design team at Gregbuk is ready to assist you in creating a banner that maximizes brand impact. From selecting bold colors and readable fonts to arranging graphics for outdoor visibility, we ensure your mesh banner captures attention effectively.
</p>

<h2>Order Your Mesh Banner Today</h2>
<p>
Boost your outdoor marketing efforts with a <strong>custom mesh banner</strong> from Gregbuk. Durable, weather-resistant, and visually striking, it’s the perfect solution for any high-traffic outdoor environment.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Mesh Banners</strong>
</a>
                         """, "alt_texts": "Mesh Banners \u2014 styled mockup with props for context.", "category_name": "mesh", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "X Banner Stands",
                         "description": "Portable X-frame banners perfect for trade shows and events.",
                         "image_url": "x-stand.jpeg", "content": """
                         <h1>X Banner Stands – Portable, Professional Displays</h1>

<h2>Lightweight, High-Impact X Banner Stands</h2>
<p>
Showcase your brand anywhere with <strong>X Banner Stands</strong> from Gregbuk. These portable and easy-to-assemble banner stands are perfect for trade shows, retail promotions, corporate events, and exhibitions. Combining convenience with professional presentation, X Banner Stands are ideal for businesses looking to make an immediate impact without complicated setup.
</p>

<h2>Why Choose X Banner Stands?</h2>
<ul>
  <li><strong>Portable and Lightweight:</strong> Easy to carry, set up, and take down, perfect for mobile marketing and events.</li>
  <li><strong>Professional Presentation:</strong> Displays your graphics in a clean, vertical format that attracts attention.</li>
  <li><strong>Durable Construction:</strong> Built with high-quality aluminum frames and sturdy components for repeated use.</li>
  <li><strong>Cost-Effective Marketing:</strong> Reusable and affordable solution for long-term brand visibility.</li>
</ul>

<h2>Customization Options</h2>
<p>
At Gregbuk, we ensure your X Banner Stand matches your brand’s identity and event requirements:
</p>
<ul>
  <li>Multiple sizes to fit standard or custom banner dimensions</li>
  <li>Full-color, high-resolution prints to make your message pop</li>
  <li>Optional carrying cases for easy transport</li>
  <li>Easy graphic replacement for quick updates or seasonal campaigns</li>
  <li>Single or double-sided display for maximum visibility</li>
</ul>

<h2>Applications</h2>
<p>
X Banner Stands are perfect for:
</p>
<ul>
  <li>Trade shows and exhibitions</li>
  <li>Retail promotions and in-store displays</li>
  <li>Corporate events, conferences, and meetings</li>
  <li>Pop-up shops and temporary installations</li>
  <li>Marketing campaigns at schools, malls, or public events</li>
</ul>

<h2>Design Support</h2>
<p>
Our design team works with you to ensure your X Banner Stand communicates your brand effectively. From choosing the right layout and colors to highlighting key messaging, we ensure your display captures attention and conveys professionalism.
</p>

<h2>Order Your X Banner Stand Today</h2>
<p>
Make your brand stand out at any event with a <strong>custom X Banner Stand</strong> from Gregbuk. Portable, stylish, and professional, it’s the ideal solution for businesses seeking flexible and impactful displays.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About X Banner Stands</strong>
</a>
                         """, "alt_texts": "X Banner Stands \u2014 detail shot highlighting craftsmanship.", "category_name": "x-banner", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Step & Repeat Banners",
                         "description": "Custom step-and-repeat banners for photo backdrops and branding.",
                         "image_url": "StepandRepeat.jpeg", "content": """
                         <h1>Step & Repeat Banners – Red Carpet Ready Branding</h1>

<h2>Elevate Your Brand with Step & Repeat Banners</h2>
<p>
Make every photo opportunity unforgettable with <strong>Step & Repeat Banners</strong> from Gregbuk. Perfect for red carpet events, corporate galas, award shows, press conferences, and product launches, these banners prominently display your logo, tagline, or sponsorships repeatedly in a clean, visually striking layout. Ideal for professional photography backdrops, your brand will be the star of every shot.
</p>

<h2>Key Features & Benefits</h2>
<ul>
  <li><strong>Custom Branding:</strong> Showcase your logos, slogans, and graphics in a repeating pattern that reinforces brand recognition.</li>
  <li><strong>Professional Appearance:</strong> Crisp, high-resolution printing ensures every photo looks polished and eye-catching.</li>
  <li><strong>Durable Materials:</strong> Made from premium vinyl or fabric options for a long-lasting, wrinkle-resistant backdrop.</li>
  <li><strong>Versatile Display:</strong> Ideal for events of all sizes, both indoor and outdoor, from small photo corners to large-scale red carpets.</li>
</ul>

<h2>Customization Options</h2>
<p>
Gregbuk provides full customization to meet your event needs:
</p>
<ul>
  <li>Multiple sizes and dimensions for small to large event spaces</li>
  <li>Single or double-sided printing for maximum visibility</li>
  <li>Optional stands, poles, and base supports for easy setup and stability</li>
  <li>Custom layout design to ensure logos are consistently visible in every shot</li>
  <li>Choice of materials: vinyl for durability, fabric for elegance, or matte finishes for reduced glare</li>
</ul>

<h2>Applications</h2>
<p>
Step & Repeat Banners are perfect for:
</p>
<ul>
  <li>Red carpet events and media walls</li>
  <li>Corporate launches, award ceremonies, and press conferences</li>
  <li>Trade shows, expos, and promotional events</li>
  <li>Photo booths, influencer activations, and social media content creation</li>
</ul>

<h2>Design Support & Guidance</h2>
<p>
Our experienced design team helps you create a layout that maximizes brand exposure. We ensure that every logo placement, color, and graphic is optimized for professional photography, giving your brand maximum impact at every event.
</p>

<h2>Order Your Step & Repeat Banner Today</h2>
<p>
Turn every event into a professional marketing opportunity with a <strong>custom Step & Repeat Banner</strong> from Gregbuk. Sleek, durable, and visually striking, these banners make your brand unforgettable.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Step & Repeat Banners</strong>
</a>
                         """, "alt_texts": "Step & Repeat Banners \u2014 close-up showing print detail and finish.", "category_name": "step-repeat", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Pop Up Display",
                         "description": "Quick and easy pop-up banners for instant presentation setups.",
                         "image_url": "popup.jpeg", "content": """
                         <h1>Pop-Up Displays – Instant, Impactful Branding</h1>

<h2>Portable Pop-Up Displays for Every Event</h2>
<p>
Make a lasting impression with <strong>Pop-Up Displays</strong> from Gregbuk. Perfect for trade shows, exhibitions, promotional events, and retail activations, these displays provide a quick, professional, and visually striking setup that highlights your brand and message. Lightweight, portable, and easy to assemble, Pop-Up Displays are the go-to solution for businesses on the move.
</p>

<h2>Features & Benefits</h2>
<ul>
  <li><strong>Quick Assembly:</strong> Set up in minutes without tools or professional help.</li>
  <li><strong>Vibrant Printing:</strong> High-resolution graphics ensure your brand stands out in any environment.</li>
  <li><strong>Durable Materials:</strong> Sturdy frames and premium fabric or vinyl panels for repeated use.</li>
  <li><strong>Portable Design:</strong> Lightweight and compact, perfect for transport and storage.</li>
  <li><strong>Customizable:</strong> Fully tailored to your branding, including size, colors, and graphics.</li>
</ul>

<h2>Types of Pop-Up Displays</h2>
<ul>
  <li><strong>Standard Pop-Up Display:</strong> Ideal for small booths and quick setups.</li>
  <li><strong>Curved Pop-Up Display:</strong> Sleek, curved design for maximum visibility and modern aesthetics.</li>
  <li><strong>Fabric Pop-Up Display:</strong> Soft, seamless printing with easy fabric replacement.</li>
  <li><strong>Backlit Pop-Up Display:</strong> Illuminated panels for a professional and eye-catching presentation.</li>
  <li><strong>Tabletop Pop-Up Display:</strong> Compact solution for counters, receptions, or small event areas.</li>
</ul>

<h2>Applications</h2>
<p>
Pop-Up Displays are perfect for:
</p>
<ul>
  <li>Trade shows, exhibitions, and product launches</li>
  <li>Corporate events, networking, and conferences</li>
  <li>Retail promotions and brand activations</li>
  <li>Marketing campaigns, photo opportunities, and presentations</li>
</ul>

<h2>Design & Printing Excellence</h2>
<p>
At Gregbuk, our expert design team ensures that every display is visually impactful, with crisp graphics, consistent colors, and branding elements aligned for maximum exposure. We provide guidance on layout, size, and materials so your Pop-Up Display truly reflects your brand identity.
</p>

<h2>Order Your Pop-Up Display Today</h2>
<p>
Bring your brand to life instantly with a <strong>custom Pop-Up Display</strong> from Gregbuk. Portable, professional, and attention-grabbing, these displays are perfect for every event and marketing opportunity.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Pop-Up Displays</strong>
</a>
                         """, "alt_texts": "Pop Up Display \u2014 professional mockup for product listing.", "category_name": "pop-up", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Tablecloths",
                         "description": "Branded table covers for events, trade shows, and promotions.",
                         "image_url": "tablecloth.jpeg", "content": """
                         <h1>Branded Tablecloths & Table Runners – Elevate Your Event Presence</h1>

<h2>Make Every Table a Statement</h2>
<p>
Create a lasting impression at trade shows, corporate events, retail promotions, or exhibitions with <strong>custom Branded Tablecloths & Table Runners</strong> from Gregbuk. Our high-quality, fully customizable designs ensure that every table reflects your brand’s professionalism, style, and message.
</p>

<h2>Why Choose Branded Table Covers?</h2>
<ul>
  <li><strong>Professional Look:</strong> Transform ordinary tables into attention-grabbing marketing displays.</li>
  <li><strong>Custom Printing:</strong> Full-color printing on premium fabrics ensures your logo, colors, and graphics pop.</li>
  <li><strong>Durable Materials:</strong> Long-lasting fabrics designed for repeated use at multiple events.</li>
  <li><strong>Easy Setup:</strong> Lightweight, wrinkle-resistant, and simple to place on any table size.</li>
  <li><strong>Versatile Options:</strong> Choose from full tablecloths, fitted styles, or stylish table runners to match your event.</li>
</ul>

<h2>Types of Table Covers</h2>
<ul>
  <li><strong>Full Tablecloths:</strong> Complete coverage for a polished, branded presentation.</li>
  <li><strong>Fitted Table Covers:</strong> Stretch-fit designs for a sleek and modern appearance.</li>
  <li><strong>Table Runners:</strong> Highlight your branding while keeping part of the table visible for displays or materials.</li>
  <li><strong>Fabric & Vinyl Options:</strong> Choose the best material for indoor or outdoor events.</li>
</ul>

<h2>Applications & Use Cases</h2>
<p>
Branded Tablecloths & Table Runners are perfect for:
</p>
<ul>
  <li>Trade shows, expos, and product launches</li>
  <li>Corporate meetings, seminars, and workshops</li>
  <li>Retail events, pop-up stores, and marketing activations</li>
  <li>Conferences, networking events, and receptions</li>
</ul>

<h2>Design Excellence</h2>
<p>
Gregbuk’s design team works closely with you to ensure that every table cover represents your brand in the best light. From logo placement to color harmony and high-resolution printing, we guarantee that your branded table displays will captivate your audience and elevate your event’s visual appeal.
</p>

<h2>Order Your Branded Table Covers Today</h2>
<p>
Stand out at every event with <strong>custom Branded Tablecloths & Table Runners</strong> from Gregbuk. Professional, durable, and stylish, these table covers turn every setup into a branding opportunity.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Table Covers</strong>
</a>
                         """, "alt_texts": "Tablecloths \u2014 angled view showing texture and edges.", "category_name": "tbc", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Table Runners",
                         "description": "Custom table runners to complement your branded setup.",
                         "image_url": "table-runner.jpeg", "content": """
                         <h1>Branded Tablecloths & Table Runners – Elevate Your Event Presence</h1>

<h2>Make Every Table a Statement</h2>
<p>
Create a lasting impression at trade shows, corporate events, retail promotions, or exhibitions with <strong>custom Branded Tablecloths & Table Runners</strong> from Gregbuk. Our high-quality, fully customizable designs ensure that every table reflects your brand’s professionalism, style, and message.
</p>

<h2>Why Choose Branded Table Covers?</h2>
<ul>
  <li><strong>Professional Look:</strong> Transform ordinary tables into attention-grabbing marketing displays.</li>
  <li><strong>Custom Printing:</strong> Full-color printing on premium fabrics ensures your logo, colors, and graphics pop.</li>
  <li><strong>Durable Materials:</strong> Long-lasting fabrics designed for repeated use at multiple events.</li>
  <li><strong>Easy Setup:</strong> Lightweight, wrinkle-resistant, and simple to place on any table size.</li>
  <li><strong>Versatile Options:</strong> Choose from full tablecloths, fitted styles, or stylish table runners to match your event.</li>
</ul>

<h2>Types of Table Covers</h2>
<ul>
  <li><strong>Full Tablecloths:</strong> Complete coverage for a polished, branded presentation.</li>
  <li><strong>Fitted Table Covers:</strong> Stretch-fit designs for a sleek and modern appearance.</li>
  <li><strong>Table Runners:</strong> Highlight your branding while keeping part of the table visible for displays or materials.</li>
  <li><strong>Fabric & Vinyl Options:</strong> Choose the best material for indoor or outdoor events.</li>
</ul>

<h2>Applications & Use Cases</h2>
<p>
Branded Tablecloths & Table Runners are perfect for:
</p>
<ul>
  <li>Trade shows, expos, and product launches</li>
  <li>Corporate meetings, seminars, and workshops</li>
  <li>Retail events, pop-up stores, and marketing activations</li>
  <li>Conferences, networking events, and receptions</li>
</ul>

<h2>Design Excellence</h2>
<p>
Gregbuk’s design team works closely with you to ensure that every table cover represents your brand in the best light. From logo placement to color harmony and high-resolution printing, we guarantee that your branded table displays will captivate your audience and elevate your event’s visual appeal.
</p>

<h2>Order Your Branded Table Covers Today</h2>
<p>
Stand out at every event with <strong>custom Branded Tablecloths & Table Runners</strong> from Gregbuk. Professional, durable, and stylish, these table covers turn every setup into a branding opportunity.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Contact Us About Table Covers</strong>
</a>
                         """, "alt_texts": "Table Runners \u2014 professional mockup for product listing.", "category_name": "T-run", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Retractable Banner",
                    "description": "Portable retractable banners for professional marketing on the go.",
                    "image_url": "retractable.jpeg",
                    "alt_texts": "Rectangle Banner service image",
                    "content": """
                    <h2>Retractable Banners</h2>
  <p>
    Showcase your brand anywhere with our portable, easy-to-use retractable banners.  
    Perfect for trade shows, conferences, exhibitions, and retail spaces,  
    these banners are lightweight, professional, and designed for maximum impact.
  </p>

  <h3>Our Retractable Banner Options</h3>
  <ul>
    <li><strong>Standard Retractable Banner:</strong> Compact and effective for everyday promotional use.</li>
    <li><strong>Premium Retractable Banner:</strong> High-quality printing with superior durability and finish.</li>
    <li><strong>Deluxe Retractable Banner:</strong> Extra-large format for maximum visibility at big events.</li>
    <li><strong>Professional Retractable Banner:</strong> Ideal for corporate branding and high-profile displays.</li>
    <li><strong>Black Retractable Banner:</strong> Sleek, stylish design for elegant presentations and events.</li>
    <li><strong>Double-Sided Retractable Banner:</strong> Displays your message on both sides for enhanced exposure.</li>
  </ul>

  <h3>Why Choose Our Retractable Banners?</h3>
  <ul>
    <li>Quick and easy setup with a roll-up mechanism</li>
    <li>Lightweight, portable, and travel-friendly</li>
    <li>High-resolution print for sharp and vibrant visuals</li>
    <li>Durable stands for repeated professional use</li>
  </ul>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Retractable Banner Quote
  </a>
                    """,
                    "category_name": "retract-banner",
                    "products": [
                        {"name": "Retractable Banner",
                         "description": "Standard retractable banner for events and exhibitions.",
                         "image_url": "retract.jpeg", "content": """
                         <h1>Retractable Banners – Portable Marketing Made Simple</h1>

<h2>Showcase Your Brand Anywhere</h2>
<p>
Make your brand impossible to miss with <strong>custom Retractable Banners</strong> from Gregbuk. Perfect for trade shows, conferences, exhibitions, retail spaces, or promotional events, these banners combine portability, durability, and high-quality printing to deliver a professional marketing solution wherever you go.
</p>

<h2>Why Choose Retractable Banners?</h2>
<ul>
  <li><strong>Quick & Easy Setup:</strong> Roll-up mechanism allows effortless installation in seconds.</li>
  <li><strong>Portable Design:</strong> Lightweight and compact for easy transportation and storage.</li>
  <li><strong>High-Quality Printing:</strong> Crisp, vibrant graphics ensure maximum visual impact.</li>
  <li><strong>Durable Stand:</strong> Sturdy base designed for repeated use at events and exhibitions.</li>
  <li><strong>Double-Sided Options:</strong> Increase exposure with banners visible from both sides.</li>
</ul>

<h2>Our Retractable Banner Options</h2>
<ul>
  <li><strong>Standard Retractable Banner:</strong> Ideal for everyday promotional use with compact design.</li>
  <li><strong>Premium Retractable Banner:</strong> High-resolution printing with superior finish for professional appeal.</li>
  <li><strong>Deluxe Retractable Banner:</strong> Extra-large size for maximum visibility at larger events.</li>
  <li><strong>Professional Retractable Banner:</strong> Designed for corporate branding and high-profile displays.</li>
  <li><strong>Black Retractable Banner:</strong> Sleek and elegant for sophisticated events.</li>
  <li><strong>Double-Sided Retractable Banner:</strong> Display your message on both sides to capture more attention.</li>
</ul>

<h2>Applications & Use Cases</h2>
<p>
Retractable Banners are perfect for a wide range of marketing scenarios, including:
</p>
<ul>
  <li>Trade shows, expos, and conventions</li>
  <li>Corporate presentations and workshops</li>
  <li>Retail promotions and in-store marketing</li>
  <li>Conferences, seminars, and networking events</li>
  <li>Product launches and special promotions</li>
</ul>

<h2>Customization & Design</h2>
<p>
Gregbuk allows you to fully customize your retractable banner with your logo, graphics, and brand colors. Choose the perfect size, style, and finish to match your event requirements. Our team ensures your banner is visually striking and professionally printed to make a lasting impression on your audience.
</p>

<h2>Order Your Retractable Banner Today</h2>
<p>
Stand out at every event with <strong>custom Retractable Banners</strong> from Gregbuk – portable, professional, and eye-catching.
</p>

<a href="/contact?head=signs-banner" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
<strong>Request Your Retractable Banner Quote</strong>
</a>
                         """, "alt_texts": "Retractable Banner \u2014 professional mockup for product listing.", "category_name": "retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Premium Retractable Banner",
                         "description": "High-quality retractable banner with premium print and finish.",
                         "image_url": "premium-retract.jpeg", "content": """
                         <h2>Premium Retractable Banner</h2>
  <p>
    Make a bold statement at your events with our <strong>Premium Retractable Banner</strong>. 
    Designed for maximum impact, it features high-quality printing, vivid colors, and sharp graphics 
    that ensure your brand stands out in any setting. Ideal for trade shows, conferences, 
    exhibitions, and product launches, this banner combines style, durability, and portability.
  </p>

  <h3>Why Choose the Premium Retractable Banner?</h3>
  <ul>
    <li><strong>Vivid, High-Resolution Print:</strong> Your branding is displayed with clarity and impact.</li>
    <li><strong>Durable Materials:</strong> Built for repeated use at multiple events without wear.</li>
    <li><strong>Portable & Lightweight:</strong> Easy to carry and set up for any occasion.</li>
    <li><strong>Professional Appearance:</strong> Sleek and polished to enhance your brand image.</li>
    <li><strong>Customizable:</strong> Available in various sizes and finishes to suit your specific needs.</li>
  </ul>

  <p>
    Upgrade your marketing displays with the <strong>Premium Retractable Banner</strong> and leave a 
    lasting impression on every audience.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
</section>
                         """, "alt_texts": "Premium Retractable Banner \u2014 professional mockup for product listing.", "category_name": "premium-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Deluxe Retractable Banner",
                         "description": "Extra-large deluxe banners for maximum visibility.", "image_url": "DeluxeRetractable.jpeg",
                         "category_name": "deluxe-retract", "content": """
                         <h2>Deluxe Retractable Banner</h2>
  <p>
    Elevate your brand visibility with our <strong>Deluxe Retractable Banner</strong>, 
    designed for maximum impact at large-scale events. This extra-large banner ensures your 
    message is seen from afar, combining high-quality printing with professional-grade materials. 
    Perfect for exhibitions, trade shows, grand openings, and outdoor promotions.
  </p>

  <h3>Features of the Deluxe Retractable Banner</h3>
  <ul>
    <li><strong>Extra-Large Format:</strong> Makes your brand stand out in crowded event spaces.</li>
    <li><strong>Vibrant High-Resolution Print:</strong> Sharp, bold colors that grab attention.</li>
    <li><strong>Durable Construction:</strong> Designed for repeated use and long-lasting performance.</li>
    <li><strong>Portable & Easy Setup:</strong> Quick to assemble and disassemble for any event.</li>
    <li><strong>Professional Design:</strong> Sleek finish to reinforce a premium brand image.</li>
  </ul>

  <p>
    Make a grand statement with the <strong>Deluxe Retractable Banner</strong> and ensure your 
    brand captures attention everywhere it goes.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Deluxe Retractable Banner \u2014 close-up showing print detail and finish.", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Professional Retractable Banner",
                         "description": "Designed for corporate use and high-visibility promotions.",
                         "image_url": "professional-retract.jpeg", "content": """
                         <h2>Professional Retractable Banner</h2>
  <p>
    Present your brand with confidence using our <strong>Professional Retractable Banner</strong>, 
    crafted for corporate events, high-profile promotions, and business exhibitions. This banner 
    combines a polished design with superior materials to create a professional and lasting impression.
  </p>

  <h3>Key Features</h3>
  <ul>
    <li><strong>Corporate-Grade Quality:</strong> Built with premium materials to maintain a sleek, professional appearance.</li>
    <li><strong>High-Resolution Printing:</strong> Displays logos, graphics, and messaging with crisp, vibrant clarity.</li>
    <li><strong>Sturdy & Durable:</strong> Engineered to withstand frequent transport and setup at events.</li>
    <li><strong>Easy Assembly:</strong> Quick to set up and retract, perfect for exhibitions and corporate spaces.</li>
    <li><strong>Elegant Design:</strong> Clean lines and refined finish that enhances your brand image.</li>
  </ul>

  <p>
    Ideal for boardrooms, trade shows, product launches, or any setting that demands a professional presentation, 
    the <strong>Professional Retractable Banner</strong> ensures your messaging is both clear and memorable.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Professional Retractable Banner \u2014 stack of multiple items showing variety.", "category_name": "pro-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Black Retractable Banner",
                         "description": "Sleek black retractable banner for elegant event displays.",
                         "image_url": "RetractableBanner.jpeg", "content": """
                         <h2>Black Retractable Banner</h2>
  <p>
    Make a bold statement with our <strong>Black Retractable Banner</strong>, designed for elegance and high-impact visibility. 
    Its sleek black finish provides a sophisticated backdrop that highlights your logo, graphics, and promotional messaging.
  </p>

  <h3>Features & Benefits</h3>
  <ul>
    <li><strong>Sophisticated Design:</strong> Elegant black finish enhances the visual impact of your brand messaging.</li>
    <li><strong>Premium Print Quality:</strong> Crisp, vibrant graphics that stand out against the dark background.</li>
    <li><strong>Durable Construction:</strong> Built to last for repeated use at events, exhibitions, and promotions.</li>
    <li><strong>Portable & Lightweight:</strong> Easy to carry and set up anywhere for instant professional displays.</li>
    <li><strong>Versatile Use:</strong> Perfect for corporate events, product launches, conferences, and trade shows.</li>
  </ul>

  <p>
    With the <strong>Black Retractable Banner</strong>, your brand commands attention while maintaining a sleek, professional appearance. 
    Ideal for businesses and organizations that want their message to stand out with style.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Black Retractable Banner \u2014 product shot on white background.", "category_name": "black-retract", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Double Sided Retractable Banner",
                         "description": "Displays your message on both sides for maximum exposure.",
                         "image_url": "DoubleSidedRetractableBannerStandcopy.webp", "content": """
                         <h2>Double Sided Retractable Banner</h2>
  <p>
    Maximize your brand exposure with our <strong>Double Sided Retractable Banner</strong>, designed to display your message on both sides. 
    Perfect for high-traffic areas, trade shows, or events where visibility from multiple directions is essential.
  </p>

  <h3>Features & Benefits</h3>
  <ul>
    <li><strong>Dual-Sided Display:</strong> Showcase your graphics, promotions, or branding on both sides for maximum visibility.</li>
    <li><strong>Professional Print Quality:</strong> High-resolution, vibrant prints that maintain clarity and color accuracy.</li>
    <li><strong>Durable & Sturdy:</strong> Built with strong retractable mechanisms and reinforced bases for repeated use.</li>
    <li><strong>Portable & Easy Setup:</strong> Lightweight and compact for hassle-free transport and installation.</li>
    <li><strong>Versatile Applications:</strong> Ideal for events, exhibitions, conferences, and retail promotions.</li>
  </ul>

  <p>
    Elevate your marketing efforts with the <strong>Double Sided Retractable Banner</strong>, ensuring your message reaches more people while maintaining a sleek and professional presentation.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Double Sided Retractable Banner \u2014 styled mockup with props for context.", "category_name": "dbs-retract", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Advertising Flags",
                    "description": "Promotional flags to capture attention outdoors and boost brand visibility.",
                    "image_url": "mainadvert-flag.jpeg",
                    "alt_texts": "Advertising Flags service image",
                    "content": """
                    <h2>Advertising Flags</h2>
  <p>
    Boost your brand’s visibility with our high-impact advertising flags.  
    Designed for outdoor promotions, events, and storefront displays,  
    these flags are durable, eye-catching, and perfect for grabbing attention from afar.
  </p>

  <h3>Our Advertising Flag Options</h3>
  <ul>
    <li><strong>Feather Flags:</strong> Tall and aerodynamic, perfect for outdoor brand exposure.</li>
    <li><strong>Teardrop Flags:</strong> Unique teardrop shape that draws attention at events and promotions.</li>
    <li><strong>Blade Flags:</strong> Sleek blade-style design with bold graphics for maximum visibility.</li>
    <li><strong>Custom Flags:</strong> Fully personalized to match your brand identity and messaging.</li>
  </ul>

  <h3>Why Choose Our Flags?</h3>
  <ul>
    <li>Lightweight and easy to assemble</li>
    <li>Durable materials suitable for outdoor use</li>
    <li>Vivid printing for sharp, long-lasting colors</li>
    <li>Perfect for events, storefronts, and roadside marketing</li>
  </ul>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request an Advertising Flag Quote
  </a>
                    """,
                    "category_name": "ad-flag",
                    "products": [
                        {"name": "Feather Flags",
                         "description": "Tall, aerodynamic flags ideal for outdoor advertising.",
                         "image_url": "FeatherFlag.jpeg", "content": """
                         <h2>Feather Flags</h2>
  <p>
    Capture attention from afar with our <strong>Feather Flags</strong>, perfect for outdoor promotions, events, and storefront displays. 
    Their tall, aerodynamic design ensures your brand is seen even from a distance.
  </p>

  <h3>Features & Benefits</h3>
  <ul>
    <li><strong>Eye-Catching Design:</strong> The curved feather shape draws attention and highlights your branding.</li>
    <li><strong>Durable Materials:</strong> Made with weather-resistant fabrics and reinforced stitching to withstand wind and rain.</li>
    <li><strong>Vibrant Prints:</strong> High-resolution graphics ensure your logo, message, or promotion pops.</li>
    <li><strong>Easy Assembly:</strong> Quick to set up with lightweight poles and stable bases for outdoor use.</li>
    <li><strong>Versatile Applications:</strong> Ideal for trade shows, retail events, grand openings, or roadside marketing.</li>
  </ul>

  <p>
    Make your brand stand out with our <strong>Feather Flags</strong>—a professional, portable, and visually striking solution for any outdoor marketing need.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Feather Flags \u2014 professional mockup for product listing.", "category_name": "f-flags", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Teardrop Flags",
                         "description": "Eye-catching teardrop-shaped flags for promotions and events.",
                         "image_url": "TeardropFlags.jpeg", "content": """
                         <h2>Teardrop Flags</h2>
  <p>
    Make a bold statement with our <strong>Teardrop Flags</strong>, designed to capture attention at events, promotions, and outdoor marketing campaigns. 
    Their distinctive teardrop shape ensures your message stands out in any crowd.
  </p>

  <h3>Features & Benefits</h3>
  <ul>
    <li><strong>Distinctive Shape:</strong> The teardrop design creates a dynamic visual impact, perfect for grabbing attention.</li>
    <li><strong>Weather-Resistant Materials:</strong> Crafted from durable, high-quality fabrics that withstand sun, wind, and rain.</li>
    <li><strong>High-Resolution Graphics:</strong> Ensure your logo, message, or promotion is displayed clearly and vibrantly.</li>
    <li><strong>Portable & Easy Setup:</strong> Lightweight poles and sturdy bases allow fast assembly and relocation.</li>
    <li><strong>Versatile Applications:</strong> Ideal for grand openings, trade shows, sports events, or outdoor retail displays.</li>
  </ul>

  <p>
    Elevate your brand visibility with our <strong>Teardrop Flags</strong>—a stylish, professional, and impactful outdoor marketing tool.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Teardrop Flags \u2014 close-up showing print detail and finish.", "category_name": "t-flag", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Blade Flags",
                         "description": "Blade-style flags with bold graphics for maximum visibility.",
                         "image_url": "blade-flag.jpeg", "content": """
                         <h2>Blade Flags</h2>
  <p>
    Capture attention instantly with our <strong>Blade Flags</strong>, designed for maximum visibility and professional outdoor branding. 
    Their tall, sleek, and bold design ensures your brand stands out in any environment.
  </p>

  <h3>Features & Benefits</h3>
  <ul>
    <li><strong>Bold & Sleek Design:</strong> The blade shape offers a modern and professional look that enhances brand visibility.</li>
    <li><strong>Durable Materials:</strong> Made from high-quality, weather-resistant fabric to endure wind, rain, and sun exposure.</li>
    <li><strong>Vivid Printing:</strong> High-resolution graphics ensure your logo or promotional message is clear and vibrant.</li>
    <li><strong>Easy Setup:</strong> Lightweight poles and stable bases make installation quick and convenient.</li>
    <li><strong>Versatile Use:</strong> Perfect for outdoor events, storefronts, trade shows, sports events, and promotional campaigns.</li>
  </ul>

  <p>
    With our <strong>Blade Flags</strong>, your brand achieves striking visibility and leaves a lasting impression on your audience.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Quote
  </a>
                         """, "alt_texts": "Blade Flags \u2014 angled view showing texture and edges.", "category_name": "b-flag", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Custom Flags",
                         "description": "Fully customizable flags tailored to your branding requirements.",
                         "image_url": "custumflag.jpeg", "content": """
                         <h2>Custom Flags</h2>
  <p>
    Showcase your brand your way with <strong>Custom Flags</strong> from Gregbuk. Fully personalized to match your logo, colors, and messaging, these flags are perfect for any promotional or outdoor event.
  </p>

  <h3>Features & Advantages</h3>
  <ul>
    <li><strong>Fully Customizable:</strong> Design flags that reflect your brand identity, from colors and shapes to graphics and slogans.</li>
    <li><strong>Durable & Weather-Resistant:</strong> Crafted from premium fabrics and materials that withstand sun, rain, and wind exposure.</li>
    <li><strong>Vivid Printing:</strong> High-resolution prints ensure your message is clear, vibrant, and professional.</li>
    <li><strong>Easy Installation:</strong> Lightweight poles and sturdy bases allow quick setup for any event.</li>
    <li><strong>Versatile Use:</strong> Perfect for store openings, outdoor promotions, trade shows, sports events, and community outreach.</li>
  </ul>

  <p>
    With <strong>Custom Flags</strong>, make every promotional opportunity count and ensure your brand stands out wherever your flag waves.
  </p>

  <a href="/contact?head=signs-banner" class="btn btn-primary">
    Request a Custom Flag Quote
  </a>
                         """, "alt_texts": "Custom Flags \u2014 detail shot highlighting craftsmanship.", "category_name": "c-flag", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        },
        {
            "name": "Seals & Stamps",
            "description": "Professional seals and stamps for authentication, branding, and official documents.",
            "image_url": "seals&stamps.jpeg",
            "icon_name": "#cil-check",
            "alt_texts": "Seals and Stamps service image",
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
  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Get Quote Now<strong></a> 
            """,
            "subservices": [
                {
                    "name": "Seals",
                    "description": "High-quality seals for official documents, company use, and security.",
                    "image_url": "companyseal.jpeg",
                    "alt_texts": "Seals service image",
                    "content": """
                    <h2>Seals</h2>
  <p>
    Ensure authenticity, security, and professionalism with our range of high-quality seals.  
    From corporate use to legal validation and product security, we provide seals designed  
    to meet every requirement while maintaining a premium look and feel.
  </p>

  <h3>Our Seal Options</h3>
  <ul>
    <li><strong>Company Seals:</strong> Official seals for corporate documents and certifications.</li>
    <li><strong>Notary Seals:</strong> Professional seals to validate and authenticate legal documents.</li>
    <li><strong>Embossed Seals:</strong> Elegant raised impressions for a sophisticated and timeless finish.</li>
    <li><strong>Holographic Seals:</strong> Secure holographic designs for brand protection and authenticity.</li>
    <li><strong>Tamper-Evident Seals:</strong> Designed to reveal any unauthorized opening, ensuring security.</li>
  </ul>

  <h3>Why Choose Our Seals?</h3>
  <ul>
    <li>Durable materials with a professional finish</li>
    <li>Options for corporate, legal, and security use</li>
    <li>Customizable to suit your brand or official requirements</li>
    <li>Available in embossed, holographic, and tamper-proof designs</li>
  </ul>

  <a href="/contact?head=seals-stamps" class="btn btn-primary">
    Request a Seal Quote
  </a>
                    """,
                    "category_name": "seals",
                    "products": [
                        {"name": "Company Seals",
                         "description": "Official seals for corporate documents and certifications.",
                         "image_url": "Company-seal1-1.png", "content": """
                         <h2>Company Seals – Elevate Your Corporate Documents</h2>
  <p>
    In the corporate world, <strong>first impressions matter</strong>. Our <strong>Company Seals</strong> are meticulously designed to enhance the authenticity, credibility, and professionalism of your official documents. From contracts and certificates to official correspondence, these seals convey authority and trust while reinforcing your brand identity.
  </p>

  <h3>Why Choose Our Company Seals?</h3>
  <p>
    Every business needs a mark of authenticity that speaks volumes. Our seals are not just tools—they are an extension of your brand, crafted to demonstrate attention to detail and commitment to excellence. Using high-quality materials and precision engraving techniques, each seal leaves a crisp, detailed impression every time.
  </p>

  <ul>
    <li><strong>Premium Materials:</strong> Constructed from durable metals and high-quality plastics for long-lasting reliability.</li>
    <li><strong>Precision Engraving:</strong> Intricate designs ensure clear, professional impressions on any official document.</li>
    <li><strong>Custom Branding:</strong> Add your company logo, name, and tagline to create a distinctive corporate signature.</li>
    <li><strong>Security & Authenticity:</strong> Deter fraud and unauthorized duplication with unique, precision-crafted designs.</li>
    <li><strong>Versatile Usage:</strong> Perfect for contracts, certificates, invoices, packaging, and all corporate documentation.</li>
  </ul>

  <h3>Enhancing Brand Identity Through Professional Seals</h3>
  <p>
    A <strong>Company Seal</strong> communicates more than authenticity; it communicates trust. By using a professionally crafted seal, your documents reflect meticulous attention to detail and a commitment to quality. Whether you’re a startup, a growing enterprise, or a large corporation, our seals are tailored to elevate the perception of your brand.
  </p>

  <h3>Easy Customization & Ordering</h3>
  <p>
    Creating your custom company seal is simple with Gregbuk. Choose your preferred style, material, and size, then upload your company logo or use one of our professionally designed templates. Our platform provides instant previews and pricing, ensuring you know exactly what to expect before placing your order. Receive your custom seal promptly with fast, reliable shipping.
  </p>

  <p>
    Invest in a mark of professionalism. Our <strong>Company Seals</strong> ensure every document you present makes a lasting impression, reinforcing credibility and corporate integrity.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Request a Company Seal Quote
  </a>
                         """, "alt_texts": "Company Seals \u2014 close-up showing print detail and finish.", "category_name": "company-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Notary Seals",
                         "description": "Professional notary seals to validate legal documents.",
                         "image_url": "Notary-Seal.jpeg", "content": """
                         <h2>Notary Seals – Trusted Validation for Legal Documents</h2>
  <p>
    Ensure the authenticity and legality of your important documents with our <strong>Notary Seals</strong>. Designed for legal professionals, government offices, and corporate entities, these seals provide a clear, professional impression that demonstrates trust and authority in every document they validate.
  </p>

  <h3>Why Choose Gregbuk Notary Seals?</h3>
  <p>
    Our notary seals combine precision, durability, and professional design to meet the high standards required for legal validation. Each seal is carefully crafted to provide crisp, legible impressions that stand up to scrutiny, ensuring your documents are officially recognized and legally binding.
  </p>

  <ul>
    <li><strong>Precision Engraving:</strong> Every detail, including text, logos, and borders, is engraved with accuracy for flawless impressions.</li>
    <li><strong>Durable Materials:</strong> High-quality metals and plastics ensure the seal withstands repeated use without wear.</li>
    <li><strong>Professional Design:</strong> Clean, elegant designs suitable for notarizations, contracts, deeds, and affidavits.</li>
    <li><strong>Legal Compliance:</strong> Crafted to meet standard notary requirements, giving your documents credibility and authority.</li>
    <li><strong>Customizable Options:</strong> Add your name, title, and jurisdiction for a seal that uniquely identifies your office.</li>
  </ul>

  <h3>Applications of Notary Seals</h3>
  <p>
    Notary seals are essential for validating a wide range of documents. They communicate professionalism and trust, protecting both you and your clients. Typical applications include:
  </p>
  <ul>
    <li>Official legal documents such as affidavits, powers of attorney, and contracts</li>
    <li>Corporate agreements and certification forms</li>
    <li>Government filings and regulatory submissions</li>
    <li>Certificates, notarized statements, and authorized letters</li>
  </ul>

  <h3>Seamless Customization & Ordering</h3>
  <p>
    Creating your custom <strong>Notary Seal</strong> is fast and easy with Gregbuk. Choose your preferred seal type, material, and size, then upload your artwork or select from professionally designed templates. Instantly preview your seal and receive transparent pricing before ordering. Fast, reliable shipping ensures your seal arrives ready for immediate use.
  </p>

  <p>
    Enhance your credibility and authority with a notary seal that is as professional as your work. With Gregbuk, your documents are validated with clarity, precision, and trustworthiness.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Request a Notary Seal Quote
  </a>
                         """, "alt_texts": "Notary Seals \u2014 in-use photo demonstrating scale.", "category_name": "notary-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Embossed Seals", "description": "Elegant embossed seals for a sophisticated finish.",
                         "image_url": "embossed-seal.jpeg", "content": """
                         <section>
  <h2>Embossed Seals – Elegant Impressions for a Sophisticated Finish</h2>
  <p>
    Elevate your documents, certificates, and official correspondence with <strong>custom embossed seals</strong> from Gregbuk. These seals create a raised, tactile impression that adds a touch of elegance and authority, making your materials instantly recognizable and professional.
  </p>

  <h3>Why Choose Embossed Seals?</h3>
  <p>
    Embossed seals are more than just functional—they convey prestige, attention to detail, and authenticity. Each seal is carefully engineered to produce sharp, consistent impressions that reflect the quality and professionalism of your organization.
  </p>

  <ul>
    <li><strong>Premium Raised Impressions:</strong> Crisp, detailed embossing for certificates, awards, and official documents.</li>
    <li><strong>Durable Construction:</strong> Made with high-quality metals and plastics for repeated, long-lasting use.</li>
    <li><strong>Professional Aesthetic:</strong> Sleek, elegant design that communicates authority and sophistication.</li>
    <li><strong>Customizable Options:</strong> Add logos, text, and intricate patterns for a unique seal that matches your brand.</li>
    <li><strong>Versatile Applications:</strong> Perfect for legal documents, corporate certifications, event awards, and branding.</li>
  </ul>

  <h3>Applications of Embossed Seals</h3>
  <p>
    Embossed seals are ideal for occasions where professionalism and impression matter. Common uses include:
  </p>
  <ul>
    <li>Corporate certifications and official company documents</li>
    <li>Legal certificates and notarized documents</li>
    <li>Awards, diplomas, and recognition certificates</li>
    <li>Custom branding for envelopes, packaging, and stationery</li>
  </ul>

  <h3>Easy Customization & Online Ordering</h3>
  <p>
    Gregbuk makes it simple to create your own embossed seal. Select the seal type, size, and material, upload your artwork or choose from professional templates, and instantly preview your design. Transparent pricing and fast shipping ensure you receive a premium product ready for immediate use.
  </p>

  <p>
    Impress your clients, partners, and stakeholders with a <strong>custom embossed seal</strong> that embodies professionalism, authority, and attention to detail.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Request an Embossed Seal Quote
  </a>
                         """, "alt_texts": "Embossed Seals \u2014 professional mockup for product listing.", "category_name": "embossed-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Holographic Seals",
                         "description": "Secure holographic seals for brand protection and authenticity.",
                         "image_url": "holographic_seal.jpeg", "content": """
                          <h2>Holographic Seals – Secure & Eye-Catching Authentication</h2>
  <p>
    Protect your documents and products with <strong>custom holographic seals</strong> from Gregbuk. Designed to prevent tampering and ensure authenticity, these seals combine advanced security features with visually striking holographic effects that make your branding stand out.
  </p>

  <h3>Why Choose Holographic Seals?</h3>
  <p>
    Holographic seals are an excellent choice for organizations that value both security and presentation. Each seal features a unique holographic design that is difficult to replicate, providing confidence in authenticity while enhancing your professional image.
  </p>

  <ul>
    <li><strong>Tamper-Proof Security:</strong> Built-in holographic patterns reveal any unauthorized attempts to remove or alter the seal.</li>
    <li><strong>Brand Recognition:</strong> Custom holographic designs showcase logos and brand elements in a visually striking way.</li>
    <li><strong>Durable Materials:</strong> Long-lasting adhesive and premium holographic foil ensure your seal remains intact and vibrant.</li>
    <li><strong>Custom Sizes & Shapes:</strong> Create seals that perfectly fit your packaging, certificates, or promotional items.</li>
    <li><strong>Professional & Modern:</strong> Adds a cutting-edge, professional look to all your documents and products.</li>
  </ul>

  <h3>Applications of Holographic Seals</h3>
  <p>
    Holographic seals are versatile and can be used wherever authentication and visual appeal are essential:
  </p>
  <ul>
    <li>Official corporate documents and certifications</li>
    <li>Product packaging for brand protection and anti-counterfeit measures</li>
    <li>Legal and notary documents requiring authenticity verification</li>
    <li>Promotional materials and branded merchandise for premium presentation</li>
  </ul>

  <h3>Seamless Online Customization & Ordering</h3>
  <p>
    At Gregbuk, designing your <strong>holographic seals</strong> is simple. Choose your seal type, shape, and size, then upload your artwork or select from professional templates. Preview your design instantly, get transparent pricing, and receive fast, reliable delivery.
  </p>

  <p>
    Ensure security, authenticity, and a professional finish with <strong>custom holographic seals</strong> from Gregbuk, making every document or product truly standout.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Request a Holographic Seal Quote
  </a>
                         """, "alt_texts": "Holographic Seals \u2014 product shot on white background.", "category_name": "holo-seal", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Tamper-Evident Seals",
                         "description": "Seals designed to show any unauthorized opening.", "image_url": "tamper-evident.jpeg",
                         "category_name": "te-seal", "content": """
                         <h2>Tamper-Evident Seals – Maximum Security & Peace of Mind</h2>
  <p>
    Protect your products, documents, and shipments with <strong>tamper-evident seals</strong> from Gregbuk. These seals are specifically designed to reveal any unauthorized access, ensuring your items remain secure and your brand retains its credibility. Ideal for businesses, legal applications, and sensitive documentation, our tamper-evident solutions provide unmatched peace of mind.
  </p>

  <h3>Why Choose Tamper-Evident Seals?</h3>
  <p>
    Tamper-evident seals offer both protection and accountability. Once applied, any attempt to remove or tamper with the seal will leave clear evidence, safeguarding the integrity of your products or documents. These seals are essential for organizations that prioritize security and professionalism.
  </p>

  <ul>
    <li><strong>Visible Tamper Detection:</strong> Seals break, tear, or display a void pattern upon unauthorized removal, instantly alerting you to tampering.</li>
    <li><strong>Custom Branding:</strong> Personalize with your logo, company name, or unique designs to maintain a professional image.</li>
    <li><strong>Durable Materials:</strong> Made from high-quality adhesive and materials that withstand handling, shipping, and environmental conditions.</li>
    <li><strong>Versatile Applications:</strong> Perfect for product packaging, official documents, pharmaceuticals, electronics, and secure shipments.</li>
    <li><strong>Regulatory Compliance:</strong> Meets standards for secure labeling and document integrity where applicable.</li>
  </ul>

  <h3>Applications of Tamper-Evident Seals</h3>
  <p>
    Tamper-evident seals are essential for a wide range of uses:
  </p>
  <ul>
    <li>Sealing confidential documents to prevent unauthorized access</li>
    <li>Protecting product packaging from tampering or counterfeiting</li>
    <li>Securing medical, pharmaceutical, or laboratory equipment</li>
    <li>Ensuring the integrity of legal and financial records</li>
    <li>Shipping and logistics applications for maximum accountability</li>
  </ul>

  <h3>Easy Online Customization & Ordering</h3>
  <p>
    At Gregbuk, creating <strong>tamper-evident seals</strong> is simple and efficient. Select your seal type, size, and design, upload your artwork or use one of our professional templates, preview your design instantly, and get transparent pricing before confirming your order. Fast delivery ensures your seals arrive ready for immediate application.
  </p>

  <p>
    Safeguard your products and documents with <strong>tamper-evident seals</strong> from Gregbuk – combining high security, professional appearance, and ease of use in one premium solution.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Request a Tamper-Evident Seal Quote
  </a>
                         """, "alt_texts": "Tamper-Evident Seals \u2014 styled mockup with props for context.", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Stamps",
                    "description": "Custom stamps for office, branding, and creative purposes.",
                    "image_url": "stampps.jpeg",
                    "alt_texts": "Stamps service image",
                    "content": """
                    <h2>Stamps</h2>
  <p>
    Make your mark with our range of high-quality custom stamps.  
    Whether for official documents, branding, or everyday office use,  
    our stamps deliver precision, convenience, and durability.
  </p>

  <h3>Our Stamp Options</h3>
  <ul>
    <li><strong>Signature Stamps:</strong> Save time with convenient stamps for fast and consistent signatures.</li>
    <li><strong>Rubber Stamps:</strong> Traditional and reliable for official marking and branding.</li>
    <li><strong>Self-Inking Stamps:</strong> Mess-free, easy-to-use stamps for repeated impressions.</li>
    <li><strong>Pre-Inked Stamps:</strong> Crisp and consistent results without the need for ink pads.</li>
    <li><strong>Date Stamps:</strong> Perfect for tracking, labeling, and maintaining records.</li>
  </ul>

  <h3>Why Choose Our Stamps?</h3>
  <ul>
    <li>Durable and built for frequent use</li>
    <li>Customizable with text, logos, or designs</li>
    <li>Available in multiple stamp styles and sizes</li>
    <li>Clean impressions with every use</li>
  </ul>

  <a href="/contact?head=seals-stamps" class="btn btn-primary">
    Order Your Custom Stamp
  </a>
                    """,
                    "category_name": "stamps",
                    "products": [
                        {"name": "Signature Stamp",
                         "description": "Convenient stamps for signing documents efficiently.",
                         "image_url": "Signature-Stamp.jpeg", "content": """
                         <h2>Signature Stamps – Effortless Signing & Consistency</h2>
  <p>
    Streamline your workflow with <strong>custom signature stamps</strong> from Gregbuk. Designed for offices, legal firms, and corporate environments, our signature stamps allow you to sign documents quickly, accurately, and consistently. Perfect for repetitive approvals, contracts, and official paperwork, they save time while maintaining professionalism.
  </p>

  <h3>Why Choose Signature Stamps?</h3>
  <ul>
    <li><strong>Time-Saving:</strong> Apply your signature instantly without the need for repetitive manual signing.</li>
    <li><strong>Professional Appearance:</strong> Each stamp produces a clean, legible, and sharp signature for official documents.</li>
    <li><strong>Durable Design:</strong> Built for frequent use, ensuring long-lasting performance in high-volume environments.</li>
    <li><strong>Customizable:</strong> Personalize with your handwritten signature, name, or logo for a unique touch.</li>
    <li><strong>Consistent Results:</strong> Each impression is identical, maintaining accuracy and uniformity across all documents.</li>
  </ul>

  <h3>Applications of Signature Stamps</h3>
  <p>
    Signature stamps are ideal for a wide range of professional scenarios:
  </p>
  <ul>
    <li>Official letters, contracts, and legal documents</li>
    <li>Corporate approvals and internal paperwork</li>
    <li>Accounting, invoices, and financial forms</li>
    <li>Education institutions for certifications and administrative purposes</li>
    <li>Medical offices for prescriptions and patient records</li>
  </ul>

  <h3>Easy Online Customization & Ordering</h3>
  <p>
    Creating your <strong>custom signature stamp</strong> online is simple with Gregbuk. Select the stamp size, style, and type, upload your signature or design, and preview the final product before ordering. Our instant pricing tool ensures transparency, while fast shipping guarantees your stamp arrives ready for immediate use.
  </p>

  <p>
    Enhance your efficiency, maintain consistency, and project professionalism with <strong>Gregbuk Signature Stamps</strong> – the perfect solution for fast and reliable document signing.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Signature Stamp Today
  </a>
                         """, "alt_texts": "Signature Stamp \u2014 stack of multiple items showing variety.", "category_name": "signature-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Rubber Stamp",
                         "description": "Traditional rubber stamps for official marking and branding.",
                         "image_url": "RubberStamps.jpeg", "content": """
                         <h2>Rubber Stamps – Reliable Marking & Branding</h2>
  <p>
    Make every mark count with <strong>custom rubber stamps</strong> from Gregbuk. Perfect for offices, businesses, and creative projects, our rubber stamps provide reliable, precise, and professional impressions. Ideal for official documents, branding, or labeling, they ensure every imprint reflects your professionalism.
  </p>

  <h3>Benefits of Rubber Stamps</h3>
  <ul>
    <li><strong>Precision & Clarity:</strong> Every impression is sharp, consistent, and legible, perfect for important documents.</li>
    <li><strong>Durability:</strong> Made with high-quality rubber and sturdy handles, built to last for thousands of impressions.</li>
    <li><strong>Customizable Designs:</strong> Tailor your stamp with text, logos, or unique graphics to match your brand identity.</li>
    <li><strong>Ease of Use:</strong> Simple to handle and apply, reducing time and effort on repetitive stamping tasks.</li>
    <li><strong>Versatility:</strong> Suitable for paper, envelopes, packaging, certificates, and more.</li>
  </ul>

  <h3>Applications of Rubber Stamps</h3>
  <p>
    Rubber stamps are widely used in professional and creative environments, including:
  </p>
  <ul>
    <li>Official corporate documents and contracts</li>
    <li>Branding on packaging, invoices, and receipts</li>
    <li>Office memos, forms, and approvals</li>
    <li>Certificates, awards, and recognition plaques</li>
    <li>Arts, crafts, and custom stationery projects</li>
  </ul>

  <h3>Easy Online Customization & Ordering</h3>
  <p>
    Ordering your <strong>custom rubber stamp</strong> is effortless with Gregbuk. Choose your preferred size, handle type, and ink color. Upload your design or text, preview your stamp, and get instant pricing. We ensure your stamp is crafted to exact specifications and shipped promptly.
  </p>

  <p>
    Trust Gregbuk to deliver durable, high-quality rubber stamps that leave a lasting impression for your brand or office.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Get Your Custom Rubber Stamp
  </a>
                         """, "alt_texts": "Rubber Stamp \u2014 professional mockup for product listing.", "category_name": "rubber-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Self-Inking Stamp",
                         "description": "Easy-to-use self-inking stamps for repetitive use.", "image_url": "stamp1.jpg",
                         "category_name": "self-ink-stamp", "content": """
                         <section>
  <h2>Self-Inking Stamps – Efficiency Meets Precision</h2>
  <p>
    Simplify repetitive stamping tasks with <strong>self-inking stamps</strong> from Gregbuk. Designed for speed, convenience, and professional results, our self-inking stamps deliver crisp, consistent impressions every time without the need for separate ink pads. Perfect for offices, retail, and administrative workflows.
  </p>

  <h3>Why Choose Self-Inking Stamps?</h3>
  <ul>
    <li><strong>Convenience:</strong> Integrated ink system saves time and reduces mess, making stamping fast and efficient.</li>
    <li><strong>Consistent Impressions:</strong> Each stamp delivers clear, uniform impressions, ideal for repetitive tasks.</li>
    <li><strong>Durable & Long-Lasting:</strong> Built to withstand thousands of impressions with minimal maintenance.</li>
    <li><strong>Customizable:</strong> Personalize with logos, text, or unique designs to reflect your brand or business needs.</li>
    <li><strong>Multiple Ink Colors:</strong> Choose from a variety of ink colors for added versatility and visual impact.</li>
  </ul>

  <h3>Applications of Self-Inking Stamps</h3>
  <p>
    Self-inking stamps are perfect for a wide range of professional and creative uses, including:
  </p>
  <ul>
    <li>Company logos and branding on documents, invoices, and packaging</li>
    <li>Approval, received, or processed stamps for office workflows</li>
    <li>Address stamps for envelopes and correspondence</li>
    <li>Custom designs for events, crafts, and personal projects</li>
    <li>Repetitive marking tasks in schools, businesses, and retail environments</li>
  </ul>

  <h3>Easy Online Ordering & Customization</h3>
  <p>
    With Gregbuk, creating your <strong>custom self-inking stamp</strong> is simple and efficient. Select your preferred stamp size, shape, and ink color, upload your artwork or text, and preview your design. Our platform provides instant pricing, and we deliver your custom stamp quickly with professional craftsmanship guaranteed.
  </p>

  <p>
    Boost productivity and maintain professionalism with Gregbuk’s self-inking stamps – the perfect combination of efficiency, precision, and reliability.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Self-Inking Stamp
  </a>
                         """, "alt_texts": "Self-Inking Stamp \u2014 angled view showing texture and edges.", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Pre-ink Stamp", "description": "Pre-inked stamps for crisp, consistent impressions.",
                         "image_url": "PreInkedStamp.jpeg", "content": """
                         <h2>Pre-Ink Stamps – Crisp Impressions, Every Time</h2>
  <p>
    Achieve perfectly sharp and clear impressions with <strong>pre-ink stamps</strong> from Gregbuk. Unlike traditional stamps, pre-ink stamps are pre-filled with high-quality ink, ensuring consistent results without the need for an external ink pad. Ideal for office, administrative, and creative applications, these stamps provide a professional touch to every document.
  </p>

  <h3>Advantages of Pre-Ink Stamps</h3>
  <ul>
    <li><strong>Precision Printing:</strong> Delivers sharp and detailed impressions for text, logos, and designs.</li>
    <li><strong>Long-Lasting:</strong> Each pre-ink stamp can produce thousands of impressions before needing replacement.</li>
    <li><strong>Mess-Free:</strong> No separate ink pad required, reducing smudges and keeping your workspace clean.</li>
    <li><strong>Customizable:</strong> Personalize with company logos, branding messages, addresses, or creative designs.</li>
    <li><strong>Variety of Ink Colors:</strong> Choose from multiple colors to suit your brand or personal preference.</li>
  </ul>

  <h3>Applications of Pre-Ink Stamps</h3>
  <p>
    Pre-ink stamps are perfect for businesses, offices, and creative projects:
  </p>
  <ul>
    <li>Corporate branding and official document marking</li>
    <li>Address stamps for mailings and envelopes</li>
    <li>Approval, received, or processed stamps for workflow management</li>
    <li>Custom logos or personalized designs for creative or promotional use</li>
    <li>Consistent stamping in schools, workshops, and retail environments</li>
  </ul>

  <h3>Seamless Online Customization & Ordering</h3>
  <p>
    Creating your <strong>custom pre-ink stamp</strong> is easy with Gregbuk. Select your preferred size, ink color, and design, upload your artwork or text, and preview your stamp before ordering. Our system provides instant pricing, ensuring you know the cost upfront. Fast delivery guarantees your stamp arrives ready to use.
  </p>

  <p>
    Enhance professionalism and efficiency with Gregbuk’s pre-ink stamps – the perfect solution for crisp, reliable, and high-quality stamping every time.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Pre-Ink Stamp
  </a>
                         """, "alt_texts": "Pre-Ink Stamp \u2014 stack of multiple items showing variety.", "category_name": "pre-ink-stamp", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Date Stamp",
                         "description": "Date stamps for tracking, labeling, or official documentation.",
                         "image_url": "date-stamp.jpeg", "content": """
                         <h2>Date Stamps – Accurate, Efficient, and Professional</h2>
  <p>
    Keep your documents organized and track important dates with <strong>custom date stamps</strong> from Gregbuk. Designed for offices, administrative workflows, and creative projects, our date stamps provide reliable, precise, and clear impressions every time. Perfect for businesses, schools, and government offices, these stamps help maintain order, accuracy, and professionalism.
  </p>

  <h3>Key Features of Gregbuk Date Stamps</h3>
  <ul>
    <li><strong>Adjustable Date:</strong> Easily set day, month, and year for accurate stamping every time.</li>
    <li><strong>Clear Impressions:</strong> High-quality ink ensures every date is crisp, legible, and professional.</li>
    <li><strong>Durable Construction:</strong> Built to withstand frequent use while maintaining consistent performance.</li>
    <li><strong>Customizable Design:</strong> Add your logo, company name, or special text alongside the date for branding purposes.</li>
    <li><strong>Variety of Ink Colors:</strong> Choose from black, blue, red, or other colors to match your workflow or branding needs.</li>
  </ul>

  <h3>Applications of Date Stamps</h3>
  <p>
    Date stamps are essential tools for businesses and institutions that require accurate documentation:
  </p>
  <ul>
    <li>Document tracking for approvals, receipts, and official records</li>
    <li>Mail and envelope date marking for professional correspondence</li>
    <li>Inventory management and product labeling</li>
    <li>Archiving, filing, and record-keeping in offices and institutions</li>
    <li>Event planning and scheduling for workshops or creative projects</li>
  </ul>

  <h3>Easy Online Customization & Ordering</h3>
  <p>
    Creating your <strong>custom date stamp</strong> online is simple with Gregbuk. Select your preferred size, ink color, and design options, add any branding or text, and preview your stamp before placing an order. Instant pricing and fast shipping ensure you receive a professional-quality stamp ready for immediate use.
  </p>

  <p>
    Streamline your document management and elevate your workflow with Gregbuk’s reliable and customizable date stamps.
  </p>

  <a href="/contact?head=seals-stamps" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Date Stamp
  </a>
                         """, "alt_texts": "Date Stamp \u2014 professional mockup for product listing.", "category_name": "date-stamp", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                }
            ]
        },
        {
            "name": "Frames and Plaques",
            "description": "Decorative and functional frames and plaques for awards, photos, and displays.",
            "image_url": "frame&plaque.jpeg",
            "icon_name": "#cil-image",
            "alt_texts": "Frames and Plaques service image",
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
  <a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary"><strong>Contact Us Now</strong></a> 
            """,
            "subservices": [
                {
                    "name": "Frame",
                    "description": "High-quality frames to protect and showcase your photos and artwork.",
                    "image_url": "frame.jpeg",
                    "alt_texts": "Frame service image",
                    "content": """
                    <h2>Frames</h2>
  <p>
    Protect and showcase your favorite photos, artworks, and certificates  
    with our collection of premium frames. Available in multiple materials  
    and finishes, our frames are designed to enhance presentation while  
    keeping your items safe.
  </p>

  <h3>Our Frame Options</h3>
  <ul>
    <li><strong>Wood Frames:</strong> Classic and elegant, available in different finishes to match any décor.</li>
    <li><strong>Metal Frames:</strong> Sleek, durable, and modern — ideal for a professional or contemporary look.</li>
    <li><strong>Plastic Frames:</strong> Affordable, lightweight, and available in various colors and styles.</li>
    <li><strong>Glass Frames:</strong> Minimalist and stylish, perfect for modern interiors and elegant displays.</li>
  </ul>

  <h3>Why Choose Our Frames?</h3>
  <ul>
    <li>Durable materials with a premium finish</li>
    <li>Custom sizes available to fit any photo or artwork</li>
    <li>Perfect for home, office, or gifting purposes</li>
    <li>Designed to complement and protect your prints</li>
  </ul>

  <a href="/contact?head=frame-plaques" class="btn btn-primary">
    Get a Custom Frame Quote
  </a>
                    """,
                    "category_name": "frame",
                    "products": [
                        {"name": "Wood Frame",
                         "description": "Classic wooden frames available in various finishes for elegant display.",
                         "image_url": "woodframe.jpg", "content": """
                         <h2>Wood Frame – Timeless Elegance for Your Memories</h2>
<p>
    Preserve and showcase your cherished photos, certificates, and artworks with <strong>custom wood frames</strong> from Gregbuk. Expertly crafted from premium timber, each frame combines durability with a timeless aesthetic, adding warmth and sophistication to any display. Perfect for homes, offices, galleries, and gift-giving, our wood frames are designed to highlight your content while providing long-lasting protection.
</p>

<h3>Key Features of Gregbuk Wood Frames</h3>
<ul>
    <li><strong>High-Quality Timber:</strong> Made from durable and sustainably sourced wood for longevity and elegance.</li>
    <li><strong>Variety of Finishes:</strong> Choose from classic, natural, stained, or painted finishes to complement your décor.</li>
    <li><strong>Precision Craftsmanship:</strong> Each frame is carefully constructed with smooth edges, sturdy joints, and a flawless finish.</li>
    <li><strong>Protective Glazing:</strong> Optional glass or acrylic covers to safeguard your photos and artwork from dust, moisture, and fading.</li>
    <li><strong>Customizable Sizes:</strong> Available in multiple sizes and styles to perfectly fit your content, whether small photos or large certificates.</li>
</ul>

<h3>Applications of Wood Frames</h3>
<p>
    Wood frames are versatile and enhance the presentation of various items, making them perfect for:
</p>
<ul>
    <li>Framing personal photographs and cherished memories</li>
    <li>Displaying certificates, diplomas, or awards professionally</li>
    <li>Artworks, sketches, or prints for home and gallery exhibitions</li>
    <li>Corporate and office presentations to add warmth and style</li>
    <li>Unique gifts for weddings, anniversaries, and special occasions</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Designing your <strong>custom wood frame</strong> online is simple with Gregbuk. Select your preferred size, finish, and style, upload your artwork or photo, and preview your frame before ordering. With instant pricing and reliable shipping, your frame will arrive ready to display your memories in style.
</p>

<p>
    Elevate your home, office, or gift-giving experience with Gregbuk’s handcrafted wood frames, where timeless elegance meets modern quality.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Wood Frame
</a>
                         """, "alt_texts": "Wood Frame \u2014 detail shot highlighting craftsmanship.", "category_name": "wood-frames", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Metal Frame", "description": "Modern metal frames offering sleek and durable design.",
                         "image_url": "metal_frame.jpg", "content": """
                         <h2>Metal Frame – Sleek, Modern, and Durable</h2>
<p>
    Showcase your artwork, certificates, or photographs with <strong>custom metal frames</strong> from Gregbuk. Crafted from high-quality metals, these frames provide a sleek and contemporary finish that complements modern interiors and professional spaces. Ideal for homes, offices, galleries, or corporate settings, our metal frames combine strength, style, and precision to protect and elevate your displays.
</p>

<h3>Key Features of Gregbuk Metal Frames</h3>
<ul>
    <li><strong>Premium Metal Construction:</strong> Made from sturdy aluminum or steel for durability and long-lasting performance.</li>
    <li><strong>Modern Aesthetic:</strong> Sleek, minimalist designs that add sophistication to any space or display.</li>
    <li><strong>Variety of Finishes:</strong> Choose from matte, brushed, or polished finishes to suit your style.</li>
    <li><strong>Protective Covering:</strong> Optional glass or acrylic glazing keeps your content safe from dust, scratches, and fading.</li>
    <li><strong>Custom Sizes Available:</strong> Frames can be tailored to fit small photographs, certificates, or large artworks with precision.</li>
</ul>

<h3>Applications of Metal Frames</h3>
<p>
    Metal frames are versatile and perfect for modern and professional presentations, including:
</p>
<ul>
    <li>Displaying contemporary artwork, prints, and photographs</li>
    <li>Framing certificates, awards, or diplomas for corporate or academic recognition</li>
    <li>Enhancing gallery exhibitions with sleek and durable displays</li>
    <li>Professional office decor to showcase achievements or branding</li>
    <li>Stylish gifts for modern homes, events, or corporate clients</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Ordering your <strong>custom metal frame</strong> online is simple with Gregbuk. Select your preferred size, finish, and style, upload your artwork or photo, and preview the design before purchase. With instant pricing and fast delivery, your frame will arrive ready to enhance your space with style and durability.
</p>

<p>
    Combine strength, elegance, and modern design with Gregbuk’s metal frames—perfect for anyone who values a professional and contemporary presentation.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Metal Frame
</a>
                         """, "alt_texts": "Metal Frame \u2014 product shot on white background.", "category_name": "metal-frames", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Plastic Frame",
                         "description": "Affordable plastic frames in multiple colors and styles.",
                         "image_url": "plastic_frame.png", "content": """
                         <h2>Plastic Frame – Versatile, Lightweight, and Stylish</h2>
<p>
    Display your photos, certificates, and artwork with <strong>custom plastic frames</strong> from Gregbuk. Designed for versatility and affordability, our plastic frames are lightweight yet durable, making them perfect for homes, offices, classrooms, and events. With a variety of colors, styles, and finishes, these frames offer a practical solution without compromising on aesthetic appeal.
</p>

<h3>Key Features of Gregbuk Plastic Frames</h3>
<ul>
    <li><strong>Durable and Lightweight:</strong> Made from high-quality, resilient plastic that protects your content while being easy to handle.</li>
    <li><strong>Wide Range of Colors:</strong> Choose from classic neutrals or vibrant shades to complement your décor or personal style.</li>
    <li><strong>Multiple Styles and Finishes:</strong> Smooth, textured, or glossy finishes for a polished and professional look.</li>
    <li><strong>Protective Cover:</strong> Includes clear acrylic or PVC glazing to shield your photos and artwork from dust and scratches.</li>
    <li><strong>Custom Sizes Available:</strong> Frames can be made to fit standard photo sizes or custom dimensions with precision.</li>
</ul>

<h3>Applications of Plastic Frames</h3>
<p>
    Plastic frames are versatile and suitable for a wide range of uses:
</p>
<ul>
    <li>Displaying personal photos and keepsakes in homes and offices</li>
    <li>Framing certificates, awards, and diplomas for schools and institutions</li>
    <li>Decorating events, workshops, or creative exhibitions</li>
    <li>Gift items for birthdays, anniversaries, or corporate giveaways</li>
    <li>Classroom or educational displays with durable and lightweight frames</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Ordering your <strong>custom plastic frame</strong> online is quick and simple with Gregbuk. Choose your preferred size, color, and style, upload your artwork or photo, and preview the design before confirming your order. With instant pricing and reliable delivery, your plastic frame will arrive ready to showcase your memories or achievements beautifully.
</p>

<p>
    Combine practicality, affordability, and style with Gregbuk’s plastic frames—perfect for everyday displays, gifts, or events.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Plastic Frame
</a>
                         """, "alt_texts": "Plastic Frame \u2014 styled mockup with props for context.", "category_name": "plastic-frames", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Glass Frame",
                         "description": "Glass frames with minimalistic design, perfect for modern interiors.",
                         "image_url": "glass-frame.jpg", "content": """
                         <h2>Glass Frame – Elegant, Minimalist, and Premium</h2>
<p>
    Showcase your photos, certificates, and artwork with <strong>custom glass frames</strong> from Gregbuk. Designed for a sleek, modern aesthetic, our glass frames provide crystal-clear visibility and a sophisticated finish. Perfect for contemporary interiors, galleries, offices, and personal displays, these frames combine elegance with durability for a premium presentation.
</p>

<h3>Key Features of Gregbuk Glass Frames</h3>
<ul>
    <li><strong>Premium Glass Material:</strong> High-quality glass provides a clear, sharp view of your artwork or photos while protecting them from dust and scratches.</li>
    <li><strong>Minimalist Design:</strong> Clean edges and transparent glazing create a modern, professional look that complements any décor.</li>
    <li><strong>Durable Construction:</strong> Securely holds your artwork or photos in place with strong backing and sturdy fittings.</li>
    <li><strong>Customizable Options:</strong> Choose from various sizes, edge styles, and finishes to match your personal or corporate aesthetic.</li>
    <li><strong>Easy to Display:</strong> Suitable for wall mounting or tabletop presentation, offering versatile display options.</li>
</ul>

<h3>Applications of Glass Frames</h3>
<p>
    Glass frames are ideal for highlighting important photos, certificates, and creative works:
</p>
<ul>
    <li>Displaying artwork, photography, or professional prints in homes and offices</li>
    <li>Framing diplomas, awards, and certificates for elegant recognition</li>
    <li>Gallery exhibitions, creative showcases, and corporate presentations</li>
    <li>Event décor or commemorative displays with a refined, minimalist look</li>
    <li>Gifting high-quality framed photos or prints with a polished finish</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Creating your <strong>custom glass frame</strong> online is effortless with Gregbuk. Select your preferred size, edge style, and finish, upload your artwork or photo, and preview the final frame before ordering. With transparent pricing and fast delivery, your glass frame will arrive ready to elevate your display with elegance and clarity.
</p>

<p>
    Add a touch of sophistication and modern design to your spaces with Gregbuk’s premium glass frames, perfect for professional, personal, or decorative purposes.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Glass Frame
</a>
                         """, "alt_texts": "Glass Frame \u2014 in-use photo demonstrating scale.", "category_name": "glass-frames", "image_collection": [choice(imgg) for n in range(8)]}
                    ]
                },
                {
                    "name": "Plaques",
                    "description": "Custom plaques for awards, recognition, and corporate displays.",
                    "image_url": "plaques_now.jpeg",
                    "alt_texts": "Plaques service image",
                    "content": """
                    <h2>Plaques</h2>
  <p>
    Celebrate achievements and recognize excellence with our custom-designed plaques.  
    Perfect for awards, recognition, corporate branding, and special events, our plaques  
    are crafted with precision and elegance to leave a lasting impression.
  </p>

  <h3>Our Plaque Options</h3>
  <ul>
    <li><strong>Wood Plaques:</strong> Elegant and timeless, ideal for awards and formal recognitions.</li>
    <li><strong>Metal Plaques:</strong> Durable and professional, perfect for achievements and commemorations.</li>
    <li><strong>Acrylic Plaques:</strong> Modern and sleek, offering a clear and stylish award presentation.</li>
    <li><strong>Glass Plaques:</strong> Premium quality with refined engraving, great for prestigious recognition.</li>
    <li><strong>Crystal Plaques:</strong> Luxury finish for high-profile awards and top-tier events.</li>
  </ul>

  <h3>Why Choose Our Plaques?</h3>
  <ul>
    <li>Crafted with high-quality materials for durability</li>
    <li>Custom engraving and personalization available</li>
    <li>Wide range of styles to suit every occasion</li>
    <li>Perfect for corporate, academic, and personal recognition</li>
  </ul>

  <a href="/contact?head=frame-plaques" class="btn btn-primary">
    Order Your Custom Plaque
  </a>
                    """,
                    "category_name": "plaques",
                    "products": [
                        {"name": "Wood Plaques", "description": "Elegant wooden plaques for awards and recognitions.",
                         "image_url": "woodplaque.jpg", "content": """
                         <h2>Wood Plaques – Timeless, Elegant, and Personalized</h2>
<p>
    Celebrate achievements and recognize excellence with <strong>custom wood plaques</strong> from Gregbuk. Crafted from premium wood and finished to perfection, these plaques provide a classic and timeless way to honor accomplishments. Ideal for corporate awards, academic recognition, and personal milestones, our wood plaques combine durability with elegance for a lasting impression.
</p>

<h3>Key Features of Gregbuk Wood Plaques</h3>
<ul>
    <li><strong>Premium Wood Material:</strong> Made from high-quality, durable wood that ensures long-lasting beauty and strength.</li>
    <li><strong>Elegant Finishes:</strong> Smooth, polished surfaces with options for natural, stained, or custom finishes to suit any décor or style.</li>
    <li><strong>Custom Engraving:</strong> Personalize with names, logos, dates, or messages for a truly unique and meaningful award.</li>
    <li><strong>Versatile Sizes and Shapes:</strong> Choose from a range of standard or custom sizes to fit any award or recognition purpose.</li>
    <li><strong>Professional Presentation:</strong> Perfect for wall mounting or tabletop display, showcasing achievements with dignity and style.</li>
</ul>

<h3>Applications of Wood Plaques</h3>
<p>
    Wood plaques are perfect for presenting awards, recognizing accomplishments, and commemorating special moments:
</p>
<ul>
    <li>Corporate awards for employee achievements or service recognition</li>
    <li>Academic recognition for schools, universities, and professional training programs</li>
    <li>Personal milestones such as anniversaries, family achievements, or special occasions</li>
    <li>Community and association awards to honor outstanding contributions</li>
    <li>Custom gifts that combine elegance with lasting value</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Designing your <strong>custom wood plaque</strong> online is straightforward with Gregbuk. Select your preferred wood type, size, and finish, then personalize it with text, logos, or artwork. Instant pricing and fast delivery ensure your plaque arrives ready to impress and commemorate any achievement.
</p>

<p>
    Honor milestones, celebrate excellence, and create a lasting memory with Gregbuk’s premium wood plaques, designed to make every recognition meaningful and memorable.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Wood Plaque
</a>
                         """, "alt_texts": "Wood Plaques \u2014 stack of multiple items showing variety.", "category_name": "wood-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Metal Plaques",
                         "description": "Durable metal plaques for professional achievements and commemorations.",
                         "image_url": "metal_plaque.jpeg", "content": """
                         <h2>Metal Plaques – Durable, Sleek, and Prestigious</h2>
<p>
    Recognize excellence and commemorate achievements with <strong>custom metal plaques</strong> from Gregbuk. Crafted from high-quality metals and finished with precision, these plaques offer a sleek and modern way to honor accomplishments. Ideal for corporate awards, institutional recognition, or special commemorations, our metal plaques are designed to make a lasting impact while exuding professionalism.
</p>

<h3>Key Features of Gregbuk Metal Plaques</h3>
<ul>
    <li><strong>Premium Metal Construction:</strong> Made from durable metals such as aluminum, brass, or stainless steel to ensure long-lasting quality and resilience.</li>
    <li><strong>Professional Finish:</strong> Polished, brushed, or matte finishes available to complement any environment or style preference.</li>
    <li><strong>Custom Engraving:</strong> Personalize with names, logos, dates, or custom messages for a unique and meaningful recognition.</li>
    <li><strong>Versatile Sizes and Styles:</strong> Select from a range of shapes, sizes, and mounting options to suit your award presentation or display needs.</li>
    <li><strong>Long-Lasting Presentation:</strong> Resistant to wear and corrosion, making them suitable for both indoor and outdoor recognition purposes.</li>
</ul>

<h3>Applications of Metal Plaques</h3>
<p>
    Metal plaques are perfect for honoring achievements and highlighting contributions in a professional and stylish manner:
</p>
<ul>
    <li>Corporate awards for employees, partners, and business milestones</li>
    <li>Academic recognition for students, faculty, and institutional excellence</li>
    <li>Government and association awards for outstanding service or contributions</li>
    <li>Commemorative plaques for events, projects, or historic achievements</li>
    <li>Premium gifts that combine durability with elegance and prestige</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Designing your <strong>custom metal plaque</strong> online is quick and convenient with Gregbuk. Choose your preferred metal, size, and finish, then add personalized engraving for a truly unique and professional award. Instant pricing and fast shipping ensure your plaque arrives ready to impress and recognize achievements with lasting impact.
</p>

<p>
    Celebrate accomplishments and create memorable recognition with Gregbuk’s high-quality metal plaques, designed to showcase success with sophistication and style.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Metal Plaque
</a>

                         """, "alt_texts": "Metal Plaques \u2014 in-use photo demonstrating scale.", "category_name": "metal-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Acrylic Plaques",
                         "description": "Clear acrylic plaques for modern award displays with a sleek finish.",
                         "image_url": "Acrylic_plaques.jpeg", "content": """
                         <h2>Acrylic Plaques – Modern, Clear, and Elegant</h2>
<p>
    Highlight achievements and present awards with <strong>custom acrylic plaques</strong> from Gregbuk. Designed with a clear, sleek, and contemporary style, our acrylic plaques provide a professional and visually striking way to honor accomplishments. Perfect for corporate recognition, awards ceremonies, or personal gifts, these plaques combine durability with elegance to leave a lasting impression.
</p>

<h3>Key Features of Gregbuk Acrylic Plaques</h3>
<ul>
    <li><strong>Crystal-Clear Material:</strong> Made from high-quality acrylic for a transparent, glass-like appearance without the fragility of glass.</li>
    <li><strong>Precision Engraving:</strong> Personalize with text, logos, and designs for a professional and unique presentation.</li>
    <li><strong>Lightweight & Durable:</strong> Sturdy enough to last while being lightweight for easy handling and display.</li>
    <li><strong>Versatile Display Options:</strong> Freestanding or wall-mounted options available to suit any environment.</li>
    <li><strong>Custom Shapes & Sizes:</strong> Choose from various dimensions and shapes to perfectly match your event or recognition needs.</li>
</ul>

<h3>Applications of Acrylic Plaques</h3>
<p>
    Acrylic plaques are ideal for occasions where a modern and professional presentation is desired:
</p>
<ul>
    <li>Corporate awards for employees, achievements, and milestones</li>
    <li>Academic recognition for students, faculty, or outstanding projects</li>
    <li>Event commemorations for conferences, seminars, or special gatherings</li>
    <li>Personalized gifts for anniversaries, retirements, or special achievements</li>
    <li>Institutional displays showcasing awards, honors, or contributions</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Creating your <strong>custom acrylic plaque</strong> online with Gregbuk is simple and convenient. Select the size, shape, and design options, then add personalized engraving or logos. Our instant pricing and fast shipping ensure your acrylic plaque arrives ready to impress and celebrate achievements professionally.
</p>

<p>
    Elevate your recognition and celebrate accomplishments in a modern, stylish, and professional way with Gregbuk’s premium acrylic plaques.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Acrylic Plaque
</a>

                         """, "alt_texts": "Acrylic Plaques \u2014 professional mockup for product listing.", "category_name": "plastic-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Glass Plaques",
                         "description": "High-quality glass plaques with premium engraving for special recognition.",
                         "image_url": "glass.webp", "content": """
                         <h2>Glass Plaques – Premium, Elegant, and Timeless</h2>
<p>
    Recognize excellence and commemorate special achievements with <strong>custom glass plaques</strong> from Gregbuk. Designed for a sophisticated and timeless presentation, our glass plaques provide a polished, high-end look suitable for corporate awards, academic recognition, or prestigious events. Durable yet elegant, each plaque is crafted to create a lasting impression.
</p>

<h3>Key Features of Gregbuk Glass Plaques</h3>
<ul>
    <li><strong>High-Quality Glass:</strong> Made from premium glass for clarity, brilliance, and long-lasting durability.</li>
    <li><strong>Precise Engraving:</strong> Customizable with logos, names, messages, or designs for a professional, personalized finish.</li>
    <li><strong>Elegant Presentation:</strong> Crystal-clear transparency and refined edges make these plaques ideal for display on desks, shelves, or walls.</li>
    <li><strong>Various Sizes & Shapes:</strong> Available in multiple dimensions and designs to match your recognition or event requirements.</li>
    <li><strong>Freestanding or Wall-Mount Options:</strong> Flexible display options ensure your plaque can be showcased wherever desired.</li>
</ul>

<h3>Applications of Glass Plaques</h3>
<p>
    Glass plaques are perfect for occasions that demand elegance and professionalism:
</p>
<ul>
    <li>Corporate awards to honor top-performing employees or teams</li>
    <li>Academic achievements, including student recognition and faculty honors</li>
    <li>Special commemorations for events, anniversaries, or milestones</li>
    <li>Personalized gifts for retirees, leaders, or community contributors</li>
    <li>Display of awards in offices, boardrooms, and reception areas</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Designing your <strong>custom glass plaque</strong> online with Gregbuk is effortless. Select your preferred size, shape, and engraving options, then personalize it with text, logos, or designs. Our instant pricing and reliable shipping ensure your glass plaque arrives ready to impress, celebrate, and honor achievements in style.
</p>

<p>
    Celebrate accomplishments with sophistication and elegance using Gregbuk’s premium glass plaques, perfect for creating memorable and professional recognition pieces.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Glass Plaque
</a>

                         """, "alt_texts": "Glass Plaques \u2014 stack of multiple items showing variety.", "category_name": "glass-plaques", "image_collection": [choice(imgg) for n in range(8)]},
                        {"name": "Crystal Plaques",
                         "description": "Luxury crystal plaques for top-tier awards and prestigious events.",
                         "image_url": "crstal_plaque.jpeg", "content": """
                         <h2>Crystal Plaques – Luxurious, Prestigious, and Memorable</h2>
<p>
    Celebrate exceptional achievements with <strong>custom crystal plaques</strong> from Gregbuk. Designed to impress, these plaques combine elegance, clarity, and durability to create a luxurious recognition piece suitable for corporate awards, high-profile events, or prestigious personal gifts. Each plaque reflects sophistication and professionalism, leaving a lasting impression on recipients and viewers alike.
</p>

<h3>Key Features of Gregbuk Crystal Plaques</h3>
<ul>
    <li><strong>Premium Crystal Material:</strong> Made from high-quality, flawless crystal for maximum brilliance and clarity.</li>
    <li><strong>Custom Engraving:</strong> Personalize with logos, names, dates, and messages for a one-of-a-kind, professional award.</li>
    <li><strong>Elegant Designs:</strong> Sleek, modern shapes with polished edges make every plaque a centerpiece of recognition.</li>
    <li><strong>Various Sizes & Shapes:</strong> Choose the perfect dimensions and styles to match the importance of the occasion.</li>
    <li><strong>Freestanding or Display-Ready:</strong> Designed to be showcased on desks, shelves, or in display cases with elegance.</li>
</ul>

<h3>Applications of Crystal Plaques</h3>
<p>
    Crystal plaques are ideal for occasions where prestige and distinction matter:
</p>
<ul>
    <li>Executive and corporate awards for outstanding performance or leadership</li>
    <li>Special recognition at conferences, galas, and events</li>
    <li>Academic and institutional honors for top achievers</li>
    <li>Commemorative gifts for milestones, retirements, or anniversaries</li>
    <li>Showcasing awards in offices, boardrooms, and prestigious venues</li>
</ul>

<h3>Easy Online Customization & Ordering</h3>
<p>
    Ordering your <strong>custom crystal plaque</strong> online with Gregbuk is simple. Select the size, shape, and engraving options, then personalize it with your text or logo. Instant pricing and prompt shipping ensure your crystal plaque arrives ready to impress, honor, and commemorate in style.
</p>

<p>
    Make every achievement unforgettable with Gregbuk’s luxurious and bespoke crystal plaques, designed to reflect prestige and elegance.
</p>

<a href="/contact?head=frame-plaques" class="btn btn-outline-primary rounded-pill border border-2 border-primary">
    Order Your Crystal Plaque
</a>

                         """, "alt_texts": "Crystal Plaques \u2014 styled mockup with props for context.", "category_name": "crystal-plaques", "image_collection": [choice(imgg) for n in range(8)]}
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
            alt_texts=service_data["alt_texts"],
            content=service_data["content"] if "content" in service_data else None
        )
        for sub_data in service_data.get("subservices", []):
            sub = SubService(
                name=sub_data["name"],
                image_url=sub_data["image_url"],
                category_name=sub_data["category_name"],
                services=service,
                description=sub_data["description"],
                alt_texts=sub_data["alt_texts"],
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
                    alt_texts=prod_data["alt_texts"],
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
                alt_texts=prod_data["alt_texts"],
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

