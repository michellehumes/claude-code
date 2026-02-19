#!/usr/bin/env python3
"""
Create 10 Etsy listing images for Budget & Finance Spreadsheet Bundle
All images 2400x2400px for Etsy optimal display
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 2400, 2400

# Color palette - Modern sage/money green
DEEP_GREEN = (74, 107, 85)
SAGE_GREEN = (123, 158, 135)
SOFT_MINT = (212, 230, 217)
WARM_CREAM = (253, 248, 240)
CHARCOAL = (61, 61, 61)
WHITE = (255, 255, 255)
CORAL = (232, 145, 122)
GOLD = (212, 168, 83)
LIGHT_GRAY = (245, 245, 245)
MEDIUM_GRAY = (200, 200, 200)
DARK_SAGE = (55, 82, 65)

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.pieslice([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=fill)
    draw.pieslice([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=fill)
    if outline and width:
        draw.arc([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0+radius, y0, x1-radius, y0], fill=outline, width=width)
        draw.line([x0+radius, y1, x1-radius, y1], fill=outline, width=width)
        draw.line([x0, y0+radius, x0, y1-radius], fill=outline, width=width)
        draw.line([x1, y0+radius, x1, y1-radius], fill=outline, width=width)

def draw_spreadsheet_mockup(draw, x, y, w, h, title="Budget", rows=8, cols=5, highlight_color=SAGE_GREEN):
    """Draw a realistic spreadsheet mockup"""
    # Shadow
    draw_rounded_rect(draw, (x+8, y+8, x+w+8, y+h+8), 12, (180, 180, 180, 80))
    # Main window
    draw_rounded_rect(draw, (x, y, x+w, y+h), 12, WHITE, outline=MEDIUM_GRAY, width=2)
    # Title bar
    draw_rounded_rect(draw, (x, y, x+w, y+40), 12, highlight_color)
    draw.rectangle([x, y+24, x+w, y+40], fill=highlight_color)
    # Window dots
    for i, color in enumerate([(255,95,87), (255,189,46), (39,201,63)]):
        draw.ellipse([x+15+i*22, y+12, x+29+i*22, y+26], fill=color)
    # Title text
    font_sm = get_font(18, bold=True)
    draw.text((x+90, y+10), title, fill=WHITE, font=font_sm)
    # Grid
    row_h = (h - 70) // rows
    col_w = w // cols
    # Header row
    draw.rectangle([x+1, y+41, x+w-1, y+41+row_h], fill=(*highlight_color, 60))
    header_font = get_font(14, bold=True)
    headers = ["Category", "Budget", "Actual", "Diff", "%"]
    for c in range(min(cols, len(headers))):
        cx = x + c * col_w + col_w // 2
        draw.text((cx-20, y+48), headers[c], fill=CHARCOAL, font=header_font)
    # Grid lines
    for r in range(rows + 1):
        ry = y + 41 + r * row_h
        draw.line([(x+1, ry), (x+w-1, ry)], fill=MEDIUM_GRAY, width=1)
    for c in range(cols + 1):
        cx = x + c * col_w
        draw.line([(cx, y+41), (cx, y+h-1)], fill=MEDIUM_GRAY, width=1)
    # Some "data" bars in cells
    cell_font = get_font(12)
    sample_data = ["$2,100", "$1,850", "$250", "88%"]
    for r in range(1, min(rows, 6)):
        for c in range(1, min(cols, len(sample_data)+1)):
            cx = x + c * col_w + 8
            cy = y + 41 + r * row_h + row_h // 3
            draw.text((cx, cy), sample_data[c-1], fill=CHARCOAL, font=cell_font)

def draw_dollar_icon(draw, cx, cy, size, color=GOLD):
    draw.ellipse([cx-size, cy-size, cx+size, cy+size], fill=color)
    font = get_font(int(size*1.3), bold=True)
    draw.text((cx-size//3, cy-size//1.5), "$", fill=WHITE, font=font)

def draw_chart_mockup(draw, x, y, w, h, chart_type="bar", color=SAGE_GREEN):
    """Draw a simple chart mockup"""
    draw_rounded_rect(draw, (x, y, x+w, y+h), 8, WHITE, outline=MEDIUM_GRAY, width=1)
    if chart_type == "bar":
        num_bars = 6
        bar_w = w // (num_bars * 2)
        heights = [0.6, 0.8, 0.5, 0.9, 0.7, 0.85]
        for i, ht in enumerate(heights):
            bx = x + 20 + i * (bar_w + bar_w)
            by = y + h - 20 - int((h-50) * ht)
            c = color if i % 2 == 0 else CORAL
            draw.rectangle([bx, by, bx+bar_w, y+h-20], fill=c)
    elif chart_type == "pie":
        cx, cy = x + w//2, y + h//2
        r = min(w, h) // 2 - 20
        colors = [DEEP_GREEN, SAGE_GREEN, CORAL, GOLD, SOFT_MINT]
        angles = [0, 90, 170, 240, 310, 360]
        for i in range(len(angles)-1):
            draw.pieslice([cx-r, cy-r, cx+r, cy+r], angles[i], angles[i+1], fill=colors[i%len(colors)])
    elif chart_type == "line":
        points = []
        num_pts = 8
        for i in range(num_pts):
            px = x + 20 + i * ((w-40) // (num_pts-1))
            py = y + h//2 + int(math.sin(i*0.8) * (h//4)) - 20
            points.append((px, py))
        if len(points) >= 2:
            draw.line(points, fill=color, width=3)
        for px, py in points:
            draw.ellipse([px-4, py-4, px+4, py+4], fill=color)

def draw_checkmark(draw, x, y, size, color=DEEP_GREEN):
    draw.line([(x, y+size//2), (x+size//3, y+size)], fill=color, width=4)
    draw.line([(x+size//3, y+size), (x+size, y)], fill=color, width=4)

# ============================================================
# IMAGE 1: Hero/Cover Image
# ============================================================
def create_image_01():
    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Decorative top bar
    draw.rectangle([0, 0, W, 180], fill=DEEP_GREEN)
    draw.rectangle([0, 180, W, 190], fill=GOLD)

    # Title
    font_title = get_font(92, bold=True)
    font_sub = get_font(48)
    font_year = get_font(140, bold=True)
    font_badge = get_font(36, bold=True)

    draw.text((120, 30), "BUDGET & FINANCE", fill=WHITE, font=font_title)

    # Year badge
    draw_rounded_rect(draw, (150, 230, 550, 360), 20, CORAL)
    draw.text((195, 245), "2026", fill=WHITE, font=font_year)

    # Subtitle
    font_mid = get_font(64, bold=True)
    draw.text((600, 250), "SPREADSHEET", fill=DEEP_GREEN, font=font_mid)
    draw.text((600, 320), "BUNDLE", fill=SAGE_GREEN, font=font_mid)

    # Spreadsheet mockups (stacked, fanned)
    draw_spreadsheet_mockup(draw, 100, 450, 600, 400, "Monthly Budget", 7, 5, DEEP_GREEN)
    draw_spreadsheet_mockup(draw, 350, 520, 600, 400, "Annual Overview", 7, 5, SAGE_GREEN)
    draw_spreadsheet_mockup(draw, 600, 590, 600, 400, "Debt Payoff", 7, 5, CORAL)

    # Right side feature badges
    features = [
        ("6 Spreadsheets", DEEP_GREEN),
        ("Auto-Formulas", SAGE_GREEN),
        ("Instant Download", CORAL),
        ("Excel + Sheets", GOLD),
    ]
    for i, (text, color) in enumerate(features):
        by = 480 + i * 110
        draw_rounded_rect(draw, (1350, by, 2200, by+85), 42, color)
        draw.text((1390, by+18), text, fill=WHITE, font=font_sub)

    # Dollar icons decoration
    for pos in [(1300, 200), (2100, 350), (80, 1100)]:
        draw_dollar_icon(draw, pos[0], pos[1], 40)

    # Bottom section
    draw.rectangle([0, 1700, W, H], fill=DEEP_GREEN)
    draw.rectangle([0, 1690, W, 1700], fill=GOLD)

    # Bottom text
    font_bottom = get_font(52, bold=True)
    font_items = get_font(38)
    draw.text((120, 1750), "INCLUDED IN THIS BUNDLE:", fill=GOLD, font=font_bottom)

    items = [
        "Monthly Budget Tracker  |  Annual Overview  |  Debt Payoff Tracker",
        "Savings Goals  |  Daily Expense Log  |  Bill Payment Calendar"
    ]
    for i, item in enumerate(items):
        draw.text((120, 1840 + i * 60), item, fill=WHITE, font=font_items)

    # Corner accent
    draw.polygon([(W-200, 0), (W, 0), (W, 200)], fill=SAGE_GREEN)
    draw.polygon([(0, H-200), (0, H), (200, H)], fill=SAGE_GREEN)

    # Etsy-style "Digital Download" badge
    draw_rounded_rect(draw, (1600, 1760, 2250, 1840), 15, GOLD)
    draw.text((1630, 1770), "DIGITAL DOWNLOAD", fill=WHITE, font=font_badge)

    # "Best Seller" badge
    draw_rounded_rect(draw, (1600, 1870, 2250, 1950), 15, CORAL)
    draw.text((1640, 1880), "BEST VALUE 2026", fill=WHITE, font=font_badge)

    img.save(os.path.join(OUT_DIR, "01_hero_cover.jpg"), "JPEG", quality=95)
    print("Created: 01_hero_cover.jpg")


# ============================================================
# IMAGE 2: What's Included Overview
# ============================================================
def create_image_02():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 160], fill=DEEP_GREEN)
    font_header = get_font(72, bold=True)
    font_sub = get_font(42)
    font_item = get_font(38, bold=True)
    font_desc = get_font(30)

    draw.text((120, 40), "WHAT'S INCLUDED", fill=WHITE, font=font_header)

    # 6 cards in a 2x3 grid
    cards = [
        ("01", "Monthly Budget\nTracker", "12 monthly tabs with\nincome & expense tracking", DEEP_GREEN),
        ("02", "Annual Budget\nOverview", "Full year at a glance\nwith auto-totals", SAGE_GREEN),
        ("03", "Debt Payoff\nTracker", "Snowball & avalanche\nstrategy comparison", CORAL),
        ("04", "Savings Goal\nTracker", "10 goal slots with\nprogress tracking", GOLD),
        ("05", "Daily Expense\nTracker", "Log every purchase\nby category & method", DEEP_GREEN),
        ("06", "Bill Payment\nCalendar", "Never miss a bill +\nsubscription audit", SAGE_GREEN),
    ]

    card_w, card_h = 1050, 550
    gap_x, gap_y = 100, 80
    start_x, start_y = 100, 240

    for i, (num, title, desc, color) in enumerate(cards):
        col = i % 2
        row = i // 2
        cx = start_x + col * (card_w + gap_x)
        cy = start_y + row * (card_h + gap_y)

        # Card background
        draw_rounded_rect(draw, (cx, cy, cx+card_w, cy+card_h), 20, WARM_CREAM, outline=color, width=4)

        # Number circle
        draw.ellipse([cx+30, cy+30, cx+110, cy+110], fill=color)
        num_font = get_font(44, bold=True)
        draw.text((cx+50, cy+40), num, fill=WHITE, font=num_font)

        # Title
        draw.text((cx+140, cy+35), title, fill=CHARCOAL, font=font_item)

        # Divider line
        draw.line([(cx+30, cy+160), (cx+card_w-30, cy+160)], fill=color, width=3)

        # Description
        draw.text((cx+40, cy+180), desc, fill=(120, 120, 120), font=font_desc)

        # Mini spreadsheet icon
        mini_x, mini_y = cx + 600, cy + 250
        draw_spreadsheet_mockup(draw, mini_x, mini_y, 380, 260, title.split("\n")[0], 5, 4, color)

    # Bottom badge
    draw.rectangle([0, H-120, W, H], fill=DEEP_GREEN)
    badge_font = get_font(44, bold=True)
    draw.text((W//2-400, H-95), "6 SPREADSHEETS  |  INSTANT DOWNLOAD  |  2026", fill=WHITE, font=badge_font)

    img.save(os.path.join(OUT_DIR, "02_whats_included.jpg"), "JPEG", quality=95)
    print("Created: 02_whats_included.jpg")


# ============================================================
# IMAGE 3: Monthly Budget Tracker Detail
# ============================================================
def create_image_03():
    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Title area
    draw_rounded_rect(draw, (80, 60, W-80, 240), 20, DEEP_GREEN)
    font_title = get_font(72, bold=True)
    font_sub = get_font(36)
    draw.text((140, 80), "MONTHLY BUDGET TRACKER", fill=WHITE, font=font_title)
    draw.text((140, 170), "Track income & expenses every month with auto-calculations", fill=SOFT_MINT, font=font_sub)

    # Large spreadsheet mockup
    draw_spreadsheet_mockup(draw, 100, 300, 1400, 900, "January 2026 Budget", 12, 5, DEEP_GREEN)

    # Feature callouts on the right
    font_feat = get_font(34, bold=True)
    font_detail = get_font(28)
    features = [
        ("12 Monthly Tabs", "One tab per month,\npre-formatted & ready"),
        ("Income Section", "Track 5 income sources\nwith expected vs actual"),
        ("40+ Expense Categories", "Housing, food, health,\nentertainment & more"),
        ("Auto-Calculations", "Formulas compute totals,\ndifferences & net income"),
        ("Annual Dashboard", "See your full year\ntrends at a glance"),
    ]

    for i, (title, detail) in enumerate(features):
        fy = 320 + i * 175
        fx = 1600
        # Bullet circle
        draw.ellipse([fx, fy+5, fx+30, fy+35], fill=SAGE_GREEN)
        draw_checkmark(draw, fx+5, fy+8, 20, WHITE)
        draw.text((fx+45, fy), title, fill=DEEP_GREEN, font=font_feat)
        draw.text((fx+45, fy+45), detail, fill=CHARCOAL, font=font_detail)

    # Mini charts at bottom
    draw_chart_mockup(draw, 100, 1300, 500, 350, "bar", SAGE_GREEN)
    draw_chart_mockup(draw, 700, 1300, 500, 350, "pie", DEEP_GREEN)
    draw_chart_mockup(draw, 1300, 1300, 500, 350, "line", CORAL)

    # Labels under charts
    chart_font = get_font(28, bold=True)
    draw.text((220, 1670), "Spending by Month", fill=CHARCOAL, font=chart_font)
    draw.text((800, 1670), "Category Breakdown", fill=CHARCOAL, font=chart_font)
    draw.text((1410, 1670), "Savings Trend", fill=CHARCOAL, font=chart_font)

    # Bottom bar
    draw.rectangle([0, 1800, W, H], fill=DEEP_GREEN)
    bottom_font = get_font(48, bold=True)
    draw.text((W//2-500, 1860), "WORKS WITH EXCEL & GOOGLE SHEETS", fill=WHITE, font=bottom_font)

    # Decorative elements
    draw.rectangle([0, H-60, W, H-50], fill=GOLD)

    img.save(os.path.join(OUT_DIR, "03_monthly_budget_detail.jpg"), "JPEG", quality=95)
    print("Created: 03_monthly_budget_detail.jpg")


# ============================================================
# IMAGE 4: Debt Payoff Tracker Detail
# ============================================================
def create_image_04():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Coral header
    draw.rectangle([0, 0, W, 200], fill=CORAL)
    draw.rectangle([0, 200, W, 210], fill=GOLD)
    font_title = get_font(80, bold=True)
    font_sub = get_font(38)
    draw.text((120, 50), "DEBT PAYOFF TRACKER", fill=WHITE, font=font_title)
    draw.text((120, 145), "Your roadmap to becoming debt-free", fill=WARM_CREAM, font=font_sub)

    # Debt progress visualization
    font_label = get_font(32, bold=True)
    font_sm = get_font(26)
    debts = [
        ("Credit Card 1", 5000, 3200, CORAL),
        ("Credit Card 2", 3500, 1800, (220, 130, 110)),
        ("Student Loan", 25000, 18000, SAGE_GREEN),
        ("Car Loan", 15000, 9500, DEEP_GREEN),
        ("Personal Loan", 8000, 2000, GOLD),
    ]

    bar_x = 200
    bar_w = 1800
    for i, (name, total, remaining, color) in enumerate(debts):
        by = 300 + i * 160
        draw.text((bar_x, by), name, fill=CHARCOAL, font=font_label)
        # Background bar
        draw_rounded_rect(draw, (bar_x, by+45, bar_x+bar_w, by+90), 22, LIGHT_GRAY)
        # Progress bar
        progress = (total - remaining) / total
        pw = int(bar_w * progress)
        if pw > 44:
            draw_rounded_rect(draw, (bar_x, by+45, bar_x+pw, by+90), 22, color)
        # Percentage text
        pct_text = f"{progress*100:.0f}% paid off"
        draw.text((bar_x+bar_w+20, by+50), pct_text, fill=CHARCOAL, font=font_sm)

    # Strategy comparison section
    strat_y = 1150
    draw_rounded_rect(draw, (80, strat_y, 1150, strat_y+500), 20, SOFT_MINT, outline=SAGE_GREEN, width=3)
    draw_rounded_rect(draw, (1250, strat_y, 2320, strat_y+500), 20, (252, 232, 227), outline=CORAL, width=3)

    strat_font = get_font(44, bold=True)
    draw.text((150, strat_y+30), "SNOWBALL", fill=DEEP_GREEN, font=strat_font)
    draw.text((150, strat_y+80), "METHOD", fill=SAGE_GREEN, font=get_font(36, bold=True))
    desc_font = get_font(28)
    snowball_lines = [
        "Pay smallest balance first",
        "Quick wins for motivation",
        "Roll payments forward",
        "Best for staying motivated",
    ]
    for i, line in enumerate(snowball_lines):
        draw_checkmark(draw, 170, strat_y+150+i*55, 18, DEEP_GREEN)
        draw.text((210, strat_y+145+i*55), line, fill=CHARCOAL, font=desc_font)

    draw.text((1320, strat_y+30), "AVALANCHE", fill=CORAL, font=strat_font)
    draw.text((1320, strat_y+80), "METHOD", fill=(200, 120, 100), font=get_font(36, bold=True))
    avalanche_lines = [
        "Pay highest interest first",
        "Save more on interest",
        "Mathematically optimal",
        "Best for saving money",
    ]
    for i, line in enumerate(avalanche_lines):
        draw_checkmark(draw, 1340, strat_y+150+i*55, 18, CORAL)
        draw.text((1380, strat_y+145+i*55), line, fill=CHARCOAL, font=desc_font)

    # "VS" circle
    vs_cx = W // 2
    draw.ellipse([vs_cx-50, strat_y+200, vs_cx+50, strat_y+300], fill=GOLD)
    vs_font = get_font(42, bold=True)
    draw.text((vs_cx-28, strat_y+220), "VS", fill=WHITE, font=vs_font)

    # Bottom
    draw.rectangle([0, H-160, W, H], fill=DEEP_GREEN)
    draw.rectangle([0, H-170, W, H-160], fill=CORAL)
    bottom_font = get_font(44, bold=True)
    draw.text((W//2-550, H-120), "TRACK EVERY DEBT  |  LOG EVERY PAYMENT  |  GET FREE", fill=WHITE, font=bottom_font)

    img.save(os.path.join(OUT_DIR, "04_debt_payoff_detail.jpg"), "JPEG", quality=95)
    print("Created: 04_debt_payoff_detail.jpg")


# ============================================================
# IMAGE 5: Savings Goal Tracker Detail
# ============================================================
def create_image_05():
    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Gold header
    draw.rectangle([0, 0, W, 200], fill=GOLD)
    font_title = get_font(80, bold=True)
    font_sub = get_font(38)
    draw.text((120, 50), "SAVINGS GOAL TRACKER", fill=WHITE, font=font_title)
    draw.text((120, 145), "Watch your money grow toward every dream", fill=(255, 245, 220), font=font_sub)

    # Goal progress circles
    goals = [
        ("Emergency\nFund", 10000, 7500, DEEP_GREEN),
        ("Vacation", 3000, 1800, CORAL),
        ("New Car", 8000, 3200, SAGE_GREEN),
        ("Home\nDown Pmt", 50000, 12000, GOLD),
        ("Wedding", 15000, 5000, (180, 130, 170)),
    ]

    font_goal = get_font(30, bold=True)
    font_pct = get_font(52, bold=True)
    font_amt = get_font(24)

    for i, (name, target, saved, color) in enumerate(goals):
        cx = 250 + i * 420
        cy = 500
        r = 150

        # Background circle
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=LIGHT_GRAY, outline=MEDIUM_GRAY, width=2)

        # Progress arc (simulated with filled wedge)
        pct = saved / target
        end_angle = int(360 * pct) - 90
        if pct > 0:
            draw.pieslice([cx-r, cy-r, cx+r, cy+r], -90, end_angle, fill=color)
            # Inner circle to make it a ring
            inner_r = r - 35
            draw.ellipse([cx-inner_r, cy-inner_r, cx+inner_r, cy+inner_r], fill=WHITE)

        # Percentage text
        pct_text = f"{pct*100:.0f}%"
        bbox = draw.textbbox((0, 0), pct_text, font=font_pct)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw//2, cy - 30), pct_text, fill=color, font=font_pct)

        # Goal name below
        bbox2 = draw.textbbox((0, 0), name, font=font_goal)
        tw2 = bbox2[2] - bbox2[0]
        draw.text((cx - tw2//2, cy + r + 20), name, fill=CHARCOAL, font=font_goal, align="center")

        # Amount
        amt_text = f"${saved:,} / ${target:,}"
        bbox3 = draw.textbbox((0, 0), amt_text, font=font_amt)
        tw3 = bbox3[2] - bbox3[0]
        draw.text((cx - tw3//2, cy + r + 85), amt_text, fill=(120, 120, 120), font=font_amt)

    # Features section
    feat_y = 900
    draw.rectangle([0, feat_y, W, feat_y + 5], fill=GOLD)

    font_feat_title = get_font(52, bold=True)
    draw.text((120, feat_y + 40), "FEATURES", fill=DEEP_GREEN, font=font_feat_title)

    font_feat = get_font(34, bold=True)
    font_feat_desc = get_font(28)

    left_features = [
        ("Track 10 Goals", "Custom names, targets & deadlines"),
        ("Auto Progress", "Formulas calculate % complete"),
        ("Monthly Target", "Know exactly how much to save"),
        ("Priority Ranking", "Focus on what matters most"),
    ]
    right_features = [
        ("Savings Log", "Record every deposit with notes"),
        ("Running Totals", "See cumulative savings grow"),
        ("Source Tracking", "Know where savings come from"),
        ("Status Updates", "Mark goals in-progress or done"),
    ]

    for i, (title, desc) in enumerate(left_features):
        fy = feat_y + 120 + i * 120
        draw_dollar_icon(draw, 160, fy + 20, 25, SAGE_GREEN)
        draw.text((210, fy), title, fill=DEEP_GREEN, font=font_feat)
        draw.text((210, fy + 45), desc, fill=CHARCOAL, font=font_feat_desc)

    for i, (title, desc) in enumerate(right_features):
        fy = feat_y + 120 + i * 120
        draw_dollar_icon(draw, 1360, fy + 20, 25, GOLD)
        draw.text((1410, fy), title, fill=DEEP_GREEN, font=font_feat)
        draw.text((1410, fy + 45), desc, fill=CHARCOAL, font=font_feat_desc)

    # Bottom section with spreadsheet mockup
    draw_spreadsheet_mockup(draw, 300, 1550, 1800, 600, "Savings Goal Tracker 2026", 8, 5, GOLD)

    # Badge
    draw_rounded_rect(draw, (100, 2180, 500, 2260), 15, DEEP_GREEN)
    badge_font = get_font(32, bold=True)
    draw.text((140, 2195), "INSTANT DOWNLOAD", fill=WHITE, font=badge_font)

    img.save(os.path.join(OUT_DIR, "05_savings_tracker_detail.jpg"), "JPEG", quality=95)
    print("Created: 05_savings_tracker_detail.jpg")


# ============================================================
# IMAGE 6: Daily Expense Tracker Detail
# ============================================================
def create_image_06():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 200], fill=SAGE_GREEN)
    font_title = get_font(76, bold=True)
    font_sub = get_font(38)
    draw.text((120, 50), "DAILY EXPENSE TRACKER", fill=WHITE, font=font_title)
    draw.text((120, 145), "Log every purchase. Know where your money goes.", fill=SOFT_MINT, font=font_sub)

    # Main mockup
    draw_spreadsheet_mockup(draw, 100, 280, 1300, 800, "February 2026 Expenses", 12, 5, SAGE_GREEN)

    # Category breakdown on the right
    font_cat = get_font(36, bold=True)
    font_amt = get_font(30)
    draw.text((1550, 300), "SPENDING BY", fill=DEEP_GREEN, font=font_cat)
    draw.text((1550, 345), "CATEGORY", fill=SAGE_GREEN, font=font_cat)

    cats = [
        ("Food & Drink", "$487", CORAL, 0.35),
        ("Transportation", "$215", DEEP_GREEN, 0.15),
        ("Shopping", "$312", GOLD, 0.22),
        ("Entertainment", "$89", SAGE_GREEN, 0.06),
        ("Bills", "$450", (100, 130, 160), 0.32),
        ("Health", "$125", (170, 130, 170), 0.09),
    ]

    for i, (name, amt, color, pct) in enumerate(cats):
        cy = 430 + i * 100
        # Mini bar
        bar_max = 600
        bar_w = int(bar_max * pct)
        draw_rounded_rect(draw, (1550, cy, 1550+bar_max, cy+35), 17, LIGHT_GRAY)
        if bar_w > 34:
            draw_rounded_rect(draw, (1550, cy, 1550+bar_w, cy+35), 17, color)
        draw.text((1550, cy+40), name, fill=CHARCOAL, font=font_amt)
        draw.text((1550+bar_max+20, cy+5), amt, fill=color, font=get_font(28, bold=True))

    # Bottom features row
    feat_y = 1200
    draw.rectangle([0, feat_y, W, feat_y+5], fill=SAGE_GREEN)

    font_feat = get_font(38, bold=True)
    font_detail = get_font(28)

    bottom_features = [
        ("12 Month Tabs", "Jan through Dec,\npre-formatted"),
        ("Category Sorting", "Auto-summary by\nspending category"),
        ("Running Totals", "See daily cumulative\nspending in real-time"),
        ("Payment Methods", "Track cash, card,\nVenmo & more"),
    ]

    for i, (title, detail) in enumerate(bottom_features):
        fx = 100 + i * 580
        fy = feat_y + 50

        draw_rounded_rect(draw, (fx, fy, fx+520, fy+350), 15, WARM_CREAM, outline=SAGE_GREEN, width=2)
        # Number circle
        draw.ellipse([fx+220, fy+20, fx+300, fy+100], fill=SAGE_GREEN)
        num_font = get_font(40, bold=True)
        draw.text((fx+245, fy+30), str(i+1), fill=WHITE, font=num_font)
        draw.text((fx+30, fy+120), title, fill=DEEP_GREEN, font=font_feat)
        draw.text((fx+30, fy+175), detail, fill=CHARCOAL, font=font_detail)

    # Pie chart
    draw_chart_mockup(draw, 400, 1700, 600, 500, "pie", SAGE_GREEN)
    draw_chart_mockup(draw, 1200, 1700, 600, 500, "bar", CORAL)

    # Bottom bar
    draw.rectangle([0, H-100, W, H], fill=DEEP_GREEN)
    bottom_font = get_font(42, bold=True)
    draw.text((W//2-400, H-75), "EXCEL  +  GOOGLE SHEETS COMPATIBLE", fill=WHITE, font=bottom_font)

    img.save(os.path.join(OUT_DIR, "06_expense_tracker_detail.jpg"), "JPEG", quality=95)
    print("Created: 06_expense_tracker_detail.jpg")


# ============================================================
# IMAGE 7: Bill Calendar & Subscription Audit
# ============================================================
def create_image_07():
    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 200], fill=DEEP_GREEN)
    font_title = get_font(72, bold=True)
    font_sub = get_font(38)
    draw.text((120, 50), "BILL PAYMENT CALENDAR", fill=WHITE, font=font_title)
    draw.text((120, 145), "Never miss a bill + audit your subscriptions", fill=SOFT_MINT, font=font_sub)

    # Calendar grid mockup
    cal_x, cal_y = 100, 280
    cal_w, cal_h = 1200, 900
    draw_rounded_rect(draw, (cal_x, cal_y, cal_x+cal_w, cal_y+cal_h), 15, WHITE, outline=MEDIUM_GRAY, width=2)

    # Month header
    draw_rounded_rect(draw, (cal_x, cal_y, cal_x+cal_w, cal_y+60), 15, DEEP_GREEN)
    draw.rectangle([cal_x, cal_y+30, cal_x+cal_w, cal_y+60], fill=DEEP_GREEN)
    month_font = get_font(36, bold=True)
    draw.text((cal_x+cal_w//2-100, cal_y+12), "FEBRUARY 2026", fill=WHITE, font=month_font)

    # Day headers
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_w = cal_w // 7
    day_font = get_font(24, bold=True)
    for i, d in enumerate(days):
        dx = cal_x + i * day_w + day_w//2 - 15
        draw.text((dx, cal_y + 70), d, fill=SAGE_GREEN, font=day_font)

    # Calendar cells with some bill markers
    cell_h = (cal_h - 110) // 5
    num_font = get_font(22)
    bill_font = get_font(16, bold=True)
    day_num = 1
    bill_days = {1: ("Rent", CORAL), 5: ("Electric", SAGE_GREEN), 10: ("Internet", DEEP_GREEN),
                 15: ("Phone", GOLD), 20: ("Insurance", CORAL), 25: ("Gym", SAGE_GREEN)}

    for week in range(5):
        for day in range(7):
            if (week == 0 and day < 6) or day_num > 28:
                if week == 0:
                    continue
                else:
                    continue
            cx = cal_x + day * day_w + 5
            cy = cal_y + 100 + week * cell_h + 5

            draw.text((cx + 5, cy), str(day_num), fill=CHARCOAL, font=num_font)

            if day_num in bill_days:
                name, color = bill_days[day_num]
                draw_rounded_rect(draw, (cx+2, cy+28, cx+day_w-12, cy+50), 6, color)
                draw.text((cx+8, cy+30), name, fill=WHITE, font=bill_font)

            day_num += 1
            if day_num > 28:
                break

    # Subscription audit section on right
    audit_x = 1400
    draw_rounded_rect(draw, (audit_x, 280, 2320, 1180), 20, WHITE, outline=CORAL, width=3)
    audit_font = get_font(40, bold=True)
    draw.text((audit_x+40, 310), "SUBSCRIPTION", fill=CORAL, font=audit_font)
    draw.text((audit_x+40, 360), "AUDIT", fill=(200, 120, 100), font=audit_font)

    subs = [
        ("Netflix", "$15.99/mo", True),
        ("Spotify", "$10.99/mo", True),
        ("Amazon Prime", "$14.99/mo", True),
        ("Disney+", "$13.99/mo", False),
        ("Gym", "$49.99/mo", True),
        ("Cloud Storage", "$2.99/mo", True),
        ("Meal Kit", "$59.99/mo", False),
        ("VPN", "$8.99/mo", True),
    ]

    sub_font = get_font(28)
    amt_font = get_font(26, bold=True)
    for i, (name, amt, keep) in enumerate(subs):
        sy = 440 + i * 75
        color = DEEP_GREEN if keep else CORAL
        marker = "KEEP" if keep else "CUT"
        draw_rounded_rect(draw, (audit_x+40, sy, audit_x+130, sy+40), 10, color)
        draw.text((audit_x+52, sy+5), marker, fill=WHITE, font=get_font(22, bold=True))
        draw.text((audit_x+150, sy+5), name, fill=CHARCOAL, font=sub_font)
        draw.text((audit_x+600, sy+5), amt, fill=color, font=amt_font)

    # Potential savings callout
    save_y = 1100
    draw_rounded_rect(draw, (audit_x+40, save_y, audit_x+880, save_y+55), 12, GOLD)
    save_font = get_font(30, bold=True)
    draw.text((audit_x+60, save_y+10), "POTENTIAL SAVINGS: $73.98/mo ($887/yr)", fill=WHITE, font=save_font)

    # Bottom features
    draw.rectangle([0, 1300, W, 1310], fill=DEEP_GREEN)
    font_feat = get_font(36, bold=True)
    font_desc = get_font(28)

    feats = [
        ("20 Bill Slots", "Pre-formatted for\nall your recurring bills"),
        ("Auto-Pay Tracking", "Mark which bills are\non autopilot"),
        ("Annual Totals", "See the true yearly\ncost of each bill"),
        ("Audit Tool", "Identify subscriptions\nyou can cut"),
    ]
    for i, (title, desc) in enumerate(feats):
        fx = 100 + i * 580
        fy = 1380
        draw_rounded_rect(draw, (fx, fy, fx+520, fy+250), 12, WHITE, outline=SAGE_GREEN, width=2)
        draw.text((fx+30, fy+20), title, fill=DEEP_GREEN, font=font_feat)
        draw.text((fx+30, fy+70), desc, fill=CHARCOAL, font=font_desc)

    # Bottom
    draw.rectangle([0, H-100, W, H], fill=DEEP_GREEN)
    bottom_font = get_font(42, bold=True)
    draw.text((W//2-300, H-75), "STOP OVERPAYING. START SAVING.", fill=GOLD, font=bottom_font)

    img.save(os.path.join(OUT_DIR, "07_bill_calendar_detail.jpg"), "JPEG", quality=95)
    print("Created: 07_bill_calendar_detail.jpg")


# ============================================================
# IMAGE 8: How It Works / Compatibility
# ============================================================
def create_image_08():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 180], fill=DEEP_GREEN)
    font_title = get_font(76, bold=True)
    draw.text((120, 45), "HOW IT WORKS", fill=WHITE, font=font_title)

    # 4 steps
    font_step = get_font(44, bold=True)
    font_desc = get_font(34)
    font_num = get_font(80, bold=True)

    steps = [
        ("PURCHASE &\nDOWNLOAD", "Add to cart, checkout,\nand get instant access\nto all 6 spreadsheets"),
        ("OPEN IN EXCEL\nOR GOOGLE SHEETS", "Works with Microsoft Excel,\nGoogle Sheets, Numbers,\nand LibreOffice"),
        ("CUSTOMIZE\nFOR YOUR LIFE", "Edit categories, add goals,\nset your own budget amounts.\nMake it yours!"),
        ("TRACK &\nSAVE MONEY", "Use daily, weekly, or monthly.\nWatch your financial health\nimprove over time"),
    ]

    for i, (title, desc) in enumerate(steps):
        sx = 100
        sy = 260 + i * 370

        # Step number circle
        draw.ellipse([sx, sy, sx+120, sy+120], fill=DEEP_GREEN if i % 2 == 0 else SAGE_GREEN)
        draw.text((sx+25, sy+15), str(i+1), fill=WHITE, font=font_num)

        # Arrow connector
        if i < 3:
            arrow_y = sy + 130
            draw.line([(sx+60, arrow_y), (sx+60, arrow_y+100)], fill=GOLD, width=4)
            # Arrow head
            draw.polygon([(sx+40, arrow_y+80), (sx+80, arrow_y+80), (sx+60, arrow_y+110)], fill=GOLD)

        # Title & description
        draw.text((sx+160, sy+5), title, fill=DEEP_GREEN, font=font_step)
        draw.text((sx+160, sy+100 if "\n" in title else sy+60), desc, fill=CHARCOAL, font=font_desc)

        # Side illustration
        ix = 1400
        if i == 0:
            draw_rounded_rect(draw, (ix, sy, ix+800, sy+280), 15, SOFT_MINT)
            draw_dollar_icon(draw, ix+400, sy+140, 80, GOLD)
            cart_font = get_font(36, bold=True)
            draw.text((ix+200, sy+240), "Instant Download", fill=DEEP_GREEN, font=cart_font)
        elif i == 1:
            # App icons
            apps = [("Excel", DEEP_GREEN), ("Sheets", SAGE_GREEN), ("Numbers", CORAL)]
            for j, (app, color) in enumerate(apps):
                ax = ix + j * 270
                draw_rounded_rect(draw, (ax, sy+20, ax+230, sy+230), 20, color)
                app_font = get_font(34, bold=True)
                draw.text((ax+40, sy+100), app, fill=WHITE, font=app_font)
        elif i == 2:
            draw_spreadsheet_mockup(draw, ix, sy, 800, 280, "Your Custom Budget", 5, 4, SAGE_GREEN)
        elif i == 3:
            draw_chart_mockup(draw, ix, sy, 380, 260, "line", DEEP_GREEN)
            draw_chart_mockup(draw, ix+420, sy, 380, 260, "bar", CORAL)

    # Bottom compatibility section
    draw.rectangle([0, 1800, W, H], fill=DEEP_GREEN)
    comp_font = get_font(48, bold=True)
    draw.text((W//2-350, 1840), "COMPATIBLE WITH:", fill=GOLD, font=comp_font)

    comp_items = ["Microsoft Excel", "Google Sheets", "Apple Numbers", "LibreOffice"]
    item_font = get_font(38)
    for i, item in enumerate(comp_items):
        ix = 200 + i * 540
        draw_checkmark(draw, ix, 1940, 25, GOLD)
        draw.text((ix+40, 1935), item, fill=WHITE, font=item_font)

    # File format note
    note_font = get_font(32)
    draw.text((W//2-350, 2050), ".XLSX format  |  No software purchase needed", fill=SOFT_MINT, font=note_font)

    img.save(os.path.join(OUT_DIR, "08_how_it_works.jpg"), "JPEG", quality=95)
    print("Created: 08_how_it_works.jpg")


# ============================================================
# IMAGE 9: Testimonials / Social Proof
# ============================================================
def create_image_09():
    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 180], fill=DEEP_GREEN)
    font_title = get_font(72, bold=True)
    draw.text((120, 45), "WHAT BUYERS ARE SAYING", fill=WHITE, font=font_title)

    # Star rating
    font_star = get_font(60)
    font_rating = get_font(42, bold=True)
    stars = "★ ★ ★ ★ ★"
    draw.text((W//2-200, 220), stars, fill=GOLD, font=font_star)
    draw.text((W//2-150, 300), "4.9 out of 5 stars", fill=CHARCOAL, font=font_rating)

    # Testimonial cards
    font_quote = get_font(30)
    font_name = get_font(26, bold=True)

    testimonials = [
        ("This spreadsheet bundle changed my financial life! I can finally see where my money goes and I've saved $400/month since I started using it.", "- Sarah M.", "Verified Buyer"),
        ("So well organized and beautiful! The formulas do all the math for me. I just enter my numbers and everything calculates automatically.", "- Jessica R.", "Verified Buyer"),
        ("I've tried so many budget templates and this is BY FAR the best. The debt payoff tracker alone is worth the price. Highly recommend!", "- Michael T.", "Verified Buyer"),
        ("Finally got my finances under control! The bill calendar has saved me from late fees multiple times. Worth every penny.", "- Amanda K.", "Verified Buyer"),
    ]

    for i, (quote, name, badge) in enumerate(testimonials):
        col = i % 2
        row = i // 2
        cx = 80 + col * 1180
        cy = 400 + row * 550

        draw_rounded_rect(draw, (cx, cy, cx+1080, cy+480), 20, WHITE, outline=SAGE_GREEN, width=2)

        # Quote mark
        quote_font = get_font(80, bold=True)
        draw.text((cx+30, cy+10), '"', fill=SAGE_GREEN, font=quote_font)

        # Quote text
        # Wrap manually
        words = quote.split()
        lines = []
        current = ""
        for word in words:
            test = current + " " + word if current else word
            bbox = draw.textbbox((0, 0), test, font=font_quote)
            if bbox[2] - bbox[0] > 960:
                lines.append(current)
                current = word
            else:
                current = test
        if current:
            lines.append(current)

        for j, line in enumerate(lines[:6]):
            draw.text((cx+50, cy+90+j*42), line, fill=CHARCOAL, font=font_quote)

        # Name and badge
        name_y = cy + 380
        draw.text((cx+50, name_y), name, fill=DEEP_GREEN, font=font_name)
        draw_rounded_rect(draw, (cx+250, name_y-3, cx+480, name_y+33), 10, SAGE_GREEN)
        draw.text((cx+265, name_y+2), badge, fill=WHITE, font=get_font(22, bold=True))

        # Stars
        small_stars = "★★★★★"
        draw.text((cx+800, name_y), small_stars, fill=GOLD, font=get_font(30))

    # Bottom CTA
    draw.rectangle([0, 1500, W, H], fill=DEEP_GREEN)
    cta_font = get_font(56, bold=True)
    sub_font = get_font(36)
    draw.text((W//2-500, 1560), "JOIN THOUSANDS OF HAPPY", fill=WHITE, font=cta_font)
    draw.text((W//2-300, 1640), "BUDGET TRACKERS", fill=GOLD, font=cta_font)

    draw_rounded_rect(draw, (W//2-300, 1760, W//2+300, 1860), 30, CORAL)
    btn_font = get_font(44, bold=True)
    draw.text((W//2-200, 1780), "ADD TO CART", fill=WHITE, font=btn_font)

    # Trust badges
    trust_items = ["Instant Download", "Secure Checkout", "Satisfaction Guaranteed"]
    trust_font = get_font(28)
    for i, item in enumerate(trust_items):
        tx = 400 + i * 600
        draw_checkmark(draw, tx, 1920, 20, GOLD)
        draw.text((tx+30, 1915), item, fill=SOFT_MINT, font=trust_font)

    # Stats
    stat_font = get_font(60, bold=True)
    stat_label = get_font(28)
    stats = [("5,000+", "Downloads"), ("4.9★", "Rating"), ("6", "Spreadsheets")]
    for i, (num, label) in enumerate(stats):
        sx = 300 + i * 700
        draw.text((sx, 2020), num, fill=GOLD, font=stat_font)
        draw.text((sx, 2090), label, fill=SOFT_MINT, font=stat_label)

    img.save(os.path.join(OUT_DIR, "09_testimonials.jpg"), "JPEG", quality=95)
    print("Created: 09_testimonials.jpg")


# ============================================================
# IMAGE 10: Annual Overview + CTA
# ============================================================
def create_image_10():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Full deep green background with content
    draw.rectangle([0, 0, W, H], fill=DEEP_GREEN)

    # Decorative pattern - subtle dollar signs
    pattern_font = get_font(100)
    for row in range(8):
        for col in range(8):
            px = col * 320 + 50
            py = row * 320 + 50
            draw.text((px, py), "$", fill=(*SAGE_GREEN, 30), font=pattern_font)

    # Central content card
    card_x, card_y = 150, 150
    card_w, card_h = W - 300, H - 300
    draw_rounded_rect(draw, (card_x, card_y, card_x+card_w, card_y+card_h), 30, WHITE)

    # Title
    font_title = get_font(72, bold=True)
    font_sub = get_font(42)
    draw.text((card_x+100, card_y+80), "GET THE COMPLETE", fill=DEEP_GREEN, font=font_title)
    draw.text((card_x+100, card_y+170), "2026 BUDGET BUNDLE", fill=SAGE_GREEN, font=font_title)

    # Divider
    draw.rectangle([card_x+100, card_y+270, card_x+card_w-100, card_y+275], fill=GOLD)

    # Bundle contents with checkmarks
    font_item = get_font(38, bold=True)
    font_val = get_font(30)

    items = [
        ("Monthly Budget Tracker", "12 tabs, 40+ categories, auto-formulas"),
        ("Annual Budget Overview", "Full year planning with monthly averages"),
        ("Debt Payoff Tracker", "Snowball + avalanche strategy tools"),
        ("Savings Goal Tracker", "10 goals with progress visualization"),
        ("Daily Expense Tracker", "Category sorting & running totals"),
        ("Bill Payment Calendar", "20 bill slots + subscription audit"),
    ]

    for i, (name, val) in enumerate(items):
        iy = card_y + 320 + i * 120
        draw_checkmark(draw, card_x+120, iy+10, 28, DEEP_GREEN)
        draw.text((card_x+170, iy), name, fill=CHARCOAL, font=font_item)
        draw.text((card_x+170, iy+48), val, fill=(140, 140, 140), font=font_val)

    # Price section
    price_y = card_y + 1100
    draw.rectangle([card_x+100, price_y, card_x+card_w-100, price_y+3], fill=GOLD)

    # Strikethrough "regular" price
    reg_font = get_font(48)
    sale_font = get_font(80, bold=True)
    draw.text((card_x+200, price_y+30), "Regular: $29.99", fill=MEDIUM_GRAY, font=reg_font)
    draw.line([(card_x+200, price_y+60), (card_x+620, price_y+60)], fill=CORAL, width=3)

    draw.text((card_x+700, price_y+10), "$9.99", fill=DEEP_GREEN, font=sale_font)
    draw_rounded_rect(draw, (card_x+1050, price_y+20, card_x+1350, price_y+80), 15, CORAL)
    save_font = get_font(32, bold=True)
    draw.text((card_x+1075, price_y+30), "SAVE 67%", fill=WHITE, font=save_font)

    # CTA button
    btn_y = price_y + 140
    draw_rounded_rect(draw, (card_x+400, btn_y, card_x+card_w-400, btn_y+100), 50, CORAL)
    btn_font = get_font(48, bold=True)
    draw.text((card_x+600, btn_y+20), "ADD TO CART", fill=WHITE, font=btn_font)

    # Trust badges at bottom of card
    trust_y = btn_y + 140
    font_trust = get_font(28)
    trust = ["Instant Digital Download", "Works with Excel & Sheets", "Lifetime Access"]
    for i, t in enumerate(trust):
        tx = card_x + 250 + i * 550
        draw_checkmark(draw, tx, trust_y+5, 18, SAGE_GREEN)
        draw.text((tx+28, trust_y), t, fill=CHARCOAL, font=font_trust)

    # Decorative corners
    draw.polygon([(card_x, card_y), (card_x+80, card_y), (card_x, card_y+80)], fill=GOLD)
    draw.polygon([(card_x+card_w, card_y), (card_x+card_w-80, card_y), (card_x+card_w, card_y+80)], fill=GOLD)
    draw.polygon([(card_x, card_y+card_h), (card_x+80, card_y+card_h), (card_x, card_y+card_h-80)], fill=GOLD)
    draw.polygon([(card_x+card_w, card_y+card_h), (card_x+card_w-80, card_y+card_h), (card_x+card_w, card_y+card_h-80)], fill=GOLD)

    img.save(os.path.join(OUT_DIR, "10_bundle_cta.jpg"), "JPEG", quality=95)
    print("Created: 10_bundle_cta.jpg")


if __name__ == "__main__":
    print("Creating 10 listing images...")
    print("=" * 50)
    create_image_01()
    create_image_02()
    create_image_03()
    create_image_04()
    create_image_05()
    create_image_06()
    create_image_07()
    create_image_08()
    create_image_09()
    create_image_10()
    print("=" * 50)
    print("All 10 images created!")
