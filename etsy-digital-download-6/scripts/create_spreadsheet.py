#!/usr/bin/env python3
"""Create Social Media Marketing Planner 2026 spreadsheet."""

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, NamedStyle, numbers
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from datetime import datetime, timedelta
import calendar

# ── Colors ──
HOT_PINK = "D53F8C"
PURPLE = "6B46C1"
ELECTRIC_BLUE = "3182CE"
CORAL = "FC8181"
MINT = "68D391"
PALE_PINK = "FED7E2"
DARK_TEXT = "1A202C"
WHITE = "FFFFFF"
LIGHT_GRAY = "F7FAFC"
MED_GRAY = "E2E8F0"
DARK_GRAY = "4A5568"

# ── Fills ──
header_fill = PatternFill("solid", fgColor=HOT_PINK)
header_fill_purple = PatternFill("solid", fgColor=PURPLE)
header_fill_blue = PatternFill("solid", fgColor=ELECTRIC_BLUE)
header_fill_coral = PatternFill("solid", fgColor=CORAL)
header_fill_mint = PatternFill("solid", fgColor=MINT)
pale_pink_fill = PatternFill("solid", fgColor=PALE_PINK)
alt_row_fill = PatternFill("solid", fgColor="FFF5F7")
light_gray_fill = PatternFill("solid", fgColor=LIGHT_GRAY)
white_fill = PatternFill("solid", fgColor=WHITE)
mint_fill = PatternFill("solid", fgColor=MINT)

# ── Fonts ──
header_font = Font(name="Calibri", bold=True, color=WHITE, size=12)
title_font = Font(name="Calibri", bold=True, color=DARK_TEXT, size=16)
subtitle_font = Font(name="Calibri", bold=True, color=HOT_PINK, size=13)
body_font = Font(name="Calibri", color=DARK_TEXT, size=11)
bold_font = Font(name="Calibri", bold=True, color=DARK_TEXT, size=11)
link_font = Font(name="Calibri", color=ELECTRIC_BLUE, size=11, underline="single")
total_font = Font(name="Calibri", bold=True, color=WHITE, size=12)
pink_font = Font(name="Calibri", bold=True, color=HOT_PINK, size=11)

# ── Borders ──
thin_border = Border(
    left=Side(style="thin", color=MED_GRAY),
    right=Side(style="thin", color=MED_GRAY),
    top=Side(style="thin", color=MED_GRAY),
    bottom=Side(style="thin", color=MED_GRAY),
)

# ── Alignments ──
center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
wrap_align = Alignment(horizontal="left", vertical="top", wrap_text=True)


def style_header_row(ws, row, cols, fill=None, font=None):
    """Apply header styling to a row."""
    f = fill or header_fill
    fn = font or header_font
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = f
        cell.font = fn
        cell.alignment = center_align
        cell.border = thin_border


def style_data_rows(ws, start_row, end_row, cols):
    """Apply alternating row styling."""
    for row in range(start_row, end_row + 1):
        fill = alt_row_fill if row % 2 == 0 else white_fill
        for col in range(1, cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = fill
            cell.font = body_font
            cell.alignment = center_align
            cell.border = thin_border


def set_col_widths(ws, widths):
    """Set column widths from a dict {col_letter: width}."""
    for letter, w in widths.items():
        ws.column_dimensions[letter].width = w


def add_title_banner(ws, title, subtitle, cols):
    """Add a styled title banner at top of sheet."""
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=cols)
    cell = ws.cell(row=1, column=1, value=title)
    cell.font = Font(name="Calibri", bold=True, color=WHITE, size=18)
    cell.fill = PatternFill("solid", fgColor=PURPLE)
    cell.alignment = center_align
    ws.row_dimensions[1].height = 45

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=cols)
    cell2 = ws.cell(row=2, column=1, value=subtitle)
    cell2.font = Font(name="Calibri", bold=True, color=HOT_PINK, size=12)
    cell2.fill = pale_pink_fill
    cell2.alignment = center_align
    ws.row_dimensions[2].height = 30


# ══════════════════════════════════════════════════════════════════
wb = Workbook()

# ═══════════ TAB 1: CONTENT CALENDAR ═══════════
ws1 = wb.active
ws1.title = "Content Calendar"
ws1.sheet_properties.tabColor = HOT_PINK

add_title_banner(ws1, "📅 CONTENT CALENDAR 2026", "Plan • Schedule • Track • Grow", 10)

headers1 = ["Date", "Day", "Platform", "Content Type", "Topic / Caption",
            "Hashtags", "Status", "Engagement", "Link", "Notes"]
for col, h in enumerate(headers1, 1):
    ws1.cell(row=3, column=col, value=h)
style_header_row(ws1, 3, 10)
ws1.row_dimensions[3].height = 30

# Date auto-fill + Day formula for 100 rows
start_date = datetime(2026, 1, 1)
for i in range(100):
    row = 4 + i
    date_cell = ws1.cell(row=row, column=1)
    date_cell.value = start_date + timedelta(days=i)
    date_cell.number_format = "MMM DD, YYYY"
    # Day auto-calc
    ws1.cell(row=row, column=2, value=f'=TEXT(A{row},"DDDD")')

style_data_rows(ws1, 4, 103, 10)

# Dropdowns
dv_platform = DataValidation(type="list", formula1='"Instagram,TikTok,YouTube,Pinterest,Facebook,Twitter,LinkedIn,Blog,Email"', allow_blank=True)
dv_platform.prompt = "Select platform"
dv_platform.promptTitle = "Platform"
ws1.add_data_validation(dv_platform)
dv_platform.add("C4:C103")

dv_content = DataValidation(type="list", formula1='"Photo,Video,Carousel,Reel,Story,Blog,Newsletter"', allow_blank=True)
ws1.add_data_validation(dv_content)
dv_content.add("D4:D103")

dv_status = DataValidation(type="list", formula1='"Idea,Draft,Scheduled,Published,Boosted"', allow_blank=True)
ws1.add_data_validation(dv_status)
dv_status.add("G4:G103")

# Conditional formatting for status
ws1.conditional_formatting.add("G4:G103",
    CellIsRule(operator="equal", formula=['"Published"'], fill=PatternFill("solid", fgColor=MINT)))
ws1.conditional_formatting.add("G4:G103",
    CellIsRule(operator="equal", formula=['"Boosted"'], fill=PatternFill("solid", fgColor="B794F4")))
ws1.conditional_formatting.add("G4:G103",
    CellIsRule(operator="equal", formula=['"Idea"'], fill=PatternFill("solid", fgColor=PALE_PINK)))

set_col_widths(ws1, {"A": 16, "B": 14, "C": 15, "D": 16, "E": 35, "F": 30, "G": 14, "H": 14, "I": 25, "J": 25})

# Sample data rows
samples = [
    ("Instagram", "Reel", "New Year Goals — 2026 Vision Board", "#goals2026 #visionboard #newyear", "Scheduled"),
    ("TikTok", "Video", "Behind the Scenes Studio Tour", "#bts #smallbusiness #studiolife", "Draft"),
    ("Pinterest", "Photo", "10 Tips for Social Media Growth (Infographic)", "#socialmediatips #growthhacks", "Idea"),
    ("LinkedIn", "Carousel", "Case Study: How We Grew 10K Followers in 30 Days", "#casestudy #linkedin #growth", "Published"),
    ("Blog", "Blog", "Complete Guide to Instagram Reels in 2026", "#instagramreels #blogging", "Draft"),
]
for idx, (plat, ctype, topic, tags, status) in enumerate(samples):
    r = 4 + idx
    ws1.cell(row=r, column=3, value=plat)
    ws1.cell(row=r, column=4, value=ctype)
    ws1.cell(row=r, column=5, value=topic)
    ws1.cell(row=r, column=6, value=tags)
    ws1.cell(row=r, column=7, value=status)

ws1.freeze_panes = "A4"
ws1.auto_filter.ref = "A3:J103"

# ═══════════ TAB 2: ANALYTICS DASHBOARD ═══════════
ws2 = wb.create_sheet("Analytics Dashboard")
ws2.sheet_properties.tabColor = PURPLE

add_title_banner(ws2, "📊 ANALYTICS DASHBOARD 2026", "Track Growth • Measure Impact • Optimize Strategy", 9)

headers2 = ["Month", "Followers Gained", "Total Followers", "Engagement Rate",
            "Reach", "Impressions", "Website Clicks", "Top Post", "Revenue from Social"]
for col, h in enumerate(headers2, 1):
    ws2.cell(row=3, column=col, value=h)
style_header_row(ws2, 3, 9, fill=header_fill_purple)
ws2.row_dimensions[3].height = 30

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
sample_followers = [450, 520, 380, 610, 720, 550, 490, 680, 750, 820, 900, 1100]
sample_total = [5450, 5970, 6350, 6960, 7680, 8230, 8720, 9400, 10150, 10970, 11870, 12970]
sample_engagement = [3.2, 3.5, 2.8, 4.1, 4.5, 3.9, 3.6, 4.2, 4.8, 5.1, 5.4, 5.8]
sample_reach = [12500, 14200, 11800, 18500, 22000, 19500, 17800, 21000, 25000, 28000, 31000, 35000]
sample_impressions = [35000, 42000, 33000, 52000, 61000, 55000, 49000, 59000, 72000, 80000, 89000, 98000]
sample_clicks = [180, 210, 165, 290, 340, 310, 275, 350, 420, 480, 530, 610]
sample_revenue = [150, 200, 125, 350, 480, 390, 320, 450, 580, 680, 750, 920]

for i, m in enumerate(months):
    r = 4 + i
    ws2.cell(row=r, column=1, value=m)
    ws2.cell(row=r, column=2, value=sample_followers[i])
    ws2.cell(row=r, column=3, value=sample_total[i])
    c = ws2.cell(row=r, column=4, value=sample_engagement[i] / 100)
    c.number_format = "0.0%"
    ws2.cell(row=r, column=5, value=sample_reach[i])
    ws2.cell(row=r, column=6, value=sample_impressions[i])
    ws2.cell(row=r, column=7, value=sample_clicks[i])
    ws2.cell(row=r, column=8, value="")
    c2 = ws2.cell(row=r, column=9, value=sample_revenue[i])
    c2.number_format = "$#,##0.00"

style_data_rows(ws2, 4, 15, 9)

# Totals row
total_row = 16
ws2.cell(row=total_row, column=1, value="TOTAL / AVG")
ws2.cell(row=total_row, column=2, value=f"=SUM(B4:B15)")
ws2.cell(row=total_row, column=3, value=f"=B16")  # total is last month's total
ws2.cell(row=total_row, column=4, value=f"=AVERAGE(D4:D15)")
ws2.cell(row=total_row, column=4).number_format = "0.0%"
ws2.cell(row=total_row, column=5, value=f"=SUM(E4:E15)")
ws2.cell(row=total_row, column=6, value=f"=SUM(F4:F15)")
ws2.cell(row=total_row, column=7, value=f"=SUM(G4:G15)")
ws2.cell(row=total_row, column=8, value="—")
ws2.cell(row=total_row, column=9, value=f"=SUM(I4:I15)")
ws2.cell(row=total_row, column=9).number_format = "$#,##0.00"
style_header_row(ws2, total_row, 9, fill=header_fill_purple)

# Format number columns
for r in range(4, 16):
    for c in [2, 3, 5, 6, 7]:
        ws2.cell(row=r, column=c).number_format = "#,##0"

set_col_widths(ws2, {"A": 16, "B": 18, "C": 18, "D": 18, "E": 15, "F": 16, "G": 16, "H": 25, "I": 20})
ws2.freeze_panes = "A4"

# ═══════════ TAB 3: HASHTAG RESEARCH ═══════════
ws3 = wb.create_sheet("Hashtag Research")
ws3.sheet_properties.tabColor = "3182CE"

add_title_banner(ws3, "#️⃣ HASHTAG RESEARCH TRACKER", "Research • Categorize • Optimize • Rank", 6)

headers3 = ["Hashtag", "Category", "Popularity (Posts)", "Relevance Score (1-10)", "Performance Rating", "Notes"]
for col, h in enumerate(headers3, 1):
    ws3.cell(row=3, column=col, value=h)
style_header_row(ws3, 3, 6, fill=header_fill_blue)
ws3.row_dimensions[3].height = 30

# Pre-loaded hashtags
hashtags_data = [
    ("#socialmediamarketing", "General", "25M", 9, "High", "Core hashtag — use on every post"),
    ("#digitalmarketing", "General", "30M", 8, "High", "Broad reach, competitive"),
    ("#contentcreator", "Creator", "18M", 9, "High", "Great for behind-the-scenes"),
    ("#instagramgrowth", "Instagram", "5M", 10, "High", "Niche and relevant"),
    ("#tiktokmarketing", "TikTok", "2M", 9, "High", "Growing rapidly"),
    ("#reelsinstagram", "Instagram", "12M", 8, "Med", "Good for Reels content"),
    ("#pinterestmarketing", "Pinterest", "800K", 9, "High", "Low competition, high ROI"),
    ("#linkedintips", "LinkedIn", "3M", 7, "Med", "Professional audience"),
    ("#emailmarketing", "Email", "4M", 8, "Med", "Evergreen topic"),
    ("#smallbusinesstips", "Business", "10M", 9, "High", "Connects with target audience"),
    ("#marketingstrategy", "Strategy", "8M", 8, "High", "Authority building"),
    ("#socialmediatips", "General", "15M", 10, "High", "Educational content"),
    ("#brandawareness", "Branding", "3M", 7, "Med", "Good for case studies"),
    ("#influencermarketing", "Collab", "6M", 7, "Med", "Use for partnership posts"),
    ("#growthhacking", "Growth", "4M", 8, "High", "Trendy, tech audience"),
    ("#contentmarketing", "Content", "12M", 9, "High", "Evergreen"),
    ("#videomarketing", "Video", "5M", 8, "Med", "For video-specific posts"),
    ("#ugccreator", "Creator", "1M", 9, "High", "Hot niche in 2026"),
    ("#marketingagency", "Business", "3M", 6, "Low", "Niche B2B"),
    ("#seomarketing", "SEO", "2M", 7, "Med", "Cross-promote blog content"),
]

for i, (tag, cat, pop, rel, perf, note) in enumerate(hashtags_data):
    r = 4 + i
    ws3.cell(row=r, column=1, value=tag)
    ws3.cell(row=r, column=2, value=cat)
    ws3.cell(row=r, column=3, value=pop)
    ws3.cell(row=r, column=4, value=rel)
    ws3.cell(row=r, column=5, value=perf)
    ws3.cell(row=r, column=6, value=note)

style_data_rows(ws3, 4, 53, 6)

dv_perf = DataValidation(type="list", formula1='"High,Med,Low"', allow_blank=True)
ws3.add_data_validation(dv_perf)
dv_perf.add("E4:E53")

ws3.conditional_formatting.add("E4:E53",
    CellIsRule(operator="equal", formula=['"High"'], fill=PatternFill("solid", fgColor=MINT)))
ws3.conditional_formatting.add("E4:E53",
    CellIsRule(operator="equal", formula=['"Low"'], fill=PatternFill("solid", fgColor=CORAL)))

set_col_widths(ws3, {"A": 28, "B": 16, "C": 20, "D": 22, "E": 20, "F": 35})
ws3.freeze_panes = "A4"
ws3.auto_filter.ref = "A3:F53"

# ═══════════ TAB 4: BRAND COLLABORATIONS ═══════════
ws4 = wb.create_sheet("Brand Collaborations")
ws4.sheet_properties.tabColor = "FC8181"

add_title_banner(ws4, "🤝 BRAND COLLABORATIONS TRACKER", "Pitch • Negotiate • Deliver • Get Paid", 8)

headers4 = ["Brand Name", "Contact Person / Email", "Platform", "Deliverables",
            "Deadline", "Payment ($)", "Status", "Notes"]
for col, h in enumerate(headers4, 1):
    ws4.cell(row=3, column=col, value=h)
style_header_row(ws4, 3, 8, fill=PatternFill("solid", fgColor=CORAL))
ws4.row_dimensions[3].height = 30

# Sample data
collab_data = [
    ("GlowUp Skincare", "sarah@glowup.com", "Instagram", "3 Reels + 2 Stories", "Feb 15, 2026", 1500, "Confirmed", "UGC style content"),
    ("TechNova App", "partnerships@technova.io", "TikTok", "2 Videos", "Mar 01, 2026", 800, "Negotiating", "Tech audience focus"),
    ("Bloom Tea Co.", "collab@bloomtea.com", "Pinterest", "10 Pins + Blog Post", "Jan 30, 2026", 600, "Pitched", "Lifestyle/wellness angle"),
    ("FitLife Gym", "mark@fitlife.com", "YouTube", "1 Sponsored Video", "Apr 10, 2026", 2000, "Confirmed", "Fitness niche crossover"),
    ("EcoWear Fashion", "hello@ecowear.co", "Instagram", "5 Posts + Story Takeover", "Mar 20, 2026", 1200, "Pitched", "Sustainable fashion brand"),
]
for i, (brand, contact, plat, deliv, deadline, pay, status, notes) in enumerate(collab_data):
    r = 4 + i
    ws4.cell(row=r, column=1, value=brand)
    ws4.cell(row=r, column=2, value=contact)
    ws4.cell(row=r, column=3, value=plat)
    ws4.cell(row=r, column=4, value=deliv)
    ws4.cell(row=r, column=5, value=deadline)
    c = ws4.cell(row=r, column=6, value=pay)
    c.number_format = "$#,##0.00"
    ws4.cell(row=r, column=7, value=status)
    ws4.cell(row=r, column=8, value=notes)

style_data_rows(ws4, 4, 33, 8)

dv_collab_status = DataValidation(type="list", formula1='"Pitched,Negotiating,Confirmed,Completed,Paid"', allow_blank=True)
ws4.add_data_validation(dv_collab_status)
dv_collab_status.add("G4:G33")

dv_collab_plat = DataValidation(type="list", formula1='"Instagram,TikTok,YouTube,Pinterest,Facebook,Twitter,LinkedIn,Blog,Email"', allow_blank=True)
ws4.add_data_validation(dv_collab_plat)
dv_collab_plat.add("C4:C33")

ws4.conditional_formatting.add("G4:G33",
    CellIsRule(operator="equal", formula=['"Paid"'], fill=PatternFill("solid", fgColor=MINT)))
ws4.conditional_formatting.add("G4:G33",
    CellIsRule(operator="equal", formula=['"Confirmed"'], fill=PatternFill("solid", fgColor="B794F4")))

set_col_widths(ws4, {"A": 22, "B": 28, "C": 15, "D": 28, "E": 18, "F": 16, "G": 16, "H": 30})
ws4.freeze_panes = "A4"
ws4.auto_filter.ref = "A3:H33"

# ═══════════ TAB 5: CONTENT IDEAS BANK ═══════════
ws5 = wb.create_sheet("Content Ideas Bank")
ws5.sheet_properties.tabColor = "68D391"

add_title_banner(ws5, "💡 CONTENT IDEAS BANK", "Never Run Out of Content — 25 Ideas Pre-Loaded!", 6)

headers5 = ["Content Idea", "Best Platform", "Content Type", "Priority", "Used? (Y/N)", "Performance Notes"]
for col, h in enumerate(headers5, 1):
    ws5.cell(row=3, column=col, value=h)
style_header_row(ws5, 3, 6, fill=PatternFill("solid", fgColor=MINT))
ws5.row_dimensions[3].height = 30

ideas = [
    ("Day in the life of a social media manager", "TikTok", "Video", "High", "", ""),
    ("Before & after: brand transformation case study", "Instagram", "Carousel", "High", "", ""),
    ("5 tools every marketer needs in 2026", "LinkedIn", "Carousel", "High", "", ""),
    ("Monthly analytics review — transparent share", "Instagram", "Reel", "Medium", "", ""),
    ("Trending audio + niche tip overlay", "TikTok", "Reel", "High", "", ""),
    ("Client testimonial spotlight", "Instagram", "Story", "Medium", "", ""),
    ("Tutorial: How to schedule a week of content in 1 hour", "YouTube", "Video", "High", "", ""),
    ("Myth vs. Fact: Social media edition", "TikTok", "Video", "Medium", "", ""),
    ("Top 10 hashtag strategy for your niche", "Blog", "Blog", "High", "", ""),
    ("Q&A — answer audience DMs publicly", "Instagram", "Story", "Low", "", ""),
    ("Pin design: Step-by-step infographic", "Pinterest", "Photo", "Medium", "", ""),
    ("Newsletter: Weekly marketing digest", "Email", "Newsletter", "High", "", ""),
    ("Podcast clip: Marketing hot takes", "TikTok", "Reel", "Medium", "", ""),
    ("Algorithm update breakdown", "LinkedIn", "Carousel", "High", "", ""),
    ("Collab post with another creator", "Instagram", "Carousel", "High", "", ""),
    ("Repurpose blog post into 5 social posts", "Pinterest", "Photo", "Medium", "", ""),
    ("Share your workspace / desk setup", "TikTok", "Video", "Low", "", ""),
    ("Holiday marketing campaign ideas", "Blog", "Blog", "High", "", ""),
    ("Comparison: Instagram Reels vs TikTok in 2026", "YouTube", "Video", "High", "", ""),
    ("Share your monthly content calendar (template)", "Instagram", "Carousel", "High", "", ""),
    ("A/B test results reveal", "LinkedIn", "Carousel", "Medium", "", ""),
    ("User-generated content compilation", "Instagram", "Reel", "Medium", "", ""),
    ("Morning routine for productivity", "TikTok", "Video", "Low", "", ""),
    ("Year-in-review: Growth milestones", "Instagram", "Carousel", "High", "", ""),
    ("Beginner's guide to Pinterest marketing", "Pinterest", "Photo", "High", "", ""),
]
for i, (idea, plat, ctype, prio, used, perf) in enumerate(ideas):
    r = 4 + i
    ws5.cell(row=r, column=1, value=idea)
    ws5.cell(row=r, column=2, value=plat)
    ws5.cell(row=r, column=3, value=ctype)
    ws5.cell(row=r, column=4, value=prio)
    ws5.cell(row=r, column=5, value=used)
    ws5.cell(row=r, column=6, value=perf)

style_data_rows(ws5, 4, 53, 6)

dv_priority = DataValidation(type="list", formula1='"High,Medium,Low"', allow_blank=True)
ws5.add_data_validation(dv_priority)
dv_priority.add("D4:D53")

dv_used = DataValidation(type="list", formula1='"Y,N"', allow_blank=True)
ws5.add_data_validation(dv_used)
dv_used.add("E4:E53")

dv_idea_plat = DataValidation(type="list", formula1='"Instagram,TikTok,YouTube,Pinterest,Facebook,Twitter,LinkedIn,Blog,Email"', allow_blank=True)
ws5.add_data_validation(dv_idea_plat)
dv_idea_plat.add("B4:B53")

dv_idea_type = DataValidation(type="list", formula1='"Photo,Video,Carousel,Reel,Story,Blog,Newsletter"', allow_blank=True)
ws5.add_data_validation(dv_idea_type)
dv_idea_type.add("C4:C53")

ws5.conditional_formatting.add("D4:D53",
    CellIsRule(operator="equal", formula=['"High"'], fill=PatternFill("solid", fgColor=CORAL)))
ws5.conditional_formatting.add("D4:D53",
    CellIsRule(operator="equal", formula=['"Medium"'], fill=PatternFill("solid", fgColor=PALE_PINK)))

set_col_widths(ws5, {"A": 48, "B": 16, "C": 16, "D": 14, "E": 14, "F": 30})
ws5.freeze_panes = "A4"

# ═══════════ TAB 6: AUDIENCE INSIGHTS ═══════════
ws6 = wb.create_sheet("Audience Insights")
ws6.sheet_properties.tabColor = "D53F8C"

add_title_banner(ws6, "👥 AUDIENCE INSIGHTS BY PLATFORM", "Know Your Audience • Post at the Right Time • Grow Faster", 7)

headers6 = ["Platform", "Total Followers", "Monthly Growth Rate", "Top Demographics",
            "Best Post Time", "Best Day", "Avg Engagement Rate"]
for col, h in enumerate(headers6, 1):
    ws6.cell(row=3, column=col, value=h)
style_header_row(ws6, 3, 7)
ws6.row_dimensions[3].height = 30

audience_data = [
    ("Instagram", 8500, "4.2%", "Women 25-34 (42%)", "11:00 AM & 7:00 PM", "Wednesday", "4.8%"),
    ("TikTok", 12000, "8.5%", "Women 18-24 (38%)", "9:00 AM & 8:00 PM", "Tuesday", "6.2%"),
    ("YouTube", 3200, "2.8%", "Mixed 25-44 (55%)", "2:00 PM", "Saturday", "3.1%"),
    ("Pinterest", 5800, "5.1%", "Women 25-44 (65%)", "8:00 PM", "Sunday", "2.5%"),
    ("Facebook", 4100, "1.5%", "Women 35-54 (40%)", "1:00 PM", "Thursday", "2.1%"),
    ("Twitter", 2900, "3.2%", "Mixed 25-34 (35%)", "12:00 PM & 5:00 PM", "Monday", "1.8%"),
    ("LinkedIn", 6200, "3.8%", "Professionals 30-45 (50%)", "8:00 AM & 12:00 PM", "Tuesday", "3.5%"),
]
for i, (plat, followers, growth, demo, time, day, eng) in enumerate(audience_data):
    r = 4 + i
    ws6.cell(row=r, column=1, value=plat)
    ws6.cell(row=r, column=2, value=followers)
    ws6.cell(row=r, column=2).number_format = "#,##0"
    ws6.cell(row=r, column=3, value=growth)
    ws6.cell(row=r, column=4, value=demo)
    ws6.cell(row=r, column=5, value=time)
    ws6.cell(row=r, column=6, value=day)
    ws6.cell(row=r, column=7, value=eng)

style_data_rows(ws6, 4, 12, 7)

# Extra blank rows for more platforms
for r in range(11, 13):
    for c in range(1, 8):
        ws6.cell(row=r, column=c).border = thin_border

set_col_widths(ws6, {"A": 18, "B": 18, "C": 20, "D": 28, "E": 24, "F": 16, "G": 22})
ws6.freeze_panes = "A4"

# ═══════════ TAB 7: REVENUE TRACKER ═══════════
ws7 = wb.create_sheet("Revenue Tracker")
ws7.sheet_properties.tabColor = "6B46C1"

add_title_banner(ws7, "💰 SOCIAL MEDIA REVENUE TRACKER", "Track Every Dollar • Sponsorships • Affiliates • Products", 5)

headers7 = ["Date", "Revenue Source", "Brand / Description", "Amount ($)", "Payment Status"]
for col, h in enumerate(headers7, 1):
    ws7.cell(row=3, column=col, value=h)
style_header_row(ws7, 3, 5, fill=header_fill_purple)
ws7.row_dimensions[3].height = 30

revenue_data = [
    ("Jan 05, 2026", "Sponsorship", "GlowUp Skincare — 3 Reels", 1500, "Paid"),
    ("Jan 12, 2026", "Affiliate", "Amazon Associates — January", 245, "Paid"),
    ("Jan 20, 2026", "Product", "Social Media Template Pack Sale", 890, "Paid"),
    ("Feb 01, 2026", "Sponsorship", "TechNova App — 2 TikToks", 800, "Pending"),
    ("Feb 10, 2026", "Coaching", "1:1 Social Media Audit Session", 350, "Paid"),
    ("Feb 15, 2026", "Ad Revenue", "YouTube AdSense — February", 180, "Pending"),
    ("Mar 01, 2026", "Affiliate", "ConvertKit Affiliate Commission", 120, "Invoiced"),
    ("Mar 10, 2026", "Product", "Instagram Growth Guide eBook", 560, "Paid"),
    ("Mar 20, 2026", "Sponsorship", "EcoWear Fashion — IG Campaign", 1200, "Invoiced"),
    ("Apr 01, 2026", "Other", "Speaking Fee — Marketing Summit", 2000, "Confirmed"),
]
for i, (date, source, brand, amount, status) in enumerate(revenue_data):
    r = 4 + i
    ws7.cell(row=r, column=1, value=date)
    ws7.cell(row=r, column=2, value=source)
    ws7.cell(row=r, column=3, value=brand)
    c = ws7.cell(row=r, column=4, value=amount)
    c.number_format = "$#,##0.00"
    ws7.cell(row=r, column=5, value=status)

style_data_rows(ws7, 4, 53, 5)

# Auto-total row
total_r = 54
ws7.cell(row=total_r, column=1, value="")
ws7.cell(row=total_r, column=2, value="")
ws7.cell(row=total_r, column=3, value="TOTAL REVENUE")
ws7.cell(row=total_r, column=4, value="=SUM(D4:D53)")
ws7.cell(row=total_r, column=4).number_format = "$#,##0.00"
ws7.cell(row=total_r, column=5, value="")
style_header_row(ws7, total_r, 5, fill=header_fill_purple)

dv_source = DataValidation(type="list", formula1='"Sponsorship,Affiliate,Product,Ad Revenue,Coaching,Other"', allow_blank=True)
ws7.add_data_validation(dv_source)
dv_source.add("B4:B53")

dv_pay_status = DataValidation(type="list", formula1='"Pending,Invoiced,Confirmed,Paid,Overdue"', allow_blank=True)
ws7.add_data_validation(dv_pay_status)
dv_pay_status.add("E4:E53")

ws7.conditional_formatting.add("E4:E53",
    CellIsRule(operator="equal", formula=['"Paid"'], fill=PatternFill("solid", fgColor=MINT)))
ws7.conditional_formatting.add("E4:E53",
    CellIsRule(operator="equal", formula=['"Overdue"'], fill=PatternFill("solid", fgColor=CORAL)))

set_col_widths(ws7, {"A": 18, "B": 20, "C": 38, "D": 18, "E": 18})
ws7.freeze_panes = "A4"
ws7.auto_filter.ref = "A3:E53"

# ═══════════ TAB 8: HOW TO USE ═══════════
ws8 = wb.create_sheet("How to Use")
ws8.sheet_properties.tabColor = "FED7E2"

# Title
ws8.merge_cells("A1:F1")
c1 = ws8.cell(row=1, column=1, value="✨ HOW TO USE YOUR SOCIAL MEDIA MARKETING PLANNER 2026 ✨")
c1.font = Font(name="Calibri", bold=True, color=WHITE, size=20)
c1.fill = PatternFill("solid", fgColor=HOT_PINK)
c1.alignment = center_align
ws8.row_dimensions[1].height = 55

ws8.merge_cells("A2:F2")
c2 = ws8.cell(row=2, column=1, value="Your complete guide to planning, tracking, and growing your social media presence")
c2.font = Font(name="Calibri", italic=True, color=PURPLE, size=13)
c2.fill = pale_pink_fill
c2.alignment = center_align
ws8.row_dimensions[2].height = 35

# Instructions
instructions = [
    ("", ""),
    ("📋 GETTING STARTED", ""),
    ("Step 1:", "Open the Content Calendar tab and start filling in your posting schedule for 2026. Dates are pre-filled for the first 100 days!"),
    ("Step 2:", "Use the dropdown menus to select Platform, Content Type, and Status for each post."),
    ("Step 3:", "Track engagement numbers after each post goes live to identify what works best."),
    ("Step 4:", "Update the Analytics Dashboard monthly to see your growth trajectory."),
    ("", ""),
    ("📊 TAB OVERVIEW", ""),
    ("Content Calendar:", "Your daily posting schedule with auto-calculated days, platform dropdowns, and status tracking."),
    ("Analytics Dashboard:", "Monthly metrics tracker with auto-calculated totals and averages for the full year."),
    ("Hashtag Research:", "Track and rate your best-performing hashtags. Performance ratings auto-highlight in green/red."),
    ("Brand Collaborations:", "Manage sponsorships from pitch to payment. Never miss a deadline or invoice."),
    ("Content Ideas Bank:", "25 pre-loaded content ideas plus space for 25 more. Never run out of things to post!"),
    ("Audience Insights:", "Track demographics and best posting times for each platform you're active on."),
    ("Revenue Tracker:", "Log every dollar earned from social media — sponsorships, affiliates, products, and more."),
    ("", ""),
    ("💡 PRO TIPS", ""),
    ("Tip 1:", "Batch your content! Plan 2-4 weeks ahead using the Content Calendar for maximum consistency."),
    ("Tip 2:", "Review your Analytics Dashboard on the 1st of every month to spot trends and adjust strategy."),
    ("Tip 3:", "Rotate hashtags every 2 weeks to avoid shadowbanning — use the Hashtag Research tab to track sets."),
    ("Tip 4:", "Use the Content Ideas Bank when you feel stuck. Mark ideas as 'Used' so you don't repeat."),
    ("Tip 5:", "Always follow up on brand collaborations — move them through every status stage!"),
    ("", ""),
    ("🎯 20 BONUS CONTENT IDEAS FOR 2026", ""),
    ("1.", "Create a '2026 Goals' post and ask your audience to share theirs"),
    ("2.", "Film a 'What I Post in a Week' behind-the-scenes series"),
    ("3.", "Design a free downloadable checklist related to your niche"),
    ("4.", "Host an Instagram Live Q&A about your industry"),
    ("5.", "Share your top 3 tools for productivity (with affiliate links!)"),
    ("6.", "Post a 'This or That' poll in Stories for quick engagement"),
    ("7.", "Create a Pinterest board for your 2026 content aesthetic"),
    ("8.", "Write a LinkedIn article about a lesson learned this year"),
    ("9.", "Film a Reel showing your content creation process"),
    ("10.", "Share a carousel of your best-performing posts from last month"),
    ("11.", "Do a 'Myth vs. Reality' post about your industry"),
    ("12.", "Create a TikTok trending audio with educational overlay text"),
    ("13.", "Design an infographic for Pinterest (these get saved and shared!)"),
    ("14.", "Start a weekly newsletter recapping your best content"),
    ("15.", "Post a client/customer testimonial with their permission"),
    ("16.", "Share your morning routine or workspace setup"),
    ("17.", "Create a comparison post (e.g., Reels vs. TikTok results)"),
    ("18.", "Host a giveaway to boost follower count and engagement"),
    ("19.", "Repurpose one blog post into 10 different social media posts"),
    ("20.", "End each month with a 'Monthly Wins' celebration post"),
    ("", ""),
    ("❤️ THANK YOU!", "Thank you for purchasing this planner! If you love it, please leave a 5-star review on Etsy."),
    ("", "Questions? Reach out through Etsy messages — we're happy to help!"),
]

for i, (left, right) in enumerate(instructions):
    r = 3 + i
    cell_a = ws8.cell(row=r, column=1, value=left)
    ws8.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    cell_b = ws8.cell(row=r, column=2, value=right)

    if left and not left.startswith("Step") and not left.startswith("Tip") and not left[0].isdigit() and ":" not in left:
        # Section headers
        cell_a.font = Font(name="Calibri", bold=True, color=HOT_PINK, size=14)
        cell_a.fill = pale_pink_fill
        cell_b.fill = pale_pink_fill
        ws8.row_dimensions[r].height = 30
    elif left.startswith(("Step", "Tip", "Content", "Analytics", "Hashtag", "Brand", "Audience", "Revenue")):
        cell_a.font = Font(name="Calibri", bold=True, color=PURPLE, size=11)
        cell_b.font = body_font
        cell_b.alignment = wrap_align
        ws8.row_dimensions[r].height = 28
    elif left and left[0].isdigit():
        cell_a.font = Font(name="Calibri", bold=True, color=ELECTRIC_BLUE, size=11)
        cell_b.font = body_font
        cell_b.alignment = wrap_align
    elif "THANK" in left:
        cell_a.font = Font(name="Calibri", bold=True, color=HOT_PINK, size=14)
        cell_b.font = Font(name="Calibri", bold=True, color=DARK_TEXT, size=11)
    else:
        cell_a.font = body_font
        cell_b.font = body_font
        cell_b.alignment = wrap_align

set_col_widths(ws8, {"A": 22, "B": 20, "C": 20, "D": 20, "E": 20, "F": 20})

# ═══════════ SAVE ═══════════
output = "/home/user/claude-code/etsy-digital-download-6/product/Social_Media_Marketing_Planner_2026.xlsx"
wb.save(output)
print(f"Spreadsheet saved: {output}")
print(f"Sheets: {wb.sheetnames}")
