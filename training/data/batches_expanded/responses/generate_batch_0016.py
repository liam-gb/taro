#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0016 - Final optimized version."""

import json
import re
import random

# Moon phase openers
MOON_OPENERS = {
    "New Moon": [
        "Under the New Moon's dark embrace, new beginnings stir in the depths. This is a powerful time for planting seeds of intention, for trusting what cannot yet be seen but is already forming in the fertile darkness.",
        "The New Moon invites fresh starts and planted intentions. In this darkness before dawn, your question finds fertile ground. The absence of light creates space for vision.",
        "In this New Moon phase, seeds of possibility await your attention. The universe holds space for new directions and untried paths. What you begin now carries special power.",
    ],
    "Waxing Crescent": [
        "The Waxing Crescent brings momentum to your intentions, that first visible sliver of light after darkness. Energy builds now for manifestation. Your question arrives at a time of growing potential.",
        "As the moon grows, so does energy for your endeavor. The Waxing Crescent supports taking those first concrete steps forward. What was merely intention begins to take form.",
        "The Waxing Crescent lights your way forward. Small actions create large ripples now. Your inquiry arrives as momentum builds in the lunar cycle.",
    ],
    "First Quarter": [
        "The First Quarter moon calls for decisive action, illuminating the crossroads before you. Half shadow and half light mirrors the choices you face. This is a moment for commitment.",
        "At this lunar crossroads, commitment solidifies. The First Quarter phase asks: what are you willing to do to manifest your desires? Half the journey from dark to full is complete.",
        "The First Quarter challenges you to overcome obstacles with deliberate choice. The moon's half-light reveals both what helps and what hinders on your path.",
    ],
    "Waxing Gibbous": [
        "The Waxing Gibbous phase invites refinement and patience. Almost full, the moon reminds you that completion requires trust in the process. Fine-tuning now yields better results than forcing.",
        "As fullness approaches, the Waxing Gibbous supports calibration and adjustment. Patience serves better than force at this stage. Your question arrives as illumination grows.",
        "The Waxing Gibbous asks for refinement before harvest. Your question arrives when careful adjustment brings better results than bold action. Trust the process nearing completion.",
    ],
    "Full Moon": [
        "Under the Full Moon's brilliant illumination, truth becomes inescapably clear. What was hidden now reveals itself fully. Emotions peak and clarity arrives with the light.",
        "The Full Moon brings culmination and heightened awareness to your inquiry. This is a moment of harvest, of seeing the fruits of what was planted. Light touches everything.",
        "At this peak of lunar power, the Full Moon bathes your question in silver light. Emotions run high, but so does understanding. Nothing remains in shadow now.",
    ],
    "Waning Gibbous": [
        "The Waning Gibbous invites gratitude and the sharing of wisdom. Having reached fullness, the moon now teaches through release. Your question carries the weight of experience.",
        "As the moon begins its release, the Waning Gibbous supports integration of lessons learned. What has this cycle taught you? Your inquiry arrives at a time of processing.",
        "This Waning Gibbous phase supports giving back what you've gained. Your question carries the weight of experience seeking meaning. Integration becomes possible now.",
    ],
    "Last Quarter": [
        "The Last Quarter moon calls for release and forgiveness, a time of letting go. Half the moon has already dissolved into shadow. What must end so something new can begin?",
        "At this turning point, the Last Quarter invites you to release what no longer serves your highest good. Breaking patterns becomes possible now as light gives way to dark.",
        "The Last Quarter brings the energy of completion before renewal. Half shadow now, the moon supports releasing the old to make way for what comes next.",
    ],
    "Waning Crescent": [
        "The Waning Crescent whispers of rest and surrender, the final release before rebirth. In this dark space before renewal, deep wisdom stirs. Your question touches ancient knowing.",
        "In this final phase before renewal, the Waning Crescent supports deep reflection and restoration. Your question carries significance in this liminal space between cycles.",
        "The Waning Crescent supports surrender and preparation. As the moon prepares to be reborn, so might your understanding of this situation transform completely.",
    ],
}

TRANSITIONS = [
    "Looking deeper,",
    "The reading unfolds as",
    "Moving through the layers,",
    "Another dimension emerges:",
    "The narrative deepens as",
    "Weaving these threads,",
    "The pattern reveals:",
    "Building upon this,",
]

THEME_ELABORATIONS = {
    "relationship": [
        "In matters of connection, the heart knows truths the mind resists. Your cards suggest that authenticity, rather than strategy, opens the doors you seek. What you long for in another often reflects what you're still developing within yourself.",
        "Relationships mirror our relationship with ourselves. What you seek in another reflects what you're developing within. The cards invite you to consider what patterns repeat and what new possibilities await when you change your approach.",
        "The bonds between people are living things requiring constant tending. Consider what your cards reveal about the garden of connection you're cultivating. Some plants need pruning; others need more light.",
    ],
    "career": [
        "Your professional path is about alignment, not just advancement. The work that truly fulfills expresses who you are at your core. Consider whether your current direction honors your deeper values and gifts.",
        "Career questions often mask deeper inquiries about purpose and contribution. Consider what legacy you wish to leave through your efforts. The cards speak to the soul of your work, not just its surface.",
        "The workplace is a stage for personal development as much as professional achievement. Every challenge presents an opportunity for growth. Your career is a path of becoming, not just earning.",
    ],
    "financial": [
        "True abundance encompasses more than material wealth—it includes time, energy, relationships, and peace of mind. Your cards address the fuller picture of prosperity that you may be seeking consciously or unconsciously.",
        "Money flows most freely when aligned with values. Consider not just what you want to have, but who you want to be in relation to resources. The cards reveal the energy you bring to abundance.",
        "Financial concerns often mask deeper questions about security, worth, and freedom. The cards illuminate the roots beneath the surface worry. What belief about scarcity needs examining?",
    ],
    "health": [
        "Healing spirals through layers of release and integration, rarely moving in straight lines. Your body carries wisdom that your cards can help you access. Listen to what it tells you.",
        "Wellness encompasses mind, body, and spirit working in harmony. The cards suggest where balance may need attention. What aspects of your wholeness have you been neglecting?",
        "Recovery asks for patience with the process and compassion for yourself. Each small step forward matters, even when progress feels invisible. The cards honor your healing journey.",
    ],
    "spiritual": [
        "The spiritual path unfolds through questions more than answers. Your inquiry itself is part of the journey toward deeper understanding. Trust the questions that arise from your depths.",
        "Growth often comes disguised as difficulty. What challenges your spirit may also be what strengthens it. The cards reflect your soul's curriculum at this moment in time.",
        "Your soul's journey is uniquely yours, though ancient patterns illuminate the way. Trust the wisdom that draws you to ask these questions. Something in you already knows.",
    ],
    "family": [
        "Family bonds carry the weight of generations and the potential for profound healing. Your cards speak to patterns that may extend beyond this lifetime, calling for awareness and choice.",
        "Those closest to us often trigger our deepest work. Family relationships serve as mirrors reflecting what still needs attention within. What is your family teaching you now?",
        "Kinship asks us to balance loyalty with individual growth, honoring roots while reaching for new light. The cards illuminate the dance between belonging and becoming yourself.",
    ],
    "creative": [
        "Creativity flows from a source beyond the conscious mind. Your cards reveal what may be blocking or freeing that essential channel. What wants to be born through you?",
        "The creative impulse is sacred—it asks us to birth something new into the world. Honor this calling by addressing what the cards reveal about your relationship to expression.",
        "Expression requires both courage and surrender. Consider what fears may be silencing your authentic creative voice. The cards invite you to reclaim your right to create.",
    ],
    "general": [
        "Every question you bring carries seeds of its own answer. The cards serve as mirrors, reflecting back what you already sense within. Trust what resonates most deeply.",
        "Life's complexity rarely offers simple solutions. The cards instead offer perspective, inviting you to see your situation through new eyes. What shifts when you change your vantage point?",
        "Trust that you are exactly where you need to be to learn what you need to learn. The cards confirm the significance of this moment and your readiness to receive guidance.",
    ],
}

CARD_ELABORATIONS = {
    "The Fool": "This archetype represents the eternal beginner, carrying only faith as luggage. The universe invites you to embrace uncertainty as freedom.",
    "The Magician": "The Magician channels power from above into manifestation. All the tools you need are at hand; this card affirms your capacity to create change.",
    "The High Priestess": "Mystery and intuition flow through The High Priestess. She reminds you that some wisdom comes only through stillness.",
    "The Empress": "Abundance and nurturing energy radiate from The Empress. She speaks to the power of allowing rather than forcing growth.",
    "The Emperor": "Structure and authority define The Emperor. He brings order from chaos and reminds you of the power of clear boundaries.",
    "The Hierophant": "Tradition and spiritual teaching flow through The Hierophant. He represents the wisdom of established paths.",
    "The Lovers": "Choice and alignment emerge through The Lovers. This card speaks to decisions that honor your whole self.",
    "The Chariot": "Willpower and directed movement drive The Chariot. Opposing forces harness toward a single goal.",
    "Strength": "True power emerges through Strength—not force, but the gentle mastery of patience and compassion.",
    "The Hermit": "Inner guidance illuminates The Hermit's path. Wisdom comes through conscious retreat from noise.",
    "Wheel of Fortune": "Cycles turn through the Wheel. What rises falls; what falls rises. Change is the only constant.",
    "Justice": "Balance and truth govern Justice. Authentic action creates authentic results.",
    "The Hanged Man": "Suspension defines The Hanged Man. What seems stagnation may be gestation; sacrifice births vision.",
    "Death": "Transformation requires release. Endings enable beginnings; this card clears ground for renewal.",
    "Temperance": "Alchemy flows through Temperance. Opposing elements combine; moderation and timing are allies.",
    "The Devil": "Shadow emerges through The Devil. What chains you may be self-made; awareness enables freedom.",
    "The Tower": "Liberation crashes through The Tower. False structures fall; truth is ultimately freeing.",
    "The Star": "Hope pours from The Star. After devastation comes renewal; light returns after darkness.",
    "The Moon": "Illusion swims through The Moon. Not all is as it seems; intuition navigates where logic cannot.",
    "The Sun": "Joy blazes through The Sun. Alignment with truth illuminates your path forward.",
    "Judgement": "Awakening resounds through Judgement. A higher purpose summons you to rise into potential.",
    "The World": "Completion dances through The World. A cycle concludes; from this ending, new journeys emerge.",
}

REVERSED_INSIGHTS = [
    "This reversal turns energy inward, requiring internal work.",
    "Reversed, this card shows blocked or misdirected energy.",
    "The inverted aspect points to shadow work needing attention.",
    "This reversal indicates resistance or distorted expression.",
]

CLOSINGS = [
    "Consider taking one concrete step this week to honor what the cards have shown.",
    "The path forward begins with acknowledging what you've discovered here.",
    "Trust the wisdom that has emerged, and act aligned with this insight.",
    "Let this reading guide your next steps with clarity and purpose.",
    "The cards have illuminated possibilities—the choice how to respond is yours.",
    "Carry this awareness forward as you navigate the days ahead.",
    "Allow these insights to inform your choices going forward.",
    "The guidance is clear; your task now is to embody it.",
]

SINGLE_CARD_REFLECTIONS = [
    "When a single card carries your reading, its message holds concentrated significance. Every detail matters—the imagery, the position, the feeling it evokes. This card has appeared for you alone at this moment. Sit with it. Let its medicine work in you. What does it ask you to see that you've been avoiding? What does it affirm that you've already known? Notice what emotions arise as you consider its meaning.",
    "A single-card reading cuts through complexity to deliver essential truth. This card asks you to focus deeply on its medicine. What does it stir in you? Where do you feel it in your body? The simplicity of one card carries profound power when you give it your full attention. Return to this card throughout the day and notice how its meaning deepens.",
    "One card, one message, one invitation. The simplicity of a single-card reading belies its depth. This card appears because you are ready to receive exactly what it offers. Let it speak to you in the coming days as you encounter its energy in your waking life. Pay attention to synchronicities that echo this card's themes.",
]

SINGLE_CARD_EXTRAS = [
    "The focused energy of a single card demands focused attention. Let this message penetrate deeply rather than skimming its surface. Consider journaling about what arises as you contemplate this reading.",
    "In the concentration of one card lies clarity that more complex spreads might obscure. Trust this direct message from the cards. It has found you for a reason.",
    "A single card speaks with singular purpose. Its message is meant for exactly where you are right now. Honor this guidance by taking it seriously.",
]

def parse_prompt(input_text):
    result = {"timing": None, "question": None, "cards": [], "combinations": [], "elemental_balance": None, "dominant_element": None}

    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        for phase in MOON_OPENERS.keys():
            if phase in timing_match.group(1):
                result["timing"] = phase
                break

    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result["question"] = question_match.group(1)

    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+?)\s*\((upright|reversed)\)\s*\n\s*Keywords:\s*([^\n]+)\s*\n\s*Base meaning:\s*([^\n]+)\s*\n\s*Position context:\s*([^\n]+)'
    for match in re.finditer(card_pattern, input_text, re.MULTILINE):
        result["cards"].append({
            "position": match.group(2).strip(),
            "name": match.group(3).strip(),
            "orientation": match.group(4),
            "position_context": match.group(7).strip(),
        })

    combo_match = re.search(r'Card Combinations:\n((?:- [^\n]+\n?)+)', input_text)
    if combo_match:
        result["combinations"] = re.findall(r'- ([^\n]+)', combo_match.group(1))

    dom_match = re.search(r'Dominant:\s*(\w+)\s*energy', input_text)
    if dom_match:
        result["dominant_element"] = dom_match.group(1)

    elem_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elem_match:
        result["elemental_balance"] = elem_match.group(1).strip()

    return result

def get_theme(question):
    q = question.lower()
    if any(w in q for w in ["love", "relationship", "partner", "dating", "marriage", "romance", "boyfriend", "girlfriend", "husband", "wife", "ex"]):
        return "relationship"
    elif any(w in q for w in ["career", "job", "work", "business", "professional", "promotion", "interview", "boss", "hire"]):
        return "career"
    elif any(w in q for w in ["money", "financial", "wealth", "income", "debt", "abundance", "savings"]):
        return "financial"
    elif any(w in q for w in ["health", "healing", "recovery", "wellness", "body", "exercise", "tired", "sick"]):
        return "health"
    elif any(w in q for w in ["spiritual", "purpose", "meaning", "soul", "growth", "meditation", "path"]):
        return "spiritual"
    elif any(w in q for w in ["family", "parent", "child", "sibling", "mother", "father", "daughter", "son"]):
        return "family"
    elif any(w in q for w in ["creative", "art", "project", "passion", "expression", "write", "paint", "music"]):
        return "creative"
    return "general"

def card_text(card, short=False):
    name, pos, ori, ctx = card["name"], card["position"], card["orientation"], card["position_context"]
    is_rev = ori == "reversed"
    is_major = name in CARD_ELABORATIONS

    intros = {"Present": "In the present,", "Past": "From your past,", "Future": "Looking ahead,",
              "Challenge": "The challenge:", "Above": "Your highest potential:", "Below": "Beneath the surface,",
              "Advice": "The cards counsel:", "External": "External influences:", "Hopes/Fears": "Your hopes and fears:",
              "Outcome": "The outcome:", "Today's Guidance": "For today,", "Hidden Influences": "Hidden forces:",
              "Obstacles": "The obstacle:"}

    intro = intros.get(pos, f"In {pos},")
    app = f"{name} reversed" if is_rev else name

    if short:
        base = f"{intro} {app}—{ctx}"
    else:
        base = f"{intro} {app} appears. {ctx}"
        if is_major:
            base += f" {CARD_ELABORATIONS.get(name, '')}"

    if is_rev:
        base += f" {random.choice(REVERSED_INSIGHTS)}"
    return base

def generate_response(parsed):
    paragraphs = []
    timing = parsed["timing"] or "Full Moon"
    question = parsed["question"] or "your inquiry"
    theme = get_theme(question)
    cards = parsed["cards"]
    n = len(cards)

    opener = random.choice(MOON_OPENERS.get(timing, MOON_OPENERS["Full Moon"]))
    paragraphs.append(f"{opener} You ask: \"{question}\" Let us see what wisdom the cards hold.")

    if n == 0:
        paragraphs.append("Even without specific cards, your question carries wisdom. Trust your intuition to guide you.")
        paragraphs.append(random.choice(THEME_ELABORATIONS[theme]))
    elif n == 1:
        paragraphs.append(card_text(cards[0]))
        paragraphs.append(random.choice(THEME_ELABORATIONS[theme]))
        paragraphs.append(random.choice(SINGLE_CARD_REFLECTIONS))
        paragraphs.append(random.choice(SINGLE_CARD_EXTRAS))
    elif n == 2:
        paragraphs.append(card_text(cards[0]))
        paragraphs.append(card_text(cards[1]))
        paragraphs.append(random.choice(THEME_ELABORATIONS[theme]))
    elif n == 3:
        paragraphs.append(" ".join([card_text(c) for c in cards[:2]]))
        paragraphs.append(card_text(cards[2]))
        paragraphs.append(random.choice(THEME_ELABORATIONS[theme]))
    elif n <= 5:
        mid = n // 2
        paragraphs.append(" ".join([card_text(c) for c in cards[:mid]]))
        paragraphs.append(random.choice(TRANSITIONS) + " " + " ".join([card_text(c) for c in cards[mid:]]))
    elif n <= 7:
        mid = n // 2
        paragraphs.append(" ".join([card_text(c, short=True) for c in cards[:mid]]))
        paragraphs.append(random.choice(TRANSITIONS) + " " + " ".join([card_text(c, short=True) for c in cards[mid:]]))
    else:
        # Very long spread - ultra concise
        third = max(n // 3, 2)
        paragraphs.append(" ".join([card_text(c, short=True) for c in cards[:third]]))
        paragraphs.append(random.choice(TRANSITIONS) + " " + " ".join([card_text(c, short=True) for c in cards[third:2*third]]))
        if 2*third < n:
            paragraphs.append(random.choice(TRANSITIONS) + " " + " ".join([card_text(c, short=True) for c in cards[2*third:]]))

    # Extras - only for medium spreads
    extras = []
    if parsed["combinations"] and 3 <= n <= 6:
        extras.append(f"The cards speak together: {parsed['combinations'][0]}")

    if parsed["dominant_element"]:
        elem_notes = {"Fire": "Fire energy emphasizes passion and action.", "Water": "Water energy emphasizes emotion and intuition.",
                      "Air": "Air energy emphasizes thought and communication.", "Earth": "Earth energy emphasizes practicality and stability."}
        extras.append(elem_notes.get(parsed["dominant_element"], ""))

    rev_count = sum(1 for c in cards if c.get("orientation") == "reversed")
    if rev_count >= 3:
        extras.append("Multiple reversed cards indicate internal work is needed.")

    if extras and n <= 6:
        paragraphs.append(" ".join(extras))

    closings = {"relationship": "In matters of the heart, authenticity creates connection.",
                "career": "Your professional path unfolds through aligned choices.",
                "financial": "True prosperity encompasses more than numbers.",
                "health": "Healing asks for patience and self-compassion.",
                "spiritual": "Your soul's journey unfolds at its own pace.",
                "family": "Family patterns run deep, but awareness creates choice.",
                "creative": "Your creative voice awaits your courage.",
                "general": "The answers you seek stir within you already."}

    paragraphs.append(f"{closings[theme]} {random.choice(CLOSINGS)}")
    return "\n\n".join(paragraphs)

def main():
    with open('/home/user/taro/training/data/batches_expanded/batch_0016.json', 'r') as f:
        data = json.load(f)

    prompts = data["prompts"]
    print(f"Processing {len(prompts)} prompts...")

    responses, word_counts = [], []
    for i, prompt in enumerate(prompts):
        if i % 100 == 0:
            print(f"Processing prompt {i+1}/{len(prompts)}...")
        parsed = parse_prompt(prompt["input_text"])
        response = generate_response(parsed)
        word_counts.append(len(response.split()))
        responses.append({"id": prompt["id"], "response": response})

    with open('/home/user/taro/training/data/batches_expanded/responses/batch_0016_responses.jsonl', 'w') as f:
        for r in responses:
            f.write(json.dumps(r) + '\n')

    print(f"Written {len(responses)} responses")
    print(f"Word count: min={min(word_counts)}, max={max(word_counts)}, avg={sum(word_counts)//len(word_counts)}")
    print(f"Distribution: <200: {sum(1 for w in word_counts if w<200)}, 200-400: {sum(1 for w in word_counts if 200<=w<=400)}, >400: {sum(1 for w in word_counts if w>400)}")

if __name__ == "__main__":
    main()
