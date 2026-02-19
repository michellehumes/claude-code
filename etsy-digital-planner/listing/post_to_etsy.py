#!/usr/bin/env python3
"""
Post the 2026 Wellness & Productivity Digital Planner to Etsy.

SETUP REQUIRED:
1. Create an Etsy developer app at https://www.etsy.com/developers/your-apps
2. Get your API key (keystring) and shared secret
3. Complete OAuth 2.0 flow to get an access token
4. Set environment variables:
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
LISTING_DATA = {
    "title": "Digital Planner 2026 All-in-One Wellness Productivity GoodNotes Notability iPad Hyperlinked",
    "description": """The only planner you need for 2026 -- wellness meets productivity in one beautifully designed digital planner.

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
- Minimalist, clutter-free layouts
- Left sidebar navigation tabs on every page
- Clean typography with clear visual hierarchy
- Landscape orientation for optimal tablet viewing

FULLY HYPERLINKED: Every sidebar tab is clickable. Jump between sections with a single tap.

COMPATIBLE WITH: GoodNotes, Notability, Xodo, Noteshelf, Zinnia, PDF Expert, and any PDF annotation app.

HOW IT WORKS:
1. Purchase and instantly download the PDF file
2. Import into your favorite PDF annotation app
3. Start planning with hyperlinked navigation
4. Write, type, or draw with your stylus

WHAT YOU RECEIVE:
- 1 PDF file (28 pages, fully hyperlinked, landscape A4)
- Instant digital download
- Lifetime access through Etsy purchases

NOTE: Digital product only. No physical item shipped. Designed for tablet PDF apps. No refunds due to digital nature.""",
    "price": 9.97,
    "quantity": 999,
    "taxonomy_id": 6648,  # Digital Planners category
    "who_made": "i_did",
    "when_made": "2020_2025",
    "is_digital": True,
    "tags": [
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
    ],
    "type": "download",
    "shipping_profile_id": None,  # Digital items don't need shipping
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


def upload_listing_video(listing_id, video_path):
    """Upload video to the listing."""
    print(f"  Uploading video: {os.path.basename(video_path)}...")
    url = f"{BASE_URL}/application/shops/{ETSY_SHOP_ID}/listings/{listing_id}/videos"

    with open(video_path, "rb") as f:
        files = {"video": (os.path.basename(video_path), f, "video/mp4")}
        response = requests.post(url, headers=get_headers(), files=files)

    if response.status_code == 201:
        print("    Video uploaded successfully")
        return True
    else:
        print(f"    Error: {response.status_code} - {response.text[:200]}")
        return False


def upload_digital_file(listing_id, file_path):
    """Upload the digital download file."""
    print(f"  Uploading digital file: {os.path.basename(file_path)}...")
    url = f"{BASE_URL}/application/shops/{ETSY_SHOP_ID}/listings/{listing_id}/files"

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/pdf")}
        data = {"name": "2026_Wellness_Productivity_Digital_Planner.pdf"}

        response = requests.post(url, headers=get_headers(), files=files, data=data)

    if response.status_code == 201:
        print("    Digital file uploaded successfully")
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
    print("2026 Wellness & Productivity Digital Planner")
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
    all_files = [PRODUCT_PDF, VIDEO_FILE] + IMAGE_FILES
    for f in all_files:
        if os.path.exists(f):
            size_mb = os.path.getsize(f) / (1024 * 1024)
            print(f"  OK: {os.path.basename(f)} ({size_mb:.1f} MB)")
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
        time.sleep(0.5)  # Rate limiting

    # Step 3: Upload video
    print("\n--- Step 3: Upload Video ---")
    upload_listing_video(listing_id, VIDEO_FILE)

    # Step 4: Upload digital file
    print("\n--- Step 4: Upload Digital File ---")
    upload_digital_file(listing_id, PRODUCT_PDF)

    # Step 5: Publish
    print("\n--- Step 5: Publish Listing ---")
    publish_listing(listing_id)

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"Listing ID: {listing_id}")
    print(f"View at: https://www.etsy.com/listing/{listing_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
