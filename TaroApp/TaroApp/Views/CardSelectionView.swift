import SwiftUI

struct CardSelectionView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var deck: [Card] = CardDeck.shuffled()
    @State private var selectedIndices: Set<Int> = []

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
                    .padding(.top, TaroSpacing.xl)
                }

                // Cards remaining
                Text("\(cardsNeeded) card\(cardsNeeded == 1 ? "" : "s") remaining")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)

                // Card fan
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: -40) {
                        ForEach(Array(deck.enumerated()), id: \.element.id) { index, card in
                            CardBackView(isSelected: selectedIndices.contains(index))
                                .onTapGesture {
                                    selectCard(at: index)
                                }
                        }
                    }
                    .padding(.horizontal, TaroSpacing.xxxl)
                    .padding(.vertical, TaroSpacing.xl)
                }

                Spacer()
            }
        }
        .navigationBarHidden(true)
    }

    private func selectCard(at index: Int) {
        guard let position = currentPosition else { return }
        guard !selectedIndices.contains(index) else { return }

        selectedIndices.insert(index)
        let card = deck[index]
        let isReversed = Bool.random()

        readingSession.drawCard(card, at: position, reversed: isReversed)
    }
}

struct CardBackView: View {
    var isSelected: Bool = false

    var body: some View {
        ActiveGlassPanel(
            isActive: false,
            cornerRadius: TaroRadius.sm,
            padding: 0
        ) {
            ZStack {
                // Card gradient fill
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.2),
                        Color.deepViolet.opacity(0.15)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )

                // Decorative pattern placeholder
                Image(systemName: "sparkle")
                    .font(.system(size: 24))
                    .foregroundColor(.mysticViolet.opacity(0.3))
            }
            .frame(width: 80, height: 120)
        }
        .opacity(isSelected ? 0.3 : 1)
        .scaleEffect(isSelected ? 0.95 : 1)
        .overlay(
            // Selection glow effect
            RoundedRectangle(cornerRadius: TaroRadius.sm)
                .stroke(Color.mysticViolet, lineWidth: 2)
                .shadow(color: Color.mysticViolet.opacity(0.5), radius: 10)
                .opacity(isSelected ? 0 : 0)
        )
        .animation(TaroAnimation.springSmooth, value: isSelected)
    }
}

#Preview {
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
