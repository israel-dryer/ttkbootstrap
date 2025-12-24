# Event Loop

At the core of every Tk application is the **event loop**.

Understanding how the event loop works is essential for building responsive,
predictable applications with ttkbootstrap.

---

## What the event loop is

Tk applications are **event-driven**.

Instead of executing code linearly from top to bottom, Tk enters a loop that:

- waits for events (mouse, keyboard, window system, timers)
- dispatches those events to widgets
- updates the UI in response

In Tkinter, this loop is started by calling:

```python
app.mainloop()
```

Once the event loop starts, **your code does not run unless triggered by an event**.

---

## What counts as an event

Events include:

- user input (mouse clicks, key presses)
- window system messages (resize, expose, focus)
- timers scheduled with `after`
- idle callbacks
- virtual events (for example `<<CustomEvent>>`)

All widget interaction ultimately flows through the event loop.

---

## The single-threaded rule

Tk is **single-threaded**.

This means:

- all UI updates must happen on the main thread
- long-running operations block the event loop
- blocking the event loop freezes the UI

ttkbootstrap does not change this rule.

Instead, it provides **patterns and capabilities** that make working within this
constraint easier and more predictable.

---

## ttkbootstrap’s position on the event loop

ttkbootstrap treats the event loop as a **platform boundary**, not something to hide.

The framework:

- embraces Tk’s event-driven model
- avoids background magic that obscures control flow
- favors explicit state changes and clear event boundaries

This makes application behavior easier to reason about and debug.

---

## Scheduling work

Tk provides mechanisms for scheduling work without blocking the UI:

- `after(ms, callback)`
- `after_idle(callback)`
- `wait_variable`
- `wait_window`
- `wait_visibility`

These APIs integrate directly with the event loop.

ttkbootstrap builds on these primitives rather than replacing them.

---

## Modal behavior and the event loop

Modal interactions (such as dialogs) are implemented by **restricting event flow**,
not by starting a new event loop.

Common modal techniques include:

- pointer and keyboard grabs
- `wait_window`
- `wait_visibility`

These techniques allow the event loop to continue running while controlling
where events are delivered.

---

## Where ttkbootstrap adds structure

While ttkbootstrap does not replace the event loop, it layers structure on top of it:

- **Signals** provide declarative, event-driven state propagation
- **Capabilities** standardize event-related behaviors across widgets
- **Dialogs and forms** use consistent modal interaction patterns

All of these features are designed to work *with* the event loop, not around it.

---

## Common pitfalls

- performing blocking I/O in event handlers
- running long computations directly in callbacks
- assuming code after `mainloop()` will run immediately
- creating nested event loops unintentionally

A solid understanding of the event loop helps avoid these issues.

---

## Next steps

- See **Events & Bindings** to learn how events are delivered to widgets
- See **Capabilities → Signals** for reactive state handling
- See **Widget Lifecycle** to understand how widgets enter and leave the UI
