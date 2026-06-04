---
name: obsidian-performance
description: Diagnose and optimize Obsidian vault performance issues programmatically using CDP/CLI eval, the Obsidian API, and Chrome DevTools. Covers vault structure, configuration, metadata health, and general CDP monitoring. For precise per-plugin CPU/memory attribution and plugin bisection, use the obsidian-plugin-performance-diagnose skill.
triggers:
  - obsidian slow
  - obsidian performance
  - obsidian lag
  - obsidian startup slow
  - obsidian high memory
  - obsidian typing lag
  - obsidian vault audit
  - obsidian optimize vault
  - obsidian unresponsive
  - obsidian debug performance
  - obsidian heap snapshot
  - obsidian metadata health
  - obsidian broken links
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Performance

This skill treats performance diagnostics as a programmatic audit. Instead of guiding the user through manual UI clicks, the agent evaluates JavaScript directly in Obsidian's runtime (via CDP `Runtime.evaluate` or CLI `obsidian eval`) to inspect vault state, plugin impact, configuration, and metadata health. Fixes are applied through the same APIs.

## When to Use This Skill

- Obsidian startup is slow or getting slower over time
- The app feels laggy during typing, switching notes, or rendering
- Memory usage is unexpectedly high
- A specific plugin is suspected of causing performance degradation
- The vault has grown large and the user wants an automated health audit
- Console errors or warnings appear repeatedly
- The user wants to identify and fix broken links, orphans, or circular references
- Performance profiling via Chrome DevTools is needed

## Overview

Obsidian performance issues usually stem from one of four sources:

1. **Vault structure** — root clutter, orphaned attachments, or an excessive file count
2. **Configuration** — hardware acceleration conflicts, live preview overhead, or overly broad file inclusion
3. **Metadata integrity** — broken links, circular references, or unresolved cache entries forcing repeated re-indexing
4. **Community plugins** — heavy plugins scanning the entire vault, live-preview enhancers, or canvas/Excalidraw integrations

> [!note]
> Plugin-specific diagnosis, bisection, CPU profiling, and per-plugin memory attribution are handled by the **obsidian-plugin-performance-diagnose** skill. This skill focuses on vault health, configuration, metadata, and general CDP monitoring.

This skill provides CDP/CLI-evaluable code for each phase. Run the snippets directly in Obsidian's context and act on the results.

---

## Phase 1: Programmatic Vault Audit

Evaluate these snippets via CDP/CLI to get quantitative vault health metrics.

### Count Files by Type

```javascript
const files = app.vault.getAllLoadedFiles();
const markdown = files.filter(f => f.extension === 'md');
const attachments = files.filter(f => !f.extension === 'md' && f instanceof require('obsidian').TFile);
const folders = files.filter(f => f instanceof require('obsidian').TFolder);

console.table({
  totalFiles: files.length,
  markdownFiles: markdown.length,
  attachmentFiles: attachments.length,
  folders: folders.length
});
```

### Measure Total Vault Size

```javascript
const { exec } = require('child_process');
const path = app.vault.adapter.getBasePath();
exec(`du -sh "${path}"`, (err, stdout) => {
  console.log('Vault size:', stdout.trim());
});
```

> [!tip]
> On Windows, use `powershell -Command "(Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum"` instead of `du`.

### Detect Root Clutter

Files directly in the vault root slow down indexing because Obsidian must evaluate each one against inclusion rules.

```javascript
const root = app.vault.getRoot();
const rootFiles = root.children.filter(c => c instanceof require('obsidian').TFile);
const rootFolders = root.children.filter(c => c instanceof require('obsidian').TFolder);

console.log(`Root files: ${rootFiles.length}`);
console.log(`Root folders: ${rootFolders.length}`);
console.log('Root file names:', rootFiles.map(f => f.name));
```

> [!caution]
> More than ~50 files in the root is a strong signal for performance degradation. Consolidate into folders.

### List Largest Files

```javascript
const files = app.vault.getFiles().sort((a, b) => b.stat.size - a.stat.size);
console.table(files.slice(0, 20).map(f => ({
  path: f.path,
  sizeBytes: f.stat.size,
  sizeMB: (f.stat.size / 1024 / 1024).toFixed(2)
})));
```

### Find Orphaned Attachments

Attachments not referenced by any markdown file waste space and indexing time.

```javascript
const allFiles = app.vault.getFiles();
const mdFiles = allFiles.filter(f => f.extension === 'md');
const attachments = allFiles.filter(f => f.extension !== 'md');

// Build a set of referenced attachment basenames (approximate)
const referenced = new Set();
for (const file of mdFiles) {
  const content = await app.vault.cachedRead(file);
  for (const att of attachments) {
    if (content.includes(att.basename)) referenced.add(att.path);
  }
}

const orphans = attachments.filter(a => !referenced.has(a.path));
console.log(`Orphaned attachments: ${orphans.length}`);
console.table(orphans.map(o => ({ path: o.path, sizeMB: (o.stat.size / 1024 / 1024).toFixed(2) })));
```

---

## Phase 2: Programmatic Config Audit

Read `app.json` and workspace state to identify problematic settings.

### Read Core Settings

```javascript
const fs = require('fs');
const path = require('path');
const configPath = path.join(app.vault.adapter.getBasePath(), '.obsidian', 'app.json');
const appJson = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

console.table({
  hardwareAcceleration: appJson.hardwareAcceleration,
  livePreview: appJson.livePreview,
  attachmentFolderPath: appJson.attachmentFolderPath,
  newFileLocation: appJson.newFileLocation,
  newLinkFormat: appJson.newLinkFormat,
  useMarkdownLinks: appJson.useMarkdownLinks,
  excludedFiles: (appJson.userIgnoreFilters || []).length
});
```

### Check Workspace Complexity

Too many open leaves and splits increase DOM weight and memory pressure.

```javascript
let leafCount = 0;
let splitCount = 0;

function countItems(item) {
  if (item.children) {
    splitCount++;
    item.children.forEach(countItems);
  } else if (item.view) {
    leafCount++;
  }
}

countItems(app.workspace.rootSplit);

console.table({
  leaves: leafCount,
  splits: splitCount,
  deferredLeaves: app.workspace.getLeavesOfType('empty').filter(l => l.isDeferred).length
});
```

### Check Excluded Files List

```javascript
const excluded = app.vault.config?.userIgnoreFilters || [];
console.log('Excluded patterns:', excluded);
```

> [!note]
> If large folders (backups, `.git`, node_modules, attachment dumps) are not excluded, Obsidian indexes them unnecessarily.

---

## Phase 3: Metadata & Link Health

The metadata cache drives graph view, backlinks, and Dataview. Broken or circular links force re-resolution and slow editing.

### Inspect Resolved and Unresolved Links

```javascript
const resolved = app.metadataCache.resolvedLinks;
const unresolved = app.metadataCache.unresolvedLinks;

let resolvedCount = 0;
let unresolvedCount = 0;

for (const file of Object.keys(resolved)) {
  resolvedCount += Object.keys(resolved[file]).length;
}
for (const file of Object.keys(unresolved)) {
  unresolvedCount += Object.keys(unresolved[file]).length;
}

console.table({ resolvedCount, unresolvedCount });
```

### List All Broken Links

```javascript
const unresolved = app.metadataCache.unresolvedLinks;
const broken = [];

for (const [sourcePath, targets] of Object.entries(unresolved)) {
  for (const target of Object.keys(targets)) {
    broken.push({ source: sourcePath, brokenLink: target, count: targets[target] });
  }
}

console.log(`Total broken link references: ${broken.length}`);
console.table(broken.slice(0, 30));
```

### Detect Circular References

A simple depth-limited traversal detects obvious circular wikilink chains.

```javascript
const resolved = app.metadataCache.resolvedLinks;
const files = Object.keys(resolved);

function hasCircular(start, current, depth, visited) {
  if (depth > 10) return false;
  if (visited.has(current)) return current === start;
  visited.add(current);
  const neighbors = Object.keys(resolved[current] || {});
  for (const n of neighbors) {
    if (hasCircular(start, n, depth + 1, new Set(visited))) return true;
  }
  return false;
}

const circular = [];
for (const file of files.slice(0, 500)) { // sample first 500
  if (hasCircular(file, file, 0, new Set())) circular.push(file);
}
console.log(`Potential circular references found: ${circular.length}`);
console.log(circular.slice(0, 20));
```

> [!caution]
> Circular references are not always harmful, but deep cycles can cause stack issues in plugins that recursively traverse links.

---

## Phase 4: Automated Fixes

Apply fixes directly through the Obsidian API. Do not ask the user to open Settings and click around.

### Exclude an Attachment Folder

```javascript
const current = app.vault.config.userIgnoreFilters || [];
if (!current.includes('Attachments')) {
  app.vault.setConfig('userIgnoreFilters', [...current, 'Attachments']);
}
```

### Close Deferred or Unused Leaves

```javascript
const leaves = app.workspace.getLeavesOfType('empty');
for (const leaf of leaves) {
  if (leaf.isDeferred || !leaf.view?.file) {
    leaf.detach();
  }
}
```

### Consolidate Root Files into a Folder

```javascript
const root = app.vault.getRoot();
const rootFiles = root.children.filter(c => c instanceof require('obsidian').TFile);
const inboxPath = 'Inbox';

// Ensure Inbox exists
if (!app.vault.getAbstractFileByPath(inboxPath)) {
  await app.vault.createFolder(inboxPath);
}

for (const file of rootFiles) {
  const newPath = `${inboxPath}/${file.name}`;
  if (!app.vault.getAbstractFileByPath(newPath)) {
    await app.vault.rename(file, newPath);
  }
}
```

> [!important]
> Always verify that the destination path does not already exist before calling `vault.rename()` to avoid overwrites.

---

## Phase 5: Performance Monitoring via CDP

When Obsidian is running in an Electron environment with remote debugging enabled, use Chrome DevTools Protocol (CDP) for deeper profiling.

> [!note]
> For per-plugin CPU profiling and attribution, use the **obsidian-plugin-performance-diagnose** skill, which provides CDP `Profiler` domain snippets and automated profile-to-plugin mapping.

### Capture Startup Timeline

```javascript
// CDP Runtime.evaluate via CLI or remote debugger
// Record a performance profile snippet:

const start = performance.now();
// Trigger a targeted action, e.g. open a large note:
const file = app.vault.getAbstractFileByPath('Large Note.md');
if (file) {
  const leaf = app.workspace.getLeaf('tab');
  await leaf.openFile(file);
}
const end = performance.now();
console.log(`Open duration: ${(end - start).toFixed(2)}ms`);
```

### Scrape Console Errors

Enable CDP `Runtime.consoleAPICalled` and filter for errors:

```javascript
// Evaluated inside Obsidian via CDP:
const errors = [];
const originalError = console.error;
console.error = (...args) => {
  errors.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
  originalError.apply(console, args);
};

// After a short period, inspect `errors`:
console.log('Captured errors:', errors.length);
errors.slice(0, 20).forEach(e => console.log(e));
```

### Take a Memory Heap Snapshot

If the remote debugger exposes `HeapProfiler`, trigger a snapshot and stream it:

```javascript
// Requires CDP HeapProfiler domain enabled
// Via CLI wrapper or remote debugger:
// { method: 'HeapProfiler.takeHeapSnapshot', params: { reportProgress: true } }

// Alternatively, estimate heap growth from JS:
let heapBefore = 0;
if (performance.memory) {
  heapBefore = performance.memory.usedJSHeapSize;
  // trigger heavy operation
  await app.vault.cachedRead(app.vault.getFiles()[0]);
  const heapAfter = performance.memory.usedJSHeapSize;
  console.log(`Heap delta: ${((heapAfter - heapBefore) / 1024 / 1024).toFixed(2)} MB`);
}
```

> [!note]
> `performance.memory` is only available in Chromium contexts with `--enable-precise-memory-info`. Use CDP `Runtime.getHeapUsage()` if the flag is not set.

### Record Slow Operations

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

// Example: wrap vault read
wrap(app.vault, 'read', 100);
// wrap(app.metadataCache, 'getFileCache', 50); // if writable

console.log('Slow operations buffer initialized. Interact with vault, then inspect `slowOps`.');
```

---

## When to Ask the User

The agent should ask the user only for information that cannot be measured programmatically:

- **Subjective typing lag** — perceived responsiveness between keystroke and character render
- **Specific hardware constraints** — e.g., running on a low-RAM VM where the agent cannot inspect host specs
- **Network sync issues** — Sync performance depends on external network conditions and remote server state
- **OS-level interference** — antivirus scans, filesystem watchers, or OS indexing tools blocking the vault path
- **Battery / thermal throttling** — mobile or laptop power-state changes affecting Electron render performance

Everything else — file counts, link health, settings values, memory deltas — should be evaluated automatically.

---

## Common Performance Fixes Table

| Symptom | Likely Cause | Programmatic Fix |
|---------|-------------|------------------|
| Slow startup | Large deferred tab count or vault structure | Close deferred leaves; consolidate root files |
| Typing lag | Live preview overhead or vault config | Toggle `livePreview` off temporarily via `app.vault.setConfig` |
| Search is slow | Large vault with un-excluded folders | Add attachment/backup folders to `userIgnoreFilters` |
| Graph view crashes | Excessive links or circular references | Resolve broken links; filter graph by path; reduce metadata cache pressure |
| High memory usage | Many open leaves or large vault | Close unused leaves; consolidate root files |
| Sync is slow | Many small files or root clutter | Consolidate notes into folders; compress or externalize large attachments |
| UI stutter during layout | Complex split tree with many leaves | Detach empty leaves; reduce split nesting |
| Repeated console errors | Plugin or core misconfiguration | Inspect `console.error` buffer for stack trace; use obsidian-plugin-performance-diagnose for plugin attribution |

---

## Quick Reference Checklist

- [ ] Run Phase 1 vault audit (file counts, root clutter, largest files, orphans)
- [ ] Run Phase 2 config audit (hardware acceleration, live preview, workspace complexity, excluded files)
- [ ] Run Phase 3 metadata audit (resolved/unresolved counts, broken links, circular references)
- [ ] Apply Phase 4 automated fixes (exclude folders, close deferred leaves, consolidate root)
- [ ] Run Phase 5 CDP profiling if issue persists (heap delta, console errors, slow operation wrapping)
- [ ] If plugins are suspected, delegate to the obsidian-plugin-performance-diagnose skill
- [ ] Ask user only for subjective lag reports or external factors (network, OS, hardware)

---

## References

- [How to Debug why Obsidian is running slowly](https://publish.obsidian.md/hub/04+-+Guides%2C+Workflows%2C+%26+Courses/Guides/How+to+debug+why+Obsidian+is+running+slowly)
- [Obsidian CLI Documentation](https://help.obsidian.md/cli)
- [Obsidian TypeScript API — Vault](https://docs.obsidian.md/Reference/TypeScript+API/Vault)
- [Obsidian TypeScript API — MetadataCache](https://docs.obsidian.md/Reference/TypeScript+API/MetadataCache)
- [Obsidian TypeScript API — Workspace](https://docs.obsidian.md/Reference/TypeScript+API/Workspace)
- [Obsidian TypeScript API — Plugins](https://docs.obsidian.md/Reference/TypeScript+API/Plugins)
- [Chrome DevTools Protocol — Runtime](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/)
- [Chrome DevTools Protocol — HeapProfiler](https://chromedevtools.github.io/devtools-protocol/tot/HeapProfiler/)
