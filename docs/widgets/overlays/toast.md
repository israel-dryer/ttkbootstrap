---
title: Toast
---

# Toast

`Toast` is a **non-blocking notification overlay** that displays a
brief message in a chromeless `Toplevel` anchored to a screen corner.
Use it for confirmations ("Saved", "Copied"), status changes
("Connected"), and other transient feedback that should not interrupt
the workflow. A toast can auto-dismiss after a duration, sit until
the user closes it, or offer custom action buttons.

`Toast` is **not a widget**. It's a controller object with no parent,
no `winfo_*` surface, and no place in the geometry tree. Its public
shape is `__init__` plus `show()` / `hide()` / `destroy()` /
`configure()` / `cget()`. Each call to `show()` builds a fresh
`Toplevel`; the same instance can be reshown after `hide()` to display
the same notification again.

---

## Basic usage

Construct a Toast and call `show()` to display it. Pass `duration`
(in milliseconds) to auto-dismiss:

```python
import ttkbootstrap as ttk

app = ttk.App()

ttk.Button(
    app,
    text="Save",
    command=lambda: ttk.Toast(
        title="Saved",
        message="Your changes were saved successfully.",
        duration=3000,
    ).show(),
).pack(padx=20, pady=20)

app.mainloop()
```

The instance can be discarded — `show()` parents the `Toplevel` to
the application root, and the `duration` timer destroys it when it
expires. Keep a reference only if you want to call `hide()` /
`destroy()` manually or reshow the same toast later.

---

## Lifecycle

A toast's life starts at `show()` and ends at `hide()`, `destroy()`,
or auto-dismissal:

- **Trigger** — `show()` builds a chromeless `Toplevel`, lays out the
  content, computes the screen position, and `deiconify`s the window.
  There is no hover trigger or pointer-driven appearance — every show
  is programmatic.
- **Visibility** — the toast stays on screen until either the
  `duration` timer fires (`top.after(duration, self.hide)`), the user
  clicks the close button, the user invokes a custom button, or
  `hide()` / `destroy()` is called from code.
- **Dismissal** — `hide()` destroys the `Toplevel` and invokes
  `on_dismissed(None)`. Custom-button clicks invoke the button's own
  `command` first, then `on_dismissed(button_options_dict)`, then
  destroy the `Toplevel`. Auto-dismissal goes through `hide()`.
- **Reusable** — a single Toast instance can be shown, dismissed, and
  shown again. The controller object survives; only the `Toplevel` is
  rebuilt each time. Mutate options between shows via `configure(...)`
  or pass them to `show(**options)`.
- **Non-blocking** — toasts never steal focus or capture input. They
  set `topmost=True` so they float above the application, but other
  windows remain interactive.

```python
import ttkbootstrap as ttk

app = ttk.App()

# A reusable toast — same instance, shown twice.
toast = ttk.Toast(title="Status", duration=2000)

ttk.Button(app, text="Connected",
           command=lambda: toast.show(message="Server reachable",
                                      accent="success")).pack(padx=20, pady=10)
ttk.Button(app, text="Failed",
           command=lambda: toast.show(message="Connection refused",
                                      accent="danger")).pack(padx=20, pady=10)

app.mainloop()
```

!!! warning "Don't call `show()` again before the previous toast dismisses"
    Calling `show()` twice on the same instance while the first
    `Toplevel` is still on screen leaks the first window — `_toplevel`
    is overwritten and the previous `Toplevel` stays mapped until the
    application exits. Either let the previous toast finish (set a
    `duration` and time the second call after it) or call `hide()`
    explicitly before the second `show()`.

---

## Common options

| Option | Default | Effect |
|---|---|---|
| `title` | `None` | Header text. With no `message`, rendered in the larger `"label"` font; with a `message`, rendered as a header above the message body. |
| `message` | `None` | Body text. With no `title`, rendered in the header in `"body"` font; with a `title`, rendered as a separate section below the header (separator added). |
| `icon` | `None` | Icon shown to the left of the title. String name (`"check-lg"`) or `IconSpec` dict (`{"name": str, "size": int, "color": str}`). The `color` key accepts only PIL color names / hex — theme tokens like `"success"` raise. |
| `memo` | `None` | Small metadata text on the right of the header (e.g. `"5 mins ago"`). Renders in `"caption"` font with muted foreground. |
| `duration` | `None` | Auto-dismiss delay in milliseconds. `None` keeps the toast visible until manually closed. |
| `buttons` | `None` | Sequence of button option dicts. Each dict is passed to `ttk.Button(...)`; recognized keys include `text`, `icon`, `accent`, `variant`, plus a special `command`. See *Buttons*. |
| `show_close_button` | `True` | Renders an X close button in the header. The button calls `hide()` and fires `on_dismissed(None)`. |
| `accent` | `None` | Theme token for the toast container. Tints the background and drives the muted close-button / memo color via `"<accent>[muted]"`. |
| `bootstyle` | `None` | DEPRECATED — use `accent`. Construction-time only; `configure(bootstyle=...)` is silently a no-op for styling. |
| `position` | `None` | Tk geometry string (`"+x+y"` or `"-x-y"`). Overrides the platform default. |
| `alert` | `False` | If `True`, rings the system bell (`top.bell()`) when the toast is shown. |
| `on_dismissed` | `None` | Callback invoked when the toast goes away. Payload depends on dismissal path. See *Events*. |

The container is a `ttk.Frame` with `accent=self._accent` —
`accent="success"` tints the toast green, `accent="danger"` tints it
red, and so on. The header internally uses `b.<accent>[muted]` for
the close-button glyph and the memo text, so muted colors track the
chosen accent.

### Buttons

Each entry in `buttons=` is a dict passed to `ttk.Button(...)` after
removing the `command` key. The wrapper substitutes its own command:

```python
import ttkbootstrap as ttk

app = ttk.App()

def confirm_save():
    print("saved!")

def offer_save():
    ttk.Toast(
        title="Unsaved changes",
        message="Save before closing?",
        buttons=[
            {"text": "Save", "command": confirm_save, "accent": "primary"},
            {"text": "Discard", "accent": "danger", "variant": "outline"},
        ],
    ).show()

ttk.Button(app, text="Close", command=offer_save).pack(padx=20, pady=20)

app.mainloop()
```

When a button is clicked, the wrapper invokes the button's own
`command` (if any), then `on_dismissed(button_options_dict)`, then
destroys the `Toplevel`. The button options dict is the **original
dict including the `command` callable** — see *Events* for the
implications.

---

## Behavior

### Default position by platform

When `position` is not set, Toast anchors to the platform notification
convention via `WindowPositioning.position_anchored`:

- **macOS / Windows** — bottom-right corner, inset 25 px right and
  75 px from the bottom (`anchor_point="se"`, `offset=(-25, -75)`).
- **Linux (X11)** — top-right corner, inset 25 px right and 25 px
  from the top (`anchor_point="ne"`, `offset=(-25, 25)`).

`ensure_visible=True` keeps the toast on screen on multi-monitor
configurations. To override:

```python
ttk.Toast(message="Done", position="-25-25").show()  # bottom-right, 25,25
ttk.Toast(message="Done", position="+0+0").show()    # top-left
```

The string is a Tk geometry fragment — the leading sign is required
(`+x+y` for top/left offsets, `-x-y` for right/bottom offsets).

### Window flags

The internal `Toplevel` is created with:

- `overrideredirect=True` — chromeless on Win/Linux. On macOS (Aqua),
  `overrideredirect` is silently skipped per the framework's
  `BaseWindow` guard, so the chromeless effect comes from
  `windowtype="tooltip"` (which applies `MacWindowStyle "help none"`).
- `topmost=True` — floats above other application windows.
- `alpha=0.97` — slight transparency for visual softness.

These are not configurable from the constructor.

### `show(merge=...)` semantics

`show()` accepts the same keyword options as `__init__`. By default it
**merges** them with the existing instance config (`merge=True`):

```python
toast = ttk.Toast(title="Status", accent="primary")
toast.show(message="Connected")  # title="Status", accent="primary", message="Connected"
```

Pass `merge=False` to clear the instance config first. After
`show(merge=False)`, every option not passed to that call resets to
its default — including `accent`, `duration`, `buttons`, etc.:

```python
toast = ttk.Toast(title="A", message="x", accent="success", duration=2000)
toast.show(merge=False, message="Y")  # title=None, accent=None, duration=None, message="Y"
```

### Reconfiguring before re-show

`configure(...)` mutates the instance config but does **not** affect
a currently-visible `Toplevel`. To change the displayed toast, call
`hide()` first, then `configure(...)`, then `show()`:

```python
toast = ttk.Toast(title="Loading…", duration=None)
toast.show()
# ... background work ...
toast.hide()
toast.configure(title="Done!", duration=2000)
toast.show()
```

`configure(bootstyle=...)` post-construction stores the value but
does **not** update `_accent`, so the next `show()` paints with the
original styling. Pass `accent` instead.

### Stacking

Multiple Toast instances can coexist — each owns an independent
`Toplevel`. They will overlap if positioned identically (the
framework does not currently shift later toasts to clear the stack).
For ordered notifications, queue them yourself: only call the next
`show()` when the previous toast's `on_dismissed` callback fires.

```python
import ttkbootstrap as ttk

app = ttk.App()

queue = ["Saved", "Synced", "Done"]

def show_next(_data=None):
    if not queue:
        return
    msg = queue.pop(0)
    ttk.Toast(message=msg, duration=1500, on_dismissed=show_next).show()

ttk.Button(app, text="Run", command=show_next).pack(padx=20, pady=20)

app.mainloop()
```

---

## Events

Toast has **no virtual events**. The only hook is the `on_dismissed`
callback registered on the constructor (or via `configure(on_dismissed=...)`).

The callback fires once per dismissal with a payload that depends on
how the toast was closed:

| Dismissal path | Payload |
|---|---|
| Auto-dismiss (`duration` timer fires) | `None` |
| Close button (`show_close_button=True`) | `None` |
| Programmatic `hide()` | `None` |
| Custom button click | The full button options dict — same `dict` instance the caller supplied in `buttons=`, **including the `command` callable** |
| Programmatic `destroy()` | Not invoked — `destroy()` skips the callback |

The button-options-dict payload is unusual: a caller routing on which
button was pressed must read `data["text"]` (or whatever marker key
the caller chose to embed). The dict still contains the `command`
reference under `data["command"]`, so be careful if you serialize or
log the payload.

```python
import ttkbootstrap as ttk

app = ttk.App()

def handle_dismiss(data):
    if data is None:
        print("auto-dismissed or closed")
    else:
        print(f"button clicked: {data['text']}")

def offer_action():
    ttk.Toast(
        title="Update available",
        buttons=[
            {"text": "Install", "accent": "primary"},
            {"text": "Later", "variant": "outline"},
        ],
        on_dismissed=handle_dismiss,
    ).show()

ttk.Button(app, text="Check", command=offer_action).pack(padx=20, pady=20)

app.mainloop()
```

If you need to detect "shown" or "visible-now" events, there's no
hook — the `Toplevel` is exposed as `toast._toplevel` after `show()`
but it's a private attribute, and binding `<Map>` / `<Unmap>` on it
only works between `show()` and the dismissal you're trying to
observe.

---

## When should I use Toast?

Use Toast when:

- the message is feedback ("Saved", "Copied", "Connected"), not a
  decision — auto-dismissal is fine
- the user shouldn't be interrupted but should be informed
- the notification is independent of the focused control (otherwise
  inline messaging is closer to the action)

Prefer ToolTip when:

- the hint is contextual to a specific control and should appear on
  hover, not programmatically

Prefer a Dialog (e.g. `MessageBox.show_info`, `MessageBox.show_question`)
when:

- the user must acknowledge or decide something before continuing —
  toasts can be missed
- the content is more than one short paragraph or includes a form

Prefer inline help text or validation messaging when:

- the feedback is tied to a specific field and should persist while
  the field is focused

---

## Related widgets

- **ToolTip** — hover-only contextual hint; non-blocking and
  pointer-driven
- **MessageBox** — modal alert / confirmation dialog
- **Label** — inline status text alongside a control

---

## Reference

- **API reference:** `ttkbootstrap.Toast`
- **Related guides:** Feedback, UX Patterns, Design System
