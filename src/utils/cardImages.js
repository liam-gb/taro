// Card image path mapping - use BASE_URL for GitHub Pages compatibility
const base = import.meta.env.BASE_URL

export const CARD_IMAGES = {
  back: `${base}cards/CardBacks.png`,
  major: [
    `${base}cards/00-TheFool.png`,
    `${base}cards/01-TheMagician.png`,
    `${base}cards/02-TheHighPriestess.png`,
    `${base}cards/03-TheEmpress.png`,
    `${base}cards/04-TheEmperor.png`,
    `${base}cards/05-TheHierophant.png`,
    `${base}cards/06-TheLovers.png`,
    `${base}cards/07-TheChariot.png`,
    `${base}cards/08-Strength.png`,
    `${base}cards/09-TheHermit.png`,
    `${base}cards/10-WheelOfFortune.png`,
    `${base}cards/11-Justice.png`,
    `${base}cards/12-TheHangedMan.png`,
    `${base}cards/13-Death.png`,
    `${base}cards/14-Temperance.png`,
    `${base}cards/15-TheDevil.png`,
    `${base}cards/16-TheTower.png`,
    `${base}cards/17-TheStar.png`,
    `${base}cards/18-TheMoon.png`,
    `${base}cards/19-TheSun.png`,
    `${base}cards/20-Judgement.png`,
    `${base}cards/21-TheWorld.png`
  ],
  Wands: Array.from({length: 14}, (_, i) => `${base}cards/Wands${String(i + 1).padStart(2, '0')}.png`),
  Cups: Array.from({length: 14}, (_, i) => `${base}cards/Cups${String(i + 1).padStart(2, '0')}.png`),
  Swords: Array.from({length: 14}, (_, i) => `${base}cards/Swords${String(i + 1).padStart(2, '0')}.png`),
  Pentacles: Array.from({length: 14}, (_, i) => `${base}cards/Pentacles${String(i + 1).padStart(2, '0')}.png`)
}

export const getCardImage = (card) => {
  if (!card) return CARD_IMAGES.back
  if (card.arcana === 'major') {
    return CARD_IMAGES.major[card.id]
  }
  return CARD_IMAGES[card.suit][card.value - 1]
}
