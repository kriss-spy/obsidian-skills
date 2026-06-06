# Review Output Format

The automated reviewer's output is **three sections in this exact order**: `## Releases`, `## Behavior`, `## Source code`. The local script reproduces this format so the output is directly comparable to the dashboard log.

## Top-level shape

```markdown
## Releases
- **<severity>**: <message>
  - <evidence>
  - <explanation link, optional>

## Behavior
- **<severity>**: **<Capability Name>**: <one-line description>

## Source code
- **<severity>**: <message>
  - <file:line list, comma-separated>
  - <rule id, optional, on its own line>
```

If a section has no findings, the reviewer still prints the section header but omits any items. The local script follows the same convention.

## Severity tags

The reviewer uses five severities. They appear in this exact bolded form:

| Tag | Meaning |
|---|---|
| `**Error**` | Must be fixed. Fails the review. |
| `**Warning**` | Should be fixed. Reported in the dashboard as a yellow flag. |
| `**Recommendation**` | Optional / informational. Reported as a grey flag. |
| `**Pass**` | Capability detected and used safely — printed so reviewers see the plugin *does* the safe thing. |
| `**Info**` | Not seen in samples, reserved for future use. |

A `Pass` is a positive report, not a finding. It appears in the Behavior section only, and is included whenever the plugin exercises the safe capability at all (e.g. uses the Vault API to write files).

## Releases section

Findings against the published GitHub release. Currently a single check:

```markdown
## Releases

- **Recommendation**: Missing GitHub artifact attestations for release assets
  - main.js
  - styles.css
  - Artifact attestations let users cryptographically verify the provenance of the release assets, proving they were built from the source repository. https://docs.github.com/...
```

The sub-bullets under a Release finding are **asset names** plus an **explanation line** (no rule id, no `file:line`).

If the workflow already attests its assets, this section is omitted entirely.

## Behavior section

One bullet per detected capability. The capability name is **double-bolded**. Sub-bullets are not used in this section — it's one line per capability.

```markdown
## Behavior

- **Warning**: **Direct Filesystem Access**: Uses the Node.js `fs` module to access the filesystem outside of the Obsidian vault API. Can read and write any file on the system.
- **Warning**: **Shell Execution**: Executes shell commands via `child_process`. Gives the plugin full control over the system.
- **Recommendation**: **Clipboard Access**: Reads or writes the system clipboard. May expose content copied from outside Obsidian.
- **Pass**: **Vault Write**: Creates or modifies vault files via the Obsidian API (`vault.modify`, `vault.create`, etc.)
```

Severities for capabilities:

- `Direct Filesystem Access` → `Warning`
- `Shell Execution` → `Warning`
- `Clipboard Access` → `Recommendation`
- `Vault Write` → `Pass`

A plugin that uses none of the above prints only `## Behavior` with no bullets.

## Source code section

One bullet per **unique rule message**. Locations are accumulated and printed as a comma-separated list of `file:line` (and `file:line-line` for ranges). When the rule id is shown, it appears on its own line, prefixed with the package scope (e.g. `obsidianmd/no-unsupported-api`) — never a URL.

```markdown
## Source code

- **Error**: Don't detach leaves in onunload, as that will reset the leaf to it's default location when the plugin is loaded, even if the user has moved it to a different location.
  - src/main.ts:109-112, src/main.ts:109-112
- **Error**: Uses Obsidian APIs newer than the declared `minAppVersion`
  - obsidianmd/no-unsupported-api
  - src/modules/viewCoordinator.ts:23, src/modules/viewCoordinator.ts:36, src/modules/viewCoordinator.ts:58, src/modules/viewCoordinator.ts:67, src/modules/viewCoordinator.ts:73
- **Warning**: Unsafe assignment of an `any` value.
  - src/editorServer.ts:64, src/editorServer.ts:68, src/main.ts:110, src/main.ts:148, src/modules/ptySession.ts:138, src/modules/terminalKeyRouter.ts:22, src/modules/terminalKeyRouter.ts:39, src/modules/terminalKeyRouter.ts:41, src/modules/terminalKeyRouter.ts:43, src/views/opencodeTerminalView.ts:177
- **Warning**: Obsidian's configuration folder is not necessarily `.obsidian`, it can be configured by the user. Use `Vault#configDir` to get the current value
  - src/modules/terminalKeyRouter.ts:40
```

Notes:

- The same message from multiple files is collapsed into one bullet; the `file:line` list can repeat the same line (the reviewer does this when the same issue appears in two adjacent places).
- The `file:line` list always uses **forward slashes** and is **relative to the plugin repo root** — not absolute paths.
- A finding without a location (e.g. a manifest validation error) lists just the message and the rule id, with no `file:line` line.
- The `obsidianmd/...` and `@typescript-eslint/...` rule id lines come **after** the message, **before** the locations. Order is: message, rule id (if any), locations.

## What the local script emits

The local `review.sh` reproduces the above. Its output is a single `.md` file at `obsidian-plugin-review/reports/<timestamp>.md` (or wherever the caller redirects). It also prints a one-line summary to stdout: `Errors: N  Warnings: N  Recommendations: N  Passes: N`.

To diff against a dashboard log, copy both into a directory and `diff -u dashboard.log reports/<ts>.md` — the diff should be empty when the local rule set covers every finding.
