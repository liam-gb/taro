import { useState, useEffect } from 'react'
import Card3D from './components/Card3D'
import { FULL_DECK, MAJOR_ARCANA, SPREADS } from './data'
import { generateReadingPrompt } from './utils/generatePrompt'

const btn = 'py-4 rounded-lg transition-colors'
const btnPrimary = `${btn} bg-violet-900/30 hover:bg-violet-800/40 border border-violet-500/20 text-slate-300`
const btnSecondary = `${btn} bg-slate-800 hover:bg-slate-700 text-slate-300`

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

// Celtic Cross traditional layout positions (relative to center)
const celticLayout = [
  { x: 0, y: 0, rotate: 0 },      // 1: Present (center)
  { x: 0, y: 0, rotate: 90 },     // 2: Challenge (crossing)
  { x: -1, y: 0, rotate: 0 },     // 3: Past (left)
  { x: 1, y: 0, rotate: 0 },      // 4: Future (right)
  { x: 0, y: -1, rotate: 0 },     // 5: Above (crown)
  { x: 0, y: 1, rotate: 0 },      // 6: Below (foundation)
  { x: 2.2, y: 1.5, rotate: 0 },  // 7: Advice (staff bottom)
  { x: 2.2, y: 0.5, rotate: 0 },  // 8: External (staff)
  { x: 2.2, y: -0.5, rotate: 0 }, // 9: Hopes/Fears (staff)
  { x: 2.2, y: -1.5, rotate: 0 }, // 10: Outcome (staff top)
]

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
  const [hoveredPosition, setHoveredPosition] = useState(null)

  // Deck settings
  const [majorOnly, setMajorOnly] = useState(false)
  const [useReversals, setUseReversals] = useState(true)
  const [showSettings, setShowSettings] = useState(false)

  const shuffleDeck = () => {
    const baseDeck = majorOnly ? MAJOR_ARCANA : FULL_DECK
    const d = shuffle(baseDeck).map(c => ({
      ...c,
      reversed: useReversals ? Math.random() < 0.3 : false
    }))
    setDeck(d)
    return d
  }

  useEffect(() => { shuffleDeck() }, [majorOnly, useReversals])

  const spreadData = SPREADS[spread]
  const hoverCards = deck.slice(0, 5)
  const allRevealed = drawn.length > 0 && revealed.length === drawn.length

  // Staggered card dealing animation
  const dealCards = (cards) => {
    setDrawn(cards)
    setDealingIndex(-1)
    cards.forEach((_, i) => {
      setTimeout(() => setDealingIndex(i), i * 300)
    })
  }

  // User picks their own cards from the spread
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
    shuffleDeck()
  }

  const copy = () => {
    navigator.clipboard.writeText(generateReadingPrompt(drawn, spreadData, question))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

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
            <div className="space-y-4 max-w-sm mx-auto">
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(SPREADS).map(([k, s]) => (
                  <button key={k} onClick={() => setSpread(k)}
                    className={`p-4 rounded-lg transition-all text-left ${spread === k ? 'bg-slate-800 ring-1 ring-violet-500/40' : 'bg-slate-900/50 hover:bg-slate-800/50'}`}>
                    <div className="text-slate-300 text-sm">{s.name}</div>
                    <div className="text-xs text-slate-600 mt-1">{s.positions.length} card{s.positions.length > 1 ? 's' : ''}</div>
                  </button>
                ))}
              </div>

              {/* Settings toggle */}
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="text-slate-600 hover:text-slate-400 text-sm transition-colors"
              >
                {showSettings ? '▾ Hide options' : '▸ Deck options'}
              </button>

              {/* Settings panel */}
              {showSettings && (
                <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-800 space-y-3">
                  <Toggle label="Major Arcana only" hint="Use only the 22 Major Arcana cards" checked={majorOnly} onChange={() => setMajorOnly(!majorOnly)} />
                  <Toggle label="Reversed cards" hint="Allow cards to appear reversed (inverted meaning)" checked={useReversals} onChange={() => setUseReversals(!useReversals)} />
                </div>
              )}

              <button onClick={() => setPhase('question')} className={`w-full ${btnPrimary}`}>Begin Reading</button>
            </div>
          </div>
        )}

        {phase === 'question' && (
          <div className="max-w-md mx-auto text-center">
            <p className="text-slate-500 mb-6">What guidance do you seek?</p>
            <textarea value={question} onChange={e => setQuestion(e.target.value)} placeholder="Your question (or leave blank for general guidance)..." rows={3}
              className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-4 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-violet-500/50 resize-none mb-4" />
            <p className="text-slate-600 text-xs mb-6">Tip: Open-ended questions yield richer insights</p>
            <button onClick={() => { shuffleDeck(); setPhase('select') }} className={`w-full ${btnSecondary}`}>Continue</button>
          </div>
        )}

        {/* Card Selection Phase */}
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
              {deck.slice(0, Math.min(21, deck.length)).map((card, i) => (
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
            <button onClick={reset} className="text-slate-600 hover:text-slate-400 text-sm">
              Start Over
            </button>
          </div>
        )}

        {phase === 'reading' && (
          <div>
            {question && <p className="text-center text-slate-600 mb-4 md:mb-8 italic text-base md:text-lg px-4">"{question}"</p>}

            {/* Celtic Cross special layout */}
            {spread === 'celtic' ? (
              <div className="relative mx-auto mb-8 overflow-x-auto" style={{ minWidth: 500, height: 450 }}>
                <div className="relative" style={{ width: 500, height: 450, margin: '0 auto' }}>
                  {drawn.map((card, i) => {
                    const isRev = revealed.includes(i)
                    const isDealt = dealingIndex >= i
                    const pos = celticLayout[i]
                    const baseX = 140
                    const baseY = 180
                    const spacing = 100

                    return (
                      <div
                        key={card.id}
                        className={`absolute transition-all duration-500 ${isDealt ? 'opacity-100' : 'opacity-0 scale-75'}`}
                        style={{
                          left: baseX + pos.x * spacing,
                          top: baseY + pos.y * spacing,
                          transform: `rotate(${pos.rotate}deg)`,
                          zIndex: i === 1 ? 2 : 1
                        }}
                      >
                        <div
                          className="relative group"
                          onMouseEnter={() => setHoveredPosition(i)}
                          onMouseLeave={() => setHoveredPosition(null)}
                        >
                          {/* Position tooltip */}
                          {hoveredPosition === i && (
                            <div className="absolute -top-16 left-1/2 -translate-x-1/2 bg-slate-800 px-3 py-2 rounded-lg text-xs whitespace-nowrap z-20 border border-slate-700">
                              <div className="text-violet-400 font-medium">{spreadData.positions[i].name}</div>
                              <div className="text-slate-500">{spreadData.positions[i].description}</div>
                            </div>
                          )}
                          <Card3D
                            card={card}
                            isRevealed={isRev}
                            onClick={() => !isRev && isDealt && setRevealed([...revealed, i])}
                            size="small"
                            enableHover={isRev}
                          />
                          {isRev && (
                            <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap">
                              <p className="text-slate-400 text-xs">{card.name.split(' ').slice(-2).join(' ')}</p>
                              {card.reversed && <p className="text-amber-500/80 text-xs">Reversed</p>}
                            </div>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            ) : (
              /* Standard horizontal layout for other spreads */
              <div className={`flex flex-wrap justify-center mb-6 md:mb-8 gap-3 md:gap-6`}>
                {drawn.map((card, i) => {
                  const isRev = revealed.includes(i)
                  const isDealt = dealingIndex >= i
                  return (
                    <div
                      key={card.id}
                      className={`text-center transition-all duration-500 ${isDealt ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-8'}`}
                      onMouseEnter={() => setHoveredPosition(i)}
                      onMouseLeave={() => setHoveredPosition(null)}
                    >
                      {/* Position name with tooltip */}
                      <div className="relative">
                        <p className="text-slate-500 text-xs md:text-sm mb-2 md:mb-3 font-medium cursor-help">
                          {spreadData.positions[i].name}
                        </p>
                        {hoveredPosition === i && (
                          <div className="absolute -top-12 left-1/2 -translate-x-1/2 bg-slate-800 px-3 py-2 rounded-lg text-xs whitespace-nowrap z-20 border border-slate-700">
                            <div className="text-slate-400">{spreadData.positions[i].description}</div>
                          </div>
                        )}
                      </div>
                      <Card3D
                        card={card}
                        isRevealed={isRev}
                        onClick={() => !isRev && isDealt && setRevealed([...revealed, i])}
                        size={spread === 'single' ? 'large' : 'normal'}
                        enableHover={isRev}
                      />
                      {isRev && (
                        <div className="mt-2 md:mt-3">
                          <p className="text-slate-300 text-xs md:text-sm font-medium max-w-[120px] md:max-w-none mx-auto">{card.name}</p>
                          {card.reversed && <p className="text-amber-500/80 text-xs mt-1">Reversed</p>}
                          {/* Card keywords - show on hover */}
                          <div className={`flex flex-wrap justify-center gap-1 mt-2 max-w-[140px] mx-auto transition-opacity duration-300 ${hoveredPosition === i ? 'opacity-100' : 'opacity-0'}`}>
                            {card.keywords?.slice(0, 3).map((kw, ki) => (
                              <span key={ki} className="text-xs text-slate-500 bg-slate-800/50 px-2 py-0.5 rounded">
                                {kw}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}

            {dealingIndex >= drawn.length - 1 && !allRevealed && (
              <p className="text-center text-slate-600 animate-pulse">Click each card to reveal</p>
            )}

            {allRevealed && (
              <div className="mt-12 max-w-2xl mx-auto">
                <div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
                  <h3 className="text-slate-400 text-sm font-medium mb-4 uppercase tracking-wider">Reading Summary</h3>
                  <div className="space-y-3">
                    {drawn.map((card, i) => (
                      <div key={card.id} className="flex items-start gap-3">
                        <span className="text-violet-400 font-medium min-w-[100px]">{spreadData.positions[i].name}:</span>
                        <div>
                          <span className="text-slate-300">{card.name}{card.reversed && <span className="text-amber-500/80 ml-2">(Reversed)</span>}</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {card.keywords?.map((kw, ki) => (
                              <span key={ki} className="text-xs text-slate-500">{kw}{ki < card.keywords.length - 1 ? ' ·' : ''}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <button onClick={copy} className={`mt-6 w-full text-sm ${btnPrimary}`}>{copied ? '✓ Copied!' : 'Copy for Claude or ChatGPT'}</button>
                </div>
                <div className="text-center mt-8">
                  <button onClick={reset} className="text-slate-600 hover:text-slate-400 transition-colors">New Reading</button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
