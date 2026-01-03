---
title: PasswordEntry
---

# PasswordEntry

`PasswordEntry` is a secure, form-ready text input control for passwords, PINs, and other sensitive values.

It builds on `TextEntry`, adding masking, optional reveal behavior, and password-specific validation patterns—while preserving
the same label/message, localization, and event model used throughout ttkbootstrap v2.

---

## Quick start

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

## When to use

Use `PasswordEntry` when:

- the input should not be displayed in clear text

- you want consistent form UX (label/message/validation/events)

Consider a different control when:

- masking is not required — use [TextEntry](textentry.md)

- the input is numeric-only (PINs with numeric constraints) — use [NumericEntry](numericentry.md)

---

## Appearance

### `accent`

```python
ttk.PasswordEntry(app, label="Password")  # primary (default)
ttk.PasswordEntry(app, label="Password", accent="secondary")
ttk.PasswordEntry(app, label="Password", accent="success")
ttk.PasswordEntry(app, label="Password", accent="warning")
```

!!! link "Design System"
    For a complete list of available colors and styling options, see the [Design System](../../design-system/index.md) documentation.

---

## Examples and patterns

### Value model

PasswordEntry separates **what is displayed** from **what is stored**.

| Concept | Meaning |
|---|---|
| Text | Masked display text |
| Value | Actual committed password value |

```python
secret = pwd.value   # committed value
raw = pwd.get()      # raw internal text
```

The reveal toggle changes only the display, never the underlying value.

### Common options

#### `required`, `message`, `accent`

```python
ttk.PasswordEntry(app, label="Password", required=True, message="Minimum 8 characters")
```

#### Reveal toggle: `show_visibility_toggle`

```python
pwd = ttk.PasswordEntry(app, label="Password", show_visibility_toggle=False)
```

#### Add-ons

```python
pwd.insert_addon(ttk.Label, position="before", icon="lock", icon_only=True)
```

### Events

PasswordEntry emits the standard field events:

- `<<Input>>` / `on_input` — editing

- `<<Changed>>` / `on_changed` — committed value changed

- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

```python
def handle_changed(event):
    print("Password updated")

pwd.on_changed(handle_changed)
```

!!! tip "Event usage"
    Use `on_input(...)` for live UX feedback (e.g., strength meters).
    Use `on_changed(...)` for authentication or submission logic.

### Validation

Password validation is typically applied **on commit**, not per keystroke.

```python
pwd = ttk.PasswordEntry(app, label="Password", required=True)
pwd.add_validation_rule("min_length", 8, message="Minimum 8 characters")
```

Common patterns include:

- required

- minimum length

- character class rules

- confirmation match (cross-field rule)

---

## Behavior

- Characters are masked while typing.

- A reveal button is shown by default (configurable).

- Commit semantics match other field controls (blur or Enter).

---

## Localization

`PasswordEntry` inherits the localization capabilities from `TextEntry`. Labels, messages, and validation feedback can be localized for different languages.

!!! link "Localization"
    For complete localization configuration and supported formats, see the [Localization](../../capabilities/localization.md) documentation.

---

## Reactivity

`PasswordEntry` integrates with the signals system for reactive data binding. Changes to the field value can automatically propagate to other parts of your application.

!!! link "Signals"
    For details on reactive patterns and data binding, see the [Signals](../../capabilities/signals/signals.md) documentation.

---

## Additional resources

### Related widgets

- [TextEntry](textentry.md) — general text field
- [NumericEntry](numericentry.md) — numeric input with validation
- [Form](../forms/form.md) — structured field layout and submission

### Framework concepts

- [Forms](../../guides/forms.md) — working with form controls
- [Localization](../../capabilities/localization.md) — internationalization and formatting
- [Signals](../../capabilities/signals/signals.md) — reactive data binding

### API reference

- [`ttkbootstrap.PasswordEntry`](../../reference/widgets/PasswordEntry.md)