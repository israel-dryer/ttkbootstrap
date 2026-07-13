Widgets
=======

The complete reference for every widget — its options, methods, and (for ttk
widgets) styling. It covers the native **ttk** widgets ttkbootstrap themes, the
widgets it **ships**, and the classic **tk** widgets it themes; each page names
which it is. Python's standard library documents these incompletely — or, for
widgets like ``Text`` and ``Canvas``, not at all — so this reference is
maintained here. Pages are grouped by what the widget does.

Buttons & menus
---------------

Trigger actions and pop up menus.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Button
      :link: button
      :link-type: doc

      A clickable action trigger.

   .. grid-item-card:: Menubutton
      :link: menubutton
      :link-type: doc

      A button that pops up a menu.

   .. grid-item-card:: OptionMenu
      :link: optionmenu
      :link-type: doc

      A menu of options bound to a variable.

   .. grid-item-card:: Menu
      :link: menu
      :link-type: doc

      The classic ``tk.Menu`` — menu bars, submenus, and context menus.

Text & entry
------------

Type and edit text and values.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Entry
      :link: entry
      :link-type: doc

      A single-line text field.

   .. grid-item-card:: Spinbox
      :link: spinbox
      :link-type: doc

      A field with up/down value steppers.

   .. grid-item-card:: Combobox
      :link: combobox
      :link-type: doc

      A drop-down with an editable field.

   .. grid-item-card:: DateEntry
      :link: dateentry
      :link-type: doc

      An entry with a calendar-popup date picker.

   .. grid-item-card:: Text
      :link: text
      :link-type: doc

      The classic ``tk.Text`` widget — its full options and methods.

Selection & toggles
-------------------

Pick from options and flip state.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Checkbutton
      :link: checkbutton
      :link-type: doc

      A labeled on/off toggle.

   .. grid-item-card:: Radiobutton
      :link: radiobutton
      :link-type: doc

      A one-of-many selector.

   .. grid-item-card:: Listbox
      :link: listbox
      :link-type: doc

      The classic ``tk.Listbox`` — a list of selectable lines.

Range & progress
----------------

Show or set a value along a range.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Scale
      :link: scale
      :link-type: doc

      A slider for a numeric range.

   .. grid-item-card:: LabeledScale
      :link: labeledscale
      :link-type: doc

      A scale paired with a value label.

   .. grid-item-card:: Progressbar
      :link: progressbar
      :link-type: doc

      A determinate or indeterminate progress bar.

   .. grid-item-card:: Meter
      :link: meter
      :link-type: doc

      A radial progress/dial widget.

   .. grid-item-card:: Floodgauge
      :link: floodgauge
      :link-type: doc

      A progress bar with text drawn over the fill.

Data views
----------

Display rows and hierarchies of data.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Treeview
      :link: treeview
      :link-type: doc

      A tree/table of items.

   .. grid-item-card:: Tableview
      :link: tableview
      :link-type: doc

      A data table with sorting, filtering, and paging.

Layout & containers
-------------------

Structure the window and hold other widgets.

.. grid:: 1 2 2 2
   :gutter: 3

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

   .. grid-item-card:: Tk
      :link: tk
      :link-type: doc

      The classic ``tk.Tk`` root window and its window-manager surface.

   .. grid-item-card:: TkFrame
      :link: tkframe
      :link-type: doc

      The classic ``tk.Frame`` container.

   .. grid-item-card:: LabelFrame
      :link: tklabelframe
      :link-type: doc

      The classic ``tk.LabelFrame`` — a frame with a caption.

Display & drawing
-----------------

Show text, images, and custom graphics.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Label
      :link: label
      :link-type: doc

      Text, an image, or both.

   .. grid-item-card:: TkLabel
      :link: tklabel
      :link-type: doc

      The classic ``tk.Label`` — text, image, or both.

   .. grid-item-card:: Canvas
      :link: canvas
      :link-type: doc

      The classic ``tk.Canvas`` drawing surface — items, tags, and their methods.

Overlays
--------

Transient popups layered over the UI.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: ToastNotification
      :link: toastnotification
      :link-type: doc

      A temporary popup alert.

   .. grid-item-card:: ToolTip
      :link: tooltip
      :link-type: doc

      A hover popup attached to a widget.

.. toctree::
   :hidden:
   :maxdepth: 1

   button
   menubutton
   optionmenu
   menu
   entry
   spinbox
   combobox
   dateentry
   text
   checkbutton
   radiobutton
   listbox
   scale
   labeledscale
   progressbar
   meter
   floodgauge
   treeview
   tableview
   frame
   labelframe
   notebook
   panedwindow
   scrollbar
   separator
   sizegrip
   tk
   tkframe
   tklabelframe
   label
   tklabel
   canvas
   toastnotification
   tooltip
