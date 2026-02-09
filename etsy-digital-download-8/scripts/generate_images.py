#!/usr/bin/env python3
"""
Generate 5 Etsy listing images for Home Organization & Cleaning Planner 2026.
2700x2025 pixels, iPad mockups, fresh green gradients.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Output paths ──
OUT_DIR = "/home/user/claude-code/etsy-digital-download-8/images"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 2700, 2025

# ── Color palette ──
FOREST     = (39, 103, 73)
SAGE       = (104, 211, 145)
WARM_TERRA = (192, 86, 33)
CREAM      = (255, 255, 240)
SOFT_SAGE  = (198, 246, 213)
DUSTY_PINK = (254, 178, 178)
DARK       = (26, 32, 44)
WHITE      = (255, 255, 255)
LIGHT_GRAY = (240, 243, 240)
MID_GRAY   = (180, 190, 180)

# ── Fonts ──
def font(size, bold=False):
    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# ── Helper: fresh green gradient background ──
def make_gradient(w=W, h=H, top_color=None, bot_color=None):
    top = top_color or (230, 248, 235)
    bot = bot_color or (180, 235, 200)
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(top[0] + (bot[0] - top[0]) * y / h)
        g = int(top[1] + (bot[1] - top[1]) * y / h)
        b = int(top[2] + (bot[2] - top[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

# ── Helper: draw rounded rectangle ──
def rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    if fill:
        draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
        draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
        draw.pieslice([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=fill)
        draw.pieslice([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=fill)
        draw.pieslice([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=fill)
        draw.pieslice([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=fill)
    if outline:
        # Draw outline using arcs and lines
        draw.arc([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([(x0 + r, y0), (x1 - r, y0)], fill=outline, width=width)
        draw.line([(x0 + r, y1), (x1 - r, y1)], fill=outline, width=width)
        draw.line([(x0, y0 + r), (x0, y1 - r)], fill=outline, width=width)
        draw.line([(x1, y0 + r), (x1, y1 - r)], fill=outline, width=width)

# ── Helper: draw iPad mockup with screen content ──
def draw_ipad(img, x, y, iw, ih, screen_callback, shadow=True):
    """Draw an iPad frame at (x, y) with size (iw, ih). screen_callback draws content."""
    draw = ImageDraw.Draw(img)
    bezel = max(12, int(iw * 0.035))
    corner_r = max(18, int(iw * 0.04))

    # Shadow
    if shadow:
        for s in range(12, 0, -1):
            alpha_color = tuple(c + s * 3 for c in (80, 90, 80))
            alpha_color = tuple(min(255, c) for c in alpha_color)
            rounded_rect(draw, (x + s + 4, y + s + 4, x + iw + s + 4, y + ih + s + 4),
                        corner_r + 4, fill=alpha_color)

    # iPad body (dark border)
    rounded_rect(draw, (x - 3, y - 3, x + iw + 3, y + ih + 3), corner_r + 3, fill=(50, 55, 60))
    rounded_rect(draw, (x, y, x + iw, y + ih), corner_r, fill=(30, 35, 40))

    # Screen area
    sx, sy = x + bezel, y + bezel
    sw, sh = iw - 2 * bezel, ih - 2 * bezel
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE)

    # Call the screen content drawer
    screen_callback(draw, sx, sy, sw, sh)

    # Home indicator bar
    bar_w = int(iw * 0.3)
    bar_h = 5
    bar_x = x + (iw - bar_w) // 2
    bar_y = y + ih - bezel // 2 - 2
    rounded_rect(draw, (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), 3, fill=(120, 125, 120))

    return sx, sy, sw, sh

# ── Helper: draw annotation callout arrow + bubble ──
def draw_annotation(draw, ax, ay, bx, by, text, bg_color=WARM_TERRA, text_color=WHITE):
    f = font(26, bold=True)
    bb = draw.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 16
    bw, bh = tw + pad * 2, th + pad * 2

    # Bubble
    rx, ry = bx - bw // 2, by - bh // 2
    rounded_rect(draw, (rx, ry, rx + bw, ry + bh), 14, fill=bg_color)
    draw.text((rx + pad, ry + pad - 2), text, fill=text_color, font=f)

    # Arrow line from (ax, ay) to nearest edge of bubble
    draw.line([(ax, ay), (bx, by)], fill=bg_color, width=3)

# ── Helper: draw checkmark ──
def draw_check(draw, cx, cy, size=16, color=FOREST):
    pts = [
        (cx - size * 0.4, cy),
        (cx - size * 0.1, cy + size * 0.35),
        (cx + size * 0.5, cy - size * 0.35),
    ]
    draw.line(pts[:2], fill=color, width=max(2, size // 5))
    draw.line(pts[1:], fill=color, width=max(2, size // 5))

# ── Helper: text center ──
def text_center(draw, x, y, w, text, fnt, fill=DARK):
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw = bb[2] - bb[0]
    draw.text((x + (w - tw) // 2, y), text, fill=fill, font=fnt)

# ─────────────────────────────────────────────
#  IMAGE 1: Hero — iPad showing Weekly Cleaning Schedule
# ─────────────────────────────────────────────
def make_image_1():
    img = make_gradient(top_color=(225, 248, 232), bot_color=(170, 232, 195))
    draw = ImageDraw.Draw(img)

    # Decorative leaf/dot accents
    for cx, cy, r in [(120, 180, 45), (2580, 250, 35), (200, 1800, 30), (2500, 1750, 50), (350, 400, 20), (2400, 1500, 25)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*SAGE, ))

    # Title area at top
    title_font = font(72, bold=True)
    sub_font = font(36, bold=True)

    # Main title
    text_center(draw, 0, 60, W, "HOME ORGANIZATION", title_font, FOREST)
    text_center(draw, 0, 145, W, "& CLEANING PLANNER", title_font, FOREST)

    # Year badge
    yr_font = font(44, bold=True)
    badge_w, badge_h = 200, 60
    badge_x = W // 2 - badge_w // 2
    badge_y = 230
    rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 12, fill=WARM_TERRA)
    text_center(draw, badge_x, badge_y + 10, badge_w, "2026", yr_font, WHITE)

    # Subtitle
    text_center(draw, 0, 310, W, "8 Professionally Designed Tabs  |  Instant Download  |  Works in Excel & Google Sheets", font(28), DARK)

    # Central iPad
    ipad_w, ipad_h = 1300, 1100
    ipad_x = W // 2 - ipad_w // 2
    ipad_y = 400

    def screen_weekly(draw, sx, sy, sw, sh):
        # Header bar
        rounded_rect(draw, (sx, sy, sx + sw, sy + 55), 0, fill=FOREST)
        text_center(draw, sx, sy + 12, sw, "WEEKLY CLEANING SCHEDULE 2026", font(28, True), WHITE)

        # Subtitle
        draw.rectangle([sx, sy + 55, sx + sw, sy + 85], fill=SOFT_SAGE)
        text_center(draw, sx, sy + 60, sw, "Track daily cleaning tasks by room", font(18), FOREST)

        # Column headers
        cols = ["Room / Area", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        col_w = [sw * 0.30] + [sw * 0.10] * 7
        hdr_y = sy + 92
        draw.rectangle([sx, hdr_y, sx + sw, hdr_y + 38], fill=(220, 245, 228))

        cx_pos = sx
        for i, (c, cw) in enumerate(zip(cols, col_w)):
            cw_int = int(cw)
            draw.text((cx_pos + 8, hdr_y + 8), c, fill=FOREST, font=font(18, True))
            cx_pos += cw_int

        # Data rows
        rows_data = [
            ("Kitchen - Counters", [1,1,0,1,0,1,0]),
            ("Kitchen - Floors",   [1,0,1,0,1,0,0]),
            ("Kitchen - Dishes",   [1,1,1,1,1,0,0]),
            ("Kitchen - Appliances",[0,1,0,1,0,1,0]),
            ("Bathrooms - Toilets", [1,0,1,0,1,0,1]),
            ("Bathrooms - Shower",  [0,1,0,1,0,1,0]),
            ("Living Room - Vacuum",[1,0,0,1,0,0,1]),
            ("Living Room - Dust",  [0,1,0,0,1,0,0]),
            ("Bedroom - Make Beds", [1,1,1,1,1,1,1]),
            ("Bedroom - Laundry",   [0,0,1,0,0,1,0]),
            ("Entryway - Sweep",    [1,0,0,1,0,0,1]),
            ("Dining - Wipe Table", [1,1,1,1,1,1,1]),
            ("Home Office - Tidy",  [0,1,0,0,1,0,0]),
            ("Garage - Sweep",      [0,0,0,0,0,1,0]),
            ("Laundry Room",        [0,0,1,0,0,1,0]),
            ("Windows - Spot Clean",[0,0,0,1,0,0,0]),
        ]

        row_h = int((sh - 140) / len(rows_data))
        row_h = min(row_h, 52)
        for ri, (room, checks) in enumerate(rows_data):
            ry = hdr_y + 40 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (248, 253, 248)
            draw.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            # Thin line
            draw.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=(210, 225, 215), width=1)

            # Room name
            draw.text((sx + 10, ry + 6), room, fill=DARK, font=font(16))

            # Checkmarks
            cx_pos = sx + int(col_w[0])
            for ci, v in enumerate(checks):
                cw_int = int(col_w[ci + 1])
                if v:
                    check_cx = cx_pos + cw_int // 2
                    check_cy = ry + row_h // 2
                    # Green circle bg
                    cr = 11
                    draw.ellipse([check_cx - cr, check_cy - cr, check_cx + cr, check_cy + cr], fill=SAGE)
                    draw_check(draw, check_cx, check_cy, size=9, color=WHITE)
                cx_pos += cw_int

    draw_ipad(img, ipad_x, ipad_y, ipad_w, ipad_h, screen_weekly)

    # Annotations
    draw = ImageDraw.Draw(img)
    # Left annotation
    draw_annotation(draw, ipad_x + 60, ipad_y + 250, ipad_x - 220, ipad_y + 200,
                   "20 Pre-loaded Rooms!", WARM_TERRA)
    # Right annotation
    draw_annotation(draw, ipad_x + ipad_w - 100, ipad_y + 300, ipad_x + ipad_w + 180, ipad_y + 250,
                   "Daily Checkmarks", FOREST)
    # Bottom left
    draw_annotation(draw, ipad_x + 200, ipad_y + ipad_h - 50, ipad_x - 180, ipad_y + ipad_h + 30,
                   "All 7 Days Tracked", WARM_TERRA)

    # Bottom feature pills
    features = ["8 Organized Tabs", "Auto-Calculations", "Print-Ready", "Excel + Sheets"]
    pill_w = 280
    total_pills_w = len(features) * pill_w + (len(features) - 1) * 30
    start_x = W // 2 - total_pills_w // 2
    for i, feat in enumerate(features):
        px = start_x + i * (pill_w + 30)
        py = 1720
        rounded_rect(draw, (px, py, px + pill_w, py + 55), 28, fill=WHITE)
        rounded_rect(draw, (px, py, px + pill_w, py + 55), 28, outline=FOREST, width=2)
        text_center(draw, px, py + 13, pill_w, feat, font(24, True), FOREST)

    # Bottom tagline
    text_center(draw, 0, 1830, W, "Simplify Your Home Routine  -  Everything in One Planner", font(32, True), DARK)

    # Small format note
    text_center(draw, 0, 1900, W, "Digital Download  |  .XLSX Format  |  Fillable & Printable", font(24), FOREST)

    img.save(os.path.join(OUT_DIR, "01_hero_main_listing.png"), "PNG")
    print("Image 1 saved.")

# ─────────────────────────────────────────────
#  IMAGE 2: 7 Mini iPads showing all tabs
# ─────────────────────────────────────────────
def make_image_2():
    img = make_gradient(top_color=(220, 245, 228), bot_color=(190, 238, 210))
    draw = ImageDraw.Draw(img)

    # Top title
    text_center(draw, 0, 50, W, "WHAT'S INSIDE: 8 POWERFUL TABS", font(60, True), FOREST)
    text_center(draw, 0, 125, W, "Everything you need to organize, clean, and maintain your home", font(30), DARK)

    # 7 mini iPads in 2 rows: 4 top, 3 bottom (+1 bonus text)
    tab_names = [
        ("Weekly Cleaning\nSchedule", FOREST),
        ("Deep Cleaning\nChecklist", WARM_TERRA),
        ("Declutter\nTracker", SAGE),
        ("Home\nInventory", FOREST),
        ("Home\nMaintenance", WARM_TERRA),
        ("Household\nBudget", FOREST),
        ("Meal Planning\n& Groceries", SAGE),
    ]

    tab_icons = ["MON TUE WED", "DEEP CLEAN", "SORT ITEMS", "ITEM LIST", "FIX DATES", "$ BUDGET", "MEALS"]
    tab_details = [
        ["20 rooms/areas", "7 days tracked", "Priority levels"],
        ["60+ tasks", "Auto due dates", "Room-by-room"],
        ["Track keep/donate", "Before & after", "Room progress"],
        ["100+ items", "Serial numbers", "Insurance ready"],
        ["40+ tasks", "Cost tracking", "Contractor info"],
        ["20 categories", "Auto difference", "% tracking"],
        ["Full week meals", "Grocery list", "Budget calc"],
    ]

    mini_w, mini_h = 520, 420

    # Row 1: 4 iPads
    row1_total = 4 * mini_w + 3 * 50
    row1_start_x = (W - row1_total) // 2
    row1_y = 210

    # Row 2: 3 iPads centered
    row2_total = 3 * mini_w + 2 * 50
    row2_start_x = (W - row2_total) // 2
    row2_y = 710

    positions = []
    for i in range(4):
        positions.append((row1_start_x + i * (mini_w + 50), row1_y))
    for i in range(3):
        positions.append((row2_start_x + i * (mini_w + 50), row2_y))

    for idx, ((name, color), pos) in enumerate(zip(tab_names, positions)):
        px, py = pos
        details = tab_details[idx]
        icon_text = tab_icons[idx]

        def screen_fn(draw, sx, sy, sw, sh, _name=name, _color=color, _details=details, _icon=icon_text):
            # Header
            draw.rectangle([sx, sy, sx + sw, sy + 42], fill=_color)
            lines = _name.split('\n')
            header_text = lines[0] if len(lines) == 1 else lines[0]
            text_center(draw, sx, sy + 5, sw, header_text, font(17, True), WHITE)
            if len(lines) > 1:
                text_center(draw, sx, sy + 24, sw, lines[1], font(14, True), WHITE)

            # Fake spreadsheet rows
            row_colors = [SOFT_SAGE, WHITE, (248, 252, 248), WHITE, SOFT_SAGE]
            for ri in range(5):
                ry = sy + 50 + ri * 30
                draw.rectangle([sx + 5, ry, sx + sw - 5, ry + 28], fill=row_colors[ri % len(row_colors)])
                draw.rectangle([sx + 5, ry, sx + sw - 5, ry + 28], outline=(210, 230, 215), width=1)
                # Simulated cell dividers
                for ci in range(3):
                    cx = sx + 5 + int((sw - 10) * (ci + 1) / 4)
                    draw.line([(cx, ry), (cx, ry + 28)], fill=(210, 230, 215), width=1)

            # Feature bullets below
            for di, detail in enumerate(_details):
                dy = sy + sh - 95 + di * 26
                draw.ellipse([sx + 15, dy + 4, sx + 25, dy + 14], fill=_color)
                draw.text((sx + 32, dy), detail, fill=DARK, font=font(15))

        draw_ipad(img, px, py, mini_w, mini_h, screen_fn, shadow=True)

        # Tab number label below
        label_y = py + mini_h + 15
        text_center(draw, px, label_y, mini_w, f"Tab {idx + 1}", font(22, True), FOREST)

    # 8th tab callout - How to Use guide mention
    bonus_x = row2_start_x + 3 * (mini_w + 50) - 30
    bonus_y = row2_y + 50
    rounded_rect(draw, (bonus_x, bonus_y, bonus_x + 280, bonus_y + 300), 20, fill=WHITE)
    rounded_rect(draw, (bonus_x, bonus_y, bonus_x + 280, bonus_y + 300), 20, outline=FOREST, width=3)
    text_center(draw, bonus_x, bonus_y + 25, 280, "+", font(60, True), WARM_TERRA)
    text_center(draw, bonus_x, bonus_y + 100, 280, "Tab 8:", font(24, True), FOREST)
    text_center(draw, bonus_x, bonus_y + 135, 280, "How to Use", font(26, True), FOREST)
    text_center(draw, bonus_x, bonus_y + 175, 280, "Step-by-step", font(18), DARK)
    text_center(draw, bonus_x, bonus_y + 200, 280, "user guide", font(18), DARK)
    text_center(draw, bonus_x, bonus_y + 230, 280, "included!", font(18), DARK)

    # Bottom bar
    bar_y = 1250
    draw.rectangle([0, bar_y, W, bar_y + 70], fill=FOREST)
    text_center(draw, 0, bar_y + 15, W, "8 Tabs  |  200+ Pre-loaded Items  |  Auto-Calculations  |  Works in Excel & Google Sheets", font(30, True), WHITE)

    # Bottom tagline
    text_center(draw, 0, 1400, W, "Your Complete Home Management System", font(48, True), FOREST)
    text_center(draw, 0, 1470, W, "From daily cleaning to home inventory - everything organized in one spreadsheet", font(26), DARK)

    # Decorative circles
    for cx, cy, r in [(100, 1700, 60), (2600, 1650, 50), (200, 1600, 30), (2500, 1850, 40)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*SAGE,))

    img.save(os.path.join(OUT_DIR, "02_all_tabs_overview.png"), "PNG")
    print("Image 2 saved.")

# ─────────────────────────────────────────────
#  IMAGE 3: Two iPads — Cleaning Schedule + Deep Clean Checklist
# ─────────────────────────────────────────────
def make_image_3():
    img = make_gradient(top_color=(228, 250, 235), bot_color=(195, 240, 215))
    draw = ImageDraw.Draw(img)

    # Title
    text_center(draw, 0, 60, W, "STAY ON TOP OF EVERY CLEANING TASK", font(56, True), FOREST)
    text_center(draw, 0, 135, W, "Weekly routines + deep cleaning schedules with auto-calculated due dates", font(28), DARK)

    # Left iPad: Weekly Cleaning Schedule
    ipad1_w, ipad1_h = 1100, 1350
    ipad1_x = 130
    ipad1_y = 250

    def screen_weekly_detail(draw, sx, sy, sw, sh):
        # Header
        draw.rectangle([sx, sy, sx + sw, sy + 50], fill=FOREST)
        text_center(draw, sx, sy + 12, sw, "WEEKLY CLEANING SCHEDULE", font(24, True), WHITE)

        # Subheader
        draw.rectangle([sx, sy + 50, sx + sw, sy + 80], fill=SOFT_SAGE)
        text_center(draw, sx, sy + 55, sw, "Track daily cleaning tasks by room - check off as you go!", font(15), FOREST)

        # Column headers
        col_headers = ["Room / Area", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Priority"]
        col_widths = [sw * 0.28] + [sw * 0.08] * 7 + [sw * 0.12]
        hdr_y = sy + 84
        draw.rectangle([sx, hdr_y, sx + sw, hdr_y + 32], fill=(200, 238, 212))
        cx = sx
        for h_text, cw in zip(col_headers, col_widths):
            draw.text((cx + 4, hdr_y + 7), h_text, fill=FOREST, font=font(13, True))
            cx += int(cw)

        rooms = [
            ("Kitchen - Counters & Stovetop", [1,1,0,1,0,1,0], "High"),
            ("Kitchen - Floors",              [1,0,1,0,1,0,0], "Med"),
            ("Kitchen - Dishes & Sink",       [1,1,1,1,1,0,0], "High"),
            ("Kitchen - Appliances",          [0,1,0,1,0,1,0], "Med"),
            ("Bathrooms - Toilets & Sinks",   [1,0,1,0,1,0,1], "High"),
            ("Bathrooms - Shower/Tub",        [0,1,0,1,0,1,0], "Med"),
            ("Bathrooms - Mirrors",           [1,0,0,1,0,0,1], "Low"),
            ("Living Room - Vacuum",          [1,0,0,1,0,0,1], "Med"),
            ("Living Room - Dust Surfaces",   [0,1,0,0,1,0,0], "Med"),
            ("Bedroom - Make Beds",           [1,1,1,1,1,1,1], "High"),
            ("Bedroom - Change Sheets",       [0,0,0,0,0,1,0], "Med"),
            ("Bedroom - Laundry",             [0,0,1,0,0,1,0], "High"),
            ("Entryway - Sweep/Mop",          [1,0,0,1,0,0,1], "Low"),
            ("Dining Room - Wipe Table",      [1,1,1,1,1,1,1], "Med"),
            ("Home Office - Tidy Desk",       [0,1,0,0,1,0,0], "Low"),
            ("Garage - Quick Sweep",          [0,0,0,0,0,1,0], "Low"),
            ("Laundry Room - Clean",          [0,0,1,0,0,1,0], "Low"),
            ("Windows - Spot Clean",          [0,0,0,1,0,0,0], "Low"),
            ("Patio/Deck - Sweep",            [0,0,0,0,0,0,1], "Low"),
            ("Trash & Recycling",             [0,0,1,0,0,0,1], "High"),
        ]

        row_h = min(55, int((sh - 120) / len(rooms)))
        for ri, (room, checks, priority) in enumerate(rooms):
            ry = hdr_y + 34 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (248, 253, 248)
            draw.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            draw.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=(215, 230, 218), width=1)
            draw.text((sx + 6, ry + 5), room, fill=DARK, font=font(14))

            cx = sx + int(col_widths[0])
            for ci, v in enumerate(checks):
                cw = int(col_widths[ci + 1])
                if v:
                    ccx = cx + cw // 2
                    ccy = ry + row_h // 2
                    draw.ellipse([ccx - 10, ccy - 10, ccx + 10, ccy + 10], fill=SAGE)
                    draw_check(draw, ccx, ccy, size=7, color=WHITE)
                cx += cw

            # Priority badge
            px = sx + int(sum(col_widths[:-1]))
            pri_color = WARM_TERRA if priority == "High" else SAGE if priority == "Med" else MID_GRAY
            rounded_rect(draw, (px + 4, ry + 5, px + int(col_widths[-1]) - 4, ry + row_h - 5), 6, fill=pri_color)
            text_center(draw, px + 4, ry + 8, int(col_widths[-1]) - 8, priority, font(12, True), WHITE)

    draw_ipad(img, ipad1_x, ipad1_y, ipad1_w, ipad1_h, screen_weekly_detail)

    # Right iPad: Deep Cleaning Checklist
    ipad2_w, ipad2_h = 1100, 1350
    ipad2_x = W - ipad2_w - 130
    ipad2_y = 300

    def screen_deep_clean(draw, sx, sy, sw, sh):
        draw.rectangle([sx, sy, sx + sw, sy + 50], fill=WARM_TERRA)
        text_center(draw, sx, sy + 12, sw, "DEEP CLEANING CHECKLIST", font(24, True), WHITE)

        draw.rectangle([sx, sy + 50, sx + sw, sy + 80], fill=(255, 235, 220))
        text_center(draw, sx, sy + 55, sw, "Auto-calculates next due date based on frequency!", font(15), WARM_TERRA)

        col_headers = ["Room", "Task", "Frequency", "Last Done", "Next Due", "Status"]
        col_widths = [sw*0.12, sw*0.30, sw*0.14, sw*0.15, sw*0.15, sw*0.14]
        hdr_y = sy + 84
        draw.rectangle([sx, hdr_y, sx + sw, hdr_y + 32], fill=(255, 225, 205))
        cx = sx
        for h_text, cw in zip(col_headers, col_widths):
            draw.text((cx + 4, hdr_y + 7), h_text, fill=WARM_TERRA, font=font(13, True))
            cx += int(cw)

        tasks = [
            ("Kitchen", "Deep clean oven interior", "Monthly", "Jan 10", "Feb 9", "Due"),
            ("Kitchen", "Clean behind refrigerator", "Quarterly", "Dec 15", "Mar 16", "OK"),
            ("Kitchen", "Degrease range hood", "Monthly", "Jan 20", "Feb 19", "OK"),
            ("Kitchen", "Descale coffee maker", "Monthly", "Jan 5", "Feb 4", "Due"),
            ("Bathroom", "Scrub tile grout", "Monthly", "Jan 8", "Feb 7", "Due"),
            ("Bathroom", "Clean exhaust fan", "Quarterly", "Nov 1", "Jan 30", "Due"),
            ("Bathroom", "Deep clean toilet base", "Monthly", "Jan 15", "Feb 14", "OK"),
            ("Living Rm", "Steam clean carpets", "Quarterly", "Oct 20", "Jan 19", "Due"),
            ("Living Rm", "Clean behind furniture", "Quarterly", "Dec 1", "Mar 2", "OK"),
            ("Living Rm", "Wash curtains/drapes", "Semi-Ann", "Aug 15", "Feb 12", "Due"),
            ("Bedroom", "Flip/rotate mattress", "Quarterly", "Nov 10", "Feb 8", "Due"),
            ("Bedroom", "Clean under beds", "Monthly", "Jan 12", "Feb 11", "OK"),
            ("Bedroom", "Wash pillows & duvet", "Quarterly", "Dec 20", "Mar 21", "OK"),
            ("Garage", "Organize storage areas", "Semi-Ann", "Sep 1", "Mar 1", "OK"),
            ("Garage", "Clean garage floor", "Quarterly", "Oct 15", "Jan 14", "Due"),
            ("Windows", "Wash all windows", "Quarterly", "Oct 1", "Dec 30", "Due"),
            ("Exterior", "Power wash driveway", "Annually", "Jun 1", "Jun 1", "OK"),
            ("Exterior", "Clean gutters", "Semi-Ann", "Nov 15", "May 14", "OK"),
            ("Laundry", "Clean washer drum", "Monthly", "Jan 18", "Feb 17", "OK"),
            ("Laundry", "Clean dryer vent", "Quarterly", "Dec 5", "Mar 6", "OK"),
        ]

        row_h = min(55, int((sh - 120) / len(tasks)))
        for ri, (room, task, freq, last, nxt, status) in enumerate(tasks):
            ry = hdr_y + 34 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (255, 250, 245)
            draw.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            draw.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=(240, 225, 215), width=1)

            vals = [room, task, freq, last, nxt]
            cx = sx
            for vi, (val, cw) in enumerate(zip(vals, col_widths)):
                draw.text((cx + 4, ry + 5), val, fill=DARK, font=font(13))
                cx += int(cw)

            # Status badge
            st_x = sx + int(sum(col_widths[:-1]))
            st_color = DUSTY_PINK if status == "Due" else SOFT_SAGE
            st_text_color = (180, 50, 50) if status == "Due" else FOREST
            rounded_rect(draw, (st_x + 6, ry + 4, st_x + int(col_widths[-1]) - 6, ry + row_h - 4), 6, fill=st_color)
            text_center(draw, st_x + 6, ry + 7, int(col_widths[-1]) - 12, status, font(13, True), st_text_color)

    draw_ipad(img, ipad2_x, ipad2_y, ipad2_w, ipad2_h, screen_deep_clean)

    # Labels below iPads
    draw = ImageDraw.Draw(img)
    text_center(draw, ipad1_x, ipad1_y + ipad1_h + 25, ipad1_w, "Weekly Cleaning Schedule", font(32, True), FOREST)
    text_center(draw, ipad1_x, ipad1_y + ipad1_h + 65, ipad1_w, "Track daily tasks for 20 rooms", font(22), DARK)

    text_center(draw, ipad2_x, ipad2_y + ipad2_h + 25, ipad2_w, "Deep Cleaning Checklist", font(32, True), WARM_TERRA)
    text_center(draw, ipad2_x, ipad2_y + ipad2_h + 65, ipad2_w, "60+ tasks with auto due dates", font(22), DARK)

    img.save(os.path.join(OUT_DIR, "03_cleaning_schedule_deep_clean.png"), "PNG")
    print("Image 3 saved.")

# ─────────────────────────────────────────────
#  IMAGE 4: Two iPads — Home Inventory + Maintenance
# ─────────────────────────────────────────────
def make_image_4():
    img = make_gradient(top_color=(232, 252, 240), bot_color=(200, 242, 218))
    draw = ImageDraw.Draw(img)

    # Title
    text_center(draw, 0, 60, W, "PROTECT YOUR HOME & INVESTMENTS", font(56, True), FOREST)
    text_center(draw, 0, 135, W, "Track every item you own + never miss a maintenance task", font(28), DARK)

    # Left iPad: Home Inventory
    ipad1_w, ipad1_h = 1100, 1350
    ipad1_x = 130
    ipad1_y = 250

    def screen_inventory(draw, sx, sy, sw, sh):
        draw.rectangle([sx, sy, sx + sw, sy + 50], fill=FOREST)
        text_center(draw, sx, sy + 12, sw, "HOME INVENTORY", font(24, True), WHITE)

        draw.rectangle([sx, sy + 50, sx + sw, sy + 80], fill=SOFT_SAGE)
        text_center(draw, sx, sy + 55, sw, "Essential for insurance claims & moving!", font(15), FOREST)

        cols = ["Room", "Item", "Category", "Purchase $", "Current $", "Warranty"]
        col_w = [sw*0.14, sw*0.22, sw*0.14, sw*0.16, sw*0.16, sw*0.18]
        hdr_y = sy + 84
        draw.rectangle([sx, hdr_y, sx + sw, hdr_y + 32], fill=(200, 238, 212))
        cx = sx
        for h_text, cw in zip(cols, col_w):
            draw.text((cx + 4, hdr_y + 7), h_text, fill=FOREST, font=font(13, True))
            cx += int(cw)

        items = [
            ("Living Rm", "Sectional Sofa", "Furniture", "$2,500", "$1,800", "2029-03"),
            ("Living Rm", "65\" Smart TV", "Electronics", "$900", "$650", "2027-06"),
            ("Living Rm", "Coffee Table", "Furniture", "$350", "$280", "N/A"),
            ("Living Rm", "Floor Lamp", "Decor", "$130", "$100", "N/A"),
            ("Kitchen", "Refrigerator", "Appliance", "$1,800", "$1,400", "2030-01"),
            ("Kitchen", "Dishwasher", "Appliance", "$750", "$550", "2028-06"),
            ("Kitchen", "Microwave", "Appliance", "$250", "$180", "2027-12"),
            ("Kitchen", "Mixer (Stand)", "Appliance", "$400", "$350", "2029-03"),
            ("Bedroom", "King Bed Frame", "Furniture", "$1,200", "$900", "N/A"),
            ("Bedroom", "Mattress", "Furniture", "$1,500", "$1,200", "2035-01"),
            ("Bedroom", "Dresser", "Furniture", "$800", "$600", "N/A"),
            ("Office", "Desktop PC", "Electronics", "$1,800", "$1,200", "2027-08"),
            ("Office", "Monitor 27\"", "Electronics", "$450", "$300", "2027-08"),
            ("Office", "Desk Chair", "Furniture", "$600", "$450", "2028-03"),
            ("Garage", "Lawn Mower", "Equipment", "$500", "$350", "2028-06"),
            ("Garage", "Tool Set", "Equipment", "$300", "$250", "N/A"),
            ("Bath", "Washer", "Appliance", "$900", "$650", "2029-01"),
            ("Bath", "Dryer", "Appliance", "$850", "$600", "2029-01"),
            ("Dining", "Dining Table", "Furniture", "$1,100", "$850", "N/A"),
            ("Entry", "Security Camera", "Electronics", "$200", "$150", "2027-09"),
        ]

        row_h = min(55, int((sh - 120) / len(items)))
        for ri, row_data in enumerate(items):
            ry = hdr_y + 34 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (248, 253, 248)
            draw.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            draw.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=(215, 230, 218), width=1)

            cx = sx
            for vi, (val, cw) in enumerate(zip(row_data, col_w)):
                draw.text((cx + 4, ry + 5), val, fill=DARK, font=font(13))
                cx += int(cw)

        # Total row
        total_y = hdr_y + 34 + len(items) * row_h + 5
        draw.rectangle([sx, total_y, sx + sw, total_y + 30], fill=FOREST)
        draw.text((sx + 10, total_y + 6), "TOTAL INVENTORY VALUE:", fill=WHITE, font=font(14, True))
        text_center(draw, sx + int(sw * 0.5), total_y + 6, int(sw * 0.5), "$12,810", font(16, True), WHITE)

    draw_ipad(img, ipad1_x, ipad1_y, ipad1_w, ipad1_h, screen_inventory)

    # Right iPad: Home Maintenance
    ipad2_w, ipad2_h = 1100, 1350
    ipad2_x = W - ipad2_w - 130
    ipad2_y = 300

    def screen_maintenance(draw, sx, sy, sw, sh):
        draw.rectangle([sx, sy, sx + sw, sy + 50], fill=WARM_TERRA)
        text_center(draw, sx, sy + 12, sw, "HOME MAINTENANCE SCHEDULE", font(24, True), WHITE)

        draw.rectangle([sx, sy + 50, sx + sw, sy + 80], fill=(255, 235, 220))
        text_center(draw, sx, sy + 55, sw, "Stay ahead of repairs - auto-calculates next due dates!", font(15), WARM_TERRA)

        cols = ["Task", "Category", "Freq", "Last Done", "Next Due", "Cost"]
        col_w = [sw*0.26, sw*0.14, sw*0.12, sw*0.16, sw*0.16, sw*0.12]
        hdr_y = sy + 84
        draw.rectangle([sx, hdr_y, sx + sw, hdr_y + 32], fill=(255, 225, 205))
        cx = sx
        for h_text, cw in zip(cols, col_w):
            draw.text((cx + 4, hdr_y + 7), h_text, fill=WARM_TERRA, font=font(13, True))
            cx += int(cw)

        tasks = [
            ("Replace HVAC filters", "HVAC", "Quarterly", "Dec 15", "Mar 16", "$25"),
            ("Service furnace", "HVAC", "Annually", "Oct 1", "Oct 1", "$150"),
            ("Service A/C unit", "HVAC", "Annually", "Apr 1", "Apr 1", "$150"),
            ("Clean air ducts", "HVAC", "Annually", "Jun 15", "Jun 15", "$400"),
            ("Test smoke detectors", "Safety", "Monthly", "Jan 15", "Feb 14", "$0"),
            ("Check fire extinguishers", "Safety", "Annually", "Jan 1", "Jan 1", "$0"),
            ("Flush water heater", "Plumbing", "Annually", "Sep 1", "Sep 1", "$0"),
            ("Check pipes for leaks", "Plumbing", "Quarterly", "Dec 1", "Mar 2", "$0"),
            ("Clean gutters", "Exterior", "Semi-Ann", "Nov 15", "May 14", "$150"),
            ("Inspect roof", "Exterior", "Annually", "Apr 15", "Apr 15", "$200"),
            ("Power wash siding", "Exterior", "Annually", "May 1", "May 1", "$100"),
            ("Seal driveway cracks", "Exterior", "Annually", "Aug 1", "Aug 1", "$50"),
            ("Treat lawn/garden", "Yard", "Monthly", "Jan 10", "Feb 9", "$40"),
            ("Trim trees/shrubs", "Yard", "Quarterly", "Nov 1", "Jan 30", "$0"),
            ("Fertilize lawn", "Yard", "Quarterly", "Oct 15", "Jan 14", "$30"),
            ("Service garage door", "Garage", "Annually", "Jul 1", "Jul 1", "$100"),
            ("Check weatherstrip", "Insulation", "Annually", "Oct 1", "Oct 1", "$25"),
            ("Clean dryer vent", "Laundry", "Quarterly", "Dec 5", "Mar 6", "$0"),
            ("Test GFCI outlets", "Electrical", "Monthly", "Jan 20", "Feb 19", "$0"),
            ("Check caulking", "Bath/Kit", "Annually", "Mar 1", "Mar 1", "$15"),
        ]

        row_h = min(55, int((sh - 120) / len(tasks)))
        for ri, row_data in enumerate(tasks):
            ry = hdr_y + 34 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (255, 250, 245)
            draw.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            draw.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=(240, 225, 215), width=1)

            cx = sx
            for vi, (val, cw) in enumerate(zip(row_data, col_w)):
                draw.text((cx + 4, ry + 5), val, fill=DARK, font=font(13))
                cx += int(cw)

        # Annual cost row
        total_y = hdr_y + 34 + len(tasks) * row_h + 5
        draw.rectangle([sx, total_y, sx + sw, total_y + 30], fill=WARM_TERRA)
        draw.text((sx + 10, total_y + 6), "EST. ANNUAL MAINTENANCE:", fill=WHITE, font=font(14, True))
        text_center(draw, sx + int(sw * 0.5), total_y + 6, int(sw * 0.5), "$1,435", font(16, True), WHITE)

    draw_ipad(img, ipad2_x, ipad2_y, ipad2_w, ipad2_h, screen_maintenance)

    # Labels
    draw = ImageDraw.Draw(img)
    text_center(draw, ipad1_x, ipad1_y + ipad1_h + 25, ipad1_w, "Home Inventory", font(32, True), FOREST)
    text_center(draw, ipad1_x, ipad1_y + ipad1_h + 65, ipad1_w, "100+ items with values & warranties", font(22), DARK)

    text_center(draw, ipad2_x, ipad2_y + ipad2_h + 25, ipad2_w, "Home Maintenance Schedule", font(32, True), WARM_TERRA)
    text_center(draw, ipad2_x, ipad2_y + ipad2_h + 65, ipad2_w, "40+ tasks with cost tracking", font(22), DARK)

    img.save(os.path.join(OUT_DIR, "04_inventory_maintenance.png"), "PNG")
    print("Image 4 saved.")

# ─────────────────────────────────────────────
#  IMAGE 5: Value prop — "$8.99 INSTANT DOWNLOAD"
# ─────────────────────────────────────────────
def make_image_5():
    img = make_gradient(top_color=(225, 248, 232), bot_color=(175, 235, 200))
    draw = ImageDraw.Draw(img)

    # Large decorative circles
    for cx, cy, r, color in [
        (200, 300, 120, (*SOFT_SAGE,)),
        (2500, 400, 100, (*SOFT_SAGE,)),
        (300, 1600, 80, (*SAGE,)),
        (2400, 1700, 110, (*SOFT_SAGE,)),
        (1350, 1800, 60, (*SAGE,)),
    ]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # Top badge: "BEST VALUE"
    badge_w, badge_h = 350, 55
    badge_x = W // 2 - badge_w // 2
    badge_y = 70
    rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 28, fill=WARM_TERRA)
    text_center(draw, badge_x, badge_y + 12, badge_w, "BEST VALUE", font(30, True), WHITE)

    # Main price
    text_center(draw, 0, 165, W, "$8.99", font(140, True), FOREST)
    text_center(draw, 0, 330, W, "INSTANT DOWNLOAD", font(60, True), DARK)

    # Divider line
    line_w = 600
    draw.line([(W // 2 - line_w // 2, 420), (W // 2 + line_w // 2, 420)], fill=SAGE, width=4)

    # "What You Get" section
    text_center(draw, 0, 460, W, "EVERYTHING YOU GET:", font(42, True), FOREST)

    # Feature cards in 2 columns
    features = [
        ("Weekly Cleaning Schedule", "20 rooms, 7 days, priorities", FOREST),
        ("Deep Cleaning Checklist", "60+ tasks, auto due dates", WARM_TERRA),
        ("Declutter Tracker", "Room-by-room progress tracking", FOREST),
        ("Home Inventory", "100+ items, insurance-ready", WARM_TERRA),
        ("Home Maintenance", "40+ tasks, cost estimates", FOREST),
        ("Household Budget", "20 categories, auto-calc", WARM_TERRA),
        ("Meal Planning & Groceries", "Full week + grocery list", FOREST),
        ("How to Use Guide", "Step-by-step instructions", SAGE),
    ]

    card_w, card_h = 1050, 80
    gap_x, gap_y = 60, 18
    total_w = card_w * 2 + gap_x
    start_x = (W - total_w) // 2
    start_y = 540

    for i, (title, desc, color) in enumerate(features):
        col = i % 2
        row = i // 2
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        rounded_rect(draw, (cx, cy, cx + card_w, cy + card_h), 16, fill=WHITE)
        # Left accent bar
        draw.rectangle([cx, cy + 8, cx + 8, cy + card_h - 8], fill=color)
        # Number circle
        num_cx = cx + 40
        num_cy = cy + card_h // 2
        draw.ellipse([num_cx - 18, num_cy - 18, num_cx + 18, num_cy + 18], fill=color)
        text_center(draw, num_cx - 10, num_cy - 12, 20, str(i + 1), font(18, True), WHITE)
        # Text
        draw.text((cx + 70, cy + 12), title, fill=DARK, font=font(24, True))
        draw.text((cx + 70, cy + 44), desc, fill=(100, 110, 100), font=font(18))

    # Comparison / value section
    comp_y = start_y + 4 * (card_h + gap_y) + 40
    rounded_rect(draw, (W // 2 - 700, comp_y, W // 2 + 700, comp_y + 200), 24, fill=WHITE)

    # Left side: what others charge
    text_center(draw, W // 2 - 700, comp_y + 20, 700, "Professional Organizer Visit", font(26, True), DARK)
    text_center(draw, W // 2 - 700, comp_y + 60, 700, "$200 - $500+ per session", font(34, True), DUSTY_PINK)
    text_center(draw, W // 2 - 700, comp_y + 110, 700, "Cleaning planners: $15 - $30", font(22), (130, 130, 130))
    text_center(draw, W // 2 - 700, comp_y + 145, 700, "Home inventory apps: $5 - $10/mo", font(22), (130, 130, 130))

    # Divider
    draw.line([(W // 2, comp_y + 20), (W // 2, comp_y + 180)], fill=SAGE, width=3)

    # Right side: this product
    text_center(draw, W // 2, comp_y + 20, 700, "This Complete Planner", font(26, True), DARK)
    text_center(draw, W // 2, comp_y + 60, 700, "Just $8.99 - One Time!", font(40, True), FOREST)
    text_center(draw, W // 2, comp_y + 110, 700, "8 tabs, 200+ pre-loaded items", font(22), FOREST)
    text_center(draw, W // 2, comp_y + 145, 700, "Use forever - no subscriptions!", font(22), FOREST)

    # Bottom key benefits
    benefits = [
        ("INSTANT\nDOWNLOAD", "Get it in minutes"),
        ("EXCEL &\nGOOGLE SHEETS", "Works everywhere"),
        ("FILLABLE &\nPRINTABLE", "Use your way"),
        ("200+ ITEMS\nPRE-LOADED", "Ready to go"),
        ("AUTO\nCALCULATIONS", "Smart formulas"),
    ]

    benefit_w = 380
    total_ben = len(benefits) * benefit_w + (len(benefits) - 1) * 40
    ben_start_x = (W - total_ben) // 2
    ben_y = comp_y + 240

    for i, (title, sub) in enumerate(benefits):
        bx = ben_start_x + i * (benefit_w + 40)
        by = ben_y

        rounded_rect(draw, (bx, by, bx + benefit_w, by + 130), 18, fill=FOREST)
        lines = title.split('\n')
        text_center(draw, bx, by + 15, benefit_w, lines[0], font(24, True), WHITE)
        if len(lines) > 1:
            text_center(draw, bx, by + 45, benefit_w, lines[1], font(24, True), WHITE)
        text_center(draw, bx, by + 85, benefit_w, sub, font(18), SOFT_SAGE)

    # Final CTA
    cta_y = ben_y + 180
    rounded_rect(draw, (W // 2 - 450, cta_y, W // 2 + 450, cta_y + 80), 40, fill=WARM_TERRA)
    text_center(draw, W // 2 - 450, cta_y + 18, 900, "ADD TO CART  -  Start Organizing Today!", font(34, True), WHITE)

    # Bottom note
    text_center(draw, 0, cta_y + 110, W, "Digital product  |  No physical item shipped  |  .XLSX format", font(22), DARK)

    img.save(os.path.join(OUT_DIR, "05_value_prop_pricing.png"), "PNG")
    print("Image 5 saved.")


# ── Run all ──
if __name__ == "__main__":
    print("Generating Image 1...")
    make_image_1()
    print("Generating Image 2...")
    make_image_2()
    print("Generating Image 3...")
    make_image_3()
    print("Generating Image 4...")
    make_image_4()
    print("Generating Image 5...")
    make_image_5()
    print("\nAll 5 images generated successfully!")
