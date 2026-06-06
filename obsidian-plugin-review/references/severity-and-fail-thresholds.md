# Severity and Fail Thresholds

A reference for what the reviewer's severities mean in practice, and what makes a build **fail** the review.

## The five severities

| Tag | Order | Fail review? | Reports on dashboard as |
|---|---|---|---|
| `Error` | 1 (worst) | **Yes** | Red failure flag |
| `Warning` | 2 | No (yellow) | Yellow flag |
| `Recommendation` | 3 | No (grey) | Grey / informational flag |
| `Pass` | 4 (best) | No | Positive green check |
| `Info` | (reserved) | No | (future) |

The order is the only thing that's truly fixed: `Error > Warning > Recommendation > Pass`. The "fail review?" column is **inferred from the blog + community behaviour**:

> All new plugins and themes must pass automated review before they are added to the directory and available via search. Each new version is scanned, and if it fails to pass review, the plugin is removed from search within 24 hours.

What counts as "fails to pass" is not public. Empirically, in the scan logs, `Error` items are the only ones that look like they would block submission — `Warning` items are present in passing plugins and are described in the blog as "warnings" that don't block.

The local script defaults to:

- `Error` count > 0 → exit 1
- `Warning` count > 0 → exit 0, print warning summary
- `Recommendation` count > 0 → exit 0, print recommendation summary
- `Pass` lines don't affect exit code

Override with `REVIEW_FAIL_ON=warning` (or `recommendation`) to make the gate stricter — useful for CI on a plugin that's already in the directory and you don't want to regress.

## What constitutes an `Error`?

From the rule catalog, the following are `Error` in real review output:

- `obsidianmd/detach-leaves`
- `obsidianmd/no-unsupported-api`
- `obsidianmd/no-static-styles-assignment`
- `obsidianmd/settings-tab/no-manual-html-headings`
- `obsidianmd/settings-tab/no-problematic-settings-headings`
- `obsidianmd/validate-manifest`
- `obsidianmd/no-forbidden-elements`
- `obsidianmd/no-view-references-in-plugin`
- `obsidianmd/no-plugin-as-component`
- `obsidianmd/no-nodejs-modules`
- `obsidianmd/regex-lookbehind`
- `@typescript-eslint/ban-ts-comment` (treated as Error by the reviewer even though upstream default is Warning)

If your plugin has any of these, the build will not pass review.

## What is a `Warning`?

Almost everything else from `obsidianmd/*` and the bulk of `@typescript-eslint/*`:

- All `commands/*` rules
- `prefer-window-timers`, `prefer-active-doc`, `hardcoded-config-path`
- `no-sample-code`, `no-tfile-tfolder-cast`, `object-assign`, `platform`
- `prefer-abstract-input-suggest`, `prefer-file-manager-trash-file`
- `ui/sentence-case`, `vault/iterate`
- `@typescript-eslint/no-unsafe-*`, `no-explicit-any`, `no-unused-vars`, `no-floating-promises`, `no-misused-promises`, `no-throw-literal`, `no-require-imports`, `no-alert`, `no-unnecessary-type-assertion`

These don't block submission but accumulate in the dashboard scorecard and may invite manual review for popular/featured plugins.

## What is a `Recommendation`?

- `Clipboard Access` capability (Behavior section)
- `Missing GitHub artifact attestations` (Releases section)
- Anything the reviewer wants to surface without penalising

## What is a `Pass`?

- `Vault Write` capability, when the plugin uses the safe API

## Mapping to the scorecard

The dashboard scorecard displays findings under these categories (per the blog):

> These scorecards will continue to improve as we incorporate disclosures, privacy labels, artifact attestation, manual review results, and adoption of app capabilities.

So the scorecard has rows for:

- **Code quality** — the `## Source code` section
- **Security** — the `## Behavior` section's `Warning` rows
- **Release hygiene** — the `## Releases` section

`Pass` items in Behavior contribute to a positive "adoption of app capabilities" row (a plugin that uses `vault.modify` instead of `fs.writeFile` gets a green check on that row).

## Local script behaviour

`scripts/review.sh` exits non-zero only on `Error`. It prints a one-line summary to stdout and writes the full report to `reports/<timestamp>.md`. The agent then reads the report and decides what to fix.

To preview without failing:

```sh
REVIEW_FAIL_ON=never scripts/review.sh
```

To make the gate stricter:

```sh
REVIEW_FAIL_ON=warning scripts/review.sh
REVIEW_FAIL_ON=recommendation scripts/review.sh
```
