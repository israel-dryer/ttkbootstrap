Widgets
=======

The visual catalog. ttkbootstrap works with two kinds of widget, and the split
matters:

- **Styling ttk widgets** — the native ttk widgets ttkbootstrap themes. They
  have no ttkbootstrap Python API of their own; you use the standard
  ``tkinter.ttk`` constructor and add ``bootstyle=``. Their deep reference is
  the :doc:`Style Reference </reference/style-reference/index>`.
- **ttkbootstrap widgets** — widgets ttkbootstrap *ships* (``Meter``,
  ``Floodgauge``, ``DateEntry``, ``Tableview``, and more). These have a real
  authored API, documented in the :doc:`API Reference </reference/api/index>`.

Every catalog page follows the same shape — a one-liner, screenshots in both
themes, semantic styling first, then variants, colors, and states — so the whole
catalog reads as one system.

Styling ttk widgets
-------------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Button
      :link: button
      :link-type: doc

      A clickable action trigger — solid, outline, link, and ghost variants.

ttkbootstrap widgets
--------------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Meter
      :link: meter
      :link-type: doc

      A radial progress meter and dial.

.. toctree::
   :hidden:
   :caption: Styling ttk widgets

   button

.. toctree::
   :hidden:
   :caption: ttkbootstrap widgets

   meter
