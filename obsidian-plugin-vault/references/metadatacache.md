# MetadataCache Reference

Source: [Obsidian Developer Docs — MetadataCache](https://docs.obsidian.md/Reference/TypeScript+API/MetadataCache)

## Overview

Contains pre-parsed metadata for all indexed files in the vault.

## Key Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `getFileCache` | `(file: TFile) => CachedMetadata \| null` | Get metadata for a file object |
| `getCache` | `(path: string) => CachedMetadata \| null` | Get metadata by path string |

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `resolvedLinks` | `Record<string, Record<string, number>>` | Maps source path → destination paths with link counts |

## Events

| Event | Callback Signature | Description |
|-------|-------------------|-------------|
| `changed` | `(file: TFile, data: string, cache: CachedMetadata) => void` | File metadata changed |
| `deleted` | `(file: TFile, prevCache: CachedMetadata) => void` | File deleted |
| `resolve` | `(file: TFile) => void` | File metadata resolved |

## Usage

```typescript
const cache = this.app.metadataCache.getFileCache(file);
const frontmatter = cache?.frontmatter;
const headings = cache?.headings;
```
