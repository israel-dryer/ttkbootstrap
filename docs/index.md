---
title: Home
---

# ttkbootstrap

**ttkbootstrap** is a **modern, opinionated desktop UI framework for Python**, built on top of Tk.

It provides clear conventions for **layout**, **styling**, **state**, and **reactivity**, allowing you to build
polished, maintainable desktop applications without reinventing common UI patterns.

ttkbootstrap is designed to feel familiar to Tk users—but it goes far beyond theming or widget wrappers.

---

## What ttkbootstrap is

ttkbootstrap is a **framework**, not just a toolkit.

It provides:

- a structured application root (`App`)
- container-first layout patterns
- a design system with semantic colors, variants, and typography
- optional reactivity via signals
- integrated localization, icons, and styling conventions

These pieces work together to support **modern application workflows**, not just individual widgets.

---

## What ttkbootstrap is not

ttkbootstrap is **not**:

- a thin skin on top of Tkinter
- a collection of unrelated helper widgets
- a low-level “figure it out yourself” UI layer

You *can* adopt ttkbootstrap incrementally, but its real value appears when you follow its conventions for
layout, styling, and state.

---

## Core ideas

### Opinionated, but flexible

ttkbootstrap makes intentional choices about how applications are structured.
These opinions reduce boilerplate and ambiguity while still allowing escape hatches when needed.

### Containers express layout intent

Layout is driven by **containers**, not scattered geometry calls.
Spacing, alignment, scrolling, and resizing are handled at the container level.

### Styling is semantic

Widgets are styled using **semantic tokens**—not hardcoded colors or fonts.
This keeps applications consistent across themes and appearance modes.

### Reactivity is optional and explicit

Signals, callbacks, and events coexist.
Use simple callbacks when that’s enough; introduce signals when state needs to flow.

---

## How the documentation is organized

The documentation is structured by **intent**, not by inheritance or module layout.

### Getting Started

Learn how to create your first ttkbootstrap application and understand the core mental model.

→ [Start here if you’re new](getting-started/index.md)

### Guides

Workflow-oriented documentation that shows **how to build real applications**:
layout patterns, reactivity, styling, localization, and structure.

### Widgets

Practical documentation for each widget:
when to use it, how it behaves, and how it fits into the framework.

### Design System

Semantic colors, variants, typography, icons, and theming—how visual consistency is achieved.

### Platform

How Tk and ttk work under the hood.
This section explains behavior, constraints, and mechanics—not usage patterns.

### Capabilities

Framework features such as signals, localization, layout properties, and state handling.
These pages explain **what a capability is**, not how to apply it in an app.

### API Reference

Complete, auto-generated reference for classes, methods, and functions.

---

## Where to start

If you’re new to ttkbootstrap:

1. Begin with **Getting Started**
2. Read the **Guides** relevant to your task
3. Refer to **Widgets** for specifics
4. Use **Platform** and **Capabilities** when you need deeper understanding

If you already know Tkinter, resist the urge to jump straight to the API—ttkbootstrap rewards learning its
structure first.

---

## Philosophy

ttkbootstrap exists to make **desktop UI development productive again**.

It embraces the stability of Tk while adding the structure, consistency, and ergonomics expected from
modern UI frameworks.

If you follow its conventions, you’ll write less code, debug fewer layout issues, and ship more cohesive
applications.
