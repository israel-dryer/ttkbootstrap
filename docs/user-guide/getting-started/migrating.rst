Migrating to 2.0
================

.. note::

   This guide is being written for the 2.0 release. It will fold in the theme
   and icon migration notes staged in ``development/2_0_theme_migration.md``.

ttkbootstrap 2.0 is a cleanup and consolidation release. This page will cover
the breaking changes and their migration paths:

- **bootstyle strings** — the canonical single-string grammar; tuple/list forms
  are deprecated.
- **Theme names** — the semantic-anchor catalog (default ``bootstrap-light``);
  legacy Bootswatch names auto-register on first use.
- **Removed shims** — top-level module shims retired in favor of
  ``ttkbootstrap.widgets`` / ``ttkbootstrap.dialogs``.
- **Icons** — the character/emoji ``ttkbootstrap.icons`` catalog is removed;
  dialog and widget glyphs now render from the built-in icon font.
