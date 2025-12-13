---
icon: fontawesome/solid/language
---

# Localization

Localization in ttkbootstrap 2 is designed for people building real desktop apps who need translated strings, locale-aware numbers, and coordinated widgets that refresh whenever the user changes language.

## How the catalog works

`MessageCatalog` combines a gettext translator (loaded from `locales/<lang>/LC_MESSAGES/*.mo`) with Tcl/Tk msgcat so the toolkit understands both modern gettext keys and legacy Tcl formatting (like `%1$s`). It keeps runtime overrides in sync between gettext and msgcat, strips mnemonic `&` markers, and fires the `<<LocaleChanged>>` virtual event whenever `MessageCatalog.locale(...)` switches to a new locale. Your widgets listen to that event (the `LocalizationMixin` already does) so they can update their currently registered text or value specs.

The catalog also exposes helpers such as `set`, `set_many`, `max`, and `preferences` if you need to inject translations at runtime without editing the compiled catalogs. `MessageCatalog.translate` prefers your overrides first, then gettext, and finally Tcl msgcat to keep formatting consistent even when you use positional arguments.

## Localized specs and formatting

Two helper classes describe what needs translation:

- `LocalizedTextSpec` (shortcut `L(key, *fmtargs)`) signals that a string should be translated using the catalog and optional formatting arguments.
- `LocalizedValueSpec` (shortcut `LV(value, format_spec)`) tells ttkbootstrap to format numbers, dates, and currencies through `IntlFormatter` so they look native to the active locale.

The `LocalizationMixin` is included in most widgets. It captures `localize` and `value_format` arguments, stores the specs in `_localized_fields`, and resolves them whenever `<<LocaleChanged>>` fires. The mixin pushes the localized results into your widget via a `textvariable`, `StringVar`, `variable`, or direct `configure()` call. If a widget exposes reactive signals (`textsignal`/`textvariable`), the mixin can insert a private formatter so the signal values are also localized on each update.

## Field widgets make localization easy

Field-style composites (`Field`, `TextEntry`, `PasswordEntry`, `NumberEntry`, etc.) hook into the mixin from the start. When you pass `label`, `message`, or `value_format`, the field registers those strings via `LocalizationMixin.register_localized_field`. That means:

- Labels, helper text, and validation messages automatically translate when the locale changes.
- Passing `localize='auto'` or `True` lets the mixin translate literal strings. Set `localize=False` to keep text verbatim.
- Numeric fields can use `value_format` (e.g., `'currency'`, `'percent'`) or share a signal so every update respects the locale.
- Validation hints and add-on labels share the same localization logic, so your form messages stay synchronized.

## Recommended steps for new users

1. Generate gettext catalogs (Babel, gettext, etc.) and place them under `locales/<lang>/LC_MESSAGES/messages.mo`.
2. Call `MessageCatalog.init(locales_dir=...)` before building widgets so both gettext and Tcl msgcat are configured.
3. Prefer `L()` and `LV()` specs for any text or observable value that should translate.
4. Pass `localize` and `value_format` to widgets that support them, or register additional fields manually with `register_localized_field()` if you have extra labels or tooltips.
5. Use field widgets when possible?they already tie labels, helper text, validation, and numeric formatting into the localization system.

## App settings you can tweak

`get_app_settings()` exposes a shared `AppSettings` object for every `ttk.App`. You can configure these values when creating the app (e.g., `App(settings=AppSettings(locale="ja"))`) to override the initial locale and formatting policy before any widgets are built. The settings include:

- `locale` and `language` to define the initial locale (e.g., `en_US`) and base language.
- `date_format`, `time_format`, `number_decimal`, and `number_thousands` so you can override the defaults that `IntlFormatter` and numeric fields will honor.
- `localize_mode` (`"auto"`, `True`, `False`) which controls the default behavior for wrapping literal widget strings in localization specs. Widgets respect this global policy but you can override it per widget using the `localize` argument.

Adjust these settings before creating widgets if you want to lock down a specific policy, or mutate them afterward to influence future widgets. Together with the catalog, specs, mixin, and field composites, these settings give you a consistent localization story across the app.

If you only need to rotate locales at runtime, call `ttk.MessageCatalog.locale("ja")` (or another locale code) so gettext/msgcat swap languages and every widget hears `<<LocaleChanged>>`.
