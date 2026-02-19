#!/usr/bin/env python3
"""
Minimalist Wedding Invitation Suite - Template Generator
Generates printable wedding stationery at 300 DPI equivalent resolution.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Directories ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(BASE_DIR, exist_ok=True)

# ── Color Palette ────────────────────────────────────────────────────────────
SAGE = (143, 174, 139)        # #8FAE8B
IVORY = (255, 255, 240)       # #FFFFF0
GOLD = (197, 165, 90)         # #C5A55A
CHARCOAL = (45, 45, 45)       # #2D2D2D
BLUSH = (245, 230, 224)       # #F5E6E0
WHITE = (255, 255, 255)
GOLD_LIGHT = (220, 200, 150)
SAGE_LIGHT = (200, 220, 195)
SAGE_DARK = (100, 140, 95)

# Three color variants
VARIANTS = {
    "sage": {
        "bg": IVORY,
        "accent": SAGE,
        "border": GOLD,
        "text_primary": CHARCOAL,
        "text_secondary": SAGE,
        "highlight": BLUSH,
        "name": "Sage & Gold"
    },
    "blush": {
        "bg": (252, 248, 245),
        "accent": (210, 170, 160),
        "border": GOLD,
        "text_primary": CHARCOAL,
        "text_secondary": (180, 140, 130),
        "highlight": BLUSH,
        "name": "Blush & Gold"
    },
    "classic": {
        "bg": WHITE,
        "accent": CHARCOAL,
        "border": GOLD,
        "text_primary": CHARCOAL,
        "text_secondary": (120, 120, 120),
        "highlight": (245, 245, 240),
        "name": "Classic Gold"
    }
}


def get_font(size, bold=False):
    """Get a font at the specified size."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_serif_font(size, bold=False):
    """Get a serif font for elegant text."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_text_centered(draw, text, y, font, fill, width):
    """Draw centered text at specified y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def draw_thin_border(draw, w, h, color, inset=40, thickness=2):
    """Draw a thin elegant border with optional corners."""
    x0, y0, x1, y1 = inset, inset, w - inset, h - inset
    for i in range(thickness):
        draw.rectangle([x0 + i, y0 + i, x1 - i, y1 - i], outline=color)


def draw_double_border(draw, w, h, color, inset=40, gap=8, thickness=1):
    """Draw a double-line border."""
    x0, y0, x1, y1 = inset, inset, w - inset, h - inset
    for i in range(thickness):
        draw.rectangle([x0 + i, y0 + i, x1 - i, y1 - i], outline=color)
    x0b, y0b, x1b, y1b = inset + gap, inset + gap, w - inset - gap, h - inset - gap
    for i in range(thickness):
        draw.rectangle([x0b + i, y0b + i, x1b - i, y1b - i], outline=color)


def draw_corner_ornaments(draw, w, h, color, inset=50, size=60, thickness=2):
    """Draw elegant corner decorations."""
    corners = [
        (inset, inset),                     # top-left
        (w - inset - size, inset),           # top-right
        (inset, h - inset - size),           # bottom-left
        (w - inset - size, h - inset - size) # bottom-right
    ]
    for cx, cy in corners:
        # L-shaped corner
        draw.line([(cx, cy), (cx + size, cy)], fill=color, width=thickness)
        draw.line([(cx, cy), (cx, cy + size)], fill=color, width=thickness)


def draw_leaf(draw, cx, cy, angle_deg, length, color, thickness=2):
    """Draw a simple leaf shape at a given position and angle."""
    angle = math.radians(angle_deg)
    # Stem
    ex = cx + length * math.cos(angle)
    ey = cy + length * math.sin(angle)
    draw.line([(cx, cy), (ex, ey)], fill=color, width=thickness)
    # Leaf blades along stem
    for t in [0.3, 0.5, 0.7]:
        px = cx + t * length * math.cos(angle)
        py = cy + t * length * math.sin(angle)
        perp = angle + math.pi / 2
        leaf_len = length * 0.2 * (1 - abs(t - 0.5))
        for side in [1, -1]:
            lx = px + side * leaf_len * math.cos(perp)
            ly = py + side * leaf_len * math.sin(perp)
            draw.line([(px, py), (lx, ly)], fill=color, width=max(1, thickness - 1))


def draw_branch(draw, x, y, direction, length, color, thickness=2):
    """Draw a botanical branch with small leaves.
    direction: 'right' or 'left'
    """
    sign = 1 if direction == 'right' else -1
    # Main stem as slight curve (approximated with segments)
    points = []
    segments = 12
    for i in range(segments + 1):
        t = i / segments
        px = x + sign * t * length
        py = y + math.sin(t * math.pi) * (-length * 0.08)
        points.append((px, py))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=thickness)

    # Leaves along branch
    leaf_positions = [0.15, 0.3, 0.45, 0.6, 0.75, 0.88]
    for t in leaf_positions:
        idx = int(t * segments)
        if idx >= len(points):
            idx = len(points) - 1
        px, py = points[idx]
        leaf_size = length * 0.12
        # Alternate sides
        for side_mult in [1, -1]:
            langle = -50 * side_mult if direction == 'right' else -50 * side_mult
            la = math.radians(langle + (0 if direction == 'right' else 180))
            lx = px + leaf_size * math.cos(la)
            ly = py + leaf_size * math.sin(la)
            # Draw small oval leaf using lines
            mid_x = (px + lx) / 2
            mid_y = (py + ly) / 2
            draw.line([(px, py), (lx, ly)], fill=color, width=max(1, thickness - 1))
            # Add a tiny perpendicular for leaf width
            perp_a = la + math.pi / 2
            bw = leaf_size * 0.25
            bx1 = mid_x + bw * math.cos(perp_a)
            by1 = mid_y + bw * math.sin(perp_a)
            bx2 = mid_x - bw * math.cos(perp_a)
            by2 = mid_y - bw * math.sin(perp_a)
            draw.line([(px, py), (bx1, by1), (lx, ly)], fill=color, width=1)
            draw.line([(px, py), (bx2, by2), (lx, ly)], fill=color, width=1)


def draw_eucalyptus_sprig(draw, cx, cy, scale, color, thickness=2):
    """Draw a delicate eucalyptus-style sprig centered at (cx, cy)."""
    # Central stem going upward
    stem_len = int(120 * scale)
    top_y = cy - stem_len
    draw.line([(cx, cy), (cx, top_y)], fill=color, width=thickness)

    # Round leaves along stem
    leaf_positions = [0.2, 0.35, 0.5, 0.65, 0.8]
    for t in leaf_positions:
        py = cy - t * stem_len
        offset = int(18 * scale)
        leaf_r = int(10 * scale)
        for side in [-1, 1]:
            lx = cx + side * offset
            # Draw a small circle for eucalyptus leaf
            draw.ellipse(
                [lx - leaf_r, py - leaf_r * 0.7, lx + leaf_r, py + leaf_r * 0.7],
                outline=color, width=max(1, thickness - 1)
            )
            draw.line([(cx, py), (lx, py)], fill=color, width=1)


def draw_floral_divider(draw, y, w, color, length=300, thickness=2):
    """Draw a horizontal botanical divider."""
    cx = w // 2
    # Center dot
    r = 4
    draw.ellipse([cx - r, y - r, cx + r, y + r], fill=color)
    # Lines extending
    draw.line([(cx - length // 2, y), (cx - 20, y)], fill=color, width=thickness)
    draw.line([(cx + 20, y), (cx + length // 2, y)], fill=color, width=thickness)
    # Small leaves at ends
    for side in [-1, 1]:
        ex = cx + side * length // 2
        for angle in [-30, 30]:
            la = math.radians(angle + (0 if side == 1 else 180))
            lx = ex + 15 * math.cos(la)
            ly = y + 15 * math.sin(la)
            draw.line([(ex, y), (lx, ly)], fill=color, width=1)


def draw_decorative_top(draw, w, variant, y_start=60):
    """Draw decorative botanical elements at the top of a card."""
    color = variant["accent"]
    cx = w // 2
    # Draw two branches meeting in the middle
    draw_branch(draw, cx - 10, y_start + 30, 'left', 200, color, 2)
    draw_branch(draw, cx + 10, y_start + 30, 'right', 200, color, 2)


def draw_decorative_bottom(draw, w, h, variant, y_offset=80):
    """Draw decorative botanical elements at the bottom."""
    color = variant["accent"]
    cx = w // 2
    y = h - y_offset
    draw_branch(draw, cx - 10, y, 'left', 160, color, 2)
    draw_branch(draw, cx + 10, y, 'right', 160, color, 2)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. WEDDING INVITATION (5x7 = 1500x2100)
# ═══════════════════════════════════════════════════════════════════════════════
def create_invitation(variant_name, variant):
    w, h = 1500, 2100
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    # Double border
    draw_double_border(draw, w, h, variant["border"], inset=50, gap=12, thickness=2)
    draw_corner_ornaments(draw, w, h, variant["border"], inset=55, size=40, thickness=2)

    # Top botanical
    draw_decorative_top(draw, w, variant, y_start=80)

    # "Together with their families"
    y = 240
    f_small = get_serif_font(36)
    f_script = get_serif_font(42)
    f_names = get_serif_font(80, bold=True)
    f_and = get_serif_font(50)
    f_medium = get_serif_font(38)
    f_detail = get_serif_font(32)

    h_text = draw_text_centered(draw, "Together with their families", y, f_script, variant["text_secondary"], w)
    y += h_text + 50

    # Divider
    draw_floral_divider(draw, y, w, variant["border"], length=350, thickness=1)
    y += 60

    # Names
    h_text = draw_text_centered(draw, "[BRIDE NAME]", y, f_names, variant["text_primary"], w)
    y += h_text + 20
    h_text = draw_text_centered(draw, "&", y, f_and, variant["accent"], w)
    y += h_text + 20
    h_text = draw_text_centered(draw, "[GROOM NAME]", y, f_names, variant["text_primary"], w)
    y += h_text + 50

    # Divider
    draw_floral_divider(draw, y, w, variant["border"], length=350, thickness=1)
    y += 60

    # "Request the pleasure of your company"
    h_text = draw_text_centered(draw, "Request the pleasure of your company", y, f_script, variant["text_secondary"], w)
    y += h_text + 30
    h_text = draw_text_centered(draw, "at the celebration of their marriage", y, f_script, variant["text_secondary"], w)
    y += h_text + 60

    # Date
    h_text = draw_text_centered(draw, "[DATE]", y, f_medium, variant["text_primary"], w)
    y += h_text + 20
    h_text = draw_text_centered(draw, "at [TIME]", y, f_detail, variant["text_secondary"], w)
    y += h_text + 40

    # Venue
    h_text = draw_text_centered(draw, "[VENUE NAME]", y, f_medium, variant["text_primary"], w)
    y += h_text + 15
    h_text = draw_text_centered(draw, "[VENUE ADDRESS]", y, f_detail, variant["text_secondary"], w)
    y += h_text + 15
    h_text = draw_text_centered(draw, "[CITY, STATE]", y, f_detail, variant["text_secondary"], w)
    y += h_text + 50

    # Reception info
    h_text = draw_text_centered(draw, "Reception to follow", y, f_script, variant["text_secondary"], w)
    y += h_text + 20

    # Bottom botanical
    draw_decorative_bottom(draw, w, h, variant, y_offset=100)

    # Eucalyptus accent
    draw_eucalyptus_sprig(draw, 150, h - 200, 0.8, variant["accent"], 2)
    draw_eucalyptus_sprig(draw, w - 150, h - 200, 0.8, variant["accent"], 2)

    fname = os.path.join(BASE_DIR, f"invitation_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# 2. RSVP CARD (5x3.5 = 1500x1050)
# ═══════════════════════════════════════════════════════════════════════════════
def create_rsvp(variant_name, variant):
    w, h = 1500, 1050
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    draw_thin_border(draw, w, h, variant["border"], inset=35, thickness=2)
    draw_corner_ornaments(draw, w, h, variant["border"], inset=40, size=30, thickness=2)

    f_title = get_serif_font(52, bold=True)
    f_medium = get_serif_font(34)
    f_small = get_serif_font(28)
    f_line = get_serif_font(26)

    y = 80
    draw_text_centered(draw, "RSVP", y, f_title, variant["text_primary"], w)
    y += 70

    draw_floral_divider(draw, y, w, variant["border"], length=250, thickness=1)
    y += 40

    draw_text_centered(draw, "Kindly respond by [DATE]", y, f_medium, variant["text_secondary"], w)
    y += 55

    # Name line
    draw_text_centered(draw, "M ________________________________", y, f_small, variant["text_primary"], w)
    y += 55

    # Accept / Decline
    draw_text_centered(draw, "___ Joyfully Accepts     ___ Respectfully Declines", y, f_small, variant["text_primary"], w)
    y += 55

    # Number of guests
    draw_text_centered(draw, "Number of Guests ____", y, f_small, variant["text_primary"], w)
    y += 55

    # Meal choice
    draw_text_centered(draw, "Meal Preference:", y, f_small, variant["text_secondary"], w)
    y += 40
    draw_text_centered(draw, "___ Beef    ___ Chicken    ___ Fish    ___ Vegetarian", y, f_line, variant["text_primary"], w)
    y += 55

    # Dietary
    draw_text_centered(draw, "Dietary Restrictions: ________________________________", y, f_line, variant["text_primary"], w)

    # Small botanical accents
    draw_branch(draw, 80, h - 60, 'right', 100, variant["accent"], 1)
    draw_branch(draw, w - 80, h - 60, 'left', 100, variant["accent"], 1)

    fname = os.path.join(BASE_DIR, f"rsvp_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SAVE THE DATE (5x7 = 1500x2100)
# ═══════════════════════════════════════════════════════════════════════════════
def create_save_the_date(variant_name, variant):
    w, h = 1500, 2100
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    draw_thin_border(draw, w, h, variant["border"], inset=50, thickness=2)

    f_save = get_serif_font(56)
    f_the = get_serif_font(40)
    f_date_word = get_serif_font(56)
    f_names = get_serif_font(72, bold=True)
    f_and = get_serif_font(48)
    f_date = get_serif_font(60, bold=True)
    f_detail = get_serif_font(34)
    f_small = get_serif_font(30)

    # Top botanical
    draw_decorative_top(draw, w, variant, y_start=80)

    y = 280
    draw_text_centered(draw, "SAVE", y, f_save, variant["text_secondary"], w)
    y += 70
    draw_text_centered(draw, "the", y, f_the, variant["accent"], w)
    y += 55
    draw_text_centered(draw, "DATE", y, f_date_word, variant["text_secondary"], w)
    y += 100

    draw_floral_divider(draw, y, w, variant["border"], length=400, thickness=1)
    y += 70

    draw_text_centered(draw, "[BRIDE NAME]", y, f_names, variant["text_primary"], w)
    y += 90
    draw_text_centered(draw, "&", y, f_and, variant["accent"], w)
    y += 65
    draw_text_centered(draw, "[GROOM NAME]", y, f_names, variant["text_primary"], w)
    y += 110

    draw_floral_divider(draw, y, w, variant["border"], length=400, thickness=1)
    y += 70

    draw_text_centered(draw, "[MONTH  DAY,  YEAR]", y, f_date, variant["text_primary"], w)
    y += 80
    draw_text_centered(draw, "[CITY, STATE]", y, f_detail, variant["text_secondary"], w)
    y += 70

    draw_text_centered(draw, "Formal invitation to follow", y, f_small, variant["text_secondary"], w)

    # Bottom botanical
    draw_decorative_bottom(draw, w, h, variant, y_offset=100)
    draw_eucalyptus_sprig(draw, w // 2, h - 130, 0.7, variant["accent"], 2)

    fname = os.path.join(BASE_DIR, f"save_the_date_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DETAILS / INFO CARD (5x3.5 = 1500x1050)
# ═══════════════════════════════════════════════════════════════════════════════
def create_details(variant_name, variant):
    w, h = 1500, 1050
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    draw_thin_border(draw, w, h, variant["border"], inset=35, thickness=2)

    f_title = get_serif_font(48, bold=True)
    f_sub = get_serif_font(32, bold=True)
    f_body = get_serif_font(28)

    y = 70
    draw_text_centered(draw, "DETAILS", y, f_title, variant["text_primary"], w)
    y += 60
    draw_floral_divider(draw, y, w, variant["border"], length=250, thickness=1)
    y += 45

    # Ceremony
    draw_text_centered(draw, "CEREMONY", y, f_sub, variant["accent"], w)
    y += 40
    draw_text_centered(draw, "[TIME] | [VENUE NAME]", y, f_body, variant["text_primary"], w)
    y += 32
    draw_text_centered(draw, "[VENUE ADDRESS, CITY, STATE]", y, f_body, variant["text_secondary"], w)
    y += 50

    # Reception
    draw_text_centered(draw, "RECEPTION", y, f_sub, variant["accent"], w)
    y += 40
    draw_text_centered(draw, "[TIME] | [RECEPTION VENUE]", y, f_body, variant["text_primary"], w)
    y += 32
    draw_text_centered(draw, "[RECEPTION ADDRESS, CITY, STATE]", y, f_body, variant["text_secondary"], w)
    y += 50

    # Accommodations
    draw_text_centered(draw, "ACCOMMODATIONS", y, f_sub, variant["accent"], w)
    y += 40
    draw_text_centered(draw, "A block of rooms has been reserved at [HOTEL NAME]", y, f_body, variant["text_primary"], w)
    y += 32
    draw_text_centered(draw, "Please mention [BRIDE & GROOM] wedding for group rate", y, f_body, variant["text_secondary"], w)
    y += 50

    # Registry
    draw_text_centered(draw, "[WEDDING WEBSITE URL]", y, f_body, variant["accent"], w)

    draw_branch(draw, 70, h - 50, 'right', 90, variant["accent"], 1)
    draw_branch(draw, w - 70, h - 50, 'left', 90, variant["accent"], 1)

    fname = os.path.join(BASE_DIR, f"details_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# 5. THANK YOU CARD (5x7 = 1500x2100)
# ═══════════════════════════════════════════════════════════════════════════════
def create_thank_you(variant_name, variant):
    w, h = 1500, 2100
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    draw_double_border(draw, w, h, variant["border"], inset=50, gap=12, thickness=1)

    f_thank = get_serif_font(80, bold=True)
    f_you = get_serif_font(80, bold=True)
    f_body = get_serif_font(36)
    f_names = get_serif_font(52, bold=True)
    f_small = get_serif_font(30)

    # Top botanical
    draw_decorative_top(draw, w, variant, y_start=80)

    y = 400
    draw_text_centered(draw, "Thank", y, f_thank, variant["text_primary"], w)
    y += 100
    draw_text_centered(draw, "You", y, f_you, variant["text_primary"], w)
    y += 130

    draw_floral_divider(draw, y, w, variant["border"], length=400, thickness=1)
    y += 80

    lines = [
        "We are so grateful for your presence",
        "and generosity on our special day.",
        "",
        "Your love and support mean",
        "the world to us."
    ]
    for line in lines:
        if line:
            draw_text_centered(draw, line, y, f_body, variant["text_secondary"], w)
            y += 50
        else:
            y += 30

    y += 60
    draw_floral_divider(draw, y, w, variant["border"], length=300, thickness=1)
    y += 70

    draw_text_centered(draw, "With love,", y, f_small, variant["text_secondary"], w)
    y += 55
    draw_text_centered(draw, "[BRIDE] & [GROOM]", y, f_names, variant["text_primary"], w)
    y += 70
    draw_text_centered(draw, "[WEDDING DATE]", y, f_small, variant["accent"], w)

    # Bottom botanical
    draw_decorative_bottom(draw, w, h, variant, y_offset=100)

    fname = os.path.join(BASE_DIR, f"thank_you_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# 6. MENU CARD (4x9 = 1200x2700)
# ═══════════════════════════════════════════════════════════════════════════════
def create_menu(variant_name, variant):
    w, h = 1200, 2700
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    draw_thin_border(draw, w, h, variant["border"], inset=40, thickness=2)

    f_title = get_serif_font(56, bold=True)
    f_course = get_serif_font(36, bold=True)
    f_item = get_serif_font(30)
    f_desc = get_serif_font(24)

    # Top decoration
    draw_decorative_top(draw, w, variant, y_start=60)

    y = 180
    draw_text_centered(draw, "MENU", y, f_title, variant["text_primary"], w)
    y += 80
    draw_floral_divider(draw, y, w, variant["border"], length=280, thickness=1)
    y += 60

    courses = [
        ("FIRST COURSE", [
            ("[Appetizer Name]", "[Description of the appetizer]"),
        ]),
        ("SECOND COURSE", [
            ("[Soup or Salad Name]", "[Description of the course]"),
        ]),
        ("MAIN COURSE", [
            ("[Beef Option]", "[Description of the dish]"),
            ("[Chicken Option]", "[Description of the dish]"),
            ("[Fish Option]", "[Description of the dish]"),
            ("[Vegetarian Option]", "[Description of the dish]"),
        ]),
        ("DESSERT", [
            ("[Dessert Name]", "[Description of the dessert]"),
            ("Wedding Cake", "[Flavor description]"),
        ]),
        ("BEVERAGES", [
            ("[Signature Cocktail Name]", "[Description of cocktail]"),
            ("Open bar with selection of wines, beer, and spirits", ""),
        ]),
    ]

    for course_name, items in courses:
        draw_text_centered(draw, course_name, y, f_course, variant["accent"], w)
        y += 50
        for item_name, desc in items:
            draw_text_centered(draw, item_name, y, f_item, variant["text_primary"], w)
            y += 35
            if desc:
                draw_text_centered(draw, desc, y, f_desc, variant["text_secondary"], w)
                y += 35
            else:
                y += 10
        # Small divider between courses
        dot_r = 3
        draw.ellipse([w // 2 - dot_r, y - dot_r, w // 2 + dot_r, y + dot_r], fill=variant["border"])
        y += 40

    y += 20
    draw_text_centered(draw, "[BRIDE] & [GROOM]", y, f_course, variant["text_primary"], w)
    y += 50
    draw_text_centered(draw, "[WEDDING DATE]", y, f_desc, variant["text_secondary"], w)

    draw_decorative_bottom(draw, w, h, variant, y_offset=80)

    fname = os.path.join(BASE_DIR, f"menu_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# 7. TABLE NUMBER CARDS (4x6 = 1200x1800) - Numbers 1-20
# ═══════════════════════════════════════════════════════════════════════════════
def create_table_numbers(variant_name, variant):
    for num in range(1, 21):
        w, h = 1200, 1800
        img = Image.new("RGB", (w, h), variant["bg"])
        draw = ImageDraw.Draw(img)

        draw_double_border(draw, w, h, variant["border"], inset=45, gap=10, thickness=1)

        f_table = get_serif_font(40)
        f_number = get_serif_font(200, bold=True)
        f_small = get_serif_font(30)

        # Top botanical
        draw_decorative_top(draw, w, variant, y_start=70)

        y = 300
        draw_text_centered(draw, "TABLE", y, f_table, variant["text_secondary"], w)
        y += 80

        draw_floral_divider(draw, y, w, variant["border"], length=300, thickness=1)
        y += 80

        draw_text_centered(draw, str(num), y, f_number, variant["text_primary"], w)
        y += 250

        draw_floral_divider(draw, y, w, variant["border"], length=300, thickness=1)

        # Bottom botanical
        draw_decorative_bottom(draw, w, h, variant, y_offset=100)
        draw_eucalyptus_sprig(draw, 160, h - 250, 0.6, variant["accent"], 1)
        draw_eucalyptus_sprig(draw, w - 160, h - 250, 0.6, variant["accent"], 1)

        fname = os.path.join(BASE_DIR, f"table_number_{num:02d}_{variant_name}.png")
        img.save(fname, "PNG", dpi=(300, 300))

    print(f"  Created: table_number_01-20_{variant_name}.png (20 files)")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. PLACE CARDS (3.5x2 = 1050x600)
# ═══════════════════════════════════════════════════════════════════════════════
def create_place_card(variant_name, variant):
    w, h = 1050, 600
    img = Image.new("RGB", (w, h), variant["bg"])
    draw = ImageDraw.Draw(img)

    draw_thin_border(draw, w, h, variant["border"], inset=25, thickness=1)

    f_name = get_serif_font(48, bold=True)
    f_small = get_serif_font(24)

    # Small top decoration
    cx = w // 2
    draw_branch(draw, cx - 5, 55, 'left', 80, variant["accent"], 1)
    draw_branch(draw, cx + 5, 55, 'right', 80, variant["accent"], 1)

    y = 200
    draw_floral_divider(draw, y, w, variant["border"], length=200, thickness=1)
    y += 40

    draw_text_centered(draw, "[GUEST NAME]", y, f_name, variant["text_primary"], w)
    y += 65

    draw_floral_divider(draw, y + 20, w, variant["border"], length=200, thickness=1)

    # Tiny bottom accent
    draw_branch(draw, cx - 5, h - 55, 'left', 60, variant["accent"], 1)
    draw_branch(draw, cx + 5, h - 55, 'right', 60, variant["accent"], 1)

    fname = os.path.join(BASE_DIR, f"place_card_{variant_name}.png")
    img.save(fname, "PNG", dpi=(300, 300))
    print(f"  Created: {fname}")
    return img


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("Minimalist Wedding Invitation Suite - Template Generator")
    print("=" * 60)

    for vname, vdata in VARIANTS.items():
        print(f"\n--- Generating {vdata['name']} variant ({vname}) ---")

        print("  1. Wedding Invitation (1500x2100)")
        create_invitation(vname, vdata)

        print("  2. RSVP Card (1500x1050)")
        create_rsvp(vname, vdata)

        print("  3. Save the Date (1500x2100)")
        create_save_the_date(vname, vdata)

        print("  4. Details/Info Card (1500x1050)")
        create_details(vname, vdata)

        print("  5. Thank You Card (1500x2100)")
        create_thank_you(vname, vdata)

        print("  6. Menu Card (1200x2700)")
        create_menu(vname, vdata)

        print("  7. Table Number Cards (1200x1800) x20")
        create_table_numbers(vname, vdata)

        print("  8. Place Cards (1050x600)")
        create_place_card(vname, vdata)

    # Count files
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.png')]
    print(f"\n{'=' * 60}")
    print(f"DONE! Generated {len(files)} template files.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
