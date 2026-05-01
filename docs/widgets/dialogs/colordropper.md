---
title: ColorDropper
---

# ColorDropper

`ColorDropperDialog` is a **fullscreen screen-pixel sampler**. On
`show()` it grabs a screenshot of the entire desktop, paints it
into a fullscreen toplevel, and floats a small zoom-magnifier next
to the cursor showing the pixels under the pointer at 50× scale. A
left-click captures the pixel under the crosshair and closes the
sampler; a right-click or Escape closes without capturing.

It's the same widget that powers the eyedropper button on
[`ColorChooserDialog`](colorchooser.md) (Windows/Linux only). Used
standalone, it's the right shape for a workflow whose entire job is
"grab a color from somewhere on screen" — a paint app's pipette
tool, a theme editor sampling a logo, a scripting helper that needs
RGB values for whatever the user is pointing at.

The page slug is `ColorDropper`; the actual class is
`ttk.ColorDropperDialog`. There is no inline (non-modal) variant —
the dialog *is* the only form. The dialog is **not supported on
macOS**: it relies on PIL's `ImageGrab.grab()`, which has no aqua
implementation, so a `ColorDropperDialog` constructed on macOS
won't be able to populate its screenshot canvas.

---

## Basic usage

Construct, register a callback, then `show()`. Reading the result
directly after `show()` does **not** work the way it does on the
other dialogs in this section — see the callout below.

```python
import ttkbootstrap as ttk

app = ttk.App()

def picked(payload):
    if payload["confirmed"]:
        choice = payload["result"]
        print("hex:", choice.hex)
        print("rgb:", choice.rgb)
        print("hsl:", choice.hsl)

dlg = ttk.ColorDropperDialog()
dlg.show()                      # non-blocking — returns immediately
dlg.on_dialog_result(picked)    # register AFTER show() — see note

app.mainloop()
```

!!! note "`show()` is non-blocking on `ColorDropperDialog`"
    Unlike `ColorChooserDialog`, `MessageDialog`, `QueryDialog`,
    etc., `ColorDropperDialog.show()` does **not** call
    `wait_window()` — it sets up the bindings and returns
    immediately. To respond to the captured color either register
    an `on_dialog_result` callback, trace the underlying
    `result` Variable, or call `app.wait_variable(dlg.result)`
    yourself before reading.

If you want a synchronous one-shot helper, [`querybox.get_color`](querybox.md)
wraps `ColorChooserDialog` (which embeds the dropper) and does
block — most apps don't need to drive `ColorDropperDialog`
directly.

---

## Result value

`dlg.result` is a `tkinter.Variable`, not a plain attribute. The
captured value lives **inside** the Variable, so reads go through
`.get()`:

```python
dlg.result.get()  # ColorChoice(rgb=(r, g, b), hsl=(h, s, l), hex='#rrggbb')
                  # or None
```

On a successful left-click the Variable is set to a `ColorChoice`
namedtuple — the same `(rgb, hsl, hex)` shape produced by
[`ColorChooserDialog`](colorchooser.md), so callers can swap the
two without changing how they read the result. On any cancel path
(right-click, Escape, window-close), the Variable is set to
`None`.

The Variable is intentionally exposed: it makes the result
**reactive**. `ColorChooserDialog` itself uses
`dlg.result.trace_add('write', handler)` internally to mirror the
sampled pixel into its hex spinbox in real time — pattern that
applies whenever you want to react to the captured color without
waiting for an event:

```python
def mirror(*_):
    value = dlg.result.get()
    if value is not None:
        accent_var.set(value.hex)

dlg.result.trace_add('write', mirror)
dlg.show()
```

---

## Common options

`ColorDropperDialog.__init__()` takes **no arguments** — there is
no `title`, no `master`, no `initial_color`, no theme
configuration, no buttons override. The dialog is a fixed
fullscreen tool. Call it as `ttk.ColorDropperDialog()` and rely on
the runtime's `Toplevel` to inherit the application's root
window for the transient relationship.

If you need configurable options (a parent for the screen grab, a
custom title, a non-fullscreen mode), reach for
[`ColorChooserDialog`](colorchooser.md) — its eyedropper button
embeds this same widget, but the chooser handles parenting,
positioning, and confirmation flow.

---

## Behavior

### Activation and dismissal

`show()` performs four steps:

1. Builds a fullscreen `Toplevel` with `-fullscreen True` and an
   alpha of 1.
2. Calls `PIL.ImageGrab.grab()` to capture the current desktop and
   paints it onto a canvas inside that toplevel.
3. Builds a 100×100 zoom toplevel that follows the cursor with a
   `+` crosshair and a magnified view of the pixels under it.
4. Calls `grab_set()` so the dialog is modal *during* the picking
   interaction, then returns.

The screenshot is captured **once** at `show()` time. If the user
moves a window or scrolls during the picking session, the dropper
still shows the original frame — what you sampled is what was on
screen the moment the dropper opened, not what's there now. Close
and reopen if the desktop has changed and you need a fresh frame.

| Input | Effect |
|---|---|
| Mouse motion | Updates the zoom toplevel position and magnified view; recomputes the crosshair color so it stays readable against the sampled pixel. |
| Mousewheel up | Zooms in by one level (smaller bbox, more magnified pixels). |
| Mousewheel down | Zooms out by one level. |
| Left-click | Commits: reads the pixel under the crosshair, sets `result.get()` to the corresponding `ColorChoice`, fires `<<DialogResult>>` with `confirmed=True`, destroys both toplevels. |
| Right-click | Cancels: sets `result.get()` to `None`, fires `<<DialogResult>>` with `confirmed=False`, destroys both toplevels. |
| Escape | Same as right-click. |

The right-click binding is platform-aware (handled by
`utility.bind_right_click`), so users on macOS-style trackpads
that map right-click to two-finger tap still get the cancel
behavior — the dialog itself, however, won't run on macOS.

### Modality and parenting

The fullscreen toplevel calls `grab_set()` to capture all input
during the picking session. There is no transient parent argument
on the constructor — the dialog parents itself to the
application's root via the runtime `Toplevel` defaults.

Because `show()` is non-blocking, the application's main loop
keeps running while the dropper is active. Any background
animations, periodic timers, or `after()` callbacks scheduled
elsewhere continue to fire. If you want the call site to **wait**
for the user's pick, use `app.wait_variable(dlg.result)` after
calling `show()`:

```python
dlg = ttk.ColorDropperDialog()
dlg.show()
app.wait_variable(dlg.result)   # blocks until left/right-click or Escape
choice = dlg.result.get()       # ColorChoice or None
```

### Platform support

- **Windows** — fully supported. Use a high-DPI-aware app (set
  the appropriate manifest or call `windll.shcore.SetProcessDpiAwareness`)
  or pixel coordinates won't line up with what the user sees.
- **Linux (X11)** — supported. The zoom toplevel uses the X11
  `'-type tooltip'` window-manager hint instead of
  `override_redirect` so it floats correctly in tiling WMs.
- **macOS (aqua)** — **not supported.** PIL's `ImageGrab.grab()`
  has no aqua backend; constructing the dialog will work but
  `show()` will fail when it tries to populate the screenshot
  canvas. `ColorChooserDialog` already detects this case and
  hides its eyedropper button on macOS — apps that drive
  `ColorDropperDialog` directly should add an equivalent guard.

---

## Events

| Hook | Fires |
|---|---|
| `<<DialogResult>>` | Once per `show()` call, after either commit (left-click) or cancel (right-click / Escape). Payload is `{"result": ColorChoice \| None, "confirmed": bool}`. The event is generated on the dialog's own toplevel — there is no `master` on this dialog, so binding before `show()` returns `None` (see gotcha). |
| `on_dialog_result(cb)` | Helper that binds `<<DialogResult>>` and calls `cb(event.data)` — the **payload dict**, not the unwrapped color. Returns the bind id, or `None` if the toplevel doesn't exist yet. |
| `off_dialog_result(funcid)` | Unbinds a callback registered via `on_dialog_result`. |
| `result.trace_add('write', cb)` | The reactive path: fires every time the Variable changes, regardless of whether the change came from a commit or cancel. Useful for live preview. |

```python
dlg = ttk.ColorDropperDialog()
dlg.show()                          # creates self.toplevel
dlg.on_dialog_result(handle_color)  # binds against self.toplevel
```

The event guarantees **exactly one** `<<DialogResult>>` per
`show()` — `_emit_result` short-circuits on its second call. The
underlying Variable, by contrast, is written only when the user
commits or cancels via the bound paths; if the toplevel is
destroyed by an external `destroy()` call, no event fires and
the Variable keeps its previous value.

!!! note "Register `on_dialog_result` after `show()`"
    `on_dialog_result` binds against `self.toplevel`, which is
    `None` until `show()` runs. Calling the helper before `show()`
    returns `None` silently and your callback never fires. The
    same gotcha exists on `DateDialog`, `QueryDialog`, and
    `ColorChooserDialog`, but those at least have a `master`
    fallback — `ColorDropperDialog` doesn't. Always call
    `on_dialog_result` *after* `dlg.show()`, or trace the
    `result` Variable instead (the Variable exists from
    construction time).

---

## When should I use ColorDropper?

Use `ColorDropperDialog` when:

- the entire user task is **"grab the color of something already
  on screen."** A pipette tool, a theme-from-screenshot helper, a
  utility that reads RGB values out of an external app's window.
- you're embedding into a larger color-picker UI (mirror the
  result Variable into your own preview).
- you're driving the dialog from the [eyedropper button on
  `ColorChooserDialog`](colorchooser.md#color-dropper-windows-linux-only)
  — that's the most common path; you almost never instantiate
  `ColorDropperDialog` directly.

Prefer a different control when:

- the user picks colors from a **palette or spectrum**, not from
  the screen → use [`ColorChooserDialog`](colorchooser.md). It
  embeds this dropper as a convenience but exposes spectrum,
  themed swatches, and direct numeric entry alongside it.
- the call site needs a **synchronous helper** that returns the
  picked color → use [`querybox.get_color`](querybox.md), which
  wraps `ColorChooserDialog` (and therefore the dropper) in a
  blocking call.
- you're targeting **macOS** → fall back to `ColorChooserDialog`
  without the dropper, or use `tkinter.colorchooser.askcolor()`
  for a system-native picker.

---

## Additional resources

**Related widgets**

- [`ColorChooserDialog`](colorchooser.md) — palette / spectrum
  color picker; embeds this dropper as its eyedropper button on
  Windows/Linux.
- [`querybox.get_color`](querybox.md) — synchronous helper that
  wraps `ColorChooserDialog` for one-line color prompts.
- [`Dialog`](dialog.md) — the generic builder; not used by
  `ColorDropperDialog` (the dropper is a bare `Toplevel` rather
  than a `Dialog`-shell), but the right escape hatch when the
  fixed UI doesn't fit.

**Framework concepts**

- [Windows](../../platform/windows.md)
- [Localization](../../capabilities/localization.md)

**API reference**

- **API reference:** [`ttkbootstrap.ColorDropperDialog`](../../reference/dialogs/ColorDropperDialog.md)
- **Related guides:** Dialogs, Theming
