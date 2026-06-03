---
name: obsidian-plugin-styling
description: Style Obsidian plugins with CSS. Covers Obsidian CSS variables, dynamic stylesheet injection, styles.css loading and scoping, dark/light mode adaptation, theme-specific selectors, avoiding conflicts with other plugins and themes, mobile styling, and animation best practices. Use when writing, debugging, or refactoring plugin CSS.
triggers:
  - obsidian plugin styling
  - obsidian plugin css
  - obsidian plugin styles
  - obsidian plugin theme
  - obsidian plugin dark mode
  - obsidian plugin light mode
  - obsidian plugin stylesheet
  - obsidian plugin css variables
  - obsidian plugin mobile styling
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Styling

This skill helps you write CSS that makes your plugin look native in any Obsidian theme. It covers the variable system, stylesheet delivery, dark/light adaptation, scoping strategies, and mobile constraints.

## When to Use This Skill

- Writing or refactoring CSS for an Obsidian plugin
- Making a plugin respect the user's active theme and color scheme
- Injecting styles dynamically at runtime
- Debugging style leaks or conflicts with other plugins
- Optimizing UI for mobile (phones and tablets)

## Overview

Obsidian exposes 400+ CSS custom properties. Using them keeps your plugin visually consistent and lets community themes style your UI automatically. A plugin can ship static CSS via `styles.css` or append a `<style>` tag at runtime. Either way, your selectors should be scoped and theme-aware.

---

## CSS Variables Reference

Obsidian organizes variables into **Foundations**, **Components**, **Editor**, **Plugins**, and **Window**. Always prefer these over hardcoded values.

### Colors

#### Base palette
| Variable | Light | Dark |
|----------|-------|------|
| `--color-base-00` | `#ffffff` | `#1e1e1e` |
| `--color-base-05` | `#fcfcfc` | `#212121` |
| `--color-base-10` | `#fafafa` | `#242424` |
| `--color-base-20` | `#f6f6f6` | `#262626` |
| `--color-base-25` | `#e3e3e3` | `#2a2a2a` |
| `--color-base-30` | `#e0e0e0` | `#363636` |
| `--color-base-35` | `#d4d4d4` | `#3f3f3f` |
| `--color-base-40` | `#bdbdbd` | `#555555` |
| `--color-base-50` | `#ababab` | `#666666` |
| `--color-base-60` | `#707070` | `#999999` |
| `--color-base-70` | `#5a5a5a` | `#bababa` |
| `--color-base-100` | `#222222` | `#dadada` |

#### Accent
| Variable | Default | Description |
|----------|---------|-------------|
| `--accent-h` | `254` | Hue |
| `--accent-s` | `80%` | Saturation |
| `--accent-l` | `68%` | Lightness |

#### Semantic colors
| Variable | Description |
|----------|-------------|
| `--background-primary` | Primary background |
| `--background-primary-alt` | Surface on top of primary |
| `--background-secondary` | Secondary background |
| `--background-secondary-alt` | Surface on top of secondary |
| `--background-modifier-hover` | Hovered elements |
| `--background-modifier-active-hover` | Active hovered elements |
| `--background-modifier-border` | Border color |
| `--background-modifier-border-hover` | Border (hover) |
| `--background-modifier-border-focus` | Border (focus) |
| `--background-modifier-error` | Error background |
| `--background-modifier-success` | Success background |
| `--interactive-normal` | Standard interactive background |
| `--interactive-hover` | Interactive hover |
| `--interactive-accent` | Accent interactive background |
| `--interactive-accent-hover` | Accent interactive hover |
| `--text-normal` | Normal text |
| `--text-muted` | Muted text |
| `--text-faint` | Faint text |
| `--text-on-accent` | Text on dark accent |
| `--text-on-accent-inverted` | Text on light accent |
| `--text-accent` | Accent text |
| `--text-accent-hover` | Accent text (hover) |
| `--text-selection` | Selected text background |
| `--text-highlight-bg` | Highlighted text background |

> [!tip]
> Extended colors (`--color-red`, `--color-orange`, etc.) also have `-rgb` variants (e.g., `--color-red-rgb`) for use inside `rgba()`.

### Typography

| Variable | Description |
|----------|-------------|
| `--font-interface-theme` | UI font |
| `--font-text-theme` | Editor font |
| `--font-monospace-theme` | Code font |
| `--font-text-size` | Editor font size (user setting) |
| `--font-smallest` | `0.8em` |
| `--font-smaller` | `0.875em` |
| `--font-small` | `0.933em` |
| `--font-ui-smaller` | `12px` |
| `--font-ui-small` | `13px` |
| `--font-ui-medium` | `15px` |
| `--font-ui-large` | `20px` |
| `--line-height-normal` | `1.5` |
| `--line-height-tight` | `1.3` |

### Spacing

Obsidian uses a **4-pixel grid**. Prefer `--size-4-*` for margins and padding.

| Variable | Value |
|----------|-------|
| `--size-4-1` | `4px` |
| `--size-4-2` | `8px` |
| `--size-4-3` | `12px` |
| `--size-4-4` | `16px` |
| `--size-4-5` | `20px` |
| `--size-4-6` | `24px` |
| `--size-4-8` | `32px` |
| `--size-4-9` | `36px` |
| `--size-4-12` | `48px` |
| `--size-4-16` | `64px` |
| `--size-4-18` | `72px` |

> [!note]
> A 2-pixel grid (`--size-2-*`) exists for fine-grained control; use it sparingly.

### Icons

| Variable | Description |
|----------|-------------|
| `--icon-size` | Width and height shorthand |
| `--icon-stroke` | Stroke width shorthand |
| `--icon-color` | Base icon color |
| `--icon-color-hover` | Hover color |
| `--icon-color-active` | Active color |
| `--icon-color-focused` | Focused color |
| `--icon-opacity` | Base opacity |
| `--icon-opacity-hover` | Hover opacity |
| `--icon-opacity-active` | Active opacity |

Icon sizes: `--icon-xs` (`14px`), `--icon-s` (`16px`), `--icon-m` (`18px`), `--icon-l` (`18px`), `--icon-xl` (`32px`).

---

## Appending Stylesheets Dynamically

Use runtime injection when styles depend on user settings or must be computed.

```typescript
export default class MyPlugin extends Plugin {
  styleEl: HTMLStyleElement;

  onload() {
    this.styleEl = document.createElement('style');
    this.styleEl.id = 'my-plugin-dynamic-styles';
    document.head.appendChild(this.styleEl);

    this.updateStyles();
  }

  updateStyles() {
    const accent = getComputedStyle(document.body)
      .getPropertyValue('--interactive-accent')
      .trim();

    this.styleEl.textContent = `
      .my-plugin-badge {
        background-color: ${accent};
        color: var(--text-on-accent);
      }
    `;
  }

  onunload() {
    this.styleEl?.remove();
  }
}
```

> [!caution]
> Always set a unique `id` so you can remove the element cleanly in `onunload()`.

---

## styles.css Loading and Scoping

If a file named `styles.css` exists in your plugin directory next to `main.js`, Obsidian injects it automatically as a global stylesheet.

**Rules of thumb:**
- Never use bare element selectors (e.g., `div { ... }`). Scope everything under a plugin-specific class.
- Use BEM-style naming: `.my-plugin__element--modifier`.
- Keep specificity low to make it easy for themes to override.

```css
/* styles.css */
.my-plugin-panel {
  background-color: var(--background-secondary);
  border: var(--border-width) solid var(--background-modifier-border);
  border-radius: var(--radius-m);
  padding: var(--size-4-4);
}

.my-plugin-panel__title {
  font-family: var(--font-interface-theme);
  font-size: var(--font-ui-medium);
  font-weight: var(--font-semibold);
  color: var(--text-normal);
}
```

---

## Dark/Light Mode Detection and Adaptation

Obsidian toggles the `.theme-dark` and `.theme-light` classes on `body`. Target these for scheme-specific overrides.

```css
/* Default (shared) */
.my-plugin-panel {
  background-color: var(--background-secondary);
}

/* Dark overrides */
.theme-dark .my-plugin-panel {
  --my-plugin-glow: 0 0 8px rgba(0, 0, 0, 0.5);
  box-shadow: var(--my-plugin-glow);
}

/* Light overrides */
.theme-light .my-plugin-panel {
  --my-plugin-glow: 0 0 8px rgba(0, 0, 0, 0.15);
  box-shadow: var(--my-plugin-glow);
}
```

### Programmatic detection

```typescript
const isDark = document.body.classList.contains('theme-dark');
```

If you need the active theme name (e.g., to apply special fixes for a specific community theme), you can read the internal config value:

```typescript
// @ts-ignore — not yet in public API types
const themeName = this.app.vault.getConfig('cssTheme') as string;
```

> [!note]
> Prefer CSS variables over branching on the theme name. Only use the theme name for edge-case workarounds.

---

## Theme-Specific Classes and Selectors

| Class | Purpose |
|-------|---------|
| `.theme-dark` | Active base scheme is dark |
| `.theme-light` | Active base scheme is light |
| `.is-mobile` | Running on a mobile device (phone or tablet) |
| `.is-phone` | Running on a phone |
| `.is-tablet` | Running on a tablet |

You can combine them for precise targeting:

```css
.theme-dark.is-mobile .my-plugin-panel {
  border-color: var(--background-modifier-border-hover);
}
```

---

## Avoiding CSS Conflicts

### 1. Namespace every class
Prefix every class with your plugin ID or a short abbreviation.

```css
/* Good */
.my-plugin-btn { }
.my-plugin-btn--primary { }

/* Bad */
.btn { }
.primary { }
```

### 2. Avoid `!important`
It raises specificity wars and makes theme overrides painful.

### 3. Don't style Obsidian core classes directly
Unless you are intentionally overriding core UI, never target `.nav-file`, `.workspace-tab-header`, etc., from `styles.css`. If you must, use the weakest selector possible and document it.

### 4. Use `data-*` attributes for state
Instead of adding/removing classes like `.active`, use a single class and an attribute:

```css
.my-plugin-tab[data-active="true"] {
  background-color: var(--background-modifier-hover);
}
```

---

## Mobile Styling Considerations

- **Status bar** is hidden on mobile. Do not rely on `addStatusBarItem()` for critical UI.
- **Viewport units** can be unreliable because of dynamic browser chrome. Use `100dvh` where supported, or let Obsidian's layout system handle sizing.
- **Touch targets** should be at least `44px`. Use `--size-4-12` (`48px`) for buttons.
- **Reduced motion**: Respect `prefers-reduced-motion` for animations.

```css
.my-plugin-fade {
  transition: opacity 150ms ease;
}

@media (prefers-reduced-motion: reduce) {
  .my-plugin-fade {
    transition: none;
  }
}
```

- **Platform classes**: Use `.is-mobile`, `.is-phone`, `.is-tablet` to adjust layouts without JavaScript.

```css
.is-phone .my-plugin-modal {
  width: 100vw;
  margin: 0;
}
```

---

## Patterns

### Scoped CSS with BEM

```css
/* Block */
.my-plugin-card { }

/* Element */
.my-plugin-card__header { }
.my-plugin-card__body { }

/* Modifier */
.my-plugin-card--compact { }
.my-plugin-card--danger { }
```

### Conditional Theming

Use CSS custom properties as an API surface for themes:

```css
:root {
  --my-plugin-radius: var(--radius-m);
  --my-plugin-padding: var(--size-4-4);
}

.theme-dark {
  --my-plugin-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

.theme-light {
  --my-plugin-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.my-plugin-card {
  border-radius: var(--my-plugin-radius);
  padding: var(--my-plugin-padding);
  box-shadow: var(--my-plugin-shadow);
}
```

### Icon Styling

Use Obsidian's icon variables so your icons match the surrounding UI:

```css
.my-plugin-icon {
  width: var(--icon-m);
  height: var(--icon-m);
  stroke-width: var(--icon-m-stroke-width);
  color: var(--icon-color);
}

.my-plugin-icon:hover {
  color: var(--icon-color-hover);
}
```

### Animation Best Practices

- Keep transitions under `200ms` for UI feedback.
- Use `transform` and `opacity` for performant animations.
- Always provide a reduced-motion fallback.

```css
.my-plugin-toast {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 150ms ease, transform 150ms ease;
}

.my-plugin-toast.is-visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .my-plugin-toast {
    transition: none;
  }
}
```

---

## Quick Checklist

- [ ] All colors come from Obsidian CSS variables (no hex codes in TS/JS)
- [ ] Selectors are scoped behind a plugin-specific class
- [ ] Dark and light modes are handled via `.theme-dark` / `.theme-light`
- [ ] Mobile layout tested with `.is-mobile` or `this.app.emulateMobile(true)`
- [ ] `styles.css` (or dynamic `<style>`) is cleaned up in `onunload()`
- [ ] Animations respect `prefers-reduced-motion`

---

## References

- [About styling](https://docs.obsidian.md/Reference/CSS+variables/About+styling) — Official intro to Obsidian CSS
- [CSS variables](https://docs.obsidian.md/Reference/CSS+variables/CSS+variables) — Full variable categories
- [Colors](https://docs.obsidian.md/Reference/CSS+variables/Foundations/Colors) — Color palette reference
- [Spacing](https://docs.obsidian.md/Reference/CSS+variables/Foundations/Spacing) — 4-pixel grid system
- [Typography](https://docs.obsidian.md/Reference/CSS+variables/Foundations/Typography) — Fonts and sizing
- [Icons](https://docs.obsidian.md/Reference/CSS+variables/Foundations/Icons) — Icon variable reference
- [HTML elements](https://docs.obsidian.md/Plugins/User+interface/HTML+elements) — Using `createEl()` and `styles.css`
- [Build a theme](https://docs.obsidian.md/Themes/App+themes/Build+a+theme) — Theme dark/light patterns
- [Plugin guidelines](https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines) — Official plugin do's and don'ts
- [Mobile development](https://docs.obsidian.md/Plugins/Getting+started/Mobile+development) — Platform emulation and constraints
