import SwiftUI

struct ReadingView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var showShareSheet = false

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

            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    VStack(spacing: 8) {
                        Text(readingSession.selectedSpread?.displayName ?? "Your Reading")
                            .font(.system(size: 24, weight: .light, design: .serif))
                            .foregroundColor(.white)

                        if !readingSession.question.isEmpty {
                            Text("\"\(readingSession.question)\"")
                                .font(.system(size: 14, weight: .light, design: .serif))
                                .foregroundColor(.white.opacity(0.5))
                                .italic()
                        }

                        Text(Date(), style: .date)
                            .font(.system(size: 12, weight: .light))
                            .foregroundColor(.white.opacity(0.3))
                    }
                    .padding(.top, 32)

                    // Cards display
                    VStack(spacing: 16) {
                        Text("Your Cards")
                            .font(.system(size: 12, weight: .medium))
                            .foregroundColor(.white.opacity(0.5))
                            .textCase(.uppercase)
                            .tracking(1)

                        LazyVGrid(columns: [
                            GridItem(.adaptive(minimum: 100, maximum: 120))
                        ], spacing: 16) {
                            ForEach(readingSession.drawnCards) { drawnCard in
                                DrawnCardTile(drawnCard: drawnCard)
                            }
                        }
                    }
                    .padding(.horizontal, 24)

                    // Interpretation
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Interpretation")
                            .font(.system(size: 12, weight: .medium))
                            .foregroundColor(.white.opacity(0.5))
                            .textCase(.uppercase)
                            .tracking(1)

                        Text(readingSession.interpretation)
                            .font(.system(size: 16, weight: .regular))
                            .foregroundColor(.white.opacity(0.9))
                            .lineSpacing(6)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(20)
                    .background(
                        RoundedRectangle(cornerRadius: 16)
                            .fill(.white.opacity(0.05))
                            .overlay(
                                RoundedRectangle(cornerRadius: 16)
                                    .stroke(.white.opacity(0.1), lineWidth: 1)
                            )
                    )
                    .padding(.horizontal, 24)

                    // Action buttons
                    VStack(spacing: 12) {
                        Button(action: {
                            // TODO: Save reading
                        }) {
                            HStack {
                                Image(systemName: "square.and.arrow.down")
                                Text("Save Reading")
                            }
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                            .background(
                                RoundedRectangle(cornerRadius: 10)
                                    .fill(.white.opacity(0.1))
                            )
                        }

                        Button(action: {
                            UIPasteboard.general.string = readingSession.interpretation
                        }) {
                            HStack {
                                Image(systemName: "doc.on.doc")
                                Text("Copy Text")
                            }
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(.white.opacity(0.6))
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                        }

                        Button(action: {
                            readingSession.reset()
                        }) {
                            Text("New Reading")
                                .font(.system(size: 16, weight: .semibold))
                                .foregroundColor(.black)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 16)
                                .background(
                                    RoundedRectangle(cornerRadius: 12)
                                        .fill(.white)
                                )
                        }
                    }
                    .padding(.horizontal, 24)
                    .padding(.bottom, 32)
                }
            }
        }
        .navigationBarHidden(true)
    }
}

struct DrawnCardTile: View {
    let drawnCard: DrawnCard

    var body: some View {
        VStack(spacing: 8) {
            // Card visual
            ZStack {
                RoundedRectangle(cornerRadius: 8)
                    .fill(
                        LinearGradient(
                            colors: [
                                elementColor.opacity(0.3),
                                elementColor.opacity(0.1)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(elementColor.opacity(0.5), lineWidth: 1)
                    )

                VStack(spacing: 4) {
                    if let numeral = drawnCard.card.numeral {
                        Text(numeral)
                            .font(.system(size: 12, weight: .light))
                            .foregroundColor(.white.opacity(0.5))
                    }

                    Text(cardInitials)
                        .font(.system(size: 18, weight: .medium, design: .serif))
                        .foregroundColor(.white)

                    if drawnCard.isReversed {
                        Text("R")
                            .font(.system(size: 10, weight: .bold))
                            .foregroundColor(.red.opacity(0.7))
                    }
                }
            }
            .frame(width: 70, height: 100)
            .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))

            // Card info
            VStack(spacing: 2) {
                Text(drawnCard.card.name)
                    .font(.system(size: 11, weight: .medium))
                    .foregroundColor(.white)
                    .lineLimit(2)
                    .multilineTextAlignment(.center)

                Text(drawnCard.position.name)
                    .font(.system(size: 10, weight: .light))
                    .foregroundColor(.white.opacity(0.5))

                Text(drawnCard.orientationText)
                    .font(.system(size: 9, weight: .medium))
                    .foregroundColor(drawnCard.isReversed ? .red.opacity(0.7) : .green.opacity(0.7))
            }
        }
    }

    private var elementColor: Color {
        switch drawnCard.card.element {
        case .fire: return .orange
        case .water: return .blue
        case .air: return .cyan
        case .earth: return .green
        }
    }

    private var cardInitials: String {
        let words = drawnCard.card.name.split(separator: " ")
        if words.count == 1 {
            return String(words[0].prefix(3))
        }
        return words.map { String($0.prefix(1)) }.joined()
    }
}

#Preview {
    ReadingView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.threeCard)
            session.question = "Should I change careers?"
            let deck = CardDeck.shuffled()
            let spread = SpreadType.threeCard.spread
            for (index, position) in spread.positions.enumerated() {
                session.drawCard(deck[index], at: position, reversed: Bool.random())
            }
            session.setInterpretation("""
            Your reading reveals a journey of transformation.

            **Past** - The Fool (upright)
            What has shaped this moment. The Fool in this position speaks to beginnings, innocence, spontaneity, leap of faith.

            **Present** - Death (reversed)
            Where you are now. Death in this position speaks to transformation, endings, change, transition.

            **Future** - The Star (upright)
            Where this path leads. The Star in this position speaks to hope, faith, renewal, inspiration.

            Together, these cards weave a story of beginnings leading to hope.

            *This is a placeholder reading. Full LLM integration coming in PR #6.*
            """)
            return session
        }())
}
