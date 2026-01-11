#!/usr/bin/env python3
"""
Generate tarot reading responses for batch_0005.json
Creates unique, contextual readings based on cards, positions, and questions.
"""

import json
import re
import random
import hashlib

def extract_cards_from_input(input_text):
    """Parse input_text to extract card information."""
    cards = []
    lines = input_text.split('\n')

    current_card = None
    for line in lines:
        # Match card lines like "1. Position: Card Name (orientation)"
        card_match = re.match(r'\d+\.\s+([^:]+):\s+(.+?)\s*\((upright|reversed)\)', line)
        if card_match:
            position = card_match.group(1).strip()
            card_name = card_match.group(2).strip()
            orientation = card_match.group(3)
            current_card = {
                'position': position,
                'name': card_name,
                'reversed': orientation == 'reversed',
                'keywords': '',
                'context': '',
                'base_meaning': ''
            }
            cards.append(current_card)
        elif current_card and line.strip().startswith('Keywords:'):
            current_card['keywords'] = line.replace('Keywords:', '').strip()
        elif current_card and line.strip().startswith('Position context:'):
            current_card['context'] = line.replace('Position context:', '').strip()
        elif current_card and line.strip().startswith('Base meaning:'):
            current_card['base_meaning'] = line.replace('Base meaning:', '').strip()

    return cards

def extract_question(input_text):
    """Extract the question from input_text."""
    match = re.search(r'QUESTION:\s*"([^"]+)"', input_text)
    return match.group(1) if match else ""

def extract_timing(input_text):
    """Extract moon phase/timing from input_text."""
    match = re.search(r'TIMING:\s*([^\n]+)', input_text)
    return match.group(1) if match else ""

def extract_combinations(input_text):
    """Extract card combinations from input_text."""
    combinations = []
    in_combos = False
    lines = input_text.split('\n')
    for line in lines:
        if 'Card Combinations:' in line:
            in_combos = True
            continue
        if in_combos:
            if line.strip().startswith('-'):
                combinations.append(line.strip()[2:])
            elif line.strip().startswith('Elemental') or not line.strip():
                break
    return combinations

def get_card_essence(card_name, reversed=False):
    """Get the essential meaning of a card."""
    essences = {
        # Major Arcana
        'The Fool': ('fresh beginnings, innocent trust, spontaneous leaps', 'blocked starts, reckless choices, fear of the unknown'),
        'The Magician': ('manifestation power, aligned will, skillful action', 'manipulation, scattered focus, untapped potential'),
        'The High Priestess': ('intuitive wisdom, hidden knowledge, inner mystery', 'ignored intuition, secrets revealed, disconnection from inner self'),
        'The Empress': ('abundant nurturing, creative fertility, sensual pleasure', 'creative blocks, smothering love, neglected self-care'),
        'The Emperor': ('structured authority, protective boundaries, disciplined leadership', 'rigid control, absent authority, power struggles'),
        'The Hierophant': ('traditional wisdom, spiritual guidance, established paths', 'breaking conventions, questioning traditions, personal truth'),
        'The Lovers': ('meaningful choice, aligned values, deep connection', 'misaligned values, difficult choices, relationship discord'),
        'The Chariot': ('determined progress, willpower triumph, directed momentum', 'loss of direction, scattered effort, external obstacles'),
        'Strength': ('gentle courage, patient mastery, compassionate power', 'self-doubt, raw emotions, force over patience'),
        'The Hermit': ('inner wisdom, solitary reflection, guiding light', 'isolation, avoiding introspection, lost in darkness'),
        'Wheel of Fortune': ('destined turning points, cycles of change, fate in motion', 'resistance to change, bad luck, stuck cycles'),
        'Justice': ('fair outcomes, truth revealed, balanced decisions', 'unfairness, dishonesty, avoided accountability'),
        'The Hanged Man': ('willing surrender, shifted perspective, sacred pause', 'stalling, martyrdom, resistance to necessary sacrifice'),
        'Death': ('profound transformation, necessary endings, rebirth', 'resisting change, stagnation, fear of transformation'),
        'Temperance': ('balanced integration, patient alchemy, harmonious flow', 'imbalance, excess, lack of moderation'),
        'The Devil': ('shadow awareness, material attachment, binding patterns', 'breaking free, releasing bonds, facing shadows'),
        'The Tower': ('sudden revelation, necessary destruction, liberating breakdown', 'avoided disaster, internal upheaval, fear of change'),
        'The Star': ('renewed hope, healing faith, inspired guidance', 'lost hope, disconnection from purpose, dimmed faith'),
        'The Moon': ('intuitive depths, unconscious stirrings, illusive paths', 'confusion clearing, fears faced, hidden things revealed'),
        'The Sun': ('radiant joy, vital success, illuminated truth', 'dimmed joy, delayed success, clouded clarity'),
        'Judgement': ('awakened calling, liberating reckoning, renewed purpose', 'self-judgment, avoided calling, deaf to inner truth'),
        'The World': ('complete integration, achieved wholeness, fulfilled cycles', 'incomplete journey, delayed completion, unfinished business'),

        # Wands
        'Ace of Wands': ('creative spark, passionate beginning, inspired potential', 'blocked creativity, false starts, diminished passion'),
        'Two of Wands': ('planning vision, personal power, future choices', 'fear of action, limited vision, indecision'),
        'Three of Wands': ('expanding horizons, ventures in motion, waiting for ships', 'delays in progress, limited expansion, frustrated plans'),
        'Four of Wands': ('joyful celebration, stable foundation, community harmony', 'disrupted celebration, unstable home, lack of support'),
        'Five of Wands': ('healthy competition, creative conflict, growth through challenge', 'avoided conflict, overwhelming competition, scattered energy'),
        'Six of Wands': ('public recognition, victory achieved, leadership acknowledged', 'private success, delayed recognition, fear of visibility'),
        'Seven of Wands': ('defensive position, standing ground, maintaining advantage', 'overwhelmed defense, giving up position, exhausted fighting'),
        'Eight of Wands': ('swift movement, aligned momentum, rapid progress', 'delays, scattered arrows, stalled momentum'),
        'Nine of Wands': ('resilient persistence, wounded but standing, final defense', 'exhausted resistance, paranoid defense, unwilling to continue'),
        'Ten of Wands': ('heavy burdens, responsibility carried, approaching completion', 'delegated burdens, released responsibilities, refusing to carry more'),
        'Page of Wands': ('curious exploration, creative message, enthusiastic beginning', 'blocked enthusiasm, delayed news, immature approach'),
        'Knight of Wands': ('bold pursuit, passionate action, adventurous charge', 'reckless haste, scattered direction, burnout'),
        'Queen of Wands': ('confident warmth, magnetic leadership, creative mastery', 'diminished confidence, jealous control, burned-out creativity'),
        'King of Wands': ('visionary command, inspiring authority, entrepreneurial mastery', 'tyrannical control, impulsive leadership, vision without follow-through'),

        # Cups
        'Ace of Cups': ('emotional beginning, love offered, spiritual opening', 'blocked emotions, repressed feelings, love refused'),
        'Two of Cups': ('mutual connection, balanced partnership, heart meeting', 'imbalanced relationship, broken connection, disharmony'),
        'Three of Cups': ('joyful community, friendship celebration, shared happiness', 'isolation, excess indulgence, friendship troubles'),
        'Four of Cups': ('contemplative withdrawal, offered opportunity, emotional apathy', 'emerging interest, accepted offer, ending withdrawal'),
        'Five of Cups': ('grief processing, loss acknowledged, remaining hope', 'moving forward, acceptance, seeing what remains'),
        'Six of Cups': ('nostalgic sweetness, innocent joy, past gifts', 'stuck in past, childhood wounds, unhealthy nostalgia'),
        'Seven of Cups': ('imaginative possibilities, fantasy choices, dream exploration', 'clarity from illusion, grounded choice, reality check'),
        'Eight of Cups': ('emotional journey, necessary departure, seeking deeper', 'fear of leaving, aimless wandering, return after quest'),
        'Nine of Cups': ('emotional satisfaction, wishes granted, contentment', 'dissatisfaction, unfulfilled wishes, smug complacency'),
        'Ten of Cups': ('emotional fulfillment, family harmony, lasting happiness', 'disrupted harmony, family discord, broken dreams'),
        'Page of Cups': ('emotional curiosity, intuitive message, creative sensitivity', 'emotional immaturity, blocked creativity, ignored intuition'),
        'Knight of Cups': ('romantic pursuit, following heart, emotional quest', 'moodiness, unrealistic romance, emotional manipulation'),
        'Queen of Cups': ('emotional wisdom, compassionate intuition, nurturing depth', 'emotional overwhelm, manipulation through feeling, lost boundaries'),
        'King of Cups': ('emotional mastery, compassionate authority, balanced feeling', 'emotional volatility, cold manipulation, suppressed feelings'),

        # Swords
        'Ace of Swords': ('mental clarity, truth revealed, breakthrough insight', 'confused thinking, harsh truth, mental blocks'),
        'Two of Swords': ('balanced choice, temporary stalemate, guarded heart', 'decision made, information revealed, stalemate broken'),
        'Three of Swords': ('heartbreak acknowledged, painful truth, necessary sorrow', 'healing begins, pain releasing, recovery'),
        'Four of Swords': ('restorative rest, mental recovery, sacred pause', 'restlessness, forced activity, recovery interrupted'),
        'Five of Swords': ('hollow victory, conflict cost, defeated pride', 'reconciliation, released competition, peace after battle'),
        'Six of Swords': ('transitional journey, moving toward peace, leaving behind', 'stuck in troubled waters, return to difficulty, resisted transition'),
        'Seven of Swords': ('strategic action, independent thinking, calculated risk', 'exposure, honesty, failed strategy'),
        'Eight of Swords': ('mental imprisonment, self-imposed limits, perceived trap', 'freedom seen, bonds loosening, escape possible'),
        'Nine of Swords': ('anxious nights, mental anguish, worried thoughts', 'hope dawning, fears faced, anxiety releasing'),
        'Ten of Swords': ('painful ending, betrayal complete, dawn approaches', 'recovery begins, worst passed, refusing to end'),
        'Page of Swords': ('curious mind, vigilant observation, new ideas', 'scattered thoughts, gossip, mental immaturity'),
        'Knight of Swords': ('swift action, mental charge, truth pursuit', 'reckless haste, thoughtless words, burnout'),
        'Queen of Swords': ('perceptive clarity, honest boundaries, independent mind', 'cold judgment, bitter isolation, cutting words'),
        'King of Swords': ('intellectual authority, fair judgment, clear command', 'manipulative thinking, cruel judgment, biased authority'),

        # Pentacles
        'Ace of Pentacles': ('material opportunity, grounded beginning, prosperity seed', 'missed opportunity, unstable foundation, blocked prosperity'),
        'Two of Pentacles': ('adaptive balance, juggled priorities, flexible management', 'overwhelmed juggling, dropped balls, imbalanced priorities'),
        'Three of Pentacles': ('skilled collaboration, recognized craft, building together', 'poor teamwork, unrecognized work, lack of skill'),
        'Four of Pentacles': ('secure holding, protected resources, established stability', 'releasing grip, generous flow, insecurity'),
        'Five of Pentacles': ('material hardship, excluded feeling, spiritual poverty', 'recovery beginning, help arriving, hardship ending'),
        'Six of Pentacles': ('generous exchange, balanced giving, resources shared', 'imbalanced giving, strings attached, charity refused'),
        'Seven of Pentacles': ('patient assessment, invested waiting, growth evaluation', 'impatient harvest, wasted investment, abandoned growth'),
        'Eight of Pentacles': ('dedicated craft, skill development, focused work', 'perfectionism, uninspired work, skill neglected'),
        'Nine of Pentacles': ('abundant independence, cultivated success, refined pleasure', 'over-dependence, superficial success, lonely abundance'),
        'Ten of Pentacles': ('generational wealth, lasting legacy, family prosperity', 'family conflict, legacy troubles, unstable foundations'),
        'Page of Pentacles': ('studious beginning, practical opportunity, grounded curiosity', 'lack of progress, missed opportunity, unfocused study'),
        'Knight of Pentacles': ('steady progress, reliable effort, methodical pursuit', 'stuck routine, overly cautious, boring reliability'),
        'Queen of Pentacles': ('nurturing abundance, practical wisdom, grounded care', 'neglected home, materialistic focus, ungrounded nurturing'),
        'King of Pentacles': ('prosperous mastery, material authority, abundant leadership', 'materialistic excess, stubborn control, corrupt wealth'),
    }

    if card_name in essences:
        return essences[card_name][1 if reversed else 0]
    return "transformation and insight"

def get_card_advice(card_name, reversed=False):
    """Get actionable advice related to a card."""
    advice = {
        'The Fool': ('Trust the leap. Begin with openness, not certainty. Let curiosity guide you where planning cannot.', 'Address what blocks your beginning. Is fear masquerading as prudence? Take one small step to break the paralysis.'),
        'The Magician': ('Align your intentions with your actions. You have all the tools you need; now use them consciously.', 'Gather your scattered energies. Focus on one thing at a time rather than juggling half-formed plans.'),
        'The High Priestess': ('Listen to what your intuition already knows. The answers are within; create space for them to surface.', 'Reconnect with your inner knowing. Quiet the external noise and trust the whispers of your deeper self.'),
        'The Empress': ('Nurture what you wish to grow. Allow abundance in through pleasure, creativity, and self-care.', 'Address where you have neglected yourself. What needs tending? What needs space to flourish?'),
        'The Emperor': ('Establish structure that supports growth. Set boundaries, create order, take responsibility for what is yours.', 'Examine where control has become rigid. Loosen your grip where it serves no purpose.'),
        'The Hierophant': ('Consider what traditions or teachings serve your growth. Seek guidance from those who have walked this path.', 'Question inherited beliefs that no longer fit. Your spiritual authority is your own to claim.'),
        'The Lovers': ('Align your choices with your deepest values. True harmony comes from integrity, not compromise.', 'Clarify your values before making this choice. Internal alignment must precede external commitment.'),
        'The Chariot': ('Hold your course with focused will. Victory comes through directed intention, not scattered effort.', 'Reassess your direction. If obstacles persist, perhaps the path, not just the effort, needs examination.'),
        'Strength': ('Lead with patience and compassion, especially toward yourself. Gentle persistence outlasts force.', 'Acknowledge the raw emotion without letting it drive. Find the courage that comes from tenderness.'),
        'The Hermit': ('Take time for solitary reflection. The wisdom you seek is illuminated in stillness.', 'Balance solitude with connection. Too much isolation dims rather than clarifies your inner light.'),
        'Wheel of Fortune': ('Accept that change is the constant. Work with the turning rather than against it.', 'Recognize what you can and cannot control. Focus energy on your response, not the wheel itself.'),
        'Justice': ('Act with integrity. The fairest outcome requires honest accounting of all factors.', 'Address imbalance directly. What truth have you been avoiding? What accountability remains unmet?'),
        'The Hanged Man': ('Embrace the pause. Sometimes the most productive action is willing suspension, seeing from a different angle.', 'Consider if you are stalling or truly surrendering. Meaningful pause differs from avoidance.'),
        'Death': ('Allow what must end to end. The transformation you resist is the doorway to what awaits.', 'Acknowledge your resistance to change. What are you holding onto that has already passed?'),
        'Temperance': ('Seek balance through patient blending. Integration takes time; trust the alchemical process.', 'Notice where you have swung to extremes. What needs moderating to restore equilibrium?'),
        'The Devil': ('Examine your attachments honestly. Awareness of the chains is the first step to freedom.', 'You are freer than you believe. Name the pattern, and you diminish its power over you.'),
        'The Tower': ('Let the structures that no longer serve fall. What remains will be the foundation for something truer.', 'The disruption, internal or external, carries a gift. Look for what it reveals.'),
        'The Star': ('Hold hope. Even now, healing flows. Trust that you are being guided toward renewal.', 'Reconnect with what inspires you. Hope is a practice; tend it even when it feels dim.'),
        'The Moon': ('Trust the intuitive path even when it winds through shadow. Not all is clear, but you can still navigate.', 'Face what the moonlight reveals. The fears you name lose their power to drive you.'),
        'The Sun': ('Step into the light. Joy is not frivolous; it is essential. Allow yourself to shine.', 'Seek what brings warmth. If joy feels distant, take small steps toward what has delighted you before.'),
        'Judgement': ('Answer the call you have been hearing. This is your moment of awakening and renewal.', 'Release self-judgment that blocks your rising. You are ready for this reckoning.'),
        'The World': ('Celebrate this completion. You have integrated the lessons; honor the wholeness you have achieved.', 'Identify what remains unfinished. One more step may be needed before this cycle truly closes.'),

        'Ace of Wands': ('Act on the spark. This inspiration is meant to be expressed; begin before the fire dims.', 'Clear what blocks your creative channel. Something is damping the flame; address it.'),
        'Two of Wands': ('Plan with vision but do not linger at the planning stage. The world awaits your engagement.', 'Clarify your vision before acting. Uncertainty is a signal to define your direction.'),
        'Three of Wands': ('Patience. Your ships are coming; the expansion is already in motion. Watch the horizon.', 'Reassess if expected progress has stalled. What adjustments might speed your ships home?'),
        'Four of Wands': ('Celebrate the milestone. Mark this foundation with joy; you have earned this moment.', 'Address instability in your home or community before building further.'),
        'Five of Wands': ('Engage the competition constructively. This friction can sharpen you if you let it.', 'Step back from unnecessary battles. Choose where your energy is best spent.'),
        'Six of Wands': ('Accept the recognition you have earned. Leadership is also about receiving acknowledgment.', 'Do not let fear of visibility hold you back. Your victory deserves to be seen.'),
        'Seven of Wands': ('Hold your ground. The challenges test your commitment; stand firm in what you believe.', 'Assess if this position is worth defending. Sometimes strategic retreat allows regrouping.'),
        'Eight of Wands': ('Move now. Momentum is with you; actions taken now will carry far.', 'Address what has caused delays. Clear the path for movement to resume.'),
        'Nine of Wands': ('You are closer than you feel. One more push; your resilience is nearly rewarded.', 'Rest before continuing. Exhaustion is not a badge; it is a warning.'),
        'Ten of Wands': ('Prioritize. Not every burden is yours to carry; discern what you can release.', 'Delegate or release burdens you have been carrying alone. Shared weight moves faster.'),
        'Page of Wands': ('Follow your curiosity. This enthusiasm is a message; explore where it leads.', 'Ground your excitement in action. Enthusiasm without focus scatters.'),
        'Knight of Wands': ('Pursue boldly. This passion wants movement; hesitation wastes the fire.', 'Temper your charge with awareness. Speed without direction leads astray.'),
        'Queen of Wands': ('Lead with warmth and confidence. Your magnetism inspires; use it generously.', 'Rekindle your fire. What has dimmed your confidence? Address it at the source.'),
        'King of Wands': ('Command with vision. Your leadership is needed; step into the authority you carry.', 'Balance vision with listening. Inspiration must be tempered with receptivity.'),

        'Ace of Cups': ('Open to receive. Love, connection, spiritual gifts await your willingness to accept.', 'Examine what blocks emotional receiving. Your cup can only fill if you allow it.'),
        'Two of Cups': ('Invest in mutual connection. True partnership requires equal giving and receiving.', 'Address imbalance in your relationships. What needs rebalancing for harmony?'),
        'Three of Cups': ('Gather with those who uplift you. Joy shared multiplies; celebrate with community.', 'Reconnect with friends or address isolation. You need more than you are allowing yourself.'),
        'Four of Cups': ('Look at what is being offered. Discontent may blind you to present opportunities.', 'Your restlessness signals readiness for engagement. What opportunity awaits your attention?'),
        'Five of Cups': ('Honor your grief, but do not forget what remains. The standing cups also matter.', 'You are ready to move forward. Turn toward what remains with hope.'),
        'Six of Cups': ('Allow nostalgia its sweetness without being trapped by it. The past offers gifts for the present.', 'Release unhealthy attachment to the past. You are not who you were; you are who you are becoming.'),
        'Seven of Cups': ('Distinguish fantasy from genuine possibility. Dreams are valid; delusion is not.', 'Ground your choices in reality. Clarity comes from narrowing, not expanding options.'),
        'Eight of Cups': ('It is time to journey on. What you leave behind makes room for what you seek.', 'Clarify whether you are moving toward something or away from something. Purpose changes the journey.'),
        'Nine of Cups': ('Allow yourself satisfaction. Pleasure and contentment are not indulgences; they are achievements.', 'Examine what prevents satisfaction. What would it take to feel content?'),
        'Ten of Cups': ('Embrace the fullness of emotional fulfillment. This harmony is yours to enjoy.', 'Address what disrupts your sense of family or emotional home. Repair what you can.'),
        'Page of Cups': ('Approach emotions with beginner curiosity. The heart has messages; listen without judgment.', 'Allow emotional exploration even when it feels vulnerable. Curiosity heals.'),
        'Knight of Cups': ('Follow your heart with intention. This romantic or creative pursuit deserves your commitment.', 'Balance emotional pursuit with groundedness. Dreaming is not the same as doing.'),
        'Queen of Cups': ('Trust your emotional wisdom. Your compassion and intuition guide truly.', 'Restore healthy boundaries. You can care deeply without losing yourself.'),
        'King of Cups': ('Lead with emotional intelligence. Your balanced feeling serves others as much as yourself.', 'Address emotional volatility. Mastery means feeling fully while choosing wisely.'),

        'Ace of Swords': ('Cut through confusion with truth. Clarity is available; use it decisively.', 'Address what clouds your thinking. What assumption needs questioning?'),
        'Two of Swords': ('The decision cannot wait forever. Trust yourself to choose, even with incomplete information.', 'New information changes the balance. The stalemate is breaking; prepare to act.'),
        'Three of Swords': ('Allow the grief its space. This pain is a passage, not a destination.', 'Healing is underway. Honor how far you have come from the sharpest moments.'),
        'Four of Swords': ('Rest is not optional. Recovery now prevents breakdown later.', 'If rest eludes you, address what keeps your mind running. Peace is a practice.'),
        'Five of Swords': ('Consider what victory costs. Is this battle worth winning at this price?', 'Peace is possible now. Release the conflict mentality; reconciliation awaits.'),
        'Six of Swords': ('The journey to calmer waters has begun. Trust the transition even when it feels slow.', 'Examine what keeps you in troubled waters. What must you release to move on?'),
        'Seven of Swords': ('Be strategic, but do not cross into deception. Independence requires integrity.', 'Prepare for truth to surface. What needs addressing before it is revealed?'),
        'Eight of Swords': ('See that your bonds are looser than they appear. The mental trap dissolves with clearer seeing.', 'Freedom is closer than you think. Take one step; the rest will follow.'),
        'Nine of Swords': ('Your fears are magnified in the dark. What seems overwhelming shrinks in daylight.', 'Morning is coming. The anxiety is releasing; you are moving toward peace.'),
        'Ten of Swords': ('This ending, though painful, completes a chapter. The dawn behind the darkness is real.', 'The worst has passed. Recovery is not just possible; it has already begun.'),
        'Page of Swords': ('Observe keenly. This vigilant curiosity serves you; gather information before acting.', 'Direct your mental energy constructively. Scattered thinking undermines your sharpness.'),
        'Knight of Swords': ('Act decisively on your convictions. Speed and clarity combine for impact.', 'Slow your mental charge. Haste leads to errors; truth outlasts speed.'),
        'Queen of Swords': ('Speak your truth clearly. Your perception cuts through; use it with precision.', 'Warm your sharp edges with compassion. Truth can be direct without being cold.'),
        'King of Swords': ('Lead with clear thinking and fair judgment. Your mental authority is needed.', 'Examine if your judgments have become rigid or cruel. Authority requires fairness.'),

        'Ace of Pentacles': ('Accept the opportunity. This material beginning is meant to be planted and grown.', 'Address what blocks prosperity. What foundation needs stabilizing first?'),
        'Two of Pentacles': ('Stay flexible as you balance competing demands. Adaptability is your strength now.', 'Simplify if juggling has become overwhelming. Fewer balls are easier to manage.'),
        'Three of Pentacles': ('Collaborate with skill. Your craft grows through working with others.', 'Address teamwork issues directly. Your work deserves recognition; claim it.'),
        'Four of Pentacles': ('Protect what you have built. Security is valid; guard your resources wisely.', 'Examine if you are holding too tightly. What could flow more freely?'),
        'Five of Pentacles': ('Seek help; you are not as alone as you feel. Support exists; reach for it.', 'Relief is arriving. The hardship is ending; prepare to receive.'),
        'Six of Pentacles': ('Give and receive in balance. Generosity flows both ways.', 'Address imbalanced giving. Are you giving too much? Receiving too little? Find equilibrium.'),
        'Seven of Pentacles': ('Assess your investment. This pause for evaluation serves the longer growth.', 'Do not abandon what you have planted. Patience yet; the harvest approaches.'),
        'Eight of Pentacles': ('Dedicate yourself to the craft. Mastery comes through focused, repeated effort.', 'If work feels uninspired, reconnect with purpose. Why are you building this skill?'),
        'Nine of Pentacles': ('Enjoy what you have cultivated. This abundant independence is your creation.', 'Examine if self-sufficiency has become isolation. You can be complete and connected.'),
        'Ten of Pentacles': ('Build with legacy in mind. What you create now echoes through generations.', 'Address family or inheritance issues directly. Legacy is not only material.'),
        'Page of Pentacles': ('Study what interests you. This practical curiosity leads to real opportunity.', 'Apply your learning. Study without practice leads nowhere.'),
        'Knight of Pentacles': ('Proceed methodically. Your steady, reliable effort will build what lasts.', 'Avoid getting stuck in routine. Reliability should not become rigidity.'),
        'Queen of Pentacles': ('Nurture practically. Your grounded care creates real security for those you love.', 'Balance nurturing others with nurturing yourself. You cannot pour from an empty vessel.'),
        'King of Pentacles': ('Build your abundance with generosity and wisdom. Material mastery includes sharing.', 'Examine if material focus has overshadowed other values. Wealth is means, not end.'),
    }

    if card_name in advice:
        return advice[card_name][1 if reversed else 0]
    return "Reflect on what this situation asks of you. The path forward becomes clearer when you align intention with action."

def get_expanded_interpretation(card, seed):
    """Get an expanded interpretation for a card in its position."""
    random.seed(seed + hash(card['name']))

    essence = get_card_essence(card['name'], card['reversed'])
    advice = get_card_advice(card['name'], card['reversed'])
    position = card['position']
    reversed_note = " reversed" if card['reversed'] else ""
    context = card.get('context', '')

    # Position-specific expansions
    position_expansions = {
        'Past': [
            f"Looking back, {card['name']}{reversed_note} shaped the foundation you stand on now. This energy of {essence} was formative, whether you recognized it at the time or not. {context}",
            f"Your history with {card['name']}{reversed_note} runs deep. The qualities of {essence} have been part of your journey, influencing how you approach this present moment. {context}",
        ],
        'Present': [
            f"Right now, {card['name']}{reversed_note} dominates your situation. You are immersed in the energy of {essence}, and this shapes everything else in the reading. {context}",
            f"At the heart of your current experience, {card['name']}{reversed_note} calls attention to {essence}. This is what you are living through, day by day. {context}",
        ],
        'Future': [
            f"Looking ahead, {card['name']}{reversed_note} suggests a trajectory toward {essence}. This is not fixed fate but likely development if current patterns continue. {context}",
            f"The path before you leads toward {card['name']}{reversed_note} energy. Expect themes of {essence} to become increasingly relevant. {context}",
        ],
        'Challenge': [
            f"The challenge here, represented by {card['name']}{reversed_note}, asks you to grapple with {essence}. This is your growing edge, the place where development happens through struggle. {context}",
            f"{card['name']}{reversed_note} as your challenge indicates that {essence} is testing you. How you meet this test will determine much about your journey. {context}",
        ],
        'Advice': [
            f"For guidance, {card['name']}{reversed_note} offers wisdom: {essence}. This is the medicine the situation calls for. {advice}",
            f"The counsel of {card['name']}{reversed_note} is clear: embrace {essence}. {advice}",
        ],
        'Outcome': [
            f"The potential culmination through {card['name']}{reversed_note} points toward {essence}. This is where the current energies are flowing if you work with them consciously. {context}",
            f"As an outcome, {card['name']}{reversed_note} suggests {essence}. The ending of this chapter depends on how you navigate the cards that precede it. {context}",
        ],
        "Today's Guidance": [
            f"For today, {card['name']}{reversed_note} brings focus to {essence}. Let this energy guide your choices and attention as you move through the day. {context} {advice}",
            f"This day carries the signature of {card['name']}{reversed_note}. The theme of {essence} is your touchstone; return to it when you need direction. {context} {advice}",
        ],
        'Situation': [
            f"At the core of this situation, {card['name']}{reversed_note} defines the landscape. You are navigating terrain marked by {essence}. {context}",
            f"The essential nature of what you face is captured by {card['name']}{reversed_note}: {essence}. Understanding this shapes everything else. {context}",
        ],
        'Action': [
            f"The action called for, revealed through {card['name']}{reversed_note}, is to engage with {essence}. {advice}",
            f"{card['name']}{reversed_note} indicates that your next move should embody {essence}. {advice}",
        ],
        'Hidden Influences': [
            f"Beneath the surface, {card['name']}{reversed_note} operates unseen. This hidden factor of {essence} shapes more than you realize. {context}",
            f"What you cannot directly see, {card['name']}{reversed_note}, still influences everything. The energy of {essence} moves in the background. {context}",
        ],
        'External Influences': [
            f"From outside your control, {card['name']}{reversed_note} brings the energy of {essence}. These external forces shape your options. {context}",
            f"The world around you carries {card['name']}{reversed_note} energy. The quality of {essence} comes from circumstances beyond your making. {context}",
        ],
        'Obstacles': [
            f"What stands in your way, {card['name']}{reversed_note}, manifests as {essence}. This obstacle is real but not insurmountable. {context}",
            f"{card['name']}{reversed_note} as an obstacle presents {essence} as your barrier. Understanding it is the first step to moving past it. {context}",
        ],
        'Hopes/Fears': [
            f"Your hopes and fears crystallize in {card['name']}{reversed_note}. You both desire and dread {essence}. This ambivalence holds information for you. {context}",
            f"{card['name']}{reversed_note} represents what you most hope for and most fear. The {essence} energy triggers both longing and anxiety. {context}",
        ],
        'Above': [
            f"Your highest potential in this situation is revealed through {card['name']}{reversed_note}. The best possible outcome involves {essence}. {context}",
            f"Aspire toward what {card['name']}{reversed_note} represents: {essence}. This is the crown of possibility for your situation. {context}",
        ],
        'Below': [
            f"The foundation of this matter rests on {card['name']}{reversed_note}. Underneath everything, {essence} forms the bedrock. {context}",
            f"What underlies your situation is {card['name']}{reversed_note}: {essence}. This subconscious influence shapes what rises above. {context}",
        ],
    }

    # Default expansion for other positions
    if position not in position_expansions:
        expansions = [
            f"In the {position} position, {card['name']}{reversed_note} brings the energy of {essence}. {context}",
            f"As {position}, {card['name']}{reversed_note} indicates {essence}. {context}",
        ]
    else:
        expansions = position_expansions[position]

    return random.choice(expansions)

def generate_opening(question, timing, cards, seed):
    """Generate an opening paragraph."""
    random.seed(seed)

    timing_clean = timing.split('—')[0].strip() if '—' in timing else timing
    timing_meaning = timing.split('—')[1].strip() if '—' in timing else ""

    openings = [
        f"Your question, \"{question}\", arrives at a meaningful time. The {timing_clean} speaks to {timing_meaning.lower() if timing_meaning else 'this moment of transition'}. The cards have gathered to offer their perspective on what lies at the heart of your inquiry.",
        f"As you ask about {question.lower().rstrip('?')}, the tarot responds with thoughtful consideration. During this {timing_clean}, the energies are particularly suited for reflection on this matter. Let us see what wisdom the cards reveal.",
        f"The cards respond to your question: \"{question}\" Under the {timing_clean}, a time of {timing_meaning.lower() if timing_meaning else 'reflection and insight'}, this reading carries particular weight. The spread before you offers insight into your situation.",
        f"Your inquiry about {question.lower().rstrip('?')} has drawn a meaningful arrangement of cards. As we enter this reading during the {timing_clean}, the timing supports the introspection this question requires.",
    ]

    return random.choice(openings)

def generate_closing(question, cards, seed):
    """Generate an actionable closing paragraph."""
    random.seed(seed + 1000)

    # Find key cards
    advice_card = next((c for c in cards if c['position'] == 'Advice'), None)
    outcome_card = next((c for c in cards if c['position'] == 'Outcome'), None)
    action_card = next((c for c in cards if c['position'] == 'Action'), None)
    guidance_card = next((c for c in cards if c['position'] == "Today's Guidance"), None)

    key_card = advice_card or action_card or guidance_card or outcome_card or cards[-1]

    advice = get_card_advice(key_card['name'], key_card['reversed'])

    closings = [
        f"In light of this reading, your path forward asks for intentional engagement with these energies. {advice} Remember that the cards illuminate possibilities; you hold the power to shape outcomes through your choices and actions.",
        f"The wisdom offered here points toward a clear course of action. {advice} Trust that you have the resources to meet this situation. The cards have shown you the landscape; now you walk it.",
        f"Taking all these cards together, the guidance is clear. {advice} This reading is not prediction but illumination. What you do with this insight determines where the path leads.",
        f"As you move forward from this reading, carry the central message with you. {advice} The tarot has offered its perspective; your inner wisdom will integrate these insights with what you already know.",
    ]

    return random.choice(closings)

def generate_reading(prompt_data):
    """Generate a complete tarot reading for a prompt."""
    input_text = prompt_data['input_text']
    prompt_id = prompt_data['id']

    # Create a seed from the ID for reproducibility
    seed = int(hashlib.md5(prompt_id.encode()).hexdigest()[:8], 16)

    # Extract components
    question = extract_question(input_text)
    timing = extract_timing(input_text)
    cards = extract_cards_from_input(input_text)
    combinations = extract_combinations(input_text)

    if not cards:
        return f"The cards speak to your question about {question}. Trust your inner wisdom as you navigate this situation."

    # Build the reading
    paragraphs = []

    # Opening
    opening = generate_opening(question, timing, cards, seed)
    paragraphs.append(opening)

    # Card interpretations - expanded versions
    if len(cards) == 1:
        # For single card spreads, give a very detailed interpretation
        card = cards[0]
        interp = get_expanded_interpretation(card, seed)
        essence = get_card_essence(card['name'], card['reversed'])
        advice = get_card_advice(card['name'], card['reversed'])

        # Build a rich single-card reading
        para2 = interp
        paragraphs.append(para2)

        # Add reflection paragraph
        random.seed(seed + 50)
        reflections = [
            f"This single card carries significant weight in answering your question. The energy of {essence} speaks directly to what you are experiencing. Consider how this theme has appeared in your life recently, and what shifts it might be asking you to make.",
            f"When one card answers a question, every detail matters. {card['name']}{' reversed' if card['reversed'] else ''} offers concentrated wisdom. The essence of {essence} is your focal point; everything else orbits this central truth.",
            f"A single-card draw cuts to the core of the matter. There is no ambiguity in what {card['name']}{' reversed' if card['reversed'] else ''} asks you to consider. The quality of {essence} is your answer and your teacher in this moment.",
        ]
        paragraphs.append(random.choice(reflections))

    elif len(cards) <= 3:
        # For small spreads, give each card a full paragraph
        for i, card in enumerate(cards):
            interp = get_expanded_interpretation(card, seed + i)
            paragraphs.append(interp)
    else:
        # For larger spreads, group thematically
        # Temporal cards: Past, Present, Future, Situation
        temporal = [c for c in cards if c['position'] in ['Past', 'Present', 'Future', 'Situation']]
        if temporal:
            texts = [get_expanded_interpretation(c, seed + i) for i, c in enumerate(temporal)]
            paragraphs.append(" ".join(texts))

        # Challenge/Obstacle/Hidden cards
        hidden = [c for c in cards if c['position'] in ['Challenge', 'Obstacles', 'Hidden Influences']]
        if hidden:
            texts = [get_expanded_interpretation(c, seed + 100 + i) for i, c in enumerate(hidden)]
            paragraphs.append(" ".join(texts))

        # External/Environmental cards
        external = [c for c in cards if c['position'] in ['External Influences', 'External', 'Above', 'Below']]
        if external:
            texts = [get_expanded_interpretation(c, seed + 200 + i) for i, c in enumerate(external)]
            paragraphs.append(" ".join(texts))

        # Guidance cards: Advice, Action, Outcome, Hopes/Fears
        guidance = [c for c in cards if c['position'] in ['Advice', 'Action', 'Outcome', 'Hopes/Fears']]
        if guidance:
            texts = [get_expanded_interpretation(c, seed + 300 + i) for i, c in enumerate(guidance)]
            paragraphs.append(" ".join(texts))

        # Any remaining cards
        used = set(c['position'] for group in [temporal, hidden, external, guidance] for c in group)
        remaining = [c for c in cards if c['position'] not in used]
        if remaining:
            texts = [get_expanded_interpretation(c, seed + 400 + i) for i, c in enumerate(remaining)]
            paragraphs.append(" ".join(texts))

    # Add combinations insight if present
    if combinations:
        random.seed(seed + 500)
        combo_text = random.choice(combinations)
        combo_intros = [
            f"The interplay between cards adds another layer of meaning. {combo_text} This combination deserves particular attention as you reflect on your question.",
            f"Notice how certain cards amplify each other's messages. {combo_text} This synergy points to something central in your situation.",
            f"A significant pattern emerges when we consider how these cards relate. {combo_text} Let this combination inform your understanding.",
        ]
        paragraphs.append(random.choice(combo_intros))

    # Closing
    closing = generate_closing(question, cards, seed)
    paragraphs.append(closing)

    # Combine paragraphs
    reading = "\n\n".join(paragraphs)

    return reading

def main():
    # Read the batch file
    with open('/home/user/taro/training/data/batches_expanded/batch_0005.json', 'r') as f:
        batch_data = json.load(f)

    prompts = batch_data['prompts']
    print(f"Processing {len(prompts)} prompts from batch {batch_data['batch_id']}...")

    # Generate responses
    responses = []
    for i, prompt in enumerate(prompts):
        reading = generate_reading(prompt)
        responses.append({
            'id': prompt['id'],
            'response': reading
        })
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(prompts)}")

    # Write to JSONL
    output_path = '/home/user/taro/training/data/batches_expanded/responses/batch_0005_responses.jsonl'
    with open(output_path, 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')

    print(f"Wrote {len(responses)} responses to {output_path}")
    return len(responses)

if __name__ == '__main__':
    count = main()
    print(f"Complete! Generated {count} tarot readings.")
