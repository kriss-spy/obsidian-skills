# Menu Reference

Context menu class for building right-click and triggered dropdown menus.

## Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `addItem` | `addItem(cb: (item: MenuItem) => any): this` | Add a menu item |
| `addSeparator` | `addSeparator(): this` | Add a separator |
| `showAtMouseEvent` | `showAtMouseEvent(evt: MouseEvent): this` | Open at mouse event position |
| `showAtPosition` | `showAtPosition(position: Point): this` | Open at `{x, y}` |
| `hide` | `hide(): this` | Hide the menu |
| `onHide` | `onHide(callback: () => any): void` | Register hide callback |
| `setNoIcon` | `setNoIcon(): this` | Hide icons for all items |
| `setUseNativeMenu` | `setUseNativeMenu(useNativeMenu: boolean): this` | Force native or DOM (desktop only) |

## Example

```typescript
const menu = new Menu();
menu.addItem((item) =>
  item.setTitle('Copy').setIcon('documents').onClick(() => {
    new Notice('Copied');
  })
);
menu.addSeparator();
menu.addItem((item) =>
  item.setTitle('Delete').setIcon('trash').onClick(() => {
    // delete
  })
);
menu.showAtMouseEvent(event);
```

## Native Integration

Attach to Obsidian's built-in menus via workspace events:

```typescript
this.registerEvent(
  this.app.workspace.on('file-menu', (menu, file) => {
    menu.addItem((item) =>
      item.setTitle('My action').onClick(() => { /* ... */ })
    );
  })
);
```
