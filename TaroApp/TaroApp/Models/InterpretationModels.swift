import Foundation

// MARK: - Base Meanings

/// Container for all card base meanings (upright/reversed)
struct BaseMeanings: Codable {
    let major: [String: CardMeaning]
    let minor: [String: CardMeaning]?

    /// Get meaning for a card by name
    func meaning(for cardName: String) -> CardMeaning? {
        major[cardName] ?? minor?[cardName]
    }
}

/// Upright and reversed meanings for a card
struct CardMeaning: Codable {
    let upright: String
    let reversed: String

    /// Get meaning based on orientation
    func meaning(isReversed: Bool) -> String {
        isReversed ? reversed : upright
    }
}

// MARK: - Position Modifiers

/// Container for position definitions and card-in-position modifiers
struct PositionModifiersData: Codable {
    let positions: [String: PositionDefinition]
    let modifiers: [String: CardPositionModifiers]
}

/// Definition of a position (name and description)
struct PositionDefinition: Codable {
    let name: String
    let description: String
}

/// All position modifiers for a single card (upright and reversed)
struct CardPositionModifiers: Codable {
    let upright: [String: String]
    let reversed: [String: String]

    /// Get modifier for a specific position and orientation
    func modifier(for positionId: String, isReversed: Bool) -> String? {
        isReversed ? reversed[positionId] : upright[positionId]
    }
}

// MARK: - Combinations

/// Container for card combinations
struct CombinationsData: Codable {
    let combinations: [CardCombination]
}

/// A notable pairing of two cards with special meaning
struct CardCombination: Codable, Identifiable {
    let cards: [String]
    let meaning: String

    var id: String {
        cards.sorted().joined(separator: "-")
    }

    /// Check if this combination matches a pair of cards
    func matches(card1: String, card2: String) -> Bool {
        let pair = Set([card1, card2])
        let comboPair = Set(cards)
        return pair == comboPair
    }
}

// MARK: - Elemental Dynamics

/// Elemental interaction between two elements
struct ElementalInteraction: Identifiable {
    let element1: Element
    let element2: Element
    let relationship: ElementalRelationship
    let description: String

    var id: String {
        "\(element1.rawValue)-\(element2.rawValue)"
    }
}

enum ElementalRelationship: String {
    case harmonious
    case challenging
    case neutral

    var displayName: String {
        rawValue.capitalized
    }
}

// MARK: - Interpretation Result

/// Complete interpretation for a drawn card in a reading
struct CardInterpretation {
    let drawnCard: DrawnCard
    let baseMeaning: String
    let positionModifier: String?

    /// Combined interpretation text
    var fullInterpretation: String {
        if let modifier = positionModifier {
            return "\(modifier)\n\n\(baseMeaning)"
        }
        return baseMeaning
    }
}

// MARK: - Reading Interpretation

/// Complete interpretation data for a reading
struct ReadingInterpretation {
    let cardInterpretations: [CardInterpretation]
    let combinations: [CardCombination]
    let elementalFlow: ElementalFlow

    /// Find all detected combinations in the reading
    static func findCombinations(
        in drawnCards: [DrawnCard],
        from allCombinations: [CardCombination]
    ) -> [CardCombination] {
        var found: [CardCombination] = []
        let cardNames = drawnCards.map { $0.card.name }

        for i in 0..<cardNames.count {
            for j in (i+1)..<cardNames.count {
                for combo in allCombinations {
                    if combo.matches(card1: cardNames[i], card2: cardNames[j]) {
                        found.append(combo)
                    }
                }
            }
        }

        return found
    }
}

/// Elemental flow analysis for a reading
struct ElementalFlow {
    let elements: [Element]
    let summary: String

    init(from drawnCards: [DrawnCard]) {
        self.elements = drawnCards.map { $0.card.element }
        self.summary = Self.generateSummary(elements: elements)
    }

    private static func generateSummary(elements: [Element]) -> String {
        guard !elements.isEmpty else { return "" }

        let elementNames = elements.map { $0.rawValue }
        let flow = elementNames.joined(separator: " → ")

        // Count dominant element
        var counts: [Element: Int] = [:]
        for element in elements {
            counts[element, default: 0] += 1
        }

        if let dominant = counts.max(by: { $0.value < $1.value }) {
            if dominant.value > elements.count / 2 {
                return "\(flow)\nDominant: \(dominant.key.rawValue) energy"
            }
        }

        return flow
    }
}
