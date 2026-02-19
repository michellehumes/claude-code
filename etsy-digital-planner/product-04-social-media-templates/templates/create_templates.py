#!/usr/bin/env python3
"""
Create 50 Social Media Templates Bundle
- 25 Instagram Post templates (1080x1080)
- 15 Instagram Story templates (1080x1920)
- 10 Pinterest Pin templates (1000x1500)

Theme: Modern minimalist with dusty rose/blush pink palette
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

# === Color Palette ===
DUSTY_ROSE = (232, 196, 196)       # #E8C4C4
CREAM = (255, 245, 238)            # #FFF5EE
CHARCOAL = (51, 51, 51)            # #333333
GOLD = (201, 169, 110)             # #C9A96E
WHITE = (255, 255, 255)
LIGHT_PINK = (245, 225, 225)       # lighter pink accent
SOFT_GRAY = (180, 180, 180)
MEDIUM_ROSE = (220, 175, 175)      # medium shade
DARK_ROSE = (180, 140, 140)        # darker rose
LIGHT_GOLD = (220, 200, 160)       # lighter gold

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    """Draw a rounded rectangle with safety guard."""
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
        return
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def get_font(size, bold=False):
    """Get a font, falling back to default if needed."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_center_x(draw, text, font, canvas_width):
    """Get x position to center text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    return (canvas_width - tw) // 2


def draw_text_centered(draw, text, y, font, fill, canvas_width):
    """Draw centered text."""
    x = text_center_x(draw, text, font, canvas_width)
    draw.text((x, y), text, font=font, fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def draw_decorative_line(draw, y, w, color=GOLD, thickness=2, margin=100):
    """Draw a centered decorative line."""
    draw.line([(margin, y), (w - margin, y)], fill=color, width=thickness)


def draw_diamond(draw, cx, cy, size, fill):
    """Draw a small diamond shape."""
    draw.polygon([(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)], fill=fill)


def draw_circle(draw, cx, cy, r, fill=None, outline=None, width=1):
    """Draw a circle."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def draw_corner_accents(draw, w, h, color=GOLD, size=60, thickness=3):
    """Draw L-shaped corner accents."""
    m = 40
    # top-left
    draw.line([(m, m), (m + size, m)], fill=color, width=thickness)
    draw.line([(m, m), (m, m + size)], fill=color, width=thickness)
    # top-right
    draw.line([(w - m - size, m), (w - m, m)], fill=color, width=thickness)
    draw.line([(w - m, m), (w - m, m + size)], fill=color, width=thickness)
    # bottom-left
    draw.line([(m, h - m), (m + size, h - m)], fill=color, width=thickness)
    draw.line([(m, h - m - size), (m, h - m)], fill=color, width=thickness)
    # bottom-right
    draw.line([(w - m - size, h - m), (w - m, h - m)], fill=color, width=thickness)
    draw.line([(w - m, h - m - size), (w - m, h - m)], fill=color, width=thickness)


def draw_dots_pattern(draw, x0, y0, x1, y1, spacing=30, r=2, fill=LIGHT_GOLD):
    """Draw a grid of small dots in a region."""
    for x in range(x0, x1, spacing):
        for y in range(y0, y1, spacing):
            draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw_wavy_line(draw, y, w, color=GOLD, amplitude=5, freq=0.03, thickness=2, margin=80):
    """Draw a wavy horizontal line."""
    points = []
    for x in range(margin, w - margin):
        yy = y + int(amplitude * math.sin(freq * x))
        points.append((x, yy))
    if len(points) > 1:
        draw.line(points, fill=color, width=thickness)


def draw_abstract_blob(draw, cx, cy, size, fill):
    """Draw an abstract organic blob shape."""
    points = []
    for i in range(12):
        angle = 2 * math.pi * i / 12
        r = size + random.randint(-size // 4, size // 4)
        points.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
    draw.polygon(points, fill=fill)


def draw_star(draw, cx, cy, outer_r, inner_r, points_count, fill):
    """Draw a star shape."""
    pts = []
    for i in range(points_count * 2):
        angle = math.pi * i / points_count - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
    draw.polygon(pts, fill=fill)


def draw_placeholder_image_box(draw, x0, y0, x1, y1, label="[YOUR IMAGE]"):
    """Draw a placeholder box for an image area."""
    draw_rounded_rect(draw, (x0, y0, x1, y1), 10, fill=LIGHT_PINK, outline=SOFT_GRAY, width=2)
    font = get_font(20)
    draw_text_centered(draw, label, (y0 + y1) // 2 - 10, font, SOFT_GRAY, x1 - x0)
    # adjust for position
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((x0 + x1 - tw) // 2, (y0 + y1) // 2 - 10), label, font=font, fill=SOFT_GRAY)


# ===========================================================================
# TEMPLATE GENERATORS
# ===========================================================================

def create_quote_template_1(w, h, idx):
    """Centered quote with corner accents."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw_corner_accents(draw, w, h)
    font_quote = get_font(max(36, w // 20), bold=True)
    font_attr = get_font(max(22, w // 35))
    cy = h // 2 - 60
    draw_text_centered(draw, '"[YOUR QUOTE HERE]"', cy, font_quote, CHARCOAL, w)
    draw_decorative_line(draw, cy + 80, w, GOLD, 2, w // 4)
    draw_diamond(draw, w // 2, cy + 80, 6, GOLD)
    draw_text_centered(draw, "- @yourusername", cy + 110, font_attr, DARK_ROSE, w)
    return img


def create_quote_template_2(w, h, idx):
    """Quote with dusty rose sidebar."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w // 8, h], fill=DUSTY_ROSE)
    draw.rectangle([w // 8, h // 4, w // 8 + 4, 3 * h // 4], fill=GOLD)
    font_quote = get_font(max(34, w // 22), bold=True)
    font_sub = get_font(max(20, w // 35))
    xoff = w // 8 + 60
    draw.text((xoff, h // 3), '"[YOUR QUOTE', font=font_quote, fill=CHARCOAL)
    draw.text((xoff, h // 3 + 55), 'GOES HERE]"', font=font_quote, fill=CHARCOAL)
    draw.text((xoff, h // 3 + 140), "- Author Name", font=font_sub, fill=GOLD)
    draw_dots_pattern(draw, 10, 10, w // 8 - 10, h // 6, 20, 2, MEDIUM_ROSE)
    return img


def create_quote_template_3(w, h, idx):
    """Circular quote frame."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2
    r = min(w, h) // 3
    draw_circle(draw, cx, cy, r, fill=CREAM)
    draw_circle(draw, cx, cy, r - 8, outline=GOLD, width=2)
    font_q = get_font(max(28, w // 28), bold=True)
    font_a = get_font(max(18, w // 40))
    draw_text_centered(draw, '"[YOUR', cy - 40, font_q, CHARCOAL, w)
    draw_text_centered(draw, 'QUOTE]"', cy + 10, font_q, CHARCOAL, w)
    draw_text_centered(draw, "@handle", cy + 60, font_a, GOLD, w)
    draw_star(draw, 80, 80, 15, 7, 5, GOLD)
    draw_star(draw, w - 80, h - 80, 15, 7, 5, GOLD)
    return img


def create_quote_template_4(w, h, idx):
    """Minimal quote with large quotation mark."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, h - 60, w, h], fill=DUSTY_ROSE)
    big_font = get_font(min(200, w // 4), bold=True)
    draw.text((60, h // 6), "\u201C", font=big_font, fill=LIGHT_PINK)
    font_q = get_font(max(30, w // 24), bold=True)
    font_a = get_font(max(20, w // 36))
    draw.text((100, h // 3 + 20), "[YOUR QUOTE", font=font_q, fill=CHARCOAL)
    draw.text((100, h // 3 + 70), "GOES HERE]", font=font_q, fill=CHARCOAL)
    draw_decorative_line(draw, h // 3 + 130, w, GOLD, 2, 100)
    draw.text((100, h // 3 + 150), "- @yourusername", font=font_a, fill=DARK_ROSE)
    return img


def create_quote_template_5(w, h, idx):
    """Quote with geometric background."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    # geometric triangles
    draw.polygon([(0, 0), (w // 3, 0), (0, h // 3)], fill=LIGHT_PINK)
    draw.polygon([(w, h), (2 * w // 3, h), (w, 2 * h // 3)], fill=LIGHT_PINK)
    draw_rounded_rect(draw, (w // 8, h // 4, 7 * w // 8, 3 * h // 4), 20, fill=WHITE, outline=GOLD, width=2)
    font_q = get_font(max(30, w // 24), bold=True)
    font_a = get_font(max(18, w // 40))
    draw_text_centered(draw, '"[YOUR QUOTE HERE]"', h // 2 - 30, font_q, CHARCOAL, w)
    draw_text_centered(draw, "- @yourusername", h // 2 + 40, font_a, GOLD, w)
    return img


def create_promo_sale(w, h, idx):
    """Sale announcement template."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    draw_rounded_rect(draw, (40, 40, w - 40, h - 40), 0, fill=None, outline=GOLD, width=3)
    font_big = get_font(max(72, w // 8), bold=True)
    font_med = get_font(max(36, w // 20), bold=True)
    font_sm = get_font(max(22, w // 32))
    draw_text_centered(draw, "SALE", h // 4, font_big, WHITE, w)
    draw_decorative_line(draw, h // 4 + 100, w, GOLD, 3, w // 4)
    draw_text_centered(draw, "[XX]% OFF", h // 2 - 20, font_med, CHARCOAL, w)
    draw_text_centered(draw, "EVERYTHING", h // 2 + 40, font_med, CHARCOAL, w)
    draw_rounded_rect(draw, (w // 4, 3 * h // 4 - 30, 3 * w // 4, 3 * h // 4 + 30), 25, fill=CHARCOAL)
    draw_text_centered(draw, "SHOP NOW", 3 * h // 4 - 22, font_sm, WHITE, w)
    return img


def create_promo_new(w, h, idx):
    """New product announcement."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 3], fill=DUSTY_ROSE)
    font_big = get_font(max(60, w // 10), bold=True)
    font_med = get_font(max(30, w // 24), bold=True)
    font_sm = get_font(max(20, w // 36))
    draw_text_centered(draw, "NEW", h // 8, font_big, WHITE, w)
    draw_text_centered(draw, "[PRODUCT NAME]", h // 2 - 20, font_med, CHARCOAL, w)
    draw_decorative_line(draw, h // 2 + 30, w, GOLD, 2, w // 4)
    draw_text_centered(draw, "[Brief description here]", h // 2 + 60, font_sm, DARK_ROSE, w)
    draw_text_centered(draw, "$[PRICE]", h // 2 + 110, font_med, GOLD, w)
    draw_placeholder_image_box(draw, w // 4, 2 * h // 3, 3 * w // 4, h - 80, "[YOUR IMAGE]")
    return img


def create_promo_coming_soon(w, h, idx):
    """Coming soon teaser."""
    img = Image.new("RGB", (w, h), CHARCOAL)
    draw = ImageDraw.Draw(img)
    draw_corner_accents(draw, w, h, GOLD, 80, 2)
    font_big = get_font(max(50, w // 12), bold=True)
    font_med = get_font(max(28, w // 26))
    font_sm = get_font(max(20, w // 36))
    draw_text_centered(draw, "COMING", h // 3 - 30, font_big, GOLD, w)
    draw_text_centered(draw, "SOON", h // 3 + 40, font_big, GOLD, w)
    draw_wavy_line(draw, h // 2 + 20, w, DUSTY_ROSE, 4, 0.04, 2, w // 4)
    draw_text_centered(draw, "[DATE / DETAILS]", h // 2 + 60, font_med, CREAM, w)
    draw_text_centered(draw, "Stay tuned!", font_sm.size + h // 2 + 100, font_sm, DUSTY_ROSE, w)
    return img


def create_promo_launch(w, h, idx):
    """Launch day template."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 80], fill=GOLD)
    draw.rectangle([0, h - 80, w, h], fill=GOLD)
    font_label = get_font(max(18, w // 40))
    font_big = get_font(max(56, w // 12), bold=True)
    font_med = get_font(max(26, w // 28))
    draw_text_centered(draw, "IT'S HERE!", 20, font_label, WHITE, w)
    draw_text_centered(draw, "[PRODUCT", h // 3, font_big, CHARCOAL, w)
    draw_text_centered(draw, "NAME]", h // 3 + 70, font_big, CHARCOAL, w)
    draw_decorative_line(draw, h // 2 + 40, w, DUSTY_ROSE, 3, w // 5)
    draw_text_centered(draw, "[One-line description]", h // 2 + 70, font_med, DARK_ROSE, w)
    draw_rounded_rect(draw, (w // 4, 2 * h // 3, 3 * w // 4, 2 * h // 3 + 55), 28, fill=DUSTY_ROSE)
    draw_text_centered(draw, "SHOP NOW \u2192", 2 * h // 3 + 10, font_med, WHITE, w)
    draw_text_centered(draw, "LINK IN BIO", h - 60, font_label, WHITE, w)
    return img


def create_tips_template_1(w, h, idx):
    """5 Tips numbered list."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 5], fill=DUSTY_ROSE)
    font_title = get_font(max(34, w // 20), bold=True)
    font_num = get_font(max(28, w // 26), bold=True)
    font_tip = get_font(max(20, w // 36))
    draw_text_centered(draw, "5 TIPS FOR [TOPIC]", h // 10 - 10, font_title, WHITE, w)
    tips = ["[First tip goes here]", "[Second tip goes here]", "[Third tip goes here]",
            "[Fourth tip goes here]", "[Fifth tip goes here]"]
    y_start = h // 5 + 30
    spacing = (h - y_start - 40) // 5
    for i, tip in enumerate(tips):
        ny = y_start + i * spacing
        draw_circle(draw, 80, ny + 15, 18, fill=GOLD)
        font_num_small = get_font(max(20, w // 36), bold=True)
        draw.text((72, ny + 2), str(i + 1), font=font_num_small, fill=WHITE)
        draw.text((120, ny + 2), tip, font=font_tip, fill=CHARCOAL)
    return img


def create_tips_template_2(w, h, idx):
    """3 Steps template with boxes."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(32, w // 22), bold=True)
    font_step = get_font(max(22, w // 32), bold=True)
    font_desc = get_font(max(18, w // 40))
    draw_text_centered(draw, "HOW TO [TOPIC]", 50, font_title, CHARCOAL, w)
    draw_decorative_line(draw, 100, w, GOLD, 2, w // 3)
    steps = ["[STEP ONE]", "[STEP TWO]", "[STEP THREE]"]
    descs = ["[Description here]", "[Description here]", "[Description here]"]
    box_h = (h - 200) // 3 - 20
    for i in range(3):
        by = 140 + i * (box_h + 20)
        draw_rounded_rect(draw, (60, by, w - 60, by + box_h), 15, fill=LIGHT_PINK if i % 2 == 0 else CREAM, outline=DUSTY_ROSE, width=1)
        draw_circle(draw, 100, by + box_h // 2, 22, fill=GOLD)
        draw.text((90, by + box_h // 2 - 12), str(i + 1), font=font_step, fill=WHITE)
        draw.text((140, by + box_h // 3 - 5), steps[i], font=font_step, fill=CHARCOAL)
        draw.text((140, by + box_h // 3 + 30), descs[i], font=font_desc, fill=DARK_ROSE)
    return img


def create_tips_template_3(w, h, idx):
    """Checklist style template."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    draw_rounded_rect(draw, (50, 50, w - 50, h - 50), 20, fill=CREAM)
    font_title = get_font(max(30, w // 24), bold=True)
    font_item = get_font(max(20, w // 36))
    draw_text_centered(draw, "[YOUR] CHECKLIST", 90, font_title, CHARCOAL, w)
    draw_decorative_line(draw, 140, w, GOLD, 2, 100)
    items = [
        "\u2610  [Checklist item one]",
        "\u2610  [Checklist item two]",
        "\u2610  [Checklist item three]",
        "\u2610  [Checklist item four]",
        "\u2610  [Checklist item five]",
        "\u2610  [Checklist item six]",
    ]
    y = 180
    for item in items:
        draw.text((100, y), item, font=font_item, fill=CHARCOAL)
        y += (h - 260) // len(items)
    draw_text_centered(draw, "@yourusername", h - 90, get_font(max(16, w // 45)), DARK_ROSE, w)
    return img


def create_about_me(w, h, idx):
    """About me / meet the maker."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 6], fill=CHARCOAL)
    font_title = get_font(max(32, w // 22), bold=True)
    font_body = get_font(max(18, w // 38))
    font_label = get_font(max(16, w // 42))
    draw_text_centered(draw, "MEET THE MAKER", h // 12 - 10, font_title, GOLD, w)
    # Photo placeholder
    cx, cy = w // 2, h // 6 + 100
    draw_circle(draw, cx, cy, 70, fill=LIGHT_PINK, outline=GOLD, width=2)
    draw_text_centered(draw, "[PHOTO]", cy - 10, font_label, SOFT_GRAY, w)
    # Info
    draw_text_centered(draw, "[YOUR NAME]", cy + 90, get_font(max(26, w // 28), bold=True), CHARCOAL, w)
    draw_text_centered(draw, "[Your title / role]", cy + 130, font_body, DARK_ROSE, w)
    draw_decorative_line(draw, cy + 165, w, GOLD, 1, w // 4)
    lines = [
        "\u2022 [Fun fact about you]",
        "\u2022 [What you do / create]",
        "\u2022 [Your mission / values]",
        "\u2022 [Personal detail]",
    ]
    y = cy + 190
    for line in lines:
        draw.text((w // 6, y), line, font=font_body, fill=CHARCOAL)
        y += 45
    draw_text_centered(draw, "@yourusername", h - 70, font_label, GOLD, w)
    return img


def create_about_bts(w, h, idx):
    """Behind the scenes template."""
    img = Image.new("RGB", (w, h), LIGHT_PINK)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(30, w // 22), bold=True)
    font_body = get_font(max(18, w // 38))
    draw_text_centered(draw, "BEHIND THE SCENES", 50, font_title, CHARCOAL, w)
    draw_decorative_line(draw, 100, w, GOLD, 2, w // 4)
    # Large image placeholder
    draw_rounded_rect(draw, (60, 130, w - 60, h // 2 + 80), 15, fill=WHITE, outline=SOFT_GRAY, width=2)
    draw_text_centered(draw, "[YOUR PHOTO / VIDEO HERE]", h // 3 + 20, get_font(max(22, w // 30)), SOFT_GRAY, w)
    # Caption area
    draw_rounded_rect(draw, (60, h // 2 + 110, w - 60, h - 60), 15, fill=CREAM)
    draw.text((90, h // 2 + 140), "[Share your process,", font=font_body, fill=CHARCOAL)
    draw.text((90, h // 2 + 175), "workspace, or a peek", font=font_body, fill=CHARCOAL)
    draw.text((90, h // 2 + 210), "behind the curtain]", font=font_body, fill=CHARCOAL)
    draw_text_centered(draw, "@yourusername", h - 45, get_font(max(14, w // 50)), DARK_ROSE, w)
    return img


def create_testimonial_1(w, h, idx):
    """Client testimonial template."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 60], fill=GOLD)
    draw.rectangle([0, h - 60, w, h], fill=GOLD)
    font_label = get_font(max(18, w // 40), bold=True)
    font_quote = get_font(max(24, w // 30))
    font_name = get_font(max(20, w // 36), bold=True)
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "CLIENT LOVE", 15, font_label, WHITE, w)
    # Stars
    star_str = "\u2605 \u2605 \u2605 \u2605 \u2605"
    draw_text_centered(draw, star_str, h // 4 - 20, get_font(max(28, w // 26)), GOLD, w)
    # Quote
    big_q = get_font(min(120, w // 6), bold=True)
    draw.text((60, h // 4 + 10), "\u201C", font=big_q, fill=LIGHT_PINK)
    draw.text((100, h // 3 + 30), "[Client testimonial", font=font_quote, fill=CHARCOAL)
    draw.text((100, h // 3 + 70), "goes right here.", font=font_quote, fill=CHARCOAL)
    draw.text((100, h // 3 + 110), "Keep it impactful!]", font=font_quote, fill=CHARCOAL)
    draw_decorative_line(draw, 2 * h // 3, w, DUSTY_ROSE, 2, 100)
    draw_text_centered(draw, "[CLIENT NAME]", 2 * h // 3 + 20, font_name, CHARCOAL, w)
    draw_text_centered(draw, "[Title / Business]", 2 * h // 3 + 55, font_sm, DARK_ROSE, w)
    draw_text_centered(draw, "@yourusername", h - 42, font_sm, WHITE, w)
    return img


def create_testimonial_2(w, h, idx):
    """Testimonial card style."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    # Card
    margin = 60
    draw_rounded_rect(draw, (margin, margin, w - margin, h - margin), 25, fill=WHITE, outline=GOLD, width=2)
    font_label = get_font(max(20, w // 36), bold=True)
    font_quote = get_font(max(22, w // 32))
    font_name = get_font(max(18, w // 38), bold=True)
    font_sm = get_font(max(14, w // 50))
    draw_text_centered(draw, "WHAT THEY SAY", margin + 40, font_label, GOLD, w)
    draw_circle(draw, w // 2, margin + 120, 40, fill=LIGHT_PINK, outline=GOLD, width=2)
    draw_text_centered(draw, "[PIC]", margin + 110, font_sm, SOFT_GRAY, w)
    y = margin + 190
    draw_text_centered(draw, '"[Amazing testimonial', y, font_quote, CHARCOAL, w)
    draw_text_centered(draw, 'text from your happy', y + 40, font_quote, CHARCOAL, w)
    draw_text_centered(draw, 'client goes here.]"', y + 80, font_quote, CHARCOAL, w)
    draw_decorative_line(draw, y + 130, w, GOLD, 1, margin + 40)
    draw_text_centered(draw, "[CLIENT NAME]", y + 155, font_name, CHARCOAL, w)
    draw_text_centered(draw, "[Business / Location]", y + 185, font_sm, DARK_ROSE, w)
    return img


def create_promo_discount(w, h, idx):
    """Discount code template."""
    img = Image.new("RGB", (w, h), CHARCOAL)
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, w - 30, h - 30], outline=GOLD, width=2)
    font_big = get_font(max(64, w // 10), bold=True)
    font_med = get_font(max(30, w // 24), bold=True)
    font_sm = get_font(max(20, w // 36))
    font_code = get_font(max(36, w // 18), bold=True)
    draw_text_centered(draw, "[XX]%", h // 5, font_big, GOLD, w)
    draw_text_centered(draw, "OFF", h // 5 + 80, font_med, DUSTY_ROSE, w)
    draw_wavy_line(draw, h // 2 - 30, w, GOLD, 3, 0.05, 1, 80)
    draw_text_centered(draw, "USE CODE:", h // 2 + 10, font_sm, CREAM, w)
    draw_rounded_rect(draw, (w // 5, h // 2 + 50, 4 * w // 5, h // 2 + 110), 10, fill=DUSTY_ROSE)
    draw_text_centered(draw, "[CODE]", h // 2 + 58, font_code, WHITE, w)
    draw_text_centered(draw, "[Valid until DATE]", 3 * h // 4, font_sm, SOFT_GRAY, w)
    draw_text_centered(draw, "LINK IN BIO", h - 80, font_sm, GOLD, w)
    return img


def create_carousel_cover(w, h, idx):
    """Carousel / swipe post cover."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 8], fill=GOLD)
    draw.rectangle([0, 7 * h // 8, w, h], fill=GOLD)
    font_sm = get_font(max(16, w // 42))
    font_big = get_font(max(40, w // 16), bold=True)
    font_med = get_font(max(24, w // 30))
    draw_text_centered(draw, "SWIPE \u2192", h // 16 - 5, font_sm, WHITE, w)
    draw_text_centered(draw, "[NUMBER]", h // 3, font_big, CHARCOAL, w)
    draw_text_centered(draw, "[TOPIC TITLE]", h // 3 + 60, font_big, DUSTY_ROSE, w)
    draw_decorative_line(draw, h // 2 + 30, w, GOLD, 2, w // 4)
    draw_text_centered(draw, "[Subtitle or description]", h // 2 + 60, font_med, DARK_ROSE, w)
    draw_text_centered(draw, "SAVE THIS POST!", 7 * h // 8 + 15, font_sm, WHITE, w)
    draw_corner_accents(draw, w, h, DUSTY_ROSE, 50, 2)
    return img


def create_story_highlight_cover(w, h, idx):
    """Story highlight cover icon style."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2
    draw_circle(draw, cx, cy, min(w, h) // 3, fill=CREAM, outline=GOLD, width=3)
    font = get_font(max(28, w // 26), bold=True)
    font_sm = get_font(max(18, w // 38))
    icons = ["FAQ", "TIPS", "SHOP", "NEW", "ABOUT", "BTS", "LOVE", "SALE"]
    icon = icons[idx % len(icons)]
    draw_text_centered(draw, icon, cy - 15, font, CHARCOAL, w)
    draw_text_centered(draw, "[HIGHLIGHT]", cy + min(w, h) // 3 + 20, font_sm, WHITE, w)
    draw_dots_pattern(draw, 20, 20, w // 4, h // 4, 25, 2, MEDIUM_ROSE)
    draw_dots_pattern(draw, 3 * w // 4, 3 * h // 4, w - 20, h - 20, 25, 2, MEDIUM_ROSE)
    return img


def create_story_this_or_that(w, h, idx):
    """This or That interactive story."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(36, w // 20), bold=True)
    font_opt = get_font(max(24, w // 30), bold=True)
    draw_text_centered(draw, "THIS OR THAT", 80, font_title, CHARCOAL, w)
    draw_decorative_line(draw, 140, w, GOLD, 2, w // 4)
    # Two halves
    mid_y = h // 2
    draw.rectangle([40, 180, w - 40, mid_y - 20], fill=DUSTY_ROSE, outline=GOLD, width=1)
    draw.rectangle([40, mid_y + 20, w - 40, h - 120], fill=LIGHT_PINK, outline=GOLD, width=1)
    draw_text_centered(draw, "[OPTION A]", (180 + mid_y - 20) // 2 - 15, font_opt, WHITE, w)
    draw_text_centered(draw, "[OPTION B]", (mid_y + 20 + h - 120) // 2 - 15, font_opt, CHARCOAL, w)
    # OR divider
    draw_circle(draw, w // 2, mid_y, 25, fill=GOLD)
    draw_text_centered(draw, "OR", mid_y - 12, get_font(max(18, w // 38), bold=True), WHITE, w)
    draw_text_centered(draw, "@yourusername", h - 80, get_font(max(16, w // 42)), DARK_ROSE, w)
    return img


def create_story_question(w, h, idx):
    """Question / AMA story."""
    img = Image.new("RGB", (w, h), CHARCOAL)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(38, w // 18), bold=True)
    font_body = get_font(max(22, w // 32))
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "ASK ME", h // 5, font_title, GOLD, w)
    draw_text_centered(draw, "ANYTHING", h // 5 + 55, font_title, GOLD, w)
    draw_wavy_line(draw, h // 3 + 20, w, DUSTY_ROSE, 5, 0.03, 2, 80)
    # Question box
    draw_rounded_rect(draw, (60, h // 2 - 40, w - 60, h // 2 + 80), 20, fill=CREAM)
    draw_text_centered(draw, "[Type your question...]", h // 2, font_body, SOFT_GRAY, w)
    draw_text_centered(draw, "TAP TO RESPOND", 2 * h // 3 + 40, font_sm, DUSTY_ROSE, w)
    draw_corner_accents(draw, w, h, GOLD, 60, 2)
    return img


def create_story_countdown(w, h, idx):
    """Countdown / launch story."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    font_big = get_font(max(50, w // 14), bold=True)
    font_med = get_font(max(28, w // 26), bold=True)
    font_num = get_font(max(72, w // 8), bold=True)
    font_sm = get_font(max(18, w // 38))
    draw_text_centered(draw, "LAUNCHING IN", h // 6, font_big, WHITE, w)
    draw_rounded_rect(draw, (w // 4, h // 3, 3 * w // 4, h // 3 + 150), 20, fill=WHITE)
    draw_text_centered(draw, "[X]", h // 3 + 20, font_num, CHARCOAL, w)
    draw_text_centered(draw, "DAYS", h // 3 + 100, font_med, GOLD, w)
    draw_decorative_line(draw, h // 2 + 100, w, GOLD, 2, w // 4)
    draw_text_centered(draw, "[Product / Event Name]", h // 2 + 130, font_med, WHITE, w)
    draw_text_centered(draw, "SET A REMINDER!", 3 * h // 4, font_sm, CREAM, w)
    draw_star(draw, 100, h - 200, 20, 10, 5, GOLD)
    draw_star(draw, w - 100, h - 200, 20, 10, 5, GOLD)
    return img


def create_story_poll(w, h, idx):
    """Poll story template."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 7], fill=GOLD)
    font_title = get_font(max(34, w // 20), bold=True)
    font_q = get_font(max(28, w // 26), bold=True)
    font_opt = get_font(max(22, w // 32))
    draw_text_centered(draw, "POLL TIME!", h // 14 - 10, font_title, WHITE, w)
    draw_text_centered(draw, "[YOUR QUESTION]", h // 4, font_q, CHARCOAL, w)
    draw_text_centered(draw, "[Add context here]", h // 4 + 50, get_font(max(18, w // 38)), DARK_ROSE, w)
    # Poll options
    opts = ["[OPTION A]", "[OPTION B]"]
    colors = [DUSTY_ROSE, LIGHT_PINK]
    for i, opt in enumerate(opts):
        y = h // 2 + i * 140
        draw_rounded_rect(draw, (80, y, w - 80, y + 100), 20, fill=colors[i], outline=GOLD, width=1)
        draw_text_centered(draw, opt, y + 30, font_opt, CHARCOAL if i == 1 else WHITE, w)
    draw_text_centered(draw, "TAP TO VOTE!", h - 150, get_font(max(20, w // 36), bold=True), GOLD, w)
    return img


def create_pinterest_tip(w, h, idx):
    """Long Pinterest tip pin."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 7], fill=DUSTY_ROSE)
    font_title = get_font(max(36, w // 18), bold=True)
    font_sub = get_font(max(22, w // 30))
    font_item = get_font(max(20, w // 34))
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "[NUMBER] TIPS FOR", h // 14 - 30, font_title, WHITE, w)
    draw_text_centered(draw, "[YOUR TOPIC]", h // 14 + 15, font_title, WHITE, w)
    items = ["[Tip number one here]", "[Tip number two here]", "[Tip number three here]",
             "[Tip number four here]", "[Tip number five here]"]
    y = h // 7 + 40
    spacing = (h - h // 7 - 140) // len(items)
    for i, item in enumerate(items):
        draw_circle(draw, 70, y + 15, 20, fill=GOLD)
        draw.text((60, y + 2), str(i + 1), font=get_font(max(18, w // 36), bold=True), fill=WHITE)
        draw.text((110, y + 2), item, font=font_item, fill=CHARCOAL)
        if i < len(items) - 1:
            draw.line([(70, y + 35), (70, y + spacing - 5)], fill=LIGHT_GOLD, width=1)
        y += spacing
    draw.rectangle([0, h - 70, w, h], fill=GOLD)
    draw_text_centered(draw, "SAVE FOR LATER | @yourusername", h - 50, font_sm, WHITE, w)
    return img


def create_pinterest_infographic(w, h, idx):
    """Pinterest infographic style."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 100], fill=CHARCOAL)
    font_title = get_font(max(30, w // 22), bold=True)
    font_body = get_font(max(18, w // 36))
    font_sm = get_font(max(14, w // 48))
    draw_text_centered(draw, "[INFOGRAPHIC TITLE]", 30, font_title, GOLD, w)
    sections = ["[Section 1 Title]", "[Section 2 Title]", "[Section 3 Title]", "[Section 4 Title]"]
    y = 130
    sec_h = (h - 200) // len(sections)
    for i, sec in enumerate(sections):
        bg = LIGHT_PINK if i % 2 == 0 else CREAM
        draw.rectangle([30, y, w - 30, y + sec_h - 10], fill=bg)
        draw_rounded_rect(draw, (50, y + 10, w - 50, y + 45), 5, fill=DUSTY_ROSE)
        draw_text_centered(draw, sec, y + 14, get_font(max(18, w // 36), bold=True), WHITE, w)
        draw.text((60, y + 55), "[Description text for this", font=font_body, fill=CHARCOAL)
        draw.text((60, y + 80), "section goes right here]", font=font_body, fill=CHARCOAL)
        y += sec_h
    draw.rectangle([0, h - 60, w, h], fill=GOLD)
    draw_text_centered(draw, "PIN THIS! | @yourusername", h - 42, font_sm, WHITE, w)
    return img


def create_pinterest_product(w, h, idx):
    """Pinterest product showcase pin."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(32, w // 20), bold=True)
    font_med = get_font(max(22, w // 30))
    font_sm = get_font(max(16, w // 42))
    font_price = get_font(max(36, w // 18), bold=True)
    draw_text_centered(draw, "[PRODUCT NAME]", 50, font_title, WHITE, w)
    draw_decorative_line(draw, 100, w, GOLD, 2, w // 4)
    # Product image area
    draw_rounded_rect(draw, (80, 130, w - 80, h // 2 + 50), 15, fill=WHITE, outline=GOLD, width=2)
    draw_text_centered(draw, "[PRODUCT IMAGE]", h // 3 + 20, font_med, SOFT_GRAY, w)
    # Details
    draw_rounded_rect(draw, (60, h // 2 + 80, w - 60, h - 120), 15, fill=CREAM)
    draw_text_centered(draw, font_price.size and "[Product description", h // 2 + 110, font_med, CHARCOAL, w)
    draw_text_centered(draw, "goes here with details]", h // 2 + 145, font_med, CHARCOAL, w)
    draw_text_centered(draw, "$[PRICE]", h // 2 + 210, font_price, GOLD, w)
    draw_rounded_rect(draw, (w // 4, h - 100, 3 * w // 4, h - 50), 25, fill=CHARCOAL)
    draw_text_centered(draw, "SHOP NOW", h - 90, font_sm, WHITE, w)
    return img


def create_ig_post_grid(w, h, idx):
    """Instagram photo grid placeholder."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 80], fill=DUSTY_ROSE)
    font_title = get_font(max(28, w // 26), bold=True)
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "[GRID TITLE]", 22, font_title, WHITE, w)
    # 2x2 grid
    gap = 20
    gx, gy = 40, 110
    cell_w = (w - 2 * gx - gap) // 2
    cell_h = (h - gy - 120 - gap) // 2
    labels = ["[IMAGE 1]", "[IMAGE 2]", "[IMAGE 3]", "[IMAGE 4]"]
    for r in range(2):
        for c in range(2):
            x0 = gx + c * (cell_w + gap)
            y0 = gy + r * (cell_h + gap)
            draw_rounded_rect(draw, (x0, y0, x0 + cell_w, y0 + cell_h), 10, fill=LIGHT_PINK, outline=DUSTY_ROSE, width=1)
            draw_text_centered(draw, labels[r * 2 + c], y0 + cell_h // 2 - 10, font_sm, SOFT_GRAY, w)
    draw_text_centered(draw, "@yourusername", h - 60, font_sm, DARK_ROSE, w)
    return img


def create_ig_post_quote_overlay(w, h, idx):
    """Quote with background overlay feel."""
    img = Image.new("RGB", (w, h), MEDIUM_ROSE)
    draw = ImageDraw.Draw(img)
    # Gradient-like effect with rectangles
    for i in range(10):
        alpha_y = int(h * i / 10)
        shade = tuple(max(0, c - i * 5) for c in DUSTY_ROSE)
        draw.rectangle([0, alpha_y, w, alpha_y + h // 10], fill=shade)
    # Overlay card
    draw_rounded_rect(draw, (80, h // 4, w - 80, 3 * h // 4), 20, fill=(255, 255, 255))
    font_q = get_font(max(30, w // 24), bold=True)
    font_a = get_font(max(18, w // 38))
    draw_text_centered(draw, '"[YOUR', h // 3 + 10, font_q, CHARCOAL, w)
    draw_text_centered(draw, 'INSPIRING', h // 3 + 55, font_q, CHARCOAL, w)
    draw_text_centered(draw, 'QUOTE]"', h // 3 + 100, font_q, CHARCOAL, w)
    draw_diamond(draw, w // 2, h // 3 + 155, 8, GOLD)
    draw_text_centered(draw, "- @yourusername", h // 3 + 180, font_a, GOLD, w)
    return img


def create_ig_post_announcement(w, h, idx):
    """Big announcement post."""
    img = Image.new("RGB", (w, h), GOLD)
    draw = ImageDraw.Draw(img)
    draw_rounded_rect(draw, (30, 30, w - 30, h - 30), 0, fill=CREAM, outline=CHARCOAL, width=3)
    font_big = get_font(max(52, w // 12), bold=True)
    font_med = get_font(max(26, w // 28))
    font_sm = get_font(max(18, w // 38))
    draw_text_centered(draw, "BIG", h // 4 - 10, font_big, GOLD, w)
    draw_text_centered(draw, "ANNOUNCEMENT", h // 4 + 60, font_big, CHARCOAL, w)
    draw_decorative_line(draw, h // 2 + 10, w, GOLD, 3, 80)
    draw_text_centered(draw, "[Your exciting news", h // 2 + 40, font_med, CHARCOAL, w)
    draw_text_centered(draw, "goes right here!]", h // 2 + 80, font_med, CHARCOAL, w)
    draw_text_centered(draw, "[DATE / DETAILS]", 2 * h // 3 + 20, font_sm, DARK_ROSE, w)
    draw_star(draw, 100, h - 100, 18, 9, 5, GOLD)
    draw_star(draw, w - 100, h - 100, 18, 9, 5, GOLD)
    return img


def create_ig_post_stat(w, h, idx):
    """Statistics / numbers showcase."""
    img = Image.new("RGB", (w, h), CHARCOAL)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(30, w // 24), bold=True)
    font_num = get_font(max(48, w // 14), bold=True)
    font_label = get_font(max(18, w // 38))
    draw_text_centered(draw, "[YOUR BRAND] BY THE NUMBERS", 50, font_title, GOLD, w)
    draw_decorative_line(draw, 100, w, DUSTY_ROSE, 2, w // 4)
    stats = [("[XXX]+", "[Metric One]"), ("[XX]%", "[Metric Two]"), ("[X,XXX]", "[Metric Three]")]
    y = 160
    spacing = (h - 240) // len(stats)
    for num, label in stats:
        draw_text_centered(draw, num, y, font_num, DUSTY_ROSE, w)
        draw_text_centered(draw, label, y + 60, font_label, CREAM, w)
        y += spacing
    draw_corner_accents(draw, w, h, GOLD, 50, 2)
    return img


def create_ig_post_before_after(w, h, idx):
    """Before / After split template."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(30, w // 24), bold=True)
    font_label = get_font(max(22, w // 32), bold=True)
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "THE TRANSFORMATION", 30, font_title, CHARCOAL, w)
    draw_decorative_line(draw, 75, w, GOLD, 2, w // 4)
    # Two halves
    mid = w // 2
    draw.rectangle([40, 100, mid - 10, h - 100], fill=LIGHT_PINK, outline=DUSTY_ROSE, width=1)
    draw.rectangle([mid + 10, 100, w - 40, h - 100], fill=WHITE, outline=GOLD, width=1)
    draw_text_centered(draw, "BEFORE", 110, font_label, DARK_ROSE, mid)
    # shift for right half
    bbox = draw.textbbox((0, 0), "AFTER", font=font_label)
    tw = bbox[2] - bbox[0]
    draw.text((mid + 10 + (mid - 50 - tw) // 2, 110), "AFTER", font=font_label, fill=GOLD)
    draw.text((60, h // 2 - 10), "[BEFORE\n IMAGE]", font=font_sm, fill=SOFT_GRAY)
    draw.text((mid + 30, h // 2 - 10), "[AFTER\n IMAGE]", font=font_sm, fill=SOFT_GRAY)
    draw_text_centered(draw, "@yourusername", h - 70, font_sm, DARK_ROSE, w)
    return img


def create_ig_post_freebie(w, h, idx):
    """Free resource / lead magnet post."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    font_free = get_font(max(56, w // 12), bold=True)
    font_med = get_font(max(28, w // 26), bold=True)
    font_sm = get_font(max(20, w // 36))
    draw_text_centered(draw, "FREE", h // 5, font_free, WHITE, w)
    draw_text_centered(draw, "[RESOURCE NAME]", h // 5 + 80, font_med, CHARCOAL, w)
    draw_decorative_line(draw, h // 3 + 30, w, GOLD, 2, w // 4)
    bullets = ["\u2713 [Benefit one]", "\u2713 [Benefit two]", "\u2713 [Benefit three]"]
    y = h // 2 - 20
    for b in bullets:
        draw.text((w // 5, y), b, font=font_sm, fill=WHITE)
        y += 50
    draw_rounded_rect(draw, (w // 4, 3 * h // 4, 3 * w // 4, 3 * h // 4 + 55), 28, fill=CHARCOAL)
    draw_text_centered(draw, "LINK IN BIO", 3 * h // 4 + 10, font_sm, GOLD, w)
    return img


def create_story_link(w, h, idx):
    """Story with link sticker area."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    # Top decorative band
    draw.rectangle([0, 0, w, 120], fill=DUSTY_ROSE)
    draw_dots_pattern(draw, 10, 10, w, 110, 30, 2, MEDIUM_ROSE)
    font_title = get_font(max(36, w // 20), bold=True)
    font_body = get_font(max(22, w // 32))
    font_sm = get_font(max(18, w // 38))
    draw_text_centered(draw, "NEW [THING]!", 40, font_title, WHITE, w)
    # Content area
    draw_rounded_rect(draw, (60, 160, w - 60, h // 2 + 100), 20, fill=WHITE, outline=GOLD, width=2)
    draw_text_centered(draw, "[YOUR IMAGE OR", h // 3, font_body, SOFT_GRAY, w)
    draw_text_centered(draw, "GRAPHIC HERE]", h // 3 + 35, font_body, SOFT_GRAY, w)
    # Link sticker placeholder
    draw_rounded_rect(draw, (w // 4, h // 2 + 150, 3 * w // 4, h // 2 + 220), 30, fill=CHARCOAL)
    draw_text_centered(draw, "[LINK STICKER]", h // 2 + 165, font_sm, WHITE, w)
    draw_text_centered(draw, "TAP ABOVE TO SHOP!", h // 2 + 260, font_body, CHARCOAL, w)
    draw_text_centered(draw, "@yourusername", h - 100, font_sm, DARK_ROSE, w)
    return img


def create_story_reminder(w, h, idx):
    """Reminder / save this story."""
    img = Image.new("RGB", (w, h), CHARCOAL)
    draw = ImageDraw.Draw(img)
    font_big = get_font(max(44, w // 16), bold=True)
    font_med = get_font(max(26, w // 28))
    font_sm = get_font(max(18, w // 38))
    draw_text_centered(draw, "REMINDER", h // 5, font_big, GOLD, w)
    draw_wavy_line(draw, h // 5 + 70, w, DUSTY_ROSE, 5, 0.03, 2, 80)
    # Content card
    draw_rounded_rect(draw, (50, h // 3, w - 50, 2 * h // 3 + 40), 20, fill=CREAM)
    draw_text_centered(draw, "[Your important", h // 3 + 40, font_med, CHARCOAL, w)
    draw_text_centered(draw, "reminder message", h // 3 + 80, font_med, CHARCOAL, w)
    draw_text_centered(draw, "goes right here]", h // 3 + 120, font_med, CHARCOAL, w)
    draw_diamond(draw, w // 2, 2 * h // 3 + 10, 8, GOLD)
    draw_text_centered(draw, "\U0001F516 SAVE THIS", 3 * h // 4 + 20, font_sm, DUSTY_ROSE, w)
    draw_corner_accents(draw, w, h, GOLD, 60, 2)
    return img


def create_story_product_feature(w, h, idx):
    """Product feature story."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h // 8], fill=GOLD)
    font_label = get_font(max(20, w // 36), bold=True)
    font_title = get_font(max(34, w // 20), bold=True)
    font_body = get_font(max(20, w // 34))
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "FEATURED PRODUCT", h // 16 - 5, font_label, WHITE, w)
    # Product image area
    draw_rounded_rect(draw, (80, h // 8 + 30, w - 80, h // 2 + 50), 15, fill=LIGHT_PINK, outline=DUSTY_ROSE, width=1)
    draw_text_centered(draw, "[PRODUCT IMAGE]", h // 3 + 10, font_body, SOFT_GRAY, w)
    draw_text_centered(draw, "[PRODUCT NAME]", h // 2 + 90, font_title, CHARCOAL, w)
    draw_text_centered(draw, "$[PRICE]", h // 2 + 140, get_font(max(30, w // 22), bold=True), GOLD, w)
    bullets = ["\u2713 [Feature one]", "\u2713 [Feature two]", "\u2713 [Feature three]"]
    y = h // 2 + 200
    for b in bullets:
        draw.text((w // 5, y), b, font=font_body, fill=CHARCOAL)
        y += 45
    draw_rounded_rect(draw, (w // 4, h - 180, 3 * w // 4, h - 120), 28, fill=DUSTY_ROSE)
    draw_text_centered(draw, "SHOP NOW", h - 168, font_body, WHITE, w)
    draw_text_centered(draw, "@yourusername", h - 80, font_sm, DARK_ROSE, w)
    return img


def create_story_testimonial(w, h, idx):
    """Story testimonial."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    font_title = get_font(max(32, w // 22), bold=True)
    font_quote = get_font(max(22, w // 32))
    font_name = get_font(max(18, w // 38), bold=True)
    font_sm = get_font(max(16, w // 42))
    draw_text_centered(draw, "\u2605 \u2605 \u2605 \u2605 \u2605", h // 6, get_font(max(30, w // 24)), GOLD, w)
    draw_text_centered(draw, "HAPPY CLIENT", h // 6 + 50, font_title, WHITE, w)
    draw_rounded_rect(draw, (50, h // 3, w - 50, 2 * h // 3 + 40), 20, fill=CREAM)
    draw.text((80, h // 3 + 30), '"[Client testimonial', font=font_quote, fill=CHARCOAL)
    draw.text((80, h // 3 + 65), 'text goes right here.', font=font_quote, fill=CHARCOAL)
    draw.text((80, h // 3 + 100), 'Keep it genuine and', font=font_quote, fill=CHARCOAL)
    draw.text((80, h // 3 + 135), 'impactful!]"', font=font_quote, fill=CHARCOAL)
    draw_decorative_line(draw, 2 * h // 3 - 20, w, GOLD, 1, 100)
    draw_text_centered(draw, "[CLIENT NAME]", 2 * h // 3, font_name, CHARCOAL, w)
    draw_text_centered(draw, "SWIPE UP TO SHOP", 3 * h // 4 + 40, font_sm, WHITE, w)
    return img


def create_pinterest_checklist(w, h, idx):
    """Pinterest checklist pin."""
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 120], fill=CHARCOAL)
    font_title = get_font(max(30, w // 22), bold=True)
    font_item = get_font(max(18, w // 36))
    font_sm = get_font(max(14, w // 48))
    draw_text_centered(draw, "[TOPIC] CHECKLIST", 35, font_title, GOLD, w)
    draw_text_centered(draw, "Your complete guide", 75, font_sm, CREAM, w)
    items = [
        "\u2610  [Checklist item one]",
        "\u2610  [Checklist item two]",
        "\u2610  [Checklist item three]",
        "\u2610  [Checklist item four]",
        "\u2610  [Checklist item five]",
        "\u2610  [Checklist item six]",
        "\u2610  [Checklist item seven]",
        "\u2610  [Checklist item eight]",
    ]
    y = 150
    spacing = (h - 250) // len(items)
    for i, item in enumerate(items):
        bg = LIGHT_PINK if i % 2 == 0 else CREAM
        draw.rectangle([30, y, w - 30, y + spacing - 5], fill=bg)
        draw.text((60, y + (spacing - 25) // 2), item, font=font_item, fill=CHARCOAL)
        y += spacing
    draw.rectangle([0, h - 60, w, h], fill=DUSTY_ROSE)
    draw_text_centered(draw, "PIN THIS! | @yourusername", h - 42, font_sm, WHITE, w)
    return img


def create_pinterest_quote(w, h, idx):
    """Pinterest quote pin (tall format)."""
    img = Image.new("RGB", (w, h), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)
    draw_rounded_rect(draw, (40, 40, w - 40, h - 40), 20, fill=CREAM, outline=GOLD, width=2)
    font_q = get_font(max(32, w // 20), bold=True)
    font_a = get_font(max(20, w // 32))
    font_sm = get_font(max(14, w // 48))
    big_q = get_font(min(150, w // 4), bold=True)
    draw.text((80, h // 5), "\u201C", font=big_q, fill=LIGHT_PINK)
    draw_text_centered(draw, "[YOUR", h // 3 + 20, font_q, CHARCOAL, w)
    draw_text_centered(draw, "INSPIRATIONAL", h // 3 + 65, font_q, CHARCOAL, w)
    draw_text_centered(draw, "QUOTE", h // 3 + 110, font_q, CHARCOAL, w)
    draw_text_centered(draw, "GOES HERE]", h // 3 + 155, font_q, CHARCOAL, w)
    draw_decorative_line(draw, h // 3 + 210, w, GOLD, 2, 100)
    draw_text_centered(draw, "- [AUTHOR NAME]", h // 3 + 240, font_a, GOLD, w)
    draw_text_centered(draw, "PIN FOR INSPIRATION | @yourusername", h - 80, font_sm, DARK_ROSE, w)
    return img


def create_pinterest_how_to(w, h, idx):
    """Pinterest how-to / tutorial pin."""
    img = Image.new("RGB", (w, h), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 130], fill=GOLD)
    font_title = get_font(max(28, w // 24), bold=True)
    font_step = get_font(max(20, w // 34), bold=True)
    font_desc = get_font(max(16, w // 42))
    font_sm = get_font(max(14, w // 48))
    draw_text_centered(draw, "HOW TO", 20, font_title, WHITE, w)
    draw_text_centered(draw, "[YOUR TOPIC]", 60, font_title, CHARCOAL, w)
    steps = [
        ("STEP 1", "[First step description]"),
        ("STEP 2", "[Second step description]"),
        ("STEP 3", "[Third step description]"),
        ("STEP 4", "[Fourth step description]"),
    ]
    y = 160
    step_h = (h - 240) // len(steps)
    for i, (title, desc) in enumerate(steps):
        draw_rounded_rect(draw, (40, y, w - 40, y + step_h - 15), 12, fill=WHITE if i % 2 == 0 else LIGHT_PINK, outline=DUSTY_ROSE, width=1)
        draw_circle(draw, 80, y + step_h // 2 - 8, 20, fill=DUSTY_ROSE)
        draw.text((71, y + step_h // 2 - 20), str(i + 1), font=font_step, fill=WHITE)
        draw.text((120, y + step_h // 3 - 5), title, font=font_step, fill=CHARCOAL)
        draw.text((120, y + step_h // 3 + 25), desc, font=font_desc, fill=DARK_ROSE)
        y += step_h
    draw.rectangle([0, h - 55, w, h], fill=CHARCOAL)
    draw_text_centered(draw, "SAVE FOR LATER | @yourusername", h - 38, font_sm, GOLD, w)
    return img


# ===========================================================================
# MAIN GENERATION
# ===========================================================================

def generate_all_templates():
    """Generate all 50 templates."""
    random.seed(42)  # Reproducible

    # === 25 Instagram Post Templates (1080x1080) ===
    ig_post_generators = [
        # Quotes (5)
        (create_quote_template_1, "ig_post_quote_01"),
        (create_quote_template_2, "ig_post_quote_02"),
        (create_quote_template_3, "ig_post_quote_03"),
        (create_quote_template_4, "ig_post_quote_04"),
        (create_quote_template_5, "ig_post_quote_05"),
        # Promo/Sale (5)
        (create_promo_sale, "ig_post_sale_06"),
        (create_promo_new, "ig_post_new_07"),
        (create_promo_coming_soon, "ig_post_coming_soon_08"),
        (create_promo_launch, "ig_post_launch_09"),
        (create_promo_discount, "ig_post_discount_10"),
        # Tips/List (5)
        (create_tips_template_1, "ig_post_tips_11"),
        (create_tips_template_2, "ig_post_howto_12"),
        (create_tips_template_3, "ig_post_checklist_13"),
        (create_carousel_cover, "ig_post_carousel_14"),
        (create_ig_post_grid, "ig_post_grid_15"),
        # About / BTS (5)
        (create_about_me, "ig_post_aboutme_16"),
        (create_about_bts, "ig_post_bts_17"),
        (create_ig_post_announcement, "ig_post_announce_18"),
        (create_ig_post_stat, "ig_post_stats_19"),
        (create_ig_post_before_after, "ig_post_beforeafter_20"),
        # Testimonial + misc (5)
        (create_testimonial_1, "ig_post_testimonial_21"),
        (create_testimonial_2, "ig_post_testimonial_22"),
        (create_ig_post_quote_overlay, "ig_post_quoteoverlay_23"),
        (create_ig_post_freebie, "ig_post_freebie_24"),
        (create_story_highlight_cover, "ig_post_highlight_25"),
    ]

    # === 15 Instagram Story Templates (1080x1920) ===
    ig_story_generators = [
        (create_quote_template_1, "ig_story_quote_01"),
        (create_quote_template_4, "ig_story_quote_02"),
        (create_promo_sale, "ig_story_sale_03"),
        (create_promo_coming_soon, "ig_story_comingsoon_04"),
        (create_tips_template_1, "ig_story_tips_05"),
        (create_story_this_or_that, "ig_story_thisorthat_06"),
        (create_story_question, "ig_story_ama_07"),
        (create_story_countdown, "ig_story_countdown_08"),
        (create_story_poll, "ig_story_poll_09"),
        (create_about_me, "ig_story_aboutme_10"),
        (create_story_link, "ig_story_link_11"),
        (create_story_reminder, "ig_story_reminder_12"),
        (create_story_product_feature, "ig_story_product_13"),
        (create_story_testimonial, "ig_story_testimonial_14"),
        (create_testimonial_2, "ig_story_testimonial2_15"),
    ]

    # === 10 Pinterest Pin Templates (1000x1500) ===
    pin_generators = [
        (create_pinterest_tip, "pin_tips_01"),
        (create_pinterest_infographic, "pin_infographic_02"),
        (create_pinterest_product, "pin_product_03"),
        (create_pinterest_checklist, "pin_checklist_04"),
        (create_pinterest_quote, "pin_quote_05"),
        (create_pinterest_how_to, "pin_howto_06"),
        (create_quote_template_3, "pin_quote_07"),
        (create_tips_template_3, "pin_checklist2_08"),
        (create_promo_sale, "pin_sale_09"),
        (create_testimonial_1, "pin_testimonial_10"),
    ]

    total = len(ig_post_generators) + len(ig_story_generators) + len(pin_generators)
    count = 0

    print(f"Generating {total} social media templates...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Instagram Posts
    print("=== Instagram Post Templates (1080x1080) ===")
    for i, (gen_func, name) in enumerate(ig_post_generators):
        img = gen_func(1080, 1080, i)
        filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
        img.save(filepath, "PNG")
        count += 1
        print(f"  [{count}/{total}] {name}.png")

    # Instagram Stories
    print("\n=== Instagram Story Templates (1080x1920) ===")
    for i, (gen_func, name) in enumerate(ig_story_generators):
        img = gen_func(1080, 1920, i)
        filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
        img.save(filepath, "PNG")
        count += 1
        print(f"  [{count}/{total}] {name}.png")

    # Pinterest Pins
    print("\n=== Pinterest Pin Templates (1000x1500) ===")
    for i, (gen_func, name) in enumerate(pin_generators):
        img = gen_func(1000, 1500, i)
        filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
        img.save(filepath, "PNG")
        count += 1
        print(f"  [{count}/{total}] {name}.png")

    print(f"\nDone! Generated {count} templates in {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_templates()
