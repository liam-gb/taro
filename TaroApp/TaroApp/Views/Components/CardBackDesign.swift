import SwiftUI

// MARK: - CardBackDesign
/// A mystical tarot card back design with geometric patterns and shimmer effects
/// Features a central mandala-like pattern with subtle animated sparkles

struct CardBackDesign: View {
    var size: Card3DView.CardSize = .standard
    var showShimmer: Bool = true

    @State private var shimmerPhase: CGFloat = 0
    @State private var sparkleOpacity: [Double] = [0.3, 0.5, 0.7, 0.4, 0.6, 0.8, 0.5, 0.3]

    var body: some View {
        ZStack {
            // Base card background
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.deepViolet.opacity(0.9),
                            Color(hex: "1A0A2E"),
                            Color.deepViolet.opacity(0.8)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Glass material overlay
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(Material.ultraThinMaterial)
                .opacity(0.2)

            // Mystical pattern container
            GeometryReader { geometry in
                ZStack {
                    // Outer decorative border
                    decorativeBorder(in: geometry.size)

                    // Central mandala pattern
                    centralMandala(in: geometry.size)

                    // Corner decorations
                    cornerDecorations(in: geometry.size)

                    // Sparkle effects
                    if showShimmer {
                        sparkleLayer(in: geometry.size)
                    }
                }
            }
            .padding(TaroSpacing.xxs)

            // Shimmer overlay
            if showShimmer {
                shimmerOverlay
            }

            // Card border
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .stroke(
                    LinearGradient(
                        colors: [
                            Color.mysticViolet.opacity(0.6),
                            Color.lightViolet.opacity(0.3),
                            Color.mysticViolet.opacity(0.6)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 1.5
                )
        }
        .frame(width: size.width, height: size.height)
        .shadow(color: Color.black.opacity(0.4), radius: 10, y: 5)
        .shadow(color: Color.mysticViolet.opacity(0.2), radius: 15)
        .onAppear {
            startAnimations()
        }
    }

    // MARK: - Decorative Border

    @ViewBuilder
    private func decorativeBorder(in containerSize: CGSize) -> some View {
        let inset: CGFloat = size == .large ? 8 : 5
        let lineWidth: CGFloat = size == .large ? 1 : 0.5

        RoundedRectangle(cornerRadius: TaroRadius.sm)
            .stroke(
                LinearGradient(
                    colors: [
                        Color.lightViolet.opacity(0.4),
                        Color.mysticIndigo.opacity(0.3),
                        Color.lightViolet.opacity(0.4)
                    ],
                    startPoint: .top,
                    endPoint: .bottom
                ),
                lineWidth: lineWidth
            )
            .padding(inset)
    }

    // MARK: - Central Mandala

    @ViewBuilder
    private func centralMandala(in containerSize: CGSize) -> some View {
        let centerX = containerSize.width / 2
        let centerY = containerSize.height / 2
        let maxRadius = min(containerSize.width, containerSize.height) * 0.35

        ZStack {
            // Outer ring
            Circle()
                .stroke(
                    LinearGradient(
                        colors: [
                            Color.lightViolet.opacity(0.4),
                            Color.mysticIndigo.opacity(0.3)
                        ],
                        startPoint: .top,
                        endPoint: .bottom
                    ),
                    lineWidth: size == .large ? 1.5 : 1
                )
                .frame(width: maxRadius * 2, height: maxRadius * 2)

            // Middle ring
            Circle()
                .stroke(
                    Color.mysticViolet.opacity(0.3),
                    lineWidth: size == .large ? 1 : 0.5
                )
                .frame(width: maxRadius * 1.4, height: maxRadius * 1.4)

            // Inner ring
            Circle()
                .stroke(
                    Color.lightViolet.opacity(0.5),
                    lineWidth: size == .large ? 1 : 0.5
                )
                .frame(width: maxRadius * 0.8, height: maxRadius * 0.8)

            // Radiating lines
            ForEach(0..<8) { index in
                Rectangle()
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.lightViolet.opacity(0.4),
                                Color.clear
                            ],
                            startPoint: .center,
                            endPoint: .top
                        )
                    )
                    .frame(width: size == .large ? 1.5 : 1, height: maxRadius)
                    .offset(y: -maxRadius / 2)
                    .rotationEffect(.degrees(Double(index) * 45))
            }

            // Center symbol
            centralSymbol(radius: maxRadius * 0.3)

            // Decorative dots on outer ring
            ForEach(0..<12) { index in
                Circle()
                    .fill(Color.lightViolet.opacity(0.6))
                    .frame(width: size == .large ? 4 : 2.5, height: size == .large ? 4 : 2.5)
                    .offset(y: -maxRadius)
                    .rotationEffect(.degrees(Double(index) * 30))
            }
        }
        .position(x: centerX, y: centerY)
    }

    @ViewBuilder
    private func centralSymbol(radius: CGFloat) -> some View {
        ZStack {
            // Star shape using overlapping triangles
            ForEach(0..<2) { index in
                Triangle()
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.mysticViolet.opacity(0.6),
                                Color.deepViolet.opacity(0.4)
                            ],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .frame(width: radius * 1.5, height: radius * 1.5)
                    .rotationEffect(.degrees(index == 0 ? 0 : 180))
            }

            // Central glow dot
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color.lightViolet.opacity(0.8),
                            Color.mysticViolet.opacity(0.3),
                            Color.clear
                        ],
                        center: .center,
                        startRadius: 0,
                        endRadius: radius * 0.5
                    )
                )
                .frame(width: radius, height: radius)
        }
    }

    // MARK: - Corner Decorations

    @ViewBuilder
    private func cornerDecorations(in containerSize: CGSize) -> some View {
        let cornerSize: CGFloat = size == .large ? 16 : 10
        let offset: CGFloat = size == .large ? 14 : 9

        // Corner flourishes
        ForEach(0..<4) { index in
            CornerFlourish()
                .stroke(Color.lightViolet.opacity(0.4), lineWidth: size == .large ? 1 : 0.5)
                .frame(width: cornerSize, height: cornerSize)
                .rotationEffect(.degrees(Double(index) * 90))
                .position(
                    x: index % 2 == 0 ? offset : containerSize.width - offset,
                    y: index < 2 ? offset : containerSize.height - offset
                )
        }
    }

    // MARK: - Sparkle Layer

    @ViewBuilder
    private func sparkleLayer(in containerSize: CGSize) -> some View {
        let sparklePositions: [(CGFloat, CGFloat)] = [
            (0.2, 0.15), (0.8, 0.2), (0.15, 0.8), (0.85, 0.85),
            (0.5, 0.1), (0.5, 0.9), (0.1, 0.5), (0.9, 0.5)
        ]

        ForEach(Array(sparklePositions.enumerated()), id: \.offset) { index, position in
            Image(systemName: "sparkle")
                .font(.system(size: size == .large ? 8 : 5))
                .foregroundColor(.lightViolet)
                .opacity(sparkleOpacity[index])
                .position(
                    x: containerSize.width * position.0,
                    y: containerSize.height * position.1
                )
        }
    }

    // MARK: - Shimmer Overlay

    private var shimmerOverlay: some View {
        GeometryReader { geometry in
            LinearGradient(
                colors: [
                    Color.clear,
                    Color.white.opacity(0.1),
                    Color.clear
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .mask(
                Rectangle()
                    .fill(
                        LinearGradient(
                            colors: [Color.clear, Color.white, Color.clear],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .rotationEffect(.degrees(30))
                    .offset(x: shimmerPhase * geometry.size.width * 2 - geometry.size.width)
            )
        }
        .clipShape(RoundedRectangle(cornerRadius: TaroRadius.md))
        .allowsHitTesting(false)
    }

    // MARK: - Animations

    private func startAnimations() {
        // Shimmer animation
        withAnimation(.linear(duration: 3).repeatForever(autoreverses: false)) {
            shimmerPhase = 1
        }

        // Sparkle animations with staggered timing
        for index in sparkleOpacity.indices {
            let delay = Double(index) * 0.3
            withAnimation(.easeInOut(duration: 2).repeatForever(autoreverses: true).delay(delay)) {
                sparkleOpacity[index] = sparkleOpacity[index] > 0.5 ? 0.2 : 0.8
            }
        }
    }
}

// MARK: - Supporting Shapes

/// Simple triangle shape for star pattern
struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        path.closeSubpath()
        return path
    }
}

/// Corner flourish shape for decorative corners
struct CornerFlourish: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()

        // L-shaped flourish with curves
        path.move(to: CGPoint(x: rect.minX, y: rect.maxY * 0.3))
        path.addQuadCurve(
            to: CGPoint(x: rect.maxX * 0.3, y: rect.minY),
            control: CGPoint(x: rect.minX, y: rect.minY)
        )

        return path
    }
}

// MARK: - Static Card Back (No Animation)
/// A simpler card back without animations for performance

struct CardBackStatic: View {
    var size: Card3DView.CardSize = .standard

    var body: some View {
        ZStack {
            // Base gradient
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.mysticViolet.opacity(0.3),
                            Color.deepViolet.opacity(0.25)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Glass effect
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(Material.ultraThinMaterial)
                .opacity(0.3)

            // Simple center symbol
            Image(systemName: "sparkle")
                .font(.system(size: size == .large ? 32 : 20, weight: .light))
                .foregroundColor(.mysticViolet.opacity(0.4))

            // Border
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .stroke(Color.mysticViolet.opacity(0.4), lineWidth: 1)
        }
        .frame(width: size.width, height: size.height)
        .shadow(color: Color.black.opacity(0.3), radius: 8, y: 4)
    }
}

// MARK: - Mini Card Back
/// Ultra-compact card back for deck indicators

struct MiniCardBack: View {
    var width: CGFloat = 30
    var rotation: Double = 0

    var body: some View {
        RoundedRectangle(cornerRadius: 4)
            .fill(
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.4),
                        Color.deepViolet.opacity(0.3)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 4)
                    .stroke(Color.mysticViolet.opacity(0.3), lineWidth: 0.5)
            )
            .frame(width: width, height: width * 1.8)
            .rotationEffect(.degrees(rotation))
            .shadow(color: Color.black.opacity(0.2), radius: 4, y: 2)
    }
}

// MARK: - Previews

#Preview("Card Back Design") {
    ZStack {
        AuroraBackground()

        VStack(spacing: TaroSpacing.xl) {
            CardBackDesign(size: .large)

            HStack(spacing: TaroSpacing.md) {
                CardBackDesign(size: .standard)
                CardBackDesign(size: .small)
            }
        }
    }
    .preferredColorScheme(.dark)
}

#Preview("Card Back Static") {
    ZStack {
        AuroraBackground()

        HStack(spacing: TaroSpacing.md) {
            CardBackStatic(size: .small)
            CardBackStatic(size: .standard)
            CardBackStatic(size: .large)
        }
    }
    .preferredColorScheme(.dark)
}

#Preview("Mini Card Stack") {
    ZStack {
        AuroraBackground()

        ZStack {
            ForEach(0..<5) { index in
                MiniCardBack(
                    width: 40,
                    rotation: Double(index - 2) * 5
                )
                .offset(x: CGFloat(index - 2) * 3, y: CGFloat(index) * -2)
            }
        }
    }
    .preferredColorScheme(.dark)
}
