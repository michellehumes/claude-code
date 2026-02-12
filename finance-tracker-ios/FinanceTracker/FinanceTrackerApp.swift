//
//  FinanceTrackerApp.swift
//  FinanceTracker
//
//  Created by Claude
//  Finance tracking app based on Excel Life Tracker
//

import SwiftUI

@main
struct FinanceTrackerApp: App {
    @StateObject private var dataManager = FinanceDataManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(dataManager)
        }
    }
}
