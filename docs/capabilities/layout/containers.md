# Containers

Containers are widgets whose primary role is to **organize and manage layout**
for their child widgets.

In ttkbootstrap, containers are a foundational layout capability rather than
just another widget type.

This page explains how containers are used, why they matter, and how to design
layouts around them.

---

## What is a container?

A container is any widget that:

- can contain child widgets
- participates in a geometry manager
- controls spacing and resizing behavior

Common containers include:

- frames
- labeled frames
- paned windows
- scroll containers

---

## Container ownership

Containers define layout context.

Children:

- inherit geometry constraints from their container
- do not control overall spacing
- request size but do not enforce it

This separation keeps layout predictable.

---

## Single responsibility

Containers should have a clear purpose.

Good container roles:

- grouping related widgets
- managing spacing and alignment
- controlling scrolling
- defining resize behavior

Avoid containers that mix unrelated responsibilities.

---

## Composition over configuration

ttkbootstrap encourages composing layouts from simple containers rather than
heavily configuring individual widgets.

Instead of:

- tuning padding on every widget
- managing resizing individually

Prefer:

- containers with clear spacing rules
- nested layout sections
- reusable container patterns

This leads to clearer and more maintainable layouts.

---

## Nested containers

Nested containers are normal and expected.

However:

- deep nesting increases layout cost
- complex hierarchies are harder to reason about

Balance clarity with simplicity.

---

## Scrollable containers

Scrolling is a container responsibility.

Scrollable containers:

- manage viewport and content size
- coordinate scrollbars
- adapt to dynamic content

Widgets inside scroll containers should not manage scrolling themselves.

---

## Container lifecycle

Containers follow the normal widget lifecycle:

- creation
- layout
- realization
- destruction

Layout effects are not final until the event loop runs.

Avoid querying size too early.

---

## ttkbootstrap guidance

ttkbootstrap promotes:

- using containers to express layout intent
- centralizing spacing decisions
- isolating scrolling behavior
- avoiding layout logic inside widgets

These patterns reduce layout bugs.

---

## Common pitfalls

- using widgets as containers without intent
- over-nesting
- mixing geometry managers
- managing scrolling at the widget level

Understanding container responsibility avoids these issues.

---

## Next steps

- See **Spacing** for padding and margins
- See **Scrolling** for scroll container behavior
- See **Platform → Geometry & Layout** for underlying mechanics
