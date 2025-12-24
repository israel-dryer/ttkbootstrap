# Layout Properties

Layout properties control how widgets participate in layout within their
containers.

Rather than treating layout options as incidental arguments, ttkbootstrap
documents them as a capability to clarify intent and behavior.

---

## What are layout properties?

Layout properties describe how a widget:

- is positioned
- expands or contracts
- aligns within available space
- participates in scrolling

They are interpreted by the container’s geometry manager.

---

## Common layout properties

Common layout-related properties include:

- row / column
- rowspan / columnspan
- padding
- margins
- expansion and alignment flags

These properties do not move widgets by themselves — containers interpret them.

---

## Container interpretation

Layout properties are **requests**, not commands.

Containers:

- decide how to honor requests
- resolve conflicts
- distribute available space

This separation keeps layout predictable.

---

## Declarative layout intent

ttkbootstrap promotes expressing layout intent declaratively.

Instead of:

- repositioning widgets imperatively
- recalculating geometry manually

Prefer:

- clear layout properties
- well-defined containers
- stable layout hierarchies

---

## Layout timing

Layout properties are applied before final geometry resolution.

Widget size and position:

- are not final during construction
- settle after the event loop runs

Avoid querying layout-dependent values too early.

---

## Interaction with scrolling

Layout properties interact with scrolling behavior.

Scrollable containers:

- may ignore certain expansion requests
- constrain available space
- dynamically adjust content regions

Understanding this interaction avoids layout bugs.

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- consistent use of layout properties
- container-driven layout decisions
- avoiding per-widget geometry hacks
- testing layout under resize and DPI changes

These practices improve maintainability.

---

## Common pitfalls

- mixing geometry managers
- over-specifying layout properties
- assuming layout requests are guarantees
- compensating for layout issues with padding

Understanding layout properties helps avoid these issues.

---

## Next steps

- See **Layout Capabilities** for container behavior
- See **Spacing** for padding and margins
- See **Scrolling** for scroll-aware layout
