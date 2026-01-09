"""
Coverage analysis for tarot training dataset.
Analyzes 40k examples across multiple dimensions.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# All 78 tarot cards
MAJOR_ARCANA = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]

SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
RANKS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]

MINOR_ARCANA = [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]
ALL_CARDS = MAJOR_ARCANA + MINOR_ARCANA

MOON_PHASES = [
    "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
    "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
]

QUESTION_CATEGORIES = ["love", "career", "growth", "health", "family", "money", "decisions"]

# Position IDs by spread type
SPREAD_POSITIONS = {
    "single": ["todays_guidance"],
    "threeCard": ["past", "present", "future"],
    "situation": ["situation", "action", "outcome"],
    "horseshoe": ["past", "present", "hidden_influences", "obstacles", "external", "advice", "outcome"],
    "celtic": ["present", "challenge", "past", "future", "above", "below", "advice", "external", "hopes_fears", "outcome"],
}

# Position display names to IDs
POSITION_NAME_TO_ID = {
    "Today's Guidance": "todays_guidance",
    "Past": "past",
    "Present": "present",
    "Future": "future",
    "Situation": "situation",
    "Action": "action",
    "Outcome": "outcome",
    "Hidden Influences": "hidden_influences",
    "Obstacles": "obstacles",
    "External Influences": "external",
    "External": "external",
    "Advice": "advice",
    "Challenge": "challenge",
    "Above": "above",
    "Below": "below",
    "Hopes/Fears": "hopes_fears",
}

# Questions from the prompt generator
QUESTIONS = {
    "love": [
        "Will I find love?", "Is my partner the one for me?", "Should I stay in my current relationship?",
        "How can I improve my relationship?", "What is blocking me from finding love?",
        "How does my partner really feel about me?", "Am I ready for a committed relationship?",
        "What do I need to learn from this relationship?", "How can I heal from my past heartbreak?",
        "What is the future of my relationship?", "What should I look for in a partner?",
        "Why do I keep attracting the wrong people?", "Am I ready to start dating again?",
        "What energy am I projecting in the dating world?", "How can I open myself up to new love?",
        "Is marriage in my future?", "What do I need to know before getting engaged?",
        "How can we reignite the spark in our marriage?", "What is the state of my marriage?",
        "Are we ready to take the next step together?", "How do I move on from this breakup?",
        "What lessons does this heartbreak hold for me?", "Will I be able to trust again?",
        "What do I need to release to heal my heart?", "How long will it take me to feel whole again?",
        "Is there real chemistry between us?", "What attracts my ideal partner to me?",
        "Why am I drawn to this person?", "What is the nature of our connection?",
        "Does this person have genuine feelings for me?", "Are we truly compatible?",
        "What challenges will we face together?", "Where do our values align and differ?",
        "Can we build a lasting future together?", "What does our relationship need to thrive?",
        "How can we communicate better?", "What is my partner not telling me?",
        "How can I express my needs more clearly?", "What is causing distance between us?",
        "How can I feel more connected to my partner?",
    ],
    "career": [
        "Should I change careers?", "Will I get the promotion?", "Is this job right for me?",
        "How can I advance in my career?", "Should I start my own business?",
        "What is blocking my career success?", "Is it time to quit my job?",
        "What career path should I pursue?", "How can I find more fulfillment at work?",
        "What's holding me back professionally?", "Should I accept this job offer?",
        "What opportunities are coming my way?", "Is this the right time for a career change?",
        "What should I know about this new position?", "Will this move benefit my career long-term?",
        "Is my business idea viable?", "What does my business need to succeed?",
        "Should I pursue this partnership?", "How can I grow my business?",
        "What risks should I be aware of?", "What work would truly fulfill me?",
        "Am I on the right career path?", "How can I align my work with my values?",
        "What is my professional calling?", "How do I find meaning in my current job?",
        "How should I handle this difficult coworker?", "What does my boss really think of my work?",
        "How can I improve my standing at work?", "Is the office politics affecting my growth?",
        "How can I build better professional relationships?", "How can I prepare for this interview?",
        "What energy should I bring to this opportunity?", "Will I make a good impression?",
        "What do I need to show to get this role?", "How can I present my best self professionally?",
        "Am I being fairly compensated?", "Should I ask for a raise?",
        "How can I increase my earning potential?", "What is my true professional value?",
        "How do I negotiate what I deserve?",
    ],
    "growth": [
        "What is my life purpose?", "How can I become my best self?",
        "What lesson am I meant to learn right now?", "What is holding me back from growth?",
        "How can I find inner peace?", "What do I need to release?", "How can I overcome my fears?",
        "What patterns do I need to break?", "What gifts am I not fully using?",
        "How can I heal my inner child?", "How can I deepen my spiritual practice?",
        "What is my soul trying to tell me?", "How can I connect with my higher self?",
        "What spiritual lessons await me?", "How can I trust my intuition more?",
        "What needs healing within me?", "How can I transform my pain into wisdom?",
        "What old wounds still need attention?", "How do I forgive myself for past mistakes?",
        "What is ready to be released from my life?", "What habits are serving me? Which are not?",
        "How can I break this destructive pattern?", "What motivates my self-sabotaging behavior?",
        "How can I build healthier routines?", "What daily practice would benefit me most?",
        "What am I most afraid of?", "What fear is holding me back from living fully?",
        "How can I move through this block?", "What lies beneath my anxiety?",
        "How do I find courage in uncertain times?", "What aspect of myself needs attention?",
        "How can I be more authentic?", "What would help me grow right now?",
        "How can I develop more self-compassion?", "What is the next step in my personal evolution?",
        "How can I be more present in my life?", "What is distracting me from what matters?",
        "How can I find stillness in chaos?", "What would help me feel more grounded?",
        "How do I cultivate gratitude in hard times?",
    ],
    "health": [
        "What does my body need right now?", "How can I improve my overall wellbeing?",
        "What is my body trying to tell me?", "What aspect of health should I focus on?",
        "How can I feel more vibrant and alive?", "Why do I feel so drained lately?",
        "How can I restore my energy?", "What is depleting my life force?",
        "How can I cultivate more vitality?", "What would help me feel more energized?",
        "How can I better manage my stress?", "What is the source of my tension?",
        "How do I find balance in my busy life?", "What boundaries do I need for my wellbeing?",
        "How can I create more ease in my days?", "How are my emotions affecting my health?",
        "What is the mind-body message here?", "How can I listen to my body's wisdom?",
        "What emotional healing would benefit my body?", "How do I honor both my mental and physical needs?",
    ],
    "family": [
        "How can I improve my relationship with my parents?",
        "What do I need to understand about my family of origin?",
        "How do I heal my relationship with my mother?", "What does my father need from me?",
        "How can I set boundaries while honoring my parents?",
        "What does my child need from me right now?", "How can I be a better parent?",
        "What should I know about my child's path?", "How can I support my child through this challenge?",
        "What kind of parent am I called to be?", "How can I heal this rift with my sibling?",
        "What dynamics are at play in my family?", "How do I navigate family expectations?",
        "What role do I play in my family system?", "How can I maintain peace at family gatherings?",
        "What does my home need to feel like sanctuary?", "Is this the right home for me?",
        "How can I create more harmony at home?", "What energy is my living space holding?",
        "How do I make my house feel like home?",
    ],
    "money": [
        "How can I improve my financial situation?", "What is my relationship with money?",
        "What blocks my financial abundance?", "How can I create more prosperity?",
        "What do I need to know about my finances?", "Is this a good investment?",
        "How can I grow my wealth wisely?", "What financial opportunities should I consider?",
        "Should I take this financial risk?", "What does my financial future look like?",
        "How can I get out of debt?", "What lesson is this financial struggle teaching me?",
        "How do I overcome my money fears?", "What is causing my financial difficulties?",
        "How can I break the cycle of financial stress?", "How can I develop an abundance mindset?",
        "What beliefs about money are limiting me?", "How do I feel worthy of financial success?",
        "What would help me trust in abundance?", "How can I shift my scarcity thinking?",
    ],
    "decisions": [
        "Which path should I choose?", "What do I need to consider before deciding?",
        "What will happen if I choose this option?", "Am I overlooking something important?",
        "What is the wisest choice here?", "Is this the right time to act?",
        "Should I wait or move forward now?", "What timing feels right for this decision?",
        "Am I rushing this choice?", "When will conditions be favorable?",
        "I'm at a crossroads - which way should I turn?", "What direction is calling me?",
        "How do I know I'm on the right path?", "What is guiding me toward the right choice?",
        "Where is my current path leading?", "Why am I so uncertain about this?",
        "How can I gain clarity on this matter?", "What am I missing in this situation?",
        "What would help me see more clearly?", "How do I trust my decision-making?",
    ],
}


def detect_spread_type(num_cards: int) -> str:
    """Detect spread type from number of cards."""
    mapping = {1: "single", 3: "situation/threeCard", 7: "horseshoe", 10: "celtic"}
    return mapping.get(num_cards, f"unknown({num_cards})")


def parse_example(text: str) -> Dict:
    """Parse a training example to extract coverage metrics."""
    result = {
        "cards": [],
        "positions": [],
        "reversals": [],
        "question": None,
        "question_category": None,
        "moon_phase": None,
        "spread_type": None,
        "num_cards": 0,
    }

    # Extract moon phase from TIMING line
    timing_match = re.search(r'TIMING: ([^🌑🌒🌓🌔🌕🌖🌗🌘]+)', text)
    if timing_match:
        phase = timing_match.group(1).strip()
        result["moon_phase"] = phase

    # Extract question
    question_match = re.search(r'QUESTION: "([^"]+)"', text)
    if question_match:
        result["question"] = question_match.group(1)

    # Extract cards with positions and reversals
    # Pattern: "1. Position Name: Card Name (upright/reversed)"
    card_pattern = r'\d+\.\s+([^:]+):\s+([^(]+)\s*\((upright|reversed)\)'
    matches = re.findall(card_pattern, text)

    for position, card, orientation in matches:
        card_name = card.strip()
        position_name = position.strip()
        is_reversed = orientation == "reversed"

        result["cards"].append(card_name)
        result["positions"].append(position_name)
        result["reversals"].append(is_reversed)

    result["num_cards"] = len(result["cards"])
    result["spread_type"] = detect_spread_type(result["num_cards"])

    # Determine question category by matching against known questions
    if result["question"]:
        for category, questions in QUESTIONS.items():
            if result["question"] in questions:
                result["question_category"] = category
                break
        # Fuzzy match if exact match not found
        if not result["question_category"]:
            q_lower = result["question"].lower()
            for category, questions in QUESTIONS.items():
                for q in questions:
                    if q.lower() in q_lower or q_lower in q.lower():
                        result["question_category"] = category
                        break
                if result["question_category"]:
                    break

    return result


def load_and_parse_files(file_paths: List[Path]) -> List[Dict]:
    """Load all JSONL files and parse examples."""
    examples = []
    for path in file_paths:
        print(f"Processing {path.name}...")
        with open(path) as f:
            for line in f:
                data = json.loads(line)
                parsed = parse_example(data["text"])
                examples.append(parsed)
    return examples


def analyze_coverage(examples: List[Dict]) -> Dict:
    """Run comprehensive coverage analysis."""

    # Initialize counters
    card_counts = Counter()
    card_position_counts = defaultdict(Counter)  # card -> position -> count
    question_category_counts = Counter()
    spread_type_counts = Counter()
    moon_phase_counts = Counter()
    reversal_counts = {"reversed": 0, "upright": 0}
    question_usage = Counter()

    for ex in examples:
        # Card coverage
        for card in ex["cards"]:
            card_counts[card] += 1

        # Card-position coverage
        for card, position in zip(ex["cards"], ex["positions"]):
            pos_id = POSITION_NAME_TO_ID.get(position, position.lower().replace(" ", "_"))
            card_position_counts[card][pos_id] += 1

        # Question category
        if ex["question_category"]:
            question_category_counts[ex["question_category"]] += 1

        # Question usage tracking
        if ex["question"]:
            question_usage[ex["question"]] += 1

        # Spread type
        if ex["spread_type"]:
            spread_type_counts[ex["spread_type"]] += 1

        # Moon phase
        if ex["moon_phase"]:
            moon_phase_counts[ex["moon_phase"]] += 1

        # Reversals
        for is_reversed in ex["reversals"]:
            if is_reversed:
                reversal_counts["reversed"] += 1
            else:
                reversal_counts["upright"] += 1

    return {
        "card_counts": card_counts,
        "card_position_counts": card_position_counts,
        "question_category_counts": question_category_counts,
        "spread_type_counts": spread_type_counts,
        "moon_phase_counts": moon_phase_counts,
        "reversal_counts": reversal_counts,
        "question_usage": question_usage,
        "total_examples": len(examples),
    }


def print_report(analysis: Dict):
    """Print comprehensive coverage report."""

    print("\n" + "="*80)
    print("TAROT TRAINING DATA COVERAGE ANALYSIS")
    print("="*80)
    print(f"\nTotal examples analyzed: {analysis['total_examples']:,}")

    # 1. Card Coverage
    print("\n" + "-"*80)
    print("1. CARD COVERAGE (78 cards)")
    print("-"*80)

    card_counts = analysis["card_counts"]
    missing_cards = [c for c in ALL_CARDS if c not in card_counts]
    low_coverage_cards = [(c, card_counts[c]) for c in ALL_CARDS if card_counts.get(c, 0) < 50]

    total_card_appearances = sum(card_counts.values())
    expected_per_card = total_card_appearances / 78

    print(f"\nTotal card appearances: {total_card_appearances:,}")
    print(f"Expected per card (uniform): {expected_per_card:.1f}")

    # Summary stats
    counts = [card_counts.get(c, 0) for c in ALL_CARDS]
    print(f"Min: {min(counts)}, Max: {max(counts)}, Avg: {sum(counts)/len(counts):.1f}")

    if missing_cards:
        print(f"\n⚠️  MISSING CARDS ({len(missing_cards)}):")
        for card in missing_cards:
            print(f"   - {card}")

    if low_coverage_cards:
        print(f"\n⚠️  LOW COVERAGE CARDS (<50 appearances): {len(low_coverage_cards)}")
        low_coverage_cards.sort(key=lambda x: x[1])
        for card, count in low_coverage_cards[:20]:
            print(f"   - {card}: {count}")
        if len(low_coverage_cards) > 20:
            print(f"   ... and {len(low_coverage_cards) - 20} more")
    else:
        print("\n✅ All cards appear 50+ times")

    # Top and bottom 10
    print("\nTop 10 most frequent cards:")
    for card, count in card_counts.most_common(10):
        print(f"   {card}: {count}")

    print("\nBottom 10 least frequent cards:")
    sorted_cards = sorted([(c, card_counts.get(c, 0)) for c in ALL_CARDS], key=lambda x: x[1])
    for card, count in sorted_cards[:10]:
        print(f"   {card}: {count}")

    # 2. Card-Position Coverage
    print("\n" + "-"*80)
    print("2. CARD-POSITION COVERAGE")
    print("-"*80)

    card_position_counts = analysis["card_position_counts"]
    all_positions = set()
    for card_positions in card_position_counts.values():
        all_positions.update(card_positions.keys())

    print(f"\nUnique positions found: {len(all_positions)}")
    print(f"Positions: {sorted(all_positions)}")

    # Count combos with < 5 examples
    low_combos = []
    zero_combos = []
    for card in ALL_CARDS:
        for pos in all_positions:
            count = card_position_counts.get(card, {}).get(pos, 0)
            if count == 0:
                zero_combos.append((card, pos))
            elif count < 5:
                low_combos.append((card, pos, count))

    total_possible = len(ALL_CARDS) * len(all_positions)
    covered = sum(1 for card in ALL_CARDS for pos in all_positions
                  if card_position_counts.get(card, {}).get(pos, 0) > 0)

    print(f"\nTotal possible (card, position) combos: {total_possible}")
    print(f"Combos with at least 1 example: {covered} ({100*covered/total_possible:.1f}%)")
    print(f"Combos with 0 examples: {len(zero_combos)}")
    print(f"Combos with 1-4 examples: {len(low_combos)}")

    if low_combos:
        print(f"\n⚠️  Sample low-coverage combos (<5):")
        for card, pos, count in sorted(low_combos, key=lambda x: x[2])[:15]:
            print(f"   {card} @ {pos}: {count}")

    # 3. Question Category Balance
    print("\n" + "-"*80)
    print("3. QUESTION CATEGORY BALANCE")
    print("-"*80)

    qc = analysis["question_category_counts"]
    total_q = sum(qc.values())
    target_weights = {"love": 0.20, "career": 0.20, "growth": 0.20,
                     "health": 0.10, "family": 0.10, "money": 0.10, "decisions": 0.10}

    print(f"\n{'Category':<15} {'Count':>8} {'Actual %':>10} {'Target %':>10} {'Delta':>10}")
    print("-" * 55)
    for cat in QUESTION_CATEGORIES:
        count = qc.get(cat, 0)
        actual_pct = 100 * count / total_q if total_q > 0 else 0
        target_pct = 100 * target_weights.get(cat, 0)
        delta = actual_pct - target_pct
        flag = "⚠️" if abs(delta) > 2 else "✅"
        print(f"{cat:<15} {count:>8,} {actual_pct:>9.1f}% {target_pct:>9.1f}% {delta:>+9.1f}% {flag}")

    # 4. Spread Type Distribution
    print("\n" + "-"*80)
    print("4. SPREAD TYPE DISTRIBUTION")
    print("-"*80)

    st = analysis["spread_type_counts"]
    total_spreads = sum(st.values())
    target_spread_weights = {"single": 0.15, "situation/threeCard": 0.50, "horseshoe": 0.15, "celtic": 0.20}

    print(f"\n{'Spread Type':<20} {'Count':>8} {'Actual %':>10} {'Target %':>10}")
    print("-" * 50)
    for spread, count in sorted(st.items(), key=lambda x: -x[1]):
        actual_pct = 100 * count / total_spreads if total_spreads > 0 else 0
        target_pct = 100 * target_spread_weights.get(spread, 0)
        print(f"{spread:<20} {count:>8,} {actual_pct:>9.1f}% {target_pct:>9.1f}%")

    # 5. Moon Phase Distribution
    print("\n" + "-"*80)
    print("5. MOON PHASE DISTRIBUTION")
    print("-"*80)

    mp = analysis["moon_phase_counts"]
    total_moon = sum(mp.values())
    expected_per_phase = total_moon / 8

    print(f"\nExpected per phase (uniform): {expected_per_phase:.0f}")
    print(f"\n{'Moon Phase':<20} {'Count':>8} {'%':>10} {'vs Expected':>12}")
    print("-" * 52)
    for phase in MOON_PHASES:
        count = mp.get(phase, 0)
        pct = 100 * count / total_moon if total_moon > 0 else 0
        delta = count - expected_per_phase
        delta_pct = 100 * delta / expected_per_phase if expected_per_phase > 0 else 0
        flag = "⚠️" if abs(delta_pct) > 15 else "✅"
        print(f"{phase:<20} {count:>8,} {pct:>9.1f}% {delta_pct:>+10.1f}% {flag}")

    # 6. Reversal Ratio
    print("\n" + "-"*80)
    print("6. REVERSAL RATIO")
    print("-"*80)

    rc = analysis["reversal_counts"]
    total_orientations = rc["reversed"] + rc["upright"]
    reversal_pct = 100 * rc["reversed"] / total_orientations if total_orientations > 0 else 0

    print(f"\nReversed: {rc['reversed']:,} ({reversal_pct:.1f}%)")
    print(f"Upright: {rc['upright']:,} ({100-reversal_pct:.1f}%)")
    print(f"\nTarget range: 30-40%")
    if 30 <= reversal_pct <= 40:
        print("✅ Reversal ratio is within target range")
    else:
        print(f"⚠️  Reversal ratio ({reversal_pct:.1f}%) is outside target range (30-40%)")

    # 7. Question Usage Analysis
    print("\n" + "-"*80)
    print("7. QUESTION USAGE ANALYSIS")
    print("-"*80)

    qu = analysis["question_usage"]
    total_questions = len(QUESTIONS["love"]) + len(QUESTIONS["career"]) + len(QUESTIONS["growth"]) + \
                     len(QUESTIONS["health"]) + len(QUESTIONS["family"]) + len(QUESTIONS["money"]) + \
                     len(QUESTIONS["decisions"])

    print(f"\nTotal unique questions in generator: {total_questions}")
    print(f"Questions used in training data: {len(qu)}")

    # Find unused questions
    all_questions = []
    for cat, qs in QUESTIONS.items():
        all_questions.extend(qs)

    unused = [q for q in all_questions if q not in qu]
    if unused:
        print(f"\n⚠️  Unused questions ({len(unused)}):")
        for q in unused[:10]:
            print(f"   - {q}")
        if len(unused) > 10:
            print(f"   ... and {len(unused) - 10} more")

    # Most and least used questions
    print("\nTop 10 most used questions:")
    for q, count in qu.most_common(10):
        print(f"   {count:>5}: {q[:60]}...")

    print("\nBottom 10 least used questions:")
    for q, count in qu.most_common()[-10:]:
        print(f"   {count:>5}: {q[:60]}...")

    return analysis


def generate_recommendations(analysis: Dict) -> List[str]:
    """Generate recommendations for filling gaps with 10k more examples."""

    recommendations = []

    # Card coverage recommendations
    card_counts = analysis["card_counts"]
    low_cards = [c for c in ALL_CARDS if card_counts.get(c, 0) < 50]
    if low_cards:
        recommendations.append(f"Priority: Boost {len(low_cards)} cards with <50 appearances")

    # Question category recommendations
    qc = analysis["question_category_counts"]
    total_q = sum(qc.values())
    target_weights = {"love": 0.20, "career": 0.20, "growth": 0.20,
                     "health": 0.10, "family": 0.10, "money": 0.10, "decisions": 0.10}

    for cat in QUESTION_CATEGORIES:
        count = qc.get(cat, 0)
        actual_pct = count / total_q if total_q > 0 else 0
        target_pct = target_weights.get(cat, 0)
        if actual_pct < target_pct - 0.02:  # More than 2% under target
            deficit = int((target_pct - actual_pct) * 10000)  # Deficit in 10k
            recommendations.append(f"Increase '{cat}' category by ~{deficit} examples")

    # Reversal recommendations
    rc = analysis["reversal_counts"]
    total_orientations = rc["reversed"] + rc["upright"]
    reversal_pct = rc["reversed"] / total_orientations if total_orientations > 0 else 0
    if reversal_pct < 0.30:
        recommendations.append(f"Increase reversal rate from {100*reversal_pct:.1f}% to 30-40%")
    elif reversal_pct > 0.40:
        recommendations.append(f"Decrease reversal rate from {100*reversal_pct:.1f}% to 30-40%")

    return recommendations


def print_recommendations(analysis: Dict):
    """Print recommendations for 10k additional examples."""

    print("\n" + "="*80)
    print("RECOMMENDATIONS FOR 10K ADDITIONAL EXAMPLES")
    print("="*80)

    recs = generate_recommendations(analysis)

    print("\n📋 Key Actions:")
    for i, rec in enumerate(recs, 1):
        print(f"   {i}. {rec}")

    # Calculate specific allocations
    print("\n📊 Suggested 10k Allocation:")

    # Check card coverage
    card_counts = analysis["card_counts"]
    low_cards = [(c, card_counts.get(c, 0)) for c in ALL_CARDS if card_counts.get(c, 0) < 200]

    if low_cards:
        print(f"\n   Card Boosting Priority ({len(low_cards)} cards need attention):")
        low_cards.sort(key=lambda x: x[1])
        for card, count in low_cards[:10]:
            needed = max(0, 200 - count)
            print(f"      • {card}: {count} → need ~{needed} more")

    # Question balance
    print("\n   Category Allocation for 10k:")
    qc = analysis["question_category_counts"]
    total_q = sum(qc.values())
    target = {"love": 2000, "career": 2000, "growth": 2000,
              "health": 1000, "family": 1000, "money": 1000, "decisions": 1000}

    for cat, target_count in target.items():
        current_pct = 100 * qc.get(cat, 0) / total_q if total_q > 0 else 0
        print(f"      • {cat}: {target_count} examples (currently {current_pct:.1f}%)")


if __name__ == "__main__":
    # Find all training files
    data_dir = Path(__file__).parent.parent / "data" / "sft"
    files = sorted(data_dir.glob("*.jsonl"))

    print(f"Found {len(files)} data files:")
    for f in files:
        print(f"  - {f.name}")

    # Load and parse
    examples = load_and_parse_files(files)

    # Analyze
    analysis = analyze_coverage(examples)

    # Print report
    print_report(analysis)

    # Print recommendations
    print_recommendations(analysis)
