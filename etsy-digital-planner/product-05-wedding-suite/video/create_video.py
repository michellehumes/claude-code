#!/usr/bin/env python3
"""
Minimalist Wedding Invitation Suite - Promo Video Generator
Creates a 12-second 1080x1080 30fps promotional video.
"""

from PIL import Image, ImageDraw, ImageFont
import subprocess
import math
import os
import tempfile
import shutil

# ── Directories ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
os.makedirs(BASE_DIR, exist_ok=True)

W, H = 1080, 1080
FPS = 30
DURATION = 12
TOTAL_FRAMES = FPS * DURATION

# ── Color Palette ────────────────────────────────────────────────────────────
SAGE = (143, 174, 139)
IVORY = (255, 255, 240)
GOLD = (197, 165, 90)
CHARCOAL = (45, 45, 45)
BLUSH = (245, 230, 224)
WHITE = (255, 255, 255)
CREAM = (250, 248, 240)
LIGHT_SAGE = (220, 235, 218)
DARK_SAGE = (100, 140, 95)


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill)
        return
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)
    if outline and width:
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([(x0 + radius, y0), (x1 - radius, y0)], fill=outline, width=width)
        draw.line([(x0 + radius, y1), (x1 - radius, y1)], fill=outline, width=width)
        draw.line([(x0, y0 + radius), (x0, y1 - radius)], fill=outline, width=width)
        draw.line([(x1, y0 + radius), (x1, y1 - radius)], fill=outline, width=width)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_serif(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_text_centered(draw, text, y, font, fill, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def draw_gold_divider(draw, y, w, length=400):
    cx = w // 2
    draw.line([(cx - length // 2, y), (cx + length // 2, y)], fill=GOLD, width=2)
    r = 3
    draw.ellipse([cx - r, y - r, cx + r, y + r], fill=GOLD)


def draw_branch_simple(draw, x, y, direction, length, color, thickness=2):
    sign = 1 if direction == 'right' else -1
    points = []
    segments = 8
    for i in range(segments + 1):
        t = i / segments
        px = x + sign * t * length
        py = y + math.sin(t * math.pi) * (-length * 0.06)
        points.append((px, py))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=thickness)
    for t in [0.2, 0.4, 0.6, 0.8]:
        idx = int(t * segments)
        if idx < len(points):
            px, py = points[idx]
            for side in [1, -1]:
                la = math.radians(-45 * side + (0 if sign == 1 else 180))
                lx = px + 10 * math.cos(la)
                ly = py + 10 * math.sin(la)
                draw.line([(px, py), (lx, ly)], fill=color, width=1)


def load_template(name):
    path = os.path.join(TEMPLATE_DIR, name)
    if os.path.exists(path):
        return Image.open(path)
    return None


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def lerp(a, b, t):
    return a + (b - a) * t


def draw_gold_border(draw, w, h, inset=20, thickness=2):
    draw.rectangle([inset, inset, w - inset, h - inset], outline=GOLD, width=thickness)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENES
# ═══════════════════════════════════════════════════════════════════════════════

def render_scene_1(frame, total_scene_frames):
    """Scene 1: Title reveal with elegant animation (0-3s = frames 0-89)"""
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)

    t = frame / max(total_scene_frames - 1, 1)

    # Gold border fades in
    border_alpha = min(1.0, t * 2)
    if border_alpha > 0.1:
        draw_gold_border(draw, W, H, inset=25, thickness=2)
        if t > 0.2:
            draw_gold_border(draw, W, H, inset=35, thickness=1)

    # Top branches grow in
    if t > 0.1:
        branch_t = ease_out_cubic(min(1, (t - 0.1) / 0.4))
        branch_len = int(160 * branch_t)
        draw_branch_simple(draw, W // 2 - 5, 70, 'left', branch_len, SAGE, 2)
        draw_branch_simple(draw, W // 2 + 5, 70, 'right', branch_len, SAGE, 2)

    # "Minimalist" slides down from top
    f_title1 = get_serif(52, bold=True)
    f_title2 = get_serif(52, bold=True)
    f_sub = get_serif(30)

    if t > 0.15:
        title_t = ease_out_cubic(min(1, (t - 0.15) / 0.35))
        y_title = int(lerp(-60, 300, title_t))
        draw_text_centered(draw, "Minimalist", y_title, f_title1, CHARCOAL, W)

    # "Wedding Suite" slides up from bottom
    if t > 0.3:
        title2_t = ease_out_cubic(min(1, (t - 0.3) / 0.35))
        y_title2 = int(lerp(600, 370, title2_t))
        draw_text_centered(draw, "Wedding Suite", y_title2, f_title2, CHARCOAL, W)

    # Gold divider draws in
    if t > 0.5:
        div_t = ease_out_cubic(min(1, (t - 0.5) / 0.3))
        div_len = int(350 * div_t)
        draw_gold_divider(draw, 460, W, div_len)

    # Subtitle fades in
    if t > 0.65:
        sub_t = min(1, (t - 0.65) / 0.25)
        draw_text_centered(draw, "Printable Stationery Collection", 490, f_sub, SAGE, W)

    # Small tagline
    if t > 0.75:
        tag_t = min(1, (t - 0.75) / 0.2)
        f_tag = get_font(22)
        draw_text_centered(draw, "8 Matching Pieces  |  3 Color Palettes  |  Instant Download", 550, f_tag, (150, 150, 150), W)

    # Preview cards fade in at bottom
    if t > 0.6:
        preview_t = ease_out_cubic(min(1, (t - 0.6) / 0.4))
        y_base = int(lerp(H, 620, preview_t))

        templates = [
            ("invitation_sage.png", 150, 230),
            ("rsvp_sage.png", 220, 154),
            ("save_the_date_sage.png", 150, 210),
        ]
        x_positions = [120, 380, 620, 830]
        template_files = [
            "invitation_sage.png", "rsvp_sage.png",
            "save_the_date_sage.png", "menu_sage.png"
        ]
        sizes = [(200, 280), (220, 154), (200, 280), (130, 293)]

        for i, (tfile, (tw, th)) in enumerate(zip(template_files, sizes)):
            t_img = load_template(tfile)
            if t_img:
                t_img = t_img.resize((tw, th), Image.LANCZOS)
                x = x_positions[i]
                y = y_base + (i % 2) * 30
                if y + th <= H - 20 and y >= 0:
                    img.paste(t_img, (x, y))
                    draw.rectangle([x - 1, y - 1, x + tw + 1, y + th + 1], outline=GOLD, width=1)

    # Bottom branches
    if t > 0.4:
        bl_t = ease_out_cubic(min(1, (t - 0.4) / 0.4))
        bl_len = int(120 * bl_t)
        draw_branch_simple(draw, 50, H - 40, 'right', bl_len, SAGE, 2)
        draw_branch_simple(draw, W - 50, H - 40, 'left', bl_len, SAGE, 2)

    return img


def render_scene_2(frame, total_scene_frames):
    """Scene 2: Each piece slides in one by one (3-6s = frames 90-179)"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    t = frame / max(total_scene_frames - 1, 1)
    draw_gold_border(draw, W, H, inset=25, thickness=2)

    f_title = get_serif(36, bold=True)
    f_label = get_font(22)
    draw_text_centered(draw, "Complete Stationery Suite", 30, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 78, W, 300)

    # Pieces slide in sequentially
    pieces = [
        ("invitation_sage.png", "Wedding Invitation", 140, 196),
        ("rsvp_sage.png", "RSVP Card", 170, 119),
        ("save_the_date_sage.png", "Save the Date", 140, 196),
        ("details_sage.png", "Details Card", 170, 119),
        ("thank_you_sage.png", "Thank You Card", 140, 196),
        ("menu_sage.png", "Menu Card", 100, 225),
        ("table_number_01_sage.png", "Table Numbers", 120, 180),
        ("place_card_sage.png", "Place Card", 170, 97),
    ]

    # Grid layout 4x2
    grid_positions = [
        (80, 120), (330, 120), (580, 120), (830, 120),
        (80, 520), (330, 520), (580, 520), (830, 520),
    ]

    for i, (tfile, label, tw, th) in enumerate(pieces):
        # Each piece starts appearing at staggered times
        start_t = i * 0.1
        if t > start_t:
            piece_t = ease_out_cubic(min(1, (t - start_t) / 0.2))
            gx, gy = grid_positions[i]
            # Slide in from the right
            x = int(lerp(W + 50, gx, piece_t))
            y = gy + 20

            t_img = load_template(tfile)
            if t_img:
                t_img = t_img.resize((tw, th), Image.LANCZOS)
                if 0 <= x < W:
                    # Shadow
                    draw_rounded_rect(draw, (x + 3, y + 3, x + tw + 3, y + th + 3), 4, (220, 220, 215))
                    img.paste(t_img, (max(0, x), y))
                    draw.rectangle([max(0, x) - 1, y - 1, x + tw + 1, y + th + 1], outline=GOLD, width=1)

            # Label below card
            if piece_t > 0.5:
                label_alpha = min(1, (piece_t - 0.5) * 2)
                lx = gx
                ly = gy + th + 30
                if ly < H - 30:
                    draw.text((lx, ly), label, font=f_label, fill=CHARCOAL)

    # Counter at bottom
    visible_count = min(8, int(t * 10) + 1)
    f_count = get_font(26, bold=True)
    draw_rounded_rect(draw, (350, 960, 730, 1010), 15, SAGE)
    draw_text_centered(draw, f"{visible_count} of 8 Pieces", 968, f_count, WHITE, W)

    return img


def render_scene_3(frame, total_scene_frames):
    """Scene 3: 3 color variants shown (6-9s = frames 180-269)"""
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)

    t = frame / max(total_scene_frames - 1, 1)
    draw_gold_border(draw, W, H, inset=25, thickness=2)

    f_title = get_serif(38, bold=True)
    f_label = get_serif(26, bold=True)
    f_sub = get_font(22)

    draw_text_centered(draw, "3 Color Palettes", 30, f_title, CHARCOAL, W)
    draw_gold_divider(draw, 80, W, 300)

    variants = [
        ("sage", "Sage & Gold", [SAGE, IVORY, GOLD]),
        ("blush", "Blush & Gold", [(210, 170, 160), (252, 248, 245), GOLD]),
        ("classic", "Classic Gold", [CHARCOAL, WHITE, GOLD]),
    ]

    card_w, card_h = 240, 336
    col_spacing = 30

    for v_idx, (vname, vlabel, colors) in enumerate(variants):
        # Each variant reveals at staggered times
        start_t = v_idx * 0.2
        if t <= start_t:
            continue

        vt = ease_out_cubic(min(1, (t - start_t) / 0.3))

        # Column center x
        col_cx = 180 + v_idx * 360
        col_x = col_cx - card_w // 2

        # Label
        if vt > 0.3:
            draw_text_centered(draw, vlabel, 105, f_label, CHARCOAL, col_cx * 2)

        # Color swatches
        if vt > 0.2:
            sw_size = 30
            sw_total = len(colors) * sw_size + (len(colors) - 1) * 10
            sw_start = col_cx - sw_total // 2
            for ci, c in enumerate(colors):
                sx = sw_start + ci * (sw_size + 10)
                draw.ellipse([sx, 145, sx + sw_size, 145 + sw_size], fill=c, outline=GOLD, width=1)

        # Invitation card slides up
        y_start = int(lerp(H, 200, vt))
        inv_img = load_template(f"invitation_{vname}.png")
        if inv_img:
            inv_img = inv_img.resize((card_w, card_h), Image.LANCZOS)
            if y_start + card_h <= H:
                draw_rounded_rect(draw, (col_x + 3, y_start + 3, col_x + card_w + 3, y_start + card_h + 3),
                                   4, (215, 215, 210))
                img.paste(inv_img, (col_x, y_start))

        # RSVP underneath
        if vt > 0.4:
            rsvp_t = ease_out_cubic(min(1, (vt - 0.4) / 0.3))
            rsvp_y = int(lerp(H, 560, rsvp_t))
            rsvp_w, rsvp_h = 240, 168
            rsvp = load_template(f"rsvp_{vname}.png")
            if rsvp and rsvp_y + rsvp_h <= H:
                rsvp = rsvp.resize((rsvp_w, rsvp_h), Image.LANCZOS)
                img.paste(rsvp, (col_x, rsvp_y))

        # Menu card
        if vt > 0.6:
            menu_t = ease_out_cubic(min(1, (vt - 0.6) / 0.3))
            menu_y = int(lerp(H, 750, menu_t))
            menu_w_s, menu_h_s = 160, 360
            menu = load_template(f"menu_{vname}.png")
            if menu and menu_y + menu_h_s <= H:
                menu = menu.resize((menu_w_s, menu_h_s), Image.LANCZOS)
                mx = col_cx - menu_w_s // 2
                img.paste(menu, (mx, min(menu_y, H - menu_h_s - 30)))

    # Bottom text
    if t > 0.7:
        f_bottom = get_font(24, bold=True)
        draw_rounded_rect(draw, (200, 990, 880, 1040), 15, SAGE)
        draw_text_centered(draw, "Mix & Match Colors for Your Perfect Day", 998, f_bottom, WHITE, W)

    return img


def render_scene_4(frame, total_scene_frames):
    """Scene 4: CTA with price (9-12s = frames 270-359)"""
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)

    t = frame / max(total_scene_frames - 1, 1)

    # Gold double border
    draw_gold_border(draw, W, H, inset=20, thickness=3)
    draw_gold_border(draw, W, H, inset=32, thickness=1)

    f_big = get_serif(48, bold=True)
    f_title = get_serif(38, bold=True)
    f_price = get_serif(72, bold=True)
    f_original = get_font(36)
    f_sub = get_font(26)
    f_cta = get_font(34, bold=True)
    f_detail = get_font(22)

    # Top branches grow
    if t > 0.05:
        bt = ease_out_cubic(min(1, t / 0.3))
        bl = int(140 * bt)
        draw_branch_simple(draw, W // 2 - 5, 55, 'left', bl, SAGE, 2)
        draw_branch_simple(draw, W // 2 + 5, 55, 'right', bl, SAGE, 2)

    # Title
    if t > 0.05:
        tt = ease_out_cubic(min(1, (t - 0.05) / 0.25))
        y_t = int(lerp(-50, 120, tt))
        draw_text_centered(draw, "Complete Wedding", y_t, f_big, CHARCOAL, W)
        draw_text_centered(draw, "Stationery Suite", y_t + 60, f_big, CHARCOAL, W)

    # Divider
    if t > 0.2:
        dt = ease_out_cubic(min(1, (t - 0.2) / 0.2))
        draw_gold_divider(draw, 260, W, int(400 * dt))

    # "81+ Files" text
    if t > 0.25:
        draw_text_centered(draw, "81+ Print-Ready Files  |  3 Palettes  |  Instant Download", 290, f_sub, SAGE, W)

    # Small preview strip
    if t > 0.3:
        pt = ease_out_cubic(min(1, (t - 0.3) / 0.3))
        previews = ["invitation_sage.png", "rsvp_sage.png", "save_the_date_sage.png",
                     "menu_sage.png", "thank_you_sage.png"]
        pw, ph = 140, 120
        p_spacing = 20
        p_total = len(previews) * pw + (len(previews) - 1) * p_spacing
        p_sx = (W - p_total) // 2

        for i, pname in enumerate(previews):
            p_img = load_template(pname)
            if p_img:
                p_img = p_img.resize((pw, ph), Image.LANCZOS)
                x = p_sx + i * (pw + p_spacing)
                y = int(lerp(500, 350, pt))
                if 0 <= y < H - ph:
                    img.paste(p_img, (x, y))
                    draw.rectangle([x - 1, y - 1, x + pw + 1, y + ph + 1], outline=GOLD, width=1)

    # Price section
    if t > 0.4:
        price_t = ease_out_cubic(min(1, (t - 0.4) / 0.3))
        y_price = 540

        # Background box
        draw_rounded_rect(draw, (200, y_price, W - 200, y_price + 250), 20, WHITE, outline=GOLD, width=2)

        # Original price with strikethrough
        orig_text = "$39.99"
        orig_bbox = draw.textbbox((0, 0), orig_text, font=f_original)
        orig_w = orig_bbox[2] - orig_bbox[0]
        ox = (W - orig_w) // 2
        draw.text((ox, y_price + 20), orig_text, font=f_original, fill=(180, 180, 180))
        draw.line([(ox, y_price + 45), (ox + orig_w, y_price + 45)], fill=(180, 180, 180), width=3)

        # Sale price grows in
        scale = price_t
        if scale > 0:
            draw_text_centered(draw, "$14.99", y_price + 70, f_price, SAGE, W)
            draw_text_centered(draw, "63% OFF - Limited Time!", y_price + 170, f_sub, GOLD, W)

    # CTA Button
    if t > 0.6:
        cta_t = ease_out_cubic(min(1, (t - 0.6) / 0.2))
        btn_y = 830
        btn_x0 = int(lerp(-400, 220, cta_t))
        btn_x1 = btn_x0 + 640

        # Pulsing effect
        pulse = 1.0 + 0.02 * math.sin(t * 10 * math.pi)
        draw_rounded_rect(draw, (btn_x0, btn_y, btn_x1, btn_y + 80), 40, SAGE)
        draw_text_centered(draw, "Add to Cart", btn_y + 16, f_cta, WHITE, W)

    # Bottom guarantees
    if t > 0.7:
        gt = min(1, (t - 0.7) / 0.2)
        f_g = get_font(20)
        draw_text_centered(draw, "Instant Download  |  No Physical Item  |  Lifetime Access", 940, f_g, (130, 130, 130), W)

    # Bottom branches
    if t > 0.4:
        bbt = ease_out_cubic(min(1, (t - 0.4) / 0.4))
        bbl = int(100 * bbt)
        draw_branch_simple(draw, 50, H - 40, 'right', bbl, SAGE, 2)
        draw_branch_simple(draw, W - 50, H - 40, 'left', bbl, SAGE, 2)

    # Sparkle / shimmer on price
    if t > 0.5:
        shimmer_t = (t - 0.5) * 4
        for s in range(3):
            sx = W // 2 + int(80 * math.cos(shimmer_t * 2 + s * 2))
            sy = 620 + int(20 * math.sin(shimmer_t * 3 + s * 1.5))
            r = int(3 + 2 * math.sin(shimmer_t * 5 + s))
            if r > 0:
                draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=GOLD)

    return img


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("Minimalist Wedding Suite - Video Generator")
    print(f"Resolution: {W}x{H} | {FPS} fps | {DURATION}s | {TOTAL_FRAMES} frames")
    print("=" * 60)

    # Create temp directory for frames
    temp_dir = tempfile.mkdtemp(prefix="wedding_video_")
    print(f"Temp frames dir: {temp_dir}")

    # Scene breakdown (12 seconds = 360 frames)
    # Scene 1: 0-3s (frames 0-89)
    # Scene 2: 3-6s (frames 90-179)
    # Scene 3: 6-9s (frames 180-269)
    # Scene 4: 9-12s (frames 270-359)

    scenes = [
        (0, 90, render_scene_1),
        (90, 90, render_scene_2),
        (180, 90, render_scene_3),
        (270, 90, render_scene_4),
    ]

    for frame_idx in range(TOTAL_FRAMES):
        # Determine which scene
        for scene_start, scene_len, scene_fn in scenes:
            if scene_start <= frame_idx < scene_start + scene_len:
                local_frame = frame_idx - scene_start
                frame_img = scene_fn(local_frame, scene_len)
                break

        frame_path = os.path.join(temp_dir, f"frame_{frame_idx:04d}.png")
        frame_img.save(frame_path, "PNG")

        if frame_idx % 30 == 0:
            print(f"  Rendered frame {frame_idx}/{TOTAL_FRAMES} ({frame_idx * 100 // TOTAL_FRAMES}%)")

    print(f"  Rendered frame {TOTAL_FRAMES}/{TOTAL_FRAMES} (100%)")

    # Assemble video with ffmpeg
    output_path = os.path.join(BASE_DIR, "wedding_suite_promo.mp4")
    print(f"\nAssembling video: {output_path}")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(temp_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "23",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Video saved: {output_path} ({file_size:.1f} MB)")
    else:
        print(f"  FFmpeg error: {result.stderr[:500]}")

    # Cleanup temp dir
    shutil.rmtree(temp_dir, ignore_errors=True)
    print("  Temp files cleaned up.")

    print(f"\n{'=' * 60}")
    print("DONE! Video generation complete.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
