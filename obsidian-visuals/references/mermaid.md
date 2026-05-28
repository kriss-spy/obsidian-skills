# Mermaid Diagrams in Obsidian

Mermaid is a **core Obsidian plugin** -- always available. No installation needed.

## Syntax

````markdown
```mermaid
diagramType
  content
```
````

## Diagram Types

### Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant A as User
    participant B as System
    A->>B: Request
    B-->>A: Response
```

### Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +makeSound()
    }
    class Dog {
        +fetch()
    }
    Animal <|-- Dog
```

### ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
```

### Gantt Chart

```mermaid
gantt
    title Project Timeline
    section Phase 1
    Task A :a1, 2024-01-01, 30d
    Task B :a2, after a1, 20d
```

### Pie Chart

```mermaid
pie title Distribution
    "Category A" : 40
    "Category B" : 35
    "Category C" : 25
```

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Done : complete
    Done --> [*]
```

### Git Graph

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
```

## Obsidian-Specific: Linking to Notes

Use `class` to make Mermaid nodes link to Obsidian notes:

```mermaid
graph TD
    A[Start] --> B[Research]
    B --> C[Write]
    class A,B,C internal-link;
```

Or link specific nodes to specific notes:

```mermaid
graph TD
    A[Project Plan] --> B[Tasks]
    classDef link class internal-link;
    class A link;
    class B link;
```

## Configuration

Add a `%%` config block at the top:

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A --> B
```

Available themes: `default`, `forest`, `dark`, `neutral`, `base`

## Best Practices

1. Keep diagrams focused -- one concept per diagram
2. Use meaningful node labels
3. Use `%%` for comments within diagrams
4. Avoid special characters `{}` in labels without quotes
5. For large diagrams, use `flowchart` over `graph` (better layout)
