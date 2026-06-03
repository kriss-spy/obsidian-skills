# normalizePath Reference

Source: [Obsidian Developer Docs — normalizePath](https://docs.obsidian.md/Reference/TypeScript+API/normalizePath)

## Overview

Normalizes a path string for safe use with Obsidian APIs.

## Signature

```typescript
export function normalizePath(path: string): string;
```

## Usage

```typescript
import { normalizePath } from 'obsidian';

const safePath = normalizePath('My Folder//New Note.md');
// "My Folder/New Note.md"
```

Use `normalizePath()` before passing paths to `DataAdapter` or constructing file paths dynamically.
