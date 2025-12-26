---
title: Entry
---

# Entry

`Entry` is the low-level, single-line text input primitive in ttkbootstrap.

It wraps `ttk.Entry` and integrates ttkbootstrap styling plus reactive text support. `Entry` is also the building block
used by higher-level controls like `TextEntry`, `NumericEntry`, `DateEntry`, and `PasswordEntry`.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

entry = ttk.Entry(app)
entry.pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `Entry` when:

- you need direct, low-level access to `ttk.Entry` options

- you are building your own composite control

- you want Tk's `validate` / `validatecommand` behavior

### Consider a different control when...

- **you want labels, helper text, and standardized events** - prefer [TextEntry](/widgets/inputs/textentry.md)

- **you want commit-based validation with messages** - prefer [TextEntry](/widgets/inputs/textentry.md)

- **you are building application forms** - prefer [TextEntry](/widgets/inputs/textentry.md) or specialized input controls

---

## Appearance

### `bootstyle` / `style`

Use semantic tokens via `bootstyle`, or provide a concrete ttk style via `style=`.

```python
ttk.Entry(app, bootstyle="primary")
ttk.Entry(app, bootstyle="secondary")
```

!!! link "Design System"
    See the [Design System](../../design-system/index.md) for available bootstyle tokens.

---

## Examples and patterns

### Value model

`Entry` works with **raw text**:

- `entry.get()` returns the current string

- `textvariable=` or `textsignal=` keeps the text synchronized with your state

Unlike field controls such as `TextEntry`, `Entry` does not define "text vs committed value" semantics on its own.

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
ttk.Entry(app, show="*")
```

!!! note "Password input"
    For a full-featured password field (reveal toggle, validation, messages), prefer [PasswordEntry](/widgets/inputs/passwordentry.md).

### Tk validation (`validate` / `validatecommand`)

Use Tk's validation when you need per-keystroke constraints.

```python
def validate_text(new_value: str) -> bool:
    return new_value.isdigit() or new_value == ""

vcmd = (app.register(validate_text), "%P")

entry = ttk.Entry(app, validate="key", validatecommand=vcmd)
entry.pack(padx=20, pady=20)
```

!!! tip "Prefer field controls for forms"
    For most form UX, prefer [TextEntry](/widgets/inputs/textentry.md) (commit-time parsing + validation messages + consistent events).

---

## Behavior

`Entry` follows standard Tk/ttk behavior:

- keyboard focus and caret navigation

- standard widget states (`normal`, `readonly`, `disabled`)

- standard Tk events like `<KeyRelease>` and `<FocusOut>`

```python
entry.bind("<KeyRelease>", lambda e: print(entry.get()))
```

### Events

`Entry` emits standard Tk events, not structured v2 field events.

If you want standardized field events like `on_input` / `on_changed`, use [TextEntry](/widgets/inputs/textentry.md).

### Validation and constraints

Use `Entry` validation when you need low-level, immediate constraints while typing.

If you want user-friendly validation messages and commit-based validation, prefer [TextEntry](/widgets/inputs/textentry.md) (or a specialized `*Entry` control).

---

## Additional resources

### Related widgets

- [TextEntry](/widgets/inputs/textentry.md) - form-ready text control with labels, messages, and events

- [PasswordEntry](/widgets/inputs/passwordentry.md) - specialized masked input control

- [NumericEntry](/widgets/inputs/numericentry.md) - numeric input with bounds and stepping

- [DateEntry](/widgets/inputs/dateentry.md) / [TimeEntry](/widgets/inputs/timeentry.md) - structured date/time inputs

- [Combobox](/widgets/primitives/combobox.md) - selection with optional text entry

### Framework concepts

- [Design System](../../design-system/index.md)

- [Events and Signals](../../capabilities/signals/signals.md)

- [Localization](../../capabilities/localization.md)

### API reference

- [`ttkbootstrap.Entry`](../../reference/widgets/Entry.md)