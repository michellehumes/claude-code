"""
Shelzy's Designs Business Tab Builder (Tabs 26-34)

Tab 26: Shelzy's Transactions
Tab 27: Shelzy's Revenue Tracker
Tab 28: Shelzy's Product Catalog
Tab 29: Shelzy's Expenses
Tab 30: Shelzy's Monthly P&L
Tab 31: Shelzy's Customer Metrics
Tab 32: Shelzy's Inventory
Tab 33: Shelzy's Marketing
Tab 34: Shelzy's Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import COLORS, VALIDATION


class ShelzysTabBuilder:
    """Build Shelzy's Designs business tabs (26-34)"""

    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def build_all_tabs(self):
        """Build all Shelzy's Designs tabs"""
        results = {}

        results['transactions'] = self.build_transactions_tab()
        results['revenue'] = self.build_revenue_tracker_tab()
        results['catalog'] = self.build_product_catalog_tab()
        results['expenses'] = self.build_expenses_tab()
        results['pnl'] = self.build_monthly_pnl_tab()
        results['customer_metrics'] = self.build_customer_metrics_tab()
        results['inventory'] = self.build_inventory_tab()
        results['marketing'] = self.build_marketing_tab()
        results['dashboard'] = self.build_dashboard_tab()

        return results

    def build_transactions_tab(self):
        """
        Tab 26: Shelzy's Transactions
        Business financial tracking
        """
        headers = ['Date', 'Type', 'Category', 'Description', 'Channel',
                   'Customer Type', 'Amount', 'Notes']

        categories = [
            'Revenue - Product Sales', 'Revenue - Shipping', 'Revenue - Other',
            'COGS - Product Cost', 'COGS - Packaging', 'COGS - Shipping Supplies', 'COGS - Production',
            'Marketing - Paid Ads', 'Marketing - Influencer', 'Marketing - Email', 'Marketing - Social', 'Marketing - Website',
            'Operations - Software', 'Operations - Storage', 'Operations - Fees', 'Operations - Supplies',
            'Admin - Other'
        ]

        sample_data = [
            ['=TODAY()-5', 'Revenue', 'Revenue - Product Sales', 'Order #1234 - Side Hustle Tracker', 'Shopify', 'New', 29.99, ''],
            ['=TODAY()-5', 'Revenue', 'Revenue - Shipping', 'Order #1234 - Shipping', 'Shopify', 'New', 4.99, ''],
            ['=TODAY()-4', 'Revenue', 'Revenue - Product Sales', 'Order #1235 - Budget Planner Bundle', 'Amazon', 'Returning', 49.99, ''],
            ['=TODAY()-3', 'Expense', 'COGS - Packaging', 'Shipping supplies from Amazon', '', '', -45.00, ''],
            ['=TODAY()-2', 'Expense', 'Marketing - Paid Ads', 'Facebook Ads - January Campaign', '', '', -150.00, ''],
            ['=TODAY()-1', 'Expense', 'Operations - Software', 'Canva Pro subscription', '', '', -12.99, ''],
        ]

        return {
            'tab_name': "📊 Shelzy's Transactions",
            'headers': headers,
            'data': sample_data,
            'column_widths': [100, 80, 180, 250, 100, 100, 100, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'currency_col': 6,
                'conditional': {
                    'revenue_expense': {
                        'column': 6,
                        'positive_color': COLORS['positive'],
                        'negative_color': COLORS['negative']
                    }
                }
            },
            'validation': {
                'type': {'column': 1, 'values': ['Revenue', 'Expense']},
                'channel': {'column': 4, 'values': VALIDATION['sales_channel']},
                'customer_type': {'column': 5, 'values': VALIDATION['customer_type']},
            }
        }

    def build_revenue_tracker_tab(self):
        """
        Tab 27: Shelzy's Revenue Tracker
        Order-level tracking
        """
        headers = ['Date', 'Order ID', 'Channel', 'Product Name', 'SKU', 'Quantity',
                   'Unit Price', 'Total Revenue', 'Shipping Charged', 'Total Order Value',
                   'Customer Type', 'Customer ID', 'City', 'State']

        sample_data = [
            ['=TODAY()-5', 'SHZ-1234', 'Shopify', 'Side Hustle Empire Tracker', 'SHZ-SHET-001', 1,
             29.99, '=F2*G2', 4.99, '=H2+I2', 'New', 'CUST-5678', 'New York', 'NY'],
            ['=TODAY()-4', 'AMZ-5678', 'Amazon', 'Budget Planner Bundle', 'SHZ-BPB-001', 1,
             49.99, '=F3*G3', 0, '=H3+I3', 'Returning', 'CUST-1234', 'Los Angeles', 'CA'],
            ['=TODAY()-3', 'SHZ-1235', 'Shopify', 'Goal Setting Workbook', 'SHZ-GSW-001', 2,
             19.99, '=F4*G4', 4.99, '=H4+I4', 'New', 'CUST-9012', 'Chicago', 'IL'],
        ]

        return {
            'tab_name': "📊 Shelzy's Revenue Tracker",
            'headers': headers,
            'data': sample_data,
            'column_widths': [100, 100, 100, 200, 120, 80, 100, 100, 100, 120, 100, 100, 100, 80],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'currency_cols': [6, 7, 8, 9],
            },
            'validation': {
                'channel': {'column': 2, 'values': VALIDATION['sales_channel']},
                'customer_type': {'column': 10, 'values': VALIDATION['customer_type']},
            }
        }

    def build_product_catalog_tab(self):
        """
        Tab 28: Shelzy's Product Catalog
        Product information and pricing
        """
        headers = ['SKU', 'Product Name', 'Category', 'Shopify Price', 'Amazon Price',
                   'Cost Per Unit', 'Gross Margin %', 'Units in Stock', 'Reorder Point',
                   'Lead Time (days)', 'Supplier', 'Last Ordered', 'Status']

        sample_products = [
            ['SHZ-SHET-001', 'Side Hustle Empire Tracker', 'Digital Planner', 29.99, 34.99,
             2.50, '=IFERROR((D2-F2)/D2,0)', 'N/A', 'N/A', 0, 'Digital', '', 'Active'],
            ['SHZ-BPB-001', 'Budget Planner Bundle', 'Digital Planner', 49.99, 54.99,
             4.00, '=IFERROR((D3-F3)/D3,0)', 'N/A', 'N/A', 0, 'Digital', '', 'Active'],
            ['SHZ-GSW-001', 'Goal Setting Workbook', 'Digital Workbook', 19.99, 24.99,
             1.50, '=IFERROR((D4-F4)/D4,0)', 'N/A', 'N/A', 0, 'Digital', '', 'Active'],
            ['SHZ-MBJ-001', 'Minimalist Budget Journal', 'Physical', 24.99, 29.99,
             8.00, '=IFERROR((D5-F5)/D5,0)', 150, 50, 14, 'PrintCo', '=TODAY()-30', 'Active'],
        ]

        return {
            'tab_name': "📊 Shelzy's Product Catalog",
            'headers': headers,
            'data': sample_products,
            'column_widths': [120, 200, 120, 100, 100, 100, 100, 80, 80, 80, 100, 100, 80],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [3, 4, 5],
                'percentage_col': 6,
                'date_col': 11,
            }
        }

    def build_expenses_tab(self):
        """
        Tab 29: Shelzy's Expenses
        Business expense tracking
        """
        headers = ['Date', 'Vendor', 'Category', 'Description', 'Amount',
                   'Payment Method', 'Tax Deductible', 'Receipt Link', 'Notes']

        sample_expenses = [
            ['=TODAY()-15', 'Canva', 'Operations - Software', 'Canva Pro Monthly', 12.99, 'Credit Card', True, '', ''],
            ['=TODAY()-10', 'Facebook', 'Marketing - Paid Ads', 'January Ad Spend', 150.00, 'Credit Card', True, '', 'New customer acquisition campaign'],
            ['=TODAY()-7', 'Amazon', 'COGS - Packaging', 'Shipping supplies', 45.00, 'Credit Card', True, '', ''],
            ['=TODAY()-5', 'Shopify', 'Operations - Fees', 'Monthly subscription', 29.00, 'Credit Card', True, '', ''],
        ]

        return {
            'tab_name': "📊 Shelzy's Expenses",
            'headers': headers,
            'data': sample_expenses,
            'column_widths': [100, 150, 180, 250, 100, 120, 100, 200, 250],
            'freeze_rows': 1,
            'formatting': {
                'date_col': 0,
                'currency_col': 4,
                'checkbox_col': 6,
            }
        }

    def build_monthly_pnl_tab(self):
        """
        Tab 30: Shelzy's Monthly P&L
        Profit and Loss statement
        """
        headers = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'YTD']

        # P&L structure
        pnl_rows = [
            ['REVENUE', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Product Sales (Shopify)', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B2:M2)'],
            ['Product Sales (Amazon)', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B3:M3)'],
            ['Shipping Revenue', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B4:M4)'],
            ['Other Revenue', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B5:M5)'],
            ['TOTAL REVENUE', '=SUM(B2:B5)', '=SUM(C2:C5)', '=SUM(D2:D5)', '=SUM(E2:E5)', '=SUM(F2:F5)', '=SUM(G2:G5)', '=SUM(H2:H5)', '=SUM(I2:I5)', '=SUM(J2:J5)', '=SUM(K2:K5)', '=SUM(L2:L5)', '=SUM(M2:M5)', '=SUM(B6:M6)'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['COST OF GOODS SOLD', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Product Cost', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B9:M9)'],
            ['Packaging', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B10:M10)'],
            ['Shipping Supplies', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B11:M11)'],
            ['Production', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B12:M12)'],
            ['TOTAL COGS', '=SUM(B9:B12)', '=SUM(C9:C12)', '=SUM(D9:D12)', '=SUM(E9:E12)', '=SUM(F9:F12)', '=SUM(G9:G12)', '=SUM(H9:H12)', '=SUM(I9:I12)', '=SUM(J9:J12)', '=SUM(K9:K12)', '=SUM(L9:L12)', '=SUM(M9:M12)', '=SUM(B13:M13)'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['GROSS PROFIT', '=B6-B13', '=C6-C13', '=D6-D13', '=E6-E13', '=F6-F13', '=G6-G13', '=H6-H13', '=I6-I13', '=J6-J13', '=K6-K13', '=L6-L13', '=M6-M13', '=N6-N13'],
            ['Gross Margin %', '=IFERROR(B15/B6,0)', '=IFERROR(C15/C6,0)', '=IFERROR(D15/D6,0)', '=IFERROR(E15/E6,0)', '=IFERROR(F15/F6,0)', '=IFERROR(G15/G6,0)', '=IFERROR(H15/H6,0)', '=IFERROR(I15/I6,0)', '=IFERROR(J15/J6,0)', '=IFERROR(K15/K6,0)', '=IFERROR(L15/L6,0)', '=IFERROR(M15/M6,0)', '=IFERROR(N15/N6,0)'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['OPERATING EXPENSES', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['Marketing - Paid Ads', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B19:M19)'],
            ['Marketing - Other', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B20:M20)'],
            ['Software/Tools', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B21:M21)'],
            ['Platform Fees', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B22:M22)'],
            ['Other Operating', '', '', '', '', '', '', '', '', '', '', '', '', '=SUM(B23:M23)'],
            ['TOTAL OPEX', '=SUM(B19:B23)', '=SUM(C19:C23)', '=SUM(D19:D23)', '=SUM(E19:E23)', '=SUM(F19:F23)', '=SUM(G19:G23)', '=SUM(H19:H23)', '=SUM(I19:I23)', '=SUM(J19:J23)', '=SUM(K19:K23)', '=SUM(L19:L23)', '=SUM(M19:M23)', '=SUM(B24:M24)'],
            ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ['NET PROFIT', '=B15-B24', '=C15-C24', '=D15-D24', '=E15-E24', '=F15-F24', '=G15-G24', '=H15-H24', '=I15-I24', '=J15-J24', '=K15-K24', '=L15-L24', '=M15-M24', '=N15-N24'],
            ['Net Margin %', '=IFERROR(B26/B6,0)', '=IFERROR(C26/C6,0)', '=IFERROR(D26/D6,0)', '=IFERROR(E26/E6,0)', '=IFERROR(F26/F6,0)', '=IFERROR(G26/G6,0)', '=IFERROR(H26/H6,0)', '=IFERROR(I26/I6,0)', '=IFERROR(J26/J6,0)', '=IFERROR(K26/K6,0)', '=IFERROR(L26/L6,0)', '=IFERROR(M26/M6,0)', '=IFERROR(N26/N6,0)'],
        ]

        return {
            'tab_name': "📊 Shelzy's Monthly P&L",
            'headers': headers,
            'data': pnl_rows,
            'column_widths': [180, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 100],
            'freeze_rows': 1,
            'freeze_cols': 1,
            'formatting': {
                'currency_cols': list(range(1, 14)),
                'percentage_rows': [15, 26],
                'section_headers': [0, 7, 17],
                'total_rows': [5, 12, 14, 23, 25],
            }
        }

    def build_customer_metrics_tab(self):
        """
        Tab 31: Shelzy's Customer Metrics
        Customer analytics
        """
        headers = ['Month', 'Total Orders', 'New Customers', 'Returning Customers',
                   'Repeat Rate %', 'Average Order Value', 'Total Revenue',
                   'Revenue Per Customer', 'Customer Acquisition Cost']

        # Generate 12 months with formulas
        data = []
        for i in range(12):
            row_num = i + 2
            month_offset = 11 - i
            data.append([
                f'=TEXT(EOMONTH(TODAY(),-{month_offset}),"MMM YYYY")',
                f'=COUNTIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&EOMONTH(TODAY(),-{month_offset+1})+1,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,"<="&EOMONTH(TODAY(),-{month_offset}))',
                f'=COUNTIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&EOMONTH(TODAY(),-{month_offset+1})+1,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,"<="&EOMONTH(TODAY(),-{month_offset}),\'📊 Shelzy\'\'s Revenue Tracker\'!K:K,"New")',
                f'=COUNTIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&EOMONTH(TODAY(),-{month_offset+1})+1,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,"<="&EOMONTH(TODAY(),-{month_offset}),\'📊 Shelzy\'\'s Revenue Tracker\'!K:K,"Returning")',
                f'=IFERROR(D{row_num}/B{row_num},0)',
                f'=IFERROR(SUMIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!J:J,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&EOMONTH(TODAY(),-{month_offset+1})+1,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,"<="&EOMONTH(TODAY(),-{month_offset}))/B{row_num},0)',
                f'=SUMIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!J:J,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&EOMONTH(TODAY(),-{month_offset+1})+1,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,"<="&EOMONTH(TODAY(),-{month_offset}))',
                f'=IFERROR(G{row_num}/(C{row_num}+D{row_num}),0)',
                ''
            ])

        return {
            'tab_name': "📊 Shelzy's Customer Metrics",
            'headers': headers,
            'data': data,
            'column_widths': [100, 100, 120, 140, 100, 140, 120, 140, 160],
            'freeze_rows': 1,
            'formatting': {
                'currency_cols': [5, 6, 7, 8],
                'percentage_col': 4,
            }
        }

    def build_inventory_tab(self):
        """
        Tab 32: Shelzy's Inventory
        Stock management
        """
        headers = ['SKU', 'Product Name', 'Current Stock', 'Reserved', 'Available',
                   'Reorder Point', 'Reorder Quantity', 'Status', 'Last Stocked',
                   'Next Order Date', 'Notes']

        sample_inventory = [
            ['SHZ-MBJ-001', 'Minimalist Budget Journal', 150, 10, '=C2-D2', 50, 100,
             '=IF(E2<=0,"Out of Stock",IF(E2<=F2,"Low Stock","In Stock"))', '=TODAY()-30', '', ''],
            ['SHZ-WKB-001', 'Weekly Planner Booklet', 45, 5, '=C3-D3', 30, 75,
             '=IF(E3<=0,"Out of Stock",IF(E3<=F3,"Low Stock","In Stock"))', '=TODAY()-45', '=TODAY()+7', 'Order placed'],
            ['SHZ-SHET-001', 'Side Hustle Empire Tracker', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',
             'Digital', '', '', 'Digital product - unlimited'],
        ]

        return {
            'tab_name': "📊 Shelzy's Inventory",
            'headers': headers,
            'data': sample_inventory,
            'column_widths': [120, 200, 100, 80, 80, 100, 100, 100, 100, 100, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [8, 9],
                'conditional': {
                    'stock_status': {
                        'column': 7,
                        'values': {
                            'In Stock': COLORS['positive'],
                            'Low Stock': COLORS['warning'],
                            'Out of Stock': COLORS['negative']
                        }
                    }
                }
            }
        }

    def build_marketing_tab(self):
        """
        Tab 33: Shelzy's Marketing
        Campaign tracking
        """
        headers = ['Channel', 'Campaign Name', 'Start Date', 'End Date', 'Budget',
                   'Spend', 'Impressions', 'Clicks', 'Orders', 'Revenue Generated',
                   'CTR', 'Conversion Rate', 'ROAS', 'Notes']

        sample_campaigns = [
            ['Facebook Ads', 'January New Year Goals', '=TODAY()-30', '=TODAY()-15', 200, 185,
             25000, 450, 12, 359.88, '=IFERROR(H2/G2,0)', '=IFERROR(I2/H2,0)', '=IFERROR(J2/F2,0)', 'Good performance'],
            ['Instagram', 'Planner Launch', '=TODAY()-20', '=TODAY()-5', 150, 142,
             18000, 320, 8, 239.92, '=IFERROR(H3/G3,0)', '=IFERROR(I3/H3,0)', '=IFERROR(J3/F3,0)', ''],
            ['Google', 'Budget Planner Keywords', '=TODAY()-45', '', 300, 275,
             35000, 580, 15, 449.85, '=IFERROR(H4/G4,0)', '=IFERROR(I4/H4,0)', '=IFERROR(J4/F4,0)', 'Ongoing campaign'],
            ['Email', 'Welcome Series', '=TODAY()-60', '', 0, 0,
             5000, 1200, 25, 749.75, '=IFERROR(H5/G5,0)', '=IFERROR(I5/H5,0)', '=IFERROR(J5/F5,0)', 'Automated'],
        ]

        return {
            'tab_name': "📊 Shelzy's Marketing",
            'headers': headers,
            'data': sample_campaigns,
            'column_widths': [100, 200, 100, 100, 100, 100, 100, 80, 80, 120, 80, 100, 80, 200],
            'freeze_rows': 1,
            'formatting': {
                'date_cols': [2, 3],
                'currency_cols': [4, 5, 9],
                'percentage_cols': [10, 11],
            },
            'validation': {
                'channel': {'column': 0, 'values': VALIDATION['marketing_channel']},
            }
        }

    def build_dashboard_tab(self):
        """
        Tab 34: Shelzy's Dashboard
        Business overview
        """
        headers = ["SHELZY'S DESIGNS DASHBOARD", '', '', '', '', '']

        dashboard_data = [
            ['', '', '', '', '', ''],
            ['MTD PERFORMANCE', '', '', 'YTD PERFORMANCE', '', ''],
            ['Shopify Revenue', '=SUMIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!J:J,\'📊 Shelzy\'\'s Revenue Tracker\'!C:C,"Shopify",\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', '', 'Total Revenue', '=SUMIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!J:J,\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&DATE(YEAR(TODAY()),1,1))', ''],
            ['Amazon Revenue', '=SUMIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!J:J,\'📊 Shelzy\'\'s Revenue Tracker\'!C:C,"Amazon",\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', '', 'Total Orders', '=COUNTIFS(\'📊 Shelzy\'\'s Revenue Tracker\'!A:A,">="&DATE(YEAR(TODAY()),1,1))', ''],
            ['Total Revenue', '=B3+B4', '', 'Avg Order Value', '=IFERROR(E3/E4,0)', ''],
            ['Expenses', '=ABS(SUMIFS(\'📊 Shelzy\'\'s Transactions\'!G:G,\'📊 Shelzy\'\'s Transactions\'!B:B,"Expense",\'📊 Shelzy\'\'s Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1)))', '', 'New Customers', '=SUMIFS(\'📊 Shelzy\'\'s Customer Metrics\'!C:C,\'📊 Shelzy\'\'s Customer Metrics\'!A:A,">="&DATE(YEAR(TODAY()),1,1))', ''],
            ['Profit', '=B5-B6', '', 'Repeat Rate', '=IFERROR(AVERAGE(\'📊 Shelzy\'\'s Customer Metrics\'!E:E),0)', ''],
            ['Margin', '=IFERROR(B7/B5,0)', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['TOP 5 PRODUCTS (MTD)', '', '', 'TOP 5 CUSTOMERS (YTD)', '', ''],
            ['Product', 'Revenue', '', 'Customer', 'Total Spent', ''],
            ['=INDEX(\'📊 Shelzy\'\'s Revenue Tracker\'!D:D,MATCH(LARGE(SUMIF(\'📊 Shelzy\'\'s Revenue Tracker\'!D:D,\'📊 Shelzy\'\'s Revenue Tracker\'!D:D,\'📊 Shelzy\'\'s Revenue Tracker\'!J:J),1),SUMIF(\'📊 Shelzy\'\'s Revenue Tracker\'!D:D,\'📊 Shelzy\'\'s Revenue Tracker\'!D:D,\'📊 Shelzy\'\'s Revenue Tracker\'!J:J),0))', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['MARKETING PERFORMANCE', '', '', 'INVENTORY ALERTS', '', ''],
            ['Total Ad Spend', '=SUM(\'📊 Shelzy\'\'s Marketing\'!F:F)', '', 'Low Stock Items', '=COUNTIF(\'📊 Shelzy\'\'s Inventory\'!H:H,"Low Stock")', ''],
            ['Total Revenue (Ads)', '=SUM(\'📊 Shelzy\'\'s Marketing\'!J:J)', '', 'Out of Stock', '=COUNTIF(\'📊 Shelzy\'\'s Inventory\'!H:H,"Out of Stock")', ''],
            ['Overall ROAS', '=IFERROR(B16/B15,0)', '', 'Orders Pending', '=SUM(\'📊 Shelzy\'\'s Inventory\'!D:D)', ''],
            ['Best Channel', '=INDEX(\'📊 Shelzy\'\'s Marketing\'!A:A,MATCH(MAX(\'📊 Shelzy\'\'s Marketing\'!M:M),\'📊 Shelzy\'\'s Marketing\'!M:M,0))', '', '', '', ''],
        ]

        return {
            'tab_name': "📊 Shelzy's Dashboard",
            'headers': headers,
            'data': dashboard_data,
            'column_widths': [180, 120, 50, 180, 120, 50],
            'freeze_rows': 1,
            'formatting': {
                'section_headers': [1, 9, 13],
                'currency_cols': [1, 4],
                'percentage_cols': [],
            }
        }


def get_shelzys_tab_data():
    """Get all Shelzy's tab configurations without building"""
    return {
        'tabs': [
            "📊 Shelzy's Transactions",
            "📊 Shelzy's Revenue Tracker",
            "📊 Shelzy's Product Catalog",
            "📊 Shelzy's Expenses",
            "📊 Shelzy's Monthly P&L",
            "📊 Shelzy's Customer Metrics",
            "📊 Shelzy's Inventory",
            "📊 Shelzy's Marketing",
            "📊 Shelzy's Dashboard",
        ],
        'count': 9
    }
