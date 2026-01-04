import SwiftUI

struct HomeView: View {
    @EnvironmentObject var readingSession: ReadingSession

    var body: some View {
        ZStack {
            // Background gradient (placeholder for aurora effect)
            LinearGradient(
                colors: [
                    Color(red: 0.05, green: 0.05, blue: 0.15),
                    Color(red: 0.1, green: 0.05, blue: 0.2),
                    Color(red: 0.05, green: 0.1, blue: 0.15)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 32) {
                Spacer()

                // App title
                VStack(spacing: 8) {
                    Text("TARO")
                        .font(.system(size: 48, weight: .ultraLight, design: .serif))
                        .tracking(16)
                        .foregroundColor(.white)

                    Text("Private Tarot Readings")
                        .font(.system(size: 14, weight: .light))
                        .foregroundColor(.white.opacity(0.6))
                }

                Spacer()

                // Spread selection
                VStack(spacing: 16) {
                    Text("Choose Your Spread")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(.white.opacity(0.5))
                        .textCase(.uppercase)
                        .tracking(2)

                    ForEach(SpreadType.allCases) { spread in
                        SpreadButton(spread: spread) {
                            readingSession.selectSpread(spread)
                        }
                    }
                }
                .padding(.horizontal, 24)

                Spacer()

                // History link (placeholder)
                Button(action: {
                    // TODO: Navigate to history
                }) {
                    HStack {
                        Image(systemName: "clock.arrow.circlepath")
                        Text("Reading History")
                    }
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(.white.opacity(0.5))
                }
                .padding(.bottom, 32)
            }
        }
        .navigationBarHidden(true)
    }
}

struct SpreadButton: View {
    let spread: SpreadType
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(spread.displayName)
                        .font(.system(size: 16, weight: .medium))
                        .foregroundColor(.white)

                    Text("\(spread.cardCount) card\(spread.cardCount == 1 ? "" : "s")")
                        .font(.system(size: 12, weight: .light))
                        .foregroundColor(.white.opacity(0.5))
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(.white.opacity(0.3))
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 16)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(.white.opacity(0.05))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(.white.opacity(0.1), lineWidth: 1)
                    )
            )
        }
        .buttonStyle(.plain)
    }
}

#Preview {
    HomeView()
        .environmentObject(ReadingSession())
}
