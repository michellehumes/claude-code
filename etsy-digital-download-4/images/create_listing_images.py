#!/usr/bin/env python3
"""
Generate 5 professional Etsy listing images for
"Wedding Planner & Budget Spreadsheet Bundle 2026"

All images: 2700x2025 px (Etsy recommended)
"""

import math
from PIL import Image, ImageDraw, ImageFont

# ── Dimensions ────────────────────────────────────────────────────────
W, H = 2700, 2025

# ── Color Palette (Elegant, Romantic) ─────────────────────────────────
BLUSH = (232, 196, 200)
ROSE_GOLD = (183, 110, 121)
CHAMPAGNE = (247, 231, 206)
IVORY = (255, 255, 240)
SAGE_GREEN = (156, 175, 136)
DUSTY_MAUVE = (201, 169, 166)
DEEP_PLUM = (74, 32, 64)
GOLD = (197, 165, 90)
WHITE = (255, 255, 255)
CREAM = (255, 253, 248)
DARK_TEXT = (44, 44, 44)

# ── Fonts ─────────────────────────────────────────────────────────────
BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(bold=False, size=32):
    path = BOLD_PATH if bold else REG_PATH
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered_text(draw, y, text, fnt, fill, x_center=W // 2):
    tw, th = text_size(draw, text, fnt)
    draw.text((x_center - tw // 2, y), text, font=fnt, fill=fill)
    return th


def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    # Main body
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    # Corners
    draw.pieslice([x0, y0, x0 + 2 * r, y0 + 2 * r], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * r, y0, x1, y0 + 2 * r], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * r, x0 + 2 * r, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * r, y1 - 2 * r, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0 + 2 * r, y0 + 2 * r], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * r, y0, x1, y0 + 2 * r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * r, x0 + 2 * r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * r, y1 - 2 * r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + r, y0, x1 - r, y0], fill=outline, width=width)
        draw.line([x0 + r, y1, x1 - r, y1], fill=outline, width=width)
        draw.line([x0, y0 + r, x0, y1 - r], fill=outline, width=width)
        draw.line([x1, y0 + r, x1, y1 - r], fill=outline, width=width)


def draw_circle(draw, cx, cy, r, fill):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def new_canvas(bg=CREAM):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def draw_top_banner(draw, text, bg=DEEP_PLUM, fg=WHITE, height=80):
    draw.rectangle([0, 0, W, height], fill=bg)
    fnt = font(bold=True, size=28)
    draw_centered_text(draw, (height - 28) // 2 + 2, text, fnt, fg)
    return height


def draw_bottom_bar(draw, text, bg=DEEP_PLUM, fg=WHITE, height=70, y=None):
    if y is None:
        y = H - height
    draw.rectangle([0, y, W, y + height], fill=bg)
    fnt = font(bold=True, size=26)
    draw_centered_text(draw, y + (height - 26) // 2, text, fnt, fg)
    return y


def draw_decorative_diamonds(draw, y, width_span=W, color=GOLD, count=7, size=6):
    spacing = width_span // (count + 1)
    for i in range(1, count + 1):
        cx = spacing * i
        pts = [(cx, y - size), (cx + size, y), (cx, y + size), (cx - size, y)]
        draw.polygon(pts, fill=color)


# =====================================================================
# IMAGE 1 — Hero / Main Listing
# =====================================================================
def create_image_01():
    img, draw = new_canvas(CHAMPAGNE)

    # Top banner
    banner_h = draw_top_banner(draw, "INSTANT DOWNLOAD  |  GOOGLE SHEETS & EXCEL")

    # White content card with rose gold border
    card_x0, card_y0 = 100, banner_h + 30
    card_x1, card_y1 = W - 100, H - 100
    draw_rounded_rect(draw, (card_x0, card_y0, card_x1, card_y1), 18, WHITE,
                      outline=ROSE_GOLD, width=5)

    # Inner accent bar
    bar_y = card_y0 + 30
    bar_h = 56
    draw.rectangle([card_x0 + 40, bar_y, card_x1 - 40, bar_y + bar_h], fill=ROSE_GOLD)
    fnt_accent = font(bold=True, size=24)
    draw_centered_text(draw, bar_y + 14, "ALL-IN-ONE WEDDING SPREADSHEET  |  9 TABS",
                       fnt_accent, WHITE)

    # Decorative line
    draw_decorative_diamonds(draw, bar_y + bar_h + 25, color=GOLD)

    # Large title
    title_y = bar_y + bar_h + 50
    fnt_title = font(bold=True, size=72)
    draw_centered_text(draw, title_y, "WEDDING PLANNER", fnt_title, DEEP_PLUM)
    fnt_title2 = font(bold=True, size=72)
    draw_centered_text(draw, title_y + 85, "& BUDGET BUNDLE", fnt_title2, DEEP_PLUM)

    # 2026 badge
    badge_y = title_y + 190
    badge_w, badge_h = 200, 64
    badge_x = W // 2 - badge_w // 2
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      32, GOLD)
    fnt_badge = font(bold=True, size=38)
    draw_centered_text(draw, badge_y + 10, "2026", fnt_badge, WHITE)

    # Thin divider line
    div_y = badge_y + badge_h + 30
    draw.line([card_x0 + 150, div_y, card_x1 - 150, div_y], fill=DUSTY_MAUVE, width=2)

    # 9 feature bullets in 3 columns
    features = [
        "Wedding Dashboard", "Budget Tracker", "Guest List & RSVPs",
        "Vendor Manager", "Timeline Checklist", "Seating Chart",
        "Day-Of Schedule", "Gift Tracker", "How-to Guide"
    ]
    cols = 3
    rows = 3
    feat_start_y = div_y + 25
    col_width = (card_x1 - card_x0 - 120) // cols
    fnt_feat = font(bold=False, size=28)
    marker_r = 8
    for idx, feat in enumerate(features):
        col = idx % cols
        row = idx // cols
        cx = card_x0 + 100 + col * col_width
        cy = feat_start_y + row * 55
        draw_circle(draw, cx, cy + 14, marker_r, ROSE_GOLD)
        draw.text((cx + 22, cy), feat, font=fnt_feat, fill=DARK_TEXT)

    # Value prop
    vp_y = feat_start_y + rows * 55 + 25
    draw.line([card_x0 + 150, vp_y, card_x1 - 150, vp_y], fill=DUSTY_MAUVE, width=2)
    vp_y += 18
    fnt_vp = font(bold=True, size=38)
    draw_centered_text(draw, vp_y, "Plan Your Dream Wedding Without the Stress",
                       fnt_vp, ROSE_GOLD)

    # "Perfect for" section
    pf_y = vp_y + 60
    fnt_pf = font(bold=False, size=24)
    draw_centered_text(draw, pf_y, "PERFECT FOR:", font(bold=True, size=24), DEEP_PLUM)
    pf_y += 38
    draw_centered_text(draw, pf_y,
                       "Engaged Couples  |  Brides-to-Be  |  Wedding Coordinators  |  DIY Weddings",
                       fnt_pf, DARK_TEXT)

    # Decorative diamonds above bottom bar
    draw_decorative_diamonds(draw, card_y1 + 10, color=GOLD, count=5)

    # Bottom CTA bar
    draw_bottom_bar(draw, "ADD TO CART  \u2014  START PLANNING TODAY!")

    img.save("/home/user/claude-code/etsy-digital-download-4/images/01_hero_main_listing.png")
    print("  [1/5] 01_hero_main_listing.png")


# =====================================================================
# IMAGE 2 — What's Included
# =====================================================================
def create_image_02():
    img, draw = new_canvas(CREAM)

    # Header bar
    header_h = 110
    draw.rectangle([0, 0, W, header_h], fill=DEEP_PLUM)
    fnt_h = font(bold=True, size=52)
    draw_centered_text(draw, 26, "WHAT'S INCLUDED", fnt_h, WHITE)

    # Subtitle
    fnt_sub = font(bold=False, size=26)
    sub_y = header_h + 16
    draw_centered_text(draw, sub_y, "9 Professional Tabs \u2014 Everything You Need to Plan Your Wedding",
                       fnt_sub, DARK_TEXT)

    # 8 feature cards (2 cols x 4 rows)
    cards_data = [
        (1, "WEDDING DASHBOARD",
         ["Budget overview at a glance", "RSVP summary counts", "Countdown timer"], ROSE_GOLD),
        (2, "BUDGET TRACKER",
         ["23 wedding categories", "Auto-generated pie chart", "Deposit tracking"], DEEP_PLUM),
        (3, "GUEST LIST & RSVPs",
         ["150-guest capacity", "Dietary needs tracking", "Thank-you tracker"], ROSE_GOLD),
        (4, "VENDOR TRACKER",
         ["20 vendor categories", "Contract & payment status", "Contact info hub"], GOLD),
        (5, "TIMELINE CHECKLIST",
         ["12-month planning guide", "50+ pre-loaded tasks", "Priority levels"], SAGE_GREEN),
        (6, "SEATING CHART",
         ["20 tables x 8 guests", "Dietary notes per table", "Drag-and-drop friendly"], DUSTY_MAUVE),
        (7, "DAY-OF TIMELINE",
         ["Hour-by-hour schedule", "8 AM to 11 PM coverage", "Person responsible"], ROSE_GOLD),
        (8, "GIFT TRACKER",
         ["100-row gift log", "Thank-you status", "Estimated value tracker"], GOLD),
    ]

    card_start_y = sub_y + 46
    gap_x = 40
    gap_y = 22
    col_w = (W - 160 - gap_x) // 2
    card_h = 165
    fnt_num = font(bold=True, size=28)
    fnt_card_title = font(bold=True, size=26)
    fnt_bullet = font(bold=False, size=21)

    for idx, (num, title, bullets, accent) in enumerate(cards_data):
        col = idx % 2
        row = idx // 2
        x0 = 80 + col * (col_w + gap_x)
        y0 = card_start_y + row * (card_h + gap_y)
        x1 = x0 + col_w
        y1 = y0 + card_h

        # Card background
        draw_rounded_rect(draw, (x0, y0, x1, y1), 12, WHITE,
                          outline=DUSTY_MAUVE, width=2)
        # Accent left strip
        draw.rectangle([x0, y0 + 12, x0 + 8, y1 - 12], fill=accent)

        # Number circle
        nc_x = x0 + 44
        nc_y = y0 + 36
        draw_circle(draw, nc_x, nc_y, 22, accent)
        tw, _ = text_size(draw, str(num), fnt_num)
        draw.text((nc_x - tw // 2, nc_y - 15), str(num), font=fnt_num, fill=WHITE)

        # Title
        draw.text((nc_x + 34, y0 + 18), title, font=fnt_card_title, fill=DARK_TEXT)

        # Bullets
        bx = nc_x + 34
        by = y0 + 58
        for b in bullets:
            draw_circle(draw, bx - 2, by + 11, 4, accent)
            draw.text((bx + 12, by), b, font=fnt_bullet, fill=DARK_TEXT)
            by += 32

    # Bonus bar for tab 9
    bonus_y = card_start_y + 4 * (card_h + gap_y) + 8
    draw_rounded_rect(draw, (80, bonus_y, W - 80, bonus_y + 62), 12, CHAMPAGNE,
                      outline=GOLD, width=3)
    fnt_bonus = font(bold=True, size=26)
    draw_centered_text(draw, bonus_y + 14,
                       "BONUS  Tab 9:  How-to-Use Guide  \u2014  Step-by-Step Instructions Included!",
                       fnt_bonus, DEEP_PLUM)

    # Decorative diamonds
    draw_decorative_diamonds(draw, bonus_y + 82, color=GOLD, count=5)

    # Bottom bar
    draw_bottom_bar(draw, "9 TABS  |  GOOGLE SHEETS + EXCEL  |  INSTANT DOWNLOAD")

    img.save("/home/user/claude-code/etsy-digital-download-4/images/02_whats_included.png")
    print("  [2/5] 02_whats_included.png")


# =====================================================================
# IMAGE 3 — Budget & Guest List Preview
# =====================================================================
def create_image_03():
    img, draw = new_canvas(CREAM)

    # Header
    header_h = 110
    draw.rectangle([0, 0, W, header_h], fill=DEEP_PLUM)
    fnt_h = font(bold=True, size=46)
    draw_centered_text(draw, 28, "BUDGET TRACKER & GUEST LIST PREVIEW", fnt_h, WHITE)

    subtitle_y = header_h + 14
    fnt_sub = font(bold=False, size=24)
    draw_centered_text(draw, subtitle_y,
                       "Keep Every Dollar and Every Guest Organized in One Place", fnt_sub, DARK_TEXT)

    content_y = subtitle_y + 50
    panel_gap = 50
    panel_w = (W - 160 - panel_gap) // 2

    # ── LEFT: Budget Tracker mockup ──
    lx0, ly0 = 80, content_y
    lx1, ly1 = lx0 + panel_w, H - 200

    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), 14, WHITE,
                      outline=ROSE_GOLD, width=3)

    # Panel title
    draw.rectangle([lx0, ly0, lx1, ly0 + 56], fill=ROSE_GOLD)
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly0 + 30), 14, ROSE_GOLD)
    draw.rectangle([lx0, ly0 + 14, lx1, ly0 + 56], fill=ROSE_GOLD)
    fnt_pt = font(bold=True, size=26)
    draw_centered_text(draw, ly0 + 12, "BUDGET TRACKER", fnt_pt, WHITE,
                       x_center=(lx0 + lx1) // 2)

    # Table header
    th_y = ly0 + 66
    fnt_th = font(bold=True, size=19)
    fnt_td = font(bold=False, size=19)
    cols_budget = ["Category", "Estimated", "Actual", "Deposit", "Balance"]
    col_xs = [lx0 + 20, lx0 + 260, lx0 + 420, lx0 + 570, lx0 + 710]

    draw.rectangle([lx0 + 10, th_y, lx1 - 10, th_y + 34], fill=CHAMPAGNE)
    for ci, cname in enumerate(cols_budget):
        draw.text((col_xs[ci], th_y + 5), cname, font=fnt_th, fill=DEEP_PLUM)

    budget_rows = [
        ("Venue", "$8,000", "$7,800", "$3,000", "$4,800"),
        ("Catering", "$6,500", "$6,200", "$2,000", "$4,200"),
        ("Photography", "$3,500", "$3,500", "$1,000", "$2,500"),
        ("Florist", "$2,000", "$1,800", "$500", "$1,300"),
        ("DJ / Music", "$1,500", "$1,400", "$400", "$1,000"),
        ("Wedding Cake", "$800", "$750", "$200", "$550"),
        ("Invitations", "$600", "$580", "$580", "$0"),
        ("Attire", "$2,500", "$2,400", "$1,200", "$1,200"),
        ("Decor & Rentals", "$1,800", "$1,600", "$500", "$1,100"),
        ("Transportation", "$700", "$650", "$200", "$450"),
    ]

    row_y = th_y + 40
    row_h = 32
    for ri, row_data in enumerate(budget_rows):
        bg = IVORY if ri % 2 == 0 else WHITE
        draw.rectangle([lx0 + 10, row_y, lx1 - 10, row_y + row_h], fill=bg)
        for ci, val in enumerate(row_data):
            draw.text((col_xs[ci], row_y + 4), val, font=fnt_td, fill=DARK_TEXT)
        row_y += row_h

    # Totals row
    draw.rectangle([lx0 + 10, row_y, lx1 - 10, row_y + 36], fill=DEEP_PLUM)
    fnt_tot = font(bold=True, size=20)
    draw.text((col_xs[0], row_y + 6), "TOTAL", font=fnt_tot, fill=WHITE)
    draw.text((col_xs[1], row_y + 6), "$27,900", font=fnt_tot, fill=WHITE)
    draw.text((col_xs[2], row_y + 6), "$26,680", font=fnt_tot, fill=WHITE)
    draw.text((col_xs[3], row_y + 6), "$9,580", font=fnt_tot, fill=WHITE)
    draw.text((col_xs[4], row_y + 6), "$17,100", font=fnt_tot, fill=GOLD)
    row_y += 44

    # Mini pie chart area
    pie_cx = (lx0 + lx1) // 2
    pie_cy = row_y + 140
    pie_r = 110
    pie_colors = [ROSE_GOLD, DEEP_PLUM, GOLD, SAGE_GREEN, DUSTY_MAUVE, BLUSH, CHAMPAGNE]
    pie_pcts = [28, 23, 13, 7, 5, 3, 21]
    start = 0
    for pct, col in zip(pie_pcts, pie_colors):
        end = start + pct * 3.6
        draw.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r],
                      start, end, fill=col)
        start = end
    # Center hole for donut effect
    draw_circle(draw, pie_cx, pie_cy, 50, WHITE)
    fnt_pie_label = font(bold=True, size=18)
    draw_centered_text(draw, pie_cy - 12, "BUDGET", fnt_pie_label, DEEP_PLUM,
                       x_center=pie_cx)
    fnt_pie_label2 = font(bold=False, size=16)
    draw_centered_text(draw, pie_cy + 10, "BREAKDOWN", fnt_pie_label2, DARK_TEXT,
                       x_center=pie_cx)

    # ── RIGHT: Guest List mockup ──
    rx0 = lx1 + panel_gap
    rx1 = rx0 + panel_w
    ry0, ry1 = ly0, ly1

    draw_rounded_rect(draw, (rx0, ry0, rx1, ry1), 14, WHITE,
                      outline=SAGE_GREEN, width=3)

    # Panel title
    draw.rectangle([rx0, ry0, rx1, ry0 + 56], fill=SAGE_GREEN)
    draw_rounded_rect(draw, (rx0, ry0, rx1, ry0 + 30), 14, SAGE_GREEN)
    draw.rectangle([rx0, ry0 + 14, rx1, ry0 + 56], fill=SAGE_GREEN)
    draw_centered_text(draw, ry0 + 12, "GUEST LIST & RSVPs", fnt_pt, WHITE,
                       x_center=(rx0 + rx1) // 2)

    # Summary counts bar
    sc_y = ry0 + 66
    sc_h = 48
    draw.rectangle([rx0 + 10, sc_y, rx1 - 10, sc_y + sc_h], fill=IVORY)
    fnt_sc = font(bold=True, size=18)
    counts = [("87 Attending", SAGE_GREEN), ("34 Pending", GOLD), ("12 Declined", ROSE_GOLD)]
    cx_start = rx0 + 50
    for i, (label, clr) in enumerate(counts):
        x = cx_start + i * 280
        draw_circle(draw, x, sc_y + sc_h // 2, 8, clr)
        draw.text((x + 16, sc_y + 12), label, font=fnt_sc, fill=DARK_TEXT)

    # Guest table header
    gt_y = sc_y + sc_h + 14
    guest_cols = ["Guest Name", "Party", "RSVP", "Dietary", "Thank You"]
    gcol_xs = [rx0 + 20, rx0 + 310, rx0 + 420, rx0 + 560, rx0 + 720]

    draw.rectangle([rx0 + 10, gt_y, rx1 - 10, gt_y + 34], fill=CHAMPAGNE)
    for ci, cname in enumerate(guest_cols):
        draw.text((gcol_xs[ci], gt_y + 5), cname, font=fnt_th, fill=DEEP_PLUM)

    guests = [
        ("Emma & James Wilson", "2", "Attending", "None", "Sent"),
        ("Olivia Chen", "1", "Attending", "Vegan", "Sent"),
        ("Liam & Sarah Davis", "2", "Pending", "Gluten-free", "---"),
        ("Sophia Martinez", "1", "Attending", "None", "Sent"),
        ("Noah Thompson", "1", "Declined", "---", "---"),
        ("Ava & Ben Roberts", "2", "Attending", "Nut allergy", "Sent"),
        ("Mason Kim", "1", "Pending", "None", "---"),
        ("Isabella Garcia", "1", "Attending", "Vegetarian", "Sent"),
        ("Ethan Brooks", "1", "Pending", "None", "---"),
        ("Mia & Jack Anderson", "2", "Attending", "None", "Draft"),
        ("Charlotte Lee", "1", "Attending", "Dairy-free", "Sent"),
        ("Lucas Wright", "1", "Declined", "---", "---"),
    ]

    rsvp_colors = {"Attending": SAGE_GREEN, "Pending": GOLD, "Declined": ROSE_GOLD}
    gtr_y = gt_y + 40
    gtr_h = 32
    fnt_rsvp = font(bold=True, size=16)
    for gi, (name, party, rsvp, diet, ty) in enumerate(guests):
        bg = IVORY if gi % 2 == 0 else WHITE
        draw.rectangle([rx0 + 10, gtr_y, rx1 - 10, gtr_y + gtr_h], fill=bg)
        draw.text((gcol_xs[0], gtr_y + 4), name, font=fnt_td, fill=DARK_TEXT)
        draw.text((gcol_xs[1] + 20, gtr_y + 4), party, font=fnt_td, fill=DARK_TEXT)

        # RSVP badge
        rclr = rsvp_colors.get(rsvp, DARK_TEXT)
        rtw, _ = text_size(draw, rsvp, fnt_rsvp)
        badge_x = gcol_xs[2]
        draw_rounded_rect(draw, (badge_x, gtr_y + 3, badge_x + rtw + 16, gtr_y + gtr_h - 3),
                          10, rclr)
        draw.text((badge_x + 8, gtr_y + 6), rsvp, font=fnt_rsvp, fill=WHITE)

        draw.text((gcol_xs[3], gtr_y + 4), diet, font=fnt_td, fill=DARK_TEXT)
        draw.text((gcol_xs[4], gtr_y + 4), ty, font=fnt_td, fill=DARK_TEXT)
        gtr_y += gtr_h

    # Totals row
    draw.rectangle([rx0 + 10, gtr_y, rx1 - 10, gtr_y + 36], fill=DEEP_PLUM)
    draw.text((gcol_xs[0], gtr_y + 6), "TOTAL GUESTS: 133", font=fnt_tot, fill=WHITE)
    draw.text((gcol_xs[2], gtr_y + 6), "CAPACITY: 150", font=fnt_tot, fill=GOLD)

    # Tab bar at bottom
    tab_bar_y = H - 200
    draw.rectangle([80, tab_bar_y, W - 80, tab_bar_y + 52], fill=DEEP_PLUM)
    tabs = ["Dashboard", "Budget", "Guest List", "Vendors", "Timeline",
            "Seating", "Day-Of", "Gifts", "How-To"]
    tab_fnt = font(bold=True, size=18)
    tab_w = (W - 200) // len(tabs)
    for ti, tname in enumerate(tabs):
        tx = 100 + ti * tab_w
        tw, _ = text_size(draw, tname, tab_fnt)
        draw.text((tx + (tab_w - tw) // 2, tab_bar_y + 14), tname,
                  font=tab_fnt, fill=WHITE if ti != 1 else GOLD)

    # Decorative diamonds
    draw_decorative_diamonds(draw, tab_bar_y + 72, color=GOLD, count=5)

    # Bottom banner
    draw_bottom_bar(draw, "PLAN SMARTER  |  STAY ON BUDGET  |  INSTANT DOWNLOAD")

    img.save("/home/user/claude-code/etsy-digital-download-4/images/03_budget_guest_preview.png")
    print("  [3/5] 03_budget_guest_preview.png")


# =====================================================================
# IMAGE 4 — Timeline & Seating Showcase
# =====================================================================
def create_image_04():
    img, draw = new_canvas(CREAM)

    # Header
    header_h = 110
    draw.rectangle([0, 0, W, header_h], fill=DEEP_PLUM)
    fnt_h = font(bold=True, size=42)
    draw_centered_text(draw, 30,
                       "PLAN EVERY DETAIL FROM 12 MONTHS OUT TO \"I DO\"", fnt_h, WHITE)

    subtitle_y = header_h + 14
    fnt_sub = font(bold=False, size=24)
    draw_centered_text(draw, subtitle_y,
                       "Timeline Checklist + Day-Of Schedule \u2014 Never Miss a Beat", fnt_sub, DARK_TEXT)

    content_y = subtitle_y + 50
    panel_gap = 50
    panel_w = (W - 160 - panel_gap) // 2

    # ── LEFT: Timeline / Checklist ──
    lx0, ly0 = 80, content_y
    lx1, ly1 = lx0 + panel_w, H - 160

    draw_rounded_rect(draw, (lx0, ly0, lx1, ly1), 14, WHITE,
                      outline=SAGE_GREEN, width=3)

    # Title bar
    draw.rectangle([lx0, ly0, lx1, ly0 + 56], fill=SAGE_GREEN)
    draw_rounded_rect(draw, (lx0, ly0, lx1, ly0 + 30), 14, SAGE_GREEN)
    draw.rectangle([lx0, ly0 + 14, lx1, ly0 + 56], fill=SAGE_GREEN)
    fnt_pt = font(bold=True, size=26)
    draw_centered_text(draw, ly0 + 12, "TIMELINE CHECKLIST", fnt_pt, WHITE,
                       x_center=(lx0 + lx1) // 2)

    timeline_data = [
        ("12 MONTHS BEFORE", ROSE_GOLD, [
            ("Set overall budget", "Done"),
            ("Book venue", "Done"),
            ("Choose wedding party", "Done"),
        ]),
        ("9 MONTHS BEFORE", GOLD, [
            ("Book photographer", "Done"),
            ("Book caterer", "In Progress"),
            ("Send save-the-dates", "Not Started"),
        ]),
        ("6 MONTHS BEFORE", SAGE_GREEN, [
            ("Order wedding dress", "In Progress"),
            ("Book florist", "Not Started"),
            ("Plan honeymoon", "Not Started"),
        ]),
        ("3 MONTHS BEFORE", DUSTY_MAUVE, [
            ("Mail invitations", "Not Started"),
            ("Book DJ / band", "Not Started"),
            ("Order wedding cake", "Not Started"),
        ]),
        ("1 MONTH BEFORE", DEEP_PLUM, [
            ("Final dress fitting", "Not Started"),
            ("Confirm all vendors", "Not Started"),
            ("Create seating chart", "Not Started"),
        ]),
        ("1 WEEK BEFORE", ROSE_GOLD, [
            ("Final venue walkthrough", "Not Started"),
            ("Rehearsal dinner", "Not Started"),
        ]),
    ]

    status_colors = {"Done": SAGE_GREEN, "In Progress": GOLD, "Not Started": DUSTY_MAUVE}
    fnt_period = font(bold=True, size=22)
    fnt_task = font(bold=False, size=19)
    fnt_status = font(bold=True, size=15)
    ty = ly0 + 70

    for period, accent, tasks in timeline_data:
        # Period label
        draw.rectangle([lx0 + 20, ty, lx0 + 24, ty + len(tasks) * 34 + 30], fill=accent)
        draw_circle(draw, lx0 + 22, ty + 4, 6, accent)
        draw.text((lx0 + 42, ty - 6), period, font=fnt_period, fill=accent)
        ty += 30

        for task_name, status in tasks:
            sclr = status_colors[status]
            draw.text((lx0 + 52, ty), task_name, font=fnt_task, fill=DARK_TEXT)
            # Status badge
            stw, _ = text_size(draw, status, fnt_status)
            sx = lx1 - 40 - stw - 16
            draw_rounded_rect(draw, (sx, ty, sx + stw + 16, ty + 26), 8, sclr)
            draw.text((sx + 8, ty + 3), status, font=fnt_status, fill=WHITE)
            ty += 34

        ty += 10

    # ── RIGHT: Day-Of Timeline ──
    rx0 = lx1 + panel_gap
    rx1 = rx0 + panel_w
    ry0, ry1 = ly0, ly1

    draw_rounded_rect(draw, (rx0, ry0, rx1, ry1), 14, WHITE,
                      outline=ROSE_GOLD, width=3)

    # Title bar
    draw.rectangle([rx0, ry0, rx1, ry0 + 56], fill=ROSE_GOLD)
    draw_rounded_rect(draw, (rx0, ry0, rx1, ry0 + 30), 14, ROSE_GOLD)
    draw.rectangle([rx0, ry0 + 14, rx1, ry0 + 56], fill=ROSE_GOLD)
    draw_centered_text(draw, ry0 + 12, "DAY-OF TIMELINE", fnt_pt, WHITE,
                       x_center=(rx0 + rx1) // 2)

    day_of = [
        ("8:00 AM", "Bridal Suite Opens", "Wedding Planner", CHAMPAGNE),
        ("9:00 AM", "Vendor Setup Begins", "Venue Coordinator", IVORY),
        ("10:00 AM", "Hair & Makeup Starts", "Bridal Party", CHAMPAGNE),
        ("11:30 AM", "Photographer Arrives", "Lead Photographer", IVORY),
        ("12:00 PM", "Light Lunch for Party", "Caterer", CHAMPAGNE),
        ("1:00 PM", "Bride Gets Dressed", "Maid of Honor", IVORY),
        ("1:30 PM", "First Look Photos", "Photographer", CHAMPAGNE),
        ("2:00 PM", "Ceremony Begins", "Officiant", IVORY),
        ("2:30 PM", "Cocktail Hour", "Bartender", CHAMPAGNE),
        ("3:30 PM", "Reception Entrance", "DJ / Band", IVORY),
        ("4:00 PM", "First Dance", "DJ / Band", CHAMPAGNE),
        ("4:30 PM", "Dinner Service", "Caterer", IVORY),
        ("5:30 PM", "Toasts & Speeches", "Best Man / MOH", CHAMPAGNE),
        ("6:00 PM", "Cake Cutting", "Wedding Planner", IVORY),
        ("6:30 PM", "Open Dancing", "DJ / Band", CHAMPAGNE),
        ("8:00 PM", "Bouquet & Garter Toss", "DJ / Band", IVORY),
        ("9:00 PM", "Last Dance", "DJ / Band", CHAMPAGNE),
        ("9:30 PM", "Sparkler Send-Off", "Wedding Planner", IVORY),
        ("10:00 PM", "Vendor Breakdown", "Venue Coordinator", CHAMPAGNE),
        ("11:00 PM", "Suite Closes", "Venue Coordinator", IVORY),
    ]

    fnt_time = font(bold=True, size=20)
    fnt_event = font(bold=False, size=19)
    fnt_person = font(bold=False, size=16)

    dy = ry0 + 70
    row_h_day = 60
    time_col = rx0 + 20
    event_col = rx0 + 170
    person_col = rx0 + 170

    # Vertical timeline line
    line_x = rx0 + 145
    draw.line([line_x, dy, line_x, dy + len(day_of) * row_h_day - 20], fill=ROSE_GOLD, width=3)

    for i, (time, event, person, bg) in enumerate(day_of):
        ey = dy + i * row_h_day
        if ey + row_h_day > ry1 - 10:
            break
        # Background stripe
        draw.rectangle([rx0 + 10, ey, rx1 - 10, ey + row_h_day - 2], fill=bg)
        # Timeline dot
        draw_circle(draw, line_x, ey + 18, 7, ROSE_GOLD)
        draw_circle(draw, line_x, ey + 18, 4, WHITE)
        # Time
        draw.text((time_col, ey + 6), time, font=fnt_time, fill=DEEP_PLUM)
        # Event
        draw.text((event_col, ey + 4), event, font=fnt_event, fill=DARK_TEXT)
        # Person
        draw.text((person_col, ey + 30), person, font=fnt_person, fill=ROSE_GOLD)

    # Bottom tip
    tip_y = H - 155
    draw_rounded_rect(draw, (100, tip_y, W - 100, tip_y + 54), 12, CHAMPAGNE,
                      outline=GOLD, width=2)
    fnt_tip = font(bold=True, size=22)
    draw_centered_text(draw, tip_y + 12,
                       "PRO TIP:  Customize every task, time slot, and person in your spreadsheet!",
                       fnt_tip, DEEP_PLUM)

    # Bottom bar
    draw_bottom_bar(draw, "50+ TASKS  |  HOUR-BY-HOUR SCHEDULE  |  FULLY CUSTOMIZABLE",
                    y=H - 80, height=80)

    img.save("/home/user/claude-code/etsy-digital-download-4/images/04_timeline_seating.png")
    print("  [4/5] 04_timeline_seating.png")


# =====================================================================
# IMAGE 5 — Value Proposition + CTA
# =====================================================================
def create_image_05():
    img, draw = new_canvas(CREAM)

    # Header
    header_h = 115
    draw.rectangle([0, 0, W, header_h], fill=DEEP_PLUM)
    fnt_h = font(bold=True, size=50)
    draw_centered_text(draw, 28,
                       "PLAN YOUR DREAM WEDDING \u2014 STRESS FREE", fnt_h, WHITE)

    subtitle_y = header_h + 16
    fnt_sub = font(bold=False, size=26)
    draw_centered_text(draw, subtitle_y,
                       "Everything You Need, All in One Spreadsheet", fnt_sub, DARK_TEXT)

    # 6 benefits in 3x2 grid
    benefits = [
        ("SAVE THOUSANDS", "Organize vendors & budget\nto avoid costly mistakes", ROSE_GOLD),
        ("150-GUEST CAPACITY", "Track every RSVP, dietary\nneed & thank-you note", SAGE_GREEN),
        ("50+ TASK CHECKLIST", "12-month planning timeline\nso nothing slips through", GOLD),
        ("MINUTE-BY-MINUTE", "Day-of schedule from\n8 AM to 11 PM", DEEP_PLUM),
        ("FULLY CUSTOMIZABLE", "Rename, add, or remove\nanything you need", DUSTY_MAUVE),
        ("WORKS ANYWHERE", "Google Sheets & Excel\ncompatible", ROSE_GOLD),
    ]

    grid_start_y = subtitle_y + 56
    cols, rows_g = 3, 2
    card_w = 740
    card_h = 190
    gap_x = (W - cols * card_w) // (cols + 1)
    gap_y = 28
    fnt_ben_title = font(bold=True, size=28)
    fnt_ben_desc = font(bold=False, size=21)

    for idx, (title, desc, accent) in enumerate(benefits):
        col = idx % cols
        row = idx // cols
        cx0 = gap_x + col * (card_w + gap_x)
        cy0 = grid_start_y + row * (card_h + gap_y)
        cx1 = cx0 + card_w
        cy1 = cy0 + card_h

        draw_rounded_rect(draw, (cx0, cy0, cx1, cy1), 14, WHITE,
                          outline=accent, width=3)

        # Checkmark circle
        ck_cx = cx0 + 55
        ck_cy = cy0 + card_h // 2
        draw_circle(draw, ck_cx, ck_cy, 30, accent)
        # Checkmark character
        fnt_ck = font(bold=True, size=32)
        ckw, _ = text_size(draw, "\u2713", fnt_ck)
        draw.text((ck_cx - ckw // 2, ck_cy - 18), "\u2713", font=fnt_ck, fill=WHITE)

        # Title
        draw.text((cx0 + 105, cy0 + 30), title, font=fnt_ben_title, fill=DARK_TEXT)
        # Description (multiline)
        lines = desc.split("\n")
        for li, line in enumerate(lines):
            draw.text((cx0 + 105, cy0 + 72 + li * 32), line, font=fnt_ben_desc, fill=DARK_TEXT)

    # Stats bar
    stats_y = grid_start_y + rows_g * (card_h + gap_y) + 16
    draw.rectangle([0, stats_y, W, stats_y + 64], fill=DEEP_PLUM)
    fnt_stats = font(bold=True, size=26)
    stats_text = "23 Budget Categories  |  150 Guests  |  50+ Tasks  |  20 Tables  |  100 Gifts"
    draw_centered_text(draw, stats_y + 16, stats_text, fnt_stats, GOLD)

    # Testimonial / social proof
    test_y = stats_y + 64 + 24
    test_h = 140
    draw_rounded_rect(draw, (200, test_y, W - 200, test_y + test_h), 16, IVORY,
                      outline=GOLD, width=3)

    # Stars
    fnt_star = font(bold=True, size=36)
    stars = "\u2605 \u2605 \u2605 \u2605 \u2605"
    draw_centered_text(draw, test_y + 14, stars, fnt_star, GOLD)

    fnt_test = font(bold=False, size=24)
    draw_centered_text(draw, test_y + 58,
                       "\"This spreadsheet saved our wedding! We stayed on budget and",
                       fnt_test, DARK_TEXT)
    draw_centered_text(draw, test_y + 90,
                       "never forgot a single detail. Worth every penny!\"  \u2014  Verified Buyer",
                       fnt_test, DARK_TEXT)

    # "Perfect For" section
    pf_y = test_y + test_h + 24
    fnt_pf_title = font(bold=True, size=28)
    draw_centered_text(draw, pf_y, "PERFECT FOR", fnt_pf_title, DEEP_PLUM)
    pf_y += 40
    fnt_pf = font(bold=False, size=24)
    audiences = [
        "Engaged Couples", "Brides & Grooms-to-Be",
        "Wedding Coordinators", "DIY Weddings",
        "Maid of Honor & Best Man", "Parents of the Couple"
    ]
    aud_text = "  |  ".join(audiences)
    draw_centered_text(draw, pf_y, aud_text, fnt_pf, DARK_TEXT)

    # Decorative diamonds
    draw_decorative_diamonds(draw, pf_y + 46, color=GOLD, count=7)

    # CTA section
    cta_y = pf_y + 72
    draw.rectangle([0, cta_y, W, H], fill=DEEP_PLUM)

    fnt_cta1 = font(bold=True, size=38)
    draw_centered_text(draw, cta_y + 22,
                       "YOUR DREAM WEDDING STARTS WITH A PLAN", fnt_cta1, WHITE)

    # Button
    btn_y = cta_y + 80
    btn_w, btn_h = 700, 70
    btn_x = W // 2 - btn_w // 2
    draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), 35, GOLD)
    fnt_btn = font(bold=True, size=32)
    draw_centered_text(draw, btn_y + 16, "INSTANT DIGITAL DOWNLOAD", fnt_btn, WHITE)

    # Price line
    fnt_price = font(bold=True, size=28)
    draw_centered_text(draw, btn_y + btn_h + 22,
                       "$12.99  |  9 Professional Tabs  |  Google Sheets + Excel",
                       fnt_price, CHAMPAGNE)

    img.save("/home/user/claude-code/etsy-digital-download-4/images/05_value_proposition.png")
    print("  [5/5] 05_value_proposition.png")


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("Generating Etsy listing images (2700x2025)...\n")
    create_image_01()
    create_image_02()
    create_image_03()
    create_image_04()
    create_image_05()
    print("\nAll 5 images saved to /home/user/claude-code/etsy-digital-download-4/images/")
