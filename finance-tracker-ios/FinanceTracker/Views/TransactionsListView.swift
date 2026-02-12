//
//  TransactionsListView.swift
//  FinanceTracker
//
//  List view for all transactions with filtering
//

import SwiftUI

struct TransactionsListView: View {
    @EnvironmentObject var dataManager: FinanceDataManager
    @State private var selectedMonth = Date()
    @State private var filterType: TransactionType?
    @State private var filterCategory: TransactionCategory?
    @State private var searchText = ""
    @State private var showingAddSheet = false

    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Month Selector
                monthSelector

                // Filters
                filterSection

                // Transaction List
                transactionsList
            }
            .navigationTitle("Transactions")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddSheet = true }) {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                    }
                }
            }
            .sheet(isPresented: $showingAddSheet) {
                AddTransactionView()
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
                    .font(.title3)
                    .foregroundColor(.blue)
            }

            Spacer()

            Text(dataManager.monthYearString(for: selectedMonth))
                .font(.headline)

            Spacer()

            Button(action: {
                if let newDate = Calendar.current.date(byAdding: .month, value: 1, to: selectedMonth) {
                    selectedMonth = newDate
                }
            }) {
                Image(systemName: "chevron.right")
                    .font(.title3)
                    .foregroundColor(.blue)
            }
            .disabled(dataManager.isCurrentMonth(selectedMonth))
        }
        .padding()
        .background(Color(.systemGray6))
    }

    // MARK: - Filter Section
    private var filterSection: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                // Type Filter
                Menu {
                    Button("All Types") {
                        filterType = nil
                    }
                    ForEach(TransactionType.allCases, id: \.self) { type in
                        Button(type.rawValue) {
                            filterType = type
                        }
                    }
                } label: {
                    HStack {
                        Text(filterType?.rawValue ?? "Type")
                            .font(.subheadline)
                        Image(systemName: "chevron.down")
                            .font(.caption)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(filterType != nil ? Color.blue : Color(.systemGray5))
                    .foregroundColor(filterType != nil ? .white : .primary)
                    .cornerRadius(8)
                }

                // Category Filter
                Menu {
                    Button("All Categories") {
                        filterCategory = nil
                    }
                    ForEach(TransactionCategory.allCases, id: \.self) { category in
                        Button(action: { filterCategory = category }) {
                            HStack {
                                Image(systemName: category.icon)
                                Text(category.rawValue)
                            }
                        }
                    }
                } label: {
                    HStack {
                        Text(filterCategory?.rawValue ?? "Category")
                            .font(.subheadline)
                        Image(systemName: "chevron.down")
                            .font(.caption)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(filterCategory != nil ? Color.blue : Color(.systemGray5))
                    .foregroundColor(filterCategory != nil ? .white : .primary)
                    .cornerRadius(8)
                }

                // Clear Filters
                if filterType != nil || filterCategory != nil {
                    Button(action: {
                        filterType = nil
                        filterCategory = nil
                    }) {
                        HStack {
                            Text("Clear")
                                .font(.subheadline)
                            Image(systemName: "xmark.circle.fill")
                                .font(.caption)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .background(Color.red.opacity(0.1))
                        .foregroundColor(.red)
                        .cornerRadius(8)
                    }
                }
            }
            .padding(.horizontal)
        }
        .padding(.vertical, 8)
        .background(Color(.systemBackground))
    }

    // MARK: - Transactions List
    private var transactionsList: some View {
        List {
            ForEach(filteredTransactions) { transaction in
                NavigationLink(destination: TransactionDetailView(transaction: transaction)) {
                    TransactionRow(transaction: transaction)
                }
            }
            .onDelete { offsets in
                dataManager.deleteTransactions(at: offsets, from: filteredTransactions)
            }
        }
        .listStyle(PlainListStyle())
        .overlay {
            if filteredTransactions.isEmpty {
                VStack(spacing: 16) {
                    Image(systemName: "tray")
                        .font(.system(size: 60))
                        .foregroundColor(.secondary)

                    Text("No Transactions")
                        .font(.title3)
                        .fontWeight(.semibold)

                    Text("Add your first transaction to get started")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)

                    Button(action: { showingAddSheet = true }) {
                        Text("Add Transaction")
                            .fontWeight(.semibold)
                            .padding(.horizontal, 24)
                            .padding(.vertical, 12)
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                }
                .padding()
            }
        }
    }

    // MARK: - Filtered Transactions
    private var filteredTransactions: [Transaction] {
        var transactions = dataManager.transactionsForMonth(selectedMonth)

        if let type = filterType {
            transactions = transactions.filter { $0.type == type }
        }

        if let category = filterCategory {
            transactions = transactions.filter { $0.category == category }
        }

        if !searchText.isEmpty {
            transactions = transactions.filter {
                $0.description.lowercased().contains(searchText.lowercased()) ||
                $0.notes.lowercased().contains(searchText.lowercased())
            }
        }

        return transactions
    }
}

struct TransactionsListView_Previews: PreviewProvider {
    static var previews: some View {
        TransactionsListView()
            .environmentObject(FinanceDataManager())
    }
}
