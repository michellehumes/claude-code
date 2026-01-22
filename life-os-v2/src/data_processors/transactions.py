"""
Transaction data processor for Monarch Money CSV exports
"""

import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import json


class TransactionProcessor:
    """Process Monarch Money transaction CSV files"""

    def __init__(self, csv_path=None):
        self.csv_path = csv_path
        self.df = None
        self.categories = []
        self.merchants = []
        self.accounts = []
        self.credit_cards = []

    def load_csv(self, path=None):
        """Load transaction CSV file"""
        path = path or self.csv_path
        if not path:
            raise ValueError("No CSV path provided")

        self.df = pd.read_csv(path)

        # Ensure Date column is datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        # Extract unique values
        self._extract_metadata()

        return self.df

    def _extract_metadata(self):
        """Extract categories, merchants, and accounts from transactions"""
        if self.df is None:
            return

        self.categories = sorted(self.df['Category'].dropna().unique().tolist())
        self.merchants = sorted(self.df['Merchant'].dropna().unique().tolist())
        self.accounts = sorted(self.df['Account'].dropna().unique().tolist())

        # Identify credit cards (accounts with card-like names)
        card_keywords = ['card', 'visa', 'mastercard', 'amex', 'discover', 'platinum', 'gold', 'reserve', 'venture', 'freedom', 'sapphire']
        self.credit_cards = [
            acc for acc in self.accounts
            if any(kw in acc.lower() for kw in card_keywords)
        ]

    def get_transactions_data(self):
        """Get all transactions as list of lists for Google Sheets"""
        if self.df is None:
            return []

        # Convert DataFrame to list format
        data = []
        for _, row in self.df.iterrows():
            data.append([
                row['Date'].strftime('%m/%d/%Y') if pd.notna(row['Date']) else '',
                str(row['Merchant']) if pd.notna(row['Merchant']) else '',
                str(row['Category']) if pd.notna(row['Category']) else '',
                str(row['Account']) if pd.notna(row['Account']) else '',
                str(row['Original Statement']) if pd.notna(row.get('Original Statement', '')) else '',
                str(row['Notes']) if pd.notna(row.get('Notes', '')) else '',
                float(row['Amount']) if pd.notna(row['Amount']) else 0,
                str(row['Tags']) if pd.notna(row.get('Tags', '')) else '',
                str(row['Owner']) if pd.notna(row.get('Owner', '')) else ''
            ])

        return data

    def get_credit_card_data(self):
        """Extract credit card summary data"""
        if self.df is None:
            return []

        card_data = []
        today = datetime.now()
        this_month_start = today.replace(day=1)
        this_year_start = today.replace(month=1, day=1)

        for card in self.credit_cards:
            card_txns = self.df[self.df['Account'] == card]

            if len(card_txns) == 0:
                continue

            # Calculate metrics
            expenses = card_txns[card_txns['Amount'] < 0]['Amount']
            total_spent = abs(expenses.sum())
            last_txn = card_txns['Date'].max()
            txn_count = len(card_txns)
            avg_txn = abs(expenses.mean()) if len(expenses) > 0 else 0

            # Monthly spending
            monthly_txns = card_txns[card_txns['Date'] >= this_month_start]
            monthly_expenses = monthly_txns[monthly_txns['Amount'] < 0]['Amount']
            monthly_spent = abs(monthly_expenses.sum())

            # Yearly spending
            yearly_txns = card_txns[card_txns['Date'] >= this_year_start]
            yearly_expenses = yearly_txns[yearly_txns['Amount'] < 0]['Amount']
            yearly_spent = abs(yearly_expenses.sum())

            # Primary category
            if len(card_txns) > 0:
                primary_category = card_txns['Category'].mode()
                primary_category = primary_category.iloc[0] if len(primary_category) > 0 else ''
            else:
                primary_category = ''

            card_data.append([
                card,                                         # Account Name
                '',                                           # Current Balance (manual entry)
                monthly_spent,                                # This Month Spent
                yearly_spent,                                 # This Year Spent
                total_spent,                                  # All-Time Spent
                last_txn.strftime('%m/%d/%Y') if pd.notna(last_txn) else '',  # Last Transaction
                txn_count,                                    # Transaction Count
                avg_txn,                                      # Average Transaction
                primary_category                              # Primary Category
            ])

        # Sort by yearly spending (descending)
        card_data.sort(key=lambda x: x[3], reverse=True)

        return card_data

    def get_category_data(self):
        """Extract spending by category data"""
        if self.df is None:
            return []

        today = datetime.now()
        this_month_start = today.replace(day=1)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        last_month_end = this_month_start - timedelta(days=1)
        three_months_ago = today - timedelta(days=90)
        six_months_ago = today - timedelta(days=180)
        this_year_start = today.replace(month=1, day=1)

        category_data = []

        for category in self.categories:
            cat_txns = self.df[self.df['Category'] == category]
            expenses = cat_txns[cat_txns['Amount'] < 0]['Amount']

            if len(expenses) == 0:
                continue

            total_spent = abs(expenses.sum())

            # This month
            this_month_txns = cat_txns[(cat_txns['Date'] >= this_month_start)]
            this_month_exp = this_month_txns[this_month_txns['Amount'] < 0]['Amount']
            this_month_spent = abs(this_month_exp.sum())

            # Last month
            last_month_txns = cat_txns[(cat_txns['Date'] >= last_month_start) & (cat_txns['Date'] <= last_month_end)]
            last_month_exp = last_month_txns[last_month_txns['Amount'] < 0]['Amount']
            last_month_spent = abs(last_month_exp.sum())

            # 3-month average
            three_month_txns = cat_txns[cat_txns['Date'] >= three_months_ago]
            three_month_exp = three_month_txns[three_month_txns['Amount'] < 0]['Amount']
            three_month_avg = abs(three_month_exp.sum()) / 3

            # 6-month average
            six_month_txns = cat_txns[cat_txns['Date'] >= six_months_ago]
            six_month_exp = six_month_txns[six_month_txns['Amount'] < 0]['Amount']
            six_month_avg = abs(six_month_exp.sum()) / 6

            # YTD
            ytd_txns = cat_txns[cat_txns['Date'] >= this_year_start]
            ytd_exp = ytd_txns[ytd_txns['Amount'] < 0]['Amount']
            ytd_spent = abs(ytd_exp.sum())

            # Transaction count and average
            txn_count = len(expenses)
            avg_txn = abs(expenses.mean())

            # Trend (comparing this month to 3-month average)
            if three_month_avg > 0:
                trend = (this_month_spent - three_month_avg) / three_month_avg
                trend_str = "↑" if trend > 0.1 else ("↓" if trend < -0.1 else "→")
            else:
                trend_str = "→"

            category_data.append([
                category,                                     # Category
                this_month_spent,                            # This Month
                last_month_spent,                            # Last Month
                three_month_avg,                             # 3-Month Avg
                six_month_avg,                               # 6-Month Avg
                ytd_spent,                                   # YTD
                0,                                           # % of Total (calculated via formula)
                txn_count,                                   # Transaction Count
                avg_txn,                                     # Avg Transaction
                trend_str                                    # Trend
            ])

        # Sort by this month (descending)
        category_data.sort(key=lambda x: x[1], reverse=True)

        return category_data

    def get_monthly_summary(self, months=24):
        """Generate monthly summary for last N months"""
        if self.df is None:
            return []

        today = datetime.now()
        monthly_data = []

        for i in range(months):
            # Calculate month boundaries
            month_end = today.replace(day=1) - timedelta(days=1)
            if i > 0:
                for _ in range(i):
                    month_end = month_end.replace(day=1) - timedelta(days=1)

            month_start = month_end.replace(day=1)

            # Filter transactions for this month
            month_txns = self.df[(self.df['Date'] >= month_start) & (self.df['Date'] <= month_end)]

            # Calculate metrics
            income = month_txns[month_txns['Amount'] > 0]['Amount'].sum()
            expenses = abs(month_txns[month_txns['Amount'] < 0]['Amount'].sum())
            net = income - expenses
            txn_count = len(month_txns)
            days_in_month = (month_end - month_start).days + 1
            avg_daily = expenses / days_in_month if days_in_month > 0 else 0
            savings_rate = (net / income * 100) if income > 0 else 0

            monthly_data.append([
                month_start.strftime('%b %Y'),               # Month
                income,                                       # Total Income
                expenses,                                     # Total Expenses
                net,                                          # Net
                f"{savings_rate:.1f}%",                       # Savings Rate
                txn_count,                                    # Transaction Count
                avg_daily                                     # Avg Daily Spending
            ])

        return monthly_data

    def get_merchant_data(self, top_n=100):
        """Extract top merchants by spending"""
        if self.df is None:
            return []

        today = datetime.now()
        this_month_start = today.replace(day=1)
        this_year_start = today.replace(month=1, day=1)

        merchant_totals = defaultdict(lambda: {
            'total': 0, 'count': 0, 'this_month': 0, 'ytd': 0,
            'categories': [], 'last_date': None
        })

        for _, row in self.df.iterrows():
            merchant = row['Merchant']
            if pd.isna(merchant):
                continue

            amount = row['Amount']
            date = row['Date']
            category = row['Category']

            if amount < 0:  # Only count expenses
                merchant_totals[merchant]['total'] += abs(amount)
                merchant_totals[merchant]['count'] += 1
                merchant_totals[merchant]['categories'].append(category)

                if date >= this_month_start:
                    merchant_totals[merchant]['this_month'] += abs(amount)
                if date >= this_year_start:
                    merchant_totals[merchant]['ytd'] += abs(amount)

                if merchant_totals[merchant]['last_date'] is None or date > merchant_totals[merchant]['last_date']:
                    merchant_totals[merchant]['last_date'] = date

        # Sort by total spending and take top N
        sorted_merchants = sorted(merchant_totals.items(), key=lambda x: x[1]['total'], reverse=True)[:top_n]

        merchant_data = []
        for merchant, data in sorted_merchants:
            # Find primary category
            if data['categories']:
                from collections import Counter
                primary_category = Counter(data['categories']).most_common(1)[0][0]
            else:
                primary_category = ''

            avg_txn = data['total'] / data['count'] if data['count'] > 0 else 0

            merchant_data.append([
                merchant,                                     # Merchant
                data['count'],                                # Transaction Count
                data['total'],                                # Total Spent
                avg_txn,                                      # Avg Transaction
                primary_category,                             # Primary Category
                data['last_date'].strftime('%m/%d/%Y') if data['last_date'] else '',  # Last Transaction
                data['this_month'],                           # This Month
                data['ytd']                                   # YTD
            ])

        return merchant_data

    def get_budget_categories(self):
        """Get categories for budget master with historical data"""
        if self.df is None:
            return []

        today = datetime.now()
        this_month_start = today.replace(day=1)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        last_month_end = this_month_start - timedelta(days=1)
        three_months_ago = today - timedelta(days=90)
        this_year_start = today.replace(month=1, day=1)

        budget_data = []

        for category in self.categories:
            cat_txns = self.df[self.df['Category'] == category]
            expenses = cat_txns[cat_txns['Amount'] < 0]

            if len(expenses) == 0:
                continue

            # This month actual
            this_month_exp = expenses[expenses['Date'] >= this_month_start]['Amount']
            actual_spent = abs(this_month_exp.sum())

            # Last month
            last_month_exp = expenses[(expenses['Date'] >= last_month_start) & (expenses['Date'] <= last_month_end)]['Amount']
            last_month_spent = abs(last_month_exp.sum())

            # 3-month average (for budget suggestion)
            three_month_exp = expenses[expenses['Date'] >= three_months_ago]['Amount']
            three_month_avg = abs(three_month_exp.sum()) / 3

            # YTD
            ytd_exp = expenses[expenses['Date'] >= this_year_start]['Amount']
            ytd_spent = abs(ytd_exp.sum())

            budget_data.append([
                category,                                     # Category
                '',                                           # Monthly Budget (manual entry)
                actual_spent,                                 # Actual Spent
                '',                                           # Remaining (formula)
                '',                                           # % Used (formula)
                last_month_spent,                            # Last Month
                three_month_avg,                             # 3-Month Avg
                ytd_spent,                                   # YTD
                ''                                           # Status (formula)
            ])

        # Sort by 3-month average (descending)
        budget_data.sort(key=lambda x: x[6], reverse=True)

        return budget_data

    def get_shelzys_transactions(self):
        """Extract Shelzy's Designs transactions"""
        if self.df is None:
            return []

        # Filter for Shelzy's related transactions
        shelzys_keywords = ['shelzy', 'shopify', 'etsy', 'paypal', 'stripe']
        shelzys_txns = self.df[
            self.df['Category'].str.lower().str.contains('shelzy', na=False) |
            self.df['Merchant'].str.lower().str.contains('|'.join(shelzys_keywords), na=False) |
            self.df['Account'].str.lower().str.contains('shelzy', na=False)
        ]

        return self.get_transactions_data()  # Return format similar to main transactions

    @staticmethod
    def generate_sample_data():
        """Generate sample transaction data for testing"""
        import random

        categories = [
            'Groceries', 'Restaurants & Bars', 'Shopping', 'Gas', 'Utilities',
            'Rent', 'Insurance', 'Healthcare', 'Entertainment', 'Travel',
            'Subscriptions', 'Car Payment', 'Phone', 'Internet', 'Gym'
        ]

        merchants = [
            'Whole Foods', 'Stop & Shop', 'Target', 'Amazon', 'Costco',
            'Shell', 'Exxon', 'Netflix', 'Spotify', 'CVS', 'Starbucks',
            'Uber', 'Lyft', 'Chase', 'Verizon', 'Comcast'
        ]

        accounts = [
            'Sapphire Reserve (...1041)', 'Amex Gold (...2003)',
            'Venture Card (...4522)', 'Freedom Unlimited (...9759)',
            'Checking (...4688)', 'Savings (...3045)'
        ]

        owners = ['Michelle', 'Gray', 'Shared']

        data = []
        today = datetime.now()

        for i in range(500):  # Generate 500 sample transactions
            date = today - timedelta(days=random.randint(0, 365))
            category = random.choice(categories)
            merchant = random.choice(merchants)
            account = random.choice(accounts)
            owner = random.choice(owners)

            # Random amount (-500 to -5 for expenses, occasional positive for income)
            if random.random() < 0.1:  # 10% income
                amount = round(random.uniform(500, 5000), 2)
            else:
                amount = round(random.uniform(-500, -5), 2)

            data.append([
                date.strftime('%m/%d/%Y'),
                merchant,
                category,
                account,
                f"{merchant} transaction",
                '',
                amount,
                '',
                owner
            ])

        return data
