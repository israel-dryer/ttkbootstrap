---
title: Spinbox
---

# Spinbox

`Spinbox` is a thin themed wrapper over `tkinter.ttk.Spinbox` — a
single-line text field paired with up/down arrow buttons that step
through a numeric range or a list of values. It adds the ttkbootstrap
styling tokens (`accent`, `density`, `surface`, `input_background`)
and a reactive `textsignal` channel alongside the standard
`textvariable`.

For most app-level UI the [`SpinnerEntry`](../inputs/spinnerentry.md)
composite is the better choice — it adds a label, a message line, the
framework's standard `on_input` / `on_changed` events, commit-time
parsing, and validation messages. For numeric fields with bounds and
locale-aware formatting use [`NumericEntry`](../inputs/numericentry.md).
Reach for `Spinbox` directly when you are building your own composite
or specifically need the raw `ttk.Spinbox` surface — its `command=`
callback, `<<Increment>>` / `<<Decrement>>` events, `format=` option,
or the `wrap=` cycling behavior.

<figure markdown>
![spinbox](../../assets/dark/widgets-spinbox.png#only-dark)
![spinbox](../../assets/light/widgets-spinbox.png#only-light)
</figure>

---

## Basic usage

A numeric range:

```python
import ttkbootstrap as ttk

app = ttk.App()

spin = ttk.Spinbox(app, from_=0, to=10, increment=1, width=8)
spin.set(0)
spin.pack(padx=20, pady=20)

app.mainloop()
```

A fixed list of values cycles in either direction:

```python
ttk.Spinbox(app, values=("XS", "S", "M", "L", "XL"), wrap=True, width=8)
```

If both `values=` and `from_/to/increment=` are passed, `values` wins
for stepping. The numeric range options remain set on the widget but
the arrows cycle through the value list.

---

## Value model

`Spinbox` always holds a **string** — even in numeric mode. The
current text is reachable in three equivalent ways:

- **Tk method**: `spin.get()` / `spin.set(value)` /
  `spin.delete(0, "end")` / `spin.insert(0, "...")`.
- **Tk variable**: pass `textvariable=tk.StringVar(...)`.
- **Reactive signal**: pass `textsignal=ttk.Signal("")` and subscribe
  via `signal.subscribe(...)`.

`textvariable` and `textsignal` are kept in sync automatically through
`TextSignalMixin`. If you don't pass either, accessing
`spin.textsignal` (or `spin.textvariable`) lazily creates and binds
one. If both are passed, `textsignal` wins.

`Spinbox` does **no** parsing, clamping, or formatting on its own:

- `spin.set(99)` on a `from_=0, to=10` Spinbox writes `"99"` through
  unchanged — the widget will not refuse or clamp out-of-range values.
- `format="%.2f"` reformats values **only when stepping** (arrow
  click, `<<Increment>>`, `<<Decrement>>`). It does not reformat the
  current text on `spin.set(0.5)`.
- `state="readonly"` blocks user typing, not programmatic `set()` —
  any string can still be written through, including values not in
  `values=` or outside `from_/to=`.

For declarative numeric parsing, locale-aware formatting, and
out-of-range messages, use [`NumericEntry`](../inputs/numericentry.md).

---

## Common options

| Option | Type | Description |
|---|---|---|
| `from_` | `float` | Lower bound (numeric mode). |
| `to` | `float` | Upper bound (numeric mode). |
| `increment` | `float` | Step size when arrows are clicked. Default `1`. |
| `values` | `tuple[str, ...]` | List-mode values. Wins over `from_/to` for stepping when set. |
| `wrap` | `bool` | Cycle past the endpoint (max → min for numeric, last → first for list). |
| `format` | `str` | Tk format spec applied when stepping (e.g. `"%.2f"`). Does not reformat on `set()`. |
| `state` | `str` | `"normal"` (typing allowed), `"readonly"` (arrows-only), or `"disabled"`. |
| `textvariable` | `tk.Variable` | Tk variable bound to the displayed text. |
| `textsignal` | `Signal[str]` | Reactive signal bound to the text. Wins over `textvariable` when both are passed. |
| `command` | callable | Invoked on each step. **Not** invoked on `set()`, typing, or focus events — see *Events*. |
| `width` | `int` | Width of the entry field in **characters**. |
| `accent` | `str` | Theme token for the focus ring (`"primary"`, `"success"`, `"danger"`, …). Defaults to `"primary"`. |
| `surface` | `str` | Surface token of the parent container; affects the focus-ring blend. **Construction-only** — see *Behavior*. |
| `density` | `'default'` \| `'compact'` | Visual size. `compact` uses the smaller `caption` font and shorter row image. **Reconfigure is partially broken** — see *Behavior*. |
| `font` | `str \| Font` | Override the entry text font. Forced to `caption` when `density='compact'`. |
| `style_options` | `dict` | Escape hatch for additional builder keys (e.g. `{'input_background': 'background'}`). |

Only the `default` variant is registered for `TSpinbox` — passing any
other `variant` raises `BootstyleBuilderError`.

!!! note "Background tokens"
    The field's fill color resolves to the `input_background` style
    option (defaults to `content`). The constructor doesn't expose
    `input_background` directly — pass it via
    `style_options={'input_background': 'background'}`, or set it on
    the parent `Frame` so it cascades. Inside a
    `Frame(input_background='...')`, every descendant Spinbox
    inherits the value automatically.

---

## Behavior

**Standard ttk.Spinbox behavior.** Focus, caret navigation,
copy/cut/paste, click-and-hold to repeat-step, and the inherited
`<KeyPress>` / `<KeyRelease>` / `<FocusIn>` / `<FocusOut>` events all
work unchanged from ttk.

**Stepping mechanics.** A *step* is any of: clicking an arrow,
pressing `<Up>` / `<Down>` while focused, or generating
`<<Increment>>` / `<<Decrement>>` directly. Each step:

1. Reads the current value.
2. Applies `+increment` (Increment) or `-increment` (Decrement) — or,
   in list mode, advances by one position.
3. Clamps against `from_/to` (or wraps if `wrap=True`).
4. If `format=` is set, reformats the new value.
5. Writes the new text into the entry.
6. Fires `command=` and `<<Increment>>` / `<<Decrement>>`.

`command=`, `<<Increment>>`, and `<<Decrement>>` are stepping-only —
they do **not** fire on user typing, on `spin.set(...)`, or on
focus-out. To observe arbitrary text changes use the textsignal /
textvariable channel.

**State semantics:**

- `state="normal"` — user can type or step.
- `state="readonly"` — typing blocked, arrows still work, programmatic
  `set()` still writes through.
- `state="disabled"` — uneditable, dimmed, removed from focus
  traversal.

The shorthand `spin.state(["readonly"])` / `spin.state(["disabled"])`
also works (provided by `TtkStateMixin`).

**Reconfiguration.** `spin.configure(values=...)` works; arrows cycle
through the new list on the next step. `spin.configure(accent=...)`,
`configure(surface=...)`, and `configure(density=...)` all rebuild the
resolved ttk style and take effect immediately. `density` also updates
the font (`caption` for compact, `body` for default).

---

## Events

`Spinbox` does not emit any framework virtual events and ships no
`on_*` helpers. The four ways to observe value changes:

```python
# 1. Stepping only (arrow click, Up/Down key) — fires command=.
def stepped():
    print("stepped to:", spin.get())

spin = ttk.Spinbox(app, from_=0, to=10, command=stepped)
```

```python
# 2. Stepping only — virtual events with direction info.
spin.bind("<<Increment>>", lambda e: print("up:",   spin.get()))
spin.bind("<<Decrement>>", lambda e: print("down:", spin.get()))
```

```python
# 3. Every text change (typing AND stepping AND set()) — through
#    the binding channel.
spin = ttk.Spinbox(app, from_=0, to=10, textsignal=ttk.Signal(""))
spin.textsignal.subscribe(lambda value: print("text:", value))
```

```python
# 4. Per-keystroke during typing — bind directly.
spin.bind("<KeyRelease>", lambda e: print(spin.get()))
```

For framework-standard `on_input` (every keystroke) and `on_changed`
(commit boundary) helpers, use
[`SpinnerEntry`](../inputs/spinnerentry.md) or
[`NumericEntry`](../inputs/numericentry.md).

---

## Validation and constraints

`Spinbox` is a primitive — it does not validate input or clamp values
on `set()`. The arrows respect `from_/to` and `values=` at step time,
but every other input path (typing, programmatic `set()`,
`textsignal.set()`) is unconstrained.

For declarative validation messages, required-field semantics, and
form integration, use [`SpinnerEntry`](../inputs/spinnerentry.md)
(generic stepper) or
[`NumericEntry`](../inputs/numericentry.md) (numeric with locale-aware
formatting and bounds messages). For key-by-key gating that physically
rejects keystrokes, drop down to Tk's `validate` / `validatecommand`
machinery (see the [`Entry`](entry.md) reference for the
substitution-code rundown).

---

## When should I use Spinbox?

Reach for `Spinbox` directly when:

- you are **building your own composite** and need a raw input that
  you'll wrap with your own labels, messages, or layout;
- you specifically need a `ttk.Spinbox` API surface — the `command=`
  callback, `<<Increment>>` / `<<Decrement>>` events, or `wrap=True`
  cycling;
- you are interoperating with existing code that already expects a
  `ttk.Spinbox`.

For everything else — forms, settings panes, dialogs — prefer
[`SpinnerEntry`](../inputs/spinnerentry.md) for generic stepped values
or [`NumericEntry`](../inputs/numericentry.md) for numeric input with
parsing and bounds messages. Reach for
[`SelectBox`](../inputs/selectbox.md) when the choices are better
expressed as a dropdown list than as up/down arrows.

---

## Related widgets

- [SpinnerEntry](../inputs/spinnerentry.md) — form-ready stepped
  input with label, message line, and `on_input` / `on_changed`.
- [NumericEntry](../inputs/numericentry.md) — numeric input with
  bounds, parsing, and locale-aware formatting.
- [Scale](../inputs/scale.md) — continuous value input via a slider.
- [Entry](entry.md) — sibling primitive without arrows.
- [Combobox](combobox.md) — sibling primitive with a dropdown
  instead of arrows.

---

## Reference

- [`ttkbootstrap.Spinbox`](../../reference/widgets/Spinbox.md)
