import SwiftUI

// MARK: - Model Status View

/// Displays the current status of the on-device LLM model
/// Shows loading progress, errors, and device compatibility
struct ModelStatusView: View {
    @ObservedObject var modelManager: ModelManager

    @State private var animationPhase = 0.0
    @State private var pulseOpacity: Double = 0.5

    var body: some View {
        GlassPanel(
            style: .card,
            cornerRadius: TaroRadius.xl,
            padding: TaroSpacing.lg,
            glowColor: glowColor,
            glowRadius: 15
        ) {
            content
        }
    }

    @ViewBuilder
    private var content: some View {
        switch modelManager.state {
        case .notLoaded:
            notLoadedView

        case .checking:
            checkingView

        case .loading(let progress):
            loadingView(progress: progress)

        case .loaded:
            loadedView

        case .error(let error):
            errorView(error: error)
        }
    }

    // MARK: - State Views

    private var notLoadedView: some View {
        HStack(spacing: TaroSpacing.md) {
            Image(systemName: "cpu")
                .font(.system(size: 24))
                .foregroundColor(.textMuted)

            VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                Text("On-Device AI")
                    .font(TaroTypography.headline)
                    .foregroundColor(.textPrimary)

                Text("Model not loaded")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
            }

            Spacer()
        }
    }

    private var checkingView: some View {
        HStack(spacing: TaroSpacing.md) {
            ProgressView()
                .progressViewStyle(CircularProgressViewStyle(tint: .mysticViolet))

            VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                Text("Checking AI Model...")
                    .font(TaroTypography.headline)
                    .foregroundColor(.textPrimary)

                Text("Verifying model integrity")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
            }

            Spacer()
        }
    }

    private func loadingView(progress: Double) -> some View {
        VStack(spacing: TaroSpacing.md) {
            HStack(spacing: TaroSpacing.md) {
                // Animated loading indicator
                ZStack {
                    Circle()
                        .stroke(Color.mysticViolet.opacity(0.2), lineWidth: 3)
                        .frame(width: 36, height: 36)

                    Circle()
                        .trim(from: 0, to: 0.7)
                        .stroke(
                            LinearGradient(
                                colors: [.mysticViolet, .mysticCyan],
                                startPoint: .leading,
                                endPoint: .trailing
                            ),
                            style: StrokeStyle(lineWidth: 3, lineCap: .round)
                        )
                        .frame(width: 36, height: 36)
                        .rotationEffect(.degrees(animationPhase))
                }
                .onAppear {
                    withAnimation(
                        Animation
                            .linear(duration: 1)
                            .repeatForever(autoreverses: false)
                    ) {
                        animationPhase = 360
                    }
                }

                VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                    Text("Loading AI Oracle...")
                        .font(TaroTypography.headline)
                        .foregroundColor(.textPrimary)

                    Text("Preparing for on-device readings")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                }

                Spacer()
            }

            // Progress bar
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: TaroRadius.xs)
                        .fill(Color.white.opacity(0.1))
                        .frame(height: 4)

                    RoundedRectangle(cornerRadius: TaroRadius.xs)
                        .fill(
                            LinearGradient(
                                colors: [.mysticViolet, .mysticCyan],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .frame(width: geometry.size.width * progress, height: 4)
                        .animation(.easeInOut(duration: 0.3), value: progress)
                }
            }
            .frame(height: 4)

            // Progress percentage
            Text("\(Int(progress * 100))%")
                .font(TaroTypography.caption2)
                .foregroundColor(.textMuted)
                .frame(maxWidth: .infinity, alignment: .trailing)
        }
    }

    private var loadedView: some View {
        HStack(spacing: TaroSpacing.md) {
            ZStack {
                Circle()
                    .fill(Color.mysticTeal.opacity(0.2))
                    .frame(width: 40, height: 40)

                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 20))
                    .foregroundColor(.mysticTeal)
            }
            .opacity(pulseOpacity)
            .onAppear {
                withAnimation(
                    Animation
                        .easeInOut(duration: 2)
                        .repeatForever(autoreverses: true)
                ) {
                    pulseOpacity = 0.8
                }
            }

            VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                Text("AI Oracle Ready")
                    .font(TaroTypography.headline)
                    .foregroundColor(.textPrimary)

                Text("On-device • Private • No internet required")
                    .font(TaroTypography.caption)
                    .foregroundColor(.textMuted)
            }

            Spacer()

            // Model info badge
            Text(ModelManager.modelInfo.name)
                .font(TaroTypography.caption2)
                .foregroundColor(.mysticViolet)
                .padding(.horizontal, TaroSpacing.sm)
                .padding(.vertical, TaroSpacing.xxs)
                .background(Color.mysticViolet.opacity(0.15))
                .clipShape(Capsule())
        }
    }

    private func errorView(error: ModelManager.ModelError) -> some View {
        VStack(spacing: TaroSpacing.md) {
            HStack(spacing: TaroSpacing.md) {
                ZStack {
                    Circle()
                        .fill(Color.mysticPink.opacity(0.2))
                        .frame(width: 40, height: 40)

                    Image(systemName: "exclamationmark.triangle.fill")
                        .font(.system(size: 18))
                        .foregroundColor(.mysticPink)
                }

                VStack(alignment: .leading, spacing: TaroSpacing.xxs) {
                    Text("AI Unavailable")
                        .font(TaroTypography.headline)
                        .foregroundColor(.textPrimary)

                    Text(error.errorDescription ?? "An error occurred")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textSecondary)
                        .lineLimit(2)
                }

                Spacer()
            }

            if let recovery = error.recoverySuggestion {
                Text(recovery)
                    .font(TaroTypography.footnote)
                    .foregroundColor(.textMuted)
                    .multilineTextAlignment(.leading)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.top, TaroSpacing.xxs)
            }

            // Retry button for recoverable errors
            if isRetryable(error) {
                GlassButton("Try Again", icon: "arrow.clockwise", style: .secondary) {
                    Task {
                        modelManager.resetError()
                        try? await modelManager.loadModel()
                    }
                }
            }
        }
    }

    // MARK: - Helpers

    private var glowColor: Color? {
        switch modelManager.state {
        case .loaded:
            return .mysticTeal
        case .error:
            return .mysticPink
        case .loading:
            return .mysticViolet
        default:
            return nil
        }
    }

    private func isRetryable(_ error: ModelManager.ModelError) -> Bool {
        switch error {
        case .insufficientMemory, .loadingFailed, .unknown:
            return true
        case .deviceNotSupported, .modelNotFound, .modelCorrupted:
            return false
        }
    }
}

// MARK: - Compact Model Status

/// A smaller version for inline display
struct CompactModelStatusView: View {
    @ObservedObject var modelManager: ModelManager

    var body: some View {
        HStack(spacing: TaroSpacing.sm) {
            statusIcon
            statusText
        }
    }

    @ViewBuilder
    private var statusIcon: some View {
        switch modelManager.state {
        case .loaded:
            Image(systemName: "cpu.fill")
                .foregroundColor(.mysticTeal)
        case .loading, .checking:
            ProgressView()
                .scaleEffect(0.7)
        case .error:
            Image(systemName: "exclamationmark.circle.fill")
                .foregroundColor(.mysticPink)
        case .notLoaded:
            Image(systemName: "cpu")
                .foregroundColor(.textMuted)
        }
    }

    @ViewBuilder
    private var statusText: some View {
        switch modelManager.state {
        case .loaded:
            Text("AI Ready")
                .font(TaroTypography.caption)
                .foregroundColor(.mysticTeal)
        case .loading(let progress):
            Text("Loading \(Int(progress * 100))%")
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
        case .checking:
            Text("Checking...")
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
        case .error:
            Text("Unavailable")
                .font(TaroTypography.caption)
                .foregroundColor(.mysticPink)
        case .notLoaded:
            Text("Not loaded")
                .font(TaroTypography.caption)
                .foregroundColor(.textMuted)
        }
    }
}

// MARK: - Device Unsupported View

/// Full-screen view shown when device doesn't support local LLM
struct DeviceUnsupportedView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack {
            AuroraBackground()

            VStack(spacing: TaroSpacing.xl) {
                Spacer()

                // Icon
                ZStack {
                    Circle()
                        .fill(Color.mysticViolet.opacity(0.15))
                        .frame(width: 120, height: 120)

                    Image(systemName: "iphone.gen3.slash")
                        .font(.system(size: 48))
                        .foregroundColor(.mysticViolet)
                }

                // Title
                Text("Device Not Supported")
                    .font(TaroTypography.title)
                    .foregroundColor(.textPrimary)

                // Description
                GlassPanel(style: .card, cornerRadius: TaroRadius.xl, padding: TaroSpacing.lg) {
                    VStack(spacing: TaroSpacing.md) {
                        Text(DeviceCapability.unsupportedReason ?? "This device cannot run on-device AI.")
                            .font(TaroTypography.body)
                            .foregroundColor(.textSecondary)
                            .multilineTextAlignment(.center)

                        GlassDivider()

                        VStack(alignment: .leading, spacing: TaroSpacing.sm) {
                            Text("Requirements:")
                                .font(TaroTypography.headline)
                                .foregroundColor(.textPrimary)

                            requirementRow("iPhone 15 Pro or later", met: false)
                            requirementRow("A17 Pro chip or newer", met: false)
                            requirementRow("8GB RAM minimum", met: false)
                        }
                    }
                }
                .padding(.horizontal, TaroSpacing.lg)

                // Device info
                VStack(spacing: TaroSpacing.xxs) {
                    Text("Your Device")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)

                    Text(DeviceCapability.deviceName)
                        .font(TaroTypography.subheadline)
                        .foregroundColor(.textSecondary)

                    Text("\(DeviceCapability.physicalMemoryGB) RAM")
                        .font(TaroTypography.caption)
                        .foregroundColor(.textMuted)
                }

                Spacer()

                // Dismiss button
                GlassButton("I Understand", style: .primary) {
                    dismiss()
                }
                .padding(.horizontal, TaroSpacing.xl)
                .padding(.bottom, TaroSpacing.xl)
            }
        }
    }

    private func requirementRow(_ text: String, met: Bool) -> some View {
        HStack(spacing: TaroSpacing.sm) {
            Image(systemName: met ? "checkmark.circle.fill" : "xmark.circle.fill")
                .foregroundColor(met ? .mysticTeal : .mysticPink)
                .font(.system(size: 16))

            Text(text)
                .font(TaroTypography.subheadline)
                .foregroundColor(.textSecondary)

            Spacer()
        }
    }
}

// MARK: - Preview

#Preview("Model Status - Loading") {
    ZStack {
        AuroraBackground()

        VStack(spacing: TaroSpacing.lg) {
            ModelStatusView(modelManager: MockModelManager.loading)
            ModelStatusView(modelManager: MockModelManager.loaded)
            ModelStatusView(modelManager: MockModelManager.error)
        }
        .padding()
    }
    .preferredColorScheme(.dark)
}

#Preview("Device Unsupported") {
    DeviceUnsupportedView()
        .preferredColorScheme(.dark)
}

// MARK: - Mock for Previews

#if DEBUG
@MainActor
private class MockModelManager: ModelManager {
    override init() {
        super.init()
    }

    static let loading: ModelManager = {
        let manager = ModelManager.shared
        return manager
    }()

    static let loaded: ModelManager = {
        let manager = ModelManager.shared
        return manager
    }()

    static let error: ModelManager = {
        let manager = ModelManager.shared
        return manager
    }()
}
#endif
