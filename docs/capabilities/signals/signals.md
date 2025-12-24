# Signals

Signals provide a structured way to observe and react to state changes in
ttkbootstrap applications.

They complement Tk’s callback and event systems by offering a **declarative,
observable model** for application state and widget interaction.

This page explains what signals are, why they exist, and how they fit alongside
traditional Tk events.

---

## What is a signal?

A signal represents a value that can change over time and notify listeners when
it does.

Signals:

- hold a current value
- notify subscribers on change
- decouple producers from consumers

Unlike callbacks, signals model *state*, not just events.

---

## Signals vs callbacks

Callbacks:

- are invoked in response to a specific action
- are often tightly coupled to widgets
- typically represent a moment in time

Signals:

- represent ongoing state
- can have multiple observers
- allow changes to propagate naturally

Both models are useful and coexist in ttkbootstrap.

---

## Signals vs Tk variables

Tk variables (`StringVar`, `IntVar`, etc.):

- are tied to the Tcl interpreter
- are primarily widget-focused
- propagate changes implicitly

Signals:

- are pure Python objects
- can exist independently of widgets
- integrate cleanly with application logic

Signals may be used internally or bound to widgets as needed.

---

## Typical use cases

Signals are well-suited for:

- shared application state
- selection and view modes
- enabling/disabling UI sections
- synchronizing multiple widgets

They shine when multiple parts of the UI depend on the same value.

---

## Signal lifecycle

A signal:

- is created with an initial value
- notifies listeners when updated
- persists as long as it is referenced

Signals do not depend on the widget lifecycle.
Widgets may subscribe and unsubscribe freely.

---

## Integration with widgets

Widgets may:

- observe a signal to update their state
- emit changes into a signal
- synchronize bidirectionally

This allows widgets to participate in larger application workflows without
owning the underlying state.

---

## Threading considerations

Signals do not make Tk thread-safe.

If a signal is updated from a background thread:

- UI updates must be marshaled back to the event loop
- `after()` or equivalent mechanisms should be used

This mirrors Tk’s threading model.

---

## Common pitfalls

- overusing signals for simple one-off callbacks
- creating signals with unclear ownership
- updating signals from background threads without synchronization

Signals are most effective when used intentionally.

---

## Next steps

- See **Callbacks** for imperative event handling
- See **Virtual Events** for semantic event patterns
- See **Platform → Event Loop** for execution model details
