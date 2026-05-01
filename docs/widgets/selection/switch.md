---
title: Switch
---

# Switch

`Switch` is a [CheckButton](checkbutton.md) subclass restyled as a
slider track — the indicator slides between an off-position and an
on-position instead of filling a check box. The value model is
**identical** to CheckButton: a single boolean variable that flips
between `onvalue` and `offvalue` on user click, with the same
`signal=` / `variable=` binding paths.

Use `Switch` when the choice is a single immediate-effect on/off
(autosave, dark mode, wireless), where the slider affordance matches
user expectations better than a check box. The two widgets are
interchangeable below the surface — the difference is purely visual
plus one Switch-specific quirk: it has **no indeterminate state**.

<figure markdown>
![switch](../../assets/dark/widgets-switch.png#only-dark)
![switch](../../assets/light/widgets-switch.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Switch(app, text="Enable dark mode", value=True).pack(padx=20, pady=6)
ttk.Switch(app, text="Send notifications", value=False).pack(padx=20, pady=6)

app.mainloop()
```

`value=True` / `value=False` initializes the bound variable. Without
`value=`, the switch starts in the off position.

---

## Selection model

Switch holds a single boolean-shaped value in a Tk `Variable` exposed
as `widget.variable`. When `signal=` is used, a reactive
`widget.signal` mirrors it.

**Value type.** The default variable is a `BooleanVar` with
`onvalue='1'` / `offvalue='0'`. `widget.value` returns the Python
side (`True` / `False`). Pass `onvalue=` / `offvalue=` plus a matching
`variable=` to drive non-boolean domains (e.g. `"yes"` / `"no"`,
`"on"` / `"off"`).

**No tri-state.** Unlike CheckButton, Switch has **no indeterminate
indicator**. The Switch style builder maps only `selected` and
`!selected` images — forcing `state(['alternate'])` is visually
invisible (the off image renders unchanged). Use CheckButton when you
need a real third state.

**Initial state and `value=`.** The constructor reads `value=` only
when neither `signal=` nor `variable=` was passed. When you bring
your own variable, it wins:

```python
v = ttk.Signal(True)
sw = ttk.Switch(app, text="Enabled", signal=v, value=False)
# sw.value is True — the signal's pre-existing value, not value=False
```

**Independent, not grouped.** Each Switch owns its own variable
unless the caller passes one. Sharing a variable across switches
makes them all toggle together — that's a misuse pattern; reach for
[RadioButton](radiobutton.md) when the choices are mutually exclusive.

**Commit semantics.** The bound variable is updated on every user
click and on every `sw.set(...)` call. There's no separate "commit"
step.

```python
import ttkbootstrap as ttk

app = ttk.App()
dark_mode = ttk.Signal(False)

sw = ttk.Switch(app, text="Dark mode", signal=dark_mode)
sw.pack(padx=20, pady=20)

dark_mode.subscribe(lambda v: print("now:", v))

app.mainloop()
```

---

## Common options

Switch accepts the full CheckButton option surface; only the
Switch-specific items and the most-used shared options are listed
here.

| Option | Type | Effect |
| --- | --- | --- |
| `text` | `str` | Label shown next to the slider. Localized through `MessageCatalog` when `localize` permits. |
| `value` | `Any` | **Construction-time only.** Initial value written to the bound variable when `signal=` and `variable=` are both absent. |
| `onvalue` | `Any` | Value written when the switch is on. Default `'1'`. |
| `offvalue` | `Any` | Value written when the switch is off. Default `'0'`. |
| `signal` | `Signal` | Reactive binding. Subscribers fire on every change. |
| `variable` | `Variable` | Tk variable to bind directly. Mutually substitutable with `signal=`. |
| `command` | `Callable[[], None]` | Fires on **user invocation only** (click or `.invoke()`). Programmatic `set()` and variable writes do **not** fire it. |
| `state` | `'normal'` / `'disabled'` / `'readonly'` | Disables click input but keeps the variable mutable from code. |
| `accent` | str | Theme token for the slider's "on" fill (default `'primary'`). |
| `surface` | str | Background surface; usually inherited from the parent. |
| `width` | int | Label width in characters; widget pads to that width. |
| `padding` | int / tuple | Extra space around the content. |
| `anchor` | str | Content alignment (`'w'`, `'e'`, `'center'`, ...). |
| `compound` | str | Image-vs-text placement when both are set. |
| `icon` | str / dict | Theme-aware icon spec. |
| `icon_only` | bool | Drop the text-reserved padding when no label is shown. |
| `image` | `PhotoImage` | Custom image to render alongside the label. |
| `underline` | int | Index of label character to underline (Alt-shortcut hint). |
| `localize` | `bool` / `'auto'` | How `text` is treated (literal vs translation key). Default `'auto'`. |
| `takefocus` | bool | Whether the widget participates in Tab traversal. |

`bootstyle` is accepted but **deprecated**. See the warnings in
*Behavior* — the deprecated path produces a different widget shape.

`variant` is **silently overridden**: Switch unconditionally writes
`variant='switch'` when `bootstyle` is not in kwargs
(`widgets/primitives/switch.py:43-44`). Passing `variant='default'`
to a Switch has no effect.

`density` is **not** a valid option for Switch (or CheckButton) —
the style builder reads only `accent` and `surface`. Passing
`density=...` raises `TclError: unknown option "-density"`.

### Colors & Styling

```python
ttk.Switch(app, text="Default")
ttk.Switch(app, text="Secondary", accent="secondary")
ttk.Switch(app, text="Success", accent="success")
ttk.Switch(app, text="Warning", accent="warning")
ttk.Switch(app, text="Danger", accent="danger")
```

`accent` colors the slider's "on" fill; the off-state border tracks
`surface`. See [Design System – Variants](../../design-system/variants.md).

---

## Behavior

**User input.** A left-click toggles the slider and writes the
opposite of the current variable value (cycling `onvalue` ↔
`offvalue`). The standard Tk keyboard contract applies: Tab moves
focus, Space invokes.

**Disabled and readonly.** `state='disabled'` greys the slider and
blocks clicks; the variable is still writable from code. `state='readonly'`
behaves identically to `disabled` for user input on this widget.

**No indeterminate state.** The Switch style builder
(`style/builders/switch.py:42-54`) maps only `selected` and
`!selected` to images — there is no `alternate` mapping. Forcing
`sw.state(['alternate'])` does not produce a distinct visual.
Confirmed at runtime:

```python
sw = ttk.Switch(app, value=True)
sw.state(['alternate'])
# state() is now ('selected', 'alternate'), but the rendered image
# is still the normal "on" slider — the alternate flag is invisible.
```

If you need a real third state, use [CheckButton](checkbutton.md) —
its builder has dedicated indeterminate images.

**Reconfiguration.** `accent`, `text`, `state`, `value`, `signal`,
and `variable` can all be changed via `configure(...)` after
construction. Reconfiguring `value=` writes through to the bound
variable (the post-construction equivalent of `set()`).

!!! warning "`bootstyle` produces a non-Switch widget"
    The deprecated `bootstyle` argument bypasses the
    `variant='switch'` assignment
    (`widgets/primitives/switch.py:43-44`). Constructing
    `Switch(bootstyle='primary')` yields a Tk style of
    `bs[…].primary.TCheckbutton` — a regular CheckButton with a
    check-box indicator, not a slider. Use `accent='primary'`
    instead. The deprecation warning fires, but the visual silently
    diverges from what the class name implies.

!!! warning "`set(None)` raises"
    `BooleanVar` cannot hold `None`, so `sw.set(None)` raises
    `TypeError: getboolean() argument must be str, not None`. There
    is no programmatic path to the indeterminate state at all on
    Switch — the visual mapping isn't there either, so the question
    doesn't arise in practice. If your domain has a real "unset"
    third state, switch to CheckButton with a custom `tk.StringVar`.

---

## Events

Three independent observation paths, identical to CheckButton:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `command=` callback | The **user** clicks (or `widget.invoke()` is called). Programmatic `set()` does not fire it. | No arguments. |
| `signal.subscribe(fn)` | The bound variable changes — **either** from a user click **or** from `set()` / `configure(value=...)` / `signal.value = ...`. | The new value. |
| `variable.trace_add('write', fn)` | Same as signal: any variable write. | The Tk trace tuple `(name, index, mode)`. |

Use `command=` for user-intent handlers ("save when the user toggles
this") and the signal for "react to any change" listeners.

```python
import ttkbootstrap as ttk

app = ttk.App()
v = ttk.Signal(False)

def on_click():
    print("user toggled, current:", v.value)

def on_change(new_value):
    print("any change, new:", new_value)

sw = ttk.Switch(app, text="Notify me", signal=v, command=on_click)
v.subscribe(on_change)
sw.pack(padx=20, pady=20)

app.mainloop()
```

Switch emits **no virtual events** of its own — there is no
`<<Changed>>` to bind, and no `on_*` / `off_*` helpers beyond what's
above.

---

## When should I use Switch?

Use Switch when:

- the choice is a single boolean that takes effect immediately (dark
  mode, autosave, wireless on/off)
- the slider affordance matches user expectations better than a
  check box (system settings, hardware-style toggles)

Prefer:

- **[CheckButton](checkbutton.md)** — for form-style "check this
  option" lists, terms-and-conditions agreement, or any case where a
  third (indeterminate) state is meaningful
- **[CheckToggle](checktoggle.md)** — when the toggle should look
  like a button you press in (toolbars, view-mode selectors)
- **[RadioButton](radiobutton.md)** / **[RadioGroup](radiogroup.md)**
  — when only one of several options can be active

Visually, Switch reads as immediate effect, CheckButton reads as a
reviewable form choice. They are interchangeable mechanically; the
choice is about user expectation.

---

## Related widgets

- **[CheckButton](checkbutton.md)** — parent class; classic check
  box with tri-state support
- **[CheckToggle](checktoggle.md)** — sibling subclass with
  toolbutton chrome
- **[RadioButton](radiobutton.md)** — mutually-exclusive sibling
- **[Form](../forms/form.md)** — declarative wrapper supporting
  `editor='switch'` for switch fields

---

## Reference

- **API reference:** `ttkbootstrap.Switch`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
