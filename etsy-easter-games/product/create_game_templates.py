"""
Create printable Easter Party Game templates as PDF-ready images.
Each game is a US Letter (8.5x11") page at 300 DPI = 2550x3300 pixels.
Generates preview pages for the key games in the bundle.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math
import random

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_pages")
os.makedirs(OUT_DIR, exist_ok=True)

# US Letter at 300 DPI
PW, PH = 2550, 3300
MARGIN = 150

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
PEACH = (255, 218, 185)
CORAL = (255, 160, 122)

WHITE = (255, 255, 255)
CREAM = (255, 253, 248)
LIGHT_GRAY = (240, 240, 240)
MED_GRAY = (200, 200, 200)
DARK_TEXT = (55, 55, 70)
CHARCOAL = (40, 40, 55)
DEEP_PURPLE = (102, 51, 153)
DEEP_PINK = (199, 21, 133)
FOREST_GREEN = (60, 130, 80)
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


def center_text(draw, text, y, font, color, canvas_width=PW):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]


def draw_egg(draw, cx, cy, w, h, fill_color, outline_color=None):
    draw.ellipse([(cx - w//2, cy - h//2), (cx + w//2, cy + h//2)],
                 fill=fill_color, outline=outline_color, width=2)


def draw_page_header(draw, title, subtitle=None, accent_color=LAVENDER, text_color=DEEP_PURPLE):
    """Draw a standard game page header with Easter decoration."""
    # Top accent bar
    rounded_rect(draw, (0, 0, PW, 30), 0, accent_color)

    # Header background
    rounded_rect(draw, (MARGIN, 60, PW - MARGIN, 280), 30, accent_color)

    # Decorative eggs in header
    for ex, ec in [(MARGIN + 80, SOFT_PINK), (MARGIN + 160, BUTTER_YELLOW),
                   (PW - MARGIN - 80, MINT_GREEN), (PW - MARGIN - 160, SKY_BLUE)]:
        draw_egg(draw, ex, 170, 40, 52, ec)

    # Title
    font_title = get_font(80, bold=True)
    center_text(draw, title, 90, font_title, text_color)

    if subtitle:
        font_sub = get_font(40)
        center_text(draw, subtitle, 200, font_sub, DARK_TEXT)

    # Bottom accent line
    draw.line([(MARGIN, 300), (PW - MARGIN, 300)], fill=accent_color, width=4)


def draw_page_footer(draw, accent_color=LAVENDER):
    """Draw standard page footer."""
    draw.line([(MARGIN, PH - 180), (PW - MARGIN, PH - 180)], fill=accent_color, width=3)
    font_footer = get_font(28)
    center_text(draw, "Easter Party Games Bundle | For Personal Use Only", PH - 150, font_footer, MED_GRAY)
    center_text(draw, "www.etsy.com/shop/ChelseasDesigns", PH - 110, font_footer, MED_GRAY)
    # Bottom accent bar
    rounded_rect(draw, (0, PH - 30, PW, PH), 0, accent_color)


# ═══════════════════════════════════════════════════
#  GAME 1: EASTER TRIVIA
# ═══════════════════════════════════════════════════
def create_easter_trivia():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER TRIVIA CHALLENGE", "Test your Easter knowledge!", LAVENDER, DEEP_PURPLE)

    questions = [
        ("1. What animal is most associated with Easter?",
         ["a) Lamb", "b) Bunny", "c) Chick", "d) Dove"]),
        ("2. How many jelly beans are consumed at Easter in the US?",
         ["a) 1 billion", "b) 8 billion", "c) 16 billion", "d) 24 billion"]),
        ("3. What flower is the traditional symbol of Easter?",
         ["a) Rose", "b) Tulip", "c) Lily", "d) Daisy"]),
        ("4. What is the day before Easter called?",
         ["a) Good Friday", "b) Palm Sunday", "c) Holy Saturday", "d) Ash Wednesday"]),
        ("5. In which country did the tradition of the Easter Bunny originate?",
         ["a) England", "b) France", "c) Germany", "d) Netherlands"]),
        ("6. What is the most popular Easter candy in America?",
         ["a) Chocolate eggs", "b) Peeps", "c) Jelly beans", "d) Cadbury Creme Eggs"]),
        ("7. What does the Easter egg symbolize?",
         ["a) Spring", "b) New life", "c) Fertility", "d) All of the above"]),
        ("8. What is an Easter bonnet?",
         ["a) A type of cake", "b) A decorated hat", "c) A basket", "d) A greeting card"]),
    ]

    font_q = get_font(38, bold=True)
    font_a = get_font(32)

    y = 360
    for q_text, answers in questions:
        # Question
        rounded_rect(draw, (MARGIN + 20, y - 10, PW - MARGIN - 20, y + 45), 10, LAVENDER)
        draw.text((MARGIN + 40, y - 5), q_text, font=font_q, fill=DEEP_PURPLE)
        y += 65

        # Answers in 2x2 grid
        col_w = (PW - 2 * MARGIN - 100) // 2
        for ai, ans in enumerate(answers):
            col = ai % 2
            row = ai // 2
            ax = MARGIN + 60 + col * col_w
            ay = y + row * 50
            draw.ellipse([(ax - 5, ay + 8), (ax + 22, ay + 35)], fill=BUTTER_YELLOW)
            draw.text((ax + 30, ay + 5), ans, font=font_a, fill=DARK_TEXT)
        y += 130

    draw_page_footer(draw, LAVENDER)
    img.save(os.path.join(OUT_DIR, "01_easter_trivia.png"), quality=95)
    print("Created: 01_easter_trivia.png")


# ═══════════════════════════════════════════════════
#  GAME 2: WORD SEARCH
# ═══════════════════════════════════════════════════
def create_word_search():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER WORD SEARCH", "Find all the hidden Easter words!", MINT_GREEN, FOREST_GREEN)

    # Word list
    words = ["BUNNY", "EGGS", "BASKET", "SPRING", "CHICK", "LAMB", "LILY",
             "BONNET", "PARADE", "CHOCOLATE", "CARROT", "HUNT", "FLOWERS", "SUNDAY"]

    # Create a simple grid with the words embedded
    random.seed(42)
    grid_size = 14
    grid = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Initialize grid with random letters
    for r in range(grid_size):
        row = []
        for c in range(grid_size):
            row.append(random.choice(letters))
        grid.append(row)

    # Place some words horizontally
    placements = [
        (0, 0, "BUNNY"), (1, 5, "EGGS"), (2, 0, "BASKET"),
        (3, 7, "SPRING"), (4, 1, "CHICK"), (5, 0, "LAMB"),
        (6, 8, "LILY"), (7, 2, "BONNET"), (8, 0, "PARADE"),
        (9, 1, "CHOCOLATE"), (10, 4, "CARROT"), (11, 0, "HUNT"),
        (12, 2, "FLOWERS"), (13, 6, "SUNDAY"),
    ]

    for row, col, word in placements:
        if row < grid_size:
            for i, ch in enumerate(word):
                if col + i < grid_size:
                    grid[row][col + i] = ch

    # Draw grid
    cell_size = 130
    grid_total = grid_size * cell_size
    grid_x = (PW - grid_total) // 2
    grid_y = 380

    font_cell = get_font(56, bold=True)
    font_cell_light = get_font(56)

    pastel_bg_colors = [SOFT_PINK, LAVENDER, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE, PEACH]

    for r in range(grid_size):
        for c in range(grid_size):
            x = grid_x + c * cell_size
            y = grid_y + r * cell_size
            # Alternating subtle background
            bg = WHITE if (r + c) % 2 == 0 else LIGHT_GRAY
            rounded_rect(draw, (x, y, x + cell_size, y + cell_size), 5, bg, outline=MED_GRAY, width=1)
            letter = grid[r][c]
            bbox = draw.textbbox((0, 0), letter, font=font_cell)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((x + (cell_size - tw) // 2, y + (cell_size - th) // 2 - 5),
                     letter, font=font_cell, fill=DARK_TEXT)

    # Word list at bottom
    word_y = grid_y + grid_total + 50
    rounded_rect(draw, (MARGIN + 20, word_y, PW - MARGIN - 20, word_y + 250), 20, MINT_GREEN)
    font_word_title = get_font(40, bold=True)
    center_text(draw, "WORDS TO FIND:", word_y + 20, font_word_title, FOREST_GREEN)

    font_word = get_font(32, bold=True)
    cols = 4
    col_w = (PW - 2 * MARGIN - 100) // cols
    for i, word in enumerate(words):
        col = i % cols
        row = i // cols
        wx = MARGIN + 80 + col * col_w
        wy = word_y + 80 + row * 50
        draw.text((wx, wy), word, font=font_word, fill=DEEP_PURPLE)

    draw_page_footer(draw, MINT_GREEN)
    img.save(os.path.join(OUT_DIR, "02_word_search.png"), quality=95)
    print("Created: 02_word_search.png")


# ═══════════════════════════════════════════════════
#  GAME 3: EASTER BINGO
# ═══════════════════════════════════════════════════
def create_bingo():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER BINGO", "Card 1 of 10", SOFT_PINK, DEEP_PINK)

    # Bingo grid 5x5
    cell_size = 380
    grid_total = 5 * cell_size
    grid_x = (PW - grid_total) // 2
    grid_y = 360

    # Headers
    headers = ["B", "I", "N", "G", "O"]
    header_colors = [LAVENDER, SOFT_PINK, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE]
    font_header = get_font(90, bold=True)
    font_cell = get_font(36, bold=True)
    font_cell_sm = get_font(30)

    for c, (letter, color) in enumerate(zip(headers, header_colors)):
        x = grid_x + c * cell_size
        rounded_rect(draw, (x, grid_y, x + cell_size, grid_y + 100), 0, color)
        bbox = draw.textbbox((0, 0), letter, font=font_header)
        tw = bbox[2] - bbox[0]
        draw.text((x + (cell_size - tw) // 2, grid_y + 2), letter, font=font_header, fill=CHARCOAL)

    # Bingo items
    bingo_grid = [
        ["Easter\nBunny", "Jelly\nBeans", "Easter\nBasket", "Spring\nFlowers", "Chocolate\nEgg"],
        ["Easter\nBonnet", "Baby\nChick", "Easter\nLily", "Colored\nEggs", "Hot Cross\nBuns"],
        ["Lamb", "Carrot\nCake", "FREE\nSPACE", "Easter\nParade", "Peeps"],
        ["Egg\nHunt", "Easter\nSunday", "Spring\nRain", "Tulips", "Bunny\nEars"],
        ["Daffodils", "Pastel\nColors", "Easter\nDinner", "Robin\nEggs", "New\nBonnet"],
    ]

    for r, row in enumerate(bingo_grid):
        for c, item in enumerate(row):
            x = grid_x + c * cell_size
            y = grid_y + 100 + r * (cell_size - 30)

            # Cell background
            if item == "FREE\nSPACE":
                bg = header_colors[c]
            else:
                bg = WHITE

            rounded_rect(draw, (x, y, x + cell_size, y + cell_size - 30),
                        0, bg, outline=MED_GRAY, width=2)

            # Draw small egg decoration for FREE SPACE
            if item == "FREE\nSPACE":
                draw_egg(draw, x + cell_size // 2, y + 60, 50, 65, WHITE)

            # Text
            lines = item.split("\n")
            total_h = len(lines) * 46
            start_ty = y + (cell_size - 30 - total_h) // 2
            for li, line in enumerate(lines):
                f = font_cell if item == "FREE\nSPACE" else font_cell_sm
                bbox = draw.textbbox((0, 0), line, font=f)
                tw = bbox[2] - bbox[0]
                color = DEEP_PINK if item == "FREE\nSPACE" else DARK_TEXT
                draw.text((x + (cell_size - tw) // 2, start_ty + li * 46), line, font=f, fill=color)

    draw_page_footer(draw, SOFT_PINK)
    img.save(os.path.join(OUT_DIR, "03_easter_bingo.png"), quality=95)
    print("Created: 03_easter_bingo.png")


# ═══════════════════════════════════════════════════
#  GAME 4: WOULD YOU RATHER
# ═══════════════════════════════════════════════════
def create_would_you_rather():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "WOULD YOU RATHER?", "Easter Edition - Circle your choice!", BUTTER_YELLOW, WARM_BROWN)

    questions = [
        ("Have unlimited chocolate eggs forever", "Find one golden egg worth $1,000"),
        ("Be the Easter Bunny for a day", "Be a baby chick for a day"),
        ("Only eat jelly beans for a week", "Only eat Peeps for a week"),
        ("Have a pet bunny", "Have a pet baby chick"),
        ("Do an indoor scavenger hunt", "Do an outdoor egg hunt"),
        ("Wear bunny ears everywhere for a month", "Wear a giant Easter bonnet everywhere for a month"),
        ("Make your own chocolate eggs", "Decorate real eggs"),
        ("Have Easter every month", "Have Christmas every month"),
        ("Live in a house shaped like an egg", "Drive a car shaped like a bunny"),
        ("Have it rain jelly beans", "Have it snow marshmallows"),
    ]

    font_q_num = get_font(36, bold=True)
    font_q = get_font(34, bold=True)
    font_or = get_font(40, bold=True)

    y = 360
    for i, (opt_a, opt_b) in enumerate(questions):
        # Question number
        num_x = MARGIN + 30
        draw.ellipse([(num_x, y + 5), (num_x + 50, y + 55)], fill=BUTTER_YELLOW)
        bbox = draw.textbbox((0, 0), str(i + 1), font=font_q_num)
        tw = bbox[2] - bbox[0]
        draw.text((num_x + (50 - tw) // 2, y + 8), str(i + 1), font=font_q_num, fill=WARM_BROWN)

        # Option A
        opt_a_x = MARGIN + 100
        rounded_rect(draw, (opt_a_x, y, opt_a_x + 900, y + 55), 10, SOFT_PINK)
        draw.text((opt_a_x + 15, y + 8), opt_a, font=font_q, fill=DEEP_PINK)

        # OR
        or_x = opt_a_x + 920
        draw.text((or_x, y + 5), "OR", font=font_or, fill=WARM_BROWN)

        # Option B
        opt_b_x = or_x + 80
        rounded_rect(draw, (opt_b_x, y, opt_b_x + 900, y + 55), 10, MINT_GREEN)
        draw.text((opt_b_x + 15, y + 8), opt_b, font=font_q, fill=FOREST_GREEN)

        y += 90

        # Decorative divider between questions
        if i < len(questions) - 1:
            mid_x = PW // 2
            draw_egg(draw, mid_x, y - 15, 15, 19, BUTTER_YELLOW)
            y += 20

    # Instructions at bottom
    inst_y = y + 40
    rounded_rect(draw, (MARGIN + 50, inst_y, PW - MARGIN - 50, inst_y + 100), 15, BUTTER_YELLOW)
    font_inst = get_font(32)
    center_text(draw, "Circle your answer, then compare with friends & family!", inst_y + 10, font_inst, WARM_BROWN)
    center_text(draw, "Bonus: Take turns explaining WHY you chose your answer!", inst_y + 55, font_inst, DARK_TEXT)

    draw_page_footer(draw, BUTTER_YELLOW)
    img.save(os.path.join(OUT_DIR, "04_would_you_rather.png"), quality=95)
    print("Created: 04_would_you_rather.png")


# ═══════════════════════════════════════════════════
#  GAME 5: SCAVENGER HUNT (Indoor)
# ═══════════════════════════════════════════════════
def create_scavenger_hunt():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER SCAVENGER HUNT", "Indoor Edition - Check off each item you find!", SKY_BLUE, CHARCOAL)

    items = [
        "Something shaped like an egg",
        "Something pink",
        "Something that hops",
        "Something that smells like spring",
        "A flower (real or fake)",
        "Something yellow",
        "Something soft like a bunny",
        "A basket or container",
        "Something with polka dots",
        "Something that makes you smile",
        "A picture of an animal",
        "Something green like grass",
        "A ribbon or bow",
        "Something sweet to eat",
        "Something purple or lavender",
        "A pair of something",
        "Something smaller than an egg",
        "Something you'd put in an Easter basket",
        "A book about spring or animals",
        "Something that sparkles or shines",
    ]

    font_item = get_font(36)
    font_item_bold = get_font(36, bold=True)

    y = 360
    pastel_colors = [SOFT_PINK, LAVENDER, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE, PEACH]

    for i, item in enumerate(items):
        # Checkbox
        box_x = MARGIN + 40
        box_y = y + 2
        color = pastel_colors[i % len(pastel_colors)]
        rounded_rect(draw, (box_x, box_y, box_x + 50, box_y + 50), 8, WHITE, outline=color, width=3)

        # Number
        num_x = box_x + 65
        draw.text((num_x, y + 5), f"{i + 1}.", font=font_item_bold, fill=CHARCOAL)

        # Item text
        text_x = num_x + 60
        draw.text((text_x, y + 5), item, font=font_item, fill=DARK_TEXT)

        y += 62

        # Subtle divider
        if i < len(items) - 1 and i % 5 == 4:
            draw.line([(MARGIN + 40, y + 5), (PW - MARGIN - 40, y + 5)], fill=color, width=2)
            y += 15

    # Scoring section
    score_y = y + 30
    rounded_rect(draw, (MARGIN + 50, score_y, PW - MARGIN - 50, score_y + 150), 20, SKY_BLUE)
    font_score_title = get_font(40, bold=True)
    font_score = get_font(32)
    center_text(draw, "HOW DID YOU DO?", score_y + 15, font_score_title, CHARCOAL)
    center_text(draw, "1-5 items: Good start!  |  6-10: Nice work!  |  11-15: Amazing!  |  16-20: Easter Champion!", score_y + 70, font_score, DARK_TEXT)
    center_text(draw, "My score: _____ / 20", score_y + 110, font_score, CHARCOAL)

    draw_page_footer(draw, SKY_BLUE)
    img.save(os.path.join(OUT_DIR, "05_scavenger_hunt.png"), quality=95)
    print("Created: 05_scavenger_hunt.png")


# ═══════════════════════════════════════════════════
#  GAME 6: EASTER EMOJI PICTIONARY
# ═══════════════════════════════════════════════════
def create_emoji_pictionary():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER EMOJI PICTIONARY", "Guess the Easter word from the emoji clues!", LAVENDER, DEEP_PURPLE)

    # Since we can't render actual emojis well in PIL, we'll use text descriptions
    clues = [
        ("1.", "Rabbit + Egg + Basket", "_______________"),
        ("2.", "Church + Sunrise + Cross", "_______________"),
        ("3.", "Flower + Rain + Sun", "_______________"),
        ("4.", "Candy + Bean + Rainbow", "_______________"),
        ("5.", "Chick + Egg + Crack", "_______________"),
        ("6.", "Bunny + Ears + Hat", "_______________"),
        ("7.", "Chocolate + Bunny + Wrapper", "_______________"),
        ("8.", "Egg + Paint + Brush", "_______________"),
        ("9.", "Basket + Grass + Candy", "_______________"),
        ("10.", "Parade + Bonnet + Flowers", "_______________"),
        ("11.", "Lamb + Baby + Spring", "_______________"),
        ("12.", "Treasure + Map + Hunt", "_______________"),
    ]

    font_num = get_font(40, bold=True)
    font_clue = get_font(38)
    font_answer = get_font(36)

    y = 360
    for i, (num, clue, answer_line) in enumerate(clues):
        color = [SOFT_PINK, LAVENDER, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE, PEACH][i % 6]

        # Row background
        rounded_rect(draw, (MARGIN + 20, y, PW - MARGIN - 20, y + 70), 12, color)

        # Number
        draw.text((MARGIN + 40, y + 12), num, font=font_num, fill=DEEP_PURPLE)

        # Emoji clue description
        draw.text((MARGIN + 120, y + 14), clue, font=font_clue, fill=CHARCOAL)

        # Answer line
        draw.text((PW - MARGIN - 500, y + 16), "Answer:", font=font_answer, fill=DARK_TEXT)
        draw.line([(PW - MARGIN - 370, y + 55), (PW - MARGIN - 40, y + 55)], fill=CHARCOAL, width=2)

        y += 95

    # Instructions
    inst_y = y + 40
    rounded_rect(draw, (MARGIN + 50, inst_y, PW - MARGIN - 50, inst_y + 130), 15, LAVENDER)
    font_inst = get_font(32, bold=True)
    center_text(draw, "HOW TO PLAY: Read the emoji clue out loud.", inst_y + 15, font_inst, DEEP_PURPLE)
    font_inst2 = get_font(30)
    center_text(draw, "Each set of emojis represents an Easter-related word or phrase.", inst_y + 55, font_inst2, DARK_TEXT)
    center_text(draw, "Write your answer on the line. Check the answer key when done!", inst_y + 90, font_inst2, DARK_TEXT)

    draw_page_footer(draw, LAVENDER)
    img.save(os.path.join(OUT_DIR, "06_emoji_pictionary.png"), quality=95)
    print("Created: 06_emoji_pictionary.png")


# ═══════════════════════════════════════════════════
#  GAME 7: EASTER I SPY
# ═══════════════════════════════════════════════════
def create_i_spy():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER I SPY", "Count each Easter item you can find!", PEACH, WARM_BROWN)

    # Create a field of scattered Easter items (represented as colored shapes)
    random.seed(99)
    item_area_y = 350
    item_area_h = 1800
    item_area = (MARGIN + 50, item_area_y, PW - MARGIN - 50, item_area_y + item_area_h)

    # Background for the I Spy area
    rounded_rect(draw, item_area, 20, WHITE, outline=PEACH, width=3)

    # Scatter colored eggs, circles (representing different items)
    egg_colors = {
        "Pink Eggs": (SOFT_PINK, 0),
        "Purple Eggs": (LAVENDER, 0),
        "Green Eggs": (MINT_GREEN, 0),
        "Yellow Eggs": (BUTTER_YELLOW, 0),
        "Blue Eggs": (SKY_BLUE, 0),
    }

    all_items = []
    for color_name, (color, _) in egg_colors.items():
        count = random.randint(4, 8)
        egg_colors[color_name] = (color, count)
        for _ in range(count):
            ex = random.randint(item_area[0] + 60, item_area[2] - 60)
            ey = random.randint(item_area[1] + 60, item_area[3] - 60)
            size = random.randint(30, 55)
            all_items.append((ex, ey, size, color, "egg"))

    # Also add some flowers and stars
    flower_count = random.randint(5, 9)
    star_count = random.randint(4, 7)

    for _ in range(flower_count):
        fx = random.randint(item_area[0] + 60, item_area[2] - 60)
        fy = random.randint(item_area[1] + 60, item_area[3] - 60)
        all_items.append((fx, fy, 35, CORAL, "flower"))

    for _ in range(star_count):
        sx = random.randint(item_area[0] + 60, item_area[2] - 60)
        sy = random.randint(item_area[1] + 60, item_area[3] - 60)
        all_items.append((sx, sy, 25, SOFT_YELLOW, "star"))

    # Draw all items
    random.shuffle(all_items)
    for x, y, size, color, shape in all_items:
        if shape == "egg":
            draw_egg(draw, x, y, size, int(size * 1.3), color, outline_color=CHARCOAL)
            # Stripe decoration on egg
            draw.line([(x - size//3, y), (x + size//3, y)], fill=WHITE, width=2)
        elif shape == "flower":
            # Simple flower
            for angle in range(0, 360, 72):
                rad = math.radians(angle)
                px = x + int(math.cos(rad) * size // 2)
                py = y + int(math.sin(rad) * size // 2)
                draw.ellipse([(px - 8, py - 8), (px + 8, py + 8)], fill=color)
            draw.ellipse([(x - 6, y - 6), (x + 6, y + 6)], fill=BUTTER_YELLOW)
        elif shape == "star":
            # Simple diamond/star shape
            draw.polygon([(x, y - size), (x + size//2, y), (x, y + size), (x - size//2, y)], fill=color, outline=CHARCOAL)

    # Counting section at bottom
    count_y = item_area[3] + 50
    rounded_rect(draw, (MARGIN + 30, count_y, PW - MARGIN - 30, count_y + 450), 20, PEACH)

    font_count_title = get_font(44, bold=True)
    center_text(draw, "I SPY... How many can you count?", count_y + 20, font_count_title, WARM_BROWN)

    font_count = get_font(36)
    count_items = [
        ("Pink Eggs:", f"{egg_colors['Pink Eggs'][1]}"),
        ("Purple Eggs:", f"{egg_colors['Purple Eggs'][1]}"),
        ("Green Eggs:", f"{egg_colors['Green Eggs'][1]}"),
        ("Yellow Eggs:", f"{egg_colors['Yellow Eggs'][1]}"),
        ("Blue Eggs:", f"{egg_colors['Blue Eggs'][1]}"),
        ("Flowers:", f"{flower_count}"),
        ("Stars:", f"{star_count}"),
    ]

    for i, (label, correct) in enumerate(count_items):
        col = i % 3
        row = i // 3
        cx = MARGIN + 100 + col * 700
        cy = count_y + 90 + row * 80

        # Color swatch
        if "Pink" in label: swatch = SOFT_PINK
        elif "Purple" in label: swatch = LAVENDER
        elif "Green" in label: swatch = MINT_GREEN
        elif "Yellow" in label: swatch = BUTTER_YELLOW
        elif "Blue" in label: swatch = SKY_BLUE
        elif "Flower" in label: swatch = CORAL
        else: swatch = SOFT_YELLOW

        draw.ellipse([(cx, cy + 5), (cx + 35, cy + 40)], fill=swatch, outline=CHARCOAL)
        draw.text((cx + 50, cy + 3), label, font=font_count, fill=DARK_TEXT)
        draw.line([(cx + 350, cy + 38), (cx + 480, cy + 38)], fill=CHARCOAL, width=2)

    draw_page_footer(draw, PEACH)
    img.save(os.path.join(OUT_DIR, "07_i_spy.png"), quality=95)
    print("Created: 07_i_spy.png")


# ═══════════════════════════════════════════════════
#  GAME 8: EASTER MAZE
# ═══════════════════════════════════════════════════
def create_maze():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER MAZE", "Help the bunny find the Easter basket!", SOFT_PINK, DEEP_PINK)

    # Create a simple maze using rectangles as walls
    maze_x = MARGIN + 100
    maze_y = 380
    maze_w = PW - 2 * MARGIN - 200
    maze_h = 2200

    # Maze border
    rounded_rect(draw, (maze_x, maze_y, maze_x + maze_w, maze_y + maze_h), 10, WHITE, outline=DEEP_PINK, width=5)

    # Start label
    font_label = get_font(40, bold=True)
    draw.text((maze_x + 20, maze_y - 60), "START", font=font_label, fill=DEEP_PINK)
    draw_egg(draw, maze_x + 180, maze_y - 40, 35, 45, SOFT_PINK)

    # End label
    draw.text((maze_x + maze_w - 200, maze_y + maze_h + 20), "FINISH!", font=font_label, fill=FOREST_GREEN)
    draw_egg(draw, maze_x + maze_w - 50, maze_y + maze_h + 45, 35, 45, MINT_GREEN)

    # Draw maze walls (simplified grid-based maze)
    wall_color = DEEP_PINK
    wall_width = 6
    cell = maze_w // 8  # 8 columns

    # Horizontal walls
    h_walls = [
        (1, 0, 3), (1, 5, 7),
        (2, 1, 4), (2, 6, 8),
        (3, 0, 2), (3, 3, 5), (3, 7, 8),
        (4, 1, 3), (4, 4, 6),
        (5, 0, 2), (5, 3, 5), (5, 6, 8),
        (6, 1, 4), (6, 5, 7),
        (7, 0, 3), (7, 4, 6),
        (8, 2, 5), (8, 6, 8),
        (9, 0, 2), (9, 3, 6),
    ]

    rows_in_maze = 10
    row_height = maze_h // rows_in_maze

    for row, col_start, col_end in h_walls:
        y = maze_y + row * row_height
        x1 = maze_x + col_start * cell
        x2 = maze_x + col_end * cell
        draw.line([(x1, y), (x2, y)], fill=wall_color, width=wall_width)

    # Vertical walls
    v_walls = [
        (0, 1, 3), (0, 2, 5), (0, 4, 7),
        (1, 3, 5), (1, 6, 8),
        (2, 1, 3), (2, 5, 7),
        (3, 2, 4), (3, 4, 6), (3, 7, 9),
        (4, 3, 5), (4, 6, 8),
        (5, 1, 3), (5, 5, 7),
        (6, 2, 4), (6, 7, 9),
        (7, 3, 5), (7, 5, 8),
    ]

    for col, row_start, row_end in v_walls:
        x = maze_x + col * cell
        y1 = maze_y + row_start * row_height
        y2 = maze_y + row_end * row_height
        draw.line([(x, y1), (x, y2)], fill=wall_color, width=wall_width)

    # Decorative eggs inside some maze cells
    deco_positions = [(2, 2), (5, 4), (1, 6), (7, 3), (4, 7), (8, 1)]
    pastel = [SOFT_PINK, LAVENDER, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE, PEACH]
    for i, (r, c) in enumerate(deco_positions):
        ex = maze_x + c * cell + cell // 2
        ey = maze_y + r * row_height + row_height // 2
        draw_egg(draw, ex, ey, 30, 38, pastel[i % len(pastel)])

    draw_page_footer(draw, SOFT_PINK)
    img.save(os.path.join(OUT_DIR, "08_easter_maze.png"), quality=95)
    print("Created: 08_easter_maze.png")


# ═══════════════════════════════════════════════════
#  GAME 9: COLORING PAGE
# ═══════════════════════════════════════════════════
def create_coloring_page():
    img = Image.new("RGB", (PW, PH), WHITE)
    draw = ImageDraw.Draw(img)

    # Simple header (coloring pages have minimal chrome)
    font_title = get_font(60, bold=True)
    center_text(draw, "Happy Easter!", 80, font_title, MED_GRAY)

    font_sub = get_font(36)
    center_text(draw, "Color this Easter scene!", 160, font_sub, MED_GRAY)

    # Draw a large Easter egg in the center with patterns to color
    cx, cy = PW // 2, PH // 2
    egg_w, egg_h = 700, 950
    outline_color = CHARCOAL
    lw = 4

    # Main egg outline
    draw.ellipse([(cx - egg_w, cy - egg_h), (cx + egg_w, cy + egg_h)],
                 fill=WHITE, outline=outline_color, width=lw)

    # Horizontal pattern bands on egg
    bands = [-600, -350, -100, 150, 400, 650]
    for band_y in bands:
        # Wavy line across egg
        y_pos = cy + band_y
        # Calculate egg width at this y position
        # Ellipse equation: (x/a)^2 + (y/b)^2 = 1 -> x = a * sqrt(1 - (y/b)^2)
        rel_y = band_y / egg_h
        if abs(rel_y) < 1:
            half_w = int(egg_w * math.sqrt(1 - rel_y * rel_y))
            draw.line([(cx - half_w, y_pos), (cx + half_w, y_pos)], fill=outline_color, width=lw)

    # Zigzag pattern in one band
    zig_y = cy - 225
    rel_y_zig = -225 / egg_h
    if abs(rel_y_zig) < 1:
        half_w_zig = int(egg_w * math.sqrt(1 - rel_y_zig * rel_y_zig))
        points = []
        for x in range(cx - half_w_zig + 30, cx + half_w_zig - 30, 60):
            points.append((x, zig_y + (30 if len(points) % 2 == 0 else -30)))
        if len(points) > 1:
            draw.line(points, fill=outline_color, width=3)

    # Circles pattern in another band
    circle_y = cy + 275
    rel_y_c = 275 / egg_h
    if abs(rel_y_c) < 1:
        half_w_c = int(egg_w * math.sqrt(1 - rel_y_c * rel_y_c))
        for cx_offset in range(-half_w_c + 80, half_w_c - 80, 120):
            draw.ellipse([(cx + cx_offset - 30, circle_y - 30),
                         (cx + cx_offset + 30, circle_y + 30)],
                        fill=WHITE, outline=outline_color, width=3)

    # Stars pattern
    star_y = cy - 475
    rel_y_s = -475 / egg_h
    if abs(rel_y_s) < 1:
        half_w_s = int(egg_w * math.sqrt(1 - rel_y_s * rel_y_s))
        for sx_offset in range(-half_w_s + 100, half_w_s - 100, 150):
            # Simple diamond star
            sx = cx + sx_offset
            s = 20
            draw.polygon([(sx, star_y - s), (sx + s//2, star_y),
                         (sx, star_y + s), (sx - s//2, star_y)],
                        fill=WHITE, outline=outline_color, width=2)

    # Small bunny and flowers at the bottom
    # Simple flower outlines at bottom of page
    for fx_offset in [-500, -250, 0, 250, 500]:
        fx = cx + fx_offset
        fy = PH - 350
        # Flower petals
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            px = fx + int(math.cos(rad) * 40)
            py = fy + int(math.sin(rad) * 40)
            draw.ellipse([(px - 20, py - 20), (px + 20, py + 20)],
                        fill=WHITE, outline=outline_color, width=2)
        draw.ellipse([(fx - 12, fy - 12), (fx + 12, fy + 12)],
                    fill=WHITE, outline=outline_color, width=2)
        # Stem
        draw.line([(fx, fy + 40), (fx, fy + 100)], fill=outline_color, width=2)
        # Leaf
        draw.ellipse([(fx + 5, fy + 55), (fx + 35, fy + 75)],
                    fill=WHITE, outline=outline_color, width=2)

    # Footer
    font_footer = get_font(28)
    center_text(draw, "Easter Party Games Bundle | For Personal Use Only", PH - 100, font_footer, MED_GRAY)

    img.save(os.path.join(OUT_DIR, "09_coloring_page.png"), quality=95)
    print("Created: 09_coloring_page.png")


# ═══════════════════════════════════════════════════
#  GAME 10: CHARADES CARDS
# ═══════════════════════════════════════════════════
def create_charades():
    img = Image.new("RGB", (PW, PH), CREAM)
    draw = ImageDraw.Draw(img)

    draw_page_header(draw, "EASTER CHARADES", "Cut out the cards. Draw one and act it out!", SOFT_GREEN, FOREST_GREEN)

    prompts = [
        "Decorating\nEaster Eggs", "The Easter\nBunny Hopping", "Finding a\nHidden Egg",
        "Eating\nChocolate", "Wearing a\nBonnet", "Hunting for\nEaster Eggs",
        "Petting a\nBaby Chick", "Making an\nEaster Basket", "Rolling an\nEgg Down a Hill",
        "Putting on\nBunny Ears", "Biting the Ears\nOff a Chocolate\nBunny", "Having an\nEgg & Spoon\nRace",
        "Planting\nSpring Flowers", "Opening an\nEaster Card", "Doing the\nBunny Hop\nDance",
        "Dyeing\nEaster Eggs", "Cracking Open\na Plastic Egg", "Marching in\nan Easter\nParade",
        "Feeding\na Lamb", "Taking a Photo\nwith the\nEaster Bunny",
    ]

    # Card grid: 4 columns x 5 rows
    cols, rows = 4, 5
    card_w = (PW - 2 * MARGIN - (cols - 1) * 20) // cols
    card_h = (PH - 500 - (rows - 1) * 20) // rows
    gap = 20

    font_prompt = get_font(30, bold=True)
    pastel_colors = [SOFT_PINK, LAVENDER, MINT_GREEN, BUTTER_YELLOW, SKY_BLUE, PEACH]

    for i, prompt in enumerate(prompts):
        col = i % cols
        row = i // cols
        x = MARGIN + col * (card_w + gap)
        y = 360 + row * (card_h + gap)

        color = pastel_colors[i % len(pastel_colors)]

        # Card with dashed border effect
        rounded_rect(draw, (x, y, x + card_w, y + card_h), 15, color, outline=CHARCOAL, width=2)

        # Inner white area
        inner_margin = 8
        rounded_rect(draw, (x + inner_margin, y + inner_margin,
                           x + card_w - inner_margin, y + card_h - inner_margin),
                    12, WHITE, outline=color, width=2)

        # Prompt text
        lines = prompt.split("\n")
        total_h = len(lines) * 42
        start_ty = y + (card_h - total_h) // 2
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_prompt)
            tw = bbox[2] - bbox[0]
            draw.text((x + (card_w - tw) // 2, start_ty + li * 42), line, font=font_prompt, fill=CHARCOAL)

    # Cut line instruction
    font_cut = get_font(28)
    center_text(draw, "- - - - - - - Cut along the card edges - - - - - - -", PH - 200, font_cut, MED_GRAY)

    draw_page_footer(draw, SOFT_GREEN)
    img.save(os.path.join(OUT_DIR, "10_charades_cards.png"), quality=95)
    print("Created: 10_charades_cards.png")


# ═══════════════════════════════════════════════════
#  GENERATE ALL GAME PAGES
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Easter Party Game template pages...")
    print(f"Output directory: {OUT_DIR}")
    print(f"Page size: {PW}x{PH} (US Letter at 300 DPI)\n")

    create_easter_trivia()
    create_word_search()
    create_bingo()
    create_would_you_rather()
    create_scavenger_hunt()
    create_emoji_pictionary()
    create_i_spy()
    create_maze()
    create_coloring_page()
    create_charades()

    print(f"\nAll 10 game template pages saved to: {OUT_DIR}")
    print("These represent sample pages from the 25-game bundle.")
