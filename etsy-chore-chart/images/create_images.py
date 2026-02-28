#!/usr/bin/env python3
"""
Etsy Listing Images for Kids Chore Chart System
7 images at 2700 x 2025 px, 4:3 ratio, 300 DPI, RGB
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── DIMENSIONS ────────────────────────────────────────────────────────────────
W, H = 2700, 2025
MARGIN = 150
DPI = 300

# ── COLORS ────────────────────────────────────────────────────────────────────
C = {
    "bg":           (250, 251, 252),
    "white":        (255, 255, 255),
    "primary":      (74, 144, 217),
    "primary_dark":  (44, 62, 80),
    "primary_light": (214, 228, 240),
    "secondary":    (245, 166, 35),
    "secondary_light": (255, 243, 214),
    "success":      (39, 174, 96),
    "success_light": (213, 245, 227),
    "incomplete":   (224, 224, 224),
    "gray_text":    (153, 153, 153),
    "dark_text":    (44, 62, 80),
    "sub_header":   (52, 73, 94),
    "border":       (189, 195, 199),
    "input_bg":     (255, 255, 240),
    "danger":       (231, 76, 60),
    "badge_bg":     (248, 249, 250),
}


# ── FONT HELPERS ──────────────────────────────────────────────────────────────
def get_font(size, bold=False):
    """Get a system font, fallback to default."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ── DRAWING HELPERS ───────────────────────────────────────────────────────────
def new_image():
    img = Image.new("RGB", (W, H), C["bg"])
    return img, ImageDraw.Draw(img)


def draw_rounded_rect(draw, xy, fill, radius=20, outline=None, width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_header_bar(draw, y, text, fill=None, text_color=None, height=90, font_size=38):
    fill = fill or C["primary_dark"]
    text_color = text_color or C["white"]
    draw_rounded_rect(draw, (MARGIN, y, W - MARGIN, y + height), fill=fill, radius=12)
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y + (height - font_size) // 2 - 2), text, fill=text_color, font=font)


def draw_title_section(draw, headline, subheadline=None, y_start=100):
    font_h = get_font(72, bold=True)
    bbox = draw.textbbox((0, 0), headline, font=font_h)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y_start), headline, fill=C["primary_dark"], font=font_h)

    y_next = y_start + 90
    if subheadline:
        font_sub = get_font(34, bold=False)
        bbox = draw.textbbox((0, 0), subheadline, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y_next), subheadline, fill=C["gray_text"], font=font_sub)
        y_next += 55

    # Divider
    y_next += 15
    draw.line([(MARGIN + 200, y_next), (W - MARGIN - 200, y_next)], fill=C["primary"], width=4)
    return y_next + 30


def draw_chore_grid_mini(draw, x, y, w, h, title="Chore Chart", rows=8):
    """Draw a miniature chore grid preview."""
    draw_rounded_rect(draw, (x, y, x+w, y+h), fill=C["white"], radius=14,
                      outline=C["border"], width=2)

    # Header
    draw_rounded_rect(draw, (x, y, x+w, y+50), fill=C["primary_dark"], radius=14)
    draw_rounded_rect(draw, (x, y+35, x+w, y+50), fill=C["primary_dark"], radius=0)
    font = get_font(22, bold=True)
    bbox = draw.textbbox((0, 0), title, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw) // 2, y + 12), title, fill=C["white"], font=font)

    # Column headers
    col_h_y = y + 55
    draw.rectangle((x+2, col_h_y, x+w-2, col_h_y+28), fill=C["sub_header"])
    small = get_font(13, bold=True)
    labels = ["CHORE", "M", "T", "W", "T", "F", "S", "S", "PTS"]
    positions = [x+10, x+w*0.42, x+w*0.48, x+w*0.54, x+w*0.60, x+w*0.66, x+w*0.72, x+w*0.78, x+w*0.88]
    for lbl, px in zip(labels, positions):
        draw.text((int(px), col_h_y+6), lbl, fill=C["white"], font=small)

    # Rows
    row_font = get_font(13, bold=False)
    chore_names = ["Make Bed", "Brush Teeth", "Pick Up Toys", "Set Table", "Clear Dishes", "Feed Pet", "Pack Bag", "Tidy Room"]
    for i in range(rows):
        ry = col_h_y + 30 + i * 26
        bg = C["primary_light"] if i % 2 == 1 else C["white"]
        draw.rectangle((x+2, ry, x+w-2, ry+24), fill=bg)

        if i < len(chore_names):
            draw.text((x+10, ry+4), chore_names[i], fill=C["dark_text"], font=row_font)

        # Checkmarks (random pattern)
        check_font = get_font(15, bold=True)
        pattern = [
            [1,1,0,1,1,0,1],
            [1,1,1,1,1,1,1],
            [0,1,1,0,1,1,0],
            [1,0,1,1,1,0,1],
            [1,1,1,1,0,1,1],
            [0,1,0,1,1,1,0],
            [1,1,1,0,1,0,1],
            [1,1,1,1,1,1,0],
        ]
        for j in range(7):
            cx = int(positions[1 + j])
            if i < len(pattern) and pattern[i][j]:
                draw.text((cx, ry+3), "✓", fill=C["success"], font=check_font)

        # Points
        pts = sum(pattern[i]) if i < len(pattern) else 0
        draw.text((int(positions[8]), ry+4), str(pts), fill=C["secondary"], font=row_font)


def draw_progress_bar_mini(draw, x, y, w, h, pct=0.72, color=None):
    """Draw a mini progress bar."""
    color = color or C["primary"]
    draw_rounded_rect(draw, (x, y, x+w, y+h), fill=C["incomplete"], radius=h//2)
    fill_w = max(h, int(w * pct))
    draw_rounded_rect(draw, (x, y, x+fill_w, y+h), fill=color, radius=h//2)
    font = get_font(int(h*0.6), bold=True)
    text = f"{int(pct*100)}%"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + fill_w//2 - tw//2, y + 2), text, fill=C["white"], font=font)


def draw_bullet(draw, x, y, text, icon_color=None, font_size=28):
    icon_color = icon_color or C["primary"]
    font = get_font(font_size, bold=False)
    # Bullet circle
    draw.ellipse((x, y+6, x+18, y+24), fill=icon_color)
    draw.text((x + 32, y), text, fill=C["dark_text"], font=font)


def draw_callout_box(draw, x, y, w, h, text, icon_color=None):
    icon_color = icon_color or C["primary"]
    draw_rounded_rect(draw, (x, y, x+w, y+h), fill=C["white"], radius=12,
                      outline=C["border"], width=2)
    # Left accent bar
    draw_rounded_rect(draw, (x, y, x+8, y+h), fill=icon_color, radius=4)

    font = get_font(22, bold=False)
    # Word wrap
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > w - 40:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test
    if current_line:
        lines.append(current_line)

    ty = y + (h - len(lines) * 30) // 2
    for line in lines:
        draw.text((x + 24, ty), line, fill=C["dark_text"], font=font)
        ty += 30


def draw_step_circle(draw, cx, cy, number, size=70):
    draw.ellipse((cx - size//2, cy - size//2, cx + size//2, cy + size//2), fill=C["primary"])
    font = get_font(36, bold=True)
    text = str(number)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2 - 4), text, fill=C["white"], font=font)


def draw_badge(draw, x, y, text, bg_color=None, text_color=None):
    bg_color = bg_color or C["primary"]
    text_color = text_color or C["white"]
    font = get_font(22, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    pad = 24
    draw_rounded_rect(draw, (x, y, x + tw + pad*2, y + 44), fill=bg_color, radius=22)
    draw.text((x + pad, y + 10), text, fill=text_color, font=font)
    return tw + pad * 2


def draw_bottom_strip(draw, texts, y=None):
    y = y or (H - MARGIN - 60)
    draw_rounded_rect(draw, (MARGIN, y, W - MARGIN, y + 55), fill=C["primary_dark"], radius=10)
    font = get_font(22, bold=True)
    total_w = 0
    spacer = 80
    widths = []
    for t in texts:
        bbox = draw.textbbox((0, 0), t, font=font)
        widths.append(bbox[2] - bbox[0])
        total_w += bbox[2] - bbox[0]
    total_w += spacer * (len(texts) - 1)
    sx = (W - total_w) // 2
    for i, (t, tw) in enumerate(zip(texts, widths)):
        draw.text((sx, y + 14), t, fill=C["white"], font=font)
        sx += tw + spacer
        if i < len(texts) - 1:
            # Dot separator
            draw.ellipse((sx - spacer//2 - 5, y + 24, sx - spacer//2 + 5, y + 34), fill=C["secondary"])


def draw_sheet_preview(draw, x, y, w, h, title, accent_color, content_lines=None):
    """Draw a sheet preview card."""
    draw_rounded_rect(draw, (x, y, x+w, y+h), fill=C["white"], radius=14,
                      outline=C["border"], width=2)
    # Tab accent
    draw_rounded_rect(draw, (x, y, x+w, y+52), fill=accent_color, radius=14)
    draw_rounded_rect(draw, (x, y+38, x+w, y+52), fill=accent_color, radius=0)
    font = get_font(22, bold=True)
    bbox = draw.textbbox((0, 0), title, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w-tw)//2, y+14), title, fill=C["white"], font=font)

    if content_lines:
        small = get_font(16, bold=False)
        cy = y + 65
        for line in content_lines:
            if cy + 22 > y + h - 10:
                break
            draw.text((x + 16, cy), line, fill=C["dark_text"], font=small)
            cy += 24


def save_image(img, name):
    path = f"/home/user/claude-code/etsy-chore-chart/images/{name}"
    img.save(path, dpi=(DPI, DPI), quality=95)
    print(f"Saved: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 1 — HERO
# ══════════════════════════════════════════════════════════════════════════════
def create_image_1():
    img, draw = new_image()

    y = draw_title_section(draw,
        "Ultimate Kids Chore Chart System",
        "Build Responsibility. Track Progress. Reward Success.",
        y_start=80
    )

    # Main chore grid preview (center, large)
    grid_w, grid_h = 900, 450
    grid_x = W // 2 - grid_w // 2 - 20
    grid_y = y + 30
    draw_chore_grid_mini(draw, grid_x, grid_y, grid_w, grid_h, "Daily Chores")

    # Progress section (right side)
    px = grid_x + grid_w + 40
    py = grid_y + 20

    draw_rounded_rect(draw, (px, py, px + 520, py + 200), fill=C["white"], radius=14,
                      outline=C["border"], width=2)
    font_sm_b = get_font(20, bold=True)
    font_sm = get_font(18, bold=False)
    draw.text((px+20, py+15), "WEEKLY PROGRESS", fill=C["primary_dark"], font=font_sm_b)
    draw_progress_bar_mini(draw, px+20, py+55, 480, 32, 0.72, C["primary"])
    draw.text((px+20, py+100), "Points: 54 / 75", fill=C["dark_text"], font=font_sm)
    draw.text((px+20, py+130), "Completion: 72%", fill=C["dark_text"], font=font_sm)
    draw.text((px+20, py+160), "Status: Keep Going!", fill=C["secondary"], font=font_sm_b)

    # Reward tracker (right side below)
    ry = py + 220
    draw_rounded_rect(draw, (px, ry, px + 520, ry + 180), fill=C["white"], radius=14,
                      outline=C["border"], width=2)
    draw.text((px+20, ry+15), "REWARD TRACKER", fill=C["primary_dark"], font=font_sm_b)
    draw_progress_bar_mini(draw, px+20, ry+55, 480, 32, 0.85, C["success"])
    draw.text((px+20, ry+100), "Goal: 75 Points", fill=C["dark_text"], font=font_sm)
    draw.text((px+20, ry+130), "Reward: Almost There!", fill=C["success"], font=font_sm_b)

    # Left side mini
    lx = MARGIN + 30
    ly = grid_y + 20
    draw_rounded_rect(draw, (lx, ly, lx + 340, ly + 200), fill=C["white"], radius=14,
                      outline=C["border"], width=2)
    draw.text((lx+20, ly+15), "WEEKLY SUMMARY", fill=C["primary_dark"], font=font_sm_b)
    days_short = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    bar_font = get_font(14, bold=False)
    for i, d in enumerate(days_short):
        bar_y = ly + 50 + i * 28
        draw.text((lx+20, bar_y+2), d, fill=C["dark_text"], font=bar_font)
        pct = [0.9, 0.7, 0.8, 0.6, 0.9][i]
        bar_w = int(200 * pct)
        draw_rounded_rect(draw, (lx+70, bar_y, lx+70+bar_w, bar_y+20), fill=C["primary"], radius=10)

    # Bottom benefit lines
    benefits_y = H - MARGIN - 280
    benefits = [
        ("Visual progress tracking", C["primary"]),
        ("Customizable rewards", C["secondary"]),
        ("Simple for parents", C["success"]),
    ]
    bx = MARGIN + 200
    for i, (text, color) in enumerate(benefits):
        x = bx + i * 700
        draw_rounded_rect(draw, (x, benefits_y, x+580, benefits_y+65), fill=C["white"],
                          radius=12, outline=C["border"], width=2)
        draw.ellipse((x+15, benefits_y+18, x+45, benefits_y+48), fill=color)
        font = get_font(26, bold=False)
        draw.text((x+60, benefits_y+17), text, fill=C["dark_text"], font=font)

    draw_bottom_strip(draw, ["Instant Download", "Fully Editable", "Excel Compatible"])

    save_image(img, "01_hero.png")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 2 — HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════════
def create_image_2():
    img, draw = new_image()

    y = draw_title_section(draw, "How It Works", y_start=100)

    steps = [
        ("Assign Chores", "Customize the chore list\nfor your child's age\nand responsibilities.", C["primary"]),
        ("Track Completion", "Mark chores done each day\nwith a simple checkmark.\nProgress auto-calculates.", C["secondary"]),
        ("Earn Rewards", "Points add up toward\na reward goal you set.\nCelebrate success!", C["success"]),
    ]

    step_w = 650
    gap = 60
    total = step_w * 3 + gap * 2
    sx = (W - total) // 2
    card_y = y + 60

    for i, (title, desc, color) in enumerate(steps):
        cx = sx + i * (step_w + gap)

        # Card
        draw_rounded_rect(draw, (cx, card_y, cx + step_w, card_y + 680),
                          fill=C["white"], radius=20, outline=C["border"], width=2)

        # Step number circle
        circle_cx = cx + step_w // 2
        draw_step_circle(draw, circle_cx, card_y + 70, i + 1, size=90)

        # Title
        font_title = get_font(36, bold=True)
        bbox = draw.textbbox((0, 0), title, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text((circle_cx - tw // 2, card_y + 140), title, fill=C["primary_dark"], font=font_title)

        # Accent line
        draw.line([(cx + 60, card_y + 195), (cx + step_w - 60, card_y + 195)], fill=color, width=4)

        # Description
        font_desc = get_font(26, bold=False)
        for j, line in enumerate(desc.split('\n')):
            bbox = draw.textbbox((0, 0), line, font=font_desc)
            tw = bbox[2] - bbox[0]
            draw.text((circle_cx - tw // 2, card_y + 220 + j * 40), line, fill=C["dark_text"], font=font_desc)

        # Mini visual per step
        if i == 0:
            # Mini chore list
            mini_y = card_y + 360
            chores_mini = ["Make Bed", "Brush Teeth", "Pick Up Toys", "Set Table", "Feed Pet"]
            sm = get_font(20, bold=False)
            for k, ch in enumerate(chores_mini):
                chy = mini_y + k * 40
                draw_rounded_rect(draw, (cx+60, chy, cx+step_w-60, chy+34),
                                  fill=C["primary_light"] if k%2 else C["white"],
                                  radius=6, outline=C["border"], width=1)
                draw.text((cx+80, chy+6), ch, fill=C["dark_text"], font=sm)
        elif i == 1:
            # Mini check grid
            mini_y = card_y + 360
            sm = get_font(18, bold=True)
            days_header = ["M", "T", "W", "T", "F", "S", "S"]
            for k, dh in enumerate(days_header):
                dx = cx + 100 + k * 68
                draw.text((dx, mini_y), dh, fill=C["primary_dark"], font=sm)
            checks = [
                [1,1,1,1,1,0,1],
                [1,0,1,1,1,1,0],
                [1,1,1,0,1,1,1],
                [0,1,1,1,1,0,1],
            ]
            ck = get_font(22, bold=True)
            for row_i, row in enumerate(checks):
                for col_i, val in enumerate(row):
                    bx_pos = cx + 95 + col_i * 68
                    by = mini_y + 30 + row_i * 38
                    draw_rounded_rect(draw, (bx_pos, by, bx_pos+36, by+30),
                                      fill=C["success_light"] if val else C["incomplete"],
                                      radius=6)
                    if val:
                        draw.text((bx_pos+6, by+2), "✓", fill=C["success"], font=ck)
        else:
            # Mini reward meter
            mini_y = card_y + 380
            draw_progress_bar_mini(draw, cx+80, mini_y, step_w-160, 40, 0.85, C["success"])
            font_r = get_font(28, bold=True)
            text_r = "85% — Almost There!"
            bbox = draw.textbbox((0, 0), text_r, font=font_r)
            tw = bbox[2] - bbox[0]
            draw.text((circle_cx - tw//2, mini_y + 60), text_r, fill=C["success"], font=font_r)

        # Arrow between cards
        if i < 2:
            arrow_x = cx + step_w + gap // 2
            arrow_y = card_y + 340
            # Arrow body
            draw.polygon([
                (arrow_x - 25, arrow_y - 15),
                (arrow_x + 15, arrow_y),
                (arrow_x - 25, arrow_y + 15),
            ], fill=C["primary"])

    draw_bottom_strip(draw, ["Simple Setup", "Auto Tracking", "Instant Results"])

    save_image(img, "02_how_it_works.png")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 3 — PROGRESS TRACKING
# ══════════════════════════════════════════════════════════════════════════════
def create_image_3():
    img, draw = new_image()

    y = draw_title_section(draw, "Visual Progress Made Simple", y_start=80)

    # Main progress panel
    panel_x, panel_y = MARGIN + 60, y + 40
    panel_w, panel_h = W - MARGIN * 2 - 120, 520

    draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                      fill=C["white"], radius=20, outline=C["border"], width=2)

    # Header bar
    draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + 60),
                      fill=C["primary_dark"], radius=20)
    draw_rounded_rect(draw, (panel_x, panel_y + 40, panel_x + panel_w, panel_y + 60),
                      fill=C["primary_dark"], radius=0)
    font_hdr = get_font(26, bold=True)
    draw.text((panel_x + 30, panel_y + 15), "WEEKLY PROGRESS SUMMARY", fill=C["white"], font=font_hdr)

    # Completion percentage (large)
    pct_x = panel_x + 80
    pct_y = panel_y + 100
    font_big = get_font(120, bold=True)
    draw.text((pct_x, pct_y), "72%", fill=C["primary"], font=font_big)
    font_label = get_font(28, bold=False)
    draw.text((pct_x + 10, pct_y + 140), "Weekly Completion Rate", fill=C["gray_text"], font=font_label)

    # Progress bar
    bar_y = pct_y + 200
    draw.text((pct_x, bar_y - 35), "Overall Progress", fill=C["dark_text"], font=get_font(22, bold=True))
    draw_progress_bar_mini(draw, pct_x, bar_y, 600, 45, 0.72, C["primary"])

    # Points progress bar
    bar_y2 = bar_y + 75
    draw.text((pct_x, bar_y2 - 35), "Reward Progress", fill=C["dark_text"], font=get_font(22, bold=True))
    draw_progress_bar_mini(draw, pct_x, bar_y2, 600, 45, 0.85, C["success"])

    # Right side — daily bars
    bar_section_x = panel_x + panel_w // 2 + 80
    bar_section_y = panel_y + 90
    font_day = get_font(22, bold=False)
    font_day_b = get_font(22, bold=True)
    days_data = [
        ("Monday", 0.9), ("Tuesday", 0.7), ("Wednesday", 0.8),
        ("Thursday", 0.6), ("Friday", 0.9), ("Saturday", 0.5), ("Sunday", 0.7)
    ]
    for i, (day, pct) in enumerate(days_data):
        dy = bar_section_y + i * 56
        draw.text((bar_section_x, dy + 4), day, fill=C["dark_text"], font=font_day)
        bar_x = bar_section_x + 160
        bar_w = 500
        fill_w = int(bar_w * pct)
        draw_rounded_rect(draw, (bar_x, dy, bar_x + bar_w, dy + 32), fill=C["incomplete"], radius=16)
        color = C["success"] if pct >= 0.8 else C["secondary"] if pct >= 0.5 else C["danger"]
        draw_rounded_rect(draw, (bar_x, dy, bar_x + fill_w, dy + 32), fill=color, radius=16)
        pct_text = f"{int(pct*100)}%"
        draw.text((bar_x + bar_w + 15, dy + 4), pct_text, fill=C["dark_text"], font=font_day_b)

    # Callout boxes
    callouts = [
        ("See progress instantly", C["primary"]),
        ("Motivate consistency", C["secondary"]),
        ("Clear weekly goals", C["success"]),
    ]
    cw = 650
    cgap = 60
    ctotal = cw * 3 + cgap * 2
    csx = (W - ctotal) // 2
    cy = panel_y + panel_h + 60

    for i, (text, color) in enumerate(callouts):
        cx = csx + i * (cw + cgap)
        draw_callout_box(draw, cx, cy, cw, 70, text, color)

    draw_bottom_strip(draw, ["Auto-Calculated", "Visual Feedback", "Weekly Review"])

    save_image(img, "03_progress_tracking.png")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 4 — REWARD SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
def create_image_4():
    img, draw = new_image()

    y = draw_title_section(draw, "Motivating Reward System", y_start=80)

    # Main reward panel
    panel_x, panel_y = MARGIN + 60, y + 40
    panel_w = W - MARGIN * 2 - 120
    panel_h = 500

    draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                      fill=C["white"], radius=20, outline=C["border"], width=2)

    # Header
    draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + 60),
                      fill=C["secondary"], radius=20)
    draw_rounded_rect(draw, (panel_x, panel_y + 40, panel_x + panel_w, panel_y + 60),
                      fill=C["secondary"], radius=0)
    font_hdr = get_font(26, bold=True)
    draw.text((panel_x + 30, panel_y + 15), "REWARD TRACKER", fill=C["white"], font=font_hdr)

    # Points section
    py = panel_y + 85
    font_lg = get_font(80, bold=True)
    font_md = get_font(28, bold=False)
    font_md_b = get_font(28, bold=True)

    # Points earned
    col1_x = panel_x + 80
    draw.text((col1_x, py), "54", fill=C["primary"], font=font_lg)
    draw.text((col1_x, py + 90), "Points Earned", fill=C["gray_text"], font=font_md)

    # Divider
    draw.text((col1_x + 200, py + 20), "/", fill=C["border"], font=get_font(60, bold=False))

    # Points goal
    col2_x = col1_x + 280
    draw.text((col2_x, py), "75", fill=C["secondary"], font=font_lg)
    draw.text((col2_x, py + 90), "Points Goal", fill=C["gray_text"], font=font_md)

    # Reward threshold indicator
    thresh_x = col2_x + 300
    draw_rounded_rect(draw, (thresh_x, py, thresh_x + 450, py + 120),
                      fill=C["secondary_light"], radius=16, outline=C["secondary"], width=2)
    draw.text((thresh_x + 30, py + 15), "Reward Threshold", fill=C["dark_text"], font=font_md_b)
    draw.text((thresh_x + 30, py + 55), "Reach 75 points to earn", fill=C["dark_text"], font=font_md)
    draw.text((thresh_x + 30, py + 85), "your weekly reward!", fill=C["secondary"], font=font_md_b)

    # Large progress bar
    bar_y = py + 155
    draw.text((col1_x, bar_y), "Progress: 72%", fill=C["dark_text"], font=font_md_b)
    draw_progress_bar_mini(draw, col1_x, bar_y + 45, panel_w - 200, 50, 0.72, C["secondary"])

    # Reward earned indicator
    indicator_y = bar_y + 120
    draw_rounded_rect(draw, (col1_x, indicator_y, col1_x + panel_w - 200, indicator_y + 60),
                      fill=C["success_light"], radius=12, outline=C["success"], width=3)
    font_earned = get_font(28, bold=True)
    text_e = "Keep Going! — 21 more points to REWARD EARNED!"
    bbox = draw.textbbox((0, 0), text_e, font=font_earned)
    tw = bbox[2] - bbox[0]
    mid = col1_x + (panel_w - 200) // 2
    draw.text((mid - tw//2, indicator_y + 15), text_e, fill=C["success"], font=font_earned)

    # Callouts
    callouts = [
        ("Customizable reward goals", C["secondary"]),
        ("Automatic tracking", C["primary"]),
        ("Positive reinforcement", C["success"]),
    ]
    cw = 650
    cgap = 60
    ctotal = cw * 3 + cgap * 2
    csx = (W - ctotal) // 2
    cy = panel_y + panel_h + 60

    for i, (text, color) in enumerate(callouts):
        cx = csx + i * (cw + cgap)
        draw_callout_box(draw, cx, cy, cw, 70, text, color)

    draw_bottom_strip(draw, ["Set Your Own Goals", "Points System", "Celebrate Success"])

    save_image(img, "04_reward_system.png")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 5 — PARENT CONTROL VIEW
# ══════════════════════════════════════════════════════════════════════════════
def create_image_5():
    img, draw = new_image()

    y = draw_title_section(draw, "Designed for Parents", y_start=80)

    # Three panels side by side
    card_w = 680
    card_h = 550
    gap = 50
    total = card_w * 3 + gap * 2
    sx = (W - total) // 2
    cy = y + 50

    panels = [
        {
            "title": "Editable Chore List",
            "color": C["primary"],
            "items": [
                ("Chore names", "Customize for any age"),
                ("Points values", "Set daily & weekly points"),
                ("Reward goal", "Choose your target"),
                ("Child's name", "Personalize the chart"),
                ("Week dates", "Track by week"),
            ]
        },
        {
            "title": "Protected Formulas",
            "color": C["secondary"],
            "items": [
                ("Auto-counting", "Completions tallied"),
                ("Progress %", "Calculated live"),
                ("Point totals", "Always accurate"),
                ("Reward status", "Auto-triggers"),
                ("Weekly summary", "Links to chart"),
            ]
        },
        {
            "title": "Clear Input Zones",
            "color": C["success"],
            "items": [
                ("Yellow cells", "= Editable input"),
                ("White cells", "= Auto-calculated"),
                ("Frozen headers", "Always visible"),
                ("Drop-downs", "Easy checkmarks"),
                ("Notes area", "Add reward details"),
            ]
        },
    ]

    for i, panel in enumerate(panels):
        px = sx + i * (card_w + gap)
        draw_rounded_rect(draw, (px, cy, px + card_w, cy + card_h),
                          fill=C["white"], radius=20, outline=C["border"], width=2)

        # Title bar
        draw_rounded_rect(draw, (px, cy, px + card_w, cy + 65), fill=panel["color"], radius=20)
        draw_rounded_rect(draw, (px, cy + 45, px + card_w, cy + 65), fill=panel["color"], radius=0)
        font_t = get_font(26, bold=True)
        bbox = draw.textbbox((0, 0), panel["title"], font=font_t)
        tw = bbox[2] - bbox[0]
        draw.text((px + (card_w - tw)//2, cy + 18), panel["title"], fill=C["white"], font=font_t)

        # Items
        font_item = get_font(22, bold=True)
        font_desc = get_font(20, bold=False)
        for j, (item, desc) in enumerate(panel["items"]):
            iy = cy + 90 + j * 88
            # Icon bar
            draw_rounded_rect(draw, (px + 25, iy, px + card_w - 25, iy + 75),
                              fill=C["badge_bg"], radius=10)
            draw.ellipse((px + 40, iy + 15, px + 62, iy + 37), fill=panel["color"])
            draw.text((px + 75, iy + 10), item, fill=C["dark_text"], font=font_item)
            draw.text((px + 75, iy + 40), desc, fill=C["gray_text"], font=font_desc)

    # Callouts
    callouts = [
        ("Easy customization", C["primary"]),
        ("No complex setup", C["secondary"]),
        ("Fully automated", C["success"]),
    ]
    cw = 650
    cgap = 60
    ctotal = cw * 3 + cgap * 2
    csx = (W - ctotal) // 2
    ccy = cy + card_h + 50

    for i, (text, color) in enumerate(callouts):
        cx = csx + i * (cw + cgap)
        draw_callout_box(draw, cx, ccy, cw, 70, text, color)

    draw_bottom_strip(draw, ["Parent-Friendly", "No Learning Curve", "Works Immediately"])

    save_image(img, "05_parent_controls.png")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 6 — EVERYTHING INCLUDED
# ══════════════════════════════════════════════════════════════════════════════
def create_image_6():
    img, draw = new_image()

    y = draw_title_section(draw, "Everything Included", y_start=80)

    # 4 sheet previews in a 2x2 grid
    card_w = 950
    card_h = 420
    gap_x = 60
    gap_y = 50
    total_w = card_w * 2 + gap_x
    sx = (W - total_w) // 2
    sy = y + 40

    sheets = [
        {
            "title": "Main Chore Sheet",
            "color": C["primary"],
            "lines": [
                "- 10 customizable daily chores",
                "- 5 customizable weekly chores",
                "- Daily check-mark tracking (Mon-Sun)",
                "- Auto-calculated completion counts",
                "- Point system (1pt daily, 2pt weekly)",
                "- Progress bar & reward status",
                "- Notes section for reward details",
            ]
        },
        {
            "title": "Weekly Summary",
            "color": C["secondary"],
            "lines": [
                "- Day-by-day completion breakdown",
                "- Auto-calculated daily percentages",
                "- Status indicators (Great/Good/Needs Work)",
                "- Visual bar chart for daily performance",
                "- Overall weekly completion rate",
                "- Points earned vs goal tracking",
                "- Reward progress percentage",
            ]
        },
        {
            "title": "Reward Tracker",
            "color": C["success"],
            "lines": [
                "- Current week reward status",
                "- Points earned vs goal display",
                "- Visual progress bar",
                "- 8-week reward bank history",
                "- Cumulative stats tracking",
                "- Total rewards earned counter",
                "- Average completion rate",
            ]
        },
        {
            "title": "Instructions Guide",
            "color": C["gray_text"],
            "lines": [
                "- Step-by-step setup guide",
                "- How to track daily chores",
                "- How to track weekly chores",
                "- Understanding the summary",
                "- Tips for success",
                "- Editable vs locked cells guide",
                "- Troubleshooting help",
            ]
        }
    ]

    positions = [
        (sx, sy),
        (sx + card_w + gap_x, sy),
        (sx, sy + card_h + gap_y),
        (sx + card_w + gap_x, sy + card_h + gap_y),
    ]

    for (px, py), sheet in zip(positions, sheets):
        draw_rounded_rect(draw, (px, py, px + card_w, py + card_h),
                          fill=C["white"], radius=16, outline=C["border"], width=2)

        # Tab header
        draw_rounded_rect(draw, (px, py, px + card_w, py + 55), fill=sheet["color"], radius=16)
        draw_rounded_rect(draw, (px, py + 38, px + card_w, py + 55), fill=sheet["color"], radius=0)
        font_t = get_font(24, bold=True)
        bbox = draw.textbbox((0, 0), sheet["title"], font=font_t)
        tw = bbox[2] - bbox[0]
        draw.text((px + (card_w - tw)//2, py + 14), sheet["title"], fill=C["white"], font=font_t)

        # Content lines
        font_line = get_font(20, bold=False)
        for j, line in enumerate(sheet["lines"]):
            ly = py + 70 + j * 44
            # Bullet
            draw.ellipse((px + 30, ly + 8, px + 44, ly + 22), fill=sheet["color"])
            draw.text((px + 55, ly), line.lstrip("- "), fill=C["dark_text"], font=font_line)

    draw_bottom_strip(draw, ["Fully Editable", "Instant Download", "Excel Compatible"],
                      y=H - MARGIN - 55)

    save_image(img, "06_everything_included.png")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 7 — OUTCOME
# ══════════════════════════════════════════════════════════════════════════════
def create_image_7():
    img, draw = new_image()

    y = draw_title_section(draw,
        "Raise Responsible Kids",
        y_start=80
    )

    # Dashboard overview panel
    dash_x = MARGIN + 80
    dash_y = y + 40
    dash_w = W - MARGIN * 2 - 160
    dash_h = 480

    draw_rounded_rect(draw, (dash_x, dash_y, dash_x + dash_w, dash_y + dash_h),
                      fill=C["white"], radius=20, outline=C["border"], width=2)

    # Header
    draw_rounded_rect(draw, (dash_x, dash_y, dash_x + dash_w, dash_y + 60),
                      fill=C["primary_dark"], radius=20)
    draw_rounded_rect(draw, (dash_x, dash_y + 40, dash_x + dash_w, dash_y + 60),
                      fill=C["primary_dark"], radius=0)
    font_hdr = get_font(26, bold=True)
    draw.text((dash_x + 30, dash_y + 15), "CHORE CHART DASHBOARD", fill=C["white"], font=font_hdr)

    # Left side: Summary stats
    stat_x = dash_x + 50
    stat_y = dash_y + 90

    stats = [
        ("This Week", "72%", C["primary"]),
        ("Points", "54 / 75", C["secondary"]),
        ("Streak", "3 weeks", C["success"]),
        ("Rewards", "2 earned", C["success"]),
    ]

    for i, (label, value, color) in enumerate(stats):
        sy_pos = stat_y + i * 90
        draw_rounded_rect(draw, (stat_x, sy_pos, stat_x + 350, sy_pos + 75),
                          fill=C["badge_bg"], radius=12, outline=C["border"], width=1)
        font_label = get_font(20, bold=False)
        font_val = get_font(32, bold=True)
        draw.text((stat_x + 20, sy_pos + 8), label, fill=C["gray_text"], font=font_label)
        draw.text((stat_x + 20, sy_pos + 36), value, fill=color, font=font_val)

    # Right side: Mini chart
    chart_x = dash_x + 500
    chart_y = dash_y + 85
    chart_w = dash_w - 560
    chart_h = 180

    draw_rounded_rect(draw, (chart_x, chart_y, chart_x + chart_w, chart_y + chart_h),
                      fill=C["badge_bg"], radius=12, outline=C["border"], width=1)
    draw.text((chart_x + 20, chart_y + 10), "Daily Completion", fill=C["dark_text"], font=get_font(20, bold=True))

    # Bar chart
    days_vals = [("M", 0.9), ("T", 0.7), ("W", 0.8), ("T", 0.6), ("F", 0.9), ("S", 0.5), ("S", 0.7)]
    bar_base = chart_y + chart_h - 25
    bar_area_h = 100
    bar_spacing = chart_w // 8
    font_sm = get_font(14, bold=True)
    for i, (day, pct) in enumerate(days_vals):
        bx = chart_x + 40 + i * bar_spacing
        bh = int(bar_area_h * pct)
        color = C["success"] if pct >= 0.8 else C["secondary"] if pct >= 0.5 else C["danger"]
        draw_rounded_rect(draw, (bx, bar_base - bh, bx + 40, bar_base), fill=color, radius=6)
        draw.text((bx + 12, bar_base + 3), day, fill=C["dark_text"], font=font_sm)

    # Reward section
    reward_y = chart_y + chart_h + 30
    draw_rounded_rect(draw, (chart_x, reward_y, chart_x + chart_w, reward_y + 140),
                      fill=C["success_light"], radius=12, outline=C["success"], width=2)
    draw.text((chart_x + 20, reward_y + 10), "Reward Progress", fill=C["dark_text"], font=get_font(20, bold=True))
    draw_progress_bar_mini(draw, chart_x + 20, reward_y + 45, chart_w - 40, 35, 0.72, C["success"])
    draw.text((chart_x + 20, reward_y + 95), "21 points to go — Keep it up!", fill=C["success"], font=get_font(20, bold=True))

    # Outcome statements
    outcomes = [
        ("Build consistency", C["primary"]),
        ("Encourage independence", C["secondary"]),
        ("Make chores motivating", C["success"]),
    ]

    ow = 650
    ogap = 60
    ototal = ow * 3 + ogap * 2
    osx = (W - ototal) // 2
    oy = dash_y + dash_h + 60

    for i, (text, color) in enumerate(outcomes):
        ox = osx + i * (ow + ogap)
        draw_rounded_rect(draw, (ox, oy, ox + ow, oy + 80), fill=C["white"],
                          radius=14, outline=color, width=3)
        font_o = get_font(28, bold=True)
        bbox = draw.textbbox((0, 0), text, font=font_o)
        tw = bbox[2] - bbox[0]
        draw.text((ox + (ow - tw)//2, oy + 23), text, fill=color, font=font_o)

    draw_bottom_strip(draw, ["Structured System", "Proven Results", "Happy Families"])

    save_image(img, "07_outcome.png")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Creating all 7 Etsy listing images...")
    create_image_1()
    create_image_2()
    create_image_3()
    create_image_4()
    create_image_5()
    create_image_6()
    create_image_7()
    print("All images created successfully!")
