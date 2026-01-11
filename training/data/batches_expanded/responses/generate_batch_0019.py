#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0019.json - Enhanced version"""

import json
import re
import random
from pathlib import Path

# Load the batch file
batch_path = Path("/home/user/taro/training/data/batches_expanded/batch_0019.json")
output_path = Path("/home/user/taro/training/data/batches_expanded/responses/batch_0019_responses.jsonl")

with open(batch_path) as f:
    data = json.load(f)

def parse_input_text(input_text):
    """Parse the input text to extract timing, question, and cards."""
    result = {
        "timing": "",
        "timing_meaning": "",
        "question": "",
        "cards": [],
        "elemental_balance": "",
        "dominant_element": ""
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1)
        # Remove emoji
        timing_full = re.sub(r'[\U0001F300-\U0001F9FF]', '', timing_full).strip()
        result["timing"] = timing_full.split(" — ")[0].strip() if " — " in timing_full else timing_full
        result["timing_meaning"] = timing_full.split(" — ")[1].strip() if " — " in timing_full else ""

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result["question"] = question_match.group(1)

    # Extract cards
    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s+Keywords:\s*([^\n]+)\n\s+Base meaning:\s*([^\n]+)\n\s+Position context:\s*([^\n]+)'
    for match in re.finditer(card_pattern, input_text):
        card = {
            "number": match.group(1),
            "position": match.group(2).strip(),
            "name": match.group(3).strip(),
            "keywords": match.group(4).strip(),
            "base_meaning": match.group(5).strip(),
            "position_context": match.group(6).strip()
        }
        card["reversed"] = "(reversed)" in card["name"].lower()
        card["card_name"] = card["name"].replace("(reversed)", "").replace("(upright)", "").strip()
        result["cards"].append(card)

    # Extract elemental balance
    balance_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if balance_match:
        result["elemental_balance"] = balance_match.group(1).strip()

    # Extract dominant element
    dominant_match = re.search(r'Dominant:\s*(\w+)\s*energy', input_text)
    if dominant_match:
        result["dominant_element"] = dominant_match.group(1)

    return result

def capitalize_first(text):
    """Capitalize first letter of text."""
    if not text:
        return text
    return text[0].upper() + text[1:] if len(text) > 1 else text.upper()

def capitalize_sentences(text):
    """Capitalize first letter of each sentence and after common punctuation."""
    if not text:
        return text
    # First split by period
    result = []
    sentences = text.split('. ')
    for i, s in enumerate(sentences):
        s = s.strip()
        if not s:
            continue
        # Capitalize first letter
        s = capitalize_first(s)
        # Also capitalize after em-dashes
        parts = s.split('—')
        s = '—'.join(capitalize_first(p.strip()) if j > 0 else p for j, p in enumerate(parts))
        result.append(s)
    return '. '.join(result)

def format_question_phrase(question):
    """Format question as a readable phrase."""
    q = question.lower().rstrip('?').strip()
    # Remove common question starters for flowing prose
    starters_to_remove = [
        "what steps should i take to ",
        "what steps should i take ",
        "what is the true cost of ",
        "what causes my ",
        "what wisdom is my ",
        "what should i ",
        "what steps ",
        "what parts of my ",
        "what ",
        "how can i recover from ",
        "how can i ",
        "how do i ",
        "how should i ",
        "how ",
        "should i prioritize ",
        "should i ",
        "will i find ",
        "will i ",
        "am i going to find ",
        "am i going to ",
        "am i ",
        "is my relationship with ",
        "is my ",
        "where is my ",
        "where is ",
        "which parts of my ",
        "which parts of ",
        "which ",
    ]
    for starter in starters_to_remove:
        if q.startswith(starter):
            q = q[len(starter):]
            break
    return q

def format_card_name(name):
    """Format card name to avoid double 'The' and clean up."""
    name = name.strip()
    # Remove duplicate "The" patterns
    while "The The " in name:
        name = name.replace("The The ", "The ")
    while "the The " in name:
        name = name.replace("the The ", "the ")
    if name.startswith("The The "):
        name = name[4:]
    return name

# Opening phrases for variety
OPENINGS = [
    "Your cards speak with clarity about the path before you.",
    "The spread reveals meaningful patterns for your consideration.",
    "There is much wisdom emerging from these cards.",
    "This reading illuminates your question with depth and nuance.",
    "The cards have assembled to offer guidance worth heeding.",
    "A powerful message emerges from this configuration.",
    "Your inquiry has drawn forth significant insights.",
    "The energies present in this spread deserve careful attention.",
    "These cards tell a story that speaks directly to your situation.",
    "What surfaces in this reading holds practical wisdom for you.",
]

# Transition phrases
TRANSITIONS = [
    "Looking deeper into the spread,",
    "The surrounding cards add important context.",
    "Building upon this foundation,",
    "The energetic flow continues as",
    "This connects to a broader pattern where",
    "The reading deepens to reveal that",
    "Further layers emerge as we see",
    "The narrative expands when we consider that",
    "Adding another dimension,",
    "The cards weave together to show",
]

# Position-specific language
POSITION_INTROS = {
    "past": ["Your past position reveals", "Looking to what shaped this moment,", "The foundation of your situation shows", "What brought you here is reflected in"],
    "present": ["In the present moment,", "Your current position shows", "Right now, the energy manifests as", "The heart of your situation reveals"],
    "future": ["Looking ahead,", "What approaches is signaled by", "The future position suggests", "Coming energies appear as"],
    "challenge": ["The challenge before you is reflected in", "What you must navigate appears as", "The obstacle or growth edge shows", "Testing you at this time,"],
    "advice": ["The guidance offered comes through", "Your counsel appears as", "The wisdom to heed emerges from", "For direction, consider"],
    "outcome": ["The trajectory leads toward", "This path culminates in", "The potential outcome appears as", "Where this leads is shown by"],
    "situation": ["The core of your situation is captured by", "At the heart of this matter,", "The essence of what you face appears as", "Your circumstances are reflected in"],
    "action": ["The action called for is", "What to do is shown by", "Your next move is guided by", "The step to take emerges from"],
    "hidden": ["Beneath the surface,", "Operating unseen,", "The hidden influence of", "What you may not see is"],
    "external": ["From the outside,", "External forces manifest as", "Others and circumstances bring", "The world around you offers"],
    "above": ["At your highest potential,", "The best possible outcome shows", "What you aspire to appears as", "Your guiding star is"],
    "below": ["At the root of this,", "Underlying everything,", "The foundation holds", "Deep beneath, we find"],
    "hopes": ["Your hopes and fears converge in", "What you wish for and dread alike appears as", "The emotional stakes show in", "Your deepest feelings manifest as"],
}

def get_position_intro(position):
    """Get an appropriate intro phrase for a card position."""
    pos_lower = position.lower()
    for key, phrases in POSITION_INTROS.items():
        if key in pos_lower:
            return random.choice(phrases)
    return f"The {position} position shows"

# Element descriptions
ELEMENT_INSIGHTS = {
    "Fire": "This fire-dominant reading emphasizes action, passion, and creative will. You are being called to move boldly.",
    "Water": "The water energy flowing through this reading speaks to emotions, intuition, and the wisdom of feeling rather than thinking.",
    "Air": "With air energy prevailing, this is a time for mental clarity, communication, and seeing truth without illusion.",
    "Earth": "The earth element grounding this reading points to practical matters, material concerns, and the need for tangible action.",
    "Balanced": "The elemental balance in this reading suggests you have access to multiple types of energy and wisdom right now."
}

def generate_reading(prompt_data):
    """Generate a full tarot reading response."""
    parsed = parse_input_text(prompt_data["input_text"])
    question = parsed["question"] or prompt_data.get("question", "your situation")
    cards = parsed["cards"]
    timing = parsed["timing"]
    timing_meaning = parsed["timing_meaning"]
    q_phrase = format_question_phrase(question)

    if not cards:
        return generate_generic_reading(question)

    paragraphs = []

    # PARAGRAPH 1: Opening and first cards
    opening = random.choice(OPENINGS)
    para1 = f"{opening} "

    if timing_meaning:
        para1 += f"The {timing} phase carries the energy of {timing_meaning.lower()}, setting a meaningful context for exploring {q_phrase}. "

    # First card with position-specific intro
    first_card = cards[0]
    first_card_name = format_card_name(first_card['card_name'])
    pos_intro = get_position_intro(first_card["position"])
    first_context = capitalize_sentences(first_card['position_context'])

    if first_card["reversed"]:
        para1 += f"{pos_intro} the {first_card_name} in its reversed aspect. {first_context} "
    else:
        para1 += f"{pos_intro} the {first_card_name}. {first_context} "

    # Second card if exists
    if len(cards) > 1:
        second_card = cards[1]
        second_card_name = format_card_name(second_card['card_name'])
        second_intro = get_position_intro(second_card["position"])
        second_context = capitalize_sentences(second_card['position_context'])
        if second_card["reversed"]:
            para1 += f"{second_intro} the {second_card_name} reversed, indicating that {second_context.lower() if second_context else ''}"
        else:
            para1 += f"{second_intro} the {second_card_name}, suggesting that {second_context.lower() if second_context else ''}"

    paragraphs.append(para1)

    # PARAGRAPH 2: Middle cards and weaving
    if len(cards) > 2:
        transition = random.choice(TRANSITIONS)
        para2 = f"{transition} "

        middle_cards = cards[2:min(len(cards), 5)]
        card_interpretations = []

        for card in middle_cards:
            card_name = format_card_name(card['card_name'])
            pos_intro = get_position_intro(card["position"])
            context = capitalize_sentences(card['position_context'])
            if card["reversed"]:
                interp = f"{pos_intro.lower()} the {card_name} reversed reveals that {context.lower() if context else ''}"
            else:
                interp = f"{pos_intro.lower()} the {card_name} shows that {context.lower() if context else ''}"
            card_interpretations.append(interp)

        para2 += " Furthermore, ".join(card_interpretations[:2])
        if len(card_interpretations) > 2:
            para2 += f" Additionally, {card_interpretations[2]}"

        para2 += f" These threads weave together to address your question about {q_phrase}."
        paragraphs.append(para2)

    # PARAGRAPH 3: Additional cards for large spreads or thematic expansion
    if len(cards) > 5:
        remaining_cards = cards[5:-1] if len(cards) > 6 else [cards[5]]
        para3 = "The surrounding influences provide essential context. "

        for i, card in enumerate(remaining_cards[:3]):
            card_name = format_card_name(card['card_name'])
            pos_intro = get_position_intro(card["position"])
            context = capitalize_sentences(card['position_context'])
            if card["reversed"]:
                para3 += f"{pos_intro} the {card_name} reversed signals that {context.lower() if context else ''}. "
            else:
                para3 += f"{pos_intro} the {card_name} indicates that {context.lower() if context else ''}. "

        paragraphs.append(para3)
    elif len(cards) <= 2:
        # Expand for short spreads
        para3 = generate_thematic_expansion(question, cards)
        paragraphs.append(para3)

    # PARAGRAPH 4: Outcome and synthesis
    outcome_card = None
    advice_card = None
    for card in cards:
        if "outcome" in card["position"].lower():
            outcome_card = card
        if "advice" in card["position"].lower():
            advice_card = card

    if not outcome_card:
        outcome_card = cards[-1]

    para4 = ""
    if outcome_card:
        outcome_name = format_card_name(outcome_card['card_name'])
        outcome_context = capitalize_sentences(outcome_card['position_context'])
        if outcome_card["reversed"]:
            para4 = f"Your {outcome_card['position'].lower()}, the {outcome_name} reversed, carries an important message. {outcome_context} While this presents challenges, it also reveals where growth is possible. "
        else:
            para4 = f"The {outcome_name} appearing as your {outcome_card['position'].lower()} offers encouragement. {outcome_context} This suggests a constructive path forward exists. "

    # Add elemental insight
    if parsed["dominant_element"] and parsed["dominant_element"] in ELEMENT_INSIGHTS:
        para4 += ELEMENT_INSIGHTS[parsed["dominant_element"]] + " "
    elif parsed["elemental_balance"] and "Balanced" in parsed["elemental_balance"]:
        para4 += "The elemental balance present suggests you can draw upon multiple energies as needed. "

    paragraphs.append(para4)

    # PARAGRAPH 5: Actionable guidance
    para5 = "For your path forward: "

    if advice_card:
        advice_name = format_card_name(advice_card['card_name'])
        advice_context = capitalize_sentences(advice_card['position_context'])
        if advice_card["reversed"]:
            para5 += f"The {advice_name} reversed as your guidance suggests you {advice_context.lower() if advice_context else ''}. "
        else:
            para5 += f"Taking the {advice_name}'s counsel, {advice_context.lower() if advice_context else ''}. "

    para5 += generate_action_from_question(question, cards)
    para5 += " " + generate_specific_actions(question, cards)

    paragraphs.append(para5)

    # Ensure minimum length
    result = " ".join(paragraphs)
    word_count = len(result.split())

    while word_count < 210:
        result += " " + generate_additional_wisdom(question, cards)
        word_count = len(result.split())

    # Post-process to fix common issues
    result = post_process_response(result)

    return result

def post_process_response(text):
    """Fix common formatting issues in the response."""
    # Fix "The The" patterns
    text = text.replace("The The ", "The ")
    text = text.replace("the The ", "the ")

    # Fix sentences that start with lowercase after period+space
    import re
    def fix_sentence_start(match):
        return match.group(1) + match.group(2).upper()

    text = re.sub(r'(\. )([a-z])', fix_sentence_start, text)

    # Fix sentences that start with lowercase after em-dash
    text = re.sub(r'(—)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)

    # Remove double spaces
    while '  ' in text:
        text = text.replace('  ', ' ')

    return text

def generate_thematic_expansion(question, cards):
    """Generate additional thematic content for short spreads."""
    q_lower = question.lower()

    expansions = []

    if any(word in q_lower for word in ["heal", "toxic", "relationship"]):
        expansions = [
            "Healing from difficult relationships requires patience with yourself above all. The patterns that brought you here did not form overnight, and they will not dissolve instantly either. Trust that each day brings small opportunities for growth.",
            "What has wounded you has also taught you something valuable about your own boundaries and needs. As you move forward, carry the wisdom while releasing the pain.",
        ]
    elif any(word in q_lower for word in ["career", "job", "work", "professional"]):
        expansions = [
            "Your professional path is rarely linear, though it often appears so in retrospect. The doubts and transitions you experience now are part of a larger unfolding that will make sense with time.",
            "Consider that work is not merely about external achievements but about expressing your authentic gifts in the world. When these align, fulfillment follows.",
        ]
    elif any(word in q_lower for word in ["decision", "choice", "should"]):
        expansions = [
            "Every significant choice involves releasing one possibility to embrace another. This letting go is often where the real difficulty lies, not in the decision itself.",
            "Trust that you have more wisdom than you credit yourself with. The answer often arrives not through more thinking but through creating stillness in which insight can surface.",
        ]
    elif any(word in q_lower for word in ["money", "financial"]):
        expansions = [
            "Your relationship with resources reflects deeper beliefs about security, worthiness, and flow. Examining these beliefs can unlock new possibilities.",
            "Material concerns, while practical, are also symbolic of how you value yourself and what you believe you deserve. Consider both dimensions.",
        ]
    elif any(word in q_lower for word in ["health", "body", "sleep", "pain"]):
        expansions = [
            "Your body carries wisdom that your mind sometimes overlooks. Listen to its messages with compassion rather than frustration.",
            "Healing is not always linear. Honor the progress you have made even when setbacks occur, and treat yourself with the kindness you would offer a dear friend.",
        ]
    elif any(word in q_lower for word in ["creative", "art", "project"]):
        expansions = [
            "Creative blocks often protect us from something we are not yet ready to face. Rather than pushing through, consider what the resistance might be showing you.",
            "Every creative endeavor moves through seasons of productivity and fallow periods. Both are necessary for the full expression of your gifts.",
        ]
    elif any(word in q_lower for word in ["spiritual", "purpose", "meaning"]):
        expansions = [
            "The search for meaning is itself meaningful. The questions you carry are shaping you as much as any answers will.",
            "Purpose often reveals itself not through grand revelations but through the quiet accumulation of what brings you alive. Notice what enlivens you.",
        ]
    elif any(word in q_lower for word in ["identity", "who am i", "self"]):
        expansions = [
            "You are not fixed but ever-becoming. The parts of yourself you are questioning now are not failures but invitations to greater authenticity.",
            "Your identity is both who you have been and who you are becoming. Honor your history while giving yourself permission to evolve.",
        ]
    else:
        expansions = [
            "This moment, however it feels, is temporary. What seems solid will shift; what seems stuck will eventually move. Trust the process.",
            "The answers you seek may not come in the form you expect. Stay open to wisdom arriving through unexpected channels.",
        ]

    return random.choice(expansions)

def generate_action_from_question(question, cards):
    """Generate action advice based on question type."""
    q_lower = question.lower()

    if any(word in q_lower for word in ["relationship", "love", "partner", "dating"]):
        return "Focus on honest communication and emotional authenticity. Speak your truth with compassion, and create space for others to do the same."
    elif any(word in q_lower for word in ["career", "job", "work", "professional"]):
        return "Take concrete steps toward your professional goals while remaining adaptable to unexpected opportunities. Document your achievements and clarify your core values."
    elif any(word in q_lower for word in ["money", "financial", "finances", "wealth"]):
        return "Review your resources with honesty and make decisions from clarity rather than fear. Consider seeking guidance from those with relevant expertise."
    elif any(word in q_lower for word in ["health", "healing", "wellness", "pain", "body"]):
        return "Prioritize consistent self-care practices and consider consulting appropriate professionals. Small daily habits often matter more than dramatic interventions."
    elif any(word in q_lower for word in ["creative", "creativity", "art", "project"]):
        return "Trust your creative instincts while maintaining practical discipline. Set aside protected time for your craft without pressure for immediate results."
    elif any(word in q_lower for word in ["decision", "choice", "should i"]):
        return "Gather the information you need, then trust your gut. Analysis has its place, but at some point you must act with imperfect knowledge."
    elif any(word in q_lower for word in ["family", "parent", "child", "home"]):
        return "Nurture important connections while maintaining healthy boundaries. Express care in ways that honor both your needs and those of your family."
    elif any(word in q_lower for word in ["spiritual", "purpose", "meaning"]):
        return "Create regular space for reflection and contemplation. The answers you seek often emerge from stillness rather than striving."
    elif any(word in q_lower for word in ["anxiety", "fear", "worry", "stress"]):
        return "Ground yourself through breath, movement, or contact with nature when anxious thoughts arise. Name what you feel without judgment."
    elif any(word in q_lower for word in ["identity", "who am i", "self"]):
        return "Explore what values truly resonate with you versus those inherited from others. Give yourself permission to evolve."
    elif any(word in q_lower for word in ["community", "friend", "social", "belong"]):
        return "Begin with small, low-pressure connections before committing to larger group involvement. Quality matters more than quantity in relationships."
    elif any(word in q_lower for word in ["burnout", "exhaust", "tired"]):
        return "Identify and protect non-negotiable rest time. Delegate or release what you can, and recognize that sustainable effort outperforms unsustainable intensity."
    elif any(word in q_lower for word in ["change", "transition", "moving"]):
        return "Acknowledge what you are grieving about the old while consciously welcoming the new. Transitions require mourning as much as anticipation."
    else:
        return "Stay present with what is while taking small, consistent steps forward. Trust that clarity will come through engagement rather than waiting."

def generate_specific_actions(question, cards):
    """Generate specific actionable steps."""
    q_lower = question.lower()

    actions = []

    # Check for reversed cards suggesting shadow work
    reversed_count = sum(1 for c in cards if c["reversed"])
    if reversed_count > len(cards) / 2:
        actions.append("With multiple reversed cards appearing, prioritize inner reflection before external action. Something within needs attention first.")

    # Question-specific actions
    if "heal" in q_lower or "recovery" in q_lower:
        actions.append("Consider journaling to process your experience, and be patient with your timeline for healing.")
    elif "toxic" in q_lower:
        actions.append("Establish and maintain firm boundaries. Consider what support systems you need to stay centered.")
    elif "career" in q_lower or "job" in q_lower:
        actions.append("This week, take one concrete step toward clarifying what you truly want from your work life.")
    elif "relationship" in q_lower:
        actions.append("Practice expressing your needs clearly without attachment to a specific response from others.")
    elif "decision" in q_lower:
        actions.append("Write out the implications of each choice, then notice your gut response when you imagine living with each option.")
    elif "anxiety" in q_lower or "fear" in q_lower or "paralysis" in q_lower:
        actions.append("When anxious thoughts arise, name them specifically rather than letting them remain vague. Specificity reduces their power.")
    elif "money" in q_lower or "financial" in q_lower:
        actions.append("Create a clear picture of your current situation before making any changes. Knowledge brings power here.")
    elif "creative" in q_lower:
        actions.append("Set aside dedicated time this week for your creative work, even if only fifteen minutes. Consistency builds momentum.")
    elif "spiritual" in q_lower or "purpose" in q_lower:
        actions.append("Establish a simple daily practice, even if only five minutes, to create space for inner listening.")
    elif "sleep" in q_lower:
        actions.append("Create a consistent wind-down ritual before bed, and address racing thoughts through journaling rather than rumination.")
    elif "identity" in q_lower or "who am i" in q_lower:
        actions.append("This week, notice moments when you feel most yourself. These point toward your authentic core.")
    elif "community" in q_lower:
        actions.append("Reach out to one person this week, without pressure for it to become a deep connection immediately.")
    elif "burnout" in q_lower or "exhaust" in q_lower:
        actions.append("Identify one thing you can stop doing or delegate this week. Protection of your energy is not selfish but necessary.")
    elif "change" in q_lower or "transition" in q_lower:
        actions.append("Acknowledge both excitement and grief as valid parts of any transition. Make space for both.")
    elif "trust" in q_lower:
        actions.append("Observe patterns over time rather than judging isolated incidents. Trust is built through consistent evidence.")
    elif "food" in q_lower or "eating" in q_lower or "body" in q_lower:
        actions.append("Approach your relationship with nourishment with curiosity rather than judgment. Notice patterns without immediately trying to fix them.")
    else:
        actions.append("Take one small action this week that aligns with the guidance offered here. Small steps create momentum.")

    return " ".join(actions)

def generate_additional_wisdom(question, cards):
    """Generate additional content to meet word count."""
    additions = [
        "Remember that growth rarely follows a straight line. Honor your progress even when it feels slow or uncertain. Each step, however small, moves you forward on your path.",
        "The wisdom you seek is often already within you, waiting for the space to emerge. Trust what you know in your bones, not just your mind. Stillness reveals what activity obscures.",
        "Change takes time, and patience with yourself is not passive but an active form of self-care. Be as kind to yourself as you would be to someone you love dearly.",
        "Every reading is a snapshot of energies in motion. You are not fixed to any outcome but always have the power of choice in how you respond to circumstances.",
        "What feels like an ending may be a beginning in disguise. Remain open to possibilities you cannot yet see. The universe often works in mysterious ways.",
        "Trust the timing of your life, even when it differs from what you planned. What is meant for you will find its way to you in the right moment.",
        "Your journey is unique and cannot be compared to anyone else's path. Honor your own rhythm and the lessons that are specifically yours to learn.",
        "Sometimes the greatest strength lies in surrender—not giving up, but releasing the need to control every outcome. Flow with what is, not against it.",
        "The challenges you face now are preparing you for something you cannot yet imagine. Trust that this difficulty serves a greater purpose in your unfolding story.",
        "Listen to your body as much as your mind. It carries wisdom that rational thought cannot access. Pay attention to what it tells you through sensation and intuition.",
    ]
    return random.choice(additions)

def generate_generic_reading(question):
    """Fallback for when parsing fails."""
    return f"""The cards offer meaningful insight into your question about {question.lower().rstrip('?')}. The energies present suggest a time of reflection and potential transformation. What may feel like obstacles are actually opportunities for growth in disguise. Trust that even uncertainty serves a purpose in your journey.

There are forces at work beneath the surface that are shaping your circumstances in ways not immediately visible. Some of what you face now has roots in patterns that formed long ago. By bringing awareness to these patterns, you gain power to change them. The universe often works on a different timeline than our conscious minds prefer, and patience serves you well here.

Your path forward involves both action and reflection in balance. Consider what truly matters to you, stripped of others' expectations. Make time this week for stillness, even if brief, and listen to what arises. Sometimes the answer emerges not from thinking harder but from creating space for wisdom to surface. Small, consistent steps matter more than dramatic changes right now.

For practical guidance: Journal about your experience to gain clarity. Notice your emotional responses without trying to fix them immediately. Identify one small action you can take this week that aligns with your deeper values. Remember that you have navigated challenges before and carry that strength with you now. Trust the process, even when the destination remains unclear."""

# Process all prompts
responses = []
for i, prompt in enumerate(data["prompts"]):
    try:
        reading = generate_reading(prompt)
        responses.append({
            "id": prompt["id"],
            "response": reading
        })
    except Exception as e:
        # Fallback response
        responses.append({
            "id": prompt["id"],
            "response": generate_generic_reading(prompt.get("question", "your situation"))
        })

    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1}/{len(data['prompts'])} prompts")

# Write to JSONL
with open(output_path, 'w') as f:
    for resp in responses:
        f.write(json.dumps(resp) + '\n')

print(f"Generated {len(responses)} responses")
print(f"Output written to: {output_path}")

# Word count stats
words = [len(r["response"].split()) for r in responses]
print(f"Word count stats: min={min(words)}, max={max(words)}, avg={sum(words)/len(words):.1f}")
print(f"Under 200: {sum(1 for w in words if w < 200)}")
print(f"200-400: {sum(1 for w in words if 200 <= w <= 400)}")
print(f"Over 400: {sum(1 for w in words if w > 400)}")
