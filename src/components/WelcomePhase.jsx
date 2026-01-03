import Card3D from './Card3D'
import Button from './Button'
import { SPREADS } from '../data'
import { CARD_FAN_ROTATION, HOVER_CARD_COUNT } from '../constants'

export default function WelcomePhase({
  hoverCards,
  selectedSpread,
  onSelectSpread,
  onBegin
}) {
  return (
    <div className="text-center">
      <p className="text-slate-600 text-sm mb-6 md:mb-8">Tap or hover to glimpse the cards</p>

      <div className="flex justify-center gap-2 md:gap-4 mb-8 md:mb-12 flex-wrap">
        {Array.from({ length: HOVER_CARD_COUNT }, (_, i) => (
          <div
            key={i}
            className={i >= 3 ? 'hidden md:block' : ''}
            style={{ transform: `rotate(${(i - 2) * CARD_FAN_ROTATION}deg)` }}
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
              onClick={() => onSelectSpread(key)}
              className={`p-4 rounded-lg transition-all text-left
                ${selectedSpread === key
                  ? 'bg-slate-800 ring-1 ring-violet-500/40'
                  : 'bg-slate-900/50 hover:bg-slate-800/50'}`}
            >
              <div className="text-slate-300 text-sm">{s.name}</div>
              <div className="text-xs text-slate-600 mt-1">
                {s.positions.length} card{s.positions.length > 1 ? 's' : ''}
              </div>
            </button>
          ))}
        </div>

        <Button onClick={onBegin} fullWidth>
          Begin Reading
        </Button>
      </div>
    </div>
  )
}
