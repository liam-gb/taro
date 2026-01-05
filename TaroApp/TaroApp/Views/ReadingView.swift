import SwiftUI

struct ReadingView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var showShareSheet = false

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            ScrollView {
                VStack(spacing: TaroSpacing.lg) {
                    // Header
                    VStack(spacing: TaroSpacing.xs) {
                        Text(readingSession.selectedSpread?.displayName ?? "Your Reading")
                            .font(TaroTypography.mystical(24, weight: .light))
                            .foregroundColor(.textPrimary)

                        if !readingSession.question.isEmpty {
                            Text("\"\(readingSession.question)\"")
                                .font(TaroTypography.mystical(14, weight: .light))
                                .foregroundColor(.textSecondary)
                                .italic()
                        }

                        Text(Date(), style: .date)
                            .font(TaroTypography.caption)
                            .foregroundColor(.textMuted)
                    }
                    .padding(.top, TaroSpacing.xl)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Cards display
                    GlassPanel(style: .card, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
                        VStack(spacing: TaroSpacing.md) {
                            Text("Your Cards")
                                .font(TaroTypography.caption)
                                .foregroundColor(.textMuted)
                                .textCase(.uppercase)
                                .tracking(1)

                            LazyVGrid(columns: [
                                GridItem(.adaptive(minimum: 100, maximum: 120))
                            ], spacing: TaroSpacing.md) {
                                ForEach(readingSession.drawnCards) { drawnCard in
                                    DrawnCardTile(drawnCard: drawnCard)
                                }
                            }
                        }
                    }
                    .padding(.horizontal, TaroSpacing.lg)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Interpretation
                    GlassPanel(style: .summary, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
                        VStack(alignment: .leading, spacing: TaroSpacing.md) {
                            Text("Interpretation")
                                .font(TaroTypography.caption)
                                .foregroundColor(.textMuted)
                                .textCase(.uppercase)
                                .tracking(1)

                            Text(readingSession.interpretation)
                                .font(TaroTypography.ethereal(16, weight: .regular))
                                .foregroundColor(.textPrimary)
                                .lineSpacing(6)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    .padding(.horizontal, TaroSpacing.lg)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Action buttons
                    VStack(spacing: TaroSpacing.sm) {
                        GlassButton("Save Reading", icon: "square.and.arrow.down", style: .secondary) {
                            // TODO: Save reading
                        }
                        .frame(maxWidth: .infinity)

                        GlassButton("Copy Text", icon: "doc.on.doc", style: .text) {
                            UIPasteboard.general.string = readingSession.interpretation
                        }

                        GlowingButton("New Reading") {
                            readingSession.reset()
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .padding(.horizontal, TaroSpacing.lg)
                    .padding(.bottom, TaroSpacing.xl)
                }
            }
        }
        .navigationBarHidden(true)
    }
}

struct DrawnCardTile: View {
    let drawnCard: DrawnCard

    var body: some View {
        VStack(spacing: TaroSpacing.xs) {
            // Card visual
            ActiveGlassPanel(
                isActive: false,
                cornerRadius: TaroRadius.sm,
                padding: 0
            ) {
                ZStack {
                    LinearGradient(
                        colors: [
                            elementColor.opacity(0.3),
                            elementColor.opacity(0.1)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )

                    VStack(spacing: TaroSpacing.xxs) {
                        if let numeral = drawnCard.card.numeral {
                            Text(numeral)
                                .font(TaroTypography.caption)
                                .foregroundColor(.textSecondary)
                        }

                        Text(cardInitials)
                            .font(TaroTypography.mystical(18, weight: .medium))
                            .foregroundColor(.textPrimary)

                        if drawnCard.isReversed {
                            Text("R")
                                .font(TaroTypography.caption2)
                                .fontWeight(.bold)
                                .foregroundColor(.mysticPink)
                        }
                    }
                }
                .frame(width: 70, height: 100)
            }
            .overlay(
                RoundedRectangle(cornerRadius: TaroRadius.sm)
                    .stroke(elementColor.opacity(0.5), lineWidth: 1)
            )
            .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))

            // Card info
            VStack(spacing: TaroSpacing.xxxs) {
                Text(drawnCard.card.name)
                    .font(TaroTypography.ethereal(11, weight: .medium))
                    .foregroundColor(.textPrimary)
                    .lineLimit(2)
                    .multilineTextAlignment(.center)

                Text(drawnCard.position.name)
                    .font(TaroTypography.caption2)
                    .foregroundColor(.textSecondary)

                Text(drawnCard.orientationText)
                    .font(TaroTypography.caption2)
                    .fontWeight(.medium)
                    .foregroundColor(drawnCard.isReversed ? .mysticPink : .mysticEmerald)
            }
        }
    }

    private var elementColor: Color {
        switch drawnCard.card.element {
        case .fire: return .orange
        case .water: return .mysticCyan
        case .air: return .mysticTeal
        case .earth: return .mysticEmerald
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
        .preferredColorScheme(.dark)
}
