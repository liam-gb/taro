const styles = {
  base: 'relative font-light tracking-wide transition-all duration-300',
  primary: 'btn-glass py-4 px-6 rounded-xl text-slate-200',
  secondary: 'btn-glass-secondary py-4 px-6 rounded-xl',
  text: 'btn-text py-2 px-4'
}

export default function Button({ variant = 'primary', className = '', children, ...props }) {
  return (
    <button className={`${styles.base} ${styles[variant]} ${className}`} {...props}>
      <span className="relative z-10">{children}</span>
    </button>
  )
}
