//
//  Formatters.swift
//  FinanceTracker
//
//  Utility formatters for currency and dates
//

import Foundation

struct Formatters {
    static let currency: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        formatter.maximumFractionDigits = 2
        return formatter
    }()

    static let currencyShort: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        formatter.maximumFractionDigits = 0
        return formatter
    }()

    static let mediumDate: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .none
        return formatter
    }()

    static let shortDate: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "MMM d"
        return formatter
    }()

    static let monthYear: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "MMMM yyyy"
        return formatter
    }()

    static func formatCurrency(_ amount: Double) -> String {
        currency.string(from: NSNumber(value: amount)) ?? "$0.00"
    }

    static func formatCurrencyShort(_ amount: Double) -> String {
        currencyShort.string(from: NSNumber(value: amount)) ?? "$0"
    }
}
