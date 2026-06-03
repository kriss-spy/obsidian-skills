# Right-to-Left (RTL)

Source: https://docs.obsidian.md/Plugins/User+interface/Right-to-left

Obsidian supports right-to-left (RTL) languages such as Arabic, Dhivehi, Hebrew, Farsi, Syriac, and Urdu.

## Contexts

- **App interface** — defined by the language selected in Obsidian Settings. If the user selects an RTL language, the app interface is automatically reversed, and a `.mod-rtl` class is added to the `body` element. The specific interface language is added to the `lang` attribute on the `html` element.
- **Note content** — can be written in LTR, RTL, or mixed. Obsidian automatically detects the direction of the language in the editor and adds the `dir` attribute to each line.

## CSS helpers and rules for RTL

### Selectors for language direction

The `.mod-rtl` class is added to the `body` element when an RTL language is selected in Settings → General.

```css
.mod-rtl .plugin-class {
  direction: rtl;
}
```

#### Editor selectors

The `dir="rtl"` attribute is added to the `.markdown-source-view` element when the user chooses an RTL interface language or sets RTL as the default editor direction.

The `dir` attribute is set to `rtl` or `ltr` per line on `.cm-line` elements by detecting the first strongly directional character.

### Icons are mirrored automatically

Obsidian automatically reverses the direction of icons when the interface is in RTL mode. To prevent reversing a specific icon in RTL mode you must explicitly unset the transformation.

### Use the direction variable for horizontal calculations

The CSS variable `--direction` is available for calculations such as `translateX()`:

| Variable | LTR value | RTL value |
|----------|-----------|-----------|
| `--direction` | `1` | `-1` |

### Choose the best bidirectional handling for an element

The CSS `unicode-bidi` property can be used to determine how bidirectional content is treated. Using the `plaintext` value can be useful in certain cases. In the Obsidian UI the `plaintext` value is used whenever a single line of content is present that could be either LTR or RTL (file names, outline items, tooltips, status bar elements).
