---
title: Custom Themes
---

# Custom Themes

A theme is a JSON file that maps the design-system tokens to concrete
values: a foreground / background pair, a palette of base color shades,
and a `semantic` map that points each brand token at a specific shade
step. Everything else — the 9-step shade spectrum, the surface tokens,
the on-surface foregrounds, the stroke colors — is **derived
automatically** from those inputs.

You can ship a custom theme alongside your application by writing the
JSON file, registering it before the App is constructed, and switching
to it at runtime.

## Theme schema

A theme file is a single JSON object with these top-level fields:

| Field | Required | What it is |
|---|---|---|
| `name` | yes | Unique identifier used in `theme_use()`. Convention: kebab-case ending in `-light` / `-dark` (e.g. `"ocean-dark"`). |
| `display_name` | yes | Human-readable label used in pickers (e.g. `"Ocean Dark"`). |
| `mode` | yes | `"light"` or `"dark"`. Drives surface-derivation math. |
| `foreground` | yes | Default text color (hex). |
| `background` | yes | Default page surface color (hex). Becomes the `content` surface; the rest are derived from it. |
| `white` | yes | Pure white reference (`"#ffffff"`). |
| `black` | yes | Pure black reference (`"#000000"`). |
| `shades` | yes | Map of base color names (`blue`, `red`, etc.) to hex values. Each becomes the 500-step of a 9-step spectrum. |
| `semantic` | yes | Map of brand tokens (`primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`) to shade-step references. |

A working example, paraphrased from the bundled `bootstrap-light` theme:

```json
{
  "name": "bootstrap-light",
  "display_name": "Bootstrap Light",
  "mode": "light",
  "foreground": "#212529",
  "background": "#ffffff",
  "white": "#ffffff",
  "black": "#000000",
  "shades": {
    "blue": "#0d6efd",
    "indigo": "#6610f2",
    "purple": "#6f42c1",
    "red": "#dc3545",
    "orange": "#fd7e14",
    "yellow": "#ffc107",
    "green": "#198754",
    "teal": "#20c997",
    "cyan": "#0dcaf0",
    "gray": "#adb5bd",
    "pink": "#d63384"
  },
  "semantic": {
    "primary": "blue[600]",
    "secondary": "gray[700]",
    "success": "green[600]",
    "info": "cyan[600]",
    "warning": "yellow[600]",
    "danger": "red[600]",
    "light": "gray[100]",
    "dark": "gray[900]"
  }
}
```

The standard 11 shade names are `blue`, `indigo`, `purple`, `red`,
`orange`, `yellow`, `green`, `teal`, `cyan`, `gray`, `pink`. You can
add or omit shades, but the bundled themes all carry the full set so
that semantic references like `primary: "indigo[500]"` resolve no
matter which theme is active.

## How shades expand

Each shade you define becomes the **500-step** of a 9-step spectrum
generated automatically:

| Step | Meaning | Direction |
|---|---|---|
| `[100]` | Lightest tint | `mix_with(white, 80%)` |
| `[200]`–`[400]` | Progressively darker tints | toward base color |
| `[500]` | Base color (your defined shade) | as-defined |
| `[600]`–`[800]` | Progressively darker shades | toward black |
| `[900]` | Darkest shade | very near black |

A theme that defines `"blue": "#3498db"` automatically provides
`blue[100]` through `blue[900]` — verifiable at runtime via
`Style().style_builder.color("blue[300]")`. You don't write the
intermediate values; the framework computes them.

The convention for the `semantic` map is to reference the 500-step
on light themes and the 400-step on dark themes (lighter to remain
visible on dark backgrounds), but this is just a convention — any
step from the spectrum is valid.

## What's auto-derived

A theme defines literals (`foreground`, `background`, the shade
500-steps) and the semantic-token map. The framework derives
everything else:

| Derived family | How it's computed | Used by |
|---|---|---|
| Shade spectrum (9 steps per shade) | Generated from each defined 500-step | `accent="blue[300]"`, `[NNN]` modifier |
| Surface tokens (`chrome`, `content`, `card`, `overlay`, `input`) | Derived from `background` and `mode`. Light themes pick subtle darker tints; dark themes pick subtle lighter tints. | `surface=` kwarg on containers |
| On-surface foregrounds (`on_<surface>`) | `best_foreground(surface, [foreground, white, black])` | Default text color when the widget sits on that surface |
| Muted foregrounds (`on_<surface>_secondary`) | Derived to maintain ~3:1 contrast | Secondary text |
| Stroke colors (`stroke`, `stroke_subtle`) | Derived from `background` and `mode` | Borders and dividers |

This means a custom theme only needs to specify ~17 hex values
(foreground, background, 11 shades, 4 special tokens) plus the
semantic map — and you get the full token vocabulary documented in
[Colors](colors.md).

## Registering and switching to a custom theme

Register the theme **before** creating the App, then switch to it
with `ttk.set_theme(name)`:

```python
import json
import pathlib
import tempfile
import ttkbootstrap as ttk
from ttkbootstrap.style.theme_provider import register_user_theme

theme = {
    "name": "demo-dark",
    "display_name": "Demo Dark",
    "mode": "dark",
    "foreground": "#e0e0e0",
    "background": "#1a1a1a",
    "white": "#ffffff",
    "black": "#000000",
    "shades": {
        "blue": "#3498db", "red": "#e74c3c", "green": "#2ecc71",
        "orange": "#f39c12", "yellow": "#f1c40f", "cyan": "#1abc9c",
        "teal": "#16a085", "purple": "#9b59b6", "pink": "#e91e63",
        "indigo": "#6610f2", "gray": "#95a5a6",
    },
    "semantic": {
        "primary": "blue[400]",
        "secondary": "gray[600]",
        "success": "green[400]",
        "info": "cyan[400]",
        "warning": "orange[400]",
        "danger": "red[400]",
        "light": "gray[200]",
        "dark": "gray[800]",
    },
}
path = pathlib.Path(tempfile.gettempdir()) / "demo-dark.json"
path.write_text(json.dumps(theme))

register_user_theme("demo-dark", str(path))

app = ttk.App(title="Custom theme")
ttk.set_theme("demo-dark")

ttk.Button(app, text="Save", accent="primary").pack(padx=20, pady=20)
app.mainloop()
```

`register_user_theme(name, path)` reads the JSON, validates the schema,
and registers the theme under the given name. After that, the theme
appears in `ttk.get_themes()` and is switchable via `ttk.set_theme(name)`.
Theme switching cascades automatically through every widget; no
per-widget reconfiguration is required.

## Reading from a packaged file

For an installed application, ship the JSON inside your package and
load it via `importlib.resources`:

```python
import importlib.resources as res
from ttkbootstrap.style.theme_provider import register_user_theme

with res.as_file(res.files("myapp.themes").joinpath("brand-light.json")) as p:
    register_user_theme("brand-light", str(p))
```

Then construct the App and switch to the theme as in the previous
example. Themes registered this way appear in `ttk.get_themes()`
alongside the bundled ones, so a "select theme" picker in your
application's settings dialog can list them transparently.

## Built-in themes

The framework ships paired light/dark themes you can use unchanged or
fork as a starting point for your own:

| Family | Light | Dark |
|---|---|---|
| Bootstrap | `bootstrap-light` | `bootstrap-dark` |
| Docs | `docs-light` | `docs-dark` |
| Ocean | `ocean-light` | `ocean-dark` |
| Forest | `forest-light` | `forest-dark` |
| Rose | `rose-light` | `rose-dark` |
| Amber | `amber-light` | `amber-dark` |
| Aurora | `aurora-light` | `aurora-dark` |
| Classic | `classic-light` | `classic-dark` |

`AppSettings.light_theme` / `AppSettings.dark_theme` default to
`"bootstrap-light"` / `"bootstrap-dark"` — the abstract `theme="light"` /
`theme="dark"` aliases you pass to `App(...)` resolve to those.
Override `AppSettings` to point at a different family:

```python
import ttkbootstrap as ttk

settings = ttk.AppSettings(
    light_theme="ocean-light",
    dark_theme="ocean-dark",
)
app = ttk.App(title="Ocean theme", settings=settings)
app.mainloop()
```

## Where to read next

- The token vocabulary your theme must satisfy: [Colors](colors.md).
- The variant axis that combines with theme tokens:
  [Variants](variants.md).
- Application-level theme workflows (switching at runtime, OS-mode
  following, persisting selection): [Guides → Theming](../guides/theming.md).
- The runtime style-resolution mechanics that consume theme values:
  [Platform → Styling Internals](../platform/ttk-styles-elements.md).
