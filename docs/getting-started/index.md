# Getting Started

This section helps you get productive with ttkbootstrap quickly—without requiring deep knowledge
of Tkinter or ttk internals.

ttkbootstrap is a **framework**, not just a styling layer. The recommended approach is to embrace
its defaults and patterns rather than treating it like raw tkinter.

---

## The ttkbootstrap mindset

When using ttkbootstrap, you should expect:

- **Opinionated defaults**  
  Fonts, colors, spacing, and widget behavior are chosen for you.

- **Declarative configuration**  
  Express intent in constructors and configuration objects rather than imperative mutation.

- **Reactive interaction**  
  Signals and events drive UI updates and behavior.

- **Consistent patterns**  
  Widgets, dialogs, forms, and layouts follow shared conventions.

This mindset leads to simpler, more maintainable applications.

---

## What you don’t need to know (to get started)

You do *not* need to:

- understand ttk layout elements
- manually manage widget state flags
- build your own validation systems
- invent icon or image handling
- deeply study the Tk event loop

These concerns are handled—or at least structured—by the framework so you can focus on building
your application first. You can always dive deeper later if needed.

---

## Typical workflow

A typical ttkbootstrap application looks like this:

1. Create an application (`App`)
2. Choose a theme and configuration
3. Compose widgets using framework components
4. Connect behavior with signals and callbacks
5. Validate input and manage state declaratively
6. Package and distribute

Each step is explicitly supported by the framework and explored in more depth throughout the documentation.

---

## How this section is organized

- [Installation](installation.md) — installing ttkbootstrap
- [Quick Start](quick-start.md) — building a minimal application

After that, explore:

- [Guides](../guides/index.md) — practical how-to guides for common tasks
- [Widgets](../widgets/index.md) — discovering available components
- [Platform](../platform/index.md) — understanding the foundations (optional but useful)
- [Capabilities](../capabilities/index.md) — learning the framework’s core features

When you're ready to ship:

- [Project Structure](../platform/project-structure.md) — organizing real-world apps
- [Build & Distribute](../platform/build-and-ship.md) — packaging applications

---

## Next steps

- Follow the [Quick Start](quick-start.md) to build your first app
- Read the [Guides](../guides/index.md) to learn recommended patterns
- Browse [Widgets](../widgets/index.md) to see what’s available
