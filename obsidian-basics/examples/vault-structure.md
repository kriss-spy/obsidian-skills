# Obsidian Vault Structure Example

This example demonstrates a well-organized Obsidian vault structure.

## Folder Structure

```
Knowledge-Base/
├── .obsidian/                      # Obsidian configuration
│   ├── app.json                    # App settings
│   ├── appearance.json             # Theme settings
│   ├── community-plugins.json      # Community plugins list
│   ├── core-plugins.json           # Core plugins list
│   ├── hotkeys.json                # Keyboard shortcuts
│   ├── templates.json              # Template settings
│   ├── workspace.json              # Workspace layout
│   └── plugins/                    # Plugin files
│       ├── dataview/
│       ├── templater-obsidian/
│       └── obsidian-git/
│
├── 00-Inbox/                       # Capture notes quickly
│   └── (temp files)
│
├── 01-Projects/                    # Active projects
│   ├── Project-Alpha/
│   │   ├── Overview.md
│   │   ├── Requirements.md
│   │   └── Meeting Notes/
│   └── Project-Beta/
│       └── Overview.md
│
├── 02-Areas/                       # Ongoing areas of responsibility
│   ├── Health/
│   ├── Finance/
│   ├── Career/
│   └── Learning/
│
├── 03-Resources/                   # Reference material
│   ├── Books/
│   ├── Articles/
│   ├── Courses/
│   └── Tools/
│
├── 04-Archive/                     # Completed/Inactive
│   ├── 2023-Projects/
│   └── Old Notes/
│
├── 05-Daily/                       # Daily notes
│   ├── 2024/
│   │   ├── 2024-01-15.md
│   │   └── 2024-01-16.md
│   └── 2023/
│
├── Templates/                      # Note templates
│   ├── Daily Note.md
│   ├── Project.md
│   ├── Meeting.md
│   └── Book Review.md
│
├── Attachments/                    # Images, PDFs, etc.
│   ├── Screenshots/
│   ├── Documents/
│   └── Diagrams/
│
└── Home.md                         # Entry point / Dashboard
```

## Configuration Files

### app.json
```json
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "00-Inbox",
  "attachmentFolderPath": "Attachments",
  "showUnsupportedFiles": false,
  "spellcheck": true,
  "spellcheckLanguages": ["en-US"]
}
```

### appearance.json
```json
{
  "theme": "obsidian",
  "accentColor": "#7c3aed",
  "cssTheme": "Minimal",
  "enabledCssSnippets": ["custom-headings"],
  "textFontFamily": "Inter",
  "monospaceFontFamily": "JetBrains Mono"
}
```

### community-plugins.json
```json
[
  "dataview",
  "templater-obsidian",
  "obsidian-git",
  "calendar",
  "periodic-notes",
  "tag-wrangler"
]
```

### core-plugins.json
```json
[
  "graph",
  "backlink",
  "page-preview",
  "note-composer",
  "command-palette",
  "editor-status",
  "starred",
  "outline",
  "word-count"
]
```

## Example Notes

### Home.md (Dashboard)
```markdown
# Knowledge Base

## Quick Links
- [[Project-Alpha]]
- [[Daily Notes]]
- [[Books]]

## Active Projects
```dataview
LIST
FROM "01-Projects"
WHERE status = "active"
SORT file.name ASC
```

## Recent Daily Notes
```dataview
LIST
FROM "05-Daily"
SORT file.name DESC
LIMIT 5
```

## Tags
- #project
- #area
- #resource
- #daily
```

### Templates/Daily Note.md
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
week: <% tp.date.now("W") %>
---

# <% tp.date.now("YYYY-MM-DD") %> - <% tp.date.now("dddd") %>

## Morning
- [ ] 

## Afternoon
- [ ] 

## Evening
- [ ] 

## Notes

## Tomorrow's Priorities
1. 
2. 
3. 
```

### Templates/Meeting.md
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
time: <% tp.date.now("HH:mm") %>
attendees: 
---

# <% tp.file.title %>

## Attendees
- 

## Agenda
1. 
2. 
3. 

## Discussion

## Action Items
- [ ] 
- [ ] 

## Next Meeting
- Date: 
- Topics: 
```

## Best Practices

1. **PARA Method** - Projects, Areas, Resources, Archive
2. **Daily Notes** - Date-based notes in YYYY-MM-DD format
3. **Templates** - Consistent structure for common note types
4. **Links** - Use wiki-links to connect related notes
5. **Tags** - Supplement links with tags for discoverability
