//
//  SettingsView.swift
//  FinanceTracker
//
//  Settings and data management
//

import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var dataManager: FinanceDataManager
    @State private var showingResetAlert = false
    @State private var showingClearAlert = false
    @State private var showingExportSheet = false

    var body: some View {
        NavigationView {
            List {
                // App Info Section
                Section(header: Text("About")) {
                    HStack {
                        Text("App Name")
                        Spacer()
                        Text("Finance Tracker")
                            .foregroundColor(.secondary)
                    }

                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }

                    HStack {
                        Text("Total Transactions")
                        Spacer()
                        Text("\(dataManager.transactions.count)")
                            .foregroundColor(.secondary)
                    }
                }

                // Data Management Section
                Section(header: Text("Data Management")) {
                    Button(action: {
                        showingResetAlert = true
                    }) {
                        HStack {
                            Image(systemName: "arrow.clockwise.circle.fill")
                                .foregroundColor(.blue)
                            Text("Reset to Sample Data")
                                .foregroundColor(.primary)
                        }
                    }

                    Button(action: {
                        exportData()
                    }) {
                        HStack {
                            Image(systemName: "square.and.arrow.up.fill")
                                .foregroundColor(.blue)
                            Text("Export Data")
                                .foregroundColor(.primary)
                        }
                    }

                    Button(action: {
                        showingClearAlert = true
                    }) {
                        HStack {
                            Image(systemName: "trash.fill")
                                .foregroundColor(.red)
                            Text("Clear All Data")
                                .foregroundColor(.red)
                        }
                    }
                }

                // Categories Section
                Section(header: Text("Categories"), footer: Text("Transaction categories are pre-defined and cannot be edited.")) {
                    ForEach(TransactionCategory.allCases, id: \.self) { category in
                        HStack {
                            Image(systemName: category.icon)
                                .foregroundColor(.blue)
                                .frame(width: 30)
                            Text(category.rawValue)
                        }
                    }
                }

                // Support Section
                Section(header: Text("Support")) {
                    Link(destination: URL(string: "https://github.com/michellehumes/claude-code")!) {
                        HStack {
                            Image(systemName: "questionmark.circle.fill")
                                .foregroundColor(.blue)
                            Text("Help & Documentation")
                                .foregroundColor(.primary)
                            Spacer()
                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }

                    Button(action: {
                        shareApp()
                    }) {
                        HStack {
                            Image(systemName: "square.and.arrow.up.fill")
                                .foregroundColor(.blue)
                            Text("Share App")
                                .foregroundColor(.primary)
                        }
                    }
                }

                // Credits Section
                Section(header: Text("Credits")) {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Built for Michelle (Shelzy) Humes")
                            .font(.subheadline)

                        Text("Based on the Excel Life Tracker finance module")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        Text("Created with SwiftUI • February 2026")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                }
            }
            .listStyle(InsetGroupedListStyle())
            .navigationTitle("Settings")
            .alert("Reset to Sample Data", isPresented: $showingResetAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Reset", role: .destructive) {
                    dataManager.resetToSampleData()
                }
            } message: {
                Text("This will replace all your current transactions with sample data. This action cannot be undone.")
            }
            .alert("Clear All Data", isPresented: $showingClearAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Clear", role: .destructive) {
                    dataManager.clearAllData()
                }
            } message: {
                Text("This will permanently delete all your transactions. This action cannot be undone.")
            }
        }
    }

    // MARK: - Export Data
    private func exportData() {
        // In a real app, this would create a CSV or JSON file and share it
        // For now, we'll just show a placeholder
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted

        if let jsonData = try? encoder.encode(dataManager.transactions),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print("Export Data:")
            print(jsonString)

            // In production, use UIActivityViewController to share the file
            // For now, data is printed to console
        }
    }

    // MARK: - Share App
    private func shareApp() {
        // Placeholder for sharing functionality
        // In a real app, this would open UIActivityViewController
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
            .environmentObject(FinanceDataManager())
    }
}
