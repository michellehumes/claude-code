import SwiftUI
import SwiftData

struct SettingsView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var children: [Child]
    @Query private var milestones: [Milestone]

    @State private var showingEditChild = false
    @State private var showingResetConfirmation = false

    var child: Child? {
        children.first
    }

    var achievedCount: Int {
        milestones.filter { $0.status == .achieved }.count
    }

    var workingCount: Int {
        milestones.filter { $0.status == .working }.count
    }

    var body: some View {
        NavigationStack {
            List {
                // Child info section
                Section {
                    if let child = child {
                        HStack(spacing: 16) {
                            Circle()
                                .fill(
                                    LinearGradient(
                                        colors: [.pink, .purple],
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .frame(width: 60, height: 60)
                                .overlay(
                                    Text(String(child.name.prefix(1)))
                                        .font(.title)
                                        .fontWeight(.bold)
                                        .foregroundColor(.white)
                                )

                            VStack(alignment: .leading, spacing: 4) {
                                Text(child.name)
                                    .font(.title2)
                                    .fontWeight(.bold)

                                Text(child.ageDescription)
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)

                                Text("Born \(child.birthDate.formatted(date: .long, time: .omitted))")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.vertical, 8)
                    }

                    Button {
                        showingEditChild = true
                    } label: {
                        Label("Edit Child Info", systemImage: "pencil")
                    }
                } header: {
                    Text("Child")
                }

                // Statistics section
                Section {
                    HStack {
                        Text("Total Milestones")
                        Spacer()
                        Text("\(milestones.count)")
                            .foregroundColor(.secondary)
                    }

                    HStack {
                        Text("Achieved")
                        Spacer()
                        Text("\(achievedCount)")
                            .foregroundColor(.green)
                    }

                    HStack {
                        Text("Working On")
                        Spacer()
                        Text("\(workingCount)")
                            .foregroundColor(.orange)
                    }

                    HStack {
                        Text("Not Started")
                        Spacer()
                        Text("\(milestones.count - achievedCount - workingCount)")
                            .foregroundColor(.secondary)
                    }
                } header: {
                    Text("Statistics")
                }

                // About section
                Section {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }

                    Link(destination: URL(string: "https://www.cdc.gov/ncbddd/actearly/milestones/index.html")!) {
                        HStack {
                            Text("CDC Milestone Resources")
                            Spacer()
                            Image(systemName: "arrow.up.right.square")
                                .foregroundColor(.secondary)
                        }
                    }
                } header: {
                    Text("About")
                } footer: {
                    Text("Milestone data is based on CDC developmental guidelines. Every child develops at their own pace. Consult your pediatrician with any concerns.")
                }

                // Reset section
                Section {
                    Button(role: .destructive) {
                        showingResetConfirmation = true
                    } label: {
                        Label("Reset All Progress", systemImage: "arrow.counterclockwise")
                    }
                } footer: {
                    Text("This will clear all achievement dates and reset all milestones to 'Not Yet' status.")
                }
            }
            .navigationTitle("Settings")
            .sheet(isPresented: $showingEditChild) {
                EditChildSheet(child: child)
            }
            .confirmationDialog(
                "Reset All Progress?",
                isPresented: $showingResetConfirmation,
                titleVisibility: .visible
            ) {
                Button("Reset All", role: .destructive) {
                    resetAllProgress()
                }
                Button("Cancel", role: .cancel) {}
            } message: {
                Text("This will clear all achievement dates and notes. This cannot be undone.")
            }
        }
    }

    private func resetAllProgress() {
        for milestone in milestones {
            milestone.status = .notYet
            milestone.achievedDate = nil
            milestone.notes = nil
        }
        try? modelContext.save()
    }
}

struct EditChildSheet: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss

    let child: Child?

    @State private var name: String = ""
    @State private var birthDate: Date = Date()

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("Name", text: $name)

                    DatePicker(
                        "Birth Date",
                        selection: $birthDate,
                        in: ...Date(),
                        displayedComponents: .date
                    )
                } header: {
                    Text("Child Information")
                }

                Section {
                    let ageMonths = calculateAge()
                    HStack {
                        Text("Current Age")
                        Spacer()
                        Text("\(ageMonths) months")
                            .foregroundColor(.secondary)
                    }
                } header: {
                    Text("Preview")
                }
            }
            .navigationTitle("Edit Child")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        saveChanges()
                        dismiss()
                    }
                    .fontWeight(.semibold)
                    .disabled(name.isEmpty)
                }
            }
            .onAppear {
                if let child = child {
                    name = child.name
                    birthDate = child.birthDate
                }
            }
        }
    }

    private func calculateAge() -> Int {
        let calendar = Calendar.current
        let components = calendar.dateComponents([.month], from: birthDate, to: Date())
        return components.month ?? 0
    }

    private func saveChanges() {
        if let child = child {
            child.name = name
            child.birthDate = birthDate
            try? modelContext.save()
        }
    }
}

#Preview {
    SettingsView()
        .modelContainer(for: [Child.self, Milestone.self], inMemory: true)
}
