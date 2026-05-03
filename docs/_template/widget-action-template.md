---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what action this widget triggers or represents
- where it's commonly used (dialogs, toolbars, menus, forms)
- a comparison sentence if useful ("Unlike X…", "Similar to Y…")

The intro carries the "what is this" framing — there's no separate
`Framework integration` lead. Its content distributes into Common
options (theme tokens, icons), Behavior (keyboard, focus, disabled),
Events (command, virtual events), and Localization & reactivity.

---

## Basic usage

One minimal, runnable example showing the core interaction.

```python
import ttkbootstrap as ttk

# minimal, copy/paste runnable
```

---

## Common options

Curated — what users actually configure. Action widgets typically
have a small but loaded option set:

- `text`, `icon`, `compound`
- `accent`, `variant` (semantic color + treatment)
- `density` (size variants)
- `state` (`normal` / `disabled`)
- `command`
- widget-specific essentials

Theme tokens, accent/variant combinations, icon-only vs icon+text,
and density variants live here — no separate `Appearance` section.
Show short representative examples per concern; this is not an API
dump.

---

## Behavior

Interaction rules:

- keyboard bindings (Space, Return)
- focus and tab order
- hover/pressed/disabled visual states
- `state(...)` semantics
- open/close rules for menu-like actions
- `command` invocation timing (on press, on release, on Enter)

If the widget has a popup or composes with a menu, describe the
open/close lifecycle here.

---

## Events

The hooks for reacting to user action:

- the `command` callback (the canonical action hook)
- virtual events the widget emits (e.g. `<<MenuOpen>>`)
- payload shape if applicable

```python
def handle():
    ...

widget = ttk.Widget(app, command=handle)
```

---

## Patterns

*Optional — include only when the widget has real composition
patterns to show (icon-only buttons, button groups, inline toolbars,
dynamic enable/disable).*

Skip for widgets whose API is fully covered by Common options +
Behavior + Events.

---

## Localization & reactivity

How the widget participates in:

- locale-aware text updates (signal-bound text, `MessageCatalog`)
- reactive command bindings (signal-driven enable/disable)

Link out to:

- [Signals & Events](../capabilities/signals/index.md)
- [Localization](../capabilities/localization.md)

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
- **Related guides:** …
