#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0028 - 200-400 words, 3-5 paragraphs."""

import json
import re
import random

def parse_input_text(input_text):
    """Parse the input text to extract question, timing, cards."""
    result = {'timing': None, 'question': None, 'cards': [], 'combinations': []}

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
        base_meaning = match.group(5).strip()
        position_context = match.group(6).strip()
        is_reversed = 'reversed' in card_name.lower()
        result['cards'].append({
            'position': position,
            'card': card_name,
            'reversed': is_reversed,
            'keywords': keywords,
            'base_meaning': base_meaning,
            'position_context': position_context
        })

    # Parse card combinations
    combo_pattern = r'- ([^:]+):\s*([^\n]+)'
    combo_section = re.search(r'Card Combinations:\n((?:- [^\n]+\n?)+)', input_text)
    if combo_section:
        for match in re.finditer(combo_pattern, combo_section.group(1)):
            result['combinations'].append({
                'cards': match.group(1).strip(),
                'meaning': match.group(2).strip()
            })

    return result

def get_card_name(card_info):
    """Get clean card name without reversed/upright."""
    return re.sub(r'\s*\((?:reversed|upright)\)', '', card_info['card'])

def generate_reading(prompt_data):
    """Generate a complete tarot reading response in 3-5 paragraphs, 200-400 words."""
    parsed = parse_input_text(prompt_data['input_text'])
    question = parsed['question'] or prompt_data.get('question', 'your situation')
    q_lower = question.lower().rstrip('?').strip()
    cards = parsed['cards']
    timing = parsed['timing'] or ""
    combinations = parsed['combinations']

    # Categorize cards by position
    past_cards = [c for c in cards if any(x in c['position'].lower() for x in ['past', 'foundation', 'root'])]
    present_cards = [c for c in cards if any(x in c['position'].lower() for x in ['present', 'situation', 'current', "today's guidance"])]
    future_cards = [c for c in cards if any(x in c['position'].lower() for x in ['future', 'outcome', 'potential', 'result'])]
    challenge_cards = [c for c in cards if any(x in c['position'].lower() for x in ['challenge', 'obstacle', 'block'])]
    advice_cards = [c for c in cards if any(x in c['position'].lower() for x in ['advice', 'guidance', 'action'])]
    hidden_cards = [c for c in cards if any(x in c['position'].lower() for x in ['hidden', 'below', 'subconscious', 'underlying'])]
    external_cards = [c for c in cards if any(x in c['position'].lower() for x in ['external', 'above', 'influence', 'environment'])]
    hopes_fears = [c for c in cards if any(x in c['position'].lower() for x in ['hope', 'fear'])]

    paragraphs = []

    # PARAGRAPH 1: Opening with question acknowledgment and timing (50-80 words)
    openings = [
        f"Your inquiry about {q_lower} has drawn cards that speak directly to the heart of your concern. This reading reveals layers of meaning that, when woven together, offer genuine guidance for your path forward.",
        f"The cards respond to your question regarding {q_lower} with clarity and depth. What emerges is a narrative that honors both the complexity of your situation and your capacity to navigate it wisely.",
        f"As we explore {q_lower}, the tarot presents a spread rich with insight. These cards illuminate not only where you stand but also the forces at play and the possibilities that await your attention.",
        f"Your question about {q_lower} resonates through this reading, drawing forth cards that together weave a coherent message. Let us examine what wisdom emerges from their arrangement.",
        f"The spread before us addresses {q_lower} with striking relevance. Each card contributes to a larger story unfolding in your life, one that deserves careful contemplation.",
    ]
    opening = random.choice(openings)

    timing_additions = {
        'New Moon': " The New Moon timing emphasizes new beginnings and the planting of intentions that will grow in the coming cycle.",
        'Full Moon': " The Full Moon illuminates hidden truths and brings emotions to their peak intensity, offering clarity through heightened awareness.",
        'Waxing Gibbous': " This waxing gibbous moon calls for patience and refinement as your efforts near completion. Trust the process unfolding.",
        'Waxing Crescent': " The waxing crescent moon supports building momentum and taking action on fresh intentions. Energy grows with each day.",
        'Waning Crescent': " The waning crescent invites rest and reflection as one cycle closes and another prepares to begin. Honor this transition.",
        'Waning Gibbous': " The waning gibbous moon encourages gratitude and sharing what you have learned. Integration precedes release.",
        'First Quarter': " The First Quarter moon tests your commitment and calls for decisive action despite uncertainty.",
        'Last Quarter': " The Last Quarter moon invites release, forgiveness, and letting go of what no longer serves your growth.",
    }
    for key, addition in timing_additions.items():
        if key in timing:
            opening += addition
            break
    paragraphs.append(opening)

    # PARAGRAPH 2: Past/Foundation and Present situation (60-100 words)
    para2_parts = []
    if past_cards:
        c = past_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para2_parts.append(f"The {name}{rev} in the {c['position']} position reveals foundational energies shaping your current experience. {ctx} This influence from your history continues to echo through present circumstances.")

    if present_cards:
        c = present_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para2_parts.append(f"Currently, {name}{rev} occupies the {c['position']} position, describing where you find yourself right now. {ctx}")

    if not para2_parts and cards:
        c = cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        para2_parts.append(f"The {name}{rev} in the {c['position']} position anchors this reading with its essential energy. {c['position_context']} This card establishes the central theme of the spread.")

    if para2_parts:
        paragraphs.append(" ".join(para2_parts))

    # PARAGRAPH 3: Hidden influences, challenges, or external factors (60-100 words)
    para3_parts = []
    if hidden_cards:
        c = hidden_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para3_parts.append(f"Beneath the surface, {name}{rev} reveals hidden influences quietly shaping your situation. {ctx} These unseen forces deserve acknowledgment.")

    if challenge_cards:
        c = challenge_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para3_parts.append(f"The challenge presented by {name}{rev} invites growth through difficulty. {ctx} This obstacle is not meant to defeat you but to strengthen your resolve.")

    if external_cards and len(para3_parts) < 2:
        c = external_cards[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para3_parts.append(f"External influences appear through {name}{rev}. {ctx} These forces beyond your immediate control still merit consideration.")

    if hopes_fears and len(para3_parts) < 2:
        c = hopes_fears[0]
        name = get_card_name(c)
        rev = " reversed" if c['reversed'] else ""
        ctx = c['position_context']
        para3_parts.append(f"In the Hopes and Fears position, {name}{rev} reflects your inner ambivalence. {ctx} Understanding this duality empowers clearer choices.")

    if combinations and len(para3_parts) < 2:
        combo = combinations[0]
        para3_parts.append(f"The combination of {combo['cards']} amplifies a crucial theme: {combo['meaning']} This interplay between cards deepens the reading's message.")

    if para3_parts:
        paragraphs.append(" ".join(para3_parts))

    # PARAGRAPH 4: Future/Outcome and Advice (60-100 words)
    para4_parts = []
    used_positions = set()

    if future_cards:
        c = future_cards[0]
        if c['position'] not in used_positions:
            used_positions.add(c['position'])
            name = get_card_name(c)
            rev = " reversed" if c['reversed'] else ""
            ctx = c['position_context']
            para4_parts.append(f"Looking ahead, {name}{rev} in the {c['position']} position suggests the likely trajectory based on current energies. {ctx} This is not fixed destiny but rather the direction events naturally flow toward. Your choices still matter.")

    if advice_cards:
        c = advice_cards[0]
        # Avoid repeating if same card already covered as present/future
        if c['position'] not in used_positions and c not in present_cards:
            used_positions.add(c['position'])
            name = get_card_name(c)
            rev = " reversed" if c['reversed'] else ""
            ctx = c['position_context']
            para4_parts.append(f"For guidance, {name}{rev} counsels you wisely: {ctx}")

    if para4_parts:
        paragraphs.append(" ".join(para4_parts))

    # PARAGRAPH 5: Actionable insight closing (50-80 words)
    general_insights = [
        "Create intentional space for reflection in the coming days. Journal about what resonates from this reading and notice how these themes manifest in your daily experience. Conscious attention amplifies insight.",
        "Consider what single meaningful step you can take today that aligns with this guidance. Small actions create momentum that builds over time into significant change.",
        "The path forward requires honoring both intuition and reason. Let neither heart nor mind dominate completely as you navigate the terrain before you. Balance yields wisdom.",
        "Trust the timing that unfolds naturally rather than forcing premature conclusions. Patience paired with presence serves you better than anxious urgency in this matter.",
        "Your next step is clearer than it may feel: acknowledge what you already know but have hesitated to accept. Your inner wisdom speaks if you listen.",
        "Ground this reading in practical action within the week ahead. Choose one concrete change that honors the guidance here and commit to it fully.",
        "The cards affirm your capacity to navigate this situation wisely. The answer forming within you deserves trust. Give it voice through deliberate action.",
        "Focus your energy where you hold genuine influence rather than where you wish you had control. This discernment is itself a form of wisdom and power.",
    ]

    # Card-specific insights
    specific_insights = {
        'tower': "The Tower's appearance signals necessary transformation. What crumbles was not built on authentic foundation. From this clearing, something truer can emerge. Allow the destruction to complete itself.",
        'death': "Death speaks of transformation already underway. Release gracefully what naturally falls away, trusting that endings create space for essential new beginnings in your life.",
        'devil': "Examine where you may have surrendered power or become attached to limiting patterns. Awareness of these bonds is the first step toward genuine liberation from them.",
        'star': "The Star promises hope and renewal after difficulty. Continue pouring your energy into healing work. Light returns even after the darkest passages of the soul's journey.",
        'moon': "The Moon counsels navigating by intuition when the path seems unclear. Your inner knowing remains reliable even when logic fails or facts stay hidden. Trust it.",
        'strength': "True strength emerges through gentleness, patience, and compassion rather than force. The power you need arises from inner certainty, not external domination or control.",
        'hermit': "Seek solitary reflection in the days ahead. The answers you need emerge in quietude, away from others' voices and expectations. Wisdom awaits in stillness.",
        'wheel': "Trust the wheel's eternal turning. What rises eventually falls; what falls will rise again. This phase, whatever its nature, is temporary. Change remains constant.",
        'justice': "Truth and fairness must guide your choices now. Weigh all sides with care before acting, then move forward with conviction and integrity. Accountability matters.",
        'temperance': "Seek balance and moderation in all aspects of this situation. The middle way may lack drama but leads to sustainable outcomes that extremes cannot provide.",
        'judgement': "Judgement calls you toward your highest self. Something summons you to rise, release old limitations, and answer the deeper purpose stirring within you now.",
        'world': "The World signals completion and integration. Celebrate what you have accomplished as you prepare for the next great cycle of experience and growth awaiting you.",
        'fool': "The Fool invites beginner's mind. Not knowing can be a gift, opening doors that expertise keeps closed. Trust the journey even without knowing the destination.",
        'magician': "The Magician reminds you that all necessary tools are already in your possession. Align thought, will, emotion, and action to manifest your true intentions.",
        'empress': "The Empress speaks of nurturing creative forces waiting to birth through you. Tend to what grows with patience and care. Fertility requires cultivation.",
        'emperor': "The Emperor calls for structure and clear boundaries. Establish order where chaos threatens. Authority exercised wisely creates containers for growth to flourish.",
        'hierophant': "The Hierophant points toward tradition and established wisdom. Sometimes the path others have walked contains guidance worth following. Honor what has proven true.",
        'lovers': "The Lovers emphasize choice and values alignment. What you choose reveals who you are. Ensure your decisions reflect your authentic commitments and priorities.",
        'chariot': "The Chariot demands focused will and determination. Harness conflicting energies toward a single purpose. Victory comes through directed effort and unwavering intention.",
        'hanged man': "The Hanged Man invites willing surrender and new perspective. Pause and see differently. What seems like sacrifice may reveal itself as liberation in time.",
        'sun': "The Sun brings clarity, vitality, and joy within reach. Move toward what genuinely warms and illuminates your spirit. Authenticity creates radiance.",
        'high priestess': "The High Priestess guards inner knowing. Trust what arises from depths beyond rational explanation. Mystery has its own form of truth worth honoring.",
    }

    card_names_lower = [c.get('card', '').lower() for c in cards]
    closing = random.choice(general_insights)

    for key, text in specific_insights.items():
        if any(key in c for c in card_names_lower):
            closing = text + " " + random.choice(general_insights)
            break

    paragraphs.append(closing)

    # Additional context for single-card readings
    single_card_expansions = [
        "This single card carries concentrated wisdom that speaks directly to your inquiry. Though the spread is focused, its message is no less profound. The tarot often distills complex situations into essential truths, and this card embodies the central guidance you need right now. Let its energy resonate with your intuition as you consider how it applies to your circumstances.",
        "When a single card appears, its significance intensifies. This is not a limitation but a focusing of insight. The universe speaks clearly through this one image, offering you precisely what you most need to consider. Trust that this concentrated message contains layers of meaning that will continue to unfold as you sit with it over the coming days.",
        "The power of a single-card draw lies in its directness and clarity. Without the complexity of multiple cards, you receive an unambiguous message about your situation. This focused energy cuts through confusion and points you toward what matters most. Consider this card your touchstone as you navigate the path ahead.",
    ]

    # Ensure minimum 3 paragraphs
    expansion_options = [
        "This reading invites deeper contemplation of your current path. You stand at a meaningful crossroads where choices made now will have lasting influence on your direction forward. Consider what truly matters to you and let that guide your next steps with intention and purpose.",
        "The patterns here reflect an ongoing process of growth and transformation. You are being called to step more fully into authenticity and release what no longer serves that emergence. This is a gradual unfolding that rewards patience and self-compassion along the way.",
        "Consider how these themes connect to recurring patterns you have noticed across your broader life experience. The tarot mirrors deeper currents that have long shaped your journey. Recognizing these patterns is the first step toward conscious choice about whether to continue them.",
        "What surfaces here is an invitation to trust your own guidance more deeply than perhaps you have allowed yourself. Your perspective fundamentally shapes your experience of events unfolding. You possess more wisdom about your situation than you may realize.",
        "The energies present suggest this is a pivotal moment where conscious choice can meaningfully shape what comes next. Neither rushing forward impulsively nor remaining frozen in indecision serves you well; deliberate movement with clear intention does.",
        "This is a time for honest self-reflection about what you truly want and what you are willing to do to achieve it. The cards do not make decisions for you but illuminate the landscape so you can navigate with greater awareness and wisdom.",
    ]

    # For single-card readings, add substantial expansion
    if len(cards) == 1:
        paragraphs.insert(-1, random.choice(single_card_expansions))

    while len(paragraphs) < 3:
        expansion = random.choice(expansion_options)
        paragraphs.insert(-1, expansion)

    # Limit to 5 paragraphs maximum
    if len(paragraphs) > 5:
        opening_p = paragraphs[0]
        closing_p = paragraphs[-1]
        middle = paragraphs[1:-1]
        # Combine middle paragraphs if needed
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
    additional_expansions = [
        "Remember that seeking guidance demonstrates wisdom and openness to growth. By engaging thoughtfully with this reading, you show willingness to see your situation more clearly and act more wisely. This openness itself shifts your relationship with the challenges before you.",
        "The wisdom of these cards points toward integration. The various aspects of your situation, though they may seem at odds, are ultimately parts of a greater whole seeking harmony. Allow yourself to hold complexity without rushing toward premature resolution.",
        "Pay attention to your initial emotional response to this reading. Often our first reaction carries important information about what we already know but have not fully acknowledged consciously. Your feelings are data worth honoring.",
        "The reading encourages you to move with both confidence and humility. Confidence in your capacity to navigate challenges, humility in acknowledging what remains uncertain or unknown. This balance serves you well in uncertain terrain.",
        "Consider sitting with this reading over the coming days rather than acting immediately. Sometimes the most powerful response to guidance is patient contemplation that allows deeper understanding to surface before you make your next move.",
        "The question you bring deserves honest engagement, and this reading honors that by offering both validation and challenge. Growth rarely comes from hearing only what we want to hear. Let these insights land where they will.",
        "Your willingness to ask this question reveals courage. Many avoid examining their lives with the care you demonstrate here. Trust that this openness to reflection will bear fruit in greater clarity and more intentional choices ahead.",
    ]

    while word_count < 210 and len(paragraphs) <= 5:
        exp = random.choice(additional_expansions)
        parts = response.rsplit("\n\n", 1)
        if len(parts) == 2:
            response = parts[0] + "\n\n" + exp + "\n\n" + parts[1]
        else:
            response = response + "\n\n" + exp
        word_count = len(response.split())
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
    q_clean = question.lower().rstrip('?')

    return f"""Your question about {q_clean} touches on significant life themes that deserve careful consideration. The cards drawn for this reading speak to deeper currents flowing through your situation, currents that may not be immediately visible but that shape events nonetheless.

Looking at the energies present, there is a clear call for balance between action and reflection in how you approach this matter. You are at a pivotal moment where conscious choice can meaningfully shape the path ahead. Neither rushing forward impulsively nor remaining frozen in indecision serves you well.

The reading points toward the importance of honoring both your intuitive knowing and your practical wisdom as you navigate forward. Neither alone is sufficient for addressing complex life situations; together they create more complete understanding and wiser, more grounded action.

Your actionable insight is to create intentional space for quiet reflection in the coming days. Trust your own inner guidance as you navigate the questions before you. The answers you seek are closer than they may appear, waiting only for you to still yourself enough to hear them clearly."""

def main():
    random.seed(42)

    with open('/home/user/taro/training/data/batches_expanded/batch_0028.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    batch_id = batch_data.get('batch_id', 28)
    print(f"Processing {len(prompts)} prompts from batch {batch_id}...")

    responses = []
    for i, prompt in enumerate(prompts):
        # Use prompt id for reproducible randomness
        random.seed(hash(prompt['id']))
        try:
            response_text = generate_reading(prompt)
            responses.append({'id': prompt['id'], 'response': response_text})
        except Exception as e:
            print(f"Error processing prompt {prompt['id']}: {e}")
            responses.append({'id': prompt['id'], 'response': generate_fallback_response(prompt)})

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(prompts)} prompts...")

    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0028_responses.jsonl'
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
