# Scrolling

Scrolling is a layout capability that allows content larger than its viewport
to remain accessible without resizing the entire window.

In Tk, scrolling is not automatic — it must be designed explicitly.
ttkbootstrap formalizes scrolling as a shared layout capability to avoid
repeated, error-prone implementations.

---

## Scrolling as a layout concern

Scrolling is not an attribute of individual widgets.

Instead:

- containers define a viewport
- content defines a scrollable region
- scrollbars reflect and control viewport position

Treating scrolling as a layout capability leads to more predictable behavior.

---

## Scrollable containers

A scrollable container:

- owns the viewport
- tracks content size
- synchronizes scrollbars
- adapts to dynamic content

Widgets inside scroll containers should not manage scrolling directly.

---

## Content size and updates

Scrollable content may change size at runtime.

Correct scrolling behavior requires:

- recalculating scroll regions
- responding to content changes
- updating scrollbars accordingly

Failing to update the scroll region is a common bug.

---

## Vertical and horizontal scrolling

Scrolling may be:

- vertical
- horizontal
- both

Not all content benefits from both directions.

Choose scrolling direction intentionally.

---

## Mouse wheel handling

Mouse wheel behavior:

- varies by platform
- must be bound explicitly
- interacts with focus and grabs

ttkbootstrap provides standardized patterns to normalize scrolling behavior
across platforms.

---

## Performance considerations

Scrolling performance depends on:

- number of visible widgets
- redraw cost
- layout complexity

Efficient scrolling favors:

- reusing widgets
- minimizing redraws
- avoiding deep hierarchies

---

## ttkbootstrap guidance

ttkbootstrap encourages:

- using provided scroll container patterns
- centralizing scroll logic
- avoiding custom per-widget scrolling
- testing scrolling on all target platforms

These practices improve consistency and usability.

---

## Common pitfalls

- attaching scrollbars directly to content widgets
- forgetting to update scroll regions
- binding mouse wheel events inconsistently
- scrolling large widget trees inefficiently

Understanding scrolling mechanics helps avoid these issues.

---

## Next steps

- See [Containers](containers.md) for layout composition.
- See [Spacing](spacing.md) for layout density considerations.
- See [Platform → Geometry & Layout](../../platform/geometry-and-layout.md) for underlying mechanics.
