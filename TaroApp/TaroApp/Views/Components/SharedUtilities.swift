import SwiftUI

// MARK: - Haptics

struct Haptics {
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle) {
        UIImpactFeedbackGenerator(style: style).impactOccurred()
    }

    static func notification(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        UINotificationFeedbackGenerator().notificationOccurred(type)
    }

    static func light() { impact(.light) }
    static func medium() { impact(.medium) }
    static func soft() { impact(.soft) }
    static func success() { notification(.success) }
}

// MARK: - String Extensions

extension String {
    func abbreviatedCardName(forSmallSize: Bool) -> String {
        guard forSmallSize else { return self }
        let words = self.split(separator: " ")
        guard words.count > 2 else { return self }
        return words.prefix(2).joined(separator: " ")
    }
}

// MARK: - Time Formatting

/// Formats seconds into a readable time string
func formatElapsedTime(_ seconds: Double) -> String {
    let mins = Int(seconds) / 60
    let secs = Int(seconds) % 60
    if mins > 0 {
        return String(format: "%d:%02d", mins, secs)
    }
    return String(format: "%.1fs", seconds)
}

// MARK: - Card Animation State

struct CardAnimationState {
    var isVisible: Bool = false
    var isFlipped: Bool = false
    var opacity: Double = 0
    var scale: CGFloat = 0.5
    var offset: CGSize = CGSize(width: 0, height: 50)
    var glowOpacity: Double = 0
    var labelOpacity: Double = 0
}
