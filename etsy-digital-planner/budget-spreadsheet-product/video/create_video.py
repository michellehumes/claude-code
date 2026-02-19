#!/usr/bin/env python3
"""
Create 12-second promotional video for Budget & Finance Spreadsheet Bundle
1080x1080px at 30fps for Etsy listing video
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
import struct
import zlib

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

W, H = 1080, 1080
FPS = 30
DURATION = 12
TOTAL_FRAMES = FPS * DURATION

# Colors
DEEP_GREEN = (74, 107, 85)
SAGE_GREEN = (123, 158, 135)
SOFT_MINT = (212, 230, 217)
WARM_CREAM = (253, 248, 240)
CHARCOAL = (61, 61, 61)
WHITE = (255, 255, 255)
CORAL = (232, 145, 122)
GOLD = (212, 168, 83)
LIGHT_GRAY = (245, 245, 245)
MEDIUM_GRAY = (200, 200, 200)

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    # Guard against degenerate rects
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

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out(t):
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

def draw_mini_spreadsheet(draw, x, y, w, h, title, color, alpha_pct=1.0):
    draw_rounded_rect(draw, (x, y, x+w, y+h), 8, WHITE)
    draw_rounded_rect(draw, (x, y, x+w, y+30), 8, color)
    draw.rectangle([x, y+20, x+w, y+30], fill=color)
    font = get_font(14, bold=True)
    draw.text((x+10, y+7), title, fill=WHITE, font=font)
    row_h = (h - 40) // 6
    for r in range(7):
        ry = y + 35 + r * row_h
        draw.line([(x+1, ry), (x+w-1, ry)], fill=MEDIUM_GRAY, width=1)
    col_w = w // 4
    for c in range(5):
        cx = x + c * col_w
        draw.line([(cx, y+35), (cx, y+h-1)], fill=MEDIUM_GRAY, width=1)

def draw_dollar_icon(draw, cx, cy, size, color=GOLD):
    draw.ellipse([cx-size, cy-size, cx+size, cy+size], fill=color)
    font = get_font(int(size*1.3), bold=True)
    draw.text((cx-size//3, cy-size//1.5), "$", fill=WHITE, font=font)

def draw_progress_bar(draw, x, y, w, h, progress, color, bg=LIGHT_GRAY):
    draw_rounded_rect(draw, (x, y, x+w, y+h), h//2, bg)
    pw = int(w * progress)
    if pw > h:
        draw_rounded_rect(draw, (x, y, x+pw, y+h), h//2, color)

def draw_checkmark(draw, x, y, size, color):
    draw.line([(x, y+size//2), (x+size//3, y+size)], fill=color, width=3)
    draw.line([(x+size//3, y+size), (x+size, y)], fill=color, width=3)


def generate_frame(frame_num):
    """Generate a single frame of the video"""
    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    t = frame_num / TOTAL_FRAMES  # 0 to 1 progress through video
    frame_in_scene = frame_num % (TOTAL_FRAMES // 4)
    scene_t = frame_in_scene / (TOTAL_FRAMES // 4)
    scene = min(frame_num // (TOTAL_FRAMES // 4), 3)

    # ===== SCENE 1: Title Reveal (0-3s) =====
    if scene == 0:
        # Background
        draw.rectangle([0, 0, W, H], fill=DEEP_GREEN)

        # Animated dollar signs floating up
        for i in range(12):
            dx = 80 + (i * 97) % W
            base_y = H + 100 - ((scene_t * 800 + i * 120) % (H + 200))
            size = 20 + i % 3 * 10
            alpha_color = tuple(int(c * 0.15) + int(DEEP_GREEN[j] * 0.85) for j, c in enumerate(SAGE_GREEN))
            font_d = get_font(size)
            draw.text((dx, base_y), "$", fill=alpha_color, font=font_d)

        # Title slides in from left
        title_x = int(lerp(-600, 100, ease_out(min(scene_t * 2, 1))))
        font_title = get_font(58, bold=True)
        draw.text((title_x, 280), "BUDGET &", fill=WHITE, font=font_title)
        draw.text((title_x, 350), "FINANCE", fill=WHITE, font=font_title)

        # Year badge pops in
        if scene_t > 0.3:
            badge_t = ease_out(min((scene_t - 0.3) * 2.5, 1))
            badge_size = int(80 * badge_t)
            if badge_size > 20:
                bx, by = 700, 280
                draw_rounded_rect(draw, (bx, by, bx+300, by+max(badge_size*2, 40)), min(15, badge_size), CORAL)
                if badge_size > 30:
                    year_font = get_font(min(badge_size, 80), bold=True)
                    draw.text((bx+50, by+badge_size//2-10), "2026", fill=WHITE, font=year_font)

        # Subtitle fades in
        if scene_t > 0.5:
            sub_t = min((scene_t - 0.5) * 2, 1)
            font_sub = get_font(40, bold=True)
            sub_y = int(lerp(500, 460, ease_out(sub_t)))
            draw.text((100, sub_y), "SPREADSHEET BUNDLE", fill=GOLD, font=font_sub)

        # "6 Spreadsheets" counter
        if scene_t > 0.7:
            count_t = min((scene_t - 0.7) * 3.3, 1)
            count = int(6 * count_t)
            count_font = get_font(120, bold=True)
            label_font = get_font(36)
            draw.text((W//2-80, 580), str(count), fill=GOLD, font=count_font)
            draw.text((W//2-120, 710), "SPREADSHEETS", fill=WHITE, font=label_font)

        # Bottom bar
        draw.rectangle([0, H-80, W, H], fill=GOLD)
        bar_font = get_font(28, bold=True)
        draw.text((W//2-200, H-60), "INSTANT DIGITAL DOWNLOAD", fill=DEEP_GREEN, font=bar_font)

    # ===== SCENE 2: Spreadsheets Fan Out (3-6s) =====
    elif scene == 1:
        draw.rectangle([0, 0, W, H], fill=WHITE)

        # Header
        draw.rectangle([0, 0, W, 100], fill=DEEP_GREEN)
        header_font = get_font(36, bold=True)
        draw.text((W//2-200, 30), "WHAT'S INCLUDED", fill=WHITE, font=header_font)

        sheets = [
            ("Monthly Budget", DEEP_GREEN),
            ("Annual Overview", SAGE_GREEN),
            ("Debt Payoff", CORAL),
            ("Savings Goals", GOLD),
            ("Expense Tracker", DEEP_GREEN),
            ("Bill Calendar", SAGE_GREEN),
        ]

        for i, (name, color) in enumerate(sheets):
            # Stagger the entrance
            delay = i * 0.12
            if scene_t > delay:
                entry_t = ease_out(min((scene_t - delay) * 2.5, 1))
                col = i % 2
                row = i // 2
                target_x = 80 + col * 520
                target_y = 140 + row * 300
                start_x = W + 200
                x = int(lerp(start_x, target_x, entry_t))
                y = target_y

                draw_mini_spreadsheet(draw, x, y, 450, 260, name, color)

                # Checkmark appears after entry
                if entry_t > 0.8:
                    check_t = (entry_t - 0.8) * 5
                    if check_t > 0:
                        draw.ellipse([x+390, y+10, x+430, y+50], fill=SAGE_GREEN)
                        draw_checkmark(draw, x+397, y+18, 20, WHITE)

        # Bottom
        draw.rectangle([0, H-70, W, H], fill=DEEP_GREEN)
        bot_font = get_font(26, bold=True)
        draw.text((W//2-250, H-50), "EXCEL + GOOGLE SHEETS COMPATIBLE", fill=WHITE, font=bot_font)

    # ===== SCENE 3: Features Showcase (6-9s) =====
    elif scene == 2:
        draw.rectangle([0, 0, W, H], fill=WARM_CREAM)

        # Rotating features
        features = [
            ("Auto-Calculating\nFormulas", "Enter your numbers,\nwe do the math", DEEP_GREEN),
            ("40+ Expense\nCategories", "Every spending category\nyou'll ever need", SAGE_GREEN),
            ("Debt Freedom\nTools", "Snowball & avalanche\nstrategies included", CORAL),
            ("Track 10\nSavings Goals", "Visualize progress\ntoward every dream", GOLD),
        ]

        # Determine which feature is showing
        feat_duration = 1.0 / len(features)
        feat_idx = min(int(scene_t / feat_duration), len(features) - 1)
        feat_t = (scene_t - feat_idx * feat_duration) / feat_duration

        title, desc, color = features[feat_idx]

        # Background accent
        draw.rectangle([0, 0, W, 300], fill=color)

        # Feature number
        num_font = get_font(48, bold=True)
        draw.text((50, 30), f"FEATURE {feat_idx+1}/{len(features)}", fill=WHITE, font=num_font)

        # Title with slide-in
        title_x = int(lerp(-400, 80, ease_out(min(feat_t * 3, 1))))
        title_font = get_font(52, bold=True)
        draw.text((title_x, 120), title, fill=WHITE, font=title_font)

        # Description
        if feat_t > 0.2:
            desc_t = ease_out(min((feat_t - 0.2) * 2, 1))
            desc_font = get_font(36)
            desc_y = 370
            draw.text((80, desc_y), desc, fill=CHARCOAL, font=desc_font)

        # Visual element
        if feat_t > 0.3:
            vis_t = ease_out(min((feat_t - 0.3) * 2, 1))
            vis_y = int(lerp(H, 500, vis_t))

            if feat_idx == 0:
                # Formula mockup
                draw_mini_spreadsheet(draw, 150, vis_y, 780, 400, "Auto-Formulas", color)
                # Animated "calculating" effect
                if feat_t > 0.6:
                    calc_t = (feat_t - 0.6) * 2.5
                    for r in range(5):
                        if calc_t > r * 0.15:
                            ry = vis_y + 50 + r * 60
                            draw_rounded_rect(draw, (500, ry, 500+int(250*min((calc_t-r*0.15)*3,1)), ry+25), 5, SAGE_GREEN)

            elif feat_idx == 1:
                # Category grid
                cats = ["Housing", "Food", "Transport", "Health", "Fun", "Bills", "Savings", "Personal"]
                for ci, cat in enumerate(cats):
                    cr = ci // 4
                    cc = ci % 4
                    cx = 100 + cc * 230
                    cy = vis_y + cr * 180
                    cat_color = DEEP_GREEN if ci % 2 == 0 else SAGE_GREEN
                    draw_rounded_rect(draw, (cx, cy, cx+200, cy+150), 12, cat_color)
                    cat_font = get_font(24, bold=True)
                    draw.text((cx+20, cy+60), cat, fill=WHITE, font=cat_font)

            elif feat_idx == 2:
                # Debt progress bars
                debts_vis = [("Card 1", 0.75, CORAL), ("Loan", 0.45, SAGE_GREEN), ("Car", 0.60, GOLD)]
                for di, (dname, dprog, dcol) in enumerate(debts_vis):
                    dy = vis_y + di * 120
                    d_font = get_font(28, bold=True)
                    draw.text((100, dy), dname, fill=CHARCOAL, font=d_font)
                    animated_prog = dprog * min(feat_t * 2, 1)
                    draw_progress_bar(draw, 280, dy+5, 600, 30, animated_prog, dcol)
                    pct_font = get_font(24, bold=True)
                    draw.text((900, dy+5), f"{int(animated_prog*100)}%", fill=dcol, font=pct_font)

            elif feat_idx == 3:
                # Savings goal circles
                goals_vis = [("Emergency", 0.75, DEEP_GREEN), ("Vacation", 0.60, CORAL), ("Home", 0.24, GOLD)]
                for gi, (gname, gprog, gcol) in enumerate(goals_vis):
                    gcx = 200 + gi * 300
                    gcy = vis_y + 120
                    gr = 80
                    animated_prog = gprog * min(feat_t * 2, 1)
                    draw.ellipse([gcx-gr, gcy-gr, gcx+gr, gcy+gr], fill=LIGHT_GRAY)
                    end_angle = int(360 * animated_prog) - 90
                    if animated_prog > 0:
                        draw.pieslice([gcx-gr, gcy-gr, gcx+gr, gcy+gr], -90, end_angle, fill=gcol)
                        inner = gr - 20
                        draw.ellipse([gcx-inner, gcy-inner, gcx+inner, gcy+inner], fill=WHITE)
                    pct_font = get_font(28, bold=True)
                    pct_str = f"{int(animated_prog*100)}%"
                    draw.text((gcx-25, gcy-15), pct_str, fill=gcol, font=pct_font)
                    g_font = get_font(20, bold=True)
                    draw.text((gcx-40, gcy+gr+10), gname, fill=CHARCOAL, font=g_font)

        # Progress dots at bottom
        draw.rectangle([0, H-60, W, H], fill=DEEP_GREEN)
        for di in range(len(features)):
            dot_x = W//2 - 60 + di * 40
            dot_color = GOLD if di == feat_idx else SAGE_GREEN
            dot_r = 10 if di == feat_idx else 6
            draw.ellipse([dot_x-dot_r, H-38-dot_r, dot_x+dot_r, H-38+dot_r], fill=dot_color)

    # ===== SCENE 4: CTA / Closing (9-12s) =====
    elif scene == 3:
        draw.rectangle([0, 0, W, H], fill=DEEP_GREEN)

        # Pulsing background effect
        pulse = 0.5 + 0.5 * math.sin(scene_t * math.pi * 4)
        bg_shade = tuple(int(c + 15 * pulse) for c in DEEP_GREEN)
        draw.rectangle([0, 0, W, H], fill=bg_shade)

        # Central card slides up
        card_y = int(lerp(H, 100, ease_out(min(scene_t * 2, 1))))
        card_w, card_h = 900, 800
        card_x = (W - card_w) // 2

        draw_rounded_rect(draw, (card_x, card_y, card_x+card_w, card_y+card_h), 25, WHITE)

        # Gold corner accents
        draw.polygon([(card_x, card_y), (card_x+50, card_y), (card_x, card_y+50)], fill=GOLD)
        draw.polygon([(card_x+card_w, card_y), (card_x+card_w-50, card_y), (card_x+card_w, card_y+50)], fill=GOLD)

        # Title
        title_font = get_font(46, bold=True)
        draw.text((card_x+100, card_y+50), "GET THE COMPLETE", fill=DEEP_GREEN, font=title_font)
        draw.text((card_x+80, card_y+110), "2026 BUDGET BUNDLE", fill=SAGE_GREEN, font=title_font)

        # Divider
        draw.rectangle([card_x+80, card_y+180, card_x+card_w-80, card_y+184], fill=GOLD)

        # Items with staggered checkmarks
        items = [
            "Monthly Budget Tracker",
            "Annual Overview",
            "Debt Payoff Tracker",
            "Savings Goal Tracker",
            "Daily Expense Log",
            "Bill Payment Calendar",
        ]
        item_font = get_font(30, bold=True)
        for i, item in enumerate(items):
            delay = 0.1 + i * 0.06
            if scene_t > delay:
                iy = card_y + 210 + i * 60
                entry_t = ease_out(min((scene_t - delay) * 3, 1))
                ix = int(lerp(card_x + card_w, card_x + 120, entry_t))
                draw_checkmark(draw, ix, iy+5, 18, DEEP_GREEN)
                draw.text((ix+30, iy), item, fill=CHARCOAL, font=item_font)

        # Price
        if scene_t > 0.5:
            price_t = ease_out(min((scene_t - 0.5) * 2.5, 1))
            price_y = card_y + 600
            price_font = get_font(64, bold=True)
            reg_font = get_font(34)

            # Crossed out price
            draw.text((card_x+150, price_y+10), "$29.99", fill=MEDIUM_GRAY, font=reg_font)
            draw.line([(card_x+150, price_y+32), (card_x+330, price_y+32)], fill=CORAL, width=3)

            # Sale price
            scale = int(64 * price_t)
            if scale > 10:
                sale_font = get_font(min(scale, 64), bold=True)
                draw.text((card_x+380, price_y-10), "$9.99", fill=DEEP_GREEN, font=sale_font)

            # Save badge
            if scene_t > 0.7:
                draw_rounded_rect(draw, (card_x+620, price_y, card_x+800, price_y+50), 12, CORAL)
                save_font = get_font(24, bold=True)
                draw.text((card_x+635, price_y+10), "SAVE 67%", fill=WHITE, font=save_font)

        # CTA Button with pulse
        if scene_t > 0.6:
            btn_pulse = 1 + 0.03 * math.sin(scene_t * math.pi * 8)
            btn_w = int(500 * btn_pulse)
            btn_h = int(70 * btn_pulse)
            btn_x = card_x + (card_w - btn_w) // 2
            btn_y = card_y + 700
            draw_rounded_rect(draw, (btn_x, btn_y, btn_x+btn_w, btn_y+btn_h), 35, CORAL)
            btn_font = get_font(32, bold=True)
            draw.text((btn_x+130, btn_y+18), "ADD TO CART", fill=WHITE, font=btn_font)

        # Bottom bar
        draw.rectangle([0, H-60, W, H], fill=GOLD)
        bot_font = get_font(24, bold=True)
        draw.text((W//2-200, H-45), "INSTANT DOWNLOAD  |  EXCEL + SHEETS", fill=DEEP_GREEN, font=bot_font)

    return img


def create_video_from_frames():
    """Create MP4 video from frames using raw frame assembly"""

    print("Generating video frames...")
    frames = []
    for i in range(TOTAL_FRAMES):
        frame = generate_frame(i)
        frames.append(frame)
        if i % 30 == 0:
            print(f"  Frame {i}/{TOTAL_FRAMES} ({i*100//TOTAL_FRAMES}%)")

    # Save as individual frames, then use ffmpeg if available
    frames_dir = os.path.join(OUT_DIR, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    for i, frame in enumerate(frames):
        frame.save(os.path.join(frames_dir, f"frame_{i:04d}.jpg"), "JPEG", quality=85)

    print(f"Saved {len(frames)} frames")

    # Try ffmpeg
    import subprocess
    ffmpeg_path = None
    for p in ["/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
        if os.path.exists(p):
            ffmpeg_path = p
            break

    if ffmpeg_path is None:
        result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)
        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip()

    output_path = os.path.join(OUT_DIR, "budget_bundle_promo.mp4")

    if ffmpeg_path:
        cmd = [
            ffmpeg_path,
            "-y",
            "-framerate", str(FPS),
            "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "23",
            "-t", str(DURATION),
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Created video: {output_path}")
        else:
            print(f"ffmpeg error: {result.stderr[:500]}")
            # Fall back to GIF
            gif_path = os.path.join(OUT_DIR, "budget_bundle_promo.gif")
            # Use every 3rd frame for smaller GIF
            gif_frames = frames[::3]
            gif_frames[0].save(
                gif_path,
                save_all=True,
                append_images=gif_frames[1:],
                duration=100,
                loop=0,
                optimize=True
            )
            print(f"Created GIF fallback: {gif_path}")
    else:
        print("ffmpeg not found, creating GIF...")
        gif_path = os.path.join(OUT_DIR, "budget_bundle_promo.gif")
        gif_frames = frames[::3]
        gif_frames[0].save(
            gif_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=100,
            loop=0,
            optimize=True
        )
        print(f"Created GIF: {gif_path}")

    # Cleanup frames
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)

    return output_path


if __name__ == "__main__":
    print("Creating promotional video...")
    print("=" * 50)
    create_video_from_frames()
    print("=" * 50)
    print("Video creation complete!")
