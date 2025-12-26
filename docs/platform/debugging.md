# Debugging

Debugging Tk and ttk applications can feel opaque because much of the behavior
is managed by the Tcl/Tk engine behind the scenes.
However, there are reliable techniques for understanding what the UI is doing
and why.

This page focuses on **practical debugging strategies** for ttkbootstrap applications.

---

## Understand the event loop

Most UI issues are event-loop related.

Symptoms often include:

- UI freezing
- callbacks firing unexpectedly
- layout appearing incorrect until resize

Start by asking:

- *What callback is running?*
- *Is something blocking the event loop?*

Logging entry and exit of callbacks is often revealing.

---

## Use logging liberally

Print statements and logging are effective tools.

Common logging targets:

- widget creation and destruction
- layout changes
- signal emissions
- window lifecycle events

Structured logging helps trace complex UI behavior.

---

## Inspect widget hierarchy

Understanding the widget tree is critical.

Helpful techniques:

- print widget parents and children
- log `winfo_parent()` and `winfo_children()`
- temporarily add borders or background colors

Visualizing structure often reveals layout mistakes.

---

## Verify geometry timing

Many bugs stem from querying geometry too early.

If values seem wrong:

- ensure the event loop has run
- defer logic using `after_idle()`
- avoid size-dependent logic in constructors

Correct timing resolves many layout issues.

---

## Debug styles

Styling bugs are often name-resolution problems.

Tips:

- log the resolved style name
- inspect theme definitions
- verify state transitions (hover, active, disabled)

Remember that styles are resolved dynamically.

---

## Image-related issues

Common image bugs include:

- images disappearing
- incorrect scaling
- excessive memory usage

Check:

- that image objects are kept alive
- whether images are cached
- DPI assumptions

Image bugs often masquerade as layout problems.

---

## Focus and grab issues

If input behaves strangely:

- log focus changes
- verify grab status
- check window ownership

Focus and grab bugs are subtle but diagnosable.

---

## Isolate problems

When debugging complex issues:

- reduce the UI to a minimal example
- remove unrelated widgets
- simplify layout and styles

Small reproductions make issues obvious.

---

## ttkbootstrap-specific guidance

ttkbootstrap provides structure to reduce debugging effort:

- centralized styling
- explicit capabilities
- predictable widget lifecycles

Leaning into these abstractions simplifies diagnosis:

- See [Guides → App Structure](../guides/app-structure.md) for application organization patterns.
- See [Capabilities → Signals](../capabilities/signals/index.md) for reactive state debugging.

---

## Common pitfalls

- assuming synchronous layout
- mixing Tk and ttk styling
- blocking the event loop
- losing references to images

Most bugs fall into a small set of patterns.

---

## Next steps

- See [Performance](performance.md) for responsiveness issues.
- See [Images & DPI](images-and-dpi.md) for rendering bugs.
- See [Capabilities → State & Interaction](../capabilities/state-and-interaction.md) for behavior-specific debugging.
