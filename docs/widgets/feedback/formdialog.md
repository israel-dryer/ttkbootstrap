---
title: FormDialog
icon: fontawesome/solid/rectangle-list
---

# FormDialog

`FormDialog` is a data-entry dialog that embeds a `Form` widget inside a `Dialog`. It’s the “batteries included” way to collect structured input with **auto-inferred fields** (from a data dict) or an **explicit form layout** (FieldItem / GroupItem / TabsItem), with validation and a standard OK/Cancel footer.

<!--
IMAGE: FormDialog overview
Suggested: FormDialog with two columns, mixed field types (text, number, checkbox), and OK/Cancel footer
Theme variants: light / dark
-->

---

## Basic usage

### Auto-infer fields from data

Pass a dict and `FormDialog` will infer editors from types:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FormDialog

app = ttk.App()

initial_data = {
    "first_name": "Jane",
    "last_name": "Doe",
    "age": 30,
    "active": True,
}

dlg = FormDialog(
    master=app,
    title="Edit User",
    data=initial_data,
    col_count=2,
)

dlg.show()

if dlg.result:
    print("Updated:", dlg.result)

app.mainloop()
```

<!--
IMAGE: Auto-inferred fields
Suggested: Same example rendered, highlighting inferred editors for bool/int/str
-->

### Explicit layout with groups

Use `FieldItem`, `GroupItem`, and `TabsItem` when you want a curated layout:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FormDialog
from ttkbootstrap.widgets.composites.form import FieldItem, GroupItem

app = ttk.App()

items = [
    GroupItem(
        label="Personal Info",
        col_count=2,
        items=[
            FieldItem(key="first_name", label="First Name"),
            FieldItem(key="last_name", label="Last Name"),
            FieldItem(key="email", label="Email"),
        ],
    ),
    FieldItem(key="bio", label="Bio", editor="text"),
]

dlg = FormDialog(
    master=app,
    title="User Profile",
    items=items,
    data={"first_name": "", "last_name": "", "email": "", "bio": ""},
    buttons=["Cancel", "Save"],
)

dlg.show()
print(dlg.result)

app.mainloop()
```

<!--
IMAGE: GroupItem layout
Suggested: LabelFrame group with two-column grid + a full-width text editor beneath
-->

---

## What problem it solves

Most “settings” or “edit record” dialogs are the same workflow:

1. Show a set of labeled fields
2. Validate input
3. Return structured data on OK
4. Scroll when the dialog is taller than the window

`FormDialog` packages that workflow into a single component:

- Embeds a `Form` inside a `Dialog`
- Auto-generates fields or accepts explicit layouts
- Provides a standard footer (Cancel/OK by default)
- Validates before accepting non-cancel actions
- Handles scrolling internally (no extra plumbing)

---

## Core concepts

### Result value

After `.show()`, results are available on:

```python
dlg.result  # dict[str, Any] | None
```

- a dict when the user confirms
- `None` when the user cancels/closes

Internally, `FormDialog` transfers the embedded `Form`’s `data` on success.

---

### Buttons are normalized and validated

`buttons` can be:

- `DialogButton` instances
- dicts that become `DialogButton(**mapping)`
- strings (convenience)

If you don’t provide buttons, the default is:

- Cancel (role: `cancel`, result: `None`)
- OK (role: `primary`, result: `"ok"`, default=True)

**Important behavior:** for non-cancel actions, the dialog validates the form before closing.

!!! tip "Use roles, not custom styles"
    Prefer `role="primary"` / `role="cancel"` over hard-coding bootstyles so your dialogs stay consistent.

---

### Scroll behavior is built in

`FormDialog` manages scrolling internally using a `ScrollView` so long forms don’t overflow the screen.

- `scrollable=True` is kept for compatibility but scrolling is effectively handled by the dialog
- `scrollview_options` lets you tune scrollbar behavior (defaults keep the scrollbar visible to avoid width “jumps”)

```python
dlg = FormDialog(
    master=app,
    data=initial_data,
    scrollview_options={"show_scrollbar": "always"},
)
```

<!--
IMAGE: Internal scrolling
Suggested: A tall form showing scrollbar behavior and consistent content width
-->

---

### Dialog sizing (minsize) is calculated

If you don’t supply `minsize`, the dialog calculates a minimum width based on:

- `col_count * min_col_width`
- nested structures (groups/tabs) when `items` are provided
- internal padding + dialog chrome

This prevents accidental horizontal scrolling caused by too-narrow dialogs.

You can still override:

```python
dlg = FormDialog(master=app, data=initial_data, minsize=(720, 420))
```

---

## Common options & patterns

### Respond to live data changes

Use `on_data_changed` to react when any field changes:

```python
def on_data_changed(data: dict):
    print("changed:", data)

dlg = FormDialog(master=app, data=initial_data, on_data_changed=on_data_changed)
dlg.show()
```

!!! note "Live changes vs confirmation"
    `on_data_changed` fires as the user edits fields. `result` is only produced when the user confirms.

---

### Custom validation before closing

To validate beyond per-field validation, provide a button with a command.
Return `False` to keep the dialog open.

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import FormDialog, DialogButton
from tkinter import messagebox

app = ttk.App()

def validate_and_close(dlg: FormDialog):
    data = dlg.form.data
    if not data.get("email"):
        messagebox.showwarning("Validation Error", "Email is required!")
        return False  # keep open
    # returning None/True allows close; FormDialog will set result to form data

dlg = FormDialog(
    master=app,
    title="Registration",
    data={"email": "", "password": ""},
    buttons=[
        DialogButton(text="Cancel", role="cancel", result=None),
        DialogButton(text="Register", role="primary", result="submitted", command=validate_and_close, default=True),
    ],
)

dlg.show()
print(dlg.result)

app.mainloop()
```

---

### Popover mode (advanced)

`FormDialog` forwards `mode="popover"` to the underlying `Dialog`.
Popover mode is best for small, contextual forms.

```python
dlg = FormDialog(master=app, data={"query": ""}, mode="popover")
dlg.show(anchor_to="cursor", anchor_point="sw", window_point="nw", offset=(8, 8), auto_flip=True)
```

<!--
IMAGE: Popover FormDialog
Suggested: Small single-field form popover anchored to a search button
-->

---

## Events

`FormDialog` is primarily used imperatively:

- Call `show(...)`
- Read `result` afterward
- Use `on_data_changed` for live updates

For richer dialog lifecycle events, use `Dialog` directly and embed a `Form` in `content_builder`.

---

## UX guidance

- Prefer 1–2 columns for dialogs; more columns reduce readability
- Use groups/tabs to reduce cognitive load on large forms
- Always provide a clear cancel path
- Keep confirmation labels specific (“Save”, “Apply”, “Register”)

!!! tip "Make confirmation explicit"
    Use a primary action label that reflects what will happen (“Save changes” vs “OK”) when the operation has side effects.

---

## When to use / when not to

**Use FormDialog when:**

- You need to collect structured input and return a dict
- You want a fast, consistent settings/edit dialog pattern
- The form may need scrolling or layout grouping

**Avoid FormDialog when:**

- The workflow is multi-step (use `PageStack`)
- You only need a single value (consider a smaller query dialog or inline field)
- You need highly custom layout beyond Form’s item model (use `Dialog` + custom content)

---

## Related widgets

- **Dialog** — generic dialog builder (FormDialog uses it internally)
- **Form** — embedded data-entry widget
- **ScrollView** — used internally for scrolling long forms
- **DateDialog / FontDialog / FilterDialog** — specialized picker-style dialogs
