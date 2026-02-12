//
//  ContentView.swift
//  FinanceTracker
//
//  Main navigation view
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var dataManager: FinanceDataManager

    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "chart.pie.fill")
                }

            TransactionsListView()
                .tabItem {
                    Label("Transactions", systemImage: "list.bullet")
                }

            ChartsView()
                .tabItem {
                    Label("Insights", systemImage: "chart.bar.fill")
                }

            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
        }
        .accentColor(.blue)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(FinanceDataManager())
    }
}
