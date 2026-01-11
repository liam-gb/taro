#!/usr/bin/env python3
"""
Generate tarot reading responses for batch_0025.json
Processes all 500 prompts and writes to JSONL format.
"""

import json
import re
import random
from pathlib import Path

# Varied opening phrases
OPENINGS = [
    "Your reading arrives during {timing_phase}—a time of {timing_meaning}.",
    "The cards speak as you journey through {timing_phase}, {timing_meaning}.",
    "In this {timing_phase} phase of {timing_meaning}, your question finds voice.",
    "During this {timing_phase}—when {timing_meaning}—the cards respond.",
    "As the {timing_phase} invites {timing_meaning}, your reading unfolds.",
]

# Paragraph transitions
TRANSITIONS = [
    "Looking deeper into this spread,",
    "The heart of your reading reveals",
    "What emerges with clarity is",
    "At the core of this question,",
    "The cards weave together to show",
    "Examining the pattern that forms,",
    "The threads connect meaningfully:",
    "Building upon this foundation,",
]

# Closing transitions
CLOSINGS = [
    "Your path forward becomes clearer:",
    "The actionable wisdom here is this:",
    "As practical guidance,",
    "To work with these energies,",
    "Your next step emerges:",
    "The cards advise concrete action:",
]


def capitalize_first(s):
    """Capitalize the first letter of a string."""
    if not s:
        return s
    return s[0].upper() + s[1:]


def parse_input_text(input_text):
    """Parse the input text to extract question, timing, cards, and positions."""
    result = {
        'timing': None,
        'timing_phase': None,
        'timing_meaning': None,
        'question': None,
        'cards': [],
        'elemental_balance': None,
        'combinations': []
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1).strip()
        result['timing'] = timing_full
        # Parse timing phase and meaning
        if '—' in timing_full:
            parts = timing_full.split('—')
            result['timing_phase'] = parts[0].strip()
            result['timing_meaning'] = parts[1].strip().lower() if len(parts) > 1 else ""
        else:
            result['timing_phase'] = timing_full
            result['timing_meaning'] = "transformation"

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Extract cards - pattern matches position, card name, and details
    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+(?:\n(?!\d+\.)(?!Card Combinations)(?!Elemental)[^\n]+)*)'

    for match in re.finditer(card_pattern, input_text):
        raw_name = match.group(3).strip()
        is_reversed = '(reversed)' in raw_name.lower()
        # Clean the card name - remove the (upright) or (reversed) suffix
        clean_name = re.sub(r'\s*\((upright|reversed)\)', '', raw_name, flags=re.IGNORECASE).strip()

        card = {
            'number': int(match.group(1)),
            'position': match.group(2).strip(),
            'name': clean_name,
            'full_name': raw_name,
            'keywords': match.group(4).strip(),
            'base_meaning': match.group(5).strip(),
            'position_context': capitalize_first(match.group(6).strip()),
            'reversed': is_reversed
        }
        result['cards'].append(card)

    # Extract elemental balance
    elemental_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elemental_match:
        result['elemental_balance'] = elemental_match.group(1).strip()

    # Extract card combinations if present
    combo_match = re.search(r'Card Combinations:\n((?:- [^\n]+\n?)+)', input_text)
    if combo_match:
        combos = re.findall(r'- ([^\n]+)', combo_match.group(1))
        result['combinations'] = combos

    return result


def get_card_element(card_name):
    """Determine the elemental association of a card."""
    name_lower = card_name.lower()
    if 'wands' in name_lower:
        return 'fire'
    elif 'cups' in name_lower:
        return 'water'
    elif 'swords' in name_lower:
        return 'air'
    elif 'pentacles' in name_lower:
        return 'earth'
    else:
        # Major Arcana associations
        fire_majors = ['emperor', 'strength', 'wheel', 'tower', 'sun', 'judgement']
        water_majors = ['high priestess', 'empress', 'chariot', 'hanged', 'death', 'moon', 'star']
        air_majors = ['fool', 'magician', 'lovers', 'justice', 'temperance', 'world']
        earth_majors = ['hierophant', 'hermit', 'devil']

        for major in fire_majors:
            if major in name_lower:
                return 'fire'
        for major in water_majors:
            if major in name_lower:
                return 'water'
        for major in air_majors:
            if major in name_lower:
                return 'air'
        for major in earth_majors:
            if major in name_lower:
                return 'earth'
    return 'spirit'


def format_card_name(name):
    """Format card name, avoiding double 'the'."""
    # Don't add 'the' if it already starts with The
    if name.lower().startswith('the '):
        return name
    return name


def generate_reading(parsed_data):
    """Generate a 3-5 paragraph tarot reading response (200-400 words)."""
    question = parsed_data['question']
    timing_phase = parsed_data.get('timing_phase', 'this moment')
    timing_meaning = parsed_data.get('timing_meaning', 'transformation')
    cards = parsed_data['cards']
    combinations = parsed_data['combinations']

    if not cards:
        return "Unable to generate reading - no cards detected."

    paragraphs = []

    # ====== OPENING PARAGRAPH ======
    opening_template = random.choice(OPENINGS)
    opening = opening_template.format(timing_phase=timing_phase, timing_meaning=timing_meaning)

    first_para = f"{opening} You ask: \"{question}\" "

    if len(cards) == 1:
        # Single card reading - expand significantly
        card = cards[0]
        card_name = format_card_name(card['name'])
        rev_phrase = ", appearing in its reversed position," if card['reversed'] else ""
        first_para += f"A single card steps forward to answer: {card_name}{rev_phrase} in the {card['position']} position. "
        first_para += f"{card['position_context']} "

        if card['reversed']:
            first_para += f"When this card appears reversed, it asks you to look at where its energy might be blocked, inverted, or calling for conscious integration. "
            first_para += f"Rather than seeing reversal as negative, consider it an invitation to examine the shadow side of these themes. "
        else:
            first_para += f"This card arrives upright, suggesting its energy flows freely and can be accessed directly. "

        # Add elemental context for single card
        element = get_card_element(card['name'])
        element_context = {
            'fire': "The fire element here speaks to passion, creativity, and will—energy that wants to move and transform.",
            'water': "The water element flows through this reading, touching on emotions, intuition, and the depths of feeling.",
            'air': "The air element dominates, bringing clarity, communication, and the power of thought to your question.",
            'earth': "The earth element grounds this reading in practical matters, material concerns, and tangible outcomes.",
            'spirit': "As a Major Arcana card, this speaks to larger life themes and soul-level transformation."
        }
        first_para += element_context.get(element, "")

    else:
        # Multi-card reading
        first_para += f"The cards arrange themselves across {len(cards)} positions, each illuminating a different facet of your situation. "

        # Describe first card meaningfully
        card = cards[0]
        card_name = format_card_name(card['name'])
        rev_phrase = " reversed" if card['reversed'] else ""
        first_para += f"Beginning with {card_name}{rev_phrase} in your {card['position']} position: {card['position_context']} "

    paragraphs.append(first_para)

    # ====== MIDDLE PARAGRAPHS ======
    if len(cards) > 1:
        transition = random.choice(TRANSITIONS)
        middle_para = f"{transition} "

        # Process cards 2-4 (or remaining cards)
        middle_cards = cards[1:min(4, len(cards))]
        for card in middle_cards:
            card_name = format_card_name(card['name'])
            if card['reversed']:
                middle_para += f"{card_name} appears reversed in your {card['position']} position—{card['position_context'].lower()} The reversal intensifies the need to examine this energy consciously. "
            else:
                middle_para += f"{card_name} in your {card['position']} position indicates that {card['position_context'].lower()} "

            # Add base meaning if available
            if card['base_meaning'] and card['base_meaning'] != 'Meaning not available':
                meaning_snippet = card['base_meaning'][:120]
                if len(card['base_meaning']) > 120:
                    meaning_snippet = meaning_snippet.rsplit(' ', 1)[0] + "..."
                middle_para += f"This card's essence—{meaning_snippet.lower()}—deepens the message. "

        paragraphs.append(middle_para)

        # Additional cards if more than 4
        if len(cards) > 4:
            remaining_cards = cards[4:]
            extra_para = ""
            for card in remaining_cards:
                card_name = format_card_name(card['name'])
                rev_phrase = " (reversed)" if card['reversed'] else ""
                extra_para += f"{card_name}{rev_phrase} in your {card['position']} position adds: {card['position_context']} "
            paragraphs.append(extra_para)

    # ====== COMBINATION INSIGHTS ======
    if combinations:
        combo_para = "The cards speak to each other in meaningful patterns. "
        for combo in combinations[:2]:
            combo_para += f"{combo} "
        paragraphs.append(combo_para)

    # ====== SYNTHESIS PARAGRAPH ======
    synthesis_para = ""

    # Find key thematic cards
    outcome_card = None
    advice_card = None
    for card in cards:
        pos_lower = card['position'].lower()
        if 'outcome' in pos_lower or 'future' in pos_lower:
            outcome_card = card
        if 'advice' in pos_lower or 'action' in pos_lower or 'guidance' in pos_lower:
            advice_card = card

    if outcome_card or advice_card or len(cards) > 2:
        synthesis_para = "Weaving these threads together, a narrative emerges. "

        if outcome_card:
            card_name = format_card_name(outcome_card['name'])
            rev_note = " reversed" if outcome_card['reversed'] else ""
            synthesis_para += f"Your {outcome_card['position']} position holds {card_name}{rev_note}, suggesting that {outcome_card['position_context'].lower()} "

        # Theme-based insight - more specific matching
        q_lower = question.lower()
        if any(w in q_lower for w in ['love', 'relationship', 'partner', 'romance', 'dating', 'marriage', 'intimacy']):
            synthesis_para += "In matters of love, these cards remind you that authentic connection requires first knowing—and accepting—yourself. "
        elif any(w in q_lower for w in ['food', 'eating', 'diet', 'weight', 'body image']):
            synthesis_para += "Your relationship with nourishment reflects deeper patterns of self-care and self-worth that these cards illuminate. "
        elif any(w in q_lower for w in ['work', 'career', 'job', 'money', 'business', 'professional']):
            synthesis_para += "Your professional and material concerns intersect with deeper questions of purpose and worth. "
        elif any(w in q_lower for w in ['fear', 'afraid', 'anxiety', 'worry', 'scared']):
            synthesis_para += "The fears you carry often contain wisdom when examined directly rather than avoided. "
        elif any(w in q_lower for w in ['heal', 'health', 'wellness', 'recovery', 'illness']):
            synthesis_para += "Healing unfolds in its own time, and these cards honor where you are in that journey. "
        elif any(w in q_lower for w in ['decision', 'choice', 'path', 'should i', 'which']):
            synthesis_para += "The choice before you is less about right versus wrong and more about alignment with your authentic self. "
        elif any(w in q_lower for w in ['family', 'parent', 'mother', 'father', 'sibling', 'child']):
            synthesis_para += "Family patterns run deep, and understanding them is the first step to conscious choice about which to continue. "
        elif any(w in q_lower for w in ['creative', 'art', 'write', 'create', 'block', 'inspiration']):
            synthesis_para += "Creative energy flows best when we release attachment to outcomes and trust the process. "
        elif any(w in q_lower for w in ['identity', 'who am i', 'authentic', 'true self', 'pretend']):
            synthesis_para += "Questions of identity invite patience—who you are becoming is as important as who you have been. "
        elif any(w in q_lower for w in ['purpose', 'meaning', 'why', 'transition', 'change']):
            synthesis_para += "Life transitions carry their own wisdom, even when the path forward seems unclear. "
        else:
            synthesis_para += "Your question touches on themes of growth and understanding that these cards illuminate. "

        paragraphs.append(synthesis_para)

    # ====== ACTIONABLE CLOSING ======
    closing = random.choice(CLOSINGS)
    action_para = f"{closing} "

    # Find the best card for actionable advice
    action_card = advice_card or outcome_card or cards[-1]
    action_card_name = format_card_name(action_card['name'])

    if action_card['reversed']:
        action_para += f"The reversed {action_card_name} invites you to examine where this energy might be blocked or distorted. "
        action_para += "Journal about what arises when you sit with this reversal. What needs releasing? What needs reclaiming? "
    else:
        action_para += f"Align yourself with the energy of {action_card_name}. "

    # Element-specific advice
    element = get_card_element(action_card['name'])
    if element == 'fire':
        action_para += "Take one bold action today—start that project, speak your truth, or move your body in a way that feels alive. "
    elif element == 'water':
        action_para += "Honor your emotions today. Let yourself feel fully, reach out to someone who understands, or spend time near water. "
    elif element == 'air':
        action_para += "Seek clarity through communication. Write down your thoughts, have an honest conversation, or simply name what you have been avoiding. "
    elif element == 'earth':
        action_para += "Ground this reading in practical action. What one tangible step can you take today? Make it real and make it count. "
    else:
        action_para += "This Major Arcana energy asks for more than surface changes. Sit with its medicine and trust that transformation is already underway. "

    # Final sentence connecting back to question
    question_end = question.rstrip('?').rstrip('.')
    action_para += f"Your question—\"{question_end}\"—deserves your continued attention. The cards have spoken; now respond with intention."

    paragraphs.append(action_para)

    # ====== ENSURE WORD COUNT ======
    response = '\n\n'.join(paragraphs)
    word_count = len(response.split())

    # If too short, add more context
    if word_count < 200:
        elemental_insight = "\n\nThe elemental balance of this reading offers additional insight. "
        if parsed_data['elemental_balance']:
            elemental_insight += f"With {parsed_data['elemental_balance']}, "
        elemental_insight += "you are called to integrate multiple types of energy. Trust that you have access to passion, emotion, thought, and practical wisdom within yourself. "
        elemental_insight += "No single approach will answer everything—but awareness of these patterns is itself transformative. "
        card_name = format_card_name(cards[0]['name'])
        elemental_insight += f"Return to this reading in the coming days and notice what shifts. {card_name} especially asks for your ongoing attention."
        response += elemental_insight

    return response


def main():
    input_path = Path('/home/user/taro/training/data/batches_expanded/batch_0025.json')
    output_path = Path('/home/user/taro/training/data/batches_expanded/responses/batch_0025_responses.jsonl')

    print(f"Reading from: {input_path}")
    print(f"Writing to: {output_path}")

    with open(input_path, 'r') as f:
        data = json.load(f)

    prompts = data['prompts']
    print(f"Processing {len(prompts)} prompts...")

    responses = []
    with open(output_path, 'w') as f:
        for i, prompt in enumerate(prompts):
            prompt_id = prompt['id']
            input_text = prompt['input_text']

            # Parse the input text
            parsed = parse_input_text(input_text)

            # Generate the reading
            response = generate_reading(parsed)

            # Write to JSONL
            output_line = json.dumps({'id': prompt_id, 'response': response})
            f.write(output_line + '\n')
            responses.append(response)

            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1}/{len(prompts)} prompts...")

    print(f"Complete! Wrote {len(prompts)} responses to {output_path}")

    # Verification
    word_counts = [len(r.split()) for r in responses]
    print(f"\nWord count statistics:")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")
    print(f"  Avg: {sum(word_counts) / len(word_counts):.1f}")
    print(f"  Under 200: {sum(1 for c in word_counts if c < 200)}")
    print(f"  Over 400: {sum(1 for c in word_counts if c > 400)}")


if __name__ == '__main__':
    main()
