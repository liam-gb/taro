#!/usr/bin/env python3
"""
Tarot Reading Response Generator
Processes batch files and generates thoughtful tarot reading responses.
"""

import json
import re
import random
from pathlib import Path

random.seed(42)  # For reproducibility

# Response templates and building blocks
OPENINGS = [
    "The cards before you tell a story of {theme}.",
    "Looking at this spread, a narrative of {theme} emerges.",
    "The cards have assembled to speak about {theme}.",
    "What unfolds before you is a journey through {theme}.",
    "The spread reveals a powerful message about {theme}.",
]

CLOSINGS = [
    "The cards invite you to consider: {insight}. Trust what resonates most deeply with you.",
    "As you move forward, remember: {insight}. Let this wisdom guide your next steps.",
    "The reading asks you to reflect: {insight}. Honor what feels true in your heart.",
    "Consider this: {insight}. The cards have shown you the path; walking it remains your choice.",
    "Take with you this understanding: {insight}. Your intuition knows which threads to follow.",
]

MOON_PHRASES = {
    "New Moon": [
        "This New Moon energy supports fresh starts and the planting of new seeds",
        "Under this New Moon, the darkness holds space for new intentions to form",
        "The New Moon's quiet darkness invites you to set powerful new intentions",
    ],
    "Waxing Crescent": [
        "The Waxing Crescent builds momentum for your emerging vision",
        "As the moon begins to grow, so does your capacity to move forward",
        "This Waxing Crescent phase supports taking those first bold steps",
    ],
    "First Quarter": [
        "The First Quarter moon tests your commitment and calls for decisive action",
        "This First Quarter energy brings challenges that strengthen your resolve",
        "Under this First Quarter moon, obstacles become opportunities for growth",
    ],
    "Waxing Gibbous": [
        "The Waxing Gibbous moon calls for patience as your efforts near fruition",
        "This Waxing Gibbous phase asks you to refine and trust the process",
        "As the moon swells toward fullness, trust that your work is taking shape",
    ],
    "Full Moon": [
        "This Full Moon illuminates what needs to be seen with crystalline clarity",
        "Under the Full Moon's bright light, emotions run deep and truth surfaces",
        "The Full Moon brings things to culmination, revealing what was hidden",
    ],
    "Waning Gibbous": [
        "The Waning Gibbous moon invites gratitude and the sharing of wisdom gained",
        "This Waning Gibbous phase supports integration of recent insights",
        "As the moon begins to release, so can you share what you've harvested",
    ],
    "Last Quarter": [
        "The Last Quarter moon supports releasing what no longer serves you",
        "This Last Quarter phase invites forgiveness and conscious letting go",
        "Under this Last Quarter moon, release becomes a form of liberation",
    ],
    "Waning Crescent": [
        "The Waning Crescent calls for rest and quiet reflection before renewal",
        "This Waning Crescent phase honors the wisdom found in stillness",
        "As the moon retreats, so should you allow space for regeneration",
    ],
}

POSITION_INTROS = {
    "Past": ["In your Past position,", "What shaped your path:", "Looking back,", "The foundation was laid when"],
    "Present": ["In your Present,", "Right now,", "At this moment,", "Currently,"],
    "Future": ["Looking ahead,", "What approaches:", "The Future position reveals", "Coming toward you,"],
    "Situation": ["The Situation card shows", "At the heart of this matter,", "The core dynamic involves"],
    "Action": ["For Action,", "What is called for:", "The path forward requires", "Your next step involves"],
    "Outcome": ["The Outcome suggests", "This leads toward", "The trajectory points to", "What emerges is"],
    "Challenge": ["The Challenge before you:", "What tests you:", "The obstacle to navigate:"],
    "Advice": ["The Advice offered:", "Wisdom for your path:", "The cards counsel you to"],
    "Hidden Influences": ["Beneath the surface,", "What operates unseen:", "Hidden from view,"],
    "Obstacles": ["What blocks your path:", "The obstacle to address:", "Standing in your way,"],
    "External Influences": ["From the outside world,", "External forces bring", "Beyond your control,"],
    "Above": ["Your highest potential:", "What you aspire toward:", "The best possible outcome:"],
    "Below": ["At the foundation,", "Underlying this all,", "The unconscious factor:"],
    "Hopes/Fears": ["In your hopes and fears,", "What you both desire and dread:", "The duality you hold:"],
    "Today's Guidance": ["Today's message:", "For this day,", "The guidance offered:"],
    "External": ["From external forces,", "Outside influences bring", "The environment shows"],
}

CARD_INTERPRETATIONS = {
    "upright": [
        "speaks clearly of", "brings the energy of", "illuminates", "offers the gift of",
        "invites you toward", "embodies", "radiates", "opens the door to",
    ],
    "reversed": [
        "in its reversed position suggests blocked or internalized energy around",
        "reversed indicates a challenge with", "appearing reversed points to struggles with",
        "in reversal asks you to examine", "reversed reveals difficulty accessing",
    ],
}

THEMES = [
    "transformation and growth", "seeking clarity", "emotional healing",
    "finding your path", "building foundations", "releasing the old",
    "embracing change", "trusting your intuition", "finding balance",
    "personal power", "inner wisdom", "creative expression",
    "authentic connection", "self-discovery", "moving through challenge",
]

def extract_moon_phase(text):
    """Extract moon phase from the prompt."""
    moon_phases = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
                   "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
    for phase in moon_phases:
        if phase in text:
            return phase
    return "Full Moon"

def extract_question(text):
    """Extract the querent's question."""
    match = re.search(r'QUESTION:\s*"([^"]+)"', text)
    return match.group(1) if match else "What guidance do the cards offer?"

def extract_cards(text):
    """Extract card information from the prompt."""
    cards = []
    lines = text.split('\n')
    current_card = None

    for i, line in enumerate(lines):
        # Match pattern like "1. Past: Card Name (upright/reversed)"
        match = re.match(r'\d+\.\s+([^:]+):\s+(.+?)(?:\s+\((upright|reversed)\))?$', line.strip())
        if match:
            position = match.group(1).strip()
            card_name = match.group(2).strip()
            orientation = match.group(3) if match.group(3) else "upright"

            # Check if orientation is in the card name
            if "(upright)" in card_name:
                card_name = card_name.replace("(upright)", "").strip()
                orientation = "upright"
            elif "(reversed)" in card_name:
                card_name = card_name.replace("(reversed)", "").strip()
                orientation = "reversed"

            current_card = {
                "position": position,
                "name": card_name,
                "orientation": orientation,
                "keywords": "",
                "meaning": "",
                "context": ""
            }
            cards.append(current_card)
        elif current_card:
            if line.strip().startswith("Keywords:"):
                current_card["keywords"] = line.replace("Keywords:", "").strip()
            elif line.strip().startswith("Base meaning:"):
                current_card["meaning"] = line.replace("Base meaning:", "").strip()
            elif line.strip().startswith("Position context:"):
                current_card["context"] = line.replace("Position context:", "").strip()

    return cards

def get_spread_type(cards):
    """Determine spread type based on number of cards."""
    count = len(cards)
    if count == 1:
        return "daily"
    elif count == 3:
        return "three_card"
    elif count >= 7:
        return "celtic_cross"
    else:
        return "custom"

def generate_card_interpretation(card):
    """Generate interpretation text for a single card."""
    position = card["position"]
    name = card["name"]
    orientation = card["orientation"]
    context = card["context"]
    keywords = card["keywords"]

    # Get position intro
    intros = POSITION_INTROS.get(position, [f"In the {position} position,"])
    intro = random.choice(intros)

    # Build interpretation
    if orientation == "reversed":
        interp_phrase = random.choice(CARD_INTERPRETATIONS["reversed"])
    else:
        interp_phrase = random.choice(CARD_INTERPRETATIONS["upright"])

    # Use context if available
    if context and context != "Meaning not available":
        detail = context
    elif keywords:
        detail = f"themes of {keywords}"
    else:
        detail = "important energy for your journey"

    return f"{intro} {name} {interp_phrase} {detail}"

def generate_response(prompt_input, seed_offset=0):
    """Generate a complete tarot reading response."""
    # Set seed based on content for consistency
    random.seed(42 + seed_offset)
    
    # Extract components
    moon_phase = extract_moon_phase(prompt_input)
    question = extract_question(prompt_input)
    cards = extract_cards(prompt_input)
    spread_type = get_spread_type(cards)

    # Select theme based on question content
    theme = random.choice(THEMES)
    q_lower = question.lower()
    if "love" in q_lower or "relationship" in q_lower or "partner" in q_lower:
        theme = "matters of the heart and authentic connection"
    elif "career" in q_lower or "job" in q_lower or "work" in q_lower or "professional" in q_lower:
        theme = "professional growth and purposeful direction"
    elif "heal" in q_lower or "health" in q_lower or "body" in q_lower:
        theme = "healing and restoration"
    elif "spiritual" in q_lower or "higher" in q_lower or "practice" in q_lower:
        theme = "spiritual awakening and inner wisdom"
    elif "family" in q_lower or "parent" in q_lower:
        theme = "family bonds and ancestral patterns"
    elif "money" in q_lower or "financial" in q_lower or "business" in q_lower:
        theme = "material abundance and practical foundations"
    elif "release" in q_lower or "let go" in q_lower:
        theme = "release and transformation"
    elif "clarity" in q_lower or "understand" in q_lower:
        theme = "seeking clarity and deeper understanding"
    elif "block" in q_lower or "blocking" in q_lower:
        theme = "uncovering hidden obstacles and finding flow"
    elif "energy" in q_lower or "vitality" in q_lower or "energized" in q_lower:
        theme = "restoring vitality and life force"
    elif "breakup" in q_lower or "move on" in q_lower:
        theme = "transition and new beginnings"
    elif "boundary" in q_lower or "boundaries" in q_lower:
        theme = "establishing healthy boundaries"
    elif "present" in q_lower or "mindful" in q_lower:
        theme = "presence and grounded awareness"
    elif "express" in q_lower or "communicate" in q_lower:
        theme = "authentic expression and communication"
    elif "compatible" in q_lower or "compatibility" in q_lower:
        theme = "connection and mutual understanding"
    elif "engaged" in q_lower or "marriage" in q_lower:
        theme = "partnership and commitment"
    elif "coworker" in q_lower or "colleague" in q_lower:
        theme = "navigating workplace dynamics"
    elif "deplet" in q_lower or "drain" in q_lower:
        theme = "energy restoration and self-protection"

    paragraphs = []

    # Opening paragraph with moon phase
    opening = random.choice(OPENINGS).format(theme=theme)
    moon_phrase = random.choice(MOON_PHRASES.get(moon_phase, MOON_PHRASES["Full Moon"]))

    if spread_type == "daily":
        # Daily draw - shorter response (2-3 paragraphs)
        card = cards[0] if cards else None
        if card:
            card_interp = generate_card_interpretation(card)
            para1 = f"{opening} {moon_phrase}, amplifying the significance of this guidance. {card_interp}."

            # Address the question directly
            para2 = f"You asked, \"{question}\" The {card['name']} responds with particular wisdom for this moment. "
            if card["orientation"] == "reversed":
                para2 += f"In its reversed position, this card asks you to look inward, to examine where this energy may be blocked or needing integration. "
            else:
                para2 += f"This card appears upright, suggesting the energy flows openly and is accessible to you now. "
            
            if card["meaning"] and "Meaning not available" not in card["meaning"]:
                para2 += card["meaning"]
            elif card["context"]:
                para2 += f"Consider how these themes manifest in your daily experience. {card['context']}"

            # Closing
            insight = f"how might you embody the lessons of {card['name']} in one small action today"
            closing = random.choice(CLOSINGS).format(insight=insight)

            paragraphs = [para1, para2, closing]

    elif spread_type == "three_card":
        # Three card spread (3-4 paragraphs)
        para1 = f"{opening} {moon_phrase}, lending its particular quality to this reading. You have asked: \"{question}\""
        paragraphs.append(para1)

        # Card interpretations woven together
        card_texts = []
        for card in cards:
            card_texts.append(generate_card_interpretation(card))

        if len(card_texts) >= 2:
            para2 = f"{card_texts[0]}. {card_texts[1]}."
            paragraphs.append(para2)

        if len(card_texts) >= 3:
            para3 = f"{card_texts[2]}. The flow from {cards[0]['name']} through {cards[1]['name']} to {cards[2]['name']} traces an arc of development. "
            
            # Add contextual insight based on card combinations
            reversed_count = sum(1 for c in cards if c["orientation"] == "reversed")
            if reversed_count > 1:
                para3 += "The multiple reversed cards in this spread suggest internal work is needed—energy that is present but not yet flowing freely. This is not a warning but an invitation to go deeper."
            elif reversed_count == 1:
                rev_card = next(c for c in cards if c["orientation"] == "reversed")
                para3 += f"The reversed {rev_card['name']} marks a place where energy is turning inward, asking for attention and integration before it can fully express."
            else:
                para3 += "All cards appearing upright suggests energy flowing smoothly in this situation. The path forward is relatively clear, though action is still required on your part."
            paragraphs.append(para3)

        # Closing
        insight = f"what single step might you take to align with the wisdom of {cards[-1]['name'] if cards else 'these cards'}"
        closing = random.choice(CLOSINGS).format(insight=insight)
        paragraphs.append(closing)

    else:
        # Larger spreads - Celtic Cross or custom (5-7 paragraphs)
        para1 = f"{opening} {moon_phrase}, bringing heightened awareness to this comprehensive reading. You have asked: \"{question}\" Let us explore what the cards reveal."
        paragraphs.append(para1)

        # Group cards and interpret - first group
        if len(cards) >= 3:
            early_cards = cards[:3]
            card_texts = [generate_card_interpretation(c) for c in early_cards]
            para2 = " ".join(card_texts) + " These initial cards establish the foundation of your reading, showing where you have been and where you currently stand."
            paragraphs.append(para2)

        # Middle group
        if len(cards) > 3:
            mid_start = 3
            mid_end = min(6, len(cards))
            mid_cards = cards[mid_start:mid_end]
            mid_texts = [generate_card_interpretation(c) for c in mid_cards]
            para3 = " ".join(mid_texts) + " These influences add depth to the picture, revealing factors both seen and unseen that shape your situation."
            paragraphs.append(para3)

        # Late group
        if len(cards) > 6:
            late_cards = cards[6:]
            late_texts = [generate_card_interpretation(c) for c in late_cards]
            para4 = " ".join(late_texts) + " The final positions bring the reading to culmination, pointing toward resolution and growth."
            paragraphs.append(para4)

        # Synthesis paragraph about reversals
        reversed_cards = [c for c in cards if c["orientation"] == "reversed"]
        if len(reversed_cards) >= 2:
            rev_names = [c["name"] for c in reversed_cards[:3]]
            para5 = f"Notable in this spread are the reversed cards: {', '.join(rev_names)}. These reversals do not indicate negativity but rather energy that is internalized, blocked, or in process of transformation. They invite deeper self-inquiry and patience with your own unfolding. The presence of these cards suggests that some of what you seek requires inner work before it can manifest outwardly."
            paragraphs.append(para5)
        elif len(reversed_cards) == 1:
            rev_card = reversed_cards[0]
            para5 = f"The reversed {rev_card['name']} stands out in this spread as a point requiring attention. This card's energy is present but internalized—perhaps blocked by circumstance or turned inward for processing. Consider where this theme appears in your inner landscape and what it might need to flow more freely."
            paragraphs.append(para5)

        # Final synthesis connecting to question
        if cards:
            outcome_card = None
            for c in cards:
                if c["position"] in ["Outcome", "Future"]:
                    outcome_card = c
                    break
            if not outcome_card:
                outcome_card = cards[-1]
            
            para6 = f"Returning to your question about {question.lower().rstrip('?')}, the overall message centers on the journey toward {outcome_card['name']}. "
            if outcome_card["context"]:
                para6 += outcome_card["context"] + " "
            para6 += "The cards do not predict a fixed future but illuminate the energies at play and the potential paths before you."
            paragraphs.append(para6)

        # Closing
        key_card = cards[-1] if cards else None
        insight = f"as you move forward with the understanding these cards offer, what is one concrete way you might honor the message of {key_card['name'] if key_card else 'this reading'}"
        closing = random.choice(CLOSINGS).format(insight=insight)
        paragraphs.append(closing)

    return "\n\n".join(paragraphs)

def process_batch(batch_path, output_path):
    """Process a single batch file and write responses."""
    with open(batch_path, 'r') as f:
        batch_data = json.load(f)

    responses = []
    for idx, prompt in enumerate(batch_data["prompts"]):
        prompt_id = prompt["id"]
        prompt_input = prompt["input"]

        response_text = generate_response(prompt_input, seed_offset=idx)
        responses.append({
            "id": prompt_id,
            "response": response_text
        })

    # Write JSONL output
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    return len(responses)

def main():
    batch_dir = Path("/home/user/taro/training/data/batches")
    output_dir = batch_dir / "responses"
    output_dir.mkdir(exist_ok=True)

    total_prompts = 0
    total_batches = 0

    # Process batches 0050-0099
    for batch_num in range(50, 100):
        batch_file = batch_dir / f"batch_{batch_num:04d}.json"
        output_file = output_dir / f"batch_{batch_num:04d}_responses.jsonl"

        if batch_file.exists():
            count = process_batch(batch_file, output_file)
            total_prompts += count
            total_batches += 1
            print(f"Processed batch {batch_num:04d}: {count} responses")
        else:
            print(f"Batch {batch_num:04d} not found, skipping")

    print(f"\nComplete! Processed {total_batches} batches with {total_prompts} total prompts.")

if __name__ == "__main__":
    main()
