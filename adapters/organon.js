import { createPlugin } from '../index.js'
import { requireOrganon } from '../interfaces.js'
export function install(context, options) {
  requireOrganon(context.evolve)
  return createPlugin(options).apply(context)
}
