---
name: obsidian-add-knowledge
description: "Reconcile new knowledge with an Obsidian vault before writing it. Use when the user provides text, a URL, or a topic to add to their vault, or when another skill needs to capture sourced knowledge without creating duplicate or misplaced notes."
---

# Obsidian Add Knowledge

**Reconcile** incoming knowledge with the live vault before writing. Prefer extending the right note over creating another note about the same concept.

## Steps

### 1. Distill the payload

Identify the subject, content type, useful claims, source, and likely related concepts. If the input is a URL, extract its substantive content and retain the URL for attribution.

**Complete when:** the subject and content type are explicit, and every externally sourced claim has a source to cite.

### 2. Reconcile with existing notes

Search note names and contents using several distinctive terms, including aliases and broader concepts. Read the strongest candidates rather than deciding from filenames alone.

Choose one outcome:

- **Update** when an existing note owns the same concept.
- **Create** when the concept is independently useful and no existing note owns it.
- **Ask** when the input is too ambiguous to choose safely.

**Complete when:** the strongest candidates have been inspected and the update-or-create decision cites that evidence.

### 3. Inspect the neighborhood

For a new note, discover candidate locations from the vault's actual structure, navigation notes, and nearby examples. List each candidate folder and inspect representative files.

Treat a folder with a strong repeated content type as a **dedicated neighborhood**. Place the note there only when its content type matches. Prefer the vault's established taxonomy over a generic taxonomy or a fixed depth target.

Choose the narrowest existing neighborhood that can also accommodate plausible sibling notes. Introduce a new category folder only when those siblings make the category useful now.

**Complete when:** the proposed parent exists or its new category is justified, its contents were inspected, and the payload matches the neighborhood's organizing principle.

### 4. Propose the change

Before any write, present:

- The exact target path
- Whether the operation updates or creates
- A compact outline or patch preview
- Why this note owns the concept and why the location fits
- Any source attribution and useful WikiLinks

Ask for confirmation. A path or format explicitly supplied by the user still requires a preview, but not a competing location search unless it conflicts with the vault.

**Complete when:** the user has approved the exact target and substance of the change.

### 5. Write atomically

Apply only the approved change using the vault's preferred editing tool. Preserve local frontmatter, heading, naming, and link conventions. Add source attribution for external material and link only clearly related existing notes.

If approval changes the target or scope, return to the relevant earlier step rather than carrying stale assumptions forward.

**Complete when:** the approved knowledge exists once, in the approved note, without unrelated edits.

### 6. Verify

Read the edited note and check its links or metadata when supported. Report the final path and whether the note was created or updated.

**Complete when:** the saved content, path, and links match the approved proposal, or any verification failure is reported plainly.

## Placement Heuristics

Classify by what the knowledge **is**, not words that happen to occur in it. A company's model release may belong with industry products; a model architecture may belong with technical model notes; a library may belong with tools. Resolve uncertain ownership by comparing neighboring notes.

Depth is evidence, not a goal. Use enough hierarchy to express the vault's taxonomy, but do not manufacture folders merely to reach a preferred depth.

## Hard Gate

User confirmation separates investigation from mutation. Stop after the proposal until the user confirms the exact target and substance.
