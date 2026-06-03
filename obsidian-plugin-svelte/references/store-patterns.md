# Svelte Store Patterns for Obsidian Plugins

## Writable store holding plugin reference

```typescript
import { writable } from 'svelte/store';
import type MyPlugin from './main';
export const pluginStore = writable<MyPlugin | undefined>(undefined);
```

## Set store in view

```typescript
async onOpen() {
  pluginStore.set(this.plugin);
  this.component = mount(MyComponent, { target: this.contentEl });
}
```

## Subscribe in component

```svelte
<script lang="ts">
  import { pluginStore } from './store';
  let plugin;
  pluginStore.subscribe(p => plugin = p);
</script>
```

## Bridging Obsidian events

```typescript
const files = writable<TFile[]>([]);
this.registerEvent(
  this.app.vault.on('create', () => { /* update store */ })
);
```

> Subscriptions are auto-cleaned when the component is destroyed.
