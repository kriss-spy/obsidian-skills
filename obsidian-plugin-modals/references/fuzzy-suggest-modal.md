# FuzzySuggestModal Reference

Fuzzy-matched suggestion modal with automatic highlighting.

## Abstract Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `getItems` | `getItems(): T[]` | Return all items |
| `getItemText` | `getItemText(item: T): string` | Return searchable text |
| `onChooseItem` | `onChooseItem(item: T, evt: MouseEvent \| KeyboardEvent): void` | Handle selection |

## Overridable Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `renderSuggestion` | `renderSuggestion(match: FuzzyMatch<T>, el: HTMLElement): void` | Custom row rendering |
| `onChooseSuggestion` | `onChooseSuggestion(match: FuzzyMatch<T>, evt: MouseEvent \| KeyboardEvent): void` | Selection hook |

## Utility

`renderResults(container, text, match, offset?)` — highlight matched ranges.

## Example

```typescript
class TagFuzzyModal extends FuzzySuggestModal<string> {
  getItems(): string[] {
    return ['idea', 'todo', 'bug', 'feature'];
  }

  getItemText(tag: string): string {
    return tag;
  }

  onChooseItem(tag: string, evt: MouseEvent | KeyboardEvent) {
    new Notice(`#${tag}`);
  }
}
```
