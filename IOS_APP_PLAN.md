# Taro iOS App - Implementation Plan

## Overview

Native Swift iOS app with on-device LLM for private, offline tarot readings. Key innovation: **prompt optimization through strategic pre-calculation** to minimize local LLM workload.

---

## The Combinatorial Challenge

### Why We Can't Pre-Calculate Everything

| Spread | Cards | Positions | With Reversals | Total Combinations |
|--------|-------|-----------|----------------|-------------------|
| Daily Draw | 1 | 1 | 78 × 2 | 156 |
| 3-Card | 3 | 3 | 78P3 × 2³ | ~3.5 million |
| Horseshoe | 7 | 7 | 78P7 × 2⁷ | ~1.2 trillion |
| Celtic Cross | 10 | 10 | 78P10 × 2¹⁰ | ~10 quintillion |

**Conclusion**: Full reading pre-calculation is impossible. We need a smarter approach.

---

## Prompt Optimization Strategy

### The "Atomic Building Blocks" Approach

Instead of generating full readings, we pre-calculate **atomic pieces** that the local LLM combines:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRE-CALCULATED (Bundled)                      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Card Meanings (156 items)                             │
│  ├── 78 cards × 2 orientations                                  │
│  └── Rich, poetic interpretations per card                      │
│                                                                  │
│  Layer 2: Position Meanings (~24 items)                         │
│  ├── What each position represents per spread                   │
│  └── How to interpret a card in that position                   │
│                                                                  │
│  Layer 3: Card-in-Position Snippets (~3,744 items)              │
│  ├── 78 cards × 2 orientations × 24 positions                   │
│  └── "The Fool in the 'Challenge' position suggests..."         │
│                                                                  │
│  Layer 4: Notable Combinations (~200 items)                     │
│  ├── Two-card pairings with special meanings                    │
│  └── Death + Star = "Hope after endings"                        │
│                                                                  │
│  Layer 5: Elemental Dynamics (16 items)                         │
│  ├── Fire+Water, Air+Earth, etc.                                │
│  └── "Tension between passion and emotion"                      │
│                                                                  │
│  Layer 6: Spread Narrative Templates (5 items)                  │
│  ├── Story arc structure for each spread type                   │
│  └── "Your Celtic Cross reveals a journey from X to Y..."       │
│                                                                  │
│  Layer 7: Thematic Connectors (~50 items)                       │
│  ├── Transition phrases for card-to-card flow                   │
│  └── "This energy flows into...", "Contrasting this..."         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 LOCAL LLM ROLE (Runtime)                         │
├─────────────────────────────────────────────────────────────────┤
│  1. SELECT relevant pre-calculated blocks                        │
│  2. WEAVE them into coherent narrative                          │
│  3. PERSONALIZE based on user's question                        │
│  4. SYNTHESIZE overall theme/message                            │
│  5. GENERATE closing insight (small creative task)              │
└─────────────────────────────────────────────────────────────────┘
```

### Storage Estimate

| Layer | Items | Avg Size | Total |
|-------|-------|----------|-------|
| Card Meanings | 156 | 500 bytes | 78 KB |
| Position Meanings | 24 | 300 bytes | 7 KB |
| Card-in-Position | 3,744 | 200 bytes | 750 KB |
| Combinations | 200 | 150 bytes | 30 KB |
| Elemental | 16 | 200 bytes | 3 KB |
| Templates | 5 | 1 KB | 5 KB |
| Connectors | 50 | 100 bytes | 5 KB |
| **Total** | | | **~900 KB** |

This is trivial storage for rich, pre-generated content.

---

## Prompt Architecture

### Current Approach (Web App)
```
[Full system prompt with all tarot knowledge]
[Card definitions]
[Position meanings]
[User's reading]
[Request for interpretation]

→ External LLM generates everything
→ ~4000+ tokens input, ~1000+ tokens output
```

### Optimized Approach (iOS App)
```
[Minimal system prompt: "You are weaving a tarot reading"]
[Pre-calculated card-in-position text for THIS reading]
[Pre-calculated relevant combinations found]
[Elemental summary for THIS spread]
[User's question]
[Template structure for THIS spread type]

→ Local LLM weaves and personalizes
→ ~800 tokens input, ~400 tokens output
```

### Example: 3-Card Reading

**Before (what we send to Claude now):**
```markdown
# Full tarot instruction manual (2000 tokens)
# All 78 card meanings (massive)
# User's reading: The Fool (Past), Death (Present), The Star (Future)
# Please interpret...
```

**After (what local LLM receives):**
```markdown
You are crafting a tarot reading. Weave these elements into a
cohesive narrative addressing the seeker's question.

QUESTION: "Should I change careers?"

PAST - The Fool (Upright):
"In your past position, The Fool speaks to a time of beginnings
and innocent leaps. You approached this situation with fresh eyes,
perhaps naively, but with genuine openness to possibility."

PRESENT - Death (Upright):
"Death in your present indicates profound transformation is
actively occurring. Something must end for renewal to begin.
This is not loss but metamorphosis."

FUTURE - The Star (Upright):
"The Star illuminating your future promises hope and healing
after this transition. Your authentic path is revealing itself."

NOTABLE: Death → Star is the "Hope After Endings" combination,
signifying that current struggles lead directly to renewal.

ELEMENTAL FLOW: Air (Fool) → Water (Death) → Water (Star)
Thoughts give way to deep emotional transformation.

Weave these into 3-4 paragraphs. End with actionable insight.
```

The local LLM now has a **much easier job** - synthesis, not generation.

---

## Technical Architecture

### Tech Stack

```
┌─────────────────────────────────────────────────┐
│                   UI Layer                       │
│              SwiftUI + Animations                │
│    (Cards, Spreads, Shuffle, Reading Display)   │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│               Reading Engine                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Card Drawer │  │ Spread Mgr  │  │ Shuffle │ │
│  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│            Prompt Assembly Engine                │
│  ┌─────────────────────────────────────────────┐│
│  │ 1. Fetch card-in-position snippets          ││
│  │ 2. Detect & fetch relevant combinations     ││
│  │ 3. Calculate elemental dynamics             ││
│  │ 4. Select spread narrative template         ││
│  │ 5. Inject user question                     ││
│  │ 6. Assemble optimized prompt                ││
│  └─────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              Local LLM Engine                    │
│         llama.cpp / MLX Swift                    │
│  ┌─────────────────────────────────────────────┐│
│  │  Model: Phi-3-mini-4k (Q4 quantized)        ││
│  │  Size: ~2GB                                  ││
│  │  Context: 4096 tokens                        ││
│  │  Speed: ~15-30 tokens/sec on iPhone 15 Pro  ││
│  └─────────────────────────────────────────────┘│
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│             Pre-calculated Data                  │
│              (Bundled JSON/SQLite)               │
│  cards.json | positions.json | combinations.json│
└─────────────────────────────────────────────────┘
```

### Model Options

| Model | Size (Q4) | Quality | Speed (iPhone 15 Pro) |
|-------|-----------|---------|----------------------|
| Phi-3-mini-4k | 2.0 GB | Good | ~25 tok/s |
| Gemma-2B | 1.5 GB | Decent | ~30 tok/s |
| TinyLlama-1.1B | 0.6 GB | Basic | ~50 tok/s |
| Mistral-7B | 4.0 GB | Excellent | ~10 tok/s |

**Recommendation**: Start with **Phi-3-mini** - best quality/size/speed balance.

---

## Pre-Calculation Generation Plan

### Phase 1: Expand Existing Data

We already have in `interpretations.js`:
- 78 card meanings (upright + reversed)
- Keywords per card

**Need to generate:**
```javascript
// card-in-position snippets
{
  "the-fool": {
    "upright": {
      "celtic-past": "In your distant past, The Fool speaks to...",
      "celtic-present": "The Fool crossing your present suggests...",
      "celtic-challenge": "As your challenge, The Fool indicates...",
      // ... all 24 positions
    },
    "reversed": {
      // same structure
    }
  }
}
```

### Phase 2: Generate via Claude API

Script to generate all card-in-position combinations:
```python
for card in cards:  # 78
    for orientation in ['upright', 'reversed']:  # 2
        for position in positions:  # 24
            prompt = f"""
            Write a 2-3 sentence interpretation snippet for:
            Card: {card['name']} ({orientation})
            Position: {position['name']} - {position['meaning']}
            Spread: {position['spread']}

            Style: Second person, mystical but accessible.
            Focus on what this card means specifically in this position.
            """
            # Generate and store
```

**Cost estimate**: ~3,744 API calls × ~200 tokens = ~750K tokens ≈ $2-3

### Phase 3: Combination Expansion

Expand from current 18 combinations to ~200 meaningful pairings:
- All Major Arcana pairs with special meaning
- Cross-suit thematic pairs
- Sequential card meanings (when cards appear in order)

### Phase 4: Quality Refinement

- Human review of generated content
- Consistency pass for tone/style
- A/B testing different phrasings

---

## App Features

### Core Features (MVP)

1. **Card Drawing & Spreads**
   - All 5 spread types from web app
   - Beautiful 3D card animations (port from React)
   - Shuffle interaction

2. **On-Device Interpretation**
   - Local LLM generates readings
   - No internet required
   - Complete privacy

3. **Question Input**
   - Optional question before reading
   - Question influences interpretation

4. **Reading History**
   - Save past readings locally
   - Journal/notes per reading

### Enhanced Features (v1.1+)

5. **Daily Notification**
   - Morning card pull reminder
   - Widget showing daily card

6. **Deck Customization**
   - Major Arcana only toggle
   - Reversed cards toggle

7. **Themes**
   - Dark/Light mode
   - Different card back designs

8. **iCloud Sync**
   - Reading history across devices

---

## Development Phases (PR Tracking)

Each phase maps to a separate Pull Request for incremental progress tracking.

---

### PR #1: iOS Foundation & Data Models
**Status:** `COMPLETE`
**Branch:** `claude/plan-ios-migration-3Pnze`
**Dependencies:** None (starting point)

- [x] Pre-calculated data exists (`ios-precalc/`)
- [x] Xcode project structure created
- [x] Swift data models: `Card.swift`, `Spread.swift`, `Position.swift`, `Reading.swift`
- [x] Static data ported to Swift (`CardDeck.swift` with all 78 cards)
- [x] Basic SwiftUI app entry point (`TaroApp.swift`)
- [x] Navigation placeholder views (Home, Question, Shuffle, CardSelection, Generating, Reading)

**Deliverable:** Compiles, shows basic navigation between placeholder screens.

---

### PR #2: Pre-calculated Data Integration
**Status:** `PENDING`
**Dependencies:** PR #1

- [ ] JSON data loading service (`DataService.swift`)
- [ ] Import `base-meanings.json` into app bundle
- [ ] Import `position-modifiers.json` into app bundle
- [ ] Import `combinations.json` into app bundle
- [ ] Unit tests for data loading
- [ ] Swift models for interpretation data

**Deliverable:** All pre-calculated tarot data accessible in Swift.

---

### PR #3: Core UI Framework
**Status:** `PENDING`
**Dependencies:** PR #1

- [ ] Theme system (colors, typography, spacing)
- [ ] Aurora gradient background component
- [ ] Glass panel/card component
- [ ] Custom button styles
- [ ] Dark mode support

**Deliverable:** Consistent visual language matching web app aesthetic.

---

### PR #4: Card UI & Animations
**Status:** `PENDING`
**Dependencies:** PR #3

- [ ] 3D card component (`Card3DView.swift`)
- [ ] Card flip animation
- [ ] Card back design
- [ ] Hover/selection states
- [ ] Shuffle animation
- [ ] Fan-out card selection interaction

**Deliverable:** Interactive, animated tarot cards.

---

### PR #5: Spread Selection & Layout
**Status:** `PENDING`
**Dependencies:** PR #4

- [ ] Spread selection view with all 5 spread types
- [ ] Spread layout engine (positions for each spread)
- [ ] Celtic Cross layout (overlapping cards)
- [ ] Card placement animations
- [ ] Question input modal

**Deliverable:** User can select spread, optionally enter question, draw cards.

---

### PR #6: LLM Integration
**Status:** `PENDING`
**Dependencies:** PR #2

- [ ] Integrate llama.cpp or MLX Swift
- [ ] Model download/management system
- [ ] `LLMService.swift` - load model, run inference
- [ ] Streaming token output
- [ ] Generation parameters (temperature, top-p)
- [ ] Memory management for model

**Deliverable:** Can run local LLM inference on device.

---

### PR #7: Prompt Assembly & Reading Flow
**Status:** `PENDING`
**Dependencies:** PR #5, PR #6

- [ ] `PromptAssembler.swift` - build prompts from pre-calc data
- [ ] Combination detection (find notable pairings in spread)
- [ ] Elemental flow calculation
- [ ] Reading display view with streaming text
- [ ] Reading state management

**Deliverable:** Complete end-to-end reading experience.

---

### PR #8: History & Persistence
**Status:** `PENDING`
**Dependencies:** PR #7

- [ ] Core Data schema for readings
- [ ] `HistoryService.swift` - save/load readings
- [ ] History list view
- [ ] Reading detail view (view past readings)
- [ ] Delete/manage readings
- [ ] Optional iCloud sync

**Deliverable:** Readings persist across app launches.

---

### PR #9: Polish & App Store
**Status:** `PENDING`
**Dependencies:** PR #8

- [ ] App icon (all sizes)
- [ ] Launch screen
- [ ] App Store screenshots
- [ ] App Store description
- [ ] Privacy policy (no data collection!)
- [ ] TestFlight distribution
- [ ] Final App Store submission

**Deliverable:** Published app in App Store.

---

## Pre-Calculation Status

The pre-calculated data generation is **COMPLETE**:

| Layer | Status | File |
|-------|--------|------|
| Card Meanings | COMPLETE | `ios-precalc/base-meanings.json` (40KB) |
| Position Modifiers | COMPLETE | `ios-precalc/position-modifiers.json` (431KB) |
| Card Combinations | COMPLETE | `ios-precalc/combinations.json` (19KB) |
| Elemental Dynamics | PENDING | Needs generation |
| Spread Templates | PENDING | Needs generation |
| Thematic Connectors | PENDING | Needs generation |

---

## Legacy Development Phases (Reference)

### Phase 0: Pre-Calculation Sprint
- [x] Generate card-in-position snippets via Claude API
- [x] Base meanings for all 78 cards
- [x] Position modifiers for all positions
- [x] Card combinations database
- [ ] Generate elemental dynamics content
- [ ] Create spread narrative templates
- [ ] Generate thematic connectors

### Phase 1: iOS Foundation
- [ ] Xcode project setup
- [ ] SwiftUI app structure
- [ ] Port card data models
- [ ] Port spread configurations
- [ ] Basic navigation flow

### Phase 2: Card UI
- [ ] 3D card component in SwiftUI
- [ ] Card flip animations
- [ ] Shuffle animation
- [ ] Fan-out card selection
- [ ] Spread layout views

### Phase 3: LLM Integration
- [ ] Integrate llama.cpp or MLX Swift
- [ ] Model loading/management
- [ ] Prompt assembly engine
- [ ] Streaming text display
- [ ] Generation settings (temperature, etc.)

### Phase 4: Reading Flow
- [ ] Complete reading experience
- [ ] Question input
- [ ] Reading display
- [ ] Copy/share functionality

### Phase 5: Polish & Submit
- [ ] Reading history (Core Data)
- [ ] App icons & launch screen
- [ ] App Store assets
- [ ] TestFlight beta
- [ ] App Store submission

---

## File Structure

```
TaroApp/
├── TaroApp.swift                 # App entry point
├── Models/
│   ├── Card.swift                # Card model
│   ├── Spread.swift              # Spread configurations
│   ├── Reading.swift             # Reading state
│   └── Position.swift            # Position in spread
├── Views/
│   ├── HomeView.swift            # Main menu
│   ├── SpreadSelectionView.swift # Choose spread
│   ├── ShuffleView.swift         # Shuffle interaction
│   ├── CardSelectionView.swift   # Draw cards
│   ├── ReadingView.swift         # Display reading
│   └── Components/
│       ├── Card3DView.swift      # 3D card with flip
│       ├── CardBackView.swift    # Card back design
│       ├── GlassPanel.swift      # Frosted glass effect
│       └── AuroraBackground.swift # Animated background
├── Services/
│   ├── LLMService.swift          # Local LLM interface
│   ├── PromptAssembler.swift     # Build optimized prompts
│   ├── ReadingEngine.swift       # Core reading logic
│   └── HistoryService.swift      # Persist readings
├── Data/
│   ├── cards.json                # Card definitions
│   ├── interpretations.json      # Pre-calc meanings
│   ├── positions.json            # Card-in-position snippets
│   ├── combinations.json         # Notable pairings
│   └── templates.json            # Narrative templates
├── Resources/
│   ├── Models/                   # LLM model files
│   │   └── phi-3-mini-q4.gguf
│   └── Assets.xcassets           # Images, icons
└── Tests/
    └── ...
```

---

## Costs Summary

| Item | Cost | Frequency |
|------|------|-----------|
| Apple Developer Program | $99 | Annual |
| Pre-calculation API calls | ~$3 | One-time |
| Development time | Your time | One-time |
| **Total to launch** | **~$102** | |

---

## Open Questions

1. **Model download strategy**: Bundle with app (larger initial download) or download on first launch?
2. **Fallback**: Offer external API option for older/slower devices?
3. **Monetization**: Free with ads? One-time purchase? Subscription?
4. **Card artwork**: Use existing public domain? Commission custom art?

---

## Next Steps

1. **Approve this plan** - any adjustments needed?
2. **Begin pre-calculation sprint** - generate card-in-position content
3. **Set up Xcode project** - basic SwiftUI structure
4. **Prototype LLM integration** - test Phi-3 on device

---

*This plan optimizes for a delightful, private, offline tarot experience that works well within the constraints of on-device LLM inference.*
