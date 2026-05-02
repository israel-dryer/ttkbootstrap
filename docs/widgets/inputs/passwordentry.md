---
title: PasswordEntry
---

# PasswordEntry

`PasswordEntry` is a form-ready masked text input for passwords, PINs,
and other sensitive values. It extends [`TextEntry`](textentry.md) with
two password-specific behaviors: characters are replaced by a mask
glyph (`•` by default) as the user types, and an inline visibility
button reveals the cleartext while it is held down.

The committed value is the user's raw string — masking changes only
the display, never the underlying value. All other field machinery
(label, message, validation, signal/variable binding, accent, density,
add-ons) is inherited unchanged from `TextEntry`.

<figure markdown>
![passwordentry](../../assets/dark/widgets-passwordentry.png#only-dark)
![passwordentry](../../assets/light/widgets-passwordentry.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

pwd = ttk.PasswordEntry(
    app,
    label="Password",
    required=True,
    message="Must be at least 8 characters",
)
pwd.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Value model

`PasswordEntry` separates **what is shown on screen** from **what is
stored**:

| Concept | Meaning | How to read it |
|---|---|---|
| Display | The masked glyphs visible in the field. | n/a — for the user only |
| Text | The raw editable string, updated on every keystroke. | `pwd.get()` |
| Value | The committed string — the value at focus-in is set on blur or **Enter**. | `pwd.value` |

The reveal button changes the display only; `pwd.value` and `pwd.get()`
always return the actual characters the user typed.

### Empty values

When the field is empty:

- with `allow_blank=True` (the default), the committed value is `None`.
- with `allow_blank=False`, the previous value is preserved on commit.

### Signals and variables

`pwd.signal` and `pwd.variable` are bound to the **raw text** — the
cleartext password, not the masked display. Pass your own with
`textsignal=` or `textvariable=` to share the value with another
widget.

```python
pw = ttk.Signal("")
pwd = ttk.PasswordEntry(app, textsignal=pw)
```

!!! warning "Sensitive data"
    The signal and variable carry the cleartext. Don't log them, mirror
    them into a visible widget, or persist them through a Tk variable
    that survives the dialog. Read `pwd.value` at submit time and clear
    the field afterwards if you need to be careful.

---

## Common options

| Option | Purpose |
|---|---|
| `value` | Initial committed value. |
| `label` | Text shown above the entry. |
| `message` | Helper text shown below; replaced by validation errors. |
| `required` | Adds an asterisk to the label and a `'required'` validation rule. |
| `show_visibility_toggle` | Show or hide the inline reveal button (default `True`). |
| `show` | Mask character (default `'•'`). |
| `allow_blank` | Whether an empty input commits as `None` (default) or preserves the previous value. |
| `width` | Width of the entry in characters. |
| `state` | `'normal'`, `'disabled'`, or `'readonly'`. |
| `accent` | Semantic color token for the focus ring (`primary`, `success`, `danger`, …). |
| `density` | `'default'` or `'compact'` for tight forms. |
| `textsignal` / `textvariable` | External signal or Tk variable bound to the raw text. |
| `initial_focus` | Take focus on creation. |

```python
ttk.PasswordEntry(app, label="Password")                    # primary (default)
ttk.PasswordEntry(app, label="Password", accent="success")
ttk.PasswordEntry(app, label="Password", density="compact")
```

!!! link "See [Design System](../../design-system/index.md) for the full set of accent and density tokens."

---

## Behavior

### Masking

Every typed character is replaced by `show` (default `'•'`) on screen.
The mask is purely cosmetic: copy/paste, selection, and the underlying
value all use the cleartext. To change the mask glyph:

```python
pin = ttk.PasswordEntry(app, label="PIN", show="*")
```

### Visibility toggle

The inline eye icon after the entry is a **press-and-hold** control,
not a click toggle. The cleartext is visible only while the button is
actively pressed; releasing or moving focus away re-masks the field.
The icon swaps to a struck-through eye while pressed.

This is intentional — it lets a user verify a typo without leaving the
field exposed if they walk away.

```python
pwd = ttk.PasswordEntry(app, label="Password", show_visibility_toggle=False)
pwd.configure(show_visibility_toggle=True)   # show it again later
```

### Add-ons

Like other field controls, `PasswordEntry` accepts prefix and suffix
add-ons via `insert_addon`. They share the field's disabled state and
focus styling, and slot in alongside the visibility toggle.

```python
pwd = ttk.PasswordEntry(app, label="Password")
pwd.insert_addon(ttk.Label, position="before", icon="lock", icon_only=True)
```

### Disable, enable, readonly

```python
pwd.disable()        # not editable, not focusable; toggle disables too
pwd.enable()
pwd.readonly(True)   # focusable, copyable, not editable
pwd.readonly(False)
```

---

## Events

`PasswordEntry` emits the same events as [`TextEntry`](textentry.md);
the masking and reveal button do not fire their own.

**Input and value events** (callback receives the raw event;
read `event.data`):

| Event | Helper | Fires when… | `event.data` |
|---|---|---|---|
| `<<Input>>` | `on_input` | every keystroke | `{'text': str}` |
| `<<Change>>` | `on_changed` | committed value differs from focus-in value | `{'value', 'prev_value', 'text'}` |
| `<Return>` | `on_enter` | **Enter** pressed in the field | `{'value', 'text'}` |

```python
def update_strength_meter(event):
    text = event.data["text"]
    meter.set(score(text))

def submit(event):
    authenticate(event.data["value"])

pwd.on_input(update_strength_meter)
pwd.on_enter(submit)
```

**Validation events** (callback receives the payload `dict` directly):

| Event | Helper | Fires when… | Payload |
|---|---|---|---|
| `<<Valid>>` | `on_valid` | validation passes | `{'value', 'is_valid': True, 'message': ''}` |
| `<<Invalid>>` | `on_invalid` | validation fails | `{'value', 'is_valid': False, 'message': str}` |
| `<<Validate>>` | `on_validated` | after any validation | `{'value', 'is_valid': bool, 'message': str}` |

!!! tip "Live vs committed"
    Use `on_input` for live feedback like strength meters. Use
    `on_changed` or `on_enter` for authentication or submission — they
    fire only on the value the user settled on.

---

## Validation and constraints

Rules are added with `add_validation_rule(rule_type, **kwargs)` and
run automatically on key release and blur. Built-in rule types are
`'required'`, `'pattern'`, `'stringLength'`, and `'custom'`.

```python
pwd = ttk.PasswordEntry(app, label="Password", required=True)

# At least 8 characters
pwd.add_validation_rule("stringLength", min=8, message="Minimum 8 characters")

# Must contain a digit and an uppercase letter
pwd.add_validation_rule(
    "pattern",
    pattern=r"(?=.*\d)(?=.*[A-Z]).+",
    message="Must include a digit and an uppercase letter",
)

# Custom rule on the parsed value
pwd.add_validation_rule(
    "custom",
    func=lambda v: v not in COMMON_PASSWORDS,
    message="That password is too common",
)
```

A failed rule replaces the message line with the rule's error text and
emits `<<Invalid>>`. A passing rule restores the original message and
emits `<<Valid>>`.

### Confirmation fields

Cross-field rules — "this must equal that" — aren't a built-in rule
type. Wire them up with `on_changed` on the confirm field:

```python
pwd     = ttk.PasswordEntry(app, label="Password", required=True)
confirm = ttk.PasswordEntry(app, label="Confirm password", required=True)

confirm.add_validation_rule(
    "custom",
    func=lambda v: v == pwd.value,
    message="Passwords do not match",
)

# Re-validate the confirm field whenever the primary changes
pwd.on_changed(lambda e: confirm.validate())
```

If you need per-keystroke filtering — blocking characters as the user
types — use Tk's low-level `validate` / `validatecommand` on the
underlying [`Entry`](../primitives/entry.md). `PasswordEntry`'s rule
system is designed around commit-time validation.

---

## When should I use PasswordEntry?

Use `PasswordEntry` when:

- the field collects a value that should not be visible on screen (passwords, PINs, recovery codes).
- you want the reveal-while-held UX to verify input without leaving cleartext exposed.
- the field needs the same form chrome (label, message, validation) as the other inputs in the form.

Prefer a different control when:

- the field is plain text → use [TextEntry](textentry.md).
- the input is a numeric PIN with bounds and stepping → use [NumericEntry](numericentry.md).
- the field collects a one-time code split across digits → that's a custom widget, not `PasswordEntry`.

---

## Related widgets

- [TextEntry](textentry.md) — base composite text field that `PasswordEntry` extends.
- [NumericEntry](numericentry.md) — numeric input with bounds and stepping.
- [Entry](../primitives/entry.md) — low-level text input primitive (no label, message, or validation).
- [Form](form.md) — assemble a full form from field declarations.

---

## Reference

- **API reference:** [`ttkbootstrap.PasswordEntry`](../../reference/widgets/PasswordEntry.md)
- **Related guides:**
    - [Forms](../../guides/forms.md)
    - [Localization](../../capabilities/localization.md)
    - [Signals](../../capabilities/signals/signals.md)
