//
//  DashboardView.swift
//  FinanceTracker
//
//  Main dashboard with monthly summary
//

import SwiftUI

struct DashboardView: View {
    @EnvironmentObject var dataManager: FinanceDataManager
    @State private var selectedMonth = Date()

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Month Selector
                    monthSelector

                    // Summary Cards
                    summaryCards

                    // Recent Transactions
                    recentTransactionsSection

                    // Top Spending Categories
                    topCategoriesSection
                }
                .padding()
            }
            .navigationTitle("Finance Tracker")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    NavigationLink(destination: AddTransactionView()) {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                    }
                }
            }
        }
    }

    // MARK: - Month Selector
    private var monthSelector: some View {
        HStack {
            Button(action: {
                if let newDate = Calendar.current.date(byAdding: .month, value: -1, to: selectedMonth) {
                    selectedMonth = newDate
                }
            }) {
                Image(systemName: "chevron.left")
                    .font(.title2)
                    .foregroundColor(.blue)
            }

            Spacer()

            Text(dataManager.monthYearString(for: selectedMonth))
                .font(.title2)
                .fontWeight(.semibold)

            Spacer()

            Button(action: {
                if let newDate = Calendar.current.date(byAdding: .month, value: 1, to: selectedMonth) {
                    selectedMonth = newDate
                }
            }) {
                Image(systemName: "chevron.right")
                    .font(.title2)
                    .foregroundColor(.blue)
            }
            .disabled(dataManager.isCurrentMonth(selectedMonth))
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }

    // MARK: - Summary Cards
    private var summaryCards: some View {
        VStack(spacing: 16) {
            SummaryCard(
                title: "Total Income",
                amount: dataManager.totalIncome(for: selectedMonth),
                color: .green,
                icon: "arrow.down.circle.fill"
            )

            SummaryCard(
                title: "Total Expenses",
                amount: dataManager.totalExpenses(for: selectedMonth),
                color: .red,
                icon: "arrow.up.circle.fill"
            )

            SummaryCard(
                title: "Net Cash Flow",
                amount: dataManager.netCashFlow(for: selectedMonth),
                color: dataManager.netCashFlow(for: selectedMonth) >= 0 ? .green : .red,
                icon: "dollarsign.circle.fill"
            )
        }
    }

    // MARK: - Recent Transactions
    private var recentTransactionsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Recent Transactions")
                    .font(.headline)
                Spacer()
                NavigationLink("See All") {
                    TransactionsListView()
                }
                .font(.subheadline)
            }

            let recentTransactions = dataManager.transactionsForMonth(selectedMonth).prefix(5)

            if recentTransactions.isEmpty {
                Text("No transactions this month")
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(Array(recentTransactions)) { transaction in
                    NavigationLink(destination: TransactionDetailView(transaction: transaction)) {
                        TransactionRow(transaction: transaction)
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }

    // MARK: - Top Categories
    private var topCategoriesSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Top Spending Categories")
                .font(.headline)

            let topCategories = dataManager.topExpenseCategories(for: selectedMonth, limit: 5)

            if topCategories.isEmpty {
                Text("No expenses this month")
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(topCategories, id: \.category) { item in
                    CategoryRow(category: item.category, amount: item.amount)
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

// MARK: - Summary Card Component
struct SummaryCard: View {
    let title: String
    let amount: Double
    let color: Color
    let icon: String

    var body: some View {
        HStack {
            Image(systemName: icon)
                .font(.title)
                .foregroundColor(color)
                .frame(width: 50)

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline)
                    .foregroundColor(.secondary)

                Text(Formatters.formatCurrency(amount))
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(color)
            }

            Spacer()
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Transaction Row Component
struct TransactionRow: View {
    let transaction: Transaction

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: transaction.category.icon)
                .font(.title3)
                .foregroundColor(.blue)
                .frame(width: 40, height: 40)
                .background(Color.blue.opacity(0.1))
                .cornerRadius(8)

            VStack(alignment: .leading, spacing: 4) {
                Text(transaction.description)
                    .font(.body)
                    .foregroundColor(.primary)

                HStack {
                    Text(transaction.category.rawValue)
                        .font(.caption)
                        .foregroundColor(.secondary)

                    Text("•")
                        .foregroundColor(.secondary)

                    Text(transaction.shortDate)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            Spacer()

            Text(transaction.type == .income ? "+" : "-")
                .font(.body)
                .foregroundColor(transaction.type == .income ? .green : .red)
                + Text(Formatters.formatCurrency(transaction.amount))
                .font(.body)
                .fontWeight(.semibold)
                .foregroundColor(transaction.type == .income ? .green : .red)
        }
        .padding(.vertical, 8)
    }
}

// MARK: - Category Row Component
struct CategoryRow: View {
    let category: TransactionCategory
    let amount: Double

    var body: some View {
        HStack {
            Image(systemName: category.icon)
                .font(.body)
                .foregroundColor(.blue)
                .frame(width: 30)

            Text(category.rawValue)
                .font(.body)

            Spacer()

            Text(Formatters.formatCurrency(amount))
                .font(.body)
                .fontWeight(.semibold)
                .foregroundColor(.primary)
        }
        .padding(.vertical, 6)
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
            .environmentObject(FinanceDataManager())
    }
}
