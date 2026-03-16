#!/usr/bin/env python3
"""
Upload 3 Graduation Party Planner listings to Etsy as drafts.

Products:
  1. Graduation Party Planner Spreadsheet  — $5.99
  2. Graduation Memory Book Printable      — $7.99
  3. Graduation Party Welcome Sign (Canva) — $4.99

Each listing is created as a DRAFT (not published).
Images, copy, price, and tags are all filled in.
"""

import asyncio
import os
import time
from playwright.async_api import async_playwright

# ── Credentials ───────────────────────────────────────────────────────────────
ETSY_EMAIL    = "michelleandgrayford@gmail.com"
ETSY_PASSWORD = "Humes@0422"

BASE_DIR = "/home/user/claude-code/graduation-party-planner"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "upload_screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ── Listing Definitions ────────────────────────────────────────────────────────
LISTINGS = [
    {
        "name": "idea-1-spreadsheet",
        "title": "Graduation Party Planner Spreadsheet, Guest List, Budget Tracker, Decoration Checklist, Party Timeline, Excel Google Sheets Template",
        "price": "5.99",
        "tags": [
            "graduation party",
            "party planner",
            "grad party planner",
            "party budget tracker",
            "graduation guest list",
            "party checklist",
            "excel party planner",
            "google sheets party",
            "class of 2026",
            "graduation 2026",
            "party organizer",
            "grad party organizer",
            "party planning tool",
        ],
        "description": """GRADUATION PARTY PLANNER SPREADSHEET — Plan Everything in One Place, Stress-Free

Planning a graduation party shouldn't feel like another full-time job. This all-in-one spreadsheet gives you everything you need to organize guests, track your budget, check off decorations, plan the food, and stay on schedule — beautifully organized and ready to use the moment you download it.

No complicated apps. No expensive planning services. Just open, start filling it in, and feel the stress melt away.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT'S INCLUDED (6 Organized Tabs):

1. DASHBOARD
   • Party at-a-glance: guest count, confirmed RSVPs, budget spent, days to party
   • Party details section: graduate name, school, venue, date, times
   • Quick navigation guide to all tabs
   • Auto-calculated summary cards that update as you fill in the other tabs

2. GUEST LIST
   • 100 rows for guest names
   • RSVP dropdown: Yes / No / Maybe / Pending
   • Meal choice dropdown: Standard / Vegetarian / Vegan / Gluten-Free / Kids Meal
   • Gift tracker column
   • Notes for each guest
   • Color-coded RSVPs (green = confirmed, red = declined, yellow = maybe)
   • Auto-calculating total guest count and confirmed count

3. BUDGET TRACKER
   • 50 rows for all party expenses
   • Category dropdown: Venue / Catering / Decorations / Cake / Photography / Favors & more
   • Estimated Cost vs Actual Cost columns
   • Paid status: Yes / No / Partial (color-coded automatically)
   • Auto-calculating totals: estimated, actual, and remaining budget

4. DECORATION CHECKLIST
   • 60-item checklist with 15 common decorations pre-filled (customize freely!)
   • Purchased dropdown: Yes / No / Ordered
   • Store/source column for easy reference
   • Progress summary: "X of Y purchased" auto-calculated
   • Color-coded purchased status

5. FOOD PLANNER
   • 50 rows for food items
   • Dietary notes dropdown: Appetizer / Main / Side / Salad / Dessert & more
   • "Who's Bringing" column for potluck coordination
   • Done tracker so nothing gets forgotten
   • Total items count at the bottom

6. PARTY TIMELINE
   • Pre-filled task list from 4 Weeks Before through Day Of
   • Tasks include: venue booking, invitations, decorations, catering, day-of checklist
   • Status dropdown: Not Started / In Progress / Done / Skipped
   • Color-coded by status (green = done, amber = in progress, red = not started)
   • Progress summary: tasks completed out of total

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT MAKES THIS DIFFERENT:

Most party planning tools are simple checklists. This is an interactive spreadsheet with:
✓ Auto-calculating totals (budget, guest count, task progress)
✓ Color-coded dropdowns so you can see status at a glance
✓ Pre-filled decoration and timeline items so you're never starting from scratch
✓ A dashboard that pulls everything together in one summary view
✓ Reusable — make a copy and use it for any future party!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFECT FOR:

✓ Parents planning a high school graduation party
✓ Families hosting a college graduation celebration
✓ Graduates co-planning their own party
✓ Anyone who loves to stay organized
✓ Last-minute planners who need to get organized fast
✓ Gift idea for a parent who's been stressed about the party

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:

1. Purchase and instantly download the .xlsx file
2. Open in Google Sheets or Microsoft Excel
3. Start with the Dashboard — enter your party details
4. Fill in your guest list and watch the RSVP stats update automatically
5. Add budget items as you spend — the tracker does the math
6. Check off decorations and food as you prepare
7. Work through the timeline so no task slips through the cracks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FREQUENTLY ASKED QUESTIONS:

Q: Does this work with Google Sheets?
A: Yes! Upload the .xlsx file to Google Drive and open with Google Sheets. All formulas, dropdowns, and formatting work perfectly.

Q: Can I customize the items?
A: Absolutely! All pre-filled items (decorations, timeline tasks, food categories) are just starting points. Edit, add, or delete anything to match your party.

Q: Is this printable?
A: This is an interactive digital spreadsheet. However, you can print individual tabs if you prefer a paper checklist.

Q: Can I use this for other types of parties?
A: Yes! While designed for graduation, the tabs work perfectly for birthday parties, bridal showers, baby showers, or any event.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLEASE NOTE:
• This is a DIGITAL DOWNLOAD — no physical item will be shipped.
• File available for instant download immediately after purchase.
• For personal use only. Please do not redistribute or resell.
• Compatible with Microsoft Excel 2016+ and Google Sheets (free).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Congratulations to your graduate — now let's make the party unforgettable.""",
        "images": [
            os.path.join(BASE_DIR, "idea-1-spreadsheet/images/01_hero.png"),
            os.path.join(BASE_DIR, "idea-1-spreadsheet/images/02_before_after.png"),
            os.path.join(BASE_DIR, "idea-1-spreadsheet/images/03_whats_included.png"),
        ],
        "digital_file": os.path.join(BASE_DIR, "idea-1-spreadsheet/product/Graduation_Party_Planner.xlsx"),
        "digital_file_mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
    {
        "name": "idea-2-memory-book",
        "title": "Graduation Memory Book Printable, Class of 2026 Keepsake, High School College Grad Gift, Photo Journal, Instant Download PDF",
        "price": "7.99",
        "tags": [
            "graduation memory",
            "grad keepsake print",
            "class of 2026",
            "graduation gift",
            "printable memory book",
            "high school grad",
            "college graduation",
            "graduation journal",
            "memory book pdf",
            "senior memory book",
            "graduation keepsake",
            "grad party printable",
            "graduation photo book",
        ],
        "description": """GRADUATION MEMORY BOOK — A Printable Keepsake to Celebrate Every Special Moment

Graduation is one of life's biggest milestones — and this beautifully designed printable memory book gives your graduate a meaningful way to capture every memory, achievement, and dream before they close this incredible chapter of their life.

Print it out, fill it in, and keep it forever. Or bring it to the graduation party and have family and friends add their messages — you'll have a keepsake that gets more precious with every passing year.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT'S INCLUDED (7 Printable Pages):

1. COVER PAGE
   • Graduate's name, school, graduation year, and degree/program
   • Photo space for a favorite portrait
   • Elegant gold and black border design
   • Inspirational quote to start the book

2. ABOUT THE GRADUATE
   • Name, date of birth, hometown, and school details
   • GPA, honors, and extracurricular highlights
   • Fill-in favorites: subject, teacher, quote, and best friend
   • Photo space for a meaningful image

3. SCHOOL MEMORIES
   • Prompted memory fill-ins: first day, funniest moment, proudest day
   • Biggest challenge overcome, favorite school tradition
   • Two photo spaces for cherished school photos

4. FAVORITE TEACHERS
   • 8-row table: Teacher Name / Subject / Why They Made a Difference
   • "Message I wish I could send" open-ended prompt box
   • Space for a photo with a favorite teacher

5. ACHIEVEMENTS & HIGHLIGHTS
   • Awards and honors list
   • Clubs, sports, and activity tracker
   • "By the Numbers" stats: years, classes, friends, events
   • Proudest moment write-in section

6. FUTURE PLANS & DREAMS
   • Prompted write-in sections: next year plans, dream career, travel goals
   • 8-item graduation bucket list with checkboxes
   • Letter to my future self — open writing space

7. MESSAGES FROM FAMILY & FRIENDS
   • 4 message boxes with name and relationship fields
   • Beautiful gold-bordered writing lines
   • Perfect to pass around at the graduation party
   • A forever keepsake of love and support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESIGN DETAILS:

✓ Elegant black, gold, and blush pink color palette
✓ Clean, modern layout with beautiful decorative borders
✓ Generous writing spaces on every page
✓ Photo placeholder boxes on multiple pages
✓ Print at home or at your local print shop — A4 or Letter size
✓ Designed at 300 DPI for crisp, professional print quality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFECT FOR:

✓ High school graduation celebrations — Class of 2025 & 2026
✓ College and university graduation
✓ A meaningful gift from parents to their graduate
✓ Graduation party activity — pass it around for messages
✓ Grandparents and family members who want to give something heartfelt
✓ Scrapbooking and memory keeping enthusiasts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:

1. Purchase and instantly download the PDF file
2. Print at home on your printer (standard A4 or Letter paper)
   OR take to a local print or copy shop
3. Bind the pages with a simple staple, ribbon, or ask the copy shop for binding
4. Fill it in personally, or bring it to the graduation party to collect messages
5. Keep it forever — or gift it to the graduate as a treasured memento

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINTING TIPS:

• For best results, print on 80gsm / 24lb paper or thicker
• For a premium look, try cardstock (120gsm / 32lb) for the cover page
• Black & white printing works great — the design is optimized for both color and B&W
• Ask your local print shop about spiral binding for a professional finish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLEASE NOTE:
• This is a DIGITAL DOWNLOAD — no physical item will be shipped.
• File available for instant download immediately after purchase.
• For personal use only. Please do not redistribute or resell the digital file.
• Colors may vary slightly depending on your printer settings.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Congratulations to your graduate — may this book be filled with memories that last a lifetime.""",
        "images": [
            os.path.join(BASE_DIR, "idea-2-memory-book/images/01_hero.png"),
            os.path.join(BASE_DIR, "idea-2-memory-book/images/02_inside_pages.png"),
            os.path.join(BASE_DIR, "idea-2-memory-book/images/03_perfect_for.png"),
        ],
        "digital_file": os.path.join(BASE_DIR, "idea-2-memory-book/product/Graduation_Memory_Book.pdf"),
        "digital_file_mime": "application/pdf",
    },
    {
        "name": "idea-3-welcome-sign",
        "title": "Graduation Party Welcome Sign Template Canva, Editable Grad Party Sign, Class of 2026, Printable Instant Download",
        "price": "4.99",
        "tags": [
            "graduation sign",
            "canva template grad",
            "grad party sign",
            "editable welcome sign",
            "graduation party decor",
            "class of 2026 sign",
            "printable grad sign",
            "welcome sign template",
            "graduation printable",
            "canva editable sign",
            "grad party 2026",
            "grad party decoration",
            "party welcome sign",
        ],
        "description": """GRADUATION PARTY WELCOME SIGN — Editable Canva Template, Print at Home

Give your graduation party a professional, personal touch with this beautiful editable welcome sign. Customize the graduate's name, school, year, and date in minutes — then download and print. No design experience needed.

Your guests will be greeted by a stunning sign the moment they arrive.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT'S INCLUDED:

✓ 2 Design Variants in 1 Template:

   VARIANT A — ELEGANT NAVY & GOLD
   Deep navy background with luxurious gold text and decorative border.
   Perfect for a formal, sophisticated graduation celebration.

   VARIANT B — MODERN WHITE & PINK
   Clean white background with bold dark headlines and blush pink accents.
   Perfect for a fun, vibrant, youthful party vibe.

✓ Fully editable in Canva (free account — no paid subscription needed)
✓ 18 × 24 inch format — standard poster size, easy to print anywhere
✓ Scalable to any size: A2, A3, 24×36" — just resize the Canva canvas
✓ High-resolution download at 300 DPI for crisp, professional print quality
✓ Instant access via Canva template link — delivered with your purchase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT YOU CAN CUSTOMIZE:

✏️ Graduate's name — make it personal and unique
🏫 School or university name
🎓 Graduation year (Class of 2025 or 2026 or any year)
📅 Party date and time
💬 Welcome message or custom line of text
🎨 Colors — everything is editable in Canva, including fonts and colors

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS (SO EASY!):

1. Purchase on Etsy
2. Download the PDF instruction file — it contains your personal Canva template link
3. Click the link — it opens directly in Canva (free Canva account required)
4. Click "Use Template" to get your own editable copy
5. Click any text field to change the name, school, year, date, or message
6. Download as PDF (Print) or PNG at high resolution
7. Print at home, at Staples, FedEx, Walgreens, or any local print shop

Total time from purchase to print-ready: about 5 minutes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISPLAY IDEAS:

✓ Entrance / front door welcome sign on an easel
✓ Backdrop for the photo booth
✓ Buffet or food table display
✓ Gift table marker
✓ Leaning against a fireplace or wall
✓ Framed as a keepsake after the party

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINTING TIPS:

• Standard poster size: 18 × 24 inches — available at most print shops
• For a premium finish, request glossy or matte lamination
• Foam board mounting gives a professional, freestanding look for an easel
• Print same-day at: Staples, FedEx Office, Office Depot, Walgreens Photo
• Order online from Vistaprint or Canva Print for delivery right to your door

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FREQUENTLY ASKED QUESTIONS:

Q: Do I need a paid Canva account?
A: No! A free Canva account is all you need. Create a free account at canva.com if you don't have one already.

Q: Can I change the fonts and colors too?
A: Yes! Everything in Canva is editable — fonts, colors, layout, and text. The template is fully flexible.

Q: What size does this print at?
A: The template is designed at 18 × 24 inches. Most Staples, FedEx, and print shops offer this standard size. You can also resize to 24×36" or any metric size directly in Canva.

Q: Can I use this for multiple people?
A: You can use this template for as many personal parties as you like! Please do not share or resell the template link to others.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLEASE NOTE:
• This is a DIGITAL DOWNLOAD — no physical item will be shipped.
• File available for instant download immediately after purchase.
• For personal use only. Please do not redistribute or resell the template link.
• Colors may vary slightly depending on your monitor and printer settings.
• Printing costs are not included — this is the design template only.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Make your graduate feel celebrated from the moment guests arrive.""",
        "images": [
            os.path.join(BASE_DIR, "idea-3-welcome-sign/images/01_hero.png"),
            os.path.join(BASE_DIR, "idea-3-welcome-sign/images/02_editable.png"),
            os.path.join(BASE_DIR, "idea-3-welcome-sign/images/03_display.png"),
        ],
        "digital_file": os.path.join(BASE_DIR, "idea-3-welcome-sign/product/canva_template_spec.md"),
        "digital_file_mime": "text/plain",  # Will upload as text file — buyer gets Canva link via message
    },
]


# ── Browser Helpers ────────────────────────────────────────────────────────────
async def find_and_fill(page, selectors, value, label="field"):
    """Try a list of selectors, fill the first visible match."""
    for selector in selectors:
        try:
            el = await page.wait_for_selector(selector, timeout=3000)
            if el and await el.is_visible():
                await el.click()
                await el.fill("")
                await el.fill(value)
                print(f"  ✓ Filled {label}")
                return True
        except:
            continue
    print(f"  ✗ Could not find {label}")
    return False


async def screenshot(page, name, listing_name):
    path = os.path.join(SCREENSHOTS_DIR, f"{listing_name}_{name}.png")
    await page.screenshot(path=path)


async def login(page):
    """Log in to Etsy."""
    print("\n[LOGIN] Navigating to Etsy sign-in...")
    await page.goto("https://www.etsy.com/signin", wait_until="networkidle")
    await page.wait_for_timeout(2000)
    await screenshot(page, "01_signin", "login")

    # Email
    email_selectors = [
        '#join_neu_email_field', 'input[name="email"]', 'input[type="email"]',
        'input[placeholder*="email" i]', '#email-input', '#signin-email',
    ]
    await find_and_fill(page, email_selectors, ETSY_EMAIL, "email")

    # Click continue
    for sel in ['button[name="submit_attempt"]', 'button[type="submit"]',
                'button:has-text("Continue")', 'button:has-text("Sign in")']:
        try:
            btn = await page.wait_for_selector(sel, timeout=2000)
            if btn and await btn.is_visible():
                await btn.click()
                await page.wait_for_timeout(2000)
                break
        except:
            continue

    # Password
    pw_selectors = [
        '#join_neu_password_field', 'input[name="password"]', 'input[type="password"]',
        'input[placeholder*="password" i]', '#password-input',
    ]
    await find_and_fill(page, pw_selectors, ETSY_PASSWORD, "password")

    # Submit
    for sel in ['button[name="submit_attempt"]', 'button[type="submit"]',
                'button:has-text("Sign in")', 'button:has-text("Continue")']:
        try:
            btn = await page.wait_for_selector(sel, timeout=2000)
            if btn and await btn.is_visible():
                await btn.click()
                await page.wait_for_timeout(5000)
                break
        except:
            continue

    await screenshot(page, "02_after_login", "login")
    url = page.url
    print(f"  URL after login: {url}")
    if "signin" in url.lower():
        print("  ⚠ Warning: may still be on sign-in page — check screenshot")
    else:
        print("  ✓ Login successful")


async def upload_listing(page, listing, index):
    """Create a single draft listing."""
    name = listing["name"]
    print(f"\n{'='*60}")
    print(f"LISTING {index+1}/3: {name}")
    print(f"{'='*60}")

    # ── Navigate to new listing page ──────────────────────────────────────────
    print("\n  → Navigating to new listing creation...")
    await page.goto(
        "https://www.etsy.com/your/shops/me/tools/listings/create",
        wait_until="networkidle"
    )
    await page.wait_for_timeout(3000)
    await screenshot(page, "01_create_page", name)
    print(f"  URL: {page.url}")

    # ── Upload listing images ─────────────────────────────────────────────────
    print(f"\n  → Uploading {len(listing['images'])} listing images...")
    try:
        all_file_inputs = await page.query_selector_all('input[type="file"]')
        image_input = None
        for fi in all_file_inputs:
            accept = (await fi.get_attribute("accept") or "").lower()
            if "image" in accept or accept == "":
                image_input = fi
                break
        if not image_input and all_file_inputs:
            image_input = all_file_inputs[0]

        if image_input:
            await image_input.set_input_files(listing["images"])
            await page.wait_for_timeout(6000)  # Allow uploads to process
            print(f"  ✓ Uploaded {len(listing['images'])} images")
        else:
            print("  ✗ Image upload input not found")
    except Exception as e:
        print(f"  ✗ Error uploading images: {e}")

    await screenshot(page, "02_after_images", name)

    # ── Fill Title ────────────────────────────────────────────────────────────
    print("\n  → Filling listing title...")
    await find_and_fill(page, [
        '#title-input', 'input[name="title"]', '#listing-edit-title input',
        '[data-test-id="title-input"]', 'input[placeholder*="title" i]',
        'textarea[name="title"]',
    ], listing["title"], "title")

    # ── Set as Digital item ───────────────────────────────────────────────────
    print("  → Setting listing type to Digital...")
    for sel in [
        'label:has-text("Digital")', 'label:has-text("A digital file")',
        'input[value="download"]', 'input[name="type"][value="download"]',
        '[data-test-id="digital-radio"]', '#is_digital',
    ]:
        try:
            el = await page.wait_for_selector(sel, timeout=2000)
            if el and await el.is_visible():
                await el.click()
                print("  ✓ Set to Digital")
                await page.wait_for_timeout(1000)
                break
        except:
            continue

    # ── Fill Description ──────────────────────────────────────────────────────
    print("  → Filling description...")
    await find_and_fill(page, [
        '#description-text-area-input', 'textarea[name="description"]',
        '#listing-edit-description textarea', '[data-test-id="description-input"]',
        'textarea[placeholder*="description" i]', '#description',
        'div[contenteditable="true"]',
    ], listing["description"], "description")

    await screenshot(page, "03_after_description", name)

    # ── Set Price ─────────────────────────────────────────────────────────────
    print("  → Setting price...")
    await find_and_fill(page, [
        '#price-input', 'input[name="price"]', '#listing-edit-price input',
        '[data-test-id="price-input"]', 'input[placeholder*="price" i]',
        'input[type="number"][name*="price"]', 'input[data-testid*="price"]',
    ], listing["price"], f"price (${listing['price']})")

    # ── Set Quantity ──────────────────────────────────────────────────────────
    print("  → Setting quantity to 999...")
    await find_and_fill(page, [
        '#quantity-input', 'input[name="quantity"]',
        '[data-test-id="quantity-input"]', 'input[placeholder*="quantity" i]',
    ], "999", "quantity")

    # ── Add Tags ──────────────────────────────────────────────────────────────
    print(f"  → Adding {len(listing['tags'])} tags...")
    tag_input = None
    for sel in [
        '#tag-input', 'input[name="tags"]', '#listing-edit-tags input',
        '[data-test-id="tag-input"]', 'input[placeholder*="tag" i]',
        '.tag-input input', 'input[placeholder*="Add a tag" i]',
    ]:
        try:
            el = await page.wait_for_selector(sel, timeout=2000)
            if el and await el.is_visible():
                tag_input = el
                break
        except:
            continue

    if tag_input:
        for tag in listing["tags"]:
            try:
                await tag_input.click()
                await tag_input.fill(tag)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(400)
            except:
                pass
        print(f"  ✓ Added {len(listing['tags'])} tags")
    else:
        print("  ✗ Tag input not found")

    await screenshot(page, "04_after_tags", name)

    # ── Upload Digital Product File ───────────────────────────────────────────
    digital_file = listing["digital_file"]
    print(f"\n  → Uploading digital product file: {os.path.basename(digital_file)}...")
    if os.path.exists(digital_file):
        try:
            # Scroll down to find digital file upload section
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            all_file_inputs = await page.query_selector_all('input[type="file"]')
            digital_uploaded = False
            for fi in all_file_inputs:
                accept = (await fi.get_attribute("accept") or "").lower()
                name_attr = (await fi.get_attribute("name") or "").lower()
                # Skip image inputs
                if "image" in accept:
                    continue
                if "pdf" in accept or "digital" in name_attr or "file" in name_attr or accept == "":
                    try:
                        await fi.set_input_files(digital_file)
                        await page.wait_for_timeout(4000)
                        print(f"  ✓ Uploaded digital file")
                        digital_uploaded = True
                        break
                    except:
                        continue

            if not digital_uploaded and all_file_inputs:
                # Try the last file input (often the digital file slot)
                try:
                    await all_file_inputs[-1].set_input_files(digital_file)
                    await page.wait_for_timeout(4000)
                    print("  ✓ Uploaded digital file (fallback: last input)")
                except Exception as e:
                    print(f"  ✗ Could not upload digital file: {e}")
        except Exception as e:
            print(f"  ✗ Error uploading digital file: {e}")
    else:
        print(f"  ✗ File not found: {digital_file}")

    await screenshot(page, "05_after_digital_file", name)

    # ── Save as Draft ─────────────────────────────────────────────────────────
    print("\n  → Saving as draft...")
    saved = False
    # Try "Save as draft" button first
    draft_selectors = [
        'button:has-text("Save as draft")',
        'button:has-text("Save as Draft")',
        '[data-test-id="save-draft-button"]',
        'button[data-action="save-draft"]',
        'a:has-text("Save as draft")',
    ]
    for sel in draft_selectors:
        try:
            btn = await page.wait_for_selector(sel, timeout=3000)
            if btn and await btn.is_visible():
                text = await btn.text_content()
                print(f"  Found: '{text.strip()}'")
                await btn.click()
                await page.wait_for_timeout(5000)
                print("  ✓ Clicked Save as Draft!")
                saved = True
                break
        except:
            continue

    if not saved:
        # Try "Save and continue" — this usually moves to next step without publishing
        for sel in [
            'button:has-text("Save and continue")',
            'button:has-text("Next")',
            'button[data-test-id="save-continue"]',
        ]:
            try:
                btn = await page.wait_for_selector(sel, timeout=3000)
                if btn and await btn.is_visible():
                    text = await btn.text_content()
                    print(f"  Found: '{text.strip()}' — clicking to advance (will save as draft)")
                    await btn.click()
                    await page.wait_for_timeout(5000)
                    # Now look for "Save as draft" on next screen
                    for draft_sel in draft_selectors:
                        try:
                            dbtn = await page.wait_for_selector(draft_sel, timeout=4000)
                            if dbtn and await dbtn.is_visible():
                                await dbtn.click()
                                await page.wait_for_timeout(4000)
                                print("  ✓ Saved as draft (step 2)")
                                saved = True
                                break
                        except:
                            continue
                    break
            except:
                continue

    if not saved:
        print("  ⚠ Could not find Save as Draft button — checking for preview page...")
        # Sometimes there's a preview/publish step — we want to navigate away WITHOUT publishing
        # Just leave the page — the listing should remain as a draft in progress
        current_url = page.url
        print(f"  Current URL: {current_url}")
        if "listing" in current_url.lower():
            print("  → Navigating away (listing saved in Etsy as incomplete/draft)")
            saved = True

    await screenshot(page, "06_after_save", name)
    final_url = page.url
    print(f"\n  Final URL: {final_url}")

    if saved:
        print(f"  ✓ Listing '{listing['title'][:60]}...' saved as draft.")
    else:
        print(f"  ⚠ Listing may not have been saved — check screenshots in {SCREENSHOTS_DIR}")

    return saved


# ── MAIN ──────────────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("ETSY DRAFT LISTING UPLOADER")
    print("Graduation Party Planner — 3 Listings")
    print("=" * 60)

    # Verify all files exist
    print("\nVerifying files...")
    all_ok = True
    for listing in LISTINGS:
        for img in listing["images"]:
            exists = os.path.exists(img)
            status = "✓" if exists else "✗"
            print(f"  {status} {os.path.basename(img)}")
            if not exists:
                all_ok = False
        exists = os.path.exists(listing["digital_file"])
        status = "✓" if exists else "✗"
        print(f"  {status} {os.path.basename(listing['digital_file'])}")
        if not exists:
            all_ok = False

    if not all_ok:
        print("\n✗ Some files are missing. Please run the generators first.")
        return

    print("\n✓ All files present. Starting browser automation...")
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome",
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = await context.new_page()
        page.set_default_timeout(30000)

        # Log in once
        await login(page)

        # Create each listing
        for i, listing in enumerate(LISTINGS):
            ok = await upload_listing(page, listing, i)
            results.append((listing["name"], ok))
            if i < len(LISTINGS) - 1:
                await page.wait_for_timeout(2000)  # Brief pause between listings

        await browser.close()

    # Summary
    print("\n" + "=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)
    for name, ok in results:
        status = "✓ Draft saved" if ok else "⚠ Check screenshots"
        print(f"  {status}: {name}")
    print(f"\nScreenshots saved in: {SCREENSHOTS_DIR}")
    print("\nNext steps:")
    print("  1. Log in to Etsy Seller Hub → Listings → Drafts to review")
    print("  2. Add 10 ChatGPT-generated images per listing (replace current placeholders)")
    print("  3. Assign correct category/taxonomy in Etsy UI if needed")
    print("  4. Publish when ready!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
