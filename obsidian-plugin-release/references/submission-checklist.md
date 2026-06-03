# Submission Checklist Reference

## Required Repository Files

- `README.md`
- `LICENSE`
- `manifest.json`

## Required Release Assets

- `main.js`
- `manifest.json`
- `styles.css` (if applicable)

## `community-plugins.json` Entry

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "author": "Author Name",
  "description": "Action statement describing what the plugin does.",
  "repo": "username/repo-name"
}
```

## Common Review Items

- Resource cleanup (use `registerEvent`, `registerDomEvent`, `registerInterval`)
- Rename placeholder class names from sample plugin
- `isDesktopOnly: true` if using Node.js/Electron APIs
- Prefer Vault API over Adapter API
- Avoid `innerHTML`; use `createEl()` / `createDiv()` / `createSpan()`
- Use `normalizePath()` for all user-defined paths
- Use `workspace.getActiveViewOfType()` instead of `activeLeaf`
- Don't manage references to custom views; use `getActiveLeavesOfType()`
