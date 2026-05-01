---
title: SpinnerEntry
---

# SpinnerEntry

`SpinnerEntry` is a form-ready input with built-in step controls. It
combines a text field — for typing or pasting — with up/down spin
buttons and arrow-key stepping. All of the field chrome that
[`TextEntry`](textentry.md) provides (label, message, validation,
signal/variable binding, accent, density, add-ons) comes along
unchanged.

`SpinnerEntry` runs in one of two modes. In **values mode** you
provide a fixed list of strings and the spinner cycles through them.
In **numeric mode** you provide `minvalue`/`maxvalue` and the spinner
steps through numbers in increments of `increment`. The two modes are
mutually exclusive — pass one or the other, not both.

<figure markdown>
![spinnerentry states](../../assets/dark/widgets-spinnerentry-states.png#only-dark)
![spinnerentry states](../../assets/light/widgets-spinnerentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

qty = ttk.SpinnerEntry(
    app,
    label="Quantity",
    value=1,
    minvalue=1,
    maxvalue=99,
    increment=1,
    message="How many items?",
)
qty.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

`SpinnerEntry` separates **what is in the field right now** from **the
committed value**:

| Concept | Meaning | How to read it |
|---|---|---|
| Text | The raw editable string in the entry, updated on every keystroke. | `qty.get()` |
| Value | The committed value — produced when the user blurs the field, presses **Enter**, or clicks a spin button. | `qty.value` |

Without `value_format`, the value is the same string the user typed
(or `None` when empty). With `value_format` set, the text is parsed on
commit into the corresponding type (number, currency, date, …) and
reformatted for display, exactly like [`TextEntry`](textentry.md).

```python
qty = ttk.SpinnerEntry(app, value=3, minvalue=0, maxvalue=10)
qty.value = 7      # set committed value
current = qty.value  # read committed value
raw = qty.get()      # read raw text any time
```

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

### Signals and variables

`qty.signal` and `qty.variable` are bound to the **raw text**, not the
parsed value. Pass your own with `textsignal=` or `textvariable=` to
share the field's text with another widget.

```python
text = ttk.Signal("")
qty = ttk.SpinnerEntry(app, textsignal=text, minvalue=0, maxvalue=10)
```

!!! tip "Commit semantics"
    Parsing, formatting, and `<<Change>>` only run on commit (focus
    out, **Enter**, or spin-button click), never on every keystroke.
    Bind `<<Input>>` if you need live updates as the user types.

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial value to display. |
| `values` | List of strings to cycle through (values mode). Mutually exclusive with `minvalue`/`maxvalue`. |
| `minvalue` | Inclusive lower bound (numeric mode). |
| `maxvalue` | Inclusive upper bound (numeric mode). |
| `increment` | Step size for spin buttons and arrow keys (default `1`). Numeric mode. |
| `wrap` | Whether the spinner wraps from `maxvalue` back to `minvalue` (and vice versa). Default `False`. |
| `value_format` | Format spec applied at commit time (`'currency'`, `'percent'`, ICU number patterns, …). Optional. |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `width` | Width of the entry in characters. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |
| `initial_focus` | Take focus on creation. |

```python
ttk.SpinnerEntry(app, label="Qty", minvalue=0, maxvalue=10)            # primary (default)
ttk.SpinnerEntry(app, label="Qty", minvalue=0, maxvalue=10, accent="success")
ttk.SpinnerEntry(app, label="Qty", minvalue=0, maxvalue=10, density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Numeric mode

`minvalue`, `maxvalue`, and `increment` define a numeric range. The
spin buttons and Up/Down keys move by `increment`; `wrap=True` makes
the spinner cycle past the boundary instead of clamping.

```python
ttk.SpinnerEntry(app, label="Retry limit",   value=3,    minvalue=0, maxvalue=10, increment=1)
ttk.SpinnerEntry(app, label="Volume",        value=50,   minvalue=0, maxvalue=100, increment=5)
ttk.SpinnerEntry(app, label="Hour",          value=12,   minvalue=0, maxvalue=23, increment=1, wrap=True)
ttk.SpinnerEntry(app, label="Price", value=9.99, minvalue=0, maxvalue=100, increment=0.01,
                 value_format="currency").pack()
```

<figure markdown>
![spinnerentry formatting](../../assets/dark/widgets-spinnerentry-formats.png#only-dark)
![spinnerentry formatting](../../assets/light/widgets-spinnerentry-formats.png#only-light)
</figure>

The spin buttons enforce `minvalue`/`maxvalue`, but **typing is not
clamped** — a user can type a value outside the range. Use a
validation rule (see below) when you need the field itself to reject
out-of-range input.

### Values mode

Provide a `values` list to cycle through fixed strings. Numeric
options are ignored in this mode.

```python
ttk.SpinnerEntry(
    app,
    label="Priority",
    value="Medium",
    values=["Low", "Medium", "High"],
)
```

The spin buttons step forward and backward through the list; `wrap`
controls whether stepping past either end cycles back around.

### Stepping

- Up / Down arrow keys — step by `increment` (numeric) or to the next/previous value (values mode).
- The spin buttons on the right of the entry — same as the arrow keys.
- Typing — always allowed unless the entry is set to readonly.

### Add-ons

Like other field controls, `SpinnerEntry` accepts prefix and suffix
add-ons via `insert_addon`. They slot in alongside the spin buttons
and inherit the field's disabled state.

```python
amount = ttk.SpinnerEntry(app, label="Amount", value=0, minvalue=0, maxvalue=10000)
amount.insert_addon(ttk.Label, position="before", text="$")
```

<figure markdown>
![spinnerentry addons](../../assets/dark/widgets-spinnerentry-addons.png#only-dark)
![spinnerentry addons](../../assets/light/widgets-spinnerentry-addons.png#only-light)
</figure>

### Disable, enable, readonly

```python
qty.disable()        # not editable, not focusable; spin buttons disable too
qty.enable()
qty.readonly(True)   # focusable, copyable, not editable; spin buttons still work
qty.readonly(False)
```

---

## Events

`SpinnerEntry` emits the same events as `Field`. There are no
dedicated `<<Increment>>` / `<<Decrement>>` events — a spin-button
click commits a new value and fires `<<Change>>` like any other commit.

**Input and value events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value differs from focus-in value, including spin-button steps | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |

```python
def show_committed(event):
    print("new value:", event.data["value"])

qty.on_changed(show_committed)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

!!! tip "Live vs committed"
    Use `on_input` for live previews. Use `on_changed` when you only
    care about the final value the user settled on.

---

## Validation and constraints

Rules are added with `add_validation_rule(rule_type, **kwargs)` and
run automatically on key release and blur. Built-in rule types are
`'required'`, `'pattern'`, `'stringLength'`, and `'custom'`. There is
no built-in numeric-range rule — `minvalue` / `maxvalue` only constrain
the spin buttons, not what the user can type. Express bounds with
`'custom'` against the parsed value.

```python
qty = ttk.SpinnerEntry(app, label="Quantity", value=1, minvalue=1, maxvalue=99, required=True)

# Reject typed values that fall outside the range
def in_range(_v):
    try:
        n = int(qty.get())
    except (TypeError, ValueError):
        return False
    return 1 <= n <= 99

qty.add_validation_rule(
    "custom",
    func=in_range,
    message="Enter a whole number between 1 and 99",
)
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`. Each rule type has a default trigger (`'always'`,
`'blur'`, or `'manual'`); pass `trigger=...` to override.

If you need numeric input with built-in bounds enforcement on typing —
not just on stepping — prefer [`NumericEntry`](numericentry.md), which
clamps typed values against `minvalue`/`maxvalue`.

---

## When should I use SpinnerEntry?

Use `SpinnerEntry` when:

- stepping is the primary interaction (retry counts, hour-of-day, priority levels).
- users frequently nudge a value up or down rather than typing it.
- you want visible spin buttons as an affordance.
- you need a small, fixed list of cycling values (Low/Medium/High, Mon/Tue/Wed, …).

Prefer a different control when:

- users primarily type numbers and want bounds enforced on typing → use [NumericEntry](numericentry.md).
- the value is continuous and benefits from a slider → use [Scale](scale.md).
- the list is large or selection is the main interaction → use [SelectBox](../inputs/selectbox.md).
- the field is plain text → use [TextEntry](textentry.md).

---

## Related widgets

- [NumericEntry](numericentry.md) — numeric input with bounds clamping on typing.
- [Spinbox](../primitives/spinbox.md) — low-level stepper primitive (no label, message, or validation).
- [Scale](scale.md) — slider-based numeric adjustment.
- [SelectBox](../inputs/selectbox.md) — dropdown picker for larger lists.
- [TextEntry](textentry.md) — base composite text field; `SpinnerEntry` shares its formatting/validation/signal machinery.
- [Form](../forms/form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.SpinnerEntry`](../../reference/widgets/SpinnerEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Formatting](../../guides/formatting.md)
    - [Localization](../../capabilities/localization.md)
    - [Signals](../../capabilities/signals/signals.md)
