---
title: TextEntry
---

# TextEntry

`TextEntry` is a form-ready text input control that combines a **label**, **input field**, and **message region**.

It builds on `ttk.Entry`, but adds the features you typically need in real applications: validation, messages, formatting,
localization, and consistent field events. If you’re building forms or dialogs, `TextEntry` is usually your default text input. fileciteturn13file1

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

Entry-based field controls separate **what the user is typing** from the **committed value**.

| Concept | Meaning |
|---|---|
| Text | Raw, editable string while the field is focused |
| Value | The committed value (after parsing/validation on blur or Enter) |

```python
current = name.value      # committed value
raw = name.get()          # raw text at any time

name.value = "Ada Lovelace"
```

!!! tip "Commit semantics"
    Parsing, validation, and `value_format` are applied only when the value is committed (blur or Enter),
    never on every keystroke.

---

## Common options

### `label`, `message`, `required`

```python
ttk.TextEntry(app, label="Email", message="We'll never share it.", required=True)
```

### `bootstyle`

```python
ttk.TextEntry(app)  # primary (default)
ttk.TextEntry(app, bootstyle="secondary")
ttk.TextEntry(app, bootstyle="success")
ttk.TextEntry(app, bootstyle="warning")
```

### `value_format`

Commit-time formatting using semantic format names.

```python
ttk.TextEntry(app, label="Currency", value=1234.56, value_format="currency").pack()
ttk.TextEntry(app, label="Short Date", value="March 14, 1981", value_format="shortDate").pack()
```

<figure markdown>
![localized](../../assets/dark/widgets-textentry-localization.png#only-dark)
![localized](../../assets/light/widgets-textentry-localization.png#only-light)
</figure>

---

## Behavior

### Prefix/suffix add-ons

You can insert widgets into the field as add-ons.

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
    Many specialized Entry widgets in v2 are built using this add-on mechanism.

### Validation rules

```python
email = ttk.TextEntry(app, label="Email", required=True)

email.add_validation_rule(
    "email",
    message="Enter a valid email address"
)
```

Validation results are reflected visually and via events.

---

## Events

`TextEntry` emits structured virtual events with matching convenience methods:

- `<<Input>>` — live typing
- `<<Changed>>` — committed value changed
- `<<Valid>>`, `<<Invalid>>`, `<<Validated>>`

```python
def on_event(event):
    print("new value:", event.data["value"])

name.on_input(on_event)
name.on_changed(on_event)
name.on_valid(on_event)
```

!!! tip "Live typing"
    Use `on_input(...)` when you want live typing behavior, and `on_changed(...)` when you care about committed values.

---

## Validation and constraints

Use validation rules when:

- the field is required
- values must match a pattern (email, phone, etc.)
- multiple fields must be consistent (cross-field rules)

If you need immediate, per-keystroke constraints, use low-level Tk validation on **Entry** instead.

---

## When should I use TextEntry?

Use `TextEntry` when:

- you want a form-ready text field (label + message + validation)
- you want consistent events and commit semantics
- you want optional localization and formatting

Prefer **Entry** when:

- you need the lowest-level `ttk.Entry` behavior and options
- you are building your own composite control

---

## Related widgets

- **Entry** — low-level primitive text input
- **NumericEntry** — numeric input with bounds and stepping
- **PasswordEntry** — obscured text input
- **DateEntry** / **TimeEntry** — structured date/time input
- **Form** — build complete forms from field definitions

---

## Reference

- **API Reference:** `ttkbootstrap.TextEntry`
- **Related guides:** Forms, Internationalization → Localization, Events & Signals → Signals
