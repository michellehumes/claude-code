//
//  TransactionDetailView.swift
//  FinanceTracker
//
//  Detailed view of a single transaction
//

import SwiftUI

struct TransactionDetailView: View {
    @EnvironmentObject var dataManager: FinanceDataManager
    @Environment(\.presentationMode) var presentationMode
    @State private var showingEditSheet = false
    @State private var showingDeleteAlert = false

    let transaction: Transaction

    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Amount Card
                amountCard

                // Details Section
                detailsSection

                // Delete Button
                deleteButton
            }
            .padding()
        }
        .navigationTitle("Transaction Details")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button("Edit") {
                    showingEditSheet = true
                }
            }
        }
        .sheet(isPresented: $showingEditSheet) {
            AddTransactionView(transaction: transaction)
        }
        .alert("Delete Transaction", isPresented: $showingDeleteAlert) {
            Button("Cancel", role: .cancel) { }
            Button("Delete", role: .destructive) {
                dataManager.deleteTransaction(transaction)
                presentationMode.wrappedValue.dismiss()
            }
        } message: {
            Text("Are you sure you want to delete this transaction? This action cannot be undone.")
        }
    }

    // MARK: - Amount Card
    private var amountCard: some View {
        VStack(spacing: 12) {
            Image(systemName: transaction.category.icon)
                .font(.system(size: 50))
                .foregroundColor(.blue)
                .frame(width: 80, height: 80)
                .background(Color.blue.opacity(0.1))
                .cornerRadius(16)

            Text(transaction.description)
                .font(.title2)
                .fontWeight(.bold)
                .multilineTextAlignment(.center)

            Text(transaction.type == .income ? "+" : "-")
                .font(.title)
                .foregroundColor(transaction.type == .income ? .green : .red)
                + Text(Formatters.formatCurrency(transaction.amount))
                .font(.title)
                .fontWeight(.bold)
                .foregroundColor(transaction.type == .income ? .green : .red)

            HStack {
                Label(transaction.type.rawValue, systemImage: transaction.type == .income ? "arrow.down.circle.fill" : "arrow.up.circle.fill")
                    .font(.subheadline)
                    .foregroundColor(transaction.type == .income ? .green : .red)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(transaction.type == .income ? Color.green.opacity(0.1) : Color.red.opacity(0.1))
                    .cornerRadius(8)
            }
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color(.systemGray6))
        .cornerRadius(16)
    }

    // MARK: - Details Section
    private var detailsSection: some View {
        VStack(spacing: 16) {
            DetailRow(icon: "tag.fill", label: "Category", value: transaction.category.rawValue)
            DetailRow(icon: "calendar", label: "Date", value: transaction.formattedDate)
            DetailRow(icon: "building.columns.fill", label: "Account", value: transaction.account.isEmpty ? "Not specified" : transaction.account)
            DetailRow(icon: "person.fill", label: "Owner", value: transaction.owner.isEmpty ? "Not specified" : transaction.owner)

            if !transaction.notes.isEmpty {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Image(systemName: "note.text")
                            .foregroundColor(.blue)
                            .frame(width: 30)
                        Text("Notes")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }

                    Text(transaction.notes)
                        .font(.body)
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
    }

    // MARK: - Delete Button
    private var deleteButton: some View {
        Button(action: {
            showingDeleteAlert = true
        }) {
            Label("Delete Transaction", systemImage: "trash.fill")
                .font(.body)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.red)
                .cornerRadius(12)
        }
    }
}

// MARK: - Detail Row Component
struct DetailRow: View {
    let icon: String
    let label: String
    let value: String

    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundColor(.blue)
                .frame(width: 30)

            Text(label)
                .font(.subheadline)
                .foregroundColor(.secondary)

            Spacer()

            Text(value)
                .font(.body)
                .fontWeight(.medium)
        }
    }
}

struct TransactionDetailView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            TransactionDetailView(transaction: Transaction.sampleTransactions[0])
                .environmentObject(FinanceDataManager())
        }
    }
}
