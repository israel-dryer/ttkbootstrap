Labelframe
==========

A **labelframe** is a frame with a titled border — it groups related widgets under
a caption. ``Labelframe`` is the native ``ttk.Labelframe``, styled with
``bootstyle=``. This page covers grouping widgets under a label, then the
``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A "Contact" labelframe grouping a couple of fields, in light and dark themes.

Usage
-----

Set the caption with ``text=`` and place the grouped widgets inside the labelframe
as their ``master``. It is the natural container for a **section of a form**:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   contact = ttk.Labelframe(app, text="Contact", padding=12)
   contact.pack(fill=X, padx=10, pady=10)

   ttk.Label(contact, text="Name").pack(anchor=W)
   ttk.Entry(contact).pack(fill=X)
   ttk.Label(contact, text="Email").pack(anchor=W)
   ttk.Entry(contact).pack(fill=X)

   app.mainloop()

Like a plain :doc:`Frame <frame>`, use ``padding=`` to inset the contents; arrange
the children with any geometry manager.

Positioning and replacing the caption
-------------------------------------

``labelanchor=`` moves the caption around the border — ``"nw"`` (top-left),
``"n"`` (top-centre), ``"w"`` (down the left edge), through the twelve compass
positions:

.. code-block:: python

   ttk.Labelframe(app, text="Contact", labelanchor="nw", padding=12)

For a caption that's more than plain text, pass a **widget** as the label with
``labelwidget=`` — a label with an icon, or a checkbutton that enables the whole
group. It replaces ``text=``, and must be a child of the labelframe or one of its
ancestors:

.. code-block:: python

   enabled = ttk.Checkbutton(app, text="Shipping address", bootstyle="round-toggle")
   section = ttk.Labelframe(app, labelwidget=enabled, padding=12)
   section.pack(fill=X, padx=10, pady=10)

``underline=`` underlines one character of a text caption as a keyboard mnemonic.

Color
-----

``bootstyle`` colors the border and the caption text from the semantic palette —
use it to tie a section to a color, or to signal an important or dangerous group:

.. code-block:: python

   ttk.Labelframe(app, text="Danger zone", padding=12, bootstyle="danger")

API & reference
---------------

``Labelframe`` is the native ``ttk.Labelframe`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor and options (``text``, ``padding``,
``labelanchor``, ``labelwidget``, ``width``, ``height``, …) see the
`tkinter.ttk.Labelframe <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Labelframe>`__
reference.

.. seealso::

   :doc:`Frame <frame>` for a plain container, and
   :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>` for laying
   out the widgets inside. Want to restyle the labelframe yourself? The
   :ref:`Labelframe's styling options <labelframe-styling>` and
   its companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
