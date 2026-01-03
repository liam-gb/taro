import { useState, useEffect, useCallback } from 'react'
import Card3D from './components/Card3D'
import { FULL_DECK, SPREADS } from './data'
import { generateReadingPrompt } from './utils/generatePrompt'

export default function App() {
  const [phase, setPhase] = useState('welcome')
  const [question, setQuestion] = useState('')
  const [selectedSpread, setSelectedSpread] = useState('threeCard')
  const [deck, setDeck] = useState([])
  const [drawnCards, setDrawnCards] = useState([])
  const [revealedIndices, setRevealedIndices] = useState([])
  const [shuffleCount, setShuffleCount] = useState(0)
  const [hoverCards, setHoverCards] = useState([])
  const [copied, setCopied] = useState(false)

  const shuffleDeck = useCallback(() => {
    const shuffled = [...FULL_DECK]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    setDeck(shuffled.map(card => ({ ...card, reversed: Math.random() > 0.7 })))

    const randomCards = []
    const usedIndices = new Set()
    for (let i = 0; i < 5; i++) {
      let idx
      do { idx = Math.floor(Math.random() * shuffled.length) }
      while (usedIndices.has(idx))
      usedIndices.add(idx)
      randomCards.push(shuffled[idx])
    }
    setHoverCards(randomCards)
  }, [])

  useEffect(() => { shuffleDeck() }, [shuffleDeck])

  const spread = SPREADS[selectedSpread]
  const allRevealed = drawnCards.length > 0 && revealedIndices.length === drawnCards.length

  const handleShuffle = () => {
    shuffleDeck()
    setShuffleCount(prev => prev + 1)
  }

  const drawCards = () => {
    const numCards = spread.positions.length
    setDrawnCards(deck.slice(0, numCards))
    setDeck(deck.slice(numCards))
    setRevealedIndices([])
    setPhase('reading')
  }

  const revealCard = (index) => {
    if (!revealedIndices.includes(index)) {
      setRevealedIndices(prev => [...prev, index])
    }
  }

  const startOver = () => {
    setPhase('welcome')
    setQuestion('')
    setDrawnCards([])
    setRevealedIndices([])
    setShuffleCount(0)
    setCopied(false)
    shuffleDeck()
  }

  const copyToClipboard = () => {
    const prompt = generateReadingPrompt(drawnCards, spread, question)
    navigator.clipboard.writeText(prompt)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-200">
      <div className="text-center py-6">
        <h1 className="text-xl tracking-[0.4em] text-slate-500 font-light">TAROT</h1>
      </div>

      <div className="max-w-7xl mx-auto px-4 pb-12">

        {/* WELCOME */}
        {phase === 'welcome' && (
          <div className="text-center">
            <p className="text-slate-600 text-sm mb-6 md:mb-8">Tap or hover to glimpse the cards</p>

            {/* Mobile: 3 cards, Desktop: 5 cards */}
            <div className="flex justify-center gap-2 md:gap-4 mb-8 md:mb-12 flex-wrap">
              {[0, 1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className={`${i >= 3 ? 'hidden md:block' : ''}`}
                  style={{ transform: `rotate(${(i - 2) * 4}deg)` }}
                >
                  <Card3D
                    card={hoverCards[i]}
                    size="normal"
                    enableHover={true}
                    hoverCard={hoverCards[i]}
                  />
                </div>
              ))}
            </div>

            <div className="space-y-4 max-w-sm mx-auto">
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(SPREADS).map(([key, s]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedSpread(key)}
                    className={`p-4 rounded-lg transition-all text-left
                      ${selectedSpread === key
                        ? 'bg-slate-800 ring-1 ring-violet-500/40'
                        : 'bg-slate-900/50 hover:bg-slate-800/50'}`}
                  >
                    <div className="text-slate-300 text-sm">{s.name}</div>
                    <div className="text-xs text-slate-600 mt-1">{s.positions.length} card{s.positions.length > 1 ? 's' : ''}</div>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setPhase('question')}
                className="w-full py-4 bg-violet-900/30 hover:bg-violet-800/40 rounded-lg transition-colors text-slate-300 border border-violet-500/20"
              >
                Begin Reading
              </button>
            </div>
          </div>
        )}

        {/* QUESTION */}
        {phase === 'question' && (
          <div className="max-w-md mx-auto text-center">
            <p className="text-slate-500 mb-6">What guidance do you seek?</p>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Your question (or leave blank)..."
              className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-4 text-slate-200
                placeholder-slate-600 focus:outline-none focus:border-violet-500/50 resize-none mb-6"
              rows={3}
            />
            <button
              onClick={() => setPhase('shuffle')}
              className="w-full py-4 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors text-slate-300"
            >
              Continue
            </button>
          </div>
        )}

        {/* SHUFFLE */}
        {phase === 'shuffle' && (
          <div className="text-center">
            <p className="text-slate-500 mb-8">Focus on your question and click to shuffle</p>
            <div onClick={handleShuffle} className="inline-block cursor-pointer mb-8">
              <div className="relative" style={{ width: 260, height: 400 }}>
                {[0, 1, 2, 3, 4, 5].map((i) => (
                  <div
                    key={i}
                    style={{
                      position: 'absolute',
                      top: i * -3,
                      left: i * 3,
                      transform: shuffleCount > 0 ? `rotate(${(Math.random() - 0.5) * 8}deg)` : 'none',
                      transition: 'transform 0.3s',
                    }}
                  >
                    <Card3D size="large" />
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-center gap-3 mb-6">
              {[1, 2, 3].map(i => (
                <div key={i} className={`w-3 h-3 rounded-full transition-all duration-300
                  ${shuffleCount >= i ? 'bg-violet-400 shadow-lg shadow-violet-500/50' : 'bg-slate-700'}`} />
              ))}
            </div>

            {shuffleCount >= 3 && (
              <button
                onClick={drawCards}
                className="px-8 py-3 bg-violet-900/40 hover:bg-violet-800/50 rounded-lg transition-colors text-slate-300 border border-violet-500/20"
              >
                Draw Cards
              </button>
            )}
          </div>
        )}

        {/* READING */}
        {phase === 'reading' && (
          <div>
            {question && <p className="text-center text-slate-600 mb-4 md:mb-8 italic text-base md:text-lg px-4">"{question}"</p>}

            <div className={`flex flex-wrap justify-center mb-6 md:mb-8 ${selectedSpread === 'celtic' ? 'gap-2 md:gap-4' : 'gap-3 md:gap-6'}`}>
              {drawnCards.map((card, index) => (
                <div key={card.id} className="text-center">
                  <p className="text-slate-500 text-xs md:text-sm mb-2 md:mb-3 font-medium">{spread.positions[index].name}</p>
                  <Card3D
                    card={card}
                    isRevealed={revealedIndices.includes(index)}
                    onClick={() => revealCard(index)}
                    size={selectedSpread === 'celtic' ? 'small' : (selectedSpread === 'single' ? 'large' : 'normal')}
                    enableHover={revealedIndices.includes(index)}
                  />
                  {revealedIndices.includes(index) && (
                    <div className="mt-2 md:mt-3">
                      <p className="text-slate-300 text-xs md:text-sm font-medium max-w-[120px] md:max-w-none mx-auto">{card.name}</p>
                      {card.reversed && <p className="text-amber-500/80 text-xs mt-1">Reversed</p>}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {!allRevealed && <p className="text-center text-slate-600">Click each card to reveal</p>}

            {allRevealed && (
              <div className="mt-12 max-w-2xl mx-auto">
                <div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
                  <h3 className="text-slate-400 text-sm font-medium mb-4 uppercase tracking-wider">Reading Summary</h3>
                  <div className="space-y-3">
                    {drawnCards.map((card, index) => (
                      <div key={card.id} className="flex items-start gap-3">
                        <span className="text-violet-400 font-medium min-w-[100px]">{spread.positions[index].name}:</span>
                        <span className="text-slate-300">{card.name}{card.reversed ? <span className="text-amber-500/80 ml-2">(Reversed)</span> : ''}</span>
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={copyToClipboard}
                    className="mt-6 w-full py-3 bg-violet-900/30 hover:bg-violet-800/40 rounded-lg transition-colors text-slate-300 text-sm border border-violet-500/20"
                  >
                    {copied ? '✓ Copied!' : 'Copy for Claude or ChatGPT'}
                  </button>
                </div>

                <div className="text-center mt-8">
                  <button onClick={startOver} className="text-slate-600 hover:text-slate-400 transition-colors">
                    New Reading
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
