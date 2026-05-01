---
title: CheckButton
---

# CheckButton

`CheckButton` is the **boolean selection primitive** — an indicator
plus a label, with a bound variable that flips between `onvalue` and
`offvalue` on user click. By default it carries a `BooleanVar` whose
states are `True` / `False`, but `onvalue` and `offvalue` accept any
strings, so the same control can drive `"yes"`/`"no"`, `"on"`/`"off"`,
or any pair the surrounding form layer expects.

CheckButton is the foundation that [Switch](switch.md) and
[CheckToggle](checktoggle.md) extend — both are subclasses that
restyle the indicator (slider track, toolbutton chrome) without
changing the value model. Use CheckButton when the selection is one
*independent* boolean; use [RadioButton](radiobutton.md) when the
choice is one of many mutually-exclusive options sharing a variable.

<figure markdown>
![checkbutton](../../assets/dark/widgets-checkbutton-states.png#only-dark)
![checkbutton](../../assets/light/widgets-checkbutton-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckButton(app, text="Enable notifications", value=True).pack(padx=20, pady=6)
ttk.CheckButton(app, text="Send anonymous usage data", value=False).pack(padx=20, pady=6)

app.mainloop()
```

`value=True` / `value=False` initializes the bound variable.
Construct without `value=` to leave the variable at its default
(see *Selection model* — the default rendering is a quirk of Tk's
tri-state mechanism).

---

## Selection model

CheckButton holds a single boolean-shaped value. The state lives in a
Tk `Variable` exposed as `widget.variable` and (when `signal=` is
used) reflected through a reactive `widget.signal`.

**Value type.** The default variable is a `BooleanVar` with
`onvalue='1'` / `offvalue='0'`. `widget.value` returns the Python
side of the variable (`True` / `False`). To work in non-boolean
domains, pass `onvalue=` / `offvalue=` and a matching `variable=`:

```python
import tkinter as tk
import ttkbootstrap as ttk

app = ttk.App()
mode = tk.StringVar(value="yes")

ttk.CheckButton(
    app,
    text="Subscribed",
    variable=mode,
    onvalue="yes",
    offvalue="no",
).pack(padx=20, pady=6)

app.mainloop()
```

**Independent, not grouped.** Each CheckButton owns its own variable
unless the caller passes one explicitly. Multiple CheckButtons sharing
a variable will all toggle together — that's a misuse pattern; reach
for [RadioButton](radiobutton.md) when the choices are mutually
exclusive.

**Initial state and `value=`.** The constructor reads `value=` only
when neither `signal=` nor `variable=` was passed. When you bring
your own variable, it wins:

```python
v = ttk.Signal(True)
cb = ttk.CheckButton(app, text="Enabled", signal=v, value=False)
# cb.value is True — the signal's pre-existing value, not value=False
```

**Indeterminate state — read carefully.** A fresh CheckButton with no
`value=`, no `signal=`, and no `variable=` renders in the **alternate**
state at construction (Tk shows the indeterminate indicator). This is
a side effect of the bound `BooleanVar` having no Tcl-side value yet,
which matches the platform's default `tristatevalue` of `""`. After
the first user click, the variable cycles between `True` and `False`
only — alternate is **not reachable** programmatically. Calling
`cb.set(None)` raises `TypeError` because `BooleanVar` cannot hold
`None`. If you need a real third state that survives clicks, supply
your own `tk.StringVar` with a non-matching initial value and string
`onvalue` / `offvalue` — but understand that a single click coerces
the variable to one of those two strings.

**Commit semantics.** The bound variable is updated on every user
click and on every `cb.set(...)` call. There's no separate "commit"
step — CheckButton has no editing buffer.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `text` | `str` | Label shown next to the indicator. Localized through `MessageCatalog` when `localize` permits. |
| `value` | `Any` | **Construction-time only.** Initial value written to the bound variable when `signal=` and `variable=` are both absent. Does nothing on `configure(value=...)` post-construction. |
| `onvalue` | `Any` | Value written to the variable when checked. Default `'1'`. |
| `offvalue` | `Any` | Value written to the variable when unchecked. Default `'0'`. |
| `signal` | `Signal` | Reactive binding. Constructor auto-syncs a Tk variable to the signal so subscribers fire on every change. |
| `variable` | `Variable` | Tk variable to bind directly. Mutually substitutable with `signal=`. |
| `command` | `Callable[[], None]` | Fires on **user invocation only** (click or `.invoke()`). Programmatic `set()` and variable writes do **not** fire it. |
| `state` | `'normal'` / `'disabled'` / `'readonly'` | Disables click input but keeps the variable mutable from code. |
| `accent` | str | Theme token for the indicator's check / dot fill (default `'primary'`). |
| `surface` | str | Background surface; usually inherited from the parent. |
| `density` | `'default'` / `'compact'` | Reduces vertical / horizontal padding. |
| `width` | int | Label width in characters; widget pads to that width. |
| `padding` | int / tuple | Extra space around the content. |
| `anchor` | str | Content alignment within the widget bounds (`'w'`, `'e'`, `'center'`, ...). |
| `compound` | str | Image-vs-text placement when both are set. |
| `icon` | str / dict | Theme-aware icon spec. |
| `image` | `PhotoImage` | Custom image to render alongside the indicator. |
| `underline` | int | Index of label character to underline (Alt-shortcut hint). |
| `localize` | `bool` / `'auto'` | How `text` is treated (literal vs translation key). Default `'auto'` — tries the catalog, falls back to literal. |
| `takefocus` | bool | Whether the widget participates in Tab traversal. |
| `style_options` | dict | Extra dict forwarded to the style builder. |

`bootstyle` is accepted but **deprecated** — use `accent`.

CheckButton has effectively **one variant**: the default check-box
indicator. The `switch` style registered for `TCheckbutton` exists
solely to back the dedicated [Switch](switch.md) class (a subclass
that bakes in `variant='switch'`); reach for `Switch` rather than
passing `variant=` to `CheckButton` directly.

### Colors & Styling

```python
ttk.CheckButton(app, text="Default")
ttk.CheckButton(app, text="Secondary", accent="secondary")
ttk.CheckButton(app, text="Success", accent="success")
ttk.CheckButton(app, text="Warning", accent="warning")
ttk.CheckButton(app, text="Danger", accent="danger")
```

<figure markdown>
![colors](../../assets/dark/widgets-checkbutton-colors.png#only-dark)
![colors](../../assets/light/widgets-checkbutton-colors.png#only-light)
</figure>

`accent` colors the check / dot of the indicator. The label
foreground tracks `surface` automatically (readable on the parent's
background). Pass `surface='card'` (or any other surface token) to
shift the background under the widget.

See [Design System – Variants](../../design-system/variants.md) for
how accents apply across the framework.

---

## Behavior

**User input.** A left-click toggles the indicator and writes the
opposite of the current variable value (cycling `onvalue` ↔
`offvalue`). The standard Tk keyboard contract applies: Tab moves
focus to the widget, Space invokes it. The widget never auto-focuses
on hover.

**Disabled and readonly.** `state='disabled'` greys the indicator
and blocks clicks; the variable is still writable from code, so
`cb.set(True)` updates the rendered state but `command` does not
fire. `state='readonly'` is accepted by ttk but, in this widget,
behaves identically to `disabled` for user input.

**Reconfiguration.** `accent`, `text`, `state`, `value`, `signal`,
and `variable` can all be changed via `configure(...)` after
construction. Reconfiguring `value=` writes through to the bound
variable (this is the post-construction equivalent of `set()`),
unlike at construction time where `value=` is a one-shot
initializer.

**Visual states.** The style builder maps four state combinations
onto the indicator: `selected` (checked), `alternate` (indeterminate),
neither (unchecked), and `disabled`. Each combines with `hover`,
`focus`, and `pressed` for transient feedback.

---

## Events

There are three independent observation paths, and they have
different timing.

| Path | Fires when... | Receives |
| --- | --- | --- |
| `command=` callback | The **user** clicks (or `widget.invoke()` is called). Programmatic `set()` does not fire it. | No arguments. |
| `signal.subscribe(fn)` | The bound variable changes — **either** from a user click **or** from `set()` / `configure(value=...)` / `signal.value = ...`. | The new value. |
| `variable.trace_add('write', fn)` | Same as signal: any variable write. | The Tk trace tuple `(name, index, mode)`. |

The asymmetry matters: a "save" handler driven by user intent
belongs on `command`; a "this state changed for any reason" listener
belongs on the signal.

```python
import ttkbootstrap as ttk

app = ttk.App()
v = ttk.Signal(False)

def on_click():
    print("user-clicked, current:", v.value)

def on_change(new_value):
    print("any change, new:", new_value)

cb = ttk.CheckButton(app, text="Notify me", signal=v, command=on_click)
v.subscribe(on_change)
cb.pack(padx=20, pady=20)

app.mainloop()
```

CheckButton emits **no virtual events** of its own — there is no
`<<Changed>>` to bind. There are also no `on_*` / `off_*` helpers
beyond what's listed above.

!!! warning "`set(None)` raises"
    `BooleanVar` cannot hold `None`, so `cb.set(None)` raises
    `TypeError: getboolean() argument must be str, not None`. There
    is no public path back to the indeterminate (`alternate`) state
    once the variable has been written. If your domain has a real
    "unset" third state, use a `tk.StringVar` with custom
    `onvalue` / `offvalue` and treat any non-matching string as
    "unset" yourself.

---

## When should I use CheckButton?

Use CheckButton when:

- the choice is a single boolean (toggle a feature, accept terms,
  enable/disable a flag)
- multiple boolean options exist on the same panel and each is
  independent (settings, filters, feature flags)

Prefer:

- **[Switch](switch.md)** — when the boolean is a hardware-style
  on/off (volume, wireless, autosave) and the slider affordance
  matches user expectations better than a check
- **[CheckToggle](checktoggle.md)** — when the toggle should look
  like a button you press in (button bars, view-mode selectors)
- **[RadioButton](radiobutton.md)** / **[RadioGroup](radiogroup.md)**
  — when only one of several options can be active
- **[SelectBox](selectbox.md)** / **[OptionMenu](optionmenu.md)** —
  when the user picks one item from a dropdown list

---

## Related widgets

- **[Switch](switch.md)** — CheckButton subclass with the slider
  indicator
- **[CheckToggle](checktoggle.md)** — CheckButton subclass with
  toolbutton chrome
- **[RadioButton](radiobutton.md)** — mutually-exclusive sibling
- **[Form](../forms/form.md)** — declarative wrapper that bundles
  CheckButtons with labels and validation

---

## Reference

- **API reference:** `ttkbootstrap.CheckButton`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
