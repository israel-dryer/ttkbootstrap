---
icon: fontawesome/solid/droplet
---

# Color System

The color system lets you express semantic intent while styling widgets. Every widget accepts a `bootstyle` string that encodes a color token, an optional variant, and an optional widget suffix. Builders combine those inputs with the widget's defaults so `bootstyle="success-outline"` yields a green outline button and `bootstyle="info"` respects the informative accent.

## Bootstyle anatomy

- **Color token** (for example `primary`, `success`, `danger`) describes the intent behind the hue.
- **Variant** (such as `outline`, `ghost`, `link`, `solid`) defines the treatment around the color.
- **Widget suffix** (defaults to the widget class) scopes the variant to a specific control when you need cross-widget overrides.

The Bootstyle token system assumes the widget unless a suffix is provided, and the variant defaults to `default` when omitted.

## Anchoring to the theme

Use the shared palette, not isolated hex values: `ThemeProvider` instances and `ttk.set_theme()`/`ttk.toggle_theme()` keep every registered `Style` in sync via the live `Style.colors` map. Pick colors from the published token list so every component remains harmonized, and extend the palette with hashed styles only when extra options (border, icon, icon separator, rounded corners) require a unique style.

When you need to anchor a style to the current theme or inspect which tokens are available, read `Style.colors` directly or rely on Bootstyle strings that reuse semantic names, avoiding inventing your own palette choices. The builder only emits hashed style names such as `bs[2fb014e9].success.Outline.TButton` when it combines color, variant, widget, and extra options.

## Modifiers

Modifiers inside brackets adjust the selected token before the builder applies the variant:

- `[shade]` selects a specific shade (for example, `primary[100]`).
- `[elevation]` shifts the color lighter or darker relative to the base (for example, `background[+1]`).
- `[subtle]` blends the color with the surface tone for softer backgrounds.
- `[muted]` derives a respectful foreground with enough contrast for text on busy surfaces.

Chain modifiers like `primary[100][muted]` or `background[+2][subtle]` to fine-tune emphasis while staying aligned with the semantic token.

## Hashed style names

When you include a widget suffix or tweak borders, icons, or padding through the builder, the style registry hashes those extras into a deterministic name (`bs[2fb014e9].success.Outline.TButton`). Treat hashed names as implementation details; configure the widget API, and let Bootstyle handle the actual TTK style name. Only introduce `bs[...]` styles when the combination cannot be represented by the semantic color, variant, and widget names alone.

Use this page to track the tokens available in each theme and rely on Bootstyle strings or `Style.colors` to reuse palette choices. Custom hashed styles should be rare and reserved for tweaks that would otherwise prevent sharing colors across widgets.
