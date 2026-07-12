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

   .. grid-item-card:: Checkbutton
      :link: checkbutton
      :link-type: doc

      An on/off control — checkbox, toggle switch, or toolbutton.

   .. grid-item-card:: Radiobutton
      :link: radiobutton
      :link-type: doc

      One option in a mutually exclusive group; segmented look too.

   .. grid-item-card:: Menubutton
      :link: menubutton
      :link-type: doc

      A button that opens a dropdown menu.

   .. grid-item-card:: OptionMenu
      :link: optionmenu
      :link-type: doc

      A dropdown that picks one value from a fixed list.

   .. grid-item-card:: Frame
      :link: frame
      :link-type: doc

      A container that groups and lays out widgets; card variants.

   .. grid-item-card:: Labelframe
      :link: labelframe
      :link-type: doc

      A frame with a titled border for a section of a form.

   .. grid-item-card:: Notebook
      :link: notebook
      :link-type: doc

      A tabbed container — one page per tab.

   .. grid-item-card:: Panedwindow
      :link: panedwindow
      :link-type: doc

      Resizable panes split by a draggable sash.

   .. grid-item-card:: Label
      :link: label
      :link-type: doc

      Read-only text or an image — captions, headings, status lines.

   .. grid-item-card:: Progressbar
      :link: progressbar
      :link-type: doc

      Determinate or indeterminate progress; striped and vertical.

   .. grid-item-card:: Scale
      :link: scale
      :link-type: doc

      A slider for choosing a number from a range.

   .. grid-item-card:: Scrollbar
      :link: scrollbar
      :link-type: doc

      Scrolls a Text, Listbox, Treeview, or Canvas.

   .. grid-item-card:: Separator
      :link: separator
      :link-type: doc

      A thin line that divides content into groups.

   .. grid-item-card:: Sizegrip
      :link: sizegrip
      :link-type: doc

      The corner handle for resizing a window.

   .. grid-item-card:: Meter
      :link: meter
      :link-type: doc

      A radial progress meter and dial.

   .. grid-item-card:: Floodgauge
      :link: floodgauge
      :link-type: doc

      A progress bar that shows its value as text across the bar.

   .. grid-item-card:: LabeledScale
      :link: labeledscale
      :link-type: doc

      A scale with a value label that tracks the handle.

   .. grid-item-card:: DateEntry
      :link: dateentry
      :link-type: doc

      A text field with a pop-up calendar for choosing a date.

   .. grid-item-card:: Treeview
      :link: treeview
      :link-type: doc

      A tree, a multi-column table, or both — rows of items.

   .. grid-item-card:: Tableview
      :link: tableview
      :link-type: doc

      A data table with sorting, search, and pagination.

   .. grid-item-card:: Toast
      :link: toast
      :link-type: doc

      A temporary notification that pops up and fades.

   .. grid-item-card:: Tooltip
      :link: tooltip
      :link-type: doc

      A help popup that appears on hover.

.. toctree::
   :hidden:

   button
   entry
   combobox
   spinbox
   checkbutton
   radiobutton
   menubutton
   optionmenu
   frame
   labelframe
   notebook
   panedwindow
   label
   progressbar
   scale
   scrollbar
   separator
   sizegrip
   meter
   floodgauge
   labeledscale
   dateentry
   treeview
   tableview
   toast
   tooltip
