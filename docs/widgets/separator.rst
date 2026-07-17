Separator
=========

A **separator** is a thin line that divides content into groups — between sections
of a form or items in a menu-like list. ``Separator`` is the native
``ttk.Separator``, styled with ``bootstyle=``.

.. image:: /_static/examples/separator-hero-light.png
   :class: tb-screenshot-light
   :width: 276px
   :alt: Two stacked sections divided by a horizontal separator — light theme

.. image:: /_static/examples/separator-hero-dark.png
   :class: tb-screenshot-dark
   :width: 276px
   :alt: Two stacked sections divided by a horizontal separator — dark theme

Usage
-----

Set ``orient=`` to ``HORIZONTAL`` (a line across, to divide stacked content) or
``VERTICAL`` (a line down, to divide side-by-side content), and let it fill across
its space:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   ttk.Label(app, text="Section one").pack()
   ttk.Separator(app, orient=HORIZONTAL).pack(fill=X, pady=8)
   ttk.Label(app, text="Section two").pack()

   app.mainloop()

A horizontal separator needs ``fill=X`` (a vertical one ``fill=Y``) to stretch —
otherwise it collapses to nothing. ``orient=`` defaults to ``horizontal``, and a
separator is purely decorative — it takes no focus and has no methods beyond
styling.

Color
-----

``bootstyle`` colors the line from the semantic palette; the default is a subtle
border tone that suits most dividers:

.. code-block:: python

   ttk.Separator(app, orient=HORIZONTAL, bootstyle="primary")

Reference
---------

``Separator`` is the native ``ttk.Separator``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Separator API reference </reference/api/separator>` — every option and
  method.
- :ref:`Separator styling options <separator-styling>` — restyle it yourself, with
  the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.
