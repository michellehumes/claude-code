#!/usr/bin/env python3
"""Generate a 12-second 1080x1080 30fps promo video for the Resume Template Bundle."""

from PIL import Image, ImageDraw, ImageFont
import subprocess
import os
import math
import tempfile
import shutil

# --- Constants ---
W, H = 1080, 1080
FPS = 30
DURATION = 12  # seconds
TOTAL_FRAMES = FPS * DURATION
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), "templates")

# Color palette
NAVY = (27, 42, 74)
SLATE = (74, 111, 165)
LIGHT_GRAY = (240, 242, 245)
WHITE = (255, 255, 255)
GOLD = (201, 169, 110)
CHARCOAL = (51, 51, 51)
DARK_NAVY = (15, 25, 50)


def get_font(size, bold=False):
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


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def centered_text(draw, y, text, font, fill):
    tw = text_width(draw, text, font)
    draw.text(((W - tw) // 2, y), text, fill=fill, font=font)


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


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def lerp(a, b, t):
    return a + (b - a) * t


def load_template_thumbnails(target_h=400):
    """Load all 10 resume templates as thumbnails."""
    thumbs = []
    names = [
        "resume_01_classic.png", "resume_02_modern.png", "resume_03_creative.png",
        "resume_04_minimalist.png", "resume_05_executive.png", "resume_06_tech.png",
        "resume_07_elegant.png", "resume_08_bold.png", "resume_09_academic.png",
        "resume_10_compact.png",
    ]
    for name in names:
        path = os.path.join(TEMPLATES_DIR, name)
        if os.path.exists(path):
            t = Image.open(path)
            ratio = target_h / t.height
            new_w = int(t.width * ratio)
            t = t.resize((new_w, target_h), Image.LANCZOS)
            thumbs.append(t)
    return thumbs


# Scene timing (in seconds)
SCENE_1_END = 3.0    # Title: 0-3
SCENE_2_END = 7.0    # Cascade: 3-7
SCENE_3_END = 10.0   # Features: 7-10
SCENE_4_END = 12.0   # CTA: 10-12

# Pre-load templates
THUMBS = None


def get_thumbs():
    global THUMBS
    if THUMBS is None:
        THUMBS = load_template_thumbnails(target_h=500)
    return THUMBS


def render_scene_1(draw, img, t, frame):
    """Scene 1: '10 Professional Resume Templates' title (0-3s)."""
    # Background
    draw.rectangle([0, 0, W, H], fill=NAVY)

    # Gold border animation
    border_progress = min(1.0, t / 1.0)
    bp = ease_out_cubic(border_progress)
    border_len = int(bp * (2 * W + 2 * H))

    # Draw animated gold border
    if border_len > 0:
        points = []
        total_perim = 2 * W + 2 * H
        remaining = border_len
        # Top edge
        seg = min(remaining, W)
        if seg > 0:
            draw.line([(30, 30), (30 + seg, 30)], fill=GOLD, width=4)
        remaining -= seg
        # Right edge
        if remaining > 0:
            seg = min(remaining, H)
            draw.line([(W - 30, 30), (W - 30, 30 + seg)], fill=GOLD, width=4)
            remaining -= seg
        # Bottom edge
        if remaining > 0:
            seg = min(remaining, W)
            draw.line([(W - 30, H - 30), (W - 30 - seg, H - 30)], fill=GOLD, width=4)
            remaining -= seg
        # Left edge
        if remaining > 0:
            seg = min(remaining, H)
            draw.line([(30, H - 30), (30, H - 30 - seg)], fill=GOLD, width=4)

    # Number "10" - large, fade/scale in
    fade = min(1.0, t / 0.8)
    alpha = int(255 * ease_out_cubic(fade))
    num_font = get_font(180, bold=True)
    num_text = "10"

    if t < 1.5:
        centered_text(draw, 200, num_text, num_font, GOLD)
    else:
        # Slide up
        slide_t = min(1.0, (t - 1.5) / 0.5)
        ny = int(lerp(200, 100, ease_out_cubic(slide_t)))
        centered_text(draw, ny, num_text, num_font, GOLD)

    # Title text - appear after number
    if t > 0.8:
        title_fade = min(1.0, (t - 0.8) / 0.6)
        title_font = get_font(58, bold=True)

        if t < 1.5:
            centered_text(draw, 420, "PROFESSIONAL", title_font, WHITE)
        else:
            slide_t = min(1.0, (t - 1.5) / 0.5)
            ty = int(lerp(420, 320, ease_out_cubic(slide_t)))
            centered_text(draw, ty, "PROFESSIONAL", title_font, WHITE)

    if t > 1.2:
        sub_font = get_font(58, bold=True)
        if t < 1.5:
            centered_text(draw, 500, "RESUME TEMPLATES", sub_font, WHITE)
        else:
            slide_t = min(1.0, (t - 1.5) / 0.5)
            ty = int(lerp(500, 400, ease_out_cubic(slide_t)))
            centered_text(draw, ty, "RESUME TEMPLATES", sub_font, WHITE)

    # Subtitle appears later
    if t > 2.0:
        desc_font = get_font(36)
        fade_t = min(1.0, (t - 2.0) / 0.5)
        centered_text(draw, 520, "for Every Career Stage", desc_font, LIGHT_GRAY)

    # Decorative lines
    if t > 1.5:
        line_t = min(1.0, (t - 1.5) / 0.5)
        line_w = int(300 * ease_out_cubic(line_t))
        mid = W // 2
        draw.line([(mid - line_w, 490), (mid + line_w, 490)], fill=GOLD, width=2)


def render_scene_2(draw, img, t, frame):
    """Scene 2: Resumes flip/cascade through (3-7s)."""
    draw.rectangle([0, 0, W, H], fill=NAVY)

    # Subtle background pattern
    for i in range(0, W, 60):
        draw.line([(i, 0), (i, H)], fill=(30, 48, 82), width=1)

    thumbs = get_thumbs()
    if not thumbs:
        centered_text(draw, H // 2, "10 Templates", get_font(60, bold=True), WHITE)
        return

    scene_duration = SCENE_2_END - SCENE_1_END  # 4 seconds
    local_t = t  # 0 to 4

    # Cascade effect: each template slides in from the right
    thumb_w = thumbs[0].width
    thumb_h = thumbs[0].height

    # Display templates one by one with overlap
    templates_per_sec = 10 / scene_duration  # Show all 10 over 4 seconds
    visible_count = min(10, int(local_t * templates_per_sec) + 1)

    # Calculate positions for fan effect
    for i in range(visible_count):
        appear_time = i / templates_per_sec
        if local_t < appear_time:
            continue

        elapsed = local_t - appear_time
        slide_progress = min(1.0, elapsed / 0.4)
        sp = ease_out_cubic(slide_progress)

        # Fan out from right side, each slightly offset
        target_x = 100 + i * 85
        start_x = W + 50
        x = int(lerp(start_x, target_x, sp))

        # Slight y offset for depth
        y = 150 + i * 8

        # Scale effect - newer ones slightly larger
        scale = 0.85 + (i / 10) * 0.15
        sw = int(thumb_w * scale * 0.55)
        sh = int(thumb_h * scale * 0.55)

        if i < len(thumbs):
            resized = thumbs[i].resize((sw, sh), Image.LANCZOS)
            # Shadow
            draw.rectangle([x + 4, y + 4, x + sw + 4, y + sh + 4], fill=DARK_NAVY)
            img.paste(resized, (x, y))

    # Title at bottom
    title_font = get_font(42, bold=True)
    draw_rounded_rect(draw, (W // 2 - 300, H - 150, W // 2 + 300, H - 70), 15, GOLD)
    centered_text(draw, H - 140, "10 UNIQUE DESIGNS", title_font, NAVY)

    # Template name label
    if visible_count > 0:
        names = ["Classic", "Modern", "Creative", "Minimalist", "Executive",
                 "Tech", "Elegant", "Bold", "Academic", "Compact"]
        current_idx = min(visible_count - 1, 9)
        name_font = get_font(32, bold=True)
        centered_text(draw, H - 55, names[current_idx], name_font, WHITE)


def render_scene_3(draw, img, t, frame):
    """Scene 3: Features (ATS-friendly, print-ready, editable) (7-10s)."""
    draw.rectangle([0, 0, W, H], fill=NAVY)

    # Show a small grid of templates on the left
    thumbs = get_thumbs()
    if thumbs:
        small_h = 200
        for i in range(5):
            ratio = small_h / thumbs[i].height
            sw = int(thumbs[i].width * ratio)
            small = thumbs[i].resize((sw, small_h), Image.LANCZOS)
            x = 40 + (i % 3) * (sw + 10)
            y = 40 + (i // 3) * (small_h + 10)
            img.paste(small, (x, y))

    # Features appear one by one
    features = [
        ("\u2713  ATS-Friendly Format", "Passes automated screening"),
        ("\u2713  Print-Ready 300 DPI", "Professional quality output"),
        ("\u2713  Easy to Customize", "Word & Google Docs compatible"),
        ("\u2713  10 Unique Designs", "One for every career stage"),
        ("\u2713  Instant Download", "Start editing right away"),
    ]

    feat_title_font = get_font(44, bold=True)
    feat_desc_font = get_font(30)

    scene_duration = SCENE_3_END - SCENE_2_END  # 3 seconds
    features_area_y = 500
    feature_spacing = 105

    for i, (title, desc) in enumerate(features):
        appear_time = i * (scene_duration / len(features))
        if t < appear_time:
            continue

        elapsed = t - appear_time
        slide_progress = min(1.0, elapsed / 0.4)
        sp = ease_out_cubic(slide_progress)

        x_start = W + 50
        x_target = 120
        x = int(lerp(x_start, x_target, sp))
        y = features_area_y + i * feature_spacing

        # Feature card
        draw_rounded_rect(draw, (x - 10, y - 5, x + 850, y + 85), 12, (35, 55, 95))
        draw.text((x + 10, y + 5), title, fill=GOLD, font=feat_title_font)
        draw.text((x + 10, y + 52), desc, fill=LIGHT_GRAY, font=feat_desc_font)

    # Header
    header_font = get_font(54, bold=True)
    centered_text(draw, 480, "KEY FEATURES", header_font, GOLD)
    draw.line([(200, 475), (W - 200, 475)], fill=GOLD, width=2)


def render_scene_4(draw, img, t, frame):
    """Scene 4: CTA $8.99 (10-12s)."""
    draw.rectangle([0, 0, W, H], fill=NAVY)

    # Gold border
    draw.rectangle([25, 25, W - 25, H - 25], outline=GOLD, width=3)

    # Pulsing effect for urgency
    pulse = 0.95 + 0.05 * math.sin(t * 4 * math.pi)

    scene_duration = SCENE_4_END - SCENE_3_END  # 2 seconds

    # Title fade in
    fade = min(1.0, t / 0.5)
    title_font = get_font(52, bold=True)
    centered_text(draw, 120, "PROFESSIONAL RESUME", title_font, WHITE)
    centered_text(draw, 190, "TEMPLATE BUNDLE", title_font, GOLD)

    # Features summary
    if t > 0.3:
        feat_font = get_font(36)
        centered_text(draw, 310, "10 Templates  |  ATS-Friendly  |  Print-Ready", feat_font, LIGHT_GRAY)

    # Price - big and bold
    if t > 0.5:
        price_fade = min(1.0, (t - 0.5) / 0.3)

        # Was price
        was_font = get_font(36)
        centered_text(draw, 420, "Value: $49.99", was_font, (120, 120, 140))
        tw = text_width(draw, "Value: $49.99", was_font)
        sx = (W - tw) // 2
        draw.line([(sx, 440), (sx + tw, 440)], fill=(120, 120, 140), width=2)

        # Current price
        price_font = get_font(120, bold=True)
        centered_text(draw, 480, "$8.99", price_font, GOLD)

        # Save badge
        save_font = get_font(38, bold=True)
        bw = int(220 * pulse)
        bh = int(50 * pulse)
        draw_rounded_rect(draw, (W // 2 - bw, 640, W // 2 + bw, 640 + bh * 2), 15, GOLD)
        centered_text(draw, 650, "SAVE 82%!", save_font, NAVY)

    # CTA Button
    if t > 1.0:
        btn_scale = min(1.0, (t - 1.0) / 0.3)
        bs = ease_out_cubic(btn_scale)
        btn_w = int(380 * bs)
        btn_h = int(45 * bs)
        draw_rounded_rect(draw, (W // 2 - btn_w, 790, W // 2 + btn_w, 790 + btn_h * 2), 20, WHITE)
        if bs > 0.5:
            cta_font = get_font(48, bold=True)
            centered_text(draw, 800, "ADD TO CART", cta_font, NAVY)

    # Bottom text
    if t > 1.2:
        small_font = get_font(30)
        centered_text(draw, 930, "Instant Download  |  30-Day Guarantee", small_font, LIGHT_GRAY)
        centered_text(draw, 975, "Word & Google Docs Compatible", small_font, GOLD)


def render_frame(frame_num):
    """Render a single frame."""
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    t_global = frame_num / FPS  # Global time in seconds

    if t_global < SCENE_1_END:
        render_scene_1(draw, img, t_global, frame_num)
    elif t_global < SCENE_2_END:
        render_scene_2(draw, img, t_global - SCENE_1_END, frame_num)
    elif t_global < SCENE_3_END:
        render_scene_3(draw, img, t_global - SCENE_2_END, frame_num)
    else:
        render_scene_4(draw, img, t_global - SCENE_3_END, frame_num)

    return img


def main():
    print("Generating promo video frames...")

    # Create temp directory for frames
    temp_dir = tempfile.mkdtemp(prefix="resume_video_")

    try:
        # Render all frames
        for i in range(TOTAL_FRAMES):
            frame = render_frame(i)
            frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
            frame.save(frame_path, "PNG")

            if (i + 1) % 30 == 0:
                print(f"  Rendered {i + 1}/{TOTAL_FRAMES} frames ({(i + 1) / TOTAL_FRAMES * 100:.0f}%)")

        # Encode video with ffmpeg
        output_path = os.path.join(OUTPUT_DIR, "promo_video.mp4")
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(temp_dir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "23",
            "-movflags", "+faststart",
            output_path,
        ]

        print("  Encoding video with ffmpeg...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ffmpeg error: {result.stderr}")
        else:
            print(f"  Video saved to: {output_path}")
            # Get file size
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  File size: {size_mb:.1f} MB")

    finally:
        # Cleanup temp frames
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("  Cleaned up temp files.")

    print("Done! Promo video created.")


if __name__ == "__main__":
    main()
