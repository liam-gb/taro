import SwiftUI

struct ContentView: View {
    @EnvironmentObject var readingSession: ReadingSession

    var body: some View {
        NavigationStack {
            switch readingSession.state {
            case .selectingSpread:
                HomeView()
            case .enteringQuestion:
                QuestionInputView()
            case .shuffling:
                ShuffleView()
            case .selectingCards:
                CardSelectionView()
            case .generatingInterpretation:
                GeneratingView()
            case .displayingReading:
                ReadingView()
            }
        }
        .preferredColorScheme(.dark)
    }
}

#Preview {
    ContentView()
        .environmentObject(ReadingSession())
}
