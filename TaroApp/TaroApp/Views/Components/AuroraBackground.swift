import SwiftUI

// MARK: - Aurora Background
// Animated gradient background with slow-moving orbs
// Creates the mystical "Liquid Glass" atmosphere

struct AuroraBackground: View {
    var showRibbons: Bool = false
    @State private var animateOrbs = false

    // Orb configuration to avoid duplication
    private struct OrbConfig {
        let color: Color
        let sizeMultiplier: CGFloat
        let xMultiplier: CGFloat
        let yMultiplier: CGFloat
        let opacity: CGFloat
        let duration: Double
        let reverse: Bool
        let delay: Double

        func position(for size: CGSize) -> CGPoint {
            CGPoint(x: size.width * xMultiplier, y: size.height * yMultiplier)
        }
    }

    private let orbConfigs: [OrbConfig] = [
        OrbConfig(color: .mysticViolet, sizeMultiplier: 1.5, xMultiplier: -0.2, yMultiplier: -0.15, opacity: 0.4, duration: 15, reverse: false, delay: 0),
        OrbConfig(color: .mysticCyan, sizeMultiplier: 1.25, xMultiplier: 1.1, yMultiplier: 0.4, opacity: 0.3, duration: 20, reverse: true, delay: 0),
        OrbConfig(color: .mysticPink, sizeMultiplier: 1.0, xMultiplier: 0.3, yMultiplier: 1.1, opacity: 0.25, duration: 18, reverse: false, delay: 5),
        OrbConfig(color: .mysticTeal, sizeMultiplier: 0.9, xMultiplier: -0.15, yMultiplier: 0.6, opacity: 0.2, duration: 22, reverse: false, delay: 3)
    ]

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Base gradient background
                LinearGradient(
                    colors: [.deepSpace, .deepSpaceLight, .deepSpace],
                    startPoint: .top,
                    endPoint: .bottom
                )

                // Aurora orbs (generated from config)
                ForEach(0..<orbConfigs.count, id: \.self) { index in
                    let config = orbConfigs[index]
                    AuroraOrb(
                        color: config.color,
                        size: geometry.size.width * config.sizeMultiplier,
                        position: config.position(for: geometry.size),
                        opacity: config.opacity,
                        animationDuration: config.duration,
                        animateOrbs: animateOrbs,
                        reverse: config.reverse,
                        delay: config.delay
                    )
                }

                // Optional ribbons
                if showRibbons {
                    auroraRibbons(in: geometry)
                }
            }
        }
        .ignoresSafeArea()
        .onAppear {
            animateOrbs = true
        }
        .onDisappear {
            animateOrbs = false
        }
    }

    @ViewBuilder
    private func auroraRibbons(in geometry: GeometryProxy) -> some View {
        AuroraRibbon(yPosition: geometry.size.height * 0.1, rotation: -5, duration: 20, delay: 0)
        AuroraRibbon(yPosition: geometry.size.height * 0.5, rotation: 3, duration: 25, delay: 5)
        AuroraRibbon(yPosition: geometry.size.height * 0.75, rotation: -2, duration: 22, delay: 10)
    }
}

// MARK: - Aurora Orb Component
struct AuroraOrb: View {
    let color: Color
    let size: CGFloat
    let position: CGPoint
    let opacity: CGFloat
    let animationDuration: Double
    var animateOrbs: Bool
    var reverse: Bool = false
    var delay: Double = 0

    @State private var phase: CGFloat = 0

    var body: some View {
        Circle()
            .fill(
                RadialGradient(
                    colors: [
                        color.opacity(opacity),
                        color.opacity(opacity * 0.5),
                        Color.clear
                    ],
                    center: .center,
                    startRadius: 0,
                    endRadius: size / 2
                )
            )
            .frame(width: size, height: size)
            .blur(radius: 80)
            .blendMode(.screen)
            .position(animatedPosition)
            .scaleEffect(animatedScale)
            .onAppear {
                startAnimationIfNeeded()
            }
            .onChange(of: animateOrbs) { _, newValue in
                if newValue {
                    startAnimationIfNeeded()
                } else {
                    // Stop animation by resetting phase without animation
                    withAnimation(.linear(duration: 0.1)) {
                        phase = 0
                    }
                }
            }
    }

    private func startAnimationIfNeeded() {
        guard animateOrbs else { return }
        withAnimation(
            Animation
                .easeInOut(duration: animationDuration)
                .repeatForever(autoreverses: true)
                .delay(delay)
        ) {
            phase = 1
        }
    }

    private var animatedPosition: CGPoint {
        let xOffset: CGFloat = reverse ? -30 : 30
        let yOffset: CGFloat = reverse ? 20 : -20

        return CGPoint(
            x: position.x + (phase * xOffset),
            y: position.y + (phase * yOffset)
        )
    }

    private var animatedScale: CGFloat {
        let baseScale: CGFloat = 1.0
        let scaleVariation: CGFloat = reverse ? 0.1 : 0.15
        return baseScale + (phase * scaleVariation) - (scaleVariation / 2)
    }
}

// MARK: - Aurora Ribbon
// Optional: Horizontal flowing aurora ribbons for additional effect
struct AuroraRibbon: View {
    let yPosition: CGFloat
    let rotation: Double
    let duration: Double
    let delay: Double

    @State private var phase: CGFloat = 0

    var body: some View {
        GeometryReader { geometry in
            Rectangle()
                .fill(
                    LinearGradient(
                        colors: [
                            .clear,
                            Color.mysticViolet.opacity(0.2),
                            Color.mysticCyan.opacity(0.15),
                            Color.mysticPink.opacity(0.1),
                            Color.mysticTeal.opacity(0.15),
                            .clear
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: geometry.size.width * 2, height: 300)
                .blur(radius: 60)
                .blendMode(.screen)
                .opacity(0.5)
                .rotationEffect(.degrees(rotation))
                .offset(x: offsetX(for: geometry.size.width), y: yPosition)
                .scaleEffect(y: animatedScaleY)
                .opacity(animatedOpacity)
        }
        .onAppear {
            withAnimation(
                Animation
                    .easeInOut(duration: duration)
                    .repeatForever(autoreverses: true)
                    .delay(delay)
            ) {
                phase = 1
            }
        }
    }

    private func offsetX(for width: CGFloat) -> CGFloat {
        let startOffset = -width * 0.7
        let movement = width * 0.4
        return startOffset + (phase * movement)
    }

    private var animatedScaleY: CGFloat {
        return 1.0 + (phase * 0.2) - 0.1
    }

    private var animatedOpacity: Double {
        return 0.3 + (Double(phase) * 0.2)
    }
}

// MARK: - EnhancedAuroraBackground (Deprecated - use AuroraBackground(showRibbons: true))
/// @available(*, deprecated, message: "Use AuroraBackground(showRibbons: true) instead")
typealias EnhancedAuroraBackground = AuroraBackground

// MARK: - Preview
#Preview("Aurora Background") {
    ZStack {
        AuroraBackground()

        VStack {
            Text("Aurora Background")
                .font(TaroTypography.title)
                .foregroundColor(.textPrimary)

            Text("Mystic atmosphere")
                .font(TaroTypography.subheadline)
                .foregroundColor(.textSecondary)
        }
    }
    .preferredColorScheme(.dark)
}

#Preview("Aurora with Ribbons") {
    ZStack {
        AuroraBackground(showRibbons: true)

        Text("Aurora with Ribbons")
            .font(TaroTypography.largeTitle)
            .foregroundColor(.textPrimary)
    }
    .preferredColorScheme(.dark)
}
