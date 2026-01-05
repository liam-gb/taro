import SwiftUI

// MARK: - SpreadLayoutView
/// Positions cards according to spread type with mystical animations
/// Handles all 5 spread types with proper z-ordering and overlapping for Celtic Cross

struct SpreadLayoutView: View {
    let spreadType: SpreadType
    let drawnCards: [DrawnCard]
    var cardSize: Card3DView.CardSize = .standard
    var showPositionLabels: Bool = true
    var animateIn: Bool = true
    var onCardTap: ((DrawnCard) -> Void)? = nil

    @State private var cardStates: [CardAnimationState] = []
    @State private var hasAnimated: Bool = false
    @State private var animationTask: Task<Void, Never>?

    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Mystical connection lines (optional visual enhancement)
                if spreadType == .celtic || spreadType == .horseshoe {
                    connectionLines(in: geometry.size)
                }

                // Cards in their positions
                ForEach(Array(drawnCards.enumerated()), id: \.element.id) { index, drawnCard in
                    cardAtPosition(
                        drawnCard: drawnCard,
                        index: index,
                        in: geometry.size
                    )
                }
            }
        }
        .onAppear {
            initializeCardStates()
            if animateIn && !hasAnimated {
                animateCardsSequentially()
            }
        }
        .onDisappear {
            animationTask?.cancel()
            animationTask = nil
        }
    }

    // MARK: - Card Positioning

    @ViewBuilder
    private func cardAtPosition(
        drawnCard: DrawnCard,
        index: Int,
        in containerSize: CGSize
    ) -> some View {
        let layout = calculateCardLayout(
            for: spreadType,
            index: index,
            in: containerSize
        )
        let state = cardStates.indices.contains(index) ? cardStates[index] : CardAnimationState()

        VStack(spacing: TaroSpacing.xxs) {
            // The card itself
            ZStack {
                // Glow effect for visible cards
                if state.isVisible {
                    RoundedRectangle(cornerRadius: TaroRadius.md + 4)
                        .fill(
                            RadialGradient(
                                colors: [
                                    elementColor(for: drawnCard.card.element).opacity(0.2),
                                    Color.clear
                                ],
                                center: .center,
                                startRadius: 0,
                                endRadius: cardSize.width * 0.8
                            )
                        )
                        .frame(
                            width: cardSize.width * 1.4,
                            height: cardSize.height * 1.4
                        )
                        .blur(radius: 10)
                        .opacity(state.glowOpacity)
                }

                // Card content
                SpreadCardView(
                    drawnCard: drawnCard,
                    size: cardSize,
                    isFlipped: state.isFlipped,
                    onTap: { onCardTap?(drawnCard) }
                )
                .rotationEffect(.degrees(layout.rotation))
            }

            // Position label
            if showPositionLabels && state.isVisible {
                Text(drawnCard.position.name)
                    .font(TaroTypography.caption2)
                    .foregroundColor(.textSecondary)
                    .padding(.horizontal, TaroSpacing.xs)
                    .padding(.vertical, TaroSpacing.xxxs)
                    .background(
                        Capsule()
                            .fill(Color.black.opacity(0.3))
                            .overlay(
                                Capsule()
                                    .stroke(Color.white.opacity(0.1), lineWidth: 0.5)
                            )
                    )
                    .opacity(state.labelOpacity)
                    .offset(y: layout.rotation != 0 ? cardSize.width * 0.3 : 0)
            }
        }
        .position(x: layout.position.x, y: layout.position.y)
        .zIndex(layout.zIndex)
        .offset(x: state.offset.width, y: state.offset.height)
        .scaleEffect(state.scale)
        .opacity(state.opacity)
    }

    // MARK: - Layout Calculations

    private func calculateCardLayout(
        for spread: SpreadType,
        index: Int,
        in containerSize: CGSize
    ) -> CardLayout {
        let center = CGPoint(x: containerSize.width / 2, y: containerSize.height / 2)

        switch spread {
        case .single:
            return singleLayout(index: index, center: center)
        case .threeCard:
            return threeCardRowLayout(index: index, center: center, containerSize: containerSize)
        case .situation:
            return situationTriangleLayout(index: index, center: center, containerSize: containerSize)
        case .celtic:
            return celticCrossLayout(index: index, center: center, containerSize: containerSize)
        case .horseshoe:
            return horseshoeArcLayout(index: index, center: center, containerSize: containerSize)
        }
    }

    // MARK: - Single Card Layout

    private func singleLayout(index: Int, center: CGPoint) -> CardLayout {
        CardLayout(position: center, rotation: 0, zIndex: 1)
    }

    // MARK: - Three Card Row Layout

    private func threeCardRowLayout(
        index: Int,
        center: CGPoint,
        containerSize: CGSize
    ) -> CardLayout {
        let spacing = cardSize.width * 0.3
        let totalWidth = cardSize.width * 3 + spacing * 2
        let startX = center.x - totalWidth / 2 + cardSize.width / 2

        return CardLayout(
            position: CGPoint(
                x: startX + CGFloat(index) * (cardSize.width + spacing),
                y: center.y
            ),
            rotation: 0,
            zIndex: Double(index + 1)
        )
    }

    // MARK: - Situation Triangle Layout

    private func situationTriangleLayout(
        index: Int,
        center: CGPoint,
        containerSize: CGSize
    ) -> CardLayout {
        let verticalSpacing = cardSize.height * 0.6
        let horizontalSpacing = cardSize.width * 0.7

        switch index {
        case 0: // Situation (left)
            return CardLayout(
                position: CGPoint(x: center.x - horizontalSpacing, y: center.y + verticalSpacing * 0.3),
                rotation: 0,
                zIndex: 1
            )
        case 1: // Action (top center)
            return CardLayout(
                position: CGPoint(x: center.x, y: center.y - verticalSpacing * 0.4),
                rotation: 0,
                zIndex: 2
            )
        case 2: // Outcome (right)
            return CardLayout(
                position: CGPoint(x: center.x + horizontalSpacing, y: center.y + verticalSpacing * 0.3),
                rotation: 0,
                zIndex: 1
            )
        default:
            return CardLayout(position: center, rotation: 0, zIndex: 0)
        }
    }

    // MARK: - Celtic Cross Layout (Complex with Overlapping)

    private func celticCrossLayout(
        index: Int,
        center: CGPoint,
        containerSize: CGSize
    ) -> CardLayout {
        let unit = cardSize.width * 1.1
        let crossCenter = CGPoint(x: center.x - unit * 0.5, y: center.y)

        switch index {
        case 0: // Present (center) - base card of the cross
            return CardLayout(
                position: crossCenter,
                rotation: 0,
                zIndex: 1
            )
        case 1: // Challenge (crossing) - rotated 90° on top of Present
            return CardLayout(
                position: crossCenter,
                rotation: 90,
                zIndex: 2
            )
        case 2: // Past (left of center)
            return CardLayout(
                position: CGPoint(x: crossCenter.x - unit * 1.4, y: crossCenter.y),
                rotation: 0,
                zIndex: 1
            )
        case 3: // Future (right of center)
            return CardLayout(
                position: CGPoint(x: crossCenter.x + unit * 1.4, y: crossCenter.y),
                rotation: 0,
                zIndex: 1
            )
        case 4: // Above (crown)
            return CardLayout(
                position: CGPoint(x: crossCenter.x, y: crossCenter.y - unit * 1.5),
                rotation: 0,
                zIndex: 1
            )
        case 5: // Below (foundation)
            return CardLayout(
                position: CGPoint(x: crossCenter.x, y: crossCenter.y + unit * 1.5),
                rotation: 0,
                zIndex: 1
            )
        case 6, 7, 8, 9: // Staff (right column, bottom to top)
            let staffX = center.x + unit * 2.2
            let staffIndex = index - 6
            let staffSpacing = unit * 0.9
            let staffStartY = center.y + staffSpacing * 1.5
            return CardLayout(
                position: CGPoint(
                    x: staffX,
                    y: staffStartY - CGFloat(staffIndex) * staffSpacing
                ),
                rotation: 0,
                zIndex: Double(staffIndex + 1)
            )
        default:
            return CardLayout(position: center, rotation: 0, zIndex: 0)
        }
    }

    // MARK: - Horseshoe Arc Layout

    private func horseshoeArcLayout(
        index: Int,
        center: CGPoint,
        containerSize: CGSize
    ) -> CardLayout {
        // Arc from left to right with 7 positions
        let arcRadius = min(containerSize.width * 0.38, containerSize.height * 0.35)
        let arcCenter = CGPoint(x: center.x, y: center.y + arcRadius * 0.2)

        // Map index to angle (180° to 360° for upward-opening arc)
        let angleStep = 180.0 / 6.0 // 6 gaps for 7 cards
        let angle = Angle.degrees(180 + Double(index) * angleStep)

        let x = arcCenter.x + arcRadius * cos(angle.radians)
        let y = arcCenter.y - arcRadius * sin(angle.radians) * 0.7 // Flatten the arc slightly

        return CardLayout(
            position: CGPoint(x: x, y: y),
            rotation: 0,
            zIndex: Double(7 - abs(index - 3)) // Center card highest z-index
        )
    }

    // MARK: - Connection Lines (Visual Enhancement)

    @ViewBuilder
    private func connectionLines(in containerSize: CGSize) -> some View {
        Canvas { context, size in
            // Draw subtle connecting lines between cards
            if spreadType == .horseshoe {
                drawHorseshoeArc(context: context, size: size)
            }
        }
        .opacity(0.15)
    }

    private func drawHorseshoeArc(context: GraphicsContext, size: CGSize) {
        let center = CGPoint(x: size.width / 2, y: size.height / 2)
        let arcRadius = min(size.width * 0.38, size.height * 0.35)
        let arcCenter = CGPoint(x: center.x, y: center.y + arcRadius * 0.2)

        var path = Path()
        path.addArc(
            center: arcCenter,
            radius: arcRadius,
            startAngle: .degrees(180),
            endAngle: .degrees(360),
            clockwise: false
        )

        context.stroke(
            path,
            with: .linearGradient(
                Gradient(colors: [
                    Color.mysticViolet.opacity(0.3),
                    Color.mysticCyan.opacity(0.2),
                    Color.mysticViolet.opacity(0.3)
                ]),
                startPoint: CGPoint(x: 0, y: center.y),
                endPoint: CGPoint(x: size.width, y: center.y)
            ),
            lineWidth: 1
        )
    }

    // MARK: - Animation

    private func initializeCardStates() {
        cardStates = (0..<drawnCards.count).map { _ in
            CardAnimationState(
                isVisible: !animateIn,
                isFlipped: !animateIn,
                opacity: animateIn ? 0 : 1,
                scale: animateIn ? 0.5 : 1,
                offset: animateIn ? CGSize(width: 0, height: 50) : .zero
            )
        }
    }

    private func animateCardsSequentially() {
        hasAnimated = true
        animationTask?.cancel()

        animationTask = Task { @MainActor in
            for index in 0..<drawnCards.count {
                guard !Task.isCancelled else { return }

                let delayNanos = UInt64(Double(index) * 0.15 * 1_000_000_000)
                try? await Task.sleep(nanoseconds: delayNanos)
                guard !Task.isCancelled else { return }

                // Card appears
                withAnimation(.spring(response: 0.5, dampingFraction: 0.7)) {
                    if cardStates.indices.contains(index) {
                        cardStates[index].isVisible = true
                        cardStates[index].opacity = 1
                        cardStates[index].scale = 1
                        cardStates[index].offset = .zero
                    }
                }

                // Glow pulses in after 0.2s
                try? await Task.sleep(nanoseconds: 200_000_000)
                guard !Task.isCancelled else { return }
                withAnimation(.easeIn(duration: 0.3)) {
                    if cardStates.indices.contains(index) {
                        cardStates[index].glowOpacity = 0.8
                    }
                }

                // Card flips after 0.2s more
                try? await Task.sleep(nanoseconds: 200_000_000)
                guard !Task.isCancelled else { return }
                withAnimation(.easeInOut(duration: 0.4)) {
                    if cardStates.indices.contains(index) {
                        cardStates[index].isFlipped = true
                    }
                }
                let generator = UIImpactFeedbackGenerator(style: .medium)
                generator.impactOccurred()

                // Glow settles after 0.3s
                try? await Task.sleep(nanoseconds: 300_000_000)
                guard !Task.isCancelled else { return }
                withAnimation(.easeOut(duration: 0.5)) {
                    if cardStates.indices.contains(index) {
                        cardStates[index].glowOpacity = 0.3
                    }
                }

                // Label fades in after 0.1s
                try? await Task.sleep(nanoseconds: 100_000_000)
                guard !Task.isCancelled else { return }
                withAnimation(.easeIn(duration: 0.3)) {
                    if cardStates.indices.contains(index) {
                        cardStates[index].labelOpacity = 1
                    }
                }
            }
        }
    }

    // MARK: - Helpers

    private func elementColor(for element: Element) -> Color {
        switch element {
        case .fire: return Color(hex: "F97316")
        case .water: return .mysticCyan
        case .air: return .mysticTeal
        case .earth: return .mysticEmerald
        }
    }
}

// MARK: - Supporting Types

private struct CardLayout {
    let position: CGPoint
    let rotation: Double
    let zIndex: Double
}

private struct CardAnimationState {
    var isVisible: Bool = false
    var isFlipped: Bool = false
    var opacity: Double = 0
    var scale: CGFloat = 0.5
    var offset: CGSize = CGSize(width: 0, height: 50)
    var glowOpacity: Double = 0
    var labelOpacity: Double = 0
}

// MARK: - SpreadCardView
/// Individual card in a spread with flip capability

struct SpreadCardView: View {
    let drawnCard: DrawnCard
    var size: Card3DView.CardSize = .standard
    var isFlipped: Bool = true
    var onTap: (() -> Void)? = nil

    @State private var internalFlipped: Bool = false
    @State private var flipProgress: Double = 0
    @State private var glowOpacity: Double = 0

    var body: some View {
        ZStack {
            // Glow during flip
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(TaroGradients.violetGlow)
                .frame(width: size.width * 1.3, height: size.height * 1.3)
                .blur(radius: 20)
                .opacity(glowOpacity)

            // Card
            ZStack {
                // Back
                CardBackDesign(size: size)
                    .opacity(flipProgress < 0.5 ? 1 : 0)

                // Front
                SpreadCardFront(drawnCard: drawnCard, size: size)
                    .rotation3DEffect(
                        .degrees(180),
                        axis: (x: 0, y: 1, z: 0)
                    )
                    .opacity(flipProgress >= 0.5 ? 1 : 0)
            }
            .frame(width: size.width, height: size.height)
            .rotation3DEffect(
                .degrees(flipProgress * 180),
                axis: (x: 0, y: 1, z: 0),
                anchor: .center,
                perspective: 0.5
            )
            // Apply reversed rotation AFTER the 3D flip, on the front face
            .rotationEffect(.degrees(drawnCard.isReversed && flipProgress >= 0.5 ? 180 : 0))
        }
        .onTapGesture {
            onTap?()
        }
        .onChange(of: isFlipped) { _, newValue in
            performFlip(to: newValue)
        }
        .onAppear {
            internalFlipped = isFlipped
            flipProgress = isFlipped ? 1 : 0
        }
    }

    private func performFlip(to flipped: Bool) {
        withAnimation(.easeIn(duration: 0.15)) {
            glowOpacity = 0.7
        }

        withAnimation(.easeInOut(duration: 0.4)) {
            flipProgress = flipped ? 1 : 0
        }

        withAnimation(.easeOut(duration: 0.3).delay(0.4)) {
            glowOpacity = 0
        }
    }
}

// MARK: - SpreadCardFront
/// Front face of a card in the spread layout

struct SpreadCardFront: View {
    let drawnCard: DrawnCard
    var size: Card3DView.CardSize = .standard

    var body: some View {
        ZStack {
            // Background
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.deepSpaceLight,
                            Color.deepSpace
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Glass overlay
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(Material.ultraThinMaterial)
                .opacity(0.3)

            // Element gradient accent
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(
                    LinearGradient(
                        colors: [
                            elementColor.opacity(0.15),
                            elementColor.opacity(0.05),
                            Color.clear
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Card content
            VStack(spacing: TaroSpacing.xxs) {
                // Element badge
                Circle()
                    .fill(elementColor.opacity(0.3))
                    .frame(width: size == .large ? 24 : 16, height: size == .large ? 24 : 16)
                    .overlay(
                        Circle()
                            .stroke(elementColor.opacity(0.5), lineWidth: 1)
                    )

                Spacer()

                // Numeral
                if let numeral = drawnCard.card.numeral {
                    Text(numeral)
                        .font(TaroTypography.mystical(size == .large ? 32 : 20, weight: .light))
                        .foregroundColor(.textPrimary)
                } else if let rank = drawnCard.card.rank {
                    Text(rank.prefix(1).uppercased())
                        .font(TaroTypography.mystical(size == .large ? 28 : 18, weight: .light))
                        .foregroundColor(.textPrimary)
                }

                // Card name
                Text(abbreviatedName)
                    .font(TaroTypography.mystical(size == .large ? 14 : 10, weight: .regular))
                    .foregroundColor(.textSecondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
                    .minimumScaleFactor(0.7)

                Spacer()

                // Arcana indicator + reversed
                HStack(spacing: 4) {
                    ForEach(0..<(drawnCard.card.arcana == .major ? 3 : 1), id: \.self) { _ in
                        Circle()
                            .fill(Color.mysticViolet.opacity(0.5))
                            .frame(width: 4, height: 4)
                    }

                    if drawnCard.isReversed {
                        Text("R")
                            .font(TaroTypography.caption2)
                            .fontWeight(.bold)
                            .foregroundColor(.mysticPink)
                    }
                }
            }
            .padding(TaroSpacing.xs)

            // Border
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .stroke(
                    LinearGradient(
                        colors: [
                            elementColor.opacity(0.5),
                            elementColor.opacity(0.2)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 1.5
                )
        }
        .frame(width: size.width, height: size.height)
        .shadow(color: Color.black.opacity(0.4), radius: 10, y: 5)
        .shadow(color: elementColor.opacity(0.2), radius: 12)
    }

    private var elementColor: Color {
        switch drawnCard.card.element {
        case .fire: return Color(hex: "F97316")
        case .water: return .mysticCyan
        case .air: return .mysticTeal
        case .earth: return .mysticEmerald
        }
    }

    private var abbreviatedName: String {
        if size == .small || size == .standard {
            let words = drawnCard.card.name.split(separator: " ")
            if words.count > 2 {
                return words.prefix(2).joined(separator: " ")
            }
        }
        return drawnCard.card.name
    }
}

// MARK: - Preview

#Preview("Spread Layout - Three Card") {
    struct PreviewWrapper: View {
        let cards: [DrawnCard]

        init() {
            let deck = CardDeck.shuffled()
            let spread = SpreadType.threeCard.spread
            cards = spread.positions.enumerated().map { index, position in
                DrawnCard(
                    card: deck[index],
                    position: position,
                    isReversed: Bool.random()
                )
            }
        }

        var body: some View {
            ZStack {
                AuroraBackground()

                SpreadLayoutView(
                    spreadType: .threeCard,
                    drawnCards: cards,
                    cardSize: .standard
                )
                .padding()
            }
        }
    }

    return PreviewWrapper()
        .preferredColorScheme(.dark)
}

#Preview("Spread Layout - Celtic Cross") {
    struct PreviewWrapper: View {
        let cards: [DrawnCard]

        init() {
            let deck = CardDeck.shuffled()
            let spread = SpreadType.celtic.spread
            cards = spread.positions.enumerated().map { index, position in
                DrawnCard(
                    card: deck[index],
                    position: position,
                    isReversed: Bool.random()
                )
            }
        }

        var body: some View {
            ZStack {
                AuroraBackground()

                SpreadLayoutView(
                    spreadType: .celtic,
                    drawnCards: cards,
                    cardSize: .small
                )
                .padding()
            }
        }
    }

    return PreviewWrapper()
        .preferredColorScheme(.dark)
}

#Preview("Spread Layout - Horseshoe") {
    struct PreviewWrapper: View {
        let cards: [DrawnCard]

        init() {
            let deck = CardDeck.shuffled()
            let spread = SpreadType.horseshoe.spread
            cards = spread.positions.enumerated().map { index, position in
                DrawnCard(
                    card: deck[index],
                    position: position,
                    isReversed: Bool.random()
                )
            }
        }

        var body: some View {
            ZStack {
                AuroraBackground()

                SpreadLayoutView(
                    spreadType: .horseshoe,
                    drawnCards: cards,
                    cardSize: .small
                )
                .padding()
            }
        }
    }

    return PreviewWrapper()
        .preferredColorScheme(.dark)
}
