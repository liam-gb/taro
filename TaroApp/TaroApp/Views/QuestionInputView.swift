import SwiftUI

struct QuestionInputView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @FocusState private var isQuestionFocused: Bool

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: TaroSpacing.xl) {
                Spacer()

                // Spread info
                VStack(spacing: TaroSpacing.xs) {
                    Text(readingSession.selectedSpread?.displayName ?? "Reading")
                        .font(TaroTypography.mystical(24, weight: .light))
                        .foregroundColor(.textPrimary)

                    Text("\(readingSession.selectedSpread?.cardCount ?? 0) cards")
                        .font(TaroTypography.ethereal(14, weight: .light))
                        .foregroundColor(.textSecondary)
                }

                // Question input
                VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                    Text("What would you like guidance on?")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                        .textCase(.uppercase)
                        .tracking(1)

                    TextField("Enter your question (optional)", text: $readingSession.question, axis: .vertical)
                        .font(TaroTypography.ethereal(16, weight: .regular))
                        .foregroundColor(.textPrimary)
                        .padding(TaroSpacing.md)
                        .glassPanel(style: .standard, cornerRadius: TaroRadius.md)
                        .focused($isQuestionFocused)
                        .lineLimit(3...6)
                }
                .padding(.horizontal, TaroSpacing.lg)

                Spacer()

                // Action buttons
                VStack(spacing: TaroSpacing.md) {
                    GlowingButton("Begin Reading", icon: "sparkles") {
                        readingSession.startReading()
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, TaroSpacing.lg)

                    GlassButton("Back", style: .text) {
                        readingSession.reset()
                    }
                }
                .padding(.bottom, TaroSpacing.xl)
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            isQuestionFocused = true
        }
    }
}

#Preview {
    QuestionInputView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.threeCard)
            return session
        }())
        .preferredColorScheme(.dark)
}
