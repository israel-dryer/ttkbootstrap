# Containers

Containers are widgets whose primary role is to **organize, constrain, and express layout**
for their child widgets.

In ttkbootstrap, containers are a **core layout capability**, not just passive widget holders.
They are used to **encode layout intent**, centralize spacing rules, and reduce repetitive
geometry configuration.

This page explains how containers are used, why they matter, and how to design layouts around
them.

---

## What is a container?

A container is any widget that:

- can contain child widgets
- participates in a geometry manager (`pack`, `grid`, or `place`)
- defines spacing, alignment, and resize behavior for its children

Common containers include:

- `Frame`
- `LabelFrame`
- `PanedWindow`
- scroll containers
- layout-focused containers like **PackFrame** and **GridFrame**

---

## Container ownership

Containers define **layout context**.

Children:

- inherit geometry constraints from their container
- request size but do not enforce it
- should not control overall spacing or alignment

This separation keeps layouts predictable and prevents widgets from leaking layout concerns
into unrelated parts of the UI.

---

## Containers as layout intent

In ttkbootstrap, containers are often used to express **layout intent**, not just grouping.

Examples:

- “This section is a vertical stack with consistent spacing”
- “This area is a form with aligned labels and fields”
- “This panel scrolls, but its children do not”

Encoding these ideas at the container level leads to clearer, more maintainable layouts.

---

## Frame vs PackFrame vs GridFrame

ttkbootstrap provides container variants that **build on Tk’s geometry managers** while
reducing repetitive configuration.

### Frame

`Frame` is the most flexible and lowest-level container.

Use it when:

- you want full control over `pack` / `grid`
- you are building custom layout behavior
- layout rules vary significantly between children

### PackFrame

`PackFrame` is a **pack-based layout container** optimized for one-direction layouts.

It adds:

- consistent `gap` handling between children
- explicit layout direction (vertical or horizontal)
- centralized container-level spacing rules

Use `PackFrame` for:

- vertical stacks (forms, settings panels)
- horizontal groups (toolbars, button rows)
- layouts where `pack` would otherwise be repeated on every child

`PackFrame` does **not** replace `pack`; it **encapsulates common pack patterns**.

### GridFrame

`GridFrame` is a **grid-based layout container** optimized for aligned, multi-dimensional layouts.

It adds:

- consistent row/column `gap`
- structured row and column definitions
- clearer intent for form-style and alignment-heavy layouts

Use `GridFrame` for:

- forms and property editors
- label/value alignment
- layouts where grid structure matters more than absolute placement

`GridFrame` does **not** replace `grid`; it **standardizes common grid usage**.

---

## Composition over configuration

ttkbootstrap encourages composing layouts from **purposeful containers**
instead of heavily configuring individual widgets.

Instead of:

- tuning padding on every widget
- repeating `padx` / `pady` everywhere
- manually coordinating alignment rules

Prefer:

- containers with clear spacing rules
- nested layout sections
- reusable container patterns

This leads to layouts that are easier to reason about and modify.

---

## Nested containers

Nested containers are normal and expected.

However:

- deep nesting increases layout complexity
- excessive hierarchy can obscure intent

Aim for **logical sections**, not minimal widget count.

---

## Scrollable containers

Scrolling is a **container responsibility**.

Scrollable containers:

- manage viewport and content size
- coordinate scrollbars
- adapt to dynamic content

Widgets inside scroll containers should **not** manage scrolling themselves.

---

## Container lifecycle

Containers follow the normal widget lifecycle:

- creation
- layout
- realization
- destruction

Layout effects are not final until the event loop runs.

Avoid querying size or position too early.

---

## ttkbootstrap guidance

ttkbootstrap promotes:

- expressing layout intent at the container level
- centralizing spacing and alignment
- isolating scrolling behavior
- avoiding layout logic inside leaf widgets

These patterns reduce layout bugs and improve consistency.

---

## Common pitfalls

- using widgets as containers without intent
- over-nesting layout hierarchies
- mixing geometry managers in the same container
- managing scrolling at the widget level

Understanding container responsibility helps avoid these issues.

---

## Next steps

- See **Spacing** for padding, margins, and gaps
- See **Scrolling** for scroll container behavior
- See **Widgets → Layout** for container widgets
- See **Platform → Geometry & Layout** for underlying mechanics
