import { compareComposition } from './composition.js'
import { mkdir, readFile, rename, writeFile } from 'node:fs/promises'
import { dirname, join, resolve } from 'node:path'
import { parseArgs } from 'node:util'
import { pathToFileURL } from 'node:url'
import { createPlugin } from './index.js'

const { values } = parseArgs({ options: { work: { type: 'string', default: 'demo-run' }, config: { type: 'string' } } })
const readConfig = async path => JSON.parse(await readFile(path, 'utf8'))
const options = { ...await readConfig(new URL('./config/default.json', import.meta.url)),
  ...(values.config ? await readConfig(resolve(values.config)) : {}) }
if (!Number.isSafeInteger(options.maxBudget) || options.maxBudget < 1 || options.maxBudget > 999999) {
  throw new Error('Invalid candidate budget')
}
const task = resolve(values.work)
const root = join(task, 'run')
await mkdir(task)
await mkdir(join(root, 'candidates'), { recursive: true })
await writeFile(join(task, 'task.json'), '{"program":"solver.mjs"}')
const signal = AbortSignal.timeout(60000)
const rows = []
const target = [3, -2, 1]
const program = weights => '// EVOLVE_START\nexport const weights = ' + JSON.stringify(weights)
  + '\n// EVOLVE_END\nexport const predict = row => weights.reduce((sum, x, i) => sum + x * row[i], 0)\n'
const filename = dir => join(dir, 'solver.mjs')
let used = 0
let nextLoop

async function candidate(index, source) {
  const id = 'c' + String(index).padStart(6, '0')
  const dir = join(root, 'candidates', id)
  await mkdir(dir)
  await writeFile(filename(dir), source)
  return { id, dir }
}

async function trial(item, seed, abortSignal) {
  abortSignal.throwIfAborted()
  const { predict } = await import(pathToFileURL(filename(item.dir)))
  let squared = 0
  for (let i = 1; i <= 11; i++) {
    const row = target.map((_, j) => Math.sin(i * (j + 2) + seed))
    const expected = row.reduce((sum, x, j) => sum + x * target[j], 0)
    squared += (predict(row) - expected) ** 2
  }
  return Number.isFinite(squared) ? 1 / (1 + squared / 11) : 0
}

const files = {
  async read(path) {
    try { return await readFile(join(root, path), 'utf8') } catch (error) {
      if (error.code !== 'ENOENT') throw error
    }
  },
  async write(path, data) {
    const dest = join(root, path)
    await mkdir(dirname(dest), { recursive: true })
    await writeFile(dest + '.tmp', data)
    await rename(dest + '.tmp', dest)
  },
}
const best = () => rows.reduce((a, b) => a.fitness >= b.fitness ? a : b)
const baselineLoop = {
  name: 'standalone-loop',
  async run(_args, service) {
    const base = await candidate(0, program([0, 0, 0]))
    const pop = service.population()
    await pop.append({ id: base.id, parent: null, fitness: await service.evaluate(base), survival: 'yes' })
    while (used < options.maxBudget) {
      signal.throwIfAborted()
      const parent = best().id
      const item = await service.mutate({ parent })
      await pop.append({ id: item.id, parent, fitness: await service.evaluate(item), survival: 'yes' })
    }
    return { best_id: best().id, best_fitness: best().fitness, remaining: 0 }
  },
}
const evolve = {
  files,
  getProvider: () => baselineLoop,
  register(_slot, provider) {
    nextLoop = provider
    return () => { nextLoop = undefined }
  },
  currentRun: () => ({ task, root, signal }),
  context: () => ({ task, root, budget: { max: options.maxBudget, remaining: options.maxBudget - used } }),
  population: () => ({
    rows: () => rows,
    async append(row) {
      rows.push(row)
      await files.write('population.json', JSON.stringify(rows, null, 2))
    },
  }),
  async allocate(parent) {
    signal.throwIfAborted()
    if (used >= options.maxBudget) throw new Error('Candidate budget exhausted')
    return candidate(++used, await readFile(filename(join(root, 'candidates', parent)), 'utf8'))
  },
  async mutate({ parent }) {
    const item = await this.allocate(parent)
    await this.spawnWorker(item.dir, '{}', { label: 'offline' })
    return item
  },
  async spawnWorker(dir, prompt, { label }) {
    const input = JSON.parse(prompt.split('\n').at(-1))
    const source = await readFile(filename(dir), 'utf8')
    const weights = JSON.parse(source.match(/^export const weights = (.+)$/m)[1])
    const residuals = weights.map((weight, index) => Math.abs(weight - target[index]))
    const index = residuals.indexOf(Math.max(...residuals))
    if (label.endsWith('-diagnose')) {
      return { text: JSON.stringify({ hypothesis: {
        claim: 'Coefficient ' + index + ' is underfit', evidence: ['Residual ' + residuals[index]],
        confidence: 0.9, test: 'Score predictions across paired instances',
      } }) }
    }
    const moves = input.plan?.components ?? []
    const coordinates = moves.length ? moves.map(move => Number(move.name.split('-').at(-1))) : [index]
    for (const i of coordinates) weights[i] += 0.3 * (target[i] - weights[i])
    await writeFile(filename(dir), program(weights))
    return { text: JSON.stringify({
      operator: { name: 'coordinate-' + coordinates[0], change: 'Shrink coefficient residual', scope: 'weights',
        components: moves.map(move => move.id) },
      mechanism: { confidence: 0.65, window: 6, directive: 'Use recent residual trends.' },
    }) }
  },
  async evaluate(item) {
    const fitness = await trial(item, 5, signal)
    await files.write('evals/' + item.id + '.json', JSON.stringify({ fitness, metrics: { seed: 5 } }))
    return fitness
  },
}

let ablationRuns = 0
const maxAblationRuns = options.maxAblationRuns ?? 30
async function inspectComposition({ parent, candidate: item, plan }) {
  const coordinates = plan.components.map(move => Number(move.name.split('-').at(-1)))
  const variants = [[], ...coordinates.map(index => [index]), coordinates.slice().reverse()]
  const required = (variants.length + 1) * 3
  if (ablationRuns + required > maxAblationRuns) return { stage: 'budget', required }
  ablationRuns += required
  const dir = join(root, 'candidates', parent)
  const original = JSON.parse((await readFile(filename(dir), 'utf8')).match(/^export const weights = (.+)$/m)[1])
  const seeds = [11, 29, 47]
  const measure = async variant => {
    let sum = 0
    for (const seed of seeds) sum += await trial(variant, seed, signal)
    return sum / seeds.length
  }
  const scores = []
  for (const [index, sequence] of variants.entries()) {
    const weights = [...original]
    for (const i of sequence) weights[i] += 0.3 * (target[i] - weights[i])
    const variantDir = join(root, 'ablations', item.id, String(index))
    await mkdir(variantDir, { recursive: true })
    await writeFile(filename(variantDir), program(weights))
    scores.push(await measure({ dir: variantDir }))
  }
  return { seeds, evaluations: required, components: plan.components.map(move => move.id),
    ...compareComposition(scores[0], scores.slice(1, -1), await measure(item), scores.at(-1)) }
}

const dispose = createPlugin({ ...options, trial, inspectComposition }).apply({ evolve })
try {
  const report = await nextLoop.run(options, evolve)
  await files.write('report.json', JSON.stringify(report, null, 2))
  console.log(JSON.stringify(report))
} finally {
  dispose()
}

