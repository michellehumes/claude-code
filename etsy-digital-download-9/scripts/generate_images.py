#!/usr/bin/env python3
"""Generate all 5 Etsy listing images for Student Academic Planner 2026."""

from PIL import Image, ImageDraw, ImageFont
import math, os

# ── Dimensions ──────────────────────────────────────────────
W, H = 2700, 2025

# ── Palette ─────────────────────────────────────────────────
INDIGO      = (76, 81, 191)
VIOLET      = (128, 90, 213)
TEAL        = (49, 151, 149)
CORAL       = (245, 101, 101)
SUNSHINE    = (236, 201, 75)
PALE_INDIGO = (232, 227, 243)
DARK        = (26, 32, 44)
WHITE       = (255, 255, 255)
LIGHT_GRAY  = (243, 244, 246)
MID_GRAY    = (160, 170, 185)
NEAR_WHITE  = (248, 248, 252)

# ── Fonts ───────────────────────────────────────────────────
def font(size, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, size)

OUTDIR = "/home/user/claude-code/etsy-digital-download-9/images"
os.makedirs(OUTDIR, exist_ok=True)

# ── Helpers ─────────────────────────────────────────────────
def gradient_bg(draw, w, h, c1, c2, vertical=True):
    """Draw a linear gradient."""
    for i in range(h if vertical else w):
        ratio = i / (h if vertical else w)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        if vertical:
            draw.line([(0, i), (w, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, h)], fill=(r, g, b))

def rounded_rect(draw, xy, fill, radius=20, outline=None, width=0):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_ipad(img, x, y, w, h, screen_callback, shadow=True, bezel_color=(30, 30, 35)):
    """Draw an iPad frame at (x,y) with width w height h, then call screen_callback to fill screen content."""
    draw = ImageDraw.Draw(img)
    bezel = max(12, int(w * 0.028))
    corner = max(18, int(w * 0.04))

    # Shadow
    if shadow:
        for s in range(20, 0, -2):
            alpha_rect = (x + s + 3, y + s + 3, x + w + s + 3, y + h + s + 3)
            c = 200 - s * 8
            c = max(0, min(255, c))
            draw.rounded_rectangle(alpha_rect, radius=corner + s, fill=(c, c, c))

    # Outer body
    draw.rounded_rectangle((x, y, x + w, y + h), radius=corner, fill=bezel_color)
    # Screen area
    sx, sy = x + bezel, y + bezel
    sw, sh = w - 2 * bezel, h - 2 * bezel
    screen_corner = max(8, corner - 6)
    draw.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=screen_corner, fill=WHITE)

    # Camera dot
    cam_r = max(3, int(w * 0.008))
    draw.ellipse((x + w // 2 - cam_r, y + 4, x + w // 2 + cam_r, y + 4 + cam_r * 2), fill=(50, 50, 55))

    # Call back to draw screen contents
    screen_callback(img, sx, sy, sw, sh)

def draw_status_badge(draw, x, y, text, color, f):
    tw = draw.textlength(text, font=f)
    pad = 12
    rounded_rect(draw, (x, y, x + tw + pad * 2, y + 28), fill=color, radius=14)
    draw.text((x + pad, y + 3), text, fill=WHITE, font=f)
    return tw + pad * 2

def draw_annotation(draw, x1, y1, x2, y2, text, f, color=CORAL, bg=WHITE):
    """Draw an annotation with a line from (x1,y1) to (x2,y2) and text at (x2,y2)."""
    draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    # Circle at start
    r = 6
    draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=color)
    tw = draw.textlength(text, font=f)
    pad = 14
    # bg pill
    rx, ry = x2, y2 - 18
    draw.rounded_rectangle((rx - 4, ry - 4, rx + tw + pad, ry + 32), radius=16, fill=bg, outline=color, width=2)
    draw.text((rx + pad // 2, ry + 2), text, fill=DARK, font=f)

def draw_dotted_pattern(draw, w, h, spacing=60, color=(255, 255, 255, 30)):
    """Draw subtle dot pattern."""
    for dx in range(0, w, spacing):
        for dy in range(0, h, spacing):
            draw.ellipse((dx - 1, dy - 1, dx + 1, dy + 1), fill=color)


# ════════════════════════════════════════════════════════════
# IMAGE 1: HERO — Assignment Tracker on iPad
# ════════════════════════════════════════════════════════════
def make_image_01():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Background gradient — deep indigo to violet
    gradient_bg(draw, W, H, (55, 48, 163), (90, 60, 180))

    # Subtle decorative circles
    for cx, cy, r, alpha in [(200, 300, 250, 40), (2500, 200, 300, 35), (400, 1800, 200, 30), (2300, 1700, 280, 35)]:
        c = min(255, INDIGO[0] + alpha)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(c, c // 2 + 80, 210))

    # Geometric accent lines
    for yy in range(0, H, 150):
        draw.line([(0, yy), (W, yy)], fill=(255, 255, 255, 12), width=1)

    # Title text (left side)
    title_x = 100
    draw.text((title_x, 100), "STUDENT", fill=WHITE, font=font(82, True))
    draw.text((title_x, 195), "ACADEMIC", fill=WHITE, font=font(82, True))
    draw.text((title_x, 290), "PLANNER", fill=WHITE, font=font(82, True))

    # Year badge
    draw.rounded_rectangle((title_x, 400, title_x + 200, 456), radius=28, fill=SUNSHINE)
    draw.text((title_x + 30, 408), "2 0 2 6", fill=DARK, font=font(30, True))

    # Subtitle
    draw.text((title_x, 490), "Track Classes  |  Assignments  |  Grades", fill=(210, 210, 240), font=font(26))
    draw.text((title_x, 530), "Study Plans  |  Expenses  |  Goals", fill=(210, 210, 240), font=font(26))

    # Feature pills
    features = [("8 Smart Tabs", TEAL), ("Auto GPA Calc", VIOLET), ("Assignment Alerts", CORAL)]
    fy = 600
    for txt, col in features:
        f_small = font(22, True)
        tw = draw.textlength(txt, font=f_small)
        draw.rounded_rectangle((title_x, fy, title_x + tw + 30, fy + 40), radius=20, fill=col)
        draw.text((title_x + 15, fy + 7), txt, fill=WHITE, font=f_small)
        fy += 55

    # iPad — Assignment Tracker screen
    ipad_x, ipad_y = 1050, 80
    ipad_w, ipad_h = 1500, 1800

    def assignment_screen(img, sx, sy, sw, sh):
        d = ImageDraw.Draw(img)
        # Header bar
        d.rectangle((sx, sy, sx + sw, sy + 70), fill=INDIGO)
        d.text((sx + 20, sy + 18), "ASSIGNMENT TRACKER", fill=WHITE, font=font(28, True))
        d.text((sx + sw - 200, sy + 22), "Fall 2026", fill=(200, 200, 240), font=font(22))

        # Column headers
        col_y = sy + 85
        d.rectangle((sx, col_y, sx + sw, col_y + 42), fill=PALE_INDIGO)
        cols = ["Class", "Assignment", "Type", "Due Date", "Status", "Priority"]
        col_xs = [sx + 15, sx + 140, sx + 380, sx + 510, sx + 660, sx + 790]
        for label, cx in zip(cols, col_xs):
            d.text((cx, col_y + 10), label, fill=DARK, font=font(18, True))

        # Data rows
        rows = [
            ("PSY 101", "Chapter 3 Reading", "Homework", "Feb 8", "Graded", "Low", (76, 175, 80)),
            ("MATH 202", "Problem Set 4", "Homework", "Feb 10", "Graded", "Med", (76, 175, 80)),
            ("ENG 110", "Persuasive Essay", "Essay", "Feb 15", "In Progress", "High", CORAL),
            ("CS 150", "Lab 3: Loops", "Lab", "Feb 12", "In Progress", "High", CORAL),
            ("PSY 101", "Midterm Study Guide", "Study", "Feb 20", "Not Started", "Med", MID_GRAY),
            ("MATH 202", "Chapter 8 Problems", "Homework", "Feb 18", "In Progress", "Med", SUNSHINE),
            ("HIST 210", "Research Proposal", "Essay", "Feb 22", "Not Started", "High", MID_GRAY),
            ("CS 150", "Project 1 Proposal", "Project", "Feb 25", "Not Started", "Low", MID_GRAY),
            ("ENG 110", "Peer Review", "Review", "Feb 17", "Submitted", "Med", TEAL),
            ("HIST 210", "Map Quiz", "Quiz", "Feb 14", "Graded", "Low", (76, 175, 80)),
            ("MATH 202", "Quiz 3", "Quiz", "Feb 16", "Submitted", "Med", TEAL),
            ("PSY 101", "Lab Report 2", "Lab", "Feb 19", "In Progress", "High", CORAL),
            ("CS 150", "Reading: Ch 5", "Homework", "Feb 13", "Graded", "Low", (76, 175, 80)),
            ("ENG 110", "Grammar Exercise", "Homework", "Feb 11", "Graded", "Low", (76, 175, 80)),
            ("HIST 210", "Chapter 6 Notes", "Homework", "Feb 21", "Not Started", "Med", MID_GRAY),
            ("MATH 202", "Extra Credit Set", "Homework", "Feb 28", "Not Started", "Low", MID_GRAY),
            ("PSY 101", "Group Presentation", "Project", "Mar 1", "Not Started", "High", MID_GRAY),
            ("CS 150", "Midterm Review", "Study", "Feb 26", "Not Started", "Med", MID_GRAY),
        ]

        row_h = 44
        ry = col_y + 42
        fn = font(16)
        fn_b = font(15, True)
        for i, (cls, asgn, atype, due, status, prio, scolor) in enumerate(rows):
            if ry + row_h > sy + sh - 5:
                break
            bg = WHITE if i % 2 == 0 else NEAR_WHITE
            d.rectangle((sx, ry, sx + sw, ry + row_h), fill=bg)
            d.text((col_xs[0], ry + 12), cls, fill=INDIGO, font=fn_b)
            d.text((col_xs[1], ry + 12), asgn[:18], fill=DARK, font=fn)
            d.text((col_xs[2], ry + 12), atype, fill=MID_GRAY, font=fn)
            d.text((col_xs[3], ry + 12), due, fill=DARK, font=fn)
            # Status badge
            draw_status_badge(d, col_xs[4], ry + 8, status, scolor, font(13, True))
            # Priority
            pcol = CORAL if prio == "High" else (SUNSHINE if prio == "Med" else TEAL)
            d.text((col_xs[5], ry + 12), prio, fill=pcol, font=fn_b)
            ry += row_h

        # Bottom summary bar
        d.rectangle((sx, sy + sh - 50, sx + sw, sy + sh), fill=(245, 245, 250))
        d.text((sx + 20, sy + sh - 40), "18 Assignments", fill=DARK, font=font(18, True))
        d.text((sx + 240, sy + sh - 40), "5 Graded", fill=(76, 175, 80), font=font(17))
        d.text((sx + 410, sy + sh - 40), "4 In Progress", fill=CORAL, font=font(17))
        d.text((sx + 620, sy + sh - 40), "2 Submitted", fill=TEAL, font=font(17))

    draw_ipad(img, ipad_x, ipad_y, ipad_w, ipad_h, assignment_screen)

    # Annotations pointing to iPad features
    ann_f = font(20, True)
    draw_annotation(draw, ipad_x + 200, ipad_y + 200, ipad_x - 350, ipad_y + 150, "Color-coded Status", ann_f, CORAL)
    draw_annotation(draw, ipad_x + ipad_w - 150, ipad_y + 500, ipad_x + ipad_w + 80, ipad_y + 400, "Priority Levels", ann_f, TEAL)
    draw_annotation(draw, ipad_x + 400, ipad_y + ipad_h - 80, ipad_x - 200, ipad_y + ipad_h - 30, "Progress Summary", ann_f, VIOLET)

    # Bottom bar
    draw.rectangle((0, H - 80, W, H), fill=(30, 25, 60))
    draw.text((100, H - 60), "INSTANT DIGITAL DOWNLOAD  |  WORKS IN EXCEL, NUMBERS & GOOGLE SHEETS  |  FALL + SPRING", fill=(200, 200, 230), font=font(22))

    img.save(os.path.join(OUTDIR, "01_hero_main_listing.png"), quality=95)
    print("  [OK] 01_hero_main_listing.png")


# ════════════════════════════════════════════════════════════
# IMAGE 2: 7 Mini iPads — all tabs
# ════════════════════════════════════════════════════════════
def make_image_02():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (60, 50, 155), (100, 65, 190))

    # Title
    draw.text((W // 2 - 400, 50), "Everything You Need in 8 Smart Tabs", fill=WHITE, font=font(48, True))
    draw.text((W // 2 - 310, 115), "Your Complete Academic Command Center", fill=(210, 210, 240), font=font(28))

    tabs = [
        ("Semester Dashboard", INDIGO, "dashboard"),
        ("Class Schedule", TEAL, "schedule"),
        ("Assignment Tracker", CORAL, "assignments"),
        ("Grade Calculator", VIOLET, "grades"),
        ("Study Planner", SUNSHINE, "study"),
        ("Expense Tracker", (76, 175, 80), "expenses"),
        ("Semester Goals", INDIGO, "goals"),
    ]

    # Layout: row of 4 + row of 3
    iw, ih = 530, 540
    gap = 50

    # Row 1: 4 items
    row1_total = 4 * iw + 3 * gap
    row1_x = (W - row1_total) // 2
    row1_y = 200

    # Row 2: 3 items
    row2_total = 3 * iw + 2 * gap
    row2_x = (W - row2_total) // 2
    row2_y = 200 + ih + 80

    positions = []
    for i in range(4):
        positions.append((row1_x + i * (iw + gap), row1_y))
    for i in range(3):
        positions.append((row2_x + i * (iw + gap), row2_y))

    def make_mini_screen(tab_name, accent, kind):
        def callback(img, sx, sy, sw, sh):
            d = ImageDraw.Draw(img)
            # Header
            d.rectangle((sx, sy, sx + sw, sy + 50), fill=accent)
            d.text((sx + 12, sy + 12), tab_name, fill=WHITE, font=font(18, True))
            cy = sy + 60

            if kind == "dashboard":
                # GPA cards
                for label, val in [("Current GPA", "3.42"), ("Target GPA", "3.50"), ("Credits", "16")]:
                    d.rounded_rectangle((sx + 10, cy, sx + sw - 10, cy + 55), radius=8, fill=PALE_INDIGO)
                    d.text((sx + 20, cy + 5), label, fill=MID_GRAY, font=font(13))
                    d.text((sx + 20, cy + 25), val, fill=DARK, font=font(22, True))
                    cy += 65
                # Mini bar chart
                bars = [0.7, 0.85, 0.65, 0.9, 0.78]
                bw = (sw - 40) // len(bars) - 8
                bx = sx + 20
                for pct in bars:
                    bh_max = 80
                    bh = int(bh_max * pct)
                    d.rectangle((bx, cy + bh_max - bh, bx + bw, cy + bh_max), fill=INDIGO)
                    bx += bw + 8

            elif kind == "schedule":
                rows = [("PSY 101", "MWF 9:00", "Hall 204"), ("MATH 202", "TTh 10:30", "Sci 301"), ("ENG 110", "MWF 1:00", "Lib 105"), ("CS 150", "TTh 2:00", "Tech 210"), ("HIST 210", "MWF 3:00", "Main 108")]
                for cls, time, room in rows:
                    d.rounded_rectangle((sx + 8, cy, sx + sw - 8, cy + 42), radius=6, fill=NEAR_WHITE, outline=PALE_INDIGO, width=1)
                    d.text((sx + 15, cy + 4), cls, fill=INDIGO, font=font(14, True))
                    d.text((sx + 15, cy + 22), f"{time} - {room}", fill=MID_GRAY, font=font(11))
                    cy += 48

            elif kind == "assignments":
                items = [("Essay Draft", "Feb 15", CORAL), ("Lab 3", "Feb 12", CORAL), ("Problem Set", "Feb 18", SUNSHINE), ("Quiz", "Feb 14", (76, 175, 80)), ("Study Guide", "Feb 20", MID_GRAY)]
                for asgn, due, col in items:
                    d.rounded_rectangle((sx + 8, cy, sx + sw - 8, cy + 42), radius=6, fill=NEAR_WHITE)
                    d.ellipse((sx + 15, cy + 14, sx + 27, cy + 26), fill=col)
                    d.text((sx + 35, cy + 5), asgn, fill=DARK, font=font(14, True))
                    d.text((sx + 35, cy + 24), due, fill=MID_GRAY, font=font(11))
                    cy += 48

            elif kind == "grades":
                items = [("PSY 101", "A-", "89.3"), ("MATH 202", "B+", "86.1"), ("ENG 110", "A", "93.2"), ("CS 150", "B", "84.5"), ("HIST 210", "A-", "91.0")]
                for cls, grade, pct in items:
                    d.rounded_rectangle((sx + 8, cy, sx + sw - 8, cy + 42), radius=6, fill=NEAR_WHITE)
                    d.text((sx + 15, cy + 10), cls, fill=DARK, font=font(14, True))
                    gcol = (76, 175, 80) if grade.startswith("A") else SUNSHINE if grade.startswith("B") else CORAL
                    d.text((sx + sw - 80, cy + 4), grade, fill=gcol, font=font(20, True))
                    # small bar
                    bw_max = sw - 200
                    bw_act = int(bw_max * float(pct) / 100)
                    d.rounded_rectangle((sx + 120, cy + 28, sx + 120 + bw_max, cy + 36), radius=4, fill=LIGHT_GRAY)
                    d.rounded_rectangle((sx + 120, cy + 28, sx + 120 + bw_act, cy + 36), radius=4, fill=gcol)
                    cy += 48

            elif kind == "study":
                days = [("Mon", [("MATH", 1.5), ("PSY", 1.0)]), ("Tue", [("ENG", 2.0), ("CS", 1.5)]), ("Wed", [("HIST", 1.0), ("MATH", 2.0)])]
                for day, sessions in days:
                    d.text((sx + 12, cy), day, fill=INDIGO, font=font(15, True))
                    cy += 22
                    for subj, hrs in sessions:
                        bw = int((sw - 80) * hrs / 3.0)
                        d.rounded_rectangle((sx + 60, cy, sx + 60 + bw, cy + 22), radius=6, fill=TEAL)
                        d.text((sx + 65, cy + 2), f"{subj} ({hrs}h)", fill=WHITE, font=font(12, True))
                        cy += 28
                    cy += 10

            elif kind == "expenses":
                cats = [("Textbooks", 45.99, CORAL), ("Supplies", 12.50, SUNSHINE), ("Food", 150.0, TEAL), ("Transport", 30.0, VIOLET), ("Software", 9.99, INDIGO)]
                total = sum(v for _, v, _ in cats)
                for cat, amt, col in cats:
                    bw = int((sw - 120) * amt / total)
                    d.rounded_rectangle((sx + 8, cy, sx + sw - 8, cy + 38), radius=6, fill=NEAR_WHITE)
                    d.rounded_rectangle((sx + 10, cy + 26, sx + 10 + bw, cy + 36), radius=4, fill=col)
                    d.text((sx + 15, cy + 4), cat, fill=DARK, font=font(13, True))
                    d.text((sx + sw - 70, cy + 4), f"${amt:.0f}", fill=MID_GRAY, font=font(13))
                    cy += 46
                d.text((sx + 15, cy + 5), f"Total: ${total:.2f}", fill=DARK, font=font(16, True))

            elif kind == "goals":
                goals = [("3.5+ GPA", "Academic", 0.68, INDIGO), ("Internship", "Career", 0.30, VIOLET), ("Exercise 3x/wk", "Health", 0.75, TEAL), ("Read 10 books", "Personal", 0.40, CORAL)]
                for goal, cat, prog, col in goals:
                    d.text((sx + 12, cy), goal, fill=DARK, font=font(14, True))
                    d.text((sx + sw - 80, cy), cat, fill=MID_GRAY, font=font(11))
                    cy += 22
                    bw = sw - 30
                    d.rounded_rectangle((sx + 12, cy, sx + 12 + bw, cy + 16), radius=8, fill=LIGHT_GRAY)
                    d.rounded_rectangle((sx + 12, cy, sx + 12 + int(bw * prog), cy + 16), radius=8, fill=col)
                    d.text((sx + 12 + int(bw * prog) + 5, cy - 1), f"{int(prog * 100)}%", fill=col, font=font(12, True))
                    cy += 30
        return callback

    for idx, (name, accent, kind) in enumerate(tabs):
        px, py = positions[idx]
        draw_ipad(img, px, py, iw, ih, make_mini_screen(name, accent, kind), shadow=True)

    # Bottom label
    draw.rounded_rectangle((W // 2 - 280, H - 100, W // 2 + 280, H - 45), radius=28, fill=SUNSHINE)
    draw.text((W // 2 - 240, H - 92), "Works in Excel, Numbers & Google Sheets", fill=DARK, font=font(24, True))

    img.save(os.path.join(OUTDIR, "02_all_tabs_overview.png"), quality=95)
    print("  [OK] 02_all_tabs_overview.png")


# ════════════════════════════════════════════════════════════
# IMAGE 3: Two iPads — Assignment Tracker + Grade Calculator
# ════════════════════════════════════════════════════════════
def make_image_03():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (50, 45, 150), (80, 55, 170))

    # Accent shapes
    draw.ellipse((-150, -150, 450, 450), fill=(70, 65, 175))
    draw.ellipse((W - 400, H - 400, W + 100, H + 100), fill=(70, 65, 175))

    # Title
    draw.text((W // 2 - 380, 55), "Track Assignments & Calculate Grades", fill=WHITE, font=font(46, True))
    draw.text((W // 2 - 280, 115), "Never miss a deadline. Always know your GPA.", fill=(210, 210, 240), font=font(26))

    iw, ih = 1160, 1650
    gap = 120
    total = 2 * iw + gap
    start_x = (W - total) // 2
    ipad_y = 210

    def assignment_detail(img, sx, sy, sw, sh):
        d = ImageDraw.Draw(img)
        d.rectangle((sx, sy, sx + sw, sy + 65), fill=CORAL)
        d.text((sx + 18, sy + 16), "ASSIGNMENT TRACKER", fill=WHITE, font=font(26, True))
        d.text((sx + sw - 130, sy + 22), "Fall 2026", fill=(255, 220, 220), font=font(20))

        col_y = sy + 78
        d.rectangle((sx, col_y, sx + sw, col_y + 38), fill=PALE_INDIGO)
        headers = ["Class", "Assignment", "Due", "Status", "Priority"]
        hxs = [sx + 12, sx + 120, sx + 370, sx + 490, sx + 650]
        for h_text, hx in zip(headers, hxs):
            d.text((hx, col_y + 8), h_text, fill=DARK, font=font(16, True))

        rows = [
            ("PSY 101", "Chapter 3 Reading", "Feb 8", "Graded", "Low", (76, 175, 80)),
            ("MATH 202", "Problem Set 4", "Feb 10", "Graded", "Med", (76, 175, 80)),
            ("ENG 110", "Persuasive Essay Draft", "Feb 15", "In Progress", "High", CORAL),
            ("CS 150", "Lab 3: Loops", "Feb 12", "In Progress", "High", CORAL),
            ("PSY 101", "Midterm Study Guide", "Feb 20", "Not Started", "Med", MID_GRAY),
            ("MATH 202", "Chapter 8 Problems", "Feb 18", "In Progress", "Med", SUNSHINE),
            ("HIST 210", "Research Proposal", "Feb 22", "Not Started", "High", MID_GRAY),
            ("CS 150", "Project 1 Proposal", "Feb 25", "Not Started", "Low", MID_GRAY),
            ("ENG 110", "Peer Review", "Feb 17", "Submitted", "Med", TEAL),
            ("HIST 210", "Map Quiz", "Feb 14", "Graded", "Low", (76, 175, 80)),
            ("MATH 202", "Quiz 3", "Feb 16", "Submitted", "Med", TEAL),
            ("PSY 101", "Lab Report 2", "Feb 19", "In Progress", "High", CORAL),
            ("CS 150", "Reading: Ch 5", "Feb 13", "Graded", "Low", (76, 175, 80)),
            ("ENG 110", "Grammar Exercise", "Feb 11", "Graded", "Low", (76, 175, 80)),
            ("HIST 210", "Chapter 6 Notes", "Feb 21", "Not Started", "Med", MID_GRAY),
            ("MATH 202", "Extra Credit Set", "Feb 28", "Not Started", "Low", MID_GRAY),
            ("PSY 101", "Group Presentation", "Mar 1", "Not Started", "High", MID_GRAY),
            ("CS 150", "Midterm Review", "Feb 26", "Not Started", "Med", MID_GRAY),
            ("ENG 110", "Final Essay Outline", "Mar 3", "Not Started", "High", MID_GRAY),
            ("HIST 210", "Documentary Review", "Feb 24", "Not Started", "Med", MID_GRAY),
            ("MATH 202", "Midterm Prep", "Feb 27", "Not Started", "High", MID_GRAY),
            ("PSY 101", "Online Discussion", "Feb 16", "Submitted", "Low", TEAL),
            ("CS 150", "Lab 4: Functions", "Mar 2", "Not Started", "High", MID_GRAY),
            ("ENG 110", "Bibliography", "Feb 23", "Not Started", "Med", MID_GRAY),
        ]

        ry = col_y + 38
        rh = 42
        for i, (cls, asgn, due, status, prio, scol) in enumerate(rows):
            if ry + rh > sy + sh - 5:
                break
            bg = WHITE if i % 2 == 0 else NEAR_WHITE
            d.rectangle((sx, ry, sx + sw, ry + rh), fill=bg)
            d.text((hxs[0], ry + 11), cls, fill=INDIGO, font=font(14, True))
            d.text((hxs[1], ry + 11), asgn[:20], fill=DARK, font=font(14))
            d.text((hxs[2], ry + 11), due, fill=DARK, font=font(14))
            draw_status_badge(d, hxs[3], ry + 8, status, scol, font(12, True))
            pcol = CORAL if prio == "High" else (SUNSHINE if prio == "Med" else TEAL)
            d.text((hxs[4], ry + 11), prio, fill=pcol, font=font(14, True))
            ry += rh

    def grade_detail(img, sx, sy, sw, sh):
        d = ImageDraw.Draw(img)
        d.rectangle((sx, sy, sx + sw, sy + 65), fill=VIOLET)
        d.text((sx + 18, sy + 16), "GRADE CALCULATOR", fill=WHITE, font=font(26, True))

        # Overall GPA card
        card_y = sy + 80
        d.rounded_rectangle((sx + 15, card_y, sx + sw - 15, card_y + 90), radius=12, fill=PALE_INDIGO)
        d.text((sx + 35, card_y + 10), "Semester GPA", fill=MID_GRAY, font=font(18))
        d.text((sx + 35, card_y + 38), "3.42", fill=INDIGO, font=font(36, True))
        d.text((sx + 170, card_y + 50), "/ 4.00", fill=MID_GRAY, font=font(20))
        # Mini bar
        d.rounded_rectangle((sx + sw - 220, card_y + 30, sx + sw - 35, card_y + 50), radius=10, fill=LIGHT_GRAY)
        d.rounded_rectangle((sx + sw - 220, card_y + 30, sx + sw - 220 + int(185 * 0.855), card_y + 50), radius=10, fill=INDIGO)
        d.text((sx + sw - 210, card_y + 8), "Target: 3.50", fill=VIOLET, font=font(15, True))

        # Grade table
        table_y = card_y + 110
        d.rectangle((sx + 15, table_y, sx + sw - 15, table_y + 36), fill=PALE_INDIGO)
        th = ["Class", "HW", "Quiz", "Mid", "Proj", "Avg", "Grade"]
        txs = [sx + 25, sx + 180, sx + 270, sx + 355, sx + 440, sx + 530, sx + 630]
        for t, tx in zip(th, txs):
            d.text((tx, table_y + 8), t, fill=DARK, font=font(15, True))

        grades = [
            ("Intro Psychology", "92", "88", "85", "90", "89.3", "A-"),
            ("Calculus II", "88", "82", "79", "91", "86.1", "B+"),
            ("English Comp", "95", "93", "91", "94", "93.2", "A"),
            ("Intro to CS", "85", "80", "82", "88", "84.5", "B"),
            ("World History", "90", "94", "88", "92", "91.0", "A-"),
        ]

        ry = table_y + 36
        for i, (cls, hw, qz, mid, proj, avg, grade) in enumerate(grades):
            bg = WHITE if i % 2 == 0 else NEAR_WHITE
            d.rectangle((sx + 15, ry, sx + sw - 15, ry + 48), fill=bg)
            d.text((txs[0], ry + 14), cls[:16], fill=DARK, font=font(14, True))
            d.text((txs[1], ry + 14), hw, fill=DARK, font=font(14))
            d.text((txs[2], ry + 14), qz, fill=DARK, font=font(14))
            d.text((txs[3], ry + 14), mid, fill=DARK, font=font(14))
            d.text((txs[4], ry + 14), proj, fill=DARK, font=font(14))
            d.text((txs[5], ry + 14), avg, fill=INDIGO, font=font(14, True))
            gcol = (76, 175, 80) if grade.startswith("A") else SUNSHINE
            d.rounded_rectangle((txs[6] - 4, ry + 8, txs[6] + 46, ry + 38), radius=8, fill=gcol)
            d.text((txs[6] + 4, ry + 12), grade, fill=WHITE, font=font(16, True))
            ry += 48

        # Grade breakdown chart
        chart_y = ry + 30
        d.text((sx + 25, chart_y), "Grade Distribution", fill=DARK, font=font(20, True))
        chart_y += 35
        dist = [("A/A-", 3, (76, 175, 80)), ("B+/B", 2, SUNSHINE), ("C+/C", 0, CORAL)]
        bar_max_w = sw - 120
        total_classes = 5
        for label, count, col in dist:
            bw = int(bar_max_w * count / total_classes) if count > 0 else 4
            d.text((sx + 25, chart_y + 4), label, fill=DARK, font=font(15))
            d.rounded_rectangle((sx + 100, chart_y, sx + 100 + bw, chart_y + 28), radius=8, fill=col)
            if count > 0:
                d.text((sx + 105, chart_y + 3), str(count), fill=WHITE, font=font(15, True))
            chart_y += 40

        # Credit summary
        cred_y = chart_y + 20
        d.rounded_rectangle((sx + 15, cred_y, sx + sw - 15, cred_y + 80), radius=10, fill=PALE_INDIGO)
        d.text((sx + 30, cred_y + 10), "Credits This Semester", fill=MID_GRAY, font=font(16))
        d.text((sx + 30, cred_y + 36), "16 Credits", fill=DARK, font=font(26, True))
        d.text((sx + 250, cred_y + 42), "(5 Classes)", fill=MID_GRAY, font=font(18))

    draw_ipad(img, start_x, ipad_y, iw, ih, assignment_detail)
    draw_ipad(img, start_x + iw + gap, ipad_y, iw, ih, grade_detail)

    # Labels below
    lbl_y = ipad_y + ih + 30
    draw.rounded_rectangle((start_x + iw // 2 - 150, lbl_y, start_x + iw // 2 + 150, lbl_y + 48), radius=24, fill=CORAL)
    draw.text((start_x + iw // 2 - 120, lbl_y + 10), "Assignment Tracker", fill=WHITE, font=font(22, True))

    rx = start_x + iw + gap
    draw.rounded_rectangle((rx + iw // 2 - 130, lbl_y, rx + iw // 2 + 130, lbl_y + 48), radius=24, fill=VIOLET)
    draw.text((rx + iw // 2 - 105, lbl_y + 10), "Grade Calculator", fill=WHITE, font=font(22, True))

    img.save(os.path.join(OUTDIR, "03_assignments_grades.png"), quality=95)
    print("  [OK] 03_assignments_grades.png")


# ════════════════════════════════════════════════════════════
# IMAGE 4: Two iPads — Study Planner + Class Schedule
# ════════════════════════════════════════════════════════════
def make_image_04():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (40, 100, 140), (60, 55, 160))

    # Accent
    draw.ellipse((W - 350, -200, W + 200, 350), fill=(60, 130, 160))
    draw.ellipse((-200, H - 350, 350, H + 100), fill=(60, 130, 160))

    draw.text((W // 2 - 340, 55), "Plan Your Study Time & Schedule", fill=WHITE, font=font(48, True))
    draw.text((W // 2 - 280, 120), "Organized days lead to better grades.", fill=(200, 220, 240), font=font(26))

    iw, ih = 1160, 1650
    gap = 120
    total = 2 * iw + gap
    start_x = (W - total) // 2
    ipad_y = 200

    def study_planner_screen(img, sx, sy, sw, sh):
        d = ImageDraw.Draw(img)
        d.rectangle((sx, sy, sx + sw, sy + 65), fill=TEAL)
        d.text((sx + 18, sy + 16), "WEEKLY STUDY PLANNER", fill=WHITE, font=font(26, True))

        # Week selector
        wk_y = sy + 78
        d.rectangle((sx, wk_y, sx + sw, wk_y + 36), fill=(240, 248, 248))
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        dw = sw // 7
        for i, day in enumerate(days):
            dx = sx + i * dw
            if i == 0:  # Monday selected
                d.rectangle((dx, wk_y, dx + dw, wk_y + 36), fill=TEAL)
                d.text((dx + dw // 2 - 15, wk_y + 8), day, fill=WHITE, font=font(16, True))
            else:
                d.text((dx + dw // 2 - 15, wk_y + 8), day, fill=MID_GRAY, font=font(16))

        # Study blocks
        blocks = [
            ("8:00 AM", "Morning Review", "MATH 202", "Review Ch 7 problems", "1.5 hrs", "Library", True, INDIGO),
            ("10:00 AM", "Reading", "PSY 101", "Read Chapter 4", "1 hr", "Dorm Room", True, VIOLET),
            ("12:00 PM", "Lunch Break", "", "", "1 hr", "Cafeteria", True, MID_GRAY),
            ("1:00 PM", "Writing Block", "ENG 110", "Write essay outline", "2 hrs", "Coffee Shop", False, CORAL),
            ("3:00 PM", "Lab Prep", "CS 150", "Pre-lab exercises", "1.5 hrs", "Tech Lab", False, TEAL),
            ("5:00 PM", "History Notes", "HIST 210", "Chapter 6 notes", "1 hr", "Library", False, SUNSHINE),
            ("7:00 PM", "Problem Sets", "MATH 202", "Practice problems Ch 8", "2 hrs", "Dorm Room", False, INDIGO),
            ("9:00 PM", "Review", "PSY 101", "Flashcards midterm", "1 hr", "Dorm Room", False, VIOLET),
        ]

        by = wk_y + 48
        for time, label, subj, task, dur, loc, done, col in blocks:
            if by + 70 > sy + sh:
                break
            # Time column
            d.text((sx + 12, by + 15), time, fill=MID_GRAY, font=font(13))
            # Card
            cx = sx + 110
            cw = sw - 125
            card_bg = (245, 250, 245) if done else NEAR_WHITE
            d.rounded_rectangle((cx, by, cx + cw, by + 65), radius=8, fill=card_bg, outline=col, width=2)
            # Color bar on left
            d.rounded_rectangle((cx, by, cx + 6, by + 65), radius=3, fill=col)
            # Content
            d.text((cx + 16, by + 5), label, fill=DARK, font=font(15, True))
            if subj:
                d.text((cx + 16, by + 26), f"{subj}: {task[:28]}", fill=MID_GRAY, font=font(13))
            d.text((cx + 16, by + 44), f"{dur}  ·  {loc}", fill=col, font=font(12))
            # Checkbox
            cbx = cx + cw - 35
            cby = by + 20
            if done:
                d.rounded_rectangle((cbx, cby, cbx + 24, cby + 24), radius=4, fill=(76, 175, 80))
                d.text((cbx + 4, cby + 1), "✓", fill=WHITE, font=font(16, True))
            else:
                d.rounded_rectangle((cbx, cby, cbx + 24, cby + 24), radius=4, fill=WHITE, outline=MID_GRAY, width=2)
            by += 75

        # Summary bar
        d.rectangle((sx, sy + sh - 50, sx + sw, sy + sh), fill=(240, 248, 248))
        d.text((sx + 15, sy + sh - 40), "Total: 11 hrs", fill=DARK, font=font(17, True))
        d.text((sx + 200, sy + sh - 40), "Completed: 3/8", fill=TEAL, font=font(17))

    def class_schedule_screen(img, sx, sy, sw, sh):
        d = ImageDraw.Draw(img)
        d.rectangle((sx, sy, sx + sw, sy + 65), fill=INDIGO)
        d.text((sx + 18, sy + 16), "CLASS SCHEDULE — FALL 2026", fill=WHITE, font=font(24, True))

        # Table header
        th_y = sy + 78
        d.rectangle((sx, th_y, sx + sw, th_y + 38), fill=PALE_INDIGO)
        cols = ["Class", "Code", "Professor", "Days", "Time", "Room", "Cr"]
        cxs = [sx + 12, sx + 180, sx + 295, sx + 440, sx + 520, sx + 640, sx + 740]
        for c, cx in zip(cols, cxs):
            d.text((cx, th_y + 8), c, fill=DARK, font=font(15, True))

        classes = [
            ("Intro Psychology", "PSY 101", "Dr. Martinez", "MWF", "9:00-9:50", "Hall 204", "3"),
            ("Calculus II", "MATH 202", "Prof. Chen", "TTh", "10:30-11:45", "Sci 301", "4"),
            ("English Comp", "ENG 110", "Dr. Williams", "MWF", "1:00-1:50", "Lib 105", "3"),
            ("Intro to CS", "CS 150", "Dr. Patel", "TTh", "2:00-3:15", "Tech 210", "3"),
            ("World History", "HIST 210", "Prof. Adams", "MWF", "3:00-3:50", "Main 108", "3"),
        ]

        ry = th_y + 38
        colors_cycle = [INDIGO, TEAL, CORAL, VIOLET, SUNSHINE]
        for i, (name, code, prof, days, time, room, cr) in enumerate(classes):
            bg = WHITE if i % 2 == 0 else NEAR_WHITE
            d.rectangle((sx, ry, sx + sw, ry + 70), fill=bg)
            # Color indicator
            d.rectangle((sx, ry, sx + 5, ry + 70), fill=colors_cycle[i])
            d.text((cxs[0], ry + 8), name[:17], fill=DARK, font=font(15, True))
            d.text((cxs[1], ry + 8), code, fill=INDIGO, font=font(14))
            d.text((cxs[2], ry + 8), prof[:14], fill=MID_GRAY, font=font(14))
            d.text((cxs[3], ry + 8), days, fill=DARK, font=font(14, True))
            d.text((cxs[4], ry + 8), time, fill=DARK, font=font(14))
            d.text((cxs[5], ry + 8), room, fill=MID_GRAY, font=font(14))
            d.text((cxs[6], ry + 8), cr, fill=DARK, font=font(14, True))
            # Second row: office hours
            d.text((cxs[0] + 10, ry + 35), "Office Hrs:", fill=MID_GRAY, font=font(12))
            oh_texts = ["Tue 2-4 PM", "Mon 3-5 PM", "Wed 1-3 PM", "Thu 2-4 PM", "Fri 10-12 PM"]
            d.text((cxs[1], ry + 35), oh_texts[i], fill=TEAL, font=font(12))
            ry += 70

        # Weekly view
        wv_y = ry + 20
        d.text((sx + 15, wv_y), "WEEKLY VIEW", fill=DARK, font=font(18, True))
        wv_y += 30

        # Mini timetable grid
        days_header = ["", "Mon", "Tue", "Wed", "Thu", "Fri"]
        col_w = (sw - 80) // 5
        for di, day in enumerate(days_header):
            dx = sx + 60 + (di - 1) * col_w if di > 0 else sx + 5
            if di > 0:
                d.rectangle((dx, wv_y, dx + col_w - 4, wv_y + 25), fill=PALE_INDIGO)
            d.text((dx + 5, wv_y + 4), day, fill=DARK, font=font(13, True))

        time_slots = ["9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM"]
        slot_h = 32
        ty = wv_y + 30
        # Schedule blocks: (day_idx 0-4, start_slot, span, name, color)
        blocks = [
            (0, 0, 1, "PSY", INDIGO), (2, 0, 1, "PSY", INDIGO), (4, 0, 1, "PSY", INDIGO),
            (1, 1, 2, "MATH", TEAL), (3, 1, 2, "MATH", TEAL),
            (0, 4, 1, "ENG", CORAL), (2, 4, 1, "ENG", CORAL), (4, 4, 1, "ENG", CORAL),
            (1, 5, 2, "CS", VIOLET), (3, 5, 2, "CS", VIOLET),
            (0, 6, 1, "HIST", SUNSHINE), (2, 6, 1, "HIST", SUNSHINE), (4, 6, 1, "HIST", SUNSHINE),
        ]

        for si, ts in enumerate(time_slots):
            slot_y = ty + si * slot_h
            if slot_y + slot_h > sy + sh - 10:
                break
            d.text((sx + 5, slot_y + 6), ts, fill=MID_GRAY, font=font(11))
            d.line([(sx + 60, slot_y), (sx + sw - 10, slot_y)], fill=LIGHT_GRAY, width=1)

        for day_i, start, span, name, col in blocks:
            bx = sx + 60 + day_i * col_w
            by = ty + start * slot_h
            bh = span * slot_h
            if by + bh > sy + sh - 10:
                continue
            d.rounded_rectangle((bx + 2, by + 2, bx + col_w - 6, by + bh - 2), radius=6, fill=col)
            d.text((bx + 8, by + bh // 2 - 8), name, fill=WHITE, font=font(13, True))

    draw_ipad(img, start_x, ipad_y, iw, ih, study_planner_screen)
    draw_ipad(img, start_x + iw + gap, ipad_y, iw, ih, class_schedule_screen)

    # Labels
    lbl_y = ipad_y + ih + 30
    draw.rounded_rectangle((start_x + iw // 2 - 120, lbl_y, start_x + iw // 2 + 120, lbl_y + 48), radius=24, fill=TEAL)
    draw.text((start_x + iw // 2 - 95, lbl_y + 10), "Study Planner", fill=WHITE, font=font(22, True))

    rx = start_x + iw + gap
    draw.rounded_rectangle((rx + iw // 2 - 120, lbl_y, rx + iw // 2 + 120, lbl_y + 48), radius=24, fill=INDIGO)
    draw.text((rx + iw // 2 - 95, lbl_y + 10), "Class Schedule", fill=WHITE, font=font(22, True))

    img.save(os.path.join(OUTDIR, "04_study_schedule.png"), quality=95)
    print("  [OK] 04_study_schedule.png")


# ════════════════════════════════════════════════════════════
# IMAGE 5: Value Prop — $7.99 INSTANT DOWNLOAD
# ════════════════════════════════════════════════════════════
def make_image_05():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, W, H, (55, 48, 163), (100, 70, 195))

    # Large decorative circles
    draw.ellipse((W // 2 - 600, H // 2 - 600, W // 2 + 600, H // 2 + 600), fill=(65, 58, 175))
    draw.ellipse((W // 2 - 400, H // 2 - 400, W // 2 + 400, H // 2 + 400), fill=(75, 68, 185))

    # Price badge (large, centered)
    badge_cx, badge_cy = W // 2, 320
    badge_r = 180
    draw.ellipse((badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r), fill=SUNSHINE)
    draw.ellipse((badge_cx - badge_r + 8, badge_cy - badge_r + 8, badge_cx + badge_r - 8, badge_cy + badge_r - 8), fill=SUNSHINE, outline=WHITE, width=4)
    draw.text((badge_cx - 95, badge_cy - 60), "$7.99", fill=DARK, font=font(72, True))
    draw.text((badge_cx - 55, badge_cy + 25), "ONE TIME", fill=(100, 80, 30), font=font(22, True))

    # Main title
    title_y = 550
    draw.text((W // 2 - 450, title_y), "INSTANT DOWNLOAD", fill=WHITE, font=font(72, True))
    draw.text((W // 2 - 365, title_y + 90), "Your Complete Academic Toolkit", fill=(220, 220, 245), font=font(36))

    # Feature cards — 2 columns of 4
    features = [
        ("8 Organized Tabs", "Dashboard, Schedule, Assignments, Grades, Study, Expenses, Goals + Guide", INDIGO),
        ("Auto GPA Calculator", "Enter grades once — weighted averages and letter grades calculated instantly", VIOLET),
        ("Assignment Tracker", "Never miss a deadline with status badges, priority flags, and due-date tracking", CORAL),
        ("Study Planner", "Plan every study block by class, location, and duration for maximum focus", TEAL),
        ("Expense Tracker", "Track textbooks, food, supplies, and more — see exactly where your money goes", SUNSHINE),
        ("Semester Goals", "Set academic, career, health, and personal goals with progress tracking", INDIGO),
        ("Works Everywhere", "Fully compatible with Excel, Google Sheets, and Apple Numbers", (76, 175, 80)),
        ("Print-Friendly", "Clean layouts that look great on screen and on paper", VIOLET),
    ]

    cards_y = title_y + 165
    card_w = 1150
    card_h = 110
    gap_x = 80
    gap_y = 25
    col1_x = (W - 2 * card_w - gap_x) // 2
    col2_x = col1_x + card_w + gap_x

    for i, (title, desc, col) in enumerate(features):
        cx = col1_x if i % 2 == 0 else col2_x
        cy = cards_y + (i // 2) * (card_h + gap_y)
        # Card background
        draw.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=16, fill=(255, 255, 255, 240))
        draw.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), radius=16, fill=WHITE)
        # Accent bar left
        draw.rounded_rectangle((cx, cy, cx + 8, cy + card_h), radius=4, fill=col)
        # Icon circle
        draw.ellipse((cx + 22, cy + 20, cx + 72, cy + 70), fill=col)
        # Checkmark in circle
        draw.text((cx + 34, cy + 28), "✓", fill=WHITE, font=font(24, True))
        # Title + description
        draw.text((cx + 85, cy + 15), title, fill=DARK, font=font(22, True))
        draw.text((cx + 85, cy + 48), desc[:65], fill=MID_GRAY, font=font(16))
        if len(desc) > 65:
            draw.text((cx + 85, cy + 72), desc[65:], fill=MID_GRAY, font=font(16))

    # Bottom CTA
    cta_y = H - 180
    draw.rounded_rectangle((W // 2 - 350, cta_y, W // 2 + 350, cta_y + 80), radius=40, fill=SUNSHINE)
    draw.text((W // 2 - 280, cta_y + 16), "Download Now — Start Planning Today", fill=DARK, font=font(28, True))

    # Bottom text
    draw.text((W // 2 - 340, H - 75), "Instant PDF + XLSX  |  No subscription  |  Lifetime access", fill=(200, 200, 230), font=font(22))

    img.save(os.path.join(OUTDIR, "05_value_proposition.png"), quality=95)
    print("  [OK] 05_value_proposition.png")


# ═══════════════════════════════════════════════
# Run all
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Student Academic Planner 2026 images...")
    make_image_01()
    make_image_02()
    make_image_03()
    make_image_04()
    make_image_05()
    print("\nAll 5 images generated successfully!")
