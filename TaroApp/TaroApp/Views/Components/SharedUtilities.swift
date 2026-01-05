import SwiftUI

// MARK: - Haptic Feedback Utility
/// Centralized haptic feedback to avoid code duplication

struct Haptics {
    static func impact(_ style: UIImpactFeedbackGenerator.FeedbackStyle) {
        UIImpactFeedbackGenerator(style: style).impactOccurred()
    }

    static func notification(_ type: UINotificationFeedbackGenerator.FeedbackType) {
        UINotificationFeedbackGenerator().notificationOccurred(type)
    }

    static func selection() {
        UISelectionFeedbackGenerator().selectionChanged()
    }

    // Convenience methods
    static func light() { impact(.light) }
    static func medium() { impact(.medium) }
    static func heavy() { impact(.heavy) }
    static func soft() { impact(.soft) }
    static func rigid() { impact(.rigid) }

    static func success() { notification(.success) }
    static func warning() { notification(.warning) }
    static func error() { notification(.error) }
}

// MARK: - Press Gesture Modifier
/// Reusable press detection for button-like interactions

struct PressGestureModifier: ViewModifier {
    @Binding var isPressed: Bool
    var isDisabled: Bool = false
    var onPress: (() -> Void)? = nil

    func body(content: Content) -> some View {
        content
            .gesture(
                DragGesture(minimumDistance: 0)
                    .onChanged { _ in
                        if !isDisabled && !isPressed {
                            isPressed = true
                        }
                    }
                    .onEnded { _ in
                        isPressed = false
                        if !isDisabled {
                            onPress?()
                        }
                    }
            )
    }
}

extension View {
    /// Adds press detection with state binding
    func pressGesture(
        isPressed: Binding<Bool>,
        isDisabled: Bool = false,
        onPress: (() -> Void)? = nil
    ) -> some View {
        modifier(PressGestureModifier(
            isPressed: isPressed,
            isDisabled: isDisabled,
            onPress: onPress
        ))
    }
}

// MARK: - Card Name Abbreviation
/// Shared utility for abbreviating card names on smaller displays

extension String {
    /// Abbreviates a card name to first two words for smaller card sizes
    func abbreviatedCardName(forSmallSize: Bool) -> String {
        if forSmallSize {
            let words = self.split(separator: " ")
            if words.count > 2 {
                return words.prefix(2).joined(separator: " ")
            }
        }
        return self
    }
}

// MARK: - Shared Animation State
/// Common animation state structure for card animations

struct CardAnimationState {
    var isVisible: Bool = false
    var isFlipped: Bool = false
    var opacity: Double = 0
    var scale: CGFloat = 0.5
    var offset: CGSize = CGSize(width: 0, height: 50)
    var rotation: Double = 0
    var zIndex: Double = 0
    var glowOpacity: Double = 0
    var labelOpacity: Double = 0

    /// Creates a visible, non-animated state
    static var visible: CardAnimationState {
        CardAnimationState(
            isVisible: true,
            isFlipped: true,
            opacity: 1,
            scale: 1,
            offset: .zero,
            glowOpacity: 0.3,
            labelOpacity: 1
        )
    }

    /// Creates an initial state for animation entrance
    static func initial(animated: Bool) -> CardAnimationState {
        if animated {
            return CardAnimationState()
        } else {
            return .visible
        }
    }
}

// MARK: - Double Border Modifier
/// Reusable glass-style double border effect

struct DoubleBorderModifier: ViewModifier {
    var cornerRadius: CGFloat
    var primaryOpacity: Double
    var secondaryOpacity: Double
    var lineWidth: CGFloat

    func body(content: Content) -> some View {
        content
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(Color.white.opacity(primaryOpacity), lineWidth: lineWidth)
            )
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(Color.white.opacity(secondaryOpacity), lineWidth: lineWidth)
                    .padding(1)
            )
    }
}

extension View {
    /// Applies a double glass border effect
    func doubleBorder(
        cornerRadius: CGFloat = TaroRadius.md,
        primaryOpacity: Double = 0.1,
        secondaryOpacity: Double = 0.05,
        lineWidth: CGFloat = 0.5
    ) -> some View {
        modifier(DoubleBorderModifier(
            cornerRadius: cornerRadius,
            primaryOpacity: primaryOpacity,
            secondaryOpacity: secondaryOpacity,
            lineWidth: lineWidth
        ))
    }
}

// MARK: - Element Gradient Border
/// Reusable element-colored gradient border for cards

struct ElementGradientBorderModifier: ViewModifier {
    let element: Element
    var cornerRadius: CGFloat = TaroRadius.md
    var lineWidth: CGFloat = 1.5

    func body(content: Content) -> some View {
        content
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(
                        LinearGradient(
                            colors: [
                                element.color.opacity(0.5),
                                element.color.opacity(0.2)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: lineWidth
                    )
            )
    }
}

extension View {
    /// Applies an element-colored gradient border
    func elementGradientBorder(
        for element: Element,
        cornerRadius: CGFloat = TaroRadius.md,
        lineWidth: CGFloat = 1.5
    ) -> some View {
        modifier(ElementGradientBorderModifier(
            element: element,
            cornerRadius: cornerRadius,
            lineWidth: lineWidth
        ))
    }
}

// MARK: - Radial Glow Effect
/// Reusable radial glow for card highlights

struct RadialGlowModifier: ViewModifier {
    let color: Color
    var opacity: Double = 0.2
    var radius: CGFloat = 1.4
    var blurRadius: CGFloat = 10

    func body(content: Content) -> some View {
        content
            .background(
                GeometryReader { geometry in
                    RoundedRectangle(cornerRadius: TaroRadius.md + 4)
                        .fill(
                            RadialGradient(
                                colors: [
                                    color.opacity(opacity),
                                    Color.clear
                                ],
                                center: .center,
                                startRadius: 0,
                                endRadius: geometry.size.width * 0.8
                            )
                        )
                        .frame(
                            width: geometry.size.width * radius,
                            height: geometry.size.height * radius
                        )
                        .blur(radius: blurRadius)
                        .position(
                            x: geometry.size.width / 2,
                            y: geometry.size.height / 2
                        )
                }
            )
    }
}

extension View {
    /// Applies a radial glow effect behind the view
    func radialGlow(
        color: Color,
        opacity: Double = 0.2,
        radius: CGFloat = 1.4,
        blurRadius: CGFloat = 10
    ) -> some View {
        modifier(RadialGlowModifier(
            color: color,
            opacity: opacity,
            radius: radius,
            blurRadius: blurRadius
        ))
    }
}
