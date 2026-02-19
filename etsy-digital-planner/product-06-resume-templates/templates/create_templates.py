#!/usr/bin/env python3
"""Generate 10 unique professional resume template designs as PNG images."""

from PIL import Image, ImageDraw, ImageFont
import os

# --- Constants ---
W, H = 2550, 3300  # 8.5x11 at 300dpi
MARGIN = 200
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color palette
NAVY = (27, 42, 74)
SLATE = (74, 111, 165)
LIGHT_GRAY = (240, 242, 245)
WHITE = (255, 255, 255)
GOLD = (201, 169, 110)
CHARCOAL = (51, 51, 51)
DARK_GRAY = (100, 100, 100)
MED_GRAY = (170, 170, 170)
VERY_LIGHT = (245, 247, 250)

# Placeholder text
NAME = "[YOUR NAME]"
CONTACT = "[email] | [phone] | [city, state] | [linkedin]"
SUMMARY = (
    "Results-driven professional with 8+ years of experience in strategic planning, "
    "project management, and team leadership. Proven track record of delivering "
    "high-impact solutions that drive revenue growth and operational efficiency."
)
JOBS = [
    {
        "company": "[Company Name]",
        "title": "[Job Title]",
        "dates": "[Start Date] - [End Date]",
        "bullets": [
            "Led cross-functional team of 12 to deliver $2M project ahead of schedule",
            "Implemented new processes that improved efficiency by 35%",
            "Managed client relationships resulting in 95% retention rate",
        ],
    },
    {
        "company": "[Company Name]",
        "title": "[Job Title]",
        "dates": "[Start Date] - [End Date]",
        "bullets": [
            "Developed strategic initiatives that increased revenue by 28%",
            "Coordinated with stakeholders to align business objectives",
            "Mentored junior team members and improved team productivity",
        ],
    },
    {
        "company": "[Company Name]",
        "title": "[Job Title]",
        "dates": "[Start Date] - [End Date]",
        "bullets": [
            "Streamlined operations reducing costs by $500K annually",
            "Built and maintained key partnerships with industry leaders",
        ],
    },
]
EDUCATION = [
    {"degree": "Master of Business Administration", "school": "[University Name]", "year": "[Year]"},
    {"degree": "Bachelor of Science in [Field]", "school": "[University Name]", "year": "[Year]"},
]
SKILLS = [
    "Project Management",
    "Strategic Planning",
    "Data Analysis",
    "Team Leadership",
    "Communication",
    "Problem Solving",
    "Budget Management",
    "Agile / Scrum",
]
SKILL_LEVELS = [90, 85, 80, 95, 88, 82, 75, 70]
CERTIFICATIONS = ["PMP Certified", "Six Sigma Green Belt", "Google Analytics Certified"]
LANGUAGES = [("English", "Native"), ("Spanish", "Professional"), ("French", "Conversational")]


def get_font(size, bold=False):
    """Get a font, falling back gracefully."""
    paths = []
    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_serif_font(size, bold=False):
    """Get a serif font."""
    paths = []
    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size, bold)


def get_mono_font(size, bold=False):
    """Get a monospace font."""
    paths = []
    if bold:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size, bold)


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def text_height(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def wrap_text(draw, text, font, max_width):
    """Wrap text to fit within max_width, return list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if text_width(draw, test, font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_skill_bar(draw, x, y, w, h, level, fill_color, bg_color=MED_GRAY):
    """Draw a skill progress bar."""
    draw.rectangle([x, y, x + w, y + h], fill=bg_color)
    filled_w = int(w * level / 100)
    if filled_w > 0:
        draw.rectangle([x, y, x + filled_w, y + h], fill=fill_color)


def draw_skill_dots(draw, x, y, level, dot_color, empty_color=MED_GRAY, count=5, r=10, spacing=28):
    """Draw skill level as dots."""
    filled = int(round(level / 100 * count))
    for i in range(count):
        cx = x + i * spacing
        color = dot_color if i < filled else empty_color
        draw.ellipse([cx - r, y - r, cx + r, y + r], fill=color)


# ============================================================
# Template 1: Classic
# ============================================================
def create_classic():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = MARGIN
    y = m

    # Name
    name_font = get_serif_font(96, bold=True)
    nw = text_width(draw, NAME, name_font)
    draw.text(((W - nw) // 2, y), NAME, fill=NAVY, font=name_font)
    y += 130

    # Contact
    contact_font = get_font(36)
    cw = text_width(draw, CONTACT, contact_font)
    draw.text(((W - cw) // 2, y), CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 70

    # Divider
    draw.line([(m, y), (W - m, y)], fill=NAVY, width=3)
    y += 40

    section_font = get_serif_font(54, bold=True)
    body_font = get_font(34)
    bold_font = get_font(34, bold=True)
    small_font = get_font(30)
    content_w = W - 2 * m

    # Summary
    draw.text((m, y), "PROFESSIONAL SUMMARY", fill=NAVY, font=section_font)
    y += 75
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=2)
    y += 20
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        draw.text((m, y), line, fill=CHARCOAL, font=body_font)
        y += 48
    y += 30

    # Work Experience
    draw.text((m, y), "WORK EXPERIENCE", fill=NAVY, font=section_font)
    y += 75
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=2)
    y += 20
    for job in JOBS:
        draw.text((m, y), job["title"], fill=CHARCOAL, font=bold_font)
        dates_w = text_width(draw, job["dates"], small_font)
        draw.text((W - m - dates_w, y + 4), job["dates"], fill=DARK_GRAY, font=small_font)
        y += 48
        draw.text((m, y), job["company"], fill=SLATE, font=small_font)
        y += 44
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 60)):
                prefix = "\u2022  " if i == 0 else "   "
                draw.text((m + 30, y), prefix + bl, fill=CHARCOAL, font=body_font)
                y += 44
        y += 20
    y += 10

    # Education
    draw.text((m, y), "EDUCATION", fill=NAVY, font=section_font)
    y += 75
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=2)
    y += 20
    for edu in EDUCATION:
        draw.text((m, y), edu["degree"], fill=CHARCOAL, font=bold_font)
        yr_w = text_width(draw, edu["year"], small_font)
        draw.text((W - m - yr_w, y + 4), edu["year"], fill=DARK_GRAY, font=small_font)
        y += 48
        draw.text((m, y), edu["school"], fill=SLATE, font=small_font)
        y += 50
    y += 20

    # Skills
    draw.text((m, y), "SKILLS", fill=NAVY, font=section_font)
    y += 75
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=2)
    y += 20
    col_w = content_w // 2
    for i, skill in enumerate(SKILLS):
        col = i % 2
        row = i // 2
        sx = m + col * col_w
        sy = y + row * 48
        draw.text((sx, sy), "\u2022  " + skill, fill=CHARCOAL, font=body_font)
    y += (len(SKILLS) // 2 + 1) * 48

    img.save(os.path.join(OUTPUT_DIR, "resume_01_classic.png"), "PNG", dpi=(300, 300))
    print("  Created resume_01_classic.png")


# ============================================================
# Template 2: Modern (two-column with colored sidebar)
# ============================================================
def create_modern():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    sidebar_w = 850
    # Sidebar background
    draw.rectangle([0, 0, sidebar_w, H], fill=NAVY)

    # --- Sidebar content ---
    sx = 80
    sy = 200
    sw = sidebar_w - 160

    # Name on sidebar
    name_font = get_font(72, bold=True)
    for line in wrap_text(draw, NAME, name_font, sw):
        draw.text((sx, sy), line, fill=WHITE, font=name_font)
        sy += 90
    sy += 10

    # Contact
    contact_font = get_font(30)
    for item in ["[email]", "[phone]", "[city, state]", "[linkedin]"]:
        draw.text((sx, sy), item, fill=GOLD, font=contact_font)
        sy += 44
    sy += 40

    # Sidebar divider
    draw.line([(sx, sy), (sx + sw, sy)], fill=GOLD, width=2)
    sy += 30

    # Skills section in sidebar
    section_font = get_font(42, bold=True)
    body_font = get_font(30)
    draw.text((sx, sy), "SKILLS", fill=GOLD, font=section_font)
    sy += 60
    for i, skill in enumerate(SKILLS):
        draw.text((sx, sy), skill, fill=WHITE, font=body_font)
        sy += 40
        draw_skill_bar(draw, sx, sy, sw, 12, SKILL_LEVELS[i], GOLD, (60, 80, 120))
        sy += 32
    sy += 30

    # Languages
    draw.line([(sx, sy), (sx + sw, sy)], fill=GOLD, width=2)
    sy += 30
    draw.text((sx, sy), "LANGUAGES", fill=GOLD, font=section_font)
    sy += 60
    for lang, level in LANGUAGES:
        draw.text((sx, sy), f"{lang} - {level}", fill=WHITE, font=body_font)
        sy += 44
    sy += 30

    # Certifications
    draw.line([(sx, sy), (sx + sw, sy)], fill=GOLD, width=2)
    sy += 30
    draw.text((sx, sy), "CERTIFICATIONS", fill=GOLD, font=section_font)
    sy += 60
    for cert in CERTIFICATIONS:
        draw.text((sx, sy), "\u2022 " + cert, fill=WHITE, font=body_font)
        sy += 44

    # --- Main content ---
    mx = sidebar_w + 100
    my = 200
    mw = W - mx - MARGIN
    main_section = get_font(48, bold=True)
    main_body = get_font(32)
    main_bold = get_font(32, bold=True)
    main_small = get_font(28)

    # Summary
    draw.text((mx, my), "PROFESSIONAL SUMMARY", fill=NAVY, font=main_section)
    my += 65
    draw.line([(mx, my), (mx + mw, my)], fill=SLATE, width=2)
    my += 20
    for line in wrap_text(draw, SUMMARY, main_body, mw):
        draw.text((mx, my), line, fill=CHARCOAL, font=main_body)
        my += 44
    my += 35

    # Experience
    draw.text((mx, my), "WORK EXPERIENCE", fill=NAVY, font=main_section)
    my += 65
    draw.line([(mx, my), (mx + mw, my)], fill=SLATE, width=2)
    my += 20
    for job in JOBS:
        draw.text((mx, my), job["title"], fill=CHARCOAL, font=main_bold)
        my += 44
        draw.text((mx, my), f"{job['company']}  |  {job['dates']}", fill=SLATE, font=main_small)
        my += 44
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, main_body, mw - 50)):
                prefix = "\u2022  " if i == 0 else "   "
                draw.text((mx + 20, my), prefix + bl, fill=CHARCOAL, font=main_body)
                my += 42
        my += 20
    my += 15

    # Education
    draw.text((mx, my), "EDUCATION", fill=NAVY, font=main_section)
    my += 65
    draw.line([(mx, my), (mx + mw, my)], fill=SLATE, width=2)
    my += 20
    for edu in EDUCATION:
        draw.text((mx, my), edu["degree"], fill=CHARCOAL, font=main_bold)
        my += 44
        draw.text((mx, my), f"{edu['school']}  |  {edu['year']}", fill=SLATE, font=main_small)
        my += 50

    img.save(os.path.join(OUTPUT_DIR, "resume_02_modern.png"), "PNG", dpi=(300, 300))
    print("  Created resume_02_modern.png")


# ============================================================
# Template 3: Creative (bold header with accent color blocks)
# ============================================================
def create_creative():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = MARGIN

    # Bold header block
    header_h = 500
    draw.rectangle([0, 0, W, header_h], fill=NAVY)
    # Accent strip
    draw.rectangle([0, header_h, W, header_h + 20], fill=GOLD)

    # Name in header
    name_font = get_font(110, bold=True)
    nw = text_width(draw, NAME, name_font)
    draw.text(((W - nw) // 2, 120), NAME, fill=WHITE, font=name_font)

    # Title placeholder
    title_font = get_font(44)
    title_text = "[Professional Title]"
    tw = text_width(draw, title_text, title_font)
    draw.text(((W - tw) // 2, 260), title_text, fill=GOLD, font=title_font)

    # Contact in header
    contact_font = get_font(32)
    cw = text_width(draw, CONTACT, contact_font)
    draw.text(((W - cw) // 2, 340), CONTACT, fill=LIGHT_GRAY, font=contact_font)

    y = header_h + 60
    section_font = get_font(48, bold=True)
    body_font = get_font(32)
    bold_font = get_font(32, bold=True)
    small_font = get_font(28)
    content_w = W - 2 * m

    # Summary with accent block
    draw.rectangle([m, y, m + 8, y + 55], fill=GOLD)
    draw.text((m + 30, y), "PROFESSIONAL SUMMARY", fill=NAVY, font=section_font)
    y += 70
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        draw.text((m, y), line, fill=CHARCOAL, font=body_font)
        y += 44
    y += 35

    # Experience with accent block
    draw.rectangle([m, y, m + 8, y + 55], fill=GOLD)
    draw.text((m + 30, y), "EXPERIENCE", fill=NAVY, font=section_font)
    y += 70
    for job in JOBS:
        # Color block for job
        draw.rectangle([m, y, m + 4, y + 120], fill=SLATE)
        draw.text((m + 25, y), job["title"], fill=CHARCOAL, font=bold_font)
        y += 42
        draw.text((m + 25, y), f"{job['company']}  |  {job['dates']}", fill=SLATE, font=small_font)
        y += 44
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 60)):
                prefix = "\u2022 " if i == 0 else "  "
                draw.text((m + 40, y), prefix + bl, fill=CHARCOAL, font=body_font)
                y += 42
        y += 20
    y += 15

    # Two column bottom: Education + Skills
    col_w = (content_w - 80) // 2

    # Education
    draw.rectangle([m, y, m + 8, y + 55], fill=GOLD)
    draw.text((m + 30, y), "EDUCATION", fill=NAVY, font=section_font)
    ey = y + 70
    for edu in EDUCATION:
        draw.text((m, ey), edu["degree"], fill=CHARCOAL, font=bold_font)
        ey += 40
        draw.text((m, ey), f"{edu['school']} | {edu['year']}", fill=SLATE, font=small_font)
        ey += 50

    # Skills
    skills_x = m + col_w + 80
    draw.rectangle([skills_x, y, skills_x + 8, y + 55], fill=GOLD)
    draw.text((skills_x + 30, y), "SKILLS", fill=NAVY, font=section_font)
    sky = y + 70
    for i, skill in enumerate(SKILLS):
        draw.text((skills_x, sky), skill, fill=CHARCOAL, font=body_font)
        sky += 38
        draw_skill_bar(draw, skills_x, sky, col_w - 40, 10, SKILL_LEVELS[i], SLATE, LIGHT_GRAY)
        sky += 28

    img.save(os.path.join(OUTPUT_DIR, "resume_03_creative.png"), "PNG", dpi=(300, 300))
    print("  Created resume_03_creative.png")


# ============================================================
# Template 4: Minimalist
# ============================================================
def create_minimalist():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = 300  # Extra margins for whitespace
    y = 350

    name_font = get_font(80, bold=True)
    nw = text_width(draw, NAME, name_font)
    draw.text(((W - nw) // 2, y), NAME, fill=CHARCOAL, font=name_font)
    y += 120

    contact_font = get_font(30)
    cw = text_width(draw, CONTACT, contact_font)
    draw.text(((W - cw) // 2, y), CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 80

    # Thin line
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 60

    section_font = get_font(36, bold=True)
    body_font = get_font(30)
    bold_font = get_font(30, bold=True)
    small_font = get_font(26)
    content_w = W - 2 * m

    # Summary
    draw.text((m, y), "SUMMARY", fill=CHARCOAL, font=section_font)
    y += 55
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        draw.text((m, y), line, fill=DARK_GRAY, font=body_font)
        y += 42
    y += 50
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 40

    # Experience
    draw.text((m, y), "EXPERIENCE", fill=CHARCOAL, font=section_font)
    y += 55
    for job in JOBS[:2]:  # Only 2 for minimalist spacing
        draw.text((m, y), f"{job['title']}  \u2014  {job['company']}", fill=CHARCOAL, font=bold_font)
        y += 42
        draw.text((m, y), job["dates"], fill=DARK_GRAY, font=small_font)
        y += 40
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 40)):
                prefix = "\u2013 " if i == 0 else "  "
                draw.text((m + 20, y), prefix + bl, fill=DARK_GRAY, font=body_font)
                y += 40
        y += 30
    y += 30
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 40

    # Education
    draw.text((m, y), "EDUCATION", fill=CHARCOAL, font=section_font)
    y += 55
    for edu in EDUCATION:
        draw.text((m, y), edu["degree"], fill=CHARCOAL, font=bold_font)
        y += 40
        draw.text((m, y), f"{edu['school']}  \u2014  {edu['year']}", fill=DARK_GRAY, font=small_font)
        y += 50
    y += 30
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 40

    # Skills - simple comma list
    draw.text((m, y), "SKILLS", fill=CHARCOAL, font=section_font)
    y += 55
    skills_text = "  \u2022  ".join(SKILLS)
    for line in wrap_text(draw, skills_text, body_font, content_w):
        draw.text((m, y), line, fill=DARK_GRAY, font=body_font)
        y += 42

    img.save(os.path.join(OUTPUT_DIR, "resume_04_minimalist.png"), "PNG", dpi=(300, 300))
    print("  Created resume_04_minimalist.png")


# ============================================================
# Template 5: Executive (dark header bar, gold accents)
# ============================================================
def create_executive():
    img = Image.new("RGB", (W, H), VERY_LIGHT)
    draw = ImageDraw.Draw(img)
    m = MARGIN

    # Dark header
    header_h = 420
    draw.rectangle([0, 0, W, header_h], fill=NAVY)
    draw.rectangle([0, header_h, W, header_h + 8], fill=GOLD)

    # Name
    name_font = get_font(90, bold=True)
    nw = text_width(draw, NAME, name_font)
    draw.text(((W - nw) // 2, 100), NAME, fill=WHITE, font=name_font)

    # Title
    title_font = get_font(40)
    title_text = "SENIOR EXECUTIVE  |  [PROFESSIONAL TITLE]"
    tw = text_width(draw, title_text, title_font)
    draw.text(((W - tw) // 2, 220), title_text, fill=GOLD, font=title_font)

    # Contact
    contact_font = get_font(30)
    cw = text_width(draw, CONTACT, contact_font)
    draw.text(((W - cw) // 2, 300), CONTACT, fill=LIGHT_GRAY, font=contact_font)

    y = header_h + 60
    section_font = get_font(46, bold=True)
    body_font = get_font(32)
    bold_font = get_font(32, bold=True)
    small_font = get_font(28)
    content_w = W - 2 * m

    # Summary
    draw.text((m, y), "\u25C6  EXECUTIVE SUMMARY", fill=NAVY, font=section_font)
    y += 65
    draw.line([(m, y), (W - m, y)], fill=GOLD, width=3)
    y += 20
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        draw.text((m, y), line, fill=CHARCOAL, font=body_font)
        y += 44
    y += 30

    # Experience
    draw.text((m, y), "\u25C6  PROFESSIONAL EXPERIENCE", fill=NAVY, font=section_font)
    y += 65
    draw.line([(m, y), (W - m, y)], fill=GOLD, width=3)
    y += 20
    for job in JOBS:
        draw.text((m, y), job["title"].upper(), fill=NAVY, font=bold_font)
        dates_w = text_width(draw, job["dates"], small_font)
        draw.text((W - m - dates_w, y + 4), job["dates"], fill=DARK_GRAY, font=small_font)
        y += 44
        draw.text((m, y), job["company"], fill=GOLD, font=small_font)
        y += 42
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 60)):
                prefix = "\u25B8 " if i == 0 else "  "
                draw.text((m + 25, y), prefix + bl, fill=CHARCOAL, font=body_font)
                y += 42
        y += 18
    y += 15

    # Two columns: Education + Skills
    col_w = (content_w - 80) // 2

    draw.text((m, y), "\u25C6  EDUCATION", fill=NAVY, font=section_font)
    draw.text((m + col_w + 80, y), "\u25C6  CORE COMPETENCIES", fill=NAVY, font=section_font)
    y += 65
    draw.line([(m, y), (m + col_w, y)], fill=GOLD, width=3)
    draw.line([(m + col_w + 80, y), (W - m, y)], fill=GOLD, width=3)
    y += 20

    ey = y
    for edu in EDUCATION:
        draw.text((m, ey), edu["degree"], fill=CHARCOAL, font=bold_font)
        ey += 40
        draw.text((m, ey), f"{edu['school']} | {edu['year']}", fill=DARK_GRAY, font=small_font)
        ey += 50

    sky = y
    skills_x = m + col_w + 80
    for skill in SKILLS:
        draw.text((skills_x, sky), "\u25B8 " + skill, fill=CHARCOAL, font=body_font)
        sky += 44

    img.save(os.path.join(OUTPUT_DIR, "resume_05_executive.png"), "PNG", dpi=(300, 300))
    print("  Created resume_05_executive.png")


# ============================================================
# Template 6: Tech (monospace-inspired, grid layout)
# ============================================================
def create_tech():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = MARGIN

    # Grid-like header
    draw.rectangle([0, 0, W, 60], fill=SLATE)
    draw.rectangle([0, 60, W, 64], fill=GOLD)

    y = 120
    name_font = get_mono_font(80, bold=True)
    draw.text((m, y), "$ " + NAME, fill=NAVY, font=name_font)
    y += 110

    contact_font = get_mono_font(28)
    draw.text((m, y), "> " + CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 60

    # Grid line
    draw.rectangle([m, y, W - m, y + 4], fill=SLATE)
    y += 30

    section_font = get_mono_font(40, bold=True)
    body_font = get_mono_font(28)
    bold_font = get_mono_font(28, bold=True)
    small_font = get_mono_font(24)
    content_w = W - 2 * m

    # Two column layout
    col_w = (content_w - 60) // 2
    left_x = m
    right_x = m + col_w + 60

    # Left column
    ly = y
    draw.text((left_x, ly), "## SUMMARY", fill=SLATE, font=section_font)
    ly += 55
    for line in wrap_text(draw, SUMMARY, body_font, col_w):
        draw.text((left_x, ly), line, fill=CHARCOAL, font=body_font)
        ly += 38
    ly += 25

    draw.text((left_x, ly), "## EXPERIENCE", fill=SLATE, font=section_font)
    ly += 55
    for job in JOBS:
        draw.text((left_x, ly), f"[{job['title']}]", fill=NAVY, font=bold_font)
        ly += 38
        draw.text((left_x, ly), f"  @ {job['company']} | {job['dates']}", fill=DARK_GRAY, font=small_font)
        ly += 36
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, col_w - 60)):
                prefix = "- " if i == 0 else "  "
                draw.text((left_x + 20, ly), prefix + bl, fill=CHARCOAL, font=body_font)
                ly += 36
        ly += 15

    # Right column
    ry = y
    draw.text((right_x, ry), "## SKILLS", fill=SLATE, font=section_font)
    ry += 55
    for i, skill in enumerate(SKILLS):
        draw.text((right_x, ry), skill, fill=CHARCOAL, font=body_font)
        ry += 34
        # ASCII-style progress bar
        filled = int(SKILL_LEVELS[i] / 100 * 20)
        bar = "[" + "\u2588" * filled + "\u2591" * (20 - filled) + "]"
        draw.text((right_x, ry), bar, fill=SLATE, font=small_font)
        ry += 36
    ry += 25

    draw.text((right_x, ry), "## EDUCATION", fill=SLATE, font=section_font)
    ry += 55
    for edu in EDUCATION:
        draw.text((right_x, ry), edu["degree"], fill=NAVY, font=bold_font)
        ry += 36
        draw.text((right_x, ry), f"  {edu['school']}", fill=DARK_GRAY, font=small_font)
        ry += 32
        draw.text((right_x, ry), f"  {edu['year']}", fill=DARK_GRAY, font=small_font)
        ry += 45
    ry += 25

    draw.text((right_x, ry), "## CERTIFICATIONS", fill=SLATE, font=section_font)
    ry += 55
    for cert in CERTIFICATIONS:
        draw.text((right_x, ry), f"> {cert}", fill=CHARCOAL, font=body_font)
        ry += 40
    ry += 25

    draw.text((right_x, ry), "## LANGUAGES", fill=SLATE, font=section_font)
    ry += 55
    for lang, level in LANGUAGES:
        draw.text((right_x, ry), f"{lang}: {level}", fill=CHARCOAL, font=body_font)
        ry += 40

    # Bottom grid line
    bottom_y = max(ly, ry) + 30
    draw.rectangle([m, bottom_y, W - m, bottom_y + 4], fill=SLATE)
    draw.rectangle([0, H - 60, W, H], fill=SLATE)

    img.save(os.path.join(OUTPUT_DIR, "resume_06_tech.png"), "PNG", dpi=(300, 300))
    print("  Created resume_06_tech.png")


# ============================================================
# Template 7: Elegant (script-style name, thin borders)
# ============================================================
def create_elegant():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = MARGIN

    # Thin border
    border = 40
    draw.rectangle([border, border, W - border, H - border], outline=NAVY, width=2)
    draw.rectangle([border + 15, border + 15, W - border - 15, H - border - 15], outline=GOLD, width=1)

    y = 200

    # Elegant name (using serif as script substitute)
    name_font = get_serif_font(100, bold=True)
    nw = text_width(draw, NAME, name_font)
    draw.text(((W - nw) // 2, y), NAME, fill=NAVY, font=name_font)
    y += 140

    # Decorative line with diamond
    mid = W // 2
    draw.line([(m + 100, y), (mid - 40, y)], fill=GOLD, width=1)
    draw.polygon([(mid, y - 8), (mid + 8, y), (mid, y + 8), (mid - 8, y)], fill=GOLD)
    draw.line([(mid + 40, y), (W - m - 100, y)], fill=GOLD, width=1)
    y += 30

    # Contact centered
    contact_font = get_font(30)
    cw = text_width(draw, CONTACT, contact_font)
    draw.text(((W - cw) // 2, y), CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 80

    section_font = get_serif_font(44, bold=True)
    body_font = get_serif_font(32)
    bold_font = get_serif_font(32, bold=True)
    small_font = get_serif_font(28)
    content_w = W - 2 * m - 100

    # Summary
    section_text = "Professional Summary"
    sw_text = text_width(draw, section_text, section_font)
    draw.text(((W - sw_text) // 2, y), section_text, fill=NAVY, font=section_font)
    y += 60
    # Small decorative line under section
    draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=GOLD, width=1)
    y += 20
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        lw = text_width(draw, line, body_font)
        draw.text(((W - lw) // 2, y), line, fill=CHARCOAL, font=body_font)
        y += 44
    y += 35

    # Experience
    section_text = "Professional Experience"
    sw_text = text_width(draw, section_text, section_font)
    draw.text(((W - sw_text) // 2, y), section_text, fill=NAVY, font=section_font)
    y += 60
    draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=GOLD, width=1)
    y += 20
    for job in JOBS[:2]:
        draw.text((m + 80, y), job["title"], fill=CHARCOAL, font=bold_font)
        dates_w = text_width(draw, job["dates"], small_font)
        draw.text((W - m - 80 - dates_w, y + 4), job["dates"], fill=DARK_GRAY, font=small_font)
        y += 44
        draw.text((m + 80, y), job["company"], fill=SLATE, font=small_font)
        y += 42
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 40)):
                prefix = "\u2022 " if i == 0 else "  "
                draw.text((m + 100, y), prefix + bl, fill=CHARCOAL, font=body_font)
                y += 42
        y += 18
    y += 20

    # Education
    section_text = "Education"
    sw_text = text_width(draw, section_text, section_font)
    draw.text(((W - sw_text) // 2, y), section_text, fill=NAVY, font=section_font)
    y += 60
    draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=GOLD, width=1)
    y += 20
    for edu in EDUCATION:
        text_line = f"{edu['degree']}  |  {edu['school']}  |  {edu['year']}"
        lw = text_width(draw, text_line, body_font)
        draw.text(((W - lw) // 2, y), text_line, fill=CHARCOAL, font=body_font)
        y += 50
    y += 20

    # Skills
    section_text = "Skills & Expertise"
    sw_text = text_width(draw, section_text, section_font)
    draw.text(((W - sw_text) // 2, y), section_text, fill=NAVY, font=section_font)
    y += 60
    draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=GOLD, width=1)
    y += 20
    skills_text = "  |  ".join(SKILLS)
    for line in wrap_text(draw, skills_text, body_font, content_w):
        lw = text_width(draw, line, body_font)
        draw.text(((W - lw) // 2, y), line, fill=CHARCOAL, font=body_font)
        y += 44

    img.save(os.path.join(OUTPUT_DIR, "resume_07_elegant.png"), "PNG", dpi=(300, 300))
    print("  Created resume_07_elegant.png")


# ============================================================
# Template 8: Bold (large name, color blocks for sections)
# ============================================================
def create_bold():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = MARGIN

    y = 150

    # Huge name
    name_font = get_font(130, bold=True)
    draw.text((m, y), NAME, fill=NAVY, font=name_font)
    y += 170

    # Color block with title
    draw.rectangle([m, y, W - m, y + 70], fill=SLATE)
    title_font = get_font(36, bold=True)
    draw.text((m + 20, y + 14), "[PROFESSIONAL TITLE]", fill=WHITE, font=title_font)
    y += 90

    # Contact
    contact_font = get_font(30)
    draw.text((m, y), CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 70

    section_font = get_font(42, bold=True)
    body_font = get_font(32)
    bold_font = get_font(32, bold=True)
    small_font = get_font(28)
    content_w = W - 2 * m

    # Summary block
    draw.rectangle([m, y, m + content_w, y + 55], fill=NAVY)
    draw.text((m + 20, y + 8), "PROFESSIONAL SUMMARY", fill=WHITE, font=section_font)
    y += 70
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        draw.text((m, y), line, fill=CHARCOAL, font=body_font)
        y += 44
    y += 25

    # Experience block
    draw.rectangle([m, y, m + content_w, y + 55], fill=NAVY)
    draw.text((m + 20, y + 8), "WORK EXPERIENCE", fill=WHITE, font=section_font)
    y += 70
    for job in JOBS:
        # Accent color block for each job
        draw.rectangle([m, y, m + 6, y + 100], fill=GOLD)
        draw.text((m + 25, y), job["title"], fill=CHARCOAL, font=bold_font)
        y += 42
        draw.text((m + 25, y), f"{job['company']}  \u2022  {job['dates']}", fill=SLATE, font=small_font)
        y += 42
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 70)):
                prefix = "\u25AA " if i == 0 else "  "
                draw.text((m + 35, y), prefix + bl, fill=CHARCOAL, font=body_font)
                y += 40
        y += 18
    y += 10

    # Two column: Education + Skills
    col_w = (content_w - 40) // 2

    # Education
    draw.rectangle([m, y, m + col_w, y + 55], fill=NAVY)
    draw.text((m + 20, y + 8), "EDUCATION", fill=WHITE, font=section_font)
    ey = y + 70
    for edu in EDUCATION:
        draw.text((m, ey), edu["degree"], fill=CHARCOAL, font=bold_font)
        ey += 40
        draw.text((m, ey), f"{edu['school']} | {edu['year']}", fill=DARK_GRAY, font=small_font)
        ey += 50

    # Skills
    skills_x = m + col_w + 40
    draw.rectangle([skills_x, y, skills_x + col_w, y + 55], fill=NAVY)
    draw.text((skills_x + 20, y + 8), "SKILLS", fill=WHITE, font=section_font)
    sky = y + 70
    for i, skill in enumerate(SKILLS):
        draw.text((skills_x, sky), skill, fill=CHARCOAL, font=body_font)
        sky += 36
        draw_skill_bar(draw, skills_x, sky, col_w - 20, 14, SKILL_LEVELS[i], GOLD, LIGHT_GRAY)
        sky += 30

    img.save(os.path.join(OUTPUT_DIR, "resume_08_bold.png"), "PNG", dpi=(300, 300))
    print("  Created resume_08_bold.png")


# ============================================================
# Template 9: Academic
# ============================================================
def create_academic():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = MARGIN
    y = 150

    # Name
    name_font = get_serif_font(80, bold=True)
    nw = text_width(draw, NAME, name_font)
    draw.text(((W - nw) // 2, y), NAME, fill=NAVY, font=name_font)
    y += 110

    # Title
    title_font = get_serif_font(38)
    title_text = "Ph.D. Candidate / Researcher  |  [Department]"
    tw = text_width(draw, title_text, title_font)
    draw.text(((W - tw) // 2, y), title_text, fill=SLATE, font=title_font)
    y += 60

    # Contact
    contact_font = get_font(28)
    cw = text_width(draw, CONTACT, contact_font)
    draw.text(((W - cw) // 2, y), CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 60

    draw.line([(m, y), (W - m, y)], fill=NAVY, width=3)
    y += 30

    section_font = get_serif_font(42, bold=True)
    body_font = get_serif_font(30)
    bold_font = get_serif_font(30, bold=True)
    small_font = get_serif_font(26)
    content_w = W - 2 * m

    # Research Interests
    draw.text((m, y), "RESEARCH INTERESTS", fill=NAVY, font=section_font)
    y += 55
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 15
    research_text = "Machine learning, natural language processing, computational linguistics, AI ethics, data-driven decision systems"
    for line in wrap_text(draw, research_text, body_font, content_w):
        draw.text((m, y), line, fill=CHARCOAL, font=body_font)
        y += 40
    y += 20

    # Education
    draw.text((m, y), "EDUCATION", fill=NAVY, font=section_font)
    y += 55
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 15
    academic_edu = [
        {"degree": "Ph.D. in [Field]", "school": "[University Name]", "year": "[Year] - Present", "detail": "Dissertation: [Title of Dissertation]"},
        {"degree": "M.S. in [Field]", "school": "[University Name]", "year": "[Year]", "detail": "Thesis: [Title of Thesis]"},
        {"degree": "B.S. in [Field]", "school": "[University Name]", "year": "[Year]", "detail": "Summa Cum Laude"},
    ]
    for edu in academic_edu:
        draw.text((m, y), edu["degree"], fill=CHARCOAL, font=bold_font)
        yr_w = text_width(draw, edu["year"], small_font)
        draw.text((W - m - yr_w, y + 4), edu["year"], fill=DARK_GRAY, font=small_font)
        y += 38
        draw.text((m + 20, y), edu["school"], fill=SLATE, font=small_font)
        y += 34
        draw.text((m + 20, y), edu["detail"], fill=DARK_GRAY, font=small_font)
        y += 42
    y += 15

    # Publications
    draw.text((m, y), "PUBLICATIONS", fill=NAVY, font=section_font)
    y += 55
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 15
    pubs = [
        "[Your Name], et al. (2025). \"[Paper Title].\" Journal of [Field], 12(3), 45-67.",
        "[Your Name] & [Co-Author]. (2024). \"[Paper Title].\" Proceedings of [Conference].",
        "[Your Name], et al. (2023). \"[Paper Title].\" [Journal Name], 8(1), 12-28.",
    ]
    for pub in pubs:
        for i, line in enumerate(wrap_text(draw, pub, body_font, content_w - 40)):
            prefix = f"{pubs.index(pub)+1}. " if i == 0 else "   "
            draw.text((m, y), prefix + line, fill=CHARCOAL, font=body_font)
            y += 38
        y += 8
    y += 15

    # Teaching Experience
    draw.text((m, y), "TEACHING EXPERIENCE", fill=NAVY, font=section_font)
    y += 55
    draw.line([(m, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 15
    draw.text((m, y), "Teaching Assistant  \u2014  [Course Name]", fill=CHARCOAL, font=bold_font)
    draw.text((W - m - 200, y + 4), "[Year] - [Year]", fill=DARK_GRAY, font=small_font)
    y += 38
    draw.text((m + 20, y), "[University Name]", fill=SLATE, font=small_font)
    y += 36
    draw.text((m + 20, y), "\u2022 Led weekly discussion sections for 60+ undergraduate students", fill=CHARCOAL, font=body_font)
    y += 36
    draw.text((m + 20, y), "\u2022 Developed course materials and grading rubrics", fill=CHARCOAL, font=body_font)
    y += 50

    # Awards / Skills in two columns
    col_w = (content_w - 60) // 2
    draw.text((m, y), "AWARDS & HONORS", fill=NAVY, font=section_font)
    draw.text((m + col_w + 60, y), "TECHNICAL SKILLS", fill=NAVY, font=section_font)
    y += 55
    draw.line([(m, y), (m + col_w, y)], fill=MED_GRAY, width=1)
    draw.line([(m + col_w + 60, y), (W - m, y)], fill=MED_GRAY, width=1)
    y += 15

    awards = ["[Award Name], [Year]", "[Fellowship Name], [Year]", "Dean's List, [Years]"]
    ay = y
    for a in awards:
        draw.text((m, ay), "\u2022 " + a, fill=CHARCOAL, font=body_font)
        ay += 40

    sky = y
    sx = m + col_w + 60
    tech_skills = ["Python, R, MATLAB", "TensorFlow, PyTorch", "LaTeX, Git, SQL", "Statistical Analysis"]
    for s in tech_skills:
        draw.text((sx, sky), "\u2022 " + s, fill=CHARCOAL, font=body_font)
        sky += 40

    img.save(os.path.join(OUTPUT_DIR, "resume_09_academic.png"), "PNG", dpi=(300, 300))
    print("  Created resume_09_academic.png")


# ============================================================
# Template 10: Compact
# ============================================================
def create_compact():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    m = 140  # Tighter margins
    y = 100

    # Compact header
    name_font = get_font(68, bold=True)
    draw.text((m, y), NAME, fill=NAVY, font=name_font)
    y += 85

    contact_font = get_font(26)
    draw.text((m, y), CONTACT, fill=DARK_GRAY, font=contact_font)
    y += 45
    draw.line([(m, y), (W - m, y)], fill=NAVY, width=3)
    y += 20

    section_font = get_font(34, bold=True)
    body_font = get_font(26)
    bold_font = get_font(26, bold=True)
    small_font = get_font(23)
    content_w = W - 2 * m
    line_h = 34

    # Summary
    draw.rectangle([m, y, m + content_w, y + 38], fill=LIGHT_GRAY)
    draw.text((m + 10, y + 3), "PROFESSIONAL SUMMARY", fill=NAVY, font=section_font)
    y += 44
    for line in wrap_text(draw, SUMMARY, body_font, content_w):
        draw.text((m, y), line, fill=CHARCOAL, font=body_font)
        y += line_h
    y += 12

    # Experience
    draw.rectangle([m, y, m + content_w, y + 38], fill=LIGHT_GRAY)
    draw.text((m + 10, y + 3), "WORK EXPERIENCE", fill=NAVY, font=section_font)
    y += 44
    for job in JOBS:
        draw.text((m, y), job["title"], fill=CHARCOAL, font=bold_font)
        dates_w = text_width(draw, job["dates"], small_font)
        draw.text((W - m - dates_w, y + 3), job["dates"], fill=DARK_GRAY, font=small_font)
        y += line_h
        draw.text((m, y), job["company"], fill=SLATE, font=small_font)
        y += line_h
        for bullet in job["bullets"]:
            for i, bl in enumerate(wrap_text(draw, bullet, body_font, content_w - 40)):
                prefix = "\u2022 " if i == 0 else "  "
                draw.text((m + 15, y), prefix + bl, fill=CHARCOAL, font=body_font)
                y += line_h
        y += 8
    y += 8

    # Three columns: Education, Skills, Extra
    col_w = (content_w - 60) // 3
    col1 = m
    col2 = m + col_w + 30
    col3 = m + 2 * (col_w + 30)

    # Education
    draw.rectangle([col1, y, col1 + col_w, y + 38], fill=LIGHT_GRAY)
    draw.text((col1 + 10, y + 3), "EDUCATION", fill=NAVY, font=section_font)
    ey = y + 44
    for edu in EDUCATION:
        for line in wrap_text(draw, edu["degree"], bold_font, col_w):
            draw.text((col1, ey), line, fill=CHARCOAL, font=bold_font)
            ey += line_h
        draw.text((col1, ey), edu["school"], fill=SLATE, font=small_font)
        ey += 30
        draw.text((col1, ey), edu["year"], fill=DARK_GRAY, font=small_font)
        ey += 38

    # Skills
    draw.rectangle([col2, y, col2 + col_w, y + 38], fill=LIGHT_GRAY)
    draw.text((col2 + 10, y + 3), "SKILLS", fill=NAVY, font=section_font)
    sky = y + 44
    for skill in SKILLS:
        draw.text((col2, sky), "\u2022 " + skill, fill=CHARCOAL, font=body_font)
        sky += line_h

    # Extra: Certifications + Languages
    draw.rectangle([col3, y, col3 + col_w, y + 38], fill=LIGHT_GRAY)
    draw.text((col3 + 10, y + 3), "CERTIFICATIONS", fill=NAVY, font=section_font)
    cy = y + 44
    for cert in CERTIFICATIONS:
        for line in wrap_text(draw, cert, body_font, col_w):
            draw.text((col3, cy), "\u2022 " + line, fill=CHARCOAL, font=body_font)
            cy += line_h
    cy += 15
    draw.text((col3, cy), "LANGUAGES", fill=NAVY, font=section_font)
    cy += 40
    for lang, level in LANGUAGES:
        draw.text((col3, cy), f"{lang}: {level}", fill=CHARCOAL, font=body_font)
        cy += line_h

    img.save(os.path.join(OUTPUT_DIR, "resume_10_compact.png"), "PNG", dpi=(300, 300))
    print("  Created resume_10_compact.png")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Generating 10 resume templates...")
    create_classic()
    create_modern()
    create_creative()
    create_minimalist()
    create_executive()
    create_tech()
    create_elegant()
    create_bold()
    create_academic()
    create_compact()
    print("Done! All 10 resume templates created.")
