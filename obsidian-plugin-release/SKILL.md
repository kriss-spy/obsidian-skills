---
name: obsidian-plugin-release
description: Release, version, and distribute Obsidian plugins. Covers manifest.json versioning, versions.json compatibility, GitHub Actions release workflows, submission requirements, BRAT beta testing, load-time optimization, secret storage, and mobile/desktop considerations. Use when preparing a plugin for release, automating releases, submitting to the community directory, or setting up beta channels.
triggers:
  - obsidian plugin release
  - obsidian plugin versioning
  - obsidian plugin github actions
  - obsidian plugin submit
  - obsidian plugin beta testing
  - obsidian plugin brat
  - obsidian plugin manifest
  - obsidian plugin versions.json
  - obsidian plugin optimize load time
  - obsidian plugin secrets
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Release

This skill guides you through releasing, versioning, and distributing an Obsidian plugin. It focuses on everything that happens after development: version management, automated builds, submission to the community directory, beta testing, and post-release best practices.

## When to Use This Skill

- Preparing a plugin for its first release
- Setting up automated GitHub Actions release workflows
- Updating `manifest.json` and `versions.json` correctly
- Submitting a plugin to the official Obsidian community directory
- Setting up BRAT beta testing for pre-release versions
- Optimizing plugin load time before release
- Storing API keys and tokens securely in a plugin
- Deciding whether a plugin should be desktop-only

## Overview

A released Obsidian plugin is distributed via GitHub Releases. The community plugin system pulls `main.js`, `manifest.json`, and optional `styles.css` directly from release assets. To publish:

1. Maintain correct versioning in `manifest.json`
2. Track Obsidian compatibility in `versions.json`
3. Build production artifacts
4. Create a GitHub release with the correct assets
5. Submit to `obsidian-releases` (for first release)

After initial approval, users update automatically from your GitHub releases.

---

## `manifest.json` Versioning

The manifest is Obsidian's source of truth for plugin identity and compatibility. The `version` field must follow Semantic Versioning in `x.y.z` format (e.g., `1.0.0`, `1.2.3`). Obsidian only supports the format `x.y.z`.

### Semantic Versioning Rules

| Bump | When to use |
|------|-------------|
| **MAJOR** (`x`) | Breaking changes that affect user data, settings format, or core behavior |
| **MINOR** (`y`) | New features, backwards-compatible enhancements |
| **PATCH** (`z`) | Bug fixes, backwards-compatible corrections |

### `minAppVersion`

Set `minAppVersion` to the minimum Obsidian app version required by your plugin. If you adopt a new API that requires a newer Obsidian version, bump `minAppVersion` and update `versions.json`.

> [!tip]
> If you don't know what an appropriate version number is, use the latest stable build number.

### Version Bump Script

Use a `version-bump.mjs` script to keep `manifest.json` and `versions.json` in sync with `package.json`:

```js
import { readFileSync, writeFileSync } from 'node:fs';

const targetVersion = process.env.npm_package_version;

// Update manifest.json
const manifest = JSON.parse(readFileSync('manifest.json', 'utf8'));
const { minAppVersion } = manifest;
manifest.version = targetVersion;
writeFileSync('manifest.json', JSON.stringify(manifest, null, '\t'));

// Update versions.json
const versions = JSON.parse(readFileSync('versions.json', 'utf8'));
versions[targetVersion] = minAppVersion;
writeFileSync('versions.json', JSON.stringify(versions, null, '\t'));

console.log(`Bumped to ${targetVersion} (minAppVersion: ${minAppVersion})`);
```

Wire it into `package.json`:

```json
{
  "scripts": {
    "version": "node version-bump.mjs && git add manifest.json versions.json"
  }
}
```

Now `npm version patch` bumps `package.json`, runs the script, and stages the files automatically.

---

## `versions.json` Compatibility Mapping

`versions.json` maps each plugin version to the minimum Obsidian app version required. Obsidian uses this to serve the latest compatible plugin version to users on older app versions.

### Format

```json
{
  "1.0.0": "0.15.0",
  "1.1.0": "0.16.0",
  "1.2.0": "0.16.0"
}
```

### Rules

- You **only** need to update `versions.json` when `minAppVersion` changes, not on every release.
- If a new plugin version uses the same `minAppVersion` as the previous one, the existing mapping is still valid.
- Keep versions in ascending or descending order for readability.

### Validation

Add a validation step to your CI to catch mismatches:

```bash
node -e "
  const manifest = require('./manifest.json');
  const versions = require('./versions.json');
  if (!versions[manifest.version]) {
    console.error('versions.json missing entry for', manifest.version);
    process.exit(1);
  }
  console.log('versions.json valid for', manifest.version);
"
```

---

## GitHub Actions Release Workflow

Manually creating releases is error-prone. Automate it with a workflow that triggers on tag push.

### Official Workflow

Create `.github/workflows/release.yml`:

```yml
name: Release Obsidian plugin

on:
  push:
    tags:
      - "*"

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3

      - name: Use Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18.x"

      - name: Build plugin
        run: |
          npm install
          npm run build

      - name: Create release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          tag="${GITHUB_REF#refs/tags/}"
          gh release create "$tag" \
            --title="$tag" \
            --draft \
            main.js manifest.json styles.css
```

### Setup Steps

1. Commit the workflow file and push it.
2. In GitHub repo settings → Actions → General → Workflow permissions, select **Read and write permissions**.
3. Create an annotated tag matching the version in `manifest.json`:

```bash
git tag -a 1.0.1 -m "1.0.1"
git push origin 1.0.1
```

4. The workflow runs, creates a **draft** release, and uploads `main.js`, `manifest.json`, and `styles.css`.
5. Edit the draft release, add release notes, and click **Publish release**.

> [!important]
> The release tag must match the version in `manifest.json`. Do not use a `v` prefix (use `1.0.1`, not `v1.0.1`).

### Enhanced Workflow (with validation)

```yml
name: Release Obsidian plugin

on:
  push:
    tags:
      - "*"

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "18"

      - name: Install and build
        run: |
          npm ci
          npm run build

      - name: Verify artifacts
        run: |
          test -f main.js || { echo "main.js missing"; exit 1; }
          test -f manifest.json || { echo "manifest.json missing"; exit 1; }

      - name: Validate manifest
        run: |
          node -e "
            const m = require('./manifest.json');
            const required = ['id','name','version','minAppVersion','description','author'];
            const missing = required.filter(f => !m[f]);
            if (missing.length) {
              console.error('Missing fields:', missing.join(', '));
              process.exit(1);
            }
            console.log('manifest.json valid:', m.id, 'v' + m.version);
          "

      - name: Create release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            main.js
            manifest.json
            styles.css
          draft: true
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Plugin Submission Requirements and Guidelines

Before submitting, make sure your repository has these files at the root:

| File | Required | Purpose |
|------|----------|---------|
| `README.md` | **Yes** | Describes the plugin purpose and how to use it |
| `LICENSE` | **Yes** | Determines how others can use the code |
| `manifest.json` | **Yes** | Plugin metadata |
| `main.js` | **Yes** | Compiled plugin (in release assets) |
| `styles.css` | No | Optional custom styles |

### Submission Steps

1. **Update `manifest.json`** to a semver version (e.g., `1.0.0`).
2. **Create a GitHub release** with a tag matching the `manifest.json` version.
3. **Upload release assets**: `main.js`, `manifest.json`, `styles.css` (if any).
4. **Fork** `obsidianmd/obsidian-releases`.
5. **Add an entry** to `community-plugins.json` in your fork:

```json
{
  "id": "my-unique-plugin",
  "name": "My Plugin",
  "author": "Your Name",
  "description": "Brief description of what this plugin does.",
  "repo": "yourusername/my-plugin"
}
```

6. **Open a pull request** to `obsidianmd/obsidian-releases`.
7. Wait for automatic validation (bot assigns `Ready for review` or `Validation failed`).
8. Wait for human review from the Obsidian team.

> [!warning]
> If you see a merge conflict warning, **ignore it**. The Obsidian team will resolve conflicts before publishing.

### Submission Requirements Checklist

- [ ] `README.md` exists and explains purpose and usage
- [ ] `LICENSE` file exists
- [ ] `manifest.json` is valid JSON with all required fields
- [ ] `version` follows semver (`x.y.z`)
- [ ] `minAppVersion` is appropriate
- [ ] Release tag matches `manifest.json` version exactly
- [ ] Release assets include `main.js` and `manifest.json`
- [ ] `id` is unique and does not contain `obsidian`
- [ ] `description` is ≤250 characters, starts with an action statement, ends with a period
- [ ] No emoji or special characters in `description`
- [ ] Correct capitalization for acronyms and trademarks (e.g., "Obsidian", "Markdown", "PDF")
- [ ] Sample code from the template has been removed
- [ ] `isDesktopOnly` is `true` if using Node.js or Electron APIs
- [ ] `fundingUrl` is only present if you accept financial support
- [ ] Command IDs do not include the plugin ID (Obsidian prefixes them automatically)
- [ ] All paths use `normalizePath()` from the Obsidian API

### Review Guidelines (Common Feedback)

- **Resource management**: Any resources created by the plugin must be destroyed when disabled. Prefer `registerEvent()`, `registerDomEvent()`, and `registerInterval()` so cleanup is automatic.
- **Class names**: Rename placeholder classes like `MyPlugin` and `SampleSettingTab` to reflect your actual plugin name.
- **Vault API**: Prefer `app.vault` over `app.vault.adapter` for file operations. It has caching and serializes operations to prevent race conditions.
- **Avoid `innerHTML`**: Build DOM with `createEl()`, `createDiv()`, and `createSpan()` to avoid XSS risks.
- **Workspace.activeLeaf**: Use `app.workspace.getActiveViewOfType(MarkdownView)` instead of direct `activeLeaf` access.
- **View references**: Don't store singleton view references in your plugin. Use `app.workspace.getActiveLeavesOfType()` to access views.

---

## BRAT Beta Testing Workflow

The **Beta Reviewers Auto-update Tool (BRAT)** lets users install pre-release versions of your plugin before they reach the community directory.

### How BRAT Works

- BRAT monitors your GitHub releases.
- It downloads `manifest.json`, `main.js`, and `styles.css` directly from release assets.
- It can install specific versions or always pull the latest (including pre-releases).

### Preparing a Beta Release

1. Create a GitHub release with a semantic version number (e.g., `1.1.0-beta.1`).
2. Optionally mark it as a **pre-release** in GitHub.
3. Include `manifest.json`, `main.js`, and `styles.css` in the release assets.
4. **Do NOT commit the new version to `manifest.json` on your default branch yet.** Obsidian's updater watches the default branch; if you commit a beta version there, regular users will be prompted to update.

> [!important]
> The release tag, release name, and the version inside the released `manifest.json` must all match. For example:
> - Release tag: `1.1.0-beta.1`
> - Release name: `1.1.0-beta.1`
> - Version in released `manifest.json`: `1.1.0-beta.1`

### BRAT Installation for Testers

Testers install BRAT from the community plugins, then add your repo path (e.g., `yourusername/my-plugin`). BRAT handles download and update automatically.

> [!tip]
> If you use `-preview` or other non-semver branches for beta versions, Obsidian may not pick up the final release automatically. Users may need to update via BRAT until you release a version at least a minor release higher than the beta.

---

## Optimizing Plugin Load Time

Plugins load before the user can interact with Obsidian. A slow `onload()` blocks startup.

### Keep `onload()` Lightweight

`onload()` should contain **only registration logic**:

```typescript
class MyPlugin extends Plugin {
  async onload() {
    // Register commands, views, settings, events
    this.addCommand({ ... });
    this.registerView(VIEW_TYPE, (leaf) => new MyView(leaf));
    this.addSettingTab(new MySettingTab(this.app, this));

    // Defer heavy work
    this.app.workspace.onLayoutReady(() => {
      this.initializeExpensiveFeature();
    });
  }
}
```

### Defer Views (Obsidian v1.7.2+)

As of v1.7.2, views start as `DeferredView` instances and only upgrade when the tab is selected. When iterating workspace leaves, always use `instanceof` checks:

```typescript
const leaves = this.app.workspace.getLeavesOfType('my-view');
for (const leaf of leaves) {
  if (requireApiVersion('1.7.2')) {
    await leaf.loadIfDeferred();
  }
  if (leaf.view instanceof MyCustomView) {
    // Safe to interact
  }
}
```

> [!warning]
> Calling `loadIfDeferred()` removes the lazy-loading optimization for that view. Use it sparingly.

### Lazy Initialization Pattern

Defer expensive setup until the user actually needs it:

```typescript
class LazyService<T> {
  private instance: T | null = null;
  private initializing: Promise<T> | null = null;

  constructor(private factory: () => Promise<T>) {}

  async get(): Promise<T> {
    if (this.instance) return this.instance;
    if (this.initializing) return this.initializing;
    this.initializing = this.factory().then((inst) => {
      this.instance = inst;
      this.initializing = null;
      return inst;
    });
    return this.initializing;
  }
}

// Usage in plugin
private indexService = new LazyService(() => this.buildIndex());

this.addCommand({
  id: 'search',
  name: 'Search',
  callback: async () => {
    const index = await this.indexService.get();
    // Use index...
  },
});
```

### Vault Event Handlers During Startup

Obsidian fires `vault.on('create')` for every file during vault initialization. Register handlers inside `onLayoutReady` to avoid reacting to thousands of startup events:

```typescript
this.app.workspace.onLayoutReady(() => {
  this.registerEvent(this.app.vault.on('create', this.onCreate, this));
});
```

### Build Optimization

- Minify `main.js` in production builds to reduce file size and disk read time.
- Omit inline source maps in production (`sourcemap: false` in esbuild).

---

## Storing Secrets Securely

Never hardcode API keys, tokens, or passwords in your plugin source. Use Obsidian's data API to let users store secrets in plugin settings.

### Pattern: Settings-Based Secret Storage

```typescript
export interface MyPluginSettings {
  apiKey: string;
  apiKeySaved: boolean;
}

export const DEFAULT_SETTINGS: MyPluginSettings = {
  apiKey: '',
  apiKeySaved: false,
};
```

In your settings tab, mask the input:

```typescript
new Setting(containerEl)
  .setName('API Key')
  .setDesc('Your API key is stored locally in data.json')
  .addText((text) => {
    text.inputEl.type = 'password';
    text.setPlaceholder('sk-...')
      .setValue(this.plugin.settings.apiKey)
      .onChange(async (value) => {
        this.plugin.settings.apiKey = value;
        this.plugin.settings.apiKeySaved = !!value;
        await this.plugin.saveSettings();
      });
  });
```

> [!caution]
> Secrets in `data.json` are stored in plain text in the plugin folder. This is acceptable for user-provided keys, but never bundle your own credentials. For higher security, guide users to set environment variables outside Obsidian and read them via Node.js only on desktop (`process.env.MY_KEY`).

---

## Mobile/Desktop-Only Considerations

### `isDesktopOnly` Flag

If your plugin uses Node.js or Electron APIs (`fs`, `path`, `child_process`, `electron`), set `isDesktopOnly: true` in `manifest.json`. Mobile users will not see it in the community plugin list, and Obsidian will refuse to load it on mobile.

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "isDesktopOnly": true
}
```

### Platform-Specific Guards

If your plugin is mostly cross-platform but has one desktop-only feature, keep `isDesktopOnly: false` and gate the feature:

```typescript
import { Platform } from 'obsidian';

if (Platform.isDesktopApp) {
  // Enable desktop-only feature
}

if (Platform.isMobile) {
  // Hide or disable unsupported functionality
}
```

### Mobile Alternatives for Common Node.js APIs

| Node.js API | Web API Alternative |
|-------------|---------------------|
| `crypto` | `SubtleCrypto` |
| `fs.readFile` | `app.vault.read(file)` |
| `fs.writeFile` | `app.vault.modify(file, data)` |
| `clipboard` | `navigator.clipboard.readText()` / `writeText()` |
| `path.join` | `normalizePath()` from Obsidian API |

---

## Patterns

### Release Checklist

Use this before every release:

- [ ] Version bumped in `manifest.json` (semver `x.y.z`)
- [ ] `versions.json` updated if `minAppVersion` changed
- [ ] `package.json` version synced
- [ ] `npm run build` succeeds with no errors
- [ ] `main.js` is minified and no source maps in production
- [ ] `styles.css` included if plugin has custom styles
- [ ] Sample code and placeholder names removed
- [ ] All paths use `normalizePath()`
- [ ] `isDesktopOnly` set correctly
- [ ] No hardcoded secrets or API keys
- [ ] `README.md` and `LICENSE` present and up to date
- [ ] Changelog updated
- [ ] Git tag matches `manifest.json` version exactly
- [ ] GitHub release drafted with correct assets
- [ ] Release notes written and published

### Changelog

Maintain a `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## Changelog

## [1.1.0] - 2026-06-03

### Added
- New command to export notes to PDF

### Fixed
- Settings not persisting on mobile

## [1.0.1] - 2026-05-20

### Fixed
- Crash when opening empty vault

## [1.0.0] - 2026-05-15

- Initial release
```

### Backwards Compatibility

- Avoid breaking changes to `data.json` (settings) structure. If you must change it, provide a migration path.
- When raising `minAppVersion`, ensure `versions.json` maps the new version so users on older Obsidian builds stay on a compatible plugin version.
- Deprecate commands or settings gracefully with console warnings before removing them.

---

## References

- [Release your plugin with GitHub Actions](https://docs.obsidian.md/Plugins/Releasing/Release+your+plugin+with+GitHub+Actions) — Official automated release guide
- [Submit your plugin](https://docs.obsidian.md/Plugins/Releasing/Submit+your+plugin) — Official submission workflow
- [Submission requirements for plugins](https://docs.obsidian.md/Plugins/Releasing/Submission+requirements+for+plugins) — Required checks before submitting
- [Plugin guidelines](https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines) — Common review comments and best practices
- [Beta-testing plugins](https://docs.obsidian.md/Plugins/Releasing/Beta-testing+plugins) — Official beta testing overview
- [BRAT Developer Guide](https://github.com/TfTHacker/obsidian42-brat/blob/main/BRAT-DEVELOPER-GUIDE.md) — Setting up BRAT for your plugin
- [Optimize plugin load time](https://docs.obsidian.md/Plugins/Guides/Optimize+plugin+load+time) — Reducing startup impact
- [Defer views](https://docs.obsidian.md/Plugins/Guides/Defer+views) — Working with lazy-loaded views (v1.7.2+)
- [Store secrets](https://docs.obsidian.md/Plugins/Guides/Store+secrets) — Securely handling API keys and tokens
- [Manifest reference](https://docs.obsidian.md/Reference/Manifest) — Complete `manifest.json` schema
- [Versions reference](https://docs.obsidian.md/Reference/Versions) — `versions.json` documentation
- [Plugin review guidelines](https://github.com/obsidianmd/obsidian-releases/blob/master/plugin-review.md) — Full review checklist from obsidian-releases
