"""
Tarot card definitions and utilities for training data generation.

Mirrors the card data from src/data/cards.js for use in Python training pipeline.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import random

@dataclass
class Card:
    id: int
    name: str
    arcana: str  # "major" or "minor"
    keywords: List[str]
    element: str
    suit: Optional[str] = None
    rank: Optional[str] = None
    value: Optional[int] = None
    domain: Optional[str] = None
    numeral: Optional[str] = None


# Major Arcana
MAJOR_ARCANA: List[Card] = [
    Card(0, "The Fool", "major", ["beginnings", "innocence", "spontaneity", "leap of faith"], "Air", numeral="0"),
    Card(1, "The Magician", "major", ["manifestation", "willpower", "skill", "resourcefulness"], "Air", numeral="I"),
    Card(2, "The High Priestess", "major", ["intuition", "mystery", "inner voice", "unconscious"], "Water", numeral="II"),
    Card(3, "The Empress", "major", ["abundance", "nurturing", "fertility", "nature"], "Earth", numeral="III"),
    Card(4, "The Emperor", "major", ["authority", "structure", "control", "father figure"], "Fire", numeral="IV"),
    Card(5, "The Hierophant", "major", ["tradition", "conformity", "wisdom", "spiritual guidance"], "Earth", numeral="V"),
    Card(6, "The Lovers", "major", ["love", "harmony", "choices", "union"], "Air", numeral="VI"),
    Card(7, "The Chariot", "major", ["willpower", "determination", "victory", "control"], "Water", numeral="VII"),
    Card(8, "Strength", "major", ["courage", "patience", "inner strength", "compassion"], "Fire", numeral="VIII"),
    Card(9, "The Hermit", "major", ["introspection", "solitude", "guidance", "inner wisdom"], "Earth", numeral="IX"),
    Card(10, "Wheel of Fortune", "major", ["cycles", "fate", "turning point", "destiny"], "Fire", numeral="X"),
    Card(11, "Justice", "major", ["fairness", "truth", "karma", "accountability"], "Air", numeral="XI"),
    Card(12, "The Hanged Man", "major", ["surrender", "new perspective", "pause", "letting go"], "Water", numeral="XII"),
    Card(13, "Death", "major", ["transformation", "endings", "change", "transition"], "Water", numeral="XIII"),
    Card(14, "Temperance", "major", ["balance", "moderation", "patience", "harmony"], "Fire", numeral="XIV"),
    Card(15, "The Devil", "major", ["shadow self", "attachment", "addiction", "bondage"], "Earth", numeral="XV"),
    Card(16, "The Tower", "major", ["upheaval", "revelation", "sudden change", "awakening"], "Fire", numeral="XVI"),
    Card(17, "The Star", "major", ["hope", "faith", "renewal", "inspiration"], "Air", numeral="XVII"),
    Card(18, "The Moon", "major", ["illusion", "fear", "subconscious", "intuition"], "Water", numeral="XVIII"),
    Card(19, "The Sun", "major", ["joy", "success", "vitality", "positivity"], "Fire", numeral="XIX"),
    Card(20, "Judgement", "major", ["rebirth", "inner calling", "reflection", "reckoning"], "Fire", numeral="XX"),
    Card(21, "The World", "major", ["completion", "achievement", "wholeness", "fulfillment"], "Earth", numeral="XXI"),
]

# Suit definitions
SUITS: Dict[str, Dict[str, str]] = {
    "Wands": {"element": "Fire", "domain": "passion, creativity, action"},
    "Cups": {"element": "Water", "domain": "emotions, relationships, intuition"},
    "Swords": {"element": "Air", "domain": "thoughts, conflict, truth"},
    "Pentacles": {"element": "Earth", "domain": "finances, career, material"},
}

# Minor card templates
MINOR_CARD_TEMPLATES = [
    {"rank": "Ace", "value": 1, "keywords": ["new beginning", "potential", "opportunity"]},
    {"rank": "Two", "value": 2, "keywords": ["balance", "partnership", "duality"]},
    {"rank": "Three", "value": 3, "keywords": ["growth", "creativity", "collaboration"]},
    {"rank": "Four", "value": 4, "keywords": ["stability", "foundation", "structure"]},
    {"rank": "Five", "value": 5, "keywords": ["conflict", "challenge", "change"]},
    {"rank": "Six", "value": 6, "keywords": ["harmony", "communication", "transition"]},
    {"rank": "Seven", "value": 7, "keywords": ["reflection", "assessment", "perseverance"]},
    {"rank": "Eight", "value": 8, "keywords": ["movement", "speed", "progress"]},
    {"rank": "Nine", "value": 9, "keywords": ["fruition", "attainment", "wisdom"]},
    {"rank": "Ten", "value": 10, "keywords": ["completion", "ending", "fulfillment"]},
    {"rank": "Page", "value": 11, "keywords": ["messenger", "student", "new energy"]},
    {"rank": "Knight", "value": 12, "keywords": ["action", "adventure", "movement"]},
    {"rank": "Queen", "value": 13, "keywords": ["nurturing", "intuitive", "mastery"]},
    {"rank": "King", "value": 14, "keywords": ["authority", "control", "leadership"]},
]


def _generate_minor_arcana() -> List[Card]:
    """Generate all minor arcana cards."""
    cards = []
    card_id = 22  # Start after major arcana

    for suit_name, suit_data in SUITS.items():
        for template in MINOR_CARD_TEMPLATES:
            cards.append(Card(
                id=card_id,
                name=f"{template['rank']} of {suit_name}",
                arcana="minor",
                keywords=template["keywords"],
                element=suit_data["element"],
                suit=suit_name,
                rank=template["rank"],
                value=template["value"],
                domain=suit_data["domain"],
            ))
            card_id += 1

    return cards


MINOR_ARCANA: List[Card] = _generate_minor_arcana()
FULL_DECK: List[Card] = MAJOR_ARCANA + MINOR_ARCANA


@dataclass
class DrawnCard:
    """A card that has been drawn with orientation."""
    card: Card
    reversed: bool

    @property
    def display_name(self) -> str:
        suffix = " (Reversed)" if self.reversed else ""
        return f"{self.card.name}{suffix}"

    @property
    def orientation(self) -> str:
        return "reversed" if self.reversed else "upright"


def draw_cards(n: int, allow_reversed: bool = True) -> List[DrawnCard]:
    """
    Draw n random cards from the deck without replacement.

    Args:
        n: Number of cards to draw
        allow_reversed: Whether cards can appear reversed

    Returns:
        List of DrawnCard objects
    """
    if n > len(FULL_DECK):
        raise ValueError(f"Cannot draw {n} cards from a deck of {len(FULL_DECK)}")

    selected = random.sample(FULL_DECK, n)
    drawn = []

    for card in selected:
        reversed_card = allow_reversed and random.random() < 0.5
        drawn.append(DrawnCard(card=card, reversed=reversed_card))

    return drawn


def get_card_by_name(name: str) -> Optional[Card]:
    """Look up a card by name."""
    for card in FULL_DECK:
        if card.name.lower() == name.lower():
            return card
    return None


def get_cards_by_element(element: str) -> List[Card]:
    """Get all cards of a specific element."""
    return [c for c in FULL_DECK if c.element == element]


def get_elemental_balance(cards: List[DrawnCard]) -> Dict[str, int]:
    """Calculate elemental balance of drawn cards."""
    balance = {"Fire": 0, "Water": 0, "Air": 0, "Earth": 0}
    for drawn in cards:
        balance[drawn.card.element] += 1
    return balance


def format_card_for_prompt(drawn: DrawnCard, position_name: str = None) -> str:
    """Format a drawn card for inclusion in a prompt."""
    parts = [drawn.display_name]

    if position_name:
        parts.insert(0, f"**{position_name}:**")

    parts.append(f"(Element: {drawn.card.element})")
    parts.append(f"Keywords: {', '.join(drawn.card.keywords)}")

    if drawn.card.arcana == "minor" and drawn.card.domain:
        parts.append(f"Domain: {drawn.card.domain}")

    return " | ".join(parts) if not position_name else "\n".join(parts)


if __name__ == "__main__":
    print(f"Total cards in deck: {len(FULL_DECK)}")
    print(f"  Major Arcana: {len(MAJOR_ARCANA)}")
    print(f"  Minor Arcana: {len(MINOR_ARCANA)}")

    print("\n--- Sample draw (5 cards) ---")
    for drawn in draw_cards(5):
        print(f"  {format_card_for_prompt(drawn)}")

    print("\n--- Elemental balance of 10-card draw ---")
    ten_draw = draw_cards(10)
    balance = get_elemental_balance(ten_draw)
    for element, count in balance.items():
        print(f"  {element}: {count}")
