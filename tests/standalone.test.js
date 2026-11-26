import assert from 'node:assert/strict'
import { execFile } from 'node:child_process'
import { mkdtemp, readFile, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { promisify } from 'node:util'
import { fileURLToPath } from 'node:url'
import test from 'node:test'
import { name } from '../index.js'
import { allowance, reservePair } from '../budget.js'

test('limits candidate and pair allocations', async () => {
  assert.equal(allowance({ maxAttempts: 4, fraction: 0.4 }, 6), 2)
  const state = { pairs: 0 }
  let saved = 0
  assert.equal(await reservePair(state, 1, () => saved++), true)
  assert.equal(await reservePair(state, 1, () => saved++), false)
  assert.equal(saved, 1)
})

test('CLI executes a solver, validates paired seeds and persists artifacts', async t => {
  const tmp = await mkdtemp(join(tmpdir(), 'or-independent-'))
  t.after(() => rm(tmp, { recursive: true, force: true }))
  const task = join(tmp, 'demo')
  const entry = fileURLToPath(new URL('../run.js', import.meta.url))
  const { stdout } = await promisify(execFile)(process.execPath, [entry, '--work', task], { cwd: tmp })
  const result = JSON.parse(stdout)
  const read = async (path) => JSON.parse(await readFile(join(task, 'run', path), 'utf8'))
  const population = await read('population.json')
  const state = await read('or-operator/v' + name.split('-v')[1] + '.json')
  assert.equal(result.remaining, 0)
  assert.ok(result.best_fitness > population[0].fitness)
  assert.equal(population.length, 11)
  assert.ok(state.history.some(item => item.result.pairs?.length === 3))
  assert.ok(state.pairs <= 30)
  assert.ok(state.history.some(item => Number.isFinite(item.composition?.interaction)))
  assert.deepEqual(await read('report.json'), result)
})

