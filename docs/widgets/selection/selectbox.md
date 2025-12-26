---
title: SelectBox
---

# SelectBox

`SelectBox` is a **selection control** that lets users pick **one value from a list** using a field-like dropdown.
It can optionally support **search filtering** and **custom (user-typed) values**.

Use `SelectBox` when you want a modern "select" experience (popup list + optional search) while keeping consistent
field patterns like labels, messages, and validation.

> _Image placeholder:_
> `![SelectBox overview](../_img/widgets/selectbox/overview.png)`
> Suggested shot: closed state + open popup list.

---

## Quick start

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

## When to use

Use `SelectBox` when:

- users should pick one value from a known list

- search or filtering improves usability

- you want a field-like dropdown with consistent form patterns

### Consider a different control when...

- You want a simpler, menu-based selector — use [OptionMenu](optionmenu.md)

- You need single selection among visible options — use [RadioGroup](radiogroup.md)

- You need direct access to `ttk.Combobox` API — use [Combobox](../primitives/combobox.md)

---

## Appearance

### Variants

`SelectBox` is primarily a single pattern (field + popup list). The most meaningful "variant" is whether it behaves as:

- a **strict picker** (choose from items)

- an **editable picker** (allow custom values)

See **Allowing custom values** in the Behavior section below.

### Colors and styling

`SelectBox` typically follows field styling (surface, border, focus), plus a suffix button.

Apply `bootstyle` at the field level as needed:

```python
ttk.SelectBox(app, label="Status", items=["New", "Done"], bootstyle="secondary")
```

!!! link "Design System"
    For theming details, color tokens, and styling guidelines, see the [Design System](../../design-system/index.md) documentation.

---

## Examples and patterns

### How the value works

- `items` defines the available choices shown in the popup

- `value` is the committed selection (typically a string)

When the user selects from the popup, `SelectBox` updates `value` and emits `<<Changed>>`.

```python
print("Current:", sb.value)
sb.value = "In Progress"
```

### Common options

#### `items`

```python
sb.configure(items=["Low", "Medium", "High"])
```

#### `value`

```python
sb.value = "Medium"
```

#### `selected_index`

Get or set selection by index.

```python
sb.selected_index = 2       # select third item
print(sb.selected_index)    # returns -1 if value not in items
```

#### `search_enabled`

Enable typing to filter the popup list.

```python
sb = ttk.SelectBox(
    app,
    label="Assignee",
    items=["Alice", "Bob", "Charlie", "Diana"],
    search_enabled=True,
)
```

#### `allow_custom_values`

Allow values not present in `items`.

```python
sb = ttk.SelectBox(
    app,
    label="Tag",
    items=["Bug", "Feature", "Docs"],
    allow_custom_values=True,
)
```

#### Dropdown button options

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

### Events

```python
def on_changed(e):
    print("Changed:", sb.value)

sb.on_changed(on_changed)
```

Most commonly used:

- `<<Changed>>` — fired when the committed value changes

### Binding to signals or variables

Use two-way binding for app state.

!!! tip "Two-way binding"
    If you want two-way binding with your own state, set `textvariable=...`
    via the underlying field options.

### Validation and constraints

When `allow_custom_values=False`, values are constrained to `items`, so validation is usually minimal.

Validation is most useful when:

- the list of valid items changes dynamically

- the field is conditionally required

- the selected value must satisfy cross-field rules

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
> Suggested shot: typing "di" filters list to "Diana".

### Allowing custom values

When `allow_custom_values=True`:

- the entry becomes editable

- the dropdown button is always shown

- typed text can be kept even if it doesn't match an item

### Keyboard navigation

When the popup is open:

- **Arrow Up/Down** navigates through items (highlighted item scrolls into view)

- **Enter** selects the highlighted item

- **Tab** selects the highlighted item (search mode)

- **Escape** closes the popup without selecting

- Clicking outside the popup closes it

### Hover states

Items in the popup display hover states for visual feedback as the user moves the mouse or navigates with arrow keys.

---

## Localization

If the field label participates in localization, it follows your global field/widget localization rules.

!!! link "Localization"
    For details on internationalizing your application, see the [Localization](../../capabilities/localization.md) documentation.

---

## Additional resources

### Related widgets

- [OptionMenu](optionmenu.md) — simple menu-based selection control

- [Combobox](../primitives/combobox.md) — classic ttk dropdown + optional typing

- [RadioGroup](radiogroup.md) — single selection among visible options

- [CheckButton](checkbutton.md) — independent multi-selection

- [Form](../forms/form.md) — generate selection fields declaratively

### Framework concepts

- [Validation](../../capabilities/validation.md) — form and field validation patterns

- [Events and callbacks](../../capabilities/events.md) — handling widget events

### API reference

- [`ttkbootstrap.SelectBox`](../../reference/widgets/SelectBox.md)