#!/usr/bin/env python3
"""Generate 5 Etsy listing images for Teacher Classroom Planner 2026."""

from PIL import Image, ImageDraw, ImageFont
import math, os

# ─── Constants ───────────────────────────────────────────────────────────────
W, H = 2700, 2025
APPLE_RED   = (197, 48, 48)
SUNSHINE    = (214, 158, 46)
SKY_BLUE    = (49, 130, 206)
CHALK_GREEN = (56, 161, 105)
PALE_PEACH  = (255, 245, 245)
DARK        = (45, 55, 72)
WHITE       = (255, 255, 255)
LIGHT_GRAY  = (237, 242, 247)
MID_GRAY    = (160, 174, 192)
FAINT_LINE  = (226, 232, 240)

OUT_DIR = "/home/user/claude-code/etsy-digital-download-7/images"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

os.makedirs(OUT_DIR, exist_ok=True)

def font(size, bold=False, mono=False):
    p = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REG)
    return ImageFont.truetype(p, size)

# ─── Gradient helpers ────────────────────────────────────────────────────────
def warm_gradient(img, c1=(255, 240, 230), c2=(255, 220, 200), c3=(255, 235, 225)):
    """Three-stop vertical warm gradient."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        t = y / h
        if t < 0.5:
            tt = t / 0.5
            r = int(c1[0] + (c2[0] - c1[0]) * tt)
            g = int(c1[1] + (c2[1] - c1[1]) * tt)
            b = int(c1[2] + (c2[2] - c1[2]) * tt)
        else:
            tt = (t - 0.5) / 0.5
            r = int(c2[0] + (c3[0] - c2[0]) * tt)
            g = int(c2[1] + (c3[1] - c2[1]) * tt)
            b = int(c2[2] + (c3[2] - c2[2]) * tt)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def peachy_gradient(img):
    warm_gradient(img, (255, 248, 240), (255, 230, 215), (255, 240, 230))

def soft_blue_gradient(img):
    warm_gradient(img, (235, 245, 255), (220, 235, 255), (240, 248, 255))

def soft_green_gradient(img):
    warm_gradient(img, (240, 255, 245), (225, 250, 235), (240, 255, 248))

# ─── iPad mockup (rounded rect + screen) ────────────────────────────────────
def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_ipad(img, x, y, w, h, screen_callback, shadow=True, bezel=18):
    """Draw an iPad frame at (x,y) size (w,h) and call screen_callback to fill content."""
    draw = ImageDraw.Draw(img)
    # shadow
    if shadow:
        for i in range(20, 0, -1):
            alpha_rect = (x + 6 + i, y + 6 + i, x + w + 6 + i, y + h + 6 + i)
            c = 200 + int(55 * (i / 20))
            draw_rounded_rect(draw, alpha_rect, 24, fill=(c, c, c))
    # body
    draw_rounded_rect(draw, (x, y, x + w, y + h), 24, fill=(50, 50, 52), outline=(35, 35, 37), width=2)
    # screen area
    sx, sy = x + bezel, y + bezel
    sw, sh = w - 2 * bezel, h - 2 * bezel
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE)
    # home indicator
    bar_w = int(w * 0.25)
    bar_h = 5
    bx = x + (w - bar_w) // 2
    by = y + h - bezel // 2 - bar_h // 2
    draw_rounded_rect(draw, (bx, by, bx + bar_w, by + bar_h), 3, fill=(120, 120, 122))
    # camera dot
    cam_r = 4
    cx = x + w // 2
    cy = y + bezel // 2
    draw.ellipse([cx - cam_r, cy - cam_r, cx + cam_r, cy + cam_r], fill=(70, 70, 72))
    screen_callback(draw, sx, sy, sw, sh)

# ─── Reusable small-table renderers ─────────────────────────────────────────
def draw_tab_header(draw, sx, sy, sw, title, color, fsize=22):
    draw.rectangle([sx, sy, sx + sw, sy + 38], fill=color)
    draw.text((sx + 10, sy + 6), title, fill=WHITE, font=font(fsize, bold=True))

def draw_spreadsheet_grid(draw, sx, sy, sw, sh, headers, rows, header_color, fsize=16, row_h=28, header_h=32):
    col_w = sw // len(headers)
    # header row
    draw.rectangle([sx, sy, sx + sw, sy + header_h], fill=header_color)
    for i, hdr in enumerate(headers):
        draw.text((sx + i * col_w + 6, sy + 5), hdr, fill=WHITE, font=font(fsize, bold=True))
    # data rows
    for ri, row in enumerate(rows):
        ry = sy + header_h + ri * row_h
        bg = WHITE if ri % 2 == 0 else (248, 250, 252)
        draw.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
        draw.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=FAINT_LINE)
        for ci, val in enumerate(row):
            draw.text((sx + ci * col_w + 6, ry + 4), str(val), fill=DARK, font=font(fsize - 1))

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 1 — Hero
# ─────────────────────────────────────────────────────────────────────────────
def make_image1():
    img = Image.new("RGB", (W, H))
    peachy_gradient(img)
    draw = ImageDraw.Draw(img)

    # decorative dots
    for dx in range(0, W, 120):
        for dy in range(0, H, 120):
            draw.ellipse([dx, dy, dx + 4, dy + 4], fill=(255, 225, 210, 60))

    # Title text upper-left
    draw.text((100, 80), "TEACHER", fill=APPLE_RED, font=font(72, bold=True))
    draw.text((100, 160), "CLASSROOM", fill=DARK, font=font(72, bold=True))
    draw.text((100, 240), "PLANNER", fill=DARK, font=font(72, bold=True))

    # 2026 badge
    badge_x, badge_y = 100, 340
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + 200, badge_y + 60), 30, fill=APPLE_RED)
    draw.text((badge_x + 42, badge_y + 10), "2026", fill=WHITE, font=font(34, bold=True))

    # Subtitle
    draw.text((100, 430), "8 READY-TO-USE SPREADSHEET TABS", fill=DARK, font=font(28, bold=True))
    draw.text((100, 470), "Class Roster  |  Lesson Planner  |  Grade Tracker", fill=MID_GRAY, font=font(22))
    draw.text((100, 500), "Attendance  |  Budget  |  Parent Comm  |  IEP/504", fill=MID_GRAY, font=font(22))

    # iPad showing Grade Tracker ─ main hero
    ipad_x, ipad_y, ipad_w, ipad_h = 950, 120, 1600, 1200
    students_grades = [
        ("Emma S.", "93", "87", "62", "79", "91", "80", "B"),
        ("Liam J.", "76", "94", "75", "97", "62", "81", "B"),
        ("Noah B.", "88", "72", "95", "83", "79", "83", "B"),
        ("Olivia W.", "95", "91", "88", "92", "97", "92", "A"),
        ("Ava D.", "67", "78", "82", "59", "97", "77", "C"),
        ("Sophia M.", "91", "85", "94", "88", "76", "87", "B"),
        ("Mason T.", "72", "68", "81", "74", "89", "77", "C"),
        ("Isabella R.", "98", "92", "96", "90", "95", "94", "A"),
        ("James L.", "84", "79", "71", "88", "82", "81", "B"),
        ("Charlotte P.", "90", "87", "93", "85", "91", "89", "B"),
    ]

    def screen_grade(d, sx, sy, sw, sh):
        # Tab header bar
        draw_tab_header(d, sx, sy, sw, "GRADE TRACKER  |  Teacher Classroom Planner 2026", APPLE_RED, fsize=24)
        # sub-header
        d.rectangle([sx, sy + 38, sx + sw, sy + 68], fill=(254, 240, 240))
        d.text((sx + 10, sy + 42), "Track 20 assignments per student with automatic averages", fill=APPLE_RED, font=font(17))
        # column headers
        headers = ["Student Name", "Asgn 1", "Asgn 2", "Asgn 3", "Asgn 4", "Asgn 5", "Avg", "Grade"]
        col_ws = [int(sw * f) for f in [0.22, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.12]]
        hdr_y = sy + 72
        cx = sx
        for i, hdr in enumerate(headers):
            d.rectangle([cx, hdr_y, cx + col_ws[i], hdr_y + 36], fill=DARK)
            d.text((cx + 6, hdr_y + 7), hdr, fill=WHITE, font=font(17, bold=True))
            cx += col_ws[i]
        # data
        row_h = int((sh - 120) / (len(students_grades) + 0.5))
        row_h = min(row_h, 80)
        for ri, row in enumerate(students_grades):
            ry = hdr_y + 36 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (248, 250, 252)
            d.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            d.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=FAINT_LINE)
            cx = sx
            for ci, val in enumerate(row):
                color = DARK
                if ci == len(row) - 1:  # letter grade
                    if val == "A":
                        color = CHALK_GREEN
                    elif val == "B":
                        color = SKY_BLUE
                    else:
                        color = SUNSHINE
                    d.text((cx + 10, ry + (row_h - 22) // 2), val, fill=color, font=font(20, bold=True))
                else:
                    d.text((cx + 6, ry + (row_h - 18) // 2), val, fill=color, font=font(18))
                cx += col_ws[ci]

    draw_ipad(img, ipad_x, ipad_y, ipad_w, ipad_h, screen_grade)

    # Annotations with arrows/lines
    # Annotation 1 - "Auto-calculated averages"
    ax, ay = 950, 1400
    draw_rounded_rect(draw, (ax, ay, ax + 380, ay + 50), 25, fill=SKY_BLUE)
    draw.text((ax + 18, ay + 10), "Auto-calculated averages", fill=WHITE, font=font(22, bold=True))
    draw.line([(ax + 190, ay), (ipad_x + ipad_w - 350, ipad_y + ipad_h - 160)], fill=SKY_BLUE, width=3)

    # Annotation 2 - "Letter grades A-F"
    ax2, ay2 = 1450, 1400
    draw_rounded_rect(draw, (ax2, ay2, ax2 + 310, ay2 + 50), 25, fill=CHALK_GREEN)
    draw.text((ax2 + 18, ay2 + 10), "Letter grades A-F", fill=WHITE, font=font(22, bold=True))
    draw.line([(ax2 + 155, ay2), (ipad_x + ipad_w - 120, ipad_y + ipad_h - 200)], fill=CHALK_GREEN, width=3)

    # Annotation 3 - "Track 30+ students"
    ax3, ay3 = 1880, 1400
    draw_rounded_rect(draw, (ax3, ay3, ax3 + 310, ay3 + 50), 25, fill=SUNSHINE)
    draw.text((ax3 + 18, ay3 + 10), "Track 30+ students", fill=WHITE, font=font(22, bold=True))

    # Bottom feature badges
    features = [
        ("8 Tabs", APPLE_RED),
        ("40 Students", SKY_BLUE),
        ("Instant Download", CHALK_GREEN),
        ("Excel + Sheets", SUNSHINE),
    ]
    bx = 100
    for label, color in features:
        tw = len(label) * 16 + 40
        draw_rounded_rect(draw, (bx, 1780, bx + tw, 1830), 25, fill=color)
        draw.text((bx + 20, 1790), label, fill=WHITE, font=font(20, bold=True))
        bx += tw + 30

    # "Works on iPad, laptop, tablet" bottom text
    draw.text((100, 1860), "Works on iPad  |  Laptop  |  Any Device with Excel or Google Sheets", fill=MID_GRAY, font=font(22))

    # Decorative corner elements
    for i in range(5):
        r = 200 - i * 35
        draw.ellipse([W - 200 - r, H - 200 - r, W - 200 + r, H - 200 + r], outline=(255, 220, 200), width=2)

    img.save(os.path.join(OUT_DIR, "01_hero_main_listing.png"), "PNG")
    print("  [OK] 01_hero_main_listing.png")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 2 — All 7 tabs mini iPads
# ─────────────────────────────────────────────────────────────────────────────
def make_image2():
    img = Image.new("RGB", (W, H))
    soft_blue_gradient(img)
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((W // 2 - 400, 50), "ALL 8 TABS INCLUDED", fill=DARK, font=font(54, bold=True))
    draw.text((W // 2 - 360, 120), "Everything you need to manage your classroom", fill=MID_GRAY, font=font(26))

    tabs = [
        ("Class Roster", APPLE_RED, ["Student Name", "Grade", "Parent"], [("Emma Smith", "3rd", "Mr. Smith"), ("Liam Johnson", "4th", "Mrs. J"), ("Noah Brown", "3rd", "Mr. Brown")]),
        ("Lesson Planner", SKY_BLUE, ["Week", "Subject", "Topic"], [("Wk 1", "Math", "Place Value"), ("Wk 2", "ELA", "Narrative"), ("Wk 3", "Science", "Plants")]),
        ("Grade Tracker", CHALK_GREEN, ["Student", "Avg", "Grade"], [("Emma S.", "80", "B"), ("Liam J.", "81", "B"), ("Olivia W.", "92", "A")]),
        ("Attendance", SUNSHINE, ["Student", "D1", "D2", "D3"], [("Emma S.", "P", "P", "A"), ("Liam J.", "P", "T", "P"), ("Noah B.", "P", "P", "P")]),
        ("Budget", APPLE_RED, ["Item", "Qty", "Cost"], [("Markers", "3", "$8.99"), ("Paper", "2", "$12.49"), ("Folders", "30", "$0.89")]),
        ("Parent Comm", SKY_BLUE, ["Date", "Student", "Method"], [("10/24", "Emma S.", "Email"), ("08/14", "Liam J.", "Conf"), ("09/03", "Noah B.", "Phone")]),
        ("IEP/504", CHALK_GREEN, ["Student", "Plan", "Status"], [("Emma S.", "IEP", "On track"), ("Noah B.", "IEP", "Support"), ("Sophia M.", "504", "On track")]),
    ]

    # Layout: row 1 = 4 iPads, row 2 = 3 iPads + "How to Use" card
    ipad_w, ipad_h = 540, 420
    gap = 50
    row1_count = 4
    row2_count = 4
    row1_x_start = (W - row1_count * ipad_w - (row1_count - 1) * gap) // 2
    row2_x_start = (W - row2_count * ipad_w - (row2_count - 1) * gap) // 2
    row1_y = 220
    row2_y = 720

    positions = []
    for i in range(4):
        positions.append((row1_x_start + i * (ipad_w + gap), row1_y))
    for i in range(3):
        positions.append((row2_x_start + i * (ipad_w + gap), row2_y))

    for idx, (tab_name, color, headers, rows) in enumerate(tabs):
        px, py = positions[idx]

        def make_screen(d, sx, sy, sw, sh, _tn=tab_name, _c=color, _h=headers, _r=rows):
            draw_tab_header(d, sx, sy, sw, _tn, _c, fsize=16)
            col_w = sw // len(_h)
            hy = sy + 38
            d.rectangle([sx, hy, sx + sw, hy + 24], fill=DARK)
            for i, hdr in enumerate(_h):
                d.text((sx + i * col_w + 4, hy + 3), hdr, fill=WHITE, font=font(12, bold=True))
            for ri, row in enumerate(_r):
                ry = hy + 24 + ri * 24
                bg = WHITE if ri % 2 == 0 else (248, 250, 252)
                d.rectangle([sx, ry, sx + sw, ry + 24], fill=bg)
                for ci, val in enumerate(row):
                    fc = DARK
                    if val in ("P",):
                        fc = CHALK_GREEN
                    elif val in ("A",):
                        fc = APPLE_RED
                    elif val in ("T",):
                        fc = SUNSHINE
                    d.text((sx + ci * col_w + 4, ry + 3), val, fill=fc, font=font(12))

        draw_ipad(img, px, py, ipad_w, ipad_h, make_screen, bezel=12)

        # Label beneath
        lx = px + ipad_w // 2
        draw.text((lx - len(tab_name) * 5, py + ipad_h + 30), tab_name, fill=DARK, font=font(18, bold=True), anchor=None)

    # "How to Use" card (position 8 - bottom row last)
    hx, hy = row2_x_start + 3 * (ipad_w + gap), row2_y
    def how_screen(d, sx, sy, sw, sh):
        draw_tab_header(d, sx, sy, sw, "How to Use", SUNSHINE, fsize=16)
        steps = [
            "1. Download the .xlsx file",
            "2. Open in Excel or Sheets",
            "3. Customize your tabs",
            "4. Start planning!",
        ]
        for i, step in enumerate(steps):
            d.text((sx + 10, sy + 48 + i * 30), step, fill=DARK, font=font(14))
        d.text((sx + 10, sy + sh - 50), "Works on any device!", fill=CHALK_GREEN, font=font(14, bold=True))

    draw_ipad(img, hx, hy, ipad_w, ipad_h, how_screen, bezel=12)
    draw.text((hx + ipad_w // 2 - 50, hy + ipad_h + 30), "How to Use", fill=DARK, font=font(18, bold=True))

    # Bottom bar
    draw_rounded_rect(draw, (200, 1250, W - 200, 1310), 30, fill=DARK)
    draw.text((W // 2 - 320, 1263), "Instant Download  |  Excel & Google Sheets  |  2026 School Year", fill=WHITE, font=font(22, bold=True))

    # Decorative circles
    for i in range(6):
        cx = 60 + i * 80
        draw.ellipse([cx, 1400, cx + 20, 1420], fill=([APPLE_RED, SKY_BLUE, CHALK_GREEN, SUNSHINE, APPLE_RED, SKY_BLUE][i]))

    img.save(os.path.join(OUT_DIR, "02_all_tabs_overview.png"), "PNG")
    print("  [OK] 02_all_tabs_overview.png")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 3 — Grade Tracker + Attendance (two iPads)
# ─────────────────────────────────────────────────────────────────────────────
def make_image3():
    img = Image.new("RGB", (W, H))
    soft_green_gradient(img)
    draw = ImageDraw.Draw(img)

    draw.text((W // 2 - 350, 60), "TRACK GRADES & ATTENDANCE", fill=DARK, font=font(52, bold=True))
    draw.text((W // 2 - 280, 130), "Keep accurate records for every student", fill=MID_GRAY, font=font(26))

    # Grade Tracker iPad (left)
    students_grades = [
        ("Emma Smith", "93", "87", "62", "79", "91", "80.4", "B"),
        ("Liam Johnson", "76", "94", "75", "97", "62", "80.8", "B"),
        ("Noah Brown", "88", "72", "95", "83", "79", "83.4", "B"),
        ("Olivia Williams", "95", "91", "88", "92", "97", "92.6", "A"),
        ("Ava Davis", "67", "78", "82", "59", "97", "76.6", "C"),
        ("Sophia Martinez", "91", "85", "94", "88", "76", "86.8", "B"),
        ("Mason Taylor", "72", "68", "81", "74", "89", "76.8", "C"),
        ("Isabella Rodriguez", "98", "92", "96", "90", "95", "94.2", "A"),
        ("James Lee", "84", "79", "71", "88", "82", "80.8", "B"),
        ("Charlotte Park", "90", "87", "93", "85", "91", "89.2", "B"),
        ("Ethan Kim", "77", "83", "69", "92", "85", "81.2", "B"),
        ("Amelia Chen", "95", "98", "91", "94", "97", "95.0", "A"),
    ]

    def grade_screen(d, sx, sy, sw, sh):
        draw_tab_header(d, sx, sy, sw, "GRADE TRACKER", CHALK_GREEN, fsize=22)
        headers = ["Student", "A1", "A2", "A3", "A4", "A5", "Avg", "Grd"]
        col_ws = [int(sw * f) for f in [0.24, 0.10, 0.10, 0.10, 0.10, 0.10, 0.13, 0.13]]
        hy = sy + 42
        cx = sx
        for i, hdr in enumerate(headers):
            d.rectangle([cx, hy, cx + col_ws[i], hy + 30], fill=DARK)
            d.text((cx + 4, hy + 5), hdr, fill=WHITE, font=font(15, bold=True))
            cx += col_ws[i]
        row_h = min(48, (sh - 80) // len(students_grades))
        for ri, row in enumerate(students_grades):
            ry = hy + 30 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (245, 250, 245)
            d.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            d.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=FAINT_LINE)
            cx = sx
            for ci, val in enumerate(row):
                fc = DARK
                if ci == 7:
                    fc = CHALK_GREEN if val == "A" else (SKY_BLUE if val == "B" else SUNSHINE)
                    d.text((cx + 8, ry + (row_h - 16) // 2), val, fill=fc, font=font(16, bold=True))
                else:
                    d.text((cx + 4, ry + (row_h - 14) // 2), val, fill=fc, font=font(14))
                cx += col_ws[ci]

    draw_ipad(img, 100, 220, 1200, 1050, grade_screen, bezel=16)
    draw.text((350, 1310), "Grade Tracker", fill=CHALK_GREEN, font=font(32, bold=True))
    draw.text((350, 1355), "20 assignments per student", fill=MID_GRAY, font=font(20))
    draw.text((350, 1385), "Auto-calculated averages & letter grades", fill=MID_GRAY, font=font(20))

    # Attendance iPad (right)
    students_att = [
        ("Emma Smith",     ["P","P","P","P","P","A","P","P","P","P","P","A","P","P","P"]),
        ("Liam Johnson",   ["P","P","P","T","P","P","E","P","P","T","P","P","P","P","P"]),
        ("Noah Brown",     ["P","P","A","P","P","P","P","P","P","P","A","P","P","P","P"]),
        ("Olivia Williams",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
        ("Ava Davis",      ["P","T","P","P","A","P","P","P","P","P","P","T","P","P","P"]),
        ("Sophia Martinez",["P","P","P","P","P","P","P","P","A","P","P","P","P","P","P"]),
        ("Mason Taylor",   ["P","P","P","P","P","P","T","P","P","P","P","P","P","A","P"]),
        ("Isabella R.",    ["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
        ("James Lee",      ["P","P","P","A","P","P","P","P","P","P","P","P","T","P","P"]),
        ("Charlotte Park", ["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
        ("Ethan Kim",      ["T","P","P","P","P","P","P","A","P","P","P","P","P","P","P"]),
        ("Amelia Chen",    ["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
    ]

    def att_screen(d, sx, sy, sw, sh):
        draw_tab_header(d, sx, sy, sw, "ATTENDANCE TRACKER", SKY_BLUE, fsize=22)
        # day headers
        name_w = int(sw * 0.22)
        day_w = (sw - name_w) // 15
        hy = sy + 42
        d.rectangle([sx, hy, sx + name_w, hy + 30], fill=DARK)
        d.text((sx + 4, hy + 5), "Student", fill=WHITE, font=font(14, bold=True))
        for di in range(15):
            dx = sx + name_w + di * day_w
            d.rectangle([dx, hy, dx + day_w, hy + 30], fill=DARK)
            d.text((dx + 2, hy + 5), f"D{di+1}", fill=WHITE, font=font(11, bold=True))

        row_h = min(48, (sh - 80) // len(students_att))
        for ri, (name, days) in enumerate(students_att):
            ry = hy + 30 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (245, 248, 255)
            d.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            d.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=FAINT_LINE)
            d.text((sx + 4, ry + (row_h - 14) // 2), name, fill=DARK, font=font(13))
            for di, val in enumerate(days):
                dx = sx + name_w + di * day_w
                fc = CHALK_GREEN if val == "P" else (APPLE_RED if val == "A" else (SUNSHINE if val == "T" else SKY_BLUE))
                d.text((dx + day_w // 2 - 4, ry + (row_h - 14) // 2), val, fill=fc, font=font(14, bold=True))

    draw_ipad(img, 1400, 220, 1200, 1050, att_screen, bezel=16)
    draw.text((1650, 1310), "Attendance Tracker", fill=SKY_BLUE, font=font(32, bold=True))
    draw.text((1650, 1355), "P = Present  |  A = Absent  |  T = Tardy", fill=MID_GRAY, font=font(20))
    draw.text((1650, 1385), "Monthly tracking with attendance %", fill=MID_GRAY, font=font(20))

    # Legend bar
    legend_y = 1500
    draw_rounded_rect(draw, (200, legend_y, W - 200, legend_y + 70), 35, fill=DARK)
    items = [
        ("P = Present", CHALK_GREEN),
        ("A = Absent", APPLE_RED),
        ("T = Tardy", SUNSHINE),
        ("E = Excused", SKY_BLUE),
        ("Auto Attendance %", WHITE),
    ]
    lx = 300
    for label, color in items:
        d = draw
        d.ellipse([lx, legend_y + 25, lx + 18, legend_y + 43], fill=color)
        d.text((lx + 26, legend_y + 22), label, fill=WHITE, font=font(20, bold=True))
        lx += len(label) * 14 + 70

    # Bottom text
    draw.text((W // 2 - 250, 1650), "30+ students  |  Full school year tracking", fill=MID_GRAY, font=font(22))

    img.save(os.path.join(OUT_DIR, "03_grades_attendance.png"), "PNG")
    print("  [OK] 03_grades_attendance.png")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 4 — Lesson Planner + Parent Communication Log
# ─────────────────────────────────────────────────────────────────────────────
def make_image4():
    img = Image.new("RGB", (W, H))
    warm_gradient(img, (255, 248, 240), (255, 235, 220), (255, 245, 235))
    draw = ImageDraw.Draw(img)

    draw.text((W // 2 - 400, 60), "PLAN LESSONS & TRACK COMMUNICATION", fill=DARK, font=font(46, bold=True))
    draw.text((W // 2 - 320, 125), "40 weeks of lesson planning + parent contact log", fill=MID_GRAY, font=font(24))

    # Lesson Planner iPad (left)
    lessons = [
        ("Wk 1", "08/17-08/21", "Math", "Place Value", "Guided practice"),
        ("Wk 2", "08/24-08/28", "ELA", "Narrative Writing", "Group work"),
        ("Wk 3", "08/31-09/04", "Science", "Plant Life Cycles", "Lab experiment"),
        ("Wk 4", "09/07-09/11", "Math", "Addition Fluency", "Timed drills"),
        ("Wk 5", "09/14-09/18", "ELA", "Reading Comp", "Guided reading"),
        ("Wk 6", "09/21-09/25", "Science", "Weather Patterns", "Observation log"),
        ("Wk 7", "09/28-10/02", "Math", "Subtraction", "Worksheets"),
        ("Wk 8", "10/05-10/09", "Social St.", "Community", "Field trip"),
        ("Wk 9", "10/12-10/16", "ELA", "Poetry", "Creative writing"),
        ("Wk 10", "10/19-10/23", "Math", "Multiplication", "Flash cards"),
        ("Wk 11", "10/26-10/30", "Science", "Simple Machines", "Build project"),
    ]

    def lesson_screen(d, sx, sy, sw, sh):
        draw_tab_header(d, sx, sy, sw, "LESSON PLANNER  |  40 Weeks", SUNSHINE, fsize=20)
        headers = ["Week", "Dates", "Subject", "Topic", "Activities"]
        col_ws = [int(sw * f) for f in [0.10, 0.20, 0.15, 0.27, 0.28]]
        hy = sy + 42
        cx = sx
        for i, hdr in enumerate(headers):
            d.rectangle([cx, hy, cx + col_ws[i], hy + 28], fill=DARK)
            d.text((cx + 4, hy + 4), hdr, fill=WHITE, font=font(14, bold=True))
            cx += col_ws[i]
        row_h = min(46, (sh - 80) // len(lessons))
        for ri, row in enumerate(lessons):
            ry = hy + 28 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (255, 252, 245)
            d.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            d.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=FAINT_LINE)
            cx = sx
            for ci, val in enumerate(row):
                fc = DARK
                if ci == 2:  # subject
                    fc = SKY_BLUE
                d.text((cx + 4, ry + (row_h - 14) // 2), val, fill=fc, font=font(13))
                cx += col_ws[ci]

    draw_ipad(img, 100, 210, 1200, 1050, lesson_screen, bezel=16)
    draw.text((350, 1300), "Lesson Planner", fill=SUNSHINE, font=font(32, bold=True))
    draw.text((350, 1345), "40 weeks  |  Standards-aligned  |  Full year coverage", fill=MID_GRAY, font=font(20))

    # Parent Communication Log iPad (right)
    comms = [
        ("10/24", "Emma S.", "Mr. Smith", "Email", "Attendance", "Resolved"),
        ("08/14", "Liam J.", "Mrs. Johnson", "Conference", "Academic", "Follow-up"),
        ("09/03", "Noah B.", "Mr. Brown", "Phone", "Behavior", "Resolved"),
        ("09/15", "Olivia W.", "Mrs. Williams", "Email", "IEP Update", "Resolved"),
        ("10/01", "Ava D.", "Mr. Davis", "Conference", "Grades", "Follow-up"),
        ("10/10", "Sophia M.", "Mrs. Martinez", "Phone", "Homework", "Resolved"),
        ("10/18", "Mason T.", "Mr. Taylor", "Email", "Behavior", "Pending"),
        ("11/02", "Isabella R.", "Mrs. Rodriguez", "Conference", "Progress", "Resolved"),
        ("11/08", "James L.", "Mr. Lee", "Phone", "Attendance", "Resolved"),
        ("11/15", "Charlotte P.", "Mrs. Park", "Email", "Academic", "Follow-up"),
        ("11/22", "Ethan K.", "Mr. Kim", "Conference", "IEP", "Resolved"),
    ]

    def comm_screen(d, sx, sy, sw, sh):
        draw_tab_header(d, sx, sy, sw, "PARENT COMMUNICATION LOG", APPLE_RED, fsize=20)
        headers = ["Date", "Student", "Parent", "Method", "Topic", "Status"]
        col_ws = [int(sw * f) for f in [0.10, 0.14, 0.18, 0.16, 0.20, 0.22]]
        hy = sy + 42
        cx = sx
        for i, hdr in enumerate(headers):
            d.rectangle([cx, hy, cx + col_ws[i], hy + 28], fill=DARK)
            d.text((cx + 4, hy + 4), hdr, fill=WHITE, font=font(14, bold=True))
            cx += col_ws[i]
        row_h = min(46, (sh - 80) // len(comms))
        for ri, row in enumerate(comms):
            ry = hy + 28 + ri * row_h
            bg = WHITE if ri % 2 == 0 else (255, 248, 248)
            d.rectangle([sx, ry, sx + sw, ry + row_h], fill=bg)
            d.line([(sx, ry + row_h), (sx + sw, ry + row_h)], fill=FAINT_LINE)
            cx = sx
            for ci, val in enumerate(row):
                fc = DARK
                if ci == 5:  # status
                    if val == "Resolved":
                        fc = CHALK_GREEN
                    elif val == "Follow-up":
                        fc = SUNSHINE
                    else:
                        fc = APPLE_RED
                d.text((cx + 4, ry + (row_h - 14) // 2), val, fill=fc, font=font(13))
                cx += col_ws[ci]

    draw_ipad(img, 1400, 210, 1200, 1050, comm_screen, bezel=16)
    draw.text((1650, 1300), "Parent Communication Log", fill=APPLE_RED, font=font(32, bold=True))
    draw.text((1650, 1345), "Track every email, call, and conference", fill=MID_GRAY, font=font(20))

    # Bottom bar
    boty = 1500
    draw_rounded_rect(draw, (200, boty, W - 200, boty + 70), 35, fill=DARK)
    draw.text((W // 2 - 380, boty + 18), "Stay Organized  |  Document Everything  |  Never Miss a Follow-up", fill=WHITE, font=font(22, bold=True))

    img.save(os.path.join(OUT_DIR, "04_lessons_communication.png"), "PNG")
    print("  [OK] 04_lessons_communication.png")

# ─────────────────────────────────────────────────────────────────────────────
# IMAGE 5 — Value proposition, $9.99 INSTANT DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
def make_image5():
    img = Image.new("RGB", (W, H))
    peachy_gradient(img)
    draw = ImageDraw.Draw(img)

    # Big price badge centered top
    cx, cy = W // 2, 280
    # Outer circle
    draw.ellipse([cx - 200, cy - 200, cx + 200, cy + 200], fill=APPLE_RED, outline=DARK, width=4)
    # Inner ring
    draw.ellipse([cx - 180, cy - 180, cx + 180, cy + 180], outline=WHITE, width=3)
    draw.text((cx - 110, cy - 80), "$9.99", fill=WHITE, font=font(72, bold=True))
    draw.text((cx - 70, cy + 10), "ONLY", fill=(255, 200, 200), font=font(28, bold=True))

    # "INSTANT DOWNLOAD" banner
    bw, bh = 700, 70
    bx = W // 2 - bw // 2
    by = 530
    draw_rounded_rect(draw, (bx, by, bx + bw, by + bh), 35, fill=DARK)
    draw.text((bx + 90, by + 15), "INSTANT DOWNLOAD", fill=WHITE, font=font(36, bold=True))

    # Main title
    draw.text((W // 2 - 500, 650), "TEACHER CLASSROOM PLANNER 2026", fill=DARK, font=font(46, bold=True))

    # What's included section
    yi = 750
    draw.text((W // 2 - 200, yi), "WHAT'S INCLUDED:", fill=APPLE_RED, font=font(30, bold=True))
    yi += 60

    included = [
        ("Class Roster", "Track 40+ students with contact info", APPLE_RED),
        ("Lesson Planner", "40 weeks of standards-aligned planning", SKY_BLUE),
        ("Grade Tracker", "20 assignments with auto averages", CHALK_GREEN),
        ("Attendance Tracker", "Monthly P/A/T/E with attendance %", SUNSHINE),
        ("Classroom Budget", "Track expenses & reimbursements", APPLE_RED),
        ("Parent Communication", "Log every call, email & conference", SKY_BLUE),
        ("IEP/504 Tracker", "Confidential accommodation tracking", CHALK_GREEN),
        ("How to Use Guide", "Step-by-step setup instructions", SUNSHINE),
    ]

    # Two columns
    col1_x, col2_x = 250, 1400
    for i, (name, desc, color) in enumerate(included):
        x = col1_x if i < 4 else col2_x
        y = yi + (i % 4) * 85
        # Checkbox
        draw_rounded_rect(draw, (x, y, x + 36, y + 36), 6, fill=color)
        draw.text((x + 8, y + 4), "✓", fill=WHITE, font=font(22, bold=True))
        draw.text((x + 50, y + 2), name, fill=DARK, font=font(22, bold=True))
        draw.text((x + 50, y + 30), desc, fill=MID_GRAY, font=font(17))

    # Compatibility section
    comp_y = 1200
    draw.line([(300, comp_y), (W - 300, comp_y)], fill=FAINT_LINE, width=2)
    comp_y += 30

    draw.text((W // 2 - 140, comp_y), "WORKS WITH:", fill=DARK, font=font(26, bold=True))
    comp_y += 55

    apps = [
        ("Microsoft Excel", SKY_BLUE),
        ("Google Sheets", CHALK_GREEN),
        ("iPad / Tablet", SUNSHINE),
        ("Mac / PC", APPLE_RED),
    ]
    ax = (W - len(apps) * 350) // 2
    for label, color in apps:
        draw_rounded_rect(draw, (ax, comp_y, ax + 300, comp_y + 55), 28, fill=color)
        draw.text((ax + 30, comp_y + 12), label, fill=WHITE, font=font(24, bold=True))
        ax += 350

    # Bottom CTA
    cta_y = 1450
    draw_rounded_rect(draw, (W // 2 - 500, cta_y, W // 2 + 500, cta_y + 80), 40, fill=APPLE_RED)
    draw.text((W // 2 - 300, cta_y + 16), "ADD TO CART — INSTANT DOWNLOAD", fill=WHITE, font=font(34, bold=True))

    # Fine print
    draw.text((W // 2 - 320, cta_y + 110), "Download immediately after purchase  |  No shipping required", fill=MID_GRAY, font=font(20))
    draw.text((W // 2 - 280, cta_y + 145), "Print-ready  |  Fully editable  |  Lifetime access", fill=MID_GRAY, font=font(20))

    # Trust badges
    trust_y = cta_y + 200
    badges = [
        "Instant Access",
        "Editable Template",
        "30+ Students",
        "Full School Year",
    ]
    bx = 350
    for badge in badges:
        tw = len(badge) * 14 + 40
        draw_rounded_rect(draw, (bx, trust_y, bx + tw, trust_y + 45), 22, fill=WHITE, outline=DARK, width=2)
        draw.text((bx + 20, trust_y + 10), badge, fill=DARK, font=font(18, bold=True))
        bx += tw + 40

    # Star rating
    draw.text((W // 2 - 80, trust_y + 70), "★ ★ ★ ★ ★", fill=SUNSHINE, font=font(30, bold=True))
    draw.text((W // 2 - 100, trust_y + 110), "Loved by teachers!", fill=MID_GRAY, font=font(20))

    img.save(os.path.join(OUT_DIR, "05_value_proposition.png"), "PNG")
    print("  [OK] 05_value_proposition.png")


# ─── Run all ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Teacher Classroom Planner 2026 images...")
    make_image1()
    make_image2()
    make_image3()
    make_image4()
    make_image5()
    print("\nAll 5 images generated successfully!")
