Widgets
=======

The visual catalog — a usage guide for each widget: set ``bootstyle``, choose a
variant and color, and handle states. The recipe is the same whether the widget
is a native ttk widget ttkbootstrap themes or one ttkbootstrap ships, so they
live in one list. Every page follows the same shape — a one-liner, screenshots
in both themes, semantic styling, then variants, colors, and states — and ends
by linking to the widget's API (python.org's ``tkinter.ttk`` for a native
widget, the :doc:`API Reference </reference/api/index>` for a ttkbootstrap one)
and to the deep :doc:`Style Reference </reference/style-reference/index>`.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Button
      :link: button
      :link-type: doc

      A clickable action trigger — solid, outline, link, and ghost variants.

   .. grid-item-card:: Entry
      :link: entry
      :link-type: doc

      A single-line text field — binding, masking, and validation.

   .. grid-item-card:: Combobox
      :link: combobox
      :link-type: doc

      A text field with a dropdown of choices — pick-only or editable.

   .. grid-item-card:: Spinbox
      :link: spinbox
      :link-type: doc

      An entry with up/down arrows for stepping a range or list.

   .. grid-item-card:: Meter
      :link: meter
      :link-type: doc

      A radial progress meter and dial.

.. toctree::
   :hidden:

   button
   entry
   combobox
   spinbox
   meter
