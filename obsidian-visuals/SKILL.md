---
name: obsidian-visuals
description: Enable agents to detect installed Obsidian visualization plugins and write correct embeddable chart/diagram snippets in markdown notes. Use when creating diagrams, charts, or data visualizations in Obsidian notes, or when the user asks to visualize vault data, create Mermaid diagrams, Dataview queries, Charts plugin blocks, Canvas files, or Excalidraw diagrams.
triggers:
  - obsidian visualization
  - obsidian diagram
  - obsidian chart
  - obsidian mermaid
  - obsidian dataview
  - obsidian canvas
  - obsidian excalidraw
  - obsidian plot
  - obsidian graph
author: OpenCode
version: 1.0.0
created: 2026-06-03
---

# Obsidian Visuals

This skill is a **router/dispatcher** for Obsidian visualizations. It detects which visualization plugins are installed in the current vault, routes the user's request to the correct format, emits valid embeddable snippets, and delegates deep diagram authoring to domain-specific skills (e.g., `mermaid-expert`, `excalidraw-diagram`, etc.).

## When to Use This Skill

- Creating diagrams, charts, or data visualizations inside an Obsidian note
- Determining which visualization plugins are available in the current vault
- Choosing the right visualization type for a given use case
- Writing renderable code blocks or file embeds for Mermaid, Dataview, Charts, Canvas, or Excalidraw
- Generating mathematical or scientific plots when Mermaid/Charts are insufficient
- Delegating complex diagram authoring to specialized skills

## Overview

Obsidian supports several visualization ecosystems. Some are built-in (Mermaid, Canvas), while others require community plugins (Dataview, Charts, Excalidraw). This skill does **not** contain deep syntax guides for those formats—those live in the `references/` folder and in dedicated skills. Instead, this skill:

1. **Detects** installed visualization plugins by reading the vault's plugin manifest
2. **Routes** the user's intent to the correct visualization type
3. **Emits** minimal, valid, embeddable snippets
4. **Delegates** to other skills for full syntax depth and complex authoring

If a requested plugin is not installed, fall back to core Obsidian features (Mermaid or Canvas) or generate a static image with Python.

---

## 1. Detect Available Visualizations

### Read the Plugin Manifest

The canonical way to discover installed community plugins is to read `.obsidian/community-plugins.json` in the vault root.

#### Via Filesystem (direct vault access)

```typescript
import { readFileSync } from 'fs';
import { join } from 'path';

function getInstalledPlugins(vaultPath: string): string[] {
  const manifestPath = join(vaultPath, '.obsidian', 'community-plugins.json');
  try {
    const raw = readFileSync(manifestPath, 'utf-8');
    return JSON.parse(raw) as string[];
  } catch {
    return [];
  }
}

const plugins = getInstalledPlugins('/path/to/vault');
console.log('Installed plugins:', plugins);
```

#### Via CDP Eval (browser automation)

If you are controlling Obsidian through a browser/CDP session, evaluate inside the app context:

```typescript
const plugins = await page.evaluate(() => {
  // @ts-ignore
  return app.plugins.enabledPlugins;
});
console.log('Enabled plugins:', Array.from(plugins));
```

### Map Plugins to Visualization Capabilities

```typescript
interface VizCapabilities {
  mermaid: boolean;      // core — always true
  dataview: boolean;
  charts: boolean;
  canvas: boolean;        // core — always true
  excalidraw: boolean;
  pythonPlots: boolean;   // fallback — always possible
}

function detectCapabilities(installed: string[]): VizCapabilities {
  return {
    mermaid: true,
    dataview: installed.includes('dataview'),
    charts: installed.includes('obsidian-charts'),
    canvas: true,
    excalidraw: installed.includes('obsidian-excalidraw-plugin'),
    pythonPlots: true,
  };
}
```

### Capability-to-Snippet Mapping

| Plugin | Visualization Type | Snippet Syntax | Always Available? |
|--------|-------------------|----------------|-------------------|
| (core) | Mermaid diagrams | ````mermaid` code blocks | Yes |
| dataview | Dataview queries | ````dataview` code blocks | No |
| obsidian-charts | Charts.js charts | ````chart` code blocks | No |
| (core) | JSON Canvas | `.canvas` files + `![[note.canvas]]` embed | Yes |
| obsidian-excalidraw-plugin | Excalidraw diagrams | `.excalidraw` files + `![[note.excalidraw]]` embed | No |
| Python + matplotlib | Mathematical/scientific plots | Generate image + `![[image.png]]` embed | Yes (fallback) |

> [!caution]
> If a requested plugin is **not** installed, do not write its code block syntax—it will not render. Fall back to a core feature (Mermaid or Canvas) or generate a Python plot.

---

## 2. Choose Visualization Type

### Quick Visualization Picker

Use this decision tree to pick the right type fast:

| Need | Recommended Type | Plugin Required? | Delegation Skill |
|------|-----------------|------------------|------------------|
| Flowchart, sequence, class, ERD, Gantt, state diagram | Mermaid | No (core) | `mermaid-expert` |
| Free-form whiteboard, sketch-style diagrams | Excalidraw | Yes | `excalidraw-diagram` |
| Visual canvas, mind map, project board, link map | JSON Canvas | No (core) | — |
| Query, list, table, or aggregate vault metadata | Dataview | Yes | — |
| Bar, line, pie, radar, doughnut from inline data | Charts plugin | Yes | — |
| Mathematical functions, scientific plots, heatmaps, precise visualizations | Python + matplotlib | No (fallback) | — |
| Algorithmic / generative art | p5.js / algorithmic art | No (fallback) | `algorithmic-art` |

> [!tip]
> When in doubt, start with **Mermaid**. It is always available, text-based, and version-control friendly.

---

## 3. Write the Snippet

This skill emits minimal working snippets. For full syntax depth, invoke the dedicated skill or read the reference file.

### Mermaid (Core)

```markdown
```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No|  D[Action 2]
```
```

> [!tip] For full Mermaid syntax, invoke the `mermaid-expert` skill.
> See also: [references/mermaid.md](references/mermaid.md)

### Dataview (Plugin)

```markdown
```dataview
TABLE file.name, file.mtime
FROM "Projects"
SORT file.mtime DESC
LIMIT 10
```
```

> [!tip] For advanced Dataview queries and DataviewJS, see [references/dataview.md](references/dataview.md).

### Charts Plugin (Plugin)

```markdown
```chart
 type: bar
 labels: [Jan, Feb, Mar]
 series:
   - title: Revenue
     data: [120, 200, 150]
```
```

> [!tip] For full Chart.js configuration syntax, see [references/charts.md](references/charts.md).

### JSON Canvas (Core)

Create a `.canvas` file, then embed it:

```markdown
![[my-board.canvas]]
```

> [!tip] For the `.canvas` JSON schema, see [references/canvas.md](references/canvas.md).

### Excalidraw (Plugin)

Create a `.excalidraw` file (or let the plugin create one), then embed it:

```markdown
![[my-diagram.excalidraw]]
```

> [!tip] For Excalidraw diagram creation and automation, invoke the `excalidraw-diagram` skill.
> See also: [references/excalidraw.md](references/excalidraw.md)

---

## 4. Embed in Note

- **Code block types** (Mermaid, Dataview, Charts): write directly in the `.md` file as fenced code blocks
- **File types** (Canvas, Excalidraw): create the file, then embed with `![[filename.ext]]`

> [!note]
> Canvas and Excalidraw files are JSON. You can generate them programmatically, but it is often easier to create them inside Obsidian and then embed.

---

## 5. Python-Generated Diagrams (Fallback for Complex Plots)

When Mermaid or Charts cannot render the visualization accurately (e.g., sigmoid function, custom mathematical expressions, scientific plots):

1. **Generate the image** using the helper script:
   ```bash
   python scripts/generate_diagram.py --type sigmoid --output assets/sigmoid.png
   ```
2. **Embed in the note**:
   ```markdown
   ![[assets/sigmoid.png]]
   ```

Common use cases:
- Activation functions: sigmoid, tanh, ReLU
- Custom math expressions: `--expr "np.sin(x) * np.exp(-x/5)"`
- Scatter plots, bar charts, heatmaps from data
- Dark mode: add `--dark` flag

> [!tip] For full Python diagram syntax and examples, see [references/python-diagrams.md](references/python-diagrams.md).

---

## 6. Detecting New / Unfamiliar Plugins

When encountering an unfamiliar visualization plugin:

1. Check the plugin's documentation for its code block language identifier (e.g., ````dataview`) or file extension (e.g., `.canvas`)
2. Determine what data/parameters the plugin expects
3. Write a minimal working example and test it renders in Obsidian
4. Add it to the capability map above so future agents know it exists

> [!note]
> If the plugin is niche and undocumented, fall back to generating a static image or using a core feature.

---

## Quick Reference Checklist

- [ ] Read `.obsidian/community-plugins.json` (or `app.plugins.enabledPlugins`) to detect installed visualization plugins
- [ ] Map installed plugins to capabilities using the table above
- [ ] Use the **Quick Visualization Picker** to choose the right type for the user's need
- [ ] If the required plugin is missing, fall back to **Mermaid**, **Canvas**, or a **Python-generated image**
- [ ] Emit a minimal, valid snippet for the chosen type
- [ ] For deep Mermaid authoring, invoke the `mermaid-expert` skill
- [ ] For deep Excalidraw authoring, invoke the `excalidraw-diagram` skill
- [ ] For algorithmic art, invoke the `algorithmic-art` skill
- [ ] Verify the snippet renders correctly in Obsidian before finalizing

---

## References

- [Mermaid Diagrams](references/mermaid.md) — All diagram types, syntax, Obsidian-specific features
- [Dataview Queries](references/dataview.md) — LIST, TABLE, TASK, CALENDAR, DataviewJS
- [Charts Plugin](references/charts.md) — Chart.js configuration syntax
- [JSON Canvas](references/canvas.md) — `.canvas` file format and embed syntax
- [Excalidraw](references/excalidraw.md) — Diagram creation and embed syntax
- [Python Diagrams](references/python-diagrams.md) — Mathematical functions, scientific plots via matplotlib
