/**
 * TARO Logo - Runic/Symbolic SVG Wordmark
 *
 * Design:
 * - T: Simple tau with slight serifs
 * - A: Lambda style (Λ) - no crossbar, triangle form
 * - R: Minimal geometric R with shortened leg
 * - O: Perfect circle with subtle weight
 *
 * Inspired by elder futhark runes and sacred geometry
 */

export default function TaroLogo({ className = '', size = 'default' }) {
  // Size presets for responsive use
  const sizes = {
    small: { width: 120, height: 32 },
    default: { width: 180, height: 48 },
    large: { width: 280, height: 75 },
    hero: { width: 360, height: 96 }
  }

  const { width, height } = sizes[size] || sizes.default

  // Stroke width scales with size
  const strokeWidth = size === 'hero' ? 2.5 : size === 'large' ? 2 : 1.5

  return (
    <svg
      viewBox="0 0 180 48"
      width={width}
      height={height}
      className={className}
      aria-label="TARO"
      role="img"
    >
      <defs>
        {/* Gold gradient for the letterforms */}
        <linearGradient id="taro-gold" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#d4a574" />
          <stop offset="50%" stopColor="#c9a86c" />
          <stop offset="100%" stopColor="#a08050" />
        </linearGradient>

        {/* Subtle glow filter */}
        <filter id="taro-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="1.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <g
        fill="none"
        stroke="url(#taro-gold)"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        filter="url(#taro-glow)"
      >
        {/* T - Simple tau with subtle serifs */}
        <path d="M 8 10 L 32 10" /> {/* Top bar */}
        <path d="M 20 10 L 20 38" /> {/* Vertical stem */}

        {/* A - Lambda style (no crossbar) */}
        <path d="M 48 38 L 62 10 L 76 38" /> {/* Triangle/Lambda shape */}

        {/* R - Minimal geometric R */}
        <path d="M 92 38 L 92 10" /> {/* Vertical stem */}
        <path d="M 92 10 L 108 10 Q 116 10 116 18 Q 116 26 108 26 L 92 26" /> {/* Bowl */}
        <path d="M 102 26 L 116 38" /> {/* Leg - shortened, diagonal */}

        {/* O - Perfect circle */}
        <circle cx="144" cy="24" r="14" />
      </g>
    </svg>
  )
}
