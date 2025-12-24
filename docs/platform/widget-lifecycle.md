# Widget Lifecycle

Widgets in Tk are created, configured, displayed, and eventually destroyed.
Understanding this **lifecycle** is important for managing resources, bindings,
and state correctly in ttkbootstrap applications.

This page describes how widget lifecycle works in Tk and how ttkbootstrap
expects widgets to be created and managed.

---

## Widget creation

A widget is created when its constructor is called:

```python
label = ttk.Label(parent, text="Hello")
```

At this point:
- the widget object exists in Python
- the underlying Tk widget has been created
- the widget is **not yet visible**

Widget creation should be lightweight.
Expensive work should be deferred until later in the lifecycle.

---

## Geometry management

A widget becomes eligible for display only after it is assigned a geometry
manager:

```python
label.pack()
# or
label.grid()
```

Geometry management:
- determines where the widget appears
- participates in layout calculations
- triggers size negotiation

Until a widget is managed, it does not receive most geometry-related events.

---

## Realization and display

A widget is **realized** when Tk maps it to the screen.
This typically occurs after:

- the widget has been created
- it has been assigned a geometry manager
- the event loop has had a chance to run

Many properties (such as actual size and screen coordinates) are only valid
after realization.

---

## Configuration and updates

Widgets can be configured at any point in their lifecycle:

```python
label.configure(text="Updated")
```

Configuration changes:
- update widget appearance or behavior
- may trigger layout recalculation
- are processed asynchronously by the event loop

ttkbootstrap encourages configuration through **constructor arguments**
and **capabilities**, rather than repeated imperative updates.

---

## Focus and activation

Focus is part of the widget lifecycle:

- focus may change as widgets are displayed
- some widgets only accept focus after realization
- focus-related events are delivered through the event system

Managing focus correctly is especially important for forms and dialogs.

---

## Destruction

Widgets are destroyed explicitly or implicitly:

```python
label.destroy()
```

Destruction:
- releases Tk resources
- removes the widget from the layout
- invalidates references to the underlying Tk widget

After destruction, most widget methods should not be called.

ttkbootstrap does not automatically resurrect destroyed widgets.

---

## Lifetime and garbage collection

Tk widgets are not garbage-collected automatically when Python references are lost.
The underlying Tk widget persists until `destroy()` is called.

This is especially important for:
- images
- fonts
- top-level windows

ttkbootstrap provides abstractions to help manage lifetime correctly, but
explicit destruction is still required.

---

## ttkbootstrap lifecycle guidance

ttkbootstrap encourages a clear lifecycle pattern:

1. create widgets
2. configure behavior and capabilities
3. assign geometry
4. enter the event loop
5. destroy widgets explicitly when done

Following this pattern helps avoid subtle bugs and resource leaks.

---

## Common pitfalls

- querying size or position before realization
- performing expensive work in constructors
- forgetting to destroy top-level windows
- relying on garbage collection for cleanup

Understanding the widget lifecycle helps prevent these issues.

---

## Next steps

- See **Geometry & Layout** to understand layout timing
- See **Events & Bindings** for event delivery
- See **Capabilities** for lifecycle-aware behaviors such as signals and validation
