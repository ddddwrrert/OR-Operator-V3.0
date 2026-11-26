export function allowance(options, max) {
  return Math.min(options.maxAttempts, Math.floor(max * options.fraction))
}
export async function reservePair(state, maximum, save) {
  if (state.pairs >= maximum) return false
  state.pairs++
  await save()
  return true
}
