---
title: SelectBox
icon: fontawesome/solid/list
---


# SelectBox

`SelectBox` is a **Field-powered dropdown control** that shows a popup `Treeview` of items and keeps the usual label/message/validation tooling from `Field`.

It works either as a readonly picker or an editable, searchable control that lets users type to filter options or insert arbitrary text when `allow_custom_values=True`.

---

## Overview

Key behaviors:

- Renders an entry plus an addon dropdown button (chevron icon by default) that opens a compact popup list.
- Uses a `Treeview` under the hood so items are easy to style and scroll.
- `allow_custom_values` lets the entry accept text that isn’t part of the list.
- `search_enabled` filters list options as you type and can optionally auto-select the first match.
- Event generation (`<<Changed>>`, `<<Input>>`, `<<Valid>>`, `<<Invalid>>`) mirrors other Field widgets.

Use it for selection lists, tag inputs, or any place where keyboard-friendly filtering and optional freeform text are desirable.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(title="SelectBox Demo", theme="cosmo")

topics = ttk.SelectBox(
    app,
    label="Topic",
    items=[
        "Budget",
        "Roadmap",
        "Release Notes",
        "Customer Success",
        "Support"
    ],
    message="Click the chevron or start typing to filter",
    search_enabled=True
)
topics.pack(fill="x", padx=16, pady=8)

custom = ttk.SelectBox(
    app,
    label="Tag",
    items=["frontend", "backend", "design"],
    allow_custom_values=True,
    message="Type or choose an existing tag"
)
custom.pack(fill="x", padx=16, pady=8)

app.mainloop()
```

---

## Modes, searching, and customization

- `allow_custom_values=True` keeps the entry editable even when a dropdown button is present.
- When `search_enabled=True`, the entry filters popup items on every keystroke and can auto-select the first filtered result when the popup closes.
- Omit `show_dropdown_button` (default `True`) to hide the icon when you just want inline filtering.
- `dropdown_button_icon` controls the glyph shown on the button (e.g., `caret-down`), and you can style it via bootstyles the same way you would any addon.
- The `items` list is dynamic; calling `configure(items=[...])` replaces the popup contents instantly.

Readonly mode (`allow_custom_values=False`, `search_enabled=False`) uses a readonly entry state and binds opening the popup to the entry click, mimicking a native dropdown but with consistent theming.

---

## Events & signals

`SelectBox` relies on `Field` events:

- `<<Changed>>`: fires when the selection changes either from the popup or programmatically.
- `<<Input>>`: works while typing/searching (especially useful when `allow_custom_values=True`).
- `<<Valid>>` / `<<Invalid>>`: emitted when validation rules pass or fail.

You can add `add_validation_rule`, set `required=True`, or connect a `textsignal`/`textvariable` to react to dynamic data.

---

## When to use SelectBox

Choose `SelectBox` when you need a dropdown backed by ttkbootstrap theming but with the flexibility of freeform typing or inline filtering. It is a solid choice for tag selectors, picker dialogs, and other compact option lists.

For plain dropdowns without custom input, consider `OptionMenu` or `MenuButton`; for rated numeric choices, `SpinnerEntry` may be more appropriate.

---

## Related widgets

- `OptionMenu`
- `SpinnerEntry`
- `TextEntry`
- `Field`

