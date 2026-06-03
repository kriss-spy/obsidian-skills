# React Integration Reference

Thin summary of official docs and verified patterns for React in Obsidian plugins.

## Official Guide Summary

From [Use React in your plugin](https://docs.obsidian.md/Plugins/Getting+started/Use+React+in+your+plugin):

1. `npm install react react-dom`
2. `npm install --save-dev @types/react @types/react-dom`
3. Set `"jsx": "react-jsx"` in `tsconfig.json` compiler options
4. Write components in `.tsx` files
5. Mount with `createRoot(element).render(<Component />)`
6. Unmount with `root.unmount()` in the corresponding cleanup method

## Mount Locations

| Surface | Mount Element | Mount Method | Cleanup Method |
|---------|--------------|--------------|----------------|
| `ItemView` | `this.contentEl` | `onOpen()` | `onClose()` |
| `Modal` | `this.contentEl` | `onOpen()` | `onClose()` |
| `PluginSettingTab` | `this.containerEl` | `display()` | `hide()` |
| Status bar | `addStatusBarItem()` result | plugin init | `onunload()` |

## Memory Leak Prevention

- Store `Root` as a class property
- Call `root.unmount()` before the host element is removed from DOM
- After unmount, discard the `Root` instance; create a new one on next mount
- Do not update React state after unmount

## App Context Pattern

Use React Context to avoid prop-drilling `App` through many layers:

```tsx
export const AppContext = createContext<App | undefined>(undefined);
```

Provide it at the mount point; consume it with a custom `useApp()` hook.
