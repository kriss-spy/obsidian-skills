# Persistence Reference

## loadData

```typescript
loadData(): Promise<any>
```

Reads `data.json` from the plugin folder (`.obsidian/plugins/<id>/data.json`). Resolves to `null` if the file does not exist.

## saveData

```typescript
saveData(data: any): Promise<void>
```

Serializes `data` and writes it to `data.json`. Data must be JSON-serializable.

## Load Pattern

```typescript
async loadSettings() {
  this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
}
```

## Save Pattern

```typescript
async saveSettings() {
  await this.saveData(this.settings);
}
```

## External Changes

```typescript
async onExternalSettingsChange() {
  await this.loadSettings();
}
```

Called when `data.json` is modified externally (e.g., via Sync).
