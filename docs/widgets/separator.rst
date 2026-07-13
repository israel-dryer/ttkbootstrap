Separator
=========

A **separator** is a thin line that divides content into groups — between sections
of a form or items in a menu-like list. ``Separator`` is the native
``ttk.Separator``, styled with ``bootstyle=``.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   Two stacked sections divided by a horizontal separator, in light and dark
   themes.

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
otherwise it collapses to nothing.

Color
-----

``bootstyle`` colors the line from the semantic palette; the default is a subtle
border tone that suits most dividers:

.. code-block:: python

   ttk.Separator(app, orient=HORIZONTAL, bootstyle="primary")

API & reference
---------------

``Separator`` is the native ``ttk.Separator`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor see the
`tkinter.ttk.Separator <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Separator>`__
reference.

.. seealso::

   Want to restyle the separator yourself? The
   :ref:`Separator's styling options <separator-styling>` and
   its companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
