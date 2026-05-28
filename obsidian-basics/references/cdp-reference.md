# CDP Protocol Reference for Obsidian

Complete reference for Chrome DevTools Protocol commands when automating Obsidian.

## Getting Started

### Connection Endpoints

When Obsidian runs with `--remote-debugging-port=9222`:

```
GET http://localhost:9222/json/version     # Browser version info
GET http://localhost:9222/json/list        # List available targets
GET http://localhost:9222/json/protocol    # Full protocol definition
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:9222/devtools/page/{targetId}');
```

---

## Runtime Domain

The Runtime domain is used to execute JavaScript in Obsidian's context.

### Runtime.evaluate

Execute JavaScript code.

**Parameters:**
```javascript
{
  expression: string,      // JavaScript to execute
  objectGroup?: string,    // Group for object references
  includeCommandLineAPI?: boolean,  // Include console
  silent?: boolean,        // Suppress exceptions
  contextId?: number,      // Execution context ID
  returnByValue?: boolean, // Return value directly
  userGesture?: boolean,   // Treat as user gesture
  awaitPromise?: boolean,  // Await promise result
  throwOnSideEffect?: boolean,
  timeout?: number,
  disableBreaks?: boolean,
  replMode?: boolean,
  allowUnsafeEvalBlockedByCSP?: boolean,
  uniqueContextId?: string
}
```

**Returns:**
```javascript
{
  result: RemoteObject,    // Evaluation result
  exceptionDetails?: ExceptionDetails  // If exception thrown
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Runtime.evaluate',
  params: {
    expression: 'app.vault.getFiles().length',
    returnByValue: true,
    awaitPromise: false
  }
}));
```

### Runtime.enable / Runtime.disable

Enable or disable Runtime events.

**Example:**
```javascript
// Enable console events
ws.send(JSON.stringify({
  id: 1,
  method: 'Runtime.enable'
}));
```

### Runtime.consoleAPICalled Event

Fired when console API is called.

**Event Data:**
```javascript
{
  type: 'log' | 'debug' | 'info' | 'error' | 'warning' | 'dir' | 'dirxml' | 'table' | 'trace' | 'clear' | 'startGroup' | 'startGroupCollapsed' | 'endGroup' | 'assert' | 'profile' | 'profileEnd' | 'count' | 'timeEnd',
  args: RemoteObject[],
  executionContextId: number,
  timestamp: number,
  stackTrace?: StackTrace,
  context?: string
}
```

**Example:**
```javascript
ws.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.method === 'Runtime.consoleAPICalled') {
    const { type, args } = msg.params;
    console.log(`[${type}]`, args.map(a => a.value).join(' '));
  }
});
```

---

## Page Domain

### Page.captureScreenshot

Capture screenshot of Obsidian.

**Parameters:**
```javascript
{
  format?: 'jpeg' | 'png',  // Default: 'png'
  quality?: number,         // 0-100 (jpeg only)
  clip?: Viewport,          // Clip region
  fromSurface?: boolean,    // Capture from surface
  captureBeyondViewport?: boolean
}
```

**Returns:**
```javascript
{
  data: string  // Base64 encoded image
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Page.captureScreenshot',
  params: { format: 'png' }
}));

// Response handling
ws.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.result?.data) {
    const buffer = Buffer.from(msg.result.data, 'base64');
    fs.writeFileSync('screenshot.png', buffer);
  }
});
```

### Page.enable / Page.disable

Enable or disable Page domain.

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Page.enable'
}));
```

### Page.reload

Reload the page.

**Parameters:**
```javascript
{
  ignoreCache?: boolean,    // Bypass cache
  scriptToEvaluateOnLoad?: string  // Script to run after reload
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Page.reload',
  params: { ignoreCache: true }
}));
```

---

## DOM Domain

### DOM.querySelector

Query DOM element.

**Parameters:**
```javascript
{
  nodeId: number,    // Parent node ID (0 for document)
  selector: string   // CSS selector
}
```

**Returns:**
```javascript
{
  nodeId: number  // Node ID of found element (0 if not found)
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'DOM.querySelector',
  params: {
    nodeId: 0,
    selector: '.workspace-leaf-content'
  }
}));
```

### DOM.querySelectorAll

Query multiple DOM elements.

**Parameters:**
```javascript
{
  nodeId: number,
  selector: string
}
```

**Returns:**
```javascript
{
  nodeIds: number[]
}
```

### DOM.getDocument

Get document root.

**Parameters:**
```javascript
{
  depth?: number,           // Depth to fetch
  pierce?: boolean          // Pierce through shadow DOM
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'DOM.getDocument',
  params: { depth: 1 }
}));
```

---

## Network Domain

### Network.enable

Enable network tracking.

**Parameters:**
```javascript
{
  maxTotalBufferSize?: number,
  maxResourceBufferSize?: number,
  maxPostDataSize?: number
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Network.enable'
}));
```

### Network.getResponseBody

Get response body.

**Parameters:**
```javascript
{
  requestId: string
}
```

**Returns:**
```javascript
{
  body: string,
  base64Encoded: boolean
}
```

---

## Debugger Domain

### Debugger.enable

Enable debugger.

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Debugger.enable'
}));
```

### Debugger.pause / Debugger.resume

Pause and resume execution.

**Example:**
```javascript
// Pause
ws.send(JSON.stringify({
  id: 1,
  method: 'Debugger.pause'
}));

// Resume
ws.send(JSON.stringify({
  id: 1,
  method: 'Debugger.resume'
}));
```

---

## Target Domain

### Target.getTargets

Get all targets.

**Returns:**
```javascript
{
  targetInfos: TargetInfo[]
}
```

**Example:**
```javascript
ws.send(JSON.stringify({
  id: 1,
  method: 'Target.getTargets'
}));
```

### Target.attachToTarget

Attach to target.

**Parameters:**
```javascript
{
  targetId: string,
  flatten?: boolean
}
```

**Returns:**
```javascript
{
  sessionId: string
}
```

---

## Common Patterns

### Complete CDP Client

```javascript
const WebSocket = require('ws');

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.messageId = 0;
    this.pending = new Map();
    
    this.ws.on('message', (data) => {
      const msg = JSON.parse(data);
      
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        
        if (msg.error) {
          reject(new Error(msg.error.message));
        } else {
          resolve(msg.result);
        }
      }
      
      // Handle events
      if (msg.method) {
        this.emit(msg.method, msg.params);
      }
    });
  }
  
  async send(method, params = {}) {
    await new Promise((resolve, reject) => {
      if (this.ws.readyState === WebSocket.OPEN) {
        resolve();
      } else {
        this.ws.once('open', resolve);
        this.ws.once('error', reject);
      }
    });
    
    const id = ++this.messageId;
    
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  
  on(event, handler) {
    this.ws.on('message', (data) => {
      const msg = JSON.parse(data);
      if (msg.method === event) {
        handler(msg.params);
      }
    });
  }
  
  close() {
    this.ws.close();
  }
}

module.exports = { CDPClient };
```

### Obsidian Automation Class

```javascript
const { CDPClient } = require('./cdp-client');

class ObsidianAutomation {
  async connect(port = 9222) {
    const response = await fetch(`http://localhost:${port}/json/list`);
    const targets = await response.json();
    const target = targets.find(t => t.type === 'page');
    
    if (!target) {
      throw new Error('Obsidian not found');
    }
    
    this.client = new CDPClient(target.webSocketDebuggerUrl);
    return this;
  }
  
  async eval(expression) {
    const result = await this.client.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    
    if (result.exceptionDetails) {
      throw new Error(result.exceptionDetails.exception?.description);
    }
    
    return result.result.value;
  }
  
  async screenshot(format = 'png') {
    const result = await this.client.send('Page.captureScreenshot', { format });
    return Buffer.from(result.data, 'base64');
  }
  
  onConsole(callback) {
    this.client.send('Runtime.enable');
    this.client.on('Runtime.consoleAPICalled', callback);
  }
  
  close() {
    this.client.close();
  }
}

module.exports = { ObsidianAutomation };
```

---

## Error Handling

### Common Errors

**Connection Refused:**
- Obsidian not running with `--remote-debugging-port`
- Wrong port number
- Firewall blocking connection

**Target Not Found:**
- Obsidian window not fully loaded
- Multiple windows - need to select correct target

**Execution Context Destroyed:**
- Page reloaded during execution
- Plugin reloaded

### Error Response Format

```javascript
{
  id: 1,
  error: {
    code: number,
    message: string,
    data?: any
  }
}
```
