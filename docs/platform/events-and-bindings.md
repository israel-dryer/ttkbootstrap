# Events & Bindings

Tk delivers user input and system notifications through an **event and binding system**.
Understanding how events are generated, propagated, and handled is essential for building
predictable interfaces with ttkbootstrap.

This page focuses on **how Tk events work** and how ttkbootstrap expects you to use them.
Higher-level reactive patterns are covered in **Capabilities → Signals**.

---

## What an event is

An event represents something that happened:

- a mouse button was pressed or released
- a key was pressed
- a window was resized or exposed
- focus changed
- a timer fired

Events are identified by **event sequences**, such as:

- `<Button-1>`
- `<KeyPress>`
- `<Configure>`
- `<<VirtualEvent>>`

When an event occurs, Tk determines which bindings should run.

---

## Binding events to widgets

Events are typically bound to widgets using `bind`:

```python
widget.bind("<Button-1>", on_click)
```

Bindings associate an event sequence with a callback.
The callback is invoked when the event is delivered to the widget.

Bindings can be attached at different scopes:

- **widget bindings**: apply only to a specific widget
- **class bindings**: apply to all widgets of a given class
- **application bindings**: apply to all widgets in the application

ttkbootstrap does not change this model, but it encourages **explicit, localized bindings**
rather than global ones when possible.

---

## Event propagation

Events in Tk **propagate** through a sequence of bindtags.

Each widget has an ordered list of bindtags that determine where bindings are looked up.
Typical bindtags include:

- the widget instance
- the widget class
- the toplevel window
- the application

When an event occurs, Tk processes bindings in bindtag order until propagation stops.

Understanding propagation is critical when debugging unexpected behavior.

---

## Stopping propagation

Callbacks may stop event propagation by returning the string `"break"`:

```python
def on_click(event):
    do_something()
    return "break"
```

This prevents later bindings from running.

Use this carefully:
stopping propagation can interfere with expected widget behavior if overused.

---

## Virtual events

Virtual events are user-defined events identified by names like:

```text
<<ItemSelected>>
<<DataChanged>>
```

Virtual events allow you to decouple **what happened** from **how it was triggered**.

They are especially useful when:

- multiple inputs should trigger the same behavior
- application-level state changes need to notify many components

ttkbootstrap strongly encourages virtual events for semantic communication.

---

## ttkbootstrap’s guidance on events

ttkbootstrap treats events as a **low-level mechanism**:

- use direct bindings for immediate UI interactions
- use virtual events for semantic signals
- avoid deeply nested binding logic

For application state and data flow, prefer **Signals** over raw events.

---

## Common pitfalls

- binding too many global events
- relying on implicit propagation order
- mixing state mutation and UI effects in callbacks
- overusing `"break"`

Clear event boundaries lead to more maintainable applications.

---

## Next steps

- See **Capabilities → Signals** for declarative state propagation
- See **Widget Lifecycle** to understand when bindings should be created or removed
- See **Event Loop** for how events are scheduled and dispatched
