import SwiftUI

struct ShuffleView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var isShuffling = true

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: TaroSpacing.xl) {
                Spacer()

                // Card stack with glass effect and violet glow
                ZStack {
                    // Violet glow behind cards
                    Circle()
                        .fill(TaroGradients.violetGlow)
                        .frame(width: 300, height: 300)
                        .blur(radius: 40)
                        .opacity(0.6)

                    ForEach(0..<5) { index in
                        RoundedRectangle(cornerRadius: TaroRadius.md)
                            .fill(
                                LinearGradient(
                                    colors: [
                                        Color.mysticViolet.opacity(0.2),
                                        Color.deepViolet.opacity(0.15)
                                    ],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                            .background(
                                RoundedRectangle(cornerRadius: TaroRadius.md)
                                    .fill(Material.ultraThinMaterial)
                                    .opacity(0.3)
                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: TaroRadius.md)
                                    .stroke(Color.mysticViolet.opacity(0.3), lineWidth: 1)
                            )
                            .frame(width: 120, height: 180)
                            .shadow(color: Color.mysticViolet.opacity(0.2), radius: 15)
                            .shadow(color: Color.black.opacity(0.3), radius: 8, y: 4)
                            .rotationEffect(.degrees(Double(index - 2) * 3))
                            .offset(x: CGFloat(index - 2) * 2, y: CGFloat(index) * -2)
                    }
                }

                Text("Focus on your question...")
                    .font(TaroTypography.mystical(18, weight: .light))
                    .foregroundColor(.textSecondary)

                if !readingSession.question.isEmpty {
                    Text("\"\(readingSession.question)\"")
                        .font(TaroTypography.mystical(14, weight: .light))
                        .foregroundColor(.textMuted)
                        .italic()
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, TaroSpacing.xl)
                }

                Spacer()

                // Continue button
                GlowingButton("Draw Cards", icon: "sparkles") {
                    readingSession.beginCardSelection()
                }
                .frame(maxWidth: .infinity)
                .padding(.horizontal, TaroSpacing.lg)
                .padding(.bottom, TaroSpacing.xl)
            }
        }
        .navigationBarHidden(true)
    }
}

#Preview {
    ShuffleView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.threeCard)
            session.question = "Should I change careers?"
            return session
        }())
        .preferredColorScheme(.dark)
}
