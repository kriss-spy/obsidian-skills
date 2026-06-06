# Capability Detection (the `## Behavior` section)

The reviewer statically analyses the plugin's compiled or source JavaScript/TypeScript and reports on **what capabilities the plugin uses** — regardless of whether the usage is well-guarded or not. The output goes under `## Behavior` (see `review-output-format.md`).

This document describes exactly how the local script detects each capability, so the output is reproducible and you can add your own.

## Detection strategy

The local script uses a simple text/AST-light grep on `main.js` and every file under `src/`. For each capability, the detection pattern is a set of regexes; a single match anywhere in scope is enough to fire the finding.

Patterns are intentionally **lax**: we'd rather over-report than miss a real capability. The reviewer has the same posture — `fs` imported but not used still produces a `Direct Filesystem Access` warning.

## Direct Filesystem Access

**Severity**: `Warning`
**Message**: `Uses the Node.js fs module to access the filesystem outside of the Obsidian vault API. Can read and write any file on the system.`

Detection patterns (any one matches):

- `from ['"]fs['"]`
- `from ['"]node:fs['"]`
- `require\(['"]fs['"]\)`
- `require\(['"]node:fs['"]\)`

## Shell Execution

**Severity**: `Warning`
**Message**: `Executes shell commands via child_process. Gives the plugin full control over the system.`

Detection patterns:

- `from ['"]child_process['"]`
- `from ['"]node:child_process['"]`
- `require\(['"]child_process['"]\)`
- `require\(['"]node:child_process['"]\)`

## Clipboard Access

**Severity**: `Recommendation`
**Message**: `Reads or writes the system clipboard. May expose content copied from outside Obsidian.`

Detection patterns:

- `navigator\.clipboard`
- `electron\.clipboard`
- `\.readText\(\)` (matches `navigator.clipboard.readText()` and `electron.clipboard.readText()`)
- `\.writeText\(` (matches both `navigator.clipboard.writeText()` and `electron.clipboard.writeText()`)
- `require\(['"]electron['"]\)` followed within 5 lines by `clipboard` (covers `const { clipboard } = require("electron")`)

Note: the Obsidian API also exposes a `clipboardManager` for read access from the clipboard history command palette; calls to `app.clipboardManager.readText()` would also be flagged by the `\.readText\(\)` pattern.

## Vault Write

**Severity**: `Pass`
**Message**: `Creates or modifies vault files via the Obsidian API (vault.modify, vault.create, etc.)`

Detection patterns (any one matches):

- `\.vault\.create\(`
- `\.vault\.modify\(`
- `\.vault\.delete\(`
- `\.vault\.trash\(`
- `\.vault\.rename\(`
- `\.vault\.append\(`
- `\.fileManager\.trashFile\(`
- `\.fileManager\.createNewFile\(`
- `\.fileManager\.renameFile\(`
- `\.fileManager\.processFrontMatter\(`

If none match, no `Vault Write` line is printed. (The reviewer is silent on a missing safe capability; absence of a Pass bullet is not a problem.)

## Implementation

The patterns live in `scripts/lib/behavior-scan.sh`. Each capability is a function that takes a file path, runs its regexes, and prints a `Found: <capability>` line on stdout if matched. The orchestrator deduplicates per plugin run.

## Extending

To add a new capability:

1. Pick a severity (Warning for risky, Recommendation for opt-in, Pass for safe).
2. Add the patterns to the matching function in `behavior-scan.sh`.
3. Update `rule-catalog.md` § "Behavioural capabilities" with the new row.
4. Update `review-output-format.md` if the message format differs.

The reviewer is known to be growing in this area (the dashboard screenshot in the blog shows four `Direct Filesystem Access` / `Shell Execution` / `Clipboard Access` / `Vault Write` rows, but the scorecard spec mentions "disclosures" and "app capabilities" coming soon). New capabilities will likely land under the same `## Behavior` section.
