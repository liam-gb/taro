"""
Batch file generator for Claude Max sessions.

Creates JSON batch files that Claude can read and process directly,
writing responses to corresponding output files.
"""

import json
from pathlib import Path
from typing import List, Optional
from dataclasses import asdict

from prompt_generator import (
    TrainingPrompt, load_prompts, format_prompt_for_claude
)


def create_batch_file(
    prompts: List[TrainingPrompt],
    batch_num: int,
    output_dir: Path
) -> Path:
    """
    Create a single batch file as JSON for Claude to process.

    The batch file contains all info Claude needs to generate responses
    and write them to the corresponding output file.
    """
    batch_data = {
        "batch_id": batch_num,
        "output_file": f"responses/batch_{batch_num:04d}_responses.jsonl",
        "prompts": []
    }

    for prompt in prompts:
        batch_data["prompts"].append({
            "id": prompt.id,
            "spread_name": prompt.spread_name,
            "question": prompt.question,
            "question_category": prompt.question_category,
            "formatted_prompt": format_prompt_for_claude(prompt),
            "cards": [asdict(c) for c in prompt.cards],
            "elemental_balance": prompt.elemental_balance
        })

    output_path = output_dir / f"batch_{batch_num:04d}.json"
    with open(output_path, 'w') as f:
        json.dump(batch_data, f, indent=2)

    return output_path


def generate_all_batches(
    prompts_path: Path,
    output_dir: Path,
    batch_size: int = 25,
    start_batch: int = 0,
    max_batches: Optional[int] = None
) -> List[Path]:
    """
    Generate all batch files from a prompts JSON file.

    Args:
        prompts_path: Path to prompts.json
        output_dir: Directory to save batch files
        batch_size: Number of prompts per batch
        start_batch: Starting batch number (for resuming)
        max_batches: Maximum number of batches to generate

    Returns:
        List of created batch file paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "responses").mkdir(exist_ok=True)

    prompts = load_prompts(prompts_path)
    print(f"Loaded {len(prompts)} prompts")

    # Filter to pending only
    pending = [p for p in prompts if p.generation_status == "pending"]
    print(f"  {len(pending)} pending prompts")

    # Calculate batches
    total_batches = (len(pending) + batch_size - 1) // batch_size
    if max_batches:
        total_batches = min(total_batches, max_batches)

    print(f"Generating {total_batches} batches of {batch_size} prompts each")

    batch_files = []
    for batch_num in range(start_batch, start_batch + total_batches):
        start_idx = (batch_num - start_batch) * batch_size
        end_idx = start_idx + batch_size
        batch_prompts = pending[start_idx:end_idx]

        if not batch_prompts:
            break

        batch_path = create_batch_file(batch_prompts, batch_num, output_dir)
        batch_files.append(batch_path)

        if (batch_num + 1) % 100 == 0:
            print(f"  Created {batch_num + 1} batches...")

    # Create index file with processing instructions
    index_path = output_dir / "batch_index.json"
    index_data = {
        "total_prompts": len(prompts),
        "pending_prompts": len(pending),
        "batch_size": batch_size,
        "total_batches": len(batch_files),
        "batch_files": [str(p.name) for p in batch_files],
        "instructions": "See PROCESSING_INSTRUCTIONS.md for how to process batches"
    }
    with open(index_path, 'w') as f:
        json.dump(index_data, f, indent=2)

    # Create processing instructions
    create_processing_instructions(output_dir, batch_size)

    print(f"\nCreated {len(batch_files)} batch files in {output_dir}")

    return batch_files


def create_processing_instructions(output_dir: Path, batch_size: int):
    """Create instructions file for Claude sessions."""
    instructions = f'''# Batch Processing Instructions

## For Claude (in new chat sessions)

When asked to process a batch, you will:

1. Read the batch file (e.g., `batch_0000.json`)
2. For each prompt in the batch, generate a tarot reading response
3. Write responses to the corresponding output file in JSONL format

## Response Guidelines

For each tarot reading:
- Interpret each card in its position context
- Address the querent's specific question
- Note reversed cards appropriately
- Consider elemental balance
- Weave a cohesive narrative (200-400 words)
- Be insightful but grounded - no fortune-telling

## Output Format

Write to `responses/batch_XXXX_responses.jsonl` with one JSON object per line:

```json
{{"id": "prompt_id_here", "response": "Your complete tarot reading..."}}
```

## Example Prompt for New Claude Session

```
Please process the tarot training batch at:
/home/user/taro/training/data/batches/batch_0000.json

Read each prompt, generate a tarot reading response following the guidelines,
and write the responses to:
/home/user/taro/training/data/batches/responses/batch_0000_responses.jsonl

Use JSONL format with one {{"id": "...", "response": "..."}} per line.
```

## Batch Processing Tips

- Process 5-10 batches per session for efficiency
- Each batch has {batch_size} prompts
- Total batches: See batch_index.json
- Check progress with: `python run.py status`
'''
    with open(output_dir / "PROCESSING_INSTRUCTIONS.md", 'w') as f:
        f.write(instructions)


def get_next_unprocessed_batches(
    batches_dir: Path,
    n: int = 5
) -> List[str]:
    """Find the next N batches that haven't been processed yet."""
    responses_dir = batches_dir / "responses"

    batch_files = sorted(batches_dir.glob("batch_*.json"))
    unprocessed = []

    for batch_file in batch_files:
        batch_num = batch_file.stem.split("_")[1]
        response_file = responses_dir / f"batch_{batch_num}_responses.jsonl"

        if not response_file.exists():
            unprocessed.append(batch_file.name)
            if len(unprocessed) >= n:
                break

    return unprocessed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate batch files for Claude")
    parser.add_argument("--prompts", type=str, default="../data/prompts.json")
    parser.add_argument("--output-dir", type=str, default="../data/batches")
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--next", type=int, default=None,
                       help="Show next N unprocessed batches")

    args = parser.parse_args()

    if args.next:
        batches_dir = Path(__file__).parent / args.output_dir
        unprocessed = get_next_unprocessed_batches(batches_dir, args.next)
        print(f"Next {len(unprocessed)} unprocessed batches:")
        for b in unprocessed:
            print(f"  {b}")
    else:
        prompts_path = Path(__file__).parent / args.prompts
        output_dir = Path(__file__).parent / args.output_dir
        generate_all_batches(
            prompts_path,
            output_dir,
            batch_size=args.batch_size,
            start_batch=args.start,
            max_batches=args.max_batches
        )
