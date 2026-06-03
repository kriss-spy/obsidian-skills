---
name: obsidian-plugin-bootstrap
description: Bootstrap a new Obsidian plugin from zero. Covers dev environment setup, manifest.json, project anatomy, plugin lifecycle, hot reload workflow, mobile constraints, and building for release. Use when scaffolding a new plugin or onboarding a developer to the Obsidian plugin ecosystem.
triggers:
  - obsidian plugin bootstrap
  - obsidian plugin scaffold
  - obsidian plugin setup
  - obsidian plugin new
  - obsidian plugin development environment
  - obsidian plugin manifest
  - obsidian plugin build
  - obsidian plugin hot reload
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Bootstrap

This skill guides you through scaffolding a new Obsidian plugin from an empty directory to a working, reloadable plugin. It focuses on the bootstrap phase: environment setup, manifest configuration, project structure, and the development loop.

## When to Use This Skill

- Starting a new Obsidian plugin project
- Setting up the development environment (Node.js, esbuild, TypeScript)
- Understanding `manifest.json` requirements and best practices
- Structuring a plugin project for maintainability
- Configuring hot reload for fast iteration
- Preparing a build for release (`main.js`, `manifest.json`, `styles.css`)
- Understanding mobile constraints before writing platform-dependent code

## Overview

An Obsidian plugin is a TypeScript/JavaScript module that extends Obsidian through a well-defined API. At minimum, a plugin needs:

1. **`manifest.json`** — plugin metadata and requirements
2. **`main.js`** — compiled entry point (produced by `esbuild` from `main.ts`)
3. **`styles.css`** — optional custom styles

During development, you compile TypeScript with `esbuild`, place the outputs into a vault's `.obsidian/plugins/<id>/` folder, and reload the plugin from Obsidian's Community Plugins settings.

---

## Dev Environment Setup

### Prerequisites

- **Git** — to clone the sample plugin or initialize your own repo
- **Node.js** — LTS version recommended (v18+)
- **A code editor** — VS Code or similar
- **A dedicated development vault** — never develop plugins in your main vault

### Step 1: Create a Dev Vault

```bash
mkdir -p ~/DevVault/.obsidian/plugins
cd ~/DevVault/.obsidian/plugins
```

### Step 2: Initialize from the Sample Plugin

The official sample plugin is the canonical starting point:

```bash
git clone https://github.com/obsidianmd/obsidian-sample-plugin.git my-plugin
cd my-plugin
npm install
```

> [!tip]
> The sample plugin repo is a GitHub template. Create your own repository from it so you can push your work directly.

### Step 3: Core Config Files

After `npm install`, you will have these critical config files:

#### `package.json`

```json
{
  "name": "obsidian-sample-plugin",
  "version": "1.0.0",
  "description": "This is a sample plugin for Obsidian",
  "main": "main.js",
  "scripts": {
    "dev": "node esbuild.config.mjs",
    "build": "tsc -noEmit -skipLibCheck && node esbuild.config.mjs production",
    "version": "node version-bump.mjs && git add manifest.json versions.json"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^16.11.6",
    "@typescript-eslint/eslint-plugin": "5.29.0",
    "@typescript-eslint/parser": "5.29.0",
    "builtin-modules": "3.3.0",
    "esbuild": "0.17.3",
    "obsidian": "latest",
    "tslib": "2.4.0",
    "typescript": "4.7.4"
  }
}
```

**Key scripts:**
- `npm run dev` — starts esbuild in watch mode; rebuilds on every file change
- `npm run build` — type-checks with `tsc` then builds a production bundle

#### `tsconfig.json`

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
    "strictNullChecks": true
  },
  "include": [
    "**/*.ts"
  ]
}
```

Obsidian plugins compile to ES6. `inlineSourceMap` and `inlineSources` are required so that error stack traces in Obsidian's Developer Tools point back to your TypeScript source.

#### `esbuild.config.mjs`

```js
import esbuild from "esbuild";
import process from "process";
import builtins from "builtin-modules";

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
});

if (prod) {
  await context.rebuild();
  process.exit(0);
} else {
  await context.watch();
}
```

**Important details:**
- `format: "cjs"` — Obsidian loads plugins as CommonJS modules
- `target: "es2018"` — safe target for Electron's Chromium engine
- `external: ["obsidian", ...]` — do not bundle Obsidian or its CodeMirror dependencies; they are provided at runtime
- `sourcemap: "inline"` — only in development; omit in production to reduce bundle size

---

## `manifest.json`

The manifest is Obsidian's source of truth for plugin identity, versioning, and compatibility. It must be valid JSON and sit at the root of your plugin folder (and your repository).

### Full Schema

```json
{
  "id": "my-unique-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "minAppVersion": "0.15.0",
  "description": "A short description of what this plugin does.",
  "author": "Your Name",
  "authorUrl": "https://yourwebsite.com",
  "fundingUrl": "https://github.com/sponsors/yourusername",
  "isDesktopOnly": false
}
```

### Field Reference

| Property | Required | Type | Description |
|----------|----------|------|-------------|
| `id` | **Yes** | `string` | Unique identifier. Lowercase letters and hyphens only. Cannot end with `plugin`. Cannot contain `obsidian`. For local development, should match the plugin folder name. |
| `name` | **Yes** | `string` | Display name. Short, descriptive, English, Basic Latin characters only. No emoji. Do not reuse core plugin names or include "Obsidian". |
| `version` | **Yes** | `string` | Semantic version in `x.y.z` format. |
| `minAppVersion` | **Yes** | `string` | Minimum Obsidian app version required. Obsidian refuses to load the plugin if the app is older. |
| `description` | **Yes** | `string` | Brief description of functionality. |
| `author` | **Yes** | `string` | Author's name. |
| `authorUrl` | No | `string` | Link to author's website. |
| `fundingUrl` | No | `string` or `object` | Single URL or an object mapping label → URL (e.g., `{"Buy Me a Coffee": "...", "GitHub Sponsor": "..."}`). |
| `isDesktopOnly` | **Yes** | `boolean` | `true` if the plugin uses Node.js or Electron APIs. Mobile users will not see it in the community plugin list. |

### Best Practices

- **ID immutability** — Never change `id` after release. Changing it breaks updates for existing users and splits your plugin into two entries in the community directory.
- **Semantic versioning** — Use `x.y.z`. Bump `minAppVersion` only when you adopt a new API that requires a newer Obsidian version.
- **Match folder name locally** — For local development, the plugin folder under `.obsidian/plugins/` must match `id`. Otherwise some lifecycle hooks (like `onExternalSettingsChange`) won't fire.
- **Restart after manifest changes** — Obsidian reads `manifest.json` at startup. If you edit it, reload the app or disable/enable the plugin.

---

## Plugin Lifecycle

Every plugin extends the `Plugin` class from `obsidian`. Three lifecycle methods matter most at bootstrap time:

### `onload()`

Called when the plugin is loaded. This is where you register commands, settings, views, events, and UI elements.

```typescript
import { Plugin, Notice } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    console.log('Loading my-plugin');

    this.addRibbonIcon('dice', 'Greet', () => {
      new Notice('Hello from my plugin!');
    });

    this.addCommand({
      id: 'sample-command',
      name: 'Sample command',
      callback: () => {
        new Notice('Command triggered');
      },
    });
  }
}
```

### `onunload()`

Called when the plugin is disabled or Obsidian shuts down. Clean up event listeners, timers, DOM nodes, and registered resources here.

```typescript
  onunload() {
    console.log('Unloading my-plugin');
    // Any resource registered via this.register(), this.registerEvent(),
    // this.registerInterval(), etc. is cleaned up automatically.
    // Add manual cleanup only for resources created outside the registration system.
  }
```

> [!note]
> Anything registered with `this.register()`, `this.registerEvent()`, `this.registerDomEvent()`, `this.registerInterval()`, or `this.registerEditorExtension()` is automatically released on unload. You only need custom cleanup for resources you created independently.

### `onUserEnable()`

Called when the user explicitly enables the plugin from Community Plugins settings. This runs **after** `onload()` on first enable. Use it for one-time setup that should not repeat on normal startup (e.g., onboarding modals, default data initialization).

```typescript
  async onUserEnable() {
    // Show a welcome notice or create default config files
    new Notice('My Plugin enabled! Open settings to configure.');
  }
```

---

## Project Anatomy

As your plugin grows beyond a single file, split concerns into a `src/` directory:

```
my-plugin/
├── src/
│   ├── main.ts              # Entry point: exports default class extending Plugin
│   ├── settings.ts          # Settings interface + DEFAULT_SETTINGS
│   ├── settingsTab.ts       # PluginSettingTab implementation
│   ├── commands.ts          # Command definitions and callbacks
│   ├── views/
│   │   └── exampleView.ts   # Custom ItemView classes
│   └── utils.ts             # Shared helpers, parsers, constants
├── manifest.json
├── styles.css               # Optional; loaded automatically if present
├── package.json
├── tsconfig.json
├── esbuild.config.mjs
└── versions.json            # Maps plugin versions to minAppVersion (for release)
```

### Entry point (`src/main.ts`)

Keep `main.ts` thin. Delegate to modules:

```typescript
import { Plugin } from 'obsidian';
import { MyPluginSettings, DEFAULT_SETTINGS } from './settings';
import { MySettingTab } from './settingsTab';
import { registerCommands } from './commands';

export default class MyPlugin extends Plugin {
  settings: MyPluginSettings;

  async onload() {
    await this.loadSettings();
    this.addSettingTab(new MySettingTab(this.app, this));
    registerCommands(this);
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

### Settings module (`src/settings.ts`)

```typescript
export interface MyPluginSettings {
  mySetting: string;
  enabled: boolean;
}

export const DEFAULT_SETTINGS: MyPluginSettings = {
  mySetting: 'default',
  enabled: true,
};
```

If you move the entry point into `src/main.ts`, update `esbuild.config.mjs`:

```js
entryPoints: ["src/main.ts"],
outfile: "main.js",
```

---

## Hot Reload Workflow

### The Problem

Obsidian loads `main.js` at plugin enable time and does not auto-reload when the file changes. Without a reload strategy, every code change requires manually disabling and re-enabling the plugin.

### Solution 1: Hot-Reload Plugin (Recommended)

1. Install the **Hot-Reload** community plugin in your dev vault.
2. It monitors `.obsidian/plugins/` for changes and automatically reloads affected plugins.
3. Run `npm run dev` in your plugin project. Every save triggers a rebuild; Hot-Reload picks up the new `main.js` within seconds.

### Solution 2: Symlink Strategy

Instead of copying files, symlink the build artifacts into the vault:

```bash
# Linux / macOS
ln -s /path/to/my-plugin/main.js /path/to/DevVault/.obsidian/plugins/my-plugin/main.js
ln -s /path/to/my-plugin/manifest.json /path/to/DevVault/.obsidian/plugins/my-plugin/manifest.json
ln -s /path/to/my-plugin/styles.css /path/to/DevVault/.obsidian/plugins/my-plugin/styles.css
```

> [!caution]
> Symlinks work well on desktop but may behave inconsistently on Windows without Developer Mode, and they are irrelevant for mobile testing.

### Solution 3: Copy Script

For a cross-platform alternative, add a copy script to `package.json`:

```json
{
  "scripts": {
    "dev": "node esbuild.config.mjs",
    "build": "tsc -noEmit -skipLibCheck && node esbuild.config.mjs production",
    "copy": "cp main.js manifest.json styles.css /path/to/DevVault/.obsidian/plugins/my-plugin/"
  }
}
```

### Verification

After enabling your plugin:

1. Run `npm run dev`
2. Edit `src/main.ts` (e.g., change a `Notice` message)
3. Save — esbuild rebuilds `main.js`
4. If using Hot-Reload, the change appears in Obsidian immediately. Otherwise, disable and re-enable the plugin in Settings → Community Plugins.

---

## Mobile Development Gotchas

Obsidian runs on iOS and Android using a webview. Not everything from desktop translates.

### What Works on Mobile

- All Obsidian TypeScript APIs (`app.vault`, `app.workspace`, `app.metadataCache`, etc.)
- DOM manipulation inside Obsidian's UI
- `fetch`, `localStorage`, IndexedDB
- CodeMirror 6 editor extensions

### What Does NOT Work on Mobile

- **Node.js APIs** (`fs`, `path`, `os`, `child_process`, etc.)
- **Electron APIs** (`require('electron')`, `window.require`, IPC)
- Custom status bar items (`addStatusBarItem()` is ignored on mobile)
- Some regular expression lookbehinds on iOS < 16.4

### Guarding Platform-Specific Code

Use the `Platform` utility:

```typescript
import { Platform } from 'obsidian';

if (Platform.isDesktopApp) {
  const item = this.addStatusBarItem();
  item.setText('Desktop only');
}

if (Platform.isMobile) {
  // Avoid features that depend on Node.js/Electron
}
```

### `isDesktopOnly` Flag

If your plugin fundamentally requires Node.js or Electron (e.g., shell execution, native file system access outside the vault), set `isDesktopOnly: true` in `manifest.json`. Mobile users will not see it in the community plugin browser.

If your plugin is *mostly* compatible but has one desktop-only feature, keep `isDesktopOnly: false` and gate the feature with `Platform.isDesktopApp`.

---

## Build for Release

### Production Build

```bash
npm run build
```

This:
1. Type-checks the project with `tsc -noEmit`
2. Bundles `main.js` via esbuild with tree-shaking and no source maps

### Required Release Artifacts

A valid release must contain exactly these files at the root of the release archive:

| File | Required? | Description |
|------|-----------|-------------|
| `main.js` | **Yes** | Compiled plugin bundle |
| `manifest.json` | **Yes** | Metadata; must match the release tag |
| `styles.css` | No | Loaded automatically if present |

> [!important]
> Do not include `node_modules/`, `src/`, or build configs in the release. The Obsidian community plugin system expects only the compiled artifacts.

### Version Compatibility (`versions.json`)

If you ever raise `minAppVersion`, create `versions.json` at the repo root:

```json
{
  "1.0.0": "0.15.0",
  "1.1.0": "0.16.0"
}
```

Obsidian uses this to serve the latest compatible plugin version to users on older app versions. You only need to update `versions.json` when `minAppVersion` changes, not on every release.

---

## Quick Start Checklist

- [ ] Create a dedicated dev vault
- [ ] Clone `obsidian-sample-plugin` or initialize your own repo
- [ ] Run `npm install`
- [ ] Update `manifest.json` with a unique `id`, `name`, and `description`
- [ ] Rename the plugin folder to match `id`
- [ ] Run `npm run dev`
- [ ] Copy or symlink `main.js` and `manifest.json` into `.obsidian/plugins/<id>/`
- [ ] Enable the plugin in Obsidian → Settings → Community Plugins
- [ ] Install **Hot-Reload** for automatic reloading
- [ ] Edit code, save, verify the change reloads
- [ ] Set `isDesktopOnly` correctly if using Node.js/Electron APIs

---

## References

- [Build a plugin](https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin) — Official tutorial
- [Anatomy of a plugin](https://docs.obsidian.md/Plugins/Getting+started/Anatomy+of+a+plugin) — Overview of files and folders
- [Development workflow](https://docs.obsidian.md/Plugins/Getting+started/Development+workflow) — Hot reload, debugging, and iterating
- [Mobile development](https://docs.obsidian.md/Plugins/Getting+started/Mobile+development) — Platform-specific features and constraints
- [Manifest reference](https://docs.obsidian.md/Reference/Manifest) — Complete `manifest.json` schema
- [Versions reference](https://docs.obsidian.md/Reference/Versions) — `versions.json` and compatibility
- [Sample Plugin Template](https://github.com/obsidianmd/obsidian-sample-plugin) — Official GitHub template
- [TypeScript API Reference](https://docs.obsidian.md/Reference/TypeScript+API/) — Full API docs
