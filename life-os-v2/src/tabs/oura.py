"""
Oura Ring Integration Tab Builder (Tabs 47-54)

Tab 47: Oura Sleep Tracker
Tab 48: Oura Activity Tracker
Tab 49: Oura Readiness Tracker
Tab 50: Oura Cycle Integration
Tab 51: Oura Temperature
Tab 52: Oura Heart Rate
Tab 53: Oura Stress Tracker
Tab 54: Oura Health Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS


class OuraTabBuilder:
    """Build Oura Ring integration tabs (47-54)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self, oura_data=None):
        """Build all Oura tabs"""
        results = {}

        results['sleep'] = self.build_sleep_tracker_tab(oura_data)
        results['activity'] = self.build_activity_tracker_tab(oura_data)
        results['readiness'] = self.build_readiness_tracker_tab(oura_data)
        results['cycle'] = self.build_cycle_integration_tab(oura_data)
        results['temperature'] = self.build_temperature_tab(oura_data)
        results['heart_rate'] = self.build_heart_rate_tab(oura_data)
        results['stress'] = self.build_stress_tracker_tab(oura_data)
        results['dashboard'] = self.build_health_dashboard_tab()

        return results

    def build_sleep_tracker_tab(self, oura_data=None):
        """
        Tab 47: Oura Sleep Tracker
        Daily sleep data from Oura Ring
        """
        headers = ['Date', 'Sleep Score', 'Total Sleep (hrs)', 'Deep Sleep (min)',
                   'REM Sleep (min)', 'Light Sleep (min)', 'Sleep Efficiency %',
                   'Sleep Latency (min)', 'Restfulness Score', 'Timing Score',
                   '7-Day Avg', 'Trend', 'Notes']

        # Use provided data or generate sample
        if oura_data and hasattr(oura_data, 'get_sleep_data'):
            data = oura_data.get_sleep_data()
        else:
            from src.data_processors.oura import OuraDataProcessor
            data = OuraDataProcessor.generate_sample_sleep_data(30)

        # Add formula columns
        for i, row in enumerate(data):
            row_num = i + 2
            # 7-Day Average
            row.append(f'=IF(ROW()>=8,AVERAGE(B{row_num-6}:B{row_num}),"")')
            # Trend
            row.append(f'=IF(ROW()>=3,IF(B{row_num}>B{row_num-1},"↑",IF(B{row_num}<B{row_num-1},"↓","→")),"")')

        return {
            'tab_name': '🔴 Oura Sleep Tracker',
            'headers': headers,
            'data': data,
            'column_widths': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 60, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'percentage_col': 6,
                'conditional': {
                    'sleep_score': {
                        'column': 1,
                        'thresholds': [45, 60, 75],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   {"red": 0.95, "green": 0.76, "blue": 0.20}, COLORS['positive']]
                    },
                    'efficiency': {
                        'column': 6,
                        'thresholds': [0.7, 0.8, 0.9],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   {"red": 0.95, "green": 0.76, "blue": 0.20}, COLORS['positive']]
                    }
                }
            }
        }

    def build_activity_tracker_tab(self, oura_data=None):
        """
        Tab 48: Oura Activity Tracker
        Daily activity data from Oura Ring
        """
        headers = ['Date', 'Activity Score', 'Steps', 'Active Calories', 'Total Calories',
                   'Distance (m)', 'High Activity (min)', 'Medium Activity (min)',
                   'Low Activity (min)', 'Sedentary (hrs)', 'Inactivity Alerts',
                   'Meet Targets %', 'Move Hourly %', 'Training Volume', '7-Day Avg Steps', 'Trend']

        # Use provided data or generate sample
        if oura_data and hasattr(oura_data, 'get_activity_data'):
            data = oura_data.get_activity_data()
        else:
            from src.data_processors.oura import OuraDataProcessor
            data = OuraDataProcessor.generate_sample_activity_data(30)

        # Add formula columns
        for i, row in enumerate(data):
            row_num = i + 2
            # 7-Day Avg Steps
            row.append(f'=IF(ROW()>=8,AVERAGE(C{row_num-6}:C{row_num}),"")')
            # Trend
            row.append(f'=IF(ROW()>=3,IF(B{row_num}>B{row_num-1},"↑",IF(B{row_num}<B{row_num-1},"↓","→")),"")')

        return {
            'tab_name': '🔴 Oura Activity Tracker',
            'headers': headers,
            'data': data,
            'column_widths': [100, 100, 80, 100, 100, 100, 100, 100, 100, 80, 80, 80, 80, 80, 100, 60],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'conditional': {
                    'steps': {
                        'column': 2,
                        'thresholds': [5000, 7500, 10000],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   {"red": 0.95, "green": 0.76, "blue": 0.20}, COLORS['positive']]
                    },
                    'activity_score': {
                        'column': 1,
                        'thresholds': [55, 70, 85],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   {"red": 0.95, "green": 0.76, "blue": 0.20}, COLORS['positive']]
                    }
                }
            }
        }

    def build_readiness_tracker_tab(self, oura_data=None):
        """
        Tab 49: Oura Readiness Tracker
        Daily readiness scores from Oura Ring
        """
        headers = ['Date', 'Readiness Score', 'Recovery Index', 'Sleep Balance',
                   'Prev Day Activity', 'Activity Balance', 'Body Temperature',
                   'Resting Heart Rate', 'HRV Balance', '7-Day Avg', 'Trend', 'Notes']

        # Use provided data or generate sample
        if oura_data and hasattr(oura_data, 'get_readiness_data'):
            data = oura_data.get_readiness_data()
        else:
            from src.data_processors.oura import OuraDataProcessor
            data = OuraDataProcessor.generate_sample_readiness_data(30)

        # Add formula columns
        for i, row in enumerate(data):
            row_num = i + 2
            # 7-Day Avg
            row.append(f'=IF(ROW()>=8,AVERAGE(B{row_num-6}:B{row_num}),"")')
            # Trend
            row.append(f'=IF(ROW()>=3,IF(B{row_num}>B{row_num-1},"↑",IF(B{row_num}<B{row_num-1},"↓","→")),"")')

        return {
            'tab_name': '🔴 Oura Readiness Tracker',
            'headers': headers,
            'data': data,
            'column_widths': [100, 120, 100, 100, 100, 100, 100, 100, 100, 100, 60, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'conditional': {
                    'readiness_score': {
                        'column': 1,
                        'thresholds': [55, 70, 85],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   {"red": 0.95, "green": 0.76, "blue": 0.20}, COLORS['positive']]
                    }
                }
            }
        }

    def build_cycle_integration_tab(self, oura_data=None):
        """
        Tab 50: Oura Cycle Integration
        Sync Oura cycle data with manual tracking
        """
        headers = ['Date', 'Day of Cycle', 'Cycle Phase', 'Oura Cycle ID',
                   'Manual Cycle #', 'Period Confirmed', 'Ovulation Confirmed',
                   'Discrepancy Notes']

        # Use provided data or generate sample
        if oura_data and hasattr(oura_data, 'get_cycle_data'):
            data = oura_data.get_cycle_data()
        else:
            from src.data_processors.oura import OuraDataProcessor
            data = OuraDataProcessor.generate_sample_cycle_data(90)

        return {
            'tab_name': '🔴 Oura Cycle Integration',
            'headers': headers,
            'data': data,
            'column_widths': [100, 100, 120, 120, 100, 100, 120, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'conditional': {
                    'phase_follicular': {
                        'column': 2,
                        'value': 'Follicular',
                        'color': COLORS['follicular']
                    },
                    'phase_luteal': {
                        'column': 2,
                        'value': 'Luteal',
                        'color': COLORS['luteal']
                    }
                }
            }
        }

    def build_temperature_tab(self, oura_data=None):
        """
        Tab 51: Oura Temperature
        Daily temperature data for fertility tracking
        """
        headers = ['Date', 'Avg Nighttime Temp (°C)', 'Deviation from Baseline',
                   'Temp Trend', 'Cycle Day', 'Cycle Phase', 'Predicted Ovulation Day',
                   'BBT Shift Detected', 'Fever Alert', 'Notes']

        # Generate sample temperature data
        sample_data = []
        baseline = 36.5
        for i in range(30):
            row_num = i + 2
            # Simulate temperature pattern with slight variations
            import random
            temp_variation = random.uniform(-0.3, 0.4)
            temp = round(baseline + temp_variation, 2)
            deviation = round(temp - baseline, 2)

            sample_data.append([
                f'=TODAY()-{29-i}',
                temp,
                deviation,
                f'=IF(ROW()>=3,IF(B{row_num}>B{row_num-1}+0.1,"↑",IF(B{row_num}<B{row_num-1}-0.1,"↓","→")),"")',
                '',  # Cycle Day - linked
                '',  # Cycle Phase - linked
                '',  # Predicted Ovulation
                f'=IF(C{row_num}>=0.2,"Y","N")',  # BBT Shift
                f'=IF(B{row_num}>=37.5,"Y","N")',  # Fever Alert
                ''
            ])

        return {
            'tab_name': '🔴 Oura Temperature',
            'headers': headers,
            'data': sample_data,
            'column_widths': [100, 150, 150, 100, 80, 100, 150, 100, 80, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'conditional': {
                    'deviation': {
                        'column': 2,
                        'thresholds': [-0.5, -0.3, 0.3, 0.5],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   COLORS['positive'], COLORS['warning'], COLORS['negative']]
                    }
                }
            }
        }

    def build_heart_rate_tab(self, oura_data=None):
        """
        Tab 52: Oura Heart Rate
        Daily heart rate summaries
        """
        headers = ['Date', 'Avg Resting HR (bpm)', 'Lowest Nighttime HR', 'Avg Daytime HR',
                   'Max HR', 'HRV Score', 'HRV Trend', 'Cycle Day', 'Stress Level', 'Notes']

        # Generate sample HR data
        sample_data = []
        for i in range(30):
            row_num = i + 2
            import random
            resting_hr = random.randint(55, 75)
            lowest_hr = resting_hr - random.randint(5, 15)
            avg_daytime = resting_hr + random.randint(10, 25)
            max_hr = avg_daytime + random.randint(30, 80)
            hrv = random.randint(25, 65)

            sample_data.append([
                f'=TODAY()-{29-i}',
                resting_hr,
                lowest_hr,
                avg_daytime,
                max_hr,
                hrv,
                f'=IF(ROW()>=3,IF(F{row_num}>F{row_num-1}+2,"↑",IF(F{row_num}<F{row_num-1}-2,"↓","→")),"")',
                '',  # Cycle Day
                '',  # Stress Level
                ''
            ])

        return {
            'tab_name': '🔴 Oura Heart Rate',
            'headers': headers,
            'data': sample_data,
            'column_widths': [100, 130, 130, 120, 80, 80, 80, 80, 100, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'conditional': {
                    'resting_hr': {
                        'column': 1,
                        'thresholds': [45, 55, 75, 85],
                        'colors': [COLORS['warning'], COLORS['positive'],
                                   COLORS['positive'], COLORS['warning'], COLORS['negative']]
                    },
                    'hrv': {
                        'column': 5,
                        'thresholds': [30, 50],
                        'colors': [COLORS['negative'], COLORS['warning'], COLORS['positive']]
                    }
                }
            }
        }

    def build_stress_tracker_tab(self, oura_data=None):
        """
        Tab 53: Oura Stress Tracker
        Daily stress tracking
        """
        headers = ['Date', 'Daily Stress Score', 'Daytime Stress', 'Stress Duration (min)',
                   'Recovery Time (min)', 'Resilience Score', 'Stressful Periods',
                   'Calm Periods', 'Notes', 'Triggers']

        # Generate sample stress data
        sample_data = []
        for i in range(30):
            row_num = i + 2
            import random
            stress_score = random.randint(10, 80)
            if stress_score > 80:
                stress_level = 'Very High'
            elif stress_score > 50:
                stress_level = 'High'
            elif stress_score > 20:
                stress_level = 'Medium'
            else:
                stress_level = 'Low'

            sample_data.append([
                f'=TODAY()-{29-i}',
                stress_score,
                stress_level,
                random.randint(30, 180),
                random.randint(60, 240),
                random.randint(40, 90),
                random.randint(1, 5),
                random.randint(3, 10),
                '',
                ''
            ])

        return {
            'tab_name': '🔴 Oura Stress Tracker',
            'headers': headers,
            'data': sample_data,
            'column_widths': [100, 120, 100, 120, 120, 100, 100, 100, 200, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'conditional': {
                    'stress_score': {
                        'column': 1,
                        'thresholds': [20, 50, 80],
                        'colors': [COLORS['positive'], {"red": 0.95, "green": 0.76, "blue": 0.20},
                                   COLORS['warning'], COLORS['negative']]
                    },
                    'resilience': {
                        'column': 5,
                        'thresholds': [25, 50, 75],
                        'colors': [COLORS['negative'], COLORS['warning'],
                                   {"red": 0.95, "green": 0.76, "blue": 0.20}, COLORS['positive']]
                    }
                }
            }
        }

    def build_health_dashboard_tab(self):
        """
        Tab 54: Oura Health Dashboard
        Master health view integrating all Oura data
        """
        headers = ['OURA HEALTH DASHBOARD', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ["TODAY'S SNAPSHOT", '', '', 'WEEKLY OVERVIEW', '', ''],
            ['Sleep Score', '=\'🔴 Oura Sleep Tracker\'!B2', '=IF(B3>=85,"🟢",IF(B3>=70,"🟡",IF(B3>=55,"🟠","🔴")))', 'Avg Sleep Score (7d)', '=AVERAGE(\'🔴 Oura Sleep Tracker\'!B2:B8)', ''],
            ['Readiness Score', '=\'🔴 Oura Readiness Tracker\'!B2', '=IF(B4>=85,"🟢",IF(B4>=70,"🟡",IF(B4>=55,"🟠","🔴")))', 'Total Steps (7d)', '=SUM(\'🔴 Oura Activity Tracker\'!C2:C8)', ''],
            ['Activity Score', '=\'🔴 Oura Activity Tracker\'!B2', '=IF(B5>=85,"🟢",IF(B5>=70,"🟡",IF(B5>=55,"🟠","🔴")))', 'Avg Readiness (7d)', '=AVERAGE(\'🔴 Oura Readiness Tracker\'!B2:B8)', ''],
            ['Current Cycle Day', '=\'🔴 Oura Cycle Integration\'!B2', '', 'Sleep Debt', '=7*8-SUM(\'🔴 Oura Sleep Tracker\'!C2:C8)', 'hrs'],
            ['Cycle Phase', '=\'🔴 Oura Cycle Integration\'!C2', '', 'Recovery Status', '=IF(E5>=85,"Optimal",IF(E5>=70,"Good","Recovery Needed"))', ''],
            ['BBT Reading', '=\'🔴 Oura Temperature\'!B2', '°C', 'Activity Consistency', '=STDEV(\'🔴 Oura Activity Tracker\'!B2:B8)', ''],
            ['Resting HR', '=\'🔴 Oura Heart Rate\'!B2', 'bpm', '', '', ''],
            ['HRV', '=\'🔴 Oura Heart Rate\'!F2', '', '', '', ''],
            ['Stress Level', '=\'🔴 Oura Stress Tracker\'!C2', '', '', '', ''],
            ['Health Status', '=IF(AVERAGE(B3:B5)>=85,"🟢 Optimal",IF(AVERAGE(B3:B5)>=70,"🟡 Good",IF(AVERAGE(B3:B5)>=55,"🟠 Pay Attention","🔴 Rest Needed")))', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['MONTHLY TRENDS', '', '', 'ALERTS & INSIGHTS', '', ''],
            ['Avg Cycle Length', '=AVERAGE(\'🌸 Cycle Tracking\'!D:D)', 'days', 'Predicted Ovulation', '=MAX(\'🌸 Cycle Tracking\'!B:B)+14', ''],
            ['Temp Pattern', '=IF(AVERAGE(\'🔴 Oura Temperature\'!C2:C14)>0.2,"Post-Ovulation","Pre-Ovulation")', '', 'Days Until Ovulation', '=E15-TODAY()', 'days'],
            ['Ovulation Accuracy', '', '%', 'Low Readiness Alert', '=IF(B4<55,"⚠️ Rest recommended","")', ''],
            ['Sleep Quality Trend', '=IF(E3>AVERAGE(\'🔴 Oura Sleep Tracker\'!B9:B15),"Improving","Declining")', '', 'Sleep Declining', '=IF(E3<AVERAGE(\'🔴 Oura Sleep Tracker\'!B9:B15)*0.9,"⚠️ Sleep quality declining","")', ''],
            ['Activity Trend', '=IF(AVERAGE(\'🔴 Oura Activity Tracker\'!C2:C7)>AVERAGE(\'🔴 Oura Activity Tracker\'!C8:C14),"↑","↓")', '', 'Below Step Goal', '=IF(E4<70000,"⚠️ Weekly steps below target","")', ''],
            ['Stress Pattern', '=IF(AVERAGE(\'🔴 Oura Stress Tracker\'!B2:B7)<AVERAGE(\'🔴 Oura Stress Tracker\'!B8:B14),"Improving","Increasing")', '', 'Unusual HR', '=IF(OR(B9>80,B9<50),"⚠️ Unusual resting HR detected","")', ''],
            ['', '', '', '', '', ''],
            ['INTEGRATION SUMMARY', '', '', '', '', ''],
            ['Days of Sleep Data', '=COUNTA(\'🔴 Oura Sleep Tracker\'!A:A)-1', '', '', '', ''],
            ['Days of Activity Data', '=COUNTA(\'🔴 Oura Activity Tracker\'!A:A)-1', '', '', '', ''],
            ['Days of Cycle Data', '=COUNTA(\'🔴 Oura Cycle Integration\'!A:A)-1', '', '', '', ''],
            ['Last Sync', '=MAX(\'🔴 Oura Sleep Tracker\'!A:A)', '', '', '', ''],
            ['Data Quality Score', '=IFERROR((B23+B24+B25)/(30*3)*100,0)', '%', '', '', ''],
            ['Manual vs Oura Discrepancies', '=COUNTIF(\'🔴 Oura Cycle Integration\'!H:H,"<>")', '', '', '', ''],
        ]

        return {
            'tab_name': '🔴 Oura Health Dashboard',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [180, 120, 60, 180, 150, 60],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 13, 21],
            }
        }


def get_oura_tab_data():
    """Get all Oura tab configurations without building"""
    return {
        'tabs': [
            '🔴 Oura Sleep Tracker',
            '🔴 Oura Activity Tracker',
            '🔴 Oura Readiness Tracker',
            '🔴 Oura Cycle Integration',
            '🔴 Oura Temperature',
            '🔴 Oura Heart Rate',
            '🔴 Oura Stress Tracker',
            '🔴 Oura Health Dashboard',
        ],
        'count': 8
    }
