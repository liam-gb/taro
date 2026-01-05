import SwiftUI

struct HomeView: View {
    @EnvironmentObject var readingSession: ReadingSession

    @State private var selectedSpread: SpreadType? = nil
    @State private var showQuestionModal: Bool = false
    @State private var questionText: String = ""
    @State private var titleOpacity: Double = 0
    @State private var subtitleOpacity: Double = 0
    @State private var cardsAppeared: Bool = false
    @State private var headerGlowPulse: Bool = false

    var body: some View {
        ZStack {
            // Aurora animated background
            AuroraBackground()

            VStack(spacing: 0) {
                // Header section
                headerSection
                    .padding(.top, TaroSpacing.xl)

                // Spread selection carousel
                spreadSelectionSection

                Spacer()

                // Bottom action area
                bottomSection
                    .padding(.bottom, TaroSpacing.xl)
            }
        }
        .navigationBarHidden(true)
        .task {
            await animateEntrance()
        }
        .questionInputModal(
            isPresented: $showQuestionModal,
            question: $questionText,
            spreadType: selectedSpread ?? .single,
            onContinue: {
                startReading()
            },
            onSkip: {
                questionText = ""
                startReading()
            }
        )
    }

    // MARK: - Header Section

    private var headerSection: some View {
        VStack(spacing: TaroSpacing.sm) {
            // Decorative glow behind title
            ZStack {
                // Pulsing glow
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color.mysticViolet.opacity(headerGlowPulse ? 0.15 : 0.08),
                                Color.clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: 80
                        )
                    )
                    .frame(width: 160, height: 160)
                    .blur(radius: 30)
                    .animation(
                        .easeInOut(duration: 3).repeatForever(autoreverses: true),
                        value: headerGlowPulse
                    )

                VStack(spacing: TaroSpacing.xs) {
                    // App title with mystical styling
                    Text("TARO")
                        .font(TaroTypography.mystical(52, weight: .ultraLight))
                        .tracking(20)
                        .foregroundColor(.textPrimary)
                        .shadow(color: Color.mysticViolet.opacity(0.3), radius: 20)

                    Text("Private Tarot Readings")
                        .font(TaroTypography.ethereal(14, weight: .light))
                        .foregroundColor(.textSecondary)
                        .tracking(2)
                }
                .opacity(titleOpacity)
            }

            // Decorative divider
            HStack(spacing: TaroSpacing.md) {
                Rectangle()
                    .fill(
                        LinearGradient(
                            colors: [Color.clear, Color.mysticViolet.opacity(0.3)],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: 50, height: 1)

                Image(systemName: "sparkle")
                    .font(.system(size: 10))
                    .foregroundColor(.mysticViolet.opacity(0.5))

                Rectangle()
                    .fill(
                        LinearGradient(
                            colors: [Color.mysticViolet.opacity(0.3), Color.clear],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: 50, height: 1)
            }
            .opacity(subtitleOpacity)
        }
    }

    // MARK: - Spread Selection Section

    private var spreadSelectionSection: some View {
        VStack(spacing: TaroSpacing.md) {
            // Section label
            Text("Choose Your Spread")
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
                .textCase(.uppercase)
                .tracking(2)
                .opacity(subtitleOpacity)
                .padding(.top, TaroSpacing.xl)

            // Horizontal carousel of spread cards
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: TaroSpacing.md) {
                    ForEach(Array(SpreadType.allCases.enumerated()), id: \.element.id) { index, spread in
                        SpreadSelectionCard(
                            spreadType: spread,
                            isSelected: selectedSpread == spread,
                            delay: Double(index) * 0.1
                        ) {
                            selectSpread(spread)
                        }
                        .opacity(cardsAppeared ? 1 : 0)
                        .offset(y: cardsAppeared ? 0 : 30)
                        .animation(
                            .spring(response: 0.6, dampingFraction: 0.7)
                                .delay(Double(index) * 0.08 + 0.3),
                            value: cardsAppeared
                        )
                    }
                }
                .padding(.horizontal, TaroSpacing.lg)
                .padding(.vertical, TaroSpacing.md)
            }

            // Selected spread info
            if let spread = selectedSpread {
                selectedSpreadInfo(spread)
                    .transition(.asymmetric(
                        insertion: .scale.combined(with: .opacity),
                        removal: .opacity
                    ))
            }
        }
    }

    @ViewBuilder
    private func selectedSpreadInfo(_ spread: SpreadType) -> some View {
        GlassPanel(style: .standard, cornerRadius: TaroRadius.lg, padding: TaroSpacing.md) {
            VStack(spacing: TaroSpacing.xs) {
                Text(spread.description)
                    .font(TaroTypography.ethereal(14, weight: .regular))
                    .foregroundColor(.textSecondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)

                HStack(spacing: TaroSpacing.xxs) {
                    Image(systemName: "rectangle.portrait.on.rectangle.portrait")
                        .font(.system(size: 11))
                    Text("\(spread.cardCount) cards will be drawn")
                        .font(TaroTypography.caption)
                }
                .foregroundColor(.textMuted)
            }
        }
        .padding(.horizontal, TaroSpacing.xl)
        .animation(.spring(response: 0.4, dampingFraction: 0.8), value: selectedSpread)
    }

    // MARK: - Bottom Section

    private var bottomSection: some View {
        VStack(spacing: TaroSpacing.md) {
            // Begin reading button (only shows when spread is selected)
            if selectedSpread != nil {
                GlowingButton("Begin Reading", icon: "sparkles") {
                    showQuestionModal = true
                }
                .frame(maxWidth: .infinity)
                .padding(.horizontal, TaroSpacing.xl)
                .transition(.asymmetric(
                    insertion: .move(edge: .bottom).combined(with: .opacity),
                    removal: .opacity
                ))
            }

            // History link
            GlassButton("Reading History", icon: "clock.arrow.circlepath", style: .text) {
                // TODO: Navigate to history
            }
            .opacity(subtitleOpacity)
        }
        .animation(.spring(response: 0.5, dampingFraction: 0.8), value: selectedSpread)
    }

    // MARK: - Actions

    private func selectSpread(_ spread: SpreadType) {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred()

        withAnimation(.spring(response: 0.4, dampingFraction: 0.75)) {
            if selectedSpread == spread {
                // Tapping same spread opens modal
                showQuestionModal = true
            } else {
                selectedSpread = spread
            }
        }
    }

    private func startReading() {
        guard let spread = selectedSpread else { return }

        readingSession.selectSpread(spread)
        readingSession.question = questionText

        // Reset for next time
        questionText = ""
        selectedSpread = nil
    }

    // MARK: - Animations

    private func animateEntrance() async {
        withAnimation(.easeOut(duration: 0.6)) { titleOpacity = 1 }
        withAnimation(.easeOut(duration: 0.5).delay(0.2)) { subtitleOpacity = 1 }

        try? await Task.sleep(for: .milliseconds(100))
        guard !Task.isCancelled else { return }
        cardsAppeared = true

        try? await Task.sleep(for: .milliseconds(400))
        guard !Task.isCancelled else { return }
        headerGlowPulse = true
    }
}

// MARK: - Spread Selection Card

struct SpreadSelectionCard: View {
    let spreadType: SpreadType
    let isSelected: Bool
    var delay: Double = 0
    var onTap: () -> Void

    @State private var isPressed: Bool = false
    @State private var glowPulse: Bool = false

    var body: some View {
        Button(action: onTap) {
            VStack(spacing: TaroSpacing.sm) {
                // Spread preview
                ZStack {
                    // Selection glow
                    if isSelected {
                        RoundedRectangle(cornerRadius: TaroRadius.md)
                            .fill(
                                RadialGradient(
                                    colors: [
                                        Color.mysticViolet.opacity(glowPulse ? 0.25 : 0.15),
                                        Color.clear
                                    ],
                                    center: .center,
                                    startRadius: 0,
                                    endRadius: 80
                                )
                            )
                            .frame(width: 160, height: 120)
                            .blur(radius: 20)
                    }

                    SpreadPreview(
                        spreadType: spreadType,
                        size: CGSize(width: 140, height: 100),
                        isAnimated: isSelected
                    )
                }
                .frame(height: 100)

                // Spread info
                VStack(spacing: TaroSpacing.xxxs) {
                    Text(spreadType.displayName)
                        .font(TaroTypography.ethereal(14, weight: .medium))
                        .foregroundColor(isSelected ? .textPrimary : .textSecondary)
                        .lineLimit(1)
                        .minimumScaleFactor(0.8)

                    // Card count indicator
                    cardCountIndicator
                }
                .padding(.bottom, TaroSpacing.xs)
            }
            .padding(.horizontal, TaroSpacing.md)
            .padding(.top, TaroSpacing.md)
            .frame(width: 170)
            .background(cardBackground)
            .clipShape(RoundedRectangle(cornerRadius: TaroRadius.xl, style: .continuous))
            .overlay(cardBorder)
            .shadow(
                color: isSelected ? Color.mysticViolet.opacity(0.3) : Color.black.opacity(0.3),
                radius: isSelected ? 20 : 12,
                y: isSelected ? 8 : 6
            )
            .scaleEffect(isPressed ? 0.96 : (isSelected ? 1.02 : 1.0))
        }
        .buttonStyle(.plain)
        .simultaneousGesture(
            DragGesture(minimumDistance: 0)
                .onChanged { _ in isPressed = true }
                .onEnded { _ in isPressed = false }
        )
        .animation(TaroAnimation.springBouncy, value: isPressed)
        .animation(TaroAnimation.springSmooth, value: isSelected)
        .onChange(of: isSelected) { _, newValue in
            if newValue {
                withAnimation(.easeInOut(duration: 2).repeatForever(autoreverses: true)) {
                    glowPulse = true
                }
            } else {
                withAnimation(.linear(duration: 0.1)) {
                    glowPulse = false
                }
            }
        }
        .onAppear {
            if isSelected {
                withAnimation(.easeInOut(duration: 2).repeatForever(autoreverses: true)) {
                    glowPulse = true
                }
            }
        }
        .onDisappear {
            glowPulse = false
        }
    }

    private var cardCountIndicator: some View {
        HStack(spacing: 3) {
            ForEach(0..<min(spreadType.cardCount, 7), id: \.self) { index in
                RoundedRectangle(cornerRadius: 1.5)
                    .fill(
                        isSelected
                            ? Color.mysticViolet.opacity(0.7)
                            : Color.textMuted.opacity(0.4)
                    )
                    .frame(width: 4, height: 8)
            }
            if spreadType.cardCount > 7 {
                Text("+")
                    .font(TaroTypography.caption2)
                    .foregroundColor(.textMuted)
            }
        }
    }

    private var cardBackground: some View {
        ZStack {
            // Base gradient
            LinearGradient(
                colors: isSelected
                    ? [Color.mysticViolet.opacity(0.12), Color.deepViolet.opacity(0.06)]
                    : [Color.white.opacity(0.04), Color.white.opacity(0.02)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            // Glass material
            Material.ultraThinMaterial
                .opacity(isSelected ? 0.5 : 0.35)
        }
    }

    private var cardBorder: some View {
        RoundedRectangle(cornerRadius: TaroRadius.xl, style: .continuous)
            .stroke(
                isSelected
                    ? LinearGradient(
                        colors: [
                            Color.mysticViolet.opacity(0.6),
                            Color.lightViolet.opacity(0.3),
                            Color.mysticCyan.opacity(0.2)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                    : LinearGradient(
                        colors: [
                            Color.white.opacity(0.08),
                            Color.white.opacity(0.04)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                lineWidth: isSelected ? 1.5 : 1
            )
    }
}

// MARK: - Preview

#Preview {
    HomeView()
        .environmentObject(ReadingSession())
        .preferredColorScheme(.dark)
}

#Preview("With Selection") {
    struct PreviewWrapper: View {
        @StateObject private var session = ReadingSession()

        var body: some View {
            HomeView()
                .environmentObject(session)
        }
    }

    return PreviewWrapper()
        .preferredColorScheme(.dark)
}
