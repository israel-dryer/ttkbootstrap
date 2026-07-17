Panedwindow
===========

A **panedwindow** holds two or more panes separated by a draggable **sash**, so
the user can resize them against each other — a sidebar next to content, an editor
above a console. ``Panedwindow`` is the native ``ttk.Panedwindow``, styled with
``bootstyle=``. This page covers adding panes, controlling how they share space,
then the ``bootstyle`` color.

.. image:: /_static/examples/panedwindow-hero-light.png
   :class: tb-screenshot-light
   :width: 356px
   :alt: A narrow sidebar and a wide content pane with the sash between them — light theme

.. image:: /_static/examples/panedwindow-hero-dark.png
   :class: tb-screenshot-dark
   :width: 356px
   :alt: A narrow sidebar and a wide content pane with the sash between them — dark theme

Usage
-----

Set ``orient=`` to ``HORIZONTAL`` (panes side by side, a vertical sash) or
``VERTICAL`` (panes stacked, a horizontal sash), then ``add`` each pane — usually
a :doc:`Frame <frame>`:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   paned = ttk.Panedwindow(app, orient=HORIZONTAL)
   paned.pack(fill=BOTH, expand=YES)

   sidebar = ttk.Frame(paned, padding=10)
   ttk.Label(sidebar, text="Sidebar").pack()
   paned.add(sidebar, weight=1)

   content = ttk.Frame(paned, padding=10)
   ttk.Label(content, text="Content").pack()
   paned.add(content, weight=4)

   app.mainloop()

Sharing space
-------------

``weight`` sets how the panes divide **extra** space when the window resizes — a
pane with ``weight=4`` grows four times as fast as one with ``weight=1``, so the
content pane above stays dominant while the sidebar stays slim.

For the starting split, set a sash position explicitly with ``sashpos``. The user
can always drag the sash to override it:

.. code-block:: python

   paned.sashpos(0, 200)                    # put the first sash 200px from the start

``sashpos`` only works once the panedwindow has been laid out, so call it after an
``update_idletasks()`` (or from an idle callback) — right after ``add`` it is a
no-op. With three or more panes, sash *N* sits between panes *N* and *N+1* and the
positions stay ordered, so moving one sash can nudge its neighbours.

Adding and removing panes
-------------------------

Panes aren't fixed at construction — manage them at runtime. ``insert`` adds a
pane at a position, ``forget`` removes one (the widget itself survives), and
``pane`` re-reads or changes a pane's settings, so you can freeze a pane by giving
it ``weight=0``:

.. code-block:: python

   paned.insert(0, sidebar, weight=1)       # add a pane at the front
   paned.pane(sidebar, weight=0)            # freeze it: no share of extra space
   paned.forget(sidebar)                    # remove it again

``panes()`` returns the managed pane widgets in order. Unlike the classic
``tk.PanedWindow``, there is no per-pane ``minsize`` — a pane's minimum is driven
by its children's requested size.

Color
-----

``bootstyle`` colors the sash from the semantic palette:

.. code-block:: python

   ttk.Panedwindow(app, orient=VERTICAL, bootstyle="secondary")

Reference
---------

``Panedwindow`` is the native ``ttk.Panedwindow``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Panedwindow API reference </reference/api/panedwindow>` — every option and
  method.
- :ref:`Panedwindow styling options <panedwindow-styling>` — restyle it yourself,
  with the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Notebook <notebook>` — a tabbed rather than split layout.
   - :doc:`Frame <frame>` — the pane containers.
