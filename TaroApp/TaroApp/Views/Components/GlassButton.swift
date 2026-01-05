import SwiftUI

// MARK: - Glass Button Styles
enum GlassButtonStyle {
    case primary        // Gradient fill with glow
    case secondary      // Glass outline
    case text           // Text-only with hover underline effect
    case pill           // Pill-shaped selection button
    case icon           // Icon-only circular button
}

// MARK: - Glass Button
struct GlassButton: View {
    let title: String
    let icon: String?
    let style: GlassButtonStyle
    let isLoading: Bool
    let isDisabled: Bool
    let action: () -> Void

    @State private var isPressed = false
    @State private var isHovered = false

    init(
        _ title: String,
        icon: String? = nil,
        style: GlassButtonStyle = .primary,
        isLoading: Bool = false,
        isDisabled: Bool = false,
        action: @escaping () -> Void
    ) {
        self.title = title
        self.icon = icon
        self.style = style
        self.isLoading = isLoading
        self.isDisabled = isDisabled
        self.action = action
    }

    var body: some View {
        Button(action: handleTap) {
            buttonContent
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(isDisabled || isLoading)
        .opacity(isDisabled ? 0.5 : 1)
        .scaleEffect(isPressed ? 0.97 : 1)
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in
                    if !isPressed {
                        isPressed = true
                    }
                }
                .onEnded { _ in
                    isPressed = false
                }
        )
    }

    // MARK: - Button Content
    @ViewBuilder
    private var buttonContent: some View {
        switch style {
        case .primary:
            primaryContent
        case .secondary:
            secondaryContent
        case .text:
            textContent
        case .pill:
            pillContent
        case .icon:
            iconContent
        }
    }

    // MARK: - Primary Style
    private var primaryContent: some View {
        HStack(spacing: TaroSpacing.sm) {
            if isLoading {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .textPrimary))
                    .scaleEffect(0.8)
            } else if let iconName = icon {
                Image(systemName: iconName)
                    .font(.system(size: 16, weight: .medium))
            }

            Text(title)
                .font(TaroTypography.ethereal(16, weight: .semibold))
        }
        .foregroundColor(.textPrimary)
        .padding(.horizontal, TaroSpacing.lg)
        .padding(.vertical, TaroSpacing.md)
        .background(primaryBackground)
        .clipShape(RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous))
        .overlay(primaryBorder)
        .shadow(color: Color.mysticViolet.opacity(isPressed ? 0.3 : 0.2), radius: isPressed ? 20 : 15)
        .shadow(color: Color.black.opacity(0.3), radius: 8, y: 4)
    }

    private var primaryBackground: some View {
        ZStack {
            // Base gradient
            LinearGradient(
                colors: [
                    Color.mysticViolet.opacity(0.15),
                    Color.mysticViolet.opacity(0.05)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            // Hover/Press overlay
            LinearGradient(
                colors: [
                    Color.mysticViolet.opacity(0.2),
                    Color.mysticCyan.opacity(0.1),
                    Color.mysticPink.opacity(0.1)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .opacity(isPressed ? 1 : 0)

            // Glass effect
            Material.ultraThinMaterial
                .opacity(0.3)
        }
    }

    private var primaryBorder: some View {
        RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous)
            .stroke(
                Color.mysticViolet.opacity(isPressed ? 0.5 : 0.3),
                lineWidth: 1
            )
    }

    // MARK: - Secondary Style
    private var secondaryContent: some View {
        HStack(spacing: TaroSpacing.sm) {
            if isLoading {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .textSecondary))
                    .scaleEffect(0.8)
            } else if let iconName = icon {
                Image(systemName: iconName)
                    .font(.system(size: 16, weight: .medium))
            }

            Text(title)
                .font(TaroTypography.ethereal(16, weight: .medium))
        }
        .foregroundColor(isPressed ? .textPrimary : .textSecondary)
        .padding(.horizontal, TaroSpacing.lg)
        .padding(.vertical, TaroSpacing.md)
        .background(secondaryBackground)
        .clipShape(RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous)
                .stroke(
                    Color.white.opacity(isPressed ? 0.2 : 0.1),
                    lineWidth: 1
                )
        )
        .shadow(color: Color.black.opacity(0.2), radius: 8, y: 4)
    }

    private var secondaryBackground: some View {
        ZStack {
            Color.white.opacity(isPressed ? 0.06 : 0.03)
            Material.ultraThinMaterial
                .opacity(0.3)
        }
    }

    // MARK: - Text Style
    private var textContent: some View {
        VStack(spacing: 2) {
            HStack(spacing: TaroSpacing.xs) {
                if let iconName = icon {
                    Image(systemName: iconName)
                        .font(.system(size: 14, weight: .medium))
                }

                Text(title)
                    .font(TaroTypography.ethereal(15, weight: .medium))
            }
            .foregroundColor(isPressed ? .lightViolet : .textMuted)

            // Underline effect
            Rectangle()
                .fill(
                    LinearGradient(
                        colors: [.clear, Color.mysticViolet.opacity(0.5), .clear],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(height: 1)
                .scaleEffect(x: isPressed ? 1 : 0, anchor: .center)
                .animation(TaroAnimation.easeOutQuart, value: isPressed)
        }
        .padding(.horizontal, TaroSpacing.sm)
        .padding(.vertical, TaroSpacing.xs)
    }

    // MARK: - Pill Style
    private var pillContent: some View {
        HStack(spacing: TaroSpacing.sm) {
            if let iconName = icon {
                Image(systemName: iconName)
                    .font(.system(size: 14, weight: .medium))
            }

            Text(title)
                .font(TaroTypography.ethereal(14, weight: .medium))
        }
        .foregroundColor(isPressed ? .textPrimary : .textSecondary)
        .padding(.horizontal, TaroSpacing.md)
        .padding(.vertical, TaroSpacing.sm)
        .background(pillBackground)
        .clipShape(Capsule())
        .overlay(
            Capsule()
                .stroke(
                    Color.white.opacity(isPressed ? 0.15 : 0.08),
                    lineWidth: 1
                )
        )
    }

    private var pillBackground: some View {
        ZStack {
            Color.white.opacity(isPressed ? 0.06 : 0.03)
            Material.ultraThinMaterial
                .opacity(0.3)
        }
    }

    // MARK: - Icon Style
    private var iconContent: some View {
        ZStack {
            if isLoading {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .textPrimary))
                    .scaleEffect(0.8)
            } else if let iconName = icon {
                Image(systemName: iconName)
                    .font(.system(size: 18, weight: .medium))
                    .foregroundColor(isPressed ? .textPrimary : .textSecondary)
            }
        }
        .frame(width: 44, height: 44)
        .background(iconBackground)
        .clipShape(Circle())
        .overlay(
            Circle()
                .stroke(
                    Color.white.opacity(isPressed ? 0.15 : 0.08),
                    lineWidth: 1
                )
        )
        .shadow(color: Color.black.opacity(0.2), radius: 8, y: 4)
    }

    private var iconBackground: some View {
        ZStack {
            Color.white.opacity(isPressed ? 0.06 : 0.03)
            Material.ultraThinMaterial
                .opacity(0.3)
        }
    }

    // MARK: - Actions
    private func handleTap() {
        // Haptic feedback
        let impact = UIImpactFeedbackGenerator(style: hapticStyle)
        impact.impactOccurred()

        action()
    }

    private var hapticStyle: UIImpactFeedbackGenerator.FeedbackStyle {
        switch style {
        case .primary:
            return .medium
        case .secondary, .pill:
            return .light
        case .text, .icon:
            return .soft
        }
    }
}

// MARK: - Glowing Primary Button
// Enhanced primary button with animated glow effect
struct GlowingButton: View {
    let title: String
    let icon: String?
    let isLoading: Bool
    let action: () -> Void

    @State private var isPressed = false
    @State private var glowPhase: CGFloat = 0

    init(
        _ title: String,
        icon: String? = nil,
        isLoading: Bool = false,
        action: @escaping () -> Void
    ) {
        self.title = title
        self.icon = icon
        self.isLoading = isLoading
        self.action = action
    }

    var body: some View {
        Button(action: handleTap) {
            HStack(spacing: TaroSpacing.sm) {
                if isLoading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .textPrimary))
                        .scaleEffect(0.8)
                } else if let iconName = icon {
                    Image(systemName: iconName)
                        .font(.system(size: 16, weight: .medium))
                }

                Text(title)
                    .font(TaroTypography.ethereal(16, weight: .semibold))
            }
            .foregroundColor(.textPrimary)
            .padding(.horizontal, TaroSpacing.xl)
            .padding(.vertical, TaroSpacing.md)
            .background(background)
            .clipShape(RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous))
            .overlay(animatedBorder)
            .shadow(color: glowColor, radius: 20 + (glowPhase * 10))
            .shadow(color: Color.mysticViolet.opacity(0.1), radius: 40)
            .shadow(color: Color.black.opacity(0.3), radius: 8, y: 4)
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(isLoading)
        .scaleEffect(isPressed ? 0.97 : 1)
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .onAppear {
            withAnimation(
                Animation
                    .easeInOut(duration: 2)
                    .repeatForever(autoreverses: true)
            ) {
                glowPhase = 1
            }
        }
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }

    private var background: some View {
        ZStack {
            LinearGradient(
                colors: [
                    Color.mysticViolet.opacity(0.2),
                    Color.deepViolet.opacity(0.15)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            Material.ultraThinMaterial.opacity(0.3)
        }
    }

    private var animatedBorder: some View {
        RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous)
            .stroke(
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.5),
                        Color.mysticCyan.opacity(0.3),
                        Color.mysticPink.opacity(0.3),
                        Color.mysticViolet.opacity(0.5)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                ),
                lineWidth: 1
            )
    }

    private var glowColor: Color {
        Color.mysticViolet.opacity(0.2 + (Double(glowPhase) * 0.1))
    }

    private func handleTap() {
        let impact = UIImpactFeedbackGenerator(style: .medium)
        impact.impactOccurred()
        action()
    }
}

// MARK: - Toggle Pill Button
// Selection pill that can be toggled on/off
struct TogglePillButton: View {
    let title: String
    let icon: String?
    @Binding var isSelected: Bool

    @State private var isPressed = false

    init(
        _ title: String,
        icon: String? = nil,
        isSelected: Binding<Bool>
    ) {
        self.title = title
        self.icon = icon
        self._isSelected = isSelected
    }

    var body: some View {
        Button(action: handleTap) {
            HStack(spacing: TaroSpacing.sm) {
                if let iconName = icon {
                    Image(systemName: iconName)
                        .font(.system(size: 14, weight: .medium))
                }

                Text(title)
                    .font(TaroTypography.ethereal(14, weight: .medium))
            }
            .foregroundColor(isSelected ? .textPrimary : .textSecondary)
            .padding(.horizontal, TaroSpacing.md)
            .padding(.vertical, TaroSpacing.sm)
            .background(background)
            .clipShape(Capsule())
            .overlay(border)
            .shadow(
                color: isSelected ? Color.mysticViolet.opacity(0.15) : Color.black.opacity(0.2),
                radius: isSelected ? 20 : 8,
                y: isSelected ? 4 : 2
            )
        }
        .buttonStyle(PlainButtonStyle())
        .scaleEffect(isPressed ? 0.95 : 1)
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .animation(TaroAnimation.springSmooth, value: isSelected)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }

    private var background: some View {
        ZStack {
            if isSelected {
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.2),
                        Color.mysticViolet.opacity(0.1)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            } else {
                Color.white.opacity(0.03)
            }
            Material.ultraThinMaterial.opacity(isSelected ? 0.4 : 0.3)
        }
    }

    private var border: some View {
        Capsule()
            .stroke(
                isSelected ? Color.mysticViolet.opacity(0.4) : Color.white.opacity(0.08),
                lineWidth: 1
            )
    }

    private func handleTap() {
        let impact = UIImpactFeedbackGenerator(style: .light)
        impact.impactOccurred()
        isSelected.toggle()
    }
}

// MARK: - Icon Button
struct IconButton: View {
    let icon: String
    let size: CGFloat
    let action: () -> Void

    @State private var isPressed = false

    init(
        _ icon: String,
        size: CGFloat = 44,
        action: @escaping () -> Void
    ) {
        self.icon = icon
        self.size = size
        self.action = action
    }

    var body: some View {
        Button(action: handleTap) {
            Image(systemName: icon)
                .font(.system(size: size * 0.4, weight: .medium))
                .foregroundColor(isPressed ? .textPrimary : .textSecondary)
                .frame(width: size, height: size)
                .background(background)
                .clipShape(Circle())
                .overlay(
                    Circle()
                        .stroke(
                            Color.white.opacity(isPressed ? 0.15 : 0.08),
                            lineWidth: 1
                        )
                )
                .shadow(color: Color.black.opacity(0.2), radius: 8, y: 4)
        }
        .buttonStyle(PlainButtonStyle())
        .scaleEffect(isPressed ? 0.95 : 1)
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
    }

    private var background: some View {
        ZStack {
            Color.white.opacity(isPressed ? 0.06 : 0.03)
            Material.ultraThinMaterial.opacity(0.3)
        }
    }

    private func handleTap() {
        let impact = UIImpactFeedbackGenerator(style: .soft)
        impact.impactOccurred()
        action()
    }
}

// MARK: - Preview
#Preview("Glass Buttons") {
    ZStack {
        AuroraBackground()

        ScrollView {
            VStack(spacing: TaroSpacing.xl) {
                // Primary buttons
                VStack(spacing: TaroSpacing.md) {
                    Text("Primary")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    GlassButton("Continue", icon: "arrow.right", style: .primary) {}

                    GlassButton("Loading...", style: .primary, isLoading: true) {}

                    GlowingButton("Begin Reading", icon: "sparkles") {}
                }

                // Secondary buttons
                VStack(spacing: TaroSpacing.md) {
                    Text("Secondary")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    GlassButton("Cancel", icon: "xmark", style: .secondary) {}

                    GlassButton("Learn More", style: .secondary) {}
                }

                // Text buttons
                VStack(spacing: TaroSpacing.md) {
                    Text("Text")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    GlassButton("Skip", style: .text) {}

                    GlassButton("View Details", icon: "chevron.right", style: .text) {}
                }

                // Pills
                VStack(spacing: TaroSpacing.md) {
                    Text("Pills")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    HStack(spacing: TaroSpacing.sm) {
                        GlassButton("Love", icon: "heart", style: .pill) {}
                        GlassButton("Career", icon: "briefcase", style: .pill) {}
                        GlassButton("Health", icon: "heart.circle", style: .pill) {}
                    }
                }

                // Icon buttons
                VStack(spacing: TaroSpacing.md) {
                    Text("Icon Buttons")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    HStack(spacing: TaroSpacing.md) {
                        IconButton("arrow.left") {}
                        IconButton("house") {}
                        IconButton("gearshape") {}
                        IconButton("arrow.right") {}
                    }
                }

                // Toggle pills
                VStack(spacing: TaroSpacing.md) {
                    Text("Toggle Pills")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    TogglePillPreview()
                }
            }
            .padding(TaroSpacing.lg)
        }
    }
    .preferredColorScheme(.dark)
}

// Helper for preview
private struct TogglePillPreview: View {
    @State private var option1 = true
    @State private var option2 = false
    @State private var option3 = false

    var body: some View {
        HStack(spacing: TaroSpacing.sm) {
            TogglePillButton("Past", icon: "clock.arrow.circlepath", isSelected: $option1)
            TogglePillButton("Present", icon: "eye", isSelected: $option2)
            TogglePillButton("Future", icon: "sparkle", isSelected: $option3)
        }
    }
}
