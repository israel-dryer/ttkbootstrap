---
title: App Settings
---

# App Settings

`AppSettings` is the single configuration object for a ttkbootstrap
application. It collects metadata, theme preferences, locale, platform
behavior, and window-state persistence into one place — so application code
doesn't reach for scattered globals or environment variables.

This guide walks through what's in `AppSettings`, how to pass it to `App`,
and the lifecycle questions that come up in real applications (which fields
take effect at runtime, which are evaluated only at startup, where overrides
come from).

For per-window options not covered by `AppSettings` — `size`, `position`,
`minsize`, `resizable`, etc. — see [App Structure](app-structure.md).

---

## The mental model

`AppSettings` describes *application-level* behavior. Individual widgets
should never read or modify it; they react to framework state derived from
these settings (the active theme, the active locale, the surface inheritance
rule, etc.).

Two ways to pass settings to `App`:

```python
import ttkbootstrap as ttk

# Inline dict — the quickest form, fine for examples and small apps.
app = ttk.App(settings={
    "app_name": "Invoice Manager",
    "app_version": "2.1.0",
    "locale": "en_US",
})
```

```python
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

# Dataclass — better for IDE completion, validation, and inspection.
settings = AppSettings(
    app_name="Invoice Manager",
    app_version="2.1.0",
    locale="en_US",
)
app = ttk.App(settings=settings)
```

The two forms are interchangeable. Use the dict for short examples or when
the values come from a JSON file; use the dataclass when you want
autocomplete, want to read derived defaults before constructing the app, or
want to mutate the object before passing it in.

---

## What's in AppSettings

### Application metadata

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `app_name` | `str \| None` | `None` (becomes `"ttkbootstrap"`) | Window title and OS app identity |
| `app_author` | `str \| None` | `None` | Author/vendor; informational |
| `app_version` | `str \| None` | `None` | Version string; informational |

`app_name` is also used as the macOS Apple-menu app name (Tk's `tk appname`)
and as the leaf in the persisted-window-state filename.

### Theme

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `theme` | `str` | `"light"` | Active theme name, or `"light"` / `"dark"` alias |
| `light_theme` | `str` | `"bootstrap-light"` | What `"light"` resolves to |
| `dark_theme` | `str` | `"bootstrap-dark"` | What `"dark"` resolves to |
| `follow_system_appearance` | `bool` | `False` | Track the OS light/dark preference |
| `available_themes` | `Sequence[str]` | `()` | Filter and order the theme list shown by `get_themes()` |
| `inherit_surface_color` | `bool` | `True` | Children pick up the parent surface color |

`follow_system_appearance` is currently effective on macOS, where Tk fires
`<<TkSystemAppearanceChanged>>` and exposes the current mode. On Windows and
Linux the flag is silently a no-op. See
[Theming → Following the system appearance](theming.md#following-the-system-appearance).

`available_themes` is for apps that ship a curated picker. If empty, every
registered theme appears in `get_themes()` sorted alphabetically; if non-
empty, only listed themes are returned, in that order.

### Localization

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `locale` | `str \| None` | auto-detected | Locale identifier (e.g. `"en_US"`, `"de_DE"`) |
| `language` | `str \| None` | derived from `locale` | Base language code |
| `date_format` | `str \| None` | derived from `locale` | ICU/CLDR date pattern |
| `time_format` | `str \| None` | derived from `locale` | ICU/CLDR time pattern |
| `number_decimal` | `str \| None` | derived from `locale` | Decimal separator |
| `number_thousands` | `str \| None` | derived from `locale` | Thousands separator |
| `localize_mode` | `"auto" \| bool` | `"auto"` | Translation behavior |

When you set `locale`, the format fields are derived from it via Babel's
CLDR data. You can override any of them individually:

```python
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

settings = AppSettings(
    locale="de_DE",
    # Override the local default for ISO display.
    date_format="yyyy-MM-dd",
)

app = ttk.App(settings=settings)
```

See [Localization](localization.md) for translation patterns and message
catalogs.

### Platform behavior

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `window_style` | `str \| None` | `"mica"` | Windows-only window-effect style |
| `macos_quit_behavior` | `"native" \| "classic"` | `"native"` | macOS close/quit semantics |

`window_style` is forwarded to `pywinstyles` on Windows. Valid values include
`"mica"`, `"acrylic"`, `"aero"`, `"transparent"`, and `"win7"`; `None`
disables the effect. Ignored on macOS and Linux.

`macos_quit_behavior` controls what the close button and Cmd+Q do on macOS:

- `"native"` (default) — the close button hides the window, the dock icon
  re-shows it, and Cmd+Q (or Dock → Quit) is what actually destroys the
  process. This matches macOS conventions.
- `"classic"` — close button destroys the window, matching the
  cross-platform Tk default.

The setting is a no-op on Windows and Linux.

### Window state persistence

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `remember_window_state` | `bool` | `False` | Save/restore window geometry across launches |
| `state_path` | `str \| None` | OS config dir | Override the saved-state file location |

When `remember_window_state` is on, the app writes its geometry (size and
position) on close and restores it on next launch. Off-screen positions are
clamped back into a visible monitor. The default location is per-platform —
`Library/Application Support` on macOS, `%APPDATA%` on Windows,
`$XDG_CONFIG_HOME` on Linux — and the leaf filename includes `app_name` so
multiple apps don't collide.

```python
import ttkbootstrap as ttk

app = ttk.App(
    settings={
        "app_name": "Notes",
        "remember_window_state": True,
    },
    size=(800, 600),
)
app.mainloop()
```

The first run uses the `size=` you passed; subsequent runs honor whatever
the user last left the window at.

---

## Constructor overrides

The `App` constructor accepts a few parameters that override fields in
`AppSettings`. They're for transient or environment-driven configuration —
CLI flags, test runs, prototyping — not the long-lived app definition.

| `App(...)` arg | Overrides |
|----------------|-----------|
| `title=` | `app_name` |
| `theme=` | `theme` |
| `localize=` | `localize_mode` |
| `window_style=` | `window_style` |

Anything else you want to vary should live in the settings object itself.

```python
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

settings = AppSettings(app_name="Default Name", theme="light")

app = ttk.App(
    settings=settings,
    title="Overridden",   # wins over settings.app_name
    theme="dark",          # wins over settings.theme
)
```

---

## Reading and updating settings at runtime

The active settings live on `app.settings`:

```python
import ttkbootstrap as ttk

app = ttk.App(settings={"locale": "fr_FR"})

print(app.settings.locale)        # "fr_FR"
print(app.settings.date_format)   # "dd/MM/y" (derived)
print(app.settings.theme)         # "light"
```

Or via the global accessor (useful in code that doesn't carry an `app`
reference):

```python
from ttkbootstrap.runtime.app import get_app_settings

settings = get_app_settings()
print(settings.locale)
```

`AppSettings` is a regular dataclass — fields are mutable. **Most fields are
not live**: changing them after `App.__init__` doesn't replay the startup
behavior that consumed them. The right way to change settings at runtime is
to use the dedicated APIs:

| To change... | Do this, not `app.settings.X = ...` |
|--------------|-------------------------------------|
| Theme | `ttk.set_theme(...)` or `ttk.toggle_theme()` |
| Locale | (re-init MessageCatalog; see Localization) |
| Window state, geometry | `app.geometry(...)`, `app.title(...)` |

Mutating `app.settings` directly is fine for fields that are read on demand
(e.g. for your own application logic to inspect later), but won't propagate
to framework subsystems on its own.

---

## Inspecting derived defaults

`AppSettings` runs `__post_init__` on construction to fill in locale-derived
values. You can construct one independently to see what those defaults look
like before passing it to `App`:

```python
from ttkbootstrap.runtime.app import AppSettings

settings = AppSettings(locale="ja_JP")

print(settings.language)         # "ja"
print(settings.date_format)      # ICU pattern from CLDR
print(settings.number_decimal)   # "."
print(settings.number_thousands) # ","
```

This is useful when you want to override only one derived field while
keeping the rest of the locale defaults.

---

## A complete example

```python
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

settings = AppSettings(
    # Metadata
    app_name="Task Manager",
    app_author="Productivity Inc",
    app_version="3.0.0",

    # Theme
    theme="light",
    light_theme="ocean-light",
    dark_theme="ocean-dark",
    follow_system_appearance=True,

    # Localization
    locale="en_US",

    # Window-state persistence
    remember_window_state=True,
)

app = ttk.App(
    settings=settings,
    size=(800, 600),
    minsize=(400, 300),
)

main = ttk.PackFrame(app, direction="vertical", padding=20, gap=10)
main.pack(fill="both", expand=True)

ttk.Label(main, text=f"Welcome to {app.settings.app_name}").pack()
ttk.Label(main, text=f"Version: {app.settings.app_version}").pack()
ttk.Button(main, text="Toggle theme", command=ttk.toggle_theme).pack(pady=20)

app.mainloop()
```

Reading this top-down tells you everything about the app: what it's called,
how it's themed, how it handles localization, and how it persists across
launches. That co-location is the value `AppSettings` provides over scattered
configuration.

---

## When to use a dict vs the dataclass

Use a **dict** when:

- You're loading config from JSON, TOML, or YAML.
- You're writing a short example.
- You don't care about IDE autocomplete on field names.

```python
import json
import ttkbootstrap as ttk

with open("config.json") as f:
    config = json.load(f)

app = ttk.App(settings=config)
app.mainloop()
```

Use **`AppSettings`** when:

- You want IDE completion, type checking, and refactoring help.
- You want to inspect derived defaults (`date_format`, `language`, ...)
  before constructing `App`.
- You want to compose settings programmatically before passing them in.

```python
import os
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

settings = AppSettings(locale="ja_JP")

# e.g. tweak based on environment
if os.environ.get("APP_DARK_MODE") == "1":
    settings.theme = "dark"

app = ttk.App(settings=settings)
app.mainloop()
```

---

## Related guides

- [App Structure](app-structure.md) — application organization and
  lifecycle.
- [Theming](theming.md) — `light_theme`, `dark_theme`, and
  `follow_system_appearance` in context.
- [Localization](localization.md) — `locale`, `localize_mode`, and message
  catalogs.
- [Platform → Differences](../platform/platform-differences.md) — per-OS
  behavior for `window_style` and `macos_quit_behavior`.
