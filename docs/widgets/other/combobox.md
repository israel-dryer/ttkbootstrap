---
title: Combobox
icon: fontawesome/solid/caret-down
---

# Combobox

`Combobox` is a themed wrapper around `ttk.Combobox` that integrates ttkbootstrap’s styling system and reactive text support. It provides a familiar dropdown-selection control with consistent theming for both the entry field and the popdown list.

<!--
IMAGE: Combobox closed and open
Suggested: Combobox showing selected value, with dropdown list open below
Theme variants: light / dark
-->

---

## Basic usage

Use `Combobox` when you want to present a list of predefined values that the user can select from.

```python
import ttkbootstrap as ttk

app = ttk.App()

combo = ttk.Combobox(
    app,
    values=["Low", "Medium", "High"],
    state="readonly",
)
combo.pack(padx=20, pady=20)

app.mainloop()
```

<!--
IMAGE: Basic Combobox example
Suggested: Readonly combobox with simple text values
-->

---

## What problem it solves

The native `ttk.Combobox` popdown is styled separately from the main widget and often does not match the active theme. ttkbootstrap’s `Combobox` ensures:

- Consistent theming between the entry field and dropdown list
- Automatic restyling when the application theme changes
- A modern look that matches other ttkbootstrap controls

---

## Core concepts

### Editable vs readonly modes

`Combobox` supports two primary interaction modes:

- **Editable (`state="normal"`)**
  Users may type arbitrary text or select from the list.

- **Readonly (`state="readonly"`)**
  Users must select from the provided values.

```python
ttk.Combobox(app, values=items, state="normal")
ttk.Combobox(app, values=items, state="readonly")
```

Readonly mode is recommended for most selection-driven UI.

---

### Values and selection

The `values` option defines the list shown in the dropdown:

```python
combo.configure(values=["One", "Two", "Three"])
```

The currently selected value can be accessed or controlled via:

- `get()` / `set()`
- `textvariable`
- `textsignal`

---

### Reactive text with `textsignal`

`Combobox` supports `textsignal`, allowing the selected value to reactively synchronize with application state:

```python
combo = ttk.Combobox(app, textsignal=my_signal)
```

This is useful in signal-driven or declarative-style UIs.

---

## Common options & patterns

### Styling with bootstyle

```python
ttk.Combobox(app, values=items, bootstyle="primary")
ttk.Combobox(app, values=items, bootstyle="secondary")
```

The `bootstyle` affects both the entry field and the dropdown list.

---

### Customizing dropdown height

Control how many rows appear in the dropdown:

```python
ttk.Combobox(app, values=items, height=8)
```

---

### Using postcommand

A `postcommand` runs just before the dropdown opens. ttkbootstrap wraps this internally to ensure the popdown is styled before first use.

```python
def before_open():
    print("Opening dropdown")

ttk.Combobox(app, values=items, postcommand=before_open)
```

---

## Events

`Combobox` emits standard ttk events:

- `<<ComboboxSelected>>` when the selection changes

You can bind directly:

```python
combo.bind("<<ComboboxSelected>>", lambda e: print(combo.get()))
```

!!! tip "Higher-level controls"
    For forms and validated input, consider using `SelectBox`, which builds on Combobox-like behavior with labels, messages, and validation.

---

## UX guidance

- Use readonly mode whenever free-form input is not desired
- Keep option lists short and scannable
- For large or searchable lists, prefer `SelectBox`

---

## When to use / when not to

**Use Combobox when:**

- You need a lightweight, native-feeling dropdown
- Values are known and relatively small
- You want editable or readonly selection behavior

**Avoid Combobox when:**

- You need validation, labels, or helper text (use `SelectBox`)
- You need search/filter or complex item rendering
- You want a unified form-level API

---

## Related widgets

- **SelectBox** — higher-level, form-ready selection control
- **OptionMenu** — simpler selection dropdown
- **DropdownButton** — action-based menus
