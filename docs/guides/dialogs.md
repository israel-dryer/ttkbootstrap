---
title: Dialogs
---

# Dialogs

Dialogs are short, focused interactions that interrupt the main flow of your
application — confirming a destructive action, prompting for a value, picking
a date or color, filling out a quick form. ttkbootstrap ships ready-made
dialogs for the common cases plus a base class for building your own.

This guide covers:

- **Choosing the right dialog** — message vs. input vs. picker vs. form
- **The blocking call shape** — `dialog.show()` and `dialog.result`
- **Convenience facades** — `MessageBox` and `QueryBox`
- **Specialized pickers** — date, font, color, filter
- **Multi-field input** — `FormDialog`
- **Building custom dialogs** — subclassing `Dialog`

---

## Choosing a dialog

| You want to… | Use |
|---|---|
| Show a message and have the user acknowledge it | `MessageBox.show_info` / `show_warning` / `show_error` |
| Ask the user to confirm an action | `MessageBox.yesno` / `okcancel` |
| Prompt for a single string, number, or date | `QueryBox.get_string` / `get_integer` / `get_float` / `get_date` |
| Let the user pick one of a fixed list of values | `QueryBox.get_item` |
| Pick a color, font, or date with a rich picker UI | `ColorChooserDialog` / `FontDialog` / `DateDialog` |
| Filter a long list of options | `FilterDialog` |
| Collect several related fields at once | `FormDialog` |
| Build something none of the above covers | Subclass `Dialog` |

For the first six rows the convenience facades (`MessageBox`, `QueryBox`)
are usually all you need. Drop down to the dialog classes themselves when
you need fine-grained control over buttons, validation, or layout.

!!! note "Themed, not native"
    ttkbootstrap dialogs are styled Tk windows — they look the same on every
    platform but do **not** match the OS file or color picker. For native
    behavior (file pickers, system color/font dialogs) use Python's
    `tkinter.filedialog`, `tkinter.colorchooser`, or `tkinter.font` modules.
    See [Native vs custom dialogs](../widgets/dialogs/index.md#native-vs-custom-dialogs).

---

## The dialog call shape

Every dialog class in ttkbootstrap follows the same pattern:

```python
import ttkbootstrap as ttk

dialog = ttk.MessageDialog(message="Save changes?", buttons=["Cancel", "Save:primary"])
dialog.show()              # blocks until the user closes it
print(dialog.result)       # "Save", "Cancel", or None
```

`show()` is **modal and blocking** — it waits for the user to respond
before returning. After it returns, read `dialog.result` to find out what
happened.

`result` is `None` when the user dismisses the window without picking
anything (clicking the close button, pressing `Escape`). Always handle
that case:

```python
dialog.show()
if dialog.result is None:
    return                 # user dismissed the dialog — do nothing
if dialog.result == "Save":
    save_document()
```

The `MessageBox` and `QueryBox` facades wrap this pattern into one-line
calls that just return the value (or `None`):

```python
name = ttk.QueryBox.get_string(prompt="Project name:", title="New Project")
if name is None:
    return
print(f"Creating {name}")
```

---

## Message dialogs

Use a message dialog when you need to **tell** or **ask** the user something.

### One-line confirmations and notifications

`MessageBox` is a static facade with one method per common pattern:

```python
import ttkbootstrap as ttk

# Acknowledgement (single OK button + icon)
ttk.MessageBox.show_info("Settings saved.")
ttk.MessageBox.show_warning("This will reset your preferences.")
ttk.MessageBox.show_error("Could not connect to server.")
ttk.MessageBox.show_question("Continue with the current selection?")

# Action choices (no icon)
choice = ttk.MessageBox.yesno("Delete this file?")
if choice == "Yes":
    delete_file()

choice = ttk.MessageBox.okcancel("Apply changes?")
choice = ttk.MessageBox.yesnocancel("Save before closing?")
choice = ttk.MessageBox.retrycancel("Connection failed.")
```

Each method returns the **text** of the button pressed (`"OK"`, `"Yes"`,
`"No"`, etc.) or `None` if the user dismissed the dialog. Always test
against the actual button text.

### Custom buttons and styling

For non-standard button sets, drop down to `MessageDialog` directly. Button
specs accept a `"label:variant"` syntax to mark the primary action:

```python
import ttkbootstrap as ttk

dialog = ttk.MessageDialog(
    message="This will permanently delete 12 files.",
    title="Confirm delete",
    buttons=["Cancel", "Delete:danger"],
)
dialog.show()
if dialog.result == "Delete":
    perform_delete()
```

Common role suffixes: `primary`, `secondary`, `success`, `warning`,
`danger`, `info`. They follow the same accent vocabulary used elsewhere
in the library.

---

## Input prompts

Use an input prompt when you need **a single value** from the user.

### Strings, numbers, and dates

`QueryBox` covers the common cases:

```python
import ttkbootstrap as ttk
from datetime import date

name = ttk.QueryBox.get_string(prompt="New name:", value="Untitled")

count = ttk.QueryBox.get_integer(prompt="How many?", minvalue=1, maxvalue=99)

ratio = ttk.QueryBox.get_float(prompt="Scale factor:", value=1.0)

day = ttk.QueryBox.get_date(value=date.today())
```

All return the value or `None` on cancel.

### Picking from a list

`get_item` shows a dropdown and returns the chosen string:

```python
choice = ttk.QueryBox.get_item(
    prompt="Pick a theme:",
    items=["light", "dark", "system"],
    value="system",
)
```

### Validation and bounds

For tighter control — bounds, custom validation, formatting — use
`QueryDialog` directly. `QueryBox.get_integer` and `get_float` already
accept `minvalue` / `maxvalue`; `QueryDialog` adds support for
`value_format` patterns and validation rules attached to the underlying
field.

```python
import ttkbootstrap as ttk

dialog = ttk.QueryDialog(
    prompt="Port number:",
    title="Server settings",
    value="8080",
    datatype=int,
    minvalue=1024,
    maxvalue=65535,
)
dialog.show()
port = dialog.result
```

---

## Specialized pickers

When the value being chosen has a rich UI (a calendar, a color spectrum,
a font preview), use the dedicated picker dialog.

| Picker | Class | One-liner |
|---|---|---|
| Date | `DateDialog` | `QueryBox.get_date(...)` |
| Font | `FontDialog` | `QueryBox.get_font(...)` |
| Color | `ColorChooserDialog` | `QueryBox.get_color(...)` |
| Multi-select filter | `FilterDialog` | — |

```python
import ttkbootstrap as ttk
from datetime import date

color = ttk.QueryBox.get_color(value="#3498db")
font = ttk.QueryBox.get_font()

picker = ttk.DateDialog(initial_date=date.today())
picker.show()
selected_date = picker.result
```

`ColorChooserDialog` includes spectrum, themed-palette, and standard-palette
tabs, plus an optional screen "dropper" for sampling pixels from anywhere
on screen.

`FilterDialog` is the right fit for "let the user pick which of these items
to keep" — a list of checkboxes with optional search:

```python
columns = ["Name", "Email", "Department", "Hire date", "Manager"]
dialog = ttk.FilterDialog(items=columns, enable_search=True)
dialog.show()
visible = dialog.result   # list of selected items, or None
```

---

## Multi-field input

`FormDialog` embeds a [Form](../widgets/forms/form.md) inside a modal
dialog. Use it when you need **several related fields** in one step:

```python
import ttkbootstrap as ttk

dialog = ttk.FormDialog(
    title="New connection",
    data={"host": "localhost", "port": 5432, "ssl": True},
)
dialog.show()
if dialog.result:
    save_connection(dialog.result)   # dict of field values
```

`result` is the form's data dict on success, `None` on cancel. For explicit
layout (groups, tabs, custom editors, validation rules) pass an `items`
spec instead of `data` — see the [Forms guide](forms.md) for the field
grammar.

---

## Building custom dialogs

When none of the built-in dialogs fit, instantiate `Dialog` directly with
a content builder, or subclass it:

```python
import ttkbootstrap as ttk

def build_content(parent):
    ttk.Label(parent, text="Pick the columns to export:").pack(
        anchor="w", padx=12, pady=(12, 4)
    )
    box = ttk.Frame(parent, padding=12)
    box.pack(fill="both", expand=True)
    return box

dialog = ttk.Dialog(
    title="Export",
    content_builder=build_content,
    buttons=["Cancel", "Export:primary"],
)
dialog.show()
```

Common building blocks:

- **`content_builder`** — function that receives a parent frame and adds
  your widgets.
- **`buttons`** — list of button specs (strings, dicts, or `DialogButton`
  instances). The first button appears rightmost.
- **`mode="popover"`** — anchor the dialog to a widget instead of centering it.
- **`dialog.result`** — set inside button commands to communicate back to
  the caller.

For a fuller reference, see the [Dialog widget page](../widgets/dialogs/dialog.md).

---

## Patterns and tips

### Always parent your dialogs

Pass `master=` so the dialog inherits the right window for centering,
modality, and theme. Without it, the dialog falls back to the default
root, which is fine for top-level prompts but wrong for dialogs launched
from a secondary `Toplevel`.

```python
ttk.MessageBox.show_info("Done.", master=self.window)
```

### Keep the main thread responsive

`show()` blocks the calling thread. That's fine inside a button command —
the event loop owns the call stack — but **do not** call `show()` from a
worker thread. Marshal the result back first. See
[Threading & async](../platform/threading-and-async.md).

### Confirm destructive actions

For destructive flows, use `MessageDialog` with a `:danger` primary button
so the consequence is visible:

```python
dialog = ttk.MessageDialog(
    message=f"Permanently delete '{name}'?",
    buttons=["Cancel", "Delete:danger"],
)
dialog.show()
if dialog.result == "Delete":
    delete_item(name)
```

### Localize button text

Standard button labels (`OK`, `Cancel`, `Yes`, `No`, `Retry`) flow through
the message catalog when the dialog is built with `localize=True` —
`MessageBox` and `QueryBox` do this for you. For your own dialogs, wrap
labels with `L("Save")` so they translate. See the
[Localization guide](localization.md).

---

## Additional resources

- [Dialogs widget index](../widgets/dialogs/index.md) — per-dialog reference
- [MessageBox](../widgets/dialogs/messagebox.md) /
  [MessageDialog](../widgets/dialogs/messagedialog.md)
- [QueryBox](../widgets/dialogs/querybox.md) /
  [QueryDialog](../widgets/dialogs/querydialog.md)
- [FormDialog](../widgets/dialogs/formdialog.md) — see also the
  [Forms guide](forms.md)
- [DateDialog](../widgets/dialogs/datedialog.md),
  [FontDialog](../widgets/dialogs/fontdialog.md),
  [ColorChooser](../widgets/dialogs/colorchooser.md),
  [FilterDialog](../widgets/dialogs/filterdialog.md)
- [Dialog](../widgets/dialogs/dialog.md) — base class for custom dialogs
