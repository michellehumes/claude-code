import SwiftUI

struct MilestoneCardView: View {
    let milestone: Milestone
    let childBirthDate: Date?
    let childAge: Int

    var statusColor: Color {
        switch milestone.status {
        case .achieved: return .green
        case .working: return .orange
        case .notYet: return .gray
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

    var pacingInfo: (icon: String, text: String, color: Color)? {
        guard milestone.status == .achieved, let birthDate = childBirthDate else {
            return nil
        }

        let pacing = milestone.pacingStatus(childBirthDate: birthDate)
        switch pacing {
        case .early(let months):
            return ("arrow.up.circle.fill", "\(months) months early!", .green)
        case .onTrack:
            return ("checkmark.circle.fill", "Right on track", .blue)
        case .delayed(let months):
            return ("clock.fill", "\(months) months after average", .orange)
        case .notAchieved:
            return nil
        }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Header
            HStack {
                Image(systemName: milestone.category.icon)
                    .font(.title2)
                    .foregroundColor(categoryColor)

                VStack(alignment: .leading, spacing: 2) {
                    Text(milestone.title)
                        .font(.headline)
                        .foregroundColor(.primary)

                    Text(milestone.category.rawValue)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                Image(systemName: milestone.status.icon)
                    .font(.title2)
                    .foregroundColor(statusColor)
            }

            // Description
            Text(milestone.milestoneDescription)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(2)

            // Age range
            HStack {
                Image(systemName: "calendar")
                    .font(.caption)
                    .foregroundColor(.secondary)

                Text("Expected: \(milestone.expectedAgeRange)")
                    .font(.caption)
                    .foregroundColor(.secondary)

                Text("•")
                    .foregroundColor(.secondary)

                Text("Avg: \(milestone.averageAgeDescription)")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            // Pacing badge (if achieved)
            if let pacing = pacingInfo {
                HStack(spacing: 6) {
                    Image(systemName: pacing.icon)
                    Text(pacing.text)
                        .fontWeight(.medium)
                }
                .font(.caption)
                .foregroundColor(pacing.color)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(pacing.color.opacity(0.15))
                .cornerRadius(20)
            }

            // Status indicator for non-achieved
            if milestone.status != .achieved {
                let progressText = milestone.progressExplanation(childAgeMonths: childAge)
                Text(progressText)
                    .font(.caption)
                    .foregroundColor(childAge > milestone.expectedAgeMonthsMax ? .orange : .blue)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

#Preview {
    VStack(spacing: 16) {
        MilestoneCardView(
            milestone: Milestone(
                title: "Takes First Steps",
                description: "Walks a few steps independently without holding onto anything",
                category: .motor,
                expectedAgeMonthsMin: 9,
                expectedAgeMonthsMax: 15,
                averageAgeMonths: 12,
                status: .achieved,
                achievedDate: Calendar.current.date(byAdding: .month, value: -10, to: Date()),
                tips: "Practice walking while holding hands!"
            ),
            childBirthDate: Calendar.current.date(byAdding: .month, value: -21, to: Date()),
            childAge: 21
        )

        MilestoneCardView(
            milestone: Milestone(
                title: "Uses 50+ Words",
                description: "Has a vocabulary of approximately 50 or more words",
                category: .language,
                expectedAgeMonthsMin: 18,
                expectedAgeMonthsMax: 24,
                averageAgeMonths: 21,
                status: .working,
                tips: "Count all words, even unclear ones!"
            ),
            childBirthDate: Calendar.current.date(byAdding: .month, value: -21, to: Date()),
            childAge: 21
        )
    }
    .padding()
    .background(Color(.systemGroupedBackground))
}
