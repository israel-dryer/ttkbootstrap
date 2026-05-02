---
title: Forms
---

# Forms

`Form` is a spec-driven layout for collecting structured data. You hand it
either a starting `data` dict (and it infers the fields) or an explicit
`items` list (and it lays them out). It builds the labels, the input
widgets, the data binding, and the validation hooks for you.

When the form is the entire interaction — *fill this out, confirm or
cancel* — wrap it in a [`FormDialog`](#modal-forms-with-formdialog)
instead of placing it on a window yourself. Both share the same `data`
and `items` grammar; the only difference is the chrome around them.

This guide covers:

- Two ways to define a form: inferred from `data`, or explicit `items`
- The field grammar (`FieldItem`, editor types, options)
- Reading and writing values (`data`, signals, callbacks)
- Validation (rules, triggers, error display)
- Footer buttons and submit flow
- Grouping and tabs for larger forms
- Modal forms with `FormDialog`

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

When you pass `data` and no `items`, `Form` infers one field per key,
choosing the editor from the value's Python type:

| Value type | Editor inferred |
|---|---|
| `str` | `textentry` |
| `int` | `numericentry` |
| `float` | `numericentry` |
| `bool` | `checkbutton` |
| `date` / `datetime` | `dateentry` |

The label defaults to `key.title()` (with underscores replaced by spaces).

---

## Inferred vs. explicit layout

The `data` shortcut is convenient for prototypes and one-off forms. For
anything more — labels that aren't title-cased keys, choice fields,
required validation, multi-column layouts — pass an `items` list:

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.form import (
    FieldItem, GroupItem, TabsItem, TabItem,
)

app = ttk.App(title="Forms", size=(480, 360))

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
form.pack(fill="both", expand=True, padx=20, pady=20)
app.mainloop()
```

`FieldItem`, `GroupItem`, `TabsItem`, and `TabItem` aren't re-exported on
the `ttk.*` namespace yet — import them from
`ttkbootstrap.widgets.composites.form` as shown above, or use the plain
dict form below.

You can mix the two — `data` for initial values plus `items` for layout:

```python
items = [
    FieldItem(key="name", label="Full name"),
    FieldItem(key="role", label="Role", editor="selectbox",
              editor_options={"items": ["Admin", "User", "Viewer"]}),
]
form = ttk.Form(app, items=items, data={"name": "Alice", "role": "Admin"})
```

Field specs can also be plain dicts. The grammar is the same — every
`FieldItem` field becomes a dict key, with `type="field"` (default),
`type="group"`, or `type="tabs"` to discriminate:

```python
items = [
    {"key": "name", "label": "Full name"},
    {"key": "role", "label": "Role", "editor": "selectbox",
     "editor_options": {"items": ["Admin", "User", "Viewer"]}},
]
form = ttk.Form(app, items=items, data={"name": "Alice", "role": "Admin"})
```

---

## Field grammar

Each `FieldItem` describes one input. The most useful fields:

| Field | Description |
|---|---|
| `key` | Required. Identifier used in `form.data` and `form.field(key)`. |
| `label` | Visible label. Defaults to `key.title()`. |
| `dtype` | Type hint: `'str'`, `'int'`, `'float'`, `'bool'`, `'date'`, `'datetime'`, `'password'`, or a Python type. Drives editor inference and value coercion. |
| `editor` | Override the input widget — see editor types below. |
| `editor_options` | Dict of options forwarded to the editor (e.g. `{"items": [...]}` for selectbox, bounds for numericentry, `required=True` for the underlying `Field`). |
| `readonly` | Make the field non-editable without hiding it. |
| `visible` | If `False`, the field is skipped entirely at construction. |
| `column`, `row`, `columnspan`, `rowspan` | Explicit grid placement. Default is auto-flow across the form's `col_count` columns. |

### Editor types

`Form` accepts these editor names. Omit `editor` and one is chosen from
`dtype` (or the value's Python type) using the inference table from the
quick start.

| Editor | Widget | Typical use |
|---|---|---|
| `textentry` | [TextEntry](../widgets/inputs/textentry.md) | Single-line text |
| `numericentry` | [NumericEntry](../widgets/inputs/numericentry.md) | `int` / `float` with bounds |
| `passwordentry` | `PasswordEntry` | Masked text input |
| `dateentry` | [DateEntry](../widgets/inputs/dateentry.md) | Date / datetime picker |
| `selectbox` | [SelectBox](../widgets/inputs/selectbox.md) | Pick one of N items |
| `combobox` | [Combobox](../widgets/primitives/combobox.md) | Same, with free-text fallback |
| `spinbox` | `Spinbox` | Stepper for small numeric ranges |
| `text` | Multi-line `Text` | Long-form text |
| `toggle` / `switch` | `Switch` | Boolean as a switch |
| `checkbutton` | `CheckButton` | Boolean as a checkbox |
| `scale` | `Scale` | Numeric on a slider |

### Options forwarded via `editor_options`

`editor_options` is passed straight to the underlying widget
constructor. Common shapes:

- `selectbox` / `combobox`: `{"items": ["A", "B", "C"]}`
- `numericentry` / `spinbox` / `scale`: `{"from_": 0, "to": 100}` (bounds and stepping vary per widget — see each widget page)
- `textentry` / `passwordentry` / `numericentry` / `dateentry`: `{"required": True}` adds a built-in required-rule on the underlying `Field`; `{"show_message": True}` reserves space for inline error text under the input.

---

## Reading and writing values

```python
form.data            # dict of all current values (read-only property)
form.value           # alias for data; also writable as a setter
form.get()           # same as form.data
form.set({"name": "Alice", "age": 31})  # bulk assign

form.get_field_value("name")
form.set_field_value("name", "Alice")
```

Values returned by `form.data` are coerced according to each field's
`dtype` (so `int` fields come back as `int`, `bool` fields as `bool`,
etc.). Strings are returned as-is.

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

### Per-field signals and Tk variables

Each field has a `Field` widget you can pull out by key. `Field` exposes
both a Tk `Variable` (for legacy callbacks) and a
[Signal](../capabilities/signals/index.md) — the framework's preferred
reactive primitive:

```python
field = form.field("email")
field.signal.subscribe(lambda value: print(f"email = {value}"))

# Equivalent with a Tk Variable
field.variable.trace_add("write", lambda *_: print(field.variable.get()))
```

You can also use the form-level accessors, but they currently return
`None` for most field types — prefer `form.field(key).signal` and
`form.field(key).variable`. The form-level helpers exist mainly for
dynamic widgets (Spinbox, scale, toggle) that bypass the `Field`
wrapper:

```python
form.field_variable("toggle_field")   # Tk Variable for non-Field editors
form.field_signal("some_key")         # may be None
```

The same `form.field(key)` handle is the way into focus and state
control:

```python
form.field("email").focus_set()
form.field("email").readonly(True)
```

---

## Validation

Validation in `Form` is **field-centric**: each field carries a list of
rules, and `form.validate()` runs them all and reports the result.

### Built-in rule types

| Rule | Parameters | What it checks |
|---|---|---|
| `required` | — | Value isn't `None` and isn't an empty/whitespace string. |
| `email` | — | Value matches an email pattern. |
| `pattern` | `pattern=r"..."` | Value matches a regex. |
| `stringLength` | `min=`, `max=` | Length within `[min, max]`. |
| `custom` | `func=callable` | `func(value)` returns truthy. |

Each rule also accepts `message="..."` to override the default error
text and `trigger=...` to control when it fires (see below).

### Attaching rules

Attach rules to a field after the form is built:

```python
form.field("email").add_validation_rule("required")
form.field("email").add_validation_rule("email")
form.field("password").add_validation_rule("stringLength", min=8, max=64)
form.field("port").add_validation_rule(
    "custom",
    func=lambda v: v.isdigit() and 0 <= int(v) <= 65535,
    message="Port must be 0-65535.",
)
```

For the common case, `editor_options={"required": True}` on the
`FieldItem` adds the `required` rule for you when the form is built.

### Triggers and `form.validate()`

Each rule has a *trigger* that controls when it runs:

- `always` — every keystroke and on manual validation
- `blur` — when focus leaves the field, and on manual validation
- `key` — every keystroke
- `manual` — only when called explicitly

`form.validate()` runs only rules with trigger `always` or `manual` —
the same rules that fire field-by-field as the user types. To force a
rule to participate in `form.validate()` regardless of its default,
pass `trigger="manual"` (or `"always"`) when adding it:

```python
form.field("password").add_validation_rule(
    "stringLength", min=8, trigger="manual",
)
```

(`stringLength` defaults to `blur`, so without the override it wouldn't
fail the form on submit if the user never tabbed off the field.)

### Running validation

```python
def submit():
    if not form.validate():
        return                       # focus moves to the first invalid field
    save(form.data)
```

`validate()` returns `True` only if every rule passes. On failure it
focuses the first invalid field. Each field also fires `<<Valid>>`,
`<<Invalid>>`, and `<<Validate>>` virtual events with a payload of
`{value, is_valid, message}`, so you can render inline errors or
surface toasts:

```python
field = form.field("email")
field.bind("<<Invalid>>", lambda e: print(e.data["message"]))
```

The default `Field` renders inline error text under the input
automatically when `show_message=True` is set in `editor_options` (or
when the underlying entry was constructed with `show_message=True`).

### Async validation

The validation system is synchronous — there is no built-in hook for
awaiting a server-side check before the form is considered valid. The
pattern for async checks is:

1. Call `form.validate()` for the synchronous rules.
2. If it passes, kick off the async work (worker thread, future,
   `asyncio` task) and disable the submit button.
3. On the result, call `form.field(key).event_generate("<<Invalid>>",
   data={...})` to surface server-side errors, or proceed with persist
   / close.

---

## Footer buttons and submit

`Form` can render its own footer buttons. Each button can carry a
`result` value that's stored on `form.result` when clicked:

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

Button specs accept the same shape as `DialogButton` (`text`, `role`,
`result`, `command`, `default`, plus accent / variant overrides). Roles
control the default styling: `primary`, `secondary`, `cancel`, `danger`,
`help`.

For a free-standing form (not inside a dialog), button commands run
straight away. To validate before accepting, give the button a
`command` and short-circuit on failure:

```python
def save(form):
    if not form.validate():
        return
    persist(form.data)

form = ttk.Form(
    app,
    data={"name": "", "age": 0},
    buttons=[
        {"text": "Cancel"},
        {"text": "Save", "role": "primary", "command": save},
    ],
)
```

Inside a `FormDialog`, validation is already wired into the primary
button and runs automatically — see below.

### Resetting and dirty state

`Form` doesn't track a dirty flag for you, but the building blocks are
there:

```python
initial = {"name": "Alice", "email": "alice@example.com"}
form = ttk.Form(app, data=initial)

# Reset to the original
form.set(initial)

# Compare against the snapshot
def is_dirty():
    return form.data != initial
```

For more elaborate dirty-tracking, subscribe to `on_data_changed` and
diff against the snapshot, or wire a `Signal` per field via
`form.field(key).signal`.

---

## Grouping and tabs

For larger forms, organize fields into labeled sections (`GroupItem`)
or notebook tabs (`TabsItem`):

```python
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.form import (
    FieldItem, GroupItem, TabsItem, TabItem,
)

app = ttk.App(title="Forms", size=(640, 480))

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
form.pack(fill="both", expand=True, padx=20, pady=20)
app.mainloop()
```

`GroupItem` arranges its children in a grid (`col_count` and
`min_col_width` are independent of the parent form's). Each `TabItem`
holds its own `items` list with the same grammar; tabs themselves
inherit the form's `col_count` unless an inner `GroupItem` overrides it.

---

## Modal forms with FormDialog

When the form is the entire interaction, wrap it in a `FormDialog`:

```python
import ttkbootstrap as ttk

dialog = ttk.FormDialog(
    title="New connection",
    data={"host": "localhost", "port": 5432, "ssl": True},
)
dialog.show()
if dialog.result:
    print(dialog.result)   # dict of field values
```

`FormDialog` accepts the same `data`, `items`, `col_count`, and
`on_data_changed` arguments as `Form`. It adds its own Cancel / OK
footer (override with `buttons=` if needed), wires `form.validate()`
into the primary button automatically, and exposes the underlying
form on `dialog.form`:

```python
dialog = ttk.FormDialog(
    title="New connection",
    items=[...],
    data={...},
)

# Attach validation rules to the embedded form before showing
def configure(form):
    form.field("host").add_validation_rule("required")
    form.field("port").add_validation_rule(
        "custom",
        func=lambda v: 0 <= int(v) <= 65535,
        trigger="manual",
        message="Port must be 0-65535.",
    )

# `form` is built lazily inside show(); use a custom button command
# or subclass for setup that needs the rendered widgets.
```

`dialog.result` is the form's data dict on success and `None` on cancel.
See the [Dialogs guide](dialogs.md#multi-field-input) for the broader
dialog patterns.

---

## Patterns and tips

### Validate early, focus the first error

`form.validate()` already focuses the first invalid field. Pair that
with inline error display (`show_message=True` in `editor_options`, or
a `<<Invalid>>` handler) so the user sees what's wrong without a
popup.

### Bind to changes, not just submit

For live previews, search-as-you-type, or auto-save, hook
`on_data_changed` (whole-form callback) or
`form.field(key).signal.subscribe(...)` (per field). Both fire on
every keystroke.

### Prefer signals over Tk vars

Signals are the framework's preferred reactive primitive — they
compose, don't leak across windows, and integrate with the rest of the
[reactivity system](reactivity.md). Reach for `Field.variable` only
when interfacing with code that requires a Tk `Variable`.

### Rebuild instead of hide-and-show

There's no first-class "hide a field" API at runtime. For dynamic
forms, the durable approach is to recompute the `items` list and
rebuild the form (or two forms in a stack). The `visible=False` flag
on `FieldItem` is honored at construction time only.

---

## Additional resources

- [Form widget reference](../widgets/inputs/form.md)
- [FormDialog](../widgets/dialogs/formdialog.md)
- [Dialogs guide](dialogs.md) — modal flows
- [Reactivity guide](reactivity.md) — signals, callbacks, events
- [TextEntry](../widgets/inputs/textentry.md),
  [NumericEntry](../widgets/inputs/numericentry.md),
  [DateEntry](../widgets/inputs/dateentry.md),
  [SelectBox](../widgets/inputs/selectbox.md) — underlying field widgets
