import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { cp, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import test from 'node:test'

const original = resolve(process.env.ORGANON_ROOT ?? fileURLToPath(new URL('../../../Organon（原）', import.meta.url)))
const pluginDir = join(original, 'plugins', 'dsh-evolve-loop')
const { Evolve } = await import(pathToFileURL(join(pluginDir, 'src', 'evolve.js')))

function fixtureContext() {
  return {
    get(name) {
      if (name !== 'subprocess') return undefined
      return {
        resolveExecutable: async () => 'python',
        spawn({ argv, cwd, env, signal }) {
          signal.throwIfAborted()
          const [executable, ...args] = argv
          const result = spawnSync(executable, args, { cwd, env: { ...process.env, ...env }, encoding: 'utf8', timeout: 15000 })
          const stream = value => ({ readFrom: () => ({ text: value ?? '' }) })
          return { done: Promise.resolve({ exitCode: result.status }),
            collected: { stdout: stream(result.stdout), stderr: stream(result.stderr) } }
        },
      }
    },
    subagents: {
      getProvider: () => ({}),
      async start(_name, request) {
        const match = request.confine.root.match(/c(\d{6})$/)
        const next = Number(match[1])
        const dir = request.confine.root
        const file = join(dir, 'solution.py')
        const source = await readFile(file, 'utf8')
        const input = JSON.parse(request.prompt[0].text.split('\n').at(-1))
        const report = {
          hypothesis: { claim: 'Current construction stalls', evidence: ['constant permitted improvement'], confidence: 0.9, test: 'score' },
          operator: { name: 'move-' + next, change: 'improve constant', scope: 'fixture',
            components: input.plan?.components?.map(item => item.id) ?? [] },
          mechanism: { confidence: 0.7, window: 5, directive: 'Compare candidate trajectories' },
        }
        const update = source.replace(/^VALUE = \d+/m, 'VALUE = ' + (next === 1 ? 9 : 10 + next))
        if (!request.label?.endsWith('-diagnose')) await writeFile(file, update)
        return { result: Promise.resolve({ output: [{ type: 'text', text: JSON.stringify(report) }] }),
          dispose() {} }
      },
    },
  }
}

for (const version of ['3.0']) {
  test('V' + version + ' runs the original loop, allocation, evaluator and population', async t => {
    const task = await mkdtemp(join(tmpdir(), 'or-operator-'))
    t.after(() => rm(task, { recursive: true, force: true }))
    await cp(join(pluginDir, 'tests', 'fixtures', 'task'), task, { recursive: true })
    const { createPlugin } = await import('../index.js')
    const ctx = fixtureContext()
    ctx.evolve = new Evolve(ctx)
    const trial = async (item, seed) => {
      const run = spawnSync('python', [join(item.dir, 'solution.py')], { encoding: 'utf8' })
      assert.equal(run.status, 0)
      return Number(run.stdout.trim()) + seed / 100
    }
    const uninstall = createPlugin({ stagnation: 0, fraction: 1, trial }).apply(ctx)
    const exec = { agent: { session: { header: { cwd: task } } } }
    const first = await ctx.evolve.run({ maxBudget: 8, candidates: 1 }, exec)
    assert.deepEqual(first, { best_id: 'c000000', best_fitness: 10, remaining: 7 })
    const result = await ctx.evolve.run({ maxBudget: 8 }, exec)
    assert.deepEqual(result, { best_id: 'c000008', best_fitness: 18, remaining: 0 })
    const run = join(task, 'run')
    const state = JSON.parse(await readFile(join(run, 'or-operator', 'v' + version + '.json')))
    assert.equal(state.attempts, 8)
    assert.equal(state.pairs, 21)
    assert.equal(state.history[7].result.stage, 'paired-confirmation')
    assert.equal(state.history[0].result.accepted, false)
    assert.equal(state.history[0].result.fitness, 9)
    const rows = (await readFile(join(run, 'population.jsonl'), 'utf8')).trim().split('\n').map(JSON.parse)
    assert.equal(rows[1].survival, 'no')
    assert.equal(rows[1].fitness, 0)
    assert.equal(state.history[7].result.accepted, true)
    if (version !== '1.01') assert.ok(state.history.some(item => item.plan.kind === 'compose'))
    if (version === '3.0') assert.ok(state.mechanismDecisions.length > 0)
    uninstall()
    assert.equal(ctx.evolve.getProvider('loop').name, 'evolve-loop')
  })
}

