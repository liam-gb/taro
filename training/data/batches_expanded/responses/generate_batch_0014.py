#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0014.json"""

import json
import re
import random
import hashlib

# Card interpretation data
CARD_MEANINGS = {
    "The Fool": {
        "upright": "new beginnings, innocence, spontaneity, free spirit, taking a leap of faith",
        "reversed": "recklessness, fear of the unknown, holding back, poor judgment"
    },
    "The Magician": {
        "upright": "manifestation, resourcefulness, power, inspired action, willpower",
        "reversed": "manipulation, poor planning, untapped talents, deception"
    },
    "The High Priestess": {
        "upright": "intuition, sacred knowledge, divine feminine, subconscious mind",
        "reversed": "secrets, disconnected from intuition, withdrawal, silence"
    },
    "The Empress": {
        "upright": "femininity, beauty, nature, nurturing, abundance, fertility",
        "reversed": "creative block, dependence, emptiness, smothering"
    },
    "The Emperor": {
        "upright": "authority, structure, control, fatherhood, stability",
        "reversed": "tyranny, rigidity, coldness, excessive control, lack of discipline"
    },
    "The Hierophant": {
        "upright": "spiritual wisdom, tradition, conformity, institutions, beliefs",
        "reversed": "personal beliefs, freedom, challenging the status quo"
    },
    "The Lovers": {
        "upright": "love, harmony, relationships, values alignment, choices",
        "reversed": "self-love, disharmony, imbalance, misalignment of values"
    },
    "The Chariot": {
        "upright": "control, willpower, success, determination, direction",
        "reversed": "lack of control, aggression, obstacles, lack of direction"
    },
    "Strength": {
        "upright": "courage, persuasion, influence, compassion, inner strength",
        "reversed": "self-doubt, weakness, insecurity, low energy"
    },
    "The Hermit": {
        "upright": "soul-searching, introspection, solitude, inner guidance",
        "reversed": "isolation, loneliness, withdrawal, lost your way"
    },
    "Wheel of Fortune": {
        "upright": "good luck, karma, life cycles, destiny, turning point",
        "reversed": "bad luck, resistance to change, breaking cycles"
    },
    "Justice": {
        "upright": "fairness, truth, cause and effect, law, accountability",
        "reversed": "unfairness, lack of accountability, dishonesty"
    },
    "The Hanged Man": {
        "upright": "surrender, letting go, new perspective, pause, sacrifice",
        "reversed": "delays, resistance, stalling, indecision"
    },
    "Death": {
        "upright": "endings, change, transformation, transition, release",
        "reversed": "resistance to change, personal transformation delayed"
    },
    "Temperance": {
        "upright": "balance, moderation, patience, finding meaning, healing",
        "reversed": "imbalance, excess, self-healing, re-alignment"
    },
    "The Devil": {
        "upright": "shadow self, attachment, addiction, restriction, materialism",
        "reversed": "releasing limiting beliefs, exploring dark thoughts, detachment"
    },
    "The Tower": {
        "upright": "sudden change, upheaval, chaos, revelation, awakening",
        "reversed": "personal transformation, fear of change, averting disaster"
    },
    "The Star": {
        "upright": "hope, faith, purpose, renewal, spirituality, serenity",
        "reversed": "lack of faith, despair, discouragement, disconnection"
    },
    "The Moon": {
        "upright": "illusion, fear, anxiety, subconscious, intuition, dreams",
        "reversed": "release of fear, repressed emotion, inner confusion clearing"
    },
    "The Sun": {
        "upright": "positivity, fun, warmth, success, vitality, joy",
        "reversed": "inner child issues, overly optimistic, temporary depression"
    },
    "Judgement": {
        "upright": "judgment, rebirth, inner calling, absolution, self-evaluation",
        "reversed": "self-doubt, ignoring the call, harsh self-judgment"
    },
    "The World": {
        "upright": "completion, integration, accomplishment, travel, fulfillment",
        "reversed": "seeking closure, incomplete, empty, missing piece"
    }
}

# Opening phrases for variety
OPENINGS = [
    "The cards reveal a profound truth about your inquiry.",
    "Your reading speaks to the heart of your question.",
    "The spread before you illuminates hidden pathways.",
    "These cards carry significant wisdom for your situation.",
    "The energy of this reading resonates deeply with your question.",
    "What emerges from these cards is both challenging and illuminating.",
    "The universe offers clear guidance through this spread.",
    "Your inquiry has drawn forth meaningful insights.",
    "The cards align to address your deepest concerns.",
    "This reading cuts to the core of what you're asking."
]

# Transition phrases
TRANSITIONS = [
    "Looking deeper into this energy,",
    "As we examine the flow between these cards,",
    "The progression of the reading suggests",
    "What's particularly striking is",
    "Building on this foundation,",
    "The interplay of these energies reveals",
    "Moving through the spread,",
    "This energy connects meaningfully with",
    "The narrative that emerges shows",
    "Weaving these threads together,"
]

# Closing/actionable phrases
CLOSINGS = [
    "Your actionable guidance:",
    "Moving forward, consider this:",
    "The cards suggest you:",
    "Take this practical step:",
    "Your path forward involves:",
    "The reading asks you to:",
    "Here is your invitation:",
    "The wisdom here suggests:",
    "Consider taking this action:",
    "Your next step should be:"
]

def parse_prompt(input_text):
    """Parse the input_text to extract components."""
    result = {
        "timing": None,
        "question": None,
        "cards": [],
        "elemental_balance": None
    }

    # Extract timing/moon phase
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        result["timing"] = timing_match.group(1).strip()

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result["question"] = question_match.group(1).strip()

    # Extract cards with positions
    card_pattern = r'(\d+)\.\s*([^:]+):\s*([^\(]+)\s*\((\w+)\)\s*Keywords:\s*([^\n]+)\s*Base meaning:\s*([^\n]+)\s*Position context:\s*([^\n]+(?:\n(?!\d+\.)(?!Elemental)[^\n]+)*)'
    cards = re.findall(card_pattern, input_text, re.MULTILINE)

    for card in cards:
        result["cards"].append({
            "number": card[0],
            "position": card[1].strip(),
            "name": card[2].strip(),
            "orientation": card[3].strip().lower(),
            "keywords": card[4].strip(),
            "base_meaning": card[5].strip(),
            "position_context": card[6].strip()
        })

    # Extract elemental balance
    elem_match = re.search(r'Elemental Balance:\s*(\w+)', input_text)
    if elem_match:
        result["elemental_balance"] = elem_match.group(1).strip()

    return result

def get_reversal_note(card_name, is_reversed):
    """Generate reversal interpretation note."""
    if not is_reversed:
        return ""

    reversal_phrases = [
        f"The reversed {card_name} signals a need to look inward",
        f"With {card_name} appearing reversed, there's blocked or inverted energy",
        f"The reversal of {card_name} suggests internal rather than external focus",
        f"{card_name} reversed indicates this energy is working on a deeper, subconscious level",
        f"When {card_name} appears reversed, the message turns inward"
    ]
    return random.choice(reversal_phrases)

def generate_reading(prompt_data, prompt_id):
    """Generate a complete tarot reading response."""
    random.seed(hashlib.md5(prompt_id.encode()).hexdigest())

    parsed = parse_prompt(prompt_data["input_text"])
    question = parsed["question"] or prompt_data.get("question", "your situation")
    cards = parsed["cards"]
    timing = parsed["timing"]

    paragraphs = []

    # Opening paragraph - address question and set context
    opening = random.choice(OPENINGS)

    if timing:
        timing_context = f" The {timing.split('—')[0].strip()} phase amplifies this message, suggesting {timing.split('—')[1].strip().lower() if '—' in timing else 'a time of significant energy'}."
    else:
        timing_context = ""

    question_reflection = f'In asking "{question}", you\'ve opened yourself to receiving exactly what the cards now reveal.'

    if cards:
        first_card = cards[0]
        is_reversed = first_card["orientation"] == "reversed"
        rev_marker = " reversed" if is_reversed else ""
        card_name = first_card['name']
        card_article = "" if card_name.startswith("The ") else "the "

        opening_para = f"{opening}{timing_context} {question_reflection} {card_article.title() if card_article else ''}{card_name}{rev_marker} in the {first_card['position']} position immediately sets the tone: {first_card['position_context'].lower()}"

        if is_reversed:
            opening_para += f" {get_reversal_note(first_card['name'], True)}."

        paragraphs.append(opening_para)
    else:
        paragraphs.append(f"{opening}{timing_context} {question_reflection}")

    # Middle paragraphs - interpret remaining cards (limit to 2 middle cards for length)
    if len(cards) > 1:
        middle_cards = cards[1:-1] if len(cards) > 2 else cards[1:]
        middle_cards = middle_cards[:2]  # Limit to avoid overly long readings

        for card in middle_cards:
            transition = random.choice(TRANSITIONS)
            is_reversed = card["orientation"] == "reversed"
            rev_marker = " reversed" if is_reversed else ""
            card_name = card['name']
            card_article = "" if card_name.startswith("The ") else "the "

            para = f"{transition} {card_article}{card_name}{rev_marker} appearing in the {card['position']} position brings additional clarity. {card['position_context']}"

            if is_reversed:
                para += f" {get_reversal_note(card['name'], True)}."

            # Add interpretation based on keywords
            keywords = card["keywords"].split(",")
            if keywords:
                primary_keyword = keywords[0].strip()
                para += f" The theme of {primary_keyword} resonates strongly here, suggesting you examine how this energy manifests in your current situation."

            paragraphs.append(para)

    # Synthesis paragraph if multiple cards
    if len(cards) > 2:
        last_card = cards[-1]
        is_reversed = last_card["orientation"] == "reversed"
        rev_marker = " reversed" if is_reversed else ""
        card_name = last_card['name']
        card_article = "" if card_name.startswith("The ") else "The "
        first_card_name = cards[0]['name']
        first_article = "" if first_card_name.startswith("The ") else "the "

        synthesis = f"{card_article}{card_name}{rev_marker} in the {last_card['position']} position brings the reading full circle. {last_card['position_context']}"

        if is_reversed:
            synthesis += f" {get_reversal_note(card_name, True)}."

        # Weave narrative connection
        synthesis += f" When we consider how {first_article}{first_card_name} energy flows into this final card, a clear pattern emerges about your journey with {question.lower() if not question.endswith('?') else question[:-1].lower()}."

        paragraphs.append(synthesis)

    # Actionable insight paragraph
    closing = random.choice(CLOSINGS)

    action_suggestions = [
        "Take time this week to journal about what arose during this reading. Notice what resonates and what creates resistance—both are meaningful.",
        "Create a small ritual to honor the energy of these cards. Light a candle and spend ten minutes sitting with the primary message before taking any action.",
        "Share your insights with someone you trust, or write a letter to yourself that captures the wisdom you've received today.",
        "Choose one concrete action that aligns with the reading's guidance and commit to it within the next three days.",
        "Notice where in your body you felt the strongest response to these cards. That physical wisdom is guiding you toward truth.",
        "Before making any decisions related to your question, return to the central theme of this reading and ask yourself if your choice honors that message.",
        "Set an intention based on this reading and review it at the next moon phase. Notice how your perspective has shifted.",
        "Identify one limiting belief this reading has surfaced. Write it down, then write its opposite. Which feels more true to who you're becoming?",
        "The cards invite you to pause before reacting. When the situation arises again, take three breaths and remember what was revealed here.",
        "Find a quiet moment to meditate on the imagery of the central card. What details stand out? Those symbols hold personal meaning for you."
    ]

    # Select action based on question theme
    question_lower = question.lower()
    if any(word in question_lower for word in ["relationship", "love", "partner", "ex", "dating"]):
        specific_actions = [
            "Have an honest conversation with yourself about what you truly need in relationships before involving anyone else.",
            "Write down three non-negotiable boundaries and three areas where you can practice flexibility in love.",
            "Spend time alone this week noticing how you feel—not how you think you should feel."
        ]
    elif any(word in question_lower for word in ["career", "job", "work", "money", "business"]):
        specific_actions = [
            "Review your career goals and assess whether your daily actions align with where you want to be in five years.",
            "Identify one skill you can develop that would move you closer to your professional vision.",
            "Have a candid conversation with a mentor or trusted colleague about your path forward."
        ]
    elif any(word in question_lower for word in ["fear", "anxiety", "worry", "scared", "nervous"]):
        specific_actions = [
            "Name your fear specifically, write it down, and ask yourself: what would be true if this fear wasn't running the show?",
            "Practice a grounding technique daily for the next week. Notice how your relationship with anxiety shifts.",
            "Share your fear with someone safe. Speaking it aloud often diminishes its power."
        ]
    elif any(word in question_lower for word in ["decision", "choice", "should i", "choose"]):
        specific_actions = [
            "Write out both options and sit with each for a full day. Notice which one expands you and which contracts you.",
            "Imagine yourself one year from now having made each choice. Which future self feels more alive?",
            "Trust your first instinct, but give yourself permission to adjust course as you gather more information."
        ]
    else:
        specific_actions = action_suggestions

    final_action = random.choice(specific_actions)
    closing_para = f"{closing} {final_action} Remember that the cards illuminate possibilities, not certainties. You hold the power to shape your path forward."

    paragraphs.append(closing_para)

    # Ensure we have 3-5 paragraphs
    while len(paragraphs) < 3:
        filler = "The overall energy of this reading emphasizes the importance of staying present and trusting your inner wisdom. The patterns that emerge are not coincidental—they reflect deeper truths that are ready to be acknowledged and integrated into your conscious awareness."
        paragraphs.insert(-1, filler)

    reading = "\n\n".join(paragraphs)

    # Verify word count is in range
    word_count = len(reading.split())
    if word_count < 200:
        # Add elaboration
        elaboration = "\n\nThe elemental energies present in this reading—" + (parsed.get("elemental_balance") or "the dominant forces at play") + "—remind you to honor both your emotional truth and your practical wisdom. This is not a time for hasty action but for thoughtful integration of what has been revealed. Trust that clarity will continue to unfold as you sit with these messages."
        reading += elaboration

    # Cap at ~400 words if too long
    words = reading.split()
    if len(words) > 420:
        # Find a natural break point around 380-400 words
        truncated = ' '.join(words[:400])
        # Find last sentence end
        last_period = truncated.rfind('.')
        if last_period > 300:
            reading = truncated[:last_period + 1]
        else:
            reading = truncated + "."

    return reading

def main():
    """Process all prompts and generate responses."""
    # Load batch file
    with open('/home/user/taro/training/data/batches_expanded/batch_0014.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    print(f"Processing {len(prompts)} prompts...")

    # Generate responses
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0014_responses.jsonl'

    with open(output_path, 'w') as f:
        for i, prompt in enumerate(prompts):
            response = generate_reading(prompt, prompt['id'])

            output_line = json.dumps({
                "id": prompt['id'],
                "response": response
            })
            f.write(output_line + '\n')

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(prompts)} prompts")

    print(f"Completed! Wrote {len(prompts)} responses to {output_path}")

    # Verify output
    with open(output_path, 'r') as f:
        line_count = sum(1 for _ in f)
    print(f"Verification: {line_count} lines in output file")

if __name__ == "__main__":
    main()
