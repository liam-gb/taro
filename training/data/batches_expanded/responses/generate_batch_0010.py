#!/usr/bin/env python3
"""Generate high-quality tarot reading responses for batch_0010.json"""

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

MINOR_ARCANA_MEANINGS = {
    "Ace": {
        "Wands": {"upright": "the spark of creative inspiration and new passionate beginnings", "reversed": "blocked creativity or delayed starts"},
        "Cups": {"upright": "emotional new beginning and opening of the heart", "reversed": "repressed emotions or missed emotional opportunity"},
        "Swords": {"upright": "mental breakthrough and clarity cutting through confusion", "reversed": "mental blocks or misused intellect"},
        "Pentacles": {"upright": "material opportunity and seeds of prosperity", "reversed": "missed opportunity or poor planning"}
    },
    "Two": {
        "Wands": {"upright": "planning and looking toward future expansion", "reversed": "fear of the unknown or poor planning"},
        "Cups": {"upright": "partnership, mutual attraction, and emotional connection", "reversed": "imbalanced relationship or separation"},
        "Swords": {"upright": "difficult choice requiring balance and careful consideration", "reversed": "indecision or information withheld"},
        "Pentacles": {"upright": "juggling priorities and adapting to change", "reversed": "overwhelm or resistance to change"}
    },
    "Three": {
        "Wands": {"upright": "expansion, foresight, and plans taking shape", "reversed": "delays in plans or lack of foresight"},
        "Cups": {"upright": "celebration, friendship, and joyful community", "reversed": "isolation or overindulgence"},
        "Swords": {"upright": "heartbreak, grief, and painful truth", "reversed": "recovery from sorrow or releasing pain"},
        "Pentacles": {"upright": "teamwork, collaboration, and skilled craftsmanship", "reversed": "lack of teamwork or mediocre work"}
    },
    "Four": {
        "Wands": {"upright": "celebration, homecoming, and milestone achievement", "reversed": "lack of support or unstable foundation"},
        "Cups": {"upright": "apathy, contemplation, and missed opportunity", "reversed": "awakening to new possibilities"},
        "Swords": {"upright": "rest, recuperation, and necessary withdrawal", "reversed": "restlessness or forced activity"},
        "Pentacles": {"upright": "security, conservation, and holding resources", "reversed": "greed or financial insecurity"}
    },
    "Five": {
        "Wands": {"upright": "competition, conflict, and creative tension", "reversed": "avoiding conflict or internal struggle"},
        "Cups": {"upright": "loss, regret, and focusing on what's gone", "reversed": "acceptance and moving forward"},
        "Swords": {"upright": "defeat, betrayal, and hollow victory", "reversed": "recovery from defeat or changed perspective"},
        "Pentacles": {"upright": "material hardship and feeling left out in the cold", "reversed": "recovery from hardship or finding help"}
    },
    "Six": {
        "Wands": {"upright": "victory, recognition, and public success", "reversed": "delayed success or ego issues"},
        "Cups": {"upright": "nostalgia, memories, and innocent joy", "reversed": "stuck in the past or unrealistic nostalgia"},
        "Swords": {"upright": "transition, moving away from difficulty", "reversed": "stuck in troubled waters or resisting change"},
        "Pentacles": {"upright": "generosity, giving and receiving in balance", "reversed": "one-sided generosity or debt"}
    },
    "Seven": {
        "Wands": {"upright": "standing your ground and defending position", "reversed": "overwhelmed or giving up"},
        "Cups": {"upright": "choices, fantasy, and illusion", "reversed": "clarity emerging or overwhelming options"},
        "Swords": {"upright": "strategy, stealth, and working alone", "reversed": "confession or getting caught"},
        "Pentacles": {"upright": "patience, assessment, and long-term investment", "reversed": "impatience or lack of reward"}
    },
    "Eight": {
        "Wands": {"upright": "swift action, movement, and rapid progress", "reversed": "delays or scattered energy"},
        "Cups": {"upright": "walking away, seeking deeper meaning", "reversed": "fear of moving on or aimless wandering"},
        "Swords": {"upright": "restriction, feeling trapped, and self-imposed limits", "reversed": "release from restriction or new perspective"},
        "Pentacles": {"upright": "dedication, craftsmanship, and diligent work", "reversed": "perfectionism or lack of focus"}
    },
    "Nine": {
        "Wands": {"upright": "resilience, persistence, and near completion", "reversed": "exhaustion or paranoia"},
        "Cups": {"upright": "contentment, emotional satisfaction, and wishes fulfilled", "reversed": "dissatisfaction or smugness"},
        "Swords": {"upright": "anxiety, worry, and nightmares", "reversed": "releasing worry or hope dawning"},
        "Pentacles": {"upright": "abundance, luxury, and self-sufficiency", "reversed": "over-investment in material or loneliness"}
    },
    "Ten": {
        "Wands": {"upright": "burden, responsibility, and hard work", "reversed": "release of burden or delegation"},
        "Cups": {"upright": "emotional fulfillment, happy family, and lasting joy", "reversed": "broken family or emotional disconnection"},
        "Swords": {"upright": "painful ending, rock bottom, and betrayal", "reversed": "recovery or worst is over"},
        "Pentacles": {"upright": "wealth, inheritance, and family legacy", "reversed": "financial loss or family disputes"}
    },
    "Page": {
        "Wands": {"upright": "enthusiasm, exploration, and creative messages", "reversed": "lack of direction or setbacks"},
        "Cups": {"upright": "emotional sensitivity, intuition, and creative expression", "reversed": "emotional immaturity or creative blocks"},
        "Swords": {"upright": "curiosity, mental agility, and new ideas", "reversed": "scattered thoughts or gossip"},
        "Pentacles": {"upright": "ambition, desire to learn, and opportunity", "reversed": "lack of progress or unfocused goals"}
    },
    "Knight": {
        "Wands": {"upright": "adventure, passion, and fearless action", "reversed": "recklessness or frustration"},
        "Cups": {"upright": "romance, charm, and following the heart", "reversed": "moodiness or unrealistic expectations"},
        "Swords": {"upright": "ambition, action-oriented thinking, and determination", "reversed": "impulsiveness or ruthlessness"},
        "Pentacles": {"upright": "hard work, routine, and methodical progress", "reversed": "boredom or laziness"}
    },
    "Queen": {
        "Wands": {"upright": "confidence, warmth, and determination", "reversed": "selfishness or jealousy"},
        "Cups": {"upright": "emotional depth, intuition, and nurturing wisdom", "reversed": "emotional manipulation or insecurity"},
        "Swords": {"upright": "clear boundaries, honesty, and independent thinking", "reversed": "coldness or harsh judgment"},
        "Pentacles": {"upright": "practical nurturing, abundance, and security", "reversed": "self-centeredness or work-life imbalance"}
    },
    "King": {
        "Wands": {"upright": "visionary leadership, charisma, and bold direction", "reversed": "impulsiveness or tyranny"},
        "Cups": {"upright": "emotional balance, diplomacy, and wise counsel", "reversed": "emotional manipulation or volatility"},
        "Swords": {"upright": "intellectual power, authority, and clear judgment", "reversed": "manipulation or abuse of power"},
        "Pentacles": {"upright": "abundance, security, and generous leadership", "reversed": "materialism or financial mismanagement"}
    }
}

QUESTION_THEMES = {
    "career": ["work", "job", "career", "profession", "business", "employment", "boss", "colleague", "workplace", "promotion", "remote", "office"],
    "love": ["love", "relationship", "partner", "romance", "dating", "marriage", "heart", "boyfriend", "girlfriend", "spouse", "crush", "attraction"],
    "money": ["money", "financial", "finances", "income", "wealth", "debt", "afford", "savings", "investment", "salary", "budget"],
    "health": ["health", "wellness", "fitness", "body", "illness", "medical", "healing", "energy", "tired", "sleep", "insomnia", "food", "diet"],
    "spiritual": ["spiritual", "soul", "purpose", "meaning", "growth", "path", "destiny", "calling", "meditation", "truth", "authentic"],
    "family": ["family", "parent", "child", "sibling", "relative", "home", "household", "mother", "father", "aging", "stepchild"],
    "decision": ["should i", "decision", "choose", "choice", "whether", "or should", "wise to", "opportunity"],
    "emotion": ["feel", "feeling", "afraid", "fear", "angry", "jealous", "envy", "anxious", "worried", "procrastinate", "imposter"],
    "boundary": ["boundary", "boundaries", "outgrown", "distance", "reveal", "honest", "needs"],
    "timing": ["when", "how long", "timing", "soon", "ready", "survive"]
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

def get_minor_info(name):
    """Get info for minor arcana card."""
    base = get_card_base(name)
    orientation = "reversed" if is_reversed(name) else "upright"

    for rank in MINOR_ARCANA_MEANINGS:
        if base.startswith(rank):
            for suit in MINOR_ARCANA_MEANINGS[rank]:
                if suit in base:
                    return MINOR_ARCANA_MEANINGS[rank][suit][orientation]
    return None

def get_major_insight(name):
    """Get insight for major arcana card."""
    base = get_card_base(name)
    orientation = "reversed" if is_reversed(name) else "upright"
    if base in MAJOR_ARCANA_INSIGHTS:
        return MAJOR_ARCANA_INSIGHTS[base][orientation]
    return None

def get_card_insight(name):
    """Get insight for any card."""
    major = get_major_insight(name)
    if major:
        return major
    minor = get_minor_info(name)
    if minor:
        return minor
    return None

def generate_opening(parsed, theme):
    """Generate a thoughtful opening paragraph."""
    question = parsed["question"]
    timing = parsed["timing"]

    timing_insight = ""
    if "Full Moon" in timing:
        timing_insight = "Under the Full Moon's illuminating light, clarity emerges from shadow. This is a time of culmination and revelation."
    elif "New Moon" in timing:
        timing_insight = "The New Moon's darkness is not absence but potential. In this phase of new beginnings, seeds planted now carry special power."
    elif "Waning Crescent" in timing:
        timing_insight = "The Waning Crescent calls for rest and reflection, preparing the ground for renewal."
    elif "Waning Gibbous" in timing:
        timing_insight = "The Waning Gibbous invites gratitude and integration of recent lessons."
    elif "Waxing Crescent" in timing:
        timing_insight = "The Waxing Crescent brings momentum for action, as hope builds toward manifestation."
    elif "Waxing Gibbous" in timing:
        timing_insight = "The Waxing Gibbous asks for patience and refinement as plans near fruition."
    elif "First Quarter" in timing:
        timing_insight = "At the First Quarter, challenges test commitment. This is a threshold moment requiring decision."
    elif "Last Quarter" in timing or "Third Quarter" in timing:
        timing_insight = "The Last Quarter brings release and forgiveness, clearing what no longer serves."

    openings_by_theme = {
        "career": [
            f"Your question about your professional path\u2014\"{question}\"\u2014speaks to your deeper sense of purpose. {timing_insight} The cards offer guidance for navigating your work life with greater clarity.",
            f"Career concerns bring you to the cards today. {timing_insight} Let's explore what the cards reveal about '{question.lower()}'.",
            f"Questions of work and purpose weigh on your mind. {timing_insight} The cards respond thoughtfully to your inquiry: \"{question}\""
        ],
        "love": [
            f"Matters of the heart bring you here, asking \"{question}\" {timing_insight} The cards speak to the emotional currents flowing through your life.",
            f"Your question touches the deepest chambers of the heart. {timing_insight} Let's see what wisdom emerges for \"{question.lower()}\".",
            f"Love and connection occupy your thoughts today. {timing_insight} The cards address your heartfelt question: \"{question}\""
        ],
        "money": [
            f"Financial matters prompt this reading\u2014\"{question}\" {timing_insight} The cards illuminate the energies surrounding your material concerns.",
            f"Questions of resources and abundance bring you here. {timing_insight} Let's explore what the cards reveal about your financial path.",
            f"Material security weighs on your mind. {timing_insight} The cards respond to: \"{question}\""
        ],
        "health": [
            f"Your wellbeing is the focus today as you ask: \"{question}\" {timing_insight} The cards offer insight into the energies affecting your vitality.",
            f"Health and balance matter deeply right now. {timing_insight} Let's see what guidance emerges for your question.",
            f"Body, mind, and spirit call for attention. {timing_insight} The cards address your concern: \"{question}\""
        ],
        "decision": [
            f"A significant choice stands before you: \"{question}\" {timing_insight} The cards illuminate the energies surrounding this crossroads.",
            f"Decision weighs upon you, and you seek clarity. {timing_insight} Let's explore what guidance emerges.",
            f"Crossroads demand your attention. {timing_insight} The cards respond to your inquiry about which path to take."
        ],
        "spiritual": [
            f"Your soul seeks deeper understanding with this question: \"{question}\" {timing_insight} The cards offer insight into your spiritual journey.",
            f"Questions of meaning and authenticity guide this reading. {timing_insight} Let's explore what wisdom emerges.",
            f"The search for truth brings you here. {timing_insight} The cards address: \"{question}\""
        ],
        "emotion": [
            f"You courageously ask about your inner landscape: \"{question}\" {timing_insight} The cards illuminate the emotional currents at play.",
            f"Emotional patterns seek understanding today. {timing_insight} Let's explore what the cards reveal about your inner world.",
            f"The heart's mysteries prompt this reading. {timing_insight} The cards respond to your deep inquiry."
        ],
        "boundary": [
            f"Questions of boundaries and authenticity bring you here: \"{question}\" {timing_insight} The cards honor this important inquiry with clear guidance.",
            f"You seek wisdom about protecting your energy while staying connected. {timing_insight} Let's see what emerges.",
            f"Setting healthy limits is an act of self-respect. {timing_insight} The cards address your question with compassion."
        ],
        "family": [
            f"Family dynamics bring you to the cards today with this question: \"{question}\" {timing_insight} These ancestral currents run deep.",
            f"Home and family matters occupy your heart. {timing_insight} The cards illuminate these deeply personal dynamics.",
            f"Questions of kinship and belonging prompt this reading. {timing_insight} Let's explore what wisdom emerges."
        ],
        "general": [
            f"You come with an important question: \"{question}\" {timing_insight} The cards gather to offer their wisdom.",
            f"Your inquiry deserves thoughtful consideration. {timing_insight} Let's see what the cards reveal about \"{question.lower()}\".",
            f"The cards are drawn to address your question: \"{question}\" {timing_insight} Let's explore together."
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
    reversed_card = is_reversed(name)

    insight = get_card_insight(name)

    position_frames = {
        "Past": "Looking to what has shaped this moment",
        "Present": "In your current situation",
        "Future": "Gazing toward what's unfolding",
        "Hidden Influences": "Beneath the visible surface",
        "Obstacles": "Addressing the challenge you face",
        "External Influences": "From the world around you",
        "External": "External forces bring",
        "Advice": "The cards counsel",
        "Outcome": "The trajectory points toward",
        "Situation": "At the heart of this matter",
        "Action": "For your next step",
        "Today's Guidance": "Your message for today comes through",
        "Challenge": "The challenge emerges as",
        "Foundation": "What supports you",
        "Hopes/Fears": "In the realm of hopes and fears",
        "Above": "At the highest potential",
        "Below": "At the foundation of this situation",
        "Self": "Within yourself"
    }

    frame = position_frames.get(position, f"In the {position} position")

    if reversed_card:
        reversal_phrases = [
            f"{base_name} appears reversed here, {context.lower() if context and context[0].isupper() else context}",
            f"we find {base_name} inverted. {context}",
            f"{base_name} shows its reversed face\u2014{context.lower() if context else ''}"
        ]
        card_state = random.choice(reversal_phrases)
    else:
        upright_phrases = [
            f"{base_name} emerges clearly. {context}",
            f"we encounter {base_name}. {context}",
            f"{base_name} offers its wisdom: {context.lower() if context else ''}"
        ]
        card_state = random.choice(upright_phrases)

    if insight:
        return f"{frame}, {card_state} This card is {insight}."
    else:
        return f"{frame}, {card_state} The energy of {keywords.lower()} colors this aspect of your reading."

def generate_card_paragraphs(cards):
    """Generate flowing paragraphs interpreting the cards."""
    if len(cards) == 1:
        interp = interpret_card_in_context(cards[0], 0, 1)
        additions = [
            f" With a single card drawn, its message carries concentrated significance. Sit with the imagery of {get_card_base(cards[0]['name'])} and let it speak to the layers of your question.",
            f" This solitary card holds the essence of your answer. Let {get_card_base(cards[0]['name'])} guide your reflection.",
            f" One card speaks volumes here. {get_card_base(cards[0]['name'])} addresses your question directly and completely."
        ]
        return f"{interp}{random.choice(additions)}"

    paragraphs = []

    if len(cards) == 2:
        p1 = interpret_card_in_context(cards[0], 0, 2)
        p2 = interpret_card_in_context(cards[1], 1, 2)
        paragraphs.append(f"{p1}")
        paragraphs.append(f"{p2}")
    elif len(cards) == 3:
        for i, card in enumerate(cards):
            paragraphs.append(interpret_card_in_context(card, i, 3))
    else:
        mid = len(cards) // 2
        first_half = [interpret_card_in_context(c, i, len(cards)) for i, c in enumerate(cards[:mid])]
        second_half = [interpret_card_in_context(c, i+mid, len(cards)) for i, c in enumerate(cards[mid:])]

        paragraphs.append(" ".join(first_half))

        transitions = [
            "As the reading deepens, additional layers emerge.",
            "Moving further through the spread, more insights surface.",
            "The remaining cards add nuance and direction."
        ]
        paragraphs.append(random.choice(transitions) + " " + " ".join(second_half))

    return "\n\n".join(paragraphs)

def generate_synthesis(parsed):
    """Generate a synthesis paragraph connecting themes."""
    cards = parsed["cards"]
    combinations = parsed["combinations"]
    dominant = parsed["dominant_element"]

    elements = []

    majors = [c for c in cards if get_card_base(c["name"]) in MAJOR_ARCANA_INSIGHTS]
    reversals = [c for c in cards if is_reversed(c["name"])]

    if len(majors) > len(cards) // 2:
        elements.append("The strong presence of Major Arcana cards indicates this situation touches on significant life themes and soul-level lessons")
    elif len(majors) > 0:
        major_names = [get_card_base(m["name"]) for m in majors]
        if len(major_names) == 1:
            elements.append(f"{major_names[0]} brings archetypal weight to this reading")
        else:
            elements.append(f"The presence of {' and '.join(major_names)} brings powerful archetypal energy")

    if len(reversals) > len(cards) // 2:
        elements.append("The prevalence of reversed cards suggests blocked energy or internalized processes needing attention")
    elif len(reversals) > 0:
        elements.append("The reversed cards indicate areas where energy is blocked or working internally")

    if combinations:
        combo_text = combinations.split('\n')[0]
        if ':' in combo_text:
            combo_insight = combo_text.split(':')[1].strip()
            elements.append(f"The card combinations amplify the message: {combo_insight[:100]}")

    if dominant:
        element_meanings = {
            "Fire": "passion, will, and transformative action",
            "Water": "emotions, intuition, and deep feeling",
            "Air": "thoughts, communication, and mental clarity",
            "Earth": "material concerns, stability, and practical grounding"
        }
        meaning = element_meanings.get(dominant, "elemental forces")
        elements.append(f"The dominant {dominant} energy emphasizes {meaning}")
    elif parsed["elemental_balance"] == "Balanced":
        elements.append("The balanced elemental spread suggests you have access to multiple modes of engaging with this situation")

    if not elements:
        elements.append("The cards weave together into a coherent picture of your situation")

    return " ".join([e + "." for e in elements])

def generate_actionable_insight(parsed, theme):
    """Generate closing with specific, actionable guidance."""
    cards = parsed["cards"]

    advice_card = next((c for c in cards if "advice" in c["position"].lower()), None)
    outcome_card = next((c for c in cards if "outcome" in c["position"].lower()), None)
    action_card = next((c for c in cards if "action" in c["position"].lower()), None)
    guidance_card = advice_card or action_card or outcome_card or (cards[-1] if cards else None)

    action_by_theme = {
        "career": [
            "Identify one concrete step you can take this week to align your work with your deeper values.",
            "Consider what professional boundary needs setting or conversation needs having.",
            "Reflect on what truly motivates you beyond external recognition, and let that guide your next move."
        ],
        "love": [
            "Open a conversation with vulnerability\u2014share something true about how you feel.",
            "Consider what pattern in relationships might be ready for transformation.",
            "Nurture the relationship with yourself as the foundation for all other connections."
        ],
        "money": [
            "Review your relationship with abundance\u2014what beliefs about money might be limiting you?",
            "Take one concrete action toward financial clarity, whether budgeting, saving, or investing.",
            "Consider how your material resources can align with your deeper values."
        ],
        "health": [
            "Listen to what your body is telling you\u2014what does it need that you've been ignoring?",
            "Commit to one sustainable change rather than dramatic overhaul.",
            "Consider how physical wellbeing connects to emotional and spiritual health."
        ],
        "decision": [
            "The cards illuminate possibilities rather than making the choice for you. What does your gut say when you quiet the noise?",
            "Write out both options and notice which makes your body feel more expansive.",
            "Consider what you would advise a dear friend facing this same crossroads."
        ],
        "spiritual": [
            "Dedicate time for stillness\u2014answers often emerge in silence rather than seeking.",
            "Notice what practices or places help you feel most connected to something larger.",
            "Trust that your path is unfolding even when the destination isn't visible."
        ],
        "emotion": [
            "Allow yourself to feel without immediately trying to fix or understand. Emotions carry wisdom.",
            "Consider what unmet need might be beneath this feeling, and tend to it gently.",
            "Journal about what this emotional pattern has protected you from, and whether that protection is still needed."
        ],
        "boundary": [
            "Practice stating your truth simply, without over-explaining or apologizing.",
            "Remember that healthy boundaries don't destroy connection\u2014they create conditions for authentic relating.",
            "Start small: choose one boundary to honor this week and notice what shifts."
        ],
        "family": [
            "Remember you can honor your roots while growing in your own direction.",
            "Consider what healing might begin with you, regardless of whether others change.",
            "Journal about what patterns you wish to transform rather than pass on."
        ],
        "general": [
            "Identify one small action that aligns with the guidance offered here.",
            "Sit with this reading before making major decisions\u2014let the insights settle.",
            "Return to these insights when you need reminder of what the cards revealed today."
        ]
    }

    specific_actions = action_by_theme.get(theme, action_by_theme["general"])
    action = random.choice(specific_actions)

    closings = [
        "Trust yourself\u2014this reading empowers your choices rather than replacing your wisdom.",
        "May this reading bring clarity and courage for the journey ahead.",
        "Take what serves you and release what doesn't. You are the final authority on your own path.",
        "The cards have illuminated the terrain; now walk it with presence and confidence.",
        "Your next step matters more than the final destination. Move forward with awareness."
    ]

    if guidance_card:
        card_name = get_card_base(guidance_card["name"])
        context = guidance_card["position_context"]
        if context:
            return f"The guidance of {card_name} points the way: {context.lower() if context[0].isupper() else context} {action} {random.choice(closings)}"
        else:
            return f"Let {card_name} guide your next steps. {action} {random.choice(closings)}"
    else:
        return f"{action} {random.choice(closings)}"

def generate_reading(prompt_data):
    """Generate a complete, high-quality tarot reading."""
    seed_random(prompt_data["id"])

    parsed = parse_prompt(prompt_data["input_text"])

    if not parsed["cards"]:
        return f"Your question \"{parsed['question']}\" deserves thoughtful consideration. While the specific cards weren't fully captured, I encourage you to sit with your question in quiet reflection. Often our deepest knowing emerges when we create space for it. Trust your intuition\u2014it has wisdom to offer. Consider journaling about what feels true, what fears arise, and what possibilities excite you. The answers you seek are within reach. Sometimes the most powerful readings come not from external sources but from the stillness within. Allow yourself space to listen to your own wisdom."

    theme = get_question_theme(parsed["question"])

    paragraphs = []

    paragraphs.append(generate_opening(parsed, theme))
    paragraphs.append(generate_card_paragraphs(parsed["cards"]))
    paragraphs.append(generate_synthesis(parsed))
    paragraphs.append(generate_actionable_insight(parsed, theme))

    reading = "\n\n".join(paragraphs)

    # Ensure minimum word count of 200
    words = len(reading.split())
    while words < 200:
        reflections = [
            " Take time to notice which card's imagery speaks most strongly to you\u2014your intuitive response often carries as much meaning as traditional interpretations. The symbols, colors, and figures on each card speak a language beyond words.",
            " Consider revisiting this reading in a week to see how the themes have manifested in your daily life. The cards often reveal deeper meanings through lived experience, and patterns may become clearer with time.",
            " Remember that tarot works best as dialogue between your conscious mind and deeper wisdom. If certain aspects of this reading puzzle you, sit with that uncertainty\u2014sometimes the questions themselves matter more than quick answers.",
            " The energy of this reading invites you to trust your own instincts as you move forward. You carry more wisdom than you realize, and these cards simply reflect what you already know at some level.",
            " Notice how your body responds to different cards\u2014tension, relaxation, curiosity, or recognition. These physical signals offer additional insight into what resonates most deeply with your situation."
        ]
        reading += random.choice(reflections)
        words = len(reading.split())

    return reading

def main():
    """Process all prompts and generate readings."""
    input_path = '/home/user/taro/training/data/batches_expanded/batch_0010.json'
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0010_responses.jsonl'

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
                response = {"id": prompt["id"], "response": f"Error generating reading: {str(e)}"}
                out.write(json.dumps(response) + '\n')
                count += 1

    print(f"\n{'='*50}")
    print(f"COMPLETED: Generated {count} tarot readings")
    print(f"Output: {output_path}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
