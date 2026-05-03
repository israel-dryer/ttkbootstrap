---
title: Combobox
---

# Combobox

`Combobox` is a thin themed wrapper over `tkinter.ttk.Combobox` — a
single-line text field paired with a dropdown of values. It adds the
ttkbootstrap styling tokens (`accent`, `density`, `surface`,
`input_background`), a reactive `textsignal` channel alongside the
standard `textvariable`, and a popdown that re-styles itself to track
theme changes.

For most app-level UI the [`SelectBox`](../inputs/selectbox.md)
composite is the better choice — it adds a label, a message line,
keyboard navigation, hover affordances, an optional search/filter, and
the framework's standard `on_changed` event. Reach for `Combobox`
directly when you are building your own composite or specifically need
the raw `ttk.Combobox` surface (`current()`, `postcommand`, the
`<<ComboboxSelected>>` Tk virtual event, dropdown row count via
`height=`).

<figure markdown>
![combobox](../../assets/dark/widgets-combobox.png#only-dark)
![combobox](../../assets/light/widgets-combobox.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

combo = ttk.Combobox(
    app,
    values=["Low", "Medium", "High"],
    state="readonly",
)
combo.set("Medium")
combo.pack(padx=20, pady=20)

app.mainloop()
```

Drop `state="readonly"` to allow free-form typing; the dropdown then
acts as a suggestion list rather than the only source of values.

---

## Value model

`Combobox` holds a single string. The current text is reachable in
three equivalent ways:

- **Tk method**: `combo.get()` / `combo.set(value)` / `combo.current()`
  — `current()` returns the index of the selection inside `values`, or
  `-1` if the text matches none of them.
- **Tk variable**: pass `textvariable=tk.StringVar(...)` and read/write
  through the variable.
- **Reactive signal**: pass `textsignal=ttk.Signal("")` and subscribe
  via `signal.subscribe(...)`.

`textvariable` and `textsignal` are kept in sync automatically through
`TextSignalMixin`. If you don't pass either, accessing
`combo.textsignal` (or `combo.textvariable`) lazily creates and binds
one. If both are passed, `textsignal` wins.

The meaning of the stored text depends on `state`:

- `state="readonly"` — user input is locked to dropdown selection, but
  `combo.set("anything")` still writes any string through. The field
  paints the orphan value as plain text and `current()` returns `-1`.
- `state="normal"` — the text may be anything the user types; the
  dropdown is a suggestion list.

---

## Common options

| Option | Type | Description |
|---|---|---|
| `values` | `list[str]` | Items shown in the dropdown. Reconfigurable. |
| `state` | `str` | `"normal"` (typing allowed), `"readonly"` (dropdown-only), or `"disabled"`. |
| `textvariable` | `tk.Variable` | Tk variable bound to the displayed text. |
| `textsignal` | `Signal[str]` | Reactive signal bound to the text. Wins over `textvariable` when both are passed. |
| `height` | `int` | Maximum rows shown in the dropdown before it scrolls. |
| `width` | `int` | Width of the entry field, in **characters**. |
| `postcommand` | callable | Invoked just before the dropdown opens — useful for refreshing `values`. The framework wraps your callback to also re-style the popdown. |
| `justify` | `str` | Text alignment inside the entry field. |
| `accent` | `str` | Theme token for the focus ring (`"primary"`, `"success"`, `"danger"`, …). Defaults to `"primary"`. |
| `surface` | `str` | Surface token of the parent container; affects the focus-ring blend. **Construction-only** — see *Behavior*. |
| `density` | `'default'` \| `'compact'` | Visual size. `compact` uses the smaller `caption` font and shorter row image. **Reconfigure is partially broken** — see *Behavior*. |
| `font` | `str \| Font` | Override the entry text font. Forced to `caption` when `density='compact'`. |
| `style_options` | `dict` | Escape hatch for additional builder keys (e.g. `{'input_background': 'background'}`). |

Only the `default` variant is registered for `TCombobox` — passing any
other `variant` raises `BootstyleBuilderError`.

!!! note "Background tokens"
    The field's fill color resolves to the `input_background` style
    option (defaults to `content`). The constructor doesn't expose
    `input_background` directly — pass it via
    `style_options={'input_background': 'background'}`, or set it on
    the parent `Frame` so it cascades. Inside a
    `Frame(input_background='...')`, every descendant Combobox
    inherits the value automatically.

---

## Behavior

**Standard ttk.Combobox behavior.** Focus, caret navigation,
copy/cut/paste, dropdown open via the chevron or the down-arrow key,
and the inherited `<KeyPress>` / `<KeyRelease>` / `<FocusIn>` /
`<FocusOut>` events all work unchanged from ttk.

**Popdown styling.** The dropdown popdown is created lazily on first
open by Tk and reused afterwards. ttkbootstrap re-applies the current
theme's colors and the density-aware font on every open, by wiring its
own callback into `postcommand` (your callback is still invoked, after
the styling pass). Theme changes also re-style any popdown that is
already alive. This is the main thing the wrapper adds beyond
`ttk.Combobox` — without it the popdown's embedded listbox/scrollbar
would not track theme changes.

**State semantics:**

- `state="normal"` — user can type, dropdown is a suggestion list.
- `state="readonly"` — user can only choose from the dropdown, but
  programmatic `combo.set(...)` still writes any string through (no
  validation against `values`).
- `state="disabled"` — uneditable, dimmed, removed from focus
  traversal.

The shorthand `combo.state(["readonly"])` / `combo.state(["disabled"])`
also works (provided by `TtkStateMixin`).

**Reconfiguration.** `combo.configure(values=...)` works; the dropdown
reflects the new list on its next open. `combo.configure(accent=...)`,
`configure(surface=...)`, and `configure(density=...)` all rebuild the
resolved ttk style and take effect immediately. `density` also updates
the font (`caption` for compact, `body` for default).

---

## Events

`Combobox` does not emit any framework virtual events and ships no
`on_*` helpers. The two ways to observe value changes are:

```python
# 1. Through the binding channel — fires on every write,
#    user input or programmatic.
combo = ttk.Combobox(app, textsignal=ttk.Signal(""), values=["A", "B"])
combo.textsignal.subscribe(lambda value: print("text:", value))

# 2. Bind directly to ttk.Combobox's virtual event — fires only when
#    the user picks an item from the dropdown.
combo.bind("<<ComboboxSelected>>", lambda e: print("picked:", combo.get()))
```

`<<ComboboxSelected>>` is **not** fired by `combo.set(...)` and is not
fired when the user types. To react to typing in editable mode, bind
`<KeyRelease>` on the widget or subscribe through the textsignal.

For framework-standard `on_changed` semantics with a commit boundary
plus a built-in message line, use
[`SelectBox`](../inputs/selectbox.md).

---

## Validation and constraints

`Combobox` is a primitive — it does not validate that the text matches
`values`. With `state="readonly"` user input is constrained to the
dropdown, but the programmatic `set()` path bypasses that constraint
and silently accepts arbitrary strings. The widget will paint the
orphan value as plain text and `current()` will return `-1`.

For declarative validation messages, required-field semantics, and
form integration, use [`SelectBox`](../inputs/selectbox.md). For
key-by-key gating that physically rejects keystrokes, drop down to
Tk's `validate` / `validatecommand` machinery (see the
[`Entry`](entry.md) reference for the substitution-code rundown).

---

## When should I use Combobox?

Reach for `Combobox` directly when:

- you are **building your own composite** and need a raw
  text-plus-dropdown that you'll wrap with your own labels, messages,
  or layout;
- you specifically need a `ttk.Combobox` API surface — `current()`,
  `postcommand`, `<<ComboboxSelected>>`, the `height=` row count, the
  `xscrollcommand` hook;
- you are interoperating with existing code that already expects a
  `ttk.Combobox`.

For everything else — forms, settings panes, dialogs — prefer
[`SelectBox`](../inputs/selectbox.md). It ships with a label, a
message line, keyboard navigation, optional search/filter, and the
framework's standard event surface. Reach for
[`OptionMenu`](../selection/optionmenu.md) when you want a simple
button-and-menu picker without any text-input affordances.

---

## Related widgets

- [SelectBox](../inputs/selectbox.md) — form-ready selection control
  with label, message line, validation, and optional search.
- [OptionMenu](../selection/optionmenu.md) — button-and-menu picker
  with no text-input chrome.
- [Entry](entry.md) — sibling primitive without the dropdown half.
- [Spinbox](spinbox.md) — sibling primitive for stepped values.
- [DropdownButton](../actions/dropdownbutton.md) — opens a menu of
  *actions*, not a value picker.

---

## Reference

- [`ttkbootstrap.Combobox`](../../reference/widgets/Combobox.md)
