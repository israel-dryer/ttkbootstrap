---
title: Notebook
---

# Notebook

`Notebook` is a thin themed wrapper around `tkinter.ttk.Notebook` —
the classic platform-style tab strip that shows one page at a time and
lets the user click tabs to switch views. Tabs are addressed by stable
**keys** (preferred), **integer indices**, or the **content widget**
itself, and the registry keeps those keys consistent across `add` /
`hide` / `remove` calls.

Navigation is **random-access** (any tab can be selected from any
other), and the widget owns its content panes — adding a tab either
wraps an existing widget or auto-creates a `Frame` for you to populate.
There is no history (no back / forward); the active selection is the
only state that matters.

!!! tip "Consider TabView for new code"
    [`TabView`](tabview.md) is the modern equivalent — closable tabs
    by default, signal-driven selection, integration with the
    `surface`/`accent` design tokens, and a richer
    [`PageStack`](pagestack.md)-backed body. `Notebook` exists for
    callers who specifically want the classic ttk look or who are
    migrating from plain `tkinter.ttk.Notebook` and need the same
    surface area. Several enriched-event features on this widget are
    currently broken (see [Events](#events) below) — TabView's
    `<<PageChange>>` event has no equivalent gap.

<figure markdown>
![notebook](../../assets/dark/widgets-notebook.png#only-dark)
![notebook](../../assets/light/widgets-notebook.png#only-light)
</figure>

---

## Basic usage

`add(text=..., key=...)` with no positional argument auto-creates a
`Frame` for the tab content and returns it; populate the frame like
any other container. The first tab added is auto-selected.

```python
import ttkbootstrap as ttk

app = ttk.App()

nb = ttk.Notebook(app, accent="primary")
nb.pack(fill="both", expand=True, padx=20, pady=20)

home = nb.add(text="Home", key="home")
ttk.Label(home, text="Home content").pack(anchor="w", padx=10, pady=10)

settings = nb.add(text="Settings", key="settings")
ttk.Label(settings, text="Settings content").pack(anchor="w", padx=10, pady=10)

app.mainloop()
```

You can also add a pre-built widget:

```python
page = ttk.Frame(nb, padding=10)
ttk.Label(page, text="Built outside the notebook").pack(anchor="w")

nb.add(page, key="external", text="External")
```

---

## Navigation model

Tabs are registered in three parallel maps:

| Map | Key | Value | Purpose |
|---|---|---|---|
| `_key_registry` | user key (str) | content widget | `nb.item(key)` lookup |
| `_tk_to_key` | Tk widget path | user key (str) | reverse lookup for events |
| ttk's tab list | (positional) | content widget | underlying ttk index order |

**Keys are stable; indices are not.** Insert / remove / reorder shifts
indices but never renames keys. Auto-generated keys (when `key=` is
omitted) follow the pattern `tab1`, `tab2`, … and never repeat for the
lifetime of the notebook.

A "tab reference" accepts any of three forms — **key**, **integer
index**, or the **content widget** itself — and `_to_tab_id`
translates all three into the Tk widget path that ttk expects. When a
string isn't found in `_key_registry`, the resolver falls back to
treating it as a Tk widget path; this fallback is what surfaces
"Invalid slave specification" errors when a stale key escapes from a
caller's bookkeeping.

```python
nb.select("settings")    # by key (preferred)
nb.select(1)             # by 0-based index
nb.select(settings)      # by widget reference
```

Selection is **imperative**: `nb.select(key)` to set, `nb.select()`
(no arg) to read the current Tk widget path. There is no `signal=` or
`variable=` channel — observers must bind a virtual event (see
[Events](#events) for the working binding name).

**The first added tab is auto-selected.** Subsequent `add()` calls do
not change selection; the user (or a programmatic `select()`) does.

---

## Common options

| Option | Type | Default | Description |
|---|---|---|---|
| `accent` | str | `'background[+1]'` | Color token tinting the active tab and (when `show_border=True`) the surrounding border. |
| `variant` | `'default'` / `'tab'` / `'bar'` / `'pill'` | `'default'` | Visual variant. `tab` is an alias for `default`. See below. |
| `surface` | str | `'background'` | Body / inactive-tab fill color. Inherits from parent in container contexts. |
| `style_options` | dict | `{}` | Forwarded to the style builder; the only consumed key is `show_border` (default `True`). |
| `padding` | int / tuple | builder default | Extra space around the tab strip and pane. |
| `height`, `width` | int | platform default | Requested size in pixels. Geometry-managed children may override. |
| `bootstyle` | str | unset | DEPRECATED — use `accent` and `variant` instead. |

**Notebook is horizontal-only.** There is no `orient=` option;
passing one raises `TclError: unknown option "-orient"`. The vertical
tab strip the source `# TODO` mentions is not yet implemented.

### Variants

All four registered variants paint the same three-element layout
(border, tab, client) but with different element images:

| Variant | Tab shape | Selected emphasis |
|---|---|---|
| `default` (alias `tab`) | Classic raised tab | Tab matches surface; rest tints with `accent`. |
| `bar` | Flat tabs along a baseline | Selected tab gets an underline in `accent`. |
| `pill` | Rounded chip per tab | Selected tab fills with `accent`; others match surface. |

`bar` and `pill` are first-class — pass `variant=` directly. The
old "deprecated `bootstyle`" path also accepts these names but skips
modern processing; prefer `variant=`.

### Per-tab options

`nb.tab(tab, option=None, **kwargs)` (alias `configure_item(key, ...)`)
configures the tab strip entry, not the content widget. Options:

| Option | Type | Effect |
|---|---|---|
| `text` | str | Tab label. Treated as a translation key — see Localization below. |
| `state` | `'normal'`, `'disabled'`, `'hidden'` | Disabled tabs render dimmed and reject clicks; hidden tabs are removed from the strip but kept in the registry. |
| `image` | `PhotoImage` | Optional image alongside or replacing the label. |
| `compound` | `'top'` / `'left'` / `'right'` / `'bottom'` / `'center'` / `'none'` | Image placement. |
| `underline` | int | 0-based index of a label character to underline. |
| `sticky` | str | How the content fills its pane area. |
| `padding` | int / tuple | Padding inside the pane area. |
| `fmtargs` | tuple / list | Format arguments for localized `text`. |

### Localization

The `text` argument to `add()`, `insert()`, and `tab()` is run through
`MessageCatalog.translate(text, *fmtargs)`. If the value isn't a
registered translation key, the literal string is returned unchanged
— so the same call shape works for plain English labels and for
catalog-driven labels. The notebook listens for
`<<LocaleChanged>>` and re-translates every registered token when
the locale flips.

```python
nb.add(key="recent", text="tabs.recent", fmtargs=("Today",))
```

### `add()` / `insert()` kwarg passthrough

When the first positional argument is `None` (the auto-frame path),
extra keyword arguments are forwarded to `Frame(self, **kwargs)`:

```python
page = nb.add(text="Settings", key="settings", padding=10, accent="primary")
# Frame is created with padding=10, accent='primary'
```

When you pass an existing widget, any extra `**kwargs` are applied via
`widget.configure(**kwargs)` — the widget's own options take effect
but do not override its construction arguments for Tk-immutable options.

```python
existing = ttk.Frame(nb, padding=5)
nb.add(existing, key="x", text="X", padding=99)
# existing.cget('padding') is now (99,) — kwargs applied
```

---

## Behavior

### Hide vs remove vs forget

| Method | Effect on tab strip | Effect on registry | Reversible |
|---|---|---|---|
| `hide(tab)` | Tab disappears from strip | Key, widget, locale token preserved | Yes — `add(widget, key=...)` re-shows it |
| `forget(tab)` | Tab disappears from strip | Locale token cleared; key still in `_key_registry` (stale) | Partially — `add(widget)` re-shows but key must be re-supplied |
| `remove(tab)` | Tab disappears from strip | Key, widget, locale token all cleared | No |

`remove(tab)` removes the tab and clears all three registries.
`forget(tab)` hides the tab and clears its locale token.
`hide(tab)` hides without clearing the registry (the tab is
re-showable via `add(widget, key=...)`).

```python
nb.remove("settings")   # gone; key freed
nb.hide("settings")     # off strip; can be restored
```

Key validation (duplicate key, empty-string key) runs before the
underlying ttk insert, so a failed `add()` leaves no orphan tab.

### Tab states

```python
nb.tab("settings", state="disabled")  # dim and unclickable
nb.tab("settings", state="hidden")    # remove from strip, keep registry
nb.tab("settings", state="normal")    # restore
```

The `disabled` state also blocks programmatic `select()`; the
`hidden` state does not (selecting a hidden tab makes it visible
again at its previous position).

### Reordering

`insert(index, child=existing_widget, ...)` moves an already-managed
widget to a new position. Keys do not change. New tabs created via
`insert(index, ...)` (no child) follow the same auto-key scheme as
`add()`.

```python
nb.insert(0, nb.item("logs"))   # move the "logs" tab to index 0
```

### State and color reactivity

Notebook is in `CONTAINER_CLASSES` like other Frame-derived widgets,
so `accent="primary"` is rerouted by the bootstyle wrapper to
`surface="primary"` for the body fill. The active-tab color is driven
separately by the variant's builder using the same `accent` value.

---

## Events

| Helper | Underlying event | Payload |
|---|---|---|
| `on_tab_changed(cb)` / `off_tab_changed(id)` | `<<NotebookTabChanged>>` | `{'current': TabRef, 'previous': TabRef, 'reason': str, 'via': str}` |
| `on_tab_activated(cb)` / `off_tab_activated(id)` | `<<NotebookTabActivate>>` (synthetic) | `{'tab': TabRef}` |
| `on_tab_deactivated(cb)` / `off_tab_deactivated(id)` | `<<NotebookTabDeactivate>>` (synthetic) | `{'tab': TabRef}` |

A `TabRef` is `{'index': int | None, 'key': str | None, 'label': str | None}`.

`reason` is one of `'user'` / `'api'` / `'hide'` / `'forget'` /
`'reorder'` / `'unknown'` and `via` is one of `'click'` / `'key'` /
`'programmatic'` / `'unknown'` — the source tracks
`_mark_api_change(reason)` at every public mutation method, but the
fields are never observed because the wrapper doesn't run.

---

## When should I use Notebook?

Use `Notebook` when:

- you specifically want the classic ttk tab look (raised tabs,
  platform native styling), or
- you're migrating from plain `tkinter.ttk.Notebook` and need the
  same surface area with a few quality-of-life additions (key-based
  references, locale-aware labels).

Prefer [`TabView`](tabview.md) when:

- this is new code — TabView's signal-driven selection, closable
  tabs, and richer Common-options surface are easier to live with
- you want a working `<<PageChange>>` event with a proper payload
  (Notebook's enriched events are broken in current code)
- you want the design-system tokens to apply consistently with
  `surface` / `accent` (TabView is built on
  [`PageStack`](pagestack.md) plus [`Tabs`](../navigation/tabs.md);
  both pieces honor the modern styling axes).

Prefer [`PageStack`](pagestack.md) when:

- the workflow is sequential (wizard, multi-step form) and benefits
  from `back()` / `forward()` history.

Prefer a [`SideNav`](../navigation/sidenav.md) when:

- you have many sections that don't fit in a single horizontal strip,
  or
- the navigation chrome should persist alongside content (not above
  it).

---

## Related widgets

- **[TabView](tabview.md)** — modern tabbed view; preferred for new
  code.
- **[PageStack](pagestack.md)** — keyed pages with back / forward
  history; the body half of TabView.
- **[Tabs](../navigation/tabs.md)** — the tab strip alone, without
  content panes; the navigation half of TabView.
- **[Frame](../layout/frame.md)** — common container for tab
  content.
- **[PanedWindow](../layout/panedwindow.md)** — split layouts
  often paired with a notebook in dual-pane editors.

---

## Reference

- **API reference:** `ttkbootstrap.Notebook`
- **Related guides:** Navigation, Layout, Design System
