#!/usr/bin/env python3
"""
Create 10 Etsy listing images (2400x2400px PNG) for the
"Serene Neutrals Collection" - Minimalist Abstract Gallery Wall Art Set of 6.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = "/home/user/claude-code/etsy-digital-planner/wall-art-product"
PRINTS_DIR = os.path.join(BASE_DIR, "prints")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

PRINT_FILES = [
    "print_01_horizon.png",
    "print_02_botanical_line.png",
    "print_03_arches.png",
    "print_04_orbs.png",
    "print_05_figure_line.png",
    "print_06_brushstrokes.png",
]

PRINT_NAMES = [
    "Horizon",
    "Botanical Line",
    "Arches",
    "Orbs",
    "Figure Line",
    "Brushstrokes",
]

# ── Color Palette ──────────────────────────────────────────────────────────
CREAM       = (252, 248, 240)
WARM_SAND   = (228, 213, 193)
SOFT_TERRA  = (199, 159, 134)
MUTED_SAGE  = (173, 188, 168)
DUSTY_CLAY  = (189, 149, 130)
WARM_BLUSH  = (222, 195, 182)
CHARCOAL    = (62, 58, 55)

PALETTE_COLORS = [CREAM, WARM_SAND, SOFT_TERRA, MUTED_SAGE, DUSTY_CLAY, WARM_BLUSH]
PALETTE_NAMES  = ["Cream", "Warm Sand", "Soft Terracotta", "Muted Sage", "Dusty Clay", "Warm Blush"]

# Linen-like background (slightly warmer than cream)
LINEN = (245, 238, 225)

# Image dimensions
W, H = 2400, 2400

# ── Fonts ──────────────────────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def serif_font(size, bold=False):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


# ── Helpers ────────────────────────────────────────────────────────────────
def load_print(index):
    """Load a print image by 0-based index."""
    path = os.path.join(PRINTS_DIR, PRINT_FILES[index])
    return Image.open(path).convert("RGBA")


def resize_to_fit(img, max_w, max_h):
    """Resize image to fit within max_w x max_h, preserving aspect ratio."""
    ratio = min(max_w / img.width, max_h / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    return img.resize((new_w, new_h), Image.LANCZOS)


def draw_frame(draw, x, y, w, h, thickness=6, color=CHARCOAL):
    """Draw a rectangular frame outline."""
    for t in range(thickness):
        draw.rectangle([x - t, y - t, x + w + t, y + h + t], outline=color)


def paste_framed_print(canvas, draw, print_img, cx, cy, thumb_w, thumb_h,
                       frame_thick=8, frame_color=CHARCOAL, shadow=True, mat_width=0, mat_color=CREAM):
    """Paste a print onto canvas at center (cx, cy), with optional frame, mat, and shadow."""
    thumb = resize_to_fit(print_img, thumb_w, thumb_h)
    tw, th = thumb.size

    # Total dimensions including mat
    total_w = tw + 2 * mat_width
    total_h = th + 2 * mat_width

    x = cx - total_w // 2
    y = cy - total_h // 2

    # Shadow
    if shadow:
        shadow_off = max(4, frame_thick // 2)
        for s in range(shadow_off, 0, -1):
            sc = (200, 195, 188)
            draw.rectangle(
                [x + s + frame_thick, y + s + frame_thick,
                 x + total_w + s + frame_thick, y + total_h + s + frame_thick],
                fill=sc
            )

    # Mat area
    if mat_width > 0:
        draw.rectangle([x, y, x + total_w, y + total_h], fill=mat_color)

    # Paste print
    px = x + mat_width
    py = y + mat_width
    canvas.paste(thumb, (px, py), thumb if thumb.mode == "RGBA" else None)

    # Frame
    draw_frame(draw, x, y, total_w, total_h, thickness=frame_thick, color=frame_color)

    return (x, y, total_w, total_h)


def text_center_x(draw, text, y, fnt, fill, canvas_width=W):
    """Draw text centered horizontally."""
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return tw


def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = bbox
    if fill:
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
        draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)


def draw_badge(draw, text, cx, cy, fnt, bg_color, text_color, padding_x=40, padding_y=16, radius=12):
    """Draw a rounded badge centered at (cx, cy)."""
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    rx = cx - tw // 2 - padding_x
    ry = cy - th // 2 - padding_y
    draw_rounded_rect(draw,
                      [rx, ry, rx + tw + 2 * padding_x, ry + th + 2 * padding_y],
                      radius, fill=bg_color)
    draw.text((cx - tw // 2, ry + padding_y), text, font=fnt, fill=text_color)


def save(img, filename):
    path = os.path.join(IMAGES_DIR, filename)
    img.save(path, "PNG", quality=95)
    print(f"  Saved: {filename} ({img.size[0]}x{img.size[1]})")


# ── Load all prints once ──────────────────────────────────────────────────
print("Loading prints...")
prints = [load_print(i) for i in range(6)]
print("All prints loaded.\n")


# ======================================================================
#  IMAGE 1: Hero / Thumbnail
# ======================================================================
def create_01_hero():
    print("Creating 01_hero.png ...")
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title area at top
    title_y = 100
    fnt_title = serif_font(72, bold=True)
    text_center_x(draw, "Minimalist Gallery Wall Art", title_y, fnt_title, CHARCOAL)

    fnt_sub = font(48)
    text_center_x(draw, "Set of 6  |  Digital Download", title_y + 100, fnt_sub, DUSTY_CLAY)

    # 2 rows x 3 cols of print thumbnails
    thumb_w, thumb_h = 480, 720
    cols, rows = 3, 2
    gap_x, gap_y = 80, 60
    grid_w = cols * thumb_w + (cols - 1) * gap_x
    grid_h = rows * thumb_h + (rows - 1) * gap_y
    start_x = (W - grid_w) // 2
    start_y = 340

    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col
            px = start_x + col * (thumb_w + gap_x)
            py = start_y + row * (thumb_h + gap_y)
            cx = px + thumb_w // 2
            cy = py + thumb_h // 2
            paste_framed_print(img, draw, prints[idx], cx, cy,
                               thumb_w - 20, thumb_h - 20,
                               frame_thick=5, mat_width=12, mat_color=(255, 255, 255))

    # "INSTANT DOWNLOAD" badge at bottom
    badge_y = start_y + grid_h + 80
    draw_badge(draw, "INSTANT DOWNLOAD", W // 2, badge_y,
               font(44, bold=True), SOFT_TERRA, (255, 255, 255),
               padding_x=50, padding_y=20, radius=16)

    save(img, "01_hero.png")


# ======================================================================
#  IMAGE 2: Gallery Wall Mockup
# ======================================================================
def create_02_gallery_wall():
    print("Creating 02_gallery_wall_mockup.png ...")
    img = Image.new("RGB", (W, H), LINEN)
    draw = ImageDraw.Draw(img)

    # Add subtle texture lines to simulate linen
    for yy in range(0, H, 4):
        c = LINEN[0] + (yy % 3) - 1
        draw.line([(0, yy), (W, yy)], fill=(c, c - 5, c - 12), width=1)

    # Organic gallery arrangement: 2 rows, staggered
    positions = [
        (420,  480,  520, 780),
        (1060, 340,  480, 720),
        (1700, 520,  500, 750),
        (350,  1500, 480, 720),
        (1020, 1380, 520, 780),
        (1700, 1500, 480, 720),
    ]

    for i, (cx, cy, mw, mh) in enumerate(positions):
        paste_framed_print(img, draw, prints[i], cx, cy, mw - 40, mh - 40,
                           frame_thick=8, frame_color=(50, 45, 42),
                           mat_width=18, mat_color=(255, 255, 252))

    # Subtle title at bottom
    fnt = font(36)
    text_center_x(draw, "S E R E N E   N E U T R A L S   C O L L E C T I O N", H - 100, fnt, CHARCOAL)

    save(img, "02_gallery_wall_mockup.png")


# ======================================================================
#  IMAGE 3-5: Print Details (pairs)
# ======================================================================
def create_print_detail(filename, idx1, idx2, label):
    print(f"Creating {filename} ...")
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Two prints side by side, large
    pw, ph = 900, 1350
    gap = 120
    total_w = 2 * pw + gap
    sx = (W - total_w) // 2
    cy = H // 2 - 60

    for i, idx in enumerate([idx1, idx2]):
        cx = sx + pw // 2 + i * (pw + gap)
        paste_framed_print(img, draw, prints[idx], cx, cy, pw - 40, ph - 40,
                           frame_thick=6, frame_color=CHARCOAL,
                           mat_width=20, mat_color=(255, 255, 255))

    # Label at bottom
    fnt = serif_font(56, bold=True)
    label_y = cy + ph // 2 + 100
    # Decorative line
    line_y = label_y - 20
    lw = 300
    draw.line([(W // 2 - lw, line_y), (W // 2 + lw, line_y)], fill=SOFT_TERRA, width=2)
    text_center_x(draw, label, label_y, fnt, CHARCOAL)

    save(img, filename)


# ======================================================================
#  IMAGE 6: Sizes Included
# ======================================================================
def create_06_sizes():
    print("Creating 06_sizes_included.png ...")
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title
    fnt_title = serif_font(76, bold=True)
    text_center_x(draw, "Sizes Included", 120, fnt_title, CHARCOAL)

    # Decorative line
    draw.line([(W // 2 - 200, 220), (W // 2 + 200, 220)], fill=SOFT_TERRA, width=3)

    # Size list
    sizes_imperial = ["5 x 7\"", "8 x 10\"", "11 x 14\"", "12 x 18\"", "16 x 24\"", "18 x 24\"", "24 x 36\""]
    sizes_metric = ["A4", "A3", "A2"]

    fnt_size = font(50)
    fnt_size_bold = font(50, bold=True)
    fnt_label = font(38)

    # Imperial sizes in a grid
    cols = 3
    y_start = 300
    col_w = 600
    row_h = 100
    grid_start_x = (W - cols * col_w) // 2

    # "Imperial" badge
    draw_badge(draw, "IMPERIAL", W // 2, y_start - 10, font(32, bold=True),
               MUTED_SAGE, (255, 255, 255), padding_x=30, padding_y=10, radius=8)

    y_start += 60
    for i, size in enumerate(sizes_imperial):
        row = i // cols
        col = i % cols
        x = grid_start_x + col * col_w + col_w // 2
        y = y_start + row * row_h
        bbox = draw.textbbox((0, 0), size, font=fnt_size)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw // 2 - 50, y), "+", font=fnt_size, fill=MUTED_SAGE)
        draw.text((x - tw // 2, y), size, font=fnt_size, fill=CHARCOAL)

    metric_y = y_start + 3 * row_h + 40
    # "Metric" badge
    draw_badge(draw, "METRIC / ISO", W // 2, metric_y, font(32, bold=True),
               SOFT_TERRA, (255, 255, 255), padding_x=30, padding_y=10, radius=8)

    metric_y += 60
    metric_total_w = len(sizes_metric) * col_w
    metric_sx = (W - metric_total_w) // 2
    for i, size in enumerate(sizes_metric):
        x = metric_sx + i * col_w + col_w // 2
        bbox = draw.textbbox((0, 0), size, font=fnt_size)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw // 2 - 50, metric_y), "+", font=fnt_size, fill=SOFT_TERRA)
        draw.text((x - tw // 2, metric_y), size, font=fnt_size, fill=CHARCOAL)

    # Decorative line
    sep_y = metric_y + 120
    draw.line([(300, sep_y), (W - 300, sep_y)], fill=WARM_SAND, width=2)

    # Small print thumbnails at bottom
    thumb_w, thumb_h = 240, 360
    total_thumbs_w = 6 * thumb_w + 5 * 40
    tx_start = (W - total_thumbs_w) // 2
    ty = sep_y + 50

    for i in range(6):
        t = resize_to_fit(prints[i], thumb_w - 10, thumb_h - 10)
        px = tx_start + i * (thumb_w + 40) + (thumb_w - t.width) // 2
        py = ty + (thumb_h - t.height) // 2
        img.paste(t, (px, py), t if t.mode == "RGBA" else None)
        draw_frame(draw, px - 3, py - 3, t.width + 6, t.height + 6, thickness=2, color=CHARCOAL)

    # "10 sizes for every print" text
    bot_y = ty + thumb_h + 60
    fnt_bot = serif_font(48, bold=True)
    text_center_x(draw, "10 Size Options for Every Print", bot_y, fnt_bot, CHARCOAL)

    save(img, "06_sizes_included.png")


# ======================================================================
#  IMAGE 7: Room Context Mockup
# ======================================================================
def create_07_room():
    print("Creating 07_room_context.png ...")
    img = Image.new("RGB", (W, H), LINEN)
    draw = ImageDraw.Draw(img)

    # Wall texture
    for yy in range(0, H, 3):
        v = LINEN[0] + (yy % 5) - 2
        draw.line([(0, yy), (W, yy)], fill=(v, v - 4, v - 10), width=1)

    # Floor
    floor_y = 1900
    draw.rectangle([0, floor_y, W, H], fill=(210, 198, 180))
    draw.line([(0, floor_y), (W, floor_y)], fill=(180, 168, 150), width=3)

    # Couch shape (muted sage, simple rectangle with rounded top)
    couch_w, couch_h = 1600, 400
    couch_x = (W - couch_w) // 2
    couch_y = floor_y - couch_h - 20
    draw_rounded_rect(draw, [couch_x, couch_y, couch_x + couch_w, couch_y + couch_h],
                      40, fill=MUTED_SAGE)
    # Couch back
    back_h = 120
    draw_rounded_rect(draw, [couch_x + 20, couch_y - back_h, couch_x + couch_w - 20, couch_y + 20],
                      30, fill=(158, 173, 153))
    # Cushion divider lines
    seg = couch_w // 3
    for s in range(1, 3):
        cx_line = couch_x + s * seg
        draw.line([(cx_line, couch_y + 30), (cx_line, couch_y + couch_h - 30)], fill=(158, 173, 153), width=3)

    # Pillows
    pillow_w, pillow_h = 160, 130
    px1 = couch_x + 80
    py1 = couch_y - 40
    draw_rounded_rect(draw, [px1, py1, px1 + pillow_w, py1 + pillow_h], 20, fill=WARM_BLUSH)
    px2 = couch_x + couch_w - 80 - pillow_w
    draw_rounded_rect(draw, [px2, py1, px2 + pillow_w, py1 + pillow_h], 20, fill=DUSTY_CLAY)

    # Hang 3 prints (indices 0, 2, 4) above couch
    print_indices = [0, 2, 4]
    pw, ph = 420, 630
    gap = 80
    total = 3 * pw + 2 * gap
    sx = (W - total) // 2

    for i, pi in enumerate(print_indices):
        cx = sx + pw // 2 + i * (pw + gap)
        cy = couch_y - back_h - ph // 2 - 80
        paste_framed_print(img, draw, prints[pi], cx, cy, pw - 30, ph - 30,
                           frame_thick=7, frame_color=(50, 45, 42),
                           mat_width=16, mat_color=(255, 255, 252))

    # Side table with plant
    table_w, table_h = 120, 200
    tx = couch_x + couch_w + 60
    ty = floor_y - table_h - 20
    draw_rounded_rect(draw, [tx, ty, tx + table_w, ty + table_h], 8, fill=WARM_SAND)
    # Plant pot
    pot_w, pot_h = 60, 50
    pot_x = tx + (table_w - pot_w) // 2
    pot_y = ty - pot_h
    draw_rounded_rect(draw, [pot_x, pot_y, pot_x + pot_w, pot_y + pot_h], 6, fill=DUSTY_CLAY)
    # Leaves
    leaf_cx = pot_x + pot_w // 2
    leaf_cy = pot_y - 30
    draw.ellipse([leaf_cx - 35, leaf_cy - 50, leaf_cx + 35, leaf_cy + 10], fill=(143, 158, 138))
    draw.ellipse([leaf_cx - 25, leaf_cy - 70, leaf_cx + 25, leaf_cy - 10], fill=(153, 168, 148))

    save(img, "07_room_context.png")


# ======================================================================
#  IMAGE 8: Color Palette
# ======================================================================
def create_08_palette():
    print("Creating 08_color_palette.png ...")
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title
    fnt_title = serif_font(68, bold=True)
    text_center_x(draw, "Curated Color Palette", 100, fnt_title, CHARCOAL)

    fnt_sub = font(44)
    text_center_x(draw, "Warm Neutrals", 190, fnt_sub, DUSTY_CLAY)

    # Decorative line
    draw.line([(W // 2 - 250, 260), (W // 2 + 250, 260)], fill=SOFT_TERRA, width=2)

    # 6 color swatches as large circles with names + hex
    swatch_r = 130
    cols = 3
    rows = 2
    gap_x = 650
    gap_y = 420
    start_x = (W - (cols - 1) * gap_x) // 2
    start_y = 440

    fnt_name = font(34, bold=True)
    fnt_hex = font(28)

    all_colors = [CREAM, WARM_SAND, SOFT_TERRA, MUTED_SAGE, DUSTY_CLAY, WARM_BLUSH]
    all_names = ["Cream", "Warm Sand", "Soft Terracotta", "Muted Sage", "Dusty Clay", "Warm Blush"]

    for i in range(6):
        row = i // cols
        col = i % cols
        cx = start_x + col * gap_x
        cy = start_y + row * gap_y

        color = all_colors[i]
        # Circle outline
        draw.ellipse([cx - swatch_r, cy - swatch_r, cx + swatch_r, cy + swatch_r],
                     fill=color, outline=CHARCOAL, width=3)

        # Name below
        name = all_names[i]
        bbox = draw.textbbox((0, 0), name, font=fnt_name)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, cy + swatch_r + 20), name, font=fnt_name, fill=CHARCOAL)

        # Hex code
        hex_str = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        bbox2 = draw.textbbox((0, 0), hex_str, font=fnt_hex)
        tw2 = bbox2[2] - bbox2[0]
        draw.text((cx - tw2 // 2, cy + swatch_r + 62), hex_str, font=fnt_hex, fill=(120, 115, 110))

    # Small thumbnails of all 6 prints at bottom
    sep_y = start_y + 2 * gap_y + 160
    draw.line([(300, sep_y), (W - 300, sep_y)], fill=WARM_SAND, width=2)

    thumb_w, thumb_h = 240, 360
    total_tw = 6 * thumb_w + 5 * 40
    tx_start = (W - total_tw) // 2
    ty = sep_y + 40

    for i in range(6):
        t = resize_to_fit(prints[i], thumb_w - 10, thumb_h - 10)
        px = tx_start + i * (thumb_w + 40) + (thumb_w - t.width) // 2
        py = ty + (thumb_h - t.height) // 2
        img.paste(t, (px, py), t if t.mode == "RGBA" else None)
        draw_frame(draw, px - 2, py - 2, t.width + 4, t.height + 4, thickness=2, color=CHARCOAL)

    # Print names under thumbnails
    fnt_tiny = font(22)
    for i in range(6):
        name = PRINT_NAMES[i]
        bbox = draw.textbbox((0, 0), name, font=fnt_tiny)
        tw = bbox[2] - bbox[0]
        x = tx_start + i * (thumb_w + 40) + thumb_w // 2 - tw // 2
        draw.text((x, ty + thumb_h + 8), name, font=fnt_tiny, fill=CHARCOAL)

    save(img, "08_color_palette.png")


# ======================================================================
#  IMAGE 9: How It Works
# ======================================================================
def create_09_how_it_works():
    print("Creating 09_how_it_works.png ...")
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Title
    fnt_title = serif_font(76, bold=True)
    text_center_x(draw, "How It Works", 140, fnt_title, CHARCOAL)
    draw.line([(W // 2 - 200, 240), (W // 2 + 200, 240)], fill=SOFT_TERRA, width=3)

    # 3 steps side by side
    step_titles = ["Purchase &\nDownload", "Print at Home\nor Online", "Frame &\nDisplay"]
    step_descriptions = [
        "Complete your purchase\nand instantly receive\nyour digital files",
        "Print on quality paper\nat home or at any\nprint shop",
        "Frame your prints and\ncreate your perfect\ngallery wall"
    ]

    fnt_num = serif_font(100, bold=True)
    fnt_step = font(44, bold=True)
    fnt_desc = font(32)

    col_w = W // 3
    icon_y = 480
    icon_r = 110

    for i in range(3):
        cx = col_w // 2 + i * col_w
        accent = SOFT_TERRA if i % 2 == 0 else MUTED_SAGE

        # Large circle background
        draw.ellipse([cx - icon_r, icon_y - icon_r, cx + icon_r, icon_y + icon_r],
                     fill=accent, outline=None)

        # Draw simple icon shapes inside the circle
        if i == 0:  # Download arrow
            aw = 30
            draw.rectangle([cx - aw, icon_y - 50, cx + aw, icon_y + 10], fill=(255, 255, 255))
            draw.polygon([(cx - 60, icon_y + 10), (cx + 60, icon_y + 10), (cx, icon_y + 60)],
                         fill=(255, 255, 255))
            draw.line([(cx - 55, icon_y + 70), (cx + 55, icon_y + 70)],
                      fill=(255, 255, 255), width=8)
        elif i == 1:  # Printer
            pw2, ph2 = 100, 50
            draw.rectangle([cx - pw2 // 2, icon_y - 10, cx + pw2 // 2, icon_y + ph2 - 10],
                           fill=(255, 255, 255), outline=None)
            paper_w = 70
            draw.rectangle([cx - paper_w // 2, icon_y - 55, cx + paper_w // 2, icon_y - 5],
                           fill=(255, 255, 255), outline=None)
            draw.line([(cx - 25, icon_y - 45), (cx + 25, icon_y - 45)], fill=accent, width=3)
            draw.line([(cx - 25, icon_y - 35), (cx + 25, icon_y - 35)], fill=accent, width=3)
            draw.line([(cx - 25, icon_y - 25), (cx + 15, icon_y - 25)], fill=accent, width=3)
            draw.rectangle([cx - 50, icon_y + 40, cx + 50, icon_y + 55],
                           fill=(255, 255, 255))
        else:  # Frame
            fw, fh = 90, 120
            draw.rectangle([cx - fw // 2, icon_y - fh // 2, cx + fw // 2, icon_y + fh // 2],
                           outline=(255, 255, 255), width=8)
            iw, ih = 55, 80
            draw.rectangle([cx - iw // 2, icon_y - ih // 2, cx + iw // 2, icon_y + ih // 2],
                           fill=(255, 255, 240))

        # Step number
        num_y = icon_y + icon_r + 40
        num_text = str(i + 1)
        bbox = draw.textbbox((0, 0), num_text, font=fnt_num)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, num_y), num_text, font=fnt_num, fill=accent)

        # Step title
        title_y = num_y + 130
        for j, line in enumerate(step_titles[i].split("\n")):
            bbox = draw.textbbox((0, 0), line, font=fnt_step)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, title_y + j * 55), line, font=fnt_step, fill=CHARCOAL)

        # Step description
        desc_y = title_y + 150
        for j, line in enumerate(step_descriptions[i].split("\n")):
            bbox = draw.textbbox((0, 0), line, font=fnt_desc)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, desc_y + j * 44), line, font=fnt_desc, fill=(120, 115, 110))

    # Connecting dots between steps
    arrow_y = icon_y
    for i in range(2):
        ax = col_w + i * col_w
        for d in range(0, 60, 12):
            draw.ellipse([ax - 30 + d, arrow_y - 3, ax - 24 + d, arrow_y + 3], fill=WARM_SAND)

    # Bottom accent bar
    bar_y = H - 200
    draw.rectangle([0, bar_y, W, bar_y + 6], fill=SOFT_TERRA)

    fnt_bottom = serif_font(42, bold=True)
    text_center_x(draw, "It's that simple - instant art for your home!", bar_y + 50, fnt_bottom, CHARCOAL)

    save(img, "09_how_it_works.png")


# ======================================================================
#  IMAGE 10: CTA
# ======================================================================
def create_10_cta():
    print("Creating 10_cta.png ...")
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Decorative top border
    draw.rectangle([0, 0, W, 12], fill=SOFT_TERRA)

    # Large title
    fnt_title = serif_font(96, bold=True)
    text_center_x(draw, "Serene Neutrals", 200, fnt_title, CHARCOAL)

    fnt_title2 = serif_font(88, bold=True)
    text_center_x(draw, "Collection", 320, fnt_title2, CHARCOAL)

    # Subtitle
    fnt_sub = font(52)
    text_center_x(draw, "Set of 6 Abstract Art Prints", 470, fnt_sub, (120, 115, 110))

    # Decorative line
    draw.line([(W // 2 - 300, 560), (W // 2 + 300, 560)], fill=WARM_SAND, width=2)

    # "Instant Digital Download" badge
    draw_badge(draw, "INSTANT DIGITAL DOWNLOAD", W // 2, 650,
               font(46, bold=True), SOFT_TERRA, (255, 255, 255),
               padding_x=50, padding_y=22, radius=16)

    # Row of print thumbnails
    thumb_w, thumb_h = 280, 420
    total_tw = 6 * thumb_w + 5 * 50
    tx_start = (W - total_tw) // 2
    ty = 780

    for i in range(6):
        t = resize_to_fit(prints[i], thumb_w - 16, thumb_h - 16)
        px = tx_start + i * (thumb_w + 50) + (thumb_w - t.width) // 2
        py = ty + (thumb_h - t.height) // 2
        # Subtle shadow
        draw.rectangle([px + 4, py + 4, px + t.width + 4, py + t.height + 4],
                       fill=(220, 215, 208))
        img.paste(t, (px, py), t if t.mode == "RGBA" else None)
        draw_frame(draw, px - 3, py - 3, t.width + 6, t.height + 6, thickness=3, color=CHARCOAL)

    # Print names below thumbnails
    fnt_name = font(24)
    for i in range(6):
        name = PRINT_NAMES[i]
        bbox = draw.textbbox((0, 0), name, font=fnt_name)
        tw = bbox[2] - bbox[0]
        x = tx_start + i * (thumb_w + 50) + thumb_w // 2 - tw // 2
        draw.text((x, ty + thumb_h + 10), name, font=fnt_name, fill=CHARCOAL)

    # "7+ SIZE OPTIONS INCLUDED" with sage badge
    info_y = ty + thumb_h + 100
    draw_badge(draw, "7+ SIZE OPTIONS INCLUDED", W // 2, info_y,
               font(38, bold=True), MUTED_SAGE, (255, 255, 255),
               padding_x=40, padding_y=16, radius=12)

    # Features line
    features_y = info_y + 80
    fnt_feat = font(34)
    features = "High Resolution  |  Print Ready  |  Instant Access"
    text_center_x(draw, features, features_y, fnt_feat, (120, 115, 110))

    # Bottom decorative border
    draw.rectangle([0, H - 12, W, H], fill=SOFT_TERRA)

    # Small branding line
    fnt_tiny = font(28)
    text_center_x(draw, "S E R E N E   N E U T R A L S", H - 80, fnt_tiny, DUSTY_CLAY)

    save(img, "10_cta.png")


# ======================================================================
#  Run All
# ======================================================================
if __name__ == "__main__":
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print(f"Output directory: {IMAGES_DIR}\n")

    create_01_hero()
    create_02_gallery_wall()
    create_print_detail("03_print_detail_1.png", 0, 1,
                        "Abstract Landscape  |  Botanical Line Art")
    create_print_detail("04_print_detail_2.png", 2, 3,
                        "Geometric Arches  |  Abstract Orbs")
    create_print_detail("05_print_detail_3.png", 4, 5,
                        "Figure Line Art  |  Brushstroke Abstract")
    create_06_sizes()
    create_07_room()
    create_08_palette()
    create_09_how_it_works()
    create_10_cta()

    print(f"\nAll 10 listing images created in {IMAGES_DIR}")
    print("Done!")
