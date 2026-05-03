---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what kind of overlay this is (tooltip, toast, popover, banner)
- whether it is **blocking** (steals focus, captures input) or
  **non-blocking** (renders over content, never holds focus)
- how it appears and disappears (hover, click, programmatic, time)
- a comparison sentence if useful ("Unlike a Dialog…", "Similar to
  a Tooltip but…")

The intro carries the "what is this" framing — there's no separate
`Framework integration` lead. Its content distributes into Common
options (theme tokens, content fields, duration), Behavior
(positioning, screen safety, content composition), and Events
(lifecycle hooks, dismiss callbacks).

---

## Basic usage

One minimal, runnable example showing the overlay attached to or
triggered by typical UI.

```python
import ttkbootstrap as ttk

# minimal, copy/paste runnable
```

If the widget supports multiple trigger styles (hover / programmatic
/ click), show only the primary one here.

---

## Lifecycle

How the overlay enters and leaves the screen — the central concept
for any overlay widget:

- **Trigger** — what causes it to appear (hover, programmatic
  `show()`, click, focus event)
- **Visibility** — what keeps it on screen (mouse stays over the
  parent, fixed `duration`, until explicitly hidden)
- **Dismissal** — what causes it to disappear (mouse leaves, timer
  fires, close button, outside click, `hide()` /  `destroy()`)
- **Blocking vs non-blocking** — does it steal focus or capture
  input? Most overlays in this category are non-blocking; if a widget
  *is* blocking, contrast it with a Dialog so readers know which to
  reach for
- **One-shot vs reusable** — does the overlay instance survive
  multiple show/hide cycles, or is each presentation a fresh
  instance?

Include a short example that exercises the lifecycle when it
matters (e.g. programmatic `show()` then `hide()`, or an
`on_dismissed` callback wired to teardown).

---

## Common options

Curated — what users actually configure. Overlay widgets typically
expose:

- content fields (`text`, `title`, `message`, `icon`)
- timing (`delay`, `duration`)
- positioning (`anchor_point`, `window_point`, `auto_flip`,
  `position`)
- theme tokens (`accent`, `variant`, `padding`)
- content layout (`wraplength`, `justify`, `compound`)
- affordances (`show_close_button`, `buttons`, `alert`)

Theme tokens and content composition live here — no separate
`Appearance` section. Show short representative examples per
concern; this is not an API dump.

---

## Behavior

Interaction and presentation rules:

- **Positioning** — relative to the cursor, an anchor widget, or
  the screen; how `auto_flip` keeps the overlay on screen near a
  viewport edge; what happens when the parent is offscreen or
  unmapped
- **Content composition** — how `title` / `message` / `icon` /
  `buttons` combine; what's hidden when a field is unset; whether
  layout adapts to platform (e.g. macOS chromeless vs X11)
- **Focus and input** — non-blocking overlays should never steal
  focus or capture pointer events; if the widget *does* take focus
  in some mode, name it
- **Stacking** — what happens if multiple instances are shown at
  once (do they overlap, queue, or replace each other?)
- **Reconfiguration** — which options take effect on the next
  `show()` vs immediately on a visible overlay

If the widget composes a `Toplevel`, name the windowing flags
(`overrideredirect`, `windowtype`, `topmost`, `alpha`) so readers
know what platform behaviors are inherited.

---

## Events

Document the event surface — both raw virtual events and any
`on_*` callbacks accepted by the constructor or registered after
construction.

For each event or callback:

- when it fires
- the payload (event object, dict, or unwrapped value)
- whether it round-trips (does programmatic `hide()` fire the same
  callback as a user-triggered dismiss?)

```python
def on_dismissed(data):
    ...

widget.configure(on_dismissed=on_dismissed)
```

If the widget has *no* virtual events and *no* `on_*` callbacks,
include a deliberate negative `Events` section pointing readers at
the lifecycle methods (`show()` / `hide()` / `destroy()`) so they
don't go looking for hooks that don't exist.

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

- **OtherOverlayWidget** — alternative feedback pattern
- **Dialog** — blocking decision point
- **InlineFeedback** — when the message belongs alongside a control

---

## Reference

- **API reference:** `ttkbootstrap.WidgetName`
- **Related guides:** Feedback, UX Patterns, Design System
