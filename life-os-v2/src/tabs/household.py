"""
Household System Tab Builder (Tabs 23-25)

Tab 23: Recurring Tasks
Tab 24: One-Time Projects
Tab 25: Load Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, VALIDATION, RECURRING_TASKS


class HouseholdTabBuilder:
    """Build household system tabs (23-25)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self):
        """Build all household tabs"""
        results = {}

        results['recurring_tasks'] = self.build_recurring_tasks_tab()
        results['projects'] = self.build_one_time_projects_tab()
        results['load_dashboard'] = self.build_load_dashboard_tab()

        return results

    def build_recurring_tasks_tab(self):
        """
        Tab 23: Recurring Tasks
        Regular household tasks
        """
        headers = ['Task', 'Category', 'Owner', 'Frequency', 'Time Estimate (min)',
                   'Last Completed', 'Next Due', 'Status', 'Notes']

        data = []
        for i, task in enumerate(RECURRING_TASKS):
            row_num = i + 2
            # Calculate next due based on frequency
            freq_days = {
                'Daily': 1, 'Weekly': 7, 'Biweekly': 14,
                'Monthly': 30, 'Quarterly': 90, 'Annually': 365
            }
            days = freq_days.get(task['frequency'], 7)

            data.append([
                task['task'],
                task['category'],
                task['owner'],
                task['frequency'],
                task['time_estimate'],
                '',  # Last Completed - manual entry
                f'=IF(F{row_num}<>"",F{row_num}+{days},"")',  # Next Due
                f'=IF(G{row_num}="","",IF(G{row_num}<TODAY(),"🔴 Overdue",IF(G{row_num}<TODAY()+3,"🟡 Due Soon","🟢 On Track")))',
                ''
            ])

        return {
            'tab_name': '🏠 Recurring Tasks',
            'headers': headers,
            'data': data,
            'column_widths': [200, 120, 100, 100, 100, 120, 120, 120, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [5, 6],
                'conditional': {
                    'overdue': {
                        'column': 6,
                        'formula': '=AND(G2<TODAY(),G2<>"")',
                        'color': COLORS['negative']
                    },
                    'due_soon': {
                        'column': 6,
                        'formula': '=AND(G2<TODAY()+3,G2>=TODAY())',
                        'color': COLORS['warning']
                    }
                }
            },
            'validation': {
                'owner': {'column': 2, 'values': VALIDATION['task_owner']},
                'frequency': {'column': 3, 'values': VALIDATION['frequency']},
            }
        }

    def build_one_time_projects_tab(self):
        """
        Tab 24: One-Time Projects
        Project tracking
        """
        headers = ['Project ID', 'Project Name', 'Category', 'Owner', 'Priority',
                   'Status', 'Start Date', 'Target Completion', 'Actual Completion',
                   'Budget', 'Actual Cost', 'Notes']

        sample_projects = [
            ['HP-001', 'Kitchen renovation', 'Home', 'Both', 'P1 - High',
             'In Progress', '=TODAY()-30', '=TODAY()+60', '', '$15,000', '', 'Contractor hired'],
            ['HP-002', 'Garden landscaping', 'Outdoor', 'Gray', 'P2 - Medium',
             'Not Started', '', '=TODAY()+90', '', '$5,000', '', 'Spring project'],
            ['HP-003', 'Home office setup', 'Home', 'Michelle', 'P1 - High',
             'Completed', '=TODAY()-60', '=TODAY()-30', '=TODAY()-35', '$2,000', '$1,850', 'Under budget'],
        ]

        return {
            'tab_name': '🏠 One-Time Projects',
            'headers': headers,
            'data': sample_projects,
            'column_widths': [80, 200, 100, 80, 100, 100, 100, 120, 120, 100, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [6, 7, 8],
                'currency_cols': [9, 10],
            },
            'validation': {
                'owner': {'column': 3, 'values': VALIDATION['task_owner']},
                'priority': {'column': 4, 'values': VALIDATION['priority']},
                'status': {'column': 5, 'values': VALIDATION['status']},
            }
        }

    def build_load_dashboard_tab(self):
        """
        Tab 25: Load Dashboard
        Household load balancing metrics
        """
        headers = ['HOUSEHOLD LOAD DASHBOARD', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['WEEKLY HOURS BY OWNER', '', '', 'TASK DISTRIBUTION', '', ''],
            ['Michelle Total', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Michelle",\'🏠 Recurring Tasks\'!E:E)/60', 'hrs/week', 'Category', 'Michelle', 'Gray'],
            ['Gray Total', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Gray",\'🏠 Recurring Tasks\'!E:E)/60', 'hrs/week', 'Household', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!C:C,"Michelle",\'🏠 Recurring Tasks\'!B:B,"Household")/60', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!C:C,"Gray",\'🏠 Recurring Tasks\'!B:B,"Household")/60'],
            ['Both/Shared', '=SUMIF(\'🏠 Recurring Tasks\'!C:C,"Both",\'🏠 Recurring Tasks\'!E:E)/60', 'hrs/week', 'Finance', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!C:C,"Michelle",\'🏠 Recurring Tasks\'!B:B,"Finance")/60', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!C:C,"Gray",\'🏠 Recurring Tasks\'!B:B,"Finance")/60'],
            ['Total Hours', '=B3+B4+B5', 'hrs/week', 'Outdoor', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!C:C,"Michelle",\'🏠 Recurring Tasks\'!B:B,"Outdoor")/60', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!C:C,"Gray",\'🏠 Recurring Tasks\'!B:B,"Outdoor")/60'],
            ['', '', '', '', '', ''],
            ['LOAD BALANCE', '', '', 'STATUS SUMMARY', '', ''],
            ['Michelle %', '=IFERROR(B3/(B3+B4),0)', '', 'Overdue Tasks', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*Overdue*")', ''],
            ['Gray %', '=IFERROR(B4/(B3+B4),0)', '', 'Due Soon', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*Due Soon*")', ''],
            ['Balance Ratio', '=IF(B9<B10,B9/B10,B10/B9)', '', 'On Track', '=COUNTIF(\'🏠 Recurring Tasks\'!H:H,"*On Track*")', ''],
            ['Balance Status', '=IF(B11>0.8,"🟢 Balanced",IF(B11>0.6,"🟡 Slightly Unbalanced","🔴 Unbalanced"))', '', 'Total Tasks', '=COUNTA(\'🏠 Recurring Tasks\'!A:A)-1', ''],
            ['', '', '', '', '', ''],
            ['MONTHLY SUMMARY', '', '', '', '', ''],
            ['Metric', 'This Month', 'Last Month', 'Change', '', ''],
            ['Tasks Completed', '=COUNTIFS(\'🏠 Recurring Tasks\'!F:F,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', '=COUNTIFS(\'🏠 Recurring Tasks\'!F:F,">="&EOMONTH(TODAY(),-2)+1,\'🏠 Recurring Tasks\'!F:F,"<="&EOMONTH(TODAY(),-1))', '=B16-C16', '', ''],
            ['Hours Invested', '=SUMIFS(\'🏠 Recurring Tasks\'!E:E,\'🏠 Recurring Tasks\'!F:F,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))/60', '', '', '', ''],
        ]

        return {
            'tab_name': '🏠 Load Dashboard',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [150, 100, 80, 150, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 7, 13],
                'percentage_cols': [1],
            }
        }


def get_household_tab_data():
    """Get all household tab configurations without building"""
    return {
        'tabs': [
            '🏠 Recurring Tasks',
            '🏠 One-Time Projects',
            '🏠 Load Dashboard',
        ],
        'count': 3
    }
