import { createHash } from 'node:crypto'

export const digest = value => createHash('sha256').update(value).digest('hex')

export function splitProgram(source) {
  const start = [...source.matchAll(/^.*(?:#|\/\/)\s*EVOLVE_START\s*\r?$/gm)]
  const end = [...source.matchAll(/^.*(?:#|\/\/)\s*EVOLVE_END\s*\r?$/gm)]
  if (start.length !== 1 || end.length !== 1 || start[0].index >= end[0].index) return null
  const offset = start[0].index + start[0][0].length
  return [source.slice(0, offset), source.slice(offset, end[0].index), source.slice(end[0].index)]
}

export function profile(source) {
  const body = splitProgram(source)?.[1] ?? source
  const regions = []
  let region = { name: '<inline>', line: 1, calls: [], writes: [], branches: [] }
  regions.push(region)
  for (const [index, line] of body.split('\n').entries()) {
    const definition = line.match(/^\s*(?:(?:async\s+)?def\s+|(?:export\s+)?(?:async\s+)?function\s+|[\w:*<>]+\s+)(\w+)\s*\([^;]*\)\s*[:{]/)
    if (definition && !/^\s*(?:if|else|for|while|switch|catch|return|throw|with|assert)\b/.test(line)) {
      region = { name: definition[1], line: index + 1, calls: [], writes: [], branches: [] }
      regions.push(region)
    }
    for (const match of line.matchAll(/\b([a-zA-Z_]\w*(?:\.\w+)*)\s*\(/g)) {
      if (match[1] !== region.name && !/^(?:if|for|while|switch|catch)$/.test(match[1]) && !region.calls.includes(match[1])) region.calls.push(match[1])
    }
    const write = line.match(/^\s*([\w.]+(?:\[[^\]]+\])?)\s*(?:[+*\/-]?=(?!=)|\+\+|--)/)
    if (write && !region.writes.includes(write[1])) region.writes.push(write[1])
    if (/\b(?:if|while|for|assert|return)\b/.test(line)) region.branches.push(line.trim())
  }
  return { hash: digest(body), regions }
}

export function evidence(rows, merit, window, metrics = {}) {
  const scores = new Map(rows.map(row => [row.id, merit(row.fitness)]))
  let best = -Infinity
  let stagnant = 0
  for (const row of rows) {
    if (scores.get(row.id) > best) {
      best = scores.get(row.id)
      stagnant = 0
    } else {
      stagnant++
    }
  }
  return {
    stagnant,
    trajectory: rows.slice(-window).map(row => ({
      ...row,
      parentDelta: row.parent && scores.has(row.parent) ? scores.get(row.id) - scores.get(row.parent) : null,
      metrics: metrics[row.id],
    })),
  }
}

const validText = value => typeof value === 'string' && value.trim().length > 0 && value.length <= 1500

function parseJson(raw) {
  try {
    return JSON.parse(raw.trim().replace(/^\x60{3}(?:json)?\s*|\s*\x60{3}$/g, ''))
  } catch {
    return null
  }
}

export function parseDiagnosis(raw, minimumConfidence) {
  const hypothesis = parseJson(raw)?.hypothesis
  if (!hypothesis || ![hypothesis.claim, hypothesis.test].every(validText)) return null
  if (!Array.isArray(hypothesis.evidence) || !hypothesis.evidence.length || !hypothesis.evidence.every(validText)) return null
  if (!Number.isFinite(hypothesis.confidence) || hypothesis.confidence < minimumConfidence || hypothesis.confidence > 1) return null
  return hypothesis
}

export function parseReport(raw, minimumConfidence, expected = [], diagnosis) {
  const report = parseJson(raw)
  const hypothesis = diagnosis ?? parseDiagnosis(raw, minimumConfidence)
  const operator = report?.operator
  if (!hypothesis || !operator || ![operator.name, operator.change, operator.scope].every(validText)) return null
  if (expected.length && !expected.every(id => Array.isArray(operator.components) && operator.components.includes(id))) return null
  return { hypothesis, operator, mechanism: report.mechanism }
}

export async function validate({ parent, candidate, before, after, evaluate, merit, trial, seeds, spend, signal }) {
  const base = splitProgram(before)
  const variant = splitProgram(after)
  if (!base || !variant || base[0] !== variant[0] || base[2] !== variant[2] || base[1] === variant[1]) {
    return { accepted: false, stage: 'scope' }
  }
  signal.throwIfAborted()
  const fitness = await evaluate(candidate)
  const gain = merit(fitness) - merit(parent.fitness)
  if (!Number.isFinite(fitness) || fitness === 0 || gain <= 0) return { accepted: false, stage: 'official', fitness, gain }
  if (!trial) return { accepted: true, stage: 'official', fitness, gain, attribution: 'whole-edit paired with parent' }

  const pairs = []
  for (const seed of seeds) {
    signal.throwIfAborted()
    if (!await spend()) return { accepted: false, stage: 'trial-budget', fitness, gain, pairs }
    const control = await trial(parent, seed, signal)
    const treatment = await trial(candidate, seed, signal)
    const delta = merit(treatment) - merit(control)
    pairs.push({ seed, control, treatment, delta })
    if (![control, treatment].every(value => Number.isFinite(value) && value !== 0) || (pairs.length === 1 && delta <= 0)) {
      return { accepted: false, stage: 'paired-screen', fitness, gain, pairs }
    }
  }
  const mean = pairs.reduce((sum, pair) => sum + pair.delta, 0) / pairs.length
  const accepted = mean > 0 && pairs.filter(pair => pair.delta > 0).length > pairs.length / 2
  return { accepted, stage: 'paired-confirmation', fitness, gain, pairs, mean, attribution: 'whole-edit paired with parent' }
}

