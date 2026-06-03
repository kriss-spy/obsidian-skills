---
name: obsidian-plugin-modals
description: Build modal dialogs, suggestion modals, and context menus for Obsidian plugins. Covers Modal, SuggestModal, FuzzySuggestModal, ConfirmationModal, Menu, and patterns for returning data, chaining, and cleanup. Use when implementing user-facing popups, pickers, prompts, or right-click menus.
triggers:
  - obsidian plugin modal
  - obsidian plugin suggest modal
  - obsidian plugin fuzzy suggest
  - obsidian plugin context menu
  - obsidian plugin prompt
  - obsidian plugin picker
  - obsidian plugin confirmation dialog
  - obsidian plugin menu
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Modals

This skill covers building modal dialogs, suggestion popups, and context menus in Obsidian plugins. It focuses on the concrete API classes you extend or instantiate, the lifecycle hooks you implement, and the patterns that keep modal code maintainable.

## When to Use This Skill

- Building a custom popup that accepts user input
- Creating an autocomplete-style picker over a list of files, tags, or custom objects
- Adding fuzzy search to a command palette-like experience
- Showing confirmation dialogs before destructive actions
- Building right-click context menus in custom views or ribbon icons
- Chaining multiple modal steps into a wizard-like flow
- Returning data from a modal back to the calling command or view

## Overview

Obsidian provides a family of modal classes under the `obsidian` package:

| Class | Purpose | Extends |
|-------|---------|---------|
| `Modal` | Generic dialog with a dimmed background | — |
| `SuggestModal<T>` | Filtered, searchable list of suggestions | `Modal` |
| `FuzzySuggestModal<T>` | Fuzzy-matched suggestion list with highlighting | `SuggestModal<FuzzyMatch<T>>` |
| `ConfirmationModal` | Pre-built confirm/cancel dialog (since 1.13.0) | `Modal` |
| `Menu` | Context menu (right-click or triggered dropdown) | `Component` |

All modals are opened with `.open()` and dismissed with `.close()`. On mobile, modals animate onto the screen automatically.

---

## Modal Base Class

Extend `Modal` to build any custom dialog. The two lifecycle methods you must implement are `onOpen()` and `onClose()`.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `app` | `App` | The Obsidian app instance |
| `containerEl` | `HTMLElement` | The outer modal container |
| `modalEl` | `HTMLElement` | The modal content area |
| `contentEl` | `HTMLElement` | The main content element (build UI here) |
| `titleEl` | `HTMLElement` | The title element |
| `scope` | `Scope` | Keyboard event scope (hotkey registration) |
| `shouldRestoreSelection` | `boolean` | Whether to restore editor selection on close |

### Methods

| Method | Description |
|--------|-------------|
| `open()` | Show the modal on the active window |
| `close()` | Hide the modal |
| `onOpen()` | Called when the modal is opened; build UI here |
| `onClose()` | Called when the modal is closed; clean up here |
| `setTitle(title)` | Set the modal title |
| `setContent(content)` | Set plain-text or fragment content |
| `setCloseCallback(callback)` | Register a callback invoked on close |

### Minimal Example

```typescript
import { App, Modal } from 'obsidian';

export class ExampleModal extends Modal {
  constructor(app: App) {
    super(app);
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.setText('Look at me, I\'m a modal! 👀');
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}
```

Usage from a plugin:

```typescript
new ExampleModal(this.app).open();
```

---

## Prompt Modal

The most common use of `Modal` is a simple text-input prompt. Use a constructor callback to pass the result back to the caller.

```typescript
import { App, Modal, Setting } from 'obsidian';

export class PromptModal extends Modal {
  result: string;
  onSubmit: (result: string) => void;

  constructor(app: App, onSubmit: (result: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;

    contentEl.createEl('h2', { text: 'What\'s your name?' });

    new Setting(contentEl)
      .setName('Name')
      .addText((text) =>
        text.onChange((value) => {
          this.result = value;
        }));

    new Setting(contentEl)
      .addButton((btn) =>
        btn
          .setButtonText('Submit')
          .setCta()
          .onClick(() => {
            this.close();
            this.onSubmit(this.result);
          }));
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}
```

Usage:

```typescript
new PromptModal(this.app, (result) => {
  new Notice(`Hello, ${result}!`);
}).open();
```

> [!tip]
> You can also pass the callback into `onOpen()` via a local variable (as in the official docs) instead of storing it on `this`. Both patterns work; storing on `this` is easier when the modal grows into a form with multiple fields.

---

## SuggestModal

`SuggestModal<T>` displays a searchable list of items. The user types into an input field and the list filters in real time.

### Abstract Methods

| Method | Signature | Purpose |
|--------|-----------|---------|
| `getSuggestions` | `getSuggestions(query: string): T[] \| Promise<T[]>` | Return items matching the query |
| `renderSuggestion` | `renderSuggestion(value: T, el: HTMLElement): any` | Render a single suggestion row |
| `onChooseSuggestion` | `onChooseSuggestion(item: T, evt: MouseEvent \| KeyboardEvent): any` | Handle selection |

### Example: Book Picker

```typescript
import { App, Notice, SuggestModal } from 'obsidian';

interface Book {
  title: string;
  author: string;
}

const ALL_BOOKS: Book[] = [
  { title: 'How to Take Smart Notes', author: 'Sönke Ahrens' },
  { title: 'Thinking, Fast and Slow', author: 'Daniel Kahneman' },
  { title: 'Deep Work', author: 'Cal Newport' },
];

export class BookSuggestModal extends SuggestModal<Book> {
  getSuggestions(query: string): Book[] {
    return ALL_BOOKS.filter((book) =>
      book.title.toLowerCase().includes(query.toLowerCase())
    );
  }

  renderSuggestion(book: Book, el: HTMLElement) {
    el.createEl('div', { text: book.title });
    el.createEl('small', { text: book.author });
  }

  onChooseSuggestion(book: Book, evt: MouseEvent | KeyboardEvent) {
    new Notice(`Selected ${book.title}`);
  }
}
```

### Example: File Picker

A common pattern is picking from vault files:

```typescript
import { App, Notice, SuggestModal, TFile } from 'obsidian';

export class FileSuggestModal extends SuggestModal<TFile> {
  getSuggestions(query: string): TFile[] {
    return this.app.vault.getMarkdownFiles()
      .filter(file =>
        file.basename.toLowerCase().includes(query.toLowerCase())
      );
  }

  renderSuggestion(file: TFile, el: HTMLElement) {
    el.createEl('div', { text: file.basename });
    el.createEl('small', { text: file.path });
  }

  onChooseSuggestion(file: TFile, evt: MouseEvent | KeyboardEvent) {
    new Notice(`Selected ${file.path}`);
  }
}
```

> [!note]
> `SuggestModal` does **not** provide fuzzy matching out of the box. If you want fuzzy search, use `FuzzySuggestModal` instead.

---

## FuzzySuggestModal

`FuzzySuggestModal<T>` gives you fuzzy string search with match highlighting automatically. You only supply the item list and a string representation for each item.

### Abstract Methods

| Method | Signature | Purpose |
|--------|-----------|---------|
| `getItems` | `getItems(): T[]` | Return the full list of items |
| `getItemText` | `getItemText(item: T): string` | Return the searchable text for an item |
| `onChooseItem` | `onChooseItem(item: T, evt: MouseEvent \| KeyboardEvent): void` | Handle selection |

### Basic Example

```typescript
import { FuzzySuggestModal, Notice } from 'obsidian';

interface Book {
  title: string;
  author: string;
}

const ALL_BOOKS: Book[] = [
  { title: 'How to Take Smart Notes', author: 'Sönke Ahrens' },
  { title: 'Thinking, Fast and Slow', author: 'Daniel Kahneman' },
  { title: 'Deep Work', author: 'Cal Newport' },
];

export class BookFuzzyModal extends FuzzySuggestModal<Book> {
  getItems(): Book[] {
    return ALL_BOOKS;
  }

  getItemText(book: Book): string {
    return book.title;
  }

  onChooseItem(book: Book, evt: MouseEvent | KeyboardEvent) {
    new Notice(`Selected ${book.title}`);
  }
}
```

### Custom Rendering with `renderResults`

Override `renderSuggestion` to highlight matched substrings using `renderResults()`:

```typescript
import { FuzzyMatch, FuzzySuggestModal, Notice, renderResults } from 'obsidian';

export class CustomBookFuzzyModal extends FuzzySuggestModal<Book> {
  getItems(): Book[] {
    return ALL_BOOKS;
  }

  getItemText(item: Book): string {
    return item.title + ' ' + item.author;
  }

  renderSuggestion(match: FuzzyMatch<Book>, el: HTMLElement) {
    const titleEl = el.createDiv();
    renderResults(titleEl, match.item.title, match.match);

    const authorEl = el.createEl('small');
    const offset = -(match.item.title.length + 1);
    renderResults(authorEl, match.item.author, match.match, offset);
  }

  onChooseItem(book: Book, evt: MouseEvent | KeyboardEvent) {
    new Notice(`Selected ${book.title}`);
  }
}
```

> [!tip]
> `renderResults(container, text, match, offset?)` renders `text` into `container` while highlighting the character ranges specified by `match`. Use `offset` when the rendered text starts at a different position than the string returned by `getItemText`.

---

## FileSuggestModal and FolderSuggestModal Patterns

`FileSuggestModal` and `FolderSuggestModal` are not built-in API classes, but they are common community patterns implemented with `FuzzySuggestModal`.

### File Picker (Fuzzy)

```typescript
import { App, FuzzySuggestModal, TFile } from 'obsidian';

export class FileSuggestModal extends FuzzySuggestModal<TFile> {
  private onSelect: (file: TFile) => void;

  constructor(app: App, onSelect: (file: TFile) => void) {
    super(app);
    this.onSelect = onSelect;
  }

  getItems(): TFile[] {
    return this.app.vault.getMarkdownFiles();
  }

  getItemText(file: TFile): string {
    return file.path;
  }

  onChooseItem(file: TFile, evt: MouseEvent | KeyboardEvent) {
    this.onSelect(file);
  }
}
```

### Folder Picker (Fuzzy)

```typescript
import { App, FuzzySuggestModal, TFolder } from 'obsidian';

export class FolderSuggestModal extends FuzzySuggestModal<TFolder> {
  private onSelect: (folder: TFolder) => void;

  constructor(app: App, onSelect: (folder: TFolder) => void) {
    super(app);
    this.onSelect = onSelect;
  }

  getItems(): TFolder[] {
    return this.app.vault.getRoot().children
      .filter((f): f is TFolder => f instanceof TFolder);
  }

  getItemText(folder: TFolder): string {
    return folder.name + '/';
  }

  onChooseItem(folder: TFolder, evt: MouseEvent | KeyboardEvent) {
    this.onSelect(folder);
  }
}
```

---

## ConfirmationModal

`ConfirmationModal` (available since Obsidian 1.13.0) provides a ready-made confirm/cancel dialog. Buttons auto-close the modal unless their handler returns a truthy value.

### Methods

| Method | Description |
|--------|-------------|
| `addButton(cb)` | Add an action button (`ConfirmationButton`) |
| `addCancelButton(text?)` | Add a dismissal button |
| `addCheckbox(label, cb)` | Add a checkbox |
| `addClass(cls)` | Add a CSS class to the modal |

### Example

```typescript
import { App, ConfirmationModal, Notice } from 'obsidian';

export function confirmDeletion(app: App, fileName: string, onConfirm: () => void) {
  const modal = new ConfirmationModal(app);
  modal.addClass('my-confirm-modal');

  modal.addButton((btn) =>
    btn
      .setButtonText('Delete')
      .setWarning()
      .onClick(() => {
        onConfirm();
        return false; // close modal
      })
  );

  modal.addCancelButton('Keep file');

  modal.open();
}
```

> [!important]
> Return `false` (or any falsy value) from a button `onClick` handler to let the modal close. Return a truthy value to keep it open — useful for surfacing validation errors inline.

---

## Menu (Context Menus)

`Menu` builds right-click context menus or triggered dropdowns. It extends `Component`, so it can register child components that clean up automatically.

### Methods

| Method | Description |
|--------|-------------|
| `addItem(cb)` | Add a menu item (`MenuItem`) |
| `addSeparator()` | Add a visual separator |
| `showAtMouseEvent(evt)` | Open at the location of a `MouseEvent` |
| `showAtPosition(position)` | Open at an `{x, y}` coordinate |
| `hide()` | Hide the menu |
| `onHide(callback)` | Register a callback invoked when hidden |
| `setNoIcon()` | Hide icons for all items |
| `setUseNativeMenu(useNativeMenu)` | Force native or DOM menu (desktop only) |

### Basic Context Menu

```typescript
import { Menu, Notice, Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    this.addRibbonIcon('dice', 'Open menu', (event: MouseEvent) => {
      const menu = new Menu();

      menu.addItem((item) =>
        item
          .setTitle('Copy')
          .setIcon('documents')
          .onClick(() => {
            new Notice('Copied');
          })
      );

      menu.addItem((item) =>
        item
          .setTitle('Paste')
          .setIcon('paste')
          .onClick(() => {
            new Notice('Pasted');
          })
      );

      menu.addSeparator();

      menu.addItem((item) =>
        item
          .setTitle('Settings')
          .setIcon('gear')
          .onClick(() => {
            // open settings
          })
      );

      menu.showAtMouseEvent(event);
    });
  }
}
```

### Attaching to Built-in Menus

Subscribe to `file-menu` and `editor-menu` workspace events to append items to Obsidian's native menus:

```typescript
this.registerEvent(
  this.app.workspace.on('file-menu', (menu, file) => {
    menu.addItem((item) => {
      item
        .setTitle('Print file path')
        .setIcon('document')
        .onClick(async () => {
          new Notice(file.path);
        });
    });
  })
);

this.registerEvent(
  this.app.workspace.on('editor-menu', (menu, editor, view) => {
    menu.addItem((item) => {
      item
        .setTitle('Print file path')
        .setIcon('document')
        .onClick(async () => {
          new Notice(view.file?.path ?? 'No file');
        });
    });
  })
);
```

> [!tip]
> `showAtPosition({ x: 20, y: 20 })` opens the menu at coordinates relative to the top-left corner of the Obsidian window. Use this when you need pixel-perfect placement.

---

## Modal Lifecycle and Cleanup

### Lifecycle Order

```
new MyModal(app) → constructor
        ↓
    .open() → onOpen() → modal visible
        ↓
    .close() → onClose() → modal hidden
```

### Cleanup Rules

| Resource | Cleanup Required |
|----------|------------------|
| DOM nodes in `contentEl` | Yes — call `contentEl.empty()` in `onClose()` |
| Event listeners on `window` / `document` | Yes — remove manually or register via `this.scope` |
| Timers / intervals | Yes — clear in `onClose()` |
| Registered resources (`registerEvent`, etc.) | No — automatic if attached to the plugin instance |

### Using `setCloseCallback`

For one-off modals, `setCloseCallback` lets you handle teardown without subclassing:

```typescript
const modal = new Modal(app);
modal.setTitle('Notice');
modal.setContent('Operation completed.');
modal.setCloseCallback(() => {
  console.log('Modal closed');
});
modal.open();
```

### Keyboard Shortcuts in Modals

Register shortcuts on `this.scope` inside `onOpen()`. They are automatically scoped to the modal and cleaned up when it closes.

```typescript
onOpen() {
  const { contentEl } = this;
  // ... build UI ...

  this.scope.register(['Ctrl'], 'Enter', () => {
    this.submit();
    return false;
  });

  this.scope.register([], 'Escape', () => {
    this.close();
    return false;
  });
}
```

> [!caution]
> Do not replace the modal's built-in `scope` with a new `Scope` instance. Add custom keymaps to `this.scope` directly so that default modal behaviors (Escape, arrow keys, Enter) continue to work.

---

## Patterns

### Returning Data from Modals

The canonical pattern is a constructor callback:

```typescript
export class InputModal extends Modal {
  constructor(
    app: App,
    private onSubmit: (value: string) => void
  ) {
    super(app);
  }

  onOpen() {
    // ... build form ...
    new Setting(this.contentEl)
      .addButton((btn) =>
        btn.setButtonText('OK').onClick(() => {
          this.close();
          this.onSubmit(this.value);
        })
      );
  }
}
```

An alternative is a Promise wrapper:

```typescript
export function openPrompt(app: App, title: string): Promise<string> {
  return new Promise((resolve) => {
    const modal = new PromptModal(app, (result) => {
      resolve(result);
    });
    modal.onOpen = () => {
      modal.setTitle(title);
      // ... build rest of UI ...
    };
    modal.open();
  });
}
```

### Chaining Modals

Chain modals by opening the next one in the callback of the previous:

```typescript
new FileSuggestModal(this.app, (file) => {
  new TagSuggestModal(this.app, (tag) => {
    new Notice(`Linked ${file.basename} to #${tag}`);
  }).open();
}).open();
```

For complex wizards, consider storing intermediate state in the plugin and using a single modal that advances through steps.

### Mobile Considerations

- Modals animate onto the screen on mobile; keep content concise to avoid overflow.
- Touch targets should be at least 44x44px. Use `Setting` rows with `.addButton()` rather than tiny inline links.
- `Menu` respects `setUseNativeMenu()` on desktop but falls back to DOM menus on mobile automatically.
- Avoid modals that depend on hover states or right-click (use long-press alternatives).

---

## Quick Reference Checklist

- [ ] Extend `Modal` and implement `onOpen()` + `onClose()`
- [ ] Call `contentEl.empty()` in `onClose()`
- [ ] For suggestions, extend `SuggestModal<T>` or `FuzzySuggestModal<T>`
- [ ] Return data via constructor callback or Promise wrapper
- [ ] Use `Menu` for context menus; attach to `file-menu` / `editor-menu` events for native integration
- [ ] Register modal shortcuts on `this.scope`, never replace it
- [ ] Test on mobile: large touch targets, no hover dependencies

---

## References

- [Modals guide](https://docs.obsidian.md/Plugins/User+interface/Modals) — Official UI overview
- [Context menus guide](https://docs.obsidian.md/Plugins/User+interface/Context+menus) — Menu and event integration
- [Modal API](https://docs.obsidian.md/Reference/TypeScript+API/Modal) — Full class reference
- [SuggestModal API](https://docs.obsidian.md/Reference/TypeScript+API/SuggestModal) — SuggestModal class reference
- [FuzzySuggestModal API](https://docs.obsidian.md/Reference/TypeScript+API/FuzzySuggestModal) — FuzzySuggestModal class reference
- [Menu API](https://docs.obsidian.md/Reference/TypeScript+API/Menu) — Menu class reference
- [Scope API](https://docs.obsidian.md/Reference/TypeScript+API/Scope) — Keyboard scope reference
- [Obsidian API Type Definitions](https://github.com/obsidianmd/obsidian-api/blob/master/obsidian.d.ts) — Source of truth for signatures
