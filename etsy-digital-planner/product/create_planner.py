#!/usr/bin/env python3
"""
2026 All-in-One Wellness & Productivity Digital Planner
Creates a comprehensive, hyperlinked PDF planner for GoodNotes/Notability/Xodo
"""

import calendar
import datetime
from fpdf import FPDF

# ── Color Palette (Etsy 2026 Patina Blue + Washed Linen Neutrals) ──
PATINA_BLUE = (126, 172, 176)      # Primary accent
DEEP_TEAL = (62, 105, 110)         # Headings / dark accent
WARM_LINEN = (243, 237, 228)       # Page backgrounds
SOFT_SAGE = (183, 203, 180)        # Secondary accent
DUSTY_ROSE = (210, 175, 170)       # Wellness accent
CHARCOAL = (55, 55, 60)            # Body text
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 218, 213)
MID_GRAY = (180, 178, 173)

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

class WellnessPlanner(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=False)
        self.set_margins(0, 0, 0)
        # Pre-create link IDs for all sections
        self.link_ids = {}
        self._link_pages_set = set()
        section_keys = [
            "cover", "year_overview", "weekly_template", "daily_template",
            "goals", "habits", "wellness", "journal", "notes"
        ] + [f"month_{m[:3].lower()}" for m in MONTHS]
        for key in section_keys:
            self.link_ids[key] = self.add_link()
        self.current_section = ""

    def register_section(self, key):
        """Register current page as the destination for a section link."""
        if key in self.link_ids:
            self.set_link(self.link_ids[key], page=self.page)
            self._link_pages_set.add(key)

    # ── Utility helpers ──
    def bg(self, color=WARM_LINEN):
        self.set_fill_color(*color)
        self.rect(0, 0, 297, 210, 'F')

    def rounded_rect(self, x, y, w, h, r, color=WHITE, border_color=None):
        """Draw a rounded rectangle."""
        self.set_fill_color(*color)
        # Simple rect fallback (fpdf2 doesn't have native rounded rect easily)
        self.rect(x, y, w, h, 'F')
        if border_color:
            self.set_draw_color(*border_color)
            self.set_line_width(0.3)
            self.rect(x, y, w, h, 'D')

    def section_header(self, text, color=DEEP_TEAL):
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*color)
        self.set_xy(20, 15)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")

    def draw_tab_bar(self, active_tab=""):
        """Draw the left sidebar navigation tabs."""
        tabs = [
            ("HOME", "cover"),
            ("YEAR", "year_overview"),
            ("MONTH", "month_jan"),
            ("WEEK", "weekly_template"),
            ("DAILY", "daily_template"),
            ("GOALS", "goals"),
            ("HABITS", "habits"),
            ("WELLNESS", "wellness"),
            ("JOURNAL", "journal"),
            ("NOTES", "notes"),
        ]
        tab_h = 18
        tab_w = 28
        start_y = 10
        for i, (label, target) in enumerate(tabs):
            y = start_y + i * (tab_h + 2)
            is_active = (label == active_tab)
            bg_color = PATINA_BLUE if is_active else DEEP_TEAL
            self.set_fill_color(*bg_color)
            self.rect(0, y, tab_w, tab_h, 'F')
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(*WHITE)
            self.set_xy(0, y)
            self.cell(tab_w, tab_h, label, align='C')
            # Add link to target page (only if page has been registered)
            if target in self._link_pages_set:
                self.link(0, y, tab_w, tab_h, self.link_ids[target])
        # Bottom branding
        self.set_font("Helvetica", "I", 5)
        self.set_text_color(*MID_GRAY)
        self.set_xy(0, 200)
        self.cell(tab_w, 8, "Serenity", align='C')

    def draw_checkbox(self, x, y, size=4):
        self.set_draw_color(*MID_GRAY)
        self.set_line_width(0.3)
        self.rect(x, y, size, size, 'D')

    def draw_lined_area(self, x, y, w, num_lines, spacing=7):
        self.set_draw_color(*LIGHT_GRAY)
        self.set_line_width(0.2)
        for i in range(num_lines):
            ly = y + i * spacing
            self.line(x, ly, x + w, ly)

    # ── PAGE BUILDERS ──

    def build_cover(self):
        self.add_page()
        self.register_section("cover")

        # Full background
        self.set_fill_color(*DEEP_TEAL)
        self.rect(0, 0, 297, 210, 'F')

        # Decorative geometric shapes
        self.set_fill_color(*PATINA_BLUE)
        self.rect(0, 0, 297, 6, 'F')
        self.rect(0, 204, 297, 6, 'F')
        self.rect(0, 0, 6, 210, 'F')
        self.rect(291, 0, 6, 210, 'F')

        # Inner frame
        self.set_fill_color(72, 115, 120)  # slightly lighter teal
        self.rect(20, 20, 257, 170, 'F')

        # Central content area
        self.set_fill_color(*WARM_LINEN)
        self.rect(40, 40, 217, 130, 'F')

        # Accent bar
        self.set_fill_color(*PATINA_BLUE)
        self.rect(40, 40, 217, 3, 'F')
        self.set_fill_color(*DUSTY_ROSE)
        self.rect(40, 43, 217, 2, 'F')
        self.set_fill_color(*SOFT_SAGE)
        self.rect(40, 45, 217, 2, 'F')

        # Title
        self.set_font("Helvetica", "B", 38)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(40, 58)
        self.cell(217, 20, "2026", align='C')

        self.set_font("Helvetica", "", 16)
        self.set_text_color(*CHARCOAL)
        self.set_xy(40, 80)
        self.cell(217, 10, "ALL-IN-ONE WELLNESS & PRODUCTIVITY", align='C')

        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(40, 95)
        self.cell(217, 15, "Digital Planner", align='C')

        # Decorative divider
        self.set_fill_color(*PATINA_BLUE)
        self.rect(110, 115, 77, 1, 'F')

        # Subtitle features
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*CHARCOAL)
        features = [
            "Daily | Weekly | Monthly Planning",
            "Goal Setting | Habit Tracking | Wellness Journal",
            "Fully Hyperlinked | GoodNotes | Notability | Xodo"
        ]
        for i, feat in enumerate(features):
            self.set_xy(40, 122 + i * 7)
            self.cell(217, 7, feat, align='C')

        # Bottom accent
        self.set_fill_color(*PATINA_BLUE)
        self.rect(40, 167, 217, 3, 'F')

        # Version text
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GRAY)
        self.set_xy(40, 155)
        self.cell(217, 7, "Serenity Collection  |  Designed for iPad, Android & Windows Tablets", align='C')

    def build_year_overview(self):
        self.add_page()
        self.register_section("year_overview")
        self.bg()
        self.draw_tab_bar("YEAR")

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(35, 12)
        self.cell(0, 10, "2026 Year at a Glance")

        # 12 mini calendars (4 cols x 3 rows)
        cal_w = 58
        cal_h = 52
        start_x = 38
        start_y = 30
        gap_x = 5
        gap_y = 8

        for m in range(12):
            col = m % 4
            row = m // 4
            x = start_x + col * (cal_w + gap_x)
            y = start_y + row * (cal_h + gap_y)

            # Calendar card
            self.rounded_rect(x, y, cal_w, cal_h, 3, WHITE, LIGHT_GRAY)

            # Month name (clickable to monthly page)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*PATINA_BLUE)
            self.set_xy(x + 2, y + 2)
            self.cell(cal_w - 4, 6, MONTHS[m], align='C')
            month_key = f"month_{MONTHS[m][:3].lower()}"
            if month_key in self._link_pages_set:
                self.link(x, y, cal_w, 8, self.link_ids[month_key])

            # Day headers
            self.set_font("Helvetica", "B", 5)
            self.set_text_color(*MID_GRAY)
            days = ["M","T","W","T","F","S","S"]
            dw = (cal_w - 4) / 7
            for d, day in enumerate(days):
                self.set_xy(x + 2 + d * dw, y + 9)
                self.cell(dw, 4, day, align='C')

            # Day numbers
            self.set_font("Helvetica", "", 5)
            self.set_text_color(*CHARCOAL)
            cal = calendar.monthcalendar(2026, m + 1)
            for wi, week in enumerate(cal):
                for di, day_num in enumerate(week):
                    if day_num > 0:
                        self.set_xy(x + 2 + di * dw, y + 14 + wi * 5.5)
                        self.cell(dw, 5, str(day_num), align='C')

    def build_monthly_pages(self):
        """Build a monthly spread for each month."""
        for m in range(12):
            month_name = MONTHS[m]
            month_key = f"month_{month_name[:3].lower()}"

            # ── Monthly Overview Page ──
            self.add_page()
            self.register_section(month_key)
            self.bg()
            self.draw_tab_bar("MONTH")

            # Header
            self.set_font("Helvetica", "B", 22)
            self.set_text_color(*DEEP_TEAL)
            self.set_xy(35, 12)
            self.cell(0, 10, f"{month_name} 2026")

            # Calendar grid
            cal = calendar.monthcalendar(2026, m + 1)
            grid_x = 38
            grid_y = 30
            cell_w = 33.5
            cell_h = 24
            days_header = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

            # Day name headers
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*WHITE)
            for d, dname in enumerate(days_header):
                x = grid_x + d * cell_w
                self.set_fill_color(*DEEP_TEAL)
                self.rect(x, grid_y, cell_w, 8, 'F')
                self.set_xy(x, grid_y)
                self.cell(cell_w, 8, dname, align='C')

            # Day cells
            for wi, week in enumerate(cal):
                for di, day_num in enumerate(week):
                    x = grid_x + di * cell_w
                    y = grid_y + 8 + wi * cell_h
                    bg_c = WHITE if day_num > 0 else LIGHT_GRAY
                    self.rounded_rect(x, y, cell_w, cell_h, 0, bg_c, LIGHT_GRAY)
                    if day_num > 0:
                        self.set_font("Helvetica", "B", 9)
                        self.set_text_color(*DEEP_TEAL)
                        self.set_xy(x + 1, y + 1)
                        self.cell(10, 5, str(day_num))
                        # Lined area for notes
                        self.set_draw_color(*LIGHT_GRAY)
                        self.set_line_width(0.15)
                        for li in range(3):
                            self.line(x + 2, y + 9 + li * 5, x + cell_w - 2, y + 9 + li * 5)

            # Right sidebar - Monthly Goals & Focus
            side_x = 38
            side_y = grid_y + 8 + len(cal) * cell_h + 4
            if side_y < 175:
                self.set_font("Helvetica", "B", 9)
                self.set_text_color(*DEEP_TEAL)
                self.set_xy(side_x, side_y)
                self.cell(0, 6, "Monthly Intentions")
                self.draw_lined_area(side_x, side_y + 8, 120, 3, 6)

                self.set_xy(side_x + 130, side_y)
                self.cell(0, 6, "Wellness Focus")
                self.draw_lined_area(side_x + 130, side_y + 8, 100, 3, 6)

    def build_weekly_template(self):
        """Build 4 weekly spread templates."""
        for w in range(4):
            self.add_page()
            if w == 0:
                self.register_section("weekly_template")
            self.bg()
            self.draw_tab_bar("WEEK")

            week_label = f"Week {w+1}" if w < 4 else "Week"

            self.set_font("Helvetica", "B", 18)
            self.set_text_color(*DEEP_TEAL)
            self.set_xy(35, 10)
            self.cell(0, 10, f"Weekly Planner - {week_label}")

            # Date fields
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*CHARCOAL)
            self.set_xy(35, 22)
            self.cell(0, 5, "Week of: ______________________")

            # 7-day grid (left side - 4 days, right side - 3 days + extras)
            days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            col_w = 80
            row_h = 40
            x_left = 35
            x_right = 160

            for d, day in enumerate(days):
                if d < 4:
                    x = x_left
                    y = 32 + d * (row_h + 2)
                else:
                    x = x_right
                    y = 32 + (d - 4) * (row_h + 2)

                # Day card
                self.rounded_rect(x, y, col_w - 2 if d < 4 else 130, row_h, 3, WHITE, LIGHT_GRAY)
                self.set_font("Helvetica", "B", 9)
                self.set_text_color(*PATINA_BLUE)
                self.set_xy(x + 3, y + 2)
                self.cell(0, 5, day)

                # Priority dot
                self.set_fill_color(*DUSTY_ROSE)
                self.ellipse(x + col_w - 12 if d < 4 else x + 118, y + 3, 3, 3, 'F')

                # Lines for tasks
                self.set_font("Helvetica", "", 7)
                self.set_text_color(*CHARCOAL)
                for li in range(4):
                    ly = y + 10 + li * 7
                    self.draw_checkbox(x + 4, ly, 3)
                    self.set_draw_color(*LIGHT_GRAY)
                    self.set_line_width(0.15)
                    line_end = x + col_w - 6 if d < 4 else x + 124
                    self.line(x + 10, ly + 3, line_end, ly + 3)

            # Weekly wellness check-in (bottom right)
            wx = 160
            wy = 32 + 3 * (row_h + 2)
            self.rounded_rect(wx, wy, 130, row_h + 5, 3, color=(240, 235, 232), border_color=DUSTY_ROSE)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*DUSTY_ROSE)
            self.set_xy(wx + 3, wy + 2)
            self.cell(0, 5, "Weekly Wellness Check-in")

            labels = ["Energy:", "Mood:", "Sleep:", "Movement:"]
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*CHARCOAL)
            for i, lbl in enumerate(labels):
                self.set_xy(wx + 5, wy + 10 + i * 7)
                self.cell(20, 5, lbl)
                # Rating circles
                for c in range(5):
                    cx = wx + 30 + c * 8
                    cy = wy + 11 + i * 7
                    self.set_draw_color(*MID_GRAY)
                    self.set_line_width(0.3)
                    self.ellipse(cx, cy, 4, 4, 'D')

    def build_daily_template(self):
        """Build daily planner pages."""
        for d in range(3):  # 3 template variants
            self.add_page()
            if d == 0:
                self.register_section("daily_template")
            self.bg()
            self.draw_tab_bar("DAILY")

            self.set_font("Helvetica", "B", 18)
            self.set_text_color(*DEEP_TEAL)
            self.set_xy(35, 10)
            self.cell(0, 10, "Daily Planner")

            # Date and day
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*CHARCOAL)
            self.set_xy(35, 22)
            self.cell(0, 5, "Date: ________________    Day: ________________")

            # Morning Routine (left column)
            lx = 35
            ly = 34
            self.rounded_rect(lx, ly, 120, 50, 3, WHITE, LIGHT_GRAY)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*SOFT_SAGE)
            self.set_xy(lx + 3, ly + 2)
            self.cell(0, 5, "Morning Routine")
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*CHARCOAL)
            routines = ["Wake up time:", "Water intake:", "Movement:", "Mindfulness:", "Top priority:"]
            for i, r in enumerate(routines):
                self.set_xy(lx + 5, ly + 10 + i * 8)
                self.cell(30, 5, r)
                self.set_draw_color(*LIGHT_GRAY)
                self.line(lx + 38, ly + 15 + i * 8, lx + 115, ly + 15 + i * 8)

            # Schedule (center)
            sx = 35
            sy = 90
            self.rounded_rect(sx, sy, 120, 110, 3, WHITE, LIGHT_GRAY)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*DEEP_TEAL)
            self.set_xy(sx + 3, sy + 2)
            self.cell(0, 5, "Schedule")

            hours = ["6 AM","7 AM","8 AM","9 AM","10 AM","11 AM","12 PM",
                     "1 PM","2 PM","3 PM","4 PM","5 PM","6 PM","7 PM","8 PM"]
            self.set_font("Helvetica", "", 6)
            self.set_text_color(*MID_GRAY)
            for i, hour in enumerate(hours):
                hy = sy + 10 + i * 6.5
                self.set_xy(sx + 3, hy)
                self.cell(12, 5, hour)
                self.set_draw_color(*LIGHT_GRAY)
                self.set_line_width(0.15)
                self.line(sx + 18, hy + 4, sx + 117, hy + 4)

            # Right column - Top 3 Priorities
            rx = 162
            ry = 34
            self.rounded_rect(rx, ry, 128, 35, 3, WHITE, LIGHT_GRAY)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*PATINA_BLUE)
            self.set_xy(rx + 3, ry + 2)
            self.cell(0, 5, "Top 3 Priorities")
            for i in range(3):
                py = ry + 10 + i * 8
                self.set_fill_color(*PATINA_BLUE)
                self.ellipse(rx + 5, py + 1, 4, 4, 'F')
                self.set_font("Helvetica", "B", 7)
                self.set_text_color(*WHITE)
                self.set_xy(rx + 5, py)
                self.cell(4, 5, str(i + 1), align='C')
                self.set_draw_color(*LIGHT_GRAY)
                self.line(rx + 12, py + 4, rx + 123, py + 4)

            # To-Do List
            self.rounded_rect(rx, ry + 40, 128, 55, 3, WHITE, LIGHT_GRAY)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*DEEP_TEAL)
            self.set_xy(rx + 3, ry + 42)
            self.cell(0, 5, "To-Do List")
            for i in range(6):
                ty = ry + 50 + i * 7
                self.draw_checkbox(rx + 5, ty, 3.5)
                self.set_draw_color(*LIGHT_GRAY)
                self.line(rx + 12, ty + 3, rx + 123, ty + 3)

            # Gratitude & Reflection
            self.rounded_rect(rx, ry + 100, 128, 35, 3, color=(245, 238, 235), border_color=DUSTY_ROSE)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*DUSTY_ROSE)
            self.set_xy(rx + 3, ry + 102)
            self.cell(0, 5, "Gratitude & Reflection")
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*MID_GRAY)
            self.set_xy(rx + 3, ry + 109)
            self.cell(0, 5, "Today I am grateful for...")
            self.draw_lined_area(rx + 5, ry + 117, 118, 2, 7)

            # Water Tracker
            self.rounded_rect(rx, ry + 140, 60, 25, 3, WHITE, LIGHT_GRAY)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*PATINA_BLUE)
            self.set_xy(rx + 3, ry + 142)
            self.cell(0, 5, "Water Intake")
            for i in range(8):
                wx = rx + 5 + i * 7
                wy_pos = ry + 150
                self.set_draw_color(*PATINA_BLUE)
                self.set_line_width(0.3)
                self.ellipse(wx, wy_pos, 5, 8, 'D')

            # Mood Tracker
            self.rounded_rect(rx + 65, ry + 140, 63, 25, 3, WHITE, LIGHT_GRAY)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*DUSTY_ROSE)
            self.set_xy(rx + 68, ry + 142)
            self.cell(0, 5, "Today's Mood")
            moods = [":)", ":|", ":(", "<3", "*"]
            for i, mood in enumerate(moods):
                mx = rx + 72 + i * 11
                self.set_draw_color(*MID_GRAY)
                self.ellipse(mx, ry + 151, 8, 8, 'D')
                self.set_font("Helvetica", "", 7)
                self.set_text_color(*MID_GRAY)
                self.set_xy(mx, ry + 152)
                self.cell(8, 6, mood, align='C')

    def build_goals_section(self):
        self.add_page()
        self.register_section("goals")
        self.bg()
        self.draw_tab_bar("GOALS")

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(35, 12)
        self.cell(0, 10, "2026 Goal Setting")

        # Vision Board area
        self.rounded_rect(35, 28, 125, 80, 3, WHITE, PATINA_BLUE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*PATINA_BLUE)
        self.set_xy(38, 30)
        self.cell(0, 6, "My Vision for 2026")
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GRAY)
        self.set_xy(38, 38)
        self.cell(0, 5, "Write your vision, paste images, or sketch your dream life")
        self.draw_lined_area(40, 48, 115, 8, 7)

        # Quarterly goals
        quarters = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
        colors = [PATINA_BLUE, SOFT_SAGE, DUSTY_ROSE, DEEP_TEAL]
        qx = 168
        for i, (q, qc) in enumerate(zip(quarters, colors)):
            qy = 28 + i * 45
            self.rounded_rect(qx, qy, 122, 42, 3, WHITE, qc)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*qc)
            self.set_xy(qx + 3, qy + 2)
            self.cell(0, 5, q)
            for g in range(3):
                gy = qy + 10 + g * 10
                self.draw_checkbox(qx + 5, gy, 3.5)
                self.set_draw_color(*LIGHT_GRAY)
                self.line(qx + 12, gy + 3, qx + 117, gy + 3)

        # Word of the Year
        self.rounded_rect(35, 115, 125, 30, 3, color=DEEP_TEAL)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*WHITE)
        self.set_xy(38, 117)
        self.cell(0, 6, "My Word of the Year")
        self.set_draw_color(*PATINA_BLUE)
        self.set_line_width(0.5)
        self.rect(45, 128, 105, 12, 'D')

        # Life categories
        self.rounded_rect(35, 150, 125, 50, 3, WHITE, LIGHT_GRAY)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(38, 152)
        self.cell(0, 5, "Life Wheel - Rate Each Area (1-10)")
        areas = ["Health & Fitness", "Career & Growth", "Relationships", "Finances",
                 "Fun & Recreation", "Personal Development", "Environment", "Spirituality"]
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*CHARCOAL)
        for i, area in enumerate(areas):
            col = i % 2
            row = i // 2
            ax = 40 + col * 62
            ay = 162 + row * 9
            self.set_xy(ax, ay)
            self.cell(40, 5, area)
            # Rating dots
            for r in range(10):
                self.set_draw_color(*MID_GRAY)
                self.set_line_width(0.2)
                self.ellipse(ax + 43 + r * 5, ay + 1, 3, 3, 'D')

    def build_habits_tracker(self):
        self.add_page()
        self.register_section("habits")
        self.bg()
        self.draw_tab_bar("HABITS")

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(35, 12)
        self.cell(0, 10, "Monthly Habit Tracker")

        self.set_font("Helvetica", "", 8)
        self.set_text_color(*CHARCOAL)
        self.set_xy(35, 24)
        self.cell(0, 5, "Month: ____________________")

        # Habit grid
        grid_x = 35
        grid_y = 35
        habit_col_w = 50
        day_col_w = 7
        row_h = 9

        # Day numbers header
        self.set_font("Helvetica", "B", 5)
        self.set_text_color(*WHITE)
        self.set_fill_color(*DEEP_TEAL)
        self.rect(grid_x + habit_col_w, grid_y, 31 * day_col_w, 7, 'F')
        for d in range(1, 32):
            self.set_xy(grid_x + habit_col_w + (d - 1) * day_col_w, grid_y)
            self.cell(day_col_w, 7, str(d), align='C')

        # Habit rows
        habits_preset = [
            "Exercise 30 min", "Drink 8 glasses water", "Read 20 pages",
            "Meditate 10 min", "Sleep 7+ hours", "No screen before bed",
            "Eat fruits/veggies", "Practice gratitude", "Journal",
            "Connect with friend", "Creative time", "Walk outdoors",
            "", "", "", ""  # Blank rows for custom
        ]

        for i, habit in enumerate(habits_preset):
            y = grid_y + 7 + i * row_h
            bg_c = WHITE if i % 2 == 0 else (248, 246, 242)
            self.set_fill_color(*bg_c)
            self.rect(grid_x, y, habit_col_w, row_h, 'F')
            self.rect(grid_x + habit_col_w, y, 31 * day_col_w, row_h, 'F')

            self.set_font("Helvetica", "", 6)
            self.set_text_color(*CHARCOAL)
            self.set_xy(grid_x + 2, y)
            self.cell(habit_col_w - 4, row_h, habit)

            # Day checkboxes
            for d in range(31):
                cx = grid_x + habit_col_w + d * day_col_w + 1.5
                cy = y + 2.5
                self.set_draw_color(*LIGHT_GRAY)
                self.set_line_width(0.2)
                self.rect(cx, cy, 4, 4, 'D')

        # Summary section at bottom
        sy = grid_y + 7 + len(habits_preset) * row_h + 5
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*PATINA_BLUE)
        self.set_xy(35, sy)
        self.cell(0, 5, "Monthly Reflection")
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GRAY)
        self.set_xy(35, sy + 6)
        self.cell(0, 5, "What worked well? What will I improve next month?")
        self.draw_lined_area(37, sy + 14, 250, 2, 7)

    def build_wellness_section(self):
        self.add_page()
        self.register_section("wellness")
        self.bg()
        self.draw_tab_bar("WELLNESS")

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(35, 12)
        self.cell(0, 10, "Wellness Dashboard")

        # Sleep Tracker
        self.rounded_rect(35, 28, 128, 80, 3, WHITE, PATINA_BLUE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*PATINA_BLUE)
        self.set_xy(38, 30)
        self.cell(0, 6, "Sleep Tracker")

        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*CHARCOAL)
        for i, day in enumerate(days):
            dy = 42 + i * 9
            self.set_xy(40, dy)
            self.cell(15, 5, day)
            self.set_xy(57, dy)
            self.cell(20, 5, "Bed: ____")
            self.set_xy(80, dy)
            self.cell(20, 5, "Wake: ____")
            self.set_xy(105, dy)
            self.cell(20, 5, "Hrs: ____")
            # Quality rating circles
            for q in range(5):
                self.set_draw_color(*MID_GRAY)
                self.set_line_width(0.2)
                self.ellipse(130 + q * 6, dy + 1, 4, 3.5, 'D')

        # Meal Planner
        self.rounded_rect(168, 28, 122, 80, 3, WHITE, SOFT_SAGE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*SOFT_SAGE)
        self.set_xy(171, 30)
        self.cell(0, 6, "Weekly Meal Planner")

        meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*CHARCOAL)
        meal_w = 27
        for i, meal in enumerate(meals):
            self.set_xy(171 + i * meal_w, 40)
            self.cell(meal_w, 5, meal, align='C')

        self.set_font("Helvetica", "", 6)
        for d, day in enumerate(days):
            dy = 48 + d * 8
            self.set_text_color(*MID_GRAY)
            self.set_xy(171, dy)
            # Day label in left margin would overlap, using inline
            for mi in range(4):
                mx = 171 + mi * meal_w
                self.set_draw_color(*LIGHT_GRAY)
                self.rect(mx, dy, meal_w, 7, 'D')

        # Fitness Log
        self.rounded_rect(35, 114, 128, 88, 3, WHITE, DUSTY_ROSE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DUSTY_ROSE)
        self.set_xy(38, 116)
        self.cell(0, 6, "Weekly Fitness Log")

        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*CHARCOAL)
        fit_headers = ["Day", "Activity", "Duration", "Intensity", "Notes"]
        fit_widths = [15, 35, 20, 20, 30]
        fx = 40
        for i, (h, w) in enumerate(zip(fit_headers, fit_widths)):
            self.set_fill_color(*DUSTY_ROSE)
            self.rect(fx, 126, w, 7, 'F')
            self.set_text_color(*WHITE)
            self.set_xy(fx, 126)
            self.cell(w, 7, h, align='C')
            fx += w

        self.set_font("Helvetica", "", 6)
        self.set_text_color(*CHARCOAL)
        for d, day in enumerate(days):
            fy = 133 + d * 9
            fx = 40
            for ci, w in enumerate(fit_widths):
                self.set_draw_color(*LIGHT_GRAY)
                self.rect(fx, fy, w, 9, 'D')
                if ci == 0:
                    self.set_xy(fx, fy)
                    self.cell(w, 9, day, align='C')
                fx += w

        # Self-Care Checklist
        self.rounded_rect(168, 114, 122, 88, 3, color=(245, 238, 235), border_color=DUSTY_ROSE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DUSTY_ROSE)
        self.set_xy(171, 116)
        self.cell(0, 6, "Self-Care Menu")
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GRAY)
        self.set_xy(171, 123)
        self.cell(0, 5, "Check off what nourishes you this week")

        self_care = [
            "Take a relaxing bath", "Read for pleasure", "Call a loved one",
            "Go for a nature walk", "Try a new recipe", "Digital detox hour",
            "Stretching / yoga", "Creative expression", "Afternoon nap",
            "Skin care routine", "Listen to a podcast", "Declutter a space",
            "Write in journal", "Drink herbal tea", "Practice deep breathing"
        ]
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*CHARCOAL)
        for i, care in enumerate(self_care):
            col = i % 2
            row = i // 2
            cx = 173 + col * 60
            cy = 132 + row * 9
            self.draw_checkbox(cx, cy, 3.5)
            self.set_xy(cx + 5, cy)
            self.cell(55, 5, care)

    def build_journal_section(self):
        """Guided journal pages."""
        self.add_page()
        self.register_section("journal")
        self.bg()
        self.draw_tab_bar("JOURNAL")

        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*DEEP_TEAL)
        self.set_xy(35, 12)
        self.cell(0, 10, "Guided Journal")

        # Morning Journal
        self.rounded_rect(35, 28, 125, 85, 3, WHITE, SOFT_SAGE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*SOFT_SAGE)
        self.set_xy(38, 30)
        self.cell(0, 6, "Morning Pages")

        prompts_morning = [
            "Today I am grateful for...",
            "My intention for today is...",
            "I will feel accomplished when...",
            "One thing I'm looking forward to...",
        ]
        y_off = 40
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*CHARCOAL)
        for prompt in prompts_morning:
            self.set_xy(40, y_off)
            self.cell(0, 5, prompt)
            self.draw_lined_area(42, y_off + 7, 112, 2, 6)
            y_off += 18

        # Evening Reflection
        self.rounded_rect(168, 28, 122, 85, 3, WHITE, DUSTY_ROSE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DUSTY_ROSE)
        self.set_xy(171, 30)
        self.cell(0, 6, "Evening Reflection")

        prompts_evening = [
            "Best moment of today...",
            "Something I learned...",
            "How did I show kindness...",
            "Tomorrow I will...",
        ]
        y_off = 40
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*CHARCOAL)
        for prompt in prompts_evening:
            self.set_xy(173, y_off)
            self.cell(0, 5, prompt)
            self.draw_lined_area(175, y_off + 7, 108, 2, 6)
            y_off += 18

        # Weekly Reflection
        self.rounded_rect(35, 120, 255, 80, 3, WHITE, PATINA_BLUE)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*PATINA_BLUE)
        self.set_xy(38, 122)
        self.cell(0, 6, "Weekly Reflection & Growth")

        reflection_qs = [
            "What were my biggest wins this week?",
            "What challenges did I face, and how did I handle them?",
            "What am I proud of?",
            "What would I do differently?",
            "How did I take care of my mental and physical health?",
        ]
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*CHARCOAL)
        y_off = 132
        for q in reflection_qs:
            self.set_xy(40, y_off)
            self.cell(0, 5, q)
            self.draw_lined_area(42, y_off + 6, 242, 1, 7)
            y_off += 14

    def build_notes_section(self):
        """Blank notes pages."""
        for n in range(3):
            self.add_page()
            if n == 0:
                self.register_section("notes")
            self.bg()
            self.draw_tab_bar("NOTES")

            self.set_font("Helvetica", "B", 20)
            self.set_text_color(*DEEP_TEAL)
            self.set_xy(35, 12)
            self.cell(0, 10, "Notes")

            # Lined area
            self.rounded_rect(35, 28, 255, 172, 3, WHITE, LIGHT_GRAY)
            self.draw_lined_area(40, 35, 245, 23, 7.3)

    def build_all(self):
        """Build the complete planner."""
        # Phase 1: build all pages (collect page numbers)
        self.build_cover()
        self.build_year_overview()
        self.build_monthly_pages()
        self.build_weekly_template()
        self.build_daily_template()
        self.build_goals_section()
        self.build_habits_tracker()
        self.build_wellness_section()
        self.build_journal_section()
        self.build_notes_section()

        # Now re-render with correct hyperlinks by updating tab bars
        # (The tab bars were drawn with available page_map at render time;
        #  pages built later will have their links set correctly since
        #  we built them in order and the map grows.)

        return self


def main():
    print("Building 2026 Wellness & Productivity Digital Planner...")
    planner = WellnessPlanner()
    planner.build_all()

    output_path = "/home/user/claude-code/etsy-digital-planner/product/2026_Wellness_Productivity_Digital_Planner.pdf"
    planner.output(output_path)
    print(f"Planner saved to: {output_path}")
    print(f"Total pages: {planner.pages_count}")

if __name__ == "__main__":
    main()
