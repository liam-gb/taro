import Foundation

// MARK: - Generation Configuration

/// Configuration for LLM text generation
struct GenerationConfig: Codable, Equatable {
    /// Controls randomness in generation (0.0 = deterministic, 1.0 = very random)
    let temperature: Float

    /// Nucleus sampling - only consider tokens with cumulative probability up to this value
    let topP: Float

    /// Maximum number of tokens to generate
    let maxTokens: Int

    /// Penalty for repeating tokens (1.0 = no penalty, >1.0 = discourage repetition)
    let repetitionPenalty: Float

    /// Number of threads for inference (0 = auto-detect)
    let threadCount: Int

    /// Whether to use Metal GPU acceleration
    let useGPU: Bool

    /// Context window size
    let contextSize: Int

    // MARK: - Initialization

    init(
        temperature: Float = 0.7,
        topP: Float = 0.9,
        maxTokens: Int = 512,
        repetitionPenalty: Float = 1.1,
        threadCount: Int = 0,
        useGPU: Bool = true,
        contextSize: Int = 4096
    ) {
        self.temperature = temperature
        self.topP = topP
        self.maxTokens = maxTokens
        self.repetitionPenalty = repetitionPenalty
        self.threadCount = threadCount
        self.useGPU = useGPU
        self.contextSize = contextSize
    }
}

// MARK: - Preset Configurations

extension GenerationConfig {
    /// Default configuration for tarot readings - balanced creativity and coherence
    static let tarotReading = GenerationConfig(
        temperature: 0.7,
        topP: 0.9,
        maxTokens: 768,
        repetitionPenalty: 1.1,
        threadCount: 0,
        useGPU: true,
        contextSize: 4096
    )

    /// More creative/mystical readings - higher temperature for varied output
    static let mystical = GenerationConfig(
        temperature: 0.85,
        topP: 0.95,
        maxTokens: 1024,
        repetitionPenalty: 1.15,
        threadCount: 0,
        useGPU: true,
        contextSize: 4096
    )

    /// Direct/practical readings - lower temperature for more focused output
    static let practical = GenerationConfig(
        temperature: 0.5,
        topP: 0.8,
        maxTokens: 512,
        repetitionPenalty: 1.05,
        threadCount: 0,
        useGPU: true,
        contextSize: 4096
    )

    /// Quick single-card readings - shorter output
    static let quickReading = GenerationConfig(
        temperature: 0.65,
        topP: 0.85,
        maxTokens: 256,
        repetitionPenalty: 1.1,
        threadCount: 0,
        useGPU: true,
        contextSize: 2048
    )
}

// MARK: - Validation

extension GenerationConfig {
    /// Validates the configuration parameters
    var isValid: Bool {
        temperature >= 0 && temperature <= 2.0 &&
        topP > 0 && topP <= 1.0 &&
        maxTokens > 0 && maxTokens <= 4096 &&
        repetitionPenalty >= 1.0 && repetitionPenalty <= 2.0 &&
        threadCount >= 0 &&
        contextSize > 0 && contextSize <= 4096
    }

    /// Returns validation errors if any
    var validationErrors: [String] {
        var errors: [String] = []

        if temperature < 0 || temperature > 2.0 {
            errors.append("Temperature must be between 0.0 and 2.0")
        }
        if topP <= 0 || topP > 1.0 {
            errors.append("Top-P must be between 0.0 and 1.0")
        }
        if maxTokens <= 0 || maxTokens > 4096 {
            errors.append("Max tokens must be between 1 and 4096")
        }
        if repetitionPenalty < 1.0 || repetitionPenalty > 2.0 {
            errors.append("Repetition penalty must be between 1.0 and 2.0")
        }
        if contextSize <= 0 || contextSize > 4096 {
            errors.append("Context size must be between 1 and 4096")
        }

        return errors
    }
}

// MARK: - Reading Style

/// Predefined reading styles that map to generation configurations
enum ReadingStyle: String, CaseIterable, Codable {
    case balanced = "Balanced"
    case mystical = "Mystical"
    case practical = "Practical"

    var config: GenerationConfig {
        switch self {
        case .balanced:
            return .tarotReading
        case .mystical:
            return .mystical
        case .practical:
            return .practical
        }
    }

    var description: String {
        switch self {
        case .balanced:
            return "A harmonious blend of intuition and clarity"
        case .mystical:
            return "Deep symbolic interpretations with poetic language"
        case .practical:
            return "Direct, actionable guidance for everyday decisions"
        }
    }

    var icon: String {
        switch self {
        case .balanced:
            return "yin.yang"
        case .mystical:
            return "moon.stars"
        case .practical:
            return "lightbulb"
        }
    }
}
