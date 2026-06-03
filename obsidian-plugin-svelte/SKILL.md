---
name: obsidian-plugin-svelte
description: Integrate Svelte into Obsidian plugins. Covers build configuration (esbuild), mounting Svelte components in ItemViews, Modals, and Settings tabs, reactive state bridging, and lifecycle cleanup. Use when adding Svelte UI to an Obsidian plugin or converting vanilla DOM code to Svelte components.
triggers:
  - obsidian plugin svelte
  - obsidian svelte integration
  - obsidian svelte component
  - obsidian svelte build
  - obsidian svelte esbuild
  - obsidian svelte view
  - obsidian svelte modal
  - obsidian svelte settings
  - obsidian plugin mount svelte
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Svelte Integration

This skill guides you through adding Svelte components to an Obsidian plugin. It covers build system configuration, mounting components inside Obsidian's UI surfaces, bridging reactive state between the plugin and Svelte, and cleaning up on unload to prevent memory leaks.

## When to Use This Skill

- Adding Svelte UI components to an existing Obsidian plugin
- Configuring esbuild (or Rollup) to compile `.svelte` files
- Mounting Svelte inside an `ItemView`, `Modal`, or `PluginSettingTab`
- Bridging Obsidian plugin state / events into Svelte props or stores
- Converting vanilla DOM manipulation to reactive Svelte components
- Troubleshooting Svelte TypeScript or build issues in an Obsidian plugin

## Overview

Svelte compiles components to vanilla JavaScript at build time, so plugins incur minimal runtime overhead. In an Obsidian plugin, the typical flow is:

1. **Configure the build** — teach esbuild to compile `.svelte` files with `esbuild-svelte` and `svelte-preprocess`
2. **Write a `.svelte` component** — TypeScript-enabled via `<script lang="ts">`
3. **Mount it on an HTML element** — `mount()` (Svelte 5) or `new Component()` (Svelte 4) onto a DOM node provided by Obsidian (`this.contentEl`, `this.containerEl`, etc.)
4. **Bridge state** — pass props or use Svelte stores to share plugin state
5. **Unmount on close/unload** — call `unmount()` or `$destroy()` to release the component

---

## Setting Up Svelte

### Prerequisites

- An existing Obsidian plugin project (see `obsidian-plugin-bootstrap` if you need to scaffold one)
- **TypeScript 5.0+** — Svelte requires at least TS 5.0
- **Node.js** LTS (v18+)

### Installing Dependencies

Install the Svelte compiler, preprocessor, and esbuild plugin:

```bash
npm install --save-dev svelte svelte-preprocess esbuild-svelte svelte-check
```

> [!info]
> If the project is on an older TypeScript version, upgrade first:
> ```bash
> npm install typescript@~5.0.0
> ```

**Package roles:**

| Package | Purpose |
|---------|---------|
| `svelte` | Core compiler and runtime |
| `svelte-preprocess` | TypeScript / SCSS preprocessing inside `.svelte` files |
| `esbuild-svelte` | esbuild plugin that invokes the Svelte compiler |
| `svelte-check` | CLI type-checker for `.svelte` files |

### TypeScript Configuration

Extend `tsconfig.json` to include Svelte files and enable settings required by `svelte-preprocess` and `svelte-check`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "inlineSourceMap": true,
    "inlineSources": true,
    "module": "ESNext",
    "target": "ES6",
    "allowJs": true,
    "noImplicitAny": true,
    "moduleResolution": "node",
    "importHelpers": true,
    "isolatedModules": true,
    "strictNullChecks": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true
  },
  "include": [
    "**/*.ts",
    "**/*.svelte"
  ]
}
```

**Key additions:**
- `verbatimModuleSyntax` — required by `svelte-preprocess`
- `skipLibCheck` — required for `svelte-check` to work correctly
- `"**/*.svelte"` in `include` — ensures TypeScript sees Svelte components

### esbuild Configuration

Import the Svelte plugin and preprocessor in `esbuild.config.mjs`, then add it to the plugins array:

```js
import esbuild from "esbuild";
import process from "process";
import builtins from "builtin-modules";

import esbuildSvelte from 'esbuild-svelte';
import { sveltePreprocess } from 'svelte-preprocess';

const prod = process.argv[2] === "production";

const context = await esbuild.context({
  banner: {
    js: "",
  },
  entryPoints: ["main.ts"],
  bundle: true,
  external: [
    "obsidian",
    "electron",
    "@codemirror/autocomplete",
    "@codemirror/collab",
    "@codemirror/commands",
    "@codemirror/language",
    "@codemirror/lint",
    "@codemirror/search",
    "@codemirror/state",
    "@codemirror/view",
    "@lezer/common",
    "@lezer/highlight",
    "@lezer/lr",
    ...builtins,
  ],
  format: "cjs",
  target: "es2018",
  logLevel: "info",
  sourcemap: prod ? false : "inline",
  treeShaking: true,
  outfile: "main.js",
  plugins: [
    esbuildSvelte({
      compilerOptions: { css: 'injected' },
      preprocess: sveltePreprocess(),
    }),
  ],
});

if (prod) {
  await context.rebuild();
  process.exit(0);
} else {
  await context.watch();
}
```

**Important details:**
- `compilerOptions: { css: 'injected' }` — inlines component `<style>` blocks into the JavaScript bundle so Obsidian loads them automatically. Do not emit a separate CSS file unless you handle copying it manually.
- `preprocess: sveltePreprocess()` — enables `<script lang="ts">` and other preprocessors
- Keep `format: "cjs"` and the same `external` array as a standard plugin; Svelte itself is bundled, Obsidian APIs are not

### Add svelte-check Script

Add a type-checking script to `package.json`:

```json
{
  "scripts": {
    "dev": "node esbuild.config.mjs",
    "build": "tsc -noEmit -skipLibCheck && node esbuild.config.mjs production",
    "svelte-check": "svelte-check --tsconfig tsconfig.json"
  }
}
```

Run it alongside `tsc` before builds:

```bash
npm run svelte-check
```

---

## Creating a Svelte Component

Create a file named `Counter.svelte` in your project root (or under `src/components/`):

```svelte
<script lang="ts">
  interface Props {
    startCount: number;
  }

  let { startCount }: Props = $props();
  let count = $state(startCount);

  export function increment() {
    count += 1;
  }
</script>

<div class="number">
  <span>My number is {count}!</span>
  <button onclick={increment}>Increment</button>
</div>

<style>
  .number {
    color: var(--text-normal);
    padding: 1rem;
  }
  button {
    margin-left: 0.5rem;
  }
</style>
```

> [!tip]
> The official Obsidian docs recommend Svelte 5 runes (`$props`, `$state`). If you are on Svelte 4, use `export let startCount: number` for props and reactive declarations with `$:`.

---

## Mounting Svelte Components in Obsidian UI

Svelte components must be attached to an existing DOM element. Obsidian provides several mount targets:

| Mount Target | Property / Method | Use Case |
|--------------|-------------------|----------|
| `ItemView` content | `this.contentEl` | Custom pane views |
| `Modal` content | `this.contentEl` | Modal dialogs |
| `PluginSettingTab` | `this.containerEl` | Plugin settings UI |
| Status bar | `this.addStatusBarItem()` | Status bar indicators |
| Ribbon icon | `this.addRibbonIcon()` | Sidebar button panels |

### Mount API (Svelte 5)

```typescript
import { mount, unmount } from 'svelte';
import Counter from './Counter.svelte';

const counter = mount(Counter, {
  target: htmlElement,
  props: { startCount: 5 },
});

// Later, to destroy:
unmount(counter);
```

### Legacy Mount API (Svelte 4)

```typescript
import Counter from './Counter.svelte';

const counter = new Counter({
  target: htmlElement,
  props: { startCount: 5 },
});

// Later, to destroy:
counter.$destroy();
```

> [!note]
> If you are maintaining a plugin that must support both Svelte 4 and 5, keep the legacy `new Component()` pattern. Svelte 5 offers a compatibility mode if you migrate gradually.

---

## Props and Reactivity

### Passing Props from Obsidian to Svelte

The simplest way to push data into a component is via the `props` option at mount time:

```typescript
this.counter = mount(Counter, {
  target: this.contentEl,
  props: {
    startCount: this.settings.defaultCount,
  },
});
```

If the data changes after mount, you have two choices:
1. **Lift state into a Svelte store** and subscribe inside the component
2. **Re-mount** the component (expensive; avoid if possible)

### Using Svelte Stores for Global Plugin State

When many components need access to the plugin instance, settings, or vault data, a Svelte store avoids prop drilling.

**`store.ts`:**

```typescript
import { writable } from 'svelte/store';
import type MyPlugin from './main';

export const pluginStore = writable<MyPlugin | undefined>(undefined);
```

**Set the store when the view opens:**

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';
import type MyPlugin from './main';
import { pluginStore } from './store';
import Dashboard from './Dashboard.svelte';
import { mount, unmount } from 'svelte';

export const VIEW_TYPE_DASHBOARD = 'dashboard-view';

export class DashboardView extends ItemView {
  private component: ReturnType<typeof Dashboard> | undefined;

  constructor(leaf: WorkspaceLeaf, private plugin: MyPlugin) {
    super(leaf);
  }

  getViewType() { return VIEW_TYPE_DASHBOARD; }
  getDisplayText() { return 'Dashboard'; }

  async onOpen() {
    pluginStore.set(this.plugin);
    this.component = mount(Dashboard, {
      target: this.contentEl,
    });
  }

  async onClose() {
    if (this.component) {
      unmount(this.component);
    }
  }
}
```

**Consume the store in a component:**

```svelte
<script lang="ts">
  import type MyPlugin from './main';
  import { pluginStore } from './store';

  let plugin: MyPlugin | undefined;
  pluginStore.subscribe((p) => { plugin = p; });
</script>

{#if plugin}
  <p>Vault name: {plugin.app.vault.getName()}</p>
{/if}
```

> [!tip]
> Svelte automatically unsubscribes from a store when the component is destroyed, so you rarely need manual cleanup for subscriptions.

### Bridging Obsidian Events to Svelte Reactivity

Obsidian events (vault changes, file open, metadata cache updates) live outside Svelte's reactivity system. Bridge them by updating a writable store inside an event handler:

```typescript
// In your plugin class
async onload() {
  const fileStore = writable<TFile | null>(null);

  this.registerEvent(
    this.app.workspace.on('file-open', (file: TFile | null) => {
      fileStore.set(file);
    })
  );

  // Expose the store to components via a module-level export or plugin property
  (window as any).myPluginFileStore = fileStore;
}
```

Inside a Svelte component:

```svelte
<script lang="ts">
  import { writable, type Writable } from 'svelte/store';
  import type { TFile } from 'obsidian';

  // In production, import the store from a shared module instead of window
  const fileStore: Writable<TFile | null> = (window as any).myPluginFileStore;
  let currentFile: TFile | null = null;
  fileStore.subscribe((f) => { currentFile = f; });
</script>

{#if currentFile}
  <span>{currentFile.basename}</span>
{/if}
```

---

## Cleanup and Memory Management

Svelte components hold DOM references and subscriptions. If you do not unmount them when Obsidian closes the surface, you will leak memory and leave orphaned event listeners.

### Unmounting in Views

Always unmount in `onClose()`:

```typescript
async onClose() {
  if (this.component) {
    unmount(this.component);   // Svelte 5
    // this.component.$destroy(); // Svelte 4
  }
}
```

### Unmounting in Modals

Use `onClose()` of the `Modal` base class:

```typescript
import { Modal, App } from 'obsidian';
import MyModalContent from './MyModalContent.svelte';
import { mount, unmount } from 'svelte';

export class MyModal extends Modal {
  private component: ReturnType<typeof MyModalContent> | undefined;

  constructor(app: App) {
    super(app);
  }

  onOpen() {
    this.component = mount(MyModalContent, {
      target: this.contentEl,
      props: { title: 'Hello from Svelte' },
    });
  }

  onClose() {
    if (this.component) {
      unmount(this.component);
    }
    this.contentEl.empty();
  }
}
```

### Cleanup in `onunload()`

If your plugin mounts Svelte outside the normal view/modal lifecycle (for example, into a ribbon icon's parent element or a status bar item), destroy those instances in `onunload()`:

```typescript
export default class MyPlugin extends Plugin {
  private statusComponent: ReturnType<typeof StatusWidget> | undefined;

  async onload() {
    const statusEl = this.addStatusBarItem();
    this.statusComponent = mount(StatusWidget, {
      target: statusEl,
    });
  }

  onunload() {
    if (this.statusComponent) {
      unmount(this.statusComponent);
    }
  }
}
```

> [!caution]
> Anything created via `this.registerEvent()`, `this.registerInterval()`, or `this.registerDomEvent()` is cleaned up automatically by Obsidian. You only need manual unmounting for Svelte components that were mounted directly onto DOM nodes.

---

## Patterns

### Pattern: Svelte in a Custom `ItemView`

A complete custom view that hosts a Svelte component:

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';
import type MyPlugin from './main';
import SidebarWidget from './SidebarWidget.svelte';
import { mount, unmount } from 'svelte';

export const VIEW_TYPE_WIDGET = 'widget-view';

export class WidgetView extends ItemView {
  private widget: ReturnType<typeof SidebarWidget> | undefined;

  constructor(leaf: WorkspaceLeaf, private plugin: MyPlugin) {
    super(leaf);
  }

  getViewType() { return VIEW_TYPE_WIDGET; }
  getDisplayText() { return 'Widget View'; }

  async onOpen() {
    this.widget = mount(SidebarWidget, {
      target: this.contentEl,
      props: { plugin: this.plugin },
    });
  }

  async onClose() {
    if (this.widget) {
      unmount(this.widget);
    }
  }
}
```

Register the view in `main.ts`:

```typescript
this.registerView(VIEW_TYPE_WIDGET, (leaf) => new WidgetView(leaf, this));
```

### Pattern: Svelte in a `Modal`

```typescript
import { App, Modal } from 'obsidian';
import ConfirmDialog from './ConfirmDialog.svelte';
import { mount, unmount } from 'svelte';

export class ConfirmModal extends Modal {
  private component: ReturnType<typeof ConfirmDialog> | undefined;
  private onConfirm: () => void;

  constructor(app: App, onConfirm: () => void) {
    super(app);
    this.onConfirm = onConfirm;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();

    this.component = mount(ConfirmDialog, {
      target: contentEl,
      props: {
        message: 'Are you sure?',
        onConfirm: () => {
          this.onConfirm();
          this.close();
        },
        onCancel: () => this.close(),
      },
    });
  }

  onClose() {
    if (this.component) {
      unmount(this.component);
    }
    this.contentEl.empty();
  }
}
```

### Pattern: Svelte in `PluginSettingTab`

Replace vanilla DOM construction in your settings tab with a Svelte component for complex UIs:

```typescript
import { App, PluginSettingTab } from 'obsidian';
import type MyPlugin from './main';
import SettingsPanel from './SettingsPanel.svelte';
import { mount, unmount } from 'svelte';

export class MySettingTab extends PluginSettingTab {
  private component: ReturnType<typeof SettingsPanel> | undefined;

  constructor(app: App, private plugin: MyPlugin) {
    super(app, plugin);
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    this.component = mount(SettingsPanel, {
      target: containerEl,
      props: {
        settings: this.plugin.settings,
        onChange: async (settings: MyPluginSettings) => {
          this.plugin.settings = settings;
          await this.plugin.saveSettings();
        },
      },
    });
  }

  hide(): void {
    if (this.component) {
      unmount(this.component);
    }
  }
}
```

> [!note]
> `hide()` is called when the user navigates away from the settings tab. `display()` is called when the tab is shown. Unmount in `hide()` and re-mount in `display()` to keep component lifecycle clean.

---

## Quick Start Checklist

- [ ] Install `svelte`, `svelte-preprocess`, `esbuild-svelte`, and `svelte-check`
- [ ] Update `tsconfig.json` with `verbatimModuleSyntax`, `skipLibCheck`, and `"**/*.svelte"` in `include`
- [ ] Add `esbuildSvelte()` plugin to `esbuild.config.mjs` with `css: 'injected'`
- [ ] Add `"svelte-check"` script to `package.json`
- [ ] Write a `.svelte` component with `<script lang="ts">`
- [ ] Mount the component on an HTML element (`this.contentEl`, `this.containerEl`, etc.)
- [ ] Unmount the component in `onClose()`, `onClose()`, or `hide()`
- [ ] Bridge changing data via Svelte stores rather than remounting on every update
- [ ] Run `npm run svelte-check` before committing

---

## References

- [Use Svelte in your plugin](https://docs.obsidian.md/Plugins/Getting+started/Use+Svelte+in+your+plugin) — Official Obsidian Svelte integration guide
- [Build a plugin](https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin) — Official Obsidian plugin tutorial (prerequisite)
- [Svelte documentation](https://svelte.dev/docs/svelte/overview) — Svelte 5 docs
- [Svelte tutorial](https://svelte.dev/tutorial/svelte/welcome-to-svelte) — Interactive Svelte tutorial
- [esbuild-svelte](https://github.com/EMH333/esbuild-svelte) — esbuild plugin for Svelte
- [svelte-preprocess](https://github.com/sveltejs/svelte-preprocess) — Preprocessor for Svelte
- [Obsidian Sample Plugin](https://github.com/obsidianmd/obsidian-sample-plugin) — Canonical starting template
- [Svelte 5 runes API](https://svelte.dev/docs/svelte/what-are-runes) — `$state`, `$props`, `$derived`, `$effect`
- [Svelte stores](https://svelte.dev/docs/svelte/stores) — `writable`, `readable`, `derived`
