import { useState, useEffect, useRef } from 'react'
import { findCombinations } from '../utils/cardCombinations'
import { SUIT_INFO, ELEMENTAL_DIGNITIES } from '../data/interpretations'

// Get element from a card
function getCardElement(card) {
  if (!card) return null

  // Major Arcana have element defined in interpretations
  // Minor Arcana get element from suit
  const suitMatch = card.name.match(/of (Wands|Cups|Swords|Pentacles)/)
  if (suitMatch) {
    return SUIT_INFO[suitMatch[1]]?.element || null
  }

  // For Major Arcana, check common element associations
  const majorElements = {
    'The Fool': 'Air',
    'The Magician': 'Air',
    'The High Priestess': 'Water',
    'The Empress': 'Earth',
    'The Emperor': 'Fire',
    'The Hierophant': 'Earth',
    'The Lovers': 'Air',
    'The Chariot': 'Water',
    'Strength': 'Fire',
    'The Hermit': 'Earth',
    'Wheel of Fortune': 'Fire',
    'Justice': 'Air',
    'The Hanged Man': 'Water',
    'Death': 'Water',
    'Temperance': 'Fire',
    'The Devil': 'Earth',
    'The Tower': 'Fire',
    'The Star': 'Air',
    'The Moon': 'Water',
    'The Sun': 'Fire',
    'Judgement': 'Fire',
    'The World': 'Earth'
  }

  return majorElements[card.name] || null
}

// Get elemental relationship type
function getElementalRelationship(element1, element2) {
  if (!element1 || !element2 || element1 === element2) return null

  const pair = [element1, element2].sort().join('-')

  // Check friendly
  if (pair === 'Air-Fire' || pair === 'Earth-Water') {
    return 'friendly'
  }

  // Check challenging
  if (pair === 'Fire-Water' || pair === 'Air-Earth') {
    return 'challenging'
  }

  return 'neutral'
}

// Connection line colors
const relationshipColors = {
  friendly: { stroke: 'rgba(139, 92, 246, 0.4)', glow: 'rgba(139, 92, 246, 0.2)' },
  neutral: { stroke: 'rgba(148, 163, 184, 0.25)', glow: 'rgba(148, 163, 184, 0.1)' },
  challenging: { stroke: 'rgba(245, 158, 11, 0.35)', glow: 'rgba(245, 158, 11, 0.15)' },
  combination: { stroke: 'rgba(6, 182, 212, 0.5)', glow: 'rgba(6, 182, 212, 0.25)' }
}

export default function CardConnections({ cards, cardPositions, allRevealed }) {
  const [connections, setConnections] = useState([])
  const [visible, setVisible] = useState(false)
  const svgRef = useRef(null)

  // Calculate connections when all cards are revealed
  useEffect(() => {
    if (!allRevealed || !cards || cards.length < 2 || !cardPositions || cardPositions.length === 0) {
      setConnections([])
      setVisible(false)
      return
    }

    // Small delay before showing connections for visual effect
    const timer = setTimeout(() => {
      const newConnections = []

      // Find notable card combinations
      const combinations = findCombinations(cards)
      combinations.forEach(combo => {
        const indices = combo.cards.map(name =>
          cards.findIndex(c => c.name === name)
        ).filter(i => i !== -1)

        if (indices.length === 2) {
          newConnections.push({
            from: indices[0],
            to: indices[1],
            type: 'combination',
            meaning: combo.meaning
          })
        }
      })

      // Find elemental relationships (only if we don't have too many connections already)
      if (newConnections.length < 3) {
        for (let i = 0; i < cards.length; i++) {
          for (let j = i + 1; j < cards.length; j++) {
            const elem1 = getCardElement(cards[i])
            const elem2 = getCardElement(cards[j])
            const relationship = getElementalRelationship(elem1, elem2)

            // Only show friendly and challenging relationships
            if (relationship === 'friendly' || relationship === 'challenging') {
              // Check if this connection already exists as a combination
              const exists = newConnections.some(
                c => (c.from === i && c.to === j) || (c.from === j && c.to === i)
              )

              if (!exists && newConnections.length < 4) {
                newConnections.push({
                  from: i,
                  to: j,
                  type: relationship,
                  elements: [elem1, elem2]
                })
              }
            }
          }
        }
      }

      setConnections(newConnections)
      setVisible(true)
    }, 800)

    return () => clearTimeout(timer)
  }, [allRevealed, cards, cardPositions])

  if (!visible || connections.length === 0 || !cardPositions || cardPositions.length === 0) {
    return null
  }

  // Get SVG viewport dimensions
  const positions = cardPositions.filter(p => p)
  if (positions.length === 0) return null

  const minX = Math.min(...positions.map(p => p.x)) - 50
  const maxX = Math.max(...positions.map(p => p.x + p.width)) + 50
  const minY = Math.min(...positions.map(p => p.y)) - 50
  const maxY = Math.max(...positions.map(p => p.y + p.height)) + 50

  return (
    <svg
      ref={svgRef}
      className="absolute inset-0 pointer-events-none z-0"
      style={{
        left: minX,
        top: minY,
        width: maxX - minX,
        height: maxY - minY,
        overflow: 'visible'
      }}
    >
      <defs>
        {/* Gradient definitions for each relationship type */}
        {Object.entries(relationshipColors).map(([type, colors]) => (
          <linearGradient key={type} id={`gradient-${type}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={colors.stroke} stopOpacity="0" />
            <stop offset="20%" stopColor={colors.stroke} stopOpacity="1" />
            <stop offset="80%" stopColor={colors.stroke} stopOpacity="1" />
            <stop offset="100%" stopColor={colors.stroke} stopOpacity="0" />
          </linearGradient>
        ))}
      </defs>

      {connections.map((conn, idx) => {
        const fromPos = cardPositions[conn.from]
        const toPos = cardPositions[conn.to]

        if (!fromPos || !toPos) return null

        // Calculate center points of cards
        const fromX = fromPos.x + fromPos.width / 2 - minX
        const fromY = fromPos.y + fromPos.height / 2 - minY
        const toX = toPos.x + toPos.width / 2 - minX
        const toY = toPos.y + toPos.height / 2 - minY

        // Calculate control point for curved line
        const midX = (fromX + toX) / 2
        const midY = (fromY + toY) / 2
        const dx = toX - fromX
        const dy = toY - fromY
        const dist = Math.sqrt(dx * dx + dy * dy)

        // Perpendicular offset for curve
        const curveOffset = Math.min(dist * 0.2, 40)
        const perpX = -dy / dist * curveOffset
        const perpY = dx / dist * curveOffset

        const ctrlX = midX + perpX
        const ctrlY = midY + perpY

        const colors = relationshipColors[conn.type]
        const path = `M ${fromX} ${fromY} Q ${ctrlX} ${ctrlY} ${toX} ${toY}`

        return (
          <g key={idx} className="connection-group" style={{ opacity: 0, animation: `fade-in 0.6s ease ${idx * 0.15}s forwards` }}>
            {/* Glow layer */}
            <path
              d={path}
              fill="none"
              stroke={colors.glow}
              strokeWidth="6"
              className="card-connection-glow"
            />
            {/* Main line */}
            <path
              d={path}
              fill="none"
              stroke={`url(#gradient-${conn.type})`}
              strokeWidth="1.5"
              className="card-connection-line"
            />
          </g>
        )
      })}

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `}</style>
    </svg>
  )
}
