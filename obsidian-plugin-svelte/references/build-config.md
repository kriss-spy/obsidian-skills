# Svelte Build Configuration Reference

## Required packages

```bash
npm install --save-dev svelte svelte-preprocess esbuild-svelte svelte-check
```

## tsconfig additions

- `verbatimModuleSyntax: true`
- `skipLibCheck: true`
- `"**/*.svelte"` in `include`

## esbuild plugin setup

```js
import esbuildSvelte from 'esbuild-svelte';
import { sveltePreprocess } from 'svelte-preprocess';

plugins: [
  esbuildSvelte({
    compilerOptions: { css: 'injected' },
    preprocess: sveltePreprocess(),
  }),
]
```

## package.json script

```json
"svelte-check": "svelte-check --tsconfig tsconfig.json"
```

## CSS handling

`css: 'injected'` bundles component styles into JS. Obsidian loads them automatically. Do not emit a separate CSS file unless you copy it manually into the plugin folder.
