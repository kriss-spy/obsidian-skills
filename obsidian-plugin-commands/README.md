# obsidian-plugin-commands

Focused skill for registering and managing Obsidian plugin commands.

## What it covers

- `addCommand()` registration and the `Command` interface
- `callback` — simple global commands
- `editorCallback` — editor-aware text commands
- `checkCallback` — conditional global commands
- `editorCheckCallback` — conditional editor commands
- Default hotkeys, modifiers, and `repeatable`
- Command palette behavior and visibility
- `removeCommand()` for dynamic command management
- Patterns for choosing the right command type
- Mobile and performance considerations

## When to use

Use this skill when you need to add, configure, or debug commands in an Obsidian plugin. It does not cover plugin bootstrapping, settings, views, or release workflows — see `obsidian-plugin-bootstrap` and `obsidian-plugin-dev` for those topics.
