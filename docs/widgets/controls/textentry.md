---
title: TextEntry
icon: fontawesome/solid/i-cursor
---

# TextEntry

`TextEntry` is a fully featured input control including a label, input, and message text.

It builds on Tkinter’s native `ttk.Entry`, but adds the things you almost always need in practice.

If you are building forms, dialogs, or data-driven UIs, `TextEntry` should usually be your **default text input**.

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

## What problem does TextEntry solve?

The native `Entry` widget is intentionally low-level:

- No label
- No validation
- No helper or error messaging
- No consistent change events
- No localization support

`TextEntry` wraps those concerns into a **single control** so every text field in your app behaves the same way.

---

## Text vs value

`TextEntry` separates **what the user is typing** from **the committed value**.

| Concept | Meaning |
|-------|---------|
| Text  | Raw, editable display text |
| Value | Parsed, validated value committed on blur or Enter |

```python
# committed value
current = name.value

# update value programmatically
name.value = "Alice"
```

If you need the raw text while the user is typing:

```python
raw = name.get()
```

---

## Labels and messages

```python
field = ttk.TextEntry(
    app,
    label="Username",
    message="Must be at least 6 characters",
)
field.pack(fill="x", padx=20, pady=10)
```

Messages are commonly used for:

- Helper text
- Validation errors
- Status hints

---

## Validation

### Required fields

```python
email = ttk.TextEntry(app, label="Email", required=True)
email.pack(fill="x", padx=20, pady=10)
```

### Custom validation rules

```python
email.add_validation_rule(
    "email",
    message="Enter a valid email address"
)
```

Validation results are reflected visually and via events.

---

## Formatting with `value_format`

`TextEntry` supports powerful, locale-aware formatting via the `value_format` option.

This allows you to:
- accept flexible user input (strings, numbers, dates)
- normalize and parse it into a committed value
- reformat it for display when the user finishes editing

Formatting is applied **on commit** (blur or Enter), so it never interferes with typing.

### Named formats

In v2, `value_format` supports a set of **semantic format names**.
These formats automatically apply the correct parsing and display rules
based on the active locale.

<figure markdown>
![localized](../../assets/dark/widgets-textentry-localization.png#only-dark)
![localized](../../assets/light/widgets-textentry-localization.png#only-light)
</figure>

```python
ttk.TextEntry(
    r3,
    label="Currency",
    value=1234.56,
    value_format="currency",
).pack(side="left", padx=10)

ttk.TextEntry(
    r3,
    label="Short Date",
    value="March 14, 1981",
    value_format="shortDate",
).pack(side="left", padx=10)

ttk.TextEntry(
    r3,
    label="Fixed Point",
    value=15422354,
    value_format="fixedPoint",
).pack(side="left", padx=10)
```

!!! tip "Flexible input"
    The initial `value` does not need to be pre-formatted.
    Strings, numbers, and date-like values are parsed and normalized automatically.

!!! note "Text vs value (revisited)"
    `value_format` controls **how the committed value is displayed**.
    While the field is focused, the user edits raw text.
    When the value is committed, it is parsed, validated, and reformatted.

---

## Events

`TextEntry` emits structured virtual events with related `on_*` and `off_*` convenience bindings:

- `<<Input>>` — every keystroke
- `<<Changed>>` — committed value changed
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

Example:

```python
def on_event(event):
    print("new value:", event.data["value"])

name.on_input(on_event)
name.on_changed(on_event)
name.on_valid(on_event)
```

---

## Add-ons (prefix / suffix widgets)

Because `TextEntry` is a field control, you can insert widgets inside its layout. This is a **powerful** feature that allows you
to create customized and specialized entry fields.

<figure markdown>
![addons](../../assets/dark/widgets-textentry-addons.png#only-dark)
![addons](../../assets/light/widgets-textentry-addons.png#only-light)
</figure>

```python
# email entry
email = ttk.TextEntry(app, label="Email")
email.insert_addon(ttk.Label, position="before", icon="envelope")
email.pack(side="left", padx=10, anchor="s")

def handle_search():
    ...

search = ttk.TextEntry(app)
search.insert_addon(ttk.Button, position="after", icon="search", command=handle_search)
search.pack(side="left", padx=10, anchor="s")
```

!!! note "Power Play"
    Most of the specialized _Entry_ widgets in v2 have been created using this very method.

---

## Localization

Localization behavior is controlled by the **global application settings**.

By default, widgets use `localize="auto"`. In this mode, `label`, `message`, and `text` are treated as localization
keys **when a translation exists**. If a key is not found in the active message catalog, the widget falls back to using
the value as **plain text**.

You can override this behavior per widget if needed.

```python
# uses global app localization settings (default)
ttk.TextEntry(app, label="user.name", message="user.name.help").pack(fill="x")

# explicitly enable localization for this widget
ttk.TextEntry(app, label="user.name", localize=True).pack(fill="x")

# explicitly disable localization (always treat strings as literals)
ttk.TextEntry(app, label="Name", message="Enter your full name", localize=False).pack(fill="x")
```

!!! tip "Safe to pass literal text"
    With `localize="auto"`, you can mix localization keys and literal strings.
    If no translation is found, the string is shown as-is.

---

## When should I use TextEntry?

Use `TextEntry` when:

- you want a **full-featured text field**
- you need validation, messages, or formatting
- you’re building forms or dialogs

Use the base `Entry` widget when:

- you need the lowest-level ttk behavior
- you are building a custom composite widget

---

## Related widgets

- **NumericEntry** — numeric input with bounds and stepping
- **PasswordEntry** — obscured text input
- **DateEntry** / **TimeEntry** — structured date/time input
- **Form** — build complete forms from field definitions
