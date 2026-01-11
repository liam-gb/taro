#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0024.json - Enhanced Version"""

import json
import re
import random

random.seed(42)  # For reproducibility

def parse_prompt(input_text):
    """Extract question, timing, and cards from input_text."""
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    timing = timing_match.group(1).strip() if timing_match else ""

    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    question = question_match.group(1).strip() if question_match else ""

    cards = []
    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+(?:\n[^\n\d][^\n]*)*)'
    for match in re.finditer(card_pattern, input_text):
        cards.append({
            'number': match.group(1),
            'position': match.group(2).strip(),
            'card': match.group(3).strip(),
            'keywords': match.group(4).strip(),
            'base_meaning': match.group(5).strip(),
            'position_context': match.group(6).strip()
        })

    element_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    elements = element_match.group(1).strip() if element_match else ""

    combo_match = re.search(r'Card Combinations:\n(.*?)(?:\n\nElemental|\Z)', input_text, re.DOTALL)
    combinations = combo_match.group(1).strip() if combo_match else ""

    return {
        'timing': timing,
        'question': question,
        'cards': cards,
        'elements': elements,
        'combinations': combinations
    }

def is_reversed(card_name):
    return "(reversed)" in card_name.lower()

def get_card_name(card_str):
    return re.sub(r'\s*\((?:upright|reversed)\)', '', card_str).strip()

def get_timing_desc(timing):
    """Extract clean timing description."""
    if '—' in timing:
        parts = timing.split('—')
        phase = re.sub(r'[^\w\s]', '', parts[0]).strip()
        desc = parts[1].strip()
        return phase, desc
    return timing, "reflection and growth"

def generate_reading(parsed):
    """Generate a tarot reading response."""
    question = parsed['question']
    cards = parsed['cards']

    if not cards:
        return generate_simple_reading(parsed)

    num_cards = len(cards)
    if num_cards == 1:
        return generate_single_card_reading(parsed)
    elif num_cards == 3:
        return generate_three_card_reading(parsed)
    elif num_cards >= 5:
        return generate_complex_reading(parsed)
    else:
        return generate_general_reading(parsed)

def generate_single_card_reading(parsed):
    """Generate a single card reading (200-300 words)."""
    question = parsed['question']
    card = parsed['cards'][0]
    phase, timing_desc = get_timing_desc(parsed['timing'])

    card_name = get_card_name(card['card'])
    reversed_status = is_reversed(card['card'])
    position = card['position']
    context = card['position_context']
    keywords = card['keywords']

    # Paragraph 1: Opening with question context and timing
    opening_templates = [
        f"Your question, \"{question}\" arrives during the {phase} phase, a time for {timing_desc.lower()}. This lunar energy invites you to approach your inquiry with both honesty and compassion.",
        f"As you contemplate \"{question}\" during this {phase} moon, the cosmic timing speaks to {timing_desc.lower()}. The universe aligns to offer you meaningful guidance.",
        f"The {phase} brings a potent time for {timing_desc.lower()}, making this the perfect moment to explore your question about {question.lower().rstrip('?')}. The cards respond with wisdom tailored to your current journey.",
    ]
    opening = random.choice(opening_templates)

    # Paragraph 2: Card interpretation with depth
    if reversed_status:
        card_para = f"The {card_name} appears reversed in the {position} position, drawing your attention inward. {context} When this card shows its reversed face, it suggests that the energy here is not absent but rather internalized or blocked. You may be experiencing these themes in ways that are less visible to others but deeply felt within yourself. The reversal asks you to examine what patterns need conscious attention before you can move forward with clarity."
    else:
        card_para = f"The {card_name} emerges in the {position} position with powerful presence. {context} The energy of this card encompasses {keywords.lower()}, and these themes are actively flowing through your situation right now. This is not merely symbolic but reflects real dynamics in your life that are ready to be acknowledged and worked with intentionally."

    # Paragraph 3: Synthesis connecting to question
    synthesis_templates = [
        f"In relation to your question, this card suggests that the answer lies in examining how {keywords.split(',')[0].strip().lower()} manifests in your choices. The path forward is not about dramatic transformation but rather about bringing awareness to what already exists.",
        f"Reflecting on your inquiry, the {card_name} illuminates a crucial aspect of your situation. The themes of {keywords.lower()} are not obstacles but doorways. Your question itself contains seeds of understanding that this card helps to water.",
        f"This guidance speaks directly to your question by revealing that {question.lower().rstrip('?')} may be approached through the lens of {keywords.split(',')[0].strip().lower()}. Sometimes the most profound answers come not from external sources but from recognizing what we already sense intuitively.",
    ]
    synthesis = random.choice(synthesis_templates)

    # Paragraph 4: Actionable insight
    action_templates = [
        f"As a practical step, take time today to journal about where these themes appear in your daily life. Notice without judgment, and allow insights to emerge naturally. Consider one small action you can take this week that honors the wisdom of the {card_name}.",
        f"Moving forward, create space for quiet reflection on the {card_name}'s message. Before making any significant decisions, pause and ask yourself how the energy of {keywords.split(',')[0].strip().lower()} might guide your choice. Trust that clarity will deepen as you remain present with this guidance.",
        f"Your actionable insight is to identify one specific area where you can apply this wisdom today. Small, conscious actions aligned with the {card_name}'s energy will create ripples of meaningful change. Return to this reading when you need reminding of the path illuminated here.",
    ]
    action = random.choice(action_templates)

    return f"{opening}\n\n{card_para}\n\n{synthesis}\n\n{action}"

def generate_three_card_reading(parsed):
    """Generate a three-card spread reading (250-350 words)."""
    question = parsed['question']
    cards = parsed['cards']
    phase, timing_desc = get_timing_desc(parsed['timing'])

    # Opening paragraph
    opening = f"Your question, \"{question}\" calls forth a revealing three-card spread during this {phase} phase. As a time of {timing_desc.lower()}, the current energy supports deep inquiry into the patterns that shape your situation. Let us explore what the cards reveal about your past influences, present circumstances, and future trajectory."

    # Card interpretations
    card_texts = []
    for card in cards:
        card_name = get_card_name(card['card'])
        reversed_status = is_reversed(card['card'])
        position = card['position']
        context = card['position_context']

        if reversed_status:
            text = f"In the {position} position, the {card_name} appears reversed. {context} This reversal indicates that the energy here operates beneath the surface, perhaps blocked or seeking integration. Pay attention to where this influence may be affecting you in subtle but significant ways."
        else:
            text = f"The {position} position reveals the {card_name} in its upright aspect. {context} This card's energy flows clearly through this part of your story, offering both insight and opportunity for conscious engagement."
        card_texts.append(text)

    cards_para = " ".join(card_texts)

    # Synthesis
    synthesis = f"Viewing this spread as a cohesive narrative, we see movement from {cards[0]['position']} through {cards[1]['position']} toward {cards[2]['position']}. The cards do not predict a fixed destiny but illuminate the energetic arc of your situation. Understanding these influences empowers you to make choices aligned with your highest good rather than reacting unconsciously to unseen forces."

    # Actionable insight
    final_card = get_card_name(cards[-1]['card'])
    action = f"As you integrate this reading, focus particularly on the {final_card} in your {cards[-1]['position']} position. Consider what concrete step you can take this week to work consciously with this energy. The guidance here is not passive but invites your active participation in shaping what unfolds."

    return f"{opening}\n\n{cards_para}\n\n{synthesis}\n\n{action}"

def generate_complex_reading(parsed):
    """Generate a complex multi-card reading (300-400 words)."""
    question = parsed['question']
    cards = parsed['cards']
    phase, timing_desc = get_timing_desc(parsed['timing'])
    combinations = parsed['combinations']
    elements = parsed['elements']

    # Opening
    opening = f"Your profound inquiry, \"{question}\" draws forth an extensive reading that illuminates multiple dimensions of your situation. During this {phase} moon, a time of {timing_desc.lower()}, the cards speak with particular clarity to those willing to listen deeply."

    # First group of key cards
    key_cards = cards[:3]
    card_paras = []
    for card in key_cards:
        card_name = get_card_name(card['card'])
        reversed_status = is_reversed(card['card'])
        position = card['position']
        context = card['position_context']

        if reversed_status:
            para = f"The {card_name} reversed in {position} reveals {context} This reversal suggests internalized or blocked energy requiring conscious attention."
        else:
            para = f"In the {position} position, {card_name} shows {context}"
        card_paras.append(para)

    primary_cards = " ".join(card_paras)

    # Additional cards
    additional_cards = ""
    if len(cards) > 3:
        additional = []
        for card in cards[3:6]:
            card_name = get_card_name(card['card'])
            position = card['position']
            context = card['position_context']
            additional.append(f"The {card_name} in {position} adds depth: {context}")
        additional_cards = " ".join(additional)

    # Combinations and synthesis
    combo_text = ""
    if combinations:
        combo_text = f"The interaction between cards holds special significance. {combinations} These combinations amplify certain themes, drawing your attention to where multiple energies converge."

    # Elemental synthesis
    synthesis = f"This reading weaves together a tapestry of influences. The elemental balance suggests that {elements.split()[0] if elements else 'various'} energies are prominent, indicating where your focus naturally gravitates. The cards together point toward a path that honors both your immediate needs and deeper aspirations."

    # Actionable insight
    action = f"To work with this reading, I encourage you to sit with each card individually before considering the whole. Notice which cards evoke the strongest response—your intuition knows which guidance is most timely. As a practical step, choose one insight that resonates and create a small daily practice around it, whether through journaling, meditation, or intentional action. Return to this reading as your understanding deepens."

    paragraphs = [opening, primary_cards]
    if additional_cards:
        paragraphs.append(additional_cards)
    if combo_text:
        paragraphs.append(combo_text)
    paragraphs.append(synthesis)
    paragraphs.append(action)

    return "\n\n".join(paragraphs)

def generate_general_reading(parsed):
    """Generate a reading for 2 or 4 cards (200-300 words)."""
    question = parsed['question']
    cards = parsed['cards']
    phase, timing_desc = get_timing_desc(parsed['timing'])

    opening = f"As you seek insight into \"{question}\" the cards respond with wisdom perfectly suited to this {phase} phase. This is a time for {timing_desc.lower()}, and your inquiry aligns with this cosmic rhythm."

    card_sections = []
    for card in cards:
        card_name = get_card_name(card['card'])
        reversed_status = is_reversed(card['card'])
        position = card['position']
        context = card['position_context']
        keywords = card['keywords']

        if reversed_status:
            section = f"The {card_name} appears reversed in the {position} position. {context} This reversal invites exploration of how {keywords.split(',')[0].strip().lower()} may be blocked or internalized in your experience."
        else:
            section = f"In the {position} position, {card_name} brings its upright wisdom. {context} The themes of {keywords.lower()} flow actively through this aspect of your situation."
        card_sections.append(section)

    cards_text = " ".join(card_sections)

    synthesis = f"Together, these cards illuminate a meaningful pattern surrounding your question. The answer you seek may not arrive as a simple yes or no, but rather as an invitation to deeper understanding. What emerges is a recognition that your inquiry touches on themes larger than the immediate question itself."

    action = f"As you move forward, consider how each card's message might inform your choices in the coming days. Pay attention to moments when these themes arise organically in your life. Trust your intuition to recognize which guidance is most relevant to each situation you encounter."

    return f"{opening}\n\n{cards_text}\n\n{synthesis}\n\n{action}"

def generate_simple_reading(parsed):
    """Fallback for edge cases."""
    question = parsed['question']
    phase, timing_desc = get_timing_desc(parsed['timing'])

    return f"Your question, \"{question}\" arrives during the {phase} phase, a time for {timing_desc.lower()}. The energy surrounding your inquiry suggests that the answer lies not in seeking external validation but in deepening your own awareness. This is a moment for patient reflection rather than hasty action.\n\nTake time today to sit quietly with your question. Allow wisdom to arise naturally without forcing answers to appear. Sometimes the most profound insights come when we stop grasping and simply remain present with our inquiry.\n\nTrust that clarity will emerge as you maintain an open and receptive stance. The universe speaks to those who create space to listen. Your practical step is simply to honor this pause, trusting that understanding will deepen in its own time."

def main():
    with open('/home/user/taro/training/data/batches_expanded/batch_0024.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    print(f"Processing {len(prompts)} prompts...")

    responses = []
    for i, prompt in enumerate(prompts):
        prompt_id = prompt['id']
        input_text = prompt['input_text']
        parsed = parse_prompt(input_text)
        reading = generate_reading(parsed)

        responses.append({
            'id': prompt_id,
            'response': reading
        })

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(prompts)} prompts...")

    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0024_responses.jsonl'
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"Written {len(responses)} responses to {output_path}")

if __name__ == '__main__':
    main()
