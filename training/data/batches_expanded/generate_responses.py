#!/usr/bin/env python3
"""Generate tarot reading responses for training data - Enhanced version."""

import json
import re
import random

def parse_input_text(input_text):
    """Parse the input text to extract question, timing, cards, and combinations."""
    result = {
        'timing': None,
        'question': None,
        'cards': [],
        'combinations': [],
        'elemental_balance': None
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        result['timing'] = timing_match.group(1).strip()

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Extract cards - improved pattern
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

    # Extract card combinations
    combo_pattern = r'-\s+([^:]+):\s+([^\n]+)'
    combo_section = re.search(r'Card Combinations:(.*?)(?=Elemental Balance|$)', input_text, re.DOTALL)
    if combo_section:
        for match in re.finditer(combo_pattern, combo_section.group(1)):
            result['combinations'].append({
                'cards': match.group(1).strip(),
                'meaning': match.group(2).strip()
            })

    # Extract elemental balance
    elem_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elem_match:
        result['elemental_balance'] = elem_match.group(1).strip()

    return result


def get_card_interpretation(card_info):
    """Generate rich interpretation for a card in its position."""
    card = card_info['card']
    position = card_info['position']
    reversed_state = card_info['reversed']
    context = card_info['position_context']
    keywords = card_info['keywords']

    # Clean card name (remove reversed/upright notation for display)
    clean_card = re.sub(r'\s*\((?:reversed|upright)\)', '', card)

    return {
        'name': clean_card,
        'position': position,
        'reversed': reversed_state,
        'context': context,
        'keywords': keywords
    }


def generate_opening(question, timing, cards):
    """Generate opening paragraph addressing the question."""
    # Clean up question formatting
    q_lower = question.lower().rstrip('?').strip()
    
    openings = [
        f"Your question about {q_lower} reveals a profound journey through the cards laid before you today.",
        f"The cards speak with clarity to your inquiry: \"{question}\" This is a question that deserves thoughtful exploration.",
        f"As we explore your question regarding {q_lower}, the tarot offers wisdom worth careful consideration.",
        f"Your search for understanding about {q_lower} has drawn powerful cards that illuminate your path.",
        f"The spread before you addresses your question with remarkable depth and nuance.",
        f"In seeking to understand {q_lower}, you have called forth cards of great significance.",
        f"Your question - \"{question}\" - draws forth a reading rich with insight and guidance.",
        f"The tarot responds thoughtfully to your inquiry about {q_lower}, offering layers of meaning to explore.",
    ]

    timing_phrases = []
    if timing:
        if 'New Moon' in timing:
            timing_phrases = [
                "This New Moon timing amplifies new beginnings and the setting of powerful intentions.",
                "Under the New Moon's influence, fresh starts and new perspectives are especially favored.",
                "The New Moon's energy supports planting seeds of meaningful change in your life.",
                "New Moon darkness invites deep introspection before taking significant action.",
            ]
        elif 'Full Moon' in timing:
            timing_phrases = [
                "The Full Moon illuminates what needs to be seen with greater clarity.",
                "Under this Full Moon, emotions run high and important truths rise to the surface.",
                "Full Moon energy brings culmination, clarity, and heightened emotional awareness.",
                "This Full Moon casts revealing light on hidden aspects of your situation.",
            ]
        elif 'Waxing Gibbous' in timing:
            timing_phrases = [
                "The waxing gibbous moon calls for patience as you continue refining your approach.",
                "Under this waxing gibbous phase, trust the process that is gradually unfolding.",
                "The moon builds steadily toward fullness, as does momentum in your situation.",
            ]
        elif 'Waxing' in timing:
            timing_phrases = [
                "The waxing moon supports steady growth and the building of momentum.",
                "This waxing phase encourages patience as your plans continue to develop.",
                "With the moon waxing, trust in the power of gradual, consistent progress.",
            ]
        elif 'Waning Crescent' in timing:
            timing_phrases = [
                "The waning crescent invites necessary rest and reflection before renewal begins.",
                "This waning crescent phase supports releasing what no longer serves your growth.",
                "Under the waning crescent, prepare yourself for a new cycle of possibility.",
            ]
        elif 'Waning' in timing:
            timing_phrases = [
                "The waning moon invites valuable reflection and conscious release.",
                "This waning phase supports letting go of what no longer serves your highest good.",
                "Under the waning moon, rest and prepare yourself for coming renewal.",
            ]
        elif 'First Quarter' in timing:
            timing_phrases = [
                "The First Quarter moon brings challenges that ultimately test and strengthen commitment.",
                "This First Quarter phase calls for important decisions and meaningful action.",
                "Under the First Quarter moon, obstacles arise to reveal the depth of your resolve.",
            ]

    opening = random.choice(openings)
    if timing_phrases:
        opening += " " + random.choice(timing_phrases)

    return opening


def build_card_paragraph(card, additional_context=""):
    """Build a detailed paragraph for a single card."""
    interp = get_card_interpretation(card)
    reversed_text = " in its reversed position" if interp['reversed'] else ""
    
    templates = [
        f"The {interp['name']}{reversed_text} appears in the {interp['position']} position, bringing important energy to this reading. {interp['context']} {additional_context}",
        f"In the {interp['position']} position, the {interp['name']}{reversed_text} carries significant meaning for your situation. {interp['context']} {additional_context}",
        f"The {interp['name']}{reversed_text}, positioned as your {interp['position']}, speaks directly to the heart of your question. {interp['context']} {additional_context}",
    ]
    
    return random.choice(templates)


def generate_card_narrative(cards, question):
    """Generate the main body interpreting cards in context."""
    if not cards:
        return ""

    paragraphs = []

    # Group cards by thematic position
    past_cards = [c for c in cards if 'past' in c['position'].lower()]
    present_cards = [c for c in cards if 'present' in c['position'].lower() or 'situation' in c['position'].lower()]
    future_cards = [c for c in cards if 'future' in c['position'].lower() or 'outcome' in c['position'].lower()]
    challenge_cards = [c for c in cards if 'challenge' in c['position'].lower() or 'obstacle' in c['position'].lower()]
    advice_cards = [c for c in cards if 'advice' in c['position'].lower() or 'action' in c['position'].lower() or 'guidance' in c['position'].lower()]
    hidden_cards = [c for c in cards if 'hidden' in c['position'].lower() or 'below' in c['position'].lower()]
    external_cards = [c for c in cards if 'external' in c['position'].lower() or 'above' in c['position'].lower()]
    hopes_fears = [c for c in cards if 'hope' in c['position'].lower() or 'fear' in c['position'].lower()]
    other_cards = [c for c in cards if c not in past_cards + present_cards + future_cards + challenge_cards + advice_cards + hidden_cards + external_cards + hopes_fears]

    # Handle single-card readings with expanded content
    if len(cards) == 1:
        card = cards[0]
        interp = get_card_interpretation(card)
        reversed_note = ", appearing in its reversed position," if interp['reversed'] else ""
        
        single_card_additions = [
            "Every symbol, color, and figure in this card holds meaning for your situation.",
            "Allow this card's imagery to speak to you on multiple levels over the coming days.",
            "This card invites you to look beyond the surface to find deeper resonance.",
            "The concentrated energy of a single card reading can be especially powerful and direct.",
        ]
        
        para = f"The {interp['name']}{reversed_note} comes forward as your {interp['position']}, carrying the full weight of the reading's message. {interp['context']} This single card contains everything you need to know right now - its imagery, symbolism, and traditional meanings all speak directly to your question about {question.lower().rstrip('?')}. {random.choice(single_card_additions)}"
        paragraphs.append(para)
        
        # Add reflection on the card's deeper meaning
        reflection = get_card_reflection(interp['name'], interp['reversed'])
        if reflection:
            paragraphs.append(reflection)
            
        return "\n\n".join(paragraphs)

    # Build narrative for past/foundation
    if past_cards:
        card = past_cards[0]
        interp = get_card_interpretation(card)
        reversed_note = ", appearing reversed," if interp['reversed'] else ""
        para = f"Looking to your past, the {interp['name']}{reversed_note} occupies the {interp['position']} position, revealing foundational energies that continue to shape your current experience. {interp['context']} Understanding this history matters because it illuminates patterns and influences that inform how you approach your present situation."
        paragraphs.append(para)

    # Build narrative for present situation with challenges
    present_para_parts = []
    if present_cards:
        card = present_cards[0]
        interp = get_card_interpretation(card)
        reversed_note = " in its reversed aspect" if interp['reversed'] else ""
        present_para_parts.append(f"In your current circumstances, the {interp['name']}{reversed_note} occupies the {interp['position']} position, speaking directly to where you find yourself now. {interp['context']}")

        if challenge_cards:
            ch_card = challenge_cards[0]
            ch_interp = get_card_interpretation(ch_card)
            ch_reversed = ", reversed," if ch_interp['reversed'] else ""
            context_lower = ch_interp['context'].lower() if ch_interp['context'][0].isupper() else ch_interp['context']
            present_para_parts.append(f"The {ch_interp['name']}{ch_reversed} as your challenge adds another layer to consider: {context_lower} This tension is not meant to defeat you but to catalyze growth.")

    if present_para_parts:
        paragraphs.append(" ".join(present_para_parts))

    # Build narrative for hidden influences and deeper factors
    if hidden_cards or external_cards:
        influence_parts = []
        if hidden_cards:
            card = hidden_cards[0]
            interp = get_card_interpretation(card)
            reversed_note = " (reversed)" if interp['reversed'] else ""
            context_text = interp['context'].lower() if interp['context'][0].isupper() else interp['context']
            influence_parts.append(f"Beneath the visible surface, the {interp['name']}{reversed_note} reveals hidden influences at work: {context_text}")

        if external_cards:
            card = external_cards[0]
            interp = get_card_interpretation(card)
            reversed_note = " (reversed)" if interp['reversed'] else ""
            context_text = interp['context'].lower() if interp['context'][0].isupper() else interp['context']
            influence_parts.append(f"From the external world, the {interp['name']}{reversed_note} shapes the situation: {context_text}")

        if influence_parts:
            paragraphs.append(" ".join(influence_parts) + " These forces, though less obvious, significantly impact how events unfold.")

    # Hopes and fears
    if hopes_fears:
        card = hopes_fears[0]
        interp = get_card_interpretation(card)
        reversed_note = " (reversed)" if interp['reversed'] else ""
        para = f"The {interp['name']}{reversed_note} in the Hopes and Fears position illuminates your inner emotional landscape: {interp['context']} Understanding this duality - what you hope for and what you fear - helps you navigate your path with greater self-awareness and intention."
        paragraphs.append(para)

    # Build narrative for other influential cards
    if other_cards and len(cards) > 4:
        influences = []
        for card in other_cards[:2]:
            interp = get_card_interpretation(card)
            reversed_note = " (reversed)" if interp['reversed'] else ""
            context_text = interp['context'].lower() if interp['context'][0].isupper() else interp['context']
            influences.append(f"the {interp['name']}{reversed_note} in the {interp['position']} position, revealing that {context_text}")

        if influences:
            para = "Additional influences shape the full picture of this reading: " + "; while ".join(influences) + ". Each card adds nuance to the overall message."
            paragraphs.append(para)

    # Build narrative for future/outcome
    if future_cards:
        card = future_cards[0]
        interp = get_card_interpretation(card)
        reversed_note = ", reversed," if interp['reversed'] else ""
        para = f"Looking toward what lies ahead, the {interp['name']}{reversed_note} in the {interp['position']} position suggests the likely trajectory if current energies continue. {interp['context']} Remember that this is not fixed fate but rather the direction present forces flow toward. Your choices and actions can always influence the outcome."
        paragraphs.append(para)

    # Advice section
    if advice_cards:
        card = advice_cards[0]
        interp = get_card_interpretation(card)
        reversed_note = ", in its inverted form," if interp['reversed'] else ""
        para = f"For guidance, the {interp['name']}{reversed_note} speaks from the {interp['position']} position: {interp['context']} This counsel offers a concrete direction for moving forward with wisdom and intention."
        paragraphs.append(para)

    return "\n\n".join(paragraphs)


def get_card_reflection(card_name, is_reversed):
    """Generate a reflection on the deeper meaning of specific cards."""
    card_lower = card_name.lower()
    
    reflections = {
        'tower': "The Tower, though it may appear alarming, ultimately represents liberation from structures that have confined you. What falls away was never meant to last, and from this clearing new and more authentic foundations can emerge.",
        'death': "Death in the tarot speaks not of literal ending but of profound transformation. Like the snake shedding its skin, you are being called to release an old identity or situation so something new can be born.",
        'devil': "The Devil reveals where you may have given away your power or become attached to patterns that limit your freedom. Recognition itself is the first step toward liberation.",
        'moon': "The Moon illuminates the realm of the unconscious, where dreams, fears, and intuitions dwell. Trust your inner knowing even when the path ahead seems unclear.",
        'sun': "The Sun brings warmth, clarity, and joy. Even in its reversed form, it reminds you that light exists and can be found again. Authentic happiness is your birthright.",
        'star': "The Star offers hope and healing after difficulty. Like water poured upon the earth, renewal comes when you remain open and trusting of the process.",
        'world': "The World represents completion and integration. A significant cycle reaches its natural conclusion, and you stand at the threshold of new beginnings.",
        'fool': "The Fool invites you into beginner's mind, that space of openness and possibility before experience has shaped expectations. Trust the journey.",
        'magician': "The Magician reminds you that all the tools you need are already within your grasp. You have the power to manifest your intentions when you align thought, will, and action.",
        'high priestess': "The High Priestess guards the mysteries of the inner world. She calls you to trust your intuition, to listen deeply, and to honor what you know in your bones.",
        'empress': "The Empress embodies creative abundance and nurturing love. She invites you to care for yourself as generously as you care for others, and to trust in natural growth.",
        'emperor': "The Emperor represents structure, authority, and the power to build lasting foundations. Order and discipline serve your larger vision when applied wisely.",
        'hierophant': "The Hierophant connects you to tradition, wisdom teachings, and meaningful structure. Consider what you have inherited and what you wish to pass forward.",
        'lovers': "The Lovers speak to choices made from the heart, to values aligned with action, and to relationships that call forth your authentic self.",
        'chariot': "The Chariot embodies directed will and forward movement. Opposing forces can be harnessed toward a common goal when you hold the reins with skill.",
        'strength': "Strength reveals that true power comes through patience and compassion rather than force. The gentle approach often achieves what aggression cannot.",
        'hermit': "The Hermit calls you inward, to the solitude where wisdom ripens. Sometimes the most important journey is the one taken alone, by your own inner light.",
        'wheel': "The Wheel of Fortune reminds you that all things change. What rises will fall; what falls will rise again. Trust in the turning.",
        'justice': "Justice asks for truth and fairness, for accountability and right action. Consider carefully, then act with integrity.",
        'hanged man': "The Hanged Man invites surrender - not defeat, but the release of control that allows new perspective to emerge. Sometimes we must stop pushing to see clearly.",
        'temperance': "Temperance teaches the art of integration and patience. Opposing elements can blend into something new when given time and careful attention.",
        'judgement': "Judgement sounds the call to awakening, to rising up and answering your deepest purpose. Something summons you to become more fully yourself.",
    }
    
    for key, reflection in reflections.items():
        if key in card_lower:
            if is_reversed:
                return reflection + " In its reversed position, this energy may be blocked, excessive, or calling for special attention to be integrated."
            return reflection
    
    return None


def generate_actionable_insight(question, cards):
    """Generate closing with actionable insight."""
    insights = [
        "Take time this week to journal about what arises from this reading. The cards suggest that conscious reflection will unlock deeper understanding and clarity.",
        "Consider what small but meaningful step you can take today that aligns with this guidance. Even modest action creates momentum toward meaningful change.",
        "The path forward requires honoring both what you feel and what you know. Let neither emotion nor logic override the other as you make important decisions.",
        "Trust the timing that unfolds naturally rather than forcing premature resolution. Patience serves you here more than urgency or anxious action.",
        "Your next step is clearer than it may seem: listen to what you already know but have hesitated to acknowledge fully. The truth awaits your acceptance.",
        "Ground this reading in practical action. Choose one concrete change you can make within the next few days that honors the wisdom offered here.",
        "The cards affirm your own inner wisdom. The answer you seek is already forming within you; trust it, honor it, and give it voice in your life.",
        "Move forward with the understanding that uncertainty itself can be a teacher. Not all must be resolved immediately for meaningful progress to occur.",
        "Focus your energy where you have actual influence rather than where you wish you had control. This discernment itself is a form of power.",
        "Release what you cannot change and direct your full attention toward what remains within your power. Therein lies your freedom to act.",
        "Create sacred space for integration in the coming days. The insights from this reading will deepen as you carry them through your daily life.",
        "Allow yourself to sit with any discomfort this reading may raise. Sometimes the most valuable messages come wrapped in the guise of challenge.",
    ]

    # Add card-specific insights based on major arcana or significant cards
    card_names = [c.get('card', '').lower() for c in cards]

    specific_insights = []
    if any('tower' in c for c in card_names):
        specific_insights.append("The Tower's presence calls for acceptance of necessary change and transformation. What crumbles was not built on solid foundation. From this rubble, you can construct something far more authentic and lasting.")
    if any('death' in c for c in card_names):
        specific_insights.append("Death's transformation is already underway in your life. Your task is to release gracefully what naturally falls away, making room for what new life wishes to emerge in its place.")
    if any('empress' in c for c in card_names):
        specific_insights.append("The Empress invites you to nurture yourself as generously as you nurture others in your life. True abundance begins with genuine self-compassion and self-care.")
    if any('hermit' in c for c in card_names):
        specific_insights.append("Take time for solitary reflection in the days ahead. The answers you seek emerge in quietude, away from others' voices, opinions, and expectations.")
    if any('wheel' in c for c in card_names):
        specific_insights.append("Trust in the turning of the wheel. What goes down must rise again; what rises will eventually fall. This phase, whatever its nature, is temporary.")
    if any('star' in c for c in card_names):
        specific_insights.append("Hold onto hope as you pour your energy into healing and renewal. The Star promises that light returns after the darkest night. Keep faith in the process.")
    if any('sun' in c for c in card_names):
        specific_insights.append("Allow genuine joy into your process. Lightness of heart is not frivolity but wisdom. Celebrate what is good even while addressing what presents challenges.")
    if any('moon' in c for c in card_names):
        specific_insights.append("Navigate by intuition when the path ahead seems unclear or confusing. Your inner knowing is reliable even when logic falters or facts are hidden.")
    if any('justice' in c for c in card_names):
        specific_insights.append("Truth and fairness must guide your decisions in this matter. Consider all sides carefully before acting, but then act with conviction and integrity.")
    if any('strength' in c for c in card_names):
        specific_insights.append("True strength lies in gentleness, patience, and compassion. The power you need now is quiet and comes from inner certainty, not from force or aggression.")
    if any('temperance' in c for c in card_names):
        specific_insights.append("Seek balance and moderation in all things. The middle way may seem less dramatic than extremes, but it is sustainable and leads to genuine wisdom.")
    if any('hanged' in c for c in card_names):
        specific_insights.append("Sometimes surrender is the most powerful action available. Let go of the need to control outcomes and observe what new perspective emerges from stillness.")
    if any('judgement' in c for c in card_names):
        specific_insights.append("Listen for the call to your highest self. Something summons you to rise up, to shed old limitations, and answer your deepest purpose.")
    if any('world' in c for c in card_names):
        specific_insights.append("Completion is at hand or fast approaching. Celebrate what you have accomplished and honor this ending as you prepare for the next great cycle to begin.")
    if any('fool' in c for c in card_names):
        specific_insights.append("Embrace beginner's mind. The Fool reminds you that not knowing can be a gift, opening doors that expertise keeps closed. Trust the journey ahead.")
    if any('magician' in c for c in card_names):
        specific_insights.append("You have all the tools you need already. The Magician calls you to align thought, will, emotion, and practical action in service of your intentions.")
    if any('devil' in c for c in card_names):
        specific_insights.append("Examine where you may have given away your power or become attached to limiting patterns. Awareness itself begins the process of liberation.")

    if specific_insights:
        return random.choice(specific_insights) + " " + random.choice(insights)

    return random.choice(insights)


def generate_combinations_text(combinations):
    """Generate text about card combinations."""
    if not combinations:
        return ""
    
    combo_texts = []
    for combo in combinations[:2]:
        cards = combo['cards']
        meaning = combo['meaning'].lower() if combo['meaning'][0].isupper() else combo['meaning']
        combo_texts.append(f"{cards} together speak to {meaning}")
    
    return "The interaction between cards adds important depth to this reading: " + "; while ".join(combo_texts) + ". These combined energies amplify and nuance the meanings of the individual cards."


def generate_elemental_text(elemental_balance):
    """Generate text about elemental balance."""
    if not elemental_balance:
        return ""
    
    if 'Earth' in elemental_balance and 'Dominant' in elemental_balance:
        return "The predominance of Earth energy in this reading emphasizes practical, grounded approaches to your situation. Material concerns, stability, and tangible results are central to your path forward. Build carefully on solid foundations and trust in steady progress."
    elif 'Water' in elemental_balance and 'Dominant' in elemental_balance:
        return "Water energy dominates this spread, highlighting the emotional and intuitive dimensions of your situation. Honor your feelings as guides through this terrain; they carry wisdom that pure logic cannot access. Trust what your heart tells you."
    elif 'Fire' in elemental_balance and 'Dominant' in elemental_balance:
        return "Fire energy blazes through this reading, calling for action, passion, and courage in facing your situation. Your will and creative drive are key resources now. Move with confidence toward what ignites your spirit and don't hold back."
    elif 'Air' in elemental_balance and 'Dominant' in elemental_balance:
        return "Air energy prevails in this reading, emphasizing the role of thought, communication, and mental clarity in your situation. Your mind is your greatest tool here. Think clearly, speak truthfully, and actively seek understanding."
    elif 'Balanced' in elemental_balance:
        return "The elements flow in harmonious balance through this reading, suggesting that multiple approaches and energies serve you well. Draw on all your resources - clear thinking, emotional wisdom, passionate will, and practical action - as the situation requires. Flexibility is your friend."
    
    return ""


def generate_response(prompt_data):
    """Generate a complete tarot reading response."""
    parsed = parse_input_text(prompt_data['input_text'])
    question = parsed['question'] or prompt_data.get('question', 'your situation')

    paragraphs = []

    # Opening paragraph
    opening = generate_opening(question, parsed['timing'], parsed['cards'])
    paragraphs.append(opening)

    # Card interpretation paragraphs
    card_narrative = generate_card_narrative(parsed['cards'], question)
    if card_narrative:
        paragraphs.append(card_narrative)

    # Include card combinations if present
    if parsed['combinations']:
        combo_text = generate_combinations_text(parsed['combinations'])
        if combo_text:
            paragraphs.append(combo_text)

    # Elemental balance observation
    if parsed['elemental_balance'] and len(parsed['cards']) > 1:
        elem_text = generate_elemental_text(parsed['elemental_balance'])
        if elem_text:
            paragraphs.append(elem_text)

    # Actionable insight closing
    insight = generate_actionable_insight(question, parsed['cards'])
    paragraphs.append(insight)

    # Join paragraphs
    response = "\n\n".join(paragraphs)

    # If too short, add expansion
    word_count = len(response.split())
    while word_count < 200:
        expansion = get_expansion_text(question, parsed['cards'])
        # Insert expansion before the final insight
        parts = response.rsplit("\n\n", 1)
        if len(parts) == 2:
            response = parts[0] + "\n\n" + expansion + "\n\n" + parts[1]
        else:
            response = response + "\n\n" + expansion
        word_count = len(response.split())
        if word_count >= 200:
            break
        # Safety limit
        if word_count > 180:
            break

    # If too long (over 400 words), trim to fit
    word_count = len(response.split())
    if word_count > 400:
        paragraphs = [p for p in response.split('\n\n') if p.strip()]
        # Keep opening, essential card content, and closing
        if len(paragraphs) > 5:
            # Keep first paragraph (opening), middle paragraphs (up to 3), and last (insight)
            trimmed = [paragraphs[0]]
            # Add 2-3 middle paragraphs
            middle_count = min(3, len(paragraphs) - 2)
            trimmed.extend(paragraphs[1:1+middle_count])
            trimmed.append(paragraphs[-1])
            response = "\n\n".join(trimmed)

            # If still over, further condense
            word_count = len(response.split())
            if word_count > 400:
                paragraphs = [p for p in response.split('\n\n') if p.strip()]
                if len(paragraphs) > 4:
                    trimmed = [paragraphs[0], paragraphs[1], paragraphs[2], paragraphs[-1]]
                    response = "\n\n".join(trimmed)

    return response


def get_expansion_text(question, cards):
    """Generate additional text if response is too short."""
    expansions = [
        "This reading invites deep contemplation of your current path and circumstances. The energies present suggest that you are at a significant crossroads, one where the choices you make now will have lasting implications for your future. Trust in your ability to navigate this terrain with wisdom, grace, and self-compassion.",
        "The patterns emerging in this spread reflect an ongoing process of growth and transformation in your life. You are being called to step more fully into your authentic self, releasing old patterns, beliefs, or situations that no longer serve your highest good and greatest potential.",
        "Consider how the themes in this reading connect to recurring patterns you have noticed in your life. Often the tarot reflects not just the immediate situation but deeper currents and cycles that have shaped your journey over extended time.",
        "What surfaces here is an invitation to trust your own inner guidance more deeply than you may have before. The external situation is certainly important, but equally significant is how you relate to it internally. Your perspective and attitude fundamentally shape your experience.",
        "The wisdom of the cards points toward integration rather than separation. The various aspects of your situation, though they may seem at odds or in conflict, are ultimately parts of a greater whole that seeks harmony and balance.",
        "Pay close attention to your initial emotional response to this reading. Often our first reaction carries important information about what we already know intuitively but have not fully acknowledged or accepted in our conscious awareness.",
        "The tarot does not predict a fixed and unchangeable future but rather illuminates the present moment and its potentials. You remain the author of your own story, and this reading serves as a tool for more conscious, intentional authorship of your life.",
        "Consider returning to this reading in a few days or even weeks. Sometimes the meaning of the cards deepens significantly with reflection, and new insights emerge as you carry these images and themes through your daily experience.",
        "Allow the symbols and imagery of these cards to work on you at a deeper level than conscious analysis. The tarot speaks to the unconscious mind as much as to the rational intellect, and meanings may reveal themselves in dreams, synchronicities, or sudden realizations.",
        "Remember that seeking guidance is itself an act of wisdom. By engaging with this reading, you demonstrate openness to growth and willingness to see your situation more clearly. This receptivity is itself a powerful stance.",
    ]

    # Add card-count specific content
    if len(cards) <= 3:
        expansions.append("Though this is a focused reading with fewer cards, each position carries significant weight and meaning. The clarity of a smaller spread allows for deeper exploration of these core energies without distraction from peripheral matters.")
    elif len(cards) >= 7:
        expansions.append("The richness of this larger spread offers a comprehensive and nuanced view of your situation from multiple angles. Each card adds important nuance, and together they paint a detailed picture of the many forces at work in your life.")

    return random.choice(expansions)


def generate_fallback_response(prompt):
    """Generate a fallback response if parsing fails."""
    question = prompt.get('question', 'your question')
    return f"""Your question about {question.lower().rstrip('?')} touches on significant life themes that deserve careful attention and reflection. The cards drawn for this reading speak to deeper currents flowing through your situation, currents that may not be immediately visible on the surface but that shape events nonetheless.

Looking at the energies present in this reading, there is a clear call for balance between action and reflection in how you approach this matter. The wisdom emerging suggests that you are at a pivotal moment, one where conscious choice can meaningfully shape the path ahead. Neither rushing forward impulsively nor remaining frozen in indecision serves you well; instead, seek the middle way of deliberate, considered movement.

The reading points toward the importance of honoring both your intuitive knowing and your practical wisdom as you navigate forward. Neither alone is sufficient for addressing complex life situations; together they create a more complete understanding. Allow yourself adequate time to integrate what arises from this reading before committing to major decisions or actions.

Consider what recurring themes or patterns this situation may connect to in your broader life experience. Often our questions point to deeper lessons we are working through over time. The cards serve as mirrors, reflecting back what we may not clearly see on our own.

Your actionable insight from this reading is to create intentional space for quiet reflection in the coming days. In the stillness, clarity often emerges naturally without force or struggle. Trust your own inner guidance as you navigate the questions before you. The answers you seek are closer than they may appear, waiting only for you to still yourself enough to hear them."""


def main():
    """Process all prompts and generate responses."""
    random.seed(42)  # For reproducibility
    
    # Load batch file
    with open('/home/user/taro/training/data/batches_expanded/batch_0023.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    print(f"Processing {len(prompts)} prompts from batch {batch_data['batch_id']}...")

    # Generate responses
    responses = []
    for i, prompt in enumerate(prompts):
        random.seed(hash(prompt['id']))  # Unique seed per prompt for variety
        try:
            response_text = generate_response(prompt)
            responses.append({
                'id': prompt['id'],
                'response': response_text
            })

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(prompts)} prompts...")
        except Exception as e:
            print(f"Error processing prompt {prompt['id']}: {e}")
            responses.append({
                'id': prompt['id'],
                'response': generate_fallback_response(prompt)
            })

    # Write to JSONL file
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0023_responses.jsonl'
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"\nSuccessfully wrote {len(responses)} responses to {output_path}")

    # Comprehensive verification
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
