import SwiftUI

@main
struct TaroApp: App {
    @StateObject private var readingSession = ReadingSession()
    @StateObject private var modelManager = ModelManager.shared
    @StateObject private var llmService = LLMService.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(readingSession)
                .environmentObject(modelManager)
                .environmentObject(llmService)
                .task {
                    await initializeLLM()
                }
        }
    }

    /// Initialize the LLM service on supported devices
    private func initializeLLM() async {
        // Check if device supports local LLM
        guard DeviceCapability.supportsLocalLLM else {
            print("TaroApp: Device does not support local LLM (\(DeviceCapability.deviceName))")
            return
        }

        // Register for memory warnings
        modelManager.registerForMemoryWarnings()

        // Load the model
        do {
            try await modelManager.loadModel()
            print("TaroApp: LLM model loaded successfully")
        } catch {
            print("TaroApp: Failed to load LLM model: \(error)")
        }
    }
}
