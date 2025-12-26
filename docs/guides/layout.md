---
title: Layout
---

# Layout

This guide explains how to organize widgets on the screen—grouping, alignment, spacing, and resizing using ttkbootstrap's layout containers.

ttkbootstrap takes an **opinionated approach to layout**. Instead of asking you to manage low‑level geometry flags everywhere,
it encourages expressing **layout intent** using purpose‑built containers.

---

## Recommended approach

For most applications, you should start with ttkbootstrap’s layout containers:

- **PackFrame** — for linear layouts (vertical or horizontal)
- **GridFrame** — for structured, row/column layouts

These containers are built on Tk’s geometry managers, but remove much of the repetitive and error‑prone configuration
required when using `pack()` or `grid()` directly.

They are not required — but they are strongly recommended.

---

## Choosing a layout container

### PackFrame

Use **PackFrame** when your layout flows primarily in one direction.

Common examples:

- forms stacked vertically
- horizontal toolbars
- sidebars
- panels with simple ordering

PackFrame lets you describe *what you want*:

- direction (`vertical` or `horizontal`)
- spacing between children
- whether children expand to fill available space

Instead of *how* to pack each widget.

```python
from ttkbootstrap.widgets import PackFrame
import ttkbootstrap as ttk

app = ttk.App()

with PackFrame(app, direction="vertical", gap=8, padding=12):
    ttk.Label(text="Username")
    ttk.Entry()
    ttk.Label(text="Password")
    ttk.Entry()
    ttk.Button(text="Login", bootstyle="primary")

app.mainloop()
```

PackFrame is ideal when alignment between columns is not important.

---

### GridFrame

Use **GridFrame** when widgets need to align across rows and columns.

Common examples:

- label–value forms
- settings panels
- dashboards
- inspector or property views

GridFrame allows you to declare:

- row and column structure
- gaps between rows and columns
- spanning behavior

without manually configuring every cell.

```python
from ttkbootstrap.widgets import GridFrame
import ttkbootstrap as ttk

app = ttk.App()

with GridFrame(app, columns=2, gap=(12, 6), padding=12):
    ttk.Label(text="Name")
    ttk.Entry()

    ttk.Label(text="Email")
    ttk.Entry()

    ttk.Button(text="Save", bootstyle="primary", columnspan=2)

app.mainloop()
```

GridFrame is the recommended choice when visual alignment matters.

---

## Using Frame with pack or grid

Standard Tk layout using `Frame` with `pack()` or `grid()` is fully supported.

You may choose this approach when:

- porting existing Tkinter code
- implementing highly custom geometry behavior
- debugging layout edge cases
- learning or teaching raw Tk geometry

This approach gives you maximum control — but requires deeper knowledge of geometry flags and interactions.

```python
frame = ttk.Frame(app)
frame.pack(fill="both", expand=True)

label = ttk.Label(frame, text="Hello")
label.grid(row=0, column=0, sticky="w", padx=8, pady=4)
```

!!! link "See [Spacing & Alignment](spacing-and-alignment.md) for a deep dive into how `pack`, `grid`, padding, and alignment work in Tk."

---

## Nesting containers

Nested containers are normal and expected.

Use nesting to:

- separate layout regions
- control spacing at the container level
- isolate scrolling or resizing behavior

Prefer **shallow, intentional nesting** over deeply nested widget‑level configuration.

```python
with GridFrame(app, columns=2, gap=12):
    with PackFrame(direction="vertical", gap=6):
        ttk.Label(text="General")
        ttk.Checkbutton(text="Enable feature")

    with PackFrame(direction="vertical", gap=6):
        ttk.Label(text="Advanced")
        ttk.Checkbutton(text="Verbose logging")
```

---

## Scrollable layout

Scrolling is a **container responsibility**, not a widget responsibility.

ttkbootstrap provides composite containers such as `ScrollView` that:

- manage viewport and content sizing
- coordinate scrollbars
- adapt to dynamic content

Widgets placed inside scroll containers should not manage scrolling themselves.

---

## What layout containers do *not* hide

PackFrame and GridFrame do **not** replace Tk’s geometry system.

They:

- sit on top of `pack` and `grid`
- apply structured defaults
- reduce boilerplate

You can always drop down to raw geometry managers when needed.

Understanding the underlying system remains valuable — but it does not need to be your starting point.

---

## Common layout mistakes

- mixing `pack` and `grid` in the same container
- managing spacing on every widget instead of at the container level
- over‑nesting containers without intent
- querying widget size before layout is realized

Most layout issues disappear when containers are used intentionally.

---

## Next steps

- [Spacing & Alignment](spacing-and-alignment.md) - how padding, margins, `sticky`, and expansion
  behave under the hood when using raw `pack` and `grid`.
- [ScrollView](../widgets/layout/scrollview.md) - how scrolling is handled as a container responsibility.

If you’re new to ttkbootstrap layout, start with **PackFrame** or **GridFrame**, then return to Spacing & Alignment
only when you need finer control.
