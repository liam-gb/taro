"""
Convert completed prompts to SFT training format for MLX.

Outputs data in the JSONL format expected by mlx_lm.lora:
- train.jsonl
- valid.jsonl
- test.jsonl
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Tuple

from prompt_generator import TrainingPrompt, load_prompts, format_prompt_for_claude


# System prompt for Phi model fine-tuning
SYSTEM_PROMPT = """You are a wise and intuitive tarot reader with deep knowledge of card symbolism, archetypes, and the human experience. You provide thoughtful, insightful interpretations that:

- Honor traditional card meanings while offering fresh perspectives
- Consider each card's position and how it modifies the interpretation
- Weave individual card meanings into a cohesive narrative
- Address the querent's specific question with empathy and clarity
- Note elemental balance and its significance
- Offer guidance without fortune-telling or making absolute predictions
- Respect reversed cards as opportunities for growth or internalized energies

Provide readings that are grounded, helpful, and spiritually meaningful."""


def format_for_phi(prompt: TrainingPrompt) -> Dict[str, str]:
    """
    Format a completed prompt for Phi SFT training.

    Uses the Phi-3/Phi-4 chat template format:
    <|system|>...<|end|>
    <|user|>...<|end|>
    <|assistant|>...<|end|>
    """
    user_content = format_prompt_for_claude(prompt)

    # Phi chat format
    text = f"""<|system|>
{SYSTEM_PROMPT}
<|end|>
<|user|>
{user_content}
<|end|>
<|assistant|>
{prompt.claude_response}
<|end|>"""

    return {"text": text}


def format_for_phi_instruct(prompt: TrainingPrompt) -> Dict[str, str]:
    """
    Alternative format using instruction/input/output structure.

    Some fine-tuning setups prefer this explicit structure.
    """
    return {
        "instruction": SYSTEM_PROMPT,
        "input": format_prompt_for_claude(prompt),
        "output": prompt.claude_response
    }


def split_dataset(
    prompts: List[TrainingPrompt],
    train_ratio: float = 0.9,
    valid_ratio: float = 0.05,
    seed: int = 42
) -> Tuple[List[TrainingPrompt], List[TrainingPrompt], List[TrainingPrompt]]:
    """Split prompts into train/valid/test sets."""
    random.seed(seed)
    shuffled = prompts.copy()
    random.shuffle(shuffled)

    n = len(shuffled)
    train_end = int(n * train_ratio)
    valid_end = train_end + int(n * valid_ratio)

    return (
        shuffled[:train_end],
        shuffled[train_end:valid_end],
        shuffled[valid_end:]
    )


def convert_to_sft_format(
    prompts_path: Path,
    output_dir: Path,
    format_type: str = "chat",  # "chat" or "instruct"
    train_ratio: float = 0.9,
    valid_ratio: float = 0.05,
    seed: int = 42
) -> Dict[str, int]:
    """
    Convert prompts to SFT training format.

    Args:
        prompts_path: Path to prompts.json with completed responses
        output_dir: Directory to save train/valid/test files
        format_type: "chat" for Phi chat template, "instruct" for instruction format
        train_ratio: Fraction for training set
        valid_ratio: Fraction for validation set
        seed: Random seed for splitting

    Returns:
        Dict with counts for each split
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and filter to completed prompts
    prompts = load_prompts(prompts_path)
    completed = [p for p in prompts if p.generation_status == "completed" and p.claude_response]

    print(f"Loaded {len(prompts)} prompts, {len(completed)} completed")

    if len(completed) == 0:
        raise ValueError("No completed prompts found!")

    # Split
    train, valid, test = split_dataset(completed, train_ratio, valid_ratio, seed)

    print(f"Split: {len(train)} train, {len(valid)} valid, {len(test)} test")

    # Choose format function
    format_fn = format_for_phi if format_type == "chat" else format_for_phi_instruct

    # Write files
    counts = {}
    for name, data in [("train", train), ("valid", valid), ("test", test)]:
        output_path = output_dir / f"{name}.jsonl"
        with open(output_path, 'w') as f:
            for prompt in data:
                formatted = format_fn(prompt)
                f.write(json.dumps(formatted) + '\n')
        counts[name] = len(data)
        print(f"  Wrote {output_path} ({len(data)} examples)")

    # Write metadata
    metadata = {
        "source": str(prompts_path),
        "format_type": format_type,
        "system_prompt": SYSTEM_PROMPT,
        "total_examples": len(completed),
        "splits": counts,
        "seed": seed,
    }
    with open(output_dir / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    return counts


def preview_sft_example(prompts_path: Path, format_type: str = "chat") -> str:
    """Preview a single SFT example."""
    prompts = load_prompts(prompts_path)
    completed = [p for p in prompts if p.generation_status == "completed" and p.claude_response]

    if not completed:
        return "No completed prompts found"

    prompt = completed[0]
    format_fn = format_for_phi if format_type == "chat" else format_for_phi_instruct
    formatted = format_fn(prompt)

    return json.dumps(formatted, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert prompts to SFT format")
    parser.add_argument("--prompts", type=str, default="../data/prompts.json",
                       help="Path to prompts.json")
    parser.add_argument("--output-dir", type=str, default="../data/sft",
                       help="Output directory")
    parser.add_argument("--format", type=str, default="chat",
                       choices=["chat", "instruct"],
                       help="Output format type")
    parser.add_argument("--train-ratio", type=float, default=0.9,
                       help="Training set ratio")
    parser.add_argument("--valid-ratio", type=float, default=0.05,
                       help="Validation set ratio")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed")
    parser.add_argument("--preview", action="store_true",
                       help="Preview a single example")

    args = parser.parse_args()

    prompts_path = Path(__file__).parent / args.prompts

    if args.preview:
        print("=== SFT Example Preview ===\n")
        print(preview_sft_example(prompts_path, args.format))
    else:
        output_dir = Path(__file__).parent / args.output_dir
        counts = convert_to_sft_format(
            prompts_path,
            output_dir,
            format_type=args.format,
            train_ratio=args.train_ratio,
            valid_ratio=args.valid_ratio,
            seed=args.seed
        )
        print(f"\nConversion complete!")
        print(f"Total examples: {sum(counts.values())}")
