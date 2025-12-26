---
title: Containers
---

# Containers

Containers are widgets whose primary role is to **organize layout** for child widgets.

In ttkbootstrap, containers are more than “a place to put widgets” — they are where you express **layout intent**:
spacing rules, scrolling behavior, and consistent resizing patterns. That keeps individual widgets simpler and makes
UIs easier to evolve.

See [Platform → Geometry & Layout](../../platform/geometry-and-layout.md) for how Tk geometry managers actually compute size and placement.

---

## What is a container?

A container is any widget that:

- can contain child widgets
- participates in a geometry manager (`pack`, `grid`, or `place`)
- controls spacing and resizing behavior for its children

Common examples:

- [Frame](../widgets/layout/frame.md) / [LabelFrame](../widgets/layout/labelframe.md)
- [PanedWindow](../widgets/layout/panedwindow.md) (resizable regions)
- [ScrollView](../widgets/layout/scrollview.md) (scrollable region)

---

## Container ownership and layout context

Containers define the “layout context” that children live in.

Children:

- request size, but do not enforce it
- inherit geometry constraints from the container
- should not carry layout policy that affects siblings

This separation is what keeps complex layouts predictable.

---

## Single responsibility

Containers work best when they have a clear job.

Good container roles:

- grouping related widgets into a section
- managing spacing for a region
- controlling scrolling / viewport behavior
- defining resize rules (which parts expand vs stay fixed)

Avoid containers that mix unrelated responsibilities (for example: a container that also implements domain logic,
data access, and presentation state).

---

## Composition over per-widget tuning

ttkbootstrap encourages composing layouts from **simple containers** rather than “micro-tuning” each widget.

Instead of:

- adding `padx/pady` everywhere
- manually negotiating which widgets expand
- mixing `pack` and `grid` in the same parent

Prefer:

- containers with clear spacing rules
- nested regions for sections (header/content/footer)
- reusable container patterns

This reduces layout bugs and makes UIs easier to refactor.

See [Layout Properties](../layout-props.md) for the ttkbootstrap layout convenience options used across widgets.

---

## Opinionated layout containers: PackFrame and GridFrame

Tk’s geometry managers are powerful, but verbose:

- you repeat the same spacing and sizing rules across many widgets
- `pack` and `grid` require different mental models and options
- small inconsistencies (padding, sticky/anchor, expand/fill) accumulate

ttkbootstrap provides two *opinionated* containers that make layout intent explicit and consistent:

- **PackFrame** — an opinionated “row/column” pack container with a `direction` and a `gap`
- **GridFrame** — an opinionated grid container with `rows`, `columns`, and `gap` rules

The goal is not to replace Tk’s geometry managers — it’s to make **common layouts faster** and more consistent.

See [PackFrame](../../widgets/layout/packframe.md) and [GridFrame](../../widgets/layout/gridframe.md) for the full usage and examples.

### When should you use them?

- **Use PackFrame** for app-level structure and simple stacking:
  toolbars, sidebars, form sections, button rows, “card” content.
- **Use GridFrame** for structured alignment:
  forms, settings panels, label/value rows, responsive column layouts.

### When should you stick to `pack` / `grid` directly?

- when you’re porting an existing Tk layout and don’t want to refactor yet
- when you need geometry-manager features that are intentionally not surfaced by the opinionated container
- when you’re doing something highly custom and explicit control is clearer than convenience

A good adoption path is:

1. Start with `Frame` + `pack/grid` (familiar and explicit).
2. Introduce `PackFrame` / `GridFrame` where repetition appears.
3. Make them your default for new screens once the team is comfortable.

---

## Nested containers

Nested containers are normal and expected.

However:

- deep nesting increases layout cost
- complex hierarchies are harder to reason about

Balance clarity with simplicity. A useful rule of thumb is to nest to express a meaningful region boundary:
header/content/footer, left/nav/content/right, form section, etc.

---

## Scrollable containers

Scrolling is a **container responsibility**.

A scroll container should:

- manage viewport vs content size
- coordinate scrollbars
- provide consistent mouse wheel behavior
- keep scroll behavior out of child widgets

### ScrollView

`ScrollView` is a canvas-based scrollable container intended for **widget content** (not a text editor or tree).
It hosts **one child widget** (typically a `Frame` that contains your content), and it extends scrolling to all
descendants by injecting a custom bindtag.

Key behaviors:

- Scroll direction: `vertical`, `horizontal`, or `both`
- Scrollbar visibility: `always`, `never`, `on-hover`, or `on-scroll`
- Scrollbars only show when content overflows the viewport
- Mouse wheel works on all descendants (including dynamically added widgets)
- Shift+MouseWheel scrolls horizontally on platforms that support it

See [ScrollView](../../widgets/layout/scrollview.md) for recommended patterns and examples.

---

## Common pitfalls

- **Mixing geometry managers** inside the same parent container (`pack` and `grid` together)
- **Over-nesting** without a clear region boundary
- **Spacing by accident** (random padding values sprinkled everywhere)
- **Scrolling inside children** instead of treating it as a container/viewport concern
- **Querying sizes too early** (before the event loop has realized the layout)

See [Platform → Widget Lifecycle](../../platform/widget-lifecycle.md) for why widget sizes are not reliable until realization.

---

## Next steps

- See [Spacing](spacing.md) for how padding/margins should be applied consistently.
- See [Scrolling](scrolling.md) for scroll patterns and recommendations.
- See [Platform → Geometry & Layout](../../platform/geometry-and-layout.md) for the underlying Tk mechanics.
