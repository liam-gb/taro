# Git LFS Setup Guide for Training Data

## Prerequisites
```bash
# Install Git LFS (if not already installed)
brew install git-lfs  # macOS
# or: apt install git-lfs  # Ubuntu

# Initialize LFS in your repo
git lfs install
```

## Track Large Files
```bash
# Track the training data files
git lfs track "training/data/prompts.json"
git lfs track "training/data/sft/train.jsonl"

# This creates/updates .gitattributes
git add .gitattributes
```

## Reconstitute Split Files
The current split files need to be merged before LFS tracking:

```bash
cd training

# Merge prompts
python3 -c "
import json
prompts = []
for i in [1,2,3]:
    with open(f'data/prompts_part_{i}.json') as f:
        prompts.extend(json.load(f))
with open('data/prompts.json', 'w') as f:
    json.dump(prompts, f)
print(f'Created prompts.json: {len(prompts)} entries')
"

# Merge train.jsonl
cat data/sft/train_part_*.jsonl > data/sft/train.jsonl

# Remove split files
rm data/prompts_part_*.json
rm data/sft/train_part_*.jsonl
```

## Commit and Push
```bash
# Add the reconstituted files (LFS will handle them)
git add training/data/prompts.json training/data/sft/train.jsonl

# Commit
git commit -m "refactor: Move training data to Git LFS"

# Push (LFS uploads happen automatically)
git push origin main
```

## Verify LFS
```bash
# Check what LFS is tracking
git lfs ls-files

# Check file status
git lfs status
```

## Notes
- GitHub LFS has storage limits (1GB free, then paid)
- LFS files are stored separately from regular git objects
- Clone will download LFS files automatically
- Use `git lfs pull` if LFS files weren't downloaded
