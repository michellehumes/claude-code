#!/usr/bin/env python3
"""
Minimalist Wedding Invitation Suite - Listing Image Generator
Generates 10 Etsy listing images at 2400x2400px.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Directories ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
os.makedirs(BASE_DIR, exist_ok=True)

W, H = 2400, 2400

# ── Color Palette ────────────────────────────────────────────────────────────
SAGE = (143, 174, 139)
IVORY = (255, 255, 240)
GOLD = (197, 165, 90)
CHARCOAL = (45, 45, 45)
BLUSH = (245, 230, 224)
WHITE = (255, 255, 255)
DARK_SAGE = (100, 140, 95)
LIGHT_SAGE = (220, 235, 218)
GOLD_LIGHT = (230, 215, 170)
CREAM = (250, 248, 240)
SOFT_GRAY = (245, 245, 242)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_serif(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


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
        draw.line([(x0 + radius, y0), (x1 - radius, y0)], fill=outline, width=width)
        draw.line([(x0 + radius, y1), (x1 - radius, y1)], fill=outline, width=width)
        draw.line([(x0, y0 + radius), (x0, y1 - radius)], fill=outline, width=width)
        draw.line([(x1, y0 + radius), (x1, y1 - radius)], fill=outline, width=width)


def draw_text_centered(draw, text, y, font, fill, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def draw_text_at(draw, text, x, y, font, fill):
    draw.text((x, y), text, font=font, fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_shadow_rect(draw, xy, radius, fill, shadow_offset=8, shadow_color=(0, 0, 0, 30)):
    """Draw a rect with subtle shadow effect (approximated darker bg)."""
    x0, y0, x1, y1 = xy
    # Shadow (slightly offset, slightly darker)
    sc = tuple(max(0, c - 20) for c in fill[:3])
    draw_rounded_rect(draw, (x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset),
                       radius, sc)
    draw_rounded_rect(draw, xy, radius, fill)


def load_template(name):
    """Load a template image from the templates directory."""
    path = os.path.join(TEMPLATE_DIR, name)
    if os.path.exists(path):
        return Image.open(path)
    return None


def place_card_mockup(canvas, template_name, x, y, target_w, target_h, rotation=0, shadow=True):
    """Load template, resize, optionally rotate, and paste onto canvas."""
    img = load_template(template_name)
    if img is None:
        # Draw placeholder
        draw = ImageDraw.Draw(canvas)
        draw_rounded_rect(draw, (x, y, x + target_w, y + target_h), 10, WHITE, outline=GOLD, width=2)
        return

    img = img.resize((target_w, target_h), Image.LANCZOS)

    if rotation != 0:
        img = img.rotate(rotation, expand=True, fillcolor=(0, 0, 0, 0))

    if shadow:
        draw = ImageDraw.Draw(canvas)
        sx, sy = x + 6, y + 6
        draw_rounded_rect(draw, (sx, sy, sx + img.width, sy + img.height), 5, (200, 200, 195))

    canvas.paste(img, (x, y))


def draw_branch_simple(draw, x, y, direction, length, color, thickness=2):
    """Draw a simple botanical branch."""
    sign = 1 if direction == 'right' else -1
    points = []
    segments = 10
    for i in range(segments + 1):
        t = i / segments
        px = x + sign * t * length
        py = y + math.sin(t * math.pi) * (-length * 0.06)
        points.append((px, py))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=thickness)
    # Leaves
    for t in [0.2, 0.4, 0.6, 0.8]:
        idx = int(t * segments)
        if idx < len(points):
            px, py = points[idx]
            for side in [1, -1]:
                la = math.radians(-45 * side + (0 if sign == 1 else 180))
                lx = px + 12 * math.cos(la)
                ly = py + 12 * math.sin(la)
                draw.line([(px, py), (lx, ly)], fill=color, width=1)


def draw_gold_divider(draw, y, w, length=500):
    cx = w // 2
    draw.line([(cx - length // 2, y), (cx + length // 2, y)], fill=GOLD, width=2)
    r = 4
    draw.ellipse([cx - r, y - r, cx + r, y + r], fill=GOLD)


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 1: Hero - Flat-lay mockup of full suite
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_01():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Subtle textured background
    for i in range(0, W, 4):
        for j in range(0, H, 4):
            noise = ((i * 7 + j * 13) % 5) - 2
            r, g, b = CREAM
            img.putpixel((i, j), (r + noise, g + noise, b + noise))

    # Title at top
    f_title = get_serif(60, bold=True)
    f_sub = get_serif(34)
    draw_text_centered(draw, "Minimalist Wedding", 60, f_title, CHARCOAL, W)
    draw_text_centered(draw, "Invitation Suite", 135, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 210, W, 400)
    draw_text_centered(draw, "Complete Printable Stationery Set", 230, f_sub, SAGE, W)

    # Arrange templates in elegant flat-lay
    # Main invitation centered
    place_card_mockup(img, "invitation_sage.png", 800, 300, 500, 700)
    # Save the date - left
    place_card_mockup(img, "save_the_date_sage.png", 200, 350, 480, 672)
    # RSVP card
    place_card_mockup(img, "rsvp_sage.png", 250, 1100, 500, 350)
    # Details card
    place_card_mockup(img, "details_sage.png", 820, 1080, 500, 350)
    # Thank you
    place_card_mockup(img, "thank_you_sage.png", 1400, 300, 440, 616)
    # Menu
    place_card_mockup(img, "menu_sage.png", 1500, 1000, 340, 765)
    # Table number
    place_card_mockup(img, "table_number_01_sage.png", 1400, 1800, 320, 480)
    # Place card
    place_card_mockup(img, "place_card_sage.png", 300, 1550, 380, 217)

    # Bottom branding
    draw_rounded_rect(draw, (700, 2180, 1700, 2320), 20, SAGE)
    f_brand = get_font(36, bold=True)
    f_price = get_font(28)
    draw_text_centered(draw, "8 Piece Complete Suite", 2200, f_brand, WHITE, W)
    draw_text_centered(draw, "Instant Download  |  Editable  |  Print at Home", 2250, f_price, (230, 245, 228), W)

    # Botanical accents
    draw_branch_simple(draw, 50, 2350, 'right', 180, SAGE, 2)
    draw_branch_simple(draw, W - 50, 2350, 'left', 180, SAGE, 2)

    img.save(os.path.join(BASE_DIR, "listing_01_hero.jpg"), "JPEG", quality=95)
    print("  Created: listing_01_hero.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 2: What's Included
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_02():
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(64, bold=True)
    f_sub = get_serif(36)
    f_item = get_serif(34)
    f_detail = get_font(26)
    f_count = get_font(28, bold=True)

    draw_text_centered(draw, "What's Included", 80, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 160, W, 500)
    draw_text_centered(draw, "Your Complete Wedding Stationery Suite", 185, f_sub, SAGE, W)

    items = [
        ("Wedding Invitation", "5 x 7 inches", "3 color variants"),
        ("RSVP Card", "5 x 3.5 inches", "3 color variants"),
        ("Save the Date", "5 x 7 inches", "3 color variants"),
        ("Details / Info Card", "5 x 3.5 inches", "3 color variants"),
        ("Thank You Card", "5 x 7 inches", "3 color variants"),
        ("Menu Card", "4 x 9 inches", "3 color variants"),
        ("Table Number Cards", "4 x 6 inches", "Numbers 1-20"),
        ("Place Cards", "3.5 x 2 inches", "3 color variants"),
    ]

    y_start = 300
    for idx, (name, size, detail) in enumerate(items):
        y = y_start + idx * 240
        # Number circle
        cx, cy = 200, y + 50
        draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=SAGE)
        num_font = get_font(32, bold=True)
        draw_text_centered(draw, str(idx + 1), cy - 18, num_font, WHITE, cx * 2)

        # Item info
        draw_text_at(draw, name, 300, y + 15, f_item, CHARCOAL)
        draw_text_at(draw, f"{size}  |  {detail}", 300, y + 60, f_detail, (130, 130, 130))

        # Gold line separator
        if idx < len(items) - 1:
            draw.line([(300, y + 110), (2100, y + 110)], fill=GOLD_LIGHT, width=1)

    # Summary box at bottom
    draw_rounded_rect(draw, (300, 2180, 2100, 2320), 20, SAGE)
    f_summary = get_font(34, bold=True)
    draw_text_centered(draw, "81+ Printable Files  |  3 Color Palettes  |  Instant Download", 2220, f_summary, WHITE, W)

    # Thin gold border
    draw.rectangle([30, 30, W - 30, H - 30], outline=GOLD, width=2)

    img.save(os.path.join(BASE_DIR, "listing_02_whats_included.jpg"), "JPEG", quality=95)
    print("  Created: listing_02_whats_included.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 3: Invitation close-up with 3 color variants
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_03():
    img = Image.new("RGB", (W, H), SOFT_GRAY)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_sub = get_serif(32)

    draw_text_centered(draw, "Wedding Invitation", 60, f_title, CHARCOAL, W)
    draw_text_centered(draw, "Available in 3 Elegant Color Palettes", 130, f_sub, SAGE, W)
    draw_gold_divider(draw, 180, W, 400)

    # Three invitation variants side by side
    variants = ["sage", "blush", "classic"]
    labels = ["Sage & Gold", "Blush & Gold", "Classic Gold"]
    card_w, card_h = 620, 868
    spacing = 60
    total_w = 3 * card_w + 2 * spacing
    start_x = (W - total_w) // 2

    f_label = get_serif(30, bold=True)

    for i, (vname, label) in enumerate(zip(variants, labels)):
        x = start_x + i * (card_w + spacing)
        y = 240
        place_card_mockup(img, f"invitation_{vname}.png", x, y, card_w, card_h)
        # Label below
        label_w = draw.textbbox((0, 0), label, font=f_label)[2]
        label_x = x + (card_w - label_w) // 2
        draw.text((label_x, y + card_h + 20), label, font=f_label, fill=CHARCOAL)

    # Bottom info
    y_bottom = 1250
    draw_text_centered(draw, "5 x 7 inches  |  300 DPI  |  Print Ready", y_bottom, f_sub, (130, 130, 130), W)

    # Show close-up detail of sage variant below
    invitation = load_template("invitation_sage.png")
    if invitation:
        # Crop a detail section
        detail = invitation.crop((200, 300, 1300, 900))
        detail = detail.resize((1200, 654), Image.LANCZOS)
        x_detail = (W - 1200) // 2
        y_detail = 1350
        draw_rounded_rect(draw, (x_detail - 5, y_detail - 5, x_detail + 1205, y_detail + 659), 15, WHITE)
        img.paste(detail, (x_detail, y_detail))
        # Border
        draw.rectangle([x_detail - 2, y_detail - 2, x_detail + 1202, y_detail + 656], outline=GOLD, width=2)

    draw_text_centered(draw, "Elegant Detail Close-up", 2060, f_sub, CHARCOAL, W)

    # Bottom accent
    draw_branch_simple(draw, 100, H - 80, 'right', 200, SAGE, 2)
    draw_branch_simple(draw, W - 100, H - 80, 'left', 200, SAGE, 2)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_03_invitation_variants.jpg"), "JPEG", quality=95)
    print("  Created: listing_03_invitation_variants.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 4: RSVP + Details cards showcase
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_04():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_sub = get_serif(32)

    draw_text_centered(draw, "RSVP & Details Cards", 80, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 155, W, 450)
    draw_text_centered(draw, "Matching stationery for every wedding need", 180, f_sub, SAGE, W)

    # RSVP cards
    draw_text_centered(draw, "RSVP Cards", 280, get_serif(40, bold=True), CHARCOAL, W)
    variants = ["sage", "blush", "classic"]
    card_w, card_h = 600, 420
    spacing = 50
    total = 3 * card_w + 2 * spacing
    sx = (W - total) // 2
    for i, v in enumerate(variants):
        x = sx + i * (card_w + spacing)
        place_card_mockup(img, f"rsvp_{v}.png", x, 340, card_w, card_h)

    # Details cards
    draw_text_centered(draw, "Details / Info Cards", 860, get_serif(40, bold=True), CHARCOAL, W)
    for i, v in enumerate(variants):
        x = sx + i * (card_w + spacing)
        place_card_mockup(img, f"details_{v}.png", x, 920, card_w, card_h)

    # Info area
    y_info = 1450
    draw_rounded_rect(draw, (200, y_info, W - 200, y_info + 200), 20, LIGHT_SAGE)
    f_info = get_font(30)
    draw_text_centered(draw, "Both cards: 5 x 3.5 inches | Perfect for enclosure in invitation envelope",
                       y_info + 40, f_info, CHARCOAL, W)
    draw_text_centered(draw, "Includes meal preference, dietary restrictions, and venue details",
                       y_info + 90, f_info, DARK_SAGE, W)

    # Show place cards at bottom
    draw_text_centered(draw, "Place Cards", 1750, get_serif(40, bold=True), CHARCOAL, W)
    pc_w, pc_h = 420, 240
    pc_spacing = 80
    pc_total = 3 * pc_w + 2 * pc_spacing
    pc_sx = (W - pc_total) // 2
    for i, v in enumerate(variants):
        x = pc_sx + i * (pc_w + pc_spacing)
        place_card_mockup(img, f"place_card_{v}.png", x, 1820, pc_w, pc_h)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_04_rsvp_details.jpg"), "JPEG", quality=95)
    print("  Created: listing_04_rsvp_details.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 5: Save the Date + Thank You showcase
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_05():
    img = Image.new("RGB", (W, H), BLUSH)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_sub = get_serif(32)

    draw_text_centered(draw, "Save the Date & Thank You", 70, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 145, W, 500)

    # Save the Dates - top row
    draw_text_centered(draw, "Save the Date  |  5 x 7 inches", 190, f_sub, (130, 100, 95), W)

    variants = ["sage", "blush", "classic"]
    card_w, card_h = 500, 700
    spacing = 60
    total = 3 * card_w + 2 * spacing
    sx = (W - total) // 2

    for i, v in enumerate(variants):
        x = sx + i * (card_w + spacing)
        place_card_mockup(img, f"save_the_date_{v}.png", x, 250, card_w, card_h)

    # Thank You cards - bottom row
    draw_text_centered(draw, "Thank You Cards  |  5 x 7 inches", 1020, f_sub, (130, 100, 95), W)

    for i, v in enumerate(variants):
        x = sx + i * (card_w + spacing)
        place_card_mockup(img, f"thank_you_{v}.png", x, 1080, card_w, card_h)

    # Bottom note
    draw_rounded_rect(draw, (400, 1850, 2000, 1970), 15, WHITE)
    f_note = get_font(28)
    draw_text_centered(draw, "Send before the wedding & after - we've got you covered!", 1885, f_note, CHARCOAL, W)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_05_save_date_thank_you.jpg"), "JPEG", quality=95)
    print("  Created: listing_05_save_date_thank_you.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 6: Menu + Table Numbers showcase
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_06():
    img = Image.new("RGB", (W, H), SOFT_GRAY)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_sub = get_serif(32)
    f_label = get_serif(28)

    draw_text_centered(draw, "Menu & Table Numbers", 60, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 135, W, 450)

    # Menu cards - left side
    draw_text_centered(draw, "Menu Cards  |  4 x 9 inches", 170, f_sub, SAGE, W)

    menu_w, menu_h = 350, 788
    menu_spacing = 40
    menu_total = 3 * menu_w + 2 * menu_spacing
    menu_sx = (W - menu_total) // 2

    variants = ["sage", "blush", "classic"]
    labels = ["Sage", "Blush", "Classic"]

    for i, (v, label) in enumerate(zip(variants, labels)):
        x = menu_sx + i * (menu_w + menu_spacing)
        place_card_mockup(img, f"menu_{v}.png", x, 230, menu_w, menu_h)
        lw = draw.textbbox((0, 0), label, font=f_label)[2]
        draw.text((x + (menu_w - lw) // 2, 230 + menu_h + 10), label, font=f_label, fill=CHARCOAL)

    # Table numbers - bottom section
    y_table = 1150
    draw_text_centered(draw, "Table Number Cards  |  4 x 6 inches  |  Numbers 1-20", y_table, f_sub, SAGE, W)
    y_table += 60

    tn_w, tn_h = 210, 315
    tn_spacing = 20
    # Show numbers 1-8 in a row
    tn_total = 8 * tn_w + 7 * tn_spacing
    tn_sx = (W - tn_total) // 2

    for i in range(8):
        num = i + 1
        x = tn_sx + i * (tn_w + tn_spacing)
        place_card_mockup(img, f"table_number_{num:02d}_sage.png", x, y_table, tn_w, tn_h)

    # Second row 9-16
    y_table2 = y_table + tn_h + 30
    for i in range(8):
        num = i + 9
        x = tn_sx + i * (tn_w + tn_spacing)
        place_card_mockup(img, f"table_number_{num:02d}_sage.png", x, y_table2, tn_w, tn_h)

    # Info
    draw_rounded_rect(draw, (300, 2170, 2100, 2310), 20, SAGE)
    f_info = get_font(30, bold=True)
    draw_text_centered(draw, "20 Table Numbers + 3 Menu Variants = Complete Reception Set", 2210, f_info, WHITE, W)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_06_menu_table_numbers.jpg"), "JPEG", quality=95)
    print("  Created: listing_06_menu_table_numbers.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 7: Color palette / 3 variants comparison
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_07():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_sub = get_serif(32)
    f_name = get_serif(36, bold=True)
    f_detail = get_font(26)

    draw_text_centered(draw, "3 Beautiful Color Palettes", 70, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 145, W, 500)
    draw_text_centered(draw, "Choose the palette that matches your wedding aesthetic", 170, f_sub, (130, 130, 130), W)

    palettes = [
        ("Sage & Gold", [SAGE, IVORY, GOLD, CHARCOAL, BLUSH],
         ["Sage Green", "Ivory", "Gold", "Charcoal", "Blush"],
         "sage"),
        ("Blush & Gold", [(210, 170, 160), (252, 248, 245), GOLD, CHARCOAL, BLUSH],
         ["Rose", "Cream", "Gold", "Charcoal", "Blush"],
         "blush"),
        ("Classic Gold", [CHARCOAL, WHITE, GOLD, (120, 120, 120), (245, 245, 240)],
         ["Charcoal", "White", "Gold", "Gray", "Ivory"],
         "classic"),
    ]

    y_start = 280
    for p_idx, (name, colors, color_names, variant) in enumerate(palettes):
        y = y_start + p_idx * 700
        # Palette name
        draw_text_centered(draw, name, y, f_name, CHARCOAL, W)
        y += 55

        # Color swatches
        swatch_size = 80
        swatch_spacing = 30
        total_sw = len(colors) * swatch_size + (len(colors) - 1) * swatch_spacing
        sw_x = 200

        for c_idx, (color, cname) in enumerate(zip(colors, color_names)):
            cx = sw_x + c_idx * (swatch_size + swatch_spacing)
            draw.ellipse([cx, y, cx + swatch_size, y + swatch_size], fill=color, outline=GOLD, width=2)
            # Color name below
            cw = draw.textbbox((0, 0), cname, font=f_detail)[2]
            draw.text((cx + (swatch_size - cw) // 2, y + swatch_size + 8), cname, font=f_detail, fill=(100, 100, 100))

        # Invitation preview on the right
        preview_w, preview_h = 400, 560
        place_card_mockup(img, f"invitation_{variant}.png", W - 200 - preview_w, y - 30, preview_w, preview_h)

        # Separator
        if p_idx < 2:
            sep_y = y + 160 + preview_h // 2 - 140
            draw.line([(100, sep_y), (W - 100, sep_y)], fill=GOLD_LIGHT, width=1)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_07_color_palettes.jpg"), "JPEG", quality=95)
    print("  Created: listing_07_color_palettes.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 8: Print guide / How to use
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_08():
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_step_num = get_font(48, bold=True)
    f_step_title = get_serif(36, bold=True)
    f_step_desc = get_font(28)
    f_sub = get_serif(32)

    draw_text_centered(draw, "How to Use Your Templates", 70, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 145, W, 500)
    draw_text_centered(draw, "Print beautiful stationery in 4 easy steps", 170, f_sub, SAGE, W)

    steps = [
        ("1", "Download & Open",
         "Download your files instantly after purchase.",
         "Open the PNG files in any image viewer or editor."),
        ("2", "Customize Text",
         "Edit text using any image editor (Canva, Photoshop,",
         "or even Microsoft Word). Replace placeholder text."),
        ("3", "Print at Home or Send to Print Shop",
         "Print on quality cardstock at home (recommended:",
         "110 lb cardstock) or send to your local print shop."),
        ("4", "Trim & Celebrate!",
         "Cut along the edges with a paper trimmer",
         "for perfectly clean, professional results."),
    ]

    y = 290
    for num, title, line1, line2 in steps:
        # Step number circle
        cx = 200
        draw.ellipse([cx - 45, y - 5, cx + 45, y + 85], fill=SAGE)
        nw = draw.textbbox((0, 0), num, font=f_step_num)[2]
        draw.text((cx - nw // 2, y + 10), num, font=f_step_num, fill=WHITE)

        # Text
        draw.text((320, y + 5), title, font=f_step_title, fill=CHARCOAL)
        draw.text((320, y + 55), line1, font=f_step_desc, fill=(100, 100, 100))
        draw.text((320, y + 90), line2, font=f_step_desc, fill=(100, 100, 100))

        # Connecting line
        if num != "4":
            draw.line([(cx, y + 90), (cx, y + 155)], fill=GOLD, width=2)

        y += 170

    # Recommended paper types
    y += 30
    draw_rounded_rect(draw, (150, y, W - 150, y + 350), 20, LIGHT_SAGE)
    f_rec = get_serif(34, bold=True)
    f_rec_detail = get_font(26)

    draw_text_centered(draw, "Recommended Printing Specs", y + 25, f_rec, CHARCOAL, W)
    draw_gold_divider(draw, y + 70, W, 400)

    specs = [
        "Paper: 110 lb / 300 gsm Cardstock (Matte or Satin)",
        "Resolution: 300 DPI (Print-Ready)",
        "Color: CMYK recommended for professional printing",
        "Trim: Use a paper trimmer for clean edges",
    ]
    for i, spec in enumerate(specs):
        draw_text_centered(draw, spec, y + 100 + i * 45, f_rec_detail, CHARCOAL, W)

    # File formats
    y_format = y + 400
    draw_text_centered(draw, "File Format: High-Resolution PNG (300 DPI)", y_format, f_sub, SAGE, W)
    y_format += 50
    draw_text_centered(draw, "Compatible with: Canva, Photoshop, Word, Preview, and more",
                       y_format, f_rec_detail, (100, 100, 100), W)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_08_print_guide.jpg"), "JPEG", quality=95)
    print("  Created: listing_08_print_guide.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 9: Testimonials / Reviews
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_09():
    img = Image.new("RGB", (W, H), BLUSH)
    draw = ImageDraw.Draw(img)

    f_title = get_serif(56, bold=True)
    f_sub = get_serif(32)
    f_review = get_serif(30)
    f_author = get_font(26, bold=True)
    f_stars = get_font(36)

    draw_text_centered(draw, "What Our Customers Say", 80, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 155, W, 450)

    reviews = [
        {
            "stars": 5,
            "text": "\"Absolutely gorgeous! The sage and gold palette was perfect\nfor our spring garden wedding. So easy to customize!\"",
            "author": "- Sarah M.",
            "detail": "Verified Purchase"
        },
        {
            "stars": 5,
            "text": "\"Saved us SO much money! We printed everything at home\nand guests thought we hired a professional designer.\"",
            "author": "- Emily & James",
            "detail": "Verified Purchase"
        },
        {
            "stars": 5,
            "text": "\"The quality is incredible - 300 DPI prints look amazing.\nThe table numbers and menu cards were the perfect touch.\"",
            "author": "- Rachel T.",
            "detail": "Verified Purchase"
        },
        {
            "stars": 5,
            "text": "\"I love that there are 3 color options! We mixed the sage\nand blush variants for a unique look. Highly recommend!\"",
            "author": "- Jennifer K.",
            "detail": "Verified Purchase"
        },
        {
            "stars": 5,
            "text": "\"The complete suite has everything you need. From save the\ndates to thank you cards - one purchase covers it all.\"",
            "author": "- Amanda L.",
            "detail": "Verified Purchase"
        },
    ]

    y = 230
    for review in reviews:
        # Review card
        draw_rounded_rect(draw, (150, y, W - 150, y + 310), 20, WHITE, outline=GOLD, width=2)

        # Stars
        star_text = " ".join(["*"] * review["stars"])
        draw.text((220, y + 25), star_text, font=f_stars, fill=GOLD)

        # Review text
        lines = review["text"].split("\n")
        for i, line in enumerate(lines):
            draw.text((220, y + 80 + i * 40), line, font=f_review, fill=CHARCOAL)

        # Author
        draw.text((220, y + 200), review["author"], font=f_author, fill=SAGE)
        draw.text((220, y + 235), review["detail"], font=get_font(22), fill=(150, 150, 150))

        y += 350

    # Average rating
    draw_rounded_rect(draw, (600, y + 20, 1800, y + 120), 15, SAGE)
    f_avg = get_font(32, bold=True)
    draw_text_centered(draw, "***** 5.0 Average Rating  |  500+ Happy Couples", y + 45, f_avg, WHITE, W)

    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=2)
    img.save(os.path.join(BASE_DIR, "listing_09_testimonials.jpg"), "JPEG", quality=95)
    print("  Created: listing_09_testimonials.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE 10: Bundle CTA
# ═══════════════════════════════════════════════════════════════════════════════
def create_image_10():
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)

    f_big = get_serif(72, bold=True)
    f_title = get_serif(56, bold=True)
    f_sub = get_serif(36)
    f_price = get_serif(80, bold=True)
    f_original = get_font(40)
    f_detail = get_font(30)
    f_item = get_font(28)
    f_cta = get_font(40, bold=True)

    # Gold border
    draw.rectangle([20, 20, W - 20, H - 20], outline=GOLD, width=4)
    draw.rectangle([35, 35, W - 35, H - 35], outline=GOLD, width=2)

    # Title
    draw_text_centered(draw, "Complete Wedding", 100, f_big, CHARCOAL, W)
    draw_text_centered(draw, "Stationery Suite", 190, f_big, CHARCOAL, W)
    draw_gold_divider(draw, 290, W, 600)

    # Small preview strip
    preview_names = [
        "invitation_sage.png", "rsvp_sage.png", "save_the_date_sage.png",
        "details_sage.png", "thank_you_sage.png", "menu_sage.png",
        "table_number_01_sage.png", "place_card_sage.png"
    ]
    pw, ph = 240, 200
    p_spacing = 30
    p_total = len(preview_names) * pw + (len(preview_names) - 1) * p_spacing
    p_sx = (W - p_total) // 2

    for i, pname in enumerate(preview_names):
        x = p_sx + i * (pw + p_spacing)
        t_img = load_template(pname)
        if t_img:
            t_img = t_img.resize((pw, ph), Image.LANCZOS)
            # Shadow
            draw_rounded_rect(draw, (x + 4, 340 + 4, x + pw + 4, 340 + ph + 4), 5, (210, 210, 205))
            img.paste(t_img, (x, 340))
            draw.rectangle([x - 1, 339, x + pw + 1, 340 + ph + 1], outline=GOLD, width=1)

    # Included items list
    y = 590
    draw_text_centered(draw, "Everything You Need:", y, f_sub, SAGE, W)
    y += 60

    items_left = [
        "Wedding Invitation (3 colors)",
        "RSVP Card (3 colors)",
        "Save the Date (3 colors)",
        "Details Card (3 colors)",
    ]
    items_right = [
        "Thank You Card (3 colors)",
        "Menu Card (3 colors)",
        "Table Numbers 1-20",
        "Place Cards (3 colors)",
    ]

    for i, (left, right) in enumerate(zip(items_left, items_right)):
        ly = y + i * 50
        # Checkmark
        draw.text((400, ly), "  " + left, font=f_item, fill=CHARCOAL)
        draw.ellipse([380, ly + 8, 396, ly + 24], fill=SAGE)
        draw.text((1200, ly), "  " + right, font=f_item, fill=CHARCOAL)
        draw.ellipse([1180, ly + 8, 1196, ly + 24], fill=SAGE)

    y += 260

    # Total count
    draw_rounded_rect(draw, (400, y, 2000, y + 70), 10, LIGHT_SAGE)
    draw_text_centered(draw, "81+ Print-Ready Files  |  3 Color Palettes  |  Instant Download", y + 15, f_detail, CHARCOAL, W)
    y += 110

    # Price section
    draw_rounded_rect(draw, (500, y, 1900, y + 300), 25, WHITE, outline=GOLD, width=3)

    # Original price (struck through)
    orig_text = "$39.99"
    orig_w = draw.textbbox((0, 0), orig_text, font=f_original)[2]
    ox = (W - orig_w) // 2
    draw.text((ox, y + 30), orig_text, font=f_original, fill=(180, 180, 180))
    draw.line([(ox, y + 55), (ox + orig_w, y + 55)], fill=(180, 180, 180), width=3)

    # Sale price
    draw_text_centered(draw, "$14.99", y + 90, f_price, SAGE, W)
    draw_text_centered(draw, "63% OFF - Limited Time!", y + 200, f_detail, GOLD, W)

    y += 340

    # CTA button
    draw_rounded_rect(draw, (600, y, 1800, y + 100), 50, SAGE)
    draw_text_centered(draw, "Add to Cart - Instant Download", y + 22, f_cta, WHITE, W)

    # Bottom guarantees
    y += 150
    guarantees = [
        "Instant Digital Download",
        "No Physical Item Shipped",
        "Lifetime Access to Files"
    ]
    for i, g in enumerate(guarantees):
        gw = draw.textbbox((0, 0), g, font=f_detail)[2]
        gx = 300 + i * 700
        draw.text((gx, y), g, font=f_detail, fill=(130, 130, 130))

    # Bottom branches
    draw_branch_simple(draw, 100, H - 60, 'right', 200, SAGE, 2)
    draw_branch_simple(draw, W - 100, H - 60, 'left', 200, SAGE, 2)

    img.save(os.path.join(BASE_DIR, "listing_10_bundle_cta.jpg"), "JPEG", quality=95)
    print("  Created: listing_10_bundle_cta.jpg")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("Minimalist Wedding Suite - Listing Image Generator")
    print("=" * 60)

    print("\n1. Hero flat-lay mockup...")
    create_image_01()

    print("2. What's included...")
    create_image_02()

    print("3. Invitation variants close-up...")
    create_image_03()

    print("4. RSVP + Details cards...")
    create_image_04()

    print("5. Save the Date + Thank You...")
    create_image_05()

    print("6. Menu + Table Numbers...")
    create_image_06()

    print("7. Color palettes comparison...")
    create_image_07()

    print("8. Print guide / How to use...")
    create_image_08()

    print("9. Testimonials / Reviews...")
    create_image_09()

    print("10. Bundle CTA...")
    create_image_10()

    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.jpg')]
    print(f"\n{'=' * 60}")
    print(f"DONE! Generated {len(files)} listing images.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
