"""
Prompt generator for training data - mirrors iOS LLMService.buildPrompt() exactly.
Uses the same JSON data from TaroApp/Resources/.
"""

import json
import random
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path

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


# MARK: - Prompt Building (mirrors LLMService.buildPrompt exactly)

def build_prompt(drawn_cards: List[Dict], question: Optional[str], style: str = "balanced") -> str:
    """
    Build prompt exactly as iOS LLMService.buildPrompt() does.

    Args:
        drawn_cards: List of {"card": card_dict, "position": position_dict, "is_reversed": bool}
        question: Optional querent question
        style: "balanced", "mystical", or "practical"

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

    # Style instruction
    style_instructions = {
        "balanced": "Provide a balanced interpretation that combines intuitive insight with practical guidance.",
        "mystical": "Provide a deeply symbolic and poetic interpretation, rich with mystical imagery and spiritual insight.",
        "practical": "Provide direct, actionable guidance focused on practical steps and clear advice.",
    }
    style_instruction = style_instructions.get(style, style_instructions["balanced"])

    # Question
    user_question = f'The querent asks: "{question}"\n\n' if question else ""

    # Build full prompt in Phi-3 format (exact copy of iOS)
    prompt = f"""<|system|>
You are a wise and intuitive tarot reader. You provide thoughtful, personalized interpretations that weave together the meanings of the cards, their positions, and the querent's question. {style_instruction}<|end|>
<|user|>
{user_question}The following cards were drawn:

{card_context}{combinations_context}{elemental_context}

Please provide a cohesive interpretation of this tarot reading. Weave together the individual card meanings into a narrative that addresses the querent's situation. Be insightful but accessible.<|end|>
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


# Questions (same as before)
QUESTIONS = {
    "love": ["Will I find love?", "Is my partner the one for me?", "Should I stay in my current relationship?", "How can I improve my relationship?", "What is blocking me from finding love?", "How does my partner really feel about me?", "Am I ready for a committed relationship?", "What do I need to learn from this relationship?", "How can I heal from my past heartbreak?", "What is the future of my relationship?"],
    "career": ["Should I change careers?", "Will I get the promotion?", "Is this job right for me?", "How can I advance in my career?", "Should I start my own business?", "What is blocking my career success?", "Is it time to quit my job?", "What career path should I pursue?", "How can I find more fulfillment at work?", "What's holding me back professionally?"],
    "growth": ["What is my life purpose?", "How can I become my best self?", "What lesson am I meant to learn right now?", "What is holding me back from growth?", "How can I find inner peace?", "What do I need to release?", "How can I overcome my fears?", "What patterns do I need to break?", "What gifts am I not fully using?", "How can I heal my inner child?"],
    "general": ["What do I need to know right now?", "What should I focus on today?", "What energy surrounds me?", "What opportunities are coming?", "What challenges should I prepare for?", "What guidance do I need?"],
}
QUESTION_WEIGHTS = {"love": 0.30, "career": 0.25, "growth": 0.25, "general": 0.20}


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
            input_text = build_prompt(cards, question, style="balanced")

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
