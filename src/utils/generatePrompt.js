import {
  CARD_INTERPRETATIONS,
  SUIT_INFO,
  ELEMENTAL_DIGNITIES,
  INTERPRETATION_GUIDE
} from '../data'

function getElementalInteraction(elem1, elem2) {
  const pairs = [`${elem1}-${elem2}`, `${elem2}-${elem1}`]
  for (const category of ['friendly', 'challenging', 'neutral']) {
    for (const pair of pairs) {
      if (ELEMENTAL_DIGNITIES[category][pair]) {
        return ELEMENTAL_DIGNITIES[category][pair]
      }
    }
  }
  return null
}

export function generateReadingPrompt(drawnCards, spread, question) {
  const lines = ['# Tarot Reading Request\n']

  if (question) {
    lines.push(`## My Question\n"${question}"\n`)
  }

  // Cards drawn
  lines.push(`## The Reading: ${spread.name}\n`)
  drawnCards.forEach((card, i) => {
    const pos = spread.positions[i]
    const orientation = card.reversed ? '**REVERSED**' : 'Upright'
    lines.push(`**${pos.name}** (${pos.description}): ${card.name} — ${orientation}`)
  })

  // Gather suit/element info
  const suits = [...new Set(drawnCards.filter(c => c.suit).map(c => c.suit))]
  const hasMajor = drawnCards.some(c => c.arcana === 'major')

  // Elemental context
  if (suits.length > 0) {
    lines.push('\n## Elemental Context')
    suits.forEach(suit => {
      const info = SUIT_INFO[suit]
      lines.push(`**${suit} (${info.element})**: ${info.description}\n`)
    })
  }

  // Major arcana note
  if (hasMajor) {
    const count = drawnCards.filter(c => c.arcana === 'major').length
    lines.push(`\n*Note: ${count} Major Arcana card${count > 1 ? 's appear' : ' appears'} in this reading, indicating significant life lessons or karmic themes.*`)
  }

  // Elemental interactions
  if (suits.length >= 2) {
    lines.push('\n## Elemental Interactions')
    const elements = suits.map(s => SUIT_INFO[s].element)
    for (let i = 0; i < elements.length; i++) {
      for (let j = i + 1; j < elements.length; j++) {
        const interaction = getElementalInteraction(elements[i], elements[j])
        if (interaction) lines.push(`- ${interaction}`)
      }
    }
  }

  // Card meanings
  lines.push('\n## Card Meanings for Your Reading\n')
  drawnCards.forEach((card, i) => {
    const pos = spread.positions[i]
    const interp = CARD_INTERPRETATIONS[card.name]
    if (interp) {
      lines.push(`### ${card.name} (${pos.name} position)${card.reversed ? ' — REVERSED' : ''}`)
      lines.push(`**Keywords**: ${interp.keywords.join(', ')}\n`)
      lines.push(`**Upright meaning**: ${interp.upright}\n`)
      lines.push(`**Reversed meaning**: ${interp.reversed}\n`)
      if (card.reversed) {
        lines.push(`*This card appeared reversed in your reading, so the reversed meaning is particularly relevant, though both orientations inform interpretation.*\n`)
      }
    }
  })

  // Guide and closing
  lines.push(`---\n\n${INTERPRETATION_GUIDE}\n`)
  lines.push(`---\n\n## Please Interpret My Reading\n\nUsing the card meanings and guidance above, please provide a thoughtful interpretation of this ${spread.name} reading${question ? ' in relation to my question' : ''}. Weave the cards together into a coherent narrative and end with actionable wisdom or a reflective question for me to consider.`)

  return lines.join('\n')
}
