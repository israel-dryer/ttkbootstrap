Reference
=========

The lookup layer:

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Widgets
      :link: api/index
      :link-type: doc

      Every widget's options, methods, and — for ttk widgets — styling. The
      native ttk widgets, the ones ttkbootstrap ships, and the classic tk
      widgets, grouped by what they do.

   .. grid-item-card:: Windows
      :link: windows/index
      :link-type: doc

      The application window classes — ``App`` (the root) and ``Toplevel`` — and
      their constructor, theme, and window-management surface.

   .. grid-item-card:: Capabilities
      :link: capabilities/index
      :link-type: doc

      The methods every widget inherits, grouped by area — configuration,
      pack/grid/place, focus, grab, after, clipboard, and ``winfo`` — each
      mirroring its Tcl/Tk manual page.

   .. grid-item-card:: Events
      :link: events/index
      :link-type: doc

      The tkinter event system — event types, modifiers, key symbols, the event
      object, and the built-in ``<<virtual>>`` events.

   .. grid-item-card:: Cursors
      :link: cursors
      :link-type: doc

      The mouse-pointer names the ``cursor`` option accepts — the common set,
      the full portable list, and the platform-specific pointers.

.. toctree::
   :hidden:

   api/index
   windows/index
   capabilities/index
   events/index
   cursors
