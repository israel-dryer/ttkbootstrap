# Layout

Tk has three built-in geometry managers — `pack`, `grid`, and
`place` — and ttkbootstrap layers a small set of opinionated
container widgets on top of them so that common layouts do not
require per-call `pack()` / `grid()` boilerplate. The geometry
managers themselves are unchanged; the framework adds
container-level defaults (axis, gap, sticky, auto-placement) plus
a scrollable viewport primitive.

The pages in this section cover the four concrete topics:

- [Containers](containers.md) — `Frame`, `LabelFrame`, `Card`,
  `PackFrame`, `GridFrame`, `PanedWindow`, and which to reach
  for when.
- [Spacing](spacing.md) — `padding=`, `gap=`, geometry-manager
  `padx`/`pady`, density.
- [Scrolling](scrolling.md) — `ScrollView` and how it composes a
  `Canvas` viewport, two `Scrollbar`s, and mousewheel routing into
  one container.
- [Layout properties](../layout-props.md) — the per-call kwargs
  (`fill`, `expand`, `side`, `sticky`, `row`, `column`, `padx`,
  `pady`) the geometry managers consume.

For the underlying Tk geometry mechanics (pack's parcel model,
grid's track sizing, propagation), see
[Platform → Geometry & Layout](../../platform/geometry-and-layout.md).

---

## At a glance

| | `pack` | `grid` | `place` | `PackFrame` | `GridFrame` | `ScrollView` |
|---|---|---|---|---|---|---|
| Layout shape | 1D stack | 2D grid | absolute coords | 1D stack | 2D grid | scrollable viewport |
| Per-child kwargs | `side`, `fill`, `expand`, `padx`, `pady`, `anchor` | `row`, `column`, `rowspan`, `columnspan`, `sticky`, `padx`, `pady` | `x`, `y`, `relx`, `rely`, `relwidth`, `relheight` | inherited from container | inherited from container | content widget hosts its own children |
| Container kwargs | — | `rowconfigure(weight=, minsize=)`, `columnconfigure(...)` | — | `direction`, `gap`, `fill_items`, `expand_items`, `anchor_items` | `rows`, `columns`, `gap`, `sticky_items`, `auto_flow` | `scroll_direction`, `scrollbar_visibility` |
| Mixing in one parent | not with `grid` | not with `pack` | safe — `place` overlays | child calls flow through container | child calls flow through container | child is parented on `sv.canvas` |
| Best for | toolbars, status bars, single-column forms | multi-column forms, dashboards | overlays, drag handles, custom positioning | stacked sections with consistent gap | declarative grids without tuning every cell | long forms or stacked content that overflows |

`pack` and `grid` cannot be mixed in the same parent — Tk raises
`_tkinter.TclError: cannot use geometry manager grid inside .!frame
which already has slaves managed by pack` (and vice versa). `place`
can overlay either. Inside different parents the rule does not
apply, so a `pack`-managed parent containing a `grid`-managed child
frame is fine.

---

## Built-in geometry managers

Tk's three geometry managers stay accessible through every widget's
`pack()`, `grid()`, and `place()` methods, exactly as they do in
plain Tk:

```python
import ttkbootstrap as ttk

app = ttk.App()
section = ttk.Frame(app, padding=20)
section.pack(fill="both", expand=True)

ttk.Label(section, text="Account").pack(anchor="w")
ttk.Entry(section).pack(fill="x", pady=(8, 0))

app.mainloop()
```

`pack` allocates parcels along an axis (`side="top"` by default).
`grid` divides the parent into rows and columns sized by `weight`
and `minsize` (set via `parent.rowconfigure(0, weight=1)` /
`parent.columnconfigure(0, weight=1)`). `place` positions a
child at absolute or relative coordinates, ignoring siblings.

The cost of these managers is verbosity: every `pack()` call needs
the same `side`/`fill`/`pady` boilerplate, and every `grid()` call
needs the right cell coordinate plus track-weight setup on the
parent. The three container helpers below absorb that boilerplate.

---

## PackFrame — auto-pack with a gap

`PackFrame` is a `Frame` subclass that intercepts children's
`pack()` calls and injects a default `side` (from `direction=`),
inter-item spacing (from `gap=`), and optional fill / expand /
anchor defaults. Children call the standard `pack()` method;
PackFrame fills in the kwargs.

```python
stack = ttk.PackFrame(app, direction="vertical", gap=8, padding=20)
stack.pack(fill="both", expand=True)

ttk.Button(stack, text="First").pack()
ttk.Button(stack, text="Second").pack()
ttk.Button(stack, text="Third").pack()
```

The first child packs at the top with no leading gap; subsequent
children pack below it with `pady=(8, 0)`. Six `direction` aliases
(`vertical`, `column`, `column-reverse`, `horizontal`, `row`,
`row-reverse`) collapse to four pack `side`s (`top`, `bottom`,
`left`, `right`).

See [PackFrame](../../widgets/layout/packframe.md) for the full
option surface and edge-case rules (overriding `side=` per call,
mixing in raw `tkinter` widgets, the `before=` / `after=` kwargs).

---

## GridFrame — declarative 2D grids

`GridFrame` is a `Frame` subclass that intercepts children's
`grid()` calls and resolves the next free cell from a configurable
auto-placement policy. Tracks are sized declaratively up front;
gaps are injected as leading `padx` / `pady`; default sticky is
applied to every cell.

```python
form = ttk.GridFrame(
    app, columns=2, rows=2, gap=10, sticky_items="nsew", padding=20
)
form.pack(fill="both", expand=True)

ttk.Button(form, text="Top-Left").grid()
ttk.Button(form, text="Top-Right").grid()
ttk.Button(form, text="Bottom-Left").grid()
ttk.Button(form, text="Bottom-Right").grid()
```

`columns=` and `rows=` accept either a count or a list of size
specs (`int` for flex weight, `"auto"` for content sizing,
`"Npx"` for a minimum). `auto_flow` selects row-major / column-major
walking and the dense variants. `sticky_items` is the per-cell
default sticky; pass `sticky=` per `grid()` call to override on
specific children.

See [GridFrame](../../widgets/layout/gridframe.md) for the full
track-spec grammar, the auto-flow modes, and the per-call override
rules.

---

## ScrollView — scrollable container

`ScrollView` wraps a `Canvas` viewport, one or two `Scrollbar`s,
and per-descendant mousewheel routing into a single `Frame`
subclass. The content widget lives inside the canvas; as the
viewport scrolls, the canvas window translates relative to the
viewport, and the scrollbars report fractional position.

```python
sv = ttk.ScrollView(app)
sv.pack(fill="both", expand=True, padx=20, pady=20)

content = sv.add()
for i in range(30):
    ttk.Label(content, text=f"Row {i + 1}").pack(anchor="w", pady=4)
```

`sv.add()` returns the content `Frame` — pack widgets into it as
you would any other Frame. `scroll_direction` (`vertical` /
`horizontal` / `both`) controls which axes scroll;
`scrollbar_visibility` (`always` / `never` / `hover` / `scroll`)
controls whether bars are visible when content fits.

Scrolling is a container concern, not a widget feature. Children
inside `ScrollView` do not implement scrolling themselves — they
just sit in the canvas and the container scrolls them. Mousewheel
events are routed to the ScrollView via a per-instance bindtag,
so wheel events on any descendant scroll the right container even
when ScrollViews are nested.

See [ScrollView](../../widgets/layout/scrollview.md) for the full
contract — the canvas-window parenting requirement, the gutter
reservation rules in `hover` / `scroll` modes, the
`scroll_direction` reconfigure caveat, and `Shift+MouseWheel` for
horizontal scroll on platforms that support it.

---

## Containers vs widgets

Layout is a relationship between a widget and its parent — the
**parent** decides how the widget is placed, sized, and resized.
Treat layout policy as something the container owns:

- A child widget should request its size (via `width=` / `height=`,
  font, contents) and pass on per-call `fill` / `expand` /
  `sticky` kwargs to express layout intent.
- The container should own the geometry manager choice
  (`pack` vs `grid` vs `place`), inter-item spacing, and which
  regions expand under resize.
- A region that scrolls should be a separate container
  (`ScrollView`), not a flag on the child.

A consequence is that the same widget can live in many layouts.
A `Button` packs into a vertical stack, grids into a form, or
places onto a card overlay — the call differs, the widget does not.

---

## When to read this section

- *"Should I use `pack`, `grid`, or `place` here?"* —
  [Containers](containers.md) (the decision rubric).
- *"How do I keep `padx`/`pady` consistent across a layout?"* —
  [Spacing](spacing.md) (use `gap=` on PackFrame / GridFrame).
- *"How do I make a long form scroll?"* —
  [Scrolling](scrolling.md) and
  [ScrollView](../../widgets/layout/scrollview.md).
- *"Which kwargs does `pack()` / `grid()` accept on a single call?"* —
  [Layout properties](../layout-props.md).
- *"Why is `widget.winfo_width()` returning 1?"* —
  [Platform → Widget Lifecycle](../../platform/widget-lifecycle.md)
  (sizes are not final until the widget is mapped).
- *"How does Tk decide which child gets extra space on resize?"* —
  [Platform → Geometry & Layout](../../platform/geometry-and-layout.md)
  (pack parcels, grid weights, propagation).
- *"How do I split a region into resizable panes?"* —
  [PanedWindow](../../widgets/layout/panedwindow.md).
- *"How do I show a dropdown / overlay positioned absolutely?"* —
  use `place(x=, y=)` on the overlay widget; for popups attached to
  a triggering widget, see
  [ContextMenu](../../widgets/actions/contextmenu.md) and
  [Tooltip](../../widgets/overlays/tooltip.md).
