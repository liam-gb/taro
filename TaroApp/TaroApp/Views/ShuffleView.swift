import SwiftUI

struct ShuffleView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var isShuffling = true

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

                // Card stack placeholder
                ZStack {
                    ForEach(0..<5) { index in
                        RoundedRectangle(cornerRadius: 12)
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
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(.white.opacity(0.2), lineWidth: 1)
                            )
                            .frame(width: 120, height: 180)
                            .rotationEffect(.degrees(Double(index - 2) * 3))
                            .offset(x: CGFloat(index - 2) * 2, y: CGFloat(index) * -2)
                    }
                }

                Text("Focus on your question...")
                    .font(.system(size: 18, weight: .light, design: .serif))
                    .foregroundColor(.white.opacity(0.7))

                if !readingSession.question.isEmpty {
                    Text("\"\(readingSession.question)\"")
                        .font(.system(size: 14, weight: .light, design: .serif))
                        .foregroundColor(.white.opacity(0.4))
                        .italic()
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 32)
                }

                Spacer()

                // Continue button
                Button(action: {
                    readingSession.beginCardSelection()
                }) {
                    Text("Draw Cards")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundColor(.black)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(.white)
                        )
                }
                .padding(.horizontal, 24)
                .padding(.bottom, 32)
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
}
