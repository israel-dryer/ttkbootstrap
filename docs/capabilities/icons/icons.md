# Icons

ttkbootstrap treats icon usage as a **shared capability** — all icon-bearing
widgets plug into a common pipeline rather than each implementing their own
icon handling.

---

## Provider resolution

When a widget specifies an icon by name, the framework resolves it through an
**icon provider**:

- registered providers are searched in priority order
- the matching provider supplies the raw icon data
- the framework renders, colors, and caches the result

The built-in provider supplies the bundled icon set. Additional providers can
be registered to expose icons from third-party libraries or application-specific
icon sets. All sources are treated uniformly by the capability.

---

## State integration

Icon-bearing widgets register their icons with the TTK style engine, not as
static image references. When widget state changes — disabled, hover, pressed,
selected — the style engine selects the icon image mapped to that state.

This gives icons automatic visual feedback (muted when disabled, emphasized
when active) without any per-widget handling.

State expressions follow TTK conventions:

| Expression | Meaning |
|---|---|
| `"selected"` | Widget is selected or checked |
| `"disabled"` | Widget is disabled |
| `"hover !disabled"` | Mouse over, not disabled |
| `"pressed !disabled"` | Being clicked |
| `"focus !disabled"` | Has keyboard focus |

---

## Theme-driven coloring

Icon color is derived from the active theme's foreground token, not hardcoded
into the image asset.

When the theme changes, icon colors are recalculated to match. A single icon
name renders appropriately in both light and dark themes without application
code. Color overrides in icon specs bypass this pipeline and use the explicit
value directly.

---

## DPI scaling

Icons are sized in logical pixels and scaled to physical pixels at render time.

The framework reads the display scale factor and rasterizes the icon at the
appropriate physical resolution. Application code uses the same logical size on
all displays — DPI differences are invisible to the caller.

See [Platform → Images & DPI](../../platform/images-and-dpi.md) for per-OS DPI
behavior.

---

## Caching

Rendered icons are cached to avoid repeated rasterization and recoloring.

The cache is invalidated on theme change (color update) and on display DPI
change (size update). Applications that use the same icon across many widgets
benefit automatically — the icon is rasterized once and reused.

---

## Further reading

- [Guides → Icons](../../guides/icons.md) — practical usage: string form, dict
  form, state overrides, common patterns.
- [Design System → Icons](../../design-system/icons.md) — icon vocabulary and
  design intent.
- [Images](images.md) — image lifecycle and caching.
