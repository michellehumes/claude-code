#!/usr/bin/env python3
"""
Generate 5 professional Etsy listing images for:
Product 4: "Wedding Planner & Budget Bundle 2026"
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

# ── Output ──────────────────────────────────────────────────────────
OUT = "/home/user/claude-code/etsy-digital-download-4/images"
os.makedirs(OUT, exist_ok=True)
W, H = 2700, 2025

# ── Fonts ───────────────────────────────────────────────────────────
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ── Palette ─────────────────────────────────────────────────────────
DEEP_PLUM   = (74, 32, 64)
ROSE_GOLD   = (183, 110, 121)
BLUSH       = (232, 196, 200)
CHAMPAGNE   = (247, 231, 206)
SAGE_GREEN  = (156, 175, 136)
DUSTY_MAUVE = (201, 169, 166)
GOLD        = (197, 165, 90)
IVORY       = (255, 255, 240)
WHITE       = (255, 255, 255)
DARK_TEXT   = (44, 44, 44)
LIGHT_PLUM  = (120, 70, 110)
VERY_LIGHT_BLUSH = (245, 230, 232)
CREAM       = (252, 248, 240)

# ── Helper: vertical gradient ──────────────────────────────────────
def gradient_bg(c1, c2, w=W, h=H):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img

def radial_gradient_bg(center_color, edge_color, w=W, h=H):
    img = Image.new("RGB", (w, h))
    px = img.load()
    cx, cy = w // 2, h // 2
    max_dist = math.sqrt(cx*cx + cy*cy)
    for y in range(h):
        for x in range(w):
            d = math.sqrt((x - cx)**2 + (y - cy)**2) / max_dist
            d = min(d, 1.0)
            r = int(center_color[0] + (edge_color[0] - center_color[0]) * d)
            g = int(center_color[1] + (edge_color[1] - center_color[1]) * d)
            b = int(center_color[2] + (edge_color[2] - center_color[2]) * d)
            px[x, y] = (r, g, b)
    return img

# ── Helper: rounded rectangle ──────────────────────────────────────
def rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = bbox
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    if fill:
        draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
        draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
        draw.pieslice([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=fill)
        draw.pieslice([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + r, y1, x2 - r, y1], fill=outline, width=width)
        draw.line([x1 + r, y2, x2 - r, y2], fill=outline, width=width)
        draw.line([x1, y1 + r, x1, y2 - r], fill=outline, width=width)
        draw.line([x2, y1 + r, x2, y2 - r], fill=outline, width=width)

# ── Helper: center text ────────────────────────────────────────────
def center_text(draw, text, y, fnt, fill, w=W):
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) // 2, y), text, font=fnt, fill=fill)

def text_width(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0]

def text_height(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[3] - bb[1]

# ── Helper: draw iPad mockup ──────────────────────────────────────
def draw_ipad(draw, img, x, y, w, h, screen_content_fn, shadow=True, bezel_color=(30, 30, 30)):
    """Draw iPad frame and call screen_content_fn to fill screen area."""
    bezel = max(8, int(w * 0.025))
    corner_r = max(12, int(w * 0.04))

    # Shadow
    if shadow:
        for s in range(15, 0, -1):
            alpha_color = tuple(max(0, c - 30 + s*2) for c in (100, 100, 100))
            # Approximate shadow with offset rects
            sx, sy = x + s + 4, y + s + 4
            rounded_rect(draw, (sx, sy, sx + w, sy + h), corner_r + 4,
                        fill=(min(255, 180 + s*5), min(255, 175 + s*5), min(255, 170 + s*5)))

    # Outer body
    rounded_rect(draw, (x, y, x + w, y + h), corner_r, fill=bezel_color)

    # Inner bezel highlight
    rounded_rect(draw, (x + 1, y + 1, x + w - 1, y + h - 1), corner_r - 1,
                fill=tuple(min(255, c + 30) for c in bezel_color))
    rounded_rect(draw, (x + 2, y + 2, x + w - 2, y + h - 2), corner_r - 2,
                fill=bezel_color)

    # Screen area
    sx = x + bezel
    sy = y + bezel
    sw = w - 2 * bezel
    sh = h - 2 * bezel
    screen_r = max(4, corner_r - bezel)
    rounded_rect(draw, (sx, sy, sx + sw, sy + sh), screen_r, fill=WHITE)

    # Call content function
    screen_content_fn(draw, img, sx, sy, sw, sh)

    # Camera dot
    cam_r = max(3, int(w * 0.006))
    cam_x = x + w // 2
    cam_y = y + bezel // 2
    draw.ellipse([cam_x - cam_r, cam_y - cam_r, cam_x + cam_r, cam_y + cam_r],
                fill=(50, 50, 55))

# ── Helper: draw tab bar ──────────────────────────────────────────
ALL_TABS = ["Dashboard", "Budget", "Guest List", "Vendors", "Timeline",
            "Seating", "Day-Of", "Gifts", "How to Use"]

def draw_tab_bar(draw, sx, sy, sw, active_idx=1, tab_h=28):
    """Draw a tab bar at top of screen area."""
    tab_w = sw // len(ALL_TABS)
    for i, tab in enumerate(ALL_TABS):
        tx = sx + i * tab_w
        if i == active_idx:
            rounded_rect(draw, (tx, sy, tx + tab_w - 1, sy + tab_h), 4, fill=DEEP_PLUM)
            f = font(BOLD, max(9, tab_h // 3))
            bb = draw.textbbox((0, 0), tab, font=f)
            tw = bb[2] - bb[0]
            draw.text((tx + (tab_w - tw) // 2, sy + 4), tab, font=f, fill=WHITE)
        else:
            rounded_rect(draw, (tx, sy, tx + tab_w - 1, sy + tab_h), 4, fill=CHAMPAGNE)
            f = font(REG, max(9, tab_h // 3))
            bb = draw.textbbox((0, 0), tab, font=f)
            tw = bb[2] - bb[0]
            draw.text((tx + (tab_w - tw) // 2, sy + 4), tab, font=f, fill=DEEP_PLUM)
    # Divider
    draw.line([(sx, sy + tab_h), (sx + sw, sy + tab_h)], fill=DUSTY_MAUVE, width=1)
    return tab_h + 1

# ── Helper: draw spreadsheet table ────────────────────────────────
def draw_table(draw, sx, sy, sw, sh, headers, rows, col_widths=None,
               header_bg=DEEP_PLUM, header_fg=WHITE, alt_bg=CREAM,
               row_h=None, font_size=None, highlight_last=False):
    """Draw a spreadsheet-like table. Returns bottom y."""
    n_cols = len(headers)
    if font_size is None:
        font_size = max(10, min(18, sh // (len(rows) + 3)))
    if row_h is None:
        row_h = max(16, font_size + 8)

    hf = font(BOLD, font_size)
    rf = font(REG, font_size)

    if col_widths is None:
        col_widths = [sw // n_cols] * n_cols
        remaining = sw - sum(col_widths)
        col_widths[0] += remaining

    # Header
    cx = sx
    for i, hdr in enumerate(headers):
        rounded_rect(draw, (cx, sy, cx + col_widths[i], sy + row_h), 0, fill=header_bg)
        draw.text((cx + 4, sy + 2), hdr, font=hf, fill=header_fg)
        cx += col_widths[i]

    # Rows
    cy = sy + row_h
    for ri, row in enumerate(rows):
        is_last = (ri == len(rows) - 1) and highlight_last
        bg = CHAMPAGNE if is_last else (WHITE if ri % 2 == 0 else alt_bg)
        cx = sx
        for ci, cell in enumerate(row):
            draw.rectangle([cx, cy, cx + col_widths[ci], cy + row_h], fill=bg)
            draw.line([(cx, cy), (cx + col_widths[ci], cy)], fill=DUSTY_MAUVE, width=1)
            color = DEEP_PLUM if is_last else DARK_TEXT
            f_use = hf if is_last else rf
            draw.text((cx + 4, cy + 2), str(cell), font=f_use, fill=color)
            cx += col_widths[ci]
        cy += row_h

    # Grid lines
    draw.rectangle([sx, sy, sx + sw, cy], outline=DUSTY_MAUVE, width=1)
    return cy

# ── Helper: draw pie chart ─────────────────────────────────────────
def draw_pie_chart(draw, cx, cy, radius, slices):
    """slices: list of (label, value, color)."""
    total = sum(v for _, v, _ in slices)
    if total == 0:
        return
    start = -90
    for label, val, color in slices:
        extent = (val / total) * 360
        draw.pieslice([cx - radius, cy - radius, cx + radius, cy + radius],
                     start, start + extent, fill=color, outline=WHITE, width=1)
        start += extent

def draw_pie_legend(draw, x, y, slices, fnt_size=13):
    """Draw legend for pie chart."""
    f = font(REG, fnt_size)
    total = sum(v for _, v, _ in slices)
    for i, (label, val, color) in enumerate(slices):
        ly = y + i * (fnt_size + 6)
        draw.rectangle([x, ly + 2, x + fnt_size, ly + 2 + fnt_size], fill=color, outline=DARK_TEXT)
        pct = f"{val/total*100:.0f}%" if total > 0 else ""
        draw.text((x + fnt_size + 5, ly), f"{label} {pct}", font=f, fill=DARK_TEXT)

# ── Helper: annotation arrow + label ──────────────────────────────
def draw_annotation(draw, text, tx, ty, arrow_to_x, arrow_to_y, color=DEEP_PLUM, fnt_size=22, pill=True):
    """Draw an annotation label with a line pointing to target."""
    f = font(BOLD, fnt_size)
    bb = draw.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 10

    if pill:
        rounded_rect(draw, (tx - pad, ty - pad//2, tx + tw + pad, ty + th + pad//2),
                     12, fill=color)
        draw.text((tx, ty), text, font=f, fill=WHITE)
    else:
        draw.text((tx, ty), text, font=f, fill=color)

    # Arrow line
    draw.line([(tx + tw//2, ty + th + pad//2 if arrow_to_y > ty else ty - pad//2),
               (arrow_to_x, arrow_to_y)], fill=color, width=3)
    # Arrowhead dot
    draw.ellipse([arrow_to_x - 5, arrow_to_y - 5, arrow_to_x + 5, arrow_to_y + 5], fill=color)

# ── Helper: feature pill ──────────────────────────────────────────
def draw_pill(draw, text, cx, cy, bg=DEEP_PLUM, fg=WHITE, fnt_size=22, pad_x=20, pad_y=8):
    f = font(BOLD, fnt_size)
    bb = draw.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x1 = cx - tw//2 - pad_x
    y1 = cy - th//2 - pad_y
    x2 = cx + tw//2 + pad_x
    y2 = cy + th//2 + pad_y
    rounded_rect(draw, (x1, y1, x2, y2), (y2 - y1)//2, fill=bg)
    draw.text((cx - tw//2, cy - th//2), text, font=f, fill=fg)
    return (x1, y1, x2, y2)

# ── Helper: status badge ──────────────────────────────────────────
def draw_badge(draw, text, x, y, bg, fg=WHITE, fnt_size=12, pad_x=6, pad_y=2):
    f = font(BOLD, fnt_size)
    bb = draw.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    rounded_rect(draw, (x, y, x + tw + 2*pad_x, y + th + 2*pad_y), (th + 2*pad_y)//2, fill=bg)
    draw.text((x + pad_x, y + pad_y), text, font=f, fill=fg)
    return x + tw + 2*pad_x + 4

# ── Helper: stars ──────────────────────────────────────────────────
def draw_stars(draw, cx, y, n=5, size=20, color=GOLD):
    total_w = n * size * 2.2
    sx = cx - total_w // 2
    for i in range(n):
        x = int(sx + i * size * 2.2 + size)
        # Simple 5-pointed star
        points = []
        for j in range(10):
            angle = math.radians(-90 + j * 36)
            r = size if j % 2 == 0 else size * 0.45
            points.append((x + r * math.cos(angle), y + size + r * math.sin(angle)))
        draw.polygon(points, fill=color)


# ══════════════════════════════════════════════════════════════════
# IMAGE 1: Hero / Main Listing
# ══════════════════════════════════════════════════════════════════
def make_image_1():
    print("  [1/5] Hero Main Listing...")
    img = gradient_bg(CHAMPAGNE, IVORY)
    draw = ImageDraw.Draw(img)

    # Subtle decorative dots pattern
    for row in range(0, H, 80):
        for col in range(0, W, 80):
            draw.ellipse([col-1, row-1, col+1, row+1], fill=(*BLUSH, ))

    # ── Title block (top) ──
    title_f = font(BOLD, 72)
    center_text(draw, "WEDDING PLANNER & BUDGET BUNDLE", 40, title_f, DEEP_PLUM)

    # 2026 badge
    badge_f = font(BOLD, 50)
    bb = draw.textbbox((0, 0), "2026", font=badge_f)
    bw = bb[2] - bb[0]
    bx = W // 2 - bw // 2
    rounded_rect(draw, (bx - 20, 120, bx + bw + 20, 180), 18, fill=GOLD)
    draw.text((bx, 125), "2026", font=badge_f, fill=WHITE)

    # ── Feature pills ──
    pills = ["9 Tabs", "150 Guests", "67 Tasks", "23 Budget Categories"]
    pill_y = 205
    pill_spacing = W // (len(pills) + 1)
    for i, p in enumerate(pills):
        px = pill_spacing * (i + 1)
        draw_pill(draw, p, px, pill_y, bg=ROSE_GOLD, fg=WHITE, fnt_size=24)

    # ── iPad showing Budget Tracker ──
    ipad_x, ipad_y = 300, 270
    ipad_w, ipad_h = 1500, 1100

    def budget_screen(d, im, sx, sy, sw, sh):
        # Tab bar
        tab_off = draw_tab_bar(d, sx, sy, sw, active_idx=1, tab_h=30)
        cy = sy + tab_off + 2

        # Title inside screen
        tf = font(BOLD, 20)
        d.text((sx + 10, cy), "Budget Tracker — Wedding 2026", font=tf, fill=DEEP_PLUM)
        cy += 28

        # Summary bar
        sf = font(BOLD, 16)
        d.text((sx + 10, cy), "Total Budget: $30,000", font=sf, fill=DARK_TEXT)
        d.text((sx + 280, cy), "Spent: $27,350", font=sf, fill=ROSE_GOLD)
        d.text((sx + 500, cy), "Remaining: $2,650", font=sf, fill=SAGE_GREEN)
        cy += 26

        # Budget table
        headers = ["Category", "Estimated", "Actual", "Deposit", "Balance"]
        col_w = [sw * 3 // 10, sw * 2 // 10, sw * 2 // 10, sw * 15 // 100, sw * 15 // 100]
        # Adjust to fill
        diff = sw - sum(col_w)
        col_w[0] += diff

        rows_data = [
            ("Venue & Reception", "$8,000", "$7,800", "$3,000", "$4,800"),
            ("Catering & Bar", "$6,500", "$6,200", "$2,000", "$4,200"),
            ("Photography", "$3,500", "$3,500", "$1,500", "$2,000"),
            ("Florist & Decor", "$2,000", "$1,800", "$500", "$1,300"),
            ("DJ / Band", "$1,500", "$1,400", "$500", "$900"),
            ("Wedding Cake", "$800", "$750", "$200", "$550"),
            ("Invitations", "$600", "$580", "$580", "$0"),
            ("Officiant", "$400", "$400", "$200", "$200"),
            ("Hair & Makeup", "$1,200", "$1,200", "$0", "$1,200"),
            ("Transportation", "$800", "$720", "$300", "$420"),
            ("Favors & Gifts", "$500", "$500", "$0", "$500"),
            ("Attire & Accessories", "$2,500", "$2,500", "$1,000", "$1,500"),
            ("TOTAL", "$30,000", "$27,350", "$9,780", "$17,570"),
        ]

        bottom = draw_table(d, sx + 2, cy, sw - 4, sh - (cy - sy) - 10,
                           headers, rows_data, col_widths=col_w,
                           font_size=15, row_h=22, highlight_last=True)

        # Pie chart area to the right — overlay
        pie_cx = sx + sw - 160
        pie_cy = cy + 120
        pie_r = 80
        slices = [
            ("Venue", 8000, DEEP_PLUM),
            ("Catering", 6500, ROSE_GOLD),
            ("Photo", 3500, SAGE_GREEN),
            ("Florist", 2000, GOLD),
            ("DJ", 1500, DUSTY_MAUVE),
            ("Other", 8500, BLUSH),
        ]

        # White background for pie
        d.rectangle([pie_cx - pie_r - 20, pie_cy - pie_r - 20,
                     pie_cx + pie_r + 20, pie_cy + pie_r + 90], fill=WHITE)
        d.rectangle([pie_cx - pie_r - 20, pie_cy - pie_r - 20,
                     pie_cx + pie_r + 20, pie_cy + pie_r + 90], outline=DUSTY_MAUVE, width=1)

        pf = font(BOLD, 12)
        d.text((pie_cx - 40, pie_cy - pie_r - 16), "Budget Breakdown", font=pf, fill=DEEP_PLUM)
        draw_pie_chart(d, pie_cx, pie_cy + 5, pie_r, slices)

        # Mini legend
        lf = font(REG, 10)
        ly = pie_cy + pie_r + 10
        for i, (lbl, val, clr) in enumerate(slices[:3]):
            d.rectangle([pie_cx - pie_r, ly, pie_cx - pie_r + 8, ly + 8], fill=clr)
            d.text((pie_cx - pie_r + 12, ly - 2), f"{lbl} {val/300:.0f}%", font=lf, fill=DARK_TEXT)
            ly += 14
        for i, (lbl, val, clr) in enumerate(slices[3:]):
            d.rectangle([pie_cx, ly - 42 + i*14, pie_cx + 8, ly - 34 + i*14], fill=clr)
            d.text((pie_cx + 12, ly - 44 + i*14), f"{lbl} {val/300:.0f}%", font=lf, fill=DARK_TEXT)

    draw_ipad(draw, img, ipad_x, ipad_y, ipad_w, ipad_h, budget_screen)

    # ── Annotations ──
    draw_annotation(draw, "23 WEDDING CATEGORIES", 80, 500, ipad_x + 50, 650,
                   color=DEEP_PLUM, fnt_size=24)
    draw_annotation(draw, "AUTO BALANCE DUE", 80, 900, ipad_x + 50, 1050,
                   color=ROSE_GOLD, fnt_size=24)
    draw_annotation(draw, "BUDGET PIE CHART", 1900, 450, ipad_x + ipad_w - 100, 650,
                   color=SAGE_GREEN, fnt_size=24)

    # ── Right side feature stack ──
    ry = 550
    features_right = [
        ("Auto-Calculating Totals", DEEP_PLUM),
        ("Deposit Tracking", ROSE_GOLD),
        ("23 Budget Categories", SAGE_GREEN),
        ("Real-Time Balance", GOLD),
        ("Pie Chart Overview", DUSTY_MAUVE),
    ]
    for txt, clr in features_right:
        rf = font(BOLD, 22)
        bb = draw.textbbox((0, 0), txt, font=rf)
        tw = bb[2] - bb[0]
        rx = 2000
        rounded_rect(draw, (rx, ry, rx + tw + 30, ry + 38), 8, fill=clr)
        draw.text((rx + 15, ry + 6), txt, font=rf, fill=WHITE)
        ry += 50

    # ── Bottom bar ──
    rounded_rect(draw, (0, H - 110, W, H), 0, fill=DEEP_PLUM)
    bf = font(BOLD, 36)
    center_text(draw, "INSTANT DIGITAL DOWNLOAD  •  GOOGLE SHEETS  •  EXCEL  •  LIBREOFFICE", H - 90, bf, CHAMPAGNE)

    # Decorative corners
    for corner_x, corner_y in [(30, 30), (W - 80, 30), (30, H - 140), (W - 80, H - 140)]:
        draw.rectangle([corner_x, corner_y, corner_x + 50, corner_y + 3], fill=GOLD)
        draw.rectangle([corner_x, corner_y, corner_x + 3, corner_y + 50], fill=GOLD)

    img.save(f"{OUT}/01_hero_main_listing.png", quality=95)
    print("    -> 01_hero_main_listing.png saved")


# ══════════════════════════════════════════════════════════════════
# IMAGE 2: What's Included — 8 mini iPads
# ══════════════════════════════════════════════════════════════════
def make_image_2():
    print("  [2/5] What's Included...")
    img = gradient_bg(VERY_LIGHT_BLUSH, BLUSH)
    draw = ImageDraw.Draw(img)

    # Title
    tf = font(BOLD, 56)
    center_text(draw, "EVERYTHING YOU NEED TO PLAN YOUR DREAM WEDDING", 35, tf, DEEP_PLUM)

    # Subtitle line
    sf = font(REG, 30)
    center_text(draw, "8 Professionally Designed Spreadsheet Tabs — Ready to Use", 100, sf, ROSE_GOLD)

    # Decorative divider
    draw.line([(W//2 - 300, 145), (W//2 + 300, 145)], fill=GOLD, width=3)

    # 8 mini iPads in 4x2 grid
    pad = 40
    grid_y_start = 170
    grid_cols, grid_rows = 4, 2
    ipad_w = (W - pad * (grid_cols + 1)) // grid_cols
    ipad_h = (H - grid_y_start - 280) // grid_rows  # leave room for labels + bottom

    tab_configs = [
        ("Dashboard", 0, "Countdown, Budget, RSVPs"),
        ("Budget Tracker", 1, "Expenses & Pie Chart"),
        ("Guest List", 2, "RSVPs & Dietary Notes"),
        ("Vendor Tracker", 3, "Payments & Contacts"),
        ("Timeline", 4, "67 Tasks by Timeframe"),
        ("Seating Chart", 5, "Table Assignments"),
        ("Day-Of Timeline", 6, "Hour-by-Hour Schedule"),
        ("Gift Tracker", 7, "Gifts & Thank-Yous"),
    ]

    def make_mini_screen_fn(tab_idx, tab_type):
        def fn(d, im, sx, sy, sw, sh):
            # Header bar
            hh = 18
            rounded_rect(d, (sx, sy, sx + sw, sy + hh), 0, fill=DEEP_PLUM)
            hf = font(BOLD, 11)
            d.text((sx + 4, sy + 2), ALL_TABS[tab_idx] if tab_idx < len(ALL_TABS) else tab_type, font=hf, fill=WHITE)

            cy = sy + hh + 3
            rf = font(REG, 10)
            bf = font(BOLD, 10)
            mf = font(REG, 9)

            if tab_type == "Dashboard":
                # Countdown
                d.text((sx + 4, cy), "Days Until Wedding:", font=bf, fill=DEEP_PLUM); cy += 14
                rounded_rect(d, (sx + 4, cy, sx + 80, cy + 22), 4, fill=GOLD)
                d.text((sx + 14, cy + 4), "187 Days", font=bf, fill=WHITE); cy += 28
                d.text((sx + 4, cy), "Budget: $30,000", font=rf, fill=DARK_TEXT); cy += 14
                d.text((sx + 4, cy), "Spent:  $27,350", font=rf, fill=ROSE_GOLD); cy += 14
                d.text((sx + 4, cy), "RSVPs:  98 / 150", font=rf, fill=SAGE_GREEN); cy += 14
                d.text((sx + 4, cy), "Tasks:  42 / 67 Done", font=rf, fill=DARK_TEXT); cy += 16
                # Mini progress bar
                bar_w = sw - 10
                d.rectangle([sx + 4, cy, sx + 4 + bar_w, cy + 8], fill=CHAMPAGNE, outline=DUSTY_MAUVE)
                d.rectangle([sx + 4, cy, sx + 4 + int(bar_w * 0.63), cy + 8], fill=SAGE_GREEN)
                cy += 14
                d.text((sx + 4, cy), "Vendors: 8 Booked", font=rf, fill=DARK_TEXT)

            elif tab_type == "Budget Tracker":
                headers = ["Category", "Est.", "Actual"]
                rows = [("Venue", "$8K", "$7.8K"), ("Catering", "$6.5K", "$6.2K"),
                        ("Photo", "$3.5K", "$3.5K"), ("Florist", "$2K", "$1.8K"),
                        ("DJ", "$1.5K", "$1.4K"), ("Cake", "$800", "$750"),
                        ("TOTAL", "$30K", "$27.4K")]
                rh = min(14, (sh - 30) // (len(rows) + 1))
                # Headers
                cw = [sw * 4 // 10, sw * 3 // 10, sw * 3 // 10]
                cx = sx + 2
                for i, h in enumerate(headers):
                    d.rectangle([cx, cy, cx + cw[i] - 1, cy + rh], fill=DEEP_PLUM)
                    d.text((cx + 2, cy + 1), h, font=mf, fill=WHITE)
                    cx += cw[i]
                cy += rh
                for ri, row in enumerate(rows):
                    bg = CHAMPAGNE if ri == len(rows) - 1 else (WHITE if ri % 2 == 0 else CREAM)
                    cx = sx + 2
                    for ci, cell in enumerate(row):
                        d.rectangle([cx, cy, cx + cw[ci] - 1, cy + rh], fill=bg)
                        d.text((cx + 2, cy + 1), cell, font=mf, fill=DEEP_PLUM if ri == len(rows)-1 else DARK_TEXT)
                        cx += cw[ci]
                    cy += rh
                # Mini pie
                pie_cy = cy + 20
                if pie_cy + 20 < sy + sh:
                    slices = [("V", 8, DEEP_PLUM), ("C", 6.5, ROSE_GOLD), ("P", 3.5, SAGE_GREEN), ("O", 12, BLUSH)]
                    draw_pie_chart(d, sx + sw // 2, pie_cy, min(18, (sy + sh - pie_cy) // 2 - 2), slices)

            elif tab_type == "Guest List":
                guests = [("Sarah & Tom", "Attending", "None"),
                          ("Emily R.", "Attending", "Vegan"),
                          ("James K.", "Pending", "None"),
                          ("Lisa & Mark", "Attending", "GF"),
                          ("Amy P.", "Declined", "None"),
                          ("Chris W.", "Pending", "Nut-free"),
                          ("Rachel B.", "Attending", "None"),
                          ("David L.", "Attending", "Veg")]
                rh = min(14, (sh - 24) // (len(guests) + 1))
                # Header
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                d.text((sx + 4, cy + 1), "Guest", font=mf, fill=WHITE)
                d.text((sx + sw//2, cy + 1), "RSVP", font=mf, fill=WHITE)
                d.text((sx + sw - 40, cy + 1), "Diet", font=mf, fill=WHITE)
                cy += rh
                for gi, (name, rsvp, diet) in enumerate(guests):
                    bg = WHITE if gi % 2 == 0 else CREAM
                    d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                    d.text((sx + 4, cy + 1), name, font=mf, fill=DARK_TEXT)
                    badge_clr = SAGE_GREEN if rsvp == "Attending" else (GOLD if rsvp == "Pending" else ROSE_GOLD)
                    rounded_rect(d, (sx + sw//2, cy + 1, sx + sw//2 + 42, cy + rh - 1), 4, fill=badge_clr)
                    d.text((sx + sw//2 + 3, cy + 1), rsvp[:5], font=mf, fill=WHITE)
                    d.text((sx + sw - 40, cy + 1), diet, font=mf, fill=DARK_TEXT)
                    cy += rh

            elif tab_type == "Vendor Tracker":
                vendors = [("Venue: Grand Hall", "Paid"),
                           ("Caterer: Bella", "Deposit"),
                           ("Photo: Art Studio", "Paid"),
                           ("Florist: Bloom", "Pending"),
                           ("DJ: SoundWave", "Deposit"),
                           ("Cake: Sweet", "Pending"),
                           ("Officiant: Rev. J", "Paid"),
                           ("Makeup: Glam", "Deposit")]
                rh = min(14, (sh - 24) // (len(vendors) + 1))
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                d.text((sx + 4, cy + 1), "Vendor", font=mf, fill=WHITE)
                d.text((sx + sw - 50, cy + 1), "Status", font=mf, fill=WHITE)
                cy += rh
                for vi, (v, st) in enumerate(vendors):
                    bg = WHITE if vi % 2 == 0 else CREAM
                    d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                    d.text((sx + 4, cy + 1), v, font=mf, fill=DARK_TEXT)
                    sc = SAGE_GREEN if st == "Paid" else (GOLD if st == "Deposit" else ROSE_GOLD)
                    rounded_rect(d, (sx + sw - 52, cy + 1, sx + sw - 4, cy + rh - 1), 4, fill=sc)
                    d.text((sx + sw - 50, cy + 1), st, font=mf, fill=WHITE)
                    cy += rh

            elif tab_type == "Timeline":
                tasks = [("12 Mo", "Book venue", "Done"),
                         ("12 Mo", "Set budget", "Done"),
                         ("9 Mo", "Book caterer", "Done"),
                         ("9 Mo", "Book photographer", "Done"),
                         ("6 Mo", "Order invitations", "Done"),
                         ("6 Mo", "Book florist", "In Prog"),
                         ("3 Mo", "Final menu", "Not Yet"),
                         ("1 Mo", "Seating chart", "Not Yet")]
                rh = min(14, (sh - 24) // (len(tasks) + 1))
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                d.text((sx + 4, cy + 1), "When", font=mf, fill=WHITE)
                d.text((sx + 50, cy + 1), "Task", font=mf, fill=WHITE)
                d.text((sx + sw - 46, cy + 1), "Status", font=mf, fill=WHITE)
                cy += rh
                for ti, (when, task, status) in enumerate(tasks):
                    bg = WHITE if ti % 2 == 0 else CREAM
                    d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                    d.text((sx + 4, cy + 1), when, font=mf, fill=DARK_TEXT)
                    d.text((sx + 50, cy + 1), task, font=mf, fill=DARK_TEXT)
                    sc = SAGE_GREEN if status == "Done" else (GOLD if "Prog" in status else DUSTY_MAUVE)
                    rounded_rect(d, (sx + sw - 48, cy + 1, sx + sw - 4, cy + rh - 1), 4, fill=sc)
                    d.text((sx + sw - 46, cy + 1), status[:6], font=mf, fill=WHITE)
                    cy += rh

            elif tab_type == "Seating Chart":
                tables = [("Table 1", "Sarah, Tom, Emily, James"),
                          ("Table 2", "Lisa, Mark, Amy, Chris"),
                          ("Table 3", "Rachel, David, Nick, Jen"),
                          ("Table 4", "Mom, Dad, Aunt Sue, Uncle B"),
                          ("Table 5", "Best Man +1, MOH +1"),
                          ("Table 6", "Cousins: Pat, Mike, Dana"),
                          ("Head", "Bride, Groom, Wedding Party")]
                rh = min(14, (sh - 24) // (len(tables) + 1))
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                d.text((sx + 4, cy + 1), "Table", font=mf, fill=WHITE)
                d.text((sx + 56, cy + 1), "Guests", font=mf, fill=WHITE)
                cy += rh
                for si, (tbl, guests_txt) in enumerate(tables):
                    bg = CHAMPAGNE if "Head" in tbl else (WHITE if si % 2 == 0 else CREAM)
                    d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                    d.text((sx + 4, cy + 1), tbl, font=mf, fill=DEEP_PLUM)
                    d.text((sx + 56, cy + 1), guests_txt[:28], font=mf, fill=DARK_TEXT)
                    cy += rh

            elif tab_type == "Day-Of Timeline":
                schedule = [("8:00 AM", "Hair & Makeup"),
                            ("10:00 AM", "First Look Photos"),
                            ("11:30 AM", "Bridal Party Ready"),
                            ("1:00 PM", "Guests Arrive"),
                            ("2:00 PM", "Ceremony"),
                            ("3:00 PM", "Cocktail Hour"),
                            ("5:00 PM", "Reception"),
                            ("6:00 PM", "First Dance"),
                            ("10:00 PM", "Sparkler Exit")]
                rh = min(14, (sh - 24) // (len(schedule) + 1))
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                d.text((sx + 4, cy + 1), "Time", font=mf, fill=WHITE)
                d.text((sx + 70, cy + 1), "Event", font=mf, fill=WHITE)
                cy += rh
                for di, (time, event) in enumerate(schedule):
                    bg = WHITE if di % 2 == 0 else CREAM
                    d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                    d.text((sx + 4, cy + 1), time, font=mf, fill=DEEP_PLUM)
                    d.text((sx + 70, cy + 1), event, font=mf, fill=DARK_TEXT)
                    cy += rh

            elif tab_type == "Gift Tracker":
                gifts = [("Blender", "Sarah T.", "Received", "Sent"),
                         ("Dinnerware", "Emily R.", "Received", "Sent"),
                         ("Gift Card $100", "James K.", "Received", "Pending"),
                         ("Towel Set", "Lisa M.", "Shipped", "—"),
                         ("Vase", "Amy P.", "Received", "Sent"),
                         ("Cookware", "Chris W.", "Received", "Pending")]
                rh = min(14, (sh - 24) // (len(gifts) + 1))
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                cws = [sw * 28//100, sw * 22//100, sw * 25//100, sw * 25//100]
                heads = ["Gift", "From", "Status", "Thank You"]
                cx2 = sx + 2
                for hi, h in enumerate(heads):
                    d.text((cx2 + 2, cy + 1), h, font=mf, fill=WHITE)
                    cx2 += cws[hi]
                cy += rh
                for gi2, (gift, frm, st, ty) in enumerate(gifts):
                    bg = WHITE if gi2 % 2 == 0 else CREAM
                    d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                    cx2 = sx + 2
                    for ci2, cell in enumerate([gift, frm, st, ty]):
                        d.text((cx2 + 2, cy + 1), cell[:10], font=mf, fill=DARK_TEXT)
                        cx2 += cws[ci2]
                    cy += rh

        return fn

    for idx, (tab_name, tab_idx, desc) in enumerate(tab_configs):
        col = idx % grid_cols
        row = idx // grid_cols
        ix = pad + col * (ipad_w + pad)
        iy = grid_y_start + row * (ipad_h + 70)

        draw_ipad(draw, img, ix, iy, ipad_w, ipad_h,
                 make_mini_screen_fn(tab_idx, tab_name), shadow=True)

        # Label
        lf = font(BOLD, 22)
        bb = draw.textbbox((0, 0), tab_name, font=lf)
        lw = bb[2] - bb[0]
        draw.text((ix + ipad_w // 2 - lw // 2, iy + ipad_h + 6), tab_name, font=lf, fill=DEEP_PLUM)
        df = font(REG, 17)
        bb2 = draw.textbbox((0, 0), desc, font=df)
        dw = bb2[2] - bb2[0]
        draw.text((ix + ipad_w // 2 - dw // 2, iy + ipad_h + 32), desc, font=df, fill=ROSE_GOLD)

    # Bottom bar
    rounded_rect(draw, (0, H - 90, W, H), 0, fill=DEEP_PLUM)
    bf = font(BOLD, 32)
    center_text(draw, "8 TABS  •  150 GUESTS  •  67 TASKS  •  23 BUDGET CATEGORIES  •  INSTANT DOWNLOAD", H - 75, bf, CHAMPAGNE)

    img.save(f"{OUT}/02_whats_included.png", quality=95)
    print("    -> 02_whats_included.png saved")


# ══════════════════════════════════════════════════════════════════
# IMAGE 3: Budget & Guest List Preview — Two Overlapping iPads
# ══════════════════════════════════════════════════════════════════
def make_image_3():
    print("  [3/5] Budget & Guest Preview...")
    img = gradient_bg(IVORY, CHAMPAGNE)
    draw = ImageDraw.Draw(img)

    # Title
    tf = font(BOLD, 54)
    center_text(draw, 'BUDGET & GUEST LIST \u2014 ALL IN ONE PLACE', 30, tf, DEEP_PLUM)

    # Stats line
    sf = font(BOLD, 28)
    center_text(draw, "23 Categories  |  150 Guests  |  Auto Totals  |  RSVP Tracking", 95, sf, ROSE_GOLD)

    draw.line([(W//2 - 400, 140), (W//2 + 400, 140)], fill=GOLD, width=3)

    # ── MAIN iPad: Budget Tracker ──
    def budget_full(d, im, sx, sy, sw, sh):
        tab_off = draw_tab_bar(d, sx, sy, sw, active_idx=1, tab_h=28)
        cy = sy + tab_off + 4

        tf2 = font(BOLD, 18)
        d.text((sx + 8, cy), "Wedding Budget Tracker 2026", font=tf2, fill=DEEP_PLUM)
        cy += 24

        # Summary boxes
        boxes = [("Total Budget", "$30,000", DEEP_PLUM), ("Total Spent", "$27,350", ROSE_GOLD),
                 ("Remaining", "$2,650", SAGE_GREEN), ("Deposits", "$9,780", GOLD)]
        bw = (sw - 20) // 4
        for bi, (lbl, val, clr) in enumerate(boxes):
            bx = sx + 6 + bi * bw
            rounded_rect(d, (bx, cy, bx + bw - 4, cy + 38), 6, fill=clr)
            bf2 = font(BOLD, 12)
            d.text((bx + 6, cy + 3), lbl, font=bf2, fill=WHITE)
            vf = font(BOLD, 15)
            d.text((bx + 6, cy + 18), val, font=vf, fill=WHITE)
        cy += 46

        headers = ["Category", "Estimated", "Actual", "Deposit", "Balance", "Status"]
        rows_data = [
            ("Venue & Reception", "$8,000", "$7,800", "$3,000", "$4,800", "On Track"),
            ("Catering & Bar", "$6,500", "$6,200", "$2,000", "$4,200", "On Track"),
            ("Photography", "$3,500", "$3,500", "$1,500", "$2,000", "On Track"),
            ("Florist & Decor", "$2,000", "$1,800", "$500", "$1,300", "Under"),
            ("DJ / Entertainment", "$1,500", "$1,400", "$500", "$900", "Under"),
            ("Wedding Cake", "$800", "$750", "$200", "$550", "Under"),
            ("Invitations & Paper", "$600", "$580", "$580", "$0", "Paid"),
            ("Hair & Makeup", "$1,200", "$1,200", "$0", "$1,200", "On Track"),
            ("Transportation", "$800", "$720", "$300", "$420", "Under"),
            ("Attire & Accessories", "$2,500", "$2,500", "$1,000", "$1,500", "On Track"),
            ("TOTAL", "$30,000", "$27,350", "$9,780", "$17,570", ""),
        ]
        cw = [sw*25//100, sw*15//100, sw*14//100, sw*14//100, sw*14//100, sw*18//100]
        diff = sw - 4 - sum(cw)
        cw[0] += diff

        # Headers
        rh = 20
        cx = sx + 2
        hf2 = font(BOLD, 12)
        for i, h in enumerate(headers):
            d.rectangle([cx, cy, cx + cw[i], cy + rh], fill=DEEP_PLUM)
            d.text((cx + 3, cy + 3), h, font=hf2, fill=WHITE)
            cx += cw[i]
        cy += rh

        rf2 = font(REG, 12)
        bf3 = font(BOLD, 12)
        for ri, row in enumerate(rows_data):
            is_total = ri == len(rows_data) - 1
            bg = CHAMPAGNE if is_total else (WHITE if ri % 2 == 0 else CREAM)
            cx = sx + 2
            for ci, cell in enumerate(row):
                d.rectangle([cx, cy, cx + cw[ci], cy + rh], fill=bg)
                d.line([(cx, cy), (cx + cw[ci], cy)], fill=DUSTY_MAUVE, width=1)
                if ci == 5 and cell:
                    clr = SAGE_GREEN if cell in ("On Track", "Under", "Paid") else GOLD
                    rounded_rect(d, (cx + 2, cy + 2, cx + cw[ci] - 2, cy + rh - 2), 4, fill=clr)
                    d.text((cx + 6, cy + 3), cell, font=rf2, fill=WHITE)
                else:
                    f_use = bf3 if is_total else rf2
                    color = DEEP_PLUM if is_total else DARK_TEXT
                    d.text((cx + 3, cy + 3), str(cell), font=f_use, fill=color)
                cx += cw[ci]
            cy += rh

        # Pie chart
        pie_cy = cy + 50
        if pie_cy + 50 < sy + sh:
            slices = [("Venue", 8000, DEEP_PLUM), ("Catering", 6500, ROSE_GOLD),
                      ("Photo", 3500, SAGE_GREEN), ("Florist", 2000, GOLD),
                      ("DJ", 1500, DUSTY_MAUVE), ("Other", 8500, BLUSH)]
            pie_r = min(45, (sy + sh - pie_cy) // 2 - 5)
            draw_pie_chart(d, sx + sw // 2, pie_cy, pie_r, slices)
            lf = font(BOLD, 10)
            d.text((sx + sw//2 - 30, pie_cy + pie_r + 5), "Budget Breakdown", font=lf, fill=DEEP_PLUM)

    draw_ipad(draw, img, 100, 160, 1400, 1050, budget_full)

    # ── SECOND iPad: Guest List (overlapping, offset right) ──
    def guest_full(d, im, sx, sy, sw, sh):
        tab_off = draw_tab_bar(d, sx, sy, sw, active_idx=2, tab_h=28)
        cy = sy + tab_off + 4

        tf2 = font(BOLD, 18)
        d.text((sx + 8, cy), "Guest List & RSVPs", font=tf2, fill=DEEP_PLUM)
        cy += 24

        # Summary
        sboxes = [("Total Guests", "150", DEEP_PLUM), ("Attending", "98", SAGE_GREEN),
                  ("Pending", "32", GOLD), ("Declined", "20", ROSE_GOLD)]
        bw = (sw - 20) // 4
        for bi, (lbl, val, clr) in enumerate(sboxes):
            bx = sx + 6 + bi * bw
            rounded_rect(d, (bx, cy, bx + bw - 4, cy + 36), 6, fill=clr)
            bf2 = font(BOLD, 11)
            d.text((bx + 4, cy + 2), lbl, font=bf2, fill=WHITE)
            vf = font(BOLD, 14)
            d.text((bx + 4, cy + 17), val, font=vf, fill=WHITE)
        cy += 42

        guests = [
            ("Sarah & Tom Miller", "2", "Attending", "None", "Sent"),
            ("Emily Richardson", "1", "Attending", "Vegan", "Sent"),
            ("James & Kate Kim", "2", "Attending", "Gluten-Free", "Sent"),
            ("Lisa Park", "1", "Pending", "None", "—"),
            ("Mark & Amy Chen", "2", "Attending", "Nut Allergy", "Sent"),
            ("David Lewis", "1", "Declined", "None", "—"),
            ("Rachel Brown +1", "2", "Pending", "Vegetarian", "—"),
            ("Chris & Jen White", "2", "Attending", "None", "Sent"),
            ("Patricia Adams", "1", "Attending", "Dairy-Free", "Sent"),
            ("Michael Torres", "1", "Pending", "None", "—"),
            ("Nicole & Ben Patel", "2", "Attending", "None", "Sent"),
            ("Amanda Reese", "1", "Declined", "Vegan", "—"),
        ]

        headers = ["Guest Name", "#", "RSVP", "Dietary", "TY"]
        cw = [sw * 35//100, sw * 8//100, sw * 22//100, sw * 22//100, sw * 13//100]
        diff2 = sw - 4 - sum(cw)
        cw[0] += diff2

        rh = 19
        hf2 = font(BOLD, 11)
        cx = sx + 2
        for i, h in enumerate(headers):
            d.rectangle([cx, cy, cx + cw[i], cy + rh], fill=DEEP_PLUM)
            d.text((cx + 3, cy + 3), h, font=hf2, fill=WHITE)
            cx += cw[i]
        cy += rh

        rf2 = font(REG, 11)
        for ri, (name, count, rsvp, diet, ty) in enumerate(guests):
            bg = WHITE if ri % 2 == 0 else CREAM
            cx = sx + 2
            cells = [name, count, rsvp, diet, ty]
            for ci, cell in enumerate(cells):
                d.rectangle([cx, cy, cx + cw[ci], cy + rh], fill=bg)
                d.line([(cx, cy), (cx + cw[ci], cy)], fill=DUSTY_MAUVE, width=1)
                if ci == 2:  # RSVP badge
                    badge_clr = SAGE_GREEN if cell == "Attending" else (GOLD if cell == "Pending" else ROSE_GOLD)
                    rounded_rect(d, (cx + 2, cy + 2, cx + cw[ci] - 2, cy + rh - 2), 4, fill=badge_clr)
                    d.text((cx + 5, cy + 3), cell, font=rf2, fill=WHITE)
                elif ci == 4 and cell == "Sent":
                    rounded_rect(d, (cx + 2, cy + 2, cx + cw[ci] - 2, cy + rh - 2), 4, fill=SAGE_GREEN)
                    d.text((cx + 5, cy + 3), cell, font=rf2, fill=WHITE)
                else:
                    d.text((cx + 3, cy + 3), cell, font=rf2, fill=DARK_TEXT)
                cx += cw[ci]
            cy += rh

    draw_ipad(draw, img, 1150, 260, 1400, 1050, guest_full)

    # ── Annotations ──
    draw_annotation(draw, "TRACK EVERY DOLLAR", 50, 1300, 280, 1150, color=DEEP_PLUM, fnt_size=26)
    draw_annotation(draw, "150-GUEST CAPACITY", 1550, 160, 1750, 340, color=SAGE_GREEN, fnt_size=26)
    draw_annotation(draw, "RSVP STATUS AT A GLANCE", 2050, 600, 2400, 750, color=GOLD, fnt_size=24)
    draw_annotation(draw, "DIETARY NEEDS", 2200, 1100, 2450, 950, color=ROSE_GOLD, fnt_size=24)

    # Bottom bar
    rounded_rect(draw, (0, H - 90, W, H), 0, fill=DEEP_PLUM)
    bf = font(BOLD, 30)
    center_text(draw, "AUTO-CALCULATING  •  RSVP TRACKING  •  DIETARY NOTES  •  THANK-YOU STATUS", H - 72, bf, CHAMPAGNE)

    img.save(f"{OUT}/03_budget_guest_preview.png", quality=95)
    print("    -> 03_budget_guest_preview.png saved")


# ══════════════════════════════════════════════════════════════════
# IMAGE 4: Timeline & Seating — Two iPads Side by Side
# ══════════════════════════════════════════════════════════════════
def make_image_4():
    print("  [4/5] Timeline & Seating...")
    img = gradient_bg(CHAMPAGNE, BLUSH)
    draw = ImageDraw.Draw(img)

    # Title
    tf = font(BOLD, 56)
    center_text(draw, 'FROM 12 MONTHS OUT TO "I DO"', 30, tf, DEEP_PLUM)

    sf = font(BOLD, 28)
    center_text(draw, "67 Pre-Loaded Tasks  •  12-Month Timeline  •  Hour-by-Hour Day-Of", 100, sf, ROSE_GOLD)
    draw.line([(W//2 - 400, 145), (W//2 + 400, 145)], fill=GOLD, width=3)

    # ── LEFT iPad: Timeline Checklist ──
    def timeline_screen(d, im, sx, sy, sw, sh):
        tab_off = draw_tab_bar(d, sx, sy, sw, active_idx=4, tab_h=26)
        cy = sy + tab_off + 3

        tf2 = font(BOLD, 16)
        d.text((sx + 8, cy), "Wedding Timeline Checklist", font=tf2, fill=DEEP_PLUM)
        cy += 22

        # Progress bar
        pf = font(REG, 12)
        d.text((sx + 8, cy), "Progress: 42/67 tasks (63%)", font=pf, fill=DARK_TEXT)
        bar_x = sx + 200
        bar_w = sw - 210
        d.rectangle([bar_x, cy + 2, bar_x + bar_w, cy + 12], fill=CHAMPAGNE, outline=DUSTY_MAUVE)
        d.rectangle([bar_x, cy + 2, bar_x + int(bar_w * 0.63), cy + 12], fill=SAGE_GREEN)
        cy += 20

        tasks = [
            ("12 MONTHS BEFORE", None, None),
            ("Book wedding venue", "Done", "Jan 15"),
            ("Set overall budget", "Done", "Jan 20"),
            ("Start guest list draft", "Done", "Feb 1"),
            ("Book photographer", "Done", "Feb 10"),
            ("9 MONTHS BEFORE", None, None),
            ("Book caterer / bar", "Done", "Mar 5"),
            ("Choose wedding party", "Done", "Mar 15"),
            ("Book officiant", "Done", "Mar 20"),
            ("6 MONTHS BEFORE", None, None),
            ("Book florist", "Done", "Jun 1"),
            ("Order invitations", "Done", "Jun 10"),
            ("Book DJ / band", "In Progress", "Jun 15"),
            ("Plan honeymoon", "In Progress", "Jun 20"),
            ("3 MONTHS BEFORE", None, None),
            ("Send invitations", "Done", "Sep 1"),
            ("Book transportation", "In Progress", "Sep 5"),
            ("Order wedding cake", "Not Started", "Sep 10"),
            ("1 MONTH BEFORE", None, None),
            ("Final dress fitting", "Not Started", "Nov 1"),
            ("Finalize seating chart", "Not Started", "Nov 5"),
            ("Confirm all vendors", "Not Started", "Nov 10"),
            ("1 WEEK BEFORE", None, None),
            ("Rehearsal dinner", "Not Started", "Nov 28"),
            ("Pack for honeymoon", "Not Started", "Nov 29"),
        ]

        rh = 18
        rf2 = font(REG, 11)
        bf2 = font(BOLD, 12)
        sf2 = font(BOLD, 10)

        for ti, (task, status, date) in enumerate(tasks):
            if cy + rh > sy + sh - 4:
                break
            if status is None:
                # Section header
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=DEEP_PLUM)
                d.text((sx + 6, cy + 2), task, font=bf2, fill=WHITE)
            else:
                bg = WHITE if ti % 2 == 0 else CREAM
                d.rectangle([sx + 2, cy, sx + sw - 2, cy + rh], fill=bg)
                d.line([(sx + 2, cy), (sx + sw - 2, cy)], fill=DUSTY_MAUVE, width=1)

                # Checkbox
                chk_x = sx + 8
                chk_sz = 10
                if status == "Done":
                    d.rectangle([chk_x, cy + 4, chk_x + chk_sz, cy + 4 + chk_sz], fill=SAGE_GREEN)
                    d.text((chk_x + 1, cy + 2), "\u2713", font=sf2, fill=WHITE)
                else:
                    d.rectangle([chk_x, cy + 4, chk_x + chk_sz, cy + 4 + chk_sz], outline=DUSTY_MAUVE, width=1)

                d.text((sx + 24, cy + 2), task, font=rf2, fill=DARK_TEXT)

                # Status badge
                if status == "Done":
                    clr = SAGE_GREEN
                elif status == "In Progress":
                    clr = GOLD
                else:
                    clr = DUSTY_MAUVE
                badge_x = sx + sw - 90
                rounded_rect(d, (badge_x, cy + 2, badge_x + 55, cy + rh - 2), 4, fill=clr)
                d.text((badge_x + 3, cy + 3), status[:8], font=sf2, fill=WHITE)

                # Date
                if date:
                    d.text((sx + sw - 32, cy + 3), date[-5:], font=sf2, fill=DARK_TEXT)
            cy += rh

    draw_ipad(draw, img, 60, 170, 1260, 1080, timeline_screen)

    # ── RIGHT iPad: Day-Of Timeline ──
    def dayof_screen(d, im, sx, sy, sw, sh):
        tab_off = draw_tab_bar(d, sx, sy, sw, active_idx=6, tab_h=26)
        cy = sy + tab_off + 3

        tf2 = font(BOLD, 16)
        d.text((sx + 8, cy), "Day-Of Timeline — December 6, 2026", font=tf2, fill=DEEP_PLUM)
        cy += 22

        schedule = [
            ("7:00 AM", "Bridal Suite Opens", "Coordinator", CHAMPAGNE),
            ("8:00 AM", "Hair & Makeup — Bride", "Stylist Team", WHITE),
            ("9:00 AM", "Hair & Makeup — Bridesmaids", "Stylist Team", CREAM),
            ("10:00 AM", "First Look Photos", "Photographer", WHITE),
            ("10:30 AM", "Bridal Party Photos", "Photographer", CREAM),
            ("11:00 AM", "Family Formal Photos", "Photographer", WHITE),
            ("11:30 AM", "Break / Light Lunch", "Coordinator", CREAM),
            ("12:30 PM", "Groomsmen Get Ready", "Best Man", WHITE),
            ("1:00 PM", "Vendor Setup Begins", "Coordinator", CREAM),
            ("1:30 PM", "Guests Begin Arriving", "Ushers", WHITE),
            ("2:00 PM", "CEREMONY BEGINS", "Officiant", CHAMPAGNE),
            ("2:30 PM", "Ceremony Ends / Recessional", "DJ", CREAM),
            ("2:45 PM", "Receiving Line", "Bride & Groom", WHITE),
            ("3:00 PM", "Cocktail Hour", "Caterer / DJ", CREAM),
            ("4:00 PM", "Guests Seated for Reception", "Coordinator", WHITE),
            ("4:15 PM", "Grand Entrance & First Dance", "DJ", CHAMPAGNE),
            ("4:30 PM", "Welcome Toast & Blessing", "Best Man", CREAM),
            ("5:00 PM", "Dinner Service Begins", "Caterer", WHITE),
            ("6:00 PM", "Toasts & Speeches", "MOH / Best Man", CREAM),
            ("6:30 PM", "Cake Cutting", "Coordinator", WHITE),
            ("7:00 PM", "Parent Dances", "DJ", CREAM),
            ("7:30 PM", "Open Dancing", "DJ", WHITE),
            ("9:00 PM", "Bouquet & Garter Toss", "DJ", CREAM),
            ("9:30 PM", "Last Dance", "DJ", WHITE),
            ("10:00 PM", "Sparkler Exit / Send Off", "Coordinator", CHAMPAGNE),
        ]

        headers = ["Time", "Event", "Responsible"]
        cw = [sw * 20//100, sw * 48//100, sw * 32//100]
        diff3 = sw - 4 - sum(cw)
        cw[1] += diff3

        rh = 18
        hf2 = font(BOLD, 12)
        cx = sx + 2
        for i, h in enumerate(headers):
            d.rectangle([cx, cy, cx + cw[i], cy + rh], fill=DEEP_PLUM)
            d.text((cx + 3, cy + 2), h, font=hf2, fill=WHITE)
            cx += cw[i]
        cy += rh

        rf2 = font(REG, 11)
        bf2 = font(BOLD, 11)
        for si, (time, event, person, bg) in enumerate(schedule):
            if cy + rh > sy + sh - 4:
                break
            cx = sx + 2
            is_highlight = bg == CHAMPAGNE
            for ci, cell in enumerate([time, event, person]):
                d.rectangle([cx, cy, cx + cw[ci], cy + rh], fill=bg)
                d.line([(cx, cy), (cx + cw[ci], cy)], fill=DUSTY_MAUVE, width=1)
                f_use = bf2 if (is_highlight or ci == 0) else rf2
                clr = DEEP_PLUM if is_highlight else DARK_TEXT
                d.text((cx + 3, cy + 2), cell, font=f_use, fill=clr)
                cx += cw[ci]
            cy += rh

    draw_ipad(draw, img, 1380, 170, 1260, 1080, dayof_screen)

    # ── Annotations ──
    draw_annotation(draw, "67 PRE-LOADED TASKS", 100, 1310, 400, 1220, color=DEEP_PLUM, fnt_size=26)
    draw_annotation(draw, "12-MONTH TIMELINE", 700, 1310, 700, 1220, color=SAGE_GREEN, fnt_size=26)
    draw_annotation(draw, "HOUR-BY-HOUR DAY-OF", 1500, 1310, 1700, 1220, color=GOLD, fnt_size=26)
    draw_annotation(draw, "PERSON RESPONSIBLE", 2150, 1310, 2350, 1220, color=ROSE_GOLD, fnt_size=26)

    # Feature badges
    badge_y = 1400
    feats = [("Status Tracking", DEEP_PLUM), ("Checkbox System", SAGE_GREEN),
             ("25 Day-Of Events", GOLD), ("Vendor Coordination", ROSE_GOLD)]
    spacing = W // (len(feats) + 1)
    for i, (txt, clr) in enumerate(feats):
        draw_pill(draw, txt, spacing * (i + 1), badge_y, bg=clr, fg=WHITE, fnt_size=26)

    # Bottom bar
    rounded_rect(draw, (0, H - 90, W, H), 0, fill=DEEP_PLUM)
    bf = font(BOLD, 30)
    center_text(draw, "NEVER MISS A DETAIL  •  FROM ENGAGEMENT TO HONEYMOON  •  INSTANT DOWNLOAD", H - 72, bf, CHAMPAGNE)

    img.save(f"{OUT}/04_timeline_seating.png", quality=95)
    print("    -> 04_timeline_seating.png saved")


# ══════════════════════════════════════════════════════════════════
# IMAGE 5: Value Proposition
# ══════════════════════════════════════════════════════════════════
def make_image_5():
    print("  [5/5] Value Proposition...")
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Top 60% — Deep plum gradient
    split_y = int(H * 0.60)
    for y in range(split_y):
        t = y / split_y
        r = int(DEEP_PLUM[0] + (LIGHT_PLUM[0] - DEEP_PLUM[0]) * t * 0.5)
        g = int(DEEP_PLUM[1] + (LIGHT_PLUM[1] - DEEP_PLUM[1]) * t * 0.5)
        b = int(DEEP_PLUM[2] + (LIGHT_PLUM[2] - DEEP_PLUM[2]) * t * 0.5)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Bottom 40% — Ivory gradient
    for y in range(split_y, H):
        t = (y - split_y) / (H - split_y)
        r = int(IVORY[0] - 10 * t)
        g = int(IVORY[1] - 10 * t)
        b = int(IVORY[2] - 10 * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Subtle pattern on dark area
    for row in range(0, split_y, 60):
        for col in range(0, W, 60):
            draw.ellipse([col-1, row-1, col+1, row+1], fill=(90, 50, 80))

    # ── Centered iPad with glow ──
    ipad_w, ipad_h = 1200, 860
    ipad_x = (W - ipad_w) // 2
    ipad_y = 140

    # Glow effect
    for g in range(40, 0, -1):
        glow_color = (
            min(255, GOLD[0] + g),
            min(255, GOLD[1] + g),
            min(255, GOLD[2] + g * 2),
        )
        alpha_factor = g * 2
        gc = (
            DEEP_PLUM[0] + (GOLD[0] - DEEP_PLUM[0]) * (40 - g) // 80,
            DEEP_PLUM[1] + (GOLD[1] - DEEP_PLUM[1]) * (40 - g) // 80,
            DEEP_PLUM[2] + (GOLD[2] - DEEP_PLUM[2]) * (40 - g) // 80,
        )
        rounded_rect(draw, (ipad_x - g*2, ipad_y - g*2,
                           ipad_x + ipad_w + g*2, ipad_y + ipad_h + g*2),
                    30 + g, fill=gc)

    def value_screen(d, im, sx, sy, sw, sh):
        tab_off = draw_tab_bar(d, sx, sy, sw, active_idx=1, tab_h=24)
        cy = sy + tab_off + 3

        tf2 = font(BOLD, 16)
        d.text((sx + 8, cy), "Wedding Budget Tracker 2026", font=tf2, fill=DEEP_PLUM)
        cy += 22

        # Summary boxes
        boxes = [("Budget", "$30,000", DEEP_PLUM), ("Spent", "$27,350", ROSE_GOLD),
                 ("Remaining", "$2,650", SAGE_GREEN)]
        bw = (sw - 16) // 3
        for bi, (lbl, val, clr) in enumerate(boxes):
            bx = sx + 6 + bi * bw
            rounded_rect(d, (bx, cy, bx + bw - 4, cy + 32), 6, fill=clr)
            bf2 = font(BOLD, 11)
            d.text((bx + 4, cy + 2), lbl, font=bf2, fill=WHITE)
            vf = font(BOLD, 13)
            d.text((bx + 4, cy + 16), val, font=vf, fill=WHITE)
        cy += 38

        headers = ["Category", "Estimated", "Actual", "Balance"]
        rows_data = [
            ("Venue & Reception", "$8,000", "$7,800", "$4,800"),
            ("Catering & Bar", "$6,500", "$6,200", "$4,200"),
            ("Photography", "$3,500", "$3,500", "$2,000"),
            ("Florist & Decor", "$2,000", "$1,800", "$1,300"),
            ("DJ / Band", "$1,500", "$1,400", "$900"),
            ("Wedding Cake", "$800", "$750", "$550"),
            ("Invitations", "$600", "$580", "$0"),
            ("Hair & Makeup", "$1,200", "$1,200", "$1,200"),
            ("Attire", "$2,500", "$2,500", "$1,500"),
            ("TOTAL", "$30,000", "$27,350", "$17,570"),
        ]
        cw = [sw * 35//100, sw * 22//100, sw * 22//100, sw * 21//100]
        diff = sw - 4 - sum(cw)
        cw[0] += diff

        rh = 17
        hf2 = font(BOLD, 11)
        cx = sx + 2
        for i, h in enumerate(headers):
            d.rectangle([cx, cy, cx + cw[i], cy + rh], fill=DEEP_PLUM)
            d.text((cx + 3, cy + 2), h, font=hf2, fill=WHITE)
            cx += cw[i]
        cy += rh

        rf2 = font(REG, 11)
        bf3 = font(BOLD, 11)
        for ri, row in enumerate(rows_data):
            is_total = ri == len(rows_data) - 1
            bg = CHAMPAGNE if is_total else (WHITE if ri % 2 == 0 else CREAM)
            cx = sx + 2
            for ci, cell in enumerate(row):
                d.rectangle([cx, cy, cx + cw[ci], cy + rh], fill=bg)
                d.line([(cx, cy), (cx + cw[ci], cy)], fill=DUSTY_MAUVE, width=1)
                f_use = bf3 if is_total else rf2
                color = DEEP_PLUM if is_total else DARK_TEXT
                d.text((cx + 3, cy + 2), str(cell), font=f_use, fill=color)
                cx += cw[ci]
            cy += rh

        # Mini pie
        pie_cy = cy + 38
        if pie_cy + 30 < sy + sh:
            slices = [("Venue", 8000, DEEP_PLUM), ("Catering", 6500, ROSE_GOLD),
                      ("Photo", 3500, SAGE_GREEN), ("Other", 12000, BLUSH)]
            draw_pie_chart(d, sx + sw // 2, pie_cy, min(30, (sy + sh - pie_cy) // 2 - 2), slices)

    draw_ipad(draw, img, ipad_x, ipad_y, ipad_w, ipad_h, value_screen, bezel_color=(20, 20, 20))

    # ── Floating badges around iPad ──
    badges_info = [
        ("9 Wedding Tabs", 200, 250, DEEP_PLUM),
        ("150-Guest List", 200, 420, SAGE_GREEN),
        ("67 Task Checklist", 200, 590, GOLD),
        ("23 Budget Categories", 2100, 250, ROSE_GOLD),
        ("Day-Of Timeline", 2100, 420, DUSTY_MAUVE),
        ("Gift Tracker", 2100, 590, LIGHT_PLUM),
    ]
    for txt, bx, by, clr in badges_info:
        f_badge = font(BOLD, 26)
        bb = draw.textbbox((0, 0), txt, font=f_badge)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        px, py = bx - tw//2, by - th//2
        # Glow
        for g2 in range(6, 0, -1):
            gc2 = tuple(min(255, c + g2 * 15) for c in clr)
            rounded_rect(draw, (px - 16 - g2, py - 10 - g2, px + tw + 16 + g2, py + th + 10 + g2),
                        (th + 20)//2 + g2, fill=gc2)
        rounded_rect(draw, (px - 16, py - 10, px + tw + 16, py + th + 10),
                    (th + 20)//2, fill=clr)
        draw.text((px, py), txt, font=f_badge, fill=WHITE)

        # Connector line to iPad
        line_to_x = ipad_x if bx < W // 2 else ipad_x + ipad_w
        draw.line([(px + tw + 20 if bx < W//2 else px - 4, by),
                   (line_to_x, by)], fill=(*clr[:3],), width=2)

    # ── Bottom section (ivory area) ──
    cy_bottom = split_y + 30

    # Main tagline
    tag_f = font(BOLD, 56)
    center_text(draw, 'PLAN YOUR DREAM WEDDING \u2014 STRESS FREE', cy_bottom, tag_f, DEEP_PLUM)
    cy_bottom += 75

    # Price
    price_f = font(BOLD, 52)
    center_text(draw, "$12.99 \u2014 INSTANT DOWNLOAD", cy_bottom, price_f, ROSE_GOLD)
    cy_bottom += 70

    # Stars
    draw_stars(draw, W // 2, cy_bottom, n=5, size=24, color=GOLD)
    cy_bottom += 60

    # Testimonial
    quote_f = font(REG, 28)
    center_text(draw, '"Your dream wedding deserves an organized plan."', cy_bottom, quote_f, DARK_TEXT)
    cy_bottom += 50

    # Compatibility
    compat_f = font(BOLD, 30)
    center_text(draw, "WORKS WITH:  Google Sheets  |  Excel  |  LibreOffice", cy_bottom, compat_f, DEEP_PLUM)
    cy_bottom += 55

    # Feature strip
    feats = ["Instant Download", "Print Ready", "Lifetime Access", "Free Updates"]
    spacing = W // (len(feats) + 1)
    for i, feat in enumerate(feats):
        draw_pill(draw, feat, spacing * (i + 1), cy_bottom, bg=DEEP_PLUM, fg=CHAMPAGNE, fnt_size=24)

    # Decorative gold border
    draw.rectangle([0, 0, W - 1, 3], fill=GOLD)
    draw.rectangle([0, H - 4, W - 1, H - 1], fill=GOLD)
    draw.rectangle([0, 0, 3, H - 1], fill=GOLD)
    draw.rectangle([W - 4, 0, W - 1, H - 1], fill=GOLD)

    img.save(f"{OUT}/05_value_proposition.png", quality=95)
    print("    -> 05_value_proposition.png saved")


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  Wedding Planner & Budget Bundle 2026")
    print("  Generating 5 Etsy listing images...")
    print("=" * 60)

    make_image_1()
    make_image_2()
    make_image_3()
    make_image_4()
    make_image_5()

    print("=" * 60)
    print(f"  All 5 images saved to: {OUT}/")
    print("=" * 60)
