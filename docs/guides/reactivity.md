---
title: Reactivity
---

# Reactivity

Reactivity is how widgets stay in sync with application state without
hand-written update plumbing. ttkbootstrap's reactivity primitive is
the **Signal** — an observable value that widgets bind to and that
notifies subscribers when it changes.

If you've used React's `useState`, Vue's `ref`, or SwiftUI's
`@State` / `@Published`, signals will look familiar: a single source
of truth that the UI reads from, declarative bindings instead of
imperative `widget.configure(text=...)` calls.

---

## The problem signals solve

Without signals, keeping a UI in sync with state means writing the
same shape of glue code over and over:

```python
# Imperative — every consumer needs an explicit update
def on_name_keyrelease(event):
    name = entry.get()
    greeting_label.configure(text=f"Hello, {name}")
    title_label.configure(text=f"Profile: {name}")
    save_button.configure(state="normal" if name else "disabled")

entry.bind("<KeyRelease>", on_name_keyrelease)
```

Every new consumer adds another line to the handler. The state
(`name`) is implicit — it lives in the entry widget, and the rest of
the UI has to *ask* for it.

With a signal, state becomes explicit and consumers attach themselves
to it:

```python
import ttkbootstrap as ttk

app = ttk.App()

name = ttk.Signal("")

ttk.TextEntry(app, textsignal=name).pack()
ttk.Label(app, textvariable=name.map(lambda n: f"Hello, {n}")).pack()
ttk.Label(app, textvariable=name.map(lambda n: f"Profile: {n}")).pack()

app.mainloop()
```

The entry writes to `name`. The labels read from derived signals. No
event handler is involved, and adding another consumer never touches
existing code.

---

## Creating a signal

A signal is constructed with an initial value. The value's Python
type determines the underlying tk.Variable (`StringVar`, `IntVar`,
`DoubleVar`, `BooleanVar`, or a `set`-valued variable).

```python
import ttkbootstrap as ttk

name = ttk.Signal("")          # str-backed
count = ttk.Signal(0)          # int-backed
ratio = ttk.Signal(0.0)        # float-backed
enabled = ttk.Signal(True)     # bool-backed
tags = ttk.Signal({"a", "b"})  # set-backed
```

The type is locked at construction. `set()` enforces an exact type
match (no implicit `int → float` or `bool → int` coercion):

```python
count = ttk.Signal(0)
count.set(42)      # OK
count.set(1.5)     # TypeError — expected int, got float
```

If the initial value isn't yet known, pick the empty value of the
right type (`""`, `0`, `0.0`, `False`) rather than `None`.

---

## Reading and writing

```python
name = ttk.Signal("")

current = name.get()   # read
name.set("Alice")      # write — notifies subscribers

# Calling the signal is equivalent to .get()
current = name()
```

Setting the same value the signal already holds is a no-op —
subscribers are not notified again. This makes it safe to write
through to a signal from a subscriber without creating loops, as long
as the value actually settles.

---

## Binding to widgets

Most ttkbootstrap input widgets accept a signal directly. There are
two parameter names depending on what the widget represents:

- `textsignal=` for text-valued widgets — `TextEntry`,
  `PasswordEntry`, `NumericEntry`, `DateEntry`, `SpinnerEntry`,
  `Label`, `Button`.
- `signal=` for value-valued widgets — `Scale`, `CheckButton`,
  `Radiobutton`, `Spinbox`, `Combobox`, `Progressbar`.

```python
import ttkbootstrap as ttk

app = ttk.App()

name = ttk.Signal("")
volume = ttk.Signal(0.0)
muted = ttk.Signal(False)

ttk.TextEntry(app, textsignal=name).pack()
ttk.Scale(app, from_=0, to=100, signal=volume).pack(fill="x")
ttk.CheckButton(app, text="Mute", signal=muted).pack()

app.mainloop()
```

Binding is two-way: when the user types in the entry, `name` updates;
when you call `name.set("Alice")` from code, the entry updates.

### Signals as `textvariable=` / `variable=`

Signals are duck-typed as tk variables, so they also work in the
classic `textvariable=` and `variable=` slots — including on widgets
that don't have a dedicated `textsignal=` parameter:

```python
name = ttk.Signal("")
ttk.Label(app, textvariable=name).pack()   # works directly
```

Use `textsignal=` / `signal=` when constructing widgets that support
them (clearer intent), and fall back to `textvariable=` / `variable=`
on widgets that don't.

### Reaching the signal after construction

Every signal-aware widget exposes its bound signal as a property,
created lazily if you didn't pass one in:

```python
entry = ttk.TextEntry(app)
entry.textsignal.subscribe(lambda v: print(v))   # creates one on demand

scale = ttk.Scale(app, from_=0, to=100)
scale.signal.set(50.0)
```

This is useful when you want to keep widget construction terse and
attach reactivity afterwards.

---

## Deriving signals

Application state is rarely flat. A username drives a validation
flag; a price drives a formatted display string; a list of items
drives a count. `Signal.map()` creates a **derived signal** that
recomputes whenever the source changes:

```python
celsius = ttk.Signal(0.0)
fahrenheit = celsius.map(lambda c: c * 9/5 + 32)

ttk.Scale(app, from_=0, to=100, signal=celsius).pack(fill="x")
ttk.Label(app, textvariable=fahrenheit).pack()
```

The derived signal is read-only from the application's perspective —
its value is determined entirely by the source and the transform.

`map()` returns another `Signal`, so transforms compose:

```python
raw = ttk.Signal("  hello world  ")
cleaned = raw.map(str.strip).map(str.title)   # "Hello World"
```

### Common map patterns

**Format for display:**

```python
price = ttk.Signal(29.99)
price_text = price.map(lambda p: f"${p:.2f}")
ttk.Label(app, textvariable=price_text).pack()
```

**Boolean to text:**

```python
online = ttk.Signal(True)
status = online.map(lambda v: "Online" if v else "Offline")
ttk.Label(app, textvariable=status).pack()
```

**Validation flag and message:**

```python
username = ttk.Signal("")
is_valid = username.map(lambda u: len(u) >= 3)
hint = username.map(
    lambda u: "" if len(u) >= 3 else "At least 3 characters"
)
```

### Combining multiple signals

`map()` operates on a single source. To derive a value from two or
more signals, subscribe to each and write into a third:

```python
width = ttk.Signal(10)
height = ttk.Signal(20)
area = ttk.Signal(0)

def recompute(_=None):
    area.set(width.get() * height.get())

width.subscribe(recompute)
height.subscribe(recompute)
recompute()   # initialize
```

If you find yourself doing this often, lift it into a helper:

```python
def combine(signals, transform):
    """Derive a signal from multiple sources."""
    result = ttk.Signal(transform(*[s.get() for s in signals]))
    def update(_=None):
        result.set(transform(*[s.get() for s in signals]))
    for s in signals:
        s.subscribe(update)
    return result

area = combine([width, height], lambda w, h: w * h)
```

---

## Side effects

When something needs to happen in response to a change — log a value,
hit an API, persist to disk — use `subscribe()`. The callback
receives the new value:

```python
import ttkbootstrap as ttk

app = ttk.App()

query = ttk.Signal("")

def search(value):
    print(f"Searching for: {value!r}")

query.subscribe(search)

ttk.TextEntry(app, textsignal=query).pack()

app.mainloop()
```

`subscribe()` returns a **subscription id** (a string). Hold onto it
if you ever need to detach the callback:

```python
sub_id = query.subscribe(search)
# ... later ...
query.unsubscribe(sub_id)
```

To run the callback once with the current value at the moment of
subscription (useful for initialization), pass `immediate=True`:

```python
query.subscribe(search, immediate=True)
```

To clear every subscriber at once — typically when tearing down a
view or test fixture — call `unsubscribe_all()`:

```python
query.unsubscribe_all()
```

---

## Two-way binding and shared state

Because widget binding is two-way, the same signal can drive several
inputs and several displays at once. There's no preferred "source"
widget — whichever one was last written to wins, and everyone else
sees the new value.

```python
import ttkbootstrap as ttk

app = ttk.App()

shared = ttk.Signal("type here")

ttk.TextEntry(app, textsignal=shared).pack(pady=5)
ttk.TextEntry(app, textsignal=shared).pack(pady=5)
ttk.Label(app, textvariable=shared.map(str.upper)).pack(pady=5)

app.mainloop()
```

Editing either entry updates the other and the uppercase label —
because they're all looking at the same signal.

---

## Wrapping an existing tk.Variable

If you already have a `tk.StringVar` (or any other tk variable) —
maybe from third-party code, or from a widget you constructed before
deciding you wanted reactivity — wrap it with
`Signal.from_variable()`:

```python
import tkinter as tk
import ttkbootstrap as ttk

var = tk.StringVar(value="hello")
signal = ttk.Signal.from_variable(var)

signal.subscribe(lambda v: print("changed:", v))
var.set("world")   # subscribers are notified
```

The signal and the variable share storage, so writes through either
side propagate.

---

## Pitfalls

**Hold the subscription id if you need to detach.** `unsubscribe()`
takes the id returned by `subscribe()`, not the callback function.
Passing the callback silently does nothing.

```python
fid = signal.subscribe(handler)   # keep fid
signal.unsubscribe(fid)            # detach using fid
```

**Don't store and re-use a derived signal you intend to keep.**
`map()` uses a weak reference internally so derived signals can be
garbage-collected when no one holds them. If you write
`label.configure(textvariable=name.map(str.upper))` and don't keep a
reference to the derived signal, it may be collected and stop
updating. Bind it through the widget (which keeps it alive) or store
it explicitly:

```python
upper_name = name.map(str.upper)         # held by you
ttk.Label(app, textvariable=upper_name)  # also held by widget
```

**Set with the right type.** `Signal` enforces the type chosen at
construction. If you need a numeric signal that may hold ints or
floats, start it with `0.0` (float) — passing `0` (int) locks it to
ints.

**Avoid circular writes that don't settle.** Two signals that
update each other in their subscribers will keep firing as long as
each write changes the value. The redundant-write short-circuit
(setting a signal to its current value is a no-op) usually breaks
the loop, but only once both sides converge. Prefer `map()` for
one-direction derivation.

**Signals can be created before `App()`** — but the underlying tk
variable needs an interpreter, so creating one too early may bind it
to a transient root. Practical rule: create signals after `App()`,
or pass `master=app` if you must create one earlier and want it
attached to a specific root.

---

## How signals relate to Tk variables

A Signal is a thin layer on top of a tkinter `Variable`. The
signal's `.var` property exposes the underlying tk variable, and
`str(signal)` returns its Tcl name — which is why widgets that
expect a `textvariable=` value accept a signal directly.

| Tk variable                | Signal                          |
|----------------------------|---------------------------------|
| `var.get()`                | `signal.get()` or `signal()`    |
| `var.set(x)`               | `signal.set(x)`                 |
| `var.trace_add("write", …)`| `signal.subscribe(…)`           |
| (none — manual logic)      | `signal.map(fn)`                |
| `var.trace_remove(…, fid)` | `signal.unsubscribe(fid)`       |

Anything you can do with a tk variable still works on the underlying
storage; signals add the reactivity layer on top.

---

## Reactivity vs. callbacks vs. events

Signals aren't a replacement for every Tk-level mechanism. Three
distinct things show up in a typical app:

- **Signals** — observable state shared across widgets. Use for
  values that more than one part of the UI depends on.
- **Callbacks** — `command=` on buttons and menu items. Use for
  discrete actions that fire once per user action and don't represent
  ongoing state.
- **Events** — Tk's `bind()` system, including virtual events like
  `<<Changed>>` and convenience methods like `entry.on_changed(…)`.
  Use for input details (keystrokes, mouse, focus) and for
  widget-emitted notifications that carry payload data.

The three coexist comfortably: a button's `command=` callback often
reads the current values of several signals, and a signal change can
trigger application code that itself calls `event_generate` for a
custom virtual event.

For the full event surface, see
[Platform → Events & Bindings](../platform/events-and-bindings.md).
For the framework-internals view of signals, see
[Capabilities → Signals](../capabilities/signals/signals.md). For
the Signal class reference, see
[`ttkbootstrap.Signal`](../reference/utils/Signal.md).

---

## Next steps

- [App Structure](app-structure.md) — how applications are organized
- [Forms](forms.md) — building data-entry forms backed by signals
- [Layout](layout.md) — building layouts with containers
