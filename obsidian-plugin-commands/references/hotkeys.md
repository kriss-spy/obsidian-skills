# Hotkey Reference

## Modifier Values

| Value | Desktop | macOS |
|-------|---------|-------|
| `Mod` | Ctrl | Cmd |
| `Ctrl` | Ctrl | Ctrl |
| `Meta` | Windows | Cmd |
| `Alt` | Alt | Option |
| `Shift` | Shift | Shift |

## Common Key Values

Letters, digits, and symbols are passed as their string representation (`'a'`, `'1'`, `'/'`).

Special keys:
- `'Enter'`
- `'Escape'`
- `'Tab'`
- `'Backspace'`
- `'Delete'`
- `'ArrowUp'` / `'ArrowDown'` / `'ArrowLeft'` / `'ArrowRight'`

## Example

```typescript
hotkeys: [
  { modifiers: ['Mod', 'Shift'], key: 'd' },
]
```

## Source

- [Hotkey — TypeScript API](https://docs.obsidian.md/Reference/TypeScript+API/Hotkey)
- [Commands — User interface](https://docs.obsidian.md/Plugins/User+interface/Commands)
