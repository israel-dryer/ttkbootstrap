---
title: First Application
icon: fontawesome/solid/play
---

# First Application

Your first real application brings together the **application shell**, **layout containers**, and **styled widgets**
into a runnable ttkbootstrap program.

This page walks through the structure of a minimal but realistic application so you can understand *how ttkbootstrap is
meant to be used*, not just how to make something appear on screen.

The goal is clarity and confidence—not completeness.

---

## What This Example Demonstrates

This example shows how ttkbootstrap applications are typically structured:

- a single application entry point,
- a root window managed by the framework,
- container-based layout,
- widgets styled using semantic tokens,
- and theme-aware behavior from the start.

Each of these concepts scales naturally as your application grows.

---

## Anatomy of a ttkbootstrap Application

A ttkbootstrap application is composed of three core layers.

### 1. Application Shell

```python
ttk.App(title="ttkbootstrap 2 First App", theme="solar")
```

The application shell:

- creates the root window,
- applies the initial theme,
- enables DPI awareness,
- and manages application-wide state.

You typically create **one App instance per application**.

---

### 2. Layout Containers

Containers such as `Frame`, `Labelframe`, `ScrollView`, or `PageStack` define **structure**, not appearance.

They:

- control spacing and alignment,
- determine how widgets resize,
- establish focus and navigation boundaries.

Layout is owned by containers, not individual widgets.

---

### 3. Widgets & Content

Widgets provide interaction and presentation.

Inputs, buttons, and indicators:

- inherit the active theme,
- use semantic color and variant tokens,
- remain consistent across the application.

Widgets focus on *what they do*, not *how they are styled*.

---

## A Minimal Working Example

Below is a complete, runnable application that demonstrates these principles.

```python
import ttkbootstrap as ttk

app = ttk.App(title="ttkbootstrap 2 First App", theme="solar")

main = ttk.Frame(app.window, padding=16)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Quick details").grid(
    row=0, column=0, columnspan=2, pady=(0, 10)
)

ttk.Entry(main, bootstyle="info", width=20).grid(
    row=1, column=0, padx=(0, 8)
)

ttk.Button(
    main,
    text="Submit",
    bootstyle="success-outline",
    width=12
).grid(row=1, column=1)

ttk.Progressbar(
    main,
    bootstyle="info-striped",
    mode="indeterminate"
).grid(
    row=2,
    column=0,
    columnspan=2,
    pady=(12, 0),
    sticky="ew"
)

main.columnconfigure((0, 1), weight=1)

app.mainloop()
```

This example intentionally avoids advanced patterns so you can focus on the fundamentals.

---

## Runtime Theming

ttkbootstrap allows themes to be changed at runtime without restructuring the application.

Common operations include:

- Switching to a specific theme:
  ```python
  ttk.set_theme("cosmo")
  ```

- Toggling between light and dark variants:
  ```python
  ttk.toggle_theme()
  ```

- Listing available themes:
  ```python
  ttk.get_themes()
  ```

All widgets automatically update when the theme changes.

---

## Styling Guidance

A few best practices to keep in mind:

- Use **semantic bootstyle tokens** such as `primary`, `success-outline`, or `info-striped` instead of hardcoded colors.
- Let themes and color tokens drive appearance so your UI adapts naturally to theme changes.
- Group related widgets inside containers to manage spacing and alignment consistently.

These conventions keep applications predictable and maintainable.

---

## Where to Go Next

From here, you can:

- Explore **Widgets** to see what components are available.
- Read the **Design System** to understand how layout, color, and typography fit together.
- Follow **Guides** for real-world patterns such as forms, dialogs, and navigation.

Once you understand this basic structure, scaling up becomes straightforward.

---

## Summary

A ttkbootstrap application is built around:

- a single application shell,
- container-driven layout,
- semantic styling,
- and theme-aware behavior.

Mastering this structure early will make the rest of ttkbootstrap easier—and more enjoyable—to use.
