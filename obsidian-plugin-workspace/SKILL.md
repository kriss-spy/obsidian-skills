---
name: obsidian-plugin-workspace
description: Master the Obsidian workspace API. Covers workspace tree layout, custom views (ItemView, FileView, MarkdownView, TextFileView), leaf lifecycle, pane management, pop-out windows, linked panes, and workspace events. Use when building custom views, managing splits and tabs, or reacting to layout and focus changes.
triggers:
  - obsidian workspace
  - obsidian custom view
  - obsidian plugin workspace
  - obsidian pane management
  - obsidian workspace leaf
  - obsidian itemview
  - obsidian fileview
  - obsidian markdownview
  - obsidian textfileview
  - obsidian register view
  - obsidian workspace events
  - obsidian linked panes
  - obsidian popout window
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Workspace

This skill covers the Obsidian workspace API: how panes are organized into splits and tabs, how to create and manage `WorkspaceLeaf` instances, how to build custom views, and how to react to workspace-level events. It is the reference for anything related to layout, views, and pane lifecycle.

## When to Use This Skill

- Creating a custom view (sidebar panel, modal-like pane, or editor replacement)
- Managing where panes open (root split, left/right sidebar, pop-out windows)
- Understanding the relationship between `WorkspaceLeaf`, `WorkspaceSplit`, and `WorkspaceTabs`
- Reacting to focus changes (`active-leaf-change`), file opens (`file-open`), or layout changes (`layout-change`)
- Implementing linked panes that scroll together
- Working with deferred tabs (Obsidian v1.7.2+)
- Opening files in specific locations with `getLeaf()`, `getLeftLeaf()`, `getRightLeaf()`, or `createLeafInParent()`

## Overview

Obsidian's UI is a tree of workspace items. At the root is a `WorkspaceRoot` (or a `WorkspaceWindow` for pop-outs). It contains `WorkspaceSplit` nodes that recursively divide the screen vertically or horizontally. The leaves of this tree are `WorkspaceTabs` containers, each of which holds one or more `WorkspaceLeaf` instances. Every leaf hosts exactly one `View`.

```
WorkspaceRoot
└── WorkspaceSplit (vertical)
    ├── WorkspaceSplit (horizontal)
    │   ├── WorkspaceTabs
    │   │   ├── WorkspaceLeaf → MarkdownView
    │   │   └── WorkspaceLeaf → GraphView
    │   └── WorkspaceTabs
    │       └── WorkspaceLeaf → ItemView (custom sidebar)
    └── WorkspaceSidedock (left sidebar)
        └── WorkspaceTabs
            └── WorkspaceLeaf → FileExplorerView
```

The `app.workspace` object is your entry point to the entire tree.

---

## Workspace Tree Model

### Core Types

| Class | Role |
|-------|------|
| `WorkspaceRoot` | The top-level container for the main workspace area |
| `WorkspaceWindow` | Top-level container for a pop-out window (desktop only) |
| `WorkspaceContainer` | Abstract base for `WorkspaceRoot` and `WorkspaceWindow`; provides `win` and `doc` |
| `WorkspaceSplit` | A node that divides space; can be nested |
| `WorkspaceTabs` | Holds a tab strip and its associated leaves |
| `WorkspaceLeaf` | A single pane (tab) that hosts one `View` |
| `WorkspaceSidedock` | Sidebar container (`leftSplit`, `rightSplit`) |
| `WorkspaceMobileDrawer` | Mobile sidebar drawer |
| `WorkspaceFloating` | Container for floating leaves |

### Traversing the Tree

```typescript
import { WorkspaceLeaf, WorkspaceTabs, WorkspaceSplit } from 'obsidian';

// Visit every leaf in the entire workspace
this.app.workspace.iterateAllLeaves((leaf: WorkspaceLeaf) => {
  console.log(leaf.view.getViewType());
});

// Visit only leaves in the main (root) area
this.app.workspace.iterateRootLeaves((leaf: WorkspaceLeaf) => {
  console.log(leaf.view.getViewType());
});

// Get the root split
const root = this.app.workspace.rootSplit;

// Get side docks
const leftSidebar = this.app.workspace.leftSplit;
const rightSidebar = this.app.workspace.rightSplit;

// A leaf's parent is always WorkspaceTabs (desktop) or WorkspaceMobileDrawer (mobile)
const parent = leaf.parent;
if (parent instanceof WorkspaceTabs) {
  // Safe to assume tab container
}
```

> [!note]
> A `WorkspaceLeaf`'s `parent` is `WorkspaceTabs | WorkspaceMobileDrawer`. On desktop, it is always `WorkspaceTabs`. Check with `instanceof` before accessing `parent`-specific properties.

---

## WorkspaceLeaf Lifecycle

A `WorkspaceLeaf` is the shell that holds a view. Its lifecycle is separate from the `View` inside it: the same leaf can open, close, and swap views without being destroyed.

### Key Properties

| Property | Description |
|----------|-------------|
| `leaf.view` | The `View` currently inside the leaf. Do not cast without `instanceof`. |
| `leaf.parent` | The containing `WorkspaceTabs` or `WorkspaceMobileDrawer`. |
| `leaf.hoverPopover` | Currently active hover popover, if any. |
| `leaf.isDeferred` | **v1.7.2+** Whether the leaf is backgrounded and has a `DeferredView` placeholder. |

### Key Methods

| Method | Description |
|--------|-------------|
| `await leaf.setViewState(state, eState?)` | Open a new view type in this leaf. |
| `leaf.getViewState()` | Get the current `ViewState` (type, state, active, group, pinned). |
| `await leaf.openFile(file, openState?)` | Open a file in this leaf (works for `FileView` leaves). |
| `await leaf.open(view)` | Open a specific `View` instance in this leaf. |
| `leaf.detach()` | Destroy the leaf and its view. |
| `leaf.setPinned(pinned)` | Pin or unpin the leaf. |
| `leaf.togglePinned()` | Toggle pinned state. |
| `leaf.setGroup(group)` | Assign this leaf to a named group for linked scrolling. |
| `leaf.setGroupMember(other)` | Link this leaf to another leaf's group. |
| `leaf.loadIfDeferred()` | **v1.7.2+** If deferred, force load the real view. |

### Opening, Detaching, and Revealing

```typescript
// Detach all leaves of a specific type (common pattern before opening a singleton view)
this.app.workspace.detachLeavesOfType('my-custom-view');

// Create a leaf and reveal it
const leaf = this.app.workspace.getRightLeaf(false);
if (leaf) {
  await leaf.setViewState({ type: 'my-custom-view', active: true });
  this.app.workspace.revealLeaf(leaf);
}
```

> [!tip]
> Always `await revealLeaf(leaf)` when programmatically opening a sidebar view. It uncollapses the sidebar and brings the tab to the foreground.

### Deferred Tabs (v1.7.2+)

Obsidian now defers background tabs to improve startup performance. A deferred leaf has a placeholder `DeferredView` instead of its real view.

```typescript
if (leaf.isDeferred) {
  await leaf.loadIfDeferred();
}
// Now safe to interact with leaf.view
```

---

## Leaf Factory Methods

Obsidian provides several ways to obtain or create a `WorkspaceLeaf`. Choosing the right method determines where the pane appears.

### `getLeaf(newLeaf?, direction?)`

The most versatile factory. Behavior depends on the first argument:

| Argument | Behavior |
|----------|----------|
| `false` or omitted | Return an existing navigable leaf, or create one if none exists. |
| `true` or `'tab'` | Create a new leaf in the preferred location within the root split. |
| `'split'` | Create a new leaf adjacent to the currently active leaf. Use `direction` (`'vertical'` or `'horizontal'`) to control orientation. |
| `'window'` | Create a new leaf inside a new pop-out window (desktop only). |

```typescript
// Open in existing leaf if possible, otherwise create one
const leaf = this.app.workspace.getLeaf(false);

// Always open in a new tab in the root split
const leaf = this.app.workspace.getLeaf('tab');

// Split vertically (new leaf to the right of the active one)
const leaf = this.app.workspace.getLeaf('split', 'vertical');

// Open in a new pop-out window
const leaf = this.app.workspace.getLeaf('window');

// Open a file in the chosen leaf
await leaf.openFile(file);
```

> [!tip]
> For commands bound to a user action (like a click), pass `Keymap.isModEvent(evt)` as the first argument. This respects the user's modifier-key preference for opening files (e.g., Ctrl/Cmd+Click → new tab).

### `getLeftLeaf(split)`

Creates a new leaf inside the **left sidebar**.

```typescript
const leaf = this.app.workspace.getLeftLeaf(false);
// false = do not split the existing sidebar container; reuse space if possible
// Returns WorkspaceLeaf | null
```

### `getRightLeaf(split)`

Creates a new leaf inside the **right sidebar**.

```typescript
const leaf = this.app.workspace.getRightLeaf(false);
```

### `createLeafInParent(parent, index)`

Creates a new `WorkspaceLeaf` inside an explicit `WorkspaceSplit` at a specific index.

```typescript
const parentSplit = this.app.workspace.rootSplit;
const newLeaf = this.app.workspace.createLeafInParent(parentSplit, 0);
await newLeaf.setViewState({ type: 'my-view', active: true });
```

### `ensureSideLeaf(type, side, options)`

**v1.7.2+** Shorthand to get an existing sidebar leaf of a given type or create one if it does not exist.

```typescript
const leaf = await this.app.workspace.ensureSideLeaf('my-sidebar-view', 'left', {
  active: true,
  reveal: true,
  split: false,
});
```

| Option | Description |
|--------|-------------|
| `active` | Whether the leaf should become the active tab in its container |
| `reveal` | Whether to uncollapse and focus the sidebar |
| `split` | Whether to split the sidebar container |
| `state` | Optional initial `ViewState` payload |

### Comparison

| Use Case | Method |
|----------|--------|
| Open file in existing leaf or create one | `getLeaf(false)` |
| Open file in new root tab | `getLeaf('tab')` |
| Open file in split next to active | `getLeaf('split', direction)` |
| Open file in pop-out window | `getLeaf('window')` |
| Add custom view to left sidebar | `getLeftLeaf(false)` |
| Add custom view to right sidebar | `getRightLeaf(false)` |
| Ensure singleton sidebar view exists | `ensureSideLeaf(type, side, { reveal: true })` |
| Precise insertion into a known split | `createLeafInParent(parent, index)` |

---

## Custom Views

Custom views let you render arbitrary UI inside a leaf. The base class is `View`, but you almost always extend one of its subclasses.

### Class Hierarchy

```
View (abstract)
├── ItemView (abstract)
│   ├── FileView (abstract)
│   │   ├── EditableFileView (abstract)
│   │   │   └── TextFileView (abstract)
│   │   │       └── MarkdownView
│   └── YourCustomSidebarView
└── YourCustomRootView
```

### Implementing `ItemView`

`ItemView` is the standard base for sidebar panels, graph views, and any non-file leaf content. It provides `contentEl`, a dedicated DOM container below the header.

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';

export const VIEW_TYPE_DASHBOARD = 'dashboard-view';

export class DashboardView extends ItemView {
  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE_DASHBOARD;
  }

  getDisplayText(): string {
    return 'Dashboard';
  }

  getIcon(): string {
    return 'layout-dashboard';
  }

  async onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl('h3', { text: 'My Dashboard' });
    contentEl.createEl('p', { text: 'Custom content here.' });
  }

  async onClose() {
    // Clean up timers, observers, or external connections
  }
}
```

### Implementing `FileView`

Extend `FileView` when your view renders a file but is not a text editor. It automatically handles file loading/unloading and state serialization.

```typescript
import { FileView, WorkspaceLeaf, TFile } from 'obsidian';

export const VIEW_TYPE_IMAGE = 'image-view';

export class ImageView extends FileView {
  allowNoFile = false;

  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE_IMAGE;
  }

  getDisplayText(): string {
    return this.file?.name ?? 'Image';
  }

  async onLoadFile(file: TFile) {
    this.contentEl.empty();
    const img = this.contentEl.createEl('img');
    img.src = this.app.vault.getResourcePath(file);
  }

  async onUnloadFile(file: TFile) {
    this.contentEl.empty();
  }

  canAcceptExtension(extension: string): boolean {
    return ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'].includes(extension);
  }
}
```

### Implementing `TextFileView`

Extend `TextFileView` when you want to build a custom text editor. It manages in-memory `data`, debounced saves, and the `onLoadFile`/`onUnloadFile` lifecycle.

```typescript
import { TextFileView, WorkspaceLeaf } from 'obsidian';

export const VIEW_TYPE_JSON = 'json-editor';

export class JsonEditorView extends TextFileView {
  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE_JSON;
  }

  getViewData(): string {
    return this.data;
  }

  setViewData(data: string, clear: boolean) {
    this.data = data;
    this.contentEl.empty();
    this.contentEl.createEl('pre', { text: data });
  }

  clear() {
    this.data = '';
    this.contentEl.empty();
  }
}
```

### Extending `MarkdownView`

`MarkdownView` is Obsidian's built-in markdown editor. You rarely subclass it directly; instead, use `TextFileView` for custom editors or `FileView` for read-only file renderers.

---

## `registerView()` and `registerExtensions()`

Before you can open a custom view, you must register it during `onload()`.

### `registerView(type, viewCreator)`

```typescript
export default class MyPlugin extends Plugin {
  async onload() {
    this.registerView(
      VIEW_TYPE_DASHBOARD,
      (leaf) => new DashboardView(leaf)
    );

    this.addCommand({
      id: 'open-dashboard',
      name: 'Open Dashboard',
      callback: () => this.openDashboard(),
    });
  }

  async openDashboard() {
    const { workspace } = this.app;

    // If already open, reveal it
    const existing = workspace.getLeavesOfType(VIEW_TYPE_DASHBOARD);
    if (existing.length > 0) {
      workspace.revealLeaf(existing[0]);
      return;
    }

    // Otherwise create in right sidebar
    const leaf = workspace.getRightLeaf(false);
    if (leaf) {
      await leaf.setViewState({ type: VIEW_TYPE_DASHBOARD, active: true });
      workspace.revealLeaf(leaf);
    }
  }
}
```

### `registerExtensions(extensions, viewType)`

Associate file extensions with your custom view so double-clicking a file opens it in your view instead of the default.

```typescript
this.registerExtensions(['csv'], VIEW_TYPE_CSV);
```

> [!important]
> Only one view type can own an extension. If another plugin (or core Obsidian) already registered it, yours will not take precedence.

---

## Opening and Managing Panes

### Root Split vs Side Docks

| Location | Access | Typical Use |
|----------|--------|-------------|
| Root split | `app.workspace.rootSplit` | Main editing area |
| Left sidebar | `app.workspace.leftSplit` | File explorer, outline, custom tools |
| Right sidebar | `app.workspace.rightSplit` | Backlinks, tags, custom panels |
| Pop-out window | `app.workspace.openPopoutLeaf()` | Secondary monitor support (desktop) |

### Opening a File in a Specific Location

```typescript
import { TFile } from 'obsidian';

const file: TFile = this.app.vault.getAbstractFileByPath('Note.md') as TFile;

// Existing leaf or new root leaf
const leaf = this.app.workspace.getLeaf(false);
await leaf.openFile(file);

// New tab in root
const leaf2 = this.app.workspace.getLeaf('tab');
await leaf2.openFile(file);

// Split to the right
const leaf3 = this.app.workspace.getLeaf('split', 'vertical');
await leaf3.openFile(file);

// Pop-out window (desktop only)
const leaf4 = this.app.workspace.getLeaf('window');
await leaf4.openFile(file);
```

### Opening by Link Text

```typescript
await this.app.workspace.openLinkText(
  'Target Note',
  'Source Note.md',
  'tab', // or true, false, 'split', 'window'
  { active: true, state: { mode: 'source' } }
);
```

### Getting the Active View

```typescript
import { MarkdownView } from 'obsidian';

const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
if (activeView) {
  console.log(activeView.editor.getValue());
}
```

### Reveal and Focus

```typescript
// Bring a leaf to the foreground (uncollapses sidebars if needed)
await this.app.workspace.revealLeaf(leaf);

// Programmatically focus a leaf
this.app.workspace.setActiveLeaf(leaf, { focus: true });
```

---

## Pop-out Windows

Desktop-only feature. Use `Platform.isDesktopApp` to guard pop-out logic.

### `openPopoutLeaf(data?)`

Creates a new pop-out window with a single leaf.

```typescript
import { Platform } from 'obsidian';

if (Platform.isDesktopApp) {
  const leaf = this.app.workspace.openPopoutLeaf({
    x: 100,
    y: 100,
  });
  await leaf.setViewState({ type: 'markdown', state: { file: 'Note.md' } });
}
```

### `moveLeafToPopout(leaf, data?)`

Migrates an existing leaf to a new pop-out window.

```typescript
import { Platform } from 'obsidian';

if (Platform.isDesktopApp) {
  const activeLeaf = this.app.workspace.activeLeaf;
  if (activeLeaf) {
    this.app.workspace.moveLeafToPopout(activeLeaf, {
      x: 200,
      y: 200,
    });
  }
}
```

### Events

```typescript
this.registerEvent(
  this.app.workspace.on('window-open', (win, window) => {
    console.log('New pop-out window opened');
  })
);

this.registerEvent(
  this.app.workspace.on('window-close', (win, window) => {
    console.log('Pop-out window closed');
  })
);
```

---

## Leaf Groups and Linked Panes

Linked panes scroll together. They share a group identifier.

### Setting a Group

```typescript
const leafA = this.app.workspace.getLeaf('tab');
const leafB = this.app.workspace.getLeaf('tab');

leafA.setGroup('my-group');
leafB.setGroup('my-group');
```

### Linking Two Leaves

```typescript
leafA.setGroupMember(leafB);
// leafA now shares leafB's group automatically
```

### Getting Group Leaves

```typescript
const groupLeaves = this.app.workspace.getGroupLeaves('my-group');
```

> [!note]
> Grouping is most commonly used for preview/source linking in Markdown, but you can use it for any custom views that need synchronized scroll or state.

---

## Workspace Events

Subscribe to workspace events via `this.app.workspace.on()` and always register the returned `EventRef` with `this.registerEvent()` so it unloads cleanly.

### `active-leaf-change`

Fired when the focused leaf changes.

```typescript
this.registerEvent(
  this.app.workspace.on('active-leaf-change', (leaf: WorkspaceLeaf | null) => {
    console.log('Active leaf:', leaf?.view?.getViewType());
  })
);
```

### `layout-change`

Fired when the workspace layout is modified (splits created/destroyed, leaves moved, sidebars toggled).

```typescript
this.registerEvent(
  this.app.workspace.on('layout-change', () => {
    console.log('Workspace layout changed');
  })
);
```

### `file-open`

Fired when the active file changes. The file may open in a new leaf, an existing leaf, or an embed.

```typescript
this.registerEvent(
  this.app.workspace.on('file-open', (file: TFile | null) => {
    if (file) {
      console.log('Opened:', file.path);
    }
  })
);
```

### `resize`

Fired when a workspace item is resized or the layout changes.

```typescript
this.registerEvent(
  this.app.workspace.on('resize', () => {
    // Recalculate custom canvas sizes, etc.
  })
);
```

### Other Events

| Event | Description |
|-------|-------------|
| `window-open` | A new pop-out window was created |
| `window-close` | A pop-out window was closed |
| `css-change` | The app's CSS changed (theme switch, snippet reload) |
| `editor-change` | Editor content changed (programmatically or by user) |
| `editor-paste` | Paste event in editor |
| `editor-drop` | Drop event in editor |
| `quit` | App is about to quit (best-effort cleanup) |

---

## Quick Patterns

### Singleton Sidebar View

```typescript
async activateView() {
  const { workspace } = this.app;
  const leaves = workspace.getLeavesOfType(VIEW_TYPE_DASHBOARD);

  if (leaves.length > 0) {
    workspace.revealLeaf(leaves[0]);
    return;
  }

  const leaf = workspace.getRightLeaf(false);
  if (leaf) {
    await leaf.setViewState({ type: VIEW_TYPE_DASHBOARD, active: true });
    workspace.revealLeaf(leaf);
  }
}
```

### Open File Adjacent to Current

```typescript
const file = this.app.vault.getAbstractFileByPath('Other.md') as TFile;
const leaf = this.app.workspace.getLeaf('split', 'vertical');
await leaf.openFile(file);
```

### Close All Custom Views on Unload

```typescript
onunload() {
  this.app.workspace.detachLeavesOfType(VIEW_TYPE_DASHBOARD);
}
```

### React to Deferred Tabs

```typescript
for (const leaf of this.app.workspace.getLeavesOfType('markdown')) {
  if (leaf.isDeferred) {
    await leaf.loadIfDeferred();
  }
}
```

---

## References

- [Workspace TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/Workspace) — Full `Workspace` class reference
- [WorkspaceLeaf TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/WorkspaceLeaf) — Leaf properties and methods
- [ItemView TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/ItemView) — Base for custom views
- [FileView TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/FileView) — Base for file-backed views
- [TextFileView TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/TextFileView) — Base for custom text editors
- [MarkdownView TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/MarkdownView) — Built-in markdown editor
- [Workspace User Interface Docs](https://docs.obsidian.md/Plugins/User+interface/Workspace) — Official guide to workspace concepts
- [obsidian.d.ts](https://github.com/obsidianmd/obsidian-api/blob/master/obsidian.d.ts) — Canonical TypeScript definitions
