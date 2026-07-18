Themes
======

Theming is ttkbootstrap's headline feature. It ships **30 built-in themes** as
**15 light/dark families** — pass one to ``theme=`` on the app and every
``bootstyle`` widget recolors coherently, light or dark.

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(theme="nord-dark")     # any name from the catalog below

Each family is shown in both modes side by side — its accent palette, the
filled / outline / ghost buttons, and the input controls. The value in each
**combobox** is the exact theme name to pass as ``theme=``; the two cards are the
light/dark pair the :func:`~ttkbootstrap.App.toggle_theme` switch flips between.

.. seealso::

   :doc:`Theming & Colors </user-guide/feature-guides/theming>` — how to choose
   and switch themes at runtime, read a theme's resolved colors, and build your
   own.

bootstrap
---------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-bootstrap-light.png
      :class: tb-gallery
      :width: 264px
      :alt: bootstrap-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-bootstrap-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: bootstrap-dark theme — palette, buttons, and controls

pydata
------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-pydata-light.png
      :class: tb-gallery
      :width: 264px
      :alt: pydata-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-pydata-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: pydata-dark theme — palette, buttons, and controls

nord
----

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-nord-light.png
      :class: tb-gallery
      :width: 264px
      :alt: nord-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-nord-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: nord-dark theme — palette, buttons, and controls

solarized
---------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-solarized-light.png
      :class: tb-gallery
      :width: 264px
      :alt: solarized-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-solarized-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: solarized-dark theme — palette, buttons, and controls

catppuccin
----------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-catppuccin-light.png
      :class: tb-gallery
      :width: 264px
      :alt: catppuccin-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-catppuccin-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: catppuccin-dark theme — palette, buttons, and controls

gruvbox
-------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-gruvbox-light.png
      :class: tb-gallery
      :width: 264px
      :alt: gruvbox-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-gruvbox-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: gruvbox-dark theme — palette, buttons, and controls

dracula
-------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-dracula-light.png
      :class: tb-gallery
      :width: 264px
      :alt: dracula-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-dracula-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: dracula-dark theme — palette, buttons, and controls

tokyo-night
-----------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-tokyo-night-light.png
      :class: tb-gallery
      :width: 264px
      :alt: tokyo-night-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-tokyo-night-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: tokyo-night-dark theme — palette, buttons, and controls

one
---

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-one-light.png
      :class: tb-gallery
      :width: 264px
      :alt: one-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-one-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: one-dark theme — palette, buttons, and controls

everforest
----------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-everforest-light.png
      :class: tb-gallery
      :width: 264px
      :alt: everforest-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-everforest-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: everforest-dark theme — palette, buttons, and controls

vapor
-----

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-vapor-light.png
      :class: tb-gallery
      :width: 264px
      :alt: vapor-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-vapor-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: vapor-dark theme — palette, buttons, and controls

minty
-----

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-minty-light.png
      :class: tb-gallery
      :width: 264px
      :alt: minty-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-minty-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: minty-dark theme — palette, buttons, and controls

pulse
-----

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-pulse-light.png
      :class: tb-gallery
      :width: 264px
      :alt: pulse-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-pulse-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: pulse-dark theme — palette, buttons, and controls

united
------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-united-light.png
      :class: tb-gallery
      :width: 264px
      :alt: united-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-united-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: united-dark theme — palette, buttons, and controls

sandstone
---------

.. container:: tb-screenshot-row

   .. image:: /_static/examples/theming-card-sandstone-light.png
      :class: tb-gallery
      :width: 264px
      :alt: sandstone-light theme — palette, buttons, and controls

   .. image:: /_static/examples/theming-card-sandstone-dark.png
      :class: tb-gallery
      :width: 264px
      :alt: sandstone-dark theme — palette, buttons, and controls
