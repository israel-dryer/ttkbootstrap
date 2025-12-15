---
title: DateDialog
icon: fontawesome/solid/calendar-days
---

# DateDialog

`DateDialog` is a lightweight date-picker dialog built around `DatePicker`. It can run as a classic **modal dialog** or as a **chrome-less popover** (optional) that closes when the user clicks outside. It’s designed for quick, ergonomic date selection without building a full form dialog.

<!--
IMAGE: DateDialog modal
Suggested: Modal DateDialog centered over app with a visible title bar and calendar
Theme variants: light / dark
-->

<!--
IMAGE: DateDialog popover
Suggested: Chrome-less DateDialog anchored to a DateEntry / button, auto-flipped near screen edge
Theme variants: light / dark
-->

---

## Basic usage

Show a modal date dialog and read the selected value:

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.DateDialog(app, title="Choose a date")
dlg.show()

print("Selected:", dlg.result)  # datetime.date or None
app.mainloop()
```

Anchor the dialog near a button (popover-style positioning):

```python
import ttkbootstrap as ttk

app = ttk.App()

btn = ttk.Button(app, text="Pick date")
btn.pack(padx=20, pady=20)

dlg = ttk.DateDialog(app, title=" ", close_on_click_outside=True, hide_window_chrome=True)

def open_dialog():
    dlg.show(anchor_to=btn, anchor_point="sw", window_point="nw", offset=(0, 6), auto_flip=True)
    print("Selected:", dlg.result)

btn.configure(command=open_dialog)

app.mainloop()
```

---

## What problem it solves

Date picking is common, but building a full dialog for it is repetitive. `DateDialog` provides:

- A ready-to-use date picker surface with sensible defaults
- Optional popover behavior (close on outside click)
- Optional chrome-less presentation (no OS window decorations)
- Forwarded `DatePicker` options (bounds, disabled dates, week numbers, etc.)
- Smart positioning and auto-flip to keep the dialog on-screen

This is ideal for “pick a date and continue” flows.

---

## Core concepts

### Modal vs popover behavior

`DateDialog` uses two modes:

- **Modal** (default): blocks until the dialog closes.
- **Popover**: closes when the user clicks outside, great for anchored pickers.

Enable popover-style behavior with:

- `close_on_click_outside=True` (uses popover mode internally)
- optionally `hide_window_chrome=True` for a clean, dropdown-like look

```python
ttk.DateDialog(app, close_on_click_outside=True, hide_window_chrome=True)
```

!!! tip "Popover date picker"
    Use popover mode when the date picker feels like an extension of a field (e.g., a DateEntry trigger), not a separate task.

---

### Selecting vs resetting

The dialog closes and produces a result only when the user **selects** a date. Internal “reset” actions do not close the dialog.

This makes the dialog feel safe: only an explicit date selection commits and closes.

---

### Result value

After `.show()`, the selected date is available as:

```python
selected = dlg.result  # datetime.date or None
```

- `datetime.date` when a date was selected
- `None` if cancelled or closed without selecting

---

## Options you’ll commonly use

### Initial date

```python
from datetime import date
dlg = ttk.DateDialog(app, initial_date=date(2025, 1, 1))
```

### Week start (first_weekday)

```python
dlg = ttk.DateDialog(app, first_weekday=0)  # Monday
dlg = ttk.DateDialog(app, first_weekday=6)  # Sunday (default)
```

### Bounds and disabled dates

Limit selectable dates:

```python
dlg = ttk.DateDialog(app, min_date="2025-01-01", max_date="2025-12-31")
```

Disable specific dates:

```python
from datetime import date

dlg = ttk.DateDialog(app, disabled_dates=[date(2025, 12, 25)])
```

### Week numbers and outside days

```python
dlg = ttk.DateDialog(app, show_week_numbers=True, show_outside_days=True)
```

---

## Positioning

You can position the dialog in two ways when calling `show(...)`:

### Explicit coordinates

```python
dlg.show(position=(400, 250))
```

### Anchor-based positioning

```python
dlg.show(
    anchor_to="cursor",         # or a widget, "screen", "parent"
    anchor_point="sw",          # point on the anchor target
    window_point="nw",          # point on the dialog window
    offset=(8, 8),
    auto_flip=True,
)
```

Auto-flip is useful when the dialog is near the edge of the screen.

<!--
IMAGE: Auto-flip near edges
Suggested: DateDialog opening upward when near bottom edge
-->

---

## Events

### `on_result`

You can subscribe to results using `on_result(...)`, which fires a `<<DialogResult>>` virtual event when a date is selected.

```python
import ttkbootstrap as ttk

app = ttk.App()

dlg = ttk.DateDialog(app)

def on_date(d: object):
    print("Result event:", d)

dlg.on_result(on_date)

dlg.show()
app.mainloop()
```

To unbind, keep the returned `funcid`:

```python
funcid = dlg.on_result(on_date)
dlg.off_result(funcid)
```

!!! note "Event payload"
    `on_result(...)` receives the dialog result payload (a `datetime.date`), and the generated virtual event includes a data dict containing `result` and `confirmed`.

---

## UX guidance

- Use a **popover DateDialog** for “field-like” pickers
- Use a **modal DateDialog** when date selection is its own step
- Keep `title=" "` for popovers to avoid drawing attention to window chrome

!!! tip "Anchor to the trigger"
    For best UX, anchor the dialog to the button/field that opened it, and enable `auto_flip=True` so it stays on screen.

---

## When to use / when not to

**Use DateDialog when:**

- You need quick date selection without building a full dialog
- A date picker should feel like an extension of a field
- You want optional chrome-less popover behavior

**Avoid DateDialog when:**

- You need multiple fields and validation (use `Dialog` + form content, or a dedicated FormDialog)
- Date selection is part of a large wizard step (consider embedding `DatePicker` directly on a page)
- You need time selection as well (use a dedicated time dialog/control)

---

## Related widgets

- **DatePicker** — the embedded calendar control
- **DateEntry** — form-ready date input (often used with DateDialog)
- **Dialog** — generic dialog builder for complex flows
