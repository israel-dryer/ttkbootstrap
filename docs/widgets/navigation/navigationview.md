---
title: NavigationView
---

# NavigationView

`NavigationView` is a **sidebar navigation container** with a scrollable item list, collapsible groups,
section headers, and a footer area.

It supports three display modes: expanded (full width with text), compact (icons only), and minimal (hidden until toggled).

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App(title="Nav Demo", size=(900, 600))

nav = ttk.NavigationView(app, title="My App")
nav.pack(side="left", fill="y")

nav.add_item("home", text="Home", icon="house")
nav.add_item("docs", text="Documents", icon="file-earmark-text")
nav.add_item("settings", text="Settings", icon="gear")

nav.select("home")

def on_select(event):
    print(f"Selected: {event.data['key']}")

nav.on_selection_changed(on_select)

app.mainloop()
```

---

## When to use

Use `NavigationView` when:

- you need a sidebar navigation with icons and text

- you want collapsible groups for organizing items

- you need compact (icon-only) mode for space-constrained layouts

Consider a different control when:

- you need a complete app scaffold with toolbar and pages - use [AppShell](appshell.md)

- you need a simple vertical list - use [SideNav](sidenav.md)

- you need horizontal navigation - use [Tabs](tabs.md)

---

## Appearance

### Display modes

| Mode | Description |
|------|-------------|
| `expanded` | Full width with icon and text (default) |
| `compact` | Narrow, icon-only; groups show popup menus |
| `minimal` | Hidden until toggled open |

```python
nav = ttk.NavigationView(app, display_mode="compact")
```

### Accent color

```python
nav = ttk.NavigationView(app, accent="success")
```

---

## Examples and patterns

### Items

```python
nav.add_item("home", text="Home", icon="house")
```

### Groups

Groups expand/collapse in expanded mode and show a popup menu in compact mode.

```python
nav.add_group("files", text="Files", icon="folder")
nav.add_item("local", text="Local", icon="hdd", group="files")
nav.add_item("cloud", text="Cloud", icon="cloud", group="files")
```

### Headers and separators

```python
nav.add_separator()
nav.add_header("Favorites")
```

### Footer items

Fixed at the bottom of the pane.

```python
nav.add_footer_item("settings", text="Settings", icon="gear")
```

### Selection

```python
nav.select("home")
print(nav.selected_key)
```

### Toggling the pane

```python
nav.toggle_pane()
nav.set_display_mode("compact")
```

### Events

- `<<SelectionChanged>>` - `event.data = {'key': str}`
- `<<PaneToggled>>` - `event.data = {'is_open': bool}`
- `<<DisplayModeChanged>>` - `event.data = {'mode': str}`
- `<<BackRequested>>` - fired when back button is clicked

```python
nav.on_selection_changed(lambda e: print(e.data["key"]))
```

### External toolbar integration

Hide the internal header and control the nav from an external toolbar:

```python
nav = ttk.NavigationView(app, show_header=False, collapsible=False)

toolbar = ttk.Toolbar(app, surface="chrome")
toolbar.add_button(icon="list", command=nav.toggle_pane)
```

---

## Behavior

### Selection management

NavigationView uses a shared `Variable` for radio-group selection across all items. Selection updates are O(1) — only the previously-selected and newly-selected items are updated.

### UX guidance

- Use icons on all items for visual consistency

- Limit root-level items to 7-10 for scannability

- Use groups for secondary navigation items

- Use footer items for settings and account links

---

## Additional resources

### Related widgets

- [AppShell](appshell.md) - complete app layout with NavigationView built in

- [SideNav](sidenav.md) - simpler vertical navigation

- [Tabs](tabs.md) - horizontal tab navigation

- [PageStack](../views/pagestack.md) - page content management

### API reference

- [`ttkbootstrap.NavigationView`](../../reference/widgets/NavigationView.md)
