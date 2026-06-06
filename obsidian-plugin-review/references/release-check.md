# Release Check (the `## Releases` section)

The reviewer runs a check against the plugin's published GitHub release and reports under `## Releases`. The local script reproduces the only known check: **GitHub artifact attestations**.

## What is an artifact attestation?

GitHub's [artifact attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds) let users cryptographically verify that a release asset (`main.js`, `manifest.json`, `styles.css`) was built from the source repository, not tampered with in transit. The reviewer flags any release whose assets are not attested.

## Detection

The local script:

1. Parses `manifest.json#version` to get the current version.
2. Queries the GitHub Releases API for the plugin's repo (`GITHUB_REPOSITORY` env var or read from `manifest.json#repo` if present, or guessed from the git remote `origin`).
3. For each release asset matching `main.js`, `manifest.json`, `styles.css`, looks for a corresponding `.attestation` file in the release.
4. If any expected asset is missing its attestation, the script reports a single `Recommendation` finding.

No auth required for public repos. The script uses `gh api` if `gh` is installed and authenticated, falling back to unauthenticated `curl` (rate-limited to 60 req/h).

## Reproducing the reviewer's output

```markdown
## Releases

- **Recommendation**: Missing GitHub artifact attestations for release assets
  - main.js
  - styles.css
  - Artifact attestations let users cryptographically verify the provenance of the release assets, proving they were built from the source repository. https://docs.github.com/...
```

Sub-bullets are **asset names** (the missing ones), then an **explanation line** with the docs URL. The local script follows the same structure.

## How to add attestations to your release workflow

In `.github/workflows/release.yml`, after the build step:

```yaml
- name: Attest build provenance
  uses: actions/attest-build-provenance@v1
  with:
    subject-path: |
      main.js
      manifest.json
      styles.css
```

The action must be running with `permissions: id-token: write` (or `attestations: write`) at the job or workflow level.

## Skipping the check

The local script skips the release check if:

- `GITHUB_REPOSITORY` is not set and the git remote can't be determined, **or**
- `--skip-release` is passed to `review.sh`, **or**
- the version in `manifest.json` has no matching release (the plugin is pre-release).

The reviewer would still run the check; the local skip is so a developer can lint a plugin before its first release.

## Future checks

The blog mentions several other release-time checks the dashboard will eventually incorporate:

- **Adoption of app capabilities** — does the plugin use the safe Obsidian APIs (`vault.modify` vs `fs.writeFile`).
- **Privacy labels** — coming soon.
- **Verified author** — coming soon.

The local script has stub functions for these in `scripts/lib/release-check.sh` so they're easy to flesh out when Obsidian publishes the specs.
