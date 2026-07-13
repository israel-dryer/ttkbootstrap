API Reference
=============

The complete reference for the widget API — the native **ttk** widgets
ttkbootstrap themes, the widgets it **ships**, and the classic **tk** widgets it
themes. Each page documents a widget's options, methods, and — for ttk widgets —
its styling. Python's standard library documents these widgets incompletely —
or, for widgets like ``Text`` and ``Canvas``, not at all — so this reference is
maintained here.

Native ttk widgets
------------------

The standard ``ttk`` widgets, themed by ttkbootstrap.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Button
      :link: button
      :link-type: doc

      A clickable action trigger.

   .. grid-item-card:: Checkbutton
      :link: checkbutton
      :link-type: doc

      A labeled on/off toggle.

   .. grid-item-card:: Radiobutton
      :link: radiobutton
      :link-type: doc

      A one-of-many selector.

   .. grid-item-card:: Combobox
      :link: combobox
      :link-type: doc

      A drop-down with an editable field.

   .. grid-item-card:: Entry
      :link: entry
      :link-type: doc

      A single-line text field.

   .. grid-item-card:: Spinbox
      :link: spinbox
      :link-type: doc

      A field with up/down value steppers.

   .. grid-item-card:: Menubutton
      :link: menubutton
      :link-type: doc

      A button that pops up a menu.

   .. grid-item-card:: OptionMenu
      :link: optionmenu
      :link-type: doc

      A menu of options bound to a variable.

   .. grid-item-card:: Label
      :link: label
      :link-type: doc

      Text, an image, or both.

   .. grid-item-card:: Frame
      :link: frame
      :link-type: doc

      A container for layout.

   .. grid-item-card:: Labelframe
      :link: labelframe
      :link-type: doc

      A frame with a caption.

   .. grid-item-card:: Notebook
      :link: notebook
      :link-type: doc

      A tabbed container.

   .. grid-item-card:: Panedwindow
      :link: panedwindow
      :link-type: doc

      Resizable split panes.

   .. grid-item-card:: Progressbar
      :link: progressbar
      :link-type: doc

      A determinate or indeterminate progress bar.

   .. grid-item-card:: Scale
      :link: scale
      :link-type: doc

      A slider for a numeric range.

   .. grid-item-card:: Scrollbar
      :link: scrollbar
      :link-type: doc

      Drives another widget's view.

   .. grid-item-card:: Separator
      :link: separator
      :link-type: doc

      A dividing line.

   .. grid-item-card:: Sizegrip
      :link: sizegrip
      :link-type: doc

      A window resize handle.

   .. grid-item-card:: Treeview
      :link: treeview
      :link-type: doc

      A tree/table of items.

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
      :link: tklabelframe
      :link-type: doc

      The classic ``tk.LabelFrame`` — a frame with a caption.

.. toctree::
   :hidden:
   :maxdepth: 1

   button
   checkbutton
   radiobutton
   combobox
   entry
   spinbox
   menubutton
   optionmenu
   label
   frame
   labelframe
   notebook
   panedwindow
   progressbar
   scale
   scrollbar
   separator
   sizegrip
   treeview
   meter
   floodgauge
   labeledscale
   dateentry
   tableview
   toastnotification
   tooltip
   text
   canvas
   listbox
   menu
   tk
   tkframe
   tklabel
   tklabelframe
