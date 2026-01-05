import SwiftUI

// MARK: - QuestionInputModal
/// A mystical glass modal for entering questions before a tarot reading
/// Features ethereal animations and optional skip functionality

struct QuestionInputModal: View {
    @Binding var isPresented: Bool
    @Binding var question: String
    let spreadType: SpreadType
    var onContinue: () -> Void
    var onSkip: (() -> Void)? = nil

    @State private var modalScale: CGFloat = 0.85
    @State private var modalOpacity: Double = 0
    @State private var backgroundOpacity: Double = 0
    @State private var contentOffset: CGFloat = 20
    @State private var orbsAnimating: Bool = false
    @State private var shimmerPhase: CGFloat = 0
    @State private var animationTask: Task<Void, Never>?
    @State private var dismissTask: Task<Void, Never>?
    @FocusState private var isTextFieldFocused: Bool

    var body: some View {
        ZStack {
            // Dimmed background with tap to dismiss
            Color.black
                .opacity(backgroundOpacity * 0.7)
                .ignoresSafeArea()
                .onTapGesture {
                    dismissKeyboard()
                }

            // Floating mystical orbs in background
            floatingOrbs

            // Modal content
            VStack(spacing: 0) {
                Spacer()

                modalContent
                    .scaleEffect(modalScale)
                    .opacity(modalOpacity)
                    .offset(y: contentOffset)

                Spacer()
            }
            .padding(.horizontal, TaroSpacing.lg)
        }
        .onAppear {
            animateIn()
        }
    }

    // MARK: - Modal Content

    private var modalContent: some View {
        VStack(spacing: TaroSpacing.lg) {
            // Header
            headerSection

            GlassDivider()
                .padding(.horizontal, TaroSpacing.md)

            // Question input
            questionInputSection

            // Spread preview
            spreadPreviewSection

            GlassDivider()
                .padding(.horizontal, TaroSpacing.md)

            // Actions
            actionButtons
        }
        .padding(TaroSpacing.lg)
        .background(modalBackground)
        .clipShape(RoundedRectangle(cornerRadius: TaroRadius.xxl, style: .continuous))
        .overlay(modalBorder)
        .shadow(color: Color.mysticViolet.opacity(0.2), radius: 40, y: 10)
        .shadow(color: Color.black.opacity(0.5), radius: 30, y: 20)
    }

    // MARK: - Header Section

    private var headerSection: some View {
        VStack(spacing: TaroSpacing.xs) {
            // Decorative symbol
            ZStack {
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color.mysticViolet.opacity(0.3),
                                Color.clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: 30
                        )
                    )
                    .frame(width: 60, height: 60)
                    .blur(radius: 10)

                Image(systemName: "sparkles")
                    .font(.system(size: 28, weight: .light))
                    .foregroundColor(.mysticViolet)
            }

            Text("Focus Your Intent")
                .font(TaroTypography.mystical(22, weight: .light))
                .foregroundColor(.textPrimary)
                .tracking(2)

            Text("What wisdom do you seek?")
                .font(TaroTypography.ethereal(14, weight: .regular))
                .foregroundColor(.textSecondary)
        }
        .padding(.top, TaroSpacing.sm)
    }

    // MARK: - Question Input Section

    private var questionInputSection: some View {
        VStack(alignment: .leading, spacing: TaroSpacing.sm) {
            // Text field container
            ZStack(alignment: .topLeading) {
                // Placeholder
                if question.isEmpty {
                    Text("Enter your question here, or leave blank for general guidance...")
                        .font(TaroTypography.ethereal(15, weight: .regular))
                        .foregroundColor(.textMuted)
                        .padding(.horizontal, TaroSpacing.md)
                        .padding(.vertical, TaroSpacing.md)
                        .allowsHitTesting(false)
                }

                // Text editor
                TextEditor(text: $question)
                    .font(TaroTypography.ethereal(15, weight: .regular))
                    .foregroundColor(.textPrimary)
                    .scrollContentBackground(.hidden)
                    .padding(.horizontal, TaroSpacing.sm)
                    .padding(.vertical, TaroSpacing.xs)
                    .focused($isTextFieldFocused)
            }
            .frame(minHeight: 100, maxHeight: 140)
            .background(textFieldBackground)
            .clipShape(RoundedRectangle(cornerRadius: TaroRadius.lg, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: TaroRadius.lg, style: .continuous)
                    .stroke(
                        isTextFieldFocused
                            ? Color.mysticViolet.opacity(0.5)
                            : Color.white.opacity(0.1),
                        lineWidth: 1
                    )
                    .animation(.easeInOut(duration: 0.2), value: isTextFieldFocused)
            )

            // Character hint
            HStack {
                Image(systemName: "lightbulb.min")
                    .font(.system(size: 11))
                Text("Tip: Be specific about your situation for deeper insight")
                    .font(TaroTypography.caption2)
            }
            .foregroundColor(.textMuted)
        }
    }

    private var textFieldBackground: some View {
        ZStack {
            Color.black.opacity(0.3)
            Material.ultraThinMaterial.opacity(0.3)

            // Subtle gradient accent
            LinearGradient(
                colors: [
                    Color.mysticViolet.opacity(isTextFieldFocused ? 0.08 : 0.03),
                    Color.clear
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        }
    }

    // MARK: - Spread Preview Section

    private var spreadPreviewSection: some View {
        VStack(spacing: TaroSpacing.sm) {
            Text("Your Spread")
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
                .textCase(.uppercase)
                .tracking(1)

            HStack(spacing: TaroSpacing.md) {
                SpreadPreview(
                    spreadType: spreadType,
                    size: CGSize(width: 80, height: 60),
                    isAnimated: false
                )

                VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                    Text(spreadType.displayName)
                        .font(TaroTypography.ethereal(14, weight: .medium))
                        .foregroundColor(.textPrimary)

                    Text("\(spreadType.cardCount) cards")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textSecondary)
                }

                Spacer()
            }
            .padding(TaroSpacing.md)
            .background(
                RoundedRectangle(cornerRadius: TaroRadius.md)
                    .fill(Color.white.opacity(0.03))
                    .overlay(
                        RoundedRectangle(cornerRadius: TaroRadius.md)
                            .stroke(Color.white.opacity(0.06), lineWidth: 0.5)
                    )
            )
        }
    }

    // MARK: - Action Buttons

    private var actionButtons: some View {
        VStack(spacing: TaroSpacing.sm) {
            // Continue button
            GlowingButton(
                question.isEmpty ? "Begin Reading" : "Ask the Cards",
                icon: "sparkles"
            ) {
                dismissKeyboard()
                animateOut {
                    onContinue()
                }
            }
            .frame(maxWidth: .infinity)

            // Skip option
            if onSkip != nil {
                Button(action: {
                    dismissKeyboard()
                    animateOut {
                        onSkip?()
                    }
                }) {
                    Text("Skip for now")
                        .font(TaroTypography.ethereal(14, weight: .regular))
                        .foregroundColor(.textMuted)
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.bottom, TaroSpacing.xs)
    }

    // MARK: - Floating Orbs

    private var floatingOrbs: some View {
        GeometryReader { geometry in
            ZStack {
                // Top-left orb
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color.mysticViolet.opacity(0.25),
                                Color.clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: 100
                        )
                    )
                    .frame(width: 200, height: 200)
                    .blur(radius: 40)
                    .offset(
                        x: orbsAnimating ? -20 : 20,
                        y: orbsAnimating ? 10 : -10
                    )
                    .position(x: geometry.size.width * 0.2, y: geometry.size.height * 0.2)

                // Bottom-right orb
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color.mysticCyan.opacity(0.2),
                                Color.clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: 80
                        )
                    )
                    .frame(width: 160, height: 160)
                    .blur(radius: 30)
                    .offset(
                        x: orbsAnimating ? 15 : -15,
                        y: orbsAnimating ? -20 : 20
                    )
                    .position(x: geometry.size.width * 0.8, y: geometry.size.height * 0.7)

                // Center accent
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color.mysticPink.opacity(0.15),
                                Color.clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: 60
                        )
                    )
                    .frame(width: 120, height: 120)
                    .blur(radius: 25)
                    .offset(
                        x: orbsAnimating ? -10 : 10,
                        y: orbsAnimating ? 15 : -15
                    )
                    .position(x: geometry.size.width * 0.6, y: geometry.size.height * 0.4)
            }
            .opacity(modalOpacity)
            .animation(
                .easeInOut(duration: 4).repeatForever(autoreverses: true),
                value: orbsAnimating
            )
        }
    }

    // MARK: - Background & Border

    private var modalBackground: some View {
        ZStack {
            // Deep base
            Color.deepSpace.opacity(0.95)

            // Gradient overlay
            LinearGradient(
                colors: [
                    Color.mysticViolet.opacity(0.08),
                    Color.deepViolet.opacity(0.05),
                    Color.clear
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            // Glass material
            Material.ultraThinMaterial
                .opacity(0.4)

            // Shimmer effect
            shimmerOverlay
        }
    }

    private var shimmerOverlay: some View {
        GeometryReader { geometry in
            LinearGradient(
                colors: [
                    Color.clear,
                    Color.white.opacity(0.05),
                    Color.clear
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .mask(
                Rectangle()
                    .fill(
                        LinearGradient(
                            colors: [Color.clear, Color.white, Color.clear],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .rotationEffect(.degrees(30))
                    .offset(x: shimmerPhase * geometry.size.width * 2 - geometry.size.width)
            )
        }
        .allowsHitTesting(false)
    }

    private var modalBorder: some View {
        RoundedRectangle(cornerRadius: TaroRadius.xxl, style: .continuous)
            .stroke(
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.4),
                        Color.lightViolet.opacity(0.2),
                        Color.mysticCyan.opacity(0.2),
                        Color.mysticViolet.opacity(0.4)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                ),
                lineWidth: 1
            )
    }

    // MARK: - Animations

    private func animateIn() {
        // Start shimmer animation
        withAnimation(.linear(duration: 4).repeatForever(autoreverses: false)) {
            shimmerPhase = 1
        }

        // Background fade
        withAnimation(.easeOut(duration: 0.3)) {
            backgroundOpacity = 1
        }

        // Modal entrance
        withAnimation(.spring(response: 0.5, dampingFraction: 0.75)) {
            modalScale = 1
            modalOpacity = 1
            contentOffset = 0
        }

        // Start orb animations after modal appears using Task
        animationTask = Task { @MainActor in
            try? await Task.sleep(nanoseconds: 300_000_000)
            guard !Task.isCancelled else { return }
            orbsAnimating = true
        }
    }

    private func animateOut(completion: @escaping () -> Void) {
        // Cancel any pending animation tasks
        animationTask?.cancel()
        dismissTask?.cancel()

        // Stop orb animations
        orbsAnimating = false

        // Modal exit
        withAnimation(.easeIn(duration: 0.25)) {
            modalScale = 0.9
            modalOpacity = 0
            contentOffset = 20
            backgroundOpacity = 0
        }

        dismissTask = Task { @MainActor in
            try? await Task.sleep(nanoseconds: 250_000_000)
            guard !Task.isCancelled else { return }
            isPresented = false
            completion()
        }
    }

    private func dismissKeyboard() {
        isTextFieldFocused = false
    }
}

// MARK: - Modal Presentation Modifier

struct QuestionInputModalModifier: ViewModifier {
    @Binding var isPresented: Bool
    @Binding var question: String
    let spreadType: SpreadType
    var onContinue: () -> Void
    var onSkip: (() -> Void)?

    func body(content: Content) -> some View {
        ZStack {
            content

            if isPresented {
                QuestionInputModal(
                    isPresented: $isPresented,
                    question: $question,
                    spreadType: spreadType,
                    onContinue: onContinue,
                    onSkip: onSkip
                )
                .transition(.opacity)
                .zIndex(100)
            }
        }
    }
}

extension View {
    func questionInputModal(
        isPresented: Binding<Bool>,
        question: Binding<String>,
        spreadType: SpreadType,
        onContinue: @escaping () -> Void,
        onSkip: (() -> Void)? = nil
    ) -> some View {
        modifier(QuestionInputModalModifier(
            isPresented: isPresented,
            question: question,
            spreadType: spreadType,
            onContinue: onContinue,
            onSkip: onSkip
        ))
    }
}

// MARK: - Preview

#Preview("Question Input Modal") {
    struct PreviewWrapper: View {
        @State private var isPresented = true
        @State private var question = ""

        var body: some View {
            ZStack {
                AuroraBackground()

                VStack {
                    Text("Tap to show modal")
                        .foregroundColor(.textPrimary)

                    GlassButton("Open Modal", style: .primary) {
                        isPresented = true
                    }
                }
            }
            .questionInputModal(
                isPresented: $isPresented,
                question: $question,
                spreadType: .celtic,
                onContinue: {
                    print("Continue with question: \(question)")
                },
                onSkip: {
                    print("Skipped")
                }
            )
        }
    }

    return PreviewWrapper()
        .preferredColorScheme(.dark)
}

#Preview("Question Input Modal - Three Card") {
    struct PreviewWrapper: View {
        @State private var isPresented = true
        @State private var question = "Should I pursue this new opportunity?"

        var body: some View {
            ZStack {
                AuroraBackground()
            }
            .questionInputModal(
                isPresented: $isPresented,
                question: $question,
                spreadType: .threeCard,
                onContinue: {
                    print("Continue with question: \(question)")
                }
            )
        }
    }

    return PreviewWrapper()
        .preferredColorScheme(.dark)
}
