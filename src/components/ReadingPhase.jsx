import Card3D from './Card3D'
import Button from './Button'

export default function ReadingPhase({
  question,
  drawnCards,
  spread,
  selectedSpread,
  revealedIndices,
  onRevealCard,
  onCopy,
  copied,
  onStartOver
}) {
  const allRevealed = drawnCards.length > 0 && revealedIndices.length === drawnCards.length

  const getCardSize = () => {
    if (selectedSpread === 'celtic') return 'small'
    if (selectedSpread === 'single') return 'large'
    return 'normal'
  }

  return (
    <div>
      {question && (
        <p className="text-center text-slate-600 mb-4 md:mb-8 italic text-base md:text-lg px-4">
          "{question}"
        </p>
      )}

      <div className={`flex flex-wrap justify-center mb-6 md:mb-8 ${selectedSpread === 'celtic' ? 'gap-2 md:gap-4' : 'gap-3 md:gap-6'}`}>
        {drawnCards.map((card, index) => {
          const isRevealed = revealedIndices.includes(index)
          return (
            <div key={card.id} className="text-center">
              <p className="text-slate-500 text-xs md:text-sm mb-2 md:mb-3 font-medium">
                {spread.positions[index].name}
              </p>
              <Card3D
                card={card}
                isRevealed={isRevealed}
                onClick={() => onRevealCard(index)}
                size={getCardSize()}
                enableHover={isRevealed}
              />
              {isRevealed && (
                <div className="mt-2 md:mt-3">
                  <p className="text-slate-300 text-xs md:text-sm font-medium max-w-[120px] md:max-w-none mx-auto">
                    {card.name}
                  </p>
                  {card.reversed && <p className="text-amber-500/80 text-xs mt-1">Reversed</p>}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {!allRevealed && <p className="text-center text-slate-600">Click each card to reveal</p>}

      {allRevealed && (
        <div className="mt-12 max-w-2xl mx-auto">
          <div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
            <h3 className="text-slate-400 text-sm font-medium mb-4 uppercase tracking-wider">
              Reading Summary
            </h3>
            <div className="space-y-3">
              {drawnCards.map((card, index) => (
                <div key={card.id} className="flex items-start gap-3">
                  <span className="text-violet-400 font-medium min-w-[100px]">
                    {spread.positions[index].name}:
                  </span>
                  <span className="text-slate-300">
                    {card.name}
                    {card.reversed && <span className="text-amber-500/80 ml-2">(Reversed)</span>}
                  </span>
                </div>
              ))}
            </div>

            <Button onClick={onCopy} size="small" fullWidth className="mt-6">
              {copied ? '✓ Copied!' : 'Copy for Claude or ChatGPT'}
            </Button>
          </div>

          <div className="text-center mt-8">
            <Button onClick={onStartOver} variant="ghost">
              New Reading
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
