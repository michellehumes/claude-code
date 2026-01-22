"""
Financial Dashboard Tab Builder (Tabs 1-11)

Tab 1: Dashboard (HOME)
Tab 2: Transactions (MASTER DATA)
Tab 3: Credit Cards
Tab 4: Budget Master
Tab 5: Spending by Category
Tab 6: Monthly Summary
Tab 7: Spending by Merchant
Tab 8: Master Tasks
Tab 9: Gift Tracker
Tab 10: Health Dashboard
Tab 11: Calendar View
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, VALIDATION, GIFT_RECIPIENTS


class FinancialTabBuilder:
    """Build financial dashboard tabs (1-11)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self, transaction_data=None):
        """Build all financial tabs"""
        results = {}

        results['dashboard'] = self.build_dashboard_tab()
        results['transactions'] = self.build_transactions_tab(transaction_data)
        results['credit_cards'] = self.build_credit_cards_tab()
        results['budget_master'] = self.build_budget_master_tab()
        results['spending_category'] = self.build_spending_category_tab()
        results['monthly_summary'] = self.build_monthly_summary_tab()
        results['spending_merchant'] = self.build_spending_merchant_tab()
        results['master_tasks'] = self.build_master_tasks_tab()
        results['gift_tracker'] = self.build_gift_tracker_tab()
        results['health_dashboard'] = self.build_health_dashboard_tab()
        results['calendar_view'] = self.build_calendar_view_tab()

        return results

    def build_dashboard_tab(self):
        """
        Tab 1: Dashboard (HOME SCREEN)
        Executive summary with 4-entity breakdown
        """
        headers = [
            ['LIFE OS v2 - DASHBOARD', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['FINANCIAL OVERVIEW', '', '', 'SHELZY\'S DESIGNS', '', '', 'HEALTH STATUS', ''],
            ['Metric', 'Michelle', 'Gray', 'Joint', 'Metric', 'Value', 'Metric', 'Value'],
        ]

        # Dashboard metrics structure
        metrics = [
            ['Monthly Income', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"Michelle*",\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))',
             '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"Gray*",\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))',
             '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Joint*",\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))',
             'MTD Revenue', '=SUMIFS(\'📊 Shelzy\'\'s Transactions\'!G:G,\'📊 Shelzy\'\'s Transactions\'!C:C,"Revenue*",\'📊 Shelzy\'\'s Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))',
             'Current Cycle Day', '=\'🌸 Cycle Tracking\'!E2'],
            ['Monthly Expenses', '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"Michelle*",\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))',
             '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"Gray*",\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))',
             '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Joint*",\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))',
             'MTD Expenses', '=ABS(SUMIFS(\'📊 Shelzy\'\'s Transactions\'!G:G,\'📊 Shelzy\'\'s Transactions\'!C:C,"<>Revenue*",\'📊 Shelzy\'\'s Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))',
             'Sleep Score', '=\'🔴 Oura Sleep Tracker\'!B2'],
            ['Net Cash Flow', '=B5-B6', '=C5-C6', '=D5-D6',
             'MTD Profit', '=F5-F6',
             'Readiness Score', '=\'🔴 Oura Readiness Tracker\'!B2'],
            ['Savings Rate', '=IF(B5>0,B7/B5,0)', '=IF(C5>0,C7/C5,0)', '=IF(D5>0,D7/D5,0)',
             'Profit Margin', '=IF(F5>0,F7/F5,0)',
             'Activity Score', '=\'🔴 Oura Activity Tracker\'!B2'],
            ['', '', '', '', '', '', '', ''],
            ['JOB SEARCH STATUS', '', '', 'GOALS PROGRESS', '', '', 'UPCOMING', ''],
            ['Active Applications', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"<>Rejected")-COUNTIF(\'💼 Job Pipeline\'!H:H,"Offer")', '',
             'Michelle Goals On Track', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!F:F,"On Track")', '',
             'Interviews This Week', '=COUNTIFS(\'💼 Interview Tracker\'!C:C,">="&TODAY(),\'💼 Interview Tracker\'!C:C,"<"&TODAY()+7)'],
            ['This Week Applications', '=COUNTIFS(\'💼 Applications Tracker\'!B:B,">="&TODAY()-7)', '',
             'Gray Goals On Track', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!F:F,"On Track")', '',
             'Follow-ups Due', '=COUNTIFS(\'💼 Follow-Ups\'!D:D,"<="&TODAY(),\'💼 Follow-Ups\'!F:F,"")'],
            ['Interviews Scheduled', '=COUNTIFS(\'💼 Interview Tracker\'!C:C,">="&TODAY())', '',
             'Shared Goals On Track', '=COUNTIF(\'🎯 Shared Goals\'!F:F,"On Track")', '',
             'Appointments Today', '=COUNTIFS(\'🌸 Appointments\'!A:A,TODAY())'],
            ['', '', '', '', '', '', '', ''],
            ['HOUSEHOLD LOAD', '', '', '', '', '', '', ''],
            ['Michelle Hours/Week', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Michelle",\'🏠 Recurring Tasks\'!E:E)/60', '',
             'Gray Hours/Week', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Gray",\'🏠 Recurring Tasks\'!E:E)/60', '',
             'Load Balance', '=IF(B17>0,C17/B17*100,0)&"%"'],
        ]

        data = headers + metrics

        return {
            'tab_name': '📋 Dashboard',
            'headers': headers[3],
            'data': data,
            'column_widths': [150, 120, 120, 120, 150, 120, 150, 120],
            'freeze_rows': 1,
            'formatting': {
                'title_row': 0,
                'section_rows': [2, 10, 15],
                'currency_cols': [1, 2, 3, 5],
                'percentage_cols': [7],
            }
        }

    def build_transactions_tab(self, transaction_data=None):
        """
        Tab 2: Transactions (MASTER DATA SOURCE)
        Import entire CSV unchanged
        """
        headers = ['Date', 'Merchant', 'Category', 'Account', 'Original Statement',
                   'Notes', 'Amount', 'Tags', 'Owner']

        if transaction_data is None:
            # Generate sample data
            from src.data_processors.transactions import TransactionProcessor
            transaction_data = TransactionProcessor.generate_sample_data()

        return {
            'tab_name': '📊 Transactions',
            'headers': headers,
            'data': transaction_data,
            'column_widths': [100, 180, 150, 200, 250, 150, 100, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'currency_col': 6,
                'conditional': {
                    'income_expense': {
                        'column': 6,
                        'positive_color': COLORS['positive'],
                        'negative_color': COLORS['negative']
                    }
                }
            }
        }

    def build_credit_cards_tab(self):
        """
        Tab 3: Credit Cards
        Auto-calculate metrics from transactions
        """
        headers = ['Account Name', 'Current Balance', 'This Month Spent', 'This Year Spent',
                   'All-Time Spent', 'Last Transaction', 'Transaction Count', 'Average Transaction',
                   'Primary Category']

        # Formula-based rows that pull from Transactions
        # These will be populated with actual data or formulas
        sample_cards = [
            ['Sapphire Reserve (...1041)', '', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))*-1',
             '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))*-1',
             '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!G:G,"<0")*-1',
             '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A2)',
             '=COUNTIF(\'📊 Transactions\'!D:D,A2)',
             '=IFERROR(E2/G2,0)',
             '=INDEX(\'📊 Transactions\'!C:C,MATCH(A2,\'📊 Transactions\'!D:D,0))'],
            ['Amex Gold (...2003)', '', '', '', '', '', '', '', ''],
            ['Venture Card (...4522)', '', '', '', '', '', '', '', ''],
            ['Freedom Unlimited (...9759)', '', '', '', '', '', '', '', ''],
            ['Amazon Prime Card (...5990)', '', '', '', '', '', '', '', ''],
            ['Target Circle Card (...2828)', '', '', '', '', '', '', '', ''],
            ['USAA Visa (...9385)', '', '', '', '', '', '', '', ''],
            ['Amex Platinum (...1007)', '', '', '', '', '', '', '', ''],
        ]

        return {
            'tab_name': '💳 Credit Cards',
            'headers': headers,
            'data': sample_cards,
            'column_widths': [200, 120, 120, 120, 120, 120, 100, 120, 150],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [1, 2, 3, 4, 7],
                'date_col': 5,
            }
        }

    def build_budget_master_tab(self):
        """
        Tab 4: Budget Master
        Monthly budgets with actual spending tracking
        """
        headers = ['Category', 'Monthly Budget', 'Actual Spent', 'Remaining',
                   '% Used', 'Last Month', '3-Month Avg', 'YTD', 'Status']

        # Pre-populate categories with formulas
        categories = [
            'Groceries', 'Restaurants & Bars', 'Shopping', 'Gas', 'Utilities',
            'Rent', 'Insurance', 'Healthcare', 'Entertainment', 'Travel',
            'Subscriptions', 'Car Payment', 'Phone', 'Internet', 'Gym',
            'Personal Care', 'Clothing', 'Home', 'Gifts', 'Education',
            'Pets', 'Charity', 'Business', 'Taxes', 'Other'
        ]

        data = []
        for i, cat in enumerate(categories):
            row_num = i + 2
            data.append([
                cat,
                '',  # Monthly Budget - manual entry
                f'=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A{row_num},\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))',
                f'=B{row_num}-C{row_num}',
                f'=IFERROR(C{row_num}/B{row_num},0)',
                f'=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A{row_num},\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1)))',
                f'=AVERAGE(C{row_num},F{row_num},ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A{row_num},\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-2))))',
                f'=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A{row_num},\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1)))',
                f'=IF(E{row_num}<0.75,"✅ Under",IF(E{row_num}<0.9,"⚠️ Warning",IF(E{row_num}<=1,"🔶 Near Limit","🔴 Over")))'
            ])

        return {
            'tab_name': '📊 Budget Master',
            'headers': headers,
            'data': data,
            'column_widths': [150, 120, 120, 120, 100, 120, 120, 120, 120],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [1, 2, 3, 5, 6, 7],
                'percentage_col': 4,
                'conditional': {
                    'budget_status': {
                        'column': 4,
                        'thresholds': [0.75, 0.9, 1.0]
                    }
                }
            },
            'validation': {
                'budget_col': {
                    'column': 1,
                    'type': 'number',
                    'min': 0
                }
            }
        }

    def build_spending_category_tab(self):
        """
        Tab 5: Spending by Category
        Auto-calculated category breakdowns
        """
        headers = ['Category', 'This Month', 'Last Month', '3-Month Avg', '6-Month Avg',
                   'YTD', '% of Total', 'Transaction Count', 'Avg Transaction', 'Trend']

        # Use QUERY or array formulas for dynamic population
        data = [
            ['=UNIQUE(\'📊 Transactions\'!C:C)', '', '', '', '', '', '', '', '', ''],
        ]

        return {
            'tab_name': '📈 Spending by Category',
            'headers': headers,
            'data': data,
            'column_widths': [150, 120, 120, 120, 120, 120, 100, 100, 120, 80],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [1, 2, 3, 4, 5, 8],
                'percentage_col': 6,
            }
        }

    def build_monthly_summary_tab(self):
        """
        Tab 6: Monthly Summary
        Last 24 months of financial summaries
        """
        headers = ['Month', 'Total Income', 'Total Expenses', 'Net', 'Savings Rate %',
                   'Transaction Count', 'Avg Daily Spending']

        # Generate 24 months of data with formulas
        data = []
        for i in range(24):
            row_num = i + 2
            data.append([
                f'=TEXT(EOMONTH(TODAY(),-{i}),"MMM YYYY")',
                f'=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-{i+1})+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-{i}))',
                f'=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-{i+1})+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-{i})))',
                f'=B{row_num}-C{row_num}',
                f'=IFERROR(D{row_num}/B{row_num},0)',
                f'=COUNTIFS(\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-{i+1})+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-{i}))',
                f'=IFERROR(C{row_num}/DAY(EOMONTH(TODAY(),-{i})),0)'
            ])

        return {
            'tab_name': '💰 Monthly Summary',
            'headers': headers,
            'data': data,
            'column_widths': [120, 130, 130, 120, 120, 120, 130],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [1, 2, 3, 6],
                'percentage_col': 4,
                'conditional': {
                    'net': {
                        'column': 3,
                        'positive_color': COLORS['positive'],
                        'negative_color': COLORS['negative']
                    },
                    'savings_rate': {
                        'column': 4,
                        'thresholds': [0.1, 0.2]
                    }
                }
            }
        }

    def build_spending_merchant_tab(self):
        """
        Tab 7: Spending by Merchant
        Top 100 merchants by spending
        """
        headers = ['Merchant', 'Transaction Count', 'Total Spent', 'Avg Transaction',
                   'Primary Category', 'Last Transaction', 'This Month', 'YTD']

        # This will be populated from transaction data processing
        data = []

        return {
            'tab_name': '📊 Spending by Merchant',
            'headers': headers,
            'data': data,
            'column_widths': [200, 100, 120, 120, 150, 120, 120, 120],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [2, 3, 6, 7],
                'date_col': 5,
            }
        }

    def build_master_tasks_tab(self):
        """
        Tab 8: Master Tasks
        Unified task management
        """
        headers = ['✓', 'Task', 'Priority', 'Status', 'Due Date', 'Category',
                   'Owner', 'Linked Goal ID', 'Time Estimate (min)', 'Notes']

        sample_tasks = [
            [False, 'Review monthly budget', 'P1 - High', 'Not Started', '', 'Finance', 'Michelle', '', 30, ''],
            [False, 'Update job applications', 'P0 - Critical', 'In Progress', '', 'Career', 'Michelle', 'MG-001', 60, ''],
            [False, 'Schedule doctor appointment', 'P2 - Medium', 'Not Started', '', 'Health', 'Michelle', '', 15, ''],
            [False, 'Process Shelzy\'s orders', 'P1 - High', 'Not Started', '', 'Business', 'Michelle', 'MG-004', 45, ''],
            [False, 'Yard maintenance', 'P2 - Medium', 'Not Started', '', 'Household', 'Gray', '', 120, ''],
        ]

        return {
            'tab_name': '✅ Master Tasks',
            'headers': headers,
            'data': sample_tasks,
            'column_widths': [40, 250, 120, 120, 100, 100, 80, 100, 100, 200],
            'freeze_rows': 1,
            'formatting': {
                'checkbox_col': 0,
                'date_col': 4,
                'conditional': {
                    'overdue': {
                        'column': 4,
                        'formula': '=AND(E2<TODAY(),E2<>"")'
                    },
                    'completed': {
                        'column': 0,
                        'strikethrough_row': True
                    }
                }
            },
            'validation': {
                'priority': {'column': 2, 'values': VALIDATION['priority']},
                'status': {'column': 3, 'values': VALIDATION['status']},
                'category': {'column': 5, 'values': VALIDATION['goal_category']},
                'owner': {'column': 6, 'values': VALIDATION['task_owner']},
            }
        }

    def build_gift_tracker_tab(self):
        """
        Tab 9: Gift Tracker
        Birthday and gift management
        """
        headers = ['Recipient', 'Birthday', 'Address', 'Gift Idea', 'Budget',
                   'Purchase By Date', 'Purchased', 'Shipped', 'Notes']

        # Pre-populate with configured recipients
        data = []
        for recipient in GIFT_RECIPIENTS:
            purchase_by = f'=IF(B{len(data)+2}<>"",B{len(data)+2}-14,"")' if recipient['birthday'] else ''
            data.append([
                recipient['name'],
                recipient['birthday'],
                recipient['address'],
                '',
                '',
                purchase_by,
                False,
                False,
                recipient['notes']
            ])

        return {
            'tab_name': '🎁 Gift Tracker',
            'headers': headers,
            'data': data,
            'column_widths': [150, 100, 250, 200, 100, 120, 80, 80, 200],
            'freeze_rows': 1,
            'formatting': {
                'currency_col': 4,
                'date_cols': [1, 5],
                'checkbox_cols': [6, 7],
                'conditional': {
                    'purchase_due': {
                        'column': 5,
                        'formula': '=AND(F2<TODAY(),F2<>"",G2=FALSE)',
                        'color': COLORS['negative']
                    }
                }
            }
        }

    def build_health_dashboard_tab(self):
        """
        Tab 10: Health Dashboard
        Weight, workouts, and appointments
        """
        headers = ['HEALTH TRACKING', '', '', '', '', '']

        # Multi-section layout
        data = [
            ['WEIGHT LOG', '', '', '', '', ''],
            ['Date', 'Weight (lbs)', 'BMI', 'Notes', '', ''],
            ['', '', '=IF(B3<>"",B3/(70*70)*703,"")', '', '', ''],  # Sample BMI formula
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            # Section break
            ['', '', '', '', '', ''],
            ['WORKOUTS', '', '', '', '', ''],
            ['Date', 'Type', 'Duration (min)', 'Intensity', 'Calories', 'Notes'],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            # Section break
            ['', '', '', '', '', ''],
            ['APPOINTMENTS', '', '', '', '', ''],
            ['Date', 'Provider', 'Type', 'Reason', 'Follow-up Date', 'Notes'],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
        ]

        return {
            'tab_name': '🩺 Health Dashboard',
            'headers': headers,
            'data': data,
            'column_widths': [100, 120, 100, 150, 120, 200],
            'freeze_rows': 0,
            'formatting': {
                'section_headers': [0, 7, 13],
                'date_cols': [0],
            }
        }

    def build_calendar_view_tab(self):
        """
        Tab 11: Calendar View
        Visual monthly spending calendar
        """
        # Generate calendar structure
        headers = ['', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        # Current month calendar with spending totals
        data = [
            ['Week 1', '', '', '', '', '', '', ''],
            ['Week 2', '', '', '', '', '', '', ''],
            ['Week 3', '', '', '', '', '', '', ''],
            ['Week 4', '', '', '', '', '', '', ''],
            ['Week 5', '', '', '', '', '', '', ''],
            ['Week 6', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['LEGEND', '', '', '', '', '', '', ''],
            ['🟢 < $100', '🟡 $100-$200', '🟠 $200-$300', '🔴 > $300', '', '', '', ''],
        ]

        return {
            'tab_name': '📅 Calendar View',
            'headers': headers,
            'data': data,
            'column_widths': [80, 100, 100, 100, 100, 100, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'conditional': {
                    'spending_level': {
                        'columns': [1, 2, 3, 4, 5, 6, 7],
                        'thresholds': [100, 200, 300]
                    }
                }
            }
        }


def get_financial_tab_data():
    """Get all financial tab configurations without building"""
    return {
        'tabs': [
            '📋 Dashboard',
            '📊 Transactions',
            '💳 Credit Cards',
            '📊 Budget Master',
            '📈 Spending by Category',
            '💰 Monthly Summary',
            '📊 Spending by Merchant',
            '✅ Master Tasks',
            '🎁 Gift Tracker',
            '🩺 Health Dashboard',
            '📅 Calendar View',
        ],
        'count': 11
    }
