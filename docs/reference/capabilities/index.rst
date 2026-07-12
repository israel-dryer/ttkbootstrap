Capabilities
============

The methods every widget inherits, grouped by area — each mirroring the
corresponding Tcl/Tk manual page so the two references line up. A capability page
is a **spec** (signatures, parameters, return types); the Foundations guides
teach the same areas by building.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Configuration
      :link: configuration
      :link-type: doc

      Read and write a widget's options — ``configure``, ``cget``, ``keys``.

   .. grid-item-card:: Geometry
      :link: geometry
      :link-type: doc

      Place a widget with ``pack``, ``grid``, or ``place``; stacking order.

   .. grid-item-card:: Focus
      :link: focus
      :link-type: doc

      Query and move the keyboard focus, and traversal order.

   .. grid-item-card:: Grab
      :link: grab
      :link-type: doc

      Route input to one widget for a modal dialog.

   .. grid-item-card:: Timers
      :link: timers
      :link-type: doc

      Schedule callbacks on the event loop — ``after``, ``after_idle``.

   .. grid-item-card:: Lifecycle
      :link: lifecycle
      :link-type: doc

      Refresh, wait, and destroy — ``update``, ``wait_*``, ``destroy``.

   .. grid-item-card:: Clipboard & selection
      :link: clipboard
      :link-type: doc

      Read and write the system clipboard and the selection.

   .. grid-item-card:: Events (bind)
      :link: /reference/events/index
      :link-type: doc

      Attach behavior to input — event types, modifiers, and the event object.

   .. grid-item-card:: Widget & screen info
      :link: /reference/winfo
      :link-type: doc

      The ``winfo_*`` methods — class, size, position, and screen dimensions.

   .. grid-item-card:: Cursors
      :link: /reference/cursors
      :link-type: doc

      The mouse-pointer names the ``cursor`` option accepts.

.. toctree::
   :hidden:

   configuration
   geometry
   focus
   grab
   timers
   lifecycle
   clipboard
   /reference/events/index
   /reference/winfo
   /reference/cursors
