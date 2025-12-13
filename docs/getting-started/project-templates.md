---
icon: fontawesome/solid/layer-group
---

# Project Templates

ttkbootstrap 2 ships with opinionated templates so you can spin up production-ready projects quickly. Each template includes a structured folder layout, theming defaults, and example widgets that match the catalog.

![Template placeholder](https://placehold.co/800x800/FFFFFF/333333.webp?text=Template%20Preview&font=lato)

## Minimal App

- Lightweight entry point (`app.py`) that initializes `Style`, configures a single window, and documents the recommended folder layout.
- Ideal for tutorials or testing new widgets.

## Desktop App

- Starts with a `PageStack`/`Notebook` layout, navigation controls, and configuration for assets/fonts.
- Includes packaging bits (e.g., a basic `pyproject.toml`, resource manifest) to jumpstart PyInstaller or briefcases.

## Themed App

- Demonstrates multiple palettes, accent overrides, and runtime theme switching hooks.
- Contains helper modules for storing `theme.json` tokens, custom fonts, and a `ThemeSwitcher` widget.

## Localized App

- Template for multilingual applications with message catalogs and formatting helpers.
- Provides a lightweight localization loader plus sample date/number outputs.

## How to use

1. Clone the template directory from the repository (or generate it via the CLI when available).
2. Install dependencies (`python -m pip install -r requirements.txt`).
3. Update `.env` or configuration files with project-specific values.
4. Run the template and gradually swap in your real business logic.
