# Dataview Queries in Obsidian

Requires the **dataview** community plugin.

## Code Block Syntax

````markdown
```dataview
QUERY_TYPE
FROM source
WHERE condition
SORT field ASC/DESC
LIMIT n
```
````

## Query Types

### LIST

Simple list of files:

```dataview
LIST
FROM #project
SORT file.mtime DESC
```

List with custom display:

```dataview
LIST file.mtime AS "Modified"
FROM "Projects"
WHERE status = "active"
```

### TABLE

Table with columns:

```dataview
TABLE file.mtime AS "Modified", status, priority
FROM #task
WHERE !completed
SORT priority ASC
```

### TASK

Task list with filtering:

```dataview
TASK
FROM #project
WHERE !completed
SORT due ASC
```

Group by file:

```dataview
TASK
FROM "Projects"
WHERE !completed
GROUP BY file.link
```

### CALENDAR

Calendar view (requires date field):

```dataview
CALENDAR file.day
FROM #event
```

## Inline Queries

Display computed values inline:

```markdown
Total projects: `=length(filter(file.tasks, (t) => !t.completed))`
Last modified: `=this.file.mtime`
```

## DataviewJS

Full JavaScript queries:

````markdown
```dataviewjs
const pages = dv.pages("#project")
  .where(p => p.status === "active")
  .sort(p => p.file.mtime, "desc")

dv.table(["Name", "Modified"],
  pages.map(p => [p.file.link, p.file.mtime])
)
```
````

### Common DataviewJS Patterns

List files with custom formatting:

```dataviewjs
dv.list(dv.pages("#book").map(b => b.file.link))
```

Task summary:

```dataviewjs
const tasks = dv.pages().file.tasks
dv.paragraph("**Total:** " + tasks.length + " | **Done:** " + tasks.where(t => t.completed).length)
```

Grouped table:

```dataviewjs
dv.table(["Tag", "Count"],
  dv.pages()
    .groupBy(p => p.file.tags)
    .map(g => [g.key, g.rows.length])
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
)
```

## Data Sources

| Source | Syntax |
|--------|--------|
| All files | `FROM ""` or omit FROM |
| By tag | `FROM #tag` |
| By folder | `FROM "Folder"` |
| By link | `FROM [[Note]]` |
| Exclude | `FROM #tag AND -#archived` |
| Regex | `FROM #tag WHERE file.name.match(/pattern/)` |

## Common File Properties

| Property | Description |
|----------|-------------|
| `file.name` | File name |
| `file.path` | Full path |
| `file.folder` | Parent folder |
| `file.mtime` | Modified time |
| `file.ctime` | Created time |
| `file.size` | File size in bytes |
| `file.tags` | List of tags |
| `file.links` | List of outgoing links |
| `file.tasks` | List of tasks |
| `file.frontmatter` | All YAML properties |

## Inline Field Syntax

Define fields in note frontmatter or inline:

```markdown
status:: active
priority:: 1
due:: 2024-12-31
```

Then query them:

```dataview
TABLE status, priority, due
WHERE status = "active"
SORT due ASC
```

## Best Practices

1. Use `LIMIT` on large vaults to prevent slow renders
2. Prefer `LIST` over `TABLE` when only one column needed
3. Use `file.link` instead of `file.name` for clickable links
4. Guard against missing properties: `WHERE field` checks existence
5. For complex logic, use DataviewJS instead of DQL
