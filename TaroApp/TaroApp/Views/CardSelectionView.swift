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
            // Background
            LinearGradient(
                colors: [
                    Color(red: 0.05, green: 0.05, blue: 0.15),
                    Color(red: 0.1, green: 0.05, blue: 0.2)
                ],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()

            VStack(spacing: 24) {
                // Position indicator
                if let position = currentPosition {
                    VStack(spacing: 4) {
                        Text("Select card for")
                            .font(.system(size: 12, weight: .medium))
                            .foregroundColor(.white.opacity(0.5))
                            .textCase(.uppercase)
                            .tracking(1)

                        Text(position.name)
                            .font(.system(size: 24, weight: .light, design: .serif))
                            .foregroundColor(.white)

                        Text(position.description)
                            .font(.system(size: 14, weight: .light))
                            .foregroundColor(.white.opacity(0.5))
                    }
                    .padding(.top, 32)
                }

                // Cards remaining
                Text("\(cardsNeeded) card\(cardsNeeded == 1 ? "" : "s") remaining")
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(.white.opacity(0.4))

                // Card fan (simplified for now)
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: -40) {
                        ForEach(Array(deck.enumerated()), id: \.element.id) { index, card in
                            CardBackView(isSelected: selectedIndices.contains(index))
                                .onTapGesture {
                                    selectCard(at: index)
                                }
                        }
                    }
                    .padding(.horizontal, 60)
                    .padding(.vertical, 40)
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
        RoundedRectangle(cornerRadius: 8)
            .fill(
                LinearGradient(
                    colors: [
                        Color(red: 0.2, green: 0.15, blue: 0.3),
                        Color(red: 0.15, green: 0.1, blue: 0.25)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(.white.opacity(isSelected ? 0.5 : 0.2), lineWidth: 1)
            )
            .overlay(
                // Decorative pattern placeholder
                Image(systemName: "sparkle")
                    .font(.system(size: 24))
                    .foregroundColor(.white.opacity(0.1))
            )
            .frame(width: 80, height: 120)
            .opacity(isSelected ? 0.3 : 1)
            .scaleEffect(isSelected ? 0.95 : 1)
            .animation(.easeInOut(duration: 0.2), value: isSelected)
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
}
