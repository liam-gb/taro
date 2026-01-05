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

// MARK: - Element Color Extension (requires SwiftUI import in views)
import SwiftUI

extension Element {
    /// The color associated with this element for UI display
    var color: Color {
        switch self {
        case .fire: return Color(hex: "F97316")    // Orange
        case .water: return .mysticCyan
        case .air: return .mysticTeal
        case .earth: return .mysticEmerald
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
    /// Slug for looking up interpretations
    var slug: String {
        name.lowercased().replacingOccurrences(of: " ", with: "-")
    }
}
