---
title: Debugging
---

# Debugging

Debugging Tk and ttk applications can feel opaque because much of the behavior
is managed by the Tcl/Tk engine behind the scenes.
However, there are reliable techniques for understanding what the UI is doing
and why.

This page focuses on **practical debugging strategies** for ttkbootstrap applications.

---

## Understand the event loop

Most UI issues are event-loop related.

Symptoms often include:

- UI freezing
- callbacks firing unexpectedly
- layout appearing incorrect until resize

Start by asking:

- *What callback is running?*
- *Is something blocking the event loop?*

Logging entry and exit of callbacks is often revealing.

---

## Structured logging

Python's `logging` module integrates cleanly with Tk applications. Configure it
once at startup and use it throughout:

```python
import logging
import ttkbootstrap as ttk

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

app = ttk.App(title="My App")
log.info("App started")
app.mainloop()
```

For file output alongside the console:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8"),
    ],
)
```

Use module-level loggers (`logging.getLogger(__name__)`) rather than a single
global logger. This lets you adjust verbosity per module without changing code.

---

## Uncaught exception handler

Tk catches exceptions that occur inside event callbacks and routes them through
`Tk.report_callback_exception`. By default this prints to stderr. Override it to
log the error and optionally show a dialog:

```python
import sys
import traceback
import logging
import ttkbootstrap as ttk

log = logging.getLogger(__name__)


def handle_tk_exception(exc_type, exc_value, exc_tb):
    """Called by Tk when an exception escapes an event callback."""
    log.critical(
        "Unhandled exception in Tk callback",
        exc_info=(exc_type, exc_value, exc_tb),
    )


app = ttk.App(title="My App")
app.report_callback_exception = handle_tk_exception
app.mainloop()
```

For exceptions that occur outside Tk callbacks (startup code, background threads,
or the main thread after `mainloop` returns), override `sys.excepthook`:

```python
def handle_unhandled_exception(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return
    log.critical(
        "Unhandled exception",
        exc_info=(exc_type, exc_value, exc_tb),
    )

sys.excepthook = handle_unhandled_exception
```

---

## Crash dialog pattern

Rather than failing silently, show a dialog when an unhandled exception occurs.
This is especially useful in distributed applications where users may not see
the terminal:

```python
import sys
import traceback
import ttkbootstrap as ttk

_app = None


def crash_handler(exc_type, exc_value, exc_tb):
    """Show an error dialog and log before exiting."""
    import logging
    logging.getLogger(__name__).critical(
        "Crash", exc_info=(exc_type, exc_value, exc_tb)
    )

    message = (
        f"{exc_type.__name__}: {exc_value}\n\n"
        "The application encountered an unexpected error.\n"
        "Please check the log file for details."
    )

    if _app is not None:
        try:
            ttk.MessageBox.error(message, title="Unexpected Error")
        except Exception:
            pass  # If the dialog itself fails, don't recurse

    sys.__excepthook__(exc_type, exc_value, exc_tb)


def main():
    global _app
    sys.excepthook = crash_handler

    _app = ttk.App(title="My App")
    _app.report_callback_exception = crash_handler
    _app.mainloop()


if __name__ == "__main__":
    main()
```

!!! note "Background threads"
    `report_callback_exception` and `sys.excepthook` do not catch exceptions on
    background threads. Use `try/except` in thread targets and route errors back
    to the main thread via the Queue pattern described in
    [Threading & Async](threading-and-async.md).

---

## Inspect widget hierarchy

Understanding the widget tree is critical.

Helpful techniques:

- print widget parents and children
- log `winfo_parent()` and `winfo_children()`
- temporarily add borders or background colors

```python
def dump_tree(widget, indent=0):
    print(" " * indent + str(widget))
    for child in widget.winfo_children():
        dump_tree(child, indent + 2)

dump_tree(app)
```

Visualizing structure often reveals layout mistakes.

---

## Verify geometry timing

Many bugs stem from querying geometry too early.

If values seem wrong:

- ensure the event loop has run
- defer logic using `after_idle()`
- avoid size-dependent logic in constructors

```python
# Wrong — dimensions may be 1x1 before layout resolves
w = widget.winfo_width()

# Correct — defer until after layout
def check_size():
    w = widget.winfo_width()
    print(f"Width: {w}")

app.after_idle(check_size)
```

---

## Debug styles

Styling bugs are usually name-resolution problems — the widget is on
a style you didn't expect, or the style maps a state you didn't
account for.

```python
# What style is this widget on?
print(widget.cget("style"))                  # 'bs[<hash>].primary.Solid.TButton'

# What's the element layout?
from tkinter import ttk
s = ttk.Style()
print(s.layout(widget.cget("style")))        # the element tree

# What color does this style produce in this state?
print(s.lookup(widget.cget("style"), "background"))
print(s.lookup(widget.cget("style"), "background", ["pressed"]))

# What's the current theme?
style = ttk.get_style()
print(style.theme_use())                     # current theme name
print(style.theme_names())                   # list of all installed themes
```

The captured token attributes are useful too — `widget._accent`,
`widget._variant`, `widget._density`, `widget._surface`, and
`widget._style_options` show what the bootstyle wrapper resolved at
construction. Remember that the style is recomputed on every
`<<ThemeChanged>>`, so any `Style.configure(...)` overrides you
applied are wiped on theme switch. See
[Styling Internals](ttk-styles-elements.md) for the full
resolution model.

---

## Image-related issues

Common image bugs include:

- images disappearing (reference lost — see [Images & DPI](images-and-dpi.md))
- incorrect scaling on HiDPI
- excessive memory (image created in a loop)

Check that image objects are stored on a persistent object, not a local variable.

---

## Focus and grab issues

If input behaves strangely:

- log focus changes with `<FocusIn>` / `<FocusOut>` bindings
- verify grab status with `widget.grab_current()`
- check window ownership

```python
app.bind_all("<FocusIn>", lambda e: print(f"Focus → {e.widget}"))
```

---

## Isolate problems

When debugging complex issues:

- reduce the UI to a minimal example
- remove unrelated widgets
- simplify layout and styles

Small reproductions make issues obvious and make it easier to report bugs.

---

## Common pitfalls

- assuming synchronous layout (geometry is resolved asynchronously)
- blocking the event loop in a callback
- losing image references
- forgetting that `report_callback_exception` swallows exceptions silently by default
- not installing `sys.excepthook` for non-callback exceptions

---

## Next steps

- [Threading & Async](threading-and-async.md) — handling exceptions in background threads
- [Performance](performance.md) — responsiveness and latency issues
- [Images & DPI](images-and-dpi.md) — image reference and scaling bugs
