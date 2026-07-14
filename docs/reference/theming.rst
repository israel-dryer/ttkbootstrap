Theming
=======

A theme is a named color scheme the engine turns into widget styles.
``Theme`` declares a theme *family* in code from a handful of anchor colors;
``ThemeDefinition`` is the per-mode container the engine consumes; and
``Colors`` is the resolved palette you read off the active theme (through
``Style.colors``). ``install_legacy_themes`` brings the pre-2.0 theme names
back for migration. The :doc:`Theming & Colors
</user-guide/feature-guides/theming>` guide shows them in use.

Declaring a theme
-----------------

.. autoclass:: ttkbootstrap.Theme
   :members:

.. autoclass:: ttkbootstrap.style.ThemeDefinition
   :members:

The color palette
-----------------

.. autoclass:: ttkbootstrap.style.Colors
   :members:

Legacy themes
-------------

.. autofunction:: ttkbootstrap.install_legacy_themes

See also
--------

- :doc:`Theming & Colors </user-guide/feature-guides/theming>` — how to pick,
  switch, and build themes, with examples.
- :doc:`styling` — the ``Style`` engine that consumes these themes.
