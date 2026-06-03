# obsidian-plugin-events

Event handling and resource cleanup for Obsidian plugins. Covers Component resource management, registerEvent, registerDomEvent, registerInterval, registerScopeEvent, register, vault events, workspace events, metadata cache events, and memory leak prevention.

## What This Skill Covers

- Understanding the `Component` lifecycle and automatic cleanup model
- Using `registerEvent()` for Obsidian internal events (vault, workspace, metadata cache)
- Using `registerDomEvent()` for DOM listeners on persistent elements
- Using `registerInterval()` for auto-cancelling timers
- Using `registerScopeEvent()` for keyboard shortcuts within a `Scope`
- Using `register()` for custom cleanup callbacks
- Vault events: `create`, `modify`, `delete`, `rename`
- Workspace events: `active-leaf-change`, `layout-change`, `file-open`, `editor-change`, `editor-paste`, `editor-drop`, `resize`, `window-open`, `window-close`, `css-change`
- MetadataCache events: `changed`, `resolve`, `resolved`, `deleted`
- Best practices for preventing memory leaks and respecting other plugins

## When to Use

Use this skill when adding event listeners to an Obsidian plugin, reacting to file or UI changes, or debugging resource leaks during plugin unload.
