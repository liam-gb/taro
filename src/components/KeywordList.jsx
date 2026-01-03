export default function KeywordList({ keywords = [], variant = 'inline', limit }) {
  const items = limit ? keywords.slice(0, limit) : keywords

  if (variant === 'badges') {
    return (
      <div className="flex flex-wrap justify-center gap-1">
        {items.map((kw, i) => (
          <span key={i} className="text-xs text-slate-500 bg-slate-800/50 px-2 py-0.5 rounded">
            {kw}
          </span>
        ))}
      </div>
    )
  }

  return (
    <div className="flex flex-wrap gap-1">
      {items.map((kw, i) => (
        <span key={i} className="text-xs text-slate-500">
          {kw}{i < items.length - 1 ? ' ·' : ''}
        </span>
      ))}
    </div>
  )
}
