import SwiftUI

struct ShuffleView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var isShuffling = false
    @State private var shufflePhase: ShufflePhase = .idle
    @State private var cardStates: [CardShuffleState] = []
    @State private var showButton = false
    @State private var shuffleTask: Task<Void, Never>?

    private let cardCount = 7
    private let shuffleDuration: Double = 2.5

    enum ShufflePhase {
        case idle
        case spreading
        case shuffling
        case collecting
        case ready
    }

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: TaroSpacing.xl) {
                Spacer()

                // Card stack with shuffle animation
                ZStack {
                    // Violet glow behind cards
                    Circle()
                        .fill(TaroGradients.violetGlow)
                        .frame(width: 300, height: 300)
                        .blur(radius: 40)
                        .opacity(shufflePhase == .shuffling ? 0.8 : 0.5)
                        .animation(.easeInOut(duration: 0.5), value: shufflePhase)

                    // Animated card stack
                    ForEach(Array(cardStates.enumerated()), id: \.offset) { index, state in
                        CardBackDesign(size: .shuffle, showShimmer: shufflePhase == .ready)
                            .offset(x: state.offset.x, y: state.offset.y)
                            .rotationEffect(.degrees(state.rotation))
                            .scaleEffect(state.scale)
                            .zIndex(state.zIndex)
                            .shadow(
                                color: Color.mysticViolet.opacity(shufflePhase == .shuffling ? 0.4 : 0.2),
                                radius: shufflePhase == .shuffling ? 20 : 10
                            )
                    }
                }
                .frame(height: 250)

                // Status text
                VStack(spacing: TaroSpacing.sm) {
                    Text(shuffleStatusText)
                        .font(TaroTypography.mystical(18, weight: .light))
                        .foregroundColor(.textSecondary)
                        .animation(.easeInOut, value: shufflePhase)

                    if !readingSession.question.isEmpty {
                        Text("\"\(readingSession.question)\"")
                            .font(TaroTypography.mystical(14, weight: .light))
                            .foregroundColor(.textMuted)
                            .italic()
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, TaroSpacing.xl)
                    }
                }

                Spacer()

                // Continue button - appears after shuffle
                if showButton {
                    GlowingButton("Draw Cards", icon: "sparkles") {
                        readingSession.beginCardSelection()
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, TaroSpacing.lg)
                    .padding(.bottom, TaroSpacing.xl)
                    .transition(.opacity.combined(with: .move(edge: .bottom)))
                }

                // Shuffle button - shown before shuffle
                if shufflePhase == .idle {
                    GlowingButton("Shuffle the Deck", icon: "shuffle") {
                        startShuffleAnimation()
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal, TaroSpacing.lg)
                    .padding(.bottom, TaroSpacing.xl)
                    .transition(.opacity.combined(with: .move(edge: .bottom)))
                }
            }
            .animation(TaroAnimation.springSmooth, value: showButton)
            .animation(TaroAnimation.springSmooth, value: shufflePhase)
        }
        .navigationBarHidden(true)
        .onAppear {
            initializeCardStates()
        }
        .onDisappear {
            shuffleTask?.cancel()
        }
    }

    private var shuffleStatusText: String {
        switch shufflePhase {
        case .idle:
            return "Focus on your question..."
        case .spreading, .shuffling:
            return "Shuffling the cards..."
        case .collecting:
            return "The cards are aligned..."
        case .ready:
            return "The deck is ready"
        }
    }

    // MARK: - Card State Management

    private func initializeCardStates() {
        cardStates = (0..<cardCount).map { index in
            CardShuffleState(
                offset: CGPoint(x: CGFloat(index - 3) * 2, y: CGFloat(index) * -2),
                rotation: Double(index - 3) * 3,
                scale: 1.0,
                zIndex: Double(index)
            )
        }
    }

    // MARK: - Shuffle Animation

    private func startShuffleAnimation() {
        shuffleTask?.cancel()
        isShuffling = true
        shufflePhase = .spreading

        // Haptic feedback
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()

        // Phase 1: Spread cards out
        withAnimation(.easeOut(duration: 0.5)) {
            spreadCards()
        }

        shuffleTask = Task { @MainActor in
            // Wait for spread animation
            try? await Task.sleep(nanoseconds: 500_000_000)
            guard !Task.isCancelled else { return }

            // Phase 2: Shuffle (random movements)
            shufflePhase = .shuffling
            await performShuffleSequenceAsync()
            guard !Task.isCancelled else { return }

            // Phase 3: Collect cards back
            shufflePhase = .collecting
            withAnimation(TaroAnimation.springSmooth) {
                collectCards()
            }

            // Light haptic for collection
            let lightGenerator = UIImpactFeedbackGenerator(style: .light)
            lightGenerator.impactOccurred()

            // Wait for collect animation (0.5s)
            try? await Task.sleep(nanoseconds: 500_000_000)
            guard !Task.isCancelled else { return }

            // Phase 4: Ready state
            shufflePhase = .ready
            isShuffling = false

            // Success haptic
            let notificationGenerator = UINotificationFeedbackGenerator()
            notificationGenerator.notificationOccurred(.success)

            withAnimation(TaroAnimation.springSmooth.delay(0.3)) {
                showButton = true
            }
        }
    }

    private func spreadCards() {
        for index in cardStates.indices {
            let angle = Double(index - cardCount / 2) * 15
            let radius: CGFloat = 80

            cardStates[index].offset = CGPoint(
                x: sin(angle * .pi / 180) * radius,
                y: cos(angle * .pi / 180) * radius * 0.3 - 20
            )
            cardStates[index].rotation = angle
            cardStates[index].scale = 0.9
        }
    }

    private func performShuffleSequenceAsync() async {
        let shuffleSteps = 6
        let stepDuration = (shuffleDuration - 1.0) / Double(shuffleSteps)
        let stepNanos = UInt64(stepDuration * 1_000_000_000)

        for step in 0..<shuffleSteps {
            guard !Task.isCancelled else { return }

            withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                shuffleStep()
            }

            // Subtle haptic on each shuffle step
            if step % 2 == 0 {
                let generator = UIImpactFeedbackGenerator(style: .soft)
                generator.impactOccurred()
            }

            try? await Task.sleep(nanoseconds: stepNanos)
        }
    }

    private func shuffleStep() {
        // Randomly reorder z-indices
        var indices = Array(0..<cardCount)
        indices.shuffle()

        for (newZ, index) in indices.enumerated() {
            let randomAngle = Double.random(in: -25...25)
            let randomX = CGFloat.random(in: -60...60)
            let randomY = CGFloat.random(in: -30...30)

            cardStates[index].offset = CGPoint(x: randomX, y: randomY)
            cardStates[index].rotation = randomAngle
            cardStates[index].zIndex = Double(newZ)
            cardStates[index].scale = CGFloat.random(in: 0.85...0.95)
        }
    }

    private func collectCards() {
        for index in cardStates.indices {
            cardStates[index].offset = CGPoint(
                x: CGFloat(index - 3) * 2,
                y: CGFloat(index) * -2
            )
            cardStates[index].rotation = Double(index - 3) * 3
            cardStates[index].scale = 1.0
            cardStates[index].zIndex = Double(index)
        }
    }
}

// MARK: - Card Shuffle State

struct CardShuffleState {
    var offset: CGPoint
    var rotation: Double
    var scale: CGFloat
    var zIndex: Double
}

// MARK: - Preview

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
