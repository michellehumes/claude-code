"""
Create professional Etsy listing images for the Budget Bundle.
Generates 5 images:
1. Main listing image (hero/thumbnail)
2. Feature overview (what's included)
3. Monthly Budget tab mockup
4. Savings & Debt tabs showcase
5. Testimonial/social proof style
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = "/home/user/claude-code/etsy-digital-download/images"

# ── Dimensions: Etsy recommends 2700x2025 (4:3) for listing images
W, H = 2700, 2025

# ── Colors ──
DARK_GREEN = (27, 67, 50)
MED_GREEN = (45, 106, 79)
LIGHT_GREEN = (82, 183, 136)
PALE_GREEN = (216, 243, 220)
ACCENT_MINT = (183, 228, 199)
WHITE = (255, 255, 255)
LIGHT_GRAY = (245, 245, 245)
DARK_TEXT = (33, 33, 33)
OFF_WHITE = (250, 250, 247)
GOLD = (244, 162, 97)
SOFT_SHADOW = (200, 210, 200)
CREAM = (255, 253, 245)

def get_font(size, bold=False):
    """Try to load a clean sans-serif font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill_color, outline=None, width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill_color, outline=outline, width=width)

def draw_centered_text(draw, text, y, font, color, width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]

def draw_text_at(draw, text, x, y, font, color):
    draw.text((x, y), text, font=font, fill=color)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

# ═══════════════════════════════════════════════════
#  IMAGE 1: MAIN HERO / THUMBNAIL
# ═══════════════════════════════════════════════════
def create_hero_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Background design - diagonal stripe accent
    for i in range(0, W + H, 80):
        draw.line([(i, 0), (i - H, H)], fill=(*PALE_GREEN, 30), width=2)

    # Top banner
    draw.rectangle([(0, 0), (W, 180)], fill=DARK_GREEN)
    font_sm = get_font(42)
    draw_centered_text(draw, "INSTANT DOWNLOAD  |  GOOGLE SHEETS & EXCEL COMPATIBLE", 70, font_sm, ACCENT_MINT)

    # Main content area with shadow effect
    draw_rounded_rect(draw, (120, 250, W-120, H-200), 30, WHITE, outline=SOFT_SHADOW, width=3)

    # Inner accent stripe
    draw.rectangle([(120, 250), (W-120, 330)], fill=MED_GREEN)
    font_badge = get_font(36, bold=True)
    draw_centered_text(draw, "ALL-IN-ONE SPREADSHEET  |  7 TABS  |  READY TO USE", 265, font_badge, WHITE)

    # Main title
    font_title = get_font(110, bold=True)
    draw_centered_text(draw, "COMPLETE", 380, font_title, DARK_GREEN)
    draw_centered_text(draw, "BUDGET & FINANCE", 510, font_title, DARK_GREEN)
    draw_centered_text(draw, "BUNDLE", 640, font_title, DARK_GREEN)

    # Year badge
    font_year = get_font(72, bold=True)
    draw_rounded_rect(draw, (W//2 - 130, 790, W//2 + 130, 880), 15, GOLD)
    draw_centered_text(draw, "2026", 798, font_year, WHITE)

    # Feature bullets
    font_features = get_font(44, bold=True)
    features = [
        "Monthly Budget Planner",
        "Daily Expense Tracker",
        "Savings Goals Dashboard",
        "Debt Payoff Calculator",
        "Net Worth Tracker",
        "Annual Overview + Charts",
    ]

    y_start = 940
    col1_x = 300
    col2_x = W // 2 + 100

    for idx, feat in enumerate(features):
        col_x = col1_x if idx < 3 else col2_x
        y = y_start + (idx % 3) * 80
        # Checkmark circle
        cx, cy = col_x - 50, y + 20
        draw.ellipse([(cx-18, cy-18), (cx+18, cy+18)], fill=LIGHT_GREEN)
        draw_text_at(draw, feat, col_x, y, font_features, DARK_TEXT)

    # Divider line
    draw.line([(200, 1220), (W-200, 1220)], fill=ACCENT_MINT, width=3)

    # Value proposition
    font_value = get_font(48, bold=True)
    draw_centered_text(draw, "Take Control of Your Money in Minutes", 1270, font_value, MED_GREEN)

    font_sub = get_font(38)
    draw_centered_text(draw, "No formulas to write. No setup needed. Just fill in your numbers.", 1350, font_sub, DARK_TEXT)

    # Bottom CTA bar
    draw.rectangle([(0, H-160), (W, H)], fill=DARK_GREEN)
    font_cta = get_font(52, bold=True)
    draw_centered_text(draw, "DIGITAL DOWNLOAD  -  PRINT OR USE DIGITALLY", H-130, font_cta, ACCENT_MINT)

    img.save(os.path.join(OUT_DIR, "01_hero_main_listing.png"), quality=95)
    print("Created: 01_hero_main_listing.png")

# ═══════════════════════════════════════════════════
#  IMAGE 2: WHAT'S INCLUDED (Feature breakdown)
# ═══════════════════════════════════════════════════
def create_features_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title section
    draw.rectangle([(0, 0), (W, 200)], fill=DARK_GREEN)
    font_title = get_font(72, bold=True)
    draw_centered_text(draw, "WHAT'S INCLUDED", 55, font_title, WHITE)

    font_sub_title = get_font(38)
    draw_centered_text(draw, "7 Professional Spreadsheet Tabs  |  All Formulas Built In", 150, font_sub_title, ACCENT_MINT)

    # Feature cards - 2 columns, 4 rows
    features = [
        ("MONTHLY BUDGET", "Set income & expense targets.\nTrack actual vs budgeted.\nAuto pie chart breakdown.", LIGHT_GREEN),
        ("EXPENSE TRACKER", "Daily spending log with\ndropdown categories.\nRunning total calculator.", MED_GREEN),
        ("SAVINGS GOALS", "10 customizable goals.\nProgress % & status.\nMonthly amount needed.", LIGHT_GREEN),
        ("DEBT PAYOFF", "8 debt slots with interest.\nPayoff date calculator.\nAvalanche & Snowball tips.", MED_GREEN),
        ("NET WORTH", "Assets vs liabilities.\n12-month tracking history.\nLine chart visualization.", LIGHT_GREEN),
        ("ANNUAL OVERVIEW", "12-month income/expense grid.\nSavings rate by month.\nBar chart comparison.", MED_GREEN),
        ("HOW TO USE GUIDE", "Step-by-step instructions.\nPro tips for success.\nBeginner-friendly walkthrough.", LIGHT_GREEN),
        ("BONUS: AUTO CHARTS", "Pie, bar, and line charts.\nUpdate automatically.\nNo chart-building needed!", GOLD),
    ]

    card_w = 1150
    card_h = 320
    gap_x = 100
    gap_y = 40
    start_x = (W - 2 * card_w - gap_x) // 2
    start_y = 250

    font_card_title = get_font(44, bold=True)
    font_card_body = get_font(32)

    for idx, (title, body, accent) in enumerate(features):
        col = idx % 2
        row = idx // 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        # Card background
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, WHITE, outline=(*accent, 180), width=3)

        # Accent left bar
        draw_rounded_rect(draw, (x, y, x + 12, y + card_h), 6, accent)

        # Number badge
        badge_x = x + 40
        badge_y = y + 20
        draw.ellipse([(badge_x, badge_y), (badge_x + 60, badge_y + 60)], fill=accent)
        font_num = get_font(30, bold=True)
        num_text = str(idx + 1)
        bbox = draw.textbbox((0, 0), num_text, font=font_num)
        nw = bbox[2] - bbox[0]
        draw.text((badge_x + (60 - nw) // 2, badge_y + 12), num_text, font=font_num, fill=WHITE)

        # Title
        draw.text((x + 120, y + 30), title, font=font_card_title, fill=DARK_GREEN)

        # Body text
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw.text((x + 120, y + 100 + li * 55), f"  {line}", font=font_card_body, fill=DARK_TEXT)

    # Bottom bar
    draw.rectangle([(0, H - 100), (W, H)], fill=DARK_GREEN)
    font_bottom = get_font(36, bold=True)
    draw_centered_text(draw, "WORKS WITH GOOGLE SHEETS  |  MICROSOFT EXCEL  |  LIBREOFFICE", H - 80, font_bottom, ACCENT_MINT)

    img.save(os.path.join(OUT_DIR, "02_whats_included.png"), quality=95)
    print("Created: 02_whats_included.png")

# ═══════════════════════════════════════════════════
#  IMAGE 3: SPREADSHEET PREVIEW MOCKUP
# ═══════════════════════════════════════════════════
def create_spreadsheet_mockup():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title
    draw.rectangle([(0, 0), (W, 140)], fill=DARK_GREEN)
    font_title = get_font(56, bold=True)
    draw_centered_text(draw, "MONTHLY BUDGET TAB PREVIEW", 35, font_title, WHITE)

    # "Screen" mockup frame
    screen_x, screen_y = 150, 200
    screen_w, screen_h = W - 300, H - 350

    # Window chrome bar
    draw_rounded_rect(draw, (screen_x, screen_y, screen_x + screen_w, screen_y + 60), 12, (60, 60, 60))
    # Window dots
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([(screen_x + 20 + i*35, screen_y + 17), (screen_x + 46 + i*35, screen_y + 43)], fill=color)

    # Spreadsheet area
    ss_y = screen_y + 60
    draw.rectangle([(screen_x, ss_y), (screen_x + screen_w, screen_y + screen_h)], fill=WHITE)

    # Tab bar at bottom of spreadsheet
    tab_y = screen_y + screen_h - 50
    tabs = ["Monthly Budget", "Expense Tracker", "Savings Goals", "Debt Payoff", "Net Worth", "Annual"]
    tab_x = screen_x + 10
    font_tab = get_font(22)
    for i, tab in enumerate(tabs):
        tw = len(tab) * 14 + 30
        tab_color = LIGHT_GREEN if i == 0 else LIGHT_GRAY
        text_color = WHITE if i == 0 else DARK_TEXT
        draw_rounded_rect(draw, (tab_x, tab_y, tab_x + tw, tab_y + 45), 8, tab_color)
        draw.text((tab_x + 15, tab_y + 12), tab, font=font_tab, fill=text_color)
        tab_x += tw + 8

    # Spreadsheet content mockup
    font_ss_header = get_font(28, bold=True)
    font_ss = get_font(24)

    # Title row
    draw.rectangle([(screen_x + 10, ss_y + 10), (screen_x + screen_w - 10, ss_y + 70)], fill=PALE_GREEN)
    draw_text_at(draw, "MONTHLY BUDGET PLANNER", screen_x + 350, ss_y + 22, get_font(36, bold=True), DARK_GREEN)

    # Column headers
    header_y = ss_y + 90
    cols = [("Category", 500), ("Budgeted", 280), ("Actual", 280), ("Difference", 280), ("", 100)]
    col_x = screen_x + 50
    for label, width in cols:
        draw.rectangle([(col_x, header_y), (col_x + width, header_y + 55)], fill=MED_GREEN)
        if label:
            draw.text((col_x + 15, header_y + 14), label, font=font_ss_header, fill=WHITE)
        col_x += width

    # Sample data rows
    sample_data = [
        ("Housing (Rent/Mortgage)", "$1,500.00", "$1,500.00", "$0.00"),
        ("Utilities", "$200.00", "$185.50", "$14.50"),
        ("Groceries", "$600.00", "$542.30", "$57.70"),
        ("Transportation", "$300.00", "$275.00", "$25.00"),
        ("Insurance", "$250.00", "$250.00", "$0.00"),
        ("Healthcare", "$150.00", "$89.00", "$61.00"),
        ("Phone/Internet", "$120.00", "$120.00", "$0.00"),
        ("Subscriptions", "$80.00", "$79.99", "$0.01"),
        ("Dining Out", "$200.00", "$245.80", "-$45.80"),
        ("Entertainment", "$150.00", "$132.00", "$18.00"),
        ("Clothing", "$100.00", "$0.00", "$100.00"),
        ("Savings/Investments", "$500.00", "$500.00", "$0.00"),
    ]

    for idx, (cat, budgeted, actual, diff) in enumerate(sample_data):
        row_y = header_y + 55 + idx * 48
        bg = LIGHT_GRAY if idx % 2 == 1 else WHITE
        col_x = screen_x + 50
        values = [cat, budgeted, actual, diff]
        widths = [500, 280, 280, 280]
        for vi, (val, width) in enumerate(zip(values, widths)):
            draw.rectangle([(col_x, row_y), (col_x + width, row_y + 48)], fill=bg, outline=(*SOFT_SHADOW,))
            text_color = DARK_TEXT
            if vi == 3 and val.startswith("-"):
                text_color = (230, 57, 70)  # Red for negative
            elif vi == 3 and val != "$0.00":
                text_color = MED_GREEN
            draw.text((col_x + 15, row_y + 12), val, font=font_ss, fill=text_color)
            col_x += width

    # Summary box on right side
    sum_x = screen_x + screen_w - 520
    sum_y = ss_y + 90
    draw_rounded_rect(draw, (sum_x, sum_y, sum_x + 490, sum_y + 300), 15, PALE_GREEN, outline=MED_GREEN, width=2)
    draw_text_at(draw, "MONTHLY SUMMARY", sum_x + 100, sum_y + 20, font_ss_header, DARK_GREEN)

    summary_data = [
        ("Total Income:", "$5,200.00"),
        ("Total Expenses:", "$3,919.59"),
        ("Net Balance:", "$1,280.41"),
        ("Savings Rate:", "24.6%"),
    ]
    for si, (label, val) in enumerate(summary_data):
        sy = sum_y + 80 + si * 50
        draw_text_at(draw, label, sum_x + 30, sy, font_ss, DARK_TEXT)
        color = DARK_GREEN if si == 2 else MED_GREEN if si == 3 else DARK_TEXT
        draw_text_at(draw, val, sum_x + 290, sy, get_font(24, bold=True), color)

    # Bottom banner
    draw.rectangle([(0, H - 100), (W, H)], fill=DARK_GREEN)
    font_bottom = get_font(38, bold=True)
    draw_centered_text(draw, "ALL FORMULAS PRE-BUILT  |  JUST ENTER YOUR NUMBERS", H - 78, font_bottom, ACCENT_MINT)

    img.save(os.path.join(OUT_DIR, "03_budget_tab_preview.png"), quality=95)
    print("Created: 03_budget_tab_preview.png")

# ═══════════════════════════════════════════════════
#  IMAGE 4: SAVINGS & DEBT SHOWCASE
# ═══════════════════════════════════════════════════
def create_savings_debt_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title
    draw.rectangle([(0, 0), (W, 140)], fill=DARK_GREEN)
    font_title = get_font(56, bold=True)
    draw_centered_text(draw, "TRACK YOUR GOALS & CRUSH YOUR DEBT", 35, font_title, WHITE)

    # Left panel: Savings Goals
    panel_w = W // 2 - 80
    panel_x = 50
    panel_y = 200
    panel_h = H - 380

    draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h), 20, WHITE, outline=LIGHT_GREEN, width=3)
    draw.rectangle([(panel_x, panel_y), (panel_x + panel_w, panel_y + 80)], fill=MED_GREEN)
    font_panel = get_font(40, bold=True)
    draw.text((panel_x + 250, panel_y + 18), "SAVINGS GOALS", font=font_panel, fill=WHITE)

    goals = [
        ("Emergency Fund", "$10,000", "$7,500", 75, "Almost There!"),
        ("Vacation Fund", "$3,000", "$1,800", 60, "Halfway!"),
        ("New Car", "$8,000", "$2,400", 30, "Getting There"),
        ("Home Down Payment", "$40,000", "$12,000", 30, "Getting There"),
        ("Holiday Gifts", "$500", "$500", 100, "COMPLETE!"),
    ]

    font_goal = get_font(28, bold=True)
    font_detail = get_font(24)
    gy = panel_y + 110

    for name, target, saved, pct, status in goals:
        # Goal name and amounts
        draw_text_at(draw, name, panel_x + 40, gy, font_goal, DARK_TEXT)
        draw_text_at(draw, f"{saved} / {target}", panel_x + 40, gy + 38, font_detail, MED_GREEN)

        # Progress bar
        bar_x = panel_x + 40
        bar_y_pos = gy + 75
        bar_w = panel_w - 260
        draw_rounded_rect(draw, (bar_x, bar_y_pos, bar_x + bar_w, bar_y_pos + 30), 15, LIGHT_GRAY)
        fill_w = int(bar_w * pct / 100)
        if fill_w > 0:
            bar_color = LIGHT_GREEN if pct < 100 else GOLD
            draw_rounded_rect(draw, (bar_x, bar_y_pos, bar_x + fill_w, bar_y_pos + 30), 15, bar_color)

        # Percentage and status
        draw_text_at(draw, f"{pct}%", bar_x + bar_w + 20, bar_y_pos, font_detail, MED_GREEN)
        status_color = GOLD if status == "COMPLETE!" else DARK_TEXT
        draw_text_at(draw, status, panel_x + panel_w - 200, gy + 10, font_detail, status_color)

        gy += 140

    # Right panel: Debt Payoff
    panel_x2 = W // 2 + 30
    draw_rounded_rect(draw, (panel_x2, panel_y, panel_x2 + panel_w, panel_y + panel_h), 20, WHITE, outline=GOLD, width=3)
    draw.rectangle([(panel_x2, panel_y), (panel_x2 + panel_w, panel_y + 80)], fill=(180, 100, 50))
    draw.text((panel_x2 + 280, panel_y + 18), "DEBT PAYOFF", font=font_panel, fill=WHITE)

    debts = [
        ("Credit Card 1", "$4,200", "19.9%", "$150", "Apr 2028"),
        ("Credit Card 2", "$1,800", "22.5%", "$75", "Jan 2028"),
        ("Student Loan", "$18,500", "5.5%", "$250", "Dec 2031"),
        ("Car Loan", "$12,000", "4.9%", "$350", "Jun 2028"),
        ("Personal Loan", "$3,000", "8.0%", "$150", "Aug 2027"),
    ]

    gy = panel_y + 110
    for name, owed, rate, payment, payoff in debts:
        draw_text_at(draw, name, panel_x2 + 40, gy, font_goal, DARK_TEXT)
        draw_text_at(draw, f"Balance: {owed}  |  Rate: {rate}", panel_x2 + 40, gy + 38, font_detail, (180, 100, 50))
        draw_text_at(draw, f"Payment: {payment}/mo  |  Payoff: {payoff}", panel_x2 + 40, gy + 72, font_detail, MED_GREEN)

        # Payoff timeline bar
        gy += 130

    # Bottom section
    draw_rounded_rect(draw, (100, H - 160, W - 100, H - 30), 15, PALE_GREEN)
    font_tip = get_font(34, bold=True)
    draw_centered_text(draw, "All calculations are automatic - just enter your numbers and watch your progress!", H - 120, font_tip, DARK_GREEN)

    img.save(os.path.join(OUT_DIR, "04_savings_debt_showcase.png"), quality=95)
    print("Created: 04_savings_debt_showcase.png")

# ═══════════════════════════════════════════════════
#  IMAGE 5: WHY BUY / VALUE PROPOSITION
# ═══════════════════════════════════════════════════
def create_value_prop_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top accent
    draw.rectangle([(0, 0), (W, 20)], fill=GOLD)

    # Main title
    font_title = get_font(72, bold=True)
    draw_centered_text(draw, "WHY 10,000+ PEOPLE LOVE", 80, font_title, DARK_GREEN)
    draw_centered_text(draw, "THIS BUDGET BUNDLE", 170, font_title, DARK_GREEN)

    # Divider
    draw.line([(W//2 - 200, 280), (W//2 + 200, 280)], fill=GOLD, width=4)

    # Value points - large icons with text
    values = [
        ("SAVE HOURS", "Pre-built formulas & charts mean\nzero setup time. Just open and go."),
        ("SEE EVERYTHING", "Income, expenses, savings, debt,\nand net worth - all in one file."),
        ("WORKS ANYWHERE", "Compatible with Google Sheets,\nExcel, and LibreOffice. Use on\nany device."),
        ("BEGINNER FRIENDLY", "Includes step-by-step instructions.\nNo spreadsheet experience needed."),
        ("CUSTOMIZE FREELY", "Rename categories, add rows,\nchange colors - make it yours."),
        ("USE FOREVER", "Buy once, use every month.\nNo subscriptions. No recurring fees."),
    ]

    font_val_title = get_font(42, bold=True)
    font_val_body = get_font(30)

    # 3 columns x 2 rows
    col_w = 760
    row_h = 350
    start_x = (W - 3 * col_w) // 2
    start_y = 330

    for idx, (title, body) in enumerate(values):
        col = idx % 3
        row = idx // 3
        x = start_x + col * col_w + 40
        y = start_y + row * row_h

        # Icon circle
        cx, cy = x + 50, y + 50
        draw.ellipse([(cx - 40, cy - 40), (cx + 40, cy + 40)], fill=LIGHT_GREEN)
        # Checkmark in circle
        font_check = get_font(40, bold=True)
        draw.text((cx - 12, cy - 22), "✓", font=font_check, fill=WHITE)

        # Title and body
        draw_text_at(draw, title, x + 110, y + 20, font_val_title, DARK_GREEN)
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw_text_at(draw, line, x + 110, y + 80 + li * 45, font_val_body, DARK_TEXT)

    # Testimonial-style section
    test_y = 1100
    draw_rounded_rect(draw, (200, test_y, W - 200, test_y + 280), 20, PALE_GREEN, outline=MED_GREEN, width=2)

    # Stars
    font_star = get_font(48)
    stars = "★ ★ ★ ★ ★"
    draw_centered_text(draw, stars, test_y + 25, font_star, GOLD)

    font_quote = get_font(34)
    draw_centered_text(draw, '"I\'ve tried so many budget apps and spreadsheets.', test_y + 95, font_quote, DARK_TEXT)
    draw_centered_text(draw, 'This is the FIRST one I\'ve actually stuck with. It just works."', test_y + 140, font_quote, DARK_TEXT)

    font_attr = get_font(28, bold=True)
    draw_centered_text(draw, "- What customers are saying about budget spreadsheets", test_y + 210, font_attr, MED_GREEN)

    # Bottom CTA section
    cta_y = 1450
    draw.rectangle([(0, cta_y), (W, H)], fill=DARK_GREEN)

    font_cta_big = get_font(60, bold=True)
    draw_centered_text(draw, "START YOUR FINANCIAL JOURNEY TODAY", cta_y + 60, font_cta_big, WHITE)

    # CTA button
    btn_w, btn_h = 700, 90
    btn_x = (W - btn_w) // 2
    btn_y = cta_y + 170
    draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), 45, GOLD)
    font_btn = get_font(40, bold=True)
    draw_centered_text(draw, "INSTANT DIGITAL DOWNLOAD", btn_y + 22, font_btn, WHITE)

    # Bottom text
    font_sm = get_font(28)
    draw_centered_text(draw, "No physical item shipped  |  Download immediately after purchase", cta_y + 300, font_sm, ACCENT_MINT)
    draw_centered_text(draw, "Lifetime access  |  Free updates", cta_y + 345, font_sm, ACCENT_MINT)

    # Bottom accent
    draw.rectangle([(0, H - 20), (W, H)], fill=GOLD)

    img.save(os.path.join(OUT_DIR, "05_value_proposition.png"), quality=95)
    print("Created: 05_value_proposition.png")


# ═══════════════════════════════════════════════════
#  GENERATE ALL IMAGES
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    create_hero_image()
    create_features_image()
    create_spreadsheet_mockup()
    create_savings_debt_image()
    create_value_prop_image()
    print(f"\nAll 5 listing images saved to: {OUT_DIR}")
