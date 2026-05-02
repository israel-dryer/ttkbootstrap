# Icons

The `BootstrapIcon` constructor and the `IconSpec` dict shape are documented
on the [Icons & Images overview](index.md#bootstrapicon). This page documents
the **icon pipeline**: how a string name or `IconSpec` dict on a widget's
`icon=` kwarg becomes a per-state image map on the resolved ttk style.

The five `IconMixin` primitives — `Button`, `Label`, `CheckButton`,
`RadioButton`, `MenuButton` — wire `icon=` and `icon_only=` through
`IconMixin._delegate_icon` (`widgets/mixins/icon_mixin.py:21-27`). The
delegate writes the spec into the widget's `style_options` and triggers a
style rebuild. The style builder for that widget class then asks
`BootstyleBuilderBase.map_stateful_icons(icon, foreground_spec)`
(`style/bootstyle_builder_base.py:585-767`) to produce the
`(state_expr, image)` list that ttk consumes via `Style.element_create`.

---

## At a glance

| Stage | Where it lives | What happens |
|---|---|---|
| Spec normalization | `BootstyleBuilderBase.normalize_icon_spec` (`style/bootstyle_builder_base.py:564-583`) | String form expands to `{'name': str, 'size': default*scale}`; dict form gets a default size if omitted; explicit sizes are DPI-scaled in place. |
| Provider initialization | `_ensure_icon_provider` (`style/bootstyle_builder_base.py:48-55`) | Lazy. The first call to `_image_for` registers the framework's `_TtkBootstrapIconProvider` with `ttkbootstrap_icons.icon.Icon`. |
| State expansion | `map_stateful_icons` (`bootstyle_builder_base.py:585-767`) | Walks the widget's foreground state map plus any per-state `state` overrides on the spec, producing one `(state_expr, image)` tuple per ttk state. |
| Image rendering | `_image_for(name, size, color)` (`bootstyle_builder_base.py:667-691`) | Per-style-rebuild local cache by `(name, size, color)`. Calls `BootstrapIcon(name=…, size=…, color=…)` and returns its `.image` (a `PhotoImage`). |
| Theme repaint | `widget.rebuild_style()` after `<<ThemeChanged>>` | The widget's resolved style key is rebuilt; the foreground state map changes; `map_stateful_icons` produces new images at the new colors. |

---

## Provider resolution

The framework ships exactly one icon provider:
**`_TtkBootstrapIconProvider`**, defined at
`style/bootstyle_builder_base.py:21-45`. It is a thin subclass of
`ttkbootstrap_icons_bs.provider.BootstrapFontProvider` that overrides the
`y_bias` to `0.02` for better vertical alignment of icons against text in
ttkbootstrap buttons.

The provider is registered lazily — `_ensure_icon_provider` runs on the
first call to `_image_for` (which happens the first time a widget with an
`icon=` kwarg has its style resolved). Subsequent calls are no-ops:

```python
import ttkbootstrap as ttk
from ttkbootstrap.style import bootstyle_builder_base as b

app = ttk.App()
print(b._icon_provider_initialized)
# False — no icon-bearing widget has rendered yet

ttk.Button(app, text='X', icon='star').update()
print(b._icon_provider_initialized)
# True — provider was registered during the style build
```

There is no public registration API and no priority order — all icon names
go through this single provider. To draw a glyph from a non-Bootstrap
source, build a `PhotoImage` yourself and pass it to a widget's `image=`
kwarg directly (the ttk-native option), bypassing the icon pipeline
entirely.

The icon name must be a Bootstrap Icons name (e.g., `'star'`, `'gear'`,
`'folder'`, `'check-circle-fill'`). The provider supports both the
outline (default) and filled variants — append `-fill` to the name for
the filled glyph.

There is one short-circuit: **`name='empty'`** at
`bootstyle_builder_base.py:673-677` skips the provider entirely and
returns a fully-transparent `PhotoImage` of the requested size. Use it to
reserve layout space without rendering a glyph (e.g., to keep a column of
buttons aligned when only some carry an icon).

---

## State integration

When a widget's style is resolved, the builder for that widget class
computes a `foreground_spec` — a list of `(state_expr, color)` tuples
covering the states the widget can enter (typically some combination of
`'disabled'`, `'pressed !disabled'`, `'hover !disabled'`,
`'selected !disabled'`, and the default empty `''`). The builder then
calls `map_stateful_icons(icon, foreground_spec)`.

For each state the widget can enter, `map_stateful_icons` decides on a
`(name, color)` pair through this priority order
(`bootstyle_builder_base.py:749-763`):

1. If the spec has a `state` entry that matches the state expression,
   use its `name` and `color` overrides.
2. Otherwise, use the spec's base `name`.
3. For color: per-state override `color` wins if set; else the spec's
   base `color` if set; else the foreground color from `foreground_spec`
   for that state.

The matching algorithm at `_match_override`
(`bootstyle_builder_base.py:695-708`) accepts both exact and token forms
for state expressions:

| Override key as written | Matches state expressions |
|---|---|
| `'hover !disabled'` (exact) | Only `'hover !disabled'` |
| `'hover'` (token) | Any expression containing `hover` (e.g., `'hover !disabled'`, `'hover focus'`) |
| `'pressed'` (token) | Derives to `'pressed !disabled'` automatically |
| `'selected'` (token) | Derives to `'selected !disabled'` automatically |
| `'disabled'` | Only `'disabled'` |

So both of these produce the same map:

```python
import ttkbootstrap as ttk

app = ttk.App()

# Token form — short and idiomatic
ttk.Button(app, text='Save', icon={
    'name': 'floppy',
    'state': [('hover', {'name': 'floppy-fill'})],
}).pack(padx=20, pady=10)

# Exact form — explicit, works the same
ttk.Button(app, text='Save', icon={
    'name': 'floppy',
    'state': [('hover !disabled', {'name': 'floppy-fill'})],
}).pack(padx=20, pady=10)

app.mainloop()
```

States not covered by the foreground spec still get an entry if you
declare an override for them — `map_stateful_icons` derives the canonical
expression (e.g., `'hover'` → `'hover !disabled'`) and appends it to the
ordered states (`bootstyle_builder_base.py:737-747`). Unknown override
keys that don't match any token are dropped silently.

---

## Theme-driven coloring

The most useful path for icon color is **omit `color` entirely**. When
`base_color` is `None` and the per-state override does not set `color`,
`map_stateful_icons` falls through to `_resolve_fg(fg_val)`
(`bootstyle_builder_base.py:760`), which extracts the color from the
foreground entry the widget builder already computed for that state.

Net effect: an icon that omits `color` paints in the widget's normal
foreground when normal, dims to the disabled foreground when disabled,
brightens to the hover foreground when hovered, and so on — automatically.
This is the recommended path for theme-token integration.

```python
import ttkbootstrap as ttk

app = ttk.App()

# No 'color' — icon follows the widget's per-state foreground.
# Dims under 'disabled' without any extra wiring.
btn = ttk.Button(app, text='Submit', icon='send')
btn.pack(padx=20, pady=10)
btn.state(['disabled'])  # icon dims along with the text

app.mainloop()
```

When `<<ThemeChanged>>` fires, every wrapped widget's `rebuild_style()`
runs (registered at construction by the bootstyle wrapper). That tears
down and recomputes the resolved style key, which re-runs
`map_stateful_icons` with a fresh `foreground_spec` matching the new
theme — and the icon images are regenerated at the new colors. The cget
round-trip on `icon=` survives unchanged: pass a string and `cget('icon')`
returns a string; pass a dict and `cget('icon')` returns the normalized
dict.

!!! danger "Theme tokens crash when supplied as `IconSpec.color`"
    `Button(icon={'name': 'star', 'color': 'primary'})` raises
    `ValueError: unknown color specifier: 'primary'` from PIL. The
    `_image_for` helper at `style/bootstyle_builder_base.py:684` calls
    `BootstrapIcon(name=name, size=size, color=color)` directly without
    resolving the token — so PIL receives the literal string and
    rejects it. Hex strings (`'#ff6600'`) and PIL named colors
    (`'red'`, `'navy'`) work; theme tokens (`'primary'`,
    `'background[+1]'`) do not.

    The reliable workarounds:

    1. **Omit `color`** so the foreground map (which is already-resolved
       to hex by the widget's style builder) drives the icon. This is
       the recommended path.
    2. **Resolve the token yourself first** before constructing the
       spec:

        ```python
        import ttkbootstrap as ttk

        app = ttk.App()
        builder = ttk.Style().style_builder
        primary_hex = builder.color('primary')   # → e.g. '#4D76F6'
        ttk.Button(app, text='X', icon={'name': 'star', 'color': primary_hex}).pack(padx=20)
        ```

    The same crash applies to per-state `color` overrides
    (`'state': [('hover', {'color': 'success'})]`).

---

## DPI scaling

Icon size flows through `scale_size` (`runtime/utility.py:202-241`) at
the moment `normalize_icon_spec` is called
(`bootstyle_builder_base.py:567-583`). Both the default size (used when
the spec omits `size`) and any explicit `size` value are scaled. The
scaling factor is the framework's global UI scale (computed at App
construction from the platform baseline and the OS scaling factor).

| Source | Default size | After DPI scale on a typical macOS Retina screen |
|---|---|---|
| Button-class default (`normalize_icon_spec(default_size=18)`) | 18 | ~17–18 |
| Spec with explicit `size=24` | 24 | ~23 |

App code uses the same logical size on every display — the framework
rasterizes the icon at the appropriate physical resolution. Per-OS DPI
behavior (Retina pixel-doubling on macOS, per-monitor scaling on
Windows, Tk scaling on Linux) is documented separately on the
[Platform → Images & DPI](../../platform/images-and-dpi.md) page.

---

## Caching

`_image_for(name, size, color)` (`bootstyle_builder_base.py:667-691`)
maintains a `cache` dict local to the surrounding `map_stateful_icons`
call. Within a single style rebuild, identical `(name, size, color)`
triples reuse the same `PhotoImage` object — so a button whose hover and
focus states map to the same icon allocates one image, not two.

The cache is **rebuilt on every style rebuild**, which fires on:

- `<<ThemeChanged>>` (the bootstyle wrapper registers every widget for
  this event at construction).
- `widget.configure(icon=…)` (the `IconMixin._delegate_icon` path at
  `widgets/mixins/icon_mixin.py:21-27` calls `rebuild_style()`).
- Any other `configure_style_options(...)` write that triggers
  `rebuild_style()`.

Because the cache is local to `map_stateful_icons`, two widgets that
display the same icon at the same size and color do **not** share a
`PhotoImage` — each gets its own. The redundancy is by design: ttk owns
each widget's element images via the resolved style, and the per-rebuild
local cache keeps the image lifetime bound to the style rebuild that
created it.

For application-managed images outside the icon pipeline (logos,
photographs, custom raster assets) — see [Images](images.md) and the
`Image` utility documented on the
[Icons & Images overview](index.md#image-general-image-utility), which
maintains a process-wide cache keyed by source.

---

## Where to read next

| Question | Page |
|---|---|
| What's the constructor surface of `BootstrapIcon` and the `IconSpec` shape? | [Icons & Images overview](index.md) |
| How do I cache and load arbitrary images that aren't Bootstrap icons? | [Images](images.md) |
| What controls the framework's global DPI scaling factor, and how does it differ per OS? | [Platform → Images & DPI](../../platform/images-and-dpi.md) |
| How do I use `icon=` in practice (string form, dict form, common patterns)? | [Guides → Icons](../../guides/icons.md) |
| What's the design vocabulary for icons in the framework? | [Design System → Icons](../../design-system/icons.md) |
