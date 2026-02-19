#!/usr/bin/env python3
"""
Minimalist Abstract Gallery Wall Art Set of 6
"Serene Neutrals Collection"

Creates 6 cohesive printable art prints in multiple sizes:
- 2:3 ratio (fits 4x6, 8x12, 12x18, 16x24, 20x30)
- Base resolution: 3600x5400px (300 DPI at 12x18")

Style: Cozy minimalist, neutral palette, organic abstract shapes
Trend: "Mix It Up" - abstract + line art + botanical, unified by color palette

Color Palette: Warm neutrals
- Sand/Warm beige
- Soft terracotta
- Muted sage
- Dusty clay
- Cream/off-white
- Charcoal accents
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

OUTPUT_DIR = "/home/user/claude-code/etsy-digital-planner/wall-art-product/prints"

# Print dimensions (2:3 ratio, 300 DPI equivalent for 12x18")
W, H = 3600, 5400

# Warm Neutral Palette
CREAM = (252, 248, 240)
WARM_SAND = (228, 213, 193)
SOFT_TERRA = (199, 159, 134)
MUTED_SAGE = (173, 188, 168)
DUSTY_CLAY = (189, 149, 130)
WARM_BLUSH = (222, 195, 182)
CHARCOAL = (62, 58, 55)
DEEP_BROWN = (95, 78, 66)
PALE_OLIVE = (195, 195, 170)
LIGHT_LINEN = (245, 240, 232)
OFF_WHITE = (250, 247, 242)

random.seed(42)  # Reproducible results


def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()


def draw_organic_blob(draw, cx, cy, radius, color, irregularity=0.3, spikiness=0.2, num_vertices=12):
    """Draw an organic, blob-like shape."""
    angle_step = 2 * math.pi / num_vertices
    points = []
    for i in range(num_vertices):
        angle = i * angle_step
        r_variation = radius * (1 + random.uniform(-irregularity, irregularity))
        spike = random.uniform(-spikiness, spikiness) * radius
        r = r_variation + spike
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=color)


def draw_smooth_arc(draw, cx, cy, radius, start_angle, end_angle, color, width=8):
    """Draw a smooth arc."""
    steps = 100
    points = []
    for i in range(steps + 1):
        t = start_angle + (end_angle - start_angle) * i / steps
        x = cx + radius * math.cos(t)
        y = cy + radius * math.sin(t)
        points.append((x, y))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=width)


def draw_bezier_curve(draw, p0, p1, p2, p3, color, width=6, steps=80):
    """Draw a cubic bezier curve."""
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=width)


# ──────────────────────────────────────────────────────────
# PRINT 1: "Horizon" - Abstract landscape layers
# Overlapping organic shapes suggesting hills/horizon
# ──────────────────────────────────────────────────────────

def create_print_01_horizon():
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Layer 1: Background - soft warm wash at top
    for y in range(H // 3):
        alpha = y / (H // 3)
        r = int(CREAM[0] + (LIGHT_LINEN[0] - CREAM[0]) * alpha)
        g = int(CREAM[1] + (LIGHT_LINEN[1] - CREAM[1]) * alpha)
        b = int(CREAM[2] + (LIGHT_LINEN[2] - CREAM[2]) * alpha)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Layer 2: Large organic shape - soft sage (back mountain)
    points = []
    base_y = H * 0.55
    for x in range(0, W + 50, 50):
        y_offset = math.sin(x * 0.002) * 400 + math.sin(x * 0.005) * 200
        points.append((x, base_y + y_offset))
    points.append((W, H))
    points.append((0, H))
    draw.polygon(points, fill=MUTED_SAGE)

    # Layer 3: Mid organic shape - warm sand
    points = []
    base_y = H * 0.62
    for x in range(0, W + 50, 50):
        y_offset = math.sin(x * 0.003 + 1) * 350 + math.sin(x * 0.007) * 150
        points.append((x, base_y + y_offset))
    points.append((W, H))
    points.append((0, H))
    draw.polygon(points, fill=WARM_SAND)

    # Layer 4: Front organic shape - soft terracotta
    points = []
    base_y = H * 0.72
    for x in range(0, W + 50, 50):
        y_offset = math.sin(x * 0.004 + 2) * 300 + math.sin(x * 0.008) * 100
        points.append((x, base_y + y_offset))
    points.append((W, H))
    points.append((0, H))
    draw.polygon(points, fill=SOFT_TERRA)

    # Layer 5: Foreground - dusty clay
    points = []
    base_y = H * 0.82
    for x in range(0, W + 50, 50):
        y_offset = math.sin(x * 0.005 + 3) * 200 + math.sin(x * 0.01) * 80
        points.append((x, base_y + y_offset))
    points.append((W, H))
    points.append((0, H))
    draw.polygon(points, fill=DUSTY_CLAY)

    # Sun circle
    sun_x, sun_y = W * 0.65, H * 0.28
    sun_r = 280
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=WARM_BLUSH)

    img.save(os.path.join(OUTPUT_DIR, "print_01_horizon.png"), quality=95)
    print("Created: print_01_horizon.png")


# ──────────────────────────────────────────────────────────
# PRINT 2: "Botanical Line" - Minimal single-line botanical
# Continuous line drawing of a leaf/branch on cream
# ──────────────────────────────────────────────────────────

def create_print_02_botanical():
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Main stem - gentle S-curve
    stem_width = 10
    cx = W // 2

    # Draw main stem with bezier
    draw_bezier_curve(draw,
        (cx, H * 0.85),
        (cx - 200, H * 0.65),
        (cx + 200, H * 0.4),
        (cx - 50, H * 0.18),
        CHARCOAL, width=stem_width)

    # Leaves branching off - pairs of bezier curves
    leaf_data = [
        # (branch_point_y_ratio, direction, size_factor)
        (0.72, -1, 1.0),
        (0.68, 1, 0.9),
        (0.58, -1, 1.1),
        (0.54, 1, 0.85),
        (0.45, -1, 0.95),
        (0.42, 1, 0.8),
        (0.35, -1, 0.7),
        (0.32, 1, 0.65),
        (0.26, -1, 0.55),
        (0.24, 1, 0.5),
    ]

    for y_ratio, direction, size in leaf_data:
        # Calculate stem position at this y
        t = 1.0 - (y_ratio - 0.18) / (0.85 - 0.18)
        stem_x = cx + math.sin(t * math.pi * 1.5) * 150

        by = H * y_ratio
        leaf_len = 500 * size
        leaf_w = 250 * size

        # Leaf outline (two bezier curves forming a leaf shape)
        tip_x = stem_x + direction * leaf_len
        tip_y = by - 150 * size

        # Upper edge of leaf
        draw_bezier_curve(draw,
            (stem_x, by),
            (stem_x + direction * leaf_len * 0.3, by - leaf_w * 0.6),
            (tip_x - direction * leaf_len * 0.2, tip_y - leaf_w * 0.2),
            (tip_x, tip_y),
            CHARCOAL, width=7, steps=60)

        # Lower edge of leaf
        draw_bezier_curve(draw,
            (stem_x, by),
            (stem_x + direction * leaf_len * 0.4, by + leaf_w * 0.3),
            (tip_x - direction * leaf_len * 0.1, tip_y + leaf_w * 0.3),
            (tip_x, tip_y),
            CHARCOAL, width=7, steps=60)

        # Center vein
        draw_bezier_curve(draw,
            (stem_x, by),
            (stem_x + direction * leaf_len * 0.35, by - leaf_w * 0.15),
            (tip_x - direction * leaf_len * 0.15, tip_y + leaf_w * 0.05),
            (tip_x, tip_y),
            CHARCOAL, width=4, steps=40)

    img.save(os.path.join(OUTPUT_DIR, "print_02_botanical_line.png"), quality=95)
    print("Created: print_02_botanical_line.png")


# ──────────────────────────────────────────────────────────
# PRINT 3: "Arches" - Overlapping geometric arches
# Layered rainbow/arch shapes in neutral tones
# ──────────────────────────────────────────────────────────

def create_print_03_arches():
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Center point for arches
    cx = W // 2
    base_y = H * 0.72

    # Draw arches from outside in (largest first)
    arches = [
        (1400, MUTED_SAGE),
        (1150, WARM_SAND),
        (900, SOFT_TERRA),
        (700, DUSTY_CLAY),
        (500, WARM_BLUSH),
    ]

    for radius, color in arches:
        # Draw filled semi-circle (arch)
        arch_width = radius * 2
        arch_height = radius

        # Upper arch
        bbox = [cx - radius, base_y - radius, cx + radius, base_y + radius]
        draw.pieslice(bbox, 180, 360, fill=color)

        # Rectangle below to close the arch
        draw.rectangle([cx - radius, base_y, cx + radius, H], fill=color)

    # Cover bottom with cream to show only arches
    draw.rectangle([0, base_y, W, H], fill=CREAM)

    # Redraw just the arch parts (semi-circles only)
    for radius, color in arches:
        bbox = [cx - radius, base_y - radius, cx + radius, base_y + radius]
        draw.pieslice(bbox, 180, 360, fill=color)

    img.save(os.path.join(OUTPUT_DIR, "print_03_arches.png"), quality=95)
    print("Created: print_03_arches.png")


# ──────────────────────────────────────────────────────────
# PRINT 4: "Orbs" - Abstract circles/dots composition
# Floating organic circles in various sizes
# ──────────────────────────────────────────────────────────

def create_print_04_orbs():
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Define circles with positions, sizes, colors
    circles = [
        # (cx_ratio, cy_ratio, radius, color)
        (0.25, 0.20, 450, MUTED_SAGE),
        (0.70, 0.15, 350, WARM_BLUSH),
        (0.50, 0.40, 550, SOFT_TERRA),
        (0.20, 0.55, 380, WARM_SAND),
        (0.75, 0.50, 420, PALE_OLIVE),
        (0.40, 0.70, 500, DUSTY_CLAY),
        (0.65, 0.75, 320, MUTED_SAGE),
        (0.30, 0.85, 280, WARM_BLUSH),
        (0.80, 0.88, 350, WARM_SAND),
        # Small accent dots
        (0.15, 0.35, 120, SOFT_TERRA),
        (0.85, 0.32, 100, DUSTY_CLAY),
        (0.55, 0.12, 90, PALE_OLIVE),
        (0.10, 0.78, 110, MUTED_SAGE),
        (0.90, 0.65, 95, WARM_BLUSH),
    ]

    for cx_r, cy_r, radius, color in circles:
        cx = int(W * cx_r)
        cy = int(H * cy_r)
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)

    img.save(os.path.join(OUTPUT_DIR, "print_04_orbs.png"), quality=95)
    print("Created: print_04_orbs.png")


# ──────────────────────────────────────────────────────────
# PRINT 5: "Body Line" - Minimal figure line art
# Abstract single-line female form/silhouette
# ──────────────────────────────────────────────────────────

def create_print_05_figure_line():
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Abstract female figure - continuous flowing line
    # Head
    head_cx, head_cy = W * 0.48, H * 0.15
    head_r = 180
    draw.arc([head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
             30, 330, fill=CHARCOAL, width=10)

    # Neck
    draw_bezier_curve(draw,
        (head_cx - 60, head_cy + head_r * 0.85),
        (head_cx - 80, head_cy + head_r + 100),
        (head_cx - 120, head_cy + head_r + 180),
        (head_cx - 180, head_cy + head_r + 300),
        CHARCOAL, width=10)

    # Left shoulder flowing to back
    draw_bezier_curve(draw,
        (head_cx - 180, head_cy + head_r + 300),
        (head_cx - 500, head_cy + head_r + 350),
        (head_cx - 600, head_cy + head_r + 500),
        (head_cx - 550, head_cy + head_r + 800),
        CHARCOAL, width=10)

    # Torso curve - left side
    draw_bezier_curve(draw,
        (head_cx - 550, head_cy + head_r + 800),
        (head_cx - 450, head_cy + head_r + 1100),
        (head_cx - 380, head_cy + head_r + 1400),
        (head_cx - 500, head_cy + head_r + 1700),
        CHARCOAL, width=10)

    # Right shoulder
    draw_bezier_curve(draw,
        (head_cx + 50, head_cy + head_r * 0.9),
        (head_cx + 200, head_cy + head_r + 120),
        (head_cx + 400, head_cy + head_r + 200),
        (head_cx + 500, head_cy + head_r + 350),
        CHARCOAL, width=10)

    # Right arm flowing down
    draw_bezier_curve(draw,
        (head_cx + 500, head_cy + head_r + 350),
        (head_cx + 550, head_cy + head_r + 600),
        (head_cx + 450, head_cy + head_r + 900),
        (head_cx + 350, head_cy + head_r + 1200),
        CHARCOAL, width=10)

    # Torso curve - right side
    draw_bezier_curve(draw,
        (head_cx + 350, head_cy + head_r + 600),
        (head_cx + 300, head_cy + head_r + 900),
        (head_cx + 200, head_cy + head_r + 1200),
        (head_cx + 100, head_cy + head_r + 1600),
        CHARCOAL, width=8)

    # Abstract color accent - soft blob behind figure
    draw_organic_blob(draw, W * 0.55, H * 0.45, 600, WARM_BLUSH, 0.25, 0.15)

    # Redraw lines on top of blob (re-render key parts)
    # Left torso
    draw_bezier_curve(draw,
        (head_cx - 550, head_cy + head_r + 800),
        (head_cx - 450, head_cy + head_r + 1100),
        (head_cx - 380, head_cy + head_r + 1400),
        (head_cx - 500, head_cy + head_r + 1700),
        CHARCOAL, width=10)

    img.save(os.path.join(OUTPUT_DIR, "print_05_figure_line.png"), quality=95)
    print("Created: print_05_figure_line.png")


# ──────────────────────────────────────────────────────────
# PRINT 6: "Brushstrokes" - Abstract brushstroke composition
# Bold organic brushstrokes in neutral tones
# ──────────────────────────────────────────────────────────

def create_print_06_brushstrokes():
    img = Image.new('RGB', (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Large sweeping brushstrokes
    strokes = [
        # Terracotta diagonal sweep
        ((300, H * 0.15), (800, H * 0.12), (W * 0.6, H * 0.25), (W * 0.85, H * 0.2), SOFT_TERRA, 180),
        # Sage horizontal
        ((200, H * 0.35), (W * 0.3, H * 0.33), (W * 0.6, H * 0.38), (W - 300, H * 0.36), MUTED_SAGE, 160),
        # Sand wide arc
        ((500, H * 0.50), (W * 0.25, H * 0.45), (W * 0.7, H * 0.52), (W - 200, H * 0.48), WARM_SAND, 200),
        # Clay accent
        ((W * 0.1, H * 0.65), (W * 0.35, H * 0.62), (W * 0.55, H * 0.68), (W * 0.75, H * 0.64), DUSTY_CLAY, 140),
        # Blush low sweep
        ((100, H * 0.78), (W * 0.3, H * 0.76), (W * 0.65, H * 0.82), (W * 0.9, H * 0.80), WARM_BLUSH, 170),
    ]

    for p0, p1, p2, p3, color, width in strokes:
        # Draw thick brushstroke using multiple offset beziers
        for offset in range(-width // 2, width // 2, 3):
            opacity_factor = 1.0 - abs(offset) / (width / 2) * 0.3
            p0_off = (p0[0], p0[1] + offset)
            p1_off = (p1[0], p1[1] + offset)
            p2_off = (p2[0], p2[1] + offset)
            p3_off = (p3[0], p3[1] + offset)
            draw_bezier_curve(draw, p0_off, p1_off, p2_off, p3_off, color, width=4, steps=100)

    # Small charcoal accent lines
    draw_bezier_curve(draw,
        (W * 0.15, H * 0.28), (W * 0.25, H * 0.26),
        (W * 0.35, H * 0.30), (W * 0.45, H * 0.27),
        CHARCOAL, width=6)

    draw_bezier_curve(draw,
        (W * 0.55, H * 0.55), (W * 0.65, H * 0.53),
        (W * 0.75, H * 0.57), (W * 0.85, H * 0.54),
        CHARCOAL, width=5)

    # Small dots as accents
    accent_dots = [
        (W * 0.12, H * 0.42, 40, CHARCOAL),
        (W * 0.88, H * 0.30, 35, DEEP_BROWN),
        (W * 0.45, H * 0.88, 45, CHARCOAL),
        (W * 0.72, H * 0.72, 30, DEEP_BROWN),
    ]
    for dx, dy, dr, dc in accent_dots:
        draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=dc)

    img.save(os.path.join(OUTPUT_DIR, "print_06_brushstrokes.png"), quality=95)
    print("Created: print_06_brushstrokes.png")


if __name__ == "__main__":
    print("Creating 6 Minimalist Abstract Gallery Wall Art Prints...")
    print("Serene Neutrals Collection\n")
    create_print_01_horizon()
    create_print_02_botanical()
    create_print_03_arches()
    create_print_04_orbs()
    create_print_05_figure_line()
    create_print_06_brushstrokes()
    print(f"\nAll 6 prints created at {OUTPUT_DIR}")
    print(f"Resolution: {W}x{H}px (300 DPI at 12x18\")")
