//
//  ChartsView.swift
//  FinanceTracker
//
//  Visual insights and spending analysis
//

import SwiftUI

struct ChartsView: View {
    @EnvironmentObject var dataManager: FinanceDataManager
    @State private var selectedMonth = Date()

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Month Selector
                    monthSelector

                    // Summary Stats
                    summaryStats

                    // Spending by Category
                    categoryBreakdown

                    // Income vs Expenses Comparison
                    incomeExpenseComparison
                }
                .padding()
            }
            .navigationTitle("Insights")
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

    // MARK: - Summary Stats
    private var summaryStats: some View {
        HStack(spacing: 16) {
            StatCard(
                title: "Income",
                value: Formatters.formatCurrencyShort(dataManager.totalIncome(for: selectedMonth)),
                color: .green,
                icon: "arrow.down.circle.fill"
            )

            StatCard(
                title: "Expenses",
                value: Formatters.formatCurrencyShort(dataManager.totalExpenses(for: selectedMonth)),
                color: .red,
                icon: "arrow.up.circle.fill"
            )

            StatCard(
                title: "Net",
                value: Formatters.formatCurrencyShort(dataManager.netCashFlow(for: selectedMonth)),
                color: dataManager.netCashFlow(for: selectedMonth) >= 0 ? .green : .red,
                icon: "dollarsign.circle.fill"
            )
        }
    }

    // MARK: - Category Breakdown
    private var categoryBreakdown: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Spending by Category")
                .font(.headline)

            let categories = dataManager.expensesByCategory(for: selectedMonth)
            let total = dataManager.totalExpenses(for: selectedMonth)

            if categories.isEmpty {
                Text("No expenses this month")
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            } else {
                ForEach(categories, id: \.category) { item in
                    CategoryBreakdownRow(
                        category: item.category,
                        amount: item.amount,
                        percentage: total > 0 ? item.amount / total : 0
                    )
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }

    // MARK: - Income vs Expenses Comparison
    private var incomeExpenseComparison: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Income vs Expenses")
                .font(.headline)

            let income = dataManager.totalIncome(for: selectedMonth)
            let expenses = dataManager.totalExpenses(for: selectedMonth)
            let maxValue = max(income, expenses)

            if maxValue > 0 {
                VStack(spacing: 12) {
                    // Income Bar
                    HStack {
                        Text("Income")
                            .font(.subheadline)
                            .frame(width: 80, alignment: .leading)

                        GeometryReader { geometry in
                            HStack(spacing: 0) {
                                Rectangle()
                                    .fill(Color.green)
                                    .frame(width: geometry.size.width * (income / maxValue))

                                Spacer()
                            }
                        }
                        .frame(height: 30)
                        .background(Color.green.opacity(0.2))
                        .cornerRadius(6)

                        Text(Formatters.formatCurrencyShort(income))
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.green)
                            .frame(width: 70, alignment: .trailing)
                    }

                    // Expenses Bar
                    HStack {
                        Text("Expenses")
                            .font(.subheadline)
                            .frame(width: 80, alignment: .leading)

                        GeometryReader { geometry in
                            HStack(spacing: 0) {
                                Rectangle()
                                    .fill(Color.red)
                                    .frame(width: geometry.size.width * (expenses / maxValue))

                                Spacer()
                            }
                        }
                        .frame(height: 30)
                        .background(Color.red.opacity(0.2))
                        .cornerRadius(6)

                        Text(Formatters.formatCurrencyShort(expenses))
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.red)
                            .frame(width: 70, alignment: .trailing)
                    }
                }
            } else {
                Text("No data for this month")
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, alignment: .center)
                    .padding()
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

// MARK: - Stat Card Component
struct StatCard: View {
    let title: String
    let value: String
    let color: Color
    let icon: String

    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)

            Text(value)
                .font(.headline)
                .fontWeight(.bold)
                .foregroundColor(color)

            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - Category Breakdown Row
struct CategoryBreakdownRow: View {
    let category: TransactionCategory
    let amount: Double
    let percentage: Double

    var body: some View {
        VStack(spacing: 8) {
            HStack {
                Image(systemName: category.icon)
                    .foregroundColor(.blue)
                    .frame(width: 30)

                Text(category.rawValue)
                    .font(.body)

                Spacer()

                VStack(alignment: .trailing, spacing: 2) {
                    Text(Formatters.formatCurrency(amount))
                        .font(.body)
                        .fontWeight(.semibold)

                    Text(String(format: "%.1f%%", percentage * 100))
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            GeometryReader { geometry in
                HStack(spacing: 0) {
                    Rectangle()
                        .fill(Color.blue)
                        .frame(width: geometry.size.width * percentage)

                    Spacer()
                }
            }
            .frame(height: 6)
            .background(Color.blue.opacity(0.2))
            .cornerRadius(3)
        }
        .padding(.vertical, 4)
    }
}

struct ChartsView_Previews: PreviewProvider {
    static var previews: some View {
        ChartsView()
            .environmentObject(FinanceDataManager())
    }
}
