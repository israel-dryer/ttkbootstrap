# Callbacks

Callbacks are the primary **imperative event-handling mechanism** in Tk and ttk.
They represent functions that are invoked in direct response to user actions
or system events.

This page explains how callbacks work, how ttkbootstrap uses them, and how they
relate to signals and virtual events.

---

## What is a callback?

A callback is a function that is executed when an event occurs.

Examples include:

- clicking a button
- selecting a menu item
- pressing a key
- resizing a window

Callbacks are executed synchronously on the Tk event loop.

---

## Callback execution model

When an event occurs:

1. Tk detects the event
2. the corresponding callback is invoked
3. the callback runs to completion
4. control returns to the event loop

Because callbacks run on the event loop, they must complete quickly.

Blocking inside a callback freezes the UI.

---

## Widget command callbacks

Many widgets expose a `command` option.

This is a convenience mechanism for the most common interaction patterns,
such as button presses or selection changes.

Command callbacks:

- are simple to use
- are limited in contextual information
- map to a single widget action

They are ideal for straightforward interactions.

---

## Event bindings

More complex interactions use **event bindings**.

Bindings:

- are attached using `bind`
- respond to specific event sequences
- receive an event object with context

Bindings allow fine-grained control over input behavior.

---

## Callbacks vs signals

Callbacks:

- represent discrete actions
- are tightly coupled to events
- are typically widget-centric

Signals:

- represent evolving state
- decouple producers and consumers
- support multiple observers

Callbacks often update signals, which then propagate state changes.

---

## Error handling in callbacks

Unhandled exceptions inside callbacks:

- are printed to stderr
- do not crash the application
- may leave UI state inconsistent

It is good practice to:

- log exceptions
- fail gracefully
- keep callbacks small

---

## Performance considerations

Callbacks should:

- avoid long-running work
- defer expensive operations
- update UI incrementally

Use `after()` or background threads for non-UI work.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- using callbacks for direct user actions
- using signals for shared state
- avoiding complex logic inside callbacks
- keeping UI logic declarative where possible

This leads to cleaner, more maintainable applications.

---

## Common pitfalls

- blocking the event loop
- mixing callback and signal responsibilities
- relying on side effects
- handling too much logic in a single callback

Understanding callback scope helps avoid these issues.

---

## Next steps

- See **Virtual Events** for higher-level event patterns
- See **Signals** for state-based communication
- See **Platform → Event Loop** for execution details
