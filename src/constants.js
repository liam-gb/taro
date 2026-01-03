// Card configuration
export const CARD_SIZES = {
  small: { width: 90, height: 148 },
  normal: { width: 140, height: 230 },
  large: { width: 180, height: 295 }
}

export const SHUFFLE_DECK_SIZE = { width: 260, height: 400 }

// Animation & styling
export const CARD_TRANSITION = 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)'

export const CARD_SHADOWS = {
  idle: '0 10px 30px rgba(0,0,0,0.4)',
  hovered: '0 25px 50px rgba(0,0,0,0.5)',
  hoveredGlow: '0 25px 50px rgba(0,0,0,0.5), 0 0 30px rgba(147, 112, 219, 0.2)'
}

// Game mechanics
export const REVERSAL_PROBABILITY = 0.3
export const REQUIRED_SHUFFLES = 3
export const HOVER_ROTATION_SCALE = 10
export const CARD_FAN_ROTATION = 4  // degrees between cards in fan display
export const HOVER_CARD_COUNT = 5
export const SHUFFLE_STACK_COUNT = 6
