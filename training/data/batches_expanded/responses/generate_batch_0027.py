#!/usr/bin/env python3
"""Generate tarot reading responses for batch_0027 - Final version targeting 200-400 words."""

import json
import re
import random
import hashlib

# Load batch data
with open('/home/user/taro/training/data/batches_expanded/batch_0027.json', 'r') as f:
    batch_data = json.load(f)

def parse_input_text(input_text):
    """Parse the input text to extract timing, question, cards, and other info."""
    result = {
        'timing': None,
        'timing_meaning': None,
        'question': None,
        'cards': [],
        'combinations': [],
        'elemental_balance': None,
        'elemental_flow': None,
        'dominant_element': None
    }

    timing_match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    if timing_match:
        timing_full = timing_match.group(1).strip()
        if '—' in timing_full:
            parts = timing_full.split('—', 1)
            result['timing'] = parts[0].strip()
            result['timing_meaning'] = parts[1].strip()
        else:
            result['timing'] = timing_full

    question_match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    if question_match:
        result['question'] = question_match.group(1).strip()

    card_pattern = r'(\d+)\.\s+([^:]+):\s+([^\n]+)\n\s*Keywords:\s*([^\n]+)\n\s*Base meaning:\s*([^\n]+)\n\s*Position context:\s*([^\n]+(?:\n(?!\d+\.)(?!Card Combinations)(?!Elemental)[^\n]+)*)'
    for match in re.finditer(card_pattern, input_text):
        card = {
            'number': int(match.group(1)),
            'position': match.group(2).strip(),
            'name': match.group(3).strip(),
            'keywords': match.group(4).strip(),
            'base_meaning': match.group(5).strip(),
            'position_context': match.group(6).strip()
        }
        card['reversed'] = '(reversed)' in card['name'].lower()
        card['name_clean'] = card['name'].replace('(reversed)', '').replace('(upright)', '').strip()
        result['cards'].append(card)

    combo_section = re.search(r'Card Combinations:\n(.*?)(?=\nElemental Balance:|\Z)', input_text, re.DOTALL)
    if combo_section:
        combo_text = combo_section.group(1)
        for line in combo_text.strip().split('\n'):
            if line.startswith('-'):
                result['combinations'].append(line[1:].strip())

    elem_match = re.search(r'Elemental Balance:\s*([^\n]+)', input_text)
    if elem_match:
        result['elemental_balance'] = elem_match.group(1).strip()

    dom_match = re.search(r'Dominant:\s*([^\n]+)', input_text)
    if dom_match:
        result['dominant_element'] = dom_match.group(1).strip()

    return result

def seeded_choice(seed_str, options):
    hash_val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    return options[hash_val % len(options)]

def seeded_sample(seed_str, options, k):
    hash_val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    random.seed(hash_val)
    return random.sample(options, min(k, len(options)))

def get_question_theme(question):
    q = question.lower()
    if any(w in q for w in ['love', 'relationship', 'partner', 'heart', 'romance', 'dating', 'marriage', 'boyfriend', 'girlfriend', 'spouse', 'attract', 'soulmate', 'crush']):
        return 'love'
    elif any(w in q for w in ['career', 'job', 'work', 'professional', 'money', 'financial', 'salary', 'business', 'income', 'promotion', 'boss', 'colleague']):
        return 'career'
    elif any(w in q for w in ['family', 'parent', 'mother', 'father', 'sibling', 'child', 'daughter', 'son', 'relative', 'ancestor']):
        return 'family'
    elif any(w in q for w in ['heal', 'health', 'anxiety', 'depression', 'fear', 'anger', 'emotion', 'feeling', 'mental', 'therapy', 'trauma', 'pain', 'grief', 'hurt']):
        return 'healing'
    elif any(w in q for w in ['purpose', 'meaning', 'direction', 'path', 'calling', 'spiritual', 'soul', 'growth', 'evolve', 'destiny']):
        return 'purpose'
    elif any(w in q for w in ['decision', 'choice', 'should i', 'will i', 'when will', 'how long', 'what if', 'move', 'change']):
        return 'decision'
    elif any(w in q for w in ['creative', 'art', 'write', 'music', 'project', 'passion', 'dream', 'create', 'express']):
        return 'creative'
    elif any(w in q for w in ['friend', 'social', 'community', 'belong', 'lonely', 'connection', 'people']):
        return 'social'
    else:
        return 'general'

def generate_reading(prompt_id, question, parsed):
    """Generate a tarot reading response targeting 200-400 words, 3-5 paragraphs."""
    cards = parsed['cards']
    timing = parsed['timing'] or 'This moment'
    timing_meaning = parsed['timing_meaning'] or 'a time of reflection and attention'
    combinations = parsed['combinations']
    elemental_balance = parsed['elemental_balance'] or 'Balanced'
    dominant = parsed['dominant_element'] or elemental_balance
    theme = get_question_theme(question)
    num_cards = len(cards)

    if not cards:
        return f"Your question \"{question}\" invites deep reflection. The cards encourage you to trust your inner wisdom and take mindful steps forward. This is a time for patience and self-trust. Allow the insights you already possess to surface through quiet contemplation."

    paragraphs = []

    # === PARAGRAPH 1: Opening (longer for fewer cards) ===
    openings = [
        f"Your question—\"{question}\"—touches on matters that deserve careful attention and honest reflection. This is not a light inquiry, and the cards respond with meaningful depth.",
        f"You ask: \"{question}\" This question carries real significance, and the cards have gathered with wisdom to share. There is something here worth listening to carefully.",
        f"The question you bring—\"{question}\"—opens a doorway to understanding what moves beneath the surface of your situation. The cards reveal patterns that may have been difficult to see clearly.",
        f"\"{question}\"—this inquiry reveals your readiness to look honestly at where you are and where you might be heading. The cards honor this willingness with direct insight.",
        f"Your heart asks: \"{question}\" The cards have assembled to illuminate the path before you, offering perspective on both what is and what may become.",
        f"In asking \"{question}\" you demonstrate the courage to seek clarity where confusion has dwelt. The cards respond to this openness with guidance worth considering.",
    ]

    timing_phrases = [
        f"Under the {timing}, the emphasis falls on {timing_meaning.lower()}—and this lunar phase colors everything the cards reveal today.",
        f"The {timing} brings its particular energy of {timing_meaning.lower()} to bear on your question, shaping how these messages are best received.",
        f"With the {timing} overhead, we are reminded that {timing_meaning.lower()} is the appropriate stance for receiving this guidance.",
        f"This {timing} phase underscores the importance of {timing_meaning.lower()} as you navigate what the cards show.",
    ]

    opening = seeded_choice(prompt_id + "open1", openings)
    timing_phrase = seeded_choice(prompt_id + "time1", timing_phrases)
    para1 = f"{opening} {timing_phrase}"
    paragraphs.append(para1)

    # === PARAGRAPH 2-3: Card Interpretations ===
    def build_card_interpretation(card, seed, detailed=False):
        pos = card['position']
        name = card['name']
        reversed_status = card['reversed']
        position_context = card['position_context']
        keywords = card['keywords']

        intros = [
            f"The {name} appears in your {pos} position",
            f"In the {pos} position, {name} emerges with clarity",
            f"For your {pos}, the cards show {name}",
            f"{name} occupies the significant {pos} position",
            f"Looking at {pos}, we find {name} speaking directly to your question",
        ]
        intro = seeded_choice(seed + pos, intros)

        if reversed_status:
            reversal_notes = [
                "and appearing reversed, it signals that this energy may be blocked, internalized, or expressing through shadow patterns that require conscious attention",
                "—reversed here, suggesting the energy is turned inward, meeting internal resistance, or asking for deeper examination before it can fully express",
                "which in its reversed aspect points to delays, internal processing, or an inverted expression of its natural qualities that calls for awareness",
                "and this reversal indicates the card's energy requires patient integration rather than immediate external action",
            ]
            reversal = seeded_choice(seed + name + "rev", reversal_notes)
            return f"{intro}, {reversal}. {position_context}"
        else:
            if detailed:
                bridges = [
                    f", bringing its clear energy of {keywords.split(',')[0].strip().lower()} to this part of your reading. {position_context}",
                    f". In this position, the card speaks with directness. {position_context}",
                    f", radiating its essential quality of {keywords.split(',')[0].strip().lower()}. {position_context}",
                ]
            else:
                bridges = [
                    f". {position_context}",
                    f", bringing its energy of {keywords.split(',')[0].strip().lower()}. {position_context}",
                    f". Here, {position_context}",
                ]
            bridge = seeded_choice(seed + name + "bridge", bridges)
            return f"{intro}{bridge}"

    # Adjust detail level based on card count
    detailed = num_cards <= 4
    card_interpretations = [build_card_interpretation(c, prompt_id, detailed) for c in cards]

    if num_cards <= 3:
        card_intro = seeded_choice(prompt_id + "cintro", [
            "Let us examine what the cards reveal in this spread.",
            "The cards drawn speak with clarity to your situation.",
            "Here is what the spread shows:",
        ])
        card_para = f"{card_intro} " + " ".join(card_interpretations)
        paragraphs.append(card_para)
    elif num_cards <= 6:
        mid = num_cards // 2
        first_cards = card_interpretations[:mid]
        second_cards = card_interpretations[mid:]

        trans1 = seeded_choice(prompt_id + "tr1", [
            "Let us begin with the foundational cards in this spread, as they establish important context.",
            "The reading opens with significant imagery that sets the stage for understanding.",
            "Examining the first cards drawn reveals the groundwork of your situation.",
        ])
        trans2 = seeded_choice(prompt_id + "tr2", [
            "The remaining cards deepen and extend this message with additional perspective.",
            "Continuing through the spread, further insight emerges to complete the picture.",
            "The additional cards add important nuance and direction to the reading.",
        ])
        paragraphs.append(f"{trans1} " + " ".join(first_cards))
        paragraphs.append(f"{trans2} " + " ".join(second_cards))
    else:
        third = num_cards // 3
        paragraphs.append("The spread begins with crucial context for understanding your situation. " + " ".join(card_interpretations[:third]))
        paragraphs.append("Moving deeper into the reading, additional layers become visible. " + " ".join(card_interpretations[third:2*third]))
        paragraphs.append("The final cards complete the picture with guidance for your path forward. " + " ".join(card_interpretations[2*third:]))

    # === PARAGRAPH: Card Combinations (if present, otherwise skip) ===
    if combinations and len(combinations) >= 2:
        combo_intros = [
            "When we observe how these cards interact, deeper patterns emerge that reinforce the reading's core message.",
            "The relationships between cards amplify certain themes worth noting carefully.",
            "Notable combinations in this spread reveal additional layers of meaning.",
        ]
        combo_intro = seeded_choice(prompt_id + "combo", combo_intros)
        selected = seeded_sample(prompt_id + "combos", combinations, min(2, len(combinations)))
        combo_text = " ".join(selected)
        paragraphs.append(f"{combo_intro} {combo_text}")

    # === PARAGRAPH: Synthesis, Elemental, and Theme ===
    elem_meanings = {
        'Water': "emotional intelligence, intuitive knowing, and the wisdom that flows from deep feeling",
        'Fire': "passionate action, transformative courage, and the spark of creative will that drives change",
        'Air': "mental clarity, honest communication, and the liberating power of speaking and hearing truth",
        'Earth': "practical wisdom, patient building, and trust in gradual, solid progress over time",
        'Balanced': "integration of thinking, feeling, doing, and grounding—a harmonious blend of all approaches",
    }
    elem_desc = elem_meanings.get(dominant.split()[0] if dominant else 'Balanced', "balanced elemental energy supporting holistic wisdom")

    theme_synths = {
        'love': [
            "These cards speak to your heart's journey with honesty and compassion, acknowledging both the risks and rewards of authentic connection.",
            "The reading acknowledges both the vulnerability and strength present in matters of the heart, inviting you to honor both.",
            "Love requires courage, and these cards honor your willingness to engage authentically even when the outcome remains uncertain.",
        ],
        'career': [
            "Your professional path is illuminated by these cards with practical wisdom that balances ambition with deeper purpose.",
            "The reading speaks to the intersection of career goals and personal values, inviting alignment between what you do and who you are.",
            "Work and purpose interweave in this spread, suggesting that material success becomes meaningful when rooted in authentic contribution.",
        ],
        'family': [
            "Family patterns run deep, and these cards acknowledge the complexity of bonds that shape us from our earliest days.",
            "The reading honors both loyalty to your roots and your right to grow beyond inherited limitations into your own becoming.",
            "These ancestral threads shape who you are, yet you retain power over how you weave them into the life you choose to create.",
        ],
        'healing': [
            "Healing is rarely linear, and these cards honor the courage it takes to face what hurts rather than turning away.",
            "The reading recognizes that genuine wholeness includes integrating shadow and light alike, not rejecting any part of yourself.",
            "Your willingness to look honestly at painful patterns is itself a healing act, and the cards reflect this back to you.",
        ],
        'purpose': [
            "Questions of meaning and direction require patience, and these cards honor your seeking without rushing you toward false certainty.",
            "Purpose often reveals itself through faithful attention to what genuinely calls to you, even when the path seems unclear.",
            "The reading suggests that clarity comes not from forcing answers but from following what resonates and trusting the unfolding.",
        ],
        'decision': [
            "Choice points carry weight, and these cards help illuminate what matters most as you navigate this crossroads.",
            "The reading invites you to consider not just outcomes but alignment with your deepest values as you decide.",
            "Decisions become clearer when you understand what you truly wish to honor and protect through your choosing.",
        ],
        'creative': [
            "Creative energy flows through these cards with invitation and encouragement for your expressive nature.",
            "The reading speaks to the courage required to bring inner vision into tangible form despite doubt.",
            "Your creative impulses deserve attention and trust—these cards affirm that the urge to create is meaningful.",
        ],
        'social': [
            "Connection and belonging are fundamental needs, and these cards speak to how you navigate the space between self and others.",
            "The reading acknowledges both your longing for community and your unique individuality that seeks authentic expression.",
            "Genuine relationship requires showing up as you truly are, and these cards encourage that authenticity.",
        ],
        'general': [
            "These cards weave together into guidance worth sitting with patiently, allowing the insights to settle into understanding.",
            "The reading offers perspective that may deepen with contemplation over the coming days as circumstances evolve.",
            "Trust that the patterns here speak to what you most need to recognize and work with at this particular moment.",
        ]
    }

    synth_phrase = seeded_choice(prompt_id + "synth", theme_synths.get(theme, theme_synths['general']))
    elem_phrase = f"The {dominant} energy pervading this reading emphasizes {elem_desc}."
    paragraphs.append(f"{synth_phrase} {elem_phrase}")

    # === PARAGRAPH: Actionable Insight ===
    action_pools = {
        'love': [
            "reflect on what you genuinely need from relationship, separate from what you think you should want or what others expect of you. Practice expressing one honest feeling this week without over-explaining or apologizing for it",
            "consider where fear may be disguising itself as caution or wisdom. True vulnerability is strength, and these cards encourage you to risk being seen even when that feels uncomfortable",
            "examine your expectations carefully—are they invitations or demands? Sometimes softening our grip on specific outcomes opens doors we had given up on",
            "honor your boundaries while remaining genuinely open to connection. You can protect yourself and still allow love in—these are not contradictory",
        ],
        'career': [
            "identify one concrete step toward your professional goals you can take this week, however small it may seem. Momentum builds through consistent action over time",
            "reflect honestly on whether your current path serves your deeper values or merely meets external expectations. Alignment between work and purpose matters more than achievement alone",
            "practice articulating your worth clearly and without apology. Preparation creates genuine confidence, and confidence naturally invites the recognition you deserve",
            "consider what would bring more meaning to your daily work, and take one specific step in that direction this week",
        ],
        'family': [
            "set one small boundary that honors your wellbeing while respecting the relationship. You can love your family and still protect your peace—both can be true simultaneously",
            "notice which inherited patterns genuinely serve your life and which you are ready to release. This awareness is itself the beginning of transformation",
            "practice seeing a family member as they are now, not only through the lens of accumulated past hurt. People do change, and allowing for that serves you",
            "honor your roots while claiming your right to grow in your own direction. Loyalty does not require self-abandonment",
        ],
        'healing': [
            "create space for difficult feelings without forcing resolution or rushing toward feeling better. Sometimes emotions simply need patient witnessing before they can transform",
            "commit to one supportive practice this week, however modest—something that nourishes your wellbeing rather than numbing your pain",
            "speak to yourself as you would to someone you dearly love. Self-compassion is not weakness or self-indulgence; it is medicine for the spirit",
            "take one small action toward what you know supports your healing, even if motivation is absent today. Start anyway, and feeling often follows action",
        ],
        'purpose': [
            "pay close attention this week to what makes time disappear, what absorbs you completely. These moments of flow contain important clues about your calling",
            "release the need to see the entire path laid out before you. The next step is enough. Take that step faithfully, and the following one will reveal itself",
            "notice recurring themes in your life—people, situations, or interests that keep returning. What persists may be pointing toward purpose",
            "practice sitting in not-knowing without rushing to fill the silence with premature answers. Real clarity often arrives when we stop demanding it",
        ],
        'decision': [
            "write out your options and notice which creates a feeling of expansion in your body versus contraction. Learn to trust that physical signal as important information",
            "consider what you would choose if fear were truly removed from the equation. That clarity matters even if fear cannot be completely eliminated",
            "set a clear deadline for deciding, remembering that not choosing is itself a consequential choice. Prolonged indecision has its own costs",
            "take one small experimental step in a direction and observe carefully how it feels. Sometimes reality clarifies what imagination alone cannot",
        ],
        'creative': [
            "protect time this week for your creative work—even fifteen minutes matters. Show up with consistency and the creative flow will increasingly meet you there",
            "release perfectionism and give yourself full permission to create badly at first. Volume and practice precede mastery in all creative endeavors",
            "share something you have made with one trusted person this week. Creative work grows stronger through being witnessed and received",
            "notice what you have been avoiding creating and gently move toward it despite the resistance. The avoidance often marks what matters most",
        ],
        'social': [
            "reach out to one person this week without any agenda—simply to connect and offer presence. This gift of attention often matters more than we realize",
            "notice where you habitually hide yourself in relationship and practice one small honest reveal. Authentic self-disclosure invites genuine intimacy",
            "examine beliefs about belonging that may be keeping you unnecessarily isolated. You are likely more welcome than your fears allow you to believe",
            "offer something concrete—help, focused attention, your time—to someone in your community this week. Genuine connection grows through giving",
        ],
        'general': [
            "sit with this reading for a full day before taking any major action. Allow the insights time to settle into deeper knowing and integration",
            "journal about which card spoke most powerfully to you and explore what it stirs. That particular card likely holds a key teaching for you now",
            "identify one concrete step you can take this week that genuinely aligns with this guidance. Small aligned actions compound into meaningful change",
            "return to this reading in a few days and notice what has shifted in your understanding. Insight often deepens with time and reflection",
        ]
    }

    closers = [
        "Trust your own wisdom as you integrate what the cards have shown you today.",
        "The cards have spoken their piece; now it is yours to carry forward with conscious intention.",
        "May this reading serve your highest good and illuminate your clearest path ahead.",
        "What ultimately matters is what you choose to do with the insight you have received here.",
    ]

    action = seeded_choice(prompt_id + "action", action_pools.get(theme, action_pools['general']))
    closer = seeded_choice(prompt_id + "closer", closers)
    final_para = f"Your path forward invites you to {action}. {closer}"
    paragraphs.append(final_para)

    response = "\n\n".join(paragraphs)
    return response


# Generate all responses
output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0027_responses.jsonl'

with open(output_path, 'w') as f:
    for i, prompt in enumerate(batch_data['prompts']):
        prompt_id = prompt['id']
        question = prompt['question']
        input_text = prompt['input_text']

        parsed = parse_input_text(input_text)
        response = generate_reading(prompt_id, question, parsed)

        output_line = json.dumps({"id": prompt_id, "response": response})
        f.write(output_line + '\n')

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/500 prompts")

print(f"Completed! Generated {len(batch_data['prompts'])} responses to {output_path}")
