---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what kind of layout or structural widget this is (container,
  divider, layout primitive)
- whether it is **interactive** (user can resize, expand, scroll) or
  **purely structural** (no behavior beyond geometry)
- a comparison sentence if useful ("Unlike X…", "Similar to Y…")

The intro carries the "what is this" framing — there's no separate
`Framework integration` lead. Its content distributes into Common
options (theme tokens, padding, surfaces), Behavior (resize,
propagation, child management), and Events (`<Configure>`, virtual
events for interactive layouts).

---

## Basic usage

One minimal, runnable example showing the widget in a layout.

```python
import ttkbootstrap as ttk

# minimal, copy/paste runnable
```

If the widget supports multiple orientations or modes (horizontal vs
vertical, expanded vs collapsed), show only the primary mode here.

---

## Layout model

*Optional — include for widgets with non-trivial layout semantics
(PackFrame's `gap`/`orient`, GridFrame's `columns`/`rows`,
Accordion's expand/collapse, PanedWindow's sashes,
ScrollView's viewport). Skip for plain containers like Frame, Card,
LabelFrame, Separator, Sizegrip — they're transparent to layout.*

Describe how the widget arranges its children (or itself):

- geometry it imposes on children (auto-pack, auto-grid, manual)
- propagation rules (does the widget size to its content?)
- orientation, axis, or directional semantics
- the relationship to standard geometry managers (`pack`, `grid`,
  `place`)

Include one concise example illustrating the model.

---

## Common options

Curated — what users actually configure. Layout widgets typically
expose a small but distinctive option surface:

- `padding`, `width`, `height`
- `accent`, `variant`, `surface`, `show_border` (theme tokens)
- `orient`, `gap`, `columns` (layout-shaping options where applicable)
- `style` (explicit ttk style override)

Theme tokens, surface coloring, borders, and density live here — no
separate `Appearance` section. Show short representative examples
per concern; this is not an API dump.

---

## Behavior

Interaction and presentation rules:

- resize behavior and geometry propagation
- how the widget treats its children (manual vs automatic placement)
- click / drag / keyboard interactions for interactive layouts
  (PanedWindow sash drag, Accordion header click, Expander toggle)
- visual states (`hover`, `active`, `disabled`) where applicable
- non-interactive nature, when relevant — state it explicitly so
  readers don't go looking for hooks that don't exist

If the widget composes with scrollbars, popups, or sub-views,
describe the lifecycle here.

---

## Events

Document the event surface. For purely structural widgets this is
often a deliberate negative ("Frame emits no virtual events"); include
the section anyway so readers don't go looking.

Examples:

- `<Configure>` for resize-driven layout
- virtual events for interactive layouts (`<<TabChanged>>`,
  `<<ExpanderToggled>>`, `<<PanedWindowSashMoved>>`)
- payload shape if applicable

```python
def on_resize(event):
    ...

widget.bind("<Configure>", on_resize)
```

---

## When should I use WidgetName?

Use WidgetName when:

- …

Prefer OtherWidget when:

- …

This sits near the bottom on purpose: readers reach it after they've
seen what the widget does and how it's configured, so the
recommendation lands with context.

---

## Related widgets

- **OtherWidget** — how it differs
- **AnotherWidget** — complementary role

---

## Reference

- **API reference:** `ttkbootstrap.WidgetName`
- **Related guides:** Layout, Design System
