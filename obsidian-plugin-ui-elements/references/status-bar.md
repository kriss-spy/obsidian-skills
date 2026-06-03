# Status Bar

Source: https://docs.obsidian.md/Plugins/User+interface/Status+bar

To create a new block in the status bar, call the `addStatusBarItem()` in the `onload()` method. The `addStatusBarItem()` method returns an HTML element that you can add your own elements to.

> [!caution] Obsidian mobile
> Custom status bar items are **not** supported on Obsidian mobile apps.

## Example

```ts
import { Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    const item = this.addStatusBarItem();
    item.createEl('span', { text: 'Hello from the status bar 👋' });
  }
}
```

> [!note]
> For more information on how to use the `createEl()` method, refer to [[HTML elements]].

## Grouping elements

You can add multiple status bar items by calling `addStatusBarItem()` multiple times. Since Obsidian by default adds a gap between each status bar item, you will have to group multiple HTML elements into one status bar item, if you want to have more control over spacing.

```ts
import { Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    const fruits = this.addStatusBarItem();
    fruits.createEl('span', { text: '🍎' });
    fruits.createEl('span', { text: '🍌' });

    const veggies = this.addStatusBarItem();
    veggies.createEl('span', { text: '🥦' });
    veggies.createEl('span', { text: '🥬' });
  }
}
```
