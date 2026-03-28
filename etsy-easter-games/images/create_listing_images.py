"""
Create 10 professional Etsy listing images for the Easter Party Games Bundle.
Uses PIL/Pillow to generate high-quality 2700x2025 (4:3) images.

Images:
1.  Main hero/thumbnail
2.  What's included (25 games overview)
3.  Word & Trivia games preview
4.  Party games preview
5.  Kids activities preview
6.  Activity pages preview
7.  How it works (4 steps)
8.  Size & format info
9.  Perfect for (use cases)
10. Value proposition / CTA
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Etsy recommended listing image size (4:3)
W, H = 2700, 2025

# ── Easter Pastel Color Palette ──
SOFT_PINK = (255, 209, 220)
PASTEL_PINK = (255, 182, 203)
LAVENDER = (200, 182, 232)
SOFT_PURPLE = (167, 139, 207)
MINT_GREEN = (176, 224, 196)
SOFT_GREEN = (134, 200, 158)
BUTTER_YELLOW = (255, 245, 186)
SOFT_YELLOW = (255, 234, 138)
SKY_BLUE = (174, 214, 241)
SOFT_BLUE = (133, 193, 233)
PEACH = (255, 218, 185)
CORAL = (255, 160, 122)

# Neutrals
WHITE = (255, 255, 255)
CREAM = (255, 253, 248)
OFF_WHITE = (248, 246, 243)
LIGHT_GRAY = (240, 240, 240)
MED_GRAY = (180, 180, 180)
DARK_TEXT = (55, 55, 70)
CHARCOAL = (40, 40, 55)

# Accent colors
DEEP_PURPLE = (102, 51, 153)
DEEP_PINK = (199, 21, 133)
FOREST_GREEN = (60, 130, 80)
GOLD_ACCENT = (255, 193, 37)
WARM_BROWN = (139, 90, 43)


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, text, y, font, color, canvas_width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]


def text_at(draw, text, x, y, font, color):
    draw.text((x, y), text, font=font, fill=color)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_egg(draw, cx, cy, w, h, fill_color, outline_color=None):
    """Draw an egg shape (ellipse with slightly pointed top)."""
    draw.ellipse([(cx - w//2, cy - h//2), (cx + w//2, cy + h//2)], fill=fill_color, outline=outline_color, width=2)


def draw_bunny_ears(draw, cx, cy, size, color):
    """Draw simple bunny ear silhouettes."""
    ear_w = size // 3
    ear_h = size
    # Left ear
    draw.ellipse([(cx - ear_w - 5, cy - ear_h), (cx - 5, cy + 10)], fill=color)
    draw.ellipse([(cx - ear_w + 5, cy - ear_h + 10), (cx - 15, cy)], fill=SOFT_PINK)
    # Right ear
    draw.ellipse([(cx + 5, cy - ear_h), (cx + ear_w + 5, cy + 10)], fill=color)
    draw.ellipse([(cx + 15, cy - ear_h + 10), (cx + ear_w - 5, cy)], fill=SOFT_PINK)


def draw_scattered_eggs(draw, count=12, region=None):
    """Draw decorative scattered Easter eggs in the background."""
    import random
    random.seed(42)
    if region is None:
        region = (0, 0, W, H)
    colors = [SOFT_PINK, LAVENDER, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE, PEACH]
    for i in range(count):
        ex = random.randint(region[0] + 30, region[2] - 30)
        ey = random.randint(region[1] + 30, region[3] - 30)
        ew = random.randint(25, 50)
        eh = int(ew * 1.3)
        c = colors[i % len(colors)]
        # Make semi-transparent by using a lighter version
        light_c = tuple(min(255, v + 40) for v in c)
        draw_egg(draw, ex, ey, ew, eh, light_c)


def draw_dotted_border(draw, xy, color, dot_size=8, gap=16):
    """Draw a dotted border rectangle."""
    x0, y0, x1, y1 = xy
    # Top
    for x in range(x0, x1, dot_size + gap):
        draw.ellipse([(x, y0 - dot_size//2), (x + dot_size, y0 + dot_size//2)], fill=color)
    # Bottom
    for x in range(x0, x1, dot_size + gap):
        draw.ellipse([(x, y1 - dot_size//2), (x + dot_size, y1 + dot_size//2)], fill=color)
    # Left
    for y in range(y0, y1, dot_size + gap):
        draw.ellipse([(x0 - dot_size//2, y), (x0 + dot_size//2, y + dot_size)], fill=color)
    # Right
    for y in range(y0, y1, dot_size + gap):
        draw.ellipse([(x1 - dot_size//2, y), (x1 + dot_size//2, y + dot_size)], fill=color)


def draw_spring_flowers(draw, cx, cy, size, color):
    """Draw a simple spring flower."""
    petal_r = size // 3
    for angle in range(0, 360, 72):
        rad = math.radians(angle)
        px = cx + int(math.cos(rad) * size // 2)
        py = cy + int(math.sin(rad) * size // 2)
        draw.ellipse([(px - petal_r, py - petal_r), (px + petal_r, py + petal_r)], fill=color)
    # Center
    draw.ellipse([(cx - petal_r//2, cy - petal_r//2), (cx + petal_r//2, cy + petal_r//2)], fill=BUTTER_YELLOW)


# ═══════════════════════════════════════════════════
#  IMAGE 1: MAIN HERO / THUMBNAIL
# ═══════════════════════════════════════════════════
def create_image_01_hero():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Soft wavy background accent
    for y_off in range(0, H, 200):
        color = SOFT_PINK if (y_off // 200) % 2 == 0 else BUTTER_YELLOW
        light = tuple(min(255, c + 30) for c in color)
        for x in range(0, W, 4):
            wave_y = y_off + int(20 * math.sin(x / 80))
            draw.rectangle([(x, wave_y), (x + 3, wave_y + 3)], fill=light)

    # Scattered decorative eggs in background
    draw_scattered_eggs(draw, 15)

    # Top banner with bunny ears
    rounded_rect(draw, (0, 0, W, 160), 0, SOFT_PURPLE)
    font_banner = get_font(42, bold=True)
    center_text(draw, "INSTANT DOWNLOAD  |  PRINT & PLAY  |  ALL AGES", 55, font_banner, WHITE)

    # Main content card
    rounded_rect(draw, (100, 220, W - 100, H - 160), 40, WHITE, outline=LAVENDER, width=4)

    # Inner accent bar
    rounded_rect(draw, (100, 220, W - 100, 310), 0, LAVENDER)
    font_badge = get_font(38, bold=True)
    center_text(draw, "25 PRINTABLE GAMES & ACTIVITIES  |  FAMILIES  |  CLASSROOMS  |  PARTIES", 240, font_badge, WHITE)

    # Bunny ears at top center
    draw_bunny_ears(draw, W // 2, 230, 80, SOFT_PINK)

    # Main title
    font_title_lg = get_font(120, bold=True)
    font_title_md = get_font(100, bold=True)
    center_text(draw, "EASTER", 350, font_title_lg, DEEP_PURPLE)
    center_text(draw, "PARTY GAMES", 490, font_title_md, DEEP_PURPLE)
    center_text(draw, "BUNDLE", 610, font_title_lg, DEEP_PURPLE)

    # Year / edition badge
    font_year = get_font(64, bold=True)
    badge_w, badge_h = 240, 80
    badge_x = (W - badge_w) // 2
    badge_y = 760
    rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), 40, CORAL)
    center_text(draw, "2026", badge_y + 8, font_year, WHITE)

    # Easter eggs decoration flanking the badge
    for offset in [-200, -140, 140, 200]:
        color = [SOFT_PINK, LAVENDER, MINT_GREEN, SKY_BLUE][(offset + 200) // 70 % 4]
        draw_egg(draw, W // 2 + offset, badge_y + 40, 40, 52, color)

    # Feature highlights in pastel cards
    features = [
        ("Word Games", LAVENDER, "Trivia, Word Search,\nCrossword & More"),
        ("Party Games", SOFT_PINK, "Bingo, Charades,\nPictionary & More"),
        ("Kids Activities", MINT_GREEN, "Coloring, Mazes,\nI Spy & More"),
        ("Bonus Pages", BUTTER_YELLOW, "Scavenger Hunt,\nPhoto Props & More"),
    ]

    card_w = 540
    card_h = 220
    gap = 40
    total_w = len(features) * card_w + (len(features) - 1) * gap
    start_x = (W - total_w) // 2
    card_y = 890

    font_feat_title = get_font(36, bold=True)
    font_feat_body = get_font(28)

    for i, (title, color, body) in enumerate(features):
        x = start_x + i * (card_w + gap)
        rounded_rect(draw, (x, card_y, x + card_w, card_y + card_h), 20, color)
        # Title
        bbox = draw.textbbox((0, 0), title, font=font_feat_title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, card_y + 20), title, font=font_feat_title, fill=CHARCOAL)
        # Body
        lines = body.split("\n")
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_feat_body)
            tw = bbox[2] - bbox[0]
            draw.text((x + (card_w - tw) // 2, card_y + 80 + li * 45), line, font=font_feat_body, fill=DARK_TEXT)

    # Decorative divider
    div_y = 1150
    draw.line([(300, div_y), (W - 300, div_y)], fill=LAVENDER, width=3)
    # Small eggs on divider
    for xpos in [W // 2 - 100, W // 2, W // 2 + 100]:
        draw_egg(draw, xpos, div_y, 20, 26, SOFT_PINK)

    # Value proposition text
    font_value = get_font(52, bold=True)
    center_text(draw, "Everything You Need for an Unforgettable Easter!", 1200, font_value, DEEP_PURPLE)

    font_sub = get_font(38)
    center_text(draw, "Download  |  Print  |  Play  |  Repeat All Season Long", 1280, font_sub, DARK_TEXT)

    # Key selling points
    font_bullets = get_font(36, bold=True)
    points = [
        "Ages 3 to 99",
        "US Letter + A4",
        "Print Unlimited Copies",
        "Color + B&W Friendly",
    ]
    point_y = 1370
    point_gap = 590
    start_px = (W - len(points) * point_gap) // 2 + 80
    for i, p in enumerate(points):
        px = start_px + i * point_gap
        # Checkmark circle
        colors_list = [MINT_GREEN, SKY_BLUE, SOFT_PINK, LAVENDER]
        draw.ellipse([(px - 30, point_y), (px + 6, point_y + 36)], fill=colors_list[i])
        text_at(draw, p, px + 20, point_y, font_bullets, DARK_TEXT)

    # Bottom CTA bar
    rounded_rect(draw, (0, H - 140, W, H), 0, DEEP_PURPLE)
    font_cta = get_font(50, bold=True)
    center_text(draw, "DIGITAL DOWNLOAD  |  INSTANT ACCESS  |  PRINT AT HOME", H - 110, font_cta, WHITE)

    img.save(os.path.join(OUT_DIR, "01_hero_main_listing.png"), quality=95)
    print("Created: 01_hero_main_listing.png")


# ═══════════════════════════════════════════════════
#  IMAGE 2: WHAT'S INCLUDED (25 games overview)
# ═══════════════════════════════════════════════════
def create_image_02_whats_included():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    rounded_rect(draw, (0, 0, W, 200), 0, DEEP_PURPLE)
    font_title = get_font(72, bold=True)
    center_text(draw, "WHAT'S INCLUDED", 30, font_title, WHITE)
    font_sub = get_font(38)
    center_text(draw, "25 Beautifully Designed Printable Games & Activities", 120, font_sub, SOFT_PINK)

    # 4 category sections
    categories = [
        ("WORD & TRIVIA GAMES", LAVENDER, DEEP_PURPLE, [
            "Easter Trivia (Easy + Hard)",
            "Word Search (2 levels)",
            "Crossword Puzzle",
            "Word Scramble",
            "Fill-in-the-Blank Stories",
            "A-Z Categories",
            "Scattergories",
        ]),
        ("PARTY GAMES", SOFT_PINK, DEEP_PINK, [
            "Bingo (10 cards + caller)",
            "Emoji Pictionary",
            "Would You Rather",
            "This or That",
            "Charades (40 prompts)",
            "Who Am I?",
            "Hot Take / Opinions",
        ]),
        ("KIDS' FAVORITES", MINT_GREEN, FOREST_GREEN, [
            "I Spy",
            "Dot-to-Dot (3 designs)",
            "Color by Number (3 designs)",
            "Maze Challenge (3 levels)",
            "Matching Memory Game",
            "Scavenger Hunt (In + Out)",
        ]),
        ("ACTIVITY PAGES", BUTTER_YELLOW, WARM_BROWN, [
            "Roll & Draw",
            "Story Starters",
            "Riddles & Jokes Page",
            "Coloring Pages (5 designs)",
            "Photo Props Template",
        ]),
    ]

    col_w = 610
    col_gap = 30
    start_x = (W - 4 * col_w - 3 * col_gap) // 2
    card_y = 240

    font_cat_title = get_font(34, bold=True)
    font_item = get_font(28)

    for i, (title, bg_color, text_color, items) in enumerate(categories):
        x = start_x + i * (col_w + col_gap)
        card_h = 120 + len(items) * 55 + 30

        # Card background
        rounded_rect(draw, (x, card_y, x + col_w, card_y + card_h), 20, WHITE, outline=bg_color, width=3)

        # Category header
        rounded_rect(draw, (x, card_y, x + col_w, card_y + 80), 20, bg_color)
        # Fix bottom corners of header
        draw.rectangle([(x, card_y + 60), (x + col_w, card_y + 80)], fill=bg_color)
        bbox = draw.textbbox((0, 0), title, font=font_cat_title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (col_w - tw) // 2, card_y + 22), title, font=font_cat_title, fill=text_color)

        # Items list
        for j, item in enumerate(items):
            iy = card_y + 100 + j * 55
            # Number circle
            num_color = bg_color
            draw.ellipse([(x + 20, iy + 5), (x + 48, iy + 33)], fill=num_color)
            num_font = get_font(18, bold=True)
            draw.text((x + 28, iy + 8), str(j + 1), font=num_font, fill=text_color)
            # Item text
            draw.text((x + 60, iy + 5), item, font=font_item, fill=DARK_TEXT)

    # Decorative eggs between columns
    for cx in [start_x + col_w + 15, start_x + 2 * (col_w + col_gap) - 15, start_x + 3 * (col_w + col_gap) - 15]:
        for ey_offset in [400, 600, 800]:
            colors = [SOFT_PINK, LAVENDER, MINT_GREEN]
            draw_egg(draw, cx, ey_offset, 20, 26, colors[ey_offset // 200 % 3])

    # Bottom summary bar
    summary_y = H - 320
    rounded_rect(draw, (80, summary_y, W - 80, summary_y + 130), 20, LAVENDER)
    font_summary = get_font(44, bold=True)
    center_text(draw, "25 Games  |  60+ Pages  |  US Letter + A4  |  Answer Keys Included", summary_y + 15, font_summary, DEEP_PURPLE)
    font_summary_sub = get_font(34)
    center_text(draw, "Everything organized in individual PDFs + one complete bundle file", summary_y + 75, font_summary_sub, DARK_TEXT)

    # Bottom bar
    rounded_rect(draw, (0, H - 140, W, H), 0, DEEP_PURPLE)
    font_bottom = get_font(42, bold=True)
    center_text(draw, "INSTANT DOWNLOAD  |  PRINT AT HOME  |  UNLIMITED COPIES", H - 108, font_bottom, WHITE)

    img.save(os.path.join(OUT_DIR, "02_whats_included.png"), quality=95)
    print("Created: 02_whats_included.png")


# ═══════════════════════════════════════════════════
#  IMAGE 3: WORD & TRIVIA GAMES PREVIEW
# ═══════════════════════════════════════════════════
def create_image_03_word_games():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    rounded_rect(draw, (0, 0, W, 180), 0, LAVENDER)
    font_title = get_font(64, bold=True)
    center_text(draw, "WORD & TRIVIA GAMES PREVIEW", 50, font_title, DEEP_PURPLE)

    # Create mockup "pages" showing word games
    # Page 1: Trivia
    page_w, page_h = 720, 900
    pages = [
        ("EASTER TRIVIA", LAVENDER, [
            "1. What does the Easter",
            "   Bunny carry eggs in?",
            "   a) Basket  b) Bag",
            "   c) Bucket  d) Box",
            "",
            "2. How many jelly beans",
            "   are consumed at Easter?",
            "   a) 8 billion  b) 16 billion",
            "   c) 24 billion  d) 1 billion",
            "",
            "3. What flower is most",
            "   associated with Easter?",
            "   a) Rose  b) Lily",
            "   c) Daisy  d) Tulip",
        ]),
        ("WORD SEARCH", SOFT_PINK, [
            "B U N N Y C H I C K",
            "E A S T E R E G G S",
            "S P R I N G L A M B",
            "J E L L Y B E A N S",
            "C H O C O L A T E P",
            "B A S K E T H U N T",
            "F L O W E R S S U N",
            "P A R A D E C R O S",
            "C A R R O T D Y E S",
            "B O N N E T P A I N",
            "",
            "Find: BUNNY, EGGS,",
            "SPRING, BASKET...",
        ]),
        ("CROSSWORD", MINT_GREEN, [
            "      1",
            "    _ _ _ _ _",
            "  2 |       |",
            "  _ _ _ _ _ _",
            "    |   3   |",
            "    _ _ _ _ _ _",
            "        |",
            "  4 _ _ _ _ _",
            "        |",
            "",
            "ACROSS:",
            "2. Fuzzy Easter animal",
            "4. Easter egg activity",
            "DOWN:",
            "1. Spring flower",
        ]),
    ]

    gap = 60
    total_w = len(pages) * page_w + (len(pages) - 1) * gap
    start_x = (W - total_w) // 2
    page_y = 240

    font_page_title = get_font(36, bold=True)
    font_page_content = get_font(24)

    for i, (title, accent, content) in enumerate(pages):
        x = start_x + i * (page_w + gap)

        # Page shadow
        rounded_rect(draw, (x + 8, page_y + 8, x + page_w + 8, page_y + page_h + 8), 15, MED_GRAY)
        # Page
        rounded_rect(draw, (x, page_y, x + page_w, page_y + page_h), 15, WHITE, outline=accent, width=3)

        # Page header
        rounded_rect(draw, (x + 2, page_y + 2, x + page_w - 2, page_y + 80), 13, accent)
        # Easter egg decoration in header
        draw_egg(draw, x + 50, page_y + 42, 30, 38, WHITE)
        draw_egg(draw, x + page_w - 50, page_y + 42, 30, 38, WHITE)
        bbox = draw.textbbox((0, 0), title, font=font_page_title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (page_w - tw) // 2, page_y + 22), title, font=font_page_title, fill=CHARCOAL)

        # Page content
        for j, line in enumerate(content):
            ly = page_y + 110 + j * 48
            draw.text((x + 40, ly), line, font=font_page_content, fill=DARK_TEXT)

    # "Sample Preview" watermark-style text
    font_preview = get_font(28)
    center_text(draw, "Sample previews shown — actual designs are beautifully formatted & print-ready", page_y + page_h + 40, font_preview, MED_GRAY)

    # Also includes section
    also_y = page_y + page_h + 100
    rounded_rect(draw, (200, also_y, W - 200, also_y + 160), 20, LAVENDER)
    font_also = get_font(40, bold=True)
    center_text(draw, "Also Includes: Word Scramble  |  Fill-in-the-Blank  |  A-Z  |  Scattergories", also_y + 20, font_also, DEEP_PURPLE)
    font_also_sub = get_font(32)
    center_text(draw, "7 word & trivia games total — multiple difficulty levels for all ages!", also_y + 85, font_also_sub, DARK_TEXT)

    # Bottom bar
    rounded_rect(draw, (0, H - 120, W, H), 0, DEEP_PURPLE)
    font_bottom = get_font(40, bold=True)
    center_text(draw, "HOURS OF BRAIN-TEASING FUN FOR THE WHOLE FAMILY", H - 90, font_bottom, WHITE)

    img.save(os.path.join(OUT_DIR, "03_game_preview_word.png"), quality=95)
    print("Created: 03_game_preview_word.png")


# ═══════════════════════════════════════════════════
#  IMAGE 4: PARTY GAMES PREVIEW
# ═══════════════════════════════════════════════════
def create_image_04_party_games():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    rounded_rect(draw, (0, 0, W, 180), 0, SOFT_PINK)
    font_title = get_font(64, bold=True)
    center_text(draw, "PARTY GAMES PREVIEW", 50, font_title, DEEP_PINK)

    # Bingo card mockup (large, center-left)
    bingo_x, bingo_y = 100, 240
    bingo_w, bingo_h = 1100, 1050

    # Shadow
    rounded_rect(draw, (bingo_x + 10, bingo_y + 10, bingo_x + bingo_w + 10, bingo_y + bingo_h + 10), 15, MED_GRAY)
    rounded_rect(draw, (bingo_x, bingo_y, bingo_x + bingo_w, bingo_y + bingo_h), 15, WHITE, outline=SOFT_PINK, width=3)

    # Bingo header
    rounded_rect(draw, (bingo_x + 2, bingo_y + 2, bingo_x + bingo_w - 2, bingo_y + 90), 13, SOFT_PINK)
    font_bingo_title = get_font(48, bold=True)
    draw.text((bingo_x + 350, bingo_y + 18), "EASTER BINGO", font=font_bingo_title, fill=DEEP_PINK)

    # Bingo grid
    grid_x = bingo_x + 50
    grid_y = bingo_y + 120
    cell_w = 190
    cell_h = 170
    headers = ["B", "I", "N", "G", "O"]
    header_colors = [LAVENDER, SOFT_PINK, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE]

    font_bingo_header = get_font(52, bold=True)
    font_bingo_cell = get_font(22)

    for col, (letter, color) in enumerate(zip(headers, header_colors)):
        hx = grid_x + col * cell_w
        rounded_rect(draw, (hx, grid_y, hx + cell_w, grid_y + 60), 0, color)
        bbox = draw.textbbox((0, 0), letter, font=font_bingo_header)
        tw = bbox[2] - bbox[0]
        draw.text((hx + (cell_w - tw) // 2, grid_y + 2), letter, font=font_bingo_header, fill=CHARCOAL)

    bingo_items = [
        ["Easter\nBunny", "Jelly\nBeans", "Easter\nEgg", "Spring\nFlower", "Choco\nBunny"],
        ["Easter\nBasket", "Lamb", "Bonnet", "FREE\nSPACE", "Dyed\nEggs"],
        ["Peeps", "Carrot", "Cross", "Lily", "Chick"],
        ["Parade", "Hunt", "Sunrise", "Tulip", "Nest"],
    ]

    for row_idx, row in enumerate(bingo_items):
        for col_idx, item in enumerate(row):
            cx = grid_x + col_idx * cell_w
            cy = grid_y + 60 + row_idx * cell_h
            bg = header_colors[col_idx] if item == "FREE\nSPACE" else WHITE
            outline = header_colors[col_idx]
            rounded_rect(draw, (cx, cy, cx + cell_w, cy + cell_h), 0, bg, outline=outline, width=1)
            lines = item.split("\n")
            for li, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font_bingo_cell)
                tw = bbox[2] - bbox[0]
                draw.text((cx + (cell_w - tw) // 2, cy + 50 + li * 32 - len(lines) * 16), line, font=font_bingo_cell, fill=DARK_TEXT)

    # Right side: Other party games preview cards
    right_x = 1300
    card_w = 1280
    mini_card_h = 230
    mini_gap = 30

    party_games = [
        ("EMOJI PICTIONARY", LAVENDER, "Guess the Easter word from emojis!\n\n  Egg + Bunny + Basket = ???\n  Church + Sunrise + Cross = ???"),
        ("WOULD YOU RATHER", BUTTER_YELLOW, "Would you rather...\n\n  Have unlimited chocolate eggs OR\n  Find a golden Easter egg worth $100?"),
        ("CHARADES", MINT_GREEN, "40 Easter-themed prompts!\n\n  Act out: Decorating Easter Eggs\n  Act out: The Easter Bunny Hopping"),
        ("THIS OR THAT", PEACH, "Easter Edition Choices:\n\n  Chocolate Bunny OR Jelly Beans?\n  Indoor Hunt OR Outdoor Hunt?"),
    ]

    font_mini_title = get_font(32, bold=True)
    font_mini_body = get_font(24)

    for i, (title, color, body) in enumerate(party_games):
        y = 240 + i * (mini_card_h + mini_gap)
        # Shadow
        rounded_rect(draw, (right_x + 6, y + 6, right_x + card_w + 6, y + mini_card_h + 6), 15, MED_GRAY)
        rounded_rect(draw, (right_x, y, right_x + card_w, y + mini_card_h), 15, WHITE, outline=color, width=3)

        # Color accent bar on left
        rounded_rect(draw, (right_x, y, right_x + 12, y + mini_card_h), 6, color)

        draw.text((right_x + 30, y + 15), title, font=font_mini_title, fill=CHARCOAL)
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw.text((right_x + 30, y + 60 + li * 35), line, font=font_mini_body, fill=DARK_TEXT)

    # Also includes note
    also_y = 1340
    rounded_rect(draw, (100, also_y, W - 100, also_y + 100), 20, SOFT_PINK)
    font_also = get_font(38, bold=True)
    center_text(draw, "Also: Who Am I?  |  Hot Take / Opinions  |  10 Unique Bingo Cards + Caller Sheet", also_y + 25, font_also, DEEP_PINK)

    # Bottom bar
    rounded_rect(draw, (0, H - 130, W, H), 0, DEEP_PINK)
    font_bottom = get_font(42, bold=True)
    center_text(draw, "7 PARTY GAMES  |  PERFECT FOR EASTER GATHERINGS OF ANY SIZE", H - 100, font_bottom, WHITE)

    img.save(os.path.join(OUT_DIR, "04_game_preview_party.png"), quality=95)
    print("Created: 04_game_preview_party.png")


# ═══════════════════════════════════════════════════
#  IMAGE 5: KIDS ACTIVITIES PREVIEW
# ═══════════════════════════════════════════════════
def create_image_05_kids_activities():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    rounded_rect(draw, (0, 0, W, 180), 0, MINT_GREEN)
    font_title = get_font(64, bold=True)
    center_text(draw, "KIDS' FAVORITES PREVIEW", 50, font_title, FOREST_GREEN)

    # Activity cards in a 3x2 grid
    activities = [
        ("EASTER I SPY", MINT_GREEN, [
            "Can you find all the",
            "hidden Easter items?",
            "",
            "Eggs: ___    Bunnies: ___",
            "Chicks: ___  Baskets: ___",
            "Flowers: ___ Carrots: ___",
        ]),
        ("COLOR BY NUMBER", SOFT_PINK, [
            "Follow the color key",
            "to reveal the picture!",
            "",
            "1 = Pink    4 = Green",
            "2 = Yellow  5 = Blue",
            "3 = Purple  6 = Orange",
        ]),
        ("EASTER MAZES", SKY_BLUE, [
            "Help the bunny find",
            "the Easter basket!",
            "",
            "3 Difficulty Levels:",
            "  Easy (Ages 3-5)",
            "  Medium (Ages 5-8)",
            "  Hard (Ages 8+)",
        ]),
        ("DOT-TO-DOT", BUTTER_YELLOW, [
            "Connect the dots to",
            "discover the picture!",
            "",
            "3 Designs Included:",
            "  Easter Bunny",
            "  Easter Egg",
            "  Spring Chick",
        ]),
        ("MEMORY MATCH", LAVENDER, [
            "Cut out the cards and",
            "play matching pairs!",
            "",
            "20 Easter-themed",
            "matching cards with",
            "adorable illustrations",
        ]),
        ("SCAVENGER HUNT", PEACH, [
            "Indoor + Outdoor",
            "versions included!",
            "",
            "Find: Something pink",
            "Find: An egg shape",
            "Find: Something soft",
        ]),
    ]

    card_w = 800
    card_h = 460
    col_gap = 50
    row_gap = 40
    cols = 3
    total_w = cols * card_w + (cols - 1) * col_gap
    start_x = (W - total_w) // 2
    start_y = 230

    font_card_title = get_font(36, bold=True)
    font_card_body = get_font(28)

    for i, (title, accent, content) in enumerate(activities):
        col = i % cols
        row = i // cols
        x = start_x + col * (card_w + col_gap)
        y = start_y + row * (card_h + row_gap)

        # Shadow
        rounded_rect(draw, (x + 8, y + 8, x + card_w + 8, y + card_h + 8), 20, MED_GRAY)
        # Card
        rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, WHITE, outline=accent, width=3)
        # Header
        rounded_rect(draw, (x + 2, y + 2, x + card_w - 2, y + 70), 18, accent)
        draw.rectangle([(x + 2, y + 52), (x + card_w - 2, y + 70)], fill=accent)
        # Eggs in header
        draw_egg(draw, x + 45, y + 37, 28, 36, WHITE)
        draw_egg(draw, x + card_w - 45, y + 37, 28, 36, WHITE)
        # Title
        bbox = draw.textbbox((0, 0), title, font=font_card_title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, y + 17), title, font=font_card_title, fill=CHARCOAL)

        # Content
        for j, line in enumerate(content):
            draw.text((x + 40, y + 95 + j * 48), line, font=font_card_body, fill=DARK_TEXT)

    # Bottom section
    bottom_y = H - 320
    rounded_rect(draw, (120, bottom_y, W - 120, bottom_y + 130), 20, MINT_GREEN)
    font_bottom_text = get_font(42, bold=True)
    center_text(draw, "6 Kids' Activities  |  Ages 3+  |  Educational & Fun!", bottom_y + 15, font_bottom_text, FOREST_GREEN)
    font_bottom_sub = get_font(32)
    center_text(draw, "Perfect for keeping little ones entertained at Easter parties & family gatherings", bottom_y + 75, font_bottom_sub, DARK_TEXT)

    # Bottom bar
    rounded_rect(draw, (0, H - 140, W, H), 0, FOREST_GREEN)
    font_bar = get_font(42, bold=True)
    center_text(draw, "KIDS WILL LOVE THESE  |  PARENTS WILL LOVE THE QUIET!", H - 108, font_bar, WHITE)

    img.save(os.path.join(OUT_DIR, "05_game_preview_kids.png"), quality=95)
    print("Created: 05_game_preview_kids.png")


# ═══════════════════════════════════════════════════
#  IMAGE 6: ACTIVITY PAGES PREVIEW
# ═══════════════════════════════════════════════════
def create_image_06_activity_pages():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    rounded_rect(draw, (0, 0, W, 180), 0, BUTTER_YELLOW)
    font_title = get_font(64, bold=True)
    center_text(draw, "BONUS ACTIVITY PAGES", 50, font_title, WARM_BROWN)

    # Activity preview cards
    activities = [
        ("ROLL & DRAW", BUTTER_YELLOW, WARM_BROWN, [
            "Roll the dice and draw",
            "what you get!",
            "",
            "1 = Bunny Ears",
            "2 = Easter Egg",
            "3 = Spring Flower",
            "4 = Baby Chick",
            "5 = Easter Basket",
            "6 = Carrot",
        ]),
        ("STORY STARTERS", LAVENDER, DEEP_PURPLE, [
            "Creative writing prompts:",
            "",
            "\"The Easter Bunny forgot",
            "where he hid the last",
            "golden egg, so he...\"",
            "",
            "\"I woke up on Easter",
            "morning to find a tiny",
            "bunny in my shoe...\"",
        ]),
        ("RIDDLES & JOKES", SOFT_PINK, DEEP_PINK, [
            "Q: What do you call a",
            "rabbit with fleas?",
            "A: Bugs Bunny!",
            "",
            "Q: Why did the Easter",
            "egg hide?",
            "A: Because it was a",
            "little chicken!",
            "",
            "20+ riddles included!",
        ]),
        ("COLORING PAGES", MINT_GREEN, FOREST_GREEN, [
            "5 beautiful Easter",
            "coloring designs:",
            "",
            "1. Easter Bunny Garden",
            "2. Decorated Egg Mandala",
            "3. Spring Basket Scene",
            "4. Baby Animals",
            "5. Easter Celebration",
            "",
            "Detailed + age-friendly",
        ]),
    ]

    card_w = 580
    card_h = 750
    gap = 50
    total_w = len(activities) * card_w + (len(activities) - 1) * gap
    start_x = (W - total_w) // 2
    card_y = 240

    font_card_title = get_font(34, bold=True)
    font_card_body = get_font(26)

    for i, (title, accent, text_color, content) in enumerate(activities):
        x = start_x + i * (card_w + gap)

        # Shadow
        rounded_rect(draw, (x + 8, card_y + 8, x + card_w + 8, card_y + card_h + 8), 20, MED_GRAY)
        # Card
        rounded_rect(draw, (x, card_y, x + card_w, card_y + card_h), 20, WHITE, outline=accent, width=3)
        # Header
        rounded_rect(draw, (x + 2, card_y + 2, x + card_w - 2, card_y + 80), 18, accent)
        draw.rectangle([(x + 2, card_y + 60), (x + card_w - 2, card_y + 80)], fill=accent)
        bbox = draw.textbbox((0, 0), title, font=font_card_title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, card_y + 22), title, font=font_card_title, fill=text_color)

        # Content
        for j, line in enumerate(content):
            draw.text((x + 35, card_y + 110 + j * 50), line, font=font_card_body, fill=DARK_TEXT)

    # Photo props callout
    props_y = card_y + card_h + 60
    rounded_rect(draw, (200, props_y, W - 200, props_y + 200), 25, PEACH)
    font_props_title = get_font(48, bold=True)
    center_text(draw, "BONUS: Easter Party Photo Props Template!", props_y + 25, font_props_title, WARM_BROWN)
    font_props_body = get_font(34)
    center_text(draw, "Bunny ears, carrot, Easter egg, \"Happy Easter\" sign & more!", props_y + 90, font_props_body, DARK_TEXT)
    center_text(draw, "Print, cut, and attach to sticks for instant photo booth fun!", props_y + 135, font_props_body, DARK_TEXT)

    # Bottom bar
    rounded_rect(draw, (0, H - 130, W, H), 0, WARM_BROWN)
    font_bar = get_font(42, bold=True)
    center_text(draw, "5 BONUS ACTIVITIES  |  CREATIVITY + LAUGHTER GUARANTEED", H - 98, font_bar, WHITE)

    img.save(os.path.join(OUT_DIR, "06_game_preview_activity.png"), quality=95)
    print("Created: 06_game_preview_activity.png")


# ═══════════════════════════════════════════════════
#  IMAGE 7: HOW IT WORKS (4 steps)
# ═══════════════════════════════════════════════════
def create_image_07_how_it_works():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Background decoration
    draw_scattered_eggs(draw, 10, (0, 400, W, H - 200))

    # Header
    rounded_rect(draw, (0, 0, W, 200), 0, DEEP_PURPLE)
    font_title = get_font(80, bold=True)
    center_text(draw, "HOW IT WORKS", 25, font_title, WHITE)
    font_sub = get_font(40)
    center_text(draw, "4 Simple Steps to Easter Fun!", 120, font_sub, SOFT_PINK)

    # 4 step cards
    steps = [
        ("1", "PURCHASE", "Add to cart and\ncomplete checkout.\nIt takes just\n30 seconds!", LAVENDER, DEEP_PURPLE),
        ("2", "DOWNLOAD", "Your files are\navailable instantly.\nDownload the ZIP\nfile to your device.", SOFT_PINK, DEEP_PINK),
        ("3", "PRINT", "Print at home or\nat a print shop.\nUS Letter or A4.\nColor or B&W!", MINT_GREEN, FOREST_GREEN),
        ("4", "PLAY!", "Grab some pencils\nand start playing!\nFun for the\nwhole family!", BUTTER_YELLOW, WARM_BROWN),
    ]

    card_w = 560
    card_h = 650
    gap = 50
    total_w = len(steps) * card_w + (len(steps) - 1) * gap
    start_x = (W - total_w) // 2
    card_y = 300

    font_step_num = get_font(100, bold=True)
    font_step_title = get_font(48, bold=True)
    font_step_body = get_font(34)

    for i, (num, title, body, bg_color, text_color) in enumerate(steps):
        x = start_x + i * (card_w + gap)

        # Shadow
        rounded_rect(draw, (x + 8, card_y + 8, x + card_w + 8, card_y + card_h + 8), 25, MED_GRAY)
        # Card
        rounded_rect(draw, (x, card_y, x + card_w, card_y + card_h), 25, WHITE, outline=bg_color, width=4)

        # Large number circle
        circle_r = 70
        circle_x = x + card_w // 2
        circle_y = card_y + 80
        draw.ellipse([(circle_x - circle_r, circle_y - circle_r),
                      (circle_x + circle_r, circle_y + circle_r)], fill=bg_color)
        bbox = draw.textbbox((0, 0), num, font=font_step_num)
        tw = bbox[2] - bbox[0]
        draw.text((circle_x - tw // 2, circle_y - 55), num, font=font_step_num, fill=text_color)

        # Title
        bbox = draw.textbbox((0, 0), title, font=font_step_title)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, card_y + 190), title, font=font_step_title, fill=text_color)

        # Decorative line
        draw.line([(x + 80, card_y + 260), (x + card_w - 80, card_y + 260)], fill=bg_color, width=3)

        # Body
        lines = body.split("\n")
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_step_body)
            tw = bbox[2] - bbox[0]
            draw.text((x + (card_w - tw) // 2, card_y + 290 + li * 60), line, font=font_step_body, fill=DARK_TEXT)

        # Arrow between cards (except last)
        if i < len(steps) - 1:
            arrow_x = x + card_w + gap // 2
            arrow_y = card_y + card_h // 2
            draw.polygon([
                (arrow_x - 15, arrow_y - 20),
                (arrow_x + 15, arrow_y),
                (arrow_x - 15, arrow_y + 20),
            ], fill=LAVENDER)

    # Reassurance bar
    bar_y = card_y + card_h + 80
    rounded_rect(draw, (150, bar_y, W - 150, bar_y + 120), 20, LAVENDER)
    font_reassure = get_font(40, bold=True)
    center_text(draw, "No waiting for shipping!  Download and start playing in under 5 minutes!", bar_y + 35, font_reassure, DEEP_PURPLE)

    # Bottom bar
    rounded_rect(draw, (0, H - 130, W, H), 0, DEEP_PURPLE)
    font_bar = get_font(42, bold=True)
    center_text(draw, "INSTANT ACCESS  |  NO SHIPPING  |  PLAY TODAY", H - 98, font_bar, WHITE)

    img.save(os.path.join(OUT_DIR, "07_how_it_works.png"), quality=95)
    print("Created: 07_how_it_works.png")


# ═══════════════════════════════════════════════════
#  IMAGE 8: SIZE & FORMAT INFO
# ═══════════════════════════════════════════════════
def create_image_08_size_format():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Header
    rounded_rect(draw, (0, 0, W, 180), 0, SKY_BLUE)
    font_title = get_font(64, bold=True)
    center_text(draw, "SIZES, FORMATS & PRINTING TIPS", 50, font_title, CHARCOAL)

    # Two main panels side by side
    panel_w = 1200
    panel_h = 550
    panel_gap = 100
    panel_x1 = (W - 2 * panel_w - panel_gap) // 2
    panel_x2 = panel_x1 + panel_w + panel_gap
    panel_y = 240

    # Panel 1: Sizes
    rounded_rect(draw, (panel_x1 + 6, panel_y + 6, panel_x1 + panel_w + 6, panel_y + panel_h + 6), 20, MED_GRAY)
    rounded_rect(draw, (panel_x1, panel_y, panel_x1 + panel_w, panel_y + panel_h), 20, WHITE, outline=SKY_BLUE, width=3)
    rounded_rect(draw, (panel_x1 + 2, panel_y + 2, panel_x1 + panel_w - 2, panel_y + 80), 18, SKY_BLUE)
    draw.rectangle([(panel_x1 + 2, panel_y + 60), (panel_x1 + panel_w - 2, panel_y + 80)], fill=SKY_BLUE)
    font_panel_title = get_font(40, bold=True)
    draw.text((panel_x1 + 350, panel_y + 18), "TWO SIZES INCLUDED", font=font_panel_title, fill=CHARCOAL)

    font_size_big = get_font(56, bold=True)
    font_size_label = get_font(36, bold=True)
    font_size_detail = get_font(30)

    # US Letter
    box_x = panel_x1 + 80
    box_y = panel_y + 120
    rounded_rect(draw, (box_x, box_y, box_x + 450, box_y + 350), 15, BUTTER_YELLOW)
    center_text(draw, "US LETTER", box_y + 30, font_size_label, WARM_BROWN, canvas_width=box_x * 2 + 450)
    draw.text((box_x + 100, box_y + 90), '8.5" x 11"', font=font_size_big, fill=CHARCOAL)
    draw.text((box_x + 80, box_y + 180), "Standard US paper size", font=font_size_detail, fill=DARK_TEXT)
    draw.text((box_x + 80, box_y + 220), "Perfect for home printing", font=font_size_detail, fill=DARK_TEXT)
    draw.text((box_x + 80, box_y + 260), "Most common in USA/Canada", font=font_size_detail, fill=DARK_TEXT)

    # A4
    box_x2 = panel_x1 + 620
    rounded_rect(draw, (box_x2, box_y, box_x2 + 450, box_y + 350), 15, LAVENDER)
    center_text(draw, "A4 SIZE", box_y + 30, font_size_label, DEEP_PURPLE, canvas_width=box_x2 * 2 + 450)
    draw.text((box_x2 + 70, box_y + 90), "210 x 297mm", font=font_size_big, fill=CHARCOAL)
    draw.text((box_x2 + 80, box_y + 180), "International paper size", font=font_size_detail, fill=DARK_TEXT)
    draw.text((box_x2 + 80, box_y + 220), "Perfect for UK/EU/AU buyers", font=font_size_detail, fill=DARK_TEXT)
    draw.text((box_x2 + 80, box_y + 260), "Standard worldwide format", font=font_size_detail, fill=DARK_TEXT)

    # Panel 2: Printing
    rounded_rect(draw, (panel_x2 + 6, panel_y + 6, panel_x2 + panel_w + 6, panel_y + panel_h + 6), 20, MED_GRAY)
    rounded_rect(draw, (panel_x2, panel_y, panel_x2 + panel_w, panel_y + panel_h), 20, WHITE, outline=CORAL, width=3)
    rounded_rect(draw, (panel_x2 + 2, panel_y + 2, panel_x2 + panel_w - 2, panel_y + 80), 18, CORAL)
    draw.rectangle([(panel_x2 + 2, panel_y + 60), (panel_x2 + panel_w - 2, panel_y + 80)], fill=CORAL)
    draw.text((panel_x2 + 350, panel_y + 18), "PRINTING OPTIONS", font=font_panel_title, fill=WHITE)

    # Color print
    box_y2 = panel_y + 120
    rounded_rect(draw, (panel_x2 + 80, box_y2, panel_x2 + 530, box_y2 + 350), 15, SOFT_PINK)
    center_text(draw, "FULL COLOR", box_y2 + 30, font_size_label, DEEP_PINK, canvas_width=(panel_x2 + 80) * 2 + 450)
    draw.text((panel_x2 + 120, box_y2 + 100), "Gorgeous pastel", font=font_size_detail, fill=DARK_TEXT)
    draw.text((panel_x2 + 120, box_y2 + 140), "Easter designs", font=font_size_detail, fill=DARK_TEXT)
    draw.text((panel_x2 + 120, box_y2 + 200), "Best visual impact", font=font_size_detail, fill=DARK_TEXT)
    draw.text((panel_x2 + 120, box_y2 + 240), "Great for parties!", font=font_size_detail, fill=DARK_TEXT)

    # B&W print
    rounded_rect(draw, (panel_x2 + 620, box_y2, panel_x2 + 1070, box_y2 + 350), 15, LIGHT_GRAY)
    center_text(draw, "BLACK & WHITE", box_y2 + 30, font_size_label, CHARCOAL, canvas_width=(panel_x2 + 620) * 2 + 450)
    draw.text((panel_x2 + 660, box_y2 + 100), "Toner-friendly", font=font_size_detail, fill=DARK_TEXT)
    draw.text((panel_x2 + 660, box_y2 + 140), "design layouts", font=font_size_detail, fill=DARK_TEXT)
    draw.text((panel_x2 + 660, box_y2 + 200), "Saves ink/toner", font=font_size_detail, fill=DARK_TEXT)
    draw.text((panel_x2 + 660, box_y2 + 240), "Still looks great!", font=font_size_detail, fill=DARK_TEXT)

    # What you receive section
    receive_y = panel_y + panel_h + 80
    rounded_rect(draw, (100, receive_y, W - 100, receive_y + 450), 25, WHITE, outline=LAVENDER, width=3)

    font_receive_title = get_font(48, bold=True)
    center_text(draw, "WHAT YOU'LL RECEIVE", receive_y + 30, font_receive_title, DEEP_PURPLE)

    font_receive = get_font(34)
    items = [
        "1 ZIP file containing all game PDFs",
        "25 individual game PDF files (for easy selection)",
        "1 Complete Bundle PDF (all games in one file)",
        "US Letter + A4 versions of every game",
        "Answer keys for all applicable games",
        "Printing tips & recommendations sheet",
    ]

    for i, item in enumerate(items):
        iy = receive_y + 100 + i * 52
        col = MINT_GREEN if i % 2 == 0 else LAVENDER
        draw.ellipse([(250, iy + 5), (278, iy + 33)], fill=col)
        draw.text((300, iy + 3), item, font=font_receive, fill=DARK_TEXT)

    # Bottom bar
    rounded_rect(draw, (0, H - 130, W, H), 0, SKY_BLUE)
    font_bar = get_font(42, bold=True)
    center_text(draw, "PRINT UNLIMITED COPIES  |  ONE PURCHASE = LIFETIME ACCESS", H - 98, font_bar, CHARCOAL)

    img.save(os.path.join(OUT_DIR, "08_size_and_format.png"), quality=95)
    print("Created: 08_size_and_format.png")


# ═══════════════════════════════════════════════════
#  IMAGE 9: PERFECT FOR (Use Cases)
# ═══════════════════════════════════════════════════
def create_image_09_perfect_for():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Background scattered eggs
    draw_scattered_eggs(draw, 8, (0, 300, W, H - 200))

    # Header
    rounded_rect(draw, (0, 0, W, 200), 0, CORAL)
    font_title = get_font(80, bold=True)
    center_text(draw, "PERFECT FOR...", 25, font_title, WHITE)
    font_sub = get_font(40)
    center_text(draw, "So Many Occasions & Celebrations!", 120, font_sub, CREAM)

    # Use case cards in 2 rows of 4
    use_cases = [
        ("Family Easter\nGatherings", SOFT_PINK, DEEP_PINK),
        ("Kids' Easter\nParties", MINT_GREEN, FOREST_GREEN),
        ("Classroom\nCelebrations", LAVENDER, DEEP_PURPLE),
        ("Sunday School\n& Church", BUTTER_YELLOW, WARM_BROWN),
        ("Easter Brunch\nEntertainment", SKY_BLUE, CHARCOAL),
        ("Egg Hunt\nWarm-Up Fun", PEACH, WARM_BROWN),
        ("Virtual Easter\nParties (Zoom!)", SOFT_PINK, DEEP_PINK),
        ("Easter Basket\nStuffers", MINT_GREEN, FOREST_GREEN),
    ]

    card_w = 570
    card_h = 280
    gap_x = 50
    gap_y = 50
    cols = 4
    rows = 2
    total_w = cols * card_w + (cols - 1) * gap_x
    start_x = (W - total_w) // 2
    start_y = 280

    font_case_title = get_font(38, bold=True)

    for i, (title, bg, text_color) in enumerate(use_cases):
        col = i % cols
        row = i // cols
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        # Shadow
        rounded_rect(draw, (x + 6, y + 6, x + card_w + 6, y + card_h + 6), 25, MED_GRAY)
        # Card
        rounded_rect(draw, (x, y, x + card_w, y + card_h), 25, bg, outline=text_color, width=2)

        # Easter egg decoration
        draw_egg(draw, x + card_w // 2, y + 60, 50, 65, WHITE)

        # Title text
        lines = title.split("\n")
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_case_title)
            tw = bbox[2] - bbox[0]
            draw.text((x + (card_w - tw) // 2, y + 120 + li * 55), line, font=font_case_title, fill=text_color)

    # Testimonial-style section
    test_y = start_y + 2 * (card_h + gap_y) + 60
    rounded_rect(draw, (200, test_y, W - 200, test_y + 300), 25, WHITE, outline=LAVENDER, width=3)

    font_stars = get_font(48)
    center_text(draw, "★ ★ ★ ★ ★", test_y + 20, font_stars, GOLD_ACCENT)

    font_quote = get_font(36)
    center_text(draw, '"These games were a HIT at our Easter party! The kids loved', test_y + 90, font_quote, DARK_TEXT)
    center_text(draw, 'the scavenger hunt and the adults couldn\'t stop playing trivia."', test_y + 140, font_quote, DARK_TEXT)

    font_attr = get_font(30, bold=True)
    center_text(draw, "— What families say about Easter game bundles", test_y + 210, font_attr, LAVENDER)

    # Age range bar
    age_y = test_y + 330
    rounded_rect(draw, (300, age_y, W - 300, age_y + 90), 20, LAVENDER)
    font_age = get_font(40, bold=True)
    center_text(draw, "Toddlers  |  Kids  |  Teens  |  Adults  |  Grandparents", age_y + 20, font_age, DEEP_PURPLE)

    # Bottom bar
    rounded_rect(draw, (0, H - 130, W, H), 0, CORAL)
    font_bar = get_font(42, bold=True)
    center_text(draw, "ONE BUNDLE  |  ENDLESS POSSIBILITIES  |  ALL AGES WELCOME", H - 98, font_bar, WHITE)

    img.save(os.path.join(OUT_DIR, "09_perfect_for.png"), quality=95)
    print("Created: 09_perfect_for.png")


# ═══════════════════════════════════════════════════
#  IMAGE 10: VALUE PROPOSITION / CTA
# ═══════════════════════════════════════════════════
def create_image_10_value_prop():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Decorative top accent
    rounded_rect(draw, (0, 0, W, 20), 0, GOLD_ACCENT)

    # Title
    font_title = get_font(72, bold=True)
    center_text(draw, "WHY CHOOSE THIS", 60, font_title, DEEP_PURPLE)
    center_text(draw, "EASTER GAMES BUNDLE?", 150, font_title, DEEP_PURPLE)

    # Decorative divider with eggs
    div_y = 260
    draw.line([(W // 2 - 250, div_y), (W // 2 + 250, div_y)], fill=LAVENDER, width=4)
    draw_egg(draw, W // 2, div_y, 30, 38, SOFT_PINK)

    # Value propositions in 2 columns x 3 rows
    values = [
        ("25 GAMES IN ONE", "More games than any other bundle.\nHours of entertainment for just\none small price.", LAVENDER, DEEP_PURPLE),
        ("ALL AGES WELCOME", "From toddlers to grandparents.\nSomething fun for every single\nperson at your gathering.", SOFT_PINK, DEEP_PINK),
        ("GORGEOUS DESIGN", "Soft Easter pastels with adorable\nillustrations. Not clip-art junk —\nactual beautiful designs.", MINT_GREEN, FOREST_GREEN),
        ("PRINT UNLIMITED", "One purchase = unlimited prints.\nPerfect for large groups, classrooms,\nand multi-day celebrations.", BUTTER_YELLOW, WARM_BROWN),
        ("INSTANT DOWNLOAD", "No waiting for shipping. Download\nand start printing in under\n2 minutes flat.", SKY_BLUE, CHARCOAL),
        ("TWO SIZES INCLUDED", "US Letter AND A4 formats.\nPerfect for buyers anywhere\nin the world.", PEACH, WARM_BROWN),
    ]

    card_w = 1200
    card_h = 230
    gap_x = 100
    gap_y = 30
    start_x = (W - 2 * card_w - gap_x) // 2
    start_y = 310

    font_val_title = get_font(40, bold=True)
    font_val_body = get_font(30)

    for i, (title, body, accent, text_color) in enumerate(values):
        col = i % 2
        row = i // 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        # Card
        rounded_rect(draw, (x, y, x + card_w, y + card_h), 20, WHITE, outline=accent, width=3)
        # Accent left bar
        rounded_rect(draw, (x, y, x + 15, y + card_h), 8, accent)

        # Checkmark circle
        cx, cy = x + 55, y + card_h // 2
        draw.ellipse([(cx - 30, cy - 30), (cx + 30, cy + 30)], fill=accent)
        font_check = get_font(36, bold=True)
        draw.text((cx - 11, cy - 20), "✓", font=font_check, fill=text_color)

        # Title
        draw.text((x + 110, y + 20), title, font=font_val_title, fill=text_color)
        # Body
        lines = body.split("\n")
        for li, line in enumerate(lines):
            draw.text((x + 110, y + 75 + li * 42), line, font=font_val_body, fill=DARK_TEXT)

    # Bottom CTA section with gradient-style effect
    cta_y = start_y + 3 * (card_h + gap_y) + 30
    rounded_rect(draw, (0, cta_y, W, H), 0, DEEP_PURPLE)

    # Decorative eggs in CTA area
    for ex, ey, ec in [(200, cta_y + 50, SOFT_PINK), (400, cta_y + 80, LAVENDER),
                        (2300, cta_y + 50, MINT_GREEN), (2500, cta_y + 80, BUTTER_YELLOW)]:
        draw_egg(draw, ex, ey, 30, 38, ec)

    font_cta_title = get_font(64, bold=True)
    center_text(draw, "MAKE THIS EASTER UNFORGETTABLE", cta_y + 30, font_cta_title, WHITE)

    # CTA button
    btn_w, btn_h = 900, 100
    btn_x = (W - btn_w) // 2
    btn_y = cta_y + 130
    rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h), 50, GOLD_ACCENT)
    font_btn = get_font(48, bold=True)
    center_text(draw, "INSTANT DIGITAL DOWNLOAD", btn_y + 22, font_btn, CHARCOAL)

    # Final text
    font_final = get_font(32)
    center_text(draw, "25 Games  |  60+ Pages  |  All Ages  |  US Letter + A4  |  Print Unlimited Copies", btn_y + 130, font_final, SOFT_PINK)
    center_text(draw, "No physical item shipped  |  Download immediately after purchase  |  Personal use", btn_y + 180, font_final, LAVENDER)

    # Bottom accent
    rounded_rect(draw, (0, H - 20, W, H), 0, GOLD_ACCENT)

    img.save(os.path.join(OUT_DIR, "10_value_proposition.png"), quality=95)
    print("Created: 10_value_proposition.png")


# ═══════════════════════════════════════════════════
#  GENERATE ALL IMAGES
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating 10 Easter Party Games Bundle listing images...")
    print(f"Output directory: {OUT_DIR}")
    print(f"Image size: {W}x{H} (4:3 ratio)\n")

    create_image_01_hero()
    create_image_02_whats_included()
    create_image_03_word_games()
    create_image_04_party_games()
    create_image_05_kids_activities()
    create_image_06_activity_pages()
    create_image_07_how_it_works()
    create_image_08_size_format()
    create_image_09_perfect_for()
    create_image_10_value_prop()

    print(f"\nAll 10 listing images saved to: {OUT_DIR}")
    print("Ready for Etsy upload!")
