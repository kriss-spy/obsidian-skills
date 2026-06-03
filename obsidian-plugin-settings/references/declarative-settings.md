# Declarative Settings Reference

## Definition Shapes

Each entry in `getSettingDefinitions()` is one of:

- A setting with `control` — declarative binding to one settings key
- A setting with `render` callback — full control over the `Setting` row
- A setting with `action` callback — clickable row that runs your function
- A name/desc-only row — useful for headings or informational text
- `SettingDefinitionGroup` (`type: 'group'`) — heading + nested items
- `SettingDefinitionList` (`type: 'list'`) — add, delete, reorder
- `SettingDefinitionPage` (`type: 'page'`) — navigable sub-page

## Control Types

| Type | Stored value | Params |
|------|-------------|--------|
| `toggle` | `boolean` | — |
| `text` | `string` | `placeholder?` |
| `textarea` | `string` | `placeholder?`, `rows?` |
| `number` | `number` | `min?`, `max?`, `step?`, `placeholder?` |
| `slider` | `number` | `min`, `max`, `step` |
| `dropdown` | `string` | `options: Record<string, string>` |
| `file` | `string` (path) | `filter?`, `placeholder?` |
| `folder` | `string` (path) | `filter?`, `includeRoot?`, `placeholder?` |
| `color` | `string` (hex) | — |

## Shared Control Options

- `defaultValue?` — fallback when stored value is `undefined` or `null`
- `validate?` — `(value: any) => string \| undefined` or async variant

## Conditional Predicates

- `visible?: boolean \| () => boolean` — hides row when false
- `disabled?: boolean \| () => boolean` — disables control when false

## Tab Methods

- `this.refreshDomState()` — re-evaluate predicates without full re-render
- `this.update()` — rebuild definitions and re-render
