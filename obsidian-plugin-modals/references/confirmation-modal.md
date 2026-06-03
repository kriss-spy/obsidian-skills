# ConfirmationModal Reference

Pre-built confirm/cancel dialog available since Obsidian 1.13.0.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `buttonContainerEl` | `HTMLElement` | Button row container |

## Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `addButton` | `addButton(cb: (btn: ConfirmationButton) => any): this` | Add action button |
| `addCancelButton` | `addCancelButton(text?: string): this` | Add cancel button |
| `addCheckbox` | `addCheckbox(label: string, cb: (value: boolean) => any \| Promise<any>): this` | Add checkbox |
| `addClass` | `addClass(cls: string): this` | Add CSS class |

## ConfirmationButton

Extends `ButtonComponent` with:

| Method | Description |
|--------|-------------|
| `onClick(handler)` | Click handler; return truthy to keep modal open |
| `setInitialFocus()` | Focus this button on open |
| `setSecondary()` | Place button outside main group |
| `setCancel()` | Style as dismissal action |

## Example

```typescript
const modal = new ConfirmationModal(app);
modal.addButton((btn) =>
  btn
    .setButtonText('Delete')
    .setWarning()
    .onClick(() => {
      doDelete();
      return false; // close modal
    })
);
modal.addCancelButton('Keep');
modal.open();
```
