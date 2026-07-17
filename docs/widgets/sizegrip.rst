Sizegrip
========

A **sizegrip** is the small ribbed handle in the bottom-right corner of a window
that the user drags to resize it. ``Sizegrip`` is the native ``ttk.Sizegrip``,
styled with ``bootstyle=``.

.. image:: /_static/examples/sizegrip-hero-light.png
   :class: tb-screenshot-light
   :width: 296px
   :alt: A window with the ribbed sizegrip handle in its bottom-right corner — light theme

.. image:: /_static/examples/sizegrip-hero-dark.png
   :class: tb-screenshot-dark
   :width: 296px
   :alt: A window with the ribbed sizegrip handle in its bottom-right corner — dark theme

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

A sizegrip only resizes from the **south-east**, which is why it belongs at the
bottom-right with ``anchor=SE``. Two caveats:

- It **won't resize a window whose position was set relative to the right or
  bottom edge** — a ``geometry("WxH-x-y")`` with minus signs. Windows placed with
  ``+x+y`` work normally.
- On macOS the window already draws its own resize corner, so a ``Sizegrip`` there
  is redundant (harmless, but the native grip sits on top).

Color
-----

``bootstyle`` colors the grip dots from the semantic palette:

.. code-block:: python

   ttk.Sizegrip(app, bootstyle="secondary")

Reference
---------

``Sizegrip`` is the native ``ttk.Sizegrip``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Sizegrip API reference </reference/api/sizegrip>` — every option and
  method.
- :ref:`Sizegrip styling options <sizegrip-styling>` — restyle it yourself, with
  the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Windows </user-guide/feature-guides/windows>` — window geometry and resizing.
