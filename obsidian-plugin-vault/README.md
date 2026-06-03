# obsidian-plugin-vault

AI agent skill for the Obsidian Vault API, file operations, and metadata cache.

## What This Skill Covers

- **File operations**: `read`, `cachedRead`, `create`, `modify`, `delete`, `rename`, `createFolder`, `process`
- **File types**: `TFile`, `TAbstractFile`, `TFolder` — when to use each
- **Locating files**: `getAbstractFileByPath`, `getFileByPath`, `getFolderByPath`, `getMarkdownFiles`, `getFiles`
- **MetadataCache**: `getFileCache`, `getCache`, frontmatter, headings, links, embeds, tags, blocks
- **Vault events**: `create`, `modify`, `delete`, `rename`
- **Patterns**: safe file operations, path handling, working with the active file, reading frontmatter

## Usage

This skill is triggered by prompts related to:
- Obsidian vault API and file operations
- Reading, writing, creating, or deleting vault files
- Metadata cache, frontmatter, tags, links
- Vault events and file system changes

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Main skill instructions and code patterns |
| `references/` | Thin reference docs from official Obsidian sources |

## References

- [Vault API](https://docs.obsidian.md/Reference/TypeScript+API/Vault)
- [TFile](https://docs.obsidian.md/Reference/TypeScript+API/TFile)
- [TAbstractFile](https://docs.obsidian.md/Reference/TypeScript+API/TAbstractFile)
- [TFolder](https://docs.obsidian.md/Reference/TypeScript+API/TFolder)
- [CachedMetadata](https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata)
- [MetadataCache](https://docs.obsidian.md/Reference/TypeScript+API/MetadataCache)
