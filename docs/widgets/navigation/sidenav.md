---
title: SideNav
---

# SideNav

`SideNav` is a **simple vertical navigation list** built from Expander widgets.

For a more feature-rich sidebar with display modes, groups, and compact mode, use [NavigationView](navigationview.md).

---

## Quick start

```python
import ttkbootstrap as ttk

app = ttk.App()

nav = ttk.SideNav(app)
nav.pack(side="left", fill="y")

app.mainloop()
```

---

## When to use

Use `SideNav` when:

- you need a simple vertical navigation list with expander-style items

Consider a different control when:

- you need display modes (compact/minimal), groups, or footer items - use [NavigationView](navigationview.md)

- you need a complete app scaffold - use [AppShell](appshell.md)

---

## Additional resources

### Related widgets

- [NavigationView](navigationview.md) - feature-rich sidebar navigation

- [AppShell](appshell.md) - complete app layout

- [Tabs](tabs.md) - horizontal tab navigation

### API reference

- [`ttkbootstrap.SideNav`](../../reference/widgets/SideNav.md)
