import Foundation

// MARK: - Spread Model

/// Represents a tarot spread configuration
struct Spread: Identifiable, Hashable {
    let id: SpreadType
    let name: String
    let positions: [Position]

    var cardCount: Int {
        positions.count
    }
}

// MARK: - Spread Type

enum SpreadType: String, CaseIterable, Identifiable {
    case single
    case threeCard
    case situation
    case celtic
    case horseshoe

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .single: return "Daily Draw"
        case .threeCard: return "Past · Present · Future"
        case .situation: return "Situation · Action · Outcome"
        case .celtic: return "Celtic Cross"
        case .horseshoe: return "Horseshoe"
        }
    }

    var description: String {
        switch self {
        case .single:
            return "A single card for daily guidance"
        case .threeCard:
            return "Explore the timeline of your situation"
        case .situation:
            return "Understand what you face and how to approach it"
        case .celtic:
            return "The classic 10-card spread for deep insight"
        case .horseshoe:
            return "A 7-card spread revealing hidden influences"
        }
    }

    var cardCount: Int {
        switch self {
        case .single: return 1
        case .threeCard: return 3
        case .situation: return 3
        case .celtic: return 10
        case .horseshoe: return 7
        }
    }
}

// MARK: - Spread Configurations

extension Spread {
    /// All available spreads
    static let all: [Spread] = SpreadType.allCases.map { $0.spread }
}

extension SpreadType {
    /// Celtic Cross layout positions (relative grid coordinates)
    private static let celticLayout: [(x: CGFloat, y: CGFloat, rotation: Double)] = [
        (0, 0, 0),           // 1: Present (center)
        (0, 0, 90),          // 2: Challenge (crossing)
        (-1.3, 0, 0),        // 3: Past (left)
        (1.3, 0, 0),         // 4: Future (right)
        (0, -1.5, 0),        // 5: Above (crown)
        (0, 1.5, 0),         // 6: Below (foundation)
        (2.5, 2.25, 0),      // 7: Advice (staff bottom)
        (2.5, 0.75, 0),      // 8: External (staff)
        (2.5, -0.75, 0),     // 9: Hopes/Fears (staff)
        (2.5, -2.25, 0)      // 10: Outcome (staff top)
    ]

    /// Horseshoe layout positions
    private static let horseshoeLayout: [(x: CGFloat, y: CGFloat, rotation: Double)] = [
        (-3, 1, 0),          // 1: Past
        (-2, 0, 0),          // 2: Present
        (-1, -0.5, 0),       // 3: Hidden Influences
        (0, -0.75, 0),       // 4: Obstacles
        (1, -0.5, 0),        // 5: External Influences
        (2, 0, 0),           // 6: Advice
        (3, 1, 0)            // 7: Outcome
    ]

    /// Get the Spread configuration for this type
    var spread: Spread {
        switch self {
        case .single:
            return Spread(
                id: self,
                name: displayName,
                positions: [
                    StandardPosition.todaysGuidance.toPosition()
                ]
            )

        case .threeCard:
            return Spread(
                id: self,
                name: displayName,
                positions: [
                    StandardPosition.past.toPosition(x: -1),
                    StandardPosition.present.toPosition(x: 0),
                    StandardPosition.future.toPosition(x: 1)
                ]
            )

        case .situation:
            return Spread(
                id: self,
                name: displayName,
                positions: [
                    StandardPosition.situation.toPosition(x: -1),
                    StandardPosition.action.toPosition(x: 0),
                    StandardPosition.outcome.toPosition(x: 1)
                ]
            )

        case .celtic:
            let celticPositions: [StandardPosition] = [
                .present, .challenge, .past, .future, .above, .below,
                .advice, .external, .hopesFears, .outcome
            ]
            return Spread(
                id: self,
                name: displayName,
                positions: zip(celticPositions, Self.celticLayout).map { position, layout in
                    position.toPosition(x: layout.x, y: layout.y, rotation: layout.rotation)
                }
            )

        case .horseshoe:
            let horseshoePositions: [StandardPosition] = [
                .past, .present, .hiddenInfluences, .obstacles,
                .externalInfluences, .advice, .outcome
            ]
            return Spread(
                id: self,
                name: displayName,
                positions: zip(horseshoePositions, Self.horseshoeLayout).map { position, layout in
                    position.toPosition(x: layout.x, y: layout.y, rotation: layout.rotation)
                }
            )
        }
    }
}
