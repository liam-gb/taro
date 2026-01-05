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

// Connection line colors - warm for tension, cool for support
const relationshipColors = {
  // Cool colors for supporting/friendly connections
  friendly: {
    stroke: 'rgba(56, 189, 248, 0.6)',      // Sky blue
    glow: 'rgba(56, 189, 248, 0.25)',
    accent: 'rgba(139, 92, 246, 0.5)'       // Purple accent
  },
  neutral: {
    stroke: 'rgba(148, 163, 184, 0.25)',
    glow: 'rgba(148, 163, 184, 0.1)',
    accent: 'rgba(148, 163, 184, 0.2)'
  },
  // Warm colors for challenging/tension connections
  challenging: {
    stroke: 'rgba(251, 146, 60, 0.6)',      // Orange
    glow: 'rgba(239, 68, 68, 0.3)',         // Red glow
    accent: 'rgba(245, 158, 11, 0.5)'       // Amber accent
  },
  // Mystical cyan/violet for special combinations
  combination: {
    stroke: 'rgba(192, 132, 252, 0.7)',     // Violet
    glow: 'rgba(6, 182, 212, 0.35)',        // Cyan glow
    accent: 'rgba(236, 72, 153, 0.5)'       // Pink accent
  }
}

// Get human-readable explanation for a connection
function getConnectionExplanation(conn, cards) {
  const fromCard = cards[conn.from]?.name || 'Unknown'
  const toCard = cards[conn.to]?.name || 'Unknown'

  if (conn.type === 'combination' && conn.meaning) {
    return conn.meaning
  }

  if (conn.elements) {
    const [elem1, elem2] = conn.elements
    if (conn.type === 'friendly') {
      return `${elem1} & ${elem2} complement each other, strengthening their energies`
    }
    if (conn.type === 'challenging') {
      return `${elem1} & ${elem2} create tension that demands resolution`
    }
  }

  return `Connection between ${fromCard} and ${toCard}`
}

export default function CardConnections({ cards, cardPositions, allRevealed }) {
  const [connections, setConnections] = useState([])
  const [visible, setVisible] = useState(false)
  const [hoveredConnection, setHoveredConnection] = useState(null)
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 })
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
      const allConnections = []

      // Find notable card combinations (highest priority)
      const combinations = findCombinations(cards)
      combinations.forEach(combo => {
        const indices = combo.cards.map(name =>
          cards.findIndex(c => c.name === name)
        ).filter(i => i !== -1)

        if (indices.length === 2) {
          allConnections.push({
            from: indices[0],
            to: indices[1],
            type: 'combination',
            meaning: combo.meaning,
            priority: 100 // Highest priority for symbolic combinations
          })
        }
      })

      // Find elemental relationships between all card pairs
      for (let i = 0; i < cards.length; i++) {
        for (let j = i + 1; j < cards.length; j++) {
          const elem1 = getCardElement(cards[i])
          const elem2 = getCardElement(cards[j])
          const relationship = getElementalRelationship(elem1, elem2)

          // Only show friendly and challenging relationships
          if (relationship === 'friendly' || relationship === 'challenging') {
            // Check if this connection already exists as a combination
            const exists = allConnections.some(
              c => (c.from === i && c.to === j) || (c.from === j && c.to === i)
            )

            if (!exists) {
              // Priority based on relationship type and position adjacency
              // Challenging relationships are more notable (tension to address)
              // Adjacent cards (by position) have slightly higher priority
              const adjacencyBonus = Math.abs(i - j) === 1 ? 10 : 0
              const typePriority = relationship === 'challenging' ? 50 : 30

              allConnections.push({
                from: i,
                to: j,
                type: relationship,
                elements: [elem1, elem2],
                priority: typePriority + adjacencyBonus
              })
            }
          }
        }
      }

      // Sort by priority (highest first) and take top connections
      const sortedConnections = allConnections
        .sort((a, b) => b.priority - a.priority)
        .slice(0, 5) // Show up to 5 most important connections

      setConnections(sortedConnections)
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

  const handleConnectionHover = (conn, idx, e) => {
    setHoveredConnection(idx)
    const rect = svgRef.current?.getBoundingClientRect()
    if (rect) {
      setTooltipPos({
        x: e.clientX - rect.left + minX,
        y: e.clientY - rect.top + minY - 10
      })
    }
  }

  const handleConnectionMove = (e) => {
    const rect = svgRef.current?.getBoundingClientRect()
    if (rect) {
      setTooltipPos({
        x: e.clientX - rect.left + minX,
        y: e.clientY - rect.top + minY - 10
      })
    }
  }

  return (
    <>
      <svg
        ref={svgRef}
        className="absolute inset-0 z-0"
        style={{
          left: minX,
          top: minY,
          width: maxX - minX,
          height: maxY - minY,
          overflow: 'visible',
          pointerEvents: 'none'
        }}
      >
        <defs>
          {/* Mystical gradient definitions with color transitions */}
          {Object.entries(relationshipColors).map(([type, colors]) => (
            <linearGradient key={type} id={`gradient-${type}`} x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor={colors.stroke} stopOpacity="0" />
              <stop offset="15%" stopColor={colors.stroke} stopOpacity="0.8" />
              <stop offset="50%" stopColor={colors.accent} stopOpacity="1" />
              <stop offset="85%" stopColor={colors.stroke} stopOpacity="0.8" />
              <stop offset="100%" stopColor={colors.stroke} stopOpacity="0" />
            </linearGradient>
          ))}
          {/* Animated glow filter for mystical effect */}
          <filter id="mystical-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur1" />
            <feGaussianBlur stdDeviation="6" result="blur2" />
            <feMerge>
              <feMergeNode in="blur2" />
              <feMergeNode in="blur1" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
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

          // Calculate control points for a more loopy cubic bezier curve
          const midX = (fromX + toX) / 2
          const midY = (fromY + toY) / 2
          const dx = toX - fromX
          const dy = toY - fromY
          const dist = Math.sqrt(dx * dx + dy * dy)

          // Much larger perpendicular offset for more pronounced loopy curves
          // Alternate curve direction based on index for visual variety
          const curveDirection = idx % 2 === 0 ? 1 : -1
          const curveOffset = Math.min(dist * 0.7, 120) * curveDirection
          const perpX = -dy / dist * curveOffset
          const perpY = dx / dist * curveOffset

          // Use cubic bezier with two control points for S-curve effect
          const ctrl1X = fromX + dx * 0.25 + perpX * 0.8
          const ctrl1Y = fromY + dy * 0.25 + perpY * 0.8
          const ctrl2X = fromX + dx * 0.75 + perpX
          const ctrl2Y = fromY + dy * 0.75 + perpY

          const colors = relationshipColors[conn.type]
          const path = `M ${fromX} ${fromY} C ${ctrl1X} ${ctrl1Y} ${ctrl2X} ${ctrl2Y} ${toX} ${toY}`
          const isHovered = hoveredConnection === idx

          return (
            <g key={idx} className="connection-group" style={{ opacity: 0, animation: `fade-in 0.6s ease ${idx * 0.15}s forwards` }}>
              {/* Outer glow layer - softest, widest */}
              <path
                d={path}
                fill="none"
                stroke={colors.glow}
                strokeWidth={isHovered ? "20" : "16"}
                strokeLinecap="round"
                style={{
                  filter: 'blur(4px)',
                  transition: 'stroke-width 0.3s ease',
                  opacity: 0.5
                }}
              />
              {/* Inner glow layer */}
              <path
                d={path}
                fill="none"
                stroke={colors.glow}
                strokeWidth={isHovered ? "10" : "8"}
                strokeLinecap="round"
                className="card-connection-glow"
                style={{
                  filter: 'url(#mystical-glow)',
                  transition: 'stroke-width 0.3s ease'
                }}
              />
              {/* Core energy line with gradient */}
              <path
                d={path}
                fill="none"
                stroke={`url(#gradient-${conn.type})`}
                strokeWidth={isHovered ? "3.5" : "2.5"}
                strokeLinecap="round"
                className="card-connection-line"
                style={{ transition: 'stroke-width 0.3s ease' }}
              />
              {/* Bright center highlight */}
              <path
                d={path}
                fill="none"
                stroke="rgba(255, 255, 255, 0.3)"
                strokeWidth={isHovered ? "1.5" : "1"}
                strokeLinecap="round"
                style={{
                  transition: 'stroke-width 0.3s ease',
                  opacity: isHovered ? 0.6 : 0.4
                }}
              />
              {/* Invisible wider path for easier hover targeting */}
              <path
                d={path}
                fill="none"
                stroke="transparent"
                strokeWidth="24"
                style={{ cursor: 'pointer', pointerEvents: 'stroke' }}
                onMouseEnter={(e) => handleConnectionHover(conn, idx, e)}
                onMouseMove={handleConnectionMove}
                onMouseLeave={() => setHoveredConnection(null)}
              />
            </g>
          )
        })}

        <style>{`
          @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
          }
          @keyframes energy-pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 0.8; }
          }
          .connection-group .card-connection-glow {
            animation: energy-pulse 3s ease-in-out infinite;
          }
          .connection-group:nth-child(2) .card-connection-glow {
            animation-delay: 0.5s;
          }
          .connection-group:nth-child(3) .card-connection-glow {
            animation-delay: 1s;
          }
          .connection-group:nth-child(4) .card-connection-glow {
            animation-delay: 1.5s;
          }
          .connection-group:nth-child(5) .card-connection-glow {
            animation-delay: 2s;
          }
        `}</style>
      </svg>

      {/* Connection tooltip */}
      {hoveredConnection !== null && connections[hoveredConnection] && (
        <div
          className="absolute z-50 pointer-events-none"
          style={{
            left: tooltipPos.x,
            top: tooltipPos.y,
            transform: 'translate(-50%, -100%)'
          }}
        >
          <div className="tooltip-glass px-4 py-2.5 rounded-xl text-xs whitespace-nowrap max-w-[280px]"
            style={{ animation: 'tooltip-fade-in 0.15s ease' }}>
            {/* Decorative top accent */}
            <div className="absolute -top-px left-4 right-4 h-px bg-gradient-to-r from-transparent via-amber-500/50 to-transparent" />

            <div className="text-slate-300/90 font-light text-center" style={{ whiteSpace: 'normal' }}>
              {getConnectionExplanation(connections[hoveredConnection], cards)}
            </div>

            {/* Arrow pointer */}
            <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 bg-[rgba(15,15,25,0.9)] border-r border-b border-white/10" />
          </div>
        </div>
      )}
    </>
  )
}
