import SwiftUI
import SwiftData

enum AgeGroup: String, CaseIterable {
    case past = "Past"
    case current = "Current"
    case upcoming = "Upcoming"

    var description: String {
        switch self {
        case .past: return "Milestones Ruby should have already reached"
        case .current: return "Milestones expected at Ruby's current age"
        case .upcoming: return "Milestones coming in the next 2 years"
        }
    }

    var icon: String {
        switch self {
        case .past: return "clock.arrow.circlepath"
        case .current: return "circle.dotted"
        case .upcoming: return "arrow.forward.circle"
        }
    }

    var color: Color {
        switch self {
        case .past: return .orange
        case .current: return .purple
        case .upcoming: return .blue
        }
    }
}

struct AgeGroupView: View {
    @Query(sort: \Milestone.averageAgeMonths) private var milestones: [Milestone]
    @Query private var children: [Child]

    let ageGroup: AgeGroup

    var child: Child? {
        children.first
    }

    var childAge: Int {
        child?.ageInMonths ?? 21
    }

    var filteredMilestones: [Milestone] {
        switch ageGroup {
        case .past:
            return milestones.filter { $0.expectedAgeMonthsMax < childAge }
        case .current:
            return milestones.filter { $0.expectedAgeMonthsMin <= childAge && $0.expectedAgeMonthsMax >= childAge }
        case .upcoming:
            return milestones.filter { $0.expectedAgeMonthsMin > childAge && $0.expectedAgeMonthsMin <= childAge + 24 }
        }
    }

    var achievedCount: Int {
        filteredMilestones.filter { $0.status == .achieved }.count
    }

    var groupedByAge: [(String, [Milestone])] {
        let grouped = Dictionary(grouping: filteredMilestones) { milestone -> Int in
            return milestone.averageAgeMonths
        }

        return grouped.sorted { $0.key < $1.key }.map { key, value in
            let label = formatAge(months: key)
            return (label, value.sorted { $0.title < $1.title })
        }
    }

    var body: some View {
        List {
            // Summary section
            Section {
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Image(systemName: ageGroup.icon)
                            .font(.title)
                            .foregroundColor(ageGroup.color)

                        VStack(alignment: .leading) {
                            Text("\(ageGroup.rawValue) Milestones")
                                .font(.headline)
                            Text(ageGroup.description)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }

                    HStack(spacing: 20) {
                        VStack {
                            Text("\(filteredMilestones.count)")
                                .font(.title2)
                                .fontWeight(.bold)
                            Text("Total")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }

                        Divider()
                            .frame(height: 40)

                        VStack {
                            Text("\(achievedCount)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.green)
                            Text("Achieved")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }

                        Divider()
                            .frame(height: 40)

                        VStack {
                            Text("\(filteredMilestones.count - achievedCount)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(ageGroup == .past ? .orange : .gray)
                            Text("Remaining")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    .frame(maxWidth: .infinity)
                }
                .padding(.vertical, 8)
            }

            // Milestones grouped by age
            ForEach(groupedByAge, id: \.0) { ageLabel, milestones in
                Section(header: Text(ageLabel)) {
                    ForEach(milestones, id: \.id) { milestone in
                        NavigationLink {
                            MilestoneDetailView(milestone: milestone)
                        } label: {
                            AgeGroupMilestoneRow(
                                milestone: milestone,
                                childAge: childAge,
                                childBirthDate: child?.birthDate
                            )
                        }
                    }
                }
            }
        }
        .listStyle(.insetGrouped)
        .navigationTitle(ageGroup.rawValue)
    }

    private func formatAge(months: Int) -> String {
        if months < 12 {
            return "\(months) months"
        } else {
            let years = months / 12
            let remainingMonths = months % 12
            if remainingMonths == 0 {
                return "\(years) year\(years == 1 ? "" : "s")"
            }
            return "\(years)y \(remainingMonths)m"
        }
    }
}

struct AgeGroupMilestoneRow: View {
    let milestone: Milestone
    let childAge: Int
    let childBirthDate: Date?

    var statusIcon: String {
        milestone.status.icon
    }

    var statusColor: Color {
        switch milestone.status {
        case .achieved: return .green
        case .working: return .orange
        case .notYet: return .gray
        }
    }

    var pacingBadge: (text: String, color: Color)? {
        guard milestone.status == .achieved, let birthDate = childBirthDate else {
            return nil
        }

        let pacing = milestone.pacingStatus(childBirthDate: birthDate)
        switch pacing {
        case .early(let months):
            return ("\(months)m early", .green)
        case .delayed(let months):
            return ("\(months)m late", .orange)
        case .onTrack:
            return ("On track", .blue)
        case .notAchieved:
            return nil
        }
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
        HStack(spacing: 12) {
            Image(systemName: statusIcon)
                .foregroundColor(statusColor)
                .font(.title3)
                .frame(width: 28)

            VStack(alignment: .leading, spacing: 4) {
                Text(milestone.title)
                    .font(.subheadline)
                    .fontWeight(.medium)

                HStack(spacing: 6) {
                    Image(systemName: milestone.category.icon)
                        .font(.caption2)
                        .foregroundColor(categoryColor)

                    Text(milestone.category.rawValue)
                        .font(.caption)
                        .foregroundColor(.secondary)

                    if let badge = pacingBadge {
                        Text("•")
                            .foregroundColor(.secondary)
                        Text(badge.text)
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundColor(badge.color)
                    }
                }
            }

            Spacer()
        }
        .padding(.vertical, 2)
    }
}

#Preview {
    NavigationStack {
        AgeGroupView(ageGroup: .current)
    }
    .modelContainer(for: [Child.self, Milestone.self], inMemory: true)
}
