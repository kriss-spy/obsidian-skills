# obsidian-plugin-editor

Integrate with the Obsidian editor through CodeMirror 6 extensions, the Editor API, and markdown post-processing.

## What This Skill Covers

- Reading and writing editor content via the `Editor` API (`getCursor`, `replaceSelection`, `replaceRange`, etc.)
- Registering CodeMirror 6 extensions with `registerEditorExtension()`
- Building `ViewPlugin`s for real-time editor behavior
- Managing custom state with `StateField` and `StateEffect`
- Rendering decorations (widgets, marks, replacements) in Live Preview
- Working with the viewport for performant large-document handling
- Markdown post-processing for Reading view (`registerMarkdownPostProcessor`, `registerMarkdownCodeBlockProcessor`)
- Autocomplete popups with `EditorSuggest`
- Communicating between CM6 extensions and the Obsidian plugin

## When to Use

Use this skill when implementing any feature that touches the editing surface, renders custom DOM in preview mode, or provides inline autocomplete.
