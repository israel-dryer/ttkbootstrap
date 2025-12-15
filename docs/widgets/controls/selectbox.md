---
title: SelectBox
icon: fontawesome/solid/square-check
---

# SelectBox

`SelectBox` is a **dropdown-style field control** built on top of `Field`.

It looks like a regular input field, but includes a suffix button that opens a lightweight popup with a list of options.
When the user selects an item, the field updates its value and emits `<<Changed>>`.

Use `SelectBox` when you want the feel of a modern “select” control (popup list + optional search) while keeping the
same **label / message / validation** patterns used by other v2 field widgets.

> _Image placeholder:_  
> `![SelectBox overview](../_img/widgets/selectbox/overview.png)`  
> (Show closed state + open popup list.)

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

## Common options

### `items`

`items` is the list of strings shown in the popup.

```python
sb.configure(items=["Low", "Medium", "High"])
```

### `value`

The current selected value (a string). When the user selects from the popup, `SelectBox` updates `value`
and emits `<<Changed>>`.

```python
print("Current:", sb.value)
sb.value = "Medium"
```

!!! tip "Two-way binding"
    If you want two-way binding with your own state, set `textvariable=...` via the underlying `FieldOptions`.

---

## Opening the popup

`SelectBox` opens the popup when:

- the dropdown button is clicked
- the field is **readonly** and the user clicks the entry area (default behavior when search/custom values are off)

The popup is implemented as a small `Toplevel` with a `TreeView` inside it.

---

## Search / filtering

Enable search to allow typing in the field to filter the popup list.

```python
sb = ttk.SelectBox(
    app,
    label="Assignee",
    items=["Alice", "Bob", "Charlie", "Diana"],
    search_enabled=True,
)
sb.pack(fill="x", padx=20, pady=20)
```

How filtering works:

- As you type, the popup list is rebuilt to show matching items.
- The **first matching item** is automatically selected in the popup.
- If `allow_custom_values=False`, closing the popup without an explicit selection will commit the **first match**.

> _Image placeholder:_  
> `![SelectBox filtering](../_img/widgets/selectbox/filtering.png)`  
> (Show typing “di” filters list to “Diana”.)

---

## Allowing custom values

By default, `SelectBox` behaves like a strict picker: you choose from the list.

If you want users to type values not in the list, enable `allow_custom_values=True`.

```python
sb = ttk.SelectBox(
    app,
    label="Tag",
    items=["Bug", "Feature", "Docs"],
    allow_custom_values=True,
)
sb.pack(fill="x", padx=20, pady=20)
```

Behavior details:

- The entry becomes editable.
- The dropdown button is always shown (even if you disable it via `show_dropdown_button`).
- With `search_enabled=True`, typed values filter the list, but the typed value can be kept.

---

## Dropdown button

You can control the button and icon.

```python
sb = ttk.SelectBox(
    app,
    label="Priority",
    items=["Low", "Medium", "High"],
    show_dropdown_button=True,
    dropdown_button_icon="chevron-down",
)
sb.pack(fill="x", padx=20, pady=20)
```

!!! note "Using custom values"
    `show_dropdown_button` is **ignored** when `allow_custom_values=True` (the button is always present).   
    The default icon is `"chevron-down"`.

---

## Keyboard & closing behavior

- **Escape** closes the popup.
- In search mode (and when `allow_custom_values=False`), **Tab** or **Enter** selects the highlighted item.
- Clicking outside the popup closes it.

---

## Events

`SelectBox` emits the standard field events.

Most commonly you’ll use:

- `<<Changed>>` — fired when the committed value changes (for example, after selecting an item)

Example:

```python
def on_changed(e):
    # Depending on your event system, you may have structured payload.
    print("Changed:", sb.value)

sb.on_changed(on_changed)
```

---

## When should I use SelectBox?

Use `SelectBox` when:

- you want a clean “pick from a list” field with a modern popup
- you want optional search filtering
- you want the consistent v2 field experience (label, message, validation)

Prefer `OptionMenu` when:

- you want a simpler, native menu-based picker with minimal behavior

Prefer `Combobox` when:

- you want the classic ttk combobox widget (including its built-in dropdown behavior)

---

## Related widgets

- **OptionMenu** — simple menu-based selection control
- **Combobox** — classic ttk dropdown + optional typing
- **TextEntry** — free-form text input field control
- **Form** — generate forms using field controls like `SelectBox`
