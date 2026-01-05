"""
Response parser for Claude outputs.
Parses JSONL responses and merges into prompts dataset.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

from prompt_generator import TrainingPrompt, load_prompts, save_prompts


def parse_jsonl(text: str) -> Tuple[List[Dict], List[str]]:
    """Parse JSONL response text, handling code blocks and malformed lines."""
    # Strip code block markers
    text = re.sub(r'```(?:json|jsonl)?\n?', '', text)
    text = re.sub(r'```', '', text)

    responses, errors = [], []

    for line in text.strip().split('\n'):
        line = line.strip()
        if not line or not line.startswith('{'):
            continue
        try:
            obj = json.loads(line)
            if 'id' in obj and 'response' in obj:
                responses.append(obj)
        except json.JSONDecodeError as e:
            errors.append(f"Parse error: {line[:50]}... ({e})")

    return responses, errors


def merge_responses(prompts_path: Path, response_dir: Path) -> Tuple[int, List[str]]:
    """Merge response files into prompts dataset."""
    prompts = load_prompts(prompts_path)
    by_id = {p.id: p for p in prompts}

    all_errors = []
    merged = 0

    for f in list(response_dir.glob("*.jsonl")) + list(response_dir.glob("*.txt")):
        responses, errors = parse_jsonl(f.read_text())
        all_errors.extend([f"{f.name}: {e}" for e in errors])

        for r in responses:
            if r['id'] in by_id:
                by_id[r['id']].response = r['response']
                by_id[r['id']].status = "completed"
                merged += 1
            else:
                all_errors.append(f"Unknown ID: {r['id']}")

        print(f"  {f.name}: {len(responses)} responses")

    save_prompts(prompts, prompts_path)
    return merged, all_errors


def get_progress_report(prompts_path: Path) -> str:
    """Generate progress report."""
    prompts = load_prompts(prompts_path)

    completed = [p for p in prompts if p.status == "completed"]
    pending = [p for p in prompts if p.status == "pending"]

    lengths = [len(p.response) for p in completed if p.response]
    avg_len = sum(lengths) / len(lengths) if lengths else 0

    return f"""{'='*50}
TRAINING DATA PROGRESS
{'='*50}
Total: {len(prompts)}
Completed: {len(completed)} ({len(completed)/len(prompts)*100:.1f}%)
Pending: {len(pending)}

Response lengths:
  Avg: {avg_len:.0f} chars
  Min: {min(lengths) if lengths else 0}
  Max: {max(lengths) if lengths else 0}
{'='*50}"""


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", default="../data/prompts.json")
    parser.add_argument("--responses", default="../data/batches/responses")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    base = Path(__file__).parent
    prompts_path = base / args.prompts

    if args.report:
        print(get_progress_report(prompts_path))
    else:
        merged, errors = merge_responses(prompts_path, base / args.responses)
        print(f"\nMerged {merged} responses")
        if errors:
            print(f"Errors: {len(errors)}")
        print(get_progress_report(prompts_path))
