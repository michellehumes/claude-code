#!/usr/bin/env python3
"""
Create 10 Etsy listing images for the 2026 Wellness & Productivity Digital Planner.

Based on Etsy 2026 best practices:
- 2400x2400px square format (best CTR)
- Clean, neutral backgrounds (warm linen / white)
- Strong typography with clear hierarchy
- Product mockups showing planner on iPad
- Consistent brand colors (Patina Blue palette)
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/home/user/claude-code/etsy-digital-planner/images"
SIZE = 2400

# Color palette matching the planner
PATINA_BLUE = (126, 172, 176)
DEEP_TEAL = (62, 105, 110)
WARM_LINEN = (243, 237, 228)
SOFT_SAGE = (183, 203, 180)
DUSTY_ROSE = (210, 175, 170)
CHARCOAL = (55, 55, 60)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 218, 213)
NEAR_WHITE = (250, 248, 245)


def get_font(size, bold=False):
    """Get a font, falling back to default if needed."""
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_ipad_mockup(draw, x, y, w, h, screen_color=WHITE):
    """Draw a simplified iPad mockup."""
    # iPad body (dark gray bezel)
    bezel = 20
    draw.rounded_rectangle([x, y, x+w, y+h], radius=30, fill=(40, 40, 42), outline=(30, 30, 32), width=2)
    # Screen
    draw.rectangle([x+bezel, y+bezel, x+w-bezel, y+h-bezel], fill=screen_color)
    # Home button
    btn_size = 30
    draw.ellipse([x + w//2 - btn_size//2, y + h - bezel + 2, x + w//2 + btn_size//2, y + h - 4], outline=(80, 80, 82), width=2)
    return (x+bezel, y+bezel, x+w-bezel, y+h-bezel)


def draw_planner_preview(draw, sx, sy, sw, sh):
    """Draw a mini planner layout inside the screen area."""
    # Background
    draw.rectangle([sx, sy, sx+sw, sy+sh], fill=WARM_LINEN)

    # Left sidebar tabs
    tab_w = int(sw * 0.08)
    tab_labels = ["H", "Y", "M", "W", "D", "G", "H", "W", "J", "N"]
    tab_h = sh // 12
    for i, label in enumerate(tab_labels):
        ty = sy + 10 + i * (tab_h + 3)
        color = PATINA_BLUE if i == 2 else DEEP_TEAL
        draw.rectangle([sx, ty, sx + tab_w, ty + tab_h], fill=color)

    # Content area header
    cx = sx + tab_w + 10
    cy = sy + 15
    cw = sw - tab_w - 20
    font_title = get_font(max(14, sh // 20), bold=True)
    draw.text((cx, cy), "February 2026", fill=DEEP_TEAL, font=font_title)

    # Calendar grid
    grid_y = cy + sh // 12
    cell_w = cw // 7
    cell_h = (sh - grid_y + sy - 30) // 6
    days = ["M", "T", "W", "T", "F", "S", "S"]
    font_sm = get_font(max(10, sh // 30))
    font_day = get_font(max(10, sh // 30), bold=True)

    # Day headers
    for d, day in enumerate(days):
        dx = cx + d * cell_w
        draw.rectangle([dx, grid_y, dx + cell_w - 2, grid_y + cell_h - 2], fill=DEEP_TEAL)
        draw.text((dx + cell_w // 4, grid_y + 2), day, fill=WHITE, font=font_sm)

    # Day cells
    import calendar
    cal = calendar.monthcalendar(2026, 2)
    for wi, week in enumerate(cal):
        for di, day_num in enumerate(week):
            dx = cx + di * cell_w
            dy = grid_y + (wi + 1) * cell_h
            if day_num > 0:
                draw.rectangle([dx, dy, dx + cell_w - 2, dy + cell_h - 2], fill=WHITE, outline=LIGHT_GRAY)
                draw.text((dx + 3, dy + 2), str(day_num), fill=DEEP_TEAL, font=font_sm)


def draw_accent_bars(draw, y, width):
    """Draw the decorative triple accent bar."""
    bar_h = 8
    draw.rectangle([0, y, width, y + bar_h], fill=PATINA_BLUE)
    draw.rectangle([0, y + bar_h, width, y + bar_h * 2], fill=DUSTY_ROSE)
    draw.rectangle([0, y + bar_h * 2, width, y + bar_h * 3], fill=SOFT_SAGE)


def draw_feature_badge(draw, x, y, text, color=PATINA_BLUE):
    """Draw a rounded feature badge."""
    font = get_font(36)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 20
    draw.rounded_rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], radius=25, fill=color)
    draw.text((x + pad, y + pad), text, fill=WHITE, font=font)
    return tw + pad * 2


# ──────────────────────────────────────────────────────────
# IMAGE 1: HERO / THUMBNAIL - The most important image
# Clean title with iPad mockup
# ──────────────────────────────────────────────────────────

def create_image_01_hero():
    img = Image.new('RGB', (SIZE, SIZE), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    # Top accent bars
    draw_accent_bars(draw, 0, SIZE)

    # Title area
    font_year = get_font(180, bold=True)
    font_title = get_font(72, bold=True)
    font_sub = get_font(48)
    font_sm = get_font(36)

    draw.text((SIZE // 2, 180), "2026", fill=DEEP_TEAL, font=font_year, anchor="mt")
    draw.text((SIZE // 2, 400), "WELLNESS & PRODUCTIVITY", fill=CHARCOAL, font=font_sub, anchor="mt")
    draw.text((SIZE // 2, 480), "Digital Planner", fill=DEEP_TEAL, font=font_title, anchor="mt")

    # Decorative line
    draw.rectangle([SIZE // 2 - 200, 580, SIZE // 2 + 200, 583], fill=PATINA_BLUE)

    # iPad mockup centered
    ipad_w, ipad_h = 1200, 900
    ipad_x = (SIZE - ipad_w) // 2
    ipad_y = 650
    screen = draw_ipad_mockup(draw, ipad_x, ipad_y, ipad_w, ipad_h)
    draw_planner_preview(draw, screen[0], screen[1], screen[2] - screen[0], screen[3] - screen[1])

    # Bottom feature badges
    badges = ["GoodNotes", "Notability", "Xodo", "iPad"]
    badge_y = 1620
    total_w = 0
    widths = []
    for b in badges:
        font = get_font(32)
        bbox = font.getbbox(b)
        w = bbox[2] - bbox[0] + 40
        widths.append(w)
        total_w += w
    gap = 30
    total_w += gap * (len(badges) - 1)
    bx = (SIZE - total_w) // 2
    for i, (b, w) in enumerate(zip(badges, widths)):
        draw.rounded_rectangle([bx, badge_y, bx + w, badge_y + 60], radius=30, fill=DEEP_TEAL)
        draw.text((bx + 20, badge_y + 10), b, fill=WHITE, font=get_font(32))
        bx += w + gap

    # Bottom accent
    draw_accent_bars(draw, SIZE - 24, SIZE)

    # Price indicator
    draw.rounded_rectangle([SIZE - 380, 100, SIZE - 60, 200], radius=20, fill=DUSTY_ROSE)
    draw.text((SIZE - 340, 115), "BEST", fill=WHITE, font=get_font(36, bold=True))
    draw.text((SIZE - 340, 155), "SELLER", fill=WHITE, font=get_font(30))

    img.save(os.path.join(OUTPUT_DIR, "01_hero_thumbnail.png"), quality=95)
    print("Created: 01_hero_thumbnail.png")


# ──────────────────────────────────────────────────────────
# IMAGE 2: FEATURE OVERVIEW
# ──────────────────────────────────────────────────────────

def create_image_02_features():
    img = Image.new('RGB', (SIZE, SIZE), NEAR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_accent_bars(draw, 0, SIZE)

    font_title = get_font(80, bold=True)
    draw.text((SIZE // 2, 100), "Everything You Need", fill=DEEP_TEAL, font=font_title, anchor="mt")
    draw.text((SIZE // 2, 200), "In One Planner", fill=PATINA_BLUE, font=get_font(60), anchor="mt")

    # Feature grid (3x3)
    features = [
        ("Daily Planning", "Structured daily layouts\nwith time blocking"),
        ("Weekly Spreads", "Full weekly overview\nwith wellness check-in"),
        ("Monthly Calendar", "12 months of\ncalendar grids"),
        ("Goal Setting", "Quarterly goals +\nlife wheel assessment"),
        ("Habit Tracker", "31-day grid for\n16 custom habits"),
        ("Wellness Dashboard", "Sleep, meals, fitness\n& self-care tracking"),
        ("Guided Journal", "Morning & evening\nreflection prompts"),
        ("Mood & Water", "Daily mood & hydration\ntracking built-in"),
        ("Notes Pages", "Lined notes for\nbrainstorming & ideas"),
    ]

    grid_start_y = 340
    cell_size = 550
    gap = 60
    cols = 3
    total_grid_w = cols * cell_size + (cols - 1) * gap
    start_x = (SIZE - total_grid_w) // 2

    colors = [PATINA_BLUE, SOFT_SAGE, DUSTY_ROSE, DEEP_TEAL, PATINA_BLUE, SOFT_SAGE, DUSTY_ROSE, DEEP_TEAL, PATINA_BLUE]

    for i, (title, desc) in enumerate(features):
        col = i % 3
        row = i // 3
        x = start_x + col * (cell_size + gap)
        y = grid_start_y + row * (cell_size + gap)

        # Card
        draw.rounded_rectangle([x, y, x + cell_size, y + cell_size], radius=25, fill=WHITE, outline=LIGHT_GRAY, width=2)

        # Color accent bar at top
        draw.rounded_rectangle([x, y, x + cell_size, y + 8], radius=0, fill=colors[i])

        # Number circle
        draw.ellipse([x + cell_size // 2 - 35, y + 30, x + cell_size // 2 + 35, y + 100], fill=colors[i])
        draw.text((x + cell_size // 2, y + 45), str(i + 1), fill=WHITE, font=get_font(44, bold=True), anchor="mt")

        # Title
        draw.text((x + cell_size // 2, y + 130), title, fill=DEEP_TEAL, font=get_font(38, bold=True), anchor="mt")

        # Description
        for li, line in enumerate(desc.split('\n')):
            draw.text((x + cell_size // 2, y + 190 + li * 45), line.strip(), fill=CHARCOAL, font=get_font(30), anchor="mt")

    # Bottom
    draw.rectangle([0, SIZE - 100, SIZE, SIZE], fill=DEEP_TEAL)
    draw.text((SIZE // 2, SIZE - 70), "28 Pages | Fully Hyperlinked | Instant Download", fill=WHITE, font=get_font(40), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "02_feature_overview.png"), quality=95)
    print("Created: 02_feature_overview.png")


# ──────────────────────────────────────────────────────────
# IMAGE 3: MONTHLY CALENDAR PREVIEW
# ──────────────────────────────────────────────────────────

def create_image_03_monthly():
    img = Image.new('RGB', (SIZE, SIZE), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    draw_accent_bars(draw, 0, SIZE)

    draw.text((SIZE // 2, 100), "Monthly Calendar View", fill=DEEP_TEAL, font=get_font(80, bold=True), anchor="mt")
    draw.text((SIZE // 2, 200), "Plan your month at a glance", fill=CHARCOAL, font=get_font(44), anchor="mt")

    # Large iPad with monthly view
    ipad_w, ipad_h = 2000, 1400
    ipad_x = (SIZE - ipad_w) // 2
    ipad_y = 330
    screen = draw_ipad_mockup(draw, ipad_x, ipad_y, ipad_w, ipad_h)
    sx, sy, ex, ey = screen
    sw, sh = ex - sx, ey - sy

    # Draw monthly calendar inside
    draw.rectangle([sx, sy, ex, ey], fill=WARM_LINEN)

    # Sidebar
    tab_w = int(sw * 0.06)
    for i in range(10):
        ty = sy + 5 + i * (sh // 11)
        color = PATINA_BLUE if i == 2 else DEEP_TEAL
        draw.rectangle([sx, ty, sx + tab_w, ty + sh // 12], fill=color)

    # Header
    cx = sx + tab_w + 20
    draw.text((cx, sy + 15), "March 2026", fill=DEEP_TEAL, font=get_font(60, bold=True))

    # Calendar
    import calendar
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cal = calendar.monthcalendar(2026, 3)
    grid_y = sy + 100
    cell_w = (sw - tab_w - 40) // 7
    cell_h = (sh - 140) // 6

    # Day headers
    for d, day in enumerate(days):
        dx = cx + d * cell_w
        draw.rectangle([dx, grid_y, dx + cell_w - 3, grid_y + cell_h - 3], fill=DEEP_TEAL)
        draw.text((dx + cell_w // 2, grid_y + cell_h // 3), day[:3], fill=WHITE, font=get_font(24, bold=True), anchor="mt")

    for wi, week in enumerate(cal):
        for di, day_num in enumerate(week):
            dx = cx + di * cell_w
            dy = grid_y + (wi + 1) * cell_h
            if day_num > 0:
                draw.rectangle([dx, dy, dx + cell_w - 3, dy + cell_h - 3], fill=WHITE, outline=LIGHT_GRAY)
                draw.text((dx + 8, dy + 5), str(day_num), fill=DEEP_TEAL, font=get_font(28, bold=True))
                # Fake notes lines
                for li in range(3):
                    ly = dy + 40 + li * 20
                    if ly < dy + cell_h - 10:
                        draw.line([(dx + 8, ly), (dx + cell_w - 15, ly)], fill=LIGHT_GRAY, width=1)

    # Bottom callout
    draw.rounded_rectangle([200, 1850, SIZE - 200, 2000], radius=30, fill=DEEP_TEAL)
    draw.text((SIZE // 2, 1890), "All 12 months included with clickable navigation", fill=WHITE, font=get_font(40), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "03_monthly_preview.png"), quality=95)
    print("Created: 03_monthly_preview.png")


# ──────────────────────────────────────────────────────────
# IMAGE 4: DAILY PLANNER PREVIEW
# ──────────────────────────────────────────────────────────

def create_image_04_daily():
    img = Image.new('RGB', (SIZE, SIZE), NEAR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_accent_bars(draw, 0, SIZE)

    draw.text((SIZE // 2, 100), "Daily Planner Layout", fill=DEEP_TEAL, font=get_font(80, bold=True), anchor="mt")
    draw.text((SIZE // 2, 200), "Structure your day for success", fill=CHARCOAL, font=get_font(44), anchor="mt")

    # iPad mockup
    ipad_w, ipad_h = 2000, 1400
    ipad_x = (SIZE - ipad_w) // 2
    ipad_y = 320
    screen = draw_ipad_mockup(draw, ipad_x, ipad_y, ipad_w, ipad_h)
    sx, sy, ex, ey = screen
    sw, sh = ex - sx, ey - sy

    draw.rectangle([sx, sy, ex, ey], fill=WARM_LINEN)

    # Sidebar
    tab_w = int(sw * 0.06)
    for i in range(10):
        ty = sy + 5 + i * (sh // 11)
        color = PATINA_BLUE if i == 4 else DEEP_TEAL
        draw.rectangle([sx, ty, sx + tab_w, ty + sh // 12], fill=color)

    cx = sx + tab_w + 20
    draw.text((cx, sy + 15), "Daily Planner", fill=DEEP_TEAL, font=get_font(50, bold=True))

    # Morning routine box
    bx = cx
    by = sy + 90
    bw = (sw - tab_w - 50) // 2
    bh = 250
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=WHITE, outline=LIGHT_GRAY, width=2)
    draw.text((bx + 15, by + 10), "Morning Routine", fill=SOFT_SAGE, font=get_font(28, bold=True))
    items = ["Wake up time:", "Water intake:", "Movement:", "Mindfulness:"]
    for i, item in enumerate(items):
        iy = by + 50 + i * 48
        draw.text((bx + 20, iy), item, fill=CHARCOAL, font=get_font(22))
        draw.line([(bx + 170, iy + 28), (bx + bw - 20, iy + 28)], fill=LIGHT_GRAY, width=1)

    # Schedule box
    sby = by + bh + 20
    sbh = sh - (sby - sy) - 20
    draw.rounded_rectangle([bx, sby, bx + bw, sby + sbh], radius=10, fill=WHITE, outline=LIGHT_GRAY, width=2)
    draw.text((bx + 15, sby + 10), "Schedule", fill=DEEP_TEAL, font=get_font(28, bold=True))
    hours = ["7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM"]
    for i, hour in enumerate(hours):
        hy = sby + 50 + i * 38
        if hy < sby + sbh - 20:
            draw.text((bx + 15, hy), hour, fill=(150, 150, 150), font=get_font(18))
            draw.line([(bx + 90, hy + 22), (bx + bw - 15, hy + 22)], fill=LIGHT_GRAY, width=1)

    # Right column
    rx = cx + bw + 20
    # Top 3 priorities
    draw.rounded_rectangle([rx, by, rx + bw, by + 180], radius=10, fill=WHITE, outline=LIGHT_GRAY, width=2)
    draw.text((rx + 15, by + 10), "Top 3 Priorities", fill=PATINA_BLUE, font=get_font(28, bold=True))
    for i in range(3):
        py = by + 55 + i * 40
        draw.ellipse([rx + 15, py, rx + 40, py + 25], fill=PATINA_BLUE)
        draw.text((rx + 21, py + 2), str(i + 1), fill=WHITE, font=get_font(18, bold=True))
        draw.line([(rx + 50, py + 22), (rx + bw - 15, py + 22)], fill=LIGHT_GRAY, width=1)

    # To-do list
    ty = by + 200
    draw.rounded_rectangle([rx, ty, rx + bw, ty + 280], radius=10, fill=WHITE, outline=LIGHT_GRAY, width=2)
    draw.text((rx + 15, ty + 10), "To-Do List", fill=DEEP_TEAL, font=get_font(28, bold=True))
    for i in range(6):
        iy = ty + 50 + i * 38
        draw.rectangle([rx + 15, iy, rx + 35, iy + 20], outline=(150, 150, 150), width=1)
        draw.line([(rx + 45, iy + 18), (rx + bw - 15, iy + 18)], fill=LIGHT_GRAY, width=1)

    # Gratitude
    gy = ty + 300
    draw.rounded_rectangle([rx, gy, rx + bw, gy + 180], radius=10, fill=(245, 238, 235), outline=DUSTY_ROSE, width=2)
    draw.text((rx + 15, gy + 10), "Gratitude & Reflection", fill=DUSTY_ROSE, font=get_font(26, bold=True))
    draw.text((rx + 20, gy + 45), "Today I am grateful for...", fill=(150, 150, 150), font=get_font(20))
    for i in range(3):
        ly = gy + 80 + i * 30
        draw.line([(rx + 20, ly), (rx + bw - 20, ly)], fill=LIGHT_GRAY, width=1)

    # Bottom
    draw.rounded_rectangle([200, 1830, SIZE - 200, 1980], radius=30, fill=DUSTY_ROSE)
    draw.text((SIZE // 2, 1870), "Morning routine + schedule + gratitude in one page", fill=WHITE, font=get_font(40), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "04_daily_preview.png"), quality=95)
    print("Created: 04_daily_preview.png")


# ──────────────────────────────────────────────────────────
# IMAGE 5: WELLNESS FEATURES
# ──────────────────────────────────────────────────────────

def create_image_05_wellness():
    img = Image.new('RGB', (SIZE, SIZE), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    # Full width teal header
    draw.rectangle([0, 0, SIZE, 300], fill=DEEP_TEAL)
    draw.text((SIZE // 2, 80), "Built for Your", fill=WHITE, font=get_font(70), anchor="mt")
    draw.text((SIZE // 2, 170), "WELLNESS", fill=PATINA_BLUE, font=get_font(100, bold=True), anchor="mt")

    # Wellness feature cards
    cards = [
        ("Sleep Tracker", "Track bedtime, wake time,\nhours & sleep quality\nfor every day of the week", PATINA_BLUE),
        ("Meal Planner", "Weekly breakfast, lunch,\ndinner & snack planning\nfor healthy eating habits", SOFT_SAGE),
        ("Fitness Log", "Log activities, duration,\nintensity & personal notes\nfor every workout", DUSTY_ROSE),
        ("Self-Care Menu", "15 self-care ideas to\ncheck off each week\nfor balanced living", DEEP_TEAL),
        ("Mood Tracking", "Daily mood check-in\nwith visual indicators\ntrack emotional patterns", PATINA_BLUE),
        ("Water Intake", "8-glass daily tracker\nstay hydrated with\nvisual water drop tracking", SOFT_SAGE),
    ]

    card_w = 680
    card_h = 450
    gap = 60
    cols = 3
    total_w = cols * card_w + (cols - 1) * gap
    start_x = (SIZE - total_w) // 2

    for i, (title, desc, color) in enumerate(cards):
        col = i % 3
        row = i // 3
        x = start_x + col * (card_w + gap)
        y = 400 + row * (card_h + gap)

        # Card
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=25, fill=WHITE, outline=LIGHT_GRAY, width=2)

        # Color top bar
        draw.rectangle([x + 2, y + 2, x + card_w - 2, y + 12], fill=color)

        # Title
        draw.text((x + card_w // 2, y + 50), title, fill=color, font=get_font(48, bold=True), anchor="mt")

        # Divider
        draw.rectangle([x + card_w // 2 - 80, y + 115, x + card_w // 2 + 80, y + 117], fill=LIGHT_GRAY)

        # Description
        for li, line in enumerate(desc.split('\n')):
            draw.text((x + card_w // 2, y + 145 + li * 50), line.strip(), fill=CHARCOAL, font=get_font(32), anchor="mt")

    # Bottom bar
    draw.rectangle([0, SIZE - 120, SIZE, SIZE], fill=DEEP_TEAL)
    draw.text((SIZE // 2, SIZE - 85), "Complete wellness tracking built into every week", fill=WHITE, font=get_font(42), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "05_wellness_features.png"), quality=95)
    print("Created: 05_wellness_features.png")


# ──────────────────────────────────────────────────────────
# IMAGE 6: HABIT TRACKER PREVIEW
# ──────────────────────────────────────────────────────────

def create_image_06_habits():
    img = Image.new('RGB', (SIZE, SIZE), NEAR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_accent_bars(draw, 0, SIZE)

    draw.text((SIZE // 2, 100), "Habit Tracker", fill=DEEP_TEAL, font=get_font(90, bold=True), anchor="mt")
    draw.text((SIZE // 2, 220), "Build consistency with 31-day tracking", fill=CHARCOAL, font=get_font(44), anchor="mt")

    # iPad mockup with habit tracker
    ipad_w, ipad_h = 2000, 1400
    ipad_x = (SIZE - ipad_w) // 2
    ipad_y = 350
    screen = draw_ipad_mockup(draw, ipad_x, ipad_y, ipad_w, ipad_h)
    sx, sy, ex, ey = screen
    sw, sh = ex - sx, ey - sy

    draw.rectangle([sx, sy, ex, ey], fill=WARM_LINEN)

    # Header
    draw.text((sx + 100, sy + 20), "Monthly Habit Tracker", fill=DEEP_TEAL, font=get_font(40, bold=True))

    # Habit grid
    habit_col = 300
    day_col = int((sw - habit_col - 40) / 31)
    row_h = (sh - 80) // 14

    # Day header row
    for d in range(1, 32):
        dx = sx + 20 + habit_col + (d - 1) * day_col
        draw.rectangle([dx, sy + 70, dx + day_col - 1, sy + 70 + row_h], fill=DEEP_TEAL)
        if d % 3 == 1:
            draw.text((dx + 2, sy + 75), str(d), fill=WHITE, font=get_font(14))

    # Habit rows
    habits = [
        "Exercise 30 min", "Drink 8 glasses water", "Read 20 pages",
        "Meditate 10 min", "Sleep 7+ hours", "No screen before bed",
        "Eat fruits/veggies", "Practice gratitude", "Journal",
        "Connect with friend", "Creative time", "Walk outdoors"
    ]

    for i, habit in enumerate(habits):
        ry = sy + 70 + (i + 1) * row_h
        bg = WHITE if i % 2 == 0 else (248, 246, 242)
        draw.rectangle([sx + 20, ry, sx + 20 + habit_col, ry + row_h], fill=bg)
        draw.text((sx + 25, ry + 5), habit, fill=CHARCOAL, font=get_font(18))

        for d in range(31):
            dx = sx + 20 + habit_col + d * day_col
            draw.rectangle([dx, ry, dx + day_col - 1, ry + row_h], fill=bg, outline=LIGHT_GRAY)
            # Some filled in for visual appeal
            if (i + d) % 5 < 3 and d < 15:
                draw.rectangle([dx + 2, ry + 2, dx + day_col - 3, ry + row_h - 2], fill=PATINA_BLUE)

    # Bottom callouts
    draw.rounded_rectangle([200, 1850, 780, 2000], radius=30, fill=PATINA_BLUE)
    draw.text((490, 1890), "12 pre-set habits", fill=WHITE, font=get_font(38), anchor="mt")

    draw.rounded_rectangle([850, 1850, 1550, 2000], radius=30, fill=SOFT_SAGE)
    draw.text((1200, 1890), "4 blank rows", fill=WHITE, font=get_font(38), anchor="mt")

    draw.rounded_rectangle([1620, 1850, 2200, 2000], radius=30, fill=DUSTY_ROSE)
    draw.text((1910, 1890), "Monthly reflection", fill=WHITE, font=get_font(38), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "06_habit_tracker.png"), quality=95)
    print("Created: 06_habit_tracker.png")


# ──────────────────────────────────────────────────────────
# IMAGE 7: GOAL SETTING PREVIEW
# ──────────────────────────────────────────────────────────

def create_image_07_goals():
    img = Image.new('RGB', (SIZE, SIZE), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    # Teal header
    draw.rectangle([0, 0, SIZE, 280], fill=DEEP_TEAL)
    draw.text((SIZE // 2, 60), "Set Goals.", fill=PATINA_BLUE, font=get_font(90, bold=True), anchor="mt")
    draw.text((SIZE // 2, 170), "Crush Them.", fill=WHITE, font=get_font(90, bold=True), anchor="mt")

    # Four quarter cards
    quarters = [
        ("Q1", "Jan - Mar", PATINA_BLUE),
        ("Q2", "Apr - Jun", SOFT_SAGE),
        ("Q3", "Jul - Sep", DUSTY_ROSE),
        ("Q4", "Oct - Dec", DEEP_TEAL),
    ]

    card_w = 520
    card_h = 600
    gap = 40
    total_w = 4 * card_w + 3 * gap
    start_x = (SIZE - total_w) // 2

    for i, (q, period, color) in enumerate(quarters):
        x = start_x + i * (card_w + gap)
        y = 380

        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=20, fill=WHITE, outline=color, width=3)

        # Quarter header
        draw.rounded_rectangle([x + 20, y + 20, x + card_w - 20, y + 120], radius=15, fill=color)
        draw.text((x + card_w // 2, y + 40), q, fill=WHITE, font=get_font(50, bold=True), anchor="mt")
        draw.text((x + card_w // 2, y + 85), period, fill=WHITE, font=get_font(28), anchor="mt")

        # Goal lines with checkboxes
        for g in range(5):
            gy = y + 160 + g * 80
            draw.rectangle([x + 30, gy, x + 55, gy + 25], outline=color, width=2)
            draw.line([(x + 70, gy + 22), (x + card_w - 30, gy + 22)], fill=LIGHT_GRAY, width=2)

    # Life wheel section
    wy = 1060
    draw.rounded_rectangle([100, wy, SIZE - 100, wy + 350], radius=25, fill=WHITE, outline=PATINA_BLUE, width=2)
    draw.text((SIZE // 2, wy + 30), "Life Wheel Assessment", fill=DEEP_TEAL, font=get_font(56, bold=True), anchor="mt")
    draw.text((SIZE // 2, wy + 100), "Rate 8 life areas from 1-10 to find your focus", fill=CHARCOAL, font=get_font(36), anchor="mt")

    areas = ["Health", "Career", "Relationships", "Finances", "Fun", "Growth", "Environment", "Spirituality"]
    badge_colors = [PATINA_BLUE, SOFT_SAGE, DUSTY_ROSE, DEEP_TEAL, PATINA_BLUE, SOFT_SAGE, DUSTY_ROSE, DEEP_TEAL]
    total_badges_w = len(areas) * 240 + (len(areas) - 1) * 20
    bx = (SIZE - total_badges_w) // 2
    for i, (area, bc) in enumerate(zip(areas, badge_colors)):
        draw.rounded_rectangle([bx, wy + 170, bx + 240, wy + 230], radius=15, fill=bc)
        draw.text((bx + 120, wy + 185), area, fill=WHITE, font=get_font(26, bold=True), anchor="mt")
        bx += 260

    # Word of the year
    draw.rounded_rectangle([600, 1500, SIZE - 600, 1680], radius=25, fill=DEEP_TEAL)
    draw.text((SIZE // 2, 1530), "Choose Your", fill=PATINA_BLUE, font=get_font(44), anchor="mt")
    draw.text((SIZE // 2, 1590), "WORD OF THE YEAR", fill=WHITE, font=get_font(56, bold=True), anchor="mt")

    # Bottom
    draw_accent_bars(draw, SIZE - 24, SIZE)

    img.save(os.path.join(OUTPUT_DIR, "07_goal_setting.png"), quality=95)
    print("Created: 07_goal_setting.png")


# ──────────────────────────────────────────────────────────
# IMAGE 8: GUIDED JOURNAL PREVIEW
# ──────────────────────────────────────────────────────────

def create_image_08_journal():
    img = Image.new('RGB', (SIZE, SIZE), NEAR_WHITE)
    draw = ImageDraw.Draw(img)

    draw_accent_bars(draw, 0, SIZE)

    draw.text((SIZE // 2, 100), "Guided Journal", fill=DEEP_TEAL, font=get_font(90, bold=True), anchor="mt")
    draw.text((SIZE // 2, 220), "Reflect, grow & find gratitude daily", fill=CHARCOAL, font=get_font(44), anchor="mt")

    # Two large cards side by side
    card_w = 1050
    card_h = 900
    gap = 60
    start_x = (SIZE - 2 * card_w - gap) // 2

    # Morning card
    mx = start_x
    my = 340
    draw.rounded_rectangle([mx, my, mx + card_w, my + card_h], radius=25, fill=WHITE, outline=SOFT_SAGE, width=3)
    draw.rectangle([mx + 3, my + 3, mx + card_w - 3, my + 15], fill=SOFT_SAGE)
    draw.text((mx + card_w // 2, my + 50), "Morning Pages", fill=SOFT_SAGE, font=get_font(52, bold=True), anchor="mt")

    morning_prompts = [
        "Today I am grateful for...",
        "My intention for today is...",
        "I will feel accomplished when...",
        "One thing I'm looking forward to...",
    ]
    for i, prompt in enumerate(morning_prompts):
        py = my + 140 + i * 180
        draw.text((mx + 40, py), prompt, fill=CHARCOAL, font=get_font(34))
        for li in range(3):
            draw.line([(mx + 40, py + 50 + li * 38), (mx + card_w - 40, py + 50 + li * 38)], fill=LIGHT_GRAY, width=1)

    # Evening card
    ex_card = start_x + card_w + gap
    draw.rounded_rectangle([ex_card, my, ex_card + card_w, my + card_h], radius=25, fill=WHITE, outline=DUSTY_ROSE, width=3)
    draw.rectangle([ex_card + 3, my + 3, ex_card + card_w - 3, my + 15], fill=DUSTY_ROSE)
    draw.text((ex_card + card_w // 2, my + 50), "Evening Reflection", fill=DUSTY_ROSE, font=get_font(52, bold=True), anchor="mt")

    evening_prompts = [
        "Best moment of today...",
        "Something I learned...",
        "How did I show kindness...",
        "Tomorrow I will...",
    ]
    for i, prompt in enumerate(evening_prompts):
        py = my + 140 + i * 180
        draw.text((ex_card + 40, py), prompt, fill=CHARCOAL, font=get_font(34))
        for li in range(3):
            draw.line([(ex_card + 40, py + 50 + li * 38), (ex_card + card_w - 40, py + 50 + li * 38)], fill=LIGHT_GRAY, width=1)

    # Weekly reflection banner
    wy = 1350
    draw.rounded_rectangle([100, wy, SIZE - 100, wy + 250], radius=25, fill=PATINA_BLUE)
    draw.text((SIZE // 2, wy + 40), "PLUS: Weekly Reflection & Growth", fill=WHITE, font=get_font(56, bold=True), anchor="mt")
    draw.text((SIZE // 2, wy + 120), "Deep reflection prompts for wins, challenges & self-care", fill=(220, 240, 240), font=get_font(38), anchor="mt")
    draw.text((SIZE // 2, wy + 180), "Track your personal growth journey all year long", fill=(200, 225, 225), font=get_font(34), anchor="mt")

    # Bottom
    draw.rectangle([0, SIZE - 80, SIZE, SIZE], fill=DEEP_TEAL)
    draw.text((SIZE // 2, SIZE - 55), "Journaling prompts designed by wellness experts", fill=WHITE, font=get_font(36), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "08_guided_journal.png"), quality=95)
    print("Created: 08_guided_journal.png")


# ──────────────────────────────────────────────────────────
# IMAGE 9: COMPATIBILITY / WHAT'S INCLUDED
# ──────────────────────────────────────────────────────────

def create_image_09_compatibility():
    img = Image.new('RGB', (SIZE, SIZE), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, SIZE, 300], fill=DEEP_TEAL)
    draw.text((SIZE // 2, 70), "Works With Your", fill=PATINA_BLUE, font=get_font(60), anchor="mt")
    draw.text((SIZE // 2, 160), "Favorite Apps", fill=WHITE, font=get_font(90, bold=True), anchor="mt")

    # App compatibility cards
    apps = [
        ("GoodNotes", "iPad & Mac"),
        ("Notability", "iPad & Mac"),
        ("Xodo", "Android & Windows"),
        ("Noteshelf", "iPad"),
        ("Zinnia", "iPad"),
        ("PDF Expert", "All devices"),
    ]

    card_w = 680
    card_h = 250
    gap = 40
    cols = 3
    total_w = cols * card_w + (cols - 1) * gap
    start_x = (SIZE - total_w) // 2
    app_colors = [PATINA_BLUE, DEEP_TEAL, SOFT_SAGE, DUSTY_ROSE, PATINA_BLUE, DEEP_TEAL]

    for i, (app_name, device) in enumerate(apps):
        col = i % 3
        row = i // 3
        x = start_x + col * (card_w + gap)
        y = 400 + row * (card_h + gap)

        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=20, fill=WARM_LINEN, outline=app_colors[i], width=3)
        draw.text((x + card_w // 2, y + 50), app_name, fill=app_colors[i], font=get_font(52, bold=True), anchor="mt")
        draw.text((x + card_w // 2, y + 130), device, fill=CHARCOAL, font=get_font(36), anchor="mt")

        # Checkmark
        draw.ellipse([x + card_w - 70, y + 15, x + card_w - 20, y + 65], fill=app_colors[i])
        draw.text((x + card_w - 48, y + 18), "Y", fill=WHITE, font=get_font(30, bold=True), anchor="mt")

    # What's included section
    wy = 1050
    draw.rectangle([0, wy, SIZE, SIZE], fill=WARM_LINEN)
    draw.text((SIZE // 2, wy + 40), "What's Included", fill=DEEP_TEAL, font=get_font(70, bold=True), anchor="mt")

    includes = [
        "28-page hyperlinked PDF planner",
        "12 monthly calendar spreads",
        "4 weekly planner templates",
        "3 daily planner layouts",
        "Goal setting & life wheel assessment",
        "Monthly habit tracker (31 days)",
        "Wellness dashboard (sleep, meals, fitness)",
        "Guided morning & evening journal",
        "Self-care checklist & mood tracker",
        "3 lined notes pages",
    ]

    col_items = 5
    col_w = 1000
    for i, item in enumerate(includes):
        col = i // col_items
        row = i % col_items
        ix = 200 + col * col_w
        iy = wy + 150 + row * 70

        # Checkmark circle
        draw.ellipse([ix, iy, ix + 40, iy + 40], fill=PATINA_BLUE)
        draw.text((ix + 20, iy + 5), "Y", fill=WHITE, font=get_font(22, bold=True), anchor="mt")
        draw.text((ix + 55, iy + 5), item, fill=CHARCOAL, font=get_font(34))

    # Bottom
    draw.rectangle([0, SIZE - 100, SIZE, SIZE], fill=DEEP_TEAL)
    draw.text((SIZE // 2, SIZE - 70), "Instant download | No shipping | Start planning today", fill=WHITE, font=get_font(40), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "09_compatibility.png"), quality=95)
    print("Created: 09_compatibility.png")


# ──────────────────────────────────────────────────────────
# IMAGE 10: SOCIAL PROOF / CTA
# ──────────────────────────────────────────────────────────

def create_image_10_cta():
    img = Image.new('RGB', (SIZE, SIZE), DEEP_TEAL)
    draw = ImageDraw.Draw(img)

    # Decorative frame
    draw.rectangle([30, 30, SIZE - 30, SIZE - 30], outline=PATINA_BLUE, width=4)
    draw.rectangle([60, 60, SIZE - 60, SIZE - 60], outline=(80, 130, 135), width=2)

    # Inner content area
    draw.rounded_rectangle([100, 100, SIZE - 100, SIZE - 100], radius=30, fill=WARM_LINEN)

    # Triple accent bar
    draw.rectangle([100, 100, SIZE - 100, 112], fill=PATINA_BLUE)
    draw.rectangle([100, 112, SIZE - 100, 120], fill=DUSTY_ROSE)
    draw.rectangle([100, 120, SIZE - 100, 126], fill=SOFT_SAGE)

    # Star rating
    stars = "* * * * *"
    draw.text((SIZE // 2, 200), stars, fill=DUSTY_ROSE, font=get_font(80), anchor="mt")

    # Testimonial style
    draw.text((SIZE // 2, 340), '"This planner changed how', fill=DEEP_TEAL, font=get_font(56), anchor="mt")
    draw.text((SIZE // 2, 410), 'I approach my entire day.', fill=DEEP_TEAL, font=get_font(56), anchor="mt")
    draw.text((SIZE // 2, 480), 'The wellness features are', fill=DEEP_TEAL, font=get_font(56), anchor="mt")
    draw.text((SIZE // 2, 550), 'exactly what I needed."', fill=DEEP_TEAL, font=get_font(56), anchor="mt")

    # Divider
    draw.rectangle([SIZE // 2 - 200, 640, SIZE // 2 + 200, 643], fill=PATINA_BLUE)

    # Key selling points
    points = [
        "Instant Download - Start Planning Today",
        "Works on iPad, Android & Windows Tablets",
        "Fully Hyperlinked Navigation",
        "Designed for GoodNotes, Notability & More",
        "28 Beautifully Designed Pages",
        "Wellness + Productivity in One Place",
    ]

    for i, point in enumerate(points):
        py = 720 + i * 80
        draw.ellipse([SIZE // 2 - 500, py, SIZE // 2 - 470, py + 30], fill=PATINA_BLUE)
        draw.text((SIZE // 2 - 450, py - 2), point, fill=CHARCOAL, font=get_font(38))

    # CTA section
    cta_y = 1250
    draw.rounded_rectangle([300, cta_y, SIZE - 300, cta_y + 200], radius=30, fill=DEEP_TEAL)
    draw.text((SIZE // 2, cta_y + 30), "2026 Wellness & Productivity", fill=PATINA_BLUE, font=get_font(48), anchor="mt")
    draw.text((SIZE // 2, cta_y + 100), "DIGITAL PLANNER", fill=WHITE, font=get_font(72, bold=True), anchor="mt")

    # Price callout
    draw.rounded_rectangle([SIZE // 2 - 250, cta_y + 240, SIZE // 2 + 250, cta_y + 360], radius=25, fill=DUSTY_ROSE)
    draw.text((SIZE // 2, cta_y + 260), "Add to Cart", fill=WHITE, font=get_font(56, bold=True), anchor="mt")

    # Mini feature badges at bottom
    badges = ["Instant Download", "No Shipping", "PDF Format", "Lifetime Access"]
    badge_w = 400
    total = len(badges) * badge_w + (len(badges) - 1) * 30
    bx = (SIZE - total) // 2
    by = cta_y + 420
    for badge in badges:
        draw.rounded_rectangle([bx, by, bx + badge_w, by + 60], radius=15, fill=SOFT_SAGE)
        draw.text((bx + badge_w // 2, by + 12), badge, fill=WHITE, font=get_font(28, bold=True), anchor="mt")
        bx += badge_w + 30

    # Bottom accent
    draw.rectangle([100, SIZE - 126, SIZE - 100, SIZE - 120], fill=SOFT_SAGE)
    draw.rectangle([100, SIZE - 120, SIZE - 100, SIZE - 112], fill=DUSTY_ROSE)
    draw.rectangle([100, SIZE - 112, SIZE - 100, SIZE - 100], fill=PATINA_BLUE)

    img.save(os.path.join(OUTPUT_DIR, "10_social_proof_cta.png"), quality=95)
    print("Created: 10_social_proof_cta.png")


# ──────────────────────────────────────────────────────────
# IMAGE 5B: WEEKLY PLANNER PREVIEW (replacing generic wellness)
# ──────────────────────────────────────────────────────────

def create_image_05b_weekly():
    """Additional weekly spread preview as image 5."""
    img = Image.new('RGB', (SIZE, SIZE), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    draw_accent_bars(draw, 0, SIZE)

    draw.text((SIZE // 2, 100), "Weekly Planner Spread", fill=DEEP_TEAL, font=get_font(80, bold=True), anchor="mt")
    draw.text((SIZE // 2, 210), "Plan your week with built-in wellness check-ins", fill=CHARCOAL, font=get_font(42), anchor="mt")

    # iPad mockup
    ipad_w, ipad_h = 2000, 1400
    ipad_x = (SIZE - ipad_w) // 2
    ipad_y = 340
    screen = draw_ipad_mockup(draw, ipad_x, ipad_y, ipad_w, ipad_h)
    sx, sy, ex, ey = screen
    sw, sh = ex - sx, ey - sy

    draw.rectangle([sx, sy, ex, ey], fill=WARM_LINEN)

    # Sidebar
    tab_w = int(sw * 0.06)
    for i in range(10):
        ty = sy + 5 + i * (sh // 11)
        color = PATINA_BLUE if i == 3 else DEEP_TEAL
        draw.rectangle([sx, ty, sx + tab_w, ty + sh // 12], fill=color)

    cx = sx + tab_w + 20
    draw.text((cx, sy + 10), "Weekly Planner - Week 1", fill=DEEP_TEAL, font=get_font(40, bold=True))

    # 7 day cards
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    card_w_inner = (sw - tab_w - 50) // 2 - 10
    for d, day in enumerate(days):
        if d < 4:
            dx = cx
            dy = sy + 60 + d * (sh // 5)
        else:
            dx = cx + card_w_inner + 20
            dy = sy + 60 + (d - 4) * (sh // 5)

        day_h = sh // 5 - 10
        draw.rounded_rectangle([dx, dy, dx + card_w_inner, dy + day_h], radius=8, fill=WHITE, outline=LIGHT_GRAY, width=1)
        draw.text((dx + 10, dy + 5), day, fill=PATINA_BLUE, font=get_font(22, bold=True))

        # Checkboxes
        for ci in range(3):
            cy_box = dy + 30 + ci * 25
            if cy_box < dy + day_h - 10:
                draw.rectangle([dx + 10, cy_box, dx + 22, cy_box + 12], outline=LIGHT_GRAY, width=1)
                draw.line([(dx + 30, cy_box + 10), (dx + card_w_inner - 10, cy_box + 10)], fill=LIGHT_GRAY, width=1)

    # Wellness check-in card at bottom right
    wcx = cx + card_w_inner + 20
    wcy = sy + 60 + 3 * (sh // 5)
    wch = sh // 5 - 10
    draw.rounded_rectangle([wcx, wcy, wcx + card_w_inner, wcy + wch], radius=8, fill=(245, 238, 235), outline=DUSTY_ROSE, width=2)
    draw.text((wcx + 10, wcy + 5), "Wellness Check-in", fill=DUSTY_ROSE, font=get_font(20, bold=True))

    # Bottom callout
    draw.rounded_rectangle([200, 1830, SIZE - 200, 1980], radius=30, fill=PATINA_BLUE)
    draw.text((SIZE // 2, 1870), "4 weekly spread templates with task lists & priorities", fill=WHITE, font=get_font(40), anchor="mt")

    img.save(os.path.join(OUTPUT_DIR, "05b_weekly_preview.png"), quality=95)
    print("Created: 05b_weekly_preview.png")


if __name__ == "__main__":
    print("Creating 10 Etsy listing images...")
    create_image_01_hero()
    create_image_02_features()
    create_image_03_monthly()
    create_image_04_daily()
    create_image_05_wellness()
    create_image_05b_weekly()
    create_image_06_habits()
    create_image_07_goals()
    create_image_08_journal()
    create_image_09_compatibility()
    create_image_10_cta()
    print("\nAll 10 images created successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
