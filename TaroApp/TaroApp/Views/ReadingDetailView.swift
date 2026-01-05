import SwiftUI

struct ReadingDetailView: View {
    @Environment(\.dismiss) private var dismiss
    @State var reading: Reading
    var onDelete: (() -> Void)?
    var onUpdate: ((Reading) -> Void)?

    @State private var showShareSheet = false
    @State private var showDeleteConfirmation = false
    @State private var showCopiedFeedback = false
    @State private var selectedCard: DrawnCard?
    @State private var showCardDetail = false
    @State private var isEditingNotes = false
    @State private var notesText = ""
    @State private var headerOpacity: Double = 0
    @State private var contentOpacity: Double = 0

    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateStyle = .long
        formatter.timeStyle = .short
        return formatter
    }

    var body: some View {
        ZStack {
            AuroraBackground()

            ScrollView {
                VStack(spacing: TaroSpacing.lg) {
                    // Header
                    headerSection
                        .opacity(headerOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Cards section
                    cardsSection
                        .opacity(contentOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Interpretation section
                    interpretationSection
                        .opacity(contentOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Notes section
                    notesSection
                        .opacity(contentOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Action buttons
                    actionButtonsSection
                        .opacity(contentOpacity)
                }
            }

            // Card detail overlay
            if showCardDetail, let card = selectedCard {
                cardDetailOverlay(for: card)
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            notesText = reading.notes ?? ""
            animateEntrance()
        }
        .sheet(isPresented: $showShareSheet) {
            ShareSheet(items: [shareableReadingText])
        }
        .alert("Delete Reading?", isPresented: $showDeleteConfirmation) {
            Button("Cancel", role: .cancel) {}
            Button("Delete", role: .destructive) {
                deleteReading()
            }
        } message: {
            Text("This reading will be permanently deleted.")
        }
    }

    // MARK: - Header Section

    private var headerSection: some View {
        VStack(spacing: TaroSpacing.sm) {
            // Navigation bar
            HStack {
                Button(action: { dismiss() }) {
                    Image(systemName: "chevron.left")
                        .font(.system(size: 18, weight: .medium))
                        .foregroundColor(.textSecondary)
                }

                Spacer()

                // Favorite button
                Button(action: toggleFavorite) {
                    Image(systemName: reading.isFavorite ? "star.fill" : "star")
                        .font(.system(size: 18))
                        .foregroundColor(reading.isFavorite ? .mysticViolet : .textSecondary)
                }
            }
            .padding(.horizontal, TaroSpacing.lg)
            .padding(.top, TaroSpacing.lg)

            // Spread name with decorative elements
            HStack(spacing: TaroSpacing.sm) {
                decorativeLine(leading: true)

                Text(reading.spreadType.displayName)
                    .font(TaroTypography.mystical(24, weight: .light))
                    .foregroundColor(.textPrimary)
                    .tracking(2)

                decorativeLine(leading: false)
            }

            // Question if provided
            if let question = reading.question, !question.isEmpty {
                Text("\"\(question)\"")
                    .font(TaroTypography.mystical(14, weight: .light))
                    .foregroundColor(.textSecondary)
                    .italic()
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, TaroSpacing.xl)
            }

            // Date
            Text(dateFormatter.string(from: reading.createdAt))
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
        }
    }

    private func decorativeLine(leading: Bool) -> some View {
        Rectangle()
            .fill(
                LinearGradient(
                    colors: leading
                        ? [Color.clear, Color.mysticViolet.opacity(0.3)]
                        : [Color.mysticViolet.opacity(0.3), Color.clear],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .frame(width: 40, height: 1)
    }

    // MARK: - Cards Section

    private var cardsSection: some View {
        GlassPanel(style: .card, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
            VStack(spacing: TaroSpacing.md) {
                Text("Your Cards")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
                    .textCase(.uppercase)
                    .tracking(1)

                LazyVGrid(columns: [
                    GridItem(.adaptive(minimum: 100, maximum: 120))
                ], spacing: TaroSpacing.md) {
                    ForEach(drawnCards) { drawnCard in
                        SavedCardTile(drawnCard: drawnCard)
                            .onTapGesture {
                                selectCard(drawnCard)
                            }
                    }
                }
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    /// Convert DrawnCardData to DrawnCard for display
    private var drawnCards: [DrawnCard] {
        reading.drawnCards.compactMap { cardData -> DrawnCard? in
            guard let card = CardDeck.card(withId: cardData.cardId),
                  let position = reading.spreadType.spread.positions.first(where: { $0.id == cardData.positionId })
            else {
                return nil
            }
            return DrawnCard(card: card, position: position, isReversed: cardData.isReversed)
        }
    }

    // MARK: - Interpretation Section

    private var interpretationSection: some View {
        GlassPanel(style: .summary, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
            VStack(alignment: .leading, spacing: TaroSpacing.md) {
                HStack {
                    Text("Interpretation")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                        .textCase(.uppercase)
                        .tracking(1)

                    Spacer()

                    Image(systemName: "sparkles")
                        .font(.system(size: 12))
                        .foregroundColor(.mysticViolet.opacity(0.5))
                }

                if let interpretation = reading.interpretation {
                    MarkdownTextView(text: interpretation)
                } else {
                    Text("No interpretation available")
                        .font(TaroTypography.ethereal(14))
                        .foregroundColor(.textMuted)
                        .italic()
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    // MARK: - Notes Section

    private var notesSection: some View {
        GlassPanel(style: .standard, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
            VStack(alignment: .leading, spacing: TaroSpacing.md) {
                HStack {
                    Text("Journal Notes")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                        .textCase(.uppercase)
                        .tracking(1)

                    Spacer()

                    Button(action: {
                        if isEditingNotes {
                            saveNotes()
                        }
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                            isEditingNotes.toggle()
                        }
                    }) {
                        Text(isEditingNotes ? "Save" : "Edit")
                            .font(TaroTypography.caption)
                            .foregroundColor(.mysticViolet)
                    }
                }

                if isEditingNotes {
                    TextEditor(text: $notesText)
                        .font(TaroTypography.ethereal(15))
                        .foregroundColor(.textPrimary)
                        .scrollContentBackground(.hidden)
                        .frame(minHeight: 120)
                        .padding(TaroSpacing.sm)
                        .background(
                            RoundedRectangle(cornerRadius: TaroRadius.md)
                                .fill(Color.white.opacity(0.03))
                                .overlay(
                                    RoundedRectangle(cornerRadius: TaroRadius.md)
                                        .stroke(Color.mysticViolet.opacity(0.3), lineWidth: 1)
                                )
                        )
                } else if let notes = reading.notes, !notes.isEmpty {
                    Text(notes)
                        .font(TaroTypography.ethereal(15))
                        .foregroundColor(.textPrimary)
                        .lineSpacing(4)
                } else {
                    Text("Tap Edit to add personal reflections about this reading...")
                        .font(TaroTypography.ethereal(14))
                        .foregroundColor(.textMuted)
                        .italic()
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    // MARK: - Action Buttons Section

    private var actionButtonsSection: some View {
        VStack(spacing: TaroSpacing.sm) {
            // Copy and Share row
            HStack(spacing: TaroSpacing.sm) {
                GlassButton(
                    showCopiedFeedback ? "Copied!" : "Copy",
                    icon: showCopiedFeedback ? "checkmark" : "doc.on.doc",
                    style: .secondary
                ) {
                    copyReading()
                }
                .frame(maxWidth: .infinity)

                GlassButton("Share", icon: "square.and.arrow.up", style: .secondary) {
                    showShareSheet = true
                }
                .frame(maxWidth: .infinity)
            }

            // Similar reading button
            GlassButton("Similar Reading", icon: "arrow.triangle.2.circlepath", style: .primary) {
                startSimilarReading()
            }
            .frame(maxWidth: .infinity)

            // Delete button
            GlassButton("Delete Reading", icon: "trash", style: .text) {
                showDeleteConfirmation = true
            }
            .frame(maxWidth: .infinity)
        }
        .padding(.horizontal, TaroSpacing.lg)
        .padding(.bottom, TaroSpacing.xl)
    }

    // MARK: - Card Detail Overlay

    @ViewBuilder
    private func cardDetailOverlay(for drawnCard: DrawnCard) -> some View {
        ZStack {
            Color.black.opacity(0.7)
                .ignoresSafeArea()
                .onTapGesture {
                    dismissCardDetail()
                }

            VStack(spacing: TaroSpacing.lg) {
                // Large card display
                SpreadCardFront(drawnCard: drawnCard, size: .large)
                    .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))
                    .shadow(color: drawnCard.card.element.color.opacity(0.4), radius: 30)

                // Card info panel
                GlassPanel(style: .summary, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
                    VStack(spacing: TaroSpacing.md) {
                        VStack(spacing: TaroSpacing.xxs) {
                            Text(drawnCard.card.name)
                                .font(TaroTypography.mystical(22, weight: .light))
                                .foregroundColor(.textPrimary)

                            Text(drawnCard.position.name)
                                .font(TaroTypography.caption)
                                .foregroundColor(.textSecondary)
                                .textCase(.uppercase)
                                .tracking(1)
                        }

                        GlassDivider()

                        HStack(spacing: TaroSpacing.lg) {
                            detailItem(
                                label: "Orientation",
                                value: drawnCard.orientationText,
                                color: drawnCard.isReversed ? .mysticPink : .mysticEmerald
                            )

                            detailItem(
                                label: "Arcana",
                                value: drawnCard.card.arcana == .major ? "Major" : "Minor",
                                color: .mysticViolet
                            )

                            detailItem(
                                label: "Element",
                                value: drawnCard.card.element.rawValue.capitalized,
                                color: drawnCard.card.element.color
                            )
                        }

                        if !drawnCard.card.keywords.isEmpty {
                            GlassDivider()

                            VStack(spacing: TaroSpacing.xs) {
                                Text("Keywords")
                                    .font(TaroTypography.caption2)
                                    .foregroundColor(.textMuted)
                                    .textCase(.uppercase)

                                FlowLayout(spacing: TaroSpacing.xs) {
                                    ForEach(drawnCard.card.keywords, id: \.self) { keyword in
                                        Text(keyword)
                                            .font(TaroTypography.caption)
                                            .foregroundColor(.textSecondary)
                                            .padding(.horizontal, TaroSpacing.sm)
                                            .padding(.vertical, TaroSpacing.xxs)
                                            .background(
                                                Capsule()
                                                    .fill(Color.white.opacity(0.05))
                                                    .overlay(
                                                        Capsule()
                                                            .stroke(Color.white.opacity(0.1), lineWidth: 0.5)
                                                    )
                                            )
                                    }
                                }
                            }
                        }
                    }
                }
                .padding(.horizontal, TaroSpacing.lg)

                GlassButton("Close", icon: "xmark", style: .text) {
                    dismissCardDetail()
                }
            }
            .padding(.vertical, TaroSpacing.xl)
        }
        .transition(.opacity)
    }

    private func detailItem(label: String, value: String, color: Color) -> some View {
        VStack(spacing: TaroSpacing.xxxs) {
            Text(label)
                .font(TaroTypography.caption2)
                .foregroundColor(.textMuted)
                .textCase(.uppercase)

            Text(value)
                .font(TaroTypography.ethereal(14, weight: .medium))
                .foregroundColor(color)
        }
    }

    // MARK: - Actions

    private func selectCard(_ card: DrawnCard) {
        Haptics.light()
        withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
            selectedCard = card
            showCardDetail = true
        }
    }

    private func dismissCardDetail() {
        withAnimation(.easeOut(duration: 0.25)) {
            showCardDetail = false
            selectedCard = nil
        }
    }

    private func toggleFavorite() {
        Task {
            do {
                try await HistoryService.shared.toggleFavorite(id: reading.id)
                reading.isFavorite.toggle()
                onUpdate?(reading)
                Haptics.light()
            } catch {
                print("ReadingDetailView: Failed to toggle favorite: \(error)")
            }
        }
    }

    private func saveNotes() {
        Task {
            do {
                try await HistoryService.shared.updateNotes(id: reading.id, notes: notesText)
                reading.notes = notesText.isEmpty ? nil : notesText
                onUpdate?(reading)
                Haptics.success()
            } catch {
                print("ReadingDetailView: Failed to save notes: \(error)")
            }
        }
    }

    private func copyReading() {
        UIPasteboard.general.string = shareableReadingText
        Haptics.success()

        withAnimation(.easeInOut(duration: 0.2)) {
            showCopiedFeedback = true
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            withAnimation(.easeInOut(duration: 0.2)) {
                showCopiedFeedback = false
            }
        }
    }

    private func deleteReading() {
        Task {
            do {
                try await HistoryService.shared.deleteReading(id: reading.id)
                onDelete?()
                Haptics.notification(.success)
                dismiss()
            } catch {
                print("ReadingDetailView: Failed to delete: \(error)")
            }
        }
    }

    private func startSimilarReading() {
        // This would need to be handled by the parent via a callback
        // For now, just dismiss and let user start new reading manually
        Haptics.medium()
        dismiss()
    }

    private var shareableReadingText: String {
        var text = ""

        text += "\(reading.spreadType.displayName) Tarot Reading\n"
        text += "\(dateFormatter.string(from: reading.createdAt))\n\n"

        if let question = reading.question, !question.isEmpty {
            text += "Question: \"\(question)\"\n\n"
        }

        text += "Cards Drawn:\n"
        for cardData in reading.drawnCards {
            if let card = CardDeck.card(withId: cardData.cardId),
               let position = reading.spreadType.spread.positions.first(where: { $0.id == cardData.positionId }) {
                let orientation = cardData.isReversed ? "Reversed" : "Upright"
                text += "- \(position.name): \(card.name) (\(orientation))\n"
            }
        }
        text += "\n"

        if let interpretation = reading.interpretation {
            text += "Interpretation:\n"
            text += interpretation
        }

        if let notes = reading.notes, !notes.isEmpty {
            text += "\n\nPersonal Notes:\n"
            text += notes
        }

        text += "\n\n---\nGenerated with Taro"

        return text
    }

    private func animateEntrance() {
        withAnimation(.easeOut(duration: 0.5)) {
            headerOpacity = 1
        }
        withAnimation(.easeOut(duration: 0.6).delay(0.2)) {
            contentOpacity = 1
        }
    }
}

// MARK: - Saved Card Tile

struct SavedCardTile: View {
    let drawnCard: DrawnCard

    var body: some View {
        let color = drawnCard.card.element.color
        VStack(spacing: TaroSpacing.xs) {
            ActiveGlassPanel(
                isActive: false,
                cornerRadius: TaroRadius.sm,
                padding: 0
            ) {
                ZStack {
                    LinearGradient(
                        colors: [color.opacity(0.3), color.opacity(0.1)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )

                    VStack(spacing: TaroSpacing.xxs) {
                        if let numeral = drawnCard.card.numeral {
                            Text(numeral)
                                .font(TaroTypography.caption)
                                .foregroundColor(.textSecondary)
                        }

                        Text(cardInitials)
                            .font(TaroTypography.mystical(18, weight: .medium))
                            .foregroundColor(.textPrimary)

                        if drawnCard.isReversed {
                            Text("R")
                                .font(TaroTypography.caption2)
                                .fontWeight(.bold)
                                .foregroundColor(.mysticPink)
                        }
                    }
                }
                .frame(width: 70, height: 100)
            }
            .overlay(
                RoundedRectangle(cornerRadius: TaroRadius.sm)
                    .stroke(color.opacity(0.5), lineWidth: 1)
            )
            .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))

            VStack(spacing: TaroSpacing.xxxs) {
                Text(drawnCard.card.name)
                    .font(TaroTypography.ethereal(11, weight: .medium))
                    .foregroundColor(.textPrimary)
                    .lineLimit(2)
                    .multilineTextAlignment(.center)

                Text(drawnCard.position.name)
                    .font(TaroTypography.caption2)
                    .foregroundColor(.textSecondary)

                Text(drawnCard.orientationText)
                    .font(TaroTypography.caption2)
                    .fontWeight(.medium)
                    .foregroundColor(drawnCard.isReversed ? .mysticPink : .mysticEmerald)
            }
        }
    }

    private var cardInitials: String {
        let words = drawnCard.card.name.split(separator: " ")
        return words.count == 1 ? String(words[0].prefix(3)) : words.map { String($0.prefix(1)) }.joined()
    }
}

// MARK: - CardDeck Extension

extension CardDeck {
    /// Get a card by its ID
    static func card(withId id: Int) -> Card? {
        allCards.first { $0.id == id }
    }
}

// MARK: - Preview

#Preview {
    NavigationStack {
        ReadingDetailView(
            reading: Reading(
                spreadType: .threeCard,
                question: "What should I focus on?",
                drawnCards: [
                    DrawnCardData(cardId: 0, positionId: "past", isReversed: false),
                    DrawnCardData(cardId: 13, positionId: "present", isReversed: true),
                    DrawnCardData(cardId: 17, positionId: "future", isReversed: false)
                ],
                interpretation: """
                Your reading reveals a journey of transformation.

                **Past** - The Fool (upright)
                What has shaped this moment. The Fool in this position speaks to beginnings, innocence, spontaneity, leap of faith.

                **Present** - Death (reversed)
                Where you are now. Death in this position speaks to transformation, endings, change, transition.

                **Future** - The Star (upright)
                Where this path leads. The Star in this position speaks to hope, faith, renewal, inspiration.

                Together, these cards weave a story of beginnings leading to hope.
                """,
                notes: "This reading really resonated with me. I need to embrace change."
            )
        )
    }
    .preferredColorScheme(.dark)
}
