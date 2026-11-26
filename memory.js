export async function openMemory(files, path) {
  const state = JSON.parse(await files.read(path) ?? '{"attempts":0,"pairs":0,"history":[]}')
  if (!Array.isArray(state.history) || ![state.attempts, state.pairs].every(n => Number.isSafeInteger(n) && n >= 0)) {
    throw new Error('Invalid operator memory: ' + path)
  }
  return { state, save: () => files.write(path, JSON.stringify(state, null, 2) + '\n') }
}
