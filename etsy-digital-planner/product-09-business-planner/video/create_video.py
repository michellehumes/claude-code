#!/usr/bin/env python3
"""
Small Business Planner Bundle - Promo Video
Generates a 12-second 1080x1080 30fps MP4 promo video.
"""

import os
import subprocess
import tempfile
import shutil
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Color palette
ROYAL_BLUE = (44, 95, 138)
STEEL_BLUE = (70, 130, 180)
LIGHT_BLUE = (214, 232, 245)
WHITE = (255, 255, 255)
CHARCOAL = (51, 51, 51)
AMBER = (232, 148, 58)
RED_ACCENT = (212, 70, 56)
DARK_BG = (30, 50, 75)

W, H = 1080, 1080
FPS = 30
DURATION = 12  # seconds
TOTAL_FRAMES = FPS * DURATION


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


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_centered(draw, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)


def text_centered_in_rect(draw, rect, text, font, fill):
    x0, y0, x1, y1 = rect
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - tw) // 2
    y = y0 + (y1 - y0 - th) // 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_gradient_bg(img, color1, color2):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return draw


def ease_in_out(t):
    """Smooth easing function."""
    if t < 0.5:
        return 2 * t * t
    return 1 - (-2 * t + 2) ** 2 / 2


def scene_1_title(frame_num, total_scene_frames):
    """Scene 1: Small Business Planner title (0-3s = frames 0-89)."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, ROYAL_BLUE)

    progress = frame_num / total_scene_frames

    # Top accent bar
    draw.rectangle([0, 0, W, 5], fill=AMBER)

    # Animated title - slide in from top
    title_y_target = 280
    if progress < 0.3:
        ease = ease_in_out(progress / 0.3)
        title_y = int(-100 + (title_y_target + 100) * ease)
    else:
        title_y = title_y_target

    title_font = get_font(52, bold=True)
    text_centered(draw, title_y, "SMALL BUSINESS", title_font, WHITE)
    text_centered(draw, title_y + 70, "PLANNER BUNDLE", title_font, WHITE)

    # Subtitle - fade in
    if progress > 0.3:
        sub_progress = min(1, (progress - 0.3) / 0.3)
        alpha = int(255 * sub_progress)
        sub_font = get_font(26)
        text_centered(draw, title_y + 175, "8 Professional Spreadsheets", sub_font,
                      (LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2]))

    # Year badge - pop in
    if progress > 0.5:
        badge_progress = min(1, (progress - 0.5) / 0.3)
        badge_scale = ease_in_out(badge_progress)
        bw = int(220 * badge_scale)
        bh = int(45 * badge_scale)
        bx = (W - bw) // 2
        by = title_y + 240
        if bw > 20 and bh > 10:
            draw_rounded_rect(draw, (bx, by, bx + bw, by + bh), 15, fill=AMBER)
            if badge_scale > 0.7:
                badge_font = get_font(22, bold=True)
                text_centered_in_rect(draw, (bx, by, bx + bw, by + bh), "2026 EDITION", badge_font, WHITE)

    # Decorative elements
    if progress > 0.6:
        for_ent_font = get_font(22)
        text_centered(draw, title_y + 320, "for Entrepreneurs", for_ent_font, AMBER)

    # Mini spreadsheet icons at bottom
    if progress > 0.4:
        icon_progress = min(1, (progress - 0.4) / 0.4)
        icons_alpha = ease_in_out(icon_progress)
        icon_y = int(680 + (1 - icons_alpha) * 50)
        for i in range(4):
            ix = 120 + i * 230
            color = ROYAL_BLUE if i % 2 == 0 else STEEL_BLUE
            draw_rounded_rect(draw, (ix, icon_y, ix + 200, icon_y + 140), 10, fill=WHITE)
            draw_rounded_rect(draw, (ix, icon_y, ix + 200, icon_y + 30), 10, fill=color)
            draw.rectangle([ix, icon_y + 20, ix + 200, icon_y + 30], fill=color)
            # Mini rows
            for j in range(4):
                ry = icon_y + 40 + j * 22
                bg = LIGHT_BLUE if j % 2 == 0 else WHITE
                draw.rectangle([ix + 5, ry, ix + 195, ry + 18], fill=bg)

    # Bottom bar
    draw.rectangle([0, H - 50, W, H], fill=AMBER)
    if progress > 0.5:
        bot_font = get_font(18, bold=True)
        text_centered(draw, H - 40, "Excel & Google Sheets Compatible", bot_font, WHITE)

    return img


def scene_2_spreadsheets(frame_num, total_scene_frames):
    """Scene 2: 8 spreadsheets showcase (3-6s = frames 90-179)."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, (248, 250, 252), LIGHT_BLUE)

    progress = frame_num / total_scene_frames

    # Header
    draw.rectangle([0, 0, W, 70], fill=ROYAL_BLUE)
    title_font = get_font(32, bold=True)
    text_centered(draw, 15, "8 SPREADSHEETS INCLUDED", title_font, WHITE)

    spreadsheets = [
        ("Income Tracker", ROYAL_BLUE),
        ("Expense Tracker", STEEL_BLUE),
        ("Profit & Loss", ROYAL_BLUE),
        ("Invoice Tracker", STEEL_BLUE),
        ("Client CRM", ROYAL_BLUE),
        ("Content Calendar", STEEL_BLUE),
        ("Inventory Tracker", ROYAL_BLUE),
        ("Tax Deductions", STEEL_BLUE),
    ]

    # Staggered reveal of spreadsheet cards
    for i, (name, color) in enumerate(spreadsheets):
        delay = i * 0.08
        if progress > delay:
            card_progress = min(1, (progress - delay) / 0.3)
            ease = ease_in_out(card_progress)

            col = i % 2
            row = i // 2
            cx = 50 + col * 510
            cy = 100 + row * 230
            cw = 480
            ch = 200

            # Slide in from right
            offset_x = int((1 - ease) * 300)
            cx += offset_x

            draw_rounded_rect(draw, (cx, cy, cx + cw, cy + ch), 14, fill=WHITE)
            draw_rounded_rect(draw, (cx, cy, cx + cw, cy + 40), 14, fill=color)
            draw.rectangle([cx, cy + 25, cx + cw, cy + 40], fill=color)

            name_font = get_font(20, bold=True)
            draw.text((cx + 15, cy + 8), name, font=name_font, fill=WHITE)

            # Number badge
            draw.ellipse([cx + cw - 45, cy + 5, cx + cw - 10, cy + 35], fill=AMBER)
            num_font = get_font(16, bold=True)
            nbbox = draw.textbbox((0, 0), str(i + 1), font=num_font)
            nw = nbbox[2] - nbbox[0]
            draw.text((cx + cw - 28 - nw // 2, cy + 9), str(i + 1), font=num_font, fill=WHITE)

            # Mini rows
            for j in range(5):
                ry = cy + 50 + j * 28
                bg = LIGHT_BLUE if j % 2 == 0 else WHITE
                draw.rectangle([cx + 8, ry, cx + cw - 8, ry + 24], fill=bg)

    # Bottom accent
    draw.rectangle([0, H - 50, W, H], fill=AMBER)
    bot_font = get_font(18, bold=True)
    text_centered(draw, H - 40, "Complete Business Management Bundle", bot_font, WHITE)

    return img


def scene_3_features(frame_num, total_scene_frames):
    """Scene 3: Features (6-9s = frames 180-269)."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, DARK_BG, (35, 70, 110))

    progress = frame_num / total_scene_frames

    draw.rectangle([0, 0, W, 5], fill=AMBER)

    title_font = get_font(38, bold=True)
    text_centered(draw, 30, "KEY FEATURES", title_font, WHITE)

    features = [
        ("Auto-Formulas", "SUM, SUMIF, COUNTIF & more"),
        ("Tax-Ready", "Deduction tracking & savings"),
        ("Data Validation", "Dropdown menus for accuracy"),
        ("Dashboard Views", "Annual summary at a glance"),
        ("12-Month Tracking", "Full 2026 year coverage"),
        ("Professional Design", "Clean, organized layouts"),
        ("Frozen Headers", "Easy scrolling navigation"),
        ("Instructions Tab", "Get started in minutes"),
    ]

    for i, (title, desc) in enumerate(features):
        delay = i * 0.08
        if progress > delay:
            card_progress = min(1, (progress - delay) / 0.25)
            ease = ease_in_out(card_progress)

            col = i % 2
            row = i // 2
            fx = 40 + col * 520
            fy = 100 + row * 225
            fw = 490
            fh = 200

            # Scale in effect
            scale = ease
            actual_w = int(fw * scale)
            actual_h = int(fh * scale)
            actual_x = fx + (fw - actual_w) // 2
            actual_y = fy + (fh - actual_h) // 2

            if actual_w > 20 and actual_h > 20:
                draw_rounded_rect(draw, (actual_x, actual_y, actual_x + actual_w, actual_y + actual_h),
                                  12, fill=WHITE)

                if scale > 0.6:
                    # Icon circle
                    icon_x = actual_x + 25
                    icon_y = actual_y + actual_h // 2 - 25
                    draw.ellipse([icon_x, icon_y, icon_x + 50, icon_y + 50], fill=AMBER)
                    num_font = get_font(22, bold=True)
                    draw.text((icon_x + 15, icon_y + 12), str(i + 1), font=num_font, fill=WHITE)

                    # Text
                    t_font = get_font(22, bold=True)
                    d_font = get_font(17)
                    draw.text((actual_x + 90, actual_y + actual_h // 2 - 30), title, font=t_font, fill=ROYAL_BLUE)
                    draw.text((actual_x + 90, actual_y + actual_h // 2 + 10), desc, font=d_font, fill=CHARCOAL)

    # Bottom highlight
    if progress > 0.6:
        draw_rounded_rect(draw, (100, H - 130, W - 100, H - 60), 20, fill=AMBER)
        hl_font = get_font(24, bold=True)
        text_centered_in_rect(draw, (100, H - 130, W - 100, H - 60), "100+ Auto-Calculating Formulas", hl_font, WHITE)

    draw.rectangle([0, H - 50, W, H], fill=ROYAL_BLUE)

    return img


def scene_4_cta(frame_num, total_scene_frames):
    """Scene 4: CTA $11.99 (9-12s = frames 270-359)."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = draw_gradient_bg(img, ROYAL_BLUE, DARK_BG)

    progress = frame_num / total_scene_frames

    draw.rectangle([0, 0, W, 5], fill=AMBER)

    # Title
    title_font = get_font(42, bold=True)
    text_centered(draw, 50, "SMALL BUSINESS", title_font, WHITE)
    text_centered(draw, 105, "PLANNER BUNDLE", title_font, WHITE)

    # "8 Spreadsheets" subtitle
    sub_font = get_font(24)
    text_centered(draw, 175, "8 Professional Spreadsheets for Entrepreneurs", sub_font, LIGHT_BLUE)

    # Items list
    if progress > 0.1:
        items = [
            "Income Tracker", "Expense Tracker", "P&L Statement", "Invoice Tracker",
            "Client CRM", "Content Calendar", "Inventory", "Tax Deductions"
        ]
        item_font = get_font(18)
        for i, item in enumerate(items):
            col = i % 2
            row = i // 2
            ix = 150 + col * 420
            iy = 240 + row * 55
            draw.ellipse([ix - 22, iy + 2, ix - 4, iy + 20], fill=AMBER)
            draw.text((ix + 5, iy), item, font=item_font, fill=WHITE)

    # Price section - animated
    if progress > 0.25:
        price_progress = min(1, (progress - 0.25) / 0.3)
        ease = ease_in_out(price_progress)

        ph = int(250 * ease)
        py = 490
        if ph > 30:
            draw_rounded_rect(draw, (120, py, W - 120, py + ph), 20, fill=AMBER)

            if ease > 0.5:
                # Original price with strikethrough
                orig_font = get_font(24)
                text_centered(draw, py + 15, "Regular Price: $29.99", orig_font, WHITE)
                obbox = draw.textbbox((0, 0), "Regular Price: $29.99", font=orig_font)
                ow = obbox[2] - obbox[0]
                ox = (W - ow) // 2
                draw.line([(ox, py + 30), (ox + ow, py + 30)], fill=WHITE, width=2)

            if ease > 0.7:
                # Sale price
                price_font = get_font(72, bold=True)
                text_centered(draw, py + 50, "$11.99", price_font, WHITE)

            if ease > 0.9:
                save_font = get_font(22, bold=True)
                text_centered(draw, py + 160, "SAVE 60% - Limited Time!", save_font, WHITE)

    # CTA Button - pulse effect
    if progress > 0.5:
        btn_progress = (progress - 0.5) / 0.5
        # Subtle pulse
        pulse = 1.0 + 0.03 * abs(((btn_progress * 4) % 2) - 1)
        btn_w = int(600 * pulse)
        btn_h = int(70 * pulse)
        bx = (W - btn_w) // 2
        by = 790

        draw_rounded_rect(draw, (bx, by, bx + btn_w, by + btn_h), 35, fill=AMBER)
        cta_font = get_font(28, bold=True)
        text_centered_in_rect(draw, (bx, by, bx + btn_w, by + btn_h), "ADD TO CART", cta_font, WHITE)

    # Bottom info
    if progress > 0.6:
        info_font = get_font(18)
        text_centered(draw, 900, "Instant Download  |  Excel & Google Sheets", info_font, LIGHT_BLUE)
        text_centered(draw, 935, "Satisfaction Guaranteed", info_font, AMBER)

    # Bottom bars
    draw.rectangle([0, H - 50, W, H], fill=AMBER)
    bot_font = get_font(18, bold=True)
    text_centered(draw, H - 40, "Start Organizing Your Business Today!", bot_font, WHITE)
    draw.rectangle([0, H - 5, W, H], fill=ROYAL_BLUE)

    return img


def main():
    print("=" * 60)
    print("Small Business Planner Bundle - Promo Video")
    print(f"Generating {DURATION}s video at {W}x{H} {FPS}fps...")
    print("=" * 60)

    # Create temp directory for frames
    tmp_dir = tempfile.mkdtemp(prefix="biz_planner_video_")
    print(f"  Temp frames directory: {tmp_dir}")

    # Scene boundaries (in frames)
    # Scene 1: 0-89 (3s), Scene 2: 90-179 (3s), Scene 3: 180-269 (3s), Scene 4: 270-359 (3s)
    scene_frames = [
        (0, 90, scene_1_title),
        (90, 180, scene_2_spreadsheets),
        (180, 270, scene_3_features),
        (270, 360, scene_4_cta),
    ]

    for frame_num in range(TOTAL_FRAMES):
        # Determine which scene
        for start, end, scene_func in scene_frames:
            if start <= frame_num < end:
                local_frame = frame_num - start
                total_scene = end - start
                img = scene_func(local_frame, total_scene)
                break

        # Add scene transition (crossfade at boundaries)
        frame_path = os.path.join(tmp_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")

        if frame_num % 30 == 0:
            print(f"  Frame {frame_num}/{TOTAL_FRAMES} ({frame_num * 100 // TOTAL_FRAMES}%)")

    print(f"  All {TOTAL_FRAMES} frames generated.")

    # Encode video with ffmpeg
    output_path = os.path.join(OUTPUT_DIR, "promo_video.mp4")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(tmp_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        "-movflags", "+faststart",
        output_path
    ]

    print("  Encoding video with ffmpeg...")
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg error: {result.stderr}")
    else:
        print(f"  Created: {output_path}")

    # Cleanup
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print("  Cleaned up temporary frames.")

    # Verify
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Video size: {size_mb:.1f} MB")
    else:
        print("  WARNING: Video file was not created!")

    print("\n" + "=" * 60)
    print("Promo video created successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
