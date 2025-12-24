# Signals

Signals are ttkbootstrap’s **reactive state mechanism**.

They provide a high-level, framework-oriented way for widgets and application
logic to communicate **state changes** without relying on low-level Tk events.

Signals are central to ttkbootstrap’s philosophy: *build modern, reactive
desktop applications with clear data flow and minimal wiring.*


!!! note "Signals are built on Tk variables"
    Signals are **not** “pure Python.” Internally, they are built on **Tk variables** (e.g., `StringVar`, `IntVar`, etc.),
    but they expose a more modern and flexible API on top:

    - `subscribe()` / `unsubscribe()` instead of Tk traces
    - mapping and composition helpers (where supported)
    - easier reuse across widgets and application state

---

## What is a signal?

A **signal** represents a stream of values over time.

Under the hood, a signal is implemented using **Tk variables + traces**, wrapped in a higher-level subscription API.

- Widgets **emit signals** when their state changes
- Application code **subscribes** to signals to react to those changes
- Signals are **decoupled** from widget implementation details

Unlike Tk events, signals are about **state**, not raw user input.

```python
def on_value_changed(value):
    print(value)

signal.subscribe(on_value_changed)
```

---

## Signals vs Tk event bindings

Signals are **not** Tk bindings.

| Tk bindings | Signals |
|------------|---------|
| Listen to low-level UI events | Represent semantic state changes |
| Triggered by user input | Triggered by value changes |
| Use `bind()` / `bind_all()` | Use `subscribe()` |
| Event-driven | Reactive / data-driven |
| Tied to widgets | Can be shared across widgets |

Tk bindings are still useful for:

- raw keyboard and mouse handling
- custom gestures
- low-level widget behavior

Signals are preferred for:

- form values
- selection state
- application state
- coordinated UI updates

---

## Subscribing to a signal

To react to changes, **subscribe** to the signal.

```python
def on_changed(value):
    print("New value:", value)

signal.subscribe(on_changed)
```

Subscriptions are:

- explicit
- easy to reason about
- safe to add and remove dynamically

To stop listening:

```python
signal.unsubscribe(on_changed)
```

This makes signals well-suited for:

- dynamic UIs
- temporary views
- dialogs and overlays

---

## Emitting values

Signals emit values internally when widget state changes.

As a user, you typically do **not** emit signals manually.
Instead, you:

- connect widgets to signals
- subscribe application logic to signals
- let the framework manage propagation

This keeps UI and logic cleanly separated.

---

## Signals and widgets

Many ttkbootstrap widgets accept a `signal` argument:

```python
signal = Signal()

entry = ttk.TextEntry(app, signal=signal)
label = ttk.Label(app, textvariable=signal)
```

In this pattern:

- the entry **updates** the signal
- the label **reacts** to the signal
- neither widget knows about the other

This enables **reactive composition** without tight coupling.

---

## Signals and callbacks

Signals do not replace callbacks — they **complement** them.

Typical usage:

- **Callbacks**: handle immediate user actions (clicks, submissions)
- **Signals**: track ongoing state (values, selection, mode)

Example:

```python
def on_submit():
    print("Submitted:", signal.value)

button = ttk.Button(app, text="Submit", command=on_submit)
```

Here:

- the signal tracks state continuously
- the callback reacts at a specific moment

---

## Signals and virtual events

Some widgets also emit **virtual Tk events** (e.g. `<<Changed>>`).

These exist for:

- interoperability with existing Tk code
- advanced event routing

For most applications:

> **Prefer signals for application logic.**  
> Use virtual events only when you need event-level integration.

See:

- [Virtual Events](virtual-events.md)
- [Callbacks](callbacks.md)

---

## Design philosophy

Signals are intentionally:

- explicit (you opt in)
- predictable (no implicit side effects)
- framework-level (not Tk-specific)

They support ttkbootstrap’s goals:

- modern UI patterns
- reactive data flow
- clean separation of concerns
- scalable application architecture

If you come from frameworks like React, Vue, or Angular,
signals should feel immediately familiar.

---

## See also

**Related capabilities**

- [Callbacks](callbacks.md)
- [Virtual Events](virtual-events.md)
- [Configuration](configuration.md)
- [State & Interaction](state-and-interaction.md)

**API reference**

- **Signal** — `ttkbootstrap.utils.Signal`
