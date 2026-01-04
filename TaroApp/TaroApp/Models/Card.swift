import Foundation

// MARK: - Card Model

/// Represents a single tarot card from the 78-card deck
struct Card: Identifiable, Codable, Hashable {
    let id: Int
    let name: String
    let arcana: Arcana
    let element: Element
    let keywords: [String]

    // Optional properties for minor arcana
    let suit: Suit?
    let rank: String?
    let numeral: String?

    var isReversed: Bool = false

    enum CodingKeys: String, CodingKey {
        case id, name, arcana, element, keywords, suit, rank, numeral
    }

    init(id: Int, name: String, arcana: Arcana, element: Element, keywords: [String], suit: Suit? = nil, rank: String? = nil, numeral: String? = nil) {
        self.id = id
        self.name = name
        self.arcana = arcana
        self.element = element
        self.keywords = keywords
        self.suit = suit
        self.rank = rank
        self.numeral = numeral
    }
}

// MARK: - Arcana

enum Arcana: String, Codable {
    case major
    case minor
}

// MARK: - Element

enum Element: String, Codable, CaseIterable {
    case fire = "Fire"
    case water = "Water"
    case air = "Air"
    case earth = "Earth"

    var emoji: String {
        switch self {
        case .fire: return "🔥"
        case .water: return "💧"
        case .air: return "💨"
        case .earth: return "🌍"
        }
    }

    var description: String {
        switch self {
        case .fire: return "Passion, creativity, action"
        case .water: return "Emotions, relationships, intuition"
        case .air: return "Thoughts, conflict, truth"
        case .earth: return "Finances, career, material"
        }
    }
}

// MARK: - Suit

enum Suit: String, Codable, CaseIterable {
    case wands = "Wands"
    case cups = "Cups"
    case swords = "Swords"
    case pentacles = "Pentacles"

    var element: Element {
        switch self {
        case .wands: return .fire
        case .cups: return .water
        case .swords: return .air
        case .pentacles: return .earth
        }
    }

    var domain: String {
        switch self {
        case .wands: return "passion, creativity, action"
        case .cups: return "emotions, relationships, intuition"
        case .swords: return "thoughts, conflict, truth"
        case .pentacles: return "finances, career, material"
        }
    }
}

// MARK: - Drawn Card

/// A card that has been drawn in a reading, with position and orientation
struct DrawnCard: Identifiable, Hashable {
    let id = UUID()
    let card: Card
    let position: Position
    let isReversed: Bool

    var orientationText: String {
        isReversed ? "Reversed" : "Upright"
    }
}

// MARK: - Card Extensions

extension Card {
    /// Display name including suit for minor arcana
    var displayName: String {
        name
    }

    /// Slug for looking up interpretations
    var slug: String {
        name.lowercased().replacingOccurrences(of: " ", with: "-")
    }

    /// Returns a copy with reversed state toggled
    func withOrientation(reversed: Bool) -> Card {
        var copy = self
        copy.isReversed = reversed
        return copy
    }
}
