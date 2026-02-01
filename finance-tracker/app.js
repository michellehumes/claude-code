// Finance Tracker Application
class FinanceTracker {
    constructor() {
        this.transactions = [];
        this.filteredTransactions = [];
        this.currentPage = 1;
        this.itemsPerPage = 25;
        this.sortColumn = 'date';
        this.sortDirection = 'desc';
        this.categoryChart = null;
        this.timelineChart = null;

        this.init();
    }

    init() {
        // Event listeners
        document.getElementById('csvFile').addEventListener('change', (e) => this.handleFileUpload(e));
        document.getElementById('loadSample').addEventListener('click', () => this.loadSampleData());
        document.getElementById('clearFilters').addEventListener('click', () => this.clearFilters());
        document.getElementById('prevPage').addEventListener('click', () => this.changePage(-1));
        document.getElementById('nextPage').addEventListener('click', () => this.changePage(1));

        // Filter listeners
        ['dateFrom', 'dateTo', 'categoryFilter', 'accountFilter', 'ownerFilter', 'searchFilter'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => this.applyFilters());
            document.getElementById(id).addEventListener('input', () => this.applyFilters());
        });

        // Table header sorting
        document.querySelectorAll('#transactionsTable th[data-sort]').forEach(th => {
            th.addEventListener('click', () => this.sortTable(th.dataset.sort));
        });
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                this.parseCSV(e.target.result);
            };
            reader.readAsText(file);
        }
    }

    async loadSampleData() {
        // Try to load from the sample file, or use embedded data
        try {
            const response = await fetch('../monarch-perks-system/sample_transactions.csv');
            if (response.ok) {
                const text = await response.text();
                this.parseCSV(text);
                return;
            }
        } catch (e) {
            console.log('Loading embedded sample data');
        }

        // Use embedded sample data
        this.parseCSV(this.getSampleData());
    }

    parseCSV(csvText) {
        const lines = csvText.trim().split('\n');
        const headers = this.parseCSVLine(lines[0]);

        this.transactions = [];
        for (let i = 1; i < lines.length; i++) {
            const values = this.parseCSVLine(lines[i]);
            if (values.length >= headers.length) {
                const transaction = {};
                headers.forEach((header, index) => {
                    transaction[header.trim()] = values[index]?.trim() || '';
                });

                // Parse amount as number
                transaction.Amount = parseFloat(transaction.Amount) || 0;

                // Parse date
                if (transaction.Date) {
                    transaction.dateObj = new Date(transaction.Date);
                }

                this.transactions.push(transaction);
            }
        }

        // Sort by date descending
        this.transactions.sort((a, b) => (b.dateObj || 0) - (a.dateObj || 0));
        this.filteredTransactions = [...this.transactions];

        this.showSections();
        this.populateFilters();
        this.updateDashboard();
    }

    parseCSVLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;

        for (let i = 0; i < line.length; i++) {
            const char = line[i];

            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
        }
        result.push(current);

        return result;
    }

    showSections() {
        [
            'summarySection',
            'chartsSection',
            'ownerSummary',
            'monthlyOverview',
            'categoryBreakdown',
            'accountSummary',
            'transactionsSection'
        ].forEach(id => {
            document.getElementById(id).style.display = 'block';
        });
    }

    populateFilters() {
        const categories = [...new Set(this.transactions.map(t => t.Category).filter(Boolean))].sort();
        const accounts = [...new Set(this.transactions.map(t => t.Account).filter(Boolean))].sort();
        const owners = [...new Set(this.transactions.map(t => this.getOwnerName(t)).filter(Boolean))].sort();

        const categorySelect = document.getElementById('categoryFilter');
        categorySelect.innerHTML = '<option value="">All Categories</option>';
        categories.forEach(cat => {
            categorySelect.innerHTML += `<option value="${cat}">${cat}</option>`;
        });

        const accountSelect = document.getElementById('accountFilter');
        accountSelect.innerHTML = '<option value="">All Accounts</option>';
        accounts.forEach(acc => {
            accountSelect.innerHTML += `<option value="${acc}">${acc}</option>`;
        });

        const ownerSelect = document.getElementById('ownerFilter');
        ownerSelect.innerHTML = '<option value="">All Owners</option>';
        owners.forEach(owner => {
            ownerSelect.innerHTML += `<option value="${owner}">${owner}</option>`;
        });

        // Set date range
        const dates = this.transactions.map(t => t.Date).filter(Boolean).sort();
        if (dates.length > 0) {
            document.getElementById('dateFrom').value = dates[0];
            document.getElementById('dateTo').value = dates[dates.length - 1];
        }
    }

    applyFilters() {
        const dateFrom = document.getElementById('dateFrom').value;
        const dateTo = document.getElementById('dateTo').value;
        const category = document.getElementById('categoryFilter').value;
        const account = document.getElementById('accountFilter').value;
        const owner = document.getElementById('ownerFilter').value;
        const search = document.getElementById('searchFilter').value.toLowerCase();

        this.filteredTransactions = this.transactions.filter(t => {
            if (dateFrom && t.Date < dateFrom) return false;
            if (dateTo && t.Date > dateTo) return false;
            if (category && t.Category !== category) return false;
            if (account && t.Account !== account) return false;
            if (owner && this.getOwnerName(t) !== owner) return false;
            if (search && !t.Merchant?.toLowerCase().includes(search)) return false;
            return true;
        });

        this.currentPage = 1;
        this.updateDashboard();
    }

    clearFilters() {
        document.getElementById('categoryFilter').value = '';
        document.getElementById('accountFilter').value = '';
        document.getElementById('ownerFilter').value = '';
        document.getElementById('searchFilter').value = '';

        const dates = this.transactions.map(t => t.Date).filter(Boolean).sort();
        if (dates.length > 0) {
            document.getElementById('dateFrom').value = dates[0];
            document.getElementById('dateTo').value = dates[dates.length - 1];
        }

        this.filteredTransactions = [...this.transactions];
        this.currentPage = 1;
        this.updateDashboard();
    }

    updateDashboard() {
        this.updateSummary();
        this.updateCharts();
        this.updateOwnerSummary();
        this.updateMonthlyOverview();
        this.updateCategoryBreakdown();
        this.updateAccountSummary();
        this.updateTransactionsTable();
    }

    updateSummary() {
        const income = this.filteredTransactions
            .filter(t => t.Amount > 0)
            .reduce((sum, t) => sum + t.Amount, 0);

        const expenses = this.filteredTransactions
            .filter(t => t.Amount < 0)
            .reduce((sum, t) => sum + Math.abs(t.Amount), 0);

        const net = income - expenses;

        document.getElementById('totalIncome').textContent = this.formatCurrency(income);
        document.getElementById('totalExpenses').textContent = this.formatCurrency(expenses);
        document.getElementById('netCashFlow').textContent = this.formatCurrency(net);
        document.getElementById('netCashFlow').className = net >= 0 ? 'amount-positive' : 'amount-negative';
        document.getElementById('totalTransactions').textContent = this.filteredTransactions.length;
    }

    updateCharts() {
        this.updateCategoryChart();
        this.updateTimelineChart();
    }

    updateCategoryChart() {
        const categoryData = {};

        this.filteredTransactions
            .filter(t => t.Amount < 0)
            .forEach(t => {
                const cat = t.Category || 'Uncategorized';
                categoryData[cat] = (categoryData[cat] || 0) + Math.abs(t.Amount);
            });

        const sortedCategories = Object.entries(categoryData)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);

        const labels = sortedCategories.map(([cat]) => cat);
        const data = sortedCategories.map(([, amount]) => amount);
        const colors = this.generateColors(labels.length);

        const ctx = document.getElementById('categoryChart').getContext('2d');

        if (this.categoryChart) {
            this.categoryChart.destroy();
        }

        this.categoryChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 15,
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${context.label}: ${this.formatCurrency(value)} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    updateTimelineChart() {
        const monthlyData = {};

        this.filteredTransactions.forEach(t => {
            if (t.Date) {
                const month = t.Date.substring(0, 7); // YYYY-MM
                if (!monthlyData[month]) {
                    monthlyData[month] = { income: 0, expenses: 0 };
                }
                if (t.Amount > 0) {
                    monthlyData[month].income += t.Amount;
                } else {
                    monthlyData[month].expenses += Math.abs(t.Amount);
                }
            }
        });

        const sortedMonths = Object.keys(monthlyData).sort();
        const incomeData = sortedMonths.map(m => monthlyData[m].income);
        const expensesData = sortedMonths.map(m => monthlyData[m].expenses);
        const labels = sortedMonths.map(m => {
            const [year, month] = m.split('-');
            return new Date(year, month - 1).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        });

        const ctx = document.getElementById('timelineChart').getContext('2d');

        if (this.timelineChart) {
            this.timelineChart.destroy();
        }

        this.timelineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Income',
                        data: incomeData,
                        backgroundColor: 'rgba(22, 163, 74, 0.7)',
                        borderColor: 'rgba(22, 163, 74, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Expenses',
                        data: expensesData,
                        backgroundColor: 'rgba(220, 38, 38, 0.7)',
                        borderColor: 'rgba(220, 38, 38, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: (value) => this.formatCurrency(value)
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (context) => `${context.dataset.label}: ${this.formatCurrency(context.raw)}`
                        }
                    }
                }
            }
        });
    }

    updateCategoryBreakdown() {
        const categoryData = {};

        this.filteredTransactions.forEach(t => {
            const cat = t.Category || 'Uncategorized';
            if (!categoryData[cat]) {
                categoryData[cat] = { total: 0, count: 0 };
            }
            categoryData[cat].total += t.Amount;
            categoryData[cat].count++;
        });

        const sortedCategories = Object.entries(categoryData)
            .sort((a, b) => a[1].total - b[1].total); // Most negative first

        const maxExpense = Math.max(...sortedCategories.map(([, data]) => Math.abs(data.total)));

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Transactions</th>
                        <th>Total</th>
                        <th>% of Spending</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
        `;

        const totalExpenses = sortedCategories
            .filter(([, data]) => data.total < 0)
            .reduce((sum, [, data]) => sum + Math.abs(data.total), 0);

        sortedCategories.forEach(([category, data]) => {
            const percentage = data.total < 0 ? ((Math.abs(data.total) / totalExpenses) * 100).toFixed(1) : '-';
            const barWidth = data.total < 0 ? (Math.abs(data.total) / maxExpense) * 100 : 0;
            const amountClass = data.total >= 0 ? 'amount-positive' : 'amount-negative';

            html += `
                <tr>
                    <td><strong>${category}</strong></td>
                    <td>${data.count}</td>
                    <td class="${amountClass}">${this.formatCurrency(data.total)}</td>
                    <td>${percentage}${percentage !== '-' ? '%' : ''}</td>
                    <td style="width: 150px;">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${barWidth}%"></div>
                        </div>
                    </td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        document.getElementById('categoryTable').innerHTML = html;
    }

    updateAccountSummary() {
        const accountData = {};

        this.filteredTransactions.forEach(t => {
            const acc = t.Account || 'Unknown';
            if (!accountData[acc]) {
                accountData[acc] = { total: 0, count: 0, income: 0, expenses: 0 };
            }
            accountData[acc].total += t.Amount;
            accountData[acc].count++;
            if (t.Amount > 0) {
                accountData[acc].income += t.Amount;
            } else {
                accountData[acc].expenses += Math.abs(t.Amount);
            }
        });

        const sortedAccounts = Object.entries(accountData)
            .sort((a, b) => b[1].count - a[1].count);

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Account</th>
                        <th>Transactions</th>
                        <th>Income</th>
                        <th>Expenses</th>
                        <th>Net</th>
                    </tr>
                </thead>
                <tbody>
        `;

        sortedAccounts.forEach(([account, data]) => {
            const netClass = data.total >= 0 ? 'amount-positive' : 'amount-negative';
            html += `
                <tr>
                    <td><strong>${account}</strong></td>
                    <td>${data.count}</td>
                    <td class="amount-positive">${this.formatCurrency(data.income)}</td>
                    <td class="amount-negative">${this.formatCurrency(data.expenses)}</td>
                    <td class="${netClass}">${this.formatCurrency(data.total)}</td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        document.getElementById('accountTable').innerHTML = html;
    }

    updateTransactionsTable() {
        // Sort
        const sorted = [...this.filteredTransactions].sort((a, b) => {
            let valA, valB;

            switch (this.sortColumn) {
                case 'date':
                    valA = a.Date || '';
                    valB = b.Date || '';
                    break;
                case 'amount':
                    valA = a.Amount;
                    valB = b.Amount;
                    break;
                default:
                    valA = (a[this.sortColumn.charAt(0).toUpperCase() + this.sortColumn.slice(1)] || '').toLowerCase();
                    valB = (b[this.sortColumn.charAt(0).toUpperCase() + this.sortColumn.slice(1)] || '').toLowerCase();
            }

            if (valA < valB) return this.sortDirection === 'asc' ? -1 : 1;
            if (valA > valB) return this.sortDirection === 'asc' ? 1 : -1;
            return 0;
        });

        // Paginate
        const totalPages = Math.ceil(sorted.length / this.itemsPerPage);
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const pageData = sorted.slice(startIndex, startIndex + this.itemsPerPage);

        // Render
        const tbody = document.getElementById('transactionsBody');
        tbody.innerHTML = '';

        pageData.forEach(t => {
            const amountClass = t.Amount >= 0 ? 'amount-positive' : 'amount-negative';
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${t.Date || '-'}</td>
                <td>${t.Merchant || '-'}</td>
                <td>${t.Category || '-'}</td>
                <td>${t.Account || '-'}</td>
                <td class="${amountClass}">${this.formatCurrency(t.Amount)}</td>
                <td>${this.getOwnerName(t)}</td>
            `;
            tbody.appendChild(row);
        });

        // Update pagination
        document.getElementById('pageInfo').textContent = `Page ${this.currentPage} of ${totalPages || 1}`;
        document.getElementById('prevPage').disabled = this.currentPage <= 1;
        document.getElementById('nextPage').disabled = this.currentPage >= totalPages;

        // Update sort indicators
        document.querySelectorAll('#transactionsTable th[data-sort]').forEach(th => {
            th.textContent = th.textContent.replace(' ↑', '').replace(' ↓', '');
            if (th.dataset.sort === this.sortColumn) {
                th.textContent += this.sortDirection === 'asc' ? ' ↑' : ' ↓';
            }
        });
    }

    sortTable(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }
        this.updateTransactionsTable();
    }

    changePage(delta) {
        const totalPages = Math.ceil(this.filteredTransactions.length / this.itemsPerPage);
        this.currentPage = Math.max(1, Math.min(totalPages, this.currentPage + delta));
        this.updateTransactionsTable();
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(amount);
    }

    generateColors(count) {
        const colors = [
            '#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#8b5cf6',
            '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1',
            '#14b8a6', '#a855f7', '#eab308', '#64748b', '#10b981'
        ];
        return colors.slice(0, count);
    }

    getOwnerName(transaction) {
        return transaction.Owner?.trim() || 'Unassigned';
    }

    updateOwnerSummary() {
        const ownerData = {};

        this.filteredTransactions.forEach(t => {
            const owner = this.getOwnerName(t);
            if (!ownerData[owner]) {
                ownerData[owner] = { total: 0, income: 0, expenses: 0, count: 0 };
            }
            ownerData[owner].total += t.Amount;
            ownerData[owner].count++;
            if (t.Amount > 0) {
                ownerData[owner].income += t.Amount;
            } else {
                ownerData[owner].expenses += Math.abs(t.Amount);
            }
        });

        const sortedOwners = Object.entries(ownerData).sort((a, b) => b[1].count - a[1].count);

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Owner</th>
                        <th>Transactions</th>
                        <th>Income</th>
                        <th>Expenses</th>
                        <th>Net</th>
                    </tr>
                </thead>
                <tbody>
        `;

        sortedOwners.forEach(([owner, data]) => {
            const netClass = data.total >= 0 ? 'amount-positive' : 'amount-negative';
            html += `
                <tr>
                    <td><strong>${owner}</strong></td>
                    <td>${data.count}</td>
                    <td class="amount-positive">${this.formatCurrency(data.income)}</td>
                    <td class="amount-negative">${this.formatCurrency(data.expenses)}</td>
                    <td class="${netClass}">${this.formatCurrency(data.total)}</td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        document.getElementById('ownerTable').innerHTML = html;
    }

    updateMonthlyOverview() {
        const monthlyData = {};

        this.filteredTransactions.forEach(t => {
            if (!t.Date) return;
            const month = t.Date.substring(0, 7);
            const owner = this.getOwnerName(t);

            if (!monthlyData[month]) {
                monthlyData[month] = {};
            }
            if (!monthlyData[month][owner]) {
                monthlyData[month][owner] = { income: 0, expenses: 0 };
            }

            if (t.Amount > 0) {
                monthlyData[month][owner].income += t.Amount;
            } else {
                monthlyData[month][owner].expenses += Math.abs(t.Amount);
            }
        });

        const sortedMonths = Object.keys(monthlyData).sort();

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Owner</th>
                        <th>Income</th>
                        <th>Expenses</th>
                        <th>Net</th>
                    </tr>
                </thead>
                <tbody>
        `;

        sortedMonths.forEach(month => {
            const owners = Object.keys(monthlyData[month]).sort();
            owners.forEach((owner, index) => {
                const data = monthlyData[month][owner];
                const net = data.income - data.expenses;
                const netClass = net >= 0 ? 'amount-positive' : 'amount-negative';
                const monthLabel = index === 0 ? this.formatMonthLabel(month) : '';

                html += `
                    <tr>
                        <td>${monthLabel}</td>
                        <td><strong>${owner}</strong></td>
                        <td class="amount-positive">${this.formatCurrency(data.income)}</td>
                        <td class="amount-negative">${this.formatCurrency(data.expenses)}</td>
                        <td class="${netClass}">${this.formatCurrency(net)}</td>
                    </tr>
                `;
            });
        });

        html += '</tbody></table>';
        document.getElementById('monthlyTable').innerHTML = html;
    }

    formatMonthLabel(month) {
        const [year, monthIndex] = month.split('-');
        return new Date(year, monthIndex - 1).toLocaleDateString('en-US', {
            month: 'short',
            year: 'numeric'
        });
    }

    getSampleData() {
        return `Date,Merchant,Category,Account,Original Statement,Notes,Amount,Tags,Owner
2026-10-01,BILL PAY 12 Harbor,Rent,CHECKING (...4688),BILL PAY 12 Harbor ON-LINE No Account Number ON 08-29,,-7500.00,,Shared
2026-07-25,Lord Camden Inn,Hotel,Michelle's Sapphire Reserve (...1041),LORD CAMDEN INN,,-1470.57,,Shared
2026-02-11,Woodstock Inn & Resort,Hotel,Venture (...4522),WOODSTOCK INN & RESORT,,-867.91,,Shared
2026-01-09,Spotify,Music,Venture (...4522),Spotify USA,,-11.99,,Shared
2026-01-09,Geico,Car Insurance,Venture (...4522),GEICO *AUTO,,-152.51,,Shared
2026-01-09,BMW,Car Payment,CHECKING (...4688),BMW BANK BMWFS PYMT,,-751.00,,Shared
2026-01-09,Riverhead Brew House,Restaurants & Bars,Gray's Amex Gold Card (...2003),RIVERHEAD BREW HOUSE,,-123.11,,Shared
2026-01-09,Target,Shopping,Target Circle Card (...2828),TARGET 1818 076 6905,,-130.36,,Shared
2026-01-09,OpenAI,Subscriptions,Michelle's Freedom Unlimited (...9759),OPENAI *CHATGPT SUBSCR,,-217.75,,Shared
2026-01-09,Lyft,Taxi & Ride Shares,Michelle's Sapphire Reserve (...1041),LYFT *1 RIDE 07-19,,0.79,,Shared
2026-01-08,Sagtown Coffee,Delivery & Takeout,Gray's Amex Gold Card (...2003),AplPay SAGTOWN COFFE,,-26.14,,Shared
2026-01-08,Hamptonchutney.com,Restaurants & Bars,Venture (...4522),HAMPTONCHUTNEY.COM,,-19.37,,Shared
2026-01-08,E Hampton,Restaurants & Bars,Gray's Amex Platinum Card (...1007),E HAMPTON 631 329-6666,,-169.65,,Shared
2026-01-07,Stop & Shop,Groceries,Gray's Amex Gold Card (...2003),AplPay STOP & SHOP,,-20.04,,Shared
2026-01-07,Addepar,Paychecks,CHECKING (...4688),ADDEPAR INC Payroll,,5005.08,,Gray Perkins
2026-01-06,Bridgehampton Wine Cellars,Groceries,USAA Rate Advantage Platinum Visa (...9385),BRIDGEHAMPTON WINE CELLAR,,-45.68,,Shared
2026-01-06,Lyft,Taxi & Ride Shares,Michelle's Sapphire Reserve (...1041),LYFT *2 RIDES 07-02,,0.79,,Shared
2026-01-06,Citarella,Groceries,Gray's Amex Gold Card (...2003),AplPay CITARELLA,,-14.15,,Shared
2026-01-06,U-Haul,Storage Units,Venture (...4522),U-HAULCONSUMERS TIRE,,-43.00,,Shared
2026-01-05,Amazon,Shopping,Amazon Prime Card (...5990),AMAZON MKTPL,,-57.11,,Shared
2026-01-05,Stop & Shop,Groceries,Gray's Amex Gold Card (...2003),AplPay STOP & SHOP,,-69.31,,Shared
2026-01-05,Shopify,Shelzy's Designs,Michelle's Sapphire Reserve (...1041),PAYPAL *SHOPIFY,,-46.68,,Shared
2026-01-05,eBay,Shopping,Venture (...4522),eBay O*26-14033-02904,,-23.32,,Shared
2026-01-05,Starbucks,Delivery & Takeout,Venture (...4522),STARBUCKS,,-15.00,,Shared
2026-01-05,Costco,Gas & Car Wash,Venture (...4522),COSTCO GAS #0230,,-25.63,,Shared
2026-01-05,Costco,Shopping,Venture (...4522),WWW COSTCO COM,,-146.81,,Shared
2026-01-05,Airport Parking,Parking,Venture (...4522),MACARTHUR AIRPORT PARKIN,,-257.92,,Shared
2026-01-05,Breeze Aviation Group,Airline,Venture (...4522),BREEZE AVIATION GROUP,,-4.50,,Shared
2026-01-05,Apple,Subscriptions,Venture (...4522),APPLE.COM/BILL,,-2.99,,Shared
2026-01-04,Amazon,Shopping,Amazon Prime Card (...5990),AMAZON MKTPL,,-26.97,,Shared
2026-01-04,Villa Italian Specialt,Delivery & Takeout,Michelle's Sapphire Reserve (...1041),VILLA ITALIAN SPECIALTIES,,-31.60,,Shared
2026-01-04,Otter.ai,Subscriptions,Michelle's Freedom Unlimited (...9759),OTTER.AI,,-18.50,,Shared
2026-01-04,Citarella,Groceries,Gray's Amex Gold Card (...2003),AplPay CITARELLA,,-28.91,,Shared
2026-01-03,Long Island Aquarium,Shopping,Michelle's Sapphire Reserve (...1041),LONG ISLAND AQUARIUM,,-10.60,,Shared
2026-01-03,Google,Subscriptions,Michelle's Freedom Unlimited (...9759),GOOGLE *SVCSGDP,,-27.21,,Shared
2026-01-03,Lovable,Subscriptions,Michelle's Freedom Unlimited (...9759),LOVABLE,,-27.19,,Shared
2026-01-03,Lyft,Taxi & Ride Shares,Michelle's Sapphire Reserve (...1041),LYFT *MEMB ANNUAL,,-216.66,,Shared
2026-01-03,Hulu,Subscriptions,Michelle's Marriott Bonvoy Brilliant (...5005),HULU 888-439-4858 CA,,-12.99,,Shared
2026-01-03,UBER EATS,Delivery & Takeout,Gray's Amex Platinum Card (...1007),UBER EATS help.uber.com,,-33.03,,Shared
2026-01-03,Public Service Enterprise Group,Electric & Gas,Venture (...4522),PSEG LI RESIDENTIAL,,-264.97,,Shared
2026-01-02,Platinum Digital Entertainment,Subscriptions,Gray's Amex Platinum Card (...1007),Credit,,25.00,,Shared
2026-01-02,Amazon,Shopping,Amazon Prime Card (...5990),AMAZON MKTPLACE PMTS,,20.34,,Shared
2026-01-02,Nuuly,Shopping,Michelle's Sapphire Reserve (...1041),NUULY,,-363.57,,Shared
2026-01-02,Youtube TV,Youtube TV,Gray's Amex Platinum Card (...1007),GOOGLE *YOUTUBE TV,,-82.99,,Shared
2026-01-02,Breeze Aviation Group,Airline,Gray's Amex Platinum Card (...1007),BREEZE AIRWAYS,,-175.00,,Shared
2026-01-02,Interest Charge,Financial Fees,Michelle's Freedom Unlimited (...9759),PURCHASE INTEREST CHARGE,,-55.09,,Shared
2026-01-02,Ring Premium Plan,Ring Insurance,Venture (...4522),RING PREMIUM PLAN,,2.00,,Shared
2026-01-02,OpenAI,Subscriptions,Venture (...4522),OPENAI *CHATGPT SUBSCR,,-21.78,,Shared
2026-01-02,Membership Fee,Subscriptions,Gray's Amex Platinum Card (...1007),MEMBERSHIP FEE,,-195.00,,Shared
2026-01-02,Walmart+,Shopping,Michelle's Platinum Card (...7008),WMT PLUS JAN 2026,,-14.10,,Shared
2026-01-01,Amazon,Shopping,Amazon Prime Card (...5990),AMAZON MKTPL,,-14.07,,Shared
2026-01-01,Etsy,Shopping,Michelle's Slate Card (...0443),Etsy.com*US,,-10.86,,Shared
2026-01-01,Breeze Aviation Group,Airline,Gray's Amex Platinum Card (...1007),BREEZE AIRWAYS,,-1504.34,,Shared
2026-01-01,American Airlines,Airline,Gray's Amex Platinum Card (...1007),AMERICAN AIRLINES,,-315.48,,Shared`;
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    window.financeTracker = new FinanceTracker();
});
