# Vault API Reference

Source: [Obsidian Developer Docs — Vault](https://docs.obsidian.md/Reference/TypeScript+API/Vault)

## Overview

`Vault` extends `Events`. Work with files and folders stored inside a vault.

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `adapter` | `DataAdapter` | Low-level file system adapter |
| `configDir` | `string` | Path to config folder (typically `.obsidian`) |

## Key Methods

| Method | Description |
|--------|-------------|
| `read(file)` | Read plaintext from disk. Use if you intend to modify afterward. |
| `cachedRead(file)` | Read from cache. Better performance for read-only use. |
| `create(path, data, options?)` | Create a new plaintext file. |
| `createBinary(path, data, options?)` | Create a new binary file. |
| `modify(file, data, options?)` | Modify plaintext contents. |
| `modifyBinary(file, data, options?)` | Modify binary contents. |
| `process(file, fn, options?)` | Atomically read, modify, and save. |
| `delete(file, force?)` | Delete the file completely. |
| `rename(file, newPath)` | Rename or move a file. Prefer `FileManager.renameFile()` for link updates. |
| `copy(file, newPath)` | Create a copy of a file or folder. |
| `append(file, data, options?)` | Append text to a plaintext file. |
| `appendBinary(file, data, options?)` | Append data to a binary file. |
| `createFolder(path)` | Create a new folder. |
| `getAbstractFileByPath(path)` | Get file or folder at path. Returns `TAbstractFile \| null`. |
| `getFileByPath(path)` | Get file at path. Returns `TFile \| null`. |
| `getFolderByPath(path)` | Get folder at path. Returns `TFolder \| null`. |
| `getMarkdownFiles()` | Get all Markdown files. |
| `getFiles()` | Get all files. |
| `getAllLoadedFiles()` | Get all files and folders. |
| `getAllFolders(includeRoot?)` | Get all folders. |
| `getRoot()` | Get root folder. |
| `getName()` | Get vault name. |
| `getResourcePath(file)` | Get a browser URI for the file. |
| `trash(file, system?)` | Move to trash (system or local). |

## Events

| Event | Callback Signature | Description |
|-------|-------------------|-------------|
| `create` | `(file: TAbstractFile) => void` | File created. Also fires for existing files on vault load. |
| `modify` | `(file: TAbstractFile) => void` | File modified. |
| `delete` | `(file: TAbstractFile) => void` | File deleted. |
| `rename` | `(file: TAbstractFile, oldPath: string) => void` | File renamed or moved. |
