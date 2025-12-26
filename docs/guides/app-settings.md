---
title: App Settings
---

# App Settings

This guide explains how to configure a ttkbootstrap application using `AppSettings`—the centralized configuration object for themes, localization, and application metadata.

---

## Overview

ttkbootstrap applications are configured through `AppSettings` rather than scattered flags and globals. This provides:

- **Centralized configuration** — all settings in one place
- **Type safety** — IDE autocomplete and validation
- **Sensible defaults** — auto-detected locale, standard themes
- **Flexibility** — pass a dict or a dataclass

---

## Design Intent

AppSettings defines *application-level behavior*, not widget-level styling.
Individual widgets should not read or modify settings directly; instead,
they react to framework state derived from these settings.

---

## Quick Start

### Using a Dictionary

The simplest approach—pass settings as a dict:

```python
import ttkbootstrap as ttk

app = ttk.App(
    settings={
        "app_name": "My Application",
        "app_version": "1.0.0",
        "theme": "dark",
        "locale": "en_US",
    }
)

app.mainloop()
```

### Using the AppSettings Class

For better IDE support and validation:

```python
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

settings = AppSettings(
    app_name="My Application",
    app_version="1.0.0",
    theme="dark",
    locale="en_US",
)

app = ttk.App(settings=settings)
app.mainloop()
```

Both approaches are equivalent. Use the class when you want autocomplete or need to inspect/modify settings before passing them.

---

## Configuration Options

### Application Metadata

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `app_name` | `str` | `None` | Application name (used in title bar) |
| `app_author` | `str` | `None` | Author name (used for config paths) |
| `app_version` | `str` | `None` | Version string |

```python
settings = AppSettings(
    app_name="Invoice Manager",
    app_author="Acme Corp",
    app_version="2.1.0",
)
```

### Theme Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `theme` | `str` | `"light"` | Active theme name or alias |
| `light_theme` | `str` | `"bootstrap-light"` | Theme for `"light"` alias |
| `dark_theme` | `str` | `"bootstrap-dark"` | Theme for `"dark"` alias |
| `available_themes` | `Sequence[str]` | `()` | Themes available to the user |
| `inherit_surface_color` | `bool` | `True` | Children inherit parent's background |

```python
settings = AppSettings(
    theme="dark",
    light_theme="ocean-light",
    dark_theme="ocean-dark",
)
```

!!! link "Theming Guide"
    See [Theming](theming.md) for theme customization and switching.

### Localization Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `locale` | `str` | auto-detected | Locale identifier (e.g., `"en_US"`, `"de_DE"`) |
| `language` | `str` | derived from locale | Base language code (e.g., `"en"`) |
| `date_format` | `str` | derived from locale | Date format pattern |
| `time_format` | `str` | derived from locale | Time format pattern |
| `number_decimal` | `str` | derived from locale | Decimal separator |
| `number_thousands` | `str` | derived from locale | Thousands separator |
| `localize_mode` | `bool \| "auto"` | `"auto"` | Localization behavior |

```python
settings = AppSettings(
    locale="de_DE",
    # Derived automatically:
    # language = "de"
    # date_format = "dd.MM.yy"
    # number_decimal = ","
    # number_thousands = "."
)
```

When you specify a `locale`, format settings are automatically derived from it. You can override any individual setting:

```python
settings = AppSettings(
    locale="en_US",
    date_format="yyyy-MM-dd",  # Override the US default
)
```

!!! link "Localization Guide"
    See [Localization](localization.md) for message catalogs and translations.

---

## Constructor Overrides

The `App` constructor accepts `title`, `theme`, and `localize` parameters that override settings. Constructor overrides 
are intended for transient or environment-driven configuration (such as CLI flags or testing), not long-term configuration.


```python
settings = AppSettings(
    app_name="Default Name",
    theme="light",
)

# title and theme override the settings values
app = ttk.App(
    settings=settings,
    title="Overridden Title",  # Overrides app_name
    theme="dark",              # Overrides theme
    localize=True,             # Overrides localize_mode
)
```

This is useful for:

- Quick prototyping without modifying settings
- Command-line argument overrides
- Testing with different configurations

---

## Accessing Settings at Runtime

Access the current settings through the app instance:

```python
app = ttk.App(settings={"locale": "fr_FR"})

# Read settings
print(app.settings.locale)        # "fr_FR"
print(app.settings.date_format)   # "dd/MM/y"
print(app.settings.theme)         # "light"

app.settings.app_name = "New Name"
```
!!! warning "Runtime Updates"
    Settings are mutable, but many settings (such as theme and localization)
    are evaluated during application startup and may require explicit refresh
    or rebuild logic to take effect.


Or use the global accessor:

```python
from ttkbootstrap.runtime.app import get_app_settings

settings = get_app_settings()
print(settings.locale)
```

---

## Complete Example

A fully configured application:

```python
import ttkbootstrap as ttk
from ttkbootstrap.runtime.app import AppSettings

# Define settings
settings = AppSettings(
    # App metadata
    app_name="Task Manager",
    app_author="Productivity Inc",
    app_version="3.0.0",

    # Theme configuration
    theme="light",
    light_theme="ocean-light",
    dark_theme="ocean-dark",

    # Localization
    locale="en_US",
    localize_mode="auto",
)

# Create app with settings and window options
app = ttk.App(
    settings=settings,
    size=(800, 600),
    minsize=(400, 300),
    resizable=(True, True),
)

# Build UI
main = ttk.PackFrame(app, direction="vertical", padding=20, gap=10)
main.pack(fill="both", expand=True)

ttk.Label(main, text=f"Welcome to {app.settings.app_name}").pack()
ttk.Label(main, text=f"Version: {app.settings.app_version}").pack()
ttk.Label(main, text=f"Locale: {app.settings.locale}").pack()

ttk.Button(main, text="Toggle Theme", command=ttk.toggle_theme).pack(pady=20)

app.mainloop()
```

---

## Dict vs Class: When to Use Each

### Use a Dict When:

- Quick prototyping or examples
- Configuration comes from JSON/YAML files
- You don't need IDE autocomplete

```python
# From a config file
import json

with open("config.json") as f:
    config = json.load(f)

app = ttk.App(settings=config)
```

### Use AppSettings When:

- You want IDE autocomplete and type checking
- You need to validate or transform settings
- You want to inspect defaults before passing

```python
settings = AppSettings(locale="ja_JP")

# Inspect derived values
print(f"Date format: {settings.date_format}")
print(f"Language: {settings.language}")

# Modify before use
if some_condition:
    settings.theme = "dark"

app = ttk.App(settings=settings)
```

---

## Default Values

When no settings are provided, `AppSettings` uses sensible defaults:

| Setting | Default Value |
|---------|---------------|
| `app_name` | `None` (falls back to `"ttkbootstrap"`) |
| `theme` | `"light"` |
| `light_theme` | `"bootstrap-light"` |
| `dark_theme` | `"bootstrap-dark"` |
| `locale` | Auto-detected from system |
| `inherit_surface_color` | `True` |
| `localize_mode` | `"auto"` |

Locale-dependent settings (`date_format`, `time_format`, `number_decimal`, `number_thousands`) are derived from the detected or specified locale.

---

## Summary

- Use `settings` parameter to pass configuration to `App`
- Pass a **dict** for simplicity or an **AppSettings** instance for type safety
- Settings cover **metadata**, **theming**, and **localization**
- Constructor parameters (`title`, `theme`, `localize`) override settings
- Access settings at runtime via `app.settings` or `get_app_settings()`

---

## Next Steps

- [App Structure](app-structure.md) — application organization and lifecycle
- [Theming](theming.md) — theme configuration and customization
- [Localization](localization.md) — internationalization and translations