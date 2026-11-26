export function compareComposition(control, singles, forward, reverse) {
  const gains = singles.map(score => score - control)
  const gain = forward - control
  return {
    control, singles, forward, reverse, gain,
    interaction: gain - gains.reduce((sum, value) => sum + value, 0),
    orderEffect: forward - reverse,
    conflicts: forward < Math.max(...singles),
  }
}

