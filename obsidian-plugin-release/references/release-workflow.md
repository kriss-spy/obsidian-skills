# Release Workflow Reference

## GitHub Actions Workflow

`.github/workflows/release.yml` — triggers on tag push, builds, and drafts a release with `main.js`, `manifest.json`, and `styles.css`.

## Release Tag Format

Use `x.y.z` without a `v` prefix. Must exactly match `manifest.json` `version`.

## Required Release Assets

| File | Required | Description |
|------|----------|-------------|
| `main.js` | Yes | Compiled plugin bundle |
| `manifest.json` | Yes | Plugin metadata |
| `styles.css` | No | Optional custom styles |

## BRAT Beta Testing

- Create a GitHub release (can be marked pre-release).
- Include `manifest.json`, `main.js`, `styles.css` in assets.
- Do not commit the beta version to `manifest.json` on the default branch.
- Release tag, release name, and `manifest.json` version must all match.
