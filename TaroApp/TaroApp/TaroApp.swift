import SwiftUI

@main
struct TaroApp: App {
    @StateObject private var readingSession = ReadingSession()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(readingSession)
        }
    }
}
