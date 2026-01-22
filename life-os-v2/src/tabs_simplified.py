"""
Life OS v2 - Simplified 8-Tab Version

Tab 1: Dashboard (Master Overview)
Tab 2: Transactions (Financial Data)
Tab 3: Budget & Spending
Tab 4: Job Search
Tab 5: Goals
Tab 6: Household & Tasks
Tab 7: Shelzy's Business
Tab 8: Health & Fertility
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    COLORS, VALIDATION, GIFT_RECIPIENTS, SUPPLEMENTS,
    RECURRING_TASKS, MICHELLE_GOALS, GRAY_GOALS, SHARED_GOALS
)


class SimplifiedTabBuilder:
    """Build simplified 8-tab Life OS system"""

    def __init__(self, service=None, spreadsheet_id=None):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self, transaction_data=None, oura_data=None):
        """Build all 8 tabs"""
        results = {}

        results['dashboard'] = self.build_dashboard_tab()
        results['transactions'] = self.build_transactions_tab(transaction_data)
        results['budget'] = self.build_budget_spending_tab()
        results['job_search'] = self.build_job_search_tab()
        results['goals'] = self.build_goals_tab()
        results['household'] = self.build_household_tab()
        results['shelzys'] = self.build_shelzys_tab()
        results['health'] = self.build_health_tab(oura_data)

        return results

    def build_dashboard_tab(self):
        """Tab 1: Master Dashboard - Overview of everything"""
        headers = ['LIFE OS v2 DASHBOARD', '', '', '', '', '']

        data = [
            ['', '', '', '', '', ''],
            ['═══ FINANCIAL OVERVIEW ═══', '', '', '═══ JOB SEARCH ═══', '', ''],
            ['Monthly Income', '=SUMIF(Transactions!G:G,">0")', '', 'Active Applications', '=COUNTIF(\'Job Search\'!F:F,"Active")', ''],
            ['Monthly Expenses', '=ABS(SUMIF(Transactions!G:G,"<0"))', '', 'Interviews Scheduled', '=COUNTIF(\'Job Search\'!E:E,"Interview")', ''],
            ['Net Cash Flow', '=B3-B4', '', 'Offers', '=COUNTIF(\'Job Search\'!E:E,"Offer")', ''],
            ['Savings Rate', '=IFERROR(B5/B3,0)', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['═══ GOALS PROGRESS ═══', '', '', '═══ HOUSEHOLD ═══', '', ''],
            ['Michelle On Track', '=COUNTIF(Goals!D:D,"On Track")', '', 'Tasks Overdue', '=COUNTIF(\'Household\'!G:G,"Overdue")', ''],
            ['Gray On Track', '=COUNTIF(Goals!D:D,"On Track")', '', 'Tasks Due Soon', '=COUNTIF(\'Household\'!G:G,"Due Soon")', ''],
            ['Shared On Track', '=COUNTIF(Goals!D:D,"On Track")', '', 'Load Balance', 'See Household tab', ''],
            ['', '', '', '', '', ''],
            ['═══ SHELZY\'S DESIGNS ═══', '', '', '═══ HEALTH STATUS ═══', '', ''],
            ['MTD Revenue', '=SUMIF(\'Shelzy\'\'s Business\'!C:C,"Revenue",\'Shelzy\'\'s Business\'!E:E)', '', 'Sleep Score', '=Health!B3', ''],
            ['MTD Expenses', '=ABS(SUMIF(\'Shelzy\'\'s Business\'!C:C,"<>Revenue",\'Shelzy\'\'s Business\'!E:E))', '', 'Readiness', '=Health!B4', ''],
            ['MTD Profit', '=B14-B15', '', 'Activity', '=Health!B5', ''],
            ['Profit Margin', '=IFERROR(B16/B14,0)', '', 'Cycle Day', '=Health!B6', ''],
        ]

        return {
            'tab_name': 'Dashboard',
            'headers': headers,
            'data': data,
            'column_widths': [180, 130, 50, 180, 130, 50],
            'freeze_rows': 1,
            'formatting': {'currency_cols': [1, 4]}
        }

    def build_transactions_tab(self, transaction_data=None):
        """Tab 2: All Transactions"""
        headers = ['Date', 'Merchant', 'Category', 'Account', 'Original Statement',
                   'Notes', 'Amount', 'Tags', 'Owner']

        if transaction_data is None:
            from src.data_processors.transactions import TransactionProcessor
            transaction_data = TransactionProcessor.generate_sample_data()

        return {
            'tab_name': 'Transactions',
            'headers': headers,
            'data': transaction_data,
            'column_widths': [100, 180, 150, 200, 250, 150, 100, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'currency_col': 6,
            }
        }

    def build_budget_spending_tab(self):
        """Tab 3: Budget & Spending Analysis"""
        headers = ['BUDGET & SPENDING', '', '', '', '', '', '']

        categories = [
            'Groceries', 'Restaurants', 'Shopping', 'Gas', 'Utilities',
            'Rent/Mortgage', 'Insurance', 'Healthcare', 'Entertainment', 'Travel',
            'Subscriptions', 'Car', 'Phone', 'Internet', 'Personal Care'
        ]

        data = [
            ['', '', '', '', '', '', ''],
            ['═══ MONTHLY BUDGET ═══', '', '', '', '', '', ''],
            ['Category', 'Budget', 'Actual', 'Remaining', '% Used', 'Last Month', 'Status'],
        ]

        for i, cat in enumerate(categories):
            row_num = i + 4
            data.append([
                cat,
                '',  # Budget - manual entry
                f'=ABS(SUMIF(Transactions!C:C,A{row_num},Transactions!G:G))',
                f'=B{row_num}-C{row_num}',
                f'=IFERROR(C{row_num}/B{row_num},0)',
                '',
                f'=IF(E{row_num}<0.75,"✅",IF(E{row_num}<0.9,"⚠️",IF(E{row_num}<=1,"🔶","🔴")))'
            ])

        # Add monthly summary section
        data.extend([
            ['', '', '', '', '', '', ''],
            ['═══ MONTHLY SUMMARY (Last 12 Months) ═══', '', '', '', '', '', ''],
            ['Month', 'Income', 'Expenses', 'Net', 'Savings Rate', 'Transactions', ''],
        ])

        for i in range(12):
            row_num = len(data) + 1
            data.append([
                f'Month -{i}',
                '',  # Will show formulas in real version
                '',
                '',
                '',
                '',
                ''
            ])

        return {
            'tab_name': 'Budget & Spending',
            'headers': headers,
            'data': data,
            'column_widths': [150, 100, 100, 100, 80, 100, 80],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [1, 2, 3, 5],
                'percentage_col': 4,
            }
        }

    def build_job_search_tab(self):
        """Tab 4: Job Search (Pipeline + Applications + Interviews)"""
        headers = ['JOB SEARCH TRACKER', '', '', '', '', '', '', '', '']

        data = [
            ['', '', '', '', '', '', '', '', ''],
            ['═══ PIPELINE ═══', '', '', '', '', '', '', '', ''],
            ['Company', 'Role', 'Location', 'Salary Range', 'Stage', 'Status', 'Next Action', 'Due Date', 'Notes'],
            ['Anthropic', 'Senior PM', 'SF (Remote)', '$150K-$180K', 'Applied', 'Active', 'Follow up', '', ''],
            ['Stripe', 'Product Lead', 'NYC (Hybrid)', '$160K-$200K', 'Interview', 'Active', 'Prep for round 2', '', ''],
            ['Notion', 'Group PM', 'Remote', '$140K-$170K', 'Final Round', 'Active', 'Case study prep', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['═══ INTERVIEWS ═══', '', '', '', '', '', '', '', ''],
            ['Date', 'Company', 'Type', 'Interviewer', 'Prep Done', 'Thank You Sent', 'Feeling (1-10)', 'Follow-up', 'Notes'],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['═══ RECRUITERS ═══', '', '', '', '', '', '', '', ''],
            ['Name', 'Company', 'Type', 'Email', 'Phone', 'Last Contact', 'Next Follow-up', 'Opportunities', 'Notes'],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', ''],
            ['═══ METRICS ═══', '', '', '', '', '', '', '', ''],
            ['Total Applications', '=COUNTA(A4:A11)-COUNTBLANK(A4:A11)', '', 'Interview Rate', '=IFERROR(COUNTIF(E4:E11,"Interview")/B25,0)', '', '', '', ''],
            ['Active', '=COUNTIF(F4:F11,"Active")', '', 'Offer Rate', '=IFERROR(COUNTIF(E4:E11,"Offer")/B25,0)', '', '', '', ''],
        ]

        return {
            'tab_name': 'Job Search',
            'headers': headers,
            'data': data,
            'column_widths': [120, 150, 120, 120, 100, 80, 150, 100, 200],
            'freeze_rows': 1,
            'formatting': {}
        }

    def build_goals_tab(self):
        """Tab 5: All Goals (Michelle, Gray, Shared)"""
        headers = ['GOALS TRACKER', '', '', '', '', '', '', '']

        data = [
            ['', '', '', '', '', '', '', ''],
            ['═══ MICHELLE\'S GOALS ═══', '', '', '', '', '', '', ''],
            ['Goal', 'Category', 'Target Date', 'Status', 'Progress', 'Current', 'Target', 'Notes'],
        ]

        for goal in MICHELLE_GOALS:
            data.append([
                goal['goal'],
                goal['category'],
                goal['target'],
                goal['status'],
                f"{goal['progress']}%",
                goal.get('current_value', ''),
                goal.get('target_value', ''),
                ''
            ])

        data.extend([
            ['', '', '', '', '', '', '', ''],
            ['═══ GRAY\'S GOALS ═══', '', '', '', '', '', '', ''],
            ['Goal', 'Category', 'Target Date', 'Status', 'Progress', 'Current', 'Target', 'Notes'],
        ])

        for goal in GRAY_GOALS:
            data.append([
                goal['goal'],
                goal['category'],
                goal['target'],
                goal['status'],
                f"{goal['progress']}%",
                goal.get('current_value', ''),
                goal.get('target_value', ''),
                ''
            ])

        data.extend([
            ['', '', '', '', '', '', '', ''],
            ['═══ SHARED GOALS ═══', '', '', '', '', '', '', ''],
            ['Goal', 'Category', 'Target Date', 'Status', 'Progress', 'Current', 'Target', 'Notes'],
        ])

        for goal in SHARED_GOALS:
            data.append([
                goal['goal'],
                goal['category'],
                goal['target'],
                goal['status'],
                f"{goal['progress']}%",
                goal.get('current_value', ''),
                goal.get('target_value', ''),
                ''
            ])

        return {
            'tab_name': 'Goals',
            'headers': headers,
            'data': data,
            'column_widths': [250, 100, 100, 100, 80, 100, 100, 200],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [5, 6],
            }
        }

    def build_household_tab(self):
        """Tab 6: Household Tasks & Projects"""
        headers = ['HOUSEHOLD MANAGEMENT', '', '', '', '', '', '', '']

        data = [
            ['', '', '', '', '', '', '', ''],
            ['═══ RECURRING TASKS ═══', '', '', '', '', '', '', ''],
            ['Task', 'Category', 'Owner', 'Frequency', 'Time (min)', 'Last Done', 'Status', 'Notes'],
        ]

        for task in RECURRING_TASKS:
            data.append([
                task['task'],
                task['category'],
                task['owner'],
                task['frequency'],
                task['time_estimate'],
                '',
                '',
                ''
            ])

        data.extend([
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['═══ ONE-TIME PROJECTS ═══', '', '', '', '', '', '', ''],
            ['Project', 'Category', 'Owner', 'Priority', 'Status', 'Budget', 'Actual', 'Notes'],
            ['Kitchen renovation', 'Home', 'Both', 'High', 'In Progress', '$15,000', '', ''],
            ['Garden landscaping', 'Outdoor', 'Gray', 'Medium', 'Not Started', '$5,000', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['═══ GIFT TRACKER ═══', '', '', '', '', '', '', ''],
            ['Recipient', 'Birthday', 'Gift Idea', 'Budget', 'Purchase By', 'Purchased', 'Address', 'Notes'],
        ])

        for recipient in GIFT_RECIPIENTS:
            data.append([
                recipient['name'],
                recipient['birthday'],
                '',
                '',
                '',
                '',
                recipient['address'],
                recipient['notes']
            ])

        data.extend([
            ['', '', '', '', '', '', '', ''],
            ['═══ LOAD BALANCE ═══', '', '', '', '', '', '', ''],
            ['Michelle Hours/Week', '=SUMIF(C4:C8,"Michelle",E4:E8)/60', '', 'Gray Hours/Week', '=SUMIF(C4:C8,"Gray",E4:E8)/60', '', '', ''],
            ['Balance Ratio', '=IFERROR(B29/E29,0)', '', '', '', '', '', ''],
        ])

        return {
            'tab_name': 'Household',
            'headers': headers,
            'data': data,
            'column_widths': [180, 100, 80, 100, 80, 100, 100, 200],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [5, 6],
            }
        }

    def build_shelzys_tab(self):
        """Tab 7: Shelzy's Designs Business"""
        headers = ["SHELZY'S DESIGNS", '', '', '', '', '', '']

        data = [
            ['', '', '', '', '', '', ''],
            ['═══ TRANSACTIONS ═══', '', '', '', '', '', ''],
            ['Date', 'Type', 'Category', 'Description', 'Amount', 'Channel', 'Notes'],
            ['', 'Revenue', 'Product Sales', '', '', 'Shopify', ''],
            ['', 'Revenue', 'Product Sales', '', '', 'Amazon', ''],
            ['', 'Expense', 'Marketing', '', '', '', ''],
            ['', 'Expense', 'COGS', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['═══ PRODUCTS ═══', '', '', '', '', '', ''],
            ['SKU', 'Product Name', 'Price', 'Cost', 'Margin', 'Stock', 'Status'],
            ['SHZ-001', 'Side Hustle Empire Tracker', '$29.99', '$2.50', '92%', 'Digital', 'Active'],
            ['SHZ-002', 'Budget Planner Bundle', '$49.99', '$4.00', '92%', 'Digital', 'Active'],
            ['SHZ-003', 'Goal Setting Workbook', '$19.99', '$1.50', '92%', 'Digital', 'Active'],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['═══ MONTHLY P&L ═══', '', '', '', '', '', ''],
            ['', 'Jan', 'Feb', 'Mar', 'Apr', 'YTD', ''],
            ['Revenue', '', '', '', '', '=SUM(B20:E20)', ''],
            ['COGS', '', '', '', '', '=SUM(B21:E21)', ''],
            ['Gross Profit', '=B20-B21', '=C20-C21', '=D20-D21', '=E20-E21', '=F20-F21', ''],
            ['Marketing', '', '', '', '', '=SUM(B23:E23)', ''],
            ['Operations', '', '', '', '', '=SUM(B24:E24)', ''],
            ['Net Profit', '=B22-B23-B24', '=C22-C23-C24', '=D22-D23-D24', '=E22-E23-E24', '=F22-F23-F24', ''],
            ['', '', '', '', '', '', ''],
            ['═══ KEY METRICS ═══', '', '', '', '', '', ''],
            ['Total Revenue (MTD)', '=SUMIF(B4:B10,"Revenue",E4:E10)', '', 'Avg Order Value', '', '', ''],
            ['Total Orders (MTD)', '', '', 'Repeat Rate', '', '', ''],
            ['Marketing ROAS', '', '', 'Best Channel', '', '', ''],
        ]

        return {
            'tab_name': "Shelzy's Business",
            'headers': headers,
            'data': data,
            'column_widths': [150, 100, 120, 150, 100, 100, 150],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [4],
            }
        }

    def build_health_tab(self, oura_data=None):
        """Tab 8: Health & Fertility (including Oura data)"""
        headers = ['HEALTH & FERTILITY', '', '', '', '', '', '']

        # Generate sample Oura data
        import random
        sleep_data = []
        for i in range(14):
            sleep_data.append([
                f'=TODAY()-{13-i}',
                random.randint(65, 95),  # Sleep score
                round(random.uniform(6, 9), 1),  # Hours
                random.randint(45, 120),  # Deep
                random.randint(60, 150),  # REM
            ])

        data = [
            ['', '', '', '', '', '', ''],
            ['═══ TODAY\'S HEALTH ═══', '', '', '═══ CYCLE TRACKING ═══', '', '', ''],
            ['Sleep Score', random.randint(70, 95), '', 'Current Cycle Day', '', '', ''],
            ['Readiness Score', random.randint(70, 95), '', 'Cycle Phase', '', '', ''],
            ['Activity Score', random.randint(70, 95), '', 'Period Start', '', '', ''],
            ['Cycle Day', '', '', 'Ovulation (Est)', '', '', ''],
            ['Resting HR', f'{random.randint(55, 70)} bpm', '', 'Cycle Length (Avg)', '', '', ''],
            ['HRV', random.randint(30, 60), '', 'Luteal Phase (Avg)', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['═══ SLEEP LOG (14 Days) ═══', '', '', '', '', '', ''],
            ['Date', 'Score', 'Hours', 'Deep (min)', 'REM (min)', 'Efficiency', 'Notes'],
        ]

        for row in sleep_data:
            data.append(row + ['', ''])

        data.extend([
            ['', '', '', '', '', '', ''],
            ['═══ DAILY FERTILITY LOG ═══', '', '', '', '', '', ''],
            ['Date', 'Cycle Day', 'BBT', 'Cervical Mucus', 'OPK', 'Notes', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['═══ SUPPLEMENTS ═══', '', '', '', '', '', ''],
            ['Supplement', 'Dosage', 'Frequency', 'Purpose', 'Status', '', ''],
        ])

        for supp in SUPPLEMENTS:
            data.append([
                supp['name'],
                supp['dosage'],
                supp['frequency'],
                supp['purpose'],
                supp['status'],
                '',
                ''
            ])

        data.extend([
            ['', '', '', '', '', '', ''],
            ['═══ APPOINTMENTS ═══', '', '', '', '', '', ''],
            ['Date', 'Provider', 'Type', 'Reason', 'Follow-up', 'Notes', ''],
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
        ])

        return {
            'tab_name': 'Health',
            'headers': headers,
            'data': data,
            'column_widths': [100, 100, 100, 120, 100, 100, 150],
            'freeze_rows': 1,
            'formatting': {}
        }


# Tab configuration for simplified version
SIMPLIFIED_TABS = [
    {"name": "Dashboard", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "Transactions", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "Budget & Spending", "color": {"red": 0.26, "green": 0.52, "blue": 0.96}},
    {"name": "Job Search", "color": {"red": 0.42, "green": 0.65, "blue": 0.31}},
    {"name": "Goals", "color": {"red": 0.95, "green": 0.76, "blue": 0.20}},
    {"name": "Household", "color": {"red": 0.61, "green": 0.35, "blue": 0.71}},
    {"name": "Shelzy's Business", "color": {"red": 0.91, "green": 0.46, "blue": 0.22}},
    {"name": "Health", "color": {"red": 0.96, "green": 0.70, "blue": 0.80}},
]


def get_simplified_tab_data():
    """Get simplified tab configurations"""
    return {
        'tabs': [t['name'] for t in SIMPLIFIED_TABS],
        'count': 8
    }
