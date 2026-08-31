---
name: obsidian-plugman
description: "Drive the Plugman CLI to install, update, uninstall, inspect, and export Obsidian community plugins from a terminal. Use when the user wants to manage Obsidian plugins with plugman, restore plugins into a vault from a plugin list, check or apply plugin updates, preview changes with dry-run, or script plugin management with JSON output."
triggers:
  - plugman
  - obsidian plugin manager
  - install obsidian plugin
  - update obsidian plugins
  - obsidian plugin list
  - plugins.list
  - obsidian plugins cli
author: OpenCode
version: 1.0.0
created: 2026-08-31
---

# Obsidian Plugman

Plugman is a standalone, npm-like command-line manager for Obsidian community plugins. Each command operates on exactly one Vault: the Vault Root that is the current working directory. It works while Obsidian is open (coordinating disable/reload with the app) and while it is closed.

This skill covers operating the `plugman` executable. It does not cover building or developing Plugman itself.

## 1. Check the CLI is installed

```sh
plugman --version
```

If missing, install it for the current user (no admin rights needed):

```sh
# macOS / Linux
curl -fsSL https://github.com/kriss-spy/plugman/releases/latest/download/install.sh | sh

# Windows PowerShell
irm https://github.com/kriss-spy/plugman/releases/latest/download/install.ps1 | iex
```

Set `PLUGMAN_NO_MODIFY_PATH=1` before the install command to skip PATH changes. Open a new terminal after installing. `go install github.com/kriss-spy/plugman/cmd/plugman@latest` also works when Go is available.

**Live coordination requirement:** when Obsidian is open, Plugman must coordinate with it through the official Obsidian CLI. Make sure the `obsidian` executable is on PATH (and enabled in Obsidian) before mutating plugins in a running vault. Closed-vault operations need nothing extra.

## 2. Run it from the Vault Root

Every command requires the current directory to be the exact Vault Root (the directory containing `.obsidian/`). Plugman does not search parent directories and accepts no vault-path override. Run commands with the vault root as the working directory; for an agent this means resolving the vault root first, then executing each command there.

```sh
cd ~/Documents/MyVault
plugman list
```

Run from the wrong directory fails fast with `current directory is not an Obsidian Vault Root` and changes nothing.

## 3. Command surface

| Command | Purpose |
|---------|---------|
| `install <inputs...>` | Install plugins from IDs, versions, Plugin Lists, or GitHub URLs |
| `update [inputs...]` | Advance installed plugins to newer releases |
| `uninstall <ids...>` | Remove plugins (asks for confirmation unless `--yes`) |
| `list` | Show installed plugins and their state (vault-local, no network) |
| `outdated` | Check installed plugins for newer releases (read-only) |
| `info <input>` | Show release, compatibility, and installation details for one plugin |
| `export <path>` | Write the installed set to a Plugin List file |

Common flags: `--json` on read commands emits stable JSON with no ANSI escapes; `--dry-run` on every mutating command resolves and validates the plan without touching the vault.

### install

```sh
plugman install dataview                        # newest compatible release
plugman install dataview@0.5.67                 # exact version
plugman install ./plugins.list                  # whole Plugin List
plugman install https://github.com/owner/repo   # GitHub release asset
plugman install dataview --enable --dry-run     # preview first
```

- At least one input required; inputs may mix IDs, `id@version`, Plugin List paths, and GitHub URLs.
- Newly installed plugins stay **disabled** unless `--enable` is passed; `--enable` only affects plugins newly installed by this command.
- An already-installed unversioned plugin is left unchanged. An exact declaration upgrades an older install; downgrading needs `--allow-downgrade`.

### update

```sh
plugman update            # every installed official-directory plugin
plugman update dataview   # targeted
plugman update --dry-run  # print planned version changes only
```

- Bare `update` covers plugins known to Obsidian's official community directory; a GitHub-only plugin must be named by URL or via a Plugin List containing its URL.
- Enabled stays enabled, disabled stays disabled.
- Prints the plan, then applies it **without asking again**. Exact versions and exact release URLs never move.

### uninstall

```sh
plugman uninstall demo           # interactive: shows state, asks once
plugman uninstall demo --yes     # non-interactive
plugman uninstall demo --keep-data
```

- Default removes the entire plugin folder, including `data.json` and the `.plugman.json` Source Record.
- `--keep-data` preserves `data.json` for later reinstall.
- Non-interactive runs require `--yes`. Uninstall never edits Plugin Lists.

### list / outdated / info

```sh
plugman list --json
plugman outdated
plugman info dataview --json
```

- All three are read-only. `list` uses vault-local state only.
- `outdated` reports current vs newest compatible version, enabled state, source, and release URL.
- `info` accepts one official ID or GitHub URL.

### export

```sh
plugman export saved.plugins
plugman export prod.plugins --enabled --latest --force
```

- Official plugins export as IDs; GitHub-only plugins export using their Source Records.
- Exact installed versions are written by default; `--latest` omits them.
- Export fails before writing if any included plugin has neither an official listing nor a Source Record (e.g. manually copied plugin folders) — it names the unresolved plugin.
- An existing destination is never overwritten without `--force`.

## 4. Plugin Inputs and Plugin Lists

A Plugin Input is one of:

```text
dataview                                                 # official community ID
dataview@0.5.67                                          # pinned official ID
./plugins.list                                           # Plugin List file
https://github.com/owner/repo                            # GitHub repository (newest compatible non-prerelease)
https://github.com/owner/repo/releases/tag/1.3.13        # exact release
```

A Plugin List is a plain, user-owned text file:

```text
# Core plugins
dataview
homepage@1.4.3
https://github.com/kriss-spy/obsidian-opencode
```

Blank lines and `#` comments are ignored. Multiple lists compose additively; duplicates of the same resolved plugin are deduplicated; conflicting exact versions fail before any vault change. Plugman treats lists as read-only inputs — it never edits them, including during uninstall.

## 5. GitHub installs

Only public `https://github.com/<owner>/<repo>` URLs are supported. Plugman downloads release assets only (`main.js` + `manifest.json` required, `styles.css` optional) — it never clones, builds, or executes repository scripts. A GitHub install writes a `.plugman.json` Source Record inside the plugin folder; the record documents provenance and does not pin future updates.

Set `GH_TOKEN` or `GITHUB_TOKEN` in the environment to raise GitHub API limits when resolving GitHub-only repositories. Plugman never writes or prints the token.

## 6. Batch and failure semantics

For every mutating command:

1. The entire batch is parsed, resolved, validated, and downloaded first. If preflight fails, **nothing changes**.
2. Plugins are applied sequentially, each with its own short-lived Restore Point.
3. A failing plugin is restored and the command stops; plugins completed earlier in the batch stay applied.
4. Re-running the same command skips satisfied inputs and resumes naturally.

Result categories to interpret for the user:

- **Success** — completed, or no change was needed.
- **Preflight failure** — nothing changed; fix the reported input and re-run.
- **Partial failure** — earlier plugins succeeded, the failing one was restored; re-run to resume.
- **Recovery required** — restoration could not be verified; recovery material was preserved in the vault for manual action. Do not delete `.obsidian/.plugman/recovery/` without reading it.

## 7. Typical workflows

**Preview before acting** — prefer `--dry-run` whenever the outcome is unclear:

```sh
plugman install ./plugins.list --dry-run
plugman update --dry-run
```

**Restore plugins into a fresh vault:**

```sh
cd /path/to/NewVault
plugman install saved.plugins            # or add --enable to activate them
```

**Reproducible setup file:** keep a `plugins.list` in the vault or a dotfiles repo; export exact pins with `plugman export plugins.list`, or portable latest-version pins with `--latest`.

**Routine maintenance:**

```sh
plugman outdated
plugman update --dry-run
plugman update
plugman list --json
```

## 8. Scripting notes

- `--json` output is stable, machine-readable, and ANSI-free; progress and diagnostics go to stderr.
- `list --json` emits `{"schemaVersion":1,"plugins":[...]}` with `folder`, `id`, `version`, `enabled`, `source` (`kind`, `repository`, `release`), `status`, and `problems` per plugin. `source.kind` is `unknown` for manually installed plugins.
- Bare `plugman` prints help; `plugman --version` prints the executable version.

## 9. Boundaries

Plugman deliberately does not: search the community directory, support version ranges or channels, install prereleases implicitly, access private repositories, support BRAT or GitLab, build from source, manage mobile, self-update, or keep lockfiles. For any of these, explain the boundary instead of improvising.

## References

- [CLI reference](references/cli-reference.md) — exact per-command flags and verified output shapes.
