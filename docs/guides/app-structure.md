---
title: App Structure
---

# App Structure

A ttkbootstrap application is built around a single root window that owns the
event loop, the active theme, the current locale, and the application
settings. Everything else — widgets, signals, secondary windows — hangs off
that root.

This guide walks through how to assemble a real application: which entry
point to choose, how to lay out the UI, how to manage shared state, how to
move between views, and how to wire window lifecycle and app-wide options
together. By the end you should be able to read or write the top of any
ttkbootstrap `main.py` and understand what each piece is doing.

---

## Choosing an entry point

Every ttkbootstrap app starts with one of two classes:

| | `App` | `AppShell` |
|---|---|---|
| What it gives you | A blank window | Toolbar + sidebar + page stack, prewired |
| Best for | Custom layouts, single-view tools, dialog-driven utilities | Multi-page navigation apps |
| Layout | You build everything | Built; you add pages |

Both create the main window, install the theme, set up the application
context, and own the event loop. You create exactly one of them per process.

```python
import ttkbootstrap as ttk

# Option A: blank window — you build the layout
app = ttk.App(title="My Application", size=(800, 600))

# Option B: window with built-in navigation
shell = ttk.AppShell(title="My Application", size=(1000, 650))
```

`AppShell` is a subclass of `App`, so anything you can do on an `App`
(themes, settings, lifecycle, scheduling, signals) you can also do on an
`AppShell`. Pick `AppShell` when your app has clearly separated views
behind a sidebar; pick `App` when it doesn't.

If you opt into `AppShell` but don't want the sidebar — for example, an app
with only a toolbar — pass `show_nav=False` and add pages through
`shell.pages.add()` directly. `AppShell` does not require a navigation
structure to function.

!!! tip "Scaffolding"
    Use `ttkb start MyApp` to scaffold a project around `App`, or
    `ttkb start MyApp --template appshell` for the navigation layout.

---

## A minimal application

The smallest complete program demonstrates the three steps every
ttkbootstrap app performs:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Hello", size=(400, 300))

ttk.Label(app, text="Hello, ttkbootstrap!").pack(padx=20, pady=20)
ttk.Button(app, text="Close", command=app.destroy).pack(pady=10)

app.mainloop()
```

1. **Create** the App. This initializes Tk, applies the theme, and
   registers the App as the process's "current app" so `Signal` and other
   framework helpers can find it.
2. **Build** the UI. Add widgets to the App or to containers under it.
3. **Run** the event loop. `mainloop()` shows the window, centers it on
   screen the first time, and processes events until the window is
   destroyed.

`app.destroy()` ends the loop and tears down the window. `app.close()` is
an alternative that calls `quit()` (stops the loop without destroying
widgets) — useful when you need to run code after the loop returns.

---

## Application options

`App.__init__` accepts a small set of window options inline; everything
else is configured through `AppSettings` (covered below).

```python
import ttkbootstrap as ttk

app = ttk.App(
    title="My App",
    theme="darkly",
    size=(900, 600),
    minsize=(640, 480),
    resizable=(True, True),
    alpha=1.0,
)

app.mainloop()
```

The options most apps use:

- `title` — text shown in the title bar.
- `theme` — name of the active theme. Overrides `settings.theme`.
- `size`, `position`, `minsize`, `maxsize` — window geometry. Position
  defaults to centered on first show.
- `resizable` — `(width, height)` resize permissions.
- `icon` — a `PhotoImage` or path to use as the window icon.
- `alpha` — overall window transparency, `0.0` to `1.0`.

`AppShell` accepts the same options plus shell-specific ones
(`frameless`, `show_toolbar`, `show_nav`, `nav_display_mode`, `nav_accent`,
`toolbar_density`).

### Frameless windows

Setting `frameless=True` on `AppShell` removes the OS title bar entirely.
The toolbar gains minimize/maximize/close buttons and becomes draggable —
the result is a fully custom-chromed window:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(
    title="Custom Window",
    size=(1000, 650),
    frameless=True,
)

shell.mainloop()
```

This is the only ttkbootstrap-specific way to get a borderless window;
everything else uses the OS chrome.

---

## App-wide settings

Window options on the constructor cover geometry. Anything that affects
the *application* — theme pair, locale, persistence, platform behavior —
lives on `AppSettings`.

```python
import ttkbootstrap as ttk

app = ttk.App(
    title="My App",
    settings={
        "app_name": "MyApp",
        "app_version": "1.0.0",
        "theme": "dark",
        "locale": "de_DE",
        "remember_window_state": True,
    },
)

app.mainloop()
```

You can pass settings as a dict (shown above) or as an `AppSettings`
instance; both work. Settings are accessible at runtime via `app.settings`
and `ttk.get_app_settings()`.

A full inventory of what `AppSettings` controls — auto-detected
locale defaults, platform-specific options like `window_style` and
`macos_quit_behavior`, and how persistence works — is in the dedicated
[App Settings](app-settings.md) guide. The short version: anything that
should hold for the whole application's lifetime goes there, not into
constructor kwargs.

---

## Layout

Containers carry layout in ttkbootstrap. Widgets don't position
themselves — their parent container decides where they go. There are
three primitives:

- **`Frame`** — a plain container. You call `pack()`, `grid()`, or
  `place()` on each child explicitly.
- **`PackFrame`** — a Frame that adds default `direction` and `gap`
  spacing for its children. Children call the regular `pack()`; the
  frame applies the defaults.
- **`GridFrame`** — a Frame with declarative `rows`, `columns`, and
  `gap`. Children call `grid()` and are auto-placed into the next free
  cell unless they specify a position.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Layout primer", size=(420, 220))

# Outer column with even spacing.
main = ttk.PackFrame(app, direction="vertical", gap=10, padding=20)
main.pack(fill="both", expand=True)

ttk.Label(main, text="A vertical PackFrame with gap=10").pack()

# Inner row of buttons; the row inherits its parent's place in main,
# but defines its own horizontal layout.
buttons = ttk.PackFrame(main, direction="horizontal", gap=8)
buttons.pack()
ttk.Button(buttons, text="Save").pack()
ttk.Button(buttons, text="Cancel").pack()

app.mainloop()
```

Composing PackFrames like this — vertical outer, horizontal inner —
gives you the same shape that flexbox calls "column with row of items"
without any geometry math.

When you need a true 2D layout (forms with aligned labels, dashboards
with proportional regions), reach for `GridFrame`:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Grid layout", size=(440, 180))

form = ttk.GridFrame(
    app,
    columns=["auto", 1],   # label column shrinks to content; field column grows
    gap=(12, 8),           # (column_gap, row_gap)
    padding=20,
)
form.pack(fill="both", expand=True)

ttk.Label(form, text="Name:").grid(sticky="e")
ttk.TextEntry(form).grid(sticky="ew")

ttk.Label(form, text="Email:").grid(sticky="e")
ttk.TextEntry(form).grid(sticky="ew")

app.mainloop()
```

For deeper coverage of the layout primitives — direction tokens,
fill/expand defaults, sticky values, auto-flow — see the
[Layout guide](layout.md).

### What `AppShell` builds for you

When you choose `AppShell` you skip the outer layout entirely:

```
AppShell (window)
├── Toolbar (top)
│   └── hamburger, title, spacer, [your buttons]
└── Frame (body)
    ├── SideNav (left)
    └── PageStack (right, fills remainder)
        ├── Frame (page "home")
        ├── Frame (page "docs")
        └── ...
```

Pages are added through `add_page()`; the toolbar and sidenav are exposed
as `shell.toolbar` and `shell.nav` for further customization.

---

## State management with signals

Most non-trivial apps need to share state across widgets — a current
user, a selected item, an error message that several panels react to.
ttkbootstrap models that with **signals**.

A `Signal` wraps a typed value and notifies subscribers whenever it
changes. Multiple widgets can subscribe to the same signal without
knowing about each other.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Signals", size=(360, 200))

# Shared state
username = ttk.Signal("")

# An entry that writes to the signal
ttk.TextEntry(app, label="Name", textsignal=username).pack(padx=20, pady=10, fill="x")

# A label that reads from the signal
greeting = ttk.Label(app, text="Hello, ?")
greeting.pack(padx=20)

# Reactive update: subscriber receives the new value
username.subscribe(lambda value: greeting.configure(text=f"Hello, {value or '?'}"))

app.mainloop()
```

Three things to know about signals:

1. **The constructor takes the initial value positionally**, and the
   signal's *type* is fixed by it. `Signal("")` is a string signal,
   `Signal(0)` is an int signal, `Signal(False)` is a bool signal.
   `set()` enforces the type at runtime.
2. **`subscribe(callback)` calls back with the new value.** The
   callback signature is `def callback(value): ...` — no event object,
   just the new value. `subscribe` returns an id you can pass to
   `unsubscribe()`. Pass `immediate=True` to fire the callback once
   with the current value at subscription time.
3. **Widgets bind via dedicated kwargs** (`textsignal=`, `signal=`,
   `value=`) rather than `textvariable=`. The widget keeps the signal
   and its underlying `tk.Variable` in sync automatically.

### Why signals, not Tk variables

`tk.StringVar` / `IntVar` / etc. work, and ttkbootstrap accepts them. But
signals are preferable for application state because:

- They're **typed** — a `Signal(0)` rejects `set("oops")` at runtime;
  an `IntVar` silently coerces or errors at use time.
- They're **subscribable directly** — `signal.subscribe(callback)` vs.
  the lower-level `var.trace_add('write', ...)` dance.
- They **support derivation** — `derived = signal.map(transform)`
  produces a new signal that updates whenever the source changes.
- They **proxy** the underlying `tk.Variable`, so anywhere you used to
  pass a variable you can pass a signal.

For larger applications, group related signals in a `state.py` module
and import from there:

```python
# src/myapp/state.py
import ttkbootstrap as ttk

current_user = ttk.Signal("")
is_logged_in = ttk.Signal(False)
unread_count = ttk.Signal(0)
```

Reactivity, subscription lifecycle, and the difference between signals,
callbacks, and events are covered in depth in the
[Reactivity guide](reactivity.md).

---

## Navigation

If you chose `AppShell`, navigation is already wired: each page is
associated with a sidebar item, and selecting the item shows the page.

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="My App", size=(1000, 650))

home = shell.add_page("home", text="Home", icon="house")
ttk.Label(home, text="Welcome!").pack(padx=20, pady=20)

docs = shell.add_page("docs", text="Documents", icon="file-earmark-text")
ttk.Label(docs, text="Your documents.").pack(padx=20, pady=20)

# Footer items pin to the bottom of the sidebar.
shell.add_page("settings", text="Settings", icon="gear", is_footer=True)

# Toolbar buttons appear right of the title.
shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)

shell.mainloop()
```

`add_page(key, text=, icon=, is_footer=, group=, scrollable=, page=)`
creates the nav item and the page in one call and returns the page's
`Frame` so you can pack content into it. If you pass `page=` you can
substitute your own widget instead of a generated Frame — useful when a
page is a self-contained class.

For programmatic navigation:

```python
shell.navigate("settings")        # show the settings page
shell.on_page_changed(handler)    # subscribe to page changes
shell.current_page                # the active page key, or None
```

If you're building on `App` rather than `AppShell`, you can compose the
same pattern manually using `PageStack` for the content area and
`SideNav` (or whatever sidebar UI you want) for the picker. The
[Navigation guide](navigation.md) walks through both ends of that
spectrum, including tabs, multi-step wizards, and custom sidebars.

---

## Multiple windows

Secondary windows — settings dialogs, detail views, tool palettes — use
`Toplevel`. A `Toplevel` shares the `App`'s event loop and theme; it has
its own geometry, lifecycle, and close button.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Main", size=(500, 300))

def open_settings():
    win = ttk.Toplevel(title="Settings", size=(360, 220), transient=app)
    ttk.Label(win, text="Settings go here").pack(padx=20, pady=20)
    ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)

ttk.Button(app, text="Open settings", command=open_settings).pack(pady=20)

app.mainloop()
```

Useful options on `Toplevel`:

- `transient=app` — visually attaches the window to its parent so the
  WM treats it as auxiliary (no taskbar icon on most platforms,
  minimizes with the parent).
- `topmost=True` — keeps the window above others.
- `windowtype="utility"` (or `"splash"`, `"tooltip"`) — hints the WM
  about the window's role.

For dialog-style flows (file pickers, message boxes, modal forms), prefer
the dedicated dialog classes in the [Dialogs guide](dialogs.md) over a
hand-rolled `Toplevel`.

---

## Lifecycle and the close button

The `App` lifecycle has four stages:

1. **Construction** — `App(...)` initializes Tk, applies the theme,
   loads the message catalog, and registers the App as current.
2. **Building** — you create widgets, signals, and pages.
3. **Running** — `app.mainloop()` shows the window and pumps events
   until the window is destroyed.
4. **Cleanup** — destroy callbacks fire, traces are released, and (if
   `remember_window_state=True`) the window geometry is persisted.

To run code when the user clicks the close button — for example, prompt
to save unsaved work — register an `on_close` handler:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Confirm exit", size=(360, 180))

def confirm_quit():
    # Ask, save, etc. Then either destroy or do nothing to cancel.
    app.destroy()

app.on_close(confirm_quit)
ttk.Label(app, text="Try the close button.").pack(padx=20, pady=40)

app.mainloop()
```

`on_close()` is just a convenience wrapper around
`protocol("WM_DELETE_WINDOW", handler)`; it overrides whatever the
platform default would have been.

On macOS, the default close-button behavior is to *hide* the window
rather than destroy it — that's the OS convention, and Cmd+Q (or
Dock → Quit) is what actually quits. Set
`AppSettings.macos_quit_behavior="classic"` to use the cross-platform
"close button destroys" behavior instead.

---

## Theme switching at runtime

Themes can change while the app is running; every widget repaints
automatically:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Theme switching", theme="cosmo", size=(360, 160))

ttk.Button(app, text="Toggle theme", command=ttk.toggle_theme).pack(pady=40)

app.mainloop()
```

`ttk.toggle_theme()` flips between `settings.light_theme` and
`settings.dark_theme`. To set a specific theme by name, use
`ttk.set_theme("darkly")`. To follow the OS appearance automatically
(macOS only at present), set `follow_system_appearance=True` in
settings.

---

## Localization at the app level

Internationalized apps set the locale once on `AppSettings`; widgets
auto-translate `text=` strings against the active message catalog and
format locale-sensitive values (dates, numbers) accordingly.

```python
import ttkbootstrap as ttk

app = ttk.App(
    title="Localized",
    settings={"locale": "de_DE"},
)

# Labels translate their text=. Strings are looked up against the
# message catalog; missing keys fall back to the literal text.
ttk.Label(app, text="Cancel").pack(padx=40, pady=20)

app.mainloop()
```

The translation catalog (gettext `.mo` files), the active language, and
runtime language switching are covered in the
[Localization guide](localization.md). At the app-structure level, the
only thing to know is: set `locale` on settings, and put your translation
catalogs under `locales/` next to your code.

---

## Putting it together

A worked single-window app combining state, layout, and lifecycle:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Counter", size=(320, 240))

# State
counter = ttk.Signal(0)

# Layout
main = ttk.PackFrame(app, direction="vertical", gap=12, padding=24)
main.pack(fill="both", expand=True)

# Display reacts to the signal
display = ttk.Label(main, font="display-xl[48]", text="0")
counter.subscribe(lambda value: display.configure(text=str(value)))
display.pack()

# Controls mutate the signal
controls = ttk.PackFrame(main, direction="horizontal", gap=8)
controls.pack()
ttk.Button(controls, text="+1", command=lambda: counter.set(counter.get() + 1)).pack()
ttk.Button(controls, text="Reset", command=lambda: counter.set(0)).pack()

app.mainloop()
```

The same shape, refactored into `AppShell`:

```python
import ttkbootstrap as ttk

shell = ttk.AppShell(title="Counter", size=(900, 600))

# State
counter = ttk.Signal(0)

# A page returned by add_page() is a Frame you can build into.
home = shell.add_page("home", text="Home", icon="house")

display = ttk.Label(home, font="display-xl[48]", text="0")
counter.subscribe(lambda value: display.configure(text=str(value)))
display.pack(padx=20, pady=20)

controls = ttk.PackFrame(home, direction="horizontal", gap=8)
controls.pack(padx=20)
ttk.Button(controls, text="+1", command=lambda: counter.set(counter.get() + 1)).pack()
ttk.Button(controls, text="Reset", command=lambda: counter.set(0)).pack()

# A second page demonstrates that pages are independent containers.
about = shell.add_page("about", text="About", icon="info-circle")
ttk.Label(about, text="Counter App v1.0").pack(padx=20, pady=20)

shell.mainloop()
```

Both versions follow the same pattern: state lives in signals, layout
lives in containers, behavior lives in callbacks that mutate signals.
The only difference is whether you build the outer chrome yourself
(`App`) or accept the standard one (`AppShell`).

---

## Project structure

`ttkb start` scaffolds two layouts. The **basic** template (default)
gives you a single-view `App`:

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

The **appshell** template (`--template appshell`) gives you an
`AppShell` with sidebar navigation and one file per page:

```
myapp/
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

The chosen template is recorded in `ttkb.toml`, so `ttkb add view` and
`ttkb add page` know which scaffold to use.

As your project grows, factor app-wide concerns into their own modules:

```
myapp/
├── src/myapp/
│   ├── __init__.py
│   ├── main.py            # App / AppShell construction
│   ├── settings.py        # AppSettings defaults
│   ├── state.py           # Signals, shared state
│   ├── views/             # or pages/, depending on template
│   └── services/          # IO, data, persistence
├── assets/
├── locales/               # Translation catalogs
└── ttkb.toml
```

Detailed coverage of file organization, packaging, and PyInstaller
integration is in the [Project Structure](../platform/project-structure.md)
platform guide.

---

## Next steps

- [App Settings](app-settings.md) — full reference for `AppSettings`.
- [Layout](layout.md) — `Frame`, `PackFrame`, `GridFrame` in depth.
- [Reactivity](reactivity.md) — signals, callbacks, events, and the
  subscription lifecycle.
- [Navigation](navigation.md) — `AppShell`, `SideNav`, `PageStack`,
  tabs, and wizard patterns.
- [Localization](localization.md) — message catalogs, runtime language
  switching.
- [Project Structure](../platform/project-structure.md) — file layout,
  packaging, distribution.
