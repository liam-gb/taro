import SwiftUI

// MARK: - Aurora Background
// Animated gradient background with slow-moving orbs
// Creates the mystical "Liquid Glass" atmosphere

struct AuroraBackground: View {
    @State private var animateOrbs = false

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Base gradient background
                LinearGradient(
                    colors: [.deepSpace, .deepSpaceLight, .deepSpace],
                    startPoint: .top,
                    endPoint: .bottom
                )

                // Aurora orbs
                AuroraOrb(
                    color: .mysticViolet,
                    size: geometry.size.width * 1.5,
                    position: CGPoint(x: -geometry.size.width * 0.2, y: -geometry.size.height * 0.15),
                    opacity: 0.4,
                    animationDuration: 15,
                    animateOrbs: animateOrbs
                )

                AuroraOrb(
                    color: .mysticCyan,
                    size: geometry.size.width * 1.25,
                    position: CGPoint(x: geometry.size.width * 1.1, y: geometry.size.height * 0.4),
                    opacity: 0.3,
                    animationDuration: 20,
                    animateOrbs: animateOrbs,
                    reverse: true
                )

                AuroraOrb(
                    color: .mysticPink,
                    size: geometry.size.width,
                    position: CGPoint(x: geometry.size.width * 0.3, y: geometry.size.height * 1.1),
                    opacity: 0.25,
                    animationDuration: 18,
                    animateOrbs: animateOrbs,
                    delay: 5
                )

                AuroraOrb(
                    color: .mysticTeal,
                    size: geometry.size.width * 0.9,
                    position: CGPoint(x: -geometry.size.width * 0.15, y: geometry.size.height * 0.6),
                    opacity: 0.2,
                    animationDuration: 22,
                    animateOrbs: animateOrbs,
                    delay: 3
                )
            }
        }
        .ignoresSafeArea()
        .onAppear {
            animateOrbs = true
        }
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
            .onChange(of: animateOrbs) { _, newValue in
                if newValue {
                    withAnimation(
                        Animation
                            .easeInOut(duration: animationDuration)
                            .repeatForever(autoreverses: true)
                            .delay(delay)
                    ) {
                        phase = 1
                    }
                }
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

// MARK: - Enhanced Aurora Background
// Combines orbs with optional ribbons for maximum mystical effect
struct EnhancedAuroraBackground: View {
    @State private var animateOrbs = false
    var showRibbons: Bool = false

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Base background
                Color.deepSpace

                // Subtle gradient overlay
                LinearGradient(
                    colors: [
                        .deepSpace,
                        .deepSpaceLight,
                        .deepSpace
                    ],
                    startPoint: .top,
                    endPoint: .bottom
                )

                // Aurora orbs
                auroraOrbs(in: geometry)

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
    }

    @ViewBuilder
    private func auroraOrbs(in geometry: GeometryProxy) -> some View {
        // Violet orb - top left
        AuroraOrb(
            color: .mysticViolet,
            size: geometry.size.width * 1.5,
            position: CGPoint(
                x: -geometry.size.width * 0.2,
                y: -geometry.size.height * 0.15
            ),
            opacity: 0.4,
            animationDuration: 15,
            animateOrbs: animateOrbs
        )

        // Cyan orb - right middle
        AuroraOrb(
            color: .mysticCyan,
            size: geometry.size.width * 1.25,
            position: CGPoint(
                x: geometry.size.width * 1.1,
                y: geometry.size.height * 0.4
            ),
            opacity: 0.3,
            animationDuration: 20,
            animateOrbs: animateOrbs,
            reverse: true
        )

        // Pink orb - bottom center
        AuroraOrb(
            color: .mysticPink,
            size: geometry.size.width,
            position: CGPoint(
                x: geometry.size.width * 0.3,
                y: geometry.size.height * 1.1
            ),
            opacity: 0.25,
            animationDuration: 18,
            animateOrbs: animateOrbs,
            delay: 5
        )

        // Teal orb - left middle
        AuroraOrb(
            color: .mysticTeal,
            size: geometry.size.width * 0.9,
            position: CGPoint(
                x: -geometry.size.width * 0.15,
                y: geometry.size.height * 0.6
            ),
            opacity: 0.2,
            animationDuration: 22,
            animateOrbs: animateOrbs,
            delay: 3
        )
    }

    @ViewBuilder
    private func auroraRibbons(in geometry: GeometryProxy) -> some View {
        AuroraRibbon(
            yPosition: geometry.size.height * 0.1,
            rotation: -5,
            duration: 20,
            delay: 0
        )

        AuroraRibbon(
            yPosition: geometry.size.height * 0.5,
            rotation: 3,
            duration: 25,
            delay: 5
        )

        AuroraRibbon(
            yPosition: geometry.size.height * 0.75,
            rotation: -2,
            duration: 22,
            delay: 10
        )
    }
}

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

#Preview("Enhanced Aurora") {
    ZStack {
        EnhancedAuroraBackground(showRibbons: true)

        Text("Enhanced Aurora")
            .font(TaroTypography.largeTitle)
            .foregroundColor(.textPrimary)
    }
    .preferredColorScheme(.dark)
}
