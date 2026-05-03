# Icons & Images

ttkbootstrap exposes three concrete pieces of API for visual assets:

- **`BootstrapIcon`** — vector glyph from the bundled Bootstrap Icons
  set, rendered to a `PhotoImage` at any size and color. Used directly,
  or referenced by name from a widget's `icon=` kwarg.
- **`IconSpec`** dict — the shape every icon-bearing widget accepts
  (`{name, size, color, state}`). Lets the style engine swap the icon
  per widget state (disabled, hover, pressed, selected) without
  per-widget code.
- **`Image`** — class-method utility for loading and caching arbitrary
  images (file, bytes, PIL object, transparent spacer) into Tk
  `PhotoImage` objects.

Use `BootstrapIcon` and `IconSpec` for symbolic glyphs; use `Image` for
photographic content, decorative assets, and anything that isn't a
Bootstrap icon.

---

## At a glance

| Piece | Where it lives | What it gives you |
|---|---|---|
| `BootstrapIcon(name, size, color)` | `ttkbootstrap.BootstrapIcon` | A `PhotoImage`-bearing icon object (`.image`) |
| `icon='name'` (widget kwarg) | Button, Label, CheckButton, RadioButton, MenuButton | Single-state icon, color follows the widget's foreground per state |
| `icon={...}` (`IconSpec` dict) | Same five primitives + composites that forward it | Per-state icon overrides through the style engine |
| `Image.open(path)` etc. | `ttkbootstrap.Image` (from `ttkbootstrap.api.utils`) | Cached `PhotoImage` from a file, bytes, PIL image, or transparent spacer |

The five `IconMixin` primitives — `Button`, `Label`, `CheckButton`,
`RadioButton`, `MenuButton` — are the foundational icon-bearing widgets.
Composites that present an icon (`Toolbar`, `Toast`, `SideNav`,
`Tabs`, `Accordion`, `Expander`, `Calendar`, `DropdownButton`,
`MenuBar`, `SelectBox`, `DateEntry`, `TimeEntry`, `PasswordEntry`,
`NumericEntry`, `AppShell`) forward an `icon=` argument to one of those
primitives or to their own internal renderer.

---

## `BootstrapIcon`

`BootstrapIcon` is the Bootstrap Icons font wrapped as a Tk image. The
constructor takes a name, a size, and a color, and returns an object
whose `.image` attribute is a `PhotoImage` you can pass to any widget's
`image=` kwarg.

```python
import ttkbootstrap as ttk

app = ttk.App()
star = ttk.BootstrapIcon('star', size=24, color='#ff6600')
ttk.Label(app, image=star.image, text='Favorite', compound='left').pack(padx=20, pady=20)
app.mainloop()
```

Constructor surface (from `ttkbootstrap_icons_bs.BootstrapIcon`):

| Argument | Type | Default | Notes |
|---|---|---|---|
| `name` | `str` | required | Icon name (e.g., `'star'`, `'gear'`, `'folder'`); use `style='fill'` or appended suffix to pick the filled variant |
| `size` | `int` | `24` | Pixel size of the rendered glyph |
| `color` | `str` | `'black'` | Hex (`'#ff0000'`) or PIL named color (`'red'`, `'navy'`). **Theme tokens like `'primary'` are not resolved here** — see Direct construction below |
| `style` | `'fill' \| 'outline' \| None` | `None` | Picks between filled and outlined variants; falls back to outline default |

The icon object also exposes `.image` (the cached `PhotoImage`),
`.name`, `.size`, `.color`, and `.cleanup()` for explicit teardown.

Theme tokens (`'primary'`, `'background[+1]'`, etc.) are resolved
through the style engine before reaching PIL, so
`Button(icon={'name': 'star', 'color': 'primary'})` works. When
calling `BootstrapIcon(...)` directly, pass a resolved hex value or a
PIL named color — the direct constructor does not resolve tokens.

---

## `IconSpec` — the widget `icon=` shape

The five `IconMixin` primitives accept either a string or a dict:

```python
import ttkbootstrap as ttk

app = ttk.App()

# String form — color follows the widget's foreground per state
ttk.Button(app, text='Save', icon='floppy').pack(padx=10, pady=10)

# Dict form — explicit size, hex color
ttk.Button(app, text='Open', icon={
    'name': 'folder',
    'size': 16,
    'color': '#3366ff',
}).pack(padx=10, pady=10)

# Per-state override — disabled state gets a muted icon
ttk.Button(app, text='Submit', icon={
    'name': 'check-circle',
    'size': 16,
    'state': [
        ('disabled', {'color': '#bbbbbb'}),
        ('pressed !disabled', {'name': 'check-circle-fill'}),
    ],
}).pack(padx=10, pady=10)

app.mainloop()
```

`IconSpec` keys (`style/bootstyle_builder_base.py:68`):

| Key | Type | Notes |
|---|---|---|
| `name` | `str` | Required; the Bootstrap icon name |
| `size` | `int \| None` | Pixel size; defaults to widget-class default (e.g., 18 for Button) and is DPI-scaled |
| `color` | `str \| None` | Hex string, PIL color name, or theme-derived hex. **Omit it** to inherit the widget's foreground per state (the recommended path) |
| `state` | `list[(state_expr, str \| dict)]` | Per-state overrides; expressions follow ttk's state syntax (e.g., `'disabled'`, `'hover !disabled'`, `'pressed !disabled'`, `'selected'`) |

The state-override value is either a bare icon name (string) or an
`IconStateMap` dict with `name` and/or `color`. State expressions follow
ttk's syntax: space-separated tokens, prefix `!` for negation. Unknown
states are silently ignored.

When `color` is omitted, the icon inherits the widget's foreground
state map — so a Button icon that has no `color` paints in the active
foreground and dims under `disabled` automatically. That's the path
most callers want; explicit `color` overrides every state unless a
per-state override sets its own.

The `icon=` option round-trips through `cget` (you get back the
normalized `IconSpec` dict, or the string you passed in if you used the
string form) and survives `<<ThemeChanged>>` — the style engine
re-resolves the icon's foreground at the new theme.

A second mixin-provided option, `icon_only=True`, suppresses the text
and shows just the icon (useful for compact toolbars). Both `icon` and
`icon_only` are reconfigurable at runtime via `widget.configure(...)`.

---

## `Image` — general image utility

`Image` is the class-method utility for loading and caching arbitrary
images (anything that isn't a Bootstrap icon — logos, photos,
illustrations, custom raster icons). All methods return a
`PIL.ImageTk.PhotoImage` and cache the result so repeated calls reuse
the same image:

```python
import ttkbootstrap as ttk
from ttkbootstrap import Image

app = ttk.App()

logo = Image.open('logo.png')                  # cached by absolute path
spacer = Image.transparent(16, 16)             # cached by (w, h)
icon_blob = Image.from_bytes(open('x.png', 'rb').read())  # cached by md5 hash

ttk.Label(app, image=logo).pack()
app.mainloop()
```

| Method | Cache key | Notes |
|---|---|---|
| `Image.open(path)` | `('file', resolved_path)` | Pillow-backed; supports any format Pillow reads. Path is `~`-expanded and resolved. |
| `Image.from_pil(pil_image)` | `('pil', id(image))` | Wraps an existing PIL image; cache reuses same instance only |
| `Image.from_bytes(data)` | `('bytes', md5(data))` | For embedded resources, downloads, or any raw image data |
| `Image.transparent(w, h)` | `('transparent', w, h)` | Fully transparent RGBA spacer, useful for compound padding |

All methods accept a custom `key=` argument to control cache identity
explicitly (useful for versioning, e.g., `key=('icon', 'v2')`).

Inspect or clear the cache:

- `Image.cache_info()` returns an `ImageCacheInfo` with `items=N`.
- `Image.clear_cache()` empties it (widgets still referencing freed
  entries may render incorrectly).
- `Image.get_cached(key)` / `Image.set_cached(key, img)` for direct
  cache access.

The cache solves Tk's reference-keeping problem: a Python `PhotoImage`
that is garbage-collected has its underlying Tcl image freed, and any
widget displaying it goes blank with no exception. Routing every load
through `Image.*` keeps a strong reference for as long as the cache
lives. See [Platform → Images & DPI](../../platform/images-and-dpi.md)
for the wider explanation of this pinning gotcha.

---

## Where to read next

| Question | Page |
|---|---|
| What icon names ship with the framework, and how do I pick one? | [Icons](icons.md) |
| How do widgets resolve icons through the style engine, and what happens on theme change? | [Icons](icons.md) |
| How does `Image` cache, and when should I provide my own cache key? | [Images](images.md) |
| Why does my image disappear after I return from a function? | [Platform → Images & DPI](../../platform/images-and-dpi.md) — the pinning idiom |
| How do I use icons as a developer (string form, dict form, common patterns)? | [Guides → Icons](../../guides/icons.md) |
| What icons are part of the design vocabulary? | [Design System → Icons](../../design-system/icons.md) |
