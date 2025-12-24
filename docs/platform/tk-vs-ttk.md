# Tk vs ttk

Tkinter exposes two closely related widget systems: **Tk** and **ttk**.
Understanding the distinction between them is critical to using ttkbootstrap effectively.

This page explains what Tk and ttk are, how they differ, and why ttkbootstrap is built
primarily on top of ttk.

---

## What is Tk

Tk is the original widget toolkit underlying Tkinter.

Tk widgets:
- are highly flexible
- expose many low-level configuration options
- are styled largely through direct configuration

Classic Tk widgets include:
- `tk.Label`
- `tk.Button`
- `tk.Entry`
- `tk.Text`

Tk widgets prioritize flexibility over consistency.
Their appearance varies significantly across platforms and themes.

---

## What is ttk

ttk (Themed Tk) is a newer widget set layered on top of Tk.

ttk widgets:
- separate appearance from behavior
- rely on a theme and style engine
- provide more consistent native-looking controls

Common ttk widgets include:
- `ttk.Label`
- `ttk.Button`
- `ttk.Entry`
- `ttk.Treeview`

ttk widgets are styled declaratively through styles rather than direct color settings.

---

## Why ttkbootstrap is ttk-first

ttkbootstrap is designed around ttk because:

- ttk supports a centralized styling system
- themes can be swapped dynamically
- widget appearance is consistent across platforms
- styles can be layered and extended

Most ttkbootstrap widgets are ttk widgets or composites built from ttk primitives.

---

## When Tk widgets are still used

Some Tk widgets have no ttk equivalent or require direct Tk functionality.

Examples include:
- `tk.Canvas`
- `tk.Text`
- low-level drawing or custom rendering

ttkbootstrap supports these widgets but wraps them carefully to integrate with
themes, fonts, and capabilities.

---

## Styling implications

The Tk vs ttk distinction affects how widgets are styled:

- Tk widgets are styled imperatively
- ttk widgets are styled declaratively
- ttk styles are resolved by name, not by instance

ttkbootstrap’s design system builds on ttk’s style model rather than overriding it.

---

## Practical guidance

When building ttkbootstrap applications:

- prefer ttk widgets whenever possible
- use Tk widgets only when necessary
- avoid mixing Tk and ttk styling approaches on the same widget

This keeps applications consistent and themeable.

---

## Next steps

- See **ttk Styles & Elements** for how ttk styling works internally
- See **Platform → Styling** for how ttkbootstrap extends ttk themes
- See **Widgets** for user-facing components built on these systems
