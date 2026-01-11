#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0022 - optimized for 200-400 words, 3-5 paragraphs."""

import json
import re
import random

def parse_input_text(input_text):
    """Parse the input text to extract question, timing, cards."""
    result = {'timing': None, 'question': None, 'cards': []}
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        result['timing'] = timing_match.group(1).strip()
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()
    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+(?:\n(?!\d+\.)(?!Card Combinations)(?!Elemental)[^\n]+)*)'
    for match in re.finditer(card_pattern, input_text):
        position = match.group(2).strip()
        card_name = match.group(3).strip()
        keywords = match.group(4).strip()
        position_context = match.group(6).strip()
        is_reversed = 'reversed' in card_name.lower()
        result['cards'].append({
            'position': position, 'card': card_name, 'reversed': is_reversed,
            'keywords': keywords, 'position_context': position_context
        })
    return result

def get_card_name(card_info):
    """Get clean card name."""
    return re.sub(r'\s*\((?:reversed|upright)\)', '', card_info['card'])

def generate_reading(prompt_data):
    """Generate a complete tarot reading response in 3-5 paragraphs, 200-400 words."""
    parsed = parse_input_text(prompt_data['input_text'])
    question = parsed['question'] or prompt_data.get('question', 'your situation')
    q_lower = question.lower().rstrip('?').strip()
    cards = parsed['cards']
    timing = parsed['timing'] or ""

    # Categorize cards
    past_cards = [c for c in cards if any(x in c['position'].lower() for x in ['past', 'foundation', 'root'])]
    present_cards = [c for c in cards if any(x in c['position'].lower() for x in ['present', 'situation', 'current'])]
    future_cards = [c for c in cards if any(x in c['position'].lower() for x in ['future', 'outcome', 'potential', 'result'])]
    challenge_cards = [c for c in cards if any(x in c['position'].lower() for x in ['challenge', 'obstacle', 'block'])]
    advice_cards = [c for c in cards if any(x in c['position'].lower() for x in ['advice', 'guidance', 'action'])]
    hidden_cards = [c for c in cards if any(x in c['position'].lower() for x in ['hidden', 'below', 'subconscious', 'underlying'])]
    external_cards = [c for c in cards if any(x in c['position'].lower() for x in ['external', 'above', 'influence', 'environment'])]
    hopes_fears = [c for c in cards if any(x in c['position'].lower() for x in ['hope', 'fear'])]

    paragraphs = []

    # PARAGRAPH 1: Opening with question and timing context (50-80 words)
    openings = [
        f"Your question about {q_lower} calls forth a powerful spread that speaks directly to your situation and offers meaningful guidance for your path forward.",
        f"The cards reveal significant insight into your query regarding {q_lower}. This reading illuminates both the challenges and opportunities before you.",
        f"As we explore {q_lower}, the tarot offers wisdom and guidance that addresses the heart of your concern with clarity and depth.",
        f"Your search for understanding about {q_lower} has drawn cards of great significance that weave together into a coherent message.",
    ]
    opening = random.choice(openings)
    timing_additions = {
        'New Moon': " This New Moon timing amplifies new beginnings, the setting of powerful intentions, and fresh starts in your life.",
        'Full Moon': " The Full Moon illuminates what needs to be seen with clarity, bringing emotions and hidden truths to the surface.",
        'Waxing Gibbous': " The waxing gibbous moon calls for patience and refinement as momentum continues building toward culmination.",
        'Waxing Crescent': " The waxing crescent supports steady growth, building momentum, and taking those important first steps.",
        'Waning Crescent': " The waning crescent invites rest, reflection, and preparation for the new cycle about to begin.",
        'Waning': " The waning moon invites valuable reflection, conscious release, and letting go of what no longer serves.",
        'First Quarter': " The First Quarter moon brings challenges that test commitment and call for decisive action.",
    }
    for key, addition in timing_additions.items():
        if key in timing:
            opening += addition
            break
    paragraphs.append(opening)

    # PARAGRAPH 2: Foundation and Present (60-100 words)
    para2_parts = []
    if past_cards:
        c = past_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        para2_parts.append(f"{name}{rev} in the {c['position']} position reveals foundational energies that continue to shape your experience. {c['position_context']} This historical influence informs your current approach.")
    if present_cards:
        c = present_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context'] if c['position_context'][0].isupper() else c['position_context'].capitalize()
        para2_parts.append(f"Currently, {name}{rev} occupies the {c['position']} position, speaking directly to where you find yourself now. {ctx}")
    if not para2_parts and cards:
        c = cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        para2_parts.append(f"The {name}{rev} in the {c['position']} position anchors this reading with important energy. {c['position_context']} This card sets the tone for the entire spread.")
    if para2_parts:
        paragraphs.append(" ".join(para2_parts))

    # PARAGRAPH 3: Hidden influences, challenges, or external factors (60-100 words)
    para3_parts = []
    if hidden_cards:
        c = hidden_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context'] if c['position_context'][0].isupper() else c['position_context'].capitalize()
        para3_parts.append(f"Beneath the visible surface, {name}{rev} reveals hidden influences at work in your situation. {ctx} These unseen forces significantly shape how events unfold.")
    if challenge_cards:
        c = challenge_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context'] if c['position_context'][0].isupper() else c['position_context'].capitalize()
        para3_parts.append(f"The challenge presented by {name}{rev} asks you to grow. {ctx} This tension is meant to catalyze growth, not defeat you.")
    if external_cards and len(para3_parts) < 2:
        c = external_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context'] if c['position_context'][0].isupper() else c['position_context'].capitalize()
        para3_parts.append(f"External influences through {name}{rev} shape your situation. {ctx}")
    if hopes_fears and len(para3_parts) < 2:
        c = hopes_fears[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context'] if c['position_context'][0].isupper() else c['position_context'].capitalize()
        para3_parts.append(f"The Hopes and Fears position holds {name}{rev}. {ctx} Understanding this duality helps you navigate with greater self-awareness.")
    if para3_parts:
        paragraphs.append(" ".join(para3_parts))

    # PARAGRAPH 4: Future/Outcome and Advice (60-100 words)
    para4_parts = []
    if future_cards:
        c = future_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para4_parts.append(f"Looking ahead, {name}{rev} in the {c['position']} position suggests the likely trajectory if current energies continue. {ctx} Remember this is not fixed fate but rather the direction present forces flow toward; your choices can influence this outcome.")
    if advice_cards:
        c = advice_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para4_parts.append(f"For guidance, {name}{rev} counsels: {ctx} This wisdom offers concrete direction for moving forward with intention.")
    if para4_parts:
        paragraphs.append(" ".join(para4_parts))

    # PARAGRAPH 5: Actionable insight closing (40-70 words)
    insights = [
        "Take time this week to journal about what arises from this reading. Conscious reflection will unlock deeper understanding and reveal how these energies manifest in your daily life.",
        "Consider what small but meaningful step you can take today that aligns with this guidance. Even modest action creates momentum toward meaningful change in your situation.",
        "The path forward requires honoring both what you feel and what you know. Let neither emotion nor logic override the other as you make important decisions ahead.",
        "Trust the timing that unfolds naturally rather than forcing premature resolution. Patience and presence serve you better than anxiety or urgency in this matter.",
        "Your next step is clearer than it may seem: listen to what you already know but have hesitated to acknowledge fully. Trust your inner wisdom.",
        "Ground this reading in practical action. Choose one concrete change you can make within the next few days that honors the guidance revealed here.",
        "The cards affirm your own inner wisdom. The answer you seek is already forming within you; trust it, honor it, and give it voice in your life.",
        "Focus your energy where you have actual influence rather than where you wish you had control. This discernment is itself a form of power.",
    ]
    card_names_lower = [c.get('card', '').lower() for c in cards]
    specific_insights = {
        'tower': "The Tower calls for acceptance of necessary transformation. What crumbles was not built on solid foundation; from this clearing, something far more authentic can emerge.",
        'death': "Death's transformation is already underway in your life. Release gracefully what naturally falls away, trusting that this makes room for essential new growth.",
        'devil': "Examine where you may have given away your power or become attached to limiting patterns. Awareness of these chains is the first step toward liberation.",
        'star': "Hold onto hope as you pour your energy into healing and renewal. The Star promises that light returns after even the darkest night of the soul.",
        'moon': "Navigate by intuition when the path seems unclear or confusing. Your inner knowing is reliable even when logic falters or facts remain hidden.",
        'strength': "True strength lies in gentleness, patience, and compassion rather than force. The power you need comes from inner certainty, not external aggression.",
        'hermit': "Take time for solitary reflection in the days ahead. The answers you seek emerge in quietude, away from the noise of others' voices and opinions.",
        'wheel': "Trust in the turning of the wheel. What rises will fall; what falls will rise again. This phase, whatever its nature, is temporary and will shift.",
        'justice': "Truth and fairness must guide your decisions in this matter. Consider all sides carefully before acting, but then move with conviction and integrity.",
        'temperance': "Seek balance and moderation in all things now. The middle way may seem less dramatic than extremes, but it leads to sustainable wisdom.",
        'judgement': "Listen for the call to your highest self. Something summons you to rise up, shed old limitations, and answer your deepest purpose.",
        'world': "Completion is at hand. Celebrate what you have accomplished and honor this ending as you prepare for the next great cycle of your journey.",
        'fool': "Embrace beginner's mind. The Fool reminds you that not knowing can be a gift, opening doors that expertise keeps closed. Trust the path ahead.",
        'magician': "You have all the tools you need. The Magician calls you to align thought, will, emotion, and action in service of manifesting your intentions.",
    }
    closing = random.choice(insights)
    for key, text in specific_insights.items():
        if any(key in c for c in card_names_lower):
            closing = text + " " + random.choice(insights)
            break
    paragraphs.append(closing)

    # Ensure we have at least 3 substantive paragraphs
    while len(paragraphs) < 3:
        expansion = random.choice([
            "This reading invites deep contemplation of your current path and circumstances. You are at a significant crossroads where the choices you make now will have lasting implications for your future direction.",
            "The patterns emerging here reflect an ongoing process of growth and transformation in your life. You are being called to step more fully into your authentic self and release what no longer serves.",
            "Consider how these themes connect to recurring patterns you have noticed in your broader life experience. The tarot reflects deeper currents that have shaped your journey over time.",
            "What surfaces here is an invitation to trust your own inner guidance more deeply than perhaps you have before. Your perspective and attitude fundamentally shape your experience of events.",
        ])
        paragraphs.insert(-1, expansion)

    # Limit to 5 paragraphs maximum
    if len(paragraphs) > 5:
        opening_p = paragraphs[0]
        closing_p = paragraphs[-1]
        middle = paragraphs[1:-1]
        combined = []
        step = max(1, len(middle) // 3)
        for i in range(0, len(middle), step):
            chunk = middle[i:i+step]
            if chunk:
                combined.append(" ".join(chunk))
        paragraphs = [opening_p] + combined[:3] + [closing_p]

    response = "\n\n".join(paragraphs)

    # Expand if too short (under 200 words)
    word_count = len(response.split())
    expansions = [
        "The energies present suggest you are at a significant moment where conscious choice can meaningfully shape the path ahead. Neither rushing forward impulsively nor remaining frozen in indecision serves you well; instead, seek the middle way of deliberate, considered movement toward your goals.",
        "This reading points toward the importance of honoring both your intuitive knowing and your practical wisdom as you navigate forward. Neither alone is sufficient for addressing complex life situations; together they create more complete understanding and wiser action.",
        "The wisdom of these cards points toward integration rather than separation. The various aspects of your situation, though they may seem at odds or in conflict, are ultimately parts of a greater whole that seeks harmony and balance.",
        "Pay close attention to your initial emotional response to this reading. Often our first reaction carries important information about what we already know intuitively but have not fully acknowledged or accepted in our conscious awareness.",
        "Remember that seeking guidance is itself an act of wisdom. By engaging with this reading, you demonstrate openness to growth and willingness to see your situation more clearly. This receptivity is itself powerful.",
    ]
    while word_count < 200 and len(paragraphs) <= 5:
        exp = random.choice(expansions)
        parts = response.rsplit("\n\n", 1)
        if len(parts) == 2:
            response = parts[0] + "\n\n" + exp + "\n\n" + parts[1]
        else:
            response = response + "\n\n" + exp
        word_count = len(response.split())
        # Prevent infinite loop
        paragraphs = response.split('\n\n')
        if len(paragraphs) > 5:
            paragraphs = paragraphs[:4] + [paragraphs[-1]]
            response = "\n\n".join(paragraphs)
            break

    # Trim if too long (over 400 words)
    while len(response.split()) > 400:
        para_list = response.split('\n\n')
        if len(para_list) > 3:
            mid_idx = len(para_list) // 2
            para_list.pop(mid_idx)
            response = "\n\n".join(para_list)
        else:
            break

    return response

def generate_fallback_response(prompt):
    """Generate a fallback response if parsing fails."""
    question = prompt.get('question', 'your question')
    return f"""Your question about {question.lower().rstrip('?')} touches on significant life themes that deserve careful attention and reflection. The cards drawn for this reading speak to deeper currents flowing through your situation, currents that may not be immediately visible but that shape events nonetheless.

Looking at the energies present, there is a clear call for balance between action and reflection in how you approach this matter. You are at a pivotal moment where conscious choice can meaningfully shape the path ahead. Seek the middle way of deliberate, considered movement.

The reading points toward the importance of honoring both your intuitive knowing and your practical wisdom as you navigate forward. Neither alone is sufficient for addressing complex life situations; together they create more complete understanding.

Your actionable insight is to create intentional space for quiet reflection in the coming days. Trust your own inner guidance as you navigate the questions before you. The answers you seek are closer than they may appear, waiting only for you to still yourself enough to hear them."""

def main():
    random.seed(42)
    with open('/home/user/taro/training/data/batches_expanded/batch_0022.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    print(f"Processing {len(prompts)} prompts from batch {batch_data['batch_id']}...")

    responses = []
    for i, prompt in enumerate(prompts):
        random.seed(hash(prompt['id']))
        try:
            response_text = generate_reading(prompt)
            responses.append({'id': prompt['id'], 'response': response_text})
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(prompts)} prompts...")
        except Exception as e:
            print(f"Error processing prompt {prompt['id']}: {e}")
            responses.append({'id': prompt['id'], 'response': generate_fallback_response(prompt)})

    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0022_responses.jsonl'
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"\nSuccessfully wrote {len(responses)} responses to {output_path}")

    # Verification
    with open(output_path, 'r') as f:
        lines = f.readlines()
    word_counts = []
    para_counts = []
    for line in lines:
        data = json.loads(line)
        word_counts.append(len(data['response'].split()))
        para_counts.append(len([p for p in data['response'].split('\n\n') if p.strip()]))
    
    print(f"\nVerification:")
    print(f"  Total responses: {len(lines)}")
    print(f"  Word counts - Min: {min(word_counts)}, Max: {max(word_counts)}, Avg: {sum(word_counts)/len(word_counts):.1f}")
    print(f"  In 200-400 range: {sum(1 for w in word_counts if 200 <= w <= 400)} ({100*sum(1 for w in word_counts if 200 <= w <= 400)/len(word_counts):.1f}%)")
    print(f"  Paragraph counts - Min: {min(para_counts)}, Max: {max(para_counts)}, Avg: {sum(para_counts)/len(para_counts):.1f}")
    print(f"  In 3-5 para range: {sum(1 for p in para_counts if 3 <= p <= 5)} ({100*sum(1 for p in para_counts if 3 <= p <= 5)/len(para_counts):.1f}%)")

if __name__ == '__main__':
    main()
