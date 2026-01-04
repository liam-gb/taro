import Foundation

// MARK: - Position Model

/// Represents a position within a spread where a card can be placed
struct Position: Identifiable, Codable, Hashable {
    let id: String
    let name: String
    let description: String

    // Layout coordinates for visual placement
    var x: CGFloat = 0
    var y: CGFloat = 0
    var rotation: Double = 0

    enum CodingKeys: String, CodingKey {
        case id, name, description, x, y, rotation
    }

    init(id: String, name: String, description: String, x: CGFloat = 0, y: CGFloat = 0, rotation: Double = 0) {
        self.id = id
        self.name = name
        self.description = description
        self.x = x
        self.y = y
        self.rotation = rotation
    }
}

// MARK: - Position Slug

extension Position {
    /// Slug for looking up position modifiers in pre-calculated data
    var slug: String {
        name.lowercased()
            .replacingOccurrences(of: " ", with: "_")
            .replacingOccurrences(of: "/", with: "_")
            .replacingOccurrences(of: "'", with: "")
    }
}

// MARK: - Standard Positions

/// All unique positions across all spread types
enum StandardPosition: String, CaseIterable {
    // Single card
    case todaysGuidance = "todays_guidance"

    // Three card spread
    case past
    case present
    case future

    // Situation spread
    case situation
    case action
    case outcome

    // Celtic Cross specific
    case challenge
    case above
    case below
    case advice
    case external
    case hopesFears = "hopes_fears"

    // Horseshoe specific
    case hiddenInfluences = "hidden_influences"
    case obstacles
    case externalInfluences = "external_influences"

    var displayName: String {
        switch self {
        case .todaysGuidance: return "Today's Guidance"
        case .past: return "Past"
        case .present: return "Present"
        case .future: return "Future"
        case .situation: return "Situation"
        case .action: return "Action"
        case .outcome: return "Outcome"
        case .challenge: return "Challenge"
        case .above: return "Above"
        case .below: return "Below"
        case .advice: return "Advice"
        case .external: return "External"
        case .hopesFears: return "Hopes/Fears"
        case .hiddenInfluences: return "Hidden Influences"
        case .obstacles: return "Obstacles"
        case .externalInfluences: return "External Influences"
        }
    }

    var description: String {
        switch self {
        case .todaysGuidance: return "Your guidance for today"
        case .past: return "What has shaped this moment"
        case .present: return "Where you are now"
        case .future: return "Where this path leads"
        case .situation: return "The nature of what you face"
        case .action: return "The approach advised"
        case .outcome: return "The likely result"
        case .challenge: return "The obstacle you face"
        case .above: return "Best possible outcome, conscious goals"
        case .below: return "Subconscious influences, hidden foundation"
        case .advice: return "Guidance for moving forward"
        case .external: return "Outside influences affecting you"
        case .hopesFears: return "What you hope for or fear"
        case .hiddenInfluences: return "Factors not immediately apparent"
        case .obstacles: return "Challenges to overcome"
        case .externalInfluences: return "People or events affecting you"
        }
    }

    func toPosition(x: CGFloat = 0, y: CGFloat = 0, rotation: Double = 0) -> Position {
        Position(
            id: self.rawValue,
            name: displayName,
            description: description,
            x: x,
            y: y,
            rotation: rotation
        )
    }
}
