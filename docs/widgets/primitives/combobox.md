---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: Combobox
---

# Combobox

`Combobox` is a **primitive selection widget** that wraps `ttk.Combobox` with ttkbootstrap styling and reactive text support.

It provides a familiar dropdown list with optional typing. Use `Combobox` when you want low-level ttk behavior with improved
visuals. Use **SelectBox** when you want a form-ready selection field with labels, messages, validation, and standardized events. fileciteturn15file0

---

## Overview

A Combobox is a hybrid control:

- **dropdown list** of values (`values=...`)

- optional **typing** (editable mode)

- selection is represented as **text** (string)

It is best for compact, low-complexity pickers.

---

## Basic usage

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

## Variants

### Readonly (pick only)

Users must pick from the list.

```python
ttk.Combobox(app, values=["One", "Two", "Three"], state="readonly")
```

### Editable (type + suggestions)

Users can type any text, or pick from the list.

```python
ttk.Combobox(app, values=["Apple", "Banana", "Cherry"], state="normal")
```

---

## How the value works

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

- `state="readonly"` → text should always be one of `values`

- `state="normal"` → text may be arbitrary

---

## Binding to signals or variables

### Tk variables

```python
choice = ttk.StringVar(value="Medium")

combo = ttk.Combobox(app, textvariable=choice, values=["Low", "Medium", "High"], state="readonly")
```

### Reactive signals

```python
combo = ttk.Combobox(app, textsignal=my_signal, values=["Low", "Medium", "High"], state="readonly")
```

---

## Common options

### `values`

Defines the list shown in the dropdown.

```python
combo.configure(values=["One", "Two", "Three"])
```

### `state`

- `"readonly"` for strict selection

- `"normal"` for editable mode

- `"disabled"` to disable interaction

```python
combo.configure(state="readonly")
```

### `bootstyle`

Applies ttkbootstrap theme styling.

```python
ttk.Combobox(app, values=["A", "B"], bootstyle="primary")
ttk.Combobox(app, values=["A", "B"], bootstyle="secondary")
```

---

## Behavior

- Clicking the arrow opens the dropdown list.

- In readonly mode, selection is made from the list only.

- In editable mode, typing changes the text immediately.

---

## Events

Combobox emits standard ttk events (no field-style `on_changed` helpers).

Most commonly used:

- `<<ComboboxSelected>>` — when the user selects an item from the dropdown

```python
combo.bind("<<ComboboxSelected>>", lambda e: print(combo.get()))
```

If you need to react to typing, bind key events:

```python
combo.bind("<KeyRelease>", lambda e: print(combo.get()))
```

---

## Validation and constraints

Combobox is a primitive widget and does not provide built-in validation semantics.

Use `state="readonly"` to constrain values to the list, or apply your own validation rules externally.

If you want validation messages, required behavior, and commit semantics, prefer **SelectBox**.

---

## Colors and styling

Use `bootstyle` tokens to match the active theme. The entry field and the dropdown list are styled consistently and respond
to theme changes. fileciteturn15file0

---

## Localization

Combobox does not automatically localize `values`. If you supply localized strings, they will be displayed as-is.

If you need localization-aware field labels and messaging, prefer **SelectBox**.

---

## When should I use Combobox?

Use `Combobox` when:

- you want a lightweight dropdown with optional typing

- the list of values is relatively small

- you want low-level ttk control over options and events

Prefer **SelectBox** when:

- you want a form-ready field (label/message/validation)

- you need standardized events (`on_input` / `on_changed`)

- options are long and filtering/search is useful

Prefer **OptionMenu** when:

- you want the simplest menu-style single selection picker

---

## Related widgets

- **SelectBox** — form-ready selection control with validation and optional search

- **OptionMenu** — simple menu-based picker

- **DropdownButton** — action menu (not value selection)

---

## Reference

- **API Reference:** `ttkbootstrap.Combobox`

- **Related guides:** Events & Signals → Signals

---

## Additional resources

### Related widgets

- [Canvas](canvas.md)

- [Entry](entry.md)

- [Spinbox](spinbox.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Combobox`](../../reference/widgets/Combobox.md)
