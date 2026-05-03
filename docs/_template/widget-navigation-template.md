---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what kind of navigation surface this is (tab bar, side rail,
  toolbar, app shell, page-stack-with-chrome)
- whether navigation is **random-access** (tabs, side nav) or
  **sequential** (wizard, page stack history)
- whether the widget owns content panes (tab + page coupling) or is
  pure chrome that drives external content

The intro carries the "what is this" framing — there's no separate
`Framework integration` lead. Its content distributes into Common
options (variants, orientation, density), Behavior (selection model,
keyboard, history), and Events (selection-change, close, add).

---

## Basic usage

One minimal, runnable example showing the widget driving navigation.

```python
import ttkbootstrap as ttk

# minimal, copy/paste runnable
```

If the widget supports multiple variants or orientations (bar / pill,
horizontal / vertical), show only the primary form here.

---

## Navigation model

How navigation targets are addressed and how state moves between them:

- how items are added (`add()`, `add_page()`, etc.) and what keys /
  iids identify them
- random-access vs sequential semantics (a tab bar lets users jump;
  a page stack pushes/pops)
- whether selection is reactive (signal / variable) or imperative
  (`set(key)`)
- page lifecycle if the widget owns content panes (created on
  `add()`, mounted on selection, kept around vs destroyed on close)
- whether navigation history is preserved (back/forward) or
  forgotten (active-only)

Include a short example that shows the model — typically the
selection round-trip (read current → set new → observe change).

---

## Common options

Curated — what users actually configure. Navigation widgets typically
expose:

- `variant` (`bar` / `pill`, `compact` / `extended`, …)
- `orient` (`horizontal` / `vertical`)
- `accent`, `surface`, `density`, `show_border` (theme tokens)
- per-item appearance (`tab_width`, `icon_only`, badge support)
- toggles for the affordance set (`enable_closing`,
  `enable_adding`, `enable_reordering`)

Theme tokens, density, and per-item visual options live here — no
separate `Appearance` section. Show short representative examples
per concern; this is not an API dump.

---

## Behavior

Interaction and presentation rules:

- selection model — single-select vs none-allowed, default selection,
  programmatic `set()` paths and what they emit
- keyboard contract (Tab / arrows / Home / End, focus-vs-selection)
- mouse contract (click to select, middle-click to close, drag to
  reorder if supported)
- close / add / drag affordances and the events they generate
- disabled state — what `state(["disabled"])` does to selection,
  what `configure_item(key, state="disabled")` skips
- coupling to content (does selecting a tab show its page? does the
  widget own the page-stack or just emit events?)
- visual states (`hover`, `focus`, `selected`)

---

## Events

Document the event surface — both raw virtual events and the
`on_*`/`off_*` helpers when present.

For each event:

- when it fires
- the payload (`event.data` shape)
- whether it round-trips (does `set(key)` re-fire the change event?)

```python
def on_changed(event):
    ...

nav.on_tab_changed(on_changed)
```

If the widget has *no* virtual events and *no* `on_*` helpers,
include a deliberate negative `Events` section pointing readers at
`signal.subscribe(...)` or `variable.trace_add(...)` instead, so they
don't go looking.

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

- **OtherNavigationWidget** — alternative navigation pattern
- **ContentWidget** — the typical pane that the navigation drives
- **ActionWidget** — triggers used alongside navigation chrome

---

## Reference

- **API reference:** `ttkbootstrap.WidgetName`
- **Related guides:** Navigation, Layout, Design System
