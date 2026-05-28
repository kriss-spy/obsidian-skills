# JSON Canvas in Obsidian

Canvas is a **core Obsidian feature** -- always available. Creates visual boards with notes, images, and connections.

## Creating a Canvas File

Create a `.canvas` file with JSON structure:

```json
{
  "nodes": [
    {
      "id": "a1b2c3d4e5f67890",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 200,
      "text": "# Title\n\nContent here"
    },
    {
      "id": "b2c3d4e5f6789012",
      "type": "file",
      "x": 500,
      "y": 0,
      "width": 400,
      "height": 300,
      "file": "Notes/Project.md"
    }
  ],
  "edges": [
    {
      "id": "c3d4e5f678901234",
      "fromNode": "a1b2c3d4e5f67890",
      "fromSide": "right",
      "toNode": "b2c3d4e5f6789012",
      "toSide": "left",
      "label": "relates to"
    }
  ]
}
```

## Node Types

### Text Node

```json
{
  "id": "unique16charhex",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Heading\n\nBody text with **markdown**",
  "color": "1"
}
```

### File Node

```json
{
  "id": "unique16charhex",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "path/to/note.md",
  "subpath": "#heading"
}
```

### Link Node

```json
{
  "id": "unique16charhex",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://example.com"
}
```

### Group Node

```json
{
  "id": "unique16charhex",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "Group Label",
  "color": "4"
}
```

## Edge Properties

```json
{
  "id": "unique16charhex",
  "fromNode": "sourceNodeId",
  "fromSide": "right",
  "fromEnd": "arrow",
  "toNode": "targetNodeId",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "1",
  "label": "connection label"
}
```

| Property | Values |
|----------|--------|
| `fromSide` / `toSide` | `top`, `right`, `bottom`, `left` |
| `fromEnd` / `toEnd` | `none`, `arrow` |

## Colors

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

## Embedding in Notes

```markdown
![[MyCanvas.canvas]]
```

## ID Generation

Generate unique 16-character lowercase hex strings:

```bash
openssl rand -hex 8
# or
python -c "import secrets; print(secrets.token_hex(8))"
```

## Layout Guidelines

- Coordinates: `x` increases right, `y` increases down
- Space nodes 50-100px apart
- Align to grid (multiples of 10 or 20)
- Suggested sizes:
  - Small text: 200-300 × 80-150
  - Medium text: 300-450 × 150-300
  - File preview: 300-500 × 200-400

## Use Cases

- Mind maps
- Project planning boards
- Research canvases
- Decision trees
- Concept maps
- Workflow diagrams

## Validation Checklist

1. All `id` values unique across nodes and edges
2. Every `fromNode` / `toNode` references existing node
3. Required fields present for each node type
4. Valid JSON (no unescaped newlines in text)
5. Use `\n` for line breaks in text, not `\\n`
