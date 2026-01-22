"""
Fertility & Health Tab Builder (Tabs 35-40)

Tab 35: Cycle Tracking
Tab 36: Daily Log
Tab 37: DPO Tracker
Tab 38: Appointments
Tab 39: Supplements
Tab 40: Monthly Summary
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, VALIDATION, SUPPLEMENTS


class FertilityTabBuilder:
    """Build fertility & health tabs (35-40)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self):
        """Build all fertility tabs"""
        results = {}

        results['cycle_tracking'] = self.build_cycle_tracking_tab()
        results['daily_log'] = self.build_daily_log_tab()
        results['dpo_tracker'] = self.build_dpo_tracker_tab()
        results['appointments'] = self.build_appointments_tab()
        results['supplements'] = self.build_supplements_tab()
        results['monthly_summary'] = self.build_monthly_summary_tab()

        return results

    def build_cycle_tracking_tab(self):
        """
        Tab 35: Cycle Tracking
        Menstrual cycle history
        """
        headers = ['Cycle #', 'Cycle Start Date', 'Period End Date', 'Cycle Length',
                   'Period Length', 'Ovulation Date (Est)', 'Ovulation Confirmed',
                   'Ovulation Method', 'Luteal Phase Length', 'Cycle Notes', 'Symptoms']

        sample_data = []
        for i in range(1, 7):
            row_num = i + 1
            sample_data.append([
                i,
                '',  # Cycle Start Date
                '',  # Period End Date
                f'=IF(AND(B{row_num}<>"",B{row_num+1}<>""),B{row_num+1}-B{row_num},"")',  # Cycle Length
                f'=IF(AND(B{row_num}<>"",C{row_num}<>""),C{row_num}-B{row_num}+1,"")',  # Period Length
                f'=IF(B{row_num}<>"",B{row_num}+14,"")',  # Ovulation Est
                '',  # Ovulation Confirmed
                '',  # Method
                f'=IF(AND(D{row_num}<>"",F{row_num}<>""),D{row_num}-(F{row_num}-B{row_num}),"")',  # Luteal Phase
                '',  # Notes
                ''   # Symptoms
            ])

        return {
            'tab_name': '🌸 Cycle Tracking',
            'headers': headers,
            'data': sample_data,
            'column_widths': [80, 120, 120, 100, 100, 130, 120, 120, 120, 200, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [1, 2, 5],
            },
            'validation': {
                'confirmed': {'column': 6, 'values': ['Yes', 'No', '']},
                'method': {'column': 7, 'values': ['OPK', 'BBT', 'Cervical Mucus', 'Multiple', 'Oura', '']},
            }
        }

    def build_daily_log_tab(self):
        """
        Tab 36: Daily Log
        Daily fertility tracking
        """
        headers = ['Date', 'Cycle Day', 'BBT (°F)', 'Cervical Mucus', 'OPK Result',
                   'Cervix Position', 'Energy (1-10)', 'Mood', 'Symptoms',
                   'Intimate Activity', 'Notes']

        # Generate 30 days of template rows
        sample_data = []
        for i in range(30):
            row_num = i + 2
            sample_data.append([
                f'=TODAY()-{29-i}',
                '',  # Cycle Day - linked to Cycle Tracking
                '',  # BBT - can be auto-populated from Oura
                '',  # Cervical Mucus
                '',  # OPK
                '',  # Cervix
                '',  # Energy
                '',  # Mood
                '',  # Symptoms
                '',  # Activity
                ''   # Notes
            ])

        return {
            'tab_name': '🌸 Daily Log',
            'headers': headers,
            'data': sample_data,
            'column_widths': [100, 80, 80, 120, 100, 100, 80, 100, 200, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
            },
            'validation': {
                'cervical_mucus': {'column': 3, 'values': VALIDATION['cervical_mucus']},
                'opk': {'column': 4, 'values': ['Positive', 'Negative', 'Almost Positive', '']},
                'cervix': {'column': 5, 'values': ['Low/Firm/Closed', 'Medium', 'High/Soft/Open', '']},
                'energy': {'column': 6, 'type': 'number', 'min': 1, 'max': 10},
            }
        }

    def build_dpo_tracker_tab(self):
        """
        Tab 37: DPO Tracker
        Days Past Ovulation tracking
        """
        headers = ['Cycle #', 'Ovulation Date', 'DPO', 'Date', 'Symptoms',
                   'BBT', 'Test Taken', 'Test Result', 'Notes']

        # Template for DPO 1-16 tracking
        sample_data = []
        for dpo in range(1, 17):
            sample_data.append([
                '',  # Cycle # - linked
                '',  # Ovulation Date - linked
                dpo,
                f'=IF(B{dpo+1}<>"",B{dpo+1}+C{dpo+1},"")',  # Date formula
                '',  # Symptoms
                '',  # BBT
                False,  # Test Taken
                '',  # Test Result
                ''   # Notes
            ])

        return {
            'tab_name': '🌸 DPO Tracker',
            'headers': headers,
            'data': sample_data,
            'column_widths': [80, 120, 60, 100, 250, 80, 80, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [1, 3],
                'checkbox_col': 6,
            },
            'validation': {
                'test_result': {'column': 7, 'values': ['Positive', 'Negative', 'Invalid', 'Indent', 'Evap', '']},
            }
        }

    def build_appointments_tab(self):
        """
        Tab 38: Appointments
        Medical appointments tracking
        """
        headers = ['Date', 'Time', 'Provider', 'Type', 'Reason', 'Tests Ordered',
                   'Results', 'Next Steps', 'Follow-up Date', 'Notes']

        sample_appointments = [
            ['', '', 'Dr. Smith', 'OB/GYN', 'Annual exam', '', '', '', '', ''],
            ['', '', 'Dr. Johnson', 'Fertility Specialist', 'Initial consultation', '', '', '', '', ''],
            ['', '', '', 'Lab', 'Bloodwork', 'AMH, FSH, TSH', '', '', '', ''],
        ]

        return {
            'tab_name': '🌸 Appointments',
            'headers': headers,
            'data': sample_appointments,
            'column_widths': [100, 80, 150, 120, 200, 150, 200, 200, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [0, 8],
            },
            'validation': {
                'type': {'column': 3, 'values': VALIDATION['appointment_type']},
            }
        }

    def build_supplements_tab(self):
        """
        Tab 39: Supplements
        Supplement tracking
        """
        headers = ['Supplement Name', 'Dosage', 'Frequency', 'Started Date',
                   'Purpose', 'Prescribed By', 'Status', 'Notes']

        data = []
        for supp in SUPPLEMENTS:
            data.append([
                supp['name'],
                supp['dosage'],
                supp['frequency'],
                supp['started'],
                supp['purpose'],
                supp['prescribed_by'],
                supp['status'],
                ''
            ])

        return {
            'tab_name': '🌸 Supplements',
            'headers': headers,
            'data': data,
            'column_widths': [180, 100, 100, 100, 200, 120, 80, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 3,
            },
            'validation': {
                'frequency': {'column': 2, 'values': ['Daily', 'Twice Daily', 'Weekly', 'As Needed']},
                'status': {'column': 6, 'values': ['Active', 'Paused', 'Discontinued']},
            }
        }

    def build_monthly_summary_tab(self):
        """
        Tab 40: Monthly Summary
        Fertility metrics overview
        """
        headers = ['FERTILITY MONTHLY SUMMARY', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['CYCLE METRICS (Last 3 Cycles)', '', '', 'BBT ANALYSIS', '', ''],
            ['Average Cycle Length', '=AVERAGE(\'🌸 Cycle Tracking\'!D2:D4)', 'days', 'Follicular Phase Avg', '', ''],
            ['Average Luteal Phase', '=AVERAGE(\'🌸 Cycle Tracking\'!I2:I4)', 'days', 'Luteal Phase Avg', '', ''],
            ['Average Period Length', '=AVERAGE(\'🌸 Cycle Tracking\'!E2:E4)', 'days', 'Temperature Shift', '', ''],
            ['Cycle Regularity', '=STDEV(\'🌸 Cycle Tracking\'!D2:D4)', 'std dev', 'Avg Shift Amount', '', ''],
            ['', '', '', '', '', ''],
            ['OVULATION TRACKING', '', '', 'SUPPLEMENT COMPLIANCE', '', ''],
            ['Confirmed Ovulations', '=COUNTIF(\'🌸 Cycle Tracking\'!G:G,"Yes")', '', 'Active Supplements', '=COUNTIF(\'🌸 Supplements\'!G:G,"Active")', ''],
            ['Prediction Accuracy', '', '%', 'Days Taking', '=DATEDIF(MIN(\'🌸 Supplements\'!D:D),TODAY(),"D")', ''],
            ['Avg Ovulation Day', '=AVERAGE(ARRAYFORMULA(\'🌸 Cycle Tracking\'!F2:F10-\'🌸 Cycle Tracking\'!B2:B10))', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['UPCOMING', '', '', 'OURA INTEGRATION', '', ''],
            ['Next Period (Est)', '=MAX(\'🌸 Cycle Tracking\'!B:B)+AVERAGE(\'🌸 Cycle Tracking\'!D:D)', '', 'Sleep Score Avg', '=AVERAGE(\'🔴 Oura Sleep Tracker\'!B:B)', ''],
            ['Next Ovulation (Est)', '=MAX(\'🌸 Cycle Tracking\'!B:B)+AVERAGE(\'🌸 Cycle Tracking\'!D:D)+14', '', 'Readiness Avg', '=AVERAGE(\'🔴 Oura Readiness Tracker\'!B:B)', ''],
            ['Fertile Window Start', '=N14-5', '', 'Temp Trend', '=\'🔴 Oura Temperature\'!D2', ''],
            ['Fertile Window End', '=N14+1', '', 'Current Cycle Day', '=\'🔴 Oura Cycle Integration\'!B2', ''],
            ['', '', '', '', '', ''],
            ['APPOINTMENTS UPCOMING', '', '', '', '', ''],
            ['Date', 'Provider', 'Type', 'Reason', '', ''],
            ['=FILTER(\'🌸 Appointments\'!A:A,\'🌸 Appointments\'!A:A>=TODAY())', '', '', '', '', ''],
        ]

        return {
            'tab_name': '🌸 Monthly Summary',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [180, 120, 80, 180, 120, 80],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 7, 12, 18],
                'date_cols': [],
            }
        }


def get_fertility_tab_data():
    """Get all fertility tab configurations without building"""
    return {
        'tabs': [
            '🌸 Cycle Tracking',
            '🌸 Daily Log',
            '🌸 DPO Tracker',
            '🌸 Appointments',
            '🌸 Supplements',
            '🌸 Monthly Summary',
        ],
        'count': 6
    }
