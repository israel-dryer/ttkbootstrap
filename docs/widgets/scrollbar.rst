Scrollbar
=========

A **scrollbar** scrolls a widget whose contents are larger than its view — a
``Text``, a ``Listbox``, a ``Treeview``, or a ``Canvas``. ``Scrollbar`` is the
native ``ttk.Scrollbar``, styled with
``bootstyle=``. This page covers wiring it to a widget, the orientation, then the
``bootstyle`` color and variants.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A scrolled text box with a vertical scrollbar in light and dark themes.

Wiring it up
------------

A scrollbar and its widget are connected **both ways**: the scrollbar tells the
widget where to scroll (``command``), and the widget tells the scrollbar where it
is so the thumb tracks (``set``). Wire both:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   text = ttk.Text(app, height=8, width=40)
   scroll = ttk.Scrollbar(app, orient=VERTICAL, command=text.yview)
   text.configure(yscrollcommand=scroll.set)

   text.pack(side=LEFT, fill=BOTH, expand=YES)
   scroll.pack(side=RIGHT, fill=Y)

   app.mainloop()

- ``command=text.yview`` — the scrollbar drives the text's vertical view.
- ``yscrollcommand=scroll.set`` — the text reports its position back so the thumb
  follows. (Use ``xview`` / ``xscrollcommand`` with a ``HORIZONTAL`` scrollbar.)

.. tip::

   For a text area or a frame of widgets, ttkbootstrap's
   :doc:`ScrolledText / ScrolledFrame </user-guide/how-to/scrollable>` do this
   wiring for you — reach for a bare ``Scrollbar`` when you attach one to a
   ``Listbox``, ``Canvas``, or ``Treeview`` yourself.

Color and variants
------------------

``bootstyle`` colors the thumb from the semantic palette. A ``round`` variant
gives it rounded ends, and ``thin`` makes it a slim track for dense UIs:

.. code-block:: python

   ttk.Scrollbar(app, orient=VERTICAL, command=text.yview, bootstyle="primary round")
   ttk.Scrollbar(app, orient=VERTICAL, command=text.yview, bootstyle="secondary thin")

API & reference
---------------

``Scrollbar`` is the native ``ttk.Scrollbar`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor and options (``orient``, ``command``)
and the ``set`` method, see the
`tkinter.ttk.Scrollbar <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Scrollbar>`__
reference.

.. seealso::

   :doc:`Scroll long content </user-guide/how-to/scrollable>` for the ready-made
   ``ScrolledText`` / ``ScrolledFrame``. Want to restyle the scrollbar yourself?
   The :ref:`Scrollbar's styling options <scrollbar-styling>`
   and its companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
