#!/usr/bin/env python3
"""
Create a 12-second 1080x1080 30fps promo video for the Social Media Templates Bundle.
4 scenes:
  Scene 1 (0-3s): Title reveal "50 Social Media Templates"
  Scene 2 (3-6s): Templates scrolling/fanning out
  Scene 3 (6-9s): Features showcase (3 sizes, editable, etc)
  Scene 4 (9-12s): CTA with price $12.99

Uses ffmpeg if available, GIF fallback otherwise.
"""

import os
import math
import subprocess
import tempfile
import shutil
from PIL import Image, ImageDraw, ImageFont

# === Color Palette ===
DUSTY_ROSE = (232, 196, 196)
CREAM = (255, 245, 238)
CHARCOAL = (51, 51, 51)
GOLD = (201, 169, 110)
WHITE = (255, 255, 255)
LIGHT_PINK = (245, 225, 225)
SOFT_GRAY = (180, 180, 180)
MEDIUM_ROSE = (220, 175, 175)
DARK_ROSE = (180, 140, 140)
LIGHT_GOLD = (220, 200, 160)

W, H = 1080, 1080
FPS = 30
DURATION = 12  # seconds
TOTAL_FRAMES = FPS * DURATION

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.dirname(OUTPUT_DIR), "templates")


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    if x1 - x0 < 2 * radius or y1 - y0 < 2 * radius:
        if x1 > x0 and y1 > y0:
            draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
        return
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_center_x(draw, text, font, canvas_width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    return (canvas_width - tw) // 2


def draw_text_centered(draw, text, y, font, fill, canvas_width):
    x = text_center_x(draw, text, font, canvas_width)
    draw.text((x, y), text, font=font, fill=fill)


def draw_corner_accents(draw, w, h, color=GOLD, size=60, thickness=3):
    m = 30
    draw.line([(m, m), (m + size, m)], fill=color, width=thickness)
    draw.line([(m, m), (m, m + size)], fill=color, width=thickness)
    draw.line([(w - m - size, m), (w - m, m)], fill=color, width=thickness)
    draw.line([(w - m, m), (w - m, m + size)], fill=color, width=thickness)
    draw.line([(m, h - m), (m + size, h - m)], fill=color, width=thickness)
    draw.line([(m, h - m - size), (m, h - m)], fill=color, width=thickness)
    draw.line([(w - m - size, h - m), (w - m, h - m)], fill=color, width=thickness)
    draw.line([(w - m, h - m - size), (w - m, h - m)], fill=color, width=thickness)


def draw_star(draw, cx, cy, outer_r, inner_r, points_count, fill):
    pts = []
    for i in range(points_count * 2):
        angle = math.pi * i / points_count - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
    draw.polygon(pts, fill=fill)


def ease_out(t):
    """Ease-out cubic."""
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    """Ease-in-out cubic."""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2


def load_template_thumbnails():
    """Load template thumbnails for Scene 2."""
    templates = []
    names = [
        "ig_post_quote_01.png", "ig_post_sale_06.png", "ig_post_tips_11.png",
        "ig_post_coming_soon_08.png", "ig_post_testimonial_21.png", "ig_post_freebie_24.png",
        "ig_post_aboutme_16.png", "ig_post_discount_10.png", "ig_story_quote_01.png",
        "ig_story_poll_09.png", "pin_tips_01.png", "pin_quote_05.png",
    ]
    for name in names:
        path = os.path.join(TEMPLATE_DIR, name)
        if os.path.exists(path):
            img = Image.open(path)
            templates.append(img)
    return templates


# ===========================================================================
# SCENE GENERATORS
# ===========================================================================

def render_scene1(frame_num, total_scene_frames):
    """Scene 1: Title reveal '50 Social Media Templates' (0-3s)."""
    t = frame_num / max(total_scene_frames - 1, 1)
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Background animation - expanding rose circle
    max_r = int(math.sqrt(W ** 2 + H ** 2) / 2)
    circle_r = int(max_r * ease_out(min(t * 1.5, 1.0)))
    cx, cy = W // 2, H // 2
    draw.ellipse([cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r], fill=DUSTY_ROSE)

    # Corner accents fade in
    if t > 0.3:
        draw_corner_accents(draw, W, H, GOLD, 60, 3)

    # Title text with slide-up animation
    font_big = get_font(72, bold=True)
    font_sub = get_font(44, bold=True)
    font_year = get_font(36)

    if t > 0.15:
        title_t = ease_out(min((t - 0.15) / 0.4, 1.0))
        offset = int(100 * (1 - title_t))
        alpha_sim = min(title_t * 1.5, 1.0)

        # "50" big number
        font_num = get_font(160, bold=True)
        draw_text_centered(draw, "50", H // 2 - 180 + offset, font_num, GOLD, W)

    if t > 0.35:
        sub_t = ease_out(min((t - 0.35) / 0.4, 1.0))
        offset2 = int(60 * (1 - sub_t))
        draw_text_centered(draw, "SOCIAL MEDIA", H // 2 + 20 + offset2, font_big, WHITE, W)
        draw_text_centered(draw, "TEMPLATES", H // 2 + 100 + offset2, font_big, CHARCOAL, W)

    if t > 0.55:
        year_t = ease_out(min((t - 0.55) / 0.3, 1.0))
        # Gold line
        line_w = int(400 * year_t)
        draw.rectangle([W // 2 - line_w // 2, H // 2 + 200, W // 2 + line_w // 2, H // 2 + 204], fill=GOLD)
        draw_text_centered(draw, "2026 EDITION", H // 2 + 220, font_year, DARK_ROSE, W)

    if t > 0.7:
        # Decorative stars
        for sx, sy in [(150, 200), (930, 200), (150, 880), (930, 880)]:
            draw_star(draw, sx, sy, 12, 6, 5, GOLD)

    return img


def render_scene2(frame_num, total_scene_frames, thumbnails):
    """Scene 2: Templates scrolling/fanning out (3-6s)."""
    t = frame_num / max(total_scene_frames - 1, 1)
    img = Image.new("RGB", (W, H), CHARCOAL)
    draw = ImageDraw.Draw(img)

    # Title at top
    font_title = get_font(38, bold=True)
    draw_text_centered(draw, "YOUR COMPLETE TEMPLATE COLLECTION", 30, font_title, GOLD, W)

    if not thumbnails:
        draw_text_centered(draw, "[Template previews]", H // 2, get_font(40), CREAM, W)
        return img

    # Fan out animation - templates spread from center
    num_cards = min(len(thumbnails), 8)
    card_w, card_h = 200, 200

    for i in range(num_cards):
        card_t = max(0, min((t - i * 0.05) / 0.6, 1.0))
        et = ease_out(card_t)

        # Fan arrangement
        angle_range = 60  # degrees total spread
        angle = -angle_range / 2 + (angle_range / (num_cards - 1)) * i
        angle_rad = math.radians(angle * et)

        # Position: start from center, fan outward
        center_x = W // 2
        center_y = H // 2 + 50
        radius = 320 * et
        x = int(center_x + radius * math.sin(angle_rad) - card_w // 2)
        y = int(center_y - radius * math.cos(angle_rad) * 0.4 + abs(angle) * 1.5 * et - card_h // 2)

        # Scale effect
        scale = 0.5 + 0.5 * et
        actual_w = int(card_w * scale)
        actual_h = int(card_h * scale)

        if actual_w > 0 and actual_h > 0 and i < len(thumbnails):
            thumb = thumbnails[i].resize((actual_w, actual_h), Image.LANCZOS)
            paste_x = x + (card_w - actual_w) // 2
            paste_y = y + (card_h - actual_h) // 2
            # Ensure within bounds
            paste_x = max(0, min(paste_x, W - actual_w))
            paste_y = max(0, min(paste_y, H - actual_h))
            img.paste(thumb, (paste_x, paste_y))
            draw = ImageDraw.Draw(img)

    # Scrolling row at bottom
    if t > 0.3:
        scroll_t = (t - 0.3) / 0.7
        row_y = H - 200
        scroll_offset = int(scroll_t * 600)
        thumb_size = 150
        gap = 20
        for i in range(len(thumbnails)):
            tx = -scroll_offset + i * (thumb_size + gap) + 50
            if -thumb_size < tx < W:
                if i < len(thumbnails):
                    thumb = thumbnails[i].resize((thumb_size, thumb_size), Image.LANCZOS)
                    ty = row_y
                    tx = max(0, min(tx, W - thumb_size))
                    img.paste(thumb, (tx, ty))
                    draw = ImageDraw.Draw(img)

    # Bottom label
    draw_rounded_rect(draw, (W // 4, H - 40, 3 * W // 4, H - 5), 10, fill=GOLD)
    draw_text_centered(draw, "50 UNIQUE DESIGNS", H - 37, get_font(24, bold=True), WHITE, W)

    return img


def render_scene3(frame_num, total_scene_frames):
    """Scene 3: Features showcase (6-9s)."""
    t = frame_num / max(total_scene_frames - 1, 1)
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 80], fill=DUSTY_ROSE)
    draw_text_centered(draw, "EVERYTHING YOU NEED", 18, get_font(40, bold=True), WHITE, W)

    features = [
        ("\u2713  25 Instagram Post Templates", "1080 x 1080 px"),
        ("\u2713  15 Instagram Story Templates", "1080 x 1920 px"),
        ("\u2713  10 Pinterest Pin Templates", "1000 x 1500 px"),
        ("\u2713  Modern Minimalist Design", "Dusty Rose Palette"),
        ("\u2713  Easy to Customize", "Works with Any Editor"),
        ("\u2713  Instant Digital Download", "Ready in Minutes"),
    ]

    font_feature = get_font(36, bold=True)
    font_detail = get_font(28)

    y_start = 130
    feature_h = 130

    for i, (feature, detail) in enumerate(features):
        # Stagger reveal
        reveal_t = max(0, min((t - i * 0.1) / 0.3, 1.0))
        et = ease_out(reveal_t)

        if et > 0:
            fy = y_start + i * feature_h
            # Slide in from left
            x_offset = int(200 * (1 - et))

            # Background bar
            bar_w = int((W - 100) * et)
            bg_color = LIGHT_PINK if i % 2 == 0 else WHITE
            draw_rounded_rect(draw, (50 - x_offset, fy, 50 + bar_w, fy + feature_h - 10), 15, fill=bg_color, outline=DUSTY_ROSE, width=1)

            # Check icon circle
            draw.ellipse([70 - x_offset, fy + 15, 110 - x_offset, fy + 55], fill=GOLD)

            draw.text((130 - x_offset, fy + 15), feature, font=font_feature, fill=CHARCOAL)
            draw.text((130 - x_offset, fy + 65), detail, font=font_detail, fill=DARK_ROSE)

    # Bottom summary badge
    if t > 0.7:
        badge_t = ease_out(min((t - 0.7) / 0.3, 1.0))
        badge_h = int(120 * badge_t)
        draw_rounded_rect(draw, (100, H - 50 - badge_h, W - 100, H - 50), 20, fill=CHARCOAL)
        if badge_t > 0.5:
            draw_text_centered(draw, "50 TEMPLATES \u2022 3 PLATFORMS \u2022 1 BRAND", H - 100, get_font(34, bold=True), GOLD, W)

    draw_corner_accents(draw, W, H, GOLD, 40, 2)

    return img


def render_scene4(frame_num, total_scene_frames):
    """Scene 4: CTA with price $12.99 (9-12s)."""
    t = frame_num / max(total_scene_frames - 1, 1)
    img = Image.new("RGB", (W, H), DUSTY_ROSE)
    draw = ImageDraw.Draw(img)

    draw_corner_accents(draw, W, H, GOLD, 60, 3)

    font_cta = get_font(52, bold=True)
    font_price = get_font(100, bold=True)
    font_sub = get_font(36)
    font_btn = get_font(40, bold=True)
    font_sm = get_font(28)

    # Title slides down
    if t > 0.05:
        title_t = ease_out(min((t - 0.05) / 0.3, 1.0))
        y_off = int(80 * (1 - title_t))
        draw_text_centered(draw, "GET YOURS TODAY!", 120 + y_off, font_cta, WHITE, W)

    # Price animation - zoom in
    if t > 0.2:
        price_t = ease_out(min((t - 0.2) / 0.35, 1.0))
        size = int(100 * price_t)
        if size > 10:
            price_font = get_font(size, bold=True)
            draw_text_centered(draw, "$12.99", H // 2 - 100, price_font, GOLD, W)

    # Strikethrough old price
    if t > 0.35:
        draw_text_centered(draw, "$39.99", H // 2 - 180, get_font(38), SOFT_GRAY, W)
        bbox = draw.textbbox((0, 0), "$39.99", font=get_font(38))
        tw = bbox[2] - bbox[0]
        sx = (W - tw) // 2
        draw.line([(sx - 5, H // 2 - 162), (sx + tw + 5, H // 2 - 162)], fill=SOFT_GRAY, width=2)

    # Savings badge
    if t > 0.4:
        badge_t = ease_out(min((t - 0.4) / 0.2, 1.0))
        bw = int(350 * badge_t)
        draw_rounded_rect(draw, (W // 2 - bw // 2, H // 2 + 30, W // 2 + bw // 2, H // 2 + 80), 25, fill=CHARCOAL)
        if badge_t > 0.7:
            draw_text_centered(draw, "SAVE 68%", H // 2 + 36, get_font(32, bold=True), GOLD, W)

    # CTA button with pulse
    if t > 0.5:
        btn_t = ease_out(min((t - 0.5) / 0.25, 1.0))
        # Pulse effect
        pulse = 1 + 0.03 * math.sin(t * 15)
        btn_w = int(500 * btn_t * pulse)
        btn_h = int(80 * btn_t)
        if btn_w > 20 and btn_h > 20:
            draw_rounded_rect(draw,
                              (W // 2 - btn_w // 2, H // 2 + 120, W // 2 + btn_w // 2, H // 2 + 120 + btn_h),
                              btn_h // 2, fill=WHITE)
            if btn_t > 0.6:
                draw_text_centered(draw, "ADD TO CART", H // 2 + 132, font_btn, DUSTY_ROSE, W)

    # Bottom features
    if t > 0.6:
        feat_t = ease_out(min((t - 0.6) / 0.25, 1.0))
        if feat_t > 0.5:
            items = ["Instant Download", "Lifetime Access", "Commercial Use"]
            for i, item in enumerate(items):
                ix = 120 + i * 320
                draw.text((ix, H - 160), f"\u2713 {item}", font=font_sm, fill=WHITE)

    # Stars decorations
    if t > 0.7:
        for sx, sy in [(100, 300), (980, 300), (100, 780), (980, 780)]:
            draw_star(draw, sx, sy, 15, 7, 5, GOLD)

    # Final flash / emphasis
    if t > 0.85:
        draw.rectangle([0, H - 80, W, H], fill=GOLD)
        draw_text_centered(draw, "50 Templates \u2022 $12.99 \u2022 Shop Now!", H - 60, get_font(30, bold=True), WHITE, W)

    return img


# ===========================================================================
# MAIN VIDEO GENERATION
# ===========================================================================

def generate_video():
    """Generate the 12-second promo video."""
    print(f"Generating {DURATION}s video at {FPS}fps ({TOTAL_FRAMES} frames)...")
    print(f"Resolution: {W}x{H}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Load template thumbnails for scene 2
    print("Loading template thumbnails...")
    thumbnails = load_template_thumbnails()
    print(f"  Loaded {len(thumbnails)} template thumbnails")

    # Scene frame ranges
    scene_frames = FPS * 3  # 3 seconds each
    scenes = [
        (0, scene_frames, "Scene 1: Title Reveal"),
        (scene_frames, 2 * scene_frames, "Scene 2: Template Fan"),
        (2 * scene_frames, 3 * scene_frames, "Scene 3: Features"),
        (3 * scene_frames, 4 * scene_frames, "Scene 4: CTA"),
    ]

    # Check if ffmpeg is available
    has_ffmpeg = False
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        has_ffmpeg = result.returncode == 0
    except FileNotFoundError:
        pass

    if has_ffmpeg:
        print("Using ffmpeg for MP4 output...")
        _generate_mp4(scenes, scene_frames, thumbnails)
    else:
        print("ffmpeg not found. Generating GIF fallback...")
        _generate_gif(scenes, scene_frames, thumbnails)


def _generate_mp4(scenes, scene_frames, thumbnails):
    """Generate MP4 using ffmpeg."""
    tmpdir = tempfile.mkdtemp(prefix="social_video_")

    try:
        print("Rendering frames...")
        for frame_num in range(TOTAL_FRAMES):
            # Determine which scene
            if frame_num < scene_frames:
                img = render_scene1(frame_num, scene_frames)
                scene_label = 1
            elif frame_num < 2 * scene_frames:
                img = render_scene2(frame_num - scene_frames, scene_frames, thumbnails)
                scene_label = 2
            elif frame_num < 3 * scene_frames:
                img = render_scene3(frame_num - 2 * scene_frames, scene_frames)
                scene_label = 3
            else:
                img = render_scene4(frame_num - 3 * scene_frames, scene_frames)
                scene_label = 4

            frame_path = os.path.join(tmpdir, f"frame_{frame_num:04d}.png")
            img.save(frame_path, "PNG")

            if frame_num % 30 == 0:
                print(f"  Frame {frame_num}/{TOTAL_FRAMES} (Scene {scene_label})")

        print(f"\nEncoding MP4 with ffmpeg...")
        output_path = os.path.join(OUTPUT_DIR, "promo_video.mp4")

        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(tmpdir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "medium",
            "-movflags", "+faststart",
            output_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  Created: promo_video.mp4 ({size_mb:.1f} MB)")
        else:
            print(f"  ffmpeg error: {result.stderr[:500]}")
            # Fallback to GIF
            print("  Falling back to GIF...")
            _generate_gif_from_frames(tmpdir)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _generate_gif(scenes, scene_frames, thumbnails):
    """Generate GIF fallback (lower frame rate for file size)."""
    gif_fps = 10
    gif_step = FPS // gif_fps
    frames = []

    print("Rendering frames for GIF...")
    for frame_num in range(0, TOTAL_FRAMES, gif_step):
        if frame_num < scene_frames:
            img = render_scene1(frame_num, scene_frames)
        elif frame_num < 2 * scene_frames:
            img = render_scene2(frame_num - scene_frames, scene_frames, thumbnails)
        elif frame_num < 3 * scene_frames:
            img = render_scene3(frame_num - 2 * scene_frames, scene_frames)
        else:
            img = render_scene4(frame_num - 3 * scene_frames, scene_frames)

        # Resize for GIF
        gif_img = img.resize((540, 540), Image.LANCZOS)
        frames.append(gif_img)

        if frame_num % 30 == 0:
            print(f"  Frame {frame_num}/{TOTAL_FRAMES}")

    output_path = os.path.join(OUTPUT_DIR, "promo_video.gif")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // gif_fps,
        loop=0,
        optimize=True,
    )
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Created: promo_video.gif ({size_mb:.1f} MB)")


def _generate_gif_from_frames(tmpdir):
    """Generate GIF from already-rendered frames."""
    frames = []
    gif_step = 3
    frame_num = 0
    while True:
        path = os.path.join(tmpdir, f"frame_{frame_num:04d}.png")
        if not os.path.exists(path):
            break
        if frame_num % gif_step == 0:
            img = Image.open(path).resize((540, 540), Image.LANCZOS)
            frames.append(img)
        frame_num += 1

    if frames:
        output_path = os.path.join(OUTPUT_DIR, "promo_video.gif")
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Created: promo_video.gif ({size_mb:.1f} MB)")


if __name__ == "__main__":
    generate_video()
    print("\nDone!")
