---
title: Form
---

# Form

`Form` is a **spec-driven form builder**.

It makes it easy to build consistent data-entry UIs by composing the standard v2 input widgets (TextEntry, NumericEntry, SelectBox, DateEntry, etc.) from a single definition.

---

## Quick start

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

## When to use

Use `Form` when:

- you want to build forms from a spec (instead of manually wiring every widget)

- you need consistent label/message/validation behavior across fields

- you need consistent layout + validation across many fields

- the form structure changes dynamically (feature flags, permissions, metadata-driven UI)

- you want a single place to read/write form data and run validation

### Consider a different control when...

- the form is small (1–3 fields) — hand-built layouts may be simpler

- the layout is highly custom or artistic — manual composition gives more control

- you need extremely bespoke widget composition per row

- the entire task is "fill this form and confirm/cancel" in a modal flow — prefer [FormDialog](../dialogs/formdialog.md)

---

## Appearance

A `Form` takes a list of field definitions (and optional layout/grouping instructions) and produces:

- labeled field widgets (using your v2 field controls)

- an internal data model (readable as a dict)

- validation helpers and a consistent "submit" flow

- optional grouping and tabs for larger forms

This is a **builder/composite**: it does not replace your input widgets—it standardizes how they're assembled and managed.

!!! link "Design System"
    See the [Design System](../../design-system/index.md) for form layout guidelines and spacing recommendations.

---

## Examples and patterns

### Form spec

`Form` is configured with a list of item definitions.

#### Field items

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

#### Editor-specific options

Some editors accept additional options:

- select-like editors: `items=[...]`

- numeric editors: `min`, `max`, `step`, formatting options

- date editors: `min_date`, `max_date`, formatting options

### Layout

#### Columns

For wide forms, you can specify a column count:

```python
form = ttk.Form(app, columns=2, items=[...])
```

#### Explicit placement (advanced)

If your implementation supports explicit row/column placement, use it for custom layouts:

```python
{"key": "first", "label": "First name", "editor": "text", "row": 0, "column": 0}
{"key": "last", "label": "Last name", "editor": "text", "row": 0, "column": 1}
```

### Grouping and tabs

For larger forms, organize fields into groups and tabs.

#### Groups

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

#### Tabs

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

### Data model

#### Reading data

Use `get()`, the `value` property, or the `data` property to get all field values:

```python
# All equivalent
data = form.get()
data = form.value
data = form.data

print(data["name"])
```

Get a single field's value:

```python
email = form.get_field_value("email")
```

#### Setting data

Set all values at once:

```python
form.set({"name": "Alice", "age": 34})
# Or use the property
form.value = {"name": "Alice", "age": 34}
```

Set a single field's value:

```python
form.set_field_value("status", "Done")
```

### Validation

#### Validate the full form

```python
ok = form.validate()
```

#### Required fields

```python
{"key": "name", "label": "Name", "editor": "text", "required": True}
```

#### Custom validation (if supported)

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

### Footer actions and "submit" flows

A common pattern is to:

1. validate the form
2. read `form.data`
3. commit changes / close dialog / navigate

If your `Form` supports built-in footer buttons, use them for consistent layouts. Otherwise, pair with `ButtonGroup` or a simple button row.

---

## Behavior

### Accessing fields and widgets

Access a field widget by key:

```python
email_field = form.field("email")  # Returns the Field widget
email_field.focus_set()
```

Get all field widgets or keys:

```python
for field in form.fields():
    print(field.value)

for key in form.keys():
    print(key, form.get_field_value(key))
```

Use this to:

- focus the first invalid field

- dynamically enable/disable fields

- update items for select fields

### Variable and signal access

Access Tk Variables and Signals for reactive binding:

```python
# Get the Tk Variable for a field
var = form.field_variable("name")
var.trace_add("write", lambda *_: print("name changed"))

# Get the Signal for a field's value
signal = form.field_signal("age")
if signal:
    signal.subscribe(lambda v: print(f"age is now {v}"))

# Get the text Signal for a field
text_signal = form.field_textsignal("email")
```

---

## Localization

Form labels and validation messages should be localized for international users.

!!! link "Localization"
    See the [Localization guide](../../localization/index.md) for details on translating form content.

---

## Reactivity

Form data can be bound to reactive signals for automatic UI updates when values change.

!!! link "Signals"
    See the [Signals documentation](../../signals/index.md) for reactive data binding patterns.

---

## Additional resources

### Related widgets

- [TextEntry](../inputs/textentry.md) / [NumericEntry](../inputs/numericentry.md) / [DateEntry](../inputs/dateentry.md) / [SelectBox](../selection/selectbox.md) — the underlying field widgets

- [FormDialog](../dialogs/formdialog.md) — modal form flow

- [PageStack](../views/pagestack.md) — multi-step (wizard) forms

- [FilterDialog](../dialogs/filterdialog.md) — specialized form for filters

### Framework concepts

- [Design System](../../design-system/index.md) — layout and spacing guidelines

- [Validation](../../validation/index.md) — form validation patterns

- [Localization](../../localization/index.md) — internationalization support

### API reference

- [`ttkbootstrap.Form`](../../reference/widgets/Form.md)