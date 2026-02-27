#!/usr/bin/env python3
"""
Automate Etsy listing creation for Easter Party Games Bundle via Playwright/Chromium.
Logs in, navigates to listing creation, fills all fields, uploads files.

SETUP:
  pip install playwright
  python3 -m playwright install chromium
  python3 automate_etsy_chrome.py
"""

import asyncio
import os
import time
from playwright.async_api import async_playwright

# ── Credentials (use env vars or fallback) ──
ETSY_EMAIL = os.environ.get("ETSY_EMAIL", "michelleandgrayford@gmail.com")
ETSY_PASSWORD = os.environ.get("ETSY_PASSWORD", "Humes@0422")

# ── Files ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGE_FILES = [
    os.path.join(BASE_DIR, "images/01_hero_main_listing.png"),
    os.path.join(BASE_DIR, "images/02_whats_included.png"),
    os.path.join(BASE_DIR, "images/03_game_preview_word.png"),
    os.path.join(BASE_DIR, "images/04_game_preview_party.png"),
    os.path.join(BASE_DIR, "images/05_game_preview_kids.png"),
    os.path.join(BASE_DIR, "images/06_game_preview_activity.png"),
    os.path.join(BASE_DIR, "images/07_how_it_works.png"),
    os.path.join(BASE_DIR, "images/08_size_and_format.png"),
    os.path.join(BASE_DIR, "images/09_perfect_for.png"),
    os.path.join(BASE_DIR, "images/10_value_proposition.png"),
]

SCREENSHOT_DIR = os.path.join(BASE_DIR, "listing/screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ── Listing Data ──
LISTING_TITLE = "Easter Games Bundle Printable Easter Party Games for Kids Adults Family Easter Activities Classroom Games Egg Hunt Trivia Instant Download"

LISTING_DESCRIPTION = """EASTER PARTY GAMES BUNDLE — 25 Printable Games for the Whole Family

Make this Easter unforgettable with 25 beautifully designed printable party games that everyone will love — from toddlers to grandparents!

Whether you're planning an Easter brunch, classroom party, family gathering, church event, or egg hunt — this bundle has you covered with hours of entertainment.

Just download, print, and play. It's that simple.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT'S INCLUDED (25 Games):

WORD & TRIVIA GAMES:
1. Easter Trivia Challenge (Easy + Hard versions)
2. Easter Word Search (2 difficulty levels)
3. Easter Crossword Puzzle
4. Easter Word Scramble
5. Easter Fill-in-the-Blank Stories (Mad Libs style)
6. Easter A-Z Categories
7. Easter Scattergories

FUN PARTY GAMES:
8. Easter Bingo (10 unique cards + calling sheet)
9. Easter Emoji Pictionary
10. Easter Would You Rather
11. Easter This or That
12. Easter Charades Cards (40 prompts)
13. Easter Who Am I? Game
14. Easter Hot Take / Unpopular Opinions

KIDS' FAVORITES:
15. Easter I Spy
16. Easter Dot-to-Dot (3 designs)
17. Easter Color by Number (3 designs)
18. Easter Maze Challenge (3 levels)
19. Easter Matching Memory Game
20. Easter Scavenger Hunt (Indoor + Outdoor)

ACTIVITY PAGES:
21. Easter Roll & Draw
22. Easter Story Starters (Creative Writing)
23. Easter Riddles & Jokes Page
24. Easter Coloring Pages (5 designs)
25. Easter Party Photo Props Template

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY FAMILIES LOVE THIS BUNDLE:

✓ SOMETHING FOR EVERYONE — Games for kids, teens, and adults. Ages 3 to 99.
✓ READY IN MINUTES — Download, print, and play. No prep, no fuss.
✓ PRINT AS MANY AS YOU NEED — One purchase = unlimited prints. Perfect for large groups.
✓ TWO SIZES INCLUDED — US Letter (8.5 x 11") AND A4 for international buyers.
✓ GORGEOUS DESIGN — Soft pastel palette with adorable bunny, egg, and spring illustrations.
✓ TONER-FRIENDLY — Beautiful full-color designs that also look great printed in black & white.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFECT FOR:

• Easter Sunday family gatherings
• Kids' Easter parties
• Classroom Easter celebrations
• Sunday School & church events
• Easter brunch entertainment
• Egg hunt warm-up activities
• Virtual Easter celebrations (play over Zoom!)
• Easter care packages & basket stuffers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:

1. Purchase and download the PDF files instantly
2. Print at home or at a local print shop
3. Grab some pencils, pens, or crayons
4. Play and enjoy with family & friends!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT YOU'LL RECEIVE:

• 1 ZIP file containing:
  - All 25 games as individual PDF files (for easy selection)
  - 1 Complete Bundle PDF (all games in one file)
  - US Letter (8.5 x 11") versions
  - A4 international versions
  - Answer keys where applicable
  - Printing tips & recommendations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FREQUENTLY ASKED QUESTIONS:

Q: What age group are these games for?
A: This bundle includes games for ALL ages! Simple activities for kids 3+ (coloring, I Spy, dot-to-dot), challenging word games for older kids and teens, and sophisticated party games adults will love (trivia, Scattergories, Would You Rather).

Q: Can I print these more than once?
A: Absolutely! Print as many copies as you need for your family, classroom, or event.

Q: Is this a physical product?
A: No, this is a DIGITAL DOWNLOAD. No physical item will be shipped. Download immediately after purchase.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLEASE NOTE:
• DIGITAL DOWNLOAD — no physical item shipped
• Files available immediately after purchase
• For personal use only
• No refunds due to digital nature

Make this Easter one to remember!"""

LISTING_TAGS = [
    "easter games bundle",
    "easter party games",
    "printable easter",
    "easter activities",
    "easter games kids",
    "easter egg hunt",
    "easter trivia",
    "classroom easter",
    "family easter games",
    "easter printable",
    "easter bingo",
    "easter scavenger hunt",
    "easter word search",
]

LISTING_PRICE = "7.99"


async def run():
    print("=" * 60)
    print("ETSY LISTING AUTOMATION")
    print("Easter Party Games Bundle")
    print("=" * 60)

    # Validate files
    print("\nChecking files...")
    for f in IMAGE_FILES:
        if os.path.exists(f):
            size_kb = os.path.getsize(f) / 1024
            print(f"  OK: {os.path.basename(f)} ({size_kb:.0f} KB)")
        else:
            print(f"  MISSING: {f}")
            return

    async with async_playwright() as p:
        # Launch browser
        print("\n[1/8] Launching Chromium...")
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )

        page = await context.new_page()
        page.set_default_timeout(60000)

        # ── Step 1: Log in to Etsy ──
        print("\n[2/8] Logging into Etsy...")
        print("  A browser window will open. If you see a CAPTCHA, solve it manually.")
        await page.goto("https://www.etsy.com/signin", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "01_signin.png"))

        # Find and fill email
        email_selectors = [
            '#join_neu_email_field', 'input[name="email"]', 'input[type="email"]',
            '#email-input', 'input[placeholder*="email" i]', 'input[placeholder*="Email" i]',
        ]
        email_input = None
        for selector in email_selectors:
            try:
                email_input = await page.wait_for_selector(selector, timeout=3000)
                if email_input:
                    break
            except:
                continue

        if not email_input:
            inputs = await page.query_selector_all('input[type="text"], input[type="email"], input:not([type])')
            for inp in inputs:
                if await inp.is_visible():
                    email_input = inp
                    break

        if email_input:
            await email_input.click()
            await email_input.fill(ETSY_EMAIL)
            print(f"  Entered email: {ETSY_EMAIL}")
        else:
            print("  WARNING: Could not find email input")

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "02_email.png"))

        # Click continue
        continue_selectors = [
            'button[name="submit_attempt"]', 'button[type="submit"]',
            'button:has-text("Continue")', 'button:has-text("Sign in")',
        ]
        for selector in continue_selectors:
            try:
                btn = await page.wait_for_selector(selector, timeout=2000)
                if btn and await btn.is_visible():
                    await btn.click()
                    await page.wait_for_timeout(2000)
                    break
            except:
                continue

        # Fill password
        password_selectors = [
            '#join_neu_password_field', 'input[name="password"]',
            'input[type="password"]', '#password-input',
        ]
        password_input = None
        for selector in password_selectors:
            try:
                password_input = await page.wait_for_selector(selector, timeout=3000)
                if password_input:
                    break
            except:
                continue

        if password_input:
            await password_input.click()
            await password_input.fill(ETSY_PASSWORD)
            print("  Entered password")

            for selector in continue_selectors:
                try:
                    btn = await page.wait_for_selector(selector, timeout=2000)
                    if btn and await btn.is_visible():
                        await btn.click()
                        break
                except:
                    continue

            await page.wait_for_timeout(5000)

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "03_after_login.png"))
        print(f"  Current URL: {page.url}")

        # Pause to let user handle CAPTCHA/2FA if needed
        if "signin" in page.url or "captcha" in page.url.lower():
            print("\n  ⏳ Waiting for you to complete login (CAPTCHA/2FA)...")
            print("  Complete the login in the browser window, then it will continue automatically.")
            try:
                await page.wait_for_url("**/your/shops/**", timeout=120000)
            except:
                pass
            await page.wait_for_timeout(3000)
            print(f"  Current URL after login: {page.url}")

        # ── Step 2: Navigate to listing creation ──
        print("\n[3/8] Navigating to listing creation page...")
        await page.goto("https://www.etsy.com/your/shops/me/tools/listings/create", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "04_create_listing.png"))

        # ── Step 3: Upload photos ──
        print("\n[4/8] Uploading listing photos...")
        try:
            file_inputs = await page.query_selector_all('input[type="file"]')
            if file_inputs:
                await file_inputs[0].set_input_files(IMAGE_FILES)
                print(f"  Uploaded {len(IMAGE_FILES)} images")
                await page.wait_for_timeout(5000)
            else:
                print("  WARNING: Could not find image upload input")
        except Exception as e:
            print(f"  Error uploading images: {e}")

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "05_after_images.png"))

        # ── Step 4: Fill title ──
        print("\n[5/8] Filling in listing details...")
        title_selectors = [
            '#title-input', 'input[name="title"]', 'textarea[name="title"]',
            'input[placeholder*="title" i]',
        ]
        for selector in title_selectors:
            try:
                title_input = await page.wait_for_selector(selector, timeout=2000)
                if title_input and await title_input.is_visible():
                    await title_input.click()
                    await title_input.fill(LISTING_TITLE)
                    print(f"  Filled title: {LISTING_TITLE[:60]}...")
                    break
            except:
                continue

        # Set as Digital
        digital_selectors = [
            'label:has-text("Digital")', 'label:has-text("A digital file")',
            'input[value="digital"]',
        ]
        for selector in digital_selectors:
            try:
                digital = await page.wait_for_selector(selector, timeout=2000)
                if digital and await digital.is_visible():
                    await digital.click()
                    print("  Set listing type: Digital")
                    await page.wait_for_timeout(1000)
                    break
            except:
                continue

        # Description
        desc_selectors = [
            '#description-text-area-input', 'textarea[name="description"]',
            '[data-test-id="description-input"]', 'textarea[placeholder*="description" i]',
        ]
        for selector in desc_selectors:
            try:
                desc_input = await page.wait_for_selector(selector, timeout=2000)
                if desc_input and await desc_input.is_visible():
                    await desc_input.click()
                    await desc_input.fill(LISTING_DESCRIPTION)
                    print(f"  Filled description ({len(LISTING_DESCRIPTION)} chars)")
                    break
            except:
                continue

        # Price
        price_selectors = [
            '#price-input', 'input[name="price"]',
            'input[placeholder*="price" i]', 'input[type="number"][name*="price"]',
        ]
        for selector in price_selectors:
            try:
                price_input = await page.wait_for_selector(selector, timeout=2000)
                if price_input and await price_input.is_visible():
                    await price_input.click()
                    await price_input.fill(LISTING_PRICE)
                    print(f"  Set price: ${LISTING_PRICE}")
                    break
            except:
                continue

        # Tags
        tag_selectors = [
            '#tag-input', 'input[name="tags"]', 'input[placeholder*="tag" i]',
        ]
        tag_input = None
        for selector in tag_selectors:
            try:
                tag_input = await page.wait_for_selector(selector, timeout=2000)
                if tag_input and await tag_input.is_visible():
                    break
                tag_input = None
            except:
                continue

        if tag_input:
            for tag in LISTING_TAGS:
                await tag_input.fill(tag)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(300)
            print(f"  Added {len(LISTING_TAGS)} tags")

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "06_after_details.png"))

        # ── Step 6: Publish ──
        print("\n[8/8] Saving/Publishing listing...")
        publish_selectors = [
            'button:has-text("Publish")', 'button:has-text("Save and continue")',
            'button[type="submit"]:has-text("Publish")', 'button:has-text("Save")',
        ]
        for selector in publish_selectors:
            try:
                btn = await page.wait_for_selector(selector, timeout=3000)
                if btn and await btn.is_visible():
                    text = await btn.text_content()
                    print(f"  Found publish button: '{text.strip()}'")
                    await btn.click()
                    print("  Clicked publish!")
                    await page.wait_for_timeout(5000)
                    break
            except:
                continue

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "07_final.png"))
        print(f"\n  Final URL: {page.url}")

        print("\n" + "=" * 60)
        print("AUTOMATION COMPLETE")
        print(f"Screenshots saved in: {SCREENSHOT_DIR}")
        print("=" * 60)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
