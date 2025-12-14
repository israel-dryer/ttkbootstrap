---
title: Form
icon: fontawesome/solid/rectangle-list
---

# Form

`Form` builds a complete data entry UI from a definition or data dictionary.

In ttkbootstrap v2, `Form` wraps a `Frame` to create structured layouts with:

- **Automatic field generation** from data dictionaries
- **Explicit layout control** with `FieldItem`, `GroupItem`, and `TabsItem`
- **Multiple field types** (textentry, numericentry, dateentry, checkbutton, selectbox, etc.)
- **Built-in validation** with `.validate()` method
- **Data syncing** via `.data` property
- **Footer buttons** with automatic styling
- **Flexible layouts** with multi-column grids, groups, and tabs

Use `Form` when building dialogs, settings panels, or any structured data entry interface.

> _Image placeholder:_
> `![Form example](../_img/widgets/form/overview.png)`
> Suggested shot: multi-field form with labels, validation messages, grouped sections, and footer buttons.

---

## Basic usage

### From data dictionary

The simplest way to use `Form` is to pass a data dictionary. Fields are inferred from the keys and value types.

```python
import ttkbootstrap as ttk

app = ttk.App()

data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "subscribe": True,
}

form = ttk.Form(app, data=data)
form.pack(fill="both", expand=True, padx=20, pady=20)

print(form.data)  # Get current form values

app.mainloop()
```

---

## Explicit field definitions

For more control, use `FieldItem` to define each field explicitly.

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.form import FieldItem

app = ttk.App()

items = [
    FieldItem(key="username", label="Username", editor="textentry"),
    FieldItem(key="password", label="Password", editor="passwordentry"),
    FieldItem(key="remember", label="Remember me", editor="checkbutton"),
]

form = ttk.Form(app, items=items, data={"username": "", "password": "", "remember": False})
form.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
```

---

## Field types

`Form` supports multiple editor types. If not specified, the editor is inferred from `dtype` or the data value.

### Available editors

| Editor | Description | Default for |
|--------|-------------|-------------|
| `textentry` | Text input with validation | `str` values |
| `numericentry` | Numeric input | `int`, `float` values |
| `passwordentry` | Masked password input | `dtype='password'` |
| `dateentry` | Date picker | `date`, `datetime` values |
| `checkbutton` | Checkbox | `bool` values |
| `toggle` | Toggle switch | - |
| `selectbox` | Dropdown selection | - |
| `spinbox` | Numeric spinner | - |
| `scale` | Slider control | - |
| `text` | Multi-line text area | - |

### Specifying editors

```python
items = [
    FieldItem(key="priority", label="Priority", editor="selectbox",
              editor_options={"items": ["Low", "Medium", "High"]}),
    FieldItem(key="volume", label="Volume", editor="scale",
              editor_options={"from_": 0, "to": 100}),
    FieldItem(key="notes", label="Notes", editor="text",
              editor_options={"height": 5}),
]
```

---

## Layout options

### Multi-column layout

Use `col_count` to arrange fields in columns.

```python
form = ttk.Form(
    app,
    data={"first_name": "", "last_name": "", "email": "", "phone": ""},
    col_count=2,  # Two columns
)
```

### Explicit positioning

Control the exact grid position of fields.

```python
items = [
    FieldItem(key="title", label="Title", row=0, column=0, columnspan=2),
    FieldItem(key="first_name", label="First Name", row=1, column=0),
    FieldItem(key="last_name", label="Last Name", row=1, column=1),
]
```

---

## Groups

Use `GroupItem` to organize fields into labeled sections.

```python
from ttkbootstrap.widgets.composites.form import FieldItem, GroupItem

items = [
    GroupItem(
        label="Personal Information",
        items=[
            FieldItem(key="name", label="Name"),
            FieldItem(key="email", label="Email"),
        ],
    ),
    GroupItem(
        label="Account Settings",
        items=[
            FieldItem(key="username", label="Username"),
            FieldItem(key="password", label="Password", editor="passwordentry"),
        ],
    ),
]

form = ttk.Form(app, items=items, data={})
```

### Multi-column groups

Groups can have their own column layout.

```python
GroupItem(
    label="Address",
    col_count=2,  # Two columns within this group
    items=[
        FieldItem(key="street", label="Street", columnspan=2),
        FieldItem(key="city", label="City"),
        FieldItem(key="state", label="State"),
    ],
)
```

---

## Tabs

Use `TabsItem` to organize fields across multiple tabs.

```python
from ttkbootstrap.widgets.composites.form import TabsItem, TabItem

items = [
    TabsItem(
        tabs=[
            TabItem(
                label="General",
                items=[
                    FieldItem(key="name", label="Name"),
                    FieldItem(key="email", label="Email"),
                ],
            ),
            TabItem(
                label="Advanced",
                items=[
                    FieldItem(key="debug", label="Debug mode", editor="checkbutton"),
                    FieldItem(key="timeout", label="Timeout", editor="numericentry"),
                ],
            ),
        ],
    ),
]

form = ttk.Form(app, items=items, data={})
```

---

## Data handling

### Getting form data

Use the `.data` property to retrieve current values.

```python
form = ttk.Form(app, data={"name": "Alice", "age": 25})
form.pack()

# Later...
current_data = form.data
print(current_data)  # {"name": "...", "age": ...}
```

### Setting form data

Update all fields by assigning to `.data` or using `configure(data=...)`.

```python
form.data = {"name": "Bob", "age": 30}

# Or
form.configure(data={"name": "Bob", "age": 30})
```

### Reacting to changes

Use `on_data_changed` callback to respond when any field changes.

```python
def handle_change(data):
    print("Form data changed:", data)

form = ttk.Form(app, data={}, on_data_changed=handle_change)
```

---

## Validation

Call `.validate()` to run validation rules on all fields. Returns `True` if all fields are valid.

```python
items = [
    FieldItem(
        key="email",
        label="Email",
        editor="textentry",
        editor_options={"required": True, "show_message": True},
    ),
]

form = ttk.Form(app, items=items, data={"email": ""})
form.pack()

if form.validate():
    print("All fields valid!")
    print(form.data)
else:
    print("Validation failed")
```

> See **TextEntry**, **NumericEntry**, and other `*Entry` widgets for validation options.

---

## Footer buttons

Add action buttons to the bottom of the form.

```python
form = ttk.Form(
    app,
    data={"name": ""},
    buttons=["Cancel", "Save"],
)
```

### Custom button configuration

```python
from ttkbootstrap.dialogs.dialog import DialogButton

buttons = [
    DialogButton(text="Cancel", role="cancel"),
    DialogButton(text="Save", role="primary", result="save"),
]

form = ttk.Form(app, data={}, buttons=buttons)
```

After a button is clicked, check `form.result` for the button's result value.

---

## Accessing field widgets

### Get field variables

```python
var = form.get_field_variable("name")
print(var.get())
```

### Get field signals

```python
signal = form.get_field_signal("age")
textsignal = form.get_field_textsignal("email")
```

### Access widgets directly

```python
# Widgets are stored in form._widgets
name_widget = form._widgets.get("name")
```

---

## Field options

### Common `FieldItem` options

```python
FieldItem(
    key="field_name",          # Required: unique identifier
    label="Field Label",       # Optional: display label (defaults to key)
    dtype='str',               # Optional: data type hint
    editor='textentry',        # Optional: editor type
    editor_options={},         # Optional: options passed to the editor widget
    readonly=False,            # Optional: make field read-only
    visible=True,              # Optional: show/hide field
    row=None,                  # Optional: explicit grid row
    column=None,               # Optional: explicit grid column
    columnspan=1,              # Optional: span multiple columns
    rowspan=1,                 # Optional: span multiple rows
)
```

### Common `editor_options`

For validation-enabled editors (`textentry`, `numericentry`, etc.):

```python
editor_options={
    "required": True,
    "show_message": True,
    "bootstyle": "primary",
}
```

For `selectbox`:

```python
editor_options={
    "items": ["Option 1", "Option 2", "Option 3"],
}
```

For `scale`:

```python
editor_options={
    "from_": 0,
    "to": 100,
    "orient": "horizontal",
}
```

---

## Bootstyle

Apply a bootstyle to the form container.

```python
form = ttk.Form(app, data={}, bootstyle="secondary")
```

---

## When should I use Form?

Use `Form` when:

- building dialogs with multiple input fields
- creating settings panels
- you need consistent field layout and validation
- data is structured as key-value pairs
- you want automatic field generation from data

Prefer individual widgets when:

- you only need 1-2 input fields
- you need complete custom layout control
- the form structure is very dynamic

---

## Related widgets

- **TextEntry** — text input with validation
- **NumericEntry** — numeric input with validation
- **DateEntry** — date picker
- **PasswordEntry** — masked password input
- **SelectBox** — dropdown selection
- **Dialog** — modal dialogs with forms
- **Field** — base class for form fields