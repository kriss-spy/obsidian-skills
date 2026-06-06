---
name: obsidian-plugin-review
description: Run the local equivalent of the automated review on an Obsidian plugin. Reproduces the reviewer output format (Releases / Behavior / Source code) using eslint-plugin-obsidianmd plus a custom capability scan and a manifest/release check. Use before tagging a release, after a refactor, or whenever you want to catch the issues the dashboard would flag without submitting a release.
triggers:
  - obsidian plugin review
  - obsidian plugin automated review
  - obsidian plugin lint
  - obsidian plugin scorecard
  - obsidian plugin preflight
  - obsidian plugin dashboard
  - obsidian plugin eslint
author: OpenCode
version: 1.0.0
created: 2026-06-06
---

# Obsidian Plugin Review

This skill runs the **local equivalent of the automated review** on an Obsidian plugin. The output is in the same three-section format the developer dashboard shows, so you can catch issues before submitting a release.

The skill is a **faithful mirror** of the public parts of the reviewer: it uses the official `eslint-plugin-obsidianmd` and `@typescript-eslint` rulesets, plus a custom static-analysis scan for the `## Behavior` capabilities (`fs`, `child_process`, clipboard, Vault API), plus a check for GitHub artifact attestations on the latest release. A small set of `## Releases` / `## Source code` rules are local-only (see `references/rule-catalog.md` for the full list and provenance).

## When to use

- Before tagging a release, to catch issues that would fail the dashboard review.
- After a refactor, to confirm no new findings slipped in.
- When triaging findings from the dashboard log (paste a `.log` next to a local report and `diff`).
- When a plugin author wants a "what would the reviewer say?" preview without submitting.

## When **not** to use

- For runtime behaviour tests — use the plugin's own test suite (e.g. `vitest`).
- For TypeScript compilation errors — use `tsc --noEmit`.
- For the actual submission — use the developer dashboard at <https://community.obsidian.md/>.

## Quick start

```sh
# From a plugin's repo root:
<skill-dir>/scripts/review.sh
```

That runs all four sub-checks (eslint, behavior scan, manifest check, release attestation check) and writes a report to `./obsidian-plugin-review-reports/review-<timestamp>.md`. Exit code is `1` on any `Error` finding, `0` otherwise. Override with `--fail-on=warning|recommendation|never`.

Diff a local report against a dashboard log:

```sh
diff -u dashboard.log obsidian-plugin-review-reports/review-<ts>.md
```

The local script targets the same output format (see `references/review-output-format.md`), so an empty diff means a clean run.

## What the report looks like

The report is three sections in this order: `## Releases`, `## Behavior`, `## Source code`. The format is documented in `references/review-output-format.md` and reverse-engineered from real dashboard output.

```markdown
## Releases

- **Recommendation**: Missing GitHub artifact attestations for release assets
  - main.js
  - styles.css
  - Artifact attestations let users cryptographically verify the provenance of the release assets, proving they were built from the source repository. https://...

## Behavior

- **Warning**: **Direct Filesystem Access**: Uses the Node.js `fs` module to access the filesystem outside of the Obsidian vault API. ...
- **Warning**: **Shell Execution**: Executes shell commands via `child_process`. ...
- **Recommendation**: **Clipboard Access**: Reads or writes the system clipboard. ...
- **Pass**: **Vault Write**: Creates or modifies vault files via the Obsidian API (`vault.modify`, `vault.create`, etc.)

## Source code

- **Error**: Don't detach leaves in onunload, as that will reset the leaf to ...
  - obsidianmd/detach-leaves
  - src/main.ts:109-112
- **Warning**: Use 'window.setTimeout()' instead of 'setTimeout()' for popout window compatibility.
  - obsidianmd/prefer-window-timers
  - src/modules/ptySession.ts:113, src/modules/terminalKeyRouter.ts:105, ...
```

A `**Pass**` in the Behavior section is a positive report — the plugin uses the safe API. A `**Recommendation**` is informational. `**Warning**` doesn't fail the review on its own (the dashboard shows it as a yellow flag). `**Error**` fails the review.

## Output location

By default, reports land in `./obsidian-plugin-review-reports/`. Override with `--report-dir <path>`. Each run gets a unique timestamped filename so reports are append-only.

## Sub-checks and what they do

The script is a thin orchestrator over four independent checks. Each is a small script in `scripts/lib/` that emits tab-separated findings to stdout; the orchestrator tags them with a section name and `report.sh` aggregates into markdown.

| Sub-check | Script | What it does |
|---|---|---|
| Source code (eslint) | `eslint-runner.sh` | Runs `eslint` with the bundled flat config that extends `obsidianmd.configs.recommended` and `@typescript-eslint` recommended-type-checked. Emits one TSV row per finding. |
| Source code (manifest) | `manifest-check.sh` | Validates `manifest.json` against the submission requirements (id, name, version, minAppVersion, description, author, fundingUrl, isDesktopOnly, etc.). |
| Behavior | `behavior-scan.sh` | Greps the source tree for `fs` / `child_process` imports and clipboard / vault-API call-sites. Emits one row per detected capability. |
| Releases | `release-check.sh` | Calls the GitHub Releases API and looks for `.attestation` companion files on the version's release assets. |

Each sub-check is independently runnable — see their `--help` (or read the header comment) for details. The orchestrator's job is just to wire them up, count severities, and emit a report.

## Prerequisites

The orchestrator script depends on:

- `bash`, `find`, `grep`, `jq`, `python3` — standard on most Linux/macOS.
- `node` 18+ and the bundled npm dependencies in `scripts/lib/node_modules/` (run `cd scripts/lib && npm install` once after cloning).
- For the release check, either the `gh` CLI authenticated against your repo, or unauthenticated `curl` (60 req/h rate limit).

The skill's own `scripts/lib/` ships with a `package.json` pinning:

- `eslint@^9`
- `eslint-plugin-obsidianmd@^0.3.0`
- `@typescript-eslint/parser@^8`
- `@typescript-eslint/eslint-plugin@^8`

These match the rule versions used in the official reviewer at the time this skill was built (May 2026). Bump them as Obsidian updates the dashboard.

## Severity model

See `references/severity-and-fail-thresholds.md` for the long version. Short version:

- `Error` → fails the review.
- `Warning` → doesn't fail; reports in the scorecard.
- `Recommendation` → informational; doesn't fail.
- `Pass` → positive; appears in the Behavior section.

By default the script exits non-zero on `Error`. Tighten with `--fail-on=warning` for CI on a plugin already in the directory.

## How to interpret findings

When the script reports a finding:

1. Look up the rule in `references/rule-catalog.md`. Every rule has its severity, message wording, and a one-line "how to fix" note.
2. For source-code findings, the rule id is on the line below the message (e.g. `obsidianmd/detach-leaves`).
3. For Behavior findings, the capability name is **double-bolded** (`**Direct Filesystem Access**`). A Warning is a strong signal to the dashboard that the plugin can do dangerous things; a Pass is the opposite.
4. For Releases findings, the missing asset is a sub-bullet.

The catalog is the canonical reference for "why is this flagged?" and "how do I fix it?".

## Limitations vs the real reviewer

The dashboard's reviewer has some checks we cannot fully reproduce locally:

- **Malware / vulnerability scanning** — the dashboard's signature set isn't public. We don't try to replicate this; the local script has a stub.
- **Scorecard scoring rubric** — the dashboard's exact weight per category isn't public. We emit findings at Error/Warning/Recommendation/Pass severities; the dashboard decides how that maps to a numeric score.
- **Disclosures, privacy labels, verified author** — the blog post says these are "coming in the coming months". Until Obsidian publishes the schemas, the local script is silent on them.
- **Private / closed-source plugins** — the dashboard no longer accepts new closed-source submissions. The local script only inspects what's in the repo, so it works the same either way.

The `## Source code` section is the most faithful part — it uses the same linter the dashboard uses, with severity overrides tuned to match real review output. The `## Behavior` and `## Releases` sections are best-effort reproductions based on reverse-engineering.

## Custom rules

The skill is a starting point. To add a custom rule:

1. Add the rule to `.eslintrc.obsidian-review.cjs` (under `rules: { ... }` in the second config block).
2. Add a row to `references/rule-catalog.md`.
3. If the rule is reviewer-mapped (i.e. the dashboard also flags this), mark it as such in the catalog.
4. Re-run `scripts/review.sh` to verify.

To add a custom capability (Behavior section), see `references/capability-detection.md` — there's a clear extension point.

## References

- `references/rule-catalog.md` — full rule index with severities, messages, and fixes.
- `references/review-output-format.md` — exact format of the three sections.
- `references/severity-and-fail-thresholds.md` — what each severity means and what makes a build fail.
- `references/capability-detection.md` — how the Behavior section detects capabilities, with extension points.
- `references/manifest-check.md` — manifest field rules and fixes.
- `references/release-check.md` — GitHub artifact attestations and how to add them to your release workflow.
- [obsidianmd/eslint-plugin](https://github.com/obsidianmd/eslint-plugin) — the upstream linter.
- [The future of Obsidian plugins](https://obsidian.md/blog/future-of-plugins/) — blog post announcing the automated review.
- [Plugin submission requirements](https://docs.obsidian.md/Plugins/Releasing/Submission+requirements+for+plugins) — what the reviewer enforces.
