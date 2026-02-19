#!/usr/bin/env python3
"""
Promo video for Motivational Quote Wall Art Prints Bundle.
12 seconds, 1080x1080, 30fps MP4.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import struct
import zlib
import tempfile
import math

# Paths
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINTS_DIR = os.path.join(BASE, "prints")
OUT = os.path.join(BASE, "video")

# Video settings
VW, VH = 1080, 1080
FPS = 30
DURATION = 12
TOTAL_FRAMES = FPS * DURATION  # 360 frames

# Colors
SAGE = (143, 174, 139)
DUSTY_ROSE = (212, 160, 160)
NAVY = (27, 42, 74)
GOLD = (201, 169, 110)
CREAM = (255, 248, 240)
CHARCOAL = (51, 51, 51)
TERRACOTTA = (196, 113, 59)
WHITE = (255, 255, 255)
WARM_CREAM = (250, 240, 225)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_font_bold(size):
    return get_font(size, bold=True)


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill)
        return
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.pieslice([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=fill)
    draw.pieslice([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0+2*radius, y0+2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*radius, y0, x1, y0+2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*radius, x0+2*radius, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*radius, y1-2*radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([(x0+radius, y0), (x1-radius, y0)], fill=outline, width=width)
        draw.line([(x0+radius, y1), (x1-radius, y1)], fill=outline, width=width)
        draw.line([(x0, y0+radius), (x0, y1-radius)], fill=outline, width=width)
        draw.line([(x1, y0+radius), (x1, y1-radius)], fill=outline, width=width)


def centered_text(draw, text, y, font, fill, canvas_w=VW):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (canvas_w - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def load_print_thumb(num, size=(200, 250)):
    """Load and resize a print."""
    path = os.path.join(PRINTS_DIR, f"quote_print_{num:02d}.jpg")
    img = Image.open(path)
    return img.resize(size, Image.LANCZOS)


def ease_in_out(t):
    """Smooth easing function."""
    return t * t * (3 - 2 * t)


# Pre-load print thumbnails
print("Loading print thumbnails...")
THUMBS = {}
for i in range(1, 31):
    THUMBS[i] = load_print_thumb(i, (180, 225))
THUMBS_LG = {}
for i in range(1, 31):
    THUMBS_LG[i] = load_print_thumb(i, (280, 350))


def render_scene_1(frame_in_scene, total_scene_frames):
    """Scene 1: Title card - '30 Motivational Quote Prints'"""
    img = Image.new('RGB', (VW, VH), NAVY)
    draw = ImageDraw.Draw(img)

    progress = frame_in_scene / total_scene_frames

    # Decorative border fade in
    if progress > 0.1:
        alpha = min(1.0, (progress - 0.1) / 0.3)
        border_color = tuple(int(NAVY[i] + (GOLD[i] - NAVY[i]) * alpha) for i in range(3))
        draw.rectangle([30, 30, VW - 30, VH - 30], outline=border_color, width=2)
        draw.rectangle([45, 45, VW - 45, VH - 45], outline=border_color, width=1)

    # Number "30" - large and bold, fades in
    if progress > 0.05:
        alpha = min(1.0, (progress - 0.05) / 0.25)
        font_30 = get_font_bold(220)
        c = tuple(int(NAVY[i] + (GOLD[i] - NAVY[i]) * alpha) for i in range(3))
        centered_text(draw, "30", 180, font_30, c)

    # "MOTIVATIONAL QUOTE" title
    if progress > 0.2:
        alpha = min(1.0, (progress - 0.2) / 0.3)
        font_title = get_font_bold(72)
        c = tuple(int(NAVY[i] + (WHITE[i] - NAVY[i]) * alpha) for i in range(3))
        centered_text(draw, "MOTIVATIONAL", 440, font_title, c)
        centered_text(draw, "QUOTE PRINTS", 530, font_title, c)

    # Subtitle
    if progress > 0.4:
        alpha = min(1.0, (progress - 0.4) / 0.3)
        font_sub = get_font(38)
        c = tuple(int(NAVY[i] + (GOLD[i] - NAVY[i]) * alpha) for i in range(3))
        centered_text(draw, "Printable Wall Art Bundle", 650, font_sub, c)

    # Small sample prints at bottom
    if progress > 0.5:
        alpha = min(1.0, (progress - 0.5) / 0.3)
        samples = [1, 5, 10, 16, 22, 30]
        pw, ph = 130, 162
        gap = 20
        total_w = len(samples) * pw + (len(samples) - 1) * gap
        sx = (VW - total_w) // 2
        for i, pnum in enumerate(samples):
            x = sx + i * (pw + gap)
            y = 760
            thumb = THUMBS[pnum].resize((pw, ph), Image.LANCZOS)
            # Frame
            draw.rectangle([x - 3, y - 3, x + pw + 3, y + ph + 3], fill=WHITE)
            img.paste(thumb, (x, y))

    return img


def render_scene_2(frame_in_scene, total_scene_frames):
    """Scene 2: Prints scrolling/cascading through."""
    img = Image.new('RGB', (VW, VH), CREAM)
    draw = ImageDraw.Draw(img)

    progress = frame_in_scene / total_scene_frames

    # Title at top
    font_title = get_font_bold(45)
    centered_text(draw, "30 UNIQUE DESIGNS", 30, font_title, CHARCOAL)

    # Scrolling cascade of prints - 3 columns scrolling up at different speeds
    pw, ph = 280, 350
    col_gap = 30
    total_col_w = 3 * pw + 2 * col_gap
    start_x = (VW - total_col_w) // 2

    # Column assignments
    cols = [
        [1, 4, 7, 10, 13, 16, 19, 22, 25, 28],
        [2, 5, 8, 11, 14, 17, 20, 23, 26, 29],
        [3, 6, 9, 12, 15, 18, 21, 24, 27, 30],
    ]

    speeds = [1.0, 1.3, 0.9]  # Different scroll speeds

    for col_idx in range(3):
        x = start_x + col_idx * (pw + col_gap)
        speed = speeds[col_idx]

        # Scroll offset
        scroll = progress * speed * (len(cols[col_idx]) * (ph + 20) - VH + 200)

        for print_idx, pnum in enumerate(cols[col_idx]):
            y = 100 + print_idx * (ph + 20) - int(scroll)

            # Only draw if visible
            if -ph < y < VH:
                thumb = THUMBS_LG[pnum]
                resized = thumb.resize((pw, ph), Image.LANCZOS)
                # Shadow
                draw.rectangle([x + 4, y + 4, x + pw + 4, y + ph + 4], fill=(200, 195, 185))
                # Frame
                draw.rectangle([x - 3, y - 3, x + pw + 3, y + ph + 3], fill=WHITE)
                img.paste(resized, (x, y))

    # Gradient overlay at top and bottom for smooth edge
    for i in range(80):
        alpha = i / 80
        c = tuple(int(CREAM[j] * (1 - alpha) + CREAM[j] * alpha) for j in range(3))
        # Only draw fading at very top
        draw.line([(0, i), (VW, i)], fill=CREAM)
        draw.line([(0, VH - i), (VW, VH - i)], fill=CREAM)

    return img


def render_scene_3(frame_in_scene, total_scene_frames):
    """Scene 3: Room mockup visualization."""
    img = Image.new('RGB', (VW, VH), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    progress = frame_in_scene / total_scene_frames

    # Wall texture
    for y in range(0, VH, 3):
        shade = 248 + (y % 6 == 0) * 2
        draw.line([(0, y), (VW, y)], fill=(shade, shade - 8, shade - 15))

    # "STYLED IN YOUR SPACE" text
    if progress > 0.05:
        alpha = min(1.0, (progress - 0.05) / 0.2)
        font_title = get_font_bold(48)
        c = tuple(int(WARM_CREAM[i] + (CHARCOAL[i] - WARM_CREAM[i]) * alpha) for i in range(3))
        centered_text(draw, "STYLED IN YOUR SPACE", 30, font_title, c)

    # Gallery wall - prints appearing one by one
    prints_layout = [
        (5, 120, 180, 240, 300),   # left
        (10, 410, 130, 280, 350),  # center top
        (16, 740, 180, 240, 300),  # right
        (3, 200, 560, 200, 250),   # bottom left
        (22, 650, 560, 200, 250),  # bottom right
    ]

    for i, (pnum, x, y, pw, ph) in enumerate(prints_layout):
        appear_time = 0.1 + i * 0.12
        if progress > appear_time:
            scale = min(1.0, (progress - appear_time) / 0.15)
            scale = ease_in_out(scale)

            cur_pw = int(pw * scale)
            cur_ph = int(ph * scale)
            cur_x = x + (pw - cur_pw) // 2
            cur_y = y + (ph - cur_ph) // 2

            if cur_pw > 10 and cur_ph > 10:
                # Frame
                frame_m = 8
                draw.rectangle([cur_x - frame_m + 3, cur_y - frame_m + 3,
                               cur_x + cur_pw + frame_m + 3, cur_y + cur_ph + frame_m + 3],
                              fill=(200, 190, 175))
                draw.rectangle([cur_x - frame_m, cur_y - frame_m,
                               cur_x + cur_pw + frame_m, cur_y + cur_ph + frame_m],
                              fill=WHITE)

                thumb = THUMBS_LG[pnum].resize((cur_pw, cur_ph), Image.LANCZOS)
                img.paste(thumb, (cur_x, cur_y))

    # Shelf
    if progress > 0.6:
        draw.rectangle([80, 870, VW - 80, 885], fill=(160, 130, 100))
        draw.rectangle([80, 885, VW - 80, 900], fill=(140, 110, 80))

    # Bottom text
    if progress > 0.7:
        font_note = get_font(32)
        centered_text(draw, "Perfect for any room in your home", 940, font_note, CHARCOAL)
        font_note2 = get_font_bold(28)
        centered_text(draw, "Print at home or at your local print shop", 990, font_note2, GOLD)

    return img


def render_scene_4(frame_in_scene, total_scene_frames):
    """Scene 4: CTA with price."""
    img = Image.new('RGB', (VW, VH), NAVY)
    draw = ImageDraw.Draw(img)

    progress = frame_in_scene / total_scene_frames

    # Border
    draw.rectangle([25, 25, VW - 25, VH - 25], outline=GOLD, width=2)

    # "30 Quote Prints Bundle"
    if progress > 0.05:
        alpha = min(1.0, (progress - 0.05) / 0.2)
        font_title = get_font_bold(65)
        c = tuple(int(NAVY[i] + (WHITE[i] - NAVY[i]) * alpha) for i in range(3))
        centered_text(draw, "30 QUOTE PRINTS", 120, font_title, c)
        font_sub = get_font(40)
        c2 = tuple(int(NAVY[i] + (GOLD[i] - NAVY[i]) * alpha) for i in range(3))
        centered_text(draw, "Wall Art Bundle", 210, font_sub, c2)

    # Mini print grid (2 rows of 5)
    if progress > 0.15:
        samples = [1, 5, 8, 10, 16, 22, 25, 28, 3, 17]
        pw, ph = 160, 200
        gap = 16
        total_w = 5 * pw + 4 * gap
        sx = (VW - total_w) // 2
        for idx, pnum in enumerate(samples):
            row = idx // 5
            col = idx % 5
            x = sx + col * (pw + gap)
            y = 310 + row * (ph + 16)
            thumb = THUMBS[pnum].resize((pw, ph), Image.LANCZOS)
            draw.rectangle([x - 2, y - 2, x + pw + 2, y + ph + 2], fill=WHITE)
            img.paste(thumb, (x, y))

    # Price
    if progress > 0.3:
        scale = min(1.0, (progress - 0.3) / 0.2)
        scale = ease_in_out(scale)
        font_price = get_font_bold(int(140 * scale))
        if font_price.size > 10:
            centered_text(draw, "$7.99", 770, font_price, WHITE)

    # "Instant Download"
    if progress > 0.45:
        font_inst = get_font_bold(42)
        centered_text(draw, "INSTANT DOWNLOAD", 930, font_inst, GOLD)

    # CTA button
    if progress > 0.55:
        btn_alpha = min(1.0, (progress - 0.55) / 0.15)
        btn_color = tuple(int(NAVY[i] + (TERRACOTTA[i] - NAVY[i]) * btn_alpha) for i in range(3))
        draw_rounded_rect(draw, (VW // 2 - 300, 1000, VW // 2 + 300, 1060), 15, fill=btn_color)
        font_cta = get_font_bold(36)
        centered_text(draw, "GET YOURS TODAY", 1010, font_cta, WHITE)

    return img


# ============================================================
# MP4 writer (raw MJPEG in MP4 container)
# ============================================================

def create_mp4_with_ffmpeg(frames_dir, output_path, fps=30):
    """Use ffmpeg to create MP4 from frame images."""
    import subprocess
    cmd = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'medium',
        '-crf', '23',
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def create_video():
    """Generate the complete promo video."""
    # Scene timing (in seconds)
    scenes = [
        (0, 3, render_scene_1),     # 0-3s: Title
        (3, 7, render_scene_2),     # 3-7s: Scrolling prints
        (7, 10, render_scene_3),    # 7-10s: Room mockup
        (10, 12, render_scene_4),   # 10-12s: CTA
    ]

    # Create temp directory for frames
    frames_dir = tempfile.mkdtemp()
    print(f"  Rendering {TOTAL_FRAMES} frames to temp directory...")

    for frame_num in range(TOTAL_FRAMES):
        current_time = frame_num / FPS

        # Find current scene
        for start, end, render_func in scenes:
            if start <= current_time < end:
                scene_duration = end - start
                scene_frames = int(scene_duration * FPS)
                frame_in_scene = int((current_time - start) * FPS)
                img = render_func(frame_in_scene, scene_frames)
                break
        else:
            # Last frame
            img = render_scene_4(FPS * 2 - 1, FPS * 2)

        # Save frame
        frame_path = os.path.join(frames_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")

        if frame_num % 30 == 0:
            print(f"    Frame {frame_num}/{TOTAL_FRAMES} ({current_time:.1f}s)")

    # Compile to MP4
    output_path = os.path.join(OUT, "promo_video.mp4")
    print(f"  Encoding MP4...")
    create_mp4_with_ffmpeg(frames_dir, output_path, FPS)

    # Clean up frames
    import shutil
    shutil.rmtree(frames_dir)

    return output_path


if __name__ == "__main__":
    print("Generating 12-second promo video (1080x1080, 30fps)...")
    path = create_video()
    print(f"\nVideo saved: {path}")

    # Verify
    size = os.path.getsize(path)
    print(f"File size: {size / 1024:.1f} KB")
    print("Video generation complete!")
