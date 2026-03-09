---
title: AppShell
---

# AppShell

`AppShell` is a **composite layout widget** that scaffolds the standard desktop application layout:
toolbar at top, sidebar navigation on the left, and page content on the right.

It wires together a `Toolbar`, `NavigationView`, and `PageStack` so you don't have to.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App(title="My App", size=(1000, 650))

shell = ttk.AppShell(app, title="My App")
shell.pack(fill="both", expand=True)

home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Welcome!").pack(padx=20, pady=20)

docs = shell.add_page("docs", text="Documents", icon="file-earmark-text")
ttk.Label(docs, text="Your documents.").pack(padx=20, pady=20)

app.mainloop()
```

---

## When to use

Use `AppShell` when:

- you need the common toolbar + sidebar + content layout

- you want navigation wired to page switching automatically

- you want a quick scaffold without manual widget composition

Consider a different control when:

- you need a custom layout that doesn't match the toolbar/sidebar/content pattern

- you only need tabs or a page stack without a sidebar - use [TabView](../views/tabview.md) or [PageStack](../views/pagestack.md)

---

## Appearance

### With toolbar (default)

When `show_toolbar=True`, the toolbar spans the top with a hamburger toggle, title, and spacer for custom buttons.

```python
shell = ttk.AppShell(app, title="My App")

# Add buttons after the spacer
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)
```

### Without toolbar

When `show_toolbar=False`, the NavigationView manages its own collapse toggle.

```python
shell = ttk.AppShell(app, show_toolbar=False)
```

### Without navigation

When `show_nav=False`, only the toolbar and page content are shown. Use `shell.pages.add()` directly.

```python
shell = ttk.AppShell(app, title="My App", show_nav=False)
page = shell.pages.add("home", sticky="nsew")
```

---

## Examples and patterns

### Adding pages

`add_page()` creates both a nav item and a page in one call. The first page is auto-navigated to.

```python
home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Home content").pack()
```

### Groups, headers, separators

```python
shell.add_separator()
shell.add_header("Files")
shell.add_group("storage", text="Storage", icon="folder", is_expanded=True)
shell.add_page("local", text="Local", icon="hdd", group="storage")
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
def on_change(event):
    print(f"Now on: {event.data['page']}")

shell.on_page_changed(on_change)
```

### Accessing child widgets

```python
shell.toolbar    # Toolbar or None
shell.nav        # NavigationView or None
shell.pages      # PageStack (always present)
```

---

## Behavior

### Navigation wiring

When a nav item is selected, AppShell automatically navigates the PageStack. Nav items added via `add_page()` trigger page switches. Nav items without pages (added directly to `shell.nav`) do not.

### Auto-navigation

The first page added via `add_page()` is automatically displayed.

---

## Additional resources

### Related widgets

- [NavigationView](navigationview.md) - the sidebar navigation component

- [Toolbar](toolbar.md) - the top toolbar component

- [PageStack](../views/pagestack.md) - the page content manager

- [TabView](../views/tabview.md) - tab-based content switching

### API reference

- [`ttkbootstrap.AppShell`](../../reference/widgets/AppShell.md)
