import XCTest
@testable import TaroApp

final class DataServiceTests: XCTestCase {

    // MARK: - Base Meanings Tests

    func testBaseMeaningsLoaded() {
        let service = DataService.shared
        XCTAssertTrue(service.isLoaded, "DataService should load successfully")
        XCTAssertNotNil(service.baseMeanings, "Base meanings should be loaded")
    }

    func testMajorArcanaBaseMeanings() {
        let service = DataService.shared

        // Test The Fool
        let foolUpright = service.baseMeaning(for: "The Fool", isReversed: false)
        XCTAssertNotNil(foolUpright, "The Fool upright meaning should exist")
        XCTAssertTrue(foolUpright?.contains("potential") == true, "The Fool should mention potential")

        let foolReversed = service.baseMeaning(for: "The Fool", isReversed: true)
        XCTAssertNotNil(foolReversed, "The Fool reversed meaning should exist")
        XCTAssertTrue(foolReversed?.contains("reckless") == true || foolReversed?.contains("Blocked") == true,
                      "The Fool reversed should mention blockage or recklessness")

        // Test Death
        let deathUpright = service.baseMeaning(for: "Death", isReversed: false)
        XCTAssertNotNil(deathUpright, "Death upright meaning should exist")
        XCTAssertTrue(deathUpright?.contains("Transformation") == true || deathUpright?.contains("ending") == true,
                      "Death should mention transformation")
    }

    // MARK: - Position Modifiers Tests

    func testPositionModifiersLoaded() {
        let service = DataService.shared
        XCTAssertNotNil(service.positionModifiers, "Position modifiers should be loaded")
    }

    func testCardInPositionModifier() {
        let service = DataService.shared

        // Test The Fool in Past position
        let foolPast = service.positionModifier(for: "The Fool", position: "past", isReversed: false)
        XCTAssertNotNil(foolPast, "The Fool in Past position should have a modifier")
        XCTAssertTrue(foolPast?.contains("leap") == true || foolPast?.contains("began") == true || foolPast?.contains("already") == true,
                      "Past position should reference past events")

        // Test The Fool reversed in Present position
        let foolPresentReversed = service.positionModifier(for: "The Fool", position: "present", isReversed: true)
        XCTAssertNotNil(foolPresentReversed, "The Fool reversed in Present position should have a modifier")
    }

    func testAllPositionsHaveModifiers() {
        let service = DataService.shared
        let positions = ["todays_guidance", "past", "present", "future", "situation", "action",
                        "outcome", "challenge", "above", "below", "advice", "external",
                        "hopes_fears", "hidden_influences", "obstacles", "external_influences"]

        for position in positions {
            let modifier = service.positionModifier(for: "The Fool", position: position, isReversed: false)
            XCTAssertNotNil(modifier, "The Fool should have a modifier for \(position) position")
        }
    }

    // MARK: - Combinations Tests

    func testCombinationsLoaded() {
        let service = DataService.shared
        XCTAssertFalse(service.combinations.isEmpty, "Combinations should be loaded")
        XCTAssertGreaterThan(service.combinations.count, 20, "Should have more than 20 combinations")
    }

    func testFindSpecificCombination() {
        let service = DataService.shared

        // Death + Star is a notable combination
        let found = service.findCombinations(in: ["Death", "The Star"])
        XCTAssertFalse(found.isEmpty, "Death + Star combination should be found")

        if let combo = found.first {
            XCTAssertTrue(combo.meaning.lowercased().contains("hope") || combo.meaning.lowercased().contains("renewal"),
                         "Death + Star combination should mention hope or renewal")
        }
    }

    func testFindMultipleCombinations() {
        let service = DataService.shared

        // Test with multiple cards that have known combinations
        let cards = ["The Fool", "The World", "Death", "The Star"]
        let found = service.findCombinations(in: cards)

        // The Fool + The World and Death + Star are both known combinations
        XCTAssertGreaterThanOrEqual(found.count, 2, "Should find at least 2 combinations in these cards")
    }

    func testNoCombinationFound() {
        let service = DataService.shared

        // Test with cards that likely don't have a specific combination
        let found = service.findCombinations(in: ["Two of Wands", "Seven of Pentacles"])
        // This should return empty or a valid result - just ensure no crash
        XCTAssertNotNil(found, "Should return a valid array even if empty")
    }

    // MARK: - Interpretation Tests

    func testCardInterpretation() {
        let service = DataService.shared

        // Create a mock drawn card
        let card = CardDeck.allCards.first { $0.name == "The Fool" }!
        let position = StandardPosition.present.toPosition()
        let drawnCard = DrawnCard(card: card, position: position, isReversed: false)

        let interpretation = service.interpretation(for: drawnCard)

        XCTAssertEqual(interpretation.drawnCard.card.name, "The Fool")
        XCTAssertFalse(interpretation.baseMeaning.isEmpty, "Base meaning should not be empty")
        XCTAssertNotNil(interpretation.positionModifier, "Position modifier should exist")
        XCTAssertFalse(interpretation.fullInterpretation.isEmpty, "Full interpretation should not be empty")
    }

    func testReadingInterpretation() {
        let service = DataService.shared

        // Create a mock 3-card reading
        let fool = CardDeck.allCards.first { $0.name == "The Fool" }!
        let death = CardDeck.allCards.first { $0.name == "Death" }!
        let star = CardDeck.allCards.first { $0.name == "The Star" }!

        let drawnCards = [
            DrawnCard(card: fool, position: StandardPosition.past.toPosition(), isReversed: false),
            DrawnCard(card: death, position: StandardPosition.present.toPosition(), isReversed: false),
            DrawnCard(card: star, position: StandardPosition.future.toPosition(), isReversed: false)
        ]

        let readingInterpretation = service.interpretation(for: drawnCards)

        XCTAssertEqual(readingInterpretation.cardInterpretations.count, 3, "Should have 3 card interpretations")
        XCTAssertFalse(readingInterpretation.combinations.isEmpty, "Should find combinations (Death + Star)")
        XCTAssertEqual(readingInterpretation.elementalFlow.elements.count, 3, "Should have 3 elements in flow")
    }

    // MARK: - Error Handling Tests

    func testMissingCardGracefullyHandled() {
        let service = DataService.shared

        // Test with a non-existent card
        let meaning = service.baseMeaning(for: "Nonexistent Card", isReversed: false)
        XCTAssertNil(meaning, "Should return nil for nonexistent card")

        let modifier = service.positionModifier(for: "Nonexistent Card", position: "present", isReversed: false)
        XCTAssertNil(modifier, "Should return nil for nonexistent card position")
    }

    func testMissingPositionGracefullyHandled() {
        let service = DataService.shared

        // Test with a non-existent position
        let modifier = service.positionModifier(for: "The Fool", position: "nonexistent_position", isReversed: false)
        XCTAssertNil(modifier, "Should return nil for nonexistent position")
    }

    // MARK: - Elemental Flow Tests

    func testElementalFlowGeneration() {
        let fool = CardDeck.allCards.first { $0.name == "The Fool" }!
        let aceOfCups = CardDeck.allCards.first { $0.name == "Ace of Cups" }!

        let drawnCards = [
            DrawnCard(card: fool, position: StandardPosition.past.toPosition(), isReversed: false),
            DrawnCard(card: aceOfCups, position: StandardPosition.present.toPosition(), isReversed: false)
        ]

        let flow = ElementalFlow(from: drawnCards)

        XCTAssertEqual(flow.elements.count, 2, "Should have 2 elements")
        XCTAssertFalse(flow.summary.isEmpty, "Summary should not be empty")
        XCTAssertTrue(flow.summary.contains("→"), "Summary should contain arrow for flow")
    }
}
