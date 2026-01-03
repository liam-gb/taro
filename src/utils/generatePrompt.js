import {
  CARD_INTERPRETATIONS,
  SUIT_INFO,
  ELEMENTAL_DIGNITIES,
  INTERPRETATION_GUIDE
} from '../data'

export function generateReadingPrompt(drawnCards, spread, question) {
  // Build a comprehensive, self-contained prompt
  let prompt = `# Tarot Reading Request\n\n`

  // Add the question if provided
  if (question) {
    prompt += `## My Question\n"${question}"\n\n`
  }

  // Add the spread and cards drawn
  prompt += `## The Reading: ${spread.name}\n\n`
  drawnCards.forEach((card, index) => {
    const pos = spread.positions[index]
    const orientation = card.reversed ? '**REVERSED**' : 'Upright'
    prompt += `**${pos.name}** (${pos.description}): ${card.name} — ${orientation}\n`
  })

  // Gather unique suits present for context
  const suitsPresent = new Set()
  const hasMajorArcana = drawnCards.some(c => c.arcana === 'major')
  drawnCards.forEach(card => {
    if (card.suit) suitsPresent.add(card.suit)
  })

  // Add suit context if minor arcana present
  if (suitsPresent.size > 0) {
    prompt += `\n## Elemental Context\n`
    suitsPresent.forEach(suit => {
      const info = SUIT_INFO[suit]
      prompt += `**${suit} (${info.element})**: ${info.description}\n\n`
    })
  }

  // Add Major Arcana note if present
  if (hasMajorArcana) {
    const majorCount = drawnCards.filter(c => c.arcana === 'major').length
    prompt += `\n*Note: ${majorCount} Major Arcana card${majorCount > 1 ? 's appear' : ' appears'} in this reading, indicating significant life lessons or karmic themes.*\n`
  }

  // Add elemental interactions if multiple suits
  if (suitsPresent.size >= 2) {
    prompt += `\n## Elemental Interactions\n`
    const elements = [...suitsPresent].map(s => SUIT_INFO[s].element)
    for (let i = 0; i < elements.length; i++) {
      for (let j = i + 1; j < elements.length; j++) {
        const pair1 = `${elements[i]}-${elements[j]}`
        const pair2 = `${elements[j]}-${elements[i]}`
        if (ELEMENTAL_DIGNITIES.friendly[pair1] || ELEMENTAL_DIGNITIES.friendly[pair2]) {
          prompt += `- ${ELEMENTAL_DIGNITIES.friendly[pair1] || ELEMENTAL_DIGNITIES.friendly[pair2]}\n`
        } else if (ELEMENTAL_DIGNITIES.challenging[pair1] || ELEMENTAL_DIGNITIES.challenging[pair2]) {
          prompt += `- ${ELEMENTAL_DIGNITIES.challenging[pair1] || ELEMENTAL_DIGNITIES.challenging[pair2]}\n`
        } else if (ELEMENTAL_DIGNITIES.neutral[pair1] || ELEMENTAL_DIGNITIES.neutral[pair2]) {
          prompt += `- ${ELEMENTAL_DIGNITIES.neutral[pair1] || ELEMENTAL_DIGNITIES.neutral[pair2]}\n`
        }
      }
    }
  }

  // Add detailed card meanings for each drawn card
  prompt += `\n## Card Meanings for Your Reading\n\n`
  drawnCards.forEach((card, index) => {
    const pos = spread.positions[index]
    const interp = CARD_INTERPRETATIONS[card.name]
    if (interp) {
      prompt += `### ${card.name} (${pos.name} position)${card.reversed ? ' — REVERSED' : ''}\n`
      prompt += `**Keywords**: ${interp.keywords.join(', ')}\n\n`
      prompt += `**Upright meaning**: ${interp.upright}\n\n`
      prompt += `**Reversed meaning**: ${interp.reversed}\n\n`
      if (card.reversed) {
        prompt += `*This card appeared reversed in your reading, so the reversed meaning is particularly relevant, though both orientations inform interpretation.*\n\n`
      }
    }
  })

  // Add interpretation guide
  prompt += `---\n\n${INTERPRETATION_GUIDE}\n\n`

  // Add closing request
  prompt += `---\n\n## Please Interpret My Reading\n\nUsing the card meanings and guidance above, please provide a thoughtful interpretation of this ${spread.name} reading${question ? ' in relation to my question' : ''}. Weave the cards together into a coherent narrative and end with actionable wisdom or a reflective question for me to consider.`

  return prompt
}
