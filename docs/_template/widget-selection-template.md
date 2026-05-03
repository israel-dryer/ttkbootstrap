---
title: WidgetName
---

# WidgetName

1–2 paragraphs that say:

- what kind of selection this is (boolean, mutually-exclusive, set,
  list-of-one, list-of-many)
- what value type it produces (`bool`, `str`, `set[str]`, ...) and
  how that value is committed
- a comparison sentence if useful ("Unlike Switch...", "Like
  RadioGroup but...")

The intro carries the "what is this" framing — there's no separate
`Framework integration` lead. Its content distributes into Common
options (theme tokens, items, on/off values), Behavior (selection
model, keyboard, popup), and Events (`command`, signal, virtual
events).

---

## Basic usage

One minimal, runnable example showing the widget producing its
typical value.

```python
import ttkbootstrap as ttk

# minimal, copy/paste runnable
```

If the widget supports multiple variants (checkbox / toggle, radio /
button-radio), show only the primary form here.

---

## Selection model

How the widget represents its selected state — the central concept
for any selection control:

- **Value type** — what the bound variable / signal holds (`bool`,
  the `onvalue`/`offvalue` strings, the chosen item, a `set` of
  selected items)
- **Independent vs mutually-exclusive** — does this widget stand
  alone (CheckButton), participate in a one-of-many group sharing a
  variable (RadioButton), or own its own group (RadioGroup,
  SelectBox)?
- **Initial state** — what `value=` does at construction, and how it
  interacts with `signal=` / `variable=` (does the bound variable
  win?  does `value=` clobber it?)
- **Indeterminate / empty / no-selection** — is there a third state
  (tri-state checkbox, "nothing selected" in a SelectBox)?  How is
  it reached, and is it reachable post-construction?
- **Commit semantics** — when does the bound state actually change?
  (click, programmatic `set()`, popup close, Enter)

Include a short example that shows the model — typically the
selection round-trip (read current → set new → observe change).

---

## Common options

Curated — what users actually configure. Selection widgets typically
expose:

- `text` (label or per-item text)
- `value` (initial selected value)
- `onvalue` / `offvalue` (boolean controls)
- `items` (list-based controls)
- `signal=` / `variable=` (state binding)
- `command=` (user-invocation callback)
- `accent`, `variant`, `surface`, `density` (theme tokens)
- `state` (`normal` / `disabled` / `readonly`)
- widget-specific options (`allow_custom_values`, `search_mode`,
  `multiselect`)

Theme tokens, density, and per-item visual options live here — no
separate `Appearance` section. Show short representative examples
per concern; this is not an API dump.

---

## Behavior

Interaction and presentation rules:

- **User input** — click / Space / Enter; per-platform conventions
  (e.g. radio arrow keys); whether typing is captured (search /
  type-to-select)
- **Keyboard contract** — focus-vs-selection (does Tab move focus
  without changing selection?); group navigation for radio-style
  controls; Escape semantics for popup controls
- **Popup behavior** (dropdown / combobox controls) — open / close
  triggers, focus capture, what dismisses without committing
- **Group behavior** (radio controls) — how widgets sharing a
  variable coordinate, what happens when no member is selected at
  startup
- **Disabled / readonly** — what input paths are blocked, whether
  the variable can still be written programmatically, what the
  visual state looks like
- **Reconfiguration** — which options take effect immediately
  (`state`, `accent`) vs require reconstruction (variant, items list
  for some controls)
- **Visual states** — `hover`, `focus`, `selected`, `pressed`,
  `disabled`, `alternate` (indeterminate)

---

## Events

Document the event surface — the `command=` callback, signal /
variable observation, and any virtual events.

For each:

- when it fires (user-invocation only, every variable write,
  popup-close)
- the payload (no args, the new value, an event object)
- whether it round-trips (does programmatic `set()` re-fire the
  same callback as a click?)

```python
def on_changed(value):
    ...

widget.signal.subscribe(on_changed)
```

If the widget has *no* virtual events and *no* `on_*` helpers,
include a deliberate negative `Events` section pointing readers at
`command=`, `signal.subscribe(...)`, or `variable.trace_add(...)`
instead, so they don't go looking for hooks that don't exist.

---

## When should I use WidgetName?

Use WidgetName when:

- ...

Prefer OtherWidget when:

- ...

This sits near the bottom on purpose: readers reach it after they've
seen what the widget does and how it's configured, so the
recommendation lands with context.

---

## Related widgets

- **OtherSelectionWidget** — alternative selection pattern
- **GroupingWidget** — manages multiple of these as one control
- **Form** — bundles fields with validation and layout

---

## Reference

- **API reference:** `ttkbootstrap.WidgetName`
- **Related guides:** Selection, Forms, Localization
