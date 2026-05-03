# Signals & Events

A ttkbootstrap widget exposes its behavior through three observation
mechanisms, each with a different signature and timing:

- **Callbacks** — a function passed via `command=` or wired with `bind()`,
  invoked when something happens. The `on_*` helpers (`on_changed`,
  `on_input`, `on_dialog_result`, `on_tab_added`, …) are sugar over
  `bind()` for specific virtual events.
- **Virtual events** — symbolic Tk events written `<<Name>>`, dispatched
  with `event_generate(...)` and observed with `bind(...)`. Listeners
  receive a Tk event whose `.data` carries the payload.
- **Signals** — `Signal[T]` instances wrapping a `tk.Variable`. Listeners
  subscribe to value changes with `signal.subscribe(callback)` and
  receive the new value directly.

Most widgets that hold a value support `signal=` (or `textsignal=`) and
`variable=` (or `textvariable=`) constructor kwargs; the Signal lives
on the widget as `widget.signal` / `widget.textsignal`. Tk's `bind()`
and `event_generate()` are always available.

---

## At a glance

| | Callback | Virtual event | Signal |
|---|---|---|---|
| Registered with | `command=`, `on_*`, `bind()` | `bind('<<Name>>', cb)` | `signal.subscribe(cb)` |
| Listener receives | nothing (or a Tk event) | a Tk event with `.data` | the new value |
| Multiple listeners | one for `command=`; many for `bind()` | many | many |
| Fires on | user invocation only (for `command=`); event delivery (for `bind()`) | `event_generate(...)` | every variable write |
| Decoupled from widget | no | partially (semantic name) | yes (just a `tk.Variable`) |
| Best for | simple per-widget reactions | composite-widget transitions | shared state across widgets |

The three mechanisms are not alternatives — most widgets fire all of
them. A `CheckButton(signal=sig, command=cmd)` runs `cmd` only when
the user clicks (or `cb.invoke()`), but every write to `sig` (user or
programmatic) reaches `signal.subscribe(...)` listeners. The
asymmetry matters when you want "react to user intent" versus "react
to any state change."

---

## Signals

`Signal[T]` is a thin wrapper over a `tk.Variable` (`StringVar`,
`IntVar`, `DoubleVar`, `BooleanVar`, or `SetVar`, chosen from the
constructor argument's type) that adds:

- `signal.subscribe(cb)` / `signal.unsubscribe(fid)` — value-based
  observation; callback receives the new value directly.
- `signal.map(fn)` — derived signal that tracks a transform.
- `signal()` / `signal.get()` / `signal.set(value)` — value access,
  with strict type enforcement on `set`.
- `signal.var` — the underlying `tk.Variable` for use in widget
  `textvariable=` / `variable=` slots.

```python
import ttkbootstrap as ttk

app = ttk.App()
name = ttk.Signal("")

entry = ttk.TextEntry(app, textsignal=name)
label = ttk.Label(app, textvariable=name)  # both views share state

name.subscribe(lambda v: print("name is now:", v))
```

`Signal` lives at `ttkbootstrap.Signal`. Widgets accept `signal=` /
`variable=` for value widgets (CheckButton, Scale, Progressbar) and
`textsignal=` / `textvariable=` for text widgets (Entry, Label,
Button). When both are passed, the signal wins.

For the full API surface, the lazy-creation contract, and the
`Signal.from_variable(...)` adapter for wrapping pre-existing
`tk.Variable`s, see [Signals](signals.md).

---

## Callbacks

A callback is the simplest observation mechanism: pass a function as
`command=` and the widget calls it on user invocation.

```python
def submit():
    print("submitted")

ttk.Button(app, text="Submit", command=submit).pack()
```

`command=` fires only when the user invokes the widget (click, Enter
key, `widget.invoke()`). It does not fire on programmatic value
writes — a `CheckButton(command=cb)` running `cb.set(True)` does not
call the command.

For more general callbacks attached to specific events:

- `widget.bind('<<Change>>', handler)` for virtual events.
- `widget.bind('<Button-1>', handler)` for raw input events.
- `widget.on_changed(cb)`, `widget.on_input(cb)`, `widget.on_tab_added(cb)`,
  and other `on_*` helpers — each is sugar over `bind()` for a
  specific framework event.

Callbacks run synchronously on the Tk event loop; long-running work
must be deferred (`after`, threads, `asyncio` integration). See
[Callbacks](callbacks.md) for the `command` / `bind` / `on_*` surface
in detail.

---

## Virtual events

Virtual events are Tk events identified by a symbolic name in double
angle brackets, dispatched with `widget.event_generate('<<Name>>',
data=payload)` and observed with `widget.bind('<<Name>>', handler)`.

The framework emits dozens of widget-specific virtual events
including `<<Change>>`, `<<Input>>`, `<<Selected>>`, `<<TabAdd>>`,
`<<TabSelect>>`, `<<TabClose>>`, `<<PageChange>>`, `<<PageMount>>`,
`<<PageUnmount>>`, `<<RowClick>>`, `<<SelectionChange>>`,
`<<DialogResult>>`, `<<ItemInvoked>>`, `<<DisplayModeChanged>>`,
`<<ThemeChanged>>`, `<<LocaleChanged>>`, and others. Each widget's
page documents which events it emits and what `event.data` carries.

Two pitfalls worth flagging up front:

- **Virtual events do not propagate up the parent chain.** A
  `<<TabSelect>>` emitted on a `TabItem` does not reach the parent
  `Tabs` widget. This affects more than a dozen widgets in the
  library; bind on the same widget that emits, not its parent.
- **Use `add="+"` to keep prior bindings.** A bare `widget.bind('<X>',
  cb)` replaces any earlier binding on that event for that widget.
  `widget.bind('<X>', cb, add="+")` chains.

See [Virtual Events](virtual-events.md) for the dispatch model,
naming conventions, and `event.data` payload shape.

---

## When to read this section

- *"How do I make two widgets share state?"* —
  [Signals](signals.md).
- *"What's the difference between `command=` and `signal.subscribe`?"* —
  [Callbacks](callbacks.md).
- *"Why doesn't my `<<TabSelect>>` handler fire on the parent `Tabs`?"* —
  [Virtual Events](virtual-events.md).
- *"What happens when an exception escapes a callback?"* —
  [Platform → Event Loop](../../platform/event-loop.md).
- *"How do bindings, bindtags, and `add="+"` interact?"* —
  [Platform → Events and Bindings](../../platform/events-and-bindings.md).
- *"Is the `bind()` walked in widget order or class order?"* —
  [Platform → Events and Bindings](../../platform/events-and-bindings.md).
- *"How do I make a derived value that updates automatically?"* —
  [Signals](signals.md) (`signal.map`).
- *"How do I emit my own semantic event from a custom widget?"* —
  [Virtual Events](virtual-events.md).
