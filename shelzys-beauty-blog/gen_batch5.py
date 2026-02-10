#!/usr/bin/env python3
"""Generate posts 33-42 for Shelzy's Beauty Blog."""
import sys, os
sys.path.insert(0, "/home/user/claude-code/shelzys-beauty-blog")
from generate_posts import header, footer, product_card, quick_pick_table, faq_section, alink, abtn, write_post

TAG = "shelzysbeauty-20"

# ─────────────────────────────────────────────
# POST 33: Anti-Aging Routine
# ─────────────────────────────────────────────
def post_33():
    h = header(
        "A Dermatologist-Inspired Anti-Aging Routine You Can Build on Amazon",
        "Routines", 
        "Build a complete dermatologist-inspired anti-aging skincare routine with 7 proven products from Amazon. Vitamin C, retinol, peptides, and SPF — all under $165 total.",
        11)
    qp = quick_pick_table([
        ("Cleanser", "best-overall", "La Roche-Posay Toleriane Hydrating Cleanser", "B01N7T7JKJ", "15"),
        ("Vitamin C", "best-overall", "TruSkin Vitamin C Serum", "B01M4MCUAF", "22"),
        ("Peptides", "best-overall", "The Ordinary Buffet", "B0711Y5XBZ", "17"),
        ("Retinol", "best-overall", "CeraVe Resurfacing Retinol", "B07K3268DB", "18"),
        ("Eye Cream", "best-overall", "RoC Retinol Correxion Eye Cream", "B00AOAKVQ8", "25"),
        ("Moisturizer", "best-overall", "Olay Regenerist Micro-Sculpting Cream", "B0040MZAVI", "26"),
        ("SPF", "best-overall", "EltaMD UV Clear SPF 46", "B002MSN3QQ", "39"),
    ])
    body = f"""
    <p>When I hit my early 30s, I noticed changes that no amount of wishful thinking could undo — fine lines around my eyes, a subtle loss of firmness along my jawline, and dark spots that seemed to appear overnight. Sound familiar? The good news is that a well-constructed anti-aging routine doesn't require a dermatologist's budget. You just need the right active ingredients in the right order.</p>
    <p>I spent months researching what dermatologists actually recommend (not what influencers sell) and built a complete 7-step routine entirely from Amazon. Every product here targets a specific sign of aging with clinically proven ingredients — vitamin C for brightening, peptides for firmness, retinol for fine lines, and SPF to prevent further damage. The total cost? Under $165 for a routine that rivals what you'd get from a $500 consultation.</p>
    <p>Below, I'll walk you through each step, explain why it matters for aging skin, and share the exact product I use. Whether you're building your first anti-aging routine or upgrading an existing one, this guide has you covered.</p>
    {qp}

    <h2>Step 1: Gentle Cleanser — The Foundation of Any Routine</h2>
    <p>A gentle cleanser is even more important as you age. Harsh cleansers strip your skin of natural oils that become increasingly precious over time. Your cleanser should remove dirt and makeup without disrupting your skin barrier, which is already thinning with age. A compromised barrier accelerates fine lines and dullness.</p>
    {product_card("La Roche-Posay Toleriane Hydrating Gentle Cleanser", "La Roche-Posay", "B01N7T7JKJ", "14.99", 4.5,
        "This creamy, non-foaming cleanser respects your skin barrier while thoroughly cleaning. Formulated with ceramides, niacinamide, and La Roche-Posay's prebiotic thermal water, it leaves skin feeling soft and hydrated — never tight or stripped. It's the cleanser dermatologists recommend most for mature and sensitive skin.",
        ["Ceramides and niacinamide support barrier", "Non-foaming, ultra-gentle", "Removes makeup effectively", "Fragrance-free and pH-balanced"],
        ["Won't remove heavy waterproof makeup alone", "Some prefer a foaming feel"],
        "Mature or sensitive skin needing a gentle daily cleanser")}

    <h2>Step 2: Vitamin C Serum — Morning Brightening + Protection</h2>
    <p>Vitamin C is the single best morning active for aging skin. It neutralizes free radicals from UV exposure and pollution, boosts collagen production, and fades dark spots and uneven tone. Think of it as your skin's daily shield against the environmental damage that accelerates aging.</p>
    {product_card("TruSkin Vitamin C Serum", "TruSkin", "B01M4MCUAF", "21.99", 4.5,
        "This bestselling serum combines 15% vitamin C with hyaluronic acid and vitamin E for a triple-threat formula that brightens, hydrates, and protects. After 6 weeks of daily use, my sun spots were noticeably lighter and my overall complexion had a luminous quality it hadn't had in years. It layers beautifully under SPF and moisturizer.",
        ["15% vitamin C with vitamin E for stability", "Visible brightening in 4-6 weeks", "Lightweight, absorbs quickly", "Pairs perfectly with SPF"],
        ["Earthy natural scent", "Must be stored away from sunlight"],
        "Anyone wanting to address dullness, dark spots, and prevent further damage")}

    <h2>Step 3: Peptide Serum — Firmness and Texture</h2>
    <p>Peptides are amino acid chains that signal your skin to produce more collagen and elastin — the proteins responsible for that firm, bouncy quality we associate with youthful skin. While retinol gets all the attention, peptides work synergistically with it and are gentle enough for everyday use. They're the unsung heroes of anti-aging.</p>
    {product_card("The Ordinary Buffet", "The Ordinary", "B0711Y5XBZ", "16.99", 4.5,
        "Buffet is aptly named — it's a cocktail of multiple peptide technologies, amino acids, and hyaluronic acid all in one serum. Matrixyl 3000, Matrixyl synthe'6, SYN-AKE, and more work together to target multiple signs of aging simultaneously. After two months, I noticed my skin felt significantly firmer and my fine lines around the mouth were softer.",
        ["Multi-peptide formula targets multiple concerns", "Hyaluronic acid for hydration", "Gentle enough for daily AM and PM use", "Incredible value for the ingredients"],
        ["Slightly tacky texture while drying", "Results take 8+ weeks to notice"],
        "Those wanting to improve firmness and smooth fine lines without irritation")}

    <h2>Step 4: Retinol — The Gold Standard (PM Only)</h2>
    <p>If there's one ingredient with the most scientific backing for anti-aging, it's retinol. A derivative of vitamin A, retinol accelerates cell turnover, stimulates collagen production, smooths fine lines, and evens skin tone. Use it at night since it increases sun sensitivity, and always pair with SPF the next morning.</p>
    {product_card("CeraVe Resurfacing Retinol Serum", "CeraVe", "B07K3268DB", "17.99", 4.5,
        "What makes this retinol stand out is the encapsulated delivery system that releases retinol gradually, reducing irritation while maintaining efficacy. The addition of ceramides and niacinamide means it actually supports your skin barrier while delivering anti-aging benefits. Most retinols compromise your barrier — this one strengthens it.",
        ["Encapsulated retinol for gradual release", "Ceramides protect the skin barrier", "Niacinamide reduces potential irritation", "Lightweight, non-greasy formula"],
        ["Lower concentration (good for beginners)", "May need to upgrade after 6+ months"],
        "Retinol beginners or those with sensitive skin who want anti-aging without irritation")}

    <h2>Step 5: Eye Cream — Targeted Care for Delicate Skin</h2>
    <p>The skin around your eyes is up to 10 times thinner than the rest of your face, making it the first area to show aging. A dedicated eye cream with retinol can address crow's feet, dark circles, and puffiness without the irritation that a full-strength face retinol might cause in this delicate area.</p>
    {product_card("RoC Retinol Correxion Eye Cream", "RoC", "B00AOAKVQ8", "24.99", 4.5,
        "RoC has been in the retinol game longer than almost anyone, and this eye cream shows that expertise. The mineral complex combined with pure retinol visibly reduces crow's feet and under-eye lines. In clinical tests, 94% of users saw visible improvement in fine lines around the eyes in 12 weeks.",
        ["Clinically proven to reduce crow's feet", "Gentle enough for the eye area", "Mineral complex enhances results", "Trusted brand with decades of retinol expertise"],
        ["Takes 8-12 weeks for visible results", "Small tube for the price"],
        "Anyone concerned about crow's feet, fine lines, or puffiness around the eyes")}

    <h2>Step 6: Moisturizer — Lock It All In</h2>
    <p>A rich moisturizer seals in all your active ingredients and provides an additional layer of anti-aging benefits. For aging skin, look for ingredients like niacinamide, peptides, and hyaluronic acid — and avoid anything that will sit heavily or clog pores.</p>
    {product_card("Olay Regenerist Micro-Sculpting Cream", "Olay", "B0040MZAVI", "25.99", 4.5,
        "Don't let the drugstore price fool you — Olay Regenerist has outperformed high-end creams in independent testing. The formula includes amino-peptides, niacinamide, and hyaluronic acid to plump, firm, and hydrate. It absorbs quickly, works beautifully under makeup, and provides a subtle plumping effect that's visible within hours.",
        ["Outperforms many luxury creams in blind tests", "Amino-peptides and niacinamide", "Visible plumping effect", "Elegant texture, great under makeup"],
        ["Contains fragrance", "Jar packaging"],
        "Those wanting a multi-benefit anti-aging moisturizer at a drugstore price")}

    <h2>Step 7: SPF — The Most Important Anti-Aging Step</h2>
    <p>Up to 90% of visible skin aging is caused by UV exposure. You can use every serum and cream on this list, but without daily SPF, you're fighting a losing battle. SPF is non-negotiable — it prevents new damage while your other products repair existing damage.</p>
    {product_card("EltaMD UV Clear Broad-Spectrum SPF 46", "EltaMD", "B002MSN3QQ", "39.00", 5,
        "The #1 dermatologist-recommended sunscreen in the US, and for good reason. This zinc oxide-based formula includes niacinamide and hyaluronic acid, so it actively improves your skin while protecting it. It's oil-free, fragrance-free, and leaves zero white cast. It's the only sunscreen I've ever enjoyed applying daily.",
        ["#1 dermatologist-recommended SPF", "Niacinamide and hyaluronic acid included", "Zero white cast, elegant finish", "Oil-free, won't clog pores"],
        ["Higher price point", "Only SPF 46 (still more than adequate)"],
        "Anyone serious about preventing premature aging — this is THE sunscreen to own")}

    <h2>How to Layer Your Routine</h2>
    <h3>Morning Routine</h3>
    <ol>
      <li>{alink("B01N7T7JKJ", "La Roche-Posay Toleriane Cleanser")} — Gentle cleanse</li>
      <li>{alink("B01M4MCUAF", "TruSkin Vitamin C Serum")} — Wait 1-2 minutes to absorb</li>
      <li>{alink("B0711Y5XBZ", "The Ordinary Buffet")} — Peptides for firmness</li>
      <li>{alink("B00AOAKVQ8", "RoC Eye Cream")} — Pat gently around eye area</li>
      <li>{alink("B0040MZAVI", "Olay Regenerist")} — Moisturize</li>
      <li>{alink("B002MSN3QQ", "EltaMD UV Clear SPF 46")} — Final step, always</li>
    </ol>
    <h3>Evening Routine</h3>
    <ol>
      <li>{alink("B01N7T7JKJ", "La Roche-Posay Toleriane Cleanser")} — Double cleanse if wearing makeup</li>
      <li>{alink("B0711Y5XBZ", "The Ordinary Buffet")} — Peptides</li>
      <li>{alink("B07K3268DB", "CeraVe Resurfacing Retinol")} — Use 3-4 nights per week to start</li>
      <li>{alink("B00AOAKVQ8", "RoC Eye Cream")} — Nightly eye treatment</li>
      <li>{alink("B0040MZAVI", "Olay Regenerist")} — Seal everything in</li>
    </ol>

    <h2>Final Verdict</h2>
    <p>You don't need a $500 dermatologist consultation to build an effective anti-aging routine. These seven products cover every evidence-based anti-aging category — antioxidant protection, peptide support, retinol treatment, and UV defense — for under $165 total. Start with the {alink("B07K3268DB", "CeraVe Retinol")} and {alink("B002MSN3QQ", "EltaMD SPF")} if you can only buy two products today. Those two steps alone will make the biggest visible difference in your skin over the next 3-6 months.</p>
"""
    faqs = faq_section([
        ("At what age should I start an anti-aging routine?",
         "Prevention is easier than correction. Starting a basic routine with SPF and vitamin C in your mid-20s is ideal. Retinol can be introduced in your late 20s to early 30s. But it's never too late to start — you'll still see significant improvements at any age."),
        ("Can I use all these products together without irritation?",
         "Start slowly. Introduce one new product every 1-2 weeks so your skin can adjust. Retinol should begin at 2-3 nights per week and gradually increase to nightly. If you experience irritation, scale back and rebuild."),
        ("How long until I see results from this routine?",
         "You'll notice improved hydration and glow within 1-2 weeks. Brightening from vitamin C shows around 4-6 weeks. Fine line improvement from retinol and peptides becomes visible at 8-12 weeks. Full results develop over 3-6 months of consistent use."),
        ("Is this routine safe for sensitive skin?",
         "Yes, every product here is formulated to be gentle. The CeraVe retinol has encapsulated delivery to reduce irritation, and the La Roche-Posay cleanser is specifically designed for sensitive skin. Just introduce products gradually."),
    ])
    write_post("routines-guides", "anti-aging-routine-amazon.html", h + body + faqs + footer())


# ─────────────────────────────────────────────
# POST 34: Korean Skincare Routine for Beginners
# ─────────────────────────────────────────────
def post_34():
    h = header(
        "The Perfect 5-Step Korean Skincare Routine for Beginners (All Under $20)",
        "Routines",
        "Build the perfect beginner Korean skincare routine with 6 products all under $20 each. Double cleanse, tone, essence, moisturize, and protect with K-beauty favorites.",
        9)
    qp = quick_pick_table([
        ("Oil Cleanser", "best-overall", "BANILA CO Clean It Zero", "B00LNQ61QC", "18"),
        ("Water Cleanser", "budget", "COSRX Low pH Good Morning Gel Cleanser", "B016NRXO06", "11"),
        ("Toner", "best-overall", "Etude SoonJung pH 5.5 Relief Toner", "B07C6L9FPH", "12"),
        ("Essence", "best-overall", "COSRX Advanced Snail 96 Mucin", "B00PBX3L7K", "13"),
        ("Moisturizer", "best-overall", "ILLIYOON Ceramide Ato Concentrate Cream", "B08BK4DCBY", "18"),
        ("SPF", "budget", "Beauty of Joseon Relief Sun", "B0B6Q2JY8Y", "16"),
    ])
    body = f"""
    <p>Korean skincare changed everything I thought I knew about taking care of my skin. After years of slapping on a single moisturizer and calling it a day, I discovered the K-beauty philosophy: treating your skin with layers of lightweight, targeted hydration rather than one heavy product. The results? Plumper, glowier, more resilient skin than I'd ever had.</p>
    <p>But the famous 10-step Korean routine? Totally unnecessary for beginners. In fact, most Korean women don't actually do 10 steps daily. The real magic is in the core 5 steps: double cleanse, tone, essence, moisturize, and protect. Master these, and you'll see the transformation that made K-beauty a global phenomenon.</p>
    <p>The best part? Every product in this routine costs under $20. You can build the complete 5-step routine for under $90 total — less than a single luxury serum.</p>
    {qp}

    <h2>Step 1: Oil Cleanser — Melt Away Sunscreen and Makeup</h2>
    <p>Double cleansing is the cornerstone of Korean skincare, and it starts with an oil-based cleanser. Oil dissolves oil — meaning it effortlessly melts away sunscreen, makeup, and the natural sebum that accumulates throughout the day. No tugging, no harsh rubbing. If you take one thing from K-beauty, let it be this step.</p>
    {product_card("BANILA CO Clean It Zero Cleansing Balm", "BANILA CO", "B00LNQ61QC", "17.99", 4.5,
        "This cult-classic cleansing balm has sold over 25 million units worldwide, and one use will show you why. The sherbet-like texture transforms into a silky oil on contact, dissolving every trace of sunscreen and makeup without leaving residue. It rinses clean with water — no greasy film, no clogged pores. It made double cleansing click for me instantly.",
        ["Sherbet texture is satisfying to use", "Removes waterproof sunscreen completely", "Rinses clean, no residue", "Contains nourishing botanical extracts"],
        ["Jar packaging requires clean hands", "Original has light fragrance"],
        "Anyone new to double cleansing who wants an easy, effective introduction")}

    <h2>Step 2: Water Cleanser — Deep Clean Without Stripping</h2>
    <p>After the oil cleanser removes surface grime, a gentle water-based cleanser sweeps away any remaining impurities, sweat, and residue. The key word here is gentle — Korean water cleansers are formulated at a low pH to match your skin's natural acidity, preventing the tight, stripped feeling Western cleansers often cause.</p>
    {product_card("COSRX Low pH Good Morning Gel Cleanser", "COSRX", "B016NRXO06", "10.99", 4.5,
        "This gel cleanser is a K-beauty staple for good reason. Formulated at pH 5.0-6.0 to respect your skin's acid mantle, it uses mild BHA (betaine salicylate) to gently purify without irritation. The gel lathers into a soft foam that rinses clean, leaving skin fresh and balanced. At $11, it lasts about 3 months of daily use.",
        ["Low pH respects skin barrier", "Mild BHA for gentle daily purifying", "Lasts months with daily use", "Under $12"],
        ["Tea tree scent isn't for everyone", "Not enough for heavy makeup removal alone"],
        "All skin types — a universal second cleanser")}

    <h2>Step 3: Toner — Prep and Balance</h2>
    <p>Korean toners are nothing like the astringent, alcohol-laden Western toners of the '90s. In K-beauty, toner is a hydrating prep step that balances your skin's pH after cleansing and helps subsequent products absorb more effectively. Think of it as priming a canvas before painting.</p>
    {product_card("Etude SoonJung pH 5.5 Relief Toner", "Etude", "B07C6L9FPH", "11.99", 4.5,
        "From Etude's sensitive skin line, this toner has a 97% naturally derived formula with panthenol (vitamin B5) and madecassoside to hydrate and calm. The watery texture absorbs instantly and creates the perfect base for your essence and moisturizer. Even my most reactive days never had an issue with this toner.",
        ["97% naturally derived ingredients", "Panthenol soothes and hydrates", "pH 5.5 matches skin's natural acidity", "Fragrance-free and hypoallergenic"],
        ["Very minimal — no dramatic visible results alone", "Bottle could be bigger for the price"],
        "Sensitive or reactive skin that needs gentle hydrating prep")}

    <h2>Step 4: Essence — The Heart of Korean Skincare</h2>
    <p>If one step sets K-beauty apart from Western routines, it's essence. This lightweight, watery product delivers concentrated hydration and active ingredients deep into your skin. Essence is responsible for that famous 'glass skin' glow — the bouncy, translucent, impossibly dewy complexion that Korean skincare is known for.</p>
    {product_card("COSRX Advanced Snail 96 Mucin Power Essence", "COSRX", "B00PBX3L7K", "13.00", 4.5,
        "Yes, it contains 96% snail mucin. No, it's not gross — it's transformative. This viscous, slightly stringy essence delivers intense hydration, promotes skin repair, and gives you that coveted dewy glow. Snail mucin naturally contains glycoproteins, hyaluronic acid, and glycolic acid. After one week, you'll wonder how you ever lived without it.",
        ["96% snail secretion filtrate", "Deeply hydrating and repairing", "Gives instant dewy glow", "A little goes a very long way"],
        ["Stringy texture takes getting used to", "Not vegan"],
        "Anyone chasing the 'glass skin' look or wanting deep lightweight hydration")}

    <h2>Step 5: Moisturizer — Seal and Protect</h2>
    <p>A good moisturizer locks in all the hydration layers you've applied and strengthens your skin barrier. Korean moisturizers tend to be lighter than their Western counterparts, relying on ceramides and lightweight oils rather than heavy occlusives. The result is moisture that feels like skin, not a mask.</p>
    {product_card("ILLIYOON Ceramide Ato Concentrate Cream", "ILLIYOON", "B08BK4DCBY", "17.99", 4.5,
        "This ceramide-rich cream is a K-beauty cult favorite that rivals CeraVe at a similar price point. The patented Ceramide Capsule technology delivers long-lasting hydration while strengthening the skin barrier. Despite being rich enough for dry skin, it absorbs surprisingly well and never feels heavy or greasy. The 200ml tube lasts about 4 months.",
        ["Patented ceramide capsule technology", "Rich yet lightweight texture", "Huge 200ml tube lasts months", "Dermatologist-tested, fragrance-free"],
        ["Can be slightly sticky in humid weather", "Plain packaging"],
        "All skin types, especially dry or compromised barriers")}

    <h2>Bonus Step: SPF — Complete the Routine</h2>
    <p>No Korean skincare routine is complete without sun protection. K-beauty sunscreens are legendary for their elegant formulas that feel like skincare, not sunscreen. No white cast, no greasy residue — just lightweight protection that makes you actually want to reapply.</p>
    {product_card("Beauty of Joseon Relief Sun: Rice + Probiotics SPF 50+", "Beauty of Joseon", "B0B6Q2JY8Y", "16.00", 5,
        "This sunscreen broke the internet for a reason. The rice bran and probiotic formula provides SPF 50+ PA++++ protection while feeling like a lightweight moisturizer. It leaves a beautiful dewy finish with zero white cast, layers perfectly under makeup, and actually improves your skin over time. This is the sunscreen that converted me from SPF-avoider to daily-applier.",
        ["SPF 50+ PA++++ broad spectrum", "Feels like a lightweight moisturizer", "Zero white cast on all skin tones", "Rice bran and probiotics nourish skin"],
        ["Can be too dewy for very oily skin", "Sells out frequently"],
        "Everyone — especially those who hate the feel of traditional sunscreen")}

    <h2>The Complete Routine Order</h2>
    <h3>Evening Routine (All 5 Steps)</h3>
    <ol>
      <li>{alink("B00LNQ61QC", "BANILA CO Clean It Zero")} — Massage onto dry face to dissolve sunscreen/makeup</li>
      <li>{alink("B016NRXO06", "COSRX Good Morning Gel Cleanser")} — Lather on wet skin, rinse</li>
      <li>{alink("B07C6L9FPH", "Etude SoonJung Toner")} — Pat into damp skin with hands</li>
      <li>{alink("B00PBX3L7K", "COSRX Snail Mucin Essence")} — Press 2-3 drops into skin</li>
      <li>{alink("B08BK4DCBY", "ILLIYOON Ceramide Cream")} — Seal everything in</li>
    </ol>
    <h3>Morning Routine (Simplified)</h3>
    <ol>
      <li>{alink("B016NRXO06", "COSRX Good Morning Gel Cleanser")} — Just the water cleanser</li>
      <li>{alink("B07C6L9FPH", "Etude SoonJung Toner")} — Hydrating prep</li>
      <li>{alink("B00PBX3L7K", "COSRX Snail Mucin Essence")} — Dewy base</li>
      <li>{alink("B08BK4DCBY", "ILLIYOON Ceramide Cream")} — Moisturize</li>
      <li>{alink("B0B6Q2JY8Y", "Beauty of Joseon Relief Sun")} — SPF always last</li>
    </ol>

    <h2>Final Verdict</h2>
    <p>Korean skincare doesn't have to be complicated or expensive. These 6 products give you a complete, effective K-beauty routine for under $90 total. Start with the double cleanse ({alink("B00LNQ61QC", "BANILA CO")} + {alink("B016NRXO06", "COSRX Gel Cleanser")}) and the {alink("B00PBX3L7K", "COSRX Snail Mucin Essence")} — those three products alone will transform your skin within two weeks. Add the rest as your budget allows, and welcome to the glow.</p>
"""
    faqs = faq_section([
        ("Do I really need to double cleanse every night?",
         "If you wear sunscreen (which you should), yes. Oil cleansers remove sunscreen and makeup that water-based cleansers can't fully dissolve. In the morning, a single water cleanser is sufficient."),
        ("Is snail mucin safe to use?",
         "Yes, snail mucin has been used in skincare for decades and is well-studied. It's harvested ethically without harming the snails. It's safe for all skin types including sensitive skin. The only exception is if you have a mollusk allergy."),
        ("Can I do the Korean routine with oily or acne-prone skin?",
         "Absolutely. The layering approach actually helps oily skin by providing adequate hydration so your skin produces less excess oil. Just choose gel or water-based products and skip heavy creams."),
        ("How long does a 5-step routine take?",
         "About 5-7 minutes once you get the hang of it. The evening routine with double cleansing takes slightly longer. Most of the time is waiting for products to absorb between layers."),
    ])
    write_post("routines-guides", "korean-skincare-routine-beginners.html", h + body + faqs + footer())



# ─────────────────────────────────────────────
# POST 35: Nighttime Routine for Acne-Prone Skin
# ─────────────────────────────────────────────
def post_35():
    h = header(
        "My Nighttime Skincare Routine for Acne-Prone Skin (What Finally Worked)",
        "Routines",
        "The exact nighttime skincare routine that finally cleared my acne-prone skin. Oil cleansing, adapalene, niacinamide, and more — all affordable Amazon finds.",
        9)
    qp = quick_pick_table([
        ("Oil Cleanser", "best-overall", "DHC Deep Cleansing Oil", "B001UE60E0", "17"),
        ("Gel Cleanser", "best-overall", "CeraVe SA Smoothing Cleanser", "B01N1LL62W", "15"),
        ("Treatment", "best-overall", "Differin Adapalene Gel", "B07L1PHSY6", "15"),
        ("Niacinamide", "budget", "The Ordinary Niacinamide 10%", "B06VSS3FPB", "7"),
        ("Moisturizer", "best-overall", "Neutrogena Hydro Boost Gel-Cream", "B00NR1YQHM", "23"),
        ("Spot Treatment", "budget", "Hero Cosmetics Mighty Patch", "B074PVTPBW", "13"),
    ])
    body = f"""
    <p>I spent years fighting acne with the wrong approach — harsh cleansers, alcohol-based toners, and skipping moisturizer because I thought it would make me break out more. My skin was simultaneously oily, dehydrated, irritated, and still covered in breakouts. It was a frustrating cycle of stripping and overproducing oil that made everything worse.</p>
    <p>The routine that finally worked was the opposite of what I expected. Gentle cleansing (including oil cleansing, which sounded terrifying), a targeted prescription-strength retinoid, and actually moisturizing my acne-prone skin. Within 8 weeks, my breakouts reduced by about 70%. Within 6 months, I had the clearest skin of my adult life.</p>
    <p>Here's the exact nighttime routine that transformed my acne-prone skin, step by step. Every product is available on Amazon, and the total cost is under $90.</p>
    {qp}

    <h2>Step 1: Oil Cleanser — Yes, Even for Acne-Prone Skin</h2>
    <p>I know what you're thinking: putting oil on acne-prone skin sounds insane. But oil cleansing is actually one of the most effective ways to remove pore-clogging sunscreen, makeup, and excess sebum. The principle is simple — oil dissolves oil. Unlike harsh foaming cleansers that strip your skin and trigger more oil production, an oil cleanser gently lifts impurities without disrupting your moisture barrier.</p>
    {product_card("DHC Deep Cleansing Oil", "DHC", "B001UE60E0", "17.00", 4.5,
        "Japan's #1 selling cleansing oil for over 20 years, and it earned that title. This olive oil-based formula melts away every trace of sunscreen and makeup, including stubborn waterproof formulas, then emulsifies and rinses completely clean with water. No residue, no clogged pores. It actually helped reduce my blackheads over time by dissolving the oxidized sebum in my pores.",
        ["Japan's #1 cleansing oil for 20+ years", "Removes absolutely everything", "Rinses clean with zero residue", "Non-comedogenic despite being oil-based"],
        ["Olive oil scent is mild but present", "Pump can be stiff"],
        "Anyone wearing sunscreen daily (which should be everyone) who needs thorough cleansing")}

    <h2>Step 2: Gel Cleanser — Gentle Exfoliation</h2>
    <p>After oil cleansing, a gentle gel cleanser removes any remaining impurities. For acne-prone skin, a formula with salicylic acid provides mild daily exfoliation that helps prevent clogged pores — the root cause of most breakouts. The key is a low concentration that works over time without causing irritation.</p>
    {product_card("CeraVe SA Smoothing Cleanser", "CeraVe", "B01N1LL62W", "14.99", 4.5,
        "This cleanser combines salicylic acid with ceramides and hyaluronic acid — so it exfoliates and purifies while simultaneously supporting your moisture barrier. Most acne cleansers strip and dry out your skin; this one cleans, treats, and hydrates in one step. The gel texture foams lightly and rinses clean without that tight, stripped feeling.",
        ["Salicylic acid for daily gentle exfoliation", "Ceramides protect skin barrier", "Fragrance-free and non-comedogenic", "Won't strip or over-dry"],
        ["SA concentration is low (gentle, not aggressive)", "Pump bottle can be messy"],
        "Acne-prone skin that's tired of harsh, stripping cleansers")}

    <h2>Step 3: Treatment — The Game Changer</h2>
    <p>Adapalene (the active ingredient in Differin) was prescription-only until 2016, and it remains the single most effective OTC treatment for acne. It's a retinoid that normalizes skin cell turnover, preventing dead cells from clogging pores in the first place. It also has anti-inflammatory properties that reduce the redness and swelling of active breakouts. This is the step that made the biggest difference in my skin.</p>
    {product_card("Differin Adapalene Gel 0.1%", "Differin", "B07L1PHSY6", "14.99", 5,
        "Formerly prescription-only, Differin is the only retinoid FDA-approved for over-the-counter acne treatment. Unlike benzoyl peroxide that treats existing pimples, adapalene prevents new breakouts from forming by normalizing cell turnover deep in the pore. Expect a 'purging' period of 2-4 weeks where things may look worse before they get dramatically better. Push through — it's worth it.",
        ["FDA-approved retinoid for OTC acne treatment", "Prevents breakouts at the source", "Anti-inflammatory properties", "Once-daily application, long-lasting results"],
        ["Purging period in weeks 2-4", "Can cause dryness and peeling initially", "Must use SPF the next morning"],
        "Anyone with persistent acne who wants the most clinically effective OTC treatment")}

    <h2>Step 4: Niacinamide — Calm Inflammation and Control Oil</h2>
    <p>Niacinamide (vitamin B3) is a multitasking powerhouse for acne-prone skin. It regulates oil production, reduces inflammation and redness, minimizes the appearance of pores, and fades post-acne marks. Applied after your retinoid, it helps soothe any irritation while delivering its own acne-fighting benefits.</p>
    {product_card("The Ordinary Niacinamide 10% + Zinc 1%", "The Ordinary", "B06VSS3FPB", "6.80", 4.5,
        "At under $7, this serum delivers clinical concentrations of niacinamide and zinc — both proven to reduce sebum production and calm inflammation. I noticed my pores looked smaller within 2 weeks, and the oiliness in my T-zone was significantly reduced. It layers well under moisturizer and doesn't pill or feel heavy.",
        ["10% niacinamide + zinc for oil control", "Visibly reduces pore appearance", "Fades post-acne dark marks", "Under $7 — incredible value"],
        ["Can pill if applied too heavily", "Some experience mild tingling initially"],
        "Oily, acne-prone skin needing oil control and pore refinement")}

    <h2>Step 5: Moisturizer — Hydrate Without Breaking Out</h2>
    <p>Skipping moisturizer is the biggest mistake people with acne-prone skin make. Dehydrated skin overproduces oil to compensate, leading to more breakouts. The right moisturizer hydrates without clogging pores, and it's essential when using retinoids like Differin that can cause dryness.</p>
    {product_card("Neutrogena Hydro Boost Gel-Cream (Extra Dry Skin)", "Neutrogena", "B00NR1YQHM", "22.99", 4.5,
        "This oil-free gel-cream uses hyaluronic acid to deliver intense hydration in an incredibly lightweight, bouncy texture that never clogs pores. The fragrance-free Extra Dry version is the one you want — it's richer than the regular Hydro Boost but still won't break you out. It absorbs in seconds and leaves skin plump and comfortable without a trace of greasiness.",
        ["Oil-free, non-comedogenic", "Hyaluronic acid for deep hydration", "Lightweight gel-cream texture", "Perfect for pairing with retinoids"],
        ["Won't be enough for very dry skin in winter", "Hydration may not last 24 hours"],
        "Acne-prone skin that needs hydration without heaviness or breakouts")}

    <h2>Step 6: Spot Treatment — Target Active Breakouts</h2>
    <p>Even with the best routine, occasional breakouts happen. Having a targeted spot treatment on hand means you can deal with surprise pimples without disrupting your entire routine. Hydrocolloid patches are the gentlest, most effective option — they draw out fluid, protect the blemish from picking, and speed healing overnight.</p>
    {product_card("Hero Cosmetics Mighty Patch Original", "Hero Cosmetics", "B074PVTPBW", "12.99", 4.5,
        "These hydrocolloid patches are the best thing that happened to my breakouts. Stick one on a pimple before bed, and by morning it's drawn out the fluid and flattened the blemish dramatically. They also prevent you from picking (which causes scarring), and they protect the breakout from bacteria while it heals. They work on pimples that have come to a head — not deep cystic acne.",
        ["Visibly flattens pimples overnight", "Prevents picking and scarring", "Drug-free, gentle hydrocolloid technology", "36 patches per pack"],
        ["Only works on surfaced pimples, not cystic acne", "Can be visible during the day"],
        "Anyone who picks at their skin or wants faster overnight pimple healing")}

    <h2>The Complete Nighttime Routine Order</h2>
    <ol>
      <li>{alink("B001UE60E0", "DHC Deep Cleansing Oil")} — Massage onto dry skin for 60 seconds, rinse</li>
      <li>{alink("B01N1LL62W", "CeraVe SA Smoothing Cleanser")} — Gentle lather on wet skin, rinse</li>
      <li>Pat skin dry, wait 1-2 minutes</li>
      <li>{alink("B07L1PHSY6", "Differin Gel")} — Pea-sized amount, spread thin over entire face (not just spots)</li>
      <li>Wait 5-10 minutes for absorption</li>
      <li>{alink("B06VSS3FPB", "The Ordinary Niacinamide")} — 2-3 drops, pat in gently</li>
      <li>{alink("B00NR1YQHM", "Neutrogena Hydro Boost")} — Seal everything in</li>
      <li>{alink("B074PVTPBW", "Mighty Patch")} — Apply to any active surfaced pimples</li>
    </ol>

    <h2>Final Verdict</h2>
    <p>This routine works because it addresses acne from multiple angles: thorough but gentle cleansing, prescription-strength prevention with {alink("B07L1PHSY6", "Differin")}, oil control with {alink("B06VSS3FPB", "niacinamide")}, proper hydration, and targeted spot treatment. Give it a full 12 weeks before judging — retinoids need time. But if you stick with it, this under-$90 routine can deliver results that rival prescription acne programs.</p>
"""
    faqs = faq_section([
        ("What is retinoid purging and how long does it last?",
         "Purging is a temporary increase in breakouts that occurs when retinoids speed up cell turnover, bringing existing clogs to the surface faster. It typically lasts 2-6 weeks. If breakouts continue after 8 weeks or appear in areas you don't normally break out, it may be a reaction rather than purging."),
        ("Can I use Differin and niacinamide together?",
         "Yes. Niacinamide actually helps buffer the irritation from retinoids while providing its own acne-fighting benefits. Apply Differin first, wait a few minutes, then layer niacinamide on top."),
        ("Should I use this routine every night?",
         "Start with Differin every other night for the first 2-4 weeks while your skin adjusts. The other steps can be done nightly from the start. Gradually increase Differin to nightly use as your skin tolerates it."),
    ])
    write_post("routines-guides", "nighttime-routine-acne-prone.html", h + body + faqs + footer())


# ─────────────────────────────────────────────
# POST 36: Curly Hair Routine for Beginners
# ─────────────────────────────────────────────
def post_36():
    h = header(
        "How to Build a Complete Curly Hair Routine from Scratch (Beginner's Guide)",
        "Routines",
        "Build a complete curly hair routine from scratch. Shampoo, condition, style, and dry your curls with affordable products and techniques for beginners.",
        11)
    qp = quick_pick_table([
        ("Shampoo", "best-overall", "SheaMoisture Coconut & Hibiscus Shampoo", "B0038TVH3Y", "10"),
        ("Conditioner", "best-overall", "SheaMoisture Coconut & Hibiscus Conditioner", "B0038TYESG", "10"),
        ("Leave-In", "best-overall", "Kinky-Curly Knot Today", "B003PC8UBU", "13"),
        ("Gel", "budget", "Eco Style Olive Oil Gel", "B004BME3AO", "5"),
        ("Deep Conditioner", "best-overall", "SheaMoisture Manuka Honey Masque", "B00SYELKOE", "12"),
        ("Microfiber Towel", "best-overall", "Aquis Original Hair Towel", "B01MSEZ3T7", "16"),
        ("Diffuser", "premium", "DevaCurl DevaFuser", "B079VK3BWF", "50"),
    ])
    body = f"""
    <p>If you've spent years straightening, blow-drying, or just being confused by your curly hair, you're not alone. Most of us grew up without anyone teaching us how to properly care for curls. We were handed a bottle of shampoo designed for straight hair, told to brush our hair dry, and wondered why it looked like a frizzy triangle. Sound familiar?</p>
    <p>The curly hair community has come a long way, and the good news is that building a proper curly routine doesn't require a cosmetology degree or a cabinet full of expensive products. It comes down to understanding a few key principles: moisture is king, sulfates are (usually) the enemy, and how you dry your hair matters as much as what you put on it.</p>
    <p>This guide walks you through every step of a beginner curly routine — from wash day to styling to drying — with affordable products that work across curl types from wavy (2A-2C) to coily (4A-4C). Let's finally give your curls what they've been asking for.</p>
    {qp}

    <h2>Step 1: Shampoo — Cleanse Without Stripping</h2>
    <p>The biggest mistake curlies make is using sulfate-heavy shampoos that strip natural oils from the hair shaft. Curly hair is inherently drier than straight hair because the oils from your scalp can't travel down the twists and bends of each strand. A sulfate-free shampoo cleanses your scalp without removing the moisture your curls desperately need.</p>
    {product_card("SheaMoisture Coconut & Hibiscus Curl & Shine Shampoo", "SheaMoisture", "B0038TVH3Y", "9.99", 4.5,
        "This sulfate-free shampoo uses coconut oil, silk protein, and neem oil to cleanse while adding moisture and shine. It lathers decently for a sulfate-free formula and leaves curls feeling clean but not stripped. The coconut-hibiscus scent is gorgeous and lingers gently. Use it 1-2 times per week, or less if your hair is very dry or coily.",
        ["Sulfate-free, gentle cleansing", "Coconut oil adds moisture while washing", "Silk protein strengthens curls", "Amazing natural scent"],
        ["May not be clarifying enough for heavy product buildup", "Can weigh down fine, wavy hair"],
        "Medium to coarse curly hair (2C-4C) needing moisture-preserving cleansing")}

    <h2>Step 2: Conditioner — Your Curl's Best Friend</h2>
    <p>Conditioner is where the magic happens for curly hair. This is not a quick rinse-and-go step — it's a 3-5 minute treatment where you detangle, hydrate, and prepare your curls for styling. Apply generously, use your fingers or a wide-tooth comb to detangle from ends to roots (never roots to ends), and let it sit while you finish the rest of your shower.</p>
    {product_card("SheaMoisture Coconut & Hibiscus Curl & Shine Conditioner", "SheaMoisture", "B0038TYESG", "9.99", 4.5,
        "The matching conditioner to the shampoo above, and arguably the more important product. The rich, creamy formula provides intense slip for detangling, and the coconut oil, silk protein, and neem oil combination leaves curls defined, soft, and moisturized. I leave it on for 3-5 minutes, detangle with fingers, then rinse with cool water to seal the cuticle.",
        ["Excellent slip for detangling", "Rich moisture without heaviness", "Matches the shampoo for a complete system", "Affordable for the quality"],
        ["Can be heavy for fine, wavy hair", "Some prefer even more slip"],
        "All curl types needing hydration and easy detangling")}

    <h2>Step 3: Leave-In Conditioner — Layer the Moisture</h2>
    <p>A leave-in conditioner adds an extra moisture layer that stays with your curls throughout the day. Apply it to soaking wet hair after the shower for maximum absorption. This step is especially crucial if you live in a dry climate or have high-porosity hair that loses moisture quickly.</p>
    {product_card("Kinky-Curly Knot Today Leave-In Conditioner/Detangler", "Kinky-Curly", "B003PC8UBU", "12.99", 4.5,
        "This organic, naturally derived leave-in has been a curly community staple for years. The marshmallow root extract provides incredible slip for detangling, while organic aloe vera and green tea provide lightweight moisture. It doesn't weigh curls down or leave them crunchy — just soft, defined, and manageable. A little goes a long way.",
        ["Organic, naturally derived formula", "Incredible slip for detangling", "Lightweight — won't weigh curls down", "Works across all curl types"],
        ["Thinner consistency than some prefer", "Scent is subtle/herbal"],
        "All curl types, especially those who need extra detangling help")}

    <h2>Step 4: Styling Gel — Define and Hold</h2>
    <p>Gel is the key to defined, frizz-free curls that last for days. The 'curly girl method' secret is applying gel to soaking wet hair, then allowing it to dry completely into a 'cast' — a stiff, crunchy outer layer that you scrunch out once dry to reveal soft, defined curls underneath. This technique is called 'scrunch out the crunch' and it's a game-changer.</p>
    {product_card("Eco Style Professional Styling Gel - Olive Oil", "Eco Style", "B004BME3AO", "4.99", 4.5,
        "At under $5 for a huge tub, this gel is a curly girl cult classic. The olive oil formula provides strong hold with added moisture, and it forms the perfect gel cast for scrunch-out-the-crunch styling. It's alcohol-free, flake-free, and works on everything from wavy to coily hair. The value is unbeatable — this tub will last months.",
        ["Under $5 for a huge tub", "Strong, frizz-fighting hold", "Olive oil adds moisture", "No flaking, no alcohol"],
        ["Very firm hold (some prefer lighter)", "Can feel heavy if over-applied"],
        "Anyone wanting defined, frizz-free curls on a budget")}

    <h2>Step 5: Deep Conditioner — Weekly Intensive Treatment</h2>
    <p>Once a week (or every two weeks for fine hair), a deep conditioning mask provides the intensive moisture treatment that daily products can't match. Apply to damp hair after shampooing, leave on for 10-30 minutes (or under a heat cap for deeper penetration), then rinse and continue with your regular styling routine.</p>
    {product_card("SheaMoisture Manuka Honey & Mafura Oil Intensive Hydration Hair Masque", "SheaMoisture", "B00SYELKOE", "11.99", 4.5,
        "This deep conditioner is like a tall drink of water for thirsty curls. The manuka honey and mafura oil combination delivers intense moisture that lasts for days after application. It softens, strengthens, and revives even the driest, most damaged curls. I use it every wash day under a heat cap for 20 minutes, and the difference in my curl definition and softness is night and day.",
        ["Manuka honey for intense hydration", "Mafura oil strengthens and softens", "Noticeable difference after one use", "Affordable for a deep treatment"],
        ["Very thick — can be hard to distribute evenly", "Heavy for fine or wavy hair"],
        "Dry, damaged, or color-treated curls needing intensive weekly moisture")}

    <h2>Essential Tool: Microfiber Towel — Stop Frizz Before It Starts</h2>
    <p>Regular terry cloth towels are one of the biggest causes of frizz. The rough fibers catch on the hair cuticle, roughing it up and creating frizz. A microfiber towel or cotton t-shirt gently absorbs excess water without disrupting your curl pattern. This one swap alone can dramatically reduce frizz.</p>
    {product_card("Aquis Original Hair Towel", "Aquis", "B01MSEZ3T7", "16.00", 4.5,
        "Aquis pioneered the microfiber hair towel category, and this original version remains the best. The proprietary Aquitex fabric absorbs water 50% faster than cotton while being incredibly gentle on curls. Use it to gently scrunch out excess water after the shower, then apply your styling products. Your curls will thank you with less frizz and more definition.",
        ["Proprietary Aquitex microfiber fabric", "Absorbs 50% faster than cotton", "Ultra-gentle on curls", "Reduces drying time significantly"],
        ["More expensive than drugstore options", "Requires proper care to maintain softness"],
        "Every curly person — this is the easiest upgrade you can make")}

    <h2>Essential Tool: Diffuser — Dry Without Disturbing</h2>
    <p>Air drying works, but it can take hours for thick curly hair, and gravity can stretch out curls as they dry. A diffuser attachment on your blow dryer circulates warm air around your curls without blasting them directly, preserving your curl pattern while cutting drying time in half. The key technique: cup your curls in the diffuser bowl and bring the dryer to your head, not the other way around.</p>
    {product_card("DevaCurl DevaFuser", "DevaCurl", "B079VK3BWF", "49.99", 4.5,
        "This uniquely designed diffuser has a hand-shaped bowl that cradles curls while drying, distributing airflow evenly without disrupting definition. The 360-degree airflow means less frizz and more volume compared to traditional flat diffusers. It's a universal fit for most blow dryers and cuts drying time by up to 50%.",
        ["Hand-shaped design cradles curls", "360-degree even airflow", "Universal fit for most dryers", "Cuts drying time by 50%"],
        ["Bulky size", "Premium price for a diffuser attachment"],
        "Anyone with thick or long curly hair who can't wait for air drying")}

    <h2>Wash Day Routine Summary</h2>
    <ol>
      <li>Wet hair thoroughly in the shower</li>
      <li>{alink("B0038TVH3Y", "SheaMoisture Shampoo")} — Focus on scalp only, let suds rinse through lengths</li>
      <li>{alink("B0038TYESG", "SheaMoisture Conditioner")} — Apply generously, detangle with fingers, leave 3-5 minutes, rinse with cool water</li>
      <li>Optional: {alink("B00SYELKOE", "SheaMoisture Deep Conditioner")} instead of regular conditioner once a week</li>
      <li>Gently scrunch out excess water with {alink("B01MSEZ3T7", "Aquis Towel")}</li>
      <li>{alink("B003PC8UBU", "Kinky-Curly Knot Today")} — Apply to soaking wet hair, scrunch in</li>
      <li>{alink("B004BME3AO", "Eco Style Gel")} — Apply generously over leave-in, scrunch in</li>
      <li>Dry with {alink("B079VK3BWF", "DevaFuser")} on medium heat, or air dry completely</li>
      <li>Once 100% dry, scrunch out the crunch — soft, defined curls revealed</li>
    </ol>

    <h2>Final Verdict</h2>
    <p>Building a curly routine doesn't have to be overwhelming or expensive. Start with the basics — {alink("B0038TVH3Y", "sulfate-free shampoo")}, {alink("B0038TYESG", "moisturizing conditioner")}, {alink("B003PC8UBU", "leave-in")}, and {alink("B004BME3AO", "gel")} — and master the scrunch-out-the-crunch technique. That alone will transform your curls. Add the {alink("B01MSEZ3T7", "microfiber towel")} next — it's the single easiest upgrade. The total cost for all 7 products? About $115. Your curls have been waiting for this.</p>
"""
    faqs = faq_section([
        ("How often should I wash curly hair?",
         "Most curlies wash 1-3 times per week. Very dry or coily hair may only need once a week; wavy or oily scalps may need 2-3 times. Listen to your scalp — it should feel clean but not tight or itchy."),
        ("What is the 'curly girl method'?",
         "The Curly Girl Method (CGM) is a haircare approach that avoids sulfates, silicones, and heat styling. While the strict version works for many, most people find a modified version — sulfate-free shampoo occasionally, water-soluble silicones allowed — is more practical and sustainable."),
        ("Can I brush curly hair?",
         "Never brush dry curly hair — it separates the curl clumps and creates frizz. Detangle only when wet and coated with conditioner, using fingers or a wide-tooth comb, starting from the ends and working up."),
        ("Why are my curls frizzy even with product?",
         "Common causes include: not applying products to wet enough hair, touching hair while drying, using a terry cloth towel, under-conditioning, or not using enough gel for hold. Try applying products to soaking wet hair and not touching until completely dry."),
    ])
    write_post("routines-guides", "curly-hair-routine-beginners.html", h + body + faqs + footer())

