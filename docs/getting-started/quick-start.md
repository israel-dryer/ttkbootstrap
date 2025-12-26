---
title: Quick Start
---

# Quick Start

This guide gets you from **zero to a running ttkbootstrap app** in just a few minutes.

The goal is not to explain everything — it’s to help you see how ttkbootstrap
applications are *structured* and *feel* different from raw tkinter.

---

## Create your first app

A ttkbootstrap application starts with an `App`, not a bare `Tk` instance.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Quick Start")

app.mainloop()
```

If you run this, you already have:

- a themed application window
- automatic light/dark awareness (depending on theme)
- a framework-managed lifecycle

---

## Add content with intent

Instead of placing widgets directly on the root window, you typically use
**containers** to express layout intent.

Here’s a simple example using a `Frame`:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Quick Start")

container = ttk.Frame(app, padding=20)
container.pack(fill="both", expand=True)

ttk.Label(container, text="Welcome to ttkbootstrap").pack(pady=(0, 10))
ttk.Button(container, text="Continue", bootstyle="primary").pack()

app.mainloop()
```

You now have:

- spacing controlled by the container
- consistent typography and colors
- a semantic action button (`primary`)

---

## What just happened?

Even in this small example, ttkbootstrap is doing more than tkinter:

- **Design system**
  - semantic colors (`primary`)
  - consistent spacing and typography
- **Layout responsibility**
  - containers manage spacing and resizing
- **Framework defaults**
  - sensible padding, focus behavior, and state visuals

You didn’t have to configure any of that manually.

---

## Recommended next steps

This Quick Start shows *what* to do — not *why*.

To keep building with confidence, continue here:

- **[Guides → App Structure](../guides/app-structure.md)**  
  How applications are organized (windows, layout, state)

- **[Guides → Layout](../guides/layout.md)**  
  When to use `Frame`, `PackFrame`, and `GridFrame`

- **[Widgets](../widgets/index.md)**  
  Explore available widgets and controls

If you prefer learning by examples, head straight to the **Guides**.

---

## A note for tkinter users

If you’re coming from tkinter:

- You can still use familiar widgets and geometry managers
- But ttkbootstrap works best when you:
  - let containers manage layout
  - rely on semantic styling instead of manual colors
  - treat the app as a cohesive system, not a script

You don’t have to relearn everything — but you *do* get better defaults.
