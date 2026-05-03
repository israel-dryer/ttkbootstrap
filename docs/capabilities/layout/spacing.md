---
title: Spacing
---

# Spacing

Tk exposes spacing through three orthogonal knobs — `padding=` on the
container, `padx`/`pady` on each geometry-manager call, and
`ipadx`/`ipady` for internal padding. ttkbootstrap layers two more on
top: `gap=` on `PackFrame` / `GridFrame` for uniform inter-item
spacing, and a `density` typography axis that scales button and
entry padding via the style system. This page is the map: which
knob does what, where each one applies, and how they compose.

For the full pack/grid/place per-call kwarg reference see
[Layout properties](../layout-props.md). For the underlying Tk
geometry mechanics see
[Platform → Geometry & Layout](../../platform/geometry-and-layout.md).

---

## Five spacing knobs at a glance

| Knob | Where it lives | What it does | Accepted by |
|---|---|---|---|
| `padding=` | Container construction | Inner padding between the container's edge and its children | `Frame`, `Card`, `LabelFrame`, `PackFrame`, `GridFrame`, every `ttk` container |
| `padx=` / `pady=` | Per-call kwarg on `pack()` / `grid()` | Outer space between the child and its siblings or the parent | Any widget being packed or gridded |
| `ipadx=` / `ipady=` | Per-call kwarg on `pack()` / `grid()` | Extra interior padding added to the *widget's own* requested size | Any widget being packed or gridded |
| `gap=` | Container construction (`PackFrame`, `GridFrame`) | Uniform spacing **between** children, injected as leading `padx` / `pady` | `PackFrame`, `GridFrame` |
| `density=` | Widget construction (action / input / data-display widgets) | Typography axis (`'default'` / `'compact'`) — scales font, padding, and resolved-style height | `Button`, `TextEntry`, `Combobox`, `Spinbox`, `OptionMenu`, `MenuButton`, `Label`, `Toolbar`, `CheckToggle`, `RadioToggle`, `TreeView` |

`padding` is the *container's* business; `padx`/`pady`/`ipadx`/`ipady`
are the *child's* business; `gap` is the container saying "stop
typing the same `pady=8` on every child, I'll inject it for you";
`density` is a coarse-grained typography control that doesn't change
per-call kwargs at all — it picks a different baseline font and a
different image element height inside the resolved ttk style.

There is **no widget-level margin option** in Tk. What CSS calls
"margin" is expressed from the parent's side via `padx`/`pady` on
the child's `pack()` / `grid()` call.

---

## `padding=` on containers

Every ttkbootstrap container forwards `padding=` straight to
`ttk.Frame`'s `-padding` option, which Tk accepts in three shapes:

| Form | Meaning |
|---|---|
| `padding=10` | All four sides 10 px |
| `padding=(20, 5)` | Horizontal 20, vertical 5 |
| `padding=(5, 10, 15, 20)` | Left 5, top 10, right 15, bottom 20 |

```python
import ttkbootstrap as ttk

app = ttk.App()
section = ttk.Frame(app, padding=(20, 12))
ttk.Label(section, text="Inside the section").pack(anchor="w")
section.pack(fill="x")
app.mainloop()
```

`Card` defaults to `padding=16`; `Frame`, `LabelFrame`, `PackFrame`,
and `GridFrame` default to no padding (Tk treats absent padding as
`""`, which `cget('padding')` reports as `''`). Reconfigure with
`section.configure(padding=(0, 24))` at any time — the change is live.

A common shape mistake is to write `padding=(0, 0, 50, 0)` and
expect "right margin." That's correct in spirit but it's *padding*
inside the parent, not margin around the parent — it shifts the
children left by 50 px instead of pushing the container away from
its neighbour. Use `pack(padx=(0, 50))` on the **parent itself** for
"margin."

---

## `padx` / `pady` on the geometry-manager call

`padx` and `pady` are per-call kwargs on `pack()` and `grid()`. They
add outer space between the child and either its parent or its
preceding sibling. Both accept a single int (symmetric) or a 2-tuple
(asymmetric):

| Form on `pack` | Meaning |
|---|---|
| `pady=10` | 10 px above and below |
| `pady=(20, 0)` | 20 px above, 0 below — the leading-edge form |
| `padx=(0, 12)` | 0 px left, 12 px right |

| Form on `grid` | Meaning |
|---|---|
| `padx=10` | 10 px left and right of the cell content |
| `padx=(20, 0)` | 20 px left, 0 right |

```python
import ttkbootstrap as ttk

app = ttk.App()
form = ttk.Frame(app, padding=20)
ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w", padx=(0, 8))
ttk.TextEntry(form).grid(row=0, column=1, sticky="ew")
ttk.Label(form, text="Email").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(8, 0))
ttk.TextEntry(form).grid(row=1, column=1, sticky="ew", pady=(8, 0))
form.pack(fill="x")
app.mainloop()
```

The 2-tuple form is the workhorse for spacing patterns. Vertical
stacks lift the leading-edge gap onto the *next* row's `pady=(N, 0)`
so the first row sits flush against the parent's padding.
`PackFrame` and `GridFrame` automate exactly this pattern via `gap=`
(see below).

---

## `ipadx` / `ipady` for internal padding

`ipadx` and `ipady` add to the **widget's own requested size** at
geometry-manager time — they expand the widget rather than reserving
space around it. Useful for stretching a button that would otherwise
size to its label:

```python
import ttkbootstrap as ttk

app = ttk.App()
ttk.Button(app, text="OK").pack(padx=20, pady=20, ipadx=24, ipady=8)
app.mainloop()
```

The button's `winfo_reqwidth()` jumps by `2 * ipadx`. The padding
applied by `padx` / `pady` sits *outside* this expanded width.

`ipadx` / `ipady` does **not** stack with `padding=` on the same
widget — `padding=` is the container's inner gutter; `ipadx` /
`ipady` is the geometry manager telling the widget "you're bigger
than you asked for." The two affect different calculations.

---

## `gap=` on PackFrame and GridFrame

`PackFrame(direction=, gap=)` and `GridFrame(rows=, columns=, gap=)`
turn the leading-edge `pad?=(N, 0)` pattern into a container-level
default. The container intercepts each child's `pack()` / `grid()`
call and injects the gap automatically.

### PackFrame — gap as leading `padx` or `pady`

`PackFrame` chooses the pack `side` from `direction`, then inserts
the gap as a leading-edge pad on every child *after* the first:

```python
import ttkbootstrap as ttk

app = ttk.App()
toolbar = ttk.PackFrame(app, direction="horizontal", gap=12, padding=8)
ttk.Button(toolbar, text="New").pack()
ttk.Button(toolbar, text="Open").pack()
ttk.Button(toolbar, text="Save").pack()
toolbar.pack(fill="x")
app.mainloop()
```

Verified `pack_info()` for the three buttons:

| Button | `padx` |
|---|---|
| New (first) | `0` |
| Open | `(12, 0)` |
| Save | `(12, 0)` |

The first child is flush against the container's padding; every
subsequent child carries a leading `(12, 0)` so the visual spacing
between siblings is uniform. The same pattern applies in vertical
mode with `pady=(N, 0)`.

`gap` is live-reconfigurable: `toolbar.configure(gap=20)` repacks
every managed child with the new spacing. Reconfiguring `direction`
also repacks (it has to — the `side` changed).

If a per-call `pack(padx=…)` or `pack(pady=…)` is provided
explicitly, the user value wins — `PackFrame` only injects the gap
when the relevant kwarg is absent. Children that don't go through
`PackFrame.pack` (raw `tkinter` widgets without `PackMixin`, or
children parented elsewhere) skip the hook entirely.

### GridFrame — gap as merged leading padding

`GridFrame` accepts `gap=N` (uniform) or `gap=(col_gap, row_gap)`
(asymmetric). The gap is injected as **leading** `padx` for any
column ≥ 1, and **leading** `pady` for any row ≥ 1:

```python
import ttkbootstrap as ttk

app = ttk.App()
form = ttk.GridFrame(app, columns=3, gap=10, padding=12)
for label in ("a", "b", "c", "d", "e"):
    ttk.Button(form, text=label).grid()
form.pack(fill="both", expand=True)
app.mainloop()
```

Verified `grid_info()` for the five buttons:

| Cell | `padx` | `pady` |
|---|---|---|
| `(0, 0)` — `a` | `0` | `0` |
| `(0, 1)` — `b` | `(10, 0)` | `0` |
| `(0, 2)` — `c` | `(10, 0)` | `0` |
| `(1, 0)` — `d` | `0` | `(10, 0)` |
| `(1, 1)` — `e` | `(10, 0)` | `(10, 0)` |

A per-call `padx=N` is **merged** with the gap, not replaced. The
merge sums the leading edge and keeps the trailing edge as the
user's value:

| User-supplied `padx` | Merge result on column ≥ 1 with `gap=10` |
|---|---|
| `4` (int) | `(14, 4)` |
| `(4, 0)` | `(14, 0)` |
| `(2, 8)` | `(12, 8)` |

Cell `(0, 0)` is special: no gap injection runs there, so a user
`padx=4` reaches the cell as `4` unchanged.

For the full track-spec grammar (`columns=[0, 1, "auto", "100px"]`)
see [GridFrame](../../widgets/layout/gridframe.md). For the
auto-flow rules and the implicit-cursor footguns see
[Layout overview](index.md).

---

## `density=` — the typography axis

`density` is a coarse style token that scales the resolved ttk
style across a coherent set of widgets. Two values are registered:
`'default'` and `'compact'`. The compact path swaps three things at
once:

| Token | Default | Compact |
|---|---|---|
| Font | `body` (~13 pt) | `caption` (~11 pt) |
| Button padding | `(8, 0)` (scaled) | `(6, 5, 6, 3)` (scaled) |
| Field height | 33 px (scaled) | 26 px (scaled) |
| Icon size | text ascent + 3 | text ascent + 4 |

```python
import ttkbootstrap as ttk

app = ttk.App()
ttk.Button(app, text="Default density").pack(pady=4)
ttk.Button(app, text="Compact density", density="compact").pack(pady=4)
ttk.TextEntry(app, density="compact").pack(pady=4, fill="x", padx=20)
app.mainloop()
```

`density` is **not** a universal kwarg. Container widgets reject
it. The accepted-by list:

| Class | `density=` accepted? |
|---|---|
| `Button`, `MenuButton`, `OptionMenu` | Yes |
| `CheckToggle`, `RadioToggle`, `Toolbar` | Yes |
| `TextEntry`, `Spinbox`, `Combobox` | Yes |
| `Label` | Yes (Tk-class autostyle path) |
| `TreeView` | Yes |
| `Frame`, `Card`, `LabelFrame`, `PackFrame`, `GridFrame` | No — raises `TclError: unknown option "-density"` |
| `CheckButton`, `RadioButton`, `Switch` | No — raises `TclError: unknown option "-density"` |
| `Tabs`, `SideNav`, `PageStack` | No — raises `TclError: unknown option "-density"` |

Pass `density='compact'` only to the widgets that accept it. Don't
expect a single `density='compact'` on a container to cascade to
its children — `density` is per-widget, and there's no descendant
walk for it the way there is for `surface`.

`Entry`, `Combobox`, and `Spinbox` (and the composites built on them)
support live density reconfiguration — `entry.configure(density='compact')`
rebuilds the resolved ttk style, not just the font.

---

## Composition rules

The five knobs interact predictably as long as you remember which
side of the parent/child boundary each one sits on:

- `padding=` reserves space *inside* the container before any child
  is placed. Increasing it shrinks the available area for children.
- `padx` / `pady` on a child's geom call reserves space *outside*
  the child within the parent. It does not change the child's own
  reqwidth/reqheight.
- `ipadx` / `ipady` *expands* the child's reqwidth/reqheight at
  geom-call time. The container's `padding=` and the child's
  `padx`/`pady` are computed against the expanded size.
- `gap=` on `PackFrame` / `GridFrame` is shorthand for "inject
  leading-edge `padx` / `pady` between siblings, but not before the
  first one." Per-call user overrides win on `PackFrame` and
  *merge* on `GridFrame`.
- `density=` doesn't touch geom kwargs at all — it picks a different
  font + image element height inside the resolved ttk style. A
  compact button still sits in the same `padx=(12, 0)` slot it
  would as a default button; it's just smaller.

A typical form combines them cleanly:

```python
import ttkbootstrap as ttk

app = ttk.App()
form = ttk.GridFrame(app, columns=[0, 1], gap=(12, 8), padding=(20, 16))
ttk.Label(form, text="Name", density="compact").grid(sticky="w")
ttk.TextEntry(form, density="compact").grid(sticky="ew")
ttk.Label(form, text="Email", density="compact").grid(sticky="w")
ttk.TextEntry(form, density="compact").grid(sticky="ew")
form.pack(fill="x", padx=20, pady=20)
app.mainloop()
```

`padding=(20, 16)` reserves the form's inner gutter; `gap=(12, 8)`
spaces the cells; `density='compact'` tightens each child's
typography; the outer `pack(padx=20, pady=20)` is the form's
"margin" relative to its parent.

---

## Where to look next

- **How does the container place its children?**
  [Layout overview](index.md) compares `pack` / `grid` / `place` /
  `PackFrame` / `GridFrame` / `ScrollView` side-by-side.
- **Which container should I reach for?**
  [Containers](containers.md) maps each container's role,
  geometry policy, and surface-cascade behavior.
- **What pack/grid/place kwargs does each call accept?**
  [Layout properties](../layout-props.md) is the per-kwarg
  reference.
- **How does `ScrollView` interact with padding and gap?**
  [Scrolling](scrolling.md).
- **How does Tk realize sizes during layout?**
  [Platform → Geometry & Layout](../../platform/geometry-and-layout.md).
- **Why is `winfo_width()` zero before `pack()` runs?**
  [Platform → Widget Lifecycle](../../platform/widget-lifecycle.md)
  explains the created/managed/mapped phases.
