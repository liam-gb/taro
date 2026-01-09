"""
Deep analysis of the 200 questions in the tarot training dataset.
Identifies gaps, missing themes, and suggests phrasing variations.
"""

from collections import defaultdict
from prompt_generator import QUESTIONS

# Define key themes/intents that questions should cover
THEMES = {
    "love": {
        "finding_love": ["find", "meet", "attract", "single"],
        "current_relationship": ["partner", "relationship", "marriage", "spouse"],
        "breakup_healing": ["breakup", "heal", "move on", "heartbreak", "ex"],
        "communication": ["communicate", "express", "tell", "saying"],
        "compatibility": ["compatible", "together", "future", "work out"],
        "trust_commitment": ["trust", "commit", "loyal", "faithful"],
        "self_love": ["love myself", "self-worth", "deserve"],
        "red_flags": ["warning", "toxic", "unhealthy"],
    },
    "career": {
        "job_change": ["change", "quit", "leave", "new job"],
        "promotion_growth": ["promotion", "advance", "grow", "success"],
        "purpose_fulfillment": ["purpose", "fulfill", "calling", "meaning"],
        "workplace_dynamics": ["coworker", "boss", "team", "office"],
        "entrepreneurship": ["business", "start", "own"],
        "compensation": ["raise", "salary", "compensat", "money", "pay"],
        "interview_job_search": ["interview", "apply", "job offer", "hire"],
        "burnout_stress": ["burnout", "stress", "overwhelm", "tired"],
    },
    "growth": {
        "life_purpose": ["purpose", "meant to", "destiny"],
        "shadow_work": ["shadow", "dark", "fear", "block"],
        "healing": ["heal", "wound", "trauma", "pain"],
        "spirituality": ["spiritual", "soul", "higher self", "divine"],
        "patterns_habits": ["pattern", "habit", "cycle", "repeat"],
        "self_improvement": ["improve", "better", "grow", "evolve"],
        "inner_child": ["inner child", "childhood", "past"],
        "authenticity": ["authentic", "true self", "mask"],
    },
    "health": {
        "physical_health": ["body", "physical", "health"],
        "energy_vitality": ["energy", "tired", "drain", "vital"],
        "mental_health": ["anxiety", "depress", "mental", "stress"],
        "balance_selfcare": ["balance", "self-care", "boundaries"],
        "mindbody": ["mind-body", "emotion", "psychosomatic"],
    },
    "family": {
        "parents": ["parent", "mother", "father", "mom", "dad"],
        "children": ["child", "kid", "parent", "son", "daughter"],
        "siblings": ["sibling", "brother", "sister"],
        "extended_family": ["family", "relatives"],
        "home_domestic": ["home", "house", "living"],
        "boundaries": ["boundary", "boundaries", "space"],
    },
    "money": {
        "general_finances": ["financial", "finances", "money"],
        "abundance_mindset": ["abundance", "prosperity", "wealth", "mindset"],
        "debt_challenges": ["debt", "struggle", "difficult"],
        "investments": ["invest", "grow", "opportunity"],
        "scarcity_fear": ["fear", "scarcity", "worry", "anxious"],
    },
    "decisions": {
        "big_choices": ["choose", "path", "option", "decision"],
        "timing": ["time", "when", "wait", "now"],
        "clarity": ["clarity", "certain", "confused", "unsure"],
        "intuition": ["trust", "gut", "intuition", "feel"],
        "direction": ["direction", "crossroads", "which way"],
    },
}

# Common question phrasings that should have variations
PHRASING_PATTERNS = [
    ("Will I...", "Am I going to...", "Is it likely that I..."),
    ("Should I...", "Is it wise to...", "Would it be good to..."),
    ("How can I...", "What steps can I take to...", "What would help me..."),
    ("What is...", "What does... mean", "Can you explain..."),
    ("Why do I...", "What causes me to...", "What's behind my..."),
    ("When will...", "How long until...", "Is the time right for..."),
]

# Life situations often asked about but potentially missing
MISSING_LIFE_SITUATIONS = {
    "love": [
        "long-distance relationships",
        "getting back together with an ex",
        "dealing with jealousy",
        "online dating",
        "age gap relationships",
        "polyamory/open relationships",
        "family disapproval of partner",
        "infidelity/cheating suspicions",
        "love languages",
        "intimacy issues",
    ],
    "career": [
        "remote work challenges",
        "career gap/returning to work",
        "imposter syndrome",
        "creative blocks",
        "retirement planning",
        "side hustle/second job",
        "toxic work environment",
        "being passed over for promotion",
        "discrimination at work",
        "work visa/relocation for job",
    ],
    "growth": [
        "grief and loss",
        "identity crisis",
        "major life transitions (divorce, empty nest)",
        "processing anger",
        "people-pleasing",
        "perfectionism",
        "procrastination",
        "comparison/envy",
        "finding community/belonging",
        "creative expression",
    ],
    "health": [
        "chronic illness/pain",
        "sleep issues",
        "addiction recovery",
        "eating disorders",
        "exercise/fitness motivation",
        "aging concerns",
        "body image",
        "fertility/pregnancy",
    ],
    "family": [
        "estranged family members",
        "caring for aging parents",
        "blended families/stepparents",
        "adoption/fostering",
        "inheritance disputes",
        "family secrets",
        "different values than family",
        "chosen family",
    ],
    "money": [
        "financial infidelity (partner)",
        "helping family financially",
        "student loans",
        "bankruptcy concerns",
        "gambling/spending addiction",
        "negotiating/asking for money",
        "career vs. money balance",
        "generational wealth/poverty",
    ],
    "decisions": [
        "moving/relocation",
        "ending friendships",
        "having children (or not)",
        "life-changing medical decisions",
        "coming out",
        "changing religion/beliefs",
        "forgiveness decisions",
        "pursuing dreams vs. stability",
    ],
}


def analyze_theme_coverage():
    """Analyze which themes are covered by current questions."""
    print("="*80)
    print("THEME COVERAGE ANALYSIS")
    print("="*80)

    for category, themes in THEMES.items():
        print(f"\n## {category.upper()}")
        questions = QUESTIONS.get(category, [])

        for theme_name, keywords in themes.items():
            matching = []
            for q in questions:
                q_lower = q.lower()
                if any(kw.lower() in q_lower for kw in keywords):
                    matching.append(q)

            coverage = len(matching)
            status = "✅" if coverage >= 3 else "⚠️" if coverage >= 1 else "❌"
            print(f"   {status} {theme_name}: {coverage} questions")
            if coverage == 0:
                print(f"      → MISSING: Need questions about {theme_name}")
            elif coverage < 3:
                print(f"      → LOW: Could add more variety")


def analyze_phrasing_diversity():
    """Check if questions use diverse phrasing patterns."""
    print("\n" + "="*80)
    print("PHRASING DIVERSITY ANALYSIS")
    print("="*80)

    all_questions = []
    for qs in QUESTIONS.values():
        all_questions.extend(qs)

    phrasing_counts = defaultdict(int)
    for q in all_questions:
        q_start = q.split()[0] if q else ""
        phrasing_counts[q_start] += 1

    print("\nQuestion starters distribution:")
    for starter, count in sorted(phrasing_counts.items(), key=lambda x: -x[1]):
        pct = 100 * count / len(all_questions)
        bar = "█" * int(pct / 2)
        print(f"   {starter:<12} {count:>4} ({pct:>5.1f}%) {bar}")

    # Check for diversity
    print("\nPhrasing Analysis:")
    top_starter = max(phrasing_counts.values())
    if top_starter > len(all_questions) * 0.4:
        print("⚠️  Over-reliance on one phrasing pattern")
    else:
        print("✅ Good phrasing diversity")


def identify_missing_questions():
    """Identify potentially missing question topics."""
    print("\n" + "="*80)
    print("POTENTIALLY MISSING QUESTION TOPICS")
    print("="*80)

    for category, situations in MISSING_LIFE_SITUATIONS.items():
        print(f"\n## {category.upper()}")
        questions = QUESTIONS.get(category, [])
        questions_text = " ".join(questions).lower()

        missing = []
        covered = []
        for situation in situations:
            keywords = situation.lower().split("/")
            if any(kw.strip() in questions_text for kw in keywords):
                covered.append(situation)
            else:
                missing.append(situation)

        if missing:
            print(f"   Missing topics ({len(missing)}):")
            for topic in missing:
                print(f"      ❌ {topic}")

        if covered:
            print(f"   Covered topics ({len(covered)}):")
            for topic in covered:
                print(f"      ✅ {topic}")


def suggest_question_variations():
    """Suggest variations for top questions."""
    print("\n" + "="*80)
    print("SUGGESTED QUESTION VARIATIONS (for top questions)")
    print("="*80)

    # Sample questions to show variations for
    key_questions = [
        ("Will I find love?", [
            "When will I meet my soulmate?",
            "Am I ready to attract love into my life?",
            "What's preventing me from finding love?",
            "Is love coming into my life soon?",
        ]),
        ("Should I change careers?", [
            "Is it time for a career pivot?",
            "Would changing my career path be wise right now?",
            "Am I meant to pursue a different profession?",
            "What would a career change bring me?",
        ]),
        ("What is my life purpose?", [
            "Why am I here?",
            "What is my soul's mission?",
            "What am I meant to do with my life?",
            "How do I discover my true calling?",
        ]),
        ("How can I improve my relationship?", [
            "What does my relationship need to thrive?",
            "What's the key to strengthening my partnership?",
            "How can we deepen our connection?",
            "What's missing in my relationship?",
        ]),
    ]

    for original, variations in key_questions:
        print(f"\n📝 Original: \"{original}\"")
        print("   Suggested variations:")
        for var in variations:
            in_data = "✓" if any(var.lower() in q.lower() for qs in QUESTIONS.values() for q in qs) else "+"
            print(f"      {in_data} \"{var}\"")


def generate_new_questions():
    """Generate recommended new questions to add."""
    print("\n" + "="*80)
    print("RECOMMENDED NEW QUESTIONS TO ADD")
    print("="*80)

    new_questions = {
        "love": [
            # Missing topics
            "How can I cope with a long-distance relationship?",
            "Should I give my ex another chance?",
            "How do I deal with jealousy in my relationship?",
            "What does my online dating experience reveal about me?",
            "Is my partner being faithful to me?",
            "How can I improve intimacy with my partner?",
            # Phrasing variations
            "When will I meet someone special?",
            "Is it wise to pursue this person?",
            "What steps can I take to find lasting love?",
        ],
        "career": [
            # Missing topics
            "How do I overcome imposter syndrome at work?",
            "What should I know about returning to work after a break?",
            "How can I handle a toxic work environment?",
            "Why was I passed over for promotion?",
            "Should I start a side business?",
            "How do I deal with burnout?",
            # Phrasing variations
            "What's blocking my professional growth?",
            "Is my current role aligned with my values?",
        ],
        "growth": [
            # Missing topics
            "How do I process grief and loss?",
            "What should I know about this identity crisis?",
            "How can I stop being a people-pleaser?",
            "What does my perfectionism teach me?",
            "Why do I keep procrastinating?",
            "How do I stop comparing myself to others?",
            # Phrasing variations
            "What's my next step in personal growth?",
            "Which shadow aspect needs my attention?",
        ],
        "health": [
            # Missing topics
            "How can I cope with chronic pain?",
            "What's affecting my sleep quality?",
            "How can I support my recovery journey?",
            "What does my body image struggle reveal?",
            "What do I need to know about my fertility journey?",
            # Phrasing variations
            "What's causing my lack of energy?",
            "How can I develop better self-care habits?",
        ],
        "family": [
            # Missing topics
            "Should I reconnect with my estranged family member?",
            "How can I balance caring for aging parents?",
            "What challenges will our blended family face?",
            "What should I know about adoption?",
            "How do I navigate having different values than my family?",
            # Phrasing variations
            "What does my family dynamic need?",
            "How can I establish healthy boundaries with relatives?",
        ],
        "money": [
            # Missing topics
            "How do I address financial issues with my partner?",
            "Should I lend money to family?",
            "How can I manage my student debt?",
            "What should I know about my spending patterns?",
            "How do I negotiate a higher salary?",
            # Phrasing variations
            "What's blocking my financial flow?",
            "Is this the right time to make this purchase?",
        ],
        "decisions": [
            # Missing topics
            "Should I relocate for this opportunity?",
            "Is it time to end this friendship?",
            "Am I ready to become a parent?",
            "How do I decide about forgiving this person?",
            "Should I follow my dreams or play it safe?",
            # Phrasing variations
            "What's the wisest path forward?",
            "How do I know when to wait vs. act?",
        ],
    }

    total_new = 0
    for category, questions in new_questions.items():
        print(f"\n## {category.upper()} ({len(questions)} new questions)")
        for q in questions:
            print(f"   + \"{q}\"")
            total_new += 1

    print(f"\n{'='*40}")
    print(f"Total new questions suggested: {total_new}")
    print(f"Current questions: 200")
    print(f"New total: {200 + total_new}")


def main():
    print("="*80)
    print("QUESTION COVERAGE DEEP ANALYSIS")
    print("="*80)

    # Count current questions
    total = sum(len(qs) for qs in QUESTIONS.values())
    print(f"\nCurrent question count: {total}")
    print("\nBy category:")
    for cat, qs in QUESTIONS.items():
        print(f"   {cat}: {len(qs)}")

    analyze_theme_coverage()
    analyze_phrasing_diversity()
    identify_missing_questions()
    suggest_question_variations()
    generate_new_questions()


if __name__ == "__main__":
    main()
