---
icon: fontawesome/solid/palette
---

# Design System Overview

ttkbootstrap 2 builds a cohesive design system on top of Tk's classic widgets by centralizing palettes, tokens, typography, icons, layout helpers, and localization so every control, dialog, and composite follows the same rules when the user switches themes or locales.

## Themes and style providers

Themes live as JSON assets under `ttkbootstrap/assets/themes/*.json` (plus the legacy bundle). Each file describes the palette, gradient helpers, semantic tokens, and metadata the builders consume. `ThemeProvider` loads all of them at startup, registers light/dark aliases defined in `AppSettings`, and exposes helpers such as `ttk.get_themes()`, `ttk.set_theme()`, and `ttk.toggle_theme()` so you can swap palettes without touching `Style()` directly. `Style` subscribes to the active provider, rebuilds every registered Bootstyle when the theme changes, and exposes `ttk.get_style().colors` so you can align custom graphics with the live palette.

## Bootstyle parsing and registry

Every widget accepts `bootstyle` strings such as `success-outline.TButton`, which the Bootstyle helpers split into `color`, `variant`, and `widget_class`. Builders generate deterministic TTK style names (including hashed names when extra options like icons or borders are present). `Style.register_style()` remembers each combination plus any custom options so theme switches (`ttk.set_theme()`, `ttk.toggle_theme()`) rebuild them automatically without you re-specifying the string.

## Typography, icons, layout, and localization

- Named typography tokens (`body`, `heading-md`, `display-xl`, etc.) plus FontMixin modifiers keep text styles consistent; updating a token via `Typography.update_font_token()` or `Typography.set_global_family()` refreshes every widget that references it.
- Icons are served by the built-in `ttkbootstrap-icons` provider; you can pass a glyph name or icon spec (e.g., `{'name': 'arrow-up-square', 'size': 25}`) and optionally state overrides. The CLI browser (`ttkbootstrap-icons`) helps you preview glyphs that already run through the Bootstyle palette.
- Layout helpers (Frame, ScrollView, PageStack, Notebook, etc.) respect the same Bootstyle tokens and encourage shallow hierarchies (three levels max) for maintainability.
- Localization uses `MessageCatalog`, `LocalizedSpec` helpers (`L`, `LV`), and `LocalizationMixin` so text, validation hints, and signal-driven values re-resolve whenever `<<LocaleChanged>>` fires.

Start here to see how palettes, Bootstyle tokens, typography, icons, layout, and localization layer together; the other design pages dig into each topic with the shared rules in place.
