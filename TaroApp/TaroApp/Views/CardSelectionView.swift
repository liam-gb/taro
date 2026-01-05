import SwiftUI

struct CardSelectionView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var deck: [Card] = CardDeck.shuffled()
    @State private var selectedIndices: Set<Int> = []
    @State private var cardStates: [FanCardState] = []
    @State private var isFanExpanded = false
    @State private var selectedCardAnimating: Int? = nil
    @State private var flyAwayCards: Set<Int> = []

    // Fan configuration
    private let visibleCardCount = 15
    private let fanArcAngle: Double = 60  // Total arc span in degrees
    private let fanRadius: CGFloat = 400  // Radius of the arc

    var currentPosition: Position? {
        guard let spread = readingSession.currentSpread else { return nil }
        let nextIndex = readingSession.drawnCards.count
        guard nextIndex < spread.positions.count else { return nil }
        return spread.positions[nextIndex]
    }

    var cardsNeeded: Int {
        (readingSession.currentSpread?.positions.count ?? 0) - readingSession.drawnCards.count
    }

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: TaroSpacing.lg) {
                // Position indicator
                if let position = currentPosition {
                    positionIndicator(for: position)
                        .padding(.top, TaroSpacing.xl)
                }

                // Cards remaining
                Text("\(cardsNeeded) card\(cardsNeeded == 1 ? "" : "s") remaining")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)

                Spacer()

                // Card fan
                cardFanView
                    .frame(height: 300)

                Spacer()

                // Instructions
                if !isFanExpanded {
                    Text("Tap to spread the cards")
                        .font(TaroTypography.mystical(14, weight: .light))
                        .foregroundColor(.textMuted)
                        .transition(.opacity)
                }
            }
            .animation(TaroAnimation.springSmooth, value: isFanExpanded)
        }
        .navigationBarHidden(true)
        .onAppear {
            initializeCardStates()
            // Auto-expand fan after a short delay
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                expandFan()
            }
        }
    }

    // MARK: - Position Indicator

    @ViewBuilder
    private func positionIndicator(for position: Position) -> some View {
        GlassPanel(style: .standard, cornerRadius: TaroRadius.lg, padding: TaroSpacing.md) {
            VStack(spacing: TaroSpacing.xxs) {
                Text("Select card for")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
                    .textCase(.uppercase)
                    .tracking(1)

                Text(position.name)
                    .font(TaroTypography.mystical(24, weight: .light))
                    .foregroundColor(.textPrimary)

                Text(position.description)
                    .font(TaroTypography.ethereal(14, weight: .light))
                    .foregroundColor(.textSecondary)
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    // MARK: - Card Fan View

    private var cardFanView: some View {
        GeometryReader { geometry in
            let centerX = geometry.size.width / 2
            let centerY = geometry.size.height + fanRadius - 120

            ZStack {
                // Central glow
                Circle()
                    .fill(TaroGradients.violetGlow)
                    .frame(width: 250, height: 250)
                    .position(x: centerX, y: geometry.size.height - 50)
                    .blur(radius: 30)
                    .opacity(0.4)

                // Fan of cards
                ForEach(Array(cardStates.enumerated()), id: \.offset) { index, state in
                    if !flyAwayCards.contains(index) {
                        FanCard(
                            index: index,
                            state: state,
                            isSelected: selectedIndices.contains(index),
                            isAnimating: selectedCardAnimating == index,
                            onSelect: {
                                selectCard(at: index)
                            }
                        )
                        .position(
                            x: centerX + state.offset.x,
                            y: centerY + state.offset.y
                        )
                        .zIndex(state.zIndex)
                    }
                }

                // Flying away cards (selected cards animating out)
                ForEach(Array(flyAwayCards), id: \.self) { index in
                    if index < cardStates.count {
                        CardBackDesign(size: .standard, showShimmer: false)
                            .rotationEffect(.degrees(cardStates[index].rotation))
                            .offset(y: -400)
                            .opacity(0)
                            .animation(.easeIn(duration: 0.5), value: flyAwayCards)
                    }
                }
            }
            .onTapGesture {
                if !isFanExpanded {
                    expandFan()
                }
            }
        }
    }

    // MARK: - Card State Management

    private func initializeCardStates() {
        // Start with stacked cards
        cardStates = (0..<visibleCardCount).map { index in
            FanCardState(
                offset: CGPoint(x: 0, y: 0),
                rotation: 0,
                scale: 1.0,
                zIndex: Double(index)
            )
        }
    }

    private func expandFan() {
        guard !isFanExpanded else { return }

        isFanExpanded = true
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()

        withAnimation(.spring(response: 0.6, dampingFraction: 0.7)) {
            for index in cardStates.indices {
                let normalizedIndex = Double(index) / Double(visibleCardCount - 1)
                let angle = (normalizedIndex - 0.5) * fanArcAngle

                // Calculate position on arc
                let radians = angle * .pi / 180
                let x = sin(radians) * fanRadius
                let y = -cos(radians) * fanRadius + fanRadius

                cardStates[index].offset = CGPoint(x: x, y: y)
                cardStates[index].rotation = angle
                cardStates[index].zIndex = Double(index)
            }
        }
    }

    private func collapseFan() {
        isFanExpanded = false

        withAnimation(TaroAnimation.springSmooth) {
            for index in cardStates.indices {
                cardStates[index].offset = CGPoint(x: 0, y: 0)
                cardStates[index].rotation = 0
            }
        }
    }

    // MARK: - Card Selection

    private func selectCard(at index: Int) {
        guard let position = currentPosition else { return }
        guard !selectedIndices.contains(index) else { return }
        guard selectedCardAnimating == nil else { return }

        // Haptic feedback
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()

        // Mark as animating
        selectedCardAnimating = index

        // Animate card lifting
        withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
            cardStates[index].scale = 1.2
            cardStates[index].zIndex = 100
        }

        // After lift, fly away
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            withAnimation(.easeIn(duration: 0.4)) {
                flyAwayCards.insert(index)
            }

            selectedIndices.insert(index)

            // Get the card and add to reading
            let card = deck[index % deck.count]
            let isReversed = Bool.random()
            readingSession.drawCard(card, at: position, reversed: isReversed)

            // Reset animation state
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
                selectedCardAnimating = nil

                // Success haptic
                let notificationGenerator = UINotificationFeedbackGenerator()
                notificationGenerator.notificationOccurred(.success)
            }
        }
    }
}

// MARK: - Fan Card State

struct FanCardState {
    var offset: CGPoint
    var rotation: Double
    var scale: CGFloat
    var zIndex: Double
}

// MARK: - Fan Card View

struct FanCard: View {
    let index: Int
    let state: FanCardState
    var isSelected: Bool
    var isAnimating: Bool
    var onSelect: () -> Void

    @State private var isPressed = false
    @State private var glowPulse = false

    var body: some View {
        ZStack {
            // Selection glow
            if isAnimating {
                RoundedRectangle(cornerRadius: TaroRadius.md + 4)
                    .fill(TaroGradients.violetGlow)
                    .frame(width: 88, height: 132)
                    .blur(radius: 15)
                    .opacity(0.8)
            }

            // Card
            CardBackDesign(size: .standard, showShimmer: !isSelected)
                .scaleEffect(isPressed ? 1.1 : state.scale)
                .rotationEffect(.degrees(state.rotation))
                .shadow(
                    color: isAnimating ? Color.mysticViolet.opacity(0.6) : Color.black.opacity(0.3),
                    radius: isAnimating ? 20 : 8,
                    y: isAnimating ? 0 : 4
                )
        }
        .opacity(isSelected && !isAnimating ? 0 : 1)
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .animation(TaroAnimation.springSmooth, value: state.scale)
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in
                    if !isSelected {
                        isPressed = true
                    }
                }
                .onEnded { _ in
                    isPressed = false
                    if !isSelected {
                        onSelect()
                    }
                }
        )
    }
}

// MARK: - Drawn Cards Display

struct DrawnCardsStrip: View {
    let drawnCards: [DrawnCard]

    var body: some View {
        HStack(spacing: TaroSpacing.sm) {
            ForEach(drawnCards) { drawnCard in
                DrawnCardMini(drawnCard: drawnCard)
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }
}

struct DrawnCardMini: View {
    let drawnCard: DrawnCard

    var body: some View {
        VStack(spacing: TaroSpacing.xxs) {
            ZStack {
                RoundedRectangle(cornerRadius: TaroRadius.xs)
                    .fill(
                        LinearGradient(
                            colors: [
                                elementColor.opacity(0.3),
                                elementColor.opacity(0.15)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 40, height: 60)

                Text(drawnCard.card.numeral ?? drawnCard.card.rank?.prefix(1).uppercased() ?? "?")
                    .font(TaroTypography.mystical(14, weight: .light))
                    .foregroundColor(.textPrimary)
                    .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))
            }
            .overlay(
                RoundedRectangle(cornerRadius: TaroRadius.xs)
                    .stroke(elementColor.opacity(0.5), lineWidth: 1)
            )

            Text(drawnCard.position.name)
                .font(TaroTypography.caption2)
                .foregroundColor(.textMuted)
                .lineLimit(1)
        }
    }

    private var elementColor: Color {
        switch drawnCard.card.element {
        case .fire: return Color(hex: "F97316")
        case .water: return Color.mysticCyan
        case .air: return Color.mysticTeal
        case .earth: return Color.mysticEmerald
        }
    }
}

// MARK: - Preview

#Preview("Card Selection") {
    CardSelectionView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.threeCard)
            session.startReading()
            session.beginCardSelection()
            return session
        }())
        .preferredColorScheme(.dark)
}

#Preview("Drawn Cards Strip") {
    ZStack {
        AuroraBackground()

        DrawnCardsStrip(drawnCards: [
            DrawnCard(
                card: Card(id: 0, name: "The Fool", arcana: .major, element: .air, keywords: [], numeral: "0"),
                position: Position(id: "past", name: "Past", description: ""),
                isReversed: false
            ),
            DrawnCard(
                card: Card(id: 1, name: "The Magician", arcana: .major, element: .fire, keywords: [], numeral: "I"),
                position: Position(id: "present", name: "Present", description: ""),
                isReversed: true
            )
        ])
    }
    .preferredColorScheme(.dark)
}
