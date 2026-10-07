// Headless integration harness: real React, React Query, nanostores and jsdom.
// SDK registration/storage/REST/OS are bounded fixtures; no app or credentials.
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { createRequire } from 'node:module'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import vm from 'node:vm'

const [pluginPath, moduleDirectory] = process.argv.slice(2)
assert(pluginPath && moduleDirectory, 'Pass plugin.js and the existing desktop node_modules directory')
const require = createRequire(resolve(moduleDirectory, 'package.json'))
const load = spec => import(pathToFileURL(require.resolve(spec)).href)
const [React, ReactDOM, jsxRuntime, stores, storeReact, query, jsdom] = await Promise.all([
  load('react'), load('react-dom/client'), load('react/jsx-runtime'), load('nanostores'),
  load('@nanostores/react'), load('@tanstack/react-query'), load('jsdom')
])
const { act } = React
const { JSDOM } = jsdom
const dom = new JSDOM('<!doctype html><div id="root"></div>', { url: 'https://fixture.invalid' })
for (const name of ['window', 'document', 'HTMLElement', 'MouseEvent', 'Event']) globalThis[name] = dom.window[name]
globalThis.IS_REACT_ACT_ENVIRONMENT = true
const source = await readFile(pluginPath, 'utf8')
const KEY = ['plugin-provider-usage', 'backend']
const makeProvider = (id, name, percent) => ({ id, name, status: 'ok', windows: [{ label: '5h', percent }] })
const providers = [
  makeProvider('openrouter', 'OpenRouter', 98), makeProvider('openai-codex', 'OpenAI Codex', 85),
  makeProvider('anthropic', 'Anthropic', 91), makeProvider('nous', 'Nous', 99)
]
const observations = []

async function scenario(name, saved, expectation, input = providers) {
  const memory = structuredClone(saved)
  const writes = []
  const alerts = []
  const paths = []
  const client = new query.QueryClient({ defaultOptions: { queries: { gcTime: 0 } } })
  const context = vm.createContext({ console, setTimeout, clearTimeout, setInterval, clearInterval, document })
  const sdk = {
    STATUSBAR_AREAS: { right: 'statusBar.right' }, atom: stores.atom, useValue: storeReact.useStore,
    useQuery: query.useQuery, useQueryClient: query.useQueryClient
  }
  const imports = { '@hermes/plugin-sdk': sdk, react: React, 'react/jsx-runtime': jsxRuntime }
  const module = new vm.SourceTextModule(source, { context, identifier: pluginPath + ':' + name })
  await module.link(async spec => {
    assert(imports[spec], 'Unsupported plugin import: ' + spec)
    const exports = Object.entries(imports[spec])
    return new vm.SyntheticModule(exports.map(([key]) => key), function () {
      for (const [key, value] of exports) this.setExport(key, value)
    }, { context })
  })
  await module.evaluate()
  let contribution
  module.namespace.default.register({
    storage: {
      get: (key, fallback) => Object.hasOwn(memory, key) ? structuredClone(memory[key]) : fallback,
      set: (key, value) => { writes.push(key); memory[key] = structuredClone(value) }
    },
    rest: async path => {
      paths.push(path)
      return { fetched_at: '2026-10-01T00:00:00Z', providers: structuredClone(input) }
    },
    os: { notify: event => alerts.push(event) },
    register: value => { contribution = value.data }
  })
  assert(contribution, 'Plugin must register its real contribution')
  const root = ReactDOM.createRoot(document.getElementById('root'))
  const content = () => React.createElement(query.QueryClientProvider, { client },
    React.createElement('section', { 'data-surface': 'bar' }, contribution.detail),
    React.createElement('section', { 'data-surface': 'tooltip' }, contribution.title),
    React.createElement('section', { 'data-surface': 'popover' }, contribution.menuContent()))
  const surface = name => document.querySelector('[data-surface="' + name + '"]')
  try {
    await act(async () => { root.render(content()) })
    // Wait for the observed Query boundary, not a guessed number of microtasks.
    for (let attempt = 0; attempt < 100 && !surface('popover').textContent.includes('GPT'); attempt++) {
      await act(async () => { await new Promise(resolve => setTimeout(resolve, 10)) })
    }
    assert(client.getQueryData(KEY), 'Real React Query must resolve the REST fixture')
    const bar = surface('bar').textContent
    assert.equal(bar, expectation.bar, name + ': status bar')
    const titles = expectation.titles || ['GPT', 'Claude']
    for (const title of titles) {
      assert(surface('tooltip').textContent.includes(title), name + ': tooltip must include ' + title)
      assert(surface('popover').textContent.includes(title), name + ': popover must include ' + title)
    }
    if (!titles.includes('Claude')) assert(!surface('popover').textContent.includes('Claude'), 'No fabricated Claude account')
    for (const title of ['OpenRouter', 'Nous', 'openrouter', 'nous']) {
      assert(!document.getElementById('root').textContent.includes(title), name + ': hidden ' + title)
    }
    assert(paths.every(path => path === '/usage?fresh=1'), 'Underlying provider API route remains unchanged')
    if (Object.hasOwn(saved, 'barProviders')) assert.deepEqual(memory.barProviders, saved.barProviders)
    assert(!writes.includes('barProviders'), 'Binding must not overwrite a saved choice')
    if (expectation.toggle) {
      const hide = surface('popover').querySelector('button[aria-label="Hide from status bar"]')
      assert(hide, 'Existing eye toggle must remain usable')
      await act(async () => { hide.dispatchEvent(new MouseEvent('click', { bubbles: true })) })
      assert.deepEqual(memory.barProviders, expectation.afterToggle, 'Eye toggle preserves hidden saved ids')
    }
    assert(alerts.every(alert => alert.title.startsWith('GPT:') || alert.title.startsWith('Claude:')),
      'No notification from a hidden provider')
    const expectedAlerts = input.filter(p => ['openai-codex', 'anthropic'].includes(p.id) &&
      p.status === 'ok' && p.windows.some(w => w.percent >= 80)).length
    assert.equal(alerts.length, expectedAlerts, 'Configured threshold alerts actually run')
    if (expectation.remaining) {
      assert(surface('popover').textContent.includes('1m'), 'Saved poll interval')
      assert(surface('popover').textContent.includes('Remaining'), 'Saved value mode')
    }
    if (expectation.error) assert(surface('popover').textContent.includes('unavailable: fixture unavailable'))
    const refresh = surface('popover').querySelector('button[aria-label="Refresh usage"]')
    const before = paths.length
    await act(async () => {
      refresh.dispatchEvent(new MouseEvent('click', { bubbles: true }))
      await Promise.resolve()
    })
    assert(paths.length > before, 'Manual refresh must invoke actual plugin REST callback')
    assert(!surface('popover').textContent.includes('OpenRouter'), 'Refresh maintains filtering')
    observations.push({ name, bar, popover: titles, savedBar: memory.barProviders ?? null,
      restCalls: paths.length, alerts: alerts.length })
  } finally {
    await act(async () => root.unmount())
    client.clear()
  }
}

await scenario('fresh', {}, { bar: 'gpt 85% · claude 91%' })
await scenario('legacy-null', { barProviders: null }, { bar: 'gpt 85% · claude 91%' })
await scenario('explicit-empty', { barProviders: [] }, { bar: '' })
await scenario('claude-only', { barProviders: ['anthropic'] }, { bar: 'claude 91%' })
await scenario('mixed-hidden-choice', { barProviders: ['openrouter', 'openai-codex'] },
  { bar: 'gpt 85%', toggle: true, afterToggle: ['openrouter'] })
await scenario('hidden-only-choice', { barProviders: ['openrouter'] }, { bar: '' })
await scenario('saved-mode-cadence', { valueMode: 'remaining', intervalMs: 60000 },
  { bar: 'gpt 15% · claude 9%', remaining: true })
await scenario('unavailable-claude', {}, { bar: 'gpt 85% · claude -', error: true },
  [providers[0], providers[1], { id: 'anthropic', name: 'Anthropic', status: 'error', error: 'fixture unavailable' }, providers[3]])
await scenario('unconfigured-claude', {}, { bar: 'gpt 85%', titles: ['GPT'] }, [providers[0], providers[1], providers[3]])
console.log(JSON.stringify({ checks: observations.length, scenarios: observations }))
dom.window.close()
