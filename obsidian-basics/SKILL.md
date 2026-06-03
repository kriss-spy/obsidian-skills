---
name: obsidian-basics
description: Provides comprehensive knowledge about the Obsidian note-taking app, including vault structure, markdown syntax, CLI usage, and CDP-based GUI automation
triggers:
  - obsidian basics
  - obsidian help
  - obsidian cli
  - obsidian cdp
  - obsidian vault
  - obsidian plugin
  - obsidian remote debugging
author: OpenCode
version: 1.0.0
created: 2026-04-15
---

# Obsidian Basics Skill

This skill should be used when working with the Obsidian note-taking application, including vault management, CLI operations, plugin development, and GUI automation via Chrome DevTools Protocol (CDP).

## When to Use This Skill

- Working with Obsidian vaults (creating, organizing, managing)
- Using the Obsidian CLI for automation and scripting
- Automating Obsidian via Chrome DevTools Protocol (CDP)
- Need quick reference for Obsidian markdown syntax and wiki-links
- Troubleshooting CDP connections or CLI issues
- General Obsidian knowledge (vault structure, configuration, APIs)

> [!tip]
> For deep plugin development — scaffolding, manifest configuration, workspace API, custom views, and release builds — see the `obsidian-plugin-bootstrap` and `obsidian-plugin-workspace` skills.

## Overview

Obsidian is a powerful markdown-based note-taking application built on Electron. It features a vault-centric architecture, extensive plugin ecosystem, and deep customization capabilities. This skill covers:

1. **General Obsidian knowledge** - Vault structure, configuration, markdown syntax
2. **Obsidian CLI** - Command-line interface for vault and plugin management
3. **CDP Automation** - Controlling Obsidian via Chrome DevTools Protocol

---

## Part 1: General Obsidian Knowledge

### Vault Architecture

An Obsidian vault is a folder on your filesystem containing:

```
vault-root/
├── .obsidian/                    # Configuration directory
│   ├── app.json                  # App settings
│   ├── appearance.json           # Theme settings
│   ├── community-plugins.json    # Enabled community plugins
│   ├── core-plugins.json         # Enabled core plugins
│   ├── hotkeys.json              # Keyboard shortcuts
│   ├── workspace.json            # Workspace layout
│   └── plugins/                  # Plugin files
│       └── plugin-id/
│           ├── main.js
│           ├── manifest.json
│           └── styles.css
├── Folder 1/
│   └── Note.md
├── Folder 2/
│   └── Another Note.md
└── Home.md                       # Entry point (optional)
```

**Key Concepts:**
- **Vault**: A folder containing markdown files and the `.obsidian` config directory
- **Workspace**: The current layout of panes, files, and UI state
- **Plugin**: JavaScript extensions that add functionality
- **Theme**: CSS customizations for appearance

### Configuration Files

#### app.json
```json
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "Inbox",
  "attachmentFolderPath": "Attachments"
}
```

#### community-plugins.json
```json
[
  "dataview",
  "templater-obsidian",
  "obsidian-git"
]
```

#### core-plugins.json
```json
[
  "graph",
  "backlink",
  "page-preview",
  "note-composer"
]
```

### Obsidian Markdown Syntax

Obsidian extends standard markdown with wiki-links and special syntax:

**WikiLinks:**
```markdown
[[Page Name]]                    # Link to another note
[[Page Name|Display Text]]       # Link with custom display text
[[Page Name#Heading]]            # Link to specific heading
[[Page Name#Heading|Display]]    # Link to heading with display text
[[#Heading]]                     # Link to heading in current note
```

**Embeds:**
```markdown
![[Embedded Note]]               # Embed entire note
![[Embedded Note#Section]]       # Embed section
![[image.png]]                   # Embed image
```

**Callouts:**
```markdown
> [!info] Title
> Content here

> [!warning] Warning Title
> Warning content

> [!tip] Tip Title
> Tip content
```

**Dataview Queries:**
```markdown
```dataview
LIST
FROM #tag
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```
```

### Key Obsidian APIs

When working with Obsidian programmatically, these APIs are essential:

**Global `app` object:**
```javascript
// Vault operations
app.vault.getFiles()                    // Get all files
app.vault.getAbstractFileByPath(path)   // Get file by path
app.vault.read(file)                    // Read file content
app.vault.modify(file, content)         // Modify file
app.vault.create(path, content)         // Create new file

// Workspace operations
app.workspace.getActiveFile()           // Get currently open file
app.workspace.openLinkText(link, source)// Open a link
app.workspace.getLeavesOfType(type)     // Get panes of type

// Metadata cache
app.metadataCache.getFileCache(file)    // Get frontmatter and links
app.metadataCache.getFirstLinkpathDest(link, source)

// Commands
app.commands.executeCommandById(id)     // Execute command
app.commands.listCommands()             // List all commands

// Plugins
app.plugins.getPlugin(id)               // Get plugin instance
app.plugins.enabledPlugins              // Set of enabled plugin IDs
```

---

## Part 2: Obsidian CLI

### Installation

The Obsidian CLI is available starting from Obsidian v1.12. Install via:

```bash
# macOS
brew install obsidian

# Or download from https://obsidian.md/download
```

> [!tip]
> The `brew install obsidian` formula may not be available in all regions; the official download at https://obsidian.md/download is always current.

### CLI Commands

#### Vault Management

```bash
# Create a new vault
obsidian vault create "My New Vault" --path /path/to/vault

# Open a vault
obsidian vault open "/path/to/vault"

# List recent vaults
obsidian vault list
```

#### File Operations

```bash
# Open a specific file in Obsidian
obsidian open "/path/to/vault/Note.md"

# Create a new note
obsidian note create "Note Name" --path "/path/to/vault" --content "Initial content"

# Daily notes
obsidian daily-note
obsidian daily-note --date "2024-01-01"
```

#### Plugin Management

```bash
# List installed plugins
obsidian plugin list

# Install a community plugin
obsidian plugin install "plugin-id"

# Enable a plugin
obsidian plugin enable "plugin-id"

# Disable a plugin
obsidian plugin disable "plugin-id"

# Reload a plugin (useful for development)
obsidian plugin reload "plugin-id"
```

> [!tip]
> `obsidian plugin reload` is the fastest way to test plugin changes during development. Combine it with `npm run dev` in your plugin project for a tight feedback loop.

#### JavaScript Evaluation

```bash
# Execute JavaScript in Obsidian context
obsidian eval --code "app.vault.getFiles().length"

# Execute from file
obsidian eval --file script.js

# Example: Get vault statistics
obsidian eval --code "console.log(JSON.stringify({files: app.vault.getFiles().length, lastOpen: app.workspace.getActiveFile()?.path}))"
```

> [!caution]
> `obsidian eval` executes JavaScript inside Obsidian's renderer process with full access to `app`, `window`, and Node.js APIs. Only run trusted code.

#### Developer Tools

```bash
# View console logs
obsidian dev:errors

# Take screenshot
obsidian dev:screenshot --output screenshot.png

# Inspect DOM element
obsidian dev:dom --selector ".nav-file-title"

# Enable debug mode
obsidian dev:debug
```

> [!note]
> `obsidian dev:errors` streams the last N console errors. Use it after reproducing a bug to capture stack traces without opening Developer Tools manually.

#### Search Operations

```bash
# Search vault contents
obsidian search "query"

# Search with options
obsidian search "query" --path "/path/to/vault" --regex
```

### CLI Environment Variables

```bash
# Specify vault path
export OBSIDIAN_VAULT_PATH="/path/to/vault"

# Enable debug output
export OBSIDIAN_DEBUG=1
```

> [!tip]
> Set `OBSIDIAN_VAULT_PATH` in your shell profile to avoid passing `--path` on every command.

---

## Part 3: CDP (Chrome DevTools Protocol) Automation

Obsidian is built on Electron, which supports the Chrome DevTools Protocol (CDP). This allows programmatic control of the Obsidian GUI for automation, testing, and integration.

> [!caution]
> Only run CDP on localhost. The debugging port has no authentication; exposing it on a network interface is a security risk.

### Starting Obsidian with CDP

#### macOS
```bash
# Launch with debugging port
open -a Obsidian --args --remote-debugging-port=9222

# Or run binary directly
/Applications/Obsidian.app/Contents/MacOS/Obsidian --remote-debugging-port=9222
```

#### Linux
```bash
obsidian --remote-debugging-port=9222
```

#### Windows
```bash
%LOCALAPPDATA%\Obsidian\Obsidian.exe --remote-debugging-port=9222
```

### Verifying CDP Connection

```bash
# Check if Obsidian is accessible
curl http://localhost:9222/json/version

# List available targets
curl http://localhost:9222/json/list
```

> [!tip]
> Save the `webSocketDebuggerUrl` from `/json/list`; it includes a random UUID that acts as an implicit token.

### CDP WebSocket Connection

Connect to Obsidian via WebSocket to execute commands:

```javascript
const WebSocket = require('ws');

async function connectToObsidian() {
  // Get WebSocket debugger URL
  const response = await fetch('http://localhost:9222/json/list');
  const targets = await response.json();
  const target = targets.find(t => t.type === 'page');
  
  if (!target) {
    throw new Error('No Obsidian target found');
  }
  
  // Connect to WebSocket
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  
  return new Promise((resolve, reject) => {
    ws.on('open', () => resolve(ws));
    ws.on('error', reject);
  });
}

async function evalInObsidian(ws, expression) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    
    ws.once('message', (data) => {
      const response = JSON.parse(data);
      if (response.id === id) {
        if (response.error) {
          reject(new Error(response.error.message));
        } else {
          resolve(response.result);
        }
      }
    });
    
    ws.send(JSON.stringify({
      id,
      method: 'Runtime.evaluate',
      params: {
        expression,
        returnByValue: true,
        awaitPromise: true
      }
    }));
  });
}

// Usage
(async () => {
  const ws = await connectToObsidian();
  const result = await evalInObsidian(ws, 'app.vault.getFiles().length');
  console.log('File count:', result.value);
  ws.close();
})();

> [!important]
> Always pass `awaitPromise: true` when evaluating async code via CDP. Without it, `Runtime.evaluate` returns a Promise object instead of the resolved value.

### Common CDP Operations

#### Execute JavaScript
```javascript
// Get vault information
const vaultInfo = await evalInObsidian(ws, `
  JSON.stringify({
    fileCount: app.vault.getFiles().length,
    activeFile: app.workspace.getActiveFile()?.path,
    plugins: Array.from(app.plugins.enabledPlugins)
  })
`);
```

#### Read Console Logs
```javascript
// Enable console log collection
ws.send(JSON.stringify({
  id: 1,
  method: 'Runtime.enable'
}));

// Listen for console events
ws.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.method === 'Runtime.consoleAPICalled') {
    console.log('Console:', msg.params.args);
  }
});
```

#### Take Screenshots
```javascript
// Capture screenshot
ws.send(JSON.stringify({
  id: 1,
  method: 'Page.captureScreenshot',
  params: {
    format: 'png',  // or 'jpeg'
    quality: 80     // for jpeg only
  }
}), (err, result) => {
  if (result && result.data) {
    const buffer = Buffer.from(result.data, 'base64');
    require('fs').writeFileSync('screenshot.png', buffer);
  }
});
```

> [!tip]
> For PDF or print output, set `format: 'jpeg'` with `quality: 90` to balance file size and fidelity.

#### DOM Inspection
```javascript
// Query DOM elements
const result = await evalInObsidian(ws, `
  JSON.stringify(
    Array.from(document.querySelectorAll('.nav-file-title'))
      .slice(0, 10)
      .map(el => el.textContent)
  )
`);
```

#### Reload Plugins
```javascript
// Reload a plugin during development
await evalInObsidian(ws, `
  app.plugins.disablePlugin('my-plugin');
  app.plugins.enablePlugin('my-plugin');
`);
```

### CDP vs CLI Comparison

| Capability | CDP | CLI |
|------------|-----|-----|
| Read/Write Files | ✅ | ✅ |
| Execute JavaScript | ✅ | ✅ |
| Real-time Console Output | ✅ | ❌ |
| DOM Inspection/Manipulation | ✅ | ❌ (limited) |
| Screenshots | ✅ | ✅ |
| Plugin Management | ✅ | ✅ |
| Command Execution | ✅ | ✅ |
| Error Monitoring | Manual | Built-in |
| Setup Complexity | Medium | Low |

### Recommended Approach

- **Use CLI for:** Day-to-day operations, vault management, simple automation
- **Use CDP for:** E2E testing, DOM manipulation, screenshots, complex automation

> [!note]
> You can combine CLI and CDP in the same workflow: use CLI for file operations and CDP for DOM verification or screenshots.

### MCP Servers for CDP

Several MCP servers provide CDP integration:

**obsidian-cdp-mcp:**
```bash
npx obsidian-cdp-mcp
```

**obsidian-devtools-mcp:**
```bash
# After installation
obsidian-devtools-mcp
```

These servers expose CDP functionality as MCP tools that can be used with Claude Code, GitHub Copilot, and other AI assistants.

> [!tip]
> If you are writing a plugin, prefer `obsidian plugin reload` via CLI over CDP `Runtime.evaluate` for reloading. It is faster and avoids WebSocket overhead.

---

## Part 4: Best Practices

### Vault Organization

```
vault/
├── 00-Inbox/              # Capture notes
├── 01-Projects/           # Active projects
├── 02-Areas/              # Ongoing responsibilities
├── 03-Resources/          # Reference material
├── 04-Archive/            # Completed/inactive
└── Templates/             # Note templates
```

### Working with Frontmatter

```markdown
---
title: Note Title
date: 2026-04-15
tags: [project/alpha, status/active]
author: John Doe
---

# Note Content
```

### Automation Workflows

**Daily Note Creation:**
```bash
obsidian daily-note --date $(date +%Y-%m-%d)
```

**Backup Vault:**
```bash
obsidian eval --code "app.vault.getFiles()" > backup-manifest.json
```

**Plugin Development:**
```bash
# Reload plugin after changes
obsidian plugin reload my-plugin
# Check for errors
obsidian dev:errors
```

### Security Considerations

When using CDP:
1. **Port Security:** Don't expose port 9222 publicly
2. **Local Only:** CDP should only be used on localhost
3. **Authentication:** No built-in auth; rely on local network security

---

## Troubleshooting

### CDP Connection Issues

```bash
# Verify Obsidian is running with debugging
curl http://localhost:9222/json/version

# Check if port is in use
lsof -i :9222

# Restart Obsidian with debugging
pkill Obsidian
open -a Obsidian --args --remote-debugging-port=9222
```

### CLI Issues

```bash
# Update CLI
brew upgrade obsidian

# Check version
obsidian --version

# Verbose output
obsidian vault list --debug
```

### Common Errors

**"Obsidian not found" (CDP):**
- Ensure Obsidian is running with `--remote-debugging-port=9222`
- Check firewall settings

**"Vault not found" (CLI):**
- Verify vault path is correct
- Ensure path has `.obsidian` directory

**Permission Denied:**
- Check file permissions on vault directory
- Run with appropriate user privileges

---

## Quick Reference Checklist

- [ ] Verify Obsidian is installed and CLI is available (`obsidian --version`)
- [ ] Know the vault path and confirm `.obsidian/` directory exists
- [ ] Set `OBSIDIAN_VAULT_PATH` environment variable (optional)
- [ ] Launch Obsidian with `--remote-debugging-port=9222` when using CDP
- [ ] Verify CDP endpoint responds (`curl http://localhost:9222/json/version`)
- [ ] Choose CLI for day-to-day automation, CDP for DOM/testing tasks
- [ ] Keep the debugging port local only; never expose 9222 publicly
- [ ] Use `obsidian plugin reload <id>` for fast plugin iteration
- [ ] Prefer `obsidian eval` for quick JavaScript snippets over full CDP scripts
- [ ] Check `obsidian dev:errors` after plugin crashes to capture stack traces

## Additional Resources

- **Official Help:** https://help.obsidian.md/
- **Developer Docs:** https://docs.obsidian.md/
- **Community Plugins:** https://obsidian.md/plugins
- **CDP Documentation:** https://chromedevtools.github.io/devtools-protocol/
- **Obsidian API Reference:** https://docs.obsidian.md/Reference/TypeScript+API/
