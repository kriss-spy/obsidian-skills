# obsidian-plugin-review

Run the local equivalent of the [automated review](https://obsidian.md/blog/future-of-plugins/) on an Obsidian plugin, before tagging a release.

The local script reproduces the dashboard's three-section output format (`## Releases`, `## Behavior`, `## Source code`) using:

- `eslint-plugin-obsidianmd` (the same linter the reviewer uses) extended with `@typescript-eslint` recommended-type-checked
- a custom static-analysis scan for the Behavior capabilities (`fs`, `child_process`, clipboard, Vault API)
- a `manifest.json` field validator
- a GitHub artifact-attestations check for the latest release

## Install

```sh
npx skills add kriss-spy/obsidian-skills --skill obsidian-plugin-review
```

Then in the skill's `scripts/lib/` directory, install the npm dependencies once:

```sh
cd scripts/lib && npm install
```

## Use

From a plugin repo root:

```sh
<skill-dir>/scripts/review.sh
```

This writes a report to `./obsidian-plugin-review-reports/review-<timestamp>.md` and exits non-zero on any `Error`-severity finding.

```sh
# Diff a local report against a dashboard log
diff -u dashboard.log obsidian-plugin-review-reports/review-<ts>.md

# Run a single sub-check
<skill-dir>/scripts/lib/manifest-check.sh .
<skill-dir>/scripts/lib/behavior-scan.sh .

# Make the gate stricter (fail on warnings, not just errors)
<skill-dir>/scripts/review.sh --fail-on=warning
```

## What you get

A report in the reviewer's exact format:

```markdown
## Releases

- **Recommendation**: Missing GitHub artifact attestations for release assets
  - main.js
  - styles.css
  - Artifact attestations let users cryptographically verify the provenance of the release assets, ...

## Behavior

- **Warning**: **Direct Filesystem Access**: Uses the Node.js `fs` module to access the filesystem outside of the Obsidian vault API. ...
- **Pass**: **Vault Write**: Creates or modifies vault files via the Obsidian API (`vault.modify`, `vault.create`, etc.)

## Source code

- **Error**: Don't detach leaves in onunload, as that will reset the leaf to its default location ...
  - obsidianmd/detach-leaves
  - src/main.ts:109-112
- **Warning**: Use 'window.setTimeout()' instead of 'setTimeout()' for popout window compatibility.
  - obsidianmd/prefer-window-timers
  - src/modules/ptySession.ts:113, ...
```

`Error` fails the review. `Warning` and `Recommendation` are flags. `Pass` is a positive report.

## What this skill does not do

- It does not submit releases or talk to the dashboard — that's still done at <https://community.obsidian.md/>.
- It does not have the dashboard's malware / vulnerability signatures (those are private).
- It does not yet implement disclosure labels, privacy labels, or the "Verified author" badge — those are "coming in the coming months" per the blog post, with no public spec to implement against.

## Layout

```
obsidian-plugin-review/
├── SKILL.md                      # this skill's instructions for the agent
├── README.md                     # you are here
├── references/
│   ├── rule-catalog.md           # every rule, with severity and fix
│   ├── review-output-format.md   # the three-section format, exactly
│   ├── severity-and-fail-thresholds.md
│   ├── capability-detection.md   # how Behavior section is built, with extension points
│   ├── manifest-check.md         # manifest field rules
│   └── release-check.md          # GitHub artifact attestations
└── scripts/
    ├── review.sh                 # main entry point
    └── lib/
        ├── .eslintrc.obsidian-review.cjs   # the eslint config
        ├── eslint-runner.sh                # runs eslint, emits TSV
        ├── behavior-scan.sh                # static capability analysis
        ├── manifest-check.sh               # manifest.json validation
        ├── release-check.sh                # GitHub attestation check
        ├── report.sh                       # TSV → markdown
        └── package.json                    # npm deps
```

## See also

- [obsidian-plugin-release](../obsidian-plugin-release/) — for the full submission workflow
- [obsidian-plugin-bootstrap](../obsidian-plugin-bootstrap/) — for scaffolding a new plugin
- [The future of Obsidian plugins](https://obsidian.md/blog/future-of-plugins/) — blog post
- [obsidianmd/eslint-plugin](https://github.com/obsidianmd/eslint-plugin) — the linter
