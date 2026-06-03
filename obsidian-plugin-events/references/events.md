# Official Obsidian Docs — Events

Extracted from https://docs.obsidian.md/ for reference. These are thin summaries; see the live docs for the latest details.

## Component Registration Methods

- `register(cb)` — Registers a custom cleanup callback called on unload.
- `registerEvent(eventRef)` — Registers an Obsidian event to be detached on unload.
- `registerDomEvent(el, type, callback, options?)` — Registers a DOM listener to be removed on unload.
- `registerInterval(id)` — Registers an interval ID to be cancelled on unload.
- `registerScopeEvent(keyHandler)` — Registers a keyboard event handler to be unregistered on unload.

## Vault Events

- `create` — Fired for every existing file at vault load, and for newly created files.
- `modify` — Fired when a file is modified.
- `delete` — Fired when a file is deleted.
- `rename` — Fired when a file is renamed. Callback receives `(file, oldPath)`.

## Workspace Events

- `active-leaf-change` — Active leaf changed.
- `layout-change` — Workspace layout changed.
- `file-open` — Active file changed. Callback receives `TFile | null`.
- `editor-change` — Editor content changed.
- `editor-paste` — Paste in editor. Check `evt.defaultPrevented`.
- `editor-drop` — Drop in editor. Check `evt.defaultPrevented`.
- `resize` — Workspace item resized or layout changed.
- `window-open` — Popout window opened (desktop).
- `window-close` — Popout window closed (desktop).
- `css-change` — App CSS changed.

## MetadataCache Events

- `changed` — File indexed and cache available. Not fired on rename.
- `resolve` — File resolved for links.
- `resolved` — All files resolved.
- `deleted` — File deleted. Previous cache may be `null`.
