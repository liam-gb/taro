import SwiftUI

struct QuestionInputView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @FocusState private var isQuestionFocused: Bool

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

                // Spread info
                VStack(spacing: 8) {
                    Text(readingSession.selectedSpread?.displayName ?? "Reading")
                        .font(.system(size: 24, weight: .light, design: .serif))
                        .foregroundColor(.white)

                    Text("\(readingSession.selectedSpread?.cardCount ?? 0) cards")
                        .font(.system(size: 14, weight: .light))
                        .foregroundColor(.white.opacity(0.5))
                }

                // Question input
                VStack(alignment: .leading, spacing: 12) {
                    Text("What would you like guidance on?")
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(.white.opacity(0.5))
                        .textCase(.uppercase)
                        .tracking(1)

                    TextField("Enter your question (optional)", text: $readingSession.question, axis: .vertical)
                        .font(.system(size: 16, weight: .regular))
                        .foregroundColor(.white)
                        .padding(16)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(.white.opacity(0.05))
                                .overlay(
                                    RoundedRectangle(cornerRadius: 12)
                                        .stroke(.white.opacity(0.1), lineWidth: 1)
                                )
                        )
                        .focused($isQuestionFocused)
                        .lineLimit(3...6)
                }
                .padding(.horizontal, 24)

                Spacer()

                // Action buttons
                VStack(spacing: 16) {
                    Button(action: {
                        readingSession.startReading()
                    }) {
                        Text("Begin Reading")
                            .font(.system(size: 16, weight: .semibold))
                            .foregroundColor(.black)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(
                                RoundedRectangle(cornerRadius: 12)
                                    .fill(.white)
                            )
                    }

                    Button(action: {
                        readingSession.reset()
                    }) {
                        Text("Back")
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(.white.opacity(0.5))
                    }
                }
                .padding(.horizontal, 24)
                .padding(.bottom, 32)
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
}
