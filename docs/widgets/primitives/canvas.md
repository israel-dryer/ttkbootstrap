---
title: Canvas
---

# Canvas

`Canvas` is the 2D drawing and interaction surface in ttkbootstrap. It
is not a custom subclass — `ttkbootstrap.Canvas` is `tkinter.Canvas`
re-exported from the top-level namespace. The integration ttkbootstrap
adds is an install-time wrapper around `tk.Canvas.__init__` that paints
the surface background and clears the focus border on construction and
re-applies them on `<<ThemeChanged>>`. Beyond that, every option,
method, item type, and event behaves exactly like the underlying
`tk.Canvas` widget.

Use `Canvas` when you need a freeform drawing surface — diagrams, node
editors, charts, drag-and-drop boards, zoomable views, or custom
virtualization. For structured records, prefer
[`ListView`](../data-display/listview.md),
[`TableView`](../data-display/tableview.md), or
[`TreeView`](../data-display/treeview.md). For a scrolling region of
ordinary widgets, prefer [`ScrollView`](../layout/scrollview.md).

<figure markdown>
![canvas](../../assets/dark/widgets-canvas.png#only-dark)
![canvas](../../assets/light/widgets-canvas.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

c = ttk.Canvas(app, width=520, height=260)
c.pack(fill="both", expand=True, padx=20, pady=20)

c.create_rectangle(20, 20, 220, 120, fill="#0d6efd", outline="")
c.create_oval(260, 30, 480, 140, outline="#212529", width=2)
c.create_text(260, 190, text="Canvas", font="heading-lg")

app.mainloop()
```

---

## Drawing model

A `Canvas` is a coordinate plane populated with **items**. Each item
has an integer **id** (returned by every `create_*` call) and zero or
more **tags** (strings that group items together). The widget has no
single value, no `textvariable`, and no reactive signal — observers
either bind to events on the canvas / its tags, or query the widget
directly.

### Items

Items are created with one of the typed factory methods. Each returns
the new item's id.

| Factory | Geometry |
|---|---|
| `create_line(x1, y1, x2, y2, …)` | Polyline through the points. |
| `create_rectangle(x1, y1, x2, y2)` | Axis-aligned rectangle. |
| `create_oval(x1, y1, x2, y2)` | Oval inscribed in the bbox. |
| `create_arc(x1, y1, x2, y2)` | Arc inscribed in the bbox; uses `start`/`extent`/`style`. |
| `create_polygon(x1, y1, x2, y2, …)` | Closed polygon. |
| `create_text(x, y, text=…)` | Text anchored at `(x, y)`. |
| `create_image(x, y, image=…)` | A `PhotoImage` / `BitmapImage`. |
| `create_bitmap(x, y, bitmap=…)` | Built-in or external bitmap. |
| `create_window(x, y, window=widget)` | An embedded child widget. |

Item ids are stable until `delete()`. They do not get reused when
items are removed, so a stored id either resolves to the original item
or to nothing (`coords()` returns `[]`, `gettags()` returns `()` —
neither raises).

#### Per-type options

Each item type accepts options shared by all items (see below) plus
its own type-specific options. The most useful per-type axes:

**`create_line`** — `arrow=` (`first` / `last` / `both` / `none`),
`arrowshape=(d1, d2, d3)` for arrowhead size, `smooth=` (`True` for
Bezier-smoothed line, `'raw'` for raw splines), `splinesteps=` for
smoothing fidelity, `capstyle=` (`butt` / `projecting` / `round`),
`joinstyle=` (`bevel` / `miter` / `round`).

**`create_rectangle`** — `fill=`, `outline=`, `width=`, `dash=` /
`dashoffset=` for dashed borders.

**`create_oval`** — same option surface as rectangle. The oval is
always inscribed in its bbox; for an angled or rotated ellipse,
build it from `create_polygon` points.

**`create_arc`** — `start=` (degrees, counter-clockwise from 3
o'clock), `extent=` (degrees of sweep), `style=` (`pieslice` /
`chord` / `arc`), plus the rectangle option set.

**`create_polygon`** — `fill=`, `outline=`, `width=`, `smooth=` /
`splinesteps=` (Bezier-smoothed polygon). Polygons are always closed:
the last point is implicitly connected back to the first.

**`create_text`** — `text=` (the literal string), `font=` (Tk font
spec or named font), `anchor=` (`n` / `ne` / `e` / `se` / `s` /
`sw` / `w` / `nw` / `center`; default `center`),
`justify=` (`left` / `center` / `right`) for multi-line text,
`width=` (wrap width in screen units; `0` means no wrapping),
`fill=` for the foreground color.

**`create_image`** — `image=` (a `PhotoImage` / `BitmapImage` /
PIL `ImageTk.PhotoImage`), `anchor=` (default `center`). The
*caller* must keep a reference to the image object — Canvas
stores only a weak association, and a garbage-collected image
disappears from the canvas with no error.

**`create_bitmap`** — `bitmap=` (one of the built-in bitmaps like
`error` / `gray12` / `info` / `question` / `questhead` /
`warning` / `hourglass`, or `@/path/to/file.xbm`), `foreground=`,
`background=`.

**`create_window`** — `window=widget` (an existing child widget
parented to the canvas), `anchor=`, `width=` / `height=`
(override the embedded widget's natural size). The embedded
widget must be a child of the canvas (or one of its ancestors)
or the call raises `TclError`. See [Embedded child widgets](#embedded-child-widgets)
under Patterns for the full quirks.

#### Common item options

Every item type accepts the options below. Set them at creation or
later via `itemconfigure(itemOrTag, option=value)`; read them back
via `itemcget(itemOrTag, option)`.

| Option | Effect |
|---|---|
| `state` | `'normal'` / `'disabled'` / `'hidden'` — see [Item state](#item-state). |
| `tags` | Tuple of strings — see [Tags](#tags). |
| `activefill` / `activeoutline` / `activewidth` | Override the `fill` / `outline` / `width` while the cursor is over the item. |
| `disabledfill` / `disabledoutline` / `disabledwidth` | Override while the item or canvas is in `state="disabled"`. |
| `stipple` / `outlinestipple` | Bitmap pattern used to "shade" a fill or outline (e.g. `gray50`). |
| `dash` / `dashoffset` | Dash pattern for outlines (tuple of pixel runs, e.g. `(4, 2)`). |

### Coordinates

The canvas uses two coordinate systems:

- **Screen coordinates** — pixel offsets relative to the widget's
  top-left, used by Tk events (`event.x` / `event.y`).
- **Canvas coordinates** — the unscrolled plane the items live on.
  Use `canvasx(event.x)` / `canvasy(event.y)` to convert a screen
  position into a canvas position; the two only differ when the
  canvas is scrolled.

Read or rewrite an item's coordinates via `coords()`. Move and scale
work on a tag-or-id, so they accept either a single id or a tag string
(including the special tag `"all"`).

```python
xy = c.coords(rect)              # list[float] — current coords
c.coords(rect, 20, 20, 180, 90)  # rewrite

c.move(rect, 10, 0)              # nudge by (dx, dy)
c.move("node", 0, 20)            # move every item tagged "node"

c.scale("all", 0, 0, 2.0, 2.0)   # double everything around (0, 0)
```

The `scrollregion` option is the rectangle the view can be scrolled
across. It is independent of where items live: items can be drawn
outside `scrollregion` and they will still render, they just won't be
reachable by scrolling. `bbox('all')` returns the bounding box of
every item, which is the usual right-hand side of a
`configure(scrollregion=…)` call after a redraw.

### Tags

Tags group items so styling, event handling, and bulk operations apply
to all of them at once. The same tag can cover any number of items,
and an item can carry any number of tags.

```python
c.create_rectangle(20, 20, 140, 80,
                   fill="#198754", outline="", tags=("node", "ok"))
c.create_text(80, 50, text="Node", fill="white",
              tags=("node",))

c.itemconfigure("ok", outline="#212529", width=2)   # restyle every "ok"
c.move("node", 200, 0)                               # move every "node"
c.delete("node")                                     # remove every "node"
```

Useful tag methods: `addtag_*` / `gettags` / `dtag` / `find_withtag` /
`tag_lower` / `tag_raise` / `tag_bind` / `tag_unbind`. The special tag
`"all"` matches every item; `"current"` matches the item under the
mouse (set by Tk during enter/leave dispatch).

### Stacking order

Items are drawn in the order they were created, with later items on
top of earlier ones. Use `tag_raise` and `tag_lower` to restack:

```python
c.tag_raise("highlight")          # bring all "highlight" items to front
c.tag_lower("background")         # send all "background" items to back
c.tag_raise(item_a, item_b)       # raise item_a just above item_b
```

`find_above(itemOrTag)` and `find_below(itemOrTag)` return the
immediate stacking neighbors as `(id,)` tuples (or `()` at the top /
bottom). Combine with `find_overlapping` to walk every item in a
region in stacking order — useful for picking the topmost item under
a click that's not the one `find_closest` would pick (which uses
geometric distance, not stacking).

### Item state

Each item has its own `state` axis, independent of the canvas-level
`state` option:

| `itemconfigure(item, state=…)` | Effect |
|---|---|
| `"normal"` | Default — visible, hit-testable. |
| `"disabled"` | Item is drawn in its `disabledfill` / `disabledoutline` colors and stops responding to bindings. |
| `"hidden"` | Item is not drawn and is not hit-testable. |

The canvas-level `state="disabled"` option **does not block item
creation or programmatic mutation** — you can still call
`create_*`, `coords()`, `move()`, etc. It restyles items into their
"disabled" colors and suppresses event delivery to tag and item
bindings, but the canvas itself is otherwise live.

---

## Common options

`tk.Canvas` exposes a large option surface; the most-used options are
below. The autostyle wrapper adds three additional construction
keywords on top — `surface`, `inherit_surface`, and `autostyle` — that
work the same way they do on [`Text`](text.md#autostyle-keywords).

### Size and view

| Option | Type | Description |
|---|---|---|
| `width` / `height` | `int` | Widget size in **pixels** (not character cells). |
| `scrollregion` | `(x1, y1, x2, y2)` or `()` | The rectangle the view can scroll across. Empty tuple resets it. |
| `confine` | `bool` | Constrain `xview`/`yview` to `scrollregion`. Default `True`. |
| `xscrollincrement` / `yscrollincrement` | `int` | Snap scroll to multiples of this many pixels. `0` for free-scroll. |
| `xscrollcommand` / `yscrollcommand` | `callable` | The reporter callbacks a scrollbar's `set` method plugs into. |

### Interaction

| Option | Type | Description |
|---|---|---|
| `closeenough` | `float` | Hit-test tolerance in pixels for `find_closest`. Default `1.0`. |
| `cursor` | `str` | Mouse-cursor name (e.g. `"hand2"`). |
| `state` | `'normal' \| 'disabled'` | Canvas-wide state — see [Drawing model § Item state](#item-state) for what this actually does. |
| `takefocus` | `bool` | Whether `<Tab>` traversal stops on the canvas. |

### Theme-critical colors

| Option | Description |
|---|---|
| `background` | Page background. The autostyle builder sets this from the resolved surface token. |
| `highlightthickness` | Border thickness; the autostyle builder sets this to `0` so the canvas blends into its parent. |
| `highlightbackground` / `highlightcolor` | Border color when unfocused / focused. Visible only when `highlightthickness > 0`. |
| `selectbackground` / `selectforeground` | Selection colors used by Tk text-edit ops on `create_text` items. |

The autostyle wrapper sets `background` and `highlightthickness` from
the active theme on construction and on every `<<ThemeChanged>>`.
`background` overrides survive until the next theme switch and then
revert. Pass `autostyle=False` for a Canvas the framework leaves
alone — see *Behavior*.

### Autostyle keywords

The install-time wrapper around `tk.Canvas.__init__` accepts three
additional kwargs that are not real Tk options:

| Option | Type | Description |
|---|---|---|
| `autostyle` | `bool` | Default `True`. Pass `False` to skip the theme-color paint and the `<<ThemeChanged>>` registration entirely. The `_surface` attribute is still captured. |
| `inherit_surface` | `bool` | Default from `AppSettings.inherit_surface_color`. When true, the new widget's `_surface` is taken from the parent — the explicit `surface=` argument is overridden. |
| `surface` | `str` | Surface token to record on the widget. Honored only when `inherit_surface=False` (or when there is no parent surface to inherit). |

`inherit_surface=True` (the default) is the opt-in behavior for legacy
Tk widgets: the canvas blends with its container rather than forcing a
specific surface. If you want to pin a surface regardless of the parent,
pass `inherit_surface=False` alongside your explicit `surface=`:

```python
ttk.Canvas(parent, surface='card', inherit_surface=False)
```

Unlike [`Text`](text.md), the Canvas builder **does** honor `surface`
— a Canvas in a `Frame(surface='card')` paints with the card
background, so the canvas blends into the container surface. If you
want the canvas to use a fixed color instead of the resolved surface
token, configure `background=` directly and accept that the next
`<<ThemeChanged>>` will revert it (or pass `autostyle=False`).

`accent`, `variant`, and `density` are **not** valid kwargs on
`Canvas` — passing any of them raises
`TclError: unknown option "-accent"` (or `-variant` / `-density`).

---

## Behavior

**Canvas-level `state="disabled"` does not block programmatic edits.**
Unlike `tk.Text` (which silently no-ops `insert`/`delete` while
disabled), `tk.Canvas` lets `create_*`, `coords()`, `move()`, and
`delete()` proceed normally. What `state="disabled"` does is restyle
items into their `disabledfill` / `disabledoutline` colors and stop
delivering events to tag and item bindings. Per-item state via
`itemconfigure(item, state="hidden")` is the right tool for hiding,
and `state="disabled"` on individual items is the right tool for
read-only visuals.

**Theme reapplication.** The widget is registered with the global
style on construction; on `<<ThemeChanged>>` the builder runs again
and resets `background` and `highlightthickness`. Direct overrides on
those options revert at the theme switch. Item colors set with
`fill=` / `outline=` are not theme-managed — set them yourself, or
re-set them in your own `<<ThemeChanged>>` handler if they need to
follow the theme.

**`scrollregion` reset.** Setting `scrollregion=()` (empty tuple)
clears it. Writing `None` produces undefined behavior across Tk
builds — use the empty tuple form.

**Item ids stay valid until `delete()`.** They are not reused when
items are removed, so a stale id resolves to nothing rather than to
some other item. `c.coords(stale_id)` returns `[]` and `c.gettags
(stale_id)` returns `()`; neither raises.

---

## Events

`Canvas` does **not** emit any framework virtual events
(`<<Change>>`, `<<Input>>`, `<<Changed>>`) and exposes no `on_*`
helpers. Events come from three places: the canvas itself (via
`bind`), individual tags or item ids (via `tag_bind`), and the
implicit `"current"` tag that Tk maintains under the mouse.

### Tag and item bindings

`tag_bind(tagOrId, sequence, callback)` attaches a handler that fires
when the matching event happens *inside the bounding box* of any
matching item. This is the canonical way to make items clickable or
hover-able.

```python
c.tag_bind("node", "<Button-1>", lambda e: print("node clicked"))
c.tag_bind("node", "<Enter>",     lambda e: c.configure(cursor="hand2"))
c.tag_bind("node", "<Leave>",     lambda e: c.configure(cursor=""))
```

Bindings live on the tag, not the items, so creating a new item with
that tag picks the binding up automatically.

### Canvas-level bindings

Bind directly on the canvas widget for events that are not item-
specific (e.g. clicks on empty regions, key presses, focus changes).
Convert screen coordinates to canvas coordinates with
`canvasx(event.x)` / `canvasy(event.y)` whenever the canvas can be
scrolled:

```python
def on_click(event):
    cx = c.canvasx(event.x)
    cy = c.canvasy(event.y)
    print("canvas coords:", cx, cy)

c.bind("<Button-1>", on_click)
```

### Hit testing

Canvas exposes three lookup helpers. None of them mutates state, so
they are safe to call from any event handler:

| Method | Returns |
|---|---|
| `find_closest(x, y)` | Tuple of one id — the topmost item nearest `(x, y)`, within `closeenough` pixels. |
| `find_overlapping(x1, y1, x2, y2)` | Tuple of every id whose bbox overlaps the rectangle. |
| `find_withtag(tagOrId)` | Tuple of every id matching the tag (or `(id,)` for an int). |
| `find_enclosed(x1, y1, x2, y2)` | Tuple of every id fully contained by the rectangle. |
| `find_above(id)` / `find_below(id)` | Tuple of one id — the immediate sibling in the stacking order. |

```python
def on_click(event):
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    hit = c.find_closest(x, y)
    if hit:
        print("hit:", hit[0], "tags:", c.gettags(hit[0]))

c.bind("<Button-1>", on_click)
```

---

## Patterns

### Pair with scrollbars

Wire `xscrollcommand` / `yscrollcommand` to the scrollbars' `set` and
the scrollbars' `command` to `xview` / `yview`. The `scrollregion`
defines the scrollable plane:

```python
frame = ttk.Frame(app)
frame.pack(fill="both", expand=True, padx=20, pady=20)

c = ttk.Canvas(frame, scrollregion=(0, 0, 2000, 1200))
c.grid(row=0, column=0, sticky="nsew")

ysb = ttk.Scrollbar(frame, orient="vertical", command=c.yview)
ysb.grid(row=0, column=1, sticky="ns")
xsb = ttk.Scrollbar(frame, orient="horizontal", command=c.xview)
xsb.grid(row=1, column=0, sticky="ew")

c.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
```

For widget-of-widgets scrolling (form panels, lists of cards),
[`ScrollView`](../layout/scrollview.md) wraps this pattern and adds
hover / always / never visibility modes.

### Drag an item

```python
drag = {"id": None, "x": 0, "y": 0}

def on_down(event):
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    hit = c.find_closest(x, y)
    if not hit:
        return
    drag["id"] = hit[0]
    drag["x"], drag["y"] = x, y

def on_move(event):
    if drag["id"] is None:
        return
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    c.move(drag["id"], x - drag["x"], y - drag["y"])
    drag["x"], drag["y"] = x, y

def on_up(_event):
    drag["id"] = None

c.bind("<ButtonPress-1>", on_down)
c.bind("<B1-Motion>", on_move)
c.bind("<ButtonRelease-1>", on_up)
```

### Zoom around a point

```python
def zoom(factor: float, origin=(0, 0)):
    c.scale("all", origin[0], origin[1], factor, factor)
    c.configure(scrollregion=c.bbox("all"))
```

`scale()` rewrites coordinates only — it does not change line widths,
font sizes, or image pixel densities. For uniform-looking zoom, scale
those attributes yourself in the same handler.

### Rubber-band selection rectangle

Draw a one-off rectangle that follows the mouse during a drag, then
use it as a hit-test region on release:

```python
state = {"rect": None, "x": 0, "y": 0}

def on_down(event):
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    state["x"], state["y"] = x, y
    state["rect"] = c.create_rectangle(
        x, y, x, y, outline="#0d6efd", dash=(4, 2),
    )

def on_drag(event):
    if state["rect"] is None:
        return
    x, y = c.canvasx(event.x), c.canvasy(event.y)
    c.coords(state["rect"], state["x"], state["y"], x, y)

def on_up(event):
    if state["rect"] is None:
        return
    x1, y1, x2, y2 = c.coords(state["rect"])
    selected = c.find_enclosed(min(x1, x2), min(y1, y2),
                               max(x1, x2), max(y1, y2))
    print("selected:", selected)
    c.delete(state["rect"])
    state["rect"] = None

c.bind("<ButtonPress-1>", on_down)
c.bind("<B1-Motion>", on_drag)
c.bind("<ButtonRelease-1>", on_up)
```

Swap `find_enclosed` for `find_overlapping` to select items partially
in the rectangle as well as fully contained ones.

### Snap to a grid

Round canvas coordinates to a grid step before applying them:

```python
GRID = 20

def snap(value: float) -> int:
    return round(value / GRID) * GRID

def on_drop(event):
    x = snap(c.canvasx(event.x))
    y = snap(c.canvasy(event.y))
    c.coords(item, x, y)
```

Combine with `xscrollincrement` / `yscrollincrement` set to the same
step to make scrolling snap as well.

### Animation with `after`

Canvas has no built-in animation loop. Drive incremental updates
through `after`, mutating coordinates in place rather than deleting
and recreating items:

```python
ball = c.create_oval(20, 20, 60, 60, fill="#0d6efd")
vx, vy = 3, 2

def tick():
    global vx, vy
    c.move(ball, vx, vy)
    x1, y1, x2, y2 = c.coords(ball)
    if x1 <= 0 or x2 >= c.winfo_width():
        vx = -vx
    if y1 <= 0 or y2 >= c.winfo_height():
        vy = -vy
    c.after(16, tick)              # ~60 fps

c.after(16, tick)
```

For smooth playback at high item counts, batch many `move` /
`coords` / `itemconfigure` calls and let Tk redraw once at the end of
the handler. Avoid mixing `update()` calls into the loop — Tk will
redraw mid-frame and wreck pacing.

### Embedded child widgets

`create_window` parks a real Tk widget at a canvas coordinate. Useful
for forms inside diagrams, inline edit fields, or any case where you
want a child widget to live on a freeform plane.

```python
entry = ttk.Entry(c)
c.create_window(100, 100, window=entry, anchor="nw", width=180)
```

Notes worth remembering:

- The widget must be parented to the canvas (or one of its
  ancestors) — pass `c` (or `app`) as the parent at construction
  time, otherwise `create_window` raises `TclError`.
- The window item's bbox tracks the *embedded widget's* requested
  size unless you pin it with `width=` / `height=`.
- The window item moves with the canvas when scrolled — you do not
  have to manage geometry separately.
- Bindings on the embedded widget take precedence over canvas-level
  bindings for events on its area.

### Embed an image (PIL)

`tk.Canvas` accepts only `PhotoImage` / `BitmapImage`. For PNG /
JPEG / arbitrary RGBA images, route through Pillow:

```python
from PIL import Image, ImageTk

img = ImageTk.PhotoImage(Image.open("logo.png"))
c.image_ref = img                              # keep a reference!
c.create_image(50, 50, image=img, anchor="nw")
```

The `image_ref = img` stash is not optional. Canvas keeps only a
weak association with the image; if the only reference is the local
`img` name, it gets garbage-collected the moment the function
returns and the image disappears with no error.

### Render only what's visible

For very large canvases, draw items lazily based on the visible view:

```python
def visible_bbox():
    x1 = c.canvasx(0)
    y1 = c.canvasy(0)
    x2 = c.canvasx(c.winfo_width())
    y2 = c.canvasy(c.winfo_height())
    return (x1, y1, x2, y2)

def repaint():
    c.delete("cell")
    x1, y1, x2, y2 = visible_bbox()
    for cell in cells_in(x1, y1, x2, y2):
        c.create_rectangle(*cell.bounds, fill=cell.color, tags=("cell",))

c.bind("<Configure>", lambda e: repaint())
c.bind("<MouseWheel>", lambda e: app.after_idle(repaint))
```

### Export to PostScript

`tk.Canvas` ships a `postscript()` method that renders the visible
region (or any specified rectangle) to a PostScript document. Useful
for print previews and as a stepping-stone to PNG via Ghostscript.

```python
c.postscript(file="diagram.ps", colormode="color")
```

Useful options: `x` / `y` / `width` / `height` for a sub-region,
`pagewidth` / `pageheight` for output size, `colormode=` (`color` /
`gray` / `mono`), and `file=` (string) or `file=None` to return the
PostScript as a string.

---

## Performance

Canvas can comfortably handle a few thousand items per layer; the
limits are easy to hit if you're sloppy. Practical guidance:

- **Mutate, don't recreate.** `coords()` / `move()` / `itemconfigure`
  are far cheaper than `delete` + `create_*`. For an animation loop
  or a repaint of a slowly-changing scene, update existing items in
  place.
- **Tag every group.** Bulk operations (`itemconfigure("nodes",
  fill=…)`, `delete("preview")`, `tag_raise("selected")`) are O(items
  with tag), not O(items in canvas). Iterating ids in Python is
  slower than letting Tcl walk the tag set.
- **Hide instead of delete** when items will come back. `state="hidden"`
  drops them from rendering and hit-testing but keeps the id, the
  tags, and any bindings. `delete` invalidates the id and frees its
  bindings.
- **`bbox` is O(items in tag).** `bbox("all")` walks every item.
  Cache it after batched mutations rather than calling it per frame.
- **Virtualize past ~10 000 items.** At that scale, drawing what's
  outside the visible viewport is wasted work — see [Render only
  what's visible](#render-only-whats-visible).
- **Batch then yield.** Run all mutations in one handler and let Tk
  redraw at idle. Calls to `update()` inside a tight loop force a
  redraw per call and tank throughput.
- **Image references survive in Python, not Tcl.** Cache
  `PhotoImage` instances on a long-lived object (the canvas itself
  is fine — `c.image_ref = img`) so the GC doesn't reclaim them
  between frames.

---

## When should I use Canvas?

Reach for `Canvas` when:

- you need **freeform 2D drawing** with full control over coordinates,
  layering, and item styling;
- interaction is **item-based** — hit testing, dragging, linking,
  selection — rather than widget-based;
- you need **zooming, panning, or custom virtualization** of a very
  large content plane;
- you're embedding a **mix of text, images, shapes, and child widgets**
  in a layout the framework's containers don't express.

Use [`ScrollView`](../layout/scrollview.md) +
[`Frame`](../layout/frame.md) for scrolling regions of ordinary
widgets, [`ListView`](../data-display/listview.md) /
[`TableView`](../data-display/tableview.md) /
[`TreeView`](../data-display/treeview.md) for structured records, and
[`Text`](text.md) for richtext-style content.

## Related widgets

- [Text](text.md) — sibling primitive for multi-line text editing
  with tag-based styling.
- [Entry](entry.md) — sibling primitive for raw single-line input.
- [ScrollView](../layout/scrollview.md) /
  [Scrollbar](../layout/scrollbar.md) — scrolling primitives.
- [ListView](../data-display/listview.md) /
  [TableView](../data-display/tableview.md) /
  [TreeView](../data-display/treeview.md) — structured-record displays.
- [Meter](../data-display/meter.md) /
  [FloodGauge](../data-display/floodgauge.md) — composite widgets
  that draw on a Canvas internally.

## Reference

- The [Tk canvas manual](https://www.tcl.tk/man/tcl/TkCmd/canvas.htm) —
  authoritative for every option, item type, item option, and
  coordinate-arithmetic form.
- Python's [`tkinter.Canvas`](https://docs.python.org/3/library/tkinter.html#tkinter.Canvas)
  bindings.
