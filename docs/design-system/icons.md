---
title: Icons
---

# Icons

Icons are the fourth token vocabulary in the design system: you supply
a **glyph name** (`"gear"`, `"chevron-down"`, `"star-fill"`) and the
framework renders it through the active icon provider, sized for the
current DPI, recolored to match the widget's foreground state.

The bundled provider is **Bootstrap Icons** (v1.13.1), the same set
used by Bootstrap CSS. It ships ~3,400 named glyphs across two visual
styles: `outline` (the default) and `fill`.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Icons")
ttk.Button(app, text="Settings", icon="gear").pack(padx=20, pady=4, fill="x")
ttk.Button(app, text="Save", icon="save", accent="primary").pack(padx=20, pady=4, fill="x")
ttk.Button(app, text="Delete", icon="trash3", accent="danger").pack(padx=20, pady=4, fill="x")
app.mainloop()
```

## The Bootstrap icon set

Every icon has a kebab-case name. There are two visual styles:

| Style | Naming convention | Count | Default? |
|---|---|---|---|
| `outline` | bare name (`gear`, `star`, `chevron-down`) or `-outline` suffix | ~2,750 | yes |
| `fill` | `-fill` suffix (`gear-fill`, `star-fill`, `heart-fill`) | ~700 |  |

The outline style is the framework default — `icon="star"` resolves
to the outline glyph. To use the fill style, append the suffix
explicitly: `icon="star-fill"`. Most outline icons have a `-fill`
counterpart, but not all. (Many of the outline-only glyphs are
informational symbols like `123`, alphabet letters, currency marks.)

Browse the full catalog at
<https://icons.getbootstrap.com/> — the names there match the
ttkbootstrap glyph names one-for-one.

## Two value forms

The widget `icon=` kwarg accepts two shapes:

| Value | Use |
|---|---|
| A glyph name string | `icon="gear"` — resolves through the default provider with default size and inherited color. |
| An `IconSpec` dict | `icon={"name": "gear", "size": 24, "color": "#ff6600"}` — fine-grained control over size and color, plus per-state overrides via `"state"`. |

The string form is what you'll use most. Reach for the dict when you
need a non-default size, an explicit color, or different glyphs for
different widget states (e.g. a `chevron-down` collapsed icon that
becomes `chevron-up` when expanded).

The full `IconSpec` shape — `name`, `size`, `color`, and the per-state
override dict — is documented under [Capabilities → Icons & Imagery](../capabilities/icons/icons.md).

## Conventions

### Color inheritance

By default, icons render in the widget's **foreground color**, not in
a fixed color. A `Button(text="Save", icon="save", accent="primary")`
shows a primary-colored icon when the button is enabled, a muted icon
when disabled, and a high-contrast icon when hovered — without you
specifying any color in the icon spec.

If you pass an explicit `color` in an `IconSpec`, it overrides the
inherited foreground. PIL color strings (`"red"`, `"navy"`) and hex
values (`"#ff6600"`) work directly.

Theme tokens (`"primary"`, `"success"`, etc.) in `IconSpec.color` are
resolved through the style engine before reaching PIL.
Hex strings and PIL named colors also work directly.

### Size and DPI

Icons size in pixels relative to the active scaling factor. Default
size is widget-class-dependent — most buttons use 16 px at 1× DPI;
larger composites scale up proportionally. Pass `IconSpec.size` to
override.

The framework caches resolved icons by `(name, size, color)`, so
re-rendering the same icon at the same size doesn't regenerate the
PIL image.

### State-aware variants

The `IconSpec.state` map lets a single widget show different icons in
different ttk states. The keys are ttk state expressions
(`"hover"`, `"pressed !disabled"`, `"selected"`, etc.); values are
either a replacement glyph name or a partial spec.

```python
import ttkbootstrap as ttk

app = ttk.App(title="State icons")
ttk.Button(
    app, text="Toggle",
    icon={
        "name": "chevron-right",
        "state": {"selected": {"name": "chevron-down"}},
    },
).pack(padx=20, pady=20)
app.mainloop()
```

The full state-expression syntax (with `!` negation and combined
predicates) is documented under [Capabilities → Icons](../capabilities/icons/icons.md).

## Which widgets support `icon=`

Five primitives accept `icon=` directly through the `IconMixin` family:

- `Button`
- `Label`
- `CheckButton` (and its subclass `Switch`)
- `RadioButton`
- `MenuButton`

Composites that wrap these primitives forward `icon=` to the
underlying widget — `Toolbar.add_button`, `SideNav.add_item`,
`Tabs.add(...)` (via the inner `TabItem`), `MessageDialog` (via its
buttons), `OptionMenu`, `DropdownButton`, and most navigation
chrome accept icon names.

The widgets that do **not** accept `icon=` are the read-only data-
display widgets (Progressbar, Floodgauge, Meter, TableView,
TreeView, ListView), the layout containers (Frame, Card, LabelFrame,
PackFrame, GridFrame), and the input widgets that don't have a
chrome surface for an icon (TextEntry, NumericEntry — though these
display chevrons and step buttons, those aren't user-supplied
icons).

## Beyond glyph icons: the `Image` utility

For arbitrary raster imagery — application logos, photographic
content, pre-rendered diagrams — use `ttk.Image` instead. It's a
thin wrapper around PIL/Tk image handling that adds a cache layer so
the same image isn't reloaded every time it's referenced:

```python
import ttkbootstrap as ttk

app = ttk.App(title="Image utility")
logo = ttk.Image.open("logo.png")
ttk.Label(app, image=logo).pack(padx=20, pady=20)
app.mainloop()
```

`Image` is for *content* imagery — pictures the user sees as content,
not as UI affordances. Glyph icons (`BootstrapIcon`) are for UI
*affordances* — symbolic indicators that integrate with theming,
state, and DPI scaling.

The full `Image` API (`Image.open` / `Image.from_pil` /
`Image.from_bytes` / `Image.transparent`, plus the cache-management
surface) is documented under [Capabilities → Images](../capabilities/icons/images.md).

## Custom icon providers

The icon provider system is pluggable. You can replace the bundled
Bootstrap provider with another icon font (Font Awesome, Material
Symbols, an in-house glyph font) by subclassing `BaseFontProvider`
and registering it.

That's an advanced workflow — most apps stay with the bundled
provider — and it's documented under
[Capabilities → Icons & Imagery](../capabilities/icons/index.md).

## Where to read next

- The full `BootstrapIcon` / `IconSpec` API surface, including the
  per-state override map: [Capabilities → Icons](../capabilities/icons/icons.md).
- The `Image` utility for arbitrary raster content:
  [Capabilities → Images](../capabilities/icons/images.md).
- The token vocabulary that determines icon foreground colors:
  [Colors](colors.md).
- DPI scaling and image cache pinning at the platform layer:
  [Platform → Images & DPI](../platform/images-and-dpi.md).
