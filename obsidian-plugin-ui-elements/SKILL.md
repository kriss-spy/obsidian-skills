---
name: obsidian-plugin-ui-elements
description: Create and manage Obsidian plugin UI elements. Covers ribbon icons, status bar items, HTML element helpers (createEl, createDiv, createSpan, createFragment), built-in Lucide icons, custom SVG icons, RTL support, and accessibility patterns. Use when adding UI components to an Obsidian plugin or styling plugin interfaces.
triggers:
  - obsidian plugin ui
  - obsidian plugin ribbon icon
  - obsidian plugin status bar
  - obsidian plugin createEl
  - obsidian plugin icons
  - obsidian plugin lucide icons
  - obsidian plugin html elements
  - obsidian plugin rtl
  - obsidian plugin right to left
  - obsidian plugin accessibility
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin UI Elements

This skill guides you through building and styling user interface elements in Obsidian plugins. It focuses on the DOM helpers, icon system, and platform considerations that let you create polished, accessible plugin interfaces.

## When to Use This Skill

- Adding a ribbon icon or status bar item to a plugin
- Creating custom HTML structures inside modals, settings tabs, or views
- Choosing and customizing icons for plugin UI
- Supporting right-to-left (RTL) languages in plugin interfaces
- Updating UI elements dynamically based on plugin state

## Overview

Obsidian exposes a rich set of DOM utilities on `HTMLElement` and provides top-level helpers for common UI patterns. At minimum, a plugin UI needs:

1. **An entry point in the chrome** — `addRibbonIcon()` or `addStatusBarItem()`
2. **Structured HTML** — `createEl()`, `createDiv()`, `createSpan()`, `createFragment()`
3. **Icons** — built-in Lucide icons via `setIcon()` or custom SVG via `addIcon()`
4. **Platform awareness** — mobile constraints and RTL language support

---

## Ribbon Icons

The left sidebar in Obsidian is called the _ribbon_. Plugins add actions to it with `addRibbonIcon()`.

### Basic Usage

```typescript
import { Plugin, Notice } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    this.addRibbonIcon('dice', 'Roll the dice', () => {
      new Notice('You rolled a 20!');
    });
  }
}
```

**Signature:**

```typescript
addRibbonIcon(
  icon: IconName,
  title: string,
  callback: (evt: MouseEvent) => any
): HTMLElement;
```

| Parameter | Description |
|-----------|-------------|
| `icon` | A built-in Lucide icon name or a custom icon added with `addIcon()` |
| `title` | Tooltip text shown on hover |
| `callback` | Click handler receiving the `MouseEvent` |

The method returns the `HTMLElement` of the ribbon button, so you can add CSS classes or additional event listeners.

### Adding CSS Classes

```typescript
const ribbonBtn = this.addRibbonIcon('search', 'Quick search', () => {
  // open search modal
});
ribbonBtn.addClass('my-plugin-ribbon-btn');
```

Then in `styles.css`:

```css
.my-plugin-ribbon-btn {
  color: var(--text-accent);
}
```

> [!note]
> Users can remove your plugin's icon from the ribbon, or even hide the ribbon entirely. Always provide an alternate access path (e.g., a command) for ribbon functionality. Do not add your own toggles for ribbon items.

---

## Status Bar Items

The status bar lives at the bottom of the desktop app. Use `addStatusBarItem()` to contribute blocks to it.

### Basic Usage

```typescript
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    const item = this.addStatusBarItem();
    item.createEl('span', { text: 'Ready' });
  }
}
```

> [!caution] Obsidian mobile
> `addStatusBarItem()` is ignored on mobile. Do not rely on it for critical functionality.

### Grouping Multiple Elements

Obsidian adds a gap between each status bar item. If you need tighter control over spacing, group related elements under a single item:

```typescript
const fruits = this.addStatusBarItem();
fruits.createEl('span', { text: '🍎' });
fruits.createEl('span', { text: '🍌' });

const veggies = this.addStatusBarItem();
veggies.createEl('span', { text: '🥦' });
veggies.createEl('span', { text: '🥬' });
```

### Updating Dynamically

Store a reference to the inner element and update it later:

```typescript
export default class MyPlugin extends Plugin {
  statusText: HTMLElement;

  async onload() {
    const item = this.addStatusBarItem();
    this.statusText = item.createEl('span', { text: 'Idle' });

    this.registerEvent(
      this.app.workspace.on('active-leaf-change', () => {
        this.statusText.setText('Changed');
      })
    );
  }
}
```

---

## HTML Element Helpers

Obsidian extends the standard DOM with convenience methods on `Node` and `HTMLElement`. These are available on any container element (settings tabs, modals, views, status bar items, etc.).

### `createEl()`

Creates an arbitrary HTML element and appends it to the parent.

```typescript
const heading = containerEl.createEl('h2', { text: 'Settings' });
const input = containerEl.createEl('input', {
  type: 'text',
  placeholder: 'Enter value',
  cls: 'my-input',
});
```

The second argument is a `DomElementInfo` object:

| Property | Type | Description |
|----------|------|-------------|
| `text` | `string \| DocumentFragment` | Text content |
| `cls` | `string \| string[]` | CSS class or classes |
| `attr` | `Record<string, string \| number \| boolean \| null>` | HTML attributes |
| `title` | `string` | Tooltip text |
| `parent` | `Node` | Override the parent node |
| `prepend` | `boolean` | Insert before existing children |

### `createDiv()`

Shorthand for `createEl('div', ...)`. Returns an `HTMLDivElement`.

```typescript
const card = containerEl.createDiv({ cls: 'card' });
card.createEl('h3', { text: 'Card Title' });
card.createEl('p', { text: 'Card body text.' });
```

### `createSpan()`

Shorthand for `createEl('span', ...)`. Returns an `HTMLSpanElement`.

```typescript
containerEl.createSpan({ text: 'Inline note', cls: 'text-muted' });
```

### `createFragment()`

Creates a `DocumentFragment` for composing multiple elements without attaching them to the DOM immediately.

```typescript
const frag = createFragment((frag) => {
  frag.createEl('strong', { text: 'Important: ' });
  frag.createEl('span', { text: 'Save your work.' });
});

containerEl.appendChild(frag);
```

> [!tip]
> `createFragment` is useful when building complex UI trees in loops or when passing content to APIs that expect a `DocumentFragment`.

---

## Icons

### Built-in Lucide Icons

Obsidian ships with the Lucide icon library (up to v0.446.0). Browse names at [lucide.dev](https://lucide.dev).

Use `setIcon()` to attach an icon to any HTML element:

```typescript
import { Plugin, setIcon } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    const item = this.addStatusBarItem();
    setIcon(item, 'info');
  }
}
```

**Signature:**

```typescript
setIcon(el: HTMLElement, iconId: IconName): void;
```

### Icon Sizes

Control icon size with the `--icon-size` CSS variable:

```css
.my-icon-container {
  --icon-size: var(--icon-size-m);
}
```

| Preset | Default value |
|--------|---------------|
| `--icon-xs` | `14px` |
| `--icon-s` | `16px` |
| `--icon-m` | `18px` |
| `--icon-l` | `18px` |
| `--icon-xl` | `32px` |

### Custom SVG Icons

Register your own icon with `addIcon()`:

```typescript
import { addIcon, Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  async onload() {
    addIcon('circle', '<circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="5" />');
    this.addRibbonIcon('circle', 'Custom icon', () => {
      console.log('Clicked!');
    });
  }
}
```

**Signature:**

```typescript
addIcon(iconId: string, svgContent: string): void;
```

| Parameter | Description |
|-----------|-------------|
| `iconId` | Unique identifier for your icon |
| `svgContent` | Raw SVG markup **without** the surrounding `<svg>` tag |

> [!important]
> Custom icons must fit within a `0 0 100 100` viewBox and follow Lucide guidelines (24x24 canvas, 2px stroke, round joins/caps, 1px padding) for visual consistency.

---

## Right-to-Left (RTL) Support

Obsidian supports RTL languages (Arabic, Hebrew, Farsi, etc.) both in the app interface and in note content.

### Interface Direction

When a user selects an RTL language in Settings → General, Obsidian:

- Adds `.mod-rtl` to the `<body>` element
- Sets `dir="rtl"` on the editor container
- Adds `lang="<code>"` to the `<html>` element (e.g., `lang="ar"`)

### CSS Best Practices

Use logical properties instead of directional ones:

```css
/* Good */
.my-box {
  margin-inline-start: 1rem;
  margin-inline-end: 1rem;
  text-align: start;
}

/* Avoid */
.my-box {
  margin-left: 1rem;
  margin-right: 1rem;
  text-align: left;
}
```

### Targeting RTL Mode

```css
.mod-rtl .my-plugin-panel {
  direction: rtl;
}
```

### Bidirectional Text

For single-line elements that may contain mixed-direction text (file names, status bar items, tooltips), use:

```css
.my-line {
  unicode-bidi: plaintext;
}
```

This ensures correct direction detection and graceful truncation with ellipses.

### Icon Mirroring

Obsidian automatically flips icons horizontally in RTL mode. To prevent flipping a specific icon:

```css
.mod-rtl .my-custom-icon svg {
  transform: none !important;
}
```

---

## Patterns

### Updating UI Elements Dynamically

Combine event registration with stored element references:

```typescript
export default class MyPlugin extends Plugin {
  wordCountEl: HTMLElement;

  async onload() {
    const item = this.addStatusBarItem();
    this.wordCountEl = item.createEl('span', { text: '0 words' });

    this.registerEvent(
      this.app.workspace.on('editor-change', (editor) => {
        const count = editor.getValue().split(/\s+/).length;
        this.wordCountEl.setText(`${count} words`);
      })
    );
  }
}
```

### Mobile Considerations

- `addStatusBarItem()` is desktop-only; gate it with `Platform.isDesktopApp`
- Ribbon icons are available on mobile but may be collapsed into the left drawer
- Avoid hover-dependent interactions; mobile has no cursor hover
- Touch targets should be at least `44x44px`

```typescript
import { Platform } from 'obsidian';

if (Platform.isDesktopApp) {
  const item = this.addStatusBarItem();
  item.setText('Desktop only');
}
```

### Accessibility

- Use semantic HTML (`<button>`, `<label>`, `<nav>`) rather than generic `<div>`s where possible
- Provide `title` attributes or `aria-label` for icon-only buttons
- Ensure sufficient color contrast by using Obsidian's CSS variables (`--text-normal`, `--text-muted`, `--text-accent`)
- Respect `prefers-reduced-motion` if adding CSS animations

```typescript
const btn = containerEl.createEl('button', {
  attr: { 'aria-label': 'Close panel' },
});
setIcon(btn, 'x');
```

---

## Quick Reference Checklist

- [ ] Ribbon icon has a corresponding command as fallback
- [ ] Status bar items are desktop-gated if critical
- [ ] HTML elements use `cls` for styling and Obsidian CSS variables
- [ ] Icons chosen from Lucide (up to v0.446.0) or custom SVG follows guidelines
- [ ] RTL support uses logical CSS properties and `.mod-rtl` selectors where needed
- [ ] Dynamic updates store element references and clean up events in `onunload()`

---

## References

- [Ribbon actions](https://docs.obsidian.md/Plugins/User+interface/Ribbon+actions)
- [Status bar](https://docs.obsidian.md/Plugins/User+interface/Status+bar)
- [HTML elements](https://docs.obsidian.md/Plugins/User+interface/HTML+elements)
- [Icons](https://docs.obsidian.md/Plugins/User+interface/Icons)
- [Right-to-left](https://docs.obsidian.md/Plugins/User+interface/Right-to-left)
- [TypeScript API: addRibbonIcon](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/addRibbonIcon)
- [TypeScript API: addStatusBarItem](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/addStatusBarItem)
- [TypeScript API: setIcon](https://docs.obsidian.md/Reference/TypeScript+API/setIcon)
- [TypeScript API: addIcon](https://docs.obsidian.md/Reference/TypeScript+API/addIcon)
- [Lucide Icons](https://lucide.dev)
