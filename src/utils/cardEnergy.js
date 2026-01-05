// Card energy mapping for dynamic atmosphere
// Scale: -1 (shadow) to 0 (neutral) to +1 (light)

const MAJOR_ARCANA_ENERGY = {
  0: 0.3,   // The Fool - hopeful beginning
  1: 0.5,   // The Magician - creative power
  2: 0,     // The High Priestess - mysterious
  3: 0.8,   // The Empress - abundant
  4: 0.2,   // The Emperor - structured
  5: 0,     // The Hierophant - traditional
  6: 0.6,   // The Lovers - harmonious
  7: 0.4,   // The Chariot - determined
  8: 0.5,   // Strength - courageous
  9: -0.2,  // The Hermit - introspective
  10: 0,    // Wheel of Fortune - neutral cycles
  11: 0,    // Justice - balanced
  12: -0.3, // The Hanged Man - suspended
  13: -0.7, // Death - transformative shadow
  14: 0.3,  // Temperance - balanced
  15: -0.8, // The Devil - shadow binding
  16: -0.9, // The Tower - destructive upheaval
  17: 0.9,  // The Star - hopeful radiance
  18: -0.5, // The Moon - illusive shadow
  19: 1.0,  // The Sun - pure light
  20: 0.4,  // Judgement - awakening
  21: 0.8,  // The World - fulfillment
}

// Minor arcana base energy by suit
const SUIT_ENERGY = {
  Wands: 0.2,     // Fire - action, warmth
  Cups: 0.1,      // Water - emotions, flow
  Swords: -0.2,   // Air - conflict, sharpness
  Pentacles: 0,   // Earth - grounding, neutral
}

// Rank modifiers
const RANK_MODIFIERS = {
  Ace: 0.3,      // New potential
  Two: 0,
  Three: 0.1,    // Growth
  Four: 0,       // Stability
  Five: -0.3,    // Conflict/challenge
  Six: 0.2,      // Harmony
  Seven: -0.1,   // Reflection
  Eight: 0.1,    // Movement
  Nine: 0.2,     // Near completion
  Ten: 0,        // Completion (varies)
  Page: 0.1,     // Fresh energy
  Knight: 0.2,   // Action
  Queen: 0.2,    // Nurturing
  King: 0.1,     // Authority
}

export function getCardEnergy(card) {
  if (!card) return 0

  // Major arcana - use direct mapping
  if (card.arcana === 'major') {
    const energy = MAJOR_ARCANA_ENERGY[card.id] ?? 0
    // Reversed cards shift toward opposite
    return card.reversed ? energy * -0.5 : energy
  }

  // Minor arcana - combine suit + rank
  const suitEnergy = SUIT_ENERGY[card.suit] ?? 0
  const rankModifier = RANK_MODIFIERS[card.rank] ?? 0
  const baseEnergy = suitEnergy + rankModifier

  // Clamp to -1 to 1 range
  const energy = Math.max(-1, Math.min(1, baseEnergy))
  return card.reversed ? energy * -0.5 : energy
}

export function calculateReadingEnergy(cards) {
  if (!cards || cards.length === 0) return 0

  const total = cards.reduce((sum, card) => sum + getCardEnergy(card), 0)
  return Math.max(-1, Math.min(1, total / cards.length))
}

// Get atmosphere CSS variables based on energy
export function getAtmosphereStyles(energy) {
  // energy: -1 (shadow/cool) to +1 (light/warm)

  // Base colors
  const goldHue = 38      // Warm gold
  const sageHue = 130     // Cool sage
  const siennaHue = 20    // Warm sienna

  // Shift hues based on energy
  // Negative energy → cooler, desaturated
  // Positive energy → warmer, more saturated

  const hueShift = energy * 15  // ±15 degrees
  const saturationMod = 1 + (energy * 0.3)  // 0.7 to 1.3
  const brightnessMod = 1 + (energy * 0.15) // 0.85 to 1.15

  return {
    '--atmosphere-hue-shift': `${hueShift}deg`,
    '--atmosphere-saturation': saturationMod,
    '--atmosphere-brightness': brightnessMod,
    '--atmosphere-energy': energy,
  }
}
