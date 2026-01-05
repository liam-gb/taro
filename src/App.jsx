import { useState, useEffect, useRef, useMemo } from 'react'
import Card3D from './components/Card3D'
import Button from './components/Button'
import CardSlot from './components/CardSlot'
import KeywordList from './components/KeywordList'
import CardConnections from './components/CardConnections'
import TaroLogo from './components/TaroLogo'
import { FULL_DECK, MAJOR_ARCANA, SPREADS } from './data'
import { generateReadingPrompt } from './utils/generatePrompt'
import { calculateReadingEnergy, getAtmosphereStyles } from './utils/cardEnergy'
import useWindowSize from './hooks/useWindowSize'
import {
  CARD_DEAL_DELAY_MS,
  COPY_FEEDBACK_TIMEOUT_MS,
  REVERSAL_PROBABILITY,
  HOVER_PREVIEW_COUNT,
  MAX_SELECTABLE_CARDS,
  CELTIC_CROSS
} from './constants'

// Aurora Background Component - Responds to reading energy
const AuroraBackground = ({ energy = 0 }) => {
  // Shift colors based on energy: negative = cooler, positive = warmer
  const hueShift = energy * 20 // ±20 degrees
  const saturationMod = 1 + (energy * 0.2) // 0.8 to 1.2
  const opacityMod = 0.25 + Math.abs(energy) * 0.1 // More intense at extremes

  return (
    <div className="aurora-bg" style={{ transition: 'all 2s ease-out' }}>
      {/* Primary orb - shifts with energy */}
      <div
        className="aurora-orb aurora-orb-1"
        style={{
          filter: `hue-rotate(${hueShift}deg) saturate(${saturationMod})`,
          opacity: opacityMod,
          transition: 'all 2s ease-out'
        }}
      />
      {/* Secondary orb - inverse shift for contrast */}
      <div
        className="aurora-orb aurora-orb-2"
        style={{
          filter: `hue-rotate(${-hueShift * 0.5}deg) saturate(${saturationMod})`,
          opacity: opacityMod * 0.8,
          transition: 'all 2s ease-out'
        }}
      />
      {/* Subtle noise texture overlay */}
      <div className="aurora-noise" />
    </div>
  )
}

// Cursor Spotlight Component - follows mouse with mystical glow
const CursorSpotlight = () => {
  const [position, setPosition] = useState({ x: -500, y: -500 })
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const handleMouseMove = (e) => {
      setPosition({ x: e.clientX, y: e.clientY })
      if (!isVisible) setIsVisible(true)
    }

    const handleMouseLeave = () => {
      setIsVisible(false)
    }

    window.addEventListener('mousemove', handleMouseMove)
    document.body.addEventListener('mouseleave', handleMouseLeave)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      document.body.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [isVisible])

  return (
    <>
      <div
        className="cursor-spotlight"
        style={{
          left: position.x,
          top: position.y,
          opacity: isVisible ? 1 : 0
        }}
      />
      <div
        className="cursor-spotlight-inner"
        style={{
          left: position.x,
          top: position.y,
          opacity: isVisible ? 1 : 0
        }}
      />
    </>
  )
}

// Glass Toggle Component
const Toggle = ({ label, hint, checked, onChange }) => (
  <div className="space-y-1">
    <label className="flex items-center justify-between cursor-pointer group">
      <span className="text-slate-400/90 text-sm font-light tracking-wide group-hover:text-slate-300 transition-colors duration-300">
        {label}
      </span>
      <div
        onClick={onChange}
        className={`w-11 h-6 rounded-full transition-all duration-300 relative ${
          checked ? 'toggle-glass-active' : 'toggle-glass'
        }`}
      >
        <div className={`toggle-knob absolute top-1 w-4 h-4 rounded-full transition-all duration-300 ${
          checked ? 'left-6' : 'left-1'
        }`} />
      </div>
    </label>
    <p className="text-xs text-slate-600/80 font-light">{hint}</p>
  </div>
)

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export default function App() {
  const [phase, setPhase] = useState('welcome')
  const [question, setQuestion] = useState('')
  const [spread, setSpread] = useState('threeCard')
  const [deck, setDeck] = useState([])
  const [drawn, setDrawn] = useState([])
  const [revealed, setRevealed] = useState([])
  const [copied, setCopied] = useState(false)
  const [dealingIndex, setDealingIndex] = useState(-1)
  const [selectedCards, setSelectedCards] = useState([])
  const [raisedCenterCard, setRaisedCenterCard] = useState(1)
  const [hoveredCelticCard, setHoveredCelticCard] = useState(null)

  // Deck settings
  const [majorOnly, setMajorOnly] = useState(false)
  const [useReversals, setUseReversals] = useState(true)
  const [showSettings, setShowSettings] = useState(false)

  // Shuffle animation state
  const [isShuffling, setIsShuffling] = useState(false)
  const [shuffleStep, setShuffleStep] = useState(0)
  const [shuffleInteraction, setShuffleInteraction] = useState({ x: 0, y: 0 })
  const [shuffleFadeOut, setShuffleFadeOut] = useState(false)
  const [selectFadeIn, setSelectFadeIn] = useState(false)
  const shuffleContainerRef = useRef(null)

  // Card positions for reading layout (used for connections)
  const cardRefs = useRef([])
  const [cardPositions, setCardPositions] = useState([])
  const readingContainerRef = useRef(null)
  const celticContainerRef = useRef(null)

  // Responsive scaling for Celtic Cross
  const { width: windowWidth } = useWindowSize()
  const celticPadding = 32
  const celticScale = Math.min(1, (windowWidth - celticPadding) / CELTIC_CROSS.width)
  const useMobileCeltic = windowWidth < 640
  const isCeltic = spread === 'celtic'

  // Computed state - must be defined before useEffects that reference it
  const allRevealed = drawn.length > 0 && revealed.length === drawn.length

  // Dynamic atmosphere based on card energy
  const readingEnergy = useMemo(() => {
    if (phase !== 'reading' || revealed.length === 0) return 0
    const revealedCards = revealed.map(i => drawn[i]).filter(Boolean)
    return calculateReadingEnergy(revealedCards)
  }, [phase, revealed, drawn])

  const atmosphereStyles = useMemo(() =>
    getAtmosphereStyles(readingEnergy),
    [readingEnergy]
  )

  // Update card positions when cards are revealed
  useEffect(() => {
    if (phase === 'reading' && allRevealed && cardRefs.current.length > 0) {
      const isCelticDesktop = isCeltic && !useMobileCeltic
      const containerRef = isCelticDesktop ? celticContainerRef : readingContainerRef
      const containerRect = containerRef.current?.getBoundingClientRect()
      if (!containerRect) return

      const positions = cardRefs.current.map(ref => {
        if (!ref) return null
        const rect = ref.getBoundingClientRect()
        return {
          x: rect.left - containerRect.left,
          y: rect.top - containerRect.top,
          width: rect.width,
          height: rect.height
        }
      })
      setCardPositions(positions)
    }
  }, [phase, allRevealed, drawn.length, isCeltic, useMobileCeltic])

  const shuffleDeck = () => {
    const baseDeck = majorOnly ? MAJOR_ARCANA : FULL_DECK
    const d = shuffle(baseDeck).map(c => ({
      ...c,
      reversed: useReversals ? Math.random() < REVERSAL_PROBABILITY : false
    }))
    setDeck(d)
    return d
  }

  useEffect(() => { shuffleDeck() }, [majorOnly, useReversals])

  const spreadData = SPREADS[spread]
  const hoverCards = deck.slice(0, HOVER_PREVIEW_COUNT)

  // Shuffle animation - creates a visual shuffling experience
  const startShuffleAnimation = () => {
    setIsShuffling(true)
    setShuffleStep(0)
    setShuffleInteraction({ x: 0, y: 0 })
    setShuffleFadeOut(false)
    setSelectFadeIn(false)
    setPhase('shuffle')

    // Start with intro animation (step 0 -> 1)
    setTimeout(() => {
      setShuffleStep(1)

      // Animate through shuffle steps
      const steps = [2, 3, 4, 5]
      let stepIndex = 0

      const animateStep = () => {
        if (stepIndex < steps.length) {
          setShuffleStep(steps[stepIndex])
          // Actually shuffle the deck at each step for randomness
          if (stepIndex === 1) shuffleDeck()
          stepIndex++
          setTimeout(animateStep, 500)
        } else {
          // Final shuffle and smooth transition to select
          shuffleDeck()
          // Start fade out animation
          setShuffleStep(6) // Gather cards tightly
          setTimeout(() => {
            setShuffleFadeOut(true)
            setTimeout(() => {
              setIsShuffling(false)
              setShuffleStep(0)
              setPhase('select')
              // Trigger fade in for select phase
              requestAnimationFrame(() => {
                setSelectFadeIn(true)
              })
            }, 500)
          }, 400)
        }
      }

      setTimeout(animateStep, 600)
    }, 100)
  }

  // Handle shuffle interaction (mouse/touch)
  const handleShuffleInteraction = (e) => {
    if (!shuffleContainerRef.current || shuffleStep === 0) return
    const rect = shuffleContainerRef.current.getBoundingClientRect()
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    const x = ((clientX - rect.left) / rect.width - 0.5) * 2 // -1 to 1
    const y = ((clientY - rect.top) / rect.height - 0.5) * 2 // -1 to 1
    setShuffleInteraction({ x, y })
  }

  const handleShuffleTap = () => {
    // On tap/click, add a random shuffle impulse
    setShuffleInteraction({
      x: (Math.random() - 0.5) * 2,
      y: (Math.random() - 0.5) * 2
    })
    // Reset after a moment
    setTimeout(() => setShuffleInteraction({ x: 0, y: 0 }), 300)
  }

  const dealCards = (cards) => {
    setDrawn(cards)
    setDealingIndex(-1)
    cards.forEach((_, i) => {
      setTimeout(() => setDealingIndex(i), i * CARD_DEAL_DELAY_MS)
    })
  }

  const selectCard = (index) => {
    if (selectedCards.includes(index)) return
    const newSelected = [...selectedCards, index]
    setSelectedCards(newSelected)
    if (newSelected.length === spreadData.positions.length) {
      const cards = newSelected.map(i => deck[i])
      setDeck(deck.filter((_, i) => !newSelected.includes(i)))
      setRevealed([])
      setPhase('reading')
      dealCards(cards)
      setSelectedCards([])
    }
  }

  const drawAllCards = () => {
    const needed = spreadData.positions.length - selectedCards.length
    const available = deck
      .slice(0, Math.min(MAX_SELECTABLE_CARDS, deck.length))
      .map((_, i) => i)
      .filter(i => !selectedCards.includes(i))
    const shuffled = shuffle(available)
    const toSelect = shuffled.slice(0, needed)
    const allSelected = [...selectedCards, ...toSelect]
    const cards = allSelected.map(i => deck[i])
    setDeck(deck.filter((_, i) => !allSelected.includes(i)))
    setRevealed([])
    setPhase('reading')
    dealCards(cards)
    setSelectedCards([])
  }

  const reset = () => {
    setPhase('welcome')
    setQuestion('')
    setDrawn([])
    setRevealed([])
    setCopied(false)
    setDealingIndex(-1)
    setSelectedCards([])
    setRaisedCenterCard(1)
    setHoveredCelticCard(null)
    setCardPositions([])
    setShuffleFadeOut(false)
    setSelectFadeIn(false)
    cardRefs.current = []
    shuffleDeck()
  }

  const copy = () => {
    navigator.clipboard.writeText(generateReadingPrompt(drawn, spreadData, question))
    setCopied(true)
    setTimeout(() => setCopied(false), COPY_FEEDBACK_TIMEOUT_MS)
  }

  const revealCard = (i) => setRevealed([...revealed, i])

  return (
    <div
      className="min-h-screen text-slate-200 relative transition-all duration-1000"
      style={atmosphereStyles}
    >
      {/* Animated Aurora Background */}
      <AuroraBackground energy={readingEnergy} />
      {/* Cursor Spotlight Effect */}
      <CursorSpotlight />

      {/* Header - Bold, edge-breaking on mobile */}
      <div className="pt-12 pb-6 md:pt-16 md:pb-8 relative overflow-visible">
        {/* Decorative gold arc - breaks out of container */}
        <div
          className="absolute -left-8 top-0 w-32 h-32 md:w-48 md:h-48 opacity-20 entrance-stagger entrance-stagger-1"
          style={{
            background: 'radial-gradient(ellipse at center, rgba(201,168,108,0.4) 0%, transparent 70%)',
            filter: 'blur(30px)',
            transform: 'rotate(-15deg)'
          }}
        />
        <div className="max-w-7xl mx-auto px-6 md:px-8">
          <div className="text-center md:text-left">
            {/* SVG Runic Logo */}
            <div className="entrance-stagger entrance-stagger-1">
              <TaroLogo size="large" className="mx-auto md:mx-0 opacity-90" />
            </div>
            {/* Decorative line - extends edge to edge on mobile */}
            <div className="mt-4 h-px entrance-stagger entrance-stagger-2 -mx-6 md:mx-0 md:w-32">
              <div className="h-full bg-gradient-to-r from-transparent via-mystic-gold/50 to-transparent md:from-mystic-gold/50 md:to-transparent" />
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 md:px-8 pb-16 relative">
        {/* Welcome Phase - Mobile-first bold composition */}
        {phase === 'welcome' && (
          <div className="relative">
            {/* Card Preview - Overlaps into header, breaks edges on mobile */}
            <div className="relative -mt-4 mb-8 md:mb-12 entrance-stagger entrance-stagger-3">
              {/* Cards fan - extends beyond container on mobile */}
              <div className="flex justify-center -mx-6 md:mx-0 overflow-visible">
                <div className="flex items-end gap-0" style={{ transform: 'perspective(800px)' }}>
                  {[0,1,2,3,4].map(i => {
                    const isCenter = i === 2
                    const offset = i - 2
                    return (
                      <div
                        key={i}
                        className={`${i === 0 || i === 4 ? 'hidden sm:block' : ''} transition-all duration-700`}
                        style={{
                          transform: `
                            rotate(${offset * 8}deg)
                            translateY(${Math.abs(offset) * 12}px)
                            translateX(${offset * -8}px)
                            ${isCenter ? 'scale(1.1)' : 'scale(0.95)'}
                          `,
                          zIndex: isCenter ? 10 : 5 - Math.abs(offset),
                          marginLeft: i > 0 ? '-24px' : '0',
                          filter: isCenter ? 'none' : 'brightness(0.85)',
                        }}
                      >
                        <Card3D card={hoverCards[i]} enableHover hoverCard={hoverCards[i]} />
                      </div>
                    )
                  })}
                </div>
              </div>
              {/* Hint text */}
              <p className="text-slate-600/70 text-xs font-light tracking-wider text-center mt-6 uppercase">
                Tap to glimpse
              </p>
            </div>

            {/* Controls Section - Stacked on mobile, cleaner hierarchy */}
            <div className="space-y-6 md:space-y-8 max-w-sm mx-auto">
              {/* Spread Selection - Horizontal scroll on mobile */}
              <div className="entrance-stagger entrance-stagger-4">
                <p className="text-slate-500/60 text-xs font-light tracking-widest uppercase text-center mb-3">
                  Choose your spread
                </p>
                <div className="flex gap-2 justify-center flex-wrap">
                  {Object.entries(SPREADS).map(([k, s]) => (
                    <button
                      key={k}
                      onClick={() => setSpread(k)}
                      className={`group px-4 py-2.5 rounded-full transition-all duration-300 ${
                        spread === k
                          ? 'pill-glass-active scale-105'
                          : 'pill-glass hover:border-white/20'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span className={`text-sm font-light tracking-wide ${
                          spread === k ? 'text-mystic-gold' : 'text-slate-400 group-hover:text-slate-300'
                        }`}>
                          {s.name}
                        </span>
                        <span className={`text-xs px-1.5 py-0.5 rounded-full transition-colors duration-300 ${
                          spread === k
                            ? 'bg-mystic-gold/30 text-mystic-gold'
                            : 'bg-white/5 text-slate-600 group-hover:text-slate-500'
                        }`}>
                          {s.positions.length}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Settings Toggle - More minimal */}
              <div className="text-center">
                <button
                  onClick={() => setShowSettings(!showSettings)}
                  className="text-slate-600 hover:text-slate-400 text-xs font-light tracking-widest uppercase transition-colors duration-300 inline-flex items-center gap-2"
                >
                  <span className={`transition-transform duration-300 text-mystic-gold/60 ${showSettings ? 'rotate-90' : ''}`}>
                    ›
                  </span>
                  <span>Options</span>
                </button>

                {/* Settings Panel */}
                {showSettings && (
                  <div className="glass rounded-2xl p-5 mt-4 space-y-4 animate-[reveal-up_0.3s_ease] text-left">
                    <Toggle
                      label="Major Arcana only"
                      hint="Use only the 22 Major Arcana cards"
                      checked={majorOnly}
                      onChange={() => setMajorOnly(!majorOnly)}
                    />
                    <div className="divider-glass" />
                    <Toggle
                      label="Reversed cards"
                      hint="Allow cards to appear reversed"
                      checked={useReversals}
                      onChange={() => setUseReversals(!useReversals)}
                    />
                  </div>
                )}
              </div>

              {/* Begin Button - Hero CTA with stronger gold */}
              <div className="entrance-stagger entrance-stagger-5 pt-2">
                <Button onClick={() => setPhase('question')} className="w-full btn-hero">
                  Begin Reading
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Question Phase */}
        {phase === 'question' && (
          <div className="max-w-sm mx-auto text-center px-2">
            <p className="text-slate-300/80 text-lg font-light tracking-wide mb-6 entrance-stagger entrance-stagger-1">
              What guidance do you seek?
            </p>
            <textarea
              value={question}
              onChange={e => setQuestion(e.target.value)}
              placeholder="Your question (or leave blank for general guidance)..."
              rows={3}
              className="input-glass w-full rounded-2xl p-5 text-slate-200 resize-none mb-3 font-light tracking-wide text-center entrance-stagger entrance-stagger-2"
            />
            <p className="text-slate-600/60 text-xs font-light mb-8 entrance-stagger entrance-stagger-2">
              Open-ended questions yield richer insights
            </p>
            <div className="entrance-stagger entrance-stagger-3">
              <Button variant="secondary" onClick={startShuffleAnimation} className="w-full">
                Continue
              </Button>
            </div>
          </div>
        )}

        {/* Shuffle Phase */}
        {phase === 'shuffle' && (
          <div className={`text-center py-16 transition-all duration-500 ${shuffleFadeOut ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}`}>
            <div
              ref={shuffleContainerRef}
              className="relative h-64 flex items-center justify-center mb-8 cursor-pointer"
              onMouseMove={handleShuffleInteraction}
              onTouchMove={handleShuffleInteraction}
              onClick={handleShuffleTap}
              onTouchStart={handleShuffleTap}
            >
              {/* Animated deck during shuffle */}
              <div className="relative">
                {[...Array(7)].map((_, i) => {
                  // Create dynamic offsets based on shuffle step
                  const isEven = i % 2 === 0
                  const baseOffset = (i - 3) * 4
                  let xOffset = baseOffset
                  let yOffset = i * 2
                  let rotation = (i - 3) * 2
                  let scale = 1

                  // Add interaction influence
                  const interactX = shuffleInteraction.x * 15 * (i - 3) * 0.3
                  const interactY = shuffleInteraction.y * 10 * Math.abs(i - 3) * 0.2
                  const interactRot = shuffleInteraction.x * 5 * (i - 3) * 0.2

                  // Animate cards based on shuffle step
                  if (shuffleStep === 0) {
                    // Intro: cards scattered, then gather
                    xOffset = (i - 3) * 60
                    yOffset = (i % 2 === 0 ? -1 : 1) * 40 + Math.sin(i) * 20
                    rotation = (i - 3) * 25
                    scale = 0.85
                  } else if (shuffleStep === 1) {
                    // Gather together smoothly
                    xOffset = baseOffset
                    yOffset = i * 2
                    rotation = (i - 3) * 3
                  } else if (shuffleStep === 2) {
                    // Split deck
                    xOffset = isEven ? baseOffset - 50 : baseOffset + 50
                    yOffset = i * 2.5
                  } else if (shuffleStep === 3) {
                    // Riffle together
                    xOffset = baseOffset + Math.sin(i * 0.8) * 25
                    yOffset = i * 2 + (isEven ? -12 : 12)
                    rotation = (i - 3) * 4
                  } else if (shuffleStep === 4) {
                    // Fan out
                    rotation = (i - 3) * 15
                    xOffset = baseOffset + (i - 3) * 12
                    yOffset = Math.abs(i - 3) * -3
                  } else if (shuffleStep === 5) {
                    // Final gather with gentle wave
                    xOffset = baseOffset * 0.3
                    yOffset = i * 1.5 + Math.sin(i * 0.5) * 3
                    rotation = (i - 3) * 1
                  } else if (shuffleStep === 6) {
                    // Tight stack before transition
                    xOffset = 0
                    yOffset = i * 0.5
                    rotation = 0
                    scale = 0.95
                  }

                  return (
                    <div
                      key={i}
                      className="absolute transition-all duration-500 ease-out"
                      style={{
                        transform: `translateX(${xOffset + interactX}px) translateY(${yOffset + interactY}px) rotate(${rotation + interactRot}deg) scale(${scale})`,
                        zIndex: i,
                        transition: shuffleStep === 0 ? 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)' : 'all 0.5s ease-out'
                      }}
                    >
                      <Card3D size="small" />
                    </div>
                  )
                })}
              </div>
            </div>
            <p className="text-slate-400/80 font-light tracking-wider text-sm animate-pulse">
              {shuffleStep === 0 ? 'Gathering the cards...' : 'Shuffling the deck...'}
            </p>
            <p className="text-slate-600/60 text-xs font-light mt-2">
              tap or move to influence
            </p>
          </div>
        )}

        {/* Card Selection Phase */}
        {phase === 'select' && (
          <div className={`text-center transition-all duration-700 ease-out ${selectFadeIn ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
            {/* Progress indicator */}
            <div className="mb-6">
              <p className="text-slate-500/60 text-xs font-light tracking-widest uppercase mb-2">
                {selectedCards.length < spreadData.positions.length
                  ? spreadData.positions[selectedCards.length].name
                  : 'Complete'
                }
              </p>
              <p className="text-slate-300/90 font-light tracking-wide">
                <span className="text-mystic-gold text-lg">{selectedCards.length}</span>
                <span className="text-slate-600/60 mx-1 text-sm">/</span>
                <span className="text-slate-500/80 text-sm">{spreadData.positions.length}</span>
              </p>
            </div>

            {/* Breathing pulse indicator - larger on mobile */}
            <div className="flex justify-center mb-6">
              <div className="breathing-pulse w-4 h-4 rounded-full bg-mystic-gold/30" />
            </div>

            {/* Card Fan - extends to edges on mobile */}
            <div className="flex flex-wrap justify-center gap-0.5 md:gap-1 mb-8 -mx-6 md:mx-0 overflow-x-auto overflow-y-visible py-4">
              {deck.slice(0, Math.min(MAX_SELECTABLE_CARDS, deck.length)).map((card, i) => (
                <div
                  key={i}
                  onClick={() => selectCard(i)}
                  className={`transition-all duration-500 flex-shrink-0 ${
                    selectedCards.includes(i)
                      ? 'opacity-10 scale-75 pointer-events-none'
                      : 'cursor-pointer hover:z-10 active:scale-95'
                  }`}
                  style={{
                    transform: `rotate(${(i - 10) * 1.5}deg)`,
                    marginLeft: i > 0 ? '-18px' : '0'
                  }}
                >
                  <Card3D size="small" enableSlowReveal={!selectedCards.includes(i)} />
                </div>
              ))}
            </div>

            {/* Actions */}
            <div className="flex justify-center gap-6">
              <Button variant="text" onClick={reset} className="text-xs">
                Start Over
              </Button>
              <Button variant="text" onClick={drawAllCards} className="text-xs">
                Draw All
              </Button>
            </div>
          </div>
        )}

        {/* Reading Phase */}
        {phase === 'reading' && (
          <div>
            {/* Question Echo - Enhanced Display */}
            {question && (
              <div className="text-center mb-8 md:mb-12 px-4">
                <p className="text-slate-600/60 text-xs font-light tracking-widest uppercase mb-3">
                  Your question
                </p>
                <p className="question-echo inline-block text-slate-300/90 text-lg md:text-xl font-light italic tracking-wide max-w-xl">
                  {question}
                </p>
              </div>
            )}

            {/* Celtic Cross Layout */}
            {isCeltic && !useMobileCeltic ? (
              <div
                className="relative mx-auto mb-10"
                style={{
                  width: CELTIC_CROSS.width * celticScale,
                  height: CELTIC_CROSS.height * celticScale
                }}
              >
                <div
                  ref={celticContainerRef}
                  className="relative origin-top-left"
                  style={{
                    width: CELTIC_CROSS.width,
                    height: CELTIC_CROSS.height,
                    transform: `scale(${celticScale})`
                  }}
                >
                  {/* Card Connection Lines */}
                  <CardConnections
                    cards={drawn}
                    cardPositions={cardPositions}
                    allRevealed={allRevealed}
                  />

                  {drawn.map((card, i) => {
                    const isDealt = dealingIndex >= i
                    const pos = spreadData.layout[i]
                    const isOverlapping = i < 2
                    const isTopCard = isOverlapping && i === raisedCenterCard
                    const canSwap = isOverlapping && revealed.includes(0) && revealed.includes(1)
                    const isHovered = hoveredCelticCard === i

                    // Z-index logic: hovered cards go on top, then overlapping logic
                    let zIndex = 1
                    if (isHovered) {
                      zIndex = 200 // Above everything including tooltips
                    } else if (isOverlapping) {
                      zIndex = isTopCard ? 10 : 5
                    }

                    const handleClick = () => {
                      if (!revealed.includes(i) && isDealt) {
                        revealCard(i)
                      } else if (canSwap && isTopCard) {
                        setRaisedCenterCard(raisedCenterCard === 1 ? 0 : 1)
                      }
                    }

                    return (
                      <div
                        key={card.id}
                        ref={el => cardRefs.current[i] = el}
                        className={`absolute transition-all duration-500 ${isDealt ? 'opacity-100' : 'opacity-0 scale-75'} ${canSwap && isTopCard ? 'cursor-pointer' : ''}`}
                        style={{
                          left: CELTIC_CROSS.baseX + pos.x * CELTIC_CROSS.spacing,
                          top: CELTIC_CROSS.baseY + pos.y * CELTIC_CROSS.spacing,
                          transform: `rotate(${pos.rotate}deg)`,
                          zIndex
                        }}
                        onClick={handleClick}
                        onMouseEnter={() => setHoveredCelticCard(i)}
                        onMouseLeave={() => setHoveredCelticCard(null)}
                      >
                        {canSwap && isTopCard && i === 0 && (
                          <div
                            className="absolute -bottom-7 left-1/2 text-xs text-amber-400/60 whitespace-nowrap font-light tracking-wide pointer-events-none"
                            style={{ transform: 'translateX(-50%)' }}
                          >
                            tap to swap
                          </div>
                        )}
                        <CardSlot
                          card={card}
                          position={spreadData.positions[i]}
                          isDealt={isDealt}
                          isRevealed={revealed.includes(i)}
                          onReveal={() => {}}
                          size="small"
                          variant="celtic"
                          isMobile={celticScale < 1}
                          hideInlineLabel={true}
                        />
                      </div>
                    )
                  })}
                </div>
              </div>
            ) : (
              /* Standard Card Layout */
              <div
                ref={readingContainerRef}
                className={`relative flex flex-wrap justify-center mb-8 md:mb-10 ${isCeltic ? 'gap-2' : 'gap-4 md:gap-8'}`}
              >
                {/* Card Connection Lines */}
                <CardConnections
                  cards={drawn}
                  cardPositions={cardPositions}
                  allRevealed={allRevealed}
                />

                {drawn.map((card, i) => {
                  const isDealt = dealingIndex >= i
                  const cardSize = spread === 'single' ? 'large' : (isCeltic ? 'small' : 'normal')
                  return (
                    <div
                      key={card.id}
                      ref={el => cardRefs.current[i] = el}
                      className={`text-center relative transition-all duration-700 ${isDealt ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-12'}`}
                    >
                      <CardSlot
                        card={card}
                        position={spreadData.positions[i]}
                        isDealt={isDealt}
                        isRevealed={revealed.includes(i)}
                        onReveal={() => revealCard(i)}
                        size={cardSize}
                        variant="standard"
                        showKeywords={!isCeltic}
                        hideInlineLabel={isCeltic}
                      />
                    </div>
                  )
                })}
              </div>
            )}

            {/* Reveal Prompt */}
            {dealingIndex >= drawn.length - 1 && !allRevealed && (
              <div className="text-center space-y-4">
                <p className="text-slate-500/70 font-light tracking-wide animate-pulse">
                  Click each card to reveal
                </p>
                <Button
                  variant="text"
                  onClick={() => setRevealed(drawn.map((_, i) => i))}
                  className="text-sm"
                >
                  Reveal All
                </Button>
              </div>
            )}

            {/* Reading Summary */}
            {allRevealed && (
              <div className="mt-14 max-w-2xl mx-auto">
                <div className="summary-card rounded-2xl p-6 md:p-8 animated-border">
                  {/* Header */}
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-gradient-to-r from-amber-500/40 to-transparent" />
                    <h3 className="text-slate-400/90 text-sm font-light uppercase tracking-[0.2em]">
                      Reading Summary
                    </h3>
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-700/50 to-transparent" />
                  </div>

                  {/* Card List */}
                  <div className="space-y-4">
                    {drawn.map((card, i) => (
                      <div key={card.id} className="flex items-start gap-4">
                        <span className="text-amber-400/80 font-light min-w-[140px] shrink-0 tracking-wide">
                          {spreadData.positions[i].name}
                        </span>
                        <div>
                          <span className="text-slate-200/90 font-light tracking-wide">
                            {card.name}
                            {card.reversed && (
                              <span className="text-amber-400/80 ml-2 text-sm">(Reversed)</span>
                            )}
                          </span>
                          <div className="mt-1">
                            <KeywordList keywords={card.keywords} />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Divider */}
                  <div className="divider-glass my-6" />

                  {/* Copy Button */}
                  <Button onClick={copy} className="w-full text-sm">
                    {copied ? 'Copied to clipboard' : 'Copy for Claude or ChatGPT'}
                  </Button>
                </div>

                {/* New Reading Button */}
                <div className="text-center mt-10">
                  <Button variant="text" onClick={reset}>
                    New Reading
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
