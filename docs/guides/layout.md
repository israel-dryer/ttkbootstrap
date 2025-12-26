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
import ttkbootstrap as ttk

app = ttk.App()

form = ttk.PackFrame(app, direction="vertical", gap=8, padding=12)
form.pack(fill="both", expand=True)

form.add(ttk.Label(form, text="Username"))
form.add(ttk.Entry(form))
form.add(ttk.Label(form, text="Password"))
form.add(ttk.Entry(form, show="*"))
form.add(ttk.Button(form, text="Login", bootstyle="primary"))

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
import ttkbootstrap as ttk

app = ttk.App()

grid = ttk.GridFrame(app, columns=["auto", 1], gap=(12, 6), padding=12, sticky_items="ew")
grid.pack(fill="both", expand=True)

grid.add(ttk.Label(grid, text="Name"), row=0, column=0, sticky="e")
grid.add(ttk.Entry(grid), row=0, column=1)

grid.add(ttk.Label(grid, text="Email"), row=1, column=0, sticky="e")
grid.add(ttk.Entry(grid), row=1, column=1)

grid.add(ttk.Button(grid, text="Save", bootstyle="primary"), row=2, column=0, columnspan=2, sticky="e")

app.mainloop()
```

GridFrame is the recommended choice when visual alignment matters.

!!! note "Use add() for GridFrame features"
    GridFrame's `gap` and `sticky_items` only apply when using `grid.add(widget, ...)`.
    Direct `.grid()` calls bypass these features.

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
grid = ttk.GridFrame(app, columns=[1, 1], gap=12, padding=12, sticky_items="nsew")
grid.pack(fill="both", expand=True)

# Left column
left = ttk.PackFrame(grid, direction="vertical", gap=6)
grid.add(left, row=0, column=0)
left.add(ttk.Label(left, text="General", font=("", 10, "bold")))
left.add(ttk.CheckButton(left, text="Enable feature"))

# Right column
right = ttk.PackFrame(grid, direction="vertical", gap=6)
grid.add(right, row=0, column=1)
right.add(ttk.Label(right, text="Advanced", font=("", 10, "bold")))
right.add(ttk.CheckButton(right, text="Verbose logging"))
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
