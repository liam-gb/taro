const styles = {
  base: 'transition-colors',
  primary: 'py-4 rounded-lg bg-violet-900/30 hover:bg-violet-800/40 border border-violet-500/20 text-slate-300',
  secondary: 'py-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300',
  text: 'text-slate-600 hover:text-slate-400'
}

export default function Button({ variant = 'primary', className = '', children, ...props }) {
  return (
    <button className={`${styles.base} ${styles[variant]} ${className}`} {...props}>
      {children}
    </button>
  )
}
