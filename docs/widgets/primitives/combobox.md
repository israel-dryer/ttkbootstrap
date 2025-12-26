---
title: Combobox
---

# Combobox

!!! tip "Prefer SelectBox"
    [SelectBox](/widgets/selection/selectbox.md) provides all the functionality of Combobox plus additional features:
    keyboard navigation, hover states, search/filtering, form integration (labels, messages, validation), and
    standardized events. Use Combobox only when you need direct access to the underlying `ttk.Combobox` API.

`Combobox` is a **primitive selection widget** that wraps `ttk.Combobox` with ttkbootstrap styling and reactive text support.

It provides a familiar dropdown list with optional typing. Use `Combobox` when you need low-level ttk behavior or direct
access to `ttk.Combobox` methods. Use [SelectBox](/widgets/selection/selectbox.md) for most selection use cases.

---

## Quick start

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

---

## When to use

Use `Combobox` when:

- you need direct access to `ttk.Combobox` methods (e.g., `current()`, `postcommand`)

- you're integrating with existing code that expects a `ttk.Combobox`

### Consider a different control when...

- **for most selection use cases** - prefer [SelectBox](/widgets/selection/selectbox.md), which provides keyboard navigation, hover states, search/filtering, and form integration

- **you want the simplest menu-style single selection picker** - prefer [OptionMenu](/widgets/selection/optionmenu.md)

---

## Appearance

A Combobox is a hybrid control:

- **dropdown list** of values (`values=...`)

- optional **typing** (editable mode)

- selection is represented as **text** (string)

It is best for compact, low-complexity pickers.

### `bootstyle`

Applies ttkbootstrap theme styling.

```python
ttk.Combobox(app, values=["A", "B"], bootstyle="primary")
ttk.Combobox(app, values=["A", "B"], bootstyle="secondary")
```

!!! link "Design System"
    See the [Design System](../../design-system/index.md) for available bootstyle tokens.

### Colors and styling

Use `bootstyle` tokens to match the active theme. The entry field and the dropdown list are styled consistently and respond
to theme changes.

---

## Examples and patterns

### Variants

#### Readonly (pick only)

Users must pick from the list.

```python
ttk.Combobox(app, values=["One", "Two", "Three"], state="readonly")
```

#### Editable (type + suggestions)

Users can type any text, or pick from the list.

```python
ttk.Combobox(app, values=["Apple", "Banana", "Cherry"], state="normal")
```

### How the value works

Combobox stores a **string**:

- `get()` returns the current text

- `set(value)` sets the current text

- `textvariable=` binds to a Tk variable

- `textsignal=` binds to a reactive signal

```python
value = combo.get()
combo.set("Medium")
```

The meaning of the text depends on `state`:

- `state="readonly"` - text should always be one of `values`

- `state="normal"` - text may be arbitrary

### Binding to signals or variables

#### Tk variables

```python
choice = ttk.StringVar(value="Medium")

combo = ttk.Combobox(app, textvariable=choice, values=["Low", "Medium", "High"], state="readonly")
```

#### Reactive signals

```python
combo = ttk.Combobox(app, textsignal=my_signal, values=["Low", "Medium", "High"], state="readonly")
```

### Common options

#### `values`

Defines the list shown in the dropdown.

```python
combo.configure(values=["One", "Two", "Three"])
```

#### `state`

- `"readonly"` for strict selection

- `"normal"` for editable mode

- `"disabled"` to disable interaction

```python
combo.configure(state="readonly")
```

### Events

Combobox emits standard ttk events (no field-style `on_changed` helpers).

Most commonly used:

- `<<ComboboxSelected>>` - when the user selects an item from the dropdown

```python
combo.bind("<<ComboboxSelected>>", lambda e: print(combo.get()))
```

If you need to react to typing, bind key events:

```python
combo.bind("<KeyRelease>", lambda e: print(combo.get()))
```

---

## Behavior

- Clicking the arrow opens the dropdown list.

- In readonly mode, selection is made from the list only.

- In editable mode, typing changes the text immediately.

### Validation and constraints

Combobox is a primitive widget and does not provide built-in validation semantics.

Use `state="readonly"` to constrain values to the list, or apply your own validation rules externally.

If you want validation messages, required behavior, and commit semantics, prefer [SelectBox](/widgets/selection/selectbox.md).

---

## Localization

Combobox does not automatically localize `values`. If you supply localized strings, they will be displayed as-is.

If you need localization-aware field labels and messaging, prefer [SelectBox](/widgets/selection/selectbox.md).

---

## Additional resources

### Related widgets

- [SelectBox](/widgets/selection/selectbox.md) - form-ready selection control with validation and optional search

- [OptionMenu](/widgets/selection/optionmenu.md) - simple menu-based picker

- [DropdownButton](/widgets/actions/dropdownbutton.md) - action menu (not value selection)

### Framework concepts

- [Events and Signals](../../capabilities/signals/signals.md)

### API reference

- [`ttkbootstrap.Combobox`](../../reference/widgets/Combobox.md)