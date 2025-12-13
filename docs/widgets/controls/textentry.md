---
title: TextEntry
icon: fontawesome/solid/i-cursor
---

# TextEntry

`TextEntry` is a **high-level text input control** designed for real-world desktop applications.

It builds on Tkinter’s native `Entry`, but adds the things you almost always need in practice:

- A **label** and **message** area
- **Validation** and validation feedback
- Optional **localization** and **formatting**
- Structured **virtual events**
- A consistent layout that works in forms and dialogs

If you are building forms, dialogs, or data-driven UIs, `TextEntry` should usually be your **default text input**.

> _Image placeholder:_  
> `![TextEntry overview](../_img/widgets/textentry/overview.png)`  
> Suggested shot: label + entry + helper message + error state.

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

## Formatting & localization

You can apply formatting when the value is committed.

```python
amount = ttk.TextEntry(
    app,
    label="Amount",
    value=1234.56,
    value_format="$#,##0.00",
    locale="en_US",
)
amount.pack(fill="x", padx=20, pady=10)
```

This is especially useful when you want **display formatting** without interfering with typing.

---

## Events

`TextEntry` emits structured virtual events:

- `<<Input>>` — every keystroke
- `<<Changed>>` — committed value changed
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

Example:

```python
def on_changed(event):
    print("new value:", event.data["value"])

name.bind("<<Changed>>", on_changed)
```

---

## Add-ons (prefix / suffix widgets)

Because `TextEntry` is a field control, you can insert widgets inside its layout.

```python
search = ttk.TextEntry(app, label="Search")
search.insert_addon(ttk.Button, position="after", text="Go")
search.pack(fill="x", padx=20, pady=10)
```

> _Image placeholder:_  
> `![TextEntry addon](../_img/widgets/textentry/addon.png)`

---

## Localization

If you use message catalogs, `localize="auto"` (or `True`) treats `label`, `message`, and `text` as translation keys.

```python
ttk.TextEntry(
    app,
    label="user.name",
    message="user.name.help",
    localize="auto",
).pack(fill="x")
```

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
