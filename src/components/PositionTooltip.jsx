export default function PositionTooltip({ position, showName = true }) {
  const topOffset = showName ? '-top-20' : '-top-16'

  return (
    <div className={`absolute ${topOffset} left-1/2 tooltip-glass px-4 py-3 rounded-xl text-xs whitespace-nowrap z-[100]`}
      style={{ transform: 'translateX(-50%)', animation: 'tooltip-fade-in 0.2s ease' }}>
      {/* Decorative top accent */}
      <div className="absolute -top-px left-4 right-4 h-px bg-gradient-to-r from-transparent via-violet-500/50 to-transparent" />

      {showName && (
        <div className="text-violet-400/90 font-medium tracking-wide mb-1">{position.name}</div>
      )}
      <div className="text-slate-400/90 font-light">{position.description}</div>

      {/* Arrow pointer */}
      <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 bg-[rgba(15,15,25,0.9)] border-r border-b border-white/10" />
    </div>
  )
}
