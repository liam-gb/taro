#!/usr/bin/env python3
"""
Main orchestration script for the Taro training data pipeline.

Usage:
    python run.py generate-prompts      # Generate ~25k prompts
    python run.py create-batches        # Create batch files for Claude Max
    python run.py merge-responses       # Merge responses from Claude
    python run.py convert-sft           # Convert to SFT format
    python run.py status                # Show progress
    python run.py test                  # Run quick test
"""

import argparse
import sys
from pathlib import Path

# Add scripts dir to path
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"


def cmd_generate_prompts(args):
    """Generate training prompts."""
    from prompt_generator import generate_dataset, get_dataset_stats

    output_path = DATA_DIR / "prompts.json"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    prompts = generate_dataset(
        target_count=args.count,
        output_path=output_path,
        seed=args.seed
    )

    stats = get_dataset_stats(prompts)
    print(f"\n✓ Generated {stats['total']} prompts")
    print(f"  Saved to: {output_path}")


def cmd_create_batches(args):
    """Create batch files for Claude Max."""
    from batch_generator import generate_all_batches

    prompts_path = DATA_DIR / "prompts.json"
    batches_dir = DATA_DIR / "batches"

    if not prompts_path.exists():
        print("Error: prompts.json not found. Run 'generate-prompts' first.")
        sys.exit(1)

    generate_all_batches(
        prompts_path,
        batches_dir,
        batch_size=args.batch_size,
        start_batch=args.start,
        max_batches=args.max_batches
    )

    print(f"\n✓ Batch files created in: {batches_dir}")
    print("\nNext steps:")
    print("1. In a new Claude session, ask Claude to process batch files")
    print("2. Claude reads batch_XXXX.json, writes to responses/batch_XXXX_responses.jsonl")
    print("3. Run 'merge-responses' when done")
    print("\nSee PROCESSING_INSTRUCTIONS.md in batches dir for details")


def cmd_merge_responses(args):
    """Merge Claude responses into prompts."""
    from response_parser import merge_responses_into_prompts, get_progress_report

    prompts_path = DATA_DIR / "prompts.json"
    responses_dir = DATA_DIR / "batches" / "responses"

    if not prompts_path.exists():
        print("Error: prompts.json not found.")
        sys.exit(1)

    if not responses_dir.exists():
        print(f"Error: responses directory not found at {responses_dir}")
        print("Process some batches first to generate response files.")
        sys.exit(1)

    merged, missing, errors = merge_responses_into_prompts(
        prompts_path, responses_dir
    )

    print(f"\n✓ Merged {merged} responses")
    if errors:
        print(f"  Warnings: {len(errors)}")

    print("\n" + get_progress_report(prompts_path))


def cmd_convert_sft(args):
    """Convert to SFT training format."""
    from convert_to_sft import convert_to_sft_format

    prompts_path = DATA_DIR / "prompts.json"
    sft_dir = DATA_DIR / "sft"

    if not prompts_path.exists():
        print("Error: prompts.json not found.")
        sys.exit(1)

    counts = convert_to_sft_format(
        prompts_path,
        sft_dir,
        format_type=args.format,
        train_ratio=args.train_ratio,
        valid_ratio=args.valid_ratio,
        seed=args.seed
    )

    print(f"\n✓ SFT data created in: {sft_dir}")
    print(f"  Train: {counts['train']}, Valid: {counts['valid']}, Test: {counts['test']}")
    print("\nNext: Run MLX fine-tuning:")
    print(f"  python -m mlx_lm.lora --model microsoft/Phi-4-mini-instruct \\")
    print(f"    --train --data {sft_dir} --iters 1000")


def cmd_status(args):
    """Show pipeline status."""
    from response_parser import get_progress_report
    from prompt_generator import load_prompts, get_dataset_stats

    prompts_path = DATA_DIR / "prompts.json"

    if not prompts_path.exists():
        print("No prompts.json found. Run 'generate-prompts' first.")
        return

    print(get_progress_report(prompts_path))

    # Check for batches
    batches_dir = DATA_DIR / "batches"
    if batches_dir.exists():
        batch_files = list(batches_dir.glob("batch_*.json"))
        print(f"\nBatch files: {len(batch_files)}")

        # Check for responses in batches/responses/
        responses_dir = batches_dir / "responses"
        if responses_dir.exists():
            response_files = list(responses_dir.glob("*.jsonl"))
            print(f"Response files: {len(response_files)}")
            if batch_files:
                pct = len(response_files) / len(batch_files) * 100
                print(f"Progress: {pct:.1f}%")

    # Check for SFT data
    sft_dir = DATA_DIR / "sft"
    if sft_dir.exists() and (sft_dir / "train.jsonl").exists():
        import json
        with open(sft_dir / "metadata.json") as f:
            meta = json.load(f)
        print(f"\nSFT data ready: {meta['total_examples']} examples")


def cmd_test(args):
    """Quick test of the pipeline."""
    print("=== Testing Pipeline ===\n")

    # Test imports
    print("1. Testing imports...")
    from questions import get_question_stats, sample_questions_weighted
    from cards import FULL_DECK, draw_cards
    from spreads import SPREADS, sample_spread_weighted
    from prompt_generator import generate_dataset, format_prompt_for_claude
    print("   ✓ All imports successful")

    # Test question generation
    print("\n2. Testing question generation...")
    stats = get_question_stats()
    print(f"   ✓ {stats['total_base_questions']} base questions in {stats['categories']} categories")

    # Test card drawing
    print("\n3. Testing card drawing...")
    cards = draw_cards(3)
    for c in cards:
        print(f"   - {c.display_name}")
    print("   ✓ Card drawing works")

    # Test spread sampling
    print("\n4. Testing spread sampling...")
    spread = sample_spread_weighted()
    print(f"   ✓ Sampled spread: {spread.name} ({len(spread.positions)} positions)")

    # Test prompt generation (small batch)
    print("\n5. Testing prompt generation (10 prompts)...")
    test_output = DATA_DIR / "test_prompts.json"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    prompts = generate_dataset(10, test_output, seed=42)
    print(f"   ✓ Generated {len(prompts)} prompts")

    # Show sample prompt
    print("\n6. Sample formatted prompt:")
    print("-" * 50)
    print(format_prompt_for_claude(prompts[0])[:500] + "...")
    print("-" * 50)

    # Cleanup
    test_output.unlink()
    print("\n✓ All tests passed!")


def main():
    parser = argparse.ArgumentParser(
        description="Taro Training Data Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py generate-prompts --count 25000
  python run.py create-batches --batch-size 25
  python run.py merge-responses
  python run.py convert-sft
  python run.py status
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # generate-prompts
    p = subparsers.add_parser("generate-prompts", help="Generate training prompts")
    p.add_argument("--count", type=int, default=25000, help="Number of prompts")
    p.add_argument("--seed", type=int, default=42, help="Random seed")

    # create-batches
    p = subparsers.add_parser("create-batches", help="Create batch files for Claude Max")
    p.add_argument("--batch-size", type=int, default=25, help="Prompts per batch")
    p.add_argument("--start", type=int, default=0, help="Starting batch number")
    p.add_argument("--max-batches", type=int, default=None, help="Max batches to create")

    # merge-responses
    p = subparsers.add_parser("merge-responses", help="Merge Claude responses")

    # convert-sft
    p = subparsers.add_parser("convert-sft", help="Convert to SFT format")
    p.add_argument("--format", choices=["chat", "instruct"], default="chat")
    p.add_argument("--train-ratio", type=float, default=0.9)
    p.add_argument("--valid-ratio", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=42)

    # status
    p = subparsers.add_parser("status", help="Show pipeline status")

    # test
    p = subparsers.add_parser("test", help="Run quick test")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Dispatch
    commands = {
        "generate-prompts": cmd_generate_prompts,
        "create-batches": cmd_create_batches,
        "merge-responses": cmd_merge_responses,
        "convert-sft": cmd_convert_sft,
        "status": cmd_status,
        "test": cmd_test,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
