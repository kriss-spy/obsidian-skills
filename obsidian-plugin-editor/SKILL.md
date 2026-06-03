---
name: obsidian-plugin-editor
description: Guide for integrating with the Obsidian editor through CodeMirror 6 extensions, the Editor API, and markdown post-processing. Use when building editor extensions, custom decorations, autocomplete, reading-view processors, or any feature that touches the editing surface or markdown rendering.
triggers:
  - obsidian editor extension
  - obsidian codemirror 6
  - obsidian editor api
  - obsidian editor suggest
  - obsidian markdown post processor
  - obsidian live preview
  - obsidian view plugin
  - obsidian state field
  - obsidian decoration
  - obsidian register editor extension
  - obsidian editor autocomplete
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Editor

This skill guides you through integrating with the Obsidian editor: CodeMirror 6 extensions, the `Editor` API, and markdown post-processing. It focuses on the editing surface — how to read and write text, extend the editor with CM6 primitives, render custom DOM in Reading view, and provide autocomplete popups.

## When to Use This Skill

- Building a CodeMirror 6 extension for Live Preview (decorations, widgets, custom behavior)
- Reading or programmatically modifying editor content via the `Editor` API
- Adding autocomplete / suggestion popups with `EditorSuggest`
- Customizing how Markdown renders in Reading view with post processors
- Implementing custom fenced code block renderers
- Deciding whether a feature belongs in an editor extension or a post processor

## Overview

Obsidian's editor is powered by **CodeMirror 6 (CM6)**. There are three main integration surfaces:

1. **`Editor` API** — Obsidian's abstraction over CM6 for common read/write operations
2. **Editor extensions** — Raw CM6 extensions (`ViewPlugin`, `StateField`, `Decoration`) registered via `registerEditorExtension()`
3. **Markdown post processors** — DOM manipulators for Reading view, registered via `registerMarkdownPostProcessor()` and `registerMarkdownCodeBlockProcessor()`

> [!tip]
> If you want to change how the document looks in **Live Preview**, build an editor extension. If you want to change how Markdown renders in **Reading view**, use a post processor.

---

## Editor API Basics

The `Editor` interface is Obsidian's abstraction over the underlying CM6 instance. It is available from `MarkdownView.editor`, `editorCallback` in commands, and `EditorSuggestContext.editor`.

### Reading Content

```typescript
const editor = view.editor;

// Get the entire document value
const fullText = editor.getValue();

// Get text at a specific range
const rangeText = editor.getRange({ line: 5, ch: 0 }, { line: 5, ch: 10 });

// Get the current selection(s)
const selection = editor.getSelection();
```

### Modifying Content

```typescript
// Replace the current selection
editor.replaceSelection('replacement text');

// Replace text in a specific range
editor.replaceRange('inserted text', { line: 5, ch: 0 }, { line: 5, ch: 10 });

// Set the entire document value
editor.setValue('# New content');
```

### Cursor and Selection

```typescript
// Get the current cursor position
const cursor = editor.getCursor(); // { line: number, ch: number }

// Set cursor position
editor.setCursor({ line: 10, ch: 5 });

// Get all selections (multi-cursor)
const selections = editor.listSelections();
```

**Key `Editor` methods:**
- `getValue()` / `setValue(value)` — Whole document
- `getSelection()` / `replaceSelection(value)` — Selected text
- `getRange(from, to)` / `replaceRange(text, from, to?)` — Specific range
- `getCursor()` / `setCursor(pos)` — Primary cursor
- `listSelections()` / `setSelections(ranges)` — Multi-cursor support
- `offsetToPos(offset)` / `posToOffset(pos)` — Convert between line/ch and absolute offset

---

## Registering Editor Extensions

To add a CM6 extension to Obsidian, call `registerEditorExtension()` in your plugin's `onload()`:

```typescript
import { Plugin } from 'obsidian';
import { myViewPlugin, myStateField } from './editorExtensions';

export default class MyPlugin extends Plugin {
  async onload() {
    this.registerEditorExtension([myViewPlugin, myStateField]);
  }
}
```

> [!note]
> `registerEditorExtension()` accepts a single `Extension` or an array. Pass an array if you need to reconfigure extensions dynamically — modify the array, then call `this.app.workspace.updateOptions()` to apply changes.

CM6 extensions are **not** bundled by esbuild. They must be listed in `external` in `esbuild.config.mjs`:

```js
external: [
  "obsidian",
  "@codemirror/state",
  "@codemirror/view",
  "@codemirror/language",
  "@lezer/common",
  // ... other cm6 deps
]
```

---

## View Plugins

A `ViewPlugin` is an editor extension that runs after the viewport has been recomputed. It gives you access to the `EditorView` but cannot make changes that impact the viewport (e.g., inserting blocks or line breaks).

> [!tip]
> If you need to change vertical layout (add line breaks, blocks), use a **State field** instead.

### Creating a View Plugin

```typescript
import { ViewUpdate, PluginValue, EditorView, ViewPlugin } from '@codemirror/view';

class ExamplePlugin implements PluginValue {
  constructor(view: EditorView) {
    // Initialize
  }

  update(update: ViewUpdate) {
    // React to document changes, viewport changes, selection changes, etc.
    if (update.docChanged) {
      console.log('Document changed');
    }
  }

  destroy() {
    // Cleanup
  }
}

export const examplePlugin = ViewPlugin.fromClass(ExamplePlugin);
```

**Key `ViewUpdate` properties:**
- `update.docChanged` — The document content changed
- `update.viewportChanged` — The visible viewport changed (scrolling)
- `update.selectionSet` — The selection changed
- `update.focusChanged` — Focus state changed
- `update.transactions` — List of transactions that caused this update

---

## State Fields

A `StateField` manages custom editor state. Unlike view plugins, state fields can affect document layout and are not tied to the viewport.

### Defining a State Field

```typescript
import { StateField, StateEffect, EditorState } from '@codemirror/state';

const addEffect = StateEffect.define<number>();
const resetEffect = StateEffect.define<void>();

export const counterField = StateField.define<number>({
  create(state: EditorState): number {
    return 0;
  },
  update(value: number, transaction) {
    let newValue = value;
    for (const effect of transaction.effects) {
      if (effect.is(addEffect)) {
        newValue += effect.value;
      } else if (effect.is(resetEffect)) {
        newValue = 0;
      }
    }
    return newValue;
  },
});
```

### Dispatching State Effects

```typescript
import { EditorView } from '@codemirror/view';

function incrementCounter(view: EditorView) {
  view.dispatch({ effects: [addEffect.of(1)] });
}
```

**State field lifecycle:**
- `create(state)` — Returns the initial value when the editor is constructed
- `update(value, transaction)` — Returns a new value after each transaction
- Effects are dispatched via `view.dispatch({ effects: [...] })`

---

## Decorations

Decorations change how content is drawn without modifying the document itself. There are four types:

1. **Mark decorations** — Style existing text (e.g., highlight, underline)
2. **Widget decorations** — Insert a custom HTML element at a position
3. **Replace decorations** — Hide or replace a range with a widget
4. **Line decorations** — Add CSS classes to entire lines

### Widgets

```typescript
import { WidgetType } from '@codemirror/view';

class MyWidget extends WidgetType {
  toDOM(view: EditorView): HTMLElement {
    const span = document.createElement('span');
    span.textContent = '👉';
    return span;
  }
}
```

### Providing Decorations from a State Field

```typescript
import { syntaxTree } from '@codemirror/language';
import { Extension, RangeSetBuilder, StateField, Transaction } from '@codemirror/state';
import { Decoration, DecorationSet, EditorView, WidgetType } from '@codemirror/view';

class EmojiWidget extends WidgetType {
  toDOM(): HTMLElement {
    const el = document.createElement('span');
    el.textContent = '👉';
    return el;
  }
}

export const emojiField = StateField.define<DecorationSet>({
  create(): DecorationSet {
    return Decoration.none;
  },
  update(oldState: DecorationSet, transaction: Transaction): DecorationSet {
    const builder = new RangeSetBuilder<Decoration>();
    syntaxTree(transaction.state).iterate({
      enter(node) {
        if (node.type.name.startsWith('list')) {
          const pos = node.from - 2;
          builder.add(pos, pos + 1, Decoration.replace({
            widget: new EmojiWidget(),
          }));
        }
      },
    });
    return builder.finish();
  },
  provide(field: StateField): Extension {
    return EditorView.decorations.from(field);
  },
});
```

### Providing Decorations from a View Plugin

```typescript
import { syntaxTree } from '@codemirror/language';
import { RangeSetBuilder } from '@codemirror/state';
import { Decoration, DecorationSet, EditorView, PluginSpec, PluginValue, ViewPlugin, ViewUpdate, WidgetType } from '@codemirror/view';

class EmojiWidget extends WidgetType {
  toDOM(): HTMLElement {
    const el = document.createElement('span');
    el.textContent = '👉';
    return el;
  }
}

class EmojiListPlugin implements PluginValue {
  decorations: DecorationSet;

  constructor(view: EditorView) {
    this.decorations = this.buildDecorations(view);
  }

  update(update: ViewUpdate) {
    if (update.docChanged || update.viewportChanged) {
      this.decorations = this.buildDecorations(update.view);
    }
  }

  destroy() {}

  buildDecorations(view: EditorView): DecorationSet {
    const builder = new RangeSetBuilder<Decoration>();
    for (const { from, to } of view.visibleRanges) {
      syntaxTree(view.state).iterate({
        from,
        to,
        enter(node) {
          if (node.type.name.startsWith('list')) {
            const pos = node.from - 2;
            builder.add(pos, pos + 1, Decoration.replace({
              widget: new EmojiWidget(),
            }));
          }
        },
      });
    }
    return builder.finish();
  }
}

const pluginSpec: PluginSpec<EmojiListPlugin> = {
  decorations: (value: EmojiListPlugin) => value.decorations,
};

export const emojiListPlugin = ViewPlugin.fromClass(EmojiListPlugin, pluginSpec);
```

> [!note]
> **State field vs view plugin for decorations:**
> - Use a **view plugin** if decorations depend on the viewport (better performance for large docs).
> - Use a **state field** if decorations must be computed for the entire document or affect layout.

---

## Viewport Plugins

Viewport plugins are a specialized view plugin that only operates on the visible portion of the document. Since the view plugin already has access to `view.visibleRanges`, most viewport-aware logic is implemented as a regular view plugin that limits its work to those ranges.

```typescript
update(update: ViewUpdate) {
  if (update.viewportChanged) {
    for (const { from, to } of update.view.visibleRanges) {
      // Only process visible content
    }
  }
}
```

This is the recommended pattern for expensive operations (syntax highlighting, spell checking) on large documents.

---

## Markdown Post Processing

Post processors run **after** Markdown has been converted to HTML in Reading view. They mutate the DOM.

### `registerMarkdownPostProcessor`

```typescript
import { Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    this.registerMarkdownPostProcessor((element, context) => {
      const codeblocks = element.findAll('code');
      for (const codeblock of codeblocks) {
        const text = codeblock.innerText.trim();
        if (text.startsWith(':') && text.endsWith(':')) {
          const emojiEl = codeblock.createSpan({ text: text });
          codeblock.replaceWith(emojiEl);
        }
      }
    });
  }
}
```

**Parameters:**
- `element` — The root `HTMLElement` of the rendered section
- `context` — `MarkdownPostProcessorContext` with metadata about the section

> [!tip]
> If your post processor needs lifecycle management (e.g., clearing intervals when the element is removed), use `context.addChild(component)` to register a `Component` that will be unloaded automatically.

### `registerMarkdownCodeBlockProcessor`

Use this for custom fenced code blocks (like Mermaid):

```typescript
import { Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    this.registerMarkdownCodeBlockProcessor('csv', (source, el, ctx) => {
      const rows = source.split('\n').filter((row) => row.length > 0);
      const table = el.createEl('table');
      const body = table.createEl('tbody');
      for (const rowText of rows) {
        const cols = rowText.split(',');
        const row = body.createEl('tr');
        for (const col of cols) {
          row.createEl('td', { text: col });
        }
      }
    });
  }
}
```

**Parameters:**
- `source` — The raw text inside the code block
- `el` — An empty `HTMLDivElement` for you to populate
- `ctx` — `MarkdownPostProcessorContext`

---

## EditorSuggest (Autocomplete)

`EditorSuggest` provides live autocomplete popups while the user types. It extends `PopoverSuggest`.

### Implementing EditorSuggest

```typescript
import { EditorSuggest, EditorSuggestContext, EditorSuggestTriggerInfo, TFile } from 'obsidian';

interface MySuggestion {
  label: string;
  value: string;
}

export class MySuggest extends EditorSuggest<MySuggestion> {
  onTrigger(cursor: EditorPosition, editor: Editor, file: TFile): EditorSuggestTriggerInfo | null {
    const line = editor.getLine(cursor.line);
    const sub = line.substring(0, cursor.ch);
    const match = sub.match(/\[\[([^\]]*)$/);
    if (!match) return null;

    return {
      start: { line: cursor.line, ch: match.index! },
      end: cursor,
      query: match[1],
    };
  }

  getSuggestions(context: EditorSuggestContext): MySuggestion[] {
    const files = this.app.vault.getMarkdownFiles();
    return files
      .filter((f) => f.basename.toLowerCase().contains(context.query.toLowerCase()))
      .map((f) => ({ label: f.basename, value: f.path }));
  }

  renderSuggestion(suggestion: MySuggestion, el: HTMLElement): void {
    el.createEl('div', { text: suggestion.label });
  }

  selectSuggestion(suggestion: MySuggestion, evt: MouseEvent | KeyboardEvent): void {
    const { editor, start, end } = this.context;
    editor.replaceRange(`[[${suggestion.value}]]`, start, end);
  }
}
```

### Registering EditorSuggest

```typescript
import { Plugin } from 'obsidian';
import { MySuggest } from './suggest';

export default class MyPlugin extends Plugin {
  async onload() {
    this.registerEditorSuggest(new MySuggest(this.app));
  }
}
```

**Key methods:**
- `onTrigger(cursor, editor, file)` — Returns `EditorSuggestTriggerInfo` if typing should trigger suggestions, or `null`
- `getSuggestions(context)` — Returns an array of suggestion objects
- `renderSuggestion(value, el)` — Renders each suggestion in the popup
- `selectSuggestion(value, evt)` — Called when the user selects a suggestion

**`EditorSuggestTriggerInfo` properties:**
- `start` — `EditorPosition` where the trigger text begins
- `end` — `EditorPosition` where the trigger text ends
- `query` — The string used to filter suggestions

---

## Communicating with Editor Extensions

CM6 extensions live inside the editor. Your plugin lives outside. To communicate across this boundary, use `editorViewField` and `editorEditorField` from Obsidian, or dispatch transactions directly.

### Accessing the CM6 EditorView from Obsidian

```typescript
import { editorViewField } from 'obsidian';
import { EditorView } from '@codemirror/view';

const view = this.app.workspace.getActiveViewOfType(MarkdownView);
if (view) {
  const cmView: EditorView = (view.editor as any).cm;
  // Or via the private API:
  // const cmView = view.editor.cm;
}
```

> [!caution]
> `editor.cm` is technically private. It is widely used but may break in future Obsidian versions. Prefer `registerEditorExtension()` and state effects for clean communication.

### Communicating via State Effects

The cleanest pattern is to define a custom `StateEffect` in your CM6 extension, then dispatch it from your plugin:

```typescript
// In your CM6 extension file
import { StateEffect } from '@codemirror/state';

export const highlightLineEffect = StateEffect.define<number>();

// In your plugin
const view = this.app.workspace.getActiveViewOfType(MarkdownView);
if (view) {
  const cmView: EditorView = (view.editor as any).cm;
  cmView.dispatch({ effects: [highlightLineEffect.of(10)] });
}
```

### Reconfiguring Extensions on the Fly

Pass an array to `registerEditorExtension()`, then modify it and call `updateOptions()`:

```typescript
export default class MyPlugin extends Plugin {
  private cmExtensions: Extension[] = [];

  async onload() {
    this.cmExtensions = [myPlugin];
    this.registerEditorExtension(this.cmExtensions);
  }

  enableFeature() {
    this.cmExtensions.push(myFeatureExtension);
    this.app.workspace.updateOptions();
  }
}
```

---

## Editor Extension vs Post Processor: Decision Guide

| Goal | Use |
|------|-----|
| Change appearance in **Live Preview** | Editor extension (`ViewPlugin`, `StateField`, `Decoration`) |
| Change appearance in **Reading view** | `registerMarkdownPostProcessor()` |
| Custom fenced code block renderer | `registerMarkdownCodeBlockProcessor()` |
| Add autocomplete while typing | `EditorSuggest` |
| Read/modify editor text programmatically | `Editor` API (`getValue`, `replaceSelection`, etc.) |
| React to cursor movement or typing in real time | `ViewPlugin` |
| Persist custom state per editor document | `StateField` |
| Insert widgets, replace text visually | `Decoration` + `ViewPlugin` or `StateField` |

> [!note]
> Editor extensions only affect the editing surface (Live Preview / Source mode). They do **not** run in Reading view. Post processors only affect Reading view. If you need both, implement both.

---

## References

- [Editor extensions](https://docs.obsidian.md/Plugins/Editor/Editor+extensions) — Official overview
- [View plugins](https://docs.obsidian.md/Plugins/Editor/View+plugins) — CM6 view plugin lifecycle
- [State fields](https://docs.obsidian.md/Plugins/Editor/State+fields) — Managing custom editor state
- [Decorations](https://docs.obsidian.md/Plugins/Editor/Decorations) — Changing editor appearance
- [Viewport](https://docs.obsidian.md/Plugins/Editor/Viewport) — Working with visible ranges
- [State management](https://docs.obsidian.md/Plugins/Editor/State+management) — Transactions and effects
- [Communicating with editor extensions](https://docs.obsidian.md/Plugins/Editor/Communicating+with+editor+extensions) — Plugin ↔ CM6 bridge
- [Markdown post processing](https://docs.obsidian.md/Plugins/Editor/Markdown+post+processing) — Reading view DOM manipulation
- [TypeScript API: Editor](https://docs.obsidian.md/Reference/TypeScript+API/Editor) — `Editor` method reference
- [TypeScript API: EditorSuggest](https://docs.obsidian.md/Reference/TypeScript+API/EditorSuggest) — Autocomplete API
- [TypeScript API: Plugin.registerEditorExtension](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/registerEditorExtension) — Registration reference
- [CodeMirror 6 System Guide](https://codemirror.net/docs/guide/) — CM6 architecture
- [CodeMirror 6 Reference](https://codemirror.net/docs/ref/) — CM6 API docs
