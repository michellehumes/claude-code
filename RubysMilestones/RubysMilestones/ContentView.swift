import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var children: [Child]
    @Query private var milestones: [Milestone]
    @State private var hasInitialized = false

    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "house.fill")
                }

            MilestoneListView()
                .tabItem {
                    Label("Milestones", systemImage: "list.bullet.clipboard.fill")
                }

            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gearshape.fill")
                }
        }
        .tint(.pink)
        .onAppear {
            initializeDataIfNeeded()
        }
    }

    private func initializeDataIfNeeded() {
        guard !hasInitialized else { return }
        hasInitialized = true

        // Create Ruby if she doesn't exist
        if children.isEmpty {
            // Ruby is 21 months old - calculate birth date
            let calendar = Calendar.current
            let birthDate = calendar.date(byAdding: .month, value: -21, to: Date()) ?? Date()
            let ruby = Child(name: "Ruby", birthDate: birthDate)
            modelContext.insert(ruby)
        }

        // Create milestones if they don't exist
        if milestones.isEmpty {
            for template in MilestoneData.allMilestones {
                let milestone = template.toMilestone()
                modelContext.insert(milestone)
            }
        }

        try? modelContext.save()
    }
}

#Preview {
    ContentView()
        .modelContainer(for: [Child.self, Milestone.self], inMemory: true)
}
