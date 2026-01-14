import SwiftUI
import SwiftData

struct DashboardView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var children: [Child]
    @Query private var milestones: [Milestone]

    var child: Child? {
        children.first
    }

    var childAge: Int {
        child?.ageInMonths ?? 21
    }

    var pastMilestones: [Milestone] {
        milestones.filter { $0.expectedAgeMonthsMax < childAge }
    }

    var currentMilestones: [Milestone] {
        milestones.filter { $0.expectedAgeMonthsMin <= childAge && $0.expectedAgeMonthsMax >= childAge }
    }

    var upcomingMilestones: [Milestone] {
        milestones.filter { $0.expectedAgeMonthsMin > childAge && $0.expectedAgeMonthsMin <= childAge + 24 }
    }

    var achievedPastCount: Int {
        pastMilestones.filter { $0.status == .achieved }.count
    }

    var achievedCurrentCount: Int {
        currentMilestones.filter { $0.status == .achieved }.count
    }

    var totalAchieved: Int {
        milestones.filter { $0.status == .achieved }.count
    }

    var earlyAchievements: Int {
        guard let birthDate = child?.birthDate else { return 0 }
        return milestones.filter { milestone in
            guard milestone.status == .achieved else { return false }
            switch milestone.pacingStatus(childBirthDate: birthDate) {
            case .early: return true
            default: return false
            }
        }.count
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Header with tagline
                    headerSection

                    // Quick Stats
                    statsSection

                    // Progress by category
                    categoryProgressSection

                    // Current milestones preview
                    currentMilestonesSection

                    // Upcoming preview
                    upcomingPreviewSection
                }
                .padding()
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private var headerSection: some View {
        VStack(spacing: 8) {
            Text("Ruby's Milestones")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundStyle(
                    LinearGradient(
                        colors: [.pink, .purple],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )

            Text("Ruby is #1, 1, 1!")
                .font(.title2)
                .fontWeight(.semibold)
                .foregroundColor(.pink)

            if let child = child {
                Text(child.ageDescription)
                    .font(.headline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical)
    }

    private var statsSection: some View {
        VStack(spacing: 16) {
            HStack(spacing: 16) {
                StatCard(
                    title: "Achieved",
                    value: "\(totalAchieved)",
                    subtitle: "milestones",
                    icon: "checkmark.circle.fill",
                    color: .green
                )

                StatCard(
                    title: "Early",
                    value: "\(earlyAchievements)",
                    subtitle: "ahead of avg",
                    icon: "arrow.up.circle.fill",
                    color: .blue
                )
            }

            HStack(spacing: 16) {
                StatCard(
                    title: "Past Due",
                    value: "\(pastMilestones.count - achievedPastCount)",
                    subtitle: "to complete",
                    icon: "clock.fill",
                    color: achievedPastCount == pastMilestones.count ? .green : .orange
                )

                StatCard(
                    title: "Current",
                    value: "\(currentMilestones.count)",
                    subtitle: "in progress",
                    icon: "circle.dotted",
                    color: .purple
                )
            }
        }
    }

    private var categoryProgressSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Progress by Category")
                .font(.headline)
                .padding(.horizontal, 4)

            VStack(spacing: 12) {
                ForEach(MilestoneCategory.allCases, id: \.self) { category in
                    CategoryProgressRow(
                        category: category,
                        achieved: categoryAchieved(category),
                        total: categoryTotal(category)
                    )
                }
            }
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(16)
        }
    }

    private var currentMilestonesSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Current Milestones")
                    .font(.headline)

                Spacer()

                NavigationLink {
                    AgeGroupView(ageGroup: .current)
                } label: {
                    Text("See All")
                        .font(.subheadline)
                        .foregroundColor(.pink)
                }
            }
            .padding(.horizontal, 4)

            if currentMilestones.isEmpty {
                Text("No milestones for current age range")
                    .foregroundColor(.secondary)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color(.systemBackground))
                    .cornerRadius(16)
            } else {
                VStack(spacing: 8) {
                    ForEach(currentMilestones.prefix(3), id: \.id) { milestone in
                        NavigationLink {
                            MilestoneDetailView(milestone: milestone)
                        } label: {
                            MilestoneRowView(milestone: milestone, childBirthDate: child?.birthDate)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding()
                .background(Color(.systemBackground))
                .cornerRadius(16)
            }
        }
    }

    private var upcomingPreviewSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Coming Up")
                    .font(.headline)

                Spacer()

                NavigationLink {
                    AgeGroupView(ageGroup: .upcoming)
                } label: {
                    Text("See All")
                        .font(.subheadline)
                        .foregroundColor(.pink)
                }
            }
            .padding(.horizontal, 4)

            if upcomingMilestones.isEmpty {
                Text("No upcoming milestones")
                    .foregroundColor(.secondary)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color(.systemBackground))
                    .cornerRadius(16)
            } else {
                VStack(spacing: 8) {
                    ForEach(upcomingMilestones.prefix(3), id: \.id) { milestone in
                        NavigationLink {
                            MilestoneDetailView(milestone: milestone)
                        } label: {
                            MilestoneRowView(milestone: milestone, childBirthDate: child?.birthDate)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding()
                .background(Color(.systemBackground))
                .cornerRadius(16)
            }
        }
    }

    private func categoryAchieved(_ category: MilestoneCategory) -> Int {
        milestones.filter { $0.category == category && $0.status == .achieved }.count
    }

    private func categoryTotal(_ category: MilestoneCategory) -> Int {
        milestones.filter { $0.category == category }.count
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let subtitle: String
    let icon: String
    let color: Color

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Text(value)
                .font(.title)
                .fontWeight(.bold)

            Text(subtitle)
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
    }
}

struct CategoryProgressRow: View {
    let category: MilestoneCategory
    let achieved: Int
    let total: Int

    var progress: Double {
        total > 0 ? Double(achieved) / Double(total) : 0
    }

    var categoryColor: Color {
        switch category.color {
        case "blue": return .blue
        case "purple": return .purple
        case "orange": return .orange
        case "pink": return .pink
        default: return .gray
        }
    }

    var body: some View {
        VStack(spacing: 8) {
            HStack {
                Image(systemName: category.icon)
                    .foregroundColor(categoryColor)

                Text(category.rawValue)
                    .font(.subheadline)

                Spacer()

                Text("\(achieved)/\(total)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            ProgressView(value: progress)
                .tint(categoryColor)
        }
    }
}

struct MilestoneRowView: View {
    let milestone: Milestone
    let childBirthDate: Date?

    var statusColor: Color {
        switch milestone.status {
        case .achieved: return .green
        case .working: return .orange
        case .notYet: return .gray
        }
    }

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: milestone.status.icon)
                .foregroundColor(statusColor)
                .font(.title3)

            VStack(alignment: .leading, spacing: 4) {
                Text(milestone.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                    .foregroundColor(.primary)

                HStack(spacing: 8) {
                    Text(milestone.category.rawValue)
                        .font(.caption2)
                        .foregroundColor(.secondary)

                    Text("•")
                        .foregroundColor(.secondary)

                    Text("Avg: \(milestone.averageAgeDescription)")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    DashboardView()
        .modelContainer(for: [Child.self, Milestone.self], inMemory: true)
}
