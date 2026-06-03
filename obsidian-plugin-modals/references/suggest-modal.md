# SuggestModal Reference

Generic autocomplete-style suggestion modal.

## Abstract Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `getSuggestions` | `getSuggestions(query: string): T[] \| Promise<T[]>` | Return matching items |
| `renderSuggestion` | `renderSuggestion(value: T, el: HTMLElement): any` | Render a row |
| `onChooseSuggestion` | `onChooseSuggestion(item: T, evt: MouseEvent \| KeyboardEvent): any` | Handle selection |

## Inherited from Modal

`open()`, `close()`, `onOpen()`, `onClose()`, `contentEl`, `scope`, etc.

## Example

```typescript
class FileSuggestModal extends SuggestModal<TFile> {
  getSuggestions(query: string): TFile[] {
    return this.app.vault.getMarkdownFiles()
      .filter(f => f.basename.toLowerCase().includes(query.toLowerCase()));
  }

  renderSuggestion(file: TFile, el: HTMLElement) {
    el.createEl('div', { text: file.basename });
  }

  onChooseSuggestion(file: TFile, evt: MouseEvent | KeyboardEvent) {
    new Notice(file.path);
  }
}
```
