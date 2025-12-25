---

## Framework integration

### Signals & events

Widgets participate in ttkbootstrap’s reactive model.

- **Signals** represent a widget’s **value/state** and are built on **Tk variables** with a modern subscription API.

- **Events** (including virtual events) represent **interactions and moments** (click, commit, focus, selection changed).

Signals and events are complementary: use signals for state flow and composition, and use events when you need
interaction-level integration.

!!! link "See also: [Signals](../../capabilities/signals.md), [Virtual Events](../../capabilities/virtual-events.md), [Callbacks](../../capabilities/callbacks.md)"

### Design system

Widgets are styled through ttkbootstrap’s design system using:

- semantic colors via `bootstyle` (e.g., `primary`, `success`, `danger`)

- variants (e.g., `outline`, `link`, `ghost` where supported)

- consistent state visuals across themes

!!! link "See also: [Colors](../../design-system/colors.md), [Variants](../../design-system/variants.md)"

### Layout properties

Widgets support ttkbootstrap layout conveniences (when available) so they compose cleanly in modern layouts.

!!! link "See also: [Layout Properties](../../capabilities/layout-props.md)"

### Localization

Text labels can be localized in localized applications.

!!! link "See also: [Localization](../../capabilities/localization.md)"


---

title: Canvas
---

# Canvas

`Canvas` is Tkinter’s **2D drawing and interaction surface** (`tk.Canvas`).

It’s the foundation for many custom UI patterns:

- diagrams and node editors

- charts and visualizations

- drag-and-drop surfaces

- zoomable / pannable views

- virtual scrolling for custom content

ttkbootstrap exposes `Canvas` as a first-class widget so you can build high-performance, interactive views with consistent theming and practical patterns.

!!! tip "Prefer higher-level widgets when they fit"
    If your UI is primarily structured data, prefer **ListView**, **TableView**, or **TreeView**.  
    Use `Canvas` when you need **custom drawing**, **freeform layout**, or **interaction** that standard widgets can’t express.

---

## Basic usage

Draw a few shapes:

```python
import ttkbootstrap as ttk

app = ttk.App()

c = ttk.Canvas(app, width=520, height=260, background="white")
c.pack(fill="both", expand=True, padx=20, pady=20)

c.create_rectangle(20, 20, 220, 120, fill="#0d6efd", outline="")
c.create_oval(260, 30, 480, 140, outline="#212529", width=2)
c.create_text(260, 190, text="Canvas", font=("TkDefaultFont", 14, "bold"))

app.mainloop()
```

---

## Key options

Canvas has a large option surface. These are the ones you’ll use most.

### Size and coordinates

- `width`, `height` — canvas size (screen units)

- `scrollregion` — the “virtual space” you can scroll around

- `confine` — constrain view to `scrollregion` when scrolling

```python
c = ttk.Canvas(app, width=600, height=400, scrollregion=(0, 0, 2000, 1200))
```

!!! note "Resetting scrollregion"
    Setting `scrollregion=()` resets it to empty.  
    Setting it to `None` may not clear it on all Tk builds.

### Interaction

- `closeenough` — hit test tolerance (pixels)

- `cursor` — cursor over the canvas

- `state="normal" | "disabled"`

### Theme-critical colors

- `background` (or `bg`)

- selection colors: `selectbackground`, `selectforeground`

If your canvas items depend on theme colors, set item colors explicitly (e.g., `fill=...`, `outline=...`) rather than relying on widget-level defaults.

---

## Canvas items

Canvas content is made of **items**, each with an integer id:

```python
rect = c.create_rectangle(10, 10, 110, 60, fill="tomato", outline="")
text = c.create_text(60, 35, text="Hello")
```

Item ids are stable until deleted. You can also assign **tags** to items.

### Common item types

- `create_line`

- `create_rectangle`

- `create_oval`

- `create_polygon`

- `create_text`

- `create_image`

- `create_window` (embed a widget)

---

## Tags

Tags are the best way to manage groups of items.

- Apply styles to many items at once

- Bind events to groups

- Move/scale groups as a unit

```python
c.create_rectangle(20, 20, 140, 80, fill="#198754", outline="", tags=("node", "ok"))
c.create_text(80, 50, text="Node", fill="white", tags=("node",))

# Move all items with the "node" tag
c.move("node", 200, 0)
```

### Bind events to a tag

```python
def on_click(_):
    print("node clicked")

c.tag_bind("node", "<Button-1>", on_click)
```

---

## Coordinates and transforms

### Reading and updating item coordinates

```python
xy = c.coords(rect)            # list[float]
c.coords(rect, 20, 20, 180, 90)  # set new coords
```

### Move items

```python
c.move(rect, 10, 0)
c.move("node", 0, 20)  # move all items with tag
```

### Scale for zoom

`scale(tagOrId, xOrigin, yOrigin, xScale, yScale)` scales coordinates around an origin.

```python
def zoom(factor: float, origin=(0, 0)):
    c.scale("all", origin[0], origin[1], factor, factor)
    c.configure(scrollregion=c.bbox("all"))
```

!!! note "Canvas scaling"
    `scale()` scales item coordinates. Text and line widths may need extra handling depending on the effect you want.

---

## Scrolling

Canvas uses `xscrollcommand`/`yscrollcommand` and `xview`/`yview` like Text.

```python
import ttkbootstrap as ttk

app = ttk.App()

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

app.mainloop()
```

### Convert screen coordinates to canvas coordinates

When the canvas is scrolled, event `x/y` are screen coordinates relative to the widget.
Use `canvasx` and `canvasy` to convert:

```python
def on_click(e):
    x = c.canvasx(e.x)
    y = c.canvasy(e.y)
    print("canvas coords:", x, y)

c.bind("<Button-1>", on_click)
```

---

## Hit testing

Canvas provides “find” helpers:

- `find_closest(x, y)`

- `find_overlapping(x1, y1, x2, y2)`

- `find_withtag(tagOrId)`

```python
def on_click(e):
    x, y = c.canvasx(e.x), c.canvasy(e.y)
    hit = c.find_closest(x, y)
    if hit:
        print("hit item id:", hit[0], "tags:", c.gettags(hit[0]))

c.bind("<Button-1>", on_click)
```

---

## Dragging (common pattern)

A minimal drag pattern:

```python
drag = {"id": None, "x": 0, "y": 0}

def on_down(e):
    x, y = c.canvasx(e.x), c.canvasy(e.y)
    hit = c.find_closest(x, y)
    if not hit:
        return
    drag["id"] = hit[0]
    drag["x"], drag["y"] = x, y

def on_move(e):
    if drag["id"] is None:
        return
    x, y = c.canvasx(e.x), c.canvasy(e.y)
    dx, dy = x - drag["x"], y - drag["y"]
    c.move(drag["id"], dx, dy)
    drag["x"], drag["y"] = x, y

def on_up(_):
    drag["id"] = None

c.bind("<ButtonPress-1>", on_down)
c.bind("<B1-Motion>", on_move)
c.bind("<ButtonRelease-1>", on_up)
```

---

## Performance tips

- Prefer **tags** for bulk operations instead of iterating every item id.

- Avoid deleting/recreating everything each frame; update coordinates and styles in-place.

- Limit the number of canvas items when possible; thousands are fine, tens of thousands may require careful design.

- For “virtualized” surfaces, render only what’s visible (use `canvasx/canvasy` + view bounds).

---

## When should I use Canvas?

Use `Canvas` when:

- you need custom drawing or freeform layout

- interaction is item-based (hit testing, dragging, linking)

- you need zooming/panning or custom virtualization

Prefer **ScrollView + Frame** when:

- you’re laying out regular widgets in a scrolling container

Prefer **ListView / TableView / TreeView** when:

- the content is primarily structured records

---

## Related widgets

- **ScrollView / Scrollbar** — scrolling primitives

- **Text** — tag-based content editing

- **ListView** — virtual scrolling for record lists

- **PageStack** — complex view composition

---

## Reference

- **API Reference:** `ttkbootstrap.Canvas` (Tkinter `tk.Canvas`)

---

## Additional resources

### Related widgets

- [Combobox](combobox.md)

- [Entry](entry.md)

- [Spinbox](spinbox.md)

### Framework concepts

- [State & Interaction](../../capabilities/state-and-interaction.md)

- [Configuration](../../capabilities/configuration.md)

### API reference

- [`ttkbootstrap.Canvas`](../../reference/widgets/Canvas.md)
