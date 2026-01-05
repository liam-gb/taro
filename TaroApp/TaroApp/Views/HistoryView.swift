import SwiftUI

struct HistoryView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var readings: [Reading] = []
    @State private var isLoading = true
    @State private var searchText = ""
    @State private var selectedFilter: HistoryFilter = .all
    @State private var showingDeleteConfirmation = false
    @State private var readingToDelete: Reading?
    @State private var selectedReading: Reading?
    @State private var showingDetail = false

    enum HistoryFilter: String, CaseIterable {
        case all = "All"
        case favorites = "Favorites"
        case single = "Single"
        case threeCard = "3 Card"
        case celtic = "Celtic"

        var spreadType: SpreadType? {
            switch self {
            case .all, .favorites: return nil
            case .single: return .single
            case .threeCard: return .threeCard
            case .celtic: return .celtic
            }
        }
    }

    var filteredReadings: [Reading] {
        var result = readings

        // Apply filter
        switch selectedFilter {
        case .all:
            break
        case .favorites:
            result = result.filter { $0.isFavorite }
        case .single, .threeCard, .celtic:
            if let spreadType = selectedFilter.spreadType {
                result = result.filter { $0.spreadType == spreadType }
            }
        }

        // Apply search
        if !searchText.isEmpty {
            result = result.filter { reading in
                reading.question?.localizedCaseInsensitiveContains(searchText) == true ||
                reading.spreadType.displayName.localizedCaseInsensitiveContains(searchText)
            }
        }

        return result
    }

    var body: some View {
        ZStack {
            AuroraBackground()

            VStack(spacing: 0) {
                // Header
                headerSection

                // Filter pills
                filterSection
                    .padding(.top, TaroSpacing.sm)

                // Search bar
                searchSection
                    .padding(.top, TaroSpacing.sm)
                    .padding(.horizontal, TaroSpacing.lg)

                // Content
                if isLoading {
                    loadingView
                } else if filteredReadings.isEmpty {
                    emptyStateView
                } else {
                    readingsList
                }
            }
        }
        .navigationBarHidden(true)
        .task {
            await loadReadings()
        }
        .refreshable {
            await loadReadings()
        }
        .sheet(isPresented: $showingDetail) {
            if let reading = selectedReading {
                NavigationStack {
                    ReadingDetailView(reading: reading, onDelete: {
                        Task {
                            await loadReadings()
                        }
                    }, onUpdate: { updatedReading in
                        if let index = readings.firstIndex(where: { $0.id == updatedReading.id }) {
                            readings[index] = updatedReading
                        }
                    })
                }
            }
        }
        .alert("Delete Reading?", isPresented: $showingDeleteConfirmation) {
            Button("Cancel", role: .cancel) {}
            Button("Delete", role: .destructive) {
                if let reading = readingToDelete {
                    Task {
                        await deleteReading(reading)
                    }
                }
            }
        } message: {
            Text("This reading will be permanently deleted.")
        }
    }

    // MARK: - Header

    private var headerSection: some View {
        HStack {
            Button(action: { dismiss() }) {
                Image(systemName: "chevron.left")
                    .font(.system(size: 18, weight: .medium))
                    .foregroundColor(.textSecondary)
            }

            Spacer()

            Text("Reading History")
                .font(TaroTypography.mystical(20, weight: .light))
                .foregroundColor(.textPrimary)

            Spacer()

            // Placeholder for symmetry
            Color.clear
                .frame(width: 24, height: 24)
        }
        .padding(.horizontal, TaroSpacing.lg)
        .padding(.top, TaroSpacing.lg)
    }

    // MARK: - Filter Section

    private var filterSection: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: TaroSpacing.xs) {
                ForEach(HistoryFilter.allCases, id: \.self) { filter in
                    FilterPill(
                        title: filter.rawValue,
                        isSelected: selectedFilter == filter
                    ) {
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                            selectedFilter = filter
                        }
                        Haptics.light()
                    }
                }
            }
            .padding(.horizontal, TaroSpacing.lg)
        }
    }

    // MARK: - Search Section

    private var searchSection: some View {
        HStack(spacing: TaroSpacing.sm) {
            Image(systemName: "magnifyingglass")
                .font(.system(size: 14))
                .foregroundColor(.textMuted)

            TextField("Search readings...", text: $searchText)
                .font(TaroTypography.ethereal(14))
                .foregroundColor(.textPrimary)
                .autocorrectionDisabled()
                .textInputAutocapitalization(.never)

            if !searchText.isEmpty {
                Button(action: { searchText = "" }) {
                    Image(systemName: "xmark.circle.fill")
                        .font(.system(size: 14))
                        .foregroundColor(.textMuted)
                }
            }
        }
        .padding(.horizontal, TaroSpacing.md)
        .padding(.vertical, TaroSpacing.sm)
        .background(
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(Color.white.opacity(0.03))
                .overlay(
                    RoundedRectangle(cornerRadius: TaroRadius.md)
                        .stroke(Color.white.opacity(0.06), lineWidth: 0.5)
                )
        )
    }

    // MARK: - Loading View

    private var loadingView: some View {
        VStack(spacing: TaroSpacing.md) {
            Spacer()
            ProgressView()
                .tint(.mysticViolet)
            Text("Loading readings...")
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
            Spacer()
        }
    }

    // MARK: - Empty State

    private var emptyStateView: some View {
        VStack(spacing: TaroSpacing.lg) {
            Spacer()

            Image(systemName: "clock.arrow.circlepath")
                .font(.system(size: 60, weight: .ultraLight))
                .foregroundColor(.mysticViolet.opacity(0.5))

            VStack(spacing: TaroSpacing.xs) {
                Text(emptyStateTitle)
                    .font(TaroTypography.mystical(20, weight: .light))
                    .foregroundColor(.textPrimary)

                Text(emptyStateMessage)
                    .font(TaroTypography.ethereal(14))
                    .foregroundColor(.textSecondary)
                    .multilineTextAlignment(.center)
            }
            .padding(.horizontal, TaroSpacing.xxl)

            Spacer()
        }
    }

    private var emptyStateTitle: String {
        if !searchText.isEmpty {
            return "No Results"
        } else if selectedFilter == .favorites {
            return "No Favorites"
        } else if selectedFilter != .all {
            return "No \(selectedFilter.rawValue) Readings"
        }
        return "No Readings Yet"
    }

    private var emptyStateMessage: String {
        if !searchText.isEmpty {
            return "Try a different search term"
        } else if selectedFilter == .favorites {
            return "Mark readings as favorites to see them here"
        } else if selectedFilter != .all {
            return "Complete a \(selectedFilter.rawValue.lowercased()) reading to see it here"
        }
        return "Your saved readings will appear here"
    }

    // MARK: - Readings List

    private var readingsList: some View {
        ScrollView {
            LazyVStack(spacing: TaroSpacing.md) {
                ForEach(filteredReadings) { reading in
                    ReadingHistoryCard(reading: reading)
                        .onTapGesture {
                            selectedReading = reading
                            showingDetail = true
                            Haptics.light()
                        }
                        .contextMenu {
                            Button(action: {
                                Task { await toggleFavorite(reading) }
                            }) {
                                Label(
                                    reading.isFavorite ? "Unfavorite" : "Favorite",
                                    systemImage: reading.isFavorite ? "star.slash" : "star"
                                )
                            }

                            Button(role: .destructive, action: {
                                readingToDelete = reading
                                showingDeleteConfirmation = true
                            }) {
                                Label("Delete", systemImage: "trash")
                            }
                        }
                        .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                            Button(role: .destructive) {
                                readingToDelete = reading
                                showingDeleteConfirmation = true
                            } label: {
                                Label("Delete", systemImage: "trash")
                            }
                        }
                        .swipeActions(edge: .leading, allowsFullSwipe: true) {
                            Button {
                                Task { await toggleFavorite(reading) }
                            } label: {
                                Label(
                                    reading.isFavorite ? "Unfavorite" : "Favorite",
                                    systemImage: reading.isFavorite ? "star.slash" : "star.fill"
                                )
                            }
                            .tint(.mysticViolet)
                        }
                }
            }
            .padding(.horizontal, TaroSpacing.lg)
            .padding(.vertical, TaroSpacing.md)
        }
    }

    // MARK: - Actions

    private func loadReadings() async {
        isLoading = true
        do {
            readings = try await HistoryService.shared.fetchAllReadings()
        } catch {
            print("HistoryView: Failed to load readings: \(error)")
        }
        isLoading = false
    }

    private func deleteReading(_ reading: Reading) async {
        do {
            try await HistoryService.shared.deleteReading(id: reading.id)
            readings.removeAll { $0.id == reading.id }
            Haptics.notification(.success)
        } catch {
            print("HistoryView: Failed to delete reading: \(error)")
        }
    }

    private func toggleFavorite(_ reading: Reading) async {
        do {
            try await HistoryService.shared.toggleFavorite(id: reading.id)
            if let index = readings.firstIndex(where: { $0.id == reading.id }) {
                readings[index].isFavorite.toggle()
            }
            Haptics.light()
        } catch {
            print("HistoryView: Failed to toggle favorite: \(error)")
        }
    }
}

// MARK: - Filter Pill

struct FilterPill: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(TaroTypography.ethereal(13, weight: isSelected ? .medium : .regular))
                .foregroundColor(isSelected ? .textPrimary : .textSecondary)
                .padding(.horizontal, TaroSpacing.md)
                .padding(.vertical, TaroSpacing.xs)
                .background(
                    Capsule()
                        .fill(isSelected ? Color.mysticViolet.opacity(0.2) : Color.white.opacity(0.03))
                        .overlay(
                            Capsule()
                                .stroke(
                                    isSelected ? Color.mysticViolet.opacity(0.4) : Color.white.opacity(0.06),
                                    lineWidth: 0.5
                                )
                        )
                )
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Reading History Card

struct ReadingHistoryCard: View {
    let reading: Reading

    var body: some View {
        GlassPanel(style: .card, cornerRadius: TaroRadius.lg, padding: TaroSpacing.md) {
            HStack(spacing: TaroSpacing.md) {
                spreadTypeIcon

                VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                    HStack {
                        Text(reading.spreadType.displayName)
                            .font(TaroTypography.ethereal(15, weight: .medium))
                            .foregroundColor(.textPrimary)

                        if reading.isFavorite {
                            Image(systemName: "star.fill")
                                .font(.system(size: 10))
                                .foregroundColor(.mysticViolet)
                        }

                        Spacer()

                        Text(TaroDateFormatters.mediumDateTime.string(from: reading.createdAt))
                            .font(TaroTypography.caption2)
                            .foregroundColor(.textMuted)
                    }

                    if let question = reading.question, !question.isEmpty {
                        Text(question)
                            .font(TaroTypography.ethereal(13))
                            .foregroundColor(.textSecondary)
                            .lineLimit(2)
                    }

                    // Card count indicator
                    HStack(spacing: TaroSpacing.xxs) {
                        Image(systemName: "rectangle.portrait.on.rectangle.portrait")
                            .font(.system(size: 10))
                        Text("\(reading.drawnCards.count) cards")
                            .font(TaroTypography.caption2)
                    }
                    .foregroundColor(.textMuted)
                }

                // Chevron
                Image(systemName: "chevron.right")
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(.textMuted)
            }
        }
    }

    private var spreadTypeIcon: some View {
        ZStack {
            RoundedRectangle(cornerRadius: TaroRadius.sm)
                .fill(reading.spreadType.color.opacity(0.15))
                .frame(width: 44, height: 44)

            Image(systemName: reading.spreadType.iconName)
                .font(.system(size: 18))
                .foregroundColor(reading.spreadType.color)
        }
    }
}

// MARK: - SpreadType Extensions

extension SpreadType {
    var color: Color {
        switch self {
        case .single: return .mysticCyan
        case .threeCard: return .mysticViolet
        case .situation: return .mysticTeal
        case .celtic: return .mysticPink
        case .horseshoe: return .mysticIndigo
        }
    }

    var iconName: String {
        switch self {
        case .single: return "rectangle.portrait"
        case .threeCard: return "rectangle.split.3x1"
        case .situation: return "arrow.triangle.branch"
        case .celtic: return "plus.rectangle.on.rectangle"
        case .horseshoe: return "circle.hexagongrid"
        }
    }
}

// MARK: - Preview

#Preview {
    NavigationStack {
        HistoryView()
    }
    .preferredColorScheme(.dark)
}
