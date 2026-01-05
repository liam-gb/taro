import Foundation
import CoreData

// MARK: - Reading Filter

/// Filter options for fetching readings
enum ReadingFilter {
    case all
    case favorites
    case spreadType(SpreadType)
    case search(String)
}

// MARK: - History Service

/// Singleton service for managing reading history persistence with Core Data
final class HistoryService {
    static let shared = HistoryService()

    // MARK: - Core Data Stack

    private lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "TaroDataModel")
        container.loadPersistentStores { _, error in
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

    private func newBackgroundContext() -> NSManagedObjectContext {
        let context = persistentContainer.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        return context
    }

    private init() {}

    // MARK: - Public API

    /// Save a reading to Core Data
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

    /// Fetch readings with optional filter
    func fetchReadings(filter: ReadingFilter = .all) async throws -> [Reading] {
        try await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            request.sortDescriptors = [NSSortDescriptor(keyPath: \ReadingEntity.createdAt, ascending: false)]

            switch filter {
            case .all:
                break
            case .favorites:
                request.predicate = NSPredicate(format: "isFavorite == YES")
            case .spreadType(let type):
                request.predicate = NSPredicate(format: "spreadType == %@", type.rawValue)
            case .search(let query):
                if !query.isEmpty {
                    request.predicate = NSPredicate(format: "question CONTAINS[cd] %@", query)
                }
            }

            let entities = try self.viewContext.fetch(request)
            return entities.compactMap { self.mapEntityToReading($0) }
        }
    }

    /// Fetch all readings (convenience method)
    func fetchAllReadings() async throws -> [Reading] {
        try await fetchReadings(filter: .all)
    }

    /// Fetch a specific reading by ID
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

    /// Fetch the most recent reading
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

    /// Delete a reading by ID
    func deleteReading(id: UUID) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
            request.fetchLimit = 1

            guard let entity = try context.fetch(request).first else { return }
            context.delete(entity)
            try context.save()
        }
    }

    /// Update notes for a reading
    func updateNotes(id: UUID, notes: String) async throws {
        try await updateReading(id: id) { entity in
            entity.notes = notes.isEmpty ? nil : notes
        }
    }

    /// Toggle the favorite status of a reading
    func toggleFavorite(id: UUID) async throws {
        try await updateReading(id: id) { entity in
            entity.isFavorite.toggle()
        }
    }

    /// Get the count of saved readings
    func readingCount() async -> Int {
        await viewContext.perform {
            let request = ReadingEntity.fetchRequest()
            return (try? self.viewContext.count(for: request)) ?? 0
        }
    }

    // MARK: - Private Helpers

    /// Update a reading entity with a transform closure
    private func updateReading(id: UUID, transform: @escaping (ReadingEntity) -> Void) async throws {
        let context = newBackgroundContext()

        try await context.perform {
            let request = ReadingEntity.fetchRequest()
            request.predicate = NSPredicate(format: "id == %@", id as CVarArg)
            request.fetchLimit = 1

            guard let entity = try context.fetch(request).first else {
                throw HistoryServiceError.readingNotFound
            }

            transform(entity)
            try context.save()
        }
    }

    /// Convert a ReadingEntity to a Reading model
    private func mapEntityToReading(_ entity: ReadingEntity) -> Reading? {
        guard let id = entity.id,
              let spreadTypeString = entity.spreadType,
              let spreadType = SpreadType(rawValue: spreadTypeString),
              let createdAt = entity.createdAt else {
            return nil
        }

        var drawnCardsData: [DrawnCardData] = []
        if let cardsSet = entity.drawnCards {
            for case let cardEntity as DrawnCardEntity in cardsSet {
                if let positionId = cardEntity.positionId {
                    drawnCardsData.append(DrawnCardData(
                        cardId: Int(cardEntity.cardId),
                        positionId: positionId,
                        isReversed: cardEntity.isReversed
                    ))
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

    var errorDescription: String? {
        switch self {
        case .readingNotFound:
            return "Reading not found"
        }
    }
}
