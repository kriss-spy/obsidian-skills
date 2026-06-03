# obsidian-plugin-svelte

OpenCode skill for integrating Svelte into Obsidian plugins.

## What it covers

- Build configuration (`esbuild` + `esbuild-svelte` + `svelte-preprocess`)
- TypeScript setup for `.svelte` files
- Mounting Svelte components in `ItemView`, `Modal`, and `PluginSettingTab`
- Bridging Obsidian plugin state into Svelte props and stores
- Lifecycle cleanup (`unmount` / `$destroy`) to prevent memory leaks
- Svelte 5 runes (`$props`, `$state`) and legacy Svelte 4 patterns

## Usage

This skill is automatically loaded by OpenCode when triggered by Svelte-related prompts in an Obsidian plugin context.

## Files

- `SKILL.md` — Full skill instructions and code patterns
- `references/` — Thin reference docs for related tools and APIs

## References

- [Official Obsidian Svelte Guide](https://docs.obsidian.md/Plugins/Getting+started/Use+Svelte+in+your+plugin)
- [Svelte Documentation](https://svelte.dev/docs/svelte/overview)
- [esbuild-svelte](https://github.com/EMH333/esbuild-svelte)
- [svelte-preprocess](https://github.com/sveltejs/svelte-preprocess)
