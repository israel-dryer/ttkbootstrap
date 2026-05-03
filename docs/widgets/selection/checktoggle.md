---
title: CheckToggle
---

# CheckToggle

`CheckToggle` is a [CheckButton](checkbutton.md) subclass restyled as
a pressed/unpressed button — checkbox semantics drawn as toolbutton
chrome. The selection model is the same boolean-valued binding as
CheckButton, but the underlying ttk style class is `Toolbutton` (not
`TCheckbutton`), which gives it a real `default` / `outline` / `ghost`
variant axis and a `density` knob — neither of which exist on the
parent.

Use `CheckToggle` when the toggle should look like a button you press
in: toolbars, view-mode strips, formatting bars (Bold / Italic /
Underline). When the user expects a check box (forms, settings),
prefer CheckButton; when the user expects a slider (immediate-effect
on/off), prefer [Switch](switch.md).

<figure markdown>
![checktoggle](../../assets/dark/widgets-checktoggle.png#only-dark)
![checktoggle](../../assets/light/widgets-checktoggle.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.CheckToggle(app, text="Bold", value=False).pack(side="left", padx=4, pady=10)
ttk.CheckToggle(app, text="Italic", value=True).pack(side="left", padx=4, pady=10)

app.mainloop()
```

`value=True` / `value=False` initializes the bound variable. Without
`value=`, the toggle starts unpressed.

---

## Selection model

CheckToggle holds a single value bound to a Tk `Variable` exposed as
`widget.variable`. When `signal=` is used, a reactive `widget.signal`
mirrors it.

**Value type.** Unlike CheckButton (which uses `BooleanVar`) the
default variable here is a **`StringVar`** with `onvalue='1'` /
`offvalue='0'` — the toolbutton style class doesn't get the
BooleanVar treatment that `TCheckbutton` does. `widget.value` returns
the variable's string contents. Pass `onvalue=` / `offvalue=` plus a
matching `variable=` to drive non-string domains (or use a custom
`tk.BooleanVar`).

**No tri-state.** The toolbutton style builder
(`style/builders/toolbutton.py`) maps `selected` / `pressed` /
`focus` / `disabled` / `hover` — but not `alternate`. Setting
`state(['alternate'])` produces no distinct visual.

That said, because the variable is a `StringVar`, you *can* park it
in a "third state" by writing any value that matches neither
`onvalue` nor `offvalue` — the widget then paints unpressed (no
`selected` flag). The first user click coerces it back to `onvalue`,
so the third state survives only until interacted with:

```python
ct = ttk.CheckToggle(app, text="Tri", value=True)
ct.set("indeterminate")     # neither '1' nor '0'
# state() → ()  (unpressed)
ct.invoke()                  # cycles to onvalue
# variable.get() → '1', state() → ('selected',)
```

**Initial state and `value=`.** The constructor reads `value=` only
when neither `signal=` nor `variable=` was passed. When you bring
your own variable, it wins.

**Independent, not grouped.** Each CheckToggle owns its own variable
unless the caller passes one. Reach for [RadioToggle](radiotoggle.md)
or [ToggleGroup](togglegroup.md) when only one toggle in a strip can
be active at a time.

**Commit semantics.** The bound variable updates on every user click
and on every `ct.set(...)` call. There's no separate "commit" step.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `text` | `str` | Label shown inside the toggle. Localized through `MessageCatalog` when `localize` permits. |
| `value` | `Any` | **Construction-time only.** Initial value written to the bound variable when `signal=` and `variable=` are both absent. |
| `onvalue` | `Any` | Value written when pressed. Default `'1'`. |
| `offvalue` | `Any` | Value written when unpressed. Default `'0'`. |
| `signal` | `Signal` | Reactive binding. Subscribers fire on every change. |
| `variable` | `Variable` | Tk variable to bind directly. Mutually substitutable with `signal=`. |
| `command` | `Callable[[], None]` | Fires on **user invocation only** (click or `.invoke()`). Programmatic `set()` and variable writes do **not** fire it. |
| `state` | `'normal'` / `'disabled'` / `'readonly'` | Disables click input but keeps the variable mutable from code. |
| `accent` | str | Theme token for the pressed / focused fill (default `'primary'`; `'secondary'` for `ghost`). |
| `variant` | `'default'` / `'solid'` / `'outline'` / `'ghost'` | Visual weight (see *Variants* below). `'default'` is an alias of `'solid'`. **No `link` or `text` variants** — those exist on Button but not on Toolbutton. |
| `density` | `'default'` / `'compact'` | Reduces vertical padding and font size. |
| `surface` | str | Background surface; usually inherited from the parent. |
| `width` | int | Label width in characters; widget pads to that width. |
| `padding` | int / tuple | Extra space around the content. |
| `anchor` | str | Content alignment (`'w'`, `'e'`, `'center'`, ...). |
| `compound` | str | Image-vs-text placement when both are set. |
| `icon` | str / dict | Theme-aware icon spec. |
| `icon_only` | bool | Drop the text-reserved padding when no label is shown — typical for icon-only toolbars. |
| `image` | `PhotoImage` | Custom image to render alongside the label. |
| `underline` | int | Index of label character to underline (Alt-shortcut hint). |
| `localize` | `bool` / `'auto'` | How `text` is treated (literal vs translation key). Default `'auto'`. |
| `takefocus` | bool | Whether the widget participates in Tab traversal. |

`bootstyle` is accepted but **deprecated** — use `accent` and
`variant`.

### Variants

```python
ttk.CheckToggle(app, text="Default")                    # solid fill
ttk.CheckToggle(app, text="Outline", variant="outline") # outline ring, fills when pressed
ttk.CheckToggle(app, text="Ghost", variant="ghost")     # no chrome until hovered/pressed
```

The three variants share the same value model and event surface;
only the chrome differs:

| Variant | Off appearance | On appearance |
| --- | --- | --- |
| `default` / `solid` | Filled (accent color) | Filled (accent active) |
| `outline` | Outlined ring | Filled (accent color) |
| `ghost` | Transparent (matches surface) | Subtle accent tint |

`ghost` is the typical choice for inline toolbar toggles where the
unpressed state should disappear into the surrounding chrome.

### Colors & Styling

```python
ttk.CheckToggle(app, text="Primary", accent="primary")
ttk.CheckToggle(app, text="Success", accent="success")
ttk.CheckToggle(app, text="Danger", accent="danger")
```

`accent` colors the pressed / focus fill. The `ghost` variant
defaults to `accent='secondary'`; the others default to
`'primary'`. See [Design System – Variants](../../design-system/variants.md).

---

## Behavior

**User input.** A left-click toggles the pressed state and writes
the opposite of the current variable value (cycling `onvalue` ↔
`offvalue`). The standard Tk keyboard contract applies: Tab moves
focus, Space invokes.

**Disabled and readonly.** `state='disabled'` greys the toggle and
blocks clicks; the variable is still writable from code.
`state='readonly'` behaves identically to `disabled` for user input
on this widget.

**Reconfiguration.** `accent`, `variant`, `text`, `state`, `value`,
`signal`, and `variable` can all be changed via `configure(...)`
after construction. Reconfiguring `value=` writes through to the
bound variable.

**Visual states.** The toolbutton style maps state combinations
across `selected` (pressed), `pressed` (clicking now), `hover`,
`focus`, and `disabled`. Each variant draws these slightly
differently — see the source for full state-spec lists.

!!! note "`set(None)` does not raise"
    Because the default variable is a `StringVar`, `ct.set(None)`
    coerces to the string `'None'` and silently writes it — the
    widget paints unpressed, since `'None'` matches neither
    `onvalue` nor `offvalue`. This is **different from CheckButton
    and Switch**, where `set(None)` raises `TypeError`. Callers
    relying on the raise as a guard need to special-case
    CheckToggle, or pass an explicit `tk.BooleanVar` to get the
    BooleanVar behavior back.

---

## Events

Three independent observation paths, identical in shape to
CheckButton:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `command=` callback | The **user** clicks (or `widget.invoke()` is called). Programmatic `set()` does not fire it. | No arguments. |
| `signal.subscribe(fn)` | The bound variable changes — **either** from a user click **or** from `set()` / `configure(value=...)` / `signal.value = ...`. | The new value. |
| `variable.trace_add('write', fn)` | Same as signal: any variable write. | The Tk trace tuple `(name, index, mode)`. |

Use `command=` for user-intent handlers ("apply formatting when the
user toggles this") and the signal for "react to any change"
listeners.

```python
import ttkbootstrap as ttk

app = ttk.App()
sig = ttk.Signal(False)

def on_click():
    print("user toggled, current:", sig.value)

def on_change(new_value):
    print("any change, new:", new_value)

ct = ttk.CheckToggle(app, text="Bold", signal=sig, command=on_click)
sig.subscribe(on_change)
ct.pack(padx=20, pady=20)

app.mainloop()
```

CheckToggle emits **no virtual events** of its own — there is no
`<<Changed>>` to bind, and no `on_*` / `off_*` helpers beyond what's
above.

---

## When should I use CheckToggle?

Use CheckToggle when:

- the toggle lives in a toolbar, formatting bar, or compact mode
  strip, and a button affordance fits better than a check indicator
- multiple independent toggles sit side-by-side (Bold / Italic /
  Underline) and benefit from button-like grouping
- you want `density='compact'` (which CheckButton doesn't expose)

Prefer:

- **[CheckButton](checkbutton.md)** — for forms, settings panels,
  and any case where the user expects a check indicator (or where a
  real indeterminate visual matters)
- **[Switch](switch.md)** — for hardware-style on/off settings (dark
  mode, autosave) where the slider affordance reads better
- **[RadioToggle](radiotoggle.md)** / **[ToggleGroup](togglegroup.md)**
  — when only one toggle in a strip can be active at a time
- **[Button](../actions/button.md)** — when the action is one-shot
  (no persistent on/off state)

---

## Related widgets

- **[CheckButton](checkbutton.md)** — parent class; classic check
  box with tri-state support
- **[Switch](switch.md)** — sibling subclass with the slider
  indicator
- **[RadioToggle](radiotoggle.md)** — toolbutton-styled mutually
  exclusive sibling
- **[ToggleGroup](togglegroup.md)** — a ButtonGroup-shaped wrapper
  for related toggles

---

## Reference

- **API reference:** `ttkbootstrap.CheckToggle`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
