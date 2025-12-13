---
icon: fontawesome/solid/circle-info
---

# What is ttkbootstrap 2?

ttkbootstrap 2 is a documentation-driven framework for building modern Tkinter applications. It preserves the stability of `ttk` while layering on refined theming, responsive layout helpers, Bootstyle tokens, and opinionated defaults inspired by contemporary design systems.

![ttkbootstrap concept](https://placehold.co/800x800/FFFFFF/333333.webp?text=Concept%20Vision&font=lato)

## Design pillars
- **Tk-native**: Still builds on `ttk` widgets and the Tk event loop so the learning curve stays gentle and compatible with the platform.
- **Theming-first**: Every widget respects shared color tokens, typography tokens, and runtime theme switching helpers such as `ttk.set_theme()` and `ttk.toggle_theme()`.
- **Pattern-rich**: Structured guidance for inputs, feedback, dialogs, layouts, navigation, and forms keeps the experience consistent across the catalog.
- **Documentation-first**: Story-driven docs and the guided navigation make each widget, helper, and design concept directly reachable.

## Architecture at a glance
1. **Application shell** - `ttk.App` boots a themed window, applies DPI adjustments, and exposes `Style`/`ThemeProvider` helpers for consistent palettes.
2. **Widget catalog** - Inputs, data display, navigation, feedback, layout, and dialog primitives share Bootstyle parsing so `success-outline` or `primary-link` behave the same in every control.
3. **Utilities & dialogs** - Theme helpers, locale-aware messaging, Form helpers, PageStack navigation, and the Dialog hierarchy live next to the widget registry to simplify real-world flows.
4. **Signals & layout patterns** - Reactive signals, virtual-event payloads, and layout helpers such as `ScrollView` and `PageStack` let you compose interactive, localized experiences without reinventing glue logic.

Read the rest of Getting Started for hands-on commands, sample apps, templates, and community resources.
