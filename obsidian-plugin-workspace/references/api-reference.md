# Workspace API Quick Reference

## Workspace Class

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `activeEditor` | `MarkdownFileInfo \| null` | Current editor component (v1.7.2+) |
| `activeLeaf` | `WorkspaceLeaf \| null` | Currently focused leaf (avoid direct use) |
| `containerEl` | `HTMLElement` | Root workspace DOM element |
| `layoutReady` | `boolean` | Whether layout has initialized |
| `leftRibbon` | `WorkspaceRibbon` | Left ribbon |
| `leftSplit` | `WorkspaceSidedock \| WorkspaceMobileDrawer` | Left sidebar |
| `rightRibbon` | `WorkspaceRibbon` | Right ribbon |
| `rightSplit` | `WorkspaceSidedock \| WorkspaceMobileDrawer` | Right sidebar |
| `rootSplit` | `WorkspaceRoot` | Main workspace area |

### Leaf Factory Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `getLeaf` | `(newLeaf?: PaneType \| boolean, direction?: SplitDirection): WorkspaceLeaf` | Create or reuse a leaf |
| `getLeftLeaf` | `(split: boolean): WorkspaceLeaf \| null` | Create leaf in left sidebar |
| `getRightLeaf` | `(split: boolean): WorkspaceLeaf \| null` | Create leaf in right sidebar |
| `createLeafInParent` | `(parent: WorkspaceSplit, index: number): WorkspaceLeaf` | Insert leaf into a specific split |
| `ensureSideLeaf` | `(type: string, side: Side, options?): Promise<WorkspaceLeaf>` | Get or create sidebar leaf (v1.7.2+) |
| `openPopoutLeaf` | `(data?: WorkspaceWindowInitData): WorkspaceLeaf` | New pop-out window leaf (desktop) |
| `moveLeafToPopout` | `(leaf: WorkspaceLeaf, data?): WorkspaceWindow` | Move existing leaf to pop-out (desktop) |

### Discovery Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `getActiveFile` | `(): TFile \| null` | Active file (fallbacks to most recent) |
| `getActiveViewOfType` | `<T>(type: Constructor<T>): T \| null` | Active view matching type |
| `getLeavesOfType` | `(viewType: string): WorkspaceLeaf[]` | All leaves of a given view type |
| `getGroupLeaves` | `(group: string): WorkspaceLeaf[]` | All leaves in a group |
| `getLeafById` | `(id: string): WorkspaceLeaf \| null` | Leaf by ID |
| `getMostRecentLeaf` | `(root?: WorkspaceRoot \| WorkspaceWindow): WorkspaceLeaf \| null` | Most recent leaf in a root |

### Layout Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `detachLeavesOfType` | `(viewType: string): void` | Remove all leaves of a type |
| `revealLeaf` | `(leaf: WorkspaceLeaf): Promise<void>` | Focus and uncollapse sidebar if needed |
| `setActiveLeaf` | `(leaf: WorkspaceLeaf, params?: { focus?: boolean }): void` | Programmatically focus a leaf |
| `createLeafBySplit` | `(leaf: WorkspaceLeaf, direction?, before?): WorkspaceLeaf` | Split an existing leaf |
| `splitActiveLeaf` | `(direction?: SplitDirection): WorkspaceLeaf` | Split the active leaf |
| `duplicateLeaf` | `(leaf: WorkspaceLeaf, leafType?, direction?): Promise<WorkspaceLeaf>` | Duplicate a leaf |
| `changeLayout` | `(workspace: unknown): Promise<void>` | Restore a saved layout |
| `getLayout` | `(): unknown` | Serialize current layout |

### Navigation

| Method | Signature | Description |
|--------|-----------|-------------|
| `openLinkText` | `(linktext, sourcePath, newLeaf?, openViewState?): Promise<void>` | Open a wikilink |
| `openFile` (on leaf) | `(file: TFile, openState?): Promise<void>` | Open a file in a specific leaf |

### Iteration

| Method | Signature | Description |
|--------|-----------|-------------|
| `iterateAllLeaves` | `(callback: (leaf) => void): void` | All leaves including sidebars and pop-outs |
| `iterateRootLeaves` | `(callback: (leaf) => void): void` | Only main area leaves |

## WorkspaceLeaf Class

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `parent` | `WorkspaceTabs \| WorkspaceMobileDrawer` | Container |
| `view` | `View` | Current view (check `instanceof` before casting) |
| `hoverPopover` | `HoverPopover \| null` | Active hover popover |
| `isDeferred` | `boolean` | Whether tab is backgrounded (v1.7.2+) |

### Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `setViewState` | `(state: ViewState, eState?: any): Promise<void>` | Open a view type |
| `getViewState` | `(): ViewState` | Current view state |
| `openFile` | `(file: TFile, openState?: OpenViewState): Promise<void>` | Open a file |
| `open` | `(view: View): Promise<View>` | Open a specific view instance |
| `detach` | `(): void` | Destroy the leaf |
| `setPinned` | `(pinned: boolean): void` | Pin/unpin |
| `togglePinned` | `(): void` | Toggle pinned |
| `setGroup` | `(group: string): void` | Set group ID |
| `setGroupMember` | `(other: WorkspaceLeaf): void` | Link to another leaf's group |
| `getIcon` | `(): IconName` | Leaf icon |
| `getDisplayText` | `(): string` | Leaf title text |
| `getEphemeralState` | `(): any` | Get ephemeral state |
| `setEphemeralState` | `(state: any): void` | Set ephemeral state |
| `loadIfDeferred` | `(): Promise<void>` | Force load if deferred (v1.7.2+) |

## View Hierarchy

### View (abstract)

| Member | Type | Description |
|--------|------|-------------|
| `app` | `App` | Application instance |
| `icon` | `IconName` | View icon |
| `navigation` | `boolean` | Whether the view is navigable |
| `leaf` | `WorkspaceLeaf` | Hosting leaf |
| `containerEl` | `HTMLElement` | Root DOM element |
| `scope` | `Scope \| null` | Optional hotkey scope |
| `getViewType()` | `abstract string` | Unique view type ID |
| `onOpen()` | `Promise<void>` | Lifecycle: view opened |
| `onClose()` | `Promise<void>` | Lifecycle: view closed |
| `getState()` | `Record<string, unknown>` | Serialize state |
| `setState()` | `(state, result): Promise<void>` | Restore state |
| `getIcon()` | `IconName` | Icon for this view |
| `onResize()` | `void` | Size changed |

### ItemView (extends View)

| Member | Type | Description |
|--------|------|-------------|
| `contentEl` | `HTMLElement` | DOM container below the header |
| `addAction()` | `(icon, title, callback): HTMLElement` | Add header action button |

### FileView (extends ItemView)

| Member | Type | Description |
|--------|------|-------------|
| `allowNoFile` | `boolean` | Whether the view can exist without a file |
| `file` | `TFile \| null` | Currently loaded file |
| `navigation` | `boolean` | `true` by default for file views |
| `getDisplayText()` | `string` | Title derived from file |
| `onLoadFile()` | `(file: TFile): Promise<void>` | File loaded into view |
| `onUnloadFile()` | `(file: TFile): Promise<void>` | File removed from view |
| `onRename()` | `(file: TFile): Promise<void>` | File was renamed |
| `canAcceptExtension()` | `(ext: string): boolean` | Whether this view handles a file extension |
| `getState()` / `setState()` | | Include file path in state |

### TextFileView (extends EditableFileView → FileView)

| Member | Type | Description |
|--------|------|-------------|
| `data` | `string` | In-memory file contents |
| `requestSave` | `() => void` | Debounced save trigger |
| `getViewData()` | `abstract string` | Read editor contents |
| `setViewData()` | `(data: string, clear: boolean): void` | Load contents into editor |
| `clear()` | `abstract void` | Clear undo history and caches |
| `save()` | `(clear?: boolean): Promise<void>` | Save to disk |

### MarkdownView (extends TextFileView)

| Member | Type | Description |
|--------|------|-------------|
| `editor` | `Editor` | CodeMirror editor instance |
| `previewMode` | `MarkdownPreviewView` | Reading mode renderer |
| `currentMode` | `MarkdownSubView` | Active sub-view (source/preview) |
| `getViewType()` | `string` | Returns `'markdown'` |
| `getMode()` | `MarkdownViewModeType` | `'source'` or `'preview'` |
| `showSearch()` | `(replace?: boolean): void` | Open find/replace |

## Plugin Registration

| Method | Signature | Description |
|--------|-----------|-------------|
| `registerView` | `(type: string, viewCreator: ViewCreator): void` | Register a custom view factory |
| `registerExtensions` | `(extensions: string[], viewType: string): void` | Bind file extensions to a view |
| `registerHoverLinkSource` | `(id: string, info: HoverLinkSource): void` | Enable Page Preview hover for your view |

## ViewState

```typescript
interface ViewState {
  type: string;
  state?: Record<string, unknown>;
  active?: boolean;
  pinned?: boolean;
  group?: WorkspaceLeaf;
}
```

## Workspace Events

| Event | Callback | Description |
|-------|----------|-------------|
| `active-leaf-change` | `(leaf: WorkspaceLeaf \| null) => any` | Focused leaf changed |
| `file-open` | `(file: TFile \| null) => any` | Active file changed |
| `layout-change` | `() => any` | Splits/tabs/sidebars modified |
| `window-open` | `(win: WorkspaceWindow, window: Window) => any` | Pop-out opened |
| `window-close` | `(win: WorkspaceWindow, window: Window) => any` | Pop-out closed |
| `resize` | `() => any` | Item resized or layout changed |
| `css-change` | `() => any` | Theme/CSS updated |
| `editor-change` | `(editor: Editor) => any` | Editor content changed |
| `editor-paste` | `(evt: ClipboardEvent, editor: Editor, view: MarkdownView) => any` | Paste in editor |
| `editor-drop` | `(evt: DragEvent, editor: Editor, view: MarkdownView) => any` | Drop in editor |
| `quit` | `() => any` | App about to quit |

## Common Types

```typescript
type SplitDirection = 'vertical' | 'horizontal';
type PaneType = 'tab' | 'split' | 'window';
type Side = 'left' | 'right';
type MarkdownViewModeType = 'source' | 'preview' | 'live';
type ViewCreator = (leaf: WorkspaceLeaf) => View;
```
