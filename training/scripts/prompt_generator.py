"""
Prompt assembly module for generating ~25k training examples.

Combines questions, cards, and spreads into complete prompts
ready for Claude Opus generation.
"""

import json
import random
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path

from cards import (
    FULL_DECK, draw_cards, DrawnCard, get_elemental_balance,
)
from spreads import SPREADS, Spread, sample_spread_weighted
from questions import (
    QUESTION_CATEGORIES, sample_questions_weighted, get_all_base_questions
)


@dataclass
class CardInPosition:
    """A card placed in a specific spread position."""
    position_name: str
    position_description: str
    card_name: str
    card_keywords: List[str]
    card_element: str
    card_arcana: str
    is_reversed: bool
    card_suit: Optional[str] = None
    card_domain: Optional[str] = None


@dataclass
class TrainingPrompt:
    """A complete training example ready for Claude generation."""
    id: str  # Unique hash for deduplication
    spread_id: str
    spread_name: str
    question: str
    question_category: str
    cards: List[CardInPosition]
    elemental_balance: Dict[str, int]
    # These will be filled in by Claude
    claude_response: Optional[str] = None
    generation_status: str = "pending"  # pending, completed, failed

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "TrainingPrompt":
        data["cards"] = [CardInPosition(**c) for c in data["cards"]]
        return cls(**data)


def generate_prompt_id(spread_id: str, question: str, cards: List[DrawnCard]) -> str:
    """Generate a unique ID for a prompt based on its content."""
    card_str = "|".join(f"{c.card.name}:{c.reversed}" for c in cards)
    content = f"{spread_id}|{question}|{card_str}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


def create_training_prompt(
    spread: Spread,
    question_data: Dict[str, str],
    drawn_cards: List[DrawnCard]
) -> TrainingPrompt:
    """Create a complete training prompt from components."""

    cards_in_positions = []
    for i, (position, drawn) in enumerate(zip(spread.positions, drawn_cards)):
        cards_in_positions.append(CardInPosition(
            position_name=position.name,
            position_description=position.description,
            card_name=drawn.card.name,
            card_keywords=drawn.card.keywords,
            card_element=drawn.card.element,
            card_arcana=drawn.card.arcana,
            is_reversed=drawn.reversed,
            card_suit=drawn.card.suit,
            card_domain=drawn.card.domain,
        ))

    prompt_id = generate_prompt_id(
        spread.id,
        question_data["question"],
        drawn_cards
    )

    return TrainingPrompt(
        id=prompt_id,
        spread_id=spread.id,
        spread_name=spread.name,
        question=question_data["question"],
        question_category=question_data["category"],
        cards=cards_in_positions,
        elemental_balance=get_elemental_balance(drawn_cards),
    )


def format_prompt_for_claude(prompt: TrainingPrompt) -> str:
    """
    Format a TrainingPrompt into the input text for Claude.

    This creates the user message that will be sent to Claude Opus
    to generate the tarot reading response.
    """
    lines = []

    # Spread and question context
    lines.append(f"## Tarot Reading Request")
    lines.append(f"**Spread:** {prompt.spread_name}")
    lines.append(f"**Question:** {prompt.question}")
    lines.append("")

    # Cards drawn
    lines.append("## Cards Drawn")
    for card in prompt.cards:
        orientation = "Reversed" if card.is_reversed else "Upright"
        lines.append(f"### {card.position_name}: {card.card_name} ({orientation})")
        lines.append(f"*Position meaning: {card.position_description}*")
        lines.append(f"- Element: {card.card_element}")
        lines.append(f"- Keywords: {', '.join(card.card_keywords)}")
        if card.card_domain:
            lines.append(f"- Domain: {card.card_domain}")
        lines.append("")

    # Elemental balance
    lines.append("## Elemental Balance")
    for element, count in prompt.elemental_balance.items():
        if count > 0:
            lines.append(f"- {element}: {count}")

    return "\n".join(lines)


def generate_dataset(
    target_count: int = 25000,
    output_path: Optional[Path] = None,
    seed: int = 42
) -> List[TrainingPrompt]:
    """
    Generate the full training dataset.

    Args:
        target_count: Number of prompts to generate
        output_path: Optional path to save intermediate results
        seed: Random seed for reproducibility

    Returns:
        List of TrainingPrompt objects
    """
    random.seed(seed)

    # Calculate distribution across spreads
    spread_counts = {}
    for spread_id, spread in SPREADS.items():
        spread_counts[spread_id] = int(target_count * spread.weight)

    # Adjust to hit exact target
    total = sum(spread_counts.values())
    if total < target_count:
        # Add remainder to most popular spread
        spread_counts["threeCard"] += target_count - total

    print(f"Generating {target_count} prompts with distribution:")
    for spread_id, count in spread_counts.items():
        print(f"  {spread_id}: {count} ({count/target_count:.1%})")

    prompts = []
    seen_ids = set()

    for spread_id, count in spread_counts.items():
        spread = SPREADS[spread_id]
        num_cards = len(spread.positions)

        # Sample questions for this spread batch
        questions = sample_questions_weighted(count, with_variations=True)

        for i, question_data in enumerate(questions):
            # Draw cards for this reading
            drawn_cards = draw_cards(num_cards, allow_reversed=True)

            # Create the prompt
            prompt = create_training_prompt(spread, question_data, drawn_cards)

            # Skip duplicates (unlikely but possible)
            if prompt.id in seen_ids:
                # Redraw
                drawn_cards = draw_cards(num_cards, allow_reversed=True)
                prompt = create_training_prompt(spread, question_data, drawn_cards)

            seen_ids.add(prompt.id)
            prompts.append(prompt)

            # Progress update
            if (len(prompts)) % 5000 == 0:
                print(f"  Generated {len(prompts)} prompts...")

    random.shuffle(prompts)  # Shuffle for training variety

    print(f"Generated {len(prompts)} unique prompts")

    # Save if path provided
    if output_path:
        save_prompts(prompts, output_path)

    return prompts


def save_prompts(prompts: List[TrainingPrompt], path: Path):
    """Save prompts to JSON file."""
    data = [p.to_dict() for p in prompts]
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(prompts)} prompts to {path}")


def load_prompts(path: Path) -> List[TrainingPrompt]:
    """Load prompts from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return [TrainingPrompt.from_dict(d) for d in data]


def get_dataset_stats(prompts: List[TrainingPrompt]) -> Dict:
    """Compute statistics about the dataset."""
    stats = {
        "total": len(prompts),
        "by_spread": {},
        "by_question_category": {},
        "by_status": {},
        "reversed_ratio": 0,
    }

    total_cards = 0
    reversed_cards = 0

    for p in prompts:
        # By spread
        stats["by_spread"][p.spread_id] = stats["by_spread"].get(p.spread_id, 0) + 1

        # By question category
        stats["by_question_category"][p.question_category] = \
            stats["by_question_category"].get(p.question_category, 0) + 1

        # By status
        stats["by_status"][p.generation_status] = \
            stats["by_status"].get(p.generation_status, 0) + 1

        # Reversed ratio
        for card in p.cards:
            total_cards += 1
            if card.is_reversed:
                reversed_cards += 1

    stats["reversed_ratio"] = reversed_cards / total_cards if total_cards > 0 else 0

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate training prompts")
    parser.add_argument("--count", type=int, default=25000, help="Number of prompts")
    parser.add_argument("--output", type=str, default="../data/prompts.json", help="Output path")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--preview", type=int, default=0, help="Preview N prompts without saving")

    args = parser.parse_args()

    if args.preview > 0:
        print(f"=== Preview of {args.preview} prompts ===\n")
        prompts = generate_dataset(args.preview, seed=args.seed)
        for i, p in enumerate(prompts[:3]):
            print(f"\n{'='*60}")
            print(f"Prompt {i+1} (ID: {p.id})")
            print(f"{'='*60}")
            print(format_prompt_for_claude(p))
    else:
        output_path = Path(__file__).parent / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        prompts = generate_dataset(args.count, output_path, args.seed)

        stats = get_dataset_stats(prompts)
        print(f"\n=== Dataset Statistics ===")
        print(f"Total prompts: {stats['total']}")
        print(f"Reversed card ratio: {stats['reversed_ratio']:.1%}")
        print(f"\nBy spread:")
        for spread_id, count in stats['by_spread'].items():
            print(f"  {spread_id}: {count}")
        print(f"\nBy question category:")
        for cat, count in stats['by_question_category'].items():
            print(f"  {cat}: {count}")
