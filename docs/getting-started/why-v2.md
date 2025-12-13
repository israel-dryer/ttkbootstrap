---
icon: fontawesome/solid/star
---

# Why ttkbootstrap 2?

ttkbootstrap 2 is the library overhaul you asked for: redesigned theming, a richer widget catalog, a modern signal surface, and stronger localization while keeping the Tk/Ttk core stable.

## Theming & typography tokens

- **Semantic palettes**: `Style.colors` and the `ThemeProvider.use_theme()` helpers keep the live map of tokens in sync with every registered palette. Use `ttk.set_theme()` to pick a palette and `ttk.toggle_theme()` to alternate between light and dark without rebuilding widgets.
- **Typography system**: Named font tokens (`body`, `body-lg`, `heading-md`, `display-xl`, etc.) plus FontMixin modifiers such as `body[bold][underline]` let you update fonts in the constructor without creating new Tk `Font` objects. `Typography.update_font_token()` and `Typography.set_global_family()` adjust the tokens globally, while FontMixin modifiers tweak the current font inline.

## Widgets & controls

- **New entries**: TextEntry, PasswordEntry, PathEntry, TimeEntry, and the signal-aware SpinnerEntry give you specialty inputs that honor Bootstyle tokens.
- **Data display & feedback**: The upgraded TableView, FloodGauge, Meter, and ScrollView work with live data, while SelectBox, DropDownButton, and ContextMenu provide modern drop-down and contextual affordances.
- **Navigation & layout**: PageStack, Notebook helpers, and ScrollView provide structured navigation surfaces that pair with Bootstyle-styled controls.
- **Form helpers**: The Form widget and FormDialog simplify complex data entry flows, pooling validation, signals, and layout in one place.
- **Integrated icons**: The built-in `ttkbootstrap-icons` provider powers every `icon` parameter, exposes Bootstrap Icons glyphs (browse via `ttkbootstrap-icons` or `https://icons.getbootstrap.com`), and hooks into the icon mixin/stateful icon specs so hover/pressed/selected imagery stays aligned with Bootstyle colors.

## Reactive signals & events

- Widgets that support `textvariable` or `variable` now expose subscribable and mappable signals, so you can attach listeners, chain transformations, and push computed values without extra plumbing.
- The virtual event system accepts payloads now: `widget.event_generate("<<VirtualEvent>>", data={"key": value})` carries contextual data to subscribers.
- Most widgets provide `on_*` and `off_*` helpers (for example, `Notebook.on_tab_changed(...)`) to keep callbacks expressive while working with the signal surface.

## Dialogs & navigation

- Dialog, MessageDialog, QueryDialog, and the generalized Dialog API give you shared theming and layout hooks.
- ContextMenu, FormDialog, and the updated Form widget pair with buttons, drop-downs, and PageStack navigation so you can craft multi-step flows without rebuilding scaffolding.

## Tooling, localization & runtime

- Reactive signals, Bootstyle tokens, and the new typography system combine with the CLI templates, runtime helpers, and localized message catalogs.
- MessageCatalog, LocalizedSpec, and the LocalizationMixin keep translations, numeric/date formatting, and the `<<LocaleChanged>>` event in sync with your UI.
- The enhanced CLI templates, learning resources, and docs mirror the upgraded library surface so you can apply these features right away.
