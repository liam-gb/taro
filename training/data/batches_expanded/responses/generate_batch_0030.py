#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0030.json - Final version"""

import json
import re
import random
from pathlib import Path

random.seed(42)

def parse_input_text(input_text):
    """Parse the input_text to extract timing, question, cards, and elemental balance."""
    result = {
        'timing': '',
        'timing_meaning': '',
        'question': '',
        'cards': [],
        'elemental_balance': '',
        'elemental_flow': '',
        'dominant_element': ''
    }

    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1)
        result['timing'] = timing_full.split('—')[0].strip() if '—' in timing_full else timing_full
        result['timing_meaning'] = timing_full.split('—')[1].strip() if '—' in timing_full else ''

    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1)

    card_pattern = re.compile(
        r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+(?:\n(?!\d+\.)(?!\n)[^\n]+)*)',
        re.MULTILINE
    )

    for match in card_pattern.finditer(input_text):
        card = {
            'number': int(match.group(1)),
            'position': match.group(2).strip(),
            'name': match.group(3).strip(),
            'keywords': [k.strip() for k in match.group(4).split(',')],
            'base_meaning': match.group(5).strip(),
            'position_context': match.group(6).strip(),
            'reversed': 'reversed' in match.group(3).lower()
        }
        result['cards'].append(card)

    elem_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elem_match:
        result['elemental_balance'] = elem_match.group(1).strip()

    dom_match = re.search(r'Dominant:\s*([^\n]+)', input_text)
    if dom_match:
        result['dominant_element'] = dom_match.group(1).strip()

    flow_match = re.search(r'(Air|Fire|Water|Earth)\s*→\s*(Air|Fire|Water|Earth)\s*→\s*(Air|Fire|Water|Earth)', input_text)
    if flow_match:
        result['elemental_flow'] = f"{flow_match.group(1)} → {flow_match.group(2)} → {flow_match.group(3)}"

    return result

def clean_card_name(name):
    """Remove orientation markers from card name."""
    return name.replace('(upright)', '').replace('(reversed)', '').strip()

def get_card_archetype_meaning(card_name):
    """Get additional meaning based on card archetype."""
    name_lower = card_name.lower()

    # Court cards
    if 'king' in name_lower:
        return "As a King, this card represents mastery, authority, and the mature expression of its suit's energy."
    elif 'queen' in name_lower:
        return "The Queen brings nurturing wisdom, emotional intelligence, and creative mastery to this position."
    elif 'knight' in name_lower:
        return "Knights embody action, movement, and the pursuit of their suit's goals with passionate dedication."
    elif 'page' in name_lower:
        return "Pages represent new beginnings, messages, and the youthful exploration of their element's qualities."

    # Number meanings
    numbers = {
        'ace': "Aces are pure potential, the seed of new beginnings waiting to unfold.",
        'two': "Twos speak to balance, partnership, and the first steps of a journey.",
        'three': "Threes bring growth, creativity, and the initial fruits of effort.",
        'four': "Fours represent stability, foundation, and a pause for consolidation.",
        'five': "Fives introduce challenge, conflict, and necessary disruption for growth.",
        'six': "Sixes bring harmony, communication, and movement toward resolution.",
        'seven': "Sevens call for reflection, assessment, and deeper understanding.",
        'eight': "Eights represent movement, change, and the power of directed will.",
        'nine': "Nines signify near-completion, wisdom gained, and preparation for culmination.",
        'ten': "Tens mark completion, the full cycle, and transition to new beginnings."
    }
    for num, meaning in numbers.items():
        if num in name_lower:
            return meaning

    # Major Arcana specifics
    majors = {
        'fool': "The Fool's presence invites trust in the journey, embracing beginner's mind and spontaneous faith.",
        'magician': "The Magician reminds you that you have all the tools needed; now is the time for focused will.",
        'high priestess': "The High Priestess calls you inward, to trust intuition over external answers.",
        'empress': "The Empress embodies creative abundance, nurturing growth, and connection to natural cycles.",
        'emperor': "The Emperor brings structure, authority, and the need for clear boundaries and leadership.",
        'hierophant': "The Hierophant speaks to tradition, learning, and seeking wisdom from established paths.",
        'lovers': "The Lovers illuminate choice, alignment of values, and the harmony of opposites.",
        'chariot': "The Chariot demands disciplined will, forward motion, and victory through determination.",
        'strength': "Strength comes through patience, compassion, and gentle mastery rather than force.",
        'hermit': "The Hermit lights the path of solitary wisdom, inner guidance, and thoughtful retreat.",
        'wheel': "The Wheel turns, reminding you that change is constant and fortune is cyclical.",
        'justice': "Justice calls for truth, accountability, and the fair consequences of actions taken.",
        'hanged': "The Hanged Man invites surrender, new perspective, and wisdom through pause.",
        'death': "Death signals profound transformation, endings that enable beginnings, and necessary release.",
        'temperance': "Temperance brings balance, patience, and the alchemy of integrating opposites.",
        'devil': "The Devil illuminates what binds you, whether chains of habit, fear, or false limitation.",
        'tower': "The Tower's lightning strikes down false structures, creating space for authentic rebuilding.",
        'star': "The Star offers hope, healing, and renewed faith after difficulty.",
        'moon': "The Moon illuminates the unconscious, illusions, and the path through uncertainty.",
        'sun': "The Sun brings clarity, vitality, and the joy of authentic self-expression.",
        'judgement': "Judgement calls for awakening, honest self-evaluation, and answering your higher calling.",
        'world': "The World celebrates completion, integration, and the achievement of a significant cycle."
    }
    for major, meaning in majors.items():
        if major in name_lower:
            return meaning

    return ""

def get_reversal_expansion(card):
    """Get expanded meaning for reversed cards."""
    expansions = [
        "This reversal suggests the energy is either blocked, internalized, or expressing in an unexpected way.",
        "When reversed, consider whether this energy is being resisted or needs to be approached differently.",
        "The inverted position hints at delays, internal processing, or a need to address something before moving forward.",
        "This reversal may indicate that the lesson here needs more integration before its gifts fully manifest.",
        "Reversed energy often points to where we resist, where growth is happening internally before becoming visible."
    ]
    return random.choice(expansions)

def generate_reading(parsed_data):
    """Generate a complete tarot reading of 200-400 words."""
    question = parsed_data['question']
    cards = parsed_data['cards']
    timing = parsed_data['timing']
    timing_meaning = parsed_data['timing_meaning']
    elemental_balance = parsed_data['elemental_balance']
    dominant_element = parsed_data['dominant_element']

    if not cards:
        return "No cards were drawn for this reading."

    paragraphs = []
    num_cards = len(cards)
    has_reversals = any(c['reversed'] for c in cards)

    # === PARAGRAPH 1: Opening and First Card ===
    opening_templates = [
        f"Your question, \"{question}\", arrives during a time of {timing_meaning.lower() if timing_meaning else 'significant transition'}. The cards have gathered to illuminate your path forward, offering both clarity and depth.",
        f"In asking \"{question}\", you invite the cards to speak to something meaningful in your life. This spread offers a layered response worth careful consideration.",
        f"The inquiry about {question.lower().rstrip('?')} resonates through this spread. Each card adds dimension to the answer you seek, building toward genuine insight.",
        f"Your question touches on {question.lower().rstrip('?')}, and the cards respond with a narrative that deserves thoughtful attention. Let us explore what emerges."
    ]

    para1 = random.choice(opening_templates) + " "

    first_card = cards[0]
    fc_name = clean_card_name(first_card['name'])
    fc_context = first_card['position_context']
    fc_archetype = get_card_archetype_meaning(fc_name)

    if first_card['reversed']:
        para1 += f"Beginning with {fc_name} reversed in the {first_card['position'].lower()} position, we encounter a nuanced foundation. {fc_context} {get_reversal_expansion(first_card)}"
    else:
        para1 += f"The {fc_name} in the {first_card['position'].lower()} position establishes the reading's foundation. {fc_context}"

    if fc_archetype and len(para1.split()) < 120:
        para1 += f" {fc_archetype}"

    paragraphs.append(para1)

    # === PARAGRAPH 2: Middle Cards Development ===
    if num_cards >= 2:
        para2 = ""
        middle_cards = cards[1:-1] if num_cards > 2 else [cards[1]]

        for i, card in enumerate(middle_cards[:3]):
            c_name = clean_card_name(card['name'])
            c_context = card['position_context']
            c_pos = card['position'].lower()
            c_archetype = get_card_archetype_meaning(c_name)

            if i == 0:
                if card['reversed']:
                    para2 += f"Building on this foundation, {c_name} appears reversed in the {c_pos} position. {c_context} {get_reversal_expansion(card)} "
                else:
                    para2 += f"The reading develops as {c_name} takes the {c_pos} position. {c_context} "
            else:
                if card['reversed']:
                    para2 += f"Adding further dimension, the reversed {c_name} at {c_pos} suggests {c_context.lower() if c_context[0].isupper() else c_context} "
                else:
                    para2 += f"The {c_name} in the {c_pos} position shows that {c_context.lower() if c_context[0].isupper() else c_context} "

            if c_archetype and i == 0 and len(para2.split()) < 80:
                para2 += c_archetype + " "

        # Thematic connection
        question_lower = question.lower()
        theme_connectors = {
            'relationship': "These cards together paint a picture of the relational dynamics at play, revealing both challenge and possibility.",
            'love': "The emotional currents flowing through these cards speak directly to matters of the heart you are navigating.",
            'career': "The professional themes emerging here invite careful consideration of your work trajectory and aspirations.",
            'work': "What unfolds professionally depends on how you engage with the energies these cards illuminate.",
            'money': "The material and financial dimensions of your question find expression in this unfolding pattern.",
            'decision': "The choice before you gains clarity through understanding how these energies interact and inform one another.",
            'why': "The underlying patterns these cards reveal offer insight into the roots of what you are experiencing.",
            'fear': "What you fear and what actually serves you become clearer as these card meanings interweave.",
            'stuck': "Movement becomes possible once you understand what these cards are illuminating about your current position."
        }

        connector_added = False
        for key, connector in theme_connectors.items():
            if key in question_lower:
                para2 += connector
                connector_added = True
                break

        if not connector_added:
            para2 += "Together, these cards weave a coherent message that addresses the heart of your inquiry."

        paragraphs.append(para2)

    # === PARAGRAPH 3: Final Card and Synthesis ===
    if num_cards >= 2:
        last_card = cards[-1]
        lc_name = clean_card_name(last_card['name'])
        lc_context = last_card['position_context']
        lc_pos = last_card['position'].lower()
        lc_archetype = get_card_archetype_meaning(lc_name)

        if last_card['reversed']:
            para3 = f"The reading reaches its culmination with {lc_name} reversed in the {lc_pos} position. {lc_context} {get_reversal_expansion(last_card)} "
        else:
            para3 = f"At the {lc_pos}, {lc_name} brings the reading toward resolution. {lc_context} "

        if lc_archetype:
            para3 += lc_archetype + " "

        # Elemental synthesis
        if dominant_element:
            elem_meanings = {
                'Fire': "The dominant Fire energy throughout emphasizes transformation, passion, and the courage to act on your truth. This elemental signature calls for boldness tempered by awareness.",
                'Water': "The prevailing Water energy speaks to emotional depths, intuitive wisdom, and the importance of honoring your feelings as valid guidance. Trust what you sense beneath the surface.",
                'Earth': "The grounding Earth energy anchors this reading in practical reality. Material concerns, tangible steps, and patient building will serve you well here.",
                'Air': "The strong Air presence calls for clear thinking and honest communication. Intellectual clarity and truthful dialogue will be your greatest tools moving forward."
            }
            for elem, meaning in elem_meanings.items():
                if elem.lower() in dominant_element.lower():
                    para3 += meaning
                    break
        elif elemental_balance and 'balanced' in elemental_balance.lower():
            para3 += "The balanced elemental energies in this spread suggest you have access to varied resources and perspectives. No single approach dominates; integration is key."
        else:
            # Card combination insight
            card_names = [clean_card_name(c['name']) for c in cards[:3]]
            if len(card_names) >= 2:
                para3 += f"The interplay between {card_names[0]} and {card_names[-1]} creates a dynamic tension that holds the key to understanding your situation more fully."

        paragraphs.append(para3)

    # === PARAGRAPH 4: Actionable Guidance ===
    closing_intros = [
        "Moving forward with this insight, consider how you might ",
        "The practical wisdom emerging from this spread invites you to ",
        "To work constructively with these energies, ",
        "As you integrate this reading, the cards suggest you ",
        "The path forward becomes clearer when you "
    ]

    question_lower = question.lower()

    # Tailored actionable advice
    if any(word in question_lower for word in ['fear', 'afraid', 'scared', 'anxiety', 'worry', 'nervous']):
        actions = [
            "identify one small, concrete action you can take today despite the fear. Courage is not the absence of fear but the willingness to move forward alongside it. Each small step builds evidence that you can handle what comes. The cards remind you that paralysis serves only the fear itself, not your wellbeing or growth.",
            "write down your specific concerns, then honestly assess what portion you can actually influence. Channel your energy into what you can affect and practice releasing what lies beyond your control. This discernment between controllable and uncontrollable factors is itself a form of power the cards are inviting you to claim."
        ]
    elif any(word in question_lower for word in ['relationship', 'partner', 'love', 'dating', 'marriage']):
        actions = [
            "initiate an honest conversation about what you truly need. Vulnerability opens doors that protection keeps permanently closed. Consider what you have been avoiding saying, and find the courage to speak it with compassion. The cards suggest that authenticity, though risky, is the path to genuine connection.",
            "examine the patterns you bring to relationships from earlier experiences. Not to blame yourself, but to understand with clarity what you are working with. Awareness of these patterns is the first step toward choosing differently. The cards encourage conscious participation in your relational life rather than unconscious repetition."
        ]
    elif any(word in question_lower for word in ['career', 'job', 'work', 'promotion', 'boss', 'professional']):
        actions = [
            "articulate clearly what professional fulfillment actually means to you, beyond titles, salary, and external validation. What work makes you feel alive and useful? This clarity becomes your compass when navigating complex professional decisions. The cards suggest that reconnecting with intrinsic motivation will serve you better than chasing external markers.",
            "identify one skill gap or growth area and create a specific, time-bound plan to address it. Development happens through intentional practice, not wishful thinking. The cards point toward taking concrete steps toward the professional self you wish to become, starting now rather than waiting for perfect conditions."
        ]
    elif any(word in question_lower for word in ['money', 'financial', 'debt', 'income', 'abundance', 'wealth']):
        actions = [
            "examine your beliefs about money, worthiness, and abundance. Often our financial patterns reflect deeper stories we tell ourselves about what we deserve or what is possible. The cards invite honest exploration of these underlying narratives, as shifting them can create space for different material outcomes.",
            "create one new habit that honors your financial wellbeing, however small. Consistent small actions compound over time. The cards suggest that your relationship with money will shift as you demonstrate to yourself, through action, that you are capable of making choices aligned with your true interests."
        ]
    elif any(word in question_lower for word in ['decision', 'choice', 'should i', 'which', 'whether']):
        actions = [
            "list the values each option honors and which it compromises. When logic alone cannot guide you, let your deepest values be the tiebreaker. Imagine yourself one year after each choice and notice which future self feels more aligned with who you want to become. The cards suggest the answer lies in what you most want to cultivate in yourself.",
            "pay attention to your body's response to each possibility. Physical wisdom often knows before the conscious mind catches up. Notice where you feel expansion or contraction, ease or resistance. The cards invite you to trust this embodied knowing alongside your mental analysis as you move toward decision."
        ]
    elif any(word in question_lower for word in ['why', 'reason', 'understand', 'meaning']):
        actions = [
            "spend time journaling about when this pattern appears in your life and what seems to trigger it. Awareness is the first teacher, and understanding the conditions that activate certain responses gives you more choice about how to engage. The cards suggest that the insight you seek comes through patient, honest self-observation.",
            "consider what this behavior or feeling might be protecting you from. Often what seems problematic serves some function, even if that function no longer matches your current needs. Understanding the purpose behind the pattern is the first step toward releasing or transforming it. The cards point toward compassionate investigation rather than self-judgment."
        ]
    elif any(word in question_lower for word in ['stuck', 'blocked', 'unable', "can't", 'struggling']):
        actions = [
            "take one tiny action in the direction you want to go, no matter how seemingly insignificant. Movement creates momentum, and the stuck place often holds less power than it seems once you begin to move. The cards suggest that perfectionism about how to proceed may be part of what keeps you frozen. Imperfect action beats perfect inaction.",
            "examine honestly what secondary benefit the stuck place might provide. Sometimes we stay because staying serves us in some way we have not fully acknowledged, whether safety, familiarity, or avoidance of risk. The cards invite this honest inventory as the gateway to genuine movement forward."
        ]
    elif any(word in question_lower for word in ['standards', 'settling', 'deserve', 'worth']):
        actions = [
            "distinguish between standards that protect your genuine needs and standards that might be masks for fear or impossible perfectionism. The cards suggest that wisdom lies in knowing the difference, honoring non-negotiable values while remaining open to the imperfect beauty of real people and real situations.",
            "reflect on where your standards come from and whether they truly serve your current self. Sometimes we inherit expectations that no longer fit. The cards invite reassessment not to lower your bar, but to ensure you are reaching toward what you actually want rather than what you think you should want."
        ]
    else:
        actions = [
            "take one concrete step this week that aligns with the guidance offered here, however modest it may seem. Small, intentional actions accumulate into meaningful change. The cards have illuminated a path; walking it is your responsibility and your power. Notice what shifts as you begin to move.",
            "return to this reading in a week and observe what has shifted in your perception or circumstances. Tarot often plants seeds that bloom gradually, and meanings deepen as you live into them. Keep these card images in mind as you navigate the coming days, allowing their wisdom to inform your choices."
        ]

    para4 = random.choice(closing_intros) + random.choice(actions)
    para4 += " The cards have spoken; the next step belongs to you."

    paragraphs.append(para4)

    return "\n\n".join(paragraphs)

def main():
    input_path = Path("/home/user/taro/training/data/batches_expanded/batch_0030.json")
    output_path = Path("/home/user/taro/training/data/batches_expanded/responses/batch_0030_responses.jsonl")

    with open(input_path, 'r') as f:
        data = json.load(f)

    prompts = data['prompts']
    print(f"Processing {len(prompts)} prompts...")

    responses = []
    for i, prompt in enumerate(prompts):
        parsed = parse_input_text(prompt['input_text'])

        if not parsed['question']:
            parsed['question'] = prompt.get('question', 'your situation')

        reading = generate_reading(parsed)

        responses.append({
            'id': prompt['id'],
            'response': reading
        })

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(prompts)}")

    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"Written {len(responses)} responses to {output_path}")

    # Statistics
    word_counts = []
    for resp in responses:
        words = len(resp['response'].split())
        word_counts.append(words)

    in_range = sum(1 for w in word_counts if 200 <= w <= 400)
    under_200 = sum(1 for w in word_counts if w < 200)
    over_400 = sum(1 for w in word_counts if w > 400)

    print(f"Word count stats: min={min(word_counts)}, max={max(word_counts)}, avg={sum(word_counts)/len(word_counts):.1f}")
    print(f"Distribution: <200: {under_200}, 200-400: {in_range}, >400: {over_400}")
    print(f"In target range: {100*in_range/len(word_counts):.1f}%")

if __name__ == "__main__":
    main()
