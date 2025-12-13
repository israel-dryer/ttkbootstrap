---
icon: fontawesome/solid/palette
---

# Design System Overview

ttkbootstrap 2 layers a semantic design system on top of Tk's classic widgets. At its core sits the `Style` singleton, which wires together ThemeProvider instances, Bootstyle parsing, and the widget registry so every component can request a variant such as `success-outline.TButton` and receive consistent, theme-wide styling.

## Theme provider & tokens

ThemeProvider instances and the `use_theme()` helper keep color palettes, gradients, and accent metadata synchronized across widgets. Calling `ttk.set_theme()` or a custom provider drives every registered `Style` so the shared tokens stay tied to the current palette.

## Bootstyle parsing

Bootstyle helpers split `bootstyle` strings into their `color`, `variant`, and `widget_class` segments, then let the builder choose the correct TTK style name. The Bootstyle token system assumes the widget unless you add an explicit suffix, and the variant defaults to `default` when you omit it.

## Style registry & rebuilding

Each Bootstyle call registers the chosen combination via `Style.register_style()` so theme switches (`ttk.set_theme()` or `ttk.toggle_theme()`) rebuild the same styles with the new palette. That registry also records extra options (borders, icons, custom width) and hashes them in the style name so you configure them through the widget API rather than hand-editing the generated string.

Start here before diving into the more focused design sections.
