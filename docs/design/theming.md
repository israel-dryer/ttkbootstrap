---
icon: fontawesome/solid/paintbrush
---

# Theming

Themes in ttkbootstrap 2 are JSON assets under `ttkbootstrap/assets/themes/*.json` (plus the legacy bundle). Each file lists the palette, semantic tokens, display information, and color variants that the builders consume. `ThemeProvider` loads all of them at startup, registers aliases (such as the configured light/dark pair), and keeps the active palette synchronized with `Style` so every widget sees the same colors.

You can explore the registered themes with `ttk.get_themes()` (and avoid calling `Style()` directly) to build selectors, then pass one of the names into `ttk.App(theme="cosmo")` or use the helper `ttk.set_theme("cyborg")`. These calls switch the active `ThemeProvider`, rebuild cached styles, and emit the virtual `<<ThemeChanged>>`/`<<LocaleChanged>>` events so localization-aware widgets refresh as well.

### Runtime usage

- Call `ttk.set_theme("solar")` before creating your UI or at runtime to swap palettes immediately.
- Use `ttk.toggle_theme()` to flip between the light/dark pair defined in `AppSettings` (usually `light_theme` and `dark_theme`). That toggles `ThemeProvider`, rebuilds every registered style, and re-styles legacy Tk widgets through `Style`'s rebuild hooks.
- Inspect `ttk.get_style().colors` or `ThemeProvider.colors` when custom graphics, charts, or iconography need to align with the active palette instead of hardcoding hex values.
- Set the initial app theme via `App(settings=AppSettings(theme="flatly"))` or call `ttk.set_theme()` from a settings screen to let users pick their favorite palette.

### Discovering themes

- `ttk.get_themes()` returns `{"name","display_name"}` pairs so you can present readable labels while wiring the canonical name into `ttk.set_theme()`.
- The JSON assets include metadata such as `mode`, semantic tokens, and color ramps, so Bootstyle builders output consistent styles without manual color math unless you are authoring a theme (that section comes later).
- Theme styles remember their generated names, so registered combinations like `success-outline.TButton` rebuild automatically whenever you switch themes.

These runtime helpers and the registered catalog keep ttkbootstrap widgets, dialogs, and layout helpers harmonized with the active theme without manual style hacking.
