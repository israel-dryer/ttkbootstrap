Frame
=====

A **frame** is a rectangular container that groups and lays out other widgets.
``Frame`` is the native ``ttk.Frame``, styled with ``bootstyle=``. This page covers
using it to structure a layout, padding its contents, then adding a border and a
colored background.

.. image:: /_static/examples/frame-hero-light.png
   :class: tb-screenshot-light tb-window-screenshot
   :width: 318px
   :alt: A colored header frame above a plain content frame — light theme

.. image:: /_static/examples/frame-hero-dark.png
   :class: tb-screenshot-dark tb-window-screenshot
   :width: 318px
   :alt: A colored header frame above a plain content frame — dark theme

Usage
-----

A frame holds other widgets: pass the frame as their ``master``, then place the
frame in its own parent. Frames are how you break a window into regions and nest
layouts — a header, a sidebar, a form — each managed independently.

A frame's ``bootstyle`` controls three independent things: a **border**
(``bordered``), a **surface** to fill it (``@card`` / ``@chrome``), and a bold
**color** fill (``primary`` …). They compose — ``"bordered @card"`` is a bordered
panel on the card surface.

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   header = ttk.Frame(app, padding=10, bootstyle="primary")
   header.pack(fill=X)
   ttk.Label(header, text="Dashboard", bootstyle="@primary").pack()

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
reason to style one is to **set a region off with a border**. The ``bordered``
variant draws a hairline border around the frame's contents:

.. code-block:: python

   ttk.Frame(app, padding=16, bootstyle="bordered")

The border color is derived from the surface the frame is filled with, so it stays
a visible hairline on the window, a card, or a chrome panel alike.

The ``highlight`` variant is the same hairline, but drawn in the **accent color
while the frame is in the** ``focus`` **state**. A frame does not track its
children's focus on its own, so you set that state yourself — for example, to make
a panel glow while an entry inside it is focused:

.. code-block:: python

   panel = ttk.Frame(app, padding=16, bootstyle="highlight")
   panel.pack()
   entry = ttk.Entry(panel)
   entry.pack()

   entry.bind("<FocusIn>",  lambda event: panel.state(["focus"]))
   entry.bind("<FocusOut>", lambda event: panel.state(["!focus"]))

Prefer ``bordered`` and ``highlight`` over a raw ``relief=``/``borderwidth=``
border: plain ttk relief is theme-dependent and needs a non-zero ``borderwidth``
to show at all, while the ``bordered`` hairline matches the rest of the theme.

Filling with a surface
----------------------

Give a frame an ``@`` **surface** token to fill it with a neutral panel color on
the theme's elevation scale — ``@chrome`` (recessive framing: a toolbar or status
bar) or ``@card`` (a raised panel: a sidebar or grouped region). Unlike a bold
color, a surface reads as a subtle, theme-matched region and gives the widgets
inside it a background to blend onto:

.. code-block:: python

   sidebar = ttk.Frame(app, bootstyle="@card", padding=12)   # the frame IS the card surface
   sidebar.pack(side="left", fill="y")
   ttk.Button(sidebar, text="Home", bootstyle="@card link").pack(fill="x")

Put the same ``@card`` token on the controls inside so a ghost, outline, or link
button blends onto the surface instead of painting a wrong-colored box. See
:doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>` for the
full surface grammar. A surface composes with ``bordered`` — ``"bordered @card"``
is a card panel with a hairline edge.

Colored background
------------------

Less often, give a frame a ``bootstyle`` color to make it a bold filled band — a
colored header or footer. Put ``@<color>`` labels inside so their text reads
against the fill (as the header in `Usage`_ does):

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
