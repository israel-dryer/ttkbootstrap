Command line
============

Installing ttkbootstrap installs a command, ``ttkb``, for the things that are
not library calls: reporting the version, opening the demo, converting a 1.x
theme, and launching the theme designer.

.. code-block:: bash

   ttkb version
   ttkb demo
   ttkb convert-theme user.py -o brand.py
   ttkb creator

Run ``ttkb`` with no arguments, or ``ttkb <command> --help``, for usage.

.. note::

   The command installs under two names — ``ttkb`` and ``ttkbootstrap`` — that
   run the same thing.

   Every command also has a ``python -m`` spelling, which is what to use when
   your environment's scripts directory is not on ``PATH``.

Commands
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Command
     - What it does
   * - ``ttkb version``
     - Print the installed version, e.g. ``2.2.0``. Same value as
       ``ttkbootstrap.__version__``.
   * - ``ttkb demo``
     - Open the widget demo: every themed widget on one window, with a theme
       picker. Same as ``python -m ttkbootstrap``.
   * - ``ttkb convert-theme``
     - Convert a ttkbootstrap 1.x theme file into the 2.x
       ``Theme(...).register()`` form. Same as
       ``python -m ttkbootstrap.convert_theme``.
   * - ``ttkb creator``
     - Open ttkcreator, the theme designer. Same as ``python -m ttkcreator``.

version
-------

.. code-block:: bash

   $ ttkb version
   2.2.0

Prints the version of the installed distribution — the same string as
``ttkbootstrap.__version__``, and what to quote in a bug report.

.. code-block:: python

   import ttkbootstrap as ttk

   print(ttk.__version__)

demo
----

.. code-block:: bash

   ttkb demo

Opens a window showing the widget set under the current theme, with a picker
that switches themes live. It is a good first check that your install works and
a quick way to see what a theme looks like before choosing one.

convert-theme
-------------

.. code-block:: bash

   ttkb convert-theme <file> [-o <output>]

Reads a theme file saved by ttkbootstrap 1.x and writes the equivalent 2.x
``Theme(...).register()`` call. All three artifacts 1.x could produce are
accepted:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - File
     - Where it came from
   * - ``user.py`` (a ``USER_THEMES`` dict)
     - ttkcreator's *Save* and *Export all themes*
   * - ``.py`` (a ``ThemeDefinition(...)`` call)
     - ttkcreator's *Export theme definition*
   * - ``.json``
     - the :meth:`~ttkbootstrap.Style.load_user_themes` format

Every theme in the file converts. Output goes to standard output, or to the
file named by ``-o``.

.. code-block:: bash

   $ ttkb convert-theme user.py -o brand.py
   Wrote brand.py

Import the generated module and the themes are available by name:

.. code-block:: python

   import ttkbootstrap as ttk
   import brand  # registers the converted themes

   app = ttk.App(theme="acme-light")

See :doc:`Migrating to 2.0 </user-guide/getting-started/migrating>` for what
carries over and what 2.x derives instead.

creator
-------

.. code-block:: bash

   ttkb creator

Opens ttkcreator: edit a theme's accent, neutral, and background colors, preview
the result on live widgets, and export a ``Theme(...).register()`` snippet to
drop into your own app.

See also
--------

- :doc:`theming` — the ``Theme`` class the converter and ttkcreator both emit.
- :doc:`/user-guide/getting-started/migrating` — the 1.x to 2.0 migration guide.
