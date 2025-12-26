# Capabilities

Capabilities describe **shared behaviors** that widgets expose in ttkbootstrap.

Rather than documenting behavior repeatedly on every widget, ttkbootstrap
formalizes common Tk/ttk behaviors as *capabilities* that can be mixed into
widgets consistently.

This section explains what capabilities are, why they exist, and how they fit
into the overall framework.

---

## What is a capability?

A capability represents a focused aspect of widget behavior, such as:

- event handling
- layout participation
- focus and grabs
- clipboard access
- validation
- localization

Capabilities:

- mirror underlying Tk/ttk functionality
- provide a consistent Python interface
- integrate with ttkbootstrap conventions

They are not standalone features — they describe **what widgets can do**.

---

## Why capabilities exist

Tk exposes a very large widget API.

Without structure:

- behavior is scattered across widget classes
- documentation becomes repetitive
- shared behavior diverges unintentionally

Capabilities provide:

- a single place to document behavior
- consistent naming and semantics
- clearer mental models for users

---

## Capabilities vs widgets

Widgets describe *what* something is.

Capabilities describe *what it can do*.

For example:

- a Button *is* a widget
- it *has* event handling, focus behavior, and layout participation

Separating these concerns improves clarity.

---

## Mapping to Tk

Most capabilities correspond directly to Tk commands or concepts.

Examples:

- `bind` → event binding
- `after` → deferred execution
- `grab` → modal input handling
- `winfo` → widget introspection

ttkbootstrap does not invent new behavior — it organizes existing behavior.

---

## How capabilities are implemented

Internally, capabilities are implemented as mixins.

Each mixin:

- focuses on a narrow behavior
- delegates to the underlying Tk widget
- documents semantics and edge cases

Widgets compose these mixins to expose a complete API.

---

## Reading capability docs

Capability pages:

- describe behavior conceptually
- explain common pitfalls
- note ttkbootstrap-specific guidance

They are intentionally widget-agnostic.

Use widget docs to see how capabilities are applied in practice.

---

## When to read this section

You should read Capabilities when:

- you want to understand widget behavior deeply
- you need precise control over interaction
- you are debugging complex UI issues
- you are extending or contributing to ttkbootstrap

---

## Next steps

Start with [Signals & Events](signals/index.md) to understand how user interaction flows through ttkbootstrap.

Then explore:

- [Layout Capabilities](layout/index.md) for containers, spacing, and scrolling.
- [Validation](validation/index.md) for input constraints and feedback.
- [Icons & Images](icons/index.md) for visual assets.
