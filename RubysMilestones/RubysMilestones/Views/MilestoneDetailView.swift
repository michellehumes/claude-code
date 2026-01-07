import SwiftUI
import SwiftData

struct MilestoneDetailView: View {
    @Environment(\.modelContext) private var modelContext
    @Bindable var milestone: Milestone
    @Query private var children: [Child]

    @State private var showingDatePicker = false
    @State private var selectedDate = Date()
    @State private var showingNotes = false

    var child: Child? {
        children.first
    }

    var pacingStatus: PacingStatus? {
        guard let birthDate = child?.birthDate else { return nil }
        return milestone.pacingStatus(childBirthDate: birthDate)
    }

    var detailedExplanation: String? {
        guard let birthDate = child?.birthDate, let childName = child?.name else { return nil }
        return milestone.detailedExplanation(childBirthDate: birthDate, childName: childName)
    }

    var categoryColor: Color {
        switch milestone.category.color {
        case "blue": return .blue
        case "purple": return .purple
        case "orange": return .orange
        case "pink": return .pink
        default: return .gray
        }
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Header
                headerSection

                // Status section
                statusSection

                // Achievement explanation (if achieved)
                if milestone.status == .achieved {
                    explanationSection
                }

                // Expected age info
                ageInfoSection

                // Tips section
                if !milestone.tips.isEmpty {
                    tipsSection
                }

                // Notes section
                notesSection
            }
            .padding()
        }
        .background(Color(.systemGroupedBackground))
        .navigationTitle("")
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showingDatePicker) {
            DatePickerSheet(
                selectedDate: $selectedDate,
                childBirthDate: child?.birthDate ?? Date(),
                onSave: { date in
                    milestone.achievedDate = date
                    milestone.status = .achieved
                    try? modelContext.save()
                }
            )
        }
    }

    private var headerSection: some View {
        VStack(spacing: 12) {
            Image(systemName: milestone.category.icon)
                .font(.system(size: 50))
                .foregroundColor(categoryColor)

            Text(milestone.title)
                .font(.title2)
                .fontWeight(.bold)
                .multilineTextAlignment(.center)

            Text(milestone.milestoneDescription)
                .font(.body)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)

            // Category badge
            Text(milestone.category.rawValue)
                .font(.caption)
                .fontWeight(.medium)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(categoryColor.opacity(0.15))
                .foregroundColor(categoryColor)
                .cornerRadius(20)
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color(.systemBackground))
        .cornerRadius(16)
    }

    private var statusSection: some View {
        VStack(spacing: 16) {
            Text("Status")
                .font(.headline)
                .frame(maxWidth: .infinity, alignment: .leading)

            HStack(spacing: 12) {
                StatusButton(
                    title: "Not Yet",
                    icon: "circle",
                    isSelected: milestone.status == .notYet,
                    color: .gray
                ) {
                    milestone.status = .notYet
                    milestone.achievedDate = nil
                    try? modelContext.save()
                }

                StatusButton(
                    title: "Working On It",
                    icon: "circle.dotted",
                    isSelected: milestone.status == .working,
                    color: .orange
                ) {
                    milestone.status = .working
                    milestone.achievedDate = nil
                    try? modelContext.save()
                }

                StatusButton(
                    title: "Achieved!",
                    icon: "checkmark.circle.fill",
                    isSelected: milestone.status == .achieved,
                    color: .green
                ) {
                    if milestone.status != .achieved {
                        selectedDate = Date()
                        showingDatePicker = true
                    }
                }
            }

            if milestone.status == .achieved, let date = milestone.achievedDate {
                HStack {
                    Image(systemName: "calendar")
                        .foregroundColor(.green)

                    Text("Achieved on \(date.formatted(date: .long, time: .omitted))")
                        .font(.subheadline)

                    Spacer()

                    Button("Change") {
                        selectedDate = date
                        showingDatePicker = true
                    }
                    .font(.caption)
                    .foregroundColor(.pink)
                }
                .padding()
                .background(Color.green.opacity(0.1))
                .cornerRadius(12)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
    }

    private var explanationSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                if let pacing = pacingStatus {
                    Image(systemName: pacing.icon)
                        .foregroundColor(pacingColor(pacing))
                    Text(pacing.description)
                        .font(.headline)
                        .foregroundColor(pacingColor(pacing))
                }
                Spacer()
            }

            if let explanation = detailedExplanation {
                Text(explanation)
                    .font(.body)
                    .foregroundColor(.primary)
                    .lineSpacing(4)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
    }

    private var ageInfoSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Expected Age Range")
                .font(.headline)

            HStack(spacing: 20) {
                VStack {
                    Text("\(milestone.expectedAgeMonthsMin)")
                        .font(.title)
                        .fontWeight(.bold)
                        .foregroundColor(.blue)
                    Text("months")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text("Earliest")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity)

                VStack {
                    Text("\(milestone.averageAgeMonths)")
                        .font(.title)
                        .fontWeight(.bold)
                        .foregroundColor(.purple)
                    Text("months")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text("Average")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity)

                VStack {
                    Text("\(milestone.expectedAgeMonthsMax)")
                        .font(.title)
                        .fontWeight(.bold)
                        .foregroundColor(.orange)
                    Text("months")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text("Latest")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity)
            }

            // Visual range indicator
            GeometryReader { geometry in
                let width = geometry.size.width
                let totalRange = 48 // 0-48 months
                let minPos = CGFloat(milestone.expectedAgeMonthsMin) / CGFloat(totalRange) * width
                let maxPos = CGFloat(milestone.expectedAgeMonthsMax) / CGFloat(totalRange) * width
                let avgPos = CGFloat(milestone.averageAgeMonths) / CGFloat(totalRange) * width

                ZStack(alignment: .leading) {
                    // Background track
                    RoundedRectangle(cornerRadius: 4)
                        .fill(Color(.systemGray5))
                        .frame(height: 8)

                    // Range indicator
                    RoundedRectangle(cornerRadius: 4)
                        .fill(
                            LinearGradient(
                                colors: [.blue, .purple, .orange],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .frame(width: maxPos - minPos, height: 8)
                        .offset(x: minPos)

                    // Average marker
                    Circle()
                        .fill(Color.purple)
                        .frame(width: 16, height: 16)
                        .offset(x: avgPos - 8)
                }
            }
            .frame(height: 16)
            .padding(.top, 8)

            if let childAge = child?.ageInMonths {
                Text(milestone.progressExplanation(childAgeMonths: childAge))
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .padding(.top, 8)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
    }

    private var tipsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "lightbulb.fill")
                    .foregroundColor(.yellow)
                Text("Tips")
                    .font(.headline)
            }

            Text(milestone.tips)
                .font(.body)
                .foregroundColor(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.systemBackground))
        .cornerRadius(16)
    }

    private var notesSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "note.text")
                    .foregroundColor(.blue)
                Text("Notes")
                    .font(.headline)
                Spacer()
            }

            if let notes = milestone.notes, !notes.isEmpty {
                Text(notes)
                    .font(.body)
                    .foregroundColor(.primary)
            }

            Button {
                showingNotes = true
            } label: {
                HStack {
                    Image(systemName: milestone.notes?.isEmpty ?? true ? "plus.circle" : "pencil.circle")
                    Text(milestone.notes?.isEmpty ?? true ? "Add notes" : "Edit notes")
                }
                .font(.subheadline)
                .foregroundColor(.pink)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .sheet(isPresented: $showingNotes) {
            NotesSheet(notes: Binding(
                get: { milestone.notes ?? "" },
                set: { milestone.notes = $0; try? modelContext.save() }
            ))
        }
    }

    private func pacingColor(_ pacing: PacingStatus) -> Color {
        switch pacing {
        case .early: return .green
        case .onTrack: return .blue
        case .delayed: return .orange
        case .notAchieved: return .gray
        }
    }
}

struct StatusButton: View {
    let title: String
    let icon: String
    let isSelected: Bool
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.title2)
                Text(title)
                    .font(.caption)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background(isSelected ? color.opacity(0.15) : Color(.systemGray6))
            .foregroundColor(isSelected ? color : .secondary)
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? color : Color.clear, lineWidth: 2)
            )
        }
    }
}

struct DatePickerSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Binding var selectedDate: Date
    let childBirthDate: Date
    let onSave: (Date) -> Void

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("When did Ruby achieve this milestone?")
                    .font(.headline)
                    .multilineTextAlignment(.center)
                    .padding(.top)

                DatePicker(
                    "Achievement Date",
                    selection: $selectedDate,
                    in: childBirthDate...Date(),
                    displayedComponents: .date
                )
                .datePickerStyle(.graphical)
                .padding()

                Spacer()
            }
            .navigationTitle("Select Date")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        onSave(selectedDate)
                        dismiss()
                    }
                    .fontWeight(.semibold)
                }
            }
        }
    }
}

struct NotesSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Binding var notes: String

    var body: some View {
        NavigationStack {
            VStack {
                TextEditor(text: $notes)
                    .padding()
            }
            .navigationTitle("Notes")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        dismiss()
                    }
                    .fontWeight(.semibold)
                }
            }
        }
    }
}

#Preview {
    NavigationStack {
        MilestoneDetailView(milestone: Milestone(
            title: "First Steps",
            description: "Takes first independent steps",
            category: .motor,
            expectedAgeMonthsMin: 9,
            expectedAgeMonthsMax: 15,
            averageAgeMonths: 12,
            tips: "Hold hands and encourage walking. Celebrate each step!"
        ))
    }
    .modelContainer(for: [Child.self, Milestone.self], inMemory: true)
}
