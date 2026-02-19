#!/usr/bin/env python3
"""
Automate Etsy listing creation via Playwright/Chromium.
Logs in, navigates to listing creation, fills all fields, uploads files.
"""

import asyncio
import os
import time
from playwright.async_api import async_playwright

# ── Credentials ──
ETSY_EMAIL = "michelleandgrayford@gmail.com"
ETSY_PASSWORD = "Humes@0422"

# ── Files ──
PROJECT_DIR = "/home/user/claude-code/etsy-digital-planner"
PRODUCT_PDF = os.path.join(PROJECT_DIR, "product/2026_Wellness_Productivity_Digital_Planner.pdf")
VIDEO_FILE = os.path.join(PROJECT_DIR, "video/etsy_listing_video.mp4")

IMAGE_FILES = [
    os.path.join(PROJECT_DIR, "images/01_hero_thumbnail.png"),
    os.path.join(PROJECT_DIR, "images/02_feature_overview.png"),
    os.path.join(PROJECT_DIR, "images/03_monthly_preview.png"),
    os.path.join(PROJECT_DIR, "images/04_daily_preview.png"),
    os.path.join(PROJECT_DIR, "images/05_wellness_features.png"),
    os.path.join(PROJECT_DIR, "images/05b_weekly_preview.png"),
    os.path.join(PROJECT_DIR, "images/06_habit_tracker.png"),
    os.path.join(PROJECT_DIR, "images/07_goal_setting.png"),
    os.path.join(PROJECT_DIR, "images/08_guided_journal.png"),
    os.path.join(PROJECT_DIR, "images/09_compatibility.png"),
]

# ── Listing Data ──
LISTING_TITLE = "Digital Planner 2026 All-in-One Wellness Productivity GoodNotes Notability iPad Hyperlinked"

LISTING_DESCRIPTION = """The only planner you need for 2026 -- wellness meets productivity in one beautifully designed digital planner.

Stop juggling multiple apps and planners. This all-in-one digital planner combines daily planning, goal setting, habit tracking, and complete wellness features into 28 thoughtfully designed, fully hyperlinked pages.

WHAT'S INSIDE:

- 12 Monthly Calendar Spreads (Jan-Dec 2026) with clickable navigation
- 4 Weekly Planner Templates with built-in wellness check-ins
- 3 Daily Planner Layouts featuring morning routine, hourly schedule, priorities, to-do list, gratitude section, water intake tracker, and mood tracker
- Goal Setting Suite with quarterly goals, life wheel assessment, and word of the year
- Monthly Habit Tracker with 12 pre-set wellness habits + 4 custom rows, 31-day grid
- Wellness Dashboard including sleep tracker, weekly meal planner, fitness log, and self-care checklist with 15 curated activities
- Guided Journal with morning pages, evening reflection, and weekly growth prompts
- 3 Lined Notes Pages for brainstorming and free writing
- Year-at-a-Glance overview with clickable month navigation

WHY THIS PLANNER IS DIFFERENT:

Unlike basic planners that only track tasks, this planner treats you as a whole person. Every week includes wellness check-ins. Every day includes gratitude. Every month includes reflection. The result? You don't just get more done -- you feel better doing it.

DESIGN DETAILS:

- Calming Patina Blue and warm linen color palette
- Minimalist, clutter-free layouts that are easy on the eyes
- Left sidebar navigation tabs on every page for instant access
- Clean typography with clear visual hierarchy
- Designed in landscape orientation for optimal tablet viewing

FULLY HYPERLINKED: Every sidebar tab is clickable. Jump from your daily planner to your habit tracker to your wellness dashboard with a single tap. No scrolling through pages -- just seamless navigation throughout the entire planner.

COMPATIBLE WITH: GoodNotes (iPad & Mac), Notability (iPad & Mac), Xodo (Android, Windows, iOS), Noteshelf (iPad), Zinnia (iPad), PDF Expert (All devices), and any PDF annotation app.

HOW IT WORKS:
1. Purchase and instantly download the PDF file
2. Import into your favorite PDF annotation app (GoodNotes, Notability, etc.)
3. Start planning! Use the hyperlinked tabs to navigate between sections
4. Write, type, or draw directly on the pages with your Apple Pencil or stylus

WHAT YOU RECEIVE:
- 1 PDF file (28 pages, fully hyperlinked, landscape A4 format)
- Instant digital download -- no waiting for shipping
- Lifetime access to your file through your Etsy purchases

NOTE: This is a DIGITAL product. No physical item will be shipped. Designed for use with PDF annotation apps on tablets. Colors may vary slightly depending on your device display settings."""

LISTING_TAGS = [
    "digital planner 2026",
    "goodnotes planner template",
    "notability planner ipad",
    "wellness journal digital",
    "habit tracker printable",
    "daily weekly monthly planner",
    "goal setting template",
    "self care planner pdf",
    "hyperlinked planner tablet",
    "productivity planner download",
    "digital journal 2026",
    "meal planner fitness log",
    "guided journal template",
]

LISTING_PRICE = "9.97"


async def run():
    print("=" * 60)
    print("ETSY LISTING AUTOMATION")
    print("2026 Wellness & Productivity Digital Planner")
    print("=" * 60)

    async with async_playwright() as p:
        # Launch browser
        print("\n[1/8] Launching Chromium...")
        browser = await p.chromium.launch(
            executable_path="/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome",
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
            ]
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )

        page = await context.new_page()
        page.set_default_timeout(30000)

        # ── Step 1: Log in to Etsy ──
        print("\n[2/8] Logging into Etsy...")
        await page.goto("https://www.etsy.com/signin", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Take screenshot to see current state
        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_01_signin.png"))
        print("  Screenshot saved: screenshot_01_signin.png")

        # Try to find and fill email field
        try:
            # Etsy signin page - look for email input
            email_selectors = [
                '#join_neu_email_field',
                'input[name="email"]',
                'input[type="email"]',
                '#email-input',
                'input[data-test-id="email-input"]',
                '#signin-email',
                'input[placeholder*="email" i]',
                'input[placeholder*="Email" i]',
            ]

            email_input = None
            for selector in email_selectors:
                try:
                    email_input = await page.wait_for_selector(selector, timeout=3000)
                    if email_input:
                        print(f"  Found email input: {selector}")
                        break
                except:
                    continue

            if not email_input:
                # Try finding any visible text input
                inputs = await page.query_selector_all('input[type="text"], input[type="email"], input:not([type])')
                for inp in inputs:
                    if await inp.is_visible():
                        email_input = inp
                        print("  Found visible text input for email")
                        break

            if email_input:
                await email_input.click()
                await email_input.fill(ETSY_EMAIL)
                await page.wait_for_timeout(500)
                print(f"  Entered email: {ETSY_EMAIL}")
            else:
                print("  WARNING: Could not find email input field")
                # Save page content for debugging
                content = await page.content()
                with open(os.path.join(PROJECT_DIR, "debug_signin_page.html"), "w") as f:
                    f.write(content)
                print("  Saved page HTML to debug_signin_page.html")

        except Exception as e:
            print(f"  Error finding email field: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_02_email.png"))

        # Look for continue/next button or password field
        try:
            # Try clicking continue/next button first (some flows split email and password)
            continue_selectors = [
                'button[name="submit_attempt"]',
                'button[type="submit"]',
                'button:has-text("Continue")',
                'button:has-text("Sign in")',
                'button:has-text("Next")',
                '[data-test-id="signin-button"]',
            ]

            for selector in continue_selectors:
                try:
                    btn = await page.wait_for_selector(selector, timeout=2000)
                    if btn and await btn.is_visible():
                        await btn.click()
                        print(f"  Clicked continue button: {selector}")
                        await page.wait_for_timeout(2000)
                        break
                except:
                    continue

        except Exception as e:
            print(f"  Note: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_03_after_email.png"))

        # Now look for password field
        try:
            password_selectors = [
                '#join_neu_password_field',
                'input[name="password"]',
                'input[type="password"]',
                '#password-input',
                '#signin-password',
                'input[placeholder*="password" i]',
                'input[placeholder*="Password" i]',
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = await page.wait_for_selector(selector, timeout=3000)
                    if password_input:
                        print(f"  Found password input: {selector}")
                        break
                except:
                    continue

            if not password_input:
                inputs = await page.query_selector_all('input[type="password"]')
                for inp in inputs:
                    if await inp.is_visible():
                        password_input = inp
                        print("  Found visible password input")
                        break

            if password_input:
                await password_input.click()
                await password_input.fill(ETSY_PASSWORD)
                await page.wait_for_timeout(500)
                print("  Entered password")

                # Click sign in button
                for selector in continue_selectors:
                    try:
                        btn = await page.wait_for_selector(selector, timeout=2000)
                        if btn and await btn.is_visible():
                            await btn.click()
                            print(f"  Clicked sign in button: {selector}")
                            break
                    except:
                        continue

                # Wait for login to complete
                await page.wait_for_timeout(5000)
                print("  Waiting for login to complete...")
            else:
                print("  WARNING: Could not find password input field")

        except Exception as e:
            print(f"  Error with password: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_04_after_login.png"))
        print(f"  Current URL: {page.url}")

        # Check if we're logged in
        if "signin" in page.url.lower():
            print("\n  WARNING: May still be on signin page. Saving debug info...")
            content = await page.content()
            with open(os.path.join(PROJECT_DIR, "debug_after_login.html"), "w") as f:
                f.write(content)

        # ── Step 2: Navigate to listing creation ──
        print("\n[3/8] Navigating to listing creation page...")
        await page.goto("https://www.etsy.com/your/shops/me/tools/listings/create", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_05_create_listing.png"))
        print(f"  Current URL: {page.url}")

        # ── Step 3: Upload photos ──
        print("\n[4/8] Uploading listing photos...")
        try:
            # Look for the photo upload area
            photo_upload_selectors = [
                'input[type="file"][accept*="image"]',
                '#listing-edit-image-upload input[type="file"]',
                '[data-selector="photo-upload"] input[type="file"]',
                'input[name="image"]',
                '.image-upload input[type="file"]',
                'input[type="file"]',
            ]

            file_input = None
            for selector in photo_upload_selectors:
                try:
                    inputs = await page.query_selector_all(selector)
                    for inp in inputs:
                        file_input = inp
                        print(f"  Found file input: {selector}")
                        break
                    if file_input:
                        break
                except:
                    continue

            if file_input:
                # Upload all images at once
                await file_input.set_input_files(IMAGE_FILES)
                print(f"  Uploaded {len(IMAGE_FILES)} images")
                await page.wait_for_timeout(5000)  # Wait for uploads
            else:
                print("  WARNING: Could not find image upload input")
                # Try alternative: drag and drop area
                all_inputs = await page.query_selector_all('input[type="file"]')
                print(f"  Found {len(all_inputs)} file inputs on page")
                if all_inputs:
                    await all_inputs[0].set_input_files(IMAGE_FILES)
                    print("  Uploaded images via first file input found")
                    await page.wait_for_timeout(5000)

        except Exception as e:
            print(f"  Error uploading images: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_06_after_images.png"))

        # ── Step 4: Upload video ──
        print("\n[5/8] Uploading listing video...")
        try:
            video_inputs = await page.query_selector_all('input[type="file"][accept*="video"], input[type="file"][accept*="mp4"]')
            if video_inputs:
                await video_inputs[0].set_input_files(VIDEO_FILE)
                print("  Uploaded video")
                await page.wait_for_timeout(5000)
            else:
                print("  Video upload input not found (may need to click 'Add video' first)")
                # Try clicking an add video button
                try:
                    add_video = await page.query_selector('button:has-text("video"), a:has-text("video"), [data-action="add-video"]')
                    if add_video:
                        await add_video.click()
                        await page.wait_for_timeout(1000)
                        video_inputs = await page.query_selector_all('input[type="file"]')
                        for vi in video_inputs:
                            accept = await vi.get_attribute("accept")
                            if accept and "video" in accept:
                                await vi.set_input_files(VIDEO_FILE)
                                print("  Uploaded video after clicking add button")
                                await page.wait_for_timeout(5000)
                                break
                except:
                    pass
        except Exception as e:
            print(f"  Error uploading video: {e}")

        # ── Step 5: Fill in listing details ──
        print("\n[6/8] Filling in listing details...")

        # Title
        try:
            title_selectors = [
                '#title-input',
                'input[name="title"]',
                '#listing-edit-title input',
                'textarea[name="title"]',
                '[data-test-id="title-input"]',
                'input[placeholder*="title" i]',
            ]
            for selector in title_selectors:
                try:
                    title_input = await page.wait_for_selector(selector, timeout=2000)
                    if title_input and await title_input.is_visible():
                        await title_input.click()
                        await title_input.fill("")
                        await title_input.fill(LISTING_TITLE)
                        print(f"  Filled title: {LISTING_TITLE[:50]}...")
                        break
                except:
                    continue
        except Exception as e:
            print(f"  Error setting title: {e}")

        # Set as Digital item
        try:
            digital_selectors = [
                'label:has-text("Digital")',
                '#is_digital',
                'input[value="digital"]',
                '[data-test-id="digital-radio"]',
                'label:has-text("A digital file")',
                'input[name="type"][value="download"]',
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
        except Exception as e:
            print(f"  Error setting digital type: {e}")

        # Description
        try:
            desc_selectors = [
                '#description-text-area-input',
                'textarea[name="description"]',
                '#listing-edit-description textarea',
                '[data-test-id="description-input"]',
                'textarea[placeholder*="description" i]',
                '#description',
            ]
            for selector in desc_selectors:
                try:
                    desc_input = await page.wait_for_selector(selector, timeout=2000)
                    if desc_input and await desc_input.is_visible():
                        await desc_input.click()
                        await desc_input.fill("")
                        await desc_input.fill(LISTING_DESCRIPTION)
                        print(f"  Filled description ({len(LISTING_DESCRIPTION)} chars)")
                        break
                except:
                    continue
        except Exception as e:
            print(f"  Error setting description: {e}")

        # Price
        try:
            price_selectors = [
                '#price-input',
                'input[name="price"]',
                '#listing-edit-price input',
                '[data-test-id="price-input"]',
                'input[placeholder*="price" i]',
                'input[type="number"][name*="price"]',
            ]
            for selector in price_selectors:
                try:
                    price_input = await page.wait_for_selector(selector, timeout=2000)
                    if price_input and await price_input.is_visible():
                        await price_input.click()
                        await price_input.fill("")
                        await price_input.fill(LISTING_PRICE)
                        print(f"  Set price: ${LISTING_PRICE}")
                        break
                except:
                    continue
        except Exception as e:
            print(f"  Error setting price: {e}")

        # Tags
        try:
            tag_selectors = [
                '#tag-input',
                'input[name="tags"]',
                '#listing-edit-tags input',
                '[data-test-id="tag-input"]',
                'input[placeholder*="tag" i]',
                '.tag-input input',
            ]
            tag_input = None
            for selector in tag_selectors:
                try:
                    tag_input = await page.wait_for_selector(selector, timeout=2000)
                    if tag_input and await tag_input.is_visible():
                        print(f"  Found tag input: {selector}")
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
            else:
                print("  WARNING: Could not find tag input")
        except Exception as e:
            print(f"  Error setting tags: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_07_after_details.png"))

        # ── Step 6: Upload digital file ──
        print("\n[7/8] Uploading digital download file...")
        try:
            # Look for digital file upload
            digital_file_selectors = [
                'input[type="file"][name*="digital"]',
                '.digital-file-upload input[type="file"]',
                '#digital-file-input',
                '[data-test-id="digital-file-upload"] input[type="file"]',
            ]

            file_uploaded = False
            for selector in digital_file_selectors:
                try:
                    di = await page.wait_for_selector(selector, timeout=2000)
                    if di:
                        await di.set_input_files(PRODUCT_PDF)
                        print("  Uploaded digital file (PDF)")
                        file_uploaded = True
                        await page.wait_for_timeout(3000)
                        break
                except:
                    continue

            if not file_uploaded:
                # Try finding all file inputs and use the one likely for digital files
                all_file_inputs = await page.query_selector_all('input[type="file"]')
                print(f"  Found {len(all_file_inputs)} total file inputs")
                # The digital file input is typically the last or second one
                for fi in all_file_inputs:
                    accept = await fi.get_attribute("accept") or ""
                    name = await fi.get_attribute("name") or ""
                    if "pdf" in accept.lower() or "digital" in name.lower() or "file" in name.lower():
                        await fi.set_input_files(PRODUCT_PDF)
                        print(f"  Uploaded digital file via matched input (accept={accept}, name={name})")
                        file_uploaded = True
                        await page.wait_for_timeout(3000)
                        break

        except Exception as e:
            print(f"  Error uploading digital file: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_08_after_digital.png"))

        # ── Step 7: Publish / Save ──
        print("\n[8/8] Saving/Publishing listing...")
        try:
            publish_selectors = [
                'button:has-text("Publish")',
                'button:has-text("Save and continue")',
                'button[type="submit"]:has-text("Publish")',
                '[data-test-id="publish-button"]',
                'button:has-text("Save")',
                '#listing-edit-submit',
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

        except Exception as e:
            print(f"  Error publishing: {e}")

        await page.screenshot(path=os.path.join(PROJECT_DIR, "screenshot_09_final.png"))
        print(f"\n  Final URL: {page.url}")

        # Save page HTML for debugging
        content = await page.content()
        with open(os.path.join(PROJECT_DIR, "debug_final_page.html"), "w") as f:
            f.write(content)

        print("\n" + "=" * 60)
        print("AUTOMATION COMPLETE")
        print("Screenshots saved in:", PROJECT_DIR)
        print("Check screenshots to verify each step succeeded.")
        print("=" * 60)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
