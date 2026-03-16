#!/usr/bin/env python3
"""
Graduation Memory Book — PDF Printable Generator (ReportLab)
Creates a beautifully formatted 7-page printable memory book:
  1. Cover Page
  2. About the Graduate
  3. School Memories
  4. Favorite Teachers
  5. Achievements
  6. Future Plans
  7. Messages from Family
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

PAGE_W, PAGE_H = A4  # 595.27 x 841.89 points
MARGIN = 18 * mm
CONTENT_W = PAGE_W - MARGIN * 2

# ── COLORS ────────────────────────────────────────────────────────────────────
GOLD    = HexColor("#D4AF37")
PINK    = HexColor("#fb5887")
DARK    = HexColor("#1e1e1e")
GRAY    = HexColor("#646464")
LIGHT   = HexColor("#f5f5f5")
WHITE   = colors.white
CREAM   = HexColor("#FFFDF5")
NAVY    = HexColor("#1a2744")
GOLD_LIGHT = HexColor("#FFF8DC")


class MemoryBook:
    def __init__(self, filename):
        self.c = rl_canvas.Canvas(filename, pagesize=A4)
        self.filename = filename

    def save(self):
        self.c.save()
        print(f"✓ Saved: {self.filename}")

    # ── DRAWING HELPERS ───────────────────────────────────────────────────────
    def filled_rect(self, x, y, w, h, fill, stroke=None, stroke_width=0.5):
        c = self.c
        c.saveState()
        if stroke:
            c.setStrokeColor(stroke)
            c.setLineWidth(stroke_width)
        else:
            c.setLineWidth(0)
        c.setFillColor(fill)
        if stroke:
            c.rect(x, y, w, h, fill=1, stroke=1)
        else:
            c.rect(x, y, w, h, fill=1, stroke=0)
        c.restoreState()

    def text_centered(self, text, y, size, color, bold=False):
        c = self.c
        c.saveState()
        c.setFillColor(color)
        if bold:
            c.setFont("Helvetica-Bold", size)
        else:
            c.setFont("Helvetica", size)
        c.drawCentredString(PAGE_W / 2, y, text)
        c.restoreState()

    def text_at(self, text, x, y, size, color, bold=False):
        c = self.c
        c.saveState()
        c.setFillColor(color)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, text)
        c.restoreState()

    def gold_line(self, y, x1=None, x2=None, width=1):
        x1 = x1 or MARGIN
        x2 = x2 or PAGE_W - MARGIN
        c = self.c
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(width)
        c.line(x1, y, x2, y)
        c.restoreState()

    def label_box(self, label, x, y, w, h, fill=None, font_size=8):
        """Draw a labeled input box."""
        fill = fill or CREAM
        self.text_at(label.upper(), x, y + h + 2, font_size, GRAY, bold=True)
        self.filled_rect(x, y, w, h, fill=fill, stroke=GOLD, stroke_width=0.4)

    def ruled_box(self, x, y, w, h, label=None, fill=None, line_color=None, num_lines=None):
        """Draw a box with horizontal writing lines."""
        fill = fill or CREAM
        line_color_rgb = line_color or HexColor("#D0D0D0")
        self.filled_rect(x, y, w, h, fill=fill, stroke=GOLD, stroke_width=0.4)
        if label:
            self.text_at(label, x + 3, y + h - 12, 7, GRAY, bold=True)
        if num_lines is None:
            num_lines = max(1, int((h - 14) / 8))
        for i in range(num_lines):
            ly = y + h - 14 - i * 8
            if ly > y + 2:
                self.c.saveState()
                self.c.setStrokeColor(line_color_rgb)
                self.c.setLineWidth(0.3)
                self.c.line(x + 3, ly, x + w - 3, ly)
                self.c.restoreState()

    def section_header(self, title, y, color=None, font_size=16):
        color = color or PINK
        self.c.saveState()
        self.c.setFillColor(color)
        self.c.setFont("Helvetica-Bold", font_size)
        self.c.drawString(MARGIN, y, title)
        self.c.restoreState()
        self.gold_line(y - 4, width=0.8)

    def photo_box(self, x, y, w, h, label="Photo"):
        self.filled_rect(x, y, w, h, fill=LIGHT, stroke=GOLD, stroke_width=0.6)
        self.c.saveState()
        self.c.setFont("Helvetica-Oblique", 10)
        self.c.setFillColor(GRAY)
        self.c.drawCentredString(x + w / 2, y + h / 2 - 4, label)
        self.c.restoreState()

    def page_top_strip(self, color=None):
        color = color or PINK
        self.filled_rect(0, PAGE_H - 14 * mm, PAGE_W, 14 * mm, fill=color)

    def page_bottom_strip(self, color=None, page_num=None):
        color = color or GOLD
        self.filled_rect(0, 0, PAGE_W, 10 * mm, fill=color)
        if page_num:
            self.c.saveState()
            self.c.setFont("Helvetica", 8)
            self.c.setFillColor(WHITE)
            self.c.drawCentredString(PAGE_W / 2, 3 * mm, f"Page {page_num}")
            self.c.restoreState()

    def corner_marks(self):
        s = 12 * mm
        cx = self.c
        cx.saveState()
        cx.setStrokeColor(GOLD)
        cx.setLineWidth(1.2)
        m = MARGIN
        t = PAGE_H - MARGIN - 10 * mm
        # Top-left
        cx.line(m, t, m + s, t)
        cx.line(m, t, m, t - s)
        # Top-right
        r = PAGE_W - m
        cx.line(r, t, r - s, t)
        cx.line(r, t, r, t - s)
        cx.restoreState()

    def new_page(self):
        self.c.showPage()

    # ── PAGE 1: COVER ─────────────────────────────────────────────────────────
    def page_cover(self):
        c = self.c

        # Background
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=CREAM)

        # Top and bottom dark bars
        self.filled_rect(0, PAGE_H - 20 * mm, PAGE_W, 20 * mm, fill=DARK)
        self.filled_rect(0, 0, PAGE_W, 20 * mm, fill=DARK)

        # Double border frame
        pad = 8 * mm
        c.saveState()
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.5)
        c.rect(pad, pad + 20 * mm, PAGE_W - pad * 2, PAGE_H - (pad + 20 * mm) * 2, fill=0, stroke=1)
        c.setLineWidth(0.4)
        inner = 12 * mm
        c.rect(inner, inner + 20 * mm, PAGE_W - inner * 2, PAGE_H - (inner + 20 * mm) * 2, fill=0, stroke=1)
        c.restoreState()

        # Graduation cap
        self.text_centered("🎓", PAGE_H - 40 * mm, 30, GOLD)

        # Title
        self.text_centered("GRADUATION", PAGE_H - 55 * mm, 28, DARK, bold=True)
        self.text_centered("MEMORY BOOK", PAGE_H - 65 * mm, 22, PINK, bold=True)

        # Gold divider
        self.gold_line(PAGE_H - 74 * mm, x1=MARGIN + 20 * mm, x2=PAGE_W - MARGIN - 20 * mm, width=1.5)

        # Subtitle
        c.saveState()
        c.setFont("Helvetica-Oblique", 12)
        c.setFillColor(GRAY)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 82 * mm, "A keepsake to celebrate your journey")
        c.restoreState()

        # Input fields
        field_y = PAGE_H - 105 * mm
        field_h = 10 * mm
        field_w = CONTENT_W * 0.65
        field_x = MARGIN + CONTENT_W * 0.175

        fields = ["Graduate's Name", "School / University", "Graduation Year", "Degree / Program"]
        for i, label in enumerate(fields):
            fy = field_y - i * (field_h + 6 * mm)
            c.saveState()
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(GRAY)
            c.drawCentredString(PAGE_W / 2, fy + field_h + 1 * mm, label.upper())
            c.restoreState()
            self.filled_rect(field_x, fy, field_w, field_h, fill=WHITE, stroke=GOLD, stroke_width=0.5)

        # Gold divider 2
        self.gold_line(field_y - 4 * (field_h + 6 * mm) - 5 * mm,
                       x1=MARGIN + 20 * mm, x2=PAGE_W - MARGIN - 20 * mm)

        # Photo box
        ph_y = 35 * mm
        ph_h = 55 * mm
        ph_w = 55 * mm
        self.photo_box((PAGE_W - ph_w) / 2, ph_y, ph_w, ph_h, "Your Photo Here")

        # Quote
        c.saveState()
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(GOLD)
        c.drawCentredString(PAGE_W / 2, 25 * mm, '"The future belongs to those who believe in the beauty of their dreams."')
        c.setFont("Helvetica", 8)
        c.setFillColor(GRAY)
        c.drawCentredString(PAGE_W / 2, 21 * mm, "— Eleanor Roosevelt")
        c.restoreState()

        self.new_page()

    # ── PAGE 2: ABOUT THE GRADUATE ────────────────────────────────────────────
    def page_about(self):
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=WHITE)
        self.page_top_strip(PINK)
        self.page_bottom_strip(GOLD, page_num=2)
        self.corner_marks()

        self.section_header("About the Graduate", PAGE_H - 22 * mm, color=PINK, font_size=18)

        half_w = (CONTENT_W - 5 * mm) / 2
        fields_left = ["Full Name", "Date of Birth", "Hometown", "School / University"]
        fields_right = ["Graduation Date", "Degree / Diploma", "GPA / Honors", "Extracurriculars"]
        y = PAGE_H - 38 * mm
        fh = 9 * mm

        for ll, rl in zip(fields_left, fields_right):
            self.label_box(ll, MARGIN, y - fh, half_w, fh, fill=CREAM)
            self.label_box(rl, MARGIN + half_w + 5 * mm, y - fh, half_w, fh, fill=CREAM)
            y -= fh + 7 * mm

        # Favorites section
        self.gold_line(y + 2 * mm)
        self.section_header("Favorites", y - 4 * mm, color=GOLD, font_size=13)
        y -= 14 * mm

        fav_items = [
            ("Favorite Subject", 9 * mm),
            ("Favorite Teacher", 9 * mm),
            ("Favorite Memory", 14 * mm),
            ("Favorite Quote", 12 * mm),
            ("Best Friend(s)", 9 * mm),
        ]
        for label, fh in fav_items:
            if y - fh < 15 * mm:
                break
            self.label_box(label, MARGIN, y - fh, CONTENT_W, fh, fill=CREAM)
            y -= fh + 5 * mm

        # Photo
        if y - 40 * mm > 12 * mm:
            self.photo_box(MARGIN, y - 40 * mm, CONTENT_W, 36 * mm, "Favorite Photo")

        self.new_page()

    # ── PAGE 3: SCHOOL MEMORIES ───────────────────────────────────────────────
    def page_memories(self):
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=WHITE)
        self.page_top_strip(GOLD)
        self.page_bottom_strip(PINK, page_num=3)
        self.corner_marks()

        self.section_header("School Memories", PAGE_H - 22 * mm, color=GOLD, font_size=18)

        prompts = [
            ("My first day of school, I remember...", 20 * mm),
            ("The funniest moment I'll never forget...", 20 * mm),
            ("My most proud school moment...", 20 * mm),
            ("The biggest challenge I overcame...", 20 * mm),
            ("My favorite tradition or school event...", 18 * mm),
        ]
        y = PAGE_H - 36 * mm
        for prompt, h in prompts:
            if y - h < 60 * mm:
                break
            self.ruled_box(MARGIN, y - h, CONTENT_W, h, label=prompt, fill=CREAM)
            y -= h + 4 * mm

        # Photo grid
        if y - 52 * mm > 12 * mm:
            ph_w = (CONTENT_W - 4 * mm) / 2
            self.photo_box(MARGIN, y - 52 * mm, ph_w, 48 * mm, "Memory Photo 1")
            self.photo_box(MARGIN + ph_w + 4 * mm, y - 52 * mm, ph_w, 48 * mm, "Memory Photo 2")

        self.new_page()

    # ── PAGE 4: FAVORITE TEACHERS ─────────────────────────────────────────────
    def page_teachers(self):
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=WHITE)
        self.page_top_strip(PINK)
        self.page_bottom_strip(GOLD, page_num=4)
        self.corner_marks()

        self.section_header("Favorite Teachers", PAGE_H - 22 * mm, color=PINK, font_size=18)

        # Intro
        self.c.saveState()
        self.c.setFont("Helvetica-Oblique", 10)
        self.c.setFillColor(GRAY)
        self.c.drawString(MARGIN, PAGE_H - 32 * mm,
                          "The teachers who shaped you, inspired you, and believed in you — remember them here.")
        self.c.restoreState()

        # Table
        col_w = [45 * mm, 35 * mm, CONTENT_W - 80 * mm]
        headers = ["Teacher Name", "Subject", "Why They Made a Difference"]
        header_y = PAGE_H - 42 * mm
        header_h = 7 * mm

        # Header row
        self.filled_rect(MARGIN, header_y - header_h, CONTENT_W, header_h, fill=DARK)
        x = MARGIN
        self.c.saveState()
        self.c.setFont("Helvetica-Bold", 8)
        self.c.setFillColor(WHITE)
        for cw, hdr in zip(col_w, headers):
            self.c.drawString(x + 2, header_y - header_h + 2, hdr)
            x += cw
        self.c.restoreState()

        row_h = 12 * mm
        row_colors_list = [CREAM, WHITE]
        y = header_y - header_h - row_h
        for i in range(8):
            if y < 55 * mm:
                break
            bg = row_colors_list[i % 2]
            self.filled_rect(MARGIN, y, CONTENT_W, row_h, fill=bg, stroke=GOLD, stroke_width=0.3)
            # Column dividers
            x = MARGIN
            for cw in col_w[:-1]:
                x += cw
                self.c.saveState()
                self.c.setStrokeColor(HexColor("#D0D0D0"))
                self.c.setLineWidth(0.2)
                self.c.line(x, y, x, y + row_h)
                self.c.restoreState()
            # Writing line
            self.c.saveState()
            self.c.setStrokeColor(HexColor("#CCCCCC"))
            self.c.setLineWidth(0.2)
            self.c.line(MARGIN + 3, y + 4, MARGIN + CONTENT_W - 3, y + 4)
            self.c.restoreState()
            y -= row_h

        # Message box
        if y - 35 * mm > 12 * mm:
            self.ruled_box(MARGIN, y - 35 * mm, CONTENT_W, 35 * mm,
                           label="A message I wish I could send to my favorite teacher...", fill=CREAM)
            y -= 39 * mm

        # Photo
        if y - 40 * mm > 12 * mm:
            self.photo_box(MARGIN, y - 40 * mm, CONTENT_W, min(36 * mm, y - 14 * mm),
                           "Photo with Favorite Teacher")

        self.new_page()

    # ── PAGE 5: ACHIEVEMENTS ──────────────────────────────────────────────────
    def page_achievements(self):
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=WHITE)
        self.page_top_strip(GOLD)
        self.page_bottom_strip(PINK, page_num=5)
        self.corner_marks()

        self.section_header("Achievements & Highlights", PAGE_H - 22 * mm, color=GOLD, font_size=18)

        # Awards
        self.text_at("Awards & Honors", MARGIN, PAGE_H - 33 * mm, 11, DARK, bold=True)
        y = PAGE_H - 43 * mm
        for i in range(5):
            if y < 55 * mm:
                break
            # Gold bullet
            self.filled_rect(MARGIN, y + 1, 4, 4, fill=GOLD)
            self.filled_rect(MARGIN + 6, y - 1, CONTENT_W - 6, 7, fill=CREAM, stroke=GOLD, stroke_width=0.3)
            y -= 10 * mm

        # Clubs
        self.gold_line(y + 4 * mm)
        self.text_at("Clubs, Sports & Activities", MARGIN, y - 1 * mm, 11, DARK, bold=True)
        y -= 9 * mm

        half_w = (CONTENT_W - 4 * mm) / 2
        for i in range(6):
            row = i // 2
            col = i % 2
            cx = MARGIN + col * (half_w + 4 * mm)
            cy = y - row * 10 * mm - 8 * mm
            if cy < 55 * mm:
                break
            self.filled_rect(cx, cy, half_w, 7 * mm, fill=CREAM, stroke=GOLD, stroke_width=0.3)
        y -= 3 * 10 * mm + 4 * mm

        # Proudest moment
        if y - 28 * mm > 55 * mm:
            self.gold_line(y + 2 * mm)
            self.ruled_box(MARGIN, y - 28 * mm, CONTENT_W, 24 * mm,
                           label="My proudest achievement during my school years...", fill=CREAM)
            y -= 32 * mm

        # Stats
        if y - 30 * mm > 12 * mm:
            self.gold_line(y + 2 * mm)
            self.text_at("By the Numbers", MARGIN, y - 3 * mm, 11, DARK, bold=True)
            stats = ["Years in school:", "Classes taken:", "Friends made:", "Events attended:"]
            sw = CONTENT_W / 2
            for i, stat in enumerate(stats):
                col = i % 2
                row = i // 2
                sx = MARGIN + col * sw
                sy = y - 10 * mm - row * 14 * mm
                if sy < 12 * mm:
                    break
                self.text_at(stat.upper(), sx, sy + 5, 7, GRAY, bold=True)
                self.filled_rect(sx, sy - 5, sw - 3, 8, fill=CREAM, stroke=GOLD, stroke_width=0.3)

        self.new_page()

    # ── PAGE 6: FUTURE PLANS ──────────────────────────────────────────────────
    def page_future(self):
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=WHITE)
        self.page_top_strip(PINK)
        self.page_bottom_strip(GOLD, page_num=6)
        self.corner_marks()

        self.section_header("Future Plans & Dreams", PAGE_H - 22 * mm, color=PINK, font_size=18)

        prompts = [
            ("My plans for the next year...", 18 * mm),
            ("My dream career or calling...", 15 * mm),
            ("Places I want to travel...", 13 * mm),
            ("Things I want to learn or try...", 13 * mm),
        ]
        y = PAGE_H - 36 * mm
        for prompt, h in prompts:
            if y - h < 55 * mm:
                break
            self.ruled_box(MARGIN, y - h, CONTENT_W, h, label=prompt, fill=CREAM)
            y -= h + 4 * mm

        # Bucket list
        self.gold_line(y + 2 * mm)
        self.text_at("My Graduation Bucket List", MARGIN, y - 2 * mm, 11, DARK, bold=True)
        y -= 10 * mm
        for i in range(8):
            if y - 8 < 40 * mm:
                break
            # Checkbox
            self.filled_rect(MARGIN, y - 5, 4 * mm, 4 * mm, fill=WHITE, stroke=GOLD, stroke_width=0.4)
            self.filled_rect(MARGIN + 5 * mm, y - 6, CONTENT_W - 5 * mm, 6 * mm,
                             fill=CREAM, stroke=GOLD, stroke_width=0.3)
            y -= 10 * mm

        # Letter to future self
        remaining = y - 14 * mm
        if remaining > 20 * mm:
            self.gold_line(y + 2 * mm)
            self.ruled_box(MARGIN, 14 * mm, CONTENT_W, remaining - 2 * mm,
                           label="A letter to my future self...", fill=CREAM)

        self.new_page()

    # ── PAGE 7: MESSAGES FROM FAMILY ─────────────────────────────────────────
    def page_messages(self):
        self.filled_rect(0, 0, PAGE_W, PAGE_H, fill=WHITE)
        self.page_top_strip(GOLD)
        self.page_bottom_strip(PINK, page_num=7)
        self.corner_marks()

        self.section_header("Messages from Family & Friends", PAGE_H - 22 * mm, color=GOLD, font_size=18)

        self.c.saveState()
        self.c.setFont("Helvetica-Oblique", 10)
        self.c.setFillColor(GRAY)
        self.c.drawString(MARGIN, PAGE_H - 31 * mm,
                          "Share this page — ask loved ones to write a special message to keep forever.")
        self.c.restoreState()

        box_h = 46 * mm
        gap = 4 * mm
        y = PAGE_H - 40 * mm

        for i in range(4):
            if y - box_h < 12 * mm:
                break
            fill = CREAM if i % 2 == 0 else WHITE
            self.filled_rect(MARGIN, y - box_h, CONTENT_W, box_h, fill=fill, stroke=GOLD, stroke_width=0.5)

            # Name & relationship row at top
            name_w = 55 * mm
            rel_w = 50 * mm
            self.filled_rect(MARGIN + 3, y - 9 * mm, name_w, 7 * mm, fill=WHITE, stroke=GOLD, stroke_width=0.3)
            self.text_at("NAME:", MARGIN + 4, y - 7 * mm, 7, GRAY, bold=True)
            self.filled_rect(MARGIN + 3 + name_w + 5 * mm, y - 9 * mm, rel_w, 7 * mm,
                             fill=WHITE, stroke=GOLD, stroke_width=0.3)
            self.text_at("RELATIONSHIP:", MARGIN + 4 + name_w + 5 * mm, y - 7 * mm, 7, GRAY, bold=True)

            # Writing lines
            num_lines = int((box_h - 12 * mm) / 7)
            for li in range(num_lines):
                ly = y - 12 * mm - li * 7
                if ly < y - box_h + 3:
                    break
                self.c.saveState()
                self.c.setStrokeColor(HexColor("#CCCCCC"))
                self.c.setLineWidth(0.3)
                self.c.line(MARGIN + 4, ly, MARGIN + CONTENT_W - 4, ly)
                self.c.restoreState()

            y -= box_h + gap

        # Final flourish
        if y - 10 * mm > 12 * mm:
            self.gold_line(y - 2 * mm)
            self.c.saveState()
            self.c.setFont("Helvetica-Oblique", 9)
            self.c.setFillColor(GOLD)
            self.c.drawCentredString(PAGE_W / 2, y - 8 * mm,
                                     "Congratulations, Graduate! This is just the beginning. ★")
            self.c.restoreState()

        self.new_page()


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    book = MemoryBook("Graduation_Memory_Book.pdf")

    book.page_cover()
    book.page_about()
    book.page_memories()
    book.page_teachers()
    book.page_achievements()
    book.page_future()
    book.page_messages()

    book.save()


if __name__ == "__main__":
    main()
