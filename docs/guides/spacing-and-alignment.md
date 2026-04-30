---
title: Spacing & Alignment
---

# Spacing & Alignment

This guide explains the underlying mental model for spacing and alignment in
Tk — how widgets occupy space inside a container and how they respond when
that space changes. It's the reference for when you reach below the
ttkbootstrap layout helpers.

For the recommended way to lay out a ttkbootstrap app — `PackFrame`,
`GridFrame`, and the `gap`/`padding` model — see the [Layout](layout.md)
guide. For the design rationale behind spacing as a layout concern see
[Capabilities → Layout → Spacing](../capabilities/layout/spacing.md).

---

## When you don't need this page

If you can express your layout with `PackFrame` or `GridFrame` plus their
`gap=` and `padding=` options, you don't need to read further. Those
containers absorb the bookkeeping this page describes.

You need this page when you're:

- working directly with `Frame` and raw `pack()` / `grid()`
- porting Tk code that already encodes geometry per child
- building custom composite widgets that manage their own layout
- debugging a layout that isn't behaving the way you expect

In every other case, reach for the higher-level containers first.

---

## The model: two paddings and one alignment rule

Tk layout spacing reduces to three concepts:

1. **External padding** — space between a widget and its neighbours.
2. **Internal padding** — extra space inside the widget itself.
3. **Alignment** — what a widget does with the leftover space in its slot.

That's it. Every spacing knob is one of those three.

### External padding (`padx`, `pady`)

External padding is space added *around* a widget by its geometry manager. It
pushes neighbours apart but doesn't affect the widget's own size.

```text
[ pad ][ widget ][ pad ]
```

Conceptually it belongs to the *container* — it describes "how far apart do
my children sit". The values can be a single integer (symmetric) or a
`(left, right)` tuple for asymmetric spacing.

### Internal padding (`ipadx`, `ipady`)

Internal padding is space added *inside* the widget by the geometry manager.
The widget grows, its neighbours don't move.

```text
[ widget(  inner  )]
```

Conceptually this belongs to the *widget* — it's "how much breathing room
does this thing's content have". You'll meet it on buttons and labels far
more than on frames.

### Alignment

When a slot is bigger than the widget that occupies it, alignment decides
what happens to the leftover space. The rules differ by geometry manager —
`grid` uses `sticky`, `pack` uses `side` plus `fill` and `expand`.

---

## Alignment with `grid`

`grid` arranges widgets into rows and columns. Each child occupies one or
more cells.

### `sticky`: which sides the widget hugs

`sticky` is a string of compass directions. The widget hugs the named sides
of its cell, stretching when it has to:

- `"w"` / `"e"` / `"n"` / `"s"` — single edge
- `"ew"` / `"ns"` — stretch in one axis
- `"nsew"` — fill the cell

```python
ttk.Entry(frame).grid(row=0, column=1, sticky="ew")
```

Without `sticky`, a widget sits centered in its cell at its requested size.

### Row and column weights

By default, grid rows and columns shrink to fit their content. If you want a
column to absorb extra space when the container is resized, you have to give
it weight:

```python
frame.columnconfigure(1, weight=1)
```

Without weight, even a `sticky="ew"` widget won't grow — there's no extra
space to stretch into.

This catches everyone the first time. The widget says "I want to stretch",
the cell says "there's nothing to stretch into" because the column has no
weight, and the result is a static layout that looks broken.

---

## Alignment with `pack`

`pack` is order-based: widgets are placed against one side of the container
in the order they're packed.

### `side`

Picks which edge the next widget docks against:

- `"top"` (default) — stack downward
- `"bottom"`
- `"left"` / `"right"` — stack horizontally

```python
ttk.Button(frame, text="OK").pack(side="right")
```

### `fill` and `expand`

These are the alignment knobs:

- `fill` — stretch the widget across its slot. `"x"`, `"y"`, `"both"`,
  or `"none"`.
- `expand` — claim a share of any leftover space in the container.

The two are independent. `fill="x"` without `expand=True` stretches the
widget to the container's current width but doesn't grow when the window is
resized. `expand=True` without `fill` reserves space but leaves the widget at
its requested size, centered in that space.

```python
ttk.Frame(frame).pack(fill="both", expand=True)
```

That combination — fill in both directions and claim leftover space — is the
classic "make this child take everything" pattern.

---

## Why this gets confusing

Tk spreads the rules across four places: the container, the child, the
geometry manager, and implicit defaults. The same visual effect is reachable
through several different settings, which means problems are usually
*compositional* — the values are individually fine but interact badly.

Common trouble spots:

- **`padx`/`pady` repeated on every child** — fragile and hard to update.
- **Forgetting column or row weights** — `sticky="ew"` does nothing.
- **Mixing geometry managers in one container** — Tk forbids it; you'll
  get either an error or silent wrongness.
- **Treating `ipadx`/`ipady` as a positioning fix** — they grow the
  widget instead of moving it.

---

## How ttkbootstrap helps

`PackFrame` and `GridFrame` move the spacing decisions onto the container.
You declare *once* what the gap and padding should be, and children just call
`pack()` or `grid()` with no arguments.

Without a layout container:

```python
ttk.Label(f, text="Name").grid(padx=8, pady=4, sticky="e")
ttk.Entry(f).grid(padx=8, pady=4, sticky="ew")
```

With one:

```python
form = ttk.GridFrame(parent, columns=2, gap=8, padding=12)
ttk.Label(form, text="Name").grid()
ttk.Entry(form).grid(sticky="ew")
```

Per-call options still work as overrides. The container provides defaults; a
child that needs something different sets it directly.

The benefits compound:

- spacing changes are one-line edits
- intent reads off the container, not the children
- layout consistency falls out automatically
- the children stop carrying geometry boilerplate

See [Layout](layout.md) for the recommended composition patterns.

---

## When manual spacing is the right tool

Reach for raw `pack()` / `grid()` and explicit padding when:

- you're porting Tk code and don't want to refactor the layout yet
- you're inside a custom widget that owns its own layout
- you've hit an edge case the helpers don't cover and need the escape hatch
- you're diagnosing geometry behaviour and stripping abstractions away

In those cases, the model in this page is exactly what you need.

---

## Summary

- Spacing is a layout concern, not a styling one.
- Two paddings (`padx`/`pady` outside, `ipadx`/`ipady` inside) plus one
  alignment rule per geometry manager covers everything.
- Most apps should let `PackFrame` and `GridFrame` carry the spacing.
- Drop down to manual spacing when you're integrating, customising, or
  debugging — and remember the model when you do.

---

## Next steps

- [Layout](layout.md) — putting `PackFrame` and `GridFrame` together
  in a real app.
- [PackFrame](../widgets/layout/packframe.md) — the linear-layout
  container; `gap`, `direction`, `fill_items`.
- [GridFrame](../widgets/layout/gridframe.md) — the grid-layout
  container; `gap`, `rows`, `columns`, `sticky_items`, auto-placement.
- [ScrollView](../widgets/layout/scrollview.md) — how spacing interacts
  with scrollable regions.
- [Capabilities → Layout → Spacing](../capabilities/layout/spacing.md) —
  the design rationale behind container-driven spacing.
