# Performance

Tk is single-threaded and event-driven, which means every layout
calculation, redraw, and Python callback runs in the same loop. A
slow handler doesn't just delay one widget — it stalls input,
animation, and timers across the whole app. This page covers the
patterns that produce real-world UI lag in ttkbootstrap, the order
of magnitude of common operations, and how to diagnose which one
you're hitting.

For background-work patterns that keep the loop free, see
[Threading & Async](threading-and-async.md).

---

## The five real bottlenecks

In rough order of frequency, these are what slow down ttkbootstrap
applications:

| Bottleneck | Symptom | Fix |
|---|---|---|
| Blocking I/O in handlers | UI freezes for the duration of the call | Move to a worker thread; hand result back via `after_idle` |
| Eager widget construction at startup | Slow startup, slow theme switch | Build views lazily — see [Lazy construction](#lazy-construction) |
| Layout thrashing | Stutter on resize, flicker on data updates | Batch geometry changes; bind `<Configure>` and debounce |
| Image regeneration in loops | Memory growth, slow scrolling | Use the `Image` cache (see [Images & DPI](images-and-dpi.md)) |
| Theme switch with many widgets | Visible "snap" delay on `set_theme()` / `toggle_theme()` | Reduce widget count or defer construction |

Most "performance" complaints land in row 1 or 2.

---

## Don't block the loop

The most common offense is calling something synchronous and slow
from a callback. Anything taking more than ~16 ms (one frame at 60
Hz) is noticeable; anything past 100 ms feels broken.

```python
# Wrong — UI freezes for the request duration
def on_click():
    response = requests.get(url)         # blocking I/O
    label.configure(text=response.text)

# Right — work runs off-thread; UI stays responsive
def on_click():
    threading.Thread(target=fetch_and_update, daemon=True).start()

def fetch_and_update():
    response = requests.get(url)
    app.after_idle(lambda: label.configure(text=response.text))
```

The same applies to `time.sleep(...)` (use `after`),
`subprocess.run(...)` without timeout (run in a thread), and
`socket.recv` / file reads of unknown size.

`update()` inside a handler is a related anti-pattern — it forces
a full event-loop pass mid-handler and can recursively re-dispatch
input events. Use `update_idletasks()` if you only need layout to
settle (see
[Event Loop → `update` vs `update_idletasks`](event-loop.md#update-vs-update_idletasks)).

---

## Lazy construction

Constructing a widget isn't free. For a ttkbootstrap composite,
each `__init__` resolves a style, paints theme colors, registers
for `<<ThemeChanged>>`, builds child widgets, and wires up signal
subscriptions. Multiply by hundreds of widgets and startup time
becomes user-visible.

Three patterns help:

**Defer hidden tabs and pages.** `PageStack.add(key, page=None)`
constructs a `Frame` lazily — the page only materializes when
`navigate(key)` is called for the first time. `Tabs` works the
same way through `TabView`. This is why a 12-tab app can start in
the same time as a 3-tab one.

**Don't pre-build dialogs.** A `MessageDialog`, `FormDialog`, or
`QueryDialog` is a fresh toplevel constructed at `show()` time.
The framework handles this; don't try to "warm" them at startup.

**Virtualize large lists.** `ListView` and `TableView` ask their
data source for *one page* of rows at a time. The non-`view`
ttk widgets (`Treeview`, `Listbox`) don't virtualize — if you put
10 000 rows in a `Treeview`, you've built 10 000 items in Tcl
memory. See the [Performance guidance section on TreeView](../widgets/data-display/treeview.md#performance-guidance).

---

## Layout cost

A `<Configure>` event fires every time a parent's geometry
changes. If your handler triggers a layout change in turn, the
two ping-pong each other and produce flicker:

```python
# Wrong — handler reflows the parent, triggering itself
def on_resize(event):
    label.configure(text=f"{event.width} px")  # changes label width
    # ...which can re-fire <Configure> on the parent...
```

For frequent updates from `<Configure>`, debounce:

```python
import time

_last = {"t": 0}

def on_resize(event):
    now = time.perf_counter()
    if now - _last["t"] < 0.05:           # 50 ms
        return
    _last["t"] = now
    expensive_redraw(event.width, event.height)
```

For programmatic layout updates of multiple widgets, batch them
between `update_idletasks()` calls so geometry resolves in one
pass:

```python
# Avoid: updates each widget interleaves with layout passes
for child in container.winfo_children():
    child.configure(state="disabled")
    container.update()       # forces a full pass each iteration

# Better: change everything, then resolve once
for child in container.winfo_children():
    child.configure(state="disabled")
container.update_idletasks()
```

---

## Image performance

The `Image` utility caches by absolute path or content hash, so
repeated `Image.open("logo.png")` calls return the same
`PhotoImage`. Constructing `tk.PhotoImage(file="logo.png")`
directly does no caching — every call decodes the file.

In a loop or per-row context, the difference is the cost of the
PNG decode times the row count. Cache aggressively.

For dynamic image generation (resizing, recoloring), use Pillow to
produce the variant once and feed it to `Image.from_pil` with a
stable `key=` argument so subsequent retrievals hit the cache:

```python
from ttkbootstrap.api.utils import Image
from PIL import Image as PILImage, ImageOps

def get_thumbnail(path: str, size: int):
    cache_key = ("thumb", path, size)
    cached = Image.get_cached(cache_key)
    if cached is not None:
        return cached
    pil = PILImage.open(path)
    pil.thumbnail((size, size))
    return Image.from_pil(pil, key=cache_key)
```

See [Images & DPI](images-and-dpi.md#the-image-utility) for the
full constructor and cache surface.

---

## Theme switch cost

`<<ThemeChanged>>` is broadcast to every registered widget after a
`set_theme()` or `toggle_theme()`. Each widget's builder runs again
to recompute colors and image elements for the new theme. Cost
scales linearly with widget count.

For an app with a few dozen widgets, the switch is instantaneous.
Past a thousand or so, you see a brief stall. Two strategies:

- **Defer hidden views.** Pages not currently navigated (PageStack,
  TabView) don't pay the cost — their widgets aren't constructed
  yet. This is the same lazy-construction pattern that helps
  startup.
- **Don't subscribe more than necessary.** Custom drawing on
  Canvas / Text / Listbox needs a `<<ThemeChanged>>` listener to
  repaint, but other widgets (the framework's themed widgets) get
  the listener registered for free during construction. Don't
  duplicate it.

---

## Measuring

The fastest way to find a slow handler is `time.perf_counter`
around every callback that's a candidate:

```python
import time

def on_click():
    t0 = time.perf_counter()
    # ... handler body ...
    print(f"on_click: {(time.perf_counter() - t0) * 1000:.1f} ms")
```

For a more systematic pass, wrap event-loop entry points with
`cProfile`:

```python
import cProfile

with cProfile.Profile() as p:
    app.mainloop()
p.print_stats(sort="cumulative")
```

Note that `mainloop` itself dominates `cumulative` time (it's
running the event loop); look at the *callees* — your handlers,
your image decodes, your layout resolutions.

For UI-specific timing, the framework's `update_idletasks()` lets
you measure layout cost discretely:

```python
t0 = time.perf_counter()
big_form.pack(fill="both", expand=True)
big_form.update_idletasks()
print(f"layout: {(time.perf_counter() - t0) * 1000:.1f} ms")
```

---

## Common pitfalls

**`update()` in a handler.** Recursively dispatches events; almost
never the right choice. Use `update_idletasks()` if you need layout
to settle.

**Polling instead of subscribing.** A 100-ms `after_repeat` that
checks for state changes does 10 wakeups/second forever. Subscribe
to the relevant `<<...>>` virtual event or `signal.subscribe`
instead.

**Eager dialog construction.** Don't construct `MessageDialog`
instances at startup "to be ready." They're cheap to construct on
demand, and the framework's `show()` API handles the lifecycle.

**Loading an entire dataset into a `Treeview`.** It doesn't
virtualize. Use `ListView` or `TableView` when row counts exceed
~1000.

**Recreating images in a row callback.** Cache via the `Image`
utility; row rendering should be a dictionary lookup, not a
PNG decode.

---

## Next steps

- [Threading & Async](threading-and-async.md) — the cure for
  blocking I/O in handlers.
- [Event Loop](event-loop.md) — the mental model for everything in
  this page.
- [Debugging](debugging.md) — logging, exception handling, and the
  widget tree dump.
- [Images & DPI](images-and-dpi.md) — the `Image` utility's cache
  semantics.
