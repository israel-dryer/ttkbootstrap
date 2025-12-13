---
title: Toast
icon: fontawesome/solid/bell
---


# Toast

`Toast` delivers frameless, themed notifications that appear in a corner of the screen, show a title/message/icon, and optionally auto-dismiss or fire callbacks.

---

## Overview

Key features:

- Titles, messages, memo text, and icons show in a structured header/body layout.
- Buttons let you attach actions; their commands trigger `on_dismissed` before the toast closes.
- `duration` auto-dismisses the toast after the given milliseconds; omit it to keep the toast open.
- `bootstyle` and `surface_color` control the toast background while `position` lets you override corner placement; defaults adapt to Windows/macOS/Linux.
- `alert=True` plays a bell sound; `show_close_button` toggles the header “x” control.

Use `Toast` for transient feedback such as saves, errors, confirmations, or background task updates without needing a dialog.

---

## Quick example

```python
import ttkbootstrap as ttk

app = ttk.App(theme="cosmo")

ttk.Button(
    app,
    text="Show toast",
    command=lambda: ttk.Toast(
        title="Upload complete",
        message="Your file is now available.",
        bootstyle="success",
        icon="cloud-check",
        duration=2500,
    ).show()
).pack(padx=20, pady=40)

app.mainloop()
```

---

## Buttons, positioning & callbacks

- Supply a `buttons` list where each dict accepts button options (`text`, `bootstyle`, `command`, etc.); the toast closes after each button and `on_dismissed` receives the button dict.
- Override default auto-placement (`-25-75`) via `position` or pass a geometry string; legacy corner strings continue to work.
- Call `show(merge=False, ...)` to replace options per display, or reuse the toast instance with `configure()`/`show()`.
- Control dismissal through the close icon (`show_close_button=False` hides it) or by calling `hide()`/`destroy()` yourself.

---

## When to use Toast

Choose `Toast` for ephemeral, non-blocking notifications that should not interrupt the workflow, especially for confirmations, alerts, or background job updates. Pair with `ToolTip` for inline guidance or `Dialogs` for heavier interactions.

---

## Related widgets

- **Dialogs** (blocking confirmations)
- **Tooltip**

