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
  // Known new moon: December 30, 2024 at 22:27 UTC
  const knownNewMoon = new Date(Date.UTC(2024, 11, 30, 22, 27))
  const synodicMonth = 29.53058867

  const daysSinceNew = (date - knownNewMoon) / (1000 * 60 * 60 * 24)
  // Add half a phase width (~1.85 days) to center phases on their peak
  const lunarAge = ((daysSinceNew % synodicMonth) + synodicMonth) % synodicMonth
  const phaseWidth = synodicMonth / 8
  const centeredAge = lunarAge + phaseWidth / 2
  const phaseIndex = Math.floor((centeredAge / synodicMonth) * 8) % 8

  return MOON_PHASES[phaseIndex]
}
