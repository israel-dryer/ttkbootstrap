---
title: Forms
---

# Forms

`Form` is a spec-driven layout for collecting structured data. You hand it
a dict (or a list of field specs) and it builds the labels, inputs, and
validation wiring for you. This guide covers how to put one together end
to end.

This guide covers:

- **The two ways to define a form** — inferred from `data`, or explicit `items`
- **Editor types** — which input widget you get, and how to pick a different one
- **Reading and writing values** — `data`, `value`, signals, callbacks
- **Validation** — built-in rules and the `validate()` flow
- **Footer buttons and submit**
- **Grouping and tabs** for larger forms
- **Modal forms** with `FormDialog`

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App(title="Forms", size=(480, 360))

form = ttk.Form(
    app,
    data={"name": "", "age": 0, "active": True},
)
form.pack(fill="both", expand=True, padx=20, pady=20)

def submit():
    if form.validate():
        print(form.data)
    else:
        print("invalid")

ttk.Button(app, text="Submit", command=submit).pack(pady=(0, 20))
app.mainloop()
```

Pass an initial `data` dict and `Form` infers the field list from the
keys, picking an input widget for each value type:

| Value type | Editor |
|---|---|
| `str` | `textentry` |
| `int` / `float` | `numericentry` |
| `bool` | `checkbutton` |
| `date` / `datetime` | `dateentry` |

---

## Inferred vs. explicit layout

The `data` shortcut is great for prototypes and one-off windows. For
anything more — labels that aren't just title-cased keys, choice fields,
required validation, multi-column layouts — pass an `items` list instead:

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.form import FieldItem, GroupItem, TabsItem, TabItem

form = ttk.Form(
    app,
    items=[
        FieldItem(key="name", label="Full name"),
        FieldItem(key="email", label="Email"),
        FieldItem(
            key="role",
            label="Role",
            editor="selectbox",
            editor_options={"items": ["Admin", "User", "Viewer"]},
        ),
    ],
)
```

You can mix the two — supply `data` for initial values and `items` for
layout. Field specs may also be plain dicts if you'd rather not import
the dataclasses:

```python
items = [
    {"key": "name", "label": "Full name"},
    {"key": "role", "label": "Role", "editor": "selectbox",
     "editor_options": {"items": ["Admin", "User", "Viewer"]}},
]
form = ttk.Form(app, items=items, data={"name": "Alice", "role": "Admin"})
```

---

## Field specs

Each `FieldItem` describes one input. The most useful fields:

| Field | Description |
|---|---|
| `key` | Required. Identifier used in `form.data`. |
| `label` | Visible label. Defaults to `key.title()`. |
| `dtype` | Type hint: `'str'`, `'int'`, `'float'`, `'bool'`, `'date'`, `'datetime'`, `'password'`, or a Python type. Drives editor inference and parsing. |
| `editor` | Override the input widget — see the table below. |
| `editor_options` | Dict of options forwarded to the editor (e.g. `items=` for selectbox, bounds for numericentry). |
| `readonly` | Disable editing without hiding the field. |
| `visible` | Show or hide the field. |
| `column` / `row` / `columnspan` / `rowspan` | Explicit grid placement. Default is auto-flow. |

### Editor types

`Form` supports these editor names:

| Editor | Widget |
|---|---|
| `textentry` | [TextEntry](../widgets/inputs/textentry.md) |
| `numericentry` | [NumericEntry](../widgets/inputs/numericentry.md) |
| `passwordentry` | `PasswordEntry` |
| `dateentry` | [DateEntry](../widgets/inputs/dateentry.md) |
| `selectbox` | [SelectBox](../widgets/selection/selectbox.md) |
| `combobox` | [Combobox](../widgets/primitives/combobox.md) |
| `spinbox` | `Spinbox` |
| `text` | Multi-line `Text` |
| `toggle` / `switch` | `Switch` |
| `checkbutton` | `CheckButton` |
| `scale` | `Scale` |

If you omit `editor`, it's chosen from the value type or `dtype` — the
inference table from the Quick Start.

---

## Reading and writing values

```python
form.data            # dict of all current values
form.value           # alias for data; assignable to set everything at once
form.get()           # same as form.data

form.get_field_value("name")
form.set_field_value("name", "Alice")
form.set({"name": "Alice", "age": 31})
```

To react to changes as the user types, pass `on_data_changed` to the
constructor:

```python
form = ttk.Form(
    app,
    data={"query": ""},
    on_data_changed=lambda data: search(data["query"]),
)
```

The callback receives the full `data` dict each time any field changes.

### Per-field signals and variables

Each field exposes both a Tk `Variable` (for legacy callbacks) and a
[Signal](../capabilities/signals/index.md) — the framework-preferred
reactive primitive:

```python
form.field_signal("age").subscribe(lambda v: print(f"age = {v}"))

# Equivalent with a Tk Variable
var = form.field_variable("age")
var.trace_add("write", lambda *_: print(var.get()))
```

You can also access the underlying `Field` widget for focus and state
control:

```python
form.field("email").focus_set()
form.field("email").readonly(True)
```

---

## Validation

Validation in `Form` is **field-centric**: each field carries a list of
rules, and `form.validate()` runs them all and reports the result.

### Built-in rules

| Rule type | What it checks |
|---|---|
| `required` | Value is not empty or `None`. |
| `email` | Value matches an email pattern. |
| `pattern` | Value matches a regex (`pattern=`). |
| `stringLength` | Length within `min_length` / `max_length`. |
| `compare` | Value compared to another field's value. |
| `custom` | User-supplied callable. |

Attach rules to a field after the form is built:

```python
form.field("email").add_validation_rule("required")
form.field("email").add_validation_rule("email")
form.field("password").add_validation_rule("stringLength", min_length=8)
```

### Running validation

```python
def submit():
    if not form.validate():
        return                       # focus moves to the first invalid field
    save(form.data)
```

`validate()` returns `True` only if every rule passes. On failure it
focuses the first invalid field; each field also fires `<<Valid>>`,
`<<Invalid>>`, and `<<Validated>>` events with `{value, is_valid,
message}` payloads, so you can render inline errors or surface toasts:

```python
field = form.field("email")
field.bind("<<Invalid>>", lambda e: print(e.data["message"]))
```

---

## Footer buttons and submit

A `Form` can render its own footer buttons. Each button can carry a
`result` value that gets stored on `form.result` when clicked:

```python
form = ttk.Form(
    app,
    data={"name": "", "age": 0},
    buttons=[
        {"text": "Cancel", "role": "cancel", "result": None},
        {"text": "Save", "role": "primary", "result": "saved"},
    ],
)
```

For a free-standing form (not inside a dialog), button commands run
straight away. If you need validation before accepting, give the button
a `command` and short-circuit on failure:

```python
def save():
    if not form.validate():
        return
    persist(form.data)

form = ttk.Form(
    app,
    data={...},
    buttons=[
        {"text": "Cancel"},
        {"text": "Save", "role": "primary", "command": save},
    ],
)
```

---

## Grouping and tabs

For larger forms, organize fields into labeled sections (`GroupItem`) or
notebook tabs (`TabsItem`):

```python
from ttkbootstrap.widgets.composites.form import FieldItem, GroupItem, TabsItem, TabItem

items = [
    GroupItem(
        label="Profile",
        col_count=2,
        items=[
            FieldItem(key="first", label="First name"),
            FieldItem(key="last", label="Last name"),
            FieldItem(key="email", label="Email", columnspan=2),
        ],
    ),
    TabsItem(
        tabs=[
            TabItem(label="Preferences", items=[
                FieldItem(key="newsletter", dtype=bool, editor="toggle"),
                FieldItem(key="timezone", editor="selectbox",
                          editor_options={"items": ["UTC", "US/Eastern"]}),
            ]),
            TabItem(label="Limits", items=[
                FieldItem(key="daily_limit", dtype="float"),
                FieldItem(key="quota", dtype="int"),
            ]),
        ],
    ),
]

form = ttk.Form(app, items=items, col_count=1)
```

Groups arrange their children in a grid (`col_count`); tabs each get
their own `items` list with the same rules.

---

## Modal forms with FormDialog

When the form is the entire interaction — "fill this out and confirm or
cancel" — wrap it in a `FormDialog` instead of placing it on a window
yourself:

```python
import ttkbootstrap as ttk

dialog = ttk.FormDialog(
    title="New connection",
    data={"host": "localhost", "port": 5432, "ssl": True},
)
dialog.show()
if dialog.result:
    save_connection(dialog.result)
```

`FormDialog` accepts the same `data` / `items` / `col_count` /
`on_data_changed` arguments as `Form`. The result is the form's data
dict on success, `None` on cancel. See the
[Dialogs guide](dialogs.md#multi-field-input).

---

## Patterns and tips

### Validate early, focus the first error

`form.validate()` already focuses the first invalid field. Pair that with
inline error display (`<<Invalid>>` handler) so the user sees what's
wrong without a popup.

### Bind to changes, not just submit

For live previews, search-as-you-type, or auto-save, hook
`on_data_changed` (whole-form callback) or `field_signal(key)` (per
field). Both fire on every keystroke.

### Hide and show fields dynamically

Use `form.field(key).pack_forget()` / `grid_forget()` for runtime
visibility, or rebuild the form with a different `items` list. The
`visible=False` flag on `FieldItem` is honored at construction time.

### Prefer signals over Tk vars

Signals are the framework's preferred reactive primitive. They compose
better, don't leak across windows, and integrate with the rest of the
[reactivity system](reactivity.md). Reach for `field_variable` only when
interfacing with code that requires a Tk `Variable`.

---

## Additional resources

- [Form widget reference](../widgets/forms/form.md)
- [FormDialog](../widgets/dialogs/formdialog.md)
- [Dialogs guide](dialogs.md) — modal flows
- [Reactivity guide](reactivity.md) — signals, callbacks, events
- [TextEntry](../widgets/inputs/textentry.md),
  [NumericEntry](../widgets/inputs/numericentry.md),
  [DateEntry](../widgets/inputs/dateentry.md),
  [SelectBox](../widgets/selection/selectbox.md) — underlying field widgets
