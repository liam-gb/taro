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

  p += `## The Reading: ${spread.name}\n\n`
  cards.forEach((c, i) => {
    p += `**${spread.positions[i].name}** (${spread.positions[i].description}): ${c.name} — ${c.reversed ? '**REVERSED**' : 'Upright'}\n`
  })

  if (suits.length) {
    p += '\n## Elemental Context\n'
    suits.forEach(s => p += `**${s} (${SUIT_INFO[s].element})**: ${SUIT_INFO[s].description}\n\n`)
  }

  if (majorCount) p += `\n*Note: ${majorCount} Major Arcana card${majorCount > 1 ? 's appear' : ' appears'} in this reading, indicating significant life lessons or karmic themes.*\n`

  if (elements.length >= 2) {
    p += '\n## Elemental Interactions\n'
    for (let i = 0; i < elements.length; i++)
      for (let j = i + 1; j < elements.length; j++) {
        const int = getInteraction(elements[i], elements[j])
        if (int) p += `- ${int}\n`
      }
  }

  p += '\n## Card Meanings for Your Reading\n\n'
  cards.forEach((c, i) => {
    const interp = CARD_INTERPRETATIONS[c.name]
    if (!interp) return
    p += `### ${c.name} (${spread.positions[i].name} position)${c.reversed ? ' — REVERSED' : ''}\n`
    p += `**Keywords**: ${interp.keywords.join(', ')}\n\n`
    p += `**Upright meaning**: ${interp.upright}\n\n`
    p += `**Reversed meaning**: ${interp.reversed}\n\n`
    if (c.reversed) p += `*This card appeared reversed in your reading, so the reversed meaning is particularly relevant, though both orientations inform interpretation.*\n\n`
  })

  p += `---\n\n${INTERPRETATION_GUIDE}\n\n`
  p += `---\n\n## Please Interpret My Reading\n\nUsing the card meanings and guidance above, please provide a thoughtful interpretation of this ${spread.name} reading${question ? ' in relation to my question' : ''}. Weave the cards together into a coherent narrative and end with actionable wisdom or a reflective question for me to consider.`

  return p
}
