---
title: LabelFrame
---

# LabelFrame

`LabelFrame` is a themed container that draws a thin border around a
region of the UI and embeds a text label into that border. It wraps
`ttk.Labelframe` and is the canonical way to group related controls
under a visible section title — settings groups, form clusters,
option panels.

Unlike [`Frame`](frame.md), `LabelFrame` does not subclass `Frame` and
does not propagate runtime `surface` changes to its descendants. It
inherits its surface from its parent at construction time the same
way Frame does, but reconfiguring the surface later restyles only the
LabelFrame itself.

<figure markdown>
![labelframe](../../assets/dark/widgets-labelframe.png#only-dark)
![labelframe](../../assets/light/widgets-labelframe.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

group = ttk.LabelFrame(app, text="Network", padding=16)
group.pack(fill="x", padx=20, pady=20)

ttk.CheckButton(group, text="Use proxy").pack(anchor="w")
ttk.Entry(group).pack(fill="x", pady=(8, 0))

app.mainloop()
```

`text=` is the embedded label. `padding=` is the inner spacing between
the border and the children. Without `padding`, the children butt up
against the border line.

---

## Common options

The styling surface is small and shared with `Frame` — `surface` is the
canonical knob, and on container classes the `accent` slot is reused
as a surface override. The border is always drawn (1 px, theme-aware
stroke); there is no public option to turn it off.

| Option         | Type         | Default       | Notes                                                                  |
| -------------- | ------------ | ------------- | ---------------------------------------------------------------------- |
| `text`         | str          | `""`          | Label text embedded in the border                                      |
| `labelanchor`  | str          | `"nw"`        | Label position; see below                                              |
| `labelwidget`  | Widget       | `None`        | Substitute a widget for the text label (e.g. an icon-bearing `Label`)  |
| `padding`      | int \| tuple | `""`          | Inner spacing; `(left, top)` or `(l, t, r, b)` accepted                |
| `width`        | int          | natural       | Requested width in pixels (see propagation note in Behavior)           |
| `height`       | int          | natural       | Requested height in pixels (see propagation note in Behavior)          |
| `surface`      | str          | parent inherit | Surface token: `chrome`, `content`, `card`, `overlay`, `input`        |
| `accent`       | str          | —             | On containers, equivalent to `surface=` — sets the fill                |
| `input_background` | str      | parent inherit | Cascades to input descendants; does **not** tint the LabelFrame itself |
| `style`        | str          | `"TLabelframe"` | Explicit ttk style name; overrides theme-token styling               |

### Label placement

`labelanchor` accepts the eight compass values plus center:

```python
ttk.LabelFrame(app, text="Network", labelanchor="nw")  # default — top left
ttk.LabelFrame(app, text="Network", labelanchor="n")   # centered top
ttk.LabelFrame(app, text="Network", labelanchor="w")   # left side, vertical
ttk.LabelFrame(app, text="Network", labelanchor="s")   # bottom (rare)
```

For a custom label — e.g. a `Label` with an icon — use `labelwidget=`
in place of `text=`:

```python
header = ttk.Label(app, text="Advanced", icon="bootstrap-gear")
ttk.LabelFrame(app, labelwidget=header, padding=12)
```

### Surface and accent

```python
ttk.LabelFrame(app, text="Section", surface="card")
ttk.LabelFrame(app, text="Section", accent="primary")   # primary-colored fill
```

`surface` and `accent` are interchangeable on container widgets:
the bootstyle constructor wrapper recognizes that `TLabelframe` is a
container class and turns `accent` into a surface override. Either
spelling produces the same effect — `surface=` is the more explicit
choice.

### Options that don't behave like Frame's

- **`show_border`** is read by the LabelFrame style builder and
  defaults to `True`, but the constructor doesn't expose it as a kwarg.
  Passing `show_border=False` raises `TclError: unknown option
  "-show_border"`. The border is effectively always on.
- **`variant`** is rejected — only the `default` variant is
  registered for `TLabelframe`, so passing any other variant raises
  `BootstyleBuilderError: Builder '<variant>' not found for widget
  class 'TLabelframe'`.
- **`input_background`** is accepted and stored on the widget; it
  cascades to input descendants the same way it does on `Frame`, but
  the LabelFrame itself is not tinted by it. Use `surface=` to color
  the LabelFrame.

---

## Behavior

`LabelFrame` is a non-interactive structural widget. It does not
respond to clicks, take keyboard focus by default, or emit any virtual
events; its responsibilities are visual surfacing and child hosting.

**Geometry propagation.** Like `ttk.Labelframe`, a `LabelFrame` sizes
itself to its content unless you disable propagation explicitly:

```python
pane = ttk.LabelFrame(app, text="Pane", width=240, height=400)
pane.pack(side="left")
pane.pack_propagate(False)   # honor width/height instead of children
```

Without `pack_propagate(False)` (or `grid_propagate(False)`), explicit
`width=`/`height=` are treated as natural-size *hints* and are
overridden by child requests.

**Surface inheritance, no runtime cascade.** At construction time,
LabelFrame inherits its surface from its parent (the same path Frame
uses), so a LabelFrame nested inside `Frame(surface="card")` picks up
the `card` surface automatically. **Runtime reconfiguration is not
cascaded**, however: calling `lf.configure_style_options(surface="card")`
restyles the LabelFrame itself but leaves child widgets on their
original surface. This is a deliberate divergence from `Frame`, which
inherits a `_refresh_descendant_surfaces` hook. If you need regional
runtime restyling, wrap the LabelFrame in a `Frame` and reconfigure
the Frame's surface instead.

**Label inside the border.** The label is drawn *into* the border
stroke, not above it — so the border line is interrupted by the label
text rather than running continuously. This is standard
`ttk.Labelframe` behavior; the embedded label is what visually anchors
the title to the region.

---

## Events

`LabelFrame` has no `on_*` event helpers and emits no virtual events.
The only event it participates in is the standard Tk `<Configure>`
notification fired on resize:

```python
def on_resize(event):
    print(event.width, event.height)

group.bind("<Configure>", on_resize)
```

If you need to react to interaction inside the group, bind to the
relevant child widgets directly — `LabelFrame` is purely a container
surface.

---

## When should I use LabelFrame?

Use `LabelFrame` when:

- a group of related controls benefits from a short, visible section
  title (e.g. "Network", "Display", "Notifications" in a settings
  page)
- the title should be visually attached to the region, not floating
  above it
- you don't need the title to be a multi-line header or include
  prominent imagery

Prefer **Frame** when the region needs no title, or when you want to
restyle the surface at runtime and have descendants restyle with it.
Prefer **Card** when you want a stronger card-style treatment with
separated header / body / footer slots and richer header content.
Use **Separator** between labelled regions when the visual break
matters more than a labelled boundary.

---

## Related widgets

- **Frame** — untitled themed container; subclass with surface cascade
- **Card** — opinionated `Frame` preset with header / body / footer
- **PackFrame** / **GridFrame** — `Frame` subclasses with auto-pack
  and auto-grid layout managers
- **Separator** — visual divider for regions inside a frame
- **Label** — pair with a plain `Frame` when the title needs to live
  in surrounding layout instead of inside the border

---

## Reference

- **API reference:** [`ttkbootstrap.LabelFrame`](../../reference/widgets/LabelFrame.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
