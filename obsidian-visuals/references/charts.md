# Charts Plugin in Obsidian

Requires the **obsidian-charts** community plugin. Creates Chart.js-based charts from YAML-like syntax.

## Code Block Syntax

````markdown
```chart
type: bar
title: "Monthly Revenue"
labels:
  - Jan
  - Feb
  - Mar
series:
  - title: "Revenue"
    data:
      - 12000
      - 15000
      - 18000
```
````

## Chart Types

### Bar Chart

```chart
type: bar
title: "Sales by Product"
labels:
  - Product A
  - Product B
  - Product C
series:
  - title: "Q1"
    data: [100, 200, 150]
  - title: "Q2"
    data: [120, 180, 170]
```

### Line Chart

```chart
type: line
title: "Website Traffic"
labels:
  - Mon
  - Tue
  - Wed
  - Thu
  - Fri
series:
  - title: "Visitors"
    data: [500, 700, 650, 800, 900]
    borderColor: "rgb(75, 192, 192)"
```

### Pie Chart

```chart
type: pie
title: "Budget Allocation"
labels:
  - Marketing
  - Engineering
  - Operations
data: [30, 50, 20]
```

### Doughnut Chart

```chart
type: doughnut
title: "Task Status"
labels:
  - Done
  - In Progress
  - Todo
data: [15, 8, 22]
```

### Polar Area Chart

```chart
type: polarArea
title: "Skill Levels"
labels:
  - JavaScript
  - Python
  - Design
  - DevOps
data: [80, 70, 60, 50]
```

### Radar Chart

```chart
type: radar
title: "Performance Review"
labels:
  - Quality
  - Speed
  - Communication
  - Leadership
  - Innovation
series:
  - title: "Current"
    data: [8, 7, 9, 6, 8]
  - title: "Target"
    data: [9, 8, 9, 8, 9]
```

### Scatter Chart

```chart
type: scatter
title: "Height vs Weight"
xLabel: "Height (cm)"
yLabel: "Weight (kg)"
series:
  - title: "People"
    data:
      - [170, 70]
      - [180, 80]
      - [165, 60]
```

### Bubble Chart

```chart
type: bubble
title: "Market Analysis"
series:
  - title: "Products"
    data:
      - {x: 10, y: 20, r: 5}
      - {x: 15, y: 10, r: 8}
```

## Common Options

```chart
type: bar
title: "Chart Title"
width: 600
height: 400
colors:
  - "rgb(255, 99, 132)"
  - "rgb(54, 162, 235)"
  - "rgb(255, 206, 86)"
```

### Animation

```chart
type: line
title: "Animated"
animation: true
```

### Legend Position

```chart
type: pie
title: "With Legend"
legendPosition: "bottom"
labels: [A, B, C]
data: [30, 40, 30]
```

### Fill Area (Line/Area)

```chart
type: line
title: "Area Chart"
fill: true
labels: [Jan, Feb, Mar]
series:
  - title: "Sales"
    data: [10, 20, 15]
    fill: true
```

## Multi-Series Example

```chart
type: bar
title: "Revenue vs Cost"
labels:
  - Q1
  - Q2
  - Q3
  - Q4
series:
  - title: "Revenue"
    data: [50, 60, 70, 80]
    borderColor: "rgb(75, 192, 192)"
    backgroundColor: "rgba(75, 192, 192, 0.5)"
  - title: "Cost"
    data: [30, 35, 40, 45]
    borderColor: "rgb(255, 99, 132)"
    backgroundColor: "rgba(255, 99, 132, 0.5)"
```

## Best Practices

1. Use `bar` for categorical comparisons
2. Use `line` for trends over time
3. Use `pie`/`doughnut` only for ≤5 categories
4. Use `scatter` for correlation analysis
5. Keep colors consistent across related charts
6. Add descriptive titles
7. Use `width`/`height` for layout control
