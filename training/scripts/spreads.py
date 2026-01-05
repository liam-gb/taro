"""
Tarot spread definitions for training data generation.

Mirrors the spread data from src/data/spreads.js.
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class Position:
    name: str
    description: str


@dataclass
class Spread:
    id: str
    name: str
    positions: List[Position]
    weight: float  # Distribution weight for sampling


SPREADS: Dict[str, Spread] = {
    "single": Spread(
        id="single",
        name="Daily Draw",
        positions=[
            Position("Today's Guidance", "Your guidance for today")
        ],
        weight=0.15,  # Single card readings are common but simple
    ),

    "threeCard": Spread(
        id="threeCard",
        name="Past · Present · Future",
        positions=[
            Position("Past", "What has led to this moment"),
            Position("Present", "Where you are now"),
            Position("Future", "Where this path leads"),
        ],
        weight=0.30,  # Most popular spread
    ),

    "situation": Spread(
        id="situation",
        name="Situation · Action · Outcome",
        positions=[
            Position("Situation", "The nature of what you face"),
            Position("Action", "The approach advised"),
            Position("Outcome", "The likely result"),
        ],
        weight=0.20,
    ),

    "horseshoe": Spread(
        id="horseshoe",
        name="Horseshoe",
        positions=[
            Position("Past", "What has shaped the situation"),
            Position("Present", "Current circumstances"),
            Position("Hidden Influences", "Factors not immediately apparent"),
            Position("Obstacles", "Challenges to overcome"),
            Position("External Influences", "People or events affecting you"),
            Position("Advice", "Guidance for moving forward"),
            Position("Outcome", "Where this path leads"),
        ],
        weight=0.15,
    ),

    "celtic": Spread(
        id="celtic",
        name="Celtic Cross",
        positions=[
            Position("Present", "Current situation"),
            Position("Challenge", "Obstacle you face"),
            Position("Past", "Recent influences"),
            Position("Future", "What's coming"),
            Position("Above", "Best outcome"),
            Position("Below", "Subconscious"),
            Position("Advice", "How to approach"),
            Position("External", "Outside influences"),
            Position("Hopes/Fears", "Inner conflict"),
            Position("Outcome", "Final result"),
        ],
        weight=0.20,  # Complex but classic
    ),
}


def get_spread(spread_id: str) -> Spread:
    """Get a spread by ID."""
    return SPREADS[spread_id]


def get_all_spreads() -> List[Spread]:
    """Return all spreads."""
    return list(SPREADS.values())


def sample_spread_weighted() -> Spread:
    """Sample a spread according to weights."""
    spreads = list(SPREADS.values())
    weights = [s.weight for s in spreads]
    return random.choices(spreads, weights=weights, k=1)[0]


def get_spread_stats() -> Dict:
    """Return statistics about spreads."""
    return {
        "total_spreads": len(SPREADS),
        "spreads": {
            s.id: {
                "name": s.name,
                "positions": len(s.positions),
                "weight": s.weight
            }
            for s in SPREADS.values()
        }
    }


if __name__ == "__main__":
    stats = get_spread_stats()
    print(f"Total spreads: {stats['total_spreads']}")
    print("\nSpreads:")
    for spread_id, info in stats['spreads'].items():
        print(f"  {info['name']}: {info['positions']} positions (weight: {info['weight']:.0%})")

    print("\n--- Sample weighted distribution (100 samples) ---")
    samples = [sample_spread_weighted().id for _ in range(100)]
    for spread_id in SPREADS:
        count = samples.count(spread_id)
        print(f"  {spread_id}: {count}%")
