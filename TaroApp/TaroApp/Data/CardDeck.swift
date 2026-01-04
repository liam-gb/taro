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

    // MARK: - Minor Arcana (Wands)

    static let wands: [Card] = [
        Card(id: 22, name: "Ace of Wands", arcana: .minor, element: .fire, keywords: ["new beginning", "potential", "opportunity"], suit: .wands, rank: "Ace"),
        Card(id: 23, name: "Two of Wands", arcana: .minor, element: .fire, keywords: ["balance", "partnership", "duality"], suit: .wands, rank: "Two"),
        Card(id: 24, name: "Three of Wands", arcana: .minor, element: .fire, keywords: ["growth", "creativity", "collaboration"], suit: .wands, rank: "Three"),
        Card(id: 25, name: "Four of Wands", arcana: .minor, element: .fire, keywords: ["stability", "foundation", "structure"], suit: .wands, rank: "Four"),
        Card(id: 26, name: "Five of Wands", arcana: .minor, element: .fire, keywords: ["conflict", "challenge", "change"], suit: .wands, rank: "Five"),
        Card(id: 27, name: "Six of Wands", arcana: .minor, element: .fire, keywords: ["harmony", "communication", "transition"], suit: .wands, rank: "Six"),
        Card(id: 28, name: "Seven of Wands", arcana: .minor, element: .fire, keywords: ["reflection", "assessment", "perseverance"], suit: .wands, rank: "Seven"),
        Card(id: 29, name: "Eight of Wands", arcana: .minor, element: .fire, keywords: ["movement", "speed", "progress"], suit: .wands, rank: "Eight"),
        Card(id: 30, name: "Nine of Wands", arcana: .minor, element: .fire, keywords: ["fruition", "attainment", "wisdom"], suit: .wands, rank: "Nine"),
        Card(id: 31, name: "Ten of Wands", arcana: .minor, element: .fire, keywords: ["completion", "ending", "fulfillment"], suit: .wands, rank: "Ten"),
        Card(id: 32, name: "Page of Wands", arcana: .minor, element: .fire, keywords: ["messenger", "student", "new energy"], suit: .wands, rank: "Page"),
        Card(id: 33, name: "Knight of Wands", arcana: .minor, element: .fire, keywords: ["action", "adventure", "movement"], suit: .wands, rank: "Knight"),
        Card(id: 34, name: "Queen of Wands", arcana: .minor, element: .fire, keywords: ["nurturing", "intuitive", "mastery"], suit: .wands, rank: "Queen"),
        Card(id: 35, name: "King of Wands", arcana: .minor, element: .fire, keywords: ["authority", "control", "leadership"], suit: .wands, rank: "King")
    ]

    // MARK: - Minor Arcana (Cups)

    static let cups: [Card] = [
        Card(id: 36, name: "Ace of Cups", arcana: .minor, element: .water, keywords: ["new beginning", "potential", "opportunity"], suit: .cups, rank: "Ace"),
        Card(id: 37, name: "Two of Cups", arcana: .minor, element: .water, keywords: ["balance", "partnership", "duality"], suit: .cups, rank: "Two"),
        Card(id: 38, name: "Three of Cups", arcana: .minor, element: .water, keywords: ["growth", "creativity", "collaboration"], suit: .cups, rank: "Three"),
        Card(id: 39, name: "Four of Cups", arcana: .minor, element: .water, keywords: ["stability", "foundation", "structure"], suit: .cups, rank: "Four"),
        Card(id: 40, name: "Five of Cups", arcana: .minor, element: .water, keywords: ["conflict", "challenge", "change"], suit: .cups, rank: "Five"),
        Card(id: 41, name: "Six of Cups", arcana: .minor, element: .water, keywords: ["harmony", "communication", "transition"], suit: .cups, rank: "Six"),
        Card(id: 42, name: "Seven of Cups", arcana: .minor, element: .water, keywords: ["reflection", "assessment", "perseverance"], suit: .cups, rank: "Seven"),
        Card(id: 43, name: "Eight of Cups", arcana: .minor, element: .water, keywords: ["movement", "speed", "progress"], suit: .cups, rank: "Eight"),
        Card(id: 44, name: "Nine of Cups", arcana: .minor, element: .water, keywords: ["fruition", "attainment", "wisdom"], suit: .cups, rank: "Nine"),
        Card(id: 45, name: "Ten of Cups", arcana: .minor, element: .water, keywords: ["completion", "ending", "fulfillment"], suit: .cups, rank: "Ten"),
        Card(id: 46, name: "Page of Cups", arcana: .minor, element: .water, keywords: ["messenger", "student", "new energy"], suit: .cups, rank: "Page"),
        Card(id: 47, name: "Knight of Cups", arcana: .minor, element: .water, keywords: ["action", "adventure", "movement"], suit: .cups, rank: "Knight"),
        Card(id: 48, name: "Queen of Cups", arcana: .minor, element: .water, keywords: ["nurturing", "intuitive", "mastery"], suit: .cups, rank: "Queen"),
        Card(id: 49, name: "King of Cups", arcana: .minor, element: .water, keywords: ["authority", "control", "leadership"], suit: .cups, rank: "King")
    ]

    // MARK: - Minor Arcana (Swords)

    static let swords: [Card] = [
        Card(id: 50, name: "Ace of Swords", arcana: .minor, element: .air, keywords: ["new beginning", "potential", "opportunity"], suit: .swords, rank: "Ace"),
        Card(id: 51, name: "Two of Swords", arcana: .minor, element: .air, keywords: ["balance", "partnership", "duality"], suit: .swords, rank: "Two"),
        Card(id: 52, name: "Three of Swords", arcana: .minor, element: .air, keywords: ["growth", "creativity", "collaboration"], suit: .swords, rank: "Three"),
        Card(id: 53, name: "Four of Swords", arcana: .minor, element: .air, keywords: ["stability", "foundation", "structure"], suit: .swords, rank: "Four"),
        Card(id: 54, name: "Five of Swords", arcana: .minor, element: .air, keywords: ["conflict", "challenge", "change"], suit: .swords, rank: "Five"),
        Card(id: 55, name: "Six of Swords", arcana: .minor, element: .air, keywords: ["harmony", "communication", "transition"], suit: .swords, rank: "Six"),
        Card(id: 56, name: "Seven of Swords", arcana: .minor, element: .air, keywords: ["reflection", "assessment", "perseverance"], suit: .swords, rank: "Seven"),
        Card(id: 57, name: "Eight of Swords", arcana: .minor, element: .air, keywords: ["movement", "speed", "progress"], suit: .swords, rank: "Eight"),
        Card(id: 58, name: "Nine of Swords", arcana: .minor, element: .air, keywords: ["fruition", "attainment", "wisdom"], suit: .swords, rank: "Nine"),
        Card(id: 59, name: "Ten of Swords", arcana: .minor, element: .air, keywords: ["completion", "ending", "fulfillment"], suit: .swords, rank: "Ten"),
        Card(id: 60, name: "Page of Swords", arcana: .minor, element: .air, keywords: ["messenger", "student", "new energy"], suit: .swords, rank: "Page"),
        Card(id: 61, name: "Knight of Swords", arcana: .minor, element: .air, keywords: ["action", "adventure", "movement"], suit: .swords, rank: "Knight"),
        Card(id: 62, name: "Queen of Swords", arcana: .minor, element: .air, keywords: ["nurturing", "intuitive", "mastery"], suit: .swords, rank: "Queen"),
        Card(id: 63, name: "King of Swords", arcana: .minor, element: .air, keywords: ["authority", "control", "leadership"], suit: .swords, rank: "King")
    ]

    // MARK: - Minor Arcana (Pentacles)

    static let pentacles: [Card] = [
        Card(id: 64, name: "Ace of Pentacles", arcana: .minor, element: .earth, keywords: ["new beginning", "potential", "opportunity"], suit: .pentacles, rank: "Ace"),
        Card(id: 65, name: "Two of Pentacles", arcana: .minor, element: .earth, keywords: ["balance", "partnership", "duality"], suit: .pentacles, rank: "Two"),
        Card(id: 66, name: "Three of Pentacles", arcana: .minor, element: .earth, keywords: ["growth", "creativity", "collaboration"], suit: .pentacles, rank: "Three"),
        Card(id: 67, name: "Four of Pentacles", arcana: .minor, element: .earth, keywords: ["stability", "foundation", "structure"], suit: .pentacles, rank: "Four"),
        Card(id: 68, name: "Five of Pentacles", arcana: .minor, element: .earth, keywords: ["conflict", "challenge", "change"], suit: .pentacles, rank: "Five"),
        Card(id: 69, name: "Six of Pentacles", arcana: .minor, element: .earth, keywords: ["harmony", "communication", "transition"], suit: .pentacles, rank: "Six"),
        Card(id: 70, name: "Seven of Pentacles", arcana: .minor, element: .earth, keywords: ["reflection", "assessment", "perseverance"], suit: .pentacles, rank: "Seven"),
        Card(id: 71, name: "Eight of Pentacles", arcana: .minor, element: .earth, keywords: ["movement", "speed", "progress"], suit: .pentacles, rank: "Eight"),
        Card(id: 72, name: "Nine of Pentacles", arcana: .minor, element: .earth, keywords: ["fruition", "attainment", "wisdom"], suit: .pentacles, rank: "Nine"),
        Card(id: 73, name: "Ten of Pentacles", arcana: .minor, element: .earth, keywords: ["completion", "ending", "fulfillment"], suit: .pentacles, rank: "Ten"),
        Card(id: 74, name: "Page of Pentacles", arcana: .minor, element: .earth, keywords: ["messenger", "student", "new energy"], suit: .pentacles, rank: "Page"),
        Card(id: 75, name: "Knight of Pentacles", arcana: .minor, element: .earth, keywords: ["action", "adventure", "movement"], suit: .pentacles, rank: "Knight"),
        Card(id: 76, name: "Queen of Pentacles", arcana: .minor, element: .earth, keywords: ["nurturing", "intuitive", "mastery"], suit: .pentacles, rank: "Queen"),
        Card(id: 77, name: "King of Pentacles", arcana: .minor, element: .earth, keywords: ["authority", "control", "leadership"], suit: .pentacles, rank: "King")
    ]

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
