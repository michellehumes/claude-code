#!/usr/bin/env python3
"""
Promo video for Digital Planner Stickers Bundle - 12 seconds, 1080x1080, 30fps.
4 scenes: Title, Sticker sheets, Features, CTA.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
import struct
import zlib
import tempfile
import subprocess

# --- Constants ---
VW, VH = 1080, 1080
FPS = 30
DURATION = 12  # seconds
TOTAL_FRAMES = FPS * DURATION  # 360 frames

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STICKER_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "stickers")

# --- Colors ---
PINK = (244, 180, 197)
PEACH = (249, 198, 168)
YELLOW = (249, 228, 167)
MINT = (181, 216, 199)
SKY = (167, 199, 231)
LAVENDER = (197, 180, 227)
WHITE = (255, 255, 255)
CHARCOAL = (68, 68, 68)
COLORS = [PINK, PEACH, YELLOW, MINT, SKY, LAVENDER]
LIGHT_PINK = (253, 235, 240)
LIGHT_LAVENDER = (240, 235, 250)
LIGHT_MINT = (230, 245, 235)
LIGHT_YELLOW = (255, 250, 230)


def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_font_regular(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


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
    if outline and width > 0:
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


def draw_text_centered(draw, text, cx, cy, font, fill=CHARCOAL):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=fill, font=font)


def draw_star(draw, cx, cy, r_outer, r_inner, fill=YELLOW, outline=CHARCOAL, width=2):
    coords = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = r_outer if i % 2 == 0 else r_inner
        coords.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(coords, fill=fill, outline=outline, width=width)


def draw_gradient_bg(img, color_top, color_bottom):
    draw = ImageDraw.Draw(img)
    for y in range(VH):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / VH)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / VH)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / VH)
        draw.line([(0, y), (VW, y)], fill=(r, g, b))


def ease_in_out(t):
    """Smooth ease-in-out function, t in [0,1]."""
    return t * t * (3 - 2 * t)


def load_sticker_sheet(name):
    path = os.path.join(STICKER_DIR, name)
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    return None


# Preload sticker sheets
SHEETS = []
SHEET_NAMES = [
    "sheet_1_daily_planner.png", "sheet_2_motivational.png",
    "sheet_3_functional_tabs.png", "sheet_4_habit_tracker.png",
    "sheet_5_seasonal.png", "sheet_6_washi_tape.png",
    "sheet_7_speech_bubbles.png", "sheet_8_icons.png",
]


def preload_sheets():
    global SHEETS
    for name in SHEET_NAMES:
        s = load_sticker_sheet(name)
        if s:
            SHEETS.append(s.resize((300, 300), Image.LANCZOS))
        else:
            placeholder = Image.new("RGBA", (300, 300), COLORS[len(SHEETS) % len(COLORS)])
            SHEETS.append(placeholder)


# =================================================================
# Scene 1: Title (0-3s, frames 0-89)
# =================================================================
def render_scene_1(frame):
    """200+ Digital Stickers colorful title."""
    img = Image.new("RGB", (VW, VH), WHITE)
    draw_gradient_bg(img, LIGHT_PINK, LIGHT_LAVENDER)
    draw = ImageDraw.Draw(img)

    t = frame / 89.0  # 0 to 1 over scene duration
    ease_t = ease_in_out(min(t * 1.5, 1.0))

    # Animated colorful circles in background
    for i in range(12):
        angle = math.radians(i * 30 + frame * 2)
        r = 200 + i * 30
        cx = VW // 2 + int(r * math.cos(angle) * 0.3)
        cy = VH // 2 + int(r * math.sin(angle) * 0.3)
        color = COLORS[i % len(COLORS)]
        radius = 20 + i * 5
        alpha_color = tuple(int(c * 0.7 + 255 * 0.3) for c in color)
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=alpha_color)

    # "200+" - scales in
    scale = ease_t
    font_size = int(140 * scale)
    if font_size > 5:
        draw_text_centered(draw, "200+", VW // 2, VH // 2 - 120, get_font(font_size), CHARCOAL)

    # "Digital Stickers" - slides up
    slide_y = int(100 * (1 - ease_t))
    draw_text_centered(draw, "Digital", VW // 2, VH // 2 + 20 + slide_y, get_font(90), CHARCOAL)
    draw_text_centered(draw, "Stickers", VW // 2, VH // 2 + 120 + slide_y, get_font(90), CHARCOAL)

    # Color bar animation
    bar_w = int(800 * ease_t)
    if bar_w > 0:
        for i, color in enumerate(COLORS):
            seg_w = bar_w // len(COLORS)
            x = VW // 2 - bar_w // 2 + i * seg_w
            draw_rounded_rect(draw, (x, VH // 2 + 230, x + seg_w - 5, VH // 2 + 255),
                              radius=6, fill=color)

    # Subtitle
    if t > 0.5:
        alpha = ease_in_out(min((t - 0.5) * 3, 1.0))
        sub_color = tuple(int(68 * alpha + 255 * (1 - alpha)) for _ in range(3))
        draw_text_centered(draw, "Planner Sticker Bundle", VW // 2, VH // 2 + 300,
                           get_font(44), sub_color)

    return img


# =================================================================
# Scene 2: Sticker sheets floating (3-6s, frames 90-179)
# =================================================================
def render_scene_2(frame):
    """Sticker sheets scrolling/floating."""
    local_frame = frame - 90
    img = Image.new("RGB", (VW, VH), WHITE)
    draw_gradient_bg(img, LIGHT_MINT, LIGHT_YELLOW)
    draw = ImageDraw.Draw(img)

    t = local_frame / 89.0

    # Title
    draw_text_centered(draw, "8 Sticker Sheets", VW // 2, 80, get_font(56), CHARCOAL)

    # Floating sticker sheets - scroll from right to left
    scroll_offset = int(t * 400)

    for i, sheet in enumerate(SHEETS):
        # Position: 2 rows of 4, with horizontal float
        col = i % 4
        row = i // 4

        base_x = 60 + col * 260
        base_y = 180 + row * 420

        # Float animation - gentle bobbing
        float_y = int(15 * math.sin(frame * 0.08 + i * 1.2))
        float_x = int(10 * math.cos(frame * 0.06 + i * 0.8))

        x = base_x + float_x
        y = base_y + float_y

        # Scale in effect
        if t < 0.3:
            entry_t = min(t / 0.3, 1.0)
            entry_t = ease_in_out(entry_t)
            size = int(250 * entry_t)
            if size < 10:
                continue
            resized = sheet.resize((size, size), Image.LANCZOS)
            offset_x = (250 - size) // 2
            offset_y = (250 - size) // 2
        else:
            size = 250
            resized = sheet.resize((size, size), Image.LANCZOS)
            offset_x = 0
            offset_y = 0

        # Create white bg for sheet
        bg = Image.new("RGB", (size, size), WHITE)
        bg.paste(resized, (0, 0), resized)
        img.paste(bg, (x + offset_x, y + offset_y))

        # Border
        draw.rectangle([x + offset_x, y + offset_y,
                        x + offset_x + size, y + offset_y + size],
                       outline=CHARCOAL, width=2)

        # Label
        labels = ["Daily", "Quotes", "Tabs", "Habits", "Seasonal", "Washi", "Bubbles", "Icons"]
        if t > 0.4:
            label_alpha = min((t - 0.4) / 0.2, 1.0)
            color = COLORS[i % len(COLORS)]
            draw_rounded_rect(draw, (x + offset_x, y + offset_y + size + 5,
                                     x + offset_x + size, y + offset_y + size + 40),
                              radius=8, fill=color)
            draw_text_centered(draw, labels[i], x + offset_x + size // 2,
                               y + offset_y + size + 22, get_font(22), CHARCOAL)

    return img


# =================================================================
# Scene 3: Features (6-9s, frames 180-269)
# =================================================================
def render_scene_3(frame):
    """Features list: GoodNotes compatible, transparent PNG, etc."""
    local_frame = frame - 180
    img = Image.new("RGB", (VW, VH), WHITE)
    draw_gradient_bg(img, LIGHT_LAVENDER, LIGHT_BLUE := (230, 240, 250))
    draw = ImageDraw.Draw(img)

    t = local_frame / 89.0

    # Title
    draw_text_centered(draw, "Features", VW // 2, 100, get_font(72), CHARCOAL)

    features = [
        ("GoodNotes & Notability", "Compatible", PINK),
        ("Transparent PNG", "Background", PEACH),
        ("200+ Stickers", "Precropped", YELLOW),
        ("High Resolution", "2048 x 2048 px", MINT),
        ("Instant Download", "Digital Product", SKY),
        ("8 Themed Sheets", "Organized Sets", LAVENDER),
    ]

    for i, (title, subtitle, color) in enumerate(features):
        # Stagger entry
        entry_delay = i * 0.1
        if t < entry_delay:
            continue
        feature_t = min((t - entry_delay) / 0.3, 1.0)
        feature_t = ease_in_out(feature_t)

        y = 200 + i * 135
        slide_x = int(100 * (1 - feature_t))

        # Feature card
        draw_rounded_rect(draw, (100 + slide_x, y, 980, y + 115),
                          radius=18, fill=WHITE, outline=color, width=3)

        # Color circle icon
        cx = 170 + slide_x
        cy = y + 57
        draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=color, outline=CHARCOAL, width=2)

        # Checkmark in circle
        draw.line([cx - 12, cy, cx - 3, cy + 12], fill=WHITE, width=3)
        draw.line([cx - 3, cy + 12, cx + 15, cy - 10], fill=WHITE, width=3)

        # Text
        draw.text((220 + slide_x, y + 18), title, fill=CHARCOAL, font=get_font(36))
        draw.text((220 + slide_x, y + 65), subtitle, fill=(120, 120, 120), font=get_font_regular(28))

    # Decorative floating stickers in right area
    if t > 0.3:
        for i in range(4):
            if i < len(SHEETS):
                size = 120
                sx = 800 + int(30 * math.sin(frame * 0.05 + i))
                sy = 200 + i * 200 + int(20 * math.cos(frame * 0.07 + i * 2))
                small = SHEETS[i].resize((size, size), Image.LANCZOS)
                bg = Image.new("RGB", (size, size), WHITE)
                bg.paste(small, (0, 0), small)
                img.paste(bg, (sx, sy))
                draw.rectangle([sx, sy, sx + size, sy + size], outline=CHARCOAL, width=1)

    return img


# =================================================================
# Scene 4: CTA (9-12s, frames 270-359)
# =================================================================
def render_scene_4(frame):
    """CTA with $6.99 price."""
    local_frame = frame - 270
    img = Image.new("RGB", (VW, VH), WHITE)
    draw_gradient_bg(img, LIGHT_PINK, LIGHT_LAVENDER)
    draw = ImageDraw.Draw(img)

    t = local_frame / 89.0
    ease_t = ease_in_out(min(t * 2, 1.0))

    # Animated background circles
    for i in range(8):
        angle = math.radians(i * 45 + frame * 1.5)
        r = 250 + i * 20
        cx = VW // 2 + int(r * math.cos(angle) * 0.2)
        cy = VH // 2 + int(r * math.sin(angle) * 0.2)
        color = COLORS[i % len(COLORS)]
        cr = 30 + i * 5
        light_color = tuple(int(c * 0.5 + 255 * 0.5) for c in color)
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=light_color)

    # Main content
    draw_text_centered(draw, "Digital Planner", VW // 2, 200, get_font(72), CHARCOAL)
    draw_text_centered(draw, "Stickers Bundle", VW // 2, 290, get_font(72), CHARCOAL)

    # Color bar
    for i, color in enumerate(COLORS):
        x = 190 + i * 115
        draw_rounded_rect(draw, (x, 365, x + 105, 385), radius=6, fill=color)

    # 200+ badge - pulsing
    pulse = 1.0 + 0.05 * math.sin(frame * 0.15)
    badge_r = int(80 * pulse)
    draw.ellipse([VW // 2 - badge_r, 430 - badge_r // 2, VW // 2 + badge_r, 430 + badge_r + badge_r // 2],
                 fill=PINK, outline=CHARCOAL, width=3)
    draw_text_centered(draw, "200+", VW // 2, 430, get_font(52), CHARCOAL)
    draw_text_centered(draw, "Stickers", VW // 2, 490, get_font(28), CHARCOAL)

    # Price - scales in
    price_scale = ease_t
    price_size = int(120 * price_scale)
    if price_size > 5:
        # Price background
        draw_rounded_rect(draw, (VW // 2 - 200, 580, VW // 2 + 200, 740),
                          radius=30, fill=WHITE, outline=CHARCOAL, width=4)
        draw_text_centered(draw, "Only", VW // 2, 610, get_font(36), CHARCOAL)
        draw_text_centered(draw, "$6.99", VW // 2, 680, get_font(price_size), CHARCOAL)

    # CTA Button
    if t > 0.3:
        btn_t = ease_in_out(min((t - 0.3) / 0.3, 1.0))
        btn_w = int(400 * btn_t)
        if btn_w > 20:
            draw_rounded_rect(draw, (VW // 2 - btn_w // 2, 790, VW // 2 + btn_w // 2, 870),
                              radius=25, fill=CHARCOAL)
            if btn_t > 0.5:
                draw_text_centered(draw, "Shop Now!", VW // 2, 830, get_font(44), WHITE)

    # Bottom features
    if t > 0.5:
        feat_t = ease_in_out(min((t - 0.5) / 0.3, 1.0))
        feat_color = tuple(int(68 * feat_t + 255 * (1 - feat_t)) for _ in range(3))
        feats = ["GoodNotes", "Notability", "iPad", "PNG"]
        for i, feat in enumerate(feats):
            x = 150 + i * 230
            draw_text_centered(draw, feat, x, 930, get_font(30), feat_color)
            if i < 3:
                draw_text_centered(draw, "|", x + 115, 930, get_font(30), feat_color)

    # Instant Download badge
    if t > 0.6:
        draw_rounded_rect(draw, (300, 980, 780, 1040), radius=15, fill=MINT)
        draw_text_centered(draw, "Instant Digital Download", VW // 2, 1010, get_font(32), CHARCOAL)

    return img


# =================================================================
# Video encoding
# =================================================================
def create_video_ffmpeg(frames, output_path):
    """Create MP4 video using ffmpeg with piped frames."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{VW}x{VH}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "23",
        output_path,
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for i, frame_img in enumerate(frames):
        raw = frame_img.tobytes()
        proc.stdin.write(raw)

    proc.stdin.close()
    stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        print(f"ffmpeg stderr: {stderr.decode()}")
        raise RuntimeError(f"ffmpeg exited with code {proc.returncode}")


# =================================================================
# Main
# =================================================================
def main():
    print("Creating promo video (12s, 1080x1080, 30fps)...")
    print("  Preloading sticker sheets...")
    preload_sheets()

    frames = []
    for f in range(TOTAL_FRAMES):
        if f % 30 == 0:
            print(f"  Rendering frame {f}/{TOTAL_FRAMES} ({f/FPS:.1f}s)...")

        if f < 90:       # Scene 1: 0-3s
            frame_img = render_scene_1(f)
        elif f < 180:    # Scene 2: 3-6s
            frame_img = render_scene_2(f)
        elif f < 270:    # Scene 3: 6-9s
            frame_img = render_scene_3(f)
        else:            # Scene 4: 9-12s
            frame_img = render_scene_4(f)

        frames.append(frame_img)

    output_path = os.path.join(SCRIPT_DIR, "promo_video.mp4")
    print(f"\n  Encoding video to {output_path}...")

    try:
        create_video_ffmpeg(frames, output_path)
        print(f"  Video saved: {output_path}")
    except Exception as e:
        print(f"  ffmpeg encoding failed: {e}")
        # Fallback: save as animated GIF
        gif_path = os.path.join(SCRIPT_DIR, "promo_video.gif")
        print(f"  Saving fallback GIF to {gif_path}...")
        # Use every 3rd frame for smaller file
        gif_frames = [f.copy() for f in frames[::3]]
        gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:],
                           duration=100, loop=0, optimize=True)
        print(f"  Fallback GIF saved: {gif_path}")

    print("\nVideo creation complete!")


if __name__ == "__main__":
    main()
