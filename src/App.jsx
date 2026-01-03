import { useReducer, useEffect, useCallback } from 'react'
import WelcomePhase from './components/WelcomePhase'
import QuestionPhase from './components/QuestionPhase'
import ShufflePhase from './components/ShufflePhase'
import ReadingPhase from './components/ReadingPhase'
import { FULL_DECK, SPREADS } from './data'
import { generateReadingPrompt } from './utils/generatePrompt'
import { REVERSAL_PROBABILITY, HOVER_CARD_COUNT } from './constants'

const initialState = {
  phase: 'welcome',
  question: '',
  selectedSpread: 'threeCard',
  deck: [],
  drawnCards: [],
  revealedIndices: [],
  shuffleCount: 0,
  hoverCards: [],
  copied: false
}

function reducer(state, action) {
  switch (action.type) {
    case 'SET_PHASE':
      return { ...state, phase: action.phase }
    case 'SET_QUESTION':
      return { ...state, question: action.question }
    case 'SET_SPREAD':
      return { ...state, selectedSpread: action.spread }
    case 'SHUFFLE':
      return {
        ...state,
        deck: action.deck,
        hoverCards: action.hoverCards,
        shuffleCount: state.shuffleCount + 1
      }
    case 'INIT_DECK':
      return { ...state, deck: action.deck, hoverCards: action.hoverCards }
    case 'DRAW_CARDS':
      return {
        ...state,
        drawnCards: action.drawnCards,
        deck: action.remainingDeck,
        revealedIndices: [],
        phase: 'reading'
      }
    case 'REVEAL_CARD':
      return state.revealedIndices.includes(action.index)
        ? state
        : { ...state, revealedIndices: [...state.revealedIndices, action.index] }
    case 'SET_COPIED':
      return { ...state, copied: action.copied }
    case 'RESET':
      return { ...initialState, deck: action.deck, hoverCards: action.hoverCards }
    default:
      return state
  }
}

function shuffleAndPrepare() {
  const shuffled = [...FULL_DECK]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  const deck = shuffled.map(card => ({ ...card, reversed: Math.random() > (1 - REVERSAL_PROBABILITY) }))
  const hoverCards = shuffled.slice(0, HOVER_CARD_COUNT)
  return { deck, hoverCards }
}

export default function App() {
  const [state, dispatch] = useReducer(reducer, initialState)
  const { phase, question, selectedSpread, deck, drawnCards, revealedIndices, shuffleCount, hoverCards, copied } = state

  const spread = SPREADS[selectedSpread]

  const shuffleDeck = useCallback((isInit = false) => {
    const { deck, hoverCards } = shuffleAndPrepare()
    dispatch({ type: isInit ? 'INIT_DECK' : 'SHUFFLE', deck, hoverCards })
  }, [])

  useEffect(() => { shuffleDeck(true) }, [shuffleDeck])

  const drawCards = () => {
    const numCards = spread.positions.length
    dispatch({
      type: 'DRAW_CARDS',
      drawnCards: deck.slice(0, numCards),
      remainingDeck: deck.slice(numCards)
    })
  }

  const copyToClipboard = () => {
    const prompt = generateReadingPrompt(drawnCards, spread, question)
    navigator.clipboard.writeText(prompt)
    dispatch({ type: 'SET_COPIED', copied: true })
    setTimeout(() => dispatch({ type: 'SET_COPIED', copied: false }), 2000)
  }

  const startOver = () => {
    const { deck, hoverCards } = shuffleAndPrepare()
    dispatch({ type: 'RESET', deck, hoverCards })
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-200">
      <div className="text-center py-6">
        <h1 className="text-xl tracking-[0.4em] text-slate-500 font-light">TAROT</h1>
      </div>

      <div className="max-w-7xl mx-auto px-4 pb-12">
        {phase === 'welcome' && (
          <WelcomePhase
            hoverCards={hoverCards}
            selectedSpread={selectedSpread}
            onSelectSpread={(s) => dispatch({ type: 'SET_SPREAD', spread: s })}
            onBegin={() => dispatch({ type: 'SET_PHASE', phase: 'question' })}
          />
        )}

        {phase === 'question' && (
          <QuestionPhase
            question={question}
            onQuestionChange={(q) => dispatch({ type: 'SET_QUESTION', question: q })}
            onContinue={() => dispatch({ type: 'SET_PHASE', phase: 'shuffle' })}
          />
        )}

        {phase === 'shuffle' && (
          <ShufflePhase
            shuffleCount={shuffleCount}
            onShuffle={() => shuffleDeck(false)}
            onDraw={drawCards}
          />
        )}

        {phase === 'reading' && (
          <ReadingPhase
            question={question}
            drawnCards={drawnCards}
            spread={spread}
            selectedSpread={selectedSpread}
            revealedIndices={revealedIndices}
            onRevealCard={(i) => dispatch({ type: 'REVEAL_CARD', index: i })}
            onCopy={copyToClipboard}
            copied={copied}
            onStartOver={startOver}
          />
        )}
      </div>
    </div>
  )
}
