Themes
======

Theming is ttkbootstrap's headline feature. It ships **30 built-in themes** as
**15 light/dark families** — pass one to ``theme=`` on the app and every
``bootstyle`` widget recolors coherently, light or dark.

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(theme="nord-dark")     # any name from the catalog below

Each card shows a family in one mode — its accent palette, the filled / outline /
ghost buttons, and the input controls. The value in the **combobox** is the exact
theme name to pass as ``theme=`` (``bootstrap-light``, ``nord-dark``, …). Switch
the tab to compare the light and dark side of every family.

.. tab-set::

   .. tab-item:: Light

      .. image:: /_static/examples/theming-gallery-light.png
         :class: tb-gallery
         :width: 590px
         :alt: A sample card for each of the 15 theme families in light mode

   .. tab-item:: Dark

      .. image:: /_static/examples/theming-gallery-dark.png
         :class: tb-gallery
         :width: 590px
         :alt: A sample card for each of the 15 theme families in dark mode

.. seealso::

   :doc:`Theming & Colors </user-guide/feature-guides/theming>` — how to choose
   and switch themes at runtime, read a theme's resolved colors, and build your
   own.
