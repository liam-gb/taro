import Foundation

// MARK: - Model Manager

/// Manages local LLM model lifecycle: loading, verification, and memory management
@MainActor
final class ModelManager: ObservableObject {
    static let shared = ModelManager()

    // MARK: - Model Configuration

    /// The bundled model filename (without extension)
    static let modelFilename = "Phi-3-mini-4k-instruct-q4"

    /// The model file extension
    static let modelExtension = "gguf"

    /// Expected model file size in bytes (~2.39GB for Q4_K_M)
    static let expectedModelSize: UInt64 = 2_390_000_000

    /// Tolerance for model size verification (5%)
    static let modelSizeTolerance: Double = 0.05

    // MARK: - Published State

    @Published private(set) var state: ModelState = .notLoaded
    @Published private(set) var loadProgress: Double = 0
    @Published private(set) var loadError: ModelError?

    // MARK: - Model State

    enum ModelState: Equatable {
        case notLoaded
        case checking
        case loading(progress: Double)
        case loaded
        case error(ModelError)

        var isReady: Bool {
            if case .loaded = self { return true }
            return false
        }

        var isLoading: Bool {
            switch self {
            case .checking, .loading:
                return true
            default:
                return false
            }
        }
    }

    // MARK: - Errors

    enum ModelError: LocalizedError, Equatable {
        case deviceNotSupported(String)
        case modelNotFound
        case modelCorrupted
        case insufficientMemory
        case loadingFailed(String)
        case unknown(String)

        var errorDescription: String? {
            switch self {
            case .deviceNotSupported(let reason):
                return reason
            case .modelNotFound:
                return "The AI model could not be found in the app bundle."
            case .modelCorrupted:
                return "The AI model appears to be corrupted. Please reinstall the app."
            case .insufficientMemory:
                return "Not enough memory available to load the AI model. Please close other apps and try again."
            case .loadingFailed(let reason):
                return "Failed to load the AI model: \(reason)"
            case .unknown(let message):
                return "An unexpected error occurred: \(message)"
            }
        }

        var recoverySuggestion: String? {
            switch self {
            case .deviceNotSupported:
                return "On-device AI readings require iPhone 15 Pro or later."
            case .modelNotFound, .modelCorrupted:
                return "Try reinstalling the app from the App Store."
            case .insufficientMemory:
                return "Close background apps to free up memory, then try again."
            case .loadingFailed, .unknown:
                return "If this problem persists, please restart the app."
            }
        }
    }

    // MARK: - Private Properties

    private var modelURL: URL?
    private var isModelLoaded = false
    private let loadQueue = DispatchQueue(label: "com.taro.modelmanager", qos: .userInitiated)

    // MARK: - Initialization

    private init() {}

    // MARK: - Public API

    /// Check if the device supports local LLM and model is available
    func checkAvailability() async -> Bool {
        // Check device capability first
        guard DeviceCapability.supportsLocalLLM else {
            let reason = DeviceCapability.unsupportedReason ?? "Device not supported"
            state = .error(.deviceNotSupported(reason))
            loadError = .deviceNotSupported(reason)
            return false
        }

        // Check if model exists in bundle
        guard getModelURL() != nil else {
            state = .error(.modelNotFound)
            loadError = .modelNotFound
            return false
        }

        return true
    }

    /// Load the model into memory
    func loadModel() async throws {
        // Prevent duplicate loading
        guard !state.isLoading && !state.isReady else { return }

        state = .checking
        loadError = nil
        loadProgress = 0

        // Check device support
        guard DeviceCapability.supportsLocalLLM else {
            let reason = DeviceCapability.unsupportedReason ?? "Device not supported"
            let error = ModelError.deviceNotSupported(reason)
            state = .error(error)
            loadError = error
            throw error
        }

        // Check memory availability
        guard DeviceCapability.hasEnoughAvailableMemory else {
            let error = ModelError.insufficientMemory
            state = .error(error)
            loadError = error
            throw error
        }

        // Find model file
        guard let url = getModelURL() else {
            let error = ModelError.modelNotFound
            state = .error(error)
            loadError = error
            throw error
        }

        // Verify model file
        state = .loading(progress: 0.1)
        loadProgress = 0.1

        do {
            try await verifyModelFile(at: url)
        } catch {
            let modelError = error as? ModelError ?? .unknown(error.localizedDescription)
            state = .error(modelError)
            loadError = modelError
            throw modelError
        }

        state = .loading(progress: 0.3)
        loadProgress = 0.3

        // Simulate loading progress for now
        // In actual implementation, llama.cpp will provide progress callbacks
        for progress in stride(from: 0.3, to: 1.0, by: 0.1) {
            try await Task.sleep(nanoseconds: 100_000_000) // 0.1 seconds
            state = .loading(progress: progress)
            loadProgress = progress
        }

        modelURL = url
        isModelLoaded = true
        state = .loaded
        loadProgress = 1.0

        print("ModelManager: Model loaded successfully from \(url.path)")
    }

    /// Unload the model from memory
    func unloadModel() {
        modelURL = nil
        isModelLoaded = false
        state = .notLoaded
        loadProgress = 0

        // Force memory cleanup
        autoreleasepool { }

        print("ModelManager: Model unloaded")
    }

    /// Get the URL to the loaded model
    func getLoadedModelURL() -> URL? {
        guard isModelLoaded else { return nil }
        return modelURL
    }

    /// Reset error state for retry
    func resetError() {
        if case .error = state {
            state = .notLoaded
            loadError = nil
        }
    }

    // MARK: - Private Helpers

    private func getModelURL() -> URL? {
        // Check bundle for the model file
        if let bundleURL = Bundle.main.url(
            forResource: Self.modelFilename,
            withExtension: Self.modelExtension
        ) {
            return bundleURL
        }

        // Check Documents directory as fallback (for development)
        let documentsURL = FileManager.default.urls(
            for: .documentDirectory,
            in: .userDomainMask
        ).first

        if let docsURL = documentsURL {
            let modelPath = docsURL.appendingPathComponent(
                "\(Self.modelFilename).\(Self.modelExtension)"
            )
            if FileManager.default.fileExists(atPath: modelPath.path) {
                return modelPath
            }
        }

        return nil
    }

    private func verifyModelFile(at url: URL) async throws {
        // Check file exists
        guard FileManager.default.fileExists(atPath: url.path) else {
            throw ModelError.modelNotFound
        }

        // Check file size
        do {
            let attributes = try FileManager.default.attributesOfItem(atPath: url.path)
            if let fileSize = attributes[.size] as? UInt64 {
                let minSize = UInt64(Double(Self.expectedModelSize) * (1 - Self.modelSizeTolerance))
                let maxSize = UInt64(Double(Self.expectedModelSize) * (1 + Self.modelSizeTolerance))

                if fileSize < minSize || fileSize > maxSize {
                    print("ModelManager: File size \(fileSize) outside expected range [\(minSize), \(maxSize)]")
                    throw ModelError.modelCorrupted
                }

                print("ModelManager: Model file verified, size: \(fileSize) bytes")
            }
        } catch let error as ModelError {
            throw error
        } catch {
            throw ModelError.unknown("Failed to verify model: \(error.localizedDescription)")
        }
    }
}

// MARK: - Memory Pressure Handling

extension ModelManager {
    /// Register for memory pressure notifications
    func registerForMemoryWarnings() {
        NotificationCenter.default.addObserver(
            forName: UIApplication.didReceiveMemoryWarningNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.handleMemoryWarning()
        }
    }

    /// Handle memory pressure by unloading model if needed
    private func handleMemoryWarning() {
        print("ModelManager: Received memory warning")

        // Unload model to free memory
        if isModelLoaded {
            unloadModel()
            print("ModelManager: Model unloaded due to memory pressure")
        }
    }
}

// MARK: - Model Info

extension ModelManager {
    /// Model information for display
    struct ModelInfo {
        let name: String
        let version: String
        let size: String
        let quantization: String
        let contextLength: Int

        static let phi3Mini = ModelInfo(
            name: "Phi-3 Mini",
            version: "4k-instruct",
            size: "2.4 GB",
            quantization: "Q4_K_M",
            contextLength: 4096
        )
    }

    /// Get info about the bundled model
    static let modelInfo = ModelInfo.phi3Mini
}
