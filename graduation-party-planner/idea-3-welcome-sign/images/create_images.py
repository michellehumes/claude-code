#!/usr/bin/env python3
"""
Etsy Listing Images for Graduation Party Welcome Sign (Canva Template)
3 images at 2700 x 2025 px, 4:3 ratio, 300 DPI, RGB
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2700, 2025
MARGIN = 150
DPI = 300

C = {
    "bg":           (255, 255, 255),
    "white":        (255, 255, 255),
    "navy":         (26, 39, 68),      # #1a2744
    "gold":         (212, 175, 55),    # #D4AF37
    "gold_light":   (255, 248, 220),
    "pink":         (251, 88, 135),    # #fb5887
    "pink_light":   (253, 232, 239),
    "dark":         (44, 62, 80),      # #2C3E50
    "gray":         (100, 100, 100),
    "light_gray":   (230, 232, 234),
    "cream":        (255, 253, 245),
    "black":        (0, 0, 0),
    "success":      (39, 174, 96),
}


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def new_image():
    img = Image.new("RGB", (W, H), C["bg"])
    return img, ImageDraw.Draw(img)


def draw_text_centered(draw, text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)
    return bbox[3] - bbox[1]


def draw_gold_bar(draw, y, x1=None, x2=None, h=5):
    x1 = x1 or MARGIN
    x2 = x2 or W - MARGIN
    draw.rectangle((x1, y, x2, y + h), fill=C["gold"])


def draw_welcome_sign_mockup(draw, x, y, w, h, variant="navy"):
    """Draw a welcome sign mockup — navy/gold or white/pink variant."""
    if variant == "navy":
        bg_color = C["navy"]
        headline_color = C["gold"]
        sub_color = C["white"]
        accent_color = C["gold"]
        border_color = C["gold"]
    else:
        bg_color = C["white"]
        headline_color = C["dark"]
        sub_color = C["pink"]
        accent_color = C["pink"]
        border_color = C["pink"]

    # Sign shadow
    draw.rounded_rectangle((x + 10, y + 10, x + w + 10, y + h + 10), radius=12, fill=C["light_gray"])

    # Sign background
    draw.rounded_rectangle((x, y, x + w, y + h), radius=12, fill=bg_color)

    # Border frame inside
    pad = 12
    draw.rounded_rectangle((x + pad, y + pad, x + w - pad, y + h - pad),
                            radius=8, outline=border_color, width=3)
    inner_pad = 20
    draw.rounded_rectangle((x + inner_pad, y + inner_pad, x + w - inner_pad, y + h - inner_pad),
                            radius=4, outline=border_color, width=1)

    # Top color stripe
    draw.rectangle((x + pad, y + pad, x + w - pad, y + pad + 20), fill=accent_color)
    draw.rounded_rectangle((x + pad, y + pad, x + w - pad, y + pad + 20), radius=8, fill=accent_color)
    draw.rectangle((x + pad, y + pad + 12, x + w - pad, y + pad + 20), fill=accent_color)

    center_x = x + w // 2
    font_welcome = get_font(max(16, w // 28), bold=False)
    font_name = get_font(max(28, w // 14), bold=True)
    font_class = get_font(max(20, w // 22), bold=True)
    font_detail = get_font(max(14, w // 30), bold=False)

    text_start = y + pad + 30

    # "WELCOME TO"
    bbox = draw.textbbox((0, 0), "WELCOME TO", font=font_welcome)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, text_start + 8), "WELCOME TO", fill=sub_color, font=font_welcome)

    # Gold divider
    div_y = text_start + 35
    draw.rectangle((center_x - 80, div_y, center_x + 80, div_y + 2), fill=accent_color)

    # Graduate name (large)
    name = "Emily's"
    bbox = draw.textbbox((0, 0), name, font=font_name)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, div_y + 8), name, fill=headline_color, font=font_name)

    # "GRADUATION PARTY"
    party_text = "GRADUATION PARTY"
    bbox = draw.textbbox((0, 0), party_text, font=font_class)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    party_y = div_y + 8 + bbox[3] - bbox[1] + 10
    draw.text((center_x - tw // 2, party_y), party_text, fill=sub_color, font=font_class)

    # Divider
    div2_y = party_y + th + 12
    draw.rectangle((center_x - 60, div2_y, center_x + 60, div2_y + 2), fill=accent_color)

    # School + year
    school_text = "Westfield High · Class of 2026"
    bbox = draw.textbbox((0, 0), school_text, font=font_detail)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, div2_y + 8), school_text, fill=sub_color, font=font_detail)

    # Date
    date_text = "Saturday, June 14, 2026"
    bbox = draw.textbbox((0, 0), date_text, font=font_detail)
    tw = bbox[2] - bbox[0]
    draw.text((center_x - tw // 2, div2_y + 8 + 30), date_text, fill=accent_color, font=font_detail)

    # Graduation cap emoji/symbol at bottom
    cap_y = y + h - 80
    if cap_y > div2_y + 80:
        font_cap = get_font(max(30, w // 16), bold=True)
        bbox = draw.textbbox((0, 0), "🎓", font=font_cap)
        tw = bbox[2] - bbox[0]
        draw.text((center_x - tw // 2, cap_y), "🎓", fill=headline_color, font=font_cap)

    # Bottom color stripe
    draw.rectangle((x + pad, y + h - pad - 20, x + w - pad, y + h - pad), fill=accent_color)
    draw.rounded_rectangle((x + pad, y + h - pad - 20, x + w - pad, y + h - pad), radius=8, fill=accent_color)
    draw.rectangle((x + pad, y + h - pad - 20, x + w - pad, y + h - pad - 12), fill=accent_color)


# ── IMAGE 1: HERO ─────────────────────────────────────────────────────────────
def create_hero():
    img, draw = new_image()

    # Accent bars
    draw.rectangle((0, 0, W, 14), fill=C["navy"])
    draw.rectangle((0, H - 14, W, H), fill=C["gold"])

    # Badge
    badge_text = "CANVA TEMPLATE — EDITABLE & INSTANT DOWNLOAD"
    font_badge = get_font(26, bold=True)
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bx = (W - bw - 60) // 2
    draw.rounded_rectangle((bx, 28, bx + bw + 60, 78), radius=25, fill=C["navy"])
    draw.text((bx + 30, 40), badge_text, fill=C["white"], font=font_badge)

    # Headline
    font_h = get_font(90, bold=True)
    draw_text_centered(draw, "GRADUATION PARTY", 92, font_h, C["dark"])
    font_h2 = get_font(72, bold=True)
    draw_text_centered(draw, "WELCOME SIGN TEMPLATE", 192, font_h2, C["gold"])

    draw_gold_bar(draw, 282, MARGIN + 200, W - MARGIN - 200, h=4)

    font_sub = get_font(36, bold=False)
    draw_text_centered(draw, "Editable in Canva — customize the name, year, school & date in minutes", 300, font_sub, C["gray"])

    # Two sign variants side by side
    sign_w = 800
    sign_h = 1120
    gap = 80
    total = sign_w * 2 + gap
    start_x = (W - total) // 2
    sign_y = 380

    # Navy/Gold variant
    draw_welcome_sign_mockup(draw, start_x, sign_y, sign_w, sign_h, variant="navy")

    # Variant label
    font_label = get_font(30, bold=True)
    bbox = draw.textbbox((0, 0), "Navy & Gold", font=font_label)
    lw = bbox[2] - bbox[0]
    lx = start_x + (sign_w - lw) // 2
    draw.rounded_rectangle((lx - 20, sign_y + sign_h + 14, lx + lw + 20, sign_y + sign_h + 56),
                            radius=10, fill=C["navy"])
    draw.text((lx, sign_y + sign_h + 22), "Navy & Gold", fill=C["white"], font=font_label)

    # White/Pink variant
    pink_x = start_x + sign_w + gap
    draw_welcome_sign_mockup(draw, pink_x, sign_y, sign_w, sign_h, variant="pink")

    bbox = draw.textbbox((0, 0), "White & Pink", font=font_label)
    lw = bbox[2] - bbox[0]
    lx = pink_x + (sign_w - lw) // 2
    draw.rounded_rectangle((lx - 20, sign_y + sign_h + 14, lx + lw + 20, sign_y + sign_h + 56),
                            radius=10, fill=C["pink"])
    draw.text((lx, sign_y + sign_h + 22), "White & Pink", fill=C["white"], font=font_label)

    # Bottom section
    draw_gold_bar(draw, 1582, MARGIN, W - MARGIN, h=3)

    font_cta = get_font(38, bold=True)
    draw_text_centered(draw, "2 Design Variants Included  •  $4.99  •  Edit in Canva (Free)", 1600, font_cta, C["dark"])

    font_star = get_font(34, bold=True)
    draw_text_centered(draw, "★★★★★  Perfect for every graduation party entrance", 1670, font_star, C["gold"])

    img.save("01_hero.png", dpi=(DPI, DPI))
    print("✓ Saved 01_hero.png")


# ── IMAGE 2: EASY TO EDIT ─────────────────────────────────────────────────────
def create_editable():
    img, draw = new_image()

    draw.rectangle((0, 0, W, 14), fill=C["navy"])
    draw.rectangle((0, H - 14, W, H), fill=C["pink"])

    font_h = get_font(90, bold=True)
    draw_text_centered(draw, "EASY TO EDIT IN CANVA", 28, font_h, C["dark"])

    draw_gold_bar(draw, 132, MARGIN + 100, W - MARGIN - 100, h=4)

    font_sub = get_font(36, bold=False)
    draw_text_centered(draw, "No design skills needed — just click, type, and download", 150, font_sub, C["gray"])

    # Left side: laptop mockup with Canva editor
    laptop_x = MARGIN
    laptop_y = 230
    laptop_w = 1300
    laptop_h = 860

    # Laptop screen bezel
    draw.rounded_rectangle((laptop_x, laptop_y, laptop_x + laptop_w, laptop_y + laptop_h),
                            radius=20, fill=C["dark"])
    screen_pad = 24
    screen_x = laptop_x + screen_pad
    screen_y = laptop_y + screen_pad
    screen_w = laptop_w - screen_pad * 2
    screen_h = laptop_h - screen_pad * 2 - 20

    # Canva editor screen
    draw.rounded_rectangle((screen_x, screen_y, screen_x + screen_w, screen_y + screen_h),
                            radius=8, fill=C["white"])

    # Canva toolbar bar
    draw.rectangle((screen_x, screen_y, screen_x + screen_w, screen_y + 32), fill=(91, 33, 182))  # Canva purple
    font_canva = get_font(18, bold=True)
    draw.text((screen_x + 12, screen_y + 8), "Canva  —  Graduation Welcome Sign", fill=C["white"], font=font_canva)

    # Left sidebar (tools)
    sidebar_w = 40
    draw.rectangle((screen_x, screen_y + 32, screen_x + sidebar_w, screen_y + screen_h),
                   fill=(240, 240, 242))

    # Canvas area with the sign inside
    canvas_x = screen_x + sidebar_w + 20
    canvas_y = screen_y + 42
    canvas_w = screen_w - sidebar_w - 20 - 200
    canvas_h = screen_h - 52
    draw.rectangle((canvas_x, canvas_y, canvas_x + canvas_w, canvas_y + canvas_h), fill=(180, 180, 190))

    # The sign at reduced scale inside canvas
    sign_pad = 20
    draw_welcome_sign_mockup(draw,
                             canvas_x + sign_pad,
                             canvas_y + sign_pad,
                             int((canvas_w - sign_pad * 2) * 0.55),
                             canvas_h - sign_pad * 2,
                             variant="navy")

    # Right panel (properties)
    rpanel_x = canvas_x + canvas_w
    draw.rectangle((rpanel_x, screen_y + 32, screen_x + screen_w, screen_y + screen_h),
                   fill=(248, 248, 250))
    font_rp = get_font(14, bold=True)
    props = ["Text", "Color", "Font", "Size", "Position"]
    for i, prop in enumerate(props):
        draw.text((rpanel_x + 10, screen_y + 42 + i * 30), prop, fill=C["gray"], font=font_rp)
        draw.rectangle((rpanel_x + 10, screen_y + 57 + i * 30, rpanel_x + 185, screen_y + 62 + i * 30),
                       fill=C["light_gray"])

    # Laptop base / keyboard
    draw.rounded_rectangle((laptop_x - 30, laptop_y + laptop_h,
                             laptop_x + laptop_w + 30, laptop_y + laptop_h + 28),
                            radius=6, fill=(50, 50, 55))
    draw.rounded_rectangle((laptop_x + laptop_w // 2 - 80, laptop_y + laptop_h + 8,
                             laptop_x + laptop_w // 2 + 80, laptop_y + laptop_h + 20),
                            radius=4, fill=(70, 70, 75))

    # Right side: Steps
    steps_x = MARGIN + 1360
    steps_w = W - steps_x - MARGIN

    font_steps_h = get_font(44, bold=True)
    draw.text((steps_x, laptop_y - 10), "HOW IT WORKS:", fill=C["dark"], font=font_steps_h)
    draw_gold_bar(draw, laptop_y + 40, steps_x, steps_x + steps_w, h=3)

    steps = [
        ("1", "Purchase & download", "Receive the Canva template link\ninstantly via PDF"),
        ("2", "Open in Canva", "Click the link — opens in free\nCanva editor automatically"),
        ("3", "Edit the text", "Click any text to change the name,\nyear, school, and date"),
        ("4", "Download", "Export as PDF or PNG at\nhigh resolution (300 DPI)"),
        ("5", "Print!", "Print at home or drop the file\noff at your local print shop"),
    ]

    font_step_num = get_font(52, bold=True)
    font_step_title = get_font(34, bold=True)
    font_step_body = get_font(26, bold=False)

    for i, (num, title, desc) in enumerate(steps):
        sy = laptop_y + 60 + i * 155
        # Number circle
        nr = 36
        ncx = steps_x + nr
        ncy = sy + nr
        draw.ellipse((ncx - nr, ncy - nr, ncx + nr, ncy + nr), fill=C["gold"])
        bbox = draw.textbbox((0, 0), num, font=font_step_num)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((ncx - nw // 2, ncy - nh // 2 - 4), num, fill=C["white"], font=font_step_num)

        # Step content
        draw.text((steps_x + nr * 2 + 20, sy + 4), title, fill=C["dark"], font=font_step_title)
        for li, line in enumerate(desc.split("\n")):
            draw.text((steps_x + nr * 2 + 20, sy + 46 + li * 34), line, fill=C["gray"], font=font_step_body)

        # Connector line
        if i < len(steps) - 1:
            draw.rectangle((steps_x + nr - 2, ncy + nr, steps_x + nr + 2, ncy + nr + 155 - nr * 2 - 10),
                           fill=C["gold_light"])

    # Bottom section
    draw_gold_bar(draw, 1140, MARGIN, W - MARGIN, h=3)

    font_bullets_h = get_font(44, bold=True)
    draw_text_centered(draw, "WHAT YOU CAN EDIT", 1162, font_bullets_h, C["dark"])

    bullets = [
        ("✏️  Graduate's Name", "Make it personal — any name, any style"),
        ("📅  Party Date & Time", "Add your exact date so guests know when to arrive"),
        ("🏫  School Name", "Add the school or university for a personal touch"),
        ("🎓  Graduation Year", "Update the year to match your Class Of"),
        ("💬  Welcome Message", "Add a custom message or leave it classic"),
    ]

    font_b_title = get_font(32, bold=True)
    font_b_desc = get_font(26, bold=False)
    col_gap = (W - MARGIN * 2) // 2
    for i, (bt, bd) in enumerate(bullets):
        bx = MARGIN + (i % 2) * col_gap + 20
        by = 1230 + (i // 2) * 100
        draw.text((bx, by), bt, fill=C["dark"], font=font_b_title)
        draw.text((bx, by + 38), bd, fill=C["gray"], font=font_b_desc)

    draw_gold_bar(draw, 1450, MARGIN, W - MARGIN, h=3)

    font_cta = get_font(36, bold=True)
    draw_text_centered(draw, "Edit in Canva (Free Account)  •  Download as PDF or PNG  •  Print Anywhere", 1470, font_cta, C["dark"])

    img.save("02_editable.png", dpi=(DPI, DPI))
    print("✓ Saved 02_editable.png")


# ── IMAGE 3: DISPLAY EXAMPLE ──────────────────────────────────────────────────
def create_display():
    img, draw = new_image()

    # Gradient-style background (light celebration feel)
    for y_row in range(H):
        ratio = y_row / H
        r = int(255 - ratio * 10)
        g = int(253 - ratio * 8)
        b = int(245 - ratio * 5)
        draw.line((0, y_row, W, y_row), fill=(r, g, b))

    draw.rectangle((0, 0, W, 14), fill=C["gold"])
    draw.rectangle((0, H - 14, W, H), fill=C["navy"])

    # Headline at top
    font_h = get_font(82, bold=True)
    draw_text_centered(draw, "WELCOME YOUR GUESTS IN STYLE", 28, font_h, C["dark"])

    draw_gold_bar(draw, 128, MARGIN + 100, W - MARGIN - 100, h=4)

    font_sub = get_font(36, bold=False)
    draw_text_centered(draw, "Professional-looking party signage — printed and displayed in minutes", 148, font_sub, C["gray"])

    # Easel mockup
    sign_y = 220
    sign_w = 700
    sign_h = 980
    sign_x = (W - sign_w) // 2 - 100

    # Easel legs
    easel_cx = sign_x + sign_w // 2
    easel_top = sign_y - 30
    leg_spread = 280
    leg_bottom = sign_y + sign_h + 200

    # Back legs
    for offset in [-leg_spread // 3, leg_spread // 3]:
        draw.line((easel_cx, easel_top, easel_cx + offset, leg_bottom), fill=(139, 90, 43), width=10)
    # Front leg (center)
    draw.line((easel_cx, easel_top, easel_cx, leg_bottom - 40), fill=(160, 110, 60), width=14)

    # Crossbar
    draw.rounded_rectangle((easel_cx - 120, sign_y - 10, easel_cx + 120, sign_y + 8),
                            radius=4, fill=(139, 90, 43))

    # The sign on the easel
    draw_welcome_sign_mockup(draw, sign_x, sign_y, sign_w, sign_h, variant="navy")

    # Decorative party elements around the sign
    # Confetti dots
    import random
    random.seed(42)
    confetti_colors = [C["gold"], C["pink"], C["navy"], (39, 174, 96)]
    for _ in range(80):
        cx = random.randint(MARGIN, W - MARGIN)
        cy = random.randint(200, H - 200)
        # Skip area near the sign
        if sign_x - 50 < cx < sign_x + sign_w + 50 and sign_y - 20 < cy < sign_y + sign_h + 20:
            continue
        cr = random.randint(6, 18)
        col = random.choice(confetti_colors)
        draw.ellipse((cx - cr, cy - cr, cx + cr, cy + cr), fill=col)

    # Balloon suggestions on sides
    balloon_specs = [
        (sign_x - 200, 400, C["gold"], 55),
        (sign_x - 140, 280, C["pink"], 50),
        (sign_x - 260, 550, C["navy"], 48),
        (sign_x + sign_w + 180, 380, C["pink"], 55),
        (sign_x + sign_w + 120, 260, C["gold"], 50),
        (sign_x + sign_w + 240, 530, C["navy"], 48),
    ]
    for bx, by, bc, br in balloon_specs:
        draw.ellipse((bx - br, by - br, bx + br, by + br), fill=bc)
        draw.line((bx, by + br, bx - 10, by + br + 80), fill=C["gray"], width=2)

    # Right side callout panel
    panel_x = sign_x + sign_w + 120
    panel_y = 500
    panel_w = W - MARGIN - panel_x
    panel_h = 700

    draw.rounded_rectangle((panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                            radius=20, fill=C["white"], outline=C["gold"], width=3)

    font_panel_h = get_font(38, bold=True)
    bbox = draw.textbbox((0, 0), "LOOKS AMAZING", font=font_panel_h)
    pw = bbox[2] - bbox[0]
    draw.text((panel_x + (panel_w - pw) // 2, panel_y + 30), "LOOKS AMAZING",
              fill=C["dark"], font=font_panel_h)
    bbox2 = draw.textbbox((0, 0), "AS A...", font=font_panel_h)
    pw2 = bbox2[2] - bbox2[0]
    draw.text((panel_x + (panel_w - pw2) // 2, panel_y + 76), "AS A...",
              fill=C["gold"], font=font_panel_h)

    draw_gold_bar(draw, panel_y + 122, panel_x + 20, panel_x + panel_w - 20, h=2)

    display_ideas = [
        ("🎪", "Party Entrance Sign"),
        ("📸", "Photo Backdrop"),
        ("🍽️", "Buffet Table Display"),
        ("🎁", "Gift Table Marker"),
        ("🖼️", "Memory Keepsake"),
    ]

    font_idea = get_font(32, bold=False)
    for i, (emoji, idea) in enumerate(display_ideas):
        iy = panel_y + 140 + i * 98
        draw.rounded_rectangle((panel_x + 20, iy, panel_x + panel_w - 20, iy + 72),
                                radius=10, fill=C["gold_light"])
        draw.text((panel_x + 36, iy + 20), emoji + "  " + idea, fill=C["dark"], font=font_idea)

    # Bottom CTA bar
    draw.rounded_rectangle((MARGIN, H - 180, W - MARGIN, H - 30),
                            radius=16, fill=C["navy"])
    font_cta = get_font(40, bold=True)
    draw_text_centered(draw, "Customize in minutes  ·  Print any size  ·  Display anywhere", H - 140, font_cta, C["white"])
    font_cta2 = get_font(34, bold=False)
    draw_text_centered(draw, "$4.99  ·  Instant Canva Access  ·  2 Design Variants Included", H - 86, font_cta2, C["gold"])

    img.save("03_display.png", dpi=(DPI, DPI))
    print("✓ Saved 03_display.png")


if __name__ == "__main__":
    create_hero()
    create_editable()
    create_display()
    print("\nAll 3 listing images created.")
