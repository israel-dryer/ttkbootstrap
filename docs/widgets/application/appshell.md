---
title: AppShell
---

# AppShell

`AppShell` is an **application window with built-in navigation** — it extends `App` and wires
together a `Toolbar`, `SideNav`, and `PageStack` into the standard desktop app layout.

---

## Quick start

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(1000, 650))

# Create a page frame and add a nav item for it
home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Welcome!").pack(padx=20, pady=20)

# Each add_page() returns a Frame you can populate with any widgets
docs = shell.add_page("docs", text="Documents", icon="file-earmark-text")
ttk.Label(docs, text="Your documents.").pack(padx=20, pady=20)

shell.mainloop()
```

---

## When to use

Use `AppShell` when:

- you need the common toolbar + sidebar + content layout

- you want navigation wired to pages automatically

- you want a quick scaffold without manual widget wiring

Consider a different control when:

- you need a plain window without navigation — use [App](app.md)

- you need a standalone sidebar in a custom layout — use [SideNav](../navigation/sidenav.md)

---

## Appearance

### Toolbar

The toolbar is shown by default. Disable it with `show_toolbar=False`.

```python
shell = ttk.AppShell(title="My App", show_toolbar=False)
```

Add buttons to the toolbar:

```python
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)
shell.toolbar.add_button(icon="gear", command=open_settings)
```

### Navigation display modes

| Mode | Description |
|------|-------------|
| `expanded` | Full width with icon and text (default) |
| `compact` | Narrow, icon-only |
| `minimal` | Hidden until toggled |

```python
shell = ttk.AppShell(title="My App", nav_display_mode="compact")
```

---

## Examples and patterns

### Adding pages

Each call to `add_page()` creates both a nav item and a page frame:

```python
page = shell.add_page("settings", text="Settings", icon="gear")
ttk.Label(page, text="Settings content").pack()
```

### Groups

```python
shell.add_group("files", text="Files", icon="folder")
shell.add_page("local", text="Local", icon="hdd", group="files")
shell.add_page("cloud", text="Cloud", icon="cloud", group="files")
```

### Footer items

```python
shell.add_page("settings", text="Settings", icon="gear", is_footer=True)
```

### Programmatic navigation

```python
shell.navigate("settings")
```

### Page change events

```python
shell.on_page_changed(lambda e: print(f"Now on: {shell.current_page}"))
```

### Frameless (custom window chrome)

Set `frameless=True` to remove the OS title bar and borders. The toolbar
automatically gains window control buttons (minimize, maximize, close) and
becomes draggable, giving you a fully custom window.

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(
    title="Custom Window",
    theme="cosmo-dark",
    size=(1000, 650),
    frameless=True,
)

# Toolbar buttons are added after the built-in window controls
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)

home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="No OS chrome — fully custom!").pack(padx=20, pady=20)

settings = shell.add_page("settings", text="Settings", icon="gear", is_footer=True)
ttk.Label(settings, text="Settings page").pack(padx=20, pady=20)

shell.mainloop()
```

---

## Components

AppShell exposes its internal widgets as properties:

| Property | Type | Description |
|----------|------|-------------|
| `toolbar` | `Toolbar` or `None` | The top toolbar |
| `nav` | `SideNav` or `None` | The sidebar navigation |
| `pages` | `PageStack` | The page content area |
| `current_page` | `str` or `None` | Key of the active page |

---

## Additional resources

### Related widgets

- [App](app.md) — plain application window

- [SideNav](../navigation/sidenav.md) — standalone sidebar navigation

- [Toolbar](../navigation/toolbar.md) — standalone toolbar

- [PageStack](../views/pagestack.md) — page container

### API reference

- [`ttkbootstrap.AppShell`](../../reference/app/AppShell.md)
