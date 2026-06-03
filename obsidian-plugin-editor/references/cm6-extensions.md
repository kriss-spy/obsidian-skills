# CodeMirror 6 Reference

Extracted from https://codemirror.net/docs/ for reference. These are thin summaries; see the live docs for the latest details.

## Core Packages

- `@codemirror/state` — `EditorState`, `StateField`, `StateEffect`, `Transaction`, `RangeSetBuilder`
- `@codemirror/view` — `EditorView`, `ViewPlugin`, `ViewUpdate`, `Decoration`, `DecorationSet`, `WidgetType`
- `@codemirror/language` — `syntaxTree`, `LanguageSupport`

## ViewPlugin

```ts
class MyPlugin implements PluginValue {
  constructor(view: EditorView) { }
  update(update: ViewUpdate) { }
  destroy() { }
}
const myPlugin = ViewPlugin.fromClass(MyPlugin, spec?);
```

`ViewUpdate` flags: `docChanged`, `viewportChanged`, `selectionSet`, `focusChanged`

## StateField

```ts
const myField = StateField.define<T>({
  create(state): T { ... },
  update(value, transaction): T { ... },
  provide?: (field) => Extension,
});
```

## Decorations

Types:
- `Decoration.mark({ class: 'my-class' })` — Style existing text
- `Decoration.widget({ widget: new MyWidget() })` — Insert element at position
- `Decoration.replace({ widget: new MyWidget() })` — Hide/replace range with widget
- `Decoration.line({ class: 'my-line' })` — Style entire line

Providing decorations:
- From state field: `provide: (f) => EditorView.decorations.from(f)`
- From view plugin: `PluginSpec = { decorations: (v) => v.decorations }`

## WidgetType

```ts
class MyWidget extends WidgetType {
  toDOM(view: EditorView): HTMLElement { ... }
  eq(other: MyWidget): boolean { ... }
  ignoreEvent(event: Event): boolean { return false; }
}
```

## Transactions

```ts
view.dispatch({
  changes: { from, to?, insert },
  selection: { anchor, head? },
  effects: [myEffect.of(value)],
  annotations: [myAnnotation.of(value)],
});
```

## Communication Patterns

- Define a `StateEffect` in the CM6 extension file
- Dispatch it from the plugin via `(editor as any).cm.dispatch({ effects: [...] })`
- Or reconfigure the extension array passed to `registerEditorExtension()` and call `app.workspace.updateOptions()`
