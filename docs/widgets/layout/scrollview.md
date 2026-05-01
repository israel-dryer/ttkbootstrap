---
title: ScrollView
---

# ScrollView

`ScrollView` is a scrollable container for arbitrary widgets. It
wraps a `Canvas` plus one or two `Scrollbar`s into a single
`Frame` subclass, hosts a content widget inside the canvas, and
binds mousewheel scrolling on every descendant — so a long form,
settings panel, or stacked card list can be made scrollable
without hand-wiring the canvas, the scrollbars, the wheel events,
and the cross-platform platform deltas.

`ScrollView` extends [Frame](frame.md), so the same `surface`,
`show_border`, `input_background`, and `padding` tokens apply to
the outer container. The viewport is a `Canvas` instance; the two
scrollbars are [Scrollbar](scrollbar.md) widgets. Both are exposed
as attributes (`canvas`, `vertical_scrollbar`,
`horizontal_scrollbar`) for situations where the composite's
defaults don't fit.

<figure markdown>
![scrollview](../../assets/dark/widgets-scrollview.png#only-dark)
![scrollview](../../assets/light/widgets-scrollview.png#only-light)
</figure>

---

## Basic usage

```python
import ttkbootstrap as ttk

app = ttk.App()

sv = ttk.ScrollView(app)
sv.pack(fill="both", expand=True, padx=20, pady=20)

content = sv.add()
for i in range(30):
    ttk.Label(content, text=f"Row {i + 1}").pack(anchor="w", pady=4)

app.mainloop()
```

`sv.add()` returns the content `Frame` you should pack widgets
into. Subsequent calls without arguments are idempotent — they
return the same frame — so it's safe to call lazily from a setup
helper.

---

## Layout model

`ScrollView` uses a fixed 2×2 internal grid:

| Cell    | Widget                                         |
| ------- | ---------------------------------------------- |
| `(0,0)` | the `canvas` viewport                          |
| `(0,1)` | `vertical_scrollbar` (`scroll_direction` ≠ horizontal) |
| `(1,0)` | `horizontal_scrollbar` (`scroll_direction` ≠ vertical) |

The content is mounted as a *canvas window* — the canvas's
`create_window(0, 0, anchor=anchor, window=child)` call — not as a
gridded child. This is what makes scrolling work: as the canvas
scrolls, the window position translates relative to the viewport,
and the scrollbars report a `(first, last)` fraction of the
content visible at any time.

**The content widget must be parented on `sv.canvas`.** When you
let `add()` create the frame for you, that's automatic. When you
build your own content widget, parent it explicitly:

```python
sv = ttk.ScrollView(app)
sv.pack(fill="both", expand=True)

content = ttk.Frame(sv.canvas, padding=16)   # parent on the canvas
sv.add(content)

ttk.Label(content, text="Custom outer frame").pack(anchor="w")
```

A widget parented on `sv` (the outer Frame) instead of `sv.canvas`
will display, but it won't scroll — it lives outside the canvas
window and ignores `xview` / `yview`.

**One content widget at a time.** `add()` raises `ValueError` if
you pass a new widget while one is already present. Call
`remove()` first to swap:

```python
sv.remove()              # detach and return the old widget
sv.add(new_content)
```

`get_child()` returns the current content widget (or `None`).

**Scrollbar gutter is reserved in `hover` and `scroll` modes.**
The grid column (vertical) and row (horizontal) that hold the
scrollbars are given a `minsize` equal to each scrollbar's natural
requested dimension, then the scrollbar widgets are
`grid_remove()`d. The minsize persists, so the canvas occupies a
constant area regardless of whether the scrollbar is currently
shown — the same idea as CSS `scrollbar-gutter: stable`. In
`always` and `never` modes no gutter is reserved (the bar is
either always there or never there, so reflow isn't possible).

---

## Common options

ScrollView's distinctive surface is four options layered on top of
[Frame](frame.md)'s container tokens:

| Option                 | Type | Default     | Notes                                                                          |
| ---------------------- | ---- | ----------- | ------------------------------------------------------------------------------ |
| `scroll_direction`     | str  | `"both"`    | `"vertical"`, `"horizontal"`, or `"both"`; controls which bars exist           |
| `scrollbar_visibility` | str  | `"always"`  | `"always"`, `"never"`, `"hover"`, or `"scroll"` (see *Visibility modes* below) |
| `autohide_delay`       | int  | `1000`      | Milliseconds before scrollbars hide in `"scroll"` mode                         |
| `scrollbar_variant`    | str  | `"default"` | Forwarded as `variant=` to both `Scrollbar` instances                          |

All four are reconfigurable at runtime through `configure(...)`
and `cget(...)`; changes rewire the canvas's scroll commands and
toggle the gutter reservation as needed.

Inherited from [Frame](frame.md):

- `padding`, `width`, `height` — outer-frame geometry
- `surface`, `show_border` — themed surface tokens
- `input_background` — cascaded fill for input descendants of the
  outer frame *only*; the canvas-window content widget is reached
  via the cascade from `sv.canvas`'s parent (the ScrollView), so
  inputs inside the scroll content do pick up the token.
- `accent` is rerouted to a `surface` override on the outer frame
  (ScrollView is in `CONTAINER_CLASSES`), so `accent="primary"`
  paints the outer container — *not* the scrollbars. To tint the
  scrollbars themselves, pass `accent` to a custom `Scrollbar`
  built on `sv.canvas` and replace the bundled bars.

### Visibility modes

```python
ttk.ScrollView(app, scrollbar_visibility="always")   # default
ttk.ScrollView(app, scrollbar_visibility="never")
ttk.ScrollView(app, scrollbar_visibility="hover")
ttk.ScrollView(app, scrollbar_visibility="scroll")
```

| Mode      | Bars visible when                              | Mousewheel    | Gutter reserved |
| --------- | ---------------------------------------------- | ------------- | --------------- |
| `always`  | content overflows                              | Always        | No              |
| `never`   | Never                                          | Always        | No              |
| `hover`   | mouse over container *and* content overflows   | While hovered | Yes             |
| `scroll`  | a wheel scroll just happened *and* overflows; auto-hides after `autohide_delay` ms | Always | Yes |

In `"never"` mode, the bars are hidden but mousewheel scrolling
still works — useful for embedding a scroll region in a chrome-free
panel.

In `"hover"` mode, mousewheel scrolling is **only enabled while the
mouse is over the container**. This keeps a parent ScrollView from
hijacking the wheel for nested scrollables.

### Direction

```python
ttk.ScrollView(app, scroll_direction="both")        # default
ttk.ScrollView(app, scroll_direction="vertical")
ttk.ScrollView(app, scroll_direction="horizontal")
```

`"vertical"` or `"horizontal"` build only the matching scrollbar;
the canvas's `xscrollcommand` / `yscrollcommand` is set to `None`
on the unused axis. Mousewheel scrolling is gated on the same axis
— `<MouseWheel>` only scrolls vertical and `<Shift-MouseWheel>` only
scrolls horizontal, so a horizontal-only ScrollView ignores plain
wheel events entirely.

### Scrollbar variant

```python
ttk.ScrollView(app, scrollbar_variant="square")
```

Passed straight through to both inner `Scrollbar` widgets. Valid
values follow [Scrollbar](scrollbar.md): `"default"` (image-based
rounded thumb) and `"square"` (flat solid-color thumb). Other
values raise `BootstyleBuilderError` from the scrollbar builder.

---

## Behavior

**Mousewheel binding via a per-instance class tag.** Each
`ScrollView` creates a unique Tk bind tag (`ScrollView_<id>`) and
binds the wheel events on that tag — not on individual widgets. At
`add()` time, the tag is inserted into the `bindtags` chain of the
canvas and *every descendant of the content widget*. This is how
the wheel scrolls regardless of which child the cursor is over.

After **bulk-adding** widgets to the content frame (especially
through programmatic loops), call `refresh_bindings()` to walk the
tree again and pick up new descendants:

```python
content = sv.add()
for i in range(1000):
    ttk.Label(content, text=str(i)).pack()
sv.refresh_bindings()
```

`enable_scrolling()` and `disable_scrolling()` toggle the wheel
binding on/off without changing visibility. `"hover"` mode uses
this internally — wheel scrolling is disabled outside the hover
window.

**Platform-specific wheel deltas** are normalized:
`event.delta / 120` on Win32, raw `event.delta` on Aqua,
`<Button-4>` / `<Button-5>` on X11. The delta is converted to
`canvas.yview_scroll(units, "units")`. `<Shift-MouseWheel>` (or
`<Shift-Button-4>` / `<Shift-Button-5>` on X11) maps to
horizontal.

**Wheel events are no-ops when content fits.** Before scrolling,
the wheel handler reads `canvas.yview()` and returns early if
`first <= 0.0 and last >= 1.0`. This means a parent ScrollView
sees the wheel event after a content-fitting child ScrollView
returns, so vertically-stacked scroll regions chain correctly.

**Auto-hide when content fits.** Even in `"always"` mode, the
scrollbars are `grid_remove`d when the content is smaller than
the viewport on that axis. The bars reappear automatically as
the content grows.

**Programmatic scrolling.** The standard view protocol is exposed
on the ScrollView itself — calls are forwarded to the inner
canvas:

```python
sv.yview()                 # ("first", "last") fraction tuple
sv.yview_moveto(0.5)       # jump to 50% from the top
sv.yview("scroll", 1, "units")
sv.xview_moveto(0.0)
```

**Reconfiguration is live.** `configure(scroll_direction=...)`
rewires the canvas scroll commands, regrids the bars, and updates
visibility. `configure(scrollbar_visibility=...)` rebinds the
hover handlers, syncs the gutter, and re-evaluates which bar
should be shown right now. `configure(scrollbar_variant=...)`
forwards to both bars.

---

## Events

`ScrollView` emits no virtual events and exposes no `on_*` event
helpers. The standard Tk `<Configure>` fires on the outer frame
when its size changes, and on the inner content widget when the
content's size changes (the latter is how the canvas's
`scrollregion` stays in sync — `ScrollView` handles it
internally; rebinding `<Configure>` on the content widget will
break that hook).

To react to scroll-position changes, hook the underlying canvas
directly:

```python
def on_view_change(first, last):
    sv.vertical_scrollbar.set(first, last)
    print("at fraction", float(first))

sv.canvas.configure(yscrollcommand=on_view_change)
```

This wraps the existing scrollbar update — calling
`vertical_scrollbar.set(first, last)` first preserves the bundled
behavior, then your callback runs. Without that, the scrollbar
will stop tracking the view.

---

## When should I use ScrollView?

Use `ScrollView` when:

- you need a scrollable region of normal widgets (forms, settings
  panels, stacked cards, dynamic lists)
- you want consistent cross-platform mousewheel behavior on a
  group of widgets without binding the events yourself
- you want a built-in autohide / hover / always-on policy without
  toggling visibility manually

Prefer **[ScrolledText](../inputs/scrolledtext.md)** when the
content is a multi-line text editor or log view — it ships with a
`Text` widget pre-wired to a vertical scrollbar.

Prefer **[Scrollbar](scrollbar.md)** plus a bare
[Canvas](../primitives/canvas.md) (or `Treeview` / `Listbox`) when
you need view virtualization, custom scroll geometry, or full
control over the wheel and view protocols.

Prefer a **[PanedWindow](panedwindow.md)** when the goal is
*resizing* fixed regions, not *scrolling* through a long region.

---

## Related widgets

- **[ScrolledText](../inputs/scrolledtext.md)** — `Text` widget
  bundled with a configurable scrollbar; same visibility-mode
  vocabulary
- **[Scrollbar](scrollbar.md)** — the underlying themed scrollbar;
  exposed as `vertical_scrollbar` / `horizontal_scrollbar`
- **[Frame](frame.md)** — parent class; `surface`, `show_border`,
  `input_background` tokens behave identically
- **[Canvas](../primitives/canvas.md)** — the inner viewport;
  exposed as `sv.canvas` for advanced wiring
- **[PanedWindow](panedwindow.md)** — resize-based alternative to
  scrolling

---

## Reference

- **API reference:** [`ttkbootstrap.ScrollView`](../../reference/widgets/ScrollView.md)
- **Related guides:** [Layout](../../platform/geometry-and-layout.md),
  [Layout Properties](../../capabilities/layout-props.md),
  [Design System](../../design-system/index.md)
