import SwiftUI

/// Sheet UI for copying an AI-ready tarot reading prompt to clipboard
/// Used for devices that don't support on-device LLM (pre-iPhone 15 Pro)
struct CopyPromptSheet: View {
    let prompt: String
    @Binding var isPresented: Bool

    @State private var hasCopied = false
    @State private var copyScale: CGFloat = 1.0

    var body: some View {
        NavigationStack {
            ZStack {
                // Background
                AuroraBackground()

                VStack(spacing: TaroSpacing.lg) {
                    // Header explanation
                    headerSection

                    // Prompt preview
                    promptPreview

                    // Copy button
                    copyButton

                    Spacer()
                }
                .padding(.horizontal, TaroSpacing.lg)
                .padding(.top, TaroSpacing.md)
            }
            .navigationTitle("AI Prompt")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        isPresented = false
                    } label: {
                        Image(systemName: "xmark.circle.fill")
                            .font(.system(size: 24))
                            .foregroundColor(.textMuted)
                    }
                }
            }
            .toolbarBackground(.hidden, for: .navigationBar)
        }
        .presentationBackground(.ultraThinMaterial)
        .presentationCornerRadius(TaroRadius.xxl)
    }

    // MARK: - Header Section

    private var headerSection: some View {
        GlassPanel(style: .card, cornerRadius: TaroRadius.lg, padding: TaroSpacing.md) {
            VStack(spacing: TaroSpacing.sm) {
                Image(systemName: "sparkles")
                    .font(.system(size: 28))
                    .foregroundStyle(
                        LinearGradient(
                            colors: [.mysticViolet, .mysticCyan],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )

                Text("Copy Prompt for AI Chat")
                    .font(TaroTypography.headline)
                    .foregroundColor(.textPrimary)

                Text("Paste this prompt into ChatGPT, Claude, or your preferred AI assistant to receive your personalized tarot reading.")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textSecondary)
                    .multilineTextAlignment(.center)
            }
        }
    }

    // MARK: - Prompt Preview

    private var promptPreview: some View {
        GlassPanel(
            style: .summary,
            cornerRadius: TaroRadius.lg,
            padding: TaroSpacing.md,
            glowColor: .mysticViolet,
            glowRadius: 10
        ) {
            VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                HStack {
                    Text("PROMPT PREVIEW")
                        .font(TaroTypography.caption)
                        .foregroundColor(.mysticViolet)
                        .tracking(1)

                    Spacer()

                    Text("\(prompt.count) characters")
                        .font(TaroTypography.caption2)
                        .foregroundColor(.textMuted)
                }

                GlassDivider()

                ScrollView {
                    Text(prompt)
                        .font(TaroTypography.body)
                        .foregroundColor(.textPrimary)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .textSelection(.enabled)
                }
                .frame(maxHeight: 300)
            }
        }
    }

    // MARK: - Copy Button

    private var copyButton: some View {
        Button(action: copyToClipboard) {
            HStack(spacing: TaroSpacing.sm) {
                if hasCopied {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 18, weight: .medium))
                        .foregroundColor(.mysticEmerald)

                    Text("Copied!")
                        .font(TaroTypography.ethereal(16, weight: .semibold))
                        .foregroundColor(.mysticEmerald)
                } else {
                    Image(systemName: "doc.on.doc")
                        .font(.system(size: 16, weight: .medium))

                    Text("Copy Prompt")
                        .font(TaroTypography.ethereal(16, weight: .semibold))
                }
            }
            .foregroundColor(hasCopied ? .mysticEmerald : .textPrimary)
            .padding(.horizontal, TaroSpacing.xl)
            .padding(.vertical, TaroSpacing.md)
            .background(buttonBackground)
            .clipShape(RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous))
            .overlay(buttonBorder)
            .shadow(color: hasCopied ? Color.mysticEmerald.opacity(0.3) : Color.mysticViolet.opacity(0.2), radius: 15)
            .shadow(color: Color.black.opacity(0.3), radius: 8, y: 4)
        }
        .buttonStyle(PlainButtonStyle())
        .scaleEffect(copyScale)
        .animation(TaroAnimation.springBouncy, value: copyScale)
        .animation(TaroAnimation.springSmooth, value: hasCopied)
    }

    private var buttonBackground: some View {
        ZStack {
            if hasCopied {
                LinearGradient(
                    colors: [
                        Color.mysticEmerald.opacity(0.2),
                        Color.mysticTeal.opacity(0.15)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            } else {
                LinearGradient(
                    colors: [
                        Color.mysticViolet.opacity(0.15),
                        Color.mysticViolet.opacity(0.05)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            }

            Material.ultraThinMaterial
                .opacity(0.3)
        }
    }

    private var buttonBorder: some View {
        RoundedRectangle(cornerRadius: TaroRadius.md, style: .continuous)
            .stroke(
                hasCopied ? Color.mysticEmerald.opacity(0.4) : Color.mysticViolet.opacity(0.3),
                lineWidth: 1
            )
    }

    // MARK: - Actions

    private func copyToClipboard() {
        // Haptic feedback
        let impact = UIImpactFeedbackGenerator(style: .medium)
        impact.impactOccurred()

        // Copy to clipboard
        UIPasteboard.general.string = prompt

        // Visual feedback
        withAnimation {
            copyScale = 0.95
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            withAnimation {
                copyScale = 1.0
                hasCopied = true
            }
        }

        // Success haptic
        let notification = UINotificationFeedbackGenerator()
        notification.notificationOccurred(.success)

        // Reset after delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            withAnimation {
                hasCopied = false
            }
        }
    }
}

// MARK: - Preview

#Preview {
    CopyPromptSheet(
        prompt: """
        I'm seeking guidance from a tarot reading. Here are the cards I drew:

        1. Past Position: The Fool (Upright)
           Keywords: new beginnings, innocence, spontaneity
           Base meaning: A fresh start, embracing the unknown with optimism.

        2. Present Position: The Tower (Reversed)
           Keywords: upheaval, sudden change, revelation
           Base meaning: Resistance to necessary change, delayed transformation.

        3. Future Position: The Star (Upright)
           Keywords: hope, inspiration, serenity
           Base meaning: Renewal and healing after difficult times.

        Elemental Flow: Spirit -> Fire -> Water

        Please provide a cohesive interpretation of this reading, weaving together the individual card meanings into a narrative that addresses my journey.
        """,
        isPresented: .constant(true)
    )
    .preferredColorScheme(.dark)
}
