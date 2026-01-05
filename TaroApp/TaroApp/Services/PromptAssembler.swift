import Foundation

// MARK: - Prompt Assembler

/// Singleton service for building optimized prompts from pre-calculated data
/// Follows the "atomic building blocks" strategy to minimize token usage
/// Target: ~800 tokens input (vs 4000+ with naive approach)
final class PromptAssembler {
    static let shared = PromptAssembler()

    // MARK: - Dependencies

    private let dataService = DataService.shared

    // MARK: - Initialization

    private init() {}

    // MARK: - Public API

    /// Assembles an optimized prompt for LLM generation
    /// Uses pre-calculated snippets rather than raw card data
    /// - Parameters:
    ///   - drawnCards: The cards drawn for this reading
    ///   - question: Optional user question
    ///   - style: Reading style (balanced, mystical, practical)
    /// - Returns: Optimized prompt string in Phi-3 chat format
    func assemblePrompt(
        for drawnCards: [DrawnCard],
        question: String?,
        style: ReadingStyle = .balanced
    ) -> String {
        // Build the card context using pre-calculated snippets
        let cardContext = buildCardContext(for: drawnCards)

        // Detect notable combinations
        let combinationsContext = buildCombinationsContext(for: drawnCards)

        // Calculate elemental flow
        let elementalContext = buildElementalContext(for: drawnCards)

        // Get style instruction
        let styleInstruction = stylePrompt(for: style)

        // Build user question context
        let questionContext = question?.isEmpty == false
            ? "QUESTION: \"\(question!)\"\n\n"
            : ""

        // Assemble using Phi-3 chat format for optimal performance
        let systemPrompt = """
        You are crafting a tarot reading. Weave the provided card interpretations into a cohesive narrative. \(styleInstruction)
        """

        let userPrompt = """
        \(questionContext)\(cardContext)\(combinationsContext)\(elementalContext)
        Weave these elements into a flowing interpretation (3-4 paragraphs). Address the seeker directly. End with actionable insight.
        """

        // Use Phi-3 chat format tokens
        return """
        <|system|>
        \(systemPrompt)<|end|>
        <|user|>
        \(userPrompt)<|end|>
        <|assistant|>
        """
    }

    /// Estimates token count for a prompt (rough approximation)
    /// Phi-3 uses roughly 4 chars per token on average
    func estimateTokenCount(_ text: String) -> Int {
        text.count / 4
    }

    // MARK: - Private Helpers

    /// Builds card context using pre-calculated position-specific snippets
    private func buildCardContext(for drawnCards: [DrawnCard]) -> String {
        var context = ""

        for drawnCard in drawnCards {
            let cardName = drawnCard.card.name
            let positionName = drawnCard.position.name
            let orientation = drawnCard.isReversed ? "Reversed" : "Upright"

            // Get the pre-calculated position-specific snippet
            let positionSlug = drawnCard.position.slug
            let snippet = dataService.positionModifier(
                for: cardName,
                position: positionSlug,
                isReversed: drawnCard.isReversed
            )

            context += "\(positionName.uppercased()) - \(cardName) (\(orientation)):\n"

            if let snippet = snippet {
                // Use the pre-calculated snippet (optimized path)
                context += "\"\(snippet)\"\n\n"
            } else {
                // Fallback to base meaning if snippet not available
                let baseMeaning = dataService.baseMeaning(
                    for: cardName,
                    isReversed: drawnCard.isReversed
                ) ?? "A card of significance in your reading."
                context += "\(baseMeaning)\n\n"
            }
        }

        return context
    }

    /// Builds combinations context from detected card pairings
    private func buildCombinationsContext(for drawnCards: [DrawnCard]) -> String {
        let combinations = dataService.findAllCombinations(in: drawnCards)

        guard !combinations.isEmpty else { return "" }

        var context = "NOTABLE COMBINATIONS:\n"
        for combo in combinations {
            let cards = combo.cards.joined(separator: " + ")
            context += "• \(cards): \(combo.meaning)\n"
        }
        context += "\n"

        return context
    }

    /// Builds elemental flow context
    private func buildElementalContext(for drawnCards: [DrawnCard]) -> String {
        let elementalFlow = ElementalFlow(from: drawnCards)
        let elements = drawnCards.map { $0.card.element.rawValue.capitalized }
        let flow = elements.joined(separator: " → ")

        var context = "ELEMENTAL FLOW: \(flow)\n"

        // Add elemental analysis
        if let dominant = elementalFlow.dominantElement {
            context += "Dominant \(dominant.rawValue.capitalized) energy: \(elementDescription(for: dominant))\n"
        } else {
            context += "Balanced elemental energies present.\n"
        }

        // Add elemental interactions for adjacent cards
        if drawnCards.count >= 2 {
            let interactions = analyzeElementalInteractions(drawnCards)
            if !interactions.isEmpty {
                context += interactions
            }
        }

        context += "\n"
        return context
    }

    /// Returns style-specific prompt instruction
    private func stylePrompt(for style: ReadingStyle) -> String {
        switch style {
        case .balanced:
            return "Balance intuitive insight with practical guidance. Be warm and accessible."
        case .mystical:
            return "Use rich symbolic language and poetic imagery. Speak to the soul's journey."
        case .practical:
            return "Focus on clear, actionable guidance. Be direct and grounded."
        }
    }

    /// Returns description for dominant element
    private func elementDescription(for element: Element) -> String {
        switch element {
        case .fire:
            return "Passion, action, and creative force drive this reading."
        case .water:
            return "Emotions, intuition, and deep feelings flow through this reading."
        case .air:
            return "Thought, communication, and mental clarity shape this reading."
        case .earth:
            return "Stability, practicality, and material concerns ground this reading."
        }
    }

    /// Analyzes elemental interactions between adjacent cards
    private func analyzeElementalInteractions(_ drawnCards: [DrawnCard]) -> String {
        guard drawnCards.count >= 2 else { return "" }

        var interactions: [String] = []

        for i in 0..<(drawnCards.count - 1) {
            let current = drawnCards[i].card.element
            let next = drawnCards[i + 1].card.element

            if current != next {
                let relationship = elementalRelationship(current, next)
                if relationship != .neutral {
                    let desc = relationship == .harmonious
                        ? "\(current.rawValue.capitalized) flows harmoniously into \(next.rawValue.capitalized)"
                        : "\(current.rawValue.capitalized) creates tension with \(next.rawValue.capitalized)"
                    interactions.append(desc)
                }
            }
        }

        return interactions.isEmpty ? "" : interactions.joined(separator: ". ") + ".\n"
    }

    /// Determines relationship between two elements
    private func elementalRelationship(_ e1: Element, _ e2: Element) -> ElementalRelationship {
        // Harmonious pairs
        let harmoniousPairs: Set<Set<Element>> = [
            [.fire, .air],      // Air feeds Fire
            [.water, .earth],   // Earth contains Water
            [.fire, .earth],    // Earth grounds Fire
            [.water, .air]      // Air moves Water
        ]

        // Challenging pairs
        let challengingPairs: Set<Set<Element>> = [
            [.fire, .water],    // Water extinguishes Fire
            [.air, .earth]      // Earth stifles Air
        ]

        let pair: Set<Element> = [e1, e2]

        if harmoniousPairs.contains(pair) {
            return .harmonious
        } else if challengingPairs.contains(pair) {
            return .challenging
        }
        return .neutral
    }
}

// MARK: - Extended Prompt Formats

extension PromptAssembler {
    /// Generates a minimal prompt for quick readings (single card)
    func assembleQuickPrompt(for card: DrawnCard, question: String?) -> String {
        let cardName = card.card.name
        let orientation = card.isReversed ? "Reversed" : "Upright"
        let positionSlug = card.position.slug

        let snippet = dataService.positionModifier(
            for: cardName,
            position: positionSlug,
            isReversed: card.isReversed
        ) ?? dataService.baseMeaning(for: cardName, isReversed: card.isReversed) ?? ""

        let questionText = question.map { "Question: \"\($0)\"\n" } ?? ""

        return """
        <|system|>
        You are giving a brief tarot insight. Be warm and direct.<|end|>
        <|user|>
        \(questionText)\(cardName) (\(orientation)) as \(card.position.name):
        \(snippet)

        Give a concise 2-3 sentence interpretation.<|end|>
        <|assistant|>
        """
    }

    /// Generates prompt optimized for Celtic Cross (10 cards)
    /// Uses more compact format to stay within token limits
    func assembleCelticCrossPrompt(
        for drawnCards: [DrawnCard],
        question: String?
    ) -> String {
        // For larger spreads, use even more compact snippets
        var cardContext = ""

        for drawnCard in drawnCards {
            let cardName = drawnCard.card.name
            let positionName = drawnCard.position.name
            let orientation = drawnCard.isReversed ? "R" : "U" // Compact notation

            // Get abbreviated snippet (first sentence only for large spreads)
            let positionSlug = drawnCard.position.slug
            var snippet = dataService.positionModifier(
                for: cardName,
                position: positionSlug,
                isReversed: drawnCard.isReversed
            ) ?? ""

            // Truncate to first sentence for token efficiency
            if let firstSentenceEnd = snippet.firstIndex(of: ".") {
                snippet = String(snippet[...firstSentenceEnd])
            }

            cardContext += "• \(positionName): \(cardName) (\(orientation)) - \(snippet)\n"
        }

        let combinations = dataService.findAllCombinations(in: drawnCards)
        let comboContext = combinations.prefix(3).map { // Limit to top 3 combinations
            "\($0.cards.joined(separator: "+")): \($0.meaning)"
        }.joined(separator: "\n")

        let elementalFlow = ElementalFlow(from: drawnCards)
        let elementSummary = elementalFlow.dominantElement.map { "Dominant: \($0.rawValue)" } ?? "Balanced"

        let questionText = question.map { "Q: \"\($0)\"\n\n" } ?? ""

        return """
        <|system|>
        Weave a Celtic Cross reading. Address the central cross first, then the staff. Be insightful but concise.<|end|>
        <|user|>
        \(questionText)\(cardContext)
        \(comboContext.isEmpty ? "" : "Combinations:\n\(comboContext)\n")
        Elements: \(elementSummary)

        Provide a cohesive interpretation (4-5 paragraphs). End with guidance.<|end|>
        <|assistant|>
        """
    }
}

// MARK: - Debug Helpers

#if DEBUG
extension PromptAssembler {
    /// Returns debug information about a prompt
    func debugPromptInfo(
        for drawnCards: [DrawnCard],
        question: String?,
        style: ReadingStyle
    ) -> String {
        let prompt = assemblePrompt(for: drawnCards, question: question, style: style)
        let estimatedTokens = estimateTokenCount(prompt)
        let combinations = dataService.findAllCombinations(in: drawnCards)

        return """
        === PROMPT DEBUG ===
        Cards: \(drawnCards.count)
        Question: \(question ?? "None")
        Style: \(style.rawValue)
        Combinations found: \(combinations.count)
        Estimated tokens: \(estimatedTokens)
        Character count: \(prompt.count)
        ====================
        """
    }
}
#endif
