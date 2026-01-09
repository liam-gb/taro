#!/usr/bin/env python3
"""Generate tarot reading responses for training data batches."""

import json
import os
import re
import random
from pathlib import Path

INPUT_DIR = Path("/home/user/taro/training/data/batches_new")
OUTPUT_DIR = INPUT_DIR / "responses"

# Opening phrases for readings
OPENINGS = [
    "The cards reveal",
    "What emerges from this spread is",
    "Your reading opens with",
    "The story the cards tell begins with",
    "Looking at what has been drawn,",
    "The pattern before you shows",
    "These cards paint a picture of",
    "What stands out immediately is",
    "This spread speaks to",
    "The cards have drawn forward",
]

# Transition phrases
TRANSITIONS = [
    "Moving deeper into the reading,",
    "This connects to",
    "Building on this foundation,",
    "The next layer reveals",
    "Alongside this energy,",
    "What makes this particularly significant is",
    "The interplay between these forces shows",
    "This dynamic shifts as we consider",
    "Weaving through this pattern,",
    "The thread continues as",
]


def parse_prompt(input_text):
    """Extract key information from the prompt."""
    info = {
        "timing": "",
        "question": "",
        "cards": [],
        "spread_type": "unknown",
        "combinations": [],
    }

    # Extract timing/moon phase
    timing_match = re.search(r"TIMING:\s*([^\n]+)", input_text)
    if timing_match:
        info["timing"] = timing_match.group(1).strip()

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        info["question"] = question_match.group(1).strip()

    # Extract cards with their details
    card_sections = re.split(r"\n\d+\.\s+", input_text)[1:]  # Split by numbered items
    
    for section in card_sections:
        if not section.strip():
            continue
        
        # Parse position and card
        header_match = re.match(r"([^:]+):\s+([^\(]+)\s*\((\w+)\)", section)
        if not header_match:
            continue
            
        position = header_match.group(1).strip()
        card_name = header_match.group(2).strip()
        orientation = header_match.group(3).strip()

        # Get position context
        context_match = re.search(r"Position context:\s+([^\n]+)", section)
        context = context_match.group(1).strip() if context_match else ""
        
        # Get base meaning if available
        base_match = re.search(r"Base meaning:\s+([^\n]+)", section)
        base_meaning = base_match.group(1).strip() if base_match else ""

        info["cards"].append({
            "position": position,
            "name": card_name,
            "orientation": orientation,
            "context": context,
            "base_meaning": base_meaning,
        })

    # Determine spread type by card count
    card_count = len(info["cards"])
    if card_count == 1:
        info["spread_type"] = "daily"
    elif card_count <= 3:
        info["spread_type"] = "three_card"
    elif card_count <= 7:
        info["spread_type"] = "seven_card"
    else:
        info["spread_type"] = "celtic_cross"

    # Extract combinations
    combo_section = re.search(r"Card Combinations:\n((?:- [^\n]+\n?)+)", input_text)
    if combo_section:
        combos = re.findall(r"- ([^:]+):\s+([^\n]+)", combo_section.group(1))
        info["combinations"] = combos

    return info


def get_moon_integration(timing, cards, question):
    """Determine if moon phase should be mentioned and how."""
    timing_lower = timing.lower()
    question_lower = question.lower()

    # Build card themes string
    card_themes = " ".join([c["context"].lower() for c in cards])

    # Last Quarter + release themes
    if "last quarter" in timing_lower:
        if any(word in card_themes for word in ["release", "letting go", "end", "forgive", "transform", "surrender"]):
            return "This Last Quarter moon supports the releasing energy present in your reading. "
        if any(word in question_lower for word in ["release", "let go", "move on", "forgive"]):
            return "The Last Quarter moon amplifies your readiness to release what no longer serves. "

    # Full Moon + clarity/culmination
    if "full moon" in timing_lower:
        if any(word in card_themes for word in ["clarity", "complete", "culminat", "reveal", "truth", "illuminate"]):
            return "Under this Full Moon, the clarity emerging from your reading intensifies. "
        if any(word in question_lower for word in ["clarity", "understand", "see", "reveal"]):
            return "The Full Moon illuminates what has been hidden, and your cards echo this revelation. "

    # New Moon + beginnings
    if "new moon" in timing_lower:
        if any(word in card_themes for word in ["begin", "new", "start", "seed", "potential", "fresh"]):
            return "This New Moon creates fertile ground for the new beginnings your cards describe. "

    # Waning phases + release/reflection
    if "waning" in timing_lower:
        if any(word in card_themes for word in ["release", "reflect", "integrate", "wisdom", "rest"]):
            return "The waning moon supports the inward focus your reading suggests. "

    return ""


def generate_daily_reading(info):
    """Generate a 2-3 paragraph daily draw reading."""
    card = info["cards"][0]
    card_name = card["name"]
    orientation = card["orientation"]
    context = card["context"]
    question = info["question"]
    base_meaning = card.get("base_meaning", "")

    is_reversed = orientation == "reversed"
    moon_text = get_moon_integration(info["timing"], info["cards"], question)

    # Build opening paragraph
    if is_reversed:
        para1 = f"{card_name} appears reversed today, bringing a message that asks you to look beneath the surface. "
        para1 += f"Rather than expressing its energy outwardly, this card points to something working internally or encountering resistance. {context}"
    else:
        if base_meaning and "Meaning not available" not in base_meaning:
            para1 = f"{card_name} arrives today with clear guidance. {base_meaning[:200]}... {context}"
        else:
            para1 = f"{card_name} arrives today with a direct message for you. {context}"

    # Second paragraph - connect to question
    para2 = moon_text if moon_text else ""
    question_clean = question.lower().rstrip('?').strip('"')
    
    if is_reversed:
        para2 += f"When you ask \"{question_clean},\" this reversed {card_name} suggests the answer lies in examining what might be blocked or internalized. "
        para2 += "Sometimes the reversal points not to something wrong, but to energy that needs conscious attention before it can flow freely outward. Consider where you might be holding back or where circumstances have created resistance."
    else:
        para2 += f"In response to your question about {question_clean}, {card_name} offers both validation and direction. "
        para2 += "This energy is actively present in your life right now. The invitation is to recognize it and work with it consciously rather than letting it operate in the background."

    # Closing with actionable insight
    closing_options = [
        f"What aspect of {card_name}'s message feels most alive in your situation today?",
        "What would it look like to act on this guidance in one concrete way?",
        f"Where might you already be experiencing what {card_name} describes, without having named it?",
        "Consider: what would change if you fully trusted this message?",
    ]
    para3 = random.choice(closing_options)

    return f"{para1}\n\n{para2}\n\n{para3}"


def generate_three_card_reading(info):
    """Generate a 3-4 paragraph three-card spread reading."""
    cards = info["cards"]
    question = info["question"]
    moon_text = get_moon_integration(info["timing"], cards, question)
    combinations = info.get("combinations", [])

    # Opening - establish the arc
    question_clean = question.lower().rstrip('?').strip('"')
    opening = random.choice(OPENINGS)
    
    first_card = cards[0]
    para1 = f"{opening} a meaningful arc in response to your question about {question_clean}. "
    
    if first_card["orientation"] == "reversed":
        para1 += f"Beginning with {first_card['name']} reversed in the {first_card['position']} position, "
        para1 += f"we see energy that has been internalized or blocked. {first_card['context']}"
    else:
        para1 += f"Beginning with {first_card['name']} in the {first_card['position']} position, "
        para1 += f"the foundation is set. {first_card['context']}"

    # Middle cards - weave the narrative
    para2 = random.choice(TRANSITIONS) + " "
    
    if len(cards) >= 2:
        second_card = cards[1]
        if second_card["orientation"] == "reversed":
            para2 += f"{second_card['name']} reversed occupies your {second_card['position']} position. "
            para2 += f"This reversal indicates energy working beneath the surface or encountering some friction. {second_card['context']} "
        else:
            para2 += f"{second_card['name']} in your {second_card['position']} position shows the current dynamic. {second_card['context']} "

    if len(cards) >= 3:
        third_card = cards[2]
        if third_card["orientation"] == "reversed":
            para2 += f"This flows toward {third_card['name']} reversed in the {third_card['position']} position, suggesting a trajectory still in formation. {third_card['context']}"
        else:
            para2 += f"This flows toward {third_card['name']} in the {third_card['position']} position. {third_card['context']}"

    # Integration - how cards relate
    para3 = moon_text if moon_text else ""
    
    if combinations:
        para3 += f"The combination of {combinations[0][0]} creates a particularly significant pattern: {combinations[0][1].lower()} "
    
    para3 += "What connects these cards is a story of movement and evolution. Each position builds on what came before, suggesting that your situation is neither static nor random but part of a meaningful unfolding."

    # Closing with actionable guidance
    closing_options = [
        "Given this arc from beginning to end, what single step feels most important right now?",
        f"What cup is being extended that you haven't yet reached for?",
        "Where do you see the central tension of this reading playing out in your daily life?",
        "What would need to shift for the outcome card's energy to express at its highest?",
    ]
    para4 = random.choice(closing_options)

    return f"{para1}\n\n{para2}\n\n{para3}\n\n{para4}"


def generate_seven_card_reading(info):
    """Generate a 4-5 paragraph seven-card spread reading."""
    cards = info["cards"]
    question = info["question"]
    moon_text = get_moon_integration(info["timing"], cards, question)
    combinations = info.get("combinations", [])

    question_clean = question.lower().rstrip('?').strip('"')
    
    # Opening
    opening = random.choice(OPENINGS)
    para1 = f"{opening} a rich and layered response to your question: \"{question}\" "

    if cards:
        first_card = cards[0]
        if first_card["orientation"] == "reversed":
            para1 += f"{first_card['name']} reversed in the {first_card['position']} position immediately draws attention, suggesting blocked or internalized energy. {first_card['context']}"
        else:
            para1 += f"{first_card['name']} in the {first_card['position']} position establishes the central theme. {first_card['context']}"

    # Core dynamics
    para2 = "The central tension in this reading emerges from several key cards working together. "
    
    for card in cards[1:4]:
        if card["orientation"] == "reversed":
            para2 += f"{card['name']} reversed in {card['position']} indicates energy still working itself out. {card['context']} "
        else:
            para2 += f"{card['name']} in {card['position']} adds another dimension: {card['context']} "

    # Hidden/external influences
    hidden = [c for c in cards if "hidden" in c["position"].lower()]
    external = [c for c in cards if "external" in c["position"].lower()]
    
    para3 = ""
    if hidden or external:
        para3 = "Looking at influences operating beyond immediate awareness, "
        for hc in hidden[:1]:
            if hc["orientation"] == "reversed":
                para3 += f"{hc['name']} reversed as a hidden influence suggests {hc['context'].lower()} "
            else:
                para3 += f"{hc['name']} as a hidden influence reveals {hc['context'].lower()} "
        for ec in external[:1]:
            if ec["orientation"] == "reversed":
                para3 += f"Meanwhile, {ec['name']} reversed from outside indicates {ec['context'].lower()}"
            else:
                para3 += f"From outside, {ec['name']} shows {ec['context'].lower()}"
    
    if combinations:
        para3 += f" The synergy between {combinations[0][0]} intensifies this reading: {combinations[0][1].lower()}"

    # Advice and outcome
    para4 = moon_text if moon_text else ""
    advice = [c for c in cards if "advice" in c["position"].lower()]
    outcome = [c for c in cards if "outcome" in c["position"].lower()]

    if advice:
        ac = advice[0]
        if ac["orientation"] == "reversed":
            para4 += f"The guidance here comes through {ac['name']} reversed, asking you to examine {ac['context'].lower()} "
        else:
            para4 += f"The guidance is clear: {ac['name']} advises you to {ac['context'].lower()} "

    if outcome:
        oc = outcome[0]
        if oc["orientation"] == "reversed":
            para4 += f"This path leads toward {oc['name']} reversed as your outcome, indicating {oc['context'].lower()}"
        else:
            para4 += f"This path leads toward {oc['name']} as your outcome, where {oc['context'].lower()}"

    # Closing
    closing_options = [
        "What specific opportunity is moving quickly toward you right now? That's where your attention belongs.",
        "Which card in this spread speaks most directly to where you are today?",
        "What would it mean to fully trust the advice this reading offers?",
        "Consider the obstacles shown here: what one thing could you do this week to work with rather than against them?",
    ]
    para5 = random.choice(closing_options)

    return f"{para1}\n\n{para2}\n\n{para3}\n\n{para4}\n\n{para5}"


def generate_celtic_cross_reading(info):
    """Generate a 5-7 paragraph Celtic Cross reading."""
    cards = info["cards"]
    question = info["question"]
    moon_text = get_moon_integration(info["timing"], cards, question)
    combinations = info.get("combinations", [])

    # Build card lookup
    def find_card(position_keyword):
        for c in cards:
            if position_keyword.lower() in c["position"].lower():
                return c
        return None

    # Opening
    para1 = f"Your Celtic Cross spread offers a comprehensive view of your question: \"{question}\" "
    para1 += "This ten-card spread reveals the forces that have shaped this moment, what supports and challenges you, and where the energy naturally flows."

    # Present and challenge
    present = find_card("present") or find_card("situation")
    challenge = find_card("challenge") or find_card("obstacle")
    
    para2 = ""
    if present:
        if present["orientation"] == "reversed":
            para2 = f"At the heart of your reading, {present['name']} reversed occupies the central position. {present['context']} "
        else:
            para2 = f"At the heart of your reading, {present['name']} occupies the central position. {present['context']} "
    
    if challenge:
        if challenge["orientation"] == "reversed":
            para2 += f"Crossing this, {challenge['name']} reversed represents the core challenge. {challenge['context']}"
        else:
            para2 += f"Crossing this, {challenge['name']} represents the core challenge. {challenge['context']}"

    # Past and future
    past = find_card("past")
    future = find_card("future")
    
    para3 = "The timeline stretches "
    if past:
        if past["orientation"] == "reversed":
            para3 += f"from {past['name']} reversed in your past, where {past['context'].lower()}, "
        else:
            para3 += f"from {past['name']} in your past, where {past['context'].lower()}, "
    
    if future:
        if future["orientation"] == "reversed":
            para3 += f"toward {future['name']} reversed approaching in your future, indicating {future['context'].lower()}"
        else:
            para3 += f"toward {future['name']} in your future, pointing to {future['context'].lower()}"

    # Above, below, hopes/fears
    above = find_card("above")
    below = find_card("below")
    hopes = find_card("hopes") or find_card("fears")
    
    para4 = ""
    if above:
        if above["orientation"] == "reversed":
            para4 = f"Your highest aspiration here, {above['name']} reversed, suggests {above['context'].lower()} "
        else:
            para4 = f"Your highest aspiration here, {above['name']}, points toward {above['context'].lower()} "
    
    if below:
        if below["orientation"] == "reversed":
            para4 += f"The foundation beneath everything, {below['name']} reversed, reveals {below['context'].lower()} "
        else:
            para4 += f"The foundation beneath everything, {below['name']}, reveals {below['context'].lower()} "
    
    if hopes:
        para4 += f"In the realm of hopes and fears, {hopes['context']}"

    # External and advice
    external = find_card("external")
    advice = find_card("advice")
    
    para5 = moon_text if moon_text else ""
    if external:
        if external["orientation"] == "reversed":
            para5 += f"From outside your immediate sphere, {external['name']} reversed shows {external['context'].lower()} "
        else:
            para5 += f"From outside your immediate sphere, {external['name']} shows {external['context'].lower()} "
    
    if advice:
        if advice["orientation"] == "reversed":
            para5 += f"The advice offered through {advice['name']} reversed asks you to examine {advice['context'].lower()}"
        else:
            para5 += f"The advice offered through {advice['name']} is direct: {advice['context'].lower()}"
    
    if combinations:
        para5 += f" The combination of {combinations[0][0]} amplifies this reading: {combinations[0][1].lower()}"

    # Outcome
    outcome = find_card("outcome")
    para6 = ""
    if outcome:
        if outcome["orientation"] == "reversed":
            para6 = f"The reading culminates in {outcome['name']} reversed as your likely outcome. {outcome['context']} This reversal suggests the final form is still responsive to the choices you make from here."
        else:
            para6 = f"The reading culminates in {outcome['name']} as your likely outcome. {outcome['context']} This card indicates the direction energy is naturally flowing, though conscious engagement with the advice can shape how this manifests."

    # Closing
    closing_options = [
        "Given everything this spread reveals, what is the single most important insight you're taking with you?",
        "Which card surprised you most, and what might that surprise be telling you?",
        "What would it look like to honor both the advice and the outcome this reading describes?",
        "Where in your daily life do you see the central pattern of this reading already playing out?",
    ]
    para7 = random.choice(closing_options)

    return f"{para1}\n\n{para2}\n\n{para3}\n\n{para4}\n\n{para5}\n\n{para6}\n\n{para7}"


def generate_response(info):
    """Generate appropriate response based on spread type."""
    spread_type = info["spread_type"]

    if spread_type == "daily":
        return generate_daily_reading(info)
    elif spread_type == "three_card":
        return generate_three_card_reading(info)
    elif spread_type == "seven_card":
        return generate_seven_card_reading(info)
    else:
        return generate_celtic_cross_reading(info)


def process_batch(batch_num):
    """Process a single batch file."""
    batch_id = f"{batch_num:04d}"
    input_file = INPUT_DIR / f"batch_{batch_id}.json"
    output_file = OUTPUT_DIR / f"batch_{batch_id}_responses.jsonl"

    if not input_file.exists():
        return 0, f"Input file not found: {input_file}"

    with open(input_file, "r") as f:
        batch_data = json.load(f)

    prompts = batch_data.get("prompts", [])
    responses = []

    for prompt in prompts:
        prompt_id = prompt["id"]
        input_text = prompt["input"]

        info = parse_prompt(input_text)
        response_text = generate_response(info)

        responses.append({
            "id": prompt_id,
            "response": response_text
        })

    with open(output_file, "w") as f:
        for resp in responses:
            f.write(json.dumps(resp) + "\n")

    return len(responses), None


def main():
    """Process all batches from 0000 to 0099."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_processed = 0
    successful_batches = 0
    failed_batches = []

    for batch_num in range(100):
        count, error = process_batch(batch_num)
        if error:
            failed_batches.append((batch_num, error))
        else:
            total_processed += count
            successful_batches += 1
            if batch_num % 10 == 0:
                print(f"Processed batch {batch_num:04d}: {count} responses")

    print(f"\n=== COMPLETION REPORT ===")
    print(f"Batches processed: {successful_batches}/100")
    print(f"Total responses generated: {total_processed}")

    if failed_batches:
        print(f"\nFailed batches:")
        for bn, err in failed_batches:
            print(f"  - batch_{bn:04d}: {err}")


if __name__ == "__main__":
    main()
