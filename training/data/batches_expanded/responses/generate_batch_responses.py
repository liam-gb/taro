#!/usr/bin/env python3
"""Generate tarot reading responses for training data - enhanced version."""

import json
import re
import random
import hashlib

def parse_input_text(input_text):
    """Parse the input_text to extract cards, positions, question, and timing."""
    result = {
        "timing": None,
        "timing_meaning": None,
        "question": None,
        "cards": [],
        "elemental_balance": None,
        "elemental_flow": None
    }

    # Extract timing with meaning
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1).strip()
        result["timing"] = timing_full
        if '—' in timing_full:
            parts = timing_full.split('—')
            result["timing_meaning"] = parts[1].strip() if len(parts) > 1 else None

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result["question"] = question_match.group(1).strip()

    # Extract cards using a more robust pattern
    # Pattern to match: "1. Position Name: Card Name (upright/reversed)"
    # Position names can include apostrophes, slashes, and spaces
    card_pattern = r'(\d+)\.\s+([^:]+):\s+(.+?)\s*\((upright|reversed)\)\s*\n\s*Keywords:\s*([^\n]+)\s*\n\s*Base meaning:\s*([^\n]+)\s*\n\s*Position context:\s*([^\n]+(?:\n(?!\d+\.|Elemental)[^\n]*)*)'

    matches = re.findall(card_pattern, input_text, re.MULTILINE)

    for match in matches:
        num, position, card_name, orientation, keywords, base_meaning, position_context = match
        result["cards"].append({
            "number": int(num),
            "position": position.strip(),
            "card_name": card_name.strip(),
            "orientation": orientation.strip(),
            "keywords": keywords.strip(),
            "base_meaning": base_meaning.strip(),
            "position_context": position_context.strip()
        })

    # Extract elemental balance
    elemental_match = re.search(r'Elemental Balance:\s*(\w+)', input_text)
    if elemental_match:
        result["elemental_balance"] = elemental_match.group(1).strip()

    flow_match = re.search(r'(\w+)\s*→\s*(\w+)\s*→\s*(\w+)', input_text)
    if flow_match:
        result["elemental_flow"] = [flow_match.group(1), flow_match.group(2), flow_match.group(3)]

    return result


def seed_random(prompt_id, question):
    """Seed random based on prompt ID for reproducibility with variety."""
    seed_str = prompt_id + question
    seed_val = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    random.seed(seed_val)


def get_question_theme(question):
    """Identify the theme of the question for tailored responses."""
    q_lower = question.lower()

    if any(w in q_lower for w in ['love', 'relationship', 'partner', 'marriage', 'divorce', 'dating', 'romance', 'heart']):
        return 'relationships'
    elif any(w in q_lower for w in ['career', 'job', 'work', 'business', 'profession', 'money', 'financial', 'income']):
        return 'career'
    elif any(w in q_lower for w in ['health', 'healing', 'body', 'illness', 'wellness', 'mental', 'energy']):
        return 'health'
    elif any(w in q_lower for w in ['spiritual', 'purpose', 'meaning', 'soul', 'growth', 'path', 'journey']):
        return 'spiritual'
    elif any(w in q_lower for w in ['family', 'children', 'parent', 'mother', 'father', 'sibling', 'child']):
        return 'family'
    elif any(w in q_lower for w in ['decision', 'choice', 'should i', 'what if', 'whether']):
        return 'decision'
    elif any(w in q_lower for w in ['fear', 'anxiety', 'worry', 'doubt', 'afraid', 'feel', 'feeling', 'fraud', 'imposter']):
        return 'emotional'
    else:
        return 'general'


def generate_opening(question, timing, timing_meaning, cards, theme):
    """Generate the opening paragraph."""
    openings = [
        f"Your inquiry \"{question}\" opens a window into the deeper currents shaping your life right now.",
        f"The question you bring today, \"{question}\" resonates with profound significance.",
        f"In asking \"{question}\" you invite the cards to illuminate what lies beneath the surface.",
        f"Your soul seeks clarity on \"{question}\" and the tarot responds with wisdom.",
        f"The question \"{question}\" speaks to a journey that has been unfolding for some time."
    ]

    opening = random.choice(openings)

    if timing_meaning:
        timing_additions = [
            f" This reading arrives during a time of {timing_meaning.lower()}, amplifying the resonance of what the cards reveal.",
            f" The current lunar energy of {timing_meaning.lower()} lends particular power to this spread.",
            f" With the moon bringing {timing_meaning.lower()}, the timing of this reading feels especially significant."
        ]
        opening += random.choice(timing_additions)

    # Add context about the spread
    if len(cards) == 1:
        spread_context = [
            " The single card drawn speaks directly to the heart of your question.",
            " This focused one-card reading offers concentrated wisdom for your situation.",
            " Through this single card, a clear message emerges for your contemplation."
        ]
    else:
        spread_context = [
            f" The {len(cards)}-card spread drawn for you today weaves a narrative that speaks to multiple dimensions of your question.",
            f" Through these {len(cards)} cards, a story emerges that illuminates your path.",
            f" Let us explore what the {len(cards)} cards laid before you have to say."
        ]
    opening += random.choice(spread_context)

    return opening


def generate_card_paragraph(card, prev_card=None, next_card=None, question_theme='general', card_count=3):
    """Generate a detailed paragraph for a single card."""
    position = card["position"]
    name = card["card_name"]
    orientation = card["orientation"]
    keywords = card["keywords"]
    base_meaning = card["base_meaning"]
    pos_context = card["position_context"]
    is_reversed = orientation == "reversed"

    para = ""

    # Position-specific transitions - expanded to handle all position types
    position_transitions = {
        "Past": [
            f"The {name} in your Past position",
            f"Looking to what has shaped your journey, {name} appears",
            f"Your foundation rests upon {name}",
            f"The roots of your current situation trace back to {name}"
        ],
        "Present": [
            f"In the Present position, {name}",
            f"The energy surrounding you right now manifests as {name}",
            f"At the heart of your current experience, {name} emerges",
            f"Your present moment is defined by {name}"
        ],
        "Future": [
            f"Moving into the Future position, {name}",
            f"The path ahead reveals {name}",
            f"Looking to what is forming on your horizon, {name} appears",
            f"The emerging energy ahead crystallizes as {name}"
        ],
        "Situation": [
            f"At the core of your situation, {name}",
            f"The heart of the matter presents {name}",
            f"Defining your current circumstances, {name} emerges"
        ],
        "Challenge": [
            f"The challenge before you takes the form of {name}",
            f"What tests you now appears as {name}",
            f"The obstacle in your path manifests as {name}"
        ],
        "Advice": [
            f"The guidance offered comes through {name}",
            f"As counsel for your journey, {name} speaks",
            f"The wisdom for this situation emerges through {name}"
        ],
        "Outcome": [
            f"The potential outcome crystallizes as {name}",
            f"Where this path may lead shows {name}",
            f"The culmination energy appears as {name}"
        ],
        "Above": [
            f"In the Above position, representing your aspirations, {name}",
            f"What you reach toward manifests as {name}",
            f"Your highest potential in this matter shows {name}"
        ],
        "Below": [
            f"The Below position reveals {name}",
            f"At the foundation of this situation, {name} appears",
            f"What grounds this experience is {name}"
        ],
        "Today's Guidance": [
            f"For today's guidance, {name} comes forward",
            f"The message for your day arrives as {name}",
            f"Today's wisdom speaks through {name}"
        ],
        "Action": [
            f"The action called for reveals itself as {name}",
            f"What to do next appears through {name}",
            f"The step forward shows {name}"
        ],
        "Obstacles": [
            f"The obstacles you face take the form of {name}",
            f"What blocks your path appears as {name}",
            f"Challenges manifest through {name}"
        ],
        "External": [
            f"External forces appear as {name}",
            f"The outside influences show {name}",
            f"What surrounds you manifests as {name}"
        ],
        "External Influences": [
            f"External influences arrive through {name}",
            f"Forces beyond your control appear as {name}",
            f"The outside world shows {name}"
        ],
        "Hidden Influences": [
            f"Hidden influences emerge as {name}",
            f"What operates beneath the surface appears as {name}",
            f"Unseen forces manifest through {name}"
        ],
        "Hopes/Fears": [
            f"Your hopes and fears crystallize in {name}",
            f"What you both desire and dread shows as {name}",
            f"The dual nature of hope and fear appears through {name}"
        ]
    }

    transitions = position_transitions.get(position, [
        f"In the {position} position, {name}",
        f"The {position} reveals {name}",
        f"As {position}, {name} speaks"
    ])

    para += random.choice(transitions)

    # Add reversed indicator
    if is_reversed:
        reversed_phrases = [
            " in its reversed aspect, signaling that this energy is blocked, internalized, or expressing through shadow.",
            " reversed, indicating that the usual expression of this card is turned inward or encountering resistance.",
            " appearing upside down, suggesting a need to examine where this energy may be stuck or misdirected.",
            " in reversal, pointing to hidden dimensions of this archetype that require your attention."
        ]
        para += random.choice(reversed_phrases)
    else:
        upright_phrases = [
            ", standing upright and channeling its energy directly into your situation.",
            ", expressing its essence clearly and powerfully.",
            " in its full upright expression, bringing its gifts openly.",
            ", radiating its traditional meaning with clarity."
        ]
        para += random.choice(upright_phrases)

    # Add position context if available
    if pos_context and pos_context != "Meaning not available":
        para += f" {pos_context}"

    # Add base meaning if available
    if base_meaning and base_meaning != "Meaning not available":
        meaning_intros = [
            f" This card speaks to {base_meaning.lower() if base_meaning[0].isupper() else base_meaning}",
            f" The essence here involves {base_meaning.lower() if base_meaning[0].isupper() else base_meaning}",
            f" At its core, this represents {base_meaning.lower() if base_meaning[0].isupper() else base_meaning}"
        ]
        para += random.choice(meaning_intros)

    # Add keywords interpretation
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
        if len(keyword_list) >= 2:
            keyword_phrases = [
                f" The themes of {keyword_list[0]} and {keyword_list[1]} interweave throughout this energy.",
                f" Notice how {keyword_list[0]} connects to your question through {keyword_list[-1]}.",
                f" The qualities of {', '.join(keyword_list[:3])} all play a role here."
            ]
            para += random.choice(keyword_phrases)

    # For single card readings, add more depth
    if card_count == 1:
        single_card_additions = [
            f" As the sole card in this reading, {name} carries the full weight of the message. Its presence is especially significant.",
            f" The singular appearance of {name} focuses all energy on this theme. Consider how this archetype speaks to every aspect of your question.",
            f" With {name} as your only card, the universe asks you to deeply contemplate this energy and its role in your life."
        ]
        para += random.choice(single_card_additions)

    return para


def generate_synthesis(cards, elemental_balance, elemental_flow, question, theme):
    """Generate the synthesis and actionable insight paragraph."""
    para = ""

    # Count reversed cards
    reversed_count = sum(1 for c in cards if c["orientation"] == "reversed")
    total_cards = len(cards)

    # Elemental insight
    if elemental_balance:
        elemental_meanings = {
            "Fire": "passion, action, and creative will",
            "Water": "emotion, intuition, and relational flow",
            "Air": "thought, communication, and mental clarity",
            "Earth": "stability, practicality, and material manifestation"
        }
        meaning = elemental_meanings.get(elemental_balance, "balanced energy")
        para += f"The dominant {elemental_balance} energy in this spread emphasizes {meaning}. "

    if elemental_flow and len(elemental_flow) >= 3:
        para += f"The elemental progression from {elemental_flow[0]} through {elemental_flow[1]} to {elemental_flow[2]} traces your journey's energetic arc. "

    # Reversed card synthesis
    if total_cards == 1:
        if reversed_count == 0:
            para += "With this card appearing upright, its energy flows directly into your situation without obstruction. "
        else:
            para += "The reversed nature of this card invites you to look within, to examine where this energy may need attention or redirection. "
    elif reversed_count == 0:
        para += "With all cards appearing upright, the energies in your reading flow without significant obstruction. This suggests a time when external circumstances align with internal readiness for change. "
    elif reversed_count == total_cards:
        para += "The entirely reversed nature of this spread indicates a deeply internal process. This is a time for reflection, shadow work, and addressing what lies beneath the surface before taking external action. "
    elif reversed_count >= total_cards // 2:
        para += f"The {reversed_count} reversed cards in your spread suggest significant areas requiring conscious attention. Some energies are blocked or need to be redirected before full manifestation can occur. "
    else:
        para += f"The mix of {total_cards - reversed_count} upright and {reversed_count} reversed card{'s' if reversed_count > 1 else ''} reveals a nuanced situation where some paths flow freely while others require additional work. "

    # Theme-specific actionable insight
    theme_actions = {
        'relationships': [
            "In matters of the heart, the cards counsel patience with yourself and honest communication with others.",
            "For your relationship journey, focus on understanding your own patterns before seeking to change another.",
            "The path forward in love requires equal measures of vulnerability and self-protection."
        ],
        'career': [
            "In your professional life, consider where your true talents may be underutilized or misdirected.",
            "Career progress now depends on aligning your daily actions with your deeper purpose.",
            "The practical steps forward involve honest assessment of what success truly means to you."
        ],
        'health': [
            "For your wellbeing, the cards emphasize the mind-body connection and the healing power of awareness.",
            "Your health journey benefits from addressing emotional roots alongside physical symptoms.",
            "Healing comes through both rest and intentional action in balance."
        ],
        'spiritual': [
            "Your spiritual growth calls for embracing both light and shadow aspects of your journey.",
            "The path of awakening requires surrender alongside dedicated practice.",
            "Purpose reveals itself through present-moment awareness rather than future-focused searching."
        ],
        'family': [
            "Family dynamics shift when one person changes their role in the pattern.",
            "The healing of family bonds begins with the healing of self.",
            "Boundaries and love can coexist; in fact, healthy boundaries enable deeper love."
        ],
        'decision': [
            "The decision before you benefits from both logical analysis and intuitive sensing.",
            "Rather than seeking the 'right' choice, consider which path offers the richest growth.",
            "Trust that you have the wisdom to choose well, and the resilience to course-correct if needed."
        ],
        'emotional': [
            "Your feelings are valid messengers, but they are not the whole truth of any situation.",
            "Emotional wisdom comes from feeling fully while also stepping back to observe.",
            "What you fear often points to what you most need to address and ultimately embrace."
        ],
        'general': [
            "The cards invite you to hold both patience and action in creative tension.",
            "Trust the process while also taking conscious steps forward.",
            "Wisdom lies in knowing when to push and when to yield."
        ]
    }

    para += random.choice(theme_actions.get(theme, theme_actions['general'])) + " "

    # Final actionable step
    first_card = cards[0]["card_name"] if cards else "the card"
    last_card = cards[-1]["card_name"] if cards else "the card"
    mid_card = cards[len(cards)//2]["card_name"] if cards else "the card"

    if total_cards == 1:
        actions = [
            f"As a concrete step, spend time this week journaling about how the energy of {first_card} manifests in your daily life.",
            f"Consider meditating on {first_card} to invite its wisdom more fully into your awareness.",
            f"The reading suggests noticing when {first_card} themes arise over the next few days and how you respond to them.",
            f"Create space for reflection by asking yourself how {first_card} speaks to both your challenges and your gifts."
        ]
    else:
        actions = [
            f"As a concrete step, spend time this week journaling about how the energy of {first_card} has shaped your relationship with this question.",
            f"Consider meditating on {last_card} to invite its wisdom into your daily awareness.",
            f"The reading suggests taking one small action aligned with the {mid_card} energy within the next three days.",
            f"Create space for reflection by returning to this reading in a week to see how the patterns have shifted.",
            f"Honor the message of {last_card} by noticing where its themes appear in your life over the coming days."
        ]

    para += random.choice(actions)

    # Closing wisdom
    closures = [
        " Remember that tarot illuminates possibilities rather than fixed destinies. Your choices shape the path forward.",
        " Trust your inner wisdom as you integrate these insights. The cards confirm what your soul already knows.",
        " Let this reading serve as a compass point, not a map. Your journey remains uniquely yours to walk.",
        " May these reflections offer clarity and courage as you navigate what lies ahead.",
        " The power of transformation lies within you. These cards simply mirror your own inner knowing."
    ]

    para += random.choice(closures)

    return para


def generate_extended_interpretation(cards, question, theme):
    """Generate additional interpretive content to meet word count requirements."""
    para = ""

    card_names = [c["card_name"] for c in cards]
    positions = [c["position"] for c in cards]

    interp_options = [
        f"The interplay between these cards creates a tapestry of meaning unique to your question. Each card informs the others, creating a dialogue that speaks to the complexity of your situation.",
        f"When we consider how {card_names[0] if card_names else 'the cards'} flows into the overall reading, we see layers of meaning that reward contemplation.",
        f"This spread invites you to consider the journey from where you have been to where you are heading. The narrative arc suggests transformation is not only possible but already underway.",
        f"Notice how the energy shifts through the reading, guiding you from awareness through understanding toward action.",
        f"The cards work together to illuminate different facets of your question, each offering a unique perspective that enriches the whole."
    ]

    para += random.choice(interp_options)

    # Add theme-specific elaboration
    theme_elaborations = {
        'relationships': " In matters of connection, we often project our inner state onto others. This reading invites you to discern what truly belongs to you versus what you may be attributing to others.",
        'career': " Professional fulfillment often requires aligning outer success with inner purpose. Consider how your work serves not just practical needs but also your deeper calling.",
        'health': " The body often speaks what the mind cannot articulate. Pay attention to what symptoms or energy patterns may be communicating about your emotional and spiritual state.",
        'spiritual': " Spiritual growth rarely follows a linear path. Trust that even apparent setbacks contain seeds of awakening if approached with curiosity rather than judgment.",
        'family': " Family patterns often span generations, invisibly shaping our expectations and reactions. Awareness itself begins the work of conscious choice over inherited reflex.",
        'decision': " Every choice closes some doors while opening others. The question is not finding the perfect path but choosing with full presence and accepting the consequences with grace.",
        'emotional': " Emotions are messengers, not masters. Learning to feel fully without being controlled by feelings is one of life's great developmental tasks.",
        'general': " Life moves in cycles of expansion and contraction. Understanding where you are in your current cycle helps you align with rather than resist natural rhythms."
    }

    para += theme_elaborations.get(theme, theme_elaborations['general'])

    return para


def generate_reading(parsed_data, question, prompt_id):
    """Generate a complete 3-5 paragraph tarot reading."""
    seed_random(prompt_id, question)

    cards = parsed_data["cards"]
    timing = parsed_data.get("timing", "")
    timing_meaning = parsed_data.get("timing_meaning", "")
    elemental = parsed_data.get("elemental_balance", "")
    elemental_flow = parsed_data.get("elemental_flow", [])
    theme = get_question_theme(question)

    if not cards:
        return "Unable to generate reading - no cards found in spread."

    paragraphs = []

    # Paragraph 1: Opening
    opening = generate_opening(question, timing, timing_meaning, cards, theme)
    paragraphs.append(opening)

    # Paragraphs 2-4: Card interpretations
    card_count = len(cards)

    if card_count == 1:
        # Single card - one detailed paragraph
        para = generate_card_paragraph(cards[0], None, None, theme, card_count)
        paragraphs.append(para)
        # Add extended interpretation for single cards
        extended = generate_extended_interpretation(cards, question, theme)
        paragraphs.append(extended)
    elif card_count <= 3:
        # Detailed paragraph for each card
        for i, card in enumerate(cards):
            prev_card = cards[i-1] if i > 0 else None
            next_card = cards[i+1] if i < len(cards)-1 else None
            para = generate_card_paragraph(card, prev_card, next_card, theme, card_count)
            paragraphs.append(para)
    else:
        # Combine some cards for longer spreads
        # First card paragraph
        paragraphs.append(generate_card_paragraph(cards[0], None, cards[1], theme, card_count))

        # Middle cards combined
        middle_para = ""
        for i, card in enumerate(cards[1:-1], 1):
            if i > 1:
                middle_para += " "
            middle_para += generate_card_paragraph(card, cards[i-1], cards[i+1], theme, card_count)
        if middle_para:
            paragraphs.append(middle_para)

        # Last card paragraph
        paragraphs.append(generate_card_paragraph(cards[-1], cards[-2], None, theme, card_count))

    # Final paragraph: Synthesis and actionable insight
    synthesis = generate_synthesis(cards, elemental, elemental_flow, question, theme)
    paragraphs.append(synthesis)

    # Join paragraphs with double newlines
    reading = "\n\n".join(paragraphs)

    # Verify word count and adjust if needed
    word_count = len(reading.split())
    if word_count < 200:
        # Add elaboration
        elaboration = generate_extended_interpretation(cards, question, theme)
        reading += "\n\n" + elaboration

    return reading


def main():
    """Main function to process all prompts and generate responses."""
    print("Loading batch file...")

    with open('/home/user/taro/training/data/batches_expanded/batch_0013.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    total = len(prompts)
    output_file = '/home/user/taro/training/data/batches_expanded/responses/batch_0013_responses.jsonl'

    print(f"Processing {total} prompts...")

    with open(output_file, 'w') as out_f:
        for i, prompt in enumerate(prompts):
            prompt_id = prompt['id']
            question = prompt['question']
            input_text = prompt['input_text']

            # Parse the input text
            parsed = parse_input_text(input_text)

            # Generate the reading
            response = generate_reading(parsed, question, prompt_id)

            # Write to JSONL
            output_line = json.dumps({"id": prompt_id, "response": response}, ensure_ascii=False)
            out_f.write(output_line + '\n')

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{total} prompts")

    print(f"\nCompleted! Generated {total} responses")
    print(f"Output written to: {output_file}")

    # Validate output
    print("\nValidating output...")
    with open(output_file, 'r') as f:
        lines = f.readlines()
        word_counts = []
        failed_count = 0
        for line in lines:
            data = json.loads(line)
            wc = len(data['response'].split())
            word_counts.append(wc)
            if wc < 50:
                failed_count += 1

    print(f"Total responses: {len(lines)}")
    print(f"Failed (< 50 words): {failed_count}")
    print(f"Average word count: {sum(word_counts)/len(word_counts):.1f}")
    print(f"Min word count: {min(word_counts)}")
    print(f"Max word count: {max(word_counts)}")

    # Show sample
    print("\n--- Sample response (first entry) ---")
    with open(output_file, 'r') as f:
        first_line = f.readline()
        sample = json.loads(first_line)
        print(f"ID: {sample['id']}")
        print(f"Response ({len(sample['response'].split())} words):")
        print(sample['response'][:800] + "..." if len(sample['response']) > 800 else sample['response'])


if __name__ == "__main__":
    main()
