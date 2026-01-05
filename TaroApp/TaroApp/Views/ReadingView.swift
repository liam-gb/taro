import SwiftUI

struct ReadingView: View {
    @EnvironmentObject var readingSession: ReadingSession
    @State private var showShareSheet = false
    @State private var selectedCard: DrawnCard? = nil
    @State private var showCardDetail = false
    @State private var viewMode: ViewMode = .spread
    @State private var headerOpacity: Double = 0
    @State private var layoutAppeared: Bool = false

    enum ViewMode {
        case spread
        case list
    }

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            ScrollView {
                VStack(spacing: TaroSpacing.lg) {
                    // Header
                    headerSection
                        .opacity(headerOpacity)

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // View mode toggle
                    viewModeToggle

                    // Cards display (spread or list view)
                    if viewMode == .spread {
                        spreadLayoutSection
                    } else {
                        listLayoutSection
                    }

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Interpretation
                    interpretationSection

                    GlassDivider()
                        .padding(.horizontal, TaroSpacing.xxl)

                    // Action buttons
                    actionButtonsSection
                }
            }

            // Card detail overlay
            if showCardDetail, let card = selectedCard {
                cardDetailOverlay(for: card)
            }
        }
        .navigationBarHidden(true)
        .onAppear {
            animateEntrance()
        }
    }

    // MARK: - Header Section

    private var headerSection: some View {
        VStack(spacing: TaroSpacing.xs) {
            // Spread name with decorative elements
            HStack(spacing: TaroSpacing.sm) {
                decorativeLine(leading: true)

                Text(readingSession.selectedSpread?.displayName ?? "Your Reading")
                    .font(TaroTypography.mystical(24, weight: .light))
                    .foregroundColor(.textPrimary)
                    .tracking(2)

                decorativeLine(leading: false)
            }

            // Question if provided
            if !readingSession.question.isEmpty {
                Text("\"\(readingSession.question)\"")
                    .font(TaroTypography.mystical(14, weight: .light))
                    .foregroundColor(.textSecondary)
                    .italic()
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, TaroSpacing.xl)
            }

            // Date
            Text(Date(), style: .date)
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
        }
        .padding(.top, TaroSpacing.xl)
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

    // MARK: - View Mode Toggle

    private var viewModeToggle: some View {
        HStack(spacing: TaroSpacing.xs) {
            viewModeButton(mode: .spread, icon: "rectangle.3.group", label: "Spread")
            viewModeButton(mode: .list, icon: "list.bullet", label: "List")
        }
        .padding(TaroSpacing.xxs)
        .background(
            Capsule()
                .fill(Color.white.opacity(0.03))
                .overlay(
                    Capsule()
                        .stroke(Color.white.opacity(0.06), lineWidth: 0.5)
                )
        )
    }

    private func viewModeButton(mode: ViewMode, icon: String, label: String) -> some View {
        Button(action: {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                viewMode = mode
            }
        }) {
            HStack(spacing: TaroSpacing.xxs) {
                Image(systemName: icon)
                    .font(.system(size: 12))
                Text(label)
                    .font(TaroTypography.caption)
            }
            .foregroundColor(viewMode == mode ? .textPrimary : .textMuted)
            .padding(.horizontal, TaroSpacing.md)
            .padding(.vertical, TaroSpacing.xs)
            .background(
                Capsule()
                    .fill(viewMode == mode ? Color.mysticViolet.opacity(0.2) : Color.clear)
            )
        }
        .buttonStyle(.plain)
    }

    // MARK: - Spread Layout Section

    private var spreadLayoutSection: some View {
        GlassPanel(style: .card, cornerRadius: TaroRadius.xl, padding: TaroSpacing.md) {
            VStack(spacing: TaroSpacing.sm) {
                Text("Your Cards")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
                    .textCase(.uppercase)
                    .tracking(1)

                // Determine card size based on spread
                let cardSize = cardSizeForSpread

                GeometryReader { geometry in
                    SpreadLayoutView(
                        spreadType: readingSession.selectedSpread ?? .single,
                        drawnCards: readingSession.drawnCards,
                        cardSize: cardSize,
                        showPositionLabels: true,
                        animateIn: layoutAppeared
                    ) { card in
                        selectCard(card)
                    }
                }
                .frame(height: spreadLayoutHeight)
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    private var cardSizeForSpread: Card3DView.CardSize {
        switch readingSession.selectedSpread {
        case .single, .threeCard, .situation:
            return .standard
        case .celtic, .horseshoe:
            return .small
        case .none:
            return .standard
        }
    }

    private var spreadLayoutHeight: CGFloat {
        switch readingSession.selectedSpread {
        case .single:
            return 200
        case .threeCard, .situation:
            return 220
        case .celtic:
            return 320
        case .horseshoe:
            return 250
        case .none:
            return 200
        }
    }

    // MARK: - List Layout Section

    private var listLayoutSection: some View {
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
                    ForEach(readingSession.drawnCards) { drawnCard in
                        DrawnCardTile(drawnCard: drawnCard)
                            .onTapGesture {
                                selectCard(drawnCard)
                            }
                    }
                }
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
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

                    // Mystical accent
                    Image(systemName: "sparkles")
                        .font(.system(size: 12))
                        .foregroundColor(.mysticViolet.opacity(0.5))
                }

                Text(readingSession.interpretation)
                    .font(TaroTypography.ethereal(16, weight: .regular))
                    .foregroundColor(.textPrimary)
                    .lineSpacing(6)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(.horizontal, TaroSpacing.lg)
    }

    // MARK: - Action Buttons Section

    private var actionButtonsSection: some View {
        VStack(spacing: TaroSpacing.sm) {
            GlassButton("Save Reading", icon: "square.and.arrow.down", style: .secondary) {
                // TODO: Save reading
            }
            .frame(maxWidth: .infinity)

            GlassButton("Copy Text", icon: "doc.on.doc", style: .text) {
                UIPasteboard.general.string = readingSession.interpretation
            }

            GlowingButton("New Reading") {
                readingSession.reset()
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
            // Background
            Color.black.opacity(0.7)
                .ignoresSafeArea()
                .onTapGesture {
                    dismissCardDetail()
                }

            // Card detail content
            VStack(spacing: TaroSpacing.lg) {
                // Large card display
                SpreadCardFront(drawnCard: drawnCard, size: .large)
                    .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))
                    .shadow(color: drawnCard.card.element.color.opacity(0.4), radius: 30)

                // Card info panel
                GlassPanel(style: .summary, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
                    VStack(spacing: TaroSpacing.md) {
                        // Card name and position
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

                        // Card details
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

                        // Keywords
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

                // Close button
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

    // MARK: - Helpers

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

    private func animateEntrance() {
        withAnimation(.easeOut(duration: 0.5)) {
            headerOpacity = 1
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            layoutAppeared = true
        }
    }
}

// MARK: - Drawn Card Tile (List View)

struct DrawnCardTile: View {
    let drawnCard: DrawnCard

    var body: some View {
        VStack(spacing: TaroSpacing.xs) {
            // Card visual
            ActiveGlassPanel(
                isActive: false,
                cornerRadius: TaroRadius.sm,
                padding: 0
            ) {
                ZStack {
                    LinearGradient(
                        colors: [
                            elementColor.opacity(0.3),
                            elementColor.opacity(0.1)
                        ],
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
                    .stroke(elementColor.opacity(0.5), lineWidth: 1)
            )
            .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))

            // Card info
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

    private var elementColor: Color {
        drawnCard.card.element.color
    }

    private var cardInitials: String {
        let words = drawnCard.card.name.split(separator: " ")
        if words.count == 1 {
            return String(words[0].prefix(3))
        }
        return words.map { String($0.prefix(1)) }.joined()
    }
}

// MARK: - Flow Layout (for keywords)

struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = flowLayout(proposal: proposal, subviews: subviews)
        return result.size
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = flowLayout(proposal: proposal, subviews: subviews)

        for (index, frame) in result.frames.enumerated() {
            subviews[index].place(
                at: CGPoint(x: bounds.minX + frame.minX, y: bounds.minY + frame.minY),
                proposal: ProposedViewSize(frame.size)
            )
        }
    }

    private func flowLayout(proposal: ProposedViewSize, subviews: Subviews) -> (size: CGSize, frames: [CGRect]) {
        let maxWidth = proposal.width ?? .infinity

        var currentX: CGFloat = 0
        var currentY: CGFloat = 0
        var lineHeight: CGFloat = 0
        var frames: [CGRect] = []

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)

            if currentX + size.width > maxWidth && currentX > 0 {
                currentX = 0
                currentY += lineHeight + spacing
                lineHeight = 0
            }

            frames.append(CGRect(origin: CGPoint(x: currentX, y: currentY), size: size))
            currentX += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }

        let totalHeight = currentY + lineHeight
        return (CGSize(width: maxWidth, height: totalHeight), frames)
    }
}

// MARK: - Preview

#Preview {
    ReadingView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.threeCard)
            session.question = "Should I change careers?"
            let deck = CardDeck.shuffled()
            let spread = SpreadType.threeCard.spread
            for (index, position) in spread.positions.enumerated() {
                session.drawCard(deck[index], at: position, reversed: Bool.random())
            }
            session.setInterpretation("""
            Your reading reveals a journey of transformation.

            **Past** - The Fool (upright)
            What has shaped this moment. The Fool in this position speaks to beginnings, innocence, spontaneity, leap of faith.

            **Present** - Death (reversed)
            Where you are now. Death in this position speaks to transformation, endings, change, transition.

            **Future** - The Star (upright)
            Where this path leads. The Star in this position speaks to hope, faith, renewal, inspiration.

            Together, these cards weave a story of beginnings leading to hope.

            *This is a placeholder reading. Full LLM integration coming in PR #6.*
            """)
            return session
        }())
        .preferredColorScheme(.dark)
}

#Preview("Celtic Cross") {
    ReadingView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.celtic)
            session.question = "What do I need to know about my current path?"
            let deck = CardDeck.shuffled()
            let spread = SpreadType.celtic.spread
            for (index, position) in spread.positions.enumerated() {
                session.drawCard(deck[index], at: position, reversed: Bool.random())
            }
            session.setInterpretation("""
            The Celtic Cross reveals the layers of your situation...

            Your reading shows a complex interplay of forces. The central cross reveals your core challenge, while the staff illuminates the path forward.

            *Full interpretation coming soon.*
            """)
            return session
        }())
        .preferredColorScheme(.dark)
}

#Preview("Horseshoe") {
    ReadingView()
        .environmentObject({
            let session = ReadingSession()
            session.selectSpread(.horseshoe)
            let deck = CardDeck.shuffled()
            let spread = SpreadType.horseshoe.spread
            for (index, position) in spread.positions.enumerated() {
                session.drawCard(deck[index], at: position, reversed: Bool.random())
            }
            session.setInterpretation("""
            The Horseshoe spread traces the arc of your journey...

            Hidden influences shape your path while obstacles become stepping stones.

            *Full interpretation coming soon.*
            """)
            return session
        }())
        .preferredColorScheme(.dark)
}
