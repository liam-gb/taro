# Tarot Training Data Coverage Analysis Report

**Dataset**: 40,000 examples (36k train + 2k valid + 2k test)
**Date**: January 2026

---

## Executive Summary

| Metric | Status | Details |
|--------|--------|---------|
| **Card Coverage** | ✅ Excellent | All 78 cards appear 2,317-2,540 times (3.3% variance) |
| **Card-Position Coverage** | ✅ Excellent | 100% of 1,170 combinations covered |
| **Question Categories** | ✅ Excellent | Within 0.3% of targets |
| **Spread Distribution** | ✅ Excellent | Within 0.7% of targets |
| **Moon Phases** | ✅ Excellent | All 8 phases within 3% of uniform |
| **Reversal Ratio** | ✅ Correct | 49.9% (matches iOS 50% probability) |
| **Question Diversity** | ⚠️ Action Needed | Missing themes and phrasing over-reliance |

**Bottom Line**: The 40k dataset has excellent structural coverage. The main gaps are:
1. Question set is missing several real-life topics
2. Question phrasing is too homogeneous ("What/How" = 78%)

---

## 1. Card Coverage Analysis

### Summary Statistics
- **Total card appearances**: 189,379
- **Expected per card (uniform)**: 2,428
- **Range**: 2,317 - 2,540 (7.3% spread, excellent uniformity)
- **All 78 cards**: ✅ Appear 50+ times

### Most/Least Frequent Cards

| Rank | Most Frequent | Count | Least Frequent | Count |
|------|--------------|-------|----------------|-------|
| 1 | Two of Wands | 2,540 | The High Priestess | 2,317 |
| 2 | Death | 2,511 | Nine of Swords | 2,339 |
| 3 | The Star | 2,500 | Four of Swords | 2,346 |
| 4 | Two of Pentacles | 2,500 | The Hierophant | 2,352 |
| 5 | The Chariot | 2,498 | Five of Pentacles | 2,355 |

**Assessment**: Card coverage is excellent. No action needed.

---

## 2. Card-Position Coverage

| Metric | Value |
|--------|-------|
| Unique positions | 15 |
| Total possible combos | 1,170 (78 cards × 15 positions) |
| Combos with ≥1 example | 1,170 (100%) |
| Combos with <5 examples | 0 |

**Positions covered**: above, action, advice, below, challenge, external, future, hidden_influences, hopes_fears, obstacles, outcome, past, present, situation, todays_guidance

**Assessment**: Perfect coverage. No action needed.

---

## 3. Question Category Balance

| Category | Count | Actual % | Target % | Delta |
|----------|-------|----------|----------|-------|
| love | 8,052 | 20.1% | 20.0% | +0.1% ✅ |
| career | 8,113 | 20.3% | 20.0% | +0.3% ✅ |
| growth | 7,941 | 19.9% | 20.0% | -0.1% ✅ |
| health | 4,010 | 10.0% | 10.0% | +0.0% ✅ |
| family | 4,002 | 10.0% | 10.0% | +0.0% ✅ |
| money | 3,913 | 9.8% | 10.0% | -0.2% ✅ |
| decisions | 3,969 | 9.9% | 10.0% | -0.1% ✅ |

**Assessment**: Perfect balance. No action needed.

---

## 4. Spread Type Distribution

| Spread Type | Cards | Count | Actual % | Target % |
|-------------|-------|-------|----------|----------|
| Three-card (situation/PPF) | 3 | 20,124 | 50.3% | 50.0% |
| Celtic Cross | 10 | 8,095 | 20.2% | 20.0% |
| Horseshoe | 7 | 6,046 | 15.1% | 15.0% |
| Single (Daily Draw) | 1 | 5,735 | 14.3% | 15.0% |

**Assessment**: Well-balanced. Single card slightly under but acceptable.

---

## 5. Moon Phase Distribution

| Moon Phase | Count | % of Total | vs Expected |
|------------|-------|------------|-------------|
| New Moon | 4,942 | 12.4% | -1.2% ✅ |
| Waxing Crescent | 5,142 | 12.9% | +2.8% ✅ |
| First Quarter | 4,851 | 12.1% | -3.0% ✅ |
| Waxing Gibbous | 4,901 | 12.3% | -2.0% ✅ |
| Full Moon | 5,093 | 12.7% | +1.9% ✅ |
| Waning Gibbous | 4,911 | 12.3% | -1.8% ✅ |
| Last Quarter | 5,112 | 12.8% | +2.2% ✅ |
| Waning Crescent | 5,048 | 12.6% | +1.0% ✅ |

**Assessment**: All phases within 3% of uniform distribution. Excellent.

---

## 6. Reversal Ratio ✅

| Orientation | Count | Percentage |
|-------------|-------|------------|
| Reversed | 94,490 | 49.9% |
| Upright | 94,889 | 50.1% |

**iOS Probability**: 50%
**Training Data**: 49.9%
**Status**: ✅ **Matches iOS behavior**

---

## 7. Question Coverage Analysis ⚠️

### 7.1 Question Usage
- **Total unique questions**: 200
- **All questions used**: ✅ Yes
- **Usage range**: 158-241 times per question

| Most Used | Count | Least Used | Count |
|-----------|-------|------------|-------|
| When will conditions be favorable? | 241 | How can I heal from my past heartbreak? | 158 |
| What needs healing within me? | 237 | What do I need to know before getting engaged? | 167 |
| Why do I feel so drained lately? | 233 | What is my relationship with money? | 168 |

### 7.2 Theme Coverage Gaps

**Missing themes by category:**

| Category | Missing/Low Themes |
|----------|-------------------|
| **Love** | ❌ self_love, ❌ red_flags, ⚠️ trust_commitment |
| **Career** | ❌ burnout_stress, ⚠️ compensation, ⚠️ interview_job_search |
| **Growth** | ⚠️ life_purpose, ⚠️ self_improvement, ⚠️ inner_child, ⚠️ authenticity |
| **Health** | ⚠️ mental_health, ⚠️ balance_selfcare |
| **Family** | ⚠️ siblings, ⚠️ boundaries |
| **Money** | ⚠️ investments, ⚠️ scarcity_fear |
| **Decisions** | ⚠️ clarity, ⚠️ intuition, ⚠️ direction |

### 7.3 Missing Life Situations

Real-world topics NOT covered by current 200 questions:

**Love (10 missing)**:
- Long-distance relationships
- Getting back together with an ex
- Dealing with jealousy
- Online dating
- Infidelity/cheating suspicions
- Intimacy issues

**Career (10 missing)**:
- Imposter syndrome
- Career gap/returning to work
- Toxic work environment
- Burnout/overwork
- Remote work challenges
- Being passed over for promotion

**Growth (10 missing)**:
- Grief and loss
- Identity crisis
- People-pleasing
- Perfectionism
- Procrastination
- Comparison/envy

**Health (8 missing)**:
- Chronic illness/pain
- Sleep issues
- Addiction recovery
- Body image
- Fertility/pregnancy

**Family (8 missing)**:
- Estranged family members
- Caring for aging parents
- Blended families/stepparents
- Family secrets

**Money (8 missing)**:
- Financial infidelity
- Student loans
- Helping family financially
- Generational wealth/poverty

**Decisions (8 missing)**:
- Moving/relocation
- Having children (or not)
- Ending friendships
- Forgiveness decisions

### 7.4 Phrasing Diversity ⚠️

| Question Starter | Count | Percentage |
|-----------------|-------|------------|
| What | 84 | 42.0% |
| How | 72 | 36.0% |
| Is | 11 | 5.5% |
| Should | 8 | 4.0% |
| Am | 6 | 3.0% |
| Will | 5 | 2.5% |
| Why | 4 | 2.0% |
| Others | 10 | 5.0% |

**Issue**: "What" and "How" account for **78%** of all questions

**Recommendation**: Add more variety with:
- "Will I..." / "Am I going to..."
- "Is it time to..." / "When should I..."
- "Why do I..." / "What causes..."
- "Should I..." / "Would it be wise to..."
- "Where is this leading..." / "Which path..."

---

## 8. Recommendations for 10k Additional Examples

### 8.1 Priority Actions

| Priority | Action | Impact |
|----------|--------|--------|
| 🔴 High | Add new questions (see below) | Cover missing life topics |
| 🔴 High | Diversify question phrasing | Reduce "What/How" dominance |
| 🟢 Low | Maintain current category balance | Already excellent |

### 8.2 Recommended 10k Allocation

```
Category Allocation (maintains current balance):
├── love:      2,000 examples (20%)
├── career:    2,000 examples (20%)
├── growth:    2,000 examples (20%)
├── health:    1,000 examples (10%)
├── family:    1,000 examples (10%)
├── money:     1,000 examples (10%)
└── decisions: 1,000 examples (10%)
```

### 8.3 New Questions to Add (53 total)

**Love (9 new)**:
1. "How can I cope with a long-distance relationship?"
2. "Should I give my ex another chance?"
3. "How do I deal with jealousy in my relationship?"
4. "What does my online dating experience reveal about me?"
5. "Is my partner being faithful to me?"
6. "How can I improve intimacy with my partner?"
7. "When will I meet someone special?"
8. "Is it wise to pursue this person?"
9. "What steps can I take to find lasting love?"

**Career (8 new)**:
1. "How do I overcome imposter syndrome at work?"
2. "What should I know about returning to work after a break?"
3. "How can I handle a toxic work environment?"
4. "Why was I passed over for promotion?"
5. "Should I start a side business?"
6. "How do I deal with burnout?"
7. "What's blocking my professional growth?"
8. "Is my current role aligned with my values?"

**Growth (8 new)**:
1. "How do I process grief and loss?"
2. "What should I know about this identity crisis?"
3. "How can I stop being a people-pleaser?"
4. "What does my perfectionism teach me?"
5. "Why do I keep procrastinating?"
6. "How do I stop comparing myself to others?"
7. "What's my next step in personal growth?"
8. "Which shadow aspect needs my attention?"

**Health (7 new)**:
1. "How can I cope with chronic pain?"
2. "What's affecting my sleep quality?"
3. "How can I support my recovery journey?"
4. "What does my body image struggle reveal?"
5. "What do I need to know about my fertility journey?"
6. "What's causing my lack of energy?"
7. "How can I develop better self-care habits?"

**Family (7 new)**:
1. "Should I reconnect with my estranged family member?"
2. "How can I balance caring for aging parents?"
3. "What challenges will our blended family face?"
4. "What should I know about adoption?"
5. "How do I navigate having different values than my family?"
6. "What does my family dynamic need?"
7. "How can I establish healthy boundaries with relatives?"

**Money (7 new)**:
1. "How do I address financial issues with my partner?"
2. "Should I lend money to family?"
3. "How can I manage my student debt?"
4. "What should I know about my spending patterns?"
5. "How do I negotiate a higher salary?"
6. "What's blocking my financial flow?"
7. "Is this the right time to make this purchase?"

**Decisions (7 new)**:
1. "Should I relocate for this opportunity?"
2. "Is it time to end this friendship?"
3. "Am I ready to become a parent?"
4. "How do I decide about forgiving this person?"
5. "Should I follow my dreams or play it safe?"
6. "What's the wisest path forward?"
7. "How do I know when to wait vs. act?"

---

## 9. Conclusion

### Do We Need 10k More Examples?

**For model quality**: The current 40k dataset has excellent structural coverage. Adding 10k more examples is **not strictly necessary** for basic model training.

**However, 10k more examples would be valuable to**:
1. Expand the question set to cover missing life situations
2. Diversify question phrasing to handle user input variations

### Recommended Next Steps

1. **Generate 200 new questions**: Use `training/prompts/generate_new_questions.md`
2. **Expand QUESTIONS dict**: Add the new questions to prompt_generator.py
3. **Generate 10k new examples** with expanded generator
4. **Re-run coverage analysis** to verify improvements

---

*Generated by coverage_analysis.py and question_analysis.py*
