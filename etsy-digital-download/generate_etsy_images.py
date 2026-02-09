#!/usr/bin/env python3
"""
Generate 5 professional Etsy listing images for
"Complete Budget & Finance Bundle 2026"
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

# ── Output ────────────────────────────────────────────────────────────
OUT = "/home/user/claude-code/etsy-digital-download/images"
os.makedirs(OUT, exist_ok=True)

# ── Dimensions ────────────────────────────────────────────────────────
W, H = 2700, 2025

# ── Color palette ─────────────────────────────────────────────────────
DARK_GREEN   = (27, 67, 50)
MED_GREEN    = (45, 106, 79)
LIGHT_GREEN  = (82, 183, 136)
PALE_GREEN   = (216, 243, 220)
WHITE        = (255, 255, 255)
DARK_TEXT     = (33, 33, 33)
LIGHT_GRAY   = (245, 245, 245)
GOLD         = (197, 165, 90)
RED_OVER     = (200, 60, 60)
GREEN_UNDER  = (40, 160, 90)
BEZEL_BLACK  = (30, 30, 30)
SCREEN_BG    = (250, 252, 250)
TAB_BG       = (235, 245, 238)

# ── Fonts ─────────────────────────────────────────────────────────────
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(bold=False, size=32):
    return ImageFont.truetype(BOLD if bold else REG, size)

# ── Helpers ───────────────────────────────────────────────────────────

def gradient_bg(w, h, top_color, bot_color):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(top_color[0] + (bot_color[0] - top_color[0]) * y / h)
        g = int(top_color[1] + (bot_color[1] - top_color[1]) * y / h)
        b = int(top_color[2] + (bot_color[2] - top_color[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def add_dots_pattern(draw, w, h, color, spacing=48, radius=2):
    for x in range(0, w, spacing):
        for y in range(0, h, spacing):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                         fill=color)


def rounded_rect(draw, bbox, radius, fill, outline=None, width=0):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)


def draw_ipad(img, x, y, w, h, screen_img=None):
    draw = ImageDraw.Draw(img)
    bezel = int(w * 0.03)
    corner = int(w * 0.04)

    # Shadow layers
    for s in range(18, 0, -1):
        sv = max(0, 200 - s * 12)
        rounded_rect(draw,
                     (x + s + 4, y + s + 6, x + w + s + 4, y + h + s + 6),
                     corner + 4, fill=(sv, sv, sv))

    # Body
    rounded_rect(draw, (x, y, x + w, y + h), corner, fill=BEZEL_BLACK)

    # Screen area
    sx, sy = x + bezel, y + bezel
    sw, sh = w - 2 * bezel, h - 2 * bezel
    screen_corner = max(4, corner - bezel)

    if screen_img:
        resized = screen_img.resize((sw, sh), Image.LANCZOS)
        mask = Image.new("L", (sw, sh), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([0, 0, sw, sh], radius=screen_corner, fill=255)
        img.paste(resized, (sx, sy), mask)
    else:
        rounded_rect(draw, (sx, sy, sx + sw, sy + sh), screen_corner, fill=SCREEN_BG)

    # Camera dot
    cam_r = max(4, int(w * 0.006))
    cam_x = x + w // 2
    cam_y = y + bezel // 2
    draw.ellipse([cam_x - cam_r, cam_y - cam_r, cam_x + cam_r, cam_y + cam_r],
                 fill=(50, 50, 55))

    return sx, sy, sw, sh


def draw_pill(draw, cx, cy, text, bg, fg, fnt, pad_x=28, pad_y=12):
    bb = fnt.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    rx = tw + pad_x * 2
    ry = th + pad_y * 2
    x0 = cx - rx // 2
    y0 = cy - ry // 2
    rounded_rect(draw, (x0, y0, x0 + rx, y0 + ry), ry // 2, fill=bg)
    draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=fg, font=fnt)
    return (x0, y0, x0 + rx, y0 + ry)


def draw_annotation(draw, label, lx, ly, tx, ty, color=GOLD):
    fnt = font(True, 22)
    bb = fnt.getbbox(label)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 10
    rounded_rect(draw, (tx - pad, ty - pad, tx + tw + pad, ty + th + pad),
                  6, fill=color)
    draw.text((tx, ty), label, fill=WHITE, font=fnt)
    draw.line([(lx, ly), (tx + tw // 2, ty + th + pad)], fill=color, width=3)
    draw.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=color)


def centered_text(draw, y, text, fnt, fill, w=W):
    bb = fnt.getbbox(text)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) // 2, y), text, fill=fill, font=fnt)


# ── Screen creators for each tab ─────────────────────────────────────

def create_budget_screen(sw, sh):
    scr = Image.new("RGB", (sw, sh), SCREEN_BG)
    d = ImageDraw.Draw(scr)

    # Toolbar
    d.rectangle([0, 0, sw, 50], fill=MED_GREEN)
    d.text((20, 12), "Complete Budget & Finance Bundle 2026", fill=WHITE, font=font(True, 22))

    # Tab bar
    tab_y = 52
    d.rectangle([0, tab_y, sw, tab_y + 36], fill=(230, 240, 232))
    tabs = ["Monthly Budget", "Expense Tracker", "Savings Goals",
            "Debt Payoff", "Net Worth", "Annual Overview", "How to Use"]
    tx = 10
    for i, t in enumerate(tabs):
        tf = font(True if i == 0 else False, 13)
        bb = tf.getbbox(t)
        twidth = bb[2] - bb[0]
        bg = WHITE if i == 0 else (230, 240, 232)
        border = LIGHT_GREEN if i == 0 else (200, 210, 200)
        d.rectangle([tx, tab_y + 4, tx + twidth + 16, tab_y + 32], fill=bg, outline=border)
        d.text((tx + 8, tab_y + 8), t, fill=DARK_GREEN if i == 0 else (100, 100, 100), font=tf)
        tx += twidth + 22

    # Title
    title_y = 100
    d.text((30, title_y), "MONTHLY BUDGET \u2014 JANUARY 2026", fill=DARK_GREEN, font=font(True, 24))

    # Summary box (right side)
    sb_x, sb_y = sw - 310, title_y - 8
    rounded_rect(d, (sb_x, sb_y, sw - 16, sb_y + 160), 10, fill=DARK_GREEN)
    d.text((sb_x + 16, sb_y + 10), "BUDGET SUMMARY", fill=GOLD, font=font(True, 16))
    summary = [
        ("Total Income", "$5,200.00"),
        ("Total Expenses", "$3,920.00"),
        ("Net Balance", "$1,280.00"),
        ("Savings Rate", "24.6%"),
    ]
    for i, (k, v) in enumerate(summary):
        yy = sb_y + 38 + i * 28
        d.text((sb_x + 16, yy), k, fill=(180, 220, 200), font=font(False, 15))
        d.text((sb_x + 200, yy), v, fill=WHITE, font=font(True, 15))

    # Budget grid
    grid_y = title_y + 50
    cols = [30, 220, 370, 510, 630]
    headers = ["CATEGORY", "BUDGETED", "ACTUAL", "DIFFERENCE", "STATUS"]
    hdr_font = font(True, 16)
    d.rectangle([20, grid_y, sw - 330, grid_y + 32], fill=MED_GREEN)
    for ci, hdr in enumerate(headers):
        d.text((cols[ci], grid_y + 7), hdr, fill=WHITE, font=hdr_font)

    rows = [
        ("Housing / Rent",    "$1,500", "$1,500", "$0",    "exact"),
        ("Utilities",         "$200",   "$185",   "+$15",  "under"),
        ("Groceries",         "$600",   "$542",   "+$58",  "under"),
        ("Transportation",    "$350",   "$310",   "+$40",  "under"),
        ("Insurance",         "$180",   "$180",   "$0",    "exact"),
        ("Phone & Internet",  "$120",   "$118",   "+$2",   "under"),
        ("Dining Out",        "$200",   "$265",   "-$65",  "over"),
        ("Entertainment",     "$150",   "$130",   "+$20",  "under"),
        ("Subscriptions",     "$60",    "$60",    "$0",    "exact"),
        ("Clothing",          "$100",   "$45",    "+$55",  "under"),
        ("Personal Care",     "$80",    "$72",    "+$8",   "under"),
        ("Health / Medical",  "$100",   "$100",   "$0",    "exact"),
        ("Pet Expenses",      "$50",    "$63",    "-$13",  "over"),
        ("Gifts / Donations", "$80",    "$80",    "$0",    "exact"),
        ("Education",         "$50",    "$30",    "+$20",  "under"),
        ("Miscellaneous",     "$100",   "$40",    "+$60",  "under"),
    ]
    rf = font(False, 14)
    for ri, (cat, bud, act, diff, status) in enumerate(rows):
        ry = grid_y + 34 + ri * 26
        bg = WHITE if ri % 2 == 0 else (242, 248, 244)
        d.rectangle([20, ry, sw - 330, ry + 26], fill=bg)
        d.text((cols[0], ry + 5), cat, fill=DARK_TEXT, font=rf)
        d.text((cols[1], ry + 5), bud, fill=DARK_TEXT, font=rf)
        d.text((cols[2], ry + 5), act, fill=DARK_TEXT, font=rf)
        diff_color = GREEN_UNDER if status == "under" else RED_OVER if status == "over" else DARK_TEXT
        d.text((cols[3], ry + 5), diff, fill=diff_color, font=font(True, 14))
        dot_color = GREEN_UNDER if status in ("under", "exact") else RED_OVER
        cx_dot = cols[4] + 30
        d.ellipse([cx_dot - 6, ry + 8, cx_dot + 6, ry + 20], fill=dot_color)

    # Pie chart
    pie_cx, pie_cy = sw - 165, sb_y + 290
    pie_r = 110
    slices = [
        (0,   100, MED_GREEN),
        (100, 135, LIGHT_GREEN),
        (135, 165, GOLD),
        (165, 210, (100, 180, 140)),
        (210, 240, (70, 130, 100)),
        (240, 280, PALE_GREEN),
        (280, 360, (150, 200, 170)),
    ]
    for start, end, color in slices:
        d.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r],
                    start - 90, end - 90, fill=color, outline=WHITE, width=2)
    inner_r = 50
    d.ellipse([pie_cx - inner_r, pie_cy - inner_r, pie_cx + inner_r, pie_cy + inner_r],
               fill=SCREEN_BG)
    d.text((pie_cx - 30, pie_cy - 12), "$3,920", fill=DARK_GREEN, font=font(True, 16))

    leg_y = pie_cy + pie_r + 16
    legend_items = [("Housing 38%", MED_GREEN), ("Groceries 14%", LIGHT_GREEN),
                    ("Transport 9%", GOLD), ("Other 39%", (150, 200, 170))]
    for li, (lt, lc) in enumerate(legend_items):
        lx = sw - 300 + (li % 2) * 140
        ly2 = leg_y + (li // 2) * 22
        d.rectangle([lx, ly2, lx + 12, ly2 + 12], fill=lc)
        d.text((lx + 18, ly2 - 2), lt, fill=DARK_TEXT, font=font(False, 12))

    return scr


def create_expense_screen(sw, sh):
    scr = Image.new("RGB", (sw, sh), SCREEN_BG)
    d = ImageDraw.Draw(scr)
    d.rectangle([0, 0, sw, 44], fill=MED_GREEN)
    d.text((16, 10), "Expense Tracker \u2014 January 2026", fill=WHITE, font=font(True, 18))

    headers = ["DATE", "DESCRIPTION", "CATEGORY", "AMOUNT", "PAYMENT"]
    col_x = [16, 110, 310, 450, 560]
    d.rectangle([8, 54, sw - 8, 82], fill=DARK_GREEN)
    hf = font(True, 14)
    for i, h in enumerate(headers):
        d.text((col_x[i], 60), h, fill=WHITE, font=hf)

    entries = [
        ("01/02", "Whole Foods Market", "Groceries", "$87.42", "Debit"),
        ("01/02", "Shell Gas Station", "Transport", "$45.00", "Credit"),
        ("01/03", "Netflix Monthly", "Subscriptions", "$15.99", "Credit"),
        ("01/04", "Trader Joe's", "Groceries", "$62.15", "Debit"),
        ("01/05", "Electric Company", "Utilities", "$95.40", "Auto-Pay"),
        ("01/05", "Water Bill", "Utilities", "$42.00", "Auto-Pay"),
        ("01/06", "Target", "Household", "$34.87", "Debit"),
        ("01/07", "Starbucks", "Dining Out", "$6.45", "Credit"),
        ("01/07", "Amazon Prime", "Subscriptions", "$14.99", "Credit"),
        ("01/08", "Costco", "Groceries", "$156.23", "Debit"),
        ("01/09", "Uber Ride", "Transport", "$18.50", "Credit"),
        ("01/10", "Chipotle", "Dining Out", "$12.85", "Credit"),
        ("01/10", "Gym Membership", "Health", "$49.99", "Auto-Pay"),
        ("01/11", "CVS Pharmacy", "Health", "$22.40", "Debit"),
        ("01/12", "Movie Tickets", "Entertainment", "$28.00", "Credit"),
        ("01/13", "Spotify", "Subscriptions", "$9.99", "Credit"),
        ("01/14", "Kroger", "Groceries", "$73.90", "Debit"),
    ]
    rf = font(False, 13)
    for ri, (date, desc, cat, amt, pay) in enumerate(entries):
        ry = 86 + ri * 25
        bg = WHITE if ri % 2 == 0 else (244, 249, 245)
        d.rectangle([8, ry, sw - 8, ry + 25], fill=bg)
        d.text((col_x[0], ry + 5), date, fill=DARK_TEXT, font=rf)
        d.text((col_x[1], ry + 5), desc, fill=DARK_TEXT, font=rf)
        d.text((col_x[2], ry + 5), cat, fill=MED_GREEN, font=rf)
        d.text((col_x[3], ry + 5), amt, fill=DARK_TEXT, font=font(True, 13))
        d.text((col_x[4], ry + 5), pay, fill=(120, 120, 120), font=rf)

    ty = 86 + len(entries) * 25 + 8
    d.rectangle([8, ty, sw - 8, ty + 30], fill=DARK_GREEN)
    d.text((col_x[0], ty + 6), "JANUARY TOTAL", fill=WHITE, font=font(True, 14))
    d.text((col_x[3], ty + 6), "$776.13", fill=GOLD, font=font(True, 14))
    return scr


def create_savings_screen(sw, sh):
    scr = Image.new("RGB", (sw, sh), SCREEN_BG)
    d = ImageDraw.Draw(scr)
    d.rectangle([0, 0, sw, 44], fill=MED_GREEN)
    d.text((16, 10), "Savings Goals Tracker", fill=WHITE, font=font(True, 18))

    goals = [
        ("Emergency Fund",    7500, 10000, LIGHT_GREEN),
        ("Vacation Fund",     1800, 3000,  GOLD),
        ("New Car",           4500, 15000, MED_GREEN),
        ("Home Down Payment", 12000, 50000, DARK_GREEN),
        ("Wedding Fund",      3200, 8000,  (100, 180, 140)),
        ("Education Fund",    800,  5000,  (70, 150, 120)),
        ("Holiday Gifts",     200,  600,   LIGHT_GREEN),
        ("Tech Upgrade",      350,  1200,  GOLD),
    ]

    y = 60
    for name, current, target, color in goals:
        pct = current / target
        d.text((20, y), name, fill=DARK_TEXT, font=font(True, 16))
        d.text((20, y + 22), f"${current:,.0f} of ${target:,.0f}", fill=(100,100,100), font=font(False, 13))
        pct_text = f"{pct*100:.0f}%"
        d.text((sw - 70, y + 8), pct_text, fill=color, font=font(True, 18))
        bar_y = y + 44
        bar_w = sw - 40
        rounded_rect(d, (20, bar_y, 20 + bar_w, bar_y + 16), 8, fill=(220, 230, 222))
        if pct > 0:
            fill_w = max(16, int(bar_w * pct))
            rounded_rect(d, (20, bar_y, 20 + fill_w, bar_y + 16), 8, fill=color)
        y += 70
    return scr


def create_debt_screen(sw, sh):
    scr = Image.new("RGB", (sw, sh), SCREEN_BG)
    d = ImageDraw.Draw(scr)
    d.rectangle([0, 0, sw, 44], fill=MED_GREEN)
    d.text((16, 10), "Debt Payoff Planner", fill=WHITE, font=font(True, 18))

    headers = ["DEBT NAME", "BALANCE", "APR", "MIN PMT", "PAYOFF"]
    cx = [16, 180, 300, 390, 500]
    d.rectangle([8, 54, sw - 8, 82], fill=DARK_GREEN)
    for i, h in enumerate(headers):
        d.text((cx[i], 60), h, fill=WHITE, font=font(True, 13))

    debts = [
        ("Student Loan",   "$18,400", "5.5%",  "$210", "Mar 2032"),
        ("Credit Card #1", "$3,200",  "19.9%", "$95",  "Aug 2027"),
        ("Credit Card #2", "$1,450",  "22.4%", "$45",  "Jan 2028"),
        ("Car Loan",       "$8,900",  "4.2%",  "$320", "Jun 2027"),
        ("Medical Bill",   "$850",    "0.0%",  "$85",  "Oct 2026"),
        ("Personal Loan",  "$2,100",  "8.5%",  "$125", "Apr 2027"),
    ]
    rf = font(False, 13)
    for ri, (name, bal, apr, pmt, payoff) in enumerate(debts):
        ry = 88 + ri * 30
        bg = WHITE if ri % 2 == 0 else (244, 249, 245)
        d.rectangle([8, ry, sw - 8, ry + 30], fill=bg)
        d.text((cx[0], ry + 7), name, fill=DARK_TEXT, font=rf)
        d.text((cx[1], ry + 7), bal, fill=RED_OVER, font=font(True, 13))
        d.text((cx[2], ry + 7), apr, fill=DARK_TEXT, font=rf)
        d.text((cx[3], ry + 7), pmt, fill=DARK_TEXT, font=rf)
        d.text((cx[4], ry + 7), payoff, fill=MED_GREEN, font=font(True, 13))

    by = 88 + len(debts) * 30 + 20
    rounded_rect(d, (16, by, sw - 16, by + 100), 10, fill=PALE_GREEN)
    d.text((30, by + 10), "RECOMMENDED STRATEGY: AVALANCHE METHOD", fill=DARK_GREEN, font=font(True, 15))
    d.text((30, by + 34), "Pay minimums on all debts, put extra toward", fill=DARK_TEXT, font=font(False, 13))
    d.text((30, by + 52), "highest APR first. Save $1,240 in interest!", fill=DARK_TEXT, font=font(False, 13))
    d.text((30, by + 74), "Total Debt: $34,900  |  Debt-Free Date: Mar 2032", fill=MED_GREEN, font=font(True, 13))
    return scr


def create_networth_screen(sw, sh):
    scr = Image.new("RGB", (sw, sh), SCREEN_BG)
    d = ImageDraw.Draw(scr)
    d.rectangle([0, 0, sw, 44], fill=MED_GREEN)
    d.text((16, 10), "Net Worth Dashboard", fill=WHITE, font=font(True, 18))

    d.text((20, 60), "ASSETS", fill=DARK_GREEN, font=font(True, 18))
    assets = [("Checking Account", "$4,200"), ("Savings Account", "$12,500"),
              ("Investment Portfolio", "$28,400"), ("Retirement (401k)", "$45,600"),
              ("Vehicle Value", "$18,000"), ("Other Assets", "$3,200")]
    y = 88
    for name, val in assets:
        d.text((24, y), name, fill=DARK_TEXT, font=font(False, 14))
        d.text((sw // 2 - 100, y), val, fill=GREEN_UNDER, font=font(True, 14))
        y += 24

    d.line([(20, y + 4), (sw - 20, y + 4)], fill=LIGHT_GREEN, width=2)
    d.text((24, y + 10), "TOTAL ASSETS", fill=DARK_GREEN, font=font(True, 15))
    d.text((sw // 2 - 100, y + 10), "$111,900", fill=GREEN_UNDER, font=font(True, 15))

    y += 44
    d.text((20, y), "LIABILITIES", fill=RED_OVER, font=font(True, 18))
    y += 28
    liabs = [("Student Loan", "$18,400"), ("Credit Cards", "$4,650"),
             ("Car Loan", "$8,900"), ("Medical", "$850"), ("Personal Loan", "$2,100")]
    for name, val in liabs:
        d.text((24, y), name, fill=DARK_TEXT, font=font(False, 14))
        d.text((sw // 2 - 100, y), val, fill=RED_OVER, font=font(True, 14))
        y += 24

    d.line([(20, y + 4), (sw - 20, y + 4)], fill=(200, 100, 100), width=2)
    d.text((24, y + 10), "TOTAL LIABILITIES", fill=RED_OVER, font=font(True, 15))
    d.text((sw // 2 - 100, y + 10), "$34,900", fill=RED_OVER, font=font(True, 15))

    y += 44
    rounded_rect(d, (16, y, sw - 16, y + 60), 12, fill=DARK_GREEN)
    d.text((30, y + 8), "NET WORTH", fill=GOLD, font=font(True, 20))
    d.text((sw // 2 - 100, y + 8), "$77,000", fill=WHITE, font=font(True, 28))
    d.text((sw // 2 + 50, y + 36), "+$2,400 this month", fill=LIGHT_GREEN, font=font(True, 13))
    return scr


def create_annual_screen(sw, sh):
    scr = Image.new("RGB", (sw, sh), SCREEN_BG)
    d = ImageDraw.Draw(scr)
    d.rectangle([0, 0, sw, 44], fill=MED_GREEN)
    d.text((16, 10), "Annual Overview \u2014 2026", fill=WHITE, font=font(True, 18))

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    headers = ["MONTH", "INCOME", "EXPENSES", "SAVED", "RATE"]
    cx = [16, 90, 190, 310, 420]
    d.rectangle([8, 54, sw - 8, 80], fill=DARK_GREEN)
    for i, h in enumerate(headers):
        d.text((cx[i], 60), h, fill=WHITE, font=font(True, 12))

    incomes  = [5200, 5200, 5400, 5200, 5200, 5500, 5200, 5200, 5400, 5200, 5200, 5800]
    expenses = [3920, 4100, 3800, 4050, 3750, 4200, 3900, 3850, 4000, 3700, 4300, 5100]
    rf = font(False, 12)
    bf = font(True, 12)
    for ri in range(12):
        ry = 84 + ri * 24
        bg = WHITE if ri % 2 == 0 else (244, 249, 245)
        d.rectangle([8, ry, sw - 8, ry + 24], fill=bg)
        saved = incomes[ri] - expenses[ri]
        rate = saved / incomes[ri] * 100
        d.text((cx[0], ry + 5), months[ri], fill=DARK_TEXT, font=bf)
        d.text((cx[1], ry + 5), f"${incomes[ri]:,}", fill=DARK_TEXT, font=rf)
        d.text((cx[2], ry + 5), f"${expenses[ri]:,}", fill=DARK_TEXT, font=rf)
        saved_color = GREEN_UNDER if saved >= 0 else RED_OVER
        d.text((cx[3], ry + 5), f"${saved:,}", fill=saved_color, font=bf)
        d.text((cx[4], ry + 5), f"{rate:.1f}%", fill=saved_color, font=rf)

    ty = 84 + 12 * 24 + 6
    d.rectangle([8, ty, sw - 8, ty + 28], fill=DARK_GREEN)
    total_inc = sum(incomes)
    total_exp = sum(expenses)
    total_saved = total_inc - total_exp
    d.text((cx[0], ty + 6), "TOTAL", fill=WHITE, font=font(True, 12))
    d.text((cx[1], ty + 6), f"${total_inc:,}", fill=WHITE, font=font(True, 12))
    d.text((cx[2], ty + 6), f"${total_exp:,}", fill=WHITE, font=font(True, 12))
    d.text((cx[3], ty + 6), f"${total_saved:,}", fill=GOLD, font=font(True, 12))
    d.text((cx[4], ty + 6), f"{total_saved/total_inc*100:.1f}%", fill=GOLD, font=font(True, 12))

    chart_y = ty + 48
    d.text((20, chart_y), "MONTHLY SAVINGS TREND", fill=DARK_GREEN, font=font(True, 14))
    chart_y += 24
    max_saved = max(i - e for i, e in zip(incomes, expenses))
    for mi in range(12):
        saved = incomes[mi] - expenses[mi]
        bar_h = max(4, int(80 * saved / max_saved))
        bx = 20 + mi * (sw - 40) // 12
        bw = (sw - 40) // 12 - 4
        d.rectangle([bx, chart_y + 80 - bar_h, bx + bw, chart_y + 80],
                     fill=LIGHT_GREEN if saved > 0 else RED_OVER)
        d.text((bx + 2, chart_y + 84), months[mi][:1], fill=(100,100,100), font=font(False, 10))
    return scr


# ══════════════════════════════════════════════════════════════════════
# IMAGE 1: Hero Main Listing
# ══════════════════════════════════════════════════════════════════════
def create_image_1():
    print("  Creating Image 1: Hero Main Listing...")
    img = gradient_bg(W, H, PALE_GREEN, WHITE)
    draw = ImageDraw.Draw(img)
    add_dots_pattern(draw, W, H, (200, 235, 210), spacing=60, radius=2)

    # Title
    title_font = font(True, 80)
    centered_text(draw, 50, "COMPLETE BUDGET & FINANCE BUNDLE", title_font, DARK_GREEN)

    # 2026 badge
    badge_font = font(True, 52)
    bb = badge_font.getbbox("2026")
    bw = bb[2] - bb[0] + 50
    bh = bb[3] - bb[1] + 24
    bx = W // 2 - bw // 2
    by = 148
    rounded_rect(draw, (bx, by, bx + bw, by + bh), bh // 2, fill=GOLD)
    draw.text((bx + 25, by + 6), "2026", fill=WHITE, font=badge_font)

    # iPad mockup
    ipad_w, ipad_h = 1500, 950
    ipad_x = W // 2 - ipad_w // 2
    ipad_y = 240
    screen = create_budget_screen(int(ipad_w * 0.94), int(ipad_h * 0.94))
    sx, sy, ssw, ssh = draw_ipad(img, ipad_x, ipad_y, ipad_w, ipad_h, screen)

    draw = ImageDraw.Draw(img)

    # Annotations
    draw_annotation(draw, "AUTO PIE CHART",
                    ipad_x + ipad_w - 200, ipad_y + 500,
                    ipad_x + ipad_w + 40, ipad_y + 360, GOLD)
    draw_annotation(draw, "19 EXPENSE CATEGORIES",
                    ipad_x + 150, ipad_y + 600,
                    ipad_x - 320, ipad_y + 480, MED_GREEN)
    draw_annotation(draw, "SAVINGS RATE 24.6%",
                    ipad_x + ipad_w - 300, ipad_y + 200,
                    ipad_x + ipad_w + 40, ipad_y + 120, LIGHT_GREEN)
    draw_annotation(draw, "ALL FORMULAS BUILT IN",
                    ipad_x + 400, ipad_y + 300,
                    ipad_x - 320, ipad_y + 220, DARK_GREEN)

    # Feature pills
    pill_y = ipad_y + ipad_h + 100
    pill_font = font(True, 30)
    pills = ["7 Tabs", "Auto Formulas", "Charts Included", "Google Sheets + Excel"]
    pill_widths = []
    for p in pills:
        bb = pill_font.getbbox(p)
        pill_widths.append(bb[2] - bb[0] + 56)
    gap = 30
    total_pill_w = sum(pill_widths) + gap * (len(pills) - 1)
    px = W // 2 - total_pill_w // 2
    for i, p in enumerate(pills):
        pcx = px + pill_widths[i] // 2
        draw_pill(draw, pcx, pill_y, p, MED_GREEN, WHITE, pill_font, 28, 16)
        px += pill_widths[i] + gap

    # Bottom bar
    bar_y = H - 110
    draw.rectangle([0, bar_y, W, H], fill=DARK_GREEN)
    centered_text(draw, bar_y + 32, "INSTANT DIGITAL DOWNLOAD", font(True, 38), WHITE)
    centered_text(draw, bar_y + 78,
        "Works with Google Sheets & Microsoft Excel  |  No subscriptions  |  Yours forever",
        font(False, 22), PALE_GREEN)

    img.save(os.path.join(OUT, "01_hero_main_listing.png"), quality=95)
    print("    -> Saved 01_hero_main_listing.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 2: What's Included
# ══════════════════════════════════════════════════════════════════════
def create_image_2():
    print("  Creating Image 2: What's Included...")
    img = gradient_bg(W, H, PALE_GREEN, (235, 248, 240))
    draw = ImageDraw.Draw(img)
    add_dots_pattern(draw, W, H, (200, 232, 210), spacing=50, radius=2)

    centered_text(draw, 40, "EVERYTHING INCLUDED IN YOUR BUNDLE", font(True, 68), DARK_GREEN)
    centered_text(draw, 122, "7 Professional Tabs Built for Your Financial Success", font(False, 32), MED_GREEN)

    mini_w, mini_h = 700, 470
    grid_gap_x, grid_gap_y = 60, 100
    grid_total_w = 3 * mini_w + 2 * grid_gap_x
    grid_x0 = W // 2 - grid_total_w // 2
    grid_y0 = 190

    screen_creators = [
        ("Monthly Budget", create_budget_screen),
        ("Expense Tracker", create_expense_screen),
        ("Savings Goals", create_savings_screen),
        ("Debt Payoff", create_debt_screen),
        ("Net Worth", create_networth_screen),
        ("Annual Overview", create_annual_screen),
    ]

    for idx, (name, creator) in enumerate(screen_creators):
        col = idx % 3
        row = idx // 3
        ix = grid_x0 + col * (mini_w + grid_gap_x)
        iy = grid_y0 + row * (mini_h + grid_gap_y + 45)
        scr = creator(int(mini_w * 0.94), int(mini_h * 0.94))
        draw_ipad(img, ix, iy, mini_w, mini_h, scr)
        draw2 = ImageDraw.Draw(img)
        lf = font(True, 24)
        bb = lf.getbbox(name)
        lw = bb[2] - bb[0]
        draw2.text((ix + mini_w // 2 - lw // 2, iy + mini_h + 18), name,
                    fill=DARK_GREEN, font=lf)

    draw = ImageDraw.Draw(img)
    badge_y = grid_y0 + 2 * (mini_h + grid_gap_y + 45) + 40
    draw_pill(draw, W // 2, badge_y, "7 PROFESSIONAL TABS + HOW TO USE GUIDE",
              GOLD, WHITE, font(True, 28), 36, 18)

    bar_y = H - 100
    draw.rectangle([0, bar_y, W, H], fill=DARK_GREEN)
    centered_text(draw, bar_y + 14,
        "ALL FORMULAS PRE-BUILT  |  CHARTS AUTO-UPDATE  |  GOOGLE SHEETS & EXCEL",
        font(True, 28), WHITE)
    centered_text(draw, bar_y + 56,
        "Instant digital download \u2014 start organizing your finances today",
        font(False, 22), PALE_GREEN)

    img.save(os.path.join(OUT, "02_whats_included.png"), quality=95)
    print("    -> Saved 02_whats_included.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 3: Budget Tab Deep Dive
# ══════════════════════════════════════════════════════════════════════
def create_image_3():
    print("  Creating Image 3: Budget Tab Deep Dive...")
    img = gradient_bg(W, H, (230, 245, 235), WHITE)
    draw = ImageDraw.Draw(img)
    add_dots_pattern(draw, W, H, (210, 235, 218), spacing=55, radius=2)

    centered_text(draw, 40, "TRACK EVERY DOLLAR \u2014 AUTOMATICALLY", font(True, 72), DARK_GREEN)
    centered_text(draw, 128, "See exactly where your money goes each month", font(False, 32), MED_GREEN)

    ipad_w, ipad_h = 1200, 850
    overlap = 100
    total_w = ipad_w * 2 - overlap
    x_start = W // 2 - total_w // 2
    ipad_y = 200

    # Left iPad
    screen_left = create_budget_screen(int(ipad_w * 0.94), int(ipad_h * 0.94))
    draw_ipad(img, x_start, ipad_y, ipad_w, ipad_h, screen_left)

    # Right iPad - Summary view
    def create_summary_screen(sw, sh):
        scr = Image.new("RGB", (sw, sh), SCREEN_BG)
        d = ImageDraw.Draw(scr)
        d.rectangle([0, 0, sw, 44], fill=MED_GREEN)
        d.text((16, 10), "Monthly Budget \u2014 Summary View", fill=WHITE, font=font(True, 18))

        pie_cx, pie_cy = sw // 2, 200
        pie_r = 130
        slices = [
            (0,   100, MED_GREEN, "Housing 38%"),
            (100, 135, LIGHT_GREEN, "Groceries 14%"),
            (135, 165, GOLD, "Transport 9%"),
            (165, 210, (100, 180, 140), "Dining 7%"),
            (210, 240, (70, 130, 100), "Entertainment 5%"),
            (240, 280, (180, 210, 190), "Utilities 5%"),
            (280, 360, (150, 200, 170), "Other 22%"),
        ]
        for start, end, color, _ in slices:
            d.pieslice([pie_cx - pie_r, pie_cy - pie_r, pie_cx + pie_r, pie_cy + pie_r],
                        start - 90, end - 90, fill=color, outline=WHITE, width=2)
        inner_r = 55
        d.ellipse([pie_cx - inner_r, pie_cy - inner_r, pie_cx + inner_r, pie_cy + inner_r],
                   fill=SCREEN_BG)
        d.text((pie_cx - 40, pie_cy - 20), "$3,920", fill=DARK_GREEN, font=font(True, 22))
        d.text((pie_cx - 30, pie_cy + 6), "TOTAL", fill=(120,120,120), font=font(False, 13))

        ly = pie_cy + pie_r + 20
        for i, (_, _, color, label) in enumerate(slices):
            lx = 30 + (i % 3) * (sw // 3)
            row = i // 3
            ly2 = ly + row * 26
            d.rectangle([lx, ly2, lx + 14, ly2 + 14], fill=color)
            d.text((lx + 20, ly2 - 2), label, fill=DARK_TEXT, font=font(False, 13))

        cy = ly + 70
        cards = [
            ("TOTAL INCOME", "$5,200", GREEN_UNDER),
            ("TOTAL EXPENSES", "$3,920", RED_OVER),
            ("NET BALANCE", "$1,280", DARK_GREEN),
            ("SAVINGS RATE", "24.6%", GOLD),
        ]
        for i, (title, val, color) in enumerate(cards):
            cxx = 20 + (i % 2) * (sw // 2)
            ccy = cy + (i // 2) * 80
            rounded_rect(d, (cxx, ccy, cxx + sw // 2 - 30, ccy + 68), 10,
                         fill=WHITE, outline=(220, 230, 222))
            d.text((cxx + 14, ccy + 8), title, fill=(120, 120, 120), font=font(False, 12))
            d.text((cxx + 14, ccy + 28), val, fill=color, font=font(True, 26))

        byy = cy + 170
        d.text((20, byy), "SAVINGS GOAL PROGRESS", fill=DARK_GREEN, font=font(True, 14))
        byy += 24
        rounded_rect(d, (20, byy, sw - 20, byy + 22), 11, fill=(220, 230, 222))
        rounded_rect(d, (20, byy, 20 + int((sw - 40) * 0.75), byy + 22), 11, fill=LIGHT_GREEN)
        d.text((sw // 2 - 20, byy + 2), "75%", fill=WHITE, font=font(True, 14))
        return scr

    screen_right = create_summary_screen(int(ipad_w * 0.94), int(ipad_h * 0.94))
    draw_ipad(img, x_start + ipad_w - overlap, ipad_y, ipad_w, ipad_h, screen_right)

    draw = ImageDraw.Draw(img)

    draw_annotation(draw, "BUDGETED vs ACTUAL",
                    x_start + 400, ipad_y + 350,
                    x_start - 80, ipad_y + 260, GOLD)
    draw_annotation(draw, "AUTO-CALCULATING DIFFERENCE",
                    x_start + 600, ipad_y + 500,
                    x_start - 80, ipad_y + 600, MED_GREEN)
    draw_annotation(draw, "EXPENSE PIE CHART",
                    x_start + ipad_w + 400, ipad_y + 300,
                    x_start + total_w + 60, ipad_y + 200, GOLD)
    draw_annotation(draw, "SAVINGS RATE CALCULATOR",
                    x_start + ipad_w + 500, ipad_y + 650,
                    x_start + total_w + 60, ipad_y + 580, LIGHT_GREEN)

    bar_y = H - 170
    rounded_rect(draw, (80, bar_y, W - 80, bar_y + 70), 35, fill=MED_GREEN)
    centered_text(draw, bar_y + 16,
        "19 Expense Categories  |  5 Income Sources  |  Auto Pie Chart  |  Savings Rate",
        font(True, 28), WHITE)

    draw.rectangle([0, H - 90, W, H], fill=DARK_GREEN)
    centered_text(draw, H - 72,
        "INSTANT DIGITAL DOWNLOAD  \u2014  GOOGLE SHEETS & EXCEL",
        font(True, 28), WHITE)

    img.save(os.path.join(OUT, "03_budget_tab_preview.png"), quality=95)
    print("    -> Saved 03_budget_tab_preview.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 4: Savings & Debt Showcase
# ══════════════════════════════════════════════════════════════════════
def create_image_4():
    print("  Creating Image 4: Savings & Debt Showcase...")
    img = gradient_bg(W, H, PALE_GREEN, WHITE)
    draw = ImageDraw.Draw(img)
    add_dots_pattern(draw, W, H, (205, 235, 215), spacing=55, radius=2)

    centered_text(draw, 40, "SET GOALS. CRUSH DEBT. BUILD WEALTH.", font(True, 68), DARK_GREEN)
    centered_text(draw, 125, "Two powerful tabs to transform your financial future",
                  font(False, 30), MED_GREEN)

    ipad_w, ipad_h = 1150, 850
    gap = 80
    total_w = ipad_w * 2 + gap
    x_start = W // 2 - total_w // 2
    ipad_y = 210

    scr_sav = create_savings_screen(int(ipad_w * 0.94), int(ipad_h * 0.94))
    draw_ipad(img, x_start, ipad_y, ipad_w, ipad_h, scr_sav)

    scr_debt = create_debt_screen(int(ipad_w * 0.94), int(ipad_h * 0.94))
    draw_ipad(img, x_start + ipad_w + gap, ipad_y, ipad_w, ipad_h, scr_debt)

    draw = ImageDraw.Draw(img)

    lf = font(True, 30)
    bb1 = lf.getbbox("SAVINGS GOALS TRACKER")
    tw1 = bb1[2] - bb1[0]
    draw.text((x_start + ipad_w // 2 - tw1 // 2, ipad_y + ipad_h + 25),
              "SAVINGS GOALS TRACKER", fill=DARK_GREEN, font=lf)

    bb2 = lf.getbbox("DEBT PAYOFF PLANNER")
    tw2 = bb2[2] - bb2[0]
    draw.text((x_start + ipad_w + gap + ipad_w // 2 - tw2 // 2, ipad_y + ipad_h + 25),
              "DEBT PAYOFF PLANNER", fill=DARK_GREEN, font=lf)

    draw_annotation(draw, "10 SAVINGS GOALS",
                    x_start + 200, ipad_y + 300,
                    x_start - 80, ipad_y + 250, GOLD)
    draw_annotation(draw, "AUTO PROGRESS %",
                    x_start + ipad_w - 100, ipad_y + 400,
                    x_start - 80, ipad_y + 440, LIGHT_GREEN)

    rx = x_start + ipad_w + gap
    draw_annotation(draw, "PAYOFF DATE CALCULATOR",
                    rx + ipad_w - 100, ipad_y + 300,
                    rx + ipad_w + 30, ipad_y + 250, GOLD)
    draw_annotation(draw, "STRATEGY TIPS",
                    rx + 300, ipad_y + 600,
                    rx + ipad_w + 30, ipad_y + 440, MED_GREEN)

    bar_y = H - 200
    draw.rectangle([0, bar_y, W, H], fill=DARK_GREEN)
    centered_text(draw, bar_y + 20,
        "YOUR JOURNEY TO FINANCIAL FREEDOM STARTS HERE", font(True, 42), WHITE)
    centered_text(draw, bar_y + 80,
        "Track savings progress in real-time  |  See your debt-free date  |  Automated calculations",
        font(False, 24), PALE_GREEN)
    centered_text(draw, bar_y + 130,
        "INSTANT DIGITAL DOWNLOAD  \u2014  GOOGLE SHEETS & EXCEL", font(True, 28), GOLD)

    img.save(os.path.join(OUT, "04_savings_debt_showcase.png"), quality=95)
    print("    -> Saved 04_savings_debt_showcase.png")


# ══════════════════════════════════════════════════════════════════════
# IMAGE 5: Value Proposition
# ══════════════════════════════════════════════════════════════════════
def create_image_5():
    print("  Creating Image 5: Value Proposition...")
    img = Image.new("RGB", (W, H), DARK_GREEN)
    draw = ImageDraw.Draw(img)

    split_y = int(H * 0.58)
    add_dots_pattern(draw, W, split_y, (35, 80, 60), spacing=50, radius=2)
    draw.rectangle([0, split_y, W, H], fill=WHITE)
    add_dots_pattern(draw, W, H, (240, 245, 240), spacing=50, radius=2)

    ipad_w, ipad_h = 1200, 800
    ipad_x = W // 2 - ipad_w // 2
    ipad_y = split_y - ipad_h // 2 - 60

    # Glow
    for g in range(40, 0, -2):
        gc_r = min(255, 82 + g)
        gc_g = min(255, 183 + g // 2)
        gc_b = min(255, 136 + g // 2)
        rounded_rect(draw, (ipad_x - g, ipad_y - g,
                           ipad_x + ipad_w + g, ipad_y + ipad_h + g),
                     60, fill=None, outline=(gc_r, gc_g, gc_b), width=2)

    screen = create_budget_screen(int(ipad_w * 0.94), int(ipad_h * 0.94))
    draw_ipad(img, ipad_x, ipad_y, ipad_w, ipad_h, screen)
    draw = ImageDraw.Draw(img)

    badges = [
        ("7 Professional Tabs",    ipad_x - 280,  ipad_y + 60),
        ("All Formulas Pre-Built", ipad_x - 310,  ipad_y + 260),
        ("Auto-Updating Charts",   ipad_x - 270,  ipad_y + 460),
        ("Google Sheets + Excel",  ipad_x + ipad_w + 50,  ipad_y + 60),
        ("Beginner Friendly",      ipad_x + ipad_w + 80,  ipad_y + 260),
        ("Buy Once, Use Forever",  ipad_x + ipad_w + 30,  ipad_y + 460),
    ]
    badge_font = font(True, 22)
    for text, bx, by in badges:
        bb = badge_font.getbbox(text)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad_x_b, pad_y_b = 22, 14
        rw, rh = tw + pad_x_b * 2, th + pad_y_b * 2
        if by < split_y:
            bg_col, fg_col, border_col = MED_GREEN, WHITE, LIGHT_GREEN
        else:
            bg_col, fg_col, border_col = WHITE, DARK_GREEN, LIGHT_GREEN
        rounded_rect(draw, (bx, by, bx + rw, by + rh), rh // 2,
                      fill=bg_col, outline=border_col, width=2)
        draw.text((bx + pad_x_b, by + pad_y_b - 2), text, fill=fg_col, font=badge_font)
        line_start_x = bx + rw if bx < ipad_x else bx
        line_end_x = ipad_x if bx < ipad_x else ipad_x + ipad_w
        line_y = by + rh // 2
        draw.line([(line_start_x, line_y), (line_end_x, line_y)],
                   fill=LIGHT_GREEN, width=1)

    ty = split_y + ipad_h // 2 - 30
    centered_text(draw, ty, "TAKE CONTROL OF YOUR MONEY IN MINUTES",
                  font(True, 56), DARK_GREEN)

    price_y = ty + 80
    draw_pill(draw, W // 2, price_y, "$9.99 \u2014 INSTANT DOWNLOAD",
              GOLD, WHITE, font(True, 36), 40, 18)

    star_y = price_y + 55
    centered_text(draw, star_y, "\u2605 \u2605 \u2605 \u2605 \u2605", font(True, 40), GOLD)
    centered_text(draw, star_y + 48, "Trusted by thousands of happy customers",
                  font(False, 24), (120, 120, 120))

    centered_text(draw, star_y + 90,
        "No subscriptions. No monthly fees. Yours forever.",
        font(True, 28), MED_GREEN)

    cta_y = H - 100
    draw.rectangle([0, cta_y, W, H], fill=DARK_GREEN)
    centered_text(draw, cta_y + 12,
        "ADD TO CART NOW \u2014 START YOUR FINANCIAL TRANSFORMATION TODAY",
        font(True, 34), WHITE)
    centered_text(draw, cta_y + 58,
        "Google Sheets & Excel  |  Instant Download  |  Lifetime Access",
        font(False, 22), PALE_GREEN)

    img.save(os.path.join(OUT, "05_value_proposition.png"), quality=95)
    print("    -> Saved 05_value_proposition.png")


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Etsy listing images...")
    print(f"Output directory: {OUT}")
    print()
    create_image_1()
    create_image_2()
    create_image_3()
    create_image_4()
    create_image_5()
    print()
    print("All 5 images generated successfully!")
    print(f"Files saved to: {OUT}")
