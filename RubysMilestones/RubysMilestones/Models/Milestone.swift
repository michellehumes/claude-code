import Foundation
import SwiftData

enum MilestoneCategory: String, Codable, CaseIterable {
    case motor = "Motor Skills"
    case language = "Language & Communication"
    case cognitive = "Cognitive & Learning"
    case social = "Social & Emotional"

    var icon: String {
        switch self {
        case .motor: return "figure.walk"
        case .language: return "bubble.left.and.bubble.right"
        case .cognitive: return "brain.head.profile"
        case .social: return "heart.circle"
        }
    }

    var color: String {
        switch self {
        case .motor: return "blue"
        case .language: return "purple"
        case .cognitive: return "orange"
        case .social: return "pink"
        }
    }
}

enum AchievementStatus: String, Codable {
    case notYet = "Not Yet"
    case achieved = "Achieved"
    case working = "Working On It"

    var icon: String {
        switch self {
        case .notYet: return "circle"
        case .achieved: return "checkmark.circle.fill"
        case .working: return "circle.dotted"
        }
    }
}

enum PacingStatus {
    case early(monthsAhead: Int)
    case onTrack
    case delayed(monthsBehind: Int)
    case notAchieved

    var description: String {
        switch self {
        case .early(let months):
            if months == 1 {
                return "1 month early"
            }
            return "\(months) months early"
        case .onTrack:
            return "Right on track"
        case .delayed(let months):
            if months == 1 {
                return "1 month behind"
            }
            return "\(months) months behind"
        case .notAchieved:
            return "Not yet achieved"
        }
    }

    var color: String {
        switch self {
        case .early: return "green"
        case .onTrack: return "blue"
        case .delayed: return "orange"
        case .notAchieved: return "gray"
        }
    }

    var icon: String {
        switch self {
        case .early: return "arrow.up.circle.fill"
        case .onTrack: return "checkmark.circle.fill"
        case .delayed: return "clock.fill"
        case .notAchieved: return "circle.dashed"
        }
    }
}

@Model
final class Milestone {
    @Attribute(.unique) var id: String
    var title: String
    var milestoneDescription: String
    var categoryRaw: String
    var expectedAgeMonthsMin: Int
    var expectedAgeMonthsMax: Int
    var averageAgeMonths: Int
    var statusRaw: String
    var achievedDate: Date?
    var notes: String?
    var tips: String

    init(
        id: String = UUID().uuidString,
        title: String,
        description: String,
        category: MilestoneCategory,
        expectedAgeMonthsMin: Int,
        expectedAgeMonthsMax: Int,
        averageAgeMonths: Int,
        status: AchievementStatus = .notYet,
        achievedDate: Date? = nil,
        notes: String? = nil,
        tips: String = ""
    ) {
        self.id = id
        self.title = title
        self.milestoneDescription = description
        self.categoryRaw = category.rawValue
        self.expectedAgeMonthsMin = expectedAgeMonthsMin
        self.expectedAgeMonthsMax = expectedAgeMonthsMax
        self.averageAgeMonths = averageAgeMonths
        self.statusRaw = status.rawValue
        self.achievedDate = achievedDate
        self.notes = notes
        self.tips = tips
    }

    var category: MilestoneCategory {
        get { MilestoneCategory(rawValue: categoryRaw) ?? .motor }
        set { categoryRaw = newValue.rawValue }
    }

    var status: AchievementStatus {
        get { AchievementStatus(rawValue: statusRaw) ?? .notYet }
        set { statusRaw = newValue.rawValue }
    }

    var expectedAgeRange: String {
        if expectedAgeMonthsMin == expectedAgeMonthsMax {
            return "\(expectedAgeMonthsMin) months"
        }
        return "\(expectedAgeMonthsMin)-\(expectedAgeMonthsMax) months"
    }

    var averageAgeDescription: String {
        if averageAgeMonths < 12 {
            return "\(averageAgeMonths) months"
        } else {
            let years = averageAgeMonths / 12
            let months = averageAgeMonths % 12
            if months == 0 {
                return "\(years) year\(years == 1 ? "" : "s")"
            }
            return "\(years) year\(years == 1 ? "" : "s"), \(months) month\(months == 1 ? "" : "s")"
        }
    }

    func pacingStatus(childBirthDate: Date) -> PacingStatus {
        guard let achievedDate = achievedDate else {
            return .notAchieved
        }

        let calendar = Calendar.current
        let components = calendar.dateComponents([.month], from: childBirthDate, to: achievedDate)
        let achievedAgeMonths = components.month ?? 0

        let difference = averageAgeMonths - achievedAgeMonths

        if difference > 1 {
            return .early(monthsAhead: difference)
        } else if difference < -1 {
            return .delayed(monthsBehind: abs(difference))
        } else {
            return .onTrack
        }
    }

    func detailedExplanation(childBirthDate: Date, childName: String) -> String {
        guard let achievedDate = achievedDate else {
            return "This milestone hasn't been achieved yet. The typical range is \(expectedAgeRange), with most children reaching it around \(averageAgeDescription)."
        }

        let calendar = Calendar.current
        let components = calendar.dateComponents([.month], from: childBirthDate, to: achievedDate)
        let achievedAgeMonths = components.month ?? 0

        let pacing = pacingStatus(childBirthDate: childBirthDate)

        var explanation = "\(childName) achieved this milestone at \(achievedAgeMonths) months old. "
        explanation += "The average age for this milestone is \(averageAgeDescription), "
        explanation += "with a typical range of \(expectedAgeRange).\n\n"

        switch pacing {
        case .early(let months):
            explanation += "This is \(months) month\(months == 1 ? "" : "s") ahead of the average! "
            explanation += "This is wonderful - \(childName) is developing this skill earlier than most children. "
            explanation += "Early achievement often indicates strong development in this area, though every child develops at their own pace."

        case .onTrack:
            explanation += "\(childName) is right on track! "
            explanation += "Achieving this milestone within the expected range shows healthy, typical development. "
            explanation += "This is exactly what pediatricians hope to see."

        case .delayed(let months):
            explanation += "This is \(months) month\(months == 1 ? "" : "s") after the average. "
            explanation += "Remember that 'average' means half of all children reach this milestone later! "
            explanation += "Development varies widely, and many factors influence timing. "
            explanation += "If \(childName) is still within the typical range (\(expectedAgeRange)), there's usually no cause for concern. "
            if achievedAgeMonths > expectedAgeMonthsMax {
                explanation += "Since this was achieved after the typical range, you may want to discuss with your pediatrician at your next visit, just to ensure everything is on track."
            }

        case .notAchieved:
            break
        }

        return explanation
    }

    func progressExplanation(childAgeMonths: Int) -> String {
        if status == .achieved {
            return "Completed!"
        }

        if childAgeMonths < expectedAgeMonthsMin {
            let monthsUntil = expectedAgeMonthsMin - childAgeMonths
            return "Expected in \(monthsUntil) month\(monthsUntil == 1 ? "" : "s")"
        } else if childAgeMonths >= expectedAgeMonthsMin && childAgeMonths <= expectedAgeMonthsMax {
            return "Now is a typical time for this milestone"
        } else {
            let monthsPast = childAgeMonths - expectedAgeMonthsMax
            return "Typically achieved \(monthsPast) month\(monthsPast == 1 ? "" : "s") ago"
        }
    }
}
