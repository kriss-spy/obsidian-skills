# TFolder Reference

Source: [Obsidian Developer Docs — TFolder](https://docs.obsidian.md/Reference/TypeScript+API/TFolder)

## Overview

Represents a folder inside the vault. Extends `TAbstractFile`.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `children` | `TAbstractFile[]` | Files and subfolders inside this folder |
| `path` | `string` | Vault-relative path (inherited) |
| `name` | `string` | Folder name (inherited) |
| `parent` | `TFolder \| null` | Parent folder (inherited) |
| `vault` | `Vault` | Vault instance (inherited) |

## Usage

```typescript
import { TFolder } from 'obsidian';

const folder = this.app.vault.getFolderByPath('Projects');
if (folder) {
  for (const child of folder.children) {
    console.log(child.path);
  }
}
```
