---
title: SelectBox
---

# SelectBox

`SelectBox` is a field-style dropdown picker built on top of [`Field`](../../reference/widgets/Field.md):
a label, an entry, a message line, and a chevron button that opens a popup list of
items. Selecting an item writes its value into the field and emits `<<Change>>`. With
`enable_search=True` the entry becomes editable and filters the popup list as the user
types; with `allow_custom_values=True` it also accepts arbitrary text outside the list.

The committed value is whatever string sits in the entry — typically one of the strings
in `items`, but the widget does not enforce that. Unlike [OptionMenu](../selection/optionmenu.md),
which renders a raw button + popup menu, `SelectBox` carries the full form-field chrome
(label, message, validation) and supports a typing-to-filter mode.

<!--
IMAGE: SelectBox overview
Suggested: closed state + open popup list
Theme variants: light / dark
-->

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

status = ttk.SelectBox(
    app,
    label="Status",
    items=["New", "In Progress", "Blocked", "Done"],
    value="New",
)
status.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

In the default mode (no search, no custom values), the entry is read-only — clicking
either the entry or the chevron button opens the popup; clicking an item commits it
and closes the popup.

---

## Value model

`SelectBox.value` holds the **currently selected string** — what shows in the entry.
By default it is one of the strings in `items`; with `allow_custom_values=True` it
can also be a free-form string the user typed.

| Concept | Meaning | How to read it |
|---|---|---|
| `value` | The current entry text. Read or written via the property. | `sb.value` |
| `selected_index` | Index of `value` in `items`, or `-1` if not found. | `sb.selected_index` |

```python
sb = ttk.SelectBox(app, items=["Low", "Medium", "High"], value="Medium")
print(sb.value)            # 'Medium'
print(sb.selected_index)   # 1
sb.value = "High"          # commits and emits <<Change>>
```

Setting `selected_index` to a valid integer writes the matching item; setting it to
`None` or `-1` clears the field. Out-of-range integers raise `IndexError`.

### Empty values

With `allow_blank=True` (the default), an empty entry commits as `None`. With
`allow_blank=False`, an empty input is replaced with the previous value on commit.

### Values not in `items`

`SelectBox` does **not** validate writes against `items`. Both the constructor `value=`
and the `sb.value =` setter silently accept any string — the entry shows that string,
`selected_index` returns `-1`, and `<<Change>>` fires as if it were a normal selection.
This is the same shape as [OptionMenu](../selection/optionmenu.md)'s permissive
contract.

!!! warning "Programmatic writes are unconstrained"
    `sb.value = "not_in_items"` succeeds with no exception even when
    `allow_custom_values=False`. Only popup-driven selection is gated by the list. If
    you need strict validation, check `sb.selected_index >= 0` after writes or attach
    a validation rule (see *Validation and constraints*).

### Signals and variables

`SelectBox` exposes the same reactive handles as [TextEntry](textentry.md), bound to
the entry text:

- `sb.signal` — a `Signal[str]`.
- `sb.variable` — a Tk `StringVar`.

Pass your own with `textsignal=` or `textvariable=` to share the field's value with
another widget or to read it reactively.

```python
selection = ttk.Signal("Medium")
sb = ttk.SelectBox(app, items=["Low", "Medium", "High"], textsignal=selection)
selection.subscribe(lambda v: print("selected:", v))
```

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial committed value. Constructor-only — `configure(value=...)` is broken; use `sb.value = ...` instead. |
| `items` | Sequence of strings shown in the popup. Reconfigurable via `configure(items=...)`. |
| `label` | Text shown above the entry. |
| `message` | Helper text below the entry; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `enable_search` | Make the entry editable; typing filters the popup list. |
| `allow_custom_values` | Make the entry editable and allow committing strings outside `items`. Forces the chevron button on. |
| `show_dropdown_button` | Whether to render the chevron button (default `True`). Ignored when `allow_custom_values=True`. |
| `dropdown_button_icon` | Icon name for the chevron button. Default `'chevron-down'`. **Construction-only** — `configure(dropdown_button_icon=...)` raises `TclError`. |
| `accent` | Semantic color token for the focus ring and active border (`primary`, `success`, `danger`, …). Also tints the highlighted item in the popup. |
| `density` | `'default'` or `'compact'` for tight forms. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the entry text. |
| `width` | Width of the entry in characters. |

```python
ttk.SelectBox(app, items=["A", "B"])                              # default
ttk.SelectBox(app, items=["A", "B"], enable_search=True)
ttk.SelectBox(app, items=["A", "B"], allow_custom_values=True)
ttk.SelectBox(app, items=["A", "B"], accent="success")
ttk.SelectBox(app, items=["A", "B"], density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Modes

The combination of `enable_search` and `allow_custom_values` defines four behaviors:

| `enable_search` | `allow_custom_values` | Entry | Popup | Commits |
|---|---|---|---|---|
| `False` | `False` | read-only | click entry or chevron | popup selection only |
| `True` | `False` | editable | click chevron, or focus + type | popup selection, **or** the first filtered item when the popup closes without explicit selection |
| `False` | `True` | editable | click chevron | popup selection, or whatever the user typed |
| `True` | `True` | editable | click chevron | popup selection, the first filter match on close, or arbitrary typed text |

### Popup positioning

The popup is a borderless `Toplevel` placed directly below the entry, matching the
entry's width. When there isn't enough room below the entry on screen, it flips above
— matching Tk's combobox `PlacePopdown` behavior. Maximum popup height is 200px;
overflow scrolls inside the popup.

### Search filtering

With `enable_search=True`, every keystroke filters `items` to the case-insensitive
substrings that match. The filter only narrows visible items; it doesn't reorder or
re-rank them.

When the popup closes without an explicit selection (Escape, Tab to another widget,
click outside), and `allow_custom_values=False`, the **first filtered item** is
committed automatically. This makes a "type the prefix, press Tab" interaction work
without an explicit Enter. With `allow_custom_values=True`, the typed text is kept
verbatim instead.

### Keyboard

When the popup is open:

- **Down / Up** — move the highlight; the popup scrolls to keep the highlighted item visible.
- **Enter** — commit the highlighted item.
- **Tab** — commit the highlighted item (search mode only).
- **Escape** — close the popup without selecting (in search mode, the first filtered item still commits per the rule above).
- **Click outside** — same as Escape.

### Reconfiguration

`configure(items=...)`, `configure(allow_custom_values=...)`, and
`configure(enable_search=...)` all take effect immediately. `configure(value=...)`
does **not** work — set the property (`sb.value = ...`) instead. `dropdown_button_icon`
cannot be reconfigured at all (TclError on attempt).

---

## Events

`SelectBox` reuses the entry's event surface — every event fires on the underlying
`entry_widget`, not on the SelectBox itself. Tk virtual events do not propagate up
the parent chain, so `sb.bind('<<Change>>', cb)` silently no-ops; use the helpers
or bind to `sb.entry_widget` directly.

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | the entry text changes (every keystroke in search/custom mode) | `{'text': str}` |
| `<<Change>>` | `on_changed` | the committed value changes — popup selection, search-filter close, or `sb.value = ...` | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the entry (search/custom mode) | `{'value', 'text'}` |

```python
def on_changed(event):
    print("now:", event.data["value"])

sb = ttk.SelectBox(app, items=["A", "B", "C"])
sb.on_changed(on_changed)
```

`<<Change>>` is suppressed when the new value equals the previous value, so writing
the same value twice fires once.

---

## Validation and constraints

`SelectBox` inherits the rule system from [TextEntry](textentry.md). The most useful
rules for a picker are `'required'` and `'custom'`:

```python
priority = ttk.SelectBox(app, label="Priority", items=["Low", "Medium", "High"], required=True)

# Reject orphan writes (the widget itself does not — see Value model).
priority.add_validation_rule(
    "custom",
    func=lambda v: v in ("", "Low", "Medium", "High"),
    message="Pick one of the listed priorities.",
)
```

Validation is most useful when:

- the list of valid items changes dynamically (re-add the rule against the new list);
- the field is conditionally required;
- the selected value must satisfy a cross-field rule.

For per-keystroke filtering of *characters* (e.g. allow only letters), use the underlying
[Entry](../primitives/entry.md)'s `validatecommand`.

---

## When should I use SelectBox?

Use `SelectBox` when:

- users pick one value from a known list and you want full form-field chrome (label, message, validation).
- the list is long enough that a search/filter helps.
- you want to allow custom values alongside a suggested list.

Prefer a different control when:

- you want a plain button + popup menu without entry chrome → use [OptionMenu](../selection/optionmenu.md).
- you need raw `ttk.Combobox` semantics → use [Combobox](../primitives/combobox.md).
- the choices fit on screen as visible options → use [RadioGroup](../selection/radiogroup.md).
- the user picks several values → use [CheckButton](../selection/checkbutton.md) or [ToggleGroup](../selection/togglegroup.md).

---

## Related widgets

- [TextEntry](textentry.md) — the input chrome SelectBox is built on.
- [OptionMenu](../selection/optionmenu.md) — simpler button-and-menu selection.
- [Combobox](../primitives/combobox.md) — low-level ttk dropdown.
- [RadioGroup](../selection/radiogroup.md) — single selection from visible options.
- [Form](form.md) — declare a `selectbox` editor in a form definition.

---

## Reference

- **API reference:** [`ttkbootstrap.SelectBox`](../../reference/widgets/SelectBox.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Signals](../../capabilities/signals/signals.md)
    - [Localization](../../capabilities/localization.md)
