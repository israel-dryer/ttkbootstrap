# Capabilities

**Capabilities** are cross-cutting behaviors that ttkbootstrap applies consistently across
widgets, dialogs, and application systems.

A capability is not a widget.
It is a behavior that can be *used by many widgets* and *composed into applications*
without duplicating logic.

---

## Why capabilities exist

Traditional Tk applications tend to implement behaviors repeatedly:

- manual variable tracing
- ad-hoc validation logic
- per-widget icon handling
- inconsistent layout conventions
- one-off localization glue

ttkbootstrap addresses this by defining **capabilities**:
well-scoped behaviors with clear contracts that widgets can opt into.

This makes applications:
- easier to reason about
- easier to extend
- more consistent in behavior

---

## Capabilities vs widgets

Widgets answer the question:
> *What UI component do I use?*

Capabilities answer the question:
> *What behaviors does this component support?*

For example:
- a widget may support **signals**
- a widget may support **validation**
- a widget may support **icons and images**
- a widget may support **layout properties**

Capabilities describe *what is possible* and *how it behaves*.
Widgets describe *what it looks like* and *what role it plays in the UI*.

---

## How capabilities are implemented

Each capability is implemented in two layers:

1. **Core capability**
   - lives in `core/capabilities`
   - contains behavior and logic
   - does not depend on widgets

2. **Widget integration**
   - implemented as widget mixins or adapters
   - connects the capability to specific widget options

This separation allows capabilities to be reused across widgets,
dialogs, composite controls, and application systems.

You do not need to understand this layering to *use* capabilities,
but it explains how ttkbootstrap maintains consistency without rigidity.

---

## Capabilities provided by ttkbootstrap

The following capability groups are documented here:

- **Signals & Events**
  - declarative state and change propagation
- **Layout**
  - spacing, scrolling, and container behavior
- **Validation**
  - input validation and feedback
- **Icons & Images**
  - icon sets, image caching, and DPI handling

Each capability page explains:
- what problem it solves
- how users interact with it
- where it applies
- any important constraints or guarantees

For exact APIs, see the API Reference.
