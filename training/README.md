# Taro Training Data Pipeline

Generate fine-tuning data for Phi models using Claude Opus as teacher.

## Overview

This pipeline:
1. Generates ~25k diverse tarot reading prompts
2. Creates batch files that Claude can process directly
3. Parses and validates Claude responses
4. Converts to MLX SFT training format

## Quick Start

```bash
cd training/scripts

# Test the pipeline
python run.py test

# Generate prompts
python run.py generate-prompts --count 25000

# Create batch files
python run.py create-batches --batch-size 25

# Check progress
python run.py status
```

## Workflow

### 1. Generate Prompts

```bash
python run.py generate-prompts --count 25000
```

Creates `data/prompts.json` with 25k training examples distributed across:
- **Spreads**: Daily Draw (15%), Three Card (30%), Situation (20%), Horseshoe (15%), Celtic Cross (20%)
- **Questions**: Love (20%), Career (18%), Personal Growth (15%), Finances (12%), etc.

### 2. Create Batch Files

```bash
python run.py create-batches --batch-size 25
```

Creates JSON batch files in `data/batches/` that Claude can read directly.

### 3. Process Batches with Claude

In a new Claude Max session, use a prompt like:

```
Please process the tarot training batch at:
/path/to/taro/training/data/batches/batch_0000.json

For each prompt, generate a tarot reading (200-400 words) that:
- Interprets each card in its position context
- Addresses the querent's specific question
- Notes reversed cards appropriately
- Weaves a cohesive narrative

Write responses to:
/path/to/taro/training/data/batches/responses/batch_0000_responses.jsonl

Format: One JSON object per line: {"id": "...", "response": "..."}
```

**Batch Processing Tips:**
- Process 5-10 batches per Claude session
- Use `python run.py status` to check progress
- Find next unprocessed: `python scripts/batch_generator.py --next 5`

### 4. Merge Responses

```bash
python run.py merge-responses
```

### 5. Convert to SFT Format

```bash
python run.py convert-sft
```

Creates MLX-compatible data in `data/sft/`.

## Fine-Tuning with MLX

```bash
# Install MLX LM
pip install mlx-lm

# LoRA fine-tuning
python -m mlx_lm.lora \
  --model microsoft/Phi-4-mini-instruct \
  --train \
  --data ./data/sft \
  --iters 1000 \
  --batch-size 4

# Merge adapters
python -m mlx_lm.fuse \
  --model microsoft/Phi-4-mini-instruct \
  --adapter-path ./adapters \
  --save-path ./phi-tarot-merged
```

## Converting to GGUF for iOS

```bash
# Using llama.cpp
python convert_hf_to_gguf.py ./phi-tarot-merged --outfile phi-tarot.gguf
./llama-quantize phi-tarot.gguf phi-tarot-q4.gguf Q4_K_M
```

## File Structure

```
training/
├── README.md
├── scripts/
│   ├── run.py              # Main orchestration
│   ├── questions.py        # ~200 base questions
│   ├── cards.py            # 78 card definitions
│   ├── spreads.py          # 5 spread types
│   ├── prompt_generator.py # Assembles training prompts
│   ├── batch_generator.py  # Creates batch files
│   ├── response_parser.py  # Parses Claude responses
│   └── convert_to_sft.py   # Converts to MLX format
├── data/
│   ├── prompts.json        # All generated prompts
│   ├── batches/            # Batch files for Claude
│   │   ├── batch_0000.json
│   │   ├── batch_0001.json
│   │   ├── ...
│   │   └── responses/      # Claude's outputs
│   └── sft/                # Final training data
│       ├── train.jsonl
│       ├── valid.jsonl
│       └── test.jsonl
└── checkpoints/            # Fine-tuning outputs
```

## Estimated Timeline

- **Prompt generation**: ~1 minute for 25k prompts
- **Batch processing**: ~1000 batches × 25 prompts each
  - 5-10 batches per Claude session
  - ~100-200 sessions total
- **SFT conversion**: ~1 minute
- **Fine-tuning**: ~30-60 minutes on M4 MBP
