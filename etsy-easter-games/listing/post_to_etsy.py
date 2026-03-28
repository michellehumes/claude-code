#!/usr/bin/env python3
"""
Post the Easter Party Games Bundle to Etsy via API.

SETUP REQUIRED:
1. Set environment variables:
   - ETSY_API_KEY: Your Etsy app API key
   - ETSY_ACCESS_TOKEN: OAuth 2.0 access token
   - ETSY_SHOP_ID: Your Etsy shop ID

Run: python3 post_to_etsy.py
"""

import os
import sys
import json
import requests
import time

# ── Configuration ──
ETSY_API_KEY = os.environ.get("ETSY_API_KEY", "")
ETSY_ACCESS_TOKEN = os.environ.get("ETSY_ACCESS_TOKEN", "")
ETSY_SHOP_ID = os.environ.get("ETSY_SHOP_ID", "")

BASE_URL = "https://openapi.etsy.com/v3"

# ── Files ──
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

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

# ── Listing Data ──
LISTING_DATA = {
    "title": "Easter Games Bundle Printable Easter Party Games for Kids Adults Family Easter Activities Classroom Games Egg Hunt Trivia Instant Download",
    "description": """EASTER PARTY GAMES BUNDLE — 25 Printable Games for the Whole Family

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
A: This bundle includes games for ALL ages! We've included simple activities for kids 3+ (coloring, I Spy, dot-to-dot), challenging word games for older kids and teens, and sophisticated party games adults will love (trivia, Scattergories, Would You Rather).

Q: Can I print these more than once?
A: Absolutely! Print as many copies as you need for your family, classroom, or event. That's the beauty of digital downloads.

Q: What printer do I need?
A: Any standard home printer works. The games look stunning in color but also work great in black & white to save ink.

Q: Can I use these for a school/classroom party?
A: Yes! These are perfect for classroom celebrations. Teachers love them.

Q: Is this a physical product?
A: No, this is a DIGITAL DOWNLOAD. No physical item will be shipped. You'll receive your files immediately after purchase.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLEASE NOTE:
• This is a DIGITAL DOWNLOAD — no physical item will be shipped
• Files are available for download immediately after purchase
• For personal use only — please do not redistribute or resell
• Due to the digital nature of this product, no refunds or exchanges are offered

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Make this Easter one to remember! Download your games bundle now and start the fun.""",
    "price": 7.99,
    "quantity": 999,
    "taxonomy_id": 6648,
    "who_made": "i_did",
    "when_made": "2020_2025",
    "is_digital": True,
    "tags": [
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
    ],
    "type": "download",
    "shipping_profile_id": None,
}


def get_headers():
    return {
        "x-api-key": ETSY_API_KEY,
        "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}",
        "Accept": "application/json",
    }


def create_draft_listing():
    """Create the listing as a draft."""
    print("Creating draft listing...")
    url = f"{BASE_URL}/application/shops/{ETSY_SHOP_ID}/listings"

    payload = {
        "title": LISTING_DATA["title"],
        "description": LISTING_DATA["description"],
        "price": LISTING_DATA["price"],
        "quantity": LISTING_DATA["quantity"],
        "taxonomy_id": LISTING_DATA["taxonomy_id"],
        "who_made": LISTING_DATA["who_made"],
        "when_made": LISTING_DATA["when_made"],
        "is_digital": LISTING_DATA["is_digital"],
        "tags": LISTING_DATA["tags"],
        "type": LISTING_DATA["type"],
    }

    response = requests.post(url, headers=get_headers(), json=payload)

    if response.status_code == 201:
        listing = response.json()
        print(f"  Draft listing created! Listing ID: {listing['listing_id']}")
        return listing["listing_id"]
    else:
        print(f"  Error creating listing: {response.status_code}")
        print(f"  {response.text}")
        return None


def upload_listing_image(listing_id, image_path, rank):
    """Upload an image to the listing."""
    print(f"  Uploading image {rank}: {os.path.basename(image_path)}...")
    url = f"{BASE_URL}/application/shops/{ETSY_SHOP_ID}/listings/{listing_id}/images"

    with open(image_path, "rb") as f:
        files = {"image": (os.path.basename(image_path), f, "image/png")}
        data = {"rank": rank, "overwrite": True}
        response = requests.post(url, headers=get_headers(), files=files, data=data)

    if response.status_code == 201:
        print(f"    Uploaded successfully (rank {rank})")
        return True
    else:
        print(f"    Error: {response.status_code} - {response.text[:200]}")
        return False


def publish_listing(listing_id):
    """Set listing state to active (publish)."""
    print("Publishing listing...")
    url = f"{BASE_URL}/application/shops/{ETSY_SHOP_ID}/listings/{listing_id}"

    payload = {"state": "active"}
    response = requests.put(url, headers=get_headers(), json=payload)

    if response.status_code == 200:
        print("  Listing published successfully!")
        return True
    else:
        print(f"  Error publishing: {response.status_code} - {response.text[:200]}")
        return False


def main():
    print("=" * 60)
    print("ETSY LISTING UPLOADER")
    print("Easter Party Games Bundle")
    print("=" * 60)

    # Validate credentials
    if not all([ETSY_API_KEY, ETSY_ACCESS_TOKEN, ETSY_SHOP_ID]):
        print("\nERROR: Missing Etsy API credentials!")
        print("\nPlease set these environment variables:")
        print("  export ETSY_API_KEY='your-api-key'")
        print("  export ETSY_ACCESS_TOKEN='your-access-token'")
        print("  export ETSY_SHOP_ID='your-shop-id'")
        print("\nTo get these:")
        print("  1. Go to https://www.etsy.com/developers/your-apps")
        print("  2. Create a new app to get your API key")
        print("  3. Complete OAuth 2.0 to get access token")
        print("  4. Find your shop ID in your shop URL or API")
        sys.exit(1)

    # Validate files exist
    print("\nChecking files...")
    for f in IMAGE_FILES:
        if os.path.exists(f):
            size_kb = os.path.getsize(f) / 1024
            print(f"  OK: {os.path.basename(f)} ({size_kb:.0f} KB)")
        else:
            print(f"  MISSING: {f}")
            sys.exit(1)

    # Step 1: Create draft listing
    print("\n--- Step 1: Create Draft Listing ---")
    listing_id = create_draft_listing()
    if not listing_id:
        sys.exit(1)

    # Step 2: Upload images
    print("\n--- Step 2: Upload Images ---")
    for i, img_path in enumerate(IMAGE_FILES):
        upload_listing_image(listing_id, img_path, rank=i + 1)
        time.sleep(0.5)

    # Step 3: Publish
    print("\n--- Step 3: Publish Listing ---")
    publish_listing(listing_id)

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"Listing ID: {listing_id}")
    print(f"View at: https://www.etsy.com/listing/{listing_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
