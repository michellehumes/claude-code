import Foundation
import SwiftData

@Model
final class Child {
    var name: String
    var birthDate: Date
    var photoData: Data?

    init(name: String, birthDate: Date, photoData: Data? = nil) {
        self.name = name
        self.birthDate = birthDate
        self.photoData = photoData
    }

    var ageInMonths: Int {
        let calendar = Calendar.current
        let components = calendar.dateComponents([.month], from: birthDate, to: Date())
        return components.month ?? 0
    }

    var ageDescription: String {
        let months = ageInMonths
        if months < 12 {
            return "\(months) month\(months == 1 ? "" : "s") old"
        } else {
            let years = months / 12
            let remainingMonths = months % 12
            if remainingMonths == 0 {
                return "\(years) year\(years == 1 ? "" : "s") old"
            } else {
                return "\(years) year\(years == 1 ? "" : "s"), \(remainingMonths) month\(remainingMonths == 1 ? "" : "s") old"
            }
        }
    }

    func ageInMonthsAt(date: Date) -> Int {
        let calendar = Calendar.current
        let components = calendar.dateComponents([.month], from: birthDate, to: date)
        return components.month ?? 0
    }
}
