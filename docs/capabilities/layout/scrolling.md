# Scrolling

Scrolling lets a widget show content larger than its viewport while keeping
the rest of the window fixed. Unlike CSS, Tk does not auto-scroll any widget
when its content overflows — every scroll path is wired up explicitly.
ttkbootstrap exposes three approaches.

## At a glance

| Path | Use when | API surface |
|---|---|---|
| Built-in scroll on the widget | The widget natively supports `xscrollcommand` / `yscrollcommand` (Text, Canvas, Listbox, Treeview, ListView, TableView, …) | Pair with [`Scrollbar`](../../widgets/layout/scrollbar.md) using the two-way protocol below |
| [`ScrollView`](../../widgets/layout/scrollview.md) | The content is a tree of arbitrary widgets (form rows, cards, mixed content) | One option (`scroll_direction`) controls the axis; one option (`scrollbar_visibility`) controls the bars |
| Pre-bundled composite | The widget already exists with bars attached | [`ScrolledText`](../../widgets/inputs/scrolledtext.md), [`TableView`](../../widgets/data-display/tableview.md), [`TreeView`](../../widgets/data-display/treeview.md), [`ListView`](../../widgets/data-display/listview.md) |

The choice depends on what you're scrolling, not on aesthetics. Picking the
wrong path produces working but fragile code — for example, hand-wiring a
Canvas + Scrollbar around a Frame tree when `ScrollView` would do it for you,
or wrapping a `Text` widget in a `ScrollView` when the Text widget already
scrolls itself.

## The two-way scrollbar protocol

Every Tk widget that scrolls and every `ttk.Scrollbar` participates in the
same symmetric contract. Wiring only one half breaks one direction silently.

```python
import ttkbootstrap as ttk

app = ttk.App()

text = ttk.Text(app, height=8, width=40)
ys = ttk.Scrollbar(app, orient="vertical", command=text.yview)
text.configure(yscrollcommand=ys.set)

text.pack(side="left", fill="both", expand=True)
ys.pack(side="right", fill="y")

app.mainloop()
```

The two halves:

- `command=text.yview` — the scrollbar drives the target. Tk calls
  `text.yview(*args)` on drag, click-arrow, page-jump, etc.
- `text.configure(yscrollcommand=ys.set)` — the target drives the scrollbar.
  The widget calls `ys.set(first, last)` whenever its view changes.

Forget the `command=` half and the bar appears but does nothing. Forget the
`yscrollcommand=` half and dragging the bar still scrolls, but the thumb
won't track when content size changes or when you scroll via mouse wheel,
arrow keys, `see(...)`, or any other view-change path.

Same shape for the horizontal axis with `xview` / `xscrollcommand` and an
`orient="horizontal"` scrollbar. See [Scrollbar](../../widgets/layout/scrollbar.md)
for the inherited methods (`set` / `get` / `delta` / `fraction`).

## Scrolling arbitrary widget trees: ScrollView

`ScrollView` wraps a `tkinter.Canvas` and gives you a content frame inside
it. The bars, the canvas, the scrollregion updates, and the mouse-wheel
bindings are all wired up for you.

```python
import ttkbootstrap as ttk

app = ttk.App()

sv = ttk.ScrollView(app, scroll_direction="vertical")
sv.pack(fill="both", expand=True)

content = sv.add()
for i in range(50):
    ttk.Button(content, text=f"Item {i}").pack(fill="x", padx=8, pady=2)

app.mainloop()
```

A few mechanics that catch first-time users:

**Parent your widgets correctly.** `sv.add()` returns a `Frame` parented on
the inner canvas (`sv.canvas`), not on the `ScrollView`. Pack/grid/place
your content into that returned frame. If you instead build widgets parented
to `sv` itself, they will not scroll — they live next to the canvas, not
inside it.

**Scrollregion updates run automatically.** ScrollView binds `<Configure>`
on the content frame and calls `canvas.configure(scrollregion=...)` whenever
the frame's size changes. Add or remove children freely; the scrollbar thumb
adjusts on the next idle tick. There is one edge case: if you add many
widgets in a tight loop and want the bindings refreshed mid-batch, call
`sv.refresh_bindings()` afterwards.

**Mouse wheel handling is normalized.** ScrollView assigns each instance a
unique bindtag (`ScrollView_<id>`) and binds `<MouseWheel>` /
`<Shift-MouseWheel>` (or `<Button-4>` / `<Button-5>` on X11) on that tag.
Every descendant of the content frame gets the tag walked into its
`bindtags()` — so the wheel works no matter where the cursor is inside the
viewport. Wheel events are no-ops when the content fits on that axis,
which means nested ScrollViews chain correctly: the outer view receives
the wheel only after the inner view bottoms out.

**Bars reserve a gutter in `hover` and `scroll` modes.** When
`scrollbar_visibility='hover'` or `'scroll'`, ScrollView reserves the
scrollbar's natural width in the grid even while the bar is hidden — the
canvas never resizes when the bar pops in. In `'always'` and `'never'`
modes there is no gutter to reserve (the bar is permanent or absent).

`scroll_direction` and `scrollbar_visibility` are construction-time
defaults but live-reconfigurable. See [ScrollView](../../widgets/layout/scrollview.md)
for the full per-option behavior matrix and the visibility modes.

## Pre-bundled scrollers

Three widgets ship with their scrollbars already wired:

- [`ScrolledText`](../../widgets/inputs/scrolledtext.md) — wraps `tkinter.Text`
  with a vertical bar (and horizontal when `wrap='none'`). Use this instead
  of building Text + Scrollbar by hand.
- [`TableView`](../../widgets/data-display/tableview.md) — vertical scrollbar
  is part of the chrome; horizontal scrolling is automatic when columns
  overflow.
- [`TreeView`](../../widgets/data-display/treeview.md) and
  [`ListView`](../../widgets/data-display/listview.md) — both ship as plain
  `ttk.Treeview` underneath; if you need scrollbars on the bare TreeView,
  wrap it in a `ScrollView` *or* attach a `Scrollbar` to its native `xview`
  / `yview` (TreeView itself supports the protocol from the previous
  section).

## Choose an axis intentionally

`scroll_direction` accepts `'vertical'`, `'horizontal'`, or `'both'`. Three
considerations matter:

1. **Reading flow.** Vertical for stacked rows; horizontal scrolling for a
   form is a usability bug.
2. **Wheel reach.** On both axes the wheel scrolls vertically by default;
   `<Shift-MouseWheel>` (Windows / macOS) or `<Shift-Button-4|5>` (X11)
   scrolls horizontally. Users who don't know about Shift will not find
   horizontal-only content.
3. **Gutter cost.** `'both'` always reserves space for both bars. If you
   only need one axis, set the direction explicitly — the unused gutter
   eats real pixels.

## Common pitfalls

- **Wiring only `command=` or only `xscrollcommand=`.** The bar appears
  but the thumb never moves — or it tracks the user's drag but loses sync
  on programmatic scrolls. Always wire both halves.
- **Building widgets parented to `ScrollView` itself.** Only the widget
  passed to (or returned by) `sv.add()` actually scrolls. Pack your content
  into that frame, not into the `ScrollView`.
- **Wrapping a `Text` or `Canvas` in `ScrollView`.** Both already scroll
  natively. Wrapping them produces a scrollable canvas containing a
  scrollable widget, with two thumbs that fight for the wheel.
- **Mixing geometry managers in the scrolled content.** The content frame
  obeys the same Tk rule as any other frame — pack OR grid, not both.
  See [Containers](containers.md).
- **Forgetting that `place()` doesn't grow the parent.** If you place
  widgets into the content frame, the frame's `winfo_reqwidth/height` stays
  small and the scrollregion never expands. Use `pack` or `grid` for
  scrolled content; reserve `place` for overlays.

## Related reading

- Want to scroll a tree of widgets? → [ScrollView widget](../../widgets/layout/scrollview.md)
- Need just the bar? → [Scrollbar widget](../../widgets/layout/scrollbar.md)
- Wrapping multi-line text? → [ScrolledText widget](../../widgets/inputs/scrolledtext.md)
- Wondering how `<MouseWheel>` differs across platforms? → [Platform → Events and bindings](../../platform/events-and-bindings.md)
- Wondering how Canvas drives scrolling under the hood? → [Canvas widget](../../widgets/primitives/canvas.md)
