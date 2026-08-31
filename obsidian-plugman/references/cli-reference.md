# Plugman CLI Reference

Exact flags and verified output shapes for `plugman` (first release line, v0.1.x). Run `plugman <command> --help` for the authoritative list on any installed binary.

## Global

- Bare `plugman` — print help.
- `plugman --version` — print the executable version (release builds report the release tag).
- Every command runs against the current directory, which must be the exact Vault Root (contains `.obsidian/`).

## Commands and flags

| Command | Flags | Notes |
|---------|-------|-------|
| `install <inputs...>` | `--enable`, `--allow-downgrade`, `--dry-run` | At least one input required |
| `update [inputs...]` | `--allow-downgrade`, `--dry-run` | Bare form updates official-directory plugins |
| `uninstall <ids...>` | `--keep-data`, `--yes`, `--dry-run` | Non-interactive use requires `--yes` |
| `list` | `--enabled`, `--json` | Vault-local only, no network |
| `outdated` | `--json` | Read-only network check |
| `info <input>` | `--json` | One official ID or GitHub URL |
| `export <path>` | `--enabled`, `--latest`, `--force` | Fails before writing on unresolvable provenance |

## Verified JSON shapes

`plugman list --json`:

```json
{
  "schemaVersion": 1,
  "plugins": [
    {
      "folder": "demo",
      "id": "demo",
      "version": "1.0.0",
      "enabled": true,
      "source": { "kind": "unknown", "repository": null, "release": null },
      "status": "valid",
      "problems": []
    }
  ]
}
```

`source.kind` values seen in practice: `unknown` (manual install), official directory, or GitHub Source Record from `.plugman.json`. `plugman outdated --json` and `plugman info --json` follow the same `schemaVersion: 1` convention.

Text `list` output is a table: `ID  VERSION  ENABLED  SOURCE  STATUS  PROBLEM`.

## Vault layout touched by Plugman

- `.obsidian/plugins/<id>/` — plugin code, `manifest.json`, optional `data.json`, optional `.plugman.json` Source Record (GitHub installs only).
- `.obsidian/.plugman/recovery/` — preserved recovery material after a Recovery-required result.
- Plugin List files (e.g. `plugins.list`) — read-only inputs; Plugman never edits them.

## Install (the CLI itself)

```sh
# macOS / Linux (user-level, no admin)
curl -fsSL https://github.com/kriss-spy/plugman/releases/latest/download/install.sh | sh

# Windows PowerShell
irm https://github.com/kriss-spy/plugman/releases/latest/download/install.ps1 | iex
```

Options: `--version <v>` / `-Version <v>`, `--bin-dir <dir>` / `-InstallDir <dir>`, and `PLUGMAN_NO_MODIFY_PATH=1` or `-NoModifyPath` to leave PATH untouched. Default destinations: `~/.local/bin` (macOS/Linux) and `%LocalAppData%\Programs\plugman\bin` (Windows). Installers verify SHA-256 checksums and refuse destinations inside a Vault.
