"""
Life OS v2 Configuration Settings
"""

# Google Sheets API Configuration
CREDENTIALS_FILE = "config/credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Spreadsheet Settings
SPREADSHEET_NAME = "Life OS v2"

# Tab Names and Order (54 tabs)
TABS = [
    # Financial Dashboard (1-11)
    {"name": "📋 Dashboard", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "📊 Transactions", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "💳 Credit Cards", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "📊 Budget Master", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "📈 Spending by Category", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "💰 Monthly Summary", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "📊 Spending by Merchant", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "✅ Master Tasks", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "🎁 Gift Tracker", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "🩺 Health Dashboard", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "📅 Calendar View", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},

    # Job Search System (12-18)
    {"name": "💼 Job Pipeline", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "💼 Applications Tracker", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "💼 Recruiter CRM", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "💼 Interview Tracker", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "💼 Follow-Ups", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "💼 Offer Comparison", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "💼 Job Search Dashboard", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},

    # Goals System (19-22)
    {"name": "🎯 Michelle's Goals", "color": {"red": 0.95, "green": 0.76, "blue": 0.20}},
    {"name": "🎯 Gray's Goals", "color": {"red": 0.95, "green": 0.76, "blue": 0.20}},
    {"name": "🎯 Shared Goals", "color": {"red": 0.95, "green": 0.76, "blue": 0.20}},
    {"name": "🎯 Goal Dashboard", "color": {"red": 0.95, "green": 0.76, "blue": 0.20}},

    # Household System (23-25)
    {"name": "🏠 Recurring Tasks", "color": {"red": 0.61, "green": 0.35, "blue": 0.71}},
    {"name": "🏠 One-Time Projects", "color": {"red": 0.61, "green": 0.35, "blue": 0.71}},
    {"name": "🏠 Load Dashboard", "color": {"red": 0.61, "green": 0.35, "blue": 0.71}},

    # Shelzy's Designs Business (26-34)
    {"name": "📊 Shelzy's Transactions", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Revenue Tracker", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Product Catalog", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Expenses", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Monthly P&L", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Customer Metrics", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Inventory", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Marketing", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "📊 Shelzy's Dashboard", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},

    # Fertility & Health (35-40)
    {"name": "🌸 Cycle Tracking", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},
    {"name": "🌸 Daily Log", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},
    {"name": "🌸 DPO Tracker", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},
    {"name": "🌸 Appointments", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},
    {"name": "🌸 Supplements", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},
    {"name": "🌸 Monthly Summary", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},

    # Executive Dashboards (41-46)
    {"name": "📈 Weekly Life Summary", "color": {"red": 0.20, "green": 0.20, "blue": 0.20}},
    {"name": "📈 Job Search Status", "color": {"red": 0.20, "green": 0.20, "blue": 0.20}},
    {"name": "📈 Financial Health", "color": {"red": 0.20, "green": 0.20, "blue": 0.20}},
    {"name": "📈 Goal Progress", "color": {"red": 0.20, "green": 0.20, "blue": 0.20}},
    {"name": "📈 Household Load", "color": {"red": 0.20, "green": 0.20, "blue": 0.20}},
    {"name": "📈 Business Performance", "color": {"red": 0.20, "green": 0.20, "blue": 0.20}},

    # Oura Ring Integration (47-54)
    {"name": "🔴 Oura Sleep Tracker", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Activity Tracker", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Readiness Tracker", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Cycle Integration", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Temperature", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Heart Rate", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Stress Tracker", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
    {"name": "🔴 Oura Health Dashboard", "color": {"red": 0.86, "green": 0.27, "blue": 0.22}},
]

# Formatting Constants
COLORS = {
    "header_bg": {"red": 0.26, "green": 0.52, "blue": 0.96},  # #4285F4
    "header_text": {"red": 1.0, "green": 1.0, "blue": 1.0},    # White
    "positive": {"red": 0.06, "green": 0.62, "blue": 0.35},    # #0F9D58 Green
    "negative": {"red": 0.86, "green": 0.27, "blue": 0.22},    # #DB4437 Red
    "warning": {"red": 0.99, "green": 0.67, "blue": 0.24},     # #FDAB3D Orange
    "completed": {"red": 0.60, "green": 0.63, "blue": 0.65},   # #9AA0A6 Gray
    "over_budget_bg": {"red": 0.96, "green": 0.78, "blue": 0.76},  # #F4C7C3
    "under_budget_bg": {"red": 0.72, "green": 0.88, "blue": 0.80}, # #B7E1CD
    "follicular": {"red": 0.85, "green": 0.93, "blue": 1.0},   # Light blue
    "luteal": {"red": 1.0, "green": 0.90, "blue": 0.95},       # Light pink
}

# Number Formats
NUMBER_FORMATS = {
    "currency": "$#,##0.00",
    "percentage": "0.0%",
    "date": "MM/DD/YYYY",
    "whole_number": "#,##0",
    "decimal": "#,##0.00",
}

# Data Validation Options
VALIDATION = {
    "priority": ["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"],
    "status": ["Not Started", "In Progress", "Blocked", "Completed"],
    "job_stage": ["Researching", "Applied", "Phone Screen", "Interview", "Final Round", "Offer", "Rejected", "Withdrawn"],
    "location_type": ["Remote", "Hybrid", "On-site"],
    "goal_status": ["Not Started", "In Progress", "On Track", "At Risk", "Blocked", "Completed"],
    "goal_category": ["Career", "Health", "Finance", "Personal", "Business", "Family"],
    "task_owner": ["Michelle", "Gray", "Both"],
    "frequency": ["Daily", "Weekly", "Biweekly", "Monthly", "Quarterly", "Annually"],
    "cervical_mucus": ["Dry", "Sticky", "Creamy", "EWCM", "Watery"],
    "cycle_phase": ["Follicular", "Luteal", "Ovulation", "Menstrual"],
    "appointment_type": ["OB/GYN", "Fertility Specialist", "Primary Care", "Lab", "Other"],
    "sales_channel": ["Shopify", "Amazon", "Direct", "Other"],
    "customer_type": ["New", "Returning"],
    "marketing_channel": ["Facebook Ads", "Instagram", "Google", "Email", "Influencer", "Other"],
    "interview_type": ["Phone Screen", "Video", "In-person", "Panel", "Technical", "Case Study"],
    "follow_up_type": ["Thank You", "Status Check", "Additional Info", "Withdrawal"],
    "recruiter_type": ["Internal Recruiter", "Agency Recruiter", "Hiring Manager", "Referral", "Networking"],
}

# Pre-populated Data
GIFT_RECIPIENTS = [
    {"name": "Gray Perkins", "birthday": "10/11", "address": "East Hampton, NY", "notes": "Husband"},
    {"name": "Kathleen", "birthday": "", "address": "", "notes": "Sister"},
    {"name": "Sapna", "birthday": "", "address": "", "notes": "Friend"},
    {"name": "Danielle", "birthday": "", "address": "", "notes": "Friend"},
    {"name": "Lila Marie", "birthday": "1/2", "address": "110 Charlton Apt 7A NYC 10014", "notes": ""},
    {"name": "Katie Martell", "birthday": "", "address": "", "notes": "Friend"},
]

SUPPLEMENTS = [
    {"name": "Prenatal Vitamin", "dosage": "1 tablet", "frequency": "Daily", "started": "1/1/2026", "purpose": "Pregnancy prep", "prescribed_by": "Dr. Smith", "status": "Active"},
    {"name": "Folic Acid", "dosage": "400mcg", "frequency": "Daily", "started": "1/1/2026", "purpose": "Neural tube development", "prescribed_by": "Dr. Smith", "status": "Active"},
    {"name": "CoQ10", "dosage": "200mg", "frequency": "Daily", "started": "1/1/2026", "purpose": "Egg quality", "prescribed_by": "", "status": "Active"},
]

RECURRING_TASKS = [
    {"task": "Grocery shopping", "owner": "Michelle", "frequency": "Weekly", "time_estimate": 90, "category": "Household"},
    {"task": "Trash/recycling", "owner": "Gray", "frequency": "Weekly", "time_estimate": 15, "category": "Household"},
    {"task": "Laundry", "owner": "Both", "frequency": "Biweekly", "time_estimate": 120, "category": "Household"},
    {"task": "Pay bills", "owner": "Michelle", "frequency": "Monthly", "time_estimate": 30, "category": "Finance"},
    {"task": "Yard work", "owner": "Gray", "frequency": "Weekly", "time_estimate": 120, "category": "Outdoor"},
]

MICHELLE_GOALS = [
    {"goal": "Secure $120K+ role", "category": "Career", "target": "6/30/2026", "progress": 25, "status": "In Progress"},
    {"goal": "Build $25K emergency fund", "category": "Finance", "target": "12/31/2026", "progress": 74, "current_value": 18500, "target_value": 25000, "status": "On Track"},
    {"goal": "Prepare for pregnancy", "category": "Health", "target": "12/31/2026", "progress": 50, "status": "In Progress"},
    {"goal": "Grow Shelzy's to $10K/month", "category": "Business", "target": "12/31/2026", "progress": 72, "current_value": 7200, "target_value": 10000, "status": "On Track"},
]

GRAY_GOALS = [
    {"goal": "Advance career at Addepar", "category": "Career", "target": "12/31/2026", "progress": 50, "status": "In Progress"},
    {"goal": "Increase investment portfolio", "category": "Finance", "target": "12/31/2026", "progress": 40, "status": "In Progress"},
    {"goal": "Complete home gym setup", "category": "Health", "target": "6/30/2026", "progress": 30, "status": "In Progress"},
]

SHARED_GOALS = [
    {"goal": "Joint emergency fund $50K", "category": "Finance", "target": "12/31/2026", "progress": 70, "current_value": 35000, "target_value": 50000, "status": "On Track"},
    {"goal": "Home renovation", "category": "Home", "target": "12/31/2026", "progress": 40, "status": "At Risk"},
    {"goal": "Plan for family expansion", "category": "Family", "target": "12/31/2026", "progress": 50, "status": "In Progress"},
]

# Column Widths (in pixels)
DEFAULT_COLUMN_WIDTH = 100
COLUMN_WIDTHS = {
    "narrow": 60,
    "small": 80,
    "medium": 120,
    "wide": 180,
    "extra_wide": 250,
}
