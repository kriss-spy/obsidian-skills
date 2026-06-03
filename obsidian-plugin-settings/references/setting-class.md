# Setting Class Reference

## Constructor

```typescript
new Setting(containerEl: HTMLElement)
```

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `settingEl` | `HTMLElement` | Outer row container |
| `infoEl` | `HTMLElement` | Left side (name + desc) |
| `nameEl` | `HTMLElement` | Name heading |
| `descEl` | `HTMLElement` | Description text |
| `controlEl` | `HTMLElement` | Right side (controls) |
| `components` | `BaseComponent[]` | Attached components |

## Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `setName(name: string)` | `this` | Set display name |
| `setDesc(desc: string \| DocumentFragment)` | `this` | Set description |
| `setHeading()` | `this` | Render as section heading |
| `setClass(cls: string)` | `this` | Add CSS class |
| `setDisabled(disabled: boolean)` | `this` | Disable entire row |
| `setTooltip(tooltip: string, options?: TooltipOptions)` | `this` | Row tooltip |
| `addText(cb)` | `this` | Text input (TextComponent) |
| `addTextArea(cb)` | `this` | Multi-line text (TextAreaComponent) |
| `addToggle(cb)` | `this` | Boolean toggle (ToggleComponent) |
| `addSlider(cb)` | `this` | Numeric slider (SliderComponent) |
| `addDropdown(cb)` | `this` | Dropdown (DropdownComponent) |
| `addColorPicker(cb)` | `this` | Color picker (ColorComponent) |
| `addButton(cb)` | `this` | Action button (ButtonComponent) |
| `addMomentFormat(cb)` | `this` | Date format input (MomentFormatComponent) |
| `addSearch(cb)` | `this` | Search input (SearchComponent) |
| `addProgressBar(cb)` | `this` | Progress bar (ProgressBarComponent) |
| `addExtraButton(cb)` | `this` | Icon button (ExtraButtonComponent) |
| `addComponent(cb)` | `this` | Custom component (1.11.0+) |
| `clear()` | `this` | Remove all contents |
| `then(cb)` | `this` | Facilitates chaining |
