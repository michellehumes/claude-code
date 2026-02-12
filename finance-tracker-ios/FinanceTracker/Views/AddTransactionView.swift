//
//  AddTransactionView.swift
//  FinanceTracker
//
//  View for adding or editing transactions
//

import SwiftUI

struct AddTransactionView: View {
    @EnvironmentObject var dataManager: FinanceDataManager
    @Environment(\.presentationMode) var presentationMode

    @State private var date = Date()
    @State private var description = ""
    @State private var category: TransactionCategory = .other
    @State private var type: TransactionType = .expense
    @State private var amount = ""
    @State private var account = ""
    @State private var owner = "Michelle"
    @State private var notes = ""

    var transaction: Transaction?
    var isEditing: Bool { transaction != nil }

    init(transaction: Transaction? = nil) {
        self.transaction = transaction

        if let transaction = transaction {
            _date = State(initialValue: transaction.date)
            _description = State(initialValue: transaction.description)
            _category = State(initialValue: transaction.category)
            _type = State(initialValue: transaction.type)
            _amount = State(initialValue: String(format: "%.2f", transaction.amount))
            _account = State(initialValue: transaction.account)
            _owner = State(initialValue: transaction.owner)
            _notes = State(initialValue: transaction.notes)
        }
    }

    var body: some View {
        NavigationView {
            Form {
                // Type Section
                Section(header: Text("Transaction Type")) {
                    Picker("Type", selection: $type) {
                        ForEach(TransactionType.allCases, id: \.self) { type in
                            Text(type.rawValue).tag(type)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                }

                // Basic Info Section
                Section(header: Text("Details")) {
                    TextField("Description", text: $description)

                    Picker("Category", selection: $category) {
                        ForEach(TransactionCategory.allCases, id: \.self) { category in
                            HStack {
                                Image(systemName: category.icon)
                                Text(category.rawValue)
                            }
                            .tag(category)
                        }
                    }

                    HStack {
                        Text("$")
                            .foregroundColor(.secondary)
                        TextField("0.00", text: $amount)
                            .keyboardType(.decimalPad)
                    }

                    DatePicker("Date", selection: $date, displayedComponents: .date)
                }

                // Account Info Section
                Section(header: Text("Account Information")) {
                    TextField("Account (e.g., Chase Checking)", text: $account)
                    TextField("Owner", text: $owner)
                }

                // Notes Section
                Section(header: Text("Notes (Optional)")) {
                    TextEditor(text: $notes)
                        .frame(height: 100)
                }
            }
            .navigationTitle(isEditing ? "Edit Transaction" : "New Transaction")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        presentationMode.wrappedValue.dismiss()
                    }
                }

                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(isEditing ? "Save" : "Add") {
                        saveTransaction()
                    }
                    .disabled(!isFormValid)
                }
            }
        }
    }

    private var isFormValid: Bool {
        !description.isEmpty && !amount.isEmpty && Double(amount) != nil && Double(amount)! > 0
    }

    private func saveTransaction() {
        guard let amountValue = Double(amount) else { return }

        if let existingTransaction = transaction {
            // Update existing transaction
            let updated = Transaction(
                id: existingTransaction.id,
                date: date,
                description: description,
                category: category,
                type: type,
                amount: amountValue,
                account: account,
                owner: owner,
                notes: notes
            )
            dataManager.updateTransaction(updated)
        } else {
            // Create new transaction
            let newTransaction = Transaction(
                date: date,
                description: description,
                category: category,
                type: type,
                amount: amountValue,
                account: account,
                owner: owner,
                notes: notes
            )
            dataManager.addTransaction(newTransaction)
        }

        presentationMode.wrappedValue.dismiss()
    }
}

struct AddTransactionView_Previews: PreviewProvider {
    static var previews: some View {
        AddTransactionView()
            .environmentObject(FinanceDataManager())
    }
}
