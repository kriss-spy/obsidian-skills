# Mount Targets in Obsidian

| Surface | DOM element | Lifecycle hook |
|---------|-------------|----------------|
| `ItemView` | `this.contentEl` | `onOpen()` / `onClose()` |
| `Modal` | `this.contentEl` | `onOpen()` / `onClose()` |
| `PluginSettingTab` | `this.containerEl` | `display()` / `hide()` |
| Status bar item | returned `HTMLElement` | manual in `onunload()` |
| Ribbon icon | returned `HTMLElement` | manual in `onunload()` |

## Svelte 5 mount/unmount

```typescript
import { mount, unmount } from 'svelte';
const instance = mount(Component, { target, props });
unmount(instance);
```

## Svelte 4 mount/$destroy

```typescript
const instance = new Component({ target, props });
instance.$destroy();
```
