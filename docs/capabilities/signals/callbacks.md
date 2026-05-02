# Callbacks

ttkbootstrap exposes three callback registration surfaces, all of which
ultimately call a Python function on the Tk thread when something
happens. The choice between them is mechanical — each is appropriate
for a different observation question — and most widgets support more
than one.

| Surface | Registered with | Fires on | Listener receives | Multiple listeners |
|---|---|---|---|---|
| `command=` kwarg | constructor or `configure(command=fn)` | user invocation only | nothing (`fn()`) | one (later overwrites) |
| `widget.bind(seq, fn, add="+")` | the [bindtag chain](../../platform/events-and-bindings.md) | every event delivery | a Tk `Event` (with `.data` for virtual events) | many (when `add="+"`) |
| `widget.on_*(fn)` helper | sugar over either of the above | depends — see below | depends — see below | many |

`command=` is the right surface for "the user did the thing"; `bind`
is the right surface for everything else. Signals (`signal.subscribe`)
are a fourth observation channel that watches a `tk.Variable` rather
than a callback dispatch — see [Signals](signals.md).

For the broader picture of how the three event mechanisms compose, see
[Signals & Events](index.md).

---

## `command=`

A handful of action-oriented widgets accept a `command=` constructor
kwarg. The callable takes no arguments and is invoked exactly once per
*user invocation*:

```python
import ttkbootstrap as ttk

app = ttk.App()
ttk.Button(app, text="Save", command=lambda: print("saved")).pack()

app.destroy()
```

| Widget | Fires on |
|---|---|
| `Button`, `Toolbutton`, `MenuButton`, `DropdownButton` | click, `<space>` while focused, `widget.invoke()` |
| `CheckButton`, `Switch`, `CheckToggle` | click, `<space>` while focused, `widget.invoke()` (NOT on programmatic value writes) |
| `RadioButton`, `RadioToggle` | click, `<space>` while focused, `widget.invoke()` (NOT on programmatic value writes) |
| `OptionMenu` | menu item selection (NOT on `optionmenu.set(...)` programmatic writes — but see the double-fire bug below) |
| `Scale` | every interactive movement (drag, arrow key) — fires repeatedly |
| `Spinbox` | stepping (arrow click, Up/Down key, `<<Increment>>` / `<<Decrement>>`) only — NOT on typing or on `spinbox.set(...)` |

The user-invocation contract matters: a `CheckButton(signal=sig,
command=cmd)` paired with `sig.set(True)` does **not** call `cmd` —
only a click or `cb.invoke()` does. Signal subscribers fire on every
write; `command=` fires only on user intent. Use that asymmetry
deliberately:

- *"Save the row when the user toggles it"* → `command=`.
- *"Recompute the derived widget every time the value changes for any
  reason"* → `signal.subscribe(...)`.

`command=` accepts a single callable. Setting it a second time
overwrites — there is no chaining mechanism. Pass `command=""` (or
`command=None`) to clear:

```python
btn = ttk.Button(app, text="Save", command=first_cb)
btn.configure(command=second_cb)   # first_cb is gone
btn.configure(command="")           # no command at all
```

If you need multiple handlers for the same user action, use
`widget.bind('<Button-1>', ...)` (or the widget's emitted virtual
event, like `<<Invoke>>`) with `add="+"`, not `command=`.

---

## `widget.bind`

`widget.bind(sequence, function, add=None)` is the general callback
surface. It registers `function` on a Tk binding tag and returns a
binding identifier — a string used to detach the binding later.

```python
btn = ttk.Button(app, text="Custom")
fid = btn.bind("<Button-1>", lambda e: print("clicked at", e.x, e.y))
```

The function receives a Tk `Event` object with the usual fields
(`x`, `y`, `widget`, `keysym`, `state`, …). Virtual events (the
`<<Name>>` form) carry an extra `event.data` field — the framework's
emitted events use it to ferry payload dicts:

```python
te = ttk.TextEntry(app)
te.entry_widget.bind("<<Change>>", lambda e: print(e.data))
# user types "hi" → {'value': 'hi', 'prev_value': 'h', 'text': 'hi'}
```

For the full bindtag walk (widget tag → class tag → toplevel tag → "all"),
how `event_generate` interacts with `<Destroy>`, and the cross-platform
`Mod` substitution for keyboard shortcuts, see
[Platform → Events and Bindings](../../platform/events-and-bindings.md).

### `add="+"` is almost always what you want

A bare `widget.bind(seq, fn)` *replaces* any prior binding on `seq`
for that widget. With more than one consumer wiring up handlers on
the same event, the second call silently destroys the first:

```python
btn.bind("<<X>>", first)
btn.bind("<<X>>", second)        # first is gone — destroyed silently
btn.event_generate("<<X>>")      # only "second" fires
```

`add="+"` (or `add=True`) chains:

```python
btn.bind("<<X>>", first, add="+")
btn.bind("<<X>>", second, add="+")
btn.event_generate("<<X>>")      # both fire, in registration order
```

The framework's `on_*` helpers all use `add="+"` internally, so
mixing them with raw binds is safe. Mixing two raw binds without
`add="+"` is the bug.

### Detaching by id

`widget.unbind(seq, fid)` detaches a single binding registered with
`add="+"` — but see the `!!! danger` block below before relying on
it. `widget.unbind(seq)` (no fid) clears every binding on that
sequence:

```python
fid = btn.bind("<Button-1>", handler)
btn.unbind("<Button-1>", fid)    # detach this one
btn.unbind("<Button-1>")          # detach every <Button-1> handler
```

!!! danger "`unbind(seq, fid)` is broken for `add="+"` bindings on Python 3.13"
    The CPython 3.13 implementation of `Misc._unbind` filters the bind
    script for lines starting with `if {"[<fid> ` — the wrapper form
    Tk uses for non-`add` bindings. Bindings registered with
    `add="+"` produce raw script lines starting with the bare fid, so
    the filter never matches: no lines are removed but
    `Tcl.deletecommand(fid)` still runs, leaving dangling references
    in the bind script. Subsequent `event_generate(seq)` then dispatches
    to the deleted proc and aborts the entire binding sequence
    silently — *every* handler on `seq`, not just the targeted one,
    stops firing. Verified on Python 3.13.9 with Tk 8.6. Workaround:
    `widget.unbind(seq)` to detach everything and re-bind the
    handlers you want to keep, or hold a single dispatcher closure
    and switch its body via a flag instead of unbinding.

---

## `on_* / off_*` helpers

Most ttkbootstrap widgets expose `on_<event>(fn)` and matching
`off_<event>(id)` helpers that wrap `bind()` or `signal.subscribe()`
for a specific event. They exist to (a) name the event without
quoting the `<<VirtualName>>` string, (b) default `add="+"`, and (c)
sometimes enrich the event data the listener receives.

```python
te = ttk.TextEntry(app)

fid = te.entry_widget.on_changed(lambda e: print(e.data["value"]))
# … later
te.entry_widget.off_changed(fid)
```

There are roughly 140 such helpers across the widget surface. They
are **not uniform** in callback shape. Three patterns exist:

| Pattern | Backed by | Callback receives | Returned id detached with |
|---|---|---|---|
| **Bind passthrough** | `widget.bind(seq, fn, add="+")` | a Tk `Event`; `event.data` is whatever the emitter passed | `widget.unbind(seq, fid)` → `off_*(fid)` |
| **Bind + enrich** | `widget.bind(seq, wrapper, add="+")` where `wrapper` rebuilds `event.data` from widget state, then calls `fn(event)` | a Tk `Event`; `event.data` is the enriched dict | `off_*(fid)` |
| **Signal subscribe** | `signal.subscribe(fn)` | the new value (no event wrapper) | `signal.unsubscribe(sid)` → `off_*(sid)` |

Examples of each:

- **Bind passthrough.** `ListView.on_item_click(cb)` →
  `cb(event)` with `event.data = {'record': dict}`.
  `Tabs.on_tab_added(cb)` → `cb(event)` with `event.data = None`.
- **Bind + enrich.** `TextEntryPart.on_enter(cb)` →
  `cb(event)` with a synthesized `event.data = {'value': ...,
  'text': ...}` built from widget state at firing time, even though
  the underlying `<Return>` event normally carries no `data`.
- **Signal subscribe.** `Tabs.on_tab_changed(cb)` → `cb(value)`
  (the new selected key, as a string). No event wrapper — wraps
  `signal.subscribe`.

The bind-vs-subscribe split is observable in the returned id: bind
helpers return strings ending in `wrapper` (a Tcl command name);
subscribe helpers return strings ending in `traced_callback` (a Tk
trace id):

```python
fid = te.entry_widget.on_changed(lambda e: ...)   # '4690485056wrapper'
sid = tabs.on_tab_changed(lambda v: ...)           # '4684328192traced_callback'
```

The shape inconsistency is a known wart — handlers can't be written
generically across the helper surface. The per-widget docs name the
shape for each helper. As a rule of thumb: helpers tied to a value
(`on_changed`, `on_tab_changed`, `on_accordion_changed`,
`on_page_changed`, `on_selection_changed` on some widgets) tend to
deliver values; helpers tied to a discrete event (`on_clicked`,
`on_item_*`, `on_tab_added`, `on_dialog_result`) tend to deliver
events. Read the docstring before writing the handler.

There is one further inconsistency — dialog-result helpers
(`MessageDialog.on_dialog_result`, `QueryDialog.on_dialog_result`,
`DateDialog.on_result`, `ColorChooserDialog.on_dialog_result`) take
the bind path *and* unwrap `event.data` to pass the payload dict
directly to the user callback, so the caller never sees the event
wrapper at all:

```python
md.on_dialog_result(lambda data: print(data))
# data == {'result': 'ok', 'confirmed': True}  — not an event
```

That's the third callback shape on the same naming pattern, and the
[Dialogs](../../widgets/dialogs/messagedialog.md) pages name it
explicitly.

---

## Exception handling

Exceptions raised inside a callback — `command=`, `bind`, or any
`on_*` helper — are caught by Tk's `report_callback_exception`,
printed to stderr as the standard `Exception in Tkinter callback`
traceback, and discarded. The event loop continues; subsequent
callbacks fire normally; the UI stays responsive:

```python
def boom():
    raise ValueError("boom!")

ttk.Button(app, text="Crash", command=boom).invoke()
# stderr:
#   Exception in Tkinter callback
#   Traceback (most recent call last):
#     File ".../tkinter/__init__.py", line 2074, in __call__
#       return self.func(*args)
#     ...
#   ValueError: boom!
```

This is convenient for development (you see the traceback) and
dangerous for production (you may not). To override, set
`tk.Tk.report_callback_exception` on the app — for example, route
to `logging.exception(...)` so traces land in your log pipeline:

```python
import logging

def report_to_log(exc, val, tb):
    logging.exception("Tk callback raised: %s", val)

app.report_callback_exception = report_to_log
```

The handler is called on the Tk thread and should return quickly.
Don't show a Tk dialog from inside it; that re-enters the event loop
and can compound failures.

One asymmetry worth knowing about: exceptions raised inside a
`signal.subscribe(cb, immediate=True)` invocation are silently
swallowed at registration time, while the same callback raising on a
later write goes through `report_callback_exception` normally. See
[Signals → Subscribing](signals.md#subscribing) for the warning
block.

---

## Common patterns

**Fan-out from `command=` to multiple handlers.** `command=` only
holds one callable. To fan out, either chain inside one wrapper or
move to `bind` + `event_generate`:

```python
def composite_action():
    save_to_db()
    notify_observers()
    update_status()

ttk.Button(app, text="Save", command=composite_action).pack()
```

**Listen for "user did the thing" without a `command=` slot.** Bind
the widget's emitted virtual event (or the underlying Tk event):

```python
btn = ttk.Button(app, text="Save")
btn.bind("<<Invoke>>", lambda e: print("invoked"), add="+")
btn.bind("<Button-1>", lambda e: print("clicked"), add="+")
```

**Defer expensive work out of the callback.** Callbacks run on the Tk
thread; long work freezes the UI. Schedule with `app.after(0, fn)`
to yield to the event loop, or hand off to a worker thread and post
the result back via `after` from the worker:

```python
def kick_off_export():
    threading.Thread(target=export_worker, daemon=True).start()

ttk.Button(app, text="Export", command=kick_off_export).pack()
```

See [Platform → Threading and async](../../platform/threading-and-async.md)
for the worker-to-Tk-thread patterns.

**Bind once, dispatch by tag.** When the same handler should fire on
multiple widgets, prefer binding on the class bindtag (or your own
custom bindtag) over re-binding per widget:

```python
app.bind_class("TButton", "<<Invoke>>", on_any_button_invoked, add="+")
```

`bind_class` is the bindtag-aware sibling of `bind`; it covers every
widget of that class. See [Platform → Events and
Bindings](../../platform/events-and-bindings.md) for the bindtag
walk.

---

## Reference

**API reference**

- `Tk.report_callback_exception` — global exception handler.
- `Misc.bind` / `Misc.unbind` — the underlying primitives.
- `Misc.event_generate` — synthesize an event (with optional `data=`).

**Related capabilities**

- [Signals & Events](index.md) — the three observation mechanisms.
- [Signals](signals.md) — `signal.subscribe` and the value-change
  channel.
- [Virtual Events](virtual-events.md) — `<<Name>>` events and the
  `event.data` payload protocol.

**Platform internals**

- [Platform → Events and Bindings](../../platform/events-and-bindings.md) —
  bindtag walk, `add="+"`, cross-platform `Mod` substitution.
- [Platform → Event Loop](../../platform/event-loop.md) — how `after`,
  `update_idletasks`, and modal `wait_*` calls interact with
  callback dispatch.
- [Platform → Threading and async](../../platform/threading-and-async.md) —
  worker-thread patterns for callbacks that can't run synchronously.
