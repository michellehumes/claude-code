#!/usr/bin/env python3
"""
Generate 5 Etsy listing images for Resume & Job Search Tracker Bundle 2026.
All images: 2700x2025 PNG
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Paths ──
OUT = "/home/user/claude-code/etsy-digital-download-5/images"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
os.makedirs(OUT, exist_ok=True)

# ── Colors ──
DEEP_BLUE  = (26, 54, 93)
TEAL       = (43, 108, 176)
LIGHT_BLUE = (190, 227, 248)
ICE        = (235, 248, 255)
CORAL      = (229, 62, 62)
GOLD       = (214, 158, 46)
WHITE      = (255, 255, 255)
BLACK      = (0, 0, 0)
DARK_BG    = (15, 32, 56)
MID_BLUE   = (34, 80, 140)
SOFT_GREEN = (56, 161, 105)
SOFT_ORANGE= (221, 146, 46)
PALE_GOLD  = (255, 243, 207)
LIGHT_CORAL= (254, 235, 235)
LIGHT_GREEN= (230, 255, 237)
LIGHT_TEAL = (220, 240, 255)
SHADOW     = (0, 0, 0, 60)
GRAY       = (120, 130, 145)
LGRAY      = (200, 210, 220)
BADGE_APPLIED  = (66, 153, 225)
BADGE_INTERVIEW= (214, 158, 46)
BADGE_OFFER    = (56, 161, 105)
BADGE_REJECTED = (229, 62, 62)

def font(size):
    return ImageFont.truetype(FONT_PATH, size)

# ── Drawing helpers ──

def rounded_rect(draw, xy, radius, fill=None, outline=None, width=0):
    x0, y0, x1, y1 = xy
    r = radius
    # Use pieslice + rectangles for rounded rect
    draw.pieslice([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=fill, outline=outline, width=width)
    draw.rectangle([x0+r, y0, x1-r, y1], fill=fill, outline=None)
    draw.rectangle([x0, y0+r, x1, y1-r], fill=fill, outline=None)
    if outline and width:
        draw.arc([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0+r, y0, x1-r, y0], fill=outline, width=width)
        draw.line([x0+r, y1, x1-r, y1], fill=outline, width=width)
        draw.line([x0, y0+r, x0, y1-r], fill=outline, width=width)
        draw.line([x1, y0+r, x1, y1-r], fill=outline, width=width)


def gradient_bg(img, c1, c2, vertical=True):
    """Fill image with linear gradient from c1 to c2."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    steps = h if vertical else w
    for i in range(steps):
        ratio = i / max(steps - 1, 1)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        if vertical:
            draw.line([(0, i), (w, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, h)], fill=(r, g, b))
    return draw


def draw_ipad(img, x, y, w, h, bezel=18, cam_side="top"):
    """Draw an iPad mockup frame at (x,y) with inner screen w x h.
       Returns (sx, sy, sw, sh) for the screen area."""
    draw = ImageDraw.Draw(img)
    # Shadow
    shadow_img = Image.new("RGBA", img.size, (0,0,0,0))
    sd = ImageDraw.Draw(shadow_img)
    for s in range(12, 0, -1):
        alpha = int(35 * (1 - s/12))
        rounded_rect(sd, (x-bezel+s+4, y-bezel+s+4, x+w+bezel+s+4, y+h+bezel+s+4),
                      bezel+10, fill=(0,0,0,alpha))
    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0,0,0,0)), shadow_img), (0,0), shadow_img)

    draw = ImageDraw.Draw(img)
    # Outer bezel
    rounded_rect(draw, (x-bezel, y-bezel, x+w+bezel, y+h+bezel),
                 bezel+8, fill=(30, 30, 35))
    # Inner bezel highlight
    rounded_rect(draw, (x-bezel+2, y-bezel+2, x+w+bezel-2, y+h+bezel-2),
                 bezel+6, fill=(50, 50, 58))
    # Screen area (white base)
    draw.rectangle([x, y, x+w, y+h], fill=WHITE)
    # Camera dot
    if cam_side == "top":
        cx = x + w // 2
        cy = y - bezel // 2
    else:
        cx = x - bezel // 2
        cy = y + h // 2
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(20,20,25))
    draw.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(40,45,60))
    return (x, y, w, h)


def draw_spreadsheet_header(draw, sx, sy, sw, cols, col_widths, header_color=TEAL,
                             text_color=WHITE, row_h=36, fsize=18):
    """Draw a header row for a spreadsheet."""
    cx = sx
    f = font(fsize)
    for i, col in enumerate(cols):
        cw = col_widths[i]
        draw.rectangle([cx, sy, cx+cw, sy+row_h], fill=header_color)
        # center text
        bbox = f.getbbox(col)
        tw = bbox[2] - bbox[0]
        draw.text((cx + (cw - tw)//2, sy + 6), col, fill=text_color, font=f)
        cx += cw
    return sy + row_h


def draw_spreadsheet_row(draw, sx, sy, sw, values, col_widths, bg=WHITE,
                          text_color=DEEP_BLUE, row_h=34, fsize=16, badges=None):
    """Draw one data row. badges is dict of col_index -> badge_color."""
    cx = sx
    f = font(fsize)
    for i, val in enumerate(values):
        cw = col_widths[i]
        draw.rectangle([cx, sy, cx+cw, sy+row_h], fill=bg)
        draw.line([(cx, sy+row_h), (cx+cw, sy+row_h)], fill=LGRAY, width=1)
        if badges and i in badges:
            # Draw badge pill
            bbox = f.getbbox(val)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            bx = cx + (cw - tw)//2 - 10
            by = sy + 5
            bw = tw + 20
            bh = row_h - 10
            rounded_rect(draw, (bx, by, bx+bw, by+bh), 10, fill=badges[i])
            draw.text((bx+10, by+2), val, fill=WHITE, font=f)
        else:
            bbox = f.getbbox(val)
            tw = bbox[2] - bbox[0]
            tx = cx + 8 if i == 0 else cx + (cw - tw)//2
            draw.text((tx, sy + 7), val, fill=text_color, font=f)
        cx += cw
    return sy + row_h


def draw_annotation(draw, x1, y1, x2, y2, text, color=CORAL, fsize=20):
    """Draw annotation line + label from (x1,y1) label to (x2,y2) point."""
    f = font(fsize)
    draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    # dot at target
    draw.ellipse([x2-6, y2-6, x2+6, y2+6], fill=color)
    # text bg
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 8
    rounded_rect(draw, (x1-pad, y1-th//2-pad, x1+tw+pad, y1+th//2+pad), 8, fill=color)
    draw.text((x1, y1-th//2-2), text, fill=WHITE, font=f)


def draw_feature_pill(draw, cx, cy, text, bg=TEAL, fg=WHITE, fsize=22):
    f = font(fsize)
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 20, 10
    x0 = cx - tw//2 - pad_x
    y0 = cy - th//2 - pad_y
    x1 = cx + tw//2 + pad_x
    y1 = cy + th//2 + pad_y
    rounded_rect(draw, (x0, y0, x1, y1), (y1-y0)//2, fill=bg)
    draw.text((cx - tw//2, cy - th//2 - 2), text, fill=fg, font=f)
    return x1  # return right edge


def draw_bottom_bar(draw, y, w, h=70, text="Instant Download  |  Google Sheets & Excel  |  Lifetime Access"):
    """Dark bottom bar."""
    draw.rectangle([0, y, w, y+h], fill=DEEP_BLUE)
    f = font(22)
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    draw.text(((w-tw)//2, y+22), text, fill=LIGHT_BLUE, font=f)


def draw_star_rating(draw, cx, cy, size=28, stars=5, color=GOLD):
    """Draw 5 stars centered at cx, cy."""
    f = font(size)
    star_text = "\u2605" * stars
    bbox = f.getbbox(star_text)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw//2, cy - size//2), star_text, fill=color, font=f)


# ============================================================
# IMAGE 1: Hero – Main Listing
# ============================================================
def create_image_1():
    W, H = 2700, 2025
    img = Image.new("RGBA", (W, H))
    gradient_bg(img, ICE, LIGHT_BLUE)
    draw = ImageDraw.Draw(img)

    # Decorative circles
    for cx, cy, r, c in [(150, 150, 200, (*TEAL, 25)), (2550, 300, 280, (*LIGHT_BLUE, 40)),
                          (200, 1800, 160, (*GOLD, 20)), (2500, 1700, 220, (*TEAL, 20))]:
        for ri in range(r, 0, -1):
            alpha = int(c[3] * (ri / r))
            draw.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(*c[:3], alpha))

    # ── Title ──
    title_f = font(80)
    title = "RESUME & JOB SEARCH"
    bbox = title_f.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 55), title, fill=DEEP_BLUE, font=title_f)

    title2 = "TRACKER BUNDLE"
    bbox2 = title_f.getbbox(title2)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W-tw2)//2, 145), title2, fill=TEAL, font=title_f)

    # 2026 badge
    badge_f = font(52)
    btext = "2026"
    bbox_b = badge_f.getbbox(btext)
    btw = bbox_b[2] - bbox_b[0]
    bx = (W + tw2)//2 + 30
    by = 150
    rounded_rect(draw, (bx, by, bx+btw+36, by+62), 14, fill=CORAL)
    draw.text((bx+18, by+4), btext, fill=WHITE, font=badge_f)

    # Subtitle
    sub_f = font(30)
    sub = "Track Applications, Interviews, Networking & More — All in One Spreadsheet"
    bbox_s = sub_f.getbbox(sub)
    stw = bbox_s[2] - bbox_s[0]
    draw.text(((W-stw)//2, 245), sub, fill=GRAY, font=sub_f)

    # ── Main iPad ──
    ipad_w, ipad_h = 1800, 1000
    ix = (W - ipad_w) // 2
    iy = 340
    sx, sy, sw, sh = draw_ipad(img, ix, iy, ipad_w, ipad_h, bezel=22)
    draw = ImageDraw.Draw(img)

    # Tab bar at top of screen
    tabs = ["Job Application Tracker", "Resume Versions", "Interview Prep", "Networking", "Salary", "Skills", "Weekly Plan", "How to Use"]
    tab_w = sw // len(tabs)
    for ti, tab in enumerate(tabs):
        tx = sx + ti * tab_w
        bg = TEAL if ti == 0 else DEEP_BLUE
        draw.rectangle([tx, sy, tx+tab_w, sy+32], fill=bg)
        tf = font(13)
        bbox_t = tf.getbbox(tab)
        ttw = bbox_t[2] - bbox_t[0]
        draw.text((tx + (tab_w-ttw)//2, sy+8), tab, fill=WHITE, font=tf)

    # Spreadsheet content - Job Application Tracker
    cols = ["Company", "Position", "Date Applied", "Status", "Follow-up", "Salary Range", "Contact", "Notes"]
    col_ws = [200, 220, 160, 140, 140, 180, 200, int(ipad_w - 200-220-160-140-140-180-200)]
    # Adjust last col
    total = sum(col_ws)
    col_ws[-1] = ipad_w - sum(col_ws[:-1])

    header_y = sy + 34
    next_y = draw_spreadsheet_header(draw, sx, header_y, sw, cols, col_ws, row_h=38, fsize=17)

    rows_data = [
        ["Google", "Software Eng.", "Jan 15, 2026", "Applied", "Jan 22", "$150-180K", "recruiter@google", "Referral from J."],
        ["Amazon", "Product Mgr.", "Jan 10, 2026", "Interview", "Jan 18", "$140-170K", "hr@amazon.com", "2nd round Tue"],
        ["Stripe", "UX Designer", "Jan 5, 2026", "Offer", "—", "$130-155K", "talent@stripe", "Offer received!"],
        ["Meta", "Data Analyst", "Jan 12, 2026", "Applied", "Jan 20", "$125-150K", "jobs@meta.com", "Applied online"],
        ["Netflix", "Sr. Engineer", "Jan 8, 2026", "Phone Screen", "Jan 16", "$180-220K", "hire@netflix", "Phone screen done"],
        ["Microsoft", "PM Lead", "Dec 28, 2025", "Rejected", "—", "$160-190K", "msft@hr.com", "No fit currently"],
        ["Apple", "iOS Developer", "Jan 14, 2026", "Applied", "Jan 21", "$155-185K", "recruit@apple", "Via LinkedIn"],
        ["Shopify", "Frontend Dev", "Jan 11, 2026", "Interview", "Jan 19", "$120-145K", "jobs@shopify", "Take-home sent"],
        ["Airbnb", "Backend Eng.", "Jan 6, 2026", "Applied", "Jan 13", "$145-175K", "talent@airbnb", "Employee referral"],
        ["Figma", "Product Desgn.", "Jan 13, 2026", "Interview", "Jan 20", "$135-160K", "hr@figma.com", "Portfolio review"],
        ["Spotify", "ML Engineer", "Jan 9, 2026", "Applied", "Jan 16", "$155-190K", "jobs@spotify", "Applied direct"],
        ["Slack", "Eng. Manager", "Jan 7, 2026", "Phone Screen", "Jan 14", "$170-200K", "hire@slack.com", "Culture fit call"],
        ["Notion", "Full Stack", "Jan 14, 2026", "Applied", "Jan 21", "$140-165K", "work@notion.so", "Startup culture"],
        ["Vercel", "DevOps Eng.", "Jan 12, 2026", "Interview", "Jan 19", "$130-155K", "team@vercel", "System design"],
        ["Databricks", "Data Eng.", "Jan 10, 2026", "Applied", "Jan 17", "$160-195K", "hr@databricks", "Sent resume v3"],
        ["Coinbase", "Blockchain Dev", "Jan 15, 2026", "Applied", "Jan 22", "$165-200K", "jobs@coinbase", "Crypto interest"],
        ["Twilio", "API Engineer", "Jan 8, 2026", "Interview", "Jan 15", "$125-150K", "recruit@twilio", "Tech screen Wed"],
        ["HubSpot", "Growth PM", "Jan 11, 2026", "Applied", "Jan 18", "$115-140K", "hr@hubspot.com", "Marketing exp."],
        ["Canva", "UI Designer", "Jan 6, 2026", "Offer", "—", "$110-135K", "talent@canva", "Start Feb 3!"],
        ["Zoom", "Security Eng.", "Jan 13, 2026", "Applied", "Jan 20", "$145-170K", "jobs@zoom.us", "InfoSec role"],
        ["Palantir", "Fwd Deploy Eng", "Jan 9, 2026", "Phone Screen", "Jan 16", "$150-185K", "hire@palantir", "Problem solving"],
        ["Square", "Mobile Dev", "Jan 14, 2026", "Applied", "Jan 21", "$140-165K", "sq@block.xyz", "Payment systems"],
    ]

    badge_map = {
        "Applied": BADGE_APPLIED,
        "Interview": BADGE_INTERVIEW,
        "Offer": BADGE_OFFER,
        "Rejected": BADGE_REJECTED,
        "Phone Screen": SOFT_ORANGE,
    }

    row_y = next_y
    for ri, row in enumerate(rows_data):
        bg_c = WHITE if ri % 2 == 0 else ICE
        badges = {}
        if row[3] in badge_map:
            badges[3] = badge_map[row[3]]
        row_y = draw_spreadsheet_row(draw, sx, row_y, sw, row, col_ws,
                                      bg=bg_c, row_h=42, fsize=16, badges=badges)
        if row_y > sy + sh - 5:
            break

    # ── Annotations ──
    # Left annotation pointing to status column
    draw_annotation(draw, ix - 250, iy + 250, sx + sum(col_ws[:3]) + 70, header_y + 80,
                    "Status Badges", CORAL, 22)
    # Right annotation pointing to salary
    draw_annotation(draw, ix + ipad_w + 40, iy + 180, sx + sum(col_ws[:5]) + 90, header_y + 120,
                    "Salary Tracking", TEAL, 22)
    # Top-right annotation
    draw_annotation(draw, ix + ipad_w + 40, iy + 350, sx + sum(col_ws[:6]) + 100, header_y + 200,
                    "Contact Info", GOLD, 22)

    # ── Feature pills ──
    pill_y = iy + ipad_h + 100
    pills = [
        ("8 Organized Tabs", TEAL),
        ("Track 100+ Applications", DEEP_BLUE),
        ("Interview Prep", CORAL),
        ("Salary Research", GOLD),
        ("Google Sheets + Excel", MID_BLUE),
    ]
    total_pill_w = 0
    pill_sizes = []
    for text, _ in pills:
        f = font(24)
        bbox = f.getbbox(text)
        pw = bbox[2] - bbox[0] + 50
        pill_sizes.append(pw)
        total_pill_w += pw + 20
    start_x = (W - total_pill_w) // 2
    for i, (text, color) in enumerate(pills):
        cx = start_x + pill_sizes[i] // 2
        draw_feature_pill(draw, cx, pill_y, text, bg=color, fsize=24)
        start_x += pill_sizes[i] + 20

    # ── Bottom bar ──
    draw_bottom_bar(draw, H - 80, W, 80,
                    "Instant Download  ·  Google Sheets & Excel Compatible  ·  Lifetime Access  ·  2026 Edition")

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "01_hero_main_listing.png"), "PNG")
    print("  [OK] 01_hero_main_listing.png")


# ============================================================
# IMAGE 2: What's Included – 7 Mini iPads
# ============================================================
def create_image_2():
    W, H = 2700, 2025
    img = Image.new("RGBA", (W, H))
    gradient_bg(img, DEEP_BLUE, (20, 45, 80))
    draw = ImageDraw.Draw(img)

    # Title
    tf = font(72)
    title = "WHAT'S INCLUDED"
    bbox = tf.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 50), title, fill=WHITE, font=tf)

    sub = font(32)
    st = "8 Professional Tabs — Everything You Need for Your 2026 Job Search"
    bbox_s = sub.getbbox(st)
    stw = bbox_s[2] - bbox_s[0]
    draw.text(((W-stw)//2, 140), st, fill=LIGHT_BLUE, font=sub)

    # 7 mini iPads in grid: row1 = 4, row2 = 3 (centered)
    tab_data = [
        ("Job Application Tracker", [
            ["Company", "Role", "Status"],
            ["Google", "SWE", "Applied"],
            ["Amazon", "PM", "Interview"],
            ["Stripe", "Design", "Offer"],
            ["Meta", "Analyst", "Applied"],
            ["Netflix", "Eng", "Screen"],
        ]),
        ("Resume Versions", [
            ["Version", "Target", "Updated"],
            ["v1 General", "Tech", "Jan 2"],
            ["v2 PM Focus", "PM", "Jan 5"],
            ["v3 Design", "UX", "Jan 8"],
            ["v4 Data", "Analytics", "Jan 10"],
            ["v5 Lead", "Mgmt", "Jan 12"],
        ]),
        ("Interview Prep", [
            ["Company", "Type", "Date"],
            ["Amazon", "Behavioral", "Jan 20"],
            ["Stripe", "Technical", "Jan 22"],
            ["Figma", "Portfolio", "Jan 24"],
            ["Shopify", "Take-home", "Jan 19"],
            ["Vercel", "System Des", "Jan 25"],
        ]),
        ("Networking Tracker", [
            ["Contact", "Company", "Method"],
            ["J. Smith", "Google", "LinkedIn"],
            ["A. Chen", "Meta", "Coffee"],
            ["R. Patel", "Stripe", "Email"],
            ["M. Jones", "Apple", "Event"],
            ["L. Garcia", "Netflix", "Referral"],
        ]),
        ("Salary Research", [
            ["Company", "Role", "Range"],
            ["Google", "SWE", "$150-180K"],
            ["Amazon", "PM", "$140-170K"],
            ["Stripe", "Design", "$130-155K"],
            ["Netflix", "Sr Eng", "$180-220K"],
            ["Apple", "iOS Dev", "$155-185K"],
        ]),
        ("Skills & Certs", [
            ["Skill", "Level", "Status"],
            ["Python", "Advanced", "Current"],
            ["AWS Cert", "Intermed.", "In Prog"],
            ["React", "Advanced", "Current"],
            ["SQL", "Expert", "Current"],
            ["Figma", "Intermed.", "Learning"],
        ]),
        ("Weekly Job Search Plan", [
            ["Day", "Task", "Hours"],
            ["Monday", "Applications", "3h"],
            ["Tuesday", "Networking", "2h"],
            ["Wednesday", "Interview Prep", "3h"],
            ["Thursday", "Skill Building", "2h"],
            ["Friday", "Follow-ups", "1.5h"],
        ]),
    ]

    # Layout: row1 has 4, row2 has 3
    mini_w, mini_h = 500, 340
    gap = 45

    # Row 1 (4 items)
    row1_total = 4 * mini_w + 3 * gap
    row1_x = (W - row1_total) // 2
    row1_y = 240

    # Row 2 (3 items centered)
    row2_total = 3 * mini_w + 2 * gap
    row2_x = (W - row2_total) // 2
    row2_y = 240 + mini_h + 200

    positions = []
    for i in range(4):
        positions.append((row1_x + i * (mini_w + gap), row1_y))
    for i in range(3):
        positions.append((row2_x + i * (mini_w + gap), row2_y))

    label_f = font(22)

    for idx, (tab_name, rows) in enumerate(tab_data):
        px, py = positions[idx]
        sx, sy, sw, sh = draw_ipad(img, px, py, mini_w, mini_h, bezel=12, cam_side="top")
        draw = ImageDraw.Draw(img)

        # Tab header bar
        draw.rectangle([sx, sy, sx+sw, sy+28], fill=TEAL)
        tn_f = font(14)
        bbox_tn = tn_f.getbbox(tab_name)
        tnw = bbox_tn[2] - bbox_tn[0]
        draw.text((sx + (sw-tnw)//2, sy+6), tab_name, fill=WHITE, font=tn_f)

        # Mini spreadsheet
        col_w = sw // len(rows[0])
        hdr_y = sy + 30
        hf = font(12)
        for ci, col in enumerate(rows[0]):
            cx = sx + ci * col_w
            draw.rectangle([cx, hdr_y, cx+col_w, hdr_y+24], fill=DEEP_BLUE)
            bbox_c = hf.getbbox(col)
            cw = bbox_c[2] - bbox_c[0]
            draw.text((cx + (col_w - cw)//2, hdr_y+5), col, fill=WHITE, font=hf)

        df = font(11)
        ry = hdr_y + 24
        for ri, row in enumerate(rows[1:]):
            bg = WHITE if ri % 2 == 0 else ICE
            for ci, val in enumerate(row):
                cx = sx + ci * col_w
                draw.rectangle([cx, ry, cx+col_w, ry+22], fill=bg)
                draw.line([(cx, ry+22), (cx+col_w, ry+22)], fill=LGRAY, width=1)
                bbox_v = df.getbbox(val)
                vw = bbox_v[2] - bbox_v[0]
                draw.text((cx + (col_w - vw)//2, ry+4), val, fill=DEEP_BLUE, font=df)
            ry += 22

        # More rows indicator
        more_f = font(11)
        draw.text((sx + sw//2 - 20, ry + 4), "...", fill=GRAY, font=more_f)

        # Fill remaining screen
        draw.rectangle([sx, ry+22, sx+sw, sy+sh], fill=ICE)
        dots_f = font(14)
        draw.text((sx + sw//2 - 30, sy + sh - 30), "▼ more rows", fill=GRAY, font=dots_f)

        # Label below
        bbox_l = label_f.getbbox(tab_name)
        lw = bbox_l[2] - bbox_l[0]
        label_x = px + (mini_w - lw) // 2
        label_y = py + mini_h + 42
        draw.text((label_x, label_y), tab_name, fill=LIGHT_BLUE, font=label_f)

        # Checkmark
        check_f = font(24)
        draw.text((label_x - 32, label_y - 2), "✓", fill=SOFT_GREEN, font=check_f)

    # Bottom bar
    draw.rectangle([0, H-80, W, H], fill=(10, 25, 50))
    bf = font(24)
    bt = "All 8 Tabs Included  ·  Fully Customizable  ·  Print-Ready  ·  2026 Edition"
    bbox_bt = bf.getbbox(bt)
    btw = bbox_bt[2] - bbox_bt[0]
    draw.text(((W-btw)//2, H-56), bt, fill=LIGHT_BLUE, font=bf)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "02_whats_included.png"), "PNG")
    print("  [OK] 02_whats_included.png")


# ============================================================
# IMAGE 3: Applications + Interviews (Two Overlapping iPads)
# ============================================================
def create_image_3():
    W, H = 2700, 2025
    img = Image.new("RGBA", (W, H))
    gradient_bg(img, ICE, (210, 235, 252))
    draw = ImageDraw.Draw(img)

    # Decorative elements
    for cx, cy, r, c in [(100, 100, 180, (*TEAL, 20)), (2600, 200, 250, (*LIGHT_BLUE, 30)),
                          (2550, 1800, 200, (*GOLD, 15))]:
        for ri in range(r, 0, -2):
            alpha = int(c[3] * (ri / r))
            draw.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(*c[:3], alpha))

    # Title
    tf = font(66)
    title = "TRACK EVERY APPLICATION & INTERVIEW"
    bbox = tf.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 50), title, fill=DEEP_BLUE, font=tf)

    stf = font(28)
    sub = "Never miss a follow-up or interview prep session again"
    bbox_s = stf.getbbox(sub)
    stw = bbox_s[2] - bbox_s[0]
    draw.text(((W-stw)//2, 135), sub, fill=GRAY, font=stf)

    # ── iPad 1 (Back/Left): Job Application Tracker ──
    iw1, ih1 = 1500, 900
    ix1, iy1 = 120, 250
    sx1, sy1, sw1, sh1 = draw_ipad(img, ix1, iy1, iw1, ih1, bezel=20)
    draw = ImageDraw.Draw(img)

    # Tab bar
    draw.rectangle([sx1, sy1, sx1+sw1, sy1+30], fill=TEAL)
    tab_f = font(15)
    draw.text((sx1+10, sy1+7), "◆ Job Application Tracker", fill=WHITE, font=tab_f)

    # Spreadsheet
    app_cols = ["Company", "Position", "Applied", "Status", "Follow-up", "Salary"]
    app_ws = [220, 240, 160, 160, 160, 160]
    # Adjust
    remain = iw1 - sum(app_ws)
    app_ws[-1] += remain

    hy = draw_spreadsheet_header(draw, sx1, sy1+32, sw1, app_cols, app_ws, row_h=36, fsize=17)

    app_rows = [
        ["Google", "Software Engineer", "Jan 15, 2026", "Applied", "Jan 22", "$150-180K"],
        ["Amazon", "Product Manager", "Jan 10, 2026", "Interview", "Jan 18", "$140-170K"],
        ["Stripe", "UX Designer", "Jan 5, 2026", "Offer", "—", "$130-155K"],
        ["Meta", "Data Analyst", "Jan 12, 2026", "Applied", "Jan 20", "$125-150K"],
        ["Netflix", "Sr. Engineer", "Jan 8, 2026", "Phone Screen", "Jan 16", "$180-220K"],
        ["Microsoft", "PM Lead", "Dec 28, 2025", "Rejected", "—", "$160-190K"],
        ["Apple", "iOS Developer", "Jan 14, 2026", "Applied", "Jan 21", "$155-185K"],
        ["Shopify", "Frontend Dev", "Jan 11, 2026", "Interview", "Jan 19", "$120-145K"],
        ["Airbnb", "Backend Eng.", "Jan 6, 2026", "Applied", "Jan 13", "$145-175K"],
        ["Figma", "Product Design", "Jan 13, 2026", "Interview", "Jan 20", "$135-160K"],
        ["Spotify", "ML Engineer", "Jan 9, 2026", "Applied", "Jan 16", "$155-190K"],
        ["Notion", "Full Stack Dev", "Jan 14, 2026", "Applied", "Jan 21", "$140-165K"],
        ["Vercel", "DevOps Eng.", "Jan 12, 2026", "Interview", "Jan 19", "$130-155K"],
        ["Databricks", "Data Engineer", "Jan 10, 2026", "Applied", "Jan 17", "$160-195K"],
        ["Coinbase", "Blockchain Dev", "Jan 15, 2026", "Applied", "Jan 22", "$165-200K"],
        ["Twilio", "API Engineer", "Jan 8, 2026", "Interview", "Jan 15", "$125-150K"],
        ["HubSpot", "Growth PM", "Jan 11, 2026", "Applied", "Jan 18", "$115-140K"],
        ["Canva", "UI Designer", "Jan 6, 2026", "Offer", "—", "$110-135K"],
        ["Zoom", "Security Eng.", "Jan 13, 2026", "Applied", "Jan 20", "$145-170K"],
        ["Palantir", "FDE", "Jan 9, 2026", "Phone Screen", "Jan 16", "$150-185K"],
    ]

    badge_map = {"Applied": BADGE_APPLIED, "Interview": BADGE_INTERVIEW,
                 "Offer": BADGE_OFFER, "Rejected": BADGE_REJECTED, "Phone Screen": SOFT_ORANGE}
    ry = hy
    for ri, row in enumerate(app_rows):
        bg = WHITE if ri % 2 == 0 else ICE
        badges = {3: badge_map[row[3]]} if row[3] in badge_map else {}
        ry = draw_spreadsheet_row(draw, sx1, ry, sw1, row, app_ws, bg=bg, row_h=40, fsize=16, badges=badges)
        if ry > sy1 + sh1 - 5:
            break

    # ── iPad 2 (Front/Right): Interview Prep ──
    iw2, ih2 = 1400, 850
    ix2, iy2 = 1150, 550
    sx2, sy2, sw2, sh2 = draw_ipad(img, ix2, iy2, iw2, ih2, bezel=20)
    draw = ImageDraw.Draw(img)

    # Tab bar
    draw.rectangle([sx2, sy2, sx2+sw2, sy2+30], fill=CORAL)
    draw.text((sx2+10, sy2+7), "◆ Interview Prep", fill=WHITE, font=tab_f)

    # Spreadsheet
    int_cols = ["Company", "Round", "Date", "Type", "Prep Status", "Notes"]
    int_ws = [200, 180, 160, 180, 180, 160]
    remain2 = iw2 - sum(int_ws)
    int_ws[-1] += remain2

    hy2 = draw_spreadsheet_header(draw, sx2, sy2+32, sw2, int_cols, int_ws,
                                   header_color=CORAL, row_h=36, fsize=17)

    int_rows = [
        ["Amazon", "Round 2", "Jan 20", "Behavioral", "Ready", "STAR method"],
        ["Stripe", "Final", "Jan 22", "Technical", "In Progress", "Algo practice"],
        ["Shopify", "Round 1", "Jan 19", "Take-home", "Submitted", "React project"],
        ["Figma", "Round 2", "Jan 24", "Portfolio", "Preparing", "Case studies"],
        ["Vercel", "Round 1", "Jan 25", "System Design", "In Progress", "Architecture"],
        ["Netflix", "Screen", "Jan 18", "Phone", "Done", "Went well!"],
        ["Twilio", "Round 1", "Jan 21", "Tech Screen", "Preparing", "APIs focus"],
        ["Google", "Round 1", "Jan 28", "Coding", "Not Started", "LeetCode prep"],
        ["Apple", "Screen", "Jan 26", "Recruiter", "Scheduled", "Background Q"],
        ["Meta", "Round 1", "Jan 29", "Technical", "Not Started", "System design"],
        ["Spotify", "Screen", "Jan 23", "Phone", "Scheduled", "ML questions"],
        ["Databricks", "Round 1", "Jan 27", "Technical", "Preparing", "Data pipelines"],
        ["Palantir", "Round 2", "Jan 30", "Problem Solving", "In Progress", "FDE scenarios"],
        ["Coinbase", "Screen", "Feb 1", "Phone", "Scheduled", "Crypto basics"],
    ]

    prep_badges = {"Ready": BADGE_OFFER, "In Progress": BADGE_INTERVIEW,
                   "Submitted": TEAL, "Preparing": SOFT_ORANGE,
                   "Done": BADGE_OFFER, "Not Started": GRAY, "Scheduled": BADGE_APPLIED}
    ry2 = hy2
    for ri, row in enumerate(int_rows):
        bg = WHITE if ri % 2 == 0 else (255, 245, 245)
        badges = {4: prep_badges.get(row[4], GRAY)}
        ry2 = draw_spreadsheet_row(draw, sx2, ry2, sw2, row, int_ws, bg=bg,
                                    row_h=40, fsize=16, badges=badges)
        if ry2 > sy2 + sh2 - 5:
            break

    # ── Annotations ──
    draw_annotation(draw, 100, 750, ix1 + 30, iy1 + 400,
                    "20+ Applications", TEAL, 24)
    draw_annotation(draw, 100, 900, ix1 + 30, iy1 + 500,
                    "Follow-up Dates", DEEP_BLUE, 24)

    draw_annotation(draw, ix2 + iw2 + 50, 650, ix2 + iw2 - 30, iy2 + 150,
                    "Prep Status", CORAL, 24)
    draw_annotation(draw, ix2 + iw2 + 50, 800, ix2 + iw2 - 30, iy2 + 300,
                    "Interview Type", GOLD, 24)

    # Feature highlight boxes at bottom
    features = [
        ("Track Every Stage", "From applied to offer — see your pipeline at a glance"),
        ("Interview Scheduler", "Prep status, dates & round tracking all in one place"),
        ("Never Miss Follow-ups", "Built-in follow-up date reminders for every application"),
    ]
    box_w = 750
    box_h = 140
    box_gap = 40
    total_bw = len(features) * box_w + (len(features)-1) * box_gap
    bx_start = (W - total_bw) // 2
    by_start = H - 250

    for i, (feat_title, feat_desc) in enumerate(features):
        bx = bx_start + i * (box_w + box_gap)
        rounded_rect(draw, (bx, by_start, bx+box_w, by_start+box_h), 16, fill=WHITE)
        # accent bar
        accent_colors = [TEAL, CORAL, GOLD]
        draw.rectangle([bx, by_start, bx+8, by_start+box_h], fill=accent_colors[i])
        ft_f = font(24)
        draw.text((bx+24, by_start+18), feat_title, fill=DEEP_BLUE, font=ft_f)
        fd_f = font(18)
        draw.text((bx+24, by_start+55), feat_desc, fill=GRAY, font=fd_f)

    # Bottom bar
    draw_bottom_bar(draw, H-80, W, 80)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "03_applications_interviews.png"), "PNG")
    print("  [OK] 03_applications_interviews.png")


# ============================================================
# IMAGE 4: Networking + Salary Research
# ============================================================
def create_image_4():
    W, H = 2700, 2025
    img = Image.new("RGBA", (W, H))
    gradient_bg(img, (240, 248, 255), LIGHT_BLUE)
    draw = ImageDraw.Draw(img)

    # Decorative
    for cx, cy, r, c in [(2600, 100, 200, (*GOLD, 25)), (100, 1900, 180, (*TEAL, 20))]:
        for ri in range(r, 0, -2):
            alpha = int(c[3] * (ri / r))
            draw.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(*c[:3], alpha))

    # Title
    tf = font(66)
    title = "BUILD YOUR NETWORK & RESEARCH SALARIES"
    bbox = tf.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 50), title, fill=DEEP_BLUE, font=tf)

    stf = font(28)
    sub = "Strategic networking and salary data to negotiate with confidence"
    bbox_s = stf.getbbox(sub)
    stw = bbox_s[2] - bbox_s[0]
    draw.text(((W-stw)//2, 135), sub, fill=GRAY, font=stf)

    # ── iPad 1 (Left): Networking Tracker ──
    iw1, ih1 = 1200, 950
    ix1, iy1 = 80, 240
    sx1, sy1, sw1, sh1 = draw_ipad(img, ix1, iy1, iw1, ih1, bezel=20)
    draw = ImageDraw.Draw(img)

    draw.rectangle([sx1, sy1, sx1+sw1, sy1+30], fill=SOFT_GREEN)
    tab_f = font(15)
    draw.text((sx1+10, sy1+7), "◆ Networking Tracker", fill=WHITE, font=tab_f)

    net_cols = ["Contact", "Company", "Title", "Method", "Last Contact", "Status"]
    net_ws = [190, 160, 180, 130, 140, 130]
    remain = iw1 - sum(net_ws)
    net_ws[-1] += remain

    hy = draw_spreadsheet_header(draw, sx1, sy1+32, sw1, net_cols, net_ws,
                                  header_color=SOFT_GREEN, row_h=36, fsize=16)

    net_rows = [
        ["James Smith", "Google", "Eng Manager", "LinkedIn", "Jan 14", "Active"],
        ["Amy Chen", "Meta", "Sr. PM", "Coffee Chat", "Jan 12", "Active"],
        ["Raj Patel", "Stripe", "Staff Eng.", "Email", "Jan 10", "Warm"],
        ["Maria Jones", "Apple", "Designer", "Conf Event", "Jan 8", "Active"],
        ["Lisa Garcia", "Netflix", "Director", "Referral", "Jan 15", "Hot Lead"],
        ["Tom Wilson", "Airbnb", "Tech Lead", "Alumni Net", "Jan 7", "Warm"],
        ["Sarah Kim", "Shopify", "Recruiter", "Cold Email", "Jan 13", "Active"],
        ["David Brown", "Microsoft", "VP Eng", "LinkedIn", "Jan 9", "Cold"],
        ["Emily White", "Figma", "HR Lead", "Twitter/X", "Jan 11", "Warm"],
        ["Chris Lee", "Spotify", "ML Lead", "Meetup", "Jan 6", "Active"],
        ["Nina Taylor", "Slack", "PM Dir.", "Referral", "Jan 14", "Hot Lead"],
        ["Alex Morgan", "Notion", "CTO", "Intro Email", "Jan 8", "Warm"],
        ["Priya Nair", "Twilio", "Eng Dir.", "LinkedIn", "Jan 12", "Active"],
        ["Kevin Park", "Vercel", "Founder", "Conference", "Jan 5", "Cold"],
        ["Rachel Adams", "HubSpot", "VP Prod", "Alumni Net", "Jan 10", "Warm"],
        ["Mike Zhang", "Coinbase", "Staff Eng", "Twitter/X", "Jan 13", "Active"],
        ["Laura Kim", "Zoom", "Recruiter", "Job Fair", "Jan 9", "Active"],
        ["John Davis", "Canva", "Design Dir", "Portfolio", "Jan 11", "Hot Lead"],
        ["Samira Khan", "Square", "Tech Lead", "LinkedIn", "Jan 7", "Warm"],
        ["Ben Thomas", "Palantir", "Recruiter", "Cold Email", "Jan 14", "Active"],
    ]

    status_colors = {"Active": TEAL, "Warm": SOFT_ORANGE, "Hot Lead": BADGE_OFFER, "Cold": GRAY}
    ry = hy
    for ri, row in enumerate(net_rows):
        bg = WHITE if ri % 2 == 0 else ICE
        badges = {5: status_colors.get(row[5], GRAY)}
        ry = draw_spreadsheet_row(draw, sx1, ry, sw1, row, net_ws, bg=bg,
                                   row_h=42, fsize=15, badges=badges)
        if ry > sy1 + sh1 - 5:
            break

    # ── iPad 2 (Right): Salary Research ──
    iw2, ih2 = 1200, 950
    ix2, iy2 = 1420, 240
    sx2, sy2, sw2, sh2 = draw_ipad(img, ix2, iy2, iw2, ih2, bezel=20)
    draw = ImageDraw.Draw(img)

    draw.rectangle([sx2, sy2, sx2+sw2, sy2+30], fill=GOLD)
    draw.text((sx2+10, sy2+7), "◆ Salary Research", fill=WHITE, font=tab_f)

    sal_cols = ["Company", "Role", "Base", "Bonus", "Equity", "Total Comp"]
    sal_ws = [180, 180, 160, 140, 150, 160]
    remain2 = iw2 - sum(sal_ws)
    sal_ws[-1] += remain2

    hy2 = draw_spreadsheet_header(draw, sx2, sy2+32, sw2, sal_cols, sal_ws,
                                   header_color=GOLD, row_h=36, fsize=16)

    sal_rows = [
        ["Google", "Software Eng.", "$165K", "$30K", "$50K/yr", "$245K"],
        ["Amazon", "Product Mgr.", "$155K", "$25K", "$40K/yr", "$220K"],
        ["Stripe", "UX Designer", "$140K", "$20K", "$35K/yr", "$195K"],
        ["Netflix", "Sr. Engineer", "$200K", "$0", "$0", "$200K"],
        ["Meta", "Data Analyst", "$135K", "$25K", "$45K/yr", "$205K"],
        ["Apple", "iOS Developer", "$170K", "$20K", "$40K/yr", "$230K"],
        ["Microsoft", "PM Lead", "$175K", "$30K", "$50K/yr", "$255K"],
        ["Shopify", "Frontend Dev", "$130K", "$15K", "$20K/yr", "$165K"],
        ["Airbnb", "Backend Eng.", "$160K", "$25K", "$45K/yr", "$230K"],
        ["Figma", "Product Design", "$145K", "$20K", "$50K/yr", "$215K"],
        ["Spotify", "ML Engineer", "$170K", "$20K", "$35K/yr", "$225K"],
        ["Databricks", "Data Engineer", "$175K", "$30K", "$55K/yr", "$260K"],
        ["Coinbase", "Blockchain", "$180K", "$25K", "$60K/yr", "$265K"],
        ["Palantir", "FDE", "$160K", "$20K", "$40K/yr", "$220K"],
        ["Twilio", "API Eng.", "$135K", "$15K", "$25K/yr", "$175K"],
        ["HubSpot", "Growth PM", "$125K", "$15K", "$20K/yr", "$160K"],
        ["Canva", "UI Designer", "$120K", "$10K", "$15K/yr", "$145K"],
        ["Notion", "Full Stack", "$150K", "$20K", "$35K/yr", "$205K"],
        ["Vercel", "DevOps", "$140K", "$15K", "$30K/yr", "$185K"],
        ["Square", "Mobile Dev", "$155K", "$20K", "$35K/yr", "$210K"],
    ]

    ry2 = hy2
    for ri, row in enumerate(sal_rows):
        bg = WHITE if ri % 2 == 0 else PALE_GOLD
        ry2 = draw_spreadsheet_row(draw, sx2, ry2, sw2, row, sal_ws, bg=bg,
                                    row_h=42, fsize=15)
        if ry2 > sy2 + sh2 - 5:
            break

    # ── Annotations ──
    draw_annotation(draw, ix1 + iw1 + 50, 380, ix1 + iw1 - 50, iy1 + 200,
                    "Contact Status", SOFT_GREEN, 24)
    draw_annotation(draw, ix1 + iw1 + 50, 520, ix1 + iw1 - 50, iy1 + 350,
                    "Outreach Method", TEAL, 24)

    draw_annotation(draw, ix2 - 80, 400, ix2 + 50, iy2 + 200,
                    "Total Compensation", GOLD, 24)
    draw_annotation(draw, ix2 - 80, 550, ix2 + 50, iy2 + 350,
                    "Equity Breakdown", CORAL, 24)

    # Feature boxes at bottom
    features = [
        ("Relationship Tracking", "Manage contacts across LinkedIn, events, email & more"),
        ("Compensation Data", "Compare base, bonus, and equity across companies"),
        ("Negotiation Ready", "Know your market value before the offer conversation"),
    ]
    box_w = 750
    box_h = 130
    box_gap = 40
    total_bw = len(features) * box_w + (len(features)-1) * box_gap
    bx_start = (W - total_bw) // 2
    by_start = H - 240

    for i, (ft, fd) in enumerate(features):
        bx = bx_start + i * (box_w + box_gap)
        rounded_rect(draw, (bx, by_start, bx+box_w, by_start+box_h), 14, fill=WHITE)
        accent_colors = [SOFT_GREEN, GOLD, CORAL]
        draw.rectangle([bx, by_start, bx+8, by_start+box_h], fill=accent_colors[i])
        draw.text((bx+24, by_start+16), ft, fill=DEEP_BLUE, font=font(24))
        draw.text((bx+24, by_start+52), fd, fill=GRAY, font=font(17))

    draw_bottom_bar(draw, H-80, W, 80)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "04_networking_salary.png"), "PNG")
    print("  [OK] 04_networking_salary.png")


# ============================================================
# IMAGE 5: Value Proposition
# ============================================================
def create_image_5():
    W, H = 2700, 2025
    img = Image.new("RGBA", (W, H))
    gradient_bg(img, DARK_BG, DEEP_BLUE)
    draw = ImageDraw.Draw(img)

    # Radial glow in center
    cx_g, cy_g = W//2, H//2 - 50
    for r in range(600, 0, -2):
        alpha = int(30 * (r / 600))
        draw.ellipse([cx_g-r, cy_g-r, cx_g+r, cy_g+r], fill=(*TEAL, alpha))

    # Title
    tf = font(70)
    title = "YOUR COMPLETE JOB SEARCH COMMAND CENTER"
    bbox = tf.getbbox(title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 60), title, fill=WHITE, font=tf)

    stf = font(30)
    sub = "Everything you need to land your dream job in 2026"
    bbox_s = stf.getbbox(sub)
    stw = bbox_s[2] - bbox_s[0]
    draw.text(((W-stw)//2, 150), sub, fill=LIGHT_BLUE, font=stf)

    # Center iPad (slightly tilted effect via offset shadow)
    iw, ih = 1400, 800
    ix = (W - iw) // 2
    iy = 260
    # Extra dramatic shadow for tilt effect
    shadow_img = Image.new("RGBA", (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(shadow_img)
    for s in range(25, 0, -1):
        alpha = int(40 * (1 - s/25))
        rounded_rect(sd, (ix-20+s+8, iy-20+s+8, ix+iw+20+s+8, iy+ih+20+s+8),
                      30, fill=(0,0,0,alpha))
    img.paste(Image.alpha_composite(Image.new("RGBA", (W,H), (0,0,0,0)), shadow_img), (0,0), shadow_img)
    draw = ImageDraw.Draw(img)

    sx, sy, sw, sh = draw_ipad(img, ix, iy, iw, ih, bezel=22)
    draw = ImageDraw.Draw(img)

    # Tab bar
    tabs = ["Applications", "Resume", "Interviews", "Network", "Salary", "Skills", "Weekly", "Guide"]
    tw_each = sw // len(tabs)
    for ti, tab in enumerate(tabs):
        tx = sx + ti * tw_each
        bg = TEAL if ti == 0 else MID_BLUE
        draw.rectangle([tx, sy, tx+tw_each, sy+28], fill=bg)
        ttf = font(13)
        bbox_t = ttf.getbbox(tab)
        ttw = bbox_t[2] - bbox_t[0]
        draw.text((tx + (tw_each-ttw)//2, sy+7), tab, fill=WHITE, font=ttf)

    # Show Application Tracker mini content
    mini_cols = ["Company", "Position", "Status", "Follow-up", "Salary", "Contact"]
    mini_ws = [210, 250, 160, 160, 190, 170]
    remain = iw - sum(mini_ws)
    mini_ws[-1] += remain
    hy = draw_spreadsheet_header(draw, sx, sy+30, sw, mini_cols, mini_ws, row_h=34, fsize=16)

    mini_rows = [
        ["Google", "Software Engineer", "Applied", "Jan 22", "$150-180K", "recruiter@goog"],
        ["Amazon", "Product Manager", "Interview", "Jan 18", "$140-170K", "hr@amazon.com"],
        ["Stripe", "UX Designer", "Offer", "—", "$130-155K", "talent@stripe"],
        ["Meta", "Data Analyst", "Applied", "Jan 20", "$125-150K", "jobs@meta.com"],
        ["Netflix", "Sr. Engineer", "Phone Screen", "Jan 16", "$180-220K", "hire@netflix"],
        ["Apple", "iOS Developer", "Applied", "Jan 21", "$155-185K", "recruit@apple"],
        ["Microsoft", "PM Lead", "Rejected", "—", "$160-190K", "msft@hr.com"],
        ["Shopify", "Frontend Dev", "Interview", "Jan 19", "$120-145K", "jobs@shopify"],
        ["Airbnb", "Backend Eng.", "Applied", "Jan 13", "$145-175K", "talent@airbnb"],
        ["Figma", "Product Design", "Interview", "Jan 20", "$135-160K", "hr@figma.com"],
        ["Spotify", "ML Engineer", "Applied", "Jan 16", "$155-190K", "jobs@spotify"],
        ["Databricks", "Data Engineer", "Applied", "Jan 17", "$160-195K", "hr@databricks"],
        ["Coinbase", "Blockchain Dev", "Applied", "Jan 22", "$165-200K", "jobs@coinbase"],
        ["Notion", "Full Stack", "Applied", "Jan 21", "$140-165K", "work@notion"],
        ["Vercel", "DevOps Eng.", "Interview", "Jan 19", "$130-155K", "team@vercel"],
        ["Palantir", "FDE", "Phone Screen", "Jan 16", "$150-185K", "hire@palantir"],
    ]

    badge_map = {"Applied": BADGE_APPLIED, "Interview": BADGE_INTERVIEW,
                 "Offer": BADGE_OFFER, "Rejected": BADGE_REJECTED, "Phone Screen": SOFT_ORANGE}

    ry = hy
    for ri, row in enumerate(mini_rows):
        bg = WHITE if ri % 2 == 0 else ICE
        badges = {2: badge_map.get(row[2], GRAY)}
        ry = draw_spreadsheet_row(draw, sx, ry, sw, row, mini_ws, bg=bg,
                                   row_h=38, fsize=15, badges=badges)
        if ry > sy + sh - 5:
            break

    # ── Floating feature badges ──
    badge_data = [
        (200, 350, "8 Tabs", TEAL),
        (200, 480, "100+ Applications", MID_BLUE),
        (200, 610, "Interview Prep", CORAL),
        (200, 740, "Salary Data", GOLD),
        (2500, 350, "Resume Versions", TEAL),
        (2500, 480, "Skills Tracker", MID_BLUE),
        (2500, 610, "Weekly Planner", SOFT_GREEN),
        (2500, 740, "How-to Guide", SOFT_ORANGE),
    ]

    for bx, by, btext, bcolor in badge_data:
        bf = font(24)
        bbox_b = bf.getbbox(btext)
        btw = bbox_b[2] - bbox_b[0]
        bth = bbox_b[3] - bbox_b[1]
        pad_x, pad_y = 24, 14
        x0 = bx - btw//2 - pad_x
        y0 = by - bth//2 - pad_y
        x1 = bx + btw//2 + pad_x
        y1 = by + bth//2 + pad_y
        # Glow
        for g in range(8, 0, -1):
            alpha = int(20 * (1 - g/8))
            rounded_rect(draw, (x0-g, y0-g, x1+g, y1+g), (y1-y0)//2+g, fill=(*bcolor, alpha))
        rounded_rect(draw, (x0, y0, x1, y1), (y1-y0)//2, fill=bcolor)
        draw.text((bx - btw//2, by - bth//2 - 2), btext, fill=WHITE, font=bf)

    # ── Price badge ──
    price_y = iy + ih + 100
    pf = font(52)
    price = "$8.99  INSTANT DOWNLOAD"
    bbox_p = pf.getbbox(price)
    pw = bbox_p[2] - bbox_p[0]
    ph = bbox_p[3] - bbox_p[1]
    px = (W - pw) // 2 - 30
    py = price_y
    rounded_rect(draw, (px - 30, py - 16, px + pw + 30, py + ph + 20), 20, fill=CORAL)
    draw.text((px, py - 6), price, fill=WHITE, font=pf)

    # ── Stars ──
    star_y = price_y + ph + 55
    sf = font(38)
    stars_text = "★ ★ ★ ★ ★"
    bbox_st = sf.getbbox(stars_text)
    stw = bbox_st[2] - bbox_st[0]
    draw.text(((W-stw)//2, star_y), stars_text, fill=GOLD, font=sf)

    review_f = font(24)
    review = "Join 10,000+ job seekers who landed their dream role"
    bbox_r = review_f.getbbox(review)
    rw = bbox_r[2] - bbox_r[0]
    draw.text(((W-rw)//2, star_y + 55), review, fill=LIGHT_BLUE, font=review_f)

    # Guarantee badges
    guarantees = ["✓ Lifetime Access", "✓ Google Sheets + Excel", "✓ Free Updates", "✓ Instant Download"]
    gf = font(22)
    g_total = 0
    g_sizes = []
    for g in guarantees:
        bbox_g = gf.getbbox(g)
        gw = bbox_g[2] - bbox_g[0] + 40
        g_sizes.append(gw)
        g_total += gw + 30
    gx = (W - g_total) // 2
    gy = star_y + 120
    for i, g in enumerate(guarantees):
        bbox_g = gf.getbbox(g)
        gw = bbox_g[2] - bbox_g[0]
        draw.text((gx + 20, gy), g, fill=SOFT_GREEN, font=gf)
        gx += g_sizes[i] + 30

    # Bottom bar
    draw.rectangle([0, H-80, W, H], fill=(10, 20, 40))
    bbf = font(22)
    bbt = "Resume & Job Search Tracker Bundle 2026  ·  Instant Digital Download  ·  Works on Any Device"
    bbox_bb = bbf.getbbox(bbt)
    bbw = bbox_bb[2] - bbox_bb[0]
    draw.text(((W-bbw)//2, H-56), bbt, fill=LIGHT_BLUE, font=bbf)

    img = img.convert("RGB")
    img.save(os.path.join(OUT, "05_value_proposition.png"), "PNG")
    print("  [OK] 05_value_proposition.png")


# ── Run all ──
if __name__ == "__main__":
    print("Generating listing images...")
    create_image_1()
    create_image_2()
    create_image_3()
    create_image_4()
    create_image_5()
    print("All 5 images generated successfully!")
