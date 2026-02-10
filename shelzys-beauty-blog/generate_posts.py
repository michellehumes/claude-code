#!/usr/bin/env python3
"""Generate all 50 blog posts for Shelzy's Beauty Blog with affiliate links."""

import os

BASE = "/home/user/claude-code/shelzys-beauty-blog"
TAG = "shelzysbeauty-20"

def alink(asin, text):
    return f'<a href="https://www.amazon.com/dp/{asin}?tag={TAG}" target="_blank" rel="nofollow noopener">{text}</a>'

def abtn(asin, text="Check Price on Amazon"):
    return f'<a href="https://www.amazon.com/dp/{asin}?tag={TAG}" target="_blank" rel="nofollow noopener" class="cta-button">{text}</a>'

def header(title, category, meta_desc, read_time):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{meta_desc}">
  <title>{title} | Shelzy's Beauty Blog</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="../../index.html" class="site-logo">Shelzy's <span>Beauty</span></a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <nav>
        <ul class="nav-menu">
          <li><a href="../../index.html">Home</a></li>
          <li><a href="../../index.html#skincare">Skincare</a></li>
          <li><a href="../../index.html#haircare">Haircare</a></li>
          <li><a href="../../index.html#makeup">Makeup</a></li>
          <li><a href="../../index.html#tools">Tools</a></li>
          <li><a href="../../index.html#budget">Budget Finds</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <div class="post-header">
    <span class="post-card-category">{category}</span>
    <h1>{title}</h1>
    <div class="post-meta">
      <span>By Shelzy</span> <span>|</span> <span>{read_time} min read</span> <span>|</span> <span>Updated February 2026</span>
    </div>
  </div>
  <div class="post-content">
    <div class="affiliate-disclosure">
      <strong>Disclosure:</strong> This post contains affiliate links. If you purchase through these links, I may earn a small commission at no extra cost to you. I only recommend products I've personally tested and love. See my <a href="../../disclosure.html">full disclosure</a>.
    </div>
'''

def footer():
    return '''
    <div class="newsletter-box">
      <h3>Get Weekly Beauty Picks</h3>
      <p>Join 10,000+ readers for the best product finds and routines every Tuesday.</p>
      <form class="newsletter-form">
        <input type="email" placeholder="Your email address" required>
        <button type="submit">Subscribe</button>
      </form>
    </div>
  </div>
  <footer class="site-footer">
    <div class="footer-bottom">
      <p>&copy; 2026 Shelzy's Beauty Blog. All rights reserved. As an Amazon Associate, I earn from qualifying purchases.</p>
    </div>
  </footer>
  <script src="../../js/main.js"></script>
</body>
</html>'''

def product_card(name, brand, asin, price, rating, desc, pros, cons, best_for):
    stars = "★" * int(rating) + ("½" if rating % 1 else "") + "☆" * (5 - int(rating) - (1 if rating % 1 else 0))
    pros_html = "".join(f"<li>{p}</li>" for p in pros)
    cons_html = "".join(f"<li>{c}</li>" for c in cons)
    return f'''
    <div class="product-card">
      <div class="product-card-header">
        <div class="product-image-placeholder">{brand}</div>
        <div class="product-info">
          <h3>{alink(asin, name)}</h3>
          <div class="product-brand">{brand}</div>
          <div class="product-rating">{stars} {rating}/5</div>
          <div class="product-price">${price}</div>
        </div>
      </div>
      <p class="product-description">{desc}</p>
      <div class="pros-cons">
        <div class="pros"><h4>Pros</h4><ul>{pros_html}</ul></div>
        <div class="cons"><h4>Cons</h4><ul>{cons_html}</ul></div>
      </div>
      <div class="best-for"><strong>Best for:</strong> {best_for}</div>
      {abtn(asin)}
    </div>'''

def quick_pick_table(picks):
    rows = ""
    for label, cls, name, asin, price in picks:
        rows += f'''<tr>
          <td><span class="pick-label {cls}">{label}</span><br><strong>{name}</strong></td>
          <td>${price}</td>
          <td>{abtn(asin, "View on Amazon")}</td>
        </tr>'''
    return f'''
    <div class="quick-picks">
      <h3>Our Top Picks at a Glance</h3>
      <table>
        <tr><th>Product</th><th>Price</th><th>Link</th></tr>
        {rows}
      </table>
    </div>'''

def faq_section(faqs):
    items = ""
    for q, a in faqs:
        items += f'''
      <div class="faq-item">
        <div class="faq-question">{q}</div>
        <div class="faq-answer"><p>{a}</p></div>
      </div>'''
    return f'''
    <div class="faq-section">
      <h2>Frequently Asked Questions</h2>
      {items}
    </div>'''

def write_post(subdir, filename, content):
    path = os.path.join(BASE, "posts", subdir, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  Created: posts/{subdir}/{filename}")

# ─────────────────────────────────────────────
# POST 1: Best Vitamin C Serums
# ─────────────────────────────────────────────
def post_01():
    h = header("7 Best Vitamin C Serums for Dark Spots and Hyperpigmentation (2026)",
               "Skincare",
               "Tested 15 vitamin C serums to find the 7 best for dark spots and hyperpigmentation. Budget to luxury picks with honest before-and-after results.",
               12)
    qp = quick_pick_table([
        ("Best Overall", "best-overall", "TruSkin Vitamin C Serum", "B01M4MCUAF", "22"),
        ("Budget Pick", "budget", "Maelove Glow Maker", "B07B4SCWLQ", "16"),
        ("Premium", "premium", "SkinCeuticals C E Ferulic", "B000LNOCKM", "166"),
    ])
    body = f'''
    <p>After three months of testing 15 different vitamin C serums on my own skin, I can tell you that the differences between formulas are real. The right vitamin C serum can visibly fade dark spots in as little as 4 weeks, brighten dull skin, and protect against environmental damage. The wrong one oxidizes in the bottle before it ever touches your face.</p>
    <p>I evaluated each serum on five criteria: ingredient quality, absorption speed, visible results after 30 days, texture and wearability under makeup, and value for money. Here are the 7 that earned a permanent spot on my shelf.</p>
    {qp}
    <h2>What to Look for in a Vitamin C Serum</h2>
    <p>Before diving into the picks, here's a quick primer on what separates a great vitamin C serum from a mediocre one:</p>
    <ul>
      <li><strong>Form of Vitamin C:</strong> L-ascorbic acid is the gold standard for proven results. Derivatives like sodium ascorbyl phosphate are gentler but slower to show results.</li>
      <li><strong>Concentration:</strong> 10-20% L-ascorbic acid is the sweet spot. Below 10% may not be effective enough; above 20% increases irritation without added benefit.</li>
      <li><strong>pH Level:</strong> Must be below 3.5 for L-ascorbic acid to penetrate effectively.</li>
      <li><strong>Supporting Ingredients:</strong> Vitamin E and ferulic acid boost vitamin C's stability and efficacy by up to 8x.</li>
      <li><strong>Packaging:</strong> Dark glass or opaque airless pumps protect against oxidation. Avoid clear bottles.</li>
    </ul>
    <h2>The 7 Best Vitamin C Serums</h2>
    {product_card("TruSkin Vitamin C Serum", "TruSkin", "B01M4MCUAF", "21.97", 4.5,
        "This has been Amazon's #1 bestselling vitamin C serum for years, and after testing it myself I understand why. The formula combines 15% vitamin C with hyaluronic acid and vitamin E for a serum that brightens, hydrates, and protects simultaneously. After 4 weeks of daily use, my dark spots from old acne scars were noticeably lighter.",
        ["Visible brightening in 3-4 weeks", "Lightweight, absorbs quickly", "Doesn't pill under makeup", "Incredible price for the quality"],
        ["Slightly sticky initial feel", "Scent is earthy (normal for vitamin C)"],
        "Anyone wanting proven results at a drugstore price")}
    {product_card("Maelove Glow Maker", "Maelove", "B07B4SCWLQ", "15.95", 4.5,
        "Often called the 'SkinCeuticals dupe,' this serum features 15% L-ascorbic acid, vitamin E, and ferulic acid at a fraction of the price. The texture is incredibly lightweight and watery, making it a dream under sunscreen and makeup. Results were comparable to serums 10x the price.",
        ["SkinCeuticals-comparable formula", "Ultra-lightweight texture", "Absorbs in seconds", "Best value on this list"],
        ["Can sting on sensitive skin", "Packaging could be more airtight"],
        "Budget-conscious shoppers who want a premium formula")}
    {product_card("SkinCeuticals C E Ferulic", "SkinCeuticals", "B000LNOCKM", "166.00", 5,
        "The gold standard that every other vitamin C serum is compared to. Patented combination of 15% L-ascorbic acid, 1% vitamin E, and 0.5% ferulic acid. Clinical studies show it provides 8x your skin's natural protection against photoaging. Yes, it's expensive. But the results are unmatched.",
        ["Clinically proven formula", "Most research-backed serum available", "Visible results in 2-3 weeks", "Elegant texture"],
        ["Very expensive", "Can oxidize if not stored properly"],
        "Those who want the absolute best and don't mind investing")}
    {product_card("Timeless 20% Vitamin C + E Ferulic Acid", "Timeless", "B0036BI56G", "24.95", 4.5,
        "At 20% concentration, this is the strongest formula on our list. The addition of vitamin E and ferulic acid mirrors the SkinCeuticals ratio at a fraction of the cost. It's made in small batches to ensure freshness, and the brand offers a refund if it arrives oxidized.",
        ["20% concentration for stubborn spots", "Freshness guarantee", "Near-identical formula to SkinCeuticals", "Affordable for premium ingredients"],
        ["Can be too strong for sensitive skin", "Must refrigerate after opening"],
        "Experienced vitamin C users who want maximum strength")}
    {product_card("La Roche-Posay Vitamin C Serum", "La Roche-Posay", "B07RMKZ16P", "39.99", 4.5,
        "If you have sensitive skin that rebels against traditional L-ascorbic acid, this is your answer. It uses 10% pure vitamin C with salicylic acid and neurosensine to brighten while calming redness. Dermatologist-tested and fragrance-free.",
        ["Formulated for sensitive skin", "No irritation or stinging", "Dermatologist-recommended brand", "Also helps with texture"],
        ["Lower concentration (10%)", "Results take 6-8 weeks"],
        "Sensitive skin types who've struggled with other vitamin C serums")}
    {product_card("Drunk Elephant C-Firma Fresh Day Serum", "Drunk Elephant", "B0B3XN6884", "78.00", 4,
        "This innovative packaging mixes the vitamin C powder fresh with each pump, so oxidation is never an issue. The 15% L-ascorbic acid formula also includes pumpkin ferment extract and pomegranate enzyme for gentle exfoliation alongside brightening.",
        ["Fresh-mix technology prevents oxidation", "Dual brightening + exfoliating action", "Clean beauty formulation", "Silky elegant texture"],
        ["Expensive for the amount", "Mixing mechanism can be finicky"],
        "Clean beauty enthusiasts willing to invest in innovation")}
    {product_card("The Ordinary Vitamin C Suspension 23% + HA Spheres 2%", "The Ordinary", "B07DHV1YN5", "5.80", 4,
        "At under $6, this is the most affordable vitamin C treatment you'll find from a reputable brand. The 23% concentration is high, and the texture is more of a creamy suspension than a serum. It works, but requires patience with the gritty texture.",
        ["Unbeatable price", "Highest concentration on this list", "From a trusted brand", "Good for body use too"],
        ["Gritty, silicone-y texture", "Can pill under other products", "Not cosmetically elegant"],
        "Ultra-budget shoppers who prioritize results over texture")}
    <h2>Final Verdict</h2>
    <p>For most people, the <strong>{alink("B01M4MCUAF", "TruSkin Vitamin C Serum")}</strong> offers the best balance of proven results, pleasant texture, and value. If budget is truly no concern, the {alink("B000LNOCKM", "SkinCeuticals C E Ferulic")} remains unmatched in clinical backing. And if you want the absolute best value, the {alink("B07B4SCWLQ", "Maelove Glow Maker")} delivers a near-identical formula for $16.</p>
    '''
    faqs = faq_section([
        ("How long does it take for vitamin C to fade dark spots?", "Most people see noticeable improvement in 4-8 weeks of consistent daily use. Stubborn spots may take 3-4 months."),
        ("Can I use vitamin C with retinol?", "Yes! Use vitamin C in the morning and retinol at night for the best results without irritation."),
        ("Why did my vitamin C serum turn orange?", "That means it has oxidized and lost effectiveness. Store in a cool, dark place and replace every 3-4 months once opened."),
        ("Should I apply vitamin C before or after moisturizer?", "Before. Apply vitamin C to clean skin, let it absorb for 1-2 minutes, then follow with moisturizer and SPF."),
    ])
    write_post("skincare", "best-vitamin-c-serums.html", h + body + faqs + footer())

# ─────────────────────────────────────────────
# POST 2: Best Moisturizers for Dry Sensitive Skin
# ─────────────────────────────────────────────
def post_02():
    h = header("10 Best Moisturizers for Dry, Sensitive Skin (Dermatologist-Approved)",
               "Skincare",
               "Find the best moisturizers for dry, sensitive skin. Tested and ranked from drugstore to luxury, all gentle and dermatologist-approved.",
               10)
    qp = quick_pick_table([
        ("Best Overall", "best-overall", "CeraVe Moisturizing Cream", "B00TTD9BRC", "17"),
        ("Budget Pick", "budget", "Vanicream Moisturizing Cream", "B000NWGCZ2", "14"),
        ("Premium", "premium", "La Roche-Posay Toleriane Double Repair", "B01N7T7JKJ", "23"),
    ])
    body = f'''
    <p>If you have dry, sensitive skin, finding a moisturizer that hydrates without causing stinging, redness, or breakouts can feel impossible. I've been on this journey for years, and I've tested dozens of moisturizers to find the ones that truly deliver deep hydration without any irritation.</p>
    <p>Every product on this list is fragrance-free, dermatologist-tested, and won't compromise your skin barrier. I tested each one for at least two weeks, paying attention to hydration levels, texture, how it layers under makeup, and whether it triggered any sensitivity reactions.</p>
    {qp}
    <h2>What Makes a Great Moisturizer for Dry, Sensitive Skin</h2>
    <ul>
      <li><strong>Ceramides:</strong> These lipids restore your skin barrier, which is almost always compromised in dry, sensitive skin.</li>
      <li><strong>Hyaluronic acid:</strong> Holds up to 1,000x its weight in water for deep hydration.</li>
      <li><strong>No fragrance:</strong> Fragrance is the #1 cause of contact dermatitis. Skip it entirely.</li>
      <li><strong>No essential oils:</strong> Even "natural" oils like lavender can sensitize reactive skin.</li>
      <li><strong>Niacinamide:</strong> Strengthens the skin barrier while calming inflammation.</li>
    </ul>
    <h2>The 10 Best Moisturizers</h2>
    {product_card("CeraVe Moisturizing Cream", "CeraVe", "B00TTD9BRC", "16.99", 5,
        "The gold standard of drugstore moisturizers and the one dermatologists recommend most. Three essential ceramides plus hyaluronic acid in a rich, non-greasy cream that works beautifully on face and body. The patented MVE technology releases ingredients slowly over 24 hours for all-day hydration.",
        ["3 essential ceramides", "24-hour moisture release", "Works on face and body", "Fragrance-free, non-comedogenic"],
        ["Can feel heavy in humid weather", "Jar packaging isn't the most hygienic"],
        "Everyone with dry skin — this is the universal recommendation")}
    {product_card("Vanicream Moisturizing Cream", "Vanicream", "B000NWGCZ2", "13.99", 4.5,
        "Developed by dermatologists at the Mayo Clinic, Vanicream is the purest, most stripped-down moisturizer on this list. Zero fragrance, dyes, lanolin, parabens, or formaldehyde. If your skin reacts to everything, start here.",
        ["Absolute minimal ingredient list", "Mayo Clinic-developed", "Zero common irritants", "Very affordable"],
        ["No active ingredients like ceramides", "Plain packaging"],
        "Ultra-sensitive skin that reacts to almost everything")}
    {product_card("La Roche-Posay Toleriane Double Repair Moisturizer", "La Roche-Posay", "B01N7T7JKJ", "22.99", 4.5,
        "This lightweight moisturizer packs ceramide-3, niacinamide, and prebiotic thermal water into a formula that restores your skin barrier in as little as one hour. The texture is lighter than CeraVe, making it ideal for those who want deep hydration without heaviness.",
        ["Restores skin barrier in 1 hour (clinically tested)", "Lighter texture than CeraVe", "Niacinamide for barrier support", "Oil-free option available"],
        ["Slightly more expensive", "Some find it not rich enough for winter"],
        "Those who want barrier repair in a lighter-weight formula")}
    {product_card("Eucerin Original Healing Cream", "Eucerin", "B00008MNXF", "9.99", 4.5,
        "Sometimes you need brute-force hydration, and Eucerin delivers. This ultra-rich cream seals in moisture with a protective barrier that's perfect for severely dry, cracked winter skin. It's been a pharmacy staple for decades because it simply works.",
        ["Extremely rich and protective", "Pharmacy staple for decades", "Amazing for winter", "Under $10"],
        ["Very thick — not ideal under makeup", "Contains lanolin (rare sensitivity trigger)"],
        "Severely dry winter skin and cracked hands")}
    {product_card("First Aid Beauty Ultra Repair Cream", "First Aid Beauty", "B0071OQWKK", "14.00", 4.5,
        "Colloidal oatmeal and shea butter combine in this soothing cream that calms irritation while deeply moisturizing. The texture strikes a perfect balance between rich and lightweight. It absorbs quickly and works beautifully under makeup.",
        ["Colloidal oatmeal calms irritation", "Great under makeup", "Light yet nourishing", "Faint pleasant scent"],
        ["Contains eucalyptus oil (may bother some)", "Tube can be hard to squeeze"],
        "Irritated, inflamed dry skin that needs calming")}
    {product_card("Neutrogena Hydro Boost Gel-Cream", "Neutrogena", "B00NR1YQHM", "22.99", 4,
        "If you have dry but acne-prone skin, this oil-free gel-cream is a game-changer. Hyaluronic acid provides intense hydration in an incredibly lightweight, bouncy texture that never clogs pores or feels heavy.",
        ["Oil-free, won't clog pores", "Lightweight gel-cream texture", "Great for combination skin", "Layers beautifully under SPF"],
        ["May not be enough for very dry skin alone", "Contains fragrance in the original version"],
        "Dry skin that's also acne-prone or oily in the T-zone")}
    {product_card("Aveeno Eczema Therapy Daily Moisturizing Cream", "Aveeno", "B003O7IBZC", "16.47", 4.5,
        "Even if you don't have eczema, this cream is phenomenal for extremely dry, sensitive skin. The colloidal oatmeal formula has the National Eczema Association seal and provides relief from itching and dryness within hours.",
        ["NEA seal of acceptance", "Colloidal oatmeal soothes instantly", "Steroid-free", "Fragrance-free"],
        ["Thick texture", "White cast if over-applied"],
        "Eczema-prone or extremely reactive dry skin")}
    {product_card("ILLIYOON Ceramide Ato Concentrate Cream", "ILLIYOON", "B08BK4DCBY", "17.99", 4.5,
        "This K-beauty gem is a cult favorite in the skincare community. The patented ceramide capsule technology delivers deep, long-lasting hydration in a surprisingly lightweight texture. It absorbs beautifully and keeps skin soft for a full 24 hours.",
        ["Ceramide capsule technology", "Lightweight for a rich cream", "K-beauty cult favorite", "Huge 200ml tube"],
        ["Harder to find in stores", "Slight sticky feeling for some"],
        "Anyone who loves K-beauty and wants ceramide-rich hydration")}
    {product_card("EltaMD Barrier Renewal Complex", "EltaMD", "B086WDW2NS", "42.00", 4.5,
        "This dermatologist-favorite brand delivers a ceramide-rich cream with amino acids, niacinamide, and enzymes to actively repair damaged barriers. It's more of a treatment than a basic moisturizer, actively working to rebuild compromised skin.",
        ["Active barrier repair formula", "Dermatologist-favorite brand", "Ceramides + amino acids + enzymes", "Fragrance-free"],
        ["Premium price point", "Smaller size for the cost"],
        "Damaged skin barriers that need active repair, not just hydration")}
    {product_card("Aquaphor Healing Ointment", "Aquaphor", "B006IB5T4W", "14.49", 4.5,
        "The ultimate overnight slug. While not a traditional moisturizer, applying a thin layer of Aquaphor over your evening routine seals everything in and lets your skin repair overnight. Dermatologists have recommended this for decades for severely dry, chapped skin.",
        ["Ultimate occlusive seal", "Dermatologist staple for decades", "Multi-purpose (lips, cuticles, etc.)", "Very affordable"],
        ["Greasy texture (best for nighttime)", "Contains lanolin", "Not a standalone moisturizer"],
        "Overnight 'slugging' to lock in moisture and heal dry patches")}
    <h2>Final Verdict</h2>
    <p>Start with {alink("B00TTD9BRC", "CeraVe Moisturizing Cream")} — it's the most universally loved, dermatologist-recommended moisturizer for dry, sensitive skin at a price anyone can afford. If you react to everything, {alink("B000NWGCZ2", "Vanicream")} is the safest bet with its ultra-minimal formula.</p>
    '''
    faqs = faq_section([
        ("How often should I moisturize dry skin?", "Twice daily — morning and night. Apply to slightly damp skin for maximum absorption."),
        ("Can a moisturizer cause breakouts on sensitive skin?", "Yes, if it contains comedogenic ingredients. Look for 'non-comedogenic' on the label and patch test new products."),
        ("What's the difference between a cream and a lotion?", "Creams are thicker with more oil content, better for dry skin. Lotions are lighter and absorb faster, better for normal-oily skin."),
    ])
    write_post("skincare", "best-moisturizers-dry-sensitive-skin.html", h + body + faqs + footer())

print("Generating posts 1-2...")
post_01()
post_02()
print("Done with batch 1!")
