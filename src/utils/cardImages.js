// Card image path mapping
export const CARD_IMAGES = {
  back: '/cards/CardBacks.png',
  major: [
    '/cards/00-TheFool.png',
    '/cards/01-TheMagician.png',
    '/cards/02-TheHighPriestess.png',
    '/cards/03-TheEmpress.png',
    '/cards/04-TheEmperor.png',
    '/cards/05-TheHierophant.png',
    '/cards/06-TheLovers.png',
    '/cards/07-TheChariot.png',
    '/cards/08-Strength.png',
    '/cards/09-TheHermit.png',
    '/cards/10-WheelOfFortune.png',
    '/cards/11-Justice.png',
    '/cards/12-TheHangedMan.png',
    '/cards/13-Death.png',
    '/cards/14-Temperance.png',
    '/cards/15-TheDevil.png',
    '/cards/16-TheTower.png',
    '/cards/17-TheStar.png',
    '/cards/18-TheMoon.png',
    '/cards/19-TheSun.png',
    '/cards/20-Judgement.png',
    '/cards/21-TheWorld.png'
  ],
  Wands: Array.from({length: 14}, (_, i) => `/cards/Wands${String(i + 1).padStart(2, '0')}.png`),
  Cups: Array.from({length: 14}, (_, i) => `/cards/Cups${String(i + 1).padStart(2, '0')}.png`),
  Swords: Array.from({length: 14}, (_, i) => `/cards/Swords${String(i + 1).padStart(2, '0')}.png`),
  Pentacles: Array.from({length: 14}, (_, i) => `/cards/Pentacles${String(i + 1).padStart(2, '0')}.png`)
}

export const getCardImage = (card) => {
  if (!card) return CARD_IMAGES.back
  if (card.arcana === 'major') {
    return CARD_IMAGES.major[card.id]
  }
  return CARD_IMAGES[card.suit][card.value - 1]
}
