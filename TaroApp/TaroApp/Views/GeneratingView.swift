import SwiftUI

struct GeneratingView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var animationPhase = 0.0
    @State private var breathingScale: CGFloat = 1.0
    @State private var pulseOpacity: Double = 0.3

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: TaroSpacing.xl) {
                Spacer()

                // Cards drawn summary
                GlassPanel(style: .card, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
                    VStack(spacing: TaroSpacing.md) {
                        Text("Your Cards")
                            .font(TaroTypography.caption)
                            .foregroundColor(.textMuted)
                            .textCase(.uppercase)
                            .tracking(1)

                        HStack(spacing: TaroSpacing.sm) {
                            ForEach(readingSession.drawnCards) { drawnCard in
                                VStack(spacing: TaroSpacing.xxs) {
                                    RoundedRectangle(cornerRadius: TaroRadius.xs)
                                        .fill(
                                            LinearGradient(
                                                colors: [
                                                    Color.mysticViolet.opacity(0.15),
                                                    Color.deepViolet.opacity(0.1)
                                                ],
                                                startPoint: .topLeading,
                                                endPoint: .bottomTrailing
                                            )
                                        )
                                        .overlay(
                                            RoundedRectangle(cornerRadius: TaroRadius.xs)
                                                .stroke(Color.mysticViolet.opacity(0.3), lineWidth: 1)
                                        )
                                        .frame(width: 50, height: 75)
                                        .overlay(
                                            Text(drawnCard.card.name.prefix(1))
                                                .font(TaroTypography.mystical(16, weight: .light))
                                                .foregroundColor(.textSecondary)
                                        )
                                        .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))

                                    Text(drawnCard.position.name)
                                        .font(TaroTypography.caption2)
                                        .foregroundColor(.textMuted)
                                        .lineLimit(1)
                                }
                            }
                        }
                    }
                }
                .padding(.horizontal, TaroSpacing.lg)

                Spacer()

                // Loading indicator with breathing animation
                GlassPanel(
                    style: .summary,
                    cornerRadius: TaroRadius.xl,
                    padding: TaroSpacing.xl,
                    glowColor: .mysticViolet,
                    glowRadius: 20
                ) {
                    VStack(spacing: TaroSpacing.md) {
                        // Animated loading indicator
                        ZStack {
                            Circle()
                                .stroke(Color.mysticViolet.opacity(0.2), lineWidth: 3)
                                .frame(width: 60, height: 60)

                            Circle()
                                .trim(from: 0, to: 0.7)
                                .stroke(
                                    LinearGradient(
                                        colors: [.mysticViolet, .mysticCyan],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ),
                                    style: StrokeStyle(lineWidth: 3, lineCap: .round)
                                )
                                .frame(width: 60, height: 60)
                                .rotationEffect(.degrees(animationPhase))
                        }
                        .scaleEffect(breathingScale)
                        .opacity(pulseOpacity + 0.5)

                        Text("Weaving your reading...")
                            .font(TaroTypography.mystical(16, weight: .light))
                            .foregroundColor(.textSecondary)

                        Text("The cards speak through the local oracle")
                            .font(TaroTypography.caption)
                            .foregroundColor(.textMuted)
                    }
                }
                .padding(.horizontal, TaroSpacing.xl)

                Spacer()

                // Placeholder: Skip button for development
                GlassButton("Skip (Dev Only)", style: .text) {
                    // Simulate interpretation generation
                    let mockInterpretation = generateMockInterpretation()
                    readingSession.setInterpretation(mockInterpretation)
                }
                .padding(.bottom, TaroSpacing.xl)
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            // Rotation animation
            withAnimation(
                Animation
                    .linear(duration: 1.5)
                    .repeatForever(autoreverses: false)
            ) {
                animationPhase = 360
            }

            // Breathing animation
            withAnimation(
                Animation
                    .easeInOut(duration: 2)
                    .repeatForever(autoreverses: true)
            ) {
                breathingScale = 1.1
                pulseOpacity = 0.6
            }

            // Auto-advance after delay
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
        .preferredColorScheme(.dark)
}
