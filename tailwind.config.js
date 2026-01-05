/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Deep cosmic backgrounds
        void: {
          DEFAULT: '#0a0a0f',
          50: '#12121a',
          100: '#1a1a24',
          200: '#22222e',
        },
        // Warm mystical accent colors
        mystic: {
          gold: '#c9a86c',      /* Aged gold - primary */
          sienna: '#a0522d',    /* Warm terracotta */
          sage: '#7a9e7e',      /* Mystical sage green */
          bronze: '#d4a574',    /* Warm bronze highlight */
          deep: '#1a1a2e',      /* Deep indigo shadow */
        },
        // Glass surface colors
        glass: {
          DEFAULT: 'rgba(255,255,255,0.03)',
          light: 'rgba(255,255,255,0.06)',
          medium: 'rgba(255,255,255,0.08)',
          bright: 'rgba(255,255,255,0.12)',
        },
      },
      fontFamily: {
        mystical: ['Cormorant Garamond', 'Garamond', 'Georgia', 'serif'],
        ethereal: ['Spectral', 'Georgia', 'serif'],
      },
      animation: {
        'aurora': 'aurora 15s ease infinite',
        'aurora-slow': 'aurora 25s ease infinite',
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 6s ease-in-out 3s infinite',
        'pulse-glow': 'pulse-glow 3s ease-in-out infinite',
        'shimmer': 'shimmer 3s linear infinite',
        'iridescent': 'iridescent 8s ease infinite',
        'breathe': 'breathe 4s ease-in-out infinite',
      },
      keyframes: {
        aurora: {
          '0%, 100%': { transform: 'translate(0, 0) rotate(0deg) scale(1)' },
          '25%': { transform: 'translate(5%, 5%) rotate(2deg) scale(1.05)' },
          '50%': { transform: 'translate(-5%, 10%) rotate(-2deg) scale(1.1)' },
          '75%': { transform: 'translate(-10%, -5%) rotate(1deg) scale(1.02)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '0.5', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.05)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        iridescent: {
          '0%, 100%': { filter: 'hue-rotate(0deg)' },
          '50%': { filter: 'hue-rotate(30deg)' },
        },
        breathe: {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        'glow-gold': '0 0 30px rgba(201, 168, 108, 0.3), 0 0 60px rgba(201, 168, 108, 0.1)',
        'glow-sage': '0 0 30px rgba(122, 158, 126, 0.3), 0 0 60px rgba(122, 158, 126, 0.1)',
        'glow-sienna': '0 0 30px rgba(160, 82, 45, 0.3), 0 0 60px rgba(160, 82, 45, 0.1)',
        'glow-soft': '0 0 40px rgba(201, 168, 108, 0.15)',
        'glass': '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
        'glass-hover': '0 12px 48px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
        'card': '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
      },
    },
  },
  plugins: [],
}
