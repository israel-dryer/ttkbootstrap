# Widget Lifecycle

A Tk widget passes through three phases between birth and death:
**created**, **managed**, and **mapped**. Each phase carries different
guarantees about what's true (size, position, visibility) and what
events fire. This page walks the phases, names the ttkbootstrap-specific
hooks attached to each, and lists the lifecycle bugs that bite people
most often: image GC, dangling `after` callbacks, and non-recursive
references to destroyed widgets.

---

## The three phases

| Phase | Triggered by | Properties available | Events fired |
|---|---|---|---|
| **Created** | `WidgetClass(parent, ...)` | Widget object exists; not visible | `<Destroy>` (on later destroy) |
| **Managed** | `widget.pack(...)` / `.grid(...)` / `.place(...)` | Widget claims space in parent's negotiation | `<Configure>` once the geometry manager processes it |
| **Mapped** | Tk maps the widget onto the X/Quartz/Win32 surface (after the event loop processes pending idle work) | `winfo_ismapped()` returns 1; pixel coordinates are real | `<Map>`, then `<Configure>` whenever size changes; `<Expose>` on dirty regions |

A widget can be created without ever being managed (`Frame` you keep
as a hidden state container), and it can be managed without yet being
mapped (just-pack-ed widgets aren't mapped until the next idle pass).

```python
import ttkbootstrap as ttk

app = ttk.App()
btn = ttk.Button(app, text="OK")        # created
btn.winfo_ismapped()                    # 0
btn.pack()                              # managed
btn.winfo_ismapped()                    # still 0 — idle pass hasn't run
btn.update_idletasks()                  # force the idle pass
btn.winfo_ismapped()                    # 1
```

---

## What the constructor actually does

Calling `WidgetClass(parent, ...)` runs the Python constructor *and*
the framework's autostyle wrapper. For ttkbootstrap widgets and for
the 16 themed Tk classes (see [Tk vs ttk](tk-vs-ttk.md#the-autostyle-wrapper)),
construction includes:

1. Capture the styling tokens (`accent`, `variant`, `density`,
   `surface`) into instance attributes. `_surface` is captured even
   when `autostyle=False`.
2. Resolve a style name from the registered builder and set the
   widget's `style=` option (ttk widgets) or paint the theme colors
   directly (Tk widgets).
3. Register the widget for `<<ThemeChanged>>` so the framework can
   re-style it on theme switch.
4. For composites: instantiate child widgets, wire up signals, install
   default validation rules, and set up the event-helper API
   (`on_*` / `off_*` methods).

This means construction is **not free**. A complex composite can do
non-trivial work before its constructor returns. Don't construct
hundreds of widgets eagerly in a startup path; lazily build the ones
you need (e.g., tabs whose pages aren't visible yet) when the user
navigates to them. See `PageStack`'s `add(key, page=None, ...)` for
the lazy-Frame pattern the framework uses.

---

## Theme change as a lifecycle event

When the application theme changes, every registered widget receives
`<<ThemeChanged>>`. The framework's builder for that widget runs
again, recomputes colors and image elements for the new theme, and
applies them. This is why ttkbootstrap widgets switch themes
*instantly* and why custom drawing on `Canvas` / `Text` / `Listbox`
needs to subscribe to `<<ThemeChanged>>` and repaint:

```python
from ttkbootstrap import get_theme_color

canvas = ttk.Canvas(app)

def repaint(_event=None):
    canvas.delete("themed")
    canvas.create_text(
        100, 50, text="hello", tags="themed",
        fill=get_theme_color("foreground"),
    )

canvas.bind("<<ThemeChanged>>", repaint)
repaint()
```

The same event also fires after locale changes route through the
theme provider; widgets that render text via `MessageCatalog` rebuild
their labels on `<<LocaleChanged>>` rather than `<<ThemeChanged>>` —
see [Capabilities → Localization](../capabilities/localization.md).

---

## Configuration after construction

`widget.configure(option=value)` is valid throughout the widget's
lifetime. ttkbootstrap widgets divide configurable options into two
groups:

- **Tk options** (`text`, `padding`, `state`, `width`, `command`,
  `variable`) — round-trip through Tcl unchanged.
- **Framework options** (`accent`, `variant`, `density`, `surface`,
  `signal`, `value`, plus widget-specific keys) — handled by Python
  *configure delegates* that may rebuild a resolved style, refresh
  child surfaces, rewire a signal subscription, or reject the
  reconfiguration with a warning.

Most delegates work cleanly. A few are construction-only — assigning
them post-construction either silently no-ops or raises `TclError`.
The known problem cases are tracked in the docs review plan's bugs
list (e.g. `Scrollbar.configure(orient=...)`,
`Separator.configure(orient=...)`,
`Entry.configure(surface=...)`); the per-widget pages name the
specific limits.

---

## Image and font references

Load images through `Image.open` (or `Image.from_pil`, `Image.from_bytes`,
`Image.transparent`) rather than constructing `PhotoImage` directly.
The `Image` cache keeps every loaded image alive for the life of the
application, so you never need to manage references manually:

```python
from ttkbootstrap import Image

ttk.Label(app, image=Image.open('logo.png')).pack()
# Cache holds the reference; no local variable needed.
```

The same applies to images embedded in `Canvas` (`create_image(...)`)
and `Text` (`image_create(...)`): pass the result of `Image.open` and
the cache handles lifetime automatically.

Font and variable references are usually fine because Tk keeps named
fonts and `*Var` instances alive internally as long as a widget
references them.

---

## `after` callbacks and destruction

A widget that's destroyed while it has a pending `after` callback
will fire that callback against a dead widget, typically raising
`TclError: invalid command name`. The framework guards a few specific
helpers (`after_repeat` returns a `cancel()` function for this
reason), but plain `after(ms, fn)` does not:

```python
class Spinner(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._token = self.after(100, self._tick)
        self.bind("<Destroy>", self._on_destroy)

    def _tick(self):
        # ...rotate icon...
        self._token = self.after(100, self._tick)

    def _on_destroy(self, _event):
        self.after_cancel(self._token)
```

Pairing each `after` with a guarded `after_cancel` in the destroy
handler is the canonical pattern. If you can't track tokens cleanly,
gate the callback with `winfo_exists()`:

```python
def tick(self):
    if not self.winfo_exists():
        return
    # ...do the work...
```

---

## Destruction

`widget.destroy()` removes the widget from the screen, releases its
Tcl resources, fires `<Destroy>`, and recursively destroys every
child. After destroy, every method on the widget either raises
`TclError` or returns stale data — `winfo_exists()` returns `0`.

Children destroyed by parent recursion **also fire `<Destroy>`**
individually before the parent does, so binding `<Destroy>` on a
specific widget is a reliable cleanup hook regardless of how the
destruction was triggered.

```python
class Worker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._cancel = self.after_repeat(500, self._poll)
        self.bind("<Destroy>", self._cleanup)

    def _cleanup(self, _event):
        self._cancel()      # stop the repeating after
        # close files, release locks, etc.
```

`<Destroy>` fires on the widget itself; you can't catch a child's
destruction by binding on the parent unless you also walk the bindtag
list. The `<Destroy>` of a child does *not* propagate to the parent
through any mechanism.

A toplevel's destruction tears down its full tree. The application's
root window destruction returns control from `mainloop()`.

---

## When to use `winfo_exists`

Three places where this check earns its keep:

- Inside an `after` callback that might outlive its widget (or use
  `after_cancel` in a `<Destroy>` handler).
- In a thread that hands work back via `after_idle`, where the widget
  may have been destroyed between the work scheduling and the
  callback firing.
- In a virtual-event handler bound on `bind_all` that may receive an
  event for a widget that's already gone.

```python
def on_global_event(event):
    if not event.widget.winfo_exists():
        return
    # ...act on the surviving widget...
```

---

## Common pitfalls

**Reading `winfo_width()` in `__init__`.** Returns `1`. Bind
`<Configure>` instead, or call `update_idletasks()` first.

**Image GC.** A `PhotoImage` constructed inline in a constructor
disappears at end of the constructor's scope. Pin it on the widget.

**`after` outlasting its widget.** Cancel in `<Destroy>` or guard with
`winfo_exists()`.

**`bind_all` outlasting its target.** A binding on the `"all"` tag
keeps firing for surviving widgets after the registering widget is
destroyed. Use `unbind_all` (or scope to a specific widget tag) when
the registration is per-instance.

**Confusing managed with mapped.** A `pack`-ed widget isn't yet on
screen; it's queued for the next idle pass. `winfo_ismapped()` is
the unambiguous check.

**Calling methods on destroyed widgets.** `winfo_exists()` returns
`0`; most other calls raise `TclError`. Guard externally if a callback
might race with destroy.

---

## Next steps

- [Event Loop](event-loop.md) — when idle tasks run, why
  `winfo_*` is stale right after `pack`/`grid`.
- [Events & Bindings](events-and-bindings.md) — `<Destroy>`,
  `<Configure>`, `<<ThemeChanged>>`, and how Tk dispatches them.
- [Geometry & Layout](geometry-and-layout.md) — propagation,
  `<Configure>`, and reading dimensions safely.
- [Capabilities → State & Interaction](../capabilities/state-and-interaction.md)
  — focus, grab, and lifecycle-aware interaction patterns.
