import { digest } from './operator.js'

// The worker can propose a successor discovery policy. Give each policy two
// attempts in the same phase before comparing its rate of validated operators.
export function mechanism(state, defaults, phase = 'plateau') {
  const history = state.history.filter(item => item.result)
  state.incumbent ??= { id: 'default', ...defaults }
  state.retired ??= []
  const incumbent = state.incumbent
  if (!state.challenger) {
    const proposal = history.at(-1)?.report?.mechanism
    if (!proposal || typeof proposal.directive !== 'string' || !proposal.directive.trim()
      || proposal.directive.length > 600 || !Number.isInteger(proposal.window)
      || proposal.window < 2 || proposal.window > 24
      || !(proposal.confidence >= 0.5 && proposal.confidence <= 0.95)) return incumbent
    const { seedCount, sequenceLength, allowComposition } = proposal
    if ((seedCount !== undefined && (!Number.isInteger(seedCount) || seedCount < 2 || seedCount > 8))
      || (sequenceLength !== undefined && ![2, 3].includes(sequenceLength))
      || (allowComposition !== undefined && typeof allowComposition !== 'boolean')) return incumbent
    const policy = {
      minimumConfidence: proposal.confidence, window: proposal.window, directive: proposal.directive,
      seedCount, sequenceLength, allowComposition,
    }
    const id = digest(JSON.stringify(policy))
    if (id === incumbent.id || state.retired.includes(id)) return incumbent
    state.challenger = { id, ...policy }
    state.trialStart = state.history.length
  }

  const challenger = state.challenger
  const recent = state.history.slice(state.trialStart).filter(item => item.result)
  const controls = recent.filter(item => item.mechanism.id === incumbent.id)
  const treatments = recent.filter(item => item.mechanism.id === challenger.id)
  const a = controls.filter(item => item.phase === phase)
  const b = treatments.filter(item => item.phase === phase)
  if (a.length >= 2 && b.length >= 2) {
    const wins = group => group.slice(0, 2).filter(item => item.result.accepted).length
    const accepted = wins(b) > wins(a)
    state.retired.push(accepted ? incumbent.id : challenger.id)
    if (accepted) state.incumbent = challenger
    state.mechanismDecisions ??= []
    state.mechanismDecisions.push({ incumbent: incumbent.id, challenger: challenger.id, phase, accepted,
      control: a.slice(0, 2).map(item => item.id), treatment: b.slice(0, 2).map(item => item.id) })
    delete state.challenger
    return state.incumbent
  }
  return a.length <= b.length ? incumbent : challenger
}

