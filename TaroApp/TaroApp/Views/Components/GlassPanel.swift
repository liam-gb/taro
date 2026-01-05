import SwiftUI

// MARK: - Glass Panel Styles
enum GlassPanelStyle {
    case standard       // Basic glass with subtle background
    case light          // Slightly more visible glass
    case card           // Card-style with gradient and stronger shadow
    case pill           // Pill-shaped for selection items
    case summary        // Summary card with enhanced effects

    var whiteOpacity: Double {
        switch self {
        case .standard, .pill: return 0.03
        case .light: return 0.06
        case .card, .summary: return 0 // Uses gradient instead
        }
    }

    var materialOpacity: Double {
        switch self {
        case .standard, .card: return 0.5
        case .light, .summary: return 0.6
        case .pill: return 0.4
        }
    }

    var usesGradient: Bool {
        self == .card || self == .summary
    }

    var borderOpacity: Double {
        switch self {
        case .standard, .pill: return 0.08
        case .light, .card, .summary: return 0.1
        }
    }

    var shadowOpacity: Double {
        switch self {
        case .standard, .pill: return 0.2
        case .light: return 0.25
        case .card, .summary: return 0.4
        }
    }

    var shadowRadius: CGFloat {
        switch self {
        case .standard: return 16
        case .light, .card: return 20
        case .pill: return 8
        case .summary: return 24
        }
    }

    var shadowY: CGFloat {
        switch self {
        case .standard, .light: return 8
        case .card, .summary: return 12
        case .pill: return 4
        }
    }
}

// MARK: - Glass Panel
// Frosted glass container with the signature Liquid Glass aesthetic
struct GlassPanel<Content: View>: View {
    let style: GlassPanelStyle
    let cornerRadius: CGFloat
    let padding: CGFloat
    let showBorder: Bool
    let glowColor: Color?
    let glowRadius: CGFloat
    @ViewBuilder let content: () -> Content

    init(
        style: GlassPanelStyle = .standard,
        cornerRadius: CGFloat = TaroRadius.xl,
        padding: CGFloat = TaroSpacing.lg,
        showBorder: Bool = true,
        glowColor: Color? = nil,
        glowRadius: CGFloat = 30,
        @ViewBuilder content: @escaping () -> Content
    ) {
        self.style = style
        self.cornerRadius = cornerRadius
        self.padding = padding
        self.showBorder = showBorder
        self.glowColor = glowColor
        self.glowRadius = glowRadius
        self.content = content
    }

    var body: some View {
        content()
            .padding(padding)
            .background(backgroundForStyle)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .overlay(borderOverlay)
            .shadow(color: Color.black.opacity(style.shadowOpacity), radius: style.shadowRadius, y: style.shadowY)
            .modifier(GlowModifier(color: glowColor, radius: glowRadius))
    }

    // MARK: - Background
    @ViewBuilder
    private var backgroundForStyle: some View {
        ZStack {
            if style.usesGradient {
                LinearGradient(
                    colors: [Color.white.opacity(style == .card ? 0.05 : 0.04), Color.white.opacity(0.02)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            } else {
                Color.white.opacity(style.whiteOpacity)
            }
            Material.ultraThinMaterial.opacity(style.materialOpacity)
        }
    }

    // MARK: - Border
    @ViewBuilder
    private var borderOverlay: some View {
        if showBorder {
            RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                .stroke(Color.white.opacity(style.borderOpacity), lineWidth: 1)
                .overlay(
                    RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                        .stroke(
                            LinearGradient(colors: [Color.white.opacity(0.1), .clear], startPoint: .top, endPoint: .bottom),
                            lineWidth: 1
                        )
                        .padding(1)
                )
        }
    }
}

// MARK: - Glow Modifier
private struct GlowModifier: ViewModifier {
    let color: Color?
    let radius: CGFloat

    func body(content: Content) -> some View {
        if let glowColor = color {
            content
                .shadow(color: glowColor.opacity(0.3), radius: radius)
                .shadow(color: glowColor.opacity(0.1), radius: radius * 2)
        } else {
            content
        }
    }
}

// MARK: - Active Glass Panel
// Glass panel with active/selected state styling
struct ActiveGlassPanel<Content: View>: View {
    let isActive: Bool
    let cornerRadius: CGFloat
    let padding: CGFloat
    @ViewBuilder let content: () -> Content

    init(
        isActive: Bool,
        cornerRadius: CGFloat = TaroRadius.xl,
        padding: CGFloat = TaroSpacing.lg,
        @ViewBuilder content: @escaping () -> Content
    ) {
        self.isActive = isActive
        self.cornerRadius = cornerRadius
        self.padding = padding
        self.content = content
    }

    var body: some View {
        content()
            .padding(padding)
            .background(background)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .stroke(borderColor, lineWidth: 1)
            )
            .shadow(color: shadowColor, radius: isActive ? 20 : 8, y: isActive ? 8 : 4)
            .animation(TaroAnimation.springSmooth, value: isActive)
    }

    private var background: some View {
        ZStack {
            if isActive {
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.2),
                        Color.mysticViolet.opacity(0.1)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            } else {
                Color.white.opacity(0.03)
            }
            Material.ultraThinMaterial
                .opacity(isActive ? 0.6 : 0.4)
        }
    }

    private var borderColor: Color {
        isActive ? Color.mysticViolet.opacity(0.4) : Color.white.opacity(0.08)
    }

    private var shadowColor: Color {
        isActive ? Color.mysticViolet.opacity(0.15) : Color.black.opacity(0.2)
    }
}

// MARK: - Iridescent Border Panel
// Glass panel with animated iridescent border effect
struct IridescentGlassPanel<Content: View>: View {
    let cornerRadius: CGFloat
    let padding: CGFloat
    let animationDuration: Double
    @ViewBuilder let content: () -> Content

    @State private var animateGradient = false

    init(
        cornerRadius: CGFloat = TaroRadius.xl,
        padding: CGFloat = TaroSpacing.lg,
        animationDuration: Double = 8,
        @ViewBuilder content: @escaping () -> Content
    ) {
        self.cornerRadius = cornerRadius
        self.padding = padding
        self.animationDuration = animationDuration
        self.content = content
    }

    var body: some View {
        content()
            .padding(padding)
            .background(
                ZStack {
                    Color.white.opacity(0.03)
                    Material.ultraThinMaterial.opacity(0.5)
                }
            )
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .overlay(iridescentBorder)
            .shadow(color: Color.black.opacity(0.3), radius: 16, y: 8)
            .onAppear {
                withAnimation(
                    Animation
                        .linear(duration: animationDuration)
                        .repeatForever(autoreverses: false)
                ) {
                    animateGradient = true
                }
            }
    }

    private var iridescentBorder: some View {
        RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
            .stroke(
                AngularGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.6),
                        Color.mysticCyan.opacity(0.6),
                        Color.mysticPink.opacity(0.5),
                        Color.mysticTeal.opacity(0.5),
                        Color.mysticViolet.opacity(0.6)
                    ],
                    center: .center,
                    angle: .degrees(animateGradient ? 360 : 0)
                ),
                lineWidth: 1
            )
            .opacity(0.6)
    }
}

// MARK: - Glass Divider
struct GlassDivider: View {
    var body: some View {
        Rectangle()
            .fill(
                LinearGradient(
                    colors: [
                        .clear,
                        Color.mysticViolet.opacity(0.3),
                        .clear
                    ],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .frame(height: 1)
    }
}

// MARK: - Convenience Modifiers
extension View {
    /// Apply standard glass panel styling
    func glassPanel(
        style: GlassPanelStyle = .standard,
        cornerRadius: CGFloat = TaroRadius.xl
    ) -> some View {
        self
            .background(
                ZStack {
                    Color.white.opacity(style == .light ? 0.06 : 0.03)
                    Material.ultraThinMaterial.opacity(0.5)
                }
            )
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .stroke(Color.white.opacity(0.08), lineWidth: 1)
            )
            .shadow(color: Color.black.opacity(0.3), radius: 16, y: 8)
    }

    /// Apply glass card styling with gradient background
    func glassCard(cornerRadius: CGFloat = TaroRadius.xl) -> some View {
        self
            .background(
                ZStack {
                    LinearGradient(
                        colors: [
                            Color.white.opacity(0.05),
                            Color.white.opacity(0.02)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                    Material.ultraThinMaterial.opacity(0.5)
                }
            )
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .stroke(Color.white.opacity(0.1), lineWidth: 1)
            )
            .shadow(color: Color.black.opacity(0.4), radius: 20, y: 12)
    }
}

// MARK: - Preview
#Preview("Glass Panels") {
    ZStack {
        AuroraBackground()

        ScrollView {
            VStack(spacing: TaroSpacing.lg) {
                GlassPanel(style: .standard) {
                    VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                        Text("Standard Glass")
                            .font(TaroTypography.headline)
                            .foregroundColor(.textPrimary)
                        Text("Basic frosted glass panel")
                            .font(TaroTypography.subheadline)
                            .foregroundColor(.textSecondary)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                }

                GlassPanel(style: .card) {
                    VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                        Text("Glass Card")
                            .font(TaroTypography.headline)
                            .foregroundColor(.textPrimary)
                        Text("Gradient background with enhanced shadow")
                            .font(TaroTypography.subheadline)
                            .foregroundColor(.textSecondary)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                }

                GlassPanel(
                    style: .card,
                    glowColor: .mysticViolet,
                    glowRadius: 20
                ) {
                    VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                        Text("Glowing Panel")
                            .font(TaroTypography.headline)
                            .foregroundColor(.textPrimary)
                        Text("With violet glow effect")
                            .font(TaroTypography.subheadline)
                            .foregroundColor(.textSecondary)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                }

                ActiveGlassPanel(isActive: true) {
                    Text("Active Selection")
                        .font(TaroTypography.headline)
                        .foregroundColor(.textPrimary)
                        .frame(maxWidth: .infinity)
                }

                IridescentGlassPanel {
                    VStack(spacing: TaroSpacing.sm) {
                        Text("Iridescent Border")
                            .font(TaroTypography.headline)
                            .foregroundColor(.textPrimary)
                        Text("Animated rainbow border")
                            .font(TaroTypography.subheadline)
                            .foregroundColor(.textSecondary)
                    }
                    .frame(maxWidth: .infinity)
                }

                GlassDivider()
                    .padding(.horizontal, TaroSpacing.xl)
            }
            .padding(TaroSpacing.lg)
        }
    }
    .preferredColorScheme(.dark)
}
