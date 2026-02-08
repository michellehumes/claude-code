"""
Create professional Etsy listing images for the Small Business Planner.
Generates 5 images at Etsy-recommended 2700x2025.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = "/home/user/claude-code/etsy-digital-download-2/images"
W, H = 2700, 2025

# ── Colors (Warm professional palette) ──
NAVY = (27, 42, 74)
STEEL_BLUE = (46, 64, 87)
DUSTY_BLUE = (107, 140, 174)
PALE_BLUE = (214, 228, 240)
ICE_BLUE = (235, 242, 250)
WHITE = (255, 255, 255)
LIGHT_GRAY = (245, 245, 245)
DARK_TEXT = (33, 33, 33)
CORAL = (232, 128, 106)
WARM_GOLD = (212, 168, 83)
SOFT_PEACH = (245, 230, 211)
MINT = (123, 200, 164)
CREAM = (255, 253, 248)

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
    return bbox[3] - bbox[1]

def draw_text_at(draw, text, x, y, font, color):
    draw.text((x, y), text, font=font, fill=color)


# ═══════════════════════════════════════════════════
#  IMAGE 1: MAIN HERO
# ═══════════════════════════════════════════════════
def create_hero_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top banner
    draw.rectangle([(0, 0), (W, 180)], fill=NAVY)
    font_sm = get_font(42)
    draw_centered_text(draw, "INSTANT DOWNLOAD  |  GOOGLE SHEETS & EXCEL COMPATIBLE", 70, font_sm, PALE_BLUE)

    # Main content card
    draw_rounded_rect(draw, (120, 240, W-120, H-180), 30, WHITE, outline=DUSTY_BLUE, width=3)

    # Inner accent bar
    draw.rectangle([(120, 240), (W-120, 320)], fill=STEEL_BLUE)
    font_badge = get_font(36, bold=True)
    draw_centered_text(draw, "ALL-IN-ONE SPREADSHEET  |  9 TABS  |  READY TO USE", 258, font_badge, PALE_BLUE)

    # Main title
    font_title = get_font(100, bold=True)
    draw_centered_text(draw, "SMALL BUSINESS", 380, font_title, NAVY)
    draw_centered_text(draw, "PLANNER &", 500, font_title, NAVY)
    draw_centered_text(draw, "STARTER KIT", 620, font_title, NAVY)

    # Year badge
    font_year = get_font(72, bold=True)
    draw_rounded_rect(draw, (W//2 - 130, 770, W//2 + 130, 860), 15, CORAL)
    draw_centered_text(draw, "2026", 778, font_year, WHITE)

    # Feature list - 3 columns
    font_features = get_font(40, bold=True)
    features = [
        "Business Dashboard",
        "Client & CRM Tracker",
        "Invoice Manager",
        "Project/Order Tracker",
        "Content Calendar",
        "Income & Expense Log",
        "Inventory Manager",
        "Goal & Action Planner",
        "How-to-Use Guide",
    ]

    y_start = 920
    col1_x = 250
    col2_x = W // 2 - 50
    col3_x = W - 700

    for idx, feat in enumerate(features):
        if idx < 3:
            col_x = col1_x
        elif idx < 6:
            col_x = col2_x
        else:
            col_x = col3_x
        y = y_start + (idx % 3) * 75
        cx, cy = col_x - 45, y + 18
        draw.ellipse([(cx-16, cy-16), (cx+16, cy+16)], fill=CORAL)
        draw_text_at(draw, feat, col_x, y, font_features, DARK_TEXT)

    # Divider
    draw.line([(200, 1180), (W-200, 1180)], fill=PALE_BLUE, width=3)

    # Value prop
    font_value = get_font(46, bold=True)
    draw_centered_text(draw, "Run Your Business Like a Pro — From Day One", 1220, font_value, STEEL_BLUE)
    font_sub = get_font(36)
    draw_centered_text(draw, "Pre-built formulas. Drop-down menus. Auto-calculating charts. Just add your data.", 1295, font_sub, DARK_TEXT)

    # Ideal for section
    font_ideal = get_font(34, bold=True)
    draw_centered_text(draw, "PERFECT FOR:  Etsy Sellers  |  Freelancers  |  Coaches  |  Service Providers  |  Small Shops", 1400, font_ideal, CORAL)

    # Bottom CTA
    draw.rectangle([(0, H-160), (W, H)], fill=NAVY)
    font_cta = get_font(48, bold=True)
    draw_centered_text(draw, "DIGITAL DOWNLOAD  -  START ORGANIZING YOUR BUSINESS TODAY", H-128, font_cta, PALE_BLUE)

    img.save(os.path.join(OUT_DIR, "01_hero_main_listing.png"), quality=95)
    print("Created: 01_hero_main_listing.png")


# ═══════════════════════════════════════════════════
#  IMAGE 2: WHAT'S INCLUDED
# ═══════════════════════════════════════════════════
def create_features_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 200)], fill=NAVY)
    font_title = get_font(72, bold=True)
    draw_centered_text(draw, "WHAT'S INCLUDED", 55, font_title, WHITE)
    font_sub = get_font(38)
    draw_centered_text(draw, "9 Professional Tabs  |  All Formulas & Dropdowns Built In", 150, font_sub, PALE_BLUE)

    features = [
        ("DASHBOARD", "Monthly revenue tracking.\nKPI metrics at a glance.\nAuto bar chart visualization.", DUSTY_BLUE),
        ("CLIENT TRACKER", "50-row CRM with contacts.\nStatus dropdowns (Lead → VIP).\nRevenue per client tracking.", STEEL_BLUE),
        ("INVOICE TRACKER", "Track sent/paid/overdue.\nAuto balance calculator.\nCollection rate summary.", WARM_GOLD),
        ("PROJECT TRACKER", "Deadline countdown timer.\nBudget vs cost vs profit.\nPriority levels (Low → Urgent).", CORAL),
        ("CONTENT CALENDAR", "100 rows for all platforms.\nPlatform & content dropdowns.\n20 content ideas included!", MINT),
        ("INCOME & EXPENSES", "Separate income & expense logs.\nTax deductible flagging.\nAuto net profit calculation.", (74, 124, 89)),
        ("INVENTORY MANAGER", "Stock levels & reorder alerts.\nCost, price, & profit/unit.\nTotal stock value tracker.", (139, 109, 176)),
        ("GOALS & PLANNING", "5 goals per quarter (20/year).\nKPI tracking per goal.\nAnnual vision prompts.", WARM_GOLD),
    ]

    card_w = 1150
    card_h = 310
    gap_x = 100
    gap_y = 35
    start_x = (W - 2 * card_w - gap_x) // 2
    start_y = 245

    font_card_title = get_font(42, bold=True)
    font_card_body = get_font(30)
    font_num = get_font(28, bold=True)

    for idx, (title, body, accent) in enumerate(features):
        col = idx % 2
        row = idx // 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, WHITE, outline=accent, width=3)
        draw_rounded_rect(draw, (x, y, x + 12, y + card_h), 6, accent)

        badge_x = x + 40
        badge_y = y + 20
        draw.ellipse([(badge_x, badge_y), (badge_x + 56, badge_y + 56)], fill=accent)
        num_text = str(idx + 1)
        bbox = draw.textbbox((0, 0), num_text, font=font_num)
        nw = bbox[2] - bbox[0]
        draw.text((badge_x + (56 - nw) // 2, badge_y + 10), num_text, font=font_num, fill=WHITE)

        draw.text((x + 115, y + 28), title, font=font_card_title, fill=NAVY)
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw.text((x + 115, y + 90 + li * 52), f"  {line}", font=font_card_body, fill=DARK_TEXT)

    # Bottom + bonus
    draw_rounded_rect(draw, (start_x, start_y + 4*(card_h+gap_y) + 10, W - start_x, start_y + 4*(card_h+gap_y) + 80), 15, PALE_BLUE)
    font_bonus = get_font(34, bold=True)
    draw_centered_text(draw, "BONUS: Tab 9 — Complete How-to-Use Guide with Pro Tips for Every Tab", start_y + 4*(card_h+gap_y) + 25, font_bonus, NAVY)

    draw.rectangle([(0, H - 90), (W, H)], fill=NAVY)
    font_bottom = get_font(34, bold=True)
    draw_centered_text(draw, "WORKS WITH GOOGLE SHEETS  |  MICROSOFT EXCEL  |  LIBREOFFICE", H - 70, font_bottom, PALE_BLUE)

    img.save(os.path.join(OUT_DIR, "02_whats_included.png"), quality=95)
    print("Created: 02_whats_included.png")


# ═══════════════════════════════════════════════════
#  IMAGE 3: DASHBOARD & CLIENT TRACKER PREVIEW
# ═══════════════════════════════════════════════════
def create_dashboard_mockup():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 140)], fill=NAVY)
    font_title = get_font(56, bold=True)
    draw_centered_text(draw, "DASHBOARD & CLIENT TRACKER PREVIEW", 35, font_title, WHITE)

    # Screen frame
    sx, sy = 100, 190
    sw, sh = W - 200, H - 320

    # Window chrome
    draw_rounded_rect(draw, (sx, sy, sx + sw, sy + 55), 12, (55, 55, 55))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([(sx + 18 + i*32, sy + 15), (sx + 42 + i*32, sy + 39)], fill=c)

    ss_y = sy + 55
    draw.rectangle([(sx, ss_y), (sx + sw, sy + sh)], fill=WHITE)

    # Tab bar
    tab_y = sy + sh - 45
    tabs = ["Dashboard", "Client Tracker", "Invoice", "Projects", "Content", "Income", "Inventory", "Goals"]
    tab_x = sx + 10
    font_tab = get_font(20)
    for i, tab in enumerate(tabs):
        tw = len(tab) * 12 + 26
        tc = DUSTY_BLUE if i == 0 else LIGHT_GRAY
        txt_c = WHITE if i == 0 else DARK_TEXT
        draw_rounded_rect(draw, (tab_x, tab_y, tab_x + tw, tab_y + 40), 8, tc)
        draw.text((tab_x + 13, tab_y + 10), tab, font=font_tab, fill=txt_c)
        tab_x += tw + 6

    # Dashboard title
    draw.rectangle([(sx + 10, ss_y + 10), (sx + sw - 10, ss_y + 60)], fill=PALE_BLUE)
    font_ss_title = get_font(32, bold=True)
    draw.text((sx + 350, ss_y + 18), "SMALL BUSINESS DASHBOARD", font=font_ss_title, fill=NAVY)

    # KPI Cards
    kpi_data = [
        ("Monthly Revenue", "$8,450", STEEL_BLUE),
        ("Monthly Expenses", "$3,120", CORAL),
        ("Net Profit", "$5,330", MINT),
        ("Profit Margin", "63.1%", WARM_GOLD),
        ("Active Clients", "12", DUSTY_BLUE),
    ]

    font_kpi_label = get_font(22)
    font_kpi_value = get_font(34, bold=True)
    kpi_w = (sw - 80) // 5
    kpi_y = ss_y + 80

    for i, (label, value, color) in enumerate(kpi_data):
        kx = sx + 20 + i * (kpi_w + 12)
        draw_rounded_rect(draw, (kx, kpi_y, kx + kpi_w, kpi_y + 110), 12, WHITE, outline=color, width=2)
        draw.rectangle([(kx, kpi_y), (kx + kpi_w, kpi_y + 6)], fill=color)
        # center label
        lbbox = draw.textbbox((0, 0), label, font=font_kpi_label)
        lw = lbbox[2] - lbbox[0]
        draw.text((kx + (kpi_w - lw) // 2, kpi_y + 20), label, font=font_kpi_label, fill=DARK_TEXT)
        vbbox = draw.textbbox((0, 0), value, font=font_kpi_value)
        vw = vbbox[2] - vbbox[0]
        draw.text((kx + (kpi_w - vw) // 2, kpi_y + 55), value, font=font_kpi_value, fill=color)

    # Revenue table
    table_y = kpi_y + 140
    font_th = get_font(24, bold=True)
    font_td = get_font(22)

    cols_t = [("Month", 200), ("Revenue", 180), ("Expenses", 180), ("Net Profit", 180), ("Margin", 140)]
    cx = sx + 40
    for label, cw in cols_t:
        draw.rectangle([(cx, table_y), (cx + cw, table_y + 45)], fill=NAVY)
        draw.text((cx + 12, table_y + 10), label, font=font_th, fill=WHITE)
        cx += cw

    table_data = [
        ("January", "$6,200", "$2,800", "$3,400", "54.8%"),
        ("February", "$7,100", "$2,950", "$4,150", "58.5%"),
        ("March", "$8,450", "$3,120", "$5,330", "63.1%"),
        ("April", "$7,800", "$3,050", "$4,750", "60.9%"),
        ("May", "$9,200", "$3,400", "$5,800", "63.0%"),
        ("June", "$8,900", "$3,250", "$5,650", "63.5%"),
    ]

    for ri, row_data in enumerate(table_data):
        ry = table_y + 45 + ri * 42
        bg = LIGHT_GRAY if ri % 2 == 1 else WHITE
        cx = sx + 40
        for ci, (_, cw) in enumerate(cols_t):
            draw.rectangle([(cx, ry), (cx + cw, ry + 42)], fill=bg, outline=(220, 220, 220))
            color = DARK_TEXT
            if ci == 3 and not row_data[ci].startswith("-"):
                color = (74, 124, 89)
            draw.text((cx + 12, ry + 10), row_data[ci], font=font_td, fill=color)
            cx += cw

    # Client tracker section on right
    ct_x = sx + sw // 2 + 50
    ct_y = table_y
    draw_rounded_rect(draw, (ct_x, ct_y, ct_x + sw // 2 - 80, ct_y + 350), 15, WHITE, outline=DUSTY_BLUE, width=2)
    draw.rectangle([(ct_x, ct_y), (ct_x + sw // 2 - 80, ct_y + 45)], fill=DUSTY_BLUE)
    draw.text((ct_x + 120, ct_y + 10), "CLIENT TRACKER", font=font_th, fill=WHITE)

    clients = [
        ("Sarah M.", "sarah@email.com", "Active", "$2,400"),
        ("Tech Corp", "info@techcorp.com", "VIP", "$12,500"),
        ("Amy L.", "amy.l@gmail.com", "Lead", "—"),
        ("Design Co", "hello@designco.io", "Active", "$4,800"),
        ("James R.", "james@biz.com", "Completed", "$1,200"),
    ]

    font_client = get_font(20)
    for ci, (name, email, status, rev) in enumerate(clients):
        cy = ct_y + 60 + ci * 55
        bg = LIGHT_GRAY if ci % 2 == 1 else WHITE
        draw.rectangle([(ct_x + 10, cy), (ct_x + sw // 2 - 90, cy + 50)], fill=bg)
        draw.text((ct_x + 20, cy + 5), name, font=get_font(22, bold=True), fill=NAVY)
        draw.text((ct_x + 20, cy + 28), email, font=font_client, fill=DARK_TEXT)

        # Status badge
        status_colors = {"Active": MINT, "VIP": WARM_GOLD, "Lead": DUSTY_BLUE, "Completed": STEEL_BLUE}
        sc = status_colors.get(status, LIGHT_GRAY)
        sbbox = draw.textbbox((0, 0), status, font=font_client)
        sw2 = sbbox[2] - sbbox[0]
        badge_x = ct_x + sw // 2 - 280
        draw_rounded_rect(draw, (badge_x, cy + 12, badge_x + sw2 + 20, cy + 38), 10, sc)
        draw.text((badge_x + 10, cy + 14), status, font=font_client, fill=WHITE)

        draw.text((ct_x + sw // 2 - 170, cy + 14), rev, font=get_font(22, bold=True), fill=NAVY)

    # Bottom banner
    draw.rectangle([(0, H - 100), (W, H)], fill=NAVY)
    font_btm = get_font(36, bold=True)
    draw_centered_text(draw, "AUTO-CALCULATING FORMULAS  |  DROP-DOWN MENUS  |  JUST ADD YOUR DATA", H - 78, font_btm, PALE_BLUE)

    img.save(os.path.join(OUT_DIR, "03_dashboard_preview.png"), quality=95)
    print("Created: 03_dashboard_preview.png")


# ═══════════════════════════════════════════════════
#  IMAGE 4: CONTENT CALENDAR & INVENTORY
# ═══════════════════════════════════════════════════
def create_content_inventory_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 140)], fill=NAVY)
    font_title = get_font(52, bold=True)
    draw_centered_text(draw, "PLAN YOUR CONTENT & MANAGE INVENTORY", 38, font_title, WHITE)

    # Left: Content Calendar
    panel_w = W // 2 - 80
    px = 50
    py = 200
    ph = H - 380

    draw_rounded_rect(draw, (px, py, px + panel_w, py + ph), 20, WHITE, outline=MINT, width=3)
    draw.rectangle([(px, py), (px + panel_w, py + 80)], fill=MINT)
    font_panel = get_font(38, bold=True)
    draw.text((px + 180, py + 18), "CONTENT CALENDAR", font=font_panel, fill=WHITE)

    font_entry = get_font(26, bold=True)
    font_detail = get_font(22)

    entries = [
        ("Mon, Jan 6", "Instagram Post", "Product Feature", "Scheduled", "Photo"),
        ("Tue, Jan 7", "TikTok", "Behind the Scenes", "Designing", "Video"),
        ("Wed, Jan 8", "Pinterest", "Blog Pin", "Published", "Infographic"),
        ("Thu, Jan 9", "Instagram Reel", "Customer Review", "Idea", "Reel"),
        ("Fri, Jan 10", "Facebook", "Weekend Sale Promo", "Scheduled", "Carousel"),
        ("Sat, Jan 11", "Email", "Newsletter", "Writing", "Newsletter"),
    ]

    ey = py + 100
    for name, platform, topic, status, content_type in entries:
        draw_text_at(draw, name, px + 30, ey, font_entry, NAVY)

        # Platform badge
        plat_colors = {"Instagram Post": (225, 48, 108), "TikTok": (0, 0, 0), "Pinterest": (189, 8, 28),
                       "Instagram Reel": (225, 48, 108), "Facebook": (66, 103, 178), "Email": STEEL_BLUE}
        pc = plat_colors.get(platform, DUSTY_BLUE)
        pbbox = draw.textbbox((0, 0), platform, font=font_detail)
        pw2 = pbbox[2] - pbbox[0]
        draw_rounded_rect(draw, (px + 280, ey + 2, px + 290 + pw2, ey + 28), 8, pc)
        draw.text((px + 285, ey + 4), platform, font=font_detail, fill=WHITE)

        draw_text_at(draw, topic, px + 30, ey + 35, font_detail, DARK_TEXT)
        draw_text_at(draw, f"{content_type}  |  {status}", px + 30, ey + 60, font_detail, DUSTY_BLUE)
        ey += 105

    # Content ideas box
    ideas_y = ey + 20
    draw_rounded_rect(draw, (px + 20, ideas_y, px + panel_w - 20, ideas_y + 200), 12, PALE_BLUE)
    draw_text_at(draw, "20 CONTENT IDEAS INCLUDED:", px + 40, ideas_y + 15, font_entry, NAVY)
    mini_ideas = [
        "Behind-the-scenes of your process",
        "Customer testimonial spotlight",
        "Before & after transformation",
        "Day in the life of your business",
        "FAQ answered + product feature",
    ]
    for ii, idea in enumerate(mini_ideas):
        draw_text_at(draw, f"  {ii+1}. {idea}", px + 40, ideas_y + 50 + ii * 30, font_detail, DARK_TEXT)

    # Right: Inventory Manager
    px2 = W // 2 + 30
    draw_rounded_rect(draw, (px2, py, px2 + panel_w, py + ph), 20, WHITE, outline=(139, 109, 176), width=3)
    draw.rectangle([(px2, py), (px2 + panel_w, py + 80)], fill=(139, 109, 176))
    draw.text((px2 + 180, py + 18), "INVENTORY MANAGER", font=font_panel, fill=WHITE)

    products = [
        ("SKU-001", "Handmade Candle - Lavender", "24", "10", "IN STOCK", "$8.00", "$22.00"),
        ("SKU-002", "Soy Candle - Vanilla", "8", "10", "LOW STOCK", "$7.50", "$19.99"),
        ("SKU-003", "Wax Melt Pack (6)", "42", "15", "IN STOCK", "$3.00", "$14.99"),
        ("SKU-004", "Gift Box Set - Premium", "3", "5", "REORDER!", "$15.00", "$45.00"),
        ("SKU-005", "Room Spray - Eucalyptus", "0", "8", "REORDER!", "$4.00", "$16.99"),
    ]

    iy = py + 100
    for sku, name, qty, reorder, status, cost, price in products:
        draw_text_at(draw, sku, px2 + 30, iy, get_font(20), DUSTY_BLUE)
        draw_text_at(draw, name, px2 + 30, iy + 25, font_entry, NAVY)

        # Quantity
        draw_text_at(draw, f"Qty: {qty}", px2 + 30, iy + 55, font_detail, DARK_TEXT)
        draw_text_at(draw, f"Reorder at: {reorder}", px2 + 200, iy + 55, font_detail, DARK_TEXT)

        # Status badge
        if status == "REORDER!":
            sc = CORAL
        elif status == "LOW STOCK":
            sc = WARM_GOLD
        else:
            sc = MINT
        sbbox = draw.textbbox((0, 0), status, font=font_detail)
        sw2 = sbbox[2] - sbbox[0]
        draw_rounded_rect(draw, (px2 + panel_w - sw2 - 60, iy + 8, px2 + panel_w - 30, iy + 34), 8, sc)
        draw.text((px2 + panel_w - sw2 - 45, iy + 10), status, font=font_detail, fill=WHITE)

        # Price info
        draw_text_at(draw, f"Cost: {cost}  |  Price: {price}", px2 + 30, iy + 82, font_detail, (74, 124, 89))

        iy += 120

    # Inventory summary box
    inv_sum_y = iy + 20
    draw_rounded_rect(draw, (px2 + 20, inv_sum_y, px2 + panel_w - 20, inv_sum_y + 160), 12, PALE_BLUE)
    draw_text_at(draw, "INVENTORY SUMMARY", px2 + 40, inv_sum_y + 15, font_entry, NAVY)
    inv_stats = [
        ("Total Products: 5", "Total Units: 77"),
        ("Stock Value: $831.00", "Items to Reorder: 2"),
    ]
    for si, (left, right) in enumerate(inv_stats):
        draw_text_at(draw, left, px2 + 40, inv_sum_y + 55 + si * 40, font_detail, DARK_TEXT)
        draw_text_at(draw, right, px2 + 400, inv_sum_y + 55 + si * 40, font_detail, DARK_TEXT)

    # Bottom
    draw_rounded_rect(draw, (100, H - 150, W - 100, H - 30), 15, PALE_BLUE)
    font_tip = get_font(32, bold=True)
    draw_centered_text(draw, "Drop-down menus for platforms, content types & statuses  |  Auto-alerts when stock is low", H - 110, font_tip, NAVY)

    img.save(os.path.join(OUT_DIR, "04_content_inventory.png"), quality=95)
    print("Created: 04_content_inventory.png")


# ═══════════════════════════════════════════════════
#  IMAGE 5: WHO IT'S FOR + VALUE PROPOSITION
# ═══════════════════════════════════════════════════
def create_value_prop_image():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, 20)], fill=CORAL)

    # Title
    font_title = get_font(68, bold=True)
    draw_centered_text(draw, "THE ONLY SPREADSHEET YOUR", 70, font_title, NAVY)
    draw_centered_text(draw, "SMALL BUSINESS NEEDS", 155, font_title, NAVY)

    draw.line([(W//2 - 200, 260), (W//2 + 200, 260)], fill=CORAL, width=4)

    # "Perfect For" section
    font_section = get_font(46, bold=True)
    draw_centered_text(draw, "PERFECT FOR", 300, font_section, CORAL)

    audiences = [
        "Etsy & Handmade Sellers",
        "Freelancers & Consultants",
        "Coaches & Course Creators",
        "Service-Based Businesses",
        "Side Hustlers & Solopreneurs",
        "Small Shop Owners",
    ]

    font_aud = get_font(38, bold=True)
    y_aud = 380
    col1_x = 250
    col2_x = W // 2 + 100

    for idx, aud in enumerate(audiences):
        col_x = col1_x if idx < 3 else col2_x
        y = y_aud + (idx % 3) * 70
        cx = col_x - 45
        draw.ellipse([(cx - 16, y + 10), (cx + 16, y + 42)], fill=CORAL)
        font_check = get_font(28, bold=True)
        draw.text((cx - 8, y + 12), "✓", font=font_check, fill=WHITE)
        draw_text_at(draw, aud, col_x, y + 8, font_aud, DARK_TEXT)

    # Benefits section
    draw.line([(200, 620), (W - 200, 620)], fill=PALE_BLUE, width=2)

    benefits = [
        ("SAVE 10+ HOURS/MONTH", "Stop juggling apps, notebooks,\nand sticky notes. Everything\nlives in one organized file."),
        ("LOOK PROFESSIONAL", "Impress clients with organized\nrecords, timely invoices, and\nsmooth project management."),
        ("KNOW YOUR NUMBERS", "See revenue, profit, expenses,\nand growth trends instantly.\nMake data-driven decisions."),
        ("NEVER MISS A BEAT", "Track deadlines, follow up on\ninvoices, reorder inventory,\nand plan content — on time."),
        ("TOTALLY CUSTOMIZABLE", "Rename fields, add rows,\nchange categories. Built to\nadapt to YOUR business."),
        ("NO LEARNING CURVE", "Pre-built formulas, dropdown\nmenus, and a complete How-to\nGuide. Ready in 5 minutes."),
    ]

    font_ben_title = get_font(38, bold=True)
    font_ben_body = get_font(28)

    col_w = 760
    row_h = 280
    start_x = (W - 3 * col_w) // 2
    start_y = 660

    for idx, (title, body) in enumerate(benefits):
        col = idx % 3
        row = idx // 3
        x = start_x + col * col_w + 40
        y = start_y + row * row_h

        cx, cy = x + 45, y + 45
        draw.ellipse([(cx-35, cy-35), (cx+35, cy+35)], fill=DUSTY_BLUE)
        font_check2 = get_font(36, bold=True)
        draw.text((cx - 14, cy - 20), "✓", font=font_check2, fill=WHITE)

        draw_text_at(draw, title, x + 100, y + 15, font_ben_title, NAVY)
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw_text_at(draw, line, x + 100, y + 70 + li * 40, font_ben_body, DARK_TEXT)

    # Testimonial
    test_y = 1280
    draw_rounded_rect(draw, (200, test_y, W - 200, test_y + 250), 20, ICE_BLUE, outline=DUSTY_BLUE, width=2)
    font_star = get_font(48)
    draw_centered_text(draw, "★ ★ ★ ★ ★", test_y + 20, font_star, WARM_GOLD)
    font_quote = get_font(32)
    draw_centered_text(draw, '"I was drowning in spreadsheets, notebooks, and random apps.', test_y + 85, font_quote, DARK_TEXT)
    draw_centered_text(draw, 'This bundle replaced ALL of them. My business has never been more organized."', test_y + 130, font_quote, DARK_TEXT)
    font_attr = get_font(26, bold=True)
    draw_centered_text(draw, "— What small business owners are saying", test_y + 195, font_attr, STEEL_BLUE)

    # Bottom CTA
    cta_y = 1580
    draw.rectangle([(0, cta_y), (W, H)], fill=NAVY)
    font_cta = get_font(56, bold=True)
    draw_centered_text(draw, "ORGANIZE YOUR BUSINESS TODAY", cta_y + 50, font_cta, WHITE)

    btn_w, btn_h = 700, 85
    btn_x = (W - btn_w) // 2
    btn_y = cta_y + 150
    draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), 42, CORAL)
    font_btn = get_font(38, bold=True)
    draw_centered_text(draw, "INSTANT DIGITAL DOWNLOAD", btn_y + 20, font_btn, WHITE)

    font_sm = get_font(26)
    draw_centered_text(draw, "Buy once, use forever  |  No subscriptions  |  No physical item shipped", cta_y + 280, font_sm, PALE_BLUE)
    draw_centered_text(draw, "$12.99  |  9 Professional Tabs  |  Google Sheets + Excel", cta_y + 320, font_sm, WARM_GOLD)

    draw.rectangle([(0, H - 20), (W, H)], fill=CORAL)

    img.save(os.path.join(OUT_DIR, "05_value_proposition.png"), quality=95)
    print("Created: 05_value_proposition.png")


if __name__ == "__main__":
    create_hero_image()
    create_features_image()
    create_dashboard_mockup()
    create_content_inventory_image()
    create_value_prop_image()
    print(f"\nAll 5 listing images saved to: {OUT_DIR}")
