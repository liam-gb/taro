import Foundation

struct MoonPhase {
    let name: String
    let icon: String
    let meaning: String

    var promptContext: String {
        "\(name) \(icon) — \(meaning)"
    }
}

enum MoonPhaseCalculator {
    private static let phases: [MoonPhase] = [
        MoonPhase(name: "New Moon", icon: "🌑", meaning: "New beginnings, setting intentions, planting seeds"),
        MoonPhase(name: "Waxing Crescent", icon: "🌒", meaning: "Taking action, building momentum, hope emerges"),
        MoonPhase(name: "First Quarter", icon: "🌓", meaning: "Challenges arise, decisions needed, commitment tested"),
        MoonPhase(name: "Waxing Gibbous", icon: "🌔", meaning: "Refining plans, patience required, trust the process"),
        MoonPhase(name: "Full Moon", icon: "🌕", meaning: "Culmination, clarity, emotions heightened, harvest results"),
        MoonPhase(name: "Waning Gibbous", icon: "🌖", meaning: "Gratitude, sharing wisdom, integration"),
        MoonPhase(name: "Last Quarter", icon: "🌗", meaning: "Release, forgiveness, letting go of what no longer serves"),
        MoonPhase(name: "Waning Crescent", icon: "🌘", meaning: "Rest, reflection, preparing for renewal")
    ]

    private static let synodicMonth: Double = 29.53058867

    // Reference new moon: December 30, 2024 22:27 UTC (Unix timestamp)
    private static let referenceNewMoon = Date(timeIntervalSince1970: 1735594020)

    static func current(for date: Date = Date()) -> MoonPhase {
        let daysSinceReference = date.timeIntervalSince(referenceNewMoon) / 86400
        var lunarAge = daysSinceReference.truncatingRemainder(dividingBy: synodicMonth)
        if lunarAge < 0 { lunarAge += synodicMonth }
        // Center each phase window so transitions occur at phase midpoints
        let phaseIndex = Int((lunarAge + synodicMonth / 16) / synodicMonth * 8) % 8
        return phases[phaseIndex]
    }
}
