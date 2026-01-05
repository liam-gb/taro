import Foundation
import CoreData

// MARK: - History Service

/// Singleton service for managing reading history persistence with Core Data
final class HistoryService {
    static let shared = HistoryService()

    // MARK: - Core Data Stack

    private lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "TaroDataModel")
        container.loadPersistentStores { description, error in
            if let error = error {
                print("HistoryService: Failed to load Core Data: \(error.localizedDescription)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        return container
    }()

    private var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }

    /// Creates a background context for save operations
    private func newBackgroundContext() -> NSManagedObjectContext {
        let context = persistentContainer.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        return context
    }

    // MARK: - Initialization

    private init() {}

    // MARK: - Public API

    /// Save a reading to Core Data
    /// - Parameter reading: The reading to save
    /// - Throws: Core Data save error
    func saveReading(_ reading: Reading) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let entity = ReadingEntity(context: context)
            entity.id = reading.id
            entity.spreadType = reading.spreadType.rawValue
            entity.question = reading.question
            entity.interpretation = reading.interpretation
            entity.createdAt = reading.createdAt
            entity.notes = reading.notes
            entity.isFavorite = reading.isFavorite

            // Create drawn card entities
            for cardData in reading.drawnCards {
                let cardEntity = DrawnCardEntity(context: context)
                cardEntity.cardId = Int32(cardData.cardId)
                cardEntity.positionId = cardData.positionId
                cardEntity.isReversed = cardData.isReversed
                cardEntity.reading = entity
            }

            try context.save()
        }
    }

    /// Fetch all readings sorted by date (newest first)
    /// - Returns: Array of Reading models
    /// - Throws: Core Data fetch error
    func fetchAllReadings() async throws -> [Reading] {
        try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.sortDescriptors = [NSSortDescriptor(keyPath: \ReadingEntity.createdAt, ascending: false)]

            let entities = try self.viewContext.fetch(request)
            return entities.compactMap { self.mapEntityToReading($0) }
        }
    }

    /// Fetch a specific reading by ID
    /// - Parameter id: The reading's UUID
    /// - Returns: The Reading if found, nil otherwise
    /// - Throws: Core Data fetch error
    func fetchReading(id: UUID) async throws -> Reading? {
        try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
            request.fetchLimit = 1

            guard let entity = try self.viewContext.fetch(request).first else {
                return nil
            }
            return self.mapEntityToReading(entity)
        }
    }

    /// Delete a reading by ID
    /// - Parameter id: The reading's UUID
    /// - Throws: Core Data error
    func deleteReading(id: UUID) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
            request.fetchLimit = 1

            guard let entity = try context.fetch(request).first else {
                return
            }

            context.delete(entity)
            try context.save()
        }
    }

    /// Update notes for a reading
    /// - Parameters:
    ///   - id: The reading's UUID
    ///   - notes: The new notes text
    /// - Throws: Core Data error
    func updateNotes(id: UUID, notes: String) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
            request.fetchLimit = 1

            guard let entity = try context.fetch(request).first else {
                throw HistoryServiceError.readingNotFound
            }

            entity.notes = notes.isEmpty ? nil : notes
            try context.save()
        }
    }

    /// Toggle the favorite status of a reading
    /// - Parameter id: The reading's UUID
    /// - Throws: Core Data error
    func toggleFavorite(id: UUID) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
            request.fetchLimit = 1

            guard let entity = try context.fetch(request).first else {
                throw HistoryServiceError.readingNotFound
            }

            entity.isFavorite.toggle()
            try context.save()
        }
    }

    /// Get the count of saved readings
    /// - Returns: The number of saved readings
    func readingCount() async -> Int {
        await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            return (try? self.viewContext.count(for: request)) ?? 0
        }
    }

    /// Fetch the most recent reading
    /// - Returns: The most recent Reading if any exist
    func fetchMostRecentReading() async throws -> Reading? {
        try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.sortDescriptors = [NSSortDescriptor(keyPath: \ReadingEntity.createdAt, ascending: false)]
            request.fetchLimit = 1

            guard let entity = try self.viewContext.fetch(request).first else {
                return nil
            }
            return self.mapEntityToReading(entity)
        }
    }

    /// Fetch readings filtered by spread type
    /// - Parameter spreadType: The spread type to filter by
    /// - Returns: Array of matching readings
    func fetchReadings(spreadType: SpreadType) async throws -> [Reading] {
        try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "spreadType == %@", spreadType.rawValue)
            request.sortDescriptors = [NSSortDescriptor(keyPath: \ReadingEntity.createdAt, ascending: false)]

            let entities = try self.viewContext.fetch(request)
            return entities.compactMap { self.mapEntityToReading($0) }
        }
    }

    /// Fetch only favorite readings
    /// - Returns: Array of favorite readings
    func fetchFavoriteReadings() async throws -> [Reading] {
        try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "isFavorite == YES")
            request.sortDescriptors = [NSSortDescriptor(keyPath: \ReadingEntity.createdAt, ascending: false)]

            let entities = try self.viewContext.fetch(request)
            return entities.compactMap { self.mapEntityToReading($0) }
        }
    }

    /// Search readings by question text
    /// - Parameter searchText: The text to search for
    /// - Returns: Array of matching readings
    func searchReadings(query: String) async throws -> [Reading] {
        guard !query.isEmpty else {
            return try await fetchAllReadings()
        }

        return try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "question CONTAINS[cd] %@", query)
            request.sortDescriptors = [NSSortDescriptor(keyPath: \ReadingEntity.createdAt, ascending: false)]

            let entities = try self.viewContext.fetch(request)
            return entities.compactMap { self.mapEntityToReading($0) }
        }
    }

    // MARK: - Private Helpers

    /// Convert a ReadingEntity to a Reading model
    private func mapEntityToReading(_ entity: ReadingEntity) -> Reading? {
        guard let id = entity.id,
              let spreadTypeString = entity.spreadType,
              let spreadType = SpreadType(rawValue: spreadTypeString),
              let createdAt = entity.createdAt else {
            return nil
        }

        // Map drawn cards from the ordered set
        var drawnCardsData: [DrawnCardData] = []
        if let cardsSet = entity.drawnCards {
            for case let cardEntity as DrawnCardEntity in cardsSet {
                if let positionId = cardEntity.positionId {
                    let cardData = DrawnCardData(
                        cardId: Int(cardEntity.cardId),
                        positionId: positionId,
                        isReversed: cardEntity.isReversed
                    )
                    drawnCardsData.append(cardData)
                }
            }
        }

        return Reading(
            id: id,
            spreadType: spreadType,
            question: entity.question,
            drawnCards: drawnCardsData,
            interpretation: entity.interpretation,
            createdAt: createdAt,
            notes: entity.notes,
            isFavorite: entity.isFavorite
        )
    }
}

// MARK: - Errors

enum HistoryServiceError: LocalizedError {
    case readingNotFound
    case saveFailed(Error)

    var errorDescription: String? {
        switch self {
        case .readingNotFound:
            return "Reading not found"
        case .saveFailed(let error):
            return "Failed to save: \(error.localizedDescription)"
        }
    }
}
