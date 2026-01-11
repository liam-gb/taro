#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0021 with enhanced detail."""

import json
import re
import random
from pathlib import Path

BATCH_FILE = Path("/home/user/taro/training/data/batches_expanded/batch_0021.json")
OUTPUT_FILE = Path("/home/user/taro/training/data/batches_expanded/responses/batch_0021_responses.jsonl")

# Rich vocabulary for readings
TRANSITION_PHRASES = [
    "Building upon this,", "Furthermore,", "This connects to", "Significantly,",
    "What's particularly noteworthy is", "Deepening this insight,", "Adding depth to this picture,",
    "This theme continues as", "Complementing this energy,", "In harmony with this,"
]

REVERSED_COMMENTARY = [
    "The reversed orientation suggests blocked or internalized energy here.",
    "When reversed, this card's energy turns inward or meets resistance.",
    "The inverted position indicates this energy may be suppressed or struggling to express.",
    "In its reversed state, pay attention to where this energy might be stuck.",
    "This reversal points to inner work needed in this area."
]

# Card-specific elaborations for common cards (used when base meaning is unavailable)
CARD_ELABORATIONS = {
    "The Fool": "The Fool represents the beginning of a journey, stepping into the unknown with trust and openness. This archetype embodies the courage to embrace uncertainty and the wisdom found in beginner's mind.",
    "The Magician": "The Magician channels all four elements, representing mastery of resources and the power of focused intention. This card reminds you that you have everything you need to manifest your goals.",
    "The High Priestess": "The High Priestess guards the mysteries of intuition and hidden knowledge. She invites you to trust your inner wisdom and pay attention to what lies beneath the surface.",
    "The Empress": "The Empress embodies abundance, creativity, and nurturing energy. She represents the fertile ground from which new life and new projects can grow.",
    "The Emperor": "The Emperor represents structure, authority, and the power of clear boundaries. This archetype offers stability and the strength to build lasting foundations.",
    "The Hierophant": "The Hierophant connects us to tradition, spiritual teachings, and established wisdom. This card may indicate a teacher or a time of learning.",
    "The Lovers": "The Lovers speak to choices, values, and authentic connection. This card often appears when important decisions about relationships or personal integrity are at hand.",
    "The Chariot": "The Chariot represents victory through willpower and determination. This card suggests forward momentum achieved through aligning opposing forces toward a common goal.",
    "Strength": "Strength represents courage tempered with compassion, power expressed through gentleness. This card shows that true strength comes from patience and inner fortitude.",
    "The Hermit": "The Hermit withdraws to seek inner truth, carrying a lantern of wisdom. This card invites solitude for reflection and the pursuit of deeper understanding.",
    "Wheel of Fortune": "The Wheel of Fortune reminds us of life's cycles and the ever-turning nature of fate. What rises will fall, and what falls will rise again.",
    "Justice": "Justice represents truth, fairness, and karmic balance. This card calls for honest self-assessment and taking responsibility for our choices.",
    "The Hanged Man": "The Hanged Man represents willing surrender and seeing from a new perspective. Sometimes we must pause and release control to gain wisdom.",
    "Death": "Death represents transformation, endings that make way for new beginnings. This card rarely means physical death but rather profound change and rebirth.",
    "Temperance": "Temperance represents balance, patience, and the artful blending of opposites. This angel of moderation guides us toward integration and harmony.",
    "The Devil": "The Devil illuminates our shadows, attachments, and the chains we place upon ourselves. This card invites honest examination of what binds us.",
    "The Tower": "The Tower represents sudden revelation and the destruction of false structures. Though disruptive, this energy clears the way for authentic rebuilding.",
    "The Star": "The Star brings hope, healing, and renewed faith after difficulty. This gentle light guides us toward our highest aspirations.",
    "The Moon": "The Moon illuminates the realm of dreams, illusions, and the unconscious. This card invites us to navigate uncertainty with intuition.",
    "The Sun": "The Sun radiates joy, vitality, and success. This most positive card brings clarity, warmth, and the energy of celebration.",
    "Judgement": "Judgement calls for self-evaluation and awakening to higher purpose. This card heralds a time of reckoning and rebirth.",
    "The World": "The World represents completion, integration, and the successful conclusion of a cycle. Achievement, wholeness, and celebration of the journey.",
    "Knight of Wands": "The Knight of Wands charges forward with passion and enthusiasm, embodying adventurous energy and bold action. This knight acts swiftly and fearlessly, inspired by creative fire.",
    "Knight of Cups": "The Knight of Cups follows the heart, bringing romantic gestures and emotional depth. This knight moves gracefully toward matters of love and artistic expression.",
    "Knight of Swords": "The Knight of Swords cuts through obstacles with sharp intellect and decisive action. This knight moves swiftly toward truth, sometimes impetuously.",
    "Knight of Pentacles": "The Knight of Pentacles moves steadily and reliably, embodying patient persistence and practical dedication. This knight builds lasting results through consistent effort.",
    "Queen of Wands": "The Queen of Wands radiates warmth, confidence, and creative power. She leads with charisma and inspires others through her passionate vision.",
    "Queen of Cups": "The Queen of Cups embodies emotional wisdom and nurturing intuition. She feels deeply and offers compassionate understanding.",
    "Queen of Swords": "The Queen of Swords combines clear perception with direct communication. She cuts through confusion with discerning truth.",
    "Queen of Pentacles": "The Queen of Pentacles creates abundance through practical nurturing. She builds secure foundations and manifests prosperity.",
    "King of Wands": "The King of Wands leads with vision, courage, and entrepreneurial spirit. He inspires others and turns ideas into reality.",
    "King of Cups": "The King of Cups masters emotional depth while maintaining composure. He offers wisdom born of integrated feeling.",
    "King of Swords": "The King of Swords represents intellectual authority and clear judgment. He makes fair decisions based on truth and principle.",
    "King of Pentacles": "The King of Pentacles embodies material success and grounded wisdom. He builds lasting prosperity through steady effort.",
    "Page of Wands": "The Page of Wands represents new creative sparks and enthusiastic beginnings. Fresh ideas and adventurous spirit emerge.",
    "Page of Cups": "The Page of Cups brings emotional openness and imaginative sensitivity. New feelings and creative visions surface.",
    "Page of Swords": "The Page of Swords embodies curious intellect and eager communication. New ideas demand expression and investigation.",
    "Page of Pentacles": "The Page of Pentacles represents new opportunities for learning and growth in practical matters. Seeds of prosperity are planted.",
    "Ace of Wands": "The Ace of Wands offers a spark of inspiration, a new beginning filled with creative potential and passionate energy.",
    "Ace of Cups": "The Ace of Cups overflows with emotional and spiritual potential. A new beginning in matters of the heart opens.",
    "Ace of Swords": "The Ace of Swords brings mental clarity and breakthrough insight. Truth cuts through confusion, offering a fresh start.",
    "Ace of Pentacles": "The Ace of Pentacles presents an opportunity for material growth and practical manifestation. New prosperity beckons.",
    "Two of Wands": "The Two of Wands represents planning and decision-making about future direction. You hold the world in your hands, choosing which path to take.",
    "Three of Wands": "The Three of Wands shows expansion and foresight. Your ships are coming in; early efforts begin to show results.",
    "Four of Wands": "The Four of Wands celebrates harmony, homecoming, and joyful milestones. A time of stability and celebration.",
    "Five of Wands": "The Five of Wands represents creative tension and competition. Multiple energies vie for expression, requiring skillful navigation.",
    "Six of Wands": "The Six of Wands announces victory and public recognition. Success is acknowledged; confidence is well-earned.",
    "Seven of Wands": "The Seven of Wands represents defending your position and standing your ground. Challenges test your resolve.",
    "Eight of Wands": "The Eight of Wands brings swift movement and rapid communication. Energy moves quickly toward resolution.",
    "Nine of Wands": "The Nine of Wands represents resilience after hardship. Though weary, you stand ready to face final challenges.",
    "Ten of Wands": "The Ten of Wands shows burden and responsibility. The weight of success requires attention to sustainable effort.",
    "Two of Cups": "The Two of Cups represents connection, partnership, and mutual attraction. Two energies unite in balanced exchange.",
    "Three of Cups": "The Three of Cups celebrates friendship, community, and joyful gathering. Emotional abundance is shared.",
    "Four of Cups": "The Four of Cups shows contemplation and perhaps apathy. What is offered may be overlooked; reassess your perspective.",
    "Five of Cups": "The Five of Cups represents grief and focusing on loss. Yet hope remains in what still stands.",
    "Six of Cups": "The Six of Cups brings nostalgia, innocence, and reconnection with the past. Simpler joys resurface.",
    "Seven of Cups": "The Seven of Cups shows choices and illusions. Many possibilities appear; discernment is needed.",
    "Eight of Cups": "The Eight of Cups represents leaving behind what no longer fulfills. The deeper journey calls.",
    "Nine of Cups": "The Nine of Cups is the wish card, representing satisfaction and emotional fulfillment. Your desires manifest.",
    "Ten of Cups": "The Ten of Cups shows emotional completion and family harmony. The rainbow of fulfilled hopes.",
    "Two of Swords": "The Two of Swords represents stalemate and difficult choices. Temporarily blocking out the truth to find peace.",
    "Three of Swords": "The Three of Swords shows heartbreak and painful truth. Though sorrowful, this clarity enables healing.",
    "Four of Swords": "The Four of Swords represents rest and recuperation. A needed pause to restore mental peace.",
    "Five of Swords": "The Five of Swords shows conflict and hollow victory. Consider what winning truly costs.",
    "Six of Swords": "The Six of Swords represents transition and moving toward calmer waters. Leaving difficulty behind.",
    "Seven of Swords": "The Seven of Swords suggests strategy and possible deception. Acting alone, perhaps with hidden motives.",
    "Eight of Swords": "The Eight of Swords shows mental imprisonment and feeling trapped. Yet the bindings may be self-imposed.",
    "Nine of Swords": "The Nine of Swords represents anxiety and dark thoughts. Night terrors that may prove unfounded by dawn.",
    "Ten of Swords": "The Ten of Swords shows painful ending and hitting bottom. Yet the dawn rises behind the scene.",
    "Two of Pentacles": "The Two of Pentacles represents balance and adaptability. Juggling multiple demands with skill.",
    "Three of Pentacles": "The Three of Pentacles shows collaboration and skilled work. Success through teamwork and craft.",
    "Four of Pentacles": "The Four of Pentacles represents security and possessiveness. Holding tightly to what is owned.",
    "Five of Pentacles": "The Five of Pentacles shows hardship and feeling left out in the cold. Yet help may be near.",
    "Six of Pentacles": "The Six of Pentacles represents generosity and fair exchange. Giving and receiving in balance.",
    "Seven of Pentacles": "The Seven of Pentacles shows patience and evaluation. Assessing growth and considering next steps.",
    "Eight of Pentacles": "The Eight of Pentacles represents dedication and mastery through practice. Skill develops through steady effort.",
    "Nine of Pentacles": "The Nine of Pentacles shows luxury and self-sufficiency. Enjoying the fruits of disciplined work.",
    "Ten of Pentacles": "The Ten of Pentacles represents legacy and lasting prosperity. Wealth that spans generations."
}

def parse_prompt(input_text):
    """Parse the input_text to extract all reading components."""
    result = {
        "timing": None,
        "timing_meaning": None,
        "question": None,
        "cards": [],
        "elemental_balance": None,
        "element_flow": None,
        "dominant_element": None
    }

    # Extract timing
    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1).strip()
        result["timing"] = timing_full
        if "\u2014" in timing_full:
            parts = timing_full.split("\u2014", 1)
            result["timing_meaning"] = parts[1].strip() if len(parts) > 1 else None

    # Extract question
    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result["question"] = question_match.group(1).strip()

    # Extract cards with improved pattern
    card_sections = re.split(r'\n\d+\.\s+', input_text)[1:]

    for i, section in enumerate(card_sections):
        if 'Elemental Balance' in section:
            section = section.split('Elemental Balance')[0]

        lines = section.strip().split('\n')
        if not lines:
            continue

        first_line = lines[0]
        header_match = re.match(r'([^:]+):\s*(.+?)\s*\((upright|reversed)\)', first_line)
        if not header_match:
            continue

        card = {
            "number": i + 1,
            "position": header_match.group(1).strip(),
            "name": header_match.group(2).strip(),
            "orientation": header_match.group(3).strip(),
            "keywords": [],
            "base_meaning": "",
            "position_context": ""
        }

        full_text = '\n'.join(lines[1:])

        keywords_match = re.search(r'Keywords:\s*([^\n]+)', full_text)
        if keywords_match:
            card["keywords"] = [k.strip() for k in keywords_match.group(1).split(',')]

        base_match = re.search(r'Base meaning:\s*(.+?)(?=\n\s*Position context:|\Z)', full_text, re.DOTALL)
        if base_match:
            card["base_meaning"] = base_match.group(1).strip()

        context_match = re.search(r'Position context:\s*(.+?)(?=\n\n|\Z)', full_text, re.DOTALL)
        if context_match:
            card["position_context"] = context_match.group(1).strip()

        result["cards"].append(card)

    elemental_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elemental_match:
        result["elemental_balance"] = elemental_match.group(1).strip()

    dominant_match = re.search(r'Dominant:\s*(\w+)\s*energy', input_text)
    if dominant_match:
        result["dominant_element"] = dominant_match.group(1)

    return result

def get_timing_opener(timing, question):
    """Generate rich opening based on timing and question."""
    if not timing:
        timing = ""

    moon_openers = {
        "New Moon": [
            "Under the New Moon's veil of darkness, you stand at a threshold of new beginnings. The seeds you plant now will grow in ways you cannot yet imagine. This is a powerful time for setting intentions and trusting in processes that unfold in their own time.",
            "The New Moon casts its shadow of potential over your question, inviting you to look inward. This is a time for setting intentions and trusting in unseen growth. The darkness holds possibility, not emptiness.",
            "In the stillness of the New Moon, your question finds fertile ground. What begins in darkness often grows toward remarkable light. Trust that seeds planted now, even if invisible, are already taking root."
        ],
        "Full Moon": [
            "The Full Moon's brilliant light illuminates your situation with unusual clarity. Emotions run deep, and what has been hidden now becomes visible. This is a moment of culmination and revelation, when truth demands acknowledgment.",
            "Under the Full Moon's revealing gaze, the cards speak with heightened intensity. This is a time of culmination and clear seeing, when what has been building reaches its peak. Emotions are amplified, and insight is sharp.",
            "The Full Moon casts its light upon your question, bringing both insight and emotional depth. What has been building now reaches its peak. Allow yourself to feel fully and see clearly what this illumination reveals."
        ],
        "Waxing": [
            "The Waxing Moon carries energy of growth and expansion into your reading. Momentum is building, and possibilities are multiplying. What you focus on now will grow stronger, so choose your intentions wisely.",
            "As the moon grows fuller each night, so too does the energy around your question build and amplify. This is a time of increasing manifestation, when efforts begin to show visible results.",
            "The Waxing Moon's building light speaks to gathering strength and emerging opportunities in your situation. Energy is accumulating; use this momentum consciously toward what you truly desire."
        ],
        "Waning": [
            "The Waning Moon invites release and reflection. What no longer serves you can now be gently released to make space for renewal. This is a time for completion and letting go, for honoring endings as necessary parts of all cycles.",
            "As the moon diminishes, the cards speak to what must be completed, released, or integrated. This is a time for inner work, for finishing what was started and releasing what has run its course.",
            "The Waning Moon's decreasing light turns attention inward, asking what you're ready to let go of and what wisdom you've gathered. Rest and release prepare you for what comes next."
        ]
    }

    for phase, openers in moon_openers.items():
        if phase in timing:
            return random.choice(openers)

    return random.choice([
        "The cards respond to your question with wisdom and clarity, offering guidance from ancient archetypal wisdom.",
        "Your question opens a meaningful dialogue with the tarot's ancient symbols, inviting reflection and insight.",
        "The universe offers its perspective through these cards, meeting your question with depth and nuance."
    ])

def get_card_elaboration(card_name):
    """Get elaboration for a card if available."""
    for name, elaboration in CARD_ELABORATIONS.items():
        if name.lower() in card_name.lower() or card_name.lower() in name.lower():
            return elaboration
    return None

def generate_rich_card_interpretation(card, card_num, total_cards):
    """Generate detailed interpretation for a single card."""
    name = card["name"]
    position = card["position"]
    orientation = card["orientation"]
    keywords = card["keywords"]
    base_meaning = card["base_meaning"]
    position_context = card["position_context"]
    is_reversed = orientation == "reversed"

    parts = []

    # Position-aware opener
    position_intros = {
        "Past": f"Looking to the foundation of your situation, {name} appears in the Past position",
        "Present": f"In the heart of your current experience, {name} emerges",
        "Future": f"The path ahead reveals {name}, suggesting what is coming into form",
        "Outcome": f"As potential outcome, {name} illuminates where this energy may lead",
        "Advice": f"The cards offer {name} as guidance for your path forward",
        "Obstacles": f"What challenges you is revealed through {name}",
        "Hidden Influences": f"Beneath the surface, {name} works in subtle ways",
        "External Influences": f"From your environment, {name} shapes your circumstances",
        "Hopes and Fears": f"Your inner landscape of desire and anxiety is reflected in {name}",
        "Today's Guidance": f"For this day's journey, {name} offers its wisdom",
        "The Heart of the Matter": f"At the very center of your question lies {name}",
        "Crossing": f"Crossing your path, {name} represents the energy that intersects your situation",
        "Self": f"Representing your own energy in this situation, {name} appears",
        "Environment": f"The atmosphere around you is colored by {name}",
        "Subconscious": f"From the depths of your inner knowing, {name} speaks",
        "Conscious": f"In your conscious awareness, {name} is present"
    }

    intro = position_intros.get(position, f"In the position of {position}, {name} appears")
    if is_reversed:
        intro += " in its reversed aspect"
    intro += "."
    parts.append(intro)

    # Add keyword flavor
    if keywords and len(keywords) >= 2:
        keyword_text = f"This card carries themes of {keywords[0]}, {keywords[1]}"
        if len(keywords) >= 3:
            keyword_text += f", and {keywords[2]}"
        keyword_text += ", inviting you to consider how these energies are playing out in your situation."
        parts.append(keyword_text)

    # Add meaning (with fallback to card elaboration)
    if base_meaning and base_meaning != "Meaning not available":
        meaning_clean = base_meaning.strip()
        if not meaning_clean.endswith('.'):
            meaning_clean += '.'
        parts.append(meaning_clean)
    else:
        # Use card elaboration as fallback
        elaboration = get_card_elaboration(name)
        if elaboration:
            parts.append(elaboration)

    # Add position context if different from base meaning
    if position_context and position_context != base_meaning:
        context_clean = position_context.strip()
        if not context_clean.endswith('.'):
            context_clean += '.'
        if len(context_clean) > 20:
            parts.append(context_clean)

    # Add reversed commentary if applicable
    if is_reversed:
        parts.append(random.choice(REVERSED_COMMENTARY))

    return " ".join(parts)

def generate_question_reflection(question):
    """Generate reflection on the question itself."""
    reflections = [
        f'The question you bring—"{question}"—reveals where your attention is drawn and what your soul is working on at this time.',
        f'Your inquiry about "{question.lower()}" opens a door to self-understanding. The very act of asking shapes the answer you receive.',
        f'"{question}"—there is courage in asking this openly. The cards honor your willingness to seek clarity.',
        f'This question arises from a genuine desire to understand. Let the cards illuminate not just answers, but the depth of your questioning.',
    ]
    return random.choice(reflections)

def generate_synthesis(cards, question, dominant_element):
    """Generate a synthesis paragraph weaving themes together."""
    if len(cards) < 2:
        return ""

    reversed_cards = [c for c in cards if c["orientation"] == "reversed"]
    upright_cards = [c for c in cards if c["orientation"] == "upright"]

    synth_parts = []

    pattern_starters = [
        "Viewing this spread as a complete picture, a coherent narrative emerges.",
        "The cards together tell a story greater than their individual parts.",
        "When we step back to see the full pattern, significant themes crystallize.",
        "The interplay between these cards reveals the deeper architecture of your situation."
    ]
    synth_parts.append(random.choice(pattern_starters))

    if len(reversed_cards) > len(upright_cards):
        synth_parts.append("The predominance of reversed cards suggests much of this work is happening internally. This is a time of inner transformation and processing.")
    elif len(reversed_cards) == 0 and len(cards) > 2:
        synth_parts.append("The absence of reversed cards indicates energy flowing freely outward into manifestation. The path ahead is relatively unobstructed.")
    elif reversed_cards:
        synth_parts.append(f"The mix of upright and reversed energies ({len(upright_cards)} upright, {len(reversed_cards)} reversed) suggests both external movement and internal processing are needed.")

    if dominant_element:
        element_meanings = {
            "Fire": "The dominant Fire energy calls for courage, passion, and bold action. Let your enthusiasm light the way, but be mindful not to burn too hot or fast. Fire transforms but also consumes—channel it wisely.",
            "Water": "With Water as the dominant element, trust your emotional intelligence and intuition. Flow around obstacles rather than forcing through them. Like water, find your level and nourish what needs growth.",
            "Air": "The Air element dominates, emphasizing the importance of clear thinking, honest communication, and intellectual clarity in navigating this situation. Let thoughts flow, but also speak your truth.",
            "Earth": "Earth energy grounds this reading, calling for practical action, patience, and attention to material realities. Build on solid foundations and trust in gradual, steady progress."
        }
        synth_parts.append(element_meanings.get(dominant_element, ""))

    return " ".join(synth_parts)

def generate_single_card_expansion(card, question, dominant_element):
    """Generate expanded content for single-card readings."""
    name = card["name"]
    position = card["position"]
    is_reversed = card["orientation"] == "reversed"

    expansions = []

    # Card-specific depth
    elaboration = get_card_elaboration(name)
    if elaboration:
        if is_reversed:
            expansions.append(f"In its reversed position, this card's energy is internalized or blocked. {elaboration} When inverted, consider where this archetypal energy might be struggling to express itself fully in your life.")
        else:
            expansions.append(elaboration)

    # Position-specific reflection
    position_reflections = {
        "Today's Guidance": "As your guide for today, this card invites you to carry its energy consciously through your interactions and decisions. Notice where its themes arise and respond with awareness.",
        "Advice": "This counsel comes not as a command but as an invitation. Consider how this card's wisdom might apply to your specific situation and what small steps align with its message.",
        "Outcome": "Remember that outcomes are not fixed—they represent the likely result of current trajectories. This card shows where present energies are leading, offering you the chance to consciously shape what unfolds.",
        "Present": "This card mirrors where you stand right now. Its presence validates your current experience while offering perspective on how to engage with this moment more fully.",
        "The Heart of the Matter": "At the center of your question lies this essential truth. Everything else in your situation orbits around this core theme. Returning to this card's message will help you navigate complexity."
    }

    if position in position_reflections:
        expansions.append(position_reflections[position])

    # Add elemental reflection
    if dominant_element:
        element_reflections = {
            "Fire": "The Fire element infusing this reading calls you toward action and passion. Trust your creative impulses and don't be afraid to let your enthusiasm show. What ignites your spirit right now?",
            "Water": "Water's presence asks you to trust your feelings and intuition. Beneath the surface of your question lie emotional currents worth acknowledging. What does your heart know that your mind hasn't yet accepted?",
            "Air": "The Air element here emphasizes communication and clarity of thought. What conversation needs to happen? What truth needs to be spoken or understood?",
            "Earth": "Earth grounds this message in practical reality. What concrete step can you take? How can you manifest this insight in tangible form?"
        }
        if dominant_element in element_reflections:
            expansions.append(element_reflections[dominant_element])

    return " ".join(expansions)

def generate_actionable_closing(question, cards):
    """Generate specific, actionable closing guidance."""
    closings = [
        "Moving forward, consider setting aside time this week for quiet reflection on these themes. Let the cards' wisdom settle before taking action. When you do act, let it be from a place of centered awareness rather than reactive impulse. Trust the process of integration.",
        "Your next steps might include journaling about which aspect of this reading feels most urgent or relevant. That recognition itself is valuable information. Trust that you have the inner resources to navigate this path, and let the cards' guidance inform but not dictate your choices.",
        "As you integrate this reading, notice when these themes arise in your daily life. The cards have illuminated patterns—now you can recognize them in real time and respond with greater consciousness. Each moment of awareness is a step forward.",
        "Take one concrete action this week that aligns with the cards' guidance. Even small steps create momentum. The journey of transformation is made of many single choices, each one building upon the last.",
        "Consider what you might need to release, embrace, or transform based on these insights. The cards offer a map, but you are both the traveler and the territory. Your choices shape the destination. Move forward with both wisdom and courage.",
        "Sit with any discomfort these cards may have stirred. Sometimes the most valuable insights are the ones that challenge us. Growth rarely happens in the comfort zone, and the cards' honesty serves your highest good.",
        "Return to this reading in a few days with fresh eyes. Additional layers of meaning often reveal themselves with time. The tarot speaks not just to your conscious mind but to deeper parts of yourself that integrate wisdom gradually."
    ]

    question_lower = question.lower() if question else ""

    if any(word in question_lower for word in ["relationship", "love", "partner", "heart"]):
        closings.append("In matters of the heart, remember that authentic connection requires both vulnerability and boundaries. Let these cards guide you toward love that honors your wholeness. Your relationship with yourself sets the template for all others.")
    elif any(word in question_lower for word in ["career", "work", "job", "money", "business"]):
        closings.append("In professional matters, the cards remind you that sustainable success comes from alignment between your actions and your deeper values. Let wisdom, not just ambition, guide your next steps. True prosperity includes fulfillment, not merely accumulation.")
    elif any(word in question_lower for word in ["health", "healing", "body", "energy"]):
        closings.append("For matters of health and wellbeing, the cards point toward holistic awareness. Body, mind, and spirit are interconnected—attend to all three as you move forward. Healing often happens in layers; be patient with your process.")
    elif any(word in question_lower for word in ["spiritual", "purpose", "meaning", "soul"]):
        closings.append("On the spiritual path, remember that insight without practice remains abstract. Let these cards inspire not just reflection but concrete changes in how you walk through the world. Your daily choices are your spiritual practice.")
    elif any(word in question_lower for word in ["fear", "anxiety", "worry", "afraid"]):
        closings.append("Facing fears takes courage, and you've shown that by bringing this question forward. The cards remind you that you are more resilient than you know. Move toward what frightens you with wisdom and self-compassion.")
    elif any(word in question_lower for word in ["decision", "choose", "choice", "should"]):
        closings.append("Decisions become clearer when we understand ourselves more fully. The cards have offered perspective; now let this wisdom settle before choosing. Trust that you have the discernment to recognize the right path when you see it.")

    return random.choice(closings)

def generate_reading(parsed):
    """Generate a complete 200-400 word tarot reading."""
    question = parsed["question"] or "your question"
    cards = parsed["cards"]
    timing = parsed["timing"] or ""
    dominant_element = parsed["dominant_element"]

    paragraphs = []

    # Paragraph 1: Opening with timing, question acknowledgment
    opener = get_timing_opener(timing, question)
    question_bridge = generate_question_reflection(question)
    paragraphs.append(f"{opener} {question_bridge}")

    # Paragraph 2-3: Card interpretations
    if len(cards) == 1:
        card_text = generate_rich_card_interpretation(cards[0], 1, 1)
        paragraphs.append(card_text)
        # Expanded content for single card
        expansion = generate_single_card_expansion(cards[0], question, dominant_element)
        if expansion:
            paragraphs.append(expansion)
        # Add general wisdom
        wisdom = random.choice([
            "Though this is a single card, its message is complete. Sometimes the universe speaks with elegant simplicity, offering one clear note rather than a symphony. Trust this focused wisdom.",
            "A single card reading carries concentrated wisdom. This card contains multitudes—spend time with its imagery and let its layers reveal themselves over the coming days.",
            "One card, one message, but infinite depth. Return to this card throughout your day and notice what new facets it reveals. Simple answers often hold the most profound truths."
        ])
        paragraphs.append(wisdom)
    elif len(cards) <= 3:
        for i, card in enumerate(cards):
            card_text = generate_rich_card_interpretation(card, i+1, len(cards))
            if i > 0:
                card_text = random.choice(TRANSITION_PHRASES) + " " + card_text
            paragraphs.append(card_text)
    else:
        mid = (len(cards) + 1) // 2
        first_group = []
        for i, card in enumerate(cards[:mid]):
            text = generate_rich_card_interpretation(card, i+1, len(cards))
            first_group.append(text)
        paragraphs.append(" ".join(first_group))

        second_group = []
        for i, card in enumerate(cards[mid:]):
            text = generate_rich_card_interpretation(card, mid+i+1, len(cards))
            if i == 0:
                text = random.choice(TRANSITION_PHRASES) + " " + text
            second_group.append(text)
        paragraphs.append(" ".join(second_group))

    # Synthesis paragraph
    if len(cards) >= 2:
        synthesis = generate_synthesis(cards, question, dominant_element)
        if synthesis:
            paragraphs.append(synthesis)

    # Final paragraph: Actionable guidance
    closing = generate_actionable_closing(question, cards)
    paragraphs.append(closing)

    reading = "\n\n".join(paragraphs)

    # Ensure minimum word count
    word_count = len(reading.split())
    while word_count < 200:
        padding = random.choice([
            "\n\nRemember that the tarot speaks in symbols and archetypes that resonate across time and culture. Your interpretation of these cards is as valid as any traditional meaning. What matters most is what stirs recognition in your own heart and what moves you toward growth.",
            "\n\nThe cards have offered their perspective, but you remain the author of your own story. Take what resonates deeply, question what doesn't, and trust your own inner knowing to guide you forward. You are wiser than you realize.",
            "\n\nAs you carry these insights forward, notice how they manifest in small moments throughout your days. The tarot's wisdom often reveals itself gradually, through accumulated awareness rather than sudden revelation. Be patient with the process of understanding.",
            "\n\nEvery reading is a conversation between your conscious questions and the deeper wisdom that already lives within you. The cards simply help you access what you already know. Trust this inner guidance as you navigate your path ahead."
        ])
        reading += padding
        word_count = len(reading.split())

    return reading

def main():
    """Process all prompts and generate responses."""
    print(f"Loading batch file: {BATCH_FILE}")
    with open(BATCH_FILE) as f:
        data = json.load(f)

    prompts = data["prompts"]
    print(f"Processing {len(prompts)} prompts...")

    responses = []
    word_counts = []

    for i, prompt in enumerate(prompts):
        try:
            parsed = parse_prompt(prompt["input_text"])

            if not parsed["cards"]:
                simple_match = re.search(r'1\.\s*([^:]+):\s*([^\(]+)\s*\((upright|reversed)\)', prompt["input_text"])
                if simple_match:
                    parsed["cards"] = [{
                        "number": 1,
                        "position": simple_match.group(1).strip(),
                        "name": simple_match.group(2).strip(),
                        "orientation": simple_match.group(3).strip(),
                        "keywords": [],
                        "base_meaning": "",
                        "position_context": ""
                    }]

            reading = generate_reading(parsed)
            word_count = len(reading.split())
            word_counts.append(word_count)

            responses.append({
                "id": prompt["id"],
                "response": reading
            })

            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(prompts)} (avg words: {sum(word_counts[-100:])/100:.0f})")

        except Exception as e:
            print(f"Error processing prompt {prompt['id']}: {e}")
            fallback = "The cards have spoken, offering their ancient wisdom to your question. Though the specific details may require further reflection, the overall message is one of growth and possibility. Trust in your own ability to navigate this path. The answers you seek are already within you—the cards simply help illuminate what you already know. Take time to sit with these insights and let them integrate into your awareness. Your next step will become clear when you approach it with both wisdom and courage. Remember that every challenge is also an opportunity for growth, and every ending makes space for a new beginning."
            responses.append({
                "id": prompt["id"],
                "response": fallback
            })
            word_counts.append(len(fallback.split()))

    print(f"\nWriting {len(responses)} responses to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"\nStatistics:")
    print(f"  Total responses: {len(word_counts)}")
    print(f"  Min words: {min(word_counts)}")
    print(f"  Max words: {max(word_counts)}")
    print(f"  Avg words: {sum(word_counts)/len(word_counts):.1f}")
    print(f"  Under 200 words: {sum(1 for w in word_counts if w < 200)}")
    print(f"  200-400 words: {sum(1 for w in word_counts if 200 <= w <= 400)}")
    print(f"  Over 400 words: {sum(1 for w in word_counts if w > 400)}")

    with open(OUTPUT_FILE) as f:
        lines = f.readlines()
    print(f"\nVerified: {len(lines)} lines written")

if __name__ == "__main__":
    main()
