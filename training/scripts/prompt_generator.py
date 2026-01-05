"""
Prompt generator for training data - mirrors iOS PromptAssembler exactly.
Uses the same JSON data from TaroApp/Resources/.
"""

import json
import random
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime, timezone


# MARK: - Moon Phase (mirrors MoonPhase.swift)

MOON_PHASES = [
    {"name": "New Moon", "icon": "🌑", "meaning": "New beginnings, setting intentions, planting seeds"},
    {"name": "Waxing Crescent", "icon": "🌒", "meaning": "Taking action, building momentum, hope emerges"},
    {"name": "First Quarter", "icon": "🌓", "meaning": "Challenges arise, decisions needed, commitment tested"},
    {"name": "Waxing Gibbous", "icon": "🌔", "meaning": "Refining plans, patience required, trust the process"},
    {"name": "Full Moon", "icon": "🌕", "meaning": "Culmination, clarity, emotions heightened, harvest results"},
    {"name": "Waning Gibbous", "icon": "🌖", "meaning": "Gratitude, sharing wisdom, integration"},
    {"name": "Last Quarter", "icon": "🌗", "meaning": "Release, forgiveness, letting go of what no longer serves"},
    {"name": "Waning Crescent", "icon": "🌘", "meaning": "Rest, reflection, preparing for renewal"},
]

SYNODIC_MONTH = 29.53058867
# Reference new moon: December 30, 2024 22:27 UTC
REFERENCE_NEW_MOON = datetime(2024, 12, 30, 22, 27, 0, tzinfo=timezone.utc)


def get_moon_phase(date: datetime = None) -> Dict:
    """Calculate moon phase for a given date (mirrors MoonPhaseCalculator.swift)."""
    if date is None:
        date = datetime.now(timezone.utc)

    days_since_ref = (date - REFERENCE_NEW_MOON).total_seconds() / 86400
    lunar_age = days_since_ref % SYNODIC_MONTH
    if lunar_age < 0:
        lunar_age += SYNODIC_MONTH

    # Center each phase window (same algorithm as iOS)
    phase_index = int((lunar_age + SYNODIC_MONTH / 16) / SYNODIC_MONTH * 8) % 8
    return MOON_PHASES[phase_index]


def get_random_moon_phase(rng: random.Random) -> Dict:
    """Get a random moon phase for training data variety."""
    return rng.choice(MOON_PHASES)


def moon_phase_context(phase: Dict) -> str:
    """Format moon phase for prompt (mirrors MoonPhase.promptContext)."""
    return f"{phase['name']} {phase['icon']} — {phase['meaning']}"

# Path to iOS app resources (source of truth)
IOS_RESOURCES = Path(__file__).parent.parent.parent / "TaroApp" / "TaroApp" / "Resources"


# MARK: - Data Loading (mirrors DataService.swift)

def load_json(filename: str) -> Dict:
    """Load JSON from iOS resources."""
    path = IOS_RESOURCES / f"{filename}.json"
    with open(path) as f:
        return json.load(f)


# Load production data
BASE_MEANINGS = load_json("base-meanings")
POSITION_MODIFIERS = load_json("position-modifiers")
COMBINATIONS = load_json("combinations")["combinations"]


def get_base_meaning(card_name: str, is_reversed: bool) -> str:
    """Get base meaning for a card (mirrors DataService.baseMeaning)."""
    meaning = BASE_MEANINGS.get("major", {}).get(card_name)
    if not meaning:
        meaning = BASE_MEANINGS.get("minor", {}).get(card_name)
    if not meaning:
        return "Meaning not available"
    return meaning["reversed"] if is_reversed else meaning["upright"]


def get_position_modifier(card_name: str, position_id: str, is_reversed: bool) -> Optional[str]:
    """Get position modifier (mirrors DataService.positionModifier)."""
    modifiers = POSITION_MODIFIERS.get("modifiers", {}).get(card_name)
    if not modifiers:
        return None
    orientation = "reversed" if is_reversed else "upright"
    return modifiers.get(orientation, {}).get(position_id)


def find_combinations(card_names: List[str]) -> List[Dict]:
    """Find matching combinations (mirrors ReadingInterpretation.findCombinations)."""
    card_set = set(card_names)
    return [c for c in COMBINATIONS if all(card in card_set for card in c["cards"])]


# MARK: - Card Data (mirrors CardDeck.swift)

CARDS = [
    # Major Arcana
    {"name": "The Fool", "keywords": ["beginnings", "innocence", "spontaneity", "leap of faith"], "element": "Air", "arcana": "major"},
    {"name": "The Magician", "keywords": ["manifestation", "willpower", "skill", "resourcefulness"], "element": "Air", "arcana": "major"},
    {"name": "The High Priestess", "keywords": ["intuition", "mystery", "inner voice", "unconscious"], "element": "Water", "arcana": "major"},
    {"name": "The Empress", "keywords": ["abundance", "nurturing", "fertility", "nature"], "element": "Earth", "arcana": "major"},
    {"name": "The Emperor", "keywords": ["authority", "structure", "control", "father figure"], "element": "Fire", "arcana": "major"},
    {"name": "The Hierophant", "keywords": ["tradition", "conformity", "wisdom", "spiritual guidance"], "element": "Earth", "arcana": "major"},
    {"name": "The Lovers", "keywords": ["love", "harmony", "choices", "union"], "element": "Air", "arcana": "major"},
    {"name": "The Chariot", "keywords": ["willpower", "determination", "victory", "control"], "element": "Water", "arcana": "major"},
    {"name": "Strength", "keywords": ["courage", "patience", "inner strength", "compassion"], "element": "Fire", "arcana": "major"},
    {"name": "The Hermit", "keywords": ["introspection", "solitude", "guidance", "inner wisdom"], "element": "Earth", "arcana": "major"},
    {"name": "Wheel of Fortune", "keywords": ["cycles", "fate", "turning point", "destiny"], "element": "Fire", "arcana": "major"},
    {"name": "Justice", "keywords": ["fairness", "truth", "karma", "accountability"], "element": "Air", "arcana": "major"},
    {"name": "The Hanged Man", "keywords": ["surrender", "new perspective", "pause", "letting go"], "element": "Water", "arcana": "major"},
    {"name": "Death", "keywords": ["transformation", "endings", "change", "transition"], "element": "Water", "arcana": "major"},
    {"name": "Temperance", "keywords": ["balance", "moderation", "patience", "harmony"], "element": "Fire", "arcana": "major"},
    {"name": "The Devil", "keywords": ["shadow self", "attachment", "addiction", "bondage"], "element": "Earth", "arcana": "major"},
    {"name": "The Tower", "keywords": ["upheaval", "revelation", "sudden change", "awakening"], "element": "Fire", "arcana": "major"},
    {"name": "The Star", "keywords": ["hope", "faith", "renewal", "inspiration"], "element": "Air", "arcana": "major"},
    {"name": "The Moon", "keywords": ["illusion", "fear", "subconscious", "intuition"], "element": "Water", "arcana": "major"},
    {"name": "The Sun", "keywords": ["joy", "success", "vitality", "positivity"], "element": "Fire", "arcana": "major"},
    {"name": "Judgement", "keywords": ["rebirth", "inner calling", "reflection", "reckoning"], "element": "Fire", "arcana": "major"},
    {"name": "The World", "keywords": ["completion", "achievement", "wholeness", "fulfillment"], "element": "Earth", "arcana": "major"},
]

# Generate Minor Arcana
SUITS = {
    "Wands": {"element": "Fire", "domain": "passion, creativity, action"},
    "Cups": {"element": "Water", "domain": "emotions, relationships, intuition"},
    "Swords": {"element": "Air", "domain": "thoughts, conflict, truth"},
    "Pentacles": {"element": "Earth", "domain": "finances, career, material"},
}

RANKS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]
RANK_KEYWORDS = {
    "Ace": ["new beginning", "potential", "opportunity"],
    "Two": ["balance", "partnership", "duality"],
    "Three": ["growth", "creativity", "collaboration"],
    "Four": ["stability", "foundation", "structure"],
    "Five": ["conflict", "challenge", "change"],
    "Six": ["harmony", "communication", "transition"],
    "Seven": ["reflection", "assessment", "perseverance"],
    "Eight": ["movement", "speed", "progress"],
    "Nine": ["fruition", "attainment", "wisdom"],
    "Ten": ["completion", "ending", "fulfillment"],
    "Page": ["messenger", "student", "new energy"],
    "Knight": ["action", "adventure", "movement"],
    "Queen": ["nurturing", "intuitive", "mastery"],
    "King": ["authority", "control", "leadership"],
}

for suit, suit_info in SUITS.items():
    for rank in RANKS:
        CARDS.append({
            "name": f"{rank} of {suit}",
            "keywords": RANK_KEYWORDS[rank],
            "element": suit_info["element"],
            "arcana": "minor",
            "suit": suit,
        })


# MARK: - Spreads (mirrors Spread.swift)

SPREADS = {
    "single": {
        "name": "Daily Draw",
        "positions": [{"id": "todays_guidance", "name": "Today's Guidance", "description": "Your guidance for today"}]
    },
    "threeCard": {
        "name": "Past · Present · Future",
        "positions": [
            {"id": "past", "name": "Past", "description": "What has led to this moment"},
            {"id": "present", "name": "Present", "description": "Where you are now"},
            {"id": "future", "name": "Future", "description": "Where this path leads"},
        ]
    },
    "situation": {
        "name": "Situation · Action · Outcome",
        "positions": [
            {"id": "situation", "name": "Situation", "description": "The nature of what you face"},
            {"id": "action", "name": "Action", "description": "The approach advised"},
            {"id": "outcome", "name": "Outcome", "description": "The likely result"},
        ]
    },
    "horseshoe": {
        "name": "Horseshoe",
        "positions": [
            {"id": "past", "name": "Past", "description": "What has shaped the situation"},
            {"id": "present", "name": "Present", "description": "Current circumstances"},
            {"id": "hidden_influences", "name": "Hidden Influences", "description": "Factors not immediately apparent"},
            {"id": "obstacles", "name": "Obstacles", "description": "Challenges to overcome"},
            {"id": "external", "name": "External Influences", "description": "People or events affecting you"},
            {"id": "advice", "name": "Advice", "description": "Guidance for moving forward"},
            {"id": "outcome", "name": "Outcome", "description": "Where this path leads"},
        ]
    },
    "celtic": {
        "name": "Celtic Cross",
        "positions": [
            {"id": "present", "name": "Present", "description": "Current situation"},
            {"id": "challenge", "name": "Challenge", "description": "Obstacle you face"},
            {"id": "past", "name": "Past", "description": "Recent influences"},
            {"id": "future", "name": "Future", "description": "What's coming"},
            {"id": "above", "name": "Above", "description": "Best outcome"},
            {"id": "below", "name": "Below", "description": "Subconscious"},
            {"id": "advice", "name": "Advice", "description": "How to approach"},
            {"id": "external", "name": "External", "description": "Outside influences"},
            {"id": "hopes_fears", "name": "Hopes/Fears", "description": "Inner conflict"},
            {"id": "outcome", "name": "Outcome", "description": "Final result"},
        ]
    },
}

SPREAD_WEIGHTS = {"single": 0.15, "threeCard": 0.30, "situation": 0.20, "horseshoe": 0.15, "celtic": 0.20}


# MARK: - Prompt Building (mirrors PromptAssembler.assemblePrompt exactly)

def build_prompt(drawn_cards: List[Dict], question: Optional[str], style: str = "balanced", moon_phase: Dict = None) -> str:
    """
    Build prompt exactly as iOS PromptAssembler.assemblePrompt() does.

    Args:
        drawn_cards: List of {"card": card_dict, "position": position_dict, "is_reversed": bool}
        question: Optional querent question
        style: "balanced", "mystical", or "practical"
        moon_phase: Optional moon phase dict, uses random if None for training variety

    Returns:
        Complete prompt in Phi-3 chat format
    """
    # Build card context
    card_context = ""
    card_names = []
    elements = []

    for i, dc in enumerate(drawn_cards):
        card = dc["card"]
        position = dc["position"]
        is_reversed = dc["is_reversed"]
        orientation = "reversed" if is_reversed else "upright"

        card_names.append(card["name"])
        elements.append(card["element"])

        base_meaning = get_base_meaning(card["name"], is_reversed)
        position_mod = get_position_modifier(card["name"], position["id"], is_reversed)

        card_context += f"""{i + 1}. {position["name"]}: {card["name"]} ({orientation})
   Keywords: {", ".join(card["keywords"])}
   Base meaning: {base_meaning}
"""
        if position_mod:
            card_context += f"   Position context: {position_mod}\n"
        card_context += "\n"

    # Combinations
    combos = find_combinations(card_names)
    combinations_context = ""
    if combos:
        combinations_context = "Card Combinations:\n"
        for combo in combos:
            combinations_context += f"- {' + '.join(combo['cards'])}: {combo['meaning']}\n"
        combinations_context += "\n"

    # Elemental flow
    element_counts = {}
    for e in elements:
        element_counts[e] = element_counts.get(e, 0) + 1

    dominant = None
    for e, count in element_counts.items():
        if count > len(elements) / 2:
            dominant = e
            break

    flow = " → ".join(elements)
    elemental_context = f"Elemental Balance: {dominant or 'Balanced'}\n{flow}"
    if dominant:
        elemental_context += f"\nDominant: {dominant} energy"

    # Style instruction (mirrors PromptAssembler)
    style_instructions = {
        "balanced": "Provide a balanced interpretation that combines intuitive insight with practical guidance.",
        "mystical": "Provide a deeply symbolic and poetic interpretation, rich with mystical imagery and spiritual insight.",
        "practical": "Provide direct, actionable guidance focused on practical steps and clear advice.",
    }
    style_instruction = style_instructions.get(style, style_instructions["balanced"])

    # Moon phase timing context (new feature)
    if moon_phase is None:
        # For training, we use a fixed phase based on card hash for reproducibility
        moon_phase = MOON_PHASES[hash(card_names[0]) % len(MOON_PHASES)]
    timing_context = f"TIMING: {moon_phase_context(moon_phase)}\n\n"

    # Question context
    question_context = f'QUESTION: "{question}"\n\n' if question else ""

    # Build full prompt in Phi-3 format (mirrors iOS PromptAssembler.assemblePrompt)
    prompt = f"""<|system|>
You are crafting a tarot reading. Weave the provided card interpretations into a cohesive narrative. {style_instruction}<|end|>
<|user|>
{timing_context}{question_context}The following cards were drawn:

{card_context}{combinations_context}{elemental_context}

Weave these elements into a flowing interpretation (3-4 paragraphs). Address the seeker directly. End with actionable insight.<|end|>
<|assistant|>
"""
    return prompt


# MARK: - Training Data Generation

@dataclass
class TrainingPrompt:
    id: str
    spread_name: str
    question: str
    question_category: str
    input_text: str
    response: Optional[str] = None
    status: str = "pending"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "spread_name": self.spread_name,
            "question": self.question,
            "question_category": self.question_category,
            "input_text": self.input_text,
            "response": self.response,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "TrainingPrompt":
        return cls(**d)


# Questions organized by category (~200 total)
QUESTIONS = {
    "love": [
        # Relationships - general
        "Will I find love?",
        "Is my partner the one for me?",
        "Should I stay in my current relationship?",
        "How can I improve my relationship?",
        "What is blocking me from finding love?",
        "How does my partner really feel about me?",
        "Am I ready for a committed relationship?",
        "What do I need to learn from this relationship?",
        "How can I heal from my past heartbreak?",
        "What is the future of my relationship?",
        # Dating
        "What should I look for in a partner?",
        "Why do I keep attracting the wrong people?",
        "Am I ready to start dating again?",
        "What energy am I projecting in the dating world?",
        "How can I open myself up to new love?",
        # Marriage & commitment
        "Is marriage in my future?",
        "What do I need to know before getting engaged?",
        "How can we reignite the spark in our marriage?",
        "What is the state of my marriage?",
        "Are we ready to take the next step together?",
        # Heartbreak & healing
        "How do I move on from this breakup?",
        "What lessons does this heartbreak hold for me?",
        "Will I be able to trust again?",
        "What do I need to release to heal my heart?",
        "How long will it take me to feel whole again?",
        # Attraction & chemistry
        "Is there real chemistry between us?",
        "What attracts my ideal partner to me?",
        "Why am I drawn to this person?",
        "What is the nature of our connection?",
        "Does this person have genuine feelings for me?",
        # Compatibility
        "Are we truly compatible?",
        "What challenges will we face together?",
        "Where do our values align and differ?",
        "Can we build a lasting future together?",
        "What does our relationship need to thrive?",
        # Communication & connection
        "How can we communicate better?",
        "What is my partner not telling me?",
        "How can I express my needs more clearly?",
        "What is causing distance between us?",
        "How can I feel more connected to my partner?",
    ],
    "career": [
        # Job changes
        "Should I change careers?",
        "Will I get the promotion?",
        "Is this job right for me?",
        "How can I advance in my career?",
        "Should I start my own business?",
        "What is blocking my career success?",
        "Is it time to quit my job?",
        "What career path should I pursue?",
        "How can I find more fulfillment at work?",
        "What's holding me back professionally?",
        # New opportunities
        "Should I accept this job offer?",
        "What opportunities are coming my way?",
        "Is this the right time for a career change?",
        "What should I know about this new position?",
        "Will this move benefit my career long-term?",
        # Business & entrepreneurship
        "Is my business idea viable?",
        "What does my business need to succeed?",
        "Should I pursue this partnership?",
        "How can I grow my business?",
        "What risks should I be aware of?",
        # Purpose & fulfillment
        "What work would truly fulfill me?",
        "Am I on the right career path?",
        "How can I align my work with my values?",
        "What is my professional calling?",
        "How do I find meaning in my current job?",
        # Workplace dynamics
        "How should I handle this difficult coworker?",
        "What does my boss really think of my work?",
        "How can I improve my standing at work?",
        "Is the office politics affecting my growth?",
        "How can I build better professional relationships?",
        # Interviews & transitions
        "How can I prepare for this interview?",
        "What energy should I bring to this opportunity?",
        "Will I make a good impression?",
        "What do I need to show to get this role?",
        "How can I present my best self professionally?",
        # Compensation & value
        "Am I being fairly compensated?",
        "Should I ask for a raise?",
        "How can I increase my earning potential?",
        "What is my true professional value?",
        "How do I negotiate what I deserve?",
    ],
    "growth": [
        # Life purpose
        "What is my life purpose?",
        "How can I become my best self?",
        "What lesson am I meant to learn right now?",
        "What is holding me back from growth?",
        "How can I find inner peace?",
        "What do I need to release?",
        "How can I overcome my fears?",
        "What patterns do I need to break?",
        "What gifts am I not fully using?",
        "How can I heal my inner child?",
        # Spirituality
        "How can I deepen my spiritual practice?",
        "What is my soul trying to tell me?",
        "How can I connect with my higher self?",
        "What spiritual lessons await me?",
        "How can I trust my intuition more?",
        # Healing & transformation
        "What needs healing within me?",
        "How can I transform my pain into wisdom?",
        "What old wounds still need attention?",
        "How do I forgive myself for past mistakes?",
        "What is ready to be released from my life?",
        # Habits & behaviors
        "What habits are serving me? Which are not?",
        "How can I break this destructive pattern?",
        "What motivates my self-sabotaging behavior?",
        "How can I build healthier routines?",
        "What daily practice would benefit me most?",
        # Fears & blocks
        "What am I most afraid of?",
        "What fear is holding me back from living fully?",
        "How can I move through this block?",
        "What lies beneath my anxiety?",
        "How do I find courage in uncertain times?",
        # Self-improvement
        "What aspect of myself needs attention?",
        "How can I be more authentic?",
        "What would help me grow right now?",
        "How can I develop more self-compassion?",
        "What is the next step in my personal evolution?",
        # Mindfulness & presence
        "How can I be more present in my life?",
        "What is distracting me from what matters?",
        "How can I find stillness in chaos?",
        "What would help me feel more grounded?",
        "How do I cultivate gratitude in hard times?",
    ],
    "health": [
        # General wellness
        "What does my body need right now?",
        "How can I improve my overall wellbeing?",
        "What is my body trying to tell me?",
        "What aspect of health should I focus on?",
        "How can I feel more vibrant and alive?",
        # Energy & vitality
        "Why do I feel so drained lately?",
        "How can I restore my energy?",
        "What is depleting my life force?",
        "How can I cultivate more vitality?",
        "What would help me feel more energized?",
        # Stress & balance
        "How can I better manage my stress?",
        "What is the source of my tension?",
        "How do I find balance in my busy life?",
        "What boundaries do I need for my wellbeing?",
        "How can I create more ease in my days?",
        # Mind-body connection
        "How are my emotions affecting my health?",
        "What is the mind-body message here?",
        "How can I listen to my body's wisdom?",
        "What emotional healing would benefit my body?",
        "How do I honor both my mental and physical needs?",
    ],
    "family": [
        # Parents
        "How can I improve my relationship with my parents?",
        "What do I need to understand about my family of origin?",
        "How do I heal my relationship with my mother?",
        "What does my father need from me?",
        "How can I set boundaries while honoring my parents?",
        # Children
        "What does my child need from me right now?",
        "How can I be a better parent?",
        "What should I know about my child's path?",
        "How can I support my child through this challenge?",
        "What kind of parent am I called to be?",
        # Siblings & extended family
        "How can I heal this rift with my sibling?",
        "What dynamics are at play in my family?",
        "How do I navigate family expectations?",
        "What role do I play in my family system?",
        "How can I maintain peace at family gatherings?",
        # Home & domestic life
        "What does my home need to feel like sanctuary?",
        "Is this the right home for me?",
        "How can I create more harmony at home?",
        "What energy is my living space holding?",
        "How do I make my house feel like home?",
    ],
    "money": [
        # Finances general
        "How can I improve my financial situation?",
        "What is my relationship with money?",
        "What blocks my financial abundance?",
        "How can I create more prosperity?",
        "What do I need to know about my finances?",
        # Investments & growth
        "Is this a good investment?",
        "How can I grow my wealth wisely?",
        "What financial opportunities should I consider?",
        "Should I take this financial risk?",
        "What does my financial future look like?",
        # Debt & challenges
        "How can I get out of debt?",
        "What lesson is this financial struggle teaching me?",
        "How do I overcome my money fears?",
        "What is causing my financial difficulties?",
        "How can I break the cycle of financial stress?",
        # Abundance mindset
        "How can I develop an abundance mindset?",
        "What beliefs about money are limiting me?",
        "How do I feel worthy of financial success?",
        "What would help me trust in abundance?",
        "How can I shift my scarcity thinking?",
    ],
    "decisions": [
        # Big choices
        "Which path should I choose?",
        "What do I need to consider before deciding?",
        "What will happen if I choose this option?",
        "Am I overlooking something important?",
        "What is the wisest choice here?",
        # Timing
        "Is this the right time to act?",
        "Should I wait or move forward now?",
        "What timing feels right for this decision?",
        "Am I rushing this choice?",
        "When will conditions be favorable?",
        # Direction & crossroads
        "I'm at a crossroads - which way should I turn?",
        "What direction is calling me?",
        "How do I know I'm on the right path?",
        "What is guiding me toward the right choice?",
        "Where is my current path leading?",
        # Clarity & confusion
        "Why am I so uncertain about this?",
        "How can I gain clarity on this matter?",
        "What am I missing in this situation?",
        "What would help me see more clearly?",
        "How do I trust my decision-making?",
    ],
}

# Weights based on target counts: love(40), career(40), growth(40), health(20), family(20), money(20), decisions(20)
QUESTION_WEIGHTS = {
    "love": 0.20,
    "career": 0.20,
    "growth": 0.20,
    "health": 0.10,
    "family": 0.10,
    "money": 0.10,
    "decisions": 0.10,
}


def draw_cards(spread_id: str, rng: random.Random) -> List[Dict]:
    """Draw cards for a spread."""
    spread = SPREADS[spread_id]
    deck = rng.sample(CARDS, len(spread["positions"]))
    return [
        {"card": card, "position": pos, "is_reversed": rng.random() < 0.5}
        for card, pos in zip(deck, spread["positions"])
    ]


def sample_question(rng: random.Random) -> tuple:
    """Sample a question with category."""
    cats = list(QUESTIONS.keys())
    weights = [QUESTION_WEIGHTS[c] for c in cats]
    cat = rng.choices(cats, weights=weights)[0]
    return rng.choice(QUESTIONS[cat]), cat


def generate_id(spread_id: str, question: str, cards: List[Dict]) -> str:
    card_str = "|".join(f"{c['card']['name']}:{c['is_reversed']}" for c in cards)
    return hashlib.md5(f"{spread_id}|{question}|{card_str}".encode()).hexdigest()[:12]


def generate_dataset(count: int = 25000, seed: int = 42) -> List[TrainingPrompt]:
    """Generate training prompts using iOS prompt format."""
    rng = random.Random(seed)

    # Distribute across spreads
    spread_counts = {sid: int(count * w) for sid, w in SPREAD_WEIGHTS.items()}
    spread_counts["threeCard"] += count - sum(spread_counts.values())

    print(f"Generating {count} prompts:")
    for sid, c in spread_counts.items():
        print(f"  {sid}: {c}")

    prompts = []
    seen = set()

    for spread_id, n in spread_counts.items():
        spread = SPREADS[spread_id]
        for _ in range(n):
            question, cat = sample_question(rng)
            cards = draw_cards(spread_id, rng)
            pid = generate_id(spread_id, question, cards)

            while pid in seen:
                cards = draw_cards(spread_id, rng)
                pid = generate_id(spread_id, question, cards)

            seen.add(pid)
            # Use random moon phase for training data variety
            moon_phase = get_random_moon_phase(rng)
            input_text = build_prompt(cards, question, style="balanced", moon_phase=moon_phase)

            prompts.append(TrainingPrompt(
                id=pid,
                spread_name=spread["name"],
                question=question,
                question_category=cat,
                input_text=input_text,
            ))

            if len(prompts) % 5000 == 0:
                print(f"  Generated {len(prompts)}...")

    rng.shuffle(prompts)
    print(f"Generated {len(prompts)} prompts")
    return prompts


def save_prompts(prompts: List[TrainingPrompt], path: Path):
    with open(path, 'w') as f:
        json.dump([p.to_dict() for p in prompts], f, indent=2)
    print(f"Saved to {path}")


def load_prompts(path: Path) -> List[TrainingPrompt]:
    with open(path) as f:
        return [TrainingPrompt.from_dict(d) for d in json.load(f)]


def get_dataset_stats(prompts: List[TrainingPrompt]) -> Dict:
    stats = {"total": len(prompts), "with_question": 0, "by_spread": {}, "by_category": {}, "by_status": {}}
    for p in prompts:
        if p.question:
            stats["with_question"] += 1
        stats["by_spread"][p.spread_name] = stats["by_spread"].get(p.spread_name, 0) + 1
        stats["by_category"][p.question_category] = stats["by_category"].get(p.question_category, 0) + 1
        stats["by_status"][p.status] = stats["by_status"].get(p.status, 0) + 1
    return stats


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=25000)
    parser.add_argument("--output", type=str, default="../data/prompts.json")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--preview", type=int, help="Preview N prompts")
    args = parser.parse_args()

    if args.preview:
        prompts = generate_dataset(args.preview, args.seed)
        print(f"\n{'='*60}\nSample prompt:\n{'='*60}")
        print(prompts[0].input_text[:2000])
    else:
        output = Path(__file__).parent / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        prompts = generate_dataset(args.count, args.seed)
        save_prompts(prompts, output)
