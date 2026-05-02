# Platform

The **Platform** section explains the runtime model that every ttkbootstrap
application runs on: how the event loop works, how widgets are styled and
laid out, what changes across operating systems, and which tools ship with
the framework.

Platform pages are not widget documentation. They explain the **why** and
the **substrate** — the rules that hold across every widget, dialog, and
window you build.

---

## What ttkbootstrap is (and is not)

ttkbootstrap is **not** just a theme.

It is a framework that provides:

- a structured application runtime (`App`, `AppShell`, `AppSettings`)
- a unified styling and theming system (the `style` package)
- consistent handling of images, fonts, icons, and DPI
- built-in localization and number/date formatting
- predictable interaction, layout, and lifecycle behavior across OSes

ttkbootstrap does **not** replace Tk or ttk. It builds on them and embraces
their strengths, while smoothing over rough edges that show up in real
applications (DPI, dark-mode handoff, missing widgets, scattered
accessibility behaviors, manual theming churn).

---

## When to read this section

Read Platform pages when you want to understand:

- how applications are created, run, and torn down
- how the event loop dispatches events, redraws, and `after`-callbacks
- how widgets are constructed, restyled on theme change, and destroyed
- how layout, geometry propagation, and DPI scaling resolve at runtime
- how behaviors differ across macOS, Windows, and Linux
- how to debug, profile, and ship a finished application

For widget APIs, see [Widgets](../widgets/index.md). For high-level
"how do I build X" recipes, see [Guides](../guides/index.md). For exact
class signatures, see the [API Reference](../reference/index.md).

---

## Relationship to Tk and ttk

Many concepts described here originate in Tk itself: the event loop,
geometry managers, widget lifecycles, virtual events, and windowing
behavior. Where appropriate, these pages reference external resources
such as Python's `tkinter` documentation and the
[TkDocs tutorial](https://tkdocs.com/).

External resources explain *how Tk works*. The Platform section explains
**how ttkbootstrap expects you to work with Tk** — what it adds, what it
constrains, and what it leaves to the underlying toolkit.

---

## Topics

**Fundamentals**

- [Tk vs ttk](tk-vs-ttk.md) — the two widget hierarchies and when each shows up
- [Event Loop](event-loop.md) — `mainloop`, `after`, idle tasks, redraw timing
- [Events & Bindings](events-and-bindings.md) — physical, virtual, and class-level binds
- [Geometry & Layout](geometry-and-layout.md) — `pack` / `grid` / `place` and propagation
- [Widget Lifecycle](widget-lifecycle.md) — construction, restyle, destruction

**Rendering and styling**

- [Styling Internals](ttk-styles-elements.md) — ttk styles, elements, and resolved style names
- [Images & DPI](images-and-dpi.md) — Retina, Windows DPI manifest, X11/Wayland scaling

**System integration**

- [Platform Differences](platform-differences.md) — macOS / Windows / Linux behavior matrix
- [Accessibility](accessibility.md) — keyboard navigation, focus rings, screen reader status
- [Windows](windows.md) — top-levels, modality, frameless, and OS chrome

**Operations**

- [Threading & Async](threading-and-async.md) — worker threads, queues, asyncio integration
- [Debugging](debugging.md) — logging, exception handlers, widget tree dumps
- [Performance](performance.md) — bottleneck patterns and profiling

**Tooling**

- [CLI](cli.md) — `ttkb` commands for scaffolding, running, and inspecting
- [Project Structure](project-structure.md) — recommended layout for a ttkbootstrap app
- [Build & Distribute](build-and-ship.md) — packaging for macOS, Windows, and Linux

---

## Next steps

If you are new to Tk, start with [Tk vs ttk](tk-vs-ttk.md) and
[Event Loop](event-loop.md) — the rest of the section assumes the model
they describe. Experienced Tk developers can jump to
[Platform Differences](platform-differences.md) and
[Styling Internals](ttk-styles-elements.md) for what ttkbootstrap adds on
top.
