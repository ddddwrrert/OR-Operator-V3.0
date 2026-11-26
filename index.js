import { createPlugin as base } from './plugin.js'
import { schedule } from './schedule.js'
import { mechanism } from './mechanism.js'
export { mechanism } from './mechanism.js'

export function createPlugin(options) {
  return base(options, { version: '3.0', schedule, mechanism })
}
export const { name, inject, apply } = createPlugin()

