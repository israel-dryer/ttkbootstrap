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

title: SelectBox
---

# SelectBox

`SelectBox` is a **selection control** that lets users pick **one value from a list** using a field-like dropdown.
It can optionally support **search filtering** and **custom (user-typed) values**.

Use `SelectBox` when you want a modern “select” experience (popup list + optional search) while keeping consistent
field patterns like labels, messages, and validation.

> _Image placeholder:_  
> `![SelectBox overview](../_img/widgets/selectbox/overview.png)`  
> Suggested shot: closed state + open popup list.

---

## Overview

`SelectBox` is best for choosing a single value from a known set of options:

- **single selection** (one committed value)

- **list-backed** choices (items)

- optional **search** to filter long lists

- optional **custom values** when list membership is not strict

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

sb = ttk.SelectBox(
    app,
    label="Status",
    items=["New", "In Progress", "Blocked", "Done"],
    value="New",
)
sb.pack(fill="x", padx=20, pady=20)

app.mainloop()
```

---

## Variants

`SelectBox` is primarily a single pattern (field + popup list). The most meaningful “variant” is whether it behaves as:

- a **strict picker** (choose from items)

- an **editable picker** (allow custom values)

See **Allowing custom values** below.

---

## How the value works

- `items` defines the available choices shown in the popup

- `value` is the committed selection (typically a string)

When the user selects from the popup, `SelectBox` updates `value` and emits `<<Changed>>`.

```python
print("Current:", sb.value)
sb.value = "In Progress"
```

---

## Binding to signals or variables

Use two-way binding for app state.

!!! tip "Two-way binding"
    If you want two-way binding with your own state, set `textvariable=...`
    via the underlying field options.

---

## Common options

### `items`

```python
sb.configure(items=["Low", "Medium", "High"])
```

### `value`

```python
sb.value = "Medium"
```

### `search_enabled`

Enable typing to filter the popup list.

```python
sb = ttk.SelectBox(
    app,
    label="Assignee",
    items=["Alice", "Bob", "Charlie", "Diana"],
    search_enabled=True,
)
```

### `allow_custom_values`

Allow values not present in `items`.

```python
sb = ttk.SelectBox(
    app,
    label="Tag",
    items=["Bug", "Feature", "Docs"],
    allow_custom_values=True,
)
```

### Dropdown button options

```python
sb = ttk.SelectBox(
    app,
    label="Priority",
    items=["Low", "Medium", "High"],
    show_dropdown_button=True,
    dropdown_button_icon="chevron-down",
)
```

!!! note "Using custom values"
    `show_dropdown_button` is ignored when `allow_custom_values=True` (the button is always present).
    The default icon is `"chevron-down"`.

---

## Behavior

### Opening the popup

The popup opens when:

- the dropdown button is clicked

- the field is readonly and the user clicks the entry area
  (default when search and custom values are off)

### Search and filtering

When `search_enabled=True`:

- typing filters the popup list

- the first matching item is automatically highlighted

- if `allow_custom_values=False`, closing the popup without explicit selection commits the first match

> _Image placeholder:_  
> `![SelectBox filtering](../_img/widgets/selectbox/filtering.png)`  
> Suggested shot: typing “di” filters list to “Diana”.

### Allowing custom values

When `allow_custom_values=True`:

- the entry becomes editable

- the dropdown button is always shown

- typed text can be kept even if it doesn’t match an item

### Keyboard and closing behavior

- **Escape** closes the popup

- In search mode (and when `allow_custom_values=False`), **Tab** or **Enter** selects the highlighted item

- Clicking outside the popup closes it

---

## Events

```python
def on_changed(e):
    print("Changed:", sb.value)

sb.on_changed(on_changed)
```

Most commonly used:

- `<<Changed>>` — fired when the committed value changes

---

## Validation and constraints

When `allow_custom_values=False`, values are constrained to `items`, so validation is usually minimal.

Validation is most useful when:

- the list of valid items changes dynamically

- the field is conditionally required

- the selected value must satisfy cross-field rules

---

## Colors and styling

`SelectBox` typically follows field styling (surface, border, focus), plus a suffix button.

Apply `bootstyle` at the field level as needed:

```python
ttk.SelectBox(app, label="Status", items=["New", "Done"], bootstyle="secondary")
```

---

## Localization

If the field label participates in localization, it follows your global field/widget localization rules.

---

## When should I use SelectBox?

Use `SelectBox` when:

- users should pick one value from a known list

- search or filtering improves usability

- you want a field-like dropdown with consistent form patterns

Prefer **OptionMenu** when:

- you want a simpler, menu-based selector

Prefer **Combobox** when:

- you need classic ttk combobox behavior

---

## Related widgets

- **OptionMenu** — simple menu-based selection control

- **Combobox** — classic ttk dropdown + optional typing

- **RadioGroup** — single selection among visible options

- **CheckButton** — independent multi-selection

- **Form** — generate selection fields declaratively

---

## Reference

- **API Reference:** `ttkbootstrap.SelectBox`

---

## Additional resources

### Related widgets

- [Calendar](calendar.md)

- [CheckButton](checkbutton.md)

- [CheckToggle](checktoggle.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.SelectBox`](../../reference/widgets/SelectBox.md)
