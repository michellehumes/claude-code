#!/usr/bin/env python3
"""
Opens your Etsy draft listing and fills in the missing fields:
- Category, Digital type, Price, Tags
Then publishes it.
"""

import asyncio
import os
import random
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "listing/screenshots")
PROFILE_DIR = os.path.join(BASE_DIR, ".chrome-profile")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

LISTING_PRICE = "7.99"
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


async def human_delay(min_ms=800, max_ms=2000):
    await asyncio.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


async def run():
    print("=" * 60)
    print("FINISH ETSY DRAFT LISTING")
    print("Easter Party Games Bundle")
    print("=" * 60)

    async with async_playwright() as p:
        print("\n[1/6] Launching Chrome...")
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            args=['--disable-blink-features=AutomationControlled'],
        )

        page = context.pages[0] if context.pages else await context.new_page()
        page.set_default_timeout(60000)

        # Go to drafts page
        print("\n[2/6] Opening your draft listings...")
        await page.goto("https://www.etsy.com/your/shops/me/tools/listings/state:draft", wait_until="domcontentloaded")
        await human_delay(3000, 5000)

        # Check if logged in
        if "signin" in page.url or "login" in page.url:
            print("  Please log in to Etsy in the browser window...")
            try:
                await page.wait_for_url("**etsy.com/**", timeout=120000)
            except:
                pass
            await page.goto("https://www.etsy.com/your/shops/me/tools/listings/state:draft", wait_until="domcontentloaded")
            await human_delay(3000, 5000)

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "draft_01_list.png"))
        print(f"  URL: {page.url}")

        # Find and click the Easter draft listing
        print("\n[3/6] Looking for your Easter Games draft...")
        easter_link = None
        # Try finding by listing title text
        selectors_to_try = [
            'a:has-text("Easter Games Bundle")',
            'a:has-text("Easter")',
            '[data-listing-card] a',
            '.listing-card a',
            'table a[href*="listing"]',
            'a[href*="listing-editor"]',
        ]
        for selector in selectors_to_try:
            try:
                links = await page.query_selector_all(selector)
                for link in links:
                    text = await link.text_content()
                    if text and "easter" in text.lower():
                        easter_link = link
                        print(f"  Found draft: '{text.strip()[:60]}...'")
                        break
                if easter_link:
                    break
            except:
                continue

        if not easter_link:
            # Just try clicking the first draft listing
            try:
                easter_link = await page.query_selector('a[href*="listing-editor"], a[href*="edit"]')
                if easter_link:
                    text = await easter_link.text_content()
                    print(f"  Found listing: '{text.strip()[:60] if text else 'untitled'}...'")
            except:
                pass

        if easter_link:
            await easter_link.click()
            await human_delay(3000, 5000)
        else:
            print("  Could not find draft automatically.")
            print("  Please click on the Easter Games draft in the browser.")
            print("  Waiting up to 60 seconds...")
            await page.wait_for_url("**/listing-editor/**", timeout=60000)
            await human_delay(2000, 3000)

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "draft_02_editing.png"))
        print(f"  Editing URL: {page.url}")

        # ── Set Category ──
        print("\n[4/6] Setting category...")
        # Try to find and click category selector
        category_selectors = [
            'button:has-text("Category")',
            'button:has-text("Select a category")',
            '[data-test-id="category-selector"]',
            '#category-selector',
            'button:has-text("Add category")',
            '.category-input button',
            'div:has-text("Category") button',
        ]
        for selector in category_selectors:
            try:
                cat_btn = await page.wait_for_selector(selector, timeout=3000)
                if cat_btn and await cat_btn.is_visible():
                    await cat_btn.click()
                    await human_delay(1000, 2000)
                    print("  Opened category selector")
                    break
            except:
                continue

        # Try searching for the category
        cat_search_selectors = [
            'input[placeholder*="category" i]',
            'input[placeholder*="search" i]',
            'input[type="search"]',
            '.category-search input',
        ]
        for selector in cat_search_selectors:
            try:
                search = await page.wait_for_selector(selector, timeout=3000)
                if search and await search.is_visible():
                    await search.click()
                    await human_delay()
                    await search.fill("party games")
                    await human_delay(1500, 2500)
                    # Click the matching result
                    result_selectors = [
                        'li:has-text("Party Games")',
                        'button:has-text("Party Games")',
                        'a:has-text("Party Games")',
                        '[role="option"]:has-text("Party")',
                    ]
                    for rs in result_selectors:
                        try:
                            result = await page.wait_for_selector(rs, timeout=3000)
                            if result and await result.is_visible():
                                await result.click()
                                print("  Selected category: Party Games")
                                await human_delay(1000, 2000)
                                break
                        except:
                            continue
                    break
            except:
                continue

        # ── Set as Digital ──
        print("  Setting type: Digital download...")
        digital_selectors = [
            'label:has-text("Digital")',
            'label:has-text("A digital file")',
            'input[value="digital"]',
            'button:has-text("Digital")',
            '[data-test-id="digital-listing-toggle"]',
        ]
        for selector in digital_selectors:
            try:
                digital = await page.wait_for_selector(selector, timeout=3000)
                if digital and await digital.is_visible():
                    await digital.click()
                    print("  Set listing type: Digital")
                    await human_delay(1000, 2000)
                    break
            except:
                continue

        # ── Set Price ──
        print("  Setting price...")
        price_selectors = [
            '#price-input', 'input[name="price"]',
            'input[placeholder*="price" i]', 'input[type="number"][name*="price"]',
            'input[aria-label*="price" i]',
        ]
        for selector in price_selectors:
            try:
                price_input = await page.wait_for_selector(selector, timeout=3000)
                if price_input and await price_input.is_visible():
                    await price_input.click()
                    await price_input.fill("")
                    await human_delay()
                    await price_input.fill(LISTING_PRICE)
                    print(f"  Set price: ${LISTING_PRICE}")
                    await human_delay()
                    break
            except:
                continue

        # ── Set Tags ──
        print("  Adding tags...")
        tag_selectors = [
            '#tag-input', 'input[name="tags"]', 'input[placeholder*="tag" i]',
            'input[aria-label*="tag" i]',
        ]
        tag_input = None
        for selector in tag_selectors:
            try:
                tag_input = await page.wait_for_selector(selector, timeout=3000)
                if tag_input and await tag_input.is_visible():
                    break
                tag_input = None
            except:
                continue

        if tag_input:
            for tag in LISTING_TAGS:
                await tag_input.fill(tag)
                await page.keyboard.press("Enter")
                await human_delay(300, 600)
            print(f"  Added {len(LISTING_TAGS)} tags")

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "draft_03_fields_filled.png"))

        # ── Review & Publish ──
        print("\n[5/6] Review the listing in the browser...")
        print("  Check everything looks correct.")
        print("  Publishing in 15 seconds... (close browser to cancel)")
        await human_delay(15000, 15000)

        print("\n[6/6] Publishing...")
        publish_selectors = [
            'button:has-text("Publish")',
            'button:has-text("Save and continue")',
            'button[type="submit"]:has-text("Publish")',
            'button:has-text("Save")',
        ]
        for selector in publish_selectors:
            try:
                btn = await page.wait_for_selector(selector, timeout=5000)
                if btn and await btn.is_visible():
                    text = await btn.text_content()
                    print(f"  Found button: '{text.strip()}'")
                    await btn.click()
                    print("  Clicked publish!")
                    await human_delay(5000, 8000)
                    break
            except:
                continue

        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, "draft_04_published.png"))
        print(f"\n  Final URL: {page.url}")

        print("\n" + "=" * 60)
        print("DONE! Check your Etsy shop to confirm the listing is live.")
        print("=" * 60)

        await context.close()


if __name__ == "__main__":
    asyncio.run(run())
