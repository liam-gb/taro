// Card interpretations for all 78 cards
export const CARD_INTERPRETATIONS = {
  // Major Arcana
  "The Fool": {
    element: "Air", planet: "Uranus",
    keywords: ["beginnings", "innocence", "spontaneity", "leap of faith"],
    upright: "The Fool represents pure potential and the courage to begin anew. This is the energy of stepping into the unknown with trust rather than fear. The seeker may be at a threshold—a new job, relationship, creative project, or life chapter. There's an invitation to embrace beginner's mind, to be open to possibilities without overthinking.",
    reversed: "Recklessness, naivety, or fear of taking necessary risks. The seeker may be acting without considering consequences, or conversely, may be so paralyzed by fear that they refuse to move forward at all."
  },
  "The Magician": {
    element: "Air", planet: "Mercury",
    keywords: ["manifestation", "willpower", "skill", "resourcefulness"],
    upright: "The Magician channels divine will into material reality. All four elements are at his disposal—he lacks nothing. This card signals that the seeker has everything needed to achieve their goal. It's time to focus intention, take action, and trust in one's abilities.",
    reversed: "Manipulation, trickery, untapped potential, or scattered energy. Talents may be misused or wasted. The seeker might be deceiving others or themselves, or may doubt their abilities when they shouldn't."
  },
  "The High Priestess": {
    element: "Water", planet: "Moon",
    keywords: ["intuition", "mystery", "inner voice", "unconscious"],
    upright: "The High Priestess guards the threshold between conscious and unconscious realms. She invites the seeker to trust intuition over logic, to listen to dreams and subtle feelings. This is a time for receptivity rather than action, for going inward rather than outward.",
    reversed: "Secrets causing harm, disconnection from intuition, or ignoring inner wisdom. The seeker may be overly rational, dismissing gut feelings, or there may be hidden information that needs to surface."
  },
  "The Empress": {
    element: "Earth", planet: "Venus",
    keywords: ["abundance", "nurturing", "fertility", "nature", "creativity"],
    upright: "The Empress embodies creative abundance and nurturing love. She represents fertility in all forms—children, projects, ideas, gardens. This card encourages the seeker to embrace pleasure, beauty, and sensory experience. Nature, comfort, and allowing things to grow organically are emphasized.",
    reversed: "Creative blocks, neglecting self-care, smothering, or dependence. The seeker may be depleted from over-giving, or struggling to birth something new."
  },
  "The Emperor": {
    element: "Fire", zodiac: "Aries",
    keywords: ["authority", "structure", "control", "father figure", "stability"],
    upright: "The Emperor represents structure, authority, and the power to create order from chaos. This card may indicate a father figure, boss, or authority in the seeker's life, or their own need to establish boundaries and take command. It's about building lasting foundations and taking responsibility.",
    reversed: "Tyranny, rigidity, abuse of power, or absent authority. The seeker may be dealing with an overbearing figure, or struggling to claim their own authority."
  },
  "The Hierophant": {
    element: "Earth", zodiac: "Taurus",
    keywords: ["tradition", "conformity", "spiritual wisdom", "institutions", "teaching"],
    upright: "The Hierophant represents established wisdom, spiritual traditions, and conventional paths. This may indicate formal education, religious or spiritual institutions, mentorship, or the value of following established methods.",
    reversed: "Challenging conventions, breaking from tradition, or spiritual independence. The seeker may need to forge their own path rather than follow established routes."
  },
  "The Lovers": {
    element: "Air", zodiac: "Gemini",
    keywords: ["love", "harmony", "choices", "union", "values alignment"],
    upright: "Beyond romantic love, The Lovers represents meaningful choices and the alignment of values. It speaks to partnerships where both people are fully seen, and to decisions that reflect one's deepest values. Union, harmony, and integration of opposites are themes.",
    reversed: "Disharmony, misaligned values, difficult relationship choices, or inner conflict. The seeker may be in a partnership that doesn't honor their values, or facing a choice between head and heart."
  },
  "The Chariot": {
    element: "Water", zodiac: "Cancer",
    keywords: ["willpower", "determination", "victory", "control", "forward movement"],
    upright: "The Chariot charges forward through sheer will and determination. The seeker is called to harness opposing forces and direct them toward a goal. Victory is available through focus, confidence, and controlled aggression.",
    reversed: "Lack of direction, scattered energy, aggression without purpose, or feeling out of control. Internal conflicts may be pulling them apart."
  },
  "Strength": {
    element: "Fire", zodiac: "Leo",
    keywords: ["courage", "patience", "inner strength", "compassion", "gentle power"],
    upright: "True strength is shown not through force but through patience, compassion, and gentle mastery of one's instincts. This card calls for courage of the heart, emotional resilience, and the quiet confidence that comes from inner knowing.",
    reversed: "Self-doubt, weakness, raw emotions overwhelming reason, or misuse of power. The seeker may be struggling with impulse control or losing confidence."
  },
  "The Hermit": {
    element: "Earth", zodiac: "Virgo",
    keywords: ["introspection", "solitude", "inner guidance", "wisdom", "soul-searching"],
    upright: "The Hermit withdraws from the noise of the world to find inner truth. This is a time for solitude, reflection, and listening to inner wisdom. A wise guide or mentor may appear, or the seeker themselves may be called to guide others.",
    reversed: "Isolation, loneliness, withdrawal from necessary engagement, or refusing to learn. Solitude has become isolation; reflection has become avoidance."
  },
  "Wheel of Fortune": {
    element: "Fire", planet: "Jupiter",
    keywords: ["cycles", "fate", "turning point", "destiny", "change"],
    upright: "The Wheel turns—what was down will rise, what was up will fall. This card represents the cyclical nature of life and the forces of fate and karma. A turning point is at hand. Current circumstances, good or bad, will shift.",
    reversed: "Bad luck, resistance to change, or being stuck in a cycle. The seeker may be fighting against natural change or experiencing a downturn in fortune."
  },
  "Justice": {
    element: "Air", zodiac: "Libra",
    keywords: ["fairness", "truth", "karma", "accountability", "legal matters"],
    upright: "Justice represents cause and effect, truth, and fair outcomes. Legal matters, contracts, and important decisions may be involved. The seeker is called to act with integrity and accept responsibility for their actions.",
    reversed: "Unfairness, dishonesty, lack of accountability, or legal complications. The seeker may be experiencing injustice, or may need to examine their own lack of integrity."
  },
  "The Hanged Man": {
    element: "Water", planet: "Neptune",
    keywords: ["surrender", "new perspective", "pause", "letting go", "sacrifice"],
    upright: "The Hanged Man surrenders to gain wisdom. Suspended between worlds, he sees everything from a new angle. This card calls for voluntary pause, surrender of control, and willingness to see differently.",
    reversed: "Stalling, resistance to necessary sacrifice, or martyrdom without purpose. The seeker may be stuck in delay, refusing to let go, or playing victim."
  },
  "Death": {
    element: "Water", zodiac: "Scorpio",
    keywords: ["transformation", "endings", "change", "transition", "rebirth"],
    upright: "Death is transformation—the necessary ending that makes new life possible. Something must die for something new to be born. This card signals the end of a relationship, identity, belief, or life chapter. Resistance is futile; embrace the change.",
    reversed: "Resistance to necessary change, stagnation, or incomplete transformation. The seeker may be clinging to what needs to end, or experiencing a prolonged, painful transition."
  },
  "Temperance": {
    element: "Fire", zodiac: "Sagittarius",
    keywords: ["balance", "moderation", "patience", "harmony", "integration"],
    upright: "Temperance represents the art of balance and the alchemy of integration. The seeker is called to moderation, patience, and the middle path. Healing, recovery, and the slow work of integration are indicated.",
    reversed: "Imbalance, excess, lack of patience, or discord. The seeker may be going to extremes, rushing when patience is needed, or struggling to integrate opposing aspects."
  },
  "The Devil": {
    element: "Earth", zodiac: "Capricorn",
    keywords: ["shadow self", "attachment", "addiction", "bondage", "materialism"],
    upright: "The Devil represents the chains we choose—addictions, unhealthy attachments, shadow patterns, materialism. This card asks the seeker to examine what binds them: substances, relationships, beliefs, fears. It's also about owning one's shadow.",
    reversed: "Breaking free, releasing attachments, or confronting shadow material. The seeker may be ready to break unhealthy bonds, or beginning to see how they've been enslaved to something."
  },
  "The Tower": {
    element: "Fire", planet: "Mars",
    keywords: ["upheaval", "revelation", "sudden change", "destruction", "awakening"],
    upright: "The Tower brings sudden, dramatic change—the lightning strike that destroys false structures. This can be terrifying but is ultimately liberating. Illusions shatter; truths are revealed; what was built on false foundations falls.",
    reversed: "Averting disaster, fear of change, or internal rather than external upheaval. The seeker may be resisting necessary destruction or experiencing the Tower energy internally as anxiety."
  },
  "The Star": {
    element: "Air", zodiac: "Aquarius",
    keywords: ["hope", "faith", "renewal", "inspiration", "serenity"],
    upright: "After the Tower's destruction comes the Star's healing hope. This card represents renewal, faith restored, and connection to something greater. The seeker is invited to trust, to heal, to be vulnerable. Inspiration flows; the universe supports.",
    reversed: "Despair, disconnection, loss of faith, or blocked inspiration. The seeker may be struggling to find hope, feeling cut off from spiritual connection."
  },
  "The Moon": {
    element: "Water", zodiac: "Pisces",
    keywords: ["illusion", "fear", "subconscious", "intuition", "confusion"],
    upright: "The Moon illuminates the realm of the unconscious—dreams, fears, illusions, intuition. Things are not as they seem. This card calls for trusting intuition even when the path is unclear, and for facing fears that emerge from the depths.",
    reversed: "Releasing fear, clarity emerging, or denial of intuition. Confusion may be lifting, or the seeker may be repressing unconscious material that needs to surface."
  },
  "The Sun": {
    element: "Fire", planet: "Sun",
    keywords: ["joy", "success", "vitality", "positivity", "clarity"],
    upright: "The Sun shines with pure, uncomplicated joy. This is one of the most positive cards—indicating success, happiness, vitality, and clear vision. Everything is illuminated; nothing is hidden. Energy is high; the future is bright.",
    reversed: "Temporary setbacks, dimmed joy, or ego inflation. The seeker may be experiencing delayed success, struggling to feel joy, or letting ego overshadow genuine happiness."
  },
  "Judgement": {
    element: "Fire", planet: "Pluto",
    keywords: ["rebirth", "inner calling", "reflection", "reckoning", "awakening"],
    upright: "Judgement sounds the call to awakening. The past is reviewed and released. The seeker may experience a profound calling, a moment of clarity about their purpose, or a need to make peace with the past. This is resurrection—a chance to answer the call of the higher self.",
    reversed: "Self-doubt, ignoring the call, or refusal to learn from the past. The seeker may be avoiding necessary self-reflection, deaf to their calling, or stuck in self-criticism."
  },
  "The World": {
    element: "Earth", planet: "Saturn",
    keywords: ["completion", "achievement", "wholeness", "fulfillment", "integration"],
    upright: "The World represents the successful completion of a cycle. The dancer has integrated all four elements and moves in harmony with the universe. The seeker may be experiencing achievement, fulfillment, or a sense of wholeness.",
    reversed: "Incompletion, delays, or lack of closure. The seeker may be struggling to finish something, or feeling unfulfilled despite apparent success."
  },
  // Wands
  "Ace of Wands": {
    keywords: ["new inspiration", "creative spark", "potential", "opportunity", "initiative"],
    upright: "A burst of creative or passionate energy. New beginnings in career, creativity, or personal ambition. The universe offers a spark—will you fan it into flame? Take initiative; act on this energy while it's fresh.",
    reversed: "Delays, lack of motivation, creative blocks, false starts. The spark is there but won't catch. The seeker may be sitting on inspiration without acting."
  },
  "Two of Wands": {
    keywords: ["planning", "future vision", "decisions", "waiting", "personal power"],
    upright: "The world is in your hands—now what will you do with it? This card represents planning, weighing options, and envisioning the future. It's a moment of strategic thinking before expansion.",
    reversed: "Fear of the unknown, lack of planning, playing it safe. The seeker may be afraid to step out of comfort zones, or planning without ever acting."
  },
  "Three of Wands": {
    keywords: ["expansion", "foresight", "overseas opportunities", "progress", "enterprise"],
    upright: "Plans are in motion; ships are sent out. This card represents expansion, progress, and watching endeavors unfold. The vision is becoming reality.",
    reversed: "Delays in plans, lack of foresight, obstacles to expansion. Anticipated progress isn't materializing."
  },
  "Four of Wands": {
    keywords: ["celebration", "harmony", "homecoming", "community", "stability"],
    upright: "A time of celebration, achievement, and joyful community. This card often indicates weddings, parties, homecomings, or reaching a significant milestone.",
    reversed: "Lack of harmony, delayed celebrations, instability at home. Something is off in the home environment or community."
  },
  "Five of Wands": {
    keywords: ["conflict", "competition", "disagreements", "tension", "challenges"],
    upright: "Creative tension, competition, or conflict. Multiple forces vie for dominance. While stressful, this energy can be generative if channeled well.",
    reversed: "Avoiding conflict, internal conflict, resolution. The seeker may be suppressing disagreements or experiencing inner turmoil."
  },
  "Six of Wands": {
    keywords: ["victory", "recognition", "success", "public acclaim", "confidence"],
    upright: "Public recognition and victory. The seeker receives acknowledgment for their efforts—promotions, awards, applause. Confidence is high and well-earned.",
    reversed: "Ego, fall from grace, lack of recognition. Success may lead to arrogance, or anticipated recognition doesn't come."
  },
  "Seven of Wands": {
    keywords: ["defensiveness", "standing ground", "competition", "perseverance", "challenge"],
    upright: "Defending your position against challenges. This card calls for courage, conviction, and refusal to back down. You've earned your position—defend it.",
    reversed: "Giving up, overwhelm, being overrun. The seeker may be unable to maintain their position, or exhausted from constant defense."
  },
  "Eight of Wands": {
    keywords: ["speed", "movement", "swift action", "travel", "communication"],
    upright: "Rapid movement and swift developments. Things accelerate—messages fly, travel happens suddenly, projects gain momentum. Strike while the iron is hot.",
    reversed: "Delays, frustration, waiting. The expected speed doesn't materialize. Messages are delayed, travel is disrupted, projects stall."
  },
  "Nine of Wands": {
    keywords: ["resilience", "persistence", "boundaries", "fatigue", "vigilance"],
    upright: "Battle-weary but still standing. The seeker has been through challenges and carries the wounds, yet refuses to give up. One more push may be needed.",
    reversed: "Stubbornness, paranoia, giving up too soon. The seeker may be too defensive, seeing threats where none exist."
  },
  "Ten of Wands": {
    keywords: ["burden", "responsibility", "hard work", "stress", "carrying too much"],
    upright: "Carrying a heavy load. The seeker has taken on too much—responsibilities, projects, others' burdens. Success has become a weight. Delegation or releasing some burdens is needed.",
    reversed: "Releasing burdens, avoiding responsibility, or collapse. The seeker may finally be letting go of excess weight, or may be shirking responsibilities."
  },
  "Page of Wands": {
    keywords: ["exploration", "enthusiasm", "discovery", "free spirit", "new ideas"],
    upright: "A messenger of creative inspiration or a person embodying youthful Fire energy. New ideas want to be explored; enthusiasm is high. Adventure calls.",
    reversed: "Lack of direction, haste, scattered energy. Ideas abound but nothing follows through."
  },
  "Knight of Wands": {
    keywords: ["action", "adventure", "passion", "impulsiveness", "fearlessness"],
    upright: "Charging forward with passion and courage. This Knight acts boldly, loves adventure, and fears nothing. It's time for bold action, travel, or passionate pursuit.",
    reversed: "Haste, recklessness, delays in plans. The Knight's energy becomes destructive impulsiveness or frustrated stagnation."
  },
  "Queen of Wands": {
    keywords: ["confidence", "determination", "warmth", "vibrant energy", "leadership"],
    upright: "A confident, charismatic leader who inspires others with warmth and determination. She knows her worth and commands respect through genuine presence. It's time to own your power with grace.",
    reversed: "Selfishness, jealousy, insecurity masked as aggression. The Queen's confidence becomes arrogance or crumbles into self-doubt."
  },
  "King of Wands": {
    keywords: ["leadership", "vision", "entrepreneur", "boldness", "honor"],
    upright: "A natural leader with bold vision and the charisma to inspire others to follow. He leads through enthusiasm and honor, turning vision into reality. It's time to lead, to act on vision with confidence.",
    reversed: "Impulsiveness, tyranny, unrealistic expectations. The King's leadership becomes domineering or his vision becomes disconnected from reality."
  },
  // Cups
  "Ace of Cups": {
    keywords: ["new love", "emotional beginning", "compassion", "creativity", "intuition"],
    upright: "A new emotional beginning overflows with possibility. New love, deepened compassion, creative inspiration, or spiritual awakening may be arriving. The heart opens; say yes to the heart.",
    reversed: "Blocked emotions, emptiness, repressed feelings. The cup is offered but can't be received. The seeker may be emotionally closed or struggling with self-love."
  },
  "Two of Cups": {
    keywords: ["partnership", "unity", "mutual attraction", "connection", "harmony"],
    upright: "A beautiful meeting of hearts. This card represents mutual attraction, partnership, and harmonious connection. Two people see and honor each other. The union is balanced and reciprocal.",
    reversed: "Imbalance, breakup, lack of harmony. The partnership is out of sync—one gives more than the other, or the connection is breaking down."
  },
  "Three of Cups": {
    keywords: ["celebration", "friendship", "community", "collaboration", "joy"],
    upright: "Joyful celebration with beloved friends. This card represents friendship, community support, and shared happiness. There's abundance in connection.",
    reversed: "Overindulgence, gossip, isolation from friends. Celebration becomes excess; friendship sours into drama."
  },
  "Four of Cups": {
    keywords: ["apathy", "contemplation", "disconnection", "reevaluation", "discontent"],
    upright: "Emotional withdrawal and contemplation. The seeker may be bored, discontent, or too focused on what's missing to see what's offered. There's an opportunity being overlooked.",
    reversed: "Renewed interest, acceptance, moving forward. The seeker begins to see opportunities they'd been missing."
  },
  "Five of Cups": {
    keywords: ["loss", "grief", "disappointment", "regret", "focusing on the negative"],
    upright: "Grief and disappointment over what's been lost. Three cups have spilled—this loss is real and deserves mourning. Yet two cups remain; not all is lost. The bridge home still stands.",
    reversed: "Acceptance, moving forward, healing. The seeker begins to turn around, to see what remains rather than only what's lost."
  },
  "Six of Cups": {
    keywords: ["nostalgia", "childhood", "innocence", "past connections", "gifts"],
    upright: "Sweet nostalgia and the healing power of innocence. Past connections resurface—childhood friends, old homes, memories. There's an invitation to reconnect with simpler times and childlike joy.",
    reversed: "Living in the past, stuck in nostalgia, childhood wounds. The seeker may be romanticizing the past at the expense of the present."
  },
  "Seven of Cups": {
    keywords: ["illusion", "fantasy", "choices", "wishful thinking", "temptation"],
    upright: "Many options appear, but which are real? This card represents the realm of fantasy, imagination, and wishful thinking. Ground fantasies in reality before choosing.",
    reversed: "Clarity, making a choice, illusions dispelled. The fog lifts; the seeker sees clearly what's real and chooses accordingly."
  },
  "Eight of Cups": {
    keywords: ["departure", "leaving behind", "seeking deeper meaning", "disillusionment"],
    upright: "Walking away from what no longer fulfills. Despite having built something, the seeker turns toward the unknown, seeking deeper meaning. A difficult but necessary journey.",
    reversed: "Fear of leaving, staying in unfulfilling situations, aimless wandering. The seeker knows they need to leave but can't."
  },
  "Nine of Cups": {
    keywords: ["wish fulfillment", "contentment", "satisfaction", "gratitude", "emotional abundance"],
    upright: "The 'wish card.' Emotional satisfaction and dreams coming true. Take time to appreciate what you have; gratitude amplifies joy. This is a moment of genuine happiness.",
    reversed: "Dissatisfaction despite having much, materialism, smugness. Wishes granted don't bring expected fulfillment."
  },
  "Ten of Cups": {
    keywords: ["harmony", "family", "emotional fulfillment", "happiness", "alignment"],
    upright: "Emotional paradise—the happy family under the rainbow. This card represents the fulfillment of emotional dreams: loving relationships, family harmony, lasting happiness.",
    reversed: "Disconnection, dysfunctional family, broken dreams. The ideal isn't matching reality. Family or relationship problems disrupt harmony."
  },
  "Page of Cups": {
    keywords: ["creative opportunity", "intuition", "messenger", "inner child", "dreams"],
    upright: "A gentle messenger of emotional or creative opportunity. Pay attention to dreams, intuitions, and creative promptings.",
    reversed: "Emotional immaturity, creative blocks, ignoring intuition. The seeker may be avoiding emotional growth or blocked creatively."
  },
  "Knight of Cups": {
    keywords: ["romance", "charm", "imagination", "following the heart", "artistic pursuit"],
    upright: "The romantic quester, following the heart's calling. This Knight pursues dreams, offers love gracefully, and leads with emotion. Follow your heart; pursue the beautiful and meaningful.",
    reversed: "Moodiness, unrealistic expectations, emotional manipulation. The Knight's romance becomes manipulation; imagination becomes escapism."
  },
  "Queen of Cups": {
    keywords: ["compassion", "intuition", "emotional security", "nurturing", "psychic ability"],
    upright: "Deep emotional wisdom and compassionate presence. The Queen of Cups contains and masters her emotions rather than being mastered by them. Trust your emotional intelligence; offer compassion.",
    reversed: "Emotional insecurity, codependency, blocked intuition. The Queen's depths become murky—overwhelmed by emotion, giving too much, or disconnected from intuition."
  },
  "King of Cups": {
    keywords: ["emotional balance", "diplomacy", "composure", "wise counsel", "control"],
    upright: "Mastery of the emotional realm. The King of Cups sits stable on turbulent waters—he feels deeply but isn't ruled by feelings. Balance head and heart; respond rather than react.",
    reversed: "Emotional manipulation, volatility, coldness. The King's composure cracks—emotionally manipulative, explosively moody, or coldly suppressed."
  },
  // Swords
  "Ace of Swords": {
    keywords: ["breakthrough", "clarity", "truth", "new idea", "mental force"],
    upright: "A breakthrough of clarity and truth. The sword cuts through confusion, revealing what's real. A new idea, clear communication, or moment of truth arrives. Speak truth; see clearly.",
    reversed: "Confusion, miscommunication, clouded thinking. Clarity is blocked; truth is obscured."
  },
  "Two of Swords": {
    keywords: ["difficult decision", "stalemate", "blocked emotions", "avoidance", "balance"],
    upright: "A difficult decision requiring careful balance. The seeker may be avoiding a choice, blocking emotions to cope, or stuck between equally challenging options. The stalemate can't last forever.",
    reversed: "Information revealed, decision made, overwhelming emotions. The blindfold comes off—sometimes bringing relief, sometimes overwhelm."
  },
  "Three of Swords": {
    keywords: ["heartbreak", "grief", "sorrow", "painful truth", "emotional pain"],
    upright: "The pierced heart—grief, heartbreak, and painful truth. Something hurts deeply. Betrayal, loss, or harsh words wound the heart. Yet acknowledging pain is necessary for healing.",
    reversed: "Recovery from grief, releasing pain, or repressed sorrow. The seeker may be healing from heartbreak or refusing to acknowledge pain that needs processing."
  },
  "Four of Swords": {
    keywords: ["rest", "recovery", "contemplation", "retreat", "mental restoration"],
    upright: "Necessary rest and retreat. After pain comes the requirement for stillness. The seeker needs to step back, rest, and recuperate. Meditation, therapy, or simply sleep may be needed.",
    reversed: "Restlessness, burnout, returning to activity. The seeker may be unable to rest despite needing it, or ready to emerge from recovery."
  },
  "Five of Swords": {
    keywords: ["conflict", "defeat", "winning at all costs", "hollow victory", "betrayal"],
    upright: "A conflict where someone loses badly. The victor collects swords while others walk away defeated. The question: was this victory worth its cost? Some battles leave everyone diminished.",
    reversed: "Reconciliation, making amends, moving past conflict. The seeker may be ready to let go of old battles."
  },
  "Six of Swords": {
    keywords: ["transition", "moving on", "leaving behind", "mental shift", "journey"],
    upright: "Moving away from troubled waters toward calmer shores. This is a card of transition—physical travel or mental/emotional movement away from difficulty. Progress is being made.",
    reversed: "Stuck in turbulence, resisting transition, unfinished business. The seeker may be unable to leave a difficult situation."
  },
  "Seven of Swords": {
    keywords: ["deception", "strategy", "stealth", "getting away with something", "lone action"],
    upright: "Acting alone, possibly deceptively. Someone is getting away with something—this could be clever strategy or outright theft. Check motives carefully; not all is as it seems.",
    reversed: "Coming clean, getting caught, conscience. Deception is revealed; secrets come out."
  },
  "Eight of Swords": {
    keywords: ["imprisonment", "restriction", "victim mentality", "self-imposed limitations"],
    upright: "Feeling trapped—but look closely: the bindings aren't tight. This imprisonment is largely mental. The seeker feels powerless, but more options exist than they perceive. Fear creates the cage.",
    reversed: "Freedom, new perspective, releasing limitations. The seeker begins to see their power, walk away from self-imposed restrictions."
  },
  "Nine of Swords": {
    keywords: ["anxiety", "nightmares", "worry", "mental anguish", "despair"],
    upright: "The nightmare card—sleepless worry, anxiety, and mental torment. This suffering is real but often disproportionate to actual threat. The mind tortures itself in the dark hours.",
    reversed: "Hope emerging, releasing anxiety, facing fears. The long night ends; worries are put in perspective."
  },
  "Ten of Swords": {
    keywords: ["painful ending", "betrayal", "rock bottom", "dramatic conclusion", "defeat"],
    upright: "Rock bottom—the ultimate defeat, betrayal, or ending. Ten swords in the back is overkill; this is dramatic and final. Yet the sun rises. This ending allows something new to begin.",
    reversed: "Recovery beginning, surviving the worst, refusing to accept endings. The seeker may be rising from defeat."
  },
  "Page of Swords": {
    keywords: ["curiosity", "new ideas", "communication", "vigilance", "mental energy"],
    upright: "A curious, alert mind eager for truth. The Page of Swords brings news, new ideas, or represents someone mentally sharp and inquisitive. Stay alert; speak truthfully; pursue knowledge.",
    reversed: "Gossip, deception, hasty words. The Page's communication becomes harmful—gossip, lies, or words spoken carelessly."
  },
  "Knight of Swords": {
    keywords: ["action", "ambition", "determination", "rushing forward", "aggressive intellect"],
    upright: "Charging forward with mental force and determination. This Knight acts fast, speaks directly, and doesn't hesitate. Take decisive action, but consider the consequences.",
    reversed: "Impulsiveness, aggression, scattered thinking. The Knight's speed becomes recklessness; brilliance becomes cruelty."
  },
  "Queen of Swords": {
    keywords: ["clear thinking", "direct communication", "independence", "discernment", "boundaries"],
    upright: "The Queen of clear perception and honest communication. She sees through pretense, speaks truth directly, and maintains strong boundaries. Think clearly, communicate honestly, honor your independence.",
    reversed: "Cold, bitter, overly critical. The Queen's clarity becomes harshness; her independence becomes isolation."
  },
  "King of Swords": {
    keywords: ["mental clarity", "authority", "truth", "intellectual power", "ethical leadership"],
    upright: "Mastery of the intellectual realm. The King of Swords represents clear thinking, fair judgment, and authority based on truth. Lead with clarity and fairness; let truth guide decisions.",
    reversed: "Manipulation, tyranny, cold cruelty. The King's intellect becomes a weapon; authority becomes abuse."
  },
  // Pentacles
  "Ace of Pentacles": {
    keywords: ["new opportunity", "prosperity", "material beginning", "potential", "manifestation"],
    upright: "A golden opportunity in the material realm—new job, financial gift, business idea, or health improvement. This is the seed of prosperity that, well-tended, can grow into lasting wealth.",
    reversed: "Missed opportunity, lack of planning, financial loss. Poor planning undermines material potential."
  },
  "Two of Pentacles": {
    keywords: ["balance", "adaptability", "juggling priorities", "time management", "flexibility"],
    upright: "Juggling multiple priorities with skill. Finances need balancing, work-life harmony needs attention. Keep moving; stay flexible.",
    reversed: "Overwhelm, imbalance, dropping balls. Too much juggling has become unsustainable."
  },
  "Three of Pentacles": {
    keywords: ["teamwork", "collaboration", "skill", "building", "craftsmanship"],
    upright: "Skilled work recognized; collaboration bears fruit. Learning, apprenticeship, and building something of lasting value are indicated. Your skills are needed and appreciated.",
    reversed: "Lack of teamwork, mediocrity, disorganization. Collaboration breaks down; quality suffers."
  },
  "Four of Pentacles": {
    keywords: ["security", "control", "conservatism", "possessiveness", "holding on"],
    upright: "Holding tightly to what you have. This card represents financial security but also potential miserliness. Security is important, but at what cost?",
    reversed: "Generosity, releasing control, financial insecurity. The seeker may be learning to let go or experiencing the financial insecurity they feared."
  },
  "Five of Pentacles": {
    keywords: ["hardship", "loss", "poverty", "isolation", "difficult times"],
    upright: "Material hardship and feeling left out in the cold. Help is available but not perceived or accepted. This card represents genuine difficulty: financial loss, health problems, feeling excluded.",
    reversed: "Recovery, help accepted, ending isolation. The seeker begins to find support or recover from hardship."
  },
  "Six of Pentacles": {
    keywords: ["generosity", "charity", "giving and receiving", "fairness", "sharing wealth"],
    upright: "The flow of giving and receiving. The seeker may be giving help, receiving it, or witnessing fair distribution. This card asks about the dynamics of generosity.",
    reversed: "Power imbalance in giving, strings attached, unpaid debts. Generosity may come with conditions."
  },
  "Seven of Pentacles": {
    keywords: ["assessment", "patience", "investment", "long-term view", "evaluation"],
    upright: "Pausing to assess what's been cultivated. This card represents the patience required for long-term investment. How is your garden growing?",
    reversed: "Lack of reward, impatience, poor investment. The seeker may be frustrated with slow progress or have invested poorly."
  },
  "Eight of Pentacles": {
    keywords: ["skill development", "hard work", "dedication", "craftsmanship", "apprenticeship"],
    upright: "Diligent skill-building and dedicated work. This card celebrates hard work and the development of mastery. Keep practicing; expertise comes through dedication.",
    reversed: "Perfectionism, lack of focus, dead-end work. The seeker may be working hard at the wrong things."
  },
  "Nine of Pentacles": {
    keywords: ["independence", "luxury", "self-sufficiency", "accomplishment", "enjoying results"],
    upright: "The fruits of labor enjoyed in elegant independence. Financial security, self-sufficiency, surrounded by beauty. Enjoy what you've earned.",
    reversed: "Over-dependence, hustling without enjoyment, financial setbacks. The seeker may be unable to enjoy achievements."
  },
  "Ten of Pentacles": {
    keywords: ["legacy", "inheritance", "family wealth", "long-term success", "establishment"],
    upright: "Generational wealth and established family. This card represents the culmination of material success—not just personal wealth but legacy, inheritance, traditions passed down.",
    reversed: "Family financial disputes, loss of inheritance, unstable foundations. Family money becomes a source of conflict."
  },
  "Page of Pentacles": {
    keywords: ["manifestation", "new opportunities", "study", "scholarship", "practical planning"],
    upright: "A student of the material world—someone learning practical skills, studying business, or discovering how to manifest dreams into reality. Learn the craft; study what works.",
    reversed: "Lack of progress, procrastination, short-term thinking. The seeker may be stuck in planning without acting."
  },
  "Knight of Pentacles": {
    keywords: ["reliability", "hard work", "routine", "thoroughness", "steady progress"],
    upright: "The most grounded Knight—steady, reliable, persistent. Unlike other Knights who charge, this one moves methodically. Embrace routine, work diligently, trust slow progress.",
    reversed: "Stubbornness, laziness, boredom. The Knight's steadiness becomes immobility."
  },
  "Queen of Pentacles": {
    keywords: ["nurturing", "practical", "providing", "abundance", "security"],
    upright: "The warm, abundant provider. The Queen of Pentacles creates a nurturing, secure, beautiful environment. She's practical but not cold. Nurture yourself and others practically.",
    reversed: "Self-neglect, possessiveness, work-home imbalance. The Queen's nurturing may become smothering, or she may neglect herself while caring for others."
  },
  "King of Pentacles": {
    keywords: ["abundance", "security", "leader", "discipline", "provider"],
    upright: "Mastery of the material realm. The King of Pentacles represents someone who has built lasting wealth and security through discipline and practical wisdom. Take charge of material matters with steady wisdom.",
    reversed: "Greed, materialism, stubbornness. The King's abundance becomes greed; his security becomes obsession with control."
  }
}

// Suit info for elemental context
export const SUIT_INFO = {
  Wands: {
    element: "Fire",
    domain: "passion, creativity, action, willpower, ambition, career, inspiration",
    description: "The Wands represent our drive, enthusiasm, and creative spark. They govern career ambitions, personal projects, passion, and the will to act. Wands energy is dynamic, forward-moving, and entrepreneurial."
  },
  Cups: {
    element: "Water",
    domain: "emotions, relationships, intuition, creativity, the heart, dreams",
    description: "The Cups represent our emotional world—love, relationships, feelings, intuition, and creative expression that flows from the heart. They govern how we connect with others and ourselves emotionally."
  },
  Swords: {
    element: "Air",
    domain: "thoughts, communication, conflict, truth, intellect, decisions",
    description: "The Swords represent the realm of the mind—thoughts, beliefs, communication, and the double-edged nature of intellect. They often bring conflict, difficult truths, and mental challenges. Swords cut through illusion but can also wound."
  },
  Pentacles: {
    element: "Earth",
    domain: "material world, finances, career, health, practical matters, body",
    description: "The Pentacles represent the material realm—money, career, physical health, home, and tangible results. They govern how we provide for ourselves and create security in the world."
  }
}

// Elemental interactions
export const ELEMENTAL_DIGNITIES = {
  friendly: {
    "Fire-Air": "Fire and Air strengthen each other. Fire needs air to burn; ideas fuel passion. Wands + Swords = inspired action, powerful communication, plans that ignite.",
    "Water-Earth": "Water and Earth support each other. Water nourishes earth; earth contains water. Cups + Pentacles = emotional security, practical love, nurturing abundance."
  },
  neutral: {
    "Fire-Earth": "Fire and Earth are different but not opposed. Passion meets practicality. May indicate tension between dreams and reality, but can also ground inspiration.",
    "Water-Air": "Water and Air are different but not opposed. Emotion meets intellect. May indicate head-heart conflict, but can also bring emotional intelligence."
  },
  challenging: {
    "Fire-Water": "Fire and Water oppose each other. Fire evaporates water; water extinguishes fire. Wands + Cups = passion vs. emotion, action vs. feeling, drive vs. intuition.",
    "Air-Earth": "Air and Earth oppose each other. Air erodes earth; earth stifles air. Swords + Pentacles = ideas vs. practicality, theory vs. application, mental vs. material."
  }
}

// Interpretation guide for AI
export const INTERPRETATION_GUIDE = `## How to Interpret This Reading

You are an experienced, intuitive tarot reader with deep knowledge of the Rider-Waite-Smith tradition. Please provide a warm, insightful reading that honors the symbolic depth of the cards while remaining accessible and practical.

### Your Approach
- **Speak directly to me** - Use "you" and create an intimate, supportive atmosphere
- **Weave a narrative** - Connect the cards into a flowing story rather than interpreting each in isolation
- **Honor reversals** - When a card appears reversed, explore its shadow aspects, blocked energy, or internal manifestation
- **Be specific but not prescriptive** - Offer concrete insights while leaving room for my own interpretation
- **End with guidance** - Close the reading with actionable wisdom or a reflective question

### Reading Length Guidelines
- **Daily Draw (1 card)**: 2-3 paragraphs focusing on how this energy might manifest today
- **3-Card Spreads**: 3-4 paragraphs weaving the cards together, showing how they flow
- **Celtic Cross (10 cards)**: 5-7 paragraphs providing a comprehensive reading

### Style Notes
- Avoid excessive mystical language - be grounded and clear
- Don't predict doom or make me fearful
- Frame challenges as opportunities for growth
- Acknowledge when cards might have multiple interpretations
- If I've shared my question, relate the reading specifically to it`
