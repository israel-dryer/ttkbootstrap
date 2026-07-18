Scrollbar
=========

A **scrollbar** scrolls a widget whose contents are larger than its view — a
``Text``, a ``Listbox``, a ``Treeview``, or a ``Canvas``. ``Scrollbar`` is the
native ``ttk.Scrollbar``, styled with
``bootstyle=``. This page covers wiring it to a widget, the orientation, then the
``bootstyle`` color and variants.

.. image:: /_static/examples/scrollbar-hero-light.png
   :class: tb-screenshot-light
   :width: 276px
   :alt: A scrolled text box with a vertical scrollbar — light theme

.. image:: /_static/examples/scrollbar-hero-dark.png
   :class: tb-screenshot-dark
   :width: 276px
   :alt: A scrolled text box with a vertical scrollbar — dark theme

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

How it talks to the widget
--------------------------

The two sides speak in **fractions** from ``0.0`` (top / left of the content) to
``1.0`` (the end). The widget calls ``set(first, last)`` with the visible slice,
and ``scroll.get()`` reads that ``(first, last)`` pair back. When the whole
content fits, the widget sends ``set(0.0, 1.0)`` and the scrollbar **disables
itself** — the thumb fills the track and greys out. That's expected, not a dead
scrollbar; it re-enables once there's something to scroll.

Wiring a scrollbar to a view Tk doesn't scroll for you (a ``Canvas`` or a custom
widget) means handling the ``command`` calls yourself — they arrive as
``("moveto", fraction)`` or ``("scroll", number, "units" | "pages")``.

Color and variants
------------------

``bootstyle`` colors the thumb from the semantic palette. A ``round`` variant
gives it rounded ends, and ``thin`` makes it a slim track for dense UIs:

.. code-block:: python

   ttk.Scrollbar(app, orient=VERTICAL, command=text.yview, bootstyle="primary round")
   ttk.Scrollbar(app, orient=VERTICAL, command=text.yview, bootstyle="secondary thin")

Reference
---------

``Scrollbar`` is the native ``ttk.Scrollbar``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Scrollbar API reference </reference/api/scrollbar>` — every option and
  method.
- :ref:`Scrollbar styling options <scrollbar-styling>` — restyle it yourself, with
  the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Scroll long content </user-guide/how-to/scrollable>` — the ready-made ``ScrolledText`` / ``ScrolledFrame``.
