export function requireOrganon(service) {
  for (const key of ['register','getProvider','context','currentRun','population','allocate','evaluate','spawnWorker']) {
    if (typeof service?.[key] !== 'function') throw new TypeError('Missing service method: ' + key)
  }
}
