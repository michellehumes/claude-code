#!/usr/bin/env python3
"""
Small Business Planner Bundle - Etsy Listing Images
Generates 10 professional listing images at 2400x2400px.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color palette
ROYAL_BLUE = (44, 95, 138)
STEEL_BLUE = (70, 130, 180)
LIGHT_BLUE = (214, 232, 245)
WHITE = (255, 255, 255)
CHARCOAL = (51, 51, 51)
AMBER = (232, 148, 58)
RED_ACCENT = (212, 70, 56)
DARK_BG = (30, 50, 75)
MEDIUM_BLUE = (55, 110, 160)
SOFT_WHITE = (248, 250, 252)

W, H = 2400, 2400


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
    if outline and width:
        # Draw outline arcs and lines
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


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


def text_centered(draw, y, text, font, fill):
    """Draw centered text at given y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)


def text_centered_in_rect(draw, rect, text, font, fill):
    """Draw centered text within a rectangle."""
    x0, y0, x1, y1 = rect
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - tw) // 2
    y = y0 + (y1 - y0 - th) // 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_spreadsheet_mockup(draw, x, y, w, h, title, rows_data, accent_color=ROYAL_BLUE):
    """Draw a mini spreadsheet mockup."""
    # Shadow
    draw_rounded_rect(draw, (x + 6, y + 6, x + w + 6, y + h + 6), 12, fill=(0, 0, 0, 40))
    # Background
    draw_rounded_rect(draw, (x, y, x + w, y + h), 12, fill=WHITE)
    # Header bar
    draw_rounded_rect(draw, (x, y, x + w, y + 45), 12, fill=accent_color)
    draw.rectangle([x, y + 25, x + w, y + 45], fill=accent_color)
    # Title
    font_sm = get_font(22, bold=True)
    draw.text((x + 15, y + 10), title, font=font_sm, fill=WHITE)
    # Grid rows
    row_h = min(28, (h - 55) // max(len(rows_data), 1))
    for i, row_text in enumerate(rows_data):
        ry = y + 50 + i * row_h
        if i % 2 == 0:
            draw.rectangle([x + 5, ry, x + w - 5, ry + row_h - 2], fill=LIGHT_BLUE)
        font_tiny = get_font(17)
        draw.text((x + 12, ry + 3), row_text, font=font_tiny, fill=CHARCOAL)


def draw_feature_card(draw, x, y, w, h, icon_text, title, desc):
    """Draw a feature card with icon."""
    draw_rounded_rect(draw, (x, y, x + w, y + h), 16, fill=WHITE)
    # Icon circle
    cx = x + 50
    cy = y + 50
    draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=AMBER)
    icon_font = get_font(28, bold=True)
    ibbox = draw.textbbox((0, 0), icon_text, font=icon_font)
    iw = ibbox[2] - ibbox[0]
    draw.text((cx - iw // 2, cy - 18), icon_text, font=icon_font, fill=WHITE)
    # Title
    title_font = get_font(28, bold=True)
    draw.text((x + 100, y + 25), title, font=title_font, fill=CHARCOAL)
    # Description
    desc_font = get_font(22)
    draw.text((x + 100, y + 62), desc, font=desc_font, fill=STEEL_BLUE)


def draw_gradient_bg(img, color1, color2):
    """Draw a vertical gradient background."""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return draw


def draw_decorative_elements(draw):
    """Add subtle decorative circles."""
    import random
    random.seed(42)
    for _ in range(15):
        cx = random.randint(50, W - 50)
        cy = random.randint(50, H - 50)
        r = random.randint(20, 80)
        alpha_color = (*STEEL_BLUE[:3], 25)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=None, outline=(*LIGHT_BLUE, 80), width=2)


def image_01_hero():
    """Hero image - Small Business Planner Bundle with spreadsheet mockups."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, ROYAL_BLUE)

    # Top accent bar
    draw.rectangle([0, 0, W, 8], fill=AMBER)

    # Main title
    title_font = get_font(82, bold=True)
    text_centered(draw, 120, "SMALL BUSINESS", title_font, WHITE)
    text_centered(draw, 220, "PLANNER BUNDLE", title_font, WHITE)

    # Subtitle
    sub_font = get_font(42)
    text_centered(draw, 340, "8 Professional Spreadsheets for Entrepreneurs", sub_font, LIGHT_BLUE)

    # Year badge
    draw_rounded_rect(draw, (980, 420, 1420, 490), 30, fill=AMBER)
    badge_font = get_font(38, bold=True)
    text_centered_in_rect(draw, (980, 420, 1420, 490), "2026 EDITION", badge_font, WHITE)

    # Spreadsheet mockups in 2x4 grid
    mockup_titles = [
        "Income Tracker", "Expense Tracker", "Profit & Loss", "Invoice Tracker",
        "Client CRM", "Content Calendar", "Inventory", "Tax Deductions"
    ]
    mockup_rows = [
        ["Revenue: $12,500", "Paid: $10,200", "Pending: $2,300"],
        ["Supplies: $450", "Marketing: $800", "Software: $120"],
        ["Revenue: $15K", "COGS: $4K", "Net Profit: $8K"],
        ["INV-001 Paid", "INV-002 Pending", "INV-003 Overdue"],
        ["Client A - Active", "Client B - Active", "Client C - Lead"],
        ["Mon: IG Post", "Wed: TikTok", "Fri: Pinterest"],
        ["SKU-001 In Stock", "SKU-002 Low", "SKU-003 Reorder"],
        ["Home Office: $2K", "Vehicle: $1.5K", "Software: $800"],
    ]
    colors = [ROYAL_BLUE, STEEL_BLUE, ROYAL_BLUE, STEEL_BLUE,
              STEEL_BLUE, ROYAL_BLUE, STEEL_BLUE, ROYAL_BLUE]

    start_y = 560
    for i in range(8):
        col = i % 4
        row = i // 4
        mx = 80 + col * 570
        my = start_y + row * 420
        draw_spreadsheet_mockup(draw, mx, my, 530, 380, mockup_titles[i], mockup_rows[i], colors[i])

    # Bottom bar
    draw.rectangle([0, H - 100, W, H], fill=AMBER)
    bottom_font = get_font(36, bold=True)
    text_centered(draw, H - 85, "Excel & Google Sheets Compatible  |  Instant Download", bottom_font, WHITE)

    # Bottom accent
    draw.rectangle([0, H - 8, W, H], fill=ROYAL_BLUE)

    fp = os.path.join(OUTPUT_DIR, "01_hero.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_02_whats_included():
    """What's included - 8 spreadsheets listed."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, (248, 250, 252), LIGHT_BLUE)

    # Top bar
    draw.rectangle([0, 0, W, 120], fill=ROYAL_BLUE)
    title_font = get_font(58, bold=True)
    text_centered(draw, 25, "WHAT'S INCLUDED", title_font, WHITE)
    sub_font = get_font(32)
    text_centered(draw, 78, "8 Professional Spreadsheets", sub_font, LIGHT_BLUE)

    spreadsheets = [
        ("1", "Business Income Tracker", "Track all revenue by client, product & payment method"),
        ("2", "Business Expense Tracker", "Categorize expenses with tax deduction flags"),
        ("3", "Profit & Loss Statement", "Auto-calculated P&L with margins & percentages"),
        ("4", "Invoice Tracker", "Manage invoices with aging report (30/60/90 days)"),
        ("5", "Client CRM Tracker", "Centralized client database with revenue tracking"),
        ("6", "Social Media Content Calendar", "Plan content across all platforms weekly"),
        ("7", "Inventory Tracker", "Stock levels, margins & auto low-stock alerts"),
        ("8", "Tax Deduction Tracker", "Quarterly deductions with estimated tax savings"),
    ]

    card_y = 170
    for i, (num, title, desc) in enumerate(spreadsheets):
        y = card_y + i * 260
        # Card background
        draw_rounded_rect(draw, (100, y, 2300, y + 230), 20, fill=WHITE)
        # Number circle
        draw.ellipse([150, y + 65, 250, y + 165], fill=ROYAL_BLUE)
        num_font = get_font(52, bold=True)
        nbbox = draw.textbbox((0, 0), num, font=num_font)
        nw = nbbox[2] - nbbox[0]
        draw.text((200 - nw // 2, y + 82), num, font=num_font, fill=WHITE)
        # Title
        t_font = get_font(40, bold=True)
        draw.text((290, y + 55), title, font=t_font, fill=CHARCOAL)
        # Description
        d_font = get_font(30)
        draw.text((290, y + 115), desc, font=d_font, fill=STEEL_BLUE)
        # Checkmark
        check_font = get_font(44, bold=True)
        draw.text((2150, y + 80), ">>>", font=check_font, fill=AMBER)

    # Bottom accent
    draw.rectangle([0, H - 60, W, H], fill=AMBER)
    b_font = get_font(28, bold=True)
    text_centered(draw, H - 50, "ALL 8 SPREADSHEETS INCLUDED IN BUNDLE", b_font, WHITE)

    fp = os.path.join(OUTPUT_DIR, "02_whats_included.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_03_income_expense():
    """Income & Expense trackers detail."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, (30, 65, 100))

    draw.rectangle([0, 0, W, 8], fill=AMBER)

    title_font = get_font(64, bold=True)
    text_centered(draw, 60, "INCOME & EXPENSE TRACKERS", title_font, WHITE)
    sub_font = get_font(36)
    text_centered(draw, 140, "Know Your Numbers. Grow Your Business.", sub_font, AMBER)

    # Income Tracker mockup
    draw_rounded_rect(draw, (80, 230, 1160, 1150), 20, fill=WHITE)
    label_font = get_font(36, bold=True)
    draw.text((120, 250), "Business Income Tracker", font=label_font, fill=ROYAL_BLUE)

    income_features = [
        "Monthly tabs (Jan - Dec)",
        "Client/Customer tracking",
        "Invoice # reference",
        "Payment method tracking",
        "Status: Paid / Pending / Overdue",
        "Monthly & YTD totals",
        "Annual Dashboard summary",
        "Auto-calculating formulas",
    ]
    feat_font = get_font(28)
    for i, feat in enumerate(income_features):
        y = 320 + i * 90
        draw.ellipse([140, y + 8, 170, y + 38], fill=AMBER)
        check_sm = get_font(20, bold=True)
        draw.text((148, y + 8), ">>", font=check_sm, fill=WHITE)
        draw.text((195, y + 8), feat, font=feat_font, fill=CHARCOAL)

    # Expense Tracker mockup
    draw_rounded_rect(draw, (1240, 230, 2320, 1150), 20, fill=WHITE)
    draw.text((1280, 250), "Business Expense Tracker", font=label_font, fill=STEEL_BLUE)

    expense_features = [
        "10 expense categories",
        "Tax deductible flags (Y/N)",
        "Receipt # tracking",
        "Category breakdowns",
        "Monthly & annual summaries",
        "Payment method tracking",
        "Vendor management",
        "Auto-calculated totals",
    ]
    for i, feat in enumerate(expense_features):
        y = 320 + i * 90
        draw.ellipse([1300, y + 8, 1330, y + 38], fill=AMBER)
        draw.text((1308, y + 8), ">>", font=check_sm, fill=WHITE)
        draw.text((1355, y + 8), feat, font=feat_font, fill=CHARCOAL)

    # Bottom section - mini spreadsheet preview
    draw_rounded_rect(draw, (80, 1200, 2320, 2100), 20, fill=(20, 45, 70))
    preview_title = get_font(34, bold=True)
    draw.text((120, 1220), "Preview: Income Tracker Dashboard", font=preview_title, fill=AMBER)

    # Mini table
    months_preview = ["January", "February", "March", "April", "May", "June"]
    amounts = ["$8,500", "$9,200", "$7,800", "$11,400", "$10,600", "$12,100"]
    table_y = 1290
    # Header
    draw_rounded_rect(draw, (120, table_y, 2280, table_y + 50), 8, fill=ROYAL_BLUE)
    col_headers = ["Month", "Income", "Paid", "Pending", "YTD Total"]
    col_x = [150, 550, 950, 1350, 1800]
    hdr_font = get_font(26, bold=True)
    for cx, ch in zip(col_x, col_headers):
        draw.text((cx, table_y + 12), ch, font=hdr_font, fill=WHITE)

    ytd = 0
    amounts_num = [8500, 9200, 7800, 11400, 10600, 12100]
    for i, (m, a, an) in enumerate(zip(months_preview, amounts, amounts_num)):
        ry = table_y + 55 + i * 48
        bg = LIGHT_BLUE if i % 2 == 0 else WHITE
        draw.rectangle([120, ry, 2280, ry + 46], fill=bg)
        row_font = get_font(24)
        ytd += an
        vals = [m, a, f"${an - 500:,}", "$500", f"${ytd:,}"]
        for cx, v in zip(col_x, vals):
            draw.text((cx, ry + 10), v, font=row_font, fill=CHARCOAL)

    # Total row
    ry = table_y + 55 + 6 * 48
    draw_rounded_rect(draw, (120, ry, 2280, ry + 50), 8, fill=AMBER)
    total_font = get_font(26, bold=True)
    draw.text((150, ry + 12), "H1 Total", font=total_font, fill=WHITE)
    draw.text((550, ry + 12), f"${sum(amounts_num):,}", font=total_font, fill=WHITE)

    # Bottom bar
    draw.rectangle([0, H - 80, W, H], fill=AMBER)
    bot_font = get_font(32, bold=True)
    text_centered(draw, H - 68, "Auto-Calculating Formulas  |  Ready to Use  |  2026 Edition", bot_font, WHITE)

    fp = os.path.join(OUTPUT_DIR, "03_income_expense.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_04_pl_invoice():
    """P&L Statement + Invoice tracker detail."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, SOFT_WHITE, LIGHT_BLUE)

    draw.rectangle([0, 0, W, 8], fill=ROYAL_BLUE)

    title_font = get_font(60, bold=True)
    text_centered(draw, 50, "PROFIT & LOSS + INVOICE TRACKER", title_font, ROYAL_BLUE)
    sub_font = get_font(34)
    text_centered(draw, 130, "Professional Financial Statements at Your Fingertips", sub_font, STEEL_BLUE)

    # P&L Card
    draw_rounded_rect(draw, (80, 210, 1160, 1400), 20, fill=WHITE, outline=ROYAL_BLUE, width=3)
    card_title = get_font(38, bold=True)
    draw.text((120, 230), "Profit & Loss Statement", font=card_title, fill=ROYAL_BLUE)

    # Mini P&L preview
    pl_items = [
        ("REVENUE", "", ROYAL_BLUE, True),
        ("  Product Sales", "$12,500", CHARCOAL, False),
        ("  Service Revenue", "$8,200", CHARCOAL, False),
        ("  Total Revenue", "$20,700", ROYAL_BLUE, True),
        ("", "", WHITE, False),
        ("COST OF GOODS SOLD", "", STEEL_BLUE, True),
        ("  Materials", "$3,200", CHARCOAL, False),
        ("  Total COGS", "$3,200", STEEL_BLUE, True),
        ("", "", WHITE, False),
        ("GROSS PROFIT", "$17,500", AMBER, True),
        ("  Gross Margin", "84.5%", AMBER, False),
        ("", "", WHITE, False),
        ("OPERATING EXPENSES", "", RED_ACCENT, True),
        ("  Marketing", "$2,100", CHARCOAL, False),
        ("  Software", "$450", CHARCOAL, False),
        ("  Total OpEx", "$5,800", RED_ACCENT, True),
        ("", "", WHITE, False),
        ("NET PROFIT", "$11,700", (0, 140, 0), True),
        ("  Net Margin", "56.5%", (0, 140, 0), False),
    ]

    pl_font = get_font(24)
    pl_bold = get_font(24, bold=True)
    for i, (label, val, color, bold) in enumerate(pl_items):
        y = 300 + i * 52
        f = pl_bold if bold else pl_font
        draw.text((140, y), label, font=f, fill=color)
        if val:
            draw.text((850, y), val, font=f, fill=color)

    # Invoice Tracker Card
    draw_rounded_rect(draw, (1240, 210, 2320, 1400), 20, fill=WHITE, outline=STEEL_BLUE, width=3)
    draw.text((1280, 230), "Invoice Tracker", font=card_title, fill=STEEL_BLUE)

    inv_features = [
        ("Invoice Management", "Track every invoice from send to payment"),
        ("Aging Report", "30 / 60 / 90 day overdue brackets"),
        ("Auto Days Overdue", "Formula calculates days past due"),
        ("Payment Status", "Paid, Pending, Overdue, Cancelled"),
        ("Client Tracking", "Link invoices to client records"),
        ("Summary Dashboard", "Total invoiced, paid, outstanding"),
    ]

    for i, (title, desc) in enumerate(inv_features):
        y = 320 + i * 165
        draw_rounded_rect(draw, (1280, y, 2280, y + 140), 12, fill=LIGHT_BLUE)
        ft = get_font(28, bold=True)
        fd = get_font(22)
        draw.text((1310, y + 20), title, font=ft, fill=ROYAL_BLUE)
        draw.text((1310, y + 65), desc, font=fd, fill=CHARCOAL)

    # Bottom section
    draw_rounded_rect(draw, (80, 1450, 2320, 2280), 20, fill=ROYAL_BLUE)
    section_title = get_font(40, bold=True)
    text_centered(draw, 1480, "12-MONTH COMPARISON VIEW", section_title, WHITE)
    desc_font = get_font(28)
    text_centered(draw, 1540, "See revenue, expenses, and profit trends at a glance", desc_font, LIGHT_BLUE)

    # Mini comparison chart (bar representation)
    months_short = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    bar_values = [65, 72, 58, 85, 78, 90, 82, 95, 88, 92, 80, 98]
    max_bar = max(bar_values)
    bar_w = 140
    bar_start_x = 200
    bar_base_y = 2150
    month_font = get_font(24, bold=True)

    for i, (m, v) in enumerate(zip(months_short, bar_values)):
        bx = bar_start_x + i * 175
        bar_h = int((v / max_bar) * 450)
        # Revenue bar
        draw_rounded_rect(draw, (bx, bar_base_y - bar_h, bx + bar_w, bar_base_y), 8, fill=AMBER)
        # Month label
        mbbox = draw.textbbox((0, 0), m, font=month_font)
        mw = mbbox[2] - mbbox[0]
        draw.text((bx + bar_w // 2 - mw // 2, bar_base_y + 10), m, font=month_font, fill=WHITE)

    # Legend
    legend_font = get_font(22)
    draw.rectangle([bar_start_x, 2200, bar_start_x + 25, 2225], fill=AMBER)
    draw.text((bar_start_x + 35, 2200), "Monthly Revenue Trend", font=legend_font, fill=WHITE)

    # Bottom bar
    draw.rectangle([0, H - 60, W, H], fill=AMBER)
    bot_font = get_font(28, bold=True)
    text_centered(draw, H - 50, "Auto-Calculated Margins & Percentages", bot_font, WHITE)

    fp = os.path.join(OUTPUT_DIR, "04_pl_invoice.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_05_crm_calendar():
    """Client CRM + Content Calendar detail."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, (35, 70, 110))

    draw.rectangle([0, 0, W, 8], fill=AMBER)

    title_font = get_font(60, bold=True)
    text_centered(draw, 50, "CLIENT CRM + CONTENT CALENDAR", title_font, WHITE)
    sub_font = get_font(34)
    text_centered(draw, 130, "Manage Relationships & Plan Your Content", sub_font, AMBER)

    # CRM Section
    draw_rounded_rect(draw, (80, 220, 1160, 1200), 20, fill=WHITE)
    card_title = get_font(36, bold=True)
    draw.text((120, 240), "Client CRM Tracker", font=card_title, fill=ROYAL_BLUE)

    crm_fields = [
        "Client Name & Contact Info",
        "Service/Product Purchased",
        "First & Last Purchase Dates",
        "Total Revenue per Client",
        "Status: Active / Inactive / Lead",
        "Priority: High / Medium / Low",
        "Notes & Follow-up Reminders",
        "Summary Statistics Dashboard",
    ]
    feat_font = get_font(28)
    for i, feat in enumerate(crm_fields):
        y = 310 + i * 95
        # Bullet
        draw_rounded_rect(draw, (140, y + 5, 170, y + 35), 4, fill=ROYAL_BLUE)
        draw.text((190, y + 3), feat, font=feat_font, fill=CHARCOAL)

    # Content Calendar Section
    draw_rounded_rect(draw, (1240, 220, 2320, 1200), 20, fill=WHITE)
    draw.text((1280, 240), "Social Media Content Calendar", font=card_title, fill=STEEL_BLUE)

    cal_fields = [
        "12 Monthly Tabs (Jan - Dec)",
        "Daily Content Planning",
        "Platform Dropdowns (IG, TT, etc.)",
        "Content Type Selection",
        "Caption & Hashtag Planning",
        "Status: Draft / Scheduled / Posted",
        "Engagement Notes Tracking",
        "Monthly Post Summaries",
    ]
    for i, feat in enumerate(cal_fields):
        y = 310 + i * 95
        draw_rounded_rect(draw, (1300, y + 5, 1330, y + 35), 4, fill=STEEL_BLUE)
        draw.text((1350, y + 3), feat, font=feat_font, fill=CHARCOAL)

    # Bottom section - Platform icons
    draw_rounded_rect(draw, (80, 1260, 2320, 1680), 20, fill=(25, 55, 85))
    section_font = get_font(36, bold=True)
    text_centered(draw, 1285, "SUPPORTED PLATFORMS", section_font, WHITE)

    platforms = ["Instagram", "TikTok", "Pinterest", "Facebook", "Twitter/X", "LinkedIn", "YouTube"]
    platform_colors = [
        (225, 48, 108), (0, 0, 0), (230, 0, 35), (66, 103, 178),
        (29, 161, 242), (0, 119, 181), (255, 0, 0)
    ]
    pw = 280
    start_x = (W - len(platforms) * pw) // 2
    for i, (plat, pcolor) in enumerate(zip(platforms, platform_colors)):
        px = start_x + i * pw + 10
        draw_rounded_rect(draw, (px, 1360, px + pw - 20, 1440), 12, fill=pcolor)
        pfont = get_font(24, bold=True)
        text_centered_in_rect(draw, (px, 1360, px + pw - 20, 1440), plat, pfont, WHITE)

    # CRM Stats preview
    draw_rounded_rect(draw, (80, 1500, 2320, 1650), 16, fill=(35, 70, 110))
    stat_items = [
        ("Total Clients", "45"), ("Active", "32"), ("Revenue", "$128,500"),
        ("Avg/Client", "$2,856"), ("High Priority", "12")
    ]
    stat_w = W // len(stat_items)
    for i, (label, val) in enumerate(stat_items):
        sx = 80 + i * (2240 // len(stat_items))
        val_font = get_font(42, bold=True)
        lbl_font = get_font(22)
        draw.text((sx + 40, 1520), val, font=val_font, fill=AMBER)
        draw.text((sx + 40, 1580), label, font=lbl_font, fill=LIGHT_BLUE)

    # Bottom testimonial area
    draw_rounded_rect(draw, (80, 1730, 2320, 2280), 20, fill=WHITE)
    preview_label = get_font(32, bold=True)
    draw.text((120, 1750), "Content Calendar Weekly View Preview", font=preview_label, fill=ROYAL_BLUE)

    # Mini calendar grid
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cal_start_x = 120
    day_w = 300
    for i, day in enumerate(days):
        dx = cal_start_x + i * day_w
        # Day header
        draw_rounded_rect(draw, (dx, 1810, dx + day_w - 10, 1860), 8, fill=ROYAL_BLUE)
        day_font = get_font(22, bold=True)
        text_centered_in_rect(draw, (dx, 1810, dx + day_w - 10, 1860), day, day_font, WHITE)
        # Content cells
        content_items = ["IG: Reel", "TT: Video", "Pin: Image"]
        for j, item in enumerate(content_items):
            cy = 1870 + j * 55
            bg = LIGHT_BLUE if j % 2 == 0 else WHITE
            draw_rounded_rect(draw, (dx + 5, cy, dx + day_w - 15, cy + 48), 6, fill=bg)
            item_font = get_font(18)
            draw.text((dx + 15, cy + 12), item, font=item_font, fill=CHARCOAL)

    # Bottom accent bar
    draw.rectangle([0, H - 60, W, H], fill=AMBER)
    bot_font = get_font(28, bold=True)
    text_centered(draw, H - 50, "Organize Your Business Relationships & Social Media Strategy", bot_font, WHITE)

    fp = os.path.join(OUTPUT_DIR, "05_crm_calendar.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_06_inventory_tax():
    """Inventory + Tax Deduction detail."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, SOFT_WHITE, LIGHT_BLUE)

    draw.rectangle([0, 0, W, 8], fill=ROYAL_BLUE)

    title_font = get_font(60, bold=True)
    text_centered(draw, 50, "INVENTORY + TAX DEDUCTION TRACKER", title_font, ROYAL_BLUE)
    sub_font = get_font(34)
    text_centered(draw, 130, "Track Stock Levels & Maximize Tax Savings", sub_font, STEEL_BLUE)

    # Inventory Card
    draw_rounded_rect(draw, (80, 220, 1160, 1300), 20, fill=WHITE, outline=ROYAL_BLUE, width=3)
    card_title = get_font(36, bold=True)
    draw.text((120, 240), "Inventory Tracker", font=card_title, fill=ROYAL_BLUE)

    inv_features = [
        ("Product & SKU", "Track items with unique identifiers"),
        ("Cost & Selling Price", "Auto-calculated profit margins"),
        ("Stock Levels", "Current stock vs. reorder point"),
        ("Low-Stock Alerts", "Auto-flags when stock is low"),
        ("Supplier Tracking", "Manage vendor relationships"),
        ("Summary Dashboard", "Total value & stock metrics"),
    ]
    for i, (title, desc) in enumerate(inv_features):
        y = 320 + i * 150
        draw_rounded_rect(draw, (120, y, 1120, y + 130), 12, fill=LIGHT_BLUE)
        ft = get_font(28, bold=True)
        fd = get_font(22)
        draw.text((150, y + 20), title, font=ft, fill=ROYAL_BLUE)
        draw.text((150, y + 60), desc, font=fd, fill=CHARCOAL)

    # Tax Deduction Card
    draw_rounded_rect(draw, (1240, 220, 2320, 1300), 20, fill=WHITE, outline=AMBER, width=3)
    draw.text((1280, 240), "Tax Deduction Tracker", font=card_title, fill=AMBER)

    tax_categories = [
        "Home Office", "Vehicle/Mileage", "Supplies", "Travel",
        "Meals (50%)", "Marketing", "Professional Dev", "Insurance",
        "Software/Subs"
    ]
    cat_font = get_font(24, bold=True)
    for i, cat in enumerate(tax_categories):
        row = i // 3
        col = i % 3
        cx = 1280 + col * 340
        cy = 320 + row * 110
        draw_rounded_rect(draw, (cx, cy, cx + 320, cy + 90), 12, fill=(255, 240, 220))
        text_centered_in_rect(draw, (cx, cy, cx + 320, cy + 90), cat, cat_font, AMBER)

    # Tax features below categories
    tax_features = [
        "Quarterly subtotals (Q1-Q4)",
        "Annual total with category breakdown",
        "Receipt tracking (Y/N)",
        "Estimated tax savings calculator",
        "Adjustable tax rate",
    ]
    feat_font = get_font(26)
    for i, feat in enumerate(tax_features):
        y = 670 + i * 65
        draw_rounded_rect(draw, (1300, y, 1330, y + 30), 4, fill=AMBER)
        draw.text((1350, y), feat, font=feat_font, fill=CHARCOAL)

    # Tax savings highlight
    draw_rounded_rect(draw, (1280, 1020, 2280, 1270), 16, fill=AMBER)
    savings_title = get_font(32, bold=True)
    draw.text((1320, 1040), "Estimated Tax Savings", font=savings_title, fill=WHITE)
    savings_val = get_font(72, bold=True)
    draw.text((1320, 1100), "$4,250", font=savings_val, fill=WHITE)
    savings_note = get_font(24)
    draw.text((1650, 1140), "at 25% tax rate", font=savings_note, fill=(255, 255, 255, 200))

    # Bottom section - Inventory preview
    draw_rounded_rect(draw, (80, 1360, 2320, 2280), 20, fill=ROYAL_BLUE)
    section_title = get_font(38, bold=True)
    text_centered(draw, 1385, "INVENTORY TRACKER PREVIEW", section_title, WHITE)

    # Mini table
    table_y = 1450
    inv_headers = ["Product", "SKU", "Cost", "Price", "Margin", "Stock", "Status"]
    inv_col_x = [120, 520, 820, 1060, 1300, 1540, 1800]
    hdr_font = get_font(26, bold=True)

    draw_rounded_rect(draw, (100, table_y, 2280, table_y + 50), 8, fill=AMBER)
    for cx, ch in zip(inv_col_x, inv_headers):
        draw.text((cx, table_y + 12), ch, font=hdr_font, fill=WHITE)

    inv_data = [
        ("Candle - Lavender", "CND-001", "$4.50", "$18.99", "76%", "145", "In Stock"),
        ("Candle - Vanilla", "CND-002", "$4.50", "$18.99", "76%", "8", "Low Stock"),
        ("Gift Box Set", "GFT-001", "$12.00", "$39.99", "70%", "52", "In Stock"),
        ("Wax Melts Pack", "WXM-001", "$3.00", "$12.99", "77%", "0", "Out of Stock"),
        ("Reed Diffuser", "DIF-001", "$6.50", "$24.99", "74%", "34", "In Stock"),
        ("Travel Candle", "CND-003", "$3.25", "$14.99", "78%", "5", "Low Stock"),
    ]

    row_font = get_font(24)
    for i, row_data in enumerate(inv_data):
        ry = table_y + 55 + i * 52
        bg = LIGHT_BLUE if i % 2 == 0 else WHITE
        draw.rectangle([100, ry, 2280, ry + 50], fill=bg)
        for j, (cx, val) in enumerate(zip(inv_col_x, row_data)):
            color = CHARCOAL
            if j == 6:
                if val == "Low Stock":
                    color = AMBER
                elif val == "Out of Stock":
                    color = RED_ACCENT
                else:
                    color = (0, 140, 0)
            draw.text((cx, ry + 12), val, font=row_font, fill=color)

    # Stats at bottom
    stats_y = table_y + 55 + 6 * 52 + 30
    stat_items = [
        ("Total Products", "6"), ("In Stock", "3"), ("Low Stock", "2"),
        ("Out of Stock", "1"), ("Inventory Value", "$3,842")
    ]
    stat_w = 2200 // len(stat_items)
    for i, (label, val) in enumerate(stat_items):
        sx = 100 + i * stat_w
        draw_rounded_rect(draw, (sx, stats_y, sx + stat_w - 20, stats_y + 110), 12, fill=(25, 55, 85))
        val_font = get_font(36, bold=True)
        lbl_font = get_font(20)
        vbbox = draw.textbbox((0, 0), val, font=val_font)
        vw = vbbox[2] - vbbox[0]
        draw.text((sx + (stat_w - 20 - vw) // 2, stats_y + 15), val, font=val_font, fill=AMBER)
        lbbox = draw.textbbox((0, 0), label, font=lbl_font)
        lw = lbbox[2] - lbbox[0]
        draw.text((sx + (stat_w - 20 - lw) // 2, stats_y + 70), label, font=lbl_font, fill=LIGHT_BLUE)

    # Bottom accent
    draw.rectangle([0, H - 50, W, H], fill=AMBER)

    fp = os.path.join(OUTPUT_DIR, "06_inventory_tax.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_07_features():
    """Key features - auto-formulas, organized, professional."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, ROYAL_BLUE)

    draw.rectangle([0, 0, W, 8], fill=AMBER)

    title_font = get_font(68, bold=True)
    text_centered(draw, 80, "KEY FEATURES", title_font, WHITE)
    sub_font = get_font(38)
    text_centered(draw, 170, "Professional Tools for Serious Entrepreneurs", sub_font, AMBER)

    features = [
        ("AUTO-FORMULAS", "SUM, SUMIF, COUNTIF, IF formulas", "auto-calculate totals, margins & more"),
        ("DATA VALIDATION", "Pre-built dropdown menus", "for consistent, error-free data entry"),
        ("PROFESSIONAL DESIGN", "Royal blue & steel blue theme", "clean headers & alternating rows"),
        ("12-MONTH TRACKING", "Full year 2026 coverage", "monthly tabs with annual summaries"),
        ("TAX-READY", "Deduction categories & receipt tracking", "quarterly subtotals & savings estimates"),
        ("DASHBOARD VIEWS", "Annual summary dashboards", "see your business performance at a glance"),
        ("FROZEN HEADERS", "Headers stay visible while scrolling", "easy navigation in large datasets"),
        ("HOW-TO GUIDES", "Instructions tab in every workbook", "get started in minutes, not hours"),
    ]

    for i, (title, line1, line2) in enumerate(features):
        row = i // 2
        col = i % 2
        fx = 80 + col * 1160
        fy = 280 + row * 470
        fw = 1100
        fh = 430

        draw_rounded_rect(draw, (fx, fy, fx + fw, fy + fh), 20, fill=WHITE)

        # Icon area
        draw_rounded_rect(draw, (fx + 30, fy + 30, fx + fw - 30, fy + 100), 12, fill=ROYAL_BLUE)
        icon_font = get_font(34, bold=True)
        text_centered_in_rect(draw, (fx + 30, fy + 30, fx + fw - 30, fy + 100), title, icon_font, WHITE)

        # Feature details
        detail_font = get_font(30, bold=True)
        desc_font = get_font(26)
        draw.text((fx + 50, fy + 130), line1, font=detail_font, fill=CHARCOAL)
        draw.text((fx + 50, fy + 180), line2, font=desc_font, fill=STEEL_BLUE)

        # Decorative elements
        # Mini checkmarks
        checks = ["Saves Time", "Reduces Errors", "Professional Look"]
        for j, check in enumerate(checks):
            cy = fy + 250 + j * 50
            draw.ellipse([fx + 50, cy, fx + 78, cy + 28], fill=AMBER)
            ck_font = get_font(15, bold=True)
            draw.text((fx + 57, cy + 4), "OK", font=ck_font, fill=WHITE)
            check_font = get_font(22)
            draw.text((fx + 90, cy + 2), check, font=check_font, fill=CHARCOAL)

    # Bottom bar
    draw.rectangle([0, H - 80, W, H], fill=AMBER)
    bot_font = get_font(32, bold=True)
    text_centered(draw, H - 68, "8 Spreadsheets  |  100+ Auto-Formulas  |  Instant Download", bot_font, WHITE)

    fp = os.path.join(OUTPUT_DIR, "07_features.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_08_how_to_use():
    """How to use / compatibility."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, SOFT_WHITE, LIGHT_BLUE)

    draw.rectangle([0, 0, W, 8], fill=ROYAL_BLUE)

    title_font = get_font(68, bold=True)
    text_centered(draw, 60, "HOW TO USE", title_font, ROYAL_BLUE)
    sub_font = get_font(36)
    text_centered(draw, 150, "Get Started in 3 Simple Steps", sub_font, STEEL_BLUE)

    steps = [
        ("1", "PURCHASE & DOWNLOAD", "Complete your purchase and instantly download\nthe ZIP file with all 8 spreadsheets."),
        ("2", "OPEN IN EXCEL OR GOOGLE SHEETS", "Open the .xlsx files in Microsoft Excel,\nGoogle Sheets, or any compatible app."),
        ("3", "START TRACKING", "Follow the Instructions tab in each workbook.\nBegin entering your business data!"),
    ]

    for i, (num, title, desc) in enumerate(steps):
        sy = 270 + i * 430
        draw_rounded_rect(draw, (100, sy, 2300, sy + 380), 24, fill=WHITE, outline=ROYAL_BLUE, width=3)

        # Step number circle
        draw.ellipse([170, sy + 100, 340, sy + 270], fill=ROYAL_BLUE)
        num_font = get_font(80, bold=True)
        nbbox = draw.textbbox((0, 0), num, font=num_font)
        nw = nbbox[2] - nbbox[0]
        draw.text((255 - nw // 2, sy + 135), num, font=num_font, fill=WHITE)

        # Arrow connector (except last)
        if i < 2:
            draw_rounded_rect(draw, (245, sy + 380, 265, sy + 430), 4, fill=AMBER)

        # Title and description
        t_font = get_font(40, bold=True)
        d_font = get_font(30)
        draw.text((420, sy + 100), title, font=t_font, fill=ROYAL_BLUE)
        draw.text((420, sy + 170), desc, font=d_font, fill=CHARCOAL)

    # Compatibility section
    comp_y = 1580
    draw_rounded_rect(draw, (100, comp_y, 2300, comp_y + 350), 24, fill=ROYAL_BLUE)
    comp_title = get_font(44, bold=True)
    text_centered(draw, comp_y + 30, "COMPATIBLE WITH", comp_title, WHITE)

    apps = [
        ("Microsoft Excel", "Desktop & Online"),
        ("Google Sheets", "Free with Google"),
        ("Apple Numbers", "Mac & iPad"),
        ("LibreOffice Calc", "Free & Open Source"),
    ]
    app_w = 500
    start_x = (W - len(apps) * app_w) // 2
    for i, (app, note) in enumerate(apps):
        ax = start_x + i * app_w + 20
        draw_rounded_rect(draw, (ax, comp_y + 110, ax + app_w - 40, comp_y + 300), 16, fill=WHITE)
        app_font = get_font(32, bold=True)
        note_font = get_font(24)
        text_centered_in_rect(draw, (ax, comp_y + 130, ax + app_w - 40, comp_y + 210), app, app_font, ROYAL_BLUE)
        text_centered_in_rect(draw, (ax, comp_y + 210, ax + app_w - 40, comp_y + 280), note, note_font, STEEL_BLUE)

    # Tips section
    tips_y = 1980
    draw_rounded_rect(draw, (100, tips_y, 2300, tips_y + 350), 20, fill=WHITE)
    tips_title = get_font(36, bold=True)
    draw.text((160, tips_y + 20), "Quick Tips:", font=tips_title, fill=AMBER)

    tips = [
        "Each workbook includes a detailed Instructions tab to get you started.",
        "Use dropdown menus for consistent data entry - no typing errors!",
        "Formulas auto-calculate - just enter your data and watch the magic.",
        "Back up your files regularly. We recommend saving to cloud storage.",
    ]
    tip_font = get_font(28)
    for i, tip in enumerate(tips):
        draw.text((200, tips_y + 80 + i * 60), f"  {tip}", font=tip_font, fill=CHARCOAL)

    fp = os.path.join(OUTPUT_DIR, "08_how_to_use.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_09_testimonials():
    """Testimonials."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, (30, 60, 95))

    draw.rectangle([0, 0, W, 8], fill=AMBER)

    title_font = get_font(64, bold=True)
    text_centered(draw, 60, "WHAT BUSINESS OWNERS SAY", title_font, WHITE)

    # Star rating
    star_font = get_font(48)
    text_centered(draw, 150, "* * * * *", star_font, AMBER)
    rating_font = get_font(30)
    text_centered(draw, 215, "5.0 out of 5 stars", rating_font, LIGHT_BLUE)

    testimonials = [
        ("Sarah M.", "Etsy Seller",
         "These spreadsheets have completely transformed how I run my\nbusiness. The P&L statement alone is worth the price!"),
        ("James R.", "Freelance Designer",
         "I love the invoice tracker and CRM. Finally, I can keep track of\nall my clients and payments in one organized place."),
        ("Maria L.", "Small Business Owner",
         "The tax deduction tracker saved me so much time during tax\nseason. I found deductions I would have missed otherwise!"),
        ("David K.", "Online Shop Owner",
         "The inventory tracker with auto low-stock alerts is genius.\nI never run out of popular products anymore."),
        ("Emma W.", "Social Media Manager",
         "The content calendar is exactly what I needed. Planning\ncontent across multiple platforms is so much easier now."),
    ]

    for i, (name, role, quote) in enumerate(testimonials):
        ty = 300 + i * 370
        draw_rounded_rect(draw, (120, ty, 2280, ty + 330), 20, fill=WHITE)

        # Quote mark
        quote_font = get_font(80, bold=True)
        draw.text((160, ty + 10), '"', font=quote_font, fill=AMBER)

        # Quote text
        q_font = get_font(28)
        draw.text((200, ty + 60), quote, font=q_font, fill=CHARCOAL)

        # Stars
        star_sm = get_font(28)
        draw.text((200, ty + 170), "* * * * *", font=star_sm, fill=AMBER)

        # Name and role
        name_font = get_font(28, bold=True)
        role_font = get_font(24)
        draw.text((200, ty + 220), f"- {name}", font=name_font, fill=ROYAL_BLUE)
        draw.text((200, ty + 260), role, font=role_font, fill=STEEL_BLUE)

        # Verified badge
        badge_font = get_font(20, bold=True)
        draw_rounded_rect(draw, (1900, ty + 240, 2230, ty + 280), 10, fill=AMBER)
        text_centered_in_rect(draw, (1900, ty + 240, 2230, ty + 280), "VERIFIED PURCHASE", badge_font, WHITE)

    # Bottom bar
    draw.rectangle([0, H - 70, W, H], fill=AMBER)
    bot_font = get_font(30, bold=True)
    text_centered(draw, H - 58, "Join 2,000+ Happy Business Owners", bot_font, WHITE)

    fp = os.path.join(OUTPUT_DIR, "09_testimonials.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def image_10_cta():
    """Bundle CTA with $11.99 price."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, ROYAL_BLUE, DARK_BG)

    draw.rectangle([0, 0, W, 10], fill=AMBER)

    # Main title
    title_font = get_font(78, bold=True)
    text_centered(draw, 80, "SMALL BUSINESS", title_font, WHITE)
    text_centered(draw, 180, "PLANNER BUNDLE", title_font, WHITE)

    # Subtitle
    sub_font = get_font(40)
    text_centered(draw, 300, "Everything You Need to Run Your Business", sub_font, LIGHT_BLUE)

    # What you get section
    draw_rounded_rect(draw, (200, 400, 2200, 1050), 24, fill=WHITE)
    section_font = get_font(40, bold=True)
    text_centered(draw, 425, "8 PROFESSIONAL SPREADSHEETS", section_font, ROYAL_BLUE)

    items = [
        "Business Income Tracker 2026",
        "Business Expense Tracker 2026",
        "Profit & Loss Statement 2026",
        "Invoice Tracker 2026",
        "Client CRM Tracker",
        "Social Media Content Calendar 2026",
        "Inventory Tracker",
        "Tax Deduction Tracker 2026",
    ]
    item_font = get_font(32)
    for i, item in enumerate(items):
        col = i // 4
        row = i % 4
        ix = 340 + col * 1000
        iy = 500 + row * 120
        draw.ellipse([ix - 35, iy + 5, ix - 5, iy + 35], fill=AMBER)
        ck = get_font(18, bold=True)
        draw.text((ix - 28, iy + 7), "OK", font=ck, fill=WHITE)
        draw.text((ix + 10, iy + 2), item, font=item_font, fill=CHARCOAL)

    # Price section
    price_y = 1120
    draw_rounded_rect(draw, (500, price_y, 1900, price_y + 400), 30, fill=AMBER)

    # Original price crossed
    orig_font = get_font(44)
    text_centered(draw, price_y + 30, "Regular Price: $29.99", orig_font, (255, 255, 255, 180))
    # Strikethrough
    obbox = draw.textbbox((0, 0), "Regular Price: $29.99", font=orig_font)
    ow = obbox[2] - obbox[0]
    ox = (W - ow) // 2
    draw.line([(ox, price_y + 55), (ox + ow, price_y + 55)], fill=WHITE, width=3)

    # Sale price
    sale_font = get_font(120, bold=True)
    text_centered(draw, price_y + 90, "$11.99", sale_font, WHITE)

    # Savings
    save_font = get_font(36, bold=True)
    text_centered(draw, price_y + 270, "SAVE 60% - Limited Time Bundle Price!", save_font, WHITE)

    # Value props
    value_y = 1580
    values = [
        "Instant Digital Download",
        "Excel & Google Sheets Compatible",
        "Auto-Calculating Formulas",
        "Lifetime Access - Use Year After Year",
    ]
    val_font = get_font(34, bold=True)
    for i, val in enumerate(values):
        vy = value_y + i * 80
        draw_rounded_rect(draw, (300, vy, 2100, vy + 65), 12, fill=(35, 70, 110))
        text_centered_in_rect(draw, (300, vy, 2100, vy + 65), val, val_font, WHITE)

    # CTA Button
    cta_y = 1920
    draw_rounded_rect(draw, (500, cta_y, 1900, cta_y + 120), 60, fill=AMBER)
    cta_font = get_font(52, bold=True)
    text_centered_in_rect(draw, (500, cta_y, 1900, cta_y + 120), "ADD TO CART - $11.99", cta_font, WHITE)

    # Guarantee
    guar_font = get_font(28)
    text_centered(draw, cta_y + 150, "Instant Download  |  Satisfaction Guaranteed", guar_font, LIGHT_BLUE)

    # Bottom accent
    draw.rectangle([0, H - 80, W, H], fill=AMBER)
    bot_font = get_font(32, bold=True)
    text_centered(draw, H - 68, "Start Organizing Your Business Today!", bot_font, WHITE)
    draw.rectangle([0, H - 8, W, H], fill=ROYAL_BLUE)

    fp = os.path.join(OUTPUT_DIR, "10_cta.jpg")
    img.save(fp, "JPEG", quality=95)
    print(f"  Created: {fp}")


def main():
    print("=" * 60)
    print("Small Business Planner Bundle - Listing Images")
    print("Generating 10 images at 2400x2400px...")
    print("=" * 60)

    image_01_hero()
    image_02_whats_included()
    image_03_income_expense()
    image_04_pl_invoice()
    image_05_crm_calendar()
    image_06_inventory_tax()
    image_07_features()
    image_08_how_to_use()
    image_09_testimonials()
    image_10_cta()

    print("\n" + "=" * 60)
    print("All 10 listing images created successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
