#!/usr/bin/env python3
"""
Create 10 Etsy listing images (2400x2400 JPG) for the Social Media Templates Bundle.
Uses the dusty rose/blush theme.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# === Color Palette ===
DUSTY_ROSE = (232, 196, 196)
CREAM = (255, 245, 238)
CHARCOAL = (51, 51, 51)
GOLD = (201, 169, 110)
WHITE = (255, 255, 255)
LIGHT_PINK = (245, 225, 225)
SOFT_GRAY = (180, 180, 180)
MEDIUM_ROSE = (220, 175, 175)
DARK_ROSE = (180, 140, 140)
LIGHT_GOLD = (220, 200, 160)
VERY_LIGHT_PINK = (250, 240, 240)

W, H = 2400, 2400
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), "templates")


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
        return
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_center_x(draw, text, font, canvas_width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    return (canvas_width - tw) // 2


def draw_text_centered(draw, text, y, font, fill, canvas_width):
    x = text_center_x(draw, text, font, canvas_width)
    draw.text((x, y), text, font=font, fill=fill)


def draw_text_centered_in_rect(draw, text, x0, y0, x1, y1, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - tw) // 2
    y = y0 + (y1 - y0 - th) // 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_phone_mockup(draw, x, y, pw, ph, label="", screen_img=None, base_img=None):
    """Draw a phone mockup rectangle with screen."""
    # Phone body (dark)
    radius = 30
    draw_rounded_rect(draw, (x, y, x + pw, y + ph), radius, fill=CHARCOAL)
    # Screen area
    sx, sy = x + 15, y + 50
    sw, sh = pw - 30, ph - 100
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE)
    if screen_img and base_img:
        try:
            scr = screen_img.resize((sw, sh), Image.LANCZOS)
            base_img.paste(scr, (sx, sy))
        except:
            draw_text_centered_in_rect(draw, label, sx, sy, sx + sw, sy + sh, get_font(20), SOFT_GRAY)
    elif label:
        draw_text_centered_in_rect(draw, label, sx, sy, sx + sw, sy + sh, get_font(20), SOFT_GRAY)
    # Notch
    nw = pw // 3
    draw_rounded_rect(draw, (x + pw // 2 - nw // 2, y, x + pw // 2 + nw // 2, y + 20), 10, fill=CHARCOAL)
    return sx, sy, sw, sh


def load_template(name):
    """Load a template image."""
    path = os.path.join(TEMPLATE_DIR, name)
    if os.path.exists(path):
        return Image.open(path)
    return None


def draw_corner_accents(draw, w, h, color=GOLD, size=80, thickness=4):
    m = 60
    draw.line([(m, m), (m + size, m)], fill=color, width=thickness)
    draw.line([(m, m), (m, m + size)], fill=color, width=thickness)
    draw.line([(w - m - size, m), (w - m, m)], fill=color, width=thickness)
    draw.line([(w - m, m), (w - m, m + size)], fill=color, width=thickness)
    draw.line([(m, h - m), (m + size, h - m)], fill=color, width=thickness)
    draw.line([(m, h - m - size), (m, h - m)], fill=color, width=thickness)
    draw.line([(w - m - size, h - m), (w - m, h - m)], fill=color, width=thickness)
    draw.line([(w - m, h - m - size), (w - m, h - m)], fill=color, width=thickness)


def draw_star(draw, cx, cy, outer_r, inner_r, points_count, fill):
    pts = []
    for i in range(points_count * 2):
        angle = math.pi * i / points_count - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
    draw.polygon(pts, fill=fill)


# ===========================================================================
# LISTING IMAGE GENERATORS
# ===========================================================================

def create_image_01_hero():
    """Hero/cover image with mockup of templates on phone screens."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Background decorative elements
    draw.rectangle([0, 0, W, 200], fill=DUSTY_ROSE)
    draw.rectangle([0, H - 200, W, H], fill=DUSTY_ROSE)

    # Title
    font_big = get_font(100, bold=True)
    font_sub = get_font(48)
    font_sm = get_font(36)
    draw_text_centered(draw, "50 SOCIAL MEDIA", 60, font_big, WHITE, W)

    # Subtitle bar
    draw_text_centered(draw, "TEMPLATES BUNDLE", 240, get_font(80, bold=True), CHARCOAL, W)
    draw_text_centered(draw, "2026 EDITION", 350, get_font(56, bold=True), GOLD, W)

    # Phone mockups (3 phones)
    phone_w, phone_h = 380, 700
    templates_to_show = [
        ("ig_post_quote_01.png", "Quote"),
        ("ig_story_sale_03.png", "Story"),
        ("pin_tips_01.png", "Pin"),
    ]

    positions = [
        (W // 2 - phone_w - 250, 500),
        (W // 2 - phone_w // 2, 450),
        (W // 2 + 250, 500),
    ]

    for (tname, label), (px, py) in zip(templates_to_show, positions):
        tmpl = load_template(tname)
        sx, sy, sw, sh = draw_phone_mockup(draw, px, py, phone_w, phone_h, label, tmpl, img)
        draw = ImageDraw.Draw(img)  # refresh draw after paste

    # Bottom info
    draw_rounded_rect(draw, (600, 1300, 1800, 1420), 30, fill=GOLD)
    draw_text_centered(draw, "Instagram \u2022 Stories \u2022 Pinterest", 1330, get_font(44, bold=True), WHITE, W)

    # Feature badges
    badges = ["25 IG Posts", "15 IG Stories", "10 Pinterest Pins"]
    bx = 350
    for badge in badges:
        draw_rounded_rect(draw, (bx, 1500, bx + 500, 1580), 20, fill=WHITE, outline=DUSTY_ROSE, width=3)
        draw_text_centered_in_rect(draw, badge, bx, 1500, bx + 500, 1580, get_font(36, bold=True), CHARCOAL)
        bx += 570

    # Floating template previews
    preview_templates = [
        "ig_post_sale_06.png", "ig_post_tips_11.png", "ig_post_testimonial_21.png",
        "ig_post_coming_soon_08.png", "ig_post_freebie_24.png", "ig_post_aboutme_16.png"
    ]
    preview_size = 280
    start_x = 140
    y_row = 1680
    for i, tname in enumerate(preview_templates):
        tmpl = load_template(tname)
        px = start_x + i * (preview_size + 85)
        if tmpl:
            tmpl_resized = tmpl.resize((preview_size, preview_size), Image.LANCZOS)
            img.paste(tmpl_resized, (px, y_row))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (px, y_row, px + preview_size, y_row + preview_size), 10, fill=LIGHT_PINK, outline=DUSTY_ROSE, width=2)

    # Branding
    draw_text_centered(draw, "INSTANT DOWNLOAD \u2022 EASY TO CUSTOMIZE", 2050, get_font(36), DARK_ROSE, W)
    draw.rectangle([0, 2100, W, 2110], fill=GOLD)

    # Bottom CTA
    draw_text_centered(draw, "$12.99", 2150, get_font(80, bold=True), GOLD, W)
    draw_text_centered(draw, "BEST VALUE FOR YOUR SOCIAL MEDIA", 2270, get_font(40), CHARCOAL, W)
    draw_corner_accents(draw, W, H, GOLD, 100, 4)

    return img


def create_image_02_whats_included():
    """What's included overview."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 280], fill=CHARCOAL)
    font_title = get_font(80, bold=True)
    font_sub = get_font(48)
    font_med = get_font(40, bold=True)
    font_body = get_font(36)
    font_sm = get_font(30)

    draw_text_centered(draw, "WHAT'S INCLUDED", 50, font_title, GOLD, W)
    draw_text_centered(draw, "50 Templates \u2022 3 Sizes \u2022 Instant Download", 170, font_sub, CREAM, W)

    # Three columns
    sections = [
        ("INSTAGRAM POSTS", "25 Templates", "1080 x 1080 px", [
            "Quote templates", "Sale & promo", "Tips & lists",
            "About me", "Testimonials", "Announcements"
        ]),
        ("INSTAGRAM STORIES", "15 Templates", "1080 x 1920 px", [
            "Quote stories", "Poll & Q&A", "This or That",
            "Countdown", "Product features", "Testimonials"
        ]),
        ("PINTEREST PINS", "10 Templates", "1000 x 1500 px", [
            "Tip lists", "Infographics", "Product pins",
            "Checklists", "Quote pins", "How-to guides"
        ]),
    ]

    col_w = 680
    col_x_start = 100
    gap = 60
    for i, (title, count, size, items) in enumerate(sections):
        x = col_x_start + i * (col_w + gap)
        y = 340

        # Column header
        draw_rounded_rect(draw, (x, y, x + col_w, y + 120), 15, fill=DUSTY_ROSE)
        draw_text_centered_in_rect(draw, title, x, y, x + col_w, y + 70, font_med, WHITE)
        draw_text_centered_in_rect(draw, count, x, y + 55, x + col_w, y + 120, font_sm, CREAM)

        # Size badge
        draw_rounded_rect(draw, (x + 100, y + 140, x + col_w - 100, y + 195), 10, fill=GOLD)
        draw_text_centered_in_rect(draw, size, x + 100, y + 140, x + col_w - 100, y + 195, font_sm, WHITE)

        # Template preview thumbnails
        tmpl_names = {
            0: ["ig_post_quote_01.png", "ig_post_sale_06.png", "ig_post_tips_11.png"],
            1: ["ig_story_quote_01.png", "ig_story_poll_09.png", "ig_story_link_11.png"],
            2: ["pin_tips_01.png", "pin_quote_05.png", "pin_product_03.png"],
        }
        ty = y + 220
        tw = 200
        tx = x + (col_w - 3 * tw - 20) // 2
        for j, tname in enumerate(tmpl_names[i]):
            tmpl = load_template(tname)
            if tmpl:
                th = int(tw * tmpl.height / tmpl.width)
                th = min(th, 300)
                tmpl_r = tmpl.resize((tw, th), Image.LANCZOS)
                img.paste(tmpl_r, (tx + j * (tw + 10), ty))
                draw = ImageDraw.Draw(img)
            else:
                draw_rounded_rect(draw, (tx + j * (tw + 10), ty, tx + j * (tw + 10) + tw, ty + 200), 5, fill=LIGHT_PINK)

        # Items list
        iy = ty + 320
        for item in items:
            draw.text((x + 40, iy), f"\u2713  {item}", font=font_body, fill=CHARCOAL)
            iy += 55

    # Bottom banner
    draw.rectangle([0, H - 200, W, H], fill=GOLD)
    draw_text_centered(draw, "50 PROFESSIONAL TEMPLATES \u2022 INSTANT DOWNLOAD", H - 150, font_med, WHITE, W)
    draw_text_centered(draw, "Easy to customize in any image editor", H - 90, font_sm, CREAM, W)

    return img


def create_image_03_ig_post_samples():
    """Instagram post template samples - grid of 6."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 220], fill=DUSTY_ROSE)
    font_title = get_font(72, bold=True)
    font_sub = get_font(40)
    draw_text_centered(draw, "INSTAGRAM POST TEMPLATES", 40, font_title, WHITE, W)
    draw_text_centered(draw, "25 Templates \u2022 1080 x 1080px", 140, font_sub, CREAM, W)

    # 3x2 grid of template previews
    templates = [
        "ig_post_quote_01.png", "ig_post_sale_06.png", "ig_post_tips_11.png",
        "ig_post_aboutme_16.png", "ig_post_testimonial_21.png", "ig_post_freebie_24.png"
    ]

    cols, rows = 3, 2
    margin = 80
    gap = 40
    cell_w = (W - 2 * margin - (cols - 1) * gap) // cols
    cell_h = cell_w  # square
    start_y = 300

    for idx, tname in enumerate(templates):
        r, c = divmod(idx, cols)
        cx = margin + c * (cell_w + gap)
        cy = start_y + r * (cell_h + gap)

        # Shadow
        draw_rounded_rect(draw, (cx + 8, cy + 8, cx + cell_w + 8, cy + cell_h + 8), 15, fill=SOFT_GRAY)

        tmpl = load_template(tname)
        if tmpl:
            tmpl_r = tmpl.resize((cell_w, cell_h), Image.LANCZOS)
            img.paste(tmpl_r, (cx, cy))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (cx, cy, cx + cell_w, cy + cell_h), 15, fill=WHITE, outline=DUSTY_ROSE, width=2)

    # Bottom info
    y_bottom = start_y + 2 * (cell_h + gap) + 40
    draw_text_centered(draw, "+ 19 MORE DESIGNS INCLUDED!", y_bottom, get_font(52, bold=True), CHARCOAL, W)
    draw.rectangle([0, H - 120, W, H], fill=GOLD)
    draw_text_centered(draw, "Quotes \u2022 Sales \u2022 Tips \u2022 About Me \u2022 Testimonials", H - 80, get_font(38), WHITE, W)

    return img


def create_image_04_ig_story_samples():
    """Instagram story template samples."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 220], fill=CHARCOAL)
    font_title = get_font(72, bold=True)
    font_sub = get_font(40)
    draw_text_centered(draw, "INSTAGRAM STORY TEMPLATES", 40, font_title, GOLD, W)
    draw_text_centered(draw, "15 Templates \u2022 1080 x 1920px", 140, font_sub, CREAM, W)

    # 5 story previews side by side
    templates = [
        "ig_story_quote_01.png", "ig_story_sale_03.png", "ig_story_thisorthat_06.png",
        "ig_story_poll_09.png", "ig_story_product_13.png"
    ]

    margin = 100
    gap = 40
    tw = (W - 2 * margin - (len(templates) - 1) * gap) // len(templates)
    th = int(tw * 1920 / 1080)
    start_y = 300

    for i, tname in enumerate(templates):
        tx = margin + i * (tw + gap)
        # Shadow
        draw_rounded_rect(draw, (tx + 6, start_y + 6, tx + tw + 6, start_y + th + 6), 12, fill=SOFT_GRAY)
        tmpl = load_template(tname)
        if tmpl:
            tmpl_r = tmpl.resize((tw, th), Image.LANCZOS)
            img.paste(tmpl_r, (tx, start_y))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (tx, start_y, tx + tw, start_y + th), 12, fill=LIGHT_PINK, outline=DUSTY_ROSE, width=2)

    y_bottom = start_y + th + 50
    draw_text_centered(draw, "+ 10 MORE STORY TEMPLATES!", y_bottom, get_font(52, bold=True), CHARCOAL, W)

    draw.rectangle([0, H - 120, W, H], fill=DUSTY_ROSE)
    draw_text_centered(draw, "Polls \u2022 Q&A \u2022 Countdowns \u2022 Testimonials \u2022 Links", H - 80, get_font(38), WHITE, W)

    return img


def create_image_05_pinterest_samples():
    """Pinterest pin template samples."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 220], fill=DUSTY_ROSE)
    font_title = get_font(72, bold=True)
    font_sub = get_font(40)
    draw_text_centered(draw, "PINTEREST PIN TEMPLATES", 40, font_title, WHITE, W)
    draw_text_centered(draw, "10 Templates \u2022 1000 x 1500px", 140, font_sub, CREAM, W)

    templates = [
        "pin_tips_01.png", "pin_infographic_02.png", "pin_product_03.png",
        "pin_checklist_04.png", "pin_quote_05.png"
    ]

    margin = 100
    gap = 40
    tw = (W - 2 * margin - (len(templates) - 1) * gap) // len(templates)
    th = int(tw * 1500 / 1000)
    start_y = 300

    for i, tname in enumerate(templates):
        tx = margin + i * (tw + gap)
        draw_rounded_rect(draw, (tx + 6, start_y + 6, tx + tw + 6, start_y + th + 6), 12, fill=SOFT_GRAY)
        tmpl = load_template(tname)
        if tmpl:
            tmpl_r = tmpl.resize((tw, th), Image.LANCZOS)
            img.paste(tmpl_r, (tx, start_y))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (tx, start_y, tx + tw, start_y + th), 12, fill=LIGHT_PINK, outline=DUSTY_ROSE, width=2)

    y_bottom = start_y + th + 50
    draw_text_centered(draw, "+ 5 MORE PIN DESIGNS!", y_bottom, get_font(52, bold=True), CHARCOAL, W)
    draw_text_centered(draw, "Optimized for Pinterest's algorithm", y_bottom + 70, get_font(38), DARK_ROSE, W)

    draw.rectangle([0, H - 120, W, H], fill=GOLD)
    draw_text_centered(draw, "Tips \u2022 Infographics \u2022 Products \u2022 Checklists \u2022 Quotes", H - 80, get_font(38), WHITE, W)

    return img


def create_image_06_color_palette():
    """Color palette and style guide."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 250], fill=CHARCOAL)
    font_title = get_font(72, bold=True)
    font_sub = get_font(42)
    font_med = get_font(36, bold=True)
    font_body = get_font(32)
    font_sm = get_font(28)

    draw_text_centered(draw, "COLOR PALETTE & STYLE GUIDE", 50, font_title, GOLD, W)
    draw_text_centered(draw, "Cohesive, Modern, Professional", 160, font_sub, CREAM, W)

    # Color swatches
    colors = [
        (DUSTY_ROSE, "Dusty Rose", "#E8C4C4"),
        (CREAM, "Cream", "#FFF5EE"),
        (CHARCOAL, "Charcoal", "#333333"),
        (GOLD, "Gold Accent", "#C9A96E"),
        (LIGHT_PINK, "Light Pink", "#F5E1E1"),
    ]

    swatch_size = 300
    gap = 60
    total_w = len(colors) * swatch_size + (len(colors) - 1) * gap
    start_x = (W - total_w) // 2
    y = 340

    for i, (color, name, hex_code) in enumerate(colors):
        sx = start_x + i * (swatch_size + gap)
        draw_rounded_rect(draw, (sx, y, sx + swatch_size, y + swatch_size), 20, fill=color, outline=SOFT_GRAY, width=2)
        draw_text_centered_in_rect(draw, name, sx, y + swatch_size + 10, sx + swatch_size, y + swatch_size + 55, font_med, CHARCOAL)
        draw_text_centered_in_rect(draw, hex_code, sx, y + swatch_size + 50, sx + swatch_size, y + swatch_size + 90, font_sm, SOFT_GRAY)

    # Style guide section
    y2 = y + swatch_size + 140
    draw.rectangle([100, y2, W - 100, y2 + 4], fill=GOLD)

    draw_text_centered(draw, "DESIGN STYLE", y2 + 30, font_title, CHARCOAL, W)

    # Style attributes
    style_items = [
        ("AESTHETIC", "Modern Minimalist"),
        ("MOOD", "Warm, Elegant, Professional"),
        ("FONTS", "Clean Sans-Serif Typography"),
        ("ELEMENTS", "Geometric Shapes, Gold Accents"),
        ("PERFECT FOR", "Small Business, Coaches, Creators"),
    ]

    y3 = y2 + 130
    for label, value in style_items:
        draw_rounded_rect(draw, (200, y3, 700, y3 + 60), 10, fill=DUSTY_ROSE)
        draw_text_centered_in_rect(draw, label, 200, y3, 700, y3 + 60, font_med, WHITE)
        draw.text((750, y3 + 10), value, font=font_body, fill=CHARCOAL)
        y3 += 85

    # Template preview collage on right side
    mini_templates = ["ig_post_quote_01.png", "ig_post_sale_06.png", "ig_post_tips_11.png",
                      "ig_post_testimonial_21.png"]
    mx = 1700
    my = y2 + 130
    ms = 280
    for i, tname in enumerate(mini_templates):
        tmpl = load_template(tname)
        r, c = divmod(i, 2)
        px = mx + c * (ms + 20)
        py = my + r * (ms + 20)
        if tmpl:
            tmpl_r = tmpl.resize((ms, ms), Image.LANCZOS)
            img.paste(tmpl_r, (px, py))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (px, py, px + ms, py + ms), 8, fill=LIGHT_PINK)

    # Bottom
    draw.rectangle([0, H - 150, W, H], fill=DUSTY_ROSE)
    draw_text_centered(draw, "CONSISTENT BRANDING ACROSS ALL PLATFORMS", H - 110, font_med, WHITE, W)
    draw_text_centered(draw, "Instagram \u2022 Stories \u2022 Pinterest", H - 60, font_sm, CREAM, W)

    return img


def create_image_07_how_to_use():
    """How to customize / use instructions."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 250], fill=GOLD)
    font_title = get_font(72, bold=True)
    font_sub = get_font(42)
    font_step_num = get_font(80, bold=True)
    font_step_title = get_font(44, bold=True)
    font_step_desc = get_font(34)
    font_sm = get_font(28)

    draw_text_centered(draw, "HOW TO USE YOUR TEMPLATES", 50, font_title, WHITE, W)
    draw_text_centered(draw, "Quick & Easy Customization", 160, font_sub, CHARCOAL, W)

    steps = [
        ("1", "DOWNLOAD", "Download your templates\ninstantly after purchase"),
        ("2", "OPEN", "Open in Canva, Photoshop,\nor any image editor"),
        ("3", "CUSTOMIZE", "Replace placeholder text\nwith your own content"),
        ("4", "EXPORT & POST", "Save as PNG/JPG and\npost to your social media!"),
    ]

    y = 340
    step_h = 420
    for i, (num, title, desc) in enumerate(steps):
        # Step box
        sx = 150
        sy = y + i * step_h

        # Number circle
        draw.ellipse([sx, sy + 20, sx + 120, sy + 140], fill=DUSTY_ROSE)
        draw_text_centered_in_rect(draw, num, sx, sy + 20, sx + 120, sy + 140, font_step_num, WHITE)

        # Title and description
        draw.text((sx + 160, sy + 30), title, font=font_step_title, fill=CHARCOAL)
        draw.text((sx + 160, sy + 90), desc, font=font_step_desc, fill=DARK_ROSE)

        # Arrow between steps
        if i < len(steps) - 1:
            draw.line([(sx + 60, sy + 150), (sx + 60, sy + step_h + 10)], fill=GOLD, width=3)
            # arrow head
            draw.polygon([(sx + 45, sy + step_h), (sx + 75, sy + step_h), (sx + 60, sy + step_h + 20)], fill=GOLD)

        # Preview on right side
        preview_map = {
            0: "ig_post_quote_01.png",
            1: "ig_post_sale_06.png",
            2: "ig_post_tips_11.png",
            3: "ig_post_freebie_24.png",
        }
        tmpl = load_template(preview_map[i])
        px = W - 600
        ps = 350
        if tmpl:
            tmpl_r = tmpl.resize((ps, ps), Image.LANCZOS)
            img.paste(tmpl_r, (px, sy))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (px, sy, px + ps, sy + ps), 10, fill=LIGHT_PINK)

    # Bottom
    draw.rectangle([0, H - 150, W, H], fill=CHARCOAL)
    draw_text_centered(draw, "WORKS WITH: Canva \u2022 Photoshop \u2022 GIMP \u2022 Any Image Editor", H - 110, font_step_title, GOLD, W)
    draw_text_centered(draw, "No design skills needed!", H - 55, font_sm, CREAM, W)

    return img


def create_image_08_before_after():
    """Before/after mockup."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 250], fill=DUSTY_ROSE)
    font_title = get_font(72, bold=True)
    font_sub = get_font(42)
    font_label = get_font(48, bold=True)
    font_body = get_font(34)

    draw_text_centered(draw, "BEFORE & AFTER", 50, font_title, WHITE, W)
    draw_text_centered(draw, "See the transformation!", 160, font_sub, CREAM, W)

    # Before side
    bx, by = 100, 350
    bw, bh = 1000, 1200
    draw_text_centered_in_rect(draw, "BEFORE", bx, by - 70, bx + bw, by, font_label, CHARCOAL)

    # "Ugly" before - plain boring post
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(240, 240, 240), outline=SOFT_GRAY, width=3)
    before_font = get_font(40)
    draw.text((bx + 100, by + 200), "My boring post", font=before_font, fill=SOFT_GRAY)
    draw.text((bx + 100, by + 280), "with no design...", font=before_font, fill=SOFT_GRAY)
    draw.text((bx + 100, by + 400), "Just plain text", font=get_font(34), fill=(200, 200, 200))
    draw.text((bx + 100, by + 460), "No branding", font=get_font(34), fill=(200, 200, 200))
    draw.text((bx + 100, by + 520), "Looks unprofessional", font=get_font(34), fill=(200, 200, 200))
    # Red X marks
    for yy in [by + 400, by + 460, by + 520]:
        draw.text((bx + 50, yy), "\u2717", font=get_font(34, bold=True), fill=(200, 100, 100))

    # After side
    ax = 1300
    draw_text_centered_in_rect(draw, "AFTER", ax, by - 70, ax + bw, by, font_label, GOLD)

    # Load actual template as the "after"
    tmpl = load_template("ig_post_quote_01.png")
    if tmpl:
        tmpl_r = tmpl.resize((bw, bh), Image.LANCZOS)
        img.paste(tmpl_r, (ax, by))
        draw = ImageDraw.Draw(img)
    else:
        draw_rounded_rect(draw, (ax, by, ax + bw, by + bh), 15, fill=LIGHT_PINK, outline=GOLD, width=3)

    # Check marks for after
    checks = ["Professional look", "Consistent branding", "More engagement"]
    cy = by + bh + 30
    for check in checks:
        draw.text((ax + 50, cy), f"\u2713  {check}", font=font_body, fill=CHARCOAL)
        cy += 50

    # Arrow between
    arrow_x = W // 2
    arrow_y = by + bh // 2
    draw.polygon([(arrow_x - 40, arrow_y - 30), (arrow_x + 40, arrow_y), (arrow_x - 40, arrow_y + 30)], fill=GOLD)

    # Bottom
    draw.rectangle([0, H - 180, W, H], fill=CHARCOAL)
    draw_text_centered(draw, "LEVEL UP YOUR SOCIAL MEDIA TODAY", H - 140, get_font(52, bold=True), GOLD, W)
    draw_text_centered(draw, "50 Templates \u2022 Instant Download \u2022 $12.99", H - 70, font_body, CREAM, W)

    return img


def create_image_09_testimonials():
    """Testimonials / social proof."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 280], fill=CHARCOAL)
    font_title = get_font(72, bold=True)
    font_sub = get_font(42)
    font_stars = get_font(44)
    font_quote = get_font(34)
    font_name = get_font(30, bold=True)
    font_sm = get_font(26)

    draw_text_centered(draw, "WHAT CUSTOMERS SAY", 50, font_title, GOLD, W)
    draw_text_centered(draw, "\u2605\u2605\u2605\u2605\u2605  5-Star Reviews", 170, font_sub, CREAM, W)

    testimonials = [
        {
            "text": '"These templates saved me SO much time!\nMy Instagram looks completely professional\nnow. Best purchase I\'ve made this year!"',
            "name": "Sarah M.",
            "title": "Small Business Owner",
        },
        {
            "text": '"I love the cohesive color palette. Everything\nmatches perfectly and my brand looks so\nput-together across all platforms."',
            "name": "Jessica K.",
            "title": "Life Coach",
        },
        {
            "text": '"As someone with zero design skills, these\ntemplates are a lifesaver. So easy to customize\nand they look amazing!"',
            "name": "Emily R.",
            "title": "Content Creator",
        },
        {
            "text": '"The Pinterest templates alone are worth the\nprice. My pin engagement has gone up 300%\nsince I started using these!"',
            "name": "Amanda L.",
            "title": "Blogger",
        },
    ]

    y = 350
    card_h = 400
    gap = 50
    for i, t in enumerate(testimonials):
        r, c = divmod(i, 2)
        cx = 80 + c * (W // 2 - 40)
        cy = y + r * (card_h + gap)
        cw = W // 2 - 120

        draw_rounded_rect(draw, (cx, cy, cx + cw, cy + card_h), 20, fill=WHITE, outline=DUSTY_ROSE, width=2)

        # Stars
        draw.text((cx + 40, cy + 20), "\u2605 \u2605 \u2605 \u2605 \u2605", font=font_stars, fill=GOLD)

        # Quote
        draw.text((cx + 40, cy + 80), t["text"], font=font_quote, fill=CHARCOAL)

        # Name
        draw.text((cx + 40, cy + card_h - 80), t["name"], font=font_name, fill=CHARCOAL)
        draw.text((cx + 40, cy + card_h - 45), t["title"], font=font_sm, fill=DARK_ROSE)

    # Stats bar
    stat_y = y + 2 * (card_h + gap) + 40
    draw.rectangle([0, stat_y, W, stat_y + 200], fill=DUSTY_ROSE)
    stats = [("500+", "Happy Customers"), ("4.9/5", "Average Rating"), ("50+", "5-Star Reviews")]
    sx = W // len(stats)
    for i, (num, label) in enumerate(stats):
        draw_text_centered_in_rect(draw, num, i * sx, stat_y, (i + 1) * sx, stat_y + 110, get_font(64, bold=True), WHITE)
        draw_text_centered_in_rect(draw, label, i * sx, stat_y + 100, (i + 1) * sx, stat_y + 190, font_name, CHARCOAL)

    # Bottom
    draw.rectangle([0, H - 120, W, H], fill=GOLD)
    draw_text_centered(draw, "JOIN HUNDREDS OF HAPPY CREATORS!", H - 80, get_font(44, bold=True), WHITE, W)

    return img


def create_image_10_cta():
    """Bundle CTA with pricing."""
    img = Image.new("RGB", (W, H), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)

    font_big = get_font(90, bold=True)
    font_title = get_font(72, bold=True)
    font_sub = get_font(48)
    font_med = get_font(40, bold=True)
    font_body = get_font(36)
    font_price = get_font(120, bold=True)
    font_sm = get_font(30)

    draw_corner_accents(draw, W, H, GOLD, 120, 5)

    draw_text_centered(draw, "GET THE COMPLETE", 120, font_title, WHITE, W)
    draw_text_centered(draw, "SOCIAL MEDIA BUNDLE", 220, font_big, CHARCOAL, W)

    draw.rectangle([W // 4, 370, 3 * W // 4, 375], fill=GOLD)

    # What's included recap
    items = [
        "\u2713  25 Instagram Post Templates (1080x1080)",
        "\u2713  15 Instagram Story Templates (1080x1920)",
        "\u2713  10 Pinterest Pin Templates (1000x1500)",
        "\u2713  Cohesive Dusty Rose Color Palette",
        "\u2713  Ready to Customize in Any Editor",
        "\u2713  Instant Digital Download",
    ]
    y = 430
    for item in items:
        draw_text_centered(draw, item, y, font_body, CHARCOAL, W)
        y += 65

    # Pricing section
    py = 850
    draw_rounded_rect(draw, (500, py, 1900, py + 400), 30, fill=WHITE, outline=GOLD, width=4)

    # Crossed out "original" price
    draw_text_centered(draw, "$39.99", py + 30, get_font(50), SOFT_GRAY, W)
    # Strikethrough
    bbox = draw.textbbox((0, 0), "$39.99", font=get_font(50))
    tw = bbox[2] - bbox[0]
    strike_x = (W - tw) // 2
    draw.line([(strike_x - 10, py + 55), (strike_x + tw + 10, py + 55)], fill=SOFT_GRAY, width=3)

    draw_text_centered(draw, "$12.99", py + 100, font_price, GOLD, W)
    draw_text_centered(draw, "LIMITED TIME OFFER", py + 260, font_med, DUSTY_ROSE, W)
    draw_text_centered(draw, "Save 68% \u2022 That's just $0.26 per template!", py + 320, font_sm, DARK_ROSE, W)

    # CTA button
    btn_y = 1320
    draw_rounded_rect(draw, (600, btn_y, 1800, btn_y + 120), 60, fill=CHARCOAL)
    draw_text_centered(draw, "ADD TO CART NOW", btn_y + 25, get_font(52, bold=True), GOLD, W)

    # Template preview strip
    preview_templates = [
        "ig_post_quote_01.png", "ig_post_sale_06.png", "ig_story_poll_09.png",
        "pin_tips_01.png", "ig_post_tips_11.png", "ig_post_testimonial_21.png",
        "ig_story_countdown_08.png", "pin_quote_05.png"
    ]
    ps = 240
    total_preview_w = len(preview_templates) * ps + (len(preview_templates) - 1) * 20
    pstart_x = (W - total_preview_w) // 2
    py2 = 1520
    for i, tname in enumerate(preview_templates):
        px = pstart_x + i * (ps + 20)
        tmpl = load_template(tname)
        if tmpl:
            tmpl_r = tmpl.resize((ps, ps), Image.LANCZOS)
            img.paste(tmpl_r, (px, py2))
            draw = ImageDraw.Draw(img)
        else:
            draw_rounded_rect(draw, (px, py2, px + ps, py2 + ps), 8, fill=LIGHT_PINK)

    # Bottom guarantees
    gy = 1830
    guarantees = ["\u2713 Instant Download", "\u2713 Lifetime Access", "\u2713 Commercial Use OK"]
    gx = W // len(guarantees)
    for i, g in enumerate(guarantees):
        draw_text_centered_in_rect(draw, g, i * gx, gy, (i + 1) * gx, gy + 60, font_med, WHITE)

    draw.rectangle([0, H - 200, W, H], fill=CHARCOAL)
    draw_text_centered(draw, "50 TEMPLATES \u2022 3 PLATFORMS \u2022 1 COHESIVE BRAND", H - 160, font_med, GOLD, W)
    draw_text_centered(draw, "Your social media glow-up starts here!", H - 90, font_body, CREAM, W)

    # Stars
    for cx in [200, 400, 2000, 2200]:
        draw_star(draw, cx, 1950, 15, 7, 5, GOLD)

    return img


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    generators = [
        (create_image_01_hero, "listing_01_hero"),
        (create_image_02_whats_included, "listing_02_whats_included"),
        (create_image_03_ig_post_samples, "listing_03_ig_post_samples"),
        (create_image_04_ig_story_samples, "listing_04_ig_story_samples"),
        (create_image_05_pinterest_samples, "listing_05_pinterest_samples"),
        (create_image_06_color_palette, "listing_06_color_palette"),
        (create_image_07_how_to_use, "listing_07_how_to_use"),
        (create_image_08_before_after, "listing_08_before_after"),
        (create_image_09_testimonials, "listing_09_testimonials"),
        (create_image_10_cta, "listing_10_cta"),
    ]

    print(f"Generating {len(generators)} listing images at {W}x{H}...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    for i, (gen_func, name) in enumerate(generators, 1):
        img = gen_func()
        filepath = os.path.join(OUTPUT_DIR, f"{name}.jpg")
        img.save(filepath, "JPEG", quality=95)
        print(f"  [{i}/{len(generators)}] {name}.jpg")

    print(f"\nDone! Generated {len(generators)} listing images.")


if __name__ == "__main__":
    main()
