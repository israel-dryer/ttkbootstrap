---
title: ColorDropper
icon: fontawesome/solid/eye-dropper
---

# ColorDropper

`ColorDropper` (implemented as `ColorDropperDialog`) is a screen color picker that lets users select a color from **any pixel on the screen**. When shown, it takes a screenshot, displays a full-screen overlay, and provides a zoomed preview near the cursor for precise selection. 

> **Interaction**
> - **Left-click** anywhere to pick a color and close
> - **Right-click** or **Escape** to cancel
> - **Mouse wheel** zooms the preview

<!--
IMAGE: ColorDropper in action
Suggested: Full-screen screenshot overlay with the magnifier window near the cursor
Theme variants: light / dark (note: screenshot content itself varies)
-->

---

## Basic usage

Show the dropper and read the selected color:

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colordropper import ColorDropperDialog

app = ttk.App()

dropper = ColorDropperDialog()
dropper.show()

choice = dropper.result.get()
if choice:
    print(choice.hex)   # "#RRGGBB"
    print(choice.rgb)   # (r, g, b)
    print(choice.hsl)   # (h, s, l)

app.mainloop()
```

<!--
IMAGE: Result output
Suggested: A small UI showing selected color swatch + hex + rgb + hsl
-->

---

## What problem it solves

Picking colors often requires sampling an exact pixel (brand colors, screenshots, UI inspection). A standard color chooser is great for browsing, but it’s not great at “match this exact color”.

`ColorDropperDialog` solves that by sampling directly from the screen and returning a structured color choice. 

---

## Core concepts

### Result type

The selected value is stored in `result` as a `ColorChoice`:

- `rgb`: `(r, g, b)` tuple
- `hsl`: `(h, s, l)` tuple
- `hex`: `"#RRGGBB"` string

```python
choice = dropper.result.get()
# choice.rgb, choice.hsl, choice.hex
```

If the user cancels, `result` is set to `None`. 

---

### Zoom preview

A small “magnifier” window follows the cursor and shows a zoomed view of pixels under the pointer. The mouse wheel adjusts `zoom_level`, allowing precise targeting. 

<!--
IMAGE: Zoom levels
Suggested: Two screenshots showing different zoom levels (wheel up vs wheel down)
-->

---

## Platform notes

- **Windows and Linux** are supported.
- **macOS is not supported** due to `PIL.ImageGrab` limitations for this workflow. 

!!! tip "High DPI displays"
    On high-DPI displays, make sure your app runs in high-DPI mode so the screenshot and pointer coordinates match cleanly. 

---

## Events

`ColorDropperDialog` emits a `<<DialogResult>>` event exactly once per show cycle (confirmed or cancelled). 

### `on_dialog_result(...)`

Use `on_dialog_result` to react when a selection is made (or cancelled):

```python
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.colordropper import ColorDropperDialog

app = ttk.App()

dropper = ColorDropperDialog()

def on_result(payload):
    # payload: {"result": ColorChoice|None, "confirmed": bool}
    print(payload)

dropper.show()
funcid = dropper.on_dialog_result(on_result)

app.mainloop()
```

To unbind later:

```python
dropper.off_dialog_result(funcid)
```

### Event payload

The event `data` payload includes:

- `result`: the `ColorChoice` (or `None`)
- `confirmed`: `True` if a color was chosen, `False` if cancelled

---

## UX guidance

- Use the color dropper when “match this pixel” is the primary goal.
- Provide a **fallback** (like a traditional color chooser) for users who want to browse colors.
- Consider showing the selected color as a swatch with hex/rgb fields so it’s easy to copy.

!!! tip "Keep it discoverable"
    Label the trigger clearly (“Pick from screen…”) and show a short hint about click/escape behavior near the control.

---

## When to use / when not to

**Use ColorDropper when:**

- Users need to sample colors from screenshots, images, or other apps
- Precision matters more than browsing
- You want hex/rgb/hsl output in a single step

**Avoid ColorDropper when:**

- You need macOS support (use a standard color chooser)
- Users primarily want to browse palettes (use `ColorChooserDialog` / color picker widgets)

---

## Related widgets

- **ColorChooserDialog** — browse/select colors from a palette UI
- **QueryBox.get_color(...)** — one-line API for color selection
- **Toast** — great for “Copied #RRGGBB” confirmation after selection
