---
title: Widgets Overview & Conventions
icon: fontawesome/solid/shapes
---

# Widgets Overview

ttkbootstrap widgets are organized around **desktop UI intent**, not HTML or web form semantics.

This page explains the conventions used throughout the widget documentation.

---

## Controls vs primitives

**Primitives**

- Low-level ttk wrappers
- Minimal UX
- Examples: `Entry`, `Spinbox`, `Scrollbar`

**Controls**

- App-facing widgets
- Validation, labels, messages, events
- Examples: `TextEntry`, `NumericEntry`, `SpinnerEntry`

!!! tip "Rule of Thumb"  
    If you are building a form, prefer controls.

---

## Layout widgets

Layout widgets exist to **structure space**, not collect input.

Examples:

- `Frame`
- `LabelFrame`
- `PanedWindow`
- `ScrollView`

They are typically non-interactive.

---

## Event conventions

ttkbootstrap favors **semantic events**:

- `on_input(...)` → live typing
- `on_changed(...)` → committed value

Avoid raw `bind("<<Changed>>")` unless you need low-level control.

---

## Styling conventions

- Use `bootstyle` for semantic styling
- Avoid hard-coded colors
- Let the theme control contrast and surfaces

---

## Dialog vs Toast vs Tooltip

- **Dialog** → blocking decisions or input
- **Toast** → non-blocking feedback
- **Tooltip** → contextual hints

Choosing the right feedback mechanism improves UX significantly.
