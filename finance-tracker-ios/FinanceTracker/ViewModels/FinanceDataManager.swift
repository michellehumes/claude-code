//
//  FinanceDataManager.swift
//  FinanceTracker
//
//  Manages transaction data and persistence
//

import Foundation
import Combine

class FinanceDataManager: ObservableObject {
    @Published var transactions: [Transaction] = []
    @Published var selectedMonth: Date = Date()

    private let transactionsKey = "saved_transactions"

    init() {
        loadTransactions()
    }

    // MARK: - Data Persistence

    func loadTransactions() {
        if let data = UserDefaults.standard.data(forKey: transactionsKey) {
            if let decoded = try? JSONDecoder().decode([Transaction].self, from: data) {
                transactions = decoded
                return
            }
        }
        // Load sample data if no saved data
        transactions = Transaction.sampleTransactions
    }

    func saveTransactions() {
        if let encoded = try? JSONEncoder().encode(transactions) {
            UserDefaults.standard.set(encoded, forKey: transactionsKey)
        }
    }

    // MARK: - CRUD Operations

    func addTransaction(_ transaction: Transaction) {
        transactions.append(transaction)
        saveTransactions()
    }

    func updateTransaction(_ transaction: Transaction) {
        if let index = transactions.firstIndex(where: { $0.id == transaction.id }) {
            transactions[index] = transaction
            saveTransactions()
        }
    }

    func deleteTransaction(_ transaction: Transaction) {
        transactions.removeAll { $0.id == transaction.id }
        saveTransactions()
    }

    func deleteTransactions(at offsets: IndexSet, from filteredTransactions: [Transaction]) {
        for offset in offsets {
            let transaction = filteredTransactions[offset]
            deleteTransaction(transaction)
        }
    }

    // MARK: - Filtering & Sorting

    func transactionsForMonth(_ date: Date) -> [Transaction] {
        let calendar = Calendar.current
        return transactions.filter { transaction in
            calendar.isDate(transaction.date, equalTo: date, toGranularity: .month)
        }.sorted { $0.date > $1.date }
    }

    func transactionsForCurrentMonth() -> [Transaction] {
        transactionsForMonth(Date())
    }

    func transactionsByCategory(for month: Date) -> [TransactionCategory: [Transaction]] {
        let monthTransactions = transactionsForMonth(month)
        return Dictionary(grouping: monthTransactions) { $0.category }
    }

    // MARK: - Financial Calculations

    func totalIncome(for month: Date) -> Double {
        transactionsForMonth(month)
            .filter { $0.type == .income }
            .reduce(0) { $0 + $1.amount }
    }

    func totalExpenses(for month: Date) -> Double {
        transactionsForMonth(month)
            .filter { $0.type == .expense }
            .reduce(0) { $0 + $1.amount }
    }

    func netCashFlow(for month: Date) -> Double {
        totalIncome(for: month) - totalExpenses(for: month)
    }

    func expensesByCategory(for month: Date) -> [(category: TransactionCategory, amount: Double)] {
        let expenses = transactionsForMonth(month).filter { $0.type == .expense }
        let grouped = Dictionary(grouping: expenses) { $0.category }
        return grouped.map { (category: $0.key, amount: $0.value.reduce(0) { $0 + $1.amount }) }
            .sorted { $0.amount > $1.amount }
    }

    func topExpenseCategories(for month: Date, limit: Int = 5) -> [(category: TransactionCategory, amount: Double)] {
        Array(expensesByCategory(for: month).prefix(limit))
    }

    // MARK: - Utility Functions

    func monthYearString(for date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "MMMM yyyy"
        return formatter.string(from: date)
    }

    func previousMonth() {
        if let newDate = Calendar.current.date(byAdding: .month, value: -1, to: selectedMonth) {
            selectedMonth = newDate
        }
    }

    func nextMonth() {
        if let newDate = Calendar.current.date(byAdding: .month, value: 1, to: selectedMonth) {
            selectedMonth = newDate
        }
    }

    func isCurrentMonth(_ date: Date) -> Bool {
        Calendar.current.isDate(date, equalTo: Date(), toGranularity: .month)
    }

    // MARK: - Sample Data Management

    func resetToSampleData() {
        transactions = Transaction.sampleTransactions
        saveTransactions()
    }

    func clearAllData() {
        transactions = []
        saveTransactions()
    }
}
