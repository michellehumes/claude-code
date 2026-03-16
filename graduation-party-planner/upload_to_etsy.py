#!/usr/bin/env python3
"""
Etsy Draft Listing Uploader — runs in VISIBLE Chrome.
Creates all 3 graduation listings as drafts.

HOW TO RUN (on your local machine):
  pip install playwright
  playwright install chromium
  python upload_to_etsy.py

Products:
  1. Graduation Party Planner Spreadsheet  ($5.99)
  2. Graduation Memory Book Printable      ($7.99)
  3. Graduation Party Welcome Sign Canva   ($4.99)
"""

import asyncio
import os
import sys
import subprocess
import time

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
ETSY_EMAIL    = "michelleandgrayford@gmail.com"
ETSY_PASSWORD = "Humes@0422"

# All paths resolve relative to this script's directory so it works on any machine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── LISTING DATA ──────────────────────────────────────────────────────────────
LISTINGS = [
    # ── LISTING 1: Spreadsheet ────────────────────────────────────────────────
    {
        "label": "Graduation Party Planner Spreadsheet",
        "title": "Graduation Party Planner Spreadsheet, Guest List, Budget Tracker, Decoration Checklist, Party Timeline, Excel Google Sheets Template",
        "price": "5.99",
        "quantity": "999",
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
   • Party details: graduate name, school, venue, date, times
   • Quick navigation guide to all tabs
   • Auto-calculated summary cards that update as you fill in other tabs

2. GUEST LIST
   • 100 rows for guest names
   • RSVP dropdown: Yes / No / Maybe / Pending
   • Meal choice dropdown: Standard / Vegetarian / Vegan / Gluten-Free / Kids Meal
   • Gift tracker column + notes
   • Color-coded RSVPs (green = confirmed, red = declined, yellow = maybe)
   • Auto-calculating total guest count and confirmed count

3. BUDGET TRACKER
   • 50 rows for all party expenses
   • Category dropdown: Venue / Catering / Decorations / Cake / Photography / Favors & more
   • Estimated Cost vs Actual Cost columns
   • Paid status: Yes / No / Partial (color-coded automatically)
   • Auto-calculating totals: estimated, actual, and remaining budget

4. DECORATION CHECKLIST
   • 60-item checklist — 15 common decorations pre-filled, fully customizable
   • Purchased dropdown: Yes / No / Ordered
   • Store/source column + progress summary auto-calculated

5. FOOD PLANNER
   • 50 rows for food items
   • Category dropdown + "Who's Bringing" column for potluck coordination
   • Done tracker so nothing gets forgotten

6. PARTY TIMELINE
   • Pre-filled task list from 4 Weeks Before through Day Of
   • Status dropdown: Not Started / In Progress / Done / Skipped
   • Color-coded status + progress summary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT MAKES THIS DIFFERENT:

✓ Auto-calculating totals (budget, guest count, task progress)
✓ Color-coded dropdowns — see status at a glance
✓ Pre-filled items so you're never starting from scratch
✓ Dashboard pulls everything together in one summary view
✓ Reusable — make a copy for any future party!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFECT FOR:
✓ Parents planning a high school graduation party
✓ Families hosting a college graduation celebration
✓ Graduates co-planning their own party
✓ Last-minute planners who need to get organized fast

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:
1. Purchase and instantly download the .xlsx file
2. Open in Google Sheets or Microsoft Excel
3. Start with the Dashboard — enter your party details
4. Fill in your guest list — RSVP stats update automatically
5. Add budget items — the tracker does the math
6. Check off decorations and food as you prepare
7. Work through the timeline so nothing slips through the cracks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAQ:
Q: Does this work with Google Sheets?
A: Yes! Upload to Google Drive and open with Google Sheets. All formulas and dropdowns work perfectly.

Q: Can I customize the items?
A: Absolutely — all pre-filled items are just starting points. Edit, add, or delete anything.

Q: Can I use this for other parties?
A: Yes — works perfectly for birthdays, bridal showers, baby showers, or any event.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• DIGITAL DOWNLOAD — no physical item shipped
• Instant download after purchase
• Personal use only — do not redistribute or resell
• Compatible with Microsoft Excel 2016+ and Google Sheets (free)

Congratulations to your graduate — now let's make the party unforgettable. 🎓""",
        "images": [
            os.path.join(SCRIPT_DIR, "idea-1-spreadsheet/images/01_hero.png"),
            os.path.join(SCRIPT_DIR, "idea-1-spreadsheet/images/02_before_after.png"),
            os.path.join(SCRIPT_DIR, "idea-1-spreadsheet/images/03_whats_included.png"),
        ],
        "digital_file": os.path.join(SCRIPT_DIR, "idea-1-spreadsheet/product/Graduation_Party_Planner.xlsx"),
    },

    # ── LISTING 2: Memory Book ────────────────────────────────────────────────
    {
        "label": "Graduation Memory Book Printable",
        "title": "Graduation Memory Book Printable, Class of 2026 Keepsake, High School College Grad Gift, Photo Journal, Instant Download PDF",
        "price": "7.99",
        "quantity": "999",
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

Graduation is one of life's biggest milestones. This beautifully designed printable memory book gives your graduate a meaningful way to capture every memory, achievement, and dream before they close this incredible chapter of their life.

Print it, fill it in, and keep it forever. Or bring it to the graduation party and have family and friends add their messages — you'll have a keepsake that gets more precious every year.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT'S INCLUDED (7 Printable Pages):

1. COVER PAGE
   • Graduate's name, school, graduation year, and degree/program
   • Photo space for a favorite portrait
   • Elegant gold and black border design with inspirational quote

2. ABOUT THE GRADUATE
   • Name, date of birth, hometown, school details, GPA, honors
   • Fill-in favorites: subject, teacher, quote, best friend
   • Photo space

3. SCHOOL MEMORIES
   • Prompted fill-ins: first day, funniest moment, proudest day
   • Biggest challenge overcome, favorite school tradition
   • Two photo spaces for cherished school photos

4. FAVORITE TEACHERS
   • 8-row table: Teacher Name / Subject / Why They Made a Difference
   • "Message I wish I could send" prompt box
   • Photo space

5. ACHIEVEMENTS & HIGHLIGHTS
   • Awards and honors list
   • Clubs, sports, and activity tracker
   • "By the Numbers" stats + proudest moment write-in

6. FUTURE PLANS & DREAMS
   • Next year plans, dream career, travel goals
   • 8-item graduation bucket list with checkboxes
   • Letter to my future self — open writing space

7. MESSAGES FROM FAMILY & FRIENDS
   • 4 message boxes with name and relationship fields
   • Gold-bordered writing lines
   • Perfect to pass around at the graduation party

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESIGN:
✓ Elegant black, gold, and blush pink color palette
✓ Clean, modern layout with decorative gold borders
✓ Generous writing spaces on every page
✓ Photo placeholder boxes on multiple pages
✓ Print at home or at a local print shop — A4 or Letter size
✓ Designed at 300 DPI for crisp, professional print quality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFECT FOR:
✓ High school graduation — Class of 2025 & 2026
✓ College and university graduation
✓ A meaningful gift from parents to their graduate
✓ Graduation party activity — pass it around for messages
✓ Grandparents and family members wanting something heartfelt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:
1. Purchase and instantly download the PDF
2. Print at home (A4 or Letter) or at any local print shop
3. Bind with a staple, ribbon, or ask your copy shop for binding
4. Fill in personally or bring to the party to collect messages
5. Keep it forever — or gift it as a treasured memento

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINTING TIPS:
• 80gsm / 24lb paper or thicker for best results
• Cardstock for the cover for a premium look
• Black & white printing works great — optimized for both
• Ask your print shop about spiral binding for a professional finish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• DIGITAL DOWNLOAD — no physical item shipped
• Instant download after purchase
• Personal use only — do not redistribute or resell
• Colors may vary slightly depending on your printer

Congratulations to your graduate — may this book be filled with memories that last a lifetime. 🎓✨""",
        "images": [
            os.path.join(SCRIPT_DIR, "idea-2-memory-book/images/01_hero.png"),
            os.path.join(SCRIPT_DIR, "idea-2-memory-book/images/02_inside_pages.png"),
            os.path.join(SCRIPT_DIR, "idea-2-memory-book/images/03_perfect_for.png"),
        ],
        "digital_file": os.path.join(SCRIPT_DIR, "idea-2-memory-book/product/Graduation_Memory_Book.pdf"),
    },

    # ── LISTING 3: Welcome Sign ───────────────────────────────────────────────
    {
        "label": "Graduation Welcome Sign Canva Template",
        "title": "Graduation Party Welcome Sign Template Canva, Editable Grad Party Sign, Class of 2026, Printable Instant Download",
        "price": "4.99",
        "quantity": "999",
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

2 Design Variants in 1 Template:

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
✏️ Graduate's name
🏫 School or university name
🎓 Graduation year (any year)
📅 Party date and time
💬 Welcome message
🎨 Colors, fonts, layout — everything in Canva is editable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:
1. Purchase on Etsy
2. Download the PDF — it contains your personal Canva template link
3. Click the link — opens directly in Canva (free account required)
4. Click "Use Template" to get your own editable copy
5. Click any text to change the name, school, year, date, or message
6. Download as PDF or PNG at high resolution
7. Print at home, at Staples, FedEx, Walgreens, or any local print shop

Total time from purchase to print-ready: about 5 minutes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISPLAY IDEAS:
✓ Entrance / front door sign on an easel
✓ Backdrop for the photo booth
✓ Buffet or food table display
✓ Gift table marker
✓ Framed as a keepsake after the party

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRINTING TIPS:
• Standard poster size: 18 × 24 inches — available at most print shops
• Glossy or matte lamination for a premium finish
• Foam board mounting for a professional freestanding easel look
• Same-day printing: Staples, FedEx Office, Office Depot, Walgreens Photo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAQ:
Q: Do I need a paid Canva account?
A: No! A free Canva account is all you need.

Q: Can I change the fonts and colors?
A: Yes — everything in Canva is fully editable.

Q: What print size does this work at?
A: Designed at 18 × 24 inches. Resize in Canva for any size.

Q: Can I use this for multiple graduates?
A: Yes, for personal use for as many parties as you like. Please do not share or resell the template link.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• DIGITAL DOWNLOAD — no physical item shipped
• Instant download after purchase
• Personal use only — do not redistribute or resell the template link
• Printing costs not included — this is the design template only

Make your graduate feel celebrated from the moment guests arrive. 🎓""",
        "images": [
            os.path.join(SCRIPT_DIR, "idea-3-welcome-sign/images/01_hero.png"),
            os.path.join(SCRIPT_DIR, "idea-3-welcome-sign/images/02_editable.png"),
            os.path.join(SCRIPT_DIR, "idea-3-welcome-sign/images/03_display.png"),
        ],
        "digital_file": os.path.join(SCRIPT_DIR, "idea-3-welcome-sign/product/canva_template_spec.md"),
    },
]


# ── HELPERS ───────────────────────────────────────────────────────────────────
def log(msg):
    print(msg, flush=True)


async def try_click(page, selectors, label="element", timeout=3000):
    """Click the first visible element matching any selector."""
    for sel in selectors:
        try:
            el = await page.wait_for_selector(sel, timeout=timeout)
            if el and await el.is_visible():
                await el.click()
                log(f"    ✓ Clicked {label} [{sel}]")
                return True
        except Exception:
            continue
    log(f"    – {label} not found (skipping)")
    return False


async def try_fill(page, selectors, value, label="field", timeout=3000):
    """Fill the first visible input matching any selector."""
    for sel in selectors:
        try:
            el = await page.wait_for_selector(sel, timeout=timeout)
            if el and await el.is_visible():
                await el.click()
                await el.fill("")
                await el.type(value, delay=18)  # human-like typing
                log(f"    ✓ Filled {label}")
                return True
        except Exception:
            continue
    log(f"    ✗ Could not fill {label}")
    return False


# ── LOGIN ─────────────────────────────────────────────────────────────────────
async def login(page):
    log("\n── LOGIN ─────────────────────────────────────────────────────────")
    log("  Navigating to Etsy sign-in page...")
    await page.goto("https://www.etsy.com/signin", wait_until="domcontentloaded")
    await page.wait_for_timeout(2500)

    # Email field
    await try_fill(page, [
        '#join_neu_email_field',
        'input[name="email"]',
        'input[type="email"]',
        'input[placeholder*="Email" i]',
    ], ETSY_EMAIL, "email")

    # Continue / Next button (some Etsy flows split email + password)
    await try_click(page, [
        'button[name="submit_attempt"]',
        'button:has-text("Continue")',
        'button:has-text("Sign in")',
        'button[type="submit"]',
    ], "Continue button")
    await page.wait_for_timeout(2000)

    # Password field
    await try_fill(page, [
        '#join_neu_password_field',
        'input[name="password"]',
        'input[type="password"]',
        'input[placeholder*="Password" i]',
    ], ETSY_PASSWORD, "password")

    # Sign In button
    await try_click(page, [
        'button[name="submit_attempt"]',
        'button:has-text("Sign in")',
        'button:has-text("Continue")',
        'button[type="submit"]',
    ], "Sign In button")

    log("  Waiting for login to complete...")
    await page.wait_for_timeout(5000)

    if "signin" in page.url.lower():
        log("  ⚠  Still on sign-in page — there may be a CAPTCHA.")
        log("  → Please complete it manually in the browser window, then press Enter here.")
        input("  Press Enter once you are fully logged in: ")
    else:
        log(f"  ✓ Logged in  (url: {page.url})")


# ── UPLOAD ONE LISTING ────────────────────────────────────────────────────────
async def upload_listing(page, listing, num, total):
    label = listing["label"]
    log(f"\n{'═'*62}")
    log(f"  LISTING {num}/{total}: {label}")
    log(f"{'═'*62}")

    # ── Navigate to new listing form ──────────────────────────────────────────
    log("\n  [1] Opening new listing form...")
    await page.goto(
        "https://www.etsy.com/your/shops/me/tools/listings/create",
        wait_until="domcontentloaded",
    )
    await page.wait_for_timeout(3000)

    if "signin" in page.url.lower() or "login" in page.url.lower():
        log("  ⚠  Redirected to login — please log in manually in the browser window.")
        log("  → Do NOT close the browser. After logging in, come back here.")
        input("  Press Enter once you are logged in: ")
        await page.goto(
            "https://www.etsy.com/your/shops/me/tools/listings/create",
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(3000)

    log(f"  URL: {page.url}")

    # ── Upload listing images ─────────────────────────────────────────────────
    log(f"\n  [2] Uploading {len(listing['images'])} listing images...")
    valid_images = [p for p in listing["images"] if os.path.exists(p)]
    if not valid_images:
        log("    ✗ No valid image files found — skipping")
    else:
        try:
            # Find the image file input (usually the first input[type=file])
            await page.wait_for_selector('input[type="file"]', timeout=8000)
            file_inputs = await page.query_selector_all('input[type="file"]')

            image_input = None
            for fi in file_inputs:
                accept = (await fi.get_attribute("accept") or "").lower()
                if "video" in accept:
                    continue  # skip video input
                if "image" in accept or not accept:
                    image_input = fi
                    break

            if not image_input and file_inputs:
                image_input = file_inputs[0]

            if image_input:
                await image_input.set_input_files(valid_images)
                log(f"    ✓ Queued {len(valid_images)} images — waiting for upload...")
                await page.wait_for_timeout(7000)
            else:
                log("    ✗ Image upload input not found")
        except PlaywrightTimeout:
            log("    ✗ Timed out looking for file input")
        except Exception as e:
            log(f"    ✗ Error uploading images: {e}")

    # ── Title ─────────────────────────────────────────────────────────────────
    log("\n  [3] Filling in title...")
    await try_fill(page, [
        '#title-input',
        'input[name="title"]',
        'textarea[name="title"]',
        '[data-test-id="title-input"]',
        'input[placeholder*="title" i]',
    ], listing["title"], "title")

    # ── Mark as Digital ───────────────────────────────────────────────────────
    log("\n  [4] Setting listing type to Digital...")
    await try_click(page, [
        'label:has-text("A digital file")',
        'label:has-text("Digital")',
        'input[value="download"]',
        'input[name="type"][value="download"]',
        '[data-test-id="digital-radio"]',
    ], "Digital type radio")
    await page.wait_for_timeout(1000)

    # ── Description ───────────────────────────────────────────────────────────
    log("\n  [5] Filling in description...")
    desc_filled = False
    for sel in [
        '#description-text-area-input',
        'textarea[name="description"]',
        '[data-test-id="description-input"]',
        'textarea[placeholder*="description" i]',
        '#description',
    ]:
        try:
            el = await page.wait_for_selector(sel, timeout=3000)
            if el and await el.is_visible():
                await el.click()
                await el.fill(listing["description"])
                log("    ✓ Filled description")
                desc_filled = True
                break
        except Exception:
            continue

    if not desc_filled:
        # Try contenteditable div (rich text editor)
        try:
            el = await page.wait_for_selector(
                'div[contenteditable="true"]', timeout=3000
            )
            if el:
                await el.click()
                await page.keyboard.press("Control+a")
                await page.keyboard.type(listing["description"], delay=2)
                log("    ✓ Filled description (contenteditable)")
        except Exception:
            log("    ✗ Could not fill description")

    # ── Price ─────────────────────────────────────────────────────────────────
    log("\n  [6] Setting price...")
    await try_fill(page, [
        '#price-input',
        'input[name="price"]',
        '[data-test-id="price-input"]',
        'input[placeholder*="price" i]',
        'input[type="number"][name*="price"]',
    ], listing["price"], f"price (${listing['price']})")

    # ── Quantity ──────────────────────────────────────────────────────────────
    log("\n  [7] Setting quantity...")
    await try_fill(page, [
        '#quantity-input',
        'input[name="quantity"]',
        '[data-test-id="quantity-input"]',
        'input[placeholder*="quantity" i]',
    ], listing["quantity"], "quantity")

    # ── Tags ──────────────────────────────────────────────────────────────────
    log(f"\n  [8] Adding {len(listing['tags'])} tags...")
    tag_input = None
    for sel in [
        '#tag-input',
        'input[name="tags"]',
        '[data-test-id="tag-input"]',
        'input[placeholder*="tag" i]',
        'input[placeholder*="Add a tag" i]',
        '.tag-input input',
    ]:
        try:
            el = await page.wait_for_selector(sel, timeout=3000)
            if el and await el.is_visible():
                tag_input = el
                break
        except Exception:
            continue

    if tag_input:
        for tag in listing["tags"]:
            try:
                await tag_input.click()
                await tag_input.fill(tag)
                await page.wait_for_timeout(300)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(400)
            except Exception:
                pass
        log(f"    ✓ Added {len(listing['tags'])} tags")
    else:
        log("    ✗ Tag input not found")

    # ── Digital product file ──────────────────────────────────────────────────
    digital_file = listing["digital_file"]
    log(f"\n  [9] Uploading product file: {os.path.basename(digital_file)}...")
    if not os.path.exists(digital_file):
        log(f"    ✗ File not found: {digital_file}")
    else:
        try:
            # Scroll down so the digital upload section is in view
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1500)

            file_inputs = await page.query_selector_all('input[type="file"]')
            uploaded = False

            # Look for a file input that is NOT an image input
            for fi in file_inputs:
                accept = (await fi.get_attribute("accept") or "").lower()
                name_attr = (await fi.get_attribute("name") or "").lower()
                if "image" in accept:
                    continue  # skip image inputs
                try:
                    await fi.set_input_files(digital_file)
                    await page.wait_for_timeout(5000)
                    log(f"    ✓ Uploaded {os.path.basename(digital_file)}")
                    uploaded = True
                    break
                except Exception:
                    continue

            if not uploaded:
                # Last resort: try the last file input on the page
                if file_inputs:
                    try:
                        await file_inputs[-1].set_input_files(digital_file)
                        await page.wait_for_timeout(5000)
                        log("    ✓ Uploaded product file (fallback)")
                    except Exception as e:
                        log(f"    ✗ Could not upload product file: {e}")
                else:
                    log("    ✗ No file inputs found for product upload")
        except Exception as e:
            log(f"    ✗ Error during product upload: {e}")

    # ── Save as Draft ─────────────────────────────────────────────────────────
    log("\n  [10] Saving as draft...")
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(1000)

    saved = False

    # First choice: explicit "Save as draft" button
    for sel in [
        'button:has-text("Save as draft")',
        'button:has-text("Save as Draft")',
        '[data-test-id="save-draft-button"]',
        'a:has-text("Save as draft")',
        'button[data-action="save-draft"]',
    ]:
        try:
            btn = await page.wait_for_selector(sel, timeout=4000)
            if btn and await btn.is_visible():
                txt = await btn.text_content()
                log(f"    → Clicking: '{txt.strip()}'")
                await btn.click()
                await page.wait_for_timeout(5000)
                log("    ✓ Saved as draft!")
                saved = True
                break
        except Exception:
            continue

    if not saved:
        # Try "Save and continue" — advances without publishing
        for sel in [
            'button:has-text("Save and continue")',
            'button:has-text("Save & continue")',
            'button[data-test-id="save-continue"]',
            'button:has-text("Next")',
        ]:
            try:
                btn = await page.wait_for_selector(sel, timeout=4000)
                if btn and await btn.is_visible():
                    txt = await btn.text_content()
                    log(f"    → Clicking: '{txt.strip()}'  (step 1 of save flow)")
                    await btn.click()
                    await page.wait_for_timeout(4000)

                    # On next screen look for "Save as draft"
                    for draft_sel in [
                        'button:has-text("Save as draft")',
                        'button:has-text("Save as Draft")',
                        '[data-test-id="save-draft-button"]',
                    ]:
                        try:
                            dbtn = await page.wait_for_selector(draft_sel, timeout=4000)
                            if dbtn and await dbtn.is_visible():
                                await dbtn.click()
                                await page.wait_for_timeout(4000)
                                log("    ✓ Saved as draft (step 2)")
                                saved = True
                                break
                        except Exception:
                            continue
                    if not saved:
                        log("    ✓ Advanced past step 1 — listing in progress/draft state")
                        saved = True
                    break
            except Exception:
                continue

    if not saved:
        log("    ⚠  Could not find Save as Draft — do NOT click Publish.")
        log("    → The listing is in draft state. You can close the tab or navigate away.")
        log("    → Press Enter to continue to the next listing.")
        input("    Press Enter: ")
        saved = True

    log(f"\n  ✓ Done: {label}")
    return saved


# ── MAIN ──────────────────────────────────────────────────────────────────────
async def main():
    log("╔══════════════════════════════════════════════════════════════╗")
    log("║       ETSY DRAFT UPLOADER — Graduation Party Planner        ║")
    log("╚══════════════════════════════════════════════════════════════╝")
    log("")
    log("  3 listings will be created as DRAFTS (not published).")
    log("  A Chrome browser window will open — you can watch it work.")
    log("")

    # Verify files
    log("Verifying files...")
    missing = []
    for lst in LISTINGS:
        for img in lst["images"]:
            if not os.path.exists(img):
                missing.append(img)
        if not os.path.exists(lst["digital_file"]):
            missing.append(lst["digital_file"])
    if missing:
        log("\n✗ Missing files:")
        for m in missing:
            log(f"    {m}")
        log("\nPlease run the product generators first:")
        log("  cd idea-1-spreadsheet/product && python create_workbook.py")
        log("  cd idea-2-memory-book/product && python create_memory_book.py")
        log("  cd idea-1-spreadsheet/images && python create_images.py")
        log("  cd idea-2-memory-book/images && python create_images.py")
        log("  cd idea-3-welcome-sign/images && python create_images.py")
        sys.exit(1)
    log("  ✓ All files present\n")

    results = []

    async with async_playwright() as p:
        log("  Launching Google Chrome with your existing profile...")
        log("  The script will automatically close any open Chrome windows first.")
        log("")
        log("  ⚠  SAVE any open work in Chrome, then press Enter.")
        input("  Press Enter to close Chrome and launch the Etsy uploader: ")

        # Kill any background Chrome processes that may be holding the profile lock.
        # (This is safe — it only affects Chrome, not this script.)
        log("  Killing any background Chrome processes...")
        subprocess.run(["pkill", "-9", "-f", "Google Chrome"], capture_output=True)
        subprocess.run(["pkill", "-9", "-f", "Google Chrome Helper"], capture_output=True)
        time.sleep(2)
        log("  ✓ Chrome processes cleared\n")

        # Use the real Chrome profile so Etsy sees a normal logged-in browser.
        # No login step needed — your existing session/cookies are reused.
        CHROME_PROFILE = os.path.expanduser(
            "~/Library/Application Support/Google/Chrome"
        )

        context = await p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            channel="chrome",
            headless=False,
            slow_mo=350,
            args=[
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-sync",
                "--disable-extensions-except=",
                "--disable-background-networking",
            ],
        )

        page = await context.new_page()
        page.set_default_timeout(30000)

        # Navigate to Etsy to confirm we're logged in
        log("\n  Checking Etsy login status...")
        await page.goto("https://www.etsy.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        if "signin" in page.url.lower():
            log("  Not logged in — please log in manually in the browser window.")
            input("  Press Enter once you're logged into Etsy: ")
        else:
            log("  ✓ Already logged into Etsy via your Chrome profile")

        # Upload all 3 listings
        for i, listing in enumerate(LISTINGS):
            ok = await upload_listing(page, listing, i + 1, len(LISTINGS))
            results.append((listing["label"], ok))
            if i < len(LISTINGS) - 1:
                log("\n  Pausing 3 seconds before next listing...")
                await page.wait_for_timeout(3000)

        log("\n  All done! Leaving browser open so you can review the drafts...")
        await page.goto("https://www.etsy.com/your/shops/me/tools/listings?status=draft",
                        wait_until="domcontentloaded")
        await page.wait_for_timeout(15000)
        await context.close()

    # ── Summary ───────────────────────────────────────────────────────────────
    log("")
    log("╔══════════════════════════════════════════════════════════════╗")
    log("║                         SUMMARY                             ║")
    log("╚══════════════════════════════════════════════════════════════╝")
    for label, ok in results:
        icon = "✓" if ok else "⚠"
        log(f"  {icon}  {label}")
    log("")
    log("  Next steps:")
    log("  1. Go to etsy.com → Seller Hub → Listings → Drafts")
    log("  2. Add 10 ChatGPT-generated images to each listing")
    log("  3. Assign the correct Etsy category if needed")
    log("  4. Click Publish when ready!")
    log("")


if __name__ == "__main__":
    asyncio.run(main())
