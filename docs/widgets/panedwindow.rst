Panedwindow
===========

A **panedwindow** holds two or more panes separated by a draggable **sash**, so
the user can resize them against each other — a sidebar next to content, an editor
above a console. ``Panedwindow`` is the native ``ttk.Panedwindow``, styled with
``bootstyle=``. This page covers adding panes, controlling how they share space,
then the ``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A horizontal panedwindow — a narrow sidebar and a wide content pane with the
   sash between them — in light and dark themes.

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

For the starting split, set a sash position explicitly with ``sashpos`` (after the
window is laid out). The user can always drag the sash to override it:

.. code-block:: python

   paned.sashpos(0, 200)                    # put the first sash 200px from the start

Color
-----

``bootstyle`` colors the sash from the semantic palette:

.. code-block:: python

   ttk.Panedwindow(app, orient=VERTICAL, bootstyle="secondary")

API & reference
---------------

``Panedwindow`` is the native ``ttk.Panedwindow`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor and pane methods (``add``,
``insert``, ``forget``, ``sashpos``, ``pane``) see the
`tkinter.ttk.Panedwindow <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Panedwindow>`__
reference.

.. seealso::

   :doc:`Notebook <notebook>` for a tabbed rather than split layout, and
   :doc:`Frame <frame>` for the pane containers. Want to restyle the panedwindow
   yourself? The
   :doc:`Style Reference › Panedwindow </reference/style-reference/panedwindow>`
   and its companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
