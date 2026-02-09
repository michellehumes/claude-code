#!/usr/bin/env python3
"""
Generate 5 professional Etsy listing images for:
Product 2: Small Business Planner & Starter Kit 2026
Navy/Coral professional palette, iPad mockups, annotation labels, real data.
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

# ── Output ──────────────────────────────────────────────────────────────
OUT = "/home/user/claude-code/etsy-digital-download-2/images"
os.makedirs(OUT, exist_ok=True)
W, H = 2700, 2025

# ── Palette ─────────────────────────────────────────────────────────────
NAVY        = (27, 42, 74)
STEEL_BLUE  = (46, 64, 87)
DUSTY_BLUE  = (107, 140, 174)
PALE_BLUE   = (214, 228, 240)
ICE_BLUE    = (235, 242, 250)
CORAL       = (232, 128, 106)
WARM_GOLD   = (212, 168, 83)
MINT        = (123, 200, 164)
WHITE       = (255, 255, 255)
DARK_TEXT   = (33, 33, 33)
LIGHT_GRAY  = (220, 225, 232)
MID_GRAY    = (180, 190, 200)
SHADOW      = (20, 30, 50, 60)

# ── Fonts ───────────────────────────────────────────────────────────────
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

# ── Helpers ─────────────────────────────────────────────────────────────
def gradient_bg(w, h, top_color, bot_color, mid_color=None):
    """Vertical gradient, optionally through a mid-color."""
    img = Image.new("RGBA", (w, h))
    for y in range(h):
        t = y / (h - 1)
        if mid_color and t < 0.5:
            s = t * 2
            r = int(top_color[0] + (mid_color[0] - top_color[0]) * s)
            g = int(top_color[1] + (mid_color[1] - top_color[1]) * s)
            b = int(top_color[2] + (mid_color[2] - top_color[2]) * s)
        elif mid_color:
            s = (t - 0.5) * 2
            r = int(mid_color[0] + (bot_color[0] - mid_color[0]) * s)
            g = int(mid_color[1] + (bot_color[1] - mid_color[1]) * s)
            b = int(mid_color[2] + (bot_color[2] - mid_color[2]) * s)
        else:
            r = int(top_color[0] + (bot_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bot_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bot_color[2] - top_color[2]) * t)
        for x in range(w):
            img.putpixel((x, y), (r, g, b, 255))
    return img

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = bbox
    r = min(radius, (x1-x0)//2, (y1-y0)//2)
    draw.rounded_rectangle(bbox, radius=r, fill=fill, outline=outline, width=width)

def draw_shadow(img, bbox, radius=30, blur_layers=8, color=SHADOW):
    """Draw a soft shadow behind a rectangle."""
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = bbox
    for i in range(blur_layers, 0, -1):
        alpha = color[3] // blur_layers
        off = i * 4
        c = (color[0], color[1], color[2], alpha)
        d.rounded_rectangle((x0-off+6, y0-off+10, x1+off+6, y1+off+10),
                             radius=radius+off, fill=c)
    return Image.alpha_composite(img, overlay)


def draw_ipad(img, draw, x, y, iw, ih, screen_content_func, shadow=True):
    """
    Draw an iPad mockup at (x, y) with inner-screen size (iw, ih).
    screen_content_func(draw, sx, sy, sw, sh) draws content inside the screen.
    """
    bezel_t, bezel_b, bezel_lr = 30, 30, 22
    ow = iw + bezel_lr * 2
    oh = ih + bezel_t + bezel_b
    bx0, by0, bx1, by1 = x, y, x + ow, y + oh
    corner = 28

    # Shadow
    if shadow:
        img_out = draw_shadow(img, (bx0, by0, bx1, by1), radius=corner, blur_layers=10,
                              color=(15, 25, 45, 50))
        draw2 = ImageDraw.Draw(img_out)
    else:
        img_out = img
        draw2 = draw

    # Bezel
    draw2.rounded_rectangle((bx0, by0, bx1, by1), radius=corner, fill=(30, 30, 32))
    # Camera dot
    cam_r = max(4, bezel_t // 6)
    draw2.ellipse((bx0 + ow // 2 - cam_r, by0 + bezel_t // 2 - cam_r,
                   bx0 + ow // 2 + cam_r, by0 + bezel_t // 2 + cam_r),
                  fill=(50, 50, 55))
    # Screen area (white)
    sx, sy = bx0 + bezel_lr, by0 + bezel_t
    draw2.rectangle((sx, sy, sx + iw, sy + ih), fill=WHITE)

    # Draw screen content
    screen_content_func(draw2, sx, sy, iw, ih)
    return img_out, draw2, ow, oh


def text_centered(draw, cx, y, text, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, y), text, font=fnt, fill=fill)

def text_width(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0]

def text_height(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[3] - bbox[1]


def draw_pill(draw, cx, cy, text, fnt, bg, fg, px=24, py=10):
    tw = text_width(draw, text, fnt)
    th = text_height(draw, text, fnt)
    x0 = cx - tw // 2 - px
    y0 = cy - th // 2 - py
    x1 = cx + tw // 2 + px
    y1 = cy + th // 2 + py
    r = (y1 - y0) // 2
    draw.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=bg)
    text_centered(draw, cx, y0 + py, text, fnt, fg)
    return x1 - x0


def draw_annotation(draw, x, y, label, fnt, direction="right", length=70, dot_r=6):
    """Draw annotation label with a line + dot."""
    # dot
    draw.ellipse((x - dot_r, y - dot_r, x + dot_r, y + dot_r), fill=CORAL)
    tw = text_width(draw, label, fnt)
    th = text_height(draw, label, fnt)
    if direction == "right":
        lx = x + dot_r + 4
        ex = lx + length
        draw.line((lx, y, ex, y), fill=CORAL, width=3)
        # label bg
        pad = 10
        draw.rounded_rectangle((ex + 4, y - th // 2 - pad, ex + 4 + tw + pad * 2, y + th // 2 + pad),
                                radius=8, fill=CORAL)
        draw.text((ex + 4 + pad, y - th // 2), label, font=fnt, fill=WHITE)
    elif direction == "left":
        lx = x - dot_r - 4
        ex = lx - length
        draw.line((ex, y, lx, y), fill=CORAL, width=3)
        pad = 10
        draw.rounded_rectangle((ex - tw - pad * 2 - 4, y - th // 2 - pad, ex - 4, y + th // 2 + pad),
                                radius=8, fill=CORAL)
        draw.text((ex - tw - pad - 4, y - th // 2), label, font=fnt, fill=WHITE)
    elif direction == "up":
        draw.line((x, y - dot_r - 4, x, y - dot_r - 4 - length), fill=CORAL, width=3)
        ey = y - dot_r - 4 - length
        pad = 10
        draw.rounded_rectangle((x - tw // 2 - pad, ey - th - pad, x + tw // 2 + pad, ey + pad),
                                radius=8, fill=CORAL)
        draw.text((x - tw // 2, ey - th), label, font=fnt, fill=WHITE)
    elif direction == "down":
        draw.line((x, y + dot_r + 4, x, y + dot_r + 4 + length), fill=CORAL, width=3)
        ey = y + dot_r + 4 + length
        pad = 10
        draw.rounded_rectangle((x - tw // 2 - pad, ey - pad, x + tw // 2 + pad, ey + th + pad),
                                radius=8, fill=CORAL)
        draw.text((x - tw // 2, ey - pad + pad), label, font=fnt, fill=WHITE)


# ──────────────────────────────── KPI CARD HELPER ─────────────────────
def draw_kpi_card(draw, x, y, w, h, title, value, color):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=WHITE, outline=LIGHT_GRAY, width=2)
    # Accent top bar
    draw.rounded_rectangle((x, y, x + w, y + 8), radius=10, fill=color)
    draw.rectangle((x, y + 5, x + w, y + 8), fill=color)
    fnt_title = font(max(14, h // 6), bold=False)
    fnt_val = font(max(18, h // 3), bold=True)
    text_centered(draw, x + w // 2, y + 14, title, fnt_title, DUSTY_BLUE)
    text_centered(draw, x + w // 2, y + h // 2 - 4, value, fnt_val, DARK_TEXT)


# ──────────────────────────────── TAB BAR ─────────────────────────────
TABS = ["Dashboard", "Client Tracker", "Invoice Tracker", "Project Tracker",
        "Content Calendar", "Income & Exp.", "Inventory", "Goals & Planning", "How to Use"]

def draw_tab_bar(draw, sx, sy, sw, sh, active_idx=0):
    """Draw a tab bar at the bottom of the screen area."""
    bar_h = max(28, sh // 14)
    by = sy + sh - bar_h
    draw.rectangle((sx, by, sx + sw, sy + sh), fill=NAVY)
    tab_w = sw // len(TABS)
    fnt_tab = font(max(11, bar_h // 3), bold=False)
    for i, t in enumerate(TABS):
        tx = sx + i * tab_w
        if i == active_idx:
            draw.rectangle((tx, by, tx + tab_w, sy + sh), fill=CORAL)
        short = t if len(t) < 10 else t[:8] + ".."
        text_centered(draw, tx + tab_w // 2, by + bar_h // 4, short, fnt_tab, WHITE)
    return bar_h


# ──────────────────────────────── TABLE HELPER ────────────────────────
def draw_table(draw, x, y, col_widths, rows, header=True, fnt_size=16,
               header_bg=NAVY, header_fg=WHITE, alt_bg=ICE_BLUE, row_h=None):
    fnt_h = font(fnt_size, bold=True)
    fnt_r = font(fnt_size, bold=False)
    rh = row_h or (fnt_size + 14)
    cx = x
    # header
    total_w = sum(col_widths)
    if header:
        draw.rectangle((x, y, x + total_w, y + rh), fill=header_bg)
        for ci, (cw, cell) in enumerate(zip(col_widths, rows[0])):
            draw.text((cx + 6, y + 4), cell, font=fnt_h, fill=header_fg)
            cx += cw
        y += rh
        data_rows = rows[1:]
    else:
        data_rows = rows
    for ri, row in enumerate(data_rows):
        bg = alt_bg if ri % 2 == 0 else WHITE
        draw.rectangle((x, y, x + total_w, y + rh), fill=bg)
        cx = x
        for ci, (cw, cell) in enumerate(zip(col_widths, row)):
            if isinstance(cell, tuple):
                text, color = cell
                # badge
                tw2 = text_width(draw, text, fnt_r)
                bx = cx + 6
                draw.rounded_rectangle((bx, y + 2, bx + tw2 + 14, y + rh - 2),
                                        radius=6, fill=color)
                draw.text((bx + 7, y + 4), text, font=fnt_r, fill=WHITE)
            else:
                draw.text((cx + 6, y + 4), str(cell), font=fnt_r, fill=DARK_TEXT)
            cx += cw
        y += rh
    # outer border
    draw.rectangle((x, y - rh * len(data_rows) - (rh if header else 0),
                     x + total_w, y), outline=LIGHT_GRAY, width=2)
    return y

def draw_bar_chart_mini(draw, x, y, w, h, values, colors, labels=None):
    """Simple bar chart."""
    draw.rectangle((x, y, x + w, y + h), fill=ICE_BLUE, outline=LIGHT_GRAY, width=1)
    n = len(values)
    max_v = max(values) if values else 1
    bar_w = max(8, (w - 20) // (n * 2))
    gap = (w - n * bar_w) // (n + 1)
    fnt_l = font(max(10, bar_w // 2), bold=False)
    for i, v in enumerate(values):
        bh = int((v / max_v) * (h - 30))
        bx = x + gap + i * (bar_w + gap)
        by = y + h - 10 - bh
        c = colors[i % len(colors)]
        draw.rectangle((bx, by, bx + bar_w, y + h - 10), fill=c)
        if labels and i < len(labels):
            text_centered(draw, bx + bar_w // 2, y + h - 10, labels[i][:3],
                          font(max(8, bar_w // 3), bold=False), DUSTY_BLUE)


def draw_status_badge(draw, x, y, text, color, fnt):
    tw = text_width(draw, text, fnt)
    th = text_height(draw, text, fnt)
    pad_x, pad_y = 8, 3
    draw.rounded_rectangle((x, y, x + tw + pad_x * 2, y + th + pad_y * 2),
                            radius=6, fill=color)
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=WHITE)
    return tw + pad_x * 2


# ══════════════════════════════════════════════════════════════════════
# IMAGE 1: HERO MAIN LISTING
# ══════════════════════════════════════════════════════════════════════
def make_image1():
    img = gradient_bg(W, H, PALE_BLUE, WHITE, ICE_BLUE)
    draw = ImageDraw.Draw(img)

    # Decorative circles
    for cx, cy, r, c in [(120, 180, 160, (*DUSTY_BLUE, 25)),
                          (2580, 350, 200, (*PALE_BLUE, 40)),
                          (350, 1800, 120, (*CORAL, 18)),
                          (2400, 1700, 140, (*WARM_GOLD, 20))]:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
        img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # ── Title area ───
    fnt_title = font(72, bold=True)
    fnt_sub = font(38, bold=False)
    text_centered(draw, W // 2, 55, "SMALL BUSINESS PLANNER & STARTER KIT", fnt_title, NAVY)

    # 2026 badge
    badge_fnt = font(52, bold=True)
    bw = text_width(draw, "2026", badge_fnt) + 50
    bx = W // 2 - bw // 2
    draw.rounded_rectangle((bx, 140, bx + bw, 205), radius=14, fill=CORAL)
    text_centered(draw, W // 2, 148, "2026", badge_fnt, WHITE)

    # ── iPad mockup (centered, large) ───
    ipad_w, ipad_h = 1340, 900
    ipad_x = W // 2 - (ipad_w + 44) // 2
    ipad_y = 240

    def dashboard_screen(d, sx, sy, sw, sh):
        d.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
        # Header bar
        d.rectangle((sx, sy, sx + sw, sy + 36), fill=NAVY)
        d.text((sx + 14, sy + 6), "Small Business Planner 2026 — Dashboard", font=font(20, True), fill=WHITE)

        # KPI cards row
        kpi_data = [("REVENUE", "$8,450", CORAL), ("EXPENSES", "$3,120", DUSTY_BLUE),
                    ("NET PROFIT", "$5,330", MINT), ("MARGIN", "63.1%", WARM_GOLD),
                    ("CLIENTS", "12", STEEL_BLUE)]
        card_w = (sw - 80) // 5
        card_h = 82
        ky = sy + 50
        for i, (title, val, col) in enumerate(kpi_data):
            cx = sx + 14 + i * (card_w + 12)
            draw_kpi_card(d, cx, ky, card_w, card_h, title, val, col)

        # Monthly revenue table
        ty = ky + card_h + 18
        fnt_sec = font(18, True)
        d.text((sx + 14, ty), "MONTHLY REVENUE & EXPENSES", font=fnt_sec, fill=NAVY)
        ty += 28
        cols = [160, 130, 130, 130, 140]
        rows_data = [
            ["Month", "Revenue", "Expenses", "Profit", "Margin"],
            ["Jan 2026", "$7,200", "$2,850", "$4,350", "60.4%"],
            ["Feb 2026", "$6,980", "$2,700", "$4,280", "61.3%"],
            ["Mar 2026", "$8,450", "$3,120", "$5,330", "63.1%"],
            ["Apr 2026", "$9,100", "$3,400", "$5,700", "62.6%"],
            ["May 2026", "$8,800", "$3,050", "$5,750", "65.3%"],
            ["Jun 2026", "$10,200", "$3,600", "$6,600", "64.7%"],
        ]
        draw_table(d, sx + 14, ty, cols, rows_data, fnt_size=16, row_h=28)

        # Mini bar chart
        chart_x = sx + 14 + sum(cols) + 30
        chart_w = sw - (chart_x - sx) - 20
        if chart_w > 80:
            d.text((chart_x, ty - 28), "REVENUE TREND", font=fnt_sec, fill=NAVY)
            vals = [7200, 6980, 8450, 9100, 8800, 10200]
            lbls = ["J", "F", "M", "A", "M", "J"]
            draw_bar_chart_mini(d, chart_x, ty, chart_w, 200, vals,
                                [CORAL, DUSTY_BLUE, MINT, WARM_GOLD, CORAL, DUSTY_BLUE], lbls)

        # Tab bar
        draw_tab_bar(d, sx, sy, sw, sh, active_idx=0)

    img, draw, ow, oh = draw_ipad(img, draw, ipad_x, ipad_y, ipad_w, ipad_h, dashboard_screen)

    # ── Annotation labels ───
    ann_fnt = font(22, True)
    draw_annotation(draw, ipad_x + 100, ipad_y + 120, "KPI DASHBOARD", ann_fnt, "left", 90)
    draw_annotation(draw, ipad_x + ow - 40, ipad_y + 400, "REVENUE vs EXPENSES", ann_fnt, "right", 80)
    draw_annotation(draw, ipad_x + ow - 200, ipad_y + 200, "AUTO BAR CHART", ann_fnt, "right", 60)

    # ── Feature pills row ───
    pill_y = ipad_y + oh + 40
    pills = ["9 Tabs", "Auto Formulas", "Drop-Down Menus", "Google Sheets + Excel"]
    pill_fnt = font(28, True)
    total_pill_w = sum(text_width(draw, p, pill_fnt) + 64 for p in pills) + 30 * (len(pills) - 1)
    px = W // 2 - total_pill_w // 2
    for p in pills:
        pw = text_width(draw, p, pill_fnt) + 64
        draw.rounded_rectangle((px, pill_y, px + pw, pill_y + 56), radius=28, fill=NAVY)
        draw.text((px + 32, pill_y + 10), p, font=pill_fnt, fill=WHITE)
        px += pw + 30

    # ── PERFECT FOR line ───
    perf_y = pill_y + 80
    perf_fnt = font(30, False)
    text_centered(draw, W // 2, perf_y,
                  "PERFECT FOR: Etsy Sellers  |  Freelancers  |  Coaches  |  Small Shops",
                  perf_fnt, STEEL_BLUE)

    # ── Bottom bar ───
    bar_h2 = 80
    draw.rectangle((0, H - bar_h2, W, H), fill=NAVY)
    bf = font(36, True)
    text_centered(draw, W // 2, H - bar_h2 + 18, "INSTANT DIGITAL DOWNLOAD — $12.99", bf, WHITE)

    # ── Stats badge top-right ───
    draw.rounded_rectangle((W - 260, 60, W - 40, 130), radius=18, fill=WARM_GOLD)
    text_centered(draw, W - 150, 72, "9 TABS", font(32, True), WHITE)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "01_hero_main_listing.png"), quality=95)
    print("  [OK] 01_hero_main_listing.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 2: WHAT'S INCLUDED — 8 MINI IPADS
# ══════════════════════════════════════════════════════════════════════
def make_image2():
    img = gradient_bg(W, H, ICE_BLUE, PALE_BLUE, WHITE)
    draw = ImageDraw.Draw(img)

    # Subtle pattern dots
    for dx in range(0, W, 60):
        for dy in range(0, H, 60):
            draw.ellipse((dx, dy, dx + 3, dy + 3), fill=(*DUSTY_BLUE, 30))

    # Title
    fnt_title = font(62, True)
    text_centered(draw, W // 2, 45, "EVERYTHING INCLUDED IN YOUR BUSINESS KIT", fnt_title, NAVY)

    # Badge
    badge_fnt = font(28, True)
    badge_txt = "9 PROFESSIONAL TABS  +  HOW TO USE GUIDE"
    bw2 = text_width(draw, badge_txt, badge_fnt) + 60
    draw.rounded_rectangle((W // 2 - bw2 // 2, 125, W // 2 + bw2 // 2, 175), radius=22, fill=CORAL)
    text_centered(draw, W // 2, 133, badge_txt, badge_fnt, WHITE)

    # 4x2 grid of mini iPads
    cols_n, rows_n = 4, 2
    pad_x, pad_y = 50, 50
    grid_w = (W - pad_x * 2)
    grid_h = (H - 260 - pad_y)
    cell_w = grid_w // cols_n
    cell_h = grid_h // rows_n
    miw = cell_w - 80
    mih = cell_h - 90

    tab_data = [
        ("Dashboard", 0),
        ("Client Tracker", 1),
        ("Invoice Tracker", 2),
        ("Project Tracker", 3),
        ("Content Calendar", 4),
        ("Income & Expenses", 5),
        ("Inventory", 6),
        ("Goals & Planning", 7),
    ]

    def make_screen_func(idx):
        def screen_func(d, sx, sy, sw, sh):
            d.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
            # Mini header
            d.rectangle((sx, sy, sx + sw, sy + 22), fill=NAVY)
            d.text((sx + 4, sy + 2), TABS[idx], font=font(12, True), fill=WHITE)

            fnt_s = font(11, False)
            fnt_sb = font(11, True)
            cy = sy + 28

            if idx == 0:  # Dashboard
                kpis = [("Revenue", "$8,450", CORAL), ("Expenses", "$3,120", DUSTY_BLUE),
                        ("Profit", "$5,330", MINT)]
                cw = (sw - 16) // 3
                for i, (t, v, c) in enumerate(kpis):
                    kx = sx + 4 + i * (cw + 4)
                    d.rounded_rectangle((kx, cy, kx + cw, cy + 44), radius=5, fill=WHITE, outline=LIGHT_GRAY)
                    d.rectangle((kx, cy, kx + cw, cy + 5), fill=c)
                    d.text((kx + 4, cy + 8), t, font=font(9, False), fill=DUSTY_BLUE)
                    d.text((kx + 4, cy + 22), v, font=font(14, True), fill=DARK_TEXT)
                cy += 52
                vals = [72, 69, 84, 91, 88, 102]
                bw3 = (sw - 20) // 6
                for i, v in enumerate(vals):
                    bh2 = int(v / 110 * (sh - (cy - sy) - 20))
                    bx2 = sx + 6 + i * (bw3 + 2)
                    d.rectangle((bx2, cy + (sh - (cy - sy) - 20) - bh2, bx2 + bw3, cy + (sh - (cy - sy) - 20)),
                                fill=[CORAL, DUSTY_BLUE, MINT][i % 3])

            elif idx == 1:  # Client Tracker
                clients = [("Sarah Chen", "sarah@email.com", "Active", MINT),
                           ("Mike Torres", "mike@biz.com", "VIP", WARM_GOLD),
                           ("Ava Johnson", "ava@shop.co", "Lead", DUSTY_BLUE),
                           ("Liam Park", "liam@co.io", "Active", MINT),
                           ("Emma Davis", "emma@free.net", "VIP", WARM_GOLD)]
                for cl in clients:
                    d.text((sx + 4, cy), cl[0], font=fnt_sb, fill=DARK_TEXT)
                    d.text((sx + sw // 3, cy), cl[1], font=fnt_s, fill=DUSTY_BLUE)
                    draw_status_badge(d, sx + sw - 65, cy, cl[2], cl[3], font(9, True))
                    cy += 22

            elif idx == 2:  # Invoice Tracker
                invs = [("INV-001", "$1,200", "Paid", MINT),
                        ("INV-002", "$850", "Pending", WARM_GOLD),
                        ("INV-003", "$2,400", "Paid", MINT),
                        ("INV-004", "$675", "Overdue", CORAL),
                        ("INV-005", "$1,100", "Paid", MINT)]
                for inv in invs:
                    d.text((sx + 4, cy), inv[0], font=fnt_sb, fill=DARK_TEXT)
                    d.text((sx + sw // 3, cy), inv[1], font=fnt_sb, fill=STEEL_BLUE)
                    draw_status_badge(d, sx + sw - 65, cy, inv[2], inv[3], font(9, True))
                    cy += 22

            elif idx == 3:  # Project Tracker
                projs = [("Website Redesign", "Mar 15", "High", CORAL),
                         ("Email Campaign", "Mar 22", "Medium", WARM_GOLD),
                         ("Product Photos", "Apr 1", "High", CORAL),
                         ("SEO Audit", "Apr 10", "Low", MINT),
                         ("Social Media Kit", "Apr 15", "Medium", WARM_GOLD)]
                for p in projs:
                    d.text((sx + 4, cy), p[0], font=fnt_sb, fill=DARK_TEXT)
                    d.text((sx + sw * 2 // 4, cy), p[1], font=fnt_s, fill=DUSTY_BLUE)
                    draw_status_badge(d, sx + sw - 65, cy, p[2], p[3], font(9, True))
                    cy += 22

            elif idx == 4:  # Content Calendar
                posts = [("Mar 3", "Instagram", "Product Launch", (200, 100, 150)),
                         ("Mar 5", "TikTok", "Behind Scenes", (40, 40, 40)),
                         ("Mar 8", "Pinterest", "Mood Board", (200, 50, 50)),
                         ("Mar 10", "Instagram", "Tutorial", (200, 100, 150)),
                         ("Mar 12", "Blog", "How-To Guide", STEEL_BLUE)]
                for p in posts:
                    d.text((sx + 4, cy), p[0], font=fnt_s, fill=DUSTY_BLUE)
                    draw_status_badge(d, sx + 55, cy, p[1], p[3], font(9, True))
                    d.text((sx + sw // 2 + 20, cy), p[2], font=fnt_s, fill=DARK_TEXT)
                    cy += 22

            elif idx == 5:  # Income & Expenses
                txns = [("Mar 1", "Etsy Sale", "+$145", MINT),
                        ("Mar 2", "Supplies", "-$67", CORAL),
                        ("Mar 3", "Custom Order", "+$320", MINT),
                        ("Mar 4", "Shipping", "-$28", CORAL),
                        ("Mar 5", "Wholesale", "+$890", MINT)]
                for t in txns:
                    d.text((sx + 4, cy), t[0], font=fnt_s, fill=DUSTY_BLUE)
                    d.text((sx + 55, cy), t[1], font=fnt_s, fill=DARK_TEXT)
                    d.text((sx + sw - 55, cy), t[2], font=fnt_sb, fill=t[3])
                    cy += 22

            elif idx == 6:  # Inventory
                items = [("Candle - Vanilla", "45", "In Stock", MINT),
                         ("Candle - Rose", "8", "Low Stock", WARM_GOLD),
                         ("Gift Box Set", "0", "Reorder", CORAL),
                         ("Wax Melts 6pk", "32", "In Stock", MINT),
                         ("Matches Tin", "5", "Low Stock", WARM_GOLD)]
                for it in items:
                    d.text((sx + 4, cy), it[0], font=fnt_s, fill=DARK_TEXT)
                    d.text((sx + sw // 2, cy), "Qty: " + it[1], font=fnt_s, fill=STEEL_BLUE)
                    draw_status_badge(d, sx + sw - 72, cy, it[2], it[3], font(9, True))
                    cy += 22

            elif idx == 7:  # Goals & Planning
                goals = [("Q1: Launch online store", True),
                         ("Q1: 50 email subscribers", True),
                         ("Q2: $10K monthly revenue", False),
                         ("Q2: Hire VA", False),
                         ("Q3: Wholesale partnerships", False)]
                for g in goals:
                    check = "✓" if g[1] else "○"
                    col = MINT if g[1] else DUSTY_BLUE
                    d.text((sx + 4, cy), check, font=fnt_sb, fill=col)
                    d.text((sx + 22, cy), g[0], font=fnt_s, fill=DARK_TEXT)
                    cy += 22

        return screen_func

    label_fnt = font(22, True)
    for gi, (tab_name, tab_idx) in enumerate(tab_data):
        col_i = gi % cols_n
        row_i = gi // cols_n
        cx = pad_x + col_i * cell_w + cell_w // 2
        cy_top = 210 + row_i * cell_h
        ix = cx - (miw + 44) // 2
        iy = cy_top

        img, draw, ow2, oh2 = draw_ipad(img, draw, ix, iy, miw, mih,
                                          make_screen_func(tab_idx), shadow=True)
        # Label
        text_centered(draw, cx, iy + oh2 + 8, tab_name, label_fnt, NAVY)

    # Bottom bar
    draw.rectangle((0, H - 60, W, H), fill=NAVY)
    text_centered(draw, W // 2, H - 52, "GOOGLE SHEETS  +  EXCEL  +  LIBRE OFFICE  —  INSTANT DOWNLOAD",
                  font(26, True), WHITE)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "02_whats_included.png"), quality=95)
    print("  [OK] 02_whats_included.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 3: DASHBOARD DEEP DIVE — TWO OVERLAPPING IPADS
# ══════════════════════════════════════════════════════════════════════
def make_image3():
    img = gradient_bg(W, H, PALE_BLUE, ICE_BLUE, WHITE)
    draw = ImageDraw.Draw(img)

    # Decorative shapes
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((2300, -80, 2700, 320), fill=(*DUSTY_BLUE, 20))
    od.ellipse((-100, 1500, 300, 1900), fill=(*CORAL, 15))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Title
    fnt_title = font(68, True)
    text_centered(draw, W // 2, 40, "YOUR BUSINESS COMMAND CENTER", fnt_title, NAVY)

    # Stats line
    stats_fnt = font(28, False)
    text_centered(draw, W // 2, 120,
                  "12-Month Tracking   |   50-Row CRM   |   Auto Profit Margin   |   Revenue Charts",
                  stats_fnt, DUSTY_BLUE)

    # ── SECOND iPad (behind, right-shifted) — Client Tracker ───
    ipad2_w, ipad2_h = 1000, 780
    ipad2_x = W // 2 + 100
    ipad2_y = 300

    def client_screen(d, sx, sy, sw, sh):
        d.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
        d.rectangle((sx, sy, sx + sw, sy + 32), fill=STEEL_BLUE)
        d.text((sx + 10, sy + 5), "Client Tracker", font=font(18, True), fill=WHITE)
        cols2 = [sw * 3 // 10, sw * 3 // 10, sw * 2 // 10, sw * 2 // 10]
        clients_data = [
            ["Client Name", "Email", "Status", "Revenue"],
            ["Sarah Chen", "sarah@email.com", ("Active", MINT), "$4,200"],
            ["Mike Torres", "mike@biz.com", ("VIP", WARM_GOLD), "$8,750"],
            ["Ava Johnson", "ava@shop.co", ("Lead", DUSTY_BLUE), "$0"],
            ["Liam Park", "liam@co.io", ("Active", MINT), "$3,100"],
            ["Emma Davis", "emma@free.net", ("VIP", WARM_GOLD), "$6,400"],
            ["Noah Kim", "noah@design.co", ("Active", MINT), "$2,800"],
            ["Olivia West", "olivia@craft.io", ("Lead", DUSTY_BLUE), "$0"],
        ]
        draw_table(d, sx + 6, sy + 40, cols2, clients_data, fnt_size=15, row_h=30,
                   header_bg=NAVY)
        draw_tab_bar(d, sx, sy, sw, sh, active_idx=1)

    img, draw, _, _ = draw_ipad(img, draw, ipad2_x, ipad2_y, ipad2_w, ipad2_h, client_screen)

    # ── MAIN iPad (front, left) — Dashboard ───
    ipad1_w, ipad1_h = 1200, 880
    ipad1_x = 160
    ipad1_y = 260

    def dashboard_deep(d, sx, sy, sw, sh):
        d.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
        d.rectangle((sx, sy, sx + sw, sy + 36), fill=NAVY)
        d.text((sx + 14, sy + 6), "Dashboard  —  Small Business Planner 2026",
               font=font(20, True), fill=WHITE)

        # KPI cards
        kpis = [("MONTHLY REVENUE", "$8,450", CORAL), ("TOTAL EXPENSES", "$3,120", DUSTY_BLUE),
                ("NET PROFIT", "$5,330", MINT), ("PROFIT MARGIN", "63.1%", WARM_GOLD),
                ("ACTIVE CLIENTS", "12", STEEL_BLUE)]
        card_w2 = (sw - 80) // 5
        card_h2 = 90
        ky = sy + 50
        for i, (t, v, c) in enumerate(kpis):
            cx2 = sx + 14 + i * (card_w2 + 12)
            draw_kpi_card(d, cx2, ky, card_w2, card_h2, t, v, c)

        # 12-month table
        ty2 = ky + card_h2 + 20
        d.text((sx + 14, ty2), "12-MONTH PERFORMANCE TRACKING", font=font(18, True), fill=NAVY)
        ty2 += 28
        cols3 = [130, 120, 120, 120, 120]
        rows3 = [
            ["Month", "Revenue", "Expenses", "Profit", "Margin"],
            ["Jan", "$7,200", "$2,850", "$4,350", "60.4%"],
            ["Feb", "$6,980", "$2,700", "$4,280", "61.3%"],
            ["Mar", "$8,450", "$3,120", "$5,330", "63.1%"],
            ["Apr", "$9,100", "$3,400", "$5,700", "62.6%"],
            ["May", "$8,800", "$3,050", "$5,750", "65.3%"],
            ["Jun", "$10,200", "$3,600", "$6,600", "64.7%"],
            ["Jul", "$9,800", "$3,300", "$6,500", "66.3%"],
            ["Aug", "$11,400", "$3,900", "$7,500", "65.8%"],
        ]
        draw_table(d, sx + 14, ty2, cols3, rows3, fnt_size=15, row_h=26)

        # Bar chart
        chart_x2 = sx + 14 + sum(cols3) + 30
        chart_w2 = sw - (chart_x2 - sx) - 20
        if chart_w2 > 80:
            d.text((chart_x2, ty2 - 28), "REVENUE CHART", font=font(16, True), fill=NAVY)
            vals2 = [72, 69, 84, 91, 88, 102, 98, 114]
            draw_bar_chart_mini(d, chart_x2, ty2, chart_w2, 210, vals2,
                                [CORAL, DUSTY_BLUE, MINT, WARM_GOLD])

        draw_tab_bar(d, sx, sy, sw, sh, active_idx=0)

    img, draw, ow3, oh3 = draw_ipad(img, draw, ipad1_x, ipad1_y, ipad1_w, ipad1_h, dashboard_deep)

    # ── Annotations ───
    ann_fnt = font(24, True)
    draw_annotation(draw, ipad1_x + 80, ipad1_y + 130, "KEY METRICS AT A GLANCE", ann_fnt, "left", 70)
    draw_annotation(draw, ipad1_x + ow3 - 30, ipad1_y + 500, "12-MONTH TRACKING", ann_fnt, "right", 60)
    draw_annotation(draw, ipad2_x + 200, ipad2_y + 200, "CLIENT STATUS BADGES", ann_fnt, "up", 55)
    draw_annotation(draw, ipad1_x + 500, ipad1_y + oh3 - 50, "AUTO-CALCULATING PROFIT", ann_fnt, "down", 50)

    # Bottom bar
    draw.rectangle((0, H - 70, W, H), fill=NAVY)
    text_centered(draw, W // 2, H - 60, "TRACK EVERYTHING IN ONE PLACE  —  INSTANT DIGITAL DOWNLOAD",
                  font(30, True), WHITE)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "03_dashboard_preview.png"), quality=95)
    print("  [OK] 03_dashboard_preview.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 4: CONTENT CALENDAR & INVENTORY — SIDE BY SIDE
# ══════════════════════════════════════════════════════════════════════
def make_image4():
    img = gradient_bg(W, H, ICE_BLUE, WHITE, PALE_BLUE)
    draw = ImageDraw.Draw(img)

    # Decorative
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((W // 2 - 150, -100, W // 2 + 150, 200), fill=(*CORAL, 18))
    od.ellipse((-60, 800, 200, 1060), fill=(*MINT, 20))
    od.ellipse((2500, 1200, 2750, 1450), fill=(*WARM_GOLD, 20))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Title
    fnt_title = font(62, True)
    text_centered(draw, W // 2, 45, "PLAN CONTENT & MANAGE STOCK — EFFORTLESSLY", fnt_title, NAVY)

    fnt_sub = font(30, False)
    text_centered(draw, W // 2, 125, "Two powerful tabs to keep your business organized and stocked",
                  fnt_sub, DUSTY_BLUE)

    # ── LEFT iPad: Content Calendar ───
    lip_w, lip_h = 1100, 820
    lip_x = 80
    lip_y = 220

    def content_screen(d, sx, sy, sw, sh):
        d.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
        d.rectangle((sx, sy, sx + sw, sy + 32), fill=NAVY)
        d.text((sx + 10, sy + 5), "Content Calendar  —  March 2026", font=font(18, True), fill=WHITE)

        cols_c = [100, 130, 200, 200, 120, 150]
        content_rows = [
            ["Date", "Platform", "Topic", "Caption Idea", "Status", "Type"],
            ["Mar 1", ("Instagram", (200, 100, 150)), "Product Launch", "New spring collection!", ("Scheduled", MINT), "Reel"],
            ["Mar 3", ("TikTok", (40, 40, 40)), "Behind the Scenes", "Watch us create...", ("Draft", WARM_GOLD), "Video"],
            ["Mar 5", ("Pinterest", (200, 50, 50)), "Mood Board", "Spring inspiration", ("Posted", DUSTY_BLUE), "Pin"],
            ["Mar 8", ("Instagram", (200, 100, 150)), "Customer Feature", "Meet our fave buyer!", ("Scheduled", MINT), "Story"],
            ["Mar 10", ("Blog", STEEL_BLUE), "How-To Guide", "5 ways to style...", ("Draft", WARM_GOLD), "Article"],
            ["Mar 12", ("Instagram", (200, 100, 150)), "Giveaway", "WIN our bestseller!", ("Idea", CORAL), "Post"],
            ["Mar 15", ("TikTok", (40, 40, 40)), "Tutorial", "Easy DIY candle", ("Draft", WARM_GOLD), "Video"],
            ["Mar 18", ("Pinterest", (200, 50, 50)), "Product Flat Lay", "Styled collection", ("Idea", CORAL), "Pin"],
            ["Mar 20", ("Instagram", (200, 100, 150)), "Testimonial", "5-star review share", ("Scheduled", MINT), "Post"],
            ["Mar 22", ("Blog", STEEL_BLUE), "Gift Guide", "Best gifts under $30", ("Draft", WARM_GOLD), "Article"],
        ]
        fnt_s2 = font(13, False)
        fnt_sb2 = font(13, True)
        rh2 = 26
        ty3 = sy + 40
        total_w2 = sum(cols_c)
        # Header
        d.rectangle((sx + 6, ty3, sx + 6 + total_w2, ty3 + rh2), fill=NAVY)
        cx3 = sx + 6
        for ci, (cw, cell) in enumerate(zip(cols_c, content_rows[0])):
            d.text((cx3 + 4, ty3 + 4), cell, font=fnt_sb2, fill=WHITE)
            cx3 += cw
        ty3 += rh2
        for ri, row in enumerate(content_rows[1:]):
            bg2 = ICE_BLUE if ri % 2 == 0 else WHITE
            d.rectangle((sx + 6, ty3, sx + 6 + total_w2, ty3 + rh2), fill=bg2)
            cx3 = sx + 6
            for ci, (cw, cell) in enumerate(zip(cols_c, row)):
                if isinstance(cell, tuple):
                    txt, col = cell
                    tw3 = text_width(d, txt, fnt_s2)
                    d.rounded_rectangle((cx3 + 4, ty3 + 3, cx3 + tw3 + 18, ty3 + rh2 - 3),
                                        radius=5, fill=col)
                    d.text((cx3 + 11, ty3 + 4), txt, font=font(11, True), fill=WHITE)
                else:
                    d.text((cx3 + 4, ty3 + 4), cell, font=fnt_s2, fill=DARK_TEXT)
                cx3 += cw
            ty3 += rh2

        draw_tab_bar(d, sx, sy, sw, sh, active_idx=4)

    img, draw, ow4, oh4 = draw_ipad(img, draw, lip_x, lip_y, lip_w, lip_h, content_screen)

    # ── RIGHT iPad: Inventory Manager ───
    rip_w, rip_h = 1100, 820
    rip_x = W - rip_w - 130
    rip_y = 220

    def inventory_screen(d, sx, sy, sw, sh):
        d.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
        d.rectangle((sx, sy, sx + sw, sy + 32), fill=NAVY)
        d.text((sx + 10, sy + 5), "Inventory Manager", font=font(18, True), fill=WHITE)

        cols_i = [180, 90, 90, 100, 110, 120, 110]
        inv_rows = [
            ["Product", "SKU", "Qty", "Reorder", "Status", "Cost", "Price"],
            ["Candle - Vanilla", "CV-001", "45", "10", ("In Stock", MINT), "$4.50", "$18.00"],
            ["Candle - Rose", "CR-002", "8", "15", ("Low Stock", WARM_GOLD), "$5.00", "$22.00"],
            ["Gift Box Set", "GB-003", "0", "5", ("Reorder", CORAL), "$12.00", "$45.00"],
            ["Wax Melts 6pk", "WM-004", "32", "10", ("In Stock", MINT), "$3.00", "$14.00"],
            ["Matches Tin", "MT-005", "5", "20", ("Low Stock", WARM_GOLD), "$1.50", "$8.00"],
            ["Candle - Lavender", "CL-006", "28", "10", ("In Stock", MINT), "$4.50", "$18.00"],
            ["Reed Diffuser", "RD-007", "3", "8", ("Low Stock", WARM_GOLD), "$6.00", "$28.00"],
            ["Candle - Cedar", "CC-008", "0", "10", ("Reorder", CORAL), "$5.50", "$24.00"],
            ["Gift Wrap Roll", "GW-009", "60", "20", ("In Stock", MINT), "$2.00", "$6.00"],
            ["Wick Trimmer", "WT-010", "18", "10", ("In Stock", MINT), "$3.50", "$12.00"],
        ]
        fnt_s3 = font(13, False)
        fnt_sb3 = font(13, True)
        rh3 = 26
        ty4 = sy + 40
        total_w3 = sum(cols_i)
        # Header
        d.rectangle((sx + 4, ty4, sx + 4 + total_w3, ty4 + rh3), fill=NAVY)
        cx4 = sx + 4
        for cw, cell in zip(cols_i, inv_rows[0]):
            d.text((cx4 + 4, ty4 + 4), cell, font=fnt_sb3, fill=WHITE)
            cx4 += cw
        ty4 += rh3
        for ri, row in enumerate(inv_rows[1:]):
            bg3 = ICE_BLUE if ri % 2 == 0 else WHITE
            d.rectangle((sx + 4, ty4, sx + 4 + total_w3, ty4 + rh3), fill=bg3)
            cx4 = sx + 4
            for ci, (cw, cell) in enumerate(zip(cols_i, row)):
                if isinstance(cell, tuple):
                    txt, col = cell
                    tw4 = text_width(d, txt, fnt_s3)
                    d.rounded_rectangle((cx4 + 3, ty4 + 3, cx4 + tw4 + 16, ty4 + rh3 - 3),
                                        radius=5, fill=col)
                    d.text((cx4 + 10, ty4 + 4), txt, font=font(11, True), fill=WHITE)
                else:
                    d.text((cx4 + 4, ty4 + 4), str(cell), font=fnt_s3, fill=DARK_TEXT)
                cx4 += cw
            ty4 += rh3

        draw_tab_bar(d, sx, sy, sw, sh, active_idx=6)

    img, draw, ow5, oh5 = draw_ipad(img, draw, rip_x, rip_y, rip_w, rip_h, inventory_screen)

    # ── Annotations ───
    ann_fnt2 = font(24, True)
    draw_annotation(draw, lip_x + 250, lip_y + 100, "12 PLATFORM OPTIONS", ann_fnt2, "up", 50)
    draw_annotation(draw, lip_x + ow4 - 60, lip_y + oh4 // 2, "20 CONTENT IDEAS", ann_fnt2, "right", 50)
    draw_annotation(draw, rip_x + 250, rip_y + 100, "AUTO REORDER ALERTS", ann_fnt2, "up", 50)
    draw_annotation(draw, rip_x + ow5 - 60, rip_y + oh5 // 2, "PROFIT PER UNIT", ann_fnt2, "right", 50)

    # Bottom bar
    bar_h3 = 80
    draw.rectangle((0, H - bar_h3, W, H), fill=NAVY)
    text_centered(draw, W // 2, H - bar_h3 + 18,
                  "NEVER RUN OUT OF STOCK  •  NEVER MISS A POST  —  $12.99",
                  font(34, True), WHITE)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "04_content_inventory.png"), quality=95)
    print("  [OK] 04_content_inventory.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 5: VALUE PROPOSITION — WHY BUY
# ══════════════════════════════════════════════════════════════════════
def make_image5():
    # Top 60% navy gradient, bottom 40% light
    img = Image.new("RGBA", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Navy gradient top
    split_y = int(H * 0.60)
    for y in range(split_y):
        t = y / split_y
        r = int(NAVY[0] + (STEEL_BLUE[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (STEEL_BLUE[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (STEEL_BLUE[2] - NAVY[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # Light bottom gradient
    for y in range(split_y, H):
        t = (y - split_y) / (H - split_y)
        r = int(ICE_BLUE[0] + (WHITE[0] - ICE_BLUE[0]) * t)
        g = int(ICE_BLUE[1] + (WHITE[1] - ICE_BLUE[1]) * t)
        b = int(ICE_BLUE[2] + (WHITE[2] - ICE_BLUE[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # Subtle radial glow behind iPad area
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for rr in range(400, 0, -5):
        alpha = int(15 * (1 - rr / 400))
        od.ellipse((W // 2 - rr, split_y - 200 - rr, W // 2 + rr, split_y - 200 + rr),
                   fill=(214, 228, 240, alpha))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # ── Centered iPad showing filled dashboard ───
    ipad_cw, ipad_ch = 1050, 700
    ipad_cx = W // 2 - (ipad_cw + 44) // 2
    ipad_cy = 160

    def value_screen(d2, sx, sy, sw, sh):
        d2.rectangle((sx, sy, sx + sw, sy + sh), fill=ICE_BLUE)
        d2.rectangle((sx, sy, sx + sw, sy + 30), fill=NAVY)
        d2.text((sx + 10, sy + 4), "Small Business Planner 2026", font=font(16, True), fill=WHITE)
        # KPIs
        kpis = [("REVENUE", "$8,450", CORAL), ("EXPENSES", "$3,120", DUSTY_BLUE),
                ("PROFIT", "$5,330", MINT), ("MARGIN", "63.1%", WARM_GOLD)]
        cw2 = (sw - 50) // 4
        ch2 = 70
        ky2 = sy + 40
        for i, (t, v, c) in enumerate(kpis):
            cx5 = sx + 10 + i * (cw2 + 10)
            draw_kpi_card(d2, cx5, ky2, cw2, ch2, t, v, c)
        # Mini table
        ty5 = ky2 + ch2 + 14
        cols5 = [120, 100, 100, 100, 100]
        rows5 = [
            ["Month", "Revenue", "Expenses", "Profit", "Margin"],
            ["Jan", "$7,200", "$2,850", "$4,350", "60.4%"],
            ["Feb", "$6,980", "$2,700", "$4,280", "61.3%"],
            ["Mar", "$8,450", "$3,120", "$5,330", "63.1%"],
            ["Apr", "$9,100", "$3,400", "$5,700", "62.6%"],
            ["May", "$8,800", "$3,050", "$5,750", "65.3%"],
        ]
        draw_table(d2, sx + 10, ty5, cols5, rows5, fnt_size=13, row_h=24)
        # Chart
        chart_x3 = sx + 10 + sum(cols5) + 20
        chart_w3 = sw - (chart_x3 - sx) - 14
        if chart_w3 > 60:
            draw_bar_chart_mini(d2, chart_x3, ty5, chart_w3, 150,
                                [72, 69, 84, 91, 88],
                                [CORAL, DUSTY_BLUE, MINT, WARM_GOLD, CORAL])
        draw_tab_bar(d2, sx, sy, sw, sh, active_idx=0)

    img, draw, ow6, oh6 = draw_ipad(img, draw, ipad_cx, ipad_cy, ipad_cw, ipad_ch, value_screen)

    # ── Floating feature badges around iPad ───
    badge_data = [
        ("9 Tabs", ipad_cx - 120, ipad_cy + 100, CORAL),
        ("Auto Formulas", ipad_cx - 80, ipad_cy + 300, WARM_GOLD),
        ("Drop-Down Menus", ipad_cx - 100, ipad_cy + 500, MINT),
        ("50-Row CRM", ipad_cx + ow6 + 40, ipad_cy + 80, DUSTY_BLUE),
        ("Content Calendar", ipad_cx + ow6 + 20, ipad_cy + 280, CORAL),
        ("Inventory Alerts", ipad_cx + ow6 + 50, ipad_cy + 480, WARM_GOLD),
    ]
    badge_fnt2 = font(24, True)
    for txt, bx, by, col in badge_data:
        tw5 = text_width(draw, txt, badge_fnt2)
        th5 = text_height(draw, txt, badge_fnt2)
        px2, py2 = 22, 12
        draw.rounded_rectangle((bx - px2, by - py2, bx + tw5 + px2, by + th5 + py2),
                                radius=20, fill=col)
        draw.text((bx, by), txt, font=badge_fnt2, fill=WHITE)
        # Connecting line to iPad area
        if bx < ipad_cx:
            draw.line((bx + tw5 + px2, by + th5 // 2, ipad_cx + 10, by + th5 // 2),
                      fill=(*col, 120), width=2)
        else:
            draw.line((bx - px2, by + th5 // 2, ipad_cx + ow6 - 10, by + th5 // 2),
                      fill=(*col, 120), width=2)

    # ── Main tagline ───
    tag_y = split_y + 30
    fnt_tag = font(58, True)
    text_centered(draw, W // 2, tag_y,
                  "RUN YOUR BUSINESS LIKE A PRO — FROM DAY ONE", fnt_tag, NAVY)

    # Price badge
    price_y = tag_y + 85
    price_txt = "$12.99 — INSTANT DOWNLOAD"
    pfnt = font(40, True)
    pw2 = text_width(draw, price_txt, pfnt) + 80
    draw.rounded_rectangle((W // 2 - pw2 // 2, price_y, W // 2 + pw2 // 2, price_y + 70),
                            radius=35, fill=CORAL)
    text_centered(draw, W // 2, price_y + 12, price_txt, pfnt, WHITE)

    # 5-star rating
    star_y = price_y + 90
    star_fnt = font(36, False)
    stars = "★ ★ ★ ★ ★"
    text_centered(draw, W // 2, star_y, stars, star_fnt, WARM_GOLD)
    sub_fnt2 = font(26, False)
    text_centered(draw, W // 2, star_y + 50, "No subscriptions. Yours forever.", sub_fnt2, STEEL_BLUE)

    # Works with
    compat_y = star_y + 110
    compat_fnt = font(28, True)
    text_centered(draw, W // 2, compat_y,
                  "WORKS WITH:  Google Sheets  |  Excel  |  LibreOffice",
                  compat_fnt, DUSTY_BLUE)

    # Bottom bar
    draw.rectangle((0, H - 60, W, H), fill=NAVY)
    text_centered(draw, W // 2, H - 52, "DIGITAL DOWNLOAD  —  EDIT IN GOOGLE SHEETS OR EXCEL  —  LIFETIME ACCESS",
                  font(24, True), WHITE)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "05_value_proposition.png"), quality=95)
    print("  [OK] 05_value_proposition.png")


# ══════════════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Product 2 images...")
    make_image1()
    make_image2()
    make_image3()
    make_image4()
    make_image5()
    print("Done! All 5 images saved to:", OUT)
