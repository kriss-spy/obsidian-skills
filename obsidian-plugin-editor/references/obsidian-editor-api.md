# Official Obsidian Docs — Editor

Extracted from https://docs.obsidian.md/ for reference. These are thin summaries; see the live docs for the latest details.

## Editor API

The `Editor` interface provides read/write access to the document:

- `getValue()` — Returns the entire document text
- `setValue(value)` — Replaces the entire document
- `getSelection()` — Returns the selected text
- `replaceSelection(value)` — Replaces the current selection
- `getRange(from, to)` — Returns text between two `EditorPosition` objects
- `replaceRange(text, from, to?)` — Replaces text in a range
- `getCursor()` — Returns the primary cursor as `EditorPosition`
- `setCursor(pos)` — Moves the primary cursor
- `listSelections()` — Returns all selections (multi-cursor)
- `offsetToPos(offset)` / `posToOffset(pos)` — Coordinate conversion
- `getLine(n)` — Returns the text of line `n`
- `lineCount()` — Total number of lines
- `hasFocus()` — Whether the editor has focus

## EditorSuggest API

- `class EditorSuggest<T> extends PopoverSuggest<T>`
- `onTrigger(cursor, editor, file): EditorSuggestTriggerInfo | null`
- `getSuggestions(context: EditorSuggestContext): T[] | Promise<T[]>`
- `renderSuggestion(value, el): void`
- `selectSuggestion(value, evt): void`
- `EditorSuggestTriggerInfo` — `{ start: EditorPosition, end: EditorPosition, query: string }`
- `EditorSuggestContext` — extends `EditorSuggestTriggerInfo` with `editor` and `file`

## Post Processor API

- `registerMarkdownPostProcessor(postProcessor, sortOrder?)`
  - `postProcessor: (element: HTMLElement, context: MarkdownPostProcessorContext) => void`
- `registerMarkdownCodeBlockProcessor(language, handler, sortOrder?)`
  - `handler: (source: string, el: HTMLElement, context: MarkdownPostProcessorContext) => void`
- `MarkdownPostProcessorContext.addChild(component)` — For lifecycle-managed children

## Plugin Registration Methods

- `registerEditorExtension(extension: Extension | Extension[])` — Registers CM6 extensions
- `registerEditorSuggest(editorSuggest: EditorSuggest<any>)` — Registers autocomplete
- To reconfigure extensions dynamically, pass an array and call `Workspace.updateOptions()`
