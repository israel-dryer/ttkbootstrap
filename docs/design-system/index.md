---
title: Design System
---

# Design System

The ttkbootstrap design system is a set of **named tokens** that you supply
as widget kwargs and that the framework resolves through the active theme
into concrete colors, fonts, and icons. You never write hex codes, font
families, or icon paths in widget code — you write tokens, and the same
widget code adapts when the theme switches.

The design system has four token vocabularies and a theme layer that maps
them to values:

| Vocabulary | Widget kwargs that consume it | Token shape | Page |
|---|---|---|---|
| Color tokens | `accent=`, `surface=` | `"primary"`, `"success"`, `"card"`, `"chrome"` | [Colors](colors.md) |
| Variant axis | `variant=` | `"solid"`, `"outline"`, `"ghost"`, `"link"`, `"text"`, `"bar"`, `"pill"` (per widget) | [Variants](variants.md) |
| Font tokens | `font=` | `"body"`, `"caption"`, `"heading-lg"`, `"code"`, plus modifier syntax | [Typography](typography.md) |
| Icon names | `icon=` | `"gear"`, `"check"`, `"chevron-down"` (Bootstrap glyph names) | [Icons](icons.md) |

The values that tokens resolve to are defined in **theme JSON files**. Each
theme ships a palette of base colors plus semantic mappings; ttkbootstrap
derives surface, foreground, and stroke tokens from there. To change the
look, you switch themes — or define your own.

- Defining a theme palette: [Custom Themes](custom-themes.md)

---

## Tokens vs values

The whole point of the token layer is that you write `accent="primary"`
once and the framework picks the right hex code for the active theme. A
button on a light theme reads as `#2780e3` (Bootstrap blue); the same
button on a dark theme reads as a brighter shade chosen for contrast. No
widget code changes.

```python
import ttkbootstrap as ttk

app = ttk.App(title="Tokens", theme="bootstrap-light")
ttk.Button(app, text="Save", accent="primary").pack(padx=20, pady=20)
app.mainloop()
```

The same `accent="primary"` would render correctly on `bootstrap-dark`,
`ocean-light`, or any custom theme that defines a `primary` semantic
token. Values are the theme's responsibility; tokens are yours.

---

## How tokens reach the widget

When you pass a token to a widget, the framework runs through this chain:

1. **The token is captured** at construction time. `accent="primary"` is
   stored on the widget; `variant="solid"` selects a registered builder.
2. **The active theme resolves the token** to a concrete value. For colors,
   this happens in `Style.builder.color('primary')`, which reads the
   theme's `semantic` map and the derived shade spectrum. For fonts, the
   token is a registered Tk named font; for icons, it's a glyph name
   passed to the icon provider.
3. **A builder composes a ttk style** combining the resolved values with
   the variant's element layout. The result is a unique style name like
   `bs[<hash>].primary.TButton` cached for reuse.
4. **The widget is configured** with that style. Subsequent calls with
   the same tokens reuse the cached style; theme changes invalidate and
   rebuild.

The internal mechanics live under
[Platform → Styling Internals](../platform/ttk-styles-elements.md). The
design-system pages stay above that layer — they describe *which tokens
exist* and *what they mean*.

---

## What's in this section

### [Colors](colors.md)

The color-token surface: brand semantics (`primary` / `success` / etc.),
surface tokens (`chrome` / `content` / `card` / `overlay` / `input`),
foreground derivations (`on_card` / `on_card_secondary`), and the
`accent` vs `surface` axes that widgets consume. Also covers the shade
spectrum (`blue[100]`–`blue[900]`) and how `accent="primary"` is looked
up at runtime.

### [Variants](variants.md)

The visual-emphasis axis. Names which widgets accept which variants
(buttons take `solid` / `outline` / `ghost` / `link` / `text`; toolbuttons
take `solid` / `outline` / `ghost`; notebooks take `bar` / `pill` / `tab`;
most other widgets are `default`-only) and what each variant does to the
rendered chrome. Variants compose with `accent`: `accent="primary",
variant="outline"` is a primary-bordered button on a transparent background.

### [Typography](typography.md)

Font tokens (`body` / `caption` / `heading-lg` / `code` / etc.) and the
modifier syntax that adjusts size and weight without breaking the token
contract (`body+2[bold]`, `caption[italic 14]`). Themes resolve tokens
to platform-appropriate fonts (Segoe UI, SF Pro, DejaVu Sans).

### [Icons](icons.md)

The Bootstrap-icon glyph set, the `BootstrapIcon` value type, and the
provider system that resolves icon names to PIL images. Icons inherit
the widget's foreground color by default, scale with DPI, and re-render
on theme changes.

### [Custom Themes](custom-themes.md)

The theme JSON schema (`name` / `mode` / `foreground` / `background` /
`shades` / `semantic`), how shades expand into a 9-step spectrum,
which semantic tokens are required, and how to register a custom theme
so widget code keeps working unchanged.

---

## When to read this section

Use these pages as references — not as cover-to-cover reading. Common
questions and where they're answered:

- **What tokens can I pass to `accent=`?** → [Colors](colors.md)
- **Which surface should a sidebar / toolbar / card use?** →
  [Colors → Surface tokens](colors.md)
- **What does `variant="ghost"` look like vs `"outline"`?** →
  [Variants](variants.md)
- **Does this widget accept `variant=`?** → [Variants — per-widget table](variants.md)
- **What font tokens are available?** → [Typography](typography.md)
- **Can I bold or resize a token's font without forking?** →
  [Typography — modifier syntax](typography.md)
- **Where do icon names come from? Can I plug in a different set?** →
  [Icons](icons.md)
- **How do I make a custom theme?** → [Custom Themes](custom-themes.md)

For the *runtime mechanics* of how tokens are resolved into styles —
ttk style names, builder caching, theme change events — see
[Platform → Styling Internals](../platform/ttk-styles-elements.md). For
*application-level workflows* (switching themes at runtime, building
theme-aware widgets), see [Guides → Theming](../guides/theming.md) and
[Guides → Styling](../guides/styling.md).
