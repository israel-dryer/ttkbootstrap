Windows
=======

The application window classes. ``App`` is the root — one per process, paired
with the style engine — and ``Toplevel`` is every window after it. Both wrap
their tkinter counterparts and fold the theme, icon, size, position, and window
constraints into one constructor. The :doc:`Windows guide
</user-guide/feature-guides/windows>` teaches them by building; these pages are
the lookup.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: App
      :link: app
      :link-type: doc

      The application root window (also exported as ``Window``).

   .. grid-item-card:: Toplevel
      :link: toplevel
      :link-type: doc

      A secondary window — dialogs, pickers, tool windows.

.. toctree::
   :hidden:

   app
   toplevel
