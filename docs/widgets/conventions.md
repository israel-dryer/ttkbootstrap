---
title: Widget docs conventions
icon: fontawesome/solid/book
---

# Widget docs conventions

This section standardizes widget documentation so every page is easy to scan and consistent.

---

## Imports and application setup

All examples use the public API:

```python
import ttkbootstrap as ttk

app = ttk.App()
```

Widgets are constructed from `ttk.*` (no deep imports) unless a page is explicitly documenting internals.

---

## Page structure

Every widget page follows this order:

1. **What it is** — plain-language description
2. **Basic usage** — smallest runnable snippet
3. **Key behaviors** — the features users need to understand (states, selection, scrolling, etc.)
4. **Styling** — `bootstyle` tokens and common variants (when applicable)
5. **Events** — `command=` and/or semantic events, plus any `on_*` helpers
6. **When to use** — recommended usage and alternatives
7. **Related widgets** — links to adjacent concepts

---

## Front matter

Each page includes a title and icon:

```yaml
---
title: Button
icon: fontawesome/solid/square
---
```

Icons should come from **Font Awesome Free (Solid)**.

---

## Code examples

- Keep examples runnable.
- Prefer small, focused snippets over large blocks.
- Use `fill="x"` and `padx/pady` to show typical layouts.
- If an API may vary, call it out explicitly and keep the example conceptual.

---

## Image placeholders

Use placeholders until you have real screenshots:

> _Image placeholder:_  
> Screenshot of Button showing default/hover/pressed/disabled states.

When you add real images, use theme-appropriate screenshots (and show light/dark when it matters).

---

## Naming

- Widget names use **PascalCase** (matches class names).
- Section headings use sentence case.
- Use the docs categories (Controls/Data Display/Feedback/Layout/Views/Menus/Tk Widgets) consistently.
