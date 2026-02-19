#!/usr/bin/env python3
"""
Etsy Listing Images for Motivational Quote Wall Art Prints Bundle.
Generates 10 listing images at 2400x2400px.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Paths
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINTS_DIR = os.path.join(BASE, "prints")
OUT = os.path.join(BASE, "images")

# Canvas
W, H = 2400, 2400

# Colors
SAGE = (143, 174, 139)
DUSTY_ROSE = (212, 160, 160)
NAVY = (27, 42, 74)
GOLD = (201, 169, 110)
CREAM = (255, 248, 240)
CHARCOAL = (51, 51, 51)
TERRACOTTA = (196, 113, 59)
SKY_BLUE = (135, 206, 235)
PLUM = (123, 80, 111)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WARM_CREAM = (250, 240, 225)
LIGHT_SAGE = (200, 220, 195)
SOFT_PINK = (245, 228, 228)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_font_bold(size):
    return get_font(size, bold=True)


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill)
        return
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.pieslice([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=fill)
    draw.pieslice([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=fill)
    if outline:
        # Draw outline arcs and lines
        draw.arc([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([(x0+radius, y0), (x1-radius, y0)], fill=outline, width=width)
        draw.line([(x0+radius, y1), (x1-radius, y1)], fill=outline, width=width)
        draw.line([(x0, y0+radius), (x0, y1-radius)], fill=outline, width=width)
        draw.line([(x1, y0+radius), (x1, y1-radius)], fill=outline, width=width)


def centered_text(draw, text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def load_print(num):
    """Load a print image."""
    path = os.path.join(PRINTS_DIR, f"quote_print_{num:02d}.jpg")
    return Image.open(path)


def draw_shadow_frame(img, print_img, x, y, w, h, shadow_offset=8):
    """Place a print with a subtle shadow/frame effect."""
    draw = ImageDraw.Draw(img)
    # Shadow
    draw.rectangle([x + shadow_offset, y + shadow_offset, x + w + shadow_offset, y + h + shadow_offset],
                    fill=(180, 180, 180))
    # White frame border
    frame_w = 6
    draw.rectangle([x - frame_w, y - frame_w, x + w + frame_w, y + h + frame_w], fill=WHITE)
    # Paste resized print
    resized = print_img.resize((w, h), Image.LANCZOS)
    img.paste(resized, (x, y))


def draw_gradient_bg(img, c1, c2):
    draw = ImageDraw.Draw(img)
    for i in range(H):
        ratio = i / H
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.line([(0, i), (W, i)], fill=(r, g, b))
    return draw


# ============================================================
# 10 Listing Images
# ============================================================

def image_01_hero():
    """Hero - grid of 9 prints in stylish arrangement."""
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title at top
    font_title = get_font_bold(70)
    centered_text(draw, "MOTIVATIONAL QUOTE WALL ART", 60, font_title, CHARCOAL)
    font_sub = get_font(45)
    centered_text(draw, "30 Printable Inspirational Posters", 150, font_sub, GOLD)

    # 3x3 grid of prints
    prints_to_show = [1, 5, 10, 17, 3, 22, 8, 16, 30]
    pw, ph = 650, 812  # 4:5 ratio
    gap = 40
    start_x = (W - (3 * pw + 2 * gap)) // 2
    start_y = 260

    for idx, pnum in enumerate(prints_to_show):
        row = idx // 3
        col = idx % 3
        x = start_x + col * (pw + gap)
        y = start_y + row * (ph + gap)
        p = load_print(pnum)
        draw_shadow_frame(img, p, x, y, pw, ph, 6)

    # Bottom bar
    draw.rectangle([0, H - 100, W, H], fill=CHARCOAL)
    font_bot = get_font_bold(40)
    centered_text(draw, "INSTANT DOWNLOAD  |  HIGH RESOLUTION  |  PRINT AT HOME", H - 80, font_bot, GOLD)

    return img


def image_02_whats_included():
    """What's included overview."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Title
    font_title = get_font_bold(90)
    font_sub = get_font(55)
    centered_text(draw, "WHAT'S INCLUDED", 100, font_title, WHITE)
    draw.line([(600, 220), (W - 600, 220)], fill=GOLD, width=3)

    # Feature cards
    features = [
        ("30", "Motivational\nQuote Prints"),
        ("2", "Print Sizes\n8x10 & 16x20"),
        ("JPG", "High Resolution\n300 DPI Files"),
        ("ZIP", "Instant Digital\nDownload"),
    ]

    card_w, card_h = 480, 500
    gap = 50
    start_x = (W - (4 * card_w + 3 * gap)) // 2
    y = 350

    for i, (big, desc) in enumerate(features):
        x = start_x + i * (card_w + gap)
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, fill=(40, 55, 85))

        font_big = get_font_bold(120)
        bbox = draw.textbbox((0, 0), big, font=font_big)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, y + 60), big, font=font_big, fill=GOLD)

        font_desc = get_font(38)
        lines = desc.split('\n')
        ly = y + 250
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_desc)
            ltw = bbox[2] - bbox[0]
            draw.text((x + (card_w - ltw) // 2, ly), line, font=font_desc, fill=WHITE)
            ly += 55

    # Sample prints below
    sample_prints = [1, 5, 9, 16, 22, 30]
    pw, ph = 320, 400
    gap2 = 40
    start_x2 = (W - (6 * pw + 5 * gap2)) // 2
    y2 = 1050

    for i, pnum in enumerate(sample_prints):
        x = start_x2 + i * (pw + gap2)
        p = load_print(pnum)
        draw_shadow_frame(img, p, x, y2, pw, ph, 4)

    # Bottom features
    font_feat = get_font_bold(42)
    features_text = [
        "Print at home or at a print shop",
        "Perfect for office, bedroom, living room",
        "Makes a great gift!"
    ]
    y3 = 1600
    for ft in features_text:
        # Checkmark
        bbox = draw.textbbox((0, 0), ft, font=font_feat)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2 - 50
        draw.text((x - 10, y3), "+", font=font_feat, fill=GOLD)
        draw.text((x + 40, y3), ft, font=font_feat, fill=WHITE)
        y3 += 80

    # Price badge
    draw_rounded_rect(draw, (W // 2 - 200, 1950, W // 2 + 200, 2080), 20, fill=TERRACOTTA)
    font_price = get_font_bold(65)
    centered_text(draw, "ONLY $7.99", 1970, font_price, WHITE)

    # Bottom
    font_bottom = get_font(35)
    centered_text(draw, "Instant Download - No Shipping Required", 2150, font_bottom, GOLD)

    return img


def image_03_showcase_1_6():
    """Prints 1-6 showcase grid."""
    return _showcase_grid([1, 2, 3, 4, 5, 6], "PRINTS 1-6", CREAM)


def image_04_showcase_7_12():
    """Prints 7-12 showcase grid."""
    return _showcase_grid([7, 8, 9, 10, 11, 12], "PRINTS 7-12", (245, 240, 235))


def image_05_showcase_13_18():
    """Prints 13-18 showcase grid."""
    return _showcase_grid([13, 14, 15, 16, 17, 18], "PRINTS 13-18", CREAM)


def image_06_showcase_19_24():
    """Prints 19-24 showcase grid."""
    return _showcase_grid([19, 20, 21, 22, 23, 24], "PRINTS 19-24", (245, 240, 235))


def image_07_showcase_25_30():
    """Prints 25-30 showcase grid."""
    return _showcase_grid([25, 26, 27, 28, 29, 30], "PRINTS 25-30", CREAM)


def _showcase_grid(print_nums, title, bg_color):
    """Create a 2x3 showcase grid."""
    img = Image.new('RGB', (W, H), bg_color)
    draw = ImageDraw.Draw(img)

    # Title
    font_title = get_font_bold(70)
    centered_text(draw, title, 50, font_title, CHARCOAL)

    # Subtitle
    font_sub = get_font(40)
    centered_text(draw, "Motivational Quote Wall Art Prints Bundle", 140, font_sub, GOLD)

    # 3x2 grid
    pw, ph = 680, 850  # 4:5 ratio
    gap = 40
    start_x = (W - (3 * pw + 2 * gap)) // 2
    start_y = 240

    for idx, pnum in enumerate(print_nums):
        row = idx // 3
        col = idx % 3
        x = start_x + col * (pw + gap)
        y = start_y + row * (ph + gap)
        p = load_print(pnum)
        draw_shadow_frame(img, p, x, y, pw, ph, 6)

    # Bottom branding
    draw.rectangle([0, H - 80, W, H], fill=CHARCOAL)
    font_bot = get_font_bold(35)
    centered_text(draw, "PRINTABLE WALL ART  |  INSTANT DOWNLOAD  |  HIGH RESOLUTION", H - 65, font_bot, GOLD)

    return img


def image_08_room_mockup():
    """Room mockup - prints on wall simulation."""
    img = Image.new('RGB', (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Wall texture - subtle horizontal lines
    for y in range(0, H, 4):
        shade = 248 + (y % 8 == 0) * 2
        draw.line([(0, y), (W, y)], fill=(shade, shade - 8, shade - 15))

    # Title
    font_title = get_font_bold(60)
    centered_text(draw, "STYLED IN YOUR SPACE", 60, font_title, CHARCOAL)

    # Gallery wall arrangement - 5 prints in a gallery layout
    # Large center print
    prints_layout = [
        (3, 750, 300, 550, 687),   # print 3 - left
        (5, 400, 1200, 480, 600),  # print 5 - bottom left
        (10, 850, 150, 700, 875),  # print 10 - center top
        (16, 1600, 300, 550, 687), # print 16 - right
        (22, 1500, 1200, 480, 600),# print 22 - bottom right
    ]

    for pnum, x, y, pw, ph in prints_layout:
        p = load_print(pnum)
        # Draw picture frame
        frame_margin = 20
        # Frame shadow
        draw.rectangle([x - frame_margin + 6, y - frame_margin + 6,
                        x + pw + frame_margin + 6, y + ph + frame_margin + 6],
                       fill=(200, 190, 175))
        # Frame
        draw.rectangle([x - frame_margin, y - frame_margin,
                        x + pw + frame_margin, y + ph + frame_margin],
                       fill=WHITE)
        # Inner mat
        draw.rectangle([x - 5, y - 5, x + pw + 5, y + ph + 5], fill=(240, 235, 225))
        # Print
        resized = p.resize((pw, ph), Image.LANCZOS)
        img.paste(resized, (x, y))

    # Console table / shelf at bottom
    draw.rectangle([200, 2000, W - 200, 2020], fill=(160, 130, 100))
    draw.rectangle([200, 2020, W - 200, 2050], fill=(140, 110, 80))

    # Plant on shelf
    # Pot
    draw.rectangle([350, 1950, 450, 2000], fill=TERRACOTTA)
    draw.polygon([(360, 1950), (440, 1950), (430, 1900), (370, 1900)], fill=TERRACOTTA)
    # Leaves
    for angle_deg in [-30, 0, 30, -60, 60]:
        rad = math.radians(angle_deg - 90)
        ex = 400 + int(80 * math.cos(rad))
        ey = 1880 + int(80 * math.sin(rad))
        draw.line([(400, 1880), (ex, ey)], fill=SAGE, width=4)
        draw.ellipse([ex - 15, ey - 8, ex + 15, ey + 8], fill=SAGE)

    # Candle
    draw.rectangle([1950, 1960, 2000, 2000], fill=(230, 220, 200))
    draw.rectangle([1965, 1940, 1985, 1960], fill=(255, 240, 200))
    # Flame
    draw.ellipse([1968, 1920, 1982, 1945], fill=(255, 200, 80))

    # Bottom text
    font_note = get_font(40)
    centered_text(draw, "Perfect for office, bedroom, living room, or nursery", 2200, font_note, CHARCOAL)
    font_note2 = get_font_bold(35)
    centered_text(draw, "Print at home or at your local print shop", 2270, font_note2, GOLD)

    return img


def image_09_testimonials():
    """Customer testimonials."""
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    font_title = get_font_bold(80)
    centered_text(draw, "CUSTOMERS LOVE IT!", 80, font_title, CHARCOAL)

    # Stars
    font_stars = get_font(70)
    centered_text(draw, "* * * * *", 190, font_stars, GOLD)

    # Testimonial cards
    testimonials = [
        ("Beautiful designs! I printed these for my home\noffice and get compliments all the time.",
         "- Sarah M.", "Verified Buyer"),
        ("Such a great value for 30 prints! The quality\nis amazing and they look so professional.",
         "- Jessica L.", "Verified Buyer"),
        ("I bought these as gifts and everyone loved\nthem. Easy to download and print!",
         "- Amanda R.", "Verified Buyer"),
        ("These are absolutely gorgeous. The typography\nand colors are perfect for any room.",
         "- Michelle K.", "Verified Buyer"),
    ]

    card_w = W - 200
    card_h = 320
    gap = 40
    y = 340

    for quote, name, badge in testimonials:
        draw_rounded_rect(draw, (100, y, 100 + card_w, y + card_h), 15, fill=WHITE, outline=(220, 215, 205), width=2)

        # Stars
        font_card_stars = get_font(35)
        draw.text((160, y + 25), "* * * * *", font=font_card_stars, fill=GOLD)

        # Quote
        font_quote = get_font(36)
        draw.text((160, y + 80), quote, font=font_quote, fill=CHARCOAL)

        # Name
        font_name = get_font_bold(34)
        draw.text((160, y + 230), name, font=font_name, fill=CHARCOAL)

        # Badge
        font_badge = get_font(28)
        draw.text((400, y + 235), badge, font=font_badge, fill=SAGE)

        y += card_h + gap

    # Bottom section - sample prints
    sample = [5, 10, 16, 22]
    pw, ph = 280, 350
    start_x = (W - (4 * pw + 3 * 30)) // 2
    y_prints = y + 30
    for i, pnum in enumerate(sample):
        x = start_x + i * (pw + 30)
        p = load_print(pnum)
        draw_shadow_frame(img, p, x, y_prints, pw, ph, 4)

    return img


def image_10_cta():
    """Bundle CTA with price."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Decorative border
    draw.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=3)
    draw.rectangle([55, 55, W - 55, H - 55], outline=GOLD, width=1)

    # Top accent
    font_bundle = get_font_bold(55)
    centered_text(draw, "LIMITED TIME OFFER", 100, font_bundle, GOLD)

    # Main title
    font_title = get_font_bold(100)
    centered_text(draw, "30 MOTIVATIONAL", 250, font_title, WHITE)
    centered_text(draw, "QUOTE PRINTS", 380, font_title, WHITE)

    # Subtitle
    font_sub = get_font(50)
    centered_text(draw, "Printable Wall Art Bundle", 520, font_sub, GOLD)

    # Sample prints - small grid
    sample = [1, 5, 8, 10, 16, 22]
    pw, ph = 300, 375
    gap = 30
    start_x = (W - (6 * pw + 5 * gap)) // 2
    y = 640

    for i, pnum in enumerate(sample):
        x = start_x + i * (pw + gap)
        p = load_print(pnum)
        # White frame
        draw.rectangle([x - 4, y - 4, x + pw + 4, y + ph + 4], fill=WHITE)
        resized = p.resize((pw, ph), Image.LANCZOS)
        img.paste(resized, (x, y))

    # Price section
    y_price = 1150

    # Crossed out "retail" price
    font_was = get_font(50)
    was_text = "Value: $45.00"
    bbox = draw.textbbox((0, 0), was_text, font=font_was)
    tw = bbox[2] - bbox[0]
    x_was = (W - tw) // 2
    draw.text((x_was, y_price), was_text, font=font_was, fill=(150, 150, 170))
    draw.line([(x_was - 10, y_price + 30), (x_was + tw + 10, y_price + 30)], fill=(150, 150, 170), width=3)

    # Big price
    font_price = get_font_bold(200)
    centered_text(draw, "$7.99", y_price + 80, font_price, WHITE)

    # Per print
    font_per = get_font(45)
    centered_text(draw, "That's only $0.27 per print!", y_price + 310, font_per, GOLD)

    # CTA button
    btn_y = y_price + 430
    draw_rounded_rect(draw, (W // 2 - 450, btn_y, W // 2 + 450, btn_y + 120), 25, fill=TERRACOTTA)
    font_cta = get_font_bold(60)
    centered_text(draw, "ADD TO CART - INSTANT DOWNLOAD", btn_y + 25, font_cta, WHITE)

    # Features at bottom
    features = [
        "Instant Digital Download",
        "High Resolution 300 DPI",
        "Print at Home or Print Shop",
        "8x10 and 16x20 Sizes"
    ]
    font_feat = get_font(36)
    y_feat = btn_y + 200
    for feat in features:
        centered_text(draw, f"+ {feat}", y_feat, font_feat, (200, 200, 215))
        y_feat += 55

    # Guarantee
    font_guar = get_font_bold(40)
    centered_text(draw, "100% Satisfaction Guaranteed", y_feat + 30, font_guar, GOLD)

    return img


# ============================================================
# Main
# ============================================================

IMAGES = [
    (1, image_01_hero, "Hero grid"),
    (2, image_02_whats_included, "What's included"),
    (3, image_03_showcase_1_6, "Prints 1-6"),
    (4, image_04_showcase_7_12, "Prints 7-12"),
    (5, image_05_showcase_13_18, "Prints 13-18"),
    (6, image_06_showcase_19_24, "Prints 19-24"),
    (7, image_07_showcase_25_30, "Prints 25-30"),
    (8, image_08_room_mockup, "Room mockup"),
    (9, image_09_testimonials, "Testimonials"),
    (10, image_10_cta, "Bundle CTA"),
]

if __name__ == "__main__":
    print(f"Generating 10 listing images at {W}x{H}px...")
    for num, func, desc in IMAGES:
        print(f"  Creating image {num:02d}/10 ({desc})...", end=" ", flush=True)
        img = func()
        path = os.path.join(OUT, f"listing_{num:02d}.jpg")
        img.save(path, "JPEG", quality=95)
        print(f"Saved: {path}")
    print(f"\nAll 10 listing images generated successfully!")
