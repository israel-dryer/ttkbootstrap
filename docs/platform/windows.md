# Windows

A Tk application is built around one or more **windows**. The first
one — the root — owns the Tcl/Tk interpreter, the style database,
and the event loop. Every other window is a *toplevel* attached to
that root. ttkbootstrap exposes three window classes for the
distinct roles you'll need them for: `App` (the root), `Toplevel`
(secondary windows and dialogs), and `AppShell` (a high-level
windowed-application shell that subclasses `App`).

This page covers how those classes relate, how to control window
chrome and platform effects, how modality actually works under the
hood, and the lifetime hooks (`WM_DELETE_WINDOW`, `withdraw`,
`destroy`) that determine when a window goes away.

---

## The three window classes

| Class | Role | Owns interpreter? | Common use |
|---|---|---|---|
| `App` | The root window | Yes — exactly one per process | The application's main window |
| `Toplevel` | Secondary window | No — shares the root's interpreter | Dialogs, floating panels, multi-window apps |
| `AppShell` | An `App` subclass with sidebar / toolbar / page-stack scaffolding pre-built | Yes (it *is* an App) | Larger apps where you want the framework to provide the layout shell |

```python
import ttkbootstrap as ttk

# Pick one root class
app = ttk.App(title="Main")
# OR
shell = ttk.AppShell(title="Main")

# Toplevels live underneath (parent flows through master=)
inspector = ttk.Toplevel(title="Inspector", master=app)
```

A process should have exactly one root. Constructing two `App`
instances creates two Tcl interpreters and breaks shared state
(styles, theme registration, image caching). Use `Toplevel` for
secondary windows.

---

## Removing OS chrome (frameless windows)

All three classes can drop the OS title bar, borders, and resize
handles, but they spell the option **inconsistently** — this is
tracked in the docs review bugs list and is worth knowing about
before you copy a snippet between classes:

| Class | Chrome-removal kwarg |
|---|---|
| `App` | `override_redirect=True` (with underscore) |
| `Toplevel` | `overrideredirect=True` (no underscore — matches Tk's native `wm overrideredirect`) |
| `AppShell` | `frameless=True` (renamed entirely) |

```python
ttk.App(override_redirect=True)                       # ✓
ttk.Toplevel(overrideredirect=True, master=parent)    # ✓
ttk.AppShell(frameless=True)                          # ✓ — maps to override_redirect

ttk.App(frameless=True)                               # ✗ TypeError — no such kwarg
ttk.Toplevel(frameless=True, master=parent)           # ✗ TclError — unknown option "-frameless"
```

A frameless window must implement its own drag handle and close
button — without OS chrome, the user has no way to move or close
it otherwise. `Toolbar` is the framework's drop-in for this; see
[Toolbar → Patterns → Custom titlebar](../widgets/application/toolbar.md).

---

## Window styles (Windows only)

The `window_style` parameter on `App` and `Toplevel` enables
backdrop effects via `pywinstyles`. Available values:
`"mica"`, `"acrylic"`, `"aero"`, `"transparent"`, `"win7"`. Silently
ignored on macOS and Linux.

```python
ttk.App(window_style="mica")        # Windows: Mica backdrop; ignored elsewhere
```

See [Platform Differences → Window style effects](platform-differences.md#window-style-effects-windows-only).

---

## Geometry, size constraints, and state

The standard Tk window-manager methods all work on `App` and
`Toplevel`:

```python
app.geometry("800x600+100+100")     # WIDTHxHEIGHT+X+Y
app.minsize(400, 300)               # smallest the user can resize to
app.maxsize(1600, 1200)             # largest
app.resizable(width=True, height=False)   # axis-by-axis lock

app.state("normal")                 # default
app.state("iconic")                 # minimized to taskbar/dock
app.state("zoomed")                 # maximized — Windows canonical;
                                    # macOS accepts but behaves differently;
                                    # some Linux WMs no-op
app.attributes("-fullscreen", True) # cross-platform fullscreen
app.attributes("-topmost", True)    # always-on-top
app.attributes("-alpha", 0.9)       # 0.0 (transparent) to 1.0 (opaque)
```

Reading the same axes uses `winfo_*`:

```python
app.winfo_width(), app.winfo_height()       # current pixel size
app.winfo_x(), app.winfo_y()                # screen coordinates
app.winfo_screenwidth(), app.winfo_screenheight()
```

Like all geometry, `winfo_width`/`winfo_height` are stale until the
event loop's first idle pass. Either bind `<Configure>` or call
`update_idletasks()` first — see [Event Loop](event-loop.md#update-vs-update_idletasks).

---

## Hide vs destroy

Tk gives you two ways to make a window go away:

| Call | Effect | Visible reopen path |
|---|---|---|
| `window.withdraw()` | Removes from screen and taskbar; widget tree intact, state preserved | `window.deiconify()` |
| `window.iconify()` | Minimize to taskbar/dock; OS treats it as live | `window.deiconify()` |
| `window.destroy()` | Tears down the widget tree, fires `<Destroy>`, releases all resources | None — must reconstruct |

Withdraw is the right pick for "close button hides instead of
destroying," for re-shown dialogs (most ttkbootstrap dialogs reuse
the same toplevel across calls), and for splash screens that
disappear after init. Destroy is the right pick when the window's
state is genuinely gone.

The application root's `destroy()` ends the event loop and returns
control to whatever called `mainloop()`. After root destruction,
every other window is also gone.

---

## The close button: `WM_DELETE_WINDOW`

By default, clicking the OS close button calls `destroy()` on the
window. Override the protocol handler to intercept:

```python
def on_close():
    if confirm_unsaved_changes():
        app.destroy()
    # else: do nothing — the close click is swallowed

app.protocol("WM_DELETE_WINDOW", on_close)
```

On macOS, the framework installs native quit behavior on `App` by
default — the red close button calls `withdraw()` instead of
`destroy()`, and Cmd+Q is what actually exits. This is governed by
`AppSettings.macos_quit_behavior`; see
[Platform Differences → Application quit behavior](platform-differences.md#application-quit-behavior).

---

## Modality

A modal window is one the user must dismiss before interacting with
the rest of the application. Modality is built from two
*independent* mechanisms:

- **`grab_set()`** — register an input grab. While in effect, the
  window manager routes mouse and keyboard events only to the
  grabbing window (and its descendants). The user can't click
  outside it.
- **`wait_window(window)`** — recursively enter the event loop and
  return only when `window` is destroyed. The Python frame that
  called this is paused, but the rest of the loop runs normally.

Both are typically used together for a blocking dialog:

```python
dialog = ttk.Toplevel(title="Confirm", master=parent)
# ... build content ...
dialog.transient(parent)        # mark as a child of parent
dialog.grab_set()               # take input grab
dialog.wait_window()            # block until destroyed
# code here runs after the dialog closes
```

Three subtleties worth knowing:

- `grab_set` is a *local* grab — restricted to the application.
  `grab_set_global()` traps even other applications. Almost never
  appropriate; use the local form.
- `wait_window` does *not* by itself enforce modality — without
  `grab_set`, the user can interact with other windows; the calling
  Python frame is just paused. Modality is the grab; blocking is
  the wait.
- `transient(parent)` declares a parent–child relationship for the
  WM. The dialog stays on top of the parent, doesn't get its own
  taskbar entry on most platforms, and minimizes with the parent.
  Always set this on dialogs.

ttkbootstrap's dialog classes (`MessageDialog`, `QueryDialog`,
`FormDialog`, etc.) handle all three calls internally. The pattern
above is what you build when you need a custom modal flow.

---

## Window lifecycle and `<Destroy>`

Window destruction fires `<Destroy>` on every widget in the window's
tree, recursively, *before* the window itself is destroyed. Bind
`<Destroy>` on the toplevel for window-level cleanup:

```python
def on_destroy(event):
    if event.widget is dialog:    # filter out child <Destroy> events
        save_dialog_state()

dialog.bind("<Destroy>", on_destroy)
```

The `event.widget is dialog` check matters because every child also
fires `<Destroy>`, and Tk delivers all of them through the same
binding chain — without the filter, the cleanup runs once per
descendant.

---

## Common pitfalls

**Two `App` instances.** Constructing a second `App` creates a
second Tcl interpreter, which doesn't share styles or images.
Symptom: themes don't apply on the second window, images appear
blank. Use `Toplevel` for additional windows.

**Frameless without a drag handle.** With OS chrome removed, the
user can't move or close the window. Pair with `Toolbar` (custom
titlebar pattern) or your own drag-bar implementation.

**`wait_window` without `grab_set`.** The dialog blocks the calling
code but the user can still click in other windows. Add
`grab_set()` for true modality.

**Hide-leaking dialogs.** A dialog that calls `withdraw()` instead
of `destroy()` keeps its widget tree alive. For long-lived
applications with many dialog uses, that adds up. Either reuse one
instance via `withdraw`/`deiconify`, or `destroy()` on close.

**Setting size before `mainloop`.** A `geometry()` call before the
loop runs is honored by the WM at first map. After mapping, calls
take effect immediately. Don't assume "geometry set before pack"
fires synchronously.

---

## Next steps

- [Platform Differences](platform-differences.md) — close-button
  semantics, system appearance, and the `macos_quit_behavior`
  setting.
- [Event Loop](event-loop.md) — `wait_window` recursion, the queue
  model, and `update_idletasks` for geometry timing.
- [Widget Lifecycle](widget-lifecycle.md) — `<Destroy>` propagation
  and per-widget cleanup hooks.
- [Widgets → AppShell](../widgets/application/appshell.md) — the
  scaffolded application shell when you want sidebar / toolbar /
  pages out of the box.
- [Widgets → Dialogs](../widgets/dialogs/index.md) — pre-built
  modal dialog patterns.
