#!/usr/bin/env python3
"""
Generate Etsy listing mockup images for ShelzysDesignsStore.
Creates 10 professional product images (5 per listing) with St. Patrick's Day themes.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "etsy-listing-images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Color Palette ──────────────────────────────────────────────
DARK_GREEN = (21, 87, 36)
MEDIUM_GREEN = (34, 139, 34)
BRIGHT_GREEN = (50, 180, 50)
LIGHT_GREEN = (144, 238, 144)
PALE_GREEN = (200, 240, 200)
MINT = (220, 245, 220)
GOLD = (218, 165, 32)
BRIGHT_GOLD = (255, 200, 50)
LIGHT_GOLD = (255, 223, 120)
PALE_GOLD = (255, 240, 180)
WHITE = (255, 255, 255)
OFF_WHITE = (248, 248, 245)
CREAM = (255, 250, 240)
LIGHT_GRAY = (240, 240, 240)
MEDIUM_GRAY = (180, 180, 180)
DARK_GRAY = (60, 60, 60)
CHARCOAL = (40, 40, 40)
ORANGE = (255, 140, 50)
SOFT_PINK = (255, 200, 200)
SKY_BLUE = (135, 206, 235)
CORAL = (255, 127, 80)

# ── Font Helpers ───────────────────────────────────────────────
def get_font(size, bold=False):
    """Get the best available font at the given size."""
    if bold:
        paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_serif_font(size, bold=False):
    """Get the best available serif font."""
    if bold:
        paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size, bold)


# ── Drawing Primitives ─────────────────────────────────────────
def draw_shamrock(draw, cx, cy, size, color):
    """Draw a shamrock (three-leaf clover) at (cx, cy)."""
    r = size // 3
    offsets = [
        (0, -r),                    # top leaf
        (-r * 0.87, r * 0.5),      # bottom-left leaf
        (r * 0.87, r * 0.5),       # bottom-right leaf
    ]
    for ox, oy in offsets:
        x = cx + int(ox)
        y = cy + int(oy)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    # stem
    stem_w = max(2, size // 10)
    draw.rectangle([cx - stem_w, cy + r // 2, cx + stem_w, cy + size], fill=color)


def draw_star(draw, cx, cy, size, color):
    """Draw a four-pointed star."""
    pts = []
    for i in range(8):
        angle = math.pi / 4 * i - math.pi / 2
        r = size if i % 2 == 0 else size * 0.4
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=color)


def draw_rainbow_arc(draw, cx, cy, radius, thickness=20):
    """Draw a rainbow arc (semicircle)."""
    colors_list = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0),
        (0, 200, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
    ]
    band = thickness // len(colors_list) + 1
    for i, c in enumerate(colors_list):
        r = radius - i * band
        if r < 5:
            break
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.arc(bbox, 180, 360, fill=c, width=band + 1)


def draw_pot_of_gold(draw, cx, cy, size):
    """Draw a simple pot of gold icon."""
    pw = size
    ph = int(size * 0.7)
    # pot body
    draw.ellipse([cx - pw // 2, cy - ph // 4, cx + pw // 2, cy + ph // 2], fill=CHARCOAL)
    draw.rectangle([cx - pw // 2 + 5, cy - ph // 4, cx + pw // 2 - 5, cy + ph // 6], fill=CHARCOAL)
    # gold rim
    draw.rectangle([cx - pw // 2 - 3, cy - ph // 4 - 4, cx + pw // 2 + 3, cy - ph // 4 + 4], fill=GOLD)
    # gold coins on top
    for offset in [-pw // 4, 0, pw // 4]:
        draw.ellipse([cx + offset - 8, cy - ph // 4 - 16, cx + offset + 8, cy - ph // 4], fill=BRIGHT_GOLD)


def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = bbox
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    # corners
    draw.pieslice([x1, y1, x1 + 2 * r, y1 + 2 * r], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x2 - 2 * r, y1, x2, y1 + 2 * r], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y2 - 2 * r, x1 + 2 * r, y2], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x2 - 2 * r, y2 - 2 * r, x2, y2], 0, 90, fill=fill, outline=outline, width=width)
    # edges
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x1 + r, y2 - r], fill=fill)
    draw.rectangle([x2 - r, y1 + r, x2, y2 - r], fill=fill)
    if outline:
        draw.line([(x1 + r, y1), (x2 - r, y1)], fill=outline, width=width)
        draw.line([(x1 + r, y2), (x2 - r, y2)], fill=outline, width=width)
        draw.line([(x1, y1 + r), (x1, y2 - r)], fill=outline, width=width)
        draw.line([(x2, y1 + r), (x2, y2 - r)], fill=outline, width=width)


def gradient_bg(img, color_top, color_bottom):
    """Apply a vertical gradient to the image."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        t = y / h
        r = int(color_top[0] * (1 - t) + color_bottom[0] * t)
        g = int(color_top[1] * (1 - t) + color_bottom[1] * t)
        b = int(color_top[2] * (1 - t) + color_bottom[2] * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def scatter_shamrocks(draw, w, h, count=25, size_range=(20, 50), color=None):
    """Scatter random shamrocks across the canvas."""
    random.seed(42)
    for _ in range(count):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(*size_range)
        c = color or (random.randint(30, 80), random.randint(130, 200), random.randint(30, 80),)
        draw_shamrock(draw, x, y, s, c)


def draw_text_centered(draw, text, y, font, fill, img_width):
    """Draw text centered horizontally at the given y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img_width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def draw_text_with_shadow(draw, text, y, font, fill, img_width, shadow_color=None, offset=3):
    """Draw centered text with a drop shadow."""
    if shadow_color is None:
        shadow_color = (0, 0, 0, 80)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img_width - tw) // 2
    # shadow
    sc = shadow_color if len(shadow_color) == 3 else shadow_color[:3]
    draw.text((x + offset, y + offset), text, font=font, fill=sc)
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def draw_banner(draw, y, height, img_width, color, alpha_color=None):
    """Draw a horizontal banner/ribbon."""
    draw.rectangle([0, y, img_width, y + height], fill=color)
    # ribbon ends
    tri_size = height // 3
    draw.polygon([(0, y), (tri_size, y + height // 2), (0, y + height)], fill=color)
    draw.polygon([(img_width, y), (img_width - tri_size, y + height // 2), (img_width, y + height)], fill=color)


def draw_page_mockup(draw, x, y, pw, ph, title_text="", color=WHITE, shadow=True):
    """Draw a paper page mockup with optional shadow."""
    if shadow:
        draw.rectangle([x + 6, y + 6, x + pw + 6, y + ph + 6], fill=(180, 180, 180))
    draw.rectangle([x, y, x + pw, y + ph], fill=color, outline=MEDIUM_GRAY, width=2)
    # lines to simulate content
    line_y = y + 30
    if title_text:
        small_f = get_font(max(14, pw // 15), bold=True)
        tb = draw.textbbox((0, 0), title_text, font=small_f)
        tw = tb[2] - tb[0]
        draw.text((x + (pw - tw) // 2, line_y), title_text, font=small_f, fill=DARK_GREEN)
        line_y += 40
    return line_y


def draw_phone_mockup(draw, cx, cy, pw, ph, screen_color=WHITE):
    """Draw a simplified phone frame and return the screen area coordinates."""
    bezel = 12
    corner_r = 30
    # phone body
    draw_rounded_rect(draw,
                      [cx - pw // 2 - bezel, cy - ph // 2 - bezel * 3,
                       cx + pw // 2 + bezel, cy + ph // 2 + bezel * 3],
                      corner_r, fill=CHARCOAL)
    # screen
    draw.rectangle([cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2], fill=screen_color)
    # notch
    draw_rounded_rect(draw, [cx - 40, cy - ph // 2 - bezel * 3, cx + 40, cy - ph // 2 - bezel], 10, fill=CHARCOAL)
    return (cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2)


def draw_laptop_mockup(draw, cx, cy, sw, sh):
    """Draw a simplified laptop and return the screen area coords."""
    # screen bezel
    bx1, by1 = cx - sw // 2 - 15, cy - sh // 2 - 15
    bx2, by2 = cx + sw // 2 + 15, cy + sh // 2 + 15
    draw_rounded_rect(draw, [bx1, by1, bx2, by2], 12, fill=DARK_GRAY)
    # screen
    draw.rectangle([cx - sw // 2, cy - sh // 2, cx + sw // 2, cy + sh // 2], fill=WHITE)
    # base/keyboard
    kw = int(sw * 1.3)
    draw_rounded_rect(draw, [cx - kw // 2, by2, cx + kw // 2, by2 + 20], 5, fill=MEDIUM_GRAY)
    # hinge
    draw.rectangle([cx - kw // 2 + 20, by2, cx + kw // 2 - 20, by2 + 4], fill=DARK_GRAY)
    return (cx - sw // 2, cy - sh // 2, cx + sw // 2, cy + sh // 2)


def add_watermark(draw, w, h, text="ShelzysDesignsStore"):
    """Add a subtle shop watermark."""
    f = get_font(28)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text((w - tw - 20, h - 40), text, font=f, fill=(180, 180, 180))


def draw_check_bullet(draw, x, y, size, color=BRIGHT_GREEN):
    """Draw a checkmark bullet point."""
    draw.ellipse([x, y, x + size, y + size], fill=color)
    # checkmark inside
    cs = size // 4
    points = [
        (x + cs, y + size // 2),
        (x + size // 2 - 2, y + size - cs - 2),
        (x + size - cs, y + cs + 2),
    ]
    draw.line(points, fill=WHITE, width=max(2, size // 8))


def draw_decorative_border(draw, w, h, thickness=8, color=GOLD):
    """Draw a decorative double-line border."""
    draw.rectangle([0, 0, w - 1, h - 1], outline=color, width=thickness)
    inset = thickness + 6
    draw.rectangle([inset, inset, w - 1 - inset, h - 1 - inset], outline=color, width=2)


# ══════════════════════════════════════════════════════════════════
# LISTING 1: St. Patrick's Day Kids Activity Bundle ($6.99)
# ══════════════════════════════════════════════════════════════════

def listing1_cover():
    """Image 1: Bold, colorful cover image with shamrocks, rainbows, festive elements."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H))
    gradient_bg(img, (15, 100, 40), (8, 60, 25))
    draw = ImageDraw.Draw(img)

    # Scatter large background shamrocks (subtle)
    random.seed(10)
    for _ in range(30):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(40, 100)
        alpha_g = random.randint(50, 90)
        draw_shamrock(draw, x, y, s, (alpha_g, alpha_g + 50, alpha_g))

    # Rainbow arcs at top
    draw_rainbow_arc(draw, W // 2, 250, 600, thickness=80)
    draw_rainbow_arc(draw, W // 2, 250, 450, thickness=50)

    # Pot of gold
    draw_pot_of_gold(draw, W // 2, 300, 80)

    # Central white panel
    panel_y = 420
    panel_h = 1100
    panel_pad = 120
    draw_rounded_rect(draw, [panel_pad, panel_y, W - panel_pad, panel_y + panel_h], 40, fill=WHITE)
    # gold border on panel
    draw_rounded_rect(draw, [panel_pad + 4, panel_y + 4, W - panel_pad - 4, panel_y + panel_h - 4], 38, outline=GOLD, width=5)

    # Title text on panel
    title_font = get_font(92, bold=True)
    sub_font = get_font(56, bold=True)
    desc_font = get_font(46)
    price_font = get_font(72, bold=True)

    ty = panel_y + 60
    draw_text_centered(draw, "ST. PATRICK'S DAY", ty, title_font, DARK_GREEN, W)
    ty += 110
    draw_text_centered(draw, "KIDS ACTIVITY", ty, title_font, DARK_GREEN, W)
    ty += 110
    draw_text_centered(draw, "BUNDLE", ty, title_font, DARK_GREEN, W)

    ty += 130
    # gold divider
    draw.rectangle([W // 2 - 250, ty, W // 2 + 250, ty + 5], fill=GOLD)
    ty += 30

    items = ["Coloring Pages", "Fun Games", "Activity Sheets", "Printable PDF Download"]
    for item in items:
        h = draw_text_centered(draw, f"★  {item}  ★", ty, desc_font, MEDIUM_GREEN, W)
        ty += h + 18

    ty += 30
    # Price badge
    badge_w, badge_h = 300, 100
    bx = W // 2 - badge_w // 2
    draw_rounded_rect(draw, [bx, ty, bx + badge_w, ty + badge_h], 20, fill=GOLD)
    draw_text_centered(draw, "$6.99", ty + 12, price_font, WHITE, W)

    # Large shamrocks flanking the panel
    draw_shamrock(draw, 90, panel_y + 200, 100, BRIGHT_GREEN)
    draw_shamrock(draw, W - 90, panel_y + 200, 100, BRIGHT_GREEN)
    draw_shamrock(draw, 90, panel_y + panel_h - 200, 80, LIGHT_GREEN)
    draw_shamrock(draw, W - 90, panel_y + panel_h - 200, 80, LIGHT_GREEN)

    # Stars near rainbow
    for sx, sy in [(200, 150), (W - 200, 150), (350, 80), (W - 350, 80)]:
        draw_star(draw, sx, sy, 25, BRIGHT_GOLD)

    # Bottom banner
    draw.rectangle([0, H - 150, W, H], fill=GOLD)
    banner_font = get_font(52, bold=True)
    draw_text_centered(draw, "INSTANT DIGITAL DOWNLOAD  ●  PRINTABLE PDF", H - 120, banner_font, DARK_GREEN, W)

    # Corner shamrocks
    draw_shamrock(draw, 50, H - 80, 50, DARK_GREEN)
    draw_shamrock(draw, W - 50, H - 80, 50, DARK_GREEN)

    add_watermark(draw, W, H - 150)
    img.save(os.path.join(OUTPUT_DIR, "listing1-cover.png"), "PNG", quality=95)
    print("  ✓ listing1-cover.png")


def listing1_whats_included():
    """Image 2: What's Included graphic."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    draw_decorative_border(draw, W, H, 10, DARK_GREEN)

    # Header area with green background
    draw.rectangle([20, 20, W - 20, 320], fill=DARK_GREEN)
    title_font = get_font(88, bold=True)
    draw_text_centered(draw, "WHAT'S INCLUDED", 60, title_font, WHITE, W)
    sub_font = get_font(48)
    draw_text_centered(draw, "St. Patrick's Day Kids Activity Bundle", 180, sub_font, LIGHT_GOLD, W)
    draw_shamrock(draw, 100, 60, 50, LIGHT_GREEN)
    draw_shamrock(draw, W - 100, 60, 50, LIGHT_GREEN)

    # Items list with icons
    items = [
        ("🎨  10+ Coloring Pages", "Shamrocks, leprechauns, rainbows & more"),
        ("🎲  5 Fun Games & Puzzles", "Mazes, word searches, matching games"),
        ("📝  Activity Sheets", "Dot-to-dot, tracing, counting activities"),
        ("✂️  Cut & Paste Crafts", "Hands-on creative craft templates"),
        ("📄  All Pages Print-Ready", "Standard US Letter size (8.5\" x 11\")"),
        ("⬇️  Instant Digital Download", "ZIP file with high-quality PDF pages"),
    ]

    y_start = 400
    item_h = 230
    item_font = get_font(52, bold=True)
    desc_font = get_font(40)
    left_margin = 180

    for i, (title, desc) in enumerate(items):
        y = y_start + i * item_h
        # alternating background
        if i % 2 == 0:
            draw.rectangle([40, y, W - 40, y + item_h - 15], fill=PALE_GREEN)
        else:
            draw.rectangle([40, y, W - 40, y + item_h - 15], fill=CREAM)
        # green checkmark circle
        draw_check_bullet(draw, 70, y + 35, 60, BRIGHT_GREEN)
        # text
        draw.text((left_margin, y + 30), title, font=item_font, fill=DARK_GREEN)
        draw.text((left_margin, y + 100), desc, font=desc_font, fill=DARK_GRAY)
        # small shamrock decoration
        draw_shamrock(draw, W - 100, y + item_h // 2, 30, LIGHT_GREEN)

    # Bottom banner
    y_bottom = y_start + len(items) * item_h + 20
    draw_rounded_rect(draw, [100, y_bottom, W - 100, y_bottom + 120], 20, fill=GOLD)
    badge_font = get_font(50, bold=True)
    draw_text_centered(draw, "ONLY $6.99  •  INSTANT DOWNLOAD", y_bottom + 30, badge_font, WHITE, W)

    add_watermark(draw, W, H)
    img.save(os.path.join(OUTPUT_DIR, "listing1-whats-included.png"), "PNG", quality=95)
    print("  ✓ listing1-whats-included.png")


def listing1_coloring_pages_mockup():
    """Image 3: Mockup of coloring pages laid out flat on a white surface."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H), OFF_WHITE)
    draw = ImageDraw.Draw(img)

    # Subtle texture - light dots
    random.seed(99)
    for _ in range(200):
        x, y = random.randint(0, W), random.randint(0, H)
        draw.ellipse([x, y, x + 3, y + 3], fill=(235, 235, 235))

    # Draw 6 coloring pages spread out
    pages = [
        ("Shamrock", "Coloring Page"),
        ("Leprechaun", "Coloring Page"),
        ("Rainbow", "Color by Number"),
        ("Pot of Gold", "Coloring Page"),
        ("Lucky Clover", "Coloring Page"),
        ("St. Patrick", "Activity Page"),
    ]

    positions = [
        (180, 200, 520, 680),
        (740, 150, 520, 680),
        (1300, 220, 520, 680),
        (250, 1020, 520, 680),
        (810, 980, 520, 680),
        (1370, 1040, 520, 680),
    ]

    title_font = get_font(30, bold=True)
    sub_font = get_font(22)

    for (title, subtitle), (px, py, pw, ph) in zip(pages, positions):
        # Page shadow
        draw.rectangle([px + 8, py + 8, px + pw + 8, py + ph + 8], fill=(200, 200, 200))
        # Page
        draw.rectangle([px, py, px + pw, py + ph], fill=WHITE, outline=LIGHT_GRAY, width=2)
        # Header area
        draw.rectangle([px + 15, py + 15, px + pw - 15, py + 70], fill=PALE_GREEN)
        tb = draw.textbbox((0, 0), title, font=title_font)
        tw = tb[2] - tb[0]
        draw.text((px + (pw - tw) // 2, py + 22), title, font=title_font, fill=DARK_GREEN)
        tb2 = draw.textbbox((0, 0), subtitle, font=sub_font)
        tw2 = tb2[2] - tb2[0]
        draw.text((px + (pw - tw2) // 2, py + 80), subtitle, font=sub_font, fill=MEDIUM_GRAY)

        # Draw a simple illustration outline based on the page type
        cx = px + pw // 2
        cy = py + ph // 2 + 30
        if "Shamrock" in title or "Clover" in title:
            draw_shamrock(draw, cx, cy, 120, LIGHT_GREEN)
            # outline over it
            draw_shamrock(draw, cx, cy, 122, None)
        elif "Leprechaun" in title:
            # simple hat shape
            draw.rectangle([cx - 60, cy - 50, cx + 60, cy + 10], outline=DARK_GREEN, width=3)
            draw.rectangle([cx - 80, cy + 10, cx + 80, cy + 30], outline=DARK_GREEN, width=3)
            draw.ellipse([cx - 40, cy + 30, cx + 40, cy + 120], outline=DARK_GREEN, width=3)
            draw.rectangle([cx - 15, cy - 20, cx + 15, cy + 10], outline=GOLD, width=2)
        elif "Rainbow" in title:
            draw_rainbow_arc(draw, cx, cy + 40, 140, thickness=50)
        elif "Pot" in title:
            draw_pot_of_gold(draw, cx, cy, 100)
        elif "Patrick" in title:
            draw_shamrock(draw, cx - 60, cy, 60, LIGHT_GREEN)
            draw_shamrock(draw, cx + 60, cy, 60, LIGHT_GREEN)
            draw_star(draw, cx, cy - 30, 30, LIGHT_GOLD)

        # Page number
        pn_font = get_font(20)
        pn = f"Page {pages.index((title, subtitle)) + 1}"
        draw.text((px + pw - 80, py + ph - 30), pn, font=pn_font, fill=MEDIUM_GRAY)

    # Decorative elements around pages
    draw_shamrock(draw, 80, 100, 60, BRIGHT_GREEN)
    draw_shamrock(draw, W - 80, 100, 60, BRIGHT_GREEN)
    draw_shamrock(draw, 80, H - 100, 60, BRIGHT_GREEN)
    draw_shamrock(draw, W - 80, H - 100, 60, BRIGHT_GREEN)
    draw_star(draw, W // 2, 80, 30, GOLD)
    draw_star(draw, W // 2, H - 80, 30, GOLD)

    # Title bar at bottom
    draw.rectangle([0, H - 120, W, H], fill=DARK_GREEN)
    bar_font = get_font(44, bold=True)
    draw_text_centered(draw, "PREVIEW  •  ST. PATRICK'S DAY COLORING PAGES", H - 95, bar_font, WHITE, W)

    add_watermark(draw, W, H - 120)
    img.save(os.path.join(OUTPUT_DIR, "listing1-coloring-pages.png"), "PNG", quality=95)
    print("  ✓ listing1-coloring-pages.png")


def listing1_lifestyle():
    """Image 4: Lifestyle image of a child coloring a St. Patrick's Day page."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Warm wooden table background
    for y in range(H):
        r = 200 + int(30 * math.sin(y * 0.02))
        g = 160 + int(20 * math.sin(y * 0.02))
        b = 110 + int(15 * math.sin(y * 0.02))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # Wood grain lines
    random.seed(55)
    for _ in range(40):
        y = random.randint(0, H)
        draw.line([(0, y), (W, y)], fill=(180, 140, 90), width=1)

    # Large coloring page in center (angled slightly)
    page_w, page_h = 900, 1200
    cx, cy = W // 2 - 50, H // 2
    # page shadow
    draw.rectangle([cx - page_w // 2 + 10, cy - page_h // 2 + 10,
                     cx + page_w // 2 + 10, cy + page_h // 2 + 10], fill=(140, 110, 70))
    draw.rectangle([cx - page_w // 2, cy - page_h // 2,
                     cx + page_w // 2, cy + page_h // 2], fill=WHITE)

    # Content on the page
    pf = get_font(44, bold=True)
    draw.text((cx - page_w // 2 + 60, cy - page_h // 2 + 40), "Happy St. Patrick's Day!", font=pf, fill=DARK_GREEN)
    # Large shamrock outline
    sc_x, sc_y = cx, cy - 50
    for ring_size in [200, 180]:
        offsets = [(0, -ring_size // 3), (-ring_size // 3 * 0.87, ring_size // 3 * 0.5),
                   (ring_size // 3 * 0.87, ring_size // 3 * 0.5)]
        r = ring_size // 3
        for ox, oy in offsets:
            ex = sc_x + int(ox)
            ey = sc_y + int(oy)
            draw.ellipse([ex - r, ey - r, ex + r, ey + r], outline=DARK_GREEN, width=4)
    # stem
    draw.line([(sc_x, sc_y + 80), (sc_x + 10, sc_y + 200)], fill=DARK_GREEN, width=4)

    # Partially colored sections (to show child coloring)
    draw.ellipse([sc_x - 55, sc_y - 90, sc_x + 10, sc_y - 30], fill=BRIGHT_GREEN)
    draw.ellipse([sc_x + 20, sc_y + 10, sc_x + 75, sc_y + 60], fill=(100, 200, 100))

    # Crayons scattered around
    crayon_colors = [
        (34, 139, 34), (255, 215, 0), (255, 140, 0), (220, 20, 60),
        (65, 105, 225), (148, 0, 211)
    ]
    crayon_positions = [
        (cx + page_w // 2 + 50, cy - 200, 15),
        (cx + page_w // 2 + 100, cy - 100, -10),
        (cx + page_w // 2 + 70, cy + 50, 20),
        (cx - page_w // 2 - 100, cy + 300, -25),
        (cx + page_w // 2 + 130, cy + 200, 5),
        (cx - page_w // 2 - 60, cy - 100, 30),
    ]
    for color, (crx, cry, angle) in zip(crayon_colors, crayon_positions):
        # simple crayon shape
        cw, ch = 25, 160
        draw.rectangle([crx, cry, crx + cw, cry + ch], fill=color)
        draw.rectangle([crx + 2, cry, crx + cw - 2, cry + 25], fill=(220, 200, 180))
        draw.polygon([(crx, cry + ch), (crx + cw, cry + ch), (crx + cw // 2, cry + ch + 20)], fill=color)

    # Child's hand (simplified - oval shape holding green crayon)
    hand_cx, hand_cy = cx + 80, cy + 120
    # arm
    draw.ellipse([hand_cx - 50, hand_cy - 30, hand_cx + 60, hand_cy + 60], fill=(240, 200, 170))
    # fingers
    for fx, fy in [(hand_cx - 20, hand_cy - 20), (hand_cx, hand_cy - 30), (hand_cx + 20, hand_cy - 25)]:
        draw.ellipse([fx - 12, fy - 10, fx + 12, fy + 15], fill=(240, 200, 170))
    # green crayon in hand
    draw.rectangle([hand_cx - 8, hand_cy - 45, hand_cx + 8, hand_cy + 5], fill=BRIGHT_GREEN)
    draw.polygon([(hand_cx - 8, hand_cy - 45), (hand_cx + 8, hand_cy - 45), (hand_cx, hand_cy - 60)], fill=BRIGHT_GREEN)

    # Overlay text
    overlay_h = 200
    draw.rectangle([0, H - overlay_h, W, H], fill=DARK_GREEN)
    draw.rectangle([0, H - overlay_h, W, H - overlay_h + 6], fill=GOLD)
    of = get_font(56, bold=True)
    sf = get_font(38)
    draw_text_centered(draw, "St. Patrick's Day Kids Activity Bundle", H - overlay_h + 40, of, WHITE, W)
    draw_text_centered(draw, "Printable Coloring Pages & Activities  •  Instant Download", H - overlay_h + 120, sf, LIGHT_GOLD, W)

    add_watermark(draw, W, H - overlay_h)
    img.save(os.path.join(OUTPUT_DIR, "listing1-lifestyle.png"), "PNG", quality=95)
    print("  ✓ listing1-lifestyle.png")


def listing1_sample_preview():
    """Image 5: Close-up preview of 2-3 sample pages from the bundle."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H))
    gradient_bg(img, PALE_GREEN, WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    hf = get_font(76, bold=True)
    sf = get_font(44)
    draw_text_with_shadow(draw, "SAMPLE PAGES PREVIEW", 60, hf, DARK_GREEN, W, (180, 220, 180))
    draw_text_centered(draw, "Here's a sneak peek at what you'll get!", 160, sf, DARK_GRAY, W)

    # Gold divider
    draw.rectangle([W // 2 - 300, 230, W // 2 + 300, 235], fill=GOLD)

    # Three overlapping pages, fanned out - taller to fill space
    page_specs = [
        {"x": 150, "y": 300, "w": 680, "h": 1100, "title": "Shamrock Coloring",
         "type": "coloring", "bg": WHITE},
        {"x": 660, "y": 260, "w": 680, "h": 1100, "title": "Word Search Puzzle",
         "type": "puzzle", "bg": WHITE},
        {"x": 1170, "y": 320, "w": 680, "h": 1100, "title": "Maze Activity",
         "type": "maze", "bg": WHITE},
    ]

    pf = get_font(32, bold=True)
    small_f = get_font(22)

    for spec in page_specs:
        x, y, pw, ph = spec["x"], spec["y"], spec["w"], spec["h"]
        # Shadow
        draw.rectangle([x + 8, y + 8, x + pw + 8, y + ph + 8], fill=(190, 190, 190))
        # Page
        draw.rectangle([x, y, x + pw, y + ph], fill=spec["bg"], outline=MEDIUM_GRAY, width=2)
        # Green header bar
        draw.rectangle([x + 10, y + 10, x + pw - 10, y + 80], fill=DARK_GREEN)
        tb = draw.textbbox((0, 0), spec["title"], font=pf)
        tw = tb[2] - tb[0]
        draw.text((x + (pw - tw) // 2, y + 25), spec["title"], font=pf, fill=WHITE)

        cx = x + pw // 2
        cy = y + ph // 2 + 30

        if spec["type"] == "coloring":
            # Big shamrock with outline
            draw_shamrock(draw, cx, cy - 30, 160, PALE_GREEN)
            # Outline circles for coloring effect
            r = 53
            for ox, oy in [(0, -53), (-46, 26), (46, 26)]:
                draw.ellipse([cx + int(ox) - r, cy - 30 + int(oy) - r,
                              cx + int(ox) + r, cy - 30 + int(oy) + r], outline=DARK_GREEN, width=3)
            draw.rectangle([cx - 4, cy + 10, cx + 4, cy + 130], outline=DARK_GREEN, width=3)
            draw.text((x + 30, y + ph - 60), "Color me in!", font=small_f, fill=MEDIUM_GRAY)

        elif spec["type"] == "puzzle":
            # Word search grid
            grid_x, grid_y = x + 60, y + 110
            cell = 52
            letters = "SHAMROCKLUCKYGOLDIRISH"
            idx = 0
            letter_font = get_font(28)
            for row in range(10):
                for col in range(10):
                    lx = grid_x + col * cell
                    ly = grid_y + row * cell
                    draw.rectangle([lx, ly, lx + cell, ly + cell], outline=LIGHT_GRAY, width=1)
                    letter = letters[idx % len(letters)]
                    idx += 1
                    lb = draw.textbbox((0, 0), letter, font=letter_font)
                    lw = lb[2] - lb[0]
                    draw.text((lx + (cell - lw) // 2, ly + 10), letter, font=letter_font, fill=DARK_GRAY)
            # Highlight a word
            draw.rectangle([grid_x, grid_y, grid_x + 8 * cell, grid_y + cell],
                           outline=BRIGHT_GREEN, width=3)
            # Word list at bottom
            draw.text((x + 30, y + ph - 100), "Find: SHAMROCK, LUCKY,", font=small_f, fill=DARK_GREEN)
            draw.text((x + 30, y + ph - 60), "GOLD, IRISH, CLOVER", font=small_f, fill=DARK_GREEN)

        elif spec["type"] == "maze":
            # Simple maze representation
            maze_x, maze_y = x + 80, y + 120
            mw, mh = pw - 160, ph - 220
            draw.rectangle([maze_x, maze_y, maze_x + mw, maze_y + mh], outline=DARK_GREEN, width=3)
            # maze internal walls
            walls = [
                (maze_x + mw // 4, maze_y, maze_x + mw // 4, maze_y + mh * 2 // 3),
                (maze_x + mw // 2, maze_y + mh // 3, maze_x + mw // 2, maze_y + mh),
                (maze_x + mw * 3 // 4, maze_y, maze_x + mw * 3 // 4, maze_y + mh * 3 // 4),
                (maze_x, maze_y + mh // 3, maze_x + mw // 3, maze_y + mh // 3),
                (maze_x + mw * 2 // 3, maze_y + mh * 2 // 3, maze_x + mw, maze_y + mh * 2 // 3),
            ]
            for wx1, wy1, wx2, wy2 in walls:
                draw.line([(wx1, wy1), (wx2, wy2)], fill=DARK_GREEN, width=3)
            # Start & end
            draw.text((maze_x - 10, maze_y - 30), "START →", font=small_f, fill=BRIGHT_GREEN)
            draw_shamrock(draw, maze_x + mw - 30, maze_y + mh - 30, 30, BRIGHT_GREEN)
            draw.text((maze_x + mw + 5, maze_y + mh - 20), "← END", font=small_f, fill=BRIGHT_GREEN)

    # Bottom bar
    draw.rectangle([0, H - 180, W, H], fill=DARK_GREEN)
    draw.rectangle([0, H - 180, W, H - 174], fill=GOLD)
    bf = get_font(50, bold=True)
    sf2 = get_font(36)
    draw_text_centered(draw, "St. Patrick's Day Kids Activity Bundle", H - 160, bf, WHITE, W)
    draw_text_centered(draw, "10+ Pages of Coloring, Games & Activities  •  $6.99", H - 90, sf2, LIGHT_GOLD, W)

    add_watermark(draw, W, H - 180)
    img.save(os.path.join(OUTPUT_DIR, "listing1-sample-preview.png"), "PNG", quality=95)
    print("  ✓ listing1-sample-preview.png")


# ══════════════════════════════════════════════════════════════════
# LISTING 2: St. Patrick's Day Social Media Templates ($11.99)
# ══════════════════════════════════════════════════════════════════

def listing2_cover():
    """Image 1: Professional cover image with green/gold branding."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H))
    # Deep green to dark green gradient
    gradient_bg(img, (18, 75, 35), (10, 50, 22))
    draw = ImageDraw.Draw(img)

    # Subtle geometric pattern overlay
    random.seed(22)
    for _ in range(50):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(20, 60)
        draw.rectangle([x, y, x + s, y + s], outline=(25, 85, 40), width=1)

    # Gold decorative lines at top and bottom
    for offset in [0, 8]:
        draw.line([(0, 30 + offset), (W, 30 + offset)], fill=GOLD, width=3)
        draw.line([(0, H - 30 - offset), (W, H - 30 - offset)], fill=GOLD, width=3)

    # Central panel - tighter fit around content
    panel_margin = 140
    panel_y1, panel_y2 = 120, H - 120
    draw_rounded_rect(draw, [panel_margin, panel_y1, W - panel_margin, panel_y2], 30,
                      fill=(255, 255, 255, 240))
    # inner gold frame
    draw_rounded_rect(draw, [panel_margin + 8, panel_y1 + 8, W - panel_margin - 8, panel_y2 - 8],
                      26, outline=GOLD, width=4)

    # Content on panel - larger fonts, better spacing
    y = panel_y1 + 80
    tag_font = get_font(42)
    draw_text_centered(draw, "✦  SOCIAL MEDIA TEMPLATES  ✦", y, tag_font, GOLD, W)

    y += 100
    title_font = get_font(110, bold=True)
    draw_text_centered(draw, "ST. PATRICK'S", y, title_font, DARK_GREEN, W)
    y += 130
    draw_text_centered(draw, "DAY", y, title_font, DARK_GREEN, W)

    y += 150
    # Gold divider with shamrock
    draw.rectangle([W // 2 - 300, y, W // 2 + 300, y + 5], fill=GOLD)
    draw_shamrock(draw, W // 2, y, 35, DARK_GREEN)

    y += 70
    sub_font = get_font(60, bold=True)
    draw_text_centered(draw, "SMALL BUSINESS", y, sub_font, MEDIUM_GREEN, W)
    y += 80
    draw_text_centered(draw, "MARKETING PACK", y, sub_font, MEDIUM_GREEN, W)

    y += 110
    detail_font = get_font(44)
    details = [
        "Instagram Posts & Stories",
        "Facebook Templates",
        "Editable in Canva",
        "Instant Download",
    ]
    for d in details:
        draw_text_centered(draw, f"●  {d}", y, detail_font, DARK_GRAY, W)
        y += 65

    y += 40
    # Price badge
    badge_w, badge_h = 380, 120
    bx = W // 2 - badge_w // 2
    draw_rounded_rect(draw, [bx, y, bx + badge_w, y + badge_h], 20, fill=GOLD)
    price_font = get_font(72, bold=True)
    draw_text_centered(draw, "$11.99", y + 20, price_font, WHITE, W)

    # Canva badge
    y += badge_h + 40
    canva_font = get_font(40, bold=True)
    draw_text_centered(draw, "FULLY EDITABLE IN CANVA", y, canva_font, GOLD, W)

    # Additional content to fill space
    y += 80
    draw.rectangle([W // 2 - 200, y, W // 2 + 200, y + 3], fill=LIGHT_GREEN)
    y += 40
    extra_font = get_font(38)
    extras = [
        "Works with FREE Canva account",
        "No design skills needed",
        "Customize colors, text & images",
        "Print or post digitally",
    ]
    for ex in extras:
        draw_text_centered(draw, f"✓  {ex}", y, extra_font, DARK_GRAY, W)
        y += 60

    # Decorative shamrock trio at bottom of panel
    y += 30
    draw_shamrock(draw, W // 2 - 100, y, 45, LIGHT_GREEN)
    draw_shamrock(draw, W // 2, y - 15, 55, BRIGHT_GREEN)
    draw_shamrock(draw, W // 2 + 100, y, 45, LIGHT_GREEN)

    # Decorative shamrocks on panel edges
    for sy in range(panel_y1 + 100, panel_y2 - 100, 200):
        draw_shamrock(draw, panel_margin + 50, sy, 25, LIGHT_GREEN)
        draw_shamrock(draw, W - panel_margin - 50, sy, 25, LIGHT_GREEN)

    # Corner decorations
    draw_star(draw, 80, 80, 25, GOLD)
    draw_star(draw, W - 80, 80, 25, GOLD)
    draw_star(draw, 80, H - 80, 25, GOLD)
    draw_star(draw, W - 80, H - 80, 25, GOLD)

    add_watermark(draw, W, H)
    img.save(os.path.join(OUTPUT_DIR, "listing2-cover.png"), "PNG", quality=95)
    print("  ✓ listing2-cover.png")


def listing2_grid_mockup():
    """Image 2: Grid mockup showing multiple template designs."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H), OFF_WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 180], fill=DARK_GREEN)
    hf = get_font(60, bold=True)
    draw_text_centered(draw, "TEMPLATE DESIGNS INCLUDED", 50, hf, WHITE, W)
    sf = get_font(34)
    draw_text_centered(draw, "Fully Editable in Canva  •  Instagram, Facebook & More", 130, sf, LIGHT_GOLD, W)

    # Grid of 9 template thumbnails (3x3)
    grid_start_y = 240
    margin = 60
    gap = 40
    cols, rows = 3, 3
    cell_w = (W - 2 * margin - (cols - 1) * gap) // cols
    cell_h = (H - grid_start_y - 200 - (rows - 1) * gap) // rows

    templates = [
        {"title": "SALE POST", "type": "sale", "color": DARK_GREEN},
        {"title": "STORY\nTEMPLATE", "type": "story", "color": MEDIUM_GREEN},
        {"title": "PROMO\nBANNER", "type": "promo", "color": BRIGHT_GREEN},
        {"title": "QUOTE\nPOST", "type": "quote", "color": GOLD},
        {"title": "EVENT\nANNOUNCE", "type": "event", "color": DARK_GREEN},
        {"title": "PRODUCT\nFEATURE", "type": "product", "color": MEDIUM_GREEN},
        {"title": "HOLIDAY\nGREETING", "type": "greeting", "color": BRIGHT_GREEN},
        {"title": "FLASH\nSALE", "type": "flash", "color": GOLD},
        {"title": "THANK\nYOU", "type": "thanks", "color": DARK_GREEN},
    ]

    tf = get_font(36, bold=True)
    label_f = get_font(24)

    for idx, tmpl in enumerate(templates):
        row = idx // cols
        col = idx % cols
        x = margin + col * (cell_w + gap)
        y = grid_start_y + row * (cell_h + gap)

        # Template card shadow
        draw.rectangle([x + 5, y + 5, x + cell_w + 5, y + cell_h + 5], fill=(200, 200, 200))
        # Template card
        draw.rectangle([x, y, x + cell_w, y + cell_h], fill=tmpl["color"])

        # Inner design elements
        inner_margin = 25
        ix1, iy1 = x + inner_margin, y + inner_margin
        ix2, iy2 = x + cell_w - inner_margin, y + cell_h - inner_margin

        # Gold border inside
        draw.rectangle([ix1, iy1, ix2, iy2], outline=GOLD, width=3)

        # Shamrock decoration
        draw_shamrock(draw, x + cell_w // 2, y + cell_h // 3, 40, LIGHT_GREEN)

        # Title text
        for i, line in enumerate(tmpl["title"].split("\n")):
            tb = draw.textbbox((0, 0), line, font=tf)
            tw = tb[2] - tb[0]
            th = tb[3] - tb[1]
            ly = y + cell_h // 2 + i * (th + 10)
            draw.text((x + (cell_w - tw) // 2, ly), line, font=tf, fill=WHITE)

        # Small "Canva" label
        draw.text((x + cell_w - 80, y + cell_h - 35), "CANVA", font=label_f, fill=LIGHT_GOLD)

    # Bottom bar
    draw.rectangle([0, H - 140, W, H], fill=DARK_GREEN)
    bf = get_font(44, bold=True)
    draw_text_centered(draw, "9+ TEMPLATES  •  EDITABLE IN CANVA  •  $11.99", H - 100, bf, WHITE, W)

    add_watermark(draw, W, H - 140)
    img.save(os.path.join(OUTPUT_DIR, "listing2-template-grid.png"), "PNG", quality=95)
    print("  ✓ listing2-template-grid.png")


def listing2_device_mockup():
    """Image 3: Phone/laptop mockup displaying one of the templates."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H))
    gradient_bg(img, PALE_GREEN, WHITE)
    draw = ImageDraw.Draw(img)

    # Header text
    hf = get_font(64, bold=True)
    sf = get_font(40)
    draw_text_centered(draw, "LOOKS GREAT ON EVERY DEVICE", 80, hf, DARK_GREEN, W)
    draw_text_centered(draw, "Edit in Canva, post anywhere!", 170, sf, DARK_GRAY, W)

    # --- Laptop mockup (left-center) - larger ---
    laptop_cx, laptop_cy = 680, 750
    laptop_sw, laptop_sh = 780, 520
    sx1, sy1, sx2, sy2 = draw_laptop_mockup(draw, laptop_cx, laptop_cy, laptop_sw, laptop_sh)

    # Content on laptop screen - a social media post preview
    draw.rectangle([sx1, sy1, sx2, sy2], fill=DARK_GREEN)
    # Gold border
    draw.rectangle([sx1 + 10, sy1 + 10, sx2 - 10, sy2 - 10], outline=GOLD, width=3)
    scr_f = get_font(40, bold=True)
    scr_sf = get_font(28)
    draw_shamrock(draw, laptop_cx, sy1 + 90, 60, LIGHT_GREEN)
    draw.text((sx1 + 80, sy1 + 180), "ST. PATRICK'S DAY", font=scr_f, fill=WHITE)
    draw.text((sx1 + 80, sy1 + 230), "SPECIAL SALE", font=scr_f, fill=BRIGHT_GOLD)
    draw.text((sx1 + 80, sy1 + 300), "20% OFF ALL ITEMS", font=scr_sf, fill=WHITE)
    draw.text((sx1 + 80, sy1 + 340), "Use code: LUCKY2026", font=scr_sf, fill=LIGHT_GOLD)

    # --- Phone mockup (right) - larger ---
    phone_cx, phone_cy = 1480, 800
    phone_sw, phone_sh = 400, 720
    px1, py1, px2, py2 = draw_phone_mockup(draw, phone_cx, phone_cy, phone_sw, phone_sh)

    # Content on phone screen - Instagram story style
    draw.rectangle([px1, py1, px2, py2], fill=MEDIUM_GREEN)
    draw.rectangle([px1 + 8, py1 + 8, px2 - 8, py2 - 8], outline=GOLD, width=3)
    draw_shamrock(draw, phone_cx, py1 + 140, 80, LIGHT_GREEN)
    ph_f = get_font(38, bold=True)
    ph_sf = get_font(26)
    draw.text((px1 + 40, py1 + 280), "HAPPY", font=ph_f, fill=WHITE)
    draw.text((px1 + 40, py1 + 330), "ST. PATRICK'S", font=ph_f, fill=WHITE)
    draw.text((px1 + 40, py1 + 380), "DAY!", font=ph_f, fill=BRIGHT_GOLD)
    draw.text((px1 + 40, py1 + 450), "Swipe up for deals", font=ph_sf, fill=LIGHT_GOLD)
    # Swipe up arrow
    arrow_cx = phone_cx
    arrow_y = py2 - 80
    draw.polygon([(arrow_cx - 20, arrow_y + 15), (arrow_cx + 20, arrow_y + 15),
                   (arrow_cx, arrow_y - 15)], fill=WHITE)
    draw.line([(arrow_cx, arrow_y + 15), (arrow_cx, arrow_y + 40)], fill=WHITE, width=4)

    # Decorative elements
    for sx, sy in [(200, 500), (W - 200, 500), (200, 1300), (W - 200, 1300)]:
        draw_shamrock(draw, sx, sy, 50, LIGHT_GREEN)
    for sx, sy in [(300, 300), (W - 300, 300), (W // 2, 1500)]:
        draw_star(draw, sx, sy, 20, GOLD)

    # Bottom section - taller to fill space
    draw.rectangle([0, H - 400, W, H], fill=DARK_GREEN)
    draw.rectangle([0, H - 400, W, H - 394], fill=GOLD)

    # Feature badges
    badge_font = get_font(38, bold=True)
    badges = ["Instagram Posts", "Stories", "Facebook", "Pinterest"]
    badge_w = 390
    total_w = len(badges) * badge_w + (len(badges) - 1) * 30
    start_x = (W - total_w) // 2
    for i, badge in enumerate(badges):
        bx = start_x + i * (badge_w + 30)
        by = H - 350
        draw_rounded_rect(draw, [bx, by, bx + badge_w, by + 80], 15, fill=GOLD)
        tb = draw.textbbox((0, 0), badge, font=badge_font)
        tw = tb[2] - tb[0]
        draw.text((bx + (badge_w - tw) // 2, by + 18), badge, font=badge_font, fill=DARK_GREEN)

    bf = get_font(52, bold=True)
    draw_text_centered(draw, "St. Patrick's Day Social Media Templates", H - 220, bf, WHITE, W)
    sf2 = get_font(38)
    draw_text_centered(draw, "Editable in Canva  •  Instant Download  •  $11.99", H - 140, sf2, LIGHT_GOLD, W)
    # Extra decorative shamrocks
    draw_shamrock(draw, 100, H - 80, 40, LIGHT_GREEN)
    draw_shamrock(draw, W - 100, H - 80, 40, LIGHT_GREEN)

    add_watermark(draw, W, H - 400)
    img.save(os.path.join(OUTPUT_DIR, "listing2-device-mockup.png"), "PNG", quality=95)
    print("  ✓ listing2-device-mockup.png")


def listing2_whats_included():
    """Image 4: What's Included graphic for social media templates."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Elegant border
    draw_decorative_border(draw, W, H, 10, DARK_GREEN)

    # Header
    draw.rectangle([20, 20, W - 20, 340], fill=DARK_GREEN)
    hf = get_font(82, bold=True)
    draw_text_centered(draw, "WHAT'S INCLUDED", 60, hf, WHITE, W)
    sf = get_font(44)
    draw_text_centered(draw, "St. Patrick's Day Social Media Templates", 175, sf, LIGHT_GOLD, W)
    draw_text_centered(draw, "For Small Business Marketing", 235, sf, LIGHT_GREEN, W)
    # Decorative shamrocks
    draw_shamrock(draw, 100, 80, 45, LIGHT_GREEN)
    draw_shamrock(draw, W - 100, 80, 45, LIGHT_GREEN)

    # Main content - two columns
    items_left = [
        ("9+ Template Designs", "Instagram posts, stories, & more"),
        ("Editable in Canva", "Easy drag-and-drop editing"),
        ("St. Patrick's Theme", "Green & gold festive branding"),
    ]
    items_right = [
        ("Multiple Sizes", "Square, portrait & landscape"),
        ("Instant Download", "PDF with Canva template links"),
        ("Commercial Use", "Perfect for your business"),
    ]

    item_font = get_font(46, bold=True)
    desc_font = get_font(34)
    col_width = (W - 160) // 2

    y_start = 420
    item_height = 200

    for i, (title, desc) in enumerate(items_left):
        y = y_start + i * item_height
        x = 80
        # Background card
        if i % 2 == 0:
            draw_rounded_rect(draw, [x, y, x + col_width - 20, y + item_height - 20], 15, fill=PALE_GREEN)
        else:
            draw_rounded_rect(draw, [x, y, x + col_width - 20, y + item_height - 20], 15, fill=CREAM)
        # Number badge
        num_font = get_font(44, bold=True)
        draw.ellipse([x + 20, y + 30, x + 80, y + 90], fill=GOLD)
        nb = draw.textbbox((0, 0), str(i + 1), font=num_font)
        nw = nb[2] - nb[0]
        draw.text((x + 50 - nw // 2, y + 38), str(i + 1), font=num_font, fill=WHITE)
        # Text
        draw.text((x + 100, y + 30), title, font=item_font, fill=DARK_GREEN)
        draw.text((x + 100, y + 90), desc, font=desc_font, fill=DARK_GRAY)

    for i, (title, desc) in enumerate(items_right):
        y = y_start + i * item_height
        x = 80 + col_width
        if i % 2 == 0:
            draw_rounded_rect(draw, [x, y, x + col_width - 20, y + item_height - 20], 15, fill=CREAM)
        else:
            draw_rounded_rect(draw, [x, y, x + col_width - 20, y + item_height - 20], 15, fill=PALE_GREEN)
        num_font = get_font(44, bold=True)
        draw.ellipse([x + 20, y + 30, x + 80, y + 90], fill=GOLD)
        nb = draw.textbbox((0, 0), str(i + 4), font=num_font)
        nw = nb[2] - nb[0]
        draw.text((x + 50 - nw // 2, y + 38), str(i + 4), font=num_font, fill=WHITE)
        draw.text((x + 100, y + 30), title, font=item_font, fill=DARK_GREEN)
        draw.text((x + 100, y + 90), desc, font=desc_font, fill=DARK_GRAY)

    # How it works section
    how_y = y_start + 3 * item_height + 40
    draw.rectangle([60, how_y, W - 60, how_y + 5], fill=GOLD)
    how_y += 30
    how_font = get_font(54, bold=True)
    draw_text_centered(draw, "HOW IT WORKS", how_y, how_font, DARK_GREEN, W)
    how_y += 80

    steps = [
        ("1. Purchase", "Instant download"),
        ("2. Open in Canva", "Click template link"),
        ("3. Customize", "Add your brand info"),
        ("4. Post!", "Share on social media"),
    ]
    step_font = get_font(38, bold=True)
    step_desc_font = get_font(30)
    step_w = (W - 160) // 4
    for i, (step, desc) in enumerate(steps):
        sx = 80 + i * step_w
        # Arrow between steps
        if i > 0:
            draw.polygon([(sx - 15, how_y + 40), (sx + 5, how_y + 55), (sx - 15, how_y + 70)], fill=GOLD)
        # Circle
        draw.ellipse([sx + step_w // 2 - 35, how_y, sx + step_w // 2 + 35, how_y + 70], fill=DARK_GREEN)
        nb = draw.textbbox((0, 0), str(i + 1), font=step_font)
        nw = nb[2] - nb[0]
        draw.text((sx + step_w // 2 - nw // 2, how_y + 10), str(i + 1), font=step_font, fill=WHITE)
        # Text
        sb = draw.textbbox((0, 0), step.split(". ")[1], font=step_font)
        stw = sb[2] - sb[0]
        draw.text((sx + (step_w - stw) // 2, how_y + 85), step.split(". ")[1], font=step_font, fill=DARK_GREEN)
        db = draw.textbbox((0, 0), desc, font=step_desc_font)
        dw = db[2] - db[0]
        draw.text((sx + (step_w - dw) // 2, how_y + 130), desc, font=step_desc_font, fill=DARK_GRAY)

    # Bottom price banner
    draw_rounded_rect(draw, [100, H - 200, W - 100, H - 60], 25, fill=GOLD)
    bf = get_font(56, bold=True)
    draw_text_centered(draw, "ONLY $11.99  •  INSTANT DOWNLOAD", H - 170, bf, WHITE, W)

    add_watermark(draw, W, H)
    img.save(os.path.join(OUTPUT_DIR, "listing2-whats-included.png"), "PNG", quality=95)
    print("  ✓ listing2-whats-included.png")


def listing2_before_after():
    """Image 5: Before/after example showing blank template vs styled post."""
    W, H = 2000, 2000
    img = Image.new("RGB", (W, H))
    gradient_bg(img, WHITE, PALE_GREEN)
    draw = ImageDraw.Draw(img)

    # Header
    hf = get_font(72, bold=True)
    sf = get_font(42)
    draw_text_centered(draw, "BEFORE & AFTER", 60, hf, DARK_GREEN, W)
    draw_text_centered(draw, "See how easy it is to customize these templates!", 155, sf, DARK_GRAY, W)
    draw.rectangle([W // 2 - 300, 220, W // 2 + 300, 225], fill=GOLD)

    # --- BEFORE (left side) ---
    before_cx = W // 4 + 40
    before_y = 320
    pw, ph = 700, 700

    # "BEFORE" label
    label_font = get_font(48, bold=True)
    tb = draw.textbbox((0, 0), "BEFORE", font=label_font)
    tw = tb[2] - tb[0]
    draw.text((before_cx - tw // 2, before_y - 10), "BEFORE", font=label_font, fill=MEDIUM_GRAY)

    before_y += 60
    # Template card shadow
    draw.rectangle([before_cx - pw // 2 + 6, before_y + 6,
                     before_cx + pw // 2 + 6, before_y + ph + 6], fill=(200, 200, 200))
    # Template card - plain/blank version
    draw.rectangle([before_cx - pw // 2, before_y,
                     before_cx + pw // 2, before_y + ph], fill=DARK_GREEN)
    draw.rectangle([before_cx - pw // 2 + 12, before_y + 12,
                     before_cx + pw // 2 - 12, before_y + ph - 12], outline=GOLD, width=3)

    # Placeholder content
    pl_font = get_font(40, bold=True)
    pl_sf = get_font(28)
    draw_shamrock(draw, before_cx, before_y + 150, 80, LIGHT_GREEN)
    draw.text((before_cx - 160, before_y + 300), "[YOUR HEADLINE", font=pl_font, fill=WHITE)
    draw.text((before_cx - 100, before_y + 350), "GOES HERE]", font=pl_font, fill=WHITE)
    draw.text((before_cx - 140, before_y + 420), "[Your description text]", font=pl_sf, fill=LIGHT_GREEN)
    draw.text((before_cx - 100, before_y + 470), "[Your CTA button]", font=pl_sf, fill=LIGHT_GOLD)
    # Placeholder image area
    draw.rectangle([before_cx - 120, before_y + 530, before_cx + 120, before_y + 630],
                    outline=MEDIUM_GRAY, width=2)
    draw.text((before_cx - 80, before_y + 560), "[Your Logo]", font=pl_sf, fill=MEDIUM_GRAY)

    # --- Arrow between ---
    arrow_cx = W // 2
    arrow_cy = before_y + ph // 2
    # Arrow body
    draw_rounded_rect(draw, [arrow_cx - 60, arrow_cy - 30, arrow_cx + 40, arrow_cy + 30], 10, fill=GOLD)
    # Arrow head
    draw.polygon([(arrow_cx + 40, arrow_cy - 50), (arrow_cx + 90, arrow_cy),
                   (arrow_cx + 40, arrow_cy + 50)], fill=GOLD)

    # --- AFTER (right side) ---
    after_cx = W * 3 // 4 - 40
    after_y = 320

    tb = draw.textbbox((0, 0), "AFTER", font=label_font)
    tw = tb[2] - tb[0]
    draw.text((after_cx - tw // 2, after_y - 10), "AFTER", font=label_font, fill=BRIGHT_GREEN)

    after_y += 60
    # Styled template shadow
    draw.rectangle([after_cx - pw // 2 + 6, after_y + 6,
                     after_cx + pw // 2 + 6, after_y + ph + 6], fill=(200, 200, 200))
    # Styled template card
    draw.rectangle([after_cx - pw // 2, after_y,
                     after_cx + pw // 2, after_y + ph], fill=DARK_GREEN)
    draw.rectangle([after_cx - pw // 2 + 12, after_y + 12,
                     after_cx + pw // 2 - 12, after_y + ph - 12], outline=GOLD, width=3)

    # Filled-in content
    styled_font = get_font(44, bold=True)
    styled_sf = get_font(30)
    styled_small = get_font(24)

    draw_shamrock(draw, after_cx, after_y + 130, 70, BRIGHT_GREEN)
    draw_star(draw, after_cx - 100, after_y + 90, 15, BRIGHT_GOLD)
    draw_star(draw, after_cx + 100, after_y + 90, 15, BRIGHT_GOLD)

    draw.text((after_cx - 200, after_y + 260), "ST. PATRICK'S DAY", font=styled_font, fill=WHITE)
    draw.text((after_cx - 130, after_y + 315), "FLASH SALE!", font=styled_font, fill=BRIGHT_GOLD)
    draw.text((after_cx - 170, after_y + 390), "Save 25% on everything", font=styled_sf, fill=LIGHT_GREEN)
    draw.text((after_cx - 140, after_y + 435), "Code: LUCKY25", font=styled_sf, fill=LIGHT_GOLD)

    # CTA button
    btn_w, btn_h = 280, 60
    draw_rounded_rect(draw, [after_cx - btn_w // 2, after_y + 500,
                              after_cx + btn_w // 2, after_y + 500 + btn_h], 15, fill=GOLD)
    btn_font = get_font(30, bold=True)
    tb = draw.textbbox((0, 0), "SHOP NOW", font=btn_font)
    btw = tb[2] - tb[0]
    draw.text((after_cx - btw // 2, after_y + 512), "SHOP NOW", font=btn_font, fill=DARK_GREEN)

    # Logo area
    draw.ellipse([after_cx - 40, after_y + 600, after_cx + 40, after_y + 660], fill=GOLD)
    logo_f = get_font(20, bold=True)
    draw.text((after_cx - 25, after_y + 618), "LOGO", font=logo_f, fill=DARK_GREEN)

    # "Just 5 minutes!" callout
    callout_y = after_y + ph + 20
    callout_font = get_font(36, bold=True)
    tb = draw.textbbox((0, 0), "Customized in just 5 minutes!", font=callout_font)
    tw = tb[2] - tb[0]
    draw.text((after_cx - tw // 2, callout_y), "Customized in just 5 minutes!", font=callout_font, fill=BRIGHT_GREEN)

    # Bottom section
    bottom_y = H - 380
    draw.rectangle([0, bottom_y, W, H], fill=DARK_GREEN)
    draw.rectangle([0, bottom_y, W, bottom_y + 6], fill=GOLD)

    bf = get_font(52, bold=True)
    draw_text_centered(draw, "IT'S THAT EASY!", bottom_y + 40, bf, WHITE, W)

    steps_y = bottom_y + 120
    step_font = get_font(38, bold=True)
    step_desc = get_font(30)
    step_items = [
        ("1", "Open in Canva"),
        ("2", "Add Your Info"),
        ("3", "Download & Post"),
    ]
    step_w = W // 3
    for i, (num, text) in enumerate(step_items):
        sx = i * step_w + step_w // 2
        draw.ellipse([sx - 30, steps_y, sx + 30, steps_y + 60], fill=GOLD)
        nb = draw.textbbox((0, 0), num, font=step_font)
        nw = nb[2] - nb[0]
        draw.text((sx - nw // 2, steps_y + 8), num, font=step_font, fill=DARK_GREEN)
        tb = draw.textbbox((0, 0), text, font=step_desc)
        tw = tb[2] - tb[0]
        draw.text((sx - tw // 2, steps_y + 75), text, font=step_desc, fill=WHITE)

    price_y = H - 90
    pf = get_font(42, bold=True)
    draw_text_centered(draw, "St. Patrick's Day Social Media Templates  •  $11.99", price_y, pf, LIGHT_GOLD, W)

    add_watermark(draw, W, H - 380)
    img.save(os.path.join(OUTPUT_DIR, "listing2-before-after.png"), "PNG", quality=95)
    print("  ✓ listing2-before-after.png")


# ══════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🍀 Generating Etsy Listing Images for ShelzysDesignsStore\n")
    print("=" * 55)

    print("\n📦 Listing 1: Kids Activity Bundle")
    listing1_cover()
    listing1_whats_included()
    listing1_coloring_pages_mockup()
    listing1_lifestyle()
    listing1_sample_preview()

    print("\n📱 Listing 2: Social Media Templates")
    listing2_cover()
    listing2_grid_mockup()
    listing2_device_mockup()
    listing2_whats_included()
    listing2_before_after()

    print("\n" + "=" * 55)
    print(f"✅ All 10 images saved to: {OUTPUT_DIR}/")
    print("=" * 55)
