---
name: obsidian-plugin-react
description: Integrate React into Obsidian plugins. Covers installing dependencies, TypeScript and esbuild configuration for JSX, mounting and unmounting React components in custom views, modals, and settings tabs, bridging Obsidian events and state into React, and preventing memory leaks with proper cleanup. Use when adding React UI to an existing or new Obsidian plugin.
triggers:
  - obsidian plugin react
  - obsidian react integration
  - obsidian plugin jsx
  - obsidian plugin react component
  - obsidian plugin react view
  - obsidian plugin react modal
  - obsidian plugin react settings
  - obsidian plugin createRoot
  - obsidian plugin react cleanup
  - obsidian plugin react context
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin React Integration

This skill guides you through embedding React components inside an Obsidian plugin. It assumes you already have a working plugin (see `obsidian-plugin-bootstrap` if you are starting from zero). The focus is on build configuration, safe mounting and cleanup, bridging Obsidian APIs into React, and common UI patterns.

## When to Use This Skill

- Adding a React-based UI to an existing Obsidian plugin
- Converting a vanilla HTML custom view into a React component
- Building complex modals or settings panels that benefit from component state
- Reusing existing React components inside Obsidian
- Managing plugin state that needs to be accessible from React components

## Overview

Obsidian plugins are plain TypeScript/JavaScript modules. React is not bundled with Obsidian, so you add it as a dependency and compile `.tsx` files into your `main.js` bundle. The integration points are:

1. **Build config** — teach TypeScript and esbuild to handle JSX
2. **Mount** — create a React root on an `HTMLElement` provided by Obsidian (`contentEl`, `containerEl`, etc.)
3. **Cleanup** — unmount the root when the view, modal, or plugin is destroyed
4. **Bridge** — pass Obsidian's `App` and plugin state into React via context or refs

> [!note]
> You do not need a framework to build Obsidian plugins. Use React when you have existing components, complex state, or a team that prefers it.

---

## Setting Up React

### 1. Install Dependencies

```bash
npm install react react-dom
npm install --save-dev @types/react @types/react-dom
```

### 2. Configure TypeScript for JSX

In `tsconfig.json`, set the JSX transform so you can write `.tsx` without importing `React` explicitly:

```json
{
  "compilerOptions": {
    "jsx": "react-jsx"
  }
}
```

This uses the modern JSX transform. If you prefer the classic transform, use `"jsx": "react"` and import `React` in every `.tsx` file.

### 3. Configure esbuild for JSX

esbuild reads `tsconfig.json` by default and respects the `jsx` setting, so `.tsx` files compile automatically. If you need to override the behavior explicitly, you can set `jsx` in `esbuild.config.mjs`:

```js
const context = await esbuild.context({
  // ... existing options
  jsx: 'automatic', // or 'transform' for classic JSX
});
```

**Key points:**
- Ensure your entry point or imported files include `.tsx` extensions (esbuild resolves them automatically)
- `react` and `react-dom` are bundled into `main.js` because they are not in the `external` array
- Do not add `react` or `react-dom` to `external`; Obsidian does not provide them at runtime

---

## Mounting React Components

React must be mounted onto a real DOM node that Obsidian provides. The most common hosts are:

| Obsidian Surface | DOM Element | Mount In | Unmount In |
|------------------|-------------|----------|------------|
| Custom `ItemView` | `this.contentEl` | `onOpen()` | `onClose()` |
| `Modal` | `this.contentEl` | `onOpen()` | `onClose()` |
| `PluginSettingTab` | `this.containerEl` | `display()` | `hide()` |
| Status bar item | returned `HTMLElement` | plugin init | `onunload()` |

### createRoot and Cleanup

Store the React `Root` instance so you can unmount it later. Always unmount to prevent memory leaks and stale event listeners.

```tsx
import { StrictMode } from 'react';
import { Root, createRoot } from 'react-dom/client';

class MyView extends ItemView {
  root: Root | null = null;

  async onOpen() {
    this.root = createRoot(this.contentEl);
    this.root.render(
      <StrictMode>
        <MyComponent />
      </StrictMode>
    );
  }

  async onClose() {
    this.root?.unmount();
    this.root = null;
  }
}
```

> [!important]
> After calling `root.unmount()`, you cannot call `root.render()` again on the same instance. Create a new root if the element is reused.

---

## Pattern: React in a Custom ItemView

A complete custom view that hosts a React component:

```tsx
// ReactView.tsx
export const ReactView = () => {
  return <h4>Hello, React!</h4>;
};
```

```tsx
// view.tsx
import { StrictMode } from 'react';
import { ItemView, WorkspaceLeaf } from 'obsidian';
import { Root, createRoot } from 'react-dom/client';
import { ReactView } from './ReactView';

export const VIEW_TYPE_EXAMPLE = 'example-view';

export class ExampleView extends ItemView {
  root: Root | null = null;

  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType() {
    return VIEW_TYPE_EXAMPLE;
  }

  getDisplayText() {
    return 'Example view';
  }

  async onOpen() {
    this.root = createRoot(this.contentEl);
    this.root.render(
      <StrictMode>
        <ReactView />
      </StrictMode>
    );
  }

  async onClose() {
    this.root?.unmount();
    this.root = null;
  }
}
```

```tsx
// main.ts
import { Plugin } from 'obsidian';
import { ExampleView, VIEW_TYPE_EXAMPLE } from './view';

export default class MyPlugin extends Plugin {
  async onload() {
    this.registerView(
      VIEW_TYPE_EXAMPLE,
      (leaf) => new ExampleView(leaf)
    );
  }
}
```

---

## Pattern: React in a Modal

```tsx
import { StrictMode } from 'react';
import { App, Modal } from 'obsidian';
import { Root, createRoot } from 'react-dom/client';
import { ModalContent } from './ModalContent';

export class ReactModal extends Modal {
  root: Root | null = null;

  constructor(app: App) {
    super(app);
  }

  onOpen() {
    this.root = createRoot(this.contentEl);
    this.root.render(
      <StrictMode>
        <ModalContent onClose={() => this.close()} />
      </StrictMode>
    );
  }

  onClose() {
    this.root?.unmount();
    this.root = null;
    this.contentEl.empty();
  }
}
```

> [!tip]
> Call `this.contentEl.empty()` after unmounting to remove any leftover DOM nodes that React may not have created.

---

## Pattern: React in PluginSettingTab

```tsx
import { StrictMode } from 'react';
import { App, PluginSettingTab } from 'obsidian';
import { Root, createRoot } from 'react-dom/client';
import { SettingsPanel } from './SettingsPanel';
import MyPlugin from './main';

export class ReactSettingTab extends PluginSettingTab {
  plugin: MyPlugin;
  root: Root | null = null;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();
    this.root = createRoot(containerEl);
    this.root.render(
      <StrictMode>
        <SettingsPanel plugin={this.plugin} />
      </StrictMode>
    );
  }

  hide(): void {
    this.root?.unmount();
    this.root = null;
  }
}
```

> [!note]
> `display()` is called every time the settings tab is opened. `hide()` is called when the user switches away or closes settings. Re-create the root on each display; do not reuse an unmounted root.

---

## Event Bridging

Obsidian events live outside React's lifecycle. To avoid stale closures, use refs or register events inside effects with proper cleanup.

### Using a Ref for the Latest Value

```tsx
import { useRef, useEffect } from 'react';
import { TFile } from 'obsidian';

export const FileWatcher = ({ app }: { app: App }) => {
  const activeFileRef = useRef<TFile | null>(null);

  useEffect(() => {
    const eventRef = app.workspace.on('file-open', (file: TFile) => {
      activeFileRef.current = file;
      // Force re-render if needed
      setCounter(c => c + 1);
    });

    return () => {
      app.workspace.offref(eventRef);
    };
  }, [app]);

  // ...
};
```

### Wrapping Obsidian Events in a Hook

```tsx
import { useEffect, useState } from 'react';
import { TFile } from 'obsidian';

export function useActiveFile(app: App) {
  const [file, setFile] = useState<TFile | null>(app.workspace.getActiveFile());

  useEffect(() => {
    const eventRef = app.workspace.on('file-open', setFile);
    return () => {
      app.workspace.offref(eventRef);
    };
  }, [app]);

  return file;
}
```

> [!caution]
> Do not call `this.registerEvent()` from inside a React component unless you have a stable reference to the plugin instance and clean it up manually. Prefer `app.workspace.on(...)` + `offref(...)` in effects so React controls the subscription lifecycle.

---

## State Management Patterns

### Pattern 1: React Context for the App Object

Pass `App` (and optionally the plugin) down the tree so components can call Obsidian APIs without prop drilling.

```tsx
// context.ts
import { createContext } from 'react';
import { App } from 'obsidian';

export const AppContext = createContext<App | undefined>(undefined);
```

```tsx
// view.tsx
this.root.render(
  <AppContext.Provider value={this.app}>
    <ReactView />
  </AppContext.Provider>
);
```

```tsx
// hooks.ts
import { useContext } from 'react';
import { AppContext } from './context';

export const useApp = (): App | undefined => {
  return useContext(AppContext);
};
```

```tsx
// ReactView.tsx
import { useApp } from './hooks';

export const ReactView = () => {
  const app = useApp();
  const vaultName = app?.vault.getName() ?? 'Unknown';
  return <h4>{vaultName}</h4>;
};
```

### Pattern 2: External Store with Refs

For state that lives in the plugin (settings, caches, etc.), store it in the plugin class and notify React with a minimal store pattern:

```tsx
// store.ts
import { Plugin } from 'obsidian';

type Listener = () => void;

export class PluginStore {
  private listeners: Listener[] = [];
  count = 0;

  increment() {
    this.count++;
    this.emit();
  }

  subscribe(listener: Listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private emit() {
    this.listeners.forEach(l => l());
  }
}
```

```tsx
// useStore.ts
import { useSyncExternalStore } from 'react';
import { PluginStore } from './store';

export function useStore(store: PluginStore) {
  return useSyncExternalStore(
    (callback) => store.subscribe(callback),
    () => store.count
  );
}
```

This keeps plugin state outside React while letting components react to changes.

---

## Cleanup and onunload()

If you mount React outside of `ItemView` or `Modal` (for example, in a status bar item or a custom DOM node), you must unmount in the plugin's `onunload()`:

```tsx
export default class MyPlugin extends Plugin {
  statusRoot: Root | null = null;

  async onload() {
    const item = this.addStatusBarItem();
    this.statusRoot = createRoot(item);
    this.statusRoot.render(<StatusComponent />);
  }

  onunload() {
    this.statusRoot?.unmount();
    this.statusRoot = null;
  }
}
```

> [!note]
> Resources registered via `this.registerEvent()`, `this.registerInterval()`, `this.registerDomEvent()`, etc. are cleaned up automatically by Obsidian. React roots are **not** registered resources — unmount them manually.

---

## Quick Start Checklist

- [ ] Install `react`, `react-dom`, and their type definitions
- [ ] Set `"jsx": "react-jsx"` in `tsconfig.json`
- [ ] Ensure esbuild processes `.tsx` files (reads `tsconfig.json` by default)
- [ ] Create a React component in a `.tsx` file
- [ ] Mount it with `createRoot(element)` in `onOpen()` / `display()` / `onOpen()`
- [ ] Unmount with `root.unmount()` in `onClose()` / `hide()` / `onunload()`
- [ ] Pass `App` into React via Context if multiple components need it
- [ ] Wrap Obsidian event subscriptions in `useEffect` with cleanup
- [ ] Test disable/enable cycles to verify no memory leaks

---

## References

- [Use React in your plugin](https://docs.obsidian.md/Plugins/Getting+started/Use+React+in+your+plugin) — Official Obsidian guide
- [React createRoot](https://react.dev/reference/react-dom/client/createRoot) — React 18 root API
- [Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context) — React Context docs
- [Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — React Hooks docs
- [Sample Plugin Template](https://github.com/obsidianmd/obsidian-sample-plugin) — Starting point for any plugin
- [TypeScript API Reference](https://docs.obsidian.md/Reference/TypeScript+API/) — Full Obsidian API docs
