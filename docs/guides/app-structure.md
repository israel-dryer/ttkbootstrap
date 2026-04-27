---
title: App Structure
---

# App Structure

This guide explains how a ttkbootstrap application is organized—the `App` class, windows, layout, state, and lifecycle.

Use `ttkb start MyApp` to scaffold a new project with the recommended structure.

---

## The App Class

Every ttkbootstrap application starts with either `App` or `AppShell`:

- **`App`** — a blank window. You build the layout from scratch.
- **`AppShell`** — an `App` with a toolbar, sidebar navigation, and page stack already wired together.

```python
import ttkbootstrap as ttk

# Option A: blank window
app = ttk.App(title="My Application", theme="darkly")

# Option B: window with built-in navigation
app = ttk.AppShell(title="My Application", theme="darkly", size=(1000, 650))
```

Both create the main window, initialize theming, set up the application context, and manage the event loop. You typically create one per process. Additional windows use `Toplevel`.

---

## Minimal Application

A complete, runnable application:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Hello", size=(400, 300))

ttk.Label(app, text="Hello, ttkbootstrap!").pack(padx=20, pady=20)
ttk.Button(app, text="Close", command=app.destroy).pack(pady=10)

app.mainloop()
```

This demonstrates the core pattern:

1. Create the App
2. Add widgets to it
3. Run the event loop

---

## AppShell: Navigation Built In

Most desktop applications follow the same layout: toolbar at the top, sidebar on the left, page content on the right. `AppShell` gives you that in one call:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", theme="cosmo-light", size=(1000, 650))

# Each add_page() creates a nav item and returns a Frame for content
home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Welcome!").pack(padx=20, pady=20)

# Add as many pages as you need
docs = shell.add_page("docs", text="Documents", icon="file-earmark-text")
ttk.Label(docs, text="Your documents.").pack(padx=20, pady=20)

# Add toolbar buttons (they appear on the right side)
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)

shell.mainloop()
```

`AppShell` extends `App`, so everything that works on `App` works on `AppShell` too.

### Frameless window

Set `frameless=True` to remove OS window chrome and get a fully custom window. The toolbar automatically gains minimize/maximize/close buttons and becomes draggable:

```python
shell = ttk.AppShell(
    title="Custom Window",
    size=(1000, 650),
    frameless=True,
)
```

### When to use App vs AppShell

| | `App` | `AppShell` |
|---|---|---|
| Layout | You build everything | Toolbar + sidebar + pages included |
| Best for | Custom layouts, simple tools, dialogs | Navigation-based apps |
| Navigation | Manual (wire your own) | Automatic (add_page wires nav to pages) |

---

## Application Options

Common `App` parameters:

```python
app = ttk.App(
    title="My App",           # Window title
    theme="superhero",        # Theme name
    size=(800, 600),          # Initial size (width, height)
    resizable=(True, True),   # Allow resize (width, height)
    alpha=1.0,                # Window transparency
)
```

!!! link "Themes"
    See [Design System → Custom Themes](../design-system/custom-themes.md) for available themes and customization.

---

## Project Structure

`ttkb start` generates one of two layouts depending on the template you
choose. The **basic** template (default) produces a single-view `App`:

```
myapp/                       # ttkb start MyApp
├── src/myapp/
│   ├── __init__.py
│   ├── main.py              # App entry point
│   └── views/
│       ├── __init__.py
│       └── main_view.py
├── assets/                  # Images, icons
├── ttkb.toml                # Project configuration
└── README.md
```

The **appshell** template produces an `AppShell` with sidebar navigation
and one file per page:

```
myapp/                       # ttkb start MyApp --template appshell
├── src/myapp/
│   ├── __init__.py
│   ├── main.py
│   └── pages/
│       ├── __init__.py
│       ├── home_page.py
│       └── settings_page.py
├── assets/
├── ttkb.toml
└── README.md
```

The chosen template is recorded in `ttkb.toml` as `[app].template`, so
`ttkb add view` and `ttkb add page` know which scaffold is appropriate for
the project.

As your project grows:

```
myapp/
├── src/myapp/
│   ├── __init__.py
│   ├── main.py
│   ├── settings.py      # AppSettings / defaults
│   ├── state.py         # Signals and shared state
│   ├── views/
│   │   ├── main_view.py
│   │   └── settings_view.py
│   └── services/        # IO, data, persistence
├── assets/
├── locales/             # Translation files
└── ttkb.toml
```

Use `ttkb start MyApp` to scaffold a new project with this structure.

!!! link "Project Structure"
    See [Platform → Project Structure](../platform/project-structure.md) for detailed guidance on file organization, packaging, and PyInstaller.

---

## Layout Hierarchy

ttkbootstrap applications follow a **container hierarchy**:

```
App (blank window)
└── PackFrame (main layout)
    ├── Frame (toolbar area)
    │   └── Button, Button, ...
    ├── PackFrame (content area)
    │   └── widgets...
    └── Frame (status bar)
        └── Label
```

With `AppShell`, the top-level structure is built for you:

```
AppShell (window)
├── Toolbar
│   └── hamburger, title, spacer, [your buttons]
└── Frame (body)
    ├── SideNav
    │   └── SideNavItem, SideNavGroup, ...
    └── PageStack
        ├── Frame (page "home")
        ├── Frame (page "docs")
        └── ...
```

Key principles:

- **Containers own layout** — each container manages its children
- **Widgets don't position themselves** — their parent decides placement
- **Nesting creates structure** — compose complex layouts from simple containers

!!! link "Layout Guide"
    See [Layout](layout.md) for details on Frame, PackFrame, and GridFrame.

---

## Application Settings

ttkbootstrap applications are configured through a centralized settings object
that defines application-wide behavior, rather than scattered flags and globals.

Configuration typically includes:

- theme and appearance
- localization settings
- default behaviors
- framework-level options

This configuration is applied at application startup and remains accessible
throughout the app lifecycle.

!!! link "See [App Settings](app-settings.md) for how settings are declared and applied using `AppSettings`."

---

## State Management

ttkbootstrap encourages **signals** for state that multiple widgets share:

```python
import ttkbootstrap as ttk

app = ttk.App()

# Shared state
username = ttk.Signal("")

# Input updates the signal
entry = ttk.TextEntry(app, signal=username)
entry.pack(padx=20, pady=10)

# Label reacts to the signal
label = ttk.Label(app, textvariable=username)
label.pack(padx=20, pady=10)

app.mainloop()
```

When the entry changes, the label updates automatically. Neither widget knows about the other—they both connect to the signal.

For larger applications, group related signals in a `state.py` module:

```python
# src/myapp/state.py
import ttkbootstrap as ttk

current_user = ttk.Signal("")
is_logged_in = ttk.Signal(False)
selected_item = ttk.Signal(None)
```

!!! link "Reactivity Guide"
    See [Reactivity](reactivity.md) for signals, callbacks, and events.

---

## Window Lifecycle

The `App` lifecycle:

1. **Creation** — `App()` creates the window and initializes theming
2. **Building** — you add widgets and configure layout
3. **Running** — `mainloop()` processes events until the window closes
4. **Cleanup** — the window is destroyed

For additional windows:

```python
def open_settings():
    settings = ttk.Toplevel(app, title="Settings")

    ttk.Label(settings, text="Settings go here").pack(padx=20, pady=20)
    ttk.Button(settings, text="Close", command=settings.destroy).pack(pady=10)

ttk.Button(app, text="Settings", command=open_settings).pack(pady=10)
```

`Toplevel` creates a secondary window that:

- shares the event loop with `App`
- can be modal or non-modal
- is destroyed independently

---

## Theme Switching

Themes can be changed at runtime:

```python
import ttkbootstrap as ttk
from ttkbootstrap import toggle_theme

app = ttk.App(theme="litera")

def switch_theme():
    toggle_theme()  # Toggles between light and dark variants

ttk.Button(app, text="Toggle Theme", command=switch_theme).pack(pady=20)

app.mainloop()
```

All widgets update automatically when the theme changes.

---

## Localization Setup

For internationalized applications:

```python
import ttkbootstrap as ttk

app = ttk.App(
    title="My App",
    locale="es",  # Spanish locale
)

# Widgets use message keys
ttk.Label(app, text="greeting.hello").pack()  # Resolved from catalog
```

!!! link "Localization Guide"
    See [Localization](localization.md) for message catalogs and runtime language switching.

---

## Putting It Together

A structured application example:

```python
import ttkbootstrap as ttk

# State
counter = ttk.Signal(0)

def increment():
    counter.set(counter.get() + 1)

# App
app = ttk.App(title="Counter", size=(300, 200))

# Layout
main = ttk.PackFrame(app, direction="vertical", gap=10, padding=20)
main.pack(fill="both", expand=True)

# Display
display = ttk.Label(main, font="display-xl[48]")
counter.subscribe(lambda v: display.configure(text=str(v)))
display.pack()

# Controls
controls = ttk.PackFrame(main, direction="horizontal", gap=10)
controls.pack()

ttk.Button(controls, text="+1", command=increment).pack()
ttk.Button(controls, text="Reset", command=lambda: counter.set(0)).pack()

app.mainloop()
```

This demonstrates:

- Signal-based state
- PackFrame for layout
- Reactive label updates
- Clean separation of concerns

For navigation-based applications, `AppShell` replaces the manual layout wiring:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(900, 600))

# State
counter = ttk.Signal(0)

# Pages
home = shell.add_page("home", text="Home", icon="house")
display = ttk.Label(home, font="display-xl[48]")
counter.subscribe(lambda v: display.configure(text=str(v)))
display.pack(padx=20, pady=20)

controls = ttk.PackFrame(home, direction="horizontal", gap=10)
controls.pack()
ttk.Button(controls, text="+1", command=lambda: counter.set(counter.get() + 1)).pack()
ttk.Button(controls, text="Reset", command=lambda: counter.set(0)).pack()

about = shell.add_page("about", text="About", icon="info-circle")
ttk.Label(about, text="Counter App v1.0").pack(padx=20, pady=20)

shell.mainloop()
```

---

## Next Steps

- [Layout](layout.md) — building layouts with containers
- [Navigation](navigation.md) — tabs, stacks, and sidebar patterns
- [Reactivity](reactivity.md) — signals, callbacks, and events
- [Project Structure](../platform/project-structure.md) — file organization and packaging
- [CLI](../platform/cli.md) — scaffolding and build tools
