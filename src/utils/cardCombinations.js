// Notable card combinations that add meaning to readings
// These are well-known pairings from traditional tarot interpretation

export const CARD_COMBINATIONS = [
  // Love & Relationship pairs
  {
    cards: ["The Lovers", "Two of Cups"],
    meaning: "A powerful love connection or soulmate energy. Deep romantic harmony."
  },
  {
    cards: ["The Empress", "The Emperor"],
    meaning: "Balance of feminine and masculine energies. A power couple or complete partnership."
  },
  {
    cards: ["Two of Cups", "Ten of Cups"],
    meaning: "Love leading to lasting happiness. Emotional fulfillment in relationships."
  },
  {
    cards: ["The Lovers", "The Devil"],
    meaning: "Passion with complications. Examine whether desire is healthy or obsessive."
  },

  // Transformation pairs
  {
    cards: ["Death", "The Tower"],
    meaning: "Major life upheaval. Complete transformation is unavoidable but ultimately liberating."
  },
  {
    cards: ["Death", "The Star"],
    meaning: "Hope after endings. Renewal follows necessary transformation."
  },
  {
    cards: ["The Tower", "The Star"],
    meaning: "Destruction leading to hope. From chaos comes clarity and healing."
  },
  {
    cards: ["Death", "Judgement"],
    meaning: "Profound rebirth. An old chapter closes as you answer a higher calling."
  },

  // Success & Achievement pairs
  {
    cards: ["The Magician", "The World"],
    meaning: "Manifestation complete. Your skills and will have created something whole."
  },
  {
    cards: ["The Sun", "The World"],
    meaning: "Ultimate success and joy. Achievement of your highest aspirations."
  },
  {
    cards: ["Wheel of Fortune", "The World"],
    meaning: "A destined cycle completing. Karma fulfilled, ready for a new chapter."
  },
  {
    cards: ["The Chariot", "The Sun"],
    meaning: "Victory and joy. Triumph through willpower brings happiness."
  },

  // Challenge pairs
  {
    cards: ["The Moon", "The Devil"],
    meaning: "Illusions and shadow work needed. Hidden fears or deceptions at play."
  },
  {
    cards: ["The Tower", "Ten of Swords"],
    meaning: "Rock bottom. Complete destruction of the old—but the only way is up."
  },
  {
    cards: ["Five of Cups", "Three of Swords"],
    meaning: "Deep grief or heartbreak. Allow yourself to mourn before moving forward."
  },

  // Wisdom & Guidance pairs
  {
    cards: ["The High Priestess", "The Hermit"],
    meaning: "Deep inner wisdom. Trust your intuition and take time for introspection."
  },
  {
    cards: ["The Hierophant", "The Hermit"],
    meaning: "Seeking wisdom from both tradition and within. A spiritual quest."
  },
  {
    cards: ["The High Priestess", "The Moon"],
    meaning: "Hidden knowledge emerging. Pay attention to dreams and intuition."
  },

  // New Beginnings pairs
  {
    cards: ["The Fool", "The World"],
    meaning: "One journey ends as another begins. Completion leads to new adventure."
  },
  {
    cards: ["The Fool", "Ace of Wands"],
    meaning: "Bold new creative beginning. Take the leap with passion."
  },
  {
    cards: ["The Magician", "Ace of Wands"],
    meaning: "Powerful new initiative. You have all the tools to begin."
  },

  // Court card connections
  {
    cards: ["Queen of Cups", "King of Cups"],
    meaning: "Emotional mastery and maturity. A deeply intuitive partnership."
  },
  {
    cards: ["Queen of Swords", "King of Swords"],
    meaning: "Sharp minds together. Clear communication and intellectual partnership."
  }
]

export function findCombinations(cards) {
  const cardNames = cards.map(c => c.name)
  const found = []

  for (const combo of CARD_COMBINATIONS) {
    if (combo.cards.every(name => cardNames.includes(name))) {
      found.push(combo)
    }
  }

  return found
}
