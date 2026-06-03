# CachedMetadata Reference

Source: [Obsidian Developer Docs — CachedMetadata](https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata)

## Overview

Pre-parsed metadata for a single file. Returned by `MetadataCache.getFileCache()` and `MetadataCache.getCache()`.

## Properties

| Property | Type | Description |
|----------|------|-------------|
| `frontmatter?` | `FrontMatterCache` | Parsed YAML frontmatter |
| `frontmatterPosition?` | `Pos` | Position of frontmatter block |
| `frontmatterLinks?` | `FrontmatterLinkCache[]` | Links inside frontmatter |
| `headings?` | `HeadingCache[]` | All headings |
| `links?` | `LinkCache[]` | Internal links `[[...]]` |
| `embeds?` | `EmbedCache[]` | Embed links `![[...]]` |
| `tags?` | `TagCache[]` | Inline tags `#tag` |
| `blocks?` | `Record<string, BlockCache>` | Block references `^id` |
| `sections?` | `SectionCache[]` | Root-level markdown blocks |
| `listItems?` | `ListItemCache[]` | List items |
| `footnotes?` | `FootnoteCache[]` | Footnote definitions |
| `footnoteRefs?` | `FootnoteRefCache[]` | Footnote references |
| `referenceLinks?` | `ReferenceLinkCache[]` | Reference-style links |

## Related Utilities

- `getAllTags(cache)` — Combines frontmatter and inline tags into one array
