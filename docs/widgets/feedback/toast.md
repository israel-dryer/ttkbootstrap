---
title: Toast
icon: fontawesome/solid/bell
---

# Toast

`Toast` displays a small, transient notification in a corner of the screen. Toasts are ideal for **non-blocking feedback** such as confirmations, status updates, or lightweight prompts that should not interrupt the user’s workflow.

<!--
IMAGE: Toast notification examples
Suggested: Success toast (auto-dismiss), warning toast with close button, toast with action buttons
Theme variants: light / dark
-->

---

## Basic usage

Show a simple toast with a message:

```python
import ttkbootstrap as ttk

app = ttk.App()

toast = ttk.Toast(message="Settings saved")
toast.show()

app.mainloop()
```

Create a toast that auto-dismisses after a duration:

```python
toast = ttk.Toast(
    title="Success",
    message="Your changes have been saved.",
    duration=3000,
    bootstyle="success",
)
toast.show()
```

<!--
IMAGE: Basic Toast example
Suggested: Bottom-right toast with title + message
-->

---

## What problem it solves

Applications often need to communicate feedback without stopping the user or requiring interaction. `Toast` solves this by:

- Displaying temporary, non-modal notifications
- Automatically dismissing after a duration (optional)
- Supporting icons, metadata, and action buttons
- Appearing above other windows without stealing focus

Unlike dialogs, toasts are **informational first** and should not block progress.

---

## Core concepts

### Title vs message

A toast can display either or both:

- **Title only** — shown prominently using a label-style font
- **Message only** — shown in the header when no title is provided
- **Title + message** — title appears in the header, message appears below

```python
ttk.Toast(title="Update complete")
ttk.Toast(message="File uploaded")
ttk.Toast(title="Warning", message="Low disk space")
```

---

### Icons

Icons appear in the header and can be provided as:

- a string icon name
- a detailed icon spec (`name`, `size`, `color`)

```python
ttk.Toast(
    title="Info",
    message="New version available",
    icon="info-circle",
)
```

```python
ttk.Toast(
    title="Alert",
    message="Connection lost",
    icon={"name": "wifi-off", "color": "danger"},
)
```

<!--
IMAGE: Toast icon variants
Suggested: Toasts with different icons and semantic colors
-->

---

### Auto-dismiss vs persistent

Control whether a toast closes automatically using `duration` (milliseconds):

```python
# Auto-dismiss
ttk.Toast(message="Saved", duration=2000)

# Persistent until closed
ttk.Toast(message="Waiting for input")
```

Persistent toasts can still be dismissed via the close button or action buttons.

---

### Action buttons

Toasts may include one or more action buttons. Each button is defined using standard ttkbootstrap button options.

```python
def on_dismissed(data):
    if data and data.get("text") == "Retry":
        print("Retry clicked")

toast = ttk.Toast(
    title="Upload failed",
    message="Check your connection.",
    buttons=[
        {"text": "Retry", "bootstyle": "primary"},
        {"text": "Dismiss", "bootstyle": "secondary"},
    ],
    on_dismissed=on_dismissed,
)
toast.show()
```

When a button is clicked:
- the toast closes
- `on_dismissed` is called with the button’s option dict

<!--
IMAGE: Toast with buttons
Suggested: Toast showing two action buttons beneath the message
-->

---

## Positioning

By default, toasts appear in a platform-appropriate screen corner:

- **Windows / macOS**: bottom-right
- **X11**: top-right

You can override the position using a geometry string:

```python
ttk.Toast(message="Custom position", position="-25-75")
```

This uses standard Tk geometry semantics.

---

## Events and lifecycle

### Dismissal callback

Use `on_dismissed` to react when a toast is closed:

```python
def on_dismissed(data):
    print("Toast dismissed:", data)

toast = ttk.Toast(message="Done", on_dismissed=on_dismissed)
toast.show()
```

The callback receives:
- the button option dict (if dismissed via a button)
- `None` if dismissed via close button or auto-dismiss

---

## UX guidance

- Use toasts for **feedback**, not decisions
- Keep text short and scannable
- Prefer semantic `bootstyle` values (`success`, `warning`, `danger`)
- Avoid stacking too many toasts at once

!!! tip "Non-blocking feedback"
    If the user must acknowledge or decide, use a Dialog instead of a Toast.

---

## When to use / when not to

**Use Toast when:**

- You want to confirm an action without interrupting
- Feedback should disappear automatically
- The message is informative, not critical

**Avoid Toast when:**

- A response is required (use Dialogs)
- The message is long or complex
- The information must remain visible

---

## Related widgets

- **Dialog** — modal, blocking user decisions
- **Tooltip** — contextual, hover-based hints
- **DropdownButton** — often paired with toast-triggering actions
