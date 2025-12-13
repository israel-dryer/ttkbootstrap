---
title: Form
icon: fontawesome/solid/list-check
---


# Form

`Form` is a **data-driven layout container** that renders labeled field widgets, groups, tabs, and footer buttons from either a data dictionary or an explicit `FieldItem`/`GroupItem` description. It pairs ttkbootstrap field controls with automatic two-way binding and validation, so you can spin up CRUD panels or dialogs without wiring every individual widget yourself.

---

## Overview

`Form` sits on top of `Frame` and:

- Accepts `data` (a `dict[str, Any]`) whose keys become field names and whose value types infer editors (`TextEntry`, `NumericEntry`, `DateEntry`, `PasswordEntry`, checkbuttons, etc.).
- Or receives an explicit `items` layout consisting of `FieldItem`, `GroupItem`, and `TabsItem` definitions (or plain mappings) to control labels, positioning, editor types, and visibility.
- Supports `col_count`, `min_col_width`, and nested groups/tabs to create responsive grids.
- Offers `buttons` (strings, `DialogButton`, or mapping configs) rendered in a footer row that automatically emit `<<Changed>>` events and populate `form.result`.
- Fires `on_data_changed` with the current data snapshot when any field updates.
- Provides helpers such as `form.data`, `validate()`, `get_field_variable()`, and `get_field_signal()` so you can integrate the form into dialogs or seats of logic.

Use `Form` when you want forms that stay in sync with your data model without manually orchestrating the widgets yourself.

---

## Quick example

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.form import Form

app = ttk.App(title="Form Demo", theme="cosmo")

data = {
    "name": "Alice",
    "email": "alice@example.com",
    "birthdate": "1990-01-15",
    "notifications": True
}

form = Form(
    app,
    data=data,
    col_count=2,
    buttons=[
        {"text": "Save", "role": "primary"},
        "Cancel"
    ],
    on_data_changed=lambda d: print("Form data:", d)
)
form.pack(fill="both", padx=16, pady=16, expand=True)

app.mainloop()
```

---

## Layout, editors, and nesting

- When `items` is omitted, `Form` infers field definitions from the `data` dict via `FieldItem`, choosing editors per dtype (`numericentry`, `dateentry`, `passwordentry`, etc.).
- Override editors or layouts by passing explicit `items`. Each `FieldItem` lets you set `editor`, `editor_options`, `column`, `row`, `visible`, `readonly`, and spans—perfect for custom grids.
- Use `GroupItem` to wrap fields in a labeled `LabelFrame` (with padding, width, height). Nest groups inside each other for complex layouts.
- Attach tabs via `TabsItem` + `TabItem` so you can split forms across tab panels while still exposing the same data binding.
- `Form` also accepts `scrollable=True` when you need the body to scroll independently.

---

## Buttons, data binding & helpers

- Footer `buttons` can be strings, `DialogButton` instances, or dictionaries. They are built with semantic bootstyles (primary/secondary/danger) and call the provided handler before storing `form.result`.
- Call `form.data` to get the current snapshot. Assign to `form.data = {...}` to push values into the widgets programmatically.
- `get_field_variable(key)` / `get_field_signal(key)` / `get_field_textsignal(key)` let you tap into the underlying Tk variables or signals for custom bindings.
- When `on_data_changed` is provided, it receives a fresh dict every time a field commit occurs, letting you validate, sync, or enable other UI.

---

## Validation & interaction

- `Form.validate()` loops through every field, runs validation rules on widgets that support `ValidationMixin`, and focuses the first invalid control. It returns `True` only when all widgets pass.
- Every field still emits standard `<</>>` events (e.g., `<<Changed>>`, `<<Input>>`, `<<Valid>>`, `<<Invalid>>`), so you can listen directly on individual widgets if needed.
- `FieldItem.editor_options` can include validation helpers like `required`, `validator`, or `show_message` so the control surfaces inline feedback.

---

## When to use Form

Use `Form` when you need a data-driven layout—like dialog forms, admin panels, or settings pages—without manually wiring every field. If you only need a single control, keep using `TextEntry`, `NumericEntry`, or `DateEntry` directly; `Form` shines when you want many fields rendered consistently and synced with your model.

For guided dialogs, pair `Form` with `DialogButton` definitions or wrap it inside `FormDialog`.

---

## Related widgets

- `FormDialog` (forms inside a dialog shell)
- `TextEntry` / `NumericEntry` / `DateEntry` (field builders used by `Form`)
- `Button` (footer actions rendered by the form)
