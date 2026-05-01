---
title: PackFrame
---

# PackFrame

`PackFrame` is a `Frame` subclass that auto-applies pack defaults to
its children. You configure direction, gap spacing, and default
fill/expand/anchor on the container; children call the standard
`pack()` method and inherit those defaults without any per-call
boilerplate.

PackFrame intercepts `pack()` and `pack_forget()` on its children, so
children's plain calls — `Button(stack).pack()` — flow through a
container hook (`_on_child_pack`) that injects the right `side`,
applies the inter-item gap as `padx`/`pady`, and tracks the widget so
gaps stay consistent when items are added or removed. As a `Frame`
subclass, PackFrame inherits the full theming surface (`surface`,
`show_border`, `input_background`) and the runtime surface cascade.

<figure markdown>
![packframe](../../assets/dark/widgets-packframe.png#only-dark)
![packframe](../../assets/light/widgets-packframe.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PackFrame(app, direction="vertical", gap=8, padding=20)
stack.pack(fill="both", expand=True)

ttk.Button(stack, text="First").pack()
ttk.Button(stack, text="Second").pack()
ttk.Button(stack, text="Third").pack()

app.mainloop()
```

Each button's plain `pack()` is intercepted by the PackFrame: the
first button gets `side="top"`; the second and third get `side="top"`
plus `pady=(8, 0)` for the gap.

---

## Layout model

PackFrame imposes single-axis pack on its children. The container's
`direction` selects the pack `side`; the order of `pack()` calls is
the visual order along that axis.

**Direction → side mapping.** Six aliases collapse to four pack sides:

| `direction`         | Pack `side` | Visual order            |
| ------------------- | ----------- | ----------------------- |
| `"vertical"`        | `"top"`     | first-added at the top  |
| `"column"`          | `"top"`     | first-added at the top  |
| `"column-reverse"`  | `"bottom"`  | first-added at the bottom |
| `"horizontal"`      | `"left"`    | first-added on the left |
| `"row"`             | `"left"`    | first-added on the left |
| `"row-reverse"`     | `"right"`   | first-added on the right |

The CSS-flexbox-style names (`row`, `column`, `*-reverse`) are
aliases for the Tk-style names — pick whichever vocabulary fits.

**Gap is between-items.** When `gap > 0`, every child after the first
gets a leading `padx` (horizontal directions) or `pady` (vertical
directions) equal to `gap`. The first child has no leading gap; no
trailing gap is added after the last child. This means inserting or
removing an item triggers a full repack so the gap shift cleanly.

```python
stack = ttk.PackFrame(app, direction="vertical", gap=12)
ttk.Label(stack, text="A").pack()  # pady=0
ttk.Label(stack, text="B").pack()  # pady=(12, 0)
ttk.Label(stack, text="C").pack()  # pady=(12, 0)
```

**Default `fill`/`expand`/`anchor`.** Set `fill_items`,
`expand_items`, or `anchor_items` on the container and every
managed child inherits them at `pack()` time:

```python
form = ttk.PackFrame(app, direction="vertical", gap=8, fill_items="x")

ttk.Entry(form).pack()           # fill="x"
ttk.Entry(form).pack()           # fill="x"
ttk.Button(form, text="OK").pack(fill="none", anchor="e")  # override
```

Per-call `pack()` options always override container defaults, so a
single child can opt out of the inherited fill or anchor. Note that
**overriding `side` on a single child will break the layout** — the
container's gap math assumes every managed child uses the
direction's pack side.

**`before=` and `after=`.** PackFrame respects the standard `pack()`
positioning kwargs, but the reference widget must already be managed
by this PackFrame:

```python
first = ttk.Label(stack, text="First")
first.pack()
last = ttk.Label(stack, text="Last")
last.pack()

# Insert between them
ttk.Label(stack, text="Middle").pack(after=first)
```

**Scope.** PackFrame only manages widgets that call `pack()` on
themselves; children that use `grid()` or `place()` flow through the
default geometry managers untouched. Mixing geometry managers inside
a single PackFrame is allowed but bypasses the gap and default-fill
behavior for the non-pack children.

---

## Common options

PackFrame extends Frame's option set with six layout-shaping
parameters:

| Option           | Type            | Default      | Notes                                                           |
| ---------------- | --------------- | ------------ | --------------------------------------------------------------- |
| `direction`      | str             | `"vertical"` | One of `vertical`, `horizontal`, `row`, `column`, `row-reverse`, `column-reverse` |
| `gap`            | int             | `0`          | Pixel spacing applied to every child after the first            |
| `fill_items`     | str \| None     | `None`       | Default `fill` for all children: `"none"`, `"x"`, `"y"`, `"both"` |
| `expand_items`   | bool \| None    | `None`       | Default `expand` for all children                               |
| `anchor_items`   | str \| None     | `None`       | Default `anchor` for all children (`"n"`, `"ne"`, …, `"center"`) |
| `propagate`      | bool \| None    | `None`       | If `False`, calls `pack_propagate(False)` so the frame honors `width`/`height` |
| `padding`        | int \| tuple    | `0`          | Inner spacing inside the PackFrame                              |
| `width`          | int             | natural      | Requested width in pixels (see `propagate`)                     |
| `height`         | int             | natural      | Requested height in pixels (see `propagate`)                    |
| `surface`        | str             | `"background"` | Surface token: `chrome`, `content`, `card`, `overlay`, `input` |
| `show_border`    | bool            | `False`      | Draws a 1px theme-aware border                                  |
| `input_background` | str           | `"content"`  | Surface token cascaded to input descendants                     |
| `accent`         | str             | —            | Accepted; on container classes the bootstyle constructor wrapper rewrites it as a `surface` override |

A `None` default for `fill_items`, `expand_items`, or `anchor_items`
means "don't inject a default" — children fall back to Tk's
standard pack defaults (`fill="none"`, `expand=False`,
`anchor="center"`).

---

## Behavior

**Pack interception.** PackFrame implements `_on_child_pack` and
`_on_child_pack_forget`, the hooks the framework's `PackMixin`
calls on the parent before delegating to Tk. Any ttkbootstrap widget
packed into a PackFrame flows through those hooks; raw `tkinter`
widgets without `PackMixin` skip the hooks and use the unmanaged
defaults.

**Runtime reconfigure.** `direction` and `gap` are wired through
configure-delegate hooks, so `stack.configure(direction="horizontal",
gap=16)` re-packs every tracked child in one pass. The other
container-level defaults (`fill_items`, `expand_items`,
`anchor_items`) are read at the next `pack()` call, so changing them
later only affects subsequently-added widgets.

**Surface cascade.** Inherited from Frame: when `surface` (or
`input_background`) is reconfigured at runtime, PackFrame walks its
descendants and re-styles every child that was inheriting from the
old surface. Children with an explicit `surface=` are left alone.

**Geometry propagation.** `propagate=False` only calls
`pack_propagate(False)` on the PackFrame itself. If you also place
the PackFrame with `grid()`, set `grid_propagate(False)` separately.

**Method chaining.** `pack()` and `pack_forget()` return `self`
(from `PackMixin`), so:

```python
btn = ttk.Button(stack, text="Click").pack()
ttk.Entry(stack).pack().focus_set()
```

---

## Events

PackFrame has no `on_*` event helpers and emits no virtual events.
Like its parent `Frame`, it participates only in the standard Tk
`<Configure>` notification fired on resize:

```python
def on_resize(event):
    print(event.width, event.height)

stack.bind("<Configure>", on_resize)
```

If you need to react to children entering or leaving the layout,
bind to those widgets directly — the container's
add/remove hooks are private and not intended as a subscription
surface.

---

## When should I use PackFrame?

Use `PackFrame` when:

- you want a single-axis stack of children with consistent gap
  spacing
- you want to set default `fill` / `expand` / `anchor` once on the
  container instead of on every `pack()` call
- you want plain `pack()` calls to "just work" with sensible
  defaults

Prefer **Frame** when you need full manual control over every child's
pack options, or when you want to mix `grid()` and `place()` freely
without the container injecting defaults. Prefer **GridFrame** for 2D
named-column layouts. Prefer **PanedWindow** when users need to
resize the regions at runtime.

---

## Related widgets

- **Frame** — the parent class; raw container with no managed pack
  defaults
- **GridFrame** — `Frame` subclass with CSS-Grid-style declarative
  rows/columns
- **LabelFrame** — titled bordered container
- **Card** — opinionated `Frame` preset with `accent='card'` and a
  border
- **PanedWindow** — resizable single-axis split regions
- **Separator** — visual divider between PackFrame children

---

## Reference

- **API reference:** [`ttkbootstrap.PackFrame`](../../reference/widgets/PackFrame.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
