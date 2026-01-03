// Major Arcana cards
export const MAJOR_ARCANA = [
  { id: 0, name: "The Fool", numeral: "0", arcana: "major", keywords: ["beginnings", "innocence", "spontaneity", "leap of faith"], element: "Air" },
  { id: 1, name: "The Magician", numeral: "I", arcana: "major", keywords: ["manifestation", "willpower", "skill", "resourcefulness"], element: "Air" },
  { id: 2, name: "The High Priestess", numeral: "II", arcana: "major", keywords: ["intuition", "mystery", "inner voice", "unconscious"], element: "Water" },
  { id: 3, name: "The Empress", numeral: "III", arcana: "major", keywords: ["abundance", "nurturing", "fertility", "nature"], element: "Earth" },
  { id: 4, name: "The Emperor", numeral: "IV", arcana: "major", keywords: ["authority", "structure", "control", "father figure"], element: "Fire" },
  { id: 5, name: "The Hierophant", numeral: "V", arcana: "major", keywords: ["tradition", "conformity", "wisdom", "spiritual guidance"], element: "Earth" },
  { id: 6, name: "The Lovers", numeral: "VI", arcana: "major", keywords: ["love", "harmony", "choices", "union"], element: "Air" },
  { id: 7, name: "The Chariot", numeral: "VII", arcana: "major", keywords: ["willpower", "determination", "victory", "control"], element: "Water" },
  { id: 8, name: "Strength", numeral: "VIII", arcana: "major", keywords: ["courage", "patience", "inner strength", "compassion"], element: "Fire" },
  { id: 9, name: "The Hermit", numeral: "IX", arcana: "major", keywords: ["introspection", "solitude", "guidance", "inner wisdom"], element: "Earth" },
  { id: 10, name: "Wheel of Fortune", numeral: "X", arcana: "major", keywords: ["cycles", "fate", "turning point", "destiny"], element: "Fire" },
  { id: 11, name: "Justice", numeral: "XI", arcana: "major", keywords: ["fairness", "truth", "karma", "accountability"], element: "Air" },
  { id: 12, name: "The Hanged Man", numeral: "XII", arcana: "major", keywords: ["surrender", "new perspective", "pause", "letting go"], element: "Water" },
  { id: 13, name: "Death", numeral: "XIII", arcana: "major", keywords: ["transformation", "endings", "change", "transition"], element: "Water" },
  { id: 14, name: "Temperance", numeral: "XIV", arcana: "major", keywords: ["balance", "moderation", "patience", "harmony"], element: "Fire" },
  { id: 15, name: "The Devil", numeral: "XV", arcana: "major", keywords: ["shadow self", "attachment", "addiction", "bondage"], element: "Earth" },
  { id: 16, name: "The Tower", numeral: "XVI", arcana: "major", keywords: ["upheaval", "revelation", "sudden change", "awakening"], element: "Fire" },
  { id: 17, name: "The Star", numeral: "XVII", arcana: "major", keywords: ["hope", "faith", "renewal", "inspiration"], element: "Air" },
  { id: 18, name: "The Moon", numeral: "XVIII", arcana: "major", keywords: ["illusion", "fear", "subconscious", "intuition"], element: "Water" },
  { id: 19, name: "The Sun", numeral: "XIX", arcana: "major", keywords: ["joy", "success", "vitality", "positivity"], element: "Fire" },
  { id: 20, name: "Judgement", numeral: "XX", arcana: "major", keywords: ["rebirth", "inner calling", "reflection", "reckoning"], element: "Fire" },
  { id: 21, name: "The World", numeral: "XXI", arcana: "major", keywords: ["completion", "achievement", "wholeness", "fulfillment"], element: "Earth" }
]

// Suit definitions
export const SUITS = {
  Wands: { element: "Fire", domain: "passion, creativity, action" },
  Cups: { element: "Water", domain: "emotions, relationships, intuition" },
  Swords: { element: "Air", domain: "thoughts, conflict, truth" },
  Pentacles: { element: "Earth", domain: "finances, career, material" }
}

// Minor card templates
const MINOR_CARDS = [
  { rank: "Ace", value: 1, keywords: ["new beginning", "potential", "opportunity"] },
  { rank: "Two", value: 2, keywords: ["balance", "partnership", "duality"] },
  { rank: "Three", value: 3, keywords: ["growth", "creativity", "collaboration"] },
  { rank: "Four", value: 4, keywords: ["stability", "foundation", "structure"] },
  { rank: "Five", value: 5, keywords: ["conflict", "challenge", "change"] },
  { rank: "Six", value: 6, keywords: ["harmony", "communication", "transition"] },
  { rank: "Seven", value: 7, keywords: ["reflection", "assessment", "perseverance"] },
  { rank: "Eight", value: 8, keywords: ["movement", "speed", "progress"] },
  { rank: "Nine", value: 9, keywords: ["fruition", "attainment", "wisdom"] },
  { rank: "Ten", value: 10, keywords: ["completion", "ending", "fulfillment"] },
  { rank: "Page", value: 11, keywords: ["messenger", "student", "new energy"] },
  { rank: "Knight", value: 12, keywords: ["action", "adventure", "movement"] },
  { rank: "Queen", value: 13, keywords: ["nurturing", "intuitive", "mastery"] },
  { rank: "King", value: 14, keywords: ["authority", "control", "leadership"] }
]

// Generate minor arcana
const generateMinorArcana = () => {
  const cards = []
  let id = 22
  Object.entries(SUITS).forEach(([suit, suitData]) => {
    MINOR_CARDS.forEach(cardData => {
      cards.push({
        id: id++,
        name: `${cardData.rank} of ${suit}`,
        suit,
        rank: cardData.rank,
        value: cardData.value,
        arcana: 'minor',
        element: suitData.element,
        domain: suitData.domain,
        keywords: cardData.keywords
      })
    })
  })
  return cards
}

export const MINOR_ARCANA = generateMinorArcana()
export const FULL_DECK = [...MAJOR_ARCANA, ...MINOR_ARCANA]
