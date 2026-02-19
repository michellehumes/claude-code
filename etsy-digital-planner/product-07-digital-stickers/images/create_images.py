#!/usr/bin/env python3
"""
Listing images for Digital Planner Stickers Bundle - 10 images at 2400x2400px.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# --- Constants ---
W, H = 2400, 2400
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STICKER_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "stickers")

# --- Color Palette ---
PINK = (244, 180, 197)
PEACH = (249, 198, 168)
YELLOW = (249, 228, 167)
MINT = (181, 216, 199)
SKY = (167, 199, 231)
LAVENDER = (197, 180, 227)
WHITE = (255, 255, 255)
CHARCOAL = (68, 68, 68)
LIGHT_PINK = (253, 235, 240)
LIGHT_BLUE = (230, 240, 250)
LIGHT_YELLOW = (255, 250, 230)
LIGHT_MINT = (230, 245, 235)
LIGHT_LAVENDER = (240, 235, 250)
COLORS = [PINK, PEACH, YELLOW, MINT, SKY, LAVENDER]


def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_font_regular(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
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
    if outline and width > 0:
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


def draw_text_centered(draw, text, cx, cy, font, fill=CHARCOAL):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=fill, font=font)


def draw_star(draw, cx, cy, r_outer, r_inner, fill=YELLOW, outline=CHARCOAL, width=2):
    coords = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = r_outer if i % 2 == 0 else r_inner
        coords.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(coords, fill=fill, outline=outline, width=width)


def draw_gradient_bg(img, color_top, color_bottom):
    """Draw a vertical gradient background."""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / H)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / H)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def load_sticker_sheet(name):
    """Try to load a sticker sheet from the stickers directory."""
    path = os.path.join(STICKER_DIR, name)
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    return None


def paste_sticker_preview(img, sheet, x, y, size):
    """Paste a resized sticker sheet preview onto image."""
    if sheet:
        preview = sheet.resize((size, size), Image.LANCZOS)
        # Create white background for the preview
        bg = Image.new("RGBA", (size, size), WHITE)
        bg.paste(preview, (0, 0), preview)
        img.paste(bg, (x, y))
        draw = ImageDraw.Draw(img)
        draw.rectangle([x, y, x + size, y + size], outline=CHARCOAL, width=3)


def draw_decorative_dots(draw, y_pos, count=20):
    """Draw decorative dots across the image."""
    for i in range(count):
        x = int(W * i / count) + 60
        color = COLORS[i % len(COLORS)]
        r = 8
        draw.ellipse([x - r, y_pos - r, x + r, y_pos + r], fill=color)


def draw_checkmark_icon(draw, x, y, size, color=MINT):
    draw_rounded_rect(draw, (x, y, x + size, y + size), radius=8, fill=color, outline=CHARCOAL, width=3)
    # Checkmark
    cx, cy = x + size // 2, y + size // 2
    draw.line([cx - size * 0.2, cy, cx - size * 0.05, cy + size * 0.2], fill=WHITE, width=4)
    draw.line([cx - size * 0.05, cy + size * 0.2, cx + size * 0.25, cy - size * 0.15], fill=WHITE, width=4)


# =================================================================
# Image 1: Hero Image
# =================================================================
def create_image_1():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_PINK, LIGHT_LAVENDER)
    draw = ImageDraw.Draw(img)

    # Title
    draw_text_centered(draw, "Digital Planner", W // 2, 180, get_font(110), CHARCOAL)
    draw_text_centered(draw, "Stickers Bundle", W // 2, 310, get_font(110), CHARCOAL)

    # Colorful underline
    for i, color in enumerate(COLORS):
        x_start = 500 + i * 230
        draw_rounded_rect(draw, (x_start, 400, x_start + 210, 418), radius=9, fill=color)

    # "200+" badge
    draw.ellipse([100, 100, 400, 400], fill=PINK, outline=CHARCOAL, width=4)
    draw_text_centered(draw, "200+", 250, 210, get_font(80), CHARCOAL)
    draw_text_centered(draw, "Stickers", 250, 290, get_font(36), CHARCOAL)

    # Tablet mockup
    tablet_x, tablet_y = 300, 500
    tablet_w, tablet_h = 1800, 1400
    draw_rounded_rect(draw, (tablet_x, tablet_y, tablet_x + tablet_w, tablet_y + tablet_h),
                      radius=40, fill=CHARCOAL, outline=CHARCOAL, width=0)
    draw_rounded_rect(draw, (tablet_x + 30, tablet_y + 30, tablet_x + tablet_w - 30, tablet_y + tablet_h - 30),
                      radius=20, fill=WHITE)

    # Place sticker sheet previews on tablet
    sheets = [
        "sheet_1_daily_planner.png", "sheet_2_motivational.png",
        "sheet_3_functional_tabs.png", "sheet_4_habit_tracker.png",
    ]
    preview_size = 380
    positions = [
        (tablet_x + 80, tablet_y + 80),
        (tablet_x + 500, tablet_y + 80),
        (tablet_x + 920, tablet_y + 80),
        (tablet_x + 1340, tablet_y + 80),
    ]
    for sheet_name, (px, py) in zip(sheets, positions):
        sheet = load_sticker_sheet(sheet_name)
        if sheet:
            paste_sticker_preview(img, sheet, px, py, preview_size)
        else:
            draw_rounded_rect(draw, (px, py, px + preview_size, py + preview_size),
                              radius=10, fill=COLORS[sheets.index(sheet_name) % len(COLORS)],
                              outline=CHARCOAL, width=2)

    # More sticker previews on tablet
    sheets2 = [
        "sheet_5_seasonal.png", "sheet_6_washi_tape.png",
        "sheet_7_speech_bubbles.png", "sheet_8_icons.png",
    ]
    positions2 = [
        (tablet_x + 80, tablet_y + 510),
        (tablet_x + 500, tablet_y + 510),
        (tablet_x + 920, tablet_y + 510),
        (tablet_x + 1340, tablet_y + 510),
    ]
    for sheet_name, (px, py) in zip(sheets2, positions2):
        sheet = load_sticker_sheet(sheet_name)
        if sheet:
            paste_sticker_preview(img, sheet, px, py, preview_size)
        else:
            draw_rounded_rect(draw, (px, py, px + preview_size, py + preview_size),
                              radius=10, fill=COLORS[sheets2.index(sheet_name) % len(COLORS)],
                              outline=CHARCOAL, width=2)

    # Bottom text
    draw_text_centered(draw, "GoodNotes  |  Notability  |  iPad  |  PNG",
                       W // 2, tablet_y + tablet_h - 60, get_font(40), WHITE)

    # Bottom bar
    draw_rounded_rect(draw, (200, 2050, 2200, 2150), radius=25, fill=PEACH, outline=CHARCOAL, width=3)
    draw_text_centered(draw, "Precropped PNG  |  Transparent Background  |  Instant Download",
                       W // 2, 2100, get_font(38), CHARCOAL)

    # Decorative corner stickers
    for i, color in enumerate(COLORS):
        draw.ellipse([2100 + (i % 3) * 60, 80 + (i // 3) * 60,
                      2140 + (i % 3) * 60, 120 + (i // 3) * 60], fill=color)

    return img


# =================================================================
# Image 2: What's Included
# =================================================================
def create_image_2():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_MINT, LIGHT_BLUE)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "What's Included", W // 2, 150, get_font(100), CHARCOAL)
    draw_decorative_dots(draw, 250)

    items = [
        ("8 Sticker Sheets", "2048 x 2048 px each", PINK),
        ("200+ Individual Stickers", "Precropped transparent PNG", PEACH),
        ("Daily Planner Set", "To-Do, Meeting, Deadline & more", YELLOW),
        ("Motivational Quotes", "25 inspirational phrases", MINT),
        ("Functional Tabs", "Month, day & numbered tabs", SKY),
        ("Habit Tracker Icons", "Water, exercise, sleep & more", LAVENDER),
        ("Seasonal & Holiday", "Hearts, snowflakes, sun & more", PINK),
        ("Washi Tape Strips", "25 decorative patterns", PEACH),
        ("Speech Bubbles", "Banners, frames & borders", YELLOW),
        ("Icons & Symbols", "Phone, email, home & 20+ more", MINT),
    ]

    start_y = 350
    for i, (title, desc, color) in enumerate(items):
        y = start_y + i * 190
        # Color bar
        draw_rounded_rect(draw, (150, y, 2250, y + 160), radius=20, fill=WHITE, outline=color, width=4)
        # Icon circle
        draw.ellipse([200, y + 25, 310, y + 135], fill=color, outline=CHARCOAL, width=3)
        draw_text_centered(draw, str(i + 1), 255, y + 80, get_font(48), WHITE)
        # Text
        draw.text((370, y + 30), title, fill=CHARCOAL, font=get_font(48))
        draw.text((370, y + 95), desc, fill=(120, 120, 120), font=get_font_regular(36))

    return img


# =================================================================
# Image 3: Sheet 1-2 Preview
# =================================================================
def create_image_3():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_PINK, LIGHT_YELLOW)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "Daily Planner + Motivational", W // 2, 130, get_font(80), CHARCOAL)
    draw_decorative_dots(draw, 220)

    # Two sheets side by side
    sheet1 = load_sticker_sheet("sheet_1_daily_planner.png")
    sheet2 = load_sticker_sheet("sheet_2_motivational.png")

    preview_size = 1000
    paste_sticker_preview(img, sheet1, 100, 320, preview_size)
    paste_sticker_preview(img, sheet2, 1300, 320, preview_size)

    # Labels
    draw_rounded_rect(draw, (200, 1380, 1000, 1460), radius=15, fill=PINK, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Daily Planner (25 stickers)", 600, 1420, get_font(38), CHARCOAL)

    draw_rounded_rect(draw, (1400, 1380, 2200, 1460), radius=15, fill=LAVENDER, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Motivational Quotes (25)", 1800, 1420, get_font(38), CHARCOAL)

    # Feature bullets
    features = [
        "To-Do, Meeting, Deadline, Reminder stickers",
        "Inspirational quotes in decorative frames",
        "Checkboxes, flags, stars & arrow tabs",
        "Clear charcoal outlines on pastel backgrounds",
    ]
    for i, feat in enumerate(features):
        y = 1550 + i * 80
        draw_checkmark_icon(draw, 300, y, 45, COLORS[i % len(COLORS)])
        draw.text((380, y + 5), feat, fill=CHARCOAL, font=get_font_regular(38))

    # Bottom note
    draw_rounded_rect(draw, (400, 2200, 2000, 2300), radius=20, fill=PEACH)
    draw_text_centered(draw, "50 stickers across 2 themed sheets", W // 2, 2250, get_font(42), CHARCOAL)

    return img


# =================================================================
# Image 4: Sheet 3-4 Preview
# =================================================================
def create_image_4():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_BLUE, LIGHT_MINT)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "Functional Tabs + Habit Tracker", W // 2, 130, get_font(80), CHARCOAL)
    draw_decorative_dots(draw, 220)

    sheet3 = load_sticker_sheet("sheet_3_functional_tabs.png")
    sheet4 = load_sticker_sheet("sheet_4_habit_tracker.png")

    preview_size = 1000
    paste_sticker_preview(img, sheet3, 100, 320, preview_size)
    paste_sticker_preview(img, sheet4, 1300, 320, preview_size)

    draw_rounded_rect(draw, (200, 1380, 1000, 1460), radius=15, fill=SKY, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Functional Tabs (25 stickers)", 600, 1420, get_font(38), CHARCOAL)

    draw_rounded_rect(draw, (1400, 1380, 2200, 1460), radius=15, fill=MINT, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Habit Tracker (25 stickers)", 1800, 1420, get_font(38), CHARCOAL)

    features = [
        "Month tabs (Jan-Dec) for section navigation",
        "Day-of-week tabs (Mon-Sun)",
        "Habit icons: water, exercise, sleep, reading",
        "Built-in checkboxes for habit tracking",
    ]
    for i, feat in enumerate(features):
        y = 1550 + i * 80
        draw_checkmark_icon(draw, 300, y, 45, COLORS[i % len(COLORS)])
        draw.text((380, y + 5), feat, fill=CHARCOAL, font=get_font_regular(38))

    draw_rounded_rect(draw, (400, 2200, 2000, 2300), radius=20, fill=MINT)
    draw_text_centered(draw, "50 stickers across 2 themed sheets", W // 2, 2250, get_font(42), CHARCOAL)

    return img


# =================================================================
# Image 5: Sheet 5-6 Preview
# =================================================================
def create_image_5():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_YELLOW, LIGHT_PINK)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "Seasonal + Washi Tape", W // 2, 130, get_font(80), CHARCOAL)
    draw_decorative_dots(draw, 220)

    sheet5 = load_sticker_sheet("sheet_5_seasonal.png")
    sheet6 = load_sticker_sheet("sheet_6_washi_tape.png")

    preview_size = 1000
    paste_sticker_preview(img, sheet5, 100, 320, preview_size)
    paste_sticker_preview(img, sheet6, 1300, 320, preview_size)

    draw_rounded_rect(draw, (200, 1380, 1000, 1460), radius=15, fill=PEACH, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Seasonal & Holiday (25)", 600, 1420, get_font(38), CHARCOAL)

    draw_rounded_rect(draw, (1400, 1380, 2200, 1460), radius=15, fill=YELLOW, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Washi Tape Strips (25)", 1800, 1420, get_font(38), CHARCOAL)

    features = [
        "Hearts, snowflakes, sun, pumpkin & more",
        "25 washi tape patterns: dots, stripes, chevron",
        "Perfect for seasonal planning & decoration",
        "Warm pastel color palette throughout",
    ]
    for i, feat in enumerate(features):
        y = 1550 + i * 80
        draw_checkmark_icon(draw, 300, y, 45, COLORS[i % len(COLORS)])
        draw.text((380, y + 5), feat, fill=CHARCOAL, font=get_font_regular(38))

    draw_rounded_rect(draw, (400, 2200, 2000, 2300), radius=20, fill=YELLOW)
    draw_text_centered(draw, "50 stickers across 2 themed sheets", W // 2, 2250, get_font(42), CHARCOAL)

    return img


# =================================================================
# Image 6: Sheet 7-8 Preview
# =================================================================
def create_image_6():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_LAVENDER, LIGHT_BLUE)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "Speech Bubbles + Icons", W // 2, 130, get_font(80), CHARCOAL)
    draw_decorative_dots(draw, 220)

    sheet7 = load_sticker_sheet("sheet_7_speech_bubbles.png")
    sheet8 = load_sticker_sheet("sheet_8_icons.png")

    preview_size = 1000
    paste_sticker_preview(img, sheet7, 100, 320, preview_size)
    paste_sticker_preview(img, sheet8, 1300, 320, preview_size)

    draw_rounded_rect(draw, (200, 1380, 1000, 1460), radius=15, fill=LAVENDER, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Speech Bubbles & Banners (25)", 600, 1420, get_font(38), CHARCOAL)

    draw_rounded_rect(draw, (1400, 1380, 2200, 1460), radius=15, fill=SKY, outline=CHARCOAL, width=2)
    draw_text_centered(draw, "Icons & Symbols (25)", 1800, 1420, get_font(38), CHARCOAL)

    features = [
        "Speech bubbles, thought clouds, banners",
        "Decorative frames, brackets & dividers",
        "25 useful icons: phone, email, home, camera",
        "Perfect for notes, journaling & planning",
    ]
    for i, feat in enumerate(features):
        y = 1550 + i * 80
        draw_checkmark_icon(draw, 300, y, 45, COLORS[i % len(COLORS)])
        draw.text((380, y + 5), feat, fill=CHARCOAL, font=get_font_regular(38))

    draw_rounded_rect(draw, (400, 2200, 2000, 2300), radius=20, fill=LAVENDER)
    draw_text_centered(draw, "50 stickers across 2 themed sheets", W // 2, 2250, get_font(42), CHARCOAL)

    return img


# =================================================================
# Image 7: How to Use Guide
# =================================================================
def create_image_7():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_MINT, LIGHT_YELLOW)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "How to Use", W // 2, 120, get_font(100), CHARCOAL)
    draw_text_centered(draw, "Your Digital Stickers", W // 2, 250, get_font(70), CHARCOAL)
    draw_decorative_dots(draw, 350)

    steps = [
        ("1", "Download & Unzip", "Download the ZIP file and extract\nall sticker sheets and individual PNGs", PINK),
        ("2", "Import to App", "Open GoodNotes or Notability\nand import the sticker sheets", PEACH),
        ("3", "Use Lasso Tool", "Select individual stickers with\nthe lasso/selection tool", YELLOW),
        ("4", "Drag & Drop", "Place stickers anywhere on\nyour planner pages", MINT),
        ("5", "Resize & Arrange", "Pinch to resize, rotate, and\narrange your stickers", SKY),
        ("6", "Or Use Individual PNGs", "Import pre-cropped individual\nsticker files directly", LAVENDER),
    ]

    for i, (num, title, desc, color) in enumerate(steps):
        y = 430 + i * 300
        # Step number circle
        draw.ellipse([200, y, 330, y + 130], fill=color, outline=CHARCOAL, width=3)
        draw_text_centered(draw, num, 265, y + 65, get_font(60), WHITE)
        # Step content
        draw_rounded_rect(draw, (380, y, 2200, y + 240), radius=20, fill=WHITE, outline=color, width=3)
        draw.text((420, y + 25), title, fill=CHARCOAL, font=get_font(48))
        draw.text((420, y + 90), desc, fill=(100, 100, 100), font=get_font_regular(34))

    # Arrow connectors
    for i in range(5):
        y = 430 + i * 300 + 200
        draw.line([265, y, 265, y + 100], fill=CHARCOAL, width=3)
        draw.polygon([(255, y + 90), (275, y + 90), (265, y + 110)], fill=CHARCOAL)

    return img


# =================================================================
# Image 8: Compatibility Info
# =================================================================
def create_image_8():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_BLUE, LIGHT_LAVENDER)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "Compatible With", W // 2, 150, get_font(100), CHARCOAL)
    draw_decorative_dots(draw, 260)

    # App compatibility grid
    apps = [
        ("GoodNotes 5 & 6", "iPad & Mac", PINK),
        ("Notability", "iPad & Mac", PEACH),
        ("Noteshelf", "iPad & Android", YELLOW),
        ("CollaNote", "iPad (Free)", MINT),
        ("Samsung Notes", "Galaxy Tab", SKY),
        ("Xodo", "Cross-Platform", LAVENDER),
    ]

    for i, (app, platform, color) in enumerate(apps):
        col = i % 2
        row = i // 2
        x = 200 + col * 1100
        y = 380 + row * 350

        draw_rounded_rect(draw, (x, y, x + 950, y + 300), radius=25, fill=WHITE, outline=color, width=4)

        # App icon placeholder
        draw_rounded_rect(draw, (x + 40, y + 50, x + 200, y + 210), radius=20, fill=color, outline=CHARCOAL, width=2)
        draw_text_centered(draw, app[0], x + 120, y + 130, get_font(80), WHITE)

        # App name and platform
        draw.text((x + 240, y + 70), app, fill=CHARCOAL, font=get_font(48))
        draw.text((x + 240, y + 140), platform, fill=(120, 120, 120), font=get_font_regular(38))

        # Checkmark
        draw_checkmark_icon(draw, x + 800, y + 100, 60, MINT)

    # File format info
    y_info = 1500
    draw_rounded_rect(draw, (200, y_info, 2200, y_info + 350), radius=30, fill=WHITE, outline=CHARCOAL, width=3)
    draw_text_centered(draw, "File Format Details", W // 2, y_info + 50, get_font(52), CHARCOAL)

    formats = [
        ("PNG", "Transparent background", PINK),
        ("2048px", "High-resolution sheets", SKY),
        ("200px", "Individual stickers", MINT),
        ("RGB", "Vibrant digital colors", YELLOW),
    ]
    for i, (fmt, desc, color) in enumerate(formats):
        x = 300 + i * 480
        y = y_info + 120
        draw_rounded_rect(draw, (x, y, x + 400, y + 180), radius=15, fill=color, outline=CHARCOAL, width=2)
        draw_text_centered(draw, fmt, x + 200, y + 60, get_font(52), CHARCOAL)
        draw_text_centered(draw, desc, x + 200, y + 130, get_font_regular(28), CHARCOAL)

    # Bottom note
    draw_rounded_rect(draw, (300, 2050, 2100, 2200), radius=25, fill=LAVENDER)
    draw_text_centered(draw, "Works with any app that supports PNG image import!",
                       W // 2, 2125, get_font(40), CHARCOAL)

    return img


# =================================================================
# Image 9: Testimonials
# =================================================================
def create_image_9():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_YELLOW, LIGHT_PINK)
    draw = ImageDraw.Draw(img)

    draw_text_centered(draw, "What Customers Say", W // 2, 150, get_font(90), CHARCOAL)

    # Stars row
    for i in range(5):
        draw_star(draw, W // 2 - 120 + i * 60, 290, 25, 12, fill=YELLOW, outline=CHARCOAL, width=2)

    draw_decorative_dots(draw, 360)

    testimonials = [
        ('"These stickers are SO cute and\nperfect for my GoodNotes planner!\nI use them every single day."',
         "- Sarah M.", "Verified Purchase", PINK),
        ('"Love the pastel color palette.\nThe washi tape strips and habit\ntracker stickers are my favorites!"',
         "- Jessica L.", "Verified Purchase", PEACH),
        ('"Great value for 200+ stickers!\nThe quality is amazing and they\nlook professional on my planner."',
         "- Emily R.", "Verified Purchase", MINT),
        ('"Best digital stickers I have found\non Etsy. The functional tabs make\nmy planner so much more organized."',
         "- Amanda K.", "Verified Purchase", LAVENDER),
    ]

    for i, (quote, name, badge, color) in enumerate(testimonials):
        y = 430 + i * 440
        draw_rounded_rect(draw, (200, y, 2200, y + 380), radius=25, fill=WHITE, outline=color, width=4)

        # Quote mark
        draw.text((250, y + 20), "\u201C", fill=color, font=get_font(80))

        # Stars
        for j in range(5):
            draw_star(draw, 280 + j * 40, y + 40, 15, 7, fill=YELLOW, outline=CHARCOAL, width=1)

        # Quote text
        draw.text((280, y + 80), quote, fill=CHARCOAL, font=get_font_regular(36))

        # Name
        draw.text((280, y + 280), name, fill=CHARCOAL, font=get_font(36))

        # Badge
        draw_rounded_rect(draw, (550, y + 280, 850, y + 320), radius=10, fill=color)
        draw_text_centered(draw, badge, 700, y + 300, get_font_regular(22), WHITE)

        # Color accent bar on left
        draw_rounded_rect(draw, (200, y, 218, y + 380), radius=0, fill=color)

    return img


# =================================================================
# Image 10: Bundle CTA
# =================================================================
def create_image_10():
    img = Image.new("RGB", (W, H), WHITE)
    draw_gradient_bg(img, LIGHT_LAVENDER, LIGHT_PINK)
    draw = ImageDraw.Draw(img)

    # Big title
    draw_text_centered(draw, "Digital Planner", W // 2, 250, get_font(120), CHARCOAL)
    draw_text_centered(draw, "Stickers Bundle", W // 2, 400, get_font(120), CHARCOAL)

    # Colorful divider
    for i, color in enumerate(COLORS):
        x = 400 + i * 270
        draw_rounded_rect(draw, (x, 530, x + 240, 555), radius=12, fill=color)

    # Sticker preview thumbnails in a row
    sheets = [
        "sheet_1_daily_planner.png", "sheet_2_motivational.png",
        "sheet_3_functional_tabs.png", "sheet_4_habit_tracker.png",
        "sheet_5_seasonal.png", "sheet_6_washi_tape.png",
        "sheet_7_speech_bubbles.png", "sheet_8_icons.png",
    ]
    thumb_size = 240
    start_x = (W - 8 * thumb_size - 7 * 20) // 2
    for i, sname in enumerate(sheets):
        sheet = load_sticker_sheet(sname)
        x = start_x + i * (thumb_size + 20)
        y = 620
        if sheet:
            paste_sticker_preview(img, sheet, x, y, thumb_size)
        else:
            draw_rounded_rect(draw, (x, y, x + thumb_size, y + thumb_size),
                              radius=8, fill=COLORS[i % len(COLORS)], outline=CHARCOAL, width=2)

    # What you get
    draw_text_centered(draw, "What You Get:", W // 2, 950, get_font(60), CHARCOAL)

    bullets = [
        "8 sticker sheets (2048 x 2048 px)",
        "200+ individual stickers (precropped PNG)",
        "Transparent background - ready to use",
        "Works with GoodNotes, Notability & more",
        "Instant digital download",
    ]
    for i, bullet in enumerate(bullets):
        y = 1040 + i * 80
        draw_checkmark_icon(draw, 500, y, 45, COLORS[i % len(COLORS)])
        draw.text((570, y + 5), bullet, fill=CHARCOAL, font=get_font_regular(40))

    # Price section
    draw_rounded_rect(draw, (600, 1520, 1800, 1750), radius=40, fill=PINK, outline=CHARCOAL, width=5)
    draw_text_centered(draw, "Only", W // 2, 1570, get_font(48), CHARCOAL)
    draw_text_centered(draw, "$6.99", W // 2, 1660, get_font(100), CHARCOAL)

    # CTA button
    draw_rounded_rect(draw, (650, 1820, 1750, 1950), radius=35, fill=CHARCOAL)
    draw_text_centered(draw, "Add to Cart", W // 2, 1885, get_font(60), WHITE)

    # Bottom trust badges
    badges = ["Instant Download", "Secure Payment", "24/7 Support"]
    for i, badge in enumerate(badges):
        x = 350 + i * 650
        y = 2050
        draw.ellipse([x, y, x + 50, y + 50], fill=COLORS[i % len(COLORS)], outline=CHARCOAL, width=2)
        draw_checkmark_icon(draw, x + 5, y + 5, 40, COLORS[i % len(COLORS)])
        draw.text((x + 65, y + 8), badge, fill=CHARCOAL, font=get_font(36))

    # Decorative dots
    draw_decorative_dots(draw, 2200)

    return img


# =================================================================
# Main
# =================================================================
def main():
    print("Creating listing images...")
    creators = [
        ("01_hero_collage.jpg", create_image_1),
        ("02_whats_included.jpg", create_image_2),
        ("03_preview_daily_motivational.jpg", create_image_3),
        ("04_preview_tabs_habit.jpg", create_image_4),
        ("05_preview_seasonal_washi.jpg", create_image_5),
        ("06_preview_bubbles_icons.jpg", create_image_6),
        ("07_how_to_use.jpg", create_image_7),
        ("08_compatibility.jpg", create_image_8),
        ("09_testimonials.jpg", create_image_9),
        ("10_bundle_cta.jpg", create_image_10),
    ]

    for fname, func in creators:
        print(f"  Creating {fname}...")
        img = func()
        path = os.path.join(SCRIPT_DIR, fname)
        img = img.convert("RGB")
        img.save(path, "JPEG", quality=95)
        print(f"    Saved {path}")

    print("\nAll 10 listing images created successfully!")


if __name__ == "__main__":
    main()
