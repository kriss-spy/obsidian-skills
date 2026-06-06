# Rule Catalog

A complete index of every rule the automated reviewer checks, grouped by source. For each rule: severity, message (as the reviewer prints it), what it catches, and how to fix it.

The severities are **Error**, **Warning**, **Recommendation**, and **Pass** — see `severity-and-fail-thresholds.md` for the order and what fails the build.

> **Source.** Severity and exact message wording are reverse-engineered from real review output in `scan-results/`. Rule ids are from the official `obsidianmd/eslint-plugin` and `@typescript-eslint` packages. Some Obsidian-specific rules from the reviewer output are not yet in the published `eslint-plugin-obsidianmd` and are marked **reviewer-local**.

---

## 1. `eslint-plugin-obsidianmd` — Obsidian API and UX rules

The published package. Repo: <https://github.com/obsidianmd/eslint-plugin>. Config name: `obsidianmd.configs.recommended`.

### `obsidianmd/detach-leaves` — Error
> Don't detach leaves in `onunload`, as that will reset the leaf to its default location when the plugin is loaded, even if the user has moved it to a different location.

Detaches a `WorkspaceLeaf` inside `onunload()`. Fix by removing the `detach()` call or moving it to a deliberate user-initiated action.

### `obsidianmd/no-unsupported-api` — Error
> Uses Obsidian APIs newer than the declared `minAppVersion`

Calls an API that the plugin's `manifest.json#minAppVersion` does not cover. Either bump `minAppVersion` or guard the call:

```ts
import { requireApiVersion } from "obsidian";
if (requireApiVersion("1.7.2")) { /* new API */ }
```

### `obsidianmd/no-static-styles-assignment` — Error
> Sets styles directly instead of using CSS classes or `setCssProps`

`el.style.X = ...` on an HTMLElement. Fix by adding a CSS class to `styles.css` and toggling it, or by using `setCssProps({ ... })`.

### `obsidianmd/settings-tab/no-manual-html-headings` — Error
> For a consistent UI use `new Setting(containerEl).setName(...).setHeading()` instead of creating HTML heading elements directly.

A settings tab is creating `<h1>..<h6>` directly. Replace with the `Setting` heading helper so theme CSS can style it.

### `obsidianmd/settings-tab/no-problematic-settings-headings` — Error
> Avoid using "settings" in settings headings.
> Avoid including the plugin name in settings headings.

A `Setting` heading starts with the word "settings" or repeats the plugin name (which is already shown in the tab title). Drop the redundant words.

### `obsidianmd/commands/no-plugin-id-in-command-id` — Warning
> The command ID should not include the plugin ID. Obsidian will make sure that there are no conflicts with other plugins.

`addCommand({ id: "my-plugin:do-thing", ... })` — drop the prefix, Obsidian namespaces commands for you.

### `obsidianmd/commands/no-plugin-name-in-command-name` — Warning
> The command name should not include the plugin name, the plugin name is already shown next to the command name in the UI.

`addCommand({ name: "My Plugin: do thing", ... })` — Obsidian appends the plugin name automatically.

### `obsidianmd/commands/no-default-hotkeys` — Warning
Discourage providing default hotkeys for commands — the same chord may collide with another plugin. Leave the second arg of `addCommand` as `() => null`.

### `obsidianmd/commands/no-command-in-command-id` / `commands/no-command-in-command-name` — Warning
`id`/`name` containing the literal word "command" is redundant in this context.

### `obsidianmd/prefer-window-timers` — Warning
> Use `'window.setTimeout()'` instead of `'setTimeout()'` for popout window compatibility.

Bare `setTimeout` / `setInterval` / `clearTimeout` / `clearInterval`. Prefix with `window.` so timers run in the correct window context when the user pops out a workspace pane.

### `obsidianmd/prefer-active-doc` — Warning
> Use `'activeDocument'` instead of `'document'` for popout window compatibility.

Bare `document.` access. Replace with `activeDocument.` so DOM queries target the right window.

### `obsidianmd/hardcoded-config-path` — Warning
> Obsidian's configuration folder is not necessarily `.obsidian`, it can be configured by the user. Use `Vault#configDir` to get the current value.

`".obsidian"` in a string literal. Use `(app.vault as Vault).configDir ?? ".obsidian"`.

### `obsidianmd/no-nodejs-modules` — Error (not in sample but in catalog)
Importing `fs`, `path`, `child_process`, `electron`, etc. without a `Platform.isDesktopApp` guard. See `obsidianmd/hardcoded-config-path` for the `.obsidian` variant.

### `obsidianmd/no-forbidden-elements` — Error
Attachment of forbidden elements (`<script>`, `<iframe>`, `<object>`, `<embed>`, etc.) to the DOM. These are blocked by Obsidian's CSP.

### `obsidianmd/no-plugin-as-component` — Error
> Disallow anti-patterns when passing a component to `MarkdownRenderer.render` to prevent memory leaks.

Passing the plugin instance as a `Component` to `MarkdownRenderer.render`. Use the view or the parent container's owner instead.

### `obsidianmd/no-sample-code` — Warning (auto-fixable)
Sample code from the obsidian-sample-plugin template that wasn't removed (e.g. placeholder imports, the demo `onClick` handler). The `obsidian-plugin-bootstrap` skill is the canonical check for this.

### `obsidianmd/no-tfile-tfolder-cast` — Warning
`as TFile` / `as TFolder` casts. Use `instanceof TFile` / `instanceof TFolder` checks.

### `obsidianmd/no-view-references-in-plugin` — Error
Storing direct references to a `View` instance on the plugin object — causes memory leaks. Use `app.workspace.getLeavesOfType()` instead.

### `obsidianmd/object-assign` — Warning
`Object.assign(a, b)` with two arguments — prefer spread: `{ ...a, ...b }`.

### `obsidianmd/platform` — Warning
Use of `navigator.userAgent` / `navigator.platform` to detect OS. Use `Platform.isMacOS` etc. from the `obsidian` module.

### `obsidianmd/prefer-abstract-input-suggest` — Warning
Hand-rolled `TextInputSuggest` — use `AbstractInputSuggest` from the Obsidian API.

### `obsidianmd/prefer-file-manager-trash-file` — Warning
`vault.trash(file)` / `vault.delete(file)` — prefer `fileManager.trashFile(file)` so the user's "System trash" / "Default trash" config is respected.

### `obsidianmd/regex-lookbehind` — Error
Regex using `(?<=...)` lookbehind. iOS versions older than 16.4 do not support it. Use capture groups and `String.match(...)` instead.

### `obsidianmd/editor-drop-paste` — Warning
Editor drop/paste event handler must check `evt.defaultPrevented` and call `evt.preventDefault()` to integrate with Obsidian's editor.

### `obsidianmd/ui/sentence-case` — Warning (in `recommended` config)
A UI string starts with a capitalised word. e.g. `"Open Settings"` → `"Open settings"`. CamelCase is allowed by default; set `enforceCamelCaseLower: true` to tighten.

### `obsidianmd/vault/iterate` — Warning (auto-fixable)
`vault.getMarkdownFiles()` then filtering by path. Use `vault.getAbstractFileByPath(path)` for a single file.

### `obsidianmd/validate-manifest` — Error
`manifest.json` missing required fields, wrong types, or invalid `id`/`minAppVersion` format. Detailed checks:

- `id` present, string, not empty, no spaces, ≤ 100 chars
- `name` present, ≤ 100 chars
- `version` present, matches `^\d+\.\d+\.\d+$`
- `minAppVersion` present, matches `^\d+\.\d+\.\d+$`
- `description` present, ≤ 250 chars, starts with a capital letter, ends with a period
- `author` present
- `isDesktopOnly` boolean (if present)
- `fundingUrl` is a valid URL (if present) — only allowed if you accept financial support

### `obsidianmd/validate-license` — Warning
`LICENSE` is missing, named oddly, or doesn't contain a recognised copyright header for the declared year.

### `obsidianmd/rule-custom-message` — Warning
Internal helper, not a check. Don't enable directly.

---

## 2. `@typescript-eslint` — TypeScript safety rules

The reviewer runs the `@typescript-eslint/recommended` ruleset in addition to the Obsidian ones. Names below are the upstream rule ids; the messages are the reviewer's wording (slightly trimmed for brevity).

### `@typescript-eslint/no-unsafe-assignment` — Warning
> Unsafe assignment of an `any` value.

`const x: Foo = someAny;` — type the source or add an explicit cast you can defend.

### `@typescript-eslint/no-unsafe-member-access` — Warning
> Unsafe member access `.X` on an `any` value.

`(x as any).foo` or chaining through an `any`. Type the chain.

### `@typescript-eslint/no-unsafe-call` — Warning
> Unsafe call of an `any` typed value.

Calling a function whose type was `any`. Type the function.

### `@typescript-eslint/no-unsafe-argument` — Warning
> Passes unsafe values into typed parameters

`f(someAny)` where `f` expects `T`. Type the argument.

### `@typescript-eslint/no-explicit-any` — Warning
> Unexpected any. Specify a different type.

Bare `: any` or `<any>` annotations. Use `unknown` and narrow, or a precise type.

### `@typescript-eslint/no-unused-vars` — Warning
> `'X'` is defined but never used.

Unused imports / locals. The reviewer configures it to allow leading-underscore names (e.g. `_event`).

### `@typescript-eslint/no-floating-promises` — Warning
> Promises must be awaited, end with a call to .catch, end with a call to .then with a rejection handler or be explicitly marked as ignored with the `void` operator.

A returned promise with no handler. Append `.catch(...)` or prefix with `void`.

### `@typescript-eslint/no-misused-promises` — Warning
> Promise returned in function argument where a void return was expected.

A `void`-returning callback (e.g. DOM event handler) is given a function that returns a promise without `await` / `void`. Wrap or `void` the call.

### `@typescript-eslint/no-throw-literal` — Warning
> Expected the Promise rejection reason to be an Error.

`throw "oops"` / `throw { code: 1 }` — throw an `Error`.

### `@typescript-eslint/no-require-imports` — Warning
> A `require()` style import is forbidden.

`const x = require("y")` — use `import` statements.

### `@typescript-eslint/no-alert` — Warning
> Unexpected confirm.

`confirm()` / `alert()` in a plugin UI. Use a `Modal` instead.

### `@typescript-eslint/no-unnecessary-type-assertion` — Warning
> This assertion is unnecessary since it does not change the type of the expression.

`"foo" as string` where TS already infers `string`. Drop the cast.

### `@typescript-eslint/ban-ts-comment` — Error
> Unexpected undescribed directive comment. Include descriptions to explain why the comment is necessary.

`// @ts-expect-error` or `// @ts-ignore` without a trailing description. The reviewer treats this as an Error, the upstream default is a Warning.

### `@typescript-eslint/no-empty-function` — Warning
Empty function bodies. (Not seen in samples, but part of the recommended set.)

### `@typescript-eslint/no-this-alias` — Warning
`const self = this;` — use arrow functions to capture `this`.

### `@typescript-eslint/prefer-as-const` — Warning
A literal that should be `as const`.

---

## 3. Reviewer-local rules (not in `eslint-plugin-obsidianmd`)

These appear in real review output but are **not** in the public package. We maintain them as custom rules in our local scan; see `scripts/lib/behavior-scan.sh` and the `local-rules` block in the eslint config.

### `reviewer-local/no-direct-html-write` — Warning
> Do not write to DOM directly using innerHTML/outerHTML property

`el.innerHTML = ...` or `el.outerHTML = ...`. Use `createEl` / `createDiv` from the Obsidian API, or `el.appendText(...)` for plain text. **XSS risk** is the underlying reason.

### Custom directive-comment enforcement — Error
Covered above by `@typescript-eslint/ban-ts-comment`.

### Behavioural capability detection
Static analysis of imports and call-sites — see `capability-detection.md`. Reported under the `## Behavior` section, not in source-code findings.

### Release artifact attestations
A release-time check (not source code). Reported under `## Releases`. See `release-check.md`.

---

## 4. Manifest requirements

Reviewed by `obsidianmd/validate-manifest` plus a few checks specific to the Obsidian submission process. The complete list is in `manifest-check.md` (mirrors the submission requirements doc).

| Field | Required | Rules |
|---|---|---|
| `id` | yes | unique, no spaces, no `obsidian` prefix, ≤ 100 chars |
| `name` | yes | ≤ 100 chars |
| `version` | yes | exact `x.y.z` semver |
| `minAppVersion` | yes | exact `x.y.z` |
| `description` | yes | ≤ 250 chars, starts with a capital, ends with a period, no emoji |
| `author` | yes | string |
| `authorUrl` | no | valid URL |
| `isDesktopOnly` | no | boolean |
| `fundingUrl` | no | valid URL; only if you accept financial support |

## 5. Release requirements

Reported under `## Releases`. See `release-check.md`.

- **Recommendation**: Missing GitHub artifact attestations for `main.js`, `manifest.json`, `styles.css`. The reviewer expects the workflow to call `actions/attest-build-provenance` for each asset. See <https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds>.

## 6. Behavioural capabilities

Reported under `## Behavior`. See `capability-detection.md`.

| Capability | Detection | Severity |
|---|---|---|
| **Direct Filesystem Access** | `import "fs"` / `import "node:fs"` / `require("fs")` anywhere in source | Warning |
| **Shell Execution** | `import "child_process"` / `require("child_process")` | Warning |
| **Clipboard Access** | `navigator.clipboard`, `electron.clipboard`, `obsidian`'s `clipboardManager` (when used to read), or any usage of `require("electron").clipboard` | Recommendation |
| **Vault Write** | `vault.create`, `vault.modify`, `vault.delete`, `vault.trash`, `vault.rename`, `vault.append`, `fileManager.trashFile`, `fileManager.createNewFile` | Pass |

A "Pass" entry is printed when the capability is detected, to tell reviewers the plugin *does* the safe thing. Plugins that never touch the vault simply don't get a `Vault Write` line.
