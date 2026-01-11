#!/usr/bin/env python3
"""Generate high-quality tarot reading responses for batch_0009.json"""

import json
import re
import random
import hashlib

# Extensive card interpretations for richer readings
MAJOR_ARCANA_INSIGHTS = {
    "The Fool": {
        "upright": "inviting you to embrace new beginnings with childlike wonder and trust in the journey ahead",
        "reversed": "suggesting caution about reckless decisions or fear that's blocking a necessary leap of faith"
    },
    "The Magician": {
        "upright": "reminding you that all the tools and talents you need are already within reach",
        "reversed": "indicating untapped potential or perhaps manipulation that needs addressing"
    },
    "The High Priestess": {
        "upright": "calling you to trust your intuition and honor the wisdom that emerges from stillness",
        "reversed": "suggesting secrets withheld or disconnection from your inner knowing"
    },
    "The Empress": {
        "upright": "bringing abundant, nurturing energy that supports growth and creative expression",
        "reversed": "pointing to creative blocks or neglect of self-care and personal needs"
    },
    "The Emperor": {
        "upright": "offering stability and structure, the power that comes from clear boundaries",
        "reversed": "warning of rigid control, tyranny, or difficulty with authority figures"
    },
    "The Hierophant": {
        "upright": "connecting you to tradition, spiritual wisdom, and established pathways",
        "reversed": "encouraging you to question convention and find your own spiritual truth"
    },
    "The Lovers": {
        "upright": "illuminating matters of the heart, meaningful choice, and values alignment",
        "reversed": "highlighting disharmony, difficult choices, or values in conflict"
    },
    "The Chariot": {
        "upright": "bringing victory through determination and mastery of opposing forces",
        "reversed": "indicating loss of direction, scattered energy, or obstacles to progress"
    },
    "Strength": {
        "upright": "showing that gentle persistence and compassion overcome brute force",
        "reversed": "suggesting self-doubt, inner weakness, or misused power"
    },
    "The Hermit": {
        "upright": "calling for solitude, inner reflection, and the wisdom found in stillness",
        "reversed": "warning of isolation, withdrawal, or fear of looking within"
    },
    "Wheel of Fortune": {
        "upright": "signaling a turning point, fate's hand moving events in new directions",
        "reversed": "indicating resistance to change or feeling caught in negative cycles"
    },
    "Justice": {
        "upright": "bringing fairness, karmic balance, and truth into the light",
        "reversed": "pointing to injustice, dishonesty, or avoidance of accountability"
    },
    "The Hanged Man": {
        "upright": "inviting surrender, new perspective through willing sacrifice",
        "reversed": "suggesting resistance to necessary pause or fear of letting go"
    },
    "Death": {
        "upright": "bringing profound transformation, the clearing that allows new growth",
        "reversed": "indicating resistance to change, stagnation, or incomplete endings"
    },
    "Temperance": {
        "upright": "blessing you with balance, patience, and the alchemy of moderation",
        "reversed": "warning of excess, impatience, or lack of long-term vision"
    },
    "The Devil": {
        "upright": "revealing attachments, shadow material, or bonds that restrict freedom",
        "reversed": "signaling liberation, breaking free from what has held you captive"
    },
    "The Tower": {
        "upright": "bringing sudden revelation, the destruction that precedes rebuilding",
        "reversed": "suggesting resisted change, fear of upheaval, or internal crisis"
    },
    "The Star": {
        "upright": "pouring out hope, healing, and faith restored after difficulty",
        "reversed": "indicating despair, disconnection from hope, or blocked inspiration"
    },
    "The Moon": {
        "upright": "illuminating the unconscious, dreams, illusions to see through",
        "reversed": "suggesting releasing fears, clarity emerging from confusion"
    },
    "The Sun": {
        "upright": "radiating joy, success, vitality, and childlike celebration",
        "reversed": "indicating dimmed joy, temporary setbacks, or false optimism"
    },
    "Judgement": {
        "upright": "calling for self-reflection, answering a higher calling, rebirth",
        "reversed": "suggesting self-doubt, failure to learn lessons, or harsh self-judgment"
    },
    "The World": {
        "upright": "celebrating completion, integration, and the fulfillment of a cycle",
        "reversed": "indicating incomplete cycles, delays, or lack of closure"
    }
}

# Minor arcana insights by suit
MINOR_ARCANA_SUITS = {
    "Wands": {
        "element": "Fire",
        "themes": "passion, creativity, ambition, and spiritual energy",
        "upright_tendency": "dynamic forward movement and inspired action",
        "reversed_tendency": "blocked creativity or misdirected passion"
    },
    "Cups": {
        "element": "Water",
        "themes": "emotions, relationships, intuition, and the heart's wisdom",
        "upright_tendency": "emotional fulfillment and deep connection",
        "reversed_tendency": "emotional turbulence or suppressed feelings"
    },
    "Swords": {
        "element": "Air",
        "themes": "thoughts, communication, conflict, and mental clarity",
        "upright_tendency": "clear thinking and decisive action",
        "reversed_tendency": "mental confusion or painful truths"
    },
    "Pentacles": {
        "element": "Earth",
        "themes": "material matters, work, health, and practical concerns",
        "upright_tendency": "stability, growth, and tangible results",
        "reversed_tendency": "material setbacks or misplaced priorities"
    }
}

COURT_CARD_INSIGHTS = {
    "Page": "youthful energy, new beginnings in this realm, messages arriving",
    "Knight": "active pursuit, movement, the energy in full expression",
    "Queen": "mature embodiment, nurturing mastery, emotional intelligence",
    "King": "complete mastery, authority, the element's wisdom made manifest"
}

QUESTION_THEMES = {
    "career": ["work", "job", "career", "profession", "business", "employment", "boss", "colleague", "workplace", "promotion", "interview", "hired", "fired", "resign"],
    "love": ["love", "relationship", "partner", "romance", "dating", "marriage", "heart", "boyfriend", "girlfriend", "spouse", "ex", "crush", "attracted", "soulmate", "twin flame"],
    "money": ["money", "financial", "finances", "income", "wealth", "debt", "afford", "savings", "investment", "budget", "earn", "pay", "cost", "expensive"],
    "health": ["health", "wellness", "fitness", "body", "illness", "medical", "healing", "energy", "tired", "sleep", "diet", "exercise", "stress", "anxiety", "mental health"],
    "spiritual": ["spiritual", "soul", "purpose", "meaning", "growth", "path", "destiny", "calling", "meditation", "awakening", "karma", "past life", "higher self"],
    "family": ["family", "parent", "mother", "father", "child", "children", "sibling", "brother", "sister", "relative", "home", "household", "daughter", "son"],
    "decision": ["should i", "decision", "choose", "choice", "whether", "or should", "which option", "what path", "best choice"],
    "timing": ["when", "how long", "timing", "soon", "ready", "right time", "waiting"],
    "fear": ["fear", "afraid", "scared", "worry", "anxious", "nervous", "dread", "terrified"],
    "creativity": ["creative", "creativity", "art", "artist", "writing", "music", "project", "inspiration", "create", "expression"],
    "friendship": ["friend", "friendship", "social", "friends", "acquaintance", "companion"],
    "self": ["myself", "who am i", "self-esteem", "confidence", "identity", "authentic", "true self", "inner", "personal growth"]
}

def get_question_theme(question):
    """Identify the primary theme of the question."""
    q_lower = question.lower()
    for theme, keywords in QUESTION_THEMES.items():
        if any(kw in q_lower for kw in keywords):
            return theme
    return "general"

def parse_prompt(input_text):
    """Extract key elements from the prompt."""
    result = {
        "timing": "",
        "question": "",
        "cards": [],
        "combinations": "",
        "elemental_balance": "",
        "dominant_element": ""
    }

    timing_match = re.search(r'TIMING: (.+?)(?:\n|$)', input_text)
    if timing_match:
        result["timing"] = timing_match.group(1).strip()

    question_match = re.search(r'QUESTION: "(.+?)"', input_text)
    if question_match:
        result["question"] = question_match.group(1).strip()

    # More robust card pattern matching
    card_pattern = r'(\d+)\. ([^:]+): ([^\n]+)\n\s+Keywords: ([^\n]+)\n\s+Base meaning: ([^\n]+)\n\s+Position context: ([^\n]+)'
    for match in re.finditer(card_pattern, input_text):
        card = {
            "number": match.group(1),
            "position": match.group(2).strip(),
            "name": match.group(3).strip(),
            "keywords": match.group(4).strip(),
            "base_meaning": match.group(5).strip(),
            "position_context": match.group(6).strip()
        }
        result["cards"].append(card)

    combo_match = re.search(r'Card Combinations:\n(.+?)\n\nElemental', input_text, re.DOTALL)
    if combo_match:
        result["combinations"] = combo_match.group(1).strip()

    elem_match = re.search(r'Elemental Balance: ([^\n]+)', input_text)
    if elem_match:
        result["elemental_balance"] = elem_match.group(1).strip()

    dom_match = re.search(r'Dominant: (\w+) energy', input_text)
    if dom_match:
        result["dominant_element"] = dom_match.group(1).strip()

    return result

def seed_random(prompt_id):
    """Seed random for consistent but varied output per prompt."""
    seed = int(hashlib.md5(prompt_id.encode()).hexdigest()[:8], 16)
    random.seed(seed)

def get_card_base(name):
    """Extract base card name without orientation."""
    return name.replace("(reversed)", "").replace("(upright)", "").strip()

def is_reversed(name):
    """Check if card is reversed."""
    return "(reversed)" in name.lower()

def get_suit(card_name):
    """Get the suit of a minor arcana card."""
    for suit in ["Wands", "Cups", "Swords", "Pentacles"]:
        if suit in card_name:
            return suit
    return None

def get_court_rank(card_name):
    """Get the court rank if applicable."""
    for rank in ["Page", "Knight", "Queen", "King"]:
        if rank in card_name:
            return rank
    return None

def get_major_insight(name):
    """Get insight for major arcana card."""
    base = get_card_base(name)
    orientation = "reversed" if is_reversed(name) else "upright"
    if base in MAJOR_ARCANA_INSIGHTS:
        return MAJOR_ARCANA_INSIGHTS[base][orientation]
    return None

def get_minor_insight(name):
    """Get insight for minor arcana card."""
    base = get_card_base(name)
    suit = get_suit(base)
    court = get_court_rank(base)
    reversed = is_reversed(name)

    if suit and suit in MINOR_ARCANA_SUITS:
        suit_info = MINOR_ARCANA_SUITS[suit]
        if court and court in COURT_CARD_INSIGHTS:
            base_insight = COURT_CARD_INSIGHTS[court]
            if reversed:
                return f"The {court} of {suit}'s energy of {base_insight.lower()} appears blocked or internalized. Consider how {suit_info['themes']} may need attention."
            else:
                return f"The {court} of {suit} brings {base_insight.lower()}, connecting you to themes of {suit_info['themes']}."
        else:
            if reversed:
                return f"This card suggests {suit_info['reversed_tendency']} in matters of {suit_info['themes']}."
            else:
                return f"This card brings {suit_info['upright_tendency']} in the realm of {suit_info['themes']}."
    return None

def generate_opening(parsed, theme):
    """Generate a thoughtful opening paragraph."""
    question = parsed["question"]
    timing = parsed["timing"]

    timing_insight = ""
    if "Full Moon" in timing:
        timing_insight = "Under the Full Moon's illuminating light, clarity emerges from shadow. This is a time of culmination and revelation, when the truth of matters can no longer hide."
    elif "New Moon" in timing:
        timing_insight = "The New Moon's darkness is not absence but potential. In this phase of new beginnings, seeds planted now carry special power."
    elif "Waning Gibbous" in timing:
        timing_insight = "The Waning Gibbous moon invites gratitude and sharing. As the light begins to recede, we are called to give back and reflect on what we've received."
    elif "Waning Crescent" in timing:
        timing_insight = "In the Waning Crescent phase, we approach the dark moon's rest. This is a time for surrender, release, and preparing for the next cycle."
    elif "Waning" in timing:
        timing_insight = "During the waning phase, we release what no longer serves. This reading carries the energy of letting go and clearing space for what comes next."
    elif "Waxing Gibbous" in timing:
        timing_insight = "The Waxing Gibbous moon refines and perfects. Patience is required now as plans take their final shape before culmination."
    elif "Waxing Crescent" in timing:
        timing_insight = "The Waxing Crescent brings hope and action. Momentum builds as intentions begin manifesting into form."
    elif "Waxing" in timing:
        timing_insight = "The waxing moon builds momentum. This is a time of growth and action, when efforts gain strength."
    elif "First Quarter" in timing:
        timing_insight = "At the First Quarter, challenges arise that test our commitment. This is a threshold moment requiring decision and action."
    elif "Third Quarter" in timing or "Last Quarter" in timing:
        timing_insight = "The Third Quarter brings reflection before release. Lessons crystallize as the cycle prepares to close."

    openings_by_theme = {
        "career": [
            f"You come seeking guidance about your professional path, asking: '{question}' {timing_insight}",
            f"Your work situation weighs on your mind as you ask: '{question}' {timing_insight}",
            f"Career questions bring you to the cards today. {timing_insight} Let's explore what they reveal about your inquiry."
        ],
        "love": [
            f"Matters of the heart bring you here today with your question: '{question}' {timing_insight}",
            f"Love's complexities prompt this reading as you ask: '{question}' {timing_insight}",
            f"Relationships stand at the center of your inquiry. {timing_insight} The cards respond to your heart's question."
        ],
        "money": [
            f"Financial concerns have prompted this reading with your question: '{question}' {timing_insight}",
            f"Material security weighs on your mind as you ask: '{question}' {timing_insight}",
            f"Questions of abundance and resources bring you here. {timing_insight} Let's explore what the cards reveal."
        ],
        "health": [
            f"Your wellbeing is the focus of this reading as you ask: '{question}' {timing_insight}",
            f"Health and vitality matter deeply right now. {timing_insight} The cards respond to your question.",
            f"Body, mind, or spirit call for attention with your inquiry: '{question}' {timing_insight}"
        ],
        "decision": [
            f"A significant choice stands before you as you ask: '{question}' {timing_insight}",
            f"Decision weighs upon you as you seek clarity: '{question}' {timing_insight}",
            f"Crossroads demand your attention. {timing_insight} Let's illuminate the path forward."
        ],
        "spiritual": [
            f"Your soul seeks deeper understanding as you ask: '{question}' {timing_insight}",
            f"Spiritual questions guide this reading. {timing_insight} The cards respond to your seeking.",
            f"Meaning and purpose call to you with your question: '{question}' {timing_insight}"
        ],
        "fear": [
            f"You bravely explore what frightens you, asking: '{question}' {timing_insight}",
            f"Fear has brought you seeking wisdom. {timing_insight} The cards honor your courage in asking.",
            f"Facing what we fear takes courage. {timing_insight} Let's see what light the cards shed on your question."
        ],
        "creativity": [
            f"Creative energy seeks expression as you ask: '{question}' {timing_insight}",
            f"Your artistic spirit prompts this reading. {timing_insight} The cards respond to your creative inquiry.",
            f"The muse has questions of her own. {timing_insight} Let's explore what blocks or frees your creative flow."
        ],
        "self": [
            f"You turn inward with your question: '{question}' {timing_insight}",
            f"Self-discovery guides this reading. {timing_insight} The cards mirror your inner landscape.",
            f"The journey to know oneself is sacred. {timing_insight} Let's see what the cards reveal about your true nature."
        ],
        "family": [
            f"Family matters weigh on your heart as you ask: '{question}' {timing_insight}",
            f"The bonds of kinship prompt this reading. {timing_insight} The cards address your family concerns.",
            f"Those closest to us shape us deeply. {timing_insight} Let's explore what the cards reveal about your family question."
        ],
        "friendship": [
            f"Friendship and social connections bring you here asking: '{question}' {timing_insight}",
            f"The bonds we choose matter deeply. {timing_insight} The cards respond to your question about friendship.",
            f"Connection with others enriches life's journey. {timing_insight} Let's see what guidance emerges."
        ],
        "timing": [
            f"Timing is everything, and you wisely ask: '{question}' {timing_insight}",
            f"When to act is as important as what to do. {timing_insight} The cards offer their perspective on timing.",
            f"Patience and action each have their season. {timing_insight} Let's explore what the cards reveal about your timing question."
        ],
        "general": [
            f"You come with an important question on your heart: '{question}' {timing_insight}",
            f"The cards are drawn to address your inquiry: '{question}' {timing_insight}",
            f"Your question deserves thoughtful consideration. {timing_insight} Let's explore what wisdom emerges."
        ]
    }

    templates = openings_by_theme.get(theme, openings_by_theme["general"])
    return random.choice(templates)

def interpret_card_in_context(card, position_in_reading, total_cards):
    """Generate rich interpretation of a card in its position."""
    position = card["position"]
    name = card["name"]
    base_name = get_card_base(name)
    keywords = card["keywords"]
    context = card["position_context"]
    reversed = is_reversed(name)

    # Check for major arcana insight
    major_insight = get_major_insight(name)
    minor_insight = get_minor_insight(name)

    # Position-specific framing
    position_frames = {
        "Past": "Looking to what has shaped this moment",
        "Present": "In the heart of your current situation",
        "Future": "Gazing toward what's unfolding",
        "Hidden Influences": "Beneath the surface",
        "Subconscious": "From the depths of your unconscious",
        "Conscious": "In your present awareness",
        "Obstacles": "Addressing what stands in your way",
        "External Influences": "From the world around you",
        "Advice": "The cards counsel",
        "Outcome": "The trajectory points toward",
        "Situation": "At the core of this matter",
        "Action": "The call to action reveals",
        "Today's Guidance": "Your message for today",
        "Challenge": "The challenge before you",
        "Foundation": "What supports you",
        "Hopes and Fears": "In the realm of hopes and fears",
        "Self": "Within yourself",
        "Querent": "Your current position",
        "Crossing": "What crosses you",
        "Crown": "Above you, representing ideals",
        "Root": "At the root of this matter",
        "Recent Past": "From the recent past",
        "Near Future": "In the near future",
        "Environment": "Your environment reveals",
        "Allies": "Those who support you",
        "Internal": "Within your inner world",
        "External": "In the outer world",
        "Guidance": "As guidance"
    }

    frame = position_frames.get(position, f"In the {position} position")

    if reversed:
        reversal_phrases = [
            f"{base_name} appears reversed, and {context.lower() if context and context[0].isupper() else context}",
            f"we find {base_name} inverted. {context}",
            f"{base_name} shows its reversed face, indicating that {context.lower() if context and context[0].isupper() else context}"
        ]
        card_state = random.choice(reversal_phrases)
    else:
        upright_phrases = [
            f"{base_name} appears with clarity. {context}",
            f"we encounter {base_name} in its upright position. {context}",
            f"{base_name} offers its wisdom directly: {context.lower() if context and context[0].isupper() else context}"
        ]
        card_state = random.choice(upright_phrases)

    # Build the interpretation
    if major_insight:
        return f"{frame}, {card_state} This powerful Major Arcana card is {major_insight}."
    elif minor_insight:
        return f"{frame}, {card_state} {minor_insight}"
    else:
        return f"{frame}, {card_state} The energy of {keywords.lower()} colors this aspect of your reading."

def generate_card_paragraphs(cards):
    """Generate flowing paragraphs interpreting the cards."""
    if len(cards) == 1:
        interp = interpret_card_in_context(cards[0], 0, 1)
        extensions = [
            f"With only one card drawn, its message carries concentrated significance. Every nuance matters. Sit with the imagery of {get_card_base(cards[0]['name'])} and let it speak to the layers of your question.",
            f"This single card carries the full weight of the reading's wisdom. The {get_card_base(cards[0]['name'])} asks for your complete attention, as within its symbolism lies the answer you seek.",
            f"When a single card appears, it demands we go deep rather than wide. The {get_card_base(cards[0]['name'])} holds everything you need to know within its frame."
        ]
        return f"{interp} {random.choice(extensions)}"

    paragraphs = []

    if len(cards) == 2:
        p1 = interpret_card_in_context(cards[0], 0, 2)
        p2 = interpret_card_in_context(cards[1], 1, 2)
        bridges = [
            "These two cards dance together, each illuminating the other.",
            "Together, these cards create a dialogue about your situation.",
            "The relationship between these cards tells its own story."
        ]
        paragraphs.append(f"{p1}\n\n{p2} {random.choice(bridges)}")
    elif len(cards) == 3:
        for i, card in enumerate(cards):
            paragraphs.append(interpret_card_in_context(card, i, 3))
        flow_phrases = [
            "The three-card spread creates a narrative arc, showing movement and development.",
            "These three cards weave together a story of progression and possibility.",
            "Together, this triad offers a complete picture of past influences, present circumstances, and future potential."
        ]
        return " ".join(paragraphs[:2]) + "\n\n" + paragraphs[2] + " " + random.choice(flow_phrases)
    else:
        # For larger spreads, group interpretations
        mid = len(cards) // 2
        first_half = [interpret_card_in_context(c, i, len(cards)) for i, c in enumerate(cards[:mid])]
        second_half = [interpret_card_in_context(c, i+mid, len(cards)) for i, c in enumerate(cards[mid:])]

        paragraphs.append(" ".join(first_half))

        transitions = [
            "As we continue through the spread, deeper layers emerge.",
            "The reading deepens as we examine the remaining cards.",
            "Moving further into the spread, additional insights surface.",
            "The narrative continues to unfold with the remaining cards."
        ]
        paragraphs.append(random.choice(transitions) + " " + " ".join(second_half))

    return "\n\n".join(paragraphs)

def generate_synthesis(parsed):
    """Generate a synthesis paragraph connecting themes."""
    cards = parsed["cards"]
    combinations = parsed["combinations"]
    dominant = parsed["dominant_element"]

    elements = []

    # Count majors and reversals
    majors = [c for c in cards if get_card_base(c["name"]) in MAJOR_ARCANA_INSIGHTS]
    reversals = [c for c in cards if is_reversed(c["name"])]

    if len(majors) > len(cards) // 2:
        elements.append("The strong presence of Major Arcana cards indicates this situation touches on significant life themes and soul-level lessons, not mere surface concerns")
    elif len(majors) > 0:
        major_names = [get_card_base(m["name"]) for m in majors]
        if len(major_names) > 1:
            elements.append(f"The {' and '.join(major_names)} bring major archetypal energy to this reading, elevating its significance")
        else:
            elements.append(f"The {major_names[0]} brings major archetypal energy to this reading")

    if len(reversals) > len(cards) // 2:
        elements.append("The prevalence of reversed cards suggests blocked energy or internalized processes that need conscious attention and integration")
    elif len(reversals) > 0:
        elements.append(f"The reversed cards in this spread point to areas requiring inner work or situations where energy flows inward rather than outward")

    if combinations:
        combo_text = combinations.split(':')[1].strip() if ':' in combinations else combinations
        elements.append(f"Notable card combinations amplify key messages: {combo_text}")

    if dominant:
        element_meanings = {
            "Fire": "passion, will, creative energy, and spiritual drive",
            "Water": "emotions, intuition, relationships, and the wisdom of the heart",
            "Air": "thoughts, communication, decisions, and mental clarity",
            "Earth": "material concerns, stability, health, and practical manifestation"
        }
        meaning = element_meanings.get(dominant, "elemental forces")
        elements.append(f"The dominant {dominant} energy in this reading emphasizes themes of {meaning}")

    if not elements:
        elements.append("The cards work together harmoniously to illuminate your path forward")

    return " ".join([e + "." for e in elements])

def generate_actionable_insight(parsed, theme):
    """Generate closing with specific, actionable guidance."""
    cards = parsed["cards"]
    question = parsed["question"]

    # Find advice and outcome cards if present
    advice_card = next((c for c in cards if "advice" in c["position"].lower()), None)
    outcome_card = next((c for c in cards if "outcome" in c["position"].lower()), None)
    action_card = next((c for c in cards if "action" in c["position"].lower()), None)
    guidance_card = next((c for c in cards if "guidance" in c["position"].lower()), None)

    key_card = advice_card or action_card or guidance_card or outcome_card or cards[-1]

    action_by_theme = {
        "career": [
            "Consider what small, concrete step you can take this week to align your work with your deeper values.",
            "Reflect on what professional boundary needs setting or what conversation needs having.",
            "Take time to envision where you want to be in one year, then work backward to identify your next move.",
            "Ask yourself what you would do if fear were not a factor in your career decisions."
        ],
        "love": [
            "Open a conversation with vulnerability, sharing something true about how you feel.",
            "Consider what pattern in relationships might be ready for transformation.",
            "Nurture the relationship with yourself as the foundation for all other connections.",
            "Practice expressing one honest need or desire to someone you trust."
        ],
        "money": [
            "Review your relationship with abundance - what beliefs about money might be limiting you?",
            "Take one concrete action toward financial clarity, whether budgeting, saving, or seeking advice.",
            "Consider how your material resources can be aligned with your deeper values.",
            "Notice where fear around money influences your decisions, and challenge one assumption."
        ],
        "health": [
            "Listen to what your body is telling you - what does it need that you've been ignoring?",
            "Commit to one sustainable change rather than dramatic overhaul.",
            "Consider how physical wellbeing connects to emotional and spiritual health.",
            "Honor rest as a productive practice, not a guilty indulgence."
        ],
        "decision": [
            "The cards don't decide for you, but they illuminate. What does your gut say when you quiet the noise?",
            "Write out both options and notice which one makes your body feel more expansive.",
            "Consider what you would advise a dear friend facing this same choice.",
            "Ask yourself which option you'll be proudest of in ten years."
        ],
        "spiritual": [
            "Dedicate time for stillness - answers often emerge in silence rather than seeking.",
            "Notice what practices or places help you feel most connected to something larger.",
            "Trust that your path is unfolding even when you cannot see the destination.",
            "Consider keeping a dream journal or meditation practice to strengthen intuition."
        ],
        "fear": [
            "Name your fear aloud - speaking it often diminishes its power over you.",
            "Ask what this fear is trying to protect you from, and whether that protection is still needed.",
            "Take one small action toward what frightens you, building courage incrementally.",
            "Consider what becomes possible on the other side of this fear."
        ],
        "creativity": [
            "Create something, anything, without judgment - let the process matter more than the product.",
            "Identify what critic's voice holds you back and write a response to it.",
            "Schedule creative time as non-negotiable, treating it with the same respect as other appointments.",
            "Consider what you created freely as a child and reconnect with that energy."
        ],
        "self": [
            "Spend time in quiet reflection, asking who you are beneath the roles you play.",
            "Notice when you abandon yourself to please others, and practice gentle boundary-setting.",
            "Journal about the qualities you most admire in others - they often reflect your own hidden gifts.",
            "Consider what you would do differently if you truly believed you were worthy of love and success."
        ],
        "family": [
            "Reflect on which family patterns you've inherited that still serve you, and which need releasing.",
            "Consider having a heart-to-heart conversation about what's truly bothering you.",
            "Remember that healthy boundaries can coexist with deep love.",
            "Ask yourself what healing in this relationship would look like, even if it seems impossible."
        ],
        "friendship": [
            "Reach out to someone you've been meaning to connect with - small gestures matter.",
            "Consider what you truly need from friendship and whether your current connections provide it.",
            "Be willing to have the vulnerable conversation that deepens connection.",
            "Reflect on whether you give as freely as you wish to receive."
        ],
        "timing": [
            "Trust that divine timing often differs from our desired timeline - patience is its own form of action.",
            "Use this waiting period productively by preparing for what you hope will come.",
            "Notice whether impatience stems from fear or genuine readiness.",
            "Consider what internal work this pause might be offering you time to complete."
        ],
        "general": [
            "Identify one small action that aligns with the guidance offered here.",
            "Sit with this reading for a day before making any major decisions.",
            "Journal about what resonates most strongly and what questions remain.",
            "Trust your intuitive response to these cards - it carries its own wisdom."
        ]
    }

    specific_actions = action_by_theme.get(theme, action_by_theme["general"])
    action = random.choice(specific_actions)

    closings = [
        "The cards illuminate possibilities, but you hold the brush that paints your future.",
        "Trust yourself - this reading is meant to empower your choices, not replace your wisdom.",
        "Return to these insights when you need reminder of what the cards revealed today.",
        "Take what serves you and release what doesn't. You are the final authority on your own path.",
        "May this reading bring clarity and courage for the journey ahead.",
        "The answers you seek are already within you - the cards simply help you remember.",
        "Walk forward with confidence, knowing you have the wisdom to navigate what comes."
    ]

    if key_card:
        card_name = get_card_base(key_card["name"])
        context = key_card["position_context"]
        # Clean up context for natural reading
        context_clean = context.lower() if context and context[0].isupper() else context
        return f"The guidance of {card_name} resonates clearly: {context_clean} {action} {random.choice(closings)}"
    else:
        return f"{action} {random.choice(closings)}"

def generate_reading(prompt_data):
    """Generate a complete, high-quality tarot reading."""
    # Seed for consistent variety
    seed_random(prompt_data["id"])

    parsed = parse_prompt(prompt_data["input_text"])

    if not parsed["cards"]:
        question = parsed.get("question", "your inquiry")
        return f"Your question '{question}' deserves thoughtful consideration. While the specific cards weren't fully captured in this reading, I encourage you to sit with your question in quiet reflection. Often our deepest knowing emerges when we create space for it. Trust your intuition - it has wisdom to offer about this situation. Consider journaling about what feels true, what fears arise, and what possibilities excite you. The answers you seek are within reach, waiting for you to quiet the noise of everyday life and listen."

    theme = get_question_theme(parsed["question"])

    paragraphs = []

    # Opening (addresses question and timing)
    paragraphs.append(generate_opening(parsed, theme))

    # Card interpretations (1-2 paragraphs depending on spread size)
    paragraphs.append(generate_card_paragraphs(parsed["cards"]))

    # Synthesis (connects themes)
    paragraphs.append(generate_synthesis(parsed))

    # Actionable insight (specific guidance)
    paragraphs.append(generate_actionable_insight(parsed, theme))

    reading = "\n\n".join(paragraphs)

    # Ensure reading is within target length (200-400 words)
    words = len(reading.split())
    if words < 200:
        # Add depth
        reflections = [
            "\n\nTake time to reflect on which card's imagery speaks most strongly to you - often our intuitive response to the visual elements carries as much meaning as the traditional interpretations.",
            "\n\nConsider revisiting this reading in a week's time to see how the themes have manifested or evolved. The cards often reveal their deeper meanings through lived experience.",
            "\n\nRemember that tarot works best as a dialogue. If certain aspects of this reading puzzle you, sit with that uncertainty - sometimes the questions matter more than quick answers.",
            "\n\nAllow yourself to return to this reading when you need guidance. The wisdom of the cards often unfolds over time, revealing new layers as your situation develops."
        ]
        reading += random.choice(reflections)

    return reading

def main():
    """Process all prompts and generate readings."""
    input_path = '/home/user/taro/training/data/batches_expanded/batch_0009.json'
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0009_responses.jsonl'

    print(f"Loading batch from {input_path}...")
    with open(input_path, 'r') as f:
        batch = json.load(f)

    total = batch["count"]
    print(f"Processing {total} prompts...")

    count = 0
    with open(output_path, 'w') as out:
        for prompt in batch["prompts"]:
            try:
                reading = generate_reading(prompt)
                response = {"id": prompt["id"], "response": reading}
                out.write(json.dumps(response, ensure_ascii=False) + '\n')
                count += 1

                if count % 100 == 0:
                    print(f"  Processed {count}/{total} prompts...")
            except Exception as e:
                print(f"  Error on prompt {prompt['id']}: {e}")
                # Write placeholder
                response = {"id": prompt["id"], "response": f"Error generating reading: {str(e)}"}
                out.write(json.dumps(response) + '\n')
                count += 1

    print(f"\n{'='*50}")
    print(f"COMPLETED: Generated {count} tarot readings")
    print(f"Output: {output_path}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
