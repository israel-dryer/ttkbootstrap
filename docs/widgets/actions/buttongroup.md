---
title: ButtonGroup
---

# ButtonGroup

A `ButtonGroup` arranges related buttons into a single connected
cluster — a toolbar segment, an action bar, an inline command row.
Buttons share a uniform style and sit flush against each other so the
group reads as one unit.

`ButtonGroup` is purely a layout and styling container — it does **not**
track which button is "selected." For single- or multi-selection, use
[ToggleGroup](../selection/togglegroup.md) or [RadioGroup](../selection/radiogroup.md)
instead.

<figure markdown>
![buttongroup](../../assets/dark/widgets-buttongroup.png#only-dark)
![buttongroup](../../assets/light/widgets-buttongroup.png#only-light)
</figure>

---

## Basic usage

Create a group, then call `add()` for each action.

```python
import ttkbootstrap as ttk

app = ttk.App()

bg = ttk.ButtonGroup(app, accent="primary")
bg.pack(padx=20, pady=20)

bg.add(text="Cut", command=lambda: print("Cut"))
bg.add(text="Copy", command=lambda: print("Copy"))
bg.add(text="Paste", command=lambda: print("Paste"))

app.mainloop()
```

`add()` returns the created widget, so it can also be captured for
later configuration:

```python
save_btn = bg.add(text="Save", command=on_save)
```

---

## Common options

| Option | Purpose |
|---|---|
| `accent` | Default accent for every child. Children inherit unless they override at `add()` time. |
| `variant` | Default variant (`solid` / `outline` / `ghost` / `link` / `text`). |
| `density` | `default` or `compact`. Enforced uniformly across children. |
| `surface` | Optional surface token; otherwise inherits from the parent. |
| `orient` | `horizontal` (default) or `vertical`. |
| `padding` | Padding around the group; default `1`. |
| `width` / `height` | Optional fixed footprint. |
| `state` | Setting `state="disabled"` on the group disables every child at once. |

`ButtonGroup` itself has no `command` or `textsignal` — those live on
the individual children. Position styling (rounded ends on first/last,
square middles) is managed automatically as buttons are added or
removed.

### Accent and variant

`accent` and `variant` set the default for every child. Children
inherit them — but a child can override either at `add()` time.

```python
ttk.ButtonGroup(app, accent="primary").pack(pady=4)
ttk.ButtonGroup(app, accent="primary", variant="outline").pack(pady=4)
ttk.ButtonGroup(app, accent="primary", variant="ghost").pack(pady=4)
```

!!! link "See [Design System → Variants](../../design-system/variants.md) for how accents and variants compose across widgets."

### Density

`density="compact"` reduces padding inside every child for dense
toolbars. The group enforces uniform density even if a child tries to
set its own.

```python
ttk.ButtonGroup(app, accent="secondary", density="compact").pack(pady=4)
```

### Orientation

Set `orient="vertical"` for a stacked column. Position styling adapts
automatically — the top child gets rounded top corners, the bottom
gets rounded bottom corners.

```python
ttk.ButtonGroup(app, accent="primary", orient="vertical").pack()
```

### Looking up children by key

Pass `key=` to give a child a stable identifier; otherwise one is
auto-generated. The key works with `item()`, `configure_item()`, and
`remove()`.

```python
bg = ttk.ButtonGroup(app, accent="primary")
bg.pack()

bg.add(text="Save", key="save", command=on_save)
bg.add(text="Discard", key="discard", command=on_discard)

# disable just the Save button
bg.configure_item("save", state="disabled")

# look it up directly
save_btn = bg.item("save")
```

`ButtonGroup` is also iterable and supports `len()` and `in`:

```python
for btn in bg:
    btn.configure(state="normal")

if "save" in bg:
    ...
```

### Mixing widget types

`add()` defaults to `Button`, but `widget_type=` accepts any compatible
class — useful when one slot in a toolbar should be a check or radio
control. For dedicated single- or multi-selection groups, prefer
[ToggleGroup](../selection/togglegroup.md) or
[RadioGroup](../selection/radiogroup.md), which manage selection state
for you.

```python
bg = ttk.ButtonGroup(app, accent="secondary", variant="outline")
bg.pack(pady=10)

bg.add(text="Bold", widget_type=ttk.CheckButton)
bg.add(text="Italic", widget_type=ttk.CheckButton)
bg.add(text="Underline", widget_type=ttk.CheckButton)
```

---

## Behavior

- **Tab / Shift+Tab** moves focus into and through the group; each
  child is a normal focus stop.
- **Space / Enter** activates the focused child.
- A child disabled directly is skipped during focus traversal; a group
  disabled via `state="disabled"` disables every child.
- Hover, focus, and pressed visuals come from the active theme — no
  extra wiring is required.
- Removing a child via `remove(key)` re-runs position styling so the
  remaining children keep correct end-cap visuals.

### Disabling the whole group

Set `state="disabled"` on the group to disable every child at once.
Re-enable by setting it back to `"normal"`.

```python
bg = ttk.ButtonGroup(app, accent="primary")
bg.pack(pady=10)
bg.add(text="Apply")
bg.add(text="Reset")

bg.configure(state="disabled")  # disables every child
bg.configure(state="normal")    # re-enables them
```

!!! link "See [State & Interaction](../../capabilities/state-and-interaction.md) for focus, hover, and disabled behavior across widgets."

---

## Events

`ButtonGroup` is a container — it has no events of its own. Each child
behaves like a standalone [Button](button.md): pass `command=` per
child, or bind Tk events on `bg.item(key)` for lower-level interactions.

```python
bg = ttk.ButtonGroup(app, accent="primary")
bg.pack()

bg.add(text="Save", key="save", command=on_save)
bg.item("save").bind("<Double-Button-1>", on_save_doubleclick)
```

---

## Patterns

### Icon-only toolbar

Combine `variant="ghost"` with `icon_only=True` for an unobtrusive
icon toolbar.

```python
bg = ttk.ButtonGroup(app, accent="secondary", variant="ghost")
bg.pack(pady=10)

bg.add(icon="undo", icon_only=True, command=lambda: print("Undo"))
bg.add(icon="redo", icon_only=True, command=lambda: print("Redo"))
bg.add(icon="trash", icon_only=True, command=lambda: print("Delete"))
```

!!! link "See [Icons & Imagery](../../capabilities/icons/index.md) for icon sizing, DPI handling, and recoloring behavior."

---

## Localization & reactivity

`ButtonGroup` is a pure container, so localization and reactivity work
on each child independently. A child added with `text="action.save"` is
resolved through the active catalog and updates automatically when the
locale changes; a child added with `textsignal=...` updates when the
signal does.

```python
status = ttk.Signal("Start")

bg = ttk.ButtonGroup(app, accent="primary")
bg.pack()

bg.add(textsignal=status, command=lambda: status.set("Stop"))
bg.add(text="action.cancel", command=app.destroy)
```

!!! link "See [Signals](../../capabilities/signals/index.md) for reactive bindings, and [Localization](../../capabilities/localization.md) for catalogs and locale switching."

---

## When should I use ButtonGroup?

Use `ButtonGroup` when the actions are conceptually a set —
**Cut/Copy/Paste**, **Bold/Italic/Underline**, **Previous/Next**,
**Zoom in/out** — and the visual grouping reinforces that they belong
together.

Prefer a different control when:

- users need to pick one or more options that persist as state → use
  [ToggleGroup](../selection/togglegroup.md) or [RadioGroup](../selection/radiogroup.md).
- the actions are unrelated and should not look connected → use
  separate [Button](button.md) widgets with normal spacing.
- one action has a primary label plus a menu of related variants →
  use [DropdownButton](dropdownbutton.md).

---

## Related widgets

- [Button](button.md) — the standalone widget that lives inside the group.
- [DropdownButton](dropdownbutton.md) — primary action plus a dropdown of related variants.
- [ToggleGroup](../selection/togglegroup.md), [RadioGroup](../selection/radiogroup.md) — connected groups *with* selection state.

---

## Reference

- **API reference:** [`ttkbootstrap.ButtonGroup`](../../reference/widgets/ButtonGroup.md)
- **Related guides:**
    - [Design System → Variants](../../design-system/variants.md)
    - [Design System → Icons](../../design-system/icons.md)
    - [Icons & Imagery](../../capabilities/icons/index.md)
    - [Signals](../../capabilities/signals/index.md)
    - [Localization](../../capabilities/localization.md)
    - [State & Interaction](../../capabilities/state-and-interaction.md)
