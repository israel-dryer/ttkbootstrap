# Virtual Events

Virtual events are **semantic, high-level events** that sit above raw input
events in Tk.

They allow applications and widgets to communicate intent without binding
directly to specific mouse or keyboard actions.

This page explains what virtual events are, how they work in Tk, and how
ttkbootstrap encourages their use.

---

## What is a virtual event?

A virtual event is an event identified by a symbolic name rather than a physical
input sequence.

Virtual event names are written in double angle brackets:

```
<<SelectionChanged>>
<<ValueCommitted>>
<<PageShown>>
```

Virtual events describe *what happened*, not *how it happened*.

---

## Why virtual events exist

Binding directly to physical events couples behavior tightly to input devices.

Virtual events:

- decouple behavior from input mechanics
- allow multiple triggers for the same action
- improve readability and intent

They are especially useful for composite widgets and complex interactions.

---

## Generating virtual events

Virtual events are generated programmatically using `event_generate`.

A widget may generate a virtual event when:
- internal state changes
- a user action completes
- a significant lifecycle transition occurs

This allows other components to react without knowing internal details.

---

## Binding to virtual events

Virtual events are handled like any other event binding.

Listeners can:

- bind at the widget level
- bind at the container level
- bind globally if appropriate

Because virtual events are semantic, bindings tend to be more stable over time.

---

## Virtual events vs callbacks

Callbacks:

- are typically attached directly to widgets
- represent immediate actions
- are often single-consumer

Virtual events:

- broadcast intent
- may have multiple listeners
- support loose coupling

Callbacks often *emit* virtual events.

---

## Virtual events vs signals

Signals represent evolving state.

Virtual events represent discrete transitions.

Both are useful:

- signals synchronize state
- virtual events announce milestones

They are complementary, not competing mechanisms.

---

## Naming conventions

Good virtual event names:

- describe the semantic action
- avoid referencing input devices
- use past tense or completed intent

Examples:

- `<<ItemSelected>>`
- `<<FormSubmitted>>`
- `<<DialogClosed>>`

Consistent naming improves discoverability.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- using virtual events for composite widgets
- emitting events for meaningful state transitions
- documenting virtual events exposed by widgets

This enables extension and customization without subclassing.

---

## Common pitfalls

- overusing virtual events for trivial actions
- emitting events too frequently
- unclear or inconsistent naming

Virtual events are most effective when used intentionally.

---

## Next steps

- See [Signals](signals.md) for state propagation.
- See [Callbacks](callbacks.md) for imperative handling.
- See [Widgets](../../widgets/index.md) for virtual events exposed by specific components.
