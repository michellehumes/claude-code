#!/usr/bin/env python3
"""
Create 10 Etsy listing images for the 2026 Meal Planner & Grocery List Bundle.
All images: 2400x2400px, JPG format, warm terracotta/sage theme.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 2400, 2400

# ── Color Palette ──
TERRACOTTA = (196, 113, 59)
SAGE = (143, 174, 139)
CREAM = (255, 248, 240)
SOFT_ORANGE = (244, 164, 96)
WHITE = (255, 255, 255)
CHARCOAL = (68, 68, 68)
SOFT_RED = (212, 114, 106)
DARK_TERRA = (156, 83, 39)
LIGHT_SAGE = (212, 232, 209)
LIGHT_TERRA = (240, 200, 168)
DARK_SAGE = (100, 130, 96)


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill)
        return
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)
    if outline and width:
        # Draw outline arcs and lines
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def centered_text(draw, y, text, font, fill, x_center=W // 2):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x_center - tw // 2, y), text, font=font, fill=fill)


def draw_food_icons(draw, y_start):
    """Draw decorative food-themed elements."""
    # Fork and knife icons (simple geometric)
    icons_data = [
        (200, y_start, "plate"),
        (600, y_start, "fork"),
        (1000, y_start, "leaf"),
        (1400, y_start, "carrot"),
        (1800, y_start, "apple"),
        (2200, y_start, "cup"),
    ]
    for x, y, icon_type in icons_data:
        if icon_type == "plate":
            draw.ellipse([x - 35, y - 35, x + 35, y + 35], outline=SAGE, width=4)
            draw.ellipse([x - 22, y - 22, x + 22, y + 22], outline=SAGE, width=2)
        elif icon_type == "fork":
            draw.line([x, y - 30, x, y + 30], fill=TERRACOTTA, width=4)
            draw.line([x - 10, y - 30, x - 10, y - 5], fill=TERRACOTTA, width=3)
            draw.line([x + 10, y - 30, x + 10, y - 5], fill=TERRACOTTA, width=3)
        elif icon_type == "leaf":
            draw.ellipse([x - 20, y - 28, x + 20, y + 5], fill=SAGE)
            draw.line([x, y + 5, x, y + 30], fill=DARK_SAGE, width=3)
        elif icon_type == "carrot":
            draw.polygon([(x, y - 30), (x - 12, y + 20), (x + 12, y + 20)], fill=SOFT_ORANGE)
            draw.line([x - 5, y - 30, x - 15, y - 40], fill=SAGE, width=3)
            draw.line([x + 5, y - 30, x + 15, y - 40], fill=SAGE, width=3)
        elif icon_type == "apple":
            draw.ellipse([x - 22, y - 20, x + 22, y + 25], fill=SOFT_RED)
            draw.line([x, y - 20, x + 5, y - 32], fill=DARK_TERRA, width=3)
            draw.ellipse([x + 2, y - 35, x + 15, y - 25], fill=SAGE)
        elif icon_type == "cup":
            draw.rectangle([x - 15, y - 20, x + 15, y + 20], outline=TERRACOTTA, width=3)
            draw.arc([x + 15, y - 10, x + 30, y + 10], 270, 90, fill=TERRACOTTA, width=3)


def draw_spreadsheet_mockup(draw, x, y, w, h, title, color, rows=5):
    """Draw a mini spreadsheet mockup."""
    draw_rounded_rect(draw, (x, y, x + w, y + h), 15, WHITE, outline=color, width=3)
    # Title bar
    draw_rounded_rect(draw, (x, y, x + w, y + 50), 15, color)
    draw.rectangle([x, y + 30, x + w, y + 50], fill=color)
    title_font = get_font(24, bold=True)
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw) // 2, y + 12), title, font=title_font, fill=WHITE)
    # Grid lines
    row_h = (h - 60) // rows
    for i in range(rows):
        ry = y + 55 + i * row_h
        draw.line([x + 10, ry, x + w - 10, ry], fill=(*color[:3],), width=1)
        # Fake cells
        for j in range(3):
            cx = x + 20 + j * (w - 40) // 3
            cell_w = (w - 60) // 3
            draw_rounded_rect(draw, (cx, ry + 4, cx + cell_w, ry + row_h - 4), 5,
                              CREAM if i % 2 == 0 else LIGHT_SAGE)


def draw_checkmark(draw, x, y, size, color):
    """Draw a checkmark icon."""
    draw.line([x, y + size * 0.5, x + size * 0.35, y + size], fill=color, width=4)
    draw.line([x + size * 0.35, y + size, x + size, y], fill=color, width=4)


def draw_decorative_border(draw, margin=40, color=TERRACOTTA):
    """Draw a decorative double-line border."""
    draw.rectangle([margin, margin, W - margin, H - margin], outline=color, width=3)
    draw.rectangle([margin + 12, margin + 12, W - margin - 12, H - margin - 12], outline=color, width=1)


def draw_corner_flourishes(draw, color=SAGE):
    """Draw corner decorative elements."""
    size = 80
    positions = [(60, 60), (W - 60, 60), (60, H - 60), (W - 60, H - 60)]
    for px, py in positions:
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=color)
        draw.ellipse([px - 20, py - 20, px + 20, py + 20], outline=color, width=2)


def add_bottom_branding(draw, text="2026 Meal Planner & Grocery List Bundle"):
    """Add consistent bottom branding bar."""
    draw_rounded_rect(draw, (80, H - 120, W - 80, H - 50), 20, TERRACOTTA)
    font = get_font(32, bold=True)
    centered_text(draw, H - 108, text, font, WHITE)


# ═══════════════════════════════════════════════════════════
# IMAGE 1: Hero Image
# ═══════════════════════════════════════════════════════════
def create_image_01_hero():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Background decorative elements
    draw_rounded_rect(draw, (0, 0, W, 350), 0, TERRACOTTA)
    draw_rounded_rect(draw, (0, 330, W, 380), 0, SAGE)

    # Decorative food icons across top
    draw_food_icons(draw, 290)

    # Main content area
    draw_rounded_rect(draw, (120, 440, W - 120, 1550), 40, WHITE, outline=SAGE, width=4)

    # Title
    font_big = get_font(100, bold=True)
    font_med = get_font(64, bold=True)
    font_sub = get_font(48)
    font_year = get_font(140, bold=True)

    centered_text(draw, 100, "2026", font_year, WHITE)
    centered_text(draw, 260, "MEAL PLANNER & GROCERY LIST", get_font(52, bold=True), WHITE)

    # Center content
    centered_text(draw, 490, "Meal Planner &", font_big, TERRACOTTA)
    centered_text(draw, 610, "Grocery List", font_big, TERRACOTTA)
    centered_text(draw, 740, "BUNDLE", font_med, SAGE)

    # Divider
    draw.line([400, 830, W - 400, 830], fill=SOFT_ORANGE, width=4)

    # Feature highlights
    features = [
        "52 Weekly Meal Plans",
        "Monthly Calendars",
        "Recipe Collection Tracker",
        "Grocery Budget Tracker",
        "Pantry Inventory System",
        "Meal Prep Planner",
    ]
    font_feat = get_font(40, bold=False)
    y = 870
    for feat in features:
        draw_checkmark(draw, 500, y + 5, 30, SAGE)
        draw.text((560, y), feat, font=font_feat, fill=CHARCOAL)
        y += 65

    # Divider
    draw.line([400, 1310, W - 400, 1310], fill=SOFT_ORANGE, width=3)

    # Bottom tagline in white box
    font_tag = get_font(36, bold=True)
    centered_text(draw, 1340, "Excel & Google Sheets Compatible", font_tag, TERRACOTTA)
    centered_text(draw, 1400, "Instant Download | Fully Editable", get_font(32), CHARCOAL)
    centered_text(draw, 1460, "Plan  |  Shop  |  Cook  |  Save", get_font(34, bold=True), SAGE)

    # Bottom section with 6 mini spreadsheet previews
    draw_rounded_rect(draw, (80, 1600, W - 80, 2000), 30, WHITE, outline=TERRACOTTA, width=3)
    centered_text(draw, 1615, "6 PROFESSIONAL SPREADSHEETS INCLUDED", get_font(36, bold=True), TERRACOTTA)

    names = ["Weekly\nPlanner", "Monthly\nCalendar", "Recipe\nTracker", "Budget\nTracker", "Pantry\nInventory", "Meal\nPrep"]
    colors = [TERRACOTTA, SAGE, SOFT_ORANGE, DARK_TERRA, DARK_SAGE, SOFT_RED]
    for i, (name, color) in enumerate(zip(names, colors)):
        bx = 150 + i * 360
        draw_rounded_rect(draw, (bx, 1680, bx + 310, 1960), 15, color)
        lines = name.split("\n")
        font_sm = get_font(30, bold=True)
        for li, line in enumerate(lines):
            centered_text(draw, 1780 + li * 40, line, font_sm, WHITE, bx + 155)

    # Food icons at bottom
    draw_food_icons(draw, 2060)
    add_bottom_branding(draw)

    # Corner flourishes
    draw_corner_flourishes(draw, SAGE)

    img.save(os.path.join(OUTPUT_DIR, "01_hero.jpg"), "JPEG", quality=95)
    print("  Saved: 01_hero.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 2: What's Included
# ═══════════════════════════════════════════════════════════
def create_image_02_whats_included():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw, 40, TERRACOTTA)
    draw_corner_flourishes(draw)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 260), 30, TERRACOTTA)
    centered_text(draw, 110, "WHAT'S INCLUDED", get_font(72, bold=True), WHITE)
    centered_text(draw, 200, "6 Professional Spreadsheets", get_font(40), WHITE)

    # 6 items in 2x3 grid
    items = [
        ("Weekly Meal Planner", "52 weekly tabs with meal\ngrids and grocery lists", TERRACOTTA),
        ("Monthly Meal Calendar", "12 monthly dinner\ncalendars with budgets", SAGE),
        ("Recipe Collection", "Track 100+ recipes\nwith ratings & filters", SOFT_ORANGE),
        ("Grocery Budget Tracker", "Monthly spending logs\nwith annual dashboard", DARK_TERRA),
        ("Pantry Inventory", "80+ pre-loaded items\nwith expiry tracking", DARK_SAGE),
        ("Meal Prep Planner", "Prep schedules, batch\ncooking & checklists", SOFT_RED),
    ]

    for i, (title, desc, color) in enumerate(items):
        col = i % 2
        row = i // 2
        bx = 140 + col * 1120
        by = 330 + row * 530

        # Card
        draw_rounded_rect(draw, (bx, by, bx + 1040, by + 480), 25, WHITE, outline=color, width=4)

        # Number badge
        draw_rounded_rect(draw, (bx + 30, by + 20, bx + 120, by + 90), 15, color)
        centered_text(draw, by + 28, str(i + 1), get_font(48, bold=True), WHITE, bx + 75)

        # Icon area
        draw_rounded_rect(draw, (bx + 150, by + 30, bx + 440, by + 200), 15, (*color, ))
        # Mini spreadsheet lines
        for ln in range(5):
            ly = by + 60 + ln * 28
            draw.line([bx + 175, ly, bx + 415, ly], fill=WHITE, width=2)

        # Text
        font_title = get_font(42, bold=True)
        font_desc = get_font(32)
        draw.text((bx + 470, by + 40), title, font=font_title, fill=color)

        # Description lines
        for li, line in enumerate(desc.split("\n")):
            draw.text((bx + 470, by + 100 + li * 42), line, font=font_desc, fill=CHARCOAL)

        # Bottom feature bar
        draw_rounded_rect(draw, (bx + 30, by + 320, bx + 1010, by + 450), 15, LIGHT_SAGE)
        feats = {
            0: "Auto-formulas | Budget tracking | 7-day grid",
            1: "Calendar view | Theme nights | Special occasions",
            2: "100 rows | Category summary | 5-star ratings",
            3: "Category breakdown | Annual charts | Per-trip avg",
            4: "Conditional formatting | Reorder alerts | 80+ items",
            5: "Time blocks | Container labels | Weekly checklist",
        }
        centered_text(draw, by + 355, feats[i], get_font(26, bold=False), CHARCOAL, bx + 520)

    # Bottom
    draw_rounded_rect(draw, (300, H - 220, W - 300, H - 120), 25, SAGE)
    centered_text(draw, H - 205, "All files work with Excel & Google Sheets", get_font(40, bold=True), WHITE)
    centered_text(draw, H - 155, "Instant download  |  Fully editable  |  Print-ready", get_font(30), WHITE)

    img.save(os.path.join(OUTPUT_DIR, "02_whats_included.jpg"), "JPEG", quality=95)
    print("  Saved: 02_whats_included.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 3: Weekly + Monthly Detail
# ═══════════════════════════════════════════════════════════
def create_image_03_weekly_monthly():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 230), 30, TERRACOTTA)
    centered_text(draw, 100, "WEEKLY MEAL PLANNER", get_font(60, bold=True), WHITE)
    centered_text(draw, 175, "+ MONTHLY CALENDAR", get_font(44, bold=True), LIGHT_TERRA)

    # Weekly planner mockup - left side
    draw_rounded_rect(draw, (100, 280, 1160, 1300), 25, WHITE, outline=TERRACOTTA, width=3)
    draw_rounded_rect(draw, (100, 280, 1160, 370), 25, TERRACOTTA)
    draw.rectangle([100, 350, 1160, 370], fill=TERRACOTTA)
    centered_text(draw, 295, "Weekly Meal Planner 2026", get_font(36, bold=True), WHITE, 630)

    # Day headers
    days_short = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(days_short):
        dx = 140 + i * 140
        draw_rounded_rect(draw, (dx, 390, dx + 120, 440), 8, SAGE)
        centered_text(draw, 397, d, get_font(24, bold=True), WHITE, dx + 60)

    # Meal rows
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    for mi, meal in enumerate(meals):
        my = 460 + mi * 90
        draw.text((120, my + 10), meal, font=get_font(22, bold=True), fill=TERRACOTTA)
        for di in range(7):
            cx = 140 + di * 140
            draw_rounded_rect(draw, (cx, my, cx + 120, my + 75), 8, LIGHT_SAGE if mi % 2 == 0 else CREAM)
            # Mini text placeholder lines
            draw.line([cx + 10, my + 25, cx + 110, my + 25], fill=SAGE, width=1)
            draw.line([cx + 10, my + 45, cx + 80, my + 45], fill=SAGE, width=1)

    # Grocery section label
    draw_rounded_rect(draw, (120, 830, 1140, 880), 10, SOFT_ORANGE)
    centered_text(draw, 838, "WEEKLY GROCERY LIST", get_font(28, bold=True), WHITE, 630)

    # Grocery grid
    for i in range(4):
        gy = 895 + i * 45
        draw.line([140, gy, 1120, gy], fill=SAGE, width=1)
        for j in range(4):
            gx = 140 + j * 245
            draw_rounded_rect(draw, (gx + 5, gy + 3, gx + 235, gy + 40), 5, CREAM)

    # Budget total
    draw_rounded_rect(draw, (700, 1080, 1140, 1130), 10, TERRACOTTA)
    centered_text(draw, 1088, "Budget Total: $___.__", get_font(26, bold=True), WHITE, 920)

    # Annotation arrows and labels
    font_ann = get_font(24, bold=True)
    draw_rounded_rect(draw, (100, 1160, 580, 1260), 15, LIGHT_TERRA)
    draw.text((130, 1180), "52 weekly tabs\nfor entire year", font=get_font(28, bold=False), fill=CHARCOAL)

    draw_rounded_rect(draw, (620, 1160, 1160, 1260), 15, LIGHT_SAGE)
    draw.text((650, 1180), "Auto-sum formulas\nfor grocery budget", font=get_font(28, bold=False), fill=CHARCOAL)

    # Monthly calendar mockup - right side / bottom
    draw_rounded_rect(draw, (100, 1310, 2300, 2060), 25, WHITE, outline=SAGE, width=3)
    draw_rounded_rect(draw, (100, 1310, 2300, 1400), 25, SAGE)
    draw.rectangle([100, 1380, 2300, 1400], fill=SAGE)
    centered_text(draw, 1325, "Monthly Meal Calendar 2026", get_font(36, bold=True), WHITE)

    # Calendar day headers
    for i, d in enumerate(days_short):
        dx = 140 + i * 290
        draw_rounded_rect(draw, (dx, 1420, dx + 260, 1470), 8, DARK_SAGE)
        centered_text(draw, 1428, d, get_font(24, bold=True), WHITE, dx + 130)

    # Calendar grid (5 weeks)
    day_num = 1
    for week in range(5):
        for day_col in range(7):
            if week == 0 and day_col < 3:
                continue
            if day_num > 31:
                continue
            cx = 140 + day_col * 290
            cy = 1485 + week * 95
            draw_rounded_rect(draw, (cx, cy, cx + 260, cy + 85), 8, CREAM)
            draw.text((cx + 8, cy + 5), str(day_num), font=get_font(22, bold=True), fill=TERRACOTTA)
            # Dinner placeholder
            draw.line([cx + 15, cy + 40, cx + 200, cy + 40], fill=SAGE, width=1)
            draw.line([cx + 15, cy + 60, cx + 150, cy + 60], fill=SAGE, width=1)
            day_num += 1

    # Side panel indicator
    draw_rounded_rect(draw, (1280, 1310, 2300, 1400), 25, SAGE)
    draw.rectangle([1280, 1380, 2300, 1400], fill=SAGE)

    # Side panel content
    side_x = 2100
    draw_rounded_rect(draw, (side_x - 50, 1420, 2280, 1650), 15, LIGHT_TERRA)
    draw.text((side_x - 30, 1430), "Side Panel:", font=get_font(24, bold=True), fill=TERRACOTTA)
    side_items = ["Meal Prep Notes", "Theme Nights", "Special Occasions", "Budget Tracker"]
    for si, s in enumerate(side_items):
        draw_checkmark(draw, side_x - 30, 1475 + si * 38, 20, SAGE)
        draw.text((side_x + 5, 1470 + si * 38), s, font=get_font(22), fill=CHARCOAL)

    # Bottom annotation
    draw_rounded_rect(draw, (100, 2080, W - 100, 2180), 20, SAGE)
    centered_text(draw, 2095, "12 monthly tabs  |  Dinner calendar layout  |  Theme night planning", get_font(34, bold=True), WHITE)
    centered_text(draw, 2145, "Includes weekly budget tracking for each month", get_font(28), WHITE)

    add_bottom_branding(draw)

    img.save(os.path.join(OUTPUT_DIR, "03_weekly_monthly_detail.jpg"), "JPEG", quality=95)
    print("  Saved: 03_weekly_monthly_detail.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 4: Recipe + Budget Detail
# ═══════════════════════════════════════════════════════════
def create_image_04_recipe_budget():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 230), 30, SOFT_ORANGE)
    centered_text(draw, 100, "RECIPE COLLECTION", get_font(60, bold=True), WHITE)
    centered_text(draw, 175, "+ GROCERY BUDGET TRACKER", get_font(44, bold=True), CREAM)

    # Recipe tracker mockup
    draw_rounded_rect(draw, (100, 280, 2300, 1100), 25, WHITE, outline=SOFT_ORANGE, width=3)
    draw_rounded_rect(draw, (100, 280, 2300, 360), 25, SOFT_ORANGE)
    draw.rectangle([100, 340, 2300, 360], fill=SOFT_ORANGE)
    centered_text(draw, 295, "Recipe Collection Tracker", get_font(36, bold=True), WHITE)

    # Column headers
    recipe_cols = ["Recipe Name", "Category", "Cuisine", "Prep", "Cook", "Servings", "Difficulty", "Rating"]
    col_w = 260
    for i, col in enumerate(recipe_cols):
        cx = 130 + i * col_w
        draw_rounded_rect(draw, (cx, 375, cx + col_w - 10, 420), 8, TERRACOTTA)
        centered_text(draw, 383, col, get_font(22, bold=True), WHITE, cx + col_w // 2 - 5)

    # Sample rows
    sample_recipes = [
        ("Chicken Stir Fry", "Dinner", "Asian", "15", "20", "4", "Easy", "4/5"),
        ("Greek Salad", "Lunch", "Mediterranean", "10", "0", "2", "Easy", "5/5"),
        ("Banana Pancakes", "Breakfast", "American", "5", "15", "4", "Easy", "5/5"),
        ("Beef Tacos", "Dinner", "Mexican", "20", "15", "6", "Medium", "4/5"),
        ("Berry Smoothie", "Snack", "American", "5", "0", "1", "Easy", "4/5"),
    ]

    for ri, recipe in enumerate(sample_recipes):
        ry = 435 + ri * 55
        fill = CREAM if ri % 2 == 0 else LIGHT_SAGE
        draw_rounded_rect(draw, (130, ry, 2270, ry + 48), 8, fill)
        for ci, val in enumerate(recipe):
            cx = 130 + ci * col_w
            draw.text((cx + 15, ry + 12), val, font=get_font(22), fill=CHARCOAL)

    # Star ratings visualization
    for ri in range(5):
        ry = 435 + ri * 55
        rx = 130 + 7 * col_w + 15
        stars = int(sample_recipes[ri][7][0])
        for s in range(5):
            color = SOFT_ORANGE if s < stars else (220, 220, 220)
            draw.text((rx + s * 25, ry + 10), "*", font=get_font(26, bold=True), fill=color)

    # Feature callouts
    draw_rounded_rect(draw, (130, 730, 750, 850), 15, LIGHT_TERRA)
    draw.text((160, 748), "100 Pre-formatted Rows", font=get_font(30, bold=True), fill=TERRACOTTA)
    draw.text((160, 790), "Ready for your favorite recipes", font=get_font(24), fill=CHARCOAL)

    draw_rounded_rect(draw, (790, 730, 1500, 850), 15, LIGHT_SAGE)
    draw.text((820, 748), "Category Summary Tab", font=get_font(30, bold=True), fill=DARK_SAGE)
    draw.text((820, 790), "Auto-counts by category", font=get_font(24), fill=CHARCOAL)

    draw_rounded_rect(draw, (1540, 730, 2270, 850), 15, LIGHT_TERRA)
    draw.text((1570, 748), "Favorites Filter", font=get_font(30, bold=True), fill=TERRACOTTA)
    draw.text((1570, 790), "Quick access to 5-star recipes", font=get_font(24), fill=CHARCOAL)

    # Category summary mini chart
    draw_rounded_rect(draw, (130, 880, 2270, 1070), 15, WHITE, outline=SAGE, width=2)
    cats = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"]
    cat_counts = [12, 15, 25, 8, 10]
    max_count = max(cat_counts)
    centered_text(draw, 890, "Category Summary", get_font(28, bold=True), SAGE)
    for ci, (cat, count) in enumerate(zip(cats, cat_counts)):
        bx = 200 + ci * 400
        bar_h = int(count / max_count * 100)
        draw_rounded_rect(draw, (bx, 1040 - bar_h, bx + 200, 1040), 8, SAGE if ci % 2 == 0 else TERRACOTTA)
        centered_text(draw, 1045, cat, get_font(20), fill=CHARCOAL, x_center=bx + 100)
        centered_text(draw, 1040 - bar_h - 25, str(count), get_font(20, bold=True), fill=CHARCOAL, x_center=bx + 100)

    # Budget tracker mockup
    draw_rounded_rect(draw, (100, 1140, 2300, 2060), 25, WHITE, outline=DARK_TERRA, width=3)
    draw_rounded_rect(draw, (100, 1140, 2300, 1230), 25, DARK_TERRA)
    draw.rectangle([100, 1210, 2300, 1230], fill=DARK_TERRA)
    centered_text(draw, 1155, "Grocery Budget Tracker 2026", get_font(36, bold=True), WHITE)
    centered_text(draw, 1200, "Monthly tabs + Annual Dashboard", get_font(26), LIGHT_TERRA)

    # Monthly spending bars
    months_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    amounts = [320, 290, 350, 310, 280, 340, 300, 330, 285, 310, 360, 400]
    max_amt = max(amounts)

    draw_rounded_rect(draw, (130, 1260, 2270, 1700), 15, LIGHT_SAGE)
    centered_text(draw, 1270, "Monthly Spending Overview", get_font(28, bold=True), DARK_SAGE)

    for i, (m, amt) in enumerate(zip(months_short, amounts)):
        bx = 180 + i * 170
        bar_h = int(amt / max_amt * 300)
        color = TERRACOTTA if i % 2 == 0 else SAGE
        draw_rounded_rect(draw, (bx, 1660 - bar_h, bx + 130, 1660), 8, color)
        centered_text(draw, 1665, m, get_font(18, bold=True), fill=CHARCOAL, x_center=bx + 65)
        centered_text(draw, 1660 - bar_h - 25, f"${amt}", get_font(16), fill=CHARCOAL, x_center=bx + 65)

    # Category breakdown section
    draw_rounded_rect(draw, (130, 1730, 1100, 2030), 15, WHITE, outline=TERRACOTTA, width=2)
    centered_text(draw, 1740, "Category Breakdown", get_font(26, bold=True), TERRACOTTA, 615)
    cat_spend = [("Produce", "$85"), ("Dairy", "$45"), ("Meat/Protein", "$95"), ("Pantry", "$55"), ("Frozen", "$30"), ("Other", "$40")]
    for ci, (cat, amt) in enumerate(cat_spend):
        cy = 1785 + ci * 38
        draw.text((170, cy), cat, font=get_font(22), fill=CHARCOAL)
        draw.text((520, cy), amt, font=get_font(22, bold=True), fill=TERRACOTTA)
        # Progress bar
        bar_w = int(int(amt.replace("$", "")) / 100 * 400)
        draw_rounded_rect(draw, (620, cy + 3, 620 + bar_w, cy + 28), 6, SAGE)

    # Annual summary
    draw_rounded_rect(draw, (1140, 1730, 2270, 2030), 15, WHITE, outline=SAGE, width=2)
    centered_text(draw, 1740, "Annual Summary", get_font(26, bold=True), DARK_SAGE, 1705)
    summary_items = [
        ("Annual Total:", "$3,875"),
        ("Monthly Average:", "$323"),
        ("Highest Month:", "$400 (Dec)"),
        ("Lowest Month:", "$280 (May)"),
        ("Avg Per Trip:", "$76"),
    ]
    for si, (label, val) in enumerate(summary_items):
        sy = 1790 + si * 45
        draw.text((1180, sy), label, font=get_font(24), fill=CHARCOAL)
        draw.text((1700, sy), val, font=get_font(24, bold=True), fill=TERRACOTTA)

    add_bottom_branding(draw)

    img.save(os.path.join(OUTPUT_DIR, "04_recipe_budget_detail.jpg"), "JPEG", quality=95)
    print("  Saved: 04_recipe_budget_detail.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 5: Pantry + Meal Prep Detail
# ═══════════════════════════════════════════════════════════
def create_image_05_pantry_mealprep():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 230), 30, DARK_SAGE)
    centered_text(draw, 100, "PANTRY INVENTORY", get_font(60, bold=True), WHITE)
    centered_text(draw, 175, "+ MEAL PREP PLANNER", get_font(44, bold=True), LIGHT_SAGE)

    # Pantry inventory mockup
    draw_rounded_rect(draw, (100, 280, 2300, 1100), 25, WHITE, outline=DARK_SAGE, width=3)
    draw_rounded_rect(draw, (100, 280, 2300, 360), 25, DARK_SAGE)
    draw.rectangle([100, 340, 2300, 360], fill=DARK_SAGE)
    centered_text(draw, 295, "Pantry Inventory Tracker", get_font(36, bold=True), WHITE)

    # Column headers
    pantry_cols = ["Item Name", "Category", "Qty", "Unit", "Expiry", "Location", "Reorder", "Notes"]
    col_w = 260
    for i, col in enumerate(pantry_cols):
        cx = 130 + i * col_w
        draw_rounded_rect(draw, (cx, 375, cx + col_w - 10, 420), 8, SAGE)
        centered_text(draw, 383, col, get_font(22, bold=True), WHITE, cx + col_w // 2 - 5)

    # Sample rows
    sample_items = [
        ("Olive Oil", "Oils", "1", "bottle", "", "Pantry", "N", "Extra virgin"),
        ("Eggs", "Dairy", "1", "dozen", "02/25", "Fridge", "Y", "Large"),
        ("Chicken Breast", "Protein", "2", "lb", "02/20", "Freezer", "N", "Boneless"),
        ("Brown Rice", "Grains", "1", "bag", "", "Pantry", "N", ""),
        ("Greek Yogurt", "Dairy", "3", "cup", "02/22", "Fridge", "Y", "Plain"),
        ("Canned Tomatoes", "Canned", "4", "can", "12/26", "Pantry", "N", "Diced"),
    ]

    for ri, item in enumerate(sample_items):
        ry = 435 + ri * 55
        fill = CREAM if ri % 2 == 0 else LIGHT_SAGE
        draw_rounded_rect(draw, (130, ry, 2270, ry + 48), 8, fill)
        for ci, val in enumerate(item):
            cx = 130 + ci * col_w
            color = CHARCOAL
            if ci == 6 and val == "Y":
                color = SOFT_RED
            elif ci == 4 and val == "02/20":
                color = SOFT_RED  # Expired/expiring
            draw.text((cx + 15, ry + 12), val, font=get_font(22), fill=color)

    # Feature highlights
    feat_y = 790
    features_pantry = [
        ("80+ Pre-loaded Items", "Common pantry staples\nalready entered", TERRACOTTA),
        ("Expiry Tracking", "Color coding for items\napproaching expiration", SOFT_RED),
        ("Shopping List Generator", "Auto-generates list from\nreorder column", SAGE),
    ]
    for fi, (title, desc, color) in enumerate(features_pantry):
        fx = 150 + fi * 720
        draw_rounded_rect(draw, (fx, feat_y, fx + 660, feat_y + 160), 15, WHITE, outline=color, width=3)
        draw_rounded_rect(draw, (fx, feat_y, fx + 660, feat_y + 50), 15, color)
        draw.rectangle([fx, feat_y + 30, fx + 660, feat_y + 50], fill=color)
        centered_text(draw, feat_y + 10, title, get_font(26, bold=True), WHITE, fx + 330)
        for li, line in enumerate(desc.split("\n")):
            centered_text(draw, feat_y + 65 + li * 35, line, get_font(24), CHARCOAL, fx + 330)

    # Shopping list preview
    draw_rounded_rect(draw, (130, 980, 2270, 1070), 15, LIGHT_TERRA)
    centered_text(draw, 995, "Shopping List Generator: Auto-shows items marked for reorder  |  Export-ready for grocery trips", get_font(26, bold=True), TERRACOTTA)
    centered_text(draw, 1035, "Never forget an item again!", get_font(24), CHARCOAL)

    # Meal prep planner mockup
    draw_rounded_rect(draw, (100, 1140, 2300, 2060), 25, WHITE, outline=SOFT_RED, width=3)
    draw_rounded_rect(draw, (100, 1140, 2300, 1230), 25, SOFT_RED)
    draw.rectangle([100, 1210, 2300, 1230], fill=SOFT_RED)
    centered_text(draw, 1155, "Meal Prep Planner", get_font(36, bold=True), WHITE)
    centered_text(draw, 1200, "4 organized tabs for efficient meal prep", get_font(26), LIGHT_TERRA)

    # Four tabs preview
    tabs = [
        ("Prep Day Schedule", "Time blocks for\nefficient cooking", [
            "8:00 AM - Gather ingredients",
            "8:30 AM - Chop vegetables",
            "9:00 AM - Cook grains",
            "9:30 AM - Cook proteins",
        ]),
        ("Batch Cooking", "Track what you made\nand storage info", [
            "Recipe: Chicken Stir Fry",
            "Servings: 8 portions",
            "Storage: Glass containers",
            "Use By: Feb 25, 2026",
        ]),
        ("Container Labels", "Print and label\nyour meal prep", [
            "Meal: Chicken Stir Fry",
            "Date: Feb 19, 2026",
            "Reheat: Microwave 3 min",
            "Servings: 1",
        ]),
        ("Weekly Checklist", "Step-by-step prep\nday guide", [
            "[ ] Review meal plan",
            "[ ] Check pantry",
            "[ ] Go grocery shopping",
            "[ ] Prep all meals",
        ]),
    ]

    for ti, (tab_title, tab_desc, tab_items) in enumerate(tabs):
        tx = 140 + ti * 540
        ty = 1260
        tw = 500

        # Tab header
        tab_colors = [TERRACOTTA, SAGE, SOFT_ORANGE, DARK_SAGE]
        draw_rounded_rect(draw, (tx, ty, tx + tw, ty + 50), 12, tab_colors[ti])
        centered_text(draw, ty + 10, tab_title, get_font(24, bold=True), WHITE, tx + tw // 2)

        # Tab content area
        draw_rounded_rect(draw, (tx, ty + 50, tx + tw, ty + 500), 0, WHITE, outline=tab_colors[ti], width=2)

        # Description
        for li, line in enumerate(tab_desc.split("\n")):
            centered_text(draw, ty + 65 + li * 30, line, get_font(20), CHARCOAL, tx + tw // 2)

        # Items
        for ii, item in enumerate(tab_items):
            draw.text((tx + 20, ty + 140 + ii * 70), item, font=get_font(20), fill=CHARCOAL)
            draw.line([tx + 20, ty + 170 + ii * 70, tx + tw - 20, ty + 170 + ii * 70], fill=SAGE, width=1)

    # Bottom summary
    draw_rounded_rect(draw, (130, 1810, 2270, 2030), 15, LIGHT_SAGE)
    centered_text(draw, 1830, "Your Complete Meal Prep Workflow", get_font(34, bold=True), DARK_SAGE)
    steps = ["Plan Meals", "Check Pantry", "Shop Groceries", "Prep & Cook", "Store & Label"]
    for si, step in enumerate(steps):
        sx = 200 + si * 400
        draw_rounded_rect(draw, (sx, 1890, sx + 320, 1960), 15, SAGE if si % 2 == 0 else TERRACOTTA)
        centered_text(draw, 1905, step, get_font(24, bold=True), WHITE, sx + 160)
        if si < len(steps) - 1:
            draw.text((sx + 340, 1900), "->", font=get_font(30, bold=True), fill=CHARCOAL)

    centered_text(draw, 1980, "Everything connected for seamless meal planning!", get_font(28), CHARCOAL)

    add_bottom_branding(draw)

    img.save(os.path.join(OUTPUT_DIR, "05_pantry_mealprep_detail.jpg"), "JPEG", quality=95)
    print("  Saved: 05_pantry_mealprep_detail.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 6: Key Features
# ═══════════════════════════════════════════════════════════
def create_image_06_features():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw, 40, SAGE)
    draw_corner_flourishes(draw, TERRACOTTA)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 260), 30, SAGE)
    centered_text(draw, 100, "KEY FEATURES", get_font(80, bold=True), WHITE)
    centered_text(draw, 200, "Everything you need for organized meal planning", get_font(36), LIGHT_SAGE)

    # Feature cards in 3x3 grid
    features = [
        ("52 Weekly Plans", "Complete year of meal\nplanning with Mon-Sun\ngrids for every week", TERRACOTTA, "52"),
        ("12 Monthly Views", "Calendar-style dinner\nplanning with theme\nnights and budgets", SAGE, "12"),
        ("100+ Recipe Slots", "Track your favorite\nrecipes with ratings\nand cook times", SOFT_ORANGE, "100+"),
        ("Auto Formulas", "Budget totals, averages\nand summaries calculate\nautomatically", DARK_TERRA, "fx"),
        ("Budget Tracking", "Monthly grocery spending\nwith annual dashboard\nand category breakdown", DARK_SAGE, "$"),
        ("80+ Pantry Items", "Pre-loaded inventory\nwith expiration tracking\nand reorder alerts", SOFT_RED, "80+"),
        ("Meal Prep Tools", "Prep schedules, batch\ncooking tracker and\ncontainer labels", TERRACOTTA, "PREP"),
        ("Frozen Panes", "Headers stay visible\nwhile scrolling through\nyour data", SAGE, "PIN"),
        ("Print Ready", "Professional formatting\ndesigned for both\nscreen and print", SOFT_ORANGE, "PRINT"),
    ]

    for i, (title, desc, color, badge) in enumerate(features):
        col = i % 3
        row = i // 3
        fx = 120 + col * 740
        fy = 320 + row * 560

        # Card background
        draw_rounded_rect(draw, (fx, fy, fx + 690, fy + 510), 25, WHITE, outline=color, width=3)

        # Badge circle
        draw.ellipse([fx + 260, fy + 20, fx + 430, fy + 160], fill=color)
        badge_font = get_font(40 if len(badge) <= 3 else 30, bold=True)
        centered_text(draw, fy + 55 if len(badge) <= 3 else fy + 62, badge, badge_font, WHITE, fx + 345)

        # Title
        centered_text(draw, fy + 185, title, get_font(36, bold=True), color, fx + 345)

        # Divider
        draw.line([fx + 100, fy + 240, fx + 590, fy + 240], fill=color, width=2)

        # Description
        for li, line in enumerate(desc.split("\n")):
            centered_text(draw, fy + 265 + li * 42, line, get_font(28), CHARCOAL, fx + 345)

        # Bottom accent
        draw_rounded_rect(draw, (fx + 50, fy + 430, fx + 640, fy + 480), 12, (*color,))
        centered_text(draw, fy + 440, ["Weekly", "Monthly", "Recipes", "Smart", "Budget", "Inventory",
                                        "Prep", "Organized", "Quality"][i],
                      get_font(24, bold=True), WHITE, fx + 345)

    add_bottom_branding(draw)

    img.save(os.path.join(OUTPUT_DIR, "06_key_features.jpg"), "JPEG", quality=95)
    print("  Saved: 06_key_features.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 7: How to Use / Workflow
# ═══════════════════════════════════════════════════════════
def create_image_07_workflow():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw, 40, TERRACOTTA)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 280), 30, TERRACOTTA)
    centered_text(draw, 100, "HOW TO USE", get_font(72, bold=True), WHITE)
    centered_text(draw, 190, "Your Complete Meal Prep Workflow", get_font(40), LIGHT_TERRA)

    # Step 1
    steps = [
        ("1", "PLAN YOUR MEALS", "Open the Weekly Meal Planner and fill in\nBreakfast, Lunch, Dinner, and Snacks\nfor each day of the week.", TERRACOTTA,
         ["Choose recipes from your Recipe Tracker", "Set theme nights for easy planning", "Note prep times for busy days"]),
        ("2", "BUILD YOUR GROCERY LIST", "Use the grocery section at the bottom of\neach weekly tab to list everything you need.\nThe budget auto-calculates!", SAGE,
         ["Organize by category (Produce, Dairy, etc.)", "Estimate costs to stay on budget", "Check Pantry Inventory first"]),
        ("3", "TRACK YOUR BUDGET", "Log every grocery trip in the Budget Tracker.\nMonthly totals and annual dashboard\nshow your spending trends.", SOFT_ORANGE,
         ["Record date, store, and amount", "See category breakdowns", "Compare month-to-month spending"]),
        ("4", "PREP & COOK", "Use the Meal Prep Planner for efficient\nbatch cooking. Follow the time-block\nschedule for organized prep days.", DARK_SAGE,
         ["Follow the prep day schedule", "Track batch cooking portions", "Label containers with dates"]),
        ("5", "MAINTAIN INVENTORY", "Keep your Pantry Tracker updated as you\nuse items. Mark items for reorder and\nnever run out of essentials.", SOFT_RED,
         ["Update quantities weekly", "Watch for expiring items", "Auto-generate shopping lists"]),
    ]

    for si, (num, title, desc, color, bullets) in enumerate(steps):
        sy = 340 + si * 395

        # Step number circle
        draw.ellipse([120, sy, 240, sy + 120], fill=color)
        centered_text(draw, sy + 20, num, get_font(64, bold=True), WHITE, 180)

        # Connector line
        if si < len(steps) - 1:
            draw.line([180, sy + 120, 180, sy + 395], fill=color, width=4)

        # Content card
        draw_rounded_rect(draw, (280, sy, 2300, sy + 350), 20, WHITE, outline=color, width=3)

        # Title bar
        draw_rounded_rect(draw, (280, sy, 2300, sy + 65), 20, color)
        draw.rectangle([280, sy + 45, 2300, sy + 65], fill=color)
        draw.text((320, sy + 12), title, font=get_font(38, bold=True), fill=WHITE)

        # Description
        for li, line in enumerate(desc.split("\n")):
            draw.text((320, sy + 85 + li * 35), line, font=get_font(28), fill=CHARCOAL)

        # Bullets on right side
        for bi, bullet in enumerate(bullets):
            bx = 1300
            by = sy + 85 + bi * 50
            draw_checkmark(draw, bx, by + 5, 25, color)
            draw.text((bx + 40, by), bullet, font=get_font(26), fill=CHARCOAL)

    # Bottom
    draw_rounded_rect(draw, (200, H - 190, W - 200, H - 80), 25, SAGE)
    centered_text(draw, H - 175, "Repeat weekly for organized, stress-free meal planning all year!", get_font(36, bold=True), WHITE)
    centered_text(draw, H - 120, "All 6 spreadsheets work together seamlessly", get_font(28), WHITE)

    img.save(os.path.join(OUTPUT_DIR, "07_how_to_use.jpg"), "JPEG", quality=95)
    print("  Saved: 07_how_to_use.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 8: Compatibility
# ═══════════════════════════════════════════════════════════
def create_image_08_compatibility():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw, 40, SAGE)
    draw_corner_flourishes(draw, TERRACOTTA)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 280), 30, SAGE)
    centered_text(draw, 100, "WORKS WITH YOUR", get_font(60, bold=True), WHITE)
    centered_text(draw, 180, "FAVORITE SPREADSHEET APP", get_font(54, bold=True), WHITE)

    # Excel section
    draw_rounded_rect(draw, (120, 340, 1150, 1100), 30, WHITE, outline=DARK_SAGE, width=4)

    # Excel icon
    draw_rounded_rect(draw, (420, 380, 850, 570), 20, (33, 115, 70))  # Excel green
    centered_text(draw, 410, "EXCEL", get_font(72, bold=True), WHITE, 635)
    centered_text(draw, 500, ".XLSX", get_font(36), (200, 255, 200), 635)

    centered_text(draw, 610, "Microsoft Excel", get_font(44, bold=True), DARK_SAGE, 635)
    centered_text(draw, 670, "Desktop & Online", get_font(32), CHARCOAL, 635)

    excel_features = [
        "All formulas work perfectly",
        "Conditional formatting preserved",
        "Charts and graphs included",
        "Frozen panes for easy navigation",
        "Print-optimized layouts",
        "Works with Excel 2016+",
    ]
    for fi, feat in enumerate(excel_features):
        fy = 740 + fi * 50
        draw_checkmark(draw, 250, fy + 5, 25, DARK_SAGE)
        draw.text((290, fy), feat, font=get_font(30), fill=CHARCOAL)

    # Google Sheets section
    draw_rounded_rect(draw, (1250, 340, 2280, 1100), 30, WHITE, outline=TERRACOTTA, width=4)

    # Google icon
    colors_g = [(66, 133, 244), (234, 67, 53), (251, 188, 4), (52, 168, 83)]
    draw_rounded_rect(draw, (1550, 380, 1980, 570), 20, (66, 133, 244))
    centered_text(draw, 410, "GOOGLE", get_font(60, bold=True), WHITE, 1765)
    centered_text(draw, 500, "SHEETS", get_font(36), (200, 220, 255), 1765)

    centered_text(draw, 610, "Google Sheets", get_font(44, bold=True), TERRACOTTA, 1765)
    centered_text(draw, 670, "Free & Cloud-Based", get_font(32), CHARCOAL, 1765)

    sheets_features = [
        "Upload .xlsx directly",
        "All formulas auto-convert",
        "Access from any device",
        "Share with family members",
        "Real-time collaboration",
        "Works with any Google account",
    ]
    for fi, feat in enumerate(sheets_features):
        fy = 740 + fi * 50
        draw_checkmark(draw, 1380, fy + 5, 25, TERRACOTTA)
        draw.text((1420, fy), feat, font=get_font(30), fill=CHARCOAL)

    # Also works with section
    draw_rounded_rect(draw, (120, 1160, 2280, 1400), 30, LIGHT_SAGE, outline=SAGE, width=2)
    centered_text(draw, 1180, "ALSO COMPATIBLE WITH", get_font(40, bold=True), DARK_SAGE)

    others = ["LibreOffice Calc", "Apple Numbers", "WPS Office", "OnlyOffice"]
    for oi, other in enumerate(others):
        ox = 250 + oi * 530
        draw_rounded_rect(draw, (ox, 1250, ox + 440, 1340), 20, WHITE, outline=SAGE, width=2)
        centered_text(draw, 1270, other, get_font(30, bold=True), CHARCOAL, ox + 220)

    # How to open section
    draw_rounded_rect(draw, (120, 1460, 2280, 2050), 30, WHITE, outline=TERRACOTTA, width=3)
    centered_text(draw, 1480, "HOW TO OPEN YOUR FILES", get_font(44, bold=True), TERRACOTTA)

    how_steps = [
        ("1", "Download", "Download the .xlsx files\nfrom your Etsy purchase", TERRACOTTA),
        ("2", "Open", "Double-click to open in Excel\nor upload to Google Drive", SAGE),
        ("3", "Customize", "Start filling in your meals,\nrecipes, and grocery lists", SOFT_ORANGE),
        ("4", "Enjoy!", "Use all year for organized\nmeal planning & budgeting", DARK_SAGE),
    ]

    for si, (num, title, desc, color) in enumerate(how_steps):
        sx = 180 + si * 530
        # Step circle
        draw.ellipse([sx + 150, 1560, sx + 260, 1670], fill=color)
        centered_text(draw, 1580, num, get_font(56, bold=True), WHITE, sx + 205)
        # Title
        centered_text(draw, 1690, title, get_font(34, bold=True), color, sx + 205)
        # Description
        for li, line in enumerate(desc.split("\n")):
            centered_text(draw, 1745 + li * 38, line, get_font(24), CHARCOAL, sx + 205)

        # Arrow
        if si < 3:
            draw.text((sx + 430, 1600), "->", font=get_font(50, bold=True), fill=CHARCOAL)

    # Instant download badge
    draw_rounded_rect(draw, (700, 1890, 1700, 2010), 25, TERRACOTTA)
    centered_text(draw, 1910, "INSTANT DIGITAL DOWNLOAD", get_font(42, bold=True), WHITE)
    centered_text(draw, 1960, "No waiting! Start planning today", get_font(28), LIGHT_TERRA)

    add_bottom_branding(draw)

    img.save(os.path.join(OUTPUT_DIR, "08_compatibility.jpg"), "JPEG", quality=95)
    print("  Saved: 08_compatibility.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 9: Testimonials
# ═══════════════════════════════════════════════════════════
def create_image_09_testimonials():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw, 40, TERRACOTTA)
    draw_corner_flourishes(draw, SAGE)

    # Header
    draw_rounded_rect(draw, (100, 80, W - 100, 280), 30, TERRACOTTA)
    centered_text(draw, 100, "WHAT CUSTOMERS SAY", get_font(68, bold=True), WHITE)

    # Star rating
    for s in range(5):
        draw.text((960 + s * 60, 195), "*", font=get_font(50, bold=True), fill=SOFT_ORANGE)

    centered_text(draw, 210, "                                 4.9 / 5 Stars", get_font(32, bold=True), WHITE)

    # Testimonial cards
    testimonials = [
        ("Sarah M.", "Busy Mom of 3",
         "This bundle has completely transformed how I plan our family meals. The weekly planner is so easy to use, and the grocery list section saves me SO much time at the store!",
         TERRACOTTA),
        ("Jennifer K.", "Budget-Conscious Cook",
         "The budget tracker is a game-changer! I had no idea how much I was spending on groceries until I started tracking. I've saved over $200/month since using these spreadsheets.",
         SAGE),
        ("Amanda T.", "Meal Prep Enthusiast",
         "Finally, a meal prep planner that actually works! The container labels and batch cooking tracker make Sunday prep days so organized. Worth every penny!",
         SOFT_ORANGE),
        ("Rachel D.", "Working Professional",
         "As someone who works long hours, having my meals planned and prepped saves me from ordering takeout every night. The recipe tracker helps me rotate through favorites.",
         DARK_SAGE),
        ("Michelle L.", "Health-Focused Planner",
         "I love that this has everything in one bundle - meal planning, grocery lists, budget tracking, AND pantry inventory. No more juggling multiple apps and notebooks!",
         SOFT_RED),
    ]

    for ti, (name, title, review, color) in enumerate(testimonials):
        ty = 340 + ti * 365
        # Card
        draw_rounded_rect(draw, (140, ty, 2260, ty + 320), 25, WHITE, outline=color, width=3)

        # Quote mark
        draw.text((180, ty + 10), '"', font=get_font(80, bold=True), fill=color)

        # Review text
        # Word wrap manually
        words = review.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=get_font(28))
            if bbox[2] - bbox[0] > 1800:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        for li, line in enumerate(lines):
            draw.text((260, ty + 30 + li * 40), line, font=get_font(28), fill=CHARCOAL)

        # Stars
        star_y = ty + 30 + len(lines) * 40 + 10
        for s in range(5):
            draw.text((260 + s * 40, star_y), "*", font=get_font(34, bold=True), fill=SOFT_ORANGE)

        # Name and title
        draw_rounded_rect(draw, (600, star_y - 5, 1200, star_y + 45), 12, color)
        draw.text((620, star_y), f"{name}  |  {title}", font=get_font(26, bold=True), fill=WHITE)

    # Bottom CTA
    draw_rounded_rect(draw, (300, H - 220, W - 300, H - 80), 30, SAGE)
    centered_text(draw, H - 205, "Join thousands of happy meal planners!", get_font(42, bold=True), WHITE)
    centered_text(draw, H - 145, "Start your organized kitchen journey today", get_font(30), WHITE)

    img.save(os.path.join(OUTPUT_DIR, "09_testimonials.jpg"), "JPEG", quality=95)
    print("  Saved: 09_testimonials.jpg")


# ═══════════════════════════════════════════════════════════
# IMAGE 10: Bundle CTA
# ═══════════════════════════════════════════════════════════
def create_image_10_cta():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Full background design
    draw_rounded_rect(draw, (0, 0, W, 400), 0, TERRACOTTA)
    draw_rounded_rect(draw, (0, 380, W, 420), 0, SAGE)

    # Decorative food icons
    draw_food_icons(draw, 350)

    # Main card
    draw_rounded_rect(draw, (100, 460, W - 100, 2100), 40, WHITE, outline=TERRACOTTA, width=5)

    # Title
    centered_text(draw, 80, "COMPLETE MEAL PLANNING", get_font(60, bold=True), WHITE)
    centered_text(draw, 160, "BUNDLE FOR 2026", get_font(72, bold=True), WHITE)
    centered_text(draw, 260, "Everything you need in one bundle", get_font(36), LIGHT_TERRA)
    centered_text(draw, 310, "Plan  |  Shop  |  Cook  |  Save", get_font(32, bold=True), LIGHT_TERRA)

    # Price section
    draw_rounded_rect(draw, (600, 510, 1800, 750), 30, TERRACOTTA)
    centered_text(draw, 530, "SPECIAL BUNDLE PRICE", get_font(40, bold=True), WHITE)

    # Crossed out original price
    orig_text = "$24.99"
    centered_text(draw, 610, orig_text, get_font(48), (200, 170, 160))
    bbox = draw.textbbox((0, 0), orig_text, font=get_font(48))
    tw = bbox[2] - bbox[0]
    cx = W // 2 - tw // 2
    draw.line([cx - 5, 640, cx + tw + 5, 640], fill=WHITE, width=3)

    # Actual price
    centered_text(draw, 660, "$9.99", get_font(64, bold=True), WHITE)

    # Savings badge
    draw_rounded_rect(draw, (1600, 510, 1790, 580), 15, SOFT_ORANGE)
    centered_text(draw, 525, "60% OFF", get_font(30, bold=True), WHITE, 1695)

    # What you get
    centered_text(draw, 790, "6 PROFESSIONAL SPREADSHEETS", get_font(44, bold=True), TERRACOTTA)
    draw.line([500, 850, W - 500, 850], fill=SAGE, width=3)

    included = [
        ("Weekly Meal Planner", "52 weekly tabs for all of 2026"),
        ("Monthly Meal Calendar", "12 monthly dinner calendars"),
        ("Recipe Collection Tracker", "Track 100+ recipes with ratings"),
        ("Grocery Budget Tracker", "Monthly logs + annual dashboard"),
        ("Pantry Inventory Tracker", "80+ pre-loaded items"),
        ("Meal Prep Planner", "Schedules, labels & checklists"),
    ]

    for ii, (item_name, item_desc) in enumerate(included):
        iy = 880 + ii * 80
        draw_checkmark(draw, 350, iy + 10, 30, SAGE)
        draw.text((410, iy), item_name, font=get_font(34, bold=True), fill=CHARCOAL)
        draw.text((1100, iy + 5), item_desc, font=get_font(28), fill=CHARCOAL)

    # Features strip
    draw_rounded_rect(draw, (200, 1380, W - 200, 1500), 20, LIGHT_SAGE)
    features_str = [
        "Instant Download", "Fully Editable", "Excel + Google Sheets",
        "Auto Formulas", "Print Ready"
    ]
    for fi, feat in enumerate(features_str):
        fx = 250 + fi * 400
        draw_rounded_rect(draw, (fx, 1400, fx + 350, 1470), 15, SAGE)
        centered_text(draw, 1415, feat, get_font(24, bold=True), WHITE, fx + 175)

    # Bonus section
    draw_rounded_rect(draw, (200, 1540, W - 200, 1750), 25, LIGHT_TERRA)
    centered_text(draw, 1555, "BONUS FEATURES INCLUDED", get_font(38, bold=True), TERRACOTTA)
    bonuses = [
        "Frozen headers for easy scrolling",
        "Pre-formatted cells with professional styling",
        "Instructions tab in every spreadsheet",
        "80+ pre-loaded pantry items",
    ]
    for bi, bonus in enumerate(bonuses):
        bx = 300 if bi < 2 else 1250
        by = 1615 + (bi % 2) * 50
        draw_checkmark(draw, bx, by + 5, 25, TERRACOTTA)
        draw.text((bx + 40, by), bonus, font=get_font(28), fill=CHARCOAL)

    # Final CTA
    draw_rounded_rect(draw, (400, 1800, W - 400, 1940), 30, TERRACOTTA)
    centered_text(draw, 1815, "GET YOUR BUNDLE NOW", get_font(52, bold=True), WHITE)
    centered_text(draw, 1885, "Only $9.99  |  Instant Download", get_font(34), LIGHT_TERRA)

    # Guarantee
    draw_rounded_rect(draw, (500, 1970, W - 500, 2070), 20, SAGE)
    centered_text(draw, 1988, "100% Satisfaction Guaranteed", get_font(36, bold=True), WHITE)
    centered_text(draw, 2030, "Digital download - no refunds, but we'll make it right!", get_font(24), WHITE)

    # Bottom
    add_bottom_branding(draw, "Start your organized kitchen journey today!")

    # Corner flourishes
    draw_corner_flourishes(draw, SAGE)

    img.save(os.path.join(OUTPUT_DIR, "10_bundle_cta.jpg"), "JPEG", quality=95)
    print("  Saved: 10_bundle_cta.jpg")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Creating Etsy Listing Images")
    print("=" * 60)

    create_image_01_hero()
    create_image_02_whats_included()
    create_image_03_weekly_monthly()
    create_image_04_recipe_budget()
    create_image_05_pantry_mealprep()
    create_image_06_features()
    create_image_07_workflow()
    create_image_08_compatibility()
    create_image_09_testimonials()
    create_image_10_cta()

    print("\n" + "=" * 60)
    print("All 10 listing images created successfully!")
    print("=" * 60)
