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

const Toggle = ({ label, hint, checked, onChange }) => (
  <>
    <label className="flex items-center justify-between cursor-pointer group">
      <span className="text-slate-400 text-sm group-hover:text-slate-300">{label}</span>
      <div onClick={onChange} className={`w-10 h-6 rounded-full transition-colors relative ${checked ? 'bg-violet-600' : 'bg-slate-700'}`}>
        <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all ${checked ? 'left-5' : 'left-1'}`} />
      </div>
    </label>
    <p className="text-xs text-slate-600 -mt-1">{hint}</p>
  </>
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
  const [raisedCenterCard, setRaisedCenterCard] = useState(1) // Which overlapping card is on top (0 or 1)

  // Deck settings
  const [majorOnly, setMajorOnly] = useState(false)
  const [useReversals, setUseReversals] = useState(true)
  const [showSettings, setShowSettings] = useState(false)

  // Responsive scaling for Celtic Cross
  const { width: windowWidth } = useWindowSize()
  const celticPadding = 32 // 16px padding on each side
  const celticScale = Math.min(1, (windowWidth - celticPadding) / CELTIC_CROSS.width)
  const useMobileCeltic = windowWidth < 640 // Use simple layout on narrow screens

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
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-200">
      <div className="text-center py-6">
        <h1 className="text-xl tracking-[0.4em] text-slate-500 font-light">TAROT</h1>
      </div>

      <div className="max-w-7xl mx-auto px-4 pb-12">
        {phase === 'welcome' && (
          <div className="text-center">
            <p className="text-slate-600 text-sm mb-6 md:mb-8">Tap or hover to glimpse the cards</p>
            <div className="flex justify-center gap-2 md:gap-4 mb-8 md:mb-12 flex-wrap">
              {[0,1,2,3,4].map(i => (
                <div key={i} className={i >= 3 ? 'hidden md:block' : ''} style={{ transform: `rotate(${(i-2)*4}deg)` }}>
                  <Card3D card={hoverCards[i]} enableHover hoverCard={hoverCards[i]} />
                </div>
              ))}
            </div>
            <div className="space-y-6 max-w-md mx-auto">
              <div className="flex flex-wrap justify-center gap-3">
                {Object.entries(SPREADS).map(([k, s]) => (
                  <button key={k} onClick={() => setSpread(k)}
                    className={`group px-5 py-3 rounded-full transition-all ${
                      spread === k
                        ? 'bg-violet-600/20 ring-1 ring-violet-500/50 text-violet-300'
                        : 'bg-slate-900/40 hover:bg-slate-800/60 text-slate-400 hover:text-slate-300'
                    }`}>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">{s.name}</span>
                      <span className="flex gap-0.5">
                        {[...Array(Math.min(s.positions.length, 7))].map((_, i) => (
                          <span
                            key={i}
                            className={`w-1.5 h-1.5 rounded-full ${
                              spread === k ? 'bg-violet-400' : 'bg-slate-600 group-hover:bg-slate-500'
                            }`}
                          />
                        ))}
                        {s.positions.length > 7 && (
                          <span className={`text-xs ml-0.5 ${spread === k ? 'text-violet-400' : 'text-slate-600'}`}>+</span>
                        )}
                      </span>
                    </div>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setShowSettings(!showSettings)}
                className="text-slate-600 hover:text-slate-400 text-sm transition-colors"
              >
                {showSettings ? '▾ Hide options' : '▸ Deck options'}
              </button>

              {showSettings && (
                <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-800 space-y-3">
                  <Toggle label="Major Arcana only" hint="Use only the 22 Major Arcana cards" checked={majorOnly} onChange={() => setMajorOnly(!majorOnly)} />
                  <Toggle label="Reversed cards" hint="Allow cards to appear reversed (inverted meaning)" checked={useReversals} onChange={() => setUseReversals(!useReversals)} />
                </div>
              )}

              <Button onClick={() => setPhase('question')} className="w-full">Begin Reading</Button>
            </div>
          </div>
        )}

        {phase === 'question' && (
          <div className="max-w-md mx-auto text-center">
            <p className="text-slate-500 mb-6">What guidance do you seek?</p>
            <textarea value={question} onChange={e => setQuestion(e.target.value)} placeholder="Your question (or leave blank for general guidance)..." rows={3}
              className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-4 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-violet-500/50 resize-none mb-4" />
            <p className="text-slate-600 text-xs mb-6">Tip: Open-ended questions yield richer insights</p>
            <Button variant="secondary" onClick={() => { shuffleDeck(); setPhase('select') }} className="w-full">Continue</Button>
          </div>
        )}

        {phase === 'select' && (
          <div className="text-center">
            <p className="text-slate-400 mb-2">Choose your cards</p>
            <p className="text-slate-600 text-sm mb-6">
              {selectedCards.length} of {spreadData.positions.length} selected
              {selectedCards.length < spreadData.positions.length && (
                <span className="text-violet-400/70"> — {spreadData.positions[selectedCards.length].name}</span>
              )}
            </p>
            <div className="flex flex-wrap justify-center gap-1 md:gap-2 mb-8 max-w-4xl mx-auto">
              {deck.slice(0, Math.min(MAX_SELECTABLE_CARDS, deck.length)).map((card, i) => (
                <div
                  key={i}
                  onClick={() => selectCard(i)}
                  className={`transition-all duration-300 ${
                    selectedCards.includes(i)
                      ? 'opacity-20 scale-90 pointer-events-none'
                      : 'hover:scale-110 hover:-translate-y-3 cursor-pointer'
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
            <Button variant="text" onClick={reset} className="text-sm">Start Over</Button>
          </div>
        )}

        {phase === 'reading' && (
          <div>
            {question && <p className="text-center text-slate-600 mb-4 md:mb-8 italic text-base md:text-lg px-4">"{question}"</p>}

            {isCeltic && !useMobileCeltic ? (
              <div
                className="relative mx-auto mb-8"
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
                        // Swap which center card is on top
                        setRaisedCenterCard(raisedCenterCard === 1 ? 0 : 1)
                      }
                    }

                    return (
                      <div
                        key={card.id}
                        className={`absolute transition-all duration-300 ${isDealt ? 'opacity-100' : 'opacity-0 scale-75'} ${canSwap && isTopCard ? 'cursor-pointer' : ''}`}
                        style={{
                          left: CELTIC_CROSS.baseX + pos.x * CELTIC_CROSS.spacing,
                          top: CELTIC_CROSS.baseY + pos.y * CELTIC_CROSS.spacing,
                          transform: `rotate(${pos.rotate}deg)`,
                          zIndex: isOverlapping ? (isTopCard ? 2 : 1) : 1
                        }}
                        onClick={handleClick}
                      >
                        {/* Position label */}
                        <div
                          className="absolute -top-6 left-1/2 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-700 shadow-lg"
                          style={{
                            zIndex: 10,
                            transform: pos.rotate ? `translateX(-50%) rotate(-${pos.rotate}deg)` : 'translateX(-50%)'
                          }}
                        >
                          <span className="text-xs font-medium text-slate-300 whitespace-nowrap">
                            {spreadData.positions[i].name}
                          </span>
                        </div>
                        {/* Swap hint for top overlapping card */}
                        {canSwap && isTopCard && (
                          <div
                            className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-xs text-violet-400/70 whitespace-nowrap"
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
                          hideInlineLabel={i < 2}
                        />
                      </div>
                    )
                  })}
                </div>
              </div>
            ) : (
              <div className={`flex flex-wrap justify-center mb-6 md:mb-8 ${isCeltic ? 'gap-2' : 'gap-3 md:gap-6'}`}>
                {drawn.map((card, i) => {
                  const isDealt = dealingIndex >= i
                  const cardSize = spread === 'single' ? 'large' : (isCeltic ? 'small' : 'normal')
                  return (
                    <div
                      key={card.id}
                      className={`text-center relative transition-all duration-500 ${isDealt ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-8'}`}
                    >
                      {/* Position label for Celtic Cross mobile view */}
                      {isCeltic && (
                        <div className="absolute -top-5 left-1/2 -translate-x-1/2 px-2 py-0.5 rounded bg-slate-900/90 border border-slate-700 shadow-lg z-10">
                          <span className="text-xs font-medium text-slate-300 whitespace-nowrap">
                            {spreadData.positions[i].name}
                          </span>
                        </div>
                      )}
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

            {dealingIndex >= drawn.length - 1 && !allRevealed && (
              <div className="text-center space-y-3">
                <p className="text-slate-600 animate-pulse">Click each card to reveal</p>
                <Button
                  variant="text"
                  onClick={() => setRevealed(drawn.map((_, i) => i))}
                  className="text-sm"
                >
                  Reveal All
                </Button>
              </div>
            )}

            {allRevealed && (
              <div className="mt-12 max-w-2xl mx-auto">
                <div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
                  <h3 className="text-slate-400 text-sm font-medium mb-4 uppercase tracking-wider">Reading Summary</h3>
                  <div className="space-y-3">
                    {drawn.map((card, i) => (
                      <div key={card.id} className="flex items-start gap-3">
                        <span className="text-violet-400 font-medium min-w-[140px] shrink-0">{spreadData.positions[i].name}:</span>
                        <div>
                          <span className="text-slate-300">{card.name}{card.reversed && <span className="text-amber-500/80 ml-2">(Reversed)</span>}</span>
                          <KeywordList keywords={card.keywords} />
                        </div>
                      </div>
                    ))}
                  </div>
                  <Button onClick={copy} className="mt-6 w-full text-sm">{copied ? '✓ Copied!' : 'Copy for Claude or ChatGPT'}</Button>
                </div>
                <div className="text-center mt-8">
                  <Button variant="text" onClick={reset}>New Reading</Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
