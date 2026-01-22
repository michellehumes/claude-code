"""
Goals System Tab Builder (Tabs 19-22)

Tab 19: Michelle's Goals
Tab 20: Gray's Goals
Tab 21: Shared Goals
Tab 22: Goal Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, VALIDATION, MICHELLE_GOALS, GRAY_GOALS, SHARED_GOALS


class GoalsTabBuilder:
    """Build goals system tabs (19-22)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self):
        """Build all goals tabs"""
        results = {}

        results['michelle_goals'] = self.build_michelle_goals_tab()
        results['gray_goals'] = self.build_gray_goals_tab()
        results['shared_goals'] = self.build_shared_goals_tab()
        results['goal_dashboard'] = self.build_goal_dashboard_tab()

        return results

    def build_michelle_goals_tab(self):
        """
        Tab 19: Michelle's Goals
        Personal goals tracking
        """
        headers = ['Goal ID', 'Goal', 'Category', 'Target Date', 'Current Value',
                   'Target Value', '% Complete', 'Status', 'Linked Tasks',
                   'Last Updated', 'Notes']

        data = []
        for i, goal in enumerate(MICHELLE_GOALS):
            goal_id = f'MG-{str(i+1).zfill(3)}'
            row_num = i + 2
            data.append([
                goal_id,
                goal['goal'],
                goal['category'],
                goal['target'],
                goal.get('current_value', ''),
                goal.get('target_value', ''),
                f'={goal["progress"]}%' if isinstance(goal['progress'], int) else f'=IF(F{row_num}>0,E{row_num}/F{row_num},0)',
                goal['status'],
                f'=COUNTIF(\'✅ Master Tasks\'!H:H,A{row_num})',
                '=TODAY()',
                ''
            ])

        return {
            'tab_name': "🎯 Michelle's Goals",
            'headers': headers,
            'data': data,
            'column_widths': [80, 250, 100, 100, 100, 100, 100, 100, 80, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [3, 9],
                'currency_cols': [4, 5],
                'percentage_col': 6,
                'conditional': {
                    'status': {
                        'column': 7,
                        'values': {
                            'On Track': COLORS['positive'],
                            'At Risk': COLORS['warning'],
                            'Blocked': COLORS['negative'],
                            'Completed': COLORS['completed']
                        }
                    }
                }
            },
            'validation': {
                'category': {'column': 2, 'values': VALIDATION['goal_category']},
                'status': {'column': 7, 'values': VALIDATION['goal_status']},
            }
        }

    def build_gray_goals_tab(self):
        """
        Tab 20: Gray's Goals
        Personal goals tracking
        """
        headers = ['Goal ID', 'Goal', 'Category', 'Target Date', 'Current Value',
                   'Target Value', '% Complete', 'Status', 'Linked Tasks',
                   'Last Updated', 'Notes']

        data = []
        for i, goal in enumerate(GRAY_GOALS):
            goal_id = f'GG-{str(i+1).zfill(3)}'
            row_num = i + 2
            data.append([
                goal_id,
                goal['goal'],
                goal['category'],
                goal['target'],
                goal.get('current_value', ''),
                goal.get('target_value', ''),
                f'={goal["progress"]}%' if isinstance(goal['progress'], int) else f'=IF(F{row_num}>0,E{row_num}/F{row_num},0)',
                goal['status'],
                f'=COUNTIF(\'✅ Master Tasks\'!H:H,A{row_num})',
                '=TODAY()',
                ''
            ])

        return {
            'tab_name': "🎯 Gray's Goals",
            'headers': headers,
            'data': data,
            'column_widths': [80, 250, 100, 100, 100, 100, 100, 100, 80, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [3, 9],
                'currency_cols': [4, 5],
                'percentage_col': 6,
            },
            'validation': {
                'category': {'column': 2, 'values': VALIDATION['goal_category']},
                'status': {'column': 7, 'values': VALIDATION['goal_status']},
            }
        }

    def build_shared_goals_tab(self):
        """
        Tab 21: Shared Goals
        Joint household/family goals
        """
        headers = ['Goal ID', 'Goal', 'Category', 'Target Date', 'Current Value',
                   'Target Value', '% Complete', 'Status', 'Primary Owner',
                   'Linked Tasks', 'Last Updated', 'Notes']

        data = []
        for i, goal in enumerate(SHARED_GOALS):
            goal_id = f'SG-{str(i+1).zfill(3)}'
            row_num = i + 2
            data.append([
                goal_id,
                goal['goal'],
                goal['category'],
                goal['target'],
                goal.get('current_value', ''),
                goal.get('target_value', ''),
                f'={goal["progress"]}%' if isinstance(goal['progress'], int) else f'=IF(F{row_num}>0,E{row_num}/F{row_num},0)',
                goal['status'],
                'Both',
                f'=COUNTIF(\'✅ Master Tasks\'!H:H,A{row_num})',
                '=TODAY()',
                ''
            ])

        return {
            'tab_name': '🎯 Shared Goals',
            'headers': headers,
            'data': data,
            'column_widths': [80, 250, 100, 100, 100, 100, 100, 100, 80, 80, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [3, 10],
                'currency_cols': [4, 5],
                'percentage_col': 6,
            },
            'validation': {
                'category': {'column': 2, 'values': VALIDATION['goal_category']},
                'status': {'column': 7, 'values': VALIDATION['goal_status']},
                'owner': {'column': 8, 'values': VALIDATION['task_owner']},
            }
        }

    def build_goal_dashboard_tab(self):
        """
        Tab 22: Goal Dashboard
        Overview of all goals progress
        """
        headers = ['GOAL DASHBOARD', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['MICHELLE\'S GOALS', '', '', 'GRAY\'S GOALS', '', ''],
            ['Total Goals', '=COUNTA(\'🎯 Michelle\'\'s Goals\'!A:A)-1', '', 'Total Goals', '=COUNTA(\'🎯 Gray\'\'s Goals\'!A:A)-1', ''],
            ['On Track', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"On Track")', '', 'On Track', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"On Track")', ''],
            ['At Risk', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"At Risk")', '', 'At Risk', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"At Risk")', ''],
            ['Completed', '=COUNTIF(\'🎯 Michelle\'\'s Goals\'!H:H,"Completed")', '', 'Completed', '=COUNTIF(\'🎯 Gray\'\'s Goals\'!H:H,"Completed")', ''],
            ['Avg Progress', '=AVERAGE(\'🎯 Michelle\'\'s Goals\'!G:G)', '', 'Avg Progress', '=AVERAGE(\'🎯 Gray\'\'s Goals\'!G:G)', ''],
            ['', '', '', '', '', ''],
            ['SHARED GOALS', '', '', 'GOALS DUE THIS QUARTER', '', ''],
            ['Total Goals', '=COUNTA(\'🎯 Shared Goals\'!A:A)-1', '', 'Goal', 'Due Date', 'Status'],
            ['On Track', '=COUNTIF(\'🎯 Shared Goals\'!H:H,"On Track")', '', '(See Goals tabs for details)', '', ''],
            ['At Risk', '=COUNTIF(\'🎯 Shared Goals\'!H:H,"At Risk")', '', '', '', ''],
            ['Completed', '=COUNTIF(\'🎯 Shared Goals\'!H:H,"Completed")', '', '', '', ''],
            ['Avg Progress', '=AVERAGE(\'🎯 Shared Goals\'!G:G)', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['PROGRESS BY CATEGORY', '', '', '', '', ''],
            ['Category', 'Michelle', 'Gray', 'Shared', 'Overall', ''],
            ['Career', '=AVERAGEIF(\'🎯 Michelle\'\'s Goals\'!C:C,"Career",\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Gray\'\'s Goals\'!C:C,"Career",\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Shared Goals\'!C:C,"Career",\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B18:D18)', ''],
            ['Health', '=AVERAGEIF(\'🎯 Michelle\'\'s Goals\'!C:C,"Health",\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Gray\'\'s Goals\'!C:C,"Health",\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Shared Goals\'!C:C,"Health",\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B19:D19)', ''],
            ['Finance', '=AVERAGEIF(\'🎯 Michelle\'\'s Goals\'!C:C,"Finance",\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Gray\'\'s Goals\'!C:C,"Finance",\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Shared Goals\'!C:C,"Finance",\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B20:D20)', ''],
            ['Personal', '=AVERAGEIF(\'🎯 Michelle\'\'s Goals\'!C:C,"Personal",\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Gray\'\'s Goals\'!C:C,"Personal",\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Shared Goals\'!C:C,"Personal",\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B21:D21)', ''],
            ['Business', '=AVERAGEIF(\'🎯 Michelle\'\'s Goals\'!C:C,"Business",\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Gray\'\'s Goals\'!C:C,"Business",\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Shared Goals\'!C:C,"Business",\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B22:D22)', ''],
            ['Family', '=AVERAGEIF(\'🎯 Michelle\'\'s Goals\'!C:C,"Family",\'🎯 Michelle\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Gray\'\'s Goals\'!C:C,"Family",\'🎯 Gray\'\'s Goals\'!G:G)', '=AVERAGEIF(\'🎯 Shared Goals\'!C:C,"Family",\'🎯 Shared Goals\'!G:G)', '=AVERAGE(B23:D23)', ''],
        ]

        return {
            'tab_name': '🎯 Goal Dashboard',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [150, 100, 100, 150, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 8, 15],
                'percentage_cols': [1, 4],
            }
        }


def get_goals_tab_data():
    """Get all goals tab configurations without building"""
    return {
        'tabs': [
            "🎯 Michelle's Goals",
            "🎯 Gray's Goals",
            '🎯 Shared Goals',
            '🎯 Goal Dashboard',
        ],
        'count': 4
    }
