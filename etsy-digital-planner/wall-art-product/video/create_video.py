#!/usr/bin/env python3
"""
Create a 12-second Etsy listing video for "Minimalist Abstract Gallery Wall Art Set of 6".
1920x1080 @ 30fps, MP4, no audio.

Video structure (360 frames total):
  Frames   0-60  (2s): Title reveal with fade-in
  Frames  61-120 (2s): Prints 1+2 side by side, slide in from edges
  Frames 121-180 (2s): Prints 3+4 side by side, slide in from edges
  Frames 181-240 (2s): Prints 5+6 side by side, slide in from edges
  Frames 241-300 (2s): All 6 prints gallery wall arrangement
  Frames 301-360 (2s): CTA screen
"""

import os
import sys
import shutil
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
W, H = 1920, 1080
FPS = 30
TOTAL_FRAMES = 360

# Colour palette
CREAM       = (252, 248, 240)
WARM_SAND   = (228, 213, 193)
SOFT_TERRA  = (199, 159, 134)
MUTED_SAGE  = (173, 188, 168)
DUSTY_CLAY  = (189, 149, 130)
CHARCOAL    = (62,  58,  55)

# Paths
PRINTS_DIR = "/home/user/claude-code/etsy-digital-planner/wall-art-product/prints"
VIDEO_DIR  = "/home/user/claude-code/etsy-digital-planner/wall-art-product/video"
OUTPUT_MP4 = os.path.join(VIDEO_DIR, "etsy_listing_video.mp4")

PRINT_FILES = [
    "print_01_horizon.png",
    "print_02_botanical_line.png",
    "print_03_arches.png",
    "print_04_orbs.png",
    "print_05_figure_line.png",
    "print_06_brushstrokes.png",
]

FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_prints():
    """Load all 6 prints and return as list of PIL Images."""
    imgs = []
    for fname in PRINT_FILES:
        path = os.path.join(PRINTS_DIR, fname)
        img = Image.open(path).convert("RGB")
        imgs.append(img)
    return imgs


def make_thumbnail(img, max_w, max_h):
    """Resize an image to fit within max_w x max_h, preserving aspect ratio."""
    thumb = img.copy()
    thumb.thumbnail((max_w, max_h), Image.LANCZOS)
    return thumb


def add_frame_border(img, border=6, color=CHARCOAL):
    """Add a picture-frame border around an image with mat and subtle shadow."""
    w, h = img.size
    mat = 10
    shadow_offset = 5
    # Total size: image + mat on each side + border on each side + shadow
    total_w = w + (mat + border) * 2 + shadow_offset
    total_h = h + (mat + border) * 2 + shadow_offset
    framed = Image.new("RGB", (total_w, total_h), CREAM)
    draw = ImageDraw.Draw(framed)

    # Shadow
    sx = border + mat + shadow_offset
    sy = border + mat + shadow_offset
    draw.rectangle(
        [sx, sy, sx + w + (mat + border) * 2 - 1, sy + h + (mat + border) * 2 - 1],
        fill=(210, 205, 195),
    )

    # Outer frame rectangle
    fx, fy = 0, 0
    draw.rectangle(
        [fx, fy, fx + w + (mat + border) * 2 - 1, fy + h + (mat + border) * 2 - 1],
        fill=color,
    )

    # White mat
    draw.rectangle(
        [fx + border, fy + border,
         fx + border + w + mat * 2 - 1, fy + border + h + mat * 2 - 1],
        fill=(255, 255, 255),
    )

    # Paste the image
    framed.paste(img, (border + mat, border + mat))
    return framed


def ease_in_out(t):
    """Smooth ease-in-out (cubic)."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def lerp(a, b, t):
    """Linear interpolation."""
    return a + (b - a) * t


def color_lerp(c1, c2, t):
    """Interpolate between two RGB colours."""
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


# ---------------------------------------------------------------------------
# Scene renderers  (each returns an RGB PIL Image of size W x H)
# ---------------------------------------------------------------------------

def render_title(frame_idx):
    """Frames 0-60: Title reveal with fade-in and accent bars."""
    img = Image.new("RGBA", (W, H), (*CREAM, 255))
    draw = ImageDraw.Draw(img)

    # Progress 0..1 over the 61 frames
    t = min(frame_idx / 50, 1.0)
    alpha = int(255 * ease_in_out(t))

    # Accent bar top (expands from centre)
    bar_w = int(lerp(0, 260, ease_in_out(min(t * 1.3, 1.0))))
    draw.rectangle(
        [W // 2 - bar_w // 2, 310, W // 2 + bar_w // 2, 318],
        fill=(*SOFT_TERRA, alpha),
    )

    # Title text
    font_title = ImageFont.truetype(FONT_SERIF_BOLD, 82)
    font_sub   = ImageFont.truetype(FONT_REG, 42)

    title1 = "Serene Neutrals"
    title2 = "Gallery Wall Art Set"

    # Measure text
    bb1 = draw.textbbox((0, 0), title1, font=font_title)
    tw1 = bb1[2] - bb1[0]
    bb2 = draw.textbbox((0, 0), title2, font=font_sub)
    tw2 = bb2[2] - bb2[0]

    x1 = (W - tw1) // 2
    y1 = 350
    draw.text((x1, y1), title1, fill=(*CHARCOAL, alpha), font=font_title)

    x2 = (W - tw2) // 2
    y2 = 465
    draw.text((x2, y2), title2, fill=(*DUSTY_CLAY, alpha), font=font_sub)

    # Lower accent bar (sage)
    draw.rectangle(
        [W // 2 - bar_w // 2, 535, W // 2 + bar_w // 2, 543],
        fill=(*MUTED_SAGE, alpha),
    )

    # Small diamond ornament
    if t > 0.3:
        orn_alpha = int(255 * ease_in_out(min((t - 0.3) / 0.7, 1.0)))
        cx, cy = W // 2, 575
        sz = 8
        draw.polygon(
            [(cx, cy - sz), (cx + sz, cy), (cx, cy + sz), (cx - sz, cy)],
            fill=(*SOFT_TERRA, orn_alpha),
        )

    return img.convert("RGB")


def render_pair(frame_idx, local_frame, print_a, print_b):
    """Frames showing two prints sliding in from the sides."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Thumbnail size for 2-up display
    thumb_h = 560
    thumb_w = int(thumb_h * (2 / 3))  # 2:3 aspect ratio

    ta = make_thumbnail(print_a, thumb_w, thumb_h)
    tb = make_thumbnail(print_b, thumb_w, thumb_h)
    fa = add_frame_border(ta, border=6, color=CHARCOAL)
    fb = add_frame_border(tb, border=6, color=CHARCOAL)

    fw, fh = fa.size

    # Target positions: centred, with gap
    gap = 100
    left_x  = W // 2 - gap // 2 - fw
    right_x = W // 2 + gap // 2
    y_pos   = (H - fh) // 2 + 10

    # Slide animation (first 25 frames of the segment)
    slide_t = min(local_frame / 20, 1.0)
    ease = ease_in_out(slide_t)

    cur_left_x  = int(lerp(-fw, left_x, ease))
    cur_right_x = int(lerp(W, right_x, ease))

    img.paste(fa, (cur_left_x, y_pos))
    img.paste(fb, (cur_right_x, y_pos))

    # Subtle decorative line at bottom
    if slide_t > 0.5:
        line_t = ease_in_out(min((slide_t - 0.5) / 0.5, 1.0))
        c = color_lerp(CREAM, DUSTY_CLAY, line_t)
        line_w = int(160 * line_t)
        lx = (W - line_w) // 2
        ly = H - 70
        draw.line([(lx, ly), (lx + line_w, ly)], fill=c, width=2)

    return img


def render_gallery(frame_idx, local_frame, prints_list):
    """Frames 241-300: All 6 prints in a gallery wall arrangement (2 rows x 3 cols)."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Gallery heading
    fade_t = min(local_frame / 20, 1.0)
    ease = ease_in_out(fade_t)

    font_heading = ImageFont.truetype(FONT_SERIF_BOLD, 36)
    heading = "Your Gallery Wall Collection"
    bb = draw.textbbox((0, 0), heading, font=font_heading)
    tw = bb[2] - bb[0]
    hx = (W - tw) // 2

    c_head = color_lerp(CREAM, CHARCOAL, ease)
    draw.text((hx, 40), heading, fill=c_head, font=font_heading)

    # Accent line under heading
    bar_w = int(120 * ease)
    bar_c = color_lerp(CREAM, SOFT_TERRA, ease)
    draw.rectangle(
        [W // 2 - bar_w // 2, 90, W // 2 + bar_w // 2, 94],
        fill=bar_c,
    )

    # Thumbnail sizes for 6-up grid
    thumb_h = 340
    thumb_w = int(thumb_h * (2 / 3))

    cols, rows = 3, 2
    gap_x, gap_y = 50, 40

    # Pre-compute framed sizes to determine grid layout
    sample_thumb = make_thumbnail(prints_list[0], thumb_w, thumb_h)
    sample_framed = add_frame_border(sample_thumb, border=5, color=CHARCOAL)
    sfw, sfh = sample_framed.size

    total_w = cols * sfw + (cols - 1) * gap_x
    total_h = rows * sfh + (rows - 1) * gap_y
    start_x = (W - total_w) // 2
    start_y = 120 + (H - 120 - total_h) // 2

    for idx, pr in enumerate(prints_list):
        col = idx % cols
        row = idx // cols

        # Staggered fade-in
        delay = idx * 3
        item_t = min(max(local_frame - delay, 0) / 18, 1.0)
        item_ease = ease_in_out(item_t)

        if item_ease < 0.01:
            continue

        thumb = make_thumbnail(pr, thumb_w, thumb_h)
        framed = add_frame_border(thumb, border=5, color=CHARCOAL)
        fw, fh = framed.size

        tx = start_x + col * (sfw + gap_x)
        target_y = start_y + row * (sfh + gap_y)
        ty = int(lerp(target_y + 30, target_y, item_ease))

        # Fade by blending with cream background
        overlay = Image.new("RGB", framed.size, CREAM)
        blended = Image.blend(overlay, framed, item_ease)
        img.paste(blended, (tx, ty))

    return img


def render_cta(frame_idx, local_frame):
    """Frames 301-360: CTA screen."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    t = min(local_frame / 25, 1.0)
    ease = ease_in_out(t)

    # Terracotta accent block at top and bottom
    block_h = int(lerp(0, 8, ease))
    draw.rectangle([0, 0, W, block_h], fill=SOFT_TERRA)
    draw.rectangle([0, H - block_h, W, H], fill=SOFT_TERRA)

    # Central decorative frame
    frame_margin = int(lerp(W // 2, 140, ease))
    frame_top = int(lerp(H // 2, 180, ease))
    frame_bot = int(lerp(H // 2, H - 180, ease))
    if frame_margin < W // 2 - 10:
        draw.rectangle(
            [frame_margin, frame_top, W - frame_margin, frame_bot],
            outline=WARM_SAND, width=2,
        )

    # Main CTA text
    font_big = ImageFont.truetype(FONT_SERIF_BOLD, 64)
    font_med = ImageFont.truetype(FONT_REG, 36)
    font_sm  = ImageFont.truetype(FONT_REG, 28)

    # "Set of 6"
    line1 = "Set of 6"
    bb1 = draw.textbbox((0, 0), line1, font=font_big)
    tw1 = bb1[2] - bb1[0]
    c1 = color_lerp(CREAM, CHARCOAL, ease)
    draw.text(((W - tw1) // 2, 290), line1, fill=c1, font=font_big)

    # Decorative separator
    sep_w = int(180 * ease)
    sep_y = 380
    sep_c = color_lerp(CREAM, SOFT_TERRA, ease)
    draw.rectangle(
        [W // 2 - sep_w // 2, sep_y, W // 2 + sep_w // 2, sep_y + 3],
        fill=sep_c,
    )

    # "Instant Download"
    t2 = min(max(local_frame - 8, 0) / 20, 1.0)
    ease2 = ease_in_out(t2)
    line2 = "Instant Download"
    bb2 = draw.textbbox((0, 0), line2, font=font_med)
    tw2 = bb2[2] - bb2[0]
    c2 = color_lerp(CREAM, DUSTY_CLAY, ease2)
    draw.text(((W - tw2) // 2, 420), line2, fill=c2, font=font_med)

    # "7 Sizes Included"
    t3 = min(max(local_frame - 16, 0) / 20, 1.0)
    ease3 = ease_in_out(t3)
    line3 = "7 Sizes Included"
    bb3 = draw.textbbox((0, 0), line3, font=font_med)
    tw3 = bb3[2] - bb3[0]
    c3 = color_lerp(CREAM, DUSTY_CLAY, ease3)
    draw.text(((W - tw3) // 2, 480), line3, fill=c3, font=font_med)

    # Sage accent dots
    if ease > 0.6:
        dot_t = ease_in_out(min((ease - 0.6) / 0.4, 1.0))
        dot_c = color_lerp(CREAM, MUTED_SAGE, dot_t)
        for dx in [-60, 0, 60]:
            cx = W // 2 + dx
            cy = 560
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=dot_c)

    # Bottom tagline
    t4 = min(max(local_frame - 24, 0) / 20, 1.0)
    ease4 = ease_in_out(t4)
    tagline = "Printable Wall Art  \u2022  Modern Minimalist Design"
    bb4 = draw.textbbox((0, 0), tagline, font=font_sm)
    tw4 = bb4[2] - bb4[0]
    c4 = color_lerp(CREAM, CHARCOAL, ease4)
    draw.text(((W - tw4) // 2, 640), tagline, fill=c4, font=font_sm)

    return img


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading print images...")
    prints = load_prints()
    print(f"  Loaded {len(prints)} prints.")

    tmp_dir = tempfile.mkdtemp(prefix="etsy_video_frames_")
    print(f"Temporary frame directory: {tmp_dir}")

    try:
        for f_idx in range(TOTAL_FRAMES):
            if f_idx % 60 == 0:
                print(f"  Rendering frame {f_idx}/{TOTAL_FRAMES} ...")

            if f_idx <= 60:
                frame = render_title(f_idx)

            elif f_idx <= 120:
                local = f_idx - 61
                frame = render_pair(f_idx, local, prints[0], prints[1])

            elif f_idx <= 180:
                local = f_idx - 121
                frame = render_pair(f_idx, local, prints[2], prints[3])

            elif f_idx <= 240:
                local = f_idx - 181
                frame = render_pair(f_idx, local, prints[4], prints[5])

            elif f_idx <= 300:
                local = f_idx - 241
                frame = render_gallery(f_idx, local, prints)

            else:
                local = f_idx - 301
                frame = render_cta(f_idx, local)

            frame_path = os.path.join(tmp_dir, f"frame_{f_idx:04d}.png")
            frame.save(frame_path)

        print("All frames rendered. Encoding video with ffmpeg...")

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(tmp_dir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "18",
            "-an",
            OUTPUT_MP4,
        ]

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("ffmpeg STDERR:", result.stderr)
            sys.exit(1)

        file_size = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
        print(f"Video saved to: {OUTPUT_MP4}")
        print(f"File size: {file_size:.2f} MB")

    finally:
        print("Cleaning up temporary frames...")
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("Done!")


if __name__ == "__main__":
    main()
