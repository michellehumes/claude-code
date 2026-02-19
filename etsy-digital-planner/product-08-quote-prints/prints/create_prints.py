#!/usr/bin/env python3
"""
Motivational Quote Wall Art Prints Bundle
Generates 30 unique motivational/inspirational quote art prints at 2400x3000px.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
import random

# Output directory
OUT = os.path.dirname(os.path.abspath(__file__))

# Canvas size (4:5 ratio for 8x10 / 16x20)
W, H = 2400, 3000

# Color palette
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
SOFT_PINK = (245, 228, 228)
WARM_BEIGE = (240, 230, 210)
DARK_SAGE = (100, 140, 95)
LIGHT_GOLD = (230, 210, 170)
DEEP_PLUM = (90, 50, 80)
SOFT_SKY = (200, 225, 245)
WARM_CREAM = (250, 240, 225)


def get_font(size, bold=False):
    """Get a font at the given size."""
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


def get_font_light(size):
    """Get a lighter font."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_gradient(img, color1, color2, vertical=True):
    """Draw a gradient on the image."""
    draw = ImageDraw.Draw(img)
    for i in range(H if vertical else W):
        ratio = i / (H if vertical else W)
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        if vertical:
            draw.line([(0, i), (W, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, H)], fill=(r, g, b))
    return draw


def draw_radial_gradient(img, center_color, edge_color):
    """Draw a radial gradient."""
    draw = ImageDraw.Draw(img)
    cx, cy = W // 2, H // 2
    max_r = math.sqrt(cx**2 + cy**2)
    # Fill with edge color first
    draw.rectangle([0, 0, W, H], fill=edge_color)
    steps = 200
    for i in range(steps, 0, -1):
        ratio = i / steps
        r_val = int(edge_color[0] + (center_color[0] - edge_color[0]) * (1 - ratio))
        g_val = int(edge_color[1] + (center_color[1] - edge_color[1]) * (1 - ratio))
        b_val = int(edge_color[2] + (center_color[2] - edge_color[2]) * (1 - ratio))
        rad = int(max_r * ratio)
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(r_val, g_val, b_val))
    return draw


def draw_thin_border(draw, margin=60, color=GOLD, width=3):
    """Draw a thin decorative border."""
    draw.rectangle([margin, margin, W - margin, H - margin], outline=color, width=width)


def draw_double_border(draw, margin=50, color=GOLD, width=2):
    """Draw a double-line border."""
    draw.rectangle([margin, margin, W - margin, H - margin], outline=color, width=width)
    draw.rectangle([margin + 15, margin + 15, W - margin - 15, H - margin - 15], outline=color, width=width)


def draw_corner_accents(draw, color=GOLD, size=120, margin=80, width=3):
    """Draw corner accent lines."""
    # Top-left
    draw.line([(margin, margin), (margin + size, margin)], fill=color, width=width)
    draw.line([(margin, margin), (margin, margin + size)], fill=color, width=width)
    # Top-right
    draw.line([(W - margin - size, margin), (W - margin, margin)], fill=color, width=width)
    draw.line([(W - margin, margin), (W - margin, margin + size)], fill=color, width=width)
    # Bottom-left
    draw.line([(margin, H - margin), (margin + size, H - margin)], fill=color, width=width)
    draw.line([(margin, H - margin - size), (margin, H - margin)], fill=color, width=width)
    # Bottom-right
    draw.line([(W - margin - size, H - margin), (W - margin, H - margin)], fill=color, width=width)
    draw.line([(W - margin, H - margin - size), (W - margin, H - margin)], fill=color, width=width)


def draw_stars(draw, count=50, color=WHITE):
    """Draw small star dots."""
    random.seed(42)
    for _ in range(count):
        x = random.randint(50, W - 50)
        y = random.randint(50, H - 50)
        sz = random.randint(2, 6)
        draw.ellipse([x - sz, y - sz, x + sz, y + sz], fill=color)
    # Some brighter stars
    for _ in range(15):
        x = random.randint(100, W - 100)
        y = random.randint(100, H - 100)
        sz = random.randint(3, 5)
        # Cross shape for twinkle
        draw.line([(x - sz * 2, y), (x + sz * 2, y)], fill=color, width=1)
        draw.line([(x, y - sz * 2), (x, y + sz * 2)], fill=color, width=1)
        draw.ellipse([x - sz, y - sz, x + sz, y + sz], fill=color)


def draw_botanical_corners(draw, color=SAGE, margin=100):
    """Draw simple botanical leaf shapes in corners."""
    # Simple leaf/branch strokes
    for corner in range(4):
        if corner == 0:  # top-left
            cx, cy = margin + 50, margin + 50
            dx, dy = 1, 1
        elif corner == 1:  # top-right
            cx, cy = W - margin - 50, margin + 50
            dx, dy = -1, 1
        elif corner == 2:  # bottom-left
            cx, cy = margin + 50, H - margin - 50
            dx, dy = 1, -1
        else:  # bottom-right
            cx, cy = W - margin - 50, H - margin - 50
            dx, dy = -1, -1

        # Draw small leaf clusters
        for i in range(3):
            angle = i * 30 + 20
            rad = math.radians(angle)
            ex = cx + int(dx * 80 * math.cos(rad))
            ey = cy + int(dy * 80 * math.sin(rad))
            draw.line([(cx, cy), (ex, ey)], fill=color, width=3)
            # Small leaf ellipses
            leaf_cx = cx + int(dx * 50 * math.cos(rad))
            leaf_cy = cy + int(dy * 50 * math.sin(rad))
            draw.ellipse([leaf_cx - 12, leaf_cy - 6, leaf_cx + 12, leaf_cy + 6], fill=color)


def draw_geometric_dots(draw, color, spacing=120, radius=4):
    """Draw a subtle dot pattern."""
    for x in range(spacing, W, spacing):
        for y in range(spacing, H, spacing):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)


def draw_horizontal_line(draw, y, color=GOLD, width=2, margin=300):
    """Draw a decorative horizontal line."""
    draw.line([(margin, y), (W - margin, y)], fill=color, width=width)


def draw_diamond(draw, cx, cy, size=15, color=GOLD):
    """Draw a small diamond shape."""
    draw.polygon([(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)], fill=color)


def centered_text(draw, text, y, font, fill):
    """Draw centered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def wrap_text_centered(draw, text, y, font, fill, max_width=1800):
    """Word-wrap text and draw centered."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = current + " " + w if current else w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    total_h = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lh = bbox[3] - bbox[1]
        total_h += lh + 30

    cy = y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        x = (W - tw) // 2
        draw.text((x, cy), line, font=font, fill=fill)
        cy += lh + 30
    return cy - y


# ============================================================
# 30 Print Designs
# ============================================================

def print_01():
    """Be the energy you want to attract - bold modern"""
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Geometric color block background
    draw.rectangle([0, 0, W, 400], fill=CHARCOAL)
    draw.rectangle([0, H - 400, W, H], fill=CHARCOAL)

    # Side accent bars
    draw.rectangle([0, 400, 80, H - 400], fill=TERRACOTTA)
    draw.rectangle([W - 80, 400, W, H - 400], fill=TERRACOTTA)

    # Text
    font_lg = get_font_bold(200)
    font_sm = get_font(60)

    words = ["BE THE", "ENERGY", "YOU WANT", "TO", "ATTRACT"]
    y = 600
    for word in words:
        if word == "ENERGY":
            f = get_font_bold(260)
            color = TERRACOTTA
        elif word == "TO":
            f = get_font(120)
            color = CHARCOAL
        else:
            f = get_font_bold(180)
            color = CHARCOAL
        centered_text(draw, word, y, f, color)
        bbox = draw.textbbox((0, 0), word, font=f)
        y += bbox[3] - bbox[1] + 20

    # Small decorative line
    draw_horizontal_line(draw, y + 40, TERRACOTTA, 4, 600)

    return img


def print_02():
    """She believed she could so she did - elegant script style"""
    img = Image.new('RGB', (W, H), SOFT_PINK)
    draw = ImageDraw.Draw(img)

    # Subtle gradient overlay
    for i in range(H):
        ratio = i / H
        alpha = int(30 * ratio)
        draw.line([(0, i), (W, i)], fill=(255, 248, 240, alpha))

    draw_double_border(draw, 80, GOLD, 2)
    draw_corner_accents(draw, GOLD, 80, 80, 2)

    # Text layout - elegant mixed sizing
    y = 800
    font_she = get_font(140)
    font_believed = get_font_bold(160)
    font_she_could = get_font(140)
    font_so = get_font(100)
    font_she_did = get_font_bold(200)

    centered_text(draw, "she", y, font_she, PLUM)
    y += 170
    centered_text(draw, "BELIEVED", y, font_believed, PLUM)
    y += 200
    centered_text(draw, "she could", y, font_she_could, PLUM)
    y += 170
    centered_text(draw, "so", y, font_so, GOLD)
    y += 130
    centered_text(draw, "SHE DID", y, font_she_did, PLUM)

    # Decorative diamond below
    draw_diamond(draw, W // 2, y + 280, 20, GOLD)

    return img


def print_03():
    """Good things take time - minimalist centered"""
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Very minimal design
    font_good = get_font(120)
    font_things = get_font_bold(220)
    font_take = get_font(100)
    font_time = get_font_bold(280)

    y = 900
    centered_text(draw, "good", y, font_good, CHARCOAL)
    y += 160
    centered_text(draw, "THINGS", y, font_things, CHARCOAL)
    y += 260
    centered_text(draw, "take", y, font_take, CHARCOAL)
    y += 140
    centered_text(draw, "TIME", y, font_time, CHARCOAL)

    # Single thin line accent
    draw_horizontal_line(draw, y + 340, CHARCOAL, 2, 900)

    return img


def print_04():
    """Inhale courage exhale fear - zen/calm style"""
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, SOFT_SKY, WHITE)

    # Zen circle (enso)
    cx, cy = W // 2, H // 2 - 100
    r = 500
    for t in range(3):
        draw.arc([cx - r + t, cy - r + t, cx + r - t, cy + r - t], 10, 350,
                 fill=NAVY, width=8)

    # Text inside the circle
    font_action = get_font_bold(140)
    font_word = get_font(110)

    centered_text(draw, "INHALE", cy - 200, font_action, NAVY)
    centered_text(draw, "courage", cy - 50, font_word, SAGE)

    draw_horizontal_line(draw, cy + 40, SAGE, 2, 700)

    centered_text(draw, "EXHALE", cy + 80, font_action, NAVY)
    centered_text(draw, "fear", cy + 230, font_word, DUSTY_ROSE)

    return img


def print_05():
    """You are enough - bold and large"""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Large bold centered text
    font_you = get_font(160)
    font_are = get_font(120)
    font_enough = get_font_bold(340)

    y = 900
    centered_text(draw, "you are", y, font_you, GOLD)
    y += 250
    centered_text(draw, "ENOUGH", y, font_enough, WHITE)

    # Accent line above
    draw_horizontal_line(draw, 850, GOLD, 3, 700)
    # Accent line below
    draw_horizontal_line(draw, y + 380, GOLD, 3, 700)

    # Small text at bottom
    font_sm = get_font(50)
    centered_text(draw, "always have been, always will be", y + 450, font_sm, GOLD)

    return img


def print_06():
    """Create the life you can't wait to wake up to - sunrise colors"""
    img = Image.new('RGB', (W, H))
    # Sunrise gradient: deep purple -> orange -> warm yellow
    draw = ImageDraw.Draw(img)
    for i in range(H):
        ratio = i / H
        if ratio < 0.4:
            r_ratio = ratio / 0.4
            r = int(60 + (220 - 60) * r_ratio)
            g = int(30 + (120 - 30) * r_ratio)
            b = int(100 + (60 - 100) * r_ratio)
        elif ratio < 0.7:
            r_ratio = (ratio - 0.4) / 0.3
            r = int(220 + (255 - 220) * r_ratio)
            g = int(120 + (200 - 120) * r_ratio)
            b = int(60 + (100 - 60) * r_ratio)
        else:
            r_ratio = (ratio - 0.7) / 0.3
            r = int(255)
            g = int(200 + (240 - 200) * r_ratio)
            b = int(100 + (180 - 100) * r_ratio)
        draw.line([(0, i), (W, i)], fill=(r, g, b))

    # Sun circle
    draw.ellipse([W // 2 - 200, 600, W // 2 + 200, 1000], fill=(255, 220, 150))

    font_create = get_font_bold(180)
    font_the = get_font(100)
    font_life = get_font_bold(220)
    font_rest = get_font(90)

    y = 1200
    centered_text(draw, "CREATE", y, font_create, WHITE)
    y += 220
    centered_text(draw, "the life you", y, font_the, WHITE)
    y += 140
    centered_text(draw, "CAN'T WAIT", y, font_life, WHITE)
    y += 260
    centered_text(draw, "to wake up to", y, font_rest, WHITE)

    return img


def print_07():
    """Be yourself everyone else is taken - playful"""
    img = Image.new('RGB', (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Colorful dots pattern background
    random.seed(7)
    colors = [SAGE, DUSTY_ROSE, SKY_BLUE, TERRACOTTA, GOLD, PLUM]
    for _ in range(80):
        x = random.randint(50, W - 50)
        y_pos = random.randint(50, H - 50)
        sz = random.randint(15, 40)
        c = random.choice(colors)
        # Semi-transparent effect by blending
        blended = tuple(int(c[i] * 0.3 + WARM_CREAM[i] * 0.7) for i in range(3))
        draw.ellipse([x - sz, y_pos - sz, x + sz, y_pos + sz], fill=blended)

    # Text
    font_be = get_font_bold(300)
    font_yourself = get_font_bold(180)
    font_rest = get_font(90)

    y = 700
    centered_text(draw, "BE", y, font_be, CHARCOAL)
    y += 350
    centered_text(draw, "YOURSELF", y, font_yourself, TERRACOTTA)
    y += 250
    centered_text(draw, "everyone else", y, font_rest, CHARCOAL)
    y += 130
    centered_text(draw, "is already taken", y, font_rest, CHARCOAL)

    # Playful underline
    draw.line([(500, y + 120), (W - 500, y + 120)], fill=TERRACOTTA, width=6)

    return img


def print_08():
    """Stars can't shine without darkness - dark background with stars"""
    img = Image.new('RGB', (W, H), (15, 15, 35))
    draw = ImageDraw.Draw(img)

    # Star field
    draw_stars(draw, 120, WHITE)

    # Subtle nebula-like gradient glow in center
    for r in range(400, 0, -2):
        alpha_ratio = r / 400
        color = (
            int(40 + 30 * (1 - alpha_ratio)),
            int(20 + 20 * (1 - alpha_ratio)),
            int(60 + 40 * (1 - alpha_ratio))
        )
        draw.ellipse([W // 2 - r, H // 2 - r - 100, W // 2 + r, H // 2 + r - 100], fill=color)

    # Re-draw stars on top
    draw_stars(draw, 60, (255, 255, 220))

    font_stars = get_font_bold(180)
    font_cant = get_font(120)
    font_shine = get_font_bold(220)
    font_rest = get_font(100)

    y = 900
    centered_text(draw, "STARS", y, font_stars, WHITE)
    y += 220
    centered_text(draw, "can't shine", y, font_cant, (200, 200, 220))
    y += 160
    centered_text(draw, "WITHOUT", y, font_shine, GOLD)
    y += 260
    centered_text(draw, "darkness", y, font_rest, (200, 200, 220))

    return img


def print_09():
    """Bloom where you are planted - botanical frame"""
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Botanical frame
    draw_thin_border(draw, 100, SAGE, 3)
    draw_botanical_corners(draw, DARK_SAGE, 100)

    # Additional leaf decorations along top and bottom
    for x in range(300, W - 300, 150):
        # Top leaves
        draw.ellipse([x - 20, 80, x + 20, 120], fill=SAGE)
        # Bottom leaves
        draw.ellipse([x - 20, H - 120, x + 20, H - 80], fill=SAGE)

    # Text
    font_bloom = get_font_bold(260)
    font_where = get_font(110)
    font_planted = get_font_bold(160)

    y = 1000
    centered_text(draw, "BLOOM", y, font_bloom, DARK_SAGE)
    y += 310
    centered_text(draw, "where you are", y, font_where, CHARCOAL)
    y += 160
    centered_text(draw, "PLANTED", y, font_planted, DARK_SAGE)

    # Small flower accent
    draw_diamond(draw, W // 2, y + 250, 18, SAGE)

    return img


def print_10():
    """The best is yet to come - elegant gold"""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    draw_double_border(draw, 80, GOLD, 2)

    # Decorative top/bottom flourishes
    draw_horizontal_line(draw, 300, GOLD, 2, 400)
    draw_diamond(draw, W // 2, 300, 15, GOLD)
    draw_horizontal_line(draw, H - 300, GOLD, 2, 400)
    draw_diamond(draw, W // 2, H - 300, 15, GOLD)

    font_the = get_font(130)
    font_best = get_font_bold(280)
    font_is = get_font(100)
    font_yet = get_font_bold(200)
    font_to_come = get_font(130)

    y = 800
    centered_text(draw, "the", y, font_the, GOLD)
    y += 180
    centered_text(draw, "BEST", y, font_best, WHITE)
    y += 320
    centered_text(draw, "is yet", y, font_is, GOLD)
    y += 150
    centered_text(draw, "TO COME", y, font_yet, WHITE)

    return img


def print_11():
    """Stay wild moon child - celestial theme"""
    img = Image.new('RGB', (W, H), (20, 20, 50))
    draw = ImageDraw.Draw(img)

    # Stars
    draw_stars(draw, 80, (255, 255, 230))

    # Moon crescent
    cx, cy = W // 2 + 300, 500
    draw.ellipse([cx - 200, cy - 200, cx + 200, cy + 200], fill=(240, 235, 210))
    draw.ellipse([cx - 100, cy - 250, cx + 300, cy + 150], fill=(20, 20, 50))

    font_stay = get_font_bold(200)
    font_wild = get_font_bold(300)
    font_moon = get_font(120)
    font_child = get_font_bold(200)

    y = 1000
    centered_text(draw, "STAY", y, font_stay, (240, 235, 210))
    y += 250
    centered_text(draw, "WILD", y, font_wild, WHITE)
    y += 350
    centered_text(draw, "moon", y, font_moon, GOLD)
    y += 160
    centered_text(draw, "CHILD", y, font_child, (240, 235, 210))

    return img


def print_12():
    """Kindness is free sprinkle it everywhere - colorful"""
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Colorful confetti/sprinkles
    random.seed(12)
    colors = [SAGE, DUSTY_ROSE, SKY_BLUE, TERRACOTTA, GOLD, PLUM, (255, 180, 100)]
    for _ in range(150):
        x = random.randint(30, W - 30)
        y_pos = random.randint(30, H - 30)
        sz = random.randint(8, 25)
        c = random.choice(colors)
        shape = random.choice(['circle', 'rect'])
        if shape == 'circle':
            draw.ellipse([x - sz, y_pos - sz, x + sz, y_pos + sz], fill=c)
        else:
            angle = random.randint(0, 3)
            draw.rectangle([x - sz, y_pos - sz // 2, x + sz, y_pos + sz // 2], fill=c)

    # White text background strip
    draw.rectangle([100, 900, W - 100, 2200], fill=(255, 255, 255, 200))

    font_kind = get_font_bold(180)
    font_is = get_font(100)
    font_free = get_font_bold(250)
    font_rest = get_font(90)

    y = 950
    centered_text(draw, "KINDNESS", y, font_kind, PLUM)
    y += 230
    centered_text(draw, "is free", y, font_is, CHARCOAL)
    y += 160
    centered_text(draw, "SPRINKLE IT", y, font_free, TERRACOTTA)
    y += 300
    centered_text(draw, "everywhere", y, font_rest, CHARCOAL)

    return img


def print_13():
    """Make today amazing - energetic bold"""
    img = Image.new('RGB', (W, H), TERRACOTTA)
    draw = ImageDraw.Draw(img)

    # Bold geometric background
    draw.rectangle([0, 0, W, 600], fill=CHARCOAL)
    draw.rectangle([0, H - 200, W, H], fill=CHARCOAL)

    # Diagonal accent
    draw.polygon([(0, 600), (W, 400), (W, 600)], fill=(180, 95, 45))

    font_make = get_font_bold(280)
    font_today = get_font_bold(220)
    font_amazing = get_font_bold(260)

    centered_text(draw, "MAKE", 200, font_make, WHITE)
    centered_text(draw, "TODAY", 1100, font_today, WHITE)
    centered_text(draw, "AMAZING", 1600, font_amazing, CREAM)

    # Energetic lines
    draw.line([(200, 2200), (W - 200, 2200)], fill=WHITE, width=6)
    draw.line([(200, 2230), (W - 200, 2230)], fill=WHITE, width=3)

    return img


def print_14():
    """Trust the timing of your life - calm and serene"""
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, (220, 235, 245), CREAM)

    draw_thin_border(draw, 100, SAGE, 2)

    font_trust = get_font_bold(160)
    font_the = get_font(110)
    font_timing = get_font_bold(200)
    font_of = get_font(80)
    font_life = get_font_bold(180)

    y = 900
    centered_text(draw, "TRUST", y, font_trust, NAVY)
    y += 200
    centered_text(draw, "the", y, font_the, SAGE)
    y += 150
    centered_text(draw, "TIMING", y, font_timing, NAVY)
    y += 250
    centered_text(draw, "of your", y, font_of, SAGE)
    y += 130
    centered_text(draw, "LIFE", y, font_life, NAVY)

    # Serene wave line
    for x in range(300, W - 300):
        yy = int(y + 300 + 15 * math.sin(x / 60))
        draw.rectangle([x, yy, x + 1, yy + 2], fill=SAGE)

    return img


def print_15():
    """You are capable of amazing things - gradient"""
    img = Image.new('RGB', (W, H))
    # Purple to blue gradient
    draw = draw_gradient(img, PLUM, (100, 140, 200))

    font_you = get_font(120)
    font_capable = get_font_bold(200)
    font_of = get_font(90)
    font_amazing = get_font_bold(220)
    font_things = get_font_bold(200)

    y = 800
    centered_text(draw, "you are", y, font_you, WHITE)
    y += 180
    centered_text(draw, "CAPABLE", y, font_capable, WHITE)
    y += 260
    centered_text(draw, "of", y, font_of, LIGHT_GOLD)
    y += 130
    centered_text(draw, "AMAZING", y, font_amazing, WHITE)
    y += 260
    centered_text(draw, "THINGS", y, font_things, LIGHT_GOLD)

    # Subtle geometric accent
    draw_horizontal_line(draw, y + 150, WHITE, 2, 700)

    return img


def print_16():
    """Choose joy - large letters, simple"""
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Massive text
    font_choose = get_font(200)
    font_joy = get_font_bold(500)

    centered_text(draw, "choose", 900, font_choose, CHARCOAL)
    centered_text(draw, "JOY", 1200, font_joy, TERRACOTTA)

    # Small period accent
    draw.ellipse([W // 2 + 350, 1650, W // 2 + 400, 1700], fill=TERRACOTTA)

    return img


def print_17():
    """Dream big work hard stay humble - three-line stack"""
    img = Image.new('RGB', (W, H), CHARCOAL)
    draw = ImageDraw.Draw(img)

    # Three distinct color bands
    band_h = H // 3
    draw.rectangle([0, 0, W, band_h], fill=(40, 50, 65))
    draw.rectangle([0, band_h, W, band_h * 2], fill=CHARCOAL)
    draw.rectangle([0, band_h * 2, W, H], fill=(40, 50, 65))

    font = get_font_bold(220)

    centered_text(draw, "DREAM BIG", band_h // 2 - 60, font, GOLD)
    centered_text(draw, "WORK HARD", band_h + band_h // 2 - 60, font, WHITE)
    centered_text(draw, "STAY HUMBLE", band_h * 2 + band_h // 2 - 60, font, DUSTY_ROSE)

    # Thin separator lines
    draw.line([(300, band_h), (W - 300, band_h)], fill=GOLD, width=2)
    draw.line([(300, band_h * 2), (W - 300, band_h * 2)], fill=GOLD, width=2)

    return img


def print_18():
    """Be a voice not an echo - modern typographic"""
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Strong typographic contrast
    font_be_a = get_font(100)
    font_voice = get_font_bold(350)
    font_not_an = get_font(100)
    font_echo = get_font_bold(300)

    y = 700
    centered_text(draw, "be a", y, font_be_a, CHARCOAL)
    y += 160
    centered_text(draw, "VOICE", y, font_voice, NAVY)
    y += 400
    centered_text(draw, "not an", y, font_not_an, CHARCOAL)
    y += 160
    # Echo in lighter color to represent fading
    centered_text(draw, "ECHO", y, font_echo, (180, 180, 190))

    # Bold accent line
    draw.rectangle([200, y - 30, W - 200, y - 20], fill=NAVY)

    return img


def print_19():
    """Collect moments not things - travel-inspired"""
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, (200, 180, 160), WARM_CREAM)

    draw_corner_accents(draw, TERRACOTTA, 100, 80, 3)

    # Compass-like decoration
    cx, cy = W // 2, 500
    r = 120
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TERRACOTTA, width=3)
    draw.line([(cx, cy - r - 20), (cx, cy + r + 20)], fill=TERRACOTTA, width=2)
    draw.line([(cx - r - 20, cy), (cx + r + 20, cy)], fill=TERRACOTTA, width=2)

    font_collect = get_font_bold(200)
    font_moments = get_font_bold(180)
    font_not = get_font(100)
    font_things = get_font(160)

    y = 1000
    centered_text(draw, "COLLECT", y, font_collect, CHARCOAL)
    y += 250
    centered_text(draw, "MOMENTS", y, font_moments, TERRACOTTA)
    y += 280
    centered_text(draw, "not", y, font_not, CHARCOAL)
    y += 150
    centered_text(draw, "things", y, font_things, CHARCOAL)

    return img


def print_20():
    """Progress not perfection - clean modern"""
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Clean geometric accent - colored bar at top
    draw.rectangle([0, 0, W, 120], fill=SAGE)

    font_progress = get_font_bold(240)
    font_not = get_font(140)
    font_perfection = get_font_bold(180)

    y = 1100
    centered_text(draw, "PROGRESS", y, font_progress, CHARCOAL)
    y += 300
    centered_text(draw, "not", y, font_not, SAGE)
    y += 200
    centered_text(draw, "PERFECTION", y, font_perfection, CHARCOAL)

    # Bottom accent bar
    draw.rectangle([0, H - 120, W, H], fill=SAGE)

    return img


def print_21():
    """Life is tough but so are you - strong/bold"""
    img = Image.new('RGB', (W, H), CHARCOAL)
    draw = ImageDraw.Draw(img)

    # Bold red accent stripe
    draw.rectangle([0, 1300, W, 1700], fill=TERRACOTTA)

    font_life = get_font_bold(200)
    font_is = get_font(120)
    font_tough = get_font_bold(280)
    font_but = get_font(100)
    font_so = get_font_bold(200)
    font_you = get_font_bold(300)

    centered_text(draw, "LIFE IS", 600, font_life, WHITE)
    centered_text(draw, "TOUGH", 850, font_tough, WHITE)

    centered_text(draw, "but so", 1350, font_but, WHITE)
    centered_text(draw, "ARE YOU", 1800, font_you, WHITE)

    # Strong line
    draw.rectangle([300, 1200, W - 300, 1210], fill=TERRACOTTA)

    return img


def print_22():
    """Grateful thankful blessed - warm tones"""
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, WARM_CREAM, WARM_BEIGE)

    draw_thin_border(draw, 80, TERRACOTTA, 2)

    font_main = get_font_bold(200)
    font_div = get_font(40)

    y = 900
    centered_text(draw, "GRATEFUL", y, font_main, TERRACOTTA)
    y += 300
    # Decorative divider
    draw_diamond(draw, W // 2, y, 12, GOLD)
    draw_horizontal_line(draw, y, GOLD, 1, 700)
    y += 80
    centered_text(draw, "THANKFUL", y, font_main, CHARCOAL)
    y += 300
    draw_diamond(draw, W // 2, y, 12, GOLD)
    draw_horizontal_line(draw, y, GOLD, 1, 700)
    y += 80
    centered_text(draw, "BLESSED", y, font_main, SAGE)

    return img


def print_23():
    """Happiness is homemade - cozy/warm"""
    img = Image.new('RGB', (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Warm checkered subtle pattern
    for x in range(0, W, 200):
        for y_pos in range(0, H, 200):
            if (x // 200 + y_pos // 200) % 2 == 0:
                c = (245, 235, 220)
            else:
                c = WARM_CREAM
            draw.rectangle([x, y_pos, x + 200, y_pos + 200], fill=c)

    # Heart shape accent
    cx, cy = W // 2, 600
    # Simple heart with two circles and a triangle
    draw.ellipse([cx - 100, cy - 60, cx, cy + 40], fill=DUSTY_ROSE)
    draw.ellipse([cx, cy - 60, cx + 100, cy + 40], fill=DUSTY_ROSE)
    draw.polygon([(cx - 100, cy), (cx + 100, cy), (cx, cy + 100)], fill=DUSTY_ROSE)

    font_happiness = get_font_bold(180)
    font_is = get_font(100)
    font_homemade = get_font_bold(200)

    y = 1100
    centered_text(draw, "HAPPINESS", y, font_happiness, CHARCOAL)
    y += 250
    centered_text(draw, "is", y, font_is, DUSTY_ROSE)
    y += 150
    centered_text(draw, "HOMEMADE", y, font_homemade, CHARCOAL)

    return img


def print_24():
    """Adventure awaits - wanderlust theme"""
    img = Image.new('RGB', (W, H))
    # Mountain-like gradient: dark top to warm bottom
    draw = draw_gradient(img, NAVY, (180, 160, 140))

    # Simple mountain silhouettes
    # Mountain 1
    draw.polygon([(0, 2200), (600, 1400), (1200, 2200)], fill=(40, 55, 80))
    # Mountain 2
    draw.polygon([(800, 2200), (1500, 1200), (2200, 2200)], fill=(50, 65, 90))
    # Mountain 3
    draw.polygon([(1400, 2200), (2000, 1500), (2400, 2200)], fill=(35, 50, 75))
    # Snow caps
    draw.polygon([(1500, 1200), (1420, 1350), (1580, 1350)], fill=WHITE)

    # Ground
    draw.rectangle([0, 2200, W, H], fill=(60, 75, 50))

    font_adventure = get_font_bold(240)
    font_awaits = get_font(180)

    centered_text(draw, "ADVENTURE", 500, font_adventure, WHITE)
    centered_text(draw, "awaits", 800, font_awaits, GOLD)

    # Arrow decoration
    cx = W // 2
    draw.line([(cx - 100, 1050), (cx + 100, 1050)], fill=GOLD, width=3)
    draw.polygon([(cx + 100, 1035), (cx + 130, 1050), (cx + 100, 1065)], fill=GOLD)

    return img


def print_25():
    """You matter - large impactful"""
    img = Image.new('RGB', (W, H))
    draw = draw_radial_gradient(img, (60, 50, 80), (30, 25, 45))

    font_you = get_font(200)
    font_matter = get_font_bold(400)

    centered_text(draw, "you", 1000, font_you, DUSTY_ROSE)
    centered_text(draw, "MATTER", 1300, font_matter, WHITE)

    # Glowing accent lines
    for i in range(5):
        y_line = 1800 + i * 8
        alpha = 255 - i * 50
        c = (DUSTY_ROSE[0], DUSTY_ROSE[1], DUSTY_ROSE[2])
        draw.line([(600, y_line), (W - 600, y_line)], fill=c, width=2)

    return img


def print_26():
    """Today is a good day for a good day - sunny/bright"""
    img = Image.new('RGB', (W, H), (255, 250, 230))
    draw = ImageDraw.Draw(img)

    # Sun rays radiating from top
    cx, cy = W // 2, -200
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        ex = cx + int(3000 * math.cos(rad))
        ey = cy + int(3000 * math.sin(rad))
        draw.line([(cx, cy), (ex, ey)], fill=(255, 240, 200), width=40)

    # Bright sun
    draw.ellipse([cx - 300, cy - 100, cx + 300, cy + 500], fill=(255, 220, 100))

    font_today = get_font_bold(180)
    font_is_a = get_font(100)
    font_good_day = get_font_bold(220)
    font_for_a = get_font(100)

    y = 1000
    centered_text(draw, "TODAY IS A", y, font_today, CHARCOAL)
    y += 250
    centered_text(draw, "GOOD DAY", y, font_good_day, TERRACOTTA)
    y += 300
    centered_text(draw, "for a", y, font_for_a, CHARCOAL)
    y += 150
    centered_text(draw, "GOOD DAY", y, font_good_day, TERRACOTTA)

    return img


def print_27():
    """Be the change you wish to see - earth tones"""
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, (180, 160, 130), (220, 200, 170))

    draw_thin_border(draw, 90, (120, 100, 70), 3)

    # Earth circle decoration
    cx, cy = W // 2, 600
    draw.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=SAGE, width=4)
    # Simple continent shapes
    draw.ellipse([cx - 60, cy - 80, cx + 40, cy - 20], fill=SAGE)
    draw.ellipse([cx - 30, cy - 10, cx + 80, cy + 60], fill=SAGE)
    draw.ellipse([cx - 100, cy + 20, cx - 30, cy + 80], fill=SAGE)

    font_be = get_font(140)
    font_change = get_font_bold(240)
    font_rest = get_font(100)

    y = 1100
    centered_text(draw, "be the", y, font_be, CHARCOAL)
    y += 200
    centered_text(draw, "CHANGE", y, font_change, (80, 60, 40))
    y += 300
    centered_text(draw, "you wish to see", y, font_rest, CHARCOAL)

    return img


def print_28():
    """Rise above the storm - dramatic"""
    img = Image.new('RGB', (W, H))
    # Dramatic storm gradient
    draw = draw_gradient(img, (30, 30, 50), (80, 80, 100))

    # Lightning bolt accent
    points = [
        (W // 2 + 50, 200), (W // 2 - 50, 800),
        (W // 2 + 30, 800), (W // 2 - 100, 1400),
        (W // 2 + 80, 750), (W // 2 - 10, 750),
        (W // 2 + 120, 200)
    ]
    draw.polygon(points, fill=(255, 255, 200))

    # Cloud shapes
    for cx, cy in [(400, 400), (1800, 300), (1000, 250)]:
        for dx, dy, r in [(-60, 0, 80), (60, 0, 80), (0, -40, 90), (-30, -20, 70), (30, -20, 70)]:
            draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(60, 60, 80))

    font_rise = get_font_bold(300)
    font_above = get_font(160)
    font_storm = get_font_bold(240)

    centered_text(draw, "RISE", 1600, font_rise, WHITE)
    centered_text(draw, "above the", 1950, font_above, (200, 200, 220))
    centered_text(draw, "STORM", 2200, font_storm, GOLD)

    return img


def print_29():
    """Let your light shine - radiant/glowing effect"""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Radiant glow from center
    cx, cy = W // 2, H // 2
    for r in range(800, 0, -4):
        ratio = 1 - r / 800
        color = (
            int(27 + (255 - 27) * ratio * 0.3),
            int(42 + (220 - 42) * ratio * 0.3),
            int(74 + (150 - 74) * ratio * 0.3)
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # Light rays
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        for d in range(100, 600, 3):
            x = int(cx + d * math.cos(rad))
            y = int(cy + d * math.sin(rad))
            brightness = max(0, 100 - d // 6)
            c = (27 + brightness, 42 + brightness, 74 + brightness)
            if 0 <= x < W and 0 <= y < H:
                draw.point((x, y), fill=c)

    font_let = get_font(140)
    font_your = get_font(120)
    font_light = get_font_bold(300)
    font_shine = get_font_bold(240)

    centered_text(draw, "let your", 1000, font_let, GOLD)
    centered_text(draw, "LIGHT", 1200, font_light, WHITE)
    centered_text(draw, "SHINE", 1550, font_shine, GOLD)

    return img


def print_30():
    """This is your year - bold with 2026"""
    img = Image.new('RGB', (W, H))
    draw = draw_gradient(img, CHARCOAL, NAVY)

    # Large year in background
    font_year_bg = get_font_bold(600)
    bbox = draw.textbbox((0, 0), "2026", font=font_year_bg)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    # Subtle background year
    draw.text((x, 300), "2026", font=font_year_bg, fill=(50, 60, 85))

    draw_corner_accents(draw, GOLD, 120, 80, 3)

    font_this = get_font(160)
    font_is = get_font(120)
    font_your = get_font_bold(200)
    font_year = get_font_bold(350)
    font_2026 = get_font_bold(180)

    y = 900
    centered_text(draw, "THIS IS", y, font_this, WHITE)
    y += 250
    centered_text(draw, "YOUR", y, font_your, GOLD)
    y += 280
    centered_text(draw, "YEAR", y, font_year, WHITE)

    # 2026 below
    y += 500
    centered_text(draw, "2026", y, font_2026, GOLD)

    # Decorative line
    draw_horizontal_line(draw, y - 50, GOLD, 2, 600)

    return img


# ============================================================
# Main execution
# ============================================================

PRINTS = [
    (1, print_01), (2, print_02), (3, print_03), (4, print_04), (5, print_05),
    (6, print_06), (7, print_07), (8, print_08), (9, print_09), (10, print_10),
    (11, print_11), (12, print_12), (13, print_13), (14, print_14), (15, print_15),
    (16, print_16), (17, print_17), (18, print_18), (19, print_19), (20, print_20),
    (21, print_21), (22, print_22), (23, print_23), (24, print_24), (25, print_25),
    (26, print_26), (27, print_27), (28, print_28), (29, print_29), (30, print_30),
]

if __name__ == "__main__":
    print(f"Generating 30 motivational quote prints at {W}x{H}px...")
    for num, func in PRINTS:
        print(f"  Creating print {num:02d}/30...", end=" ", flush=True)
        img = func()
        path = os.path.join(OUT, f"quote_print_{num:02d}.jpg")
        img.save(path, "JPEG", quality=95)
        print(f"Saved: {path}")
    print(f"\nAll 30 prints generated successfully!")
