#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0031.json - Final version with word count control"""

import json
import re
import random
import hashlib

def get_seed(prompt_id):
    """Get consistent random seed from prompt ID."""
    return int(hashlib.md5(prompt_id.encode()).hexdigest()[:8], 16)

def parse_input_text(input_text):
    """Parse the input text to extract question, cards, and spread info."""
    result = {
        'timing': None,
        'timing_meaning': None,
        'question': None,
        'cards': [],
        'elemental_balance': None,
        'dominant_element': None,
        'combinations': []
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1).strip()
        result['timing'] = timing_full
        if '---' in timing_full:
            parts = timing_full.split('---')
            result['timing_meaning'] = parts[1].strip() if len(parts) > 1 else None

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Extract cards
    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+(?:\n(?!\d+\.)[^\n]+)*)'

    for match in re.finditer(card_pattern, input_text):
        card = {
            'position_num': match.group(1),
            'position': match.group(2).strip(),
            'name': match.group(3).strip(),
            'keywords': match.group(4).strip(),
            'base_meaning': match.group(5).strip(),
            'position_context': match.group(6).strip(),
            'reversed': '(reversed)' in match.group(3).lower()
        }
        # Clean card name
        card['clean_name'] = card['name'].replace(' (reversed)', '').replace(' (upright)', '').strip()
        result['cards'].append(card)

    # Extract elemental balance
    elemental_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elemental_match:
        result['elemental_balance'] = elemental_match.group(1).strip()

    dominant_match = re.search(r'Dominant:\s*(\w+)\s*energy', input_text)
    if dominant_match:
        result['dominant_element'] = dominant_match.group(1).strip()

    # Extract combinations
    combo_pattern = r'- ([^:]+):\s*([^\n]+(?:\n(?!-)(?![A-Z])[^\n]+)*)'
    combos_section = re.search(r'Card Combinations:(.*?)(?=Elemental Balance|$)', input_text, re.DOTALL)
    if combos_section:
        for match in re.finditer(combo_pattern, combos_section.group(1)):
            result['combinations'].append({
                'cards': match.group(1).strip(),
                'meaning': match.group(2).strip()
            })

    return result

def get_card_element(card):
    """Determine the element of a card."""
    name = card['clean_name'].lower()
    if 'wands' in name:
        return 'Fire'
    elif 'cups' in name:
        return 'Water'
    elif 'swords' in name:
        return 'Air'
    elif 'pentacles' in name:
        return 'Earth'
    elif any(m in name for m in ['emperor', 'tower', 'sun', 'strength', 'chariot', 'wheel', 'magician']):
        return 'Fire'
    elif any(m in name for m in ['empress', 'world', 'hierophant', 'devil', 'hermit']):
        return 'Earth'
    elif any(m in name for m in ['high priestess', 'hanged man', 'moon', 'death', 'star']):
        return 'Water'
    else:
        return 'Air'

def get_question_theme(question):
    """Extract the main theme from the question."""
    q = question.lower()
    if any(w in q for w in ['love', 'relationship', 'partner', 'marriage', 'dating', 'heart']):
        return 'relationships'
    elif any(w in q for w in ['money', 'financial', 'career', 'job', 'work', 'business', 'income']):
        return 'career_finance'
    elif any(w in q for w in ['health', 'healing', 'wellness', 'pain', 'illness', 'treatment']):
        return 'health'
    elif any(w in q for w in ['family', 'parent', 'child', 'sibling', 'mother', 'father']):
        return 'family'
    elif any(w in q for w in ['spiritual', 'purpose', 'meaning', 'soul', 'destiny', 'calling']):
        return 'spiritual'
    elif any(w in q for w in ['decision', 'choice', 'should i', 'which', 'whether']):
        return 'decision'
    elif any(w in q for w in ['friend', 'friendship', 'social']):
        return 'friendship'
    else:
        return 'general'

def generate_opening(parsed, rng, length='normal'):
    """Generate opening paragraph."""
    question = parsed['question']
    timing = parsed['timing'] or ''
    num_cards = len(parsed['cards'])
    theme = get_question_theme(question)

    # Moon phase context
    moon_contexts = {
        'New Moon': 'This New Moon phase supports new beginnings and fresh perspectives',
        'Waxing Crescent': 'The Waxing Crescent energy supports taking those first steps forward',
        'First Quarter': 'The First Quarter moon brings challenges that test your commitment',
        'Waxing Gibbous': 'This Waxing Gibbous phase calls for patience and refinement',
        'Full Moon': 'Under the Full Moon, emotions and truths come to full illumination',
        'Waning Gibbous': 'The Waning Gibbous invites gratitude and sharing of wisdom',
        'Last Quarter': 'This Last Quarter phase supports release and letting go',
        'Waning Crescent': 'The Waning Crescent invites rest and reflection before renewal'
    }

    moon_context = ''
    for phase, context in moon_contexts.items():
        if phase in timing:
            moon_context = context + '. '
            break

    if length == 'extended':
        # Extended opening for single-card readings
        return f"You bring a significant question to this reading: \"{question}\" {moon_context}The cards have been drawn to illuminate the energies, challenges, and possibilities surrounding your inquiry. This single card drawn carries concentrated meaning, serving as a focal point for understanding your current situation. Let us explore what wisdom emerges from this moment of reflection and guidance."
    elif length == 'condensed':
        # Shorter opening for large spreads
        return f"Your question about {question.lower().rstrip('?')} is addressed by the cards before us. {moon_context}Let us examine what they reveal."
    else:
        # Theme-specific openings
        theme_openings = {
            'relationships': [
                f"Your heart's question about {question.lower().rstrip('?')} deserves careful attention. {moon_context}The cards drawn reveal the emotional currents and relational dynamics at play.",
                f"Matters of connection and relationship are rarely simple, and your question reflects this complexity. {moon_context}Let us see what wisdom the cards offer."
            ],
            'career_finance': [
                f"Questions of material security and professional direction carry real weight. Your inquiry about {question.lower().rstrip('?')} arrives at a significant moment. {moon_context}The spread addresses both practical concerns and deeper patterns.",
                f"You seek clarity on {question.lower().rstrip('?')}, a question touching both immediate circumstances and longer-term trajectory. {moon_context}The cards illuminate the forces at work."
            ],
            'health': [
                f"Questions about health and healing require both sensitivity and honesty. {moon_context}Your inquiry about {question.lower().rstrip('?')} opens a dialogue with energies that can offer perspective.",
                f"Matters of physical and emotional wellbeing are deeply personal. {moon_context}The cards respond to your question with insights into the patterns at play."
            ],
            'family': [
                f"Family bonds carry the weight of history, expectation, and love in complex measure. {moon_context}Your question about {question.lower().rstrip('?')} touches on dynamics that have shaped you.",
                f"The relationships we share with family are often our most challenging and rewarding. {moon_context}Let us explore what the cards reveal."
            ],
            'spiritual': [
                f"You ask about something essential to your soul's journey. {moon_context}The question of {question.lower().rstrip('?')} invites deep reflection, and the cards speak to both your current position and potential.",
                f"Spiritual questions often emerge at significant crossroads. {moon_context}Your inquiry resonates with a search for meaning that the cards can help illuminate."
            ],
            'decision': [
                f"The weight of decision rests upon you, and you wisely seek guidance. {moon_context}Your question about {question.lower().rstrip('?')} reflects a genuine desire to choose wisely.",
                f"Facing a significant choice, you ask: {question} {moon_context}The spread helps clarify both options and deeper currents."
            ],
            'friendship': [
                f"Friendships, like all meaningful relationships, require attention and sometimes difficult honesty. {moon_context}Your question about {question.lower().rstrip('?')} touches on connections that matter.",
                f"The bonds of friendship shape our lives in profound ways. {moon_context}Let us see what insight the cards offer."
            ],
            'general': [
                f"You bring an important question to this reading: \"{question}\" {moon_context}The {num_cards} card{'s' if num_cards > 1 else ''} drawn create a narrative addressing your situation.",
                f"Your inquiry about {question.lower().rstrip('?')} arrives at a meaningful moment. {moon_context}The cards illuminate the energies and possibilities surrounding your question."
            ]
        }

        openings = theme_openings.get(theme, theme_openings['general'])
        return rng.choice(openings)

def generate_card_interpretation(card, rng, verbose=True):
    """Generate interpretation for a single card."""
    position = card['position']
    name = card['clean_name']
    reversed_status = " reversed" if card['reversed'] else ""
    context = card['position_context']

    if verbose:
        position_templates = {
            'Past': f"In your past, the {name}{reversed_status} has laid important groundwork. {context.capitalize()}",
            'Present': f"Currently, the {name}{reversed_status} captures where you stand. {context.capitalize()}",
            'Future': f"Looking ahead, the {name}{reversed_status} indicates what is forming. {context.capitalize()}",
            'Situation': f"The {name}{reversed_status} encapsulates your current situation: {context.lower()}",
            'Action': f"The {name}{reversed_status} calls you to specific action. {context.capitalize()}",
            'Outcome': f"The {name}{reversed_status} as outcome suggests where this leads. {context.capitalize()}",
            'Challenge': f"Your challenge, represented by the {name}{reversed_status}, demands attention. {context.capitalize()}",
            'Advice': f"The {name}{reversed_status} offers essential guidance: {context.lower()}",
            'Above': f"Above you, representing highest potential, the {name}{reversed_status} shines. {context.capitalize()}",
            'Below': f"At the foundation, the {name}{reversed_status} reveals deeper currents. {context.capitalize()}",
            'External': f"External influences, shown by the {name}{reversed_status}, bring outside forces to bear. {context.capitalize()}",
            'External Influences': f"Forces beyond your control, represented by the {name}{reversed_status}, play their part. {context.capitalize()}",
            'Hopes/Fears': f"The {name}{reversed_status} reveals what you both hope for and fear. {context.capitalize()}",
            'Hidden Influences': f"Working beneath awareness, the {name}{reversed_status} shapes events invisibly. {context.capitalize()}",
            'Obstacles': f"Standing between you and your goal, the {name}{reversed_status} must be addressed. {context.capitalize()}",
            "Today's Guidance": f"For today, the {name}{reversed_status} offers focused guidance: {context.lower()}"
        }
    else:
        # Condensed versions for large spreads
        position_templates = {
            'Past': f"The {name}{reversed_status} in your past shows {context.split('.')[0].lower()}.",
            'Present': f"Currently, the {name}{reversed_status}: {context.split('.')[0].lower()}.",
            'Future': f"Ahead, the {name}{reversed_status} suggests {context.split('.')[0].lower()}.",
            'Situation': f"The {name}{reversed_status}: {context.split('.')[0].lower()}.",
            'Action': f"Action required: the {name}{reversed_status} says {context.split('.')[0].lower()}.",
            'Outcome': f"Outcome via the {name}{reversed_status}: {context.split('.')[0].lower()}.",
            'Challenge': f"Your challenge ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'Advice': f"Advice from the {name}{reversed_status}: {context.split('.')[0].lower()}.",
            'Above': f"Highest potential ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'Below': f"Foundation ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'External': f"External forces ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'External Influences': f"Outside influences ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'Hopes/Fears': f"Hopes and fears ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'Hidden Influences': f"Hidden ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            'Obstacles': f"Obstacle ({name}{reversed_status}): {context.split('.')[0].lower()}.",
            "Today's Guidance": f"Today's guidance ({name}{reversed_status}): {context.split('.')[0].lower()}."
        }

    return position_templates.get(position, f"The {name}{reversed_status} in {position}: {context.split('.')[0].lower()}.")

def generate_card_paragraphs(cards, parsed, rng, verbose=True):
    """Generate paragraphs for all cards."""
    if not cards:
        return []

    if len(cards) <= 3:
        # Single paragraph with all cards
        sentences = [generate_card_interpretation(c, rng, verbose) for c in cards]
        return [" ".join(sentences)]
    else:
        # Group by function for larger spreads
        groups = [
            (['Past', 'Below', 'Hidden Influences', 'Situation'], 'foundation'),
            (['Present', 'Challenge', 'Obstacles'], 'present'),
            (['External', 'External Influences', 'Action'], 'external'),
            (['Above', 'Advice', 'Hopes/Fears', "Today's Guidance"], 'guidance'),
            (['Future', 'Outcome'], 'outcome')
        ]

        paragraphs = []
        for positions, _ in groups:
            group_cards = [c for c in cards if c['position'] in positions]
            if group_cards:
                sentences = [generate_card_interpretation(c, rng, verbose) for c in group_cards]
                paragraphs.append(" ".join(sentences))

        return paragraphs

def generate_synthesis(parsed, rng, length='normal'):
    """Generate synthesis paragraph connecting themes."""
    cards = parsed['cards']
    if len(cards) < 2:
        return ""

    reversed_count = sum(1 for c in cards if c['reversed'])
    total = len(cards)

    # Element analysis
    elements = [get_card_element(c) for c in cards]
    element_counts = {e: elements.count(e) for e in set(elements)}
    dominant = max(element_counts.keys(), key=lambda x: element_counts[x]) if element_counts else None

    element_insights = {
        'Fire': 'The prevalence of Fire energy suggests this is a time for bold action, passion, and creative initiative. Move forward with conviction.',
        'Water': 'Water energy flows through this reading, emphasizing emotional intelligence, intuition, and authentic connection. Trust your feelings.',
        'Air': 'Air energy highlights clear thinking, honest communication, and intellectual discernment. Truth and clarity are your allies.',
        'Earth': 'Earth energy grounds this reading in practical matters and the importance of steady, patient effort. Build on solid foundations.'
    }

    synthesis_parts = []

    if length == 'extended':
        # More detailed synthesis for shorter readings
        if reversed_count > total / 2:
            synthesis_parts.append("The significant number of reversed cards suggests that much of the current energy is internalized or blocked. This is a time for inner work, honest self-reflection, and addressing what may be stuck before external progress becomes possible. Consider what beliefs, fears, or patterns might be creating resistance.")
        elif reversed_count > 0:
            synthesis_parts.append(f"The balance of {total - reversed_count} upright and {reversed_count} reversed cards suggests a situation with both momentum and obstacles, areas of flow and places where energy is blocked or needs redirection.")

        if dominant and element_counts[dominant] > 1:
            synthesis_parts.append(element_insights.get(dominant, ''))

        if parsed['combinations']:
            combo = parsed['combinations'][0]
            synthesis_parts.append(f"The relationship between {combo['cards']} is particularly telling: {combo['meaning']}")
    elif length == 'condensed':
        # Brief synthesis for longer readings
        if reversed_count > total / 2:
            synthesis_parts.append("Multiple reversed cards indicate blocked or internalized energy requiring attention.")
        if dominant and element_counts[dominant] > 2:
            synthesis_parts.append(f"{dominant} energy dominates, emphasizing {element_insights.get(dominant, '').split('.')[0].lower()}.")
    else:
        # Normal synthesis
        if reversed_count > 0:
            synthesis_parts.append(f"The mix of {total - reversed_count} upright and {reversed_count} reversed cards shows both flow and blockage in your situation.")
        if dominant and element_counts[dominant] > 1:
            synthesis_parts.append(element_insights.get(dominant, ''))

    return " ".join(synthesis_parts)

def generate_single_card_expansion(card, parsed, rng):
    """Generate expanded content for single-card readings."""
    element = get_card_element(card)
    theme = get_question_theme(parsed['question'])

    element_contexts = {
        'Fire': "This Fire energy speaks to passion, will, courage, and the drive to act. It asks you to consider where you might be holding back when bold action is needed, or conversely, where impulsiveness might benefit from temperance.",
        'Water': "This Water energy emphasizes emotion, intuition, relationships, and the depths of feeling. It invites you to honor your emotional truth and trust the wisdom that comes from within rather than from logic alone.",
        'Air': "This Air energy highlights thought, communication, truth, and mental clarity. It suggests that clear seeing and honest expression are central to your situation, and that the mind's role cannot be overlooked.",
        'Earth': "This Earth energy grounds you in practical reality, material concerns, patience, and steady effort. It reminds you that sustainable progress comes through consistent action and attention to concrete details."
    }

    reversal_context = ""
    if card['reversed']:
        reversal_context = " The reversed orientation of this card suggests that its energy is blocked, internalized, or expressing in an imbalanced way. Rather than seeing this as purely negative, consider it an invitation to examine what might need adjustment, what shadow aspect calls for acknowledgment, or what internal work precedes external manifestation."

    # Add base meaning if available
    base_meaning = ""
    if card['base_meaning'] and card['base_meaning'] != 'Meaning not available':
        base_meaning = f" The essential meaning of this card speaks to: {card['base_meaning']}"

    return f"{element_contexts.get(element, '')}{reversal_context}{base_meaning}"

def generate_closing(parsed, rng, length='normal'):
    """Generate actionable closing paragraph."""
    question = parsed['question']
    cards = parsed['cards']
    theme = get_question_theme(question)

    # Find key cards
    advice_card = next((c for c in cards if c['position'] == 'Advice'), None)
    outcome_card = next((c for c in cards if c['position'] in ['Outcome', 'Future']), None)
    action_card = next((c for c in cards if c['position'] == 'Action'), None)

    # Generate specific action
    specific_action = None
    if advice_card:
        specific_action = advice_card['position_context'].split('.')[0]
        if specific_action.lower().startswith('the guidance is'):
            specific_action = specific_action[15:].strip()
    elif action_card:
        specific_action = action_card['position_context'].split('.')[0]

    action_phrase = f"{specific_action}. " if specific_action else ""

    if length == 'extended':
        # Extended closing for short readings
        theme_closings = {
            'relationships': f"In matters of the heart, authenticity is your greatest ally. {action_phrase}Take one small step toward honest communication this week, even if it feels vulnerable. Remember that healthy relationships require both giving and receiving, and that you deserve to have your needs honored. The path forward may not be perfectly clear, but each authentic interaction builds toward the connection you seek.",
            'career_finance': f"Financial and career matters respond to a combination of strategic thinking and aligned action. {action_phrase}Your practical next step is to identify one concrete action you can take this week that moves you toward stability or growth. Trust your ability to navigate this terrain, and remember that patience is not passive waiting but active preparation for opportunity.",
            'health': f"Healing is rarely linear, and the cards honor the complexity of your experience. {action_phrase}Your immediate action is to identify one small act of self-care you can commit to this week. Remember that addressing mind, body, and spirit together often yields the best results, and that seeking support is a sign of wisdom, not weakness.",
            'family': f"Family relationships carry the weight of history, but they can also evolve. {action_phrase}Your actionable step is to choose one relationship and identify what you can realistically offer or expect from it. Boundaries are not walls but bridges that make genuine connection possible. Transformation in family systems begins with individual choices.",
            'spiritual': f"Your spiritual journey is uniquely your own, yet it connects you to something greater. {action_phrase}Make time this week for stillness and reflection, even if only for a few minutes. The answers you seek are not outside you but waiting to be recognized within. Trust the unfolding of your path.",
            'decision': f"Decisions become clearer when we understand both our values and our fears. {action_phrase}Before choosing, ask yourself: which option aligns more closely with who I want to become? Sometimes the right choice feels like expansion rather than contraction. Trust yourself to navigate whatever follows your decision.",
            'friendship': f"Friendships, like all living things, require tending. {action_phrase}Your next step is to be clear with yourself about what you need and what you can offer in this connection. Honest assessment now prevents resentment later. Consider having a direct conversation, or if that's not possible, journaling your thoughts for clarity.",
            'general': f"The reading before you offers both insight and direction. {action_phrase}Your immediate action is to identify the one thing that felt most resonant as you considered these cards. Start there. Remember that you have more agency than you might feel in this moment, and that clarity comes through movement, not just contemplation. Trust the process."
        }
    elif length == 'condensed':
        # Brief closing for long readings
        theme_closings = {
            'relationships': f"{action_phrase}Move toward authentic communication. You deserve connection that honors your needs.",
            'career_finance': f"{action_phrase}Take one concrete step this week toward your goal. Trust your ability to navigate.",
            'health': f"{action_phrase}Commit to one small act of self-care this week. Healing happens gradually.",
            'family': f"{action_phrase}Choose one boundary to establish or one connection to nurture. Start there.",
            'spiritual': f"{action_phrase}Make time for reflection. The answers you seek are within you.",
            'decision': f"{action_phrase}Choose what aligns with who you want to become. Trust yourself.",
            'friendship': f"{action_phrase}Be clear about what you need and can offer. Honest assessment serves everyone.",
            'general': f"{action_phrase}Identify what resonated most and act on it. Clarity comes through movement."
        }
    else:
        theme_closings = {
            'relationships': f"In matters of the heart, authenticity is your greatest ally. {action_phrase}Take one small step toward honest communication this week. Remember that healthy relationships require both giving and receiving.",
            'career_finance': f"Financial and career matters respond to strategic thinking and aligned action. {action_phrase}Identify one concrete action you can take this week. Trust your ability to navigate this terrain.",
            'health': f"Healing is rarely linear. {action_phrase}Commit to one small act of self-care this week. Remember that addressing mind, body, and spirit together often yields the best results.",
            'family': f"Family relationships carry history but can also evolve. {action_phrase}Identify what you can realistically offer or expect. Boundaries make genuine connection possible.",
            'spiritual': f"Your spiritual journey is uniquely your own. {action_phrase}Make time for stillness and reflection. The answers you seek are waiting within.",
            'decision': f"Decisions clarify when we understand our values and fears. {action_phrase}Ask which option aligns with who you want to become. Trust yourself to navigate what follows.",
            'friendship': f"Friendships require honest attention. {action_phrase}Be clear about what you need and can offer. Honest assessment now prevents resentment later.",
            'general': f"The reading offers both insight and direction. {action_phrase}Identify what felt most resonant and start there. Clarity comes through movement, not just contemplation."
        }

    return theme_closings.get(theme, theme_closings['general'])

def generate_reading(prompt):
    """Generate a complete tarot reading response with word count control."""
    rng = random.Random(get_seed(prompt['id']))
    parsed = parse_input_text(prompt['input_text'])

    if not parsed['cards']:
        return f"Your question about {prompt.get('question', 'your situation')} invites reflection. Even in moments of uncertainty, remember that you carry wisdom within you. Take time to consider what you truly need, and trust that clarity will emerge as you move forward with intention and openness. The path ahead may not be fully visible, but each step you take with awareness brings you closer to understanding. Consider what small action you might take today that aligns with your deeper values and aspirations."

    cards = parsed['cards']
    num_cards = len(cards)

    # Determine content strategy based on card count
    if num_cards == 1:
        # Single card: Extended everything
        paragraphs = [
            generate_opening(parsed, rng, 'extended'),
            generate_card_interpretation(cards[0], rng, True),
            generate_single_card_expansion(cards[0], parsed, rng),
            generate_closing(parsed, rng, 'extended')
        ]
    elif num_cards <= 3:
        # Small spread: Normal + some extension
        paragraphs = [
            generate_opening(parsed, rng, 'normal')
        ]
        paragraphs.extend(generate_card_paragraphs(cards, parsed, rng, True))
        synthesis = generate_synthesis(parsed, rng, 'extended')
        if synthesis:
            paragraphs.append(synthesis)
        paragraphs.append(generate_closing(parsed, rng, 'normal'))
    elif num_cards <= 7:
        # Medium spread: Normal
        paragraphs = [
            generate_opening(parsed, rng, 'normal')
        ]
        paragraphs.extend(generate_card_paragraphs(cards, parsed, rng, True))
        synthesis = generate_synthesis(parsed, rng, 'normal')
        if synthesis:
            paragraphs.append(synthesis)
        paragraphs.append(generate_closing(parsed, rng, 'normal'))
    else:
        # Large spread (8+): Condensed
        paragraphs = [
            generate_opening(parsed, rng, 'condensed')
        ]
        paragraphs.extend(generate_card_paragraphs(cards, parsed, rng, False))
        synthesis = generate_synthesis(parsed, rng, 'condensed')
        if synthesis:
            paragraphs.append(synthesis)
        paragraphs.append(generate_closing(parsed, rng, 'condensed'))

    response = "\n\n".join(p for p in paragraphs if p)

    # Word count adjustment
    word_count = len(response.split())

    if word_count < 200:
        # Add filler content
        fillers = [
            "Take a moment to sit with these insights before taking action. Sometimes the most profound guidance needs time to integrate.",
            "The cards speak not as destiny but as possibility. Your choices remain your own, informed but not determined by what is revealed.",
            "Consider returning to this reading in a few days to see what new understanding has emerged from reflection.",
            "Remember that tarot illuminates patterns and possibilities rather than fixed outcomes. You always retain the power of choice."
        ]
        response += "\n\n" + rng.choice(fillers)

    elif word_count > 400:
        # Trim by reducing paragraphs
        paragraphs = response.split("\n\n")
        while len("\n\n".join(paragraphs).split()) > 400 and len(paragraphs) > 3:
            # Remove the longest middle paragraph
            if len(paragraphs) > 4:
                middle_start = 1
                middle_end = len(paragraphs) - 1
                lengths = [(i, len(paragraphs[i].split())) for i in range(middle_start, middle_end)]
                longest_idx = max(lengths, key=lambda x: x[1])[0]
                paragraphs.pop(longest_idx)
            else:
                # Truncate the middle paragraphs
                for i in range(1, len(paragraphs) - 1):
                    sentences = paragraphs[i].split('. ')
                    if len(sentences) > 2:
                        paragraphs[i] = '. '.join(sentences[:len(sentences)//2 + 1]) + '.'
                break
        response = "\n\n".join(paragraphs)

    return response

def main():
    # Load batch file
    with open('/home/user/taro/training/data/batches_expanded/batch_0031.json', 'r') as f:
        data = json.load(f)

    prompts = data['prompts']
    print(f"Processing {len(prompts)} prompts...")

    # Generate responses
    responses = []
    word_counts = []

    for i, prompt in enumerate(prompts):
        response = generate_reading(prompt)
        responses.append({
            'id': prompt['id'],
            'response': response
        })
        word_counts.append(len(response.split()))

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(prompts)} prompts...")

    # Write to JSONL
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0031_responses.jsonl'
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    # Statistics
    in_range = sum(1 for wc in word_counts if 200 <= wc <= 400)
    too_short = sum(1 for wc in word_counts if wc < 200)
    too_long = sum(1 for wc in word_counts if wc > 400)

    print(f"\nWritten {len(responses)} responses to {output_path}")
    print(f"\nWord count statistics:")
    print(f"  Min: {min(word_counts)}")
    print(f"  Max: {max(word_counts)}")
    print(f"  Average: {sum(word_counts)/len(word_counts):.1f}")
    print(f"\nStatus breakdown:")
    print(f"  OK (200-400): {in_range} ({in_range/len(word_counts)*100:.1f}%)")
    print(f"  Too short (<200): {too_short}")
    print(f"  Too long (>400): {too_long}")

    # Print samples
    print("\n" + "="*60)
    print("SAMPLE RESPONSES")
    print("="*60)

    for idx in [0, 4, 50]:  # Sample different types
        if idx < len(responses):
            print(f"\n--- Response {idx+1} (ID: {responses[idx]['id']}) ---")
            print(f"Words: {word_counts[idx]}")
            print(responses[idx]['response'][:1200])
            if len(responses[idx]['response']) > 1200:
                print("...")

if __name__ == '__main__':
    main()
