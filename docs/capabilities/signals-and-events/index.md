# Signals & Events

Signals and events describe how information and interaction flow through a
ttkbootstrap application.

Tk provides a powerful but low-level event system. ttkbootstrap builds on this
by introducing **signals** and encouraging the use of **virtual events** to make
application behavior more declarative, composable, and easier to reason about.

This section explains these mechanisms and how they work together.

---

## Interaction models

ttkbootstrap supports three complementary interaction models:

- **Callbacks** — imperative responses to user actions
- **Virtual events** — semantic notifications of meaningful transitions
- **Signals** — observable state that changes over time

Each model serves a different purpose.

---

## Callbacks

Callbacks are functions executed in direct response to an event.

They are best used for:
- immediate reactions
- simple, localized logic
- triggering state changes

Callbacks are synchronous and run on the Tk event loop.

---

## Virtual events

Virtual events represent *what happened*, not *how it happened*.

They:
- decouple behavior from input devices
- allow multiple listeners
- improve readability and intent

Virtual events are ideal for composite widgets and reusable components.

---

## Signals

Signals represent shared application state.

They:
- hold a current value
- notify observers on change
- decouple producers from consumers

Signals are especially useful when multiple widgets depend on the same value.

---

## How they work together

In a typical flow:

1. a user action triggers a callback
2. the callback updates a signal
3. the widget emits a virtual event
4. other components react independently

This layered approach keeps logic clean and extensible.

---

## Choosing the right tool

Use:

- callbacks for direct user interaction
- signals for shared or persistent state
- virtual events for semantic transitions

They are complementary, not exclusive.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- minimizing complex logic in callbacks
- using signals to model state
- emitting virtual events for meaningful transitions
- documenting exposed events and signals

These practices lead to maintainable applications.

---

## Next steps

- See **Signals** for state-based communication
- See **Callbacks** for imperative handling
- See **Virtual Events** for semantic patterns
- See **Platform → Event Loop** for execution details
