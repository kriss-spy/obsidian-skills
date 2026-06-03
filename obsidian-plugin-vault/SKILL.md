---
name: obsidian-plugin-vault
description: Work with the Obsidian Vault API, file operations, and metadata cache. Covers reading, writing, creating, deleting, and renaming files; navigating TFile, TAbstractFile, and TFolder; listening to vault events; and querying parsed metadata via MetadataCache. Use when implementing file system features, batch operations, note generators, or anything that touches vault contents.
triggers:
  - obsidian vault api
  - obsidian file operations
  - obsidian vault read write
  - obsidian vault create delete
  - obsidian metadata cache
  - obsidian tfile
  - obsidian vault events
  - obsidian file system
  - obsidian get markdown files
  - obsidian frontmatter cache
  - obsidian file rename
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Plugin Vault

This skill covers the `Vault` API for reading, writing, and managing files and folders inside an Obsidian vault. It also covers the file type hierarchy (`TFile`, `TAbstractFile`, `TFolder`), vault events, and the `MetadataCache` for querying parsed frontmatter, headings, links, and tags.

## When to Use This Skill

- Reading or modifying note contents programmatically
- Creating, deleting, or renaming files and folders
- Batch-processing all Markdown files in the vault
- Listening for file changes (create, modify, delete, rename)
- Querying parsed metadata (frontmatter, headings, links, embeds, tags)
- Working with the active file or resolving file paths

## Overview

`this.app.vault` is the primary interface for file system operations. It extends `Events`, so you can subscribe to vault-wide changes. `this.app.metadataCache` provides pre-parsed metadata for every indexed file, avoiding the need to parse Markdown yourself.

Key rule: always use `Vault` APIs instead of raw Node.js `fs` calls. Obsidian's abstraction handles sync, mobile compatibility, and link updates.

---

## File Types

### `TAbstractFile`

The base class for anything inside the vault. Properties:

| Property | Type | Description |
|----------|------|-------------|
| `path` | `string` | Vault-relative path |
| `name` | `string` | File or folder name |
| `parent` | `TFolder \| null` | Parent folder, or `null` for root |
| `vault` | `Vault` | Reference to the vault instance |

Use `instanceof TFile` or `instanceof TFolder` to narrow the type.

### `TFile`

Represents a file. Extends `TAbstractFile`.

| Property | Type | Description |
|----------|------|-------------|
| `basename` | `string` | Name without extension |
| `extension` | `string` | File extension (e.g., `md`) |
| `stat` | `FileStats` | Size, creation time, modification time |

Use `TFile` when you need to read, modify, or delete a specific file.

### `TFolder`

Represents a folder. Extends `TAbstractFile`.

| Property | Type | Description |
|----------|------|-------------|
| `children` | `TAbstractFile[]` | Files and subfolders inside this folder |

Use `TFolder` when iterating over directory contents or creating nested paths.

---

## File Operations

### Reading Files

```typescript
import { TFile } from 'obsidian';

// Read directly from disk (use this if you plan to modify the file)
const file = this.app.vault.getAbstractFileByPath('Notes/Idea.md');
if (file instanceof TFile) {
  const content = await this.app.vault.read(file);
  console.log(content);
}
```

Use `cachedRead()` when you only need to display content to the user and do not intend to modify it afterward. It avoids unnecessary disk reads.

```typescript
const content = await this.app.vault.cachedRead(file);
```

### Creating Files

```typescript
// Create a plaintext file
await this.app.vault.create('New Note.md', '# Hello World');

// Create inside a folder (create the folder first if needed)
await this.app.vault.createFolder('Projects');
await this.app.vault.create('Projects/Todo.md', '- [ ] Task 1');
```

> [!tip]
> `vault.create()` throws if the file already exists. Check first or catch the error.

### Modifying Files

```typescript
const file = this.app.vault.getAbstractFileByPath('Notes/Idea.md');
if (file instanceof TFile) {
  await this.app.vault.modify(file, '# Updated Idea\n\nNew content here.');
}
```

For atomic read-modify-write operations, use `process()`:

```typescript
await this.app.vault.process(file, (data) => {
  return data.replace(/TODO/g, 'DONE');
});
```

This avoids race conditions if the file changes between read and write.

### Deleting Files

```typescript
const file = this.app.vault.getAbstractFileByPath('Notes/Old.md');
if (file instanceof TFile) {
  await this.app.vault.delete(file);
}
```

Pass `true` as the second argument to force-delete without moving to trash.

### Renaming and Moving

```typescript
const file = this.app.vault.getAbstractFileByPath('Notes/Draft.md');
if (file instanceof TFile) {
  await this.app.vault.rename(file, 'Notes/Final.md');
}
```

> [!caution]
> If you need links to be automatically updated across the vault, use `this.app.fileManager.renameFile()` instead of `vault.rename()`.

### Creating Folders

```typescript
await this.app.vault.createFolder('Archive/2026');
```

Creates intermediate folders automatically if needed.

---

## Locating Files

### `getAbstractFileByPath()`

Returns `TAbstractFile | null`. Narrow with `instanceof`:

```typescript
const abstractFile = this.app.vault.getAbstractFileByPath('Notes/Log.md');
if (abstractFile instanceof TFile) {
  // It's a file
} else if (abstractFile instanceof TFolder) {
  // It's a folder
}
```

### `getFileByPath()` and `getFolderByPath()`

Type-safe helpers that return `TFile | null` and `TFolder | null` respectively:

```typescript
const file = this.app.vault.getFileByPath('Notes/Log.md');
const folder = this.app.vault.getFolderByPath('Notes');
```

### Listing All Files

```typescript
// All Markdown files
const markdownFiles = this.app.vault.getMarkdownFiles();

// All files (including attachments)
const allFiles = this.app.vault.getFiles();

// All files and folders
const everything = this.app.vault.getAllLoadedFiles();

// All folders
const folders = this.app.vault.getAllFolders();
```

---

## MetadataCache

`this.app.metadataCache` holds parsed metadata for every indexed file. Use it instead of parsing Markdown yourself.

### `getFileCache()`

```typescript
const file = this.app.vault.getFileByPath('Notes/Idea.md');
if (file) {
  const cache = this.app.metadataCache.getFileCache(file);
  if (cache) {
    // Frontmatter
    console.log(cache.frontmatter);

    // Headings
    console.log(cache.headings);

    // Internal links [[like this]]
    console.log(cache.links);

    // Embeds ![[like this]]
    console.log(cache.embeds);

    // Tags #tag or frontmatter tags
    console.log(cache.tags);

    // Block references ^block-id
    console.log(cache.blocks);
  }
}
```

### `getCache()`

Query by path string instead of `TFile`:

```typescript
const cache = this.app.metadataCache.getCache('Notes/Idea.md');
```

### Frontmatter

`cache.frontmatter` is a plain object. Keys match your frontmatter properties.

```typescript
const cache = this.app.metadataCache.getFileCache(file);
const status = cache?.frontmatter?.status ?? 'draft';
const tags = cache?.frontmatter?.tags ?? [];
```

### Tags

`getAllTags()` combines frontmatter tags and inline `#tags` into a single array:

```typescript
import { getAllTags } from 'obsidian';

const cache = this.app.metadataCache.getFileCache(file);
const allTags = getAllTags(cache);
// ['#idea', '#project', '#daily']
```

### Resolved Links

`metadataCache.resolvedLinks` maps source paths to destination paths with link counts:

```typescript
const links = this.app.metadataCache.resolvedLinks['Notes/Idea.md'];
// { 'Notes/Related.md': 2, 'Notes/Other.md': 1 }
```

---

## Vault Events

`Vault` extends `Events`. Subscribe to changes with `this.app.vault.on(...)`. Always register the handler so it is cleaned up on unload.

### `create`

Fired when a file is created. Also fires for every existing file when the vault first loads. To skip initial load events, register inside `this.app.workspace.onLayoutReady()`.

```typescript
this.registerEvent(
  this.app.vault.on('create', (file: TAbstractFile) => {
    if (file instanceof TFile) {
      console.log('Created:', file.path);
    }
  })
);
```

### `modify`

Fired when a file is modified.

```typescript
this.registerEvent(
  this.app.vault.on('modify', (file: TAbstractFile) => {
    if (file instanceof TFile) {
      console.log('Modified:', file.path);
    }
  })
);
```

### `delete`

Fired when a file is deleted.

```typescript
this.registerEvent(
  this.app.vault.on('delete', (file: TAbstractFile) => {
    console.log('Deleted:', file.path);
  })
);
```

### `rename`

Fired when a file or folder is renamed or moved. The callback receives the new file object and the old path.

```typescript
this.registerEvent(
  this.app.vault.on('rename', (file: TAbstractFile, oldPath: string) => {
    console.log('Renamed:', oldPath, '→', file.path);
  })
);
```

---

## Patterns

### Safe File Operations

Always check that a file exists and is the expected type before operating on it. Wrap async calls in `try/catch`.

```typescript
async safeModify(path: string, newContent: string) {
  const file = this.app.vault.getFileByPath(path);
  if (!file) {
    new Notice(`File not found: ${path}`);
    return;
  }

  try {
    await this.app.vault.modify(file, newContent);
    new Notice('File updated');
  } catch (error) {
    console.error('Modify failed:', error);
    new Notice('Failed to update file');
  }
}
```

### Path Handling

Use `normalizePath()` before constructing or comparing paths:

```typescript
import { normalizePath } from 'obsidian';

const safePath = normalizePath('My Folder/New Note.md');
// "My Folder/New Note.md"
```

### Working with the Active File

```typescript
const activeFile = this.app.workspace.getActiveFile();
if (activeFile) {
  const content = await this.app.vault.read(activeFile);
  const cache = this.app.metadataCache.getFileCache(activeFile);
  // ...
}
```

### Reading Frontmatter

```typescript
const file = this.app.workspace.getActiveFile();
if (file) {
  const cache = this.app.metadataCache.getFileCache(file);
  const frontmatter = cache?.frontmatter;
  if (frontmatter) {
    const tags: string[] = frontmatter.tags ?? [];
    const date: string = frontmatter.date ?? '';
    console.log({ tags, date });
  }
}
```

### Batch Processing

Process all Markdown files without blocking the UI:

```typescript
async processAllNotes() {
  const files = this.app.vault.getMarkdownFiles();

  for (const file of files) {
    const content = await this.app.vault.read(file);
    // ... do work ...
  }
}
```

For very large vaults, consider chunking or yielding to the event loop.

---

## Quick Reference

| Task | API |
|------|-----|
| Read file | `vault.read(file)` |
| Cached read | `vault.cachedRead(file)` |
| Create file | `vault.create(path, data)` |
| Create folder | `vault.createFolder(path)` |
| Modify file | `vault.modify(file, data)` |
| Atomic modify | `vault.process(file, fn)` |
| Delete file | `vault.delete(file)` |
| Rename file | `vault.rename(file, newPath)` |
| Get by path | `vault.getAbstractFileByPath(path)` |
| Get file | `vault.getFileByPath(path)` |
| Get folder | `vault.getFolderByPath(path)` |
| All Markdown | `vault.getMarkdownFiles()` |
| All files | `vault.getFiles()` |
| Metadata | `metadataCache.getFileCache(file)` |
| Tags | `getAllTags(cache)` |
| Resolved links | `metadataCache.resolvedLinks` |
| Normalize path | `normalizePath(path)` |

---

## References

- [Vault API](https://docs.obsidian.md/Reference/TypeScript+API/Vault) — Official TypeScript API reference
- [TFile](https://docs.obsidian.md/Reference/TypeScript+API/TFile) — File object properties
- [TAbstractFile](https://docs.obsidian.md/Reference/TypeScript+API/TAbstractFile) — Base file type
- [TFolder](https://docs.obsidian.md/Reference/TypeScript+API/TFolder) — Folder object properties
- [CachedMetadata](https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata) — Parsed metadata structure
- [MetadataCache](https://docs.obsidian.md/Reference/TypeScript+API/MetadataCache) — Metadata query methods
- [normalizePath](https://docs.obsidian.md/Reference/TypeScript+API/normalizePath) — Path normalization utility
- [getAllTags](https://docs.obsidian.md/Reference/TypeScript+API/getAllTags) — Combine all tags from a file
