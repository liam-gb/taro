"""
Convert completed prompts to SFT training format for MLX.
"""

import json
import random
from pathlib import Path
from typing import List, Dict

from prompt_generator import TrainingPrompt, load_prompts

SYSTEM_PROMPT = """You are a wise tarot reader with deep knowledge of card symbolism and archetypes. Provide thoughtful interpretations that:
- Honor traditional meanings while offering fresh perspectives
- Consider each card's position context
- Weave cards into a cohesive narrative
- Address the querent's question with empathy
- Note reversed cards as opportunities or internalized energies
- Offer guidance without fortune-telling"""


def format_for_phi(prompt: TrainingPrompt) -> Dict[str, str]:
    """Format for Phi chat template."""
    return {"text": f"""<|system|>
{SYSTEM_PROMPT}
<|end|>
<|user|>
{prompt.input_text}
<|end|>
<|assistant|>
{prompt.response}
<|end|>"""}


def convert_to_sft(
    prompts_path: Path,
    output_dir: Path,
    train_ratio: float = 0.9,
    valid_ratio: float = 0.05,
    seed: int = 42
) -> Dict[str, int]:
    """Convert to train/valid/test JSONL files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    prompts = load_prompts(prompts_path)
    completed = [p for p in prompts if p.status == "completed" and p.response]

    if not completed:
        raise ValueError("No completed prompts found")

    print(f"Converting {len(completed)} completed prompts")

    random.seed(seed)
    random.shuffle(completed)

    n = len(completed)
    train_end = int(n * train_ratio)
    valid_end = train_end + int(n * valid_ratio)

    splits = {
        "train": completed[:train_end],
        "valid": completed[train_end:valid_end],
        "test": completed[valid_end:]
    }

    counts = {}
    for name, data in splits.items():
        path = output_dir / f"{name}.jsonl"
        with open(path, 'w') as f:
            for p in data:
                f.write(json.dumps(format_for_phi(p)) + '\n')
        counts[name] = len(data)
        print(f"  {name}: {len(data)}")

    with open(output_dir / "metadata.json", 'w') as f:
        json.dump({"total_examples": len(completed), "splits": counts, "seed": seed}, f, indent=2)

    return counts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", default="../data/prompts.json")
    parser.add_argument("--output-dir", default="../data/sft")
    parser.add_argument("--train-ratio", type=float, default=0.9)
    parser.add_argument("--valid-ratio", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    base = Path(__file__).parent
    convert_to_sft(
        base / args.prompts,
        base / args.output_dir,
        args.train_ratio,
        args.valid_ratio,
        args.seed
    )
