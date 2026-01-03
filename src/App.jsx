import { useState, useEffect } from 'react'
import Card3D from './components/Card3D'
import Button from './components/Button'
import CardSlot from './components/CardSlot'
import KeywordList from './components/KeywordList'
import { FULL_DECK, MAJOR_ARCANA, SPREADS } from './data'
import { generateReadingPrompt } from './utils/generatePrompt'
import useWindowSize from './hooks/useWindowSize'
import {
  CARD_DEAL_DELAY_MS,
  COPY_FEEDBACK_TIMEOUT_MS,
  REVERSAL_PROBABILITY,
  HOVER_PREVIEW_COUNT,
  MAX_SELECTABLE_CARDS,
  CELTIC_CROSS
} from './constants'

// Aurora Background Component
const AuroraBackground = () => (
  <div className="aurora-bg">
    <div className="aurora-orb aurora-orb-1" />
    <div className="aurora-orb aurora-orb-2" />
    <div className="aurora-orb aurora-orb-3" />
    <div className="aurora-orb aurora-orb-4" />
  </div>
)

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

  // Deck settings
  const [majorOnly, setMajorOnly] = useState(false)
  const [useReversals, setUseReversals] = useState(true)
  const [showSettings, setShowSettings] = useState(false)

  // Responsive scaling for Celtic Cross
  const { width: windowWidth } = useWindowSize()
  const celticPadding = 32
  const celticScale = Math.min(1, (windowWidth - celticPadding) / CELTIC_CROSS.width)
  const useMobileCeltic = windowWidth < 640

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
  const allRevealed = drawn.length > 0 && revealed.length === drawn.length

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
    shuffleDeck()
  }

  const copy = () => {
    navigator.clipboard.writeText(generateReadingPrompt(drawn, spreadData, question))
    setCopied(true)
    setTimeout(() => setCopied(false), COPY_FEEDBACK_TIMEOUT_MS)
  }

  const isCeltic = spread === 'celtic'
  const revealCard = (i) => setRevealed([...revealed, i])

  return (
    <div className="min-h-screen text-slate-200 relative">
      {/* Animated Aurora Background */}
      <AuroraBackground />

      {/* Header */}
      <div className="text-center py-8 md:py-10 relative">
        <h1 className="text-mystical text-2xl md:text-3xl text-slate-300/90 font-light">
          TAROT
        </h1>
        <div className="mt-2 w-24 h-px mx-auto bg-gradient-to-r from-transparent via-violet-500/40 to-transparent" />
      </div>

      <div className="max-w-7xl mx-auto px-4 pb-16 relative">
        {/* Welcome Phase */}
        {phase === 'welcome' && (
          <div className="text-center">
            <p className="text-slate-500/80 text-sm font-light tracking-wide mb-8 md:mb-10">
              Tap or hover to glimpse the cards
            </p>

            {/* Card Preview */}
            <div className="flex justify-center gap-2 md:gap-4 mb-10 md:mb-14 flex-wrap">
              {[0,1,2,3,4].map(i => (
                <div
                  key={i}
                  className={`${i >= 3 ? 'hidden md:block' : ''} transition-transform duration-500`}
                  style={{ transform: `rotate(${(i-2)*4}deg)` }}
                >
                  <Card3D card={hoverCards[i]} enableHover hoverCard={hoverCards[i]} />
                </div>
              ))}
            </div>

            <div className="space-y-8 max-w-lg mx-auto">
              {/* Spread Selection Pills */}
              <div className="flex flex-wrap justify-center gap-3">
                {Object.entries(SPREADS).map(([k, s]) => (
                  <button
                    key={k}
                    onClick={() => setSpread(k)}
                    className={`group px-5 py-3 rounded-full transition-all duration-300 ${
                      spread === k
                        ? 'pill-glass-active'
                        : 'pill-glass hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className={`text-sm font-light tracking-wide ${
                        spread === k ? 'text-violet-300' : 'text-slate-400 group-hover:text-slate-300'
                      }`}>
                        {s.name}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded-full transition-colors duration-300 ${
                        spread === k
                          ? 'bg-violet-500/30 text-violet-300'
                          : 'bg-white/5 text-slate-500 group-hover:text-slate-400'
                      }`}>
                        {s.positions.length}
                      </span>
                    </div>
                  </button>
                ))}
              </div>

              {/* Settings Toggle */}
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="text-slate-600 hover:text-slate-400 text-sm font-light tracking-wide transition-colors duration-300 flex items-center gap-2 mx-auto"
              >
                <span className={`transition-transform duration-300 ${showSettings ? 'rotate-90' : ''}`}>
                  ›
                </span>
                <span>Deck options</span>
              </button>

              {/* Settings Panel */}
              {showSettings && (
                <div className="glass rounded-2xl p-5 space-y-4 animate-[reveal-up_0.3s_ease]">
                  <Toggle
                    label="Major Arcana only"
                    hint="Use only the 22 Major Arcana cards"
                    checked={majorOnly}
                    onChange={() => setMajorOnly(!majorOnly)}
                  />
                  <div className="divider-glass" />
                  <Toggle
                    label="Reversed cards"
                    hint="Allow cards to appear reversed (inverted meaning)"
                    checked={useReversals}
                    onChange={() => setUseReversals(!useReversals)}
                  />
                </div>
              )}

              {/* Begin Button */}
              <Button onClick={() => setPhase('question')} className="w-full">
                Begin Reading
              </Button>
            </div>
          </div>
        )}

        {/* Question Phase */}
        {phase === 'question' && (
          <div className="max-w-md mx-auto text-center">
            <p className="text-slate-400/80 text-lg font-light tracking-wide mb-8">
              What guidance do you seek?
            </p>
            <textarea
              value={question}
              onChange={e => setQuestion(e.target.value)}
              placeholder="Your question (or leave blank for general guidance)..."
              rows={3}
              className="input-glass w-full rounded-xl p-5 text-slate-200 resize-none mb-4 font-light tracking-wide"
            />
            <p className="text-slate-600/80 text-xs font-light mb-8">
              Tip: Open-ended questions yield richer insights
            </p>
            <Button variant="secondary" onClick={() => { shuffleDeck(); setPhase('select') }} className="w-full">
              Continue
            </Button>
          </div>
        )}

        {/* Card Selection Phase */}
        {phase === 'select' && (
          <div className="text-center">
            <p className="text-slate-300/90 font-light tracking-wide mb-2">Choose your cards</p>
            <p className="text-slate-500/80 text-sm font-light mb-8">
              <span className="text-violet-400/80">{selectedCards.length}</span>
              <span className="text-slate-600/60 mx-2">of</span>
              <span>{spreadData.positions.length}</span>
              {selectedCards.length < spreadData.positions.length && (
                <span className="text-violet-400/60 ml-3">— {spreadData.positions[selectedCards.length].name}</span>
              )}
            </p>

            {/* Card Fan */}
            <div className="flex flex-wrap justify-center gap-1 md:gap-2 mb-10 max-w-4xl mx-auto">
              {deck.slice(0, Math.min(MAX_SELECTABLE_CARDS, deck.length)).map((card, i) => (
                <div
                  key={i}
                  onClick={() => selectCard(i)}
                  className={`transition-all duration-500 ${
                    selectedCards.includes(i)
                      ? 'opacity-10 scale-75 pointer-events-none'
                      : 'hover:scale-110 hover:-translate-y-4 cursor-pointer hover:z-10'
                  }`}
                  style={{
                    transform: `rotate(${(i - 10) * 2}deg)`,
                    marginLeft: i > 0 ? '-20px' : '0'
                  }}
                >
                  <Card3D size="small" />
                </div>
              ))}
            </div>
            <div className="flex justify-center gap-6">
              <Button variant="text" onClick={reset} className="text-sm">
                Start Over
              </Button>
              <Button variant="text" onClick={drawAllCards} className="text-sm">
                Draw All Cards
              </Button>
            </div>
          </div>
        )}

        {/* Reading Phase */}
        {phase === 'reading' && (
          <div>
            {/* Question Display */}
            {question && (
              <p className="text-center text-slate-500/80 mb-6 md:mb-10 italic text-base md:text-lg font-light px-4">
                "{question}"
              </p>
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
                  className="relative origin-top-left"
                  style={{
                    width: CELTIC_CROSS.width,
                    height: CELTIC_CROSS.height,
                    transform: `scale(${celticScale})`
                  }}
                >
                  {drawn.map((card, i) => {
                    const isDealt = dealingIndex >= i
                    const pos = spreadData.layout[i]
                    const isOverlapping = i < 2
                    const isTopCard = isOverlapping && i === raisedCenterCard
                    const canSwap = isOverlapping && revealed.includes(0) && revealed.includes(1)

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
                        className={`absolute transition-all duration-500 ${isDealt ? 'opacity-100' : 'opacity-0 scale-75'} ${canSwap && isTopCard ? 'cursor-pointer' : ''}`}
                        style={{
                          left: CELTIC_CROSS.baseX + pos.x * CELTIC_CROSS.spacing,
                          top: CELTIC_CROSS.baseY + pos.y * CELTIC_CROSS.spacing,
                          transform: `rotate(${pos.rotate}deg)`,
                          zIndex: isOverlapping ? (isTopCard ? 2 : 1) : 1
                        }}
                        onClick={handleClick}
                      >
                        {canSwap && isTopCard && (
                          <div
                            className="absolute -bottom-7 left-1/2 -translate-x-1/2 text-xs text-violet-400/60 whitespace-nowrap font-light tracking-wide"
                            style={{ transform: pos.rotate ? `translateX(-50%) rotate(-${pos.rotate}deg)` : 'translateX(-50%)' }}
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
              <div className={`flex flex-wrap justify-center mb-8 md:mb-10 ${isCeltic ? 'gap-2' : 'gap-4 md:gap-8'}`}>
                {drawn.map((card, i) => {
                  const isDealt = dealingIndex >= i
                  const cardSize = spread === 'single' ? 'large' : (isCeltic ? 'small' : 'normal')
                  return (
                    <div
                      key={card.id}
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
                <div className="summary-card rounded-2xl p-6 md:p-8">
                  {/* Header */}
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-8 h-px bg-gradient-to-r from-violet-500/40 to-transparent" />
                    <h3 className="text-slate-400/90 text-sm font-light uppercase tracking-[0.2em]">
                      Reading Summary
                    </h3>
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-700/50 to-transparent" />
                  </div>

                  {/* Card List */}
                  <div className="space-y-4">
                    {drawn.map((card, i) => (
                      <div key={card.id} className="flex items-start gap-4">
                        <span className="text-violet-400/80 font-light min-w-[140px] shrink-0 tracking-wide">
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
