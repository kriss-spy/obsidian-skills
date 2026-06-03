# obsidian-plugin-react

Integrate React into Obsidian plugins. Covers dependency setup, TypeScript and esbuild JSX configuration, mounting and unmounting React components in views, modals, and settings tabs, bridging Obsidian events and state into React, and preventing memory leaks with proper cleanup.

## What This Skill Covers

- Installing `react`, `react-dom`, and type definitions
- Configuring `tsconfig.json` and esbuild for JSX
- Mounting React components with `createRoot` in `ItemView`, `Modal`, and `PluginSettingTab`
- Unmounting roots to prevent memory leaks
- Bridging Obsidian events into React with hooks and refs
- Passing `App` and plugin state via React Context or external stores
- Cleanup discipline in `onClose()`, `hide()`, and `onunload()`

## When to Use

Use this skill when you need to add React-based UI to an Obsidian plugin, convert a vanilla view to React, or manage complex component state inside Obsidian's UI surfaces.
