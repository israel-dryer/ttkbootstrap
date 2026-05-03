# Capabilities

The **Capabilities** section explains the cross-cutting framework features
that sit on top of Tk: how reactive state is propagated, how layout is
declared, how input is validated, how images and icons resolve, how
configuration flows from `AppSettings` to widgets, and how locale-aware
text and number formatting work.

Capability pages are not widget documentation. They explain the
**features the framework adds** — the systems that hold across every
widget that uses them, regardless of which widget you reach for.

---

## Capabilities vs Platform vs Guides

These three sections describe related but distinct things:

- **Platform** — the **substrate**. Event loop, geometry managers, ttk
  styling internals, OS-level differences, lifecycle. Mostly inherited
  from Tk; ttkbootstrap explains how it expects you to work with it.
- **Capabilities** — the **framework features layered on top**. Signals,
  validation, the icon pipeline, the configuration dataclass, the
  localization stack. These are concepts ttkbootstrap *adds*; they don't
  exist in plain Tk.
- **Guides** — the **how-to recipes** that combine capabilities and
  widgets to build something concrete (forms, dialogs, navigation
  shells).

For widget APIs, see [Widgets](../widgets/index.md). For exact class
signatures, see the [API Reference](../reference/index.md). For visual
tokens and themes, see [Design System](../design-system/index.md).

---

## When to read this section

Read Capabilities pages when you want to understand:

- how to react to widget state changes without hand-rolling Tk variable
  traces ([Signals & Events](signals/index.md))
- which container best fits a layout, and how spacing and scrolling are
  expressed declaratively ([Layout](layout/index.md))
- how the validation engine combines rules, triggers, and feedback
  ([Validation](validation/index.md))
- how icon names resolve, how images load, and how DPI and theme
  changes propagate ([Icons & Images](icons/index.md))
- which `pack` / `grid` / `place` options ttkbootstrap promotes to
  first-class widget kwargs ([Layout Properties](layout-props.md))
- how widget state, focus, and grabs interact across the framework
  ([State & Interaction](state-and-interaction.md))
- how `AppSettings`, widget kwargs, and `configure()` relate
  ([Configuration](configuration.md))
- how `MessageCatalog` / `IntlFormatter` / `LocaleObserver` cooperate
  to produce a localized UI ([Localization](localization.md))

---

## Topics

**Reactivity**

- [Signals & Events](signals/index.md) — observable state, callbacks,
  and virtual events
- [Signals](signals/signals.md) — the `Signal` class, subscriptions,
  derived signals, Tk-variable interop
- [Callbacks](signals/callbacks.md) — `command=` vs `bind` vs
  `signal.subscribe`, when each fires
- [Virtual Events](signals/virtual-events.md) — `<<EventName>>` payloads,
  emission, propagation rules

**Layout**

- [Layout](layout/index.md) — the four container choices and when each
  fits
- [Containers](layout/containers.md) — `Frame` / `PackFrame` /
  `GridFrame` / `Card` / `LabelFrame` semantics
- [Spacing](layout/spacing.md) — `padding`, `gap`, density, padding
  inheritance
- [Scrolling](layout/scrolling.md) — `ScrollView`, scrollbar visibility
  modes, scroll-direction reconfiguration
- [Layout Properties](layout-props.md) — pack / grid / place options
  surfaced as first-class kwargs

**Input and feedback**

- [Validation](validation/index.md) — the rule engine, triggers, and
  result flow
- [Rules](validation/rules.md) — built-in rule types (`required`,
  `numeric`, `regex`, `stringLength`, …) and custom callable rules
- [Results](validation/results.md) — `ValidationResult` payload,
  `<<Validate>>` event, `is_valid` state
- [State & Interaction](state-and-interaction.md) — widget state flags
  (`disabled`, `readonly`, `focus`, `pressed`), focus traversal, grabs

**Visual assets**

- [Icons & Images](icons/index.md) — overview of the resource pipeline
- [Icons](icons/icons.md) — `BootstrapIcon`, the icon registry, theme
  and state coloring, DPI scaling
- [Images](icons/images.md) — `Image` utility, PhotoImage GC pinning,
  Pillow integration, asset variants

**Configuration and localization**

- [Configuration](configuration.md) — `AppSettings`, widget kwargs,
  `configure()` / `cget()` round-tripping rules
- [Localization](localization.md) — `MessageCatalog` (gettext-backed),
  `IntlFormatter` (Babel-backed), and the `<<LocaleChanged>>` event
  that re-renders translated text and reformats locale-aware values

---

## Next steps

If you are wiring up app state for the first time, start with
[Signals & Events](signals/index.md) — it's the foundation most other
capability pages assume. If you are building forms, jump to
[Validation](validation/index.md) and [Layout](layout/index.md). For
asset handling, [Icons & Images](icons/index.md) covers both icons and
photos in one place.
