import Foundation

// MARK: - LLM Service

/// Core service for local LLM inference using llama.cpp
/// Provides streaming text generation for tarot readings
@MainActor
final class LLMService: ObservableObject {
    static let shared = LLMService()

    // MARK: - Published State

    @Published private(set) var isGenerating = false
    @Published private(set) var isModelReady = false
    @Published private(set) var currentError: LLMError?

    // MARK: - Dependencies

    private let modelManager = ModelManager.shared
    private let dataService = DataService.shared

    // MARK: - Private State

    private var currentTask: Task<Void, Never>?
    private let inferenceQueue = DispatchQueue(label: "com.taro.llm.inference", qos: .userInitiated)

    // MARK: - Errors

    enum LLMError: LocalizedError {
        case modelNotLoaded
        case generationFailed(String)
        case cancelled
        case invalidInput
        case contextOverflow

        var errorDescription: String? {
            switch self {
            case .modelNotLoaded:
                return "The AI model is not ready. Please wait for it to load."
            case .generationFailed(let reason):
                return "Failed to generate reading: \(reason)"
            case .cancelled:
                return "Generation was cancelled."
            case .invalidInput:
                return "Invalid input provided for generation."
            case .contextOverflow:
                return "The reading context is too long. Please try with fewer cards."
            }
        }
    }

    // MARK: - Initialization

    private init() {
        // Observe model manager state
        Task {
            for await _ in modelManager.$state.values {
                isModelReady = modelManager.state.isReady
            }
        }
    }

    // MARK: - Public API

    /// Initialize the LLM service (loads model if supported)
    func initialize() async {
        guard DeviceCapability.supportsLocalLLM else {
            print("LLMService: Device does not support local LLM")
            return
        }

        do {
            try await modelManager.loadModel()
            isModelReady = true
        } catch {
            print("LLMService: Failed to load model: \(error)")
            currentError = .generationFailed(error.localizedDescription)
        }
    }

    /// Generate a tarot reading interpretation
    /// Returns an AsyncThrowingStream of tokens for real-time UI updates
    func generateReading(
        for drawnCards: [DrawnCard],
        question: String?,
        style: ReadingStyle = .balanced
    ) -> AsyncThrowingStream<String, Error> {
        AsyncThrowingStream { continuation in
            let task = Task {
                do {
                    try await performGeneration(
                        drawnCards: drawnCards,
                        question: question,
                        style: style,
                        continuation: continuation
                    )
                    continuation.finish()
                } catch {
                    continuation.finish(throwing: error)
                }
            }

            continuation.onTermination = { @Sendable _ in
                task.cancel()
            }

            currentTask = task
        }
    }

    /// Generate a complete reading (non-streaming)
    func generateReadingComplete(
        for drawnCards: [DrawnCard],
        question: String?,
        style: ReadingStyle = .balanced
    ) async throws -> String {
        var result = ""
        for try await token in generateReading(for: drawnCards, question: question, style: style) {
            result += token
        }
        return result
    }

    /// Cancel any ongoing generation
    func cancelGeneration() {
        currentTask?.cancel()
        currentTask = nil
        isGenerating = false
    }

    /// Check if LLM is available on this device
    var isAvailable: Bool {
        DeviceCapability.supportsLocalLLM
    }

    // MARK: - Private Generation

    private func performGeneration(
        drawnCards: [DrawnCard],
        question: String?,
        style: ReadingStyle,
        continuation: AsyncThrowingStream<String, Error>.Continuation
    ) async throws {
        guard isModelReady else {
            throw LLMError.modelNotLoaded
        }

        guard !drawnCards.isEmpty else {
            throw LLMError.invalidInput
        }

        isGenerating = true
        currentError = nil

        defer {
            Task { @MainActor in
                isGenerating = false
            }
        }

        // Check for cancellation
        try Task.checkCancellation()

        // Build the prompt
        let prompt = buildPrompt(
            for: drawnCards,
            question: question,
            style: style
        )

        // For now, simulate streaming generation
        // In actual implementation, this would use llama.cpp inference
        try await simulateGeneration(
            prompt: prompt,
            config: style.config,
            continuation: continuation
        )
    }

    // MARK: - Prompt Building

    private func buildPrompt(
        for drawnCards: [DrawnCard],
        question: String?,
        style: ReadingStyle
    ) -> String {
        // Get interpretations from DataService
        let reading = dataService.interpretation(for: drawnCards)

        // Build card context
        var cardContext = ""
        for (index, interpretation) in reading.cardInterpretations.enumerated() {
            let card = interpretation.drawnCard
            let orientation = card.isReversed ? "reversed" : "upright"
            cardContext += """
            \(index + 1). \(card.position.name): \(card.card.name) (\(orientation))
               Keywords: \(card.card.keywords.joined(separator: ", "))
               Base meaning: \(interpretation.baseMeaning)
            """
            if let modifier = interpretation.positionModifier {
                cardContext += "\n   Position context: \(modifier)"
            }
            cardContext += "\n\n"
        }

        // Add combinations if found
        var combinationsContext = ""
        if !reading.combinations.isEmpty {
            combinationsContext = "Card Combinations:\n"
            for combo in reading.combinations {
                combinationsContext += "- \(combo.card1) + \(combo.card2): \(combo.meaning)\n"
            }
            combinationsContext += "\n"
        }

        // Add elemental balance
        let elementalContext = """
        Elemental Balance: \(reading.elementalFlow.dominantElement?.rawValue.capitalized ?? "Balanced")
        \(reading.elementalFlow.summary)
        """

        // Build the full prompt using Phi-3 chat format
        let styleInstruction: String
        switch style {
        case .balanced:
            styleInstruction = "Provide a balanced interpretation that combines intuitive insight with practical guidance."
        case .mystical:
            styleInstruction = "Provide a deeply symbolic and poetic interpretation, rich with mystical imagery and spiritual insight."
        case .practical:
            styleInstruction = "Provide direct, actionable guidance focused on practical steps and clear advice."
        }

        let userQuestion = question?.isEmpty == false ? "The querent asks: \"\(question!)\"\n\n" : ""

        let prompt = """
        <|system|>
        You are a wise and intuitive tarot reader. You provide thoughtful, personalized interpretations that weave together the meanings of the cards, their positions, and the querent's question. \(styleInstruction)<|end|>
        <|user|>
        \(userQuestion)The following cards were drawn:

        \(cardContext)\(combinationsContext)\(elementalContext)

        Please provide a cohesive interpretation of this tarot reading. Weave together the individual card meanings into a narrative that addresses the querent's situation. Be insightful but accessible.<|end|>
        <|assistant|>
        """

        return prompt
    }

    // MARK: - Simulated Generation (Placeholder)

    /// Simulates streaming generation for development/testing
    /// This will be replaced with actual llama.cpp inference
    private func simulateGeneration(
        prompt: String,
        config: GenerationConfig,
        continuation: AsyncThrowingStream<String, Error>.Continuation
    ) async throws {
        // Generate a placeholder response based on the prompt
        // In production, this would call llama.cpp

        let response = generatePlaceholderReading()

        // Simulate streaming by yielding words with delays
        let words = response.components(separatedBy: " ")
        for (index, word) in words.enumerated() {
            try Task.checkCancellation()

            // Yield the word (add space except for first word)
            let token = index == 0 ? word : " " + word
            continuation.yield(token)

            // Variable delay to simulate generation speed
            let delay = UInt64.random(in: 20_000_000...80_000_000) // 20-80ms
            try await Task.sleep(nanoseconds: delay)
        }
    }

    private func generatePlaceholderReading() -> String {
        """
        The cards have spoken, and their wisdom flows through this reading like starlight through midnight water.

        Your journey begins with the energy present in the first position, which speaks to the foundation of your question. The cards here reveal patterns that have been forming beneath the surface, waiting for the right moment to emerge into your conscious awareness.

        As we move deeper into the spread, a narrative begins to unfold. The interplay between the cards suggests a period of transformation ahead. There are challenges to be faced, yes, but within each challenge lies an opportunity for growth and self-discovery.

        The elemental energies present in this reading create a dynamic flow. Notice how they interact—some supporting each other, others creating productive tension that sparks change. This balance is key to understanding the path forward.

        Take time to sit with these insights. The cards offer guidance, but the power to shape your destiny remains in your hands. Trust your intuition as you navigate the coming days, and remember that every ending contains the seed of a new beginning.

        *This reading was generated locally on your device, ensuring your personal reflections remain private.*
        """
    }
}

// MARK: - Convenience Extensions

extension LLMService {
    /// Generate a quick single-card reading
    func generateQuickReading(
        for card: DrawnCard,
        question: String?
    ) async throws -> String {
        try await generateReadingComplete(
            for: [card],
            question: question,
            style: .balanced
        )
    }
}

// MARK: - Debug Helpers

#if DEBUG
extension LLMService {
    /// Test generation without model for development
    func testGeneration() async throws -> String {
        let deck = CardDeck.shuffled()
        let positions = SpreadType.threeCard.spread.positions
        let drawnCards = positions.enumerated().map { index, position in
            DrawnCard(
                card: deck[index],
                position: position,
                isReversed: Bool.random()
            )
        }

        return try await generateReadingComplete(
            for: drawnCards,
            question: "What guidance do the cards offer for my creative projects?",
            style: .mystical
        )
    }
}
#endif
