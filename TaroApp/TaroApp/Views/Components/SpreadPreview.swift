import SwiftUI

// MARK: - SpreadPreview
/// Mini preview of tarot spread layouts for selection cards
/// Shows a scaled-down representation of card positions for each spread type

struct SpreadPreview: View {
    let spreadType: SpreadType
    var size: CGSize = CGSize(width: 100, height: 80)
    var isAnimated: Bool = false

    @State private var cardAppearance: [Bool] = []
    @State private var glowPulse: Bool = false

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Subtle glow backdrop
                if isAnimated {
                    Circle()
                        .fill(
                            RadialGradient(
                                colors: [
                                    Color.mysticViolet.opacity(glowPulse ? 0.15 : 0.08),
                                    Color.clear
                                ],
                                center: .center,
                                startRadius: 0,
                                endRadius: geometry.size.width * 0.6
                            )
                        )
                        .scaleEffect(glowPulse ? 1.1 : 1.0)
                        .animation(
                            .easeInOut(duration: 2.5).repeatForever(autoreverses: true),
                            value: glowPulse
                        )
                }

                // Spread layout
                spreadLayout(in: geometry.size)
            }
        }
        .frame(width: size.width, height: size.height)
        .onAppear {
            initializeCardAppearance()
            if isAnimated {
                glowPulse = true
                animateCardsIn()
            }
        }
    }

    // MARK: - Spread Layouts

    @ViewBuilder
    private func spreadLayout(in containerSize: CGSize) -> some View {
        let center = CGPoint(x: containerSize.width / 2, y: containerSize.height / 2)

        switch spreadType {
        case .single:
            singleCardLayout(center: center, containerSize: containerSize)
        case .threeCard:
            threeCardLayout(center: center, containerSize: containerSize)
        case .situation:
            situationLayout(center: center, containerSize: containerSize)
        case .celtic:
            celticCrossLayout(center: center, containerSize: containerSize)
        case .horseshoe:
            horseshoeLayout(center: center, containerSize: containerSize)
        }
    }

    // MARK: - Single Card Layout

    @ViewBuilder
    private func singleCardLayout(center: CGPoint, containerSize: CGSize) -> some View {
        let cardSize = miniCardSize(for: containerSize, cardCount: 1)

        MiniLayoutCard(size: cardSize, isHighlighted: true)
            .position(center)
            .opacity(cardAppearance.indices.contains(0) && cardAppearance[0] ? 1 : 0)
            .animation(.spring(response: 0.5, dampingFraction: 0.7), value: cardAppearance)
    }

    // MARK: - Three Card Layout (Row)

    @ViewBuilder
    private func threeCardLayout(center: CGPoint, containerSize: CGSize) -> some View {
        let cardSize = miniCardSize(for: containerSize, cardCount: 3)
        let spacing = cardSize.width * 0.3
        let totalWidth = cardSize.width * 3 + spacing * 2
        let startX = center.x - totalWidth / 2 + cardSize.width / 2

        ForEach(0..<3) { index in
            MiniLayoutCard(size: cardSize, isHighlighted: index == 1)
                .position(
                    x: startX + CGFloat(index) * (cardSize.width + spacing),
                    y: center.y
                )
                .opacity(cardAppearance.indices.contains(index) && cardAppearance[index] ? 1 : 0)
                .animation(
                    .spring(response: 0.5, dampingFraction: 0.7).delay(Double(index) * 0.1),
                    value: cardAppearance
                )
        }
    }

    // MARK: - Situation Layout (Triangle/Pyramid)

    @ViewBuilder
    private func situationLayout(center: CGPoint, containerSize: CGSize) -> some View {
        let cardSize = miniCardSize(for: containerSize, cardCount: 3)
        let spacing = cardSize.width * 0.25

        // Top card (Action)
        MiniLayoutCard(size: cardSize, isHighlighted: true)
            .position(x: center.x, y: center.y - cardSize.height * 0.4)
            .opacity(cardAppearance.indices.contains(1) && cardAppearance[1] ? 1 : 0)
            .animation(.spring(response: 0.5, dampingFraction: 0.7).delay(0.1), value: cardAppearance)

        // Bottom left (Situation)
        MiniLayoutCard(size: cardSize)
            .position(
                x: center.x - cardSize.width * 0.6 - spacing,
                y: center.y + cardSize.height * 0.35
            )
            .opacity(cardAppearance.indices.contains(0) && cardAppearance[0] ? 1 : 0)
            .animation(.spring(response: 0.5, dampingFraction: 0.7), value: cardAppearance)

        // Bottom right (Outcome)
        MiniLayoutCard(size: cardSize)
            .position(
                x: center.x + cardSize.width * 0.6 + spacing,
                y: center.y + cardSize.height * 0.35
            )
            .opacity(cardAppearance.indices.contains(2) && cardAppearance[2] ? 1 : 0)
            .animation(.spring(response: 0.5, dampingFraction: 0.7).delay(0.2), value: cardAppearance)
    }

    // MARK: - Celtic Cross Layout

    @ViewBuilder
    private func celticCrossLayout(center: CGPoint, containerSize: CGSize) -> some View {
        let cardSize = miniCardSize(for: containerSize, cardCount: 10)
        let unit = cardSize.width * 0.8

        // Cross section (center)
        let crossCenter = CGPoint(x: center.x - unit * 0.8, y: center.y)

        // Position 1: Present (center)
        MiniLayoutCard(size: cardSize, isHighlighted: true)
            .position(crossCenter)
            .opacity(cardAppearance.indices.contains(0) && cardAppearance[0] ? 1 : 0)
            .zIndex(1)

        // Position 2: Challenge (crossing) - rotated 90°
        MiniLayoutCard(size: cardSize, rotation: 90, isCrossing: true)
            .position(crossCenter)
            .opacity(cardAppearance.indices.contains(1) && cardAppearance[1] ? 1 : 0)
            .zIndex(2)

        // Position 3: Past (left)
        MiniLayoutCard(size: cardSize)
            .position(x: crossCenter.x - unit * 1.5, y: crossCenter.y)
            .opacity(cardAppearance.indices.contains(2) && cardAppearance[2] ? 1 : 0)

        // Position 4: Future (right)
        MiniLayoutCard(size: cardSize)
            .position(x: crossCenter.x + unit * 1.5, y: crossCenter.y)
            .opacity(cardAppearance.indices.contains(3) && cardAppearance[3] ? 1 : 0)

        // Position 5: Above (crown)
        MiniLayoutCard(size: cardSize)
            .position(x: crossCenter.x, y: crossCenter.y - unit * 1.4)
            .opacity(cardAppearance.indices.contains(4) && cardAppearance[4] ? 1 : 0)

        // Position 6: Below (foundation)
        MiniLayoutCard(size: cardSize)
            .position(x: crossCenter.x, y: crossCenter.y + unit * 1.4)
            .opacity(cardAppearance.indices.contains(5) && cardAppearance[5] ? 1 : 0)

        // Staff section (right column) - 4 cards
        let staffX = center.x + unit * 2.5
        let staffSpacing = unit * 0.85
        let staffStartY = center.y + staffSpacing * 1.5

        ForEach(0..<4) { index in
            MiniLayoutCard(size: cardSize)
                .position(
                    x: staffX,
                    y: staffStartY - CGFloat(index) * staffSpacing
                )
                .opacity(cardAppearance.indices.contains(6 + index) && cardAppearance[6 + index] ? 1 : 0)
        }
    }

    // MARK: - Horseshoe Layout (Arc)

    @ViewBuilder
    private func horseshoeLayout(center: CGPoint, containerSize: CGSize) -> some View {
        let cardSize = miniCardSize(for: containerSize, cardCount: 7)

        // Arc parameters
        let arcRadius = containerSize.width * 0.38
        let arcCenter = CGPoint(x: center.x, y: center.y + arcRadius * 0.3)

        // 7 cards in an arc from left to right
        ForEach(0..<7) { index in
            let angle = Angle.degrees(180 + Double(index) * (180 / 6))
            let x = arcCenter.x + arcRadius * cos(angle.radians)
            let y = arcCenter.y - arcRadius * sin(angle.radians) * 0.6

            MiniLayoutCard(
                size: cardSize,
                isHighlighted: index == 3 // Center card highlighted
            )
            .position(x: x, y: y)
            .opacity(cardAppearance.indices.contains(index) && cardAppearance[index] ? 1 : 0)
            .animation(
                .spring(response: 0.5, dampingFraction: 0.7).delay(Double(index) * 0.08),
                value: cardAppearance
            )
        }
    }

    // MARK: - Helpers

    private func miniCardSize(for containerSize: CGSize, cardCount: Int) -> CGSize {
        let baseWidth: CGFloat

        switch cardCount {
        case 1:
            baseWidth = containerSize.width * 0.28
        case 3:
            baseWidth = containerSize.width * 0.2
        case 7:
            baseWidth = containerSize.width * 0.1
        case 10:
            baseWidth = containerSize.width * 0.09
        default:
            baseWidth = containerSize.width * 0.15
        }

        return CGSize(width: baseWidth, height: baseWidth * 1.6)
    }

    private func initializeCardAppearance() {
        cardAppearance = Array(repeating: !isAnimated, count: spreadType.cardCount)
    }

    private func animateCardsIn() {
        for index in 0..<spreadType.cardCount {
            DispatchQueue.main.asyncAfter(deadline: .now() + Double(index) * 0.1) {
                withAnimation {
                    if cardAppearance.indices.contains(index) {
                        cardAppearance[index] = true
                    }
                }
            }
        }
    }
}

// MARK: - MiniLayoutCard
/// Small card representation for spread previews

struct MiniLayoutCard: View {
    var size: CGSize = CGSize(width: 12, height: 20)
    var isHighlighted: Bool = false
    var rotation: Double = 0
    var isCrossing: Bool = false

    var body: some View {
        ZStack {
            // Card shape
            RoundedRectangle(cornerRadius: size.width * 0.15)
                .fill(
                    LinearGradient(
                        colors: isHighlighted
                            ? [Color.mysticViolet.opacity(0.5), Color.deepViolet.opacity(0.4)]
                            : [Color.mysticViolet.opacity(0.25), Color.deepViolet.opacity(0.2)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Glass overlay
            RoundedRectangle(cornerRadius: size.width * 0.15)
                .fill(Material.ultraThinMaterial)
                .opacity(0.15)

            // Inner detail (only for larger previews)
            if size.width > 10 {
                RoundedRectangle(cornerRadius: size.width * 0.1)
                    .stroke(
                        Color.lightViolet.opacity(isHighlighted ? 0.4 : 0.2),
                        lineWidth: 0.5
                    )
                    .padding(size.width * 0.15)
            }

            // Border
            RoundedRectangle(cornerRadius: size.width * 0.15)
                .stroke(
                    LinearGradient(
                        colors: isHighlighted
                            ? [Color.lightViolet.opacity(0.6), Color.mysticViolet.opacity(0.4)]
                            : [Color.lightViolet.opacity(0.3), Color.mysticViolet.opacity(0.2)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: isHighlighted ? 1 : 0.5
                )
        }
        .frame(width: isCrossing ? size.height : size.width, height: isCrossing ? size.width : size.height)
        .rotationEffect(.degrees(rotation))
        .shadow(
            color: isHighlighted ? Color.mysticViolet.opacity(0.3) : Color.black.opacity(0.2),
            radius: isHighlighted ? 4 : 2,
            y: 1
        )
    }
}

// MARK: - SpreadPreviewCard
/// A complete spread selection card with preview and info

struct SpreadPreviewCard: View {
    let spreadType: SpreadType
    let isSelected: Bool
    var onTap: () -> Void

    @State private var isPressed: Bool = false
    @State private var shimmerPhase: CGFloat = 0

    var body: some View {
        Button(action: onTap) {
            VStack(spacing: TaroSpacing.md) {
                // Spread preview
                SpreadPreview(
                    spreadType: spreadType,
                    size: CGSize(width: 140, height: 100),
                    isAnimated: isSelected
                )
                .padding(.top, TaroSpacing.sm)

                // Spread info
                VStack(spacing: TaroSpacing.xxs) {
                    Text(spreadType.displayName)
                        .font(TaroTypography.ethereal(15, weight: .medium))
                        .foregroundColor(.textPrimary)
                        .lineLimit(1)

                    Text(spreadType.description)
                        .font(TaroTypography.caption2)
                        .foregroundColor(.textSecondary)
                        .lineLimit(2)
                        .multilineTextAlignment(.center)

                    // Card count badge
                    HStack(spacing: TaroSpacing.xxs) {
                        ForEach(0..<min(spreadType.cardCount, 5), id: \.self) { _ in
                            RoundedRectangle(cornerRadius: 1)
                                .fill(Color.mysticViolet.opacity(0.5))
                                .frame(width: 4, height: 7)
                        }
                        if spreadType.cardCount > 5 {
                            Text("+\(spreadType.cardCount - 5)")
                                .font(TaroTypography.caption2)
                                .foregroundColor(.textMuted)
                        }
                    }
                    .padding(.top, TaroSpacing.xxs)
                }
                .padding(.horizontal, TaroSpacing.sm)
                .padding(.bottom, TaroSpacing.md)
            }
            .frame(width: 160)
            .background(cardBackground)
            .clipShape(RoundedRectangle(cornerRadius: TaroRadius.lg, style: .continuous))
            .overlay(cardBorder)
            .shadow(
                color: isSelected ? Color.mysticViolet.opacity(0.3) : Color.black.opacity(0.3),
                radius: isSelected ? 20 : 12,
                y: isSelected ? 8 : 6
            )
            .scaleEffect(isPressed ? 0.96 : (isSelected ? 1.02 : 1.0))
            .animation(TaroAnimation.springBouncy, value: isPressed)
            .animation(TaroAnimation.springSmooth, value: isSelected)
        }
        .buttonStyle(.plain)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }

    private var cardBackground: some View {
        ZStack {
            // Base gradient
            LinearGradient(
                colors: isSelected
                    ? [Color.mysticViolet.opacity(0.15), Color.deepViolet.opacity(0.08)]
                    : [Color.white.opacity(0.05), Color.white.opacity(0.02)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            // Glass material
            Material.ultraThinMaterial
                .opacity(isSelected ? 0.6 : 0.4)
        }
    }

    private var cardBorder: some View {
        RoundedRectangle(cornerRadius: TaroRadius.lg, style: .continuous)
            .stroke(
                isSelected
                    ? LinearGradient(
                        colors: [
                            Color.mysticViolet.opacity(0.6),
                            Color.lightViolet.opacity(0.4),
                            Color.mysticCyan.opacity(0.3)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                    : LinearGradient(
                        colors: [Color.white.opacity(0.1), Color.white.opacity(0.05)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                lineWidth: isSelected ? 1.5 : 1
            )
    }
}

// MARK: - Preview

#Preview("Spread Previews") {
    ZStack {
        AuroraBackground()

        ScrollView {
            VStack(spacing: TaroSpacing.xl) {
                ForEach(SpreadType.allCases) { spread in
                    VStack(spacing: TaroSpacing.sm) {
                        Text(spread.displayName)
                            .font(TaroTypography.caption)
                            .foregroundColor(.textSecondary)

                        SpreadPreview(
                            spreadType: spread,
                            size: CGSize(width: 160, height: 120),
                            isAnimated: true
                        )
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: TaroRadius.md)
                                .fill(Color.white.opacity(0.03))
                                .overlay(
                                    RoundedRectangle(cornerRadius: TaroRadius.md)
                                        .stroke(Color.white.opacity(0.08), lineWidth: 1)
                                )
                        )
                    }
                }
            }
            .padding()
        }
    }
    .preferredColorScheme(.dark)
}

#Preview("Spread Selection Cards") {
    struct SelectionPreview: View {
        @State private var selectedSpread: SpreadType? = .threeCard

        var body: some View {
            ZStack {
                AuroraBackground()

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: TaroSpacing.md) {
                        ForEach(SpreadType.allCases) { spread in
                            SpreadPreviewCard(
                                spreadType: spread,
                                isSelected: selectedSpread == spread
                            ) {
                                selectedSpread = spread
                            }
                        }
                    }
                    .padding(.horizontal, TaroSpacing.lg)
                    .padding(.vertical, TaroSpacing.xl)
                }
            }
        }
    }

    return SelectionPreview()
        .preferredColorScheme(.dark)
}
