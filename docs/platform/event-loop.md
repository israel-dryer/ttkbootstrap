# Event Loop

Every ttkbootstrap application is event-driven. After your `__main__`
code finishes building widgets and registering callbacks, control passes
to the **event loop** — Tk's central dispatcher — and stays there until
the application exits. Understanding what the loop does, what it
schedules, and how it can be blocked is the foundation for everything
else in this section.

---

## What runs in the loop

The loop alternates between two queues maintained by Tcl:

- **The event queue** — input events (mouse, keyboard, virtual events
  posted with `event_generate`) and timer callbacks scheduled with
  `after(ms, ...)`.
- **The idle queue** — work scheduled with `after_idle(...)` plus
  internal Tk redraw and geometry-resolution tasks.

On each iteration the loop drains one event from the event queue,
dispatches it to the relevant handler, then drains every pending idle
task before going back for the next event. Idle tasks therefore run
*between* events — not concurrently, never preempting a handler in
progress.

You enter the loop with:

```python
import ttkbootstrap as ttk

app = ttk.App()
# ... build UI, register callbacks ...
app.mainloop()
```

`mainloop()` returns when the root window is destroyed (typically when
the user closes it or you call `app.destroy()`). Code after `mainloop()`
runs only at shutdown — common uses are persisting state and emitting
exit logs.

---

## The single-threaded rule

Tk is single-threaded. All widget reads, writes, and callbacks must
happen on the thread that called `mainloop()` (typically the main
thread). Touching widgets from a worker thread either crashes or
silently corrupts state, depending on platform.

This is not a limitation ttkbootstrap can paper over. The framework's
position is to expose the boundary clearly:

- For periodic UI work, use `after` / `after_idle` / `after_repeat`.
- For background computation or I/O, use a worker thread plus a queue
  or `after_idle` to hand results back. See
  [Threading & Async](threading-and-async.md) for the full pattern.

---

## Scheduling work

Tk's scheduling primitives are exposed on every widget through
`AfterMixin`:

| Call | When the callback runs |
|---|---|
| `widget.after(ms, fn, *args)` | Once, after at least `ms` milliseconds, on the event queue |
| `widget.after_idle(fn, *args)` | Once, when the event queue next drains and Tk reaches the idle queue |
| `widget.after_cancel(token)` | Cancels a callback whose token came from `after` or `after_idle` |
| `widget.after_repeat(ms, fn, *args)` | ttkbootstrap helper — runs `fn` every `ms` until you call the returned `cancel()` |

All four return promptly (they're queue insertions, not waits).

```python
# Run once after 250 ms
token = app.after(250, lambda: print("tick"))

# Cancel before it fires
app.after_cancel(token)

# Run every 250 ms until cancelled
cancel = app.after_repeat(250, refresh_status)
# ...later...
cancel()
```

Use `after_idle` when you want work to happen *after* the current
handler returns and Tk has finished its pending layout/paint pass — for
example, scrolling to the bottom of a `Text` after inserting content,
or focusing a widget that was just gridded.

---

## `update` vs `update_idletasks`

Two methods let you ask the loop to drain manually:

- `widget.update_idletasks()` runs only the idle queue. It's safe to
  call inside an event handler — geometry/paint catches up, but you
  don't accidentally re-enter user-input dispatch.
- `widget.update()` drains the **whole** loop one full pass: input
  events, timers, idle tasks. Calling it inside an event handler can
  reorder events, fire user callbacks recursively, and tangle modality.
  Avoid it unless you know exactly why you need it.

The common case for `update_idletasks` is reading post-layout geometry
in a handler that just repacked widgets:

```python
frame.pack(...)
frame.update_idletasks()        # let geometry resolve
print(frame.winfo_width())      # now meaningful
```

`update()` is rarely the right answer. If you find yourself reaching for
it, the underlying problem is usually "I want to wait for X" — and the
right tool is `wait_variable` or a worker thread with `after_idle`
hand-off, not `update()`.

---

## Wait calls enter a recursive loop

These three calls — used by every modal dialog in the framework — do
**not** "block while preventing event delivery." They enter a recursive
call to Tcl's event-loop driver:

| Call | Returns when |
|---|---|
| `widget.wait_variable(var)` | `var` is written |
| `widget.wait_window(window)` | `window` is destroyed |
| `widget.wait_visibility(window)` | `window`'s visibility changes |

While the call is on the stack, Tk's event loop runs normally — handlers
fire, timers fire, idle tasks run. The only thing held up is the Python
frame that called `wait_*`. This is how `MessageDialog.show()` blocks
until the user clicks a button: it calls `wait_window` on its toplevel,
and the surrounding event loop keeps the rest of the UI alive.

Two consequences worth remembering:

- Re-entrancy is real. A handler that calls `wait_*` can be invoked
  again before the outer call returns (e.g. the user opens the dialog
  twice). Guard against this with a flag on the caller, or use the
  framework's dialog APIs which gate themselves.
- Modality (the "you can't click outside the dialog" property) comes
  from `grab_set()` on the toplevel, not from `wait_window`. The two
  are independent.

---

## Posting events

To inject an event into the queue from code — typically a virtual event
emitted by a custom widget — use `event_generate`:

```python
widget.event_generate("<<MyChange>>", data={"value": 42})
```

The event is appended to the event queue and fires the next time the
loop drains it. The `data=` payload is passed through Tk's
`-data` attribute and surfaces on the receiving handler as
`event.data`.

`event_generate` is also how you simulate user input in tests
(`widget.event_generate("<Button-1>", x=10, y=10)`), and how to fire
class-level virtual events like `<<ThemeChanged>>` — though framework
code is the usual emitter for those.

---

## Common pitfalls

**Long-running code in a handler.** A click handler that does a 5-second
HTTP request blocks the loop for 5 seconds — no redraws, no other
input, the OS marks the window as "Not Responding." Move the work to a
thread; hand the result back via `after_idle`.

**Calling `mainloop()` more than once.** Each `App` calls `mainloop()`
once internally if you use `app.start()`, or you call it yourself. A
second nested `mainloop()` re-enters the loop recursively, which is
almost never what you want.

**Forgetting `after_cancel`.** A widget destroyed while it has a pending
`after` callback will fire the callback against a dead widget,
typically raising `TclError: invalid command name`. Track the token and
cancel it in your widget's destroy hook.

**Reading geometry without `update_idletasks`.** `winfo_width()` /
`winfo_height()` / `winfo_rootx()` return the *last laid-out* values.
Right after a `pack()` / `grid()` / `place()` call, those are stale
until idle tasks run.

**Recursive `update()`.** Calling `widget.update()` inside an event
handler can recursively dispatch the same handler. Use
`update_idletasks()` if you only need layout to settle.

---

## Next steps

- [Events & Bindings](events-and-bindings.md) — physical events,
  virtual events, and how Tk picks a handler.
- [Widget Lifecycle](widget-lifecycle.md) — construction, destruction,
  and the order in which `<Configure>` / `<<ThemeChanged>>` fire.
- [Threading & Async](threading-and-async.md) — concrete patterns for
  worker threads, queues, and `asyncio` integration.
- [Capabilities → Signals](../capabilities/signals/index.md) — the
  reactive layer ttkbootstrap builds on top of variables and virtual
  events.
