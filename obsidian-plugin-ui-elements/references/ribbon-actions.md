# Ribbon Actions

Source: https://docs.obsidian.md/Plugins/User+interface/Ribbon+actions

The sidebar on the left side of the Obsidian interface is mainly known as the _ribbon_. The purpose of the ribbon is to host actions defined by plugins.

To add an action to the ribbon, use the `addRibbonIcon()` method.

## Example

```ts
import { Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    this.addRibbonIcon('dice', 'Print to console', () => {
      console.log('Hello, you!');
    });
  }
}
```

The first argument specifies which icon to use. For more information on the available icons, and how to add your own, refer to [[Icons]].

> [!note]
> Users can remove your plugin's icon from the ribbon, or even opt to hide the ribbon entirely. Therefore it's advisable to include alternate ways of accessing functionality that's in the ribbon, such as creating a [[Commands|command]]. It is also recommended that plugins do not add their own toggles for ribbon items.
