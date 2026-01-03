export default function KeywordList({ keywords = [], variant = 'inline', limit }) {
  const items = limit ? keywords.slice(0, limit) : keywords

  if (variant === 'badges') {
    return (
      <div className="flex flex-wrap justify-center gap-1.5">
        {items.map((kw, i) => (
          <span
            key={i}
            className="text-xs text-slate-400/90 badge-glass px-2.5 py-1 rounded-full font-light tracking-wide"
          >
            {kw}
          </span>
        ))}
      </div>
    )
  }

  return (
    <div className="flex flex-wrap gap-1">
      {items.map((kw, i) => (
        <span key={i} className="text-xs text-slate-500/90 font-light">
          {kw}{i < items.length - 1 && <span className="text-violet-500/40 mx-1">·</span>}
        </span>
      ))}
    </div>
  )
}
