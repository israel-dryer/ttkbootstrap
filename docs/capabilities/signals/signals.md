# Signals

`Signal[T]` is a generic, typed wrapper over a `tk.Variable` that adds
subscription, type enforcement, and a derivation operator. It is the
framework's primary mechanism for sharing reactive state across widgets.

```python
import ttkbootstrap as ttk

name = ttk.Signal("")

name.subscribe(lambda v: print("name is now:", v))
name.set("Alice")
# prints: name is now: Alice
```

`Signal` lives at `ttkbootstrap.Signal`. The class is a thin layer over
the standard Tk variable system — every Signal has a backing
`tk.Variable` accessible via `signal.var`, every value write is just a
Tcl variable write, and listeners are implemented with `trace_add` —
so the value participates in the same Tk dispatch as `textvariable=`
and `variable=`.

For the broader picture of how Signals fit alongside callbacks and
virtual events, see [Signals & Events](index.md).

---

## Constructing a signal

`Signal(value, name=None, master=None)` accepts three arguments:

| Argument | Meaning |
|---|---|
| `value` | The initial value. Its **runtime type** picks the backing `tk.Variable` (see below) and is stored as `signal.type` for the lifetime of the signal. |
| `name` | Optional Tcl variable name. Auto-generated as `"SIG<n>"` when omitted; pass an explicit name to make the variable findable from Tcl or to share a name across processes. |
| `master` | Optional `tk.Misc` to own the underlying variable. Defaults to the implicit root window — the same fallback `tk.StringVar()` uses. |

The signal must be created **after** an `App` (or another `tk.Tk`)
exists, since `tk.Variable` constructors require a default root.

---

## Backing variable

`Signal(value)` chooses its backing `tk.Variable` from the *type* of
the initial value:

| Initial value | Backing variable | Stored as |
|---|---|---|
| `bool` (e.g. `False`) | `tk.BooleanVar` | `0` / `1` |
| `int` (e.g. `0`) | `tk.IntVar` | integer |
| `float` (e.g. `0.0`) | `tk.DoubleVar` | floating-point |
| `set` (e.g. `set()`) | `SetVar` | `repr(set)` |
| anything else | `tk.StringVar` | string |

The check is `isinstance(value, ...)` ordered as above, so `bool`
matches before `int`. `Signal(True)` is a `BooleanVar`-backed signal,
not an `IntVar`-backed one.

The backing variable is published as `signal.var`. Pass `signal.var`
(or `signal` itself, since `__str__` returns the Tcl name) to a widget
slot that expects a `tk.Variable`:

```python
import ttkbootstrap as ttk

app = ttk.App()
name = ttk.Signal("")

# Either form works — configure(textvariable=...) accepts a Tcl name
ttk.Label(app, textvariable=name).pack()
ttk.Label(app, textvariable=name.var).pack()

app.destroy()
```

`Signal.from_variable(tk_var, *, name=None, coerce=None)` adapts a
pre-existing `tk.Variable` — useful for wrapping a variable Tk created
on your behalf (e.g. a widget's auto-built variable) without
re-allocating it:

```python
import tkinter as tk
import ttkbootstrap as ttk

app = ttk.App()

raw = tk.StringVar(value="hello")
sig = ttk.Signal.from_variable(raw)        # wraps, does not copy
print(sig.get())                            # 'hello'
sig.set("world")
print(raw.get())                            # 'world' — same variable

app.destroy()
```

`coerce=` overrides the inferred Python type — for instance, treat an
`IntVar` as `Signal[str]` if you only ever read the stringified form.
Without it, the type is inferred from the variable subclass via the
same table as the constructor (and `BooleanVar` → `bool`,
`IntVar` → `int`, etc.).

---

## Reading and writing the value

A signal is read by calling it (`signal()`) or by `signal.get()` —
they are aliases. The value comes through the backing variable, so
the type round-trips as Python:

```python
import ttkbootstrap as ttk

count = ttk.Signal(0)

count.set(5)
print(count())          # 5  (int)
print(count.get())      # 5  (alias)
print(type(count()))    # <class 'int'>
```

`signal.set(value)` enforces `type(value) is signal.type` strictly —
no subclass coercion, no `int`-from-`bool` slip:

```python
import ttkbootstrap as ttk

count = ttk.Signal(0)

count.set(7)            # ok
try:
    count.set(True)     # bool is a subclass of int, but the check is exact
except TypeError as exc:
    print(exc)          # Expected int, got bool
```

This strictness exists because `bool` is a subclass of `int` in
Python; without the exact-type check, `Signal(0)` would silently
accept `True` and the BooleanVar/IntVar split would be impossible to
preserve. If you need to allow either, build a `Signal(0)` and coerce
explicitly — `count.set(int(flag))`.

`set` short-circuits when the new value equals the current value — no
write to the backing variable, no listener notification:

```python
import ttkbootstrap as ttk

count = ttk.Signal(0)
count.subscribe(lambda v: print("changed:", v))

count.set(0)        # no output — equal to current
count.set(7)        # changed: 7
count.set(7)        # no output — equal to current
```

This matters for derivation patterns: a transform that maps to a
narrower domain (e.g. `int → bool`) won't fire downstream listeners
when the input changes within an equivalence class.

`Signal` proxies attribute lookups to its backing variable through
`__getattr__`, so any `tk.Variable` method works directly on the
signal — `signal.trace_info()`, `signal.trace_add(...)`, and
`signal.trace_remove(...)` all reach through to the underlying
`tk.Variable`. Use this sparingly; the framework already exposes
`subscribe` / `unsubscribe` for the common path.

---

## Subscribing

`signal.subscribe(callback)` registers a listener that fires every
time the backing variable is written. The callback receives the *new
value*, not a Tk event:

```python
import ttkbootstrap as ttk

name = ttk.Signal("")

def react(value):
    print("name is now:", value)

fid = name.subscribe(react)
name.set("Alice")        # name is now: Alice
name.unsubscribe(fid)
name.set("Bob")          # silent
```

`subscribe` returns a trace id (`fid`), a string assigned by Tk that
identifies the underlying `trace_add` registration. Pass the id back
to `unsubscribe(fid)` to detach. `unsubscribe_all()` detaches every
subscriber on the signal. Both `unsubscribe(unknown_fid)` and a
double-`unsubscribe(fid)` are silent — neither raises.

Pass `immediate=True` to also invoke the callback once at registration
time with the current value — useful for "render now, then react to
changes" wiring:

```python
import ttkbootstrap as ttk

name = ttk.Signal("Alice")
name.subscribe(lambda v: print("rendered:", v), immediate=True)
# rendered: Alice  (fires synchronously inside subscribe)
```

Subscribing the **same callable twice** registers two distinct traces.
Both fids are tracked, both fire on every write, and detaching one
leaves the other live:

```python
import ttkbootstrap as ttk

name = ttk.Signal("")
def react(v): print("hit:", v)

fid1 = name.subscribe(react)
fid2 = name.subscribe(react)
name.set("Alice")           # hit: Alice  (twice)
name.unsubscribe(fid1)
name.set("Bob")             # hit: Bob    (once)
```

This is intentional — composite widgets that wire the same handler
through multiple paths rely on it. If you want exactly one
subscription per callable, dedupe at the call site.

!!! note "Dispatch order is reverse insertion order"
    Tk traces fire in the order they were *registered*, but Tcl
    walks them in reverse — the last subscriber added is the first
    one called. With `signal.subscribe(a); signal.subscribe(b);
    signal.subscribe(c)`, a write fires `c`, then `b`, then `a`.
    Don't rely on subscription order for ordering side effects;
    use a single coordinator subscriber that dispatches in the
    order you want.

!!! warning "Exception handling differs between `immediate=True` and normal dispatch"
    Exceptions raised inside the **immediate** invocation are
    silently swallowed — the subscription still registers and the
    error is lost. Exceptions raised inside a **write-driven**
    dispatch propagate to Tk's `report_callback_exception` and
    print to stderr (the standard "Exception in Tkinter callback"
    trace). Don't rely on `immediate=True` to surface errors at
    registration time; wrap the callback yourself if you need to
    fail loudly.

The callback runs synchronously on the Tk thread inside the variable
write. Long-running work must be deferred — schedule with `after()`,
spawn a worker thread, or hand off to the asyncio integration. See
[Platform → Threading and async](../../platform/threading-and-async.md).

---

## Deriving signals with `map`

`signal.map(transform)` returns a *derived* signal that tracks the
output of `transform` applied to every value of the source. The
derived signal is itself a `Signal[U]`, so you can subscribe to it,
bind it to a widget, or chain another `map`:

```python
import ttkbootstrap as ttk

name = ttk.Signal("alice")
upper = name.map(str.upper)

print(upper.get())          # 'ALICE'
name.set("bob")
print(upper.get())          # 'BOB'
```

The derived signal is its own variable; reads come from the cached
transform output, not from re-running `transform()` on demand.

---

## Plugging signals into widgets

Widgets that hold a value accept a constructor kwarg for binding to a
signal. The naming convention splits along value-vs-text:

| Widget kind | Constructor kwargs | Property | Default backing var |
|---|---|---|---|
| Value widgets — CheckButton, Scale, Progressbar, RadioButton, ToggleGroup, … | `signal=` / `variable=` | `widget.signal` / `widget.variable` | inferred from class |
| Text widgets — Entry, Label, Button, OptionMenu, … | `textsignal=` / `textvariable=` | `widget.textsignal` / `widget.textvariable` | `StringVar` |

When both `signal=` and `variable=` (or both `textsignal=` and
`textvariable=`) are passed, the signal wins; the variable argument
is ignored. Composite widgets (TextEntry, NumericEntry, DateEntry,
SelectBox, …) accept the same kwargs and forward them to their inner
primitive — the property still lives on the composite as
`widget.signal` (or `widget.textsignal`, depending on the composite).

Two value widgets sharing one signal stay in lockstep without any
explicit wiring:

```python
import ttkbootstrap as ttk

app = ttk.App()
amount = ttk.Signal(0)

ttk.Scale(app, from_=0, to=100, signal=amount).pack(fill="x")
ttk.Progressbar(app, signal=amount).pack(fill="x")

amount.subscribe(lambda v: app.title(f"value={v:.0f}"))

app.destroy()
```

The same pattern applies to `textsignal=` / `textvariable=` for text
widgets:

```python
import ttkbootstrap as ttk

app = ttk.App()
name = ttk.Signal("")

ttk.TextEntry(app, textsignal=name).pack()
ttk.Label(app, textvariable=name).pack()

app.destroy()
```

### Lazy creation

If a widget is constructed without a `signal=` / `variable=` /
`textsignal=` / `textvariable=` argument, accessing
`widget.signal` (or `widget.textsignal`) for the first time creates
one on demand. The default value depends on the widget class —
`False` for CheckButton, `0` for RadioButton and Progressbar, `0.0`
for Scale, `""` for everything else.

```python
import ttkbootstrap as ttk

app = ttk.App()

cb = ttk.CheckButton(app, text="Agree")
print(cb.signal.get())     # False — Signal[bool] auto-created on first access

ent = ttk.TextEntry(app)
print(ent.signal.get())    # ''   — Signal[str] auto-created on first access

app.destroy()
```

The lazy signal is owned by the widget and exposed by the same
property on every subsequent access — calling `widget.signal` twice
returns the *same* `Signal` instance, so other widgets binding to it
later (`other.signal = cb.signal`) compose correctly.

### Reading subscriptions vs `command=`

`signal.subscribe(...)` and the widget's `command=` parameter (or
its `<<Change>>` virtual event) are not interchangeable. The signal
fires on every variable write; `command=` fires only on user
invocation; `<<Change>>` fires only when the framework explicitly
emits it. The split is documented per widget — but the rule of thumb
is: **subscribe to the signal when you want to react to state, bind
`command=` when you want to react to user intent.** See
[Callbacks](callbacks.md) for the contrast in detail.

---

## Common patterns

**Two-way binding across two views.** Bind both views to the same
signal — Tk's variable system delivers writes to all observers:

```python
import ttkbootstrap as ttk

app = ttk.App()
amount = ttk.Signal(50)

ttk.Scale(app, from_=0, to=100, signal=amount).pack(fill="x")
ttk.Progressbar(app, signal=amount, maximum=100).pack(fill="x")

app.destroy()
```

**Computed view via `map`.** A derived signal makes a transformation
addressable — bind it as a textvariable and the displayed string
tracks the source automatically:

```python
import ttkbootstrap as ttk

app = ttk.App()
count = ttk.Signal(0)
caption = count.map(lambda n: f"{n} items selected")

ttk.Label(app, textvariable=caption).pack()
count.set(3)        # label updates to "3 items selected"

app.destroy()
```

(Bind the derived signal to a name first — see the GC warning above.)

**Wrapping a Tk-owned variable.** Many composite widgets (or
hand-rolled `tk.Spinbox` instances) construct their own
`tk.Variable`. `Signal.from_variable(...)` lets you observe writes
without replacing the variable:

```python
import tkinter as tk
import ttkbootstrap as ttk

app = ttk.App()

raw = tk.StringVar(value="x")
sig = ttk.Signal.from_variable(raw)

sig.subscribe(lambda v: print("write:", v))
raw.set("y")        # write: y
sig.set("z")        # write: z  (same variable)

app.destroy()
```

---

## Reference

**API reference**

- `ttkbootstrap.Signal` — the class.
- `ttkbootstrap.SetVar` — the backing variable used for `set` values.

**Related capabilities**

- [Signals & Events](index.md) — how signals compose with callbacks
  and virtual events.
- [Callbacks](callbacks.md) — `command=`, `bind()`, and the `on_*`
  helpers.
- [Virtual Events](virtual-events.md) — `<<Name>>` events and the
  `event.data` payload.
- [Configuration](../configuration.md) — widget options that aren't
  signals.

**Platform internals**

- [Platform → Events and Bindings](../../platform/events-and-bindings.md) —
  how `trace_add` interacts with the broader event machinery.
- [Platform → Threading and async](../../platform/threading-and-async.md) —
  scheduling work from inside a subscriber callback.
