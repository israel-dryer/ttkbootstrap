---
title: AppShell
---

# AppShell

`AppShell` is an **opinionated application shell** — an `App` subclass
that wires a [`Toolbar`](../navigation/toolbar.md), a
[`SideNav`](../navigation/sidenav.md), and a
[`PageStack`](../views/pagestack.md) into the standard desktop layout
(toolbar across the top, sidebar on the left, pages filling the rest).
You instantiate it as the root window of your application — the same
way you would [`App`](app.md) — and add pages instead of building the
outer layout yourself.

Choose `AppShell` when your app has clearly separated views behind a
sidebar. Choose [`App`](app.md) when it doesn't.

<figure markdown>
![appshell](../../assets/dark/widgets-appshell.png#only-dark)
![appshell](../../assets/light/widgets-appshell.png#only-light)
</figure>

---

## Basic usage

`AppShell` builds the toolbar, sidebar, and page stack for you. Your
job is to add pages: each `add_page()` call creates a sidebar item *and*
a content `Frame` for the page in one step, and returns the `Frame` so
you can build into it.

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(1000, 650))

home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Welcome!").pack(padx=20, pady=20)

docs = shell.add_page("docs", text="Documents", icon="file-earmark-text")
ttk.Label(docs, text="Your documents.").pack(padx=20, pady=20)

shell.mainloop()
```

The first page added is selected automatically. Subsequent pages are
mounted only when the user navigates to them (via the sidebar or a
programmatic `shell.navigate(key)`).

!!! tip "Scaffolding"
    `ttkb start MyApp --template appshell` scaffolds a complete
    `AppShell` project — `main.py`, a `pages/` directory with one
    file per page, and `ttkb.toml` — so you can skip the
    boilerplate when starting fresh. `ttkb add page <Name>` then
    adds a new page module and wires it into `main.py`. See the
    [CLI reference](../../platform/cli.md) for the full set of
    commands.

---

## Anatomy

`AppShell` builds the outer structure once at construction. You cannot
change the body layout, but each component is optional:

```
AppShell  (the Tk root window)
├── Toolbar         (top, fill='x') — when show_toolbar=True
│   ├── hamburger button             # toggles SideNav (only when show_nav=True)
│   ├── separator
│   ├── title label                  # only when title="..." is set
│   ├── spacer                       # subsequent buttons sit at the right edge
│   └── window controls              # min/max/close, when show_window_controls=True
└── body Frame      (top, fill='both', expand=True)
    ├── SideNav     (left, fill='y')          — when show_nav=True
    └── PageStack   (left, fill='both', expand=True)
        ├── page "home"
        ├── page "docs"
        └── ...
```

The toolbar's pre-populated layout (hamburger → separator → title →
spacer) is fixed; user-added buttons land **after** the spacer and
align to the right of the bar.

The body is a regular `Frame` with a left-to-right pack layout — there
is no way to put the sidebar on the right or the toolbar at the bottom.
If you need a non-standard arrangement, build on `App` directly with the
same component classes (`Toolbar`, `SideNav`, `PageStack`).

!!! note "Custom toggles when the toolbar is hidden"
    With `show_toolbar=False, show_nav=True`, the hamburger button (which
    lives on the toolbar) is gone and the SideNav header is also
    suppressed — so there is **no built-in UI** to toggle the sidebar.
    The sidebar is still collapsible programmatically via
    `shell.nav.toggle_pane()`; wire your own keyboard shortcut or button
    if users need to collapse it.

---

## Window options

`AppShell` extends `App`, so it accepts every windowing option that
[`App`](app.md) does (`title`, `theme`, `size`, `position`, `minsize`,
`maxsize`, `resizable`, `icon`, `alpha`, plus the full `settings=`
surface). On top of those, it adds shell-specific options:

| Option | Default | Effect |
|---|---|---|
| `frameless` | `False` | Remove the OS title bar and borders. Implies `show_window_controls=True` and `draggable=True` so the toolbar can host the controls and act as the drag surface. |
| `show_toolbar` | `True` | Include the top toolbar. |
| `show_window_controls` | `False` | Show minimize / maximize / close buttons in the toolbar. |
| `draggable` | `False` | Drag the window by dragging the toolbar's empty space. |
| `toolbar_density` | `"default"` | Toolbar button density (`"default"` or `"compact"`). |
| `show_nav` | `True` | Include the sidebar. With `False`, `add_page()` raises `RuntimeError` — use `shell.pages.add(...)` directly instead. |
| `nav_display_mode` | `"expanded"` | Initial sidebar mode (`"expanded"` for full width with text, `"compact"` for icons only, `"minimal"` for full width but designed to be hidden via the hamburger). |
| `nav_accent` | `"primary"` | Accent token for the SideNav selection indicator. |

`frameless=True` is the cleanest path to a fully custom window: the OS
chrome is gone, the toolbar grows minimize / maximize / close buttons,
and the toolbar's empty space becomes the drag handle.

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(
    title="Custom Window",
    theme="darkly",
    size=(1100, 700),
    frameless=True,
)

shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)

home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="No OS chrome — fully custom!").pack(padx=20, pady=20)

shell.mainloop()
```

Window state, theme, locale, persistence, and platform behavior all flow
through `AppSettings` exactly as on `App`. See the [App Settings
guide](../../guides/app-settings.md) for the full inventory.

---

## Building the shell

`add_page(key, text="", icon=None, page=None, group=None,
is_footer=False, scrollable=False, **nav_kwargs)` is the central API.
It performs three actions in one call:

1. registers a sidebar item with the given `key`
2. creates (or accepts) a content widget in the page stack under the
   same key
3. auto-navigates to it if it's the first page added

The return value is the page widget you build into:

```python
page = shell.add_page("settings", text="Settings", icon="gear")
ttk.Label(page, text="Settings content").pack(padx=20, pady=20)
```

Pass `page=` to substitute your own widget — useful when a page is a
self-contained class:

```python
import ttkbootstrap as ttk

class HomePage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Home").pack(padx=20, pady=20)

shell = ttk.AppShell(title="Class Pages", size=(900, 600))
shell.add_page("home", text="Home", icon="house", page=HomePage(shell.pages))

shell.mainloop()
```

Pass `scrollable=True` to wrap the page in a
[`ScrollView`](../layout/scrollview.md) with vertical scrolling. The
returned widget is the scrollable content frame, so packed children
scroll naturally:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="Scrollable", size=(900, 600))

docs = shell.add_page("docs", text="Documents", icon="folder", scrollable=True)
for n in range(50):
    ttk.Label(docs, text=f"Item {n}").pack(anchor="w", padx=20)

shell.mainloop()
```

### Groups, headers, separators, footer items

The sidebar has four structural primitives. Each is forwarded through
to the underlying [`SideNav`](../navigation/sidenav.md):

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="Sidebar primitives", size=(1000, 650))

# Header: a non-interactive section title between items
shell.add_header("Workspace")

shell.add_page("home",  text="Home",     icon="house")
shell.add_page("inbox", text="Inbox",    icon="envelope")

# Separator: a thin divider line
shell.add_separator()

# Group: nest pages under a collapsible header
shell.add_group("files", text="Files", icon="folder", is_expanded=True)
shell.add_page("local", text="Local", icon="hdd",   group="files")
shell.add_page("cloud", text="Cloud", icon="cloud", group="files")

# Footer: items pinned to the bottom of the sidebar
shell.add_page("settings", text="Settings", icon="gear", is_footer=True)

shell.mainloop()
```

`is_footer=True` and `group=` are mutually exclusive — a page belongs
to the footer or to a group, not both. Headers and separators are
inserted at the current end of the main item list and don't interact
with selection.

---

## Navigation

```python
shell.navigate("settings")        # programmatic nav (sidebar + page)
shell.select("settings")          # alias for navigate()
print(shell.current_page)         # "settings" — the active page key, or None
```

`navigate(key, data=None)` updates the sidebar's selected item *and*
swaps the page stack to the matching page. Sidebar clicks call the
same path internally, so user navigation and programmatic navigation
fire the same events. The optional `data=` argument is delivered to the
target page through the `<<PageWillMount>>` / `<<PageMount>>` lifecycle
events — see [PageStack](../views/pagestack.md) for the full lifecycle.

To observe navigation, bind `on_page_changed`:

```python
def on_change(event):
    payload = event.data
    print(f"{payload['prev_page']} → {payload['page']}")

shell.on_page_changed(on_change)
```

`on_page_changed(callback)` is a thin alias for
`shell.pages.on_page_changed(callback)` — it binds to the underlying
[`PageStack`](../views/pagestack.md)'s `<<PageChange>>` event and
returns a bind id (passable to `shell.off_page_changed(bind_id)`). The
callback receives a Tk event whose `event.data` carries the navigation
payload:

| Key | Meaning |
|---|---|
| `page` | Key of the page just navigated to |
| `prev_page` | Key of the previous page (or `None` on the first navigation) |
| `prev_data` | Data dict that was passed to the previous `navigate()` call |
| `nav` | `"push"`, `"back"`, or `"forward"` — how the navigation happened |
| `index` | Index of the current entry in the back/forward history |
| `length` | Total length of the history |
| `can_back` | `True` if `shell.pages.back()` is valid |
| `can_forward` | `True` if `shell.pages.forward()` is valid |

If you passed `data={...}` to `navigate()`, those keys are merged into
`event.data` at the top level (so caller-supplied fields sit alongside
the framework keys above).

For per-page lifecycle hooks (mount, unmount, will-mount), bind on the
page widget directly rather than on the shell.

---

## Components

For anything `AppShell`'s own API doesn't surface, drop down to the
underlying widgets via these properties:

| Property | Type | When present |
|---|---|---|
| `shell.toolbar` | [`Toolbar`](../navigation/toolbar.md) or `None` | Only when `show_toolbar=True` |
| `shell.nav` | [`SideNav`](../navigation/sidenav.md) or `None` | Only when `show_nav=True` |
| `shell.pages` | [`PageStack`](../views/pagestack.md) | Always |
| `shell.current_page` | `str` (page key) or `None` | Always |

```python
# Add right-aligned toolbar buttons (they sit after the built-in spacer):
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)
shell.toolbar.add_button(icon="gear", command=open_settings)

# Subscribe to sidebar selection independently of page changes:
shell.nav.on_selection_changed(lambda e: log(e.data["key"]))

# Use the page stack's history when running without a sidebar:
if shell.pages.can_back():
    shell.pages.back()
```

The handles return the same widget instances the shell built — mutating
them mutates the shell. There is no separate "shell view" wrapper.

When `show_nav=False`, `add_page()` is unavailable (raises
`RuntimeError`); use `shell.pages.add(key, page=...)` to register pages
directly on the stack and drive navigation from your own code or
keyboard shortcuts.

---

## When should I use AppShell?

Use `AppShell` when:

- the app has a small-to-medium set of top-level destinations behind a
  sidebar (settings panes, dashboards, lists, multi-mode tools)
- you want a frameless / custom-chromed window without rebuilding the
  toolbar and drag handling yourself
- you'd rather configure a layout than build it

Prefer [`App`](app.md) when:

- the app is a single view (a calculator, a one-screen utility, a
  dialog-driven tool)
- you need a layout `AppShell` doesn't allow (sidebar on the right,
  toolbar at the bottom, multi-pane workspace)
- you want full control over the outer structure

Prefer [`Toplevel`](toplevel.md) for **secondary** windows (settings
panels, inspectors, tool palettes) — `AppShell` is the *primary*
window of the process, instantiated once.

---

## Related widgets

- [`App`](app.md) — the underlying root window class without the layout opinions
- [`Toplevel`](toplevel.md) — secondary windows that share the App's theme and event loop
- [`Toolbar`](../navigation/toolbar.md) — the toolbar widget AppShell builds at the top
- [`SideNav`](../navigation/sidenav.md) — the sidebar widget AppShell builds on the left
- [`PageStack`](../views/pagestack.md) — the page container AppShell builds on the right

---

## Reference

- **API reference:** [`ttkbootstrap.AppShell`](../../reference/app/AppShell.md)
- **Related guides:** [App Structure](../../guides/app-structure.md), [Navigation](../../guides/navigation.md), [Toolbars](../../guides/toolbars.md)
