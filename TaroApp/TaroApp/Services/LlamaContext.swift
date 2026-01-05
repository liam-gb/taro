import Foundation
import llama

// MARK: - Llama Errors

/// Errors that can occur during llama.cpp operations
enum LlamaError: LocalizedError {
    case modelNotFound(path: String)
    case failedToLoadModel
    case failedToCreateContext
    case failedToTokenize
    case failedToGenerate(String)
    case contextOverflow
    case cancelled
    case invalidConfiguration

    var errorDescription: String? {
        switch self {
        case .modelNotFound(let path):
            return "Model file not found at path: \(path)"
        case .failedToLoadModel:
            return "Failed to load the LLM model. The file may be corrupted."
        case .failedToCreateContext:
            return "Failed to create inference context. Try closing other apps."
        case .failedToTokenize:
            return "Failed to tokenize the input prompt."
        case .failedToGenerate(let reason):
            return "Generation failed: \(reason)"
        case .contextOverflow:
            return "Input is too long for the model's context window."
        case .cancelled:
            return "Generation was cancelled."
        case .invalidConfiguration:
            return "Invalid model configuration."
        }
    }
}

// MARK: - Llama Context Configuration

/// Configuration for the llama.cpp context
struct LlamaContextConfig {
    /// Number of tokens in the context window
    var contextSize: Int32 = 4096

    /// Number of layers to offload to GPU (0 = CPU only, -1 = all layers)
    var gpuLayers: Int32 = -1

    /// Number of threads to use for generation
    var threadCount: Int32 = 4

    /// Batch size for prompt processing
    var batchSize: Int32 = 512

    /// Whether to use memory mapping
    var useMemoryMap: Bool = true

    /// Whether to lock model in memory
    var useLockMemory: Bool = false

    static let `default` = LlamaContextConfig()

    /// Configuration optimized for iOS devices
    static let mobile = LlamaContextConfig(
        contextSize: 4096,
        gpuLayers: -1,  // Use Metal GPU
        threadCount: 4,
        batchSize: 512,
        useMemoryMap: true,
        useLockMemory: false
    )
}

// MARK: - Generation Parameters

/// Parameters for text generation
struct GenerationParameters {
    var temperature: Float = 0.7
    var topP: Float = 0.9
    var topK: Int32 = 40
    var repeatPenalty: Float = 1.1
    var maxTokens: Int32 = 2048

    static let `default` = GenerationParameters()

    static let creative = GenerationParameters(
        temperature: 0.9,
        topP: 0.95,
        topK: 50,
        repeatPenalty: 1.05,
        maxTokens: 2048
    )

    static let focused = GenerationParameters(
        temperature: 0.5,
        topP: 0.85,
        topK: 30,
        repeatPenalty: 1.15,
        maxTokens: 2048
    )
}

// MARK: - Llama Context

/// Swift wrapper around llama.cpp context for safe memory management and inference
final class LlamaContext: @unchecked Sendable {
    // MARK: - Private Properties

    private var model: OpaquePointer?
    private var context: OpaquePointer?
    private var sampler: OpaquePointer?
    private let config: LlamaContextConfig

    private var isCancelled = false
    private let lock = NSLock()

    // MARK: - Initialization

    /// Initialize the context with a model file
    /// - Parameters:
    ///   - modelPath: Path to the .gguf model file
    ///   - config: Context configuration
    init(modelPath: String, config: LlamaContextConfig = .mobile) throws {
        self.config = config

        // Verify file exists
        guard FileManager.default.fileExists(atPath: modelPath) else {
            throw LlamaError.modelNotFound(path: modelPath)
        }

        // Initialize llama backend
        llama_backend_init()

        // Load model
        var modelParams = llama_model_default_params()
        modelParams.n_gpu_layers = config.gpuLayers
        modelParams.use_mmap = config.useMemoryMap
        modelParams.use_mlock = config.useLockMemory

        guard let loadedModel = llama_load_model_from_file(modelPath, modelParams) else {
            throw LlamaError.failedToLoadModel
        }
        self.model = loadedModel

        // Create context
        var contextParams = llama_context_default_params()
        contextParams.n_ctx = UInt32(config.contextSize)
        contextParams.n_batch = UInt32(config.batchSize)
        contextParams.n_threads = UInt32(config.threadCount)
        contextParams.n_threads_batch = UInt32(config.threadCount)

        guard let ctx = llama_new_context_with_model(loadedModel, contextParams) else {
            llama_free_model(loadedModel)
            throw LlamaError.failedToCreateContext
        }
        self.context = ctx

        // Create sampler chain
        let samplerParams = llama_sampler_chain_default_params()
        self.sampler = llama_sampler_chain_init(samplerParams)

        print("LlamaContext: Model loaded successfully")
        print("LlamaContext: Context size: \(config.contextSize)")
        print("LlamaContext: GPU layers: \(config.gpuLayers)")
    }

    deinit {
        cleanup()
    }

    // MARK: - Public API

    /// Generate text from a prompt with streaming output
    /// - Parameters:
    ///   - prompt: The input prompt
    ///   - params: Generation parameters
    ///   - onToken: Callback for each generated token
    func generate(
        prompt: String,
        params: GenerationParameters = .default,
        onToken: @escaping (String) -> Void
    ) async throws {
        guard let model = model, let context = context else {
            throw LlamaError.failedToCreateContext
        }

        // Reset cancellation flag
        lock.lock()
        isCancelled = false
        lock.unlock()

        // Tokenize the prompt
        let tokens = try tokenize(prompt)

        guard tokens.count < config.contextSize else {
            throw LlamaError.contextOverflow
        }

        // Clear the KV cache
        llama_kv_cache_clear(context)

        // Process prompt in batches
        var batch = llama_batch_init(Int32(tokens.count), 0, 1)
        defer { llama_batch_free(batch) }

        // Fill the batch with prompt tokens
        for (i, token) in tokens.enumerated() {
            llama_batch_add(&batch, token, Int32(i), [0], false)
        }

        // Mark the last token for logits
        batch.logits[Int(batch.n_tokens) - 1] = 1

        // Decode the prompt
        let decodeResult = llama_decode(context, batch)
        if decodeResult != 0 {
            throw LlamaError.failedToGenerate("Failed to process prompt")
        }

        // Setup sampler for generation
        configureSampler(params: params)

        // Generate tokens
        var generatedCount: Int32 = 0
        var currentPos = Int32(tokens.count)

        while generatedCount < params.maxTokens {
            // Check for cancellation
            lock.lock()
            let cancelled = isCancelled
            lock.unlock()

            if cancelled {
                throw LlamaError.cancelled
            }

            try Task.checkCancellation()

            // Sample the next token
            let newToken = llama_sampler_sample(sampler, context, -1)

            // Check for end of generation
            if llama_token_is_eog(model, newToken) {
                break
            }

            // Convert token to text
            if let text = tokenToString(newToken) {
                onToken(text)
            }

            // Prepare batch for next token
            llama_batch_clear(&batch)
            llama_batch_add(&batch, newToken, currentPos, [0], true)

            // Decode
            let result = llama_decode(context, batch)
            if result != 0 {
                throw LlamaError.failedToGenerate("Failed to decode token")
            }

            currentPos += 1
            generatedCount += 1

            // Yield to allow other async work
            await Task.yield()
        }

        print("LlamaContext: Generated \(generatedCount) tokens")
    }

    /// Cancel any ongoing generation
    func cancel() {
        lock.lock()
        isCancelled = true
        lock.unlock()
    }

    /// Clean up resources
    func cleanup() {
        if let sampler = sampler {
            llama_sampler_free(sampler)
            self.sampler = nil
        }

        if let context = context {
            llama_free(context)
            self.context = nil
        }

        if let model = model {
            llama_free_model(model)
            self.model = nil
        }

        llama_backend_free()
        print("LlamaContext: Resources cleaned up")
    }

    // MARK: - Private Helpers

    private func tokenize(_ text: String) throws -> [llama_token] {
        guard let model = model else {
            throw LlamaError.failedToTokenize
        }

        let utf8 = text.utf8CString
        let maxTokens = Int32(utf8.count) + 128

        var tokens = [llama_token](repeating: 0, count: Int(maxTokens))

        let tokenCount = utf8.withUnsafeBufferPointer { buffer in
            llama_tokenize(
                model,
                buffer.baseAddress,
                Int32(utf8.count - 1), // Exclude null terminator
                &tokens,
                maxTokens,
                true,  // Add BOS
                true   // Special tokens
            )
        }

        if tokenCount < 0 {
            throw LlamaError.failedToTokenize
        }

        return Array(tokens.prefix(Int(tokenCount)))
    }

    private func tokenToString(_ token: llama_token) -> String? {
        guard let model = model else { return nil }

        var buffer = [CChar](repeating: 0, count: 64)
        let length = llama_token_to_piece(model, token, &buffer, Int32(buffer.count), 0, false)

        if length > 0 {
            return String(cString: buffer)
        }
        return nil
    }

    private func configureSampler(params: GenerationParameters) {
        guard let sampler = sampler else { return }

        // Clear existing samplers
        llama_sampler_reset(sampler)

        // Add temperature sampler
        llama_sampler_chain_add(sampler, llama_sampler_init_temp(params.temperature))

        // Add top-k sampler
        llama_sampler_chain_add(sampler, llama_sampler_init_top_k(params.topK))

        // Add top-p sampler
        llama_sampler_chain_add(sampler, llama_sampler_init_top_p(params.topP, 1))

        // Add repetition penalty (using DRY sampler for repeat penalty)
        llama_sampler_chain_add(sampler, llama_sampler_init_penalties(
            Int32(config.contextSize),  // penalty_last_n
            params.repeatPenalty,       // penalty_repeat
            0.0,                         // penalty_freq
            0.0                          // penalty_present
        ))

        // Add distribution sampler for final selection
        llama_sampler_chain_add(sampler, llama_sampler_init_dist(UInt32.random(in: 0...UInt32.max)))
    }
}

// MARK: - Model Info Extension

extension LlamaContext {
    /// Get information about the loaded model
    var modelInfo: (vocabSize: Int, contextSize: Int, embeddingSize: Int)? {
        guard let model = model else { return nil }

        return (
            vocabSize: Int(llama_n_vocab(model)),
            contextSize: Int(config.contextSize),
            embeddingSize: Int(llama_n_embd(model))
        )
    }
}
