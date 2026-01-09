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
    "Your question opens to {theme}.",
    "The cards speak directly to {theme}.",
    "What emerges here is a story of {theme}.",
    "This reading addresses {theme} with clarity.",
    "The path before you involves {theme}.",
]

# Card-specific powerful openings
CARD_OPENINGS = {
    "The Fool": "The Fool appears with an invitation to trust the unknown.",
    "The Magician": "The Magician arrives with all elements at your command.",
    "The High Priestess": "The High Priestess emerges from the threshold between knowing and mystery.",
    "The Empress": "The Empress brings her abundant, nurturing presence to your question.",
    "The Emperor": "The Emperor establishes his grounded authority in this reading.",
    "The Hierophant": "The Hierophant offers the wisdom of established paths.",
    "The Lovers": "The Lovers bring their energy of meaningful choice and true alignment.",
    "The Chariot": "The Chariot drives forward with unstoppable determination.",
    "Strength": "Strength appears with her message of gentle mastery over instinct.",
    "The Hermit": "The Hermit raises his lantern to illuminate your inner truth.",
    "Wheel of Fortune": "The Wheel turns, marking a significant moment of change.",
    "Justice": "Justice holds her scales, calling for honest accounting.",
    "The Hanged Man": "The Hanged Man hangs willingly, offering a radical shift in perspective.",
    "Death": "Death arrives as transformation's messenger, not an end but a passage.",
    "Temperance": "Temperance flows into your reading with patient, alchemical grace.",
    "The Devil": "The Devil appears to illuminate the chains you may not see clearly.",
    "The Tower": "The Tower strikes with its lightning revelation.",
    "The Star": "The Star shines with hope after difficulty.",
    "The Moon": "The Moon illuminates the path through intuition's realm.",
    "The Sun": "The Sun brightens everything with uncomplicated joy.",
    "Judgement": "Judgement sounds its trumpet, calling you to awakening.",
    "The World": "The World completes the circle with integration and fulfillment.",
    "Four of Cups": "The Four of Cups appears with a gentle but pointed message: abundance may already be present, but you're not seeing it clearly.",
    "Nine of Swords": "The Nine of Swords acknowledges the weight of your worry.",
    "Ten of Wands": "The Ten of Wands reveals the burden you've been carrying.",
    "Eight of Cups": "The Eight of Cups asks what you must walk away from to find what you seek.",
    "Three of Swords": "The Three of Swords appears without apology for the heartbreak it represents.",
    "Ace of Pentacles": "The Ace of Pentacles offers something tangible and real.",
    "Ace of Cups": "The Ace of Cups overflows with new emotional possibility.",
    "Ace of Wands": "The Ace of Wands sparks with fresh creative fire.",
    "Ace of Swords": "The Ace of Swords cuts through confusion with brilliant clarity.",
}

CLOSINGS = [
    "{insight}",
]

# Actionable endings per style guide
ACTIONABLE_ENDINGS = [
    "What cup is being extended that you haven't yet reached for?",
    "What specific opportunity is moving quickly toward you right now? That's where your attention belongs.",
    "What would it look like to trust yourself completely in this situation?",
    "What are you holding onto that has already completed its purpose?",
    "Where in your body do you feel the truth of this reading? That sensation holds information.",
    "What conversation have you been avoiding that this reading suggests you need to have?",
    "If you knew this situation would resolve in your favor, what would you do differently today?",
    "What small, concrete step could you take this week to honor what these cards reveal?",
    "What permission are you waiting for that you could give yourself right now?",
    "What would change if you stopped fighting against what is clearly ending?",
    "What has the cards' message awakened in you that was already stirring?",
    "Where might you be seeking complexity when simplicity is what's called for?",
    "What truth do you already know that you've been waiting for permission to act on?",
    "What relationship or pattern has outlived its purpose in your growth?",
    "What would courage look like in this situation, not dramatic but steady?",
    "Who in your life reflects the energy these cards are asking you to embody?",
    "What fear is disguising itself as practical concern?",
    "What would you create if you stopped waiting for perfect conditions?",
    "Where are you giving your power away that you could reclaim today?",
    "What decision have you actually already made that you're avoiding acknowledging?",
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

def should_mention_moon(moon_phase, cards, question):
    """Determine if moon phase naturally resonates with reading themes."""
    q_lower = question.lower()

    # Last Quarter + release themes
    if "Last Quarter" in moon_phase:
        release_words = ["release", "let go", "forgive", "end", "quit", "leave", "breakup"]
        if any(w in q_lower for w in release_words):
            return True
        # Check if cards suggest release
        card_names = [c.get("name", "").lower() for c in cards]
        if any("death" in c or "tower" in c or "eight of cups" in c for c in card_names):
            return True

    # Full Moon + clarity/culmination
    if "Full Moon" in moon_phase:
        clarity_words = ["clarity", "reveal", "truth", "see", "understand", "culminat"]
        if any(w in q_lower for w in clarity_words):
            return True

    # New Moon + beginnings
    if "New Moon" in moon_phase:
        begin_words = ["start", "begin", "new", "launch", "create", "fresh"]
        if any(w in q_lower for w in begin_words):
            return True
        card_names = [c.get("name", "").lower() for c in cards]
        if any("ace" in c or "fool" in c for c in card_names):
            return True

    return False

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
        theme = "your professional path and purposeful direction"
    elif "heal" in q_lower or "health" in q_lower or "body" in q_lower:
        theme = "healing and wholeness"
    elif "spiritual" in q_lower or "higher" in q_lower or "practice" in q_lower:
        theme = "spiritual growth and inner wisdom"
    elif "family" in q_lower or "parent" in q_lower or "mother" in q_lower or "father" in q_lower:
        theme = "family dynamics and inherited patterns"
    elif "money" in q_lower or "financial" in q_lower or "business" in q_lower or "debt" in q_lower:
        theme = "your relationship with resources and abundance"
    elif "release" in q_lower or "let go" in q_lower:
        theme = "release and transformation"
    elif "clarity" in q_lower or "understand" in q_lower or "see" in q_lower:
        theme = "clarity and deeper understanding"
    elif "block" in q_lower or "blocking" in q_lower or "stuck" in q_lower:
        theme = "what's blocking your flow"
    elif "energy" in q_lower or "vitality" in q_lower or "alive" in q_lower:
        theme = "vitality and life force"
    elif "breakup" in q_lower or "move on" in q_lower:
        theme = "transition and forward movement"
    elif "boundary" in q_lower or "boundaries" in q_lower:
        theme = "boundaries and self-protection"
    elif "fear" in q_lower or "afraid" in q_lower or "scared" in q_lower:
        theme = "facing what holds you back"
    elif "trust" in q_lower:
        theme = "trust and vulnerability"
    elif "decision" in q_lower or "choose" in q_lower or "choice" in q_lower:
        theme = "the decision before you"
    elif "purpose" in q_lower or "meaning" in q_lower:
        theme = "purpose and meaning"
    elif "authentic" in q_lower or "true self" in q_lower:
        theme = "authentic self-expression"

    paragraphs = []

    # Determine if moon phase should be mentioned
    mention_moon = should_mention_moon(moon_phase, cards, question)
    moon_phrase = random.choice(MOON_PHRASES.get(moon_phase, MOON_PHRASES["Full Moon"])) if mention_moon else None

    if spread_type == "daily":
        # Daily draw - shorter response (2-3 paragraphs)
        card = cards[0] if cards else None
        if card:
            card_name = card['name']
            # Use card-specific opening if available
            if card_name in CARD_OPENINGS:
                para1 = CARD_OPENINGS[card_name]
            else:
                para1 = f"{card_name} appears in your daily draw with a direct message."

            # Add context from card
            if card["context"] and "Meaning not available" not in card["context"]:
                para1 += f" {card['context']}"
            elif card["meaning"] and "Meaning not available" not in card["meaning"]:
                para1 += f" {card['meaning']}"

            # Second paragraph addresses the question
            para2 = f"You ask about {question.lower().rstrip('?')}. "
            if card["orientation"] == "reversed":
                para2 += f"The {card_name} reversed suggests this energy is currently blocked, internalized, or in process of transformation within you. Rather than flowing outward, it asks for inner attention. "
            else:
                para2 += f"With {card_name} upright, this energy is accessible and ready to work with you. "

            # Add moon context if relevant
            if moon_phrase:
                para2 += f"{moon_phrase}."

            # Closing with actionable insight
            closing = random.choice(ACTIONABLE_ENDINGS)

            paragraphs = [para1, para2, closing]

    elif spread_type == "three_card":
        # Three card spread (3-4 paragraphs) - weave cards into narrative
        first_card = cards[0] if cards else None
        card_name = first_card['name'] if first_card else ""

        # Opening with first card
        if card_name in CARD_OPENINGS:
            para1 = f"Your question about {question.lower().rstrip('?')} unfolds across a meaningful arc. {CARD_OPENINGS[card_name]}"
        else:
            para1 = f"Your question about {question.lower().rstrip('?')} unfolds through three cards that tell a connected story. {card_name} opens the reading"
            if first_card and first_card["orientation"] == "reversed":
                para1 += " in its reversed position, suggesting this energy is currently blocked or turning inward."
            else:
                para1 += ", setting the foundation for what follows."

        if first_card and first_card["context"] and "Meaning not available" not in first_card["context"]:
            para1 += f" {first_card['context']}"
        paragraphs.append(para1)

        # Second paragraph weaves remaining cards
        if len(cards) >= 2:
            second_card = cards[1]
            para2 = ""
            if second_card["position"] in ["Present", "Action", "Challenge"]:
                para2 = f"At the center of this reading, {second_card['name']} "
            else:
                para2 = f"Moving forward, {second_card['name']} "

            if second_card["orientation"] == "reversed":
                para2 += "appears reversed, indicating energy that is internalized or in process. "
            else:
                para2 += "brings its energy clearly into focus. "

            if second_card["context"] and "Meaning not available" not in second_card["context"]:
                para2 += second_card["context"]

            paragraphs.append(para2)

        # Third paragraph with outcome/resolution and synthesis
        if len(cards) >= 3:
            third_card = cards[2]
            para3 = f"The reading culminates with {third_card['name']}"
            if third_card["orientation"] == "reversed":
                para3 += " reversed"
            para3 += ". "

            if third_card["context"] and "Meaning not available" not in third_card["context"]:
                para3 += third_card["context"] + " "

            # Add moon phrase if relevant
            if moon_phrase:
                para3 += f"{moon_phrase}."

            paragraphs.append(para3)

        # Closing with actionable insight
        closing = random.choice(ACTIONABLE_ENDINGS)
        paragraphs.append(closing)

    else:
        # Larger spreads - Celtic Cross or custom (5-7 paragraphs)
        first_card = cards[0] if cards else None
        card_name = first_card['name'] if first_card else ""

        # Opening paragraph with first card
        if card_name in CARD_OPENINGS:
            para1 = f"Your question about {question.lower().rstrip('?')} calls for a comprehensive exploration. {CARD_OPENINGS[card_name]}"
        else:
            para1 = f"Your question about {question.lower().rstrip('?')} opens to a rich tapestry of influences. {card_name} begins the reading"
            if first_card and first_card["orientation"] == "reversed":
                para1 += " reversed, suggesting its energy is internalized or blocked."

        if first_card and first_card["context"] and "Meaning not available" not in first_card["context"]:
            para1 += f" {first_card['context']}"
        paragraphs.append(para1)

        # Group cards into narrative sections
        # Section 1: Foundation (cards 1-3)
        if len(cards) >= 3:
            para2 = ""
            for c in cards[1:3]:
                if c["context"] and "Meaning not available" not in c["context"]:
                    if c["orientation"] == "reversed":
                        para2 += f"{c['name']} reversed adds complexity: {c['context']} "
                    else:
                        para2 += f"{c['name']} contributes: {c['context']} "
            if para2:
                paragraphs.append(para2.strip())

        # Section 2: Influences (cards 4-6)
        if len(cards) > 3:
            mid_cards = cards[3:min(6, len(cards))]
            para3 = "Deeper influences shape this situation. "
            for c in mid_cards:
                if c["context"] and "Meaning not available" not in c["context"]:
                    para3 += f"{c['context']} "
            paragraphs.append(para3.strip())

        # Section 3: Guidance and outcome (cards 7+)
        if len(cards) > 6:
            late_cards = cards[6:]
            para4 = "Looking toward resolution, "
            for c in late_cards:
                if c["context"] and "Meaning not available" not in c["context"]:
                    if c["position"] == "Advice":
                        para4 += f"the cards advise: {c['context']} "
                    elif c["position"] == "Outcome":
                        para4 += f"The trajectory points toward {c['name']}: {c['context']} "
                    else:
                        para4 += f"{c['context']} "
            paragraphs.append(para4.strip())

        # Synthesis paragraph with moon if relevant
        reversed_cards = [c for c in cards if c["orientation"] == "reversed"]
        if len(reversed_cards) >= 2:
            rev_names = [c["name"] for c in reversed_cards[:3]]
            para5 = f"Several reversed cards appear in this spread: {', '.join(rev_names)}. These are not warnings but invitations to inner work. The energy exists but is turning inward, asking for attention before it can fully express outwardly."
            if moon_phrase:
                para5 += f" {moon_phrase}."
            paragraphs.append(para5)
        elif moon_phrase:
            paragraphs.append(moon_phrase + ".")

        # Final synthesis
        outcome_card = None
        for c in cards:
            if c["position"] in ["Outcome", "Future"]:
                outcome_card = c
                break
        if not outcome_card and cards:
            outcome_card = cards[-1]

        if outcome_card:
            para6 = f"The arc of this reading moves toward {outcome_card['name']}. "
            if outcome_card["context"] and "Meaning not available" not in outcome_card["context"]:
                para6 += outcome_card["context"]
            paragraphs.append(para6)

        # Closing with actionable insight
        closing = random.choice(ACTIONABLE_ENDINGS)
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

def main(start_batch=100, end_batch=200):
    batch_dir = Path("/home/user/taro/training/data/batches")
    output_dir = batch_dir / "responses"
    output_dir.mkdir(exist_ok=True)

    total_prompts = 0
    total_batches = 0

    # Process specified batch range
    for batch_num in range(start_batch, end_batch):
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
    return total_batches, total_prompts

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        main(start, end)
    else:
        main()
