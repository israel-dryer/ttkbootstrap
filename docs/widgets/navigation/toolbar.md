---
title: Toolbar
---

# Toolbar

`Toolbar` is a **horizontal toolbar container** for icon buttons, labels, separators, and custom widgets.

It optionally supports window control buttons (minimize, maximize, close) and window dragging for custom titlebars.

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

toolbar = ttk.Toolbar(app, surface="chrome")
toolbar.pack(fill="x")

toolbar.add_button(icon="list", command=lambda: print("menu"))
toolbar.add_separator()
toolbar.add_label(text="My App", font="heading-md")
toolbar.add_spacer()
toolbar.add_button(icon="gear", command=lambda: print("settings"))

app.mainloop()
```

---

## When to use

Use `Toolbar` when:

- you need a horizontal bar with icon buttons and labels

- you want a custom titlebar with window controls

- you're building a toolbar for an [AppShell](appshell.md) or standalone layout

Consider a different control when:

- you need tab-based navigation - use [Tabs](tabs.md)

- you need a menu bar - use `MenuBar`

---

## Appearance

### Density

```python
# Standard buttons
toolbar = ttk.Toolbar(app, density="default")

# Smaller buttons
toolbar = ttk.Toolbar(app, density="compact")
```

### Window controls

```python
toolbar = ttk.Toolbar(
    app,
    show_window_controls=True,
    draggable=True,
)
```

---

## Examples and patterns

### Adding items

Items are added left-to-right. Use `add_spacer()` to push subsequent items to the right.

```python
toolbar.add_button(icon="arrow-left", command=go_back)
toolbar.add_separator()
toolbar.add_label(text="Page Title", font="heading-md")
toolbar.add_spacer()
toolbar.add_button(icon="sun", command=ttk.toggle_theme)
```

### Custom widgets

```python
search = ttk.Entry(toolbar.content)
toolbar.add_widget(search)
```

### Accessing window controls

```python
toolbar.minimize_button  # Button or None
toolbar.maximize_button  # Button or None
toolbar.close_button     # Button or None
```

---

## Additional resources

### Related widgets

- [AppShell](appshell.md) - uses Toolbar as its top bar

- [NavigationView](navigationview.md) - sidebar navigation

### API reference

- [`ttkbootstrap.Toolbar`](../../reference/widgets/Toolbar.md)
