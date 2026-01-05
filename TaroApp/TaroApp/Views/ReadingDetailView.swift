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

    var body: some View {
        ZStack {
            AuroraBackground()

            ScrollView {
                VStack(spacing: TaroSpacing.lg) {
                    headerSection
                        .opacity(headerOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    cardsSection
                        .opacity(contentOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    interpretationSection
                        .opacity(contentOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    notesSection
                        .opacity(contentOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    actionButtonsSection
                        .opacity(contentOpacity)
                }
            }

            if showCardDetail, let card = selectedCard {
                CardDetailOverlay(drawnCard: card) {
                    withAnimation(.easeOut(duration: 0.25)) {
                        showCardDetail = false
                        selectedCard = nil
                    }
                }
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            notesText = reading.notes ?? ""
            animateEntrance()
        }
        .sheet(isPresented: $showShareSheet) {
            ShareSheet(items: [reading.shareableText()])
        }
        .alert("Delete Reading?", isPresented: $showDeleteConfirmation) {
            Button("Cancel", role: .cancel) {}
            Button("Delete", role: .destructive) { deleteReading() }
        } message: {
            Text("This reading will be permanently deleted.")
        }
    }

    // MARK: - Header Section

    private var headerSection: some View {
        VStack(spacing: TaroSpacing.sm) {
            HStack {
                Button(action: { dismiss() }) {
                    Image(systemName: "chevron.left")
                        .font(.system(size: 18, weight: .medium))
                        .foregroundColor(.textSecondary)
                }

                Spacer()

                Button(action: toggleFavorite) {
                    Image(systemName: reading.isFavorite ? "star.fill" : "star")
                        .font(.system(size: 18))
                        .foregroundColor(reading.isFavorite ? .mysticViolet : .textSecondary)
                }
            }
            .padding(.horizontal, TaroSpacing.lg)
            .padding(.top, TaroSpacing.lg)

            HStack(spacing: TaroSpacing.sm) {
                DecorativeLine(leading: true)

                Text(reading.spreadType.displayName)
                    .font(TaroTypography.mystical(24, weight: .light))
                    .foregroundColor(.textPrimary)
                    .tracking(2)

                DecorativeLine(leading: false)
            }

            if let question = reading.question, !question.isEmpty {
                Text("\"\(question)\"")
                    .font(TaroTypography.mystical(14, weight: .light))
                    .foregroundColor(.textSecondary)
                    .italic()
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, TaroSpacing.xl)
            }

            Text(TaroDateFormatters.longDateTime.string(from: reading.createdAt))
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
        }
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
                        DrawnCardTile(drawnCard: drawnCard)
                            .onTapGesture { selectCard(drawnCard) }
                    }
                }
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    private var drawnCards: [DrawnCard] {
        reading.drawnCards.compactMap { cardData -> DrawnCard? in
            guard let card = CardDeck.card(withId: cardData.cardId),
                  let position = reading.spreadType.spread.positions.first(where: { $0.id == cardData.positionId })
            else { return nil }
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
                        if isEditingNotes { saveNotes() }
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
            HStack(spacing: TaroSpacing.sm) {
                GlassButton(
                    showCopiedFeedback ? "Copied!" : "Copy",
                    icon: showCopiedFeedback ? "checkmark" : "doc.on.doc",
                    style: .secondary
                ) { copyReading() }
                .frame(maxWidth: .infinity)

                GlassButton("Share", icon: "square.and.arrow.up", style: .secondary) {
                    showShareSheet = true
                }
                .frame(maxWidth: .infinity)
            }

            GlassButton("Similar Reading", icon: "arrow.triangle.2.circlepath", style: .primary) {
                Haptics.medium()
                dismiss()
            }
            .frame(maxWidth: .infinity)

            GlassButton("Delete Reading", icon: "trash", style: .text) {
                showDeleteConfirmation = true
            }
            .frame(maxWidth: .infinity)
        }
        .padding(.horizontal, TaroSpacing.lg)
        .padding(.bottom, TaroSpacing.xl)
    }

    // MARK: - Actions

    private func selectCard(_ card: DrawnCard) {
        Haptics.light()
        withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
            selectedCard = card
            showCardDetail = true
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
        UIPasteboard.general.string = reading.shareableText()
        Haptics.success()

        withAnimation(.easeInOut(duration: 0.2)) { showCopiedFeedback = true }
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            withAnimation(.easeInOut(duration: 0.2)) { showCopiedFeedback = false }
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

    private func animateEntrance() {
        withAnimation(.easeOut(duration: 0.5)) { headerOpacity = 1 }
        withAnimation(.easeOut(duration: 0.6).delay(0.2)) { contentOpacity = 1 }
    }
}

// MARK: - CardDeck Extension

extension CardDeck {
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
                What has shaped this moment.

                **Present** - Death (reversed)
                Where you are now.

                **Future** - The Star (upright)
                Where this path leads.
                """,
                notes: "This reading really resonated with me."
            )
        )
    }
    .preferredColorScheme(.dark)
}
