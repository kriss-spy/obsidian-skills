# obsidian-plugin-modals

A focused skill for building modal dialogs, suggestion popups, and context menus in Obsidian plugins.

## What This Skill Provides

1. **Modal Base Class** — Lifecycle (`onOpen`, `onClose`), `contentEl`, cleanup patterns
2. **Prompt Modals** — Simple text-input dialogs with callback patterns
3. **SuggestModal** — Filtered suggestion lists with custom rendering
4. **FuzzySuggestModal** — Fuzzy-matched search with built-in highlighting
5. **ConfirmationModal** — Ready-made confirm/cancel dialogs (1.13.0+)
6. **Menu / Context Menus** — `addItem`, `addSeparator`, `showAtMouseEvent`, `showAtPosition`
7. **Patterns** — Returning data, chaining modals, Promise wrappers, mobile considerations

## Installation

```bash
npx skills add kriss-spy/obsidian-skills --skill obsidian-plugin-modals
```

## When to Use This Skill

Use this skill when:
- Creating a custom popup or form dialog
- Building an autocomplete file/tag/object picker
- Adding fuzzy search to a plugin command
- Implementing confirmation dialogs before destructive actions
- Adding right-click context menus to custom views
- Chaining multiple modal steps into a wizard flow

## Resources

- `SKILL.md` — Complete API reference and code examples
- `references/` — Thin reference docs for key classes

## Trigger Phrases

This skill activates on:
- "obsidian plugin modal"
- "obsidian plugin suggest modal"
- "obsidian plugin fuzzy suggest"
- "obsidian plugin context menu"
- "obsidian plugin prompt"
- "obsidian plugin picker"
- "obsidian plugin confirmation dialog"
- "obsidian plugin menu"

## Version

1.0.0 — Initial release covering Modal, SuggestModal, FuzzySuggestModal, ConfirmationModal, and Menu.

## Author

OpenCode
