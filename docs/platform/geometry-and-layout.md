# Geometry & Layout

Layout in Tk is controlled by **geometry managers**.
Understanding how geometry works is essential for building interfaces that resize,
align, and behave predictably in ttkbootstrap applications.

This page explains how Tk layout works at a conceptual level and how ttkbootstrap
expects you to structure layouts.

---

## Geometry managers

Tk provides three geometry managers:

- **pack** — simple, flow-based layout
- **grid** — table-based, two-dimensional layout
- **place** — absolute or relative positioning

Only **one geometry manager may be used per container**.
Mixing geometry managers within the same container leads to undefined behavior.

ttkbootstrap does not change this rule.

---

## How layout is resolved

Layout resolution is not immediate.

When geometry is assigned:
- widgets request a size
- containers negotiate available space
- final sizes and positions are computed by Tk

Actual widget dimensions are only reliable **after the event loop has run**.

This is why size-dependent logic should not run in constructors.

---

## Container responsibility

Layout responsibility belongs to the **container**, not the child widget.

Containers:
- control spacing and alignment
- determine how children expand or contract
- define scroll behavior

ttkbootstrap encourages designing layouts by composing containers,
rather than fine-tuning individual widgets.

---

## Resizing behavior

Resizing is governed by:

- geometry manager options (`expand`, `fill`, `sticky`)
- weight configuration (for grid)
- container size constraints

Predictable resizing requires explicitly defining how extra space is distributed.

ttkbootstrap favors explicit layout intent over implicit defaults.

---

## Layout and scrolling

Scrollable layouts introduce additional constraints:

- content size may exceed viewport size
- geometry must adapt dynamically
- scrollbars must stay synchronized

ttkbootstrap provides standardized scroll container patterns to
avoid re-implementing these behaviors repeatedly.

---

## ttkbootstrap layout conventions

While Tk allows many layout styles, ttkbootstrap promotes a few conventions:

- prefer `grid` for structured layouts
- use containers to manage spacing consistently
- avoid deep nesting where possible
- centralize scrolling behavior in dedicated containers

These conventions reduce layout complexity and improve maintainability.

---

## Common pitfalls

- querying widget size before layout resolution
- mixing geometry managers in a single container
- relying on implicit expansion behavior
- implementing scrolling manually for each widget

Understanding layout mechanics helps avoid these problems.

---

## Next steps

- See **Layout Capabilities** for spacing and container helpers
- See **Widget Lifecycle** for layout timing considerations
- See **Platform → Styling** for how layout interacts with styling
