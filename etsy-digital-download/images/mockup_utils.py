"""
Shared device mockup utilities for Etsy listing images.
Creates realistic iPad-style mockups with filled-in spreadsheet content.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill_color, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill_color, outline=outline, width=width)

def draw_centered_text(draw, text, y, font, color, img_width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img_width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)

def draw_ipad(draw, x, y, w, h, bezel=28, corner=30):
    """Draw an iPad-style device frame with shadow."""
    # Shadow
    shadow_offset = 12
    draw_rounded_rect(draw, (x + shadow_offset, y + shadow_offset,
                             x + w + shadow_offset, y + h + shadow_offset),
                      corner + 5, (180, 180, 180, 80))
    # Outer bezel (dark gray)
    draw_rounded_rect(draw, (x, y, x + w, y + h), corner, (40, 40, 40))
    # Inner bezel (slightly lighter)
    draw_rounded_rect(draw, (x + 3, y + 3, x + w - 3, y + h - 3), corner - 2, (55, 55, 55))
    # Camera dot
    cam_x = x + w // 2
    cam_y = y + bezel // 2
    draw.ellipse([(cam_x - 5, cam_y - 5), (cam_x + 5, cam_y + 5)], fill=(80, 80, 80))
    # Screen area
    screen_x = x + bezel
    screen_y = y + bezel
    screen_w = w - 2 * bezel
    screen_h = h - 2 * bezel
    draw.rectangle([(screen_x, screen_y), (screen_x + screen_w, screen_y + screen_h)], fill=(255, 255, 255))
    return screen_x, screen_y, screen_w, screen_h

def draw_annotation_arrow(draw, start_x, start_y, end_x, end_y, color, width=3):
    """Draw a line with a small arrow tip."""
    draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
    # Simple arrowhead
    import math
    angle = math.atan2(end_y - start_y, end_x - start_x)
    arrow_len = 12
    a1 = angle + math.pi * 0.8
    a2 = angle - math.pi * 0.8
    draw.line([(end_x, end_y), (end_x + arrow_len * math.cos(a1), end_y + arrow_len * math.sin(a1))], fill=color, width=width)
    draw.line([(end_x, end_y), (end_x + arrow_len * math.cos(a2), end_y + arrow_len * math.sin(a2))], fill=color, width=width)

def draw_annotation_label(draw, text, x, y, font, text_color, bg_color, padding=10):
    """Draw a label with rounded background."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw_rounded_rect(draw, (x - padding, y - padding // 2, x + tw + padding, y + th + padding), 8, bg_color)
    draw.text((x, y), text, font=font, fill=text_color)
    return tw, th

def draw_spreadsheet_grid(draw, x, y, cols, rows, col_widths, row_height, header_data,
                          row_data, header_bg, header_fg, alt_row_bg, border_color=(220, 220, 220)):
    """Draw a mini spreadsheet table with headers and data."""
    font_header = get_font(17, bold=True)
    font_cell = get_font(15)

    # Draw headers
    cx = x
    for i, (header, width) in enumerate(zip(header_data, col_widths)):
        draw.rectangle([(cx, y), (cx + width, y + row_height)], fill=header_bg, outline=border_color)
        draw.text((cx + 6, y + 5), header, font=font_header, fill=header_fg)
        cx += width

    # Draw data rows
    for ri, row in enumerate(row_data):
        ry = y + row_height + ri * row_height
        bg = alt_row_bg if ri % 2 == 1 else (255, 255, 255)
        cx = x
        for ci, (cell, width) in enumerate(zip(row, col_widths)):
            draw.rectangle([(cx, ry), (cx + width, ry + row_height)], fill=bg, outline=border_color)
            color = (44, 44, 44)
            if isinstance(cell, str) and cell.startswith("-$"):
                color = (220, 50, 50)
            elif isinstance(cell, str) and cell.startswith("$") and ci > 0:
                color = (44, 44, 44)
            draw.text((cx + 6, ry + 5), str(cell), font=font_cell, fill=color)
            cx += width

    total_h = row_height + len(row_data) * row_height
    return total_h

def draw_status_badge(draw, text, x, y, color, font=None):
    """Draw a colored status badge."""
    if font is None:
        font = get_font(14, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw_rounded_rect(draw, (x, y, x + tw + 16, y + 22), 6, color)
    draw.text((x + 8, y + 3), text, font=font, fill=(255, 255, 255))
    return tw + 16

def draw_tab_bar(draw, tabs, active_idx, x, y, active_color, inactive_color=(235, 235, 235)):
    """Draw spreadsheet-style tab bar."""
    font = get_font(14)
    tx = x
    for i, tab in enumerate(tabs):
        tw = len(tab) * 9 + 20
        is_active = i == active_idx
        bg = active_color if is_active else inactive_color
        fg = (255, 255, 255) if is_active else (80, 80, 80)
        draw_rounded_rect(draw, (tx, y, tx + tw, y + 28), 6, bg)
        draw.text((tx + 10, y + 6), tab, font=font, fill=fg)
        tx += tw + 4
