# ttkbootstrap v2 Roadmap

## Overview
Version 2 of **ttkbootstrap** is about refreshing the library inside and out — cleaner styles, better organization, and a smoother developer experience. 
The goal isn’t to rewrite everything, but to refine what already works, fix long-standing inconsistencies, and modernize the overall look and feel.

There will be a few small breaking changes to make the API more consistent and maintainable, but they’ll be clearly documented and easy to adapt to.

---

## Style and Theme Updates

### A simpler styling engine
The current engine draws widget layouts on the fly. It’s flexible, but also complex.  For v2, the plan is to switch to an **image color-replacement engine** — the same approach that proved much faster and easier to maintain in experiments with `ttkbootstrap-next`.

This change keeps all the benefits of dynamic color and style rendering, but removes a ton of overhead from the codebase. It also makes it much simpler for users to create custom themes.

### Consistent bootstyle keywords
Over time, the `bootstyle` parameter has grown a few different patterns and aliases. That’s going away in v2.  There will be **one clean, consistent way** to use bootstyle keywords.

To help with migration, an **app-level compatibility flag** will be available in `AppConfig`, so you can still use the old format if needed (though it won’t be recommended).

### Refined and expanded themes
The built-in themes are getting a complete review — color contrast, accessibility, and general visual polish will all be improved.  Several new light and dark themes will be added as well, with better balance and more modern tones.

### Easier custom themes
Creating a user-defined theme has always been possible, but not exactly smooth.  In v2, it’ll be straightforward to set up your own palette, fonts, and layout preferences — all without digging into the internal engine.  You’ll also be able to pick a default icon provider, and control things like scaling and default sizes more easily.

### Simulated transparency
Tkinter doesn’t really support transparency, but v2 will fake it in a smart way.  Widgets will be able to **inherit background colors** from their parent containers automatically, giving the illusion of transparency — for example, rounded buttons that blend perfectly into dark or light frames.

### Built-in icon support
With the new `ttkbootstrap-icons` packages, icon support will finally be a first-class feature.  The library will include a default icon provider out of the box (BootstrapIcons), and you can swap providers globally with a single AppConfig setting.
This means consistent iconography across buttons, dialogs, and built-in UI elements — no more manually attaching images everywhere.

---

## Widgets

Version 2 will introduce new widgets and polish up some existing ones.  
The focus is on filling long-standing gaps while keeping things lightweight and native to Tkinter.

### New widgets
- **FileChooser** – A themed, cross-platform file picker (especially helpful for Linux users).
- **PasswordEntry** – Entry widget with a show/hide toggle.
- **NumericEntry** – Entry that only accepts numbers, with formatting and optional stepper buttons.
- **DateEntry** – Updated and refactored date picker.
- **FileEntry** – Entry field with a built-in file browser button.
- **LabeledEntry** – A wrapper for entries that supports inline labels, validation messages, and add-on buttons.
- **StackNavigator** – A simple navigation container for switching between views or panels.
- **Notebook** – Improved tab management, better visuals, and more flexibility.
- **ListView** – A custom list widget that supports icons, buttons, and selectable rows.

### Other enhancements
- Better localized number and text formatting.
- Easier integration with message catalogs for translations.
- More consistent widget defaults across platforms.

---

## Global App Configuration

Version 2 introduces a new **AppConfig** system — a static, global configuration that controls application-wide defaults.

To use, just import and configure it once at the start of your app, like this:

```python
from ttkbootstrap import AppConfig

AppConfig.set(
    theme="flatly",
    font=("Segoe UI", 10),
    icons="lucide",
    legacy_keywords=False
)
```

This configuration is shared across all widgets and modules, so you can change themes, fonts, or icons globally with one call.  
AppConfig will also handle other preferences like window defaults, language, and scaling.

---

## Command Line Tools

A simple **CLI tool** will be included to make it easier to get started with ttkbootstrap projects.  
It’ll support things like:
- Creating new project scaffolds
- Generating or editing themes
- Packaging your app with PyInstaller

The idea is to speed up setup and eliminate repetitive manual steps.

---

## Localization

The message catalog system is being refactored for better flexibility and cleaner integration with widgets.  
The new design will make it easier to:
- Translate app-level text resources
- Switch languages at runtime
- Contribute new translations without modifying core files

---

## Documentation

The docs will be completely reorganized for v2. The goal is to make them **easier to navigate and more example-driven**.  
You can expect:
- Better structure and topic grouping
- Updated tutorials and walkthroughs
- A refreshed gallery with real-world apps built using ttkbootstrap
- Highlighted community projects and contributions

---

## Development and Contribution

v2 will include a cleaner, more consistent developer experience, both for contributors and users reading the source.

### Highlights
- Consistent code style and naming conventions
- Type hints and docstrings throughout
- Cleaner project structure and logical module organization
- Contribution guidelines covering PR process, code style, and examples
- Templates for bug reports and feature requests
- Expanded test coverage for widgets and layout behavior

The end goal is to make contributing to ttkbootstrap as straightforward and enjoyable as using it.

---

## Summary
**ttkbootstrap v2** is a thoughtful evolution of the library — not a rewrite, but a refinement.  It brings modern styling, unified conventions, true icon support, and better documentation while keeping the classic API that people already know.

The focus is on clarity, stability, and long-term maintainability — helping ttkbootstrap remain the go-to toolkit for building beautiful Tkinter apps with modern design.
