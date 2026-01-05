import SwiftUI

struct GeneratingView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @EnvironmentObject var modelManager: ModelManager
    @EnvironmentObject var llmService: LLMService

    @State private var animationPhase = 0.0
    @State private var breathingScale: CGFloat = 1.0
    @State private var pulseOpacity: Double = 0.3
    @State private var streamedText: String = ""
    @State private var generationError: String?
    @State private var showDeviceUnsupported = false
    @State private var showCopyPromptSheet = false
    @State private var externalPrompt: String = ""
    @State private var elapsedTime: Double = 0
    @State private var statsTimer: Timer?

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

                // Loading/Generation indicator
                if let error = generationError {
                    errorView(error)
                } else if !streamedText.isEmpty {
                    streamingPreview
                } else {
                    loadingIndicator
                }

                Spacer()

                // Model status or cancel button
                if llmService.isGenerating {
                    GlassButton("Cancel", icon: "xmark", style: .secondary) {
                        llmService.cancelGeneration()
                        // Fall back to template-based reading
                        let fallbackInterpretation = generateFallbackInterpretation()
                        readingSession.setInterpretation(fallbackInterpretation)
                    }
                    .padding(.bottom, TaroSpacing.xl)
                } else if !DeviceCapability.supportsLocalLLM {
                    unsupportedDeviceActions
                        .padding(.horizontal, TaroSpacing.xl)
                        .padding(.bottom, TaroSpacing.xl)
                }
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            startAnimations()
        }
        .task {
            await startGeneration()
        }
        .sheet(isPresented: $showDeviceUnsupported) {
            DeviceUnsupportedView()
        }
        .sheet(isPresented: $showCopyPromptSheet) {
            CopyPromptSheet(prompt: externalPrompt, isPresented: $showCopyPromptSheet)
        }
        .onDisappear {
            stopStatsTimer()
        }
    }

    // MARK: - Subviews

    private var loadingIndicator: some View {
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

                if DeviceCapability.supportsLocalLLM {
                    Text("The cards speak through the local oracle")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                } else {
                    Text("Using traditional interpretation")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                }
            }
        }
        .padding(.horizontal, TaroSpacing.xl)
    }

    private var streamingPreview: some View {
        GlassPanel(
            style: .summary,
            cornerRadius: TaroRadius.xl,
            padding: TaroSpacing.lg,
            glowColor: .mysticCyan,
            glowRadius: 15
        ) {
            VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                HStack {
                    Text("Reading in Progress")
                        .font(TaroTypography.caption)
                        .foregroundColor(.mysticCyan)
                        .textCase(.uppercase)
                        .tracking(1)

                    Spacer()

                    // Typing indicator
                    HStack(spacing: 4) {
                        ForEach(0..<3) { i in
                            Circle()
                                .fill(Color.mysticCyan)
                                .frame(width: 6, height: 6)
                                .opacity(0.3 + (0.7 * sin(animationPhase / 60 + Double(i) * 0.5)))
                        }
                    }
                }

                ScrollViewReader { proxy in
                    ScrollView {
                        Text(streamedText)
                            .font(TaroTypography.body)
                            .foregroundColor(.textPrimary)
                            .multilineTextAlignment(.leading)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .id("streamingText")
                    }
                    .frame(maxHeight: 200)
                    .onChange(of: streamedText) { _, _ in
                        withAnimation(.easeOut(duration: 0.1)) {
                            proxy.scrollTo("streamingText", anchor: .bottom)
                        }
                    }
                }

                // Generation stats bar
                generationStatsBar
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    // MARK: - Generation Stats Bar

    private var generationStatsBar: some View {
        HStack(spacing: TaroSpacing.md) {
            // Time elapsed
            HStack(spacing: TaroSpacing.xxs) {
                Image(systemName: "clock")
                    .font(.system(size: 10))
                Text(formatTime(elapsedTime))
                    .font(TaroTypography.caption2)
            }
            .foregroundColor(.textMuted)

            Spacer()

            // Tokens generated
            HStack(spacing: TaroSpacing.xxs) {
                Image(systemName: "text.word.spacing")
                    .font(.system(size: 10))
                Text("\(readingSession.tokensGenerated) tokens")
                    .font(TaroTypography.caption2)
            }
            .foregroundColor(.textMuted)

            // Generation speed
            if readingSession.generationSpeed > 0 {
                HStack(spacing: TaroSpacing.xxs) {
                    Image(systemName: "speedometer")
                        .font(.system(size: 10))
                    Text(String(format: "%.1f tok/s", readingSession.generationSpeed))
                        .font(TaroTypography.caption2)
                }
                .foregroundColor(.mysticCyan)
            }
        }
        .padding(.top, TaroSpacing.xs)
    }

    private func formatTime(_ seconds: Double) -> String {
        let mins = Int(seconds) / 60
        let secs = Int(seconds) % 60
        if mins > 0 {
            return String(format: "%d:%02d", mins, secs)
        }
        return String(format: "%.1fs", seconds)
    }

    // MARK: - Unsupported Device Actions

    private var unsupportedDeviceActions: some View {
        VStack(spacing: TaroSpacing.md) {
            // Device status
            GlassPanel(style: .card, cornerRadius: TaroRadius.lg, padding: TaroSpacing.md) {
                VStack(spacing: TaroSpacing.sm) {
                    HStack(spacing: TaroSpacing.xs) {
                        Image(systemName: "iphone.slash")
                            .font(.system(size: 16))
                            .foregroundColor(.mysticPink)

                        Text("On-Device AI Unavailable")
                            .font(TaroTypography.caption)
                            .foregroundColor(.textSecondary)
                    }

                    Text("Your device doesn't support on-device AI readings. Copy the prompt below to use with your preferred AI assistant.")
                        .font(TaroTypography.caption2)
                        .foregroundColor(.textMuted)
                        .multilineTextAlignment(.center)
                }
            }

            // Copy prompt button
            GlowingButton("Copy Prompt for AI Chat", icon: "doc.on.doc") {
                externalPrompt = generateExternalAIPrompt()
                showCopyPromptSheet = true
            }
        }
    }

    private func errorView(_ error: String) -> some View {
        GlassPanel(
            style: .card,
            cornerRadius: TaroRadius.xl,
            padding: TaroSpacing.lg,
            glowColor: .mysticPink,
            glowRadius: 15
        ) {
            VStack(spacing: TaroSpacing.md) {
                Image(systemName: "exclamationmark.triangle.fill")
                    .font(.system(size: 32))
                    .foregroundColor(.mysticPink)

                Text("Generation Error")
                    .font(TaroTypography.headline)
                    .foregroundColor(.textPrimary)

                Text(error)
                    .font(TaroTypography.caption)
                    .foregroundColor(.textSecondary)
                    .multilineTextAlignment(.center)

                // Action buttons
                VStack(spacing: TaroSpacing.sm) {
                    // Regenerate button
                    GlassButton("Try Again", icon: "arrow.clockwise", style: .primary) {
                        regenerate()
                    }

                    // Fallback option
                    GlassButton("Use Traditional Reading", icon: "doc.text", style: .secondary) {
                        let interpretation = generateFallbackInterpretation()
                        readingSession.setInterpretation(interpretation)
                    }
                }
            }
        }
        .padding(.horizontal, TaroSpacing.xl)
    }

    /// Retry generation after an error
    private func regenerate() {
        generationError = nil
        streamedText = ""
        readingSession.resetGenerationTracking()
        Task {
            await generateWithLLM()
        }
    }

    // MARK: - Generation

    private func startGeneration() async {
        guard DeviceCapability.supportsLocalLLM else { return }

        if modelManager.state.isReady {
            await generateWithLLM()
        } else {
            // Model not ready - wait and retry
            try? await Task.sleep(for: .seconds(2))
            guard !Task.isCancelled, modelManager.state.isReady else { return }
            await generateWithLLM()
        }
    }

    private func generateWithLLM() async {
        streamedText = ""
        generationError = nil

        // Start tracking generation
        readingSession.startGeneration()
        startStatsTimer()

        do {
            for try await token in llmService.generateReading(
                for: readingSession.drawnCards,
                question: readingSession.question.isEmpty ? nil : readingSession.question,
                style: .balanced
            ) {
                streamedText += token
                // Count tokens (approximation: split by spaces/punctuation)
                let tokenCount = token.split(whereSeparator: { $0.isWhitespace || $0.isPunctuation }).count
                if tokenCount > 0 {
                    readingSession.recordTokens(tokenCount)
                } else if !token.isEmpty {
                    readingSession.recordToken()
                }
            }

            // Generation complete
            stopStatsTimer()
            readingSession.completeGeneration()
            readingSession.setInterpretation(streamedText)

            // Log performance stats
            #if DEBUG
            if let latency = readingSession.firstTokenLatency {
                print("GeneratingView: First token latency: \(String(format: "%.2f", latency))s")
            }
            print("GeneratingView: Total tokens: \(readingSession.tokensGenerated)")
            print("GeneratingView: Speed: \(String(format: "%.1f", readingSession.generationSpeed)) tok/s")
            #endif

        } catch is CancellationError {
            // Cancelled - already handled
            stopStatsTimer()
            readingSession.completeGeneration()
        } catch {
            stopStatsTimer()
            readingSession.completeGeneration()
            generationError = error.localizedDescription
        }
    }

    // MARK: - Stats Timer

    private func startStatsTimer() {
        elapsedTime = 0
        statsTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            elapsedTime = readingSession.elapsedGenerationTime
        }
    }

    private func stopStatsTimer() {
        statsTimer?.invalidate()
        statsTimer = nil
    }

    // MARK: - Fallback Interpretation

    private func generateFallbackInterpretation() -> String {
        let dataService = DataService.shared
        let reading = dataService.interpretation(for: readingSession.drawnCards)

        var text = "# Your Tarot Reading\n\n"

        if !readingSession.question.isEmpty {
            text += "*Your question: \"\(readingSession.question)\"*\n\n"
        }

        text += "The cards have been drawn and their wisdom awaits. Let us explore what they reveal.\n\n"

        // Individual card interpretations
        for interpretation in reading.cardInterpretations {
            let card = interpretation.drawnCard
            let orientation = card.isReversed ? "Reversed" : "Upright"

            text += "## \(card.position.name)\n"
            text += "**\(card.card.name)** (\(orientation))\n\n"
            text += "\(interpretation.baseMeaning)\n\n"

            if let modifier = interpretation.positionModifier {
                text += "*In this position:* \(modifier)\n\n"
            }
        }

        // Combinations
        if !reading.combinations.isEmpty {
            text += "## Card Connections\n\n"
            for combo in reading.combinations {
                text += "**\(combo.card1) & \(combo.card2):** \(combo.meaning)\n\n"
            }
        }

        // Elemental summary
        text += "## Elemental Balance\n\n"
        text += "\(reading.elementalFlow.summary)\n\n"

        // Closing
        text += "---\n\n"
        text += "*Take time to reflect on these messages. The cards offer guidance, but your intuition is the key to unlocking their deeper meaning.*"

        return text
    }

    // MARK: - External AI Prompt Generation

    /// Generates a comprehensive prompt for external AI services
    /// Includes all card details, positions, meanings, combinations, and elemental balance
    private func generateExternalAIPrompt() -> String {
        let dataService = DataService.shared
        let reading = dataService.interpretation(for: readingSession.drawnCards)

        var prompt = "I'm seeking guidance from a tarot reading. "

        // Add user's question if provided
        if !readingSession.question.isEmpty {
            prompt += "My question is: \"\(readingSession.question)\"\n\n"
        } else {
            prompt += "Please interpret the following cards for me.\n\n"
        }

        prompt += "Here are the cards I drew:\n\n"

        // Card details with positions, names, orientation, keywords, and meanings
        for (index, interpretation) in reading.cardInterpretations.enumerated() {
            let card = interpretation.drawnCard
            let orientation = card.isReversed ? "Reversed" : "Upright"

            prompt += "\(index + 1). \(card.position.name): \(card.card.name) (\(orientation))\n"
            prompt += "   Keywords: \(card.card.keywords.joined(separator: ", "))\n"
            prompt += "   Base meaning: \(interpretation.baseMeaning)\n"

            if let modifier = interpretation.positionModifier {
                prompt += "   In this position: \(modifier)\n"
            }
            prompt += "\n"
        }

        // Card combinations if any
        if !reading.combinations.isEmpty {
            prompt += "Notable Card Combinations:\n"
            for combo in reading.combinations {
                let cards = combo.cards.joined(separator: " & ")
                prompt += "- \(cards): \(combo.meaning)\n"
            }
            prompt += "\n"
        }

        // Elemental balance
        let elements = readingSession.drawnCards.map { $0.card.element.rawValue.capitalized }
        let elementFlow = elements.joined(separator: " -> ")
        prompt += "Elemental Flow: \(elementFlow)\n"
        prompt += "\(reading.elementalFlow.summary)\n\n"

        // Request for interpretation
        prompt += """
        Please provide a cohesive interpretation of this tarot reading. Weave together the individual card meanings into a narrative that addresses my question or situation. Consider:
        - How each card's position influences its meaning
        - The relationships between the cards
        - The elemental energies present
        - Practical guidance I can apply

        Be insightful, warm, and accessible in your interpretation.
        """

        return prompt
    }

    // MARK: - Animations

    private func startAnimations() {
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
        .environmentObject(ModelManager.shared)
        .environmentObject(LLMService.shared)
        .preferredColorScheme(.dark)
}
