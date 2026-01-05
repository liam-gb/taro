import SwiftUI

// MARK: - Card3DView
/// A 3D tarot card component with perspective transforms and flip animation
/// Uses SwiftUI 3D transforms to create a realistic card flip effect

struct Card3DView: View {
    let card: Card?
    @Binding var isFlipped: Bool
    var size: CardSize = .standard
    var onTap: (() -> Void)? = nil

    @State private var flipProgress: Double = 0
    @State private var glowOpacity: Double = 0

    // Standard tarot card ratio: approximately 2.5:4.5 (5:9)
    enum CardSize {
        case small      // 60 x 108
        case standard   // 80 x 144
        case large      // 120 x 216
        case shuffle    // 100 x 180

        var width: CGFloat {
            switch self {
            case .small: return 60
            case .standard: return 80
            case .large: return 120
            case .shuffle: return 100
            }
        }

        var height: CGFloat {
            width * 1.8  // Tarot ratio
        }
    }

    var body: some View {
        ZStack {
            // Glow effect during flip
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(TaroGradients.violetGlow)
                .frame(width: size.width * 1.3, height: size.height * 1.3)
                .blur(radius: 20)
                .opacity(glowOpacity)

            // Card container with 3D transform
            ZStack {
                // Back of card (visible when not flipped)
                CardBackDesign(size: size)
                    .opacity(flipProgress < 0.5 ? 1 : 0)

                // Front of card (visible when flipped)
                CardFrontView(card: card, size: size)
                    .rotation3DEffect(
                        .degrees(180),
                        axis: (x: 0, y: 1, z: 0)
                    )
                    .opacity(flipProgress >= 0.5 ? 1 : 0)
            }
            .frame(width: size.width, height: size.height)
            .rotation3DEffect(
                .degrees(flipProgress * 180),
                axis: (x: 0, y: 1, z: 0),
                anchor: .center,
                perspective: 0.5
            )
        }
        .onTapGesture {
            if let onTap = onTap {
                onTap()
            } else {
                flipCard()
            }
        }
        .onChange(of: isFlipped) { _, newValue in
            performFlipAnimation(to: newValue)
        }
    }

    private func flipCard() {
        isFlipped.toggle()
    }

    private func performFlipAnimation(to flipped: Bool) {
        // Add glow during flip
        withAnimation(.easeIn(duration: TaroAnimation.quick)) {
            glowOpacity = 0.8
        }

        // Perform flip
        withAnimation(.easeInOut(duration: TaroAnimation.smooth)) {
            flipProgress = flipped ? 1 : 0
        }

        // Fade glow after flip
        withAnimation(.easeOut(duration: TaroAnimation.standard).delay(TaroAnimation.smooth)) {
            glowOpacity = 0
        }

        // Haptic feedback
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
    }
}

// MARK: - CardFrontView
/// Displays the front face of a tarot card

struct CardFrontView: View {
    let card: Card?
    var size: Card3DView.CardSize = .standard

    var body: some View {
        ZStack {
            // Glass background
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.deepSpaceLight,
                            Color.deepSpace
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            // Glass overlay
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .fill(Material.ultraThinMaterial)
                .opacity(0.3)

            // Card content
            VStack(spacing: TaroSpacing.xxs) {
                if let card = card {
                    // Element indicator
                    elementBadge(for: card.element)

                    Spacer()

                    // Card numeral or rank
                    if let numeral = card.numeral {
                        Text(numeral)
                            .font(TaroTypography.mystical(size == .large ? 32 : 20, weight: .light))
                            .foregroundColor(.textPrimary)
                    } else if let rank = card.rank {
                        Text(rank.prefix(1).uppercased())
                            .font(TaroTypography.mystical(size == .large ? 28 : 18, weight: .light))
                            .foregroundColor(.textPrimary)
                    }

                    // Card name (abbreviated for smaller sizes)
                    Text(abbreviatedName(card.name))
                        .font(TaroTypography.mystical(size == .large ? 14 : 10, weight: .regular))
                        .foregroundColor(.textSecondary)
                        .multilineTextAlignment(.center)
                        .lineLimit(2)
                        .minimumScaleFactor(0.7)

                    Spacer()

                    // Arcana indicator
                    arcanaIndicator(for: card)
                } else {
                    // Placeholder for nil card
                    Image(systemName: "questionmark")
                        .font(.system(size: size == .large ? 40 : 24))
                        .foregroundColor(.textMuted)
                }
            }
            .padding(TaroSpacing.xs)

            // Border
            RoundedRectangle(cornerRadius: TaroRadius.md)
                .stroke(
                    LinearGradient(
                        colors: [
                            elementColor(for: card?.element ?? .fire).opacity(0.5),
                            elementColor(for: card?.element ?? .fire).opacity(0.2)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 1.5
                )
        }
        .frame(width: size.width, height: size.height)
        .shadow(color: Color.black.opacity(0.4), radius: 10, y: 5)
        .shadow(color: elementColor(for: card?.element ?? .fire).opacity(0.3), radius: 15)
    }

    @ViewBuilder
    private func elementBadge(for element: Element) -> some View {
        Circle()
            .fill(elementColor(for: element).opacity(0.3))
            .frame(width: size == .large ? 24 : 16, height: size == .large ? 24 : 16)
            .overlay(
                Circle()
                    .stroke(elementColor(for: element).opacity(0.5), lineWidth: 1)
            )
    }

    @ViewBuilder
    private func arcanaIndicator(for card: Card) -> some View {
        HStack(spacing: 2) {
            ForEach(0..<(card.arcana == .major ? 3 : 1), id: \.self) { _ in
                Circle()
                    .fill(Color.mysticViolet.opacity(0.5))
                    .frame(width: 4, height: 4)
            }
        }
    }

    private func elementColor(for element: Element) -> Color {
        switch element {
        case .fire: return Color(hex: "F97316")    // Orange
        case .water: return Color.mysticCyan
        case .air: return Color.mysticTeal
        case .earth: return Color.mysticEmerald
        }
    }

    private func abbreviatedName(_ name: String) -> String {
        if size == .small || size == .standard {
            let words = name.split(separator: " ")
            if words.count > 2 {
                return words.prefix(2).joined(separator: " ")
            }
        }
        return name
    }
}

// MARK: - FlippableCard
/// Convenience wrapper for Card3DView with state management

struct FlippableCard: View {
    let card: Card?
    var size: Card3DView.CardSize = .standard
    var startFlipped: Bool = false
    var onFlip: ((Bool) -> Void)? = nil

    @State private var isFlipped: Bool = false

    var body: some View {
        Card3DView(
            card: card,
            isFlipped: $isFlipped,
            size: size,
            onTap: {
                isFlipped.toggle()
                onFlip?(isFlipped)
            }
        )
        .onAppear {
            isFlipped = startFlipped
        }
    }
}

// MARK: - SelectableCard
/// Card with selection state and hover effects

struct SelectableCard: View {
    let index: Int
    var isSelected: Bool = false
    var isDisabled: Bool = false
    var size: Card3DView.CardSize = .standard
    var onSelect: (() -> Void)? = nil

    @State private var isPressed: Bool = false
    @State private var glowPulse: Bool = false

    var body: some View {
        ZStack {
            // Selection glow ring
            if isSelected {
                RoundedRectangle(cornerRadius: TaroRadius.md + 4)
                    .stroke(
                        LinearGradient(
                            colors: [
                                Color.mysticViolet,
                                Color.lightViolet,
                                Color.mysticViolet
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 3
                    )
                    .frame(width: size.width + 8, height: size.height + 8)
                    .shadow(color: Color.mysticViolet.opacity(glowPulse ? 0.8 : 0.4), radius: glowPulse ? 20 : 12)
                    .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: glowPulse)
            }

            // Card back
            CardBackDesign(size: size)
                .opacity(isSelected ? 0.5 : (isDisabled ? 0.3 : 1))
                .scaleEffect(isPressed ? 1.05 : (isSelected ? 0.95 : 1))
        }
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .animation(TaroAnimation.springSmooth, value: isSelected)
        .onAppear {
            if isSelected {
                glowPulse = true
            }
        }
        .onChange(of: isSelected) { _, newValue in
            glowPulse = newValue
        }
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in
                    if !isDisabled && !isSelected {
                        isPressed = true
                    }
                }
                .onEnded { _ in
                    isPressed = false
                    if !isDisabled && !isSelected {
                        let generator = UIImpactFeedbackGenerator(style: .light)
                        generator.impactOccurred()
                        onSelect?()
                    }
                }
        )
    }
}

// MARK: - Previews

#Preview("Card3DView - Flip") {
    struct FlipPreview: View {
        @State private var isFlipped = false

        var body: some View {
            ZStack {
                AuroraBackground()

                VStack(spacing: TaroSpacing.xl) {
                    Card3DView(
                        card: Card(
                            id: 0,
                            name: "The Fool",
                            arcana: .major,
                            element: .air,
                            keywords: ["beginnings", "innocence"],
                            numeral: "0"
                        ),
                        isFlipped: $isFlipped,
                        size: .large
                    )

                    GlowingButton(isFlipped ? "Show Back" : "Flip Card", icon: "arrow.triangle.2.circlepath") {
                        isFlipped.toggle()
                    }
                }
            }
        }
    }

    return FlipPreview()
        .preferredColorScheme(.dark)
}

#Preview("Card Sizes") {
    ZStack {
        AuroraBackground()

        HStack(spacing: TaroSpacing.lg) {
            VStack {
                CardBackDesign(size: .small)
                Text("Small")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
            }

            VStack {
                CardBackDesign(size: .standard)
                Text("Standard")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
            }

            VStack {
                CardBackDesign(size: .large)
                Text("Large")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
            }
        }
    }
    .preferredColorScheme(.dark)
}

#Preview("Selectable Cards") {
    struct SelectablePreview: View {
        @State private var selectedIndex: Int? = nil

        var body: some View {
            ZStack {
                AuroraBackground()

                HStack(spacing: -30) {
                    ForEach(0..<5) { index in
                        SelectableCard(
                            index: index,
                            isSelected: selectedIndex == index,
                            size: .standard
                        ) {
                            selectedIndex = index
                        }
                        .zIndex(selectedIndex == index ? 10 : Double(5 - index))
                    }
                }
            }
        }
    }

    return SelectablePreview()
        .preferredColorScheme(.dark)
}
