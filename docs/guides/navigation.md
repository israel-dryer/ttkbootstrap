---
title: Navigation
---

# Navigation

Navigation is how users move between views in your application. ttkbootstrap
ships three patterns covering most desktop app shapes: a sidebar pattern
(`AppShell` / `SideNav`), a tab pattern (`TabView` / `Tabs`), and a stack
pattern (`PageStack`). All three are built on the same building blocks, so
you can mix them inside one window when the structure calls for it.

This guide covers:

- choosing a pattern,
- the `AppShell` shortcut and its component pieces,
- tabs (modern `TabView`, low-level `Tabs`, legacy `Notebook`),
- `PageStack` for stack-based navigation with history,
- combining patterns and rolling your own,
- programmatic navigation, deep linking, and state preservation.

---

## Choosing a pattern

| Pattern         | Shape                                | Best for                                                  | Widgets                  |
|-----------------|--------------------------------------|-----------------------------------------------------------|--------------------------|
| **Sidebar**     | Vertical nav, many top-level items   | Most desktop apps; navigation is the primary surface      | `AppShell`, `SideNav`    |
| **Tabs**        | Horizontal/vertical bar of peers     | 2 to 7 peer sections; users switch back and forth freely  | `TabView`, `Tabs`        |
| **Stack**       | Single page at a time, with history  | Wizards, flows, drill-down (list → detail → edit)         | `PageStack`              |

For most applications, **start with `AppShell`**. It bundles a toolbar, a
sidebar, and a `PageStack` into one window and exposes the underlying
widgets when you need to reach for them. Drop down to `SideNav` + `PageStack`
if you need custom layout, or to `TabView` / `PageStack` directly if the
sidebar pattern doesn't fit.

You can nest patterns. Tabs inside a sidebar page is common, and a
`PageStack` inside a tab is fine for drill-downs scoped to that tab.

---

## AppShell

`AppShell` is the fastest way to build a navigation-based application. It
extends `App` and wires a `Toolbar`, `SideNav`, and `PageStack` into the
common toolbar + sidebar + content layout. Each component is exposed as a
property (`shell.toolbar`, `shell.nav`, `shell.pages`) for direct access.

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(1000, 650))

# add_page() creates a nav item AND a page Frame in one call.
home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Welcome!").pack(padx=20, pady=20)

docs = shell.add_page("docs", text="Documents", icon="file-earmark-text")
ttk.Label(docs, text="Your documents.").pack(padx=20, pady=20)

# Toolbar buttons appear on the right (after the title).
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)

shell.mainloop()
```

The first page added becomes the active page automatically. Selecting a nav
item navigates the underlying `PageStack`; the two are kept in sync.

### Pages, groups, and footer items

`add_page()` accepts `key`, `text`, `icon`, `page`, `group`, `is_footer`,
and `scrollable`:

```python
# Sectioned with a group header
shell.add_group("files", text="Files", icon="folder")
shell.add_page("local", text="Local",  icon="hdd",   group="files")
shell.add_page("cloud", text="Cloud",  icon="cloud", group="files")

# Pinned to the bottom of the sidebar
shell.add_page("settings", text="Settings", icon="gear", is_footer=True)

# Wrapped in a vertical ScrollView for long content
long = shell.add_page("report", text="Report", icon="file", scrollable=True)
for i in range(50):
    ttk.Label(long, text=f"Row {i}").pack(anchor="w", padx=20)
```

Pass `page=<existing widget>` to use a pre-built widget instead of letting
`AppShell` create a Frame for you. Other useful navigation methods:
`add_header(text)`, `add_separator()`.

### Programmatic navigation

```python
shell.navigate("settings")            # by key
shell.select("settings")              # alias for navigate()
print(shell.current_page)             # 'settings'

# Pass data along to the page (read it from event.data on <<PageMount>>).
shell.navigate("docs", data={"document_id": 42})

# React to page changes
shell.on_page_changed(lambda e: print(f"now on: {shell.current_page}"))
```

### When to reach past `AppShell`

- **Custom toolbar layout, multiple toolbars, or no toolbar** — assemble
  `SideNav` + `PageStack` (and a `Toolbar`, optionally) yourself.
- **Horizontal tabs as the top-level nav** — use `TabView`.
- **No navigation at all** — use plain `App`.

!!! link "AppShell reference"
    See [AppShell](../widgets/application/appshell.md) for all options
    including `frameless` mode, `nav_display_mode`, and component access.

---

## SideNav (standalone sidebar)

`SideNav` is the sidebar widget that `AppShell` uses internally. Use it when
you want sidebar navigation but need control over the surrounding layout
(custom toolbar position, dual sidebars, status bar, etc.).

A standalone `SideNav` does not own the content area — wire it to a
`PageStack` yourself:

```python
import ttkbootstrap as ttk

app = ttk.App(title="SideNav + PageStack", size=(900, 600))

nav = ttk.SideNav(app)
nav.pack(side="left", fill="y")

stack = ttk.PageStack(app)
stack.pack(side="left", fill="both", expand=True)

# Add nav items and pages with matching keys
nav.add_item("home", text="Home", icon="house")
home = stack.add("home", padding=20)
ttk.Label(home, text="Welcome!").pack()

nav.add_item("settings", text="Settings", icon="gear")
settings = stack.add("settings", padding=20)
ttk.Label(settings, text="Settings page").pack()

# Wire selection to navigation
nav.on_selection_changed(lambda e: stack.navigate(e.data["key"]))

nav.select("home")  # initial selection (also triggers navigation)
app.mainloop()
```

### Display modes

`SideNav` supports three layouts via `display_mode`:

| Mode       | Description                                                |
|------------|------------------------------------------------------------|
| `expanded` | Full width with icon + text (default).                     |
| `compact`  | Narrow, icon-only; groups become popup menus on click.     |
| `minimal`  | Hidden until toggled open.                                 |

```python
nav = ttk.SideNav(app, display_mode="compact")

nav.toggle_pane()                  # expanded ↔ compact (or open ↔ closed in minimal)
nav.set_display_mode("expanded")   # set explicitly
```

`AppShell` exposes the same option as `nav_display_mode`.

### Groups, headers, separators, and footer items

```python
nav.add_header(text="Workspace")
nav.add_group("files", text="Files", icon="folder")
nav.add_item("local",  text="Local", icon="hdd",   group="files")
nav.add_item("cloud",  text="Cloud", icon="cloud", group="files")
nav.add_separator()
nav.add_footer_item("settings", text="Settings", icon="gear")
```

In `expanded` mode, groups expand and collapse inline; in `compact` mode
they show a popup menu of their items.

!!! link "SideNav reference"
    See [SideNav](../widgets/navigation/sidenav.md) for events, toolbar
    integration, and full method reference.

---

## Tabs

For peer-level navigation with a visible bar, ttkbootstrap provides three
widgets at different levels:

| Widget      | What it is                                                                                          |
|-------------|-----------------------------------------------------------------------------------------------------|
| `TabView`   | Composite of a `Tabs` bar and a `PageStack`. Selecting a tab swaps the page. The default choice.    |
| `Tabs`      | Just the tab bar — no content area. Useful when you want a `PageStack` (or anything else) elsewhere.|
| `Notebook`  | Thin wrapper over native `ttk.Notebook`. Kept for compatibility; prefer `TabView` for new code.     |

### TabView (bar + pages, single widget)

```python
import ttkbootstrap as ttk

app = ttk.App()

tabs = ttk.TabView(app, accent="primary")
tabs.pack(fill="both", expand=True, padx=10, pady=10)

# add(key, text=..., icon=..., page=...) returns the page widget
home = tabs.add("home", text="Home", icon="house")
ttk.Label(home, text="Welcome to the application").pack(anchor="w")

settings = tabs.add("settings", text="Settings", icon="gear")
ttk.Label(settings, text="Configure your preferences here").pack(anchor="w")

about = tabs.add("about", text="About", icon="info-circle")
ttk.Label(about, text="Version 1.0").pack(anchor="w")

# Programmatic switching
tabs.select("settings")
print(tabs.current)              # 'settings'

# Listen for page changes
tabs.on_page_changed(lambda e: print("now on:", e.data["page"]))

app.mainloop()
```

`TabView` supports horizontal or vertical orientation (`orient=`),
closable tabs (`enable_closing=True | "hover"`), and a "+" add button
(`enable_adding=True`, fires `<<TabAdd>>`). See the
[TabView reference](../widgets/views/tabview.md).

### Tabs (bar only)

When you want a tab bar that drives something other than a `PageStack`
(e.g., switching `TableView` filters, toggling chart series), use `Tabs`:

```python
import ttkbootstrap as ttk

app = ttk.App()

bar = ttk.Tabs(app)
bar.pack(fill="x", padx=10, pady=10)

bar.add(text="All",     key="all")
bar.add(text="Active",  key="active")
bar.add(text="Archived", key="archived")

bar.on_tab_changed(lambda value: print(f"filter: {value}"))

app.mainloop()
```

### Notebook (legacy)

`Notebook` wraps the native `ttk.Notebook`. New code should prefer
`TabView`, which has a more modern look, closable / addable tabs, and
better integration with the design system. `Notebook` remains supported
for migrations and code that depends on the native widget. See the
[Notebook reference](../widgets/views/notebook.md).

### When to use tabs

- Users need to **switch freely** between views (no inherent order).
- Views are **peers** (no parent/child or sequence relationship).
- You have **2 to 7** top-level sections.

If you have many sections, prefer a sidebar (`SideNav` / `AppShell`). If
navigation is sequential or hierarchical, prefer `PageStack`.

---

## Stack-based navigation with PageStack

Use `PageStack` when navigation is **sequential or flow-based**. It shows
one page at a time and maintains a history stack — like a browser, complete
with back and forward.

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PageStack(app)
stack.pack(fill="both", expand=True, padx=10, pady=10)

welcome = stack.add("welcome", padding=20)
details = stack.add("details", padding=20)
confirm = stack.add("confirm", padding=20)

ttk.Label(welcome, text="Welcome! Let's get started.").pack(anchor="w", pady=(0, 10))
ttk.Button(welcome, text="Continue",
           command=lambda: stack.navigate("details")).pack()

ttk.Label(details, text="Enter your details").pack(anchor="w", pady=(0, 10))
ttk.Button(details, text="Back",     command=stack.back).pack(side="left", padx=(0, 5))
ttk.Button(details, text="Continue", command=lambda: stack.navigate("confirm")).pack(side="left")

ttk.Label(confirm, text="All done!").pack(anchor="w", pady=(0, 10))
ttk.Button(confirm, text="Back", command=stack.back).pack()

stack.navigate("welcome")
app.mainloop()
```

### Navigation methods

| Method                                | Description                                                         |
|---------------------------------------|---------------------------------------------------------------------|
| `add(key, page=None, **frame_kwargs)` | Register a page. If `page` is None, a Frame is created and returned.|
| `navigate(key, data=None)`            | Push a new entry onto the history.                                  |
| `navigate(key, replace=True)`         | Replace the current history entry (no back arrow appears).          |
| `back()` / `forward()`                | Move through history.                                               |
| `can_back()` / `can_forward()`        | Whether each direction is currently possible.                       |
| `current()`                           | `(key, data)` of the visible page, or `None`.                       |
| `remove(key)`                         | Remove and destroy a page.                                          |

### Passing data between pages

`navigate()` accepts a `data=` dict that travels with the history entry and
appears on the page lifecycle events. The page reads it from `event.data`:

```python
def on_mount(event):
    data = event.data
    print(data["page"])         # 'detail'
    user_id = data.get("user_id")
    # populate the detail view from user_id...

detail.bind("<<PageMount>>", on_mount, add="+")

# elsewhere:
stack.navigate("detail", data={"user_id": 42})
```

### Lifecycle events

Each page receives, in order:

- `<<PageWillMount>>` — fired before the page is shown.
- `<<PageMount>>`     — fired after the page is packed in.
- `<<PageUnmount>>`   — fired when the page is hidden (it remains in
  memory; widgets are not destroyed).

The `PageStack` itself fires `<<PageChange>>` after navigation completes.
All event payloads expose:

| Field                         | Meaning                                       |
|-------------------------------|-----------------------------------------------|
| `page`                        | Key of the new page.                          |
| `prev_page`, `prev_data`      | Key and data of the page being left.          |
| `nav`                         | `'push'`, `'back'`, or `'forward'`.           |
| `index`, `length`             | Position in history and total history length. |
| `can_back`, `can_forward`     | Same as the methods, snapshotted.             |

```python
stack.on_page_changed(lambda e: print(f"{e.data['prev_page']} -> {e.data['page']} ({e.data['nav']})"))
```

Because pages are kept alive across navigation, widget state (form values,
scroll position, etc.) is preserved automatically. Use `<<PageMount>>` to
refresh data when a page becomes visible again.

### When to use PageStack

- **Multi-step wizards** or onboarding flows.
- **Drill-down** navigation: list view → detail view → edit view.
- Anywhere a **back button** improves usability.

---

## Combining patterns

Patterns nest. A common shape is `AppShell` for top-level sections with
`TabView` inside one of the pages:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="Combined Navigation", size=(1000, 650))

home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Dashboard", font="heading-xl").pack(anchor="w", padx=20, pady=20)

settings = shell.add_page("settings", text="Settings", icon="gear")

tabs = ttk.TabView(settings)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

general = tabs.add("general",  text="General")
ttk.Label(general, text="General settings").pack(anchor="w", padx=10, pady=10)

advanced = tabs.add("advanced", text="Advanced")
ttk.Label(advanced, text="Advanced options").pack(anchor="w", padx=10, pady=10)

shell.mainloop()
```

A `PageStack` inside a tab is just as valid — useful when one tab needs a
list → detail drill-down without leaving its tab context.

---

## Custom sidebar

When `SideNav` doesn't fit (unusual layouts, custom item rendering), a
plain `Frame` of `Button`s driving a `PageStack` works well. This is
significantly more code than `SideNav`, so reach for it only when needed:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Custom Sidebar", size=(800, 500))

sidebar = ttk.Frame(app, padding=10, width=200)
sidebar.pack(side="left", fill="y")

stack = ttk.PageStack(app)
stack.pack(side="left", fill="both", expand=True)

for key in ["dashboard", "users", "settings"]:
    page = stack.add(key, padding=20)
    ttk.Label(page, text=key.title(), font="heading-xl").pack(anchor="w")

nav_buttons = {}
for label, key in [("Dashboard", "dashboard"), ("Users", "users"), ("Settings", "settings")]:
    btn = ttk.Button(
        sidebar, text=label, width=20,
        accent="secondary", variant="outline",
        command=lambda k=key: stack.navigate(k),
    )
    btn.pack(fill="x", pady=2)
    nav_buttons[key] = btn

def on_page_changed(event):
    current = event.data.get("page")
    for key, btn in nav_buttons.items():
        if key == current:
            btn.configure(accent="primary", variant=None)
        else:
            btn.configure(accent="secondary", variant="outline")

stack.on_page_changed(on_page_changed)
stack.navigate("dashboard")

app.mainloop()
```

---

## Programmatic navigation and deep linking

All three patterns expose a `navigate(key, data=...)` method, so opening
a specific view from a CLI argument, a URL handler, or a notification
click is uniform:

```python
# AppShell — keeps the sidebar selection in sync
shell.navigate("users", data={"filter": "active"})

# TabView — switches to the named tab
tabs.navigate("settings")

# PageStack directly
stack.navigate("user-detail", data={"user_id": 42})
```

For history-based navigation (back/forward), use `PageStack` (directly or
through `AppShell.pages`). `Tabs` and `TabView` don't maintain history of
their own; if you want back/forward over tab switches, navigate the
underlying `PageStack` instead of setting the tab.

---

## State preservation

Navigation in ttkbootstrap is non-destructive by default:

- **`PageStack` pages** are packed and unpacked, never destroyed (unless
  you call `remove()`). Widget state, scroll position, and entry contents
  are preserved across navigation.
- **`TabView` pages** sit in an internal `PageStack` and behave the same
  way.
- **`Notebook` tabs** likewise keep their child widgets alive.
- **`AppShell` pages** are managed by its internal `PageStack`, so the
  same guarantee applies.

For state you need to **save explicitly** (e.g., persist a draft form
before the user closes the app), bind to `<<PageUnmount>>` on the page
or `<<PageChange>>` on the stack and write to your data layer there.

---

## Best practices

**Keep navigation consistent.** Place navigation in the same location
across all views. Use consistent labels and icons. Don't mix tabs and
sidebar at the same level of hierarchy in the same window.

**Show the current location.** `SideNav` and `TabView` highlight the
selected item automatically. For custom navigation, listen to
`<<PageChange>>` and update your nav UI to match (the custom-sidebar
example above shows the pattern).

**Match the pattern to the user's mental model.** Tabs imply "peers,
pick one." A sidebar implies "many sections, broad scope." A stack
implies "I'm in a flow, I can go back." Picking the wrong shape is
often more confusing than any styling choice.

**Prefer `add_page` / `add` over manual wiring.** The composite widgets
(`AppShell`, `TabView`) keep nav and content in sync for you. Drop down
to `SideNav` + `PageStack` only when you need the extra control.

---

## Additional resources

- [AppShell](../widgets/application/appshell.md) — toolbar + sidebar + pages in one window.
- [SideNav](../widgets/navigation/sidenav.md) — standalone sidebar navigation.
- [Toolbar](../widgets/navigation/toolbar.md) — horizontal toolbar.
- [TabView](../widgets/views/tabview.md) — tabs + content area.
- [Tabs](../widgets/navigation/tabs.md) — standalone tab bar.
- [Notebook](../widgets/views/notebook.md) — legacy `ttk.Notebook` wrapper.
- [PageStack](../widgets/views/pagestack.md) — stack-based navigation with history.
- [App structure](app-structure.md) — organizing your application code.
