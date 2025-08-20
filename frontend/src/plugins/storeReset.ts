// src/plugins/storeReset.ts
import type { PiniaPluginContext } from 'pinia'

// This array will store references to all Pinia store instances
const stores: any[] = []

// This plugin runs for every store when it's created
export function storeResetPlugin({ store }: PiniaPluginContext) {
  stores.push(store)
}

// Call this to reset all stores to their initial state
export function resetAllStores() {
  stores.forEach((store) => {
    if (typeof store.$reset === 'function') {
      store.$reset()
    }
  })
}