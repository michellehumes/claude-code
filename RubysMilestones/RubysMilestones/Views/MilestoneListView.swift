import SwiftUI
import SwiftData

enum MilestoneFilter: String, CaseIterable {
    case all = "All"
    case past = "Past"
    case current = "Current"
    case upcoming = "Upcoming"
    case achieved = "Achieved"
    case notAchieved = "Not Achieved"
}

struct MilestoneListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Milestone.averageAgeMonths) private var milestones: [Milestone]
    @Query private var children: [Child]

    @State private var selectedFilter: MilestoneFilter = .all
    @State private var selectedCategory: MilestoneCategory?
    @State private var searchText = ""

    var child: Child? {
        children.first
    }

    var childAge: Int {
        child?.ageInMonths ?? 21
    }

    var filteredMilestones: [Milestone] {
        var result = milestones

        // Apply time-based filter
        switch selectedFilter {
        case .all:
            break
        case .past:
            result = result.filter { $0.expectedAgeMonthsMax < childAge }
        case .current:
            result = result.filter { $0.expectedAgeMonthsMin <= childAge && $0.expectedAgeMonthsMax >= childAge }
        case .upcoming:
            result = result.filter { $0.expectedAgeMonthsMin > childAge }
        case .achieved:
            result = result.filter { $0.status == .achieved }
        case .notAchieved:
            result = result.filter { $0.status != .achieved }
        }

        // Apply category filter
        if let category = selectedCategory {
            result = result.filter { $0.category == category }
        }

        // Apply search filter
        if !searchText.isEmpty {
            result = result.filter {
                $0.title.localizedCaseInsensitiveContains(searchText) ||
                $0.milestoneDescription.localizedCaseInsensitiveContains(searchText)
            }
        }

        return result
    }

    var groupedMilestones: [(String, [Milestone])] {
        let grouped = Dictionary(grouping: filteredMilestones) { milestone -> String in
            let months = milestone.averageAgeMonths
            if months < 12 {
                return "\(months) months"
            } else {
                let years = months / 12
                let remainingMonths = months % 12
                if remainingMonths == 0 {
                    return "\(years) year\(years == 1 ? "" : "s")"
                }
                return "\(years) year\(years == 1 ? "" : "s") \(remainingMonths) mo"
            }
        }

        return grouped.sorted { first, second in
            let firstMonths = filteredMilestones.first { m in
                grouped[first.0]?.contains(where: { $0.id == m.id }) ?? false
            }?.averageAgeMonths ?? 0

            let secondMonths = filteredMilestones.first { m in
                grouped[second.0]?.contains(where: { $0.id == m.id }) ?? false
            }?.averageAgeMonths ?? 0

            return firstMonths < secondMonths
        }
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Filters
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(MilestoneFilter.allCases, id: \.self) { filter in
                            FilterChip(
                                title: filter.rawValue,
                                isSelected: selectedFilter == filter
                            ) {
                                withAnimation {
                                    selectedFilter = filter
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 8)
                }
                .background(Color(.systemBackground))

                // Category filters
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        FilterChip(
                            title: "All Categories",
                            isSelected: selectedCategory == nil
                        ) {
                            withAnimation {
                                selectedCategory = nil
                            }
                        }

                        ForEach(MilestoneCategory.allCases, id: \.self) { category in
                            FilterChip(
                                title: category.rawValue,
                                icon: category.icon,
                                isSelected: selectedCategory == category
                            ) {
                                withAnimation {
                                    selectedCategory = category
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.bottom, 8)
                }
                .background(Color(.systemBackground))

                // Results count
                HStack {
                    Text("\(filteredMilestones.count) milestones")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Spacer()
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                .background(Color(.systemGroupedBackground))

                // Milestones list
                List {
                    ForEach(groupedMilestones, id: \.0) { group, milestones in
                        Section(header: Text(group)) {
                            ForEach(milestones, id: \.id) { milestone in
                                NavigationLink {
                                    MilestoneDetailView(milestone: milestone)
                                } label: {
                                    MilestoneListRow(
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
            }
            .navigationTitle("Milestones")
            .searchable(text: $searchText, prompt: "Search milestones")
        }
    }
}

struct FilterChip: View {
    let title: String
    var icon: String? = nil
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 4) {
                if let icon = icon {
                    Image(systemName: icon)
                        .font(.caption)
                }
                Text(title)
                    .font(.caption)
                    .fontWeight(isSelected ? .semibold : .regular)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(isSelected ? Color.pink : Color(.systemGray5))
            .foregroundColor(isSelected ? .white : .primary)
            .cornerRadius(20)
        }
    }
}

struct MilestoneListRow: View {
    let milestone: Milestone
    let childAge: Int
    let childBirthDate: Date?

    var statusColor: Color {
        switch milestone.status {
        case .achieved: return .green
        case .working: return .orange
        case .notYet: return .gray
        }
    }

    var timingIndicator: (text: String, color: Color)? {
        if milestone.status == .achieved, let birthDate = childBirthDate {
            let pacing = milestone.pacingStatus(childBirthDate: birthDate)
            return (pacing.description, pacingColor(pacing))
        }

        if childAge > milestone.expectedAgeMonthsMax && milestone.status != .achieved {
            let monthsLate = childAge - milestone.expectedAgeMonthsMax
            return ("Expected \(monthsLate) mo ago", .orange)
        }

        if childAge < milestone.expectedAgeMonthsMin {
            let monthsUntil = milestone.expectedAgeMonthsMin - childAge
            return ("In ~\(monthsUntil) months", .blue)
        }

        return nil
    }

    func pacingColor(_ pacing: PacingStatus) -> Color {
        switch pacing {
        case .early: return .green
        case .onTrack: return .blue
        case .delayed: return .orange
        case .notAchieved: return .gray
        }
    }

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: milestone.status.icon)
                .foregroundColor(statusColor)
                .font(.title2)
                .frame(width: 30)

            VStack(alignment: .leading, spacing: 4) {
                Text(milestone.title)
                    .font(.subheadline)
                    .fontWeight(.medium)

                HStack(spacing: 6) {
                    Image(systemName: milestone.category.icon)
                        .font(.caption2)
                    Text(milestone.expectedAgeRange)
                        .font(.caption)
                        .foregroundColor(.secondary)

                    if let timing = timingIndicator {
                        Text("•")
                            .foregroundColor(.secondary)
                        Text(timing.text)
                            .font(.caption)
                            .foregroundColor(timing.color)
                    }
                }
            }
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    MilestoneListView()
        .modelContainer(for: [Child.self, Milestone.self], inMemory: true)
}
