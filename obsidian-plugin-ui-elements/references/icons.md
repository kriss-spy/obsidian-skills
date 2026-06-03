# Icons

Source: https://docs.obsidian.md/Plugins/User+interface/Icons

Several of the UI components in the Obsidian API let you configure an accompanying icon. You can choose from one of the built-in icons, or you can add your own.

## Browse available icons

Browse to [lucide.dev](https://lucide.dev) to see all available icons and their corresponding names.

> **Please note:** Only icons up to v0.446.0 are supported at this time.

## Use icons

If you'd like to use icons in your custom interfaces, use the `setIcon()` utility function to add an icon to an HTML element.

```ts
import { Plugin, setIcon } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    const item = this.addStatusBarItem();
    setIcon(item, 'info');
  }
}
```

To change the size of an icon, set the `--icon-size` CSS variable on the element containing the icon using preset sizes:

```css
div {
  --icon-size: var(--icon-size-m);
}
```

## Add your own icon

To add a custom icon for your plugin, use the `addIcon()` utility:

```ts
import { addIcon, Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    addIcon('circle', `<svg>...</svg>`);
    this.addRibbonIcon('circle', 'Click me', () => {
      console.log('Hello, you!');
    });
  }
}
```

`addIcon` takes two arguments:

1. A name to uniquely identify your icon.
2. The SVG content for the icon, without the surrounding `<svg>` tag.

Note that your icon needs to fit within a `0 0 100 100` view box to be drawn properly.

After the call to `addIcon`, you can use the icon just like any of the built-in icons.

### Icon design guidelines

For compatibility and cohesiveness with the Obsidian interface, your icons should follow Lucide's guidelines:

- Icons must be designed on a 24 by 24 pixels canvas
- Icons must have at least 1 pixel padding within the canvas
- Icons must have a stroke width of 2 pixels
- Icons must use round joins
- Icons must use round caps
- Icons must use centered strokes
- Shapes (such as rectangles) in icons must have border radius of 2 pixels
- Distinct elements must have 2 pixels of spacing between each other
