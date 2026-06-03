# Official Obsidian Docs — Getting Started

Extracted from https://docs.obsidian.md/ for reference. These are thin summaries; see the live docs for the latest details.

## Build a Plugin

- Prerequisites: Git, Node.js, code editor
- Always use a separate dev vault (never your main vault)
- Clone `obsidian-sample-plugin` into `.obsidian/plugins/`
- Run `npm install` then `npm run dev`
- Enable the plugin in Settings → Community Plugins
- Update `manifest.json` to set a unique `id` and `name`
- Restart Obsidian when changing `manifest.json`
- Reload the plugin after source changes (disable/enable, or use Hot-Reload)

## Anatomy of a Plugin

A plugin consists of:
- `manifest.json` — metadata
- `main.js` — compiled entry point
- `styles.css` — optional styles
- `data.json` — auto-generated settings storage

## Development Workflow

- `npm run dev` watches for changes and rebuilds
- `npm run build` creates a production bundle
- Install the Hot-Reload plugin for automatic reloading
- Use Developer Tools (`Ctrl/Cmd+Shift+I`) for debugging
- `this.app.emulateMobile(true)` to test mobile UI on desktop

## Mobile Development

- Node.js and Electron APIs are unavailable on mobile
- Use `Platform.isIosApp`, `Platform.isAndroidApp`, `Platform.isDesktopApp` to guard code
- `isDesktopOnly: true` in `manifest.json` prevents mobile installation
- Lookbehind regex is only supported on iOS 16.4+
- Inspect Android via `chrome://inspect` with USB debugging
- Inspect iOS via Safari Web Inspector (iOS 16.4+, macOS required)
