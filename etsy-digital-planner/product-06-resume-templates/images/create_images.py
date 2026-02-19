#!/usr/bin/env python3
"""Generate 10 Etsy listing images for Professional Resume Template Bundle."""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# --- Constants ---
W, H = 2400, 2400
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), "templates")

# Color palette
NAVY = (27, 42, 74)
SLATE = (74, 111, 165)
LIGHT_GRAY = (240, 242, 245)
WHITE = (255, 255, 255)
GOLD = (201, 169, 110)
CHARCOAL = (51, 51, 51)
DARK_GRAY = (100, 100, 100)
SOFT_NAVY = (35, 55, 95)
VERY_LIGHT = (248, 249, 252)


def get_font(size, bold=False):
    paths = []
    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def text_height(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


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


def centered_text(draw, y, text, font, fill):
    tw = text_width(draw, text, font)
    draw.text(((W - tw) // 2, y), text, fill=fill, font=font)


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if text_width(draw, test, font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def load_template_thumbnails(target_h=500):
    """Load all 10 resume templates as thumbnails."""
    thumbs = []
    names = [
        "resume_01_classic.png", "resume_02_modern.png", "resume_03_creative.png",
        "resume_04_minimalist.png", "resume_05_executive.png", "resume_06_tech.png",
        "resume_07_elegant.png", "resume_08_bold.png", "resume_09_academic.png",
        "resume_10_compact.png",
    ]
    for name in names:
        path = os.path.join(TEMPLATES_DIR, name)
        if os.path.exists(path):
            t = Image.open(path)
            ratio = target_h / t.height
            new_w = int(t.width * ratio)
            t = t.resize((new_w, target_h), Image.LANCZOS)
            thumbs.append(t)
    return thumbs


def add_shadow(img, thumb, pos, offset=8, shadow_color=(0, 0, 0, 60)):
    """Paste a thumbnail with a subtle drop shadow."""
    shadow = Image.new("RGBA", (thumb.width + offset, thumb.height + offset), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle([offset, offset, thumb.width + offset, thumb.height + offset], fill=shadow_color)
    img.paste(Image.alpha_composite(Image.new("RGBA", shadow.size, (0, 0, 0, 0)), shadow), pos, shadow)
    img.paste(thumb, pos)


# ============================================================
# Image 1: Hero - All 10 resumes in grid display
# ============================================================
def create_hero():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Title at top
    title_font = get_font(72, bold=True)
    centered_text(draw, 60, "PROFESSIONAL RESUME", title_font, WHITE)
    sub_font = get_font(56, bold=True)
    centered_text(draw, 150, "TEMPLATE BUNDLE", sub_font, GOLD)

    # Load templates and arrange in 2 rows of 5
    thumbs = load_template_thumbnails(target_h=440)
    if thumbs:
        thumb_w = thumbs[0].width
        spacing = 25
        total_w = 5 * thumb_w + 4 * spacing
        start_x = (W - total_w) // 2

        for row in range(2):
            for col in range(5):
                idx = row * 5 + col
                if idx < len(thumbs):
                    x = start_x + col * (thumb_w + spacing)
                    y_pos = 280 + row * (440 + spacing)
                    # Shadow effect
                    draw.rectangle([x + 6, y_pos + 6, x + thumb_w + 6, y_pos + 440 + 6], fill=(15, 25, 50))
                    img.paste(thumbs[idx], (x, y_pos))

    # Bottom text
    bottom_font = get_font(48, bold=True)
    centered_text(draw, 1520, "10 UNIQUE DESIGNS  |  ATS-FRIENDLY  |  PRINT-READY", bottom_font, WHITE)

    # Gold accent line
    draw.rectangle([300, 1600, W - 300, 1604], fill=GOLD)

    # Subtitle
    desc_font = get_font(40)
    centered_text(draw, 1640, "Instant Download  |  Easy to Customize  |  Word & Google Docs", desc_font, LIGHT_GRAY)

    # Price badge
    draw_rounded_rect(draw, (W // 2 - 180, 1730, W // 2 + 180, 1830), 20, GOLD)
    price_font = get_font(64, bold=True)
    centered_text(draw, 1745, "ONLY $8.99", price_font, NAVY)

    img.save(os.path.join(OUTPUT_DIR, "listing_01_hero.jpg"), "JPEG", quality=95)
    print("  Created listing_01_hero.jpg")


# ============================================================
# Image 2: What's Included
# ============================================================
def create_whats_included():
    img = Image.new("RGB", (W, H), VERY_LIGHT)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 220], fill=NAVY)
    title_font = get_font(72, bold=True)
    centered_text(draw, 60, "WHAT'S INCLUDED", title_font, WHITE)

    y = 300
    items = [
        ("10", "Professional Resume Templates", "Unique designs for every career stage"),
        ("10", "Matching Cover Letters", "Coordinated designs for a complete package"),
        ("ATS", "Friendly Formatting", "Passes automated screening systems"),
        ("300", "DPI Print-Ready Files", "Crisp, professional quality printing"),
        ("A4+", "US Letter Sizes", "Compatible with standard paper sizes"),
    ]

    check_font = get_font(72, bold=True)
    item_font = get_font(48, bold=True)
    desc_font = get_font(36)

    for num, title, desc in items:
        # Number/icon circle
        draw_rounded_rect(draw, (180, y, 340, y + 130), 20, NAVY)
        nw = text_width(draw, num, check_font)
        draw.text((260 - nw // 2, y + 18), num, fill=GOLD, font=check_font)

        # Text
        draw.text((400, y + 10), title, fill=NAVY, font=item_font)
        draw.text((400, y + 72), desc, fill=DARK_GRAY, font=desc_font)

        # Divider
        y += 160
        if y < 1200:
            draw.line([(180, y - 10), (W - 180, y - 10)], fill=LIGHT_GRAY, width=2)

    # Bottom section
    y += 40
    draw.rectangle([0, y, W, H], fill=NAVY)

    features_font = get_font(42, bold=True)
    small_font = get_font(34)

    bonus_items = [
        "Easy-to-edit placeholders",
        "Step-by-step editing guide",
        "Font pairing suggestions",
        "Color customization tips",
    ]

    centered_text(draw, y + 30, "BONUS FEATURES", features_font, GOLD)
    by = y + 100
    for item in bonus_items:
        centered_text(draw, by, "\u2713  " + item, small_font, WHITE)
        by += 50

    img.save(os.path.join(OUTPUT_DIR, "listing_02_whats_included.jpg"), "JPEG", quality=95)
    print("  Created listing_02_whats_included.jpg")


# ============================================================
# Image 3: Templates 1-3 Close-up
# ============================================================
def create_showcase_1_3():
    img = Image.new("RGB", (W, H), LIGHT_GRAY)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 180], fill=NAVY)
    title_font = get_font(60, bold=True)
    centered_text(draw, 50, "CLASSIC  |  MODERN  |  CREATIVE", title_font, WHITE)

    thumbs = load_template_thumbnails(target_h=750)
    if len(thumbs) >= 3:
        thumb_w = thumbs[0].width
        spacing = 50
        total_w = 3 * thumb_w + 2 * spacing
        start_x = (W - total_w) // 2

        labels = ["Classic", "Modern", "Creative"]
        label_font = get_font(42, bold=True)

        for i in range(3):
            x = start_x + i * (thumb_w + spacing)
            y_pos = 260
            # Shadow
            draw.rectangle([x + 8, y_pos + 8, x + thumb_w + 8, y_pos + 750 + 8], fill=(180, 180, 180))
            img.paste(thumbs[i], (x, y_pos))

            # Label
            lw = text_width(draw, labels[i], label_font)
            draw.text((x + (thumb_w - lw) // 2, y_pos + 770), labels[i], fill=NAVY, font=label_font)

    # Bottom bar
    draw.rectangle([0, H - 200, W, H], fill=NAVY)
    bottom_font = get_font(44, bold=True)
    centered_text(draw, H - 160, "Part of the 10-Template Professional Bundle", bottom_font, GOLD)
    small_font = get_font(36)
    centered_text(draw, H - 100, "ATS-Friendly  |  Print-Ready  |  Easy to Edit", small_font, WHITE)

    img.save(os.path.join(OUTPUT_DIR, "listing_03_showcase_1_3.jpg"), "JPEG", quality=95)
    print("  Created listing_03_showcase_1_3.jpg")


# ============================================================
# Image 4: Templates 4-6 Close-up
# ============================================================
def create_showcase_4_6():
    img = Image.new("RGB", (W, H), LIGHT_GRAY)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 180], fill=NAVY)
    title_font = get_font(60, bold=True)
    centered_text(draw, 50, "MINIMALIST  |  EXECUTIVE  |  TECH", title_font, WHITE)

    thumbs = load_template_thumbnails(target_h=750)
    if len(thumbs) >= 6:
        selected = thumbs[3:6]
        thumb_w = selected[0].width
        spacing = 50
        total_w = 3 * thumb_w + 2 * spacing
        start_x = (W - total_w) // 2

        labels = ["Minimalist", "Executive", "Tech"]
        label_font = get_font(42, bold=True)

        for i in range(3):
            x = start_x + i * (thumb_w + spacing)
            y_pos = 260
            draw.rectangle([x + 8, y_pos + 8, x + thumb_w + 8, y_pos + 750 + 8], fill=(180, 180, 180))
            img.paste(selected[i], (x, y_pos))

            lw = text_width(draw, labels[i], label_font)
            draw.text((x + (thumb_w - lw) // 2, y_pos + 770), labels[i], fill=NAVY, font=label_font)

    draw.rectangle([0, H - 200, W, H], fill=NAVY)
    bottom_font = get_font(44, bold=True)
    centered_text(draw, H - 160, "Part of the 10-Template Professional Bundle", bottom_font, GOLD)
    small_font = get_font(36)
    centered_text(draw, H - 100, "ATS-Friendly  |  Print-Ready  |  Easy to Edit", small_font, WHITE)

    img.save(os.path.join(OUTPUT_DIR, "listing_04_showcase_4_6.jpg"), "JPEG", quality=95)
    print("  Created listing_04_showcase_4_6.jpg")


# ============================================================
# Image 5: Templates 7-10 Close-up
# ============================================================
def create_showcase_7_10():
    img = Image.new("RGB", (W, H), LIGHT_GRAY)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 180], fill=NAVY)
    title_font = get_font(52, bold=True)
    centered_text(draw, 50, "ELEGANT  |  BOLD  |  ACADEMIC  |  COMPACT", title_font, WHITE)

    thumbs = load_template_thumbnails(target_h=650)
    if len(thumbs) >= 10:
        selected = thumbs[6:10]
        thumb_w = selected[0].width
        spacing = 35
        total_w = 4 * thumb_w + 3 * spacing
        start_x = (W - total_w) // 2

        labels = ["Elegant", "Bold", "Academic", "Compact"]
        label_font = get_font(38, bold=True)

        for i in range(4):
            x = start_x + i * (thumb_w + spacing)
            y_pos = 300
            draw.rectangle([x + 8, y_pos + 8, x + thumb_w + 8, y_pos + 650 + 8], fill=(180, 180, 180))
            img.paste(selected[i], (x, y_pos))

            lw = text_width(draw, labels[i], label_font)
            draw.text((x + (thumb_w - lw) // 2, y_pos + 670), labels[i], fill=NAVY, font=label_font)

    draw.rectangle([0, H - 200, W, H], fill=NAVY)
    bottom_font = get_font(44, bold=True)
    centered_text(draw, H - 160, "Part of the 10-Template Professional Bundle", bottom_font, GOLD)
    small_font = get_font(36)
    centered_text(draw, H - 100, "ATS-Friendly  |  Print-Ready  |  Easy to Edit", small_font, WHITE)

    img.save(os.path.join(OUTPUT_DIR, "listing_05_showcase_7_10.jpg"), "JPEG", quality=95)
    print("  Created listing_05_showcase_7_10.jpg")


# ============================================================
# Image 6: Key Features
# ============================================================
def create_key_features():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 250], fill=NAVY)
    title_font = get_font(72, bold=True)
    centered_text(draw, 40, "KEY FEATURES", title_font, WHITE)
    sub_font = get_font(44)
    centered_text(draw, 140, "Professional Templates Built for Results", sub_font, GOLD)

    features = [
        ("ATS-FRIENDLY", "Optimized formatting that passes\nautomated tracking systems"),
        ("PRINT-READY", "300 DPI high-resolution files\nfor crisp, professional prints"),
        ("EASY TO EDIT", "Simple placeholder text - just\nreplace with your information"),
        ("MODERN DESIGNS", "Contemporary layouts that stand\nout to hiring managers"),
        ("MULTIPLE FORMATS", "Compatible with Word, Google\nDocs, and PDF export"),
        ("INSTANT DOWNLOAD", "Get your templates immediately\nafter purchase - no waiting"),
    ]

    # 2x3 grid
    cols = 2
    card_w = 950
    card_h = 320
    x_spacing = (W - cols * card_w) // (cols + 1)
    y_start = 340
    y_spacing = 50

    feat_title_font = get_font(44, bold=True)
    feat_desc_font = get_font(34)

    for idx, (title, desc) in enumerate(features):
        col = idx % cols
        row = idx // cols
        x = x_spacing + col * (card_w + x_spacing)
        y = y_start + row * (card_h + y_spacing)

        # Card background
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, VERY_LIGHT)

        # Gold accent bar on left
        draw.rectangle([x, y + 20, x + 8, y + card_h - 20], fill=GOLD)

        # Icon area
        draw_rounded_rect(draw, (x + 40, y + 40, x + 130, y + 130), 15, NAVY)
        icon_font = get_font(48, bold=True)
        icons = ["\u2713", "\u2699", "\u270E", "\u2605", "\u2630", "\u21E9"]
        iw = text_width(draw, icons[idx], icon_font)
        draw.text((x + 85 - iw // 2, y + 55), icons[idx], fill=GOLD, font=icon_font)

        # Text
        draw.text((x + 160, y + 50), title, fill=NAVY, font=feat_title_font)
        desc_y = y + 110
        for line in desc.split("\n"):
            draw.text((x + 160, desc_y), line, fill=DARK_GRAY, font=feat_desc_font)
            desc_y += 44

    # Bottom
    draw.rectangle([0, H - 160, W, H], fill=NAVY)
    bottom_font = get_font(48, bold=True)
    centered_text(draw, H - 120, "10 Templates  |  Instant Download  |  $8.99", bottom_font, GOLD)

    img.save(os.path.join(OUTPUT_DIR, "listing_06_key_features.jpg"), "JPEG", quality=95)
    print("  Created listing_06_key_features.jpg")


# ============================================================
# Image 7: How to Customize / Edit Guide
# ============================================================
def create_edit_guide():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 220], fill=NAVY)
    title_font = get_font(68, bold=True)
    centered_text(draw, 60, "HOW TO CUSTOMIZE", title_font, WHITE)

    steps = [
        ("1", "DOWNLOAD", "Download your template files\ninstantly after purchase"),
        ("2", "OPEN", "Open in Microsoft Word or\nGoogle Docs"),
        ("3", "EDIT", "Replace placeholder text with\nyour personal information"),
        ("4", "CUSTOMIZE", "Adjust colors, fonts, and\nlayout to your preference"),
        ("5", "EXPORT", "Save as PDF for a polished,\nprofessional finish"),
        ("6", "APPLY", "Send your resume and land\nyour dream job!"),
    ]

    step_num_font = get_font(80, bold=True)
    step_title_font = get_font(46, bold=True)
    step_desc_font = get_font(34)

    y_start = 320
    for idx, (num, title, desc) in enumerate(steps):
        row = idx // 2
        col = idx % 2
        x = 150 + col * 1150
        y = y_start + row * 380

        # Step number circle
        cx, cy = x + 50, y + 50
        draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=NAVY)
        nw = text_width(draw, num, step_num_font)
        draw.text((cx - nw // 2, cy - 45), num, fill=GOLD, font=step_num_font)

        # Arrow to next (horizontal)
        if col == 0:
            draw.line([(x + 900, y + 50), (x + 1050, y + 50)], fill=GOLD, width=4)
            # Arrow head
            draw.polygon([(x + 1050, y + 35), (x + 1080, y + 50), (x + 1050, y + 65)], fill=GOLD)

        # Step title and description
        draw.text((x + 120, y + 10), title, fill=NAVY, font=step_title_font)
        desc_y = y + 70
        for line in desc.split("\n"):
            draw.text((x + 120, desc_y), line, fill=DARK_GRAY, font=step_desc_font)
            desc_y += 44

    # Bottom
    draw.rectangle([0, H - 280, W, H], fill=LIGHT_GRAY)
    tip_font = get_font(40, bold=True)
    tip_desc = get_font(34)
    centered_text(draw, H - 240, "PRO TIP", tip_font, NAVY)
    centered_text(draw, H - 180, "Always save as PDF before sending to preserve formatting.", tip_desc, DARK_GRAY)
    centered_text(draw, H - 120, "Our templates are designed to work perfectly in both Word and Google Docs!", tip_desc, DARK_GRAY)

    img.save(os.path.join(OUTPUT_DIR, "listing_07_edit_guide.jpg"), "JPEG", quality=95)
    print("  Created listing_07_edit_guide.jpg")


# ============================================================
# Image 8: Before/After
# ============================================================
def create_before_after():
    img = Image.new("RGB", (W, H), LIGHT_GRAY)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 200], fill=NAVY)
    title_font = get_font(64, bold=True)
    centered_text(draw, 55, "TEMPLATE  vs  FILLED RESUME", title_font, WHITE)

    # Load a template for "before"
    thumbs = load_template_thumbnails(target_h=850)

    half_w = W // 2

    # Before side (template)
    draw.rectangle([60, 260, half_w - 30, 280], fill=SLATE)
    label_font = get_font(48, bold=True)
    bw = text_width(draw, "TEMPLATE", label_font)
    draw.text(((half_w - 60 - bw) // 2 + 60, 300), "TEMPLATE", fill=SLATE, font=label_font)

    if len(thumbs) >= 2:
        thumb = thumbs[1]  # Modern template
        tx = (half_w - 60 - thumb.width) // 2 + 60
        draw.rectangle([tx + 6, 376, tx + thumb.width + 6, 376 + 850 + 6], fill=(180, 180, 180))
        img.paste(thumb, (tx, 370))

    # Arrow in center
    arrow_y = H // 2 - 20
    draw.polygon([
        (half_w - 60, arrow_y - 30),
        (half_w + 60, arrow_y),
        (half_w - 60, arrow_y + 30),
    ], fill=GOLD)

    # After side (filled - simulate with colored template)
    draw.rectangle([half_w + 30, 260, W - 60, 280], fill=GOLD)
    aw = text_width(draw, "FILLED RESUME", label_font)
    draw.text((half_w + 30 + (half_w - 90 - aw) // 2, 300), "FILLED RESUME", fill=GOLD, font=label_font)

    if len(thumbs) >= 2:
        # Use the same template but with a green tint overlay to simulate "filled"
        filled = thumbs[1].copy()
        overlay = Image.new("RGB", filled.size, (240, 255, 240))
        filled = Image.blend(filled, overlay, 0.08)
        fx = half_w + 30 + (half_w - 90 - filled.width) // 2
        draw.rectangle([fx + 6, 376, fx + filled.width + 6, 376 + 850 + 6], fill=(180, 180, 180))
        img.paste(filled, (fx, 370))

        # Add "CUSTOMIZED" stamp
        stamp_font = get_font(36, bold=True)
        stamp_text = "YOUR INFO HERE"
        sw = text_width(draw, stamp_text, stamp_font)
        sx = fx + (filled.width - sw) // 2
        draw_rounded_rect(draw, (sx - 20, 600, sx + sw + 20, 660), 10, GOLD)
        draw.text((sx, 608), stamp_text, fill=NAVY, font=stamp_font)

    # Bottom
    draw.rectangle([0, H - 180, W, H], fill=NAVY)
    bottom_font = get_font(44, bold=True)
    centered_text(draw, H - 140, "Easy Placeholder Text  \u2192  Replace with Your Details  \u2192  Done!", bottom_font, WHITE)
    small_font = get_font(36)
    centered_text(draw, H - 80, "Works with Microsoft Word & Google Docs", small_font, GOLD)

    img.save(os.path.join(OUTPUT_DIR, "listing_08_before_after.jpg"), "JPEG", quality=95)
    print("  Created listing_08_before_after.jpg")


# ============================================================
# Image 9: Testimonials
# ============================================================
def create_testimonials():
    img = Image.new("RGB", (W, H), VERY_LIGHT)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 240], fill=NAVY)
    title_font = get_font(68, bold=True)
    centered_text(draw, 40, "WHAT CUSTOMERS SAY", title_font, WHITE)
    star_font = get_font(56)
    centered_text(draw, 140, "\u2605 \u2605 \u2605 \u2605 \u2605", star_font, GOLD)

    testimonials = [
        {
            "text": "These templates are incredible! I used the Modern design and got called for 3 interviews within the first week. The ATS-friendly format really makes a difference.",
            "name": "Sarah M.",
            "title": "Marketing Manager",
            "stars": 5,
        },
        {
            "text": "Best resume templates I've found on Etsy. Clean, professional designs that are super easy to customize. The editing guide was very helpful too!",
            "name": "James K.",
            "title": "Software Engineer",
            "stars": 5,
        },
        {
            "text": "I bought this bundle for my whole team during our career transition. Every single person found a template they loved. Amazing value for the price!",
            "name": "Lisa R.",
            "title": "HR Director",
            "stars": 5,
        },
        {
            "text": "The Executive template is stunning. It perfectly showcases my experience and skills. I've already recommended this to several colleagues.",
            "name": "David P.",
            "title": "Senior Consultant",
            "stars": 5,
        },
    ]

    quote_font = get_font(32)
    name_font = get_font(36, bold=True)
    title_f = get_font(28)
    star_sm = get_font(32)

    card_w = 1000
    card_h = 380
    x_margin = (W - 2 * card_w) // 3
    y_start = 320

    for idx, test in enumerate(testimonials):
        col = idx % 2
        row = idx // 2
        x = x_margin + col * (card_w + x_margin)
        y = y_start + row * (card_h + 60)

        # Card
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, WHITE)
        # Gold top accent
        draw.rectangle([x + 20, y, x + card_w - 20, y + 5], fill=GOLD)

        # Stars
        stars = "\u2605 " * test["stars"]
        draw.text((x + 40, y + 25), stars, fill=GOLD, font=star_sm)

        # Quote
        qy = y + 70
        for line in wrap_text(draw, f'"{test["text"]}"', quote_font, card_w - 80):
            draw.text((x + 40, qy), line, fill=CHARCOAL, font=quote_font)
            qy += 40

        # Author
        draw.text((x + 40, y + card_h - 80), f"\u2014 {test['name']}", fill=NAVY, font=name_font)
        draw.text((x + 40, y + card_h - 40), test["title"], fill=DARK_GRAY, font=title_f)

    # Bottom
    draw.rectangle([0, H - 200, W, H], fill=NAVY)
    bottom_font = get_font(48, bold=True)
    centered_text(draw, H - 160, "Join 2,000+ Happy Customers", bottom_font, WHITE)
    small_font = get_font(38)
    centered_text(draw, H - 100, "4.9/5 Average Rating  |  Instant Download", small_font, GOLD)

    img.save(os.path.join(OUTPUT_DIR, "listing_09_testimonials.jpg"), "JPEG", quality=95)
    print("  Created listing_09_testimonials.jpg")


# ============================================================
# Image 10: Bundle CTA with $8.99 price
# ============================================================
def create_bundle_cta():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Gold border
    draw.rectangle([30, 30, W - 30, H - 30], outline=GOLD, width=4)
    draw.rectangle([50, 50, W - 50, H - 50], outline=GOLD, width=2)

    y = 150

    # Title
    title_font = get_font(80, bold=True)
    centered_text(draw, y, "PROFESSIONAL RESUME", title_font, WHITE)
    y += 100
    centered_text(draw, y, "TEMPLATE BUNDLE", title_font, GOLD)
    y += 130

    # Features list
    feat_font = get_font(44, bold=True)
    features = [
        "\u2713  10 Unique Professional Designs",
        "\u2713  ATS-Friendly Formatting",
        "\u2713  Print-Ready 300 DPI Quality",
        "\u2713  Word & Google Docs Compatible",
        "\u2713  Step-by-Step Editing Guide",
        "\u2713  Instant Digital Download",
    ]
    for feat in features:
        centered_text(draw, y, feat, feat_font, WHITE)
        y += 65

    y += 40

    # Decorative line
    draw.rectangle([400, y, W - 400, y + 3], fill=GOLD)
    y += 50

    # Price section
    was_font = get_font(42)
    centered_text(draw, y, "VALUE: $49.99", was_font, DARK_GRAY)
    # Strikethrough
    tw = text_width(draw, "VALUE: $49.99", was_font)
    sx = (W - tw) // 2
    draw.line([(sx, y + 22), (sx + tw, y + 22)], fill=DARK_GRAY, width=3)
    y += 70

    # Big price
    price_font = get_font(140, bold=True)
    centered_text(draw, y, "$8.99", price_font, GOLD)
    y += 180

    # Savings
    save_font = get_font(48, bold=True)
    draw_rounded_rect(draw, (W // 2 - 280, y, W // 2 + 280, y + 70), 15, GOLD)
    centered_text(draw, y + 8, "SAVE 82% - LIMITED TIME!", save_font, NAVY)
    y += 110

    # CTA
    cta_font = get_font(56, bold=True)
    draw_rounded_rect(draw, (W // 2 - 400, y, W // 2 + 400, y + 100), 20, WHITE)
    centered_text(draw, y + 16, "ADD TO CART NOW", cta_font, NAVY)
    y += 140

    # Bottom text
    small_font = get_font(34)
    centered_text(draw, y, "Instant Download  |  No Shipping Required", small_font, LIGHT_GRAY)
    y += 50
    centered_text(draw, y, "30-Day Money-Back Guarantee", small_font, GOLD)

    img.save(os.path.join(OUTPUT_DIR, "listing_10_bundle_cta.jpg"), "JPEG", quality=95)
    print("  Created listing_10_bundle_cta.jpg")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Generating 10 listing images...")
    create_hero()
    create_whats_included()
    create_showcase_1_3()
    create_showcase_4_6()
    create_showcase_7_10()
    create_key_features()
    create_edit_guide()
    create_before_after()
    create_testimonials()
    create_bundle_cta()
    print("Done! All 10 listing images created.")
