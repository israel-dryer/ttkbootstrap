---
title: App Structure
---

# App Structure

This guide explains how a ttkbootstrap application is organized—the `App` class, windows, layout, state, and lifecycle.

Use `ttkb start MyApp` to scaffold a new project with the recommended structure.

---

## The App Class

Every ttkbootstrap application starts with an `App` instance:

```python
import ttkbootstrap as ttk

app = ttk.App(title="My Application", theme="darkly")

# ... build your UI ...

app.mainloop()
```

The `App` class:

- creates the main window
- initializes theming
- sets up the application context
- manages the event loop

You typically create one `App` per process. Additional windows use `Toplevel`.

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

A CLI-generated ttkbootstrap project:

```
myapp/
├── src/myapp/
│   ├── __init__.py
│   ├── main.py          # App entry point
│   └── views/
│       └── main_view.py
├── assets/              # Images, icons
├── ttkb.toml            # Project configuration
└── README.md
```

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
App (main window)
└── PackFrame (main layout)
    ├── Frame (toolbar area)
    │   └── Button, Button, ...
    ├── PackFrame (content area)
    │   └── widgets...
    └── Frame (status bar)
        └── Label
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
main.add(display)

# Controls
controls = ttk.PackFrame(main, direction="horizontal", gap=10)
main.add(controls)

controls.add(ttk.Button(controls, text="+1", command=increment))
controls.add(ttk.Button(controls, text="Reset", command=lambda: counter.set(0)))

app.mainloop()
```

This demonstrates:

- Signal-based state
- PackFrame for layout
- Reactive label updates
- Clean separation of concerns

---

## Next Steps

- [Layout](layout.md) — building layouts with containers
- [Navigation](navigation.md) — tabs, stacks, and sidebar patterns
- [Reactivity](reactivity.md) — signals, callbacks, and events
- [Project Structure](../platform/project-structure.md) — file organization and packaging
- [CLI](../platform/cli.md) — scaffolding and build tools
