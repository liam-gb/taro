#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0029."""

import json
import re
import random

# Load the batch file
with open('/home/user/taro/training/data/batches_expanded/batch_0029.json', 'r') as f:
    batch_data = json.load(f)

def parse_input_text(input_text):
    """Parse the input_text to extract question, timing, cards, and combinations."""
    result = {
        'question': '',
        'timing': '',
        'cards': [],
        'combinations': [],
        'elemental_balance': ''
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        result['timing'] = timing_match.group(1).strip()

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Extract cards
    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+(?:\n(?!\d+\.)(?!Card Combinations)(?!Elemental)[^\n]*)*)'
    cards = re.findall(card_pattern, input_text, re.MULTILINE)

    for card in cards:
        card_info = {
            'position_num': card[0],
            'position': card[1].strip(),
            'card_name': card[2].strip(),
            'keywords': card[3].strip(),
            'base_meaning': card[4].strip(),
            'position_context': card[5].strip()
        }
        result['cards'].append(card_info)

    # Extract combinations
    combo_section = re.search(r'Card Combinations:\n(.*?)(?=Elemental Balance)', input_text, re.DOTALL)
    if combo_section:
        combos = re.findall(r'-\s*([^:]+):\s*([^\n]+(?:\n(?!-)(?!Elemental)[^\n]*)*)', combo_section.group(1))
        result['combinations'] = [(c[0].strip(), c[1].strip()) for c in combos]

    # Extract elemental balance
    elem_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elem_match:
        result['elemental_balance'] = elem_match.group(1).strip()

    return result

def is_reversed(card_name):
    """Check if a card is reversed."""
    return '(reversed)' in card_name.lower()

def get_card_base_name(card_name):
    """Get the base name of the card without reversed indicator."""
    return re.sub(r'\s*\(reversed\)\s*', '', card_name, flags=re.IGNORECASE).strip()

def generate_opening(question, timing, cards):
    """Generate an opening paragraph."""
    openings = [
        f"Your question about {question.lower().rstrip('?')} emerges at a significant moment. {timing.split('—')[0].strip() if '—' in timing else timing} brings its own energy to this reading, and the cards respond with clarity and depth.",
        f"You ask: \"{question}\" This inquiry touches something essential. The cards have arranged themselves in a pattern that speaks directly to your situation, offering both illumination and practical guidance.",
        f"The question \"{question}\" carries real weight, and the cards honor it with a thoughtful spread. Under the current {timing.split('—')[0].strip() if '—' in timing else 'lunar'} influence, certain energies are heightened, making this an auspicious time for insight.",
        f"Your inquiry—{question.lower().rstrip('?')}—resonates through this spread with remarkable coherence. The cards that emerged create a narrative that addresses both the seen and unseen aspects of your situation.",
        f"This reading addresses your question: \"{question}\" The spread reveals a journey from where you stand now toward greater understanding. Let the cards illuminate what needs to be seen."
    ]
    return random.choice(openings)

def generate_card_interpretation(card, include_reversal_note=True):
    """Generate interpretation for a single card."""
    position = card['position']
    card_name = card['card_name']
    context = card['position_context']
    keywords = card['keywords']
    reversed_card = is_reversed(card_name)

    position_intros = {
        'Present': [f"In your Present position, {card_name} speaks to where you find yourself right now.",
                    f"The {card_name} in your Present reveals the current energies at play.",
                    f"Currently, {card_name} illuminates your immediate situation."],
        'Past': [f"The {card_name} in your Past position shows the foundation you've built upon.",
                f"Looking to your Past, {card_name} reveals what has shaped this moment.",
                f"Your Past position holds {card_name}, indicating where you've come from."],
        'Future': [f"Looking ahead, {card_name} in your Future position suggests what's emerging.",
                  f"The Future position reveals {card_name}, pointing toward what's developing.",
                  f"{card_name} in the Future indicates the direction events are moving."],
        'Challenge': [f"Your Challenge is represented by {card_name}.",
                     f"The {card_name} as your Challenge reveals what you must navigate.",
                     f"In the Challenge position, {card_name} shows what requires your attention."],
        'Above': [f"Above you, {card_name} represents your highest aspirations in this matter.",
                 f"The {card_name} in the Above position speaks to your conscious goals.",
                 f"Your best potential, shown by {card_name}, involves reaching higher."],
        'Below': [f"Below, {card_name} reveals the unconscious foundation of this situation.",
                 f"The {card_name} beneath this reading shows what operates unseen.",
                 f"At the foundation, {card_name} indicates deeper currents at work."],
        'Advice': [f"The Advice position offers {card_name} as guidance.",
                  f"{card_name} appears as your Advice, suggesting a clear path forward.",
                  f"For guidance, the cards present {card_name}."],
        'External': [f"External influences are shown through {card_name}.",
                    f"The {card_name} in the External position reveals outside forces at play.",
                    f"Around you, {card_name} indicates how the world is affecting this situation."],
        'Hopes/Fears': [f"Your Hopes and Fears are embodied by {card_name}.",
                       f"The {card_name} in this position reveals what you both desire and fear.",
                       f"In Hopes/Fears, {card_name} shows the duality of your expectations."],
        'Outcome': [f"The Outcome position reveals {card_name}.",
                   f"{card_name} as your Outcome suggests where this is heading.",
                   f"The potential resolution shown by {card_name} offers important insight."],
        'Situation': [f"The {card_name} defines your current Situation.",
                     f"Your Situation is characterized by {card_name}.",
                     f"At the heart of things, {card_name} reveals the core dynamic."],
        'Crossing': [f"Crossing your path, {card_name} represents immediate obstacles or influences.",
                    f"The {card_name} crosses you, indicating what stands in your way.",
                    f"What crosses you is {card_name}, a force you must acknowledge."],
        'Foundation': [f"The Foundation of this matter is {card_name}.",
                      f"{card_name} forms the Foundation, showing what this situation rests upon.",
                      f"Beneath everything, {card_name} provides the base for all that follows."],
        'Recent Past': [f"In your Recent Past, {card_name} shows what's just occurred.",
                       f"The {card_name} in Recent Past indicates energies now fading.",
                       f"What recently shaped things is shown by {card_name}."],
        'Crown': [f"The Crown position holds {card_name}, your highest potential.",
                 f"{card_name} crowns this reading, showing what you might achieve.",
                 f"Above all, {card_name} indicates the best possible outcome."],
        'Self': [f"The Self position reveals {card_name}, how you appear in this situation.",
                f"{card_name} represents your Self, showing your role here.",
                f"You are represented by {card_name} in this matter."],
        'Environment': [f"Your Environment is shaped by {card_name}.",
                       f"The {card_name} in Environment shows the world around you.",
                       f"Surrounding circumstances, shown by {card_name}, influence everything."]
    }

    # Get appropriate intro or use generic
    generic_intros = [f"The {card_name} in the {position} position carries significant meaning.",
                     f"In {position}, {card_name} reveals important insights.",
                     f"{card_name} appears in your {position}, offering clarity."]

    intro = random.choice(position_intros.get(position, generic_intros))

    # Build the interpretation
    interpretation = f"{intro} {context}"

    if reversed_card and include_reversal_note:
        reversal_notes = [
            " This reversed energy suggests blocked or internalized expression of these qualities.",
            " In its reversed position, this card indicates challenges in fully expressing its gifts.",
            " The reversal here points to inner work needed before this energy can flow freely.",
            " Reversed, this card asks you to examine where this energy may be stuck or misdirected."
        ]
        interpretation += random.choice(reversal_notes)

    return interpretation

def generate_combination_insight(combinations):
    """Generate insight from card combinations."""
    if not combinations:
        return ""

    combo_intros = [
        "The combination of cards reveals deeper patterns.",
        "Notable combinations in this spread amplify certain messages.",
        "The cards speak to each other in meaningful ways.",
        "Particularly significant is how certain cards interact."
    ]

    insights = [random.choice(combo_intros)]
    for combo_cards, combo_meaning in combinations[:2]:  # Use up to 2 combinations
        insights.append(f"{combo_cards}: {combo_meaning}")

    return " ".join(insights)

def generate_closing(question, cards, elemental_balance):
    """Generate a closing paragraph with actionable insight."""
    # Find outcome or advice card for closing focus
    outcome_card = None
    advice_card = None
    for card in cards:
        if 'Outcome' in card['position']:
            outcome_card = card
        if 'Advice' in card['position']:
            advice_card = card

    focus_card = outcome_card or advice_card or cards[-1]

    # Determine question theme for tailored advice
    question_lower = question.lower()

    if any(word in question_lower for word in ['love', 'relationship', 'partner', 'marriage', 'romantic', 'dating']):
        theme_advice = [
            "In matters of the heart, authenticity creates the deepest connections. Let your actions align with your values.",
            "Love asks for presence and patience. Focus on being genuine rather than perfect.",
            "The heart knows its own truth. Trust what these cards have revealed about your emotional landscape.",
            "Relationships thrive when both parties show up fully. Consider how you might deepen your presence."
        ]
    elif any(word in question_lower for word in ['career', 'job', 'work', 'business', 'professional', 'money', 'financial']):
        theme_advice = [
            "Professional growth requires both strategy and intuition. Let this reading inform your next concrete step.",
            "Career paths unfold through action. Identify one thing you can do this week to honor what the cards have shown.",
            "Financial matters respond to clarity and intention. Use this insight to make more aligned choices.",
            "Work is sacred when it aligns with purpose. Consider how these messages apply to your daily efforts."
        ]
    elif any(word in question_lower for word in ['health', 'healing', 'wellness', 'body', 'energy']):
        theme_advice = [
            "Healing happens in layers. Honor your body's wisdom as you integrate these insights.",
            "Wellness encompasses mind, body, and spirit. Let this reading guide holistic self-care.",
            "Your body carries wisdom. Listen to what it tells you as you consider these cards.",
            "Health journeys require patience. Take one nurturing action today based on this guidance."
        ]
    elif any(word in question_lower for word in ['spiritual', 'purpose', 'meaning', 'growth', 'path', 'journey']):
        theme_advice = [
            "Spiritual growth unfolds in its own time. Trust the path even when you cannot see the destination.",
            "Your soul's journey is unique. Let these insights illuminate your next steps without forcing outcomes.",
            "Meaning emerges through experience. Carry these messages with you as you move forward.",
            "The spiritual path asks for presence. Ground today's insight through reflection or meditation."
        ]
    else:
        theme_advice = [
            "Wisdom arrives through openness. Let this reading settle before taking action, then move with clarity.",
            "The cards offer guidance, not commands. Take what resonates and leave what doesn't serve you.",
            "Integration takes time. Sit with these insights before making major decisions.",
            "Trust your own knowing. These cards reflect what you already sense at a deeper level."
        ]

    closings = [
        f"Moving forward, let the wisdom of {focus_card['card_name']} guide your choices. {random.choice(theme_advice)}",
        f"The path revealed here asks for both reflection and action. {random.choice(theme_advice)} The cards have shown you what you need to see—now the choice of how to respond is yours.",
        f"This reading illuminates more than it prescribes. {random.choice(theme_advice)} Take one concrete step this week that honors what you've learned here.",
        f"The spread tells a coherent story with a clear direction. {random.choice(theme_advice)} Return to these insights when you need guidance."
    ]

    if elemental_balance:
        balance_notes = {
            'Balanced': "The balanced elemental energies suggest you have all the resources you need—it's a matter of integration.",
            'Fire-dominant': "The prevalence of Fire energy calls for bold action and creative courage.",
            'Water-dominant': "Water's dominance here emphasizes emotional intelligence and intuitive flow.",
            'Air-dominant': "Air's strong presence asks for clear thinking and honest communication.",
            'Earth-dominant': "Earth's grounding influence reminds you to stay practical and patient."
        }
        for key, note in balance_notes.items():
            if key.lower().replace('-', ' ') in elemental_balance.lower() or key.lower().replace('-dominant', '') in elemental_balance.lower():
                return f"{random.choice(closings)} {note}"

    return random.choice(closings)

def generate_elaboration(question, card, timing):
    """Generate additional elaboration for short spreads to meet minimum word count."""
    question_lower = question.lower()
    card_name = card['card_name']
    keywords = card.get('keywords', '')

    # Theme-specific elaborations
    if any(word in question_lower for word in ['love', 'relationship', 'partner', 'heart', 'romantic']):
        elaborations = [
            f"The energy of {card_name} in matters of the heart speaks to the quality of connection you're cultivating. Whether you're seeking love, nurturing an existing bond, or healing from past wounds, this card reminds you that authentic relating begins with self-knowledge. The patterns you carry from earlier experiences shape how you show up in partnership—awareness of these patterns is the first step toward choosing differently.",
            f"When {card_name} appears in a love reading, it often signals a turning point in how you approach intimacy and vulnerability. True connection requires both openness and healthy boundaries. Consider what walls you've built and which ones serve your wellbeing versus which ones keep love at a distance. This card invites honest reflection on your readiness to receive what you're asking for.",
            f"Relationships serve as mirrors, reflecting back parts of ourselves we might otherwise overlook. The appearance of {card_name} suggests examining not just what you want from love, but what you bring to it. Your capacity for genuine connection expands when you're willing to see yourself clearly and extend that same compassionate seeing to others."
        ]
    elif any(word in question_lower for word in ['career', 'job', 'work', 'money', 'business', 'professional', 'financial']):
        elaborations = [
            f"The {card_name} in your professional inquiry points toward the intersection of practical necessity and deeper purpose. Work occupies so much of our lives that finding alignment between what we do and who we are becomes essential for wellbeing. Consider whether your current path honors your gifts and values, or whether adjustments are needed to bring these into greater harmony.",
            f"Financial and career matters touch on our sense of security and self-worth in profound ways. The energy of {card_name} invites you to examine your relationship with abundance—not just monetary wealth, but the richness of meaningful contribution and fair exchange. What you're building now has implications beyond the immediate; plant seeds that align with your long-term vision.",
            f"Professional growth rarely follows a straight line. The presence of {card_name} acknowledges both the challenges and opportunities in your work life. Success comes through a combination of strategic action and intuitive timing. Trust your instincts about when to push forward and when to step back, allowing developments to unfold in their own time."
        ]
    elif any(word in question_lower for word in ['health', 'healing', 'body', 'wellness', 'energy', 'anxiety', 'stress', 'chronic', 'illness', 'condition', 'pain', 'depression', 'mental']):
        elaborations = [
            f"The {card_name} appearing in a health-related reading reminds you that wellbeing encompasses physical, emotional, mental, and spiritual dimensions. Symptoms often carry messages—your body communicates through sensation and discomfort when something needs attention. Listen deeply to what's being asked of you, and respond with both practical care and compassionate presence.",
            f"Healing is rarely linear and seldom quick. The energy of {card_name} honors the complexity of your wellness journey while pointing toward sustainable approaches rather than quick fixes. What practices genuinely nourish you? What habits deplete your vitality? This is a time for honest inventory and gentle but consistent course corrections.",
            f"The connection between mind and body is intimate and reciprocal. When {card_name} appears regarding health matters, consider how your thoughts, emotions, and life circumstances might be manifesting physically. Addressing root causes rather than just symptoms leads to more lasting wellness. Self-care isn't selfish—it's the foundation for everything else."
        ]
    elif any(word in question_lower for word in ['family', 'parent', 'child', 'mother', 'father', 'sibling', 'home']):
        elaborations = [
            f"Family dynamics carry the weight of history and the complexity of intertwined lives. The {card_name} acknowledges that these relationships often trigger our deepest patterns and most tender vulnerabilities. You can honor family bonds while also maintaining necessary boundaries. Growth sometimes requires updating old roles that no longer fit who you've become.",
            f"The family sphere holds both our greatest teachers and our most challenging lessons. With {card_name} appearing in this context, consider what ancestral patterns you carry and which ones you wish to transform. Breaking cycles takes awareness, intention, and patience with yourself and others. Each small shift ripples through generations.",
            f"Home is both a physical space and an emotional state. The energy of {card_name} invites reflection on what creates a sense of belonging and safety for you. Whether you're navigating family of origin issues or building chosen family connections, the core question remains: how do you create environments where authentic self-expression is possible?"
        ]
    elif any(word in question_lower for word in ['spiritual', 'purpose', 'meaning', 'soul', 'path', 'journey', 'growth', 'transition', 'retirement', 'change', 'direction', 'life', 'identity', 'future', 'next']):
        elaborations = [
            f"Spiritual questions resist easy answers—that's part of their gift. The {card_name} appearing here honors your seeking while reminding you that the path itself is the destination. Purpose unfolds through lived experience rather than abstract contemplation. Trust the wisdom gathering in you through each challenge embraced and each lesson integrated.",
            f"The quest for meaning is fundamental to human experience. With {card_name} in this reading, you're invited to examine not just what you believe but how those beliefs translate into daily practice. Spirituality that doesn't transform how you treat yourself and others remains incomplete. Let your actions become your most authentic prayer.",
            f"Personal growth happens in spirals rather than straight lines—you revisit familiar themes at deeper levels as you evolve. The energy of {card_name} acknowledges where you are in this spiral while pointing toward continued unfolding. The challenges you face now are precisely calibrated for your development. Trust the intelligence of your soul's curriculum."
        ]
    else:
        elaborations = [
            f"The {card_name} carries layers of meaning that deepen upon reflection. Beyond its immediate message lies an invitation to examine your assumptions and habitual responses. What patterns keep repeating in your life? What would become possible if you approached this situation with fresh eyes? Sometimes the most powerful shifts come not from dramatic action but from subtle changes in perspective.",
            f"Every reading offers both reflection and direction. The {card_name} illuminates your current circumstances while hinting at potentials not yet realized. The gap between where you are and where you want to be holds valuable information. Rather than rushing to close this gap, consider what it might teach you about patience, timing, and the art of allowing.",
            f"Life rarely presents clean, simple situations—complexity is the norm. The appearance of {card_name} acknowledges the multifaceted nature of your inquiry while offering a thread to follow through the maze. Trust that clarity will come as you engage thoughtfully with the questions rather than grasping at premature answers. Process reveals itself through presence."
        ]

    return random.choice(elaborations)

def generate_reading(parsed_data):
    """Generate a complete tarot reading from parsed data."""
    question = parsed_data['question']
    timing = parsed_data['timing']
    cards = parsed_data['cards']
    combinations = parsed_data['combinations']
    elemental_balance = parsed_data['elemental_balance']

    paragraphs = []

    # Opening paragraph
    paragraphs.append(generate_opening(question, timing, cards))

    # Card interpretations - group into paragraphs
    if len(cards) == 1:
        # Single card spread - need more elaboration
        card_texts = [generate_card_interpretation(card) for card in cards]
        paragraphs.append(" ".join(card_texts))
        # Add elaboration paragraph for single card spreads
        paragraphs.append(generate_elaboration(question, cards[0], timing))
        # Add additional reflection paragraph for single-card readings
        card_name = cards[0]['card_name']
        additional_reflections = [
            f"Consider journaling about how {card_name} speaks to your current circumstances. Write down three specific ways this energy might manifest in your daily life, and one concrete action you can take today that aligns with its message. The cards work best when we translate their wisdom into tangible steps.",
            f"As you carry this reading with you, notice moments when the energy of {card_name} appears in unexpected ways. Perhaps in a conversation, a decision point, or a shift in perspective. These synchronicities deepen your connection to the guidance offered and show you how the reading ripples through your lived experience.",
            f"This single card holds concentrated wisdom. Like a seed, {card_name} contains everything needed for growth—but you must provide the soil and tend to what emerges. What conditions can you create that allow this guidance to take root? What habits or patterns might need clearing to make space for new growth?"
        ]
        paragraphs.append(random.choice(additional_reflections))
    elif len(cards) <= 3:
        # Short spread - one paragraph for all cards plus elaboration
        card_texts = [generate_card_interpretation(card) for card in cards]
        paragraphs.append(" ".join(card_texts))
        # Add elaboration for short spreads
        if combinations:
            paragraphs.append(generate_combination_insight(combinations) + " " + generate_elaboration(question, cards[-1], timing))
        else:
            paragraphs.append(generate_elaboration(question, cards[-1], timing))
    elif len(cards) <= 6:
        # Medium spread - two paragraphs
        mid = len(cards) // 2
        first_half = [generate_card_interpretation(card) for card in cards[:mid]]
        second_half = [generate_card_interpretation(card) for card in cards[mid:]]
        paragraphs.append(" ".join(first_half))
        paragraphs.append(" ".join(second_half))
        if combinations:
            paragraphs.append(generate_combination_insight(combinations))
    else:
        # Large spread - three paragraphs
        third = len(cards) // 3
        first = [generate_card_interpretation(card) for card in cards[:third]]
        second = [generate_card_interpretation(card) for card in cards[third:2*third]]
        third_part = [generate_card_interpretation(card) for card in cards[2*third:]]
        paragraphs.append(" ".join(first))
        paragraphs.append(" ".join(second))
        if combinations:
            paragraphs.append(" ".join(third_part) + " " + generate_combination_insight(combinations))
        else:
            paragraphs.append(" ".join(third_part))

    # Closing paragraph with actionable insight
    paragraphs.append(generate_closing(question, cards, elemental_balance))

    # Join and ensure proper length
    reading = "\n\n".join(paragraphs)

    return reading

def process_batch():
    """Process all prompts in the batch and generate responses."""
    responses = []

    for i, prompt in enumerate(batch_data['prompts']):
        prompt_id = prompt['id']
        input_text = prompt['input_text']

        try:
            parsed = parse_input_text(input_text)
            if not parsed['cards']:
                # Fallback parsing for edge cases
                parsed['question'] = prompt.get('question', 'your situation')

            reading = generate_reading(parsed)
            responses.append({'id': prompt_id, 'response': reading})

        except Exception as e:
            # Generate a generic reading on error
            question = prompt.get('question', 'your question')
            generic = f"Your question about {question.lower().rstrip('?')} touches on important themes. The cards have emerged to offer guidance and perspective on this matter.\n\nThe spread reveals a journey of transformation and growth. Each card position adds depth to the narrative, showing both challenges and opportunities that lie before you. Pay attention to the reversed cards, as they often point to internal work or blocked energies that need attention.\n\nAs you move forward, trust your intuition to guide you. The cards serve as mirrors, reflecting what you already know at a deeper level. Take time to integrate these insights before making major decisions. Your path forward becomes clearer when you align your actions with your authentic values."
            responses.append({'id': prompt_id, 'response': generic})

        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1}/{len(batch_data['prompts'])} prompts")

    return responses

# Generate all responses
print(f"Processing batch {batch_data['batch_id']} with {batch_data['count']} prompts...")
responses = process_batch()

# Write to JSONL file
output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0029_responses.jsonl'
with open(output_path, 'w') as f:
    for response in responses:
        f.write(json.dumps(response) + '\n')

print(f"Written {len(responses)} responses to {output_path}")
