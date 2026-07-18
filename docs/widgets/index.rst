Widgets
=======

The visual catalog — a usage guide for each widget: set ``bootstyle``, choose a
variant and color, and handle states. The recipe is the same whether the widget
is a native ttk widget ttkbootstrap themes or one ttkbootstrap ships, so they
live in one list, grouped by purpose. Every page follows the same shape — a
one-liner, screenshots in both themes, semantic styling, then variants, colors,
and states — and ends by linking to the widget's API (python.org's
``tkinter.ttk`` for a native widget, the :doc:`widget reference
</reference/api/index>` for a ttkbootstrap one), where each page also documents
the widget's hand-styling surface.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: :octicon:`zap;1.5em;sd-mr-1` Actions

      Buttons that trigger commands.

      :doc:`button`

   .. grid-item-card:: :octicon:`pencil;1.5em;sd-mr-1` Inputs

      Free-text, numeric, and date entry, plus sliders — single- and multi-line.

      :doc:`entry` · :doc:`text` · :doc:`spinbox` · :doc:`dateentry` ·
      :doc:`scale` · :doc:`labeledscale`

   .. grid-item-card:: :octicon:`check-circle;1.5em;sd-mr-1` Selection

      Choose from a set of options — toggles, radios, and dropdowns.

      :doc:`checkbutton` · :doc:`radiobutton` · :doc:`combobox` ·
      :doc:`optionmenu` · :doc:`menubutton`

   .. grid-item-card:: :octicon:`table;1.5em;sd-mr-1` Data display

      Show values and records — labels, progress, meters, tables, and trees.

      :doc:`label` · :doc:`progressbar` · :doc:`meter` · :doc:`floodgauge` ·
      :doc:`treeview` · :doc:`tableview`

   .. grid-item-card:: :octicon:`columns;1.5em;sd-mr-1` Containers & layout

      Group and arrange widgets — frames, tabs, panes, and scrolling.

      :doc:`frame` · :doc:`labelframe` · :doc:`notebook` · :doc:`panedwindow` ·
      :doc:`scrolled` · :doc:`scrollbar` · :doc:`separator` · :doc:`sizegrip`

   .. grid-item-card:: :octicon:`paintbrush;1.5em;sd-mr-1` Drawing

      A free-form surface for shapes, text, images, and embedded widgets.

      :doc:`canvas`

   .. grid-item-card:: :octicon:`comment;1.5em;sd-mr-1` Overlays

      Transient surfaces that float above the content — tooltips and toasts.

      :doc:`tooltip` · :doc:`toast`

.. toctree::
   :caption: Actions
   :hidden:

   button

.. toctree::
   :caption: Inputs
   :hidden:

   entry
   text
   spinbox
   dateentry
   scale
   labeledscale

.. toctree::
   :caption: Selection
   :hidden:

   checkbutton
   radiobutton
   combobox
   optionmenu
   menubutton

.. toctree::
   :caption: Data display
   :hidden:

   label
   progressbar
   meter
   floodgauge
   treeview
   tableview

.. toctree::
   :caption: Containers & layout
   :hidden:

   frame
   labelframe
   notebook
   panedwindow
   scrolled
   scrollbar
   separator
   sizegrip

.. toctree::
   :caption: Drawing
   :hidden:

   canvas

.. toctree::
   :caption: Overlays
   :hidden:

   tooltip
   toast
