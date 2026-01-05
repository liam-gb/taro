import SwiftUI

struct HomeView: View {
    @EnvironmentObject var readingSession: ReadingSession

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: TaroSpacing.xl) {
                Spacer()

                // App title
                VStack(spacing: TaroSpacing.xs) {
                    Text("TARO")
                        .font(TaroTypography.mystical(48, weight: .ultraLight))
                        .tracking(16)
                        .foregroundColor(.textPrimary)

                    Text("Private Tarot Readings")
                        .font(TaroTypography.ethereal(14, weight: .light))
                        .foregroundColor(.textSecondary)
                }

                Spacer()

                // Spread selection
                VStack(spacing: TaroSpacing.md) {
                    Text("Choose Your Spread")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                        .textCase(.uppercase)
                        .tracking(2)

                    ForEach(SpreadType.allCases) { spread in
                        GlassPanel(style: .card, cornerRadius: TaroRadius.md, padding: 0) {
                            Button(action: {
                                readingSession.selectSpread(spread)
                            }) {
                                HStack {
                                    VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                                        Text(spread.displayName)
                                            .font(TaroTypography.ethereal(16, weight: .medium))
                                            .foregroundColor(.textPrimary)

                                        Text("\(spread.cardCount) card\(spread.cardCount == 1 ? "" : "s")")
                                            .font(TaroTypography.caption)
                                            .foregroundColor(.textSecondary)
                                    }

                                    Spacer()

                                    Image(systemName: "chevron.right")
                                        .font(.system(size: 14, weight: .medium))
                                        .foregroundColor(.textMuted)
                                }
                                .padding(.horizontal, TaroSpacing.lg)
                                .padding(.vertical, TaroSpacing.md)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
                .padding(.horizontal, TaroSpacing.lg)

                Spacer()

                // History link
                GlassButton("Reading History", icon: "clock.arrow.circlepath", style: .text) {
                    // TODO: Navigate to history
                }
                .padding(.bottom, TaroSpacing.xl)
            }
        }
        .navigationBarHidden(true)
    }
}

#Preview {
    HomeView()
        .environmentObject(ReadingSession())
        .preferredColorScheme(.dark)
}
