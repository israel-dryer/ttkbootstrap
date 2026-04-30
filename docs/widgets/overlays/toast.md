---
title: Toast
---

# Toast

`Toast` is a **non-blocking notification overlay** used to show brief feedback without interrupting the workflow.

Use Toast for messages like "Saved", "Copied", or "Connected". Toasts should disappear automatically and should not require user action.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Toast(
    title="Saved",
    message="Your changes were saved successfully.",
).show()

app.mainloop()
```

---

## When to use

Use Toast when:

- feedback is helpful but not critical

- the user should not be interrupted

### Consider a different control when...

- the user must confirm or decide something — use [MessageBox](../dialogs/messagebox.md)

- the feedback is tied to a specific control (validation, helper text) — use inline messaging

---

## Appearance

### Variants

Toast supports different visual intents through the `accent` parameter:

- `info` — general information
- `success` — positive confirmation
- `warning` — caution notices
- `danger` — error or critical messages

!!! link "Design System"
    See the [Colors & Styling](../../design-system/colors.md) guide for complete color options.

---

## Examples & patterns

### Common options

- `title` — the toast heading

- `message` — the body text

- `duration` — auto-hide delay in milliseconds

- `accent` / intent — info, success, warning, danger

---

## Behavior

- Non-modal (does not block)

- Auto-dismiss after a short duration (typically configurable)

- Usually stacks if multiple toasts are shown

- Click-to-dismiss is common (if supported)

!!! note "Default position by platform"
    When `position` is not set, Toast anchors to the platform notification convention:

    - **macOS / Windows** — bottom-right corner (inset 25 px right, 75 px bottom)
    - **Linux (X11)** — top-right corner (inset 25 px right, 25 px top)

    Pass `position` explicitly to override: `Toast(message="Done", position="-25-75")`

---

## Additional resources

### Related widgets

- [Tooltip](./tooltip.md) — contextual hover help

- [MessageBox](../dialogs/messagebox.md) — modal alerts and confirmations

### Framework concepts

- [Overlays](./index.md) — overview of overlay widgets

### API reference

- [`ttkbootstrap.Toast`](../../reference/widgets/Toast.md)