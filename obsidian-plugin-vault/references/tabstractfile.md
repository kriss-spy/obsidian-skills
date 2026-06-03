# TAbstractFile Reference

Source: [Obsidian Developer Docs — TAbstractFile](https://docs.obsidian.md/Reference/TypeScript+API/TAbstractFile)

## Overview

Base class for anything inside the vault.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `path` | `string` | Vault-relative path |
| `name` | `string` | File or folder name |
| `parent` | `TFolder \| null` | Parent folder |
| `vault` | `Vault` | Reference to the vault |

## Narrowing

```typescript
import { TFile, TFolder } from 'obsidian';

const abstractFile = this.app.vault.getAbstractFileByPath('Notes');
if (abstractFile instanceof TFile) {
  // Handle file
} else if (abstractFile instanceof TFolder) {
  // Handle folder
}
```
