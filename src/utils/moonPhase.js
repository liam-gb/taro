// Simple moon phase calculation based on lunar cycle
// Synodic month is ~29.53 days

const MOON_PHASES = [
  { name: "New Moon", icon: "🌑", meaning: "New beginnings, setting intentions, planting seeds" },
  { name: "Waxing Crescent", icon: "🌒", meaning: "Taking action, building momentum, hope emerges" },
  { name: "First Quarter", icon: "🌓", meaning: "Challenges arise, decisions needed, commitment tested" },
  { name: "Waxing Gibbous", icon: "🌔", meaning: "Refining plans, patience required, trust the process" },
  { name: "Full Moon", icon: "🌕", meaning: "Culmination, clarity, emotions heightened, harvest results" },
  { name: "Waning Gibbous", icon: "🌖", meaning: "Gratitude, sharing wisdom, integration" },
  { name: "Last Quarter", icon: "🌗", meaning: "Release, forgiveness, letting go of what no longer serves" },
  { name: "Waning Crescent", icon: "🌘", meaning: "Rest, reflection, preparing for renewal" }
]

export function getMoonPhase(date = new Date()) {
  // Known new moon: January 6, 2000
  const knownNewMoon = new Date(2000, 0, 6, 18, 14)
  const synodicMonth = 29.53058867

  const daysSinceNew = (date - knownNewMoon) / (1000 * 60 * 60 * 24)
  const lunarAge = daysSinceNew % synodicMonth
  const phaseIndex = Math.floor((lunarAge / synodicMonth) * 8) % 8

  return MOON_PHASES[phaseIndex]
}
