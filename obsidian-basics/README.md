# obsidian-basics

A comprehensive skill for working with the Obsidian note-taking application, covering vault management, CLI operations, and GUI automation via Chrome DevTools Protocol (CDP).

## What This Skill Provides

This skill equips AI assistants with knowledge about:

1. **Obsidian Fundamentals** - Vault structure, configuration, markdown syntax, and core concepts
2. **CLI Usage** - Command-line interface for vault and plugin management
3. **CDP Automation** - Programmatic control of Obsidian via Chrome DevTools Protocol

## Installation

```bash
npx skills add @yourscope/obsidian-basics-skill
```

Or install from GitHub:
```bash
npx skills add yourname/obsidian-basics-skill
```

## When to Use This Skill

Use this skill when:
- Working with Obsidian vault files and configuration
- Automating Obsidian via CLI commands
- Developing Obsidian plugins
- Setting up CDP-based automation for E2E testing
- Integrating Obsidian with external tools
- Troubleshooting Obsidian automation issues

## Quick Start

### Understanding Vault Structure

An Obsidian vault is simply a folder with:
- Markdown files (`.md`)
- Configuration in `.obsidian/` directory
- Optional attachments, templates, and plugins

### Using the CLI

```bash
# Create a vault
obsidian vault create "My Vault" --path ~/vaults/my-vault

# Open a vault
obsidian vault open ~/vaults/my-vault

# Create a daily note
obsidian daily-note

# Evaluate JavaScript
obsidian eval --code "app.vault.getFiles().length"
```

### Using CDP Automation

1. Launch Obsidian with debugging:
   ```bash
   # macOS
   open -a Obsidian --args --remote-debugging-port=9222
   
   # Linux
   obsidian --remote-debugging-port=9222
   ```

2. Connect via WebSocket:
   ```javascript
   const ws = new WebSocket('ws://localhost:9222/devtools/page/{targetId}');
   ```

3. Execute JavaScript:
   ```javascript
   ws.send(JSON.stringify({
     id: 1,
     method: 'Runtime.evaluate',
     params: { expression: 'app.vault.getFiles().length' }
   }));
   ```

## Key Capabilities

### 1. Vault Management
- Create and organize vaults
- Understand `.obsidian/` configuration files
- Work with plugins and themes

### 2. File Operations
- Read and modify markdown files
- Work with wiki-links and embeds
- Handle frontmatter metadata

### 3. Plugin Development
- Reload plugins during development
- Debug using console logs
- Inspect DOM elements

### 4. Automation
- Use CLI for simple operations
- Use CDP for complex automation
- Take screenshots programmatically
- Execute arbitrary JavaScript

## Resources

- `SKILL.md` - Complete reference documentation
- `examples/` - Practical code examples
- `references/` - Additional documentation
- `scripts/` - Utility scripts

## External Resources

- [Obsidian Help](https://help.obsidian.md/)
- [Developer Documentation](https://docs.obsidian.md/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Obsidian API Reference](https://docs.obsidian.md/Reference/TypeScript+API/)

## Trigger Phrases

This skill activates on:
- "obsidian basics"
- "obsidian help"
- "obsidian cli"
- "obsidian cdp"
- "obsidian vault"
- "obsidian plugin"
- "obsidian remote debugging"

## Version

1.0.0 - Initial release with comprehensive Obsidian knowledge

## Author

OpenCode
