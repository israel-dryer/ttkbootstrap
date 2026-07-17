Frame
=====

A **frame** is a rectangular container that groups and lays out other widgets.
``Frame`` is the native ``ttk.Frame``, styled with ``bootstyle=``. This page covers
using it to structure a layout, padding its contents, then adding a border and a
colored background.

.. image:: /_static/examples/frame-hero-light.png
   :class: tb-screenshot-light
   :width: 316px
   :alt: A colored header frame above a plain content frame — light theme

.. image:: /_static/examples/frame-hero-dark.png
   :class: tb-screenshot-dark
   :width: 316px
   :alt: A colored header frame above a plain content frame — dark theme

Usage
-----

A frame holds other widgets: pass the frame as their ``master``, then place the
frame in its own parent. Frames are how you break a window into regions and nest
layouts — a header, a sidebar, a form — each managed independently:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   header = ttk.Frame(app, padding=10, bootstyle="primary")
   header.pack(fill=X)
   ttk.Label(header, text="Dashboard", bootstyle="inverse-primary").pack()

   content = ttk.Frame(app, padding=20)
   content.pack(fill=BOTH, expand=YES)
   ttk.Label(content, text="Body goes here").pack()

   app.mainloop()

``padding=`` insets the frame's contents so its children don't hug the edges
(one value for all sides, or ``(left, top, right, bottom)``). Which geometry
manager you use *inside* a frame is independent of the one used to place the frame
itself — see :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>`.

Adding a border
---------------

By default a frame is invisible — it takes the window background. The most common
reason to style one is to **set a region off with a border**. The ``card`` variant
draws a hairline border around the frame's contents:

.. code-block:: python

   ttk.Frame(app, padding=16, bootstyle="card")

The ``highlight`` variant is the same hairline, but drawn in the **accent color
while the frame is in the** ``focus`` **state**. A frame does not track its
children's focus on its own, so you set that state yourself — for example, to make
a card glow while an entry inside it is focused:

.. code-block:: python

   card = ttk.Frame(app, padding=16, bootstyle="highlight")
   card.pack()
   entry = ttk.Entry(card)
   entry.pack()

   entry.bind("<FocusIn>",  lambda event: card.state(["focus"]))
   entry.bind("<FocusOut>", lambda event: card.state(["!focus"]))

Prefer ``card`` and ``highlight`` over a raw ``relief=``/``borderwidth=`` border:
plain ttk relief is theme-dependent and needs a non-zero ``borderwidth`` to show
at all, while the ``card`` hairline matches the rest of the theme.

Colored background
------------------

Less often, give a frame a ``bootstyle`` color to make it a filled band — a
colored header or footer. Put ``inverse-<color>`` labels inside so their text
reads against the fill (as the header in `Usage`_ does):

.. code-block:: python

   ttk.Frame(app, padding=10, bootstyle="secondary")

Fixing a frame's size
---------------------

A frame sizes itself to fit its children, so ``width=`` and ``height=`` are
**ignored** the moment you pack or grid anything into it. To make a frame hold a
fixed size regardless of its contents, turn **geometry propagation** off:

.. code-block:: python

   panel = ttk.Frame(app, width=200, height=120)
   panel.pack()
   panel.pack_propagate(False)      # keep 200x120 even after adding children

Use ``grid_propagate(False)`` instead when the frame's children are gridded. This
is the usual answer to "why won't my frame stay the size I set?"

Reference
---------

``Frame`` is the native ``ttk.Frame``; ttkbootstrap adds only the ``bootstyle``
keyword.

- :doc:`Frame API reference </reference/api/frame>` — every option and method.
- :ref:`Frame styling options <frame-styling>` — restyle it yourself, with the
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Labelframe <labelframe>` — a frame with a titled border.
   - :doc:`Notebook <notebook>` — a tabbed container.
   - :doc:`Panedwindow <panedwindow>` — a split, resizable container.
   - :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>` — laying out the contents.
