# Obsidian API Reference

Complete reference for the Obsidian JavaScript API when using CDP automation.

## Global `app` Object

The `app` object is the main entry point for Obsidian's API.

### App Properties

| Property | Type | Description |
|----------|------|-------------|
| `app.vault` | `Vault` | File system operations |
| `app.workspace` | `Workspace` | UI and layout management |
| `app.metadataCache` | `MetadataCache` | File metadata and links |
| `app.fileManager` | `FileManager` | File manipulation utilities |
| `app.plugins` | `PluginManager` | Plugin management |
| `app.commands` | `CommandManager` | Command execution |
| `app.setting` | `Settings` | App settings |

---

## Vault API

### File Operations

```javascript
// Get all files
const files = app.vault.getFiles();

// Get markdown files only
const markdownFiles = app.vault.getMarkdownFiles();

// Get file by path
const file = app.vault.getAbstractFileByPath("Folder/Note.md");

// Read file content
const content = await app.vault.read(file);

// Modify file
await app.vault.modify(file, "New content");

// Create new file
const newFile = await app.vault.create("Folder/New Note.md", "Content");

// Delete file
await app.vault.delete(file);

// Rename file
await app.vault.rename(file, "Folder/New Name.md");

// Check if file exists
const exists = app.vault.getAbstractFileByPath("Note.md") !== null;
```

### Directory Operations

```javascript
// Get all loaded files (includes folders)
const allFiles = app.vault.getAllLoadedFiles();

// Filter for folders only
const folders = allFiles.filter(f => f.children !== undefined);

// Create folder
await app.vault.createFolder("New Folder");

// Check if path is folder
const isFolder = file instanceof require('obsidian').TFolder;
```

### Vault Properties

| Property | Type | Description |
|----------|------|-------------|
| `app.vault.adapter` | `DataAdapter` | Low-level file system |
| `app.vault.configDir` | `string` | `.obsidian` path |
| `app.vault.getName()` | `string` | Vault name |

---

## Workspace API

### Active File

```javascript
// Get active file
const activeFile = app.workspace.getActiveFile();

// Get active editor
const activeEditor = app.workspace.activeEditor;

// Get active view
const activeView = app.workspace.getActiveViewOfType(require('obsidian').MarkdownView);
```

### Opening Files

```javascript
// Open file
await app.workspace.openLinkText("Note Name", "", false);

// Open in new leaf (pane)
await app.workspace.openLinkText("Note Name", "", true);

// Open with specific view state
await app.workspace.openLinkText("Note Name", "", false, { state: { mode: "source" } });
```

### Leaves and Panes

```javascript
// Get all leaves
const leaves = app.workspace.getLeavesOfType("markdown");

// Get leaf by type
const markdownLeaf = app.workspace.getLeavesOfType("markdown")[0];

// Detach leaf (close pane)
markdownLeaf.detach();

// Split leaf
const newLeaf = app.workspace.createLeafBySplit(markdownLeaf);
```

### Workspace Events

```javascript
// Listen for file open
app.workspace.on('file-open', (file) => {
  console.log('Opened:', file?.path);
});

// Listen for active leaf change
app.workspace.on('active-leaf-change', (leaf) => {
  console.log('Active leaf changed');
});
```

---

## MetadataCache API

### File Cache

```javascript
// Get cache for file
const cache = app.metadataCache.getFileCache(file);

// Cache properties
{
  frontmatter: { title: "Note", tags: ["project"] },
  headings: [{ heading: "Title", level: 1, position: {...} }],
  links: [{ link: "Other Note", displayText: "Other", position: {...} }],
  embeds: [{ link: "Image.png", position: {...} }],
  tags: [{ tag: "#project", position: {...} }],
  blocks: { "block-id": { ... } }
}
```

### Link Resolution

```javascript
// Resolve link to file
const targetFile = app.metadataCache.getFirstLinkpathDest("Note Name", sourceFile.path);

// Get backlinks
const backlinks = app.metadataCache.getBacklinksForFile(file);

// Get tags
const tags = app.metadataCache.getTags();
```

---

## Plugin API

### Plugin Management

```javascript
// Get plugin instance
const plugin = app.plugins.getPlugin("dataview");

// Check if plugin enabled
const isEnabled = app.plugins.enabledPlugins.has("dataview");

// Enable plugin
await app.plugins.enablePlugin("plugin-id");

// Disable plugin
await app.plugins.disablePlugin("plugin-id");

// Get all enabled plugins
const enabled = Array.from(app.plugins.enabledPlugins);
```

### Plugin Instance

```javascript
// Access plugin settings
const settings = plugin.settings;

// Access plugin methods (if exposed)
plugin.someMethod();
```

---

## Command API

### Execute Commands

```javascript
// Execute by ID
app.commands.executeCommandById("app:reload");

// List all commands
const commands = app.commands.listCommands();
commands.forEach(cmd => {
  console.log(`${cmd.id}: ${cmd.name}`);
});

// Find command by name
const command = commands.find(c => c.name.includes("Reload"));
```

### Common Command IDs

| Command | ID |
|---------|-----|
| Reload app | `app:reload` |
| Open settings | `app:open-settings` |
| Open quick switcher | `app:open-quick-switcher` |
| Toggle graph | `graph:open` |
| Toggle outline | `outline:open` |

---

## FileManager API

### File Operations

```javascript
// Generate markdown link
const link = app.fileManager.generateMarkdownLink(file, sourcePath);
// Returns: [[File Name]] or [[File Name|Display]]

// Get new file path
const newPath = app.fileManager.getNewFileParent("Folder");

// Trash file
await app.fileManager.trashFile(file);
```

---

## Common Patterns

### Find Files by Tag

```javascript
function findByTag(tag) {
  return app.vault.getMarkdownFiles().filter(file => {
    const cache = app.metadataCache.getFileCache(file);
    return cache?.tags?.some(t => t.tag === tag);
  });
}

// Usage
const projectFiles = findByTag("#project");
```

### Find Orphaned Files

```javascript
function findOrphans() {
  const allFiles = app.vault.getMarkdownFiles();
  const linked = new Set();
  
  allFiles.forEach(file => {
    const cache = app.metadataCache.getFileCache(file);
    cache?.links?.forEach(link => {
      const dest = app.metadataCache.getFirstLinkpathDest(link.link, file.path);
      if (dest) linked.add(dest.path);
    });
  });
  
  return allFiles.filter(f => !linked.has(f.path));
}
```

### Get Daily Notes

```javascript
function getDailyNotes() {
  return app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith("Daily/"))
    .sort((a, b) => b.name.localeCompare(a.name));
}
```

### Batch Update Files

```javascript
async function batchUpdate(files, transformer) {
  for (const file of files) {
    const content = await app.vault.read(file);
    const newContent = transformer(content);
    if (content !== newContent) {
      await app.vault.modify(file, newContent);
    }
  }
}

// Usage
await batchUpdate(
  app.vault.getMarkdownFiles(),
  content => content.replace(/old/g, "new")
);
```

---

## Type References

### TFile

```javascript
{
  path: "Folder/Note.md",
  name: "Note.md",
  basename: "Note",
  extension: "md",
  stat: { size: 1234, mtime: 1234567890, ctime: 1234567890 },
  parent: TFolder
}
```

### TFolder

```javascript
{
  path: "Folder",
  name: "Folder",
  children: [TFile, TFolder, ...],
  parent: TFolder
}
```

### CachedMetadata

```javascript
{
  frontmatter?: { [key: string]: any },
  frontmatterPosition?: Pos,
  headings?: HeadingCache[],
  sections?: SectionCache[],
  links?: ReferenceCache[],
  embeds?: ReferenceCache[],
  tags?: TagCache[],
  blocks?: { [id: string]: BlockCache },
  listItems?: ListItemCache[]
}
```
