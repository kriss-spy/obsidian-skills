# Obsidian CLI Command Reference

Complete reference for the Obsidian CLI commands.

## Installation

```bash
# macOS
brew install obsidian

# Linux (download from obsidian.md)
curl -L -o obsidian https://obsidian.md/download && chmod +x obsidian
```

## Global Options

```bash
obsidian [command] [options]

--help, -h      Show help
--version, -v   Show version
--debug         Enable debug output
```

---

## vault

Vault management commands.

### vault create

Create a new vault.

```bash
obsidian vault create <name> [options]

Options:
  --path <path>     Vault location (required)
  --template <tpl>  Use template vault

Example:
  obsidian vault create "My Notes" --path ~/Documents/Obsidian
```

### vault open

Open an existing vault.

```bash
obsidian vault open <path> [options]

Options:
  --new-window      Open in new window

Example:
  obsidian vault open ~/Documents/Obsidian
```

### vault list

List recent vaults.

```bash
obsidian vault list [options]

Options:
  --limit <n>       Limit results (default: 10)
  --json            Output as JSON

Example:
  obsidian vault list --limit 5 --json
```

---

## open

Open a specific file.

```bash
obsidian open <path> [options]

Options:
  --line <n>        Jump to line number
  --new-tab         Open in new tab

Example:
  obsidian open ~/Documents/Obsidian/Projects/Notes.md --line 10
```

---

## note

Note management commands.

### note create

Create a new note.

```bash
obsidian note create <title> [options]

Options:
  --path <path>     Vault path (required)
  --content <text>  Initial content
  --template <tpl>  Use template
  --open            Open after creation

Example:
  obsidian note create "Meeting Notes" \
    --path ~/Documents/Obsidian \
    --content "## Attendees\n\n" \
    --open
```

---

## daily-note

Open or create daily note.

```bash
obsidian daily-note [options]

Options:
  --date <date>     Specific date (YYYY-MM-DD)
  --offset <days>   Offset from today

Example:
  obsidian daily-note                    # Today
  obsidian daily-note --date 2024-01-15  # Specific date
  obsidian daily-note --offset -1        # Yesterday
```

---

## plugin

Plugin management commands.

### plugin list

List installed plugins.

```bash
obsidian plugin list [options]

Options:
  --enabled-only    Show only enabled plugins
  --community-only  Show only community plugins
  --core-only       Show only core plugins
  --json            Output as JSON

Example:
  obsidian plugin list --enabled-only --json
```

### plugin install

Install a community plugin.

```bash
obsidian plugin install <id> [options]

Options:
  --version <ver>   Specific version
  --enable          Enable after install

Example:
  obsidian plugin install dataview --enable
```

### plugin uninstall

Uninstall a plugin.

```bash
obsidian plugin uninstall <id>

Example:
  obsidian plugin uninstall dataview
```

### plugin enable

Enable a plugin.

```bash
obsidian plugin enable <id>

Example:
  obsidian plugin enable dataview
```

### plugin disable

Disable a plugin.

```bash
obsidian plugin disable <id>

Example:
  obsidian plugin disable dataview
```

### plugin reload

Reload a plugin (useful for development).

```bash
obsidian plugin reload <id>

Example:
  obsidian plugin reload my-custom-plugin
```

---

## eval

Execute JavaScript in Obsidian context.

```bash
obsidian eval [options]

Options:
  --code <js>       JavaScript code to execute
  --file <path>     JavaScript file to execute
  --json            Parse output as JSON

Example:
  # Simple evaluation
  obsidian eval --code "app.vault.getFiles().length"
  
  # Multi-line code
  obsidian eval --code "
    const files = app.vault.getFiles();
    console.log(JSON.stringify({
      count: files.length
    }));
  "
  
  # From file
  obsidian eval --file script.js
```

### Available Globals in Eval

```javascript
app              // Main app instance
require          // Node-style require
console          // Console API
process          // Process info
```

### Eval Examples

**Get Vault Stats:**
```bash
obsidian eval --code "
  const stats = {
    files: app.vault.getFiles().length,
    markdown: app.vault.getMarkdownFiles().length,
    active: app.workspace.getActiveFile()?.path
  };
  console.log(JSON.stringify(stats));
"
```

**List All Tags:**
```bash
obsidian eval --code "
  const tags = new Set();
  app.vault.getMarkdownFiles().forEach(file => {
    const cache = app.metadataCache.getFileCache(file);
    cache?.tags?.forEach(t => tags.add(t.tag));
  });
  console.log(JSON.stringify([...tags].sort()));
"
```

**Search Files:**
```bash
obsidian eval --code "
  const query = 'TODO';
  const results = app.vault.getMarkdownFiles().filter(file => {
    const content = app.vault.cachedRead(file);
    return content.includes(query);
  });
  console.log(JSON.stringify(results.map(f => f.path)));
"
```

---

## search

Search vault contents.

```bash
obsidian search <query> [options]

Options:
  --path <path>     Vault path
  --regex           Use regex search
  --case-sensitive  Case sensitive search
  --json            Output as JSON

Example:
  obsidian search "project alpha"
  obsidian search "TODO|FIXME" --regex
```

---

## dev

Developer tools.

### dev:errors

View console errors.

```bash
obsidian dev:errors [options]

Options:
  --follow, -f      Keep streaming errors
  --limit <n>       Limit results
  --since <time>    Only errors since timestamp
  --json            Output as JSON

Example:
  obsidian dev:errors --follow
  obsidian dev:errors --limit 10
```

### dev:screenshot

Capture screenshot.

```bash
obsidian dev:screenshot [options]

Options:
  --output <path>   Output file path
  --format <fmt>    Format: png, jpeg (default: png)
  --quality <n>     JPEG quality 0-100
  --full-page       Capture full page

Example:
  obsidian dev:screenshot --output screenshot.png
  obsidian dev:screenshot --format jpeg --quality 90
```

### dev:dom

Inspect DOM elements.

```bash
obsidian dev:dom [options]

Options:
  --selector <sel>  CSS selector
  --html            Include HTML content
  --text            Include text content
  --json            Output as JSON

Example:
  obsidian dev:dom --selector ".nav-file-title" --text
```

### dev:debug

Enable debug mode.

```bash
obsidian dev:debug [options]

Options:
  --port <n>        Debug port (default: 9222)

Example:
  obsidian dev:debug --port 9223
```

---

## config

Configuration commands.

### config get

Get configuration value.

```bash
obsidian config get <key> [options]

Example:
  obsidian config get theme
  obsidian config get hotkeys
```

### config set

Set configuration value.

```bash
obsidian config set <key> <value>

Example:
  obsidian config set theme "obsidian"
```

---

## Environment Variables

```bash
# Default vault path
export OBSIDIAN_VAULT_PATH="$HOME/Documents/Obsidian"

# Debug output
export OBSIDIAN_DEBUG=1

# CLI config directory
export OBSIDIAN_CONFIG_DIR="$HOME/.config/obsidian"
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Vault not found |
| 4 | Plugin not found |
| 5 | Network error |
| 6 | Permission denied |

---

## Scripting Examples

### Backup Script

```bash
#!/bin/bash
set -e

VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian}"
BACKUP_DIR="$HOME/Backups/Obsidian"
DATE=$(date +%Y%m%d-%H%M%S)

# Create backup
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/vault-$DATE.tar.gz" -C "$VAULT" .

# Cleanup old backups (keep 10)
ls -t "$BACKUP_DIR"/vault-*.tar.gz | tail -n +11 | xargs -r rm

echo "Backup complete: vault-$DATE.tar.gz"
```

### Sync Status

```bash
#!/bin/bash
obsidian eval --code "
  const files = app.vault.getFiles();
  const lastModified = files
    .map(f => f.stat.mtime)
    .sort((a, b) => b - a)[0];
  
  console.log(JSON.stringify({
    totalFiles: files.length,
    lastModified: new Date(lastModified).toISOString()
  }));
" --json
```

### Plugin Health Check

```bash
#!/bin/bash
echo "Checking plugin health..."

obsidian plugin list --json | jq -r '.[] | select(.enabled) | .id' | while read -r plugin; do
  echo "Checking $plugin..."
  obsidian eval --code "
    const p = app.plugins.getPlugin('$plugin');
    console.log(JSON.stringify({
      id: '$plugin',
      loaded: !!p,
      version: p?.manifest?.version
    }));
  " --json
done
```
