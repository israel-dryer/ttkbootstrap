API Reference
=============

The complete reference for the widget API — the widgets ttkbootstrap **ships**,
and the classic **tk** widgets it themes. Python's standard library documents
the tk widgets incompletely — or, for widgets like ``Text`` and ``Canvas``, not
at all — so this reference is maintained here. A widget's styling surface lives
separately in the :doc:`Style Reference </reference/style-reference/index>`.

.. note::

   Reference pages for the native **ttk** widgets (``Button``, ``Entry``,
   ``Notebook``, …) are still being added.

Shipped widgets
---------------

The widgets ttkbootstrap adds on top of ttk.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Meter
      :link: meter
      :link-type: doc

      A radial progress/dial widget.

   .. grid-item-card:: Floodgauge
      :link: floodgauge
      :link-type: doc

      A progress bar with text drawn over the fill.

   .. grid-item-card:: LabeledScale
      :link: labeledscale
      :link-type: doc

      A scale paired with a value label.

   .. grid-item-card:: DateEntry
      :link: dateentry
      :link-type: doc

      An entry with a calendar-popup date picker.

   .. grid-item-card:: Tableview
      :link: tableview
      :link-type: doc

      A data table with sorting, filtering, and paging.

   .. grid-item-card:: ToastNotification
      :link: toastnotification
      :link-type: doc

      A temporary popup alert.

   .. grid-item-card:: ToolTip
      :link: tooltip
      :link-type: doc

      A hover popup attached to a widget.

Classic tk widgets
------------------

The ``tkinter`` widgets ttkbootstrap themes.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Text
      :link: text
      :link-type: doc

      The tk ``Text`` widget — its full options and methods.

   .. grid-item-card:: Canvas
      :link: canvas
      :link-type: doc

      The tk ``Canvas`` drawing surface — items, tags, and their methods.

   .. grid-item-card:: Listbox
      :link: listbox
      :link-type: doc

      The tk ``Listbox`` — a list of selectable lines.

   .. grid-item-card:: Menu
      :link: menu
      :link-type: doc

      The tk ``Menu`` — menu bars, submenus, and context menus.

   .. grid-item-card:: Tk
      :link: tk
      :link-type: doc

      The classic ``tk.Tk`` root window and its window-manager surface.

   .. grid-item-card:: TkFrame
      :link: tkframe
      :link-type: doc

      The classic ``tk.Frame`` container.

   .. grid-item-card:: TkLabel
      :link: tklabel
      :link-type: doc

      The classic ``tk.Label`` — text, image, or both.

   .. grid-item-card:: LabelFrame
      :link: labelframe
      :link-type: doc

      The classic ``tk.LabelFrame`` — a frame with a caption.

.. toctree::
   :hidden:
   :maxdepth: 1

   meter
   floodgauge
   labeledscale
   dateentry
   tableview
   toastnotification
   tooltip
   button
   text
   canvas
   listbox
   menu
   tk
   tkframe
   tklabel
   labelframe