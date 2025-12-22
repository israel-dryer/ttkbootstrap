---
title: Toast
---

# Toast

`Toast` is a **non-blocking notification overlay** used to show brief feedback without interrupting the workflow.

Use Toast for messages like “Saved”, “Copied”, or “Connected”. Toasts should disappear automatically and should not require user action.

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Toast(
    app,
    title="Saved",
    message="Your changes were saved successfully.",
).show()

app.mainloop()
```

---

## Behavior

- Non-modal (does not block)
- Auto-dismiss after a short duration (typically configurable)
- Usually stacks if multiple toasts are shown
- Click-to-dismiss is common (if supported)

---

## Common options

- `title`
- `message`
- `duration` (auto-hide delay)
- `bootstyle` / intent (info/success/warning/error)

---

## When should I use Toast?

Use Toast when:

- feedback is helpful but not critical
- the user should not be interrupted

Prefer **MessageBox** when:

- the user must confirm or decide something

Prefer inline messaging when:

- the feedback is tied to a specific control (validation, helper text)

---

## Related widgets

- **Tooltip** — contextual hover help
- **MessageBox** — modal alerts and confirmations

---

## Reference

- **API Reference:** `ttkbootstrap.Toast`
