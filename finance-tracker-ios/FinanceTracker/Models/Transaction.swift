//
//  Transaction.swift
//  FinanceTracker
//
//  Data model for financial transactions
//

import Foundation

enum TransactionType: String, Codable, CaseIterable {
    case income = "Income"
    case expense = "Expense"

    var color: String {
        switch self {
        case .income: return "green"
        case .expense: return "red"
        }
    }
}

enum TransactionCategory: String, Codable, CaseIterable {
    case housing = "Housing"
    case utilities = "Utilities"
    case groceries = "Groceries"
    case dining = "Dining"
    case transportation = "Transportation"
    case health = "Health"
    case fitness = "Fitness"
    case subscriptions = "Subscriptions"
    case shopping = "Shopping"
    case travel = "Travel"
    case education = "Education"
    case business = "Business"
    case savings = "Savings"
    case salary = "Salary"
    case other = "Other"

    var icon: String {
        switch self {
        case .housing: return "house.fill"
        case .utilities: return "bolt.fill"
        case .groceries: return "cart.fill"
        case .dining: return "fork.knife"
        case .transportation: return "car.fill"
        case .health: return "cross.fill"
        case .fitness: return "figure.walk"
        case .subscriptions: return "arrow.clockwise"
        case .shopping: return "bag.fill"
        case .travel: return "airplane"
        case .education: return "book.fill"
        case .business: return "briefcase.fill"
        case .savings: return "dollarsign.circle.fill"
        case .salary: return "banknote.fill"
        case .other: return "ellipsis.circle.fill"
        }
    }
}

struct Transaction: Identifiable, Codable {
    var id: UUID
    var date: Date
    var description: String
    var category: TransactionCategory
    var type: TransactionType
    var amount: Double
    var account: String
    var owner: String
    var notes: String

    init(id: UUID = UUID(),
         date: Date = Date(),
         description: String = "",
         category: TransactionCategory = .other,
         type: TransactionType = .expense,
         amount: Double = 0.0,
         account: String = "",
         owner: String = "",
         notes: String = "") {
        self.id = id
        self.date = date
        self.description = description
        self.category = category
        self.type = type
        self.amount = amount
        self.account = account
        self.owner = owner
        self.notes = notes
    }

    var formattedAmount: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        return formatter.string(from: NSNumber(value: amount)) ?? "$0.00"
    }

    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        return formatter.string(from: date)
    }

    var shortDate: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "MMM d"
        return formatter.string(from: date)
    }
}

// MARK: - Sample Data
extension Transaction {
    static var sampleTransactions: [Transaction] {
        let calendar = Calendar.current
        let now = Date()

        return [
            Transaction(
                date: calendar.date(byAdding: .day, value: -1, to: now)!,
                description: "Salary - Main Job",
                category: .salary,
                type: .income,
                amount: 4500.00,
                account: "Chase Checking",
                owner: "Michelle",
                notes: "Bi-weekly payroll"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -2, to: now)!,
                description: "Rent Payment",
                category: .housing,
                type: .expense,
                amount: 1800.00,
                account: "Chase Checking",
                owner: "Michelle",
                notes: "Monthly rent"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -3, to: now)!,
                description: "Trader Joes",
                category: .groceries,
                type: .expense,
                amount: 85.50,
                account: "Chase Credit",
                owner: "Michelle",
                notes: "Weekly shopping"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -4, to: now)!,
                description: "Starbucks",
                category: .dining,
                type: .expense,
                amount: 12.00,
                account: "Chase Credit",
                owner: "Michelle",
                notes: "Coffee meeting"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -5, to: now)!,
                description: "LA Fitness",
                category: .fitness,
                type: .expense,
                amount: 50.00,
                account: "Chase Checking",
                owner: "Michelle",
                notes: "Monthly membership"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -6, to: now)!,
                description: "Electric Bill",
                category: .utilities,
                type: .expense,
                amount: 120.00,
                account: "Chase Checking",
                owner: "Michelle",
                notes: "January usage"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -7, to: now)!,
                description: "Amazon",
                category: .shopping,
                type: .expense,
                amount: 67.00,
                account: "Chase Credit",
                owner: "Michelle",
                notes: "Office supplies"
            ),
            Transaction(
                date: calendar.date(byAdding: .day, value: -10, to: now)!,
                description: "Etsy Sales",
                category: .business,
                type: .income,
                amount: 450.00,
                account: "Business Account",
                owner: "Michelle",
                notes: "Wedding planners sold"
            ),
        ]
    }
}
