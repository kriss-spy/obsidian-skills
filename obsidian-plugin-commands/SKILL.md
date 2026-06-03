---
name: obsidian-plugin-commands
description: Register and manage commands in Obsidian plugins. Covers addCommand(), callback variants, conditional commands, default hotkeys, command palette integration, removeCommand(), and patterns for choosing the right command type. Use when adding commands to a plugin, configuring hotkeys, or making commands context-sensitive.
triggers:
  - obsidian plugin command
  - obsidian plugin addCommand
  - obsidian plugin hotkey
  - obsidian plugin command palette
  - obsidian plugin conditional command
  - obsidian plugin editor command
  - obsidian plugin removeCommand
  - obsidian plugin callback
  - obsidian plugin checkCallback
  - obsidian plugin editorCallback
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Commands

This skill focuses on registering, managing, and optimizing commands within an Obsidian plugin. Commands are the primary way users interact with plugins through the Command Palette and keyboard shortcuts.

## When to Use This Skill

- Adding a new command to an Obsidian plugin
- Choosing between `callback`, `editorCallback`, `checkCallback`, and `editorCheckCallback`
- Configuring default hotkeys for plugin commands
- Making commands context-sensitive (appear only when conditions are met)
- Dynamically adding or removing commands at runtime
- Understanding command palette behavior and mobile constraints

## Overview

Commands in Obsidian are actions users invoke from the Command Palette (Ctrl/Cmd+P) or via hotkeys. Every command is registered through `Plugin.addCommand()` inside `onload()`. The API provides four callback flavors that determine when and how a command executes:

| Callback | Context Required | Conditional | Use Case |
|----------|-----------------|-------------|----------|
| `callback` | None | No | Global actions: open modals, toggle settings, run vault-wide operations |
| `checkCallback` | None | Yes | Global actions that only make sense in certain states |
| `editorCallback` | Active editor | No | Text manipulation: insert, replace, format |
| `editorCheckCallback` | Active editor | Yes | Text manipulation that depends on cursor state, selection, or file type |

The command `id` and `name` are automatically prefixed with your plugin's ID and name. You only supply the local portion.

---

## `addCommand()` Registration

Register commands inside `onload()`. The return value is a `Command` object, though you rarely need to hold onto it.

```typescript
import { Plugin, Notice } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    this.addCommand({
      id: 'say-hello',
      name: 'Say hello',
      callback: () => {
        new Notice('Hello from the plugin!');
      },
    });
  }
}
```

**Required fields:**
- `id` — unique within your plugin. Lowercase letters, numbers, and hyphens recommended.
- `name` — human-friendly string shown in the Command Palette.

**Optional fields:**
- `callback` / `checkCallback` / `editorCallback` / `editorCheckCallback` — exactly one should be provided.
- `hotkeys` — array of default hotkey objects.
- `icon` — icon ID for ribbon toolbar integration.
- `mobileOnly` — if `true`, the command only appears on mobile.
- `repeatable` — if `true`, holding the hotkey repeats the command.

> [!note]
> If you provide multiple callbacks, the precedence is: `editorCheckCallback` > `editorCallback` > `checkCallback` > `callback`.

---

## Simple Commands (`callback`)

Use `callback` for actions that do not depend on the active editor and are always available.

```typescript
this.addCommand({
  id: 'open-settings',
  name: 'Open plugin settings',
  callback: () => {
    // Open the plugin's setting tab
    (this.app as any).setting.open();
    (this.app as any).setting.openTabById(this.manifest.id);
  },
});
```

Common use cases:
- Opening modals or custom views
- Toggling plugin settings
- Running vault-wide searches or operations
- Triggering file creation outside the editor context

```typescript
this.addCommand({
  id: 'create-daily-note',
  name: 'Create daily note',
  callback: async () => {
    const date = window.moment().format('YYYY-MM-DD');
    const path = `Daily/${date}.md`;
    const existing = this.app.vault.getAbstractFileByPath(path);
    if (!existing) {
      await this.app.vault.create(path, `# ${date}\n\n`);
    }
    await this.app.workspace.openLinkText(path, '', false);
  },
});
```

---

## Editor Commands (`editorCallback`)

Use `editorCallback` when your command manipulates text. It only appears in the Command Palette when an editor is active.

```typescript
import { Plugin, Editor, MarkdownView } from 'obsidian';

this.addCommand({
  id: 'wrap-bold',
  name: 'Wrap selection in bold',
  editorCallback: (editor: Editor, view: MarkdownView) => {
    const selection = editor.getSelection();
    editor.replaceSelection(`**${selection}**`);
  },
});
```

**Arguments:**
- `editor` — the active `Editor` instance. Provides `getSelection()`, `replaceSelection()`, `getCursor()`, `replaceRange()`, etc.
- `view` — the parent `MarkdownView` or `MarkdownFileInfo`. Use it to access `file` or check view state.

> [!tip]
> If your command needs the file path, access it through `view.file`:
> ```typescript
> editorCallback: (editor, view) => {
>   const file = view.file;
>   if (file) {
>     new Notice(`Editing ${file.basename}`);
>   }
> }
> ```

---

## Conditional Commands

### `checkCallback`

Use `checkCallback` when a command's availability depends on runtime state (e.g., a file is open, a setting is enabled). The callback runs **twice**:

1. **`checking: true`** — Obsidian is probing whether the command should appear in the Command Palette. Do not perform side effects. Return `true` if the command should be shown, `false` or `undefined` to hide it.
2. **`checking: false`** — The user triggered the command. Perform the action.

```typescript
this.addCommand({
  id: 'copy-file-path',
  name: 'Copy active file path to clipboard',
  checkCallback: (checking: boolean) => {
    const activeFile = this.app.workspace.getActiveFile();
    if (activeFile) {
      if (!checking) {
        navigator.clipboard.writeText(activeFile.path);
        new Notice('Path copied');
      }
      return true;
    }
    return false;
  },
});
```

> [!important]
> Always perform the condition check in **both** branches. Time may pass between the check and the execution, so state can change.

### `editorCheckCallback`

Same two-phase behavior as `checkCallback`, but only evaluated when an editor is active. It receives the `editor` and `view` arguments in addition to `checking`.

```typescript
this.addCommand({
  id: 'sort-selected-lines',
  name: 'Sort selected lines alphabetically',
  editorCheckCallback: (checking: boolean, editor: Editor, view: MarkdownView) => {
    const selection = editor.getSelection();
    if (selection.length > 0) {
      if (!checking) {
        const sorted = selection.split('\n').sort().join('\n');
        editor.replaceSelection(sorted);
      }
      return true;
    }
    return false;
  },
});
```

> [!caution]
> Do not put heavy computations in the `checking: true` path. It runs frequently while the Command Palette is open. Keep checks lightweight.

---

## Default Hotkeys

You can assign default hotkeys that users can later override in Settings → Hotkeys.

```typescript
this.addCommand({
  id: 'toggle-focus-mode',
  name: 'Toggle focus mode',
  hotkeys: [
    {
      modifiers: ['Mod', 'Shift'],
      key: 'f',
    },
  ],
  callback: () => {
    document.body.classList.toggle('focus-mode');
  },
});
```

**Modifier values:**
- `'Mod'` — Ctrl on Windows/Linux, Cmd on macOS
- `'Ctrl'` — Ctrl on all platforms
- `'Meta'` — Windows key on Windows, Cmd on macOS
- `'Alt'` — Alt/Option
- `'Shift'` — Shift

**Key values:** Any single character (`'a'`, `'1'`, `'/'`), or special keys like `'Enter'`, `'Escape'`, `'ArrowUp'`, `'ArrowDown'`, `'Tab'`, `'Backspace'`, `'Delete'`.

> [!warning]
> Avoid setting default hotkeys for plugins intended for public distribution. They conflict easily with user mappings and other plugins. If you must, choose obscure combinations and document them.

### Multiple Hotkeys

A command can have multiple default hotkeys:

```typescript
hotkeys: [
  { modifiers: ['Mod'], key: 'm' },
  { modifiers: ['Mod', 'Shift'], key: 'm' },
],
```

### `repeatable`

Set `repeatable: true` to allow holding the hotkey to repeatedly trigger the command:

```typescript
this.addCommand({
  id: 'increase-heading',
  name: 'Increase heading level',
  repeatable: true,
  editorCallback: (editor) => {
    // ... logic to increase heading depth
  },
});
```

---

## Command Palette Integration

Once registered, commands appear automatically in Obsidian's Command Palette (Ctrl/Cmd+P). The display name is prefixed with your plugin name:

```
My Plugin: Say hello
My Plugin: Wrap selection in bold
```

Users can:
- Search by name or plugin name
- Assign custom hotkeys via Settings → Hotkeys
- Remove default hotkeys if they conflict

> [!note]
> Commands hidden by `checkCallback` returning `false` will not show up in the Command Palette at all. This is the cleanest way to create context-sensitive commands.

---

## `removeCommand()` for Dynamic Management

If your plugin registers commands dynamically (e.g., based on settings or external state), use `removeCommand()` to clean them up.

```typescript
export default class MyPlugin extends Plugin {
  async onload() {
    this.addCommand({
      id: 'feature-a',
      name: 'Run feature A',
      callback: () => this.runFeatureA(),
    });
  }

  enableFeatureB() {
    this.addCommand({
      id: 'feature-b',
      name: 'Run feature B',
      callback: () => this.runFeatureB(),
    });
  }

  disableFeatureB() {
    this.removeCommand('feature-b');
  }
}
```

> [!tip]
> Prefer static command registration in `onload()` when possible. Static commands are simpler and automatically cleaned up on plugin unload. Use dynamic registration sparingly.

---

## Patterns and Best Practices

### Choosing the Right Callback

| Scenario | Recommended Callback |
|----------|---------------------|
| Always available, no editor needed | `callback` |
| Always available, but only in certain app states | `checkCallback` |
| Text insertion or transformation | `editorCallback` |
| Text transformation that needs a valid selection or cursor context | `editorCheckCallback` |

### Mobile Considerations

- The Command Palette works on mobile, but hotkeys are impractical without a physical keyboard.
- Consider adding ribbon icons or menu items as alternative entry points for command functionality.
- `mobileOnly` can hide desktop-only commands, but it is rarely needed. Most commands should work on both platforms.

### Naming and IDs

- Keep `id` stable after release. Changing it breaks user hotkey assignments.
- Use descriptive `name` values. Users search the Command Palette by name.
- Prefix `id` with a short domain if your plugin has many commands: `insert-date`, `insert-time`, `format-table`.

### Performance

- Keep `checkCallback` and `editorCheckCallback` checks fast. They run on every Command Palette open and while typing.
- Do not access the vault or network in check callbacks.
- Cache any derived state needed for checks (e.g., a settings flag) rather than recomputing it.

---

## Quick Reference Checklist

- [ ] Command has a unique `id` within the plugin
- [ ] Command has a clear, searchable `name`
- [ ] Correct callback type chosen for the use case
- [ ] `checkCallback` / `editorCheckCallback` checks are lightweight
- [ ] `checkCallback` / `editorCheckCallback` perform the condition check in both `checking` branches
- [ ] Default hotkeys are avoided for public plugins, or use obscure combinations
- [ ] `removeCommand()` is used if commands are registered dynamically
- [ ] Commands are registered in `onload()`

---

## References

- [Commands — User interface](https://docs.obsidian.md/Plugins/User+interface/Commands) — Official guide to command registration
- [Command — TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/Command) — Full `Command` interface reference
- [Plugin.addCommand()](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/addCommand) — API method reference
- [Plugin.removeCommand()](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/removeCommand) — Dynamic command removal
- [Hotkey — TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/Hotkey) — Hotkey object schema
- [Plugin guidelines](https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines) — Best practices for releasing plugins
