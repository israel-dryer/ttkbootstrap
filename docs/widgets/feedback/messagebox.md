---
title: MessageBox
icon: fontawesome/solid/comment-dots
---

# MessageBox

`MessageBox` is a convenience facade for showing standard **message dialogs** (info, warning, error, question, OK/Cancel, Yes/No, etc.). It is built on top of `MessageDialog`, which in turn uses the generic `Dialog` system for consistent theming and button behavior.

Use `MessageBox` when you want a **fast, standardized** confirmation or notification dialog without building a custom `Dialog`.

<!--
IMAGE: MessageBox presets
Suggested: Grid of 4 dialogs: info/warning/error/question with their icons
Theme variants: light / dark
-->

---

## Basic usage

Show an informational message:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageBox

app = ttk.App()

MessageBox.show_info("Settings saved.", title="Success", master=app)

app.mainloop()
```

Ask a question and branch on the user’s choice:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageBox

app = ttk.App()

result = MessageBox.yesno("Delete this file?", title="Confirm", master=app)

if result == "Yes":
    print("Delete")
else:
    print("Cancel")

app.mainloop()
```

<!--
IMAGE: Basic Yes/No messagebox
Suggested: “Confirm” dialog with Yes/No buttons
-->

---

## What problem it solves

Most apps need “standard dialogs” repeatedly:

- show an error
- warn the user
- ask for confirmation
- provide OK/Cancel flows

`MessageBox` solves this by providing one-line helpers with sensible defaults:

- semantic icons (info/warn/error/question)
- common button sets (OK, OK/Cancel, Yes/No, etc.)
- consistent button roles and default selection
- optional system bell (`alert=True`)

---

## Core concepts

### MessageBox vs MessageDialog vs Dialog

- **MessageBox**
  - static helper methods
  - returns the text of the button pressed (or `None`)
  - fastest way to show standard dialogs

- **MessageDialog**
  - lightweight class for building message dialogs with custom buttons/icons
  - emits `<<DialogResult>>` on the target

- **Dialog**
  - generic dialog builder for fully custom layouts and workflows

If you just need “standard buttons + text”, use **MessageBox**.

---

### Return value

All `MessageBox` helpers return:

- the **text** of the pressed button (e.g., `"OK"`, `"Cancel"`, `"Yes"`, `"No"`, `"Retry"`)
- or `None` if the dialog is closed without a confirmed result

```python
result = MessageBox.okcancel("Continue?", master=app)
print(result)  # "OK" or "Cancel" (or None)
```

!!! note "Result is button text"
    The return value is the resolved button label text, not a boolean. Compare against the expected labels.

---

### Buttons and bootstyle parsing

`MessageDialog` (and therefore `MessageBox`) supports button label strings in two forms:

1) Plain labels:
```python
["Cancel", "OK"]
```

2) `label:bootstyle` format:
```python
["OK:primary"]
```

When no bootstyle is provided:

- the default/last button becomes `primary`
- other buttons become `secondary`
- the first button becomes `cancel` when its label contains “cancel”

You can also override the default button with `default="OK"` (or any button label).

<!--
IMAGE: Button style parsing
Suggested: Same message dialog showing default primary vs explicit "label:bootstyle" usage
-->

---

### Icons

`MessageDialog` can show an optional header icon. You may supply:

- a string icon name (Bootstrap Icons)
- a dict spec: `{"name": "...", "size": 32, "color": "..."}`

```python
from ttkbootstrap.dialogs import MessageDialog

dlg = MessageDialog(
    "Disk space is low.",
    title="Warning",
    icon="exclamation-triangle-fill",
)
dlg.show()
```

```python
dlg = MessageDialog(
    "Connection lost.",
    title="Error",
    icon={"name": "wifi-off", "size": 32, "color": "danger"},
)
dlg.show()
```

---

### Text wrapping and multiline messages

Messages are wrapped to a maximum character width (default: `width=50`), and multiline strings are supported.

```python
from ttkbootstrap.dialogs import MessageDialog

dlg = MessageDialog(
    "Line 1\nLine 2\nLine 3",
    width=60,
)
dlg.show()
```

---

### Localization

When `localize=True` is enabled (used internally by `MessageBox`), button labels are treated as translation keys and translated via `MessageCatalog`.

For example, if you use semantic keys:

- `button.ok`
- `button.cancel`

they will be translated automatically when the message catalog is configured.

!!! tip "Prefer semantic button keys"
    Use `button.ok` / `button.cancel` style keys for consistent localization across your app.

---

## Common MessageBox helpers

These methods are designed to be “drop-in” replacements for classic Tk message boxes:

```python
MessageBox.ok("Message", title="Title")
MessageBox.okcancel("Message")
MessageBox.yesno("Message")
MessageBox.yesnocancel("Message")
MessageBox.retrycancel("Message")

MessageBox.show_info("Message")
MessageBox.show_warning("Message")
MessageBox.show_error("Message")
MessageBox.show_question("Message")
```

The `show_*` variants include a default semantic icon.

---

## Events

### `<<DialogResult>>`

`MessageDialog` emits:

- `<<DialogResult>>` with `event.data = {"result": <str>, "confirmed": True}`

You can subscribe using the helper methods:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog

app = ttk.App()

dlg = MessageDialog("Saved", title="Info")

def on_result(payload):
    print("Result payload:", payload)

funcid = dlg.on_dialog_result(on_result)
dlg.show()

# later...
dlg.off_dialog_result(funcid)

app.mainloop()
```

!!! note "Target of the event"
    The event is generated on the dialog’s toplevel if available, otherwise on `master`.

---

## UX guidance

- Keep message text short and action-oriented
- Make destructive actions explicit (e.g., “Delete” instead of “OK”)
- Avoid using dialogs for non-critical feedback (use `Toast`)

!!! tip "Don’t interrupt unnecessarily"
    If the user doesn’t need to decide, show a Toast instead of a MessageBox.

---

## When to use / when not to

**Use MessageBox when:**

- You need a standard confirmation/alert quickly
- The dialog content is simple text + buttons
- You want built-in icons and consistent defaults

**Avoid MessageBox when:**

- You need rich layouts or embedded widgets (use `Dialog`)
- You need a form with multiple inputs (use `FormDialog`)
- You need non-blocking feedback (use `Toast`)

---

## Related widgets

- **MessageDialog** — class-based message dialog with custom buttons/icons
- **Dialog** — generic dialog builder
- **Toast** — non-blocking notifications
- **FilterDialog / DateDialog / FontDialog** — specialized picker dialogs
