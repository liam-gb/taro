// Celtic Cross traditional layout positions (relative grid coordinates)
const CELTIC_LAYOUT = [
  { x: 0, y: 0, rotate: 0 },      // 1: Present (center)
  { x: 0, y: 0, rotate: 90 },     // 2: Challenge (crossing)
  { x: -1, y: 0, rotate: 0 },     // 3: Past (left)
  { x: 1, y: 0, rotate: 0 },      // 4: Future (right)
  { x: 0, y: -1, rotate: 0 },     // 5: Above (crown)
  { x: 0, y: 1, rotate: 0 },      // 6: Below (foundation)
  { x: 2.2, y: 1.5, rotate: 0 },  // 7: Advice (staff bottom)
  { x: 2.2, y: 0.5, rotate: 0 },  // 8: External (staff)
  { x: 2.2, y: -0.5, rotate: 0 }, // 9: Hopes/Fears (staff)
  { x: 2.2, y: -1.5, rotate: 0 }, // 10: Outcome (staff top)
]

export const SPREADS = {
  single: {
    name: "Daily Draw",
    positions: [{ name: "Today's Guidance", description: "Your guidance for today" }]
  },
  threeCard: {
    name: "Past · Present · Future",
    positions: [
      { name: "Past", description: "What has led to this moment" },
      { name: "Present", description: "Where you are now" },
      { name: "Future", description: "Where this path leads" }
    ]
  },
  situation: {
    name: "Situation · Action · Outcome",
    positions: [
      { name: "Situation", description: "The nature of what you face" },
      { name: "Action", description: "The approach advised" },
      { name: "Outcome", description: "The likely result" }
    ]
  },
  celtic: {
    name: "Celtic Cross",
    layout: CELTIC_LAYOUT,
    positions: [
      { name: "Present", description: "Current situation" },
      { name: "Challenge", description: "Obstacle you face" },
      { name: "Past", description: "Recent influences" },
      { name: "Future", description: "What's coming" },
      { name: "Above", description: "Best outcome" },
      { name: "Below", description: "Subconscious" },
      { name: "Advice", description: "How to approach" },
      { name: "External", description: "Outside influences" },
      { name: "Hopes/Fears", description: "Inner conflict" },
      { name: "Outcome", description: "Final result" }
    ]
  },
  horseshoe: {
    name: "Horseshoe",
    positions: [
      { name: "Past", description: "What has shaped the situation" },
      { name: "Present", description: "Current circumstances" },
      { name: "Hidden Influences", description: "Factors not immediately apparent" },
      { name: "Obstacles", description: "Challenges to overcome" },
      { name: "External Influences", description: "People or events affecting you" },
      { name: "Advice", description: "Guidance for moving forward" },
      { name: "Outcome", description: "Where this path leads" }
    ]
  }
}
