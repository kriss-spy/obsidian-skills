---
name: obsidian-visuals
description: Enable agents to detect installed Obsidian visualization plugins and write correct embeddable chart/diagram snippets in markdown notes. Use when creating diagrams, charts, or data visualizations in Obsidian notes, or when the user asks to visualize vault data, create Mermaid diagrams, Dataview queries, Charts plugin blocks, Canvas files, or Excalidraw diagrams.
---

# Obsidian Visuals

Help agents understand which visualization types are available in the current vault and write correct, renderable snippets embedded in Obsidian markdown notes.

## Workflow

### 1. Detect Available Visualizations

Run `obsidian plugins` to get installed plugins. Map plugins to visualization capabilities:

| Plugin | Visualization Type | Snippet Syntax |
|--------|-------------------|----------------|
| (core) | Mermaid diagrams | ````mermaid` code blocks |
| dataview | Dataview queries | ````dataview` code blocks |
| obsidian-charts | Charts.js charts | ````chart` code blocks |
| (core) | JSON Canvas | `.canvas` files + `![[note.canvas]]` embed |
| obsidian-excalidraw-plugin | Excalidraw diagrams | `.excalidraw` files + `![[note.excalidraw]]` embed |
| Python + matplotlib | Mathematical/scientific plots | Generate image + `![[image.png]]` embed |

If a plugin is not listed, the agent can still write Mermaid and Canvas (core Obsidian features).

### 2. Choose Visualization Type

Match the user's intent to the right type:

| Need | Recommended Type |
|------|-----------------|
| Software diagrams (flow, sequence, class, ERD) | Mermaid |
| Query/list/aggregate vault data | Dataview |
| Data charts (bar, line, pie, etc.) from inline data | Charts plugin |
| Visual canvas, mind map, project board | JSON Canvas |
| Free-form whiteboard diagrams | Excalidraw |
| Math functions, scientific plots, precise visualizations | Python + matplotlib |

### 3. Write the Snippet

Use the correct syntax for the chosen type. See references below for each type's syntax and examples.

### 4. Embed in Note

- **Code block types** (Mermaid, Dataview, Charts): write directly in the `.md` file as fenced code blocks
- **File types** (Canvas, Excalidraw): create the file, then embed with `![[filename.ext]]`

### 5. Python-Generated Diagrams (Fallback for Complex Plots)

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

See [Python Diagrams](references/python-diagrams.md) for full syntax and examples.

## Detecting New Plugins

When encountering an unfamiliar visualization plugin:

1. Check the plugin's documentation for its code block language identifier (e.g., ````dataview`) or file extension (e.g., `.canvas`)
2. Determine what data/parameters the plugin expects
3. Write a minimal working example and test it renders in Obsidian

## References

- [Mermaid Diagrams](references/mermaid.md) - All diagram types, syntax, Obsidian-specific features
- [Dataview Queries](references/dataview.md) - LIST, TABLE, TASK, CALENDAR, DataviewJS
- [Charts Plugin](references/charts.md) - Chart.js configuration syntax
- [JSON Canvas](references/canvas.md) - `.canvas` file format and embed syntax
- [Excalidraw](references/excalidraw.md) - Diagram creation and embed syntax
- [Python Diagrams](references/python-diagrams.md) - Mathematical functions, scientific plots via matplotlib
