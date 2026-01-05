import Foundation

// MARK: - Card Deck

/// Contains all 78 tarot cards
enum CardDeck {

    // MARK: - Major Arcana

    static let majorArcana: [Card] = [
        Card(id: 0, name: "The Fool", arcana: .major, element: .air, keywords: ["beginnings", "innocence", "spontaneity", "leap of faith"], numeral: "0"),
        Card(id: 1, name: "The Magician", arcana: .major, element: .air, keywords: ["manifestation", "willpower", "skill", "resourcefulness"], numeral: "I"),
        Card(id: 2, name: "The High Priestess", arcana: .major, element: .water, keywords: ["intuition", "mystery", "inner voice", "unconscious"], numeral: "II"),
        Card(id: 3, name: "The Empress", arcana: .major, element: .earth, keywords: ["abundance", "nurturing", "fertility", "nature"], numeral: "III"),
        Card(id: 4, name: "The Emperor", arcana: .major, element: .fire, keywords: ["authority", "structure", "control", "father figure"], numeral: "IV"),
        Card(id: 5, name: "The Hierophant", arcana: .major, element: .earth, keywords: ["tradition", "conformity", "wisdom", "spiritual guidance"], numeral: "V"),
        Card(id: 6, name: "The Lovers", arcana: .major, element: .air, keywords: ["love", "harmony", "choices", "union"], numeral: "VI"),
        Card(id: 7, name: "The Chariot", arcana: .major, element: .water, keywords: ["willpower", "determination", "victory", "control"], numeral: "VII"),
        Card(id: 8, name: "Strength", arcana: .major, element: .fire, keywords: ["courage", "patience", "inner strength", "compassion"], numeral: "VIII"),
        Card(id: 9, name: "The Hermit", arcana: .major, element: .earth, keywords: ["introspection", "solitude", "guidance", "inner wisdom"], numeral: "IX"),
        Card(id: 10, name: "Wheel of Fortune", arcana: .major, element: .fire, keywords: ["cycles", "fate", "turning point", "destiny"], numeral: "X"),
        Card(id: 11, name: "Justice", arcana: .major, element: .air, keywords: ["fairness", "truth", "karma", "accountability"], numeral: "XI"),
        Card(id: 12, name: "The Hanged Man", arcana: .major, element: .water, keywords: ["surrender", "new perspective", "pause", "letting go"], numeral: "XII"),
        Card(id: 13, name: "Death", arcana: .major, element: .water, keywords: ["transformation", "endings", "change", "transition"], numeral: "XIII"),
        Card(id: 14, name: "Temperance", arcana: .major, element: .fire, keywords: ["balance", "moderation", "patience", "harmony"], numeral: "XIV"),
        Card(id: 15, name: "The Devil", arcana: .major, element: .earth, keywords: ["shadow self", "attachment", "addiction", "bondage"], numeral: "XV"),
        Card(id: 16, name: "The Tower", arcana: .major, element: .fire, keywords: ["upheaval", "revelation", "sudden change", "awakening"], numeral: "XVI"),
        Card(id: 17, name: "The Star", arcana: .major, element: .air, keywords: ["hope", "faith", "renewal", "inspiration"], numeral: "XVII"),
        Card(id: 18, name: "The Moon", arcana: .major, element: .water, keywords: ["illusion", "fear", "subconscious", "intuition"], numeral: "XVIII"),
        Card(id: 19, name: "The Sun", arcana: .major, element: .fire, keywords: ["joy", "success", "vitality", "positivity"], numeral: "XIX"),
        Card(id: 20, name: "Judgement", arcana: .major, element: .fire, keywords: ["rebirth", "inner calling", "reflection", "reckoning"], numeral: "XX"),
        Card(id: 21, name: "The World", arcana: .major, element: .earth, keywords: ["completion", "achievement", "wholeness", "fulfillment"], numeral: "XXI")
    ]

    // MARK: - Minor Arcana

    /// Rank definitions with shared keywords (same meaning across all suits)
    private static let ranks: [(rank: String, keywords: [String])] = [
        ("Ace", ["new beginning", "potential", "opportunity"]),
        ("Two", ["balance", "partnership", "duality"]),
        ("Three", ["growth", "creativity", "collaboration"]),
        ("Four", ["stability", "foundation", "structure"]),
        ("Five", ["conflict", "challenge", "change"]),
        ("Six", ["harmony", "communication", "transition"]),
        ("Seven", ["reflection", "assessment", "perseverance"]),
        ("Eight", ["movement", "speed", "progress"]),
        ("Nine", ["fruition", "attainment", "wisdom"]),
        ("Ten", ["completion", "ending", "fulfillment"]),
        ("Page", ["messenger", "student", "new energy"]),
        ("Knight", ["action", "adventure", "movement"]),
        ("Queen", ["nurturing", "intuitive", "mastery"]),
        ("King", ["authority", "control", "leadership"])
    ]

    /// Generate all 14 cards for a suit
    private static func generateSuit(_ suit: Suit, startingId: Int) -> [Card] {
        ranks.enumerated().map { index, rankInfo in
            Card(
                id: startingId + index,
                name: "\(rankInfo.rank) of \(suit.rawValue)",
                arcana: .minor,
                element: suit.element,
                keywords: rankInfo.keywords,
                suit: suit,
                rank: rankInfo.rank
            )
        }
    }

    static let wands: [Card] = generateSuit(.wands, startingId: 22)
    static let cups: [Card] = generateSuit(.cups, startingId: 36)
    static let swords: [Card] = generateSuit(.swords, startingId: 50)
    static let pentacles: [Card] = generateSuit(.pentacles, startingId: 64)

    // MARK: - Full Deck

    static let minorArcana: [Card] = wands + cups + swords + pentacles

    static let fullDeck: [Card] = majorArcana + minorArcana

    // MARK: - Card Lookup

    /// Find a card by ID
    static func card(withId id: Int) -> Card? {
        fullDeck.first { $0.id == id }
    }

    /// Find a card by name
    static func card(named name: String) -> Card? {
        fullDeck.first { $0.name.lowercased() == name.lowercased() }
    }

    // MARK: - Shuffling

    /// Returns a shuffled copy of the full deck
    static func shuffled() -> [Card] {
        fullDeck.shuffled()
    }

    /// Draw n cards from a shuffled deck
    static func draw(_ count: Int, allowReversed: Bool = true) -> [(card: Card, reversed: Bool)] {
        let shuffled = fullDeck.shuffled()
        return shuffled.prefix(count).map { card in
            let reversed = allowReversed ? Bool.random() : false
            return (card, reversed)
        }
    }
}
