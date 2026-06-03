---
name: obsidian-plugin-events
description: Event handling and resource cleanup for Obsidian plugins. Covers Component resource management, registerEvent, registerDomEvent, registerInterval, registerScopeEvent, register, vault events, workspace events, metadata cache events, and memory leak prevention. Use when adding event listeners, reacting to file changes, or managing plugin lifecycle cleanup.
triggers:
  - obsidian plugin events
  - obsidian plugin event handling
  - obsidian plugin registerEvent
  - obsidian plugin registerDomEvent
  - obsidian plugin registerInterval
  - obsidian plugin memory leak
  - obsidian plugin cleanup
  - obsidian vault events
  - obsidian workspace events
  - obsidian metadata cache events
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Events

This skill guides you through event handling and resource cleanup in Obsidian plugins. It focuses on the registration system that keeps plugins memory-safe: listening to Obsidian events, DOM events, intervals, scope events, and custom cleanup callbacks.

## When to Use This Skill

- Adding event listeners to vault files, workspace layout, or editor changes
- Registering DOM event listeners that must be removed on plugin unload
- Setting up timers with `setInterval` that need automatic cancellation
- Handling keyboard events via Obsidian's scope system
- Preventing memory leaks by cleaning up resources properly
- Understanding the `Component` lifecycle and registration methods

## Overview

Obsidian's plugin system is built on the `Component` class, which provides a registration-based resource management model. When you register a resource through `this.register...()` methods inside a plugin, it is automatically cleaned up when the plugin unloads. This prevents the most common source of plugin bugs: leaking event listeners, DOM nodes, and timers after the plugin is disabled.

At minimum, every plugin that reacts to the outside world needs:

1. **`registerEvent()`** — for Obsidian internal events (vault, workspace, metadata cache)
2. **`registerDomEvent()`** — for DOM event listeners on elements that persist after unload
3. **`registerInterval()`** — for `setInterval` timers that must be cancelled
4. **`registerScopeEvent()`** — for keyboard events bound to a `Scope`
5. **`register()`** — for custom cleanup callbacks

All of these are inherited from `Component` and available on `Plugin`, `View`, `Modal`, `SettingTab`, and any other class that extends `Component`.

---

## Component Resource Management

`Component` is the base class for almost every interactive object in Obsidian. It owns a lifecycle (`load` → `onload` → `unload` → `onunload`) and a registry of cleanup callbacks. When a component unloads, every registered resource is released in reverse order.

```typescript
import { Component } from 'obsidian';

class MyComponent extends Component {
  onload() {
    // Register resources here
    this.register(() => console.log('cleanup 1'));
    this.register(() => console.log('cleanup 2'));
  }

  onunload() {
    // Automatically called in reverse:
    // cleanup 2
    // cleanup 1
  }
}
```

> [!note]
> `Plugin` extends `Component`. Anything you register via `this.register()`, `this.registerEvent()`, etc. inside your plugin class is automatically cleaned up when the plugin is disabled or Obsidian shuts down.

### Child Components

You can also nest components. When a parent unloads, all children unload too:

```typescript
const child = new MyComponent();
this.addChild(child); // child.onload() is called if parent is already loaded
// child.onunload() is called automatically when parent unloads
```

---

## `registerEvent()`

Registers an Obsidian internal event to be detached when the component unloads. Use this for vault events, workspace events, metadata cache events, and any event fired through Obsidian's `Events` class.

```typescript
import { Plugin, TFile } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    // React when a file is opened
    this.registerEvent(
      this.app.workspace.on('file-open', (file: TFile | null) => {
        console.log('Opened:', file?.path);
      })
    );

    // React when a file is modified
    this.registerEvent(
      this.app.vault.on('modify', (file: TFile) => {
        console.log('Modified:', file.path);
      })
    );
  }
}
```

> [!tip]
> If you call `app.workspace.on(...)`, `app.vault.on(...)`, or `app.metadataCache.on(...)` without `registerEvent()`, the listener stays alive after your plugin unloads. Always wrap Obsidian event subscriptions with `registerEvent()`.

### Manual Unregistration (Rare)

If you need to remove a single listener before unload, save the `EventRef`:

```typescript
const ref = this.app.workspace.on('file-open', handler);
this.registerEvent(ref);

// Later, if you want to remove it early:
this.app.workspace.offref(ref);
```

---

## `registerDomEvent()`

Registers a DOM event listener on an element, `window`, or `document` that will be automatically removed when the component unloads. This is essential for global events like `resize`, `scroll`, or `keydown`.

```typescript
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    // Listen to window resize
    this.registerDomEvent(window, 'resize', () => {
      console.log('Window resized');
    });

    // Listen to document clicks
    this.registerDomEvent(document, 'click', (evt: MouseEvent) => {
      console.log('Document clicked at', evt.clientX, evt.clientY);
    });

    // Listen to a specific element
    const el = document.createElement('div');
    document.body.appendChild(el);
    this.registerDomEvent(el, 'mouseenter', () => {
      console.log('Mouse entered custom element');
    });
  }
}
```

> [!caution]
> If you attach listeners to DOM nodes that you create (e.g., custom modals, settings tabs), always use `registerDomEvent()`. If you use `el.addEventListener('click', ...)` directly, the listener leaks when the plugin unloads unless you manually call `removeEventListener` in `onunload()`.

---

## `registerInterval()`

Registers an interval ID so it is automatically cancelled via `clearInterval` when the component unloads. Use `window.setInterval` (not the global `setInterval`) to avoid TypeScript confusion between Node.js and Browser APIs.

```typescript
import { Plugin, Notice } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    // Auto-cancelling heartbeat
    this.registerInterval(
      window.setInterval(() => {
        new Notice('Still alive');
      }, 60000)
    );
  }
}
```

> [!important]
> `registerInterval()` does not return anything useful; it registers the ID for cleanup. If you need to cancel the interval before unload, keep the interval ID returned by `window.setInterval` and call `window.clearInterval(id)` yourself. You can still register a custom cleanup callback with `this.register(() => clearInterval(id))` for safety.

---

## `registerScopeEvent()`

Registers a keyboard event handler bound to a `Scope` so it is automatically unregistered when the component unloads. Scopes receive keyboard events and bind callbacks to hotkeys. Only one scope is active at a time, but scopes may define parent scopes and inherit their hotkeys.

```typescript
import { Plugin, Scope } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    const scope = new Scope(this.app.scope);

    // Register Ctrl+Shift+H to toggle a highlight mode
    const handler = scope.register(['Mod', 'Shift'], 'H', (evt: KeyboardEvent) => {
      console.log('Highlight toggle triggered');
      return true; // indicate the event was handled
    });

    this.registerScopeEvent(handler);
  }
}
```

> [!tip]
> Use `registerScopeEvent()` when building custom modals, views, or widgets that need keyboard shortcuts while focused. Return `true` from the callback to stop the event from propagating to other scopes.

---

## `register()`

Registers an arbitrary callback to be invoked when the component unloads. Use this for resources that do not fit the other registration methods.

```typescript
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  private ws: WebSocket | null = null;

  async onload() {
    this.ws = new WebSocket('wss://example.com/feed');

    this.register(() => {
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }
    });
  }
}
```

> [!note]
> Callbacks registered with `register()` execute in reverse registration order (LIFO). Register dependent resources first and their cleanup last.

---

## Vault Events

The `Vault` class extends `Events` and fires when files change on disk. All vault events are available through `app.vault.on(...)` and should be wrapped with `registerEvent()`.

### `create`

Called when a file is created. **Also called when the vault is first loaded for each existing file.** If you do not wish to receive create events on vault load, register your event handler inside `Workspace.onLayoutReady()`.

```typescript
this.registerEvent(
  this.app.vault.on('create', (file: TAbstractFile) => {
    if (file instanceof TFile) {
      console.log('Created file:', file.path);
    }
  })
);
```

### `modify`

Called when a file is modified.

```typescript
this.registerEvent(
  this.app.vault.on('modify', (file: TFile) => {
    console.log('Modified:', file.path);
  })
);
```

### `delete`

Called when a file is deleted.

```typescript
this.registerEvent(
  this.app.vault.on('delete', (file: TAbstractFile) => {
    console.log('Deleted:', file.path);
  })
);
```

### `rename`

Called when a file is renamed.

```typescript
this.registerEvent(
  this.app.vault.on('rename', (file: TAbstractFile, oldPath: string) => {
    console.log('Renamed:', oldPath, '→', file.path);
  })
);
```

> [!tip]
> To avoid processing every existing file at startup, wrap your `create` listener inside `this.app.workspace.onLayoutReady(() => { ... })`.

---

## Workspace Events

The `Workspace` class extends `Events` and fires for UI and layout changes. All workspace events are available through `app.workspace.on(...)` and should be wrapped with `registerEvent()`.

### `active-leaf-change`

Triggered when the active leaf changes.

```typescript
this.registerEvent(
  this.app.workspace.on('active-leaf-change', (leaf: WorkspaceLeaf) => {
    console.log('Active leaf changed:', leaf.view.getViewType());
  })
);
```

### `layout-change`

Triggered when the workspace layout changes.

```typescript
this.registerEvent(
  this.app.workspace.on('layout-change', () => {
    console.log('Layout changed');
  })
);
```

### `file-open`

Triggered when the active file changes. The file could be in a new leaf, an existing leaf, or an embed.

```typescript
this.registerEvent(
  this.app.workspace.on('file-open', (file: TFile | null) => {
    if (file) {
      console.log('Active file:', file.path);
    }
  })
);
```

### `editor-change`

Triggered when changes to an editor have been applied, either programmatically or from a user event.

```typescript
this.registerEvent(
  this.app.workspace.on('editor-change', (editor: Editor) => {
    console.log('Editor changed');
  })
);
```

### `editor-paste`

Triggered when the editor receives a paste event. Check for `evt.defaultPrevented` before attempting to handle this event, and return if it has already been handled. Use `evt.preventDefault()` to indicate that you've handled the event.

```typescript
this.registerEvent(
  this.app.workspace.on('editor-paste', (evt: ClipboardEvent, editor: Editor) => {
    if (evt.defaultPrevented) return;

    const text = evt.clipboardData?.getData('text/plain');
    if (text?.startsWith('special-prefix:')) {
      evt.preventDefault();
      editor.replaceSelection(text.replace('special-prefix:', ''));
    }
  })
);
```

### `editor-drop`

Triggered when the editor receives a drop event. Check for `evt.defaultPrevented` before attempting to handle this event, and return if it has already been handled. Use `evt.preventDefault()` to indicate that you've handled the event.

```typescript
this.registerEvent(
  this.app.workspace.on('editor-drop', (evt: DragEvent, editor: Editor) => {
    if (evt.defaultPrevented) return;

    const files = evt.dataTransfer?.files;
    if (files && files.length > 0) {
      evt.preventDefault();
      // handle dropped files
    }
  })
);
```

### `resize`

Triggered when a `WorkspaceItem` is resized or the workspace layout has changed.

```typescript
this.registerEvent(
  this.app.workspace.on('resize', () => {
    console.log('Resized');
  })
);
```

### `window-open`

Triggered when a new popout window is created. Desktop only.

```typescript
this.registerEvent(
  this.app.workspace.on('window-open', (win: WorkspaceWindow) => {
    console.log('Popout window opened');
  })
);
```

### `window-close`

Triggered when a popout window is closed. Desktop only.

```typescript
this.registerEvent(
  this.app.workspace.on('window-close', (win: WorkspaceWindow) => {
    console.log('Popout window closed');
  })
);
```

### `css-change`

Triggered when the CSS of the app has changed.

```typescript
this.registerEvent(
  this.app.workspace.on('css-change', () => {
    console.log('CSS updated');
  })
);
```

---

## `MetadataCache` Events

The `MetadataCache` class extends `Events` and fires when files are indexed, resolved, or deleted. All metadata cache events are available through `app.metadataCache.on(...)` and should be wrapped with `registerEvent()`.

### `changed`

Called when a file has been indexed, and its (updated) cache is now available. **Note:** This is not called when a file is renamed for performance reasons. You must hook the vault `rename` event for those.

```typescript
this.registerEvent(
  this.app.metadataCache.on('changed', (file: TFile, data: string, cache: CachedMetadata) => {
    console.log('Metadata indexed:', file.path);
    console.log('Frontmatter:', cache.frontmatter);
  })
);
```

### `resolve`

Called when a file has been resolved for `resolvedLinks` and `unresolvedLinks`. This happens sometimes after a file has been indexed.

```typescript
this.registerEvent(
  this.app.metadataCache.on('resolve', (file: TFile) => {
    console.log('Links resolved for:', file.path);
  })
);
```

### `resolved`

Called when all files have been resolved. This will be fired each time files get modified after the initial load.

```typescript
this.registerEvent(
  this.app.metadataCache.on('resolved', () => {
    console.log('All links resolved');
  })
);
```

### `deleted`

Called when a file has been deleted. A best-effort previous version of the cached metadata is presented, but it could be `null` in case the file was not successfully cached previously.

```typescript
this.registerEvent(
  this.app.metadataCache.on('deleted', (file: TFile, prevCache: CachedMetadata | null) => {
    console.log('Metadata deleted for:', file.path);
  })
);
```

---

## Memory Leak Prevention and Cleanup Best Practices

The most common cause of plugin bugs is failing to clean up resources. Follow these rules to keep plugins memory-safe.

### Rule 1: Always Use Registration Methods

Never attach listeners, intervals, or DOM nodes without registering them:

```typescript
// BAD: leaks on unload
window.addEventListener('resize', this.onResize);
setInterval(this.onTick, 1000);

// GOOD: auto-cleans on unload
this.registerDomEvent(window, 'resize', this.onResize);
this.registerInterval(window.setInterval(this.onTick, 1000));
```

### Rule 2: Avoid `onunload()` for Registered Resources

If you used `registerEvent()`, `registerDomEvent()`, `registerInterval()`, `registerScopeEvent()`, or `register()`, you do **not** need to clean them up in `onunload()`. The `Component` base class handles it.

```typescript
export default class MyPlugin extends Plugin {
  onunload() {
    // Only clean up things you created WITHOUT registration
    console.log('Unloading');
  }
}
```

### Rule 3: Use `register()` for External Resources

WebSockets, workers, or third-party library instances should be cleaned up with `register()`:

```typescript
const worker = new Worker('worker.js');
this.register(() => worker.terminate());
```

### Rule 4: Debounce Expensive Handlers

Event handlers that run on every keystroke or file change can slow down Obsidian. Debounce them:

```typescript
import { debounce } from 'obsidian';

const onChange = debounce((file: TFile) => {
  // expensive operation
}, 500, true);

this.registerEvent(this.app.vault.on('modify', onChange));
```

### Rule 5: Check `defaultPrevented` for Paste and Drop

Always respect other plugins:

```typescript
this.registerEvent(
  this.app.workspace.on('editor-paste', (evt, editor) => {
    if (evt.defaultPrevented) return;
    // your logic
  })
);
```

### Rule 6: Guard Platform-Specific Events

Some workspace events (e.g., `window-open`, `window-close`) only apply to the desktop app. They will not fire on mobile, but registering them is harmless.

---

## Quick Reference Checklist

- [ ] Obsidian events wrapped with `this.registerEvent(...)`
- [ ] DOM events on persistent elements wrapped with `this.registerDomEvent(...)`
- [ ] Intervals created with `window.setInterval(...)` and wrapped with `this.registerInterval(...)`
- [ ] Scope hotkeys wrapped with `this.registerScopeEvent(...)`
- [ ] External resources cleaned up via `this.register(() => ...)`
- [ ] `editor-paste` and `editor-drop` handlers check `evt.defaultPrevented`
- [ ] Vault `create` listener guarded with `onLayoutReady()` if startup noise is unwanted
- [ ] No manual cleanup needed in `onunload()` for registered resources

---

## References

- [Events guide](https://docs.obsidian.md/Plugins/Events) — Official overview of event handling in plugins
- [Component.registerEvent()](https://docs.obsidian.md/Reference/TypeScript+API/Component/registerEvent) — API reference
- [Component.registerDomEvent()](https://docs.obsidian.md/Reference/TypeScript+API/Component/registerDomEvent) — API reference
- [Component.registerInterval()](https://docs.obsidian.md/Reference/TypeScript+API/Component/registerInterval) — API reference
- [Component.register()](https://docs.obsidian.md/Reference/TypeScript+API/Component/register) — API reference
- [Component.registerScopeEvent()](https://docs.obsidian.md/Reference/TypeScript+API/Component/registerScopeEvent) — API reference
- [Vault](https://docs.obsidian.md/Reference/TypeScript+API/Vault) — Vault events (`create`, `modify`, `delete`, `rename`)
- [Workspace](https://docs.obsidian.md/Reference/TypeScript+API/Workspace) — Workspace events (`file-open`, `layout-change`, `editor-change`, etc.)
- [MetadataCache](https://docs.obsidian.md/Reference/TypeScript+API/MetadataCache) — Metadata cache events (`changed`, `resolve`, `resolved`)
- [Scope](https://docs.obsidian.md/Reference/TypeScript+API/Scope) — Scope class for keyboard events
- [Events](https://docs.obsidian.md/Reference/TypeScript+API/Events) — Base `Events` class (`on`, `off`, `offref`, `trigger`)
