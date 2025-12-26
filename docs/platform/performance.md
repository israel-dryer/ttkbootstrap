# Performance

Tk is a single-threaded, event-driven UI toolkit.
Understanding where performance costs come from — and how to avoid common traps —
is essential for building responsive ttkbootstrap applications.

This page explains performance considerations at the platform level.

---

## The event loop model

Tk processes all UI work on a single event loop.

This includes:

- handling user input
- redrawing widgets
- running callbacks
- resolving layout

Any long-running operation blocks the event loop and freezes the UI.

---

## Avoid blocking the event loop

Operations that should **not** run directly in callbacks include:

- long computations
- blocking I/O
- network requests
- large file reads

Instead, offload work to:

- background threads
- subprocesses
- incremental callbacks using `after()`

The UI should remain responsive at all times.

---

## Layout cost

Layout resolution is not free.

Costs increase with:

- deeply nested widget hierarchies
- frequent geometry changes
- repeated calls to geometry managers

ttkbootstrap encourages:

- container-based layout
- minimizing unnecessary relayouts
- batching layout changes where possible

See [Guides → Layout](../guides/layout.md) for layout patterns that minimize overhead.

---

## Image and font performance

Images and fonts are relatively expensive resources.

Performance tips:

- cache images instead of recreating them
- reuse named fonts
- avoid repeated image scaling

ttkbootstrap’s Image and typography systems exist partly to address these concerns.

---

## Redraw frequency

Widgets may redraw in response to:

- state changes
- size changes
- style changes

Excessive redraws can impact performance, especially on lower-powered systems.

Avoid unnecessary state toggling or style recomputation.

---

## Measuring performance

Useful techniques include:

- logging callback execution time
- temporarily disabling expensive UI updates
- isolating layout-heavy sections

Performance issues are often localized and can be addressed incrementally.

---

## ttkbootstrap guidance

ttkbootstrap promotes the following performance practices:

- keep callbacks short
- cache reusable resources
- prefer declarative layout patterns
- avoid deep widget trees

Following these patterns helps maintain responsiveness.
See [Guides → App Structure](../guides/app-structure.md) for application organization.

---

## Common pitfalls

- performing blocking work in callbacks
- rebuilding widgets unnecessarily
- excessive image recreation
- uncontrolled layout thrashing

Understanding the event loop model is key to avoiding these issues.

---

## Next steps

- See [Debugging](debugging.md) for diagnosing performance problems.
- See [Capabilities → Signals](../capabilities/signals/index.md) for coordinating background work.
- See [Images & DPI](images-and-dpi.md) for image performance considerations.
