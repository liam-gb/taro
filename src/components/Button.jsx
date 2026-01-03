const variants = {
  primary: 'bg-violet-900/30 hover:bg-violet-800/40 border border-violet-500/20 text-slate-300',
  secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-300',
  ghost: 'text-slate-600 hover:text-slate-400'
}

const sizes = {
  normal: 'py-4 px-6',
  small: 'py-3 px-4 text-sm'
}

export default function Button({
  children,
  onClick,
  variant = 'primary',
  size = 'normal',
  className = '',
  fullWidth = false
}) {
  return (
    <button
      onClick={onClick}
      className={`
        ${variants[variant]}
        ${sizes[size]}
        ${fullWidth ? 'w-full' : ''}
        rounded-lg transition-colors
        ${className}
      `}
    >
      {children}
    </button>
  )
}
