---
title: Entry
---

# Entry

`Entry` is the low-level, single-line text input primitive in ttkbootstrap.

It wraps `ttk.Entry` and integrates ttkbootstrap styling plus reactive text support. `Entry` is also the building block
used by higher-level controls like `TextEntry`, `NumericEntry`, `DateEntry`, and `PasswordEntry`. fileciteturn13file0

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

entry = ttk.Entry(app)
entry.pack(padx=20, pady=20)

app.mainloop()
```

---

## Value model

`Entry` works with **raw text**:

- `entry.get()` returns the current string
- `textvariable=` or `textsignal=` keeps the text synchronized with your state

Unlike field controls such as `TextEntry`, `Entry` does not define “text vs committed value” semantics on its own.

---

## Common options

### `bootstyle` / `style`

Use semantic tokens via `bootstyle`, or provide a concrete ttk style via `style=`.

```python
ttk.Entry(app, bootstyle="primary")
ttk.Entry(app, bootstyle="secondary")
```

### `textvariable`

Bind to a Tk variable.

```python
name = ttk.StringVar(value="Ada")
ttk.Entry(app, textvariable=name).pack()
```

### `textsignal`

Bind to a reactive signal (no Tk variable needed).

```python
entry = ttk.Entry(app, textsignal=my_signal)
```

### `show`

Mask input characters (useful for basic password-style entry).

```python
ttk.Entry(app, show="•")
```

!!! note "Password input"
    For a full-featured password field (reveal toggle, validation, messages), prefer **PasswordEntry**.

### Tk validation (`validate` / `validatecommand`)

Use Tk’s validation when you need per-keystroke constraints.

```python
def validate_text(new_value: str) -> bool:
    return new_value.isdigit() or new_value == ""

vcmd = (app.register(validate_text), "%P")

entry = ttk.Entry(app, validate="key", validatecommand=vcmd)
entry.pack(padx=20, pady=20)
```

!!! tip "Prefer field controls for forms"
    For most form UX, prefer **TextEntry** (commit-time parsing + validation messages + consistent events).

---

## Behavior

`Entry` follows standard Tk/ttk behavior:

- keyboard focus and caret navigation
- standard widget states (`normal`, `readonly`, `disabled`)
- standard Tk events like `<KeyRelease>` and `<FocusOut>`

```python
entry.bind("<KeyRelease>", lambda e: print(entry.get()))
```

---

## Events

`Entry` emits standard Tk events, not structured v2 field events.

If you want standardized field events like `on_input` / `on_changed`, use **TextEntry**.

---

## Validation and constraints

Use `Entry` validation when you need low-level, immediate constraints while typing.

If you want user-friendly validation messages and commit-based validation, prefer **TextEntry** (or a specialized `*Entry` control).

---

## When should I use Entry?

Use `Entry` when:

- you need direct, low-level access to `ttk.Entry` options
- you are building your own composite control
- you want Tk’s `validate` / `validatecommand` behavior

Prefer **TextEntry** when:

- you want labels, helper text, and standardized events
- you want commit-based validation with messages
- you are building application forms

---

## Related widgets

- **TextEntry** — form-ready text control with labels, messages, and events
- **PasswordEntry** — specialized masked input control
- **NumericEntry** — numeric input with bounds and stepping
- **DateEntry** / **TimeEntry** — structured date/time inputs
- **Combobox** — selection with optional text entry

---

## Reference

- **API Reference:** `ttkbootstrap.Entry`
- **Related guides:** Design System, Events & Signals → Signals, Internationalization → Localization
