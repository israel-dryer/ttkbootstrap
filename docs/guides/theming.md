---
title: Theming
---

# Theming

This guide is the practical reference for theming a ttkbootstrap application:
selecting a theme at startup, switching at runtime, exposing a theme picker,
following system appearance, and registering custom themes that ship with your
app.

For the underlying theme model (properties, shades, semantic tokens, the
built-in family list) see
[Design System → Custom Themes](../design-system/custom-themes.md). This guide
assumes that vocabulary and focuses on what application code does with it.

---

## The single fact to remember

A theme defines what semantic tokens like `primary` and `surface` resolve to.
Your widgets ask for the token; the theme decides the color.

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")

# "primary" means whatever ocean-light says it means.
# Switching themes changes the resolved color, not this code.
ttk.Button(app, text="Submit", accent="primary")
```

That separation is the entire point. Your application code stays theme-neutral;
themes plug in underneath.

---

## Selecting a theme

### At startup

Pass `theme=` to `App` (or set it on `AppSettings`). The value is either a
specific theme name (`"ocean-light"`, `"forest-dark"`) or one of the aliases
`"light"` / `"dark"`:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")
app.mainloop()
```

### Light and dark aliases

`"light"` and `"dark"` resolve through `AppSettings.light_theme` and
`AppSettings.dark_theme`. They default to `"bootstrap-light"` and `"bootstrap-dark"`.
Configure them when you create the app to make the aliases — and
`toggle_theme()` — point at your preferred family:

```python
import ttkbootstrap as ttk

app = ttk.App(
    theme="light",
    settings={
        "light_theme": "ocean-light",
        "dark_theme": "ocean-dark",
    },
)
```

After this call:

- `theme="light"` resolved to `ocean-light` at startup
- `set_theme("dark")` would switch to `ocean-dark`
- `toggle_theme()` cycles between the two

### Switching at runtime

The runtime API is three small functions on `ttkbootstrap`:

```python
import ttkbootstrap as ttk

ttk.set_theme("forest-light")    # switch to a specific theme
ttk.toggle_theme()                # flip light <-> dark via the aliases
current = ttk.get_theme()         # name of the active theme
```

`set_theme()` is the underlying primitive. `toggle_theme()` is sugar over it
that reads `light_theme` / `dark_theme` from `AppSettings`.

A typical theme-toggle button:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")

ttk.Button(
    app,
    text="Toggle theme",
    command=ttk.toggle_theme,
).pack(padx=20, pady=20)

app.mainloop()
```

---

## Exposing a theme picker

`get_themes()` returns every registered theme as a list of dicts with `name`
and `display_name`. Use it to populate menus, comboboxes, or settings panels:

```python
import ttkbootstrap as ttk

app = ttk.App()

themes = ttk.get_themes()
for theme in themes:
    print(f"{theme['name']}: {theme['display_name']}")
```

A minimal picker wired up with a `SelectBox`:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")

theme_names = [t["name"] for t in ttk.get_themes()]

picker = ttk.SelectBox(app, value=ttk.get_theme(), items=theme_names)
picker.bind("<<Change>>", lambda e: ttk.set_theme(picker.value))
picker.pack(padx=20, pady=20)

app.mainloop()
```

Both the v2 and legacy theme packages are loaded automatically; the same list
covers all of them.

---

## Following the system appearance

On macOS, ttkbootstrap can track the OS light/dark preference automatically.
Set `follow_system_appearance=True` and provide the two themes to switch
between:

```python
import ttkbootstrap as ttk

app = ttk.App(
    settings={
        "follow_system_appearance": True,
        "light_theme": "ocean-light",
        "dark_theme": "ocean-dark",
    },
)
```

With this set, the initial theme is chosen to match the OS, and the app rebinds
to `<<TkSystemAppearanceChanged>>` so it updates live when the user toggles
appearance in System Settings.

The flag is currently effective on macOS only. On Windows and Linux it is
silently a no-op — the app keeps whatever theme was specified at startup. On
those platforms, ship your own UI control (a toggle button or settings option)
and call `toggle_theme()` directly.

---

## Reacting to theme changes

`set_theme()` and `toggle_theme()` rebuild every registered TTK style and
restyle every legacy Tk widget tracked by the runtime. Most application code
does nothing — widgets re-render automatically.

If your code holds derived state that depends on the theme (a custom canvas,
a manually-drawn chart, a colour picked out of the palette), listen for
`<<ThemeChanged>>` on the root window. Tk fires this event whenever the
underlying ttk theme changes:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")

def on_theme_changed(_event):
    current = ttk.get_theme()
    # rebuild any cached colours, redraw custom widgets, etc.
    print(f"Theme is now {current}")

app.bind("<<ThemeChanged>>", on_theme_changed, add="+")

ttk.Button(app, text="Toggle", command=ttk.toggle_theme).pack(padx=20, pady=20)
app.mainloop()
```

Use `add="+"` so you don't displace bindings the framework itself installs.

---

## Reading colors from the active theme

Every named token resolves to a hex string through `get_theme_color()`:

```python
import ttkbootstrap as ttk

app = ttk.App(theme="ocean-light")

primary = ttk.get_theme_color("primary")    # e.g. "#0d6efd"
surface = ttk.get_theme_color("background")  # current theme background
```

You can ask for any registered token: semantic roles (`primary`, `success`),
neutral roles (`foreground`, `background`), surface tokens (`card`, `chrome`,
`overlay`, `input`), or a specific shade step (`blue[500]`, `gray[700]`).

Color tokens are intended for occasional, deliberate use — for example, picking
a stroke colour for a custom canvas or feeding a chart library. Day-to-day
widget styling should stay on `accent=` and `variant=` so themes can do their
job. See [Styling](styling.md) for the full token vocabulary and modifier
syntax.

For lower-level access (full palette dictionary, theme metadata), call
`get_theme_provider()`:

```python
provider = ttk.get_theme_provider()

provider.name           # "ocean-light"
provider.mode           # "light" or "dark"
provider.colors["primary"]   # same as get_theme_color("primary")
provider.colors["blue[300]"]
```

---

## Registering custom themes

A theme is a JSON file. The full property list and shape are documented in
[Design System → Custom Themes](../design-system/custom-themes.md). To make
your app see a custom theme, register it before constructing `App`:

```python
from ttkbootstrap.style.theme_provider import register_user_theme

register_user_theme("acme-light", "themes/acme-light.json")
register_user_theme("acme-dark", "themes/acme-dark.json")

import ttkbootstrap as ttk
app = ttk.App(theme="acme-light")
```

The registry is process-global, so a single registration call covers every
window the app opens. Register both modes if you ship dark mode — many users
expect it, and `toggle_theme()` needs both ends of the pair.

To make a custom family the default for the `"light"` / `"dark"` aliases, also
set `light_theme` and `dark_theme` on `AppSettings`:

```python
register_user_theme("acme-light", "themes/acme-light.json")
register_user_theme("acme-dark", "themes/acme-dark.json")

app = ttk.App(
    theme="light",
    settings={
        "light_theme": "acme-light",
        "dark_theme": "acme-dark",
    },
)
```

---

## Common patterns

### Persisting the user's choice

ttkbootstrap doesn't persist the active theme automatically. Save it on close
and re-apply on startup using whichever storage mechanism your app uses — a
JSON file in the OS config directory, a settings database, etc. Sketch:

```python
import json
from pathlib import Path

import ttkbootstrap as ttk

CONFIG = Path.home() / ".myapp.json"

def load_pref(key, default):
    if CONFIG.exists():
        return json.loads(CONFIG.read_text()).get(key, default)
    return default

def save_pref(key, value):
    data = json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
    data[key] = value
    CONFIG.write_text(json.dumps(data))

app = ttk.App(theme=load_pref("theme", "ocean-light"))

def on_close():
    save_pref("theme", ttk.get_theme())
    app.destroy()

app.on_close(on_close)
app.mainloop()
```

---

## Related guides

- [Design System → Custom Themes](../design-system/custom-themes.md) — theme
  vocabulary, properties, shade spectrum, and the built-in family list.
- [Styling](styling.md) — using `accent`, `variant`, and color tokens on
  individual widgets.
- [App Settings](app-settings.md) — `light_theme`, `dark_theme`, and
  `follow_system_appearance` in context.
