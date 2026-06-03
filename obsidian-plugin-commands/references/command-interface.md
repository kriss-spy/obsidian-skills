# Command Interface Reference

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `string` | Yes | Unique identifier within the plugin. |
| `name` | `string` | Yes | Human-friendly name for the Command Palette. |
| `callback` | `() => any` | No | Simple global callback. |
| `checkCallback` | `(checking: boolean) => boolean \| void` | No | Conditional global callback. |
| `editorCallback` | `(editor: Editor, ctx: MarkdownView \| MarkdownFileInfo) => any` | No | Editor-only callback. |
| `editorCheckCallback` | `(checking: boolean, editor: Editor, ctx: MarkdownView \| MarkdownFileInfo) => boolean \| void` | No | Conditional editor callback. |
| `hotkeys` | `Hotkey[]` | No | Default keyboard shortcuts. |
| `icon` | `IconName` | No | Icon for toolbar integration. |
| `mobileOnly` | `boolean` | No | Restrict to mobile. |
| `repeatable` | `boolean` | No | Repeat while holding hotkey. |

## Callback Precedence

If multiple callbacks are provided, Obsidian uses the first available in this order:

1. `editorCheckCallback`
2. `editorCallback`
3. `checkCallback`
4. `callback`

## Source

- [Command — TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/Command)
