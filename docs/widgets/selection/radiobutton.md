---
title: RadioButton
---

# RadioButton

`RadioButton` is the **mutually-exclusive selection primitive** — a
filled-circle indicator plus a label, with a *shared* variable across
sibling radios. Each radio carries its own `value=`; clicking any
radio writes that value into the shared variable, and the radio whose
`value=` matches paints as selected. The variable is the single
source of truth for the group.

Unlike CheckButton (where each control owns an independent boolean),
RadioButton is meaningful only in groups of two or more sharing a
`signal=` or `variable=`. For higher-level grouping, see
[RadioGroup](radiogroup.md) (manages a set of radios as one widget)
and [RadioToggle](radiotoggle.md) / [ToggleGroup](togglegroup.md)
(toolbutton-styled variants).

<figure markdown>
![radiobutton states](../../assets/dark/widgets-radiobutton-states.png#only-dark)
![radiobutton states](../../assets/light/widgets-radiobutton-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

choice = ttk.Signal("medium")

ttk.RadioButton(app, text="Low",    signal=choice, value="low").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="Medium", signal=choice, value="medium").pack(anchor="w", padx=20, pady=2)
ttk.RadioButton(app, text="High",   signal=choice, value="high").pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

The radio whose `value=` equals the current signal value paints
selected (here, "Medium"). Clicking another radio writes its `value=`
to `choice`, and the visual selection follows.

---

## Selection model

RadioButton holds **no value of its own** — selection is decided by
matching `value=` against the shared variable. The Tk variable lives
on the widget as `widget.variable`; when `signal=` is used, a reactive
`widget.signal` mirrors it. Sibling radios sharing the same `signal=`
or `variable=` reuse the same underlying object.

**Value type.** The default variable is an **`IntVar`** (initial
value `0`). Pass `value=` strings or other non-int types to coerce
the variable to a string representation. To pin a known type, supply
your own `tk.StringVar` / `tk.IntVar` via `variable=` (or a typed
`Signal`) and pass it to every radio in the group.

**Mutually exclusive, by sharing a variable.** "Group" is not a
class-level concept on RadioButton — it's an emergent property of two
or more radios pointing at the same variable. Forgetting to pass
`signal=` / `variable=` makes each radio its own independent group of
one (clicking one does not deselect another). For a group container
that enforces the binding, use [RadioGroup](radiogroup.md).

```python
choice = ttk.Signal("a")
r1 = ttk.RadioButton(app, text="A", signal=choice, value="a")
r2 = ttk.RadioButton(app, text="B", signal=choice, value="b")
# r1.signal is r2.signal  -> True (shared)
# r1.value is r2.value    -> True (both read from the same signal)
```

**Initial selection.** The radio whose `value=` matches the variable's
*current* value paints selected. With `Signal("medium")` and three
radios `value="low"` / `"medium"` / `"high"`, "Medium" is selected at
construction. Without an initial value (e.g. a default `Signal()`
holding `""`), no radio paints selected — that's the "no choice yet"
state. To force a selection at startup, set the signal *before*
constructing the radios, or call `choice.set("medium")` after.

**Reading and writing the selected value.** The selected value is
just `signal.get()` (or `variable.get()`). Each radio also exposes
`widget.value` as a convenience that reads the shared variable —
critically, `widget.value` returns the *current selection*, **not**
the radio's own `value=` constructor argument:

```python
choice = ttk.Signal("medium")
r1 = ttk.RadioButton(app, text="Low", signal=choice, value="low")
r2 = ttk.RadioButton(app, text="Medium", signal=choice, value="medium")
# r1.value -> "medium"  (shared selection, NOT "low")
# r2.value -> "medium"
```

The radio's own `value=` constructor argument is stored as the Tk
option `widget.cget("value")` — that's the constant the radio writes
into the variable when clicked.

**Commit semantics.** Clicking a radio writes its constructor `value=`
into the shared variable immediately; programmatic
`widget.set(some_value)` writes through the same path. There's no
separate commit step.

---

## Common options

| Option | Type | Effect |
| --- | --- | --- |
| `text` | `str` | Label shown next to the indicator. Localized through `MessageCatalog` when `localize` permits. |
| `value` | `Any` | The constant this radio writes into the shared variable when clicked. Required for meaningful group behavior — defaults to `''`. |
| `signal` | `Signal` | Shared reactive binding across the group. Subscribers fire on every change. |
| `variable` | `Variable` | Shared Tk variable to bind directly. Mutually substitutable with `signal=`. |
| `command` | `Callable[[], None]` | Fires on **user invocation only** (click or `.invoke()`). Programmatic `set()` and variable writes do **not** fire it. |
| `state` | `'normal'` / `'disabled'` / `'readonly'` | Disables click input but keeps the variable mutable from code. |
| `accent` | str | Theme token for the selected indicator's dot fill (default `'primary'`). |
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

`bootstyle` is accepted but **deprecated** — use `accent`.

RadioButton has only one variant: the default circular indicator.
The style builder (`style/builders/radiobutton.py`) registers only
`'default'` for `TRadiobutton`; passing any other variant raises
`BootstyleBuilderError`. For a button-style radio, use the dedicated
[RadioToggle](radiotoggle.md) class (it maps to a separate
`Toolbutton` style class with its own variant axis).

`density` is **not** a valid option for RadioButton — the style
builder reads only `accent` and `surface`. Passing `density=...`
raises `TclError: unknown option "-density"`. (RadioToggle does
accept `density=`.)

### Colors & Styling

```python
ttk.RadioButton(app, text="Default")
ttk.RadioButton(app, text="Secondary", accent="secondary")
ttk.RadioButton(app, text="Success", accent="success")
ttk.RadioButton(app, text="Warning", accent="warning")
ttk.RadioButton(app, text="Danger", accent="danger")
```

<figure markdown>
![colors](../../assets/dark/widgets-radiobutton-colors.png#only-dark)
![colors](../../assets/light/widgets-radiobutton-colors.png#only-light)
</figure>

`accent` colors the selected indicator's dot. The label foreground
tracks `surface` automatically. See
[Design System – Variants](../../design-system/variants.md).

---

## Behavior

**User input.** A left-click selects the radio and writes its
constructor `value=` into the shared variable. The standard Tk
keyboard contract applies: Tab moves focus, Space selects the focused
radio. Unlike some platform conventions, the **arrow keys do not
auto-cycle** between radios sharing a variable — RadioButton inherits
ttk's stock Tab traversal model. For arrow-key navigation across a
group, use [RadioGroup](radiogroup.md), which adds the binding.

**Disabled and readonly.** `state='disabled'` greys the indicator and
blocks clicks; the variable is still writable from code. Disabling a
radio whose value happens to be the current selection leaves the
selection visible but uninteractive — the user can still pick another
radio in the group. `state='readonly'` behaves identically to
`disabled` for user input.

**Reconfiguration.** `accent`, `text`, `state`, `value`, `signal`,
and `variable` can all be changed via `configure(...)` after
construction. Reconfiguring `value=` changes the **constant this
radio writes when clicked** — it does *not* re-write the shared
variable. Use `widget.set(new)` (or `signal.set(new)`) to change the
current selection.

**Visual states.** The style builder maps three combinations onto
the indicator: `selected`, `!selected !alternate`, and `disabled`.
Each combines with `focus` for keyboard focus feedback. RadioButton
has no `alternate` (indeterminate) state — it would be meaningless
for mutually-exclusive choice.

---

## Events

Three observation paths, with the same timing asymmetry as
CheckButton:

| Path | Fires when... | Receives |
| --- | --- | --- |
| `command=` callback (per radio) | The **user** clicks (or `widget.invoke()` is called) **on this specific radio**. Programmatic `set()` does not fire it. | No arguments. |
| `signal.subscribe(fn)` | The shared variable changes — from any radio's user click, from `set()` on any radio, from direct `signal.set(...)`. | The new selected value. |
| `variable.trace_add('write', fn)` | Same as signal: any variable write. | The Tk trace tuple `(name, index, mode)`. |

For group-level handling, subscribe to the shared signal **once** —
one subscription covers selections from every radio in the group:

```python
import ttkbootstrap as ttk

app = ttk.App()
choice = ttk.Signal("medium")

def on_change(new_value):
    print("now selected:", new_value)

choice.subscribe(on_change)

for label, val in [("Low", "low"), ("Medium", "medium"), ("High", "high")]:
    ttk.RadioButton(app, text=label, signal=choice, value=val).pack(anchor="w", padx=20, pady=2)

app.mainloop()
```

Use per-radio `command=` only when you need to know which **specific**
radio was clicked (e.g. analytics, per-option side effects).
RadioButton emits **no virtual events** of its own and exposes no
`on_*` helpers.

---

## When should I use RadioButton?

Use RadioButton when:

- the user must pick **exactly one** of a small set of options (≤ ~7)
- all options are short and benefit from being visible at once
  (priority levels, sort order, view mode, license tier)
- screen space is available for the full list

Prefer:

- **[RadioGroup](radiogroup.md)** — when the radios should be managed
  as a single composite widget (with arrow-key navigation, layout
  control, and bulk option updates)
- **[RadioToggle](radiotoggle.md)** / **[ToggleGroup](togglegroup.md)**
  — when the choice is a view mode or formatting strip and a button
  affordance fits better than a radio indicator
- **[OptionMenu](optionmenu.md)** — for medium-length lists (~5–20)
  where space is tight; a button + popup menu
- **[SelectBox](selectbox.md)** — for longer lists or when the user
  needs search / filtering
- **[CheckButton](checkbutton.md)** — when **multiple** independent
  options are allowed (RadioButton is *exactly one*)

---

## Related widgets

- **[RadioGroup](radiogroup.md)** — composite container that owns
  the shared signal and adds keyboard navigation
- **[RadioToggle](radiotoggle.md)** — toolbutton-styled mutually
  exclusive sibling
- **[ToggleGroup](togglegroup.md)** — group container for
  RadioToggle children
- **[CheckButton](checkbutton.md)** — independent boolean siblings
  (multi-select)
- **[SelectBox](selectbox.md)** / **[OptionMenu](optionmenu.md)** —
  dropdown selection alternatives

---

## Reference

- **API reference:** `ttkbootstrap.RadioButton`
- **Related guides:** [Signals](../../capabilities/signals/signals.md),
  [Localization](../../capabilities/localization.md),
  [Design System](../../design-system/index.md)
