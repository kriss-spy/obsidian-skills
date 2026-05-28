# Excalidraw in Obsidian

Requires the **obsidian-excalidraw-plugin** community plugin.

## Creating an Excalidraw Diagram

Create a `.excalidraw` file with JSON structure:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "rect1",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 100,
      "strokeWidth": 2,
      "roughness": 0,
      "opacity": 100,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#e0e0e0",
      "fillStyle": "solid"
    },
    {
      "id": "text1",
      "type": "text",
      "x": 150,
      "y": 130,
      "width": 100,
      "height": 40,
      "text": "Hello World",
      "fontSize": 20,
      "fontFamily": 3,
      "textAlign": "center",
      "verticalAlign": "middle",
      "strokeColor": "#1e1e1e",
      "opacity": 100
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Embedding in Notes

```markdown
![[MyDiagram.excalidraw]]
```

## Element Types

### Rectangle

```json
{
  "id": "rect1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeWidth": 2,
  "roughness": 0,
  "opacity": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent"
}
```

### Ellipse

```json
{
  "id": "ellipse1",
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 100,
  "height": 100,
  "strokeWidth": 2,
  "roughness": 0,
  "opacity": 100
}
```

### Diamond

```json
{
  "id": "diamond1",
  "type": "diamond",
  "x": 100,
  "y": 100,
  "width": 100,
  "height": 100,
  "strokeWidth": 2,
  "roughness": 0,
  "opacity": 100
}
```

### Text

```json
{
  "id": "text1",
  "type": "text",
  "x": 100,
  "y": 100,
  "text": "Label text",
  "fontSize": 16,
  "fontFamily": 3,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e1e1e",
  "opacity": 100
}
```

### Arrow

```json
{
  "id": "arrow1",
  "type": "arrow",
  "x": 0,
  "y": 0,
  "points": [[0, 0], [100, 50]],
  "strokeWidth": 2,
  "roughness": 0,
  "opacity": 100,
  "startArrowHead": null,
  "endArrowHead": "arrow"
}
```

### Line

```json
{
  "id": "line1",
  "type": "line",
  "x": 0,
  "y": 0,
  "points": [[0, 0], [100, 0], [100, 100]],
  "strokeWidth": 2,
  "roughness": 0,
  "opacity": 100
}
```

## Common Settings

| Property | Values | Description |
|----------|--------|-------------|
| `roughness` | `0` (clean), `1` (sketch) | Edge style |
| `strokeWidth` | `1`, `2`, `3` | Line thickness |
| `opacity` | `100` | Always use 100 |
| `fontFamily` | `1` (virgil), `2` (helvetica), `3` (code) | Font style |

## Best Practices

1. Use `roughness: 0` for professional diagrams
2. Use `fontFamily: 3` for clean text
3. Position elements on a grid (multiples of 20)
4. Use arrows to show relationships explicitly
5. Keep diagrams focused -- one concept per file
6. Use descriptive element IDs for maintainability
