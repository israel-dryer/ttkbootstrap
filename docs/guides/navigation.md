---
title: Navigation
---

# Navigation

Navigation is how users move between different views in your application. ttkbootstrap provides
several patterns for organizing and switching between content areas.

This guide covers:

- **Tabs** — category-based switching with [Notebook](../widgets/views/notebook.md)
- **Stacked views** — flow-based navigation with [PageStack](../widgets/views/pagestack.md)
- **Sidebar navigation** — custom navigation panels controlling a PageStack

---

## Choosing a navigation pattern

| Pattern | Best for | Widget |
|---------|----------|--------|
| **Tabs** | Category switching, settings panels, dashboards | `Notebook` |
| **Stacked views** | Wizards, multi-step flows, drill-down navigation | `PageStack` |
| **Sidebar + stack** | App-wide navigation, many sections, persistent menu | `PageStack` + custom sidebar |

---

## Tabs with Notebook

Use `Notebook` when users need **random access** to related views. Tabs are visible and clickable,
making it easy to switch between categories.

```python
import ttkbootstrap as ttk

app = ttk.App()

notebook = ttk.Notebook(app, accent="primary", padding=20)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Create tabs
home = notebook.add(text="Home", key="home")
settings = notebook.add(text="Settings", key="settings")
about = notebook.add(text="About", key="about")

# Add content to each tab
ttk.Label(home, text="Welcome to the application").pack(anchor="w")
ttk.Label(settings, text="Configure your preferences here").pack(anchor="w")
ttk.Label(about, text="Version 1.0").pack(anchor="w")

app.mainloop()
```

### When to use tabs

- Users need to switch freely between views
- Views are peers (no hierarchy or sequence)
- You have 2-7 top-level sections

### When to avoid tabs

- You have many sections (7+) — consider sidebar navigation
- Navigation is sequential — use PageStack instead
- Views have parent-child relationships — use PageStack with back/forward

---

## Stacked views with PageStack

Use `PageStack` when navigation is **sequential or flow-based**. It maintains a history stack,
enabling back/forward navigation like a web browser.

```python
import ttkbootstrap as ttk

app = ttk.App()

stack = ttk.PageStack(app)
stack.pack(fill="both", expand=True, padx=10, pady=10)

# Create pages
welcome = stack.add("welcome", padding=20)
details = stack.add("details", padding=20)
confirm = stack.add("confirm", padding=20)

# Welcome page
ttk.Label(welcome, text="Welcome! Let's get started.").pack(anchor="w", pady=(0, 10))
ttk.Button(welcome, text="Continue", command=lambda: stack.navigate("details")).pack()

# Details page
ttk.Label(details, text="Enter your details").pack(anchor="w", pady=(0, 10))
ttk.Button(details, text="Back", command=stack.back).pack(side="left", padx=(0, 5))
ttk.Button(details, text="Continue", command=lambda: stack.navigate("confirm")).pack(side="left")

# Confirm page
ttk.Label(confirm, text="All done!").pack(anchor="w", pady=(0, 10))
ttk.Button(confirm, text="Back", command=stack.back).pack()

app.mainloop()
```

### When to use PageStack

- Multi-step wizards or forms
- Drill-down navigation (list → detail → edit)
- Back/forward improves usability

### Navigation methods

| Method | Description |
|--------|-------------|
| `navigate(key)` | Push a new page onto the history stack |
| `navigate(key, replace=True)` | Replace current page (no back) |
| `back()` | Go to previous page |
| `forward()` | Go to next page (after back) |
| `can_back()` | Check if back is available |
| `can_forward()` | Check if forward is available |

---

## Sidebar navigation

For applications with many sections, a **sidebar** provides persistent navigation that controls
a `PageStack`. This pattern is common in desktop applications and admin dashboards.

### Basic sidebar with PageStack

```python
import ttkbootstrap as ttk

app = ttk.App(title="Sidebar Navigation")
app.geometry("800x500")

# Main layout: sidebar + content area
main = ttk.PanedWindow(app, orient="horizontal")
main.pack(fill="both", expand=True)

# Sidebar
sidebar = ttk.Frame(main, padding=10, width=200)
main.add(sidebar, weight=0)

# Content area with PageStack
content = ttk.Frame(main)
main.add(content, weight=1)

stack = ttk.PageStack(content)
stack.pack(fill="both", expand=True)

# Create pages
dashboard = stack.add("dashboard", padding=20)
users = stack.add("users", padding=20)
settings = stack.add("settings", padding=20)
reports = stack.add("reports", padding=20)

ttk.Label(dashboard, text="Dashboard", font="heading-xl").pack(anchor="w")
ttk.Label(dashboard, text="Overview of your application").pack(anchor="w", pady=(10, 0))

ttk.Label(users, text="Users", font="heading-xl").pack(anchor="w")
ttk.Label(users, text="Manage user accounts").pack(anchor="w", pady=(10, 0))

ttk.Label(settings, text="Settings", font="heading-xl").pack(anchor="w")
ttk.Label(settings, text="Application configuration").pack(anchor="w", pady=(10, 0))

ttk.Label(reports, text="Reports", font="heading-xl").pack(anchor="w")
ttk.Label(reports, text="View and export reports").pack(anchor="w", pady=(10, 0))

# Sidebar navigation buttons
nav_items = [
    ("Dashboard", "dashboard"),
    ("Users", "users"),
    ("Settings", "settings"),
    ("Reports", "reports"),
]

for label, page_key in nav_items:
    btn = ttk.Button(
        sidebar,
        text=label,
        width=20,
        command=lambda k=page_key: stack.navigate(k),
    )
    btn.pack(fill="x", pady=2)

app.mainloop()
```

### Highlighting the active item

Track which navigation item is active and style it differently:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Sidebar with Active State")
app.geometry("800x500")

# Layout
main = ttk.PanedWindow(app, orient="horizontal")
main.pack(fill="both", expand=True)

sidebar = ttk.Frame(main, padding=10, width=200)
main.add(sidebar, weight=0)

content = ttk.Frame(main)
main.add(content, weight=1)

stack = ttk.PageStack(content)
stack.pack(fill="both", expand=True)

# Pages
for key in ["dashboard", "users", "settings"]:
    page = stack.add(key, padding=20)
    ttk.Label(page, text=key.title(), font="heading-xl").pack(anchor="w")

# Navigation with active tracking
nav_buttons = {}

def navigate_to(page_key):
    stack.navigate(page_key)
    update_active_state(page_key)

def update_active_state(active_key):
    for key, btn in nav_buttons.items():
        if key == active_key:
            btn.configure(accent="primary")
        else:
            btn.configure(accent="secondary", variant="outline")

nav_items = [
    ("Dashboard", "dashboard"),
    ("Users", "users"),
    ("Settings", "settings"),
]

for label, page_key in nav_items:
    btn = ttk.Button(
        sidebar,
        text=label,
        width=20,
        accent="secondary", variant="outline",
        command=lambda k=page_key: navigate_to(k),
    )
    btn.pack(fill="x", pady=2)
    nav_buttons[page_key] = btn

# Set initial active state
update_active_state("dashboard")

app.mainloop()
```

### Using events to sync sidebar state

Instead of manually updating state, listen to PageStack events:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Event-driven Sidebar")
app.geometry("800x500")

main = ttk.PanedWindow(app, orient="horizontal")
main.pack(fill="both", expand=True)

sidebar = ttk.Frame(main, padding=10, width=200)
main.add(sidebar, weight=0)

content = ttk.Frame(main)
main.add(content, weight=1)

stack = ttk.PageStack(content)
stack.pack(fill="both", expand=True)

# Pages
for key in ["dashboard", "users", "settings"]:
    page = stack.add(key, padding=20)
    ttk.Label(page, text=key.title(), font="heading-xl").pack(anchor="w")

# Navigation buttons
nav_buttons = {}

nav_items = [
    ("Dashboard", "dashboard"),
    ("Users", "users"),
    ("Settings", "settings"),
]

for label, page_key in nav_items:
    btn = ttk.Button(
        sidebar,
        text=label,
        width=20,
        accent="secondary", variant="outline",
        command=lambda k=page_key: stack.navigate(k),
    )
    btn.pack(fill="x", pady=2)
    nav_buttons[page_key] = btn

# Sync sidebar state on page change
def on_page_changed(event):
    current = event.data.get("page")
    for key, btn in nav_buttons.items():
        if key == current:
            btn.configure(accent="primary")
        else:
            btn.configure(accent="secondary", variant="outline")

stack.on_page_changed(on_page_changed)

# Trigger initial state
stack.navigate("dashboard")

app.mainloop()
```

---

## Combining patterns

You can combine navigation patterns. For example, a sidebar for top-level sections,
with tabs inside one of the sections:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Combined Navigation")
app.geometry("900x600")

main = ttk.PanedWindow(app, orient="horizontal")
main.pack(fill="both", expand=True)

# Sidebar
sidebar = ttk.Frame(main, padding=10, width=180)
main.add(sidebar, weight=0)

# Content
content = ttk.Frame(main)
main.add(content, weight=1)

stack = ttk.PageStack(content)
stack.pack(fill="both", expand=True)

# Dashboard page (simple)
dashboard = stack.add("dashboard", padding=20)
ttk.Label(dashboard, text="Dashboard", font="heading-xl").pack(anchor="w")

# Settings page (with tabs)
settings = stack.add("settings", padding=10)
ttk.Label(settings, text="Settings", font="heading-xl").pack(anchor="w", pady=(0, 10))

settings_tabs = ttk.Notebook(settings, padding=10)
settings_tabs.pack(fill="both", expand=True)

general = settings_tabs.add(text="General", key="general")
ttk.Label(general, text="General settings go here").pack(anchor="w")

advanced = settings_tabs.add(text="Advanced", key="advanced")
ttk.Label(advanced, text="Advanced options").pack(anchor="w")

# Sidebar buttons
nav_buttons = {}

for label, key in [("Dashboard", "dashboard"), ("Settings", "settings")]:
    btn = ttk.Button(
        sidebar,
        text=label,
        width=18,
        accent="secondary", variant="outline",
        command=lambda k=key: stack.navigate(k),
    )
    btn.pack(fill="x", pady=2)
    nav_buttons[key] = btn

def on_page_changed(event):
    current = event.data.get("page")
    for key, btn in nav_buttons.items():
        btn.configure(accent="primary" if key == current else "secondary", variant=None if key == current else "outline")

stack.on_page_changed(on_page_changed)
stack.navigate("dashboard")

app.mainloop()
```

---

## Best practices

### Keep navigation consistent

- Place navigation in the same location across all views
- Use consistent labels and icons
- Don't mix tabs and sidebar for the same level of navigation

### Provide context

- Show the current location (active tab, highlighted sidebar item)
- Use breadcrumbs for deep hierarchies
- Enable back navigation when appropriate

### Handle deep linking

If your app needs to open a specific view programmatically:

```python
# Navigate directly to a nested view
stack.navigate("users")
# Or with data
stack.navigate("user-detail", data={"user_id": 42})
```

### Preserve state

When switching views, consider whether state should be preserved:

- **Notebook tabs** preserve state by default (widgets stay alive)
- **PageStack pages** also preserve state (pages aren't destroyed)
- For forms, save state explicitly before navigating away

---

## Additional resources

- [Notebook](../widgets/views/notebook.md) — tabbed view container
- [PageStack](../widgets/views/pagestack.md) — stacked views with history
- [PanedWindow](../widgets/layout/panedwindow.md) — resizable split layouts
- [App Structure](app-structure.md) — organizing your application code
