"""
Batch file generator for Claude Max sessions.
Creates JSON batches that Claude reads and processes directly.
"""

import json
from pathlib import Path
from typing import List, Optional

from prompt_generator import TrainingPrompt, load_prompts


def create_batch(prompts: List[TrainingPrompt], batch_num: int, output_dir: Path) -> Path:
    """Create a batch file with prompts for Claude to process."""
    batch_data = {
        "batch_id": batch_num,
        "output_file": f"responses/batch_{batch_num:04d}_responses.jsonl",
        "prompts": [{"id": p.id, "input": p.input_text} for p in prompts]
    }

    path = output_dir / f"batch_{batch_num:04d}.json"
    with open(path, 'w') as f:
        json.dump(batch_data, f, indent=2)
    return path


def generate_all_batches(
    prompts_path: Path,
    output_dir: Path,
    batch_size: int = 25,
    start_batch: int = 0,
    max_batches: Optional[int] = None
) -> List[Path]:
    """Generate batch files from prompts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "responses").mkdir(exist_ok=True)

    prompts = load_prompts(prompts_path)
    pending = [p for p in prompts if p.status == "pending"]

    print(f"Loaded {len(prompts)} prompts ({len(pending)} pending)")

    total_batches = (len(pending) + batch_size - 1) // batch_size
    if max_batches:
        total_batches = min(total_batches, max_batches)

    print(f"Creating {total_batches} batches of {batch_size} each")

    batch_files = []
    for i in range(total_batches):
        batch_num = start_batch + i
        start_idx = i * batch_size
        batch_prompts = pending[start_idx:start_idx + batch_size]

        if not batch_prompts:
            break

        path = create_batch(batch_prompts, batch_num, output_dir)
        batch_files.append(path)

        if (i + 1) % 100 == 0:
            print(f"  Created {i + 1} batches...")

    # Write index and instructions
    with open(output_dir / "batch_index.json", 'w') as f:
        json.dump({
            "total_prompts": len(prompts),
            "pending": len(pending),
            "batch_size": batch_size,
            "total_batches": len(batch_files),
        }, f, indent=2)

    with open(output_dir / "PROCESSING_INSTRUCTIONS.md", 'w') as f:
        f.write(f"""# Batch Processing Instructions

## For Claude (in new sessions)

Process batch files by reading the JSON and generating tarot readings.

### Guidelines
- Interpret each card in its position context
- Address the querent's question directly
- Note reversed cards appropriately
- 200-400 words per reading
- Be insightful but grounded

### Output Format
Write JSONL to `responses/batch_XXXX_responses.jsonl`:
```
{{"id": "abc123", "response": "Your tarot reading..."}}
{{"id": "def456", "response": "Your tarot reading..."}}
```

### Example Prompt
```
Process the tarot batch at:
training/data/batches/batch_0000.json

For each prompt, generate a tarot reading and write to:
training/data/batches/responses/batch_0000_responses.jsonl

Format: JSONL with {{"id": "...", "response": "..."}} per line.
```

Progress: `python run.py status`
""")

    print(f"Created {len(batch_files)} batch files in {output_dir}")
    return batch_files


def get_next_unprocessed(batches_dir: Path, n: int = 5) -> List[str]:
    """Find next N unprocessed batches."""
    responses_dir = batches_dir / "responses"
    unprocessed = []

    for batch_file in sorted(batches_dir.glob("batch_*.json")):
        batch_num = batch_file.stem.split("_")[1]
        if not (responses_dir / f"batch_{batch_num}_responses.jsonl").exists():
            unprocessed.append(batch_file.name)
            if len(unprocessed) >= n:
                break

    return unprocessed


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", default="../data/prompts.json")
    parser.add_argument("--output-dir", default="../data/batches")
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--max-batches", type=int)
    parser.add_argument("--next", type=int, help="Show next N unprocessed")
    args = parser.parse_args()

    base = Path(__file__).parent
    if args.next:
        batches = get_next_unprocessed(base / args.output_dir, args.next)
        print(f"Next {len(batches)} unprocessed: {batches}")
    else:
        generate_all_batches(
            base / args.prompts,
            base / args.output_dir,
            args.batch_size,
            args.start,
            args.max_batches
        )
