"""
Job Search System Tab Builder (Tabs 12-18)

Tab 12: Job Pipeline
Tab 13: Applications Tracker
Tab 14: Recruiter CRM
Tab 15: Interview Tracker
Tab 16: Follow-Ups
Tab 17: Offer Comparison
Tab 18: Job Search Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, VALIDATION


class JobSearchTabBuilder:
    """Build job search system tabs (12-18)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self):
        """Build all job search tabs"""
        results = {}

        results['pipeline'] = self.build_pipeline_tab()
        results['applications'] = self.build_applications_tab()
        results['recruiter_crm'] = self.build_recruiter_crm_tab()
        results['interviews'] = self.build_interview_tracker_tab()
        results['follow_ups'] = self.build_follow_ups_tab()
        results['offers'] = self.build_offer_comparison_tab()
        results['dashboard'] = self.build_job_search_dashboard_tab()

        return results

    def build_pipeline_tab(self):
        """
        Tab 12: Job Pipeline
        Main job tracking system
        """
        headers = ['Pipeline ID', 'Date Added', 'Company', 'Role', 'Location',
                   'Remote/Hybrid/On-site', 'Salary Range', 'Current Stage', 'Next Action',
                   'Next Action Date', 'Days Since Last Action', 'Application Link',
                   'Priority', 'Interest Level', 'Referral Contact', 'Status', 'Notes']

        sample_data = [
            ['JP-001', '=TODAY()-14', 'Anthropic', 'Senior Product Manager', 'San Francisco, CA',
             'Remote', '$150K-$180K', 'Applied', 'Follow up on application', '=TODAY()+3',
             '=TODAY()-B2', 'https://anthropic.com/careers', 'P1 - High', '9/10', '',
             'Active', 'Dream company - AI safety focus'],
            ['JP-002', '=TODAY()-7', 'Stripe', 'Product Lead', 'New York, NY',
             'Hybrid', '$160K-$200K', 'Phone Screen', 'Prepare for technical interview', '=TODAY()+5',
             '=TODAY()-B3', 'https://stripe.com/jobs', 'P1 - High', '8/10', 'John Smith',
             'Active', 'Referred by former colleague'],
            ['JP-003', '=TODAY()-21', 'Notion', 'Group PM', 'Remote',
             'Remote', '$140K-$170K', 'Interview', 'Send thank you notes', '=TODAY()',
             '=TODAY()-B4', 'https://notion.so/careers', 'P0 - Critical', '10/10', '',
             'Active', 'Final round scheduled next week'],
        ]

        return {
            'tab_name': '💼 Job Pipeline',
            'headers': headers,
            'data': sample_data,
            'column_widths': [80, 100, 150, 180, 150, 100, 120, 120, 200, 100, 80, 200, 100, 80, 150, 80, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [1, 9],
                'conditional': {
                    'days_stale': {
                        'column': 10,
                        'thresholds': [7, 14],
                        'colors': [COLORS['positive'], COLORS['warning'], COLORS['negative']]
                    }
                }
            },
            'validation': {
                'location_type': {'column': 5, 'values': VALIDATION['location_type']},
                'stage': {'column': 7, 'values': VALIDATION['job_stage']},
                'priority': {'column': 12, 'values': VALIDATION['priority']},
            }
        }

    def build_applications_tab(self):
        """
        Tab 13: Applications Tracker
        Detailed application tracking
        """
        headers = ['Pipeline ID', 'Date Submitted', 'Resume Version', 'Cover Letter Type',
                   'Application Method', 'Time Invested (min)', 'Confirmation Received',
                   'Status Check Date', 'Response Received', 'Days to Response', 'Outcome', 'Notes']

        sample_data = [
            ['JP-001', '=TODAY()-14', 'v3.2 - PM Focus', 'Customized', 'Direct',
             45, True, '=TODAY()-7', False, '', 'Pending', ''],
            ['JP-002', '=TODAY()-7', 'v3.2 - PM Focus', 'Template', 'Referral',
             30, True, '', True, 3, 'Interview', 'Fast response due to referral'],
            ['JP-003', '=TODAY()-21', 'v3.1 - Strategy', 'Customized', 'Direct',
             60, True, '=TODAY()-14', True, 5, 'Interview', ''],
        ]

        return {
            'tab_name': '💼 Applications Tracker',
            'headers': headers,
            'data': sample_data,
            'column_widths': [80, 120, 150, 120, 120, 100, 100, 120, 100, 100, 100, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [1, 7],
                'checkbox_cols': [6, 8],
            }
        }

    def build_recruiter_crm_tab(self):
        """
        Tab 14: Recruiter CRM
        Contact management for recruiters
        """
        headers = ['Contact Type', 'Name', 'Company', 'Email', 'Phone', 'LinkedIn',
                   'First Contact Date', 'Last Contact Date', 'Next Follow-up',
                   'Relationship Strength', 'Active Opportunities', 'Notes']

        sample_data = [
            ['Internal Recruiter', 'Sarah Johnson', 'Stripe', 'sarah@stripe.com', '',
             'linkedin.com/in/sarahjohnson', '=TODAY()-7', '=TODAY()-2', '=TODAY()+5',
             '8/10', 'PM Lead role', 'Very responsive'],
            ['Referral', 'John Smith', 'Stripe', 'john@stripe.com', '555-123-4567',
             'linkedin.com/in/johnsmith', '=TODAY()-14', '=TODAY()-7', '',
             '10/10', 'Internal referral submitted', 'Former colleague from Meta'],
            ['Agency Recruiter', 'Mike Chen', 'TechRecruit', 'mike@techrecruit.com', '555-987-6543',
             'linkedin.com/in/mikechen', '=TODAY()-30', '=TODAY()-14', '=TODAY()+7',
             '5/10', 'Several PM roles', 'Specializes in product roles'],
        ]

        return {
            'tab_name': '💼 Recruiter CRM',
            'headers': headers,
            'data': sample_data,
            'column_widths': [120, 150, 120, 200, 120, 200, 100, 100, 100, 100, 150, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [6, 7, 8],
            },
            'validation': {
                'contact_type': {'column': 0, 'values': VALIDATION['recruiter_type']},
            }
        }

    def build_interview_tracker_tab(self):
        """
        Tab 15: Interview Tracker
        Interview scheduling and prep
        """
        headers = ['Pipeline ID', 'Interview Type', 'Date', 'Time', 'Duration (min)',
                   'Interviewers', 'Key Topics', 'Prep Completed', 'Questions Asked',
                   'My Questions', 'Feeling (1-10)', 'Thank You Sent', 'Follow-up Items', 'Notes']

        sample_data = [
            ['JP-002', 'Phone Screen', '=TODAY()-5', '2:00 PM', 30,
             'Sarah Johnson (Recruiter)', 'Background, motivation, salary expectations',
             True, 'Why Stripe? Career goals?', 'Team size, growth plans', 8,
             True, '', 'Good rapport, moved to next round'],
            ['JP-003', 'Video', '=TODAY()-3', '10:00 AM', 60,
             'Alex Kim (Hiring Manager)', 'Product strategy, leadership experience',
             True, 'Tell me about a product launch', 'Roadmap priorities', 9,
             True, 'Send portfolio examples', 'Very positive conversation'],
            ['JP-003', 'Panel', '=TODAY()+5', '1:00 PM', 90,
             'Team panel (4 people)', 'Case study, collaboration',
             False, '', 'Team dynamics, success metrics', '',
             False, '', 'Final round - prepare case study'],
        ]

        return {
            'tab_name': '💼 Interview Tracker',
            'headers': headers,
            'data': sample_data,
            'column_widths': [80, 120, 100, 80, 80, 200, 200, 80, 250, 200, 80, 80, 200, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 2,
                'checkbox_cols': [7, 11],
            },
            'validation': {
                'interview_type': {'column': 1, 'values': VALIDATION['interview_type']},
            }
        }

    def build_follow_ups_tab(self):
        """
        Tab 16: Follow-Ups
        Follow-up tracking and scheduling
        """
        headers = ['Pipeline ID', 'Follow-Up Type', 'Recipient', 'Scheduled Date',
                   'Sent Date', 'Send Method', 'Template Used', 'Response Received',
                   'Response Date', 'Next Action', 'Notes']

        sample_data = [
            ['JP-002', 'Thank You', 'Sarah Johnson', '=TODAY()-5', '=TODAY()-5',
             'Email', 'Standard Thank You', True, '=TODAY()-4', 'None - moving forward', ''],
            ['JP-003', 'Thank You', 'Alex Kim', '=TODAY()-3', '=TODAY()-3',
             'Email', 'Detailed Thank You', True, '=TODAY()-2', 'Send portfolio', 'Very positive response'],
            ['JP-001', 'Status Check', 'HR Team', '=TODAY()-7', '=TODAY()-7',
             'Email', 'Status Inquiry', False, '', 'Follow up again in 1 week', 'No response yet'],
        ]

        return {
            'tab_name': '💼 Follow-Ups',
            'headers': headers,
            'data': sample_data,
            'column_widths': [80, 120, 150, 100, 100, 100, 150, 100, 100, 200, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [3, 4, 8],
                'checkbox_col': 7,
            },
            'validation': {
                'follow_up_type': {'column': 1, 'values': VALIDATION['follow_up_type']},
            }
        }

    def build_offer_comparison_tab(self):
        """
        Tab 17: Offer Comparison
        Side-by-side offer analysis
        """
        headers = ['Metric', 'Offer 1', 'Offer 2', 'Offer 3', 'Notes']

        comparison_rows = [
            ['Company', '', '', '', ''],
            ['Role', '', '', '', ''],
            ['Base Salary', '', '', '', ''],
            ['Signing Bonus', '', '', '', ''],
            ['Annual Bonus %', '', '', '', ''],
            ['Total Cash Year 1', '=B3+B4+B3*B5', '=C3+C4+C3*C5', '=D3+D4+D3*D5', 'Base + Signing + Bonus'],
            ['Equity Value (4yr)', '', '', '', ''],
            ['Annual Equity', '=B7/4', '=C7/4', '=D7/4', ''],
            ['Total Comp Year 1', '=B6+B8', '=C6+C8', '=D6+D8', ''],
            ['', '', '', '', ''],
            ['Benefits Score (1-10)', '', '', '', ''],
            ['401k Match %', '', '', '', ''],
            ['PTO Days', '', '', '', ''],
            ['Remote Policy', '', '', '', ''],
            ['', '', '', '', ''],
            ['Growth Potential (1-10)', '', '', '', ''],
            ['Culture Fit (1-10)', '', '', '', ''],
            ['Commute/Location', '', '', '', ''],
            ['', '', '', '', ''],
            ['Start Date', '', '', '', ''],
            ['Decision Deadline', '', '', '', ''],
            ['', '', '', '', ''],
            ['OVERALL SCORE', '=AVERAGE(B11,B16,B17)*10', '=AVERAGE(C11,C16,C17)*10', '=AVERAGE(D11,D16,D17)*10', 'Weighted average'],
        ]

        return {
            'tab_name': '💼 Offer Comparison',
            'headers': headers,
            'data': comparison_rows,
            'column_widths': [180, 150, 150, 150, 250],
            'freeze_rows': 1,
            'freeze_cols': 1,
            'formatting': {
                'currency_rows': [2, 3, 5, 6, 7, 8],
                'percentage_rows': [4, 11],
                'date_rows': [19, 20],
                'highlight_row': 22,
            }
        }

    def build_job_search_dashboard_tab(self):
        """
        Tab 18: Job Search Dashboard
        Key metrics and visualizations
        """
        headers = ['JOB SEARCH DASHBOARD', '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['PIPELINE METRICS', '', '', 'CONVERSION FUNNEL', '', ''],
            ['Active Applications', '=COUNTIFS(\'💼 Job Pipeline\'!P:P,"Active")', '', 'Applied', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"Applied")', ''],
            ['This Week Applications', '=COUNTIFS(\'💼 Job Pipeline\'!B:B,">="&TODAY()-7)', '', 'Phone Screen', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"Phone Screen")', ''],
            ['Interview Conversion Rate', '=IFERROR(COUNTIF(\'💼 Job Pipeline\'!H:H,"Interview")/COUNTIF(\'💼 Job Pipeline\'!H:H,"Applied"),0)', '', 'Interview', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"Interview")', ''],
            ['Avg Days to Interview', '=AVERAGEIF(\'💼 Applications Tracker\'!K:K,"Interview",\'💼 Applications Tracker\'!J:J)', '', 'Final Round', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"Final Round")', ''],
            ['', '', '', 'Offer', '=COUNTIF(\'💼 Job Pipeline\'!H:H,"Offer")', ''],
            ['', '', '', '', '', ''],
            ['UPCOMING ACTIONS', '', '', 'BY COMPANY', '', ''],
            ['Interviews This Week', '=COUNTIFS(\'💼 Interview Tracker\'!C:C,">="&TODAY(),\'💼 Interview Tracker\'!C:C,"<"&TODAY()+7)', '', 'Company', 'Applications', ''],
            ['Follow-Ups Due', '=COUNTIFS(\'💼 Follow-Ups\'!D:D,"<="&TODAY(),\'💼 Follow-Ups\'!E:E,"")', '', '=UNIQUE(\'💼 Job Pipeline\'!C:C)', '=COUNTIF(\'💼 Job Pipeline\'!C:C,D11)', ''],
            ['Stalled Applications (>14d)', '=COUNTIFS(\'💼 Job Pipeline\'!K:K,">14",\'💼 Job Pipeline\'!P:P,"Active")', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['PRIORITY BREAKDOWN', '', '', '', '', ''],
            ['P0 - Critical', '=COUNTIF(\'💼 Job Pipeline\'!M:M,"P0 - Critical")', '', '', '', ''],
            ['P1 - High', '=COUNTIF(\'💼 Job Pipeline\'!M:M,"P1 - High")', '', '', '', ''],
            ['P2 - Medium', '=COUNTIF(\'💼 Job Pipeline\'!M:M,"P2 - Medium")', '', '', '', ''],
            ['P3 - Low', '=COUNTIF(\'💼 Job Pipeline\'!M:M,"P3 - Low")', '', '', '', ''],
        ]

        return {
            'tab_name': '💼 Job Search Dashboard',
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [200, 100, 50, 150, 100, 100],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 8, 13],
                'percentage_cols': [1],
            }
        }


def get_job_search_tab_data():
    """Get all job search tab configurations without building"""
    return {
        'tabs': [
            '💼 Job Pipeline',
            '💼 Applications Tracker',
            '💼 Recruiter CRM',
            '💼 Interview Tracker',
            '💼 Follow-Ups',
            '💼 Offer Comparison',
            '💼 Job Search Dashboard',
        ],
        'count': 7
    }
