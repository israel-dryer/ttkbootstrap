---
title: Containers
---

# Containers

A container is any widget that hosts children and participates in
geometry management. ttkbootstrap ships a small family of containers
that cover the common cases — plain grouping, declarative pack/grid
layout, scrolling, splitting, collapsible regions, and view stacks.
This page is the map: which container is which, what makes them
differ, and how surface and styling cascade through the tree.

For the underlying Tk mechanics (how `pack`/`grid`/`place` actually
compute placement, when sizes are realized), see
[Platform → Geometry & Layout](../../platform/geometry-and-layout.md)
and [Platform → Widget Lifecycle](../../platform/widget-lifecycle.md).
For the at-a-glance comparison of layout *mechanisms*, see
[Layout overview](index.md). This page is about the *containers* that
expose them.

---

## Container family at a glance

| Container | Role | Primary API | Geometry policy |
|---|---|---|---|
| [`Frame`](../../widgets/layout/frame.md) | Bare grouping surface | child `pack` / `grid` / `place` | child decides |
| [`Card`](../../widgets/layout/card.md) | `Frame` + `accent='card'` + border + `padding=16` | child `pack` / `grid` / `place` | child decides |
| [`LabelFrame`](../../widgets/layout/labelframe.md) | `Frame` with embedded text label | child `pack` / `grid` / `place` | child decides |
| [`PackFrame`](../../widgets/layout/packframe.md) | Auto-pack with `direction` + `gap` | child `pack()` (intercepted) | container decides side, child requests rest |
| [`GridFrame`](../../widgets/layout/gridframe.md) | Auto-grid with `rows` / `columns` / `gap` | child `grid()` (intercepted) | container auto-flows, child can override row/col |
| [`ScrollView`](../../widgets/layout/scrollview.md) | Single-child scrollable viewport | `sv.add(widget)` (or `sv.canvas` for raw access) | viewport-driven |
| [`PanedWindow`](../../widgets/layout/panedwindow.md) | Resizable horizontal/vertical splits | `pw.add(child, weight=…)` | sash-driven, user can drag |
| [`Accordion`](../../widgets/layout/accordion.md) | Vertical stack of `Expander` sections | `acc.add(title=…, …)` | mutual-exclusion-driven |
| [`Expander`](../../widgets/layout/expander.md) | Single collapsible region | `exp.add(content_widget)` | toggle-driven |
| [`Notebook`](../../widgets/views/notebook.md) | Tabbed pages (thin `ttk.Notebook` wrapper) | `nb.add(child, text=…, key=…)` | tab-selection-driven |
| [`TabView`](../../widgets/views/tabview.md) | Tabs + PageStack composite | `tv.add(key, …)` | tab-selection-driven |
| [`PageStack`](../../widgets/views/pagestack.md) | Keyed registry, one page visible at a time | `ps.add(key, …); ps.navigate(key)` | imperative, with history |

The first three (`Frame`, `Card`, `LabelFrame`) are *passive* — they
host children but don't participate in placing them; you call
`pack` / `grid` / `place` on each child yourself. The next two
(`PackFrame`, `GridFrame`) are *opinionated* — they intercept the
child's geometry call and inject defaults from the container. The
rest are *specialized* — they own the placement scheme entirely
(scrolling viewport, sash-driven splits, tab selection, etc.).

---

## Frame and its variants

`Frame` is the foundational container. It's a thin wrapper over
`ttk.Frame` with the ttkbootstrap styling tokens (`accent`,
`variant`, `surface`, `show_border`, `input_background`,
`style_options`) and the surface-cascade hook described below.

```python
import ttkbootstrap as ttk

app = ttk.App()
section = ttk.Frame(app, padding=16, surface='card', show_border=True)
ttk.Label(section, text="Group").pack()
section.pack(fill='both', expand=True)

app.mainloop()
```

**`Card`** is `Frame` with three constructor defaults
(`accent='card'`, `show_border=True`, `padding=16`) — the
container-class accent reroute then turns `accent='card'` into
`surface='card'`, so the painted background is the card surface
token. Use it when you want the framework's default elevated
section look without spelling out every option.

**`LabelFrame`** wraps `ttk.Labelframe` and renders a 1px border
with an embedded `text=` caption. Useful for form sections and
preference groups. Two notable divergences from `Frame`:

- It does **not** subclass `Frame`, so it lacks the
  surface-cascade hooks. Reconfiguring `surface` on a LabelFrame
  restyles only the LabelFrame; descendants keep their old surface.
- `show_border` is read by the style builder but is **not** captured
  into `style_options` from kwargs. Passing `show_border=False`
  raises `TclError: unknown option "-show_border"`. The border is
  effectively always on.

Both quirks are tracked on the bugs list.

---

## Auto-layout containers: PackFrame and GridFrame

`PackFrame` and `GridFrame` are `Frame` subclasses that intercept
child `pack()` / `grid()` calls and inject defaults from the
container. They sit on top of Tk's geometry managers — they do not
replace them.

`PackFrame` chooses the pack `side` from `direction`, inserts a
leading `padx` / `pady` for `gap`, and applies optional
`fill_items` / `expand_items` / `anchor_items` defaults at each
`pack()` call:

```python
import ttkbootstrap as ttk

app = ttk.App()
toolbar = ttk.PackFrame(app, direction='horizontal', gap=8, padding=8)
ttk.Button(toolbar, text='New').pack()
ttk.Button(toolbar, text='Open').pack()
ttk.Button(toolbar, text='Save').pack()
toolbar.pack(fill='x')

app.mainloop()
```

`GridFrame` exposes a CSS-grid-flavored API: `rows` / `columns`
accept either an `int` (count) or a list of size specs (`int`
weight, `'auto'`, or `'<N>px'`); `gap` is a single int or
`(col_gap, row_gap)`; `auto_flow` controls whether implicit
children fill rows or columns and whether *dense* packing fills
holes:

```python
import ttkbootstrap as ttk

app = ttk.App()
form = ttk.GridFrame(app, columns=[0, 1], gap=(8, 12), padding=12)
ttk.Label(form, text='Name').grid(sticky='w')
ttk.TextEntry(form).grid(sticky='ew')
ttk.Label(form, text='Email').grid(sticky='w')
ttk.TextEntry(form).grid(sticky='ew')
form.pack(fill='both', expand=True)

app.mainloop()
```

A child that calls `pack()` / `grid()` with explicit options can
still override the container's defaults — the per-call kwargs are
merged on top of the injected ones. See
[Layout properties](../layout-props.md) for the full pack/grid
kwarg surface and
[Spacing](spacing.md) for how `gap`, `padding`, and `density`
compose across the framework.

---

## Specialized containers

### ScrollView — scrollable viewport

`ScrollView` hosts **one child widget** inside a scrollable Canvas.
It coordinates scrollbars, propagates mousewheel events to all
descendants (via a per-instance bindtag), and gates scrollbar
visibility on whether the content overflows the viewport:

```python
import ttkbootstrap as ttk

app = ttk.App()
sv = ttk.ScrollView(app, scroll_direction='vertical')
content = sv.add()  # creates and returns a Frame parented on sv.canvas
for i in range(50):
    ttk.Label(content, text=f"Row {i}").pack(anchor='w')
sv.pack(fill='both', expand=True)

app.mainloop()
```

Defaults: `scroll_direction='both'`,
`scrollbar_visibility='always'`. The four visibility modes
(`always` / `never` / `hover` / `scroll`) and the directional
behavior are documented on the
[ScrollView page](../../widgets/layout/scrollview.md).
For a deeper look at scroll patterns, see
[Scrolling](scrolling.md).

### PanedWindow — user-resizable splits

`PanedWindow` is a thin wrapper over `ttk.Panedwindow`. Children
are added with `pw.add(child, weight=…)`; the user drags the sash
between them to resize:

```python
import ttkbootstrap as ttk

app = ttk.App()
split = ttk.PanedWindow(app, orient='horizontal')
left = ttk.Frame(split, surface='card', padding=12)
right = ttk.Frame(split, padding=12)
split.add(left, weight=1)
split.add(right, weight=2)
split.pack(fill='both', expand=True)

app.mainloop()
```

`orient` is `'horizontal'` or `'vertical'`. Sash positions can
also be set programmatically via `pw.sashpos(index, position)`.

### Accordion and Expander — collapsible regions

`Expander` is a single collapsible region — a clickable header
(icon + title + chevron) plus a content frame that toggles via
`pack()` / `pack_forget()`. Its `signal` / `variable` channel
makes it a valid radio-group member, so a stack of Expanders
sharing a `Signal` becomes a navigation accordion.

`Accordion` packages that pattern: it owns a stack of `Expander`
widgets with a built-in mutual-exclusion policy and an optional
inter-section separator strip. Use `Accordion` when the sections
are part of a single navigation group; use `Expander` directly
when each region is independent.

```python
import ttkbootstrap as ttk

app = ttk.App()
acc = ttk.Accordion(app, allow_multiple=False)
sec_a = acc.add(title='Section A')
ttk.Label(sec_a.content, text='A content').pack()
sec_b = acc.add(title='Section B')
ttk.Label(sec_b.content, text='B content').pack()
acc.pack(fill='x')

app.mainloop()
```

### Notebook, TabView, PageStack — view containers

These three are documented in detail under the
[views](../../widgets/views/pagestack.md) family but they all
play the role of *container that shows one child at a time*:

- `Notebook` — thin themed wrapper over `ttk.Notebook` with
  key-based tab registry.
- `TabView` — a `Frame` that owns a `Tabs` bar plus a `PageStack`,
  wired together so a tab click navigates the stack.
- `PageStack` — keyed registry of pages with linear push/back/forward
  history, no built-in tab UI.

---

## Surfaces cascade through descendants

`Frame.configure_style_options(surface=…)` rebuilds the Frame's
style and walks every descendant whose `_surface` matches the
old surface, retinting each to the new one
(`Frame._refresh_descendant_surfaces`,
`widgets/primitives/frame.py:110`). `input_background` cascades
the same way through `_refresh_descendant_input_backgrounds`. The
upshot: a section that toggles between page and card surfaces
recolors itself and every nested label, button, and entry without
per-widget bookkeeping.

```python
import ttkbootstrap as ttk

app = ttk.App()
section = ttk.Frame(app, padding=16, surface='content')
ttk.Label(section, text='Inside').pack()
section.pack(fill='both', expand=True)

# Later: switch to a card surface — descendants follow.
section.configure_style_options(surface='card')

app.mainloop()
```

Two caveats:

- The cascade only retints descendants whose current `_surface`
  matches the **old** surface. A descendant that was constructed
  with an explicit `surface=` override (and whose `_style_options`
  carries that override) is excluded — the explicit pin wins.
- `LabelFrame` does not subclass `Frame` and is missing the
  cascade hooks today. Children inside a LabelFrame keep their
  old surface when the LabelFrame's surface changes. Workaround:
  wrap the LabelFrame in a Frame and reconfigure the Frame.

`Card` inherits the cascade behavior from `Frame` for free.
`PackFrame`, `GridFrame`, `ScrollView`, `Accordion`, and
`Expander` all do too.

---

## Geometry managers don't mix in the same parent

Tk forbids using `pack` and `grid` on children of the **same**
parent — the second call raises:

```text
_tkinter.TclError: cannot use geometry manager grid inside .!frame
which already has slaves managed by pack
```

`place` overlays either of the others safely (it doesn't claim
the parent's geometry), but mixing pack and grid in one parent
hangs Tk's negotiation loop and is rejected at the call site.

Practical rule: pick one of pack or grid per parent. To combine
both styles, nest — a grid-managed parent can hold pack-managed
children inside a child Frame, and vice versa. `PackFrame` and
`GridFrame` make the choice explicit at the container level so a
glance at the type tells you the layout shape.

---

## When does AppShell come in?

[`AppShell`](../../widgets/application/appshell.md) is the
window-level container that composes a toolbar, a SideNav, and a
PageStack into a finished application chrome. Treat it as the
container for the *entire window*; everything covered above is
for the *body* you slot into `AppShell`'s page stack.

For toolbars and overflow chrome, see
[`Toolbar`](../../widgets/application/toolbar.md). For the full
cross-link of layout primitives to capabilities, see
[Layout overview](index.md).

---

## Where to look next

- **How does the container place its children?**
  [Layout overview](index.md) compares pack / grid / place /
  PackFrame / GridFrame / ScrollView side-by-side.
- **How do I tune padding and gaps consistently?**
  [Spacing](spacing.md) covers `padding`, `gap`, and
  density across the framework.
- **How does scrolling work end-to-end?**
  [Scrolling](scrolling.md) covers viewport
  size negotiation, mousewheel routing, and ScrollView's
  visibility modes.
- **What pack/grid/place kwargs does each widget take?**
  [Layout properties](../layout-props.md) is the per-kwarg
  reference.
- **How does Tk realize sizes during layout?**
  [Platform → Geometry & Layout](../../platform/geometry-and-layout.md)
  documents the underlying mechanics.
- **Why is `winfo_width()` zero before realization?**
  [Platform → Widget Lifecycle](../../platform/widget-lifecycle.md)
  explains the created/managed/mapped phases.
