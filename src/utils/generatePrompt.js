import { CARD_INTERPRETATIONS, SUIT_INFO, ELEMENTAL_DIGNITIES, INTERPRETATION_GUIDE } from '../data'

const getInteraction = (a, b) =>
  ['friendly', 'challenging', 'neutral'].flatMap(cat =>
    [ELEMENTAL_DIGNITIES[cat][`${a}-${b}`], ELEMENTAL_DIGNITIES[cat][`${b}-${a}`]]
  ).find(Boolean)

export function generateReadingPrompt(cards, spread, question) {
  const suits = [...new Set(cards.filter(c => c.suit).map(c => c.suit))]
  const majorCount = cards.filter(c => c.arcana === 'major').length
  const elements = suits.map(s => SUIT_INFO[s].element)

  let p = '# Tarot Reading Request\n\n'
  if (question) p += `## My Question\n"${question}"\n\n`

  // Cards drawn
  p += `## The Reading: ${spread.name}\n\n`
  cards.forEach((c, i) => {
    p += `**${spread.positions[i].name}** (${spread.positions[i].description}): ${c.name} — ${c.reversed ? '**REVERSED**' : 'Upright'}\n`
  })

  // Elemental context
  if (suits.length) {
    p += '\n## Elemental Context\n'
    suits.forEach(s => p += `**${s} (${SUIT_INFO[s].element})**: ${SUIT_INFO[s].description}\n\n`)
  }

  if (majorCount) p += `\n*Note: ${majorCount} Major Arcana card${majorCount > 1 ? 's appear' : ' appears'}, indicating significant life lessons or karmic themes.*\n`

  // Elemental interactions
  if (elements.length >= 2) {
    p += '\n## Elemental Interactions\n'
    for (let i = 0; i < elements.length; i++)
      for (let j = i + 1; j < elements.length; j++) {
        const int = getInteraction(elements[i], elements[j])
        if (int) p += `- ${int}\n`
      }
  }

  // Card meanings
  p += '\n## Card Meanings for Your Reading\n\n'
  cards.forEach((c, i) => {
    const interp = CARD_INTERPRETATIONS[c.name]
    if (!interp) return
    p += `### ${c.name} (${spread.positions[i].name})${c.reversed ? ' — REVERSED' : ''}\n`
    p += `**Keywords**: ${interp.keywords.join(', ')}\n\n**Upright**: ${interp.upright}\n\n**Reversed**: ${interp.reversed}\n\n`
    if (c.reversed) p += `*Reversed meaning is particularly relevant here.*\n\n`
  })

  p += `---\n\n${INTERPRETATION_GUIDE}\n\n---\n\n`
  p += `## Please Interpret My Reading\n\nProvide a thoughtful interpretation of this ${spread.name} reading${question ? ' in relation to my question' : ''}. Weave the cards together into a coherent narrative and end with actionable wisdom.`

  return p
}
