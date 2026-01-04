import SwiftUI

struct GeneratingView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var animationPhase = 0.0

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

            VStack(spacing: 32) {
                Spacer()

                // Cards drawn summary
                VStack(spacing: 16) {
                    Text("Your Cards")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(.white.opacity(0.5))
                        .textCase(.uppercase)
                        .tracking(1)

                    HStack(spacing: 12) {
                        ForEach(readingSession.drawnCards) { drawnCard in
                            VStack(spacing: 4) {
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(.white.opacity(0.1))
                                    .frame(width: 50, height: 75)
                                    .overlay(
                                        Text(drawnCard.card.name.prefix(1))
                                            .font(.system(size: 16, weight: .light, design: .serif))
                                            .foregroundColor(.white.opacity(0.6))
                                    )
                                    .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))

                                Text(drawnCard.position.name)
                                    .font(.system(size: 10, weight: .medium))
                                    .foregroundColor(.white.opacity(0.4))
                                    .lineLimit(1)
                            }
                        }
                    }
                }

                Spacer()

                // Loading indicator
                VStack(spacing: 16) {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        .scaleEffect(1.5)

                    Text("Weaving your reading...")
                        .font(.system(size: 16, weight: .light, design: .serif))
                        .foregroundColor(.white.opacity(0.7))

                    Text("The cards speak through the local oracle")
                        .font(.system(size: 12, weight: .light))
                        .foregroundColor(.white.opacity(0.4))
                }

                Spacer()

                // Placeholder: Skip button for development
                Button(action: {
                    // Simulate interpretation generation
                    let mockInterpretation = generateMockInterpretation()
                    readingSession.setInterpretation(mockInterpretation)
                }) {
                    Text("Skip (Dev Only)")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(.white.opacity(0.3))
                }
                .padding(.bottom, 32)
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            // TODO: Trigger actual LLM generation
            // For now, auto-advance after delay
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                if readingSession.state == .generatingInterpretation {
                    let mockInterpretation = generateMockInterpretation()
                    readingSession.setInterpretation(mockInterpretation)
                }
            }
        }
    }

    private func generateMockInterpretation() -> String {
        let cards = readingSession.drawnCards
        var text = "Your reading reveals a journey of transformation.\n\n"

        for drawnCard in cards {
            let orientation = drawnCard.isReversed ? "reversed" : "upright"
            text += "**\(drawnCard.position.name)** - \(drawnCard.card.name) (\(orientation))\n"
            text += "\(drawnCard.position.description). "
            text += "The \(drawnCard.card.name) in this position speaks to \(drawnCard.card.keywords.joined(separator: ", ")).\n\n"
        }

        text += "Together, these cards weave a story of \(cards.first?.card.keywords.first ?? "possibility") leading to \(cards.last?.card.keywords.first ?? "transformation").\n\n"
        text += "*This is a placeholder reading. Full LLM integration coming in PR #6.*"

        return text
    }
}

#Preview {
    GeneratingView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.threeCard)
            session.startReading()
            session.beginCardSelection()
            // Add some mock cards
            let deck = CardDeck.shuffled()
            let spread = SpreadType.threeCard.spread
            for (index, position) in spread.positions.enumerated() {
                session.drawCard(deck[index], at: position, reversed: Bool.random())
            }
            return session
        }())
}
