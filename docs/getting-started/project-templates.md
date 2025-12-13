---
icon: fontawesome/solid/layer-group
---

# Project Templates

ttkbootstrap 2 ships with opinionated starter projects so you can jump into a packaged layout, theming setup, and feature surface without reinventing the wheel. Each template follows the new layout guidance, keeps Bootstyle tokens consistent, and demonstrates the runtime helpers discussed in Getting Started.

![Template preview](https://placehold.co/800x800/FFFFFF/333333.webp?text=Template%20Preview&font=lato)

## Template catalog

- **Minimal App**: A single-window starter that initializes `ttk.App`, applies a theme, and documents the recommended folder structure. Ideal for experimentation.
- **Navigation App**: Demonstrates `PageStack`-based navigation, contextual menus, and how to wire a toolbar/dashboard that remains responsive across palette changes.
- **Themed App**: Ships with multiple palette JSON files, a custom `ThemeProvider`, and a theme switcher widget so you can sample how `Style.colors` keeps colors in sync.
- **Form & Data App**: Shows `Form` widgets, `FormDialog`, `TableView`, and the signal-aware entries (TextEntry, PasswordEntry, SpinnerEntry, SelectBox) that keep model data live.
- **Localized App**: Bundles `MessageCatalog`, `LocalizedSpec`, and sample `.mo` assets so you can display translated labels, dates, and currency values right away.

## Getting started with a template

1. Clone the template directory or generate it through the CLI when the official scaffolding lands.
2. Install dependencies via `python -m pip install -r requirements.txt` and configure any `.env` values (theme name, locale, API endpoints).
3. Run the template to confirm the layout, then gradually swap in your business logic while preserving the shared Bootstyle strings and typography tokens.
4. Update the theme assets or localization catalogs as needed and rerun `ttk.set_theme()` or `ttk.toggle_theme()` to test the runtime transitions.

Each template includes documentation and example widgets to guide you toward production-ready code while keeping the design system front and center.
