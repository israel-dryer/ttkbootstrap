# State & Interaction

State and interaction describe how widgets and applications respond over time
to user input, internal changes, and system events.

This capability explains how ttkbootstrap models interaction beyond simple
callbacks, tying together widget state, signals, and events.

---

## What is state?

State represents the current condition of a widget or application.

Examples include:
- enabled vs disabled
- selected vs unselected
- focused vs unfocused
- current value or mode

State changes over time in response to interaction.

---

## Interaction as transitions

Interaction is the process of moving between states.

User actions:
- trigger callbacks
- emit virtual events
- update signals

These transitions define application behavior.

---

## Widget state model

ttk widgets expose a standardized state model.

Common states:
- `normal`
- `active`
- `disabled`
- `focus`
- `selected`
- `pressed`

ttkbootstrap builds on this model rather than replacing it.

---

## Signals and state

Signals are often used to represent shared or application-level state.

When a signal changes:

- widgets update their appearance
- actions enable or disable
- dependent logic reacts

This creates a reactive interaction model.

---

## Events and interaction

Events represent discrete moments in time.

They:

- announce transitions
- decouple producers and consumers
- allow multiple listeners

Events complement state-based signals.

---

## State propagation

State may propagate through:

- parent/child relationships
- shared signals
- event emission

Clear propagation paths prevent inconsistent UI behavior.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- modeling meaningful state explicitly
- using signals for shared state
- emitting events for significant transitions
- avoiding hidden or implicit state

These practices lead to predictable interaction flows.

---

## Common pitfalls

- mixing transient events with persistent state
- duplicating state across widgets
- relying on implicit Tk state
- unclear ownership of state

Understanding state and interaction avoids these issues.

---

## Next steps

- See [Signals & Events](signals/index.md) for interaction mechanisms.
- See [Configuration](configuration.md) for initial state definition.
- See [Widgets](../widgets/index.md) for state-driven behavior examples.
