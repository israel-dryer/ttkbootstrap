---
title: Dialog
---

# Dialog

`Dialog` is the base class for building **modal** and **popover** dialogs in ttkbootstrap.

Use dialogs when you need users to **make a decision** or **provide input** before continuing.

---

## Quick start

Most dialogs follow a pattern like this:

```python
import ttkbootstrap as ttk

app = ttk.App()

dialog = ttk.Dialog(
    title="Dialog title",
    message="Explain what the user needs to do.",
)
result = dialog.show()

print("result:", result)
app.mainloop()
```

---

## When to use

Use `Dialog` (or a specialized dialog) when:

- the user must confirm an action

- the user must provide input before continuing

- the flow benefits from an explicit OK/Cancel outcome

### Consider a different control when...

- feedback should not block workflow - use [Toast](../overlays/toast.md) or [Tooltip](../overlays/tooltip.md) instead

---

## Presentation modes

### Modal (default)

Modal dialogs block interaction with the parent window until closed.

Use modal when the user must respond immediately (confirmations, required input).

### Popover

Popover dialogs are lightweight and typically close when focus is lost.

Use popover when the dialog is contextual and low-risk (quick filters, small pickers).

---

## Examples & patterns

### Common options

- `title` - window title

- `message` - primary content text (keep short)

- `parent` - parent window for stacking and focus

- `buttons` - the actions shown (OK/Cancel, Yes/No, etc.)

- `default` - default action activated by Enter (if supported)

### Value model

Dialogs produce a **single committed outcome**:

- a result value (string/bool/object), or

- `None` when cancelled/dismissed

---

## Behavior

- **Enter** typically activates the default action.

- **Escape** typically cancels (when cancel is available).

- Closing the window via the title bar is treated like cancel/dismiss.

---

## Additional resources

### Related widgets

- [MessageBox](messagebox.md) - prebuilt confirmation / alert dialogs

- [QueryBox](querybox.md) - prompt for a single value

- [FormDialog](formdialog.md) - prompt for structured multi-field input

- [FilterDialog](filterdialog.md) - choose filters with confirm/cancel

- [Toast](../overlays/toast.md) - non-blocking notification

- [Tooltip](../overlays/tooltip.md) - contextual hover help

### API reference

- [`ttkbootstrap.Dialog`](../../reference/dialogs/Dialog.md)