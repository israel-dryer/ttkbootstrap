---
title: Expander
---

# Expander

`Expander` is an interactive collapsible container — a clickable
header (icon + title + chevron) on top of a content frame that
shows or hides on toggle. It's a [Frame](frame.md) subclass, so the
outer container picks up the same `surface` / `show_border` /
`input_background` tokens as any other Frame; the styled element
that responds to hover, focus, and selection is the **header**, not
the outer Frame.

A single Expander stands alone as a self-collapsible region. Stack
several together and let an [Accordion](accordion.md) own them when
you want mutual-exclusion semantics.

<figure markdown>
![expander](../../assets/dark/widgets-expander.png#only-dark)
![expander](../../assets/light/widgets-expander.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

exp = ttk.Expander(app, title="Settings")
exp.pack(fill="x", padx=10, pady=5)

content = exp.add()
ttk.CheckButton(content, text="Enable notifications").pack(anchor="w")
ttk.CheckButton(content, text="Dark mode").pack(anchor="w")
ttk.CheckButton(content, text="Auto-save").pack(anchor="w")

app.mainloop()
```

Child widgets go on the frame returned by `add()` (or on the
`expander.content` property). Don't parent them directly on the
Expander itself — that puts them next to the content frame, not
inside it.

---

## Layout model

An Expander has three regions stacked vertically:

1. The **header** — an inner `CompositeFrame` that holds the
   optional icon, the title label, and the chevron toggle button.
   The header is always visible and is what receives clicks, focus,
   and theme styling (hover, selected, pressed).
2. The **content frame** — a plain [Frame](frame.md) below the
   header that hosts the section's children. On collapse it is
   `pack_forget()`-ed; on expand it is re-packed `fill='both',
   expand=True`. The content frame itself is permanent and stays
   addressable as `expander.content` even while collapsed.
3. The **content widget** — what `add()` returns. By default
   `add()` creates a Frame parented on the content frame and packs
   it; you can also pass a pre-built widget via `add(widget=...)`
   to use an existing Frame, GridFrame, etc. as the content.

The chevron sits to the right of the title by default
(`icon_position="after"`); set `icon_position="before"` to flip it
to the left of the title. `icon_position` is construction-only —
there is no configure delegate for it.

```python
exp = ttk.Expander(app, title="Profile")
exp.pack(fill="x", padx=10, pady=5)

# add() with no arguments creates and returns a Frame
form = exp.add(padding=12)
ttk.Label(form, text="Email").pack(anchor="w")
ttk.Entry(form).pack(fill="x")

# add() is idempotent on the no-argument path
assert exp.add() is form
```

`add(widget=existing)` after content already exists raises
`ValueError("Expander already has content.")`. The `add()` path is
write-once for the content widget; rebuild the Expander if you need
to swap it.

---

## Common options

| Option            | Type             | Default | Notes                                                                  |
| ----------------- | ---------------- | ------- | ---------------------------------------------------------------------- |
| `title`           | str              | `""`    | Header text                                                            |
| `icon`            | str \| dict      | `None`  | Optional leading icon (left of the title)                              |
| `expanded`        | bool             | `True`  | Initial expansion state                                                |
| `collapsible`     | bool             | `True`  | If `False`, hides the chevron and ignores header clicks for toggle     |
| `highlight`       | bool             | `False` | Apply ttk `selected` state to the header while expanded                |
| `icon_expanded`   | str \| dict      | `None`  | Chevron icon when expanded; defaults to `chevron-up` size 16           |
| `icon_collapsed`  | str \| dict      | `None`  | Chevron icon when collapsed; defaults to `chevron-down` size 16        |
| `icon_position`   | `"before"\|"after"` | `"after"` | Chevron placement relative to the title (construction-only)        |
| `accent`          | str              | `None`  | Theme accent applied to the **header**, not the outer Frame            |
| `variant`         | str              | `None`  | Header variant: `default` (ghost) or `solid`                           |
| `signal`          | Signal           | `None`  | Reactive signal for radio-style selection (see *Selection model*)      |
| `variable`        | Variable         | `None`  | Tk variable for selection (alternative to `signal`)                    |
| `value`           | Any              | `None`  | Value written to the signal/variable when this Expander is clicked     |

The Frame container also accepts `padding`, `width`, `height`,
`surface`, `show_border`, and `input_background` — see
[Frame](frame.md) for those.

### Header styling vs container surface

`accent` and `variant` are intercepted in `__init__` before they
reach the Frame's bootstyle wrapper, so they style the **header
strip**, not the outer container:

```python
ttk.Expander(app, title="Solid", accent="primary", variant="solid")
# header renders with the solid-primary builder;
# the outer Frame stays at the default content surface.
```

To tint the outer container (the area around the header and
content), use `surface=`:

```python
ttk.Expander(app, title="Card", surface="card", show_border=True)
```

The two are independent: a `surface="card"` Expander with
`accent="success"` paints the container card-colored and the header
success-colored.

When `show_border=True` is passed, the constructor injects
`padding=3` as a default so the 1px border doesn't clip the corners
of the inner header. Override it explicitly if you need different
spacing:

```python
ttk.Expander(app, title="Bordered", show_border=True, padding=8)
```

### Custom chevron icons

`icon_expanded` and `icon_collapsed` accept either an icon-name
string or a full icon spec dict:

```python
ttk.Expander(
    app,
    title="Custom",
    icon_expanded={"name": "dash", "size": 16},
    icon_collapsed={"name": "plus", "size": 16},
)
```

Both are reconfigurable at runtime through
`configure(icon_expanded=...)` / `configure(icon_collapsed=...)`;
the chevron updates immediately if the matching state is currently
visible.

---

## Behavior

**Click target** is the entire header strip — clicking on the icon,
the title text, the chevron, or the empty space between them all
toggle the section. The header takes keyboard focus
(`takefocus=True`), so `<Tab>` walks Expanders in tab order and
`<Return>` / `<space>` toggle the focused one.

**`collapsible=False`** hides the chevron and blocks all expansion or collapse
operations — both the header click and the programmatic `expand()` / `collapse()` /
`configure(expanded=...)` paths become no-ops. Use it to permanently fix the expansion
state in both the UI and code.

**`highlight=True`** keeps the header visually marked as `selected`
(via the inner `CompositeFrame.set_selected`) for as long as the
section is expanded. Combined with `accent` and `variant="solid"`,
this produces a clearly-marked active section in an
[Accordion](accordion.md)-style UI.

**Reconfiguration is broad but not total.** `title`, `icon`,
`collapsible`, `highlight`, `icon_expanded`, `icon_collapsed`,
`expanded`, `value`, `signal`, `variable`, and `compact` are all
delegated through `configure(...)` and `cget(...)`. Construction-
only options are `icon_position` and the Frame-level options
(`surface`, `show_border` etc.) inherited from the parent.

`compact=True` hides the title label and centers the icon (if any)
in the header; useful for collapsed-rail navigation. Toggle it back
to `False` to restore the title.

### Selection model

When you pass `signal=` (preferred) or `variable=` together with
`value=`, the Expander behaves like a radio button:

- Clicking the header writes `value` to the signal/variable and
  fires `<<Selected>>` with `{"value": value}`.
- The `is_selected` property reflects whether the current
  signal/variable value equals this Expander's `value`.
- Multiple Expanders sharing the same signal/variable form a radio
  group — clicking one updates the shared state, and you can read
  `exp.is_selected` to find the active one.

```python
from ttkbootstrap.core.signals import Signal

active = Signal("inbox")

inbox = ttk.Expander(app, title="Inbox", signal=active, value="inbox")
sent  = ttk.Expander(app, title="Sent",  signal=active, value="sent")

inbox.pack(fill="x")
sent.pack(fill="x")

# Read the active section programmatically:
for section in (inbox, sent):
    if section.is_selected:
        print("active:", section.cget("title"))
```

The selection state is **tracked but not visualized
automatically.** The header does not gain the `selected` state when
the signal updates externally — `_update_selection_state` is a
placeholder for a future "nav" style. To get a visual marker today,
either pair `signal=` with `highlight=True` and call
`expander.expand()` from your handler, or bind `<<Selected>>` and
drive `expander._header_frame.set_selected(True)` yourself.

---

## Events

| Event           | Payload (`event.data`)        | Fires on                                           |
| --------------- | ----------------------------- | -------------------------------------------------- |
| `<<Toggle>>`    | `{"expanded": bool}`          | Any state change — click, keyboard, `expand()`, `collapse()`, `toggle()`, `configure(expanded=...)` |
| `<<Selected>>`  | `{"value": Any}`              | Header click when `signal`/`variable` and `value` are configured (and the click writes the new value) |

`<<Toggle>>` is the universal observation hook. `<<Selected>>` only
fires when the Expander is wired into a selection group; a plain
collapsible section never emits it.

```python
def on_toggle(event):
    print(f"Expanded: {event.data['expanded']}")

exp.on_toggled(on_toggle)
```

The helpers are `on_toggled` / `off_toggled` and `on_selected` /
`off_selected`. Both `off_*` helpers accept the bind-id returned by
their `on_*` counterpart, or `None` to unbind every listener for
that event:

```python
bind_id = exp.on_toggled(on_toggle)
exp.off_toggled(bind_id)        # remove this one
exp.off_toggled()               # remove all <<Toggle>> listeners
```

`<<Selected>>` only fires from the click path; setting the bound
signal/variable externally does not re-fire the event on the
Expanders that don't own that value.

### Programmatic control

```python
exp.expand()                   # show the content
exp.collapse()                 # hide the content
exp.toggle()                   # flip current state (no-op if not collapsible)

# configure / cget — the canonical reconfiguration surface
exp.configure(expanded=False)
print(exp.cget("expanded"))    # False

# expand()/collapse() also fire <<Toggle>>; toggle() respects collapsible.
```

`expanded` is **not** a Python attribute on the widget — there's no
`exp.expanded` property. Use `cget("expanded")` to read state and
`configure(expanded=...)` (or `expand()` / `collapse()`) to write
it. `is_selected` and `content` are the only true properties.

---

## When should I use Expander?

Use `Expander` when:

- you have an optional or advanced section that should hide by
  default to reduce visual weight
- screen space is limited and a header-then-detail disclosure is
  more compact than always-visible chrome
- you want a single self-managing collapsible region without
  bringing in [Accordion](accordion.md)'s mutual-exclusion policy

Prefer **[Accordion](accordion.md)** when several sections share a
parent and at most one (or a small set) should be open at a time —
Accordion owns the cross-section coordination so you don't write
toggle handlers by hand.

Prefer **[LabelFrame](labelframe.md)** or **[Frame](frame.md)** when
the section is always visible — the chevron and click handlers add
overhead without payoff.

Prefer **[Notebook](../views/notebook.md)** when content switching
is tab-driven and the user always sees exactly one section at a
time; Notebook tabs replace each other, while Expander headers stay
visible alongside their (collapsed) siblings.

---

## Related widgets

- **[Accordion](accordion.md)** — owns a stack of Expanders with
  mutual-exclusion and an aggregate `<<AccordionChange>>` event
- **[Frame](frame.md)** — parent class; surface/border tokens
  behave identically
- **[LabelFrame](labelframe.md)** — titled bordered group when the
  region never collapses
- **[Notebook](../views/notebook.md)** — tab-driven content
  switching for one-active-at-a-time content
- **[Card](card.md)** — preset Frame with `accent="card"` and
  `show_border=True` for non-collapsible card chrome

---

## Reference

- **API reference:** [`ttkbootstrap.Expander`](../../reference/widgets/Expander.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
