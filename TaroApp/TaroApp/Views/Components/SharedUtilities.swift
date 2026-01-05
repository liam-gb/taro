import SwiftUI

// MARK: - Haptics

struct Haptics {
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle) {
        UIImpactFeedbackGenerator(style: style).impactOccurred()
    }

    static func notification(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        UINotificationFeedbackGenerator().notificationOccurred(type)
    }

    static func light() { impact(.light) }
    static func medium() { impact(.medium) }
    static func soft() { impact(.soft) }
    static func success() { notification(.success) }
}

// MARK: - String Extensions

extension String {
    func abbreviatedCardName(forSmallSize: Bool) -> String {
        guard forSmallSize else { return self }
        let words = self.split(separator: " ")
        guard words.count > 2 else { return self }
        return words.prefix(2).joined(separator: " ")
    }
}

// MARK: - Time Formatting

/// Formats seconds into a readable time string
func formatElapsedTime(_ seconds: Double) -> String {
    let mins = Int(seconds) / 60
    let secs = Int(seconds) % 60
    if mins > 0 {
        return String(format: "%d:%02d", mins, secs)
    }
    return String(format: "%.1fs", seconds)
}

// MARK: - Card Animation State

struct CardAnimationState {
    var isVisible: Bool = false
    var isFlipped: Bool = false
    var opacity: Double = 0
    var scale: CGFloat = 0.5
    var offset: CGSize = CGSize(width: 0, height: 50)
    var glowOpacity: Double = 0
    var labelOpacity: Double = 0
}

// MARK: - Date Formatters

/// Shared date formatters to avoid recreating on each use
enum TaroDateFormatters {
    static let mediumDateTime: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter
    }()

    static let longDateTime: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .long
        formatter.timeStyle = .short
        return formatter
    }()
}

// MARK: - Decorative Line

/// Decorative gradient line used in headers
struct DecorativeLine: View {
    let leading: Bool

    var body: some View {
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
}

// MARK: - Card Detail Item

/// Displays a labeled value with color - used in card detail overlays
struct CardDetailItem: View {
    let label: String
    let value: String
    let color: Color

    var body: some View {
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
}

// MARK: - Keyword Pill

/// Displays a keyword in a pill shape
struct KeywordPill: View {
    let keyword: String

    var body: some View {
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

// MARK: - Card Detail Overlay

/// Full-screen overlay showing card details - shared between ReadingView and ReadingDetailView
struct CardDetailOverlay: View {
    let drawnCard: DrawnCard
    let onDismiss: () -> Void

    var body: some View {
        ZStack {
            Color.black.opacity(0.7)
                .ignoresSafeArea()
                .onTapGesture { onDismiss() }

            VStack(spacing: TaroSpacing.lg) {
                SpreadCardFront(drawnCard: drawnCard, size: .large)
                    .rotationEffect(.degrees(drawnCard.isReversed ? 180 : 0))
                    .shadow(color: drawnCard.card.element.color.opacity(0.4), radius: 30)

                cardInfoPanel

                GlassButton("Close", icon: "xmark", style: .text) { onDismiss() }
            }
            .padding(.vertical, TaroSpacing.xl)
        }
        .transition(.opacity)
    }

    private var cardInfoPanel: some View {
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
                    CardDetailItem(
                        label: "Orientation",
                        value: drawnCard.orientationText,
                        color: drawnCard.isReversed ? .mysticPink : .mysticEmerald
                    )
                    CardDetailItem(
                        label: "Arcana",
                        value: drawnCard.card.arcana == .major ? "Major" : "Minor",
                        color: .mysticViolet
                    )
                    CardDetailItem(
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
                                KeywordPill(keyword: keyword)
                            }
                        }
                    }
                }
            }
        }
        .padding(.horizontal, TaroSpacing.lg)
    }
}

// MARK: - Reading Shareable Text

extension Reading {
    /// Generates shareable text for this reading
    func shareableText(using dateFormatter: DateFormatter = TaroDateFormatters.longDateTime) -> String {
        var text = "\(spreadType.displayName) Tarot Reading\n"
        text += "\(dateFormatter.string(from: createdAt))\n\n"

        if let question = question, !question.isEmpty {
            text += "Question: \"\(question)\"\n\n"
        }

        text += "Cards Drawn:\n"
        for cardData in drawnCards {
            if let card = CardDeck.card(withId: cardData.cardId),
               let position = spreadType.spread.positions.first(where: { $0.id == cardData.positionId }) {
                let orientation = cardData.isReversed ? "Reversed" : "Upright"
                text += "- \(position.name): \(card.name) (\(orientation))\n"
            }
        }
        text += "\n"

        if let interpretation = interpretation {
            text += "Interpretation:\n\(interpretation)"
        }

        if let notes = notes, !notes.isEmpty {
            text += "\n\nPersonal Notes:\n\(notes)"
        }

        text += "\n\n---\nGenerated with Taro"
        return text
    }
}
