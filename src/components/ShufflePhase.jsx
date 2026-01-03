import Card3D from './Card3D'
import Button from './Button'
import { SHUFFLE_DECK_SIZE, REQUIRED_SHUFFLES, SHUFFLE_STACK_COUNT } from '../constants'

export default function ShufflePhase({ shuffleCount, onShuffle, onDraw }) {
  const canDraw = shuffleCount >= REQUIRED_SHUFFLES

  return (
    <div className="text-center">
      <p className="text-slate-500 mb-8">Focus on your question and click to shuffle</p>

      <div onClick={onShuffle} className="inline-block cursor-pointer mb-8">
        <div className="relative" style={SHUFFLE_DECK_SIZE}>
          {Array.from({ length: SHUFFLE_STACK_COUNT }, (_, i) => (
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
        {Array.from({ length: REQUIRED_SHUFFLES }, (_, i) => (
          <div
            key={i}
            className={`w-3 h-3 rounded-full transition-all duration-300
              ${shuffleCount >= i + 1 ? 'bg-violet-400 shadow-lg shadow-violet-500/50' : 'bg-slate-700'}`}
          />
        ))}
      </div>

      {canDraw && (
        <Button onClick={onDraw}>
          Draw Cards
        </Button>
      )}
    </div>
  )
}
