import Foundation

// MARK: - Data Service

/// Singleton service for loading and accessing pre-calculated tarot interpretation data
final class DataService {
    static let shared = DataService()

    // MARK: - Loaded Data

    private(set) var baseMeanings: BaseMeanings?
    private(set) var positionModifiers: PositionModifiersData?
    private(set) var combinations: [CardCombination] = []

    // MARK: - Loading State

    private(set) var isLoaded = false
    private(set) var loadError: DataServiceError?

    // MARK: - Initialization

    private init() {
        loadAllData()
    }

    // MARK: - Public API

    /// Reload all data from bundle
    func reload() {
        loadAllData()
    }

    /// Get base meaning for a card
    func baseMeaning(for cardName: String, isReversed: Bool) -> String? {
        guard let meaning = baseMeanings?.meaning(for: cardName) else {
            return nil
        }
        return meaning.meaning(isReversed: isReversed)
    }

    /// Get position modifier for a card in a specific position
    func positionModifier(for cardName: String, position positionId: String, isReversed: Bool) -> String? {
        guard let modifiers = positionModifiers?.modifiers[cardName] else {
            return nil
        }
        return modifiers.modifier(for: positionId, isReversed: isReversed)
    }

    /// Get full interpretation for a drawn card
    func interpretation(for drawnCard: DrawnCard) -> CardInterpretation {
        let baseMeaning = baseMeaning(
            for: drawnCard.card.name,
            isReversed: drawnCard.isReversed
        ) ?? "Meaning not available"

        let positionMod = positionModifier(
            for: drawnCard.card.name,
            position: drawnCard.position.id,
            isReversed: drawnCard.isReversed
        )

        return CardInterpretation(
            drawnCard: drawnCard,
            baseMeaning: baseMeaning,
            positionModifier: positionMod
        )
    }

    /// Get full reading interpretation
    func interpretation(for drawnCards: [DrawnCard]) -> ReadingInterpretation {
        let cardInterpretations = drawnCards.map { interpretation(for: $0) }
        let foundCombinations = ReadingInterpretation.findCombinations(
            in: drawnCards,
            from: combinations
        )
        let elementalFlow = ElementalFlow(from: drawnCards)

        return ReadingInterpretation(
            cardInterpretations: cardInterpretations,
            combinations: foundCombinations,
            elementalFlow: elementalFlow
        )
    }

    /// Find combinations present in a set of cards
    func findCombinations(in cardNames: [String]) -> [CardCombination] {
        var found: [CardCombination] = []

        for i in 0..<cardNames.count {
            for j in (i+1)..<cardNames.count {
                for combo in combinations {
                    if combo.matches(card1: cardNames[i], card2: cardNames[j]) {
                        found.append(combo)
                    }
                }
            }
        }

        return found
    }

    // MARK: - Private Loading

    private func loadAllData() {
        loadError = nil

        do {
            baseMeanings = try loadJSON(filename: "base-meanings")
            positionModifiers = try loadJSON(filename: "position-modifiers")
            let combosData: CombinationsData = try loadJSON(filename: "combinations")
            combinations = combosData.combinations
            isLoaded = true
        } catch let error as DataServiceError {
            loadError = error
            isLoaded = false
            print("DataService: Failed to load data - \(error.localizedDescription)")
        } catch {
            loadError = .unknown(error)
            isLoaded = false
            print("DataService: Unknown error - \(error.localizedDescription)")
        }
    }

    private func loadJSON<T: Decodable>(filename: String) throws -> T {
        guard let url = Bundle.main.url(forResource: filename, withExtension: "json") else {
            throw DataServiceError.fileNotFound(filename)
        }

        let data: Data
        do {
            data = try Data(contentsOf: url)
        } catch {
            throw DataServiceError.readError(filename, error)
        }

        do {
            let decoder = JSONDecoder()
            return try decoder.decode(T.self, from: data)
        } catch {
            throw DataServiceError.parseError(filename, error)
        }
    }
}

// MARK: - Errors

enum DataServiceError: LocalizedError {
    case fileNotFound(String)
    case readError(String, Error)
    case parseError(String, Error)
    case unknown(Error)

    var errorDescription: String? {
        switch self {
        case .fileNotFound(let filename):
            return "Could not find \(filename).json in app bundle"
        case .readError(let filename, let error):
            return "Could not read \(filename).json: \(error.localizedDescription)"
        case .parseError(let filename, let error):
            return "Could not parse \(filename).json: \(error.localizedDescription)"
        case .unknown(let error):
            return "Unknown error: \(error.localizedDescription)"
        }
    }
}

// MARK: - Preview Support

#if DEBUG
extension DataService {
    /// Create a mock service for previews with sample data
    static func preview() -> DataService {
        let service = DataService()
        // Data loads from bundle automatically
        return service
    }
}
#endif
