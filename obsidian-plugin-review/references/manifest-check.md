# Manifest Check

A focused, line-by-line validator for `manifest.json` that mirrors the submission requirements the reviewer enforces. Run as part of `review.sh` and also useful on its own during plugin development.

## What it checks

### Required fields

| Field | Rule |
|---|---|
| `id` | string, non-empty, no whitespace, ≤ 100 chars, must not contain `obsidian` (case-insensitive) as a prefix word |
| `name` | string, non-empty, ≤ 100 chars |
| `version` | string, exactly `^\d+\.\d+\.\d+$` (no `v` prefix, no pre-release tags) |
| `minAppVersion` | string, exactly `^\d+\.\d+\.\d+$` |
| `description` | string, ≤ 250 chars, **starts with a capital letter** (or digit if a number — the reviewer doesn't flag those), **ends with `.`, `!`, or `?`**, no emoji (the reviewer is strict on this) |
| `author` | string, non-empty |

### Optional fields

| Field | Rule |
|---|---|
| `authorUrl` | if present, must be a valid `http(s)://` URL |
| `isDesktopOnly` | if present, must be boolean |
| `fundingUrl` | if present, must be a valid `http(s)://` URL. Only allowed if the plugin actually accepts financial support (the reviewer trusts what you put in the dashboard) |
| `icon` | if present, must be a string path relative to the plugin root, and the file must exist |
| `minAppVersion` (consistency) | must be ≥ the `obsidian` package's `minAppVersion` if `obsidian` is installed locally |

### Field-level failures

Each failure is reported as a `Source code` finding with message `<field>: <reason>` and rule `obsidianmd/validate-manifest`. If multiple fields fail, you get one bullet per field, not one bullet per issue.

### `versions.json` consistency

`manifest.json#version` must have a matching key in `versions.json`, mapped to a `minAppVersion` value. The check is permissive: it warns on missing key, not errors. Rationale: the reviewer doesn't run a versions.json check at all, but the local script surfaces it because it's a common submission blocker the user can fix.

## Implementation

`scripts/lib/manifest-check.sh` reads `manifest.json` with `jq` and applies the rules above. No external dependencies beyond `jq` (which is a hard dependency of the whole skill).

## Common findings and fixes

| Finding | Fix |
|---|---|
| `id: must not contain "obsidian"` | Rename your plugin id. The reviewer reserves the `obsidian-` prefix for official plugins. |
| `version: must match x.y.z` | Strip the `v` prefix and any `-beta.N` tag for the released version. (Pre-release tags are fine for the manifest, but the reviewer wants `x.y.z` exactly on a published release.) |
| `description: must start with a capital letter` | Capitalise the first word. |
| `description: must end with .` | Add a period. |
| `description: contains emoji` | Strip the emoji. The reviewer scans the description field, not the code. |
| `description: too long` | Trim to ≤ 250 chars. |
| `isDesktopOnly: not a boolean` | Use `true`/`false` (not `"true"`). |
| `fundingUrl: present but no external payment mechanism` | Remove `fundingUrl` unless the plugin has a real funding link. |
