import Foundation
import UIKit

// MARK: - Device Capability

/// Utility for detecting device capabilities for on-device LLM inference
/// Requires iPhone 15 Pro or later (A17 Pro chip, 8GB RAM) for local LLM support
enum DeviceCapability {

    // MARK: - Device Detection

    /// Model identifiers for supported devices (iPhone 15 Pro and later)
    /// Reference: https://iosref.com/ram-processor
    private static let supportedModelIdentifiers: Set<String> = [
        // iPhone 15 Pro (A17 Pro, 8GB RAM)
        "iPhone16,1",
        // iPhone 15 Pro Max (A17 Pro, 8GB RAM)
        "iPhone16,2",
        // iPhone 16 (A18, 8GB RAM)
        "iPhone17,3",
        "iPhone17,4",
        // iPhone 16 Pro (A18 Pro, 8GB RAM)
        "iPhone17,1",
        // iPhone 16 Pro Max (A18 Pro, 8GB RAM)
        "iPhone17,2",
        // Future devices with 8GB+ RAM will need to be added
    ]

    /// Minimum RAM required for LLM inference (in bytes)
    /// Phi-3-mini Q4_K_M needs ~2.4GB for model + inference overhead
    private static let minimumRAMBytes: UInt64 = 6 * 1024 * 1024 * 1024 // 6GB minimum

    // MARK: - Public API

    /// Returns true if the device supports on-device LLM inference
    static var supportsLocalLLM: Bool {
        // Check model identifier
        let modelId = modelIdentifier
        let isKnownSupported = supportedModelIdentifiers.contains(modelId)

        // Also check RAM as a fallback for future devices
        let hasEnoughRAM = physicalMemory >= minimumRAMBytes

        // For known devices, trust the identifier
        // For unknown devices, require sufficient RAM
        if isKnownSupported {
            return true
        }

        // Allow unknown devices with 8GB+ RAM (future-proofing)
        return hasEnoughRAM && physicalMemory >= 8 * 1024 * 1024 * 1024
    }

    /// Returns the device model identifier (e.g., "iPhone16,1")
    static var modelIdentifier: String {
        var systemInfo = utsname()
        uname(&systemInfo)
        let machineMirror = Mirror(reflecting: systemInfo.machine)
        let identifier = machineMirror.children.reduce("") { identifier, element in
            guard let value = element.value as? Int8, value != 0 else { return identifier }
            return identifier + String(UnicodeScalar(UInt8(value)))
        }
        return identifier
    }

    /// Returns the human-readable device name
    static var deviceName: String {
        mapToDeviceName(identifier: modelIdentifier)
    }

    /// Returns total physical memory in bytes
    static var physicalMemory: UInt64 {
        ProcessInfo.processInfo.physicalMemory
    }

    /// Returns physical memory in GB (formatted string)
    static var physicalMemoryGB: String {
        let gb = Double(physicalMemory) / (1024 * 1024 * 1024)
        return String(format: "%.1f GB", gb)
    }

    /// Returns available memory in bytes (approximate)
    static var availableMemory: UInt64 {
        var info = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size) / 4
        let result = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
            }
        }

        if result == KERN_SUCCESS {
            let used = info.resident_size
            return physicalMemory > used ? physicalMemory - used : 0
        }
        return 0
    }

    /// Checks if there's enough memory available for model loading
    /// Model requires ~2.5GB for Phi-3-mini Q4_K_M
    static var hasEnoughAvailableMemory: Bool {
        let modelSize: UInt64 = 3 * 1024 * 1024 * 1024 // 3GB buffer for safety
        return availableMemory >= modelSize
    }

    /// Returns why LLM is not supported (for error messages)
    static var unsupportedReason: String? {
        guard !supportsLocalLLM else { return nil }

        let modelId = modelIdentifier
        let ramGB = Double(physicalMemory) / (1024 * 1024 * 1024)

        if ramGB < 6 {
            return "Your device has \(String(format: "%.1f", ramGB))GB RAM. On-device AI requires at least 8GB RAM (iPhone 15 Pro or later)."
        }

        if modelId.hasPrefix("iPhone") {
            let name = mapToDeviceName(identifier: modelId)
            return "\(name) is not supported. On-device AI requires iPhone 15 Pro or later with the A17 Pro chip."
        }

        return "This device is not supported for on-device AI. Please use iPhone 15 Pro or later."
    }

    // MARK: - Device Name Mapping

    private static func mapToDeviceName(identifier: String) -> String {
        switch identifier {
        // iPhone 15 Series
        case "iPhone15,4": return "iPhone 15"
        case "iPhone15,5": return "iPhone 15 Plus"
        case "iPhone16,1": return "iPhone 15 Pro"
        case "iPhone16,2": return "iPhone 15 Pro Max"

        // iPhone 16 Series
        case "iPhone17,3", "iPhone17,4": return "iPhone 16"
        case "iPhone17,1": return "iPhone 16 Pro"
        case "iPhone17,2": return "iPhone 16 Pro Max"

        // iPhone 14 Series (not supported but for reference)
        case "iPhone14,7": return "iPhone 14"
        case "iPhone14,8": return "iPhone 14 Plus"
        case "iPhone15,2": return "iPhone 14 Pro"
        case "iPhone15,3": return "iPhone 14 Pro Max"

        // iPad Pro with M-series (could support LLM)
        case "iPad13,4", "iPad13,5", "iPad13,6", "iPad13,7": return "iPad Pro 11\" (3rd gen)"
        case "iPad13,8", "iPad13,9", "iPad13,10", "iPad13,11": return "iPad Pro 12.9\" (5th gen)"
        case "iPad14,3", "iPad14,4": return "iPad Pro 11\" (4th gen)"
        case "iPad14,5", "iPad14,6": return "iPad Pro 12.9\" (6th gen)"

        // Simulator
        case "x86_64", "arm64": return "Simulator"

        default:
            // Try to extract device family
            if identifier.hasPrefix("iPhone") {
                return "iPhone (Unknown Model)"
            } else if identifier.hasPrefix("iPad") {
                return "iPad (Unknown Model)"
            }
            return identifier
        }
    }
}

// MARK: - Chip Information

extension DeviceCapability {
    /// Returns the chip name for the current device
    static var chipName: String? {
        switch modelIdentifier {
        case "iPhone16,1", "iPhone16,2":
            return "A17 Pro"
        case "iPhone17,1", "iPhone17,2":
            return "A18 Pro"
        case "iPhone17,3", "iPhone17,4":
            return "A18"
        case "x86_64", "arm64":
            return "Apple Silicon (Simulator)"
        default:
            return nil
        }
    }

    /// Returns whether the device has a Neural Engine suitable for LLM
    static var hasNeuralEngine: Bool {
        // All supported devices have 16-core Neural Engine capable of 35+ TOPS
        supportsLocalLLM
    }

    /// Returns whether Metal GPU acceleration is available
    static var supportsMetalGPU: Bool {
        // All modern iOS devices support Metal
        true
    }
}

// MARK: - Debug Information

extension DeviceCapability {
    /// Returns a dictionary of device info for debugging
    static var debugInfo: [String: String] {
        [
            "Model Identifier": modelIdentifier,
            "Device Name": deviceName,
            "Chip": chipName ?? "Unknown",
            "Total RAM": physicalMemoryGB,
            "Supports Local LLM": supportsLocalLLM ? "Yes" : "No",
            "Has Neural Engine": hasNeuralEngine ? "Yes" : "No",
            "Metal GPU": supportsMetalGPU ? "Yes" : "No"
        ]
    }
}
