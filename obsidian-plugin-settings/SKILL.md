---
name: obsidian-plugin-settings
description: Design and implement plugin settings UI and persistence for Obsidian. Covers PluginSettingTab, the Setting class with all input types, loadData/saveData, settings interfaces and defaults, async onChange handling, declarative settings, grouping, validation, dynamic settings, and mobile UI considerations. Use when building or refactoring a plugin's settings tab, adding new configuration options, or migrating from imperative to declarative settings.
triggers:
  - obsidian plugin settings
  - obsidian plugin settings tab
  - obsidian plugin configuration
  - obsidian plugin loadData saveData
  - obsidian plugin setting input
  - obsidian plugin setting toggle
  - obsidian plugin setting dropdown
  - obsidian plugin setting slider
  - obsidian plugin setting color picker
  - obsidian plugin setting search
  - obsidian plugin setting button
  - obsidian plugin declarative settings
  - obsidian plugin settings migration
  - obsidian plugin settings validation
  - obsidian plugin dynamic settings
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Settings

This skill guides you through building and persisting plugin settings in Obsidian. It covers both the modern declarative API (Obsidian 1.13.0+) and the legacy imperative `display()` API, because both remain valid and you will encounter existing plugins using the older pattern.

## When to Use This Skill

- Adding a settings tab to a new or existing plugin
- Choosing the right input control for a configuration option
- Persisting and loading plugin data with `loadData()` and `saveData()`
- Migrating an imperative settings tab to the declarative API
- Validating user input, grouping settings, or showing/hiding fields conditionally
- Handling settings that change at runtime (dynamic settings)
- Ensuring settings work well on mobile

## Overview

An Obsidian plugin's settings consist of three layers:

1. **Data model** — a TypeScript interface and default values
2. **Persistence** — `loadData()` and `saveData()` reading/writing `data.json` in the plugin folder
3. **UI** — a `PluginSettingTab` that renders controls and binds them to the data model

Obsidian provides a rich set of built-in controls through the `Setting` class and a declarative `getSettingDefinitions()` API that handles binding, change detection, and saving automatically.

---

## Settings Data Model

### Interface and Defaults

Define the shape of your settings and provide defaults so first-time users have a working configuration immediately:

```typescript
// src/settings.ts
export interface MyPluginSettings {
  apiKey: string;
  enabled: boolean;
  maxItems: number;
  themeColor: string;
  dateFormat: string;
  defaultMode: 'edit' | 'read';
  notes: string;
}

export const DEFAULT_SETTINGS: Partial<MyPluginSettings> = {
  apiKey: '',
  enabled: true,
  maxItems: 10,
  themeColor: '#000000',
  dateFormat: 'YYYY-MM-DD',
  defaultMode: 'edit',
  notes: '',
};
```

> [!tip]
> Use `Partial<MyPluginSettings>` for `DEFAULT_SETTINGS` so TypeScript lets you define defaults for only a subset of fields. This is especially useful during early development when the settings shape is still evolving.

### Loading and Saving

Wire persistence into your plugin entry point:

```typescript
// src/main.ts
import { Plugin } from 'obsidian';
import { MyPluginSettings, DEFAULT_SETTINGS } from './settings';
import { MySettingTab } from './settingsTab';

export default class MyPlugin extends Plugin {
  settings: MyPluginSettings;

  async onload() {
    await this.loadSettings();
    this.addSettingTab(new MySettingTab(this.app, this));
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

**How it works:**
- `loadData()` reads `data.json` from the plugin folder (`.obsidian/plugins/<id>/data.json`). It returns `Promise<any>`; if the file doesn't exist yet, it resolves to `null`.
- `saveData(data)` serializes the given object and writes it to `data.json`. Data must be JSON-serializable.
- `Object.assign({}, DEFAULT_SETTINGS, await this.loadData())` overlays saved values on top of defaults, so missing keys fall back to defaults.

> [!note]
> `saveData` is asynchronous. Always `await` it, especially inside `onChange` handlers, to avoid race conditions if the user edits multiple fields quickly.

### External Settings Changes

If the user syncs their vault and `data.json` changes from another device, implement `onExternalSettingsChange()` to reload:

```typescript
async onExternalSettingsChange() {
  await this.loadSettings();
  // Re-apply any runtime state that depends on settings
}
```

---

## PluginSettingTab

A settings tab is a class extending `PluginSettingTab` that tells Obsidian how to render your plugin's configuration panel.

### Declarative API (Preferred, Obsidian 1.13.0+)

Override `getSettingDefinitions()` to return an array of setting definitions. Obsidian builds the DOM, binds values, and calls `saveData()` for you:

```typescript
import { App, PluginSettingTab } from 'obsidian';
import MyPlugin from './main';

export class MySettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  getSettingDefinitions() {
    return [
      {
        name: 'API key',
        desc: 'Your personal API key for the service.',
        control: {
          type: 'text',
          key: 'apiKey',
          placeholder: 'sk-...',
        },
      },
      {
        name: 'Enable feature',
        control: {
          type: 'toggle',
          key: 'enabled',
        },
      },
      {
        name: 'Max items',
        control: {
          type: 'slider',
          key: 'maxItems',
          min: 1,
          max: 100,
          step: 1,
        },
      },
    ];
  }
}
```

> [!important]
> `control`, `render`, and `action` are mutually exclusive on a single definition. TypeScript will reject more than one.

> [!warning]
> Keep `getSettingDefinitions()` cheap. It is called every time the tab updates and once when the tab is registered (to index settings for global search). Do not perform file reads, network calls, or expensive computation here. Move heavy work into `render` callbacks, which run only when the row is drawn.

### Imperative API (`display()`)

Before Obsidian 1.13.0, settings tabs were built by overriding `display()` and constructing `Setting` rows directly. This API remains fully supported and is still required if your plugin targets `minAppVersion` below 1.13.0:

```typescript
import { App, PluginSettingTab, Setting } from 'obsidian';
import MyPlugin from './main';

export class MySettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    new Setting(containerEl)
      .setName('API key')
      .setDesc('Your personal API key for the service.')
      .addText(text => text
        .setPlaceholder('sk-...')
        .setValue(this.plugin.settings.apiKey)
        .onChange(async (value) => {
          this.plugin.settings.apiKey = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Enable feature')
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.enabled)
        .onChange(async (value) => {
          this.plugin.settings.enabled = value;
          await this.plugin.saveSettings();
        }));
  }
}
```

> [!note]
> The imperative API is the only way to access certain advanced controls (`addMomentFormat`, `addProgressBar`, `addSearch` with custom suggesters, `addExtraButton`) inside a settings tab before 1.13.0. On 1.13.0+, use `render` callbacks within `getSettingDefinitions()` for these.

### Hybrid / Dual Support

If you need to support both old and new Obsidian versions, implement both `getSettingDefinitions()` and `display()`. Obsidian uses `getSettingDefinitions()` when available and falls back to `display()` on older versions.

---

## The `Setting` Class

The `Setting` class creates a labeled row with a name, optional description, and one or more controls.

```typescript
new Setting(containerEl)
  .setName('Setting name')
  .setDesc('Optional description')
  .addText(text => text.setValue('...'));
```

### Row Structure

Each `Setting` instance exposes these DOM elements:

| Property | Element |
|----------|---------|
| `settingEl` | The outer row container |
| `infoEl` | The left side (name + description) |
| `nameEl` | The name heading |
| `descEl` | The description text |
| `controlEl` | The right side (controls) |
| `components` | Array of attached `BaseComponent` instances |

You can also apply CSS classes or disable the whole row:

```typescript
new Setting(containerEl)
  .setName('Advanced')
  .setClass('advanced-setting')
  .setDisabled(true)
  .addText(text => text.setValue('...'));
```

### Headings

Use `setHeading()` to turn a setting row into a section header:

```typescript
new Setting(containerEl)
  .setName('Appearance')
  .setHeading();
```

---

## Input Types

All input types are available through `Setting.add…()` methods. On Obsidian 1.13.0+, many have matching declarative `control` types; the rest are available via `render` callbacks or the imperative API.

### `.addText()`

Single-line text input. Returns a `TextComponent`.

```typescript
new Setting(containerEl)
  .setName('Folder name')
  .addText(text => text
    .setPlaceholder('/')
    .setValue(this.plugin.settings.folder)
    .onChange(async (value) => {
      this.plugin.settings.folder = value;
      await this.plugin.saveSettings();
    }));
```

**Common methods:**
- `setValue(value: string)` — set current value
- `setPlaceholder(placeholder: string)` — placeholder text
- `onChange(callback: (value: string) => any)` — change handler
- `getValue()` — read current value
- `setDisabled(disabled: boolean)` — disable interaction

### `.addTextArea()`

Multi-line text input. Returns a `TextAreaComponent` (extends `AbstractTextComponent<HTMLTextAreaElement>`).

```typescript
new Setting(containerEl)
  .setName('Notes')
  .addTextArea(text => text
    .setPlaceholder('Enter multi-line notes...')
    .setValue(this.plugin.settings.notes)
    .onChange(async (value) => {
      this.plugin.settings.notes = value;
      await this.plugin.saveSettings();
    }));
```

> [!tip]
> `TextAreaComponent` inherits the same methods as `TextComponent`: `setValue`, `setPlaceholder`, `onChange`, `getValue`, `setDisabled`.

### `.addToggle()`

Boolean switch. Returns a `ToggleComponent`.

```typescript
new Setting(containerEl)
  .setName('Enable feature')
  .addToggle(toggle => toggle
    .setValue(this.plugin.settings.enabled)
    .onChange(async (value) => {
      this.plugin.settings.enabled = value;
      await this.plugin.saveSettings();
    }));
```

**Common methods:**
- `setValue(on: boolean)`
- `onChange(callback: (value: boolean) => any)`
- `getValue()`
- `setTooltip(tooltip: string, options?: TooltipOptions)`
- `setDisabled(disabled: boolean)`

### `.addSlider()`

Numeric slider. Returns a `SliderComponent`.

```typescript
new Setting(containerEl)
  .setName('Volume')
  .addSlider(slider => slider
    .setLimits(0, 100, 1)
    .setValue(this.plugin.settings.volume)
    .setDynamicTooltip()
    .onChange(async (value) => {
      this.plugin.settings.volume = value;
      await this.plugin.saveSettings();
    }));
```

**Common methods:**
- `setLimits(min: number, max: number, step: number)` — required before setting value
- `setValue(value: number)`
- `onChange(callback: (value: number) => any)`
- `getValue()`
- `setDynamicTooltip()` — shows current value as tooltip while dragging

> [!note]
> In the declarative API, `slider` controls require `min`, `max`, and `step`.

### `.addDropdown()`

Dropdown selection. Returns a `DropdownComponent`.

```typescript
new Setting(containerEl)
  .setName('Default mode')
  .addDropdown(dropdown => dropdown
    .addOption('edit', 'Editing')
    .addOption('read', 'Reading')
    .setValue(this.plugin.settings.defaultMode)
    .onChange(async (value) => {
      this.plugin.settings.defaultMode = value as 'edit' | 'read';
      await this.plugin.saveSettings();
    }));
```

**Common methods:**
- `addOption(value: string, display: string)` — add an option
- `addOptions(options: Record<string, string>)` — batch add
- `setValue(value: string)`
- `onChange(callback: (value: string) => any)`
- `getValue()`

### `.addColorPicker()`

Color picker. Values are 6-digit hash-prefixed hex strings like `#000000`. Returns a `ColorComponent`.

```typescript
new Setting(containerEl)
  .setName('Accent color')
  .addColorPicker(color => color
    .setValue(this.plugin.settings.themeColor)
    .onChange(async (value) => {
      this.plugin.settings.themeColor = value;
      await this.plugin.saveSettings();
    }));
```

**Common methods:**
- `setValue(value: string)` — hex string
- `setValueRgb(rgb: RGB)` — set via `{ r, g, b }` object
- `setValueHsl(hsl: HSL)` — set via `{ h, s, l }` object
- `getValue()` — returns hex string
- `getValueRgb()` — returns `RGB`
- `getValueHsl()` — returns `HSL`
- `onChange(callback: (value: string) => any)`

### `.addButton()`

Action button. Returns a `ButtonComponent`. Useful for one-off actions (export, reset, open modal).

```typescript
new Setting(containerEl)
  .setName('Export data')
  .setDesc('Download all plugin data as JSON.')
  .addButton(button => button
    .setButtonText('Export')
    .setCta()
    .onClick(() => {
      // perform export
      new Notice('Export complete!');
    }));
```

**Common methods:**
- `setButtonText(name: string)`
- `setCta()` — style as primary call-to-action
- `removeCta()` — remove CTA styling
- `setWarning()` — style as warning
- `setIcon(icon: string)` — add icon (requires valid Obsidian icon ID)
- `setTooltip(tooltip: string, options?: TooltipOptions)`
- `setClass(cls: string)`
- `onClick(callback: () => any)`

### `.addMomentFormat()`

Date/time format input with live preview. Returns a `MomentFormatComponent` (extends `TextComponent`).

```typescript
let dateSampleEl: HTMLElement;
const dateDesc = createFragment((frag) => {
  frag.appendText('Your current syntax looks like this: ');
  dateSampleEl = frag.createEl('b', 'u-pop');
});

new Setting(containerEl)
  .setName('Date format')
  .setDesc(dateDesc)
  .addMomentFormat((momentFormat) => momentFormat
    .setValue(this.plugin.settings.dateFormat)
    .setSampleEl(dateSampleEl)
    .setDefaultFormat('YYYY-MM-DD')
    .onChange(async (value) => {
      this.plugin.settings.dateFormat = value;
      await this.plugin.saveSettings();
    }));
```

**Common methods:**
- `setValue(value: string)`
- `setDefaultFormat(defaultFormat: string)` — placeholder and fallback when cleared
- `setSampleEl(sampleEl: HTMLElement)` — element to update with preview
- `updateSample()` — manually refresh the preview
- `onChange(callback: (value: string) => any)`

> [!note]
> `MomentFormatComponent` does not have a declarative control type yet. Use a `render` callback on 1.13.0+.

### `.addSearch()`

Search input with optional suggester integration. Returns a `SearchComponent` (extends `AbstractTextComponent<HTMLInputElement>`).

```typescript
new Setting(containerEl)
  .setName('Icon')
  .addSearch((search) => {
    search
      .setValue(this.plugin.settings.icon)
      .setPlaceholder('Search for an icon')
      .onChange(async (value) => {
        this.plugin.settings.icon = value;
        await this.plugin.saveSettings();
      });
    new IconSuggester(this.app, search.inputEl);
  });
```

**Common methods:**
- `setValue(value: string)`
- `setPlaceholder(placeholder: string)`
- `onChange(callback: (value: string) => any)`
- `getValue()`
- `clearButtonEl` — the built-in clear button element

> [!tip]
> Pair `addSearch()` with a subclass of `AbstractInputSuggest` to provide live suggestions. Attach it to `search.inputEl`.

### `.addProgressBar()`

Visual progress indicator. Returns a `ProgressBarComponent`. Useful for showing task progress or quotas.

```typescript
new Setting(containerEl)
  .setName('Sync progress')
  .setDesc('Current sync status.')
  .addProgressBar((bar) => bar.setValue(50));
```

**Common methods:**
- `setValue(value: number)` — 0–100 range typical
- `getValue()`

> [!note]
> `ProgressBarComponent` does not have a declarative control type yet. Use a `render` callback on 1.13.0+.

### `.addExtraButton()`

Compact icon-only button for secondary actions on a row: reset to default, open help, copy value, etc. Returns an `ExtraButtonComponent`.

```typescript
new Setting(containerEl)
  .setName('API endpoint')
  .addText((text) => text.setValue(this.plugin.settings.endpoint))
  .addExtraButton((button) => button
    .setIcon('lucide-rotate-ccw')
    .setTooltip('Reset to default')
    .onClick(() => {
      this.plugin.settings.endpoint = DEFAULT_SETTINGS.endpoint || '';
      this.plugin.saveSettings();
      this.display(); // re-render to reflect reset
    }));
```

**Common methods:**
- `setIcon(icon: string)`
- `setTooltip(tooltip: string, options?: TooltipOptions)`
- `onClick(callback: () => any)`
- `setDisabled(disabled: boolean)`

---

## Declarative Settings Deep Dive

### Control Types Reference

| Declarative type | Stored value | Required / Optional params |
|------------------|-------------|--------------------------|
| `toggle` | `boolean` | — |
| `text` | `string` | `placeholder?` |
| `textarea` | `string` | `placeholder?`, `rows?` |
| `number` | `number` | `min?`, `max?`, `step?`, `placeholder?` |
| `slider` | `number` | `min`, `max`, `step` |
| `dropdown` | `string` | `options: { value: 'Display', … }` |
| `file` | `string` (path) | `filter?`, `placeholder?` |
| `folder` | `string` (path) | `filter?`, `includeRoot?` (default `false`), `placeholder?` |
| `color` | `string` (hex) | — |

Every control accepts:
- `defaultValue?` — fallback when stored value is `undefined` or `null`
- `validate?` — callback returning error string or `undefined` to reject/accept

### Validation

Return a non-empty string to block the change and show an inline error:

```typescript
{
  name: 'File extension',
  control: {
    type: 'text',
    key: 'extension',
    validate: (value) => /\s/.test(value) ? 'Extension cannot contain spaces.' : undefined,
  },
}
```

Async validators work too: return `Promise<string | undefined>`.

> [!warning]
> `validate` is a UI gate, not a data invariant. The stored value may already be invalid when rendered (e.g., saved by an older plugin version). Validate again when reading settings if invariants are critical.

### Conditional Visibility and Enabling

Use `visible` and `disabled` predicates to react to other settings without rebuilding the tab:

```typescript
getSettingDefinitions() {
  return [
    {
      name: 'Enable advanced mode',
      control: { type: 'toggle', key: 'advanced' },
    },
    {
      name: 'Debug log level',
      desc: 'Only relevant when advanced mode is on.',
      visible: () => this.plugin.settings.advanced,
      control: {
        type: 'dropdown',
        key: 'logLevel',
        defaultValue: 'info',
        options: { info: 'Info', verbose: 'Verbose' },
      },
    },
    {
      name: 'Cache size (MB)',
      control: {
        type: 'number',
        key: 'cacheMb',
        min: 1,
        disabled: () => !this.plugin.settings.advanced,
      },
    },
  ];
}
```

- `visible: boolean | () => boolean` — hides the row entirely
- `disabled: boolean | () => boolean` — greys out the control but keeps the row visible

After mutating dependent state from a `render` callback or imperative path, call `this.refreshDomState()` to re-run predicates without a full re-render. For changes that add or remove definitions, call `this.update()` instead.

### Groups

Organize settings into collapsible or titled sections:

```typescript
getSettingDefinitions() {
  return [
    {
      type: 'group',
      heading: 'Appearance',
      items: [
        { name: 'Accent color', control: { type: 'color', key: 'accent' } },
        { name: 'Font size', control: { type: 'number', key: 'fontSize', min: 8, max: 32 } },
      ],
    },
    {
      type: 'group',
      heading: 'Behavior',
      items: [
        { name: 'Auto-save', control: { type: 'toggle', key: 'autoSave' } },
      ],
    },
  ];
}
```

### Lists

For user-managed collections (tag aliases, blocked domains, templates), use `type: 'list'`:

```typescript
{
  type: 'list',
  heading: 'Blocked domains',
  addText: 'Add domain',
  emptyText: 'No domains blocked.',
  action: (index: number) => {
    // Remove or edit the item at index
    this.plugin.settings.blocked.splice(index, 1);
    this.plugin.saveSettings();
    this.update();
  },
  items: this.plugin.settings.blocked.map((domain, index) => ({
    name: domain,
    action: index,
  })),
}
```

> [!note]
> The exact `list` API shape may vary by Obsidian version. Refer to the current TypeScript definitions for `SettingDefinitionList` if the compiler complains.

### Render Callback

When a declarative control type doesn't exist, or you need side effects, use `render`:

```typescript
{
  name: 'Date format',
  render: (setting: Setting) => {
    let sampleEl: HTMLElement;
    const desc = createFragment((frag) => {
      frag.appendText('Preview: ');
      sampleEl = frag.createEl('b');
    });

    setting
      .setDesc(desc)
      .addMomentFormat((momentFormat) => momentFormat
        .setValue(this.plugin.settings.dateFormat)
        .setSampleEl(sampleEl)
        .setDefaultFormat('YYYY-MM-DD')
        .onChange(async (value) => {
          this.plugin.settings.dateFormat = value;
          await this.plugin.saveSettings();
        }));
  },
}
```

### Custom Settings Storage

If your plugin stores settings somewhere other than `this.plugin.settings` (e.g., a Svelte store, immutable update pattern), override `getControlValue` and `setControlValue`:

```typescript
class MySettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  getControlValue(key: string): unknown {
    // Read from wherever your plugin keeps settings
    return this.plugin.settings[key];
  }

  async setControlValue(key: string, value: unknown): Promise<void> {
    // Update and persist yourself
    this.plugin.settings[key] = value;
    await this.plugin.saveData(this.plugin.settings);
  }

  getSettingDefinitions() { /* … */ }
}
```

> [!important]
> Overriding `setControlValue` replaces the default write path, including the automatic `saveData()` call. You must persist the data yourself.

---

## Async onChange Handling

Every control's `onChange` callback is your hook to update the data model and persist it. **Always make the handler async and await `saveSettings()`**:

```typescript
.onChange(async (value) => {
  this.plugin.settings.mySetting = value;
  await this.plugin.saveSettings();
})
```

### Debouncing Expensive Side Effects

If your `onChange` triggers expensive work (re-indexing, network calls, DOM rebuilds), debounce it so rapid changes don't queue up:

```typescript
import { debounce } from 'obsidian';

export class MySettingTab extends PluginSettingTab {
  private debouncedReindex = debounce(
    () => this.plugin.reindex(),
    500,
    true
  );

  display(): void {
    // ...
    new Setting(containerEl)
      .setName('Search folders')
      .addText(text => text
        .setValue(this.plugin.settings.searchFolders)
        .onChange(async (value) => {
          this.plugin.settings.searchFolders = value;
          await this.plugin.saveSettings();
          this.debouncedReindex();
        }));
  }
}
```

### Re-rendering After External Changes

If a button changes settings (e.g., reset to defaults), call `this.display()` to rebuild the tab so controls reflect the new values:

```typescript
.addExtraButton((button) => button
  .setIcon('lucide-rotate-ccw')
  .onClick(() => {
    this.plugin.settings = Object.assign({}, DEFAULT_SETTINGS);
    this.plugin.saveSettings();
    this.display(); // imperative tab
  }))
```

For declarative tabs, mutating `this.plugin.settings` and calling `this.update()` rebuilds the definition list and re-renders affected rows.

---

## Declarative Settings Migration

If you have an existing imperative `display()` tab and want to migrate to `getSettingDefinitions()`:

1. **Extract controls** — map each `new Setting(containerEl)…addX()` block to a `control` definition.
2. **Remove manual `saveData()` calls** — the declarative API handles persistence automatically.
3. **Move side effects** into `render` callbacks or `onChange` wrappers inside `control` definitions where supported.
4. **Implement both methods** during a transition period if you need to support `minAppVersion` below 1.13.0:

```typescript
export class MySettingTab extends PluginSettingTab {
  // New: declarative API
  getSettingDefinitions() {
    if (requireApiVersion('1.13.0')) {
      return [ /* … */ ];
    }
    return [];
  }

  // Legacy: imperative fallback
  display(): void {
    if (requireApiVersion('1.13.0')) return;
    // old imperative code …
  }
}
```

> [!tip]
> Keep the imperative code around only until you raise `minAppVersion` to 1.13.0 or higher. The declarative API is preferred for new code because it reduces boilerplate and gives users global settings search for free.

---

## Patterns

### Grouping Settings

Use visual groups to reduce cognitive load. In the imperative API, use `setHeading()` or insert custom DOM:

```typescript
containerEl.createEl('h3', { text: 'Appearance' });

new Setting(containerEl)
  .setName('Theme color')
  .addColorPicker(/* … */);

new Setting(containerEl)
  .setName('Font size')
  .addSlider(/* … */);

containerEl.createEl('h3', { text: 'Behavior' });
// …
```

In the declarative API, use `type: 'group'` definitions.

### Validation Patterns

Validate at three layers:

1. **UI** — `validate` callback on declarative controls (gives immediate feedback)
2. **Load time** — sanitize `data.json` after `loadData()` to handle legacy or corrupted values
3. **Runtime** — guard code that depends on settings values (e.g., check `apiKey` is non-empty before making a request)

```typescript
async loadSettings() {
  const raw = await this.loadData();
  this.settings = Object.assign({}, DEFAULT_SETTINGS, raw);

  // Sanitize loaded values
  if (typeof this.settings.maxItems !== 'number' || this.settings.maxItems < 1) {
    this.settings.maxItems = DEFAULT_SETTINGS.maxItems ?? 10;
  }
}
```

### Dynamic Settings

When one setting changes the available options of another:

**Imperative approach:** rebuild the affected control inside `onChange`:

```typescript
.addDropdown(dropdown => {
  const refreshOptions = () => {
    dropdown.selectEl.empty();
    const opts = this.plugin.settings.advanced
      ? { a: 'Advanced A', b: 'Advanced B' }
      : { a: 'Simple A' };
    dropdown.addOptions(opts);
    dropdown.setValue(this.plugin.settings.mode);
  };

  refreshOptions();
  dropdown.onChange(async (value) => {
    this.plugin.settings.mode = value;
    await this.plugin.saveSettings();
  });
})
```

**Declarative approach:** use `visible`/`disabled` predicates and call `this.refreshDomState()` after imperative mutations.

### Mobile UI Considerations

- **Keep labels short** — mobile settings panes are narrow; long names wrap awkwardly.
- **Avoid overcrowding rows** — a single row with both a text input and two extra buttons can overflow on small screens. Split into separate rows or use groups.
- **Test touch targets** — sliders and toggles should be easy to hit with a finger. The default Obsidian controls are already optimized; custom DOM may need padding.
- **Don't rely on hover** — tooltips on hover don't exist on touch devices. Use `setDesc()` to surface critical context as static text.
- **Conditional `isDesktopOnly`** — if a setting only makes sense on desktop (e.g., a path to an external binary), hide or disable it on mobile using `Platform.isMobile`:

```typescript
import { Platform } from 'obsidian';

// In declarative tab
{
  name: 'External binary path',
  visible: () => Platform.isDesktopApp,
  control: { type: 'text', key: 'binaryPath' },
}
```

---

## Settings Inside Modals

The declarative `getSettingDefinitions()` API is only for `PluginSettingTab`. If you need setting rows inside a [[Modal]], use `Setting` and `SettingGroup` directly against the modal's `contentEl`:

```typescript
class ConfigModal extends Modal {
  constructor(app: App, private plugin: MyPlugin) {
    super(app);
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();

    new Setting(contentEl)
      .setName('Quick toggle')
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.enabled)
        .onChange(async (value) => {
          this.plugin.settings.enabled = value;
          await this.plugin.saveSettings();
        }));
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}
```

---

## Quick Reference Checklist

- [ ] Define `interface MyPluginSettings` and `DEFAULT_SETTINGS`
- [ ] Implement `loadSettings()` with `Object.assign({}, DEFAULT_SETTINGS, await this.loadData())`
- [ ] Implement `saveSettings()` as `await this.saveData(this.settings)`
- [ ] Register the tab with `this.addSettingTab(new MySettingTab(this.app, this))`
- [ ] Choose declarative (`getSettingDefinitions()`) if `minAppVersion` ≥ 1.13.0, otherwise imperative (`display()`)
- [ ] Use `onChange(async (value) => { … await this.plugin.saveSettings(); })` for every mutable control
- [ ] Add `validate` callbacks for user-facing constraints
- [ ] Sanitize loaded data after `loadData()` to guard against corruption or legacy shapes
- [ ] Call `this.display()` (imperative) or `this.update()` (declarative) after programmatic settings changes
- [ ] Hide desktop-only settings on mobile with `Platform.isMobile`
- [ ] Implement `onExternalSettingsChange()` if users sync vaults across devices

---

## References

- [Plugin settings UI](https://docs.obsidian.md/Plugins/User+interface/Settings) — Official guide covering declarative and imperative APIs
- [Setting class](https://docs.obsidian.md/Reference/TypeScript+API/Setting) — Full method list for `Setting`
- [PluginSettingTab class](https://docs.obsidian.md/Reference/TypeScript+API/PluginSettingTab) — Tab base class reference
- [Plugin.loadData()](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/loadData) — Load `data.json` from disk
- [Plugin.saveData()](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/saveData) — Write `data.json` to disk
- [ButtonComponent](https://docs.obsidian.md/Reference/TypeScript+API/ButtonComponent) — Button control API
- [ToggleComponent](https://docs.obsidian.md/Reference/TypeScript+API/ToggleComponent) — Toggle control API
- [ColorComponent](https://docs.obsidian.md/Reference/TypeScript+API/ColorComponent) — Color picker API
- [SearchComponent](https://docs.obsidian.md/Reference/TypeScript+API/SearchComponent) — Search input API
- [MomentFormatComponent](https://docs.obsidian.md/Reference/TypeScript+API/MomentFormatComponent) — Date format input API
- [AbstractInputSuggest](https://docs.obsidian.md/Reference/TypeScript+API/AbstractInputSuggest) — Base class for custom suggesters
- [Migrate to declarative settings](https://docs.obsidian.md/Plugins/User+interface/Settings) — Migration guidance from imperative to declarative
- [Mobile development](https://docs.obsidian.md/Plugins/Getting+started/Mobile+development) — Platform constraints and `Platform` utility
