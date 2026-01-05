import XCTest
@testable import TaroApp

final class GenerationConfigTests: XCTestCase {

    // MARK: - Default Configuration Tests

    func testDefaultConfigurationIsValid() {
        let config = GenerationConfig()
        XCTAssertTrue(config.isValid)
        XCTAssertTrue(config.validationErrors.isEmpty)
    }

    func testTarotReadingPresetIsValid() {
        let config = GenerationConfig.tarotReading
        XCTAssertTrue(config.isValid)
        XCTAssertEqual(config.temperature, 0.7)
        XCTAssertEqual(config.topP, 0.9)
        XCTAssertEqual(config.maxTokens, 768)
    }

    func testMysticalPresetIsValid() {
        let config = GenerationConfig.mystical
        XCTAssertTrue(config.isValid)
        XCTAssertEqual(config.temperature, 0.85)
        XCTAssertEqual(config.maxTokens, 1024)
    }

    func testPracticalPresetIsValid() {
        let config = GenerationConfig.practical
        XCTAssertTrue(config.isValid)
        XCTAssertEqual(config.temperature, 0.5)
    }

    func testQuickReadingPresetIsValid() {
        let config = GenerationConfig.quickReading
        XCTAssertTrue(config.isValid)
        XCTAssertEqual(config.maxTokens, 256)
        XCTAssertEqual(config.contextSize, 2048)
    }

    // MARK: - Validation Tests

    func testInvalidTemperatureTooHigh() {
        let config = GenerationConfig(temperature: 3.0)
        XCTAssertFalse(config.isValid)
        XCTAssertTrue(config.validationErrors.contains { $0.contains("Temperature") })
    }

    func testInvalidTemperatureNegative() {
        let config = GenerationConfig(temperature: -0.5)
        XCTAssertFalse(config.isValid)
    }

    func testInvalidTopPZero() {
        let config = GenerationConfig(topP: 0)
        XCTAssertFalse(config.isValid)
        XCTAssertTrue(config.validationErrors.contains { $0.contains("Top-P") })
    }

    func testInvalidTopPGreaterThanOne() {
        let config = GenerationConfig(topP: 1.5)
        XCTAssertFalse(config.isValid)
    }

    func testInvalidMaxTokensZero() {
        let config = GenerationConfig(maxTokens: 0)
        XCTAssertFalse(config.isValid)
        XCTAssertTrue(config.validationErrors.contains { $0.contains("Max tokens") })
    }

    func testInvalidMaxTokensTooHigh() {
        let config = GenerationConfig(maxTokens: 10000)
        XCTAssertFalse(config.isValid)
    }

    func testInvalidRepetitionPenaltyTooLow() {
        let config = GenerationConfig(repetitionPenalty: 0.5)
        XCTAssertFalse(config.isValid)
        XCTAssertTrue(config.validationErrors.contains { $0.contains("Repetition penalty") })
    }

    func testInvalidRepetitionPenaltyTooHigh() {
        let config = GenerationConfig(repetitionPenalty: 3.0)
        XCTAssertFalse(config.isValid)
    }

    func testInvalidContextSizeZero() {
        let config = GenerationConfig(contextSize: 0)
        XCTAssertFalse(config.isValid)
        XCTAssertTrue(config.validationErrors.contains { $0.contains("Context size") })
    }

    // MARK: - Codable Tests

    func testConfigEncodeDecode() throws {
        let original = GenerationConfig.mystical
        let encoder = JSONEncoder()
        let data = try encoder.encode(original)

        let decoder = JSONDecoder()
        let decoded = try decoder.decode(GenerationConfig.self, from: data)

        XCTAssertEqual(original, decoded)
    }

    // MARK: - Reading Style Tests

    func testReadingStyleConfigMapping() {
        XCTAssertEqual(ReadingStyle.balanced.config, GenerationConfig.tarotReading)
        XCTAssertEqual(ReadingStyle.mystical.config, GenerationConfig.mystical)
        XCTAssertEqual(ReadingStyle.practical.config, GenerationConfig.practical)
    }

    func testReadingStyleHasDescriptions() {
        for style in ReadingStyle.allCases {
            XCTAssertFalse(style.description.isEmpty)
            XCTAssertFalse(style.icon.isEmpty)
        }
    }
}

final class DeviceCapabilityTests: XCTestCase {

    // MARK: - Basic Tests

    func testModelIdentifierIsNotEmpty() {
        let identifier = DeviceCapability.modelIdentifier
        XCTAssertFalse(identifier.isEmpty)
    }

    func testDeviceNameIsNotEmpty() {
        let name = DeviceCapability.deviceName
        XCTAssertFalse(name.isEmpty)
    }

    func testPhysicalMemoryIsPositive() {
        let memory = DeviceCapability.physicalMemory
        XCTAssertGreaterThan(memory, 0)
    }

    func testPhysicalMemoryGBIsFormatted() {
        let memoryGB = DeviceCapability.physicalMemoryGB
        XCTAssertTrue(memoryGB.contains("GB"))
    }

    func testSupportsMetalGPU() {
        // All iOS devices support Metal
        XCTAssertTrue(DeviceCapability.supportsMetalGPU)
    }

    // MARK: - Debug Info Tests

    func testDebugInfoContainsAllKeys() {
        let info = DeviceCapability.debugInfo

        XCTAssertNotNil(info["Model Identifier"])
        XCTAssertNotNil(info["Device Name"])
        XCTAssertNotNil(info["Total RAM"])
        XCTAssertNotNil(info["Supports Local LLM"])
        XCTAssertNotNil(info["Metal GPU"])
    }

    // MARK: - Unsupported Reason Tests

    func testUnsupportedReasonNilWhenSupported() {
        // This test behavior depends on the actual device
        if DeviceCapability.supportsLocalLLM {
            XCTAssertNil(DeviceCapability.unsupportedReason)
        } else {
            XCTAssertNotNil(DeviceCapability.unsupportedReason)
        }
    }
}

final class ModelManagerTests: XCTestCase {

    // MARK: - Model Info Tests

    func testModelInfoIsConfigured() {
        let info = ModelManager.modelInfo
        XCTAssertEqual(info.name, "Phi-3 Mini")
        XCTAssertEqual(info.quantization, "Q4_K_M")
        XCTAssertEqual(info.contextLength, 4096)
    }

    func testModelFilenameIsConfigured() {
        XCTAssertFalse(ModelManager.modelFilename.isEmpty)
        XCTAssertEqual(ModelManager.modelExtension, "gguf")
    }

    // MARK: - Error Tests

    func testDeviceNotSupportedError() {
        let error = ModelManager.ModelError.deviceNotSupported("Test reason")
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("Test reason"))
        XCTAssertNotNil(error.recoverySuggestion)
    }

    func testModelNotFoundError() {
        let error = ModelManager.ModelError.modelNotFound
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("could not be found"))
    }

    func testModelCorruptedError() {
        let error = ModelManager.ModelError.modelCorrupted
        XCTAssertNotNil(error.errorDescription)
        XCTAssertNotNil(error.recoverySuggestion)
        XCTAssertTrue(error.recoverySuggestion!.contains("reinstall"))
    }

    func testInsufficientMemoryError() {
        let error = ModelManager.ModelError.insufficientMemory
        XCTAssertNotNil(error.errorDescription)
        XCTAssertNotNil(error.recoverySuggestion)
        XCTAssertTrue(error.recoverySuggestion!.contains("Close"))
    }

    // MARK: - State Tests

    func testModelStateIsReady() {
        XCTAssertFalse(ModelManager.ModelState.notLoaded.isReady)
        XCTAssertFalse(ModelManager.ModelState.checking.isReady)
        XCTAssertFalse(ModelManager.ModelState.loading(progress: 0.5).isReady)
        XCTAssertTrue(ModelManager.ModelState.loaded.isReady)
        XCTAssertFalse(ModelManager.ModelState.error(.modelNotFound).isReady)
    }

    func testModelStateIsLoading() {
        XCTAssertFalse(ModelManager.ModelState.notLoaded.isLoading)
        XCTAssertTrue(ModelManager.ModelState.checking.isLoading)
        XCTAssertTrue(ModelManager.ModelState.loading(progress: 0.5).isLoading)
        XCTAssertFalse(ModelManager.ModelState.loaded.isLoading)
        XCTAssertFalse(ModelManager.ModelState.error(.modelNotFound).isLoading)
    }
}

final class LLMServiceTests: XCTestCase {

    // MARK: - Error Tests

    func testModelNotLoadedError() {
        let error = LLMService.LLMError.modelNotLoaded
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("not ready"))
    }

    func testGenerationFailedError() {
        let error = LLMService.LLMError.generationFailed("Test failure")
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("Test failure"))
    }

    func testCancelledError() {
        let error = LLMService.LLMError.cancelled
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("cancelled"))
    }

    func testInvalidInputError() {
        let error = LLMService.LLMError.invalidInput
        XCTAssertNotNil(error.errorDescription)
    }

    func testContextOverflowError() {
        let error = LLMService.LLMError.contextOverflow
        XCTAssertNotNil(error.errorDescription)
        XCTAssertTrue(error.errorDescription!.contains("too long"))
    }

    // MARK: - Availability Tests

    @MainActor
    func testIsAvailableMatchesDeviceCapability() {
        let service = LLMService.shared
        XCTAssertEqual(service.isAvailable, DeviceCapability.supportsLocalLLM)
    }
}
