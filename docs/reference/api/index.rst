API Reference
=============

The complete reference for the widget API. The widgets ttkbootstrap **ships**
are generated from their source docstrings; the **tk and native ttk widgets**
ttkbootstrap themes get a hand-maintained reference here too, because Python's
standard library documents them incompletely (or, for the classic tk widgets,
not at all). A widget's styling surface lives separately in the
:doc:`Style Reference </reference/style-reference/index>`.

.. note::

   This section is being built out. The shipped-widget page proves the autodoc
   pattern; the per-widget reference pages (tk and native ttk) are being added
   one at a time, starting with ``Text``.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Widgets
      :link: widgets
      :link-type: doc

      The widgets ttkbootstrap ships — ``Meter``, ``Floodgauge``,
      ``DateEntry``, ``Tableview``, and more.

   .. grid-item-card:: Text
      :link: text
      :link-type: doc

      The tk ``Text`` widget — its full options and methods.

   .. grid-item-card:: Canvas
      :link: canvas
      :link-type: doc

      The tk ``Canvas`` drawing surface — items, tags, and their methods.

.. toctree::
   :hidden:
   :maxdepth: 1

   widgets
   text
   canvas
