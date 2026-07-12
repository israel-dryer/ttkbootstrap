Sizegrip
========

A **sizegrip** is the small ribbed handle in the bottom-right corner of a window
that the user drags to resize it. ``Sizegrip`` is the native ``ttk.Sizegrip``,
styled with ``bootstyle=``.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A window with the ribbed sizegrip handle in its bottom-right corner, in light
   and dark themes.

Usage
-----

Place a sizegrip in the corner of a resizable window — pack it to the bottom-right.
It wires itself to the window's resize behavior; no callback is needed:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   ttk.Label(app, text="Drag the corner to resize").pack(padx=20, pady=20)
   ttk.Sizegrip(app).pack(side=BOTTOM, anchor=SE)

   app.mainloop()

A sizegrip is a visual affordance — the window is resizable from its edges
regardless — so add one when a corner handle makes the resize obvious, typically
beside a status bar.

Color
-----

``bootstyle`` colors the grip dots from the semantic palette:

.. code-block:: python

   ttk.Sizegrip(app, bootstyle="secondary")

API & reference
---------------

``Sizegrip`` is the native ``ttk.Sizegrip`` — ttkbootstrap adds ``bootstyle=`` but
no other Python API. For its constructor see the
`tkinter.ttk.Sizegrip <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Sizegrip>`__
reference.

.. seealso::

   :doc:`Windows </user-guide/feature-guides/windows>` for window geometry and
   resizing. Want to restyle the sizegrip yourself? The
   :doc:`Style Reference › Sizegrip </reference/style-reference/sizegrip>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide
   document the hand-styling surface.
