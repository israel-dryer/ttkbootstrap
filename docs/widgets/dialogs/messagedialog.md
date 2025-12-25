---
title: MessageDialog
---

# MessageDialog

`MessageDialog` is a **modal dialog class** for displaying messages with customizable buttons.

Use `MessageDialog` when you need a simple message popup with custom button labels, icons, and styling. For common patterns (info, warning, error, yes/no), prefer the convenience methods in [MessageBox](messagebox.md).

---

## Quick start

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog

app = ttk.App()

dialog = MessageDialog(
    message="Are you sure you want to proceed?",
    title="Confirm Action",
    buttons=["Cancel", "Proceed"],
    icon="question-circle-fill",
)
dialog.show()

print("User clicked:", dialog.result)

app.mainloop()
```

---

## When to use

Use `MessageDialog` when:

- you need custom button labels or styling
- you want to display an icon with your message
- you need programmatic control over the dialog

### Consider a different control when...

- you want a standard info/warning/error dialog -> use [MessageBox](messagebox.md) static methods
- you need user input -> use [QueryDialog](querydialog.md)
- you need a complex form -> use [FormDialog](formdialog.md)

---

## Common options

### `message`

The message text to display. Supports multiline strings.

### `title`

The dialog window title.

### `buttons`

List of button labels. Can specify bootstyle as `"label:bootstyle"`.

```python
dialog = MessageDialog(
    message="Choose an action",
    buttons=["Cancel", "Save:primary", "Delete:danger"],
)
```

### `icon`

Optional icon to display. Can be a string (icon name) or dict with `name`, `size`, `color`.

```python
MessageDialog(message="Success!", icon="check-circle-fill")
MessageDialog(message="Error!", icon={"name": "x-circle-fill", "size": 48, "color": "danger"})
```

### `default`

The button label to use as default (receives primary bootstyle and focus).

### `alert`

If True, rings the system bell when shown.

---

## Behavior

- The dialog is modal - blocks interaction with the parent until closed.
- Clicking any button closes the dialog and sets `result` to the button text.
- The `result` property returns None if the dialog was closed without clicking a button.

---

## Events

`MessageDialog` emits `<<DialogResult>>` when closed.

```python
def on_result(payload):
    print("Result:", payload["result"])
    print("Confirmed:", payload["confirmed"])

dialog.on_dialog_result(on_result)
dialog.show()
```

---

## Additional resources

### Related widgets

- [MessageBox](messagebox.md) - static convenience methods for common message patterns
- [QueryDialog](querydialog.md) - dialogs with user input
- [Dialog](dialog.md) - base dialog class for custom dialogs

### API reference

- [`ttkbootstrap.dialogs.MessageDialog`](../../reference/dialogs/MessageDialog.md)