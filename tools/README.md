# Localization tools

This folder houses the helper that drives the gettext workflow for ttkbootstrap.
`tools/make_i18n.py` now only wraps `pybabel compile`, so you can refresh the shipped
`.mo` files after editing the English catalog.

## Typical workflow

1. **Edit the English catalog** (`src/ttkbootstrap/assets/locales/en/LC_MESSAGES/ttkbootstrap.po`)
   or `development/SEMANTIC_KEYS.md` to define the semantic IDs that your library exposes.
2. **Compile the catalogs** so the wheel ships the updated `.mo` files:
   ```
   python tools/make_i18n.py
   ```
   The helper only runs `pybabel compile` now (the other extract/init/update steps have been removed because there are no `_()` calls left in the source). Use `-d`/`-D` if you need to target a different directory/domain.

## Where translations live

- **Canonical catalogs:** `src/ttkbootstrap/assets/locales/<lang>/LC_MESSAGES/ttkbootstrap.{po,mo}`
  are the files extracted, edited, and shipped with the package.
- **Top-level `locales/` directory:** this is a legacy snapshot from the old msgfmt workflow.
  It still contains `.po`/`.mo` files, but it is **not used** during extraction or packaging
  (and it currently lacks an English default). Please treat it as archived history and keep
  your edits in `src/ttkbootstrap/assets/locales`.

## Staying on top of semantic keys

- The canonical list of semantic message IDs lives in `development/SEMANTIC_KEYS.md`.
  Use that file to confirm you are not missing tokens; new keys should appear first in the
  English catalog (`src/ttkbootstrap/assets/locales/en/LC_MESSAGES/ttkbootstrap.po`).
- Edit the English `.po` directly to add or adjust semantic keys, then re-run
  `python tools/make_i18n.py` so `ttkbootstrap.mo` matches.

## Handy reminders

- When reviewing translations, `MessageCatalog.locale('fr')` and `<<LocaleChanged>>` help you
  see how the UI behaves in another language.
- `development/SEMANTIC_KEYS.md` is also the reference for migrating away from literal English
  strings: you can search or copy new keys into widgets instead of calling `MessageCatalog.translate`.
