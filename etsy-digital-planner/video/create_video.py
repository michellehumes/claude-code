#!/usr/bin/env python3
"""
Create an Etsy listing video for the 2026 Wellness & Productivity Digital Planner.

Etsy video specs:
- 5-15 seconds (we'll do ~12 seconds)
- 1080p minimum (we'll do 1920x1080)
- MP4 format
- No audio
- Under 100MB

Strategy: Animated slideshow with smooth transitions showing key planner features.
We'll create individual frames and combine with ffmpeg.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

OUTPUT_DIR = "/home/user/claude-code/etsy-digital-planner/video"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

# Colors
PATINA_BLUE = (126, 172, 176)
DEEP_TEAL = (62, 105, 110)
WARM_LINEN = (243, 237, 228)
SOFT_SAGE = (183, 203, 180)
DUSTY_ROSE = (210, 175, 170)
CHARCOAL = (55, 55, 60)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 218, 213)


def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()


def lerp_color(c1, c2, t):
    """Linearly interpolate between two colors."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def create_title_frame(frame_num, total_frames):
    """Opening title frame with animated elements."""
    img = Image.new('RGB', (W, H), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    # Accent bars sliding in from left
    progress = min(1.0, frame_num / (total_frames * 0.3))
    bar_w = int(W * progress)
    draw.rectangle([0, 0, bar_w, 6], fill=PATINA_BLUE)
    draw.rectangle([0, 6, bar_w, 10], fill=DUSTY_ROSE)
    draw.rectangle([0, 10, bar_w, 14], fill=SOFT_SAGE)

    # Bottom bars
    draw.rectangle([W - bar_w, H - 14, W, H - 8], fill=SOFT_SAGE)
    draw.rectangle([W - bar_w, H - 8, W, H - 4], fill=DUSTY_ROSE)
    draw.rectangle([W - bar_w, H - 4, W, H], fill=PATINA_BLUE)

    # Fade in text
    alpha = min(255, int(255 * min(1.0, frame_num / (total_frames * 0.4))))

    # Year
    year_y = 180 - int(30 * (1 - min(1.0, frame_num / (total_frames * 0.3))))
    draw.text((W // 2, year_y), "2026", fill=DEEP_TEAL, font=get_font(120, bold=True), anchor="mt")

    # Subtitle (appears slightly later)
    if frame_num > total_frames * 0.15:
        draw.text((W // 2, 320), "WELLNESS & PRODUCTIVITY", fill=CHARCOAL, font=get_font(36), anchor="mt")

    if frame_num > total_frames * 0.25:
        draw.text((W // 2, 380), "Digital Planner", fill=DEEP_TEAL, font=get_font(60, bold=True), anchor="mt")

    # Decorative line
    if frame_num > total_frames * 0.3:
        line_progress = min(1.0, (frame_num - total_frames * 0.3) / (total_frames * 0.2))
        line_w = int(200 * line_progress)
        draw.rectangle([W // 2 - line_w, 460, W // 2 + line_w, 463], fill=PATINA_BLUE)

    # Feature badges appearing one by one
    badges = ["GoodNotes", "Notability", "Xodo", "iPad"]
    badge_y = 520
    badge_w = 180
    gap = 20
    total_w = len(badges) * badge_w + (len(badges) - 1) * gap
    bx_start = (W - total_w) // 2

    for i, badge in enumerate(badges):
        delay = 0.35 + i * 0.1
        if frame_num > total_frames * delay:
            bx = bx_start + i * (badge_w + gap)
            draw.rounded_rectangle([bx, badge_y, bx + badge_w, badge_y + 45], radius=22, fill=DEEP_TEAL)
            draw.text((bx + badge_w // 2, badge_y + 8), badge, fill=WHITE, font=get_font(22), anchor="mt")

    # iPad mockup fading in from bottom
    if frame_num > total_frames * 0.2:
        mockup_progress = min(1.0, (frame_num - total_frames * 0.2) / (total_frames * 0.4))
        ipad_y = int(620 + 50 * (1 - mockup_progress))
        ipad_w, ipad_h = 700, 520

        ipad_x = (W - ipad_w) // 2
        # iPad body
        draw.rounded_rectangle([ipad_x, ipad_y, ipad_x + ipad_w, ipad_y + ipad_h],
                               radius=15, fill=(40, 40, 42))
        # Screen
        bezel = 12
        draw.rectangle([ipad_x + bezel, ipad_y + bezel,
                        ipad_x + ipad_w - bezel, ipad_y + ipad_h - bezel], fill=WARM_LINEN)

        # Mini planner preview on screen
        sx = ipad_x + bezel
        sy = ipad_y + bezel
        ssw = ipad_w - 2 * bezel
        ssh = ipad_h - 2 * bezel

        # Sidebar tabs
        tw = int(ssw * 0.06)
        for ti in range(8):
            ty = sy + 3 + ti * (ssh // 10)
            color = PATINA_BLUE if ti == 2 else DEEP_TEAL
            draw.rectangle([sx, ty, sx + tw, ty + ssh // 11], fill=color)

        # Header
        draw.text((sx + tw + 10, sy + 8), "February 2026", fill=DEEP_TEAL, font=get_font(20, bold=True))

        # Mini calendar grid
        import calendar
        cal = calendar.monthcalendar(2026, 2)
        gcx = sx + tw + 10
        gcy = sy + 35
        gcw = (ssw - tw - 20) // 7
        gch = (ssh - 45) // 6

        days = ["M", "T", "W", "T", "F", "S", "S"]
        for d, day in enumerate(days):
            dx = gcx + d * gcw
            draw.rectangle([dx, gcy, dx + gcw - 1, gcy + gch - 1], fill=DEEP_TEAL)

        for wi, week in enumerate(cal):
            for di, dn in enumerate(week):
                if dn > 0:
                    dx = gcx + di * gcw
                    dy = gcy + (wi + 1) * gch
                    draw.rectangle([dx, dy, dx + gcw - 1, dy + gch - 1], fill=WHITE, outline=LIGHT_GRAY)

    return img


def create_feature_frame(frame_num, total_frames, feature_title, feature_desc, accent_color):
    """Feature highlight frame."""
    img = Image.new('RGB', (W, H), WARM_LINEN)
    draw = ImageDraw.Draw(img)

    # Accent bars
    draw.rectangle([0, 0, W, 6], fill=PATINA_BLUE)
    draw.rectangle([0, 6, W, 10], fill=DUSTY_ROSE)
    draw.rectangle([0, 10, W, 14], fill=SOFT_SAGE)
    draw.rectangle([0, H - 14, W, H - 8], fill=SOFT_SAGE)
    draw.rectangle([0, H - 8, W, H - 4], fill=DUSTY_ROSE)
    draw.rectangle([0, H - 4, W, H], fill=PATINA_BLUE)

    # Animated accent circle
    progress = min(1.0, frame_num / (total_frames * 0.3))
    circle_r = int(200 * progress)
    draw.ellipse([80 - circle_r, H // 2 - circle_r, 80 + circle_r, H // 2 + circle_r],
                 fill=accent_color + (30,) if len(accent_color) == 3 else accent_color)

    # Feature title sliding in
    slide_progress = min(1.0, frame_num / (total_frames * 0.25))
    title_x = int(W // 2 - 200 * (1 - slide_progress))
    draw.text((title_x, H // 2 - 100), feature_title, fill=DEEP_TEAL, font=get_font(64, bold=True), anchor="mt")

    # Description fading in
    if frame_num > total_frames * 0.2:
        draw.text((W // 2, H // 2), feature_desc, fill=CHARCOAL, font=get_font(32), anchor="mt")

    # Colored accent bar
    draw.rectangle([W // 2 - 100, H // 2 + 50, W // 2 + 100, H // 2 + 53], fill=accent_color)

    # Bottom branding
    draw.text((W // 2, H - 60), "2026 Wellness & Productivity Digital Planner", fill=DEEP_TEAL, font=get_font(22), anchor="mt")

    return img


def create_cta_frame(frame_num, total_frames):
    """Final call-to-action frame."""
    img = Image.new('RGB', (W, H), DEEP_TEAL)
    draw = ImageDraw.Draw(img)

    # Frame border
    draw.rectangle([15, 15, W - 15, H - 15], outline=PATINA_BLUE, width=3)

    # Inner content
    draw.rounded_rectangle([50, 50, W - 50, H - 50], radius=20, fill=WARM_LINEN)

    # Accent bars
    draw.rectangle([50, 50, W - 50, 58], fill=PATINA_BLUE)
    draw.rectangle([50, 58, W - 50, 63], fill=DUSTY_ROSE)
    draw.rectangle([50, 63, W - 50, 67], fill=SOFT_SAGE)

    # Animated text
    progress = min(1.0, frame_num / (total_frames * 0.3))

    draw.text((W // 2, 150), "2026", fill=DEEP_TEAL, font=get_font(100, bold=True), anchor="mt")
    draw.text((W // 2, 270), "Wellness & Productivity", fill=CHARCOAL, font=get_font(40), anchor="mt")
    draw.text((W // 2, 330), "DIGITAL PLANNER", fill=DEEP_TEAL, font=get_font(56, bold=True), anchor="mt")

    # Divider
    draw.rectangle([W // 2 - 150, 400, W // 2 + 150, 403], fill=PATINA_BLUE)

    # Key features appearing
    features = [
        "28 Beautifully Designed Pages",
        "Fully Hyperlinked Navigation",
        "Wellness + Productivity Combined",
        "Works on All Tablets",
    ]
    for i, feat in enumerate(features):
        delay = 0.15 + i * 0.1
        if frame_num > total_frames * delay:
            fy = 440 + i * 55
            draw.ellipse([W // 2 - 380, fy + 5, W // 2 - 360, fy + 25], fill=PATINA_BLUE)
            draw.text((W // 2 - 345, fy), feat, fill=CHARCOAL, font=get_font(30))

    # CTA button
    if frame_num > total_frames * 0.4:
        btn_progress = min(1.0, (frame_num - total_frames * 0.4) / (total_frames * 0.3))
        btn_w = int(400 * btn_progress)
        btn_x = W // 2 - btn_w // 2
        btn_y = 700
        draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + 70], radius=35, fill=DUSTY_ROSE)
        if btn_w > 300:
            draw.text((W // 2, btn_y + 12), "Instant Download", fill=WHITE, font=get_font(36, bold=True), anchor="mt")

    # Bottom badges
    if frame_num > total_frames * 0.5:
        badges = ["GoodNotes", "Notability", "Xodo"]
        badge_w = 160
        gap = 20
        total_w = len(badges) * badge_w + (len(badges) - 1) * gap
        bx = (W - total_w) // 2
        for badge in badges:
            draw.rounded_rectangle([bx, 820, bx + badge_w, 860], radius=20, fill=DEEP_TEAL)
            draw.text((bx + badge_w // 2, 828), badge, fill=WHITE, font=get_font(20), anchor="mt")
            bx += badge_w + gap

    # Bottom accent
    draw.rectangle([50, H - 67, W - 50, H - 63], fill=SOFT_SAGE)
    draw.rectangle([50, H - 63, W - 50, H - 58], fill=DUSTY_ROSE)
    draw.rectangle([50, H - 58, W - 50, H - 50], fill=PATINA_BLUE)

    return img


def main():
    print("Creating video frames...")

    fps = 30
    total_seconds = 12
    total_frames = fps * total_seconds  # 360 frames

    # Scene breakdown (in frames):
    # 0-90   (3s): Title/opening with iPad mockup
    # 91-150 (2s): Feature 1 - Monthly Planning
    # 151-210(2s): Feature 2 - Daily Planner
    # 211-270(2s): Feature 3 - Wellness Tracking
    # 271-360(3s): CTA closing

    scenes = [
        (0, 90, "title"),
        (91, 150, "feature1"),
        (151, 210, "feature2"),
        (211, 270, "feature3"),
        (271, 360, "cta"),
    ]

    features = [
        ("Monthly Planning", "12 months of beautiful calendar spreads", PATINA_BLUE),
        ("Daily Structure", "Morning routine + schedule + gratitude", SOFT_SAGE),
        ("Wellness Tracking", "Sleep, meals, fitness & self-care", DUSTY_ROSE),
    ]

    for frame in range(total_frames):
        if frame <= 90:
            img = create_title_frame(frame, 90)
        elif frame <= 150:
            f_num = frame - 91
            img = create_feature_frame(f_num, 60, *features[0])
        elif frame <= 210:
            f_num = frame - 151
            img = create_feature_frame(f_num, 60, *features[1])
        elif frame <= 270:
            f_num = frame - 211
            img = create_feature_frame(f_num, 60, *features[2])
        else:
            f_num = frame - 271
            img = create_cta_frame(f_num, 90)

        img.save(os.path.join(FRAMES_DIR, f"frame_{frame:04d}.png"))

        if frame % 30 == 0:
            print(f"  Frame {frame}/{total_frames} ({frame * 100 // total_frames}%)")

    print(f"Generated {total_frames} frames")

    # Combine frames into video with ffmpeg
    print("\nCombining frames into MP4...")
    output_path = os.path.join(OUTPUT_DIR, "etsy_listing_video.mp4")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(FRAMES_DIR, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "23",
        "-an",  # No audio (Etsy doesn't support it)
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\nVideo created successfully!")
        print(f"Output: {output_path}")
        print(f"File size: {file_size:.1f} MB")
        print(f"Duration: {total_seconds}s at {fps}fps")
        print(f"Resolution: {W}x{H}")
    else:
        print(f"ffmpeg error: {result.stderr[-500:]}")

    # Clean up frames
    print("\nCleaning up frame files...")
    for f in os.listdir(FRAMES_DIR):
        os.remove(os.path.join(FRAMES_DIR, f))
    os.rmdir(FRAMES_DIR)
    print("Done!")


if __name__ == "__main__":
    main()
