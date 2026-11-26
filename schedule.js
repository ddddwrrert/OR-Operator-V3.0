// Select an action using phase-local credit and an exploration bonus.
export function schedule(history, phase, policy = {}) {
  const winners = history.filter(item => item.result?.accepted && item.report && item.plan?.kind !== 'compose')
  const components = [...new Map(winners.map(item => [
    item.report.operator.name.trim().toLowerCase(), item,
  ])).values()].sort((a, b) => b.result.gain - a.result.gain)
  const actions = ['discover']
  if (components.length) actions.push('reuse')
  if (policy.allowComposition !== false && components.length >= 2) actions.push('compose')
  const local = history.filter(item => item.phase === phase && item.result)
  const score = kind => {
    const trials = local.filter(item => item.plan?.kind === kind)
    if (!trials.length) return Infinity
    const totalReward = trials.reduce((sum, item) => {
      const cost = Math.max(1, item.elapsedMs ?? 1)
      return sum + (item.result.accepted ? 1 + Math.max(0, item.result.gain ?? 0) / cost : -0.1)
    }, 0)
    return totalReward / trials.length + Math.sqrt(2 * Math.log(local.length + 1) / trials.length)
  }
  const kind = actions.reduce((best, action) => score(action) > score(best) ? action : best)
  if (kind === 'discover') return { kind, instruction: 'Design one novel operator.' }
  return {
    kind,
    components: components.slice(0, kind === 'reuse' ? 1 : policy.sequenceLength ?? 2).map(item => ({
      id: item.id, ...item.report.operator,
    })),
    instruction: kind === 'reuse'
      ? 'Adapt the selected operator to the current solver and cite its id.'
      : 'Implement the proposed operations in the listed order, with applicability checks, and cite both ids.',
  }
}

