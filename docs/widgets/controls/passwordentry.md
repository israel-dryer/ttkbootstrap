---
title: PasswordEntry
icon: fontawesome/solid/lock
---

# PasswordEntry

`PasswordEntry` is a **secure, high-level text input control** for passwords, PINs, and other sensitive values.

It builds on `TextEntry`, adding masking, optional reveal behavior, and password-specific validation patterns — while preserving
the same label, message, validation, localization, and event model used throughout ttkbootstrap v2.

Use `PasswordEntry` whenever user input should **not be displayed in clear text**.

> _Image placeholder:_  
> `![PasswordEntry overview](../_img/widgets/passwordentry/overview.png)`  
> Suggested shot: masked field + reveal toggle + validation message.

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

## What problem does PasswordEntry solve?

A plain `Entry` can mask characters, but applications usually need more:

- consistent masking behavior
- validation feedback (length, complexity)
- reveal / hide interaction
- consistent change events
- form-friendly behavior

`PasswordEntry` standardizes these concerns so password fields behave the same everywhere.

---

## Masking behavior

By default, typed characters are hidden using a mask character.

```python
pwd = ttk.PasswordEntry(app, label="Password")
```

The mask is applied only to the **displayed text** — the committed value remains accessible programmatically.

---

## Text vs value

Like other entry controls, `PasswordEntry` separates **what is shown** from **what is stored**.

| Concept | Meaning |
|------|---------|
| Text | Masked display text |
| Value | Actual password value |

```python
secret = pwd.value      # committed value
raw = pwd.get()         # raw internal text
```

---

## Reveal / hide behavior

Many applications allow users to temporarily reveal their password.

If supported by your implementation, this may be exposed via:

- a suffix button
- a toggle icon
- programmatic control

```python
pwd = ttk.PasswordEntry(
    app,
    label="Password",
    reveal=True,   # example option
)
```

> _Image placeholder:_  
> `![PasswordEntry reveal](../_img/widgets/passwordentry/reveal.png)`

---

## Validation

Password validation is typically applied on **commit**, not per keystroke.

```python
pwd = ttk.PasswordEntry(app, label="Password", required=True)
pwd.add_validation_rule("min_length", 8, message="Minimum 8 characters")
```

Common validation rules include:

- required
- minimum length
- character class rules
- confirmation match

---

## Events

`PasswordEntry` emits the same field events as other entry widgets:

- `<<Input>>` — text editing
- `<<Changed>>` — committed value changed
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

Use the convenience helpers instead of manual `bind(...)` calls.

```python
def handle_changed(event):
    print("Password updated")

pwd.on_changed(handle_changed)
```

!!! tip "Live Typing"
    Use `on_input(...)` only for UX feedback (e.g., strength meters).  
    Use `on_changed(...)` for authentication or submission logic.

---

## Add-ons

You can add prefix or suffix widgets just like other entry controls.

```python
pwd.insert_addon(ttk.Label, position="before", text="🔒")
```

---

## When should I use PasswordEntry?

Use `PasswordEntry` when:

- input should be masked
- validation rules apply
- values are sensitive
- fields participate in a form

Use `TextEntry` when:

- masking is not required
- input is descriptive rather than secret

---

## Related widgets

- **TextEntry** — general text field
- **NumericEntry** — numeric input
- **Form** — structured field layout and submission
