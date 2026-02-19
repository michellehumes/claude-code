#!/usr/bin/env python3
"""
Digital Planner Stickers Bundle - Creates 8 sticker sheets (2048x2048)
and 50 individual stickers (200x200) for GoodNotes/Notability.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# --- Color Palette ---
PINK = (244, 180, 197)
PEACH = (249, 198, 168)
YELLOW = (249, 228, 167)
MINT = (181, 216, 199)
SKY = (167, 199, 231)
LAVENDER = (197, 180, 227)
WHITE = (255, 255, 255)
CHARCOAL = (68, 68, 68)
COLORS = [PINK, PEACH, YELLOW, MINT, SKY, LAVENDER]

SHEET_SIZE = 2048
GRID = 5  # 5x5 grid
PADDING = 20
STICKER_SIZE = (SHEET_SIZE - PADDING * (GRID + 1)) // GRID  # ~389px each
INDIVIDUAL_SIZE = 200

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDIVIDUAL_DIR = os.path.join(SCRIPT_DIR, "individual")
os.makedirs(INDIVIDUAL_DIR, exist_ok=True)

# Try to load a font
def get_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def get_font_regular(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
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


def draw_circle(draw, cx, cy, r, fill, outline=None, width=0):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def draw_star(draw, cx, cy, r_outer, r_inner, points=5, fill=YELLOW, outline=CHARCOAL, width=2):
    """Draw a star shape."""
    coords = []
    for i in range(points * 2):
        angle = math.radians(-90 + i * 360 / (points * 2))
        r = r_outer if i % 2 == 0 else r_inner
        coords.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(coords, fill=fill, outline=outline, width=width)


def draw_heart(draw, cx, cy, size, fill=PINK, outline=CHARCOAL, width=2):
    """Draw a heart shape using two circles and a triangle."""
    r = size * 0.3
    # Two circles for top bumps
    draw.ellipse([cx - size * 0.5, cy - size * 0.4, cx, cy + size * 0.1], fill=fill, outline=outline, width=width)
    draw.ellipse([cx, cy - size * 0.4, cx + size * 0.5, cy + size * 0.1], fill=fill, outline=outline, width=width)
    # Triangle for bottom
    draw.polygon([(cx - size * 0.48, cy - size * 0.05), (cx + size * 0.48, cy - size * 0.05), (cx, cy + size * 0.5)],
                 fill=fill, outline=outline, width=width)
    # Fill gap
    draw.rectangle([cx - size * 0.3, cy - size * 0.15, cx + size * 0.3, cy + size * 0.1], fill=fill)


def draw_checkmark(draw, cx, cy, size, color=CHARCOAL, width=3):
    draw.line([cx - size * 0.3, cy, cx - size * 0.05, cy + size * 0.3], fill=color, width=width)
    draw.line([cx - size * 0.05, cy + size * 0.3, cx + size * 0.35, cy - size * 0.25], fill=color, width=width)


def draw_text_centered(draw, text, cx, cy, font, fill=CHARCOAL):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=fill, font=font)


def draw_text_fitted(draw, text, cx, cy, max_width, max_size=36, fill=CHARCOAL):
    """Draw text centered, reducing font size to fit max_width."""
    size = max_size
    while size > 10:
        font = get_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        if tw <= max_width:
            break
        size -= 2
    font = get_font(size)
    draw_text_centered(draw, text, cx, cy, font, fill)
    return font


def sticker_base(draw, x, y, w, h, color, shape="rounded_rect", border_w=3):
    """Draw the sticker base shape."""
    margin = 4
    if shape == "rounded_rect":
        draw_rounded_rect(draw, (x + margin, y + margin, x + w - margin, y + h - margin),
                          radius=20, fill=color, outline=CHARCOAL, width=border_w)
    elif shape == "circle":
        cx, cy = x + w // 2, y + h // 2
        r = min(w, h) // 2 - margin
        draw_circle(draw, cx, cy, r, fill=color, outline=CHARCOAL, width=border_w)
    elif shape == "tab":
        draw_rounded_rect(draw, (x + margin, y + margin, x + w - margin, y + h - margin),
                          radius=12, fill=color, outline=CHARCOAL, width=border_w)


# =================================================================
# Sheet 1: Daily Planner Stickers
# =================================================================
def draw_sheet_1_daily_planner():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    stickers = [
        ("To Do", PINK), ("Important!", PEACH), ("Don't Forget", YELLOW),
        ("Meeting", MINT), ("Deadline", SKY), ("Clock", LAVENDER),
        ("Arrow Tab", PINK), ("Flag", PEACH), ("Star", YELLOW),
        ("Checkbox", MINT), ("Priority", SKY), ("Reminder", LAVENDER),
        ("Note", PINK), ("Goal", PEACH), ("Schedule", YELLOW),
        ("Call", MINT), ("Email", SKY), ("Errand", LAVENDER),
        ("Appt.", PINK), ("Event", PEACH), ("Bill Due", YELLOW),
        ("Birthday", MINT), ("Travel", SKY), ("Grocery", LAVENDER),
        ("Workout", PINK),
    ]

    font_lg = get_font(32)
    font_sm = get_font(24)
    font_icon = get_font(48)

    for idx, (label, color) in enumerate(stickers):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2

        sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color)

        if label == "Clock":
            # Draw clock icon
            draw_circle(draw, cx, cy - 20, 60, WHITE, CHARCOAL, 3)
            draw.line([cx, cy - 20, cx, cy - 55], fill=CHARCOAL, width=3)
            draw.line([cx, cy - 20, cx + 30, cy - 10], fill=CHARCOAL, width=3)
            draw_text_centered(draw, "Clock", cx, cy + 60, font_sm, CHARCOAL)
        elif label == "Arrow Tab":
            # Arrow pointing right
            draw.polygon([(cx - 50, cy - 25), (cx + 20, cy - 25), (cx + 50, cy),
                          (cx + 20, cy + 25), (cx - 50, cy + 25)], fill=WHITE, outline=CHARCOAL, width=2)
            draw_text_centered(draw, "Tab", cx - 10, cy, font_sm, CHARCOAL)
        elif label == "Flag":
            draw.rectangle([cx - 5, cy - 60, cx + 5, cy + 50], fill=CHARCOAL)
            draw.polygon([(cx + 5, cy - 60), (cx + 60, cy - 40), (cx + 5, cy - 20)],
                         fill=PEACH, outline=CHARCOAL, width=2)
            draw_text_centered(draw, "Flag", cx, cy + 70, font_sm, CHARCOAL)
        elif label == "Star":
            draw_star(draw, cx, cy - 10, 55, 25, fill=YELLOW, outline=CHARCOAL, width=2)
            draw_text_centered(draw, "Star", cx, cy + 65, font_sm, CHARCOAL)
        elif label == "Checkbox":
            draw.rectangle([cx - 30, cy - 40, cx + 30, cy + 20], fill=WHITE, outline=CHARCOAL, width=3)
            draw_checkmark(draw, cx, cy - 10, 40, CHARCOAL, 3)
            draw_text_centered(draw, "Done!", cx, cy + 50, font_sm, CHARCOAL)
        else:
            draw_text_fitted(draw, label, cx, cy, STICKER_SIZE - 40, 36, CHARCOAL)

    return img


# =================================================================
# Sheet 2: Motivational Quotes
# =================================================================
def draw_sheet_2_motivational():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    quotes = [
        "You Got This", "Be Kind", "Dream Big", "Stay Focused",
        "One Day\nat a Time", "Progress Not\nPerfection", "Believe", "Keep Going",
        "Be Brave", "Breathe", "Shine On", "Good Vibes",
        "Just Start", "Be Happy", "Love More", "Stay Wild",
        "No Limits", "Rise Up", "Go For It", "Stay True",
        "Hustle", "Create", "Explore", "Imagine", "Thrive",
    ]

    font_lg = get_font(28)

    for idx, quote in enumerate(quotes):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2
        color = COLORS[idx % len(COLORS)]

        # Alternate between shapes for variety
        if idx % 3 == 0:
            # Rounded rect with inner border
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color)
            draw_rounded_rect(draw, (x + 18, y + 18, x + STICKER_SIZE - 18, y + STICKER_SIZE - 18),
                              radius=14, fill=None, outline=CHARCOAL, width=1)
        elif idx % 3 == 1:
            # Circle sticker
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color, shape="circle")
        else:
            # Banner shape
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color)
            # Small decorative dots in corners
            for dx2, dy2 in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                draw_circle(draw, cx + dx2 * (STICKER_SIZE // 2 - 30),
                            cy + dy2 * (STICKER_SIZE // 2 - 30), 5, CHARCOAL)

        # Draw quote text
        lines = quote.split("\n")
        total_h = len(lines) * 32
        start_y = cy - total_h // 2
        for li, line in enumerate(lines):
            draw_text_fitted(draw, line, cx, start_y + li * 32, STICKER_SIZE - 50, 28, CHARCOAL)

    return img


# =================================================================
# Sheet 3: Functional Tabs
# =================================================================
def draw_sheet_3_functional_tabs():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    nums = ["1", "2", "3", "4", "5"]
    divider_label = "---"

    tabs = []
    for m in months:
        tabs.append(m)
    for d in days:
        tabs.append(d)
    for n in nums:
        tabs.append(n)
    tabs.append(divider_label)
    # Pad to 25
    while len(tabs) < 25:
        tabs.append("---")

    font = get_font(32)

    for idx, label in enumerate(tabs):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2
        color = COLORS[idx % len(COLORS)]

        if label == "---":
            # Section divider - horizontal strip
            draw_rounded_rect(draw, (x + 10, cy - 15, x + STICKER_SIZE - 10, cy + 15),
                              radius=8, fill=color, outline=CHARCOAL, width=2)
        elif label in months:
            # Month tab - tab shape with side notch
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color, shape="tab")
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
            # Small underline
            draw.line([cx - 30, cy + 24, cx + 30, cy + 24], fill=CHARCOAL, width=2)
        elif label in days:
            # Day tab - rounded rect
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        else:
            # Numbered circle
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color, shape="circle")
            draw_text_centered(draw, label, cx, cy, get_font(48), CHARCOAL)

    return img


# =================================================================
# Sheet 4: Habit Tracker
# =================================================================
def draw_sheet_4_habit_tracker():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    habits = [
        ("Water", SKY, "drop"), ("Exercise", MINT, "dumbbell"), ("Sleep", LAVENDER, "moon"),
        ("Medicine", PINK, "pill"), ("Read", YELLOW, "book"), ("Meditate", LAVENDER, "lotus"),
        ("Fruits", PEACH, "apple"), ("Steps", MINT, "shoe"), ("Journal", YELLOW, "pen"),
        ("Stretch", PINK, "stretch"), ("Vitamins", PEACH, "vitamin"), ("No Sugar", YELLOW, "x"),
        ("Hydrate", SKY, "glass"), ("Yoga", LAVENDER, "yoga"), ("Walk", MINT, "walk"),
        ("Gratitude", PINK, "heart"), ("Veggies", MINT, "leaf"), ("Screen Off", SKY, "screen"),
        ("Floss", WHITE, "tooth"), ("Skincare", PINK, "face"), ("Cook", PEACH, "pot"),
        ("Clean", SKY, "broom"), ("Budget", YELLOW, "dollar"), ("Practice", LAVENDER, "music"),
        ("Relax", MINT, "tea"),
    ]

    font = get_font(24)

    for idx, (label, color, icon) in enumerate(habits):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2

        sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color)

        # Draw simple icon
        icon_cy = cy - 30
        if icon == "drop":
            # Water drop
            draw.polygon([(cx, icon_cy - 45), (cx - 30, icon_cy + 15), (cx + 30, icon_cy + 15)],
                         fill=SKY, outline=CHARCOAL, width=2)
            draw.pieslice([cx - 30, icon_cy, cx + 30, icon_cy + 35], 0, 180, fill=SKY, outline=CHARCOAL, width=2)
        elif icon == "moon":
            draw.pieslice([cx - 35, icon_cy - 35, cx + 35, icon_cy + 35], 220, 500,
                          fill=LAVENDER, outline=CHARCOAL, width=2)
        elif icon == "book":
            draw.rectangle([cx - 35, icon_cy - 25, cx + 35, icon_cy + 25], fill=YELLOW, outline=CHARCOAL, width=2)
            draw.line([cx, icon_cy - 25, cx, icon_cy + 25], fill=CHARCOAL, width=2)
        elif icon == "heart":
            draw_heart(draw, cx, icon_cy, 60, PINK, CHARCOAL, 2)
        elif icon == "leaf":
            draw.pieslice([cx - 30, icon_cy - 30, cx + 30, icon_cy + 30], 30, 210,
                          fill=MINT, outline=CHARCOAL, width=2)
        elif icon == "dollar":
            draw_circle(draw, cx, icon_cy, 30, YELLOW, CHARCOAL, 2)
            draw_text_centered(draw, "$", cx, icon_cy, get_font(36), CHARCOAL)
        else:
            # Generic circle icon
            draw_circle(draw, cx, icon_cy, 30, WHITE, CHARCOAL, 2)
            draw_text_centered(draw, icon[0].upper(), cx, icon_cy, get_font(28), CHARCOAL)

        # Draw label
        draw_text_centered(draw, label, cx, cy + 55, font, CHARCOAL)

        # Small checkbox
        draw.rectangle([cx - 12, cy + 80, cx + 12, cy + 104], fill=WHITE, outline=CHARCOAL, width=2)

    return img


# =================================================================
# Sheet 5: Seasonal/Holiday
# =================================================================
def draw_sheet_5_seasonal():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    items = [
        ("Hearts", PINK), ("Snowflake", SKY), ("Sun", YELLOW),
        ("Leaves", PEACH), ("Pumpkin", PEACH), ("Gift Box", PINK),
        ("Fireworks", LAVENDER), ("Flowers", PINK), ("Rainbow", YELLOW),
        ("Umbrella", SKY), ("Candle", PEACH), ("Easter Egg", LAVENDER),
        ("Clover", MINT), ("Butterfly", LAVENDER), ("Beach", YELLOW),
        ("Stars", SKY), ("Mittens", PINK), ("Holly", MINT),
        ("Cake", PEACH), ("Balloons", LAVENDER), ("Trophy", YELLOW),
        ("Confetti", PINK), ("Tree", MINT), ("Wreath", MINT),
        ("Ribbon", PEACH),
    ]

    font = get_font(24)

    for idx, (label, color) in enumerate(items):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2

        sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color, shape="circle" if idx % 2 == 0 else "rounded_rect")

        icon_cy = cy - 15
        if label == "Hearts":
            draw_heart(draw, cx, icon_cy, 70, PINK, CHARCOAL, 2)
        elif label == "Snowflake":
            for angle in [0, 60, 120]:
                rad = math.radians(angle)
                x1 = cx + int(45 * math.cos(rad))
                y1 = icon_cy + int(45 * math.sin(rad))
                x2 = cx - int(45 * math.cos(rad))
                y2 = icon_cy - int(45 * math.sin(rad))
                draw.line([x1, y1, x2, y2], fill=CHARCOAL, width=2)
                # Small branches
                for sign in [-1, 1]:
                    bx = cx + int(25 * sign * math.cos(rad))
                    by = icon_cy + int(25 * sign * math.sin(rad))
                    draw.line([bx, by, bx + int(12 * math.cos(rad + math.pi / 3)),
                               by + int(12 * math.sin(rad + math.pi / 3))], fill=CHARCOAL, width=2)
        elif label == "Sun":
            draw_circle(draw, cx, icon_cy, 30, YELLOW, CHARCOAL, 2)
            for i in range(8):
                angle = math.radians(i * 45)
                draw.line([cx + int(35 * math.cos(angle)), icon_cy + int(35 * math.sin(angle)),
                           cx + int(50 * math.cos(angle)), icon_cy + int(50 * math.sin(angle))],
                          fill=CHARCOAL, width=2)
        elif label == "Pumpkin":
            draw.ellipse([cx - 40, icon_cy - 30, cx + 40, icon_cy + 40], fill=PEACH, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 5, icon_cy - 40, cx + 5, icon_cy - 25], fill=MINT, outline=CHARCOAL, width=1)
        elif label == "Gift Box":
            draw.rectangle([cx - 35, icon_cy - 15, cx + 35, icon_cy + 40], fill=PINK, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 35, icon_cy - 30, cx + 35, icon_cy - 15], fill=LAVENDER, outline=CHARCOAL, width=2)
            draw.line([cx, icon_cy - 30, cx, icon_cy + 40], fill=CHARCOAL, width=2)
        elif label == "Flowers":
            for a in range(5):
                angle = math.radians(a * 72 - 90)
                px = cx + int(22 * math.cos(angle))
                py = icon_cy + int(22 * math.sin(angle))
                draw_circle(draw, px, py, 15, PINK, CHARCOAL, 1)
            draw_circle(draw, cx, icon_cy, 12, YELLOW, CHARCOAL, 1)
        elif label == "Rainbow":
            for i, c in enumerate([PINK, PEACH, YELLOW, MINT, SKY, LAVENDER]):
                r = 55 - i * 7
                draw.arc([cx - r, icon_cy - r, cx + r, icon_cy + r], 180, 360, fill=c, width=5)
        elif label == "Umbrella":
            draw.pieslice([cx - 40, icon_cy - 40, cx + 40, icon_cy + 20], 180, 360, fill=SKY, outline=CHARCOAL, width=2)
            draw.line([cx, icon_cy, cx, icon_cy + 55], fill=CHARCOAL, width=3)
            draw.arc([cx, icon_cy + 40, cx + 15, icon_cy + 55], 0, 180, fill=CHARCOAL, width=2)
        elif label == "Tree":
            draw.polygon([(cx, icon_cy - 45), (cx - 35, icon_cy + 15), (cx + 35, icon_cy + 15)],
                         fill=MINT, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 8, icon_cy + 15, cx + 8, icon_cy + 40], fill=PEACH, outline=CHARCOAL, width=1)
        else:
            draw_text_centered(draw, label, cx, icon_cy, font, CHARCOAL)

        draw_text_centered(draw, label, cx, cy + 60, get_font(20), CHARCOAL)

    return img


# =================================================================
# Sheet 6: Washi Tape Strips
# =================================================================
def draw_sheet_6_washi_tape():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    patterns = [
        ("Dots Pink", PINK, "dots"), ("Stripes Peach", PEACH, "stripes"),
        ("Chevron Yellow", YELLOW, "chevron"), ("Floral Mint", MINT, "floral"),
        ("Geo Blue", SKY, "geo"), ("Hearts Lav", LAVENDER, "hearts"),
        ("Plaid Pink", PINK, "plaid"), ("Zigzag Peach", PEACH, "zigzag"),
        ("Stars Yellow", YELLOW, "stars"), ("Waves Mint", MINT, "waves"),
        ("Confetti Blue", SKY, "confetti"), ("Diamond Lav", LAVENDER, "diamond"),
        ("Dash Pink", PINK, "dash"), ("Cross Peach", PEACH, "cross"),
        ("Dot Stripe Yel", YELLOW, "dot_stripe"), ("Leaf Mint", MINT, "leaf"),
        ("Cloud Blue", SKY, "cloud"), ("Bow Lav", LAVENDER, "bow"),
        ("Arrow Pink", PINK, "arrow"), ("Grid Peach", PEACH, "grid"),
        ("Scallop Yellow", YELLOW, "scallop"), ("Tri Mint", MINT, "triangle"),
        ("Spiral Blue", SKY, "spiral"), ("Circle Lav", LAVENDER, "circle"),
        ("Rainbow", YELLOW, "rainbow"),
    ]

    for idx, (label, color, pattern) in enumerate(patterns):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)

        # Washi tape: full width, ~60% height, slightly transparent edges
        ty = y + STICKER_SIZE // 4
        th = STICKER_SIZE // 2
        tw = STICKER_SIZE - 10

        # Base tape
        draw.rectangle([x + 5, ty, x + tw + 5, ty + th], fill=color, outline=CHARCOAL, width=2)

        # Pattern overlay
        if pattern == "dots":
            for py2 in range(ty + 15, ty + th - 5, 25):
                for px2 in range(x + 20, x + tw, 25):
                    draw_circle(draw, px2, py2, 5, WHITE)
        elif pattern == "stripes":
            for sx in range(x + 15, x + tw, 20):
                draw.line([sx, ty, sx, ty + th], fill=WHITE, width=3)
        elif pattern == "chevron":
            for cy2 in range(ty + 10, ty + th - 10, 30):
                for cx2 in range(x + 20, x + tw - 10, 40):
                    draw.line([cx2, cy2 + 10, cx2 + 15, cy2], fill=WHITE, width=2)
                    draw.line([cx2 + 15, cy2, cx2 + 30, cy2 + 10], fill=WHITE, width=2)
        elif pattern == "hearts":
            for py2 in range(ty + 20, ty + th - 10, 35):
                for px2 in range(x + 25, x + tw - 10, 40):
                    draw_heart(draw, px2, py2, 18, WHITE, color, 1)
        elif pattern == "stars":
            for py2 in range(ty + 20, ty + th - 10, 35):
                for px2 in range(x + 25, x + tw - 10, 45):
                    draw_star(draw, px2, py2, 8, 4, fill=WHITE, outline=color, width=1)
        elif pattern == "plaid":
            for sx in range(x + 15, x + tw, 30):
                draw.line([sx, ty, sx, ty + th], fill=WHITE, width=2)
            for sy in range(ty + 10, ty + th, 30):
                draw.line([x + 5, sy, x + tw + 5, sy], fill=WHITE, width=2)
        elif pattern == "grid":
            for sx in range(x + 15, x + tw, 25):
                draw.line([sx, ty, sx, ty + th], fill=WHITE, width=1)
            for sy in range(ty + 10, ty + th, 25):
                draw.line([x + 5, sy, x + tw + 5, sy], fill=WHITE, width=1)
        elif pattern == "zigzag":
            for cy2 in range(ty + 10, ty + th - 10, 20):
                for cx2 in range(x + 10, x + tw, 30):
                    draw.line([cx2, cy2, cx2 + 15, cy2 + 15], fill=WHITE, width=2)
                    draw.line([cx2 + 15, cy2 + 15, cx2 + 30, cy2], fill=WHITE, width=2)
        elif pattern == "waves":
            for cy2 in range(ty + 15, ty + th, 25):
                for cx2 in range(x + 5, x + tw, 40):
                    draw.arc([cx2, cy2 - 8, cx2 + 20, cy2 + 8], 0, 180, fill=WHITE, width=2)
                    draw.arc([cx2 + 20, cy2 - 8, cx2 + 40, cy2 + 8], 180, 360, fill=WHITE, width=2)
        elif pattern == "dash":
            for py2 in range(ty + 15, ty + th, 20):
                for px2 in range(x + 15, x + tw, 30):
                    draw.line([px2, py2, px2 + 15, py2], fill=WHITE, width=3)
        else:
            # Default - small dots
            for py2 in range(ty + 15, ty + th - 5, 30):
                for px2 in range(x + 20, x + tw, 30):
                    draw_circle(draw, px2, py2, 4, WHITE)

        # Label below tape
        draw_text_centered(draw, label, x + STICKER_SIZE // 2, ty + th + 25, get_font(18), CHARCOAL)

    return img


# =================================================================
# Sheet 7: Speech Bubbles & Banners
# =================================================================
def draw_sheet_7_speech_bubbles():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    items = [
        ("Hello!", PINK, "speech"), ("OMG!", PEACH, "burst"), ("Note", YELLOW, "cloud"),
        ("Reminder", MINT, "ribbon"), ("Title", SKY, "banner"), ("Wow!", LAVENDER, "speech"),
        ("Love it!", PINK, "heart_bubble"), ("Idea!", YELLOW, "cloud"),
        ("Yes!", MINT, "speech"), ("Oops!", PEACH, "burst"),
        ("Plan", SKY, "ribbon"), ("Goals", LAVENDER, "banner"),
        ("Frame 1", PINK, "frame"), ("Frame 2", PEACH, "frame"),
        ("Frame 3", YELLOW, "frame"), ("Bracket L", MINT, "bracket_l"),
        ("Bracket R", SKY, "bracket_r"), ("Divider 1", LAVENDER, "divider"),
        ("Divider 2", PINK, "divider"), ("Divider 3", PEACH, "divider"),
        ("Tag", YELLOW, "tag"), ("Label", MINT, "label"),
        ("Box", SKY, "box"), ("Circle", LAVENDER, "circle_frame"),
        ("Scroll", PINK, "scroll"),
    ]

    font = get_font(26)

    for idx, (label, color, style) in enumerate(items):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2

        if style == "speech":
            draw.ellipse([x + 20, y + 20, x + STICKER_SIZE - 20, y + STICKER_SIZE - 50],
                         fill=color, outline=CHARCOAL, width=2)
            draw.polygon([(cx - 15, y + STICKER_SIZE - 55), (cx + 15, y + STICKER_SIZE - 55),
                          (cx - 30, y + STICKER_SIZE - 20)], fill=color, outline=CHARCOAL, width=2)
            # Fill gap
            draw.rectangle([cx - 14, y + STICKER_SIZE - 58, cx + 14, y + STICKER_SIZE - 48], fill=color)
            draw_text_centered(draw, label, cx, cy - 20, font, CHARCOAL)
        elif style == "burst":
            # Star burst
            points = []
            for i in range(12):
                angle = math.radians(i * 30 - 90)
                r = 80 if i % 2 == 0 else 55
                points.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
            draw.polygon(points, fill=color, outline=CHARCOAL, width=2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "cloud":
            # Thought cloud
            for dx2, dy2 in [(0, -35), (-35, -15), (35, -15), (-25, 20), (25, 20), (0, 10)]:
                draw_circle(draw, cx + dx2, cy + dy2, 40, color, CHARCOAL, 2)
            # Fill interior
            draw_circle(draw, cx, cy - 5, 45, color)
            draw_text_centered(draw, label, cx, cy - 5, font, CHARCOAL)
        elif style == "ribbon":
            draw.polygon([(x + 30, cy - 25), (x + STICKER_SIZE - 30, cy - 25),
                          (x + STICKER_SIZE - 15, cy), (x + STICKER_SIZE - 30, cy + 25),
                          (x + 30, cy + 25), (x + 15, cy)],
                         fill=color, outline=CHARCOAL, width=2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "banner":
            draw_rounded_rect(draw, (x + 15, y + 40, x + STICKER_SIZE - 15, y + STICKER_SIZE - 40),
                              radius=10, fill=color, outline=CHARCOAL, width=2)
            # Banner tails
            draw.polygon([(x + 15, y + STICKER_SIZE - 45), (x + 15, y + STICKER_SIZE - 25),
                          (x + 40, y + STICKER_SIZE - 40)], fill=color, outline=CHARCOAL, width=1)
            draw.polygon([(x + STICKER_SIZE - 15, y + STICKER_SIZE - 45),
                          (x + STICKER_SIZE - 15, y + STICKER_SIZE - 25),
                          (x + STICKER_SIZE - 40, y + STICKER_SIZE - 40)], fill=color, outline=CHARCOAL, width=1)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "frame":
            draw_rounded_rect(draw, (x + 15, y + 15, x + STICKER_SIZE - 15, y + STICKER_SIZE - 15),
                              radius=15, fill=None, outline=color, width=5)
            draw_rounded_rect(draw, (x + 25, y + 25, x + STICKER_SIZE - 25, y + STICKER_SIZE - 25),
                              radius=12, fill=None, outline=CHARCOAL, width=2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "bracket_l":
            draw.arc([x + 30, y + 30, x + 120, y + STICKER_SIZE - 30], 90, 270, fill=CHARCOAL, width=4)
            draw_text_centered(draw, "[", cx + 20, cy, get_font(80), color)
        elif style == "bracket_r":
            draw.arc([x + STICKER_SIZE - 120, y + 30, x + STICKER_SIZE - 30, y + STICKER_SIZE - 30],
                     270, 90, fill=CHARCOAL, width=4)
            draw_text_centered(draw, "]", cx - 20, cy, get_font(80), color)
        elif style == "divider":
            draw.line([x + 20, cy, x + STICKER_SIZE - 20, cy], fill=color, width=4)
            draw_circle(draw, cx, cy, 8, color, CHARCOAL, 2)
        elif style == "tag":
            draw_rounded_rect(draw, (x + 20, y + 40, x + STICKER_SIZE - 20, y + STICKER_SIZE - 40),
                              radius=8, fill=color, outline=CHARCOAL, width=2)
            draw_circle(draw, x + 45, y + 60, 6, WHITE, CHARCOAL, 2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "label":
            draw.rectangle([x + 20, y + 50, x + STICKER_SIZE - 20, y + STICKER_SIZE - 50],
                           fill=color, outline=CHARCOAL, width=2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "box":
            draw.rectangle([x + 25, y + 25, x + STICKER_SIZE - 25, y + STICKER_SIZE - 25],
                           fill=color, outline=CHARCOAL, width=3)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "circle_frame":
            draw_circle(draw, cx, cy, STICKER_SIZE // 2 - 15, None, color, 5)
            draw_circle(draw, cx, cy, STICKER_SIZE // 2 - 25, None, CHARCOAL, 2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "scroll":
            draw_rounded_rect(draw, (x + 25, y + 20, x + STICKER_SIZE - 25, y + STICKER_SIZE - 20),
                              radius=15, fill=color, outline=CHARCOAL, width=2)
            draw.ellipse([x + 20, y + 15, x + STICKER_SIZE - 20, y + 50], fill=color, outline=CHARCOAL, width=2)
            draw.ellipse([x + 20, y + STICKER_SIZE - 50, x + STICKER_SIZE - 20, y + STICKER_SIZE - 15],
                         fill=color, outline=CHARCOAL, width=2)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)
        elif style == "heart_bubble":
            draw_heart(draw, cx, cy - 10, 100, color, CHARCOAL, 2)
            draw_text_centered(draw, label, cx, cy - 10, get_font(20), CHARCOAL)
        else:
            sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color)
            draw_text_centered(draw, label, cx, cy, font, CHARCOAL)

    return img


# =================================================================
# Sheet 8: Icons & Symbols
# =================================================================
def draw_sheet_8_icons():
    img = Image.new("RGBA", (SHEET_SIZE, SHEET_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    icons = [
        ("Phone", MINT, "phone"), ("Email", SKY, "email"), ("Location", PINK, "pin"),
        ("Camera", PEACH, "camera"), ("Music", LAVENDER, "music"), ("Plane", SKY, "plane"),
        ("Car", YELLOW, "car"), ("Home", PEACH, "home"), ("Cart", MINT, "cart"),
        ("Dollar", YELLOW, "dollar"), ("Heart", PINK, "heart"), ("Lightbulb", YELLOW, "bulb"),
        ("Pencil", PEACH, "pencil"), ("Coffee", PINK, "coffee"), ("Clock", SKY, "clock"),
        ("Wifi", LAVENDER, "wifi"), ("Key", YELLOW, "key"), ("Lock", MINT, "lock"),
        ("Bell", PEACH, "bell"), ("Chat", SKY, "chat"), ("Globe", MINT, "globe"),
        ("Fire", PEACH, "fire"), ("Thunder", YELLOW, "thunder"), ("Link", SKY, "link"),
        ("Pin", PINK, "pushpin"),
    ]

    font = get_font(22)

    for idx, (label, color, icon) in enumerate(icons):
        row, col = divmod(idx, GRID)
        x = PADDING + col * (STICKER_SIZE + PADDING)
        y = PADDING + row * (STICKER_SIZE + PADDING)
        cx = x + STICKER_SIZE // 2
        cy = y + STICKER_SIZE // 2

        sticker_base(draw, x, y, STICKER_SIZE, STICKER_SIZE, color, shape="circle")

        icon_cy = cy - 20
        if icon == "phone":
            draw_rounded_rect(draw, (cx - 18, icon_cy - 35, cx + 18, icon_cy + 35),
                              radius=5, fill=WHITE, outline=CHARCOAL, width=2)
            draw.line([cx - 15, icon_cy + 20, cx + 15, icon_cy + 20], fill=CHARCOAL, width=1)
            draw_circle(draw, cx, icon_cy + 28, 4, CHARCOAL)
        elif icon == "email":
            draw.rectangle([cx - 35, icon_cy - 20, cx + 35, icon_cy + 20], fill=WHITE, outline=CHARCOAL, width=2)
            draw.line([cx - 35, icon_cy - 20, cx, icon_cy + 5], fill=CHARCOAL, width=2)
            draw.line([cx + 35, icon_cy - 20, cx, icon_cy + 5], fill=CHARCOAL, width=2)
        elif icon == "pin":
            draw.polygon([(cx, icon_cy + 40), (cx - 20, icon_cy - 5), (cx + 20, icon_cy - 5)],
                         fill=PINK, outline=CHARCOAL, width=2)
            draw_circle(draw, cx, icon_cy - 12, 20, PINK, CHARCOAL, 2)
            draw_circle(draw, cx, icon_cy - 12, 7, WHITE)
        elif icon == "camera":
            draw_rounded_rect(draw, (cx - 35, icon_cy - 18, cx + 35, icon_cy + 25),
                              radius=5, fill=WHITE, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 12, icon_cy - 28, cx + 12, icon_cy - 18], fill=WHITE, outline=CHARCOAL, width=2)
            draw_circle(draw, cx, icon_cy + 3, 15, None, CHARCOAL, 2)
        elif icon == "music":
            draw.ellipse([cx - 20, icon_cy + 5, cx, icon_cy + 25], fill=CHARCOAL)
            draw.line([cx, icon_cy - 35, cx, icon_cy + 15], fill=CHARCOAL, width=3)
            draw.ellipse([cx + 5, icon_cy - 5, cx + 25, icon_cy + 15], fill=CHARCOAL)
            draw.line([cx + 25, icon_cy - 45, cx + 25, icon_cy + 5], fill=CHARCOAL, width=3)
            draw.line([cx, icon_cy - 35, cx + 25, icon_cy - 45], fill=CHARCOAL, width=3)
        elif icon == "home":
            draw.polygon([(cx, icon_cy - 35), (cx - 40, icon_cy), (cx + 40, icon_cy)],
                         fill=PEACH, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 28, icon_cy, cx + 28, icon_cy + 30], fill=WHITE, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 8, icon_cy + 8, cx + 8, icon_cy + 30], fill=PEACH, outline=CHARCOAL, width=1)
        elif icon == "cart":
            draw.line([cx - 35, icon_cy - 20, cx - 20, icon_cy - 20], fill=CHARCOAL, width=3)
            draw.line([cx - 20, icon_cy - 20, cx - 10, icon_cy + 15], fill=CHARCOAL, width=2)
            draw.line([cx - 10, icon_cy + 15, cx + 25, icon_cy + 15], fill=CHARCOAL, width=2)
            draw.line([cx + 25, icon_cy + 15, cx + 30, icon_cy - 15], fill=CHARCOAL, width=2)
            draw.line([cx - 18, icon_cy - 15, cx + 30, icon_cy - 15], fill=CHARCOAL, width=2)
            draw_circle(draw, cx - 5, icon_cy + 25, 5, CHARCOAL)
            draw_circle(draw, cx + 20, icon_cy + 25, 5, CHARCOAL)
        elif icon == "dollar":
            draw_circle(draw, cx, icon_cy, 32, YELLOW, CHARCOAL, 2)
            draw_text_centered(draw, "$", cx, icon_cy, get_font(40), CHARCOAL)
        elif icon == "heart":
            draw_heart(draw, cx, icon_cy, 70, PINK, CHARCOAL, 2)
        elif icon == "bulb":
            draw_circle(draw, cx, icon_cy - 10, 28, YELLOW, CHARCOAL, 2)
            draw.rectangle([cx - 12, icon_cy + 18, cx + 12, icon_cy + 30], fill=WHITE, outline=CHARCOAL, width=2)
            # Rays
            for angle_d in [-45, 0, 45, 90, 135, 180, 225]:
                angle = math.radians(angle_d)
                draw.line([cx + int(32 * math.cos(angle)), icon_cy - 10 + int(32 * math.sin(angle)),
                           cx + int(42 * math.cos(angle)), icon_cy - 10 + int(42 * math.sin(angle))],
                          fill=CHARCOAL, width=1)
        elif icon == "pencil":
            draw.polygon([(cx - 5, icon_cy - 40), (cx + 5, icon_cy - 40), (cx + 10, icon_cy + 25),
                          (cx, icon_cy + 40), (cx - 10, icon_cy + 25)],
                         fill=PEACH, outline=CHARCOAL, width=2)
            draw.polygon([(cx - 5, icon_cy + 28), (cx, icon_cy + 40), (cx + 5, icon_cy + 28)],
                         fill=YELLOW, outline=CHARCOAL, width=1)
        elif icon == "coffee":
            draw_rounded_rect(draw, (cx - 25, icon_cy - 15, cx + 20, icon_cy + 25),
                              radius=3, fill=WHITE, outline=CHARCOAL, width=2)
            draw.arc([cx + 18, icon_cy - 5, cx + 38, icon_cy + 15], 270, 90, fill=CHARCOAL, width=2)
            # Steam
            for sx in [-10, 5]:
                draw.arc([cx + sx - 5, icon_cy - 35, cx + sx + 5, icon_cy - 20], 0, 180, fill=CHARCOAL, width=2)
        elif icon == "clock":
            draw_circle(draw, cx, icon_cy, 32, WHITE, CHARCOAL, 2)
            draw.line([cx, icon_cy, cx, icon_cy - 22], fill=CHARCOAL, width=2)
            draw.line([cx, icon_cy, cx + 18, icon_cy + 5], fill=CHARCOAL, width=2)
            draw_circle(draw, cx, icon_cy, 3, CHARCOAL)
        elif icon == "bell":
            draw.pieslice([cx - 25, icon_cy - 35, cx + 25, icon_cy + 10], 180, 360, fill=PEACH, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 25, icon_cy - 5, cx + 25, icon_cy + 10], fill=PEACH, outline=CHARCOAL, width=2)
            draw_circle(draw, cx, icon_cy + 15, 8, PEACH, CHARCOAL, 2)
            draw_circle(draw, cx, icon_cy - 35, 4, CHARCOAL)
        elif icon == "thunder":
            draw.polygon([(cx - 5, icon_cy - 40), (cx - 20, icon_cy), (cx - 2, icon_cy),
                          (cx - 10, icon_cy + 40), (cx + 20, icon_cy - 5), (cx + 2, icon_cy - 5),
                          (cx + 10, icon_cy - 40)],
                         fill=YELLOW, outline=CHARCOAL, width=2)
        elif icon == "fire":
            draw.polygon([(cx, icon_cy - 40), (cx + 25, icon_cy + 5), (cx + 15, icon_cy + 30),
                          (cx - 15, icon_cy + 30), (cx - 25, icon_cy + 5)],
                         fill=PEACH, outline=CHARCOAL, width=2)
            draw.polygon([(cx, icon_cy - 15), (cx + 12, icon_cy + 10), (cx, icon_cy + 25),
                          (cx - 12, icon_cy + 10)], fill=YELLOW, outline=CHARCOAL, width=1)
        elif icon == "wifi":
            for r in [40, 28, 16]:
                draw.arc([cx - r, icon_cy - r, cx + r, icon_cy + r], 225, 315, fill=CHARCOAL, width=3)
            draw_circle(draw, cx, icon_cy + 15, 4, CHARCOAL)
        elif icon == "globe":
            draw_circle(draw, cx, icon_cy, 32, MINT, CHARCOAL, 2)
            draw.arc([cx - 15, icon_cy - 32, cx + 15, icon_cy + 32], 0, 360, fill=CHARCOAL, width=1)
            draw.line([cx - 32, icon_cy, cx + 32, icon_cy], fill=CHARCOAL, width=1)
            draw.line([cx - 28, icon_cy - 15, cx + 28, icon_cy - 15], fill=CHARCOAL, width=1)
            draw.line([cx - 28, icon_cy + 15, cx + 28, icon_cy + 15], fill=CHARCOAL, width=1)
        elif icon == "chat":
            draw_rounded_rect(draw, (cx - 35, icon_cy - 25, cx + 35, icon_cy + 15),
                              radius=10, fill=WHITE, outline=CHARCOAL, width=2)
            draw.polygon([(cx - 10, icon_cy + 13), (cx + 5, icon_cy + 13), (cx - 15, icon_cy + 30)],
                         fill=WHITE, outline=CHARCOAL, width=2)
            draw.rectangle([cx - 9, icon_cy + 8, cx + 4, icon_cy + 16], fill=WHITE)
            # Dots
            for dx2 in [-15, 0, 15]:
                draw_circle(draw, cx + dx2, icon_cy - 5, 3, CHARCOAL)
        elif icon == "key":
            draw_circle(draw, cx - 15, icon_cy - 10, 18, YELLOW, CHARCOAL, 2)
            draw.rectangle([cx, icon_cy - 13, cx + 35, icon_cy - 7], fill=YELLOW, outline=CHARCOAL, width=2)
            draw.rectangle([cx + 25, icon_cy - 7, cx + 32, icon_cy + 5], fill=YELLOW, outline=CHARCOAL, width=1)
        elif icon == "lock":
            draw_rounded_rect(draw, (cx - 22, icon_cy - 5, cx + 22, icon_cy + 30),
                              radius=5, fill=MINT, outline=CHARCOAL, width=2)
            draw.arc([cx - 15, icon_cy - 30, cx + 15, icon_cy - 5], 180, 360, fill=CHARCOAL, width=3)
            draw_circle(draw, cx, icon_cy + 10, 4, CHARCOAL)
        elif icon == "pushpin":
            draw_circle(draw, cx, icon_cy - 15, 18, PINK, CHARCOAL, 2)
            draw.polygon([(cx - 8, icon_cy), (cx + 8, icon_cy), (cx, icon_cy + 35)],
                         fill=CHARCOAL)
        elif icon == "plane":
            draw.polygon([(cx, icon_cy - 35), (cx + 40, icon_cy + 5), (cx + 5, icon_cy),
                          (cx + 15, icon_cy + 30), (cx, icon_cy + 15),
                          (cx - 15, icon_cy + 30), (cx - 5, icon_cy),
                          (cx - 40, icon_cy + 5)],
                         fill=WHITE, outline=CHARCOAL, width=2)
        elif icon == "car":
            draw_rounded_rect(draw, (cx - 35, icon_cy - 5, cx + 35, icon_cy + 18),
                              radius=5, fill=WHITE, outline=CHARCOAL, width=2)
            draw_rounded_rect(draw, (cx - 25, icon_cy - 25, cx + 25, icon_cy - 2),
                              radius=8, fill=WHITE, outline=CHARCOAL, width=2)
            draw_circle(draw, cx - 20, icon_cy + 20, 8, CHARCOAL)
            draw_circle(draw, cx + 20, icon_cy + 20, 8, CHARCOAL)
        elif icon == "link":
            draw.arc([cx - 30, icon_cy - 15, cx + 5, icon_cy + 15], 90, 270, fill=CHARCOAL, width=3)
            draw.line([cx - 12, icon_cy - 15, cx + 12, icon_cy - 15], fill=CHARCOAL, width=3)
            draw.line([cx - 12, icon_cy + 15, cx + 12, icon_cy + 15], fill=CHARCOAL, width=3)
            draw.arc([cx - 5, icon_cy - 15, cx + 30, icon_cy + 15], 270, 90, fill=CHARCOAL, width=3)
        else:
            draw_text_centered(draw, icon[0].upper(), cx, icon_cy, get_font(36), CHARCOAL)

        draw_text_centered(draw, label, cx, cy + 50, font, CHARCOAL)

    return img


# =================================================================
# Generate Individual Stickers (200x200)
# =================================================================
def extract_individual_stickers(sheets, sheet_names):
    """Extract first 50 stickers as individual 200x200 PNGs."""
    count = 0
    for sheet_idx, (sheet_img, name) in enumerate(zip(sheets, sheet_names)):
        for row in range(GRID):
            for col in range(GRID):
                if count >= 50:
                    return count
                x = PADDING + col * (STICKER_SIZE + PADDING)
                y = PADDING + row * (STICKER_SIZE + PADDING)

                # Crop the sticker from the sheet
                crop = sheet_img.crop((x, y, x + STICKER_SIZE, y + STICKER_SIZE))
                # Resize to 200x200
                individual = crop.resize((INDIVIDUAL_SIZE, INDIVIDUAL_SIZE), Image.LANCZOS)

                fname = f"sticker_{count+1:03d}_{name}_r{row}c{col}.png"
                individual.save(os.path.join(INDIVIDUAL_DIR, fname))
                count += 1
    return count


# =================================================================
# Main
# =================================================================
def main():
    print("Generating Digital Planner Sticker Sheets...")

    sheet_funcs = [
        ("sheet_1_daily_planner", draw_sheet_1_daily_planner),
        ("sheet_2_motivational", draw_sheet_2_motivational),
        ("sheet_3_functional_tabs", draw_sheet_3_functional_tabs),
        ("sheet_4_habit_tracker", draw_sheet_4_habit_tracker),
        ("sheet_5_seasonal", draw_sheet_5_seasonal),
        ("sheet_6_washi_tape", draw_sheet_6_washi_tape),
        ("sheet_7_speech_bubbles", draw_sheet_7_speech_bubbles),
        ("sheet_8_icons", draw_sheet_8_icons),
    ]

    sheets = []
    sheet_names = []
    for name, func in sheet_funcs:
        print(f"  Creating {name}...")
        img = func()
        out_path = os.path.join(SCRIPT_DIR, f"{name}.png")
        img.save(out_path)
        print(f"    Saved {out_path}")
        sheets.append(img)
        sheet_names.append(name)

    print(f"\nExtracting individual stickers to {INDIVIDUAL_DIR}...")
    n = extract_individual_stickers(sheets, sheet_names)
    print(f"  Extracted {n} individual stickers (200x200 px each)")

    print("\nAll sticker sheets generated successfully!")
    print(f"  8 sheets at {SHEET_SIZE}x{SHEET_SIZE} px (PNG with transparency)")
    print(f"  {n} individual stickers at {INDIVIDUAL_SIZE}x{INDIVIDUAL_SIZE} px")


if __name__ == "__main__":
    main()
