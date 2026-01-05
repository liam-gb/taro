// Animated Sacred Geometry Card Back Pattern
// A mystical, alive card back with subtle animations

export default function CardBackPattern() {
  return (
    <div className="card-back-pattern">
      {/* Base gradient */}
      <div className="card-back-base" />

      {/* Outer rotating ring */}
      <div className="card-back-ring card-back-ring-outer" />

      {/* Middle pulsing ring */}
      <div className="card-back-ring card-back-ring-middle" />

      {/* Inner breathing ring */}
      <div className="card-back-ring card-back-ring-inner" />

      {/* Central focal point */}
      <div className="card-back-center" />

      {/* Constellation dots */}
      {[...Array(12)].map((_, i) => (
        <div
          key={i}
          className="card-back-star"
          style={{
            '--star-angle': `${i * 30}deg`,
            '--star-delay': `${i * 0.3}s`,
            '--star-distance': `${35 + (i % 3) * 8}%`,
          }}
        />
      ))}

      {/* Corner accents */}
      <div className="card-back-corner card-back-corner-tl" />
      <div className="card-back-corner card-back-corner-tr" />
      <div className="card-back-corner card-back-corner-bl" />
      <div className="card-back-corner card-back-corner-br" />

      {/* Subtle border glow */}
      <div className="card-back-border" />
    </div>
  )
}
