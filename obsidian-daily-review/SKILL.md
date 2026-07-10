---
name: obsidian-daily-review
description: "Conduct an end-of-day review of today's work by triangulating signals in priority order: git commits first, then today's daily note, then vault exploration if the picture is still thin. Use when the user asks for a daily review, EOD wrap-up, end-of-day summary, what they did today, or wants to reflect on the day and plan tomorrow."
triggers:
  - obsidian daily review
  - end of day review
  - eod summary
  - what did I do today
  - daily wrap up
  - obsidian daily reflection
author: OpenCode
version: 1.0.0
created: 2026-07-10
---

# Obsidian Daily Review

Review today's work by reading signals in priority order and stopping when the day is legible.

## Signal hierarchy

A **signal** is a timestamped, attributable trace of work. Read them in this order, dropping to the next only when the current one is missing or too thin to answer "what did I work on today?" and "what should I carry forward?".

1. **Git** — the strongest signal. Objective, time-stamped, and tied to actual file changes.
2. **Today's daily note** — the user's own narrative, intentions, and self-reported blockers.
3. **Vault exploration** — inference from files modified today, new notes, and recent project notes.

## Steps

### 1. Locate today's sources

Find today's daily note using the vault's date format. Confirm whether the vault is a git repo.

### 2. Read the strongest signal

If git is present, read git status, today's commits and changed files.

### 3. Read the user's account

Read today's daily note. If it does not exist, use daily note template and create it.

### 4. Triangulate or infer

If the picture from git and the daily note is thin, explore the vault:

- Files modified today
- New notes created today
- Notes linked from today's daily note

### 5. Synthesize and write

- Update today's daily note following the note structure.
- Do not guess and only write clear conclusions.
- Do not create tasks in a daily review.

## Thin-signal handling

- If git has commits today, consider asking the user to do a daily commit before moving to the daily note.
- If no source yields evidence, say so plainly and ask the user what they worked on.
