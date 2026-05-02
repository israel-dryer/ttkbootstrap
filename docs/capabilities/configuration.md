# Configuration

ttkbootstrap configuration spans three surfaces:

1. **`AppSettings`** — application-wide runtime settings (theme, locale,
   window state, platform behaviors). Lives on `app.settings`.
2. **Widget `__init__` kwargs** — per-widget options at construction time.
   Sorted by the bootstyle wrapper into Tk options (forwarded to ttk),
   styling tokens (`accent`, `variant`, `density`, `surface`), and
   `style_options` (builder-only knobs).
3. **Runtime `configure()` / `cget()`** — post-construction reconfiguration
   of options that have a delegator. Not every option round-trips —
   construction-only options are common.

This page covers what each surface does and where the boundaries are.
For *which* tokens to use, see [Design System](../design-system/index.md);
for *how to apply them in your app*, see the [Theming guide](../guides/theming.md).

---

## AppSettings

`AppSettings` is the dataclass holding application-wide runtime settings.
It's automatically populated from the system locale and overridden by
explicit kwargs on `App` / `AppShell` / `Toplevel`. Read or assign via
`app.settings`.

```python
import ttkbootstrap as ttk

settings = ttk.AppSettings(
    app_name="My App",
    theme="dark",
    locale="de_DE",
)
app = ttk.App(settings=settings)

print(app.settings.app_name)      # 'My App'
print(app.settings.date_format)   # 'd.M.yy' (auto-derived from locale)
```

| Field | Default | Notes |
|---|---|---|
| `app_name` | `None` | Window title and per-app config-file name |
| `app_author` | `None` | Reserved for config-path namespacing |
| `app_version` | `None` | Reserved for window state and About dialogs |
| `theme` | `'light'` | Logical token; resolved via `light_theme` / `dark_theme` |
| `light_theme` | `'docs-light'` | Concrete theme used when `theme='light'` |
| `dark_theme` | `'docs-dark'` | Concrete theme used when `theme='dark'` |
| `follow_system_appearance` | `False` | macOS only; tracks `<<TkSystemAppearanceChanged>>`. No-op on Win/Linux |
| `inherit_surface_color` | `True` | Children inherit parent `_surface` (overrides explicit `surface=` on Tk-class widgets — see Pitfalls) |
| `available_themes` | `()` | Filter applied to the built-in theme list |
| `locale` | system | e.g. `'en_US'`, `'de_DE'` |
| `language` / `date_format` / `time_format` / `number_decimal` / `number_thousands` | derived from locale | Override individually if needed |
| `localize_mode` | `'auto'` | `'auto'`, `True`, or `False` |
| `window_style` | `'mica'` | Windows-only `pywinstyles` effect; `None` to disable |
| `macos_quit_behavior` | `'native'` | `'native'` (close hides; Cmd+Q quits) or `'classic'` (close destroys) |
| `remember_window_state` | `False` | If `True`, save geometry on close, restore on launch |
| `state_path` | `None` | Override the OS-default state-file location |

`AppSettings` is read-anytime; **assignment to fields after construction
does not auto-apply**. For example, `app.settings.theme = 'dark'` writes
the field but doesn't switch themes — see [Runtime reconfiguration](#runtime-reconfiguration)
below.

`AppSettings` defaults can also be supplied via a project-local
`ttkb.toml` `[app]` table when scaffolding an app with the CLI. See
[Project structure](../platform/project-structure.md).

!!! warning "`light_theme` / `dark_theme` defaults"
    The defaults are `'docs-light'` / `'docs-dark'` — the themes used to
    render this site, not the canonical app themes. For most apps,
    override them to `'bootstrap-light'` / `'bootstrap-dark'` (or your
    chosen brand themes). See the bugs list for the rationale.

---

## Constructor kwargs

Every ttkbootstrap widget routes its `__init__` kwargs through
`Bootstyle.override_ttk_widget_constructor`, which sorts them into three
buckets:

1. **Tk options** (`text`, `state`, `padding`, `width`, `command`, …) —
   forwarded to the underlying ttk class.
2. **Styling tokens** (`accent`, `variant`, `density`, `surface`,
   `bootstyle`) — captured into `_accent` / `_variant` / `_surface` /
   `_style_options` and resolved into a ttk style name like
   `bs[<hash>].<accent>.<orient>.<variant>.T<Class>`.
3. **`style_options=`** — a dict of builder-only knobs that don't have
   their own kwarg (e.g. `show_border` for Frame, `show_arrows` for
   Scrollbar). Merged into `_style_options`.

```python
import ttkbootstrap as ttk

app = ttk.App()
btn = ttk.Button(app, text="Save", accent="primary", variant="outline")

print(btn.cget("style"))   # 'bs[<hash>].primary.Outline.TButton'
print(btn._accent)         # 'primary'
print(btn._variant)        # 'outline'
print(btn._surface)        # parent's surface (default 'content')
print(btn._style_options)  # {}
```

The wrapper also:

- **Inherits the parent surface** when `inherit_surface_color=True` (the
  global default). A child widget with no explicit `surface=` picks up
  the parent's `_surface`. See the cascade pitfall below.
- **Reroutes `accent` → `surface` on container classes**. `TFrame` and
  `TLabelframe` are in `CONTAINER_CLASSES`, so
  `Frame(accent='primary')` is equivalent to `Frame(surface='primary')`
  — both tint the frame background. Use `surface=` directly for clarity.
- **Registers the widget for `<<ThemeChanged>>`** so it repaints when
  `Style.theme_use(...)` is called.

```python
f = ttk.Frame(app, accent="primary")
print(f._accent)          # 'primary'
print(f._surface)          # 'primary'  (rerouted)
print(f._style_options)    # {'surface': 'primary'}
print(f.cget("style"))     # 'bs[<hash>].primary.TFrame'
```

For the full token vocabulary, see
[Design System: variants](../design-system/variants.md) and
[Design System: colors](../design-system/colors.md). For the resolved
style-name format, see [Platform: ttk styles & elements](../platform/ttk-styles-elements.md).

### `style_options` for builder-only knobs

Some widget options live entirely in the style builder and aren't
exposed as Tk options. Pass them via `style_options=`:

```python
# Frame builder reads show_border; not a ttk option
f = ttk.Frame(app, padding=8, style_options={"show_border": True})

# Scrollbar builder reads show_arrows
sb = ttk.Scrollbar(app, orient="vertical", style_options={"show_arrows": False})
```

Most widgets that take a `style_options` knob also accept it as a
top-level kwarg for ergonomics — Frame accepts `show_border=True`
directly, for example. The two paths are equivalent; the dict form is
the escape hatch when no top-level kwarg exists.

---

## Runtime reconfiguration

Post-construction options are reconfigured via `widget.configure(**kw)`
or read via `widget.cget(key)`. Two layers cooperate:

1. **Configure delegators** — Python-side handlers for tokens that
   aren't real ttk options. Defined per-class, registered via the
   `@configure_delegate` decorator. The base class routes
   `widget.configure(accent=…, variant=…, font=…)` through delegators
   that rebuild the resolved style. Tokens without a delegator raise
   `TclError: unknown option` because Tk doesn't know about them.
2. **`configure_style_options(**kw)`** — the always-on escape hatch for
   `_style_options` keys that have no delegator. Updates
   `_style_options` and (on Frame) cascades `surface` /
   `input_background` to descendants.

```python
btn = ttk.Button(app, accent="primary", variant="outline")
btn.configure(accent="success", variant="solid")  # delegated, rebuilds style
print(btn.cget("style"))  # 'bs[<hash>].success.TButton'

# Reconfigure surface on a Frame (cascades to children)
f = ttk.Frame(app, surface="card")
f.configure_style_options(surface="chrome")
print(f._surface)              # 'chrome'
print(f._style_options)        # {'surface': 'chrome', ...}
```

### What round-trips through `cget()`

| Key | Round-trips via `cget()`? |
|---|---|
| Native ttk options (`text`, `state`, `padding`, `command`, `width`, etc.) | Yes — Tk handles them |
| `style` | Yes — returns the resolved `bs[<hash>].…` name |
| `bootstyle` | Yes (deprecated) — returns the legacy form |
| `accent` | Yes on most classes (extracted from `_accent` or parsed back from style) |
| `variant` | Mixed — works on Combobox, returns `None` on Entry / Spinbox |
| `density` | Raises `TclError: unknown option "-density"` on most classes |
| `surface` | Raises `TclError` on most classes; works on Frame / LabelFrame |

For options that don't round-trip, read the captured attribute directly
(`widget._density`, `widget._surface`, `widget._style_options.get('show_border')`)
or call `widget.configure_style_options('key_name')`.

### Construction-only options

Many ttkbootstrap options accept the value at construction but **do not
rebuild correctly when reconfigured at runtime**. Common cases:

- `orient` on Separator and Scrollbar — only writes the Tk option;
  the cached `style=` keeps the original axis.
- `density` on Entry, Combobox, Spinbox — updates only the font; the
  cached style retains the original image element + padding.
- `scroll_direction` on ScrollView — rewires scroll commands but does
  not regrid the bars.
- `expanded` on Expander when `collapsible=False` — the programmatic
  paths ignore the lock.
- `show_border` on LabelFrame — never lifted into `style_options` from
  the constructor, so the border is always on.

Treat these as construction-only unless the widget's documentation says
otherwise. The bugs list (in `analysis/docs-review-and-plan.md`) tracks
each individually with the file:line of the broken delegator.

### Switching theme at runtime

The canonical runtime theme switch is `Style.theme_use(name)`:

```python
import ttkbootstrap as ttk

app = ttk.App()
style = ttk.Style()
style.theme_use("bootstrap-dark")
```

This rebuilds every theme-managed element and fires `<<ThemeChanged>>`.

!!! warning "`app.settings.theme` is decoupled from `Style.theme_use()`"
    Assigning `app.settings.theme = 'dark'` writes the dataclass field
    but does **not** apply the theme. Conversely, `style.theme_use('dark')`
    applies the theme but doesn't update `app.settings.theme`. Read
    `style.theme_use()` to find out which theme is *actually* in
    effect; treat `app.settings.theme` as the *initial* logical
    preference, not the live source of truth.

---

## Deprecated: the `bootstyle` parameter

`bootstyle` was the v1 styling shortcut (`Button(bootstyle='primary-outline')`).
It still works at construction and via `configure(bootstyle=...)` but
emits `DeprecationWarning` and is being replaced by the explicit token
vocabulary:

| Old | New |
|---|---|
| `bootstyle="primary"` | `accent="primary"` |
| `bootstyle="primary-outline"` | `accent="primary", variant="outline"` |
| `bootstyle="success-link"` | `accent="success", variant="link"` |
| `bootstyle="info-toolbutton"` | `accent="info", variant="solid"` (Toolbutton-class widgets) |

Note: `configure(bootstyle=...)` resolves accent and variant from the
hyphenated string, so a bare accent (`bootstyle='success'`) clears any
existing `_variant`. Use `configure(accent=..., variant=...)` to update
each token independently.

---

## Pitfalls

- **`inherit_surface_color=True` overrides explicit `surface=` on
  Tk-class widgets.** A vanilla `ttk.Text(parent, surface='card')` ends
  up with `_surface='content'` (parent's surface) because the autostyle
  wrapper *replaces* the explicit token with the parent's. Pass
  `inherit_surface=False` alongside `surface='card'` to pin a surface
  explicitly. (See the bugs list for the wrapper-level fix.)
- **`density` and `surface` rarely round-trip.** Don't rely on
  `widget.cget('density')` or `widget.cget('surface')`. Read
  `widget._density` / `widget._surface` directly, or use
  `widget.configure_style_options('surface')` on classes that have
  registered the option in `_style_options`.
- **Construction-only options leak through `configure()`.** Many
  delegators only update *some* of the underlying state. Follow the
  per-widget documentation, and verify against the bugs list when in
  doubt.
- **`variant` validation is per-class.** A non-default variant raises
  `BootstyleBuilderError` if the class hasn't registered it. Use
  `Style().list_themes()` for theme names, but for variants there's no
  introspection API today — read the widget page.

---

## Related

- [Application & windows](../platform/windows.md) — full constructor surface
  for `App` / `AppShell` / `Toplevel`.
- [ttk styles & elements](../platform/ttk-styles-elements.md) — how
  styling tokens resolve to ttk style names.
- [Design System](../design-system/index.md) — the token vocabulary
  (`accent`, `variant`, `surface`, `density`, color modifiers).
- [Theming guide](../guides/theming.md) — how to apply themes in an app.
- [State & interaction](state-and-interaction.md) — runtime widget state
  versus configuration.
