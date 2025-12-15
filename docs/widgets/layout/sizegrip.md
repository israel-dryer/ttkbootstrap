---
title: SizeGrip
icon: fontawesome/solid/expand
---

# SizeGrip

`SizeGrip` is a themed wrapper around `ttk.Sizegrip` that provides a small “resize handle” typically placed in the bottom-right corner of a window. It gives users an obvious affordance for resizing, especially in traditional desktop layouts.

<!--
IMAGE: SizeGrip in a status bar
Suggested: A window with a bottom status bar, SizeGrip aligned bottom-right
Theme variants: light / dark
-->

---

## Basic usage

A common pattern is to place a `SizeGrip` in a bottom “status bar” frame and align it to the right.

```python
import ttkbootstrap as ttk

app = ttk.App()

app.geometry("500x350")

content = ttk.Frame(app, padding=10)
content.pack(fill="both", expand=True)

status = ttk.Frame(app, padding=(10, 6))
status.pack(fill="x", side="bottom")

ttk.Label(status, text="Ready").pack(side="left")
ttk.SizeGrip(status).pack(side="right")

app.mainloop()
```

<!--
IMAGE: Basic SizeGrip example
Suggested: Status bar with “Ready” text and SizeGrip at the far right
-->

---

## What problem it solves

Some users expect a visible resize handle—especially on classic Windows-style UIs or when window borders are subtle. `SizeGrip` helps by:

- Making the resize affordance obvious
- Providing a consistent, theme-aware look via ttkbootstrap `bootstyle`
- Offering a small, unobtrusive control that fits naturally in status bars

---

## Core concepts

### Placement matters

`SizeGrip` is only useful if it is placed where users expect it:

- Bottom-right of the window (most common)
- Bottom-left in RTL layouts or certain UI conventions

It does not manage layout for you; it’s simply a widget you place like any other.

---

### Works best with resizable windows

If your window is not resizable, a size grip is misleading. Ensure the top-level is resizable:

```python
app.resizable(True, True)
```

(Resizability also depends on platform window manager behavior.)

---

## Common options & patterns

### Styling with bootstyle

Apply a semantic style token:

```python
ttk.SizeGrip(status, bootstyle="secondary")
```

If you provide an explicit ttk style name via `style=...`, it overrides `bootstyle`.

<!--
IMAGE: SizeGrip style variants
Suggested: Same SizeGrip rendered under different bootstyles (if theme supports it)
-->

---

### Embedding in complex footers

You can include the size grip alongside other footer widgets (progress, connection status, etc.). Just keep spacing and alignment consistent:

```python
footer = ttk.Frame(app, padding=(10, 6))
footer.pack(fill="x", side="bottom")

left = ttk.Frame(footer)
left.pack(side="left")

right = ttk.Frame(footer)
right.pack(side="right")

ttk.Label(left, text="Connected").pack(side="left")
ttk.SizeGrip(right).pack(side="right")
```

---

## Events

`SizeGrip` is typically interacted with via mouse drag; you generally do not bind events to it directly.

---

## UX guidance

- Use a size grip only when resizing is expected and helpful
- Prefer placing it inside a status bar/footer rather than floating in content
- Avoid it in modern, borderless, or highly stylized UIs where a resize handle may feel out of place

!!! tip "Don’t double up affordances"
    If your window chrome already clearly communicates resizability, a size grip may be redundant. Use it primarily when you want an explicit, discoverable resize control.

---

## When to use / when not to

**Use SizeGrip when:**

- You have a status bar/footer and want a clear resize affordance
- Your UI targets traditional desktop expectations
- Window borders are subtle and resizing is easy to miss

**Avoid SizeGrip when:**

- The window is fixed-size
- The app uses custom borderless windows or custom resizing behaviors
- The UI already has strong resize affordances

---

## Related widgets

- **Frame** — often used for status bars and footers
- **Separator** — subtle division above a status bar
- **PanedWindow** — user-resizable layout inside the window
