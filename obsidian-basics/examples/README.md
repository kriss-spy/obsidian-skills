# Obsidian CDP Automation Examples

This folder contains practical examples for automating Obsidian using the Chrome DevTools Protocol (CDP).

## Examples

### 1. Basic Connection

```javascript
// connect.js
const WebSocket = require('ws');

async function getWebSocketUrl() {
  const response = await fetch('http://localhost:9222/json/list');
  const targets = await response.json();
  const page = targets.find(t => t.type === 'page');
  return page?.webSocketDebuggerUrl;
}

async function connect() {
  const wsUrl = await getWebSocketUrl();
  if (!wsUrl) {
    throw new Error('Obsidian not found. Start with --remote-debugging-port=9222');
  }
  
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    ws.on('open', () => resolve(ws));
    ws.on('error', reject);
  });
}

module.exports = { connect };
```

### 2. Vault Operations

```javascript
// vault-ops.js
const { connect } = require('./connect');

async function getVaultInfo() {
  const ws = await connect();
  
  return new Promise((resolve, reject) => {
    const id = Date.now();
    
    ws.once('message', (data) => {
      const response = JSON.parse(data);
      if (response.id === id) {
        ws.close();
        if (response.error) reject(response.error);
        else resolve(JSON.parse(response.result.value));
      }
    });
    
    ws.send(JSON.stringify({
      id,
      method: 'Runtime.evaluate',
      params: {
        expression: `
          JSON.stringify({
            fileCount: app.vault.getFiles().length,
            folderCount: app.vault.getAllLoadedFiles()
              .filter(f => f.children).length,
            activeFile: app.workspace.getActiveFile()?.path,
            enabledPlugins: Array.from(app.plugins.enabledPlugins)
          })
        `,
        returnByValue: true
      }
    }));
  });
}

getVaultInfo().then(console.log);
```

### 3. File Creation

```javascript
// create-note.js
const { connect } = require('./connect');

async function createNote(path, content) {
  const ws = await connect();
  
  return new Promise((resolve, reject) => {
    const id = Date.now();
    
    ws.once('message', (data) => {
      const response = JSON.parse(data);
      if (response.id === id) {
        ws.close();
        if (response.error) reject(response.error);
        else resolve(response.result.value);
      }
    });
    
    ws.send(JSON.stringify({
      id,
      method: 'Runtime.evaluate',
      params: {
        expression: `
          app.vault.create(${JSON.stringify(path)}, ${JSON.stringify(content)})
            .then(() => 'Created: ${path}')
            .catch(e => 'Error: ' + e.message)
        `,
        awaitPromise: true,
        returnByValue: true
      }
    }));
  });
}

// Usage
const content = `---
date: ${new Date().toISOString().split('T')[0]}
tags: [daily]
---

# Daily Note

Today\'s notes...
`;

createNote(`Daily/${new Date().toISOString().split('T')[0]}.md`, content)
  .then(console.log)
  .catch(console.error);
```

### 4. Screenshot

```javascript
// screenshot.js
const { connect } = require('./connect');
const fs = require('fs');

async function takeScreenshot(outputPath = 'screenshot.png') {
  const ws = await connect();
  
  return new Promise((resolve, reject) => {
    const id = Date.now();
    
    ws.once('message', (data) => {
      const response = JSON.parse(data);
      if (response.id === id) {
        ws.close();
        if (response.error) {
          reject(response.error);
        } else {
          const buffer = Buffer.from(response.result.data, 'base64');
          fs.writeFileSync(outputPath, buffer);
          resolve(outputPath);
        }
      }
    });
    
    ws.send(JSON.stringify({
      id,
      method: 'Page.captureScreenshot',
      params: { format: 'png' }
    }));
  });
}

takeScreenshot().then(path => console.log(`Screenshot saved: ${path}`));
```

### 5. Console Monitoring

```javascript
// monitor-console.js
const { connect } = require('./connect');

async function monitorConsole(duration = 10000) {
  const ws = await connect();
  
  console.log(`Monitoring console for ${duration}ms...`);
  
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.method === 'Runtime.consoleAPICalled') {
      const { type, args } = msg.params;
      const text = args.map(a => a.value || a.description).join(' ');
      console.log(`[${type}] ${text}`);
    }
  });
  
  // Enable console events
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.enable'
  }));
  
  // Keep connection open
  await new Promise(resolve => setTimeout(resolve, duration));
  ws.close();
  console.log('Monitoring complete');
}

monitorConsole();
```

### 6. Plugin Development Helper

```javascript
// dev-helper.js
const { connect } = require('./connect');

class ObsidianDevHelper {
  constructor(ws) {
    this.ws = ws;
    this.messageId = 0;
  }
  
  async eval(expression, awaitPromise = true) {
    const id = ++this.messageId;
    
    return new Promise((resolve, reject) => {
      this.ws.once('message', (data) => {
        const response = JSON.parse(data);
        if (response.id === id) {
          if (response.error) reject(response.error);
          else resolve(response.result);
        }
      });
      
      this.ws.send(JSON.stringify({
        id,
        method: 'Runtime.evaluate',
        params: { expression, awaitPromise, returnByValue: true }
      }));
    });
  }
  
  async reloadPlugin(pluginId) {
    await this.eval(`app.plugins.disablePlugin('${pluginId}')`);
    await this.eval(`app.plugins.enablePlugin('${pluginId}')`);
    return `Reloaded: ${pluginId}`;
  }
  
  async getConsoleErrors() {
    const result = await this.eval(`
      JSON.stringify(
        (window._obsidianErrors || [])
          .slice(-50)
          .map(e => ({ message: e.message, stack: e.stack }))
      )
    `);
    return JSON.parse(result.value);
  }
  
  close() {
    this.ws.close();
  }
}

module.exports = { ObsidianDevHelper };
```

## Running Examples

1. Start Obsidian with debugging:
   ```bash
   open -a Obsidian --args --remote-debugging-port=9222
   ```

2. Install dependencies:
   ```bash
   npm install ws
   ```

3. Run an example:
   ```bash
   node vault-ops.js
   ```

## Requirements

- Node.js 18+
- Obsidian running with `--remote-debugging-port=9222`
- `ws` package: `npm install ws`
