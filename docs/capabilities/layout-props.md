---
title: Layout properties
---

# Layout properties

Every widget can be placed in its parent by exactly one of three
geometry managers — `pack`, `grid`, or `place`. Each manager accepts
its own kwarg vocabulary on the call that mounts the widget; this
page is the per-kwarg reference for all three. For the underlying
mechanics (parcel allocation, weight tracks, propagation), see
[Platform → Geometry & Layout](../platform/geometry-and-layout.md).
For the higher-level container helpers that inject these kwargs for
you (`PackFrame`, `GridFrame`), see
[Layout → Containers](layout/containers.md).

ttkbootstrap does not add new layout kwargs. The framework's layout
contribution is at the *container* layer (`PackFrame`'s `direction=`
and `gap=`, `GridFrame`'s `rows=` / `columns=` / `auto_flow=`,
`ScrollView`'s `scroll_direction=`); the per-call vocabulary you pass
to `widget.pack(...)` / `widget.grid(...)` / `widget.place(...)` is
unchanged from raw Tk.

---

## Three managers, three kwarg vocabularies

| Manager | Layout shape | Per-call kwargs | Container setup needed |
|---|---|---|---|
| `pack` | 1-D stack along an axis | `side`, `fill`, `expand`, `anchor`, `padx`, `pady`, `ipadx`, `ipady`, `before`, `after`, `in_` | None |
| `grid` | 2-D row/column matrix | `row`, `column`, `rowspan`, `columnspan`, `sticky`, `padx`, `pady`, `ipadx`, `ipady`, `in_` | `rowconfigure(...)` / `columnconfigure(...)` for weight |
| `place` | absolute or fractional position | `x`, `y`, `relx`, `rely`, `width`, `height`, `relwidth`, `relheight`, `anchor`, `bordermode`, `in_` | None |

You may use only **one** of `pack` and `grid` per parent — Tk raises
`TclError: cannot use geometry manager grid inside .!frame which
already has slaves managed by pack` (and vice versa). `place`
overlays either:

```python
import ttkbootstrap as ttk

app = ttk.App()
parent = ttk.Frame(app)
parent.pack()
ttk.Label(parent, text="A").pack()
ttk.Label(parent, text="B").place(x=0, y=0)  # OK — place overlays
app.mainloop()
```

Three independent siblings inside the same parent always work — the
single-manager rule applies per parent, not per widget tree.

The bad-value errors are loud (no silent fallback). `pack(fill="z")`
raises `TclError: bad fill style "z": must be none, x, y, or both`;
`grid(sticky="z")` raises `TclError: bad stickyness value "z"`;
`place(bordermode="z")` raises `TclError: bad bordermode "z"`.

---

## `pack` kwargs

| Kwarg | Type | Default | What it does |
|---|---|---|---|
| `side` | `"top"` / `"bottom"` / `"left"` / `"right"` | `"top"` | Which edge of the remaining cavity to take a strip from |
| `fill` | `"none"` / `"x"` / `"y"` / `"both"` | `"none"` | Stretch the widget within its strip on those axes |
| `expand` | bool / int / `"yes"` / `"no"` / `"true"` / `"false"` | `0` | Whether the strip itself absorbs leftover cavity space |
| `anchor` | `"n"` / `"ne"` / `"e"` / `"se"` / `"s"` / `"sw"` / `"w"` / `"nw"` / `"center"` | `"center"` | Alignment within the strip when the widget is smaller |
| `padx` | int or `(left, right)` | `0` | Outer space between widget and the strip's horizontal edge |
| `pady` | int or `(top, bottom)` | `0` | Outer space between widget and the strip's vertical edge |
| `ipadx` | int | `0` | Extra interior padding added to the widget's *requested* width |
| `ipady` | int | `0` | Extra interior padding added to the widget's *requested* height |
| `before` | sibling widget | — | Insert this widget's strip *before* the named sibling's strip |
| `after` | sibling widget | — | Insert this widget's strip *after* the named sibling's strip |
| `in_` | parent widget | the call's `master` | Pack into a different parent than the widget's `master` |

`fill` and `expand` are independent. `fill` says "make the *widget*
fill its strip on that axis"; `expand` says "make the *strip* grow
into leftover cavity space." A scrollable content area usually wants
both: `pack(fill="both", expand=True)`. A footer wants neither:
`pack(side="bottom")`.

`expand` is normalized to an int (`0` or `1`) at the Tk boundary —
`expand=True`, `expand=1`, `expand="yes"`, and `expand="true"` all
round-trip to `1`.

`ipadx` adds to the widget's own requested size. A `Button(text="Hi")`
that natively requests 44 px wide ends up 84 px wide with `ipadx=20`
(20 added to each side). `padx` is *outside* the widget — it spaces
the strip away from siblings or the parent edge, and never grows the
widget itself.

`before=` and `after=` accept a sibling already managed by `pack` in
the same parent, and they re-order the strips. Without them, strips
are taken from the cavity in call order:

```python
parent = ttk.Frame(app)
parent.pack()
a = ttk.Label(parent, text="A"); a.pack()
b = ttk.Label(parent, text="B"); b.pack()
c = ttk.Label(parent, text="C"); c.pack(before=b)  # lands between A and B
# slaves order: ['A', 'C', 'B']
```

Stock-Tk `pack` reads `expand=False` and `fill="none"` together to
mean "take only what the widget asks for"; pass at least `fill="x"`
when you want a header bar to span its parent's width.

---

## `grid` kwargs

| Kwarg | Type | Default | What it does |
|---|---|---|---|
| `row` | int | `0` | Cell row (0-based) |
| `column` | int | `0` | Cell column (0-based) |
| `rowspan` | int | `1` | Number of rows this widget covers |
| `columnspan` | int | `1` | Number of columns this widget covers |
| `sticky` | string of `n` / `s` / `e` / `w` (any combination) | `""` | Edges the widget hugs within the cell |
| `padx` | int or `(left, right)` | `0` | Outer horizontal padding around the widget |
| `pady` | int or `(top, bottom)` | `0` | Outer vertical padding around the widget |
| `ipadx` | int | `0` | Extra interior padding (added to widget width) |
| `ipady` | int | `0` | Extra interior padding (added to widget height) |
| `in_` | parent widget | the call's `master` | Grid into a different parent |

`sticky` is the single most important grid kwarg. With `sticky=""`
(the default), the widget sits centered in its cell at its requested
size — even if the cell is much larger. With `sticky="ew"` it
stretches horizontally; with `sticky="nsew"` it fills the cell on
both axes. The string is order-insensitive; Tk normalizes it to the
canonical `nesw` form: `grid(sticky="wsen")` and `grid(sticky="nsew")`
both round-trip via `grid_info()` to `'nesw'`. A tuple or
comma-separated string also works (`sticky=("n","s","e","w")` and
`sticky="n,s,e,w"` both normalize identically).

Cells that have no children render at zero size. To make a row or
column actually expand under resize, configure its weight on the
parent:

```python
form = ttk.Frame(app)
form.pack(fill="both", expand=True)
form.grid_columnconfigure(0, weight=0)        # labels: don't grow
form.grid_columnconfigure(1, weight=1)        # entries: take all extra
form.grid_rowconfigure(2, weight=1)           # one row absorbs vertical extra

ttk.Label(form, text="Name").grid(row=0, column=0, sticky="e", padx=(0, 8))
ttk.Entry(form).grid(row=0, column=1, sticky="ew", pady=4)
```

`weight` is relative — `weight=2` on column 1 next to `weight=1` on
column 2 gives column 1 twice the leftover space. `weight=0` (the
default) means "don't absorb leftover space at all." `minsize=N` on
`grid_columnconfigure` / `grid_rowconfigure` sets a floor: the track
won't shrink below `N` pixels, even when its widgets shrink.

`grid_size()` reports the bounding box of cells *that have children*
(or have been configured via `grid_*configure`):

```python
parent = ttk.Frame(app); parent.pack()
parent.grid_size()                                  # → (0, 0)
ttk.Label(parent, text="X").grid(row=2, column=3)
parent.grid_size()                                  # → (4, 3)  — columns x rows
```

Cells `(0, 0)` through `(2, 3)` exist as zero-size implicit
placeholders even though only `(2, 3)` was filled.

---

## `place` kwargs

| Kwarg | Type | Default | What it does |
|---|---|---|---|
| `x` | int | `0` | Absolute x in pixels relative to the parent |
| `y` | int | `0` | Absolute y in pixels relative to the parent |
| `relx` | float `0.0`–`1.0` | `0` | x as a fraction of parent width (added to `x`) |
| `rely` | float `0.0`–`1.0` | `0` | y as a fraction of parent height (added to `y`) |
| `width` | int | `""` (widget's requested) | Absolute width in pixels |
| `height` | int | `""` (widget's requested) | Absolute height in pixels |
| `relwidth` | float `0.0`–`1.0` | `""` | Width as a fraction of parent width (added to `width`) |
| `relheight` | float `0.0`–`1.0` | `""` | Height as a fraction of parent height (added to `height`) |
| `anchor` | `"n"` / `"ne"` / `"e"` / `"se"` / `"s"` / `"sw"` / `"w"` / `"nw"` / `"center"` | `"nw"` | Which point of the widget is placed at `(x, y)` |
| `bordermode` | `"inside"` / `"outside"` / `"ignore"` | `"inside"` | Whether `x` / `y` count from inside the parent's border |
| `in_` | parent widget | the call's `master` | Place into a different parent |

Absolute and relative coordinates *add*. `place(x=10, relx=0.5)`
positions the widget at "10 pixels to the right of the parent's
horizontal midpoint." The same composition holds for size:
`place(width=20, relwidth=1.0)` is "parent width plus 20."

`anchor="center"` is the most useful position helper — combined with
`relx=0.5, rely=0.5` it pins a widget to the parent's centroid
regardless of resize:

```python
overlay = ttk.Label(canvas, text="Loading…")
overlay.place(relx=0.5, rely=0.5, anchor="center")
```

Default size kwargs are the *empty string*, not `0`. Tk reports them
as `''` from `place_info()`, and Tk reads `""` as "use the widget's
own requested size." Pass an explicit `width=0` to force the widget
to zero-pixel width (rare, but it's how you hide a `place`-managed
overlay without `place_forget()`).

`bordermode="inside"` (the default) measures `x` / `y` from the
inside of the parent's border (Tk's standard behavior for child
positioning); `"outside"` measures from the parent's outer edge,
including its border; `"ignore"` skips border math entirely.

`place` is the only manager that does **not** participate in size
negotiation with the parent — it never causes the parent to grow to
fit the child, and `pack_propagate(False)` / `grid_propagate(False)`
do not apply to it.

---

## Composition rules

### Single-manager-per-parent

Every widget can only belong to one geometry manager at a time, and
within a single parent only one of `pack` and `grid` may register
children. Switching managers on a single widget is supported (the
last call wins) but the previous manager's info is gone:

```python
sw = ttk.Button(parent, text="X")
sw.pack(side="left")
sw.winfo_manager()           # → 'pack'
sw.grid(row=0, column=0)     # switch — last call wins
sw.winfo_manager()           # → 'grid'
sw.pack_info()               # → TclError: window ... isn't packed
```

`winfo_manager()` reports `''` (empty) before any geometry call, the
manager name afterwards, and reverts to `''` after `pack_forget()` /
`grid_forget()` / `place_forget()`.

### `*_forget` vs `grid_remove`

| Method | Discards configuration | Re-show with no args |
|---|---|---|
| `pack_forget()` | Yes — `pack_info()` raises `TclError` | No, must call `.pack(...)` again |
| `grid_forget()` | Yes — `grid_info()` returns `{}` | No, must re-pass `row=` / `column=` |
| `grid_remove()` | No — info is preserved | Yes, `widget.grid()` restores |
| `place_forget()` | Yes — `place_info()` returns `{}` | No |

`grid_remove()` is the right tool for show / hide cycles — the
widget keeps its `row` / `column` / `sticky` / padding for the next
`grid()` call. Using `grid_forget()` then re-`grid()`-ing without
args puts the widget at `row=0, column=0` regardless of where it
was, which is rarely what you want.

### Container-injected defaults

`PackFrame` and `GridFrame` intercept their children's `pack()` /
`grid()` calls and inject defaults you didn't pass. The kwargs you
supply per-call still win:

```python
stack = ttk.PackFrame(app, direction="vertical", gap=8)
stack.pack(fill="both", expand=True)
ttk.Button(stack, text="A").pack()                    # → side='top', pady=0
ttk.Button(stack, text="B").pack()                    # → side='top', pady=(8, 0)
ttk.Button(stack, text="C").pack(pady=(20, 0))        # explicit pady wins
```

`PackFrame` injects a leading `pady` (or `padx`, depending on
direction) on the second-and-later children to implement `gap`;
`GridFrame` injects a leading `padx` / `pady` for cells past row 0
or column 0, then merges with any per-call padding via
`_merge_padding`. See [Spacing](layout/spacing.md) for the full
table of container-level spacing knobs and how they compose.

If you pass kwargs that conflict with what the container injects
(e.g. `side="right"` to a PackFrame configured `direction="vertical"`),
your call wins but the gap math is no longer self-consistent — the
container assumes every child uses the same `side`.

### Method chaining

All three managers' mount methods return `self` so calls can chain:

```python
ttk.Button(parent, text="Save").pack(side="right").configure(width=10)
```

`pack_forget()` / `grid_forget()` / `place_forget()` and
`grid_remove()` also return `self`. The `*_info()` methods return a
dict (`{}` when forgotten, raise for `pack_info` post-forget).

---

## Container-side methods

Each manager also exposes methods that operate on the *container*
rather than the child. These don't take per-child kwargs — they
configure how the container negotiates its size and how its tracks
absorb extra space.

| Method | Owner | What it does |
|---|---|---|
| `parent.pack_propagate(flag=None)` | pack container | When `False`, the container ignores child size requests and stays at its configured `width=` / `height=` |
| `parent.grid_propagate(flag=None)` | grid container | Same, for grid |
| `parent.grid_rowconfigure(row, weight=, minsize=, pad=)` | grid container | Per-row sizing policy |
| `parent.grid_columnconfigure(col, weight=, minsize=, pad=)` | grid container | Per-column sizing policy |
| `parent.pack_slaves()` | pack container | List children currently packed (in order) |
| `parent.grid_slaves(row=, column=)` | grid container | List children gridded (optionally filtered) |
| `parent.place_slaves()` | place container | List children placed |
| `parent.grid_size()` | grid container | `(num_columns, num_rows)` bounding box |

Propagation defaults to *on* — a Frame with no `width=` / `height=`
shrinks to its tightest child:

```python
f = ttk.Frame(app, width=300, height=80)
ttk.Label(f, text="hi").pack()
f.pack()
app.update_idletasks()
f.winfo_width(), f.winfo_height()       # → (15, 20) — shrunk to fit
```

```python
f = ttk.Frame(app, width=300, height=80)
f.pack_propagate(False)
ttk.Label(f, text="hi").pack()
f.pack()
app.update_idletasks()
f.winfo_width(), f.winfo_height()       # → (300, 80) — held at configured size
```

!!! warning "`pack_propagate()` and `grid_propagate()` always return None"

    The mixin methods (`core/capabilities/pack.py:99-111`,
    `core/capabilities/grid.py:112-124`) always pass `flag` through
    to the underlying Tk call, including when `flag=None`. CPython
    `tkinter` distinguishes the query path from the setter path by
    a private `['_noarg_']` sentinel — so passing `None` dispatches
    as the setter, and the query never returns the current value.
    Verified at runtime: `f.pack_propagate()` → `None`, even on a
    fresh widget where the underlying Tk value is `True`. The
    propagation state itself is preserved correctly (the underlying
    Tcl `pack propagate <w>` reports the right value), but you
    cannot read it through the helper. Workaround:
    `widget.tk.call('pack', 'propagate', widget._w)` returns the
    raw Tk integer, or `widget.tk.call('grid', 'propagate', widget._w)`
    for grid.

---

## When to read this page

- *"What does `expand=True` do exactly, and how does it differ from
  `fill='both'`?"* — see the `pack` table above.
- *"Why does `sticky` need `nsew` instead of just `'fill'`?"* —
  `grid` uses edge-based hugging, not Pack's axis-based fill; see
  the `grid` section.
- *"How do I overlay a badge on a button?"* — `place(relx=, rely=,
  anchor='center')` or absolute `(x, y)` over the parent. See `place`.
- *"My Frame is collapsing to nothing — why?"* — `pack_propagate` /
  `grid_propagate` defaults to True; you have no children that
  request a non-zero size. See Container-side methods.
- *"Should I use this page or `PackFrame` / `GridFrame`?"* — Use
  the containers when you want consistent gap/sticky defaults across
  many calls; reach for raw `pack` / `grid` per-call kwargs for
  one-offs and overrides. See [Containers](layout/containers.md).
- *"Why does my `winfo_width()` return 1 in the constructor?"* — see
  [Platform → Widget Lifecycle](../platform/widget-lifecycle.md):
  sizes are not final until the widget is mapped.

---

## Where to read next

- [Layout overview](layout/index.md) — the four mechanisms compared
  side-by-side, with the choose-your-tool rubric.
- [Containers](layout/containers.md) — `PackFrame`, `GridFrame`,
  `ScrollView`, and the rest of the container hierarchy.
- [Spacing](layout/spacing.md) — how `padding=`, `padx`/`pady`,
  `ipadx`/`ipady`, `gap=`, and `density=` compose.
- [Platform → Geometry & Layout](../platform/geometry-and-layout.md)
  — Tk's parcel allocation, weight tracks, and propagation timing.
- [Platform → Widget Lifecycle](../platform/widget-lifecycle.md) —
  why `winfo_width()` is not final inside the constructor.
