# ttkbootstrap 2.0 — Theme migration guide

> **For the docs rewrite (Workstream H):** this is the authoritative,
> user-facing source for the theming migration content. It lives in
> `development/` on purpose so it is **not lost** when `docs/` is restructured
> for 2.0 — fold it into the new "Theming" / "Migrating to 2.0" pages rather than
> rewriting it from memory. Keep it updated as Workstream D (bootstyle) lands.

2.0 replaces the flat 16-key theme dictionaries with a **semantic-anchor theme
model**. You declare a theme's accent colors once; the full palette — and a
matching **light and dark** variant — is generated. This guide covers what
changed and how to migrate.

## TL;DR

| 1.x | 2.0 |
|---|---|
| ~18 single-mode themes (`cosmo`, `darkly`, …) | 15 curated **families** → 30 `-light`/`-dark` themes |
| Default `litera` | Default **`bootstrap-light`** |
| `Window(themename="darkly")` just works | Still works — a legacy name auto-registers on use (one-time `DeprecationWarning`) |
| Author a 16-key `colors` dict | Author a `Theme(...)` (accent anchors + light/dark blocks) |
| `style.colors.primary` (a string) | Still a string — **plus** `style.colors.primary[300]` ramp steps |

## Theme names changed

The built-in catalog is now 15 curated families, each generating two variants:

```
bootstrap  pydata  nord  solarized  catppuccin  gruvbox  dracula
tokyo-night  one  everforest  vapor  minty  pulse  united  sandstone
```

→ `bootstrap-light`, `bootstrap-dark`, `pydata-light`, … (30 total).

```python
import ttkbootstrap as ttk
app = ttk.Window(themename="bootstrap-dark")   # was e.g. "darkly"
```

### The old theme names still work

The pre-2.0 names (`cosmo`, `flatly`, `litera`, `darkly`, `superhero`, `solar`,
`cyborg`, `united`, `journal`, …) keep working with **no code change** — using
one auto-registers that theme on demand and emits a one-time
`DeprecationWarning`:

```python
import ttkbootstrap as ttk
app = ttk.Window(themename="darkly")   # works; warns once that "darkly" is legacy
```

Legacy themes keep their authored accent and background/foreground colors; only
their inconsistent plumbing (borders, input backgrounds) is regenerated, so they
look the same but cleaner.

If you need the **whole** pre-2.0 catalog registered up front — e.g. to
enumerate it via `Style.theme_names()` or to offer every legacy name in a theme
picker — call `install_legacy_themes()` once after creating the app:

```python
ttk.install_legacy_themes()          # bulk-registers all pre-2.0 names
```

Either way, these names are a migration convenience and are planned for removal
in 3.0.

## Authoring your own theme

### The `Theme` API (recommended)

Declare the accent anchors plus a `light` and/or `dark` background block:

```python
import ttkbootstrap as ttk

ttk.Theme(
    name="acme",
    primary="#2780e3", success="#3fb618", info="#9954bb",
    warning="#ff7518", danger="#ff0039",
    secondary=None,               # optional colored accent; else from the neutral ramp
    neutral="#7e8081",            # gray base (borders, secondary, muted)
    light=dict(background="#ffffff", foreground="#373a3c"),
    dark=dict(background="#222222",  foreground="#f8f9fa"),
).register()                      # registers acme-light + acme-dark

app = ttk.Window(themename="acme-light")
```

- Declare **one or both** of `light`/`dark`; each defined block yields a variant.
- `Theme.from_existing(base, name="acme", primary="#ff5722")` rebrands a family
  by overriding just the tokens you want.
- Call `.register()` after a `Window`/`Style` exists (or persist the spec — below).

### ttkcreator

`python -m ttkcreator` is now a `Theme` editor: pick a base family, tune the
accent anchors + neutral and the light/dark background/foreground, preview both
modes live, then **Export theme definition** to get a ready-to-use
`Theme(...).register()` Python file, or **Save** to persist it.

### Persisting a custom theme (`USER_THEME_SPECS`)

Saved themes are stored in `ttkbootstrap/themes/user.py` as anchor specs and
loaded at startup:

```python
from ttkbootstrap.themes.user import USER_THEME_SPECS

USER_THEME_SPECS["acme"] = {
    "primary": "#2780e3", "success": "#3fb618", "info": "#9954bb",
    "warning": "#ff7518", "danger": "#ff0039",
    "secondary": None, "neutral": "#7e8081",
    "light": {"background": "#ffffff", "foreground": "#373a3c"},
    "dark":  {"background": "#222222",  "foreground": "#f8f9fa"},
}
# -> themename "acme-light" / "acme-dark"
```

### Legacy 16-key dicts still work

Existing `USER_THEMES` entries and `load_user_themes(json)` files in the old
16-key shape are still loaded (adapted like the built-in legacy themes:
authored accents/bg/fg kept, plumbing regenerated). No change required, but
prefer `USER_THEME_SPECS` / the `Theme` API going forward.

## Colors: same attributes, plus ramp addressing

`style.colors` is unchanged for existing code — every attribute (`primary`,
`bg`, `fg`, `selectbg`, `border`, `inputbg`, …) is still a hex string. New in
2.0, each color also addresses its own 50–950 tint/shade ramp:

```python
c = style.colors
c.primary            # '#0a58ca'  (still a str)
c.primary[300]       # a lighter tint of primary
c.primary[700]       # a darker shade
c.ramp("primary")    # the full {50: ..., ..., 950: ...} mapping
```

## Behavior changes to be aware of

- **Selection color (`selectbg`) is now a neutral gray**, not tied to a specific
  authored value. If you relied on a particular selection color, set it via your
  own `Theme`/spec or override the style.
- **Input backgrounds in dark themes** are derived from the theme background
  (hue-preserving), so a themed dark field keeps its tint instead of washing to
  gray.
- **Built-in palettes shifted** — 2.0 regenerates each theme's derived colors
  from its anchors for consistent contrast (per-mode accent stepping, readable
  on-colors). Pin exact 1.x colors with your own `Theme`/spec if you need them.

## For library integrators

- `ThemeDefinition` and `Style.register_theme(definition)` are unchanged; a
  16-key `Colors` still constructs. The `Theme` model builds `ThemeDefinition`s
  under the hood, so both paths coexist.
- `DEFAULT_THEME` is now `"bootstrap-light"`.
