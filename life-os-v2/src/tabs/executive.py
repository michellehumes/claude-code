"""
Executive Dashboards Tab Builder (Tabs 41-46)

Tab 41: Weekly Life Summary
Tab 42: Job Search Status
Tab 43: Financial Health
Tab 44: Goal Progress
Tab 45: Household Load
Tab 46: Business Performance
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS


class ExecutiveTabBuilder:
    """Build executive dashboard tabs (41-46)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self):
        """Build all executive dashboard tabs"""
        results = {}

        results['weekly_summary'] = self.build_weekly_summary_tab()
        results['job_search_status'] = self.build_job_search_status_tab()
        results['financial_health'] = self.build_financial_health_tab()
        results['goal_progress'] = self.build_goal_progress_tab()
        results['household_load'] = self.build_household_load_tab()
        results['business_performance'] = self.build_business_performance_tab()

        return results

    def build_weekly_summary_tab(self):
        """
        Tab 41: Weekly Life Summary
        Comprehensive weekly overview
        """
        headers = ['WEEKLY LIFE SUMMARY', '', '', '', '', '', '']

        dashboard_data = [
            [f'Week of {chr(34)}=TEXT(TODAY()-WEEKDAY(TODAY(),2)+1,"MMM D"){chr(34)}', '', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['HEALTH STATUS', '', '', 'JOB SEARCH', '', '', ''],
            ['Overall Health', '=IF(AVERAGE(\'🔴 Oura Health Dashboard\'!B3:B5)>=85,"🟢 Optimal",IF(AVERAGE(\'🔴 Oura Health Dashboard\'!B3:B5)>=70,"🟡 Good",IF(AVERAGE(\'🔴 Oura Health Dashboard\'!B3:B5)>=55,"🟠 Pay Attention","🔴 Rest Needed")))', '', 'Active Applications', '=COUNTIFS(\'💼 Job Pipeline\'!P:P,"Active")', '', ''],
            ['Sleep Score (7d avg)', '=AVERAGE(FILTER(\'🔴 Oura Sleep Tracker\'!B:B,\'🔴 Oura Sleep Tracker\'!A:A>=TODAY()-7))', '', 'Interviews This Week', '=COUNTIFS(\'💼 Interview Tracker\'!C:C,">="&TODAY()-WEEKDAY(TODAY(),2)+1,\'💼 Interview Tracker\'!C:C,"<"&TODAY()-WEEKDAY(TODAY(),2)+8)', '', ''],
            ['Readiness (7d avg)', '=AVERAGE(FILTER(\'🔴 Oura Readiness Tracker\'!B:B,\'🔴 Oura Readiness Tracker\'!A:A>=TODAY()-7))', '', 'Offers Received', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"Offer")', '', ''],
            ['Activity (7d avg)', '=AVERAGE(FILTER(\'🔴 Oura Activity Tracker\'!B:B,\'🔴 Oura Activity Tracker\'!A:A>=TODAY()-7))', '', 'Top Priority', '=INDEX(\'💼 Job Pipeline\'!C:C,MATCH("P0 - Critical",\'💼 Job Pipeline\'!M:M,0))', '', ''],
            ['Cycle Day', '=\'🔴 Oura Cycle Integration\'!B2', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['GOALS', '', '', 'HOUSEHOLD', '', '', ''],
            ['On Track', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"On Track")+COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"On Track")+COUNTIF(\'🎯 Shared Goals\'!H:H,"On Track")', '', 'Tasks Completed', '=COUNTIFS(\'🏠 Recurring Tasks\'!F:F,">="&TODAY()-7)', '', ''],
            ['At Risk', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"At Risk")+COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"At Risk")+COUNTIF(\'🎯 Shared Goals\'!H:H,"At Risk")', '', 'Overdue Tasks', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*Overdue*")', '', ''],
            ['Blocked', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"Blocked")+COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"Blocked")+COUNTIF(\'🎯 Shared Goals\'!H:H,"Blocked")', '', 'Load Balance', '=\'🏠 Load Dashboard\'!B12', '', ''],
            ['Completion Rate', '=IFERROR(COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"Completed")/(COUNTA(\'🎯 Michelle\'\'s Goals\'!H:H)-1),0)', '', '', '', '', ''],
            ['', '', '', '', '', '', ''],
            ['FINANCES', '', '', 'SHELZY\'S DESIGNS', '', '', ''],
            ['Weekly Spending', '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&TODAY()-7))', '', 'Weekly Revenue', '=SUMIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!J:J,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&TODAY()-7)', '', ''],
            ['Budget Status', '=IF(AVERAGE(\'📊 Budget Master\'!E:E)<0.75,"🟢 Under Budget",IF(AVERAGE(\'📊 Budget Master\'!E:E)<0.9,"🟡 On Track","🔴 Over Budget"))', '', 'Weekly Profit', '=B17-ABS(SUMIFS(\'📊 Shelzy\'\'s Transactions\'!G:G,\'📊 Shelzy\'\'s Transactions\'!B:B,"Expense",\'📊 Shelzy\'\'s Transactions\'!A:A,">="&TODAY()-7))', '', ''],
            ['Net Cash Flow', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!A:A,">="&TODAY()-7)', '', 'Profit Margin', '=IFERROR(E18/E17,0)', '', ''],
            ['', '', '', '', '', '', ''],
            ['THIS WEEK\'S WINS', '', '', 'NEXT WEEK\'S PRIORITIES', '', '', ''],
            ['1.', '', '', '1.', '', '', ''],
            ['2.', '', '', '2.', '', '', ''],
            ['3.', '', '', '3.', '', '', ''],
        ]

        return {
            'tab_name': '📈 Weekly Life Summary',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [180, 150, 50, 180, 150, 50, 50],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [2, 9, 15, 20],
                'currency_cols': [1, 4],
            }
        }

    def build_job_search_status_tab(self):
        """
        Tab 42: Job Search Status
        Duplicate/reference to Tab 18
        """
        headers = ['JOB SEARCH STATUS', '', '', '', '', '']

        # Reference data from Job Search Dashboard
        dashboard_data = [
            ['', '', '', '', '', ''],
            ['This tab mirrors the Job Search Dashboard (Tab 18)', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['QUICK STATS', '', '', '', '', ''],
            ['Active Applications', '=COUNTIFS(\'💼 Job Pipeline\'!P:P,"Active")', '', '', '', ''],
            ['Interviews Scheduled', '=COUNTIFS(\'💼 Interview Tracker\'!C:C,">="&TODAY())', '', '', '', ''],
            ['Follow-ups Due', '=COUNTIFS(\'💼 Follow-Ups\'!D:D,"<="&TODAY(),\'💼 Follow-Ups\'!E:E,"")', '', '', '', ''],
            ['Conversion Rate', '=IFERROR(COUNTIF(\'💼 Job Pipeline\'!H:H,"Interview")/COUNTIF(\'💼 Job Pipeline\'!H:H,"Applied"),0)', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['For detailed view, see 💼 Job Search Dashboard', '', '', '', '', ''],
        ]

        return {
            'tab_name': '📈 Job Search Status',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [200, 120, 100, 100, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [3],
            }
        }

    def build_financial_health_tab(self):
        """
        Tab 43: Financial Health
        4-entity financial overview
        """
        headers = ['FINANCIAL HEALTH OVERVIEW', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['MICHELLE PERSONAL', '', '', 'GRAY PERSONAL', '', ''],
            ['Monthly Income', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Michelle*",\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', '', 'Monthly Income', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Gray*",\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', ''],
            ['Monthly Expenses', '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Michelle*",\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))', '', 'Monthly Expenses', '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Gray*",\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))', ''],
            ['Net', '=B3-B4', '', 'Net', '=E3-E4', ''],
            ['Savings Rate', '=IFERROR(B5/B3,0)', '', 'Savings Rate', '=IFERROR(E5/E3,0)', ''],
            ['Budget Status', '=IF(B4<SUM(\'📊 Budget Master\'!B:B)*0.3,"🟢 Under","🟡 On Track")', '', 'Budget Status', '=IF(E4<SUM(\'📊 Budget Master\'!B:B)*0.3,"🟢 Under","🟡 On Track")', ''],
            ['', '', '', '', '', ''],
            ['JOINT HOUSEHOLD', '', '', 'SHELZY\'S DESIGNS', '', ''],
            ['Monthly Income', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Joint*",\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', '', 'Monthly Revenue', '=SUMIFS(\'📊 Shelzy\'\'s Transactions\'!G:G,\'📊 Shelzy\'\'s Transactions\'!B:B,"Revenue",\'📊 Shelzy\'\'s Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', ''],
            ['Monthly Expenses', '=ABS(SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!I:I,"*Joint*",\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))', '', 'Monthly Expenses', '=ABS(SUMIFS(\'📊 Shelzy\'\'s Transactions\'!G:G,\'📊 Shelzy\'\'s Transactions\'!B:B,"Expense",\'📊 Shelzy\'\'s Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))', ''],
            ['Net', '=B10-B11', '', 'Profit', '=E10-E11', ''],
            ['Savings Rate', '=IFERROR(B12/B10,0)', '', 'Margin', '=IFERROR(E12/E10,0)', ''],
            ['Budget Status', '', '', 'Cash Runway', '=IFERROR(5000/E11,0)&" months"', ''],
            ['', '', '', '', '', ''],
            ['HOUSEHOLD SUMMARY', '', '', '', '', ''],
            ['Combined Net Worth', '', '(manual entry)', '', '', ''],
            ['Total Household Income', '=B3+E3+B10', '', '', '', ''],
            ['Total Household Expenses', '=B4+E4+B11', '', '', '', ''],
            ['Household Savings Rate', '=IFERROR((B18-B19)/B18,0)', '', '', '', ''],
        ]

        return {
            'tab_name': '📈 Financial Health',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [180, 130, 80, 180, 130, 80],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 8, 15],
                'currency_cols': [1, 4],
                'percentage_rows': [5, 6, 12, 13, 19],
            }
        }

    def build_goal_progress_tab(self):
        """
        Tab 44: Goal Progress
        Reference to Goal Dashboard
        """
        headers = ['GOAL PROGRESS OVERVIEW', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['This tab mirrors the Goal Dashboard (Tab 22)', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['QUICK SUMMARY', '', '', '', '', ''],
            ['', 'Michelle', 'Gray', 'Shared', 'Total', ''],
            ['Total Goals', '=COUNTA(\'🎯 Michelle\'\'s Goals\'!A:A)-1', '=COUNTA(\'🎯 Gray\'\'s Goals\'!A:A)-1', '=COUNTA(\'🎯 Shared Goals\'!A:A)-1', '=B6+C6+D6', ''],
            ['On Track', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"On Track")', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"On Track")', '=COUNTIF(\'🎯 Shared Goals\'!H:H,"On Track")', '=B7+C7+D7', ''],
            ['At Risk', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"At Risk")', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"At Risk")', '=COUNTIF(\'🎯 Shared Goals\'!H:H,"At Risk")', '=B8+C8+D8', ''],
            ['Completed', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"Completed")', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"Completed")', '=COUNTIF(\'🎯 Shared Goals\'!H:H,"Completed")', '=B9+C9+D9', ''],
            ['Avg Progress', '=AVERAGE(\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGE(\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGE(\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B10:D10)', ''],
            ['', '', '', '', '', ''],
            ['For detailed view, see 🎯 Goal Dashboard', '', '', '', '', ''],
        ]

        return {
            'tab_name': '📈 Goal Progress',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [150, 100, 100, 100, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [3],
                'percentage_row': 10,
            }
        }

    def build_household_load_tab(self):
        """
        Tab 45: Household Load
        Reference to Load Dashboard
        """
        headers = ['HOUSEHOLD LOAD OVERVIEW', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['This tab mirrors the Load Dashboard (Tab 25)', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['WEEKLY HOURS', '', '', 'TASK STATUS', '', ''],
            ['Michelle', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Michelle",\'🏠 Recurring Tasks\'!E:E)/60', 'hrs', 'Overdue', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*Overdue*")', ''],
            ['Gray', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Gray",\'🏠 Recurring Tasks\'!E:E)/60', 'hrs', 'Due Soon', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*Due Soon*")', ''],
            ['Shared', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Both",\'🏠 Recurring Tasks\'!E:E)/60', 'hrs', 'On Track', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*On Track*")', ''],
            ['', '', '', '', '', ''],
            ['BALANCE METRICS', '', '', '', '', ''],
            ['Balance Ratio', '=\'🏠 Load Dashboard\'!B11', '', '', '', ''],
            ['Status', '=\'🏠 Load Dashboard\'!B12', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['For detailed view, see 🏠 Load Dashboard', '', '', '', '', ''],
        ]

        return {
            'tab_name': '📈 Household Load',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [150, 100, 80, 150, 100, 80],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [3, 8],
            }
        }

    def build_business_performance_tab(self):
        """
        Tab 46: Business Performance
        Reference to Shelzy's Dashboard
        """
        headers = ['BUSINESS PERFORMANCE', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['This tab mirrors Shelzy\'s Dashboard (Tab 34)', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['MTD SNAPSHOT', '', '', 'YTD TOTALS', '', ''],
            ['Revenue', '=\'📊 Shelzy\'\'s Dashboard\'!B5', '', 'Revenue', '=\'📊 Shelzy\'\'s Dashboard\'!E3', ''],
            ['Expenses', '=\'📊 Shelzy\'\'s Dashboard\'!B6', '', 'Orders', '=\'📊 Shelzy\'\'s Dashboard\'!E4', ''],
            ['Profit', '=\'📊 Shelzy\'\'s Dashboard\'!B7', '', 'Avg Order Value', '=\'📊 Shelzy\'\'s Dashboard\'!E5', ''],
            ['Margin', '=\'📊 Shelzy\'\'s Dashboard\'!B8', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['KEY METRICS', '', '', '', '', ''],
            ['Marketing ROAS', '=\'📊 Shelzy\'\'s Dashboard\'!B17', '', '', '', ''],
            ['Low Stock Items', '=\'📊 Shelzy\'\'s Dashboard\'!E15', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['For detailed view, see 📊 Shelzy\'s Dashboard', '', '', '', '', ''],
        ]

        return {
            'tab_name': '📈 Business Performance',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [150, 120, 80, 150, 120, 80],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [3, 9],
                'currency_cols': [1, 4],
            }
        }


def get_executive_tab_data():
    """Get all executive tab configurations without building"""
    return {
        'tabs': [
            '📈 Weekly Life Summary',
            '📈 Job Search Status',
            '📈 Financial Health',
            '📈 Goal Progress',
            '📈 Household Load',
            '📈 Business Performance',
        ],
        'count': 6
    }
