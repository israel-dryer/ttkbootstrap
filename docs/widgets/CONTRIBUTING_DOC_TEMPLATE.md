---
title: Widget Documentation Template
icon: fontawesome/solid/file-lines
---

# Widget Name

Brief, one-paragraph introduction that explains **what this widget is** and where it fits in ttkbootstrap.
Avoid web metaphors; write for desktop UI developers.

<!--
IMAGE: Widget overview
Suggested: Default appearance in light and dark themes
-->

---

## Basic usage

Show the simplest possible working example.

```python
import ttkbootstrap as ttk

app = ttk.App()

# widget example

app.mainloop()
```

---

## What problem it solves

Explain *why* this widget exists and when it is useful.
Avoid implementation details here.

---

## Core concepts

Explain 1–3 important ideas required to use the widget correctly.

---

## Common options & patterns

Document the options users will reach for most often.
Include short examples.

---

## Events

Prefer `on_*` / `off_*` helpers when available.
Avoid raw `bind(...)` unless necessary.

---

## UX guidance

Explain best practices and common mistakes.

!!! tip "UX guidance"
    Include practical advice that helps developers make good UI decisions.

---

## When to use / when not to

**Use this widget when:**
- …

**Avoid this widget when:**
- …

---

## Related widgets

Link to related widgets and explain how they differ.
