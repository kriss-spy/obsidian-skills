# TFile Reference

Source: [Obsidian Developer Docs — TFile](https://docs.obsidian.md/Reference/TypeScript+API/TFile)

## Overview

Represents a file inside the vault. Extends `TAbstractFile`.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `basename` | `string` | Name without extension |
| `extension` | `string` | File extension |
| `name` | `string` | Full file name with extension (inherited) |
| `path` | `string` | Vault-relative path (inherited) |
| `parent` | `TFolder \| null` | Parent folder (inherited) |
| `vault` | `Vault` | Vault instance (inherited) |
| `stat` | `FileStats` | File metadata (size, ctime, mtime) |

## Usage

```typescript
import { TFile } from 'obsidian';

const file = this.app.vault.getFileByPath('Notes/Idea.md');
if (file) {
  console.log(file.basename); // "Idea"
  console.log(file.extension); // "md"
}
```
