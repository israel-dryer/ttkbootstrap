---
title: OptionMenu
---

# OptionMenu

`OptionMenu` is a **selection control** that lets users pick **one value from a short list** using a
menu-style dropdown.

In ttkbootstrap v2, `OptionMenu` wraps Tkinter's `ttk.Menubutton` and adds theming, icons, signals,
and standardized change events. It is best suited for **compact, known option sets**.

Use `OptionMenu` when the list is small and users already know the available choices.
For longer lists or search/filtering, prefer [SelectBox](selectbox.md).

---

## Overview

`OptionMenu` provides:

- **single selection** (one committed value)

- **menu-based** dropdown behavior

- compact desktop-friendly appearance

- optional **signals** and `<<Changed>>` events

It is intentionally simpler than `SelectBox` and does not support search or custom values.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

menu = ttk.OptionMenu(
    app,
    value="Medium",
    options=["Low", "Medium", "High"],
)
menu.pack(padx=20, pady=20)

app.mainloop()
```

---

## Variants

`OptionMenu` does not have behavioral variants. Its primary variations are visual, controlled by
`bootstyle` (see **Colors and styling**).

---

## How the value works

- `options` defines the list of valid values

- `value` is the currently selected option

When the user selects a menu item, `OptionMenu` updates `value` and emits `<<Changed>>`.

```python
print(menu.value)
menu.value = "High"
```

---

## Binding to signals or variables

You can bind selection state in several ways.

### Using a Tk variable

```python
color = ttk.StringVar(value="Green")

menu = ttk.OptionMenu(
    app,
    textvariable=color,
    options=["Red", "Green", "Blue"],
)
```

### Using a signal

```python
selected = ttk.Signal("Medium")

menu = ttk.OptionMenu(
    app,
    textsignal=selected,
    options=["Low", "Medium", "High"],
)

selected.subscribe(lambda v: print("changed:", v))
```

---

## Common options

### `options`

Defines the available choices.

```python
menu.configure(options=["Apple", "Banana", "Cherry"])
```

### `value`

Set or update the selected value.

```python
menu.configure(value="Banana")
```

### `state`

Disable or enable the menu.

```python
menu.configure(state="disabled")
menu.configure(state="normal")
```

### `width` and `padding`

```python
ttk.OptionMenu(
    app,
    value="A",
    options=["A", "B"],
    width=20,
    padding=(10, 6),
).pack(pady=6)
```

---

## Behavior

- Clicking the button opens a menu of options.

- Selecting an item immediately commits the value.

- The menu closes automatically after selection.

- Keyboard navigation follows standard ttk menubutton behavior.

---

## Events

`OptionMenu` emits a committed change event when selection changes.

```python
def on_changed(event):
    print("Selected:", event.data["value"])

menu.on_changed(on_changed)
```

To unbind:

```python
bind_id = menu.on_changed(on_changed)
menu.off_changed(bind_id)
```

---

## Validation and constraints

Selection is constrained to `options`.

Validation is typically unnecessary, but may be useful when:

- a selection is required before submission

- options are updated dynamically

---

## Colors and styling

`OptionMenu` supports the same `bootstyle` variants as `MenuButton`.

```python
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="primary")
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="primary-outline")
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="primary-ghost")
ttk.OptionMenu(app, value="A", options=["A", "B"], bootstyle="text")
```

---

## Icons

Use `icon=...` to attach a theme-aware icon.

```python
ttk.OptionMenu(
    app,
    value="Dark",
    options=["Light", "Dark", "Auto"],
    icon="palette",
)
```

!!! warning "Using `image=`"
    Passing a Tk `PhotoImage` via `image=` will not automatically recolor on theme changes.

---

## Localization

Text shown by `OptionMenu` participates in localization according to your global widget settings.
When `localize="auto"`, untranslated keys fall back to literal text.

---

## When should I use OptionMenu?

Use `OptionMenu` when:

- the option list is short (3-15 items)

- the control should remain compact

- search or rich presentation is unnecessary

Prefer **SelectBox** when:

- the list is long

- search or filtering is needed

- users may enter custom values

Prefer **RadioButton / RadioGroup** when:

- there are very few options and showing them inline improves clarity

---

## Additional resources

### Related widgets

- [SelectBox](selectbox.md) - dropdown selection with search and filtering
- [RadioButton](radiobutton.md) - inline mutually exclusive options
- [RadioGroup](radiogroup.md) - grouped radio options
- [MenuButton](../actions/menubutton.md) - base widget for menu-triggered buttons

### API reference

- [`ttkbootstrap.OptionMenu`](../../reference/widgets/OptionMenu.md)