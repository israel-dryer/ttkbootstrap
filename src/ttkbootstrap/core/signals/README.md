Signals for ttkbootstrap
========================

Lightweight reactive state built on top of tkinter's ``Variable`` API.
Signals wrap a ``tk.Variable`` and provide a small, typed interface for
reading, writing, deriving, and subscribing to changes.

Architecture
- ``Signal[T]``: Generic wrapper around a ``tk.Variable`` with ``get()``,
  ``set()``, ``subscribe()``, and ``map()``.
- ``_SignalTrace`` (internal): Manages Tcl traces for a variable
  (``trace_add``/``trace_remove``).
- ``TraceOperation``: Literal type alias for trace operations
  ("array", "read", "write", "unset").

Key behaviors
- Value access: ``signal()`` or ``signal.get()`` returns the current value;
  ``signal.set(v)`` updates it. Signals can be passed directly to widget
  options like ``textvariable``/``variable``; tkinter uses their Tcl name.
- Subscriptions: ``subscribe(cb, immediate=False)`` registers a callback and
  returns a trace id. Multiple subscriptions of the same callback are supported.
  Use ``unsubscribe(cb)`` to remove all subscriptions for that callback or
  ``unsubscribe_all()`` to clear all.
- Derived signals: ``map(transform)`` creates a new signal that follows this
  one using a transform function. A weak reference prevents the parent from
  keeping derived signals alive unnecessarily.
- Robustness: The last known value is cached and returned if the underlying
  Tcl variable is destroyed. Redundant updates are skipped when the new value
  equals the current one. Exact type matching is enforced in ``set()``.

Usage
1) Quick start
```python
from ttkbootstrap.core.signals import Signal

count = Signal(0)
print(count.get())    # -> 0
count.set(1)
print(count())        # -> 1 (callable alias of get)
```

2) With widgets
```python
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.core.signals import Signal

root = ttk.Window()
name = Signal("")

entry = ttk.Entry(root, textvariable=name)
entry.pack()

label = ttk.Label(root)
label.pack()

name.subscribe(lambda v: label.configure(text=f"Hello, {v}!"), immediate=True)

root.mainloop()
```

3) Derived signals with ``map``
```python
from ttkbootstrap.core.signals import Signal

price = Signal(10.0)
with_tax = price.map(lambda p: round(p * 1.07, 2))

with_tax.subscribe(lambda v: print("price with tax:", v), immediate=True)
price.set(12.0)
```

4) Wrap existing tkinter variables
```python
import tkinter as tk
from ttkbootstrap.core.signals import Signal

root = tk.Tk()
tk_var = tk.IntVar(value=5)
sig = Signal.from_variable(tk_var)

sig.subscribe(print, immediate=True)  # -> 5
tk_var.set(6)  # prints 6
sig.set(7)     # keeps both in sync
```

5) Multiple subscriptions and immediate firing
```python
from ttkbootstrap.core.signals import Signal

flag = Signal(False)

fid1 = flag.subscribe(lambda v: print("A:", v), immediate=True)
fid2 = flag.subscribe(lambda v: print("B:", v))

flag.set(True)  # triggers both

flag.unsubscribe(lambda v: print("B:", v))  # remove all B callbacks
```

Import path
- Public API is re-exported at the package level:
  - ``from ttkbootstrap.core.signals import Signal, TraceOperation``

Notes
- Tkinter is not thread-safe. Perform cross-thread updates using ``after``
  on a Tk widget.
- Callbacks should be fast; long-running work should be scheduled off the UI
  thread.
 - Create ``Signal`` after you create the Tk/Window so the underlying
   ``tk.Variable`` is attached to the same interpreter, or pass ``master=...``
   when constructing ``Signal``.
