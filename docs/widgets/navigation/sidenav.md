---
title: SideNav
---

# SideNav

`SideNav` is a themed **sidebar navigation container** — a vertical chrome
strip with an optional header, a scrollable item list, optional collapsible
groups, and an optional footer area. It manages a single selection across
all items (root, grouped, and footer) via a shared `Signal` / `tk.Variable`,
and emits `<<SelectionChanged>>` whenever that selection moves.

`SideNav` is pure navigation chrome: it does **not** own a content pane.
Pair it with a [`PageStack`](../views/pagestack.md) (or any widget you
swap from a selection listener) for the right-hand content. If you want
the sidebar plus a toolbar plus a page stack pre-wired into a window,
reach for [`AppShell`](../application/appshell.md) — `SideNav` is the
piece it builds on the left.

<figure markdown>
![sidenav](../../assets/dark/widgets-sidenav.png#only-dark)
![sidenav](../../assets/light/widgets-sidenav.png#only-light)
</figure>

---

## Basic usage

Create the sidebar, register items by key, and observe selection.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Sidebar demo", size=(900, 600))

nav = ttk.SideNav(app, title="My App")
nav.pack(side="left", fill="y")

nav.add_item("home",     text="Home",      icon="house")
nav.add_item("docs",     text="Documents", icon="file-earmark-text")
nav.add_item("settings", text="Settings",  icon="gear")

nav.select("home")
nav.on_selection_changed(lambda e: print("Selected:", e.data["key"]))

app.mainloop()
```

The first `select()` call (or the first `nav.signal.set(...)` write) sets
the active item and paints its selection indicator. `<<SelectionChanged>>`
fires on every move thereafter — user clicks and programmatic writes both
flow through the same code path.

---

## Navigation model

`SideNav` is a **random-access selection surface**: every item carries a
`key` (its unique identifier within the sidebar) and clicking the item
writes that key to a single shared variable. The variable is the only
output — `SideNav` doesn't own pages, so swapping content is your
responsibility.

| Channel | Read | Write | Reactivity |
|---|---|---|---|
| `Signal` (preferred) | `nav.signal.get()` | `nav.signal.set(k)` | `nav.signal.subscribe(cb)` → `cb(value)` |
| `tk.Variable` | `nav.variable.get()` | `nav.variable.set(k)` | `nav.variable.trace_add("write", cb)` |
| Convenience | `nav.selected_key` | `nav.select(k)` / `item.select()` | `nav.on_selection_changed(cb)` → `cb(event)` |

Pass an existing `signal=` (or `variable=`) at construction to share
state with another widget; otherwise `SideNav` creates an internal
`Signal('')`.

`select(key)` raises `KeyError` if the key is not registered. To check membership
before selecting, use `nav.node_keys()` / `nav.footer_node_keys()`.

### Item types

The sidebar has five primitives, each addressed by `key` (except
headers and separators, which are positional decoration):

| Method | Builds | Selectable | Compact-mode behavior |
|---|---|---|---|
| `add_item(key, text=, icon=, group=None, command=None)` | `SideNavItem` | yes (writes `key`) | text hidden, icon centered |
| `add_group(key, text=, icon=, is_expanded=False)` | `SideNavGroup` | no (its children are) | popup flyout on click |
| `add_header(text)` | `SideNavHeader` | no | hidden |
| `add_separator()` | `SideNavSeparator` | no | shown |
| `add_footer_item(key, text=, icon=)` | `SideNavItem` (in footer) | yes (same selection as main items) | text hidden, icon centered |

Items belong to **one** of three locations: root (no `group=`), inside a
group (`group=existing_group_key`), or the footer
(`add_footer_item(...)`). Footer items participate in the same single
selection as main items — you cannot select two items in the same
sidebar.

```python
nav.add_header("Workspace")
nav.add_item("home",  text="Home",  icon="house")
nav.add_item("inbox", text="Inbox", icon="envelope")

nav.add_separator()

nav.add_group("files", text="Files", icon="folder", is_expanded=True)
nav.add_item("local", text="Local", icon="hdd",   group="files")
nav.add_item("cloud", text="Cloud", icon="cloud", group="files")

nav.add_footer_item("settings", text="Settings", icon="gear")
```

Adding a child item with `group=` requires the group to exist
(`add_item` raises `ValueError` otherwise). Duplicate keys across any
location also raise `ValueError`.

### Lookup, removal, and reconfiguration

```python
nav.node("home")              # SideNavItem (also looks up footer items)
nav.node_keys()               # tuple of main-item keys (excludes footer)
nav.footer_node_keys()        # tuple of footer-item keys
nav.group("files")            # SideNavGroup
nav.groups()                  # all groups

nav.configure_node("home", text="Home (renamed)")
nav.remove_item("home")       # silent no-op if key missing
nav.remove_group("files")     # destroys the group and its items
```

`remove_item` is silent on a missing key (unlike `add_item`, which
raises). `remove_group` destroys both the group widget and all of its
nested items.

---

## Common options

| Option | Default | Effect |
|---|---|---|
| `title` | `""` | Header title shown in the toolbar built into the pane (only when `show_header=True`). Reconfigurable live. |
| `show_header` | `True` | Build the internal header (a `Toolbar` containing the optional back button and title). Set `False` when an external chrome (e.g. `AppShell`'s top toolbar) provides the title and toggle. |
| `show_back_button` | `False` | Add a back-arrow button to the header that emits `<<BackRequested>>` on click. SideNav itself does no history — your handler decides. |
| `collapsible` | `True` | Render a hamburger button at the top of the pane that calls `toggle_pane()`. With `False`, no hamburger is rendered (the pane can still be toggled programmatically). |
| `display_mode` | `"expanded"` | One of `"expanded"`, `"compact"`, `"minimal"`. See **Behavior → Display modes**. |
| `is_pane_open` | `True` | Initial visibility of the pane. Read by `expanded` / `minimal` modes; **ignored** by `compact` mode (which always shows the icon strip). |
| `pane_width` | `None` | Pane width in pixels for `expanded` / `minimal` modes (`None` → 280). **Ignored** by `compact` mode (which is hard-coded to 52 px). |
| `signal` | internal | Shared `Signal` for selection state. Mutually substitutes for `variable=`. |
| `variable` | internal | Shared `tk.Variable` for selection state. |
| `accent` | `"primary"` | Selection-indicator color. **Read-only after construction** — `configure(accent=…)` silently no-ops because the items' styles are baked in at construction. |
| `surface`, `padding`, `width`, `height` | inherited | Frame options. The pane interior uses `surface="chrome"` internally; the outer `SideNav` itself is a transparent Frame, so its own surface only matters if you let it show through. |

Per-item options on `add_item(...)` / `add_footer_item(...)` worth
naming: `command=` (a callable invoked on click, in addition to
selection); `is_enabled=False` (mutes interaction); `indent_level=` for
extra nesting beyond what `group=` provides.

---

## Behavior

### Display modes

The three modes differ in pane width and visibility semantics:

| Mode | Pane width | Visibility | Header / items / chevrons |
|---|---|---|---|
| `expanded` (default) | `pane_width` (default 280 px) | gated by `is_pane_open` | full — icon + text + section headers + group chevrons |
| `compact` | hard-coded 52 px | always visible | icons only — text and section headers hidden, groups open as popup flyouts |
| `minimal` | `pane_width` (default 280 px) | gated by `is_pane_open` | full — same chrome as `expanded` |

`compact` is the only mode that suppresses text labels, section headers,
and inline group expansion (groups instead pop a flyout to the right
when clicked). `expanded` and `minimal` are visually identical when
both have `is_pane_open=True` — the distinction is conceptual:
`expanded` describes a sidebar that's typically visible and only
occasionally hidden; `minimal` describes one that's typically hidden
and only briefly opened.

!!! warning "`display_mode='minimal'` does not start hidden"
    Despite the name, `display_mode='minimal'` defaults `is_pane_open=True`
    — the pane is shown in full at startup. To get a sidebar that
    starts hidden and opens on toggle, pass both
    `display_mode='minimal', is_pane_open=False`. The `compact` /
    `expanded` toggle dance via `toggle_pane()` is a separate path; see
    the next note.

### Pane state vs display mode

`SideNav` exposes two orthogonal axes that the documentation and the
hamburger-button affordance can easily blur:

- **`display_mode`** — `expanded` / `compact` / `minimal`. Set via
  `set_display_mode(mode)`; emits `<<DisplayModeChanged>>`.
- **`is_pane_open`** — pane visibility (only meaningful for
  `expanded` / `minimal`). Set via `open_pane()` / `close_pane()`;
  emits `<<PaneToggled>>`.

`toggle_pane()` chooses which axis to flip based on the current mode:

| Current mode | What `toggle_pane()` does | What it doesn't do |
|---|---|---|
| `expanded` | Switches to `compact` (emits `<<DisplayModeChanged>>`) | Doesn't hide the pane |
| `compact` | Switches to `expanded` (emits `<<DisplayModeChanged>>`) | Doesn't hide the pane |
| `minimal` | Toggles `is_pane_open` (emits `<<PaneToggled>>`) | Doesn't change the mode |

!!! warning "Hamburger ≠ show / hide in expanded mode"
    In `expanded` and `compact` modes, clicking the hamburger does **not**
    show or hide the sidebar — it shrinks `expanded` to `compact` (or
    grows it back). To hide the pane on hamburger click, use
    `display_mode='minimal'` (then `toggle_pane()` toggles visibility),
    or wire the hamburger to `nav.close_pane()` / `nav.open_pane()`
    yourself.

### Groups

In `expanded` / `minimal` modes, a `SideNavGroup` renders as a clickable
header with a chevron (▸ collapsed, ▾ expanded). Clicking the header
toggles inline expansion and emits `<<GroupExpanding>>` /
`<<GroupCollapsed>>` *on the group widget* (see Events). The selection
indicator on the group lights up when any of its child items are
currently selected, even when the group is collapsed.

In `compact` mode, the group renders as an icon-only button. Clicking
it pops a [`ContextMenu`](../actions/contextmenu.md) flyout to the right
listing the group's items; selecting one writes its key to the
selection variable just like a direct click would.

`group.expand()` / `group.collapse()` / `group.toggle()` are no-ops in
`compact` mode (the popup is the only affordance).

### Header

When `show_header=True`, the pane builds an internal `Toolbar` at the
top containing (in order): the optional back button (only when
`show_back_button=True`) and the title label (only when `title=` is
set). The hamburger button **and** its trailing separator live above
the header in the pane (driven by `collapsible`), so the visual order
from top to bottom is:

```
hamburger button       (if collapsible)
─────                  (separator)
[← back] [title]       (toolbar, if show_header=True)
… items …              (scrollable)
─────                  (footer separator, if any footer items)
… footer items …
```

In `compact` mode the title label is hidden but the back button and
hamburger remain; section headers (`add_header(...)`) are hidden too.

### Reconfiguring after construction

- `configure(title="…")` — live, retargets the title label.
- `configure(accent="…")` — **silent no-op**. The accent is baked into
  every item's resolved ttk style at construction; flipping it later
  would require rebuilding every item, which `SideNav` does not do.
- `configure_node(key, text=…, icon=…, …)` — forwards to the item;
  live for the options that have configure delegators on `SideNavItem`.

---

## Events

`SideNav` itself emits three events; individual items and groups emit
two more *on themselves* (Tk virtual events do not bubble through the
parent chain, so binding on the SideNav silently no-ops for those):

| Event | Fires on | When | `event.data` |
|---|---|---|---|
| `<<SelectionChanged>>` | the **SideNav** | the bound variable changes (user click or programmatic write) | `{"key": <new_key>}` |
| `<<PaneToggled>>` | the **SideNav** | `open_pane()` / `close_pane()` / `toggle_pane()` (when in `minimal` mode) | `{"is_open": bool}` |
| `<<DisplayModeChanged>>` | the **SideNav** | `set_display_mode(mode)` or `toggle_pane()` (when in `expanded` / `compact` mode) | `{"mode": <new_mode>}` |
| `<<BackRequested>>` | the **SideNav** | header back button is clicked (when `show_back_button=True`) | *none* |
| `<<ItemInvoked>>` | the **SideNavItem** clicked | item is clicked (or `item.select()` / `nav.select(key)` writes its key) | `{"key": <item_key>}` |
| `<<GroupExpanding>>` | the **SideNavGroup** | the group expands inline (only in `expanded` / `minimal` modes) | `{"key": <group_key>}` |
| `<<GroupCollapsed>>` | the **SideNavGroup** | the group collapses inline | `{"key": <group_key>}` |

`SideNav` ships convenience helpers for the four sidebar-level events
only; for per-item or per-group events, bind on the returned widget:

| Helper | Backed by | Callback receives | Unbind |
|---|---|---|---|
| `nav.on_selection_changed(cb)` | `bind('<<SelectionChanged>>')` | `cb(event)` — `event.data = {"key": …}` | `nav.off_selection_changed(bind_id)` |
| `nav.on_pane_toggled(cb)` | `bind('<<PaneToggled>>')` | `cb(event)` — `event.data = {"is_open": …}` | `nav.off_pane_toggled(bind_id)` |
| `nav.on_back_requested(cb)` | `bind('<<BackRequested>>')` | `cb(event)` | `nav.off_back_requested(bind_id)` |

There's no `on_display_mode_changed` helper; bind directly:
`nav.bind("<<DisplayModeChanged>>", cb)`.

For **selection** specifically, `nav.signal.subscribe(cb)` is the
"reactive" alternative — the callback receives the new value
(`cb(value)`), not a Tk event, and fires for every variable write.
Pick the helper or the signal subscription depending on whether you
want the event object or just the value.

```python
def on_selection(event):
    key = event.data["key"]
    print(f"User wants {key}")

nav.on_selection_changed(on_selection)

# Per-item:
home_item = nav.add_item("home", text="Home", icon="house")
home_item.on_invoked(lambda e: print("home invoked"))
```

---

## When should I use SideNav?

Use `SideNav` when:

- the app has a primary navigation surface that should remain visible
  (settings, dashboards, document workspaces, multi-section tools)
- you want collapsible groups, section headers, and a footer area in
  the same pane
- you need fine-grained control over the sidebar's chrome (custom
  toolbar, custom toggle affordances, external content wiring)

Prefer [`AppShell`](../application/appshell.md) when:

- you want the sidebar pre-wired into a window with a toolbar and a
  page stack — `AppShell` builds a `SideNav` for you and routes
  selection through to a `PageStack`. Reach for `SideNav` directly
  when you need a layout `AppShell` doesn't allow.

Prefer [`Tabs`](tabs.md) when:

- the navigation is contextual (tool modes, filter sets, view presets)
  rather than primary, or when a horizontal strip fits the screen
  better than a vertical column.

Prefer a custom layout with `Signal`-bound widgets when:

- the navigation isn't really a sidebar (a stepper, a wizard, a
  custom table-of-contents) — in those cases compose `Signal` +
  domain-specific widgets directly.

---

## Related widgets

- [`AppShell`](../application/appshell.md) — primary use case for
  `SideNav` (built into the shell on the left).
- [`Tabs`](tabs.md) — horizontal tab-bar selection alternative.
- [`PageStack`](../views/pagestack.md) — the typical content target
  driven by `SideNav`'s selection signal.
- [`Toolbar`](../application/toolbar.md) — what `SideNav` builds for its internal
  header and what `AppShell` builds at the top.
- [`ContextMenu`](../actions/contextmenu.md) — the popup flyout type
  used by `SideNavGroup` in `compact` mode.

---

## Reference

- **API reference:** [`ttkbootstrap.SideNav`](../../reference/widgets/SideNav.md)
- **Related guides:** [Navigation](../../guides/navigation.md), [Reactivity](../../guides/reactivity.md), [App Structure](../../guides/app-structure.md)
