import SwiftUI

// MARK: - Liquid Glass Design System
// "Jony Ive on Acid" - A mystical, ethereal interface with glassmorphism and aurora effects

// MARK: - Color Palette
extension Color {
    // Primary mystical colors
    static let mysticViolet = Color(hex: "8B5CF6")           // Primary violet
    static let deepViolet = Color(hex: "7C3AED")             // Darker violet
    static let lightViolet = Color(hex: "A78BFA")            // Lighter violet

    // Aurora accent colors
    static let mysticCyan = Color(hex: "06B6D4")             // Cyan accent
    static let mysticTeal = Color(hex: "14B8A6")             // Teal accent
    static let mysticPink = Color(hex: "EC4899")             // Pink accent
    static let mysticIndigo = Color(hex: "818CF8")           // Indigo accent
    static let mysticEmerald = Color(hex: "6EE7B7")          // Emerald accent

    // Background colors
    static let deepSpace = Color(hex: "0A0A0F")              // Main background
    static let deepSpaceLight = Color(hex: "0D0D14")         // Slightly lighter
    static let deepPurple = Color(hex: "1A0A2E")             // Deep purple bg

    // Text colors
    static let textPrimary = Color(hex: "E2E8F0")            // Primary text
    static let textSecondary = Color(hex: "94A3B8")          // Secondary text
    static let textMuted = Color(hex: "64748B")              // Muted text

    // Glass colors
    static let glassWhite = Color.white.opacity(0.03)
    static let glassBorder = Color.white.opacity(0.08)
    static let glassHighlight = Color.white.opacity(0.1)

    // Initialize from hex string
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// MARK: - Gradients
struct TaroGradients {
    // Aurora background gradient
    static let auroraBackground = LinearGradient(
        colors: [.deepSpace, .deepSpaceLight, .deepSpace],
        startPoint: .top,
        endPoint: .bottom
    )

    // Primary button gradient
    static let primaryButton = LinearGradient(
        colors: [
            Color.mysticViolet.opacity(0.15),
            Color.mysticViolet.opacity(0.05)
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    // Active button/selection gradient
    static let activeSelection = LinearGradient(
        colors: [
            Color.mysticViolet.opacity(0.2),
            Color.mysticViolet.opacity(0.1)
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    // Glass card gradient
    static let glassCard = LinearGradient(
        colors: [
            Color.white.opacity(0.05),
            Color.white.opacity(0.02)
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    // Iridescent border gradient
    static let iridescentBorder = LinearGradient(
        colors: [
            Color.mysticViolet.opacity(0.5),
            Color.mysticCyan.opacity(0.5),
            Color.mysticPink.opacity(0.5),
            Color(hex: "F59E0B").opacity(0.3),
            Color.mysticViolet.opacity(0.5)
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    // Shimmer text gradient
    static let shimmerText = LinearGradient(
        colors: [
            Color.lightViolet,
            Color.mysticIndigo,
            Color.mysticEmerald,
            Color.lightViolet
        ],
        startPoint: .leading,
        endPoint: .trailing
    )

    // Divider gradient
    static let divider = LinearGradient(
        colors: [
            .clear,
            Color.mysticViolet.opacity(0.3),
            .clear
        ],
        startPoint: .leading,
        endPoint: .trailing
    )

    // Violet glow
    static let violetGlow = RadialGradient(
        colors: [
            Color.mysticViolet.opacity(0.4),
            Color.clear
        ],
        center: .center,
        startRadius: 0,
        endRadius: 300
    )

    // Cyan glow
    static let cyanGlow = RadialGradient(
        colors: [
            Color.mysticCyan.opacity(0.3),
            Color.clear
        ],
        center: .center,
        startRadius: 0,
        endRadius: 250
    )

    // Pink glow
    static let pinkGlow = RadialGradient(
        colors: [
            Color.mysticPink.opacity(0.25),
            Color.clear
        ],
        center: .center,
        startRadius: 0,
        endRadius: 200
    )

    // Teal glow
    static let tealGlow = RadialGradient(
        colors: [
            Color.mysticTeal.opacity(0.2),
            Color.clear
        ],
        center: .center,
        startRadius: 0,
        endRadius: 175
    )
}

// MARK: - Typography
struct TaroTypography {
    // Mystical display font - for titles and headings
    static func mystical(_ size: CGFloat, weight: Font.Weight = .light) -> Font {
        .system(size: size, weight: weight, design: .serif)
    }

    // Modern ethereal font - for body text
    static func ethereal(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight, design: .default)
    }

    // Preset sizes
    static let largeTitle = mystical(34, weight: .light)
    static let title = mystical(28, weight: .light)
    static let title2 = mystical(22, weight: .light)
    static let title3 = mystical(20, weight: .regular)

    static let headline = ethereal(17, weight: .semibold)
    static let subheadline = ethereal(15, weight: .regular)
    static let body = ethereal(17, weight: .regular)
    static let callout = ethereal(16, weight: .regular)
    static let footnote = ethereal(13, weight: .regular)
    static let caption = ethereal(12, weight: .regular)
    static let caption2 = ethereal(11, weight: .regular)
}

// MARK: - Spacing Scale
struct TaroSpacing {
    static let xxxs: CGFloat = 2
    static let xxs: CGFloat = 4
    static let xs: CGFloat = 8
    static let sm: CGFloat = 12
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 48
    static let xxxl: CGFloat = 64
}

// MARK: - Corner Radii
struct TaroRadius {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 12
    static let lg: CGFloat = 16
    static let xl: CGFloat = 20
    static let xxl: CGFloat = 24
    static let full: CGFloat = 9999
}

// MARK: - Shadows
struct TaroShadows {
    // Soft glass shadow
    static func glass() -> some View {
        Color.black.opacity(0.3)
            .blur(radius: 16)
            .offset(y: 8)
    }

    // Violet glow shadow
    static func violetGlow() -> some View {
        Color.mysticViolet.opacity(0.3)
            .blur(radius: 30)
    }

    // Cyan glow shadow
    static func cyanGlow() -> some View {
        Color.mysticCyan.opacity(0.3)
            .blur(radius: 30)
    }

    // Pink glow shadow
    static func pinkGlow() -> some View {
        Color.mysticPink.opacity(0.3)
            .blur(radius: 30)
    }
}

// MARK: - Animation Durations
struct TaroAnimation {
    static let quick: Double = 0.2
    static let standard: Double = 0.3
    static let smooth: Double = 0.4
    static let slow: Double = 0.6
    static let aurora: Double = 20.0  // Aurora orb animation cycle

    // Spring animations
    static let springBouncy = Animation.spring(response: 0.4, dampingFraction: 0.7, blendDuration: 0)
    static let springSmooth = Animation.spring(response: 0.5, dampingFraction: 0.8, blendDuration: 0)
    static let springGentle = Animation.spring(response: 0.6, dampingFraction: 0.9, blendDuration: 0)

    // Easing curves
    static let easeOutQuart = Animation.timingCurve(0.25, 1, 0.5, 1, duration: standard)
    static let easeInOutCubic = Animation.timingCurve(0.65, 0, 0.35, 1, duration: smooth)
}

// MARK: - View Modifiers
extension View {
    // Apply mystical text style
    func mysticalText(_ size: CGFloat = 17, weight: Font.Weight = .light) -> some View {
        self
            .font(TaroTypography.mystical(size, weight: weight))
            .tracking(size * 0.3 / 17) // Proportional letter spacing
            .foregroundColor(.textPrimary)
    }

    // Apply ethereal text style
    func etherealText(_ size: CGFloat = 17, weight: Font.Weight = .regular) -> some View {
        self
            .font(TaroTypography.ethereal(size, weight: weight))
            .tracking(0.02 * size)
            .foregroundColor(.textPrimary)
    }

    // Glow effect
    func glowEffect(_ color: Color = .mysticViolet, radius: CGFloat = 30, opacity: Double = 0.3) -> some View {
        self
            .shadow(color: color.opacity(opacity), radius: radius)
            .shadow(color: color.opacity(opacity * 0.5), radius: radius * 2)
    }

    // Soft shadow for glass elements
    func glassShadow() -> some View {
        self
            .shadow(color: Color.black.opacity(0.3), radius: 16, y: 8)
            .shadow(color: Color.white.opacity(0.05), radius: 1, y: -1)
    }
}

// MARK: - Preview
#Preview {
    ZStack {
        Color.deepSpace.ignoresSafeArea()

        VStack(spacing: TaroSpacing.lg) {
            Text("Liquid Glass")
                .font(TaroTypography.largeTitle)
                .foregroundColor(.textPrimary)

            Text("Design System")
                .font(TaroTypography.title2)
                .foregroundColor(.textSecondary)

            HStack(spacing: TaroSpacing.md) {
                Circle()
                    .fill(Color.mysticViolet)
                    .frame(width: 40, height: 40)
                Circle()
                    .fill(Color.mysticCyan)
                    .frame(width: 40, height: 40)
                Circle()
                    .fill(Color.mysticPink)
                    .frame(width: 40, height: 40)
                Circle()
                    .fill(Color.mysticTeal)
                    .frame(width: 40, height: 40)
            }
        }
    }
    .preferredColorScheme(.dark)
}
