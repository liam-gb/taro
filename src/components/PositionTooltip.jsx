export default function PositionTooltip({ position, showName = true }) {
  const topOffset = showName ? '-top-16' : '-top-12'
  const descColor = showName ? 'text-slate-500' : 'text-slate-400'

  return (
    <div className={`absolute ${topOffset} left-1/2 -translate-x-1/2 bg-slate-800 px-3 py-2 rounded-lg text-xs whitespace-nowrap z-20 border border-slate-700`}>
      {showName && <div className="text-violet-400 font-medium">{position.name}</div>}
      <div className={descColor}>{position.description}</div>
    </div>
  )
}
