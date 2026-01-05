"""
Response parser for Claude Max outputs.

Parses JSONL responses from Claude chat sessions and merges them
back into the prompts dataset.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict

from prompt_generator import TrainingPrompt, load_prompts, save_prompts


def parse_jsonl_response(text: str) -> List[Dict]:
    """
    Parse JSONL response text from Claude.

    Handles various edge cases:
    - Code blocks (```json ... ```)
    - Mixed content with explanatory text
    - Malformed JSON lines

    Args:
        text: Raw text output from Claude

    Returns:
        List of parsed response dicts
    """
    responses = []
    errors = []

    # Remove code block markers if present
    text = re.sub(r'```(?:json|jsonl)?\n?', '', text)
    text = re.sub(r'```', '', text)

    # Try to find JSON objects
    # Pattern matches {"id": "...", "response": "..."}
    json_pattern = r'\{[^{}]*"id"\s*:\s*"[^"]+"\s*,\s*"response"\s*:\s*"(?:[^"\\]|\\.)*"\s*\}'

    # First try line-by-line parsing
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('//'):
            continue

        # Skip lines that don't look like JSON
        if not line.startswith('{'):
            continue

        try:
            obj = json.loads(line)
            if 'id' in obj and 'response' in obj:
                responses.append(obj)
        except json.JSONDecodeError as e:
            errors.append(f"Failed to parse: {line[:100]}... ({e})")

    # If line-by-line didn't work well, try regex extraction
    if len(responses) == 0:
        matches = re.findall(json_pattern, text, re.DOTALL)
        for match in matches:
            try:
                obj = json.loads(match)
                if 'id' in obj and 'response' in obj:
                    responses.append(obj)
            except json.JSONDecodeError:
                pass

    return responses, errors


def parse_response_file(file_path: Path) -> Tuple[List[Dict], List[str]]:
    """Parse a single response file."""
    with open(file_path) as f:
        text = f.read()
    return parse_jsonl_response(text)


def merge_responses_into_prompts(
    prompts_path: Path,
    response_dir: Path,
    output_path: Optional[Path] = None
) -> Tuple[int, int, List[str]]:
    """
    Merge all responses from a directory into the prompts dataset.

    Args:
        prompts_path: Path to prompts.json
        response_dir: Directory containing response files (*.txt or *.jsonl)
        output_path: Optional output path (defaults to prompts_path)

    Returns:
        Tuple of (merged_count, missing_count, errors)
    """
    prompts = load_prompts(prompts_path)
    prompts_by_id = {p.id: p for p in prompts}

    all_responses = []
    all_errors = []

    # Find response files
    response_files = list(response_dir.glob("*.txt")) + \
                     list(response_dir.glob("*.jsonl")) + \
                     list(response_dir.glob("responses_*.json"))

    print(f"Found {len(response_files)} response files")

    for file_path in response_files:
        responses, errors = parse_response_file(file_path)
        all_responses.extend(responses)
        all_errors.extend([f"{file_path.name}: {e}" for e in errors])
        print(f"  {file_path.name}: {len(responses)} responses, {len(errors)} errors")

    # Merge responses
    merged = 0
    missing = 0

    for resp in all_responses:
        prompt_id = resp['id']
        if prompt_id in prompts_by_id:
            prompts_by_id[prompt_id].claude_response = resp['response']
            prompts_by_id[prompt_id].generation_status = "completed"
            merged += 1
        else:
            missing += 1
            all_errors.append(f"Unknown prompt ID: {prompt_id}")

    # Save updated prompts
    output = output_path or prompts_path
    save_prompts(prompts, output)

    return merged, missing, all_errors


def validate_responses(prompts: List[TrainingPrompt]) -> Dict:
    """
    Validate response quality.

    Returns statistics about:
    - Completion status
    - Response lengths
    - Potential issues
    """
    stats = {
        "total": len(prompts),
        "completed": 0,
        "pending": 0,
        "failed": 0,
        "response_lengths": [],
        "too_short": [],  # < 100 chars
        "too_long": [],   # > 3000 chars
    }

    for p in prompts:
        if p.generation_status == "completed":
            stats["completed"] += 1
            if p.claude_response:
                length = len(p.claude_response)
                stats["response_lengths"].append(length)
                if length < 100:
                    stats["too_short"].append(p.id)
                elif length > 3000:
                    stats["too_long"].append(p.id)
        elif p.generation_status == "failed":
            stats["failed"] += 1
        else:
            stats["pending"] += 1

    # Calculate length stats
    if stats["response_lengths"]:
        lengths = stats["response_lengths"]
        stats["avg_length"] = sum(lengths) / len(lengths)
        stats["min_length"] = min(lengths)
        stats["max_length"] = max(lengths)
    else:
        stats["avg_length"] = 0
        stats["min_length"] = 0
        stats["max_length"] = 0

    return stats


def get_progress_report(prompts_path: Path) -> str:
    """Generate a progress report for the dataset."""
    prompts = load_prompts(prompts_path)
    stats = validate_responses(prompts)

    report = []
    report.append("=" * 50)
    report.append("TRAINING DATA GENERATION PROGRESS")
    report.append("=" * 50)
    report.append(f"Total prompts: {stats['total']}")
    report.append(f"Completed:     {stats['completed']} ({stats['completed']/stats['total']*100:.1f}%)")
    report.append(f"Pending:       {stats['pending']}")
    report.append(f"Failed:        {stats['failed']}")
    report.append("")
    report.append("Response Statistics:")
    report.append(f"  Average length: {stats['avg_length']:.0f} chars")
    report.append(f"  Min length:     {stats['min_length']} chars")
    report.append(f"  Max length:     {stats['max_length']} chars")
    report.append(f"  Too short (<100): {len(stats['too_short'])}")
    report.append(f"  Too long (>3000): {len(stats['too_long'])}")
    report.append("=" * 50)

    return "\n".join(report)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse and merge Claude responses")
    parser.add_argument("--prompts", type=str, default="../data/prompts.json",
                       help="Path to prompts.json")
    parser.add_argument("--responses", type=str, default="../data/responses",
                       help="Directory containing response files")
    parser.add_argument("--output", type=str, default=None,
                       help="Output path (defaults to prompts path)")
    parser.add_argument("--report", action="store_true",
                       help="Show progress report only")
    parser.add_argument("--test-parse", type=str, default=None,
                       help="Test parsing a single response file")

    args = parser.parse_args()

    prompts_path = Path(__file__).parent / args.prompts

    if args.test_parse:
        test_file = Path(args.test_parse)
        responses, errors = parse_response_file(test_file)
        print(f"Parsed {len(responses)} responses")
        for r in responses[:3]:
            print(f"  ID: {r['id']}, Response length: {len(r['response'])}")
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for e in errors[:5]:
                print(f"  {e}")

    elif args.report:
        print(get_progress_report(prompts_path))

    else:
        response_dir = Path(__file__).parent / args.responses
        output_path = Path(args.output) if args.output else None

        merged, missing, errors = merge_responses_into_prompts(
            prompts_path, response_dir, output_path
        )

        print(f"\nMerged {merged} responses")
        print(f"Missing prompt IDs: {missing}")
        if errors:
            print(f"\nErrors ({len(errors)}):")
            for e in errors[:10]:
                print(f"  {e}")

        print("\n" + get_progress_report(prompts_path))
