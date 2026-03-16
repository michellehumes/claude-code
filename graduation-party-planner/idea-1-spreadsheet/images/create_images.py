#!/usr/bin/env python3
"""
Etsy Listing Images for Graduation Party Planner Spreadsheet
3 images at 2700 x 2025 px, 4:3 ratio, 300 DPI, RGB
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── DIMENSIONS ────────────────────────────────────────────────────────────────
W, H = 2700, 2025
MARGIN = 150
DPI = 300

# ── COLORS ────────────────────────────────────────────────────────────────────
C = {
    "bg":           (254, 254, 254),
    "white":        (255, 255, 255),
    "primary":      (251, 88, 135),    # #fb5887 pink
    "primary_light":(253, 232, 239),
    "secondary":    (60, 164, 215),    # #3ca4d7 blue
    "secondary_light":(223, 240, 249),
    "highlight":    (254, 140, 67),    # #fe8c43 orange
    "highlight_light":(255, 240, 230),
    "dark":         (44, 62, 80),      # #2C3E50
    "gray":         (127, 140, 141),
    "light_gray":   (236, 240, 241),
    "success":      (39, 174, 96),
    "black":        (0, 0, 0),
    "card_bg":      (248, 249, 250),
}


# ── FONT HELPERS ──────────────────────────────────────────────────────────────
def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ── DRAWING HELPERS ───────────────────────────────────────────────────────────
def new_image():
    img = Image.new("RGB", (W, H), C["bg"])
    return img, ImageDraw.Draw(img)


def draw_rect(draw, xy, fill, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=16, fill=fill, outline=outline, width=width)


def draw_text_centered(draw, text, y, font, color, max_width=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, fill=color, font=font)
    return bbox[3] - bbox[1]  # return height


def draw_badge(draw, text, cx, cy, fill, text_color=None, w=320, h=54, font_size=24):
    text_color = text_color or C["white"]
    draw.rounded_rectangle(
        (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2),
        radius=27, fill=fill
    )
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=text_color, font=font)


def draw_top_accent_bar(draw, fill=None):
    fill = fill or C["primary"]
    draw.rectangle((0, 0, W, 14), fill=fill)


def draw_bottom_accent_bar(draw, fill=None):
    fill = fill or C["primary"]
    draw.rectangle((0, H - 14, W, H), fill=fill)


def draw_spreadsheet_mockup(draw, x, y, w, h):
    """Draw a simplified spreadsheet panel mockup."""
    # Outer frame
    draw.rounded_rectangle((x, y, x + w, y + h), radius=12,
                            fill=C["white"], outline=C["light_gray"], width=3)
    # Header bar
    header_h = 44
    draw.rounded_rectangle((x, y, x + w, y + header_h), radius=12, fill=C["dark"])
    draw.rectangle((x, y + header_h - 12, x + w, y + header_h), fill=C["dark"])

    # Tab labels
    tabs = ["Dashboard", "Guests", "Budget", "Checklist", "Food", "Timeline"]
    tab_w = w // len(tabs)
    font_sm = get_font(20, bold=False)
    for i, tab in enumerate(tabs):
        tx = x + i * tab_w
        if i == 0:
            draw.rectangle((tx, y + header_h, tx + tab_w, y + header_h + 32), fill=C["primary"])
            col = C["white"]
        else:
            draw.rectangle((tx, y + header_h, tx + tab_w, y + header_h + 32), fill=C["light_gray"])
            col = C["gray"]
        bbox = draw.textbbox((0, 0), tab, font=font_sm)
        tw = bbox[2] - bbox[0]
        draw.text((tx + (tab_w - tw) // 2, y + header_h + 7), tab, fill=col, font=font_sm)

    row_y = y + header_h + 32 + 10

    # Column headers
    col_headers = ["Item", "Category", "Est. Cost", "Actual", "Paid"]
    col_w = (w - 20) // len(col_headers)
    font_col = get_font(22, bold=True)
    for i, ch in enumerate(col_headers):
        cx = x + 10 + i * col_w
        draw.rectangle((cx, row_y, cx + col_w - 4, row_y + 30), fill=C["dark"])
        bbox = draw.textbbox((0, 0), ch, font=font_col)
        tw = bbox[2] - bbox[0]
        draw.text((cx + (col_w - tw) // 2, row_y + 5), ch, fill=C["white"], font=font_col)

    # Data rows
    data = [
        ["Venue", "Venue", "$500", "$480", "Yes"],
        ["Catering", "Catering", "$300", "$315", "Yes"],
        ["Decorations", "Decor", "$150", "$132", "No"],
        ["Cake", "Cake", "$80", "$85", "Partial"],
        ["Flowers", "Flowers", "$60", "", "No"],
        ["Invitations", "Print", "$40", "$38", "Yes"],
    ]
    row_colors = [C["white"], C["primary_light"]]
    paid_colors = {"Yes": C["success"], "No": C["primary"], "Partial": C["highlight"]}
    font_data = get_font(20, bold=False)
    font_data_b = get_font(20, bold=True)

    for ri, row_data in enumerate(data):
        ry = row_y + 30 + ri * 30
        bg = row_colors[ri % 2]
        draw.rectangle((x + 10, ry, x + w - 10, ry + 29), fill=bg)
        for ci, cell_val in enumerate(row_data):
            cx = x + 10 + ci * col_w
            if ci == 4 and cell_val in paid_colors:  # Paid column
                status_color = paid_colors[cell_val]
                draw.rounded_rectangle((cx + 4, ry + 6, cx + col_w - 8, ry + 23),
                                       radius=8, fill=status_color)
                bbox = draw.textbbox((0, 0), cell_val, font=font_data_b)
                tw = bbox[2] - bbox[0]
                draw.text((cx + (col_w - tw) // 2, ry + 7), cell_val,
                          fill=C["white"], font=font_data_b)
            else:
                bbox = draw.textbbox((0, 0), cell_val, font=font_data)
                draw.text((cx + 6, ry + 6), cell_val, fill=C["dark"], font=font_data)

    # Total row
    total_y = row_y + 30 + len(data) * 30
    draw.rectangle((x + 10, total_y, x + w - 10, total_y + 30), fill=C["dark"])
    font_tot = get_font(22, bold=True)
    draw.text((x + 16, total_y + 5), "TOTAL", fill=C["white"], font=font_tot)
    draw.text((x + 10 + 2 * col_w + 6, total_y + 5), "$1,130", fill=C["highlight"], font=font_tot)
    draw.text((x + 10 + 3 * col_w + 6, total_y + 5), "$1,050", fill=C["primary"], font=font_tot)


# ── IMAGE 1: HERO ─────────────────────────────────────────────────────────────
def create_hero():
    img, draw = new_image()
    draw_top_accent_bar(draw, C["primary"])
    draw_bottom_accent_bar(draw, C["primary"])

    # Top badge
    draw_badge(draw, "DIGITAL DOWNLOAD — INSTANT ACCESS", W // 2, 60,
               fill=C["primary_light"], text_color=C["primary"], w=680, h=50, font_size=22)

    # Headline
    font_h = get_font(96, bold=True)
    draw_text_centered(draw, "GRADUATION PARTY", 110, font_h, C["dark"])
    draw_text_centered(draw, "PLANNER", 210, font_h, C["primary"])

    # Subheadline
    font_sub = get_font(40, bold=False)
    draw_text_centered(draw, "Plan the perfect graduation party — all in one spreadsheet", 330, font_sub, C["gray"])

    # Spreadsheet mockup
    mock_x, mock_y = MARGIN, 400
    mock_w, mock_h = W - MARGIN * 2, 1050
    draw_spreadsheet_mockup(draw, mock_x, mock_y, mock_w, mock_h)

    # Feature pills at bottom
    features = ["Guest List", "Budget Tracker", "Decoration Checklist", "Food Planner", "Party Timeline"]
    pill_w = 310
    pill_gap = 30
    total_pill_w = len(features) * pill_w + (len(features) - 1) * pill_gap
    start_x = (W - total_pill_w) // 2
    pill_y = 1490
    colors = [C["primary"], C["secondary"], C["highlight"], C["secondary"], C["primary"]]
    font_pill = get_font(26, bold=True)
    for i, (feat, col) in enumerate(zip(features, colors)):
        px = start_x + i * (pill_w + pill_gap)
        draw.rounded_rectangle((px, pill_y, px + pill_w, pill_y + 52), radius=26, fill=col)
        bbox = draw.textbbox((0, 0), feat, font=font_pill)
        tw = bbox[2] - bbox[0]
        draw.text((px + (pill_w - tw) // 2, pill_y + 13), feat, fill=C["white"], font=font_pill)

    # Works with
    font_works = get_font(30, bold=False)
    draw_text_centered(draw, "Works with Microsoft Excel & Google Sheets", 1580, font_works, C["gray"])

    # Price badge
    draw_badge(draw, "$5.99 — Instant Download", W // 2, 1670,
               fill=C["highlight"], text_color=C["white"], w=520, h=62, font_size=30)

    # Star rating
    font_star = get_font(34, bold=True)
    draw_text_centered(draw, "★★★★★  Loved by thousands of party planners", 1760, font_star, C["highlight"])

    # Bottom tagline
    font_tag = get_font(32, bold=False)
    draw_text_centered(draw, "No apps. No subscriptions. Just download, open, and start planning.", 1830, font_tag, C["gray"])

    img.save("01_hero.png", dpi=(DPI, DPI))
    print("✓ Saved 01_hero.png")


# ── IMAGE 2: BEFORE / AFTER ───────────────────────────────────────────────────
def create_before_after():
    img, draw = new_image()
    draw_top_accent_bar(draw, C["primary"])
    draw_bottom_accent_bar(draw, C["secondary"])

    # Main headline
    font_h = get_font(82, bold=True)
    draw_text_centered(draw, "STOP STRESSING ABOUT GRAD PARTIES", 30, font_h, C["dark"])

    # Sub
    font_sub = get_font(38, bold=False)
    draw_text_centered(draw, "Plan everything in one spreadsheet — organized, clear, stress-free.", 140, font_sub, C["gray"])

    # Divider line
    mid_x = W // 2
    draw.rectangle((mid_x - 3, 185, mid_x + 3, H - 30), fill=C["light_gray"])

    panel_top = 185
    panel_bot = H - 40
    panel_h = panel_bot - panel_top

    # ── LEFT (BEFORE) ──
    left_x1, left_x2 = MARGIN // 2, mid_x - 20
    draw.rounded_rectangle((left_x1, panel_top, left_x2, panel_bot),
                            radius=16, fill=C["primary_light"])

    # BEFORE label
    font_label = get_font(64, bold=True)
    bbox = draw.textbbox((0, 0), "BEFORE", font=font_label)
    bw = bbox[2] - bbox[0]
    draw.rounded_rectangle((left_x1 + 20, panel_top + 20, left_x1 + 20 + bw + 40, panel_top + 78),
                            radius=12, fill=C["primary"])
    draw.text((left_x1 + 40, panel_top + 24), "BEFORE", fill=C["white"], font=font_label)

    # Chaos items
    chaos_items = [
        ("📋 Random sticky notes everywhere", 120),
        ("🧮 Calculator on a napkin", 190),
        ("📱 Group chat chaos — who's coming??", 260),
        ("💸 No idea what you've spent", 330),
        ("😰 Forgot to order the cake", 400),
        ("🗒️ 6 different scraps of paper", 470),
        ("❓ What time does the party start?", 540),
        ("📦 Did I buy enough decorations?", 610),
    ]
    font_chaos = get_font(32, bold=False)
    for text, offset in chaos_items:
        draw.text((left_x1 + 40, panel_top + offset), text, fill=C["dark"], font=font_chaos)

    # Stress emoji
    font_big = get_font(120, bold=True)
    draw_text_centered(draw, "😫", panel_top + 730, font_big, C["primary"])
    font_stress = get_font(36, bold=True)
    left_center = (left_x1 + left_x2) // 2
    bbox = draw.textbbox((0, 0), "Overwhelming!", font=font_stress)
    bw = bbox[2] - bbox[0]
    draw.text((left_center - bw // 2, panel_top + 870), "Overwhelming!", fill=C["primary"], font=font_stress)

    # ── RIGHT (AFTER) ──
    right_x1, right_x2 = mid_x + 20, W - MARGIN // 2
    draw.rounded_rectangle((right_x1, panel_top, right_x2, panel_bot),
                            radius=16, fill=C["secondary_light"])

    # AFTER label
    bbox = draw.textbbox((0, 0), "AFTER", font=font_label)
    bw = bbox[2] - bbox[0]
    draw.rounded_rectangle((right_x1 + 20, panel_top + 20, right_x1 + 20 + bw + 40, panel_top + 78),
                            radius=12, fill=C["success"])
    draw.text((right_x1 + 40, panel_top + 24), "AFTER", fill=C["white"], font=font_label)

    # Organized items
    organized = [
        ("✅ Guest list with RSVPs tracked", 120),
        ("✅ Budget vs actual — at a glance", 190),
        ("✅ Decoration checklist — done!", 260),
        ("✅ Timeline with every task mapped", 330),
        ("✅ Food planner with who's bringing what", 400),
        ("✅ Cake ordered — weeks in advance", 470),
        ("✅ All details in one place", 540),
        ("✅ Headcount confirmed and ready", 610),
    ]
    font_org = get_font(32, bold=False)
    for text, offset in organized:
        draw.text((right_x1 + 40, panel_top + offset), text, fill=C["dark"], font=font_org)

    # Celebrate emoji
    draw_text_centered(draw, "🎉", panel_top + 730, font_big, C["success"])
    font_calm = get_font(36, bold=True)
    right_center = (right_x1 + right_x2) // 2
    bbox = draw.textbbox((0, 0), "Stress-Free!", font=font_calm)
    bw = bbox[2] - bbox[0]
    draw.text((right_center - bw // 2, panel_top + 870), "Stress-Free!", fill=C["success"], font=font_calm)

    # Bottom text
    font_bottom = get_font(36, bold=True)
    draw_text_centered(draw, "Plan everything in one spreadsheet.", H - 80, font_bottom, C["dark"])

    img.save("02_before_after.png", dpi=(DPI, DPI))
    print("✓ Saved 02_before_after.png")


# ── IMAGE 3: WHAT'S INCLUDED ──────────────────────────────────────────────────
def create_whats_included():
    img, draw = new_image()
    draw_top_accent_bar(draw, C["primary"])
    draw_bottom_accent_bar(draw, C["secondary"])

    # Headline
    font_h = get_font(90, bold=True)
    draw_text_centered(draw, "WHAT'S INCLUDED", 30, font_h, C["dark"])

    font_sub = get_font(38, bold=False)
    draw_text_centered(draw, "6 fully organized tabs — everything you need to plan the perfect party", 140, font_sub, C["gray"])

    # 6 feature cards in 3x2 grid
    cards = [
        ("📊", "Dashboard", "Summary view: guests confirmed,\nbudget spent, tasks done", C["primary"]),
        ("👥", "Guest List", "Track RSVPs, meal choices,\ngifts, and notes", C["secondary"]),
        ("💰", "Budget Tracker", "Estimated vs actual costs,\npaid status, auto totals", C["highlight"]),
        ("🍽️", "Food Planner", "Plan your menu & track\nwho's bringing each dish", C["secondary"]),
        ("🎀", "Decoration Checklist", "Check off every item as you\nbuy or prepare it", C["primary"]),
        ("🗓️", "Party Timeline", "Week-by-week task list so\nnothing falls through the cracks", C["highlight"]),
    ]

    card_w = 760
    card_h = 580
    cols = 3
    rows = 2
    gap_x = (W - MARGIN * 2 - card_w * cols) // (cols - 1)
    gap_y = 40

    start_y = 210
    start_x = MARGIN

    font_emoji = get_font(80, bold=False)
    font_card_title = get_font(44, bold=True)
    font_card_body = get_font(28, bold=False)

    for i, (emoji, title, desc, color) in enumerate(cards):
        row = i // cols
        col = i % cols
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        # Card background
        draw.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=20,
                                fill=C["white"], outline=color, width=4)

        # Color top strip
        draw.rounded_rectangle((cx, cy, cx + card_w, cy + 12), radius=4, fill=color)
        draw.rectangle((cx, cy + 8, cx + card_w, cy + 12), fill=color)

        # Emoji circle
        circle_r = 65
        circle_cx = cx + card_w // 2
        circle_cy = cy + 100
        draw.ellipse((circle_cx - circle_r, circle_cy - circle_r,
                      circle_cx + circle_r, circle_cy + circle_r), fill=color)
        bbox = draw.textbbox((0, 0), emoji, font=font_emoji)
        ew = bbox[2] - bbox[0]
        eh = bbox[3] - bbox[1]
        draw.text((circle_cx - ew // 2, circle_cy - eh // 2 - 6), emoji,
                  fill=C["white"], font=font_emoji)

        # Title
        bbox = draw.textbbox((0, 0), title, font=font_card_title)
        tw = bbox[2] - bbox[0]
        draw.text((cx + (card_w - tw) // 2, cy + 190), title, fill=C["dark"], font=font_card_title)

        # Description (multi-line)
        lines = desc.split("\n")
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_card_body)
            lw = bbox[2] - bbox[0]
            draw.text((cx + (card_w - lw) // 2, cy + 255 + li * 40), line,
                      fill=C["gray"], font=font_card_body)

        # Bottom colored tab
        draw.rounded_rectangle((cx + card_w // 2 - 60, cy + card_h - 52,
                                 cx + card_w // 2 + 60, cy + card_h - 16),
                                radius=8, fill=color)
        font_tab = get_font(22, bold=True)
        bbox = draw.textbbox((0, 0), "Tab " + str(i + 1), font=font_tab)
        tw = bbox[2] - bbox[0]
        draw.text((cx + card_w // 2 - tw // 2, cy + card_h - 48), "Tab " + str(i + 1),
                  fill=C["white"], font=font_tab)

    # Bottom CTA
    font_cta = get_font(36, bold=True)
    draw_text_centered(draw, "Works with Microsoft Excel & Google Sheets  •  $5.99  •  Instant Download",
                       H - 80, font_cta, C["dark"])

    img.save("03_whats_included.png", dpi=(DPI, DPI))
    print("✓ Saved 03_whats_included.png")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_hero()
    create_before_after()
    create_whats_included()
    print("\nAll 3 listing images created.")
