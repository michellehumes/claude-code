#!/usr/bin/env python3
"""
Create a 12-second 1080x1080 30fps promo video for the
2026 Meal Planner & Grocery List Bundle.
"""

import os
import subprocess
import tempfile
import shutil
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1080
FPS = 30
DURATION = 12
TOTAL_FRAMES = FPS * DURATION

# ── Color Palette ──
TERRACOTTA = (196, 113, 59)
SAGE = (143, 174, 139)
CREAM = (255, 248, 240)
SOFT_ORANGE = (244, 164, 96)
WHITE = (255, 255, 255)
CHARCOAL = (68, 68, 68)
SOFT_RED = (212, 114, 106)
DARK_TERRA = (156, 83, 39)
LIGHT_SAGE = (212, 232, 209)
LIGHT_TERRA = (240, 200, 168)
DARK_SAGE = (100, 130, 96)


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
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def centered_text(draw, y, text, font, fill, x_center=W // 2):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x_center - tw // 2, y), text, font=font, fill=fill)


def draw_checkmark(draw, x, y, size, color):
    draw.line([x, y + size * 0.5, x + size * 0.35, y + size], fill=color, width=3)
    draw.line([x + size * 0.35, y + size, x + size, y], fill=color, width=3)


def draw_food_icons_small(draw, y, alpha=1.0):
    """Draw small decorative food icons."""
    icons = [
        (120, y), (300, y), (480, y), (660, y), (840, y), (960, y),
    ]
    for x, iy in icons:
        draw.ellipse([x - 12, iy - 12, x + 12, iy + 12], outline=SAGE, width=2)
        draw.ellipse([x - 6, iy - 6, x + 6, iy + 6], fill=LIGHT_SAGE)


def ease_in_out(t):
    """Ease in-out cubic."""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


# ═══════════════════════════════════════════════════════════
# SCENE RENDERERS
# ═══════════════════════════════════════════════════════════

def render_scene1(frame_in_scene, total_scene_frames):
    """Scene 1: Title with food-themed colors (0-3s)"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    t = frame_in_scene / max(total_scene_frames - 1, 1)

    # Animated background - terracotta header grows
    header_h = int(ease_in_out(min(t * 2, 1.0)) * 300)
    if header_h > 0:
        draw_rounded_rect(draw, (0, 0, W, header_h), 0, TERRACOTTA)

    # Sage accent bar
    if t > 0.15:
        bar_t = min((t - 0.15) * 3, 1.0)
        bar_w = int(ease_in_out(bar_t) * W)
        draw_rounded_rect(draw, ((W - bar_w) // 2, header_h, (W + bar_w) // 2, header_h + 15), 0, SAGE)

    # Year badge
    if t > 0.2:
        badge_t = min((t - 0.2) * 3, 1.0)
        badge_scale = ease_in_out(badge_t)
        badge_size = int(100 * badge_scale)
        if badge_size > 5:
            cx, cy = W // 2, 200
            draw_rounded_rect(draw, (cx - badge_size, cy - badge_size // 2, cx + badge_size, cy + badge_size // 2),
                              20, SAGE)
            if badge_scale > 0.5:
                centered_text(draw, cy - 25, "2026", get_font(int(44 * badge_scale), bold=True), WHITE)

    # Main title - slides up
    if t > 0.3:
        title_t = min((t - 0.3) * 2.5, 1.0)
        title_y = int(lerp(600, 380, ease_in_out(title_t)))
        alpha = ease_in_out(title_t)
        color = lerp_color(CREAM, TERRACOTTA, alpha)
        centered_text(draw, title_y, "Meal Planner &", get_font(62, bold=True), color)
        centered_text(draw, title_y + 80, "Grocery List", get_font(62, bold=True), color)

    # "BUNDLE" text
    if t > 0.5:
        bundle_t = min((t - 0.5) * 3, 1.0)
        bundle_y = int(lerp(600, 540, ease_in_out(bundle_t)))
        bundle_color = lerp_color(CREAM, SAGE, ease_in_out(bundle_t))
        centered_text(draw, bundle_y, "BUNDLE", get_font(48, bold=True), bundle_color)

    # Subtitle
    if t > 0.6:
        sub_t = min((t - 0.6) * 3, 1.0)
        sub_alpha = ease_in_out(sub_t)
        sub_color = lerp_color(CREAM, CHARCOAL, sub_alpha)
        centered_text(draw, 640, "6 Professional Spreadsheets", get_font(30), sub_color)
        centered_text(draw, 680, "Plan | Shop | Cook | Save", get_font(26, bold=True), lerp_color(CREAM, SAGE, sub_alpha))

    # Decorative food icons at bottom
    if t > 0.4:
        draw_food_icons_small(draw, 790)

    # Bottom bar
    if t > 0.7:
        bot_t = min((t - 0.7) * 3, 1.0)
        bot_w = int(ease_in_out(bot_t) * (W - 100))
        draw_rounded_rect(draw, ((W - bot_w) // 2, 850, (W + bot_w) // 2, 920), 15, TERRACOTTA)
        if bot_t > 0.3:
            centered_text(draw, 860, "Excel & Google Sheets Compatible", get_font(26, bold=True), WHITE)

    # Bottom accent
    draw_rounded_rect(draw, (0, H - 60, W, H), 0, SAGE)
    centered_text(draw, H - 50, "Instant Download | Fully Editable", get_font(20), WHITE)

    return img


def render_scene2(frame_in_scene, total_scene_frames):
    """Scene 2: 6 Spreadsheets showcase (3-6s)"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    t = frame_in_scene / max(total_scene_frames - 1, 1)

    # Header
    draw_rounded_rect(draw, (0, 0, W, 140), 0, SAGE)
    centered_text(draw, 20, "6 SPREADSHEETS", get_font(48, bold=True), WHITE)
    centered_text(draw, 85, "INCLUDED IN YOUR BUNDLE", get_font(26), LIGHT_SAGE)

    # 6 cards - appear one by one
    items = [
        ("Weekly Meal Planner", "52 weekly tabs", TERRACOTTA),
        ("Monthly Calendar", "12 monthly views", SAGE),
        ("Recipe Tracker", "100+ recipe slots", SOFT_ORANGE),
        ("Budget Tracker", "Annual dashboard", DARK_TERRA),
        ("Pantry Inventory", "80+ items loaded", DARK_SAGE),
        ("Meal Prep Planner", "Prep day schedule", SOFT_RED),
    ]

    for i, (name, desc, color) in enumerate(items):
        # Stagger appearance
        item_start = i * 0.1
        if t < item_start:
            continue

        item_t = min((t - item_start) / 0.3, 1.0)
        scale = ease_in_out(item_t)

        col = i % 2
        row = i // 2
        cx = 120 + col * 460
        cy = 190 + row * 260

        # Slide in from side
        offset_x = int((1 - scale) * (300 if col == 0 else -300))

        bx = cx + offset_x
        by = cy

        # Card
        draw_rounded_rect(draw, (bx, by, bx + 420, by + 220), 15, WHITE, outline=color, width=3)

        # Color header
        draw_rounded_rect(draw, (bx, by, bx + 420, by + 55), 15, color)
        draw.rectangle([bx, by + 35, bx + 420, by + 55], fill=color)

        # Number badge
        draw_rounded_rect(draw, (bx + 15, by + 8, bx + 55, by + 45), 10, WHITE)
        centered_text(draw, by + 10, str(i + 1), get_font(24, bold=True), color, bx + 35)

        # Title in header
        centered_text(draw, by + 12, name, get_font(24, bold=True), WHITE, bx + 250)

        # Description
        centered_text(draw, by + 75, desc, get_font(22), CHARCOAL, bx + 210)

        # Mini spreadsheet grid
        for gr in range(3):
            gy = by + 115 + gr * 28
            draw.line([bx + 30, gy, bx + 390, gy], fill=color, width=1)
            for gc in range(4):
                gx = bx + 30 + gc * 90
                draw_rounded_rect(draw, (gx + 2, gy + 3, gx + 82, gy + 22), 4,
                                  LIGHT_SAGE if gr % 2 == 0 else CREAM)

    # Bottom bar
    draw_rounded_rect(draw, (0, H - 80, W, H), 0, TERRACOTTA)
    centered_text(draw, H - 68, "All professionally formatted with auto-formulas", get_font(24, bold=True), WHITE)

    return img


def render_scene3(frame_in_scene, total_scene_frames):
    """Scene 3: Features highlight (6-9s)"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    t = frame_in_scene / max(total_scene_frames - 1, 1)

    # Header
    draw_rounded_rect(draw, (0, 0, W, 120), 0, TERRACOTTA)
    centered_text(draw, 25, "KEY FEATURES", get_font(52, bold=True), WHITE)
    centered_text(draw, 85, "Everything for organized meal planning", get_font(22), LIGHT_TERRA)

    # Feature items with staggered animation
    features = [
        ("52", "Weekly Meal Plans", "Complete year of planning\nwith daily meal grids", TERRACOTTA),
        ("100+", "Recipe Slots", "Track favorites with\nratings & cook times", SAGE),
        ("12", "Monthly Calendars", "Dinner planning with\ntheme nights", SOFT_ORANGE),
        ("80+", "Pantry Items", "Pre-loaded inventory\nwith expiry alerts", DARK_SAGE),
        ("$", "Budget Tracking", "Monthly logs with\nannual dashboard", SOFT_RED),
        ("AUTO", "Smart Formulas", "Totals & averages\ncalculate automatically", DARK_TERRA),
    ]

    for i, (badge, title, desc, color) in enumerate(features):
        feat_start = i * 0.1
        if t < feat_start:
            continue

        feat_t = min((t - feat_start) / 0.25, 1.0)
        slide = int((1 - ease_in_out(feat_t)) * 100)

        col = i % 2
        row = i // 2
        fx = 60 + col * 520
        fy = 160 + row * 260 + slide

        # Card
        draw_rounded_rect(draw, (fx, fy, fx + 480, fy + 230), 18, WHITE, outline=color, width=3)

        # Badge circle
        draw.ellipse([fx + 20, fy + 20, fx + 110, fy + 110], fill=color)
        badge_font_size = 28 if len(badge) <= 3 else 18
        centered_text(draw, fy + 38 if len(badge) <= 3 else fy + 44, badge,
                      get_font(badge_font_size, bold=True), WHITE, fx + 65)

        # Title
        draw.text((fx + 130, fy + 25), title, font=get_font(28, bold=True), fill=color)

        # Divider
        draw.line([fx + 130, fy + 65, fx + 450, fy + 65], fill=color, width=2)

        # Description
        for li, line in enumerate(desc.split("\n")):
            draw.text((fx + 130, fy + 80 + li * 30), line, font=get_font(22), fill=CHARCOAL)

        # Bottom accent
        draw_rounded_rect(draw, (fx + 20, fy + 175, fx + 460, fy + 210), 8, color)
        labels = ["Weekly", "Recipes", "Monthly", "Inventory", "Budget", "Smart"][i]
        centered_text(draw, fy + 180, labels, get_font(18, bold=True), WHITE, fx + 240)

    # Bottom
    draw_rounded_rect(draw, (0, H - 80, W, H), 0, SAGE)
    centered_text(draw, H - 68, "Professional formatting | Print ready | Frozen headers", get_font(22, bold=True), WHITE)

    return img


def render_scene4(frame_in_scene, total_scene_frames):
    """Scene 4: CTA with price (9-12s)"""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    t = frame_in_scene / max(total_scene_frames - 1, 1)

    # Background animation
    draw_rounded_rect(draw, (0, 0, W, 200), 0, TERRACOTTA)
    draw_rounded_rect(draw, (0, 180, W, 210), 0, SAGE)
    draw_rounded_rect(draw, (0, H - 100, W, H), 0, TERRACOTTA)

    # Title
    centered_text(draw, 40, "COMPLETE MEAL PLANNING", get_font(38, bold=True), WHITE)
    centered_text(draw, 95, "BUNDLE FOR 2026", get_font(48, bold=True), WHITE)
    centered_text(draw, 155, "6 Professional Spreadsheets", get_font(24), LIGHT_TERRA)

    # Main card
    card_t = min(t * 2, 1.0)
    card_scale = ease_in_out(card_t)
    card_h = int(580 * card_scale)
    card_y = 260

    if card_h > 20:
        draw_rounded_rect(draw, (60, card_y, W - 60, card_y + card_h), 25, WHITE, outline=TERRACOTTA, width=4)

    if card_scale > 0.4:
        # Price section
        draw_rounded_rect(draw, (200, 290, W - 200, 430), 20, TERRACOTTA)

        # Crossed out price
        centered_text(draw, 300, "$24.99", get_font(32), (200, 160, 150))
        bbox = draw.textbbox((0, 0), "$24.99", font=get_font(32))
        tw = bbox[2] - bbox[0]
        cx = W // 2 - tw // 2
        draw.line([cx - 5, 320, cx + tw + 5, 320], fill=WHITE, width=2)

        # Actual price - pulsing
        pulse = 1.0 + 0.03 * (1 + __import__('math').sin(t * 8))
        price_size = int(56 * pulse)
        centered_text(draw, 345, "$9.99", get_font(price_size, bold=True), WHITE)

        # Save badge
        draw_rounded_rect(draw, (W - 250, 290, W - 80, 340), 12, SOFT_ORANGE)
        centered_text(draw, 298, "60% OFF", get_font(22, bold=True), WHITE, W - 165)

    # Included items - slide in
    if card_scale > 0.6:
        included = [
            "Weekly Meal Planner (52 tabs)",
            "Monthly Meal Calendar",
            "Recipe Collection Tracker",
            "Grocery Budget Tracker",
            "Pantry Inventory Tracker",
            "Meal Prep Planner",
        ]
        for ii, item in enumerate(included):
            item_start = 0.6 + ii * 0.05
            if t < item_start:
                continue
            item_t = min((t - item_start) / 0.15, 1.0)
            item_x = int(lerp(-400, 120, ease_in_out(item_t)))

            iy = 460 + ii * 42
            draw_checkmark(draw, item_x, iy + 3, 20, SAGE)
            draw.text((item_x + 35, iy), item, font=get_font(24), fill=CHARCOAL)

    # Compatibility badges
    if t > 0.5:
        badge_t = min((t - 0.5) * 3, 1.0)
        badge_alpha = ease_in_out(badge_t)
        if badge_alpha > 0.3:
            badges = ["Excel", "Google Sheets", "Instant Download"]
            for bi, badge_text in enumerate(badges):
                bx = 100 + bi * 320
                draw_rounded_rect(draw, (bx, 740, bx + 280, 790), 12, SAGE)
                centered_text(draw, 750, badge_text, get_font(22, bold=True), WHITE, bx + 140)

    # CTA button
    if t > 0.6:
        cta_t = min((t - 0.6) * 3, 1.0)
        cta_scale = ease_in_out(cta_t)
        cta_w = int(600 * cta_scale)
        if cta_w > 50:
            draw_rounded_rect(draw, ((W - cta_w) // 2, 820, (W + cta_w) // 2, 900), 20, TERRACOTTA)
            if cta_scale > 0.5:
                centered_text(draw, 835, "GET YOUR BUNDLE NOW", get_font(30, bold=True), WHITE)
                centered_text(draw, 875, "Only $9.99", get_font(20), LIGHT_TERRA)

    # Bottom branding
    centered_text(draw, H - 85, "2026 Meal Planner & Grocery List Bundle", get_font(24, bold=True), WHITE)
    centered_text(draw, H - 50, "Start your organized kitchen journey today!", get_font(20), LIGHT_TERRA)

    # Decorative food icons
    draw_food_icons_small(draw, 940)

    return img


# ═══════════════════════════════════════════════════════════
# MAIN - Render & Encode
# ═══════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("Creating Promo Video")
    print("=" * 60)

    # Scene breakdown (12 seconds total, 30fps = 360 frames)
    scenes = [
        (0, 3, render_scene1),      # 0-3s: Title
        (3, 6, render_scene2),      # 3-6s: 6 Spreadsheets
        (6, 9, render_scene3),      # 6-9s: Features
        (9, 12, render_scene4),     # 9-12s: CTA
    ]

    tmp_dir = tempfile.mkdtemp(prefix="meal_planner_video_")
    print(f"  Temp directory: {tmp_dir}")

    try:
        for frame_num in range(TOTAL_FRAMES):
            current_time = frame_num / FPS

            # Determine which scene
            for start, end, renderer in scenes:
                if start <= current_time < end:
                    scene_frames = int((end - start) * FPS)
                    frame_in_scene = int((current_time - start) * FPS)
                    img = renderer(frame_in_scene, scene_frames)
                    break
            else:
                img = render_scene4(FPS * 3 - 1, FPS * 3)

            # Add cross-fade between scenes (last/first 5 frames)
            fade_frames = 5
            for start, end, renderer in scenes:
                scene_start_frame = int(start * FPS)
                if frame_num >= scene_start_frame and frame_num < scene_start_frame + fade_frames and start > 0:
                    # Fade from previous scene
                    prev_renderer = None
                    for ps, pe, pr in scenes:
                        if pe == start:
                            prev_renderer = pr
                            break
                    if prev_renderer:
                        prev_scene_frames = int((pe - ps) * FPS)
                        prev_img = prev_renderer(prev_scene_frames - 1, prev_scene_frames)
                        alpha = (frame_num - scene_start_frame) / fade_frames
                        img = Image.blend(prev_img, img, alpha)

            img.save(os.path.join(tmp_dir, f"frame_{frame_num:04d}.png"))

            if frame_num % 30 == 0:
                print(f"  Frame {frame_num}/{TOTAL_FRAMES} ({current_time:.1f}s)")

        print(f"  All {TOTAL_FRAMES} frames rendered.")

        # Encode with ffmpeg
        output_path = os.path.join(OUTPUT_DIR, "promo_video.mp4")
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(tmp_dir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "23",
            "-movflags", "+faststart",
            output_path
        ]

        print("  Encoding video with ffmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ffmpeg stderr: {result.stderr[:500]}")
            raise RuntimeError("ffmpeg encoding failed")

        print(f"  Saved: {output_path}")

        # Verify
        file_size = os.path.getsize(output_path)
        print(f"  File size: {file_size / 1024:.1f} KB")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print("  Cleaned up temp directory.")

    print("\n" + "=" * 60)
    print("Video created successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
