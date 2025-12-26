---
title: Spacing & Alignment
---

# Spacing & Alignment

This guide explains the underlying layout model for spacing and alignment—how widgets occupy space inside a container and how they respond when that space changes.

In ttkbootstrap, most layouts should be expressed using higher-level containers like `PackFrame` and `GridFrame`, which centralize spacing rules and reduce per-widget configuration. This guide is for when you need to reason about layout behavior directly—especially when working with `Frame`, debugging complex layouts, or integrating legacy Tk code.

---

## First: when you *don’t* need this

If you are using:

- `PackFrame` with `gap`
- `GridFrame` with `gap`, row/column definitions
- standard ttkbootstrap layout patterns

Then you typically **do not need to manage spacing manually**.

!!! link "See [Layout → Containers](containers.md) for recommended layout containers and patterns."

---

## The spacing model (mental model)

Tk layout spacing is controlled by **two kinds of padding** and **one alignment rule**.

### External padding (`padx`, `pady`)

External padding adds space **outside** the widget.

- affects distance between siblings
- controlled by the geometry manager
- belongs conceptually to the *container*

```text
[ padding ][ widget ][ padding ]
```

---

### Internal padding (`ipadx`, `ipady`)

Internal padding adds space **inside** the widget.

- increases the widget’s visual size
- does not affect neighboring widgets
- belongs conceptually to the *widget*

```text
[ widget ( inner space ) ]
```

---

### Alignment (unused space)

When a container has extra space, alignment rules determine:

- where the widget is placed
- whether it stretches
- how it reacts to resizing

This behavior differs by geometry manager.

---

## Alignment with `grid`

The `grid` geometry manager uses **cells**.

### `sticky`

`sticky` controls which sides of the cell a widget adheres to.

- `"w"` → left
- `"e"` → right
- `"n"` → top
- `"s"` → bottom
- combinations stretch (`"ew"`, `"ns"`, `"nsew"`)

```python
ttk.Entry(frame).grid(row=0, column=1, sticky="ew")
```

### Row and column weights

Grid expansion is controlled by **row and column weights**, not the widget.

```python
frame.columnconfigure(1, weight=1)
```

Without weight, widgets will not expand—even if `sticky="ew"` is set.

---

## Alignment with `pack`

The `pack` geometry manager is **order-based**.

### `side`

Controls where widgets are placed relative to the container.

- `"top"` / `"bottom"`
- `"left"` / `"right"`

```python
ttk.Button(frame, text="OK").pack(side="right")
```

---

### `fill` and `expand`

- `fill` controls **stretch direction**
- `expand` controls **whether extra space is assigned**

```python
ttk.Frame(frame).pack(fill="x", expand=True)
```

---

## Why spacing becomes confusing

Spacing rules are split across:

- the container
- the child widget
- the geometry manager
- implicit defaults

This makes it easy to:

- repeat `padx/pady` everywhere
- forget where expansion is controlled
- fight layout instead of expressing intent

---

## Why ttkbootstrap introduces layout containers

ttkbootstrap promotes **centralized spacing decisions**.

### Instead of repeating spacing:

```python
ttk.Label(f, text="Name").grid(padx=8, pady=4)
ttk.Entry(f).grid(padx=8, pady=4)
```

### Prefer container-defined spacing:

```python
with ttk.GridFrame(parent, columns=2, gap=8):
    ttk.Label(text="Name")
    ttk.Entry()
```

Benefits:

- consistent spacing
- fewer layout bugs
- clearer intent
- easier refactoring

!!! link "See [Layout → Containers](containers.md) for `PackFrame` and `GridFrame` usage."

---

## When to manage spacing manually

Manual spacing is appropriate when:

- integrating existing Tk layouts
- building custom composite widgets
- debugging unexpected geometry behavior
- implementing specialized layouts

In these cases, understanding the underlying model is essential.

---

## Common pitfalls

- mixing geometry managers in the same container
- using `ipadx/ipady` to fix alignment issues
- expecting widgets to expand without container weights
- encoding layout rules into widgets instead of containers

---

## Summary

- Spacing is a **layout concern**, not styling
- Most apps should centralize spacing using layout containers
- Understanding spacing helps you reason about layout behavior
- ttkbootstrap abstractions exist to reduce geometry noise—not hide it

---

## Next steps

- [Layout](layout.md) - how spacing and alignment concepts are applied using
  **PackFrame** and **GridFrame**.

- [PackFrame](../widgets/layout/packframe.md) - how `gap`, padding, and expansion
  replace most `padx`, `pady`, and `fill` usage.

- [GridFrame](../widgets/layout/gridframe.md) - how row/column gaps,
  spanning, and alignment simplify `sticky`, `rowconfigure`, and `columnconfigure`.

- [ScrollView](../widgets/layout/scrollview.md) - how spacing interacts with
  scrolling containers and dynamic content.

If you are working directly with `Frame` and raw `pack()` / `grid()`, keep this page bookmarked —
it explains the underlying mechanics that PackFrame and GridFrame build upon.


