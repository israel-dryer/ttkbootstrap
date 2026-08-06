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

Converting a 1.x theme
----------------------

A custom theme saved by 1.x — a ``user.py`` holding a ``USER_THEMES`` dict, a
``.py`` holding a ``ThemeDefinition(...)`` call, or a JSON file for
:meth:`~ttkbootstrap.Style.load_user_themes` — converts to the equivalent
``Theme(...).register()`` call:

.. code-block:: bash

   ttkb convert-theme user.py -o brand.py

Pass ``-o`` to write a file, or omit it to print to standard output. Every
theme in the file converts. See :doc:`Migrating to 2.0
</user-guide/getting-started/migrating>` for what carries over.

See also
--------

- :doc:`Theming & Colors </user-guide/feature-guides/theming>` — how to pick,
  switch, and build themes, with examples.
- :doc:`styling` — the ``Style`` engine that consumes these themes.
