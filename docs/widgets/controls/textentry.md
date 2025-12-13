---
title: TextEntry
icon: fontawesome/solid/i-cursor
---


# TextEntry

`TextEntry` is a **high-level text input control** designed for real-world desktop applications.  
It builds on Tkinter’s native `Entry` widget, adding labels, validation, localization, formatting, and structured
events — all in a single, reusable component.

If you are building forms, dialogs, or data-driven UIs, `TextEntry` should usually be your default text input.

---

## What problem does TextEntry solve?

Traditional `Entry` widgets are intentionally low-level:

- No label
- No validation
- No formatting
- No structured change events
- No built-in messaging

`TextEntry` wraps those concerns into a **single control** that behaves consistently across your application.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

entry = ttk.TextEntry(
    app,
    label="Name",
    message="Enter your full name",
    required=True
)
entry.pack(fill="x", padx=20, pady=10)

app.mainloop()
```

---

## Input vs value

`TextEntry` separates **what the user is typing** from **the committed value**.

| Concept | Meaning                                            |
|---------|----------------------------------------------------|
| Text    | Raw, editable display text                         |
| Value   | Parsed, validated value committed on blur or Enter |

---

## Formatting & localization

```python
amount = ttk.TextEntry(
    app,
    label="Amount",
    value=1234.56,
    value_format="¤#,##0.00",
    locale="en_US"
)
amount.pack(fill="x")
```

---

## Validation

```python
email = ttk.TextEntry(app, label="Email", required=True)
email.add_validation_rule("email", message="Invalid email address")
email.pack(fill="x")
```

---

## Add-ons

```python
search = ttk.TextEntry(app, label="Search")
search.insert_addon(ttk.Button, "after", text="Go")
search.pack(fill="x")
```

---

## When should I use TextEntry?

Use `TextEntry` for most application text input.  
Use `Entry` when you need a minimal, raw ttk widget.

---

## Related widgets

- NumericEntry
- PasswordEntry
- DateEntry
- TimeEntry
- Form
