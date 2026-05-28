---
name: obsidian-performance
description: "Diagnose and optimize Obsidian vault performance issues. Use this when the user asks about Obsidian running slowly, vault performance optimization, debugging slow Obsidian behavior, plugin performance impact, or improving Obsidian responsiveness."
risk: safe
source: community
date_added: "2026-05-17"
---

# Obsidian Performance Optimization

Diagnose and resolve Obsidian performance issues by analyzing plugin impact, vault structure, and configuration. Performance problems in Obsidian are more often caused by community plugins than by Obsidian itself.

## When to Use This Skill

- User reports Obsidian is running slowly or lagging
- User wants to optimize vault performance
- User needs to debug why Obsidian is unresponsive
- User wants to identify performance-heavy plugins
- User asks about vault size impact on performance

## Core Workflow

### Phase 1: Identify the Problem

Ask the user to describe:
1. What specific actions are slow? (startup, search, typing, switching notes, etc.)
2. Approximate vault size (number of files, total size)
3. Number of enabled community plugins
4. When did the performance issue start?

### Phase 2: Debug Using Obsidian's Built-in Tools

Guide the user to use Obsidian's performance debugging:

1. **Open the Command Palette** (`Ctrl/Cmd + P`)
2. **Run "Show debug info"** - copies system info to clipboard
3. **Open Developer Tools** (`Ctrl/Cmd + Shift + I`)
   - Check Console for errors
   - Check Performance tab to record and analyze slow operations
4. **Safe Mode Test**: Restart Obsidian in Safe Mode (Settings > Community plugins > Safe mode) to isolate plugin-related issues

Reference: [How to Debug why Obsidian is running slowly](https://publish.obsidian.md/hub/04+-+Guides%2C+Workflows%2C+%26+Courses/Guides/How+to+debug+why+Obsidian+is+running+slowly)

### Phase 3: Plugin Analysis

Community plugins are the most common cause of performance issues.

**High-impact plugins to check:**
- Plugins that scan the entire vault frequently (search, graph, tag-related)
- Plugins that modify the editor in real-time (syntax highlighters, live preview enhancers)
- Plugins that process files on save (linters, formatters)
- Plugins with canvas or Excalidraw integrations

**Diagnostic steps:**
1. Disable all community plugins (Safe Mode)
2. If performance improves, re-enable plugins one by one
3. Test after each enable to identify the culprit
4. Check plugin settings for performance-related options (e.g., debounce delays, file limits)

Use `obsidian plugin list` via CLI to review installed plugins.

### Phase 4: Vault Structure Optimization

**Large vault considerations:**
- Files in the root directory slow down indexing - use folder organization
- Reduce number of tags per file
- Avoid deeply nested folder structures (>5 levels)
- Check for circular links or broken references
- Consider excluding large folders (attachments, backups) via Settings > Files & Links > Excluded files

**Attachment management:**
- Store attachments in a dedicated folder
- Compress or externalize large images/PDFs
- Use external links for media files instead of embedding

### Phase 5: Configuration Tuning

**Settings to adjust:**
- Settings > Editor > Live Preview (toggle to test performance)
- Settings > Files & Links > Attachment folder path (consolidate attachments)
- Settings > Appearance > Hardware acceleration (toggle if GPU issues)
- Settings > Community plugins > Review and disable unused plugins

**CLI commands for maintenance:**
- `obsidian help` - list available commands
- `obsidian daily` - open daily note directly
- Use CLI for batch operations instead of manual UI interactions

## Quick Reference: Common Performance Fixes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Slow startup | Too many plugins | Disable unused plugins, use Safe Mode |
| Typing lag | Editor plugins | Disable syntax highlighters, live preview enhancers |
| Search is slow | Large vault, many tags | Exclude folders, reduce tag usage |
| Graph view crashes | Too many files/links | Filter graph, disable auto-refresh |
| High memory usage | Canvas/Excalidraw files | Close unused tabs, limit canvas size |
| Sync is slow | Many small files | Consolidate notes, reduce attachment count |

## Performance Optimization Checklist

- [ ] Test in Safe Mode to isolate plugin issues
- [ ] Review and disable unnecessary community plugins
- [ ] Check Developer Tools Console for errors
- [ ] Organize files into folders (avoid root clutter)
- [ ] Set up attachment folder and consolidate media
- [ ] Configure excluded files for non-note directories
- [ ] Update Obsidian and all plugins to latest versions
- [ ] Consider hardware acceleration settings
- [ ] Review vault size and consider splitting if >10,000 files

## References

- [Obsidian Debug Guide](https://publish.obsidian.md/hub/04+-+Guides%2C+Workflows%2C+%26+Courses/Guides/How+to+debug+why+Obsidian+is+running+slowly)
- [Obsidian CLI Documentation](https://help.obsidian.md/cli)
- [Obsidian Community Plugins](https://obsidian.md/plugins)
