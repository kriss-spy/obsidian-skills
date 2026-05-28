# Obsidian CLI Examples

Practical examples for using the Obsidian CLI.

## Vault Management

### Create a New Vault

```bash
obsidian vault create "My Knowledge Base" --path ~/Documents/Obsidian
```

### Open an Existing Vault

```bash
obsidian vault open ~/Documents/Obsidian
```

### List Recent Vaults

```bash
obsidian vault list
```

## File Operations

### Open a Specific Note

```bash
obsidian open ~/Documents/Obsidian/Projects/Project-Alpha.md
```

### Create a New Note

```bash
obsidian note create "Meeting Notes" \
  --path ~/Documents/Obsidian/Meetings \
  --content "## Attendees\n\n## Agenda\n\n## Notes"
```

### Daily Notes

```bash
# Today's daily note
obsidian daily-note

# Specific date
obsidian daily-note --date "2024-01-15"
```

## Plugin Management

### Install a Plugin

```bash
# Install Dataview
obsidian plugin install dataview

# Install Templater
obsidian plugin install templater-obsidian
```

### Enable/Disable Plugins

```bash
# Enable
obsidian plugin enable dataview

# Disable
obsidian plugin disable dataview
```

### List Installed Plugins

```bash
obsidian plugin list
```

### Reload Plugin (Development)

```bash
# Reload your custom plugin
obsidian plugin reload my-custom-plugin
```

## JavaScript Evaluation

### Get Vault Statistics

```bash
obsidian eval --code "
  console.log(JSON.stringify({
    files: app.vault.getFiles().length,
    folders: app.vault.getAllLoadedFiles().filter(f => f.children).length
  }))
"
```

### List All Tags

```bash
obsidian eval --code "
  const tags = new Set();
  app.vault.getFiles().forEach(file => {
    const cache = app.metadataCache.getFileCache(file);
    if (cache?.tags) {
      cache.tags.forEach(t => tags.add(t.tag));
    }
  });
  console.log(JSON.stringify([...tags].sort()));
"
```

### Find Orphaned Files

```bash
obsidian eval --code "
  const allFiles = app.vault.getMarkdownFiles();
  const linked = new Set();
  
  allFiles.forEach(file => {
    const cache = app.metadataCache.getFileCache(file);
    if (cache?.links) {
      cache.links.forEach(link => {
        const dest = app.metadataCache.getFirstLinkpathDest(link.link, file.path);
        if (dest) linked.add(dest.path);
      });
    }
  });
  
  const orphaned = allFiles.filter(f => !linked.has(f.path));
  console.log(JSON.stringify(orphaned.map(f => f.path)));
"
```

## Developer Tools

### View Console Errors

```bash
obsidian dev:errors
```

### Take Screenshot

```bash
obsidian dev:screenshot --output ~/screenshots/obsidian-$(date +%Y%m%d).png
```

### Inspect DOM

```bash
obsidian dev:dom --selector ".workspace-leaf-content"
```

## Search

### Search Vault

```bash
# Simple search
obsidian search "project alpha"

# Regex search
obsidian search "TODO.*urgent" --regex

# Search specific vault
obsidian search "meeting" --path ~/Documents/Obsidian
```

## Automation Scripts

### Daily Backup Script

```bash
#!/bin/bash
# backup-vault.sh

VAULT_PATH="$HOME/Documents/Obsidian"
BACKUP_DIR="$HOME/Backups/Obsidian"
DATE=$(date +%Y%m%d)

# Create backup
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/vault-$DATE.tar.gz" -C "$VAULT_PATH" .

# Keep only last 7 backups
ls -t "$BACKUP_DIR"/vault-*.tar.gz | tail -n +8 | xargs rm -f

echo "Backup complete: vault-$DATE.tar.gz"
```

### Sync Daily Note

```bash
#!/bin/bash
# sync-daily.sh

# Create daily note
obsidian daily-note

# Get note content
TODAY=$(date +%Y-%m-%d)
obsidian eval --code "
  const file = app.vault.getAbstractFileByPath('Daily Notes/$TODAY.md');
  if (file) {
    app.vault.read(file).then(content => console.log(content));
  }
"
```

## Environment Variables

### Set Default Vault

```bash
export OBSIDIAN_VAULT_PATH="$HOME/Documents/Obsidian"

# Now commands will use this vault by default
obsidian daily-note
obsidian plugin list
```

### Debug Mode

```bash
export OBSIDIAN_DEBUG=1
obsidian vault list
```
