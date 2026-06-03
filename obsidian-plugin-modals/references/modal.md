# Modal Reference

Base class for all Obsidian modals.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `app` | `App` | Obsidian app instance |
| `containerEl` | `HTMLElement` | Outer modal container |
| `modalEl` | `HTMLElement` | Modal content area |
| `contentEl` | `HTMLElement` | Main content element |
| `titleEl` | `HTMLElement` | Title element |
| `scope` | `Scope` | Keyboard scope for shortcuts |
| `shouldRestoreSelection` | `boolean` | Restore editor selection on close |

## Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `open` | `open(): void` | Show the modal |
| `close` | `close(): void` | Hide the modal |
| `onOpen` | `onOpen(): void` | Build UI here |
| `onClose` | `onClose(): void` | Clean up here |
| `setTitle` | `setTitle(title: string): this` | Set modal title |
| `setContent` | `setContent(content: string \| DocumentFragment): this` | Set content |
| `setCloseCallback` | `setCloseCallback(callback: () => void): this` | Close callback (1.10.0+) |

## Example

```typescript
class MyModal extends Modal {
  onOpen() {
    this.contentEl.setText('Hello');
  }
  onClose() {
    this.contentEl.empty();
  }
}
```
