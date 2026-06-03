# obsidian-plugin-workspace

OpenCode skill for mastering the Obsidian workspace API.

## What this skill covers

- **Workspace tree model**: `WorkspaceRoot`, `WorkspaceSplit`, `WorkspaceTabs`, `WorkspaceLeaf`
- **Leaf lifecycle**: creating, detaching, revealing, deferred tabs
- **Pane management**: `getLeaf()`, `getLeftLeaf()`, `getRightLeaf()`, `createLeafInParent()`, `ensureSideLeaf()`
- **Custom Views**: `ItemView`, `FileView`, `TextFileView`, `MarkdownView`
- **Registration**: `registerView()`, `registerExtensions()`
- **Pop-out windows**: `openPopoutLeaf()`, `moveLeafToPopout()`
- **Linked panes**: `setGroup()`, `setGroupMember()`
- **Workspace events**: `active-leaf-change`, `layout-change`, `file-open`, `window-open`, etc.

## When to use

Use this skill when:
- Building custom sidebar panels or editor views
- Managing where and how panes open
- Reacting to layout changes or focus changes
- Working with linked/scroll-synced panes
- Supporting pop-out windows on desktop

## Files

- `SKILL.md` — Main skill documentation with patterns and snippets
- `references/api-reference.md` — Quick reference for key classes and methods
