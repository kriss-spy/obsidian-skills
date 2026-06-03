# obsidian-plugin-settings

An OpenCode skill for designing and implementing Obsidian plugin settings UI and persistence.

## What it covers

- `PluginSettingTab` — declarative (`getSettingDefinitions()`) and imperative (`display()`) APIs
- `Setting` class — all input types: text, textarea, toggle, slider, dropdown, color picker, button, moment format, search, progress bar, extra button
- `loadData()` / `saveData()` — persisting settings to `data.json`
- Settings interfaces, defaults, and load-time sanitization
- Async `onChange` handling and debouncing
- Declarative settings migration from imperative tabs
- Patterns: grouping, validation, dynamic settings, conditional visibility, mobile UI considerations
- Settings inside modals

## When to use

Use this skill whenever you need to:
- Add or refactor a plugin's settings tab
- Choose the right input control for a configuration option
- Migrate an old imperative settings tab to the modern declarative API
- Validate user input, group settings, or show/hide fields conditionally
- Handle external settings changes (sync) or runtime configuration updates

## Files

- `SKILL.md` — Main skill documentation with code snippets and patterns
- `references/` — Thin reference docs for quick lookup
