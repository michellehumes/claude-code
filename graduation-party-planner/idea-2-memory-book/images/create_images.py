#!/usr/bin/env python3
"""
Etsy Listing Images for Graduation Memory Book Printable
3 images at 2700 x 2025 px, 4:3 ratio, 300 DPI, RGB
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2700, 2025
MARGIN = 150
DPI = 300

C = {
    "bg":           (255, 253, 245),   # Cream
    "white":        (255, 255, 255),
    "gold":         (212, 175, 55),    # #D4AF37
    "gold_light":   (255, 248, 220),
    "pink":         (251, 88, 135),    # #fb5887
    "pink_light":   (253, 232, 239),
    "dark":         (30, 30, 30),
    "gray":         (100, 100, 100),
    "light_gray":   (220, 220, 220),
    "cream":        (255, 253, 245),
    "success":      (39, 174, 96),
    "black":        (0, 0, 0),
}


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def new_image():
    img = Image.new("RGB", (W, H), C["bg"])
    return img, ImageDraw.Draw(img)


def draw_text_centered(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)
    return bbox[3] - bbox[1]


def draw_gold_line(draw, y, x1=None, x2=None, width=4):
    x1 = x1 or MARGIN
    x2 = x2 or W - MARGIN
    draw.rectangle((x1, y, x2, y + width), fill=C["gold"])


def draw_page_mockup(draw, x, y, w, h, title, color, items=None):
    """Draw a simplified printable page preview."""
    # Shadow
    draw.rounded_rectangle((x + 8, y + 8, x + w + 8, y + h + 8), radius=8, fill=C["light_gray"])
    # Page body
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=C["white"], outline=C["gold"], width=3)
    # Color header strip
    draw.rounded_rectangle((x, y, x + w, y + 40), radius=8, fill=color)
    draw.rectangle((x, y + 32, x + w, y + 40), fill=color)
    # Title in header
    font_title = get_font(min(26, max(16, w // 14)), bold=True)
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw) // 2, y + 9), title, fill=C["white"], font=font_title)
    # Gold divider below header
    draw.rectangle((x + 10, y + 44, x + w - 10, y + 47), fill=C["gold"])
    # Content lines
    if items:
        font_item = get_font(min(18, max(12, w // 22)), bold=False)
        for i, item in enumerate(items[:5]):
            iy = y + 56 + i * (h - 70) // min(len(items[:5]), 5)
            draw.rectangle((x + 16, iy, x + w - 16, iy + 2), fill=C["light_gray"])
            if i < len(items):
                draw.text((x + 18, iy - 16), item, fill=C["gray"], font=font_item)
    else:
        # Generic lines
        for i in range(5):
            ly = y + 60 + i * (h - 80) // 5
            line_w = w - 30 if i % 2 == 0 else w - 60
            draw.rectangle((x + 15, ly, x + 15 + line_w, ly + 3), fill=C["light_gray"])
    # Photo placeholder box
    if h > 180:
        ph_y = y + h - 80
        ph_h = 60
        draw.rounded_rectangle((x + 15, ph_y, x + w - 15, ph_y + ph_h),
                                radius=4, fill=C["gold_light"], outline=C["gold"], width=2)
        font_ph = get_font(14, bold=False)
        bbox = draw.textbbox((0, 0), "Photo", font=font_ph)
        tw2 = bbox[2] - bbox[0]
        draw.text((x + (w - tw2) // 2, ph_y + 22), "Photo", fill=C["gold"], font=font_ph)


# ── IMAGE 1: HERO ─────────────────────────────────────────────────────────────
def create_hero():
    img, draw = new_image()

    # Top and bottom accent bars
    draw.rectangle((0, 0, W, 14), fill=C["gold"])
    draw.rectangle((0, H - 14, W, H), fill=C["pink"])

    # Badge
    badge_text = "PRINTABLE PDF — INSTANT DOWNLOAD"
    font_badge = get_font(26, bold=True)
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bx = (W - bw - 60) // 2
    draw.rounded_rectangle((bx, 28, bx + bw + 60, 78), radius=25, fill=C["pink_light"])
    draw.text((bx + 30, 40), badge_text, fill=C["pink"], font=font_badge)

    # Headline
    font_h1 = get_font(100, bold=True)
    font_h2 = get_font(72, bold=True)
    draw_text_centered(draw, "GRADUATION", 90, font_h1, C["dark"])
    draw_text_centered(draw, "MEMORY BOOK", 200, font_h2, C["gold"])

    # Gold divider
    draw_gold_line(draw, 302, MARGIN + 200, W - MARGIN - 200)

    # Subtitle
    font_sub = get_font(38, bold=False)
    draw_text_centered(draw, "Capture every special moment of your graduate's journey", 320, font_sub, C["gray"])

    # Stacked pages mockup
    pages_data = [
        ("Achievements", C["gold"], ["Awards & Honors", "Clubs & Sports", "Proud Moments"]),
        ("School Memories", C["pink"], ["Funniest Memory", "Proudest Moment", "Favorite Tradition"]),
        ("About the Graduate", C["dark"], ["Name, School, Year", "Favorite Quote", "Best Friends"]),
    ]

    # Draw stacked at angles
    center_x = W // 2
    base_y = 430
    page_w, page_h = 620, 760

    # Back pages (slightly rotated effect via offset)
    offsets = [(-50, 30, C["gold"]), (0, 15, C["pink"]), (50, 0, C["dark"])]
    for i, ((title, color, items), (ox, oy, _)) in enumerate(zip(pages_data, offsets)):
        px = center_x - page_w // 2 + ox
        py = base_y + oy
        alpha = max(0, 180 - i * 40)
        if i < len(pages_data) - 1:
            # Shadow/back page tint
            draw.rounded_rectangle((px + 8, py + 8, px + page_w + 8, py + page_h + 8),
                                   radius=10, fill=C["light_gray"])
            draw.rounded_rectangle((px, py, px + page_w, py + page_h),
                                   radius=10, fill=C["cream"], outline=C["gold"], width=2)
        else:
            draw_page_mockup(draw, px, py, page_w, page_h, title, color, items)

    # Feature list below
    features = [
        "✦  About the Graduate",
        "✦  School Memories",
        "✦  Favorite Teachers",
        "✦  Achievements",
        "✦  Future Plans",
        "✦  Messages from Family",
        "✦  Photo Pages",
    ]
    font_feat = get_font(32, bold=False)
    feat_start_y = 1250
    col1_x = W // 2 - 380
    col2_x = W // 2 + 40
    for i, feat in enumerate(features):
        col_x = col1_x if i < 4 else col2_x
        fy = feat_start_y + (i % 4) * 50
        draw.text((col_x, fy), feat, fill=C["dark"], font=font_feat)

    draw_gold_line(draw, 1460, MARGIN + 100, W - MARGIN - 100)

    # Price + CTA
    font_price = get_font(44, bold=True)
    draw_text_centered(draw, "$7.99  •  7 Printable Pages  •  Instant Download PDF", 1480, font_price, C["gold"])

    font_star = get_font(36, bold=True)
    draw_text_centered(draw, "★★★★★  The perfect keepsake for graduates & families", 1560, font_star, C["pink"])

    font_tag = get_font(30, bold=False)
    draw_text_centered(draw, "Print at home or at your local print shop — A4 or Letter size", 1640, font_tag, C["gray"])

    img.save("01_hero.png", dpi=(DPI, DPI))
    print("✓ Saved 01_hero.png")


# ── IMAGE 2: INSIDE PAGES ────────────────────────────────────────────────────
def create_inside_pages():
    img, draw = new_image()

    draw.rectangle((0, 0, W, 14), fill=C["gold"])
    draw.rectangle((0, H - 14, W, H), fill=C["pink"])

    font_h = get_font(88, bold=True)
    draw_text_centered(draw, "BEAUTIFUL MEMORY PAGES", 28, font_h, C["dark"])

    font_sub = get_font(36, bold=False)
    draw_text_centered(draw, "Thoughtfully designed pages for every cherished memory", 132, font_sub, C["gray"])

    draw_gold_line(draw, 188, MARGIN + 100, W - MARGIN - 100)

    # 4 page previews in 2x2 grid
    pages = [
        ("About the Graduate", C["dark"],
         ["Full Name", "School & Year", "Favorite Quote", "Photo Space"]),
        ("School Memories", C["pink"],
         ["First Day Memory", "Funniest Moment", "Proudest Day", "Photo Grid"]),
        ("Achievements", C["gold"],
         ["Awards & Honors", "Clubs & Sports", "By the Numbers", "Proud Moments"]),
        ("Messages from Family", C["pink"],
         ["4 message boxes", "Name & relationship", "Writing lines", "Gold borders"]),
    ]

    card_w = 560
    card_h = 700
    gap_x = (W - MARGIN * 2 - card_w * 2) // 1
    gap_y = 40
    start_x = MARGIN + 100
    start_y = 210

    for i, (title, color, items) in enumerate(pages):
        col = i % 2
        row = i // 2
        px = start_x + col * (card_w + gap_x)
        py = start_y + row * (card_h + gap_y)
        draw_page_mockup(draw, px, py, card_w, card_h, title, color, items)

    # Bottom text
    draw_gold_line(draw, 1680, MARGIN + 100, W - MARGIN - 100)
    font_bot = get_font(36, bold=True)
    draw_text_centered(draw, "7 Pages Total  •  Print at Home  •  A4 & Letter Size Compatible", H - 100, font_bot, C["dark"])

    img.save("02_inside_pages.png", dpi=(DPI, DPI))
    print("✓ Saved 02_inside_pages.png")


# ── IMAGE 3: PERFECT FOR ──────────────────────────────────────────────────────
def create_perfect_for():
    img, draw = new_image()

    draw.rectangle((0, 0, W, 14), fill=C["pink"])
    draw.rectangle((0, H - 14, W, H), fill=C["gold"])

    font_h = get_font(100, bold=True)
    draw_text_centered(draw, "PERFECT FOR", 30, font_h, C["dark"])

    draw_gold_line(draw, 148, MARGIN + 150, W - MARGIN - 150, width=5)

    font_sub = get_font(36, bold=False)
    draw_text_centered(draw, "A meaningful gift that graduates will treasure forever", 168, font_sub, C["gray"])

    # 4 large cards
    cards = [
        ("🎓", "High School\nGraduates", "Celebrate 4 years of hard work\nand unforgettable memories", C["pink"]),
        ("🏛️", "College\nGraduates", "Honor years of dedication,\ngrowth, and achievement", C["gold"]),
        ("🎉", "Graduation\nParties", "The perfect activity — pass around\nand collect messages from guests", C["dark"]),
        ("👨‍👩‍👧", "Family\nKeepsakes", "A gift parents and graduates\nwill treasure for a lifetime", C["pink"]),
    ]

    card_w = 570
    card_h = 620
    gap = (W - MARGIN * 2 - card_w * 4) // 3
    start_x = MARGIN
    start_y = 260

    font_emoji = get_font(80, bold=False)
    font_card_title = get_font(42, bold=True)
    font_card_body = get_font(28, bold=False)

    for i, (emoji, title, desc, color) in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        cy = start_y

        # Card shadow
        draw.rounded_rectangle((cx + 6, cy + 6, cx + card_w + 6, cy + card_h + 6),
                                radius=20, fill=C["light_gray"])
        # Card
        draw.rounded_rectangle((cx, cy, cx + card_w, cy + card_h),
                                radius=20, fill=C["white"], outline=color, width=4)
        # Top color strip
        draw.rounded_rectangle((cx, cy, cx + card_w, cy + 16), radius=4, fill=color)
        draw.rectangle((cx, cy + 8, cx + card_w, cy + 16), fill=color)

        # Emoji circle
        cr = 72
        ecx = cx + card_w // 2
        ecy = cy + 120
        draw.ellipse((ecx - cr, ecy - cr, ecx + cr, ecy + cr), fill=color)
        bbox = draw.textbbox((0, 0), emoji, font=font_emoji)
        ew = bbox[2] - bbox[0]
        eh = bbox[3] - bbox[1]
        draw.text((ecx - ew // 2, ecy - eh // 2 - 4), emoji, fill=C["white"], font=font_emoji)

        # Title (2 lines)
        title_lines = title.split("\n")
        for li, tl in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), tl, font=font_card_title)
            tw = bbox[2] - bbox[0]
            draw.text((cx + (card_w - tw) // 2, cy + 212 + li * 52), tl,
                      fill=C["dark"], font=font_card_title)

        # Description
        desc_lines = desc.split("\n")
        for li, dl in enumerate(desc_lines):
            bbox = draw.textbbox((0, 0), dl, font=font_card_body)
            tw = bbox[2] - bbox[0]
            draw.text((cx + (card_w - tw) // 2, cy + 330 + li * 42), dl,
                      fill=C["gray"], font=font_card_body)

        # Bottom ribbon
        draw.rounded_rectangle((cx + card_w // 2 - 80, cy + card_h - 55,
                                 cx + card_w // 2 + 80, cy + card_h - 18),
                                radius=10, fill=color)
        font_rib = get_font(24, bold=True)
        bbox = draw.textbbox((0, 0), "Great Gift!", font=font_rib)
        tw = bbox[2] - bbox[0]
        draw.text((cx + card_w // 2 - tw // 2, cy + card_h - 50), "Great Gift!",
                  fill=C["white"], font=font_rib)

    # Bottom section
    draw_gold_line(draw, 930, MARGIN, W - MARGIN)

    font_also = get_font(44, bold=True)
    draw_text_centered(draw, "Also makes a beautiful gift for:", 960, font_also, C["dark"])

    gift_ideas = [
        "🎁 End-of-year teacher gifts",
        "🎁 Graduation party table activity",
        "🎁 Scrapbooking & memory keeping",
        "🎁 International students & gap year memories",
    ]
    font_gift = get_font(34, bold=False)
    for i, gift in enumerate(gift_ideas):
        gy = 1030 + i * 62
        bbox = draw.textbbox((0, 0), gift, font=font_gift)
        gw = bbox[2] - bbox[0]
        draw.text(((W - gw) // 2, gy), gift, fill=C["gray"], font=font_gift)

    draw_gold_line(draw, 1290, MARGIN + 100, W - MARGIN - 100)

    font_cta = get_font(38, bold=True)
    draw_text_centered(draw, "$7.99  •  7 Printable Pages  •  Print Unlimited Copies", 1320, font_cta, C["gold"])

    img.save("03_perfect_for.png", dpi=(DPI, DPI))
    print("✓ Saved 03_perfect_for.png")


if __name__ == "__main__":
    create_hero()
    create_inside_pages()
    create_perfect_for()
    print("\nAll 3 listing images created.")
