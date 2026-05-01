---
title: Card
---

# Card

`Card` is a themed container preset for grouping related content into
an elevated panel. It's a `Frame` subclass that ships with three
non-default constructor defaults — `accent='card'`, `show_border=True`,
`padding=16` — so a bare `Card(parent)` already renders as a bordered
box on a slightly elevated surface, with consistent inner padding.

Card is purely structural. It has no behavior of its own beyond what
Frame already provides: it doesn't manage its children's geometry,
doesn't expose interactive state, and emits no virtual events. Reach
for `Card` instead of `Frame` when you want the visual preset; reach
for `LabelFrame` when you also need a titled border, or `Expander`
when the content should collapse.

<figure markdown>
![card](../../assets/dark/widgets-card.png#only-dark)
![card](../../assets/light/widgets-card.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

card = ttk.Card(app)
card.pack(padx=20, pady=20, fill="x")

ttk.Label(card, text="Card title", font="heading-md").pack(anchor="w")
ttk.Label(card, text="Body text on the card surface.").pack(
    anchor="w", pady=(4, 0)
)

app.mainloop()
```

The bare `Card(app)` already includes 16px inner padding and a 1-pixel
border around the `card` surface. Pack or grid it the same way you
would any other Frame.

---

## Common options

Card inherits the full Frame option surface — `padding`, `width`,
`height`, `style`, `cursor`, `takefocus`, `accent`, `variant`,
`surface`, `show_border`, `style_options`, plus the deprecated
`bootstyle`. The defaults are what distinguish it:

| Option         | Default | Notes                                                                                                                                                                                  |
|----------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `padding`      | `16`    | Inner padding in pixels. Pass an int for uniform padding, a 2-tuple for `(horizontal, vertical)`, or a 4-tuple for `(left, top, right, bottom)`.                                       |
| `accent`       | `'card'`| The `card` token resolves to a slightly elevated theme surface. Because Card is a container class, `accent` is rerouted to `surface` internally — `accent='card'` ⇒ `surface='card'`. |
| `show_border`  | `True`  | Draws a 1-pixel border around the card. Pass `False` to render a borderless elevated panel (still contrasts with the parent surface).                                                  |
| `surface`      | inherited if explicitly set | Overrides the `accent`-derived surface. Use this if you want the card's surface and accent to come apart — e.g. `accent='primary', surface='card'` (no-op for plain Frame styling).   |
| `width`/`height`| `0`    | Requested geometry. Geometry propagation defaults to True; use `card.pack_propagate(False)` (or `grid_propagate`) to lock the size against child requests.                            |

Passing `bootstyle=` (deprecated) on Card suppresses the `accent='card'`
default — `bootstyle` and `accent`/`variant` are mutually exclusive,
and Card's defaulting respects that. Migrate to `accent`/`variant`
instead.

To swap the elevation token at construction time, override `accent`:

```python
ttk.Card(app, accent="primary")     # ⇒ surface='primary', tinted card
ttk.Card(app, accent="secondary")   # ⇒ surface='secondary'
ttk.Card(app, show_border=False)    # borderless elevated panel
```

The Frame style builder (`style/builders/frame.py`) reads only the
`surface` and `show_border` options — it ignores `accent` directly.
The container-class rerouting in the bootstyle constructor wrapper
(`style/bootstyle.py:464`) is what turns Card's `accent='card'`
default into a real surface change.

---

## Behavior

Card is a `Frame` subclass, so it inherits the framework's container
behavior unchanged:

- **Surface cascade.** When you reconfigure the surface at runtime
  with `card.configure_style_options(surface=...)`, the override on
  `Frame.configure_style_options` walks all descendants and re-themes
  any child that was inheriting the old surface. Children with an
  explicit surface (set via `style_options['surface']`) are not
  touched. The matching cascade exists for `input_background`.
- **Geometry propagation.** Card propagates child geometry like any
  Frame — its requested size grows to fit its children unless you
  call `card.pack_propagate(False)` (or the grid equivalent) and
  set explicit `width`/`height`.
- **No special child management.** Card does not auto-pack or
  auto-grid children. Build layout inside the card with the same
  geometry managers you'd use anywhere else.
- **Theme repaint.** `<<ThemeChanged>>` triggers a rebuild of the
  Card's style on theme switch, picking up the new `card` token's
  resolved color.

Card has no interactive state. There is no hover, active, focus, or
disabled visual — it never accepts focus by default (`takefocus=0`
inherited from `ttk.Frame`).

---

## Events

Card emits no virtual events. The only event surface worth knowing
about is the standard Tk `<Configure>` event, fired by the windowing
system on resize:

```python
def on_resize(event):
    print(f"card is now {event.width}x{event.height}")

card.bind("<Configure>", on_resize)
```

If you need a card whose visible state can change in response to
clicks (expand, collapse, dismiss), wire that behavior with
`bind("<Button-1>", ...)` on the Card itself — or use
[Expander](expander.md), which already implements collapse/expand.

---

## When should I use Card?

Use Card when:

- You want an elevated, bordered panel for grouping content and the
  default `card` surface and 1px border are appropriate.
- You'd otherwise be writing
  `Frame(parent, accent='card', show_border=True, padding=16)` by
  hand at every group.
- You're composing a dashboard, settings panel, or list of items
  where each entry should visually stand apart from the page surface.

Prefer **Frame** when you want neutral container styling without an
elevated surface or border — e.g. for invisible structural grouping,
or a row that should be transparent against its parent.

Prefer **LabelFrame** when the panel needs a *titled* border (the
title is rendered into the border itself).

Prefer **Expander** or **Accordion** when the panel needs to
collapse, or when you have several panels that should toggle as a
group.

---

## Related widgets

- **[Frame](frame.md)** — base container; Card is a Frame subclass
  with surface and border presets.
- **[LabelFrame](labelframe.md)** — titled bordered container; use
  when the section needs a heading rendered into the border.
- **[Expander](expander.md)** — collapsible single-section container.
- **[Accordion](accordion.md)** — multi-section collapsible group.
- **[PackFrame](packframe.md)** / **[GridFrame](gridframe.md)** —
  Frame subclasses with geometry presets; combine with Card by
  nesting (`Card` outside, `PackFrame` inside) when you want both
  elevation and auto-layout.

---

## Reference

- **API reference:** `ttkbootstrap.Card`
- **Related guides:** [Layout](../../guides/layout.md),
  [Design System: Surfaces](../../design-system/surfaces.md)
