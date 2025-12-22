---
title: Form
---

# Form

`Form` is a **spec-driven form builder**.

It makes it easy to build consistent data-entry UIs by composing the standard v2 input widgets (TextEntry, NumericEntry, SelectBox, DateEntry, etc.) from a single definition.

Use `Form` when you want:

- a form layout generated from a spec (instead of manually wiring every widget)
- consistent label/message/validation behavior across fields
- a single place to read/write form data and run validation

---

## Overview

A `Form` takes a list of field definitions (and optional layout/grouping instructions) and produces:

- labeled field widgets (using your v2 field controls)
- an internal data model (readable as a dict)
- validation helpers and a consistent “submit” flow
- optional grouping and tabs for larger forms

This is a **builder/composite**: it does not replace your input widgets—it standardizes how they’re assembled and managed.

---

## Basic usage

Define fields and read the committed data:

```python
import ttkbootstrap as ttk

app = ttk.App()

form = ttk.Form(
    app,
    items=[
        {"key": "name", "label": "Name", "editor": "text"},
        {"key": "age", "label": "Age", "editor": "int"},
        {"key": "status", "label": "Status", "editor": "select", "items": ["New", "In Progress", "Done"]},
    ],
)
form.pack(fill="both", expand=True, padx=20, pady=20)

def submit():
    if form.validate():
        print(form.data)   # dict-like
    else:
        print("invalid")

ttk.Button(app, text="Submit", command=submit).pack(pady=(0, 20))

app.mainloop()
```

---

## Form spec

`Form` is configured with a list of item definitions.

### Field items

A field item describes one value:

- `key` — unique field key (used in `form.data`)
- `label` — label text for the field
- `editor` — what widget/editor to use
- `value` — optional initial value
- `required` / `validate` — validation options
- `help` / `message` — optional helper text

Example:

```python
{"key": "email", "label": "Email", "editor": "text", "required": True}
```

### Editor-specific options

Some editors accept additional options:

- select-like editors: `items=[...]`
- numeric editors: `min`, `max`, `step`, formatting options
- date editors: `min_date`, `max_date`, formatting options

---

## Layout

### Columns

For wide forms, you can specify a column count:

```python
form = ttk.Form(app, columns=2, items=[...])
```

### Explicit placement (advanced)

If your implementation supports explicit row/column placement, use it for custom layouts:

```python
{"key": "first", "label": "First name", "editor": "text", "row": 0, "column": 0}
{"key": "last", "label": "Last name", "editor": "text", "row": 0, "column": 1}
```

---

## Grouping and tabs

For larger forms, organize fields into groups and tabs.

### Groups

Groups visually separate related fields (like a section):

```python
{
  "type": "group",
  "label": "Account",
  "items": [
    {"key": "user", "label": "User", "editor": "text"},
    {"key": "role", "label": "Role", "editor": "select", "items": ["Admin", "User"]},
  ]
}
```

### Tabs

Tabs separate major sections (profile/settings/permissions):

```python
{
  "type": "tabs",
  "tabs": [
    {"label": "General", "items": [...]},
    {"label": "Advanced", "items": [...]},
  ]
}
```

---

## Data model

### Reading data

`form.data` (or an equivalent accessor) returns a dict-like mapping:

```python
data = form.data
print(data["name"])
```

### Setting data

Set values in bulk (if supported):

```python
form.set_data({"name": "Alice", "age": 34})
```

Or per field:

```python
form.set_value("status", "Done")
```

---

## Validation

### Validate the full form

```python
ok = form.validate()
```

### Required fields

```python
{"key": "name", "label": "Name", "editor": "text", "required": True}
```

### Custom validation (if supported)

If your spec supports validators:

```python
{"key": "email", "label": "Email", "editor": "text", "validate": "email"}
```

Or a callable:

```python
{"key": "port", "label": "Port", "editor": "int", "validate": lambda v: 0 <= v <= 65535}
```

!!! tip "Validation UX"
    Prefer showing validation messages inline at the field level, and only use modal dialogs for form-level failures.

---

## Accessing fields and widgets

Most form builders provide a way to access the generated field widgets:

```python
field = form.field("email")
field.focus()
```

Or the underlying editor:

```python
editor = form.editor("email")
```

Use this to:

- focus the first invalid field
- dynamically enable/disable fields
- update items for select fields

---

## Footer actions and “submit” flows

A common pattern is to:

1. validate the form
2. read `form.data`
3. commit changes / close dialog / navigate

If your `Form` supports built-in footer buttons, use them for consistent layouts. Otherwise, pair with `ButtonGroup` or a simple button row.

---

## When should I use Form?

Use `Form` when:

- you want to build forms from a spec
- you need consistent layout + validation across many fields
- the form structure changes dynamically (feature flags, permissions, metadata-driven UI)

Prefer hand-built layouts when:

- the form is small (1–3 fields)
- the layout is highly custom or artistic
- you need extremely bespoke widget composition per row

Prefer `FormDialog` when:

- the entire task is “fill this form and confirm/cancel” in a modal flow

---

## Related widgets

- **TextEntry / NumericEntry / DateEntry / SelectBox** — the underlying field widgets
- **FormDialog** — modal form flow
- **PageStack** — multi-step (wizard) forms
- **FilterDialog** — specialized form for filters

---

## Reference

- **API Reference:** `ttkbootstrap.Form`
