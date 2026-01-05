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
            startGeneration()
        }
        .sheet(isPresented: $showDeviceUnsupported) {
            DeviceUnsupportedView()
        }
        .sheet(isPresented: $showCopyPromptSheet) {
            CopyPromptSheet(prompt: externalPrompt, isPresented: $showCopyPromptSheet)
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

                ScrollView {
                    Text(streamedText)
                        .font(TaroTypography.body)
                        .foregroundColor(.textPrimary)
                        .multilineTextAlignment(.leading)
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
                .frame(maxHeight: 200)
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
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

                GlassButton("Use Traditional Reading", style: .primary) {
                    let interpretation = generateFallbackInterpretation()
                    readingSession.setInterpretation(interpretation)
                }
            }
        }
        .padding(.horizontal, TaroSpacing.xl)
    }

    // MARK: - Generation

    private func startGeneration() {
        // Check if LLM is available
        if DeviceCapability.supportsLocalLLM && modelManager.state.isReady {
            Task {
                await generateWithLLM()
            }
        } else if !DeviceCapability.supportsLocalLLM {
            // Device not supported - don't auto-generate, let user choose action
            // The unsupportedDeviceActions UI will be shown automatically
            return
        } else {
            // Model not ready - wait and retry
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                if modelManager.state.isReady {
                    Task {
                        await generateWithLLM()
                    }
                }
                // If model still not ready, user can see status and take action
            }
        }
    }

    private func generateWithLLM() async {
        streamedText = ""
        generationError = nil

        do {
            for try await token in llmService.generateReading(
                for: readingSession.drawnCards,
                question: readingSession.question.isEmpty ? nil : readingSession.question,
                style: .balanced
            ) {
                streamedText += token
            }

            // Generation complete
            readingSession.setInterpretation(streamedText)

        } catch is CancellationError {
            // Cancelled - already handled
        } catch {
            generationError = error.localizedDescription
        }
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
