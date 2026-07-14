Capabilities
============

The methods every widget inherits, grouped by area — each mirroring the
corresponding Tcl/Tk manual page so the two references line up. A capability page
is a **spec** (signatures, parameters, return types); the Foundations guides
teach the same areas by building. The geometry managers that size and place a
widget (pack, grid, place, stacking order) have their own
:doc:`Geometry </reference/geometry/index>` section.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Configuration
      :link: configuration
      :link-type: doc

      Read and write a widget's options — ``configure``, ``cget``, ``keys``.

   .. grid-item-card:: Bind
      :link: bind
      :link-type: doc

      Attach callbacks to events — ``bind``, ``bind_all``, ``bindtags``.

   .. grid-item-card:: Focus
      :link: focus
      :link-type: doc

      Query and move the keyboard focus, and traversal order.

   .. grid-item-card:: Grab
      :link: grab
      :link-type: doc

      Route input to one widget for a modal dialog.

   .. grid-item-card:: After
      :link: after
      :link-type: doc

      Schedule callbacks on the event loop — ``after``, ``after_idle``.

   .. grid-item-card:: Lifecycle
      :link: lifecycle
      :link-type: doc

      Refresh, wait, and destroy — ``update``, ``wait_*``, ``destroy``.

   .. grid-item-card:: Clipboard
      :link: clipboard
      :link-type: doc

      Read and write the system clipboard.

   .. grid-item-card:: Selection
      :link: selection
      :link-type: doc

      Read, clear, and own the current selection.

   .. grid-item-card:: Widget & screen info
      :link: /reference/winfo
      :link-type: doc

      The ``winfo_*`` methods — class, size, position, and screen dimensions.

.. toctree::
   :hidden:

   configuration
   bind
   focus
   grab
   after
   lifecycle
   clipboard
   selection
   /reference/winfo
