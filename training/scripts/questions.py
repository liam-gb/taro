"""
Question generation module for tarot training data.

Generates ~200 base questions across common tarot consultation categories,
with variation templates to expand the dataset.
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class QuestionCategory:
    name: str
    weight: float  # Distribution weight for sampling
    base_questions: List[str]
    variation_templates: List[str]  # Templates with {question} placeholder


# Question categories with base questions and variation templates
QUESTION_CATEGORIES: Dict[str, QuestionCategory] = {
    "love_relationships": QuestionCategory(
        name="Love & Relationships",
        weight=0.20,  # 20% of questions
        base_questions=[
            "Will I find love?",
            "Is my partner the one for me?",
            "Should I stay in my current relationship?",
            "Why do I keep attracting the wrong people?",
            "How can I improve my relationship?",
            "Is there someone new coming into my life?",
            "What is blocking me from finding love?",
            "Should I give my ex another chance?",
            "How does my partner really feel about me?",
            "Am I ready for a committed relationship?",
            "Will my marriage survive this rough patch?",
            "Is my crush interested in me?",
            "What do I need to learn from this relationship?",
            "Should I confess my feelings?",
            "How can I heal from my past heartbreak?",
            "What kind of partner should I be looking for?",
            "Is long distance worth pursuing?",
            "Why am I afraid of intimacy?",
            "Will we reconcile after our breakup?",
            "How can I attract a healthy relationship?",
            "What is the future of my relationship?",
            "Should I trust my partner?",
            "Am I settling in my relationship?",
            "How can I communicate better with my partner?",
            "Is this relationship serving my highest good?",
        ],
        variation_templates=[
            "{question}",
            "I've been wondering: {question}",
            "My question is about love: {question}",
            "Regarding my love life, {question}",
            "I need guidance on this: {question}",
        ]
    ),

    "career_work": QuestionCategory(
        name="Career & Work",
        weight=0.18,
        base_questions=[
            "Should I change careers?",
            "Will I get the promotion?",
            "Is this job right for me?",
            "How can I advance in my career?",
            "Should I start my own business?",
            "Will I find a new job soon?",
            "What is blocking my career success?",
            "Should I go back to school?",
            "How can I deal with my difficult coworker?",
            "Is it time to quit my job?",
            "What career path should I pursue?",
            "Will my business idea succeed?",
            "How can I find more fulfillment at work?",
            "Should I take this job offer?",
            "What skills should I develop?",
            "How do I handle workplace conflict?",
            "Is freelancing right for me?",
            "Will I achieve my professional goals?",
            "How can I improve my work-life balance?",
            "What's holding me back professionally?",
            "Should I ask for a raise?",
            "Is my current path aligned with my purpose?",
            "How can I overcome imposter syndrome?",
            "What does my career look like in the next year?",
            "Should I accept more responsibility at work?",
        ],
        variation_templates=[
            "{question}",
            "Career question: {question}",
            "About my work life, {question}",
            "I need career guidance: {question}",
            "Professionally speaking, {question}",
        ]
    ),

    "finances_money": QuestionCategory(
        name="Finances & Money",
        weight=0.12,
        base_questions=[
            "Will my financial situation improve?",
            "Should I make this investment?",
            "How can I attract more abundance?",
            "Is this a good time to buy a house?",
            "Will I get out of debt?",
            "Should I lend money to this person?",
            "What is my relationship with money?",
            "How can I be more financially stable?",
            "Is this financial opportunity legitimate?",
            "Will I receive unexpected money?",
            "Should I take this financial risk?",
            "How can I save more money?",
            "What blocks my financial abundance?",
            "Is now a good time for major purchases?",
            "How can I manifest prosperity?",
        ],
        variation_templates=[
            "{question}",
            "Money question: {question}",
            "Regarding my finances, {question}",
            "I need financial guidance: {question}",
        ]
    ),

    "personal_growth": QuestionCategory(
        name="Personal Growth & Spirituality",
        weight=0.15,
        base_questions=[
            "What is my life purpose?",
            "How can I become my best self?",
            "What lesson am I meant to learn right now?",
            "How can I develop my intuition?",
            "What is holding me back from growth?",
            "How can I find inner peace?",
            "What do I need to release?",
            "How can I be more authentic?",
            "What is my spiritual path?",
            "How can I overcome my fears?",
            "What does my higher self want me to know?",
            "How can I connect with my inner wisdom?",
            "What shadow aspects need attention?",
            "How can I raise my vibration?",
            "What is my soul trying to tell me?",
            "How can I practice better self-care?",
            "What patterns do I need to break?",
            "How can I cultivate more gratitude?",
            "What is my next step in personal evolution?",
            "How can I trust the universe more?",
            "What gifts am I not fully using?",
            "How can I heal my inner child?",
            "What boundaries do I need to set?",
            "How can I live more mindfully?",
            "What is blocking my happiness?",
        ],
        variation_templates=[
            "{question}",
            "For my personal growth: {question}",
            "Spiritually, {question}",
            "I'm seeking insight: {question}",
            "On my journey of self-discovery, {question}",
        ]
    ),

    "family_home": QuestionCategory(
        name="Family & Home",
        weight=0.10,
        base_questions=[
            "How can I improve my family relationships?",
            "Should I move to a new place?",
            "How can I set boundaries with family?",
            "Will my family situation improve?",
            "How can I heal family wounds?",
            "Is this the right home for me?",
            "How can I be a better parent?",
            "Should I reconnect with estranged family?",
            "What does my family need from me?",
            "How can I create more harmony at home?",
            "Is it time to start a family?",
            "How can I support my aging parents?",
            "What family patterns am I repeating?",
            "Should I have children?",
            "How can I balance family and personal needs?",
        ],
        variation_templates=[
            "{question}",
            "About my family: {question}",
            "Regarding home life, {question}",
            "Family matter: {question}",
        ]
    ),

    "health_wellbeing": QuestionCategory(
        name="Health & Wellbeing",
        weight=0.08,
        base_questions=[
            "How can I improve my health?",
            "What is my body trying to tell me?",
            "How can I have more energy?",
            "What lifestyle changes should I make?",
            "How can I manage stress better?",
            "What is affecting my wellbeing?",
            "How can I develop healthier habits?",
            "What does my body need right now?",
            "How can I heal emotionally?",
            "What is blocking my vitality?",
            "How can I sleep better?",
            "What self-care practices serve me best?",
        ],
        variation_templates=[
            "{question}",
            "Health question: {question}",
            "For my wellbeing: {question}",
        ]
    ),

    "decisions_crossroads": QuestionCategory(
        name="Decisions & Crossroads",
        weight=0.10,
        base_questions=[
            "What should I do about this situation?",
            "Which path should I choose?",
            "What am I not seeing clearly?",
            "What will happen if I make this choice?",
            "How can I make this decision?",
            "What factors should I consider?",
            "Is this the right time to act?",
            "Should I wait or move forward?",
            "What are the consequences of each option?",
            "How can I trust my decision-making?",
            "What does my gut tell me?",
            "Am I overthinking this decision?",
            "What would I regret not doing?",
            "Is fear clouding my judgment?",
            "What is the wisest course of action?",
        ],
        variation_templates=[
            "{question}",
            "I'm at a crossroads: {question}",
            "Help me decide: {question}",
            "I need clarity on: {question}",
        ]
    ),

    "general_guidance": QuestionCategory(
        name="General Guidance",
        weight=0.07,
        base_questions=[
            "What do I need to know right now?",
            "What message does the universe have for me?",
            "What should I focus on today?",
            "What energy surrounds me?",
            "What opportunities are coming?",
            "What challenges should I prepare for?",
            "What is the theme of this week/month?",
            "What do I need to be aware of?",
            "What blessings are coming my way?",
            "What should I be grateful for?",
            "What is my current energy?",
            "What does the day/week hold for me?",
        ],
        variation_templates=[
            "{question}",
            "General reading: {question}",
            "I'm seeking guidance: {question}",
        ]
    ),
}


def get_all_base_questions() -> List[Dict[str, str]]:
    """Return all base questions with their categories."""
    questions = []
    for cat_id, category in QUESTION_CATEGORIES.items():
        for q in category.base_questions:
            questions.append({
                "question": q,
                "category": cat_id,
                "category_name": category.name
            })
    return questions


def generate_question_variation(question: str, category_id: str) -> str:
    """Generate a variation of a question using category templates."""
    category = QUESTION_CATEGORIES[category_id]
    template = random.choice(category.variation_templates)
    return template.format(question=question)


def sample_questions_weighted(n: int, with_variations: bool = True) -> List[Dict[str, str]]:
    """
    Sample n questions according to category weights.

    Args:
        n: Number of questions to sample
        with_variations: Whether to apply variation templates

    Returns:
        List of question dicts with category info
    """
    # Build weighted list of (category_id, question) tuples
    weighted_pool = []
    for cat_id, category in QUESTION_CATEGORIES.items():
        for q in category.base_questions:
            weighted_pool.extend([(cat_id, q)] * int(category.weight * 100))

    samples = []
    for _ in range(n):
        cat_id, question = random.choice(weighted_pool)
        category = QUESTION_CATEGORIES[cat_id]

        if with_variations:
            question = generate_question_variation(question, cat_id)

        samples.append({
            "question": question,
            "category": cat_id,
            "category_name": category.name
        })

    return samples


def get_question_stats() -> Dict:
    """Return statistics about the question bank."""
    total = sum(len(c.base_questions) for c in QUESTION_CATEGORIES.values())
    by_category = {
        cat_id: {
            "name": cat.name,
            "count": len(cat.base_questions),
            "weight": cat.weight,
            "variations": len(cat.variation_templates)
        }
        for cat_id, cat in QUESTION_CATEGORIES.items()
    }
    return {
        "total_base_questions": total,
        "categories": len(QUESTION_CATEGORIES),
        "by_category": by_category
    }


if __name__ == "__main__":
    # Print stats
    stats = get_question_stats()
    print(f"Total base questions: {stats['total_base_questions']}")
    print(f"Categories: {stats['categories']}")
    print("\nBy category:")
    for cat_id, info in stats['by_category'].items():
        print(f"  {info['name']}: {info['count']} questions (weight: {info['weight']:.0%})")

    print("\n--- Sample questions with variations ---")
    for q in sample_questions_weighted(10):
        print(f"  [{q['category_name']}] {q['question']}")
