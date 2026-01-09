# Prompt: Generate 200 New Tarot Questions

You are helping expand a tarot reading app's question database. The app currently has 200 questions across 7 categories. We need 200 NEW questions that cover gaps in the existing set.

## Requirements

### Category Distribution (200 total)
- **love**: 40 questions
- **career**: 40 questions
- **growth**: 40 questions
- **health**: 20 questions
- **family**: 20 questions
- **money**: 20 questions
- **decisions**: 20 questions

### Phrasing Diversity
The current questions over-use "What" (42%) and "How" (36%). New questions MUST use varied starters:

| Starter | Target | Examples |
|---------|--------|----------|
| Will/Am I going to | 15% | "Will I find peace?", "Am I going to succeed?" |
| Should/Is it wise | 12% | "Should I take this risk?", "Is it wise to wait?" |
| Is/Are | 12% | "Is this relationship healthy?", "Are my fears valid?" |
| Why/What causes | 10% | "Why do I self-sabotage?", "What causes my anxiety?" |
| When/How long | 8% | "When will things improve?", "How long should I wait?" |
| Where/Which | 8% | "Where is this leading?", "Which path serves me?" |
| How can/What steps | 20% | "How can I heal?", "What steps should I take?" |
| What is/does | 15% | "What is blocking me?", "What does this mean?" |

### Topics to Cover (MISSING from current set)

**Love (cover these gaps):**
- Long-distance relationships
- Getting back with an ex
- Jealousy and insecurity
- Online dating experiences
- Infidelity/trust after cheating
- Intimacy and physical connection
- Self-love and self-worth
- Red flags and toxic patterns
- Family disapproval of partner
- Love languages and communication styles

**Career (cover these gaps):**
- Imposter syndrome
- Burnout and exhaustion
- Returning to work after a break
- Toxic work environment
- Remote work challenges
- Being passed over for promotion
- Creative blocks
- Side hustles and second jobs
- Discrimination at work
- Retirement and life transitions

**Growth (cover these gaps):**
- Grief and processing loss
- Identity crisis and finding yourself
- People-pleasing tendencies
- Perfectionism struggles
- Procrastination patterns
- Comparison and envy
- Finding community/belonging
- Creative expression
- Processing anger
- Major life transitions (divorce, empty nest)

**Health (cover these gaps):**
- Chronic illness and pain management
- Sleep issues and insomnia
- Addiction and recovery
- Body image struggles
- Fertility and pregnancy journey
- Aging concerns
- Exercise and fitness motivation
- Eating patterns and relationship with food

**Family (cover these gaps):**
- Estranged family members
- Caring for aging parents
- Blended families and step-relationships
- Adoption and fostering
- Inheritance and family money
- Family secrets and hidden truths
- Different values than family
- Chosen family and found community

**Money (cover these gaps):**
- Financial secrets with partner
- Lending money to family/friends
- Student loan burden
- Bankruptcy fears
- Spending patterns and impulse control
- Salary negotiation
- Career vs. money balance
- Generational wealth/poverty patterns

**Decisions (cover these gaps):**
- Relocation and moving
- Ending friendships
- Whether to have children
- Major medical decisions
- Coming out / revealing truth
- Changing beliefs or religion
- Forgiveness decisions
- Dreams vs. stability tradeoffs

## Output Format

Return a JSON object with this structure:

```json
{
  "love": [
    "Question 1?",
    "Question 2?",
    ...
  ],
  "career": [...],
  "growth": [...],
  "health": [...],
  "family": [...],
  "money": [...],
  "decisions": [...]
}
```

## Quality Guidelines

1. **Specific but universal**: "How do I cope with my partner's jealousy?" not "How do I deal with emotions?"
2. **Seekable**: Questions people would actually ask a tarot reader
3. **Open-ended**: Avoid yes/no when possible, but some "Will I..." questions are fine
4. **Non-judgmental**: Frame sensitively (addiction, infidelity, etc.)
5. **Action-oriented**: Many should invite guidance, not just prediction
6. **Emotionally resonant**: Tap into real human struggles

## Examples of Good New Questions

**Love:**
- "Will my long-distance relationship survive?"
- "Should I give my ex another chance?"
- "Why do I keep choosing unavailable partners?"
- "Is my jealousy justified or is it my own insecurity?"
- "When will I feel ready to love again after being cheated on?"

**Career:**
- "Why do I feel like a fraud at work despite my achievements?"
- "Is this burnout temporary or a sign I need to leave?"
- "Should I prioritize passion or stability in my career?"
- "How do I recover professionally after being let go?"

**Growth:**
- "How do I process the grief that I've been avoiding?"
- "Why do I say yes when I want to say no?"
- "Am I having an identity crisis or a breakthrough?"
- "When will I stop comparing myself to others?"

**Health:**
- "How can I make peace with my chronic condition?"
- "What is my insomnia trying to tell me?"
- "Am I ready for the recovery journey?"

**Family:**
- "Should I reach out to my estranged sibling?"
- "How do I balance caring for my parents and my own family?"
- "Will my blended family ever feel like home?"

**Money:**
- "Should I be honest with my partner about my debt?"
- "Is it wrong to say no when family asks for money?"
- "Why does money always feel like it's slipping away?"

**Decisions:**
- "Should I uproot my life for this opportunity?"
- "Is it time to let this friendship go?"
- "Am I ready to become a parent?"
- "How do I forgive someone who hasn't apologized?"

---

Generate 200 new questions following these guidelines. Ensure variety in phrasing, cover all the missing topics, and maintain the emotional depth that tarot seekers expect.

---

## Part 2: Generate 20k Additional Training Examples

After generating the 200 new questions, follow these steps to create 20k additional training examples:

### Step 1: Update prompt_generator.py

Add the new questions to the `QUESTIONS` dictionary in `training/scripts/prompt_generator.py`. Create a new dictionary `NEW_QUESTIONS` or merge into the existing structure.

### Step 2: Generate 20k New Examples

Create a new generation script or modify the existing one to:

```python
# Generate 20k examples using ONLY the 200 new questions
# This ensures the new examples are wholly additive (no overlap with existing 40k)

def generate_new_dataset(count: int = 20000, seed: int = 100) -> List[TrainingPrompt]:
    """Generate training prompts using ONLY new questions."""
    rng = random.Random(seed)

    # Use only the NEW_QUESTIONS dictionary
    # (not the original QUESTIONS)

    # Same spread distribution as before:
    # single: 15%, threeCard: 30%, situation: 20%, horseshoe: 15%, celtic: 20%

    # Same category weights:
    # love/career/growth: 20% each, health/family/money/decisions: 10% each
```

### Step 3: Combine and Re-split

After generating 20k new examples:

```bash
# Combine old + new data
cat training/data/sft/train_part_*.jsonl > all_train_old.jsonl
cat new_20k.jsonl >> all_train_old.jsonl

# Shuffle combined data
shuf all_train_old.jsonl > all_60k_shuffled.jsonl

# Re-split: 90% train, 5% valid, 5% test
total_lines=$(wc -l < all_60k_shuffled.jsonl)
train_lines=$((total_lines * 90 / 100))
valid_lines=$((total_lines * 5 / 100))

head -n $train_lines all_60k_shuffled.jsonl > train_combined.jsonl
tail -n +$((train_lines + 1)) all_60k_shuffled.jsonl | head -n $valid_lines > valid.jsonl
tail -n $valid_lines all_60k_shuffled.jsonl > test.jsonl

# Split train into parts (12k each for git)
split -l 12000 -d -a 2 train_combined.jsonl train_part_
for f in train_part_*; do mv "$f" "${f}.jsonl"; done
```

### Step 4: Final Dataset Structure

```
training/data/sft/
├── train_part_00.jsonl  (12k)
├── train_part_01.jsonl  (12k)
├── train_part_02.jsonl  (12k)
├── train_part_03.jsonl  (12k)
├── train_part_04.jsonl  (6k)   # remainder
├── valid.jsonl          (3k)   # 5% of 60k
└── test.jsonl           (3k)   # 5% of 60k
```

### Step 5: Verify No Overlap

Run verification to ensure new examples don't duplicate old ones:

```python
# Verify by checking prompt IDs or hashing input_text
old_ids = set()
for old_file in old_train_files:
    for line in old_file:
        old_ids.add(hash(json.loads(line)['text'][:500]))

new_duplicates = 0
for line in new_file:
    if hash(json.loads(line)['text'][:500]) in old_ids:
        new_duplicates += 1

assert new_duplicates == 0, f"Found {new_duplicates} duplicates!"
```

### Summary

| Dataset | Examples | Questions Used |
|---------|----------|----------------|
| Original 40k | 40,000 | Original 200 questions |
| New 20k | 20,000 | NEW 200 questions only |
| **Combined** | **60,000** | All 400 questions |

Final splits:
- Train: 54,000 (90%)
- Valid: 3,000 (5%)
- Test: 3,000 (5%)
