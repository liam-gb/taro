# Implement Phase 2: llama.cpp Integration & Copy Prompt for Unsupported Devices

Complete the on-device LLM integration. Phase 1 established the service architecture (`LLMService`, `ModelManager`, `DeviceCapability`, `GenerationConfig`)—now implement the real inference pipeline and UX for unsupported devices.

---

## What to Build

### 1. Copy Prompt Feature for Unsupported Devices (Priority)

For devices that don't support on-device LLM (pre-iPhone 15 Pro), users should see a **"Copy prompt to paste in AI chat of your choice"** button instead of auto-generating a fallback reading.

**Create `Views/Components/CopyPromptSheet.swift`:**
- Sheet UI with mystical glass styling (use existing `GlassPanel`, `GlowingButton`, etc.)
- Shows scrollable preview of the generated prompt
- "Copy Prompt" button that copies to clipboard with haptic feedback
- Shows "Copied!" confirmation after successful copy
- "Continue with Basic Reading" secondary option for template fallback
- Dismiss button in navigation bar

**Update `Views/GeneratingView.swift`:**
- Add `@State private var showCopyPromptSheet = false`
- Add `unsupportedDeviceActions` computed property showing the copy prompt panel
- Add `generateExternalAIPrompt()` method that builds a prompt containing:
  - User's question (if provided)
  - All drawn cards with position, name, orientation (upright/reversed)
  - Card keywords and base meanings from DataService
  - Card combinations if any
  - Elemental balance summary
  - Request for cohesive interpretation
- Update `startGeneration()` to NOT auto-generate for unsupported devices—let user choose action
- Add `.sheet(isPresented: $showCopyPromptSheet)` modifier

### 2. llama.cpp Swift Package Integration

**Add SPM dependency:**
- Package: `https://github.com/StanfordBDHG/llama.cpp`
- Version: `.upToNextMinor(from: "0.1.0")`
- Enable C++ interoperability in build settings

**Create `Services/LlamaContext.swift`:**
- Swift wrapper around llama.cpp context
- Safe memory management (model/context lifecycle)
- `init(modelPath:config:)` - loads model with GPU layers
- `generate(prompt:onToken:)` - streaming token generation
- Proper cleanup in `deinit`
- `LlamaError` enum for error handling

### 3. Connect LLMService to Real Inference

**Update `Services/LLMService.swift`:**
- Add `private var llamaContext: LlamaContext?`
- Replace `simulateGeneration()` with real llama.cpp inference
- Use `LlamaContext.generate()` for streaming tokens
- Add context cleanup in `unloadModel()`

**Update `Services/ModelManager.swift`:**
- Replace simulated loading with actual model initialization
- Pre-warm model optionally for faster first inference

### 4. Bundle the Model

**Model to use:** `Phi-3-mini-4k-instruct-q4.gguf` (~2.39 GB)
- Download from: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
- Add to Xcode project resources (NOT to git)
- Add `*.gguf` to `.gitignore`

---

## Acceptance Criteria

### Copy Prompt (Task 6)
- [ ] Unsupported devices see "Copy Prompt for AI Chat" button (not auto-fallback)
- [ ] Prompt copies to clipboard with haptic feedback
- [ ] "Copied!" confirmation animates after copy
- [ ] Prompt includes: question, cards, positions, meanings, combinations, elemental flow
- [ ] "Use Basic Reading" option still available as secondary action
- [ ] Sheet styling matches app's mystical glass aesthetic

### llama.cpp Integration (Tasks 1-5)
- [ ] `import llama` compiles without errors
- [ ] Model loads from bundle successfully
- [ ] Streaming tokens appear in GeneratingView
- [ ] Cancellation stops generation immediately
- [ ] Memory properly freed when unloading

### Performance (Task 7)
- [ ] First token < 2 seconds
- [ ] Generation speed: 8+ tokens/second
- [ ] Memory peak < 4GB during inference

---

## Files to Modify/Create

**Create:**
- `Views/Components/CopyPromptSheet.swift`
- `Services/LlamaContext.swift`

**Modify:**
- `Views/GeneratingView.swift` (add copy prompt UI, external prompt generation)
- `Services/LLMService.swift` (connect to LlamaContext)
- `Services/ModelManager.swift` (real model loading)
- `.gitignore` (add *.gguf)

---

## Resources

- Stanford BDHG llama.cpp: https://github.com/StanfordBDHG/llama.cpp
- Phi-3 GGUF Models: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
- llama.cpp iOS example: https://github.com/ggml-org/llama.cpp/tree/master/examples/llama.swiftui

---

## Notes

- Use existing Theme.swift colors (`mysticViolet`, `deepSpace`, etc.) and components (`GlassPanel`, `GlowingButton`, `GlassButton`)
- Follow existing singleton patterns (see `DataService.shared`)
- The copy prompt feature should work even if llama.cpp integration isn't complete yet
- Test copy prompt on simulator (simulates unsupported device)
