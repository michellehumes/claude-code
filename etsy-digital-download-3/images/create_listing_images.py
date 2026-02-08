"""
Create professional Etsy listing images for the Wellness & Habit Tracker Bundle.
5 images at 2700x2025 (Etsy recommended).
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = "/home/user/claude-code/etsy-digital-download-3/images"
W, H = 2700, 2025

# ── Colors (Calming wellness palette) ──
PLUM = (91, 44, 111)
DUSTY_ROSE = (199, 125, 152)
SOFT_PINK = (242, 215, 213)
LAVENDER = (215, 189, 226)
PALE_LILAC = (240, 230, 246)
WHITE = (255, 255, 255)
LIGHT_GRAY = (245, 245, 245)
DARK_TEXT = (44, 44, 44)
SAGE = (130, 168, 140)
WARM_BEIGE = (245, 230, 211)
DUSTY_TEAL = (107, 159, 158)
SOFT_GOLD = (212, 168, 83)
CORAL_SOFT = (232, 165, 152)
CREAM = (255, 252, 248)

def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill_color, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill_color, outline=outline, width=width)

def draw_centered_text(draw, text, y, font, color, width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)

def draw_text_at(draw, text, x, y, font, color):
    draw.text((x, y), text, font=font, fill=color)


# ═══════════════════════════════════════════════════
#  IMAGE 1: HERO
# ═══════════════════════════════════════════════════
def create_hero_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top banner
    draw.rectangle([(0, 0), (W, 175)], fill=PLUM)
    font_sm = get_font(40)
    draw_centered_text(draw, "INSTANT DOWNLOAD  |  GOOGLE SHEETS & EXCEL COMPATIBLE", 68, font_sm, LAVENDER)

    # Main content card
    draw_rounded_rect(draw, (120, 230, W-120, H-180), 30, WHITE, outline=DUSTY_ROSE, width=3)

    # Inner accent bar
    draw.rectangle([(120, 230), (W-120, 310)], fill=DUSTY_ROSE)
    font_badge = get_font(34, bold=True)
    draw_centered_text(draw, "ALL-IN-ONE WELLNESS SPREADSHEET  |  9 TABS  |  READY TO USE", 250, font_badge, WHITE)

    # Main title
    font_title = get_font(100, bold=True)
    draw_centered_text(draw, "WELLNESS &", 360, font_title, PLUM)
    draw_centered_text(draw, "HABIT TRACKER", 480, font_title, PLUM)
    draw_centered_text(draw, "BUNDLE", 600, font_title, PLUM)

    # Year badge
    font_year = get_font(68, bold=True)
    draw_rounded_rect(draw, (W//2 - 125, 740, W//2 + 125, 825), 15, SAGE)
    draw_centered_text(draw, "2026", 748, font_year, WHITE)

    # Features - 3 columns
    font_feat = get_font(38, bold=True)
    features = [
        "Daily Habit Tracker",
        "Mood & Mental Health",
        "Fitness & Workout Log",
        "Meal Planner & Grocery",
        "Water & Sleep Tracker",
        "Gratitude Journal",
        "Self-Care Checklist",
        "Goals & Monthly Review",
        "How-to-Use Guide",
    ]

    y_start = 880
    cols = [240, W//2 - 60, W - 720]

    for idx, feat in enumerate(features):
        col_x = cols[idx // 3]
        y = y_start + (idx % 3) * 72
        cx = col_x - 40
        draw.ellipse([(cx-15, y+12), (cx+15, y+42)], fill=DUSTY_ROSE)
        draw_text_at(draw, feat, col_x, y + 8, font_feat, DARK_TEXT)

    # Divider
    draw.line([(200, 1130), (W-200, 1130)], fill=LAVENDER, width=3)

    # Value prop
    font_value = get_font(44, bold=True)
    draw_centered_text(draw, "Build Healthy Habits. Track Your Progress. Transform Your Life.", 1170, font_value, PLUM)

    font_sub = get_font(34)
    draw_centered_text(draw, "Pre-built formulas. Drop-down menus. 40+ self-care activities. 15 starter habits. 12 affirmations.", 1240, font_sub, DARK_TEXT)

    # Ideal for
    font_ideal = get_font(32, bold=True)
    draw_centered_text(draw, "PERFECT FOR:  Self-Improvement  |  New Year Goals  |  Mental Health  |  Fitness Journey  |  Daily Mindfulness", 1340, font_ideal, DUSTY_ROSE)

    # Bottom CTA
    draw.rectangle([(0, H-155), (W, H)], fill=PLUM)
    font_cta = get_font(46, bold=True)
    draw_centered_text(draw, "DIGITAL DOWNLOAD  -  YOUR WELLNESS JOURNEY STARTS NOW", H-125, font_cta, LAVENDER)

    img.save(os.path.join(OUT_DIR, "01_hero_main_listing.png"), quality=95)
    print("Created: 01_hero_main_listing.png")


# ═══════════════════════════════════════════════════
#  IMAGE 2: WHAT'S INCLUDED
# ═══════════════════════════════════════════════════
def create_features_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 195)], fill=PLUM)
    font_title = get_font(68, bold=True)
    draw_centered_text(draw, "WHAT'S INCLUDED", 52, font_title, WHITE)
    font_sub = get_font(36)
    draw_centered_text(draw, "9 Wellness Tabs  |  All Formulas & Drop-Downs Built In", 145, font_sub, LAVENDER)

    features = [
        ("HABIT TRACKER", "30-day grid for 20 habits.\nAuto completion % per habit.\nDaily consistency score.", DUSTY_ROSE),
        ("MOOD TRACKER", "Daily mood, energy & anxiety.\nSleep quality logging.\n7 monthly reflection prompts.", PLUM),
        ("FITNESS LOG", "50-row workout tracker.\nType, duration, intensity.\nMonthly summary with totals.", SAGE),
        ("MEAL PLANNER", "7-day meal plan grid.\n30-row grocery list.\nCategory dropdowns & cost.", CORAL_SOFT),
        ("WATER & SLEEP", "Daily water intake vs goal.\nBedtime & wake tracking.\nAuto hours-slept calculation.", DUSTY_TEAL),
        ("GRATITUDE JOURNAL", "Daily gratitude + affirmation.\nBest-of-day & lessons learned.\n12 affirmation ideas included.", SOFT_GOLD),
        ("SELF-CARE CHECKLIST", "40 activities in 5 categories.\nWeekly check-off system.\nPhysical, mental, emotional+.", DUSTY_ROSE),
        ("GOALS & REVIEW", "8 monthly wellness goals.\nEnd-of-month review prompts.\n12-month annual overview.", SAGE),
    ]

    card_w = 1140
    card_h = 300
    gap_x = 100
    gap_y = 32
    start_x = (W - 2 * card_w - gap_x) // 2
    start_y = 240

    font_card_title = get_font(40, bold=True)
    font_card_body = get_font(28)
    font_num = get_font(26, bold=True)

    for idx, (title, body, accent) in enumerate(features):
        col = idx % 2
        row = idx // 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 18, WHITE, outline=accent, width=3)
        draw_rounded_rect(draw, (x, y, x + 10, y + card_h), 5, accent)

        bx, by = x + 35, y + 18
        draw.ellipse([(bx, by), (bx + 52, by + 52)], fill=accent)
        nt = str(idx + 1)
        bbox = draw.textbbox((0, 0), nt, font=font_num)
        nw = bbox[2] - bbox[0]
        draw.text((bx + (52 - nw) // 2, by + 9), nt, font=font_num, fill=WHITE)

        draw.text((x + 105, y + 25), title, font=font_card_title, fill=PLUM)
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw.text((x + 105, y + 85 + li * 50), f"  {line}", font=font_card_body, fill=DARK_TEXT)

    # Bonus bar
    bonus_y = start_y + 4 * (card_h + gap_y) + 5
    draw_rounded_rect(draw, (start_x, bonus_y, W - start_x, bonus_y + 65), 15, PALE_LILAC)
    font_bonus = get_font(32, bold=True)
    draw_centered_text(draw, "BONUS: Tab 9 — Complete How-to-Use Guide + Gentle Reminders for Your Journey", bonus_y + 15, font_bonus, PLUM)

    draw.rectangle([(0, H - 85), (W, H)], fill=PLUM)
    font_btm = get_font(32, bold=True)
    draw_centered_text(draw, "WORKS WITH GOOGLE SHEETS  |  MICROSOFT EXCEL  |  LIBREOFFICE", H - 65, font_btm, LAVENDER)

    img.save(os.path.join(OUT_DIR, "02_whats_included.png"), quality=95)
    print("Created: 02_whats_included.png")


# ═══════════════════════════════════════════════════
#  IMAGE 3: HABIT TRACKER & MOOD PREVIEW
# ═══════════════════════════════════════════════════
def create_tracker_mockup():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 135)], fill=PLUM)
    font_title = get_font(52, bold=True)
    draw_centered_text(draw, "HABIT TRACKER & MOOD TRACKER PREVIEW", 35, font_title, WHITE)

    # Screen frame
    sx, sy = 100, 180
    sw, sh = W - 200, H - 310

    draw_rounded_rect(draw, (sx, sy, sx + sw, sy + 52), 12, (55, 55, 55))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([(sx + 16 + i*30, sy + 14), (sx + 38 + i*30, sy + 36)], fill=c)

    ss_y = sy + 52
    draw.rectangle([(sx, ss_y), (sx + sw, sy + sh)], fill=WHITE)

    # Tab bar
    tab_y = sy + sh - 42
    tabs = ["Habit Tracker", "Mood", "Fitness", "Meals", "Water/Sleep", "Gratitude", "Self-Care", "Goals"]
    tab_x = sx + 8
    font_tab = get_font(18)
    for i, tab in enumerate(tabs):
        tw = len(tab) * 11 + 22
        tc = DUSTY_ROSE if i == 0 else LIGHT_GRAY
        txt_c = WHITE if i == 0 else DARK_TEXT
        draw_rounded_rect(draw, (tab_x, tab_y, tab_x + tw, tab_y + 38), 7, tc)
        draw.text((tab_x + 11, tab_y + 9), tab, font=font_tab, fill=txt_c)
        tab_x += tw + 5

    # Title row
    draw.rectangle([(sx + 10, ss_y + 8), (sx + sw - 10, ss_y + 55)], fill=PALE_LILAC)
    font_ss_title = get_font(30, bold=True)
    draw.text((sx + 350, ss_y + 15), "DAILY HABIT TRACKER", font=font_ss_title, fill=PLUM)

    # Habit grid header
    grid_y = ss_y + 70
    font_th = get_font(20, bold=True)
    font_td = get_font(18)

    # Column: Habit | 1-15 | Total | %
    draw.rectangle([(sx + 15, grid_y), (sx + 300, grid_y + 38)], fill=PLUM)
    draw.text((sx + 25, grid_y + 8), "Habit", font=font_th, fill=WHITE)

    for d in range(1, 16):
        dx = sx + 300 + (d - 1) * 55
        draw.rectangle([(dx, grid_y), (dx + 55, grid_y + 38)], fill=PLUM)
        draw.text((dx + 18, grid_y + 8), str(d), font=font_th, fill=WHITE)

    draw.rectangle([(sx + 300 + 15*55, grid_y), (sx + 300 + 15*55 + 65, grid_y + 38)], fill=PLUM)
    draw.text((sx + 300 + 15*55 + 8, grid_y + 8), "Total", font=font_th, fill=WHITE)

    draw.rectangle([(sx + 300 + 15*55 + 65, grid_y), (sx + 300 + 15*55 + 130, grid_y + 38)], fill=PLUM)
    draw.text((sx + 300 + 15*55 + 85, grid_y + 8), "%", font=font_th, fill=WHITE)

    # Sample habit rows
    habits_data = [
        ("Drink 8 glasses water", ["✓","✓","✓","✓","✓","✓","✓","✓","X","✓","✓","✓","✓","✓","✓"], "13", "87%"),
        ("Exercise 30+ min", ["✓","X","✓","✓","X","✓","X","✓","✓","✓","X","✓","✓","X","✓"], "10", "67%"),
        ("Meditate", ["✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓"], "15", "100%"),
        ("Read 20+ min", ["✓","✓","X","✓","✓","✓","X","✓","✓","X","✓","✓","✓","✓","✓"], "12", "80%"),
        ("Healthy meal prep", ["✓","✓","✓","X","✓","✓","✓","X","✓","✓","✓","✓","X","✓","✓"], "12", "80%"),
        ("8 hours sleep", ["X","✓","✓","✓","X","✓","✓","✓","✓","✓","X","✓","✓","✓","✓"], "12", "80%"),
        ("Gratitude journal", ["✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓","✓"], "15", "100%"),
        ("No phone before 9am", ["X","X","✓","✓","X","✓","X","✓","✓","X","✓","✓","X","✓","✓"], "9", "60%"),
    ]

    for hi, (habit, checks, total, pct) in enumerate(habits_data):
        ry = grid_y + 38 + hi * 38
        bg = LIGHT_GRAY if hi % 2 == 1 else WHITE
        draw.rectangle([(sx + 15, ry), (sx + 300, ry + 38)], fill=bg, outline=(220, 220, 220))
        draw.text((sx + 25, ry + 9), habit, font=font_td, fill=DARK_TEXT)

        for di, check in enumerate(checks):
            dx = sx + 300 + di * 55
            draw.rectangle([(dx, ry), (dx + 55, ry + 38)], fill=bg, outline=(220, 220, 220))
            color = SAGE if check == "✓" else CORAL_SOFT
            draw.text((dx + 18, ry + 8), check, font=font_td, fill=color)

        # Total & %
        tot_x = sx + 300 + 15 * 55
        draw.rectangle([(tot_x, ry), (tot_x + 65, ry + 38)], fill=bg, outline=(220, 220, 220))
        draw.text((tot_x + 20, ry + 8), total, font=get_font(18, bold=True), fill=PLUM)
        draw.rectangle([(tot_x + 65, ry), (tot_x + 130, ry + 38)], fill=bg, outline=(220, 220, 220))
        draw.text((tot_x + 78, ry + 8), pct, font=get_font(18, bold=True), fill=PLUM)

    # Mood tracker section on the right bottom
    mood_x = sx + sw // 2 + 30
    mood_y = grid_y + 38 + len(habits_data) * 38 + 30
    mood_w = sw // 2 - 50
    mood_h = 340

    draw_rounded_rect(draw, (mood_x, mood_y, mood_x + mood_w, mood_y + mood_h), 15, WHITE, outline=DUSTY_ROSE, width=2)
    draw.rectangle([(mood_x, mood_y), (mood_x + mood_w, mood_y + 42)], fill=DUSTY_ROSE)
    draw.text((mood_x + 250, mood_y + 8), "MOOD TRACKER", font=get_font(24, bold=True), fill=WHITE)

    mood_entries = [
        ("Jan 1", "Great", "High", "1-Calm", "Excellent"),
        ("Jan 2", "Good", "Medium", "2-Mild", "Good"),
        ("Jan 3", "Okay", "Low", "3-Moderate", "Fair"),
        ("Jan 4", "Good", "High", "1-Calm", "Good"),
        ("Jan 5", "Great", "High", "1-Calm", "Excellent"),
    ]

    font_mood = get_font(18)
    font_mood_h = get_font(18, bold=True)

    # Mini headers
    mh_y = mood_y + 52
    m_headers = ["Date", "Mood", "Energy", "Anxiety", "Sleep"]
    m_widths = [100, 100, 110, 120, 120]
    mx = mood_x + 15
    for mh, mw in zip(m_headers, m_widths):
        draw.text((mx, mh_y), mh, font=font_mood_h, fill=PLUM)
        mx += mw

    for mi, (date, mood, energy, anxiety, sleep) in enumerate(mood_entries):
        my = mh_y + 30 + mi * 45
        mx = mood_x + 15
        for val, mw in zip([date, mood, energy, anxiety, sleep], m_widths):
            draw.text((mx, my), val, font=font_mood, fill=DARK_TEXT)
            mx += mw

    # Monthly reflection preview (left bottom)
    ref_x = sx + 15
    ref_y = mood_y
    ref_w = sw // 2 - 30
    ref_h = mood_h

    draw_rounded_rect(draw, (ref_x, ref_y, ref_x + ref_w, ref_y + ref_h), 15, WHITE, outline=SAGE, width=2)
    draw.rectangle([(ref_x, ref_y), (ref_x + ref_w, ref_y + 42)], fill=SAGE)
    draw.text((ref_x + 180, ref_y + 8), "MONTHLY REFLECTION", font=get_font(24, bold=True), fill=WHITE)

    reflections = [
        "What patterns did I notice?",
        "What lifted my mood the most?",
        "What were my biggest stressors?",
        "What self-care helped most?",
        "I'm proud of myself for...",
    ]
    for ri, ref in enumerate(reflections):
        ry2 = ref_y + 55 + ri * 52
        draw.text((ref_x + 20, ry2), ref, font=get_font(22, bold=True), fill=PLUM)
        draw.line([(ref_x + 20, ry2 + 32), (ref_x + ref_w - 20, ry2 + 32)], fill=LAVENDER, width=1)

    # Bottom
    draw.rectangle([(0, H - 95), (W, H)], fill=PLUM)
    font_btm = get_font(34, bold=True)
    draw_centered_text(draw, "PRE-LOADED HABITS  |  DROP-DOWN MENUS  |  AUTO-CALCULATING STATS", H - 72, font_btm, LAVENDER)

    img.save(os.path.join(OUT_DIR, "03_tracker_preview.png"), quality=95)
    print("Created: 03_tracker_preview.png")


# ═══════════════════════════════════════════════════
#  IMAGE 4: SELF-CARE, GRATITUDE & MEAL PLANNER
# ═══════════════════════════════════════════════════
def create_selfcare_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 135)], fill=PLUM)
    font_title = get_font(50, bold=True)
    draw_centered_text(draw, "SELF-CARE, GRATITUDE & MEAL PLANNING", 38, font_title, WHITE)

    # Three panels
    panel_w = (W - 160) // 3
    gap = 30

    # Panel 1: Self-Care Checklist
    px = 50
    py = 190
    ph = H - 340

    draw_rounded_rect(draw, (px, py, px + panel_w, py + ph), 18, WHITE, outline=DUSTY_ROSE, width=3)
    draw.rectangle([(px, py), (px + panel_w, py + 70)], fill=DUSTY_ROSE)
    font_panel = get_font(32, bold=True)
    draw.text((px + 80, py + 16), "SELF-CARE CHECKLIST", font=font_panel, fill=WHITE)

    categories_data = [
        ("PHYSICAL", ["Take a long bath", "Go for a walk", "Stretch or yoga", "Full night's sleep"], SAGE),
        ("MENTAL", ["Read for pleasure", "Learn something new", "Journal writing", "Social media break"], PLUM),
        ("EMOTIONAL", ["Practice gratitude", "Celebrate a small win", "Talk to someone", "Set a boundary"], DUSTY_TEAL),
    ]

    font_cat = get_font(22, bold=True)
    font_item = get_font(19)
    cy = py + 85

    for cat_name, items, color in categories_data:
        draw_rounded_rect(draw, (px + 15, cy, px + panel_w - 15, cy + 30), 8, color)
        draw.text((px + 25, cy + 4), cat_name, font=get_font(18, bold=True), fill=WHITE)
        cy += 40
        for item in items:
            # Checkbox
            draw.rounded_rectangle([(px + 25, cy + 2), (px + 45, cy + 22)], radius=4, outline=DUSTY_ROSE, width=2)
            draw.text((px + 55, cy), item, font=font_item, fill=DARK_TEXT)
            cy += 32
        cy += 15

    # "40 activities in 5 categories" label
    draw_rounded_rect(draw, (px + 15, cy + 10, px + panel_w - 15, cy + 60), 10, PALE_LILAC)
    draw.text((px + 35, cy + 22), "40 activities across 5 categories!", font=get_font(20, bold=True), fill=PLUM)

    # Panel 2: Gratitude Journal
    px2 = px + panel_w + gap
    draw_rounded_rect(draw, (px2, py, px2 + panel_w, py + ph), 18, WHITE, outline=SOFT_GOLD, width=3)
    draw.rectangle([(px2, py), (px2 + panel_w, py + 70)], fill=SOFT_GOLD)
    draw.text((px2 + 90, py + 16), "GRATITUDE JOURNAL", font=font_panel, fill=WHITE)

    entries = [
        ("Jan 1", ["My warm morning coffee", "A kind text from Mom", "Beautiful sunset walk"], "I am worthy of joy", "Grateful"),
        ("Jan 2", ["Finished a great book", "Lunchtime with a friend", "My cozy home"], "I choose progress", "Happy"),
        ("Jan 3", ["A productive morning", "Dog park with Bella", "Homemade dinner"], "I am enough", "Peaceful"),
    ]

    gy = py + 85
    font_date = get_font(22, bold=True)
    font_grat = get_font(18)

    for date, gratitudes, affirmation, mood in entries:
        draw_text_at(draw, date, px2 + 20, gy, font_date, PLUM)

        # Mood badge
        mood_colors = {"Grateful": SAGE, "Happy": SOFT_GOLD, "Peaceful": DUSTY_TEAL}
        mc = mood_colors.get(mood, DUSTY_ROSE)
        mbbox = draw.textbbox((0, 0), mood, font=font_grat)
        mw = mbbox[2] - mbbox[0]
        draw_rounded_rect(draw, (px2 + panel_w - mw - 45, gy + 2, px2 + panel_w - 20, gy + 26), 8, mc)
        draw.text((px2 + panel_w - mw - 32, gy + 4), mood, font=font_grat, fill=WHITE)

        gy += 30
        draw_text_at(draw, "Grateful for:", px2 + 20, gy, get_font(16, bold=True), DUSTY_ROSE)
        gy += 22
        for g in gratitudes:
            draw_text_at(draw, f"  - {g}", px2 + 20, gy, font_grat, DARK_TEXT)
            gy += 24
        draw_text_at(draw, f'Affirmation: "{affirmation}"', px2 + 20, gy + 5, get_font(17, True), PLUM)
        gy += 42

    # Affirmation bank preview
    aff_y = gy + 20
    draw_rounded_rect(draw, (px2 + 15, aff_y, px2 + panel_w - 15, aff_y + 280), 12, PALE_LILAC)
    draw_text_at(draw, "12 AFFIRMATIONS INCLUDED:", px2 + 30, aff_y + 12, get_font(20, bold=True), PLUM)

    sample_affs = [
        '"I am worthy of love and success"',
        '"I choose progress over perfection"',
        '"I am resilient and capable"',
        '"My potential is limitless"',
        '"I release what I cannot control"',
        '"Today I choose joy and peace"',
    ]
    for ai, aff in enumerate(sample_affs):
        draw_text_at(draw, aff, px2 + 30, aff_y + 45 + ai * 36, get_font(17), PLUM)

    # Panel 3: Meal Planner
    px3 = px2 + panel_w + gap
    draw_rounded_rect(draw, (px3, py, px3 + panel_w, py + ph), 18, WHITE, outline=CORAL_SOFT, width=3)
    draw.rectangle([(px3, py), (px3 + panel_w, py + 70)], fill=CORAL_SOFT)
    draw.text((px3 + 130, py + 16), "MEAL PLANNER", font=font_panel, fill=WHITE)

    # Mini meal grid
    my = py + 85
    days_meals = [
        ("MON", "Oatmeal & berries", "Grilled chicken salad", "Salmon & veggies"),
        ("TUE", "Smoothie bowl", "Turkey wrap", "Stir fry & rice"),
        ("WED", "Avocado toast", "Soup & bread", "Pasta primavera"),
        ("THU", "Yogurt parfait", "Grain bowl", "Tacos"),
    ]

    draw.text((px3 + 20, my), "Day", font=get_font(18, bold=True), fill=PLUM)
    draw.text((px3 + 90, my), "Breakfast", font=get_font(18, bold=True), fill=PLUM)
    draw.text((px3 + 310, my), "Lunch", font=get_font(18, bold=True), fill=PLUM)
    draw.text((px3 + 520, my), "Dinner", font=get_font(18, bold=True), fill=PLUM)
    my += 30

    for day, br, lu, di in days_meals:
        bg = LIGHT_GRAY if days_meals.index((day, br, lu, di)) % 2 == 0 else WHITE
        draw.rectangle([(px3 + 15, my), (px3 + panel_w - 15, my + 35)], fill=bg)
        draw.text((px3 + 20, my + 8), day, font=get_font(18, bold=True), fill=DUSTY_ROSE)
        draw.text((px3 + 90, my + 8), br, font=font_grat, fill=DARK_TEXT)
        draw.text((px3 + 310, my + 8), lu, font=font_grat, fill=DARK_TEXT)
        draw.text((px3 + 520, my + 8), di, font=font_grat, fill=DARK_TEXT)
        my += 40

    # Grocery list preview
    my += 20
    draw_rounded_rect(draw, (px3 + 15, my, px3 + panel_w - 15, my + 390), 12, PALE_LILAC)
    draw_text_at(draw, "GROCERY LIST", px3 + 30, my + 12, get_font(22, bold=True), PLUM)

    groceries = [
        ("Produce", ["Avocados (3)", "Berries (2 pints)", "Spinach bag", "Sweet potatoes"]),
        ("Protein", ["Chicken breast", "Salmon fillets", "Ground turkey"]),
        ("Pantry", ["Oats", "Rice", "Pasta", "Olive oil"]),
    ]

    gy2 = my + 45
    for cat, items in groceries:
        draw_text_at(draw, cat, px3 + 30, gy2, get_font(18, bold=True), CORAL_SOFT)
        gy2 += 25
        for item in items:
            draw_text_at(draw, f"  [ ] {item}", px3 + 30, gy2, font_grat, DARK_TEXT)
            gy2 += 24
        gy2 += 10

    draw_text_at(draw, "Est. Total: $85.50", px3 + 30, gy2 + 5, get_font(20, bold=True), PLUM)

    # Bottom
    draw_rounded_rect(draw, (100, H - 145, W - 100, H - 30), 15, PALE_LILAC)
    font_btm = get_font(30, bold=True)
    draw_centered_text(draw, "40 self-care activities  |  12 affirmation ideas  |  Weekly meal plans + grocery list with cost tracking", H - 105, font_btm, PLUM)

    img.save(os.path.join(OUT_DIR, "04_selfcare_gratitude_meals.png"), quality=95)
    print("Created: 04_selfcare_gratitude_meals.png")


# ═══════════════════════════════════════════════════
#  IMAGE 5: VALUE PROPOSITION
# ═══════════════════════════════════════════════════
def create_value_prop_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 18)], fill=DUSTY_ROSE)

    font_title = get_font(66, bold=True)
    draw_centered_text(draw, "YOUR COMPLETE WELLNESS", 65, font_title, PLUM)
    draw_centered_text(draw, "COMPANION", 148, font_title, PLUM)
    draw.line([(W//2 - 180, 248), (W//2 + 180, 248)], fill=DUSTY_ROSE, width=4)

    # Benefits grid
    benefits = [
        ("BUILD LASTING HABITS", "15 pre-loaded habits with a\n30-day tracking grid. See your\nconsistency grow day by day."),
        ("UNDERSTAND YOURSELF", "Track mood, energy, anxiety\nand sleep. Spot patterns.\nReflect monthly."),
        ("MOVE YOUR BODY", "Log every workout with type,\nduration, and how you felt.\nAuto-totals keep you motivated."),
        ("NOURISH YOUR BODY", "Plan meals for the week.\nOrganized grocery list with\ncost tracking. Eat intentional."),
        ("PRACTICE GRATITUDE", "Daily gratitude prompts +\n12 affirmations. Focus on\nwhat's good in your life."),
        ("PRIORITIZE SELF-CARE", "40 activities across 5 categories.\nPhysical, mental, emotional,\nsocial, and spiritual care."),
    ]

    font_ben_title = get_font(36, bold=True)
    font_ben_body = get_font(26)

    col_w = 760
    row_h = 260
    start_x = (W - 3 * col_w) // 2
    start_y = 300

    accent_colors = [DUSTY_ROSE, PLUM, SAGE, CORAL_SOFT, SOFT_GOLD, DUSTY_TEAL]

    for idx, (title, body) in enumerate(benefits):
        col = idx % 3
        row = idx // 3
        x = start_x + col * col_w + 35
        y = start_y + row * row_h

        ac = accent_colors[idx]
        cx, cy = x + 40, y + 40
        draw.ellipse([(cx-30, cy-30), (cx+30, cy+30)], fill=ac)
        font_check = get_font(32, bold=True)
        draw.text((cx - 12, cy - 18), "✓", font=font_check, fill=WHITE)

        draw_text_at(draw, title, x + 90, y + 12, font_ben_title, PLUM)
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw_text_at(draw, line, x + 90, y + 62 + li * 38, font_ben_body, DARK_TEXT)

    # Stats bar
    stats_y = 870
    draw_rounded_rect(draw, (150, stats_y, W - 150, stats_y + 100), 20, PALE_LILAC, outline=LAVENDER, width=2)
    font_stat = get_font(34, bold=True)
    stats = ["15 Starter Habits", "40 Self-Care Ideas", "12 Affirmations", "7-Day Meal Plans", "31-Day Grids"]
    stat_w = (W - 300) // 5
    for si, stat in enumerate(stats):
        sx2 = 175 + si * stat_w
        bbox = draw.textbbox((0, 0), stat, font=font_stat)
        sw2 = bbox[2] - bbox[0]
        draw.text((sx2 + (stat_w - sw2) // 2, stats_y + 30), stat, font=font_stat, fill=PLUM)

    # Testimonial
    test_y = 1020
    draw_rounded_rect(draw, (200, test_y, W - 200, test_y + 240), 20, SOFT_PINK, outline=DUSTY_ROSE, width=2)
    font_star = get_font(46)
    draw_centered_text(draw, "★ ★ ★ ★ ★", test_y + 18, font_star, SOFT_GOLD)
    font_quote = get_font(30)
    draw_centered_text(draw, '"This tracker helped me actually stick with my habits for the first time.', test_y + 80, font_quote, DARK_TEXT)
    draw_centered_text(draw, 'Seeing the checkmarks fill up is SO motivating. Best purchase I\'ve made."', test_y + 125, font_quote, DARK_TEXT)
    font_attr = get_font(24, bold=True)
    draw_centered_text(draw, "— What wellness tracker users are saying", test_y + 190, font_attr, DUSTY_ROSE)

    # "Perfect for" section
    pf_y = 1310
    draw.line([(200, pf_y), (W - 200, pf_y)], fill=LAVENDER, width=2)

    font_pf_title = get_font(40, bold=True)
    draw_centered_text(draw, "PERFECT FOR", pf_y + 20, font_pf_title, PLUM)

    audiences = [
        "New Year Goal Setters",
        "Self-Improvement Journeys",
        "Mental Health Support",
        "Fitness Beginners",
        "Mindfulness Practice",
        "Wellness Gift Giving",
    ]

    font_aud = get_font(34, bold=True)
    aud_y = pf_y + 80
    col1_x = 250
    col2_x = W // 2 + 100

    for idx, aud in enumerate(audiences):
        col_x = col1_x if idx < 3 else col2_x
        y = aud_y + (idx % 3) * 60
        cx2 = col_x - 40
        draw.ellipse([(cx2-14, y+10), (cx2+14, y+38)], fill=DUSTY_ROSE)
        draw.text((col_x, y + 8), aud, font=font_aud, fill=DARK_TEXT)

    # CTA
    cta_y = 1590
    draw.rectangle([(0, cta_y), (W, H)], fill=PLUM)
    font_cta = get_font(54, bold=True)
    draw_centered_text(draw, "START YOUR WELLNESS JOURNEY TODAY", cta_y + 45, font_cta, WHITE)

    btn_w, btn_h = 650, 80
    btn_x = (W - btn_w) // 2
    btn_y = cta_y + 140
    draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), 40, DUSTY_ROSE)
    font_btn = get_font(36, bold=True)
    draw_centered_text(draw, "INSTANT DIGITAL DOWNLOAD", btn_y + 18, font_btn, WHITE)

    font_sm_cta = get_font(24)
    draw_centered_text(draw, "Buy once, use forever  |  No subscriptions  |  No physical item shipped", cta_y + 265, font_sm_cta, LAVENDER)
    draw_centered_text(draw, "$8.99  |  9 Wellness Tabs  |  Google Sheets + Excel", cta_y + 305, font_sm_cta, SOFT_GOLD)

    draw.rectangle([(0, H - 18), (W, H)], fill=DUSTY_ROSE)

    img.save(os.path.join(OUT_DIR, "05_value_proposition.png"), quality=95)
    print("Created: 05_value_proposition.png")


if __name__ == "__main__":
    create_hero_image()
    create_features_image()
    create_tracker_mockup()
    create_selfcare_image()
    create_value_prop_image()
    print(f"\nAll 5 listing images saved to: {OUT_DIR}")
