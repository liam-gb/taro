#!/usr/bin/env python3
"""Process batch_0020.json and generate tarot reading responses."""

import json
import re
import random
import hashlib

def parse_prompt(input_text):
    """Parse the input_text to extract spread details."""
    result = {
        'timing': '',
        'question': '',
        'cards': [],
        'elemental_balance': '',
        'dominant_element': '',
        'combinations': []
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        result['timing'] = timing_match.group(1).strip()

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()

    # Find the cards section - improved regex
    cards_section = re.search(r'The following cards were drawn:(.*?)(?=Card Combinations:|Elemental Balance:|Weave these)', input_text, re.DOTALL)
    if cards_section:
        cards_text = cards_section.group(1)

        # Parse each card entry more robustly
        card_pattern = r'(\d+)\.\s*([^:]+):\s*(.+?)\s*\((\w+)\)\s*\n\s*Keywords:\s*([^\n]+)\s*\n\s*Base meaning:\s*([^\n]+)\s*\n\s*Position context:\s*([^\n]+)'
        matches = re.findall(card_pattern, cards_text, re.DOTALL)

        for match in matches:
            card = {
                'number': match[0].strip(),
                'position': match[1].strip(),
                'name': match[2].strip(),
                'orientation': match[3].strip().lower(),
                'keywords': match[4].strip(),
                'base_meaning': match[5].strip(),
                'position_context': match[6].strip()
            }
            result['cards'].append(card)

    # Extract elemental balance
    elemental_match = re.search(r'Elemental Balance:\s*(\w+)', input_text)
    if elemental_match:
        result['elemental_balance'] = elemental_match.group(1).strip()

    dominant_match = re.search(r'Dominant:\s*(\w+)\s*energy', input_text)
    if dominant_match:
        result['dominant_element'] = dominant_match.group(1).strip()

    # Extract card combinations
    combo_section = re.search(r'Card Combinations:(.*?)(?:Elemental Balance:|Weave these|$)', input_text, re.DOTALL)
    if combo_section:
        combo_pattern = r'-\s*([^:]+):\s*([^\n]+)'
        combos = re.findall(combo_pattern, combo_section.group(1))
        result['combinations'] = [{'cards': c[0].strip(), 'meaning': c[1].strip()} for c in combos]

    return result

def get_seed(prompt_id):
    """Generate consistent seed from prompt ID."""
    return int(hashlib.md5(prompt_id.encode()).hexdigest()[:8], 16)

def rephrase_question(question):
    """Create a readable topic from the question."""
    q = question.strip().rstrip('?').lower()

    # Map common question patterns to topics
    patterns = [
        (r'^will\s+(i|my|the)\s+', 'whether '),
        (r'^should\s+i\s+', 'whether you should '),
        (r'^how\s+can\s+i\s+', 'how to '),
        (r'^how\s+do\s+i\s+', 'how to '),
        (r'^how\s+will\s+', 'how '),
        (r'^what\s+is\s+', ''),
        (r'^what\s+are\s+', ''),
        (r'^why\s+do\s+i\s+', 'why you '),
        (r'^why\s+does\s+', 'why '),
        (r'^when\s+will\s+', 'when '),
        (r'^where\s+should\s+', 'where '),
        (r'^is\s+it\s+', 'whether it is '),
        (r'^is\s+my\s+', 'your '),
        (r'^are\s+my\s+', 'your '),
        (r'^do\s+i\s+', 'whether you '),
        (r'^does\s+my\s+', 'whether your '),
        (r'^can\s+i\s+', 'whether you can '),
        (r'^am\s+i\s+', 'whether you are '),
        (r'^have\s+i\s+', 'whether you have '),
        (r'^which\s+', 'which '),
    ]

    for pattern, replacement in patterns:
        if re.match(pattern, q):
            q = re.sub(pattern, replacement, q)
            break

    # Clean up "my" -> "your" throughout
    q = re.sub(r'\bmy\b', 'your', q)
    q = re.sub(r'\bi\b', 'you', q)
    q = re.sub(r'\bi\'m\b', 'you are', q)

    return q if q else "your current situation"

def generate_reading(prompt_data):
    """Generate a tarot reading response based on parsed prompt data."""
    random.seed(get_seed(prompt_data['id']))

    parsed = parse_prompt(prompt_data['input_text'])
    question = parsed['question'] or prompt_data.get('question', '')
    cards = parsed['cards']
    timing = parsed['timing']
    elemental = parsed['dominant_element'] or parsed['elemental_balance']
    combinations = parsed['combinations']

    if not cards or len(cards) < 2:
        return generate_fallback_reading(question, prompt_data['id'])

    paragraphs = []

    # Opening paragraph
    opening = generate_opening(question, timing, elemental, cards)
    paragraphs.append(opening)

    # Card interpretation - narrative style
    if len(cards) <= 3:
        card_narrative = generate_three_card_narrative(cards, question)
    else:
        card_narrative = generate_extended_narrative(cards, question, combinations)

    paragraphs.extend(card_narrative)

    # Add reflection paragraph for depth
    reflection = generate_reflection(cards, question, elemental)
    paragraphs.append(reflection)

    # Synthesis and actionable insight
    closing = generate_closing(cards, question, elemental)
    paragraphs.append(closing)

    return '\n\n'.join(paragraphs)

def generate_opening(question, timing, elemental, cards):
    """Generate opening paragraph."""
    topic = rephrase_question(question)

    openings = [
        f"Your question about {topic} opens a meaningful dialogue with the cards.",
        f"As you seek guidance on {topic}, this spread reveals important insights.",
        f"The cards respond thoughtfully to your inquiry about {topic}.",
        f"Your question regarding {topic} has drawn forth a spread rich with meaning.",
        f"These cards gather to illuminate {topic}, offering both challenge and possibility."
    ]

    opening = random.choice(openings)

    # Add timing context
    if 'New Moon' in timing:
        opening += " The New Moon timing amplifies themes of fresh starts and intention-setting, making this fertile ground for planting new seeds. This darkness holds potential, inviting you to envision what you wish to create."
    elif 'Full Moon' in timing:
        opening += " Under the Full Moon's illumination, hidden truths come to light, and matters reach their natural culmination. What has been building now reveals itself fully."
    elif 'Waning Gibbous' in timing:
        opening += " The Waning Gibbous phase supports gratitude and sharing wisdom, a time for integrating lessons learned and preparing to release what no longer serves."
    elif 'Last Quarter' in timing:
        opening += " The Last Quarter moon supports release and forgiveness, helping you let go of old patterns that have run their course."
    elif 'Waning Crescent' in timing:
        opening += " The Waning Crescent phase invites rest and surrender, preparing you for the new cycle that approaches."
    elif 'Waxing Crescent' in timing:
        opening += " The Waxing Crescent brings energy of commitment and intention, supporting forward momentum."
    elif 'First Quarter' in timing:
        opening += " The First Quarter moon calls for decisive action and overcoming obstacles, a time to push through challenges."
    elif 'Waxing Gibbous' in timing:
        opening += " The Waxing Gibbous phase supports refinement and adjustment as you approach fulfillment of your goals."

    # Add elemental context
    element_contexts = {
        'Fire': " Fire energy dominates this reading, bringing themes of passion, will, creativity, and transformative action to the forefront. This is energy that moves, creates, and sometimes burns away what must go.",
        'Water': " Water's presence flows through this spread, emphasizing emotional depth, intuition, relationships, and the wisdom of feeling. This is energy that connects, nurtures, and reveals hidden currents.",
        'Air': " Air energy prevails here, highlighting matters of thought, communication, decision-making, and perspective. This is energy that clarifies, questions, and cuts through confusion.",
        'Earth': " Grounding Earth energy anchors this reading, pointing to practical concerns, material stability, physical well-being, and tangible outcomes. This is energy that builds, sustains, and manifests."
    }
    if elemental in element_contexts:
        opening += element_contexts[elemental]

    return opening

def generate_three_card_narrative(cards, question):
    """Generate flowing narrative for 3-card spreads."""
    paragraphs = []
    positions = [c['position'] for c in cards]

    if 'Past' in positions and 'Present' in positions and 'Future' in positions:
        paragraphs.append(generate_past_present_future(cards))
    elif 'Situation' in positions and 'Action' in positions and 'Outcome' in positions:
        paragraphs.append(generate_situation_action_outcome(cards))
    else:
        paragraphs.append(generate_generic_three_card(cards))

    return paragraphs

def generate_past_present_future(cards):
    """Generate narrative for past/present/future spread."""
    past = next((c for c in cards if c['position'] == 'Past'), None)
    present = next((c for c in cards if c['position'] == 'Present'), None)
    future = next((c for c in cards if c['position'] == 'Future'), None)

    narrative = ""

    if past:
        is_reversed = past['orientation'] == 'reversed'
        rev = "In its reversed position, this energy has been blocked or internalized: " if is_reversed else ""
        narrative += f"The {past['name']} in your past position reveals the foundation from which your current situation emerged. {rev}{past['position_context']} This history shapes how you approach what lies ahead, carrying both wisdom gained and perhaps some patterns now ready for transformation. The echoes of this energy continue to influence your present, whether you recognize them consciously or not. "

    if present:
        is_reversed = present['orientation'] == 'reversed'
        rev = "Appearing reversed, this energy manifests in a more internalized or challenging way: " if is_reversed else ""
        narrative += f"Moving into your present, the {present['name']} captures the essential quality of this moment. {rev}{present['position_context']} This is the ground you stand on now, the energy actively shaping your daily experience. Understanding this card helps you recognize both what serves you and what might need conscious adjustment. "

    if future:
        is_reversed = future['orientation'] == 'reversed'
        rev = "Its reversed appearance suggests this energy may arrive in unexpected ways or require deliberate effort to integrate: " if is_reversed else ""
        narrative += f"The {future['name']} illuminates the path ahead. {rev}{future['position_context']} This is not fixed destiny but rather the direction of current momentum, showing what naturally unfolds if present patterns continue. You have agency here; awareness of this trajectory empowers you to shape it consciously."

    return narrative

def generate_situation_action_outcome(cards):
    """Generate narrative for situation/action/outcome spread."""
    situation = next((c for c in cards if c['position'] == 'Situation'), None)
    action = next((c for c in cards if c['position'] == 'Action'), None)
    outcome = next((c for c in cards if c['position'] == 'Outcome'), None)

    narrative = ""

    if situation:
        is_reversed = situation['orientation'] == 'reversed'
        rev = "Reversed, this suggests the situation involves blocked or distorted expression of this energy: " if is_reversed else ""
        narrative += f"The {situation['name']} defines the heart of your current situation. {rev}{situation['position_context']} Understanding this core dynamic is essential before considering action. This card shows you not just what is happening, but the underlying energy pattern that shapes these circumstances. Take time to truly recognize this energy at work in your life. "

    if action:
        is_reversed = action['orientation'] == 'reversed'
        rev = "In reverse, this action may require a more internal or unconventional approach: " if is_reversed else ""
        narrative += f"The {action['name']} offers clear guidance on how to proceed. {rev}{action['position_context']} This is the medicine the moment calls for, the movement that will shift the energy. The cards are specific here about what is needed; the question is whether you are ready to move in this direction. Consider how this guidance resonates with your own inner knowing. "

    if outcome:
        is_reversed = outcome['orientation'] == 'reversed'
        rev = "Its reversed position suggests the outcome may manifest in subtle or unexpected ways: " if is_reversed else ""
        narrative += f"Following this path, the {outcome['name']} reveals what naturally unfolds. {rev}{outcome['position_context']} This outcome reflects the natural consequences of the suggested action, showing you not just what might happen but why it matters."

    return narrative

def generate_generic_three_card(cards):
    """Generate narrative for any three-card spread."""
    narrative = ""

    for i, card in enumerate(cards):
        is_reversed = card['orientation'] == 'reversed'
        rev = "Appearing reversed, this energy is blocked or internalized: " if is_reversed else ""
        position_phrase = f"in the {card['position']} position" if card['position'] else f"as the {['first', 'second', 'third'][i]} card"

        if i == 0:
            narrative += f"The {card['name']} {position_phrase} establishes the reading's foundation. {rev}{card['position_context']} This sets the stage for everything that follows, establishing the energetic context in which the other cards operate. "
        elif i == 1:
            narrative += f"Central to this spread, the {card['name']} {position_phrase} deepens our understanding. {rev}{card['position_context']} This middle position often holds the key to unlocking the reading's full meaning, bridging what was with what will be. "
        else:
            narrative += f"The {card['name']} {position_phrase} brings this spread toward resolution. {rev}{card['position_context']} As the final card in this sequence, it offers both conclusion and direction, pointing toward how these energies might resolve."

    return narrative

def generate_extended_narrative(cards, question, combinations):
    """Generate narrative for larger spreads."""
    paragraphs = []

    # Group by themes
    foundation = [c for c in cards if c['position'] in ['Past', 'Situation', 'Foundation', 'Root']]
    present_challenges = [c for c in cards if c['position'] in ['Present', 'Challenge', 'Obstacles', 'Crossing']]
    influences = [c for c in cards if c['position'] in ['Hidden Influences', 'External Influences', 'Above', 'Below']]
    guidance_outcome = [c for c in cards if c['position'] in ['Action', 'Advice', 'Future', 'Outcome', 'Hopes and Fears']]

    # Catch any ungrouped cards
    grouped = foundation + present_challenges + influences + guidance_outcome
    other = [c for c in cards if c not in grouped]

    # Foundation paragraph
    if foundation:
        para = "The foundational cards establish the ground from which everything else grows, revealing the roots of your current situation. "
        for card in foundation:
            is_rev = card['orientation'] == 'reversed'
            rev = "(reversed) " if is_rev else ""
            para += f"The {card['name']} {rev}in the {card['position']} position shows: {card['position_context']} "
        para += "Understanding these roots helps you see how past experiences and underlying patterns shape your present circumstances."
        paragraphs.append(para)

    # Present/Challenges paragraph
    if present_challenges or other:
        para = "Looking at the present dynamics and the challenges you face reveals what is most active in your life right now. "
        for card in (present_challenges + other):
            is_rev = card['orientation'] == 'reversed'
            rev = "(reversed) " if is_rev else ""
            context = card['position_context'].lower() if card['position_context'] else 'significant energy is at play'
            para += f"The {card['name']} {rev}as {card['position']} indicates that {context}. "
        para += "These energies require your attention and conscious engagement."
        paragraphs.append(para)

    # Influences paragraph
    if influences:
        para = "Important influences, both visible and hidden, shape this situation in ways you may not fully recognize. "
        for card in influences:
            is_rev = card['orientation'] == 'reversed'
            rev = "(reversed) " if is_rev else ""
            context = card['position_context'].lower() if card['position_context'] else 'subtle forces are at work'
            para += f"The {card['name']} {rev}in the {card['position']} position reveals that {context}. "
        para += "Awareness of these influences empowers you to work with them rather than being unconsciously affected."
        paragraphs.append(para)

    # Guidance and outcome paragraph
    if guidance_outcome:
        para = "The cards offering guidance and pointing toward potential outcomes speak with particular clarity. "
        for card in guidance_outcome:
            is_rev = card['orientation'] == 'reversed'
            rev = "(reversed) " if is_rev else ""
            context = card['position_context'].lower() if card['position_context'] else 'important developments lie ahead'
            para += f"The {card['name']} {rev}in the {card['position']} position suggests that {context}. "
        para += "These cards offer both direction and destination, though you remain free to shape how you travel."
        paragraphs.append(para)

    # Card combinations if present
    if combinations:
        combo_para = "The interplay between certain cards creates additional layers of meaning that deepen this reading. "
        for combo in combinations[:3]:
            combo_para += f"{combo['cards']} together indicate {combo['meaning'].lower()}. "
        combo_para += "These combinations reveal connections that single cards cannot express on their own."
        paragraphs.append(combo_para)

    return paragraphs if paragraphs else [generate_generic_three_card(cards)]

def generate_reflection(cards, question, elemental):
    """Generate a reflection paragraph for additional depth."""
    topic = rephrase_question(question)

    # Count reversed cards
    reversed_count = sum(1 for c in cards if c['orientation'] == 'reversed')
    reversed_ratio = reversed_count / len(cards) if cards else 0

    # Identify card types
    major_arcana = ['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor',
                   'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit',
                   'Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death', 'Temperance',
                   'The Devil', 'The Tower', 'The Star', 'The Moon', 'The Sun', 'Judgement', 'The World']

    majors_present = [c for c in cards if c['name'] in major_arcana]
    cups = [c for c in cards if 'Cups' in c['name'] or 'Cup' in c['name']]
    swords = [c for c in cards if 'Swords' in c['name'] or 'Sword' in c['name']]
    wands = [c for c in cards if 'Wands' in c['name'] or 'Wand' in c['name']]
    pentacles = [c for c in cards if 'Pentacles' in c['name'] or 'Pentacle' in c['name']]

    reflections = []

    if reversed_ratio > 0.5:
        reflections.append(f"The prevalence of reversed cards in this reading is significant. This suggests much of the relevant energy is internalized, blocked, or working beneath the surface. There may be patterns or beliefs operating outside your conscious awareness that influence {topic}. This is an invitation to honest self-examination, not self-criticism, but genuine curiosity about what might be asking for attention.")
    elif reversed_ratio > 0:
        reflections.append(f"The reversed cards in this spread point to areas where energy may be stuck or manifesting in unexpected ways. These are not negative omens but rather invitations to look deeper, to examine where resistance or unconscious patterns might be influencing {topic}. Working consciously with these energies can transform apparent obstacles into doorways.")

    if len(majors_present) >= 2:
        major_names = [m['name'] for m in majors_present]
        reflections.append(f"The strong presence of Major Arcana cards ({', '.join(major_names[:3])}) elevates this reading beyond everyday concerns. These cards speak to soul-level lessons, significant life transitions, and archetypal forces at work. This is not a small matter; the universe is asking you to pay attention to larger patterns and deeper truths about {topic}.")
    elif len(majors_present) == 1:
        reflections.append(f"The appearance of {majors_present[0]['name']} brings Major Arcana energy into this reading, suggesting that {topic} connects to larger life themes and deeper spiritual lessons. This card acts as a beacon, drawing attention to what matters most.")

    if len(cups) >= 2:
        reflections.append(f"The abundance of Cups energy in this spread emphasizes the emotional dimension of {topic}. Feelings, relationships, intuition, and matters of the heart are central here. Honor your emotional responses as valid information; they are telling you something important.")

    if len(swords) >= 2:
        reflections.append(f"Multiple Swords cards appear, highlighting the mental and communicative aspects of {topic}. Thoughts, beliefs, decisions, and how you frame situations are all in play. Consider whether your thinking patterns serve you, and whether there are conversations that need to happen.")

    if not reflections:
        reflections.append(f"As you sit with this reading, allow the images and energies of the cards to work on you beyond intellectual analysis. Sometimes the most valuable insights about {topic} come not from thinking harder but from creating space for intuitive understanding to emerge. Notice what resonates, what creates resistance, and what surprises you.")

    return random.choice(reflections)

def generate_closing(cards, question, elemental):
    """Generate closing paragraph with actionable insight."""
    reversed_cards = [c for c in cards if c['orientation'] == 'reversed']

    major_arcana = ['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor',
                   'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit',
                   'Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death', 'Temperance',
                   'The Devil', 'The Tower', 'The Star', 'The Moon', 'The Sun', 'Judgement', 'The World']

    has_major = any(c['name'] in major_arcana for c in cards)

    # Find advice or action card, or use last card
    advice_card = next((c for c in cards if c['position'] in ['Advice', 'Action']), None)
    outcome_card = next((c for c in cards if c['position'] in ['Outcome', 'Future']), None)
    key_card = advice_card or outcome_card or cards[-1]

    # Generate actionable insight based on keywords
    keywords = key_card.get('keywords', '').split(',')
    primary_keyword = keywords[0].strip() if keywords else 'awareness'

    action_templates = [
        f"The most potent action you can take is to consciously cultivate {primary_keyword} in your daily choices. This might look like pausing before major decisions to ask whether your choice aligns with this energy. Start small, perhaps dedicating just five minutes today to embodying this quality intentionally.",
        f"Move forward by embracing {primary_keyword} as a guiding principle. Practically, this means creating space in your life where this quality can flourish, whether through specific practices, meaningful conversations, or conscious changes in routine. Ask yourself: where can I invite more of this energy today?",
        f"Your path forward becomes clearer when you center {primary_keyword}. Consider one concrete step you could take this week that embodies this energy, no matter how small. The cards suggest that consistent alignment with this quality will shift your circumstances more effectively than grand gestures.",
        f"Integrate {primary_keyword} into your approach to this situation. Sometimes the smallest shift in perspective or behavior creates the largest ripple of change. Notice where this energy is already present in your life and nurture it; notice where it is absent and explore why.",
        f"Let {primary_keyword} guide your next steps. This doesn't require dramatic action; it asks for consistent, conscious alignment with this energy in your everyday choices. Begin by simply noticing when you embody this quality and when you resist it."
    ]

    closing = random.choice(action_templates)

    # Add reversal insight if relevant
    if reversed_cards:
        rev_card = reversed_cards[0]
        closing += f" Pay particular attention to the reversed {rev_card['name']}, which signals an area where energy may be blocked, internalized, or manifesting in unexpected ways. This asks for honest self-examination about patterns that might benefit from conscious attention and compassionate transformation."

    # Add major arcana significance
    if has_major:
        closing += " The presence of Major Arcana energy indicates this is a significant moment in your larger journey, where soul-level lessons are active and meaningful choices are being made."

    # Final words
    closers = [
        " Trust the wisdom you already carry within you; the cards simply mirror what you already know at some level.",
        " Remember that you possess the resources needed for this journey, even if they are not yet fully visible to you.",
        " Hold these insights lightly, allowing them to inform rather than constrain your choices as circumstances continue to unfold.",
        " The cards illuminate possibilities and patterns; you remain the author of your story and the maker of your choices.",
        " Let this reading be a touchstone you return to as situations develop, knowing that the meaning may deepen with time."
    ]
    closing += random.choice(closers)

    return closing

def generate_fallback_reading(question, prompt_id):
    """Generate robust reading when parsing fails."""
    random.seed(get_seed(prompt_id))
    topic = rephrase_question(question)

    paragraphs = [
        f"Your question about {topic} opens a meaningful dialogue with the universe. The energy surrounding this inquiry suggests you are at a threshold, a place where old patterns meet new possibilities and where the choices you make carry real weight. Something is shifting within you, and your awareness of this shift is itself the beginning of transformation.",

        f"What emerges is a call for balance between action and patience. There are aspects of {topic} that require your active engagement, your courage, and your willingness to take concrete steps. Yet there are also dimensions that ask you to trust the unfolding process, to allow space for things to develop in their own timing. Learning to distinguish between these, to know when to push and when to yield, is part of your current work.",

        f"The path forward involves honest self-examination. What beliefs, assumptions, or patterns are you carrying about {topic}? Some undoubtedly serve you well, reflecting hard-won wisdom. Others may have outlived their usefulness and now create friction rather than flow. This is not about harsh self-judgment but rather about compassionate clarity, seeing yourself and your situation accurately so you can respond wisely.",

        f"Consider where you might be pushing against closed doors while neglecting open ones. Sometimes our energy goes to fighting battles that are already lost or won, rather than engaging with what is actually available now. What would it mean to focus your attention on what is possible rather than what feels stuck?",

        f"Your actionable step is to create dedicated time for reflection on {topic}, approaching it with curiosity rather than anxiety. Write, walk, meditate, or simply sit with the question without demanding immediate answers. Sometimes the most powerful thing you can do is remain present with uncertainty while trusting that clarity will emerge in its own time. Let this not be passive waiting but active listening, attuned to the subtle signals that will guide your next steps. Trust your capacity to navigate what lies ahead."
    ]

    return '\n\n'.join(paragraphs)

def main():
    # Load batch file
    with open('/home/user/taro/training/data/batches_expanded/batch_0020.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    print(f"Processing {len(prompts)} prompts...")

    # Generate responses
    responses = []
    for i, prompt in enumerate(prompts):
        response = generate_reading(prompt)
        responses.append({
            'id': prompt['id'],
            'response': response
        })

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(prompts)} prompts")

    # Write to JSONL
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0020_responses.jsonl'
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"Written {len(responses)} responses to {output_path}")

    # Quality check
    word_counts = [len(r['response'].split()) for r in responses]
    print(f"\nWord count stats:")
    print(f"  Min: {min(word_counts)}, Max: {max(word_counts)}, Avg: {sum(word_counts)/len(word_counts):.0f}")
    print(f"  Under 200 words: {sum(1 for wc in word_counts if wc < 200)}")
    print(f"  200-400 words: {sum(1 for wc in word_counts if 200 <= wc <= 400)}")
    print(f"  Over 400 words: {sum(1 for wc in word_counts if wc > 400)}")

if __name__ == '__main__':
    main()
