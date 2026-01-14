import SwiftUI

struct ProgressRingView: View {
    let progress: Double
    let lineWidth: CGFloat
    let size: CGFloat
    let color: Color

    init(progress: Double, lineWidth: CGFloat = 8, size: CGFloat = 100, color: Color = .pink) {
        self.progress = min(max(progress, 0), 1)
        self.lineWidth = lineWidth
        self.size = size
        self.color = color
    }

    var body: some View {
        ZStack {
            // Background ring
            Circle()
                .stroke(
                    color.opacity(0.2),
                    lineWidth: lineWidth
                )

            // Progress ring
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    color,
                    style: StrokeStyle(
                        lineWidth: lineWidth,
                        lineCap: .round
                    )
                )
                .rotationEffect(.degrees(-90))
                .animation(.easeInOut(duration: 0.5), value: progress)
        }
        .frame(width: size, height: size)
    }
}

struct ProgressRingWithLabel: View {
    let progress: Double
    let achieved: Int
    let total: Int
    let label: String
    let color: Color

    var body: some View {
        VStack(spacing: 8) {
            ZStack {
                ProgressRingView(progress: progress, color: color)

                VStack(spacing: 2) {
                    Text("\(achieved)")
                        .font(.title2)
                        .fontWeight(.bold)
                    Text("of \(total)")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }

            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
        }
    }
}

#Preview {
    HStack(spacing: 40) {
        ProgressRingWithLabel(
            progress: 0.7,
            achieved: 14,
            total: 20,
            label: "Motor",
            color: .blue
        )

        ProgressRingWithLabel(
            progress: 0.5,
            achieved: 10,
            total: 20,
            label: "Language",
            color: .purple
        )
    }
    .padding()
}
