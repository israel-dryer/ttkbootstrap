---
title: TextEntry
---

# TextEntry

`TextEntry` is a form-ready text input that combines a label, an entry
field, and a message line into a single composite widget. It builds on
[`Entry`](../primitives/entry.md) and adds locale-aware parsing,
validation, signal/variable binding, and prefix/suffix add-ons — the
features that turn a bare input into a real form field.

The committed value is whatever string the user typed; with
`value_format` set, the text is parsed at commit time into a typed
result (number, date, percent, etc.) so downstream code never has to
interpret raw input.

<figure markdown>
![textentry states](../../assets/dark/widgets-textentry-states.png#only-dark)
![textentry states](../../assets/light/widgets-textentry-states.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

name = ttk.TextEntry(
    app,
    label="Name",
    message="Enter your full name",
    required=True,
)
name.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

`TextEntry` separates **what is in the field right now** from **the
committed value**:

| Concept | Meaning | How to read it |
|---|---|---|
| Text | The raw editable string in the entry, updated on every keystroke. | `entry.get()` |
| Value | The parsed result of that text — produced when the user blurs the field or presses **Enter**. | `entry.value` |

Without `value_format`, the value is the same string the user typed —
or `None` for an empty field. With `value_format`, the text is parsed
on commit into the corresponding type (`Decimal`, `date`, `float`, …)
and reformatted for display.

```python
entry = ttk.TextEntry(app)
entry.value = "Ada Lovelace"   # set committed value
current = entry.value          # read committed value
raw = entry.get()              # read raw text any time
```

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

### Signals and variables

`TextEntry` exposes two reactive handles bound to the **raw text**, not
the parsed value:

- `entry.signal` — a `Signal[str]` for ttkbootstrap reactive bindings.
- `entry.variable` — a Tk `Variable` for legacy code.

Pass your own with `textsignal=` or `textvariable=` to share the field's
text with another widget or to drive it from elsewhere.

```python
text = ttk.Signal("")
entry = ttk.TextEntry(app, textsignal=text)
```

!!! tip "Commit semantics"
    Parsing, formatting, and `<<Change>>` only run on commit (focus out
    or **Enter**), never on every keystroke. Bind `<<Input>>` if you
    need live updates as the user types.

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial committed value. |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below the entry; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `value_format` | Locale-aware format spec applied at commit time (`'currency'`, `'shortDate'`, `'percent'`, ICU number patterns, …). |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `show` | Mask character for sensitive input (e.g. `'*'`). |
| `width` | Width of the entry in characters. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |
| `initial_focus` | Take focus on creation. |

```python
ttk.TextEntry(app)                     # primary (default)
ttk.TextEntry(app, accent="success")
ttk.TextEntry(app, density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Add-ons

`insert_addon` places a `Label`, `Button`, or `CheckButton` inside the
field — before or after the entry. The add-on inherits the field's
disabled state and contributes to focus styling.

```python
email = ttk.TextEntry(app, label="Email")
email.insert_addon(ttk.Label, position="before", icon="envelope")

def handle_search():
    ...

search = ttk.TextEntry(app)
search.insert_addon(ttk.Button, position="after", icon="search", command=handle_search)
```

<figure markdown>
![addons](../../assets/dark/widgets-textentry-addons.png#only-dark)
![addons](../../assets/light/widgets-textentry-addons.png#only-light)
</figure>

!!! note "Power feature"
    Several specialized entry widgets (PasswordEntry, PathEntry, …)
    are built on top of TextEntry's add-on mechanism.

### Disable, enable, readonly

```python
entry = ttk.TextEntry(app)
entry.disable()        # not editable, not focusable
entry.enable()
entry.readonly(True)   # focusable, copyable, not editable
entry.readonly(False)  # back to normal
```

### Locale-aware reformatting

When `value_format` is set, the committed value is parsed and
formatted using the active locale. If the locale changes at runtime,
the displayed text is reformatted automatically — the underlying value
is unchanged.

```python
ttk.TextEntry(app, label="Currency", value=1234.56, value_format="currency").pack()
ttk.TextEntry(app, label="Short date", value="March 14, 1981", value_format="shortDate").pack()
```

<figure markdown>
![localized](../../assets/dark/widgets-textentry-localization.png#only-dark)
![localized](../../assets/light/widgets-textentry-localization.png#only-light)
</figure>

!!! link "See [Localization](../../capabilities/localization.md) for the available format specs and locale handling."

---

## Events

`TextEntry` emits virtual events with structured payloads. Each one
has a matching `on_*` / `off_*` helper for ergonomic registration.

**Input and value events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value differs from focus-in value | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |

```python
def show_typing(event):
    print("typing:", event.data["text"])

def show_committed(event):
    print("committed:", event.data["value"])

entry = ttk.TextEntry(app)
entry.on_input(show_typing)
entry.on_changed(show_committed)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

```python
def warn(payload):
    print("invalid:", payload["message"])

entry.on_invalid(warn)
```

!!! tip "Live vs committed"
    Use `on_input` for live previews (counters, search filters). Use
    `on_changed` when you only care about the final value the user
    settled on.

---

## Validation and constraints

Rules are added with `add_validation_rule(rule_type, **kwargs)` and run
automatically on key release and blur. Built-in rule types are
`'required'`, `'email'`, `'pattern'`, `'stringLength'`, and `'custom'`.

```python
email = ttk.TextEntry(app, label="Email", required=True)
email.add_validation_rule("email", message="Enter a valid email address")

username = ttk.TextEntry(app, label="Username")
username.add_validation_rule("stringLength", min=3, max=20)

zipcode = ttk.TextEntry(app, label="Zip")
zipcode.add_validation_rule("pattern", pattern=r"^\d{5}(-\d{4})?$")

age = ttk.TextEntry(app, label="Age")
age.add_validation_rule("custom", func=lambda v: v.isdigit() and int(v) >= 18,
                         message="Must be 18 or older")
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`. Each rule type has a default trigger (`'always'`,
`'blur'`, or `'manual'`); pass `trigger=...` to override.

`add_validation_rules(rules)` replaces the entire rule set — useful
when constraints depend on another field's value:

```python
country = ttk.TextEntry(app, label="Country")
postal = ttk.TextEntry(app, label="Postal code")

def update_postal_rules(event):
    if event.data["value"] == "US":
        postal.add_validation_rules([
            ttk.ValidationRule("pattern", pattern=r"^\d{5}$"),
        ])

country.on_changed(update_postal_rules)
```

If you need per-keystroke filtering — blocking characters as the user
types — use Tk's low-level `validate` / `validatecommand` on the
underlying [`Entry`](../primitives/entry.md) instead. `TextEntry`'s
rule system is designed around commit-time validation.

---

## When should I use TextEntry?

Use `TextEntry` when:

- you want a form-ready text field with label, message, and validation built in.
- you need locale-aware parsing and formatting (currency, dates, decimals).
- you want consistent commit semantics (`<<Change>>` on blur or **Enter**) across the fields in a form.

Prefer a different control when:

- you need raw `ttk.Entry` behavior with no chrome → use [Entry](../primitives/entry.md).
- the field collects a number → use [NumericEntry](numericentry.md).
- the field collects a password → use [PasswordEntry](passwordentry.md).
- the field collects a date or time → use [DateEntry](dateentry.md) or [TimeEntry](timeentry.md).
- the field collects a file or directory path → use [PathEntry](pathentry.md).
- the field needs to step through preset values → use [SpinnerEntry](spinnerentry.md).

---

## Related widgets

- [Entry](../primitives/entry.md) — low-level text input primitive (no label, message, or validation).
- [NumericEntry](numericentry.md) — numeric input with bounds and stepping.
- [PasswordEntry](passwordentry.md) — masked text input.
- [PathEntry](pathentry.md) — file or directory path input.
- [DateEntry](dateentry.md) — calendar-backed date input.
- [TimeEntry](timeentry.md) — time-of-day input.
- [SpinnerEntry](spinnerentry.md) — entry that steps through values.
- [Form](form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.TextEntry`](../../reference/widgets/TextEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Localization](../../capabilities/localization.md)
    - [Signals](../../capabilities/signals/signals.md)
