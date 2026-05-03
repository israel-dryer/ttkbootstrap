---
title: NumericEntry
---

# NumericEntry

`NumericEntry` is a form-ready numeric input that combines a label, an
entry field, and a message line into a single composite widget. It
extends [`TextEntry`](textentry.md) with the behaviors numeric input
almost always needs: typed values, min/max bounds, stepping via keys
and mouse wheel, optional spin buttons, and locale-aware formatting on
commit.

The committed value is an `int` or a `float` — the type is inferred
from `value`, `minvalue`, `maxvalue`, and `increment`. Whatever the
user types is parsed at commit time, clamped (or wrapped) into range,
and reformatted for display so downstream code sees a clean numeric
value, never raw text.

<figure markdown>
![NumericEntry states](../../assets/dark/widgets-numericentry-states.png#only-dark)
![NumericEntry states](../../assets/light/widgets-numericentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.NumericEntry(
    app,
    label="Quantity",
    value=1,
    minvalue=0,
    maxvalue=999,
    message="How many items?",
)
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

`NumericEntry` separates **what is in the field right now** from **the
committed numeric value**:

| Concept | Meaning | How to read it |
|---|---|---|
| Text | The raw editable string in the entry, updated on every keystroke. | `entry.get()` |
| Value | The parsed, bounded number — produced when the user blurs the field, presses **Enter**, or steps. | `entry.value` |

Parsing, bounds clamping (or wrapping), and `value_format` are applied
at commit time only — never on every keystroke.

### Numeric type

The widget chooses `int` or `float` automatically:

- if `value`, `minvalue`, `maxvalue`, or `increment` is a `float`, the
  committed value is `float`.
- otherwise it is `int`.

```python
counter = ttk.NumericEntry(app, value=0, increment=1)        # int
amount  = ttk.NumericEntry(app, value=0.0, increment=0.01)   # float
```

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

### Signals and variables

`entry.signal` and `entry.variable` are bound to the **raw text**, not
the parsed number — same as [`TextEntry`](textentry.md). Read
`entry.value` when you need the typed numeric result.

```python
text = ttk.Signal("")
qty = ttk.NumericEntry(app, value=10, textsignal=text)
print(text.get())   # "10"
print(qty.value)    # 10
```

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial numeric value (default `0`). |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below; replaced by validation errors. |
| `minvalue` / `maxvalue` | Inclusive bounds. Out-of-range values are clamped on commit. |
| `increment` | Step size for keyboard, wheel, and spin buttons (default `1`). |
| `wrap` | If `True`, values cycle through the range instead of clamping. |
| `show_spin_buttons` | Show or hide the inline ± buttons (default `True`). |
| `value_format` | Locale-aware format spec applied on commit (`'currency'`, `'percent'`, `'fixedPoint'`, ICU patterns, …). |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |

```python
ttk.NumericEntry(app, label="Quantity")                 # primary (default)
ttk.NumericEntry(app, label="Quantity", accent="success")
ttk.NumericEntry(app, label="Quantity", density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Stepping

Stepping increments or decrements the value by `increment`. The user
can step by:

- the inline **+** / **−** spin buttons (if `show_spin_buttons=True`).
- the **Up** and **Down** arrow keys when the field has focus.
- the mouse wheel over the field.

You can also step programmatically:

```python
qty.increment()    # +1 step
qty.decrement()    # -1 step
qty.step(+5)       # +5 steps
```

Each step emits `<<Change>>` if the value actually changed, after
clamping or wrapping into range.

### Bounds and wrap

`minvalue` / `maxvalue` clamp on commit and on every step. With
`wrap=True`, values past either end cycle to the other:

```python
percent = ttk.NumericEntry(
    app,
    label="Percent",
    value=50,
    minvalue=0,
    maxvalue=100,
    increment=5,
    wrap=True,
)
```

Bounds can be changed at runtime — the current value is re-clamped:

```python
qty.configure(maxvalue=10)   # current value > 10 is clamped down
```

### Spin buttons

The increment and decrement buttons are inserted as add-ons after the
entry. `show_spin_buttons=False` hides them; toggling later via
`configure(show_spin_buttons=...)` shows or hides without rebuilding.

```python
field = ttk.NumericEntry(app, label="Quantity", show_spin_buttons=False)
```

### Add-ons

Like other field controls, `NumericEntry` accepts prefix and suffix
add-ons via `insert_addon`. They share the field's disabled state and
focus styling.

```python
salary = ttk.NumericEntry(app, label="Salary")
salary.insert_addon(ttk.Label, position="before", icon="currency-euro")

size = ttk.NumericEntry(app, label="Size", show_spin_buttons=False)
size.insert_addon(ttk.Label, position="after", text="cm", font="label[9]")
```

<figure markdown>
![addons](../../assets/dark/widgets-numericentry-addons.png#only-dark)
![addons](../../assets/light/widgets-numericentry-addons.png#only-light)
</figure>

### Disable, enable, readonly

```python
qty.disable()        # not editable, not focusable; spin buttons disable too
qty.enable()
qty.readonly(True)   # focusable, copyable, not editable
qty.readonly(False)
```

### Locale-aware formatting

When `value_format` is set, the committed number is formatted using the
active locale. If the locale changes at runtime, the displayed text is
reformatted automatically — the underlying numeric value is unchanged.

```python
ttk.NumericEntry(app, label="Currency",    value=1234.56,   value_format="currency").pack()
ttk.NumericEntry(app, label="Fixed point", value=15422354,  value_format="fixedPoint").pack()
ttk.NumericEntry(app, label="Percent",     value=0.35,      value_format="percent").pack()
```

<figure markdown>
![numeric formats](../../assets/dark/widgets-numericentry-formats.png#only-dark)
![numeric formats](../../assets/light/widgets-numericentry-formats.png#only-light)
</figure>

!!! link "See [Localization](../../capabilities/localization.md) for the available format specs and locale handling."

---

## Events

`NumericEntry` emits virtual events with structured payloads. Each one
has a matching `on_*` / `off_*` helper for ergonomic registration.

**Input, value, and step events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value differs from focus-in value | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |
| `<<Increment>>` | `on_increment` | step up requested (key, wheel, button) — fires before the step | `{'value': current_value}` |
| `<<Decrement>>` | `on_decrement` | step down requested — fires before the step | `{'value': current_value}` |

```python
def show_committed(event):
    print("committed:", event.data["value"])

def show_step_up(event):
    print("stepping up from:", event.data["value"])

qty = ttk.NumericEntry(app, value=0, minvalue=0, maxvalue=10)
qty.on_changed(show_committed)
qty.on_increment(show_step_up)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

!!! tip "Live vs committed"
    Use `on_input` for live previews. Use `on_changed` when you only
    care about the final number the user settled on. The `<<Change>>`
    event also fires on every step, so `on_changed` covers spin buttons
    and arrow-key stepping too.

---

## Validation and constraints

Bounds (`minvalue`, `maxvalue`) and `wrap` are the first line of
defense — values outside the range are clamped (or cycled) before
`<<Change>>` fires, so downstream code never sees them.

For app-level rules, use `add_validation_rule(rule_type, **kwargs)`,
which runs automatically on key release and blur. Built-in rule types
are `'required'`, `'pattern'`, `'stringLength'`, and `'custom'`.

```python
qty = ttk.NumericEntry(app, label="Quantity", minvalue=1, maxvalue=999, required=True)
qty.add_validation_rule("required", message="Quantity is required")

# Custom rule on the parsed numeric value
qty.add_validation_rule(
    "custom",
    func=lambda v: v is not None and v % 5 == 0,
    message="Must be a multiple of 5",
)
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`.

`add_validation_rules(rules)` replaces the entire rule set — useful
when constraints depend on another field's value. See
[`TextEntry`](textentry.md#validation-and-constraints) for the
cross-field pattern; the rule API is identical.

---

## When should I use NumericEntry?

Use `NumericEntry` when:

- the field collects a number and you want typed values out, not strings.
- bounds, stepping, or locale-aware formatting matter.
- you want consistent commit semantics (`<<Change>>` on blur, **Enter**, or step) across the fields in a form.

Prefer a different control when:

- the user adjusts by feel and live feedback matters → use [Scale](scale.md) or [LabeledScale](labeledscale.md).
- the input is a fixed list of preset values → use [SpinnerEntry](spinnerentry.md).
- you need raw `ttk.Spinbox` behavior with no chrome → use [Spinbox](../primitives/spinbox.md).
- the value is text → use [TextEntry](textentry.md).

---

## Related widgets

- [TextEntry](textentry.md) — base composite text field that `NumericEntry` extends.
- [SpinnerEntry](spinnerentry.md) — entry that steps through a fixed list of presets.
- [Scale](scale.md) — slider for live numeric adjustment.
- [LabeledScale](labeledscale.md) — slider with a value readout.
- [Spinbox](../primitives/spinbox.md) — low-level numeric stepper primitive.
- [Form](form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.NumericEntry`](../../reference/widgets/NumericEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Formatting](../../guides/formatting.md)
    - [Localization](../../capabilities/localization.md)
    - [Signals](../../capabilities/signals/signals.md)
