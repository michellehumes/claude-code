#!/usr/bin/env python3
"""Create 5 Etsy listing images for Social Media Marketing Planner 2026."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2700, 2025
OUT = "/home/user/claude-code/etsy-digital-download-6/images"
os.makedirs(OUT, exist_ok=True)

# Colors
HOT_PINK = (213, 63, 140)
PURPLE = (107, 70, 193)
ELECTRIC_BLUE = (49, 130, 206)
CORAL = (252, 129, 129)
MINT = (104, 211, 145)
PALE_PINK = (254, 215, 226)
DARK_TEXT = (26, 32, 44)
WHITE = (255, 255, 255)
LIGHT_GRAY = (247, 250, 252)
OFF_WHITE = (255, 248, 250)
SHADOW = (0, 0, 0, 40)

# Font helpers
def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_title = get_font(72, True)
font_subtitle = get_font(48, True)
font_medium = get_font(38, True)
font_body = get_font(32, False)
font_small = get_font(26, False)
font_tiny = get_font(22, False)
font_badge = get_font(28, True)
font_price = get_font(96, True)
font_hero = get_font(84, True)
font_big_title = get_font(68, True)
font_section = get_font(44, True)

def gradient_bg(draw, w, h, c1, c2, vertical=True):
    """Draw a gradient background."""
    for i in range(h if vertical else w):
        ratio = i / (h if vertical else w)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        if vertical:
            draw.line([(0, i), (w, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, h)], fill=(r, g, b))

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_ipad(img, draw, x, y, w, h, screen_content_func=None, shadow=True):
    """Draw an iPad mockup."""
    # Shadow
    if shadow:
        for s in range(12):
            alpha = 20 - s
            shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            sd = ImageDraw.Draw(shadow_layer)
            sd.rounded_rectangle(
                [x + s + 4, y + s + 6, x + w + s + 4, y + h + s + 6],
                radius=28, fill=(0, 0, 0, alpha)
            )
            img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0,0,0,0)), shadow_layer), mask=shadow_layer)
        draw = ImageDraw.Draw(img)

    # iPad body
    draw.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=(50, 50, 55), outline=(70, 70, 75), width=2)
    # Bezel
    bezel = 16
    draw.rounded_rectangle([x + bezel, y + bezel, x + w - bezel, y + h - bezel], radius=18, fill=WHITE)

    # Screen area
    sx, sy = x + bezel + 4, y + bezel + 4
    sw, sh = w - 2 * bezel - 8, h - 2 * bezel - 8

    if screen_content_func:
        screen_content_func(draw, sx, sy, sw, sh)

    return draw

def draw_content_calendar_screen(draw, sx, sy, sw, sh):
    """Draw content calendar spreadsheet on screen."""
    # Header bar
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=PURPLE)
    draw.text((sx + sw // 2, sy + 22), "CONTENT CALENDAR 2026", fill=WHITE, font=font_badge, anchor="mm")

    # Column headers
    cols = ["Date", "Day", "Platform", "Type", "Topic", "Status"]
    col_w = sw // len(cols)
    for i, c in enumerate(cols):
        cx = sx + i * col_w
        draw.rectangle([cx, sy + 46, cx + col_w, sy + 78], fill=HOT_PINK)
        draw.text((cx + col_w // 2, sy + 62), c, fill=WHITE, font=font_tiny, anchor="mm")

    # Data rows
    row_data = [
        ["Jan 1", "Thu", "Instagram", "Reel", "New Year Goals", "Scheduled"],
        ["Jan 2", "Fri", "TikTok", "Video", "Studio Tour BTS", "Draft"],
        ["Jan 3", "Sat", "Pinterest", "Photo", "Growth Infographic", "Idea"],
        ["Jan 4", "Sun", "LinkedIn", "Carousel", "Case Study: 10K", "Published"],
        ["Jan 5", "Mon", "Blog", "Blog", "Reels Guide 2026", "Draft"],
        ["Jan 6", "Tue", "YouTube", "Video", "Marketing Tips", "Idea"],
        ["Jan 7", "Wed", "Instagram", "Story", "Client Spotlight", "Scheduled"],
        ["Jan 8", "Thu", "TikTok", "Reel", "Trending Audio", "Published"],
        ["Jan 9", "Fri", "Email", "Newsletter", "Weekly Digest", "Scheduled"],
        ["Jan 10", "Sat", "Facebook", "Photo", "Community Post", "Idea"],
        ["Jan 11", "Sun", "Pinterest", "Photo", "Pin Design Tips", "Draft"],
        ["Jan 12", "Mon", "Instagram", "Carousel", "Tools Roundup", "Boosted"],
    ]

    status_colors = {
        "Published": MINT, "Scheduled": (179, 148, 244), "Draft": PALE_PINK,
        "Idea": LIGHT_GRAY, "Boosted": (107, 70, 193),
    }

    for ri, row in enumerate(row_data):
        ry = sy + 80 + ri * 32
        if ry + 32 > sy + sh:
            break
        bg = (255, 245, 247) if ri % 2 == 0 else WHITE
        draw.rectangle([sx, ry, sx + sw, ry + 32], fill=bg)
        for ci, val in enumerate(row):
            cx = sx + ci * col_w
            if ci == 5:  # Status column
                sc = status_colors.get(val, LIGHT_GRAY)
                pill_w = min(col_w - 10, 100)
                pill_x = cx + (col_w - pill_w) // 2
                draw.rounded_rectangle([pill_x, ry + 5, pill_x + pill_w, ry + 27], radius=10, fill=sc)
                tc = WHITE if val in ("Published", "Boosted") else DARK_TEXT
                draw.text((cx + col_w // 2, ry + 16), val, fill=tc, font=font_tiny, anchor="mm")
            else:
                draw.text((cx + col_w // 2, ry + 16), val, fill=DARK_TEXT, font=font_tiny, anchor="mm")

def draw_analytics_screen(draw, sx, sy, sw, sh):
    """Draw analytics dashboard on screen."""
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=PURPLE)
    draw.text((sx + sw // 2, sy + 22), "ANALYTICS DASHBOARD", fill=WHITE, font=font_badge, anchor="mm")

    # KPI boxes
    kpis = [
        ("7,970", "Followers\nGained", HOT_PINK),
        ("12,970", "Total\nFollowers", PURPLE),
        ("4.1%", "Avg\nEngagement", ELECTRIC_BLUE),
        ("$5,395", "Total\nRevenue", MINT),
    ]
    box_w = (sw - 40) // 4
    for i, (val, label, color) in enumerate(kpis):
        bx = sx + 8 + i * (box_w + 8)
        draw.rounded_rectangle([bx, sy + 52, bx + box_w, sy + 140], radius=12, fill=color)
        draw.text((bx + box_w // 2, sy + 82), val, fill=WHITE, font=font_badge, anchor="mm")
        draw.text((bx + box_w // 2, sy + 116), label.split("\n")[0], fill=WHITE, font=font_tiny, anchor="mm")

    # Mini bar chart
    chart_y = sy + 155
    chart_h = sh - 155 - 10
    months_short = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    values = [450, 520, 380, 610, 720, 550, 490, 680, 750, 820, 900, 1100]
    max_v = max(values)
    bar_w = (sw - 60) // 12
    for i, (m, v) in enumerate(zip(months_short, values)):
        bx = sx + 24 + i * bar_w
        bar_h = int((v / max_v) * (chart_h - 30))
        color = HOT_PINK if i % 2 == 0 else PURPLE
        draw.rectangle([bx + 4, chart_y + chart_h - 20 - bar_h, bx + bar_w - 4, chart_y + chart_h - 20], fill=color)
        draw.text((bx + bar_w // 2, chart_y + chart_h - 8), m, fill=DARK_TEXT, font=font_tiny, anchor="mm")

def draw_hashtag_screen(draw, sx, sy, sw, sh):
    """Draw hashtag research on screen."""
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=ELECTRIC_BLUE)
    draw.text((sx + sw // 2, sy + 22), "HASHTAG RESEARCH", fill=WHITE, font=font_badge, anchor="mm")

    cols = ["Hashtag", "Category", "Pop.", "Rating"]
    col_ws = [sw * 0.35, sw * 0.22, sw * 0.2, sw * 0.23]
    cx = sx
    for i, (c, cw) in enumerate(zip(cols, col_ws)):
        draw.rectangle([cx, sy + 46, cx + cw, sy + 76], fill=(64, 145, 215))
        draw.text((cx + cw // 2, sy + 61), c, fill=WHITE, font=font_tiny, anchor="mm")
        cx += cw

    rows = [
        ("#socialmedia...", "General", "25M", "High"),
        ("#digitalmarketing", "General", "30M", "High"),
        ("#contentcreator", "Creator", "18M", "High"),
        ("#instagramgrowth", "Instagram", "5M", "High"),
        ("#tiktokmarketing", "TikTok", "2M", "High"),
        ("#reelsinstagram", "Instagram", "12M", "Med"),
        ("#pinterestmktg", "Pinterest", "800K", "High"),
        ("#linkedintips", "LinkedIn", "3M", "Med"),
        ("#emailmarketing", "Email", "4M", "Med"),
        ("#smallbiztips", "Business", "10M", "High"),
    ]
    rating_colors = {"High": MINT, "Med": (255, 236, 153), "Low": CORAL}
    for ri, row in enumerate(rows):
        ry = sy + 78 + ri * 30
        if ry + 30 > sy + sh:
            break
        bg = (240, 248, 255) if ri % 2 == 0 else WHITE
        draw.rectangle([sx, ry, sx + sw, ry + 30], fill=bg)
        cx = sx
        for ci, (val, cw) in enumerate(zip(row, col_ws)):
            if ci == 3:
                rc = rating_colors.get(val, LIGHT_GRAY)
                pw = min(cw - 16, 70)
                px = cx + (cw - pw) // 2
                draw.rounded_rectangle([px, ry + 4, px + pw, ry + 26], radius=8, fill=rc)
                draw.text((cx + cw // 2, ry + 15), val, fill=DARK_TEXT, font=font_tiny, anchor="mm")
            else:
                draw.text((cx + cw // 2, ry + 15), val, fill=DARK_TEXT, font=font_tiny, anchor="mm")
            cx += cw

def draw_collab_screen(draw, sx, sy, sw, sh):
    """Draw brand collaborations on screen."""
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=CORAL)
    draw.text((sx + sw // 2, sy + 22), "BRAND COLLABORATIONS", fill=WHITE, font=font_badge, anchor="mm")

    cols = ["Brand", "Platform", "Payment", "Status"]
    col_ws = [sw * 0.3, sw * 0.22, sw * 0.22, sw * 0.26]
    cx = sx
    for i, (c, cw) in enumerate(zip(cols, col_ws)):
        draw.rectangle([cx, sy + 46, cx + cw, sy + 76], fill=(240, 120, 120))
        draw.text((cx + cw // 2, sy + 61), c, fill=WHITE, font=font_tiny, anchor="mm")
        cx += cw

    rows = [
        ("GlowUp Skin", "Instagram", "$1,500", "Confirmed"),
        ("TechNova", "TikTok", "$800", "Negotiating"),
        ("Bloom Tea", "Pinterest", "$600", "Pitched"),
        ("FitLife Gym", "YouTube", "$2,000", "Confirmed"),
        ("EcoWear", "Instagram", "$1,200", "Pitched"),
    ]
    status_c = {"Confirmed": (179, 148, 244), "Pitched": PALE_PINK, "Negotiating": (255, 236, 153), "Paid": MINT, "Completed": MINT}
    for ri, row in enumerate(rows):
        ry = sy + 78 + ri * 36
        if ry + 36 > sy + sh:
            break
        bg = (255, 245, 245) if ri % 2 == 0 else WHITE
        draw.rectangle([sx, ry, sx + sw, ry + 36], fill=bg)
        cx = sx
        for ci, (val, cw) in enumerate(zip(row, col_ws)):
            if ci == 3:
                sc = status_c.get(val, LIGHT_GRAY)
                pw = min(cw - 12, 100)
                px = cx + (cw - pw) // 2
                draw.rounded_rectangle([px, ry + 5, px + pw, ry + 31], radius=10, fill=sc)
                draw.text((cx + cw // 2, ry + 18), val, fill=DARK_TEXT, font=font_tiny, anchor="mm")
            else:
                draw.text((cx + cw // 2, ry + 18), val, fill=DARK_TEXT, font=font_tiny, anchor="mm")
            cx += cw

def draw_ideas_screen(draw, sx, sy, sw, sh):
    """Draw content ideas bank on screen."""
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=MINT)
    draw.text((sx + sw // 2, sy + 22), "CONTENT IDEAS BANK", fill=WHITE, font=font_badge, anchor="mm")
    ideas_mini = [
        "Day in the life of a SM manager",
        "Before & after: brand transformation",
        "5 tools every marketer needs",
        "Monthly analytics review",
        "Trending audio + niche tip",
        "Client testimonial spotlight",
        "How to schedule a week in 1hr",
    ]
    for i, idea in enumerate(ideas_mini):
        ry = sy + 56 + i * 34
        if ry + 30 > sy + sh:
            break
        bg = (240, 255, 245) if i % 2 == 0 else WHITE
        draw.rectangle([sx + 6, ry, sx + sw - 6, ry + 30], fill=bg)
        draw.rounded_rectangle([sx + 10, ry + 4, sx + 30, ry + 26], radius=6, fill=MINT)
        draw.text((sx + 20, ry + 15), str(i + 1), fill=WHITE, font=font_tiny, anchor="mm")
        draw.text((sx + 38, ry + 15), idea, fill=DARK_TEXT, font=font_tiny, anchor="lm")

def draw_audience_screen(draw, sx, sy, sw, sh):
    """Draw audience insights on screen."""
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=HOT_PINK)
    draw.text((sx + sw // 2, sy + 22), "AUDIENCE INSIGHTS", fill=WHITE, font=font_badge, anchor="mm")

    platforms = [
        ("Instagram", "8.5K", "4.8%", HOT_PINK),
        ("TikTok", "12K", "6.2%", DARK_TEXT),
        ("YouTube", "3.2K", "3.1%", (255, 0, 0)),
        ("Pinterest", "5.8K", "2.5%", (189, 37, 55)),
        ("LinkedIn", "6.2K", "3.5%", ELECTRIC_BLUE),
    ]
    for i, (plat, foll, eng, color) in enumerate(platforms):
        ry = sy + 56 + i * 42
        if ry + 40 > sy + sh:
            break
        bg = (255, 245, 247) if i % 2 == 0 else WHITE
        draw.rectangle([sx + 6, ry, sx + sw - 6, ry + 38], fill=bg)
        draw.rounded_rectangle([sx + 10, ry + 5, sx + 14 + 8, ry + 33], radius=4, fill=color)
        draw.text((sx + 30, ry + 19), plat, fill=DARK_TEXT, font=font_tiny, anchor="lm")
        draw.text((sx + sw * 0.55, ry + 19), foll, fill=PURPLE, font=font_badge, anchor="mm")
        draw.text((sx + sw * 0.82, ry + 19), eng, fill=MINT, font=font_badge, anchor="mm")

def draw_revenue_screen(draw, sx, sy, sw, sh):
    """Draw revenue tracker on screen."""
    draw.rectangle([sx, sy, sx + sw, sy + 44], fill=PURPLE)
    draw.text((sx + sw // 2, sy + 22), "REVENUE TRACKER", fill=WHITE, font=font_badge, anchor="mm")

    # Total box
    draw.rounded_rectangle([sx + 10, sy + 52, sx + sw - 10, sy + 110], radius=12, fill=HOT_PINK)
    draw.text((sx + sw // 2, sy + 72), "TOTAL REVENUE", fill=WHITE, font=font_tiny, anchor="mm")
    draw.text((sx + sw // 2, sy + 96), "$7,845.00", fill=WHITE, font=font_badge, anchor="mm")

    entries = [
        ("Jan 05", "Sponsorship", "$1,500"),
        ("Jan 12", "Affiliate", "$245"),
        ("Jan 20", "Product", "$890"),
        ("Feb 01", "Sponsorship", "$800"),
        ("Feb 10", "Coaching", "$350"),
    ]
    for i, (date, src, amt) in enumerate(entries):
        ry = sy + 120 + i * 32
        if ry + 30 > sy + sh:
            break
        bg = (248, 240, 255) if i % 2 == 0 else WHITE
        draw.rectangle([sx + 6, ry, sx + sw - 6, ry + 30], fill=bg)
        draw.text((sx + 14, ry + 15), date, fill=DARK_TEXT, font=font_tiny, anchor="lm")
        draw.text((sx + sw * 0.45, ry + 15), src, fill=PURPLE, font=font_tiny, anchor="mm")
        draw.text((sx + sw - 14, ry + 15), amt, fill=MINT, font=font_badge, anchor="rm")

def draw_platform_badges(draw, cx, y, platforms_list):
    """Draw platform badge pills."""
    total_w = len(platforms_list) * 160
    start_x = cx - total_w // 2
    colors = [HOT_PINK, PURPLE, ELECTRIC_BLUE, CORAL, MINT, (107, 70, 193), (49, 130, 206)]
    for i, p in enumerate(platforms_list):
        bx = start_x + i * 160
        c = colors[i % len(colors)]
        draw.rounded_rectangle([bx, y, bx + 148, y + 38], radius=19, fill=c)
        draw.text((bx + 74, y + 19), p, fill=WHITE, font=font_small, anchor="mm")

# ═══════════════════════════════════════════════════════════════
# IMAGE 1: Hero - iPad with Content Calendar + platform badges
# ═══════════════════════════════════════════════════════════════
def create_image_1():
    img = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (254, 215, 226), (237, 220, 255))

    # Decorative circles
    draw.ellipse([-100, -100, 400, 400], fill=(213, 63, 140, 30))
    draw.ellipse([W - 350, H - 350, W + 100, H + 100], fill=(107, 70, 193, 30))
    draw.ellipse([W - 600, -150, W - 100, 350], fill=(49, 130, 206, 20))

    # Title
    draw.text((W // 2, 100), "SOCIAL MEDIA", fill=HOT_PINK, font=font_hero, anchor="mm")
    draw.text((W // 2, 190), "MARKETING PLANNER", fill=PURPLE, font=font_hero, anchor="mm")
    draw.text((W // 2, 270), "2 0 2 6", fill=ELECTRIC_BLUE, font=font_title, anchor="mm")

    # Subtitle
    draw.text((W // 2, 340), "Plan  |  Schedule  |  Track  |  Grow  |  Monetize", fill=DARK_TEXT, font=font_medium, anchor="mm")

    # Platform badges
    platforms = ["Instagram", "TikTok", "YouTube", "Pinterest", "LinkedIn", "Facebook"]
    draw_platform_badges(draw, W // 2, 395, platforms)

    # Main iPad
    ipad_w, ipad_h = 1500, 1050
    ipad_x = (W - ipad_w) // 2
    ipad_y = 490
    draw = draw_ipad(img, draw, ipad_x, ipad_y, ipad_w, ipad_h, draw_content_calendar_screen)

    # Feature badges at bottom
    features = ["8 Professional Tabs", "Auto-Formulas", "Dropdown Menus", "100+ Pre-filled Rows"]
    badge_w = 280
    total = len(features) * (badge_w + 20) - 20
    start_x = (W - total) // 2
    for i, f in enumerate(features):
        bx = start_x + i * (badge_w + 20)
        by = H - 120
        color = [HOT_PINK, PURPLE, ELECTRIC_BLUE, MINT][i]
        draw.rounded_rectangle([bx, by, bx + badge_w, by + 56], radius=28, fill=color)
        draw.text((bx + badge_w // 2, by + 28), f, fill=WHITE, font=font_small, anchor="mm")

    # Watermark
    draw.text((W // 2, H - 40), "Instant Digital Download  |  Excel & Google Sheets Compatible", fill=DARK_TEXT, font=font_small, anchor="mm")

    img.convert("RGB").save(os.path.join(OUT, "01_hero_main_listing.png"), quality=95)
    print("Created 01_hero_main_listing.png")

# ═══════════════════════════════════════════════════════════════
# IMAGE 2: 7 mini iPads showing all tabs
# ═══════════════════════════════════════════════════════════════
def create_image_2():
    img = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (237, 220, 255), (254, 215, 226))

    # Title
    draw.text((W // 2, 70), "8 PROFESSIONAL TABS INCLUDED", fill=PURPLE, font=font_big_title, anchor="mm")
    draw.text((W // 2, 130), "Everything You Need to Dominate Social Media in 2026", fill=DARK_TEXT, font=font_body, anchor="mm")

    # 7 mini iPads in 2 rows (4 + 3)
    screens = [
        ("Content Calendar", draw_content_calendar_screen, HOT_PINK),
        ("Analytics", draw_analytics_screen, PURPLE),
        ("Hashtags", draw_hashtag_screen, ELECTRIC_BLUE),
        ("Collaborations", draw_collab_screen, CORAL),
        ("Ideas Bank", draw_ideas_screen, MINT),
        ("Audience", draw_audience_screen, HOT_PINK),
        ("Revenue", draw_revenue_screen, PURPLE),
    ]

    # Row 1: 4 iPads
    mini_w, mini_h = 560, 420
    row1_y = 200
    for i in range(4):
        mx = 80 + i * (mini_w + 50)
        draw = draw_ipad(img, draw, mx, row1_y, mini_w, mini_h, screens[i][1])
        # Label
        color = screens[i][2]
        lx = mx + mini_w // 2
        ly = row1_y + mini_h + 20
        draw.rounded_rectangle([lx - 100, ly, lx + 100, ly + 34], radius=17, fill=color)
        draw.text((lx, ly + 17), screens[i][0], fill=WHITE, font=font_small, anchor="mm")

    # Row 2: 3 iPads centered
    row2_y = 720
    offset_x = (W - 3 * mini_w - 2 * 50) // 2
    for i in range(3):
        mx = offset_x + i * (mini_w + 50)
        draw = draw_ipad(img, draw, mx, row2_y, mini_w, mini_h, screens[4 + i][1])
        color = screens[4 + i][2]
        lx = mx + mini_w // 2
        ly = row2_y + mini_h + 20
        draw.rounded_rectangle([lx - 100, ly, lx + 100, ly + 34], radius=17, fill=color)
        draw.text((lx, ly + 17), screens[4 + i][0], fill=WHITE, font=font_small, anchor="mm")

    # 8th tab note
    draw.rounded_rectangle([W // 2 - 200, H - 200, W // 2 + 200, H - 140], radius=25, fill=PALE_PINK)
    draw.text((W // 2, H - 170), "+ How to Use Guide Tab", fill=HOT_PINK, font=font_medium, anchor="mm")

    # Bottom
    draw.text((W // 2, H - 100), "Social Media Marketing Planner 2026  |  Instant Download", fill=DARK_TEXT, font=font_body, anchor="mm")
    draw.text((W // 2, H - 55), "Works with Excel, Google Sheets, Numbers", fill=PURPLE, font=font_small, anchor="mm")

    img.convert("RGB").save(os.path.join(OUT, "02_all_tabs_overview.png"), quality=95)
    print("Created 02_all_tabs_overview.png")

# ═══════════════════════════════════════════════════════════════
# IMAGE 3: Two iPads - Content Calendar + Analytics
# ═══════════════════════════════════════════════════════════════
def create_image_3():
    img = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (254, 215, 226), (220, 230, 255))

    # Title
    draw.text((W // 2, 80), "PLAN YOUR CONTENT + TRACK YOUR GROWTH", fill=HOT_PINK, font=font_subtitle, anchor="mm")
    draw.text((W // 2, 140), "Two Powerful Tabs Working Together", fill=PURPLE, font=font_body, anchor="mm")

    # Left iPad - Content Calendar
    ipad_w, ipad_h = 1150, 850
    draw = draw_ipad(img, draw, 80, 250, ipad_w, ipad_h, draw_content_calendar_screen)
    draw.rounded_rectangle([80 + ipad_w // 2 - 140, 1120, 80 + ipad_w // 2 + 140, 1160], radius=20, fill=HOT_PINK)
    draw.text((80 + ipad_w // 2, 1140), "Content Calendar", fill=WHITE, font=font_badge, anchor="mm")

    # Right iPad - Analytics
    draw = draw_ipad(img, draw, W - 80 - ipad_w, 250, ipad_w, ipad_h, draw_analytics_screen)
    draw.rounded_rectangle([W - 80 - ipad_w // 2 - 140, 1120, W - 80 - ipad_w // 2 + 140, 1160], radius=20, fill=PURPLE)
    draw.text((W - 80 - ipad_w // 2, 1140), "Analytics Dashboard", fill=WHITE, font=font_badge, anchor="mm")

    # Feature bullets
    features_left = ["100 Pre-filled Date Rows", "Platform & Status Dropdowns", "Auto Day-of-Week Formula"]
    features_right = ["Monthly Growth Tracking", "Auto-Calculated Totals", "Revenue from Social"]

    for i, f in enumerate(features_left):
        fy = 1220 + i * 50
        draw.ellipse([200, fy, 216, fy + 16], fill=HOT_PINK)
        draw.text((230, fy + 8), f, fill=DARK_TEXT, font=font_body, anchor="lm")

    for i, f in enumerate(features_right):
        fy = 1220 + i * 50
        draw.ellipse([W - 900, fy, W - 884, fy + 16], fill=PURPLE)
        draw.text((W - 870, fy + 8), f, fill=DARK_TEXT, font=font_body, anchor="lm")

    # Arrow between iPads
    arrow_y = 650
    for i in range(20):
        ax = W // 2 - 40 + i * 4
        draw.ellipse([ax, arrow_y - 2, ax + 6, arrow_y + 6], fill=ELECTRIC_BLUE)

    # Bottom bar
    draw.rounded_rectangle([W // 2 - 450, H - 80, W // 2 + 450, H - 30], radius=25, fill=PALE_PINK)
    draw.text((W // 2, H - 55), "Social Media Marketing Planner 2026  |  $9.99 Instant Download", fill=HOT_PINK, font=font_medium, anchor="mm")

    img.convert("RGB").save(os.path.join(OUT, "03_calendar_analytics.png"), quality=95)
    print("Created 03_calendar_analytics.png")

# ═══════════════════════════════════════════════════════════════
# IMAGE 4: Two iPads - Hashtags + Brand Collaborations
# ═══════════════════════════════════════════════════════════════
def create_image_4():
    img = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (220, 230, 255), (254, 215, 226))

    draw.text((W // 2, 80), "RESEARCH HASHTAGS + MANAGE BRAND DEALS", fill=ELECTRIC_BLUE, font=font_subtitle, anchor="mm")
    draw.text((W // 2, 140), "Grow Faster and Get Paid for Your Content", fill=DARK_TEXT, font=font_body, anchor="mm")

    ipad_w, ipad_h = 1150, 850
    draw = draw_ipad(img, draw, 80, 250, ipad_w, ipad_h, draw_hashtag_screen)
    draw.rounded_rectangle([80 + ipad_w // 2 - 140, 1120, 80 + ipad_w // 2 + 140, 1160], radius=20, fill=ELECTRIC_BLUE)
    draw.text((80 + ipad_w // 2, 1140), "Hashtag Research", fill=WHITE, font=font_badge, anchor="mm")

    draw = draw_ipad(img, draw, W - 80 - ipad_w, 250, ipad_w, ipad_h, draw_collab_screen)
    draw.rounded_rectangle([W - 80 - ipad_w // 2 - 160, 1120, W - 80 - ipad_w // 2 + 160, 1160], radius=20, fill=CORAL)
    draw.text((W - 80 - ipad_w // 2, 1140), "Brand Collaborations", fill=WHITE, font=font_badge, anchor="mm")

    features_left = ["Popularity & Relevance Scores", "Performance Rating Dropdowns", "Category Organization"]
    features_right = ["Pitch-to-Payment Pipeline", "Deadline & Deliverable Tracking", "5 Status Stages"]

    for i, f in enumerate(features_left):
        fy = 1220 + i * 50
        draw.ellipse([200, fy, 216, fy + 16], fill=ELECTRIC_BLUE)
        draw.text((230, fy + 8), f, fill=DARK_TEXT, font=font_body, anchor="lm")

    for i, f in enumerate(features_right):
        fy = 1220 + i * 50
        draw.ellipse([W - 900, fy, W - 884, fy + 16], fill=CORAL)
        draw.text((W - 870, fy + 8), f, fill=DARK_TEXT, font=font_body, anchor="lm")

    # Arrow
    arrow_y = 650
    for i in range(20):
        ax = W // 2 - 40 + i * 4
        draw.ellipse([ax, arrow_y - 2, ax + 6, arrow_y + 6], fill=HOT_PINK)

    draw.rounded_rectangle([W // 2 - 450, H - 80, W // 2 + 450, H - 30], radius=25, fill=PALE_PINK)
    draw.text((W // 2, H - 55), "20 Hashtags Pre-Loaded  |  5 Sample Brand Deals Included", fill=HOT_PINK, font=font_medium, anchor="mm")

    img.convert("RGB").save(os.path.join(OUT, "04_hashtags_collaborations.png"), quality=95)
    print("Created 04_hashtags_collaborations.png")

# ═══════════════════════════════════════════════════════════════
# IMAGE 5: Value Proposition - "$9.99 INSTANT DOWNLOAD"
# ═══════════════════════════════════════════════════════════════
def create_image_5():
    img = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, PURPLE, HOT_PINK)

    # Decorative shapes
    draw.ellipse([W - 500, -200, W + 100, 400], fill=(255, 255, 255, 15))
    draw.ellipse([-200, H - 400, 400, H + 100], fill=(255, 255, 255, 15))

    # Price banner
    draw.text((W // 2, 180), "ONLY", fill=PALE_PINK, font=font_subtitle, anchor="mm")
    draw.text((W // 2, 310), "$9.99", fill=WHITE, font=get_font(160, True), anchor="mm")
    draw.text((W // 2, 410), "INSTANT DOWNLOAD", fill=PALE_PINK, font=font_big_title, anchor="mm")

    # Divider line
    draw.line([(W // 2 - 400, 470), (W // 2 + 400, 470)], fill=PALE_PINK, width=3)

    # Product title
    draw.text((W // 2, 530), "SOCIAL MEDIA MARKETING PLANNER 2026", fill=WHITE, font=font_subtitle, anchor="mm")

    # What's included - two columns
    left_items = [
        "Content Calendar (100 Rows)",
        "Analytics Dashboard",
        "Hashtag Research Tracker",
        "Brand Collaborations Tracker",
    ]
    right_items = [
        "Content Ideas Bank (25 Ideas)",
        "Audience Insights by Platform",
        "Revenue Tracker",
        "How to Use Guide + 20 Bonus Ideas",
    ]

    for i, item in enumerate(left_items):
        iy = 620 + i * 60
        draw.text((W // 4 + 80, iy), item, fill=WHITE, font=font_medium, anchor="lm")
        draw.rounded_rectangle([W // 4 + 30, iy - 14, W // 4 + 66, iy + 14], radius=14, fill=MINT)
        draw.text((W // 4 + 48, iy), "\u2713", fill=WHITE, font=font_badge, anchor="mm")

    for i, item in enumerate(right_items):
        iy = 620 + i * 60
        draw.text((W * 3 // 4 - 350 + 80, iy), item, fill=WHITE, font=font_medium, anchor="lm")
        draw.rounded_rectangle([W * 3 // 4 - 350 + 30, iy - 14, W * 3 // 4 - 350 + 66, iy + 14], radius=14, fill=MINT)
        draw.text((W * 3 // 4 - 350 + 48, iy), "\u2713", fill=WHITE, font=font_badge, anchor="mm")

    # Divider
    draw.line([(W // 2 - 400, 880), (W // 2 + 400, 880)], fill=PALE_PINK, width=3)

    # Bonus features row
    bonuses = [
        ("Auto-Formulas", "Save Hours"),
        ("Dropdown Menus", "Stay Organized"),
        ("Color-Coded", "See Status Fast"),
        ("Pre-Filled Data", "Start Instantly"),
    ]
    for i, (title, sub) in enumerate(bonuses):
        bx = 200 + i * 580
        by = 930
        draw.rounded_rectangle([bx, by, bx + 500, by + 120], radius=20, fill=(255, 255, 255, 30))
        draw.text((bx + 250, by + 40), title, fill=WHITE, font=font_medium, anchor="mm")
        draw.text((bx + 250, by + 85), sub, fill=PALE_PINK, font=font_body, anchor="mm")

    # Compatibility
    draw.text((W // 2, 1140), "Works With:", fill=PALE_PINK, font=font_body, anchor="mm")
    apps = ["Microsoft Excel", "Google Sheets", "Apple Numbers", "LibreOffice"]
    total_w = len(apps) * 300
    start_x = (W - total_w) // 2
    for i, app in enumerate(apps):
        ax = start_x + i * 300
        draw.rounded_rectangle([ax, 1175, ax + 270, 1220], radius=22, fill=(255, 255, 255, 40))
        draw.text((ax + 135, 1198), app, fill=WHITE, font=font_badge, anchor="mm")

    # CTA
    draw.rounded_rectangle([W // 2 - 350, 1280, W // 2 + 350, 1360], radius=35, fill=WHITE)
    draw.text((W // 2, 1320), "ADD TO CART  |  INSTANT DOWNLOAD", fill=HOT_PINK, font=font_medium, anchor="mm")

    # Bottom text
    draw.text((W // 2, 1420), "No physical product will be shipped. This is a digital download.", fill=PALE_PINK, font=font_body, anchor="mm")
    draw.text((W // 2, 1470), "Start planning your social media success TODAY!", fill=WHITE, font=font_medium, anchor="mm")

    # Stars
    stars = "\u2605 \u2605 \u2605 \u2605 \u2605"
    draw.text((W // 2, 1540), stars, fill=(255, 236, 153), font=font_subtitle, anchor="mm")
    draw.text((W // 2, 1600), "Join 5,000+ Happy Social Media Marketers", fill=PALE_PINK, font=font_body, anchor="mm")

    img.convert("RGB").save(os.path.join(OUT, "05_value_proposition.png"), quality=95)
    print("Created 05_value_proposition.png")

# Run all
create_image_1()
create_image_2()
create_image_3()
create_image_4()
create_image_5()
print("\nAll 5 images created successfully!")
