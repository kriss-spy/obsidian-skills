---
name: obsidian-plugin-performance-diagnose
description: Diagnose and attribute Obsidian performance issues to specific plugins. Use when the user suspects a plugin is causing slowdown, wants to measure per-plugin CPU or memory impact, or needs to isolate a performance regression to a specific community plugin without manual safe-mode toggling.
triggers:
  - obsidian plugin slow
  - obsidian plugin performance
  - obsidian plugin lag
  - obsidian plugin memory
  - obsidian plugin cpu
  - obsidian plugin bisect
  - obsidian plugin profile
  - obsidian plugin heavy
  - obsidian plugin impact
  - obsidian plugin isolate
  - obsidian plugin regression
  - obsidian plugin attribution
author: OpenCode
version: 1.0.0
created: 2026-06-04
---

# Obsidian Plugin Performance Diagnose

This skill is specifically for **attributing** Obsidian performance problems to individual plugins. Unlike general vault audits, it focuses on precise measurement, CPU profiling, and automated isolation of the culprit plugin.

## When to Use This Skill

- A specific plugin is suspected of causing performance degradation
- Obsidian startup is slow and the user wants to know which plugin is responsible
- Memory usage is unexpectedly high and leaking from a plugin
- UI lag or typing delay correlates with a plugin's activity
- The user wants to isolate a regression without manually toggling safe mode
- Performance profiling via Chrome DevTools is needed to see exact call-stack attribution

## Overview

Community plugins are the most common cause of Obsidian performance issues. This skill provides four methods of attribution, from coarse to precise:

1. **Coarse audit** — bundle sizes, known heavy plugins, manifest inspection
2. **Binary-search bisection** — disable half the plugins, test, re-enable half; isolate the culprit in O(log n) steps
3. **CDP CPU profiling** — capture a Chrome DevTools Protocol profile and map self-time back to plugin bundles
4. **Runtime monkey-patching** — wrap every method on every enabled plugin instance to clock exact wall time spent
5. **Memory attribution** — enable plugins one by one and measure heap delta

---

## Phase 0: Static Disk Analysis (When Obsidian Is Not Running)

When Obsidian is not running, CDP/CLI eval is unavailable. Use these shell commands to audit the vault statically. **Always filter by `community-plugins.json`.**

### List Enabled Plugins from Disk

```bash
# Correct: only enabled plugins
python3 -c "import sys,json; print('\n'.join(json.load(sys.stdin)))" \
  < /path/to/vault/.obsidian/community-plugins.json
```

### Check Enabled Plugin Data for Refresh Timers

```bash
enabled=$(python3 -c "import sys,json; print(' '.join(json.load(sys.stdin)))" < /path/to/vault/.obsidian/community-plugins.json)
for p in $enabled; do
  f="/path/to/vault/.obsidian/plugins/$p/data.json"
  if [ -f "$f" ]; then
    interval=$(python3 -c "import sys,json; d=json.load(sys.stdin); val=d.get('refreshInterval', d.get('autoSaveInterval', d.get('refreshSourceControlTimer', 'N/A'))); print(val)" < "$f" 2>/dev/null)
    if [ "$interval" != "N/A" ] && [ "$interval" != "0" ] && [ "$interval" != "None" ]; then
      echo "$p: $interval"
    fi
  fi
done | sort -t: -k2 -rn
```

> [!caution]
> Never use `.obsidian/plugins/*/data.json` without first filtering to enabled plugins via `community-plugins.json`. Disabled plugins leave `data.json` behind, causing false positives.

---

## Phase 1: Coarse Plugin Audit

Quick proxy metrics that require no external tools.

> [!important]
> **Always distinguish INSTALLED vs ENABLED plugins.** Obsidian keeps `data.json` files for disabled plugins too. If you are doing static filesystem analysis instead of CDP/CLI eval, you MUST cross-reference against `.obsidian/community-plugins.json`.
>
> | Approach | Filter to apply |
> |----------|----------------|
> | CDP / CLI `obsidian eval` (preferred) | `app.plugins.enabledPlugins` |
> | Static disk analysis (fallback) | `.obsidian/community-plugins.json` |
>
> **Incorrect** (will report disabled plugins as active):
> ```bash
> for f in .obsidian/plugins/*/data.json  # ❌ All 152 installed
> ```
> **Correct** (only examines enabled plugins):
> ```bash
> enabled=$(cat .obsidian/community-plugins.json | jq -r '.[]')
> for p in $enabled; do ... .obsidian/plugins/$p/data.json ... done
> ```

### Read Installed Plugin Manifests

```javascript
const enabled = app.plugins.enabledPlugins;
const manifests = Object.entries(app.plugins.manifests)
  .filter(([id]) => enabled.has(id))
  .map(([id, m]) => ({ id, name: m.name, version: m.version, author: m.author }));

console.log(`Enabled community plugins: ${manifests.length}`);
console.table(manifests);
```

### Estimate Plugin Bundle Sizes

Large `main.js` files indicate heavy plugins.

```javascript
const fs = require('fs');
const path = require('path');
const pluginDir = path.join(app.vault.adapter.getBasePath(), '.obsidian', 'plugins');

const enabled = [...app.plugins.enabledPlugins];
const sizes = enabled.map(id => {
  const mainPath = path.join(pluginDir, id, 'main.js');
  try {
    const stat = fs.statSync(mainPath);
    return { id, mainJsKB: (stat.size / 1024).toFixed(1) };
  } catch {
    return { id, mainJsKB: 'N/A' };
  }
}).sort((a, b) => parseFloat(b.mainJsKB || 0) - parseFloat(a.mainJsKB || 0));

console.table(sizes);
```

### Flag Known High-Impact Plugins

```javascript
const heavyIds = [
  'obsidian-excalidraw-plugin',   // Large canvas rendering
  'dataview',                     // Heavy query re-evaluation
  'obsidian-git',                 // Frequent disk / git ops
  'obsidian-languagetool-plugin', // Real-time linting
  'obsidian-style-settings',      // Large CSS injection
  'obsidian-outliner',            // Deep DOM manipulation
  'calendar',                     // Date-tree scanning
  'obsidian-kanban',              // Board rendering overhead
  'dbfolder',                     // Table views with many files
  'obsidian-hover-editor',        // Popover instantiation
];

const enabled = [...app.plugins.enabledPlugins];
const flagged = heavyIds.filter(id => enabled.includes(id));
console.log('Flagged heavy plugins:', flagged);
```

> [!important]
> These plugins are not inherently bad. They are known to be resource-intensive when used with large vaults or aggressive settings. Evaluate their impact before disabling.

---

## Phase 2: Binary-Search Bisection

Instead of disabling plugins one by one, bisect the set in O(log n) steps.

### Run a Bisection Step

```javascript
async function bisectPlugins() {
  const all = [...app.plugins.enabledPlugins];
  const half = Math.ceil(all.length / 2);
  const toDisable = all.slice(0, half);

  console.log(`Disabling ${toDisable.length} plugins:`, toDisable);
  for (const id of toDisable) {
    await app.plugins.disablePlugin(id);
  }

  console.log('Test performance now. If the issue is gone, the culprit is in the disabled set.');
  console.log('If the issue persists, the culprit is in the remaining enabled set.');
  console.log('Re-enable the innocent half and continue bisecting the suspect half.');
}

bisectPlugins();
```

### Re-enable a Plugin

```javascript
await app.plugins.enablePlugin('plugin-id-here');
```

### Disable a Single Plugin

```javascript
await app.plugins.disablePlugin('plugin-id-here');
```

> [!tip]
> Keep a log of each step so you can restore the original state when finished. Store the initial enabled set before starting:
> ```javascript
> const initialEnabled = [...app.plugins.enabledPlugins];
> ```

---

## Phase 3: CDP CPU Profiling (Precise Attribution)

When Obsidian is launched with `--remote-debugging-port=9222`, capture a CPU profile and attribute self-time to each plugin bundle.

### Capture Profile via CDP

```javascript
const CDP = require('chrome-remote-interface');

async function capturePluginProfile(durationMs = 5000) {
  const client = await CDP({ port: 9222 });
  const { Profiler } = client;

  await Profiler.enable();
  await Profiler.setSamplingInterval({ interval: 100 });

  console.log('Recording CPU profile...');
  await Profiler.start();

  await new Promise(r => setTimeout(r, durationMs));

  const { profile } = await Profiler.stop();
  await Profiler.disable();
  await client.close();

  const fs = require('fs');
  fs.writeFileSync('obsidian-cpu-profile.json', JSON.stringify(profile));
  console.log('Profile saved. Load into Chrome DevTools > Performance to inspect.');

  return profile;
}

capturePluginProfile();
```

### Automate Attribution from Profile

```javascript
function attributeProfileToPlugins(profile) {
  const pluginCosts = {};

  for (const node of profile.nodes) {
    const url = node.callFrame?.url || '';
    const pluginMatch = url.match(/plugins\/([^/]+)/);

    if (pluginMatch) {
      const pluginId = pluginMatch[1];
      const selfTime = node.selfTime || 0;
      pluginCosts[pluginId] = (pluginCosts[pluginId] || 0) + selfTime;
    }
  }

  return Object.entries(pluginCosts)
    .sort((a, b) => b[1] - a[1])
    .map(([id, time]) => ({
      plugin: id,
      selfTimeMs: (time / 1000).toFixed(2)
    }));
}

// Usage after capture:
// const results = attributeProfileToPlugins(profile);
// console.table(results);
```

> [!note]
> Plugin code appears in profiles as `webpack:///./.obsidian/plugins/<id>/main.js`. The attribution function maps these URLs back to plugin IDs and sums self-time.

---

## Phase 4: Runtime Monkey-Patching (Real-Time Attribution)

Wrap every method on every loaded plugin instance to measure exact wall time spent in each plugin's code.

### Instrument All Loaded Plugins

```javascript
function instrumentPlugins() {
  const measurements = {};
  const plugins = app.plugins;

  for (const pluginId of plugins.enabledPlugins) {
    const plugin = plugins.getPlugin(pluginId);
    if (!plugin) continue;

    measurements[pluginId] = {
      totalTime: 0,
      callCount: 0,
      methods: {}
    };

    const proto = Object.getPrototypeOf(plugin);
    const methods = Object.getOwnPropertyNames(proto).filter(
      name => typeof plugin[name] === 'function' && name !== 'constructor'
    );

    for (const method of methods) {
      const original = plugin[method].bind(plugin);
      measurements[pluginId].methods[method] = { time: 0, count: 0 };

      plugin[method] = async function(...args) {
        const t0 = performance.now();
        try {
          return await original(...args);
        } finally {
          const dt = performance.now() - t0;
          measurements[pluginId].totalTime += dt;
          measurements[pluginId].callCount++;
          measurements[pluginId].methods[method].time += dt;
          measurements[pluginId].methods[method].count++;
        }
      };
    }
  }

  return measurements;
}

const perfData = instrumentPlugins();

// After some usage, report:
setInterval(() => {
  console.table(
    Object.entries(perfData)
      .sort((a, b) => b[1].totalTime - a[1].totalTime)
      .map(([id, data]) => ({
        plugin: id,
        totalTimeMs: data.totalTime.toFixed(2),
        calls: data.callCount,
        avgMs: (data.totalTime / data.callCount).toFixed(2)
      }))
  );
}, 5000);
```

### Wrap Workspace Events from Plugins

```javascript
function instrumentWorkspaceEvents() {
  const eventCosts = {};
  const originalOn = app.workspace.on.bind(app.workspace);

  app.workspace.on = function(name, callback, ctx) {
    const wrapped = function(...args) {
      const t0 = performance.now();
      try {
        return callback.apply(ctx || this, args);
      } finally {
        const dt = performance.now() - t0;
        eventCosts[name] = (eventCosts[name] || 0) + dt;
      }
    };
    return originalOn(name, wrapped, ctx);
  };

  return eventCosts;
}

const eventPerf = instrumentWorkspaceEvents();
```

> [!caution]
> This cannot capture async work that escapes the wrapper (e.g., `setTimeout`, unawaited promises). It also adds a small overhead to every wrapped call. Use only for short diagnostic sessions.

---

## Phase 5: Memory Attribution (Heap Delta)

Enable plugins one by one and measure the JS heap delta to find memory-heavy or leaky plugins.

### Measure Per-Plugin Memory Impact

```javascript
async function measurePluginMemoryImpact() {
  const results = [];
  const allPlugins = [...app.plugins.enabledPlugins];

  // Disable all
  for (const id of allPlugins) {
    await app.plugins.disablePlugin(id);
  }

  if (global.gc) global.gc();

  for (const id of allPlugins) {
    const before = performance.memory?.usedJSHeapSize || 0;

    await app.plugins.enablePlugin(id);
    await new Promise(r => setTimeout(r, 2000)); // let plugin initialize

    if (global.gc) global.gc();

    const after = performance.memory?.usedJSHeapSize || 0;
    const deltaMB = ((after - before) / 1024 / 1024).toFixed(2);

    results.push({ plugin: id, heapDeltaMB: deltaMB });
    console.log(`${id}: +${deltaMB} MB`);

    await app.plugins.disablePlugin(id);
  }

  // Restore original state
  for (const id of allPlugins) {
    await app.plugins.enablePlugin(id);
  }

  return results;
}

measurePluginMemoryImpact();
```

> [!note]
> Requires Obsidian to be launched with `--js-flags="--expose-gc"`. Some plugins may not fully clean up on `disablePlugin`, so deltas can be conservative.

---

## Phase 6: Automated Remediation

Once the culprit is identified, apply fixes directly through the API.

### Disable a Suspected Heavy Plugin

```javascript
const heavy = ['obsidian-excalidraw-plugin', 'dataview'];
for (const id of heavy) {
  if (app.plugins.enabledPlugins.has(id)) {
    await app.plugins.disablePlugin(id);
    console.log('Disabled:', id);
  }
}
```

### Programmatically Disable a Single Plugin

```javascript
await app.plugins.disablePlugin('plugin-id-here');
```

### Programmatically Enable a Plugin

```javascript
await app.plugins.enablePlugin('plugin-id-here');
```

### Record Slow Operations (General Vault Wrapping)

```javascript
const slowOps = [];
const wrap = (obj, method, threshold = 50) => {
  const orig = obj[method].bind(obj);
  obj[method] = async (...args) => {
    const t0 = performance.now();
    const result = await orig(...args);
    const t1 = performance.now();
    if (t1 - t0 > threshold) {
      slowOps.push({ method, duration: (t1 - t0).toFixed(1), args: args.length });
    }
    return result;
  };
};

wrap(app.vault, 'read', 100);
console.log('Slow operations buffer initialized. Interact with vault, then inspect `slowOps`.');
```

---

## When to Ask the User

- **Subjective typing lag** — perceived responsiveness between keystroke and character render
- **Specific hardware constraints** — e.g., running on a low-RAM VM where the agent cannot inspect host specs
- **Network sync issues** — Sync performance depends on external network conditions and remote server state
- **OS-level interference** — antivirus scans, filesystem watchers, or OS indexing tools blocking the vault path

Everything else — plugin bundle sizes, CPU profiles, memory deltas, method timings — should be evaluated automatically.

---

## Quick Reference Checklist

- [ ] If Obsidian is NOT running, use Phase 0 static disk analysis with `community-plugins.json` filtering
- [ ] If Obsidian IS running, use CDP/CLI eval with `app.plugins.enabledPlugins` filtering
- [ ] **Verify:** Did you cross-reference against `community-plugins.json` before reading any `data.json`? (Prevent disabled plugin false positives)
- [ ] Run Phase 1 coarse audit (manifests, bundle sizes, flag heavy plugins)
- [ ] Run Phase 2 bisection if the culprit is unknown and there are many plugins
- [ ] Run Phase 3 CDP CPU profiling if Obsidian is on `--remote-debugging-port` and precise attribution is needed
- [ ] Run Phase 4 runtime monkey-patching if you need real-time method-level timings without external tools
- [ ] Run Phase 5 memory attribution if the issue is high memory usage or suspected leaks
- [ ] Apply Phase 6 remediation (disable culprit, restore innocent plugins)
- [ ] Ask user only for subjective lag reports or external factors (network, OS, hardware)

---

## References

- [How to Debug why Obsidian is running slowly](https://publish.obsidian.md/hub/04+-+Guides%2C+Workflows%2C+%26+Courses/Guides/How+to+debug+why+Obsidian+is+running+slowly)
- [Obsidian CLI Documentation](https://help.obsidian.md/cli)
- [Obsidian TypeScript API — Plugins](https://docs.obsidian.md/Reference/TypeScript+API/Plugins)
- [Chrome DevTools Protocol — Profiler](https://chromedevtools.github.io/devtools-protocol/tot/Profiler/)
- [Chrome DevTools Protocol — Runtime](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/)
- [Chrome DevTools Protocol — HeapProfiler](https://chromedevtools.github.io/devtools-protocol/tot/HeapProfiler/)
