---
title: MessageBox
---

# MessageBox

`MessageBox` is a **modal feedback dialog** for communicating information and collecting simple user confirmation.

It supports common dialog types like info, warning, error, question/confirm, and can return a result indicating what the user chose.

Use MessageBox for:

- confirmations (Delete? Quit without saving?)

- error reporting (Something failed)

- simple alerts (Action completed)

<!--
IMAGE: MessageBox examples
Suggested: 3 small dialogs (info/warning/error) in light/dark
-->

---

## Quick start

### Information

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.MessageBox.ok(
    title="Saved",
    message="Your changes have been saved.",
)

app.mainloop()
```

### Confirm / question

```python
result = ttk.MessageBox.yesno(
    title="Delete file?",
    message="This action can't be undone.",
)
print("User chose:", result)  # typically True/False or "Yes"/"No"
```

---

## When to use

Use `MessageBox` when:

- you need the user to acknowledge or decide something before continuing

- the decision is simple (1-3 buttons)

- the dialog should be modal

### Consider a different control when...

- you want non-blocking feedback (Saved!, Copied!) - use [Toast](../overlays/toast.md) instead

- feedback is contextual and shouldn't interrupt workflow - use [Tooltip](../overlays/tooltip.md) or inline messaging instead

---

## Examples & patterns

### Common dialog types

Most apps stick to a small set of patterns:

- **Info** - success/neutral notification

- **Warning** - proceed with caution

- **Error** - operation failed

- **Question** - user must choose

Use the highest-level helper that matches your intent (e.g., `ok`, `yesno`, `okcancel`) to keep UI consistent.

### Common options

#### `title` and `message`

```python
ttk.MessageBox.ok(title="Notice", message="Hello!")
```

#### Detail / secondary text (if supported)

Use detail text for stack traces or extra explanation.

```python
ttk.MessageBox.show(
    title="Import failed",
    message="Could not import the file.",
    detail="The file format was not recognized.",
    icon="error",
    buttons=("OK",),
)
```

#### Parent / positioning (if supported)

Pass a parent to keep the dialog on top of the correct window.

```python
ttk.MessageBox.ok(parent=app, title="Saved", message="Done.")
```

### Value model

Message boxes return a **single committed choice** (or no value if dismissed):

- OK-only dialogs - no decision, just acknowledgement

- Yes/No, OK/Cancel - one decision

- Retry/Cancel - one decision for error recovery

Return values vary by implementation (bool, string token, enum). Treat the result as your source of truth.

---

## Behavior

- Opens as **modal** (blocks interaction until dismissed)

- Escape typically cancels (when cancel is available)

- Enter typically activates the default action (OK/Yes)

Keep messages short, actionable, and avoid putting long text in the main message line.

---

## Additional resources

### Related widgets

- [Toast](../overlays/toast.md) - non-blocking notifications

- [Tooltip](../overlays/tooltip.md) - contextual help

- [MessageDialog](messagedialog.md) - alternative message dialog

- [DateDialog](datedialog.md) - modal date selection dialog

### API reference

!!! link "API Reference"
    `ttkbootstrap.MessageBox`