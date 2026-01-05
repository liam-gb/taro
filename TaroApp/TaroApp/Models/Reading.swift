import Foundation

// MARK: - Reading Model

/// Represents a complete tarot reading session
struct Reading: Identifiable, Codable {
    let id: UUID
    let spreadType: SpreadType
    let question: String?
    let drawnCards: [DrawnCardData]
    let interpretation: String?
    let createdAt: Date

    // User notes/journaling
    var notes: String?

    init(
        id: UUID = UUID(),
        spreadType: SpreadType,
        question: String? = nil,
        drawnCards: [DrawnCardData] = [],
        interpretation: String? = nil,
        createdAt: Date = Date(),
        notes: String? = nil
    ) {
        self.id = id
        self.spreadType = spreadType
        self.question = question
        self.drawnCards = drawnCards
        self.interpretation = interpretation
        self.createdAt = createdAt
        self.notes = notes
    }
}

// MARK: - Drawn Card Data (for persistence)

/// Serializable version of DrawnCard for storage
struct DrawnCardData: Codable, Hashable {
    let cardId: Int
    let positionId: String
    let isReversed: Bool

    init(from drawnCard: DrawnCard) {
        self.cardId = drawnCard.card.id
        self.positionId = drawnCard.position.id
        self.isReversed = drawnCard.isReversed
    }

    init(cardId: Int, positionId: String, isReversed: Bool) {
        self.cardId = cardId
        self.positionId = positionId
        self.isReversed = isReversed
    }
}

// MARK: - Reading State

/// Represents the current state of an in-progress reading
enum ReadingState: Equatable {
    case selectingSpread
    case enteringQuestion
    case shuffling
    case selectingCards
    case generatingInterpretation
    case displayingReading
}

// MARK: - Reading Session

/// Manages an active reading session
@MainActor
class ReadingSession: ObservableObject {
    @Published var state: ReadingState = .selectingSpread
    @Published var selectedSpread: SpreadType?
    @Published var question: String = ""
    @Published var drawnCards: [DrawnCard] = []
    @Published var interpretation: String = ""
    @Published var isGenerating: Bool = false

    // MARK: - Generation Performance Tracking

    /// When generation started
    @Published var generationStartTime: Date?

    /// Number of tokens generated so far
    @Published var tokensGenerated: Int = 0

    /// Time when first token was received
    @Published var firstTokenTime: Date?

    /// First token latency in seconds
    var firstTokenLatency: Double? {
        guard let start = generationStartTime, let first = firstTokenTime else { return nil }
        return first.timeIntervalSince(start)
    }

    /// Generation speed in tokens per second
    var generationSpeed: Double {
        guard let start = generationStartTime, tokensGenerated > 0 else { return 0 }
        let elapsed = Date().timeIntervalSince(start)
        guard elapsed > 0 else { return 0 }
        return Double(tokensGenerated) / elapsed
    }

    /// Total generation time in seconds
    var totalGenerationTime: Double? {
        guard let start = generationStartTime, state == .displayingReading else { return nil }
        return Date().timeIntervalSince(start)
    }

    /// Elapsed time since generation started (for in-progress display)
    var elapsedGenerationTime: Double {
        guard let start = generationStartTime else { return 0 }
        return Date().timeIntervalSince(start)
    }

    var currentSpread: Spread? {
        selectedSpread?.spread
    }

    var isComplete: Bool {
        guard let spread = currentSpread else { return false }
        return drawnCards.count == spread.positions.count
    }

    func selectSpread(_ spread: SpreadType) {
        selectedSpread = spread
        state = .enteringQuestion
    }

    func startReading() {
        state = .shuffling
    }

    func beginCardSelection() {
        state = .selectingCards
    }

    func drawCard(_ card: Card, at position: Position, reversed: Bool) {
        let drawnCard = DrawnCard(card: card, position: position, isReversed: reversed)
        drawnCards.append(drawnCard)

        if isComplete {
            state = .generatingInterpretation
        }
    }

    func setInterpretation(_ text: String) {
        interpretation = text
        isGenerating = false
        state = .displayingReading
    }

    // MARK: - Generation Tracking Methods

    /// Start tracking generation time
    func startGeneration() {
        generationStartTime = Date()
        tokensGenerated = 0
        firstTokenTime = nil
        isGenerating = true
    }

    /// Record a token being generated
    func recordToken() {
        if firstTokenTime == nil {
            firstTokenTime = Date()
        }
        tokensGenerated += 1
    }

    /// Record multiple tokens being generated
    func recordTokens(_ count: Int) {
        if firstTokenTime == nil && count > 0 {
            firstTokenTime = Date()
        }
        tokensGenerated += count
    }

    /// Complete generation tracking
    func completeGeneration() {
        isGenerating = false
    }

    /// Reset generation tracking state
    func resetGenerationTracking() {
        generationStartTime = nil
        tokensGenerated = 0
        firstTokenTime = nil
    }

    func reset() {
        state = .selectingSpread
        selectedSpread = nil
        question = ""
        drawnCards = []
        interpretation = ""
        isGenerating = false
        resetGenerationTracking()
    }

    /// Create a Reading record from the current session
    func toReading() -> Reading {
        Reading(
            spreadType: selectedSpread ?? .single,
            question: question.isEmpty ? nil : question,
            drawnCards: drawnCards.map { DrawnCardData(from: $0) },
            interpretation: interpretation.isEmpty ? nil : interpretation
        )
    }
}

// MARK: - SpreadType Codable

extension SpreadType: Codable {
    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        let rawValue = try container.decode(String.self)
        self = SpreadType(rawValue: rawValue) ?? .single
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encode(rawValue)
    }
}
